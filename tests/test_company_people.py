"""Offline tests for scripts/build_company_people.py.

Fixtures are cut from the real SET API responses the CI probe returned on
29 Sep 2026 (AWC board EN/TH, AWC and FTREIT shareholder lists).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from build_company_people import (  # noqa: E402
    diff_board, merge_ticker, parse_board, parse_shareholders,
)

BOARD_EN = [
    {"name": "Mr. BOONTUCK WUNGCHAROEN", "positions": ["CHAIRMAN OF THE BOARD OF DIRECTORS"]},
    {"name": "Mrs. WALLAPA TRAISORAT", "positions": ["CHIEF EXECUTIVE OFFICER AND PRESIDENT", "DIRECTOR"]},
    {"name": "Mrs. NUNTAWAN SAKUNTANAGA", "positions": ["INDEPENDENT DIRECTOR", "CHAIRMAN OF AUDIT COMMITTEE"]},
    {"name": "Mr. KALIN SARASIN", "positions": ["INDEPENDENT DIRECTOR"]},
]
BOARD_TH = [
    {"name": "นาย บุญทักษ์ หวังเจริญ", "positions": ["ประธานกรรมการ"]},
    {"name": "นาง วัลลภา ไตรโสรัส", "positions": ["ประธานเจ้าหน้าที่บริหารและกรรมการผู้จัดการใหญ่", "กรรมการ"]},
    {"name": "นาง นันทวัลย์ ศกุนตนาค", "positions": ["กรรมการอิสระ", "ประธานกรรมการตรวจสอบ"]},
    {"name": "นาย กลินท์ สารสิน", "positions": ["กรรมการอิสระ"]},
]
HOLDERS = {
    "symbol": "AWC", "bookCloseDate": "2026-05-08T00:00:00+07:00", "caType": "XD",
    "totalShareholder": 26937, "percentScriptless": 54.21,
    "majorShareholders": [
        {"sequence": 1, "name": "บริษัท  ทีซีซี บริหารธุรกิจ จำกัด", "nationality": None,
         "numberOfShare": 14400000000, "percentOfShare": 44.96, "isThaiNVDR": False},
        {"sequence": 2, "name": "TCC RETAIL CO.,LTD", "nationality": None,
         "numberOfShare": 9600000000, "percentOfShare": 29.98, "isThaiNVDR": False},
        {"sequence": 7, "name": "Thai NVDR Company Limited", "nationality": None,
         "numberOfShare": 445341751, "percentOfShare": 1.39, "isThaiNVDR": True},
    ],
    "freeFloat": {"bookCloseDate": "2026-03-10T00:00:00+07:00", "caType": "XM",
                  "percentFreeFloat": 24.95, "numberOfHolder": 26930},
}
TODAY = "2026-09-29"


class ParseBoard(unittest.TestCase):
    def test_merges_thai_names_and_flags_roles(self):
        b = parse_board(BOARD_EN, BOARD_TH)
        self.assertEqual(len(b), 4)
        self.assertEqual(b[0]["nameTh"], "นาย บุญทักษ์ หวังเจริญ")
        self.assertTrue(b[0]["chair"])
        self.assertFalse(b[0]["independent"])
        self.assertTrue(b[2]["independent"] and b[2]["audit"])
        self.assertFalse(b[1]["independent"])
        self.assertEqual(sum(d["independent"] for d in b), 2)

    def test_mismatched_lengths_never_pair_thai_names(self):
        b = parse_board(BOARD_EN, BOARD_TH[:3])
        self.assertTrue(all(d["nameTh"] is None for d in b))

    def test_empty_or_missing(self):
        self.assertEqual(parse_board([], []), [])
        self.assertEqual(parse_board(None, None), [])


class ParseShareholders(unittest.TestCase):
    def test_fields(self):
        s = parse_shareholders(HOLDERS)
        self.assertEqual(s["recordDate"], "2026-05-08")
        self.assertEqual(s["caType"], "XD")
        self.assertEqual(s["totalShareholder"], 26937)
        self.assertEqual(s["major"][0]["name"], "บริษัท ทีซีซี บริหารธุรกิจ จำกัด")  # double space collapsed
        self.assertEqual(s["major"][0]["pct"], 44.96)
        self.assertTrue(s["major"][2]["nvdr"])
        self.assertEqual(s["freeFloat"]["percent"], 24.95)

    def test_empty(self):
        self.assertIsNone(parse_shareholders({"majorShareholders": []}))
        self.assertIsNone(parse_shareholders(None))


class Merge(unittest.TestCase):
    def setUp(self):
        self.board = parse_board(BOARD_EN, BOARD_TH)
        self.holders = parse_shareholders(HOLDERS)
        self.first = merge_ticker(None, self.board, self.holders, "PROP", "2026-09-01")

    def test_first_run_records_no_changes(self):
        self.assertEqual(self.first["boardChanges"], [])
        self.assertIsNone(self.first["boardSince"])
        self.assertEqual(self.first["shareholderHistory"], [])
        self.assertEqual(self.first["checked"], "2026-09-01")

    def test_board_change_is_dated(self):
        new = [d for d in self.board if "KALIN" not in d["name"]] + [
            {**self.board[3], "name": "Mr. NEW DIRECTOR", "nameTh": None}]
        new[1] = {**new[1], "positions": ["DIRECTOR"]}
        rec = merge_ticker(self.first, new, self.holders, "PROP", TODAY)
        ch = rec["boardChanges"][0]
        self.assertEqual(ch["date"], TODAY)
        self.assertEqual(ch["joined"], ["Mr. NEW DIRECTOR"])
        self.assertEqual(ch["left"], ["Mr. KALIN SARASIN"])
        self.assertEqual(ch["changed"][0]["name"], "Mrs. WALLAPA TRAISORAT")
        self.assertEqual(rec["boardSince"], TODAY)

    def test_same_board_different_spacing_is_not_a_change(self):
        again = [{**d, "name": d["name"].upper().replace(" ", "  ")} for d in self.board]
        self.assertIsNone(diff_board(self.board, again))
        rec = merge_ticker(self.first, again, self.holders, "PROP", TODAY)
        self.assertEqual(rec["boardChanges"], [])

    def test_new_record_date_moves_old_list_to_history(self):
        newer = {**self.holders, "recordDate": "2026-09-18", "caType": "XD"}
        rec = merge_ticker(self.first, self.board, newer, "PROP", TODAY)
        self.assertEqual(rec["shareholders"]["recordDate"], "2026-09-18")
        self.assertEqual(rec["shareholderHistory"][0]["recordDate"], "2026-05-08")
        self.assertEqual(rec["shareholderHistory"][0]["top"][0]["pct"], 44.96)
        # Same record date again: no duplicate snapshot.
        rec2 = merge_ticker(rec, self.board, newer, "PROP", "2026-09-30")
        self.assertEqual(len(rec2["shareholderHistory"]), 1)

    def test_failed_fetch_keeps_previous(self):
        rec = merge_ticker(self.first, None, None, "PROP", TODAY)
        self.assertEqual(rec["board"], self.first["board"])
        self.assertEqual(rec["shareholders"], self.first["shareholders"])
        self.assertEqual(rec["checked"], "2026-09-01")

    def test_reit_has_no_board(self):
        rec = merge_ticker(None, [], self.holders, "PF&REIT", TODAY)
        self.assertFalse(rec["boardApplicable"])
        self.assertEqual(rec["board"], [])

    def test_empty_board_for_a_company_keeps_previous(self):
        # An empty list for a non-trust is treated as a bad response, not a
        # board that resigned en masse.
        rec = merge_ticker(self.first, [], self.holders, "PROP", TODAY)
        self.assertEqual(rec["board"], self.first["board"])
        self.assertEqual(rec["boardChanges"], [])


if __name__ == "__main__":
    unittest.main()
