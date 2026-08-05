"""Ad-hoc: render the live daily brief payload to a JSON fixture file
so we can eyeball the full output without truncation.

Usage: python tests/render_dry_run.py
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

# Load the live fixture files instead of re-fetching (faster, deterministic).
# disclosure_pulse.json is gitignored (2.1 MB) — fall back to a synthetic
# minimal pulse if missing so this script still runs on a clean checkout.
FIX = REPO / "tests" / "fixtures"
ai = json.loads((FIX / "ai_insights_2026-08-04.json").read_text(encoding="utf-8"))
brief = json.loads((FIX / "morning_brief_2026-08-04.json").read_text(encoding="utf-8"))
tickers = json.loads((FIX / "tickers_2026-08-04.json").read_text(encoding="utf-8"))
_pulse_path = FIX / "disclosure_pulse_2026-08-04.json"
pulse = json.loads(_pulse_path.read_text(encoding="utf-8")) if _pulse_path.exists() else {"filings": []}

import build_daily_brief as b  # noqa: E402

rm_key = "C"
rm_tickers = {t["tk"] for t in tickers["tickers"] if t.get("rm") == rm_key}
ai_asof = b._parse_iso_date(ai.get("asOf") or "")
brief_asof = b._parse_iso_date(brief.get("asOf") or "")
overall_asof = min(ai_asof or "?", brief_asof or "?")

embeds = [
    b._build_headline_embed(ai, overall_asof),
    b._build_sector_pulse_embed(brief),
    b._build_rm_watch_embed(brief, rm_tickers),
    b._build_filings_today_embed(pulse, rm_tickers, overall_asof),
]
embeds = b._clamp_fields(embeds)
embeds = b._validate_total_chars(embeds)

payload = {
    "username": "IS1 Daily Brief",
    "content": f"**Daily Brief — {overall_asof}** · {rm_key} coverage",
    "embeds": embeds,
}
total_chars = sum(len(json.dumps(e)) for e in embeds)
print(f"embeds: {len(embeds)}, total chars: {total_chars}/{b.DISCORD_TOTAL_CHARS_MAX}")
out_path = FIX / "dry_run_payload.json"
out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"saved to {out_path}")