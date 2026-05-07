"""Surveillance poll loop.

Phase 1 (this file): for each ticker in scope, fetch recent disclosures (EN+TH),
dedup against the local DuckDB cache, return + log only new items.
Phase 2 (next session): route new items through Claude classifier.
Phase 3 (after that): LINE / Telegram alert routing by severity.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from typing import Any

from client import SetNewsClient
from coverage import ALL_TICKERS, COVERAGE
from store import insert_new_items, stats


def poll_once(tickers: list[str], lookback_days: int = 7) -> list[dict[str, Any]]:
    """Single sweep across `tickers`. Returns the genuinely new items."""
    new_total: list[dict[str, Any]] = []
    with SetNewsClient() as client:
        for sym in tickers:
            try:
                items = client.search_recent(sym, lookback_days=lookback_days)
            except Exception as e:  # noqa: BLE001
                print(f"[{sym}] ERR {type(e).__name__}: {e}")
                continue
            new = insert_new_items(items)
            tag = f"+{len(new)} new" if new else "no change"
            print(f"[{sym}] fetched={len(items):3d}  {tag}")
            new_total.extend(new)
    return new_total


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--tickers",
        nargs="*",
        help="Override ticker list (default: full 34-name coverage).",
    )
    p.add_argument(
        "--sector",
        choices=list(COVERAGE),
        help="Limit to one sector (FOOD or PROP).",
    )
    p.add_argument("--lookback-days", type=int, default=7)
    args = p.parse_args()

    if args.tickers:
        scope = args.tickers
    elif args.sector:
        scope = COVERAGE[args.sector]
    else:
        scope = ALL_TICKERS

    started = datetime.now()
    print(f"=== surveillance poll @ {started.isoformat(timespec='seconds')} ===")
    print(f"scope: {len(scope)} ticker(s) — lookback {args.lookback_days} day(s)")
    new = poll_once(scope, lookback_days=args.lookback_days)
    print(f"\n=== sweep complete: {len(new)} new disclosure(s) added ===")
    s = stats()
    print(f"DB total rows: {s['total']}")
    print("Latest 5 in DB:")
    for sym, dt, hl in s["latest"]:
        print(f"  {dt}  {sym:8s}  {(hl or '')[:80]}")


if __name__ == "__main__":
    main()
