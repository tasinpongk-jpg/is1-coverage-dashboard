#!/usr/bin/env python3
"""Build data/company-people.json: board of directors and major shareholders
for every coverage ticker, from the SET factsheet API.

Sources (no key; same cookie warmup as build_ticker_summary.py):
  /api/set/company/{TK}/board-of-director?lang=en|th   [{name, positions[]}]
  /api/set/stock/{TK}/shareholder?lang=en              {bookCloseDate, caType,
      totalShareholder, percentScriptless, majorShareholders[], freeFloat{}}

SET publishes no change dates for either list, so the builder keeps its own:
  * board: compares today's directors with the previous file and appends a
    dated entry (joined / left / role changed) when they differ. The first
    run records no changes, only the starting board.
  * shareholders: move with the record date (book closure), not the calendar.
    When the record date changes, the previous top 10 goes into history.
A failed fetch keeps the previous record for that ticker; nothing is wiped.

PF & REIT names return an empty board: a trust or fund has no board of its
own, its manager does. Those are marked boardApplicable = false.

Usage:
  python scripts/build_company_people.py                     # all tickers
  python scripts/build_company_people.py --tickers AWC,CPN   # subset
  python scripts/build_company_people.py --out /tmp/x.json   # dry run elsewhere
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_ticker_summary import (  # noqa: E402
    HTTP_TIMEOUT, SET_MAX, _set_get, _set_warmup,
)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT = DATA_DIR / "company-people.json"
BKK = timezone(timedelta(hours=7))

BOARD_HISTORY_MAX = 40        # dated board change entries kept per ticker
HOLDER_SNAPSHOTS_MAX = 8      # previous record dates kept per ticker
HISTORY_TOP_N = 10            # holders stored per historical snapshot

INDEPENDENT = re.compile(r"\bINDEPENDENT\b|กรรมการอิสระ", re.I)
CHAIR = re.compile(r"^CHAIRMAN OF THE BOARD|^ประธานกรรมการ$|^ประธานคณะกรรมการ$", re.I)
AUDIT = re.compile(r"AUDIT COMMITTEE|กรรมการตรวจสอบ", re.I)


# ── pure helpers (unit tested in tests/test_company_people.py) ───────────────

def name_key(name: str) -> str:
    """Stable identity for a director: case and spacing insensitive."""
    return re.sub(r"\s+", " ", str(name or "")).strip().upper()


def parse_board(en: list | None, th: list | None) -> list[dict]:
    """Merge the EN and TH board lists. SET returns both in the same order;
    Thai names are attached by position only when both lists have the same
    length, so a mismatch never pairs a name with the wrong person."""
    en = en if isinstance(en, list) else []
    th = th if isinstance(th, list) else []
    pair = len(th) == len(en)
    out = []
    for i, d in enumerate(en):
        positions = [p.strip() for p in (d.get("positions") or []) if str(p).strip()]
        t = th[i] if pair else {}
        out.append({
            "name": re.sub(r"\s+", " ", str(d.get("name") or "")).strip(),
            "nameTh": re.sub(r"\s+", " ", str(t.get("name") or "")).strip() or None,
            "positions": positions,
            "positionsTh": [p.strip() for p in (t.get("positions") or []) if str(p).strip()] or None,
            "independent": any(INDEPENDENT.search(p) for p in positions),
            "chair": any(CHAIR.search(p) for p in positions),
            "audit": any(AUDIT.search(p) for p in positions),
        })
    return out


def parse_shareholders(d: dict | None) -> dict | None:
    if not isinstance(d, dict) or not d.get("majorShareholders"):
        return None
    ff = d.get("freeFloat") or {}
    return {
        "recordDate": str(d.get("bookCloseDate") or "")[:10] or None,
        "caType": d.get("caType") or None,
        "totalShareholder": d.get("totalShareholder"),
        "percentScriptless": d.get("percentScriptless"),
        "freeFloat": {
            "percent": ff.get("percentFreeFloat"),
            "holders": ff.get("numberOfHolder"),
            "recordDate": str(ff.get("bookCloseDate") or "")[:10] or None,
        } if ff else None,
        "major": [{
            "rank": h.get("sequence"),
            "name": re.sub(r"\s+", " ", str(h.get("name") or "")).strip(),
            "shares": h.get("numberOfShare"),
            "pct": h.get("percentOfShare"),
            "nvdr": bool(h.get("isThaiNVDR")),
        } for h in d["majorShareholders"]],
    }


def diff_board(prev: list[dict], cur: list[dict]) -> dict | None:
    """Joined / left / role changes between two board lists, or None."""
    p = {name_key(d["name"]): d for d in prev}
    c = {name_key(d["name"]): d for d in cur}
    joined = [c[k]["name"] for k in c if k not in p]
    left = [p[k]["name"] for k in p if k not in c]
    changed = [{"name": c[k]["name"], "from": p[k]["positions"], "to": c[k]["positions"]}
               for k in c if k in p and sorted(p[k]["positions"]) != sorted(c[k]["positions"])]
    if not (joined or left or changed):
        return None
    return {"joined": joined, "left": left, "changed": changed}


def merge_ticker(prev: dict | None, board: list[dict] | None,
                 holders: dict | None, bucket: str, today: str) -> dict:
    """Fold today's fetch into the previous record. `board` / `holders` are
    None when that fetch failed; the previous value is then kept as is."""
    prev = prev or {}
    rec = {
        "boardApplicable": prev.get("boardApplicable", True),
        "board": prev.get("board") or [],
        "boardSince": prev.get("boardSince"),
        "boardChanges": list(prev.get("boardChanges") or []),
        "shareholders": prev.get("shareholders"),
        "shareholderHistory": list(prev.get("shareholderHistory") or []),
        "checked": prev.get("checked"),
    }
    if board is not None:
        if not board and bucket == "PF&REIT":
            rec["boardApplicable"] = False
            rec["board"] = []
        elif board:
            rec["boardApplicable"] = True
            had = bool(prev.get("board"))
            change = diff_board(prev.get("board") or [], board) if had else None
            if change:
                rec["boardChanges"] = ([{"date": today, **change}] + rec["boardChanges"])[:BOARD_HISTORY_MAX]
                rec["boardSince"] = today
            elif not had:
                rec["boardSince"] = None      # first sighting: start date unknown
            rec["board"] = board
    if holders is not None:
        old = rec["shareholders"]
        if old and old.get("recordDate") and old.get("recordDate") != holders.get("recordDate"):
            snap = {"recordDate": old["recordDate"], "caType": old.get("caType"),
                    "totalShareholder": old.get("totalShareholder"),
                    "top": [{"name": h["name"], "pct": h["pct"], "shares": h.get("shares")}
                            for h in (old.get("major") or [])[:HISTORY_TOP_N]]}
            hist = [s for s in rec["shareholderHistory"] if s.get("recordDate") != snap["recordDate"]]
            rec["shareholderHistory"] = ([snap] + hist)[:HOLDER_SNAPSHOTS_MAX]
        rec["shareholders"] = holders
    if board is not None or holders is not None:
        rec["checked"] = today
    return rec


# ── fetch ────────────────────────────────────────────────────────────────────

async def fetch_one(client: httpx.AsyncClient, sem: asyncio.Semaphore, tk: str):
    en, th, sh = await asyncio.gather(
        _set_get(client, f"/api/set/company/{tk}/board-of-director?lang=en", sem, tk),
        _set_get(client, f"/api/set/company/{tk}/board-of-director?lang=th", sem, tk),
        _set_get(client, f"/api/set/stock/{tk}/shareholder?lang=en", sem, tk),
    )
    board = parse_board(en, th) if isinstance(en, list) else None
    holders = parse_shareholders(sh) if isinstance(sh, dict) else None
    return tk, board, holders


async def run(tickers: list[dict], prev_doc: dict, today: str) -> dict:
    sem = asyncio.Semaphore(SET_MAX)
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, follow_redirects=True) as client:
        await _set_warmup(client)
        results = await asyncio.gather(*[fetch_one(client, sem, t["tk"]) for t in tickers])

    prev_map = prev_doc.get("tickers") or {}
    out = dict(prev_map)
    errors, counts = [], {"board": 0, "shareholders": 0, "boardChanged": 0, "newRecordDate": 0}
    bucket = {t["tk"]: t.get("sector") or t.get("bucket") for t in tickers}
    for tk, board, holders in results:
        if board is None:
            errors.append({"tk": tk, "what": "board"})
        if holders is None:
            errors.append({"tk": tk, "what": "shareholders"})
        before = prev_map.get(tk) or {}
        rec = merge_ticker(before, board, holders, bucket.get(tk) or "", today)
        out[tk] = rec
        counts["board"] += bool(rec["board"])
        counts["shareholders"] += bool(rec["shareholders"])
        counts["boardChanged"] += bool(rec["boardChanges"] and rec["boardChanges"][0]["date"] == today
                                       and len(rec["boardChanges"]) > len(before.get("boardChanges") or []))
        counts["newRecordDate"] += bool(len(rec["shareholderHistory"]) > len(before.get("shareholderHistory") or []))
    return {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "asOf": today,
        "source": "SET.or.th factsheet API: /company/{TK}/board-of-director, /stock/{TK}/shareholder",
        "counts": {**counts, "tickers": len(tickers)},
        "errors": errors,
        "tickers": dict(sorted(out.items())),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tickers", help="comma-separated subset, e.g. AWC,CPN")
    ap.add_argument("--out", default=str(OUT), help="output path (default data/company-people.json)")
    ap.add_argument("--prev", default=str(OUT), help="previous file to diff against")
    args = ap.parse_args()

    universe = json.loads((DATA_DIR / "tickers.json").read_text(encoding="utf-8"))["tickers"]
    if args.tickers:
        want = {s.strip().upper() for s in args.tickers.split(",") if s.strip()}
        universe = [t for t in universe if t["tk"] in want]
    prev_path = Path(args.prev)
    prev_doc = json.loads(prev_path.read_text(encoding="utf-8")) if prev_path.exists() else {}
    today = datetime.now(BKK).date().isoformat()

    doc = asyncio.run(run(universe, prev_doc, today))
    ok_share = doc["counts"]["shareholders"] / max(1, len(universe))
    Path(args.out).write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    c = doc["counts"]
    print(f"Wrote {args.out}: {c['tickers']} tickers, board {c['board']}, shareholders {c['shareholders']}, "
          f"board changed today {c['boardChanged']}, new record dates {c['newRecordDate']}, errors {len(doc['errors'])}")
    # Refuse to call a mostly failed run a success, so CI shows it.
    return 0 if ok_share >= 0.8 else 1


if __name__ == "__main__":
    sys.exit(main())
