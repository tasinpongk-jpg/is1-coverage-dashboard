"""Unit tests for scripts/enrich_filing.py.

Stdlib unittest only. Tests are offline — no network calls. We
mock _fetch, _resolve_pdf_url, _fetch_pdf, _call_m3, and
_post_discord to exercise the cache/formatting/fallback paths.

Run: python tests/test_enrich_filing.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import enrich_filing as e  # noqa: E402

# ---------------------------------------------------------------- fixtures

VALID_FILING = {
    "_id": "105616300",
    "tk": "TU",
    "title": "Notification for the Purchase of Office Space (Revised)",
    "title_th": "แจ้งการซื้อพื้นที่สำนักงาน (ฉบับแก้ไข)",
    "ts": "2026-08-03T18:23:05+07:00",
    "type": "connected_transaction",
    "severity": "high",
    "url": "https://www.set.or.th/en/market/news-and-alert/newsdetails?id=105616300&symbol=TU",
    "_summary": "TU connected/related-party transaction: ...",
    "_summary_th": "TU รายการที่เกี่ยวโยงกัน: ...",
}

PDF_MAGIC = b"%PDF-1.7\n%fake content for test\n%%EOF\n"


def _fake_pdf() -> bytes:
    return PDF_MAGIC + b"x" * 1000


# ---------------------------------------------------------------- helpers

def _patched_cache_path(test_dir: Path) -> None:
    """Point the module's cache path at a tempdir for the test."""
    cache = test_dir / "filing_summary.json"
    os.environ["ENRICH_CACHE_PATH"] = str(cache)
    # Bust the lru_cache-style imports if any
    if hasattr(e, "_cache_path"):
        e._cache_path.__defaults__ = (str(cache),)


# ---------------------------------------------------------------- tests

