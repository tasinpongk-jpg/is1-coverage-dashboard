#!/usr/bin/env python3
"""Merge in-session LLM synthesis JSON into company-reports.json + vault MDs.

Mirrors build_company_reports.llm_report's merge semantics: start from the
deterministic base, overlay the synthesized fields, stamp the model, write both
the dashboard JSON and the per-ticker vault markdown.

Synthesis files live in data/synthesis/out/<TK>.json with any subset of:
  tone thesis summary business financialSnapshot mdaSynthesis
  fsNotesSynthesis watchItems questions qualityFlags

Usage:
  python scripts/ingest_synthesis.py
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_company_reports as bcr  # type: ignore

OUT_DIR = bcr.DATA_DIR / "synthesis" / "out"
MODEL = "claude-opus-4-8 (in-session)"


def main() -> None:
    summary = bcr.load_json(bcr.TICKER_SUMMARY, {})
    all_t = {(t.get("tk") or "").upper(): t for t in (summary.get("tickers") or [])}
    notes_map = bcr.load_json(bcr.VAULT_NOTES, {}).get("tickers") or {}
    disclosure_payload = bcr.load_json(bcr.DISCLOSURES, {})
    oppday_payload = bcr.load_json(bcr.OPPDAY, {})

    out = bcr.load_json(bcr.OUT, {})
    reports = out.get("reports") or {}
    listed_root = bcr.find_listed_root()
    generated = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

    n = skipped = 0
    for f in sorted(OUT_DIR.glob("*.json")):
        tk = f.stem.upper()
        t = all_t.get(tk)
        if not t:
            print(f"  skip {tk}: not in ticker-summary"); skipped += 1; continue
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  skip {tk}: bad JSON ({e})"); skipped += 1; continue

        ctx = bcr.build_context(t, notes_map.get(tk) or {}, disclosure_payload, oppday_payload)
        chash = bcr.source_hash(ctx)
        base = bcr.deterministic_report(ctx, generated)
        base.update({k: data.get(k, base.get(k)) for k in data.keys()})
        base["model"] = MODEL
        base["generated"] = generated
        reports[tk] = base

        if listed_root:
            md = bcr.markdown_report(base, chash)
            path = bcr.report_path(listed_root, base)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(md, encoding="utf-8")
        n += 1

    out["reports"] = reports
    insession = sum(1 for v in reports.values() if MODEL in (v.get("model") or ""))
    out["generated"] = generated
    out["model"] = MODEL if insession == len(reports) else "mixed"
    out["totals"] = {"reports": len(reports), "llm": True, "inSession": insession, "errors": skipped}
    out.setdefault("meta", {})["synthesis"] = (
        f"{insession} reports synthesized in-session by Claude (no API key)")
    bcr.write_json(bcr.OUT, out)
    print(f"ingested {n} synthesized reports ({skipped} skipped) -> {bcr.OUT.name}"
          + (f" + vault MDs under {listed_root}" if listed_root else " (no vault root found)"))


if __name__ == "__main__":
    main()
