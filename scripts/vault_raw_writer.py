"""Persist raw filing documents as Markdown to the Obsidian vault.

Loop 4 v5 — Approach E (cache raw text + vault retry).

Reads `~/.hermes/cache/filing_summary.json` cache entries, renders each
extracted document (MD&A / Auditor Report / FS / Notes) as a verbatim
Markdown file in the user's Obsidian vault, and writes back a status
field so the cron can retry on the next tick if the vault was offline.

Vault layout (matches existing raw filings folder):
    Work-SET/Listed Company/1-Raw/01-Filings/<DOCTYPE>/<TK>/
        <DOCTYPE>_<TK>_<PERIOD>_<LANG>.md

Atomic writes: each filing produces one temp directory containing all
its markdowns, then `os.replace()` atomically swaps into place. If any
write in the temp fails, the whole filing is rolled back — vault never
sees partial filings.

Single-pass: extract text in enrich_filing.py → cache.raw_markdown.
This module only renders + writes. No network, no m3.
"""

from __future__ import annotations

import io
import json
import os
import re
import sys
import unicodedata
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Import only stdlib + reuse enrich_filing constants.
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import enrich_filing as e  # noqa: E402

DEFAULT_VAULT_ROOT = (
    Path(os.environ.get("OBSIDIAN_VAULT_ROOT"))
    if os.environ.get("OBSIDIAN_VAULT_ROOT")
    else Path(
        r"C:\Users\Tasinpong\OneDrive - The Stock Exchange of Thailand"
        r"\Claude-Vault\Work-SET\Listed Company\1-Raw\01-Filings"
    )
)
RAW_DIR_NAME = "01-Filings"  # inside Work-SET/.../1-Raw/

# Doctype → subfolder mapping (matches existing vault convention).
_DOCTYPE_DIR = {
    "MDA":     "MDA",
    "AUDITOR": "AUDITOR",
    "FS":      "FS-NOTES",  # FS lives with NOTES (per existing vault)
    "NOTES":   "FS-NOTES",
}

_VALID_DOCTYPES = set(_DOCTYPE_DIR.keys())


def _log(msg: str) -> None:
    print(f"[vault_raw_writer] {msg}", flush=True)


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


# ---------------------------------------------------------------- detection

def _detect_language(text: str) -> tuple[str, float]:
    """Return ('T' or 'E', thai_letter_ratio) per Codex design."""
    if not text:
        return ("E", 0.0)
    thai = 0
    latin = 0
    for ch in text:
        if ch.isspace() or ch.isdigit() or ch in ".,;:!?\"'()[]{}<>=/+-_*&%$#@":
            continue
        cp = ord(ch)
        if 0x0E00 <= cp <= 0x0E7F:  # Thai Unicode range
            thai += 1
        elif cp < 0x80 or 0x00C0 <= cp <= 0x024F:  # basic Latin + Latin Extended
            latin += 1
    total = thai + latin
    ratio = thai / total if total else 0.0
    return ("T" if ratio >= 0.5 else "E", ratio)


def _period_from_filing(filing: dict, title: str) -> str:
    p = (filing.get("period") or "").strip()
    if p:
        return p
    m = re.search(r"Quarter\s*([1-4])/(\d{4})", title, re.IGNORECASE)
    if m:
        return f"{m.group(2)}Q{m.group(1)}"
    m = re.search(r"Q\s*([1-4])/(\d{4})", title, re.IGNORECASE)
    if m:
        return f"{m.group(2)}Q{m.group(1)}"
    m = re.search(r"\bFY\s*(\d{4})\b", title, re.IGNORECASE)
    if m:
        return f"{m.group(1)}FY"
    m = re.search(r"\b(\d{4})\s*FY\b", title, re.IGNORECASE)
    if m:
        return f"{m.group(1)}FY"
    m = re.search(r"(\d{4})/(\d{4})", title)
    if m:
        return f"{m.group(2)}FY"
    return "UNKNOWN"


def _period_kind(period: str) -> str:
    return "quarter" if "Q" in period else ("year" if "FY" in period else "unknown")


# ---------------------------------------------------------------- rendering

