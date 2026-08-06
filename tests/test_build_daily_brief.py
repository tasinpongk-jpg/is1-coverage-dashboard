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
        pulse = _load_fixture("disclosure_pulse_2026-08-04.json")
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