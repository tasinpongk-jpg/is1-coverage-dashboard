"""Build data/oppday-minutes.json from Opp Day summaries in the Obsidian vault.

Source files are produced manually on the MacBook and land via OneDrive sync at:
  {VAULT_ROOT}/Work-SET/Listed Company/3-Outputs/02-Deliverables/Reports/
    {TICKER}_oppday_{period}_summary.md

Usage:
  python scripts/build_oppday_minutes.py          # rebuild JSON if reports changed
  python scripts/build_oppday_minutes.py --push   # also git commit + push when changed

VAULT_ROOT env var overrides the default OneDrive path (so the same script can
run on macOS, where the OneDrive mount point differs).
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA_FILE = REPO / "data" / "oppday-minutes.json"
TICKERS_FILE = REPO / "data" / "tickers.json"

DEFAULT_VAULT = Path.home() / "OneDrive - The Stock Exchange of Thailand" / "Claude-Vault"
REPORTS_SUBPATH = Path("Work-SET") / "Listed Company" / "3-Outputs" / "02-Deliverables" / "Reports"

FILENAME_RE = re.compile(r"^(?P<ticker>[A-Z0-9]+)_oppday_(?P<period>[a-z0-9]+)_summary\.md$")
DATE_LINE_RE = re.compile(r"\*\*วันที่:\*\*\s*(.+)")
OVERVIEW_HEADING_RE = re.compile(r"^##\s*1\.?\s*ภาพรวมธุรกิจ\s*$", re.MULTILINE)

OVERVIEW_MAX_CHARS = 300

# oppday-minutes.html filters on data-val="PFREIT" and styles .s-PFREIT;
# tickers.json spells the same sector "PF&REIT".
SECTOR_LABELS = {"PF&REIT": "PFREIT"}


def period_label(filename_segment: str) -> str:
    m = re.fullmatch(r"ye(\d{4})", filename_segment)
    if m:
        return f"YE/{m.group(1)}"
    m = re.fullmatch(r"q([1-4])y?(\d{4})", filename_segment)
    if m:
        return f"Q{m.group(1)}/{m.group(2)}"
    return filename_segment.upper()


def extract_period(content: str) -> str:
    m = DATE_LINE_RE.search(content)
    return m.group(1).strip() if m else ""


def extract_overview(content: str) -> str:
    m = OVERVIEW_HEADING_RE.search(content)
    if not m:
        return ""
    rest = content[m.end():].lstrip("\n")
    paragraph = rest.split("\n\n", 1)[0].replace("\n", " ").strip()
    return paragraph[:OVERVIEW_MAX_CHARS]


def guess_source(content: str) -> str:
    # The Jun-2026 manual build tagged each report by what material the Mac
    # transcription used; new files can only be inferred from the text itself.
    has_slides = "[Slide" in content
    has_qa = any(marker in content for marker in ("ถาม-ตอบ", "Q&A", "คำถาม"))
    if has_slides and has_qa:
        return "transcript+slides"
    if has_slides:
        return "slides-only"
    return "transcript-only"


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build(reports_dir: Path) -> dict:
    ticker_meta = {t["tk"]: t for t in load_json(TICKERS_FILE)["tickers"]}
    previous_sources: dict[str, str] = {}
    if DATA_FILE.exists():
        previous_sources = {
            s["ticker"]: s["source"] for s in load_json(DATA_FILE).get("summaries", [])
        }

    summaries = []
    period_segments: dict[str, int] = {}
    for path in sorted(reports_dir.iterdir()):
        m = FILENAME_RE.match(path.name)
        if not m:
            continue
        ticker = m.group("ticker")
        seg = m.group("period")
        period_segments[seg] = period_segments.get(seg, 0) + 1
        content = path.read_text(encoding="utf-8")
        meta = ticker_meta.get(ticker)
        if meta is None:
            print(f"WARN: {ticker} not in tickers.json — rm/sector left blank", file=sys.stderr)
        summaries.append({
            "ticker": ticker,
            "rm": meta["rm"] if meta else "",
            "sector": SECTOR_LABELS.get(meta["sector"], meta["sector"]) if meta else "",
            "period": extract_period(content),
            "source": previous_sources.get(ticker) or guess_source(content),
            "overview": extract_overview(content),
            "content": content,
        })

    if not summaries:
        sys.exit(f"ERROR: no report files matched in {reports_dir}")

    dominant_segment = max(period_segments, key=period_segments.get)
    return {
        "generated": datetime.date.today().isoformat(),
        "period": period_label(dominant_segment),
        "total": len(summaries),
        "summaries": summaries,
    }


def unchanged(old: dict, new: dict) -> bool:
    keys = ("period", "total", "summaries")
    return all(old.get(k) == new.get(k) for k in keys)


def git(*args: str) -> None:
    subprocess.run(["git", "-C", str(REPO), *args], check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--push", action="store_true", help="git commit + push when changed")
    args = parser.parse_args()

    vault = Path(os.environ.get("VAULT_ROOT", DEFAULT_VAULT))
    reports_dir = vault / REPORTS_SUBPATH
    if not reports_dir.is_dir():
        sys.exit(f"ERROR: reports folder not found: {reports_dir}")

    new = build(reports_dir)

    if DATA_FILE.exists() and unchanged(load_json(DATA_FILE), new):
        print(f"No change ({new['total']} summaries) — nothing to do.")
        return

    DATA_FILE.write_text(
        json.dumps(new, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Wrote {DATA_FILE.name}: {new['total']} summaries, period {new['period']}.")

    if args.push:
        git("pull", "--rebase", "origin", "main")
        git("add", str(DATA_FILE))
        git("commit", "-m", f"oppday minutes refresh {new['generated']} ({new['total']} summaries)")
        git("push", "origin", "main")
        print("Committed and pushed.")


if __name__ == "__main__":
    main()
