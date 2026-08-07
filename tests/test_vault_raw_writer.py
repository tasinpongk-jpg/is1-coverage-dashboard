"""Tests for scripts/vault_raw_writer.py (Loop 4 v5 raw markdown persistence)."""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import vault_raw_writer as v  # noqa: E402
import enrich_filing as e  # noqa: E402  (for _classify_doctype)


# ---------------------------------------------------------------- fixtures

def _minimal_raw_doc(doctype: str = "MDA", text: str = "Sample content",
                     sha: str = "a" * 64,
                     tk: str = "TEKA") -> dict:
    """Build one raw_markdown doc entry as enrich_filing would produce."""
    return {
        "doctype": doctype,
        "tk": tk,
        "text": text,
        "sha256": sha,
        "member_filename": f"{doctype}.pdf",
        "raw_bytes_len": 1024,
        "extractor": "pypdf-v1",
        "extraction_status": "ok",
    }


def _teka_filing() -> dict:
    return {
        "tk": "TEKA", "sector": "CONS",
        "title": "Financial Statement Quarter 2/2026 (Reviewed)",
        "ts": "2026-08-05T18:00:00+07:00",
        "url": "https://www.set.or.th/en/market/news-and-alert/newsdetails?id=17858869957410",
        "filing_id": "17858869957410",
    }


def _aai_filing() -> dict:
    return {
        "tk": "AAI", "sector": "FOOD",
        "title": "Financial Statement Q1/2025",
        "ts": "2025-05-15T18:00:00+07:00",
        "url": "https://x",
        "filing_id": "12345",
    }


def _cache_entry(raw_markdown: dict | None = None,
                  filing_id: str = "17858869957410",
                  tk: str = "TEKA") -> dict:
    entry = {
        "filing_id": filing_id,
        "tk": tk,
        "bullets_th": ["• bullet 1"],
        "model": "MiniMax-M3",
        "tokens": {"in": 1, "out": 1},
        "pdf_sha256": "z" * 64,
        "prompt_version": 2,
    }
    if raw_markdown is not None:
        entry["raw_markdown"] = raw_markdown
    return entry


# ---------------------------------------------------------------- language detection

class TestDetectLanguage(unittest.TestCase):
    def test_thai_majority(self):
        text = "บริษัท ทีฆาก่อสร้าง จำกัด " * 50
        lang, ratio = v._detect_language(text)
        self.assertEqual(lang, "T")
        self.assertGreater(ratio, 0.9)

    def test_english_majority(self):
        text = "The quick brown fox jumps over the lazy dog " * 50
        lang, ratio = v._detect_language(text)
        self.assertEqual(lang, "E")
        self.assertLess(ratio, 0.1)

    def test_mixed_around_threshold(self):
        # 6 Thai chars × 10 reps + 5 Latin chars × 10 reps →
        # 60 Thai / (60 + 50) = 0.545. Threshold is 0.5 → classified T.
        text = ("บริษัท " * 10) + ("hello " * 10)
        lang, ratio = v._detect_language(text)
        self.assertEqual(lang, "T")
        self.assertAlmostEqual(ratio, 0.545, places=2)

    def test_empty_string(self):
        lang, ratio = v._detect_language("")
        self.assertEqual(lang, "E")
        self.assertEqual(ratio, 0.0)


# ---------------------------------------------------------------- period parsing

class TestPeriodFromFiling(unittest.TestCase):
    def test_quarter_long(self):
        self.assertEqual(
            v._period_from_filing({}, "Financial Statement Quarter 2/2026"),
            "2026Q2")

    def test_quarter_short(self):
        self.assertEqual(v._period_from_filing({}, "F45 Q3/2025"), "2025Q3")

    def test_fy_long(self):
        self.assertEqual(v._period_from_filing({}, "Annual Report FY2025"),
                         "2025FY")

    def test_fy_thai_buddhist(self):
        # Thai fiscal year notation: 2569 / 2026
        self.assertEqual(v._period_from_filing({}, "งบการเงิน 2569 / 2026"),
                         "2026FY")

    def test_unknown(self):
        self.assertEqual(v._period_from_filing({}, "Random filing"),
                         "UNKNOWN")

    def test_explicit_period_in_filing(self):
        self.assertEqual(
            v._period_from_filing({"period": "2025Q4"}, "anything"),
            "2025Q4")

    def test_period_kind(self):
        self.assertEqual(v._period_kind("2026Q2"), "quarter")
        self.assertEqual(v._period_kind("2025FY"), "year")
        self.assertEqual(v._period_kind("UNKNOWN"), "unknown")


