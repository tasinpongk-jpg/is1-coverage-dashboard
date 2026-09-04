"""Unit tests for build_daily_brief.py — no live HTTP, no Discord.

Run from repo root:
    python tests/test_build_daily_brief.py

Tests use the live fixtures saved under tests/fixtures/ (snapshotted
from the deployed dashboard 2026-08-04). Add synthetic fixtures for
edge cases.

Stdlib unittest only — keep test suite dependency-free.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import build_daily_brief as b  # noqa: E402

FIX = REPO / "tests" / "fixtures"


def _load_fixture(name: str) -> dict:
    return json.loads((FIX / name).read_text(encoding="utf-8"))


def _maybe_load(name: str) -> dict | None:
    """Load fixture if present, else return None. Lets unit tests run
    without the heavy disclosure_pulse.json (which is gitignored for size)."""
    p = FIX / name
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


# ---------------------------------------------------------------- fixtures

class TestFixtures(unittest.TestCase):
    def test_ai_insights_has_required_keys(self):
        d = _load_fixture("ai_insights_2026-08-04.json")
        for k in ("asOf", "model", "headline", "market_take",
                  "sector_notes", "watchlist", "risk_flags"):
            self.assertIn(k, d, f"ai-insights missing {k!r}")

    def test_morning_brief_has_rows(self):
        d = _load_fixture("morning_brief_2026-08-04.json")
        self.assertGreater(len(d.get("rows") or []), 0)

    def test_tickers_has_rm_field(self):
        d = _load_fixture("tickers_2026-08-04.json")
        rm_c = [t for t in d["tickers"] if t.get("rm") == "C"]
        self.assertGreater(len(rm_c), 0)

    def test_disclosure_pulse_has_filings(self):
        d = _maybe_load("disclosure_pulse_2026-08-04.json")
        if d is None:
            self.skipTest("disclosure_pulse_2026-08-04.json fixture missing (gitignored)")
        self.assertGreater(len(d.get("filings") or []), 0)


# ---------------------------------------------------------------- sections

class TestBuildHeadlineEmbed(unittest.TestCase):
    def test_basic(self):
        ai = _load_fixture("ai_insights_2026-08-04.json")
        emb = b._build_headline_embed(ai, "2026-08-04")
        self.assertIn("title", emb)
        self.assertIn("description", emb)
        self.assertIn(ai["headline"][:30], emb["description"])
        self.assertEqual(len(emb["title"]), min(len(emb["title"]), b.EMBED_TITLE_MAX))

    def test_empty_inputs(self):
        emb = b._build_headline_embed({}, "2026-08-04")
        self.assertIn("title", emb)
        # No crash; risk_flags count = 0 → green color
        self.assertEqual(emb["color"], 0x22C55E)

    def test_high_risk_count_red(self):
        ai = {"headline": "x", "market_take": "y.", "risk_flags": [1, 2, 3, 4]}
        self.assertEqual(b._build_headline_embed(ai, "2026-08-04")["color"], 0xEF4444)


class TestBuildSectorPulseEmbed(unittest.TestCase):
    def test_basic(self):
        brief = _load_fixture("morning_brief_2026-08-04.json")
        emb = b._build_sector_pulse_embed(brief)
        self.assertEqual(len(emb["fields"]), 6)  # top 3 + bottom 3
        # all fields should have name + value
        for f in emb["fields"]:
            self.assertIn("name", f)
            self.assertIn("value", f)

    def test_empty_rows(self):
        emb = b._build_sector_pulse_embed({"rows": []})
        self.assertEqual(emb["fields"], [])

    def test_handles_null_pct1d(self):
        # NWR and GLAND have null pct1d in deployed data — must not crash.
        brief = {"rows": [
            {"tk": "A", "sector": "FOOD", "pct1d": 1.5},
            {"tk": "B", "sector": "FOOD", "pct1d": None},
            {"tk": "C", "sector": "FOOD", "pct1d": -2.5},
            {"tk": "D", "sector": "FOOD", "pct1d": None},
        ]}
        emb = b._build_sector_pulse_embed(brief)
        # Only FOOD sector with 2 valid rows should appear
        names = " ".join(f["name"] for f in emb["fields"])
        self.assertIn("FOOD", names)
        # values should show 1/2 up (only 1 of 2 valid is positive)
        values_text = " ".join(f["value"] for f in emb["fields"])
        self.assertIn("1/2 up", values_text)


class TestBuildRmWatchEmbed(unittest.TestCase):
    def test_basic(self):
        brief = _load_fixture("morning_brief_2026-08-04.json")
        tickers = _load_fixture("tickers_2026-08-04.json")
        rm_c = {t["tk"] for t in tickers["tickers"] if t.get("rm") == "C"}
        emb = b._build_rm_watch_embed(brief, rm_c)
        # Should have at least Top and Bottom fields
        names = " ".join(f.get("name", "") for f in emb["fields"])
        self.assertIn("Top", names)
        self.assertIn("Bottom", names)

    def test_no_rm_tickers(self):
        brief = _load_fixture("morning_brief_2026-08-04.json")
        emb = b._build_rm_watch_embed(brief, set())
        self.assertEqual(emb["fields"], [])

    def test_skips_null_pct1d(self):
        brief = {"rows": [
            {"tk": "X", "sector": "FOOD", "pct1d": None, "hi52": False, "lo52": False},
            {"tk": "Y", "sector": "FOOD", "pct1d": 1.0, "hi52": False, "lo52": False},
        ]}
        emb = b._build_rm_watch_embed(brief, {"X", "Y"})
        # Should not crash; only Y appears in Top
        body = " ".join(f.get("value", "") for f in emb["fields"])
        self.assertIn("Y", body)
        # X has null, should not crash sort


class TestBuildFilingsTodayEmbed(unittest.TestCase):
    def test_basic(self):
        pulse = _maybe_load("disclosure_pulse_2026-08-04.json") or {"filings": []}
        tickers = _load_fixture("tickers_2026-08-04.json")
        rm_c = {t["tk"] for t in tickers["tickers"] if t.get("rm") == "C"}
        emb = b._build_filings_today_embed(pulse, rm_c, "2026-08-04")
        self.assertIn("Counts", emb["fields"][0]["name"])

    def test_empty_filings(self):
        emb = b._build_filings_today_embed({"filings": []}, set(), "2026-08-04")
        self.assertIn("all: 0", emb["fields"][0]["value"])


# ---------------------------------------------------------------- truncation

class TestTruncate(unittest.TestCase):
    def test_short(self):
        self.assertEqual(b._truncate("hello", 10), "hello")

    def test_exact(self):
        self.assertEqual(b._truncate("hello", 5), "hello")

    def test_long(self):
        out = b._truncate("hello world", 5)
        self.assertEqual(out, "hell…")
        self.assertEqual(len(out), 5)


class TestClampFields(unittest.TestCase):
    def test_clamps_long_title(self):
        embeds = [{"title": "x" * 1000, "description": "ok", "fields": []}]
        out = b._clamp_fields(embeds)
        self.assertLessEqual(len(out[0]["title"]), b.EMBED_TITLE_MAX)

    def test_clamps_long_value(self):
        embeds = [{"title": "ok", "fields": [
            {"name": "x" * 1000, "value": "y" * 2000}
        ]}]
        out = b._clamp_fields(embeds)
        self.assertLessEqual(len(out[0]["fields"][0]["name"]), b.EMBED_FIELD_NAME_MAX)
        self.assertLessEqual(len(out[0]["fields"][0]["value"]), b.EMBED_FIELD_VALUE_MAX)


class TestValidateTotalChars(unittest.TestCase):
    def test_under_limit(self):
        embeds = [
            {"title": "a", "description": "b", "fields": [{"name": "n", "value": "v"}],
             "footer": {"text": "f"}}
        ]
        out = b._validate_total_chars(embeds)
        self.assertEqual(len(out), 1)

    def test_over_limit_drops_last(self):
        # Build two embeds where the second one alone exceeds 6000 chars.
        big_value = "x" * 6500
        embeds = [
            {"title": "a", "description": "b", "fields": [{"name": "n", "value": "v"}],
             "footer": {"text": "f"}},
            {"title": "c", "description": "d", "fields": [{"name": "n", "value": big_value}],
             "footer": {"text": "g"}},
        ]
        out = b._validate_total_chars(embeds)
        # Second embed alone is ~6502 chars > 6000 → dropped.
        self.assertEqual(len(out), 1)


# ---------------------------------------------------------------- idempotency

class TestIdempotency(unittest.TestCase):
    def test_already_posted_today_exits_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state = {
                "last_posted_date": b._bkk_today(),
                "last_posted_at": b.datetime.now(b.timezone.utc).isoformat(),
            }
            state_path.write_text(json.dumps(state), encoding="utf-8")
            with b._FileLock(state_path.parent / ".lock") as held:
                self.assertTrue(held)
                s = b._load_json(state_path)
                self.assertEqual(s["last_posted_date"], b._bkk_today())

    def test_tampered_state_list_does_not_crash(self):
        # Codex P0 #2 finding: state.json = '["tampered"]' used to crash
        # with AttributeError. Should now log a warning and return {}.
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            state_path.write_text('["tampered"]', encoding="utf-8")
            s = b._load_state("C")
            self.assertIsInstance(s, dict)
            self.assertEqual(s["last_posted_date"], None)
            self.assertEqual(s["seen_ids"], [])

    def test_tampered_state_string_does_not_crash(self):
        with tempfile.TemporaryDirectory() as tmp:
            state_path = Path(tmp) / "state.json"
            state_path.write_text('"just a string"', encoding="utf-8")
            s = b._load_state("C")
            self.assertIsInstance(s, dict)
            self.assertEqual(s["rm"], "C")  # default filled by setdefault


class TestParseRetryAfter(unittest.TestCase):
    def test_delta_seconds(self):
        self.assertEqual(b._parse_retry_after("120"), 120.0)

    def test_empty_defaults_to_2(self):
        self.assertEqual(b._parse_retry_after(""), 2.0)
        self.assertEqual(b._parse_retry_after(None), 2.0)

    def test_http_date_imf_fixdate(self):
        # Future date — should return positive seconds
        from datetime import datetime, timedelta, timezone
        future = datetime.now(timezone.utc) + timedelta(seconds=300)
        date_str = future.strftime("%a, %d %b %Y %H:%M:%S GMT")
        result = b._parse_retry_after(date_str)
        # Should be ~300s (clamped to [0, 300])
        self.assertGreater(result, 200)
        self.assertLessEqual(result, 300)

    def test_http_date_in_past_returns_zero(self):
        from datetime import datetime, timedelta, timezone
        past = datetime.now(timezone.utc) - timedelta(hours=1)
        date_str = past.strftime("%a, %d %b %Y %H:%M:%S GMT")
        result = b._parse_retry_after(date_str)
        self.assertEqual(result, 0.0)

    def test_unparseable_falls_back_to_2(self):
        self.assertEqual(b._parse_retry_after("garbage"), 2.0)

    def test_clamped_to_max_300(self):
        # Far-future date → clamp to 300
        from datetime import datetime, timedelta, timezone
        far_future = datetime.now(timezone.utc) + timedelta(days=365)
        date_str = far_future.strftime("%a, %d %b %Y %H:%M:%S GMT")
        result = b._parse_retry_after(date_str)
        self.assertEqual(result, 300.0)


class TestIsRiskItem(unittest.TestCase):
    """Tests for keyword-driven risk flag detection (TH + EN)."""

    def test_thai_bankruptcy(self):
        self.assertTrue(b._is_risk_item({"title": "บริษัทถูกฟ้องล้มละลาย", "excerpt": ""}))

    def test_thai_default(self):
        self.assertTrue(b._is_risk_item({"title": "ผิดนัดชำระหนี้", "excerpt": "ข่าวจาก..."}))

    def test_thai_delisting(self):
        self.assertTrue(b._is_risk_item({"title": "หุ้นเข้าข่ายถูกเพิกถอน", "excerpt": ""}))

    def test_english_delisting(self):
        self.assertTrue(b._is_risk_item({"title": "Firm faces delisting risk", "excerpt": ""}))

    def test_english_qualified_opinion(self):
        self.assertTrue(b._is_risk_item({
            "title": "Audit report",
            "excerpt": "Auditor issued a qualified opinion on the FY2025 financials",
        }))

    def test_benign_title_is_not_risk(self):
        self.assertFalse(b._is_risk_item({"title": "Q2 รายได้โต 33% QoQ", "excerpt": "บริษัทฯ..."}))

    def test_empty_input_is_not_risk(self):
        self.assertFalse(b._is_risk_item({"title": "", "excerpt": ""}))
        self.assertFalse(b._is_risk_item({}))

    def test_case_insensitive(self):
        # English keywords must match regardless of case in the haystack.
        self.assertTrue(b._is_risk_item({"title": "DELISTING imminent", "excerpt": ""}))
        self.assertTrue(b._is_risk_item({"title": "Risk of Bankruptcy", "excerpt": ""}))


class TestPickNewsForEmbed(unittest.TestCase):
    """RM-C first, market fallback rule."""

    def _mk(self, tk, ts, source="HOONSMART"):
        return {
            "id": f"id-{tk}-{ts}",
            "tk": tk,
            "ts": ts,
            "source": source,
            "title": f"news about {tk}",
            "url": f"https://example.com/{tk}",
        }

    def test_rm_c_priority_when_enough(self):
        items = [
            self._mk("X", "2026-09-04T10:00:00+07:00"),
            self._mk("Y", "2026-09-04T09:00:00+07:00"),
            self._mk("Z", "2026-09-04T08:00:00+07:00"),
            self._mk("OTHER", "2026-09-04T11:00:00+07:00"),  # newer but not RM-C
        ]
        rm_c = {"X", "Y", "Z"}
        picked, label = b._pick_news_for_embed(items, rm_c)
        self.assertEqual(label, "rm-c")
        self.assertEqual([it["tk"] for it in picked], ["X", "Y", "Z"])

    def test_fallback_when_rm_c_below_min(self):
        # Only 2 RM-C items but threshold is 3 → market fallback.
        items = [
            self._mk("X", "2026-09-04T10:00:00+07:00"),
            self._mk("Y", "2026-09-04T09:00:00+07:00"),
            self._mk("A", "2026-09-04T11:00:00+07:00"),
            self._mk("B", "2026-09-04T10:30:00+07:00"),
            self._mk("C", "2026-09-04T10:15:00+07:00"),
        ]
        rm_c = {"X", "Y"}
        picked, label = b._pick_news_for_embed(items, rm_c)
        self.assertEqual(label, "market-fallback")
        # Newest-first across all sources
        self.assertEqual([it["tk"] for it in picked], ["A", "B", "C", "X", "Y"])

    def test_empty_returns_none_label(self):
        picked, label = b._pick_news_for_embed([], {"X"})
        self.assertEqual(picked, [])
        self.assertEqual(label, "none")

    def test_caps_at_max_rows(self):
        items = [self._mk("X", f"2026-09-04T{10 - i:02d}:00:00+07:00") for i in range(20)]
        rm_c = {"X"}
        picked, _ = b._pick_news_for_embed(items, rm_c, max_rows=5)
        self.assertEqual(len(picked), 5)

    def test_handles_missing_tk(self):
        # Items without tk field are treated as market-wide, not RM-C.
        items = [
            {"id": "1", "tk": "", "ts": "2026-09-04T10:00:00+07:00", "title": "macro"},
            {"id": "2", "ts": "2026-09-04T11:00:00+07:00", "title": "no-tk-field"},  # no tk at all
            self._mk("X", "2026-09-04T09:00:00+07:00"),
        ]
        rm_c = {"X"}
        picked, label = b._pick_news_for_embed(items, rm_c, rm_min=1)
        self.assertEqual(label, "rm-c")
        self.assertEqual([it["tk"] for it in picked], ["X"])

    def test_rm_min_threshold(self):
        # 3 RM-C items with rm_min=4 → fallback.
        items = [self._mk("X", f"2026-09-04T{10 - i:02d}:00:00+07:00") for i in range(3)]
        rm_c = {"X"}
        _, label = b._pick_news_for_embed(items, rm_c, rm_min=4)
        self.assertEqual(label, "market-fallback")


class TestBuildNewsEmbed(unittest.TestCase):
    """Full embed builder."""

    def _mk_item(self, tk, ts, source="HOONSMART", title="test", url="https://e.com/1", risk=False):
        if risk:
            title = title + " — ฟ้องล้มละลาย"
        return {
            "id": f"id-{tk}-{ts}",
            "tk": tk,
            "ts": ts,
            "source": source,
            "title": title,
            "url": url,
        }

    def test_returns_none_when_no_items(self):
        emb = b._build_news_embed({"items": [], "sources": []}, {"X"}, "2026-09-04")
        self.assertIsNone(emb)

    def test_rm_c_title_when_priority_hits(self):
        items = [self._mk_item("X", f"2026-09-04T{10 - i:02d}:00:00+07:00") for i in range(4)]
        emb = b._build_news_embed({"items": items, "sources": ["HOONSMART"]}, {"X"}, "2026-09-04")
        self.assertIsNotNone(emb)
        self.assertIn("RM-C News Watch", emb["title"])
        self.assertEqual(len(emb["fields"]), 4)

    def test_market_fallback_title_when_below_min(self):
        items = [self._mk_item("X", "2026-09-04T10:00:00+07:00")]
        emb = b._build_news_embed({"items": items, "sources": ["RYT9"]}, {"X"}, "2026-09-04")
        self.assertIn("Market News Watch", emb["title"])
        self.assertIn("no RM-C hits", emb["title"])

    def test_red_color_when_any_item_is_risk(self):
        items = [
            self._mk_item("X", "2026-09-04T10:00:00+07:00"),
            self._mk_item("Y", "2026-09-04T09:00:00+07:00", risk=True),
            self._mk_item("Z", "2026-09-04T08:00:00+07:00"),
        ]
        emb = b._build_news_embed({"items": items, "sources": ["HOONSMART"]}, {"X", "Y", "Z"}, "2026-09-04")
        self.assertEqual(emb["color"], 0xEF4444)
        self.assertIn("⚠️ flagged keywords", emb["footer"]["text"])

    def test_cyan_color_when_all_clean(self):
        items = [self._mk_item("X", f"2026-09-04T{10 - i:02d}:00:00+07:00") for i in range(4)]
        emb = b._build_news_embed({"items": items, "sources": ["HOONSMART"]}, {"X"}, "2026-09-04")
        self.assertEqual(emb["color"], 0x06B6D4)

    def test_footer_marks_scope(self):
        items = [self._mk_item("X", f"2026-09-04T{10 - i:02d}:00:00+07:00") for i in range(3)]
        emb = b._build_news_embed({"items": items, "sources": ["HOONSMART", "RYT9"]}, {"X"}, "2026-09-04")
        self.assertIn("scope=rm-c", emb["footer"]["text"])
        self.assertIn("HOONSMART", emb["footer"]["text"])

    def test_field_names_include_ticker_and_source(self):
        items = [self._mk_item("ITC", "2026-09-04T10:00:00+07:00", source="HOONSMART")]
        emb = b._build_news_embed({"items": items, "sources": ["HOONSMART"]}, {"ITC"}, "2026-09-04")
        # Field name = source label + ticker
        self.assertIn("HOONSMART", emb["fields"][0]["name"])
        self.assertIn("ITC", emb["fields"][0]["name"])

    def test_field_value_is_hyperlink(self):
        items = [self._mk_item("X", "2026-09-04T10:00:00+07:00", title="ข่าวดี", url="https://example.com/x")]
        emb = b._build_news_embed({"items": items, "sources": ["HOONSMART"]}, {"X"}, "2026-09-04")
        self.assertIn("[ข่าวดี](https://example.com/x)", emb["fields"][0]["value"])

    def test_caps_at_5_rows(self):
        items = [self._mk_item("X", f"2026-09-04T{10 - i:02d}:00:00+07:00") for i in range(20)]
        emb = b._build_news_embed({"items": items, "sources": ["HOONSMART"]}, {"X"}, "2026-09-04")
        self.assertEqual(len(emb["fields"]), 5)

    def test_total_chars_under_6000(self):
        """Integration check: 5 fields × 1024 + title + footer must
        fit under 6000 chars so the validate_total_chars helper doesn't
        drop this embed."""
        items = [
            self._mk_item(
                "X",
                f"2026-09-04T{10 - i:02d}:00:00+07:00",
                title="A" * 200,  # max-truncated title
                url="https://example.com/" + "x" * 800,
            )
            for i in range(5)
        ]
        emb = b._build_news_embed({"items": items, "sources": ["HOONSMART"]}, {"X"}, "2026-09-04")
        total = (
            len(emb["title"])
            + sum(len(f["name"]) + len(f["value"]) for f in emb["fields"])
            + len(emb["footer"]["text"])
        )
        self.assertLess(total, 6000)


# ---------------------------------------------------------------- main entry

class TestMainFailClosed(unittest.TestCase):
    def test_no_webhook_exits_1(self):
        # Clear env and ensure fail-closed (NOT silent dry-run like Phase 1).
        env_save = os.environ.copy()
        os.environ.pop("DAILY_BRIEF_WEBHOOK", None)
        # Also override HOME so the secret-file fallback returns None
        # (otherwise ~/.hermes/secrets/daily_brief.env on this dev host
        # would mask the fail-closed behavior we're testing).
        # Path.home() on Windows resolves from USERPROFILE, so we need
        # USERPROFILE set too — HOME alone is not enough.
        fake_home = tempfile.mkdtemp(prefix="hermes-no-secret-home-")
        os.environ["USERPROFILE"] = fake_home
        os.environ["HOME"] = fake_home
        os.environ["DAILY_BRIEF_STATE_DIR"] = str(tempfile.mkdtemp())
        try:
            rc = b.main()
            self.assertEqual(rc, 1)
        finally:
            os.environ.clear()
            os.environ.update(env_save)
            import shutil
            shutil.rmtree(fake_home, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)