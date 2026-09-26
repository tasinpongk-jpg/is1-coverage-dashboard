"""months_for: a year-to-date highlight row must never read as a full year."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from build_ticker_summary import months_for  # noqa: E402


class TestMonthsFor(unittest.TestCase):
    def test_legacy_quarter_codes(self):
        self.assertEqual([months_for(q) for q in ("Q1", "Q2", "Q3", "Q4", "Q9")], [3, 6, 9, 12, 12])

    def test_new_month_codes(self):
        self.assertEqual([months_for(q) for q in ("3M", "6M", "9M", "12M")], [3, 6, 9, 12])

    def test_unknown_or_blank_is_full_year(self):
        for q in ("", None, "FY", "99M"):
            self.assertEqual(months_for(q), 12)

    def test_snapshot_months_match_quarter(self):
        data = json.loads((REPO / "data" / "ticker-summary.json").read_text(encoding="utf-8"))
        for t in data["tickers"]:
            for h in t.get("highlights") or []:
                self.assertEqual(h.get("months"), months_for(h.get("quarter") or ""), f"{t['tk']} {h.get('year')}")


if __name__ == "__main__":
    unittest.main()
