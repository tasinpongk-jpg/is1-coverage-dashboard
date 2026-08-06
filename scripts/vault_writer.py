"""Persist m3-enriched filing summaries into the Obsidian vault.

Reads ~/.hermes/cache/filing_summary.json (written by enrich_filing.py)
and projects the latest summary per ticker into the user's Obsidian
vault under Claude-Vault/Work-SET/Listed Company/2-Analysis/AI-Generated/.

Three writes per filing event:

  1. Canonical historical note — 06-Inbox/<TK>-filing-summary-<PERIOD>-<DATE>.md
     YAML frontmatter + 3-section Thai body (key events, performance, material notes).
     Idempotent on source_sha256: if a note with the same hash already
     exists, restore from cache and skip re-write.

  2. Latest-summary projection — 04-Coverage/<SECTOR>/<TK>.md
     Inserts (or replaces) a <!-- BEGIN:auto-filing-summary --> block.
     Placement: directly AFTER the existing ## Snapshot section so it
     sits at the top of the body, before ## Recent disclosures and other
     manual sections. If the note doesn't exist yet, no stub is created
     (per design — user routes 06-Inbox manually to 04-Coverage).

  3. Master index row — 04-Coverage/_index.md
     Updates one row per ticker (latest filing only). Stable
     (Sector, Ticker) sort; on missing index file, creates a new one.

Design rules (from Codex review, 2026-08-06):
  - source_sha256 is the durable dedup key, NOT filename.
  - Unknown sector → index under UNMAPPED with ⚠️ flag, no new folder.
  - fallback_* result → write with ⚠️ flag so it's visible and replaceable.
  - Manual 06-Inbox file (no managed marker) → suffix -m3-<sha8>, never overwrite.
  - Dry-run mode prints what would be written without touching disk.

Vault root defaults to the user's known OneDrive path. Override via
OBSIDIAN_VAULT_ROOT env var (used by tests + CI).
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------- vault constants

# Default vault root (OneDrive on this host). Override via env var.
DEFAULT_VAULT_ROOT = (
    Path(os.environ.get("OBSIDIAN_VAULT_ROOT"))
    if os.environ.get("OBSIDIAN_VAULT_ROOT")
    else Path(
        r"C:\Users\Tasinpong\OneDrive - The Stock Exchange of Thailand"
        r"\Claude-Vault\Work-SET\Listed Company\2-Analysis\AI-Generated"
    )
)

# Sub-paths relative to vault root.
INBOX_DIR_NAME = "06-Inbox"
COVERAGE_DIR_NAME = "04-Coverage"
INDEX_FILE_NAME = "_index.md"

# Marker block (must match pattern of auto-thaibma-bonds and
# auto-disclosures already in 04-Coverage notes).
FILING_SUMMARY_BEGIN = "<!-- BEGIN:auto-filing-summary -->"
FILING_SUMMARY_END = "<!-- END:auto-filing-summary -->"
FILING_SUMMARY_HEADER = (
    "<!-- AUTO-MAINTAINED by is1-coverage-dashboard. "
    "Do not edit between markers. -->"
)

# Sectors with existing coverage folders. Anything else routes to UNMAPPED.
KNOWN_SECTORS = {"AGRI", "CONMAT", "CONS", "FOOD", "PFREIT", "PROP"}

# Default cache location (matches enrich_filing.py).
CACHE_DEFAULT = Path.home() / ".hermes" / "cache" / "filing_summary.json"
# Default disclosure-pulse.json (used to resolve tk/sector/title when
# cache["filings"] is missing — which is the current real state).
DISCLOSURE_PULSE_DEFAULT = Path(__file__).resolve().parent.parent / "data" / "disclosure-pulse.json"

# Provenance marker — used to detect files WE wrote vs manual.
MANAGED_MARKER_LINE = "<!-- is1-coverage-dashboard managed -->"


def _load_filings_lookup(repo_path: Path | None = None) -> dict:
    """Build a {filing_id: {tk, sector, title, ts, url}} lookup from
    disclosure-pulse.json. Used when cache['filings'] is missing
    (current real state)."""
    import json
    p = DISCLOSURE_PULSE_DEFAULT
    if not p.exists():
        return {}
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        _log(f"WARN: could not read disclosure-pulse.json: {e}")
        return {}
    items = d.get("filings", [])
    out: dict = {}
    for it in items:
        fid = str(it.get("_id") or "")
        if not fid:
            continue
        out[fid] = {
            "tk": it.get("tk", ""),
            "sector": it.get("sector", ""),
            "title": it.get("title") or it.get("title_th") or "",
            "ts": it.get("ts", ""),
            "url": it.get("url", ""),
        }
    return out


# ---------------------------------------------------------------- helpers

def _log(msg: str) -> None:
    print(f"[vault_writer] {msg}", flush=True)


def _now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _sha8(s: str) -> str:
    import hashlib
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:8]


def _period_from_filing(filing: dict, title: str) -> str:
    """Extract period string (YYYYQN or YYYYFY) from filing metadata.

    Tries filing['period'] first (some datasets include it), then falls
    back to regex over the title. Returns 'UNKNOWN' if nothing matches.
    """
    p = (filing.get("period") or "").strip()
    if p:
        return p
    # Title patterns: "Quarter 2/2026", "Q2/2026", "FY2025", "Annual 2025"
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
    m = re.search(r"(\d{4})/(\d{4})", title)  # Thai FY2569 / 2026
    if m:
        return f"{m.group(2)}FY"
    return "UNKNOWN"


def _filing_date_iso(filing: dict) -> str:
    """ISO date (YYYY-MM-DD) extracted from filing ts/title. Falls back to today."""
    ts = (filing.get("ts") or filing.get("fetched_at") or "").strip()
    if ts:
        # Try ISO parse
        try:
            return datetime.fromisoformat(ts.replace("Z", "+00:00")).date().isoformat()
        except ValueError:
            # Try date-only prefix
            m = re.match(r"^(\d{4}-\d{2}-\d{2})", ts)
            if m:
                return m.group(1)
    return datetime.now(timezone.utc).date().isoformat()


def _sector_for_ticker(tk: str, filing: dict) -> str:
    """Resolve sector — filing metadata first, fallback UNMAPPED."""
    sec = (filing.get("sector") or filing.get("_sector") or "").strip().upper()
    if sec and sec in KNOWN_SECTORS:
        return sec
    return "UNMAPPED"


# ---------------------------------------------------------------- renderers

def _render_inbox_note(entry: dict, source_sha256: str,
                       filing: dict) -> tuple[str, str]:
    """Return (filename, body) for 06-Inbox canonical filing summary.

    `filename` excludes the .md extension.
    """
    tk = entry.get("tk") or filing.get("tk") or "UNKNOWN"
    title = entry.get("title") or filing.get("title") or filing.get("title_th") or ""
    period = _period_from_filing(filing, title)
    filing_date = _filing_date_iso(filing)
    sector = _sector_for_ticker(tk, filing)
    bullets = entry.get("bullets_th", [])
    meta = entry.get("meta", {})
    if not meta:
        # Synthesize from real cache fields
        meta = {
            "source": "m3" if entry.get("model") == "MiniMax-M3" else "unknown",
            "in_tokens": entry.get("tokens", {}).get("in", 0),
            "out_tokens": entry.get("tokens", {}).get("out", 0),
            "document_count": 1,
        }
    source = meta.get("source", "unknown")
    cost = meta.get("cost_usd")
    if cost is None:
        cost = (meta.get("in_tokens", 0) / 1e6) * 3.0 + \
               (meta.get("out_tokens", 0) / 1e6) * 15.0
    in_tok = meta.get("in_tokens", 0)
    out_tok = meta.get("out_tokens", 0)
    doc_count = meta.get("document_count", 1)

    quality_flag = "✅ m3" if source == "m3" else "⚠️ fallback"

    # Filename: <TK>-filing-summary-<PERIOD>-<DATE>.md
    fname = f"{tk}-filing-summary-{period}-{filing_date}.md"

    fm = (
        "---\n"
        f"ticker: {tk}\n"
        f"sector: {sector}\n"
        f"period: {period}\n"
        f"filing_date: {filing_date}\n"
        f"filing_title: \"{title}\"\n"
        f"source_type: ai-generated\n"
        "generated_by: is1-coverage-dashboard\n"
        "report_type: filing-summary\n"
        f"summary_source: {source}\n"
        f"model: {entry.get('model', 'MiniMax-M3')}\n"
        f"source_sha256: \"{source_sha256}\"\n"
        f"generated_at: {_now_iso()}\n"
        f"derived_from:\n"
        f"  - \"[[MDA_{tk}_{period}_T]]\"\n"
        f"  - \"[[FS_{tk}_{period}_T]]\"\n"
        f"  - \"[[NOTES_{tk}_{period}_T]]\"\n"
        "tags: [filing-summary, inbox, auto-enriched]\n"
        f"{MANAGED_MARKER_LINE}\n"
        "---\n"
    )

    # Body — quality header + bullets. Each bullet becomes a section.
    body_lines = [
        f"# {tk} — สรุปงบ {period}",
        "",
        f"> {quality_flag} · {doc_count} document(s) · "
        f"{in_tok}/{out_tok} tokens · ${cost:.4f}",
        f"> source_sha256: `{source_sha256[:16]}...`",
        "",
    ]

    if bullets:
        body_lines.append("## m3 Thai bullets")
        body_lines.append("")
        for b in bullets:
            body_lines.append(f"- {b.lstrip('• ').strip()}")
        body_lines.append("")
    else:
        body_lines.append("## m3 Thai bullets")
        body_lines.append("")
        body_lines.append("_(no bullets returned)_")
        body_lines.append("")

    body_lines.append("## Provenance")
    body_lines.append("")
    body_lines.append(
        f"- Generated by `enrich_filing.py` (Loop 4 v3), "
        f"projected into vault by `vault_writer.py` (Loop 4 v4)"
    )
    body_lines.append(f"- Filing URL: {filing.get('url', '')}")
    body_lines.append(f"- Cache key: `{source_sha256[:16]}...`")
    body_lines.append("")

    body = fm + "\n".join(body_lines)
    return fname, body


def _render_filing_summary_block(entry: dict, source_sha256: str,
                                 filing: dict, inbox_rel_link: str) -> str:
    """Return the contents to put inside auto-filing-summary markers.

    Includes the leading comment lines so a fresh file gets a complete
    block, while a re-write replaces only the interior.
    """
    tk = entry.get("tk") or filing.get("tk") or "UNKNOWN"
    title = entry.get("title") or filing.get("title") or filing.get("title_th") or ""
    period = _period_from_filing(filing, title)
    filing_date = _filing_date_iso(filing)
    meta = entry.get("meta", {})
    source = meta.get("source") or ("m3" if entry.get("model") == "MiniMax-M3"
                                     else "unknown")
    quality_flag = "✅ m3" if source == "m3" else "⚠️ fallback"
    bullets = entry.get("bullets_th", [])

    lines = [
        FILING_SUMMARY_BEGIN,
        FILING_SUMMARY_HEADER,
        "## Latest filing summary",
        "",
        f"**{period} · {filing_date} · {quality_flag}**  ",
        f"[[{inbox_rel_link}|{title}]]",
        "",
    ]
    if bullets:
        for b in bullets:
            lines.append(f"- {b.lstrip('• ').strip()}")
    else:
        lines.append("_(no m3 bullets)_")
    lines.append("")
    lines.append(FILING_SUMMARY_END)
    return "\n".join(lines)


def _render_index_row(entry: dict, source_sha256: str, filing: dict,
                      inbox_filename: str) -> str:
    """Return one markdown table row for 04-Coverage/_index.md."""
    tk = entry.get("tk") or filing.get("tk") or "UNKNOWN"
    title = entry.get("title") or filing.get("title") or filing.get("title_th") or ""
    period = _period_from_filing(filing, title)
    filing_date = _filing_date_iso(filing)
    sector = _sector_for_ticker(tk, filing)
    meta = entry.get("meta", {})
    source = meta.get("source") or ("m3" if entry.get("model") == "MiniMax-M3"
                                     else "unknown")
    quality_flag = "✅ m3" if source == "m3" else "⚠️ fallback"
    fetched_at = entry.get("fetched_at") or entry.get("ts") or _now_iso()
    # Short timestamp HH:MM
    short_ts = fetched_at[:16].replace("T", " ")

    coverage_link = (
        f"[[04-Coverage/{sector}/{tk}|{tk}]]"
        if sector != "UNMAPPED"
        else f"`{tk}` ⚠️ sector-unmapped"
    )
    inbox_link = f"[[06-Inbox/{inbox_filename}|{title[:40]}]]"

    return (
        f"| {coverage_link} | {sector} | {inbox_link} | "
        f"{period} | {filing_date} | {quality_flag} | {short_ts} |"
    )


# ---------------------------------------------------------------- write operations

def _inbox_path(vault_root: Path, tk: str, period: str,
                filing_date: str) -> Path:
    return vault_root / INBOX_DIR_NAME / f"{tk}-filing-summary-{period}-{filing_date}.md"


def _coverage_path(vault_root: Path, sector: str, tk: str) -> Path:
    return vault_root / COVERAGE_DIR_NAME / sector / f"{tk}.md"


def _index_path(vault_root: Path) -> Path:
    return vault_root / COVERAGE_DIR_NAME / INDEX_FILE_NAME


def _existing_inbox_sha256(inbox_file: Path) -> str | None:
    """Read existing inbox file's source_sha256 from frontmatter, if managed."""
    try:
        text = inbox_file.read_text(encoding="utf-8")
    except OSError:
        return None
    if MANAGED_MARKER_LINE not in text:
        return None  # manual file — don't touch
    m = re.search(r'^source_sha256:\s*"?([a-f0-9]+)"?', text, re.MULTILINE)
    return m.group(1) if m else None


