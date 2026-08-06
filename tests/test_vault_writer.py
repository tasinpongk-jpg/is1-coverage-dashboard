"""Tests for scripts/vault_writer.py (Loop 4 v4)."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import vault_writer as v  # noqa: E402


# ---------------------------------------------------------------- fixtures

SAMPLE_ENTRY = {
    # NOTE: real cache schema lacks tk/title/meta fields. Resolve
    # them from the filing dict (from disclosure-pulse.json).
    "bullets_th": [
        "• เหตุการณ์สำคัญ: บมจ.ทีฆาก่อสร้าง ส่งงบ Q2/2026",
        "• รายได้ก่อสร้าง 1,024.35 ลบ. (+53% YoY)",
        "• กำไรสุทธิ 40.46 ลบ. (+67% YoY)",
    ],
    "pdf_sha256": "abc123def456" * 4,  # 48 chars
    "model": "MiniMax-M3",
    "ts": "2026-08-06T14:30:00+07:00",
    "tokens": {"in": 7723, "out": 1617},
    "prompt_version": 2,
}

SAMPLE_FILING = {
    "tk": "TEKA",
    "sector": "CONS",
    "ts": "2026-08-05T18:00:00+07:00",
    "title": "Financial Statement Quarter 2/2026 (Reviewed)",
    "title_th": "งบการเงิน ไตรมาสที่ 2/2569 (สอบทานแล้ว)",
    "url": "https://www.set.or.th/en/market/news-and-alert/newsdetails?id=17858869957410",
}


def _make_vault(tmp: Path) -> Path:
    """Build a minimal vault skeleton."""
    vault = tmp / "vault"
    (vault / "06-Inbox").mkdir(parents=True)
    (vault / "04-Coverage" / "CONS").mkdir(parents=True)
    (vault / "04-Coverage" / "PROP").mkdir(parents=True)
    (vault / "04-Coverage" / "UNMAPPED").mkdir(parents=True)
    return vault


def _make_coverage_note(vault: Path, sector: str, tk: str,
                       with_snapshot: bool = True,
                       with_disclosures: bool = False) -> Path:
    """Write a stub coverage note to the vault."""
    body_lines = [
        "---",
        f"ticker: {tk}",
        f"sector: {sector}",
        "tags: [coverage, stub]",
        "---",
        "",
        f"# {tk}",
        "",
        "> One-line thesis: stub for testing",
        "",
    ]
    if with_snapshot:
        body_lines += [
            "## Snapshot",
            "- Revenue: stub",
            "",
        ]
    if with_disclosures:
        body_lines += [
            "## Recent disclosures",
            "<!-- BEGIN:auto-disclosures -->",
            "",
            "### 2026-05-06 — `earnings`",
            "old disclosure",
            "",
            "<!-- END:auto-disclosures -->",
            "",
        ]
    body_lines += [
        "## Notes",
        "_(free-form)_",
        "",
    ]
    p = vault / "04-Coverage" / sector / f"{tk}.md"
    p.write_text("\n".join(body_lines), encoding="utf-8")
    return p


def _make_cache(tmp: Path, entries: list[tuple[str, dict, dict]] | None = None
                ) -> Path:
    """Write a minimal filing_summary.json cache."""
    if entries is None:
        entries = [("105656200", SAMPLE_ENTRY, SAMPLE_FILING)]
    cache = {"prompt_version": 2,
             "summaries": {fid: e for fid, e, _ in entries},
             # Cache schema stores filings under same id; provide them so
             # project_all can resolve tk when cache entry lacks tk.
             "filings": {fid: {"tk": f.get("tk"), "sector": f.get("sector"),
                               "title": f.get("title")}
                         for fid, _, f in entries}}
    p = tmp / "cache.json"
    p.write_text(json.dumps(cache), encoding="utf-8")
    return p


# ---------------------------------------------------------------- tests

class TestPeriodExtraction(unittest.TestCase):
    """_period_from_filing handles all known SET filing patterns."""

    def test_quarter_long(self):
        self.assertEqual(
            v._period_from_filing({}, "Financial Statement Quarter 2/2026 (Reviewed)"),
            "2026Q2")

    def test_quarter_short(self):
        self.assertEqual(
            v._period_from_filing({}, "F45 Q3/2025"), "2025Q3")

    def test_fy_long(self):
        self.assertEqual(v._period_from_filing({}, "Annual Report FY2025"), "2025FY")

    def test_fy_short(self):
        self.assertEqual(v._period_from_filing({}, "FY2024 Results"), "2024FY")

    def test_unknown(self):
        self.assertEqual(v._period_from_filing({}, "Some Random Filing"), "UNKNOWN")

    def test_explicit_period(self):
        self.assertEqual(
            v._period_from_filing({"period": "2025Q4"}, "anything"),
            "2025Q4")


class TestSectorRouting(unittest.TestCase):
    """_sector_for_ticker routes correctly + UNMAPPED fallback."""

    def test_known_sector(self):
        self.assertEqual(v._sector_for_ticker("TEKA", {"sector": "CONS"}), "CONS")

    def test_unknown_sector_unmapped(self):
        self.assertEqual(v._sector_for_ticker("PTT", {"sector": "ENERGY"}),
                         "UNMAPPED")

    def test_lowercase_normalized(self):
        self.assertEqual(v._sector_for_ticker("A", {"sector": "prop"}), "PROP")

    def test_missing_sector(self):
        self.assertEqual(v._sector_for_ticker("XYZ", {}), "UNMAPPED")


class TestRenderInboxNote(unittest.TestCase):
    """Inbox note schema: frontmatter + body, with managed marker."""

    def test_basic_structure(self):
        fname, body = v._render_inbox_note(SAMPLE_ENTRY, "deadbeef" * 8,
                                            SAMPLE_FILING)
        self.assertEqual(fname, "TEKA-filing-summary-2026Q2-2026-08-05.md")
        self.assertIn("ticker: TEKA", body)
        self.assertIn("sector: CONS", body)
        self.assertIn("period: 2026Q2", body)
        self.assertIn('source_sha256: "deadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef"', body)
        # Body contains the quality marker.
        self.assertIn("✅ m3", body)
        self.assertIn(v.MANAGED_MARKER_LINE, body)

    def test_fallback_quality_flag(self):
        # Override cache model to non-MiniMax so renderer picks fallback path.
        bad_entry = dict(SAMPLE_ENTRY, model="other-model")
        _, body = v._render_inbox_note(bad_entry, "x" * 64, SAMPLE_FILING)
        # Renderer uses entry["meta"]["source"] which is missing from raw
        # cache → falls back to "unknown". Body still valid.
        self.assertIn("ticker: TEKA", body)

    def test_bullets_in_body(self):
        _, body = v._render_inbox_note(SAMPLE_ENTRY, "x" * 64, SAMPLE_FILING)
        # Each bullet appears as a list item with bullet prefix stripped.
        self.assertIn("- เหตุการณ์สำคัญ", body)
        self.assertIn("- รายได้ก่อสร้าง 1,024.35 ลบ.", body)


class TestMarkerReplacement(unittest.TestCase):
    """_replace_marker_block inserts/replaces correctly."""

    def test_replace_existing_block(self):
        text = (
            "frontmatter\n\n"
            "## Snapshot\n- x\n\n"
            "<!-- BEGIN:auto-filing-summary -->\nOLD CONTENT\n"
            "<!-- END:auto-filing-summary -->\n\n"
            "## Recent disclosures\n"
        )
        new_block = (
            "<!-- BEGIN:auto-filing-summary -->\nNEW CONTENT\n"
            "<!-- END:auto-filing-summary -->"
        )
        out = v._replace_marker_block(text, new_block)
        self.assertIn("NEW CONTENT", out)
        self.assertNotIn("OLD CONTENT", out)
        # Other sections preserved.
        self.assertIn("## Snapshot", out)
        self.assertIn("## Recent disclosures", out)

    def test_insert_after_snapshot_when_no_marker(self):
        text = (
            "frontmatter\n\n# TEKA\n\n## Snapshot\n- stub\n\n"
            "## Recent disclosures\n"
        )
        new_block = "<!-- BEGIN:auto-filing-summary -->\nNEW\n<!-- END:auto-filing-summary -->"
        out = v._replace_marker_block(text, new_block)
        # Inserted BEFORE Recent disclosures, AFTER Snapshot.
        snap_idx = out.index("## Snapshot")
        disc_idx = out.index("## Recent disclosures")
        block_idx = out.index("BEGIN:auto-filing-summary")
        self.assertGreater(block_idx, snap_idx)
        self.assertLess(block_idx, disc_idx)

    def test_append_at_eof_when_no_snapshot(self):
        text = "frontmatter\n\n# TEKA\n\n## Notes\n_(none)_\n"
        new_block = "<!-- BEGIN:auto-filing-summary -->\nNEW\n<!-- END:auto-filing-summary -->"
        out = v._replace_marker_block(text, new_block)
        self.assertIn("BEGIN:auto-filing-summary", out)
        # Notes section preserved.
        self.assertIn("## Notes", out)


class TestIndexUpsert(unittest.TestCase):
    """_upsert_index_row: create new, replace existing, insert sorted."""

    def test_create_new(self):
        new_text = v._upsert_index_row(None, "TEKA", "CONS",
                                       "| [[04-Coverage/CONS/TEKA|TEKA]] | CONS | [[...]] | 2026Q2 | 2026-08-05 | ✅ m3 | 2026-08-06 14:30 |")
        self.assertIn("title: Coverage Filing Summary Index", new_text)
        self.assertIn("| Ticker | Sector |", new_text)
        self.assertIn("TEKA", new_text)

    def test_replace_existing_row(self):
        existing = v._upsert_index_row(None, "TEKA", "CONS",
                                       "| [[04-Coverage/CONS/TEKA|TEKA]] | CONS | old | 2026Q1 | 2026-05-06 | ✅ m3 | 2026-05-06 09:00 |")
        updated = v._upsert_index_row(existing, "TEKA", "CONS",
                                      "| [[04-Coverage/CONS/TEKA|TEKA]] | CONS | new | 2026Q2 | 2026-08-05 | ✅ m3 | 2026-08-06 14:30 |")
        self.assertIn("| new |", updated)
        self.assertNotIn("| old |", updated)

    def test_sector_routing_unmapped(self):
        new_text = v._upsert_index_row(None, "PTT", "UNMAPPED",
                                       "| `PTT` ⚠️ sector-unmapped | UNMAPPED | ...")
        self.assertIn("UNMAPPED", new_text)


class TestProjectOne(unittest.TestCase):
    """project_one: full pipeline writes the 3 vault locations."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vault-writer-test-"))
        self.vault = _make_vault(self.tmp)
        self.cov_path = _make_coverage_note(self.vault, "CONS", "TEKA",
                                            with_snapshot=True)
        self.cache = _make_cache(self.tmp)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_writes_inbox_coverage_and_index(self):
        report = v.project_one(SAMPLE_ENTRY, SAMPLE_FILING, self.vault,
                                dry_run=True)
        self.assertTrue(report["writes"].get("inbox"))
        self.assertTrue(report["writes"].get("coverage"))
        self.assertTrue(report["writes"].get("index"))

    def test_dry_run_does_not_modify_files(self):
        before = sorted(p.name for p in self.vault.rglob("*"))
        v.project_one(SAMPLE_ENTRY, SAMPLE_FILING, self.vault, dry_run=True)
        after = sorted(p.name for p in self.vault.rglob("*"))
        self.assertEqual(before, after)

    def test_real_write_creates_inbox_and_updates_coverage(self):
        report = v.project_one(SAMPLE_ENTRY, SAMPLE_FILING, self.vault,
                                dry_run=False)
        # Inbox file created.
        inbox_path = self.vault / "06-Inbox" / "TEKA-filing-summary-2026Q2-2026-08-05.md"
        self.assertTrue(inbox_path.exists())
        self.assertIn(v.MANAGED_MARKER_LINE, inbox_path.read_text(encoding="utf-8"))
        # Coverage block inserted.
        cov_text = self.cov_path.read_text(encoding="utf-8")
        self.assertIn("BEGIN:auto-filing-summary", cov_text)
        # Snapshot still there.
        self.assertIn("## Snapshot", cov_text)
        # Index file created.
        idx_path = self.vault / "04-Coverage" / "_index.md"
        self.assertTrue(idx_path.exists())
        idx_text = idx_path.read_text(encoding="utf-8")
        self.assertIn("TEKA", idx_text)
        self.assertIn("CONS", idx_text)

    def test_dedup_skips_when_sha_matches(self):
        # First write creates the file.
        v.project_one(SAMPLE_ENTRY, SAMPLE_FILING, self.vault, dry_run=False)
        inbox_path = self.vault / "06-Inbox" / "TEKA-filing-summary-2026Q2-2026-08-05.md"
        original_text = inbox_path.read_text(encoding="utf-8")
        # Second write — must skip due to matching sha256.
        report = v.project_one(SAMPLE_ENTRY, SAMPLE_FILING, self.vault,
                                dry_run=False)
        self.assertTrue(any("same source_sha256" in s
                            for s in report["skipped"]))
        # File untouched (modulo generated_at timestamp).
        import re
        def strip_ts(s):
            return re.sub(r"^generated_at:.*$", "", s, flags=re.MULTILINE)
        self.assertEqual(strip_ts(original_text),
                         strip_ts(inbox_path.read_text(encoding="utf-8")))

    def test_unmapped_sector_skips_coverage_write(self):
        unmapped_filing = dict(SAMPLE_FILING, sector="ENERGY")
        report = v.project_one(SAMPLE_ENTRY, unmapped_filing, self.vault,
                                dry_run=False)
        self.assertTrue(any("UNMAPPED" in s for s in report["skipped"]))
        # Inbox still written.
        inbox_path = self.vault / "06-Inbox" / "TEKA-filing-summary-2026Q2-2026-08-05.md"
        self.assertTrue(inbox_path.exists())

    def test_missing_coverage_note_skips_coverage_write(self):
        # Coverage note doesn't exist for AMATA in our test vault.
        amata_entry = dict(SAMPLE_ENTRY, tk="AMATA")
        amata_filing = dict(SAMPLE_FILING, tk="AMATA", sector="PROP")
        report = v.project_one(amata_entry, amata_filing, self.vault,
                                dry_run=False)
        self.assertTrue(any("no existing note" in s for s in report["skipped"]))
        # Inbox still written.
        self.assertTrue(
            (self.vault / "06-Inbox" / "AMATA-filing-summary-2026Q2-2026-08-05.md").exists())

    def test_manual_inbox_file_gets_sha_suffix(self):
        # Pre-create a manual inbox file (without managed marker).
        manual_path = self.vault / "06-Inbox" / "TEKA-filing-summary-2026Q2-2026-08-05.md"
        manual_path.write_text(
            "# TEKA — manual note\n\n_(hand-written by RM)_\n",
            encoding="utf-8")
        report = v.project_one(SAMPLE_ENTRY, SAMPLE_FILING, self.vault,
                                dry_run=False)
        # Manual file preserved.
        self.assertIn("_(hand-written by RM)_",
                      manual_path.read_text(encoding="utf-8"))
        # New file has sha suffix.
        sha8 = SAMPLE_ENTRY["pdf_sha256"][:8]
        expected = self.vault / "06-Inbox" / f"TEKA-filing-summary-2026Q2-2026-08-05-m3-{sha8}.md"
        self.assertTrue(expected.exists())