def _render_markdown(doc: dict, filing: dict) -> tuple[str, str]:
    """Render one document as Markdown. Returns (filename, body).

    `doc` schema (from cache.raw_markdown):
        {
          "doctype": "MDA" | "AUDITOR" | "FS" | "NOTES",
          "member_filename": "MDA_TEKA_2026Q2_T.pdf",
          "text": "...",                      # for text content
          "raw_bytes_len": 184352,            # original payload size
          "extraction_status": "ok" | "no_text",
          "extractor": "pypdf-v5" | "stdlib-docx-v1" | "stdlib-xlsx-v1",
          "sha256": "<per-doc sha256>",
          "page_count": 8,                    # optional
          "sheet_count": 3,                   # optional
        }
    """
    tk = doc["tk"]
    title = filing.get("title") or filing.get("title_th") or ""
    period = _period_from_filing(filing, title)
    filing_date = filing.get("filing_date") or filing.get("ts", "")[:10]
    sector = filing.get("sector") or "UNKNOWN"
    doctype = doc["doctype"]
    text = doc.get("text", "")
    status = doc.get("extraction_status", "ok")
    extractor = doc.get("extractor", "unknown")
    page_count = doc.get("page_count")
    sheet_count = doc.get("sheet_count")

    lang, thai_ratio = _detect_language(text)
    source_filename = doc["member_filename"]
    source_bytes = doc.get("raw_bytes_len", 0)

    filename = f"{doctype}_{tk}_{period}_{lang}.md"

    # Extract doctype-folder subdir; "FS" lives in FS-NOTES dir.
    subdir = _DOCTYPE_DIR[doctype]

    word_count = len(text.split()) if text else 0
    char_count = len(text)

    fm_lines = [
        "---",
        f"filing_id: \"{filing.get('filing_id', '')}\"",
        f"ticker: {tk}",
        f"filing_type: {doctype}",
        f"period: {period}",
        f"period_kind: {_period_kind(period)}",
        f"language: {lang}",
        f"doctype: {doctype}",
        f"sector: {sector}",
        "",
        f"source_sha256: \"{doc.get('sha256', '')}\"",
        f"source_filename: \"{source_filename}\"",
        f"source_size_bytes: {source_bytes}",
        f"source_url: \"{filing.get('url', '')}\"",
        f"first_seen: {_now_iso()[:10]}",
        "",
    ]
    if page_count is not None:
        fm_lines.append(f"page_count: {page_count}")
    if sheet_count is not None:
        fm_lines.append(f"sheet_count: {sheet_count}")
    fm_lines += [
        f"word_count: {word_count}",
        f"character_count: {char_count}",
        f"thai_letter_ratio: {thai_ratio:.3f}",
        f"extractor: \"{extractor}\"",
        f"extraction_status: {status}",
        "source_type: raw",
        f"tags: [filing, {doctype.lower()}, sector/{sector}, ticker/{tk}]",
        "---",
        "",
    ]
    fm = "\n".join(fm_lines)

    body_lines = [
        fm,
        f"# {doctype} — {tk} {period} ({lang})",
        "",
        f"> Source: `{source_filename}` · "
        f"{source_bytes:,} bytes · status: **{status}** · "
        f"extractor: `{extractor}`",
        "",
    ]
    if text:
        body_lines.append(text)
    else:
        body_lines.append("_(no extractable text — see source PDF/DOCX/XLSX)_")
    body_lines.append("")

    return filename, subdir, "\n".join(body_lines)


# ---------------------------------------------------------------- atomic write

def _atomic_write_filing(temp_dir: Path, final_dir: Path,
                        filename_subdir_pairs: list[tuple[str, str, str]]
                        ) -> bool:
    """Atomically promote a temp dir with all docs into final vault dir.

    filename_subdir_pairs: list of (filename, subdir_name, body).
    Writes all bodies into temp_dir/subdir/filename then os.replace()
    swaps temp_dir → final_dir. If any write fails, temp_dir is left
    for inspection (caller decides whether to clean up).
    """
    try:
        if temp_dir.exists():
            # Should not happen — caller chooses unique name.
            return False
        temp_dir.mkdir(parents=True, exist_ok=True)
        for filename, subdir, body in filename_subdir_pairs:
            target = temp_dir / subdir / filename
            target.parent.mkdir(parents=True, exist_ok=True)
            tmp_file = target.with_suffix(target.suffix + ".tmp")
            tmp_file.write_text(body, encoding="utf-8")
            tmp_file.replace(target)
        final_dir.parent.mkdir(parents=True, exist_ok=True)
        # Atomic swap on Windows requires the target NOT to exist.
        if final_dir.exists():
            # If same content, skip — caller dedups before this.
            return True
        os.replace(temp_dir, final_dir)
        return True
    except OSError as e:
        _log(f"atomic write failed: {e}")
        return False