def _replace_marker_block(text: str, new_block: str,
                          begin: str = FILING_SUMMARY_BEGIN,
                          end: str = FILING_SUMMARY_END) -> str:
    """Replace content between begin/end markers. If markers missing,
    insert new block directly AFTER the `## Snapshot` section (or at
    end of body if no Snapshot section)."""
    pattern = re.compile(
        re.escape(begin) + r".*?" + re.escape(end),
        re.DOTALL,
    )
    if pattern.search(text):
        return pattern.sub(new_block, text, count=1)
    # No existing markers — insert AFTER ## Snapshot if present.
    snapshot_re = re.compile(r"^(##\s+Snapshot\s*$)", re.MULTILINE)
    m = snapshot_re.search(text)
    if m:
        # Find end of Snapshot section (next ## heading or EOF).
        rest = text[m.end():]
        next_h = re.search(r"^##\s+", rest, re.MULTILINE)
        insert_at = m.end() + (next_h.start() if next_h else len(rest))
        return text[:insert_at].rstrip() + "\n\n" + new_block + "\n\n" + text[insert_at:].lstrip("\n")
    # Fallback: insert at end of body (before final trailing whitespace).
    return text.rstrip() + "\n\n" + new_block + "\n"


def _upsert_index_row(index_text: str | None, ticker: str, sector: str,
                      new_row: str) -> str:
    """Update or insert row in 04-Coverage/_index.md.

    Creates the file with header + table if missing. If a row for
    `ticker` exists (matched by first column containing ticker), replace
    it. Otherwise insert in stable (Sector, Ticker) order within the
    sector group.
    """
    header = (
        "---\n"
        "title: Coverage Filing Summary Index\n"
        "source_type: ai-generated\n"
        "generated_by: is1-coverage-dashboard\n"
        "tags: [coverage, index, auto-maintained]\n"
        "---\n\n"
        "# Coverage Filing Summary Index\n\n"
        "> Auto-maintained by `vault_writer.py` — one row per ticker, "
        "latest filing only.\n\n"
        "| Ticker | Sector | Latest Filing | Period | Filing Date | Quality | Updated |\n"
        "|---|---|---|---|---|---|---|\n"
    )
    if index_text is None:
        return header + new_row + "\n"

    # Split header (frontmatter + table head) from body.
    lines = index_text.splitlines(keepends=True)
    header_end = 0
    in_table = False
    table_done = False
    for i, line in enumerate(lines):
        if not table_done and line.startswith("|---"):
            header_end = i + 1
            table_done = True
            break

    body_lines = lines[header_end:]
    # Find existing row for this ticker (column 0 contains the ticker).
    row_re = re.compile(r"^\|\s*(?:`?\[\[[^\]|]*\|[^\]]+\]\]`?|`[^`]+`|\[\[[^\]|]*\|[^\]]+\]\])\s*\|")
    # Use simpler heuristic: first column should contain `ticker`.
    row_re_simple = re.compile(rf"^\|[^|]*{re.escape(ticker)}[^|]*\|")

    existing_idx = None
    for i, line in enumerate(body_lines):
        if line.startswith("|") and ticker in line.split("|")[1]:
            existing_idx = i
            break

    if existing_idx is not None:
        body_lines[existing_idx] = new_row + "\n"
    else:
        # Insert in stable Sector, Ticker order within body.
        body_lines.append(new_row + "\n")
        body_lines.sort(
            key=lambda l: (
                l.split("|")[2].strip() if "|" in l else "ZZ",
                l.split("|")[1].strip() if "|" in l else ticker,
            )
        )

    return "".join(lines[:header_end]) + "".join(body_lines)


