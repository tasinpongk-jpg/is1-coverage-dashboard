"""normalize_period: every vault period must compare lexicographically."""
from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

from build_vault_ticker_notes import normalize_period  # noqa: E402


class TestNormalizePeriod(unittest.TestCase):
    def test_canonical_passes_through(self):
        for p in ("2026Q1", "2025FY", "2026q2"):
            self.assertEqual(normalize_period(p), p.upper())

    def test_be_and_ad_quarter_labels(self):
        cases = {
            "Q1/2569": "2026Q1",
            "Q1/2569 (ม.ค.–มี.ค. 2569)": "2026Q1",
            "Q1/69 (มกราคม–มีนาคม 2569)": "2026Q1",
            "Q1/2026 (ไตรมาส 1 สิ้นสุด 31 มีนาคม 2569)": "2026Q1",
            "Q1/69 (1Q26) — ไตรมาส 1 สิ้นสุด 31 มีนาคม 2569": "2026Q1",
            "Q1/69 = Q2/FY2026 (3-month ended 31 March 2026)": "2026Q1",
            "Q1/2026 (1H69 — ไตรมาส 1 สิ้นสุด 31 มีนาคม 2569)": "2026Q1",
            "Q3/68": "2025Q3",
            "1Q26": "2026Q1",
            "FY2568": "2025FY",
            "FY68": "2025FY",
        }
        for raw, want in cases.items():
            self.assertEqual(normalize_period(raw), want, raw)

    def test_unreadable_falls_back_to_filename(self):
        self.assertEqual(normalize_period("", Path("PRG_2026Q2_T.md")), "2026Q2")
        self.assertEqual(normalize_period("latest", Path("notes.md")), "")

    def test_every_period_in_current_snapshot_normalizes(self):
        snap = REPO / "data" / "vault-ticker-notes.json"
        if not snap.exists():
            self.skipTest("snapshot not present")
        tickers = json.loads(snap.read_text(encoding="utf-8"))["tickers"]
        bad = set()
        for buckets in tickers.values():
            for items in buckets.values():
                for item in items:
                    raw = item.get("periodLabel") or item.get("period") or ""
                    if not raw:
                        continue
                    out = normalize_period(raw)
                    if out and not re.fullmatch(r"20\d{2}(Q[1-4]|FY)", out):
                        bad.add(raw)
        self.assertFalse(bad, sorted(bad)[:10])


if __name__ == "__main__":
    unittest.main()
