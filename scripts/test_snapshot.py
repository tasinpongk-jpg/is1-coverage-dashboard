"""
Regression tests for fetch_ticker_snapshot's handling of zero-close rows.

SETSMART returns close=0 (with volume=0) on days the ticker didn't trade.
Before fix, these flowed through as real prices and produced spurious
-100% returns on the morning-brief dashboard for illiquid tickers and
during pre-EOD weekday builds.

Run:  python scripts/test_snapshot.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


class _FakeClient:
    def __init__(self, rows): self._rows = rows
    async def __aenter__(self): return self
    async def __aexit__(self, *a): return None


async def _run_snapshot(rows):
    """Invoke fetch_ticker_snapshot against an in-memory rows list."""
    import setsmart_proxy as proxy
    async def _fake_series(client, tk, *, years=1): return rows
    proxy.fetch_eod_series = _fake_series
    return await proxy.fetch_ticker_snapshot(client=None, tk="TEST")


def _eod_row(date_iso, close, volume=1000):
    return {"date": date_iso, "close": close, "totalVolume": volume}


def test_no_trade_today_falls_back_to_prior_day():
    """ZEN-style: 19 normal days, last day didn't trade (close=0)."""
    rows = [_eod_row(f"2026-04-{d:02d}", 5.40) for d in range(1, 20)] + \
           [_eod_row("2026-04-20", 0, volume=0)]
    snap = asyncio.run(_run_snapshot(rows))
    assert snap["last"] == 5.40, f"expected 5.40, got {snap['last']}"
    assert snap["pct1d"] == 0.0, f"expected 0%, got {snap['pct1d']}"
    print("  pass: no-trade-today falls back to prior day")


def test_illiquid_ticker_uses_last_actual_trade():
    """CHOTI-style: sparse trades, today=0."""
    closes = [0, 0, 0, 0, 0, 64.25, 64.25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 64.25, 65.75, 65.75, 0]
    rows = [_eod_row(f"2026-04-{d:02d}", c, volume=(0 if c == 0 else 100))
            for d, c in enumerate(closes, start=1)]
    snap = asyncio.run(_run_snapshot(rows))
    assert snap["last"] == 65.75, f"expected 65.75, got {snap['last']}"
    assert snap["pct1d"] == 0.0, f"prev real trade was also 65.75, got {snap['pct1d']}"
    print("  pass: illiquid ticker uses last actual trade")


def test_delisted_ticker_returns_none():
    """NWR-style: entire 20-day series is 0 — should report no data."""
    rows = [_eod_row(f"2026-04-{d:02d}", 0, volume=0) for d in range(1, 21)]
    snap = asyncio.run(_run_snapshot(rows))
    assert snap["last"] is None, f"expected None, got {snap['last']}"
    assert snap["pct1d"] is None
    print("  pass: delisted ticker returns None")


def test_normal_ticker_unchanged():
    """TC-style: all days trade normally."""
    closes = [5.5, 5.55, 5.45, 5.5, 5.55, 5.55, 5.5, 5.5, 5.45, 5.45,
              5.45, 5.4, 5.5, 5.55, 5.55, 5.6, 5.7, 5.9, 5.7, 5.7]
    rows = [_eod_row(f"2026-04-{d:02d}", c) for d, c in enumerate(closes, start=1)]
    snap = asyncio.run(_run_snapshot(rows))
    assert snap["last"] == 5.7, f"expected 5.7, got {snap['last']}"
    assert snap["pct1d"] == 0.0  # 5.7 vs 5.7
    print("  pass: normal ticker unchanged")


def test_pct5d_skips_zero_days():
    """pct5d should compare against the 6th-most-recent real close, not include zeros."""
    closes = [10.0] * 5 + [0, 0, 0, 0, 0] + [11.0] * 9 + [12.0]
    rows = [_eod_row(f"2026-04-{d:02d}", c, volume=(0 if c == 0 else 100))
            for d, c in enumerate(closes, start=1)]
    snap = asyncio.run(_run_snapshot(rows))
    assert snap["last"] == 12.0
    # Filtered closes: [10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 11, 11, 12]
    # prev_5d = filtered[-6] = 11.0
    assert snap["pct5d"] == round((12.0 / 11.0 - 1) * 100, 2), f"got {snap['pct5d']}"
    print("  pass: pct5d skips zero days")


if __name__ == "__main__":
    print("Running snapshot tests...")
    test_no_trade_today_falls_back_to_prior_day()
    test_illiquid_ticker_uses_last_actual_trade()
    test_delisted_ticker_returns_none()
    test_normal_ticker_unchanged()
    test_pct5d_skips_zero_days()
    print("All tests passed.")
