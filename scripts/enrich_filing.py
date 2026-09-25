"""Enrich a SET filing with an m3-powered Thai 3-4 bullet summary.

Reads a filing from `data/disclosure-pulse.json`, resolves the
newsdetails page, fetches the underlying PDF, sends the PDF +
a Thai-bullet prompt to m3 (MiniMax-M3, Anthropic Messages API
schema), and writes the result to a local cache.

Modes:
  --auto-alert          Scan disclosure-pulse.json for new high-severity
                        RM C filings, enrich each, post Discord embeds
  --watch-channel ID    Poll a Discord channel for "summarize <TK>"
                        messages, enrich and reply
  --enrich-id FILING_ID Enrich a single filing, print result to stdout
  --ticker TK           Same as --enrich-id but picks the latest filing
                        for a ticker (auto-pick the most recent)
  --dashboard           IS1-wide: enrich new Critical + Material filings
                        (financial statements skipped, MD&A kept), then
                        publish number-checked bullets to
                        data/filing-summaries.json for the dashboard

Stdlib-only (matches house style). Reuses the HTTP plumbing from
push_rm_c_digest.py — see _post_one for the 429 / 5xx / 4xx
handling discipline.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

# ---------------------------------------------------------------- constants

# Hermes data dir (this script lives in the repo but reads the same
# data/ JSONs the dashboard reads). The data/*.json files are
# committed to the repo and are the source of truth at runtime.
REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA_DIR = REPO_ROOT / "data"

# Cache location — gitignored (`~/.hermes/cache/filing_summary.json`).
# Falls back to repo-local if HOME isn't a hermes install.
CACHE_DEFAULT = Path.home() / ".hermes" / "cache" / "filing_summary.json"

# m3 endpoint + model (Anthropic Messages API, m3 is the user's
# default model per `~/.hermes/config.yaml`).
M3_BASE_URL = "https://api.minimax.io/anthropic"
M3_MODEL = "MiniMax-M3"
M3_MAX_TOKENS = 2000  # raised from 1000 — FS ZIPs with DOCX+XLSX+notes need ~1600 tokens of paraphrased output
M3_TIMEOUT_S = 120

# Filing cache TTL (entries older than this get re-enriched).
CACHE_TTL_DAYS = 30

# Prompt version — bump this to invalidate the cache after a
# prompt change (Codex-style kill switch for stale summaries).
PROMPT_VERSION = 1

# Discord webhook resolution: same env convention as
# build_daily_brief.py — env var first, secret file second. The
# secret file is named daily_brief.env historically (Phase 1/2 use
# it for the daily brief; auto-alert reuses the same channel).
DISCORD_WEBHOOK_ENV = "DISCORD_WEBHOOK_URL"
# Try the Phase 1/2 secret-file location first (most likely to exist
# since the user already wired the daily brief). Fall back to the
# auto-alert-specific name if needed.
DISCORD_SECRET_FILE_CANDIDATES = [
    Path.home() / ".hermes" / "secrets" / "discord_webhook.env",
    Path.home() / ".hermes" / "secrets" / "daily_brief.env",
]

# Auto-alert: max number of embeds per run (avoid flood on data
# backfill or vendor dump).
MAX_ALERTS_PER_RUN = 5

# Attachment safety limits. ZIPs stay in memory and are never extracted
# to disk; the count and expanded-size limits bound decompression.
MAX_ATTACHMENT_BYTES = 20_000_000
MAX_ZIP_EXPANDED_BYTES = 20_000_000
MAX_ZIP_MEMBERS = 50
# Maximum number of documents (PDF + extracted DOCX + extracted XLSX)
# that can be forwarded to m3 from a single ZIP. SET FS ZIPs typically
# have ≤ 4 members (auditor docx + FS xlsx + notes docx); 8 covers the
# largest issuers.
MAX_DOCUMENTS = 8
# Per-DOCX / per-XLSX text budget after extraction. Plain text is sent
# to m3 as a separate text block (not a base64 document), so the ceiling
# is on the assembled string, not the raw ZIP entry.
MAX_DOCX_TEXT_BYTES = 5 * 1024 * 1024
MAX_XLSX_TEXT_BYTES = 5 * 1024 * 1024
# Loop 4 v5: PDF text extraction via pypdf (no stdlib alternative).
MAX_PDF_TEXT_BYTES = 5 * 1024 * 1024
# Loop 4 v5: max raw_markdown stored per cache entry (text only, ~40KB/filing).
MAX_RAW_MARKDOWN_PER_DOC_BYTES = 2 * 1024 * 1024

# Severity filter for auto-alert.
AUTO_ALERT_SEVERITY = "high"

# RM identifier for RM C.
DEFAULT_RM = "C"

# System prompt — the rubric the model grades itself against.
# Keep this short and constraint-heavy. Long prompts dilute the
# model's adherence to specific formatting.
SYSTEM_PROMPT = (
    "You are an assistant for a Thai securities-firm relationship manager (RM). "
    "Reply in Thai only. Be concise. Use bullet format with `•` prefix. "
    "Every bullet MUST carry a specific number, date, or decision from the "
    "document — no vague lines. Output exactly 3-4 bullets covering:\n"
    "  • เหตุการณ์สำคัญ (what happened)\n"
    "  • ตัวเลข/วันที่/มติที่สำคัญ (key numbers, dates, decisions)\n"
    "  • ทำไม RM ควรสนใจ filing นี้ (why this matters to an RM)\n"
    "  • คำถาม follow-up ที่ควรถามบริษัท (one suggested follow-up question)\n"
    "Use ONLY what is in the document. If a category has no data, omit the "
    "bullet rather than guessing. Start with the first `•` — no preamble."
)

USER_PROMPT_TEMPLATE = (
    "สรุปเอกสาร SET filing ต่อไปนี้สำหรับ RM (relationship manager):\n\n"
    "FILING:\n"
    "- Ticker: {tk}\n"
    "- Title: {title}\n"
    "- Type: {type}\n"
    "- Severity: {severity}\n"
    "- TS: {ts}\n"
    "- URL: {url}\n\n"
    "PDF content attached as the document block. "
    "Reply in Thai only, 3-4 bullets, each carrying a concrete number/date/decision."
)


# Dashboard publishing (--dashboard). Scope agreed with the IS1 desk:
# every coverage ticker, Critical + Material only, financial statements
# skipped (the vault already carries FS notes), MD&A kept.
DASHBOARD_SEVERITIES = {"high", "medium"}   # pulse bands for critical / material
DASHBOARD_LIMIT = 30                        # new m3 calls per run; peak day is ~90
DASHBOARD_OUT = "filing-summaries.json"
DASHBOARD_MAX_ATTEMPTS = 3
_MDA_TITLE_RE = re.compile(
    r"management discussion|md\s*&\s*a|คำอธิบายและ(?:การ)?วิเคราะห์", re.I)
_NUM_RE = re.compile(r"\d[\d,]*(?:\.\d+)?")
_THAI_DIGITS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")


# Dashboard prompt: extraction, not analysis. v1 (the RM prompt above) asked
# "why should an RM care", which invited opinion the filing never states,
# and let the model compute figures that the number check then dropped
# (8 of 16 bullets in the first live run of 2026-09-25). Its own version tag
# keeps these entries apart from the Discord alert cache.
DASHBOARD_PROMPT_VERSION = "dash-3"
DASHBOARD_TEMPERATURE = 0.1
# dash-3 after the second live run (2026-09-25): opinion gone and nothing
# dropped, but "1.23 percent" came out as "1.23" (3 of 3 filings), dates
# stayed as 24-Sep-2026, names in English filings were transliterated into
# Thai (SYNTEC signatories, DAOL -> ดาว), signatory/phone/email bullets
# padded the list, and leasehold vs sublease was merged.
DASHBOARD_SYSTEM_PROMPT = (
    "You extract facts from a filing a company submitted to the Stock Exchange of "
    "Thailand, for an exchange analyst. Reply in Thai only. Output 2-4 bullets, each "
    "starting with `•`, and nothing else.\n"
    "Rules:\n"
    "1. State only facts written in the document. No opinion, interpretation, market "
    "impact, investor sentiment, recommendation, or any reason the document does not "
    "itself give.\n"
    "2. Copy every number exactly as the document writes it. Never calculate, convert "
    "units, round, annualise or compare figures; do not write YoY/QoQ changes unless "
    "the document states that exact figure.\n"
    "3. Always keep the unit next to its number: baht, million baht, shares, units, "
    "rai, sq.m., years. A percentage always ends with `%` (write 1.23 percent as "
    "1.23%). Never leave a bare number.\n"
    "4. Write every date as day, Thai month name, Buddhist-era year, e.g. "
    "24 กันยายน 2569 (24-Sep-2026 and 24 September 2026 both become 24 กันยายน 2569).\n"
    "5. Names of people, companies, funds, projects and places: copy them exactly as "
    "the document writes them, in the document's own script. If the document gives a "
    "name only in English, keep it in English; never transliterate or translate a "
    "name into Thai.\n"
    "6. Skip signatories, contact persons, phone numbers, e-mail and addresses.\n"
    "7. Do not merge items that the document distinguishes (for example leasehold, "
    "sub-lease and freehold assets, or different share classes); keep each "
    "difference.\n"
    "8. Cover, in this order: what the company announced; the key figures, dates or "
    "resolutions; conditions, next steps or effective dates the document states.\n"
    "9. Prefer the document's own Thai wording. If the document is in English, "
    "translate the prose faithfully into formal Thai. Write correct Thai spelling; "
    "when unsure of a word, use the document's wording instead.\n"
    "10. A short filing gets fewer bullets. Never pad."
)
DASHBOARD_USER_PROMPT_TEMPLATE = (
    "สรุปข้อเท็จจริงจากเอกสารที่บริษัทจดทะเบียนส่งตลาดหลักทรัพย์ต่อไปนี้\n\n"
    "- Ticker: {tk}\n"
    "- Title: {title}\n"
    "- Filed: {ts}\n\n"
    "เอกสารแนบอยู่ด้านบน ตอบเป็นภาษาไทย 2-4 bullet ใช้ตัวเลขตามเอกสารพร้อมหน่วยเสมอ "
    "(เปอร์เซ็นต์ใส่ %) วันที่เป็น วัน เดือนไทย ปี พ.ศ. ชื่อเฉพาะคงตามเอกสาร ห้ามคำนวณหรือแสดงความเห็น"
)


# ---------------------------------------------------------------- logging

def _log(msg: str) -> None:
    print(f"[enrich_filing] {msg}", flush=True)


# ---------------------------------------------------------------- cache

def _cache_path() -> Path:
    """Resolve cache file location, creating parent dirs as needed."""
    p = Path(os.environ.get("ENRICH_CACHE_PATH", str(CACHE_DEFAULT)))
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def _load_cache() -> dict:
    """Load cache, defensive against tampered/corrupt state.

    Codex P0 #2 lesson (from build_daily_brief): a top-level list or
    string in the state file would crash subsequent .get() calls. We
    return an empty dict for any non-dict payload.
    """
    p = _cache_path()
    if not p.exists():
        return {"version": 1, "prompt_version": PROMPT_VERSION, "summaries": {}}
    try:
        with p.open(encoding="utf-8") as fh:
            d = json.load(fh)
    except (json.JSONDecodeError, OSError) as e:
        _log(f"WARN: cache {p} corrupt: {e}; starting fresh")
        return {"version": 1, "prompt_version": PROMPT_VERSION, "summaries": {}}
    if not isinstance(d, dict):
        _log(f"WARN: cache {p} not a dict (got {type(d).__name__}); starting fresh")
        return {"version": 1, "prompt_version": PROMPT_VERSION, "summaries": {}}
    d.setdefault("version", 1)
    d.setdefault("prompt_version", PROMPT_VERSION)
    d.setdefault("summaries", {})
    # If prompt_version changed, drop all entries — re-enrich.
    if d.get("prompt_version") != PROMPT_VERSION:
        _log(f"cache prompt_version changed ({d.get('prompt_version')} -> "
             f"{PROMPT_VERSION}); clearing all cached summaries")
        d["prompt_version"] = PROMPT_VERSION
        d["summaries"] = {}
    return d


def _atomic_write_cache(d: dict) -> None:
    """tmp + rename, same pattern as push_rm_c_digest._atomic_write_json."""
    p = _cache_path()
    tmp = p.with_suffix(p.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2, sort_keys=True)
    os.replace(tmp, p)


def _cache_get(cache: dict, filing_id: str) -> dict | None:
    """Return cached entry if it exists and is within TTL, else None."""
    entry = cache.get("summaries", {}).get(filing_id)
    if not entry:
        return None
    try:
        ts = datetime.fromisoformat(entry.get("ts", "").replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None
    age = datetime.now(timezone.utc) - ts
    if age > timedelta(days=CACHE_TTL_DAYS):
        return None
    return entry


def _cache_put(cache: dict, filing_id: str, bullets: list[str],
              model: str, in_tokens: int, out_tokens: int,
              pdf_sha256: str,
              raw_markdown: dict | None = None,
              prompt_version: int | str = PROMPT_VERSION) -> None:
    entry: dict = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "bullets_th": bullets,
        "model": model,
        "tokens": {"in": in_tokens, "out": out_tokens},
        "pdf_sha256": pdf_sha256,
        "prompt_version": prompt_version,
    }
    if raw_markdown:
        entry["raw_markdown"] = raw_markdown
    cache["summaries"][filing_id] = entry


def _build_raw_markdown(attachment: bytes, attachment_url: str,
                       filing: dict) -> dict:
    """Build raw_markdown dict for cache from downloaded attachment.

    Handles three shapes:
      1. PDF attachment → 1 entry under 'MDA' (or doctype from filing.type)
      2. ZIP with DOCX/XLSX/PDF members → 1 entry per supported member
      3. ZIP with unknown members → 0 entries (fall through)

    Returns {doctype: {text, sha256, member_filename, raw_bytes_len,
                       extractor, extraction_status, page_count?, ...}}
    Empty dict if no extractable docs.
    """
    raw: dict = {}
    filing_id = filing.get("id") or filing.get("_id") or ""
    payload_sha = hashlib.sha256(attachment).hexdigest()
    if attachment.startswith(b"%PDF-"):
        doctype = _classify_doctype(attachment_url.rsplit("/", 1)[-1] or "MDA",
                                    filing)
        text = _extract_pdf_text(attachment)
        if text:
            raw[doctype] = {
                "text": text[:MAX_RAW_MARKDOWN_PER_DOC_BYTES],
                "sha256": payload_sha,
                "member_filename": attachment_url.rsplit("/", 1)[-1] or "MDA.pdf",
                "raw_bytes_len": len(attachment),
                "extractor": "pypdf-v1",
                "extraction_status": "ok",
                "page_count": _safe_pdf_pages(attachment),
            }
        return raw
    if not attachment.startswith(b"PK\x03\x04"):
        return raw
    try:
        with zipfile.ZipFile(io.BytesIO(attachment)) as archive:
            members = [info for info in archive.infolist() if not info.is_dir()]
            for info in members:
                name = info.filename
                lower = name.lower()
                with archive.open(info) as m:
                    raw_bytes = m.read()
                doctype = _classify_doctype(name, filing)
                text = ""
                extractor = ""
                if lower.endswith(".pdf"):
                    text = _extract_pdf_text(raw_bytes) or ""
                    extractor = "pypdf-v1"
                elif lower.endswith(".docx"):
                    text = _extract_docx_text(raw_bytes) or ""
                    extractor = "stdlib-docx-v1"
                elif lower.endswith(".xlsx"):
                    text = _extract_xlsx_text(raw_bytes) or ""
                    extractor = "stdlib-xlsx-v1"
                if not text:
                    continue
                raw[doctype] = {
                    "text": text[:MAX_RAW_MARKDOWN_PER_DOC_BYTES],
                    "sha256": hashlib.sha256(raw_bytes).hexdigest(),
                    "member_filename": name,
                    "raw_bytes_len": len(raw_bytes),
                    "extractor": extractor,
                    "extraction_status": "ok",
                }
    except (zipfile.BadZipFile, OSError) as e:
        _log(f"raw_markdown ZIP parse failed: {e}")
    return raw


def _safe_pdf_pages(attachment: bytes) -> int:
    try:
        from pypdf import PdfReader
        return len(PdfReader(io.BytesIO(attachment)).pages)
    except Exception:
        return 0


# ---------------------------------------------------------------- data loading

def _load_pulse(data_dir: Path) -> dict:
    """Load the deployed disclosure-pulse.json from local data/."""
    p = data_dir / "disclosure-pulse.json"
    if not p.exists():
        return {"filings": []}
    with p.open(encoding="utf-8") as fh:
        return json.load(fh)


def _load_tickers(data_dir: Path, rm_key: str = DEFAULT_RM) -> set[str]:
    p = data_dir / "tickers.json"
    if not p.exists():
        return set()
    with p.open(encoding="utf-8") as fh:
        d = json.load(fh)
    return {t["tk"] for t in (d.get("tickers") or []) if t.get("rm") == rm_key}


def _find_filing(pulse: dict, *, ticker: str | None = None,
                 filing_id: str | None = None) -> dict | None:
    """Find a single filing. filing_id wins; otherwise latest for ticker."""
    filings = pulse.get("filings") or []
    if filing_id:
        for f in filings:
            if str(f.get("_id")) == str(filing_id):
                return f
        return None
    if ticker:
        cands = [f for f in filings if f.get("tk") == ticker]
        if not cands:
            return None
        cands.sort(key=lambda f: f.get("ts") or "", reverse=True)
        return cands[0]
    return None


# ---------------------------------------------------------------- HTTP

def _fetch(url: str, headers: dict | None = None,
          timeout: int = 30) -> tuple[bytes, dict]:
    h = {"User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0 Safari/537.36")}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), dict(r.headers)


# Regex lifted from worker.js; matches the weblink.set.or.th PDF or ZIP
# URL inside the newsdetails HTML page. SET FS ZIPs contain Office
# documents (DOCX/XLSX) instead of PDFs, so we must support both.
_PDF_URL_RE = re.compile(rb"https?://weblink\.set\.or\.th/[^\"'<> ]+\.(?:pdf|zip)",
                         re.IGNORECASE)


def _resolve_pdf_url(news_url: str) -> str | None:
    """Fetch newsdetails page, extract weblink PDF/ZIP URL via regex."""
    try:
        html, _ = _fetch(news_url, headers={
            "Referer": "https://www.set.or.th/en/market/news-and-alert/news",
            "Accept": "text/html",
        })
    except (urllib.error.URLError, TimeoutError) as e:
        _log(f"newsdetails fetch failed: {e}")
        return None
    m = _PDF_URL_RE.search(html)
    return m.group(0).decode("ascii") if m else None


def _fetch_attachment(attachment_url: str, referer: str) -> bytes | None:
    """Fetch the underlying PDF or ZIP attachment.

    Validates by magic bytes (``%PDF-`` or ``PK\x03\x04``) — Content-Type
    is unreliable because weblink.set.or.th serves PDFs/ZIPs as
    application/octet-stream. Size capped at ``MAX_ATTACHMENT_BYTES``.
    """
    try:
        body, _ = _fetch(attachment_url, headers={
            "Referer": referer,
            "Accept": "application/pdf,application/zip,*/*",
        })
    except (urllib.error.URLError, TimeoutError) as e:
        _log(f"attachment fetch failed: {e}")
        return None
    if not (body.startswith(b"%PDF-") or body.startswith(b"PK\x03\x04")):
        _log(f"attachment returned {len(body)} bytes; first 5: {body[:5]!r} — likely Incapsula")
        return None
    if len(body) > MAX_ATTACHMENT_BYTES:
        _log(f"attachment too large: {len(body)} bytes")
        return None
    return body


# Backwards-compatible alias. Pre-Phase-3 tests still patch the old name.
_fetch_pdf = _fetch_attachment


# ---------------------------------------------------------------- DOCX / XLSX extraction

def _extract_docx_text(payload: bytes) -> str | None:
    """Extract plain text from a DOCX (Office Open XML) byte payload.

    DOCX is a ZIP archive whose main content lives in word/document.xml.
    We walk every <w:t> element and join the runs with spaces — that is
    enough for m3 to paraphrase the auditor report and notes. Stdlib only.
    """
    from xml.etree import ElementTree as ET
    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            xml_bytes = archive.read("word/document.xml", MAX_DOCX_TEXT_BYTES + 1)
    except (zipfile.BadZipFile, zipfile.LargeZipFile, RuntimeError,
            OSError, NotImplementedError, ValueError, KeyError) as e:
        _log(f"DOCX rejected: {e}")
        return None
    if len(xml_bytes) > MAX_DOCX_TEXT_BYTES:
        _log(f"DOCX document.xml exceeds {MAX_DOCX_TEXT_BYTES} bytes")
        return None
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        _log(f"DOCX XML parse error: {e}")
        return None
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    parts: list[str] = []
    for elem in root.iter(f"{ns}t"):
        if elem.text:
            parts.append(elem.text.strip())
    text = " ".join(p for p in parts if p)
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        _log("DOCX yielded no text")
        return None
    if len(text.encode("utf-8")) > MAX_DOCX_TEXT_BYTES:
        _log(f"DOCX text exceeds {MAX_DOCX_TEXT_BYTES} bytes after extraction")
        return None
    return text


def _extract_xlsx_text(payload: bytes) -> str | None:
    """Extract plain text from an XLSX (Office Open XML) byte payload.

    XLSX is a ZIP archive containing xl/sharedStrings.xml and one
    xl/worksheets/sheetN.xml per sheet. We resolve shared-string indices
    and emit each sheet as a row of tab-separated cells, blank lines
    between sheets. Stdlib only.
    """
    from xml.etree import ElementTree as ET
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            shared: list[str] = []
            try:
                ss_xml = archive.read("xl/sharedStrings.xml",
                                       MAX_XLSX_TEXT_BYTES + 1)
                ss_root = ET.fromstring(ss_xml)
                for si in ss_root.findall(f"{ns}si"):
                    parts = [t.text or "" for t in si.iter(f"{ns}t")]
                    shared.append("".join(parts).strip())
            except KeyError:
                shared = []
            except ET.ParseError as e:
                _log(f"XLSX sharedStrings parse error: {e}")
                return None

            sheet_names = sorted(
                name for name in archive.namelist()
                if name.startswith("xl/worksheets/sheet")
                and name.endswith(".xml"))
            if not sheet_names:
                _log("XLSX has no worksheets")
                return None

            output_parts: list[str] = []
            for sheet_path in sheet_names:
                try:
                    sheet_xml = archive.read(sheet_path,
                                              MAX_XLSX_TEXT_BYTES + 1)
                except (KeyError, OSError):
                    continue
                if len(sheet_xml) > MAX_XLSX_TEXT_BYTES:
                    _log(f"XLSX sheet too large: {sheet_path}")
                    return None
                try:
                    sheet_root = ET.fromstring(sheet_xml)
                except ET.ParseError:
                    continue
                row_count = 0
                sheet_lines: list[str] = []
                for row in sheet_root.iter(f"{ns}row"):
                    cells: list[str] = []
                    for c in row.findall(f"{ns}c"):
                        t_attr = c.get("t")
                        v_elem = c.find(f"{ns}v")
                        inline = c.find(f"{ns}is")
                        raw_value: str = ""
                        if v_elem is not None and v_elem.text is not None:
                            raw_value = v_elem.text
                        elif inline is not None:
                            parts = [tt.text or "" for tt in inline.iter(f"{ns}t")]
                            raw_value = "".join(parts)
                        if t_attr == "s":
                            try:
                                cells.append(shared[int(raw_value)])
                            except (ValueError, IndexError):
                                cells.append(raw_value)
                        elif t_attr == "inlineStr" or t_attr == "str":
                            cells.append(raw_value)
                        else:
                            cells.append(raw_value)
                    line = "\t".join(cells).rstrip()
                    if line:
                        sheet_lines.append(line)
                        row_count += 1
                if row_count:
                    output_parts.append(
                        f"[{sheet_path}]\n" + "\n".join(sheet_lines))
            text = "\n\n".join(output_parts).strip()
            if not text:
                _log("XLSX yielded no text")
                return None
            if len(text.encode("utf-8")) > MAX_XLSX_TEXT_BYTES:
                _log(f"XLSX text exceeds {MAX_XLSX_TEXT_BYTES} bytes after extraction")
                return None
            return text
    except (zipfile.BadZipFile, zipfile.LargeZipFile, RuntimeError,
            OSError, NotImplementedError, ValueError) as e:
        _log(f"XLSX rejected: {e}")
        return None


def _extract_pdf_text(payload: bytes) -> str | None:
    """Extract plain text from a PDF byte payload via pypdf.

    Scanned PDFs (image-only) return empty string → caller marks
    extraction_status="no_text". Failures return None and the caller
    falls back to bytes-only m3 path.
    """
    try:
        from pypdf import PdfReader
    except ImportError:
        _log("pypdf not installed; PDF text extraction skipped")
        return None
    try:
        reader = PdfReader(io.BytesIO(payload))
    except Exception as e:
        _log(f"PDF rejected: {e}")
        return None
    parts: list[str] = []
    for page in reader.pages:
        try:
            t = page.extract_text() or ""
        except Exception as e:
            _log(f"PDF page extract error: {e}")
            t = ""
        if t:
            parts.append(t)
    text = "\n\n".join(parts)
    if not text.strip():
        return None  # scanned PDF or empty
    if len(text.encode("utf-8")) > MAX_PDF_TEXT_BYTES:
        _log(f"PDF text exceeds {MAX_PDF_TEXT_BYTES} bytes after extraction")
        return None
    return text


# Loop 4 v5: doctype classification for raw markdown files.
# Precedence matters — "NOTES_TO_FINANCIAL_STATEMENTS.docx" must be
# classified as NOTES, not FS. FS only matches as a complete token.
_DOCTYPE_KEYWORDS: list[tuple[str, tuple[str, ...]]] = [
    ("AUDITOR", ("auditor", "ผู้สอบบัญชี", "รายงานผู้สอบบัญชี")),
    ("NOTES",   ("note", "notes", "หมายเหตุ")),
    ("MDA",     ("mda", "md&a", "คำอธิบายและวิเคราะห์",
                 "การวิเคราะห์และคำอธิบาย")),
    ("FS",      ("financial_statement", "financialstatements",
                 "financial statements", "financial-statement",
                 "financial-statement", "งบการเงิน")),
]
_DOCTYPE_BY_FILING_TYPE = {
    "financial_statement": "FS",
    "audit":               "AUDITOR",
    "earnings":            "MDA",
    "management_discussion": "MDA",
    "notes":               "NOTES",
    "financial_statements_and_notes": "NOTES",
}
_VALID_DOCTYPES = {"MDA", "AUDITOR", "FS", "NOTES"}


def _classify_doctype(member_filename: str, filing: dict) -> str:
    """Classify a ZIP member or PDF attachment into MDA/AUDITOR/FS/NOTES.

    Filename match wins (highest precedence) — handles Thai + English
    SET conventions. Falls back to filing_type from disclosure-pulse.
    Returns 'NOTES' as safe default if nothing matches (least destructive
    placement = FS-NOTES folder is the largest bucket).
    """
    name = (member_filename or "").casefold()
    # Normalize: drop extension, replace - with space, collapse whitespace,
    # **keep underscores** so "financial_statement" stays as one token.
    stem = re.sub(r"\.(docx?|xlsx?|pdf)$", "", name, flags=re.IGNORECASE)
    stem_space = re.sub(r"[\s\-]+", " ", stem).strip()
    # Two parallel forms: with spaces and with underscores, so we match
    # both "financial statement" and "financial_statement" naming.
    tokens = set(stem_space.split())
    for doctype, kws in _DOCTYPE_KEYWORDS:
        for kw in kws:
            k = kw.replace("_", " ")
            # The keyword and stem may have either form (underscored
            # or space-separated). Test against both.
            if (k in tokens
                    or kw in tokens
                    or k in stem_space
                    or kw in stem_space):
                return doctype
    ft = (filing.get("type") or filing.get("filing_type") or "").strip().lower()
    if ft in _DOCTYPE_BY_FILING_TYPE:
        return _DOCTYPE_BY_FILING_TYPE[ft]
    return "NOTES"  # safe default


def _documents_from_payload(payload: bytes) -> list[bytes | str] | None:
    """Resolve a PDF or ZIP payload into m3-ready documents.

    Mixed-type result: PDF bytes stay as ``bytes`` (uploaded to m3 as
    ``application/pdf`` documents); DOCX/XLSX entries are extracted to
    plain text strings (sent to m3 as ``text`` blocks). The caller
    branches on element type.
    """
    if payload.startswith(b"%PDF-"):
        # Loop 4 v5: prefer text extraction (smaller m3 payload, also
        # feeds raw_markdown persistence). Fall back to bytes if pypdf
        # is missing or PDF is scanned/empty.
        text = _extract_pdf_text(payload)
        if text:
            return [text]
        return [payload]
    if not payload.startswith(b"PK\x03\x04"):
        return None
    try:
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            members = [info for info in archive.infolist() if not info.is_dir()]
            if not members:
                _log("ZIP is empty")
                return None
            if len(members) > MAX_ZIP_MEMBERS:
                _log(f"ZIP has too many members: {len(members)}")
                return None
            if any(info.flag_bits & 0x1 for info in members):
                _log("ZIP contains encrypted members")
                return None
            expanded = sum(info.file_size for info in members)
            if expanded > MAX_ZIP_EXPANDED_BYTES:
                _log(f"ZIP expanded size too large: {expanded} bytes")
                return None

            documents: list[bytes | str] = []
            for info in members:
                name = info.filename.lower()
                with archive.open(info) as member:
                    raw = member.read()
                if name.endswith(".pdf"):
                    if not raw.startswith(b"%PDF-"):
                        _log(f"ZIP member {info.filename} has no PDF magic; skipped")
                        continue
                    if len(raw) > MAX_ZIP_EXPANDED_BYTES:
                        _log(f"ZIP PDF member too large: {info.filename}")
                        return None
                    documents.append(raw)
                elif name.endswith(".docx"):
                    text = _extract_docx_text(raw)
                    if text:
                        documents.append(text)
                elif name.endswith(".xlsx"):
                    text = _extract_xlsx_text(raw)
                    if text:
                        documents.append(text)
                # ignore other members (.txt, .rels, [Content_Types].xml, etc.)
                if len(documents) >= MAX_DOCUMENTS:
                    _log(f"ZIP yielded too many documents: {len(documents)}")
                    return None
            if not documents:
                _log("ZIP contains no PDF/DOCX/XLSX documents")
                return None
            return documents
    except (zipfile.BadZipFile, zipfile.LargeZipFile, RuntimeError,
            OSError, NotImplementedError, ValueError) as e:
        _log(f"ZIP rejected: {e}")
        return None


# ---------------------------------------------------------------- m3

def _load_api_key() -> str | None:
    """Resolve m3 API key: env first, then Hermes's .env file."""
    k = os.environ.get("MINIMAX_API_KEY", "").strip()
    if k:
        return k
    env_path = Path.home() / "AppData" / "Local" / "hermes" / ".env"
    if not env_path.exists():
        return None
    try:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                k_, v = line.split("=", 1)
                if k_.strip() == "MINIMAX_API_KEY":
                    return v.strip().strip('"').strip("'")
    except OSError:
        pass
    return None


