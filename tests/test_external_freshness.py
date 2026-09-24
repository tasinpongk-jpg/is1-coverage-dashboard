"""Unit tests for the external-source freshness and health signals.

Run from repo root:
    python tests/test_external_freshness.py

Covers the case that let both SEC feeds go stale unnoticed: the daily job
rewrites data/*.json (refreshing asOf and _built_at) even when the upstream
scrape returned nothing, so a badge keyed off either reads "fresh" over rows
that are months old.

Stdlib unittest only — keep test suite dependency-free.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import build_external as b  # noqa: E402

BKK = timezone(timedelta(hours=7))


def _today() -> date:
    return datetime.now(BKK).date()


class TestNewestDate(unittest.TestCase):
    def test_picks_the_maximum_and_ignores_junk(self):
        got = b._newest_date(
            ["2026-05-29", None, "2026-06-14", "", "not-a-date", "2026-01-02"]
        )
        self.assertEqual(got, "2026-06-14")

    def test_accepts_datetimes_alongside_strings(self):
        got = b._newest_date([datetime(2026, 6, 14, 12, 0), "2026-05-29"])
        self.assertEqual(got, "2026-06-14")

    def test_returns_none_when_nothing_usable(self):
        self.assertIsNone(b._newest_date([]))
        self.assertIsNone(b._newest_date([None, "", "garbage"]))


class TestStampFreshness(unittest.TestCase):
    def test_recent_rows_are_not_stale(self):
        payload: dict = {}
        b._stamp_freshness(
            payload, _today().isoformat(), label="external_news", stale_after_days=7
        )
        self.assertEqual(payload["dataAgeDays"], 0)
        self.assertFalse(payload["stale"])

    def test_old_rows_are_flagged_stale(self):
        payload: dict = {}
        old = (_today() - timedelta(days=60)).isoformat()
        b._stamp_freshness(payload, old, label="sec_enforcement", stale_after_days=7)
        self.assertEqual(payload["dataAsOf"], old)
        self.assertEqual(payload["dataAgeDays"], 60)
        self.assertTrue(payload["stale"])

    def test_boundary_day_is_not_yet_stale(self):
        payload: dict = {}
        edge = (_today() - timedelta(days=7)).isoformat()
        b._stamp_freshness(payload, edge, label="sec_form59", stale_after_days=7)
        self.assertFalse(payload["stale"])

    def test_no_rows_at_all_is_stale_with_null_age(self):
        payload: dict = {}
        b._stamp_freshness(payload, None, label="sec_form59", stale_after_days=7)
        self.assertIsNone(payload["dataAsOf"])
        self.assertIsNone(payload["dataAgeDays"])
        self.assertTrue(payload["stale"])


class TestPreserveNonemptySnapshot(unittest.TestCase):
    """The guard protects the first zero but cannot undo one already on disk."""

    def _write(self, tmp: Path, payload: dict) -> Path:
        p = tmp / "snap.json"
        p.write_text(json.dumps(payload), encoding="utf-8")
        return p

    def test_keeps_previous_rows_when_the_scrape_returns_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._write(Path(d), {"total": 2, "items": [{"a": 1}, {"a": 2}]})
            self.assertTrue(b._preserve_nonempty_snapshot(p, {"total": 0}))

    def test_cannot_recover_once_an_empty_snapshot_was_written(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._write(Path(d), {"total": 0, "items": []})
            # Nothing left to preserve — the builder must warn instead of
            # quietly rewriting another empty file.
            self.assertFalse(b._preserve_nonempty_snapshot(p, {"total": 0}))

    def test_a_successful_scrape_always_writes(self):
        with tempfile.TemporaryDirectory() as d:
            p = self._write(Path(d), {"total": 2, "items": [{"a": 1}]})
            self.assertFalse(b._preserve_nonempty_snapshot(p, {"total": 5}))


class TestSourceHealth(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(REPO / "surveillance"))

    def _load_module(self):
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "external_sources_under_test", REPO / "surveillance" / "external_sources.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_failed_source_is_marked_not_ok(self):
        es = self._load_module()
        es.SOURCE_FAILURES.clear()
        es._note_failure("sec_form59", "r59 render: TimeoutError")
        self.assertIn("sec_form59", es.SOURCE_FAILURES)
        self.assertEqual(len(es.SOURCE_FAILURES["sec_form59"]), 1)

    def test_zero_rows_without_failure_is_still_ok(self):
        """A quiet day and an unreachable site must not look the same."""
        es = self._load_module()
        es.SOURCE_FAILURES.clear()
        es._note_failure("sec_form59", "r59 render: TimeoutError")

        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "source-health.json"
            es._write_source_health(
                {"trading_signs": 0, "sec_form59": 0}, path=str(target)
            )
            payload = json.loads(target.read_text(encoding="utf-8"))

        # trading_signs found nothing but the fetch worked; sec_form59 found
        # nothing because the render never returned.
        self.assertTrue(payload["sources"]["trading_signs"]["ok"])
        self.assertFalse(payload["sources"]["sec_form59"]["ok"])
        self.assertEqual(payload["failingCount"], 1)

    def test_partial_run_merges_rather_than_drops_other_sources(self):
        """`--only rss` must not erase the status of sources it did not run."""
        es = self._load_module()
        es.SOURCE_FAILURES.clear()

        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "source-health.json"
            es._note_failure("sec_form59", "r59 render: TimeoutError")
            es._write_source_health({"sec_form59": 0}, path=str(target))

            es.SOURCE_FAILURES.clear()
            es._write_source_health({"external_news": (4, 4)}, path=str(target))
            payload = json.loads(target.read_text(encoding="utf-8"))

        self.assertIn("sec_form59", payload["sources"])
        self.assertFalse(payload["sources"]["sec_form59"]["ok"])
        self.assertTrue(payload["sources"]["external_news"]["ok"])
        self.assertEqual(payload["sources"]["external_news"]["rows"], 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
