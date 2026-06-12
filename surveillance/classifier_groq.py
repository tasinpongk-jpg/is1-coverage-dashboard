"""Free-tier Groq fall-through for rows no rule matches.

Reuses classifier.py's SYSTEM_PROMPT and Classification schema verbatim, but
calls Groq's OpenAI-compatible endpoint (gpt-oss-120b, free tier ~1k req/day)
instead of the paid Anthropic API — the same zero-cost backend as the
"AI Agent" project. The unclassified queue grows by only a handful of rows a
day, so the free quota is never a constraint.

Stdlib-only on purpose (urllib): no new dependency for CI.

Activation: set GROQ_API_KEY in the environment (GitHub Actions secret or
local shell). Without it, classify_batch.py behaves exactly as before and
rows fall through to severity='unclassified' for the offline rule miner.
Rows classified here are tagged model='groq/<model>' so mine_rules.py can
mine them as LLM-labeled examples, same as the old Haiku rows.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

from classifier import SYSTEM_PROMPT, TOOL_DEF, Classification

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-120b"
MODEL_TAG = f"groq/{GROQ_MODEL}"


def available() -> bool:
    return bool(os.environ.get("GROQ_API_KEY"))


def classify_one_groq(
    *,
    symbol: str,
    datetime_iso: str,
    headline_en: str | None,
    headline_th: str | None,
    url: str,
    retries: int = 3,
) -> Classification:
    """One classification via Groq tool-calling. Raises on exhaustion."""
    user_lines = [f"Symbol: {symbol}", f"Datetime: {datetime_iso}"]
    if headline_en:
        user_lines.append(f"Headline (EN): {headline_en}")
    if headline_th:
        user_lines.append(f"Headline (TH): {headline_th}")
    user_lines.append(f"URL: {url}")

    body = json.dumps({
        "model": GROQ_MODEL,
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": "\n".join(user_lines)},
        ],
        "tools": [{
            "type": "function",
            "function": {
                "name": TOOL_DEF["name"],
                "description": TOOL_DEF["description"],
                "parameters": TOOL_DEF["input_schema"],
            },
        }],
        "tool_choice": {"type": "function",
                        "function": {"name": TOOL_DEF["name"]}},
    }).encode()

    req = urllib.request.Request(GROQ_URL, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
        "User-Agent": "is1-surveillance/1.0",
    })

    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                msg = json.load(r)["choices"][0]["message"]
            call = (msg.get("tool_calls") or [None])[0]
            if call is None:
                raise RuntimeError(f"no tool call in reply: {msg.get('content')!r:.200}")
            args = call["function"]["arguments"]
            return Classification.model_validate(
                json.loads(args) if isinstance(args, str) else args)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "ignore")[:200]
            last_err = RuntimeError(f"groq HTTP {e.code}: {detail}")
            if e.code == 429:  # free-tier rate limit
                time.sleep(int(e.headers.get("Retry-After") or 2 ** (attempt + 2)))
                continue
            if e.code == 400 and "tool_use_failed" in detail:
                continue  # malformed tool call from model; regenerate
            raise last_err from e
        except Exception as e:  # malformed JSON / schema mismatch — retry
            last_err = e
    raise RuntimeError(f"groq classify failed after {retries} tries: {last_err}")