def _safe_write(path: Path, content: str, dry_run: bool,
                encoding: str = "utf-8") -> bool:
    """Write file atomically (tmp + rename). Returns True if written."""
    if dry_run:
        _log(f"DRY-RUN would write {len(content)} bytes to {path}")
        return True
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(content, encoding=encoding)
        tmp.replace(path)
        _log(f"wrote {len(content)} bytes to {path}")
        return True
    except OSError as e:
        _log(f"ERROR writing {path}: {e}")
        return False


# ---------------------------------------------------------------- main flow

def project_one(cache_entry: dict, filing: dict, vault_root: Path,
                dry_run: bool = False) -> dict:
    """Project one cache entry into all 3 vault locations.

    Returns a small report dict describing what was done (or skipped).

    Note: cache_entry may NOT contain `tk`/`title`/`meta` directly —
    the cache schema only stores bullets_th, model, pdf_sha256,
    tokens, ts. Filing metadata (ticker, sector, title, url) is
    resolved from the `filing` dict (which comes from
    disclosure-pulse.json via the data/ JSON) or from filename/heuristics.
    """
    # Resolve tk + title — cache key is filing ID, not ticker.
    tk = cache_entry.get("tk") or filing.get("tk") or "UNKNOWN"
    title = cache_entry.get("title") or filing.get("title") or filing.get("title_th") or ""
    if title == "" and "ts" in cache_entry:
        # Use filing_id-derived title fallback
        title = f"Filing {cache_entry.get('ts', '')[:10]}"
    period = _period_from_filing(filing, title)
    filing_date = _filing_date_iso(filing)
    sector = _sector_for_ticker(tk, filing)
    # Normalize cache_entry so renderers can use entry["tk"], entry["title"], entry["meta"]
    norm_entry = dict(cache_entry)
    norm_entry["tk"] = tk
    norm_entry["title"] = title
    # Synthesize meta from cache fields if not present
    if "meta" not in norm_entry:
        meta = {
            "source": "m3" if cache_entry.get("model") == "MiniMax-M3" else "unknown",
            "in_tokens": cache_entry.get("tokens", {}).get("in", 0),
            "out_tokens": cache_entry.get("tokens", {}).get("out", 0),
            "cost_usd": (cache_entry.get("tokens", {}).get("in", 0) / 1e6) * 3.0 +
                         (cache_entry.get("tokens", {}).get("out", 0) / 1e6) * 15.0,
            "document_count": 1,
        }
        norm_entry["meta"] = meta
    # Use ts as fetched_at fallback
    if "fetched_at" not in norm_entry:
        norm_entry["fetched_at"] = cache_entry.get("ts", _now_iso())
    # pdf_sha256 is the durable key
    source_sha256 = cache_entry.get("pdf_sha256", "") or _sha8(
        tk + period + filing_date + json.dumps(cache_entry.get("bullets_th", []),
                                               sort_keys=True))

    report: dict = {"tk": tk, "sector": sector, "period": period,
                    "filing_date": filing_date, "source_sha256": source_sha256,
                    "writes": {}, "skipped": []}

    # --- 1. Inbox canonical note ---
    inbox_filename, inbox_body = _render_inbox_note(
        norm_entry, source_sha256, filing)
    inbox_path = vault_root / INBOX_DIR_NAME / inbox_filename

    # Dedup: if existing inbox file has same sha256, skip.
    existing_sha = _existing_inbox_sha256(inbox_path)
    if existing_sha == source_sha256:
        report["skipped"].append(
            f"inbox: same source_sha256 already present at {inbox_path}")
    else:
        if existing_sha is None and inbox_path.exists():
            # Manual file — suffix filename to avoid clobbering.
            base = inbox_path.stem
            sha8 = source_sha256[:8]
            new_name = f"{base}-m3-{sha8}.md"
            _log(f"manual inbox file detected; using {new_name} instead")
            inbox_filename = new_name
            inbox_path = vault_root / INBOX_DIR_NAME / new_name
            _, inbox_body = _render_inbox_note(cache_entry, source_sha256,
                                               filing)
            report["writes"]["inbox_filename"] = inbox_filename

        wrote = _safe_write(inbox_path, inbox_body, dry_run=dry_run)
        report["writes"]["inbox"] = wrote

    # --- 2. Coverage note block (if ticker has sector folder + note) ---
    inbox_rel_link = f"06-Inbox/{inbox_filename}"
    coverage_path = _coverage_path(vault_root, sector, tk)
    block = _render_filing_summary_block(
        norm_entry, source_sha256, filing, inbox_rel_link)

    if sector == "UNMAPPED":
        report["skipped"].append("coverage: sector UNMAPPED, no folder")
    elif not coverage_path.exists():
        report["skipped"].append(
            f"coverage: no existing note at {coverage_path} — manual routing")
    else:
        try:
            text = coverage_path.read_text(encoding="utf-8")
        except OSError as e:
            report["skipped"].append(f"coverage: read error: {e}")
        else:
            new_text = _replace_marker_block(text, block)
            if not dry_run:
                try:
                    coverage_path.write_text(new_text, encoding="utf-8")
                    _log(f"updated marker block in {coverage_path}")
                    report["writes"]["coverage"] = True
                except OSError as e:
                    _log(f"ERROR writing coverage {coverage_path}: {e}")
                    report["writes"]["coverage"] = False
            else:
                _log(f"DRY-RUN would update marker block in {coverage_path}")
                report["writes"]["coverage"] = True

    # --- 3. Master index row ---
    index_path = _index_path(vault_root)
    row = _render_index_row(norm_entry, source_sha256, filing,
                            inbox_filename)
    try:
        existing = (None if not index_path.exists()
                    else index_path.read_text(encoding="utf-8"))
    except OSError as e:
        report["skipped"].append(f"index: read error: {e}")
        existing = None
    new_index = _upsert_index_row(existing, tk, sector, row)
    if not dry_run:
        wrote = _safe_write(index_path, new_index, dry_run=False)
        report["writes"]["index"] = wrote
    else:
        _log(f"DRY-RUN would write {len(new_index)} bytes to {index_path}")
        report["writes"]["index"] = True

    return report


