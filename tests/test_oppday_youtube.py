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
        base = dict(url="u", period="q2y2026", list=False, only=None, limit=0, force=False, dry_run=False,
                    assign=None)
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


class TestJointAndFiscal(TestRun):
    def test_assign_makes_one_report_per_ticker_with_its_own_focus(self):
        prompts = []
        lister = lambda url: [{"id": "j1", "title": "Opp Day Q2/2026 TU CPN joint"}]
        fetcher = lambda vid: (TRANSCRIPT, {"upload_date": "20260912", "title": "Opp Day Q2/2026 TU CPN joint"})
        chat = lambda system, user, **k: prompts.append(user) or fake_report("รายได้ 1,200 ล้านบาท")
        self.assertEqual(oy.run(self._args(assign=["j1=TU,CPN"]), lister=lister, fetcher=fetcher, chat=chat), 0)
        for tk in ("TU", "CPN"):
            self.assertTrue((self.tmp / oy.REPORTS_DIR / f"{tk}_oppday_q2y2026_summary.md").is_file())
        self.assertIn("นำเสนอร่วมกับ CPN", prompts[0])
        self.assertIn("นำเสนอร่วมกับ TU", prompts[1])

    def test_assign_rejects_non_coverage_ticker(self):
        self.assertEqual(oy.run(self._args(assign=["j1=PTT"]), lister=lambda u: [], chat=lambda *a, **k: ""), 1)

    def test_own_fiscal_period_goes_in_the_date_line(self):
        seen = []
        lister = lambda url: [{"id": "k1", "title": "Opp Day 9M/2026 (TU)"}]
        fetcher = lambda vid: (TRANSCRIPT, {"upload_date": "20260912", "title": "Opp Day 9M/2026 (TU)"})
        chat = lambda system, user, **k: seen.append(system) or fake_report("รายได้ 1,200 ล้านบาท")
        oy.run(self._args(), lister=lister, fetcher=fetcher, chat=chat)
        self.assertIn("**วันที่:** ผลประกอบการ 9M/2569 (12 กันยายน 2569)", seen[0])
        self.assertTrue((self.tmp / oy.REPORTS_DIR / "TU_oppday_q2y2026_summary.md").is_file(),
                        "file stays under the season code so the builder groups the season")


class TestKeyFromRegistry(TestRun):
    def test_missing_key_is_filled_before_the_check(self):
        import cron_shim
        lister = lambda url: [{"id": "v1", "title": "Opp Day Q2/2026 (TU)"}]
        fetcher = lambda vid: ("x", {})
        with mock.patch.dict(os.environ, {"MINIMAX_API_KEY": ""}), \
             mock.patch.object(cron_shim, "_load_user_env",
                               side_effect=lambda: os.environ.__setitem__("MINIMAX_API_KEY", "k")) as load:
            rc = oy.run(self._args(limit=1), lister=lister, fetcher=fetcher)
        load.assert_called_once()
        self.assertEqual(rc, 0, "key found after the registry fill, so the run proceeds")


class TestCaptionDiagnostics(TestRun):
    def _proc(self, rc=0, out="", err=""):
        return mock.Mock(returncode=rc, stdout=out, stderr=err)

    def test_blocked_request_raises_not_empty(self):
        with mock.patch.object(oy, "_ytdlp", return_value=self._proc(1, err="ERROR: Sign in to confirm you're not a bot")):
            with self.assertRaises(oy.CaptionsBlocked) as cm:
                oy.fetch_captions("v1")
        self.assertIn("not a bot", str(cm.exception))

    def test_no_thai_track_is_named(self):
        meta = '{"title": "t", "subtitles": {}, "automatic_captions": {"en": [], "ja": []}}'
        with mock.patch.object(oy, "_ytdlp", return_value=self._proc(0, out=meta)):
            text, m = oy.fetch_captions("v1")
        self.assertEqual(text, "")
        self.assertIn("no Thai track", m["_caption_note"])

    def test_three_blocks_stop_the_batch(self):
        calls = []
        def fetcher(vid):
            calls.append(vid)
            raise oy.CaptionsBlocked("HTTP Error 429")
        lister = lambda url: [{"id": f"v{i}", "title": f"Opp Day Q2/2026 ({tk})"} for i, tk in enumerate(["TU", "CPN", "AAI", "M"])]
        rc = oy.run(self._args(), lister=lister, fetcher=fetcher, chat=lambda *a, **k: "")
        self.assertEqual(rc, 1)
        self.assertEqual(len(calls), 3)


class TestPeriod(unittest.TestCase):
    def test_title_period(self):
        self.assertEqual(oy.title_period("KTIS Opp Day 9M/2026"), "9M/2569")
        self.assertEqual(oy.title_period("GVREIT Q3/2026"), "Q3/2569")
        self.assertEqual(oy.title_period("EPG Q1 2026/2027"), "Q1/2569/2570")
        self.assertEqual(oy.title_period("ผลประกอบการ Q2/2569"), "Q2/2569")
        self.assertIsNone(oy.title_period("Opportunity Day (TU)"))

    def test_be_labels(self):
        self.assertEqual(oy.period_be("q2y2026"), "Q2/2569")
        self.assertEqual(oy.period_be("ye2025"), "ปีเต็ม 2568")
        self.assertEqual(oy.be_date("20260912"), "12 กันยายน 2569")
        self.assertEqual(bom.period_label("q2y2026"), "Q2/2026")


if __name__ == "__main__":
    unittest.main()