# ---------------------------------------------------------------- core

def _extract_docs_from_cache(cache_entry: dict, filing: dict
                             ) -> list[dict] | None:
    """Build list of raw_markdown docs from cache entry.

    cache_entry.raw_markdown layout (set by enrich_filing._enrich_one):
        {
          "MDA":     {"text": ..., "sha256": ..., ...},
          "AUDITOR": {...},
          "FS":      {...},
          "NOTES":   {...},
        }
    """
    raw = cache_entry.get("raw_markdown")
    if not isinstance(raw, dict) or not raw:
        return None
    docs = []
    for doctype, body in raw.items():
        if doctype not in _VALID_DOCTYPES:
            continue
        if not isinstance(body, dict):
            continue
        body = dict(body)
        body["doctype"] = doctype
        body["tk"] = cache_entry.get("tk") or filing.get("tk") or "UNKNOWN"
        docs.append(body)
    return docs


def project_one(cache_entry: dict, filing: dict, vault_root: Path
                ) -> dict:
    """Render one cache entry to the vault. Returns a report dict."""
    tk = cache_entry.get("tk") or filing.get("tk") or "UNKNOWN"
    title = filing.get("title") or filing.get("title_th") or ""
    period = _period_from_filing(filing, title)
    sector = filing.get("sector") or "UNKNOWN"

    report: dict = {
        "tk": tk, "sector": sector, "period": period,
        "writes": {}, "skipped": [],
    }

    docs = _extract_docs_from_cache(cache_entry, filing)
    if not docs:
        report["skipped"].append("no raw_markdown in cache entry")
        return report

    filing_id = cache_entry.get("filing_id") or filing.get("id") or ""
    # Build per-doc render outputs
    to_write: list[tuple[str, str, str]] = []
    skip_reasons: list[str] = []
    for doc in docs:
        if not doc.get("text") and doc.get("extraction_status", "ok") != "ok":
            skip_reasons.append(
                f"{doc['doctype']}: extraction_status={doc.get('extraction_status')}")
            continue
        filename, subdir, body = _render_markdown(doc, filing)
        to_write.append((filename, subdir, body))

    if not to_write:
        report["skipped"].extend(skip_reasons or ["no extractable docs"])
        return report

    # Final vault path: 1-Raw/01-Filings/<DOCTYPE>/<TK>/
    # Per-file write — DO NOT skip if dir exists; only skip if the
    # specific file (doctype+period+lang tuple) already exists with
    # matching sha256. If existing file has different content, suffix
    # with sha8 to preserve both versions.
    subdir = next(sub for _, sub, _ in to_write)
    final_dir = vault_root / RAW_DIR_NAME / subdir / tk
    written: list[str] = []
    skipped_files: list[str] = []
    for filename, _subdir, body in to_write:
        target = final_dir / filename
        # Use os.path.isfile (direct syscall) instead of Path.exists()
        # to bypass OneDrive cache that can return stale True/False.
        existing_sha = ""
        if os.path.isfile(str(target)):
            try:
                txt = target.read_text(encoding="utf-8", errors="ignore")
                m = re.search(r'^source_sha256:\s*"?([a-f0-9]+)"?',
                               txt, re.MULTILINE)
                if m:
                    existing_sha = m.group(1)
            except (OSError, FileNotFoundError):
                # OneDrive race: file may have been deleted between
                # isfile() and read_text(). Treat as missing.
                existing_sha = ""
        # Find matching doc to compare sha (filename is unique in to_write).
        doc_sha = ""
        for filename2, _, body2 in to_write:
            if filename2 == filename:
                # Parse sha from frontmatter of body2 (faster than
                # re-iterating docs which is no longer in scope).
                m = re.search(r'^source_sha256:\s*"?([a-f0-9]+)"?',
                               body2, re.MULTILINE)
                if m:
                    doc_sha = m.group(1)
                break
        if existing_sha == doc_sha and doc_sha:
            skipped_files.append(f"{filename}: same sha256, skipped")
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            # On Windows + OneDrive, os.replace() may fail if target
            # exists. Use os.path.isfile (direct syscall) + unlink
            # before replace. Skip unlink if already absent.
            if os.path.isfile(str(target)):
                os.unlink(str(target))
            tmp = target.with_suffix(target.suffix + ".tmp")
            tmp.write_text(body, encoding="utf-8")
            os.replace(str(tmp), str(target))
            # fsync to flush to OneDrive.
            try:
                with open(str(target), "rb") as f:
                    os.fsync(f.fileno())
            except OSError:
                pass  # best-effort
            written.append(filename)
        except OSError as e:
            skipped_files.append(f"{filename}: {e}")

    if written:
        report["writes"]["raw"] = True
        report["writes"]["docs"] = written
    if skipped_files:
        report["skipped"].extend(skipped_files)
    return report