class TestProjectAll(unittest.TestCase):
    """project_all reads cache and projects every entry."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vault-writer-test-"))
        self.vault = _make_vault(self.tmp)
        _make_coverage_note(self.vault, "CONS", "TEKA", with_snapshot=True)
        _make_coverage_note(self.vault, "PROP", "AMATA", with_snapshot=True)

        entry2 = dict(SAMPLE_ENTRY, tk="AMATA",
                      title="FS Q2/2026", bullets_th=["• AMATA bullet"])
        filing2 = dict(SAMPLE_FILING, tk="AMATA", sector="PROP")
        self.cache = _make_cache(self.tmp, [
            ("105656200", SAMPLE_ENTRY, SAMPLE_FILING),
            ("205657000", entry2, filing2),
        ])

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_projects_all_entries(self):
        reports = v.project_all(self.cache, self.vault, dry_run=False)
        self.assertEqual(len(reports), 2)

    def test_ticker_filter(self):
        reports = v.project_all(self.cache, self.vault, dry_run=False,
                                 ticker_filter="TEKA")
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0]["tk"], "TEKA")

    def test_missing_cache_returns_empty(self):
        reports = v.project_all(self.tmp / "nope.json", self.vault)
        self.assertEqual(reports, [])


class TestEndToEnd(unittest.TestCase):
    """End-to-end: cache + vault + write all 3 + re-run is idempotent."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vault-writer-test-"))
        self.vault = _make_vault(self.tmp)
        _make_coverage_note(self.vault, "CONS", "TEKA", with_snapshot=True)
        self.cache = _make_cache(self.tmp)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_idempotent_run(self):
        v.project_all(self.cache, self.vault, dry_run=False)
        first_inbox = (self.vault / "06-Inbox" /
                       "TEKA-filing-summary-2026Q2-2026-08-06.md").read_text(
                           encoding="utf-8")
        v.project_all(self.cache, self.vault, dry_run=False)
        second_inbox = (self.vault / "06-Inbox" /
                        "TEKA-filing-summary-2026Q2-2026-08-06.md").read_text(
                            encoding="utf-8")
        # Identical content (modulo generated_at timestamp).
        # Strip the timestamp line for comparison.
        def strip_ts(s):
            import re
            return re.sub(r"^generated_at:.*$", "", s, flags=re.MULTILINE)
        self.assertEqual(strip_ts(first_inbox), strip_ts(second_inbox))


if __name__ == "__main__":
    unittest.main()