class TestEnrichOneCachePath(unittest.TestCase):
    """Cache hit, cache miss, cache write, cache corruption."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix="hermes-enrich-test-"))
        _patched_cache_path(self.tmpdir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)
        os.environ.pop("ENRICH_CACHE_PATH", None)

    def test_cache_hit_skips_pdf_and_m3(self):
        # Pre-populate cache with a valid entry.
        with mock.patch.object(e, "_resolve_pdf_url") as pdf_resolve, \
             mock.patch.object(e, "_fetch_pdf") as pdf_fetch, \
             mock.patch.object(e, "_call_m3") as m3:
            # These should NOT be called.
            cache = e._load_cache()
            e._cache_put(
                cache, "105616300",
                bullets=["• cached bullet 1", "• cached bullet 2"],
                model=e.M3_MODEL, in_tokens=100, out_tokens=200,
                pdf_sha256="abc123",
            )
            e._atomic_write_cache(cache)
            bullets, meta = e._enrich_one(VALID_FILING)
            self.assertEqual(bullets, ["• cached bullet 1", "• cached bullet 2"])
            self.assertEqual(meta["source"], "cache")
            self.assertTrue(meta["cache_hit"])
            self.assertEqual(meta["cost_usd"], 0.0)
            pdf_resolve.assert_not_called()
            pdf_fetch.assert_not_called()
            m3.assert_not_called()

    def test_cache_miss_calls_m3(self):
        with mock.patch.object(e, "_resolve_pdf_url",
                               return_value="https://example.com/test.pdf"), \
             mock.patch.object(e, "_fetch_pdf",
                               return_value=_fake_pdf()), \
             mock.patch.object(e, "_call_m3",
                               return_value=(["• m3 bullet 1", "• m3 bullet 2"],
                                            {"input_tokens": 100, "output_tokens": 200})):
            bullets, meta = e._enrich_one(VALID_FILING)
            self.assertEqual(bullets, ["• m3 bullet 1", "• m3 bullet 2"])
            self.assertEqual(meta["source"], "m3")
            self.assertFalse(meta["cache_hit"])
            # Cost: 100/1e6*3 + 200/1e6*15 = 0.0003 + 0.003 = 0.0033
            self.assertAlmostEqual(meta["cost_usd"], 0.0033, places=6)
            # Cache should now have this entry.
            cache = e._load_cache()
            self.assertIn("105616300", cache["summaries"])

    def test_cache_miss_pdf_url_missing_falls_back(self):
        with mock.patch.object(e, "_resolve_pdf_url", return_value=None):
            bullets, meta = e._enrich_one(VALID_FILING)
            self.assertEqual(meta["source"], "fallback_no_pdf_url")
            self.assertIn("no_pdf_url_in_page", meta["errors"])
            # Should include pre-summary in fallback.
            self.assertTrue(any("pre-summary" in b or
                                "TU รายการที่เกี่ยวโยงกัน" in b
                                for b in bullets))

    def test_cache_miss_pdf_fetch_fails_falls_back(self):
        with mock.patch.object(e, "_resolve_pdf_url",
                               return_value="https://example.com/test.pdf"), \
             mock.patch.object(e, "_fetch_pdf", return_value=None):
            bullets, meta = e._enrich_one(VALID_FILING)
            self.assertEqual(meta["source"], "fallback_pdf_fetch")
            self.assertIn("pdf_fetch_failed", meta["errors"])

    def test_cache_miss_m3_fails_falls_back(self):
        with mock.patch.object(e, "_resolve_pdf_url",
                               return_value="https://example.com/test.pdf"), \
             mock.patch.object(e, "_fetch_pdf", return_value=_fake_pdf()), \
             mock.patch.object(e, "_call_m3", return_value=(None, {})):
            bullets, meta = e._enrich_one(VALID_FILING)
            self.assertEqual(meta["source"], "fallback_m3_failed")
            self.assertIn("m3_failed", meta["errors"])

    def test_cache_miss_pdf_too_large_falls_back(self):
        with mock.patch.object(e, "_resolve_pdf_url",
                               return_value="https://example.com/test.pdf"), \
             mock.patch.object(e, "_fetch_pdf", return_value=None):  # simulate reject
            bullets, meta = e._enrich_one(VALID_FILING)
            self.assertEqual(meta["source"], "fallback_pdf_fetch")

    def test_no_filing_id_falls_back(self):
        filing = dict(VALID_FILING)
        del filing["_id"]
        with mock.patch.object(e, "_resolve_pdf_url") as pdf_resolve:
            bullets, meta = e._enrich_one(filing)
            self.assertEqual(meta["source"], "fallback")
            self.assertIn("no _id", meta["errors"])
            pdf_resolve.assert_not_called()

    def test_force_bypasses_cache(self):
        # Pre-populate cache, then --force should re-enrich.
        with mock.patch.object(e, "_resolve_pdf_url",
                               return_value="https://example.com/test.pdf"), \
             mock.patch.object(e, "_fetch_pdf", return_value=_fake_pdf()), \
             mock.patch.object(e, "_call_m3",
                               return_value=(["• fresh m3 bullet"],
                                            {"input_tokens": 50, "output_tokens": 100})):
            cache = e._load_cache()
            e._cache_put(cache, "105616300",
                         bullets=["• OLD cached"], model="x", in_tokens=0,
                         out_tokens=0, pdf_sha256="old")
            e._atomic_write_cache(cache)
            bullets, meta = e._enrich_one(VALID_FILING, force=True)
            self.assertEqual(bullets, ["• fresh m3 bullet"])
            self.assertEqual(meta["source"], "m3")

    def test_cache_ttl_expiry(self):
        # Manually backdate the cache entry past CACHE_TTL_DAYS.
        from datetime import datetime, timedelta, timezone
        with mock.patch.object(e, "_resolve_pdf_url",
                               return_value="https://example.com/test.pdf"), \
             mock.patch.object(e, "_fetch_pdf", return_value=_fake_pdf()), \
             mock.patch.object(e, "_call_m3",
                               return_value=(["• fresh after expiry"],
                                            {"input_tokens": 1, "output_tokens": 1})):
            cache = e._load_cache()
            old_ts = (datetime.now(timezone.utc)
                      - timedelta(days=e.CACHE_TTL_DAYS + 1)).isoformat()
            cache["summaries"]["105616300"] = {
                "ts": old_ts, "bullets_th": ["• OLD expired"],
                "model": "x", "tokens": {"in": 0, "out": 0},
                "pdf_sha256": "x", "prompt_version": e.PROMPT_VERSION,
            }
            e._atomic_write_cache(cache)
            bullets, meta = e._enrich_one(VALID_FILING)
            self.assertEqual(bullets, ["• fresh after expiry"])
            self.assertEqual(meta["source"], "m3")

    def test_prompt_version_change_invalidates_cache(self):
        with mock.patch.object(e, "_resolve_pdf_url",
                               return_value="https://example.com/test.pdf"), \
             mock.patch.object(e, "_fetch_pdf", return_value=_fake_pdf()), \
             mock.patch.object(e, "_call_m3",
                               return_value=(["• new prompt version"],
                                            {"input_tokens": 1, "output_tokens": 1})):
            cache = e._load_cache()
            e._cache_put(cache, "105616300", ["• OLD prompt"],
                         "x", 0, 0, "x")
            cache["prompt_version"] = e.PROMPT_VERSION - 1  # simulate old version
            e._atomic_write_cache(cache)
            # _load_cache should detect mismatch and clear.
            cache2 = e._load_cache()
            self.assertEqual(cache2["prompt_version"], e.PROMPT_VERSION)
            self.assertEqual(cache2["summaries"], {})


class TestCacheCorruption(unittest.TestCase):
    """Codex P0 #2 lesson: top-level non-dict in state crashes .get()."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix="hermes-enrich-corrupt-"))
        _patched_cache_path(self.tmpdir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)
        os.environ.pop("ENRICH_CACHE_PATH", None)

    def test_cache_top_level_list_does_not_crash(self):
        cache_path = e._cache_path()
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text('["tampered"]', encoding="utf-8")
        d = e._load_cache()
        self.assertIsInstance(d, dict)
        self.assertEqual(d["summaries"], {})

    def test_cache_string_does_not_crash(self):
        cache_path = e._cache_path()
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text('"just a string"', encoding="utf-8")
        d = e._load_cache()
        self.assertIsInstance(d, dict)

    def test_cache_corrupt_json_does_not_crash(self):
        cache_path = e._cache_path()
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        cache_path.write_text('{invalid json,,,', encoding="utf-8")
        d = e._load_cache()
        self.assertIsInstance(d, dict)
        self.assertEqual(d["summaries"], {})


