"""oppday_youtube: coverage matching, caption parsing, number-check hold, file layout."""
from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import oppday_youtube as oy  # noqa: E402
import build_oppday_minutes as bom  # noqa: E402

COV = {"TU", "CPN", "M", "J", "AAI", "F&D"}


class TestMatch(unittest.TestCase):
    def test_coverage_ticker_found(self):
        self.assertEqual(oy.match_title("Opportunity Day Q2/2026 บริษัท ไทยยูเนี่ยน กรุ๊ป (TU)", COV), ("TU", "ok"))

    def test_not_ours(self):
        self.assertEqual(oy.match_title("Opportunity Day Q2/2026 PTT", COV)[0], None)

    def test_period_and_set_words_ignored(self):
        self.assertEqual(oy.match_title("SET Opp Day Q2 2026 | AAI", COV), ("AAI", "ok"))

    def test_single_letter_needs_brackets(self):
        self.assertEqual(oy.match_title("Opp Day Q2/2026 M Chai (M)", COV)[0], "M")
        self.assertIsNone(oy.match_title("Opp Day Q2/2026 A M B Company", COV)[0])

    def test_ampersand_ticker(self):
        self.assertEqual(oy.match_title("Opp Day Q2/2026 F&D", COV)[0], "F&D")

    def test_two_tickers_is_ambiguous(self):
        tk, why = oy.match_title("Opp Day TU and CPN joint session", COV)
        self.assertIsNone(tk)
        self.assertTrue(why.startswith("ambiguous"))


class TestVtt(unittest.TestCase):
    def test_rolling_duplicates_and_tags_removed(self):
        vtt = ("WEBVTT\nKind: captions\nLanguage: th\n\n00:00:01.000 --> 00:00:03.000\n"
               "สวัสดีครับ<00:00:02.000><c> ท่านนักลงทุน</c>\n\n00:00:03.000 --> 00:00:05.000\n"
               "สวัสดีครับ ท่านนักลงทุน\n\n00:00:05.000 --> 00:00:07.000\nรายได้ 1,200 ล้านบาท\n")
        self.assertEqual(oy.parse_vtt(vtt), "สวัสดีครับ ท่านนักลงทุน\nรายได้ 1,200 ล้านบาท")


def fake_report(numbers: str) -> str:
    return ("# รายงานสรุป Opportunity Day — TU\n**วันที่:** ผลประกอบการ Q2/2569 (12 กันยายน 2569)\n\n---\n\n"
            f"## 1. ภาพรวมธุรกิจ\n\nTU ผลิตอาหารทะเล {numbers}\n\n## 2. ผลการดำเนินงาน\n\n## 6. ประเด็นสำคัญสำหรับ RM\n\nติดตาม\n")


TRANSCRIPT = "สวัสดีครับ " * 80 + "รายได้ไตรมาสนี้ 1,200 ล้านบาท กำไร 350 ล้านบาท เติบโต 12.5 เปอร์เซ็นต์"


class TestRun(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / oy.LISTED).mkdir(parents=True)
        self.env = mock.patch.dict(os.environ, {"VAULT_ROOT": str(self.tmp)})
        self.env.start()
        self.cov = mock.patch.object(oy, "load_coverage", return_value=COV)
        self.cov.start()

    def tearDown(self):
        self.env.stop()
        self.cov.stop()

    def _args(self, **kw):
        base = dict(url="u", period="q2y2026", list=False, only=None, limit=0, force=False, dry_run=False)
        base.update(kw)
        return argparse.Namespace(**base)

    def _run(self, report_numbers, **kw):
        lister = lambda url: [{"id": "v1", "title": "Opp Day Q2/2026 (TU)"},
                              {"id": "v2", "title": "Opp Day Q2/2026 PTT"}]
        fetcher = lambda vid: (TRANSCRIPT, {"upload_date": "20260912", "title": "Opp Day Q2/2026 (TU)"})
        chat = lambda system, user, **k: fake_report(report_numbers)
        return oy.run(self._args(**kw), lister=lister, fetcher=fetcher, chat=chat)

    def test_traced_report_is_published_where_the_builder_reads(self):
        self.assertEqual(self._run("รายได้ 1,200 ล้านบาท กำไร 350 ล้านบาท"), 0)
        report = self.tmp / oy.REPORTS_DIR / "TU_oppday_q2y2026_summary.md"
        self.assertTrue(report.is_file())
        self.assertTrue(bom.FILENAME_RE.match(report.name))
        self.assertNotIn("หมายเหตุการตรวจสอบตัวเลข", report.read_text(encoding="utf-8"))
        transcript = self.tmp / oy.TRANSCRIPT_DIR / "TU" / "TU_oppday_q2y2026_transcript.md"
        self.assertIn("video_id: v1", transcript.read_text(encoding="utf-8"))

    def test_invented_numbers_are_held_for_review(self):
        self.assertEqual(self._run("รายได้ 9,999 ล้านบาท กำไร 777 ล้านบาท"), 0)
        held = self.tmp / oy.REPORTS_DIR / "TU_oppday_q2y2026_summary.review.md"
        self.assertTrue(held.is_file())
        self.assertIsNone(bom.FILENAME_RE.match(held.name), "builder must ignore held reports")
        self.assertFalse((self.tmp / oy.REPORTS_DIR / "TU_oppday_q2y2026_summary.md").exists())
        self.assertIn("9,999", held.read_text(encoding="utf-8"))

    def test_existing_report_is_skipped_unless_forced(self):
        self._run("รายได้ 1,200 ล้านบาท")
        with mock.patch.object(oy, "summarise", side_effect=AssertionError("should not run")):
            self.assertEqual(self._run("x"), 0)

    def test_list_and_dry_run_write_nothing(self):
        self.assertEqual(self._run("1,200", list=True), 0)
        self.assertEqual(self._run("1,200", dry_run=True), 0)
        self.assertFalse((self.tmp / oy.REPORTS_DIR).exists())


class TestPeriod(unittest.TestCase):
    def test_be_labels(self):
        self.assertEqual(oy.period_be("q2y2026"), "Q2/2569")
        self.assertEqual(oy.period_be("ye2025"), "ปีเต็ม 2568")
        self.assertEqual(oy.be_date("20260912"), "12 กันยายน 2569")
        self.assertEqual(bom.period_label("q2y2026"), "Q2/2026")


if __name__ == "__main__":
    unittest.main()