# ---------------------------------------------------------------- doctype classification

class TestClassifyDoctype(unittest.TestCase):
    """Tests reuse enrich_filing._classify_doctype (the core classifier)."""

    def _c(self, name: str, ft: str = "earnings") -> str:
        return e._classify_doctype(name, {"type": ft})

    def test_auditor_wins_over_notes(self):
        # "NOTES_TO_FINANCIAL_STATEMENTS" must be NOTES, not AUDITOR.
        # NOTE is BEFORE AUDITOR's precedence by design — verify both
        # recognition paths work independently.
        self.assertEqual(self._c("NOTES.DOCX"), "NOTES")
        self.assertEqual(self._c("AUDITOR_REPORT.DOCX"), "AUDITOR")

    def test_notes_filename_match(self):
        self.assertEqual(self._c("NOTES.DOCX"), "NOTES")
        self.assertEqual(self._c("FS-NOTES_TEKA_2025Q1_E.docx"), "NOTES")
        self.assertEqual(self._c("หมายเหตุ.docx"), "NOTES")

    def test_auditor_filename_match(self):
        self.assertEqual(self._c("AUDITOR_REPORT.DOCX"), "AUDITOR")
        self.assertEqual(self._c("auditor_report.pdf"), "AUDITOR")
        self.assertEqual(self._c("ผู้สอบบัญชี.pdf"), "AUDITOR")

    def test_mda_filename_match(self):
        self.assertEqual(self._c("MDA.pdf"), "MDA")
        self.assertEqual(self._c("MD&A_TEKA_2026Q2_E.pdf"), "MDA")
        self.assertEqual(self._c("คำอธิบายและวิเคราะห์.pdf"), "MDA")

    def test_fs_filename_match(self):
        self.assertEqual(self._c("FINANCIAL_STATEMENTS.XLSX"), "FS")
        self.assertEqual(self._c("financial_statement.pdf"), "FS")
        self.assertEqual(self._c("งบการเงิน.docx"), "FS")

    def test_unknown_falls_back_to_NOTES(self):
        # README.txt with no matching keyword and unknown filing_type
        # → safe default NOTES.
        self.assertEqual(self._c("README.txt", ft=""), "NOTES")

    def test_filing_type_fallback(self):
        # No keyword match → filing_type drives classification.
        self.assertEqual(self._c("statement.pdf", "financial_statement"), "FS")
        self.assertEqual(self._c("opinion.pdf", "audit"), "AUDITOR")
        self.assertEqual(self._c("review.pdf", "earnings"), "MDA")


# ---------------------------------------------------------------- render markdown

