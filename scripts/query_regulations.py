"""Ask a question against the regulations File Search store (Lex, from the CLI).

A thin local tester for the same Gemini File Search call worker.js makes — handy
for validating the store without the dashboard, and free of curl-quoting pain.

Usage:
    GEMINI_API_KEY=... python3 scripts/query_regulations.py "your question"

Prints the answer and the citation titles + page numbers it grounded on.
"""

import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "regulations-index.json"
MODEL = os.environ.get("LEX_MODEL", "gemini-2.5-flash")
KEY = os.environ.get("GEMINI_API_KEY", "")


def main():
    if not KEY:
        raise SystemExit("GEMINI_API_KEY is not set")
    if len(sys.argv) < 2:
        raise SystemExit('usage: python3 scripts/query_regulations.py "your question"')
    question = " ".join(sys.argv[1:])
    store = json.loads(MANIFEST.read_text(encoding="utf-8"))["store"]

    body = {
        "contents": [{"role": "user", "parts": [{"text": question}]}],
        "tools": [{"file_search": {"file_search_store_names": [store]}}],
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={KEY}",
        data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read())

    cand = (data.get("candidates") or [{}])[0]
    parts = cand.get("content", {}).get("parts", [])
    answer = "".join(p.get("text", "") for p in parts).strip()
    chunks = cand.get("groundingMetadata", {}).get("groundingChunks", [])
    cites = []
    for c in chunks:
        rc = c.get("retrievedContext", {})
        page = rc.get("pageNumber")
        cites.append(rc.get("title", "?") + (f" p.{page}" if page else ""))

    print("\nANSWER:\n" + (answer or "(no answer)"))
    print("\nCITATIONS: " + (", ".join(dict.fromkeys(cites)) or "(none)"))


if __name__ == "__main__":
    main()
