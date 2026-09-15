"""Offline tests for scripts/build_sec_governance.py derive().

No network. Exercises the flag logic, the null handling, and the two
comparisons (auditor code vs name) that decide auditor_change.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from build_sec_governance import derive, num  # noqa: E402

META = {"sector": "PROP", "rm": "C", "bucket": "PROP"}


def call(auditor=None, dirperf=None, board=None, prior=None, year="2024"):
    return derive("TEST", META,
                  [auditor] if auditor else [],
                  [dirperf] if dirperf else [],
                  [board] if board else [],
                  [prior] if prior else (None if prior is None else []),
                  year)


class TestNum(unittest.TestCase):
    def test_blank_is_none_not_zero(self):
        # A missing fee must never be read as a fee of zero — that would make
        # a non-filer look like a company with no non-audit work.
        self.assertIsNone(num(""))
        self.assertIsNone(num(None))
        self.assertIsNone(num("n/a"))
        self.assertEqual(num("1,250,000"), 1250000.0)
        self.assertEqual(num(0), 0.0)


class TestNonAuditRatio(unittest.TestCase):
    def test_ratio_and_flag(self):
        r = call(auditor={"audit_fee": "1000000", "non_audit_fee": "2500000"})
        self.assertEqual(r["non_audit_ratio"], 2.5)
        self.assertTrue(r["flags"]["high_non_audit"])

    def test_ratio_at_parity_is_not_flagged(self):
        r = call(auditor={"audit_fee": "1000000", "non_audit_fee": "1000000"})
        self.assertEqual(r["non_audit_ratio"], 1.0)
        self.assertFalse(r["flags"]["high_non_audit"])

    def test_zero_non_audit_is_assessed_not_skipped(self):
        r = call(auditor={"audit_fee": "1000000", "non_audit_fee": "0"})
        self.assertEqual(r["non_audit_ratio"], 0.0)
        self.assertFalse(r["flags"]["high_non_audit"])

    def test_missing_audit_fee_leaves_flag_unassessed(self):
        r = call(auditor={"audit_fee": "", "non_audit_fee": "500000"})
        self.assertIsNone(r["non_audit_ratio"])
        self.assertIsNone(r["flags"]["high_non_audit"])

    def test_zero_audit_fee_does_not_divide(self):
        r = call(auditor={"audit_fee": "0", "non_audit_fee": "500000"})
        self.assertIsNone(r["non_audit_ratio"])
        self.assertIsNone(r["flags"]["high_non_audit"])


class TestAuditorChange(unittest.TestCase):
    def test_code_change_detected(self):
        r = call(auditor={"auditor_company_code": "A1", "auditor_company_name_th": "เอ"},
                 prior={"auditor_company_code": "B2", "auditor_company_name_th": "บี"})
        self.assertTrue(r["flags"]["auditor_change"])

    def test_same_code_renamed_firm_is_not_a_change(self):
        # A firm rebrand must not read as an engagement change.
        r = call(auditor={"auditor_company_code": "A1", "auditor_company_name_th": "ชื่อใหม่"},
                 prior={"auditor_company_code": "A1", "auditor_company_name_th": "ชื่อเดิม"})
        self.assertFalse(r["flags"]["auditor_change"])

    def test_name_fallback_when_no_code(self):
        r = call(auditor={"auditor_company_name_th": "เอ"},
                 prior={"auditor_company_name_th": "บี"})
        self.assertTrue(r["flags"]["auditor_change"])

    def test_no_change_is_false_not_none(self):
        # Regression: "did not change" is a real assessment, not a missing one.
        r = call(auditor={"auditor_company_name_th": "เอ"},
                 prior={"auditor_company_name_th": "เอ"})
        self.assertIs(r["flags"]["auditor_change"], False)
        self.assertEqual(r["flag_count"], 0)

    def test_no_prior_year_leaves_it_unassessed(self):
        r = call(auditor={"auditor_company_name_th": "เอ"}, prior=None)
        self.assertIsNone(r["flags"]["auditor_change"])


class TestBoardIndependence(unittest.TestCase):
    def test_below_one_third_flagged(self):
        r = call(board={"total": "12", "total_independent": "3", "total_female": "2"})
        self.assertEqual(r["board_independent_pct"], 25.0)
        self.assertTrue(r["flags"]["low_independence"])

    def test_exactly_one_third_is_compliant(self):
        r = call(board={"total": "9", "total_independent": "3"})
        self.assertAlmostEqual(r["board_independent_pct"], 33.3, places=1)
        self.assertFalse(r["flags"]["low_independence"])

    def test_missing_board_leaves_it_unassessed(self):
        r = call(board={"total": "", "total_independent": ""})
        self.assertIsNone(r["board_independent_pct"])
        self.assertIsNone(r["flags"]["low_independence"])


class TestAgm(unittest.TestCase):
    def test_on_time_agm(self):
        r = call(dirperf={"agm_meeting_date": "2025-04-25"}, year="2024")
        self.assertEqual(r["agm_date"], "2025-04-25")
        self.assertFalse(r["flags"]["late_agm"])

    def test_late_agm(self):
        r = call(dirperf={"agm_meeting_date": "2025-06-10"}, year="2024")
        self.assertTrue(r["flags"]["late_agm"])

    def test_deadline_day_itself_is_on_time(self):
        r = call(dirperf={"agm_meeting_date": "2025-04-30"}, year="2024")
        self.assertFalse(r["flags"]["late_agm"])

    def test_iso_datetime_form_parses(self):
        r = call(dirperf={"agm_meeting_date": "2025-04-22T00:00:00Z"}, year="2024")
        self.assertEqual(r["agm_date"], "2025-04-22")

    def test_unparsed_date_is_reported_not_guessed(self):
        r = call(dirperf={"agm_meeting_date": "เมษายน 2568"}, year="2024")
        self.assertIsNone(r["agm_date"])
        self.assertIsNone(r["flags"]["late_agm"])
        self.assertIn("unparsed", r["agm_basis"])


class TestAuditCommittee(unittest.TestCase):
    def test_thin_flagged(self):
        r = call(dirperf={"total_audit_meeting": "2"})
        self.assertTrue(r["flags"]["thin_audit_cmte"])

    def test_four_is_enough(self):
        r = call(dirperf={"total_audit_meeting": "4"})
        self.assertFalse(r["flags"]["thin_audit_cmte"])

    def test_missing_unassessed(self):
        r = call(dirperf={})
        self.assertIsNone(r["flags"]["thin_audit_cmte"])


class TestFlagCount(unittest.TestCase):
    def test_counts_only_true(self):
        r = call(auditor={"audit_fee": "100", "non_audit_fee": "500",
                          "auditor_company_code": "A1"},
                 prior={"auditor_company_code": "B2"},
                 board={"total": "10", "total_independent": "2"},
                 dirperf={"agm_meeting_date": "2025-07-01", "total_audit_meeting": "1"},
                 year="2024")
        self.assertEqual(r["flag_count"], 5)

    def test_empty_record_counts_zero(self):
        r = call()
        self.assertEqual(r["flag_count"], 0)
        self.assertTrue(all(v is None for v in r["flags"].values()))


if __name__ == "__main__":
    unittest.main()
