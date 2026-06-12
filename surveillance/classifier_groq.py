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
# Tried in order; on a tokens-per-DAY 429 (free tier: 200k TPD for
# gpt-oss-120b, separate pools per model) we fall through to the next model
# instead of sleeping — a daily limit won't reset within a CI run.
GROQ_MODELS = ["openai/gpt-oss-120b", "llama-3.3-70b-versatile"]
GROQ_MODEL = GROQ_MODELS[0]
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
) -> tuple[Classification, str]:
    """One classification via Groq tool-calling. Returns (result, model_tag).

    Walks GROQ_MODELS in order; a daily-quota 429 skips straight to the next
    model. Raises after all models are exhausted."""
    user_lines = [f"Symbol: {symbol}", f"Datetime: {datetime_iso}"]
    if headline_en:
        user_lines.append(f"Headline (EN): {headline_en}")
    if headline_th:
        user_lines.append(f"Headline (TH): {headline_th}")
    user_lines.append(f"URL: {url}")

    last_err: Exception | None = None
    for model in GROQ_MODELS:
        body = json.dumps({
            "model": model,
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

        for attempt in range(retries):
            try:
                with urllib.request.urlopen(req, timeout=60) as r:
                    msg = json.load(r)["choices"][0]["message"]
                call = (msg.get("tool_calls") or [None])[0]
                if call is None:
                    raise RuntimeError(f"no tool call in reply: {msg.get('content')!r:.200}")
                args = call["function"]["arguments"]
                cls = Classification.model_validate(
                    json.loads(args) if isinstance(args, str) else args)
                return cls, f"groq/{model}"
            except urllib.error.HTTPError as e:
                detail = e.read().decode("utf-8", "ignore")[:400]
                last_err = RuntimeError(f"groq HTTP {e.code} [{model}]: {detail[:200]}")
                if e.code == 429:
                    wait = int(e.headers.get("Retry-After") or 2 ** (attempt + 2))
                    # daily quota, or any long cooldown: next model beats
                    # stalling (Retry-After on TPD limits runs to minutes)
                    if wait > 30 or "per day" in detail or "TPD" in detail \
                            or "RPD" in detail:
                        print(f"  [{model}] quota hit (retry-after {wait}s) — trying next model")
                        break
                    time.sleep(wait)
                    continue
                if e.code == 400 and "tool_use_failed" in detail:
                    continue  # malformed tool call from model; regenerate
                raise last_err from e
            except Exception as e:  # malformed JSON / schema mismatch — retry
                last_err = e
    raise RuntimeError(f"groq classify exhausted all models: {last_err}")
