"""Layer 1 of the Hermes MDA-FS harvester — discover new SET filings for IS1 tickers.

For each IS1 ticker, query SET news/search for the trailing N days, filter to
MDA / FS / AUDITOR filings via headline + tag + fileType, and write the
candidate list to data/harvest-queue.json. Layer 2 (harvest_download.py)
picks up the queue.

Why per-ticker instead of firehose:
    SET's news/search returns a hard cap of ~400 items per call. The firehose
    on busy days exceeds this. Per-ticker search returns the per-issuer items,
    well under the cap, and lets us filter to MDA/FS only. The firehose path
    is kept as `--mode firehose` for catch-up scans.

Idempotent:
    - news_id is the primary dedup key.
    - Re-running is safe: items already in the queue or marked done are skipped.
    - State persists in data/harvest-queue.json (queue) and
      data/harvest-state.json (downloaded SHA-256s).

Usage:
    python scripts/harvest_filings.py                    # default: per-ticker, 14d lookback
    python scripts/harvest_filings.py --ticker AP        # single ticker (smoke test)
    python scripts/harvest_filings.py --mode firehose    # full market, capped at 400
    python scripts/harvest_filings.py --dry-run          # don't write queue
    python scripts/harvest_filings.py --lookback 60      # 60-day window
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any, Literal

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "surveillance"))

from client import SetNewsClient  # noqa: E402

DATA_DIR = REPO / "data"
QUEUE_FILE = DATA_DIR / "harvest-queue.json"
STATE_FILE = DATA_DIR / "harvest-state.json"
TICKERS_FILE = DATA_DIR / "tickers.json"

# ---------------------------------------------------------------- classification

# Verified against TPAC MDA + FS disclosures on 2026-08-07:
#   headline "Management Discussion and Analysis Quarter 2..." → MDA, fileType=PDF
#   headline "Financial Statement Quarter 2/2026 (Reviewed)" → FS, fileType=ZIP
#   tag == "financial-statement" is a strong FS signal
MDA_HEADLINE_PAT = re.compile(r"management\s+discussion\s+(?:and|&)\s+analysis|\bMD\s*&\s*A\b", re.I)
FS_HEADLINE_PAT = re.compile(r"\bfinancial\s+statement\b", re.I)
AUDITOR_HEADLINE_PAT = re.compile(r"\b(?:independent\s+auditor.{0,5}report|auditor.{0,5}report)\b", re.I)
YEARLY_HEADLINE_PAT = re.compile(r"\b(?:yearly|annual|year[\s-]end)\b", re.I)

# Period regexes (filenames + headlines; matches vault_raw_writer.py:_period_from_filing).
# SET headline formats observed (2026-08-08 probe, AP):
#   "Management Discussion and Analysis Quarter 1 Ending 31 Mar 2026"
#   "Financial Statement Quarter 1/2026 (Reviewed)"
#   "Financial Performance Quarter 4 (F45) (Audited)"
RE_PERIOD_FILE = re.compile(r"(20\d{2}(?:Q[1-4]|FY)|\d{4}Q[1-4]|\d{4}FY)")
RE_PERIOD_HEADLINE_QTR_SLASH = re.compile(r"[Qq]uarter\s*([1-4])\s*/\s*(\d{4})")
RE_PERIOD_HEADLINE_Q_SLASH = re.compile(r"\bQ\s*([1-4])\s*/\s*(\d{4})\b")
RE_PERIOD_HEADLINE_FY = re.compile(r"\bFY\s*(\d{4})\b")
# Last resort: "Quarter N" with year inferred from the news datetime
RE_PERIOD_HEADLINE_QTR_BARE = re.compile(r"\b[Qq]uarter\s*([1-4])\b")
# Ending <date> <month> <year> — e.g. "Quarter 2 Ending 30 Jun 2026"
RE_PERIOD_ENDING = re.compile(r"[Ee]nding\s+(?:\d{1,2}\s+)?[A-Za-z]+\s+(\d{4})")
# Buddhist year (2569 = 2026 CE, 2570 = 2027 CE, etc.). Range covers 2550..2599.
RE_PERIOD_BUDDHIST = re.compile(r"\b(25[5-9]\d)\b")


def classify(headline: str, tag: str = "") -> Literal["MDA", "FS", "AUDITOR", "SKIP"]:
    """Return the filing kind based on headline + tag, or SKIP if irrelevant.

    Pure deterministic rules — no m3 here. If a filing matches multiple
    patterns, prefer MDA (rarer) then FS then AUDITOR. Headline matching is
    case-insensitive.
    """
    if MDA_HEADLINE_PAT.search(headline):
        return "MDA"
    if tag == "financial-statement" or FS_HEADLINE_PAT.search(headline):
        return "FS"
    if AUDITOR_HEADLINE_PAT.search(headline):
        return "AUDITOR"
    return "SKIP"


def _is_yearly(headline: str) -> bool:
    """True if the headline indicates a year-end (FY) filing."""
    return bool(YEARLY_HEADLINE_PAT.search(headline))


_MONTH_TO_Q = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def _month_to_quarter(month_name: str) -> int | None:
    """Map month abbreviation to quarter (1-4)."""
    if not month_name:
        return None
    m = month_name.lower()[:3]
    month_num = _MONTH_TO_Q.get(m)
    if month_num is None:
        return None
    return (month_num - 1) // 3 + 1


def _buddhist_to_gregorian(year_str: str) -> str | None:
    """Convert a Buddhist year (2569 = 2026 CE) to Gregorian, or None if invalid."""
    try:
        y = int(year_str)
    except (TypeError, ValueError):
        return None
    if 2500 <= y < 2600:  # Buddhist Era range
        return str(y - 543)
    return None


def parse_period(headline: str, url: str = "", news_datetime: str = "") -> str:
    """Extract a period label like '2026Q2' or '2025FY'.

    Priority (most authoritative first):
      1. From filename or URL (e.g., MDA_AP_2026Q1_E.md -> '2026Q1').
      2. From 'Quarter N Ending <date> <month> <year>' — use the year from
         the Ending clause (most authoritative; some PFREITs label the
         reporting period differently from the quarter-end-date, e.g.
         FPT Q2/2026 filings appear as 'Quarter 3 Ending 30 Jun 2026').
      3. From headline 'Quarter N/YYYY' (Gregorian) — convert Buddhist year
         if the year is in BE range (2550-2599).
      4. From headline 'FY YYYY'.
      5. From 'Yearly/Annual YYYY' -> YYYY FY.
      6. Bare 'Quarter N' + year inferred from news_datetime.
      7. UNKNOWN if nothing matches.
    """
    # 1. Filename / URL (always Gregorian; filenames use the canonical period).
    for source in (headline, url):
        m = RE_PERIOD_FILE.search(source)
        if m:
            return m.group(1)

    # 2. "Ending 30 Jun 2026" — the most authoritative signal. Use the
    #    month in the Ending clause to determine the quarter (NOT the
    #    headline's "Quarter N" token — SET sometimes labels filings by
    #    reporting period rather than quarter-end-date, e.g. FPT Q2/2026
    #    filings appear as "Quarter 3 Ending 30 Jun 2026").
    m = RE_PERIOD_ENDING.search(headline)
    if m:
        ending_year = m.group(1)
        ge_year = _buddhist_to_gregorian(ending_year) or ending_year
        month_m = re.search(r"Ending\s+(?:\d{1,2}\s+)?([A-Za-z]+)", headline)
        if month_m:
            q = _month_to_quarter(month_m.group(1))
            if q:
                return f"{ge_year}Q{q}"
        # No parseable month — fall through to the next priority.
    # If Ending matched but month didn't, still try the other patterns
    # below with a hint to prefer the Ending year.

    # 3. Quarter N/YYYY — convert Buddhist year if needed.
    m = RE_PERIOD_HEADLINE_QTR_SLASH.search(headline) or RE_PERIOD_HEADLINE_Q_SLASH.search(headline)
    if m:
        q, raw_year = m.group(1), m.group(2)
        ge_year = _buddhist_to_gregorian(raw_year) or raw_year
        return f"{ge_year}Q{q}"

    # 4. FY YYYY.
    m = RE_PERIOD_HEADLINE_FY.search(headline)
    if m:
        ge_year = _buddhist_to_gregorian(m.group(1)) or m.group(1)
        return f"{ge_year}FY"

    # 5. Yearly/Annual YYYY -> YYYY FY.
    if _is_yearly(headline):
        ymatch = re.search(r"\b(25\d{2}|20\d{2})\b", headline)
        if ymatch:
            ge_year = _buddhist_to_gregorian(ymatch.group(1)) or ymatch.group(1)
            return f"{ge_year}FY"

    # 6. Bare "Quarter N" + year from news_datetime.
    m = RE_PERIOD_HEADLINE_QTR_BARE.search(headline)
    if m:
        if news_datetime:
            ymatch = re.match(r"(\d{4})", news_datetime)
            if ymatch:
                return f"{ymatch.group(1)}Q{m.group(1)}"

    return "UNKNOWN"


# ---------------------------------------------------------------- queue/state I/O


def load_queue() -> dict[str, Any]:
    """Return existing queue or default. Never raises."""
    if not QUEUE_FILE.exists():
        return {"generated": "", "items": {}}
    try:
        return json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"generated": "", "items": {}}


def load_state() -> dict[str, Any]:
    """Return existing state or default. The state file holds completed downloads
    keyed by news_id → sha256 (so we can detect re-filed duplicates)."""
    if not STATE_FILE.exists():
        return {"completed": {}}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"completed": {}}


def save_queue(queue: dict[str, Any]) -> None:
    queue["generated"] = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    QUEUE_FILE.write_text(
        json.dumps(queue, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------- discovery

Item = dict[str, Any]  # {news_id, ticker, kind, period, headline, datetime, tag, url, status}


def discover_per_ticker(client: SetNewsClient, tickers: list[str], lookback: int) -> list[Item]:
    """One SET call per ticker. Lower call volume than firehose, no 400-cap risk."""
    today = dt.date.today()
    from_d = today - dt.timedelta(days=lookback)
    items: list[Item] = []
    for i, tk in enumerate(tickers):
        try:
            raw = client.search(tk, "en", from_d, today)
        except Exception as exc:  # noqa: BLE001
            print(f"[harvest] [{tk}] ERR {type(exc).__name__}: {exc}", flush=True)
            continue
        added = 0
        for entry in raw:
            headline = entry.get("headline", "")
            tag = entry.get("tag", "") or ""
            kind = classify(headline, tag)
            if kind == "SKIP":
                continue
            period = parse_period(headline, entry.get("url", ""), entry.get("datetime", ""))
            items.append({
                "news_id": str(entry.get("id")),
                "ticker": tk,
                "kind": kind,
                "period": period,
                "headline": headline,
                "datetime": entry.get("datetime", ""),
                "tag": tag,
                "url": entry.get("url", ""),
                "status": "pending",
                "discovered_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                "source": "set_per_symbol",
            })
            added += 1
        if added or (i + 1) % 25 == 0:
            print(f"[harvest] [{tk:8s}] +{added} new MDA/FS candidates ({i+1}/{len(tickers)})", flush=True)
    return items


def discover_firehose(client: SetNewsClient, lookback: int) -> list[Item]:
    """Single call. Capped at ~400/day — use only for catch-up scans."""
    today = dt.date.today()
    from_d = today - dt.timedelta(days=lookback)
    raw = client.search_all("en", from_d, today)
    print(f"[harvest] firehose returned {len(raw)} items", flush=True)
    items: list[Item] = []
    for entry in raw:
        headline = entry.get("headline", "")
        tag = entry.get("tag", "") or ""
        kind = classify(headline, tag)
        if kind == "SKIP":
            continue
        period = parse_period(headline, entry.get("url", ""), entry.get("datetime", ""))
        items.append({
            "news_id": str(entry.get("id")),
            "ticker": (entry.get("symbol") or "").upper(),
            "kind": kind,
            "period": period,
            "headline": headline,
            "datetime": entry.get("datetime", ""),
            "tag": tag,
            "url": entry.get("url", ""),
            "status": "pending",
            "discovered_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "source": "set_firehose",
        })
    return items


# ---------------------------------------------------------------- main

def load_tickers() -> list[str]:
    """Return the 232 IS1 tickers in stable order."""
    j = json.loads(TICKERS_FILE.read_text(encoding="utf-8"))
    return [t["tk"] for t in j.get("tickers", [])]


def merge_into_queue(queue: dict[str, Any], items: list[Item], state: dict[str, Any]) -> int:
    """Insert new items; skip those already completed (in state) or already queued.

    Returns the number of newly added items.
    """
    completed_ids = set(state.get("completed", {}).keys())
    existing_ids = set(queue.get("items", {}).keys())
    added = 0
    items_map = queue.setdefault("items", {})
    for it in items:
        nid = it["news_id"]
        if nid in completed_ids:
            continue  # already downloaded
        if nid in existing_ids:
            continue  # already queued (preserves prior status)
        items_map[nid] = it
        added += 1
    return added


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ticker", action="append", default=[], help="Limit to one or more tickers")
    p.add_argument("--mode", choices=["per-ticker", "firehose"], default="per-ticker")
    p.add_argument("--lookback", type=int, default=14, help="Days back to search (default 14)")
    p.add_argument("--dry-run", action="store_true", help="Print what would be queued, don't write")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    all_tickers = load_tickers()
    tickers = [t.upper() for t in args.ticker] if args.ticker else all_tickers
    if args.ticker:
        print(f"[harvest] ticker filter: {len(tickers)}/{len(all_tickers)}", flush=True)
    else:
        print(f"[harvest] scanning all {len(tickers)} IS1 tickers", flush=True)

    queue = load_queue()
    state = load_state()
    print(f"[harvest] existing queue: {len(queue.get('items', {}))} items, "
          f"completed: {len(state.get('completed', {}))}", flush=True)

    with SetNewsClient() as client:
        if args.mode == "firehose":
            items = discover_firehose(client, args.lookback)
        else:
            items = discover_per_ticker(client, tickers, args.lookback)

    print(f"[harvest] found {len(items)} MDA/FS candidates", flush=True)
    added = merge_into_queue(queue, items, state)
    print(f"[harvest] added {added} new to queue "
          f"(skipped {len(items) - added} already known)", flush=True)

    if args.dry_run:
        print("[harvest] DRY RUN — queue not written", flush=True)
        for it in items[:5]:
            print(f"  sample: {it['ticker']:6s} {it['kind']:7s} {it['period']:8s} "
                  f"#{it['news_id']} {it['headline'][:60]}", flush=True)
        return 0

    save_queue(queue)
    print(f"[harvest] wrote {QUEUE_FILE} (total queue: {len(queue['items'])})", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
