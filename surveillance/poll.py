"""Surveillance poll loop.

Phase 1 (this file): fetch the SET disclosure firehose for the lookback window,
post-filter to coverage, dedup against the local DuckDB cache, return + log
only new items.
Phase 2 (classify_batch.py): rules-first + Haiku fallback classifier writes
rows to the classifications table. Run automatically in CI after poll.py; for
local one-shot use, pass --classify to this script.
Phase 3 (route_alerts.py): email / LINE / Telegram routing by severity.

Why firehose, not per-symbol: the per-symbol endpoint silently drops ~12% of
disclosures (PFREIT distributions, NAV reports, dividend payments, no-right
adjustments, lowercased F45). The unfiltered endpoint is the only one that
returns the superset. SET also exposes no working server-side industry filter
— every shape we probed returns the same 2701-item firehose. See issue #12 +
scripts/probe_industry_endpoint.py for the receipt.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from typing import Any

from client import SetNewsClient
from coverage import ALL_TICKERS, COVERAGE
from store import insert_new_items, stats


def poll_firehose(lookback_days: int = 7) -> list[dict[str, Any]]:
    """Default path: one EN + one TH firehose call, post-filter to coverage."""
    from datetime import timedelta
    today = datetime.now().date()
    from_d = today - timedelta(days=lookback_days)
    coverage_set = set(ALL_TICKERS)
    with SetNewsClient() as client:
        en = client.search_all("en", from_d, today)
        th = client.search_all("th", from_d, today)
    for item in en:
        item.setdefault("lang", "en")
    for item in th:
        item.setdefault("lang", "th")
    all_items = en + th
    in_scope = [it for it in all_items if (it.get("symbol") or "").upper() in coverage_set]
    print(
        f"firehose: en={len(en)}  th={len(th)}  "
        f"total={len(all_items)}  in-coverage={len(in_scope)}"
    )
    new = insert_new_items(in_scope)
    by_sym: dict[str, int] = {}
    for it in new:
        sym = (it.get("symbol") or "").upper()
        by_sym[sym] = by_sym.get(sym, 0) + 1
    if by_sym:
        print("new items per symbol:")
        for sym, n in sorted(by_sym.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  {sym:8s}  +{n}")
    return new


def poll_per_symbol(tickers: list[str], lookback_days: int = 7) -> list[dict[str, Any]]:
    """Fallback for `--tickers` override: legacy per-symbol fetch.

    Known to drop ~12% of items vs. firehose — kept only because users may want
    to point at a single ticker without pulling the whole market.
    """
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
    p.add_argument(
        "--classify",
        action="store_true",
        help="After polling, invoke classify_batch.py on the local DB. "
             "Rules-tier only by default; pass --classify-haiku to enable Haiku fallback.",
    )
    p.add_argument(
        "--classify-haiku",
        action="store_true",
        help="With --classify, allow rules-ambiguous rows to fall through to Haiku (API cost).",
    )
    args = p.parse_args()

    started = datetime.now()
    print(f"=== surveillance poll @ {started.isoformat(timespec='seconds')} ===")
    if args.tickers:
        print(
            f"scope: {len(args.tickers)} ticker(s) (override, per-symbol path) "
            f"— lookback {args.lookback_days} day(s)"
        )
        new = poll_per_symbol(args.tickers, lookback_days=args.lookback_days)
    elif args.sector:
        scope = COVERAGE[args.sector]
        print(
            f"scope: sector={args.sector} ({len(scope)} ticker(s), per-symbol path) "
            f"— lookback {args.lookback_days} day(s)"
        )
        new = poll_per_symbol(scope, lookback_days=args.lookback_days)
    else:
        print(
            f"scope: full coverage ({len(ALL_TICKERS)} tickers, firehose path) "
            f"— lookback {args.lookback_days} day(s)"
        )
        new = poll_firehose(lookback_days=args.lookback_days)
    print(f"\n=== sweep complete: {len(new)} new disclosure(s) added ===")
    s = stats()
    print(f"DB total rows: {s['total']}")
    print("Latest 5 in DB:")
    for sym, dt, hl in s["latest"]:
        print(f"  {dt}  {sym:8s}  {(hl or '')[:80]}")

    if args.classify:
        print("\n=== invoking classify_batch.py ===")
        cmd = [sys.executable, "classify_batch.py"]
        if not args.classify_haiku:
            cmd.append("--rules-only")
        subprocess.run(cmd, check=False)


if __name__ == "__main__":
    main()
