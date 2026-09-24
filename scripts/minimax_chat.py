"""Minimal stdlib client for MiniMax M3 text calls.

Uses MiniMax's Anthropic-compatible Messages endpoint (same wire shape as
scripts/enrich_filing.py), so thinking blocks are filtered out and only the
reply text comes back. No third-party dependency, so it runs in any CI job.

Env:
    MINIMAX_API_KEY    required
    MINIMAX_BASE_URL   optional, default https://api.minimax.io/anthropic
    MINIMAX_MODEL      optional, default MiniMax-M3
"""

import json
import os
import time
import urllib.error
import urllib.request

BASE_URL = os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.io/anthropic").rstrip("/")
MODEL = os.environ.get("MINIMAX_MODEL", "MiniMax-M3")


def available():
    return bool(os.environ.get("MINIMAX_API_KEY"))


def chat(system, user, *, max_tokens=4000, temperature=0.2, timeout=120, retries=3):
    """Return the reply text for one system + user turn. Raises on failure."""
    body = json.dumps({
        "model": MODEL,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/v1/messages", data=body, headers={
        "x-api-key": os.environ["MINIMAX_API_KEY"],
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
    }, method="POST")
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "ignore")[:300]
            if (e.code == 429 or e.code >= 500) and attempt < retries:
                wait = int(e.headers.get("Retry-After") or 2 ** (attempt + 2))
                print(f"MiniMax HTTP {e.code}, retrying in {wait}s...")
                time.sleep(wait)
                continue
            raise RuntimeError(f"MiniMax API {e.code}: {detail}") from e
    text = "".join(b.get("text", "") for b in data.get("content", [])
                   if b.get("type") == "text").strip()
    if not text:
        raise RuntimeError(f"MiniMax returned no text (stop_reason={data.get('stop_reason')})")
    return text
