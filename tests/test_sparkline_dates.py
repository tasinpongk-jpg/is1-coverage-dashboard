"""Sparkline closes carry their session dates, aligned one to one.

company-summary.html pins SET filings to the price line by date, so a date
list that drifts from the closes (e.g. a no-trade day with close=0 kept in one
list and dropped from the other) would put a filing on the wrong session.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from build_ticker_summary import process_eod  # noqa: E402


def _rows(n: int) -> list[dict]:
    rows = []
    for i in range(n):
        day = f"2026-08-{i + 1:02d}"
        # Every fifth day is a no-trade day: SETSMART returns close=0.
        close = 0 if i % 5 == 4 else 10 + i
        rows.append({"date": day, "close": close, "totalVolume": 100 if close else 0})
    return rows


class TestSparklineDates(unittest.TestCase):
    def test_dates_align_with_closes(self):
        out = process_eod(list(reversed(_rows(30))))
        self.assertEqual(len(out["sparkline"]), 20)
        self.assertEqual(len(out["sparklineDates"]), 20)
        by_date = {r["date"]: r["close"] for r in _rows(30)}
        for close, day in zip(out["sparkline"], out["sparklineDates"]):
            self.assertEqual(by_date[day], close)
        self.assertEqual(out["sparklineDates"], sorted(out["sparklineDates"]))

    def test_no_trade_days_are_skipped(self):
        out = process_eod(_rows(30))
        self.assertNotIn("2026-08-05", out["sparklineDates"])


if __name__ == "__main__":
    unittest.main()
