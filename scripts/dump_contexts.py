#!/usr/bin/env python3
"""Dump per-ticker context JSON for in-session LLM synthesis.

Reuses build_company_reports.build_context so the context is byte-identical to
what the API path (llm_report) would see. Champ's Claude session reads these,
writes synthesis JSON to data/synthesis/out/<TK>.json, then ingest_synthesis.py
merges them back exactly like llm_report would.

Usage:
  python scripts/dump_contexts.py AAI AMATA ...        # specific
  python scripts/dump_contexts.py --filing-summary     # all with a 2025FY digest
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_company_reports as bcr  # type: ignore

CTX_DIR = bcr.DATA_DIR / "synthesis" / "context"


def resolve_tickers(args: list[str]) -> list[str]:
    if "--all" in args:
        summary = bcr.load_json(bcr.TICKER_SUMMARY, {})
        return sorted((t.get("tk") or "").upper() for t in (summary.get("tickers") or []) if t.get("tk"))
    if "--filing-summary" in args:
        notes = bcr.load_json(bcr.VAULT_NOTES, {}).get("tickers") or {}
        return sorted(t for t, v in notes.items() if v.get("filingSummary"))
    return [a.upper() for a in args if not a.startswith("--")]


def main(argv: list[str]) -> None:
    wanted = set(resolve_tickers(argv))
    summary = bcr.load_json(bcr.TICKER_SUMMARY, {})
    notes_map = bcr.load_json(bcr.VAULT_NOTES, {}).get("tickers") or {}
    disclosure_payload = bcr.load_json(bcr.DISCLOSURES, {})
    oppday_payload = bcr.load_json(bcr.OPPDAY, {})

    CTX_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    for t in summary.get("tickers") or []:
        tk = (t.get("tk") or "").upper()
        if tk not in wanted:
            continue
        ctx = bcr.build_context(t, notes_map.get(tk) or {}, disclosure_payload, oppday_payload)
        (CTX_DIR / f"{tk}.json").write_text(
            json.dumps(ctx, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        n += 1
    print(f"dumped {n} contexts to {CTX_DIR}")


if __name__ == "__main__":
    main(sys.argv[1:])
