"""End-to-end tests for scripts/build_6m26_panel.py.

Run: python tests/test_6m26_panel.py

Builds a miniature vault from the real CPN and ITC filing excerpts plus two
synthetic edge cases, then asserts the emitted CSVs, QA and provenance.
"""
from __future__ import annotations

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import build_6m26_panel as B  # noqa: E402

FIX = REPO / "tests" / "fixtures"

HEADER = "Profit & Loss Statement (Baht mn) 2Q25 1Q26 2Q26 YoY (%) QoQ (%) 6M25 6M26 YoY (%)"

# A loss-maker: no reconcilable YoY on NPAT, rescued by column geometry.
LOSSCO = "\n".join([
    HEADER,
    "Total Revenue 500 600 700 5% 1% 1,000 1,200 20%",
    "Other Income 10 10 10 0% 0% 20 24 20%",
    "Profit to Parent Company (100) (120) (90) 5% 1% (800) (450) n.m.",
])

# No half-year table at all — must be excluded, never guessed.
QUARTERONLY = "The Company reported 2Q26 revenue of Bt900mn, up 4% YoY."

FY_ROWS = [
    # ticker, sector, segment, fy2025_rfo_mb
    ("CPN", "PROP", "P3", 50000.0),
    ("ITC", "FOOD", "F3", 19000.0),
    ("AWC", "PROP", "P4", 25000.0),
    ("LOSSCO", "PROP", "P5", 2400.0),
    ("QUARTERONLY", "FOOD", "F9", 1800.0),
    ("NOFILE", "FOOD", "F9", 900.0),
]


class PanelBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        root = Path(cls._tmp.name)
        cls.vault = root / "vault"
        cls.out = root / "out"

        bodies = {
            "CPN": (FIX / "mda_CPN_2026Q2_pl_excerpt.md").read_text(encoding="utf-8"),
            "ITC": (FIX / "mda_ITC_2026Q2_pl_excerpt.md").read_text(encoding="utf-8"),
            "AWC": (FIX / "mda_AWC_2026Q2_pl_excerpt.md").read_text(encoding="utf-8"),
            "LOSSCO": LOSSCO,
            "QUARTERONLY": QUARTERONLY,
        }
        for ticker, body in bodies.items():
            folder = cls.vault / B.MDA_SUBPATH / ticker
            folder.mkdir(parents=True, exist_ok=True)
            (folder / f"MDA_{ticker}_2026Q2_E.md").write_text(body, encoding="utf-8")

        cls.fy_csv = root / "fy_company.csv"
        with cls.fy_csv.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["ticker", "sector", "primary_segment_code", "fy2025_rfo_mb"])
            writer.writerows(FY_ROWS)

        cls.summary = B.build(cls.vault, cls.fy_csv, cls.out, "2026-08-17")
        cls.companies = {
            row["ticker"]: row
            for row in csv.DictReader(
                (cls.out / "food_prop_company_6m25_6m26_2026-08-17.csv")
                .open(encoding="utf-8-sig"))
        }
        cls.segments = {
            row["primary_segment_code"]: row
            for row in csv.DictReader(
                (cls.out / "food_prop_segment_6m25_6m26_2026-08-17.csv")
                .open(encoding="utf-8-sig"))
        }

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    # ------------------------------------------------------------- perimeter

    def test_every_universe_company_appears(self):
        self.assertEqual(len(self.companies), len(FY_ROWS))
        self.assertEqual(self.summary["universe"], len(FY_ROWS))

    def test_qa_passes(self):
        self.assertEqual(self.summary["qa"], "PASS")
        self.assertEqual(self.summary["qa_counts"]["fail"], 0)

    # ------------------------------------------------------- included values

    def test_cpn_rfo_is_the_derived_01_sale_basis(self):
        row = self.companies["CPN"]
        self.assertEqual(row["rfo_panel_included"], "yes")
        self.assertAlmostEqual(float(row["rfo_6m26_mb"]), 25224.0)
        self.assertAlmostEqual(float(row["npat_owners_6m26_mb"]), 9721.0)
        self.assertEqual(row["npat_state"], "profit_increased")
        self.assertIn("26,457 - 1,233 = 25,224", row["rfo_derivation"])

    def test_every_published_figure_carries_its_evidence(self):
        row = self.companies["CPN"]
        self.assertIn("Total Revenue", row["rfo_evidence"])
        self.assertIn("Profit to Parent Company", row["npat_evidence"])
        self.assertEqual(len(row["source_sha256"]), 64)
        self.assertTrue(row["source_path"].endswith("MDA_CPN_2026Q2_E.md"))

    def test_loss_maker_enters_the_panel_with_a_state_not_a_yoy(self):
        row = self.companies["LOSSCO"]
        self.assertEqual(row["npat_panel_included"], "yes")
        self.assertAlmostEqual(float(row["npat_owners_6m26_mb"]), -450.0)
        self.assertEqual(row["npat_state"], "loss_narrowed")
        self.assertEqual(row["npat_yoy_pct_positive_base_only"], "")

    # ------------------------------------------------------------ exclusions

    def test_itc_is_out_of_the_npat_panel_but_keeps_its_revenue(self):
        row = self.companies["ITC"]
        self.assertEqual(row["rfo_panel_included"], "yes")
        self.assertAlmostEqual(float(row["rfo_6m26_mb"]), 9704.0)
        self.assertEqual(row["npat_panel_included"], "no")
        self.assertEqual(row["margin_panel_included"], "no")
        self.assertAlmostEqual(float(row["npat_unattributed_6m26_mb"]), 1715.0)
        self.assertTrue(row["panel_exclusion_reason"])

    def test_awc_detached_labels_publish_nothing(self):
        """Real figures exist in the filing but cannot be safely attributed."""
        row = self.companies["AWC"]
        self.assertEqual(row["rfo_panel_included"], "no")
        self.assertEqual(row["npat_panel_included"], "no")
        self.assertEqual(row["rfo_6m26_mb"], "")
        self.assertEqual(row["npat_owners_6m26_mb"], "")
        self.assertTrue(row["panel_exclusion_reason"])

    def test_quarter_only_filing_is_excluded_not_zero_filled(self):
        row = self.companies["QUARTERONLY"]
        self.assertEqual(row["rfo_panel_included"], "no")
        self.assertEqual(row["rfo_6m26_mb"], "")
        self.assertIn("rfo:", row["panel_exclusion_reason"])

    def test_missing_filing_is_reported_as_missing(self):
        row = self.companies["NOFILE"]
        self.assertEqual(row["rfo_panel_included"], "no")
        self.assertIn("no 2026Q2 MD&A", row["panel_exclusion_reason"])

    # ---------------------------------------------------------- aggregation

    def test_segment_totals_equal_member_sums(self):
        self.assertAlmostEqual(float(self.segments["P3"]["rfo_6m26_mb"]), 25224.0)
        self.assertAlmostEqual(float(self.segments["F3"]["rfo_6m26_mb"]), 9704.0)

    def test_segment_margin_uses_only_the_intersection(self):
        """F3 has revenue but no owner NPAT, so no margin may be reported."""
        self.assertEqual(self.segments["F3"]["margin_panel_company_count"], "0")
        self.assertEqual(self.segments["F3"]["net_margin_6m26_pct_comparable"], "")

    def test_excluded_tickers_are_named_in_the_segment_row(self):
        self.assertEqual(self.segments["F3"]["npat_panel_excluded_tickers"], "ITC")
        self.assertEqual(self.segments["F9"]["rfo_panel_company_count"], "0")

    # --------------------------------------------------------------- report

    def test_report_states_panel_counts_and_qa(self):
        text = (self.out / "COVERAGE_REPORT_6M25_6M26_2026-08-17.md").read_text(encoding="utf-8")
        self.assertIn("| Universe | 6 | 100.0% |", text)
        self.assertIn("QA verdict **PASS**", text)

    def test_report_causes_are_specific_not_generic(self):
        """ITC's table exists and reconciles; saying otherwise would misdirect."""
        text = (self.out / "COVERAGE_REPORT_6M25_6M26_2026-08-17.md").read_text(encoding="utf-8")
        self.assertIn("no owner-attributed profit line", text)
        self.assertIn("only a combined total revenue", text)

    def test_report_surfaces_promotion_candidates_with_values(self):
        text = (self.out / "COVERAGE_REPORT_6M25_6M26_2026-08-17.md").read_text(encoding="utf-8")
        self.assertIn("Candidates for analyst promotion", text)
        self.assertIn("| ITC | F3 | 1,715 |", text)

    def test_report_has_segment_coverage(self):
        text = (self.out / "COVERAGE_REPORT_6M25_6M26_2026-08-17.md").read_text(encoding="utf-8")
        self.assertIn("## Segment coverage", text)
        self.assertIn("| F3 | 1 | 1 | 0 |", text)

    # ----------------------------------------------------------- provenance

    def test_provenance_hashes_every_source_and_output(self):
        provenance = json.loads(
            (self.out / "PROVENANCE_6M25_6M26_2026-08-17.json").read_text(encoding="utf-8"))
        self.assertEqual(provenance["qa_verdict"], "PASS")
        self.assertEqual(provenance["period"], "6M26 vs 6M25")
        by_ticker = {item["ticker"]: item for item in provenance["sources"]}
        self.assertEqual(len(by_ticker["CPN"]["sha256"]), 64)
        self.assertNotIn("NOFILE", by_ticker)
        for name, digest in provenance["outputs"].items():
            self.assertEqual(len(digest), 64, name)