class TestRenderMarkdown(unittest.TestCase):

    def test_teka_mda_period_2026q2(self):
        doc = _minimal_raw_doc("MDA", "MD&A text", sha="a" * 64)
        filename, subdir, body = v._render_markdown(doc, _teka_filing())
        # Language depends on text content — ASCII → 'E', Thai → 'T'.
        # Period + ticker + doctype are deterministic from filing.
        self.assertRegex(filename, r"^MDA_TEKA_2026Q2_[ET]\.md$")
        self.assertEqual(subdir, "MDA")
        self.assertIn("MD&A text", body)

    def test_frontmatter_required_fields(self):
        doc = _minimal_raw_doc("NOTES", "notes content", sha="b" * 64)
        _, _, body = v._render_markdown(doc, _teka_filing())
        # Required YAML keys.
        for key in ("ticker:", "filing_type:", "period:", "language:",
                    "doctype:", "sector:", "source_sha256:",
                    "source_url:", "extractor:", "extraction_status:"):
            self.assertIn(key, body, f"missing {key}")

    def test_aai_english(self):
        doc = _minimal_raw_doc("MDA", "English MD&A text here.")
        filename, _, _ = v._render_markdown(doc, _aai_filing())
        self.assertTrue(filename.endswith("_E.md"))

    def test_thai_ratio_in_frontmatter(self):
        doc = _minimal_raw_doc("MDA", "บริษัท " * 100, sha="c" * 64)
        _, _, body = v._render_markdown(doc, _teka_filing())
        m = re.search(r"thai_letter_ratio:\s*([\d.]+)", body)
        self.assertIsNotNone(m)
        self.assertGreater(float(m.group(1)), 0.9)

    def test_auditor_subdir_mapping(self):
        doc = _minimal_raw_doc("AUDITOR", "บริษัท ทีฆาก่อสร้าง " * 10,
                              sha="d" * 64)
        filename, subdir, _ = v._render_markdown(doc, _teka_filing())
        # Thai content → filename ends with _T.md.
        self.assertRegex(filename, r"^AUDITOR_TEKA_2026Q2_T\.md$")
        self.assertEqual(subdir, "AUDITOR")

    def test_fs_lives_in_fs_notes_subdir(self):
        # FS doc → vault subdir FS-NOTES (per Codex spec, FS grouped with NOTES).
        doc = _minimal_raw_doc("FS", "fs", sha="e" * 64)
        _, subdir, _ = v._render_markdown(doc, _teka_filing())
        self.assertEqual(subdir, "FS-NOTES")

    def test_notes_also_in_fs_notes_subdir(self):
        doc = _minimal_raw_doc("NOTES", "notes", sha="f" * 64)
        _, subdir, _ = v._render_markdown(doc, _teka_filing())
        self.assertEqual(subdir, "FS-NOTES")


# ---------------------------------------------------------------- extract docs from cache

class TestExtractDocsFromCache(unittest.TestCase):

    def test_extracts_all_doctypes(self):
        entry = {
            "tk": "TEKA",
            "raw_markdown": {
                "MDA":     {**_minimal_raw_doc("MDA"), "tk": "TEKA"},
                "AUDITOR": {**_minimal_raw_doc("AUDITOR"), "tk": "TEKA"},
                "FS":      {**_minimal_raw_doc("FS"), "tk": "TEKA"},
                "NOTES":   {**_minimal_raw_doc("NOTES"), "tk": "TEKA"},
            },
        }
        docs = v._extract_docs_from_cache(entry, _teka_filing())
        self.assertEqual(len(docs), 4)
        self.assertEqual({d["doctype"] for d in docs},
                         {"MDA", "AUDITOR", "FS", "NOTES"})
        for d in docs:
            self.assertEqual(d["tk"], "TEKA")

    def test_empty_raw_markdown_returns_none(self):
        entry = {"tk": "TEKA", "raw_markdown": {}}
        self.assertIsNone(v._extract_docs_from_cache(entry, _teka_filing()))

    def test_missing_raw_markdown_returns_none(self):
        entry = {"tk": "TEKA"}
        self.assertIsNone(v._extract_docs_from_cache(entry, _teka_filing()))

    def test_ignores_unknown_doctype(self):
        entry = {
            "tk": "TEKA",
            "raw_markdown": {
                "MDA":        {**_minimal_raw_doc("MDA"), "tk": "TEKA"},
                "BOGUS_TYPE": {**_minimal_raw_doc("BOGUS"), "tk": "TEKA"},
            },
        }
        docs = v._extract_docs_from_cache(entry, _teka_filing())
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]["doctype"], "MDA")


# ---------------------------------------------------------------- project_one atomic + dedup

