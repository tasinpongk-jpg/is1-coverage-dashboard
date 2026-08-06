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
              pdf_sha256: str) -> None:
    cache["summaries"][filing_id] = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "bullets_th": bullets,
        "model": model,
        "tokens": {"in": in_tokens, "out": out_tokens},
        "pdf_sha256": pdf_sha256,
        "prompt_version": PROMPT_VERSION,
    }


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


def _documents_from_payload(payload: bytes) -> list[bytes | str] | None:
    """Resolve a PDF or ZIP payload into m3-ready documents.

    Mixed-type result: PDF bytes stay as ``bytes`` (uploaded to m3 as
    ``application/pdf`` documents); DOCX/XLSX entries are extracted to
    plain text strings (sent to m3 as ``text`` blocks). The caller
    branches on element type.
    """
    if payload.startswith(b"%PDF-"):
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
             filing: dict) -> tuple[list[str] | None, dict]:
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
    user = USER_PROMPT_TEMPLATE.format(
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
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": content}],
    }
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

def _enrich_one(filing: dict, *, force: bool = False) -> tuple[list[str], dict]:
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

    bullets, usage = _call_m3(documents, filing)
    if bullets is None:
        return _fallback_bullets(filing), {
            "source": "fallback_m3_failed", "in_tokens": 0, "out_tokens": 0,
            "cost_usd": 0.0, "cache_hit": False, "errors": ["m3_failed"],
        }

    in_tok = usage.get("input_tokens", 0)
    out_tok = usage.get("output_tokens", 0)
    cost = (in_tok / 1e6) * 3.0 + (out_tok / 1e6) * 15.0

    # Persist to cache atomically.
    try:
        cache = _load_cache()  # re-read in case of races
        _cache_put(cache, fid, bullets, M3_MODEL, in_tok, out_tok, payload_sha)
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
    p.add_argument("--limit", type=int, default=MAX_ALERTS_PER_RUN,
                   help=f"Max embeds per auto-alert run (default: {MAX_ALERTS_PER_RUN})")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_argparser().parse_args(argv)
    if args.auto_alert:
        webhook = _load_webhook() if not args.dry_run else None
        return _auto_alert(args.data_dir, dry_run=args.dry_run,
                           webhook=webhook, limit=args.limit)
    if args.enrich_id:
        return _enrich_id(args.enrich_id, force=args.force, data_dir=args.data_dir)
    if args.ticker:
        return _enrich_ticker(args.ticker, force=args.force, data_dir=args.data_dir)
    _log("no mode specified — use --auto-alert, --enrich-id, or --ticker")
    return 1


if __name__ == "__main__":
    sys.exit(main())