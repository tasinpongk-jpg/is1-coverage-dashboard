"""Ticker matching for wire news and the noFiling flag on external-news.json.

Run from repo root:
    python -m unittest tests/test_external_matching.py
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "surveillance"))
sys.path.insert(0, str(ROOT / "scripts"))

import external_sources as es  # noqa: E402
import build_external as be  # noqa: E402

BKK = timezone(timedelta(hours=7))


class TestThaiAliases(unittest.TestCase):
    def test_core_strips_registered_wrapper(self):
        self.assertEqual(
            es._thai_core("บริษัท เสนาดีเวลลอปเม้นท์ จำกัด (มหาชน)"), "เสนาดีเวลลอปเม้นท์"
        )
        self.assertEqual(
            es._thai_core("บริษัท ไทยยูเนี่ยน กรุ๊ป จำกัด (มหาชน)"), "ไทยยูเนี่ยนกรุ๊ป"
        )

    def _load(self, rows):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ticker-summary.json"
            p.write_text(json.dumps({"tickers": rows}, ensure_ascii=False), encoding="utf-8")
            return es.load_thai_aliases(p)

    def test_short_shared_and_out_of_coverage_names_are_dropped(self):
        got = self._load([
            {"tk": "SENA", "nameTh": "บริษัท เสนาดีเวลลอปเม้นท์ จำกัด (มหาชน)"},
            {"tk": "WIIK", "nameTh": "บริษัท วิค จำกัด (มหาชน)"},
            {"tk": "PTT", "nameTh": "บริษัท ปตท. จำกัด (มหาชน) ยาวพอแล้ว"},
            {"tk": "CPN", "nameTh": "บริษัท ชื่อซ้ำกันนะ จำกัด (มหาชน)"},
            {"tk": "TU", "nameTh": "บริษัท ชื่อซ้ำกันนะ จำกัด (มหาชน)"},
            {"tk": "SPALI", "nameTh": "บริษัท ชื่อซ้ำกันนะ จำกัด (มหาชน)"},
        ])
        self.assertEqual(got, {"เสนาดีเวลลอปเม้นท์": "SENA"})

    def test_missing_file_means_no_aliases(self):
        self.assertEqual(es.load_thai_aliases(Path("/nonexistent/x.json")), {})

    def test_live_aliases_have_no_duplicates_or_short_names(self):
        self.assertGreater(len(es.THAI_ALIASES), 150)
        self.assertTrue(all(len(k) >= es._MIN_ALIAS_LEN for k in es.THAI_ALIASES))
        self.assertTrue(set(es.THAI_ALIASES.values()) <= es.TICKER_SET)


class TestFindTickers(unittest.TestCase):
    def test_thai_name_without_ticker(self):
        self.assertEqual(es.find_tickers("เสนาดีเวลลอปเม้นท์ เปิดโครงการใหม่"), {"SENA"})

    def test_name_match_is_whitespace_tolerant(self):
        self.assertEqual(es.find_tickers("ไทย ยูเนี่ยน  กรุ๊ป ปรับเป้า"), {"TU"})

    def test_longest_name_wins_and_blocks_inner_ticker(self):
        text = "ทรัสต์เพื่อการลงทุนในสิทธิการเช่าอสังหาริมทรัพย์ CPN รีเทล โกรท จ่ายปันผล"
        self.assertEqual(es.find_tickers(text), {"CPNREIT"})

    def test_names_off_keeps_ticker_only_behaviour(self):
        self.assertEqual(es.find_tickers("เสนาดีเวลลอปเม้นท์", names=False), set())
        self.assertEqual(es.find_tickers("หุ้น SENA", names=False), {"SENA"})

    def test_thai_ticker_passes_unchanged(self):
        self.assertEqual(es.find_tickers("หุ้น WIN ขึ้น, [M] และ PLAT"), {"WIN", "M", "PLAT"})

    def test_english_ignores_bare_capitals(self):
        text = "WIN big as PIN rates ease; ALLY and ZEN rally. PLAT AQUA"
        self.assertEqual(es.find_tickers(text, "en"), set())

    def test_english_accepts_bracket_and_set_prefix(self):
        text = "Wyncoast Industrial Park (WIN) and SET: PIN gain"
        self.assertEqual(es.find_tickers(text, "en"), {"WIN", "PIN"})

    def test_english_brackets_skip_wire_acronyms(self):
        text = "Inflation (CPI) eased, the (PM) said, per (AP)"
        self.assertEqual(es.find_tickers(text, "en"), set())
        self.assertEqual(es.find_tickers("SET: AP and SET:CPI", "en"), {"AP", "CPI"})

    def test_english_skips_thai_names(self):
        self.assertEqual(es.find_tickers("เสนาดีเวลลอปเม้นท์", "en"), set())


class TestNoFilingFlag(unittest.TestCase):
    def _con(self, filings):
        con = duckdb.connect(":memory:")
        con.execute("CREATE TABLE news_items (symbol VARCHAR, datetime_iso VARCHAR)")
        con.executemany("INSERT INTO news_items VALUES (?, ?)", filings)
        return con

    def test_flags_only_names_without_a_nearby_filing(self):
        con = self._con([
            ("SENA", "2026-09-27T17:00:00+07:00"),
            ("TU", "2026-09-10T08:00:00+07:00"),
            ("CPN", "2026-09-29 09:00:00"),  # naive: read as BKK
        ])
        items = [
            {"tk": "SENA", "ts": "2026-09-28T14:33:00+07:00"},
            {"tk": "TU", "ts": "2026-09-28T09:00:00+07:00"},
            {"tk": "CPN", "ts": "2026-09-28T02:00:00+00:00"},
            {"tk": "WHA", "ts": "2026-09-28T09:00:00+07:00"},
            {"tk": "WHA", "ts": "not a date"},
        ]
        be._flag_no_filing(items, be._filing_times(con, ["CPN", "SENA", "TU", "WHA"]))
        self.assertEqual(
            [i.get("noFiling") for i in items], [False, True, False, True, None]
        )

    def test_unreadable_table_leaves_flag_unset(self):
        con = duckdb.connect(":memory:")
        items = [{"tk": "SENA", "ts": "2026-09-28T14:33:00+07:00"}]
        be._flag_no_filing(items, be._filing_times(con, ["SENA"]))
        self.assertNotIn("noFiling", items[0])

    def test_build_writes_flag_and_window(self):
        con = self._con([("SENA", datetime.now(BKK).isoformat())])
        con.execute("""CREATE TABLE external_news (id VARCHAR, source VARCHAR,
            symbol VARCHAR, sector VARCHAR, datetime_iso VARCHAR, headline VARCHAR,
            url VARCHAR, body_excerpt VARCHAR, lang VARCHAR)""")
        now = datetime.now(BKK).isoformat(timespec="seconds")
        con.executemany(
            "INSERT INTO external_news VALUES (?,?,?,?,?,?,?,?,?)",
            [("a", "KAOHOON", "SENA", "PROP", now, "t", "https://x/a", "", "th"),
             ("b", "KAOHOON", "TU", "FOOD", now, "t", "https://x/b", "", "th")],
        )
        with tempfile.TemporaryDirectory() as d:
            old = be.DATA_DIR
            be.DATA_DIR = Path(d)
            try:
                be.build_external_news(con, {"SENA": {"rm": "C"}, "TU": {"rm": "C"}})
                out = json.loads((Path(d) / "external-news.json").read_text(encoding="utf-8"))
            finally:
                be.DATA_DIR = old
        self.assertEqual(out["filingWindowDays"], be.FILING_WINDOW_DAYS)
        self.assertEqual({i["tk"]: i["noFiling"] for i in out["items"]},
                         {"SENA": False, "TU": True})


if __name__ == "__main__":
    unittest.main()