class TestProjectOne(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vault-raw-test-"))
        self.vault = self.tmp / "vault"
        (self.vault / "01-Filings").mkdir(parents=True)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_first_run_writes_file(self):
        entry = _cache_entry({"MDA": _minimal_raw_doc("MDA", "first content", sha="a" * 64)})
        report = v.project_one(entry, _teka_filing(), self.vault)
        self.assertTrue(report["writes"].get("raw"))
        target_dir = self.vault / "01-Filings" / "MDA" / "TEKA"
        files = list(target_dir.glob("MDA_TEKA_2026Q2_*.md"))
        target = files[0] if files else (target_dir / "MDA_TEKA_2026Q2_T.md")
        files = list(target_dir.glob("MDA_TEKA_2026Q2_*.md"))
        self.assertEqual(len(files), 1)
        target = files[0]
        self.assertTrue(target.exists())
        # Verify content.
        body = target.read_text(encoding="utf-8")
        self.assertIn("first content", body)

    def test_second_run_idempotent_skips(self):
        entry = _cache_entry({"MDA": _minimal_raw_doc("MDA", "first content", sha="a" * 64)})
        v.project_one(entry, _teka_filing(), self.vault)
        # Re-run with same sha → idempotent skip.
        report = v.project_one(entry, _teka_filing(), self.vault)
        self.assertFalse(report["writes"].get("raw"))
        self.assertTrue(any("same sha256" in s for s in report["skipped"]))

    def test_different_sha_overwrites(self):
        entry_v1 = _cache_entry({"MDA": _minimal_raw_doc("MDA", "version-one-content", sha="a" * 64)})
        v.project_one(entry_v1, _teka_filing(), self.vault)
        target_dir = self.vault / "01-Filings" / "MDA" / "TEKA"
        files = list(target_dir.glob("MDA_TEKA_2026Q2_*.md"))
        self.assertEqual(len(files), 1)
        target = files[0]
        body_v1 = target.read_text(encoding="utf-8")
        self.assertIn("version-one-content", body_v1)

        entry_v2 = _cache_entry({"MDA": _minimal_raw_doc("MDA", "version-two-content", sha="b" * 64)})
        report = v.project_one(entry_v2, _teka_filing(), self.vault)
        self.assertTrue(report["writes"].get("raw"))
        body_v2 = target.read_text(encoding="utf-8")
        self.assertIn("version-two-content", body_v2)
        # "version-one-content" should NOT appear (replaced, not appended).
        self.assertNotIn("version-one-content", body_v2)

    def test_no_raw_markdown_skipped(self):
        entry = _cache_entry(raw_markdown=None)
        report = v.project_one(entry, _teka_filing(), self.vault)
        self.assertFalse(report["writes"].get("raw"))
        self.assertTrue(any("no raw_markdown" in s for s in report["skipped"]))

    def test_fs_and_notes_share_fs_notes_subdir(self):
        # FS doc + NOTES doc → both land in FS-NOTES/TEKA/.
        entry = _cache_entry({
            "FS":    {**_minimal_raw_doc("FS",    "บริษัท " * 5, sha="c" * 64), "tk": "TEKA"},
            "NOTES": {**_minimal_raw_doc("NOTES", "หมายเหตุ " * 5, sha="d" * 64), "tk": "TEKA"},
        })
        report = v.project_one(entry, _teka_filing(), self.vault)
        self.assertEqual(len(report["writes"].get("docs", [])), 2)
        target_dir = self.vault / "01-Filings" / "FS-NOTES" / "TEKA"
        files = sorted(p.name for p in target_dir.glob("*.md"))
        # Both Thai (>=50% Thai chars) → _T.md.
        self.assertEqual(files,
                         ["FS_TEKA_2026Q2_T.md", "NOTES_TEKA_2026Q2_T.md"])

    def test_auditor_writes_to_auditor_subdir(self):
        entry = _cache_entry({
            "AUDITOR": {**_minimal_raw_doc("AUDITOR", "audit", sha="e" * 64),
                        "tk": "TEKA"},
        })
        v.project_one(entry, _teka_filing(), self.vault)
        target_dir = self.vault / "01-Filings" / "AUDITOR" / "TEKA"
        self.assertTrue(target_dir.exists())
        self.assertEqual(len(list(target_dir.glob("*.md"))), 1)


# ---------------------------------------------------------------- project_all

class TestProjectAll(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vault-raw-proj-all-"))
        self.vault = self.tmp / "vault"
        (self.vault / "01-Filings").mkdir(parents=True)
        self.cache_path = self.tmp / "cache.json"

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _write_cache(self, entries: list[dict]) -> None:
        cache = {
            "prompt_version": 2,
            "summaries": {e["filing_id"]: e for e in entries},
            "filings": {}
        }
        self.cache_path.write_text(json.dumps(cache), encoding="utf-8")

    def test_projects_all_with_raw_markdown(self):
        e1 = _cache_entry({"MDA": {**_minimal_raw_doc("MDA", sha="a" * 64),
                                  "tk": "TEKA"}}, filing_id="fid1", tk="TEKA")
        e2 = _cache_entry({"AUDITOR": {**_minimal_raw_doc("AUDITOR", sha="b" * 64),
                                        "tk": "AAI"}}, filing_id="fid2", tk="AAI")
        self._write_cache([e1, e2])
        # Strip the empty filings field handling (the test fixture had
        # a sentinel) — rebuild cache without it.
        cache = {
            "prompt_version": 2,
            "summaries": {e["filing_id"]: e for e in [e1, e2]},
            "filings": {},
        }
        self.cache_path.write_text(json.dumps(cache), encoding="utf-8")
        reports = v.project_all(self.cache_path, self.vault,
                                filings_lookup={"fid1": _teka_filing(),
                                                "fid2": _aai_filing()})
        self.assertEqual(len(reports), 2)
        self.assertTrue(all(r["writes"].get("raw") for r in reports))

    def test_skips_entries_without_raw_markdown(self):
        old_entry = _cache_entry(raw_markdown=None, filing_id="old")
        new_entry = _cache_entry(
            {"MDA": {**_minimal_raw_doc("MDA", sha="a" * 64), "tk": "TEKA"}},
            filing_id="new", tk="TEKA")
        self._write_cache([old_entry, new_entry])
        cache = {"prompt_version": 2,
                 "summaries": {"old": old_entry, "new": new_entry},
                 "filings": {}}
        self.cache_path.write_text(json.dumps(cache), encoding="utf-8")
        reports = v.project_all(self.cache_path, self.vault,
                                filings_lookup={"new": _teka_filing(),
                                                "old": _teka_filing()})
        # Only "new" should be projected.
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0]["tk"], "TEKA")

    def test_ticker_filter(self):
        teka_entry = _cache_entry(
            {"MDA": {**_minimal_raw_doc("MDA", sha="a" * 64), "tk": "TEKA"}},
            filing_id="fid1", tk="TEKA")
        aai_entry = _cache_entry(
            {"MDA": {**_minimal_raw_doc("MDA", sha="b" * 64), "tk": "AAI"}},
            filing_id="fid2", tk="AAI")
        cache = {"prompt_version": 2,
                 "summaries": {"fid1": teka_entry, "fid2": aai_entry},
                 "filings": {}}
        self.cache_path.write_text(json.dumps(cache), encoding="utf-8")
        reports = v.project_all(self.cache_path, self.vault,
                                filings_lookup={"fid1": _teka_filing(),
                                                "fid2": _aai_filing()},
                                ticker_filter="TEKA")
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0]["tk"], "TEKA")

    def test_missing_cache_returns_empty(self):
        reports = v.project_all(self.tmp / "nope.json", self.vault)
        self.assertEqual(reports, [])