class PlausibilityBand(unittest.TestCase):
    def test_half_year_larger_than_the_full_year_is_rejected(self):
        row = B.CompanyRow(ticker="X", sector="FOOD", segment="F1", fy2025_rfo_mb=1000.0)
        row.extract = B.extract_company("X", "\n".join([
            HEADER,
            "Total Revenue 1 2 3 5% 1% 1,000 1,100 10%",
            "Other Income 1 1 1 0% 0% 10 11 10%",
        ]))
        B.apply_fy_share_check(row)
        self.assertIn("plausibility band", row.blocking_exclusion)
        self.assertFalse(row.in_rfo_panel)

    def test_a_normal_half_year_passes(self):
        row = B.CompanyRow(ticker="X", sector="FOOD", segment="F1", fy2025_rfo_mb=2000.0)
        row.extract = B.extract_company("X", "\n".join([
            HEADER,
            "Total Revenue 1 2 3 5% 1% 900 1,000 11%",
            "Other Income 1 1 1 0% 0% 9 10 11%",
        ]))
        B.apply_fy_share_check(row)
        self.assertEqual(row.blocking_exclusion, "")
        self.assertTrue(row.in_rfo_panel)


class NpatStates(unittest.TestCase):
    def test_states_match_the_fy_panel_vocabulary(self):
        self.assertEqual(B.npat_state(100, 120), "profit_increased")
        self.assertEqual(B.npat_state(120, 100), "profit_decreased")
        self.assertEqual(B.npat_state(100, -50), "turned_to_loss")
        self.assertEqual(B.npat_state(-100, 50), "turned_to_profit")
        self.assertEqual(B.npat_state(-100, -40), "loss_narrowed")
        self.assertEqual(B.npat_state(-40, -100), "loss_widened")

    def test_yoy_is_never_computed_on_a_negative_base(self):
        self.assertIsNone(B.yoy_pct(-100, -40))
        self.assertIsNone(B.yoy_pct(0, 50))
        self.assertAlmostEqual(B.yoy_pct(100, 125), 25.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