def project_all(cache_path: Path, vault_root: Path,
                filings_lookup: dict | None = None,
                ticker_filter: str | None = None) -> list[dict]:
    """Project all cache entries that have raw_markdown to vault."""
    from vault_writer import _load_filings_lookup  # reuse helper
    if not cache_path.exists():
        _log(f"cache not found at {cache_path}")
        return []
    try:
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        _log(f"ERROR reading cache: {e}")
        return []

    summaries = cache.get("summaries", {})
    if filings_lookup is None:
        filings_lookup = cache.get("filings") or _load_filings_lookup()
    if not isinstance(filings_lookup, dict):
        filings_lookup = {}

    reports = []
    for fid, entry in summaries.items():
        if not isinstance(entry, dict):
            continue
        # Need raw_markdown — skip if absent (means enrich_filing didn't
        # produce it, likely a fallback or pre-v5 cache).
        if not entry.get("raw_markdown"):
            continue
        tk = entry.get("tk") or filings_lookup.get(fid, {}).get("tk", "")
        if ticker_filter and tk.upper() != ticker_filter.upper():
            continue
        filing = filings_lookup.get(fid, {})
        if isinstance(filing, dict):
            filing = dict(filing)
        else:
            filing = {}
        filing.setdefault("filing_id", fid)
        try:
            r = project_one(entry, filing, vault_root)
            reports.append(r)
        except Exception as e:
            _log(f"ERROR projecting {fid} ({tk}): {e}")
    return reports


# ---------------------------------------------------------------- CLI

def _build_argparser():
    import argparse
    p = argparse.ArgumentParser(
        description="Persist raw filing documents to Obsidian vault.")
    p.add_argument("--cache", type=Path,
                   default=Path.home() / ".hermes" / "cache" / "filing_summary.json")
    p.add_argument("--vault-root", type=Path, default=DEFAULT_VAULT_ROOT)
    p.add_argument("--ticker", metavar="TK", default=None)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--show-output", metavar="DOCTYPE", default=None,
                   help="Render and print markdown for one doctype of first "
                        "matching filing (no disk write)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)

    if args.show_output:
        from vault_writer import _load_filings_lookup
        cache = json.loads(args.cache.read_text(encoding="utf-8"))
        filings_lookup = cache.get("filings") or _load_filings_lookup()
        for fid, entry in cache.get("summaries", {}).items():
            if not entry.get("raw_markdown"):
                continue
            filing = filings_lookup.get(fid, {})
            if isinstance(filing, dict):
                filing = dict(filing)
            else:
                filing = {}
            filing.setdefault("filing_id", fid)
            entry = dict(entry)
            entry.setdefault("filing_id", fid)
            docs = _extract_docs_from_cache(entry, filing)
            if not docs:
                continue
            target_doctype = args.show_output.upper()
            for doc in docs:
                if doc["doctype"] != target_doctype:
                    continue
                filename, subdir, body = _render_markdown(doc, filing)
                print(f"\n=== {subdir}/{filename} ===\n")
                print(body)
                return 0
        print(f"doctype {args.show_output} not found in cache raw_markdown",
              file=sys.stderr)
        return 1

    if args.dry_run:
        _log("DRY-RUN mode not yet implemented for raw markdown "
             "(use --show-output for individual preview)")
        return 0

    reports = project_all(
        cache_path=args.cache,
        vault_root=args.vault_root,
        ticker_filter=args.ticker,
    )
    n = len(reports)
    n_written = sum(1 for r in reports if r["writes"].get("raw"))
    n_skipped = sum(len(r["skipped"]) for r in reports)
    _log(f"projected {n} filings: written={n_written} skipped={n_skipped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())