def project_all(cache_path: Path = CACHE_DEFAULT,
                vault_root: Path = DEFAULT_VAULT_ROOT,
                dry_run: bool = False,
                ticker_filter: str | None = None,
                filings_lookup: dict | None = None) -> list[dict]:
    """Read cache and project all entries into the vault.

    `ticker_filter`: if set, only project that ticker (case-insensitive).
    `filings_lookup`: dict mapping filing_id → {tk, sector, title, ...}.
        If None, falls back to the cache's `filings` dict (which may
        be empty — in which case we try disclosure-pulse.json fallback).
    """
    if not cache_path.exists():
        _log(f"cache not found at {cache_path}")
        return []
    try:
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        _log(f"ERROR reading cache: {e}")
        return []

    summaries = cache.get("summaries", {})
    # Default: use explicit filings_lookup, then cache["filings"], then
    # fall back to disclosure-pulse.json if both are empty.
    filings = (filings_lookup if filings_lookup is not None
               else cache.get("filings", {}))
    if not (isinstance(filings, dict) and len(filings) > 0):
        pulse = _load_filings_lookup()
        if pulse:
            _log(f"using disclosure-pulse.json for filings metadata "
                 f"({len(pulse)} entries)")
            filings = pulse

    if not isinstance(summaries, dict):
        _log("cache summaries is not a dict — abort")
        return []

    reports = []
    for fid, entry in summaries.items():
        if not isinstance(entry, dict):
            continue
        tk = entry.get("tk") or filings.get(fid, {}).get("tk", "") if isinstance(filings, dict) else ""
        if ticker_filter and tk.upper() != ticker_filter.upper():
            continue
        filing = filings.get(fid, {}) if isinstance(filings, dict) else {}
        try:
            r = project_one(entry, filing, vault_root, dry_run=dry_run)
            reports.append(r)
        except Exception as e:
            _log(f"ERROR projecting {fid} ({tk}): {e}")
    return reports