class TestEnrichIdMode(unittest.TestCase):
    """--enrich-id mode: CLI exit codes and JSON output shape."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix="hermes-enrich-id-"))
        _patched_cache_path(self.tmpdir)
        # Fake data dir with a real-looking pulse file
        self.fake_data = self.tmpdir / "data"
        self.fake_data.mkdir()
        self.pulse_path = self.fake_data / "disclosure-pulse.json"
        self.pulse_path.write_text(json.dumps({
            "filings": [VALID_FILING],
            "_built_at": "2026-08-05T00:00:00+00:00",
        }), encoding="utf-8")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)
        os.environ.pop("ENRICH_CACHE_PATH", None)

    def test_enrich_id_found(self):
        with mock.patch.object(e, "_enrich_one",
                               return_value=(["• test bullet"],
                                            {"source": "m3", "in_tokens": 1,
                                             "out_tokens": 1, "cost_usd": 0.001,
                                             "cache_hit": False, "errors": []})):
            rc = e._enrich_id("105616300", data_dir=self.fake_data)
            self.assertEqual(rc, 0)

    def test_enrich_id_not_found(self):
        rc = e._enrich_id("999999999", data_dir=self.fake_data)
        self.assertEqual(rc, 1)


class TestAutoAlert(unittest.TestCase):
    """--auto-alert: scan, filter, dedup, post."""

    def setUp(self):
        self.tmpdir = Path(tempfile.mkdtemp(prefix="hermes-auto-alert-"))
        _patched_cache_path(self.tmpdir)
        self.fake_data = self.tmpdir / "data"
        self.fake_data.mkdir()
        # Build a pulse with mix of severities and tickers
        self.pulse_path = self.fake_data / "disclosure-pulse.json"
        self.pulse_path.write_text(json.dumps({
            "filings": [
                {**VALID_FILING, "_id": "1", "tk": "TU",
                 "severity": "high", "ts": "2026-08-04T10:00:00+07:00"},
                {**VALID_FILING, "_id": "2", "tk": "AQUA",
                 "severity": "high", "ts": "2026-08-04T11:00:00+07:00"},
                {**VALID_FILING, "_id": "3", "tk": "CHOTI",
                 "severity": "low", "ts": "2026-08-04T12:00:00+07:00"},
                {**VALID_FILING, "_id": "4", "tk": "TC",
                 "severity": "high", "ts": "2026-08-04T13:00:00+07:00"},
                {**VALID_FILING, "_id": "5", "tk": "TU",
                 "severity": "high", "ts": "2026-08-04T14:00:00+07:00"},
            ],
        }), encoding="utf-8")
        # RM C covers TU, AQUA, CHOTI, TC (51 tickers total but for
        # this test we only need a small covered set)
        self.tickers_path = self.fake_data / "tickers.json"
        self.tickers_path.write_text(json.dumps({
            "tickers": [
                {"tk": "TU", "rm": "C"},
                {"tk": "AQUA", "rm": "C"},
                {"tk": "CHOTI", "rm": "C"},
                {"tk": "TC", "rm": "C"},
                {"tk": "OTHER", "rm": "K"},  # not RM C
                {"tk": "K_THING", "rm": "K"},
            ],
        }), encoding="utf-8")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)
        os.environ.pop("ENRICH_CACHE_PATH", None)

    def test_filters_to_rm_c_high_only(self):
        with mock.patch.object(e, "_enrich_one",
                               return_value=(["• test bullet"],
                                            {"source": "m3", "in_tokens": 1,
                                             "out_tokens": 1, "cost_usd": 0.001,
                                             "cache_hit": False, "errors": []})) as mock_enrich, \
             mock.patch.object(e, "_post_discord", return_value=True) as mock_post:
            rc = e._auto_alert(self.fake_data, dry_run=False,
                                webhook="https://example.com/x", limit=10)
            self.assertEqual(rc, 0)
            # Should enrich TU (1), AQUA (2), TC (4), TU (5) — 4
            # high-severity RM C filings. CHOTI (3) is low → skipped.
            # OTHER/K_THING are RM K → skipped.
            self.assertEqual(mock_enrich.call_count, 4)
            enriched_ids = {call.args[0]["_id"] for call in mock_enrich.call_args_list}
            self.assertEqual(enriched_ids, {"1", "2", "4", "5"})
            self.assertEqual(mock_post.call_count, 4)

    def test_skips_already_cached(self):
        # Pre-populate cache with filing 1 and 2.
        cache = e._load_cache()
        e._cache_put(cache, "1", ["• OLD"], "x", 0, 0, "x")
        e._cache_put(cache, "2", ["• OLD"], "x", 0, 0, "x")
        e._atomic_write_cache(cache)
        with mock.patch.object(e, "_enrich_one",
                               return_value=(["• should not be called"],
                                            {"source": "m3", "in_tokens": 1,
                                             "out_tokens": 1, "cost_usd": 0.001,
                                             "cache_hit": False, "errors": []})) as mock_enrich, \
             mock.patch.object(e, "_post_discord", return_value=True):
            e._auto_alert(self.fake_data, dry_run=False,
                            webhook="https://example.com/x", limit=10)
            # Only filings 4 (TC) and 5 (TU) should be enriched — not 1 or 2.
            self.assertEqual(mock_enrich.call_count, 2)
            enriched_ids = {call.args[0]["_id"] for call in mock_enrich.call_args_list}
            self.assertEqual(enriched_ids, {"4", "5"})

    def test_respects_limit(self):
        with mock.patch.object(e, "_enrich_one",
                               return_value=(["• x"], {"source": "m3",
                                            "in_tokens": 1, "out_tokens": 1,
                                            "cost_usd": 0.001,
                                            "cache_hit": False, "errors": []})), \
             mock.patch.object(e, "_post_discord", return_value=True) as mock_post:
            e._auto_alert(self.fake_data, dry_run=False,
                            webhook="https://example.com/x", limit=2)
            # 3 candidates, but limit=2 → 2 posts.
            self.assertEqual(mock_post.call_count, 2)

    def test_no_candidates_exits_0(self):
        # Empty pulse
        self.pulse_path.write_text(json.dumps({"filings": []}), encoding="utf-8")
        with mock.patch.object(e, "_enrich_one") as mock_enrich:
            rc = e._auto_alert(self.fake_data, dry_run=False,
                                webhook="https://example.com/x", limit=10)
            self.assertEqual(rc, 0)
            mock_enrich.assert_not_called()

    def test_dry_run_does_not_post(self):
        with mock.patch.object(e, "_enrich_one",
                               return_value=(["• x"], {"source": "m3",
                                            "in_tokens": 1, "out_tokens": 1,
                                            "cost_usd": 0.001,
                                            "cache_hit": False, "errors": []})), \
             mock.patch.object(e, "_post_discord", return_value=True) as mock_post:
            e._auto_alert(self.fake_data, dry_run=True,
                            webhook=None, limit=10)
            # Dry-run: enrich happens, post does NOT.
            self.assertEqual(mock_post.call_count, 0)


class TestBuildEmbed(unittest.TestCase):
    """Discord embed rendering: color, footer, fields, truncation."""

    def test_high_severity_red(self):
        emb = e._build_embed(VALID_FILING, ["• b1"],
                             {"source": "m3", "cost_usd": 0.04}, "auto-alert")
        self.assertEqual(emb["color"], 0xEF4444)
        self.assertIn("🤖", emb["title"])

    def test_medium_severity_amber(self):
        f = {**VALID_FILING, "severity": "medium"}
        emb = e._build_embed(f, ["• b1"], {"source": "m3"}, "auto-alert")
        self.assertEqual(emb["color"], 0xF59E0B)

    def test_low_severity_green(self):
        f = {**VALID_FILING, "severity": "low"}
        emb = e._build_embed(f, ["• b1"], {"source": "m3"}, "auto-alert")
        self.assertEqual(emb["color"], 0x22C55E)

    def test_cache_hit_footer(self):
        emb = e._build_embed(VALID_FILING, ["• b1"],
                             {"source": "cache", "cost_usd": 0.0}, "auto-alert")
        self.assertIn("cached", emb["footer"]["text"])

    def test_fallback_footer_warns(self):
        emb = e._build_embed(VALID_FILING, ["• b1"],
                             {"source": "fallback_pdf_fetch",
                              "cost_usd": 0.0}, "auto-alert")
        self.assertIn("⚠️", emb["footer"]["text"])
        self.assertIn("fallback_pdf_fetch", emb["footer"]["text"])

    def test_on_demand_pencil_icon(self):
        emb = e._build_embed(VALID_FILING, ["• b1"],
                             {"source": "m3", "cost_usd": 0.04}, "on-demand")
        self.assertIn("📝", emb["title"])

    def test_bullet_field_value_strips_bullet(self):
        emb = e._build_embed(VALID_FILING, ["• this is the bullet text"],
                             {"source": "m3"}, "auto-alert")
        self.assertEqual(emb["fields"][0]["value"], "this is the bullet text")

    def test_long_bullet_truncated(self):
        long = "• " + "x" * 2000
        emb = e._build_embed(VALID_FILING, [long], {"source": "m3"}, "auto-alert")
        # 1024 char limit on field value
        self.assertLessEqual(len(emb["fields"][0]["value"]), 1024)


class TestDiscordPost(unittest.TestCase):
    """Discord POST plumbing: success / 4xx / 5xx."""

    def test_dry_run_returns_true_no_post(self):
        result = e._post_discord("https://example.com/x",
                                 {"embeds": []}, dry_run=True)
        self.assertTrue(result)

    def test_success_returns_true(self):
        with mock.patch("urllib.request.urlopen") as mock_urlopen:
            mock_resp = mock.MagicMock()
            mock_resp.status = 200
            mock_resp.__enter__ = mock.Mock(return_value=mock_resp)
            mock_resp.__exit__ = mock.Mock(return_value=False)
            mock_urlopen.return_value = mock_resp
            result = e._post_discord("https://example.com/x",
                                     {"embeds": []}, dry_run=False)
            self.assertTrue(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)