def _call_m3(documents: list[bytes | str] | bytes | str,
             filing: dict, *, system: str = SYSTEM_PROMPT,
             user_template: str = USER_PROMPT_TEMPLATE,
             temperature: float | None = None) -> tuple[list[str] | None, dict]:
    """Call m3 with PDF bytes and/or extracted text blocks.

    Accepts mixed input:
      * ``bytes`` — uploaded as ``application/pdf`` document block
      * ``str``   — sent as a ``text`` block (extracted DOCX/XLSX content)
    Falls back to None on any failure (caller uses _summary_th).
    """
    api_key = _load_api_key()
    if not api_key:
        _log("MINIMAX_API_KEY not set")
        return None, {}
    if isinstance(documents, (bytes, bytearray, str)):
        documents = [documents]
    user = user_template.format(
        tk=filing.get("tk", "?"),
        title=filing.get("title") or filing.get("title_th") or "?",
        type=filing.get("type", "?"),
        severity=filing.get("severity", "?"),
        ts=filing.get("ts", "?"),
        url=filing.get("url", "?"),
    )
    content = []
    for doc in documents:
        if isinstance(doc, (bytes, bytearray)):
            b64 = base64.standard_b64encode(doc).decode("ascii")
            content.append({
                "type": "document",
                "source": {"type": "base64",
                           "media_type": "application/pdf",
                           "data": b64},
            })
        elif isinstance(doc, str):
            content.append({"type": "text", "text": doc})
    content.append({"type": "text", "text": user})
    body = {
        "model": M3_MODEL,
        "max_tokens": M3_MAX_TOKENS,
        "system": system,
        "messages": [{"role": "user", "content": content}],
    }
    if temperature is not None:
        body["temperature"] = temperature
    req = urllib.request.Request(
        f"{M3_BASE_URL}/v1/messages",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=M3_TIMEOUT_S) as r:
            data = json.loads(r.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        _log(f"m3 call failed: {e}")
        return None, {}
    except urllib.error.HTTPError as e:
        try:
            body_preview = e.read(500).decode("utf-8", "replace")
        except Exception:
            body_preview = ""
        _log(f"m3 HTTP {e.code}: {body_preview[:200]}")
        return None, {}

    text = "".join(c.get("text", "") for c in data.get("content", [])
                  if c.get("type") == "text")
    if not text.strip():
        return None, data.get("usage", {})

    # Parse bullets — split on newlines, keep lines starting with •
    bullets = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("•") or line.startswith("- ") or line.startswith("* "):
            # Normalize to •
            content = line.lstrip("•-* ").strip()
            if content:
                bullets.append(f"• {content}")
    if not bullets:
        # Fallback: take whole text as one bullet
        bullets = [f"• {text.strip()[:1000]}"]
    return bullets, data.get("usage", {})


# ---------------------------------------------------------------- bullet rendering fallback

def _fallback_bullets(filing: dict) -> list[str]:
    """No PDF or no m3 — produce best-effort bullets from pre-summary."""
    th = (filing.get("_summary_th") or "").strip()
    en = (filing.get("_summary") or "").strip()
    title = (filing.get("title") or filing.get("title_th") or "").strip()
    bullets = []
    if title:
        bullets.append(f"• {title[:240]}")
    if th:
        bullets.append(f"• {th[:240]}")
    elif en:
        bullets.append(f"• {en[:240]}")
    bullets.append("• ⚠️ AI enrichment failed — figures from pre-summary only")
    return bullets[:3]


# ---------------------------------------------------------------- core: enrich one filing

def _enrich_one(filing: dict, *, force: bool = False,
                dashboard: bool = False) -> tuple[list[str], dict]:
    """Return (bullets, meta) for a single filing. Reads/writes cache.

    Always returns SOMETHING — falls back to _summary_th if PDF or
    m3 fails. Meta has: source, in_tokens, out_tokens, cost_usd,
    cache_hit, errors.
    """
    fid = str(filing.get("_id") or "")
    if not fid:
        return _fallback_bullets(filing), {
            "source": "fallback", "in_tokens": 0, "out_tokens": 0,
            "cost_usd": 0.0, "cache_hit": False, "errors": ["no _id"],
        }
    cache = _load_cache()
    if not force:
        hit = _cache_get(cache, fid)
        if hit is not None and dashboard and hit.get("prompt_version") != DASHBOARD_PROMPT_VERSION:
            hit = None
        if hit is not None:
            return hit.get("bullets_th") or _fallback_bullets(filing), {
                "source": "cache",
                "in_tokens": hit.get("tokens", {}).get("in", 0),
                "out_tokens": hit.get("tokens", {}).get("out", 0),
                "cost_usd": 0.0,
                "cache_hit": True,
                "errors": [],
            }

    news_url = filing.get("url", "")
    if not news_url:
        return _fallback_bullets(filing), {
            "source": "fallback", "in_tokens": 0, "out_tokens": 0,
            "cost_usd": 0.0, "cache_hit": False, "errors": ["no url"],
        }

    pdf_url = _resolve_pdf_url(news_url)
    if not pdf_url:
        return _fallback_bullets(filing), {
            "source": "fallback_no_pdf_url", "in_tokens": 0, "out_tokens": 0,
            "cost_usd": 0.0, "cache_hit": False, "errors": ["no_pdf_url_in_page"],
        }

    attachment = _fetch_pdf(pdf_url, referer=news_url)
    if attachment is None:
        return _fallback_bullets(filing), {
            "source": "fallback_pdf_fetch", "in_tokens": 0, "out_tokens": 0,
            "cost_usd": 0.0, "cache_hit": False, "errors": ["pdf_fetch_failed"],
        }

    documents = _documents_from_payload(attachment)
    if documents is None:
        return _fallback_bullets(filing), {
            "source": "fallback_pdf_fetch", "in_tokens": 0, "out_tokens": 0,
            "cost_usd": 0.0, "cache_hit": False, "errors": ["no_supported_documents"],
        }

    payload_sha = hashlib.sha256(attachment).hexdigest()
    document_count = len(documents)

    if dashboard:
        bullets, usage = _call_m3(documents, filing, system=DASHBOARD_SYSTEM_PROMPT,
                                  user_template=DASHBOARD_USER_PROMPT_TEMPLATE,
                                  temperature=DASHBOARD_TEMPERATURE)
    else:
        bullets, usage = _call_m3(documents, filing)
    if bullets is None:
        return _fallback_bullets(filing), {
            "source": "fallback_m3_failed", "in_tokens": 0, "out_tokens": 0,
            "cost_usd": 0.0, "cache_hit": False, "errors": ["m3_failed"],
        }

    in_tok = usage.get("input_tokens", 0)
    out_tok = usage.get("output_tokens", 0)
    cost = (in_tok / 1e6) * 3.0 + (out_tok / 1e6) * 15.0

    # Loop 4 v5: build raw_markdown from the same attachment bytes we
    # already downloaded. Text only (no binary), ~40KB/filing — safe to
    # store in cache. vault_raw_writer.py reads this on next cron tick
    # even if the live vault write failed here.
    attachment_url = pdf_url  # already resolved above
    raw_markdown = _build_raw_markdown(attachment, attachment_url, filing)

    # Persist to cache atomically.
    try:
        cache = _load_cache()  # re-read in case of races
        _cache_put(cache, fid, bullets, M3_MODEL, in_tok, out_tok,
                   payload_sha, raw_markdown=raw_markdown,
                   prompt_version=DASHBOARD_PROMPT_VERSION if dashboard else PROMPT_VERSION)
        _atomic_write_cache(cache)
    except OSError as e:
        _log(f"WARN: cache write failed: {e}")

    return bullets, {
        "source": "m3",
        "in_tokens": in_tok,
        "out_tokens": out_tok,
        "cost_usd": cost,
        "cache_hit": False,
        "errors": [],
    }


# ---------------------------------------------------------------- Discord webhook

def _load_webhook() -> str | None:
    """Resolve Discord webhook: env first, then any candidate secret file."""
    v = os.environ.get(DISCORD_WEBHOOK_ENV, "").strip()
    if v:
        return v
    for secret_path in DISCORD_SECRET_FILE_CANDIDATES:
        if not secret_path.exists():
            continue
        try:
            for line in secret_path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    k, vv = line.split("=", 1)
                    if k.strip() == DISCORD_WEBHOOK_ENV:
                        return vv.strip().strip('"').strip("'")
        except OSError:
            pass
    return None


def _post_discord(url: str, payload: dict, *, dry_run: bool = False) -> bool:
    """Minimal Discord POST. Reuses discipline from build_daily_brief._post_one
    but without the 429/5xx retry loop — auto-alert runs in CI context
    where the upstream GitHub Action will simply retry the whole job."""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    if dry_run:
        snippet = json.dumps(payload, ensure_ascii=False)[:400]
        _log(f"DRY_RUN: POST {len(body)}B: {snippet}{'…' if len(body) > 400 else ''}")
        return True
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json", "User-Agent": "IS1-enrich/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status in (200, 204)
    except urllib.error.HTTPError as e:
        _log(f"Discord HTTP {e.code}")
        return False
    except (urllib.error.URLError, TimeoutError) as e:
        _log(f"Discord URL error: {e}")
        return False


def _build_embed(filing: dict, bullets: list[str], meta: dict,
                 channel_kind: str) -> dict:
    """Build a Discord embed for one filing."""
    sev = (filing.get("severity") or "low").lower()
    color = {"high": 0xEF4444, "medium": 0xF59E0B, "low": 0x22C55E}.get(sev, 0x3B82F6)
    tk = filing.get("tk", "?")
    type_ = filing.get("type", "?")
    ts = (filing.get("ts") or "")[:16].replace("T", " ")
    url = filing.get("url", "")

    fields = []
    for i, b in enumerate(bullets, 1):
        # Field value limit = 1024; bullets are short, safe.
        fields.append({
            "name": f"• {i}",
            "value": b.lstrip("• ").strip()[:1024],
            "inline": False,
        })

    footer_parts = [f"{tk} · {type_} · {sev}"]
    if meta.get("source") == "cache":
        footer_parts.append("cached")
    elif meta.get("source", "").startswith("fallback"):
        footer_parts.append(f"⚠️ {meta['source']}")
    if meta.get("cost_usd"):
        footer_parts.append(f"${meta['cost_usd']:.4f}")

    title_prefix = "🤖" if channel_kind == "auto-alert" else "📝"
    return {
        "title": f"{title_prefix} {tk} · {type_} ({sev})",
        "url": url,
        "color": color,
        "description": f"**SET filing summary** — {ts}",
        "fields": fields,
        "footer": {"text": " · ".join(footer_parts)},
    }


# ---------------------------------------------------------------- modes

def _enrich_id(filing_id: str, *, force: bool = False,
               data_dir: Path) -> int:
    """Single-filing mode. Print bullets + meta to stdout, exit code."""
    pulse = _load_pulse(data_dir)
    filing = _find_filing(pulse, filing_id=filing_id)
    if not filing:
        print(f"filing_id={filing_id} not found in disclosure-pulse.json",
              file=sys.stderr)
        return 1
    bullets, meta = _enrich_one(filing, force=force)
    out = {
        "filing_id": filing.get("_id"),
        "tk": filing.get("tk"),
        "title": filing.get("title") or filing.get("title_th"),
        "bullets_th": bullets,
        "meta": meta,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


def _enrich_ticker(ticker: str, *, force: bool = False,
                   data_dir: Path) -> int:
    pulse = _load_pulse(data_dir)
    filing = _find_filing(pulse, ticker=ticker)
    if not filing:
        print(f"ticker={ticker} not found in disclosure-pulse.json", file=sys.stderr)
        return 1
    return _enrich_id(str(filing["_id"]), force=force, data_dir=data_dir)


def _auto_alert(data_dir: Path, *, dry_run: bool,
                webhook: str | None, limit: int = MAX_ALERTS_PER_RUN) -> int:
    """Scan disclosure-pulse for new (not in cache) high-severity RM C filings,
    enrich each, post to Discord."""
    pulse = _load_pulse(data_dir)
    rm_tickers = _load_tickers(data_dir)
    cache = _load_cache()
    seen = set(cache.get("summaries", {}).keys())

    candidates = []
    for f in pulse.get("filings") or []:
        if (f.get("severity") or "").lower() != AUTO_ALERT_SEVERITY:
            continue
        if rm_tickers and f.get("tk") not in rm_tickers:
            continue
        fid = str(f.get("_id") or "")
        if not fid or fid in seen:
            continue
        # Re-enrich if old, or first-time; force=True to overwrite cache
        candidates.append(f)

    if not candidates:
        _log(f"auto-alert: no new high-severity RM C filings")
        return 0

    # Sort by ts descending (newest first), cap at limit
    candidates.sort(key=lambda f: f.get("ts") or "", reverse=True)
    candidates = candidates[:limit]
    _log(f"auto-alert: enriching {len(candidates)} filing(s)")

    posted = 0
    for f in candidates:
        bullets, meta = _enrich_one(f, force=True)
        embed = _build_embed(f, bullets, meta, "auto-alert")
        payload = {
            "username": "IS1 Filing Summary",
            "embeds": [embed],
        }
        if webhook and _post_discord(webhook, payload, dry_run=dry_run):
            posted += 1
        elif dry_run:
            posted += 1
        else:
            _log(f"auto-alert: failed to post filing_id={f.get('_id')}")

    _log(f"auto-alert: posted {posted}/{len(candidates)}")
    return 0 if posted == len(candidates) else 1


# ---------------------------------------------------------------- dashboard

def _is_mda(filing: dict) -> bool:
    text = f"{filing.get('title') or ''} {filing.get('title_th') or ''}"
    return bool(_MDA_TITLE_RE.search(text))


def _dashboard_eligible(filing: dict) -> bool:
    """Critical/Material, any coverage ticker; earnings only when it is MD&A."""
    if (filing.get("severity") or "").lower() not in DASHBOARD_SEVERITIES:
        return False
    if not filing.get("_id") or not filing.get("url"):
        return False
    if (filing.get("type") or "") == "earnings" and not _is_mda(filing):
        return False
    return True


def _norm_numbers(text: str) -> str:
    """Thai digits to Arabic, drop thousands separators: '1,234.5' -> '1234.5'."""
    text = (text or "").translate(_THAI_DIGITS)
    return re.sub(r"(?<=\d),(?=\d{3})", "", text)


def _number_in_source(token: str, source: str) -> bool:
    tok = token.replace(",", "").rstrip(".")
    if not tok:
        return True
    if re.search(rf"(?<![\d.]){re.escape(tok)}(?![\d])", source):
        return True
    # A year may be written in BE by the model and AD in the filing, or back.
    if re.fullmatch(r"\d{4}", tok):
        n = int(tok)
        alt = n - 543 if n >= 2500 else n + 543 if 1900 <= n <= 2100 else None
        if alt and re.search(rf"(?<!\d){alt}(?!\d)", source):
            return True
    return False


def _verify_bullets(bullets: list[str], source_text: str) -> tuple[list[str], int]:
    """Keep only bullets whose every number appears in the source document.

    Deterministic guard for CLAUDE.md rule 1 (never invent data): a figure
    the model computed, converted or misread cannot be traced to the
    filing, so the whole bullet is dropped rather than shown.
    """
    source = _norm_numbers(source_text)
    kept, dropped = [], 0
    for b in bullets:
        text = b.lstrip("•-* ").strip()
        if not text or text.startswith("⚠"):
            dropped += 1
            continue
        tokens = _NUM_RE.findall(_norm_numbers(text))
        if all(_number_in_source(t, source) for t in tokens):
            kept.append(text)
        else:
            dropped += 1
    return kept, dropped


def _source_text(entry: dict) -> str:
    raw = entry.get("raw_markdown") or {}
    return "\n\n".join(str(v.get("text") or "") for v in raw.values() if isinstance(v, dict))


def _publish_dashboard(pulse: dict, cache: dict, out_path: Path) -> dict:
    """Write number-checked summaries for eligible filings still in the pulse window."""
    summaries: dict = {}
    held = {"unverifiable": 0, "all_dropped": 0}
    for f in pulse.get("filings") or []:
        if not _dashboard_eligible(f):
            continue
        fid = str(f.get("_id"))
        entry = (cache.get("summaries") or {}).get(fid)
        if not entry or not entry.get("bullets_th"):
            continue
        if entry.get("prompt_version") != DASHBOARD_PROMPT_VERSION:
            continue  # written by the RM alert prompt, which may carry opinion
        source = _source_text(entry)
        if not source.strip():
            # Scanned PDF: m3 read the image, but nothing we can check it against.
            held["unverifiable"] += 1
            continue
        kept, dropped = _verify_bullets(entry["bullets_th"], source)
        if not kept:
            held["all_dropped"] += 1
            continue
        docs = [v.get("member_filename") for v in (entry.get("raw_markdown") or {}).values()
                if isinstance(v, dict) and v.get("member_filename")]
        summaries[fid] = {
            "tk": f.get("tk"),
            "bullets": kept,
            "dropped": dropped,
            "generated": entry.get("ts"),
            "documents": docs[:3],
        }
    payload = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model": M3_MODEL,
        "promptVersion": DASHBOARD_PROMPT_VERSION,
        "scope": "IS1 coverage · critical + material · financial statements skipped, MD&A kept",
        "rule": "bullets whose numbers are not all found in the filing text are dropped",
        "total": len(summaries),
        "held": held,
        "summaries": summaries,
    }
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    os.replace(tmp, out_path)
    return payload


def _dashboard(data_dir: Path, *, limit: int, dry_run: bool) -> int:
    """Enrich up to `limit` new eligible filings (newest first), then publish."""
    pulse = _load_pulse(data_dir)
    cache = _load_cache()
    failures = cache.get("dashboard_failures") or {}

    def backing_off(fid: str) -> bool:
        # A filing with no PDF link or a dead attachment would otherwise eat a
        # slot every run: wait a day between attempts and stop after three.
        rec = failures.get(fid) or {}
        if rec.get("attempts", 0) >= DASHBOARD_MAX_ATTEMPTS:
            return True
        try:
            last = datetime.fromisoformat(str(rec.get("last", "")).replace("Z", "+00:00"))
        except ValueError:
            return False
        return datetime.now(timezone.utc) - last < timedelta(hours=24)

    # Any cached summary counts as done, however old: the pulse window is 90
    # days and the cache TTL 30, so a TTL check here would pay m3 again for
    # every filing aged 31-90 days on each run.
    done = {fid for fid, entry in (cache.get("summaries") or {}).items()
            if entry.get("prompt_version") == DASHBOARD_PROMPT_VERSION}
    todo = [f for f in pulse.get("filings") or []
            if _dashboard_eligible(f) and str(f["_id"]) not in done
            and not backing_off(str(f["_id"]))]
    todo.sort(key=lambda f: f.get("ts") or "", reverse=True)
    _log(f"dashboard: {len(todo)} eligible filing(s) without a summary; enriching up to {limit}")
    ok = failed = 0
    for f in todo[:limit]:
        if dry_run:
            _log(f"DRY_RUN would enrich {f.get('tk')} {f.get('_id')} {f.get('title', '')[:60]}")
            continue
        _bullets, meta = _enrich_one(f, dashboard=True)
        if meta.get("source") == "m3":
            ok += 1
        else:
            failed += 1
            _log(f"dashboard: {f.get('tk')} {f.get('_id')} -> {meta.get('source')}")
            rec = failures.setdefault(str(f["_id"]), {"attempts": 0})
            rec["attempts"] = rec.get("attempts", 0) + 1
            rec["last"] = datetime.now(timezone.utc).isoformat()
            rec["reason"] = meta.get("source")
    if failed and not dry_run:
        latest = _load_cache()
        latest["dashboard_failures"] = failures
        _atomic_write_cache(latest)
    if dry_run:
        return 0
    payload = _publish_dashboard(pulse, _load_cache(), data_dir / DASHBOARD_OUT)
    _log(f"dashboard: enriched {ok}, failed {failed}; published {payload['total']} "
         f"(held: {payload['held']})")
    return 0


def _audit(data_dir: Path, *, count: int) -> int:
    """Print published bullets beside the source passage for each number.

    For the human spot-check before a publish: every figure should read the
    same in the bullet and in the quoted filing text.
    """
    out_path = data_dir / DASHBOARD_OUT
    if not out_path.exists():
        print(f"{out_path} not found — run --dashboard first", file=sys.stderr)
        return 1
    published = json.loads(out_path.read_text(encoding="utf-8")).get("summaries") or {}
    cache = _load_cache()
    pulse = {str(f.get("_id")): f for f in _load_pulse(data_dir).get("filings") or []}
    for fid, item in list(published.items())[:count]:
        f = pulse.get(fid, {})
        source = _norm_numbers(_source_text((cache.get("summaries") or {}).get(fid) or {}))
        print(f"\n=== {item.get('tk')} · {fid} · {f.get('title_th') or f.get('title') or ''}")
        print(f"    {f.get('url_th') or f.get('url') or ''}")
        for b in item.get("bullets") or []:
            print(f"  • {b}")
            for tok in dict.fromkeys(_NUM_RE.findall(_norm_numbers(b))):
                t = tok.replace(",", "").rstrip(".")
                m = re.search(rf"(?<![\d.]){re.escape(t)}(?![\d])", source)
                ctx = source[max(0, m.start() - 60):m.end() + 60].replace("\n", " ") if m else "(BE/AD year match)"
                print(f"      {tok:>14}  …{ctx}…")
        if item.get("dropped"):
            print(f"  ({item['dropped']} bullet(s) dropped by the number check)")
    # Token use of every dashboard-prompt call so far, to price the backlog.
    dash = [v for v in (cache.get("summaries") or {}).values()
            if v.get("prompt_version") == DASHBOARD_PROMPT_VERSION]
    if dash:
        tin = sum((v.get("tokens") or {}).get("in", 0) for v in dash)
        tout = sum((v.get("tokens") or {}).get("out", 0) for v in dash)
        print(f"\ntokens over {len(dash)} dashboard call(s): in {tin:,} / out {tout:,} "
              f"(avg in {tin // len(dash):,} / out {tout // len(dash):,} per filing)")
    return 0


# ---------------------------------------------------------------- CLI

def _build_argparser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Enrich SET filings with m3-powered Thai bullet summaries.")
    p.add_argument("--auto-alert", action="store_true",
                   help="Scan disclosure-pulse for new high-severity RM C filings")
    p.add_argument("--enrich-id", metavar="FILING_ID",
                   help="Enrich a single filing by SET news id")
    p.add_argument("--ticker", metavar="TK",
                   help="Enrich the latest filing for a ticker")
    p.add_argument("--force", action="store_true",
                   help="Bypass cache (re-enrich even if cached)")
    p.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR,
                   help=f"Path to data/ dir (default: {DEFAULT_DATA_DIR})")
    p.add_argument("--dry-run", action="store_true",
                   help="For --auto-alert: print embeds, don't POST")
    p.add_argument("--audit", type=int, metavar="N", default=None,
                   help="Print N published summaries with the source text behind each number")
    p.add_argument("--dashboard", action="store_true",
                   help="IS1-wide critical+material summaries -> data/filing-summaries.json")
    p.add_argument("--limit", type=int, default=None,
                   help=f"Max filings per run (auto-alert default {MAX_ALERTS_PER_RUN}, "
                        f"dashboard default {DASHBOARD_LIMIT})")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)
    if args.auto_alert:
        webhook = _load_webhook() if not args.dry_run else None
        return _auto_alert(args.data_dir, dry_run=args.dry_run,
                           webhook=webhook, limit=args.limit or MAX_ALERTS_PER_RUN)
    if args.audit is not None:
        return _audit(args.data_dir, count=args.audit)
    if args.dashboard:
        return _dashboard(args.data_dir, limit=args.limit or DASHBOARD_LIMIT,
                          dry_run=args.dry_run)
    if args.enrich_id:
        return _enrich_id(args.enrich_id, force=args.force, data_dir=args.data_dir)
    if args.ticker:
        return _enrich_ticker(args.ticker, force=args.force, data_dir=args.data_dir)
    _log("no mode specified — use --auto-alert, --dashboard, --enrich-id, or --ticker")
    return 1


if __name__ == "__main__":
    sys.exit(main())