# ---------------------------------------------------------------- CLI

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Project m3-enriched filing summaries into Obsidian vault.")
    p.add_argument("--cache", type=Path, default=CACHE_DEFAULT,
                   help="Path to filing_summary.json cache")
    p.add_argument("--vault-root", type=Path, default=DEFAULT_VAULT_ROOT,
                   help="Vault root (overrides OBSIDIAN_VAULT_ROOT env var)")
    p.add_argument("--ticker", metavar="TK", default=None,
                   help="Project only this ticker (case-insensitive)")
    p.add_argument("--dry-run", action="store_true",
                   help="Print what would be written without touching disk")
    p.add_argument("--show-output", metavar="TK", default=None,
                   help="Print the full body that would be written for this "
                        "ticker (uses current cache state)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)

    if args.show_output:
        # Diagnostic: print the would-be inbox body for one ticker.
        cache = json.loads(args.cache.read_text(encoding="utf-8"))
        target = args.show_output.upper()
        # Build filings lookup (cache may lack filings metadata).
        filings_lookup = cache.get("filings") or _load_filings_lookup()
        for fid, entry in cache.get("summaries", {}).items():
            # Resolve tk from entry OR filings_lookup (cache keys are
            # filing_ids, not tickers — see _load_filings_lookup).
            tk = entry.get("tk") or filings_lookup.get(fid, {}).get("tk", "")
            if tk.upper() != target:
                continue
            filing = filings_lookup.get(fid, {})
            title = entry.get("title") or filing.get("title") or ""
            period = _period_from_filing(filing, title)
            filing_date = _filing_date_iso(filing)
            sha = entry.get("pdf_sha256", "") or _sha8(
                tk + period + filing_date + json.dumps(
                    entry.get("bullets_th", []), sort_keys=True))
            # Normalize entry for renderer (project_one does this too).
            norm_entry = dict(entry)
            norm_entry["tk"] = tk
            norm_entry["title"] = title
            if "meta" not in norm_entry:
                norm_entry["meta"] = {
                    "source": "m3" if entry.get("model") == "MiniMax-M3"
                              else "unknown",
                    "in_tokens": entry.get("tokens", {}).get("in", 0),
                    "out_tokens": entry.get("tokens", {}).get("out", 0),
                    "cost_usd": (entry.get("tokens", {}).get("in", 0) / 1e6) * 3.0
                                 + (entry.get("tokens", {}).get("out", 0) / 1e6) * 15.0,
                    "document_count": 1,
                }
            fname, body = _render_inbox_note(norm_entry, sha, filing)
            print(f"\n=== {fname} ===\n")
            print(body)
            return 0
        print(f"ticker {args.show_output} not found in cache", file=sys.stderr)
        return 1

    reports = project_all(
        cache_path=args.cache,
        vault_root=args.vault_root,
        dry_run=args.dry_run,
        ticker_filter=args.ticker,
    )

    # Summary
    n = len(reports)
    n_inbox = sum(1 for r in reports if r["writes"].get("inbox"))
    n_cov = sum(1 for r in reports if r["writes"].get("coverage"))
    n_idx = sum(1 for r in reports if r["writes"].get("index"))
    n_skip = sum(len(r["skipped"]) for r in reports)
    _log(f"projected {n} filings: inbox={n_inbox} coverage={n_cov} "
         f"index={n_idx} skipped={n_skip}")

    if args.dry_run:
        _log("DRY-RUN — no files were modified")

    return 0


if __name__ == "__main__":
    sys.exit(main())