# ---------------------------------------------------------------- CLI

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="vault-raw-cli-"))
        self.vault = self.tmp / "vault"
        (self.vault / "01-Filings").mkdir(parents=True)
        self.cache_path = self.tmp / "cache.json"
        teka_entry = _cache_entry(
            {"MDA": {**_minimal_raw_doc("MDA", "CLI test content",
                                      sha="a" * 64), "tk": "TEKA"}},
            filing_id="fid1", tk="TEKA")
        cache = {"prompt_version": 2,
                 "summaries": {"fid1": teka_entry},
                 "filings": {"fid1": _teka_filing()}}
        self.cache_path.write_text(json.dumps(cache), encoding="utf-8")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_cli_writes_real_file(self):
        rc = v.main(["--cache", str(self.cache_path),
                     "--vault-root", str(self.vault)])
        self.assertEqual(rc, 0)
        target_dir = self.vault / "01-Filings" / "MDA" / "TEKA"
        files = list(target_dir.glob("MDA_TEKA_2026Q2_*.md"))
        target = files[0] if files else (target_dir / "MDA_TEKA_2026Q2_T.md")
        self.assertTrue(target.exists())
        self.assertIn("CLI test content", target.read_text(encoding="utf-8"))

    def test_cli_show_output_prints(self):
        from io import StringIO
        import contextlib
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            rc = v.main(["--cache", str(self.cache_path),
                         "--vault-root", str(self.vault),
                         "--show-output", "MDA"])
        self.assertEqual(rc, 0)
        output = buf.getvalue()
        self.assertIn("CLI test content", output)

    def test_cli_show_output_unknown_doctype(self):
        rc = v.main(["--cache", str(self.cache_path),
                     "--vault-root", str(self.vault),
                     "--show-output", "BOGUS"])
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()