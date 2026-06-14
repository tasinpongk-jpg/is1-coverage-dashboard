"""Build data/vault-ticker-notes.json from local Obsidian vault notes.

The ticker-summary page uses this as a compact per-ticker briefing layer:
earnings-call notes, MD&A snippets, and financial-statement note flags. The
full vault remains local; this file intentionally keeps only short excerpts.

Run:
  python scripts/build_vault_ticker_notes.py

VAULT_ROOT can override the default OneDrive path.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data"
OUT = DATA_DIR / "vault-ticker-notes.json"
TICKERS_FILE = DATA_DIR / "tickers.json"

DEFAULT_VAULT = Path.home() / "OneDrive - The Stock Exchange of Thailand" / "Claude-Vault"
ALT_VAULT = Path.home() / "Library" / "CloudStorage" / "OneDrive2-TheStockExchangeofThailand" / "Claude-Vault"
LISTED_SUBPATH = Path("Work-SET") / "Listed Company"

MDA_SUBPATH = Path("1-Raw") / "01-Filings" / "MDA"
FS_NOTES_SUBPATH = Path("1-Raw") / "01-Filings" / "FS-NOTES"
CALLS_SUBPATH = Path("2-Analysis") / "AI-Generated" / "03-Earning Calls"
FILING_SUMMARY_SUBPATH = Path("2-Analysis") / "AI-Generated" / "06-Inbox"
ONEREPORT_BIZ_SUBPATH = Path("1-Raw") / "01-Filings" / "ONEREPORT-BIZ"

MAX_PER_BUCKET = 5
SNIPPET_CHARS = 520


def load_tickers() -> set[str]:
    with TICKERS_FILE.open(encoding="utf-8") as f:
        return {t["tk"] for t in json.load(f).get("tickers", [])}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta: dict[str, Any] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        val = val.strip().strip('"').strip("'")
        if val.lower() in {"true", "false"}:
            meta[key.strip()] = val.lower() == "true"
        else:
            meta[key.strip()] = val
    return meta, parts[2].lstrip()


def first_heading(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line.lstrip("#").strip()
    return ""


def clean_line(line: str) -> str:
    line = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", line)
    line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
    line = re.sub(r"[*_`>#]", "", line)
    line = re.sub(r"\s+", " ", line)
    return line.strip(" -|\t")


def clean_snippet(text: str, max_chars: int = SNIPPET_CHARS) -> str:
    lines: list[str] = []
    for raw in text.splitlines():
        raw_stripped = raw.strip()
        if raw_stripped.startswith("|") or re.match(r"^\|?[-:\s|]+\|?$", raw_stripped):
            continue
        if raw_stripped.startswith(("<!--", "#MARKER:")):
            continue
        s = clean_line(raw)
        if not s:
            continue
        low = s.lower()
        if set(s) <= {"-", "|", " "}:
            continue
        if low.startswith(("filing id:", "filed:", "source:", "extracted:", "tags:", "format:")):
            continue
        if s.startswith("#") or s.startswith("MARKER:"):
            continue
        lines.append(s)
        if sum(len(x) + 1 for x in lines) >= max_chars:
            break
    snippet = " ".join(lines)
    return snippet[: max_chars - 1].rstrip() + ("..." if len(snippet) >= max_chars else "")


def content_lines(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.splitlines():
        raw_stripped = raw.strip()
        if raw_stripped.startswith("|") or re.match(r"^\|?[-:\s|]+\|?$", raw_stripped):
            continue
        s = clean_line(raw)
        if not s or len(s) < 16:
            continue
        low = s.lower()
        if low.startswith(("filing id:", "filed:", "source:", "extracted:", "tags:", "format:")):
            continue
        if low.startswith(("note:", "pie chart data", "key geographic narratives")):
            continue
        if s.endswith(":") and len(s) < 80:
            continue
        if "หน่วย:" in s and not re.search(r"\d", s):
            continue
        if re.match(r"^\d+(?:\.\d+)*\.?\s+", s):
            continue
        if re.match(r"^note\s+\d+\s*[—-].+$", s, re.I) and len(s) < 80:
            continue
        lines.append(s)
    return lines


def compact_unique(items: list[str], limit: int = 3, max_chars: int = 180) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        s = re.sub(r"\s+", " ", item).strip()
        if not s:
            continue
        key = s.lower()[:90]
        if key in seen:
            continue
        seen.add(key)
        if len(s) > max_chars:
            s = s[: max_chars - 1].rstrip() + "..."
        out.append(s)
        if len(out) >= limit:
            break
    return out


def section_points(body: str, heading_pattern: str, limit: int = 3) -> list[str]:
    return compact_unique(content_lines(section_after(body, heading_pattern)), limit=limit)


def keyword_points(body: str, keywords: tuple[str, ...], limit: int = 3) -> list[str]:
    hits: list[str] = []
    for line in content_lines(body):
        low = line.lower()
        if any(k in low for k in keywords):
            hits.append(line)
    return compact_unique(hits, limit=limit)


def metric_lines(text: str, limit: int = 4) -> list[str]:
    metrics: list[str] = []
    for raw in text.splitlines():
        s = raw.strip()
        if not s.startswith("|") or re.match(r"^\|?[-:\s|]+\|?$", s):
            continue
        cells = [clean_line(c) for c in s.strip("|").split("|")]
        cells = [c for c in cells if c]
        if len(cells) < 2 or not re.search(r"\d", " ".join(cells)):
            continue
        if cells[0].lower() in {"item", "metric", "รายการ"}:
            continue
        metrics.append(" — ".join(cells[:3]))
    return compact_unique(metrics, limit=limit, max_chars=150)


def tone_from(lines: list[str], flags: list[str]) -> str:
    text = " ".join(lines).lower()
    pos = len(re.findall(r"growth|increase|improve|recover|catalyst|เติบโต|เพิ่มขึ้น|ฟื้น|ดีขึ้น|หนุน", text))
    neg = len(re.findall(r"decline|decrease|drop|risk|pressure|loss|impair|default|ลดลง|กดดัน|ขาดทุน|เสี่ยง", text))
    if flags or neg > pos + 1:
        return "Watch"
    if pos > neg + 1:
        return "Positive"
    return "Neutral"


def analyze_body(body: str, bucket: str, snippet: str) -> dict[str, Any]:
    if bucket == "calls":
        summary_text = section_after(body, r"executive summary") or body
        drivers = section_points(body, r"revenue drivers|margin commentary|strategic initiatives", 4)
        risks = keyword_points(body, ("risk", "ความเสี่ยง", "ผันผวน", "สงคราม", "ลดลง", "ชะลอ", "กดดัน", "tariff", "fx"), 4)
        guidance = section_points(body, r"forward guidance|guidance|outlook|แนวโน้ม|เป้าหมาย", 3)
        metrics = metric_lines(section_after(body, r"key metrics") or body, 4)
        flags = keyword_points(body, ("tariff", "fx", "usd", "risk", "pressure", "decline", "ลดลง", "กดดัน"), 3)
    elif bucket == "fsNotes":
        summary_text = flagged_snippet(body) or body
        drivers = keyword_points(body, ("revenue", "customer", "segment", "รายได้", "ลูกค้า"), 3)
        risks = keyword_points(body, ("going concern", "default", "covenant", "impair", "pledge", "loan", "rpt", "related", "ผิดนัด", "ด้อยค่า"), 4)
        guidance = []
        metrics = metric_lines(body, 4)
        flags = keyword_points(body, ("flag", "critical", "primary flag", "mt/rpt", "rpt", "size test", "going concern", "covenant", "default", "impair", "pledge", "loan"), 4)
    elif bucket == "filingSummary":
        flag_text = filing_flag_snippet(body)
        summary_text = flag_text or body
        drivers = keyword_points(body, ("รายได้", "กำไร", "margin", "revenue", "volume", "ปริมาณ", "growth", "เติบโต"), 3)
        risks = keyword_points(body, ("HIGH", "MED", "🔴", "🟡", "rpt", "risk", "impair", "กดดัน", "เสี่ยง"), 4)
        guidance = []
        metrics = metric_lines(body, 4)
        flags = [s for s in flag_text.split("  ") if s][:5]
    elif bucket == "bizProfile":
        summary_text = body[:2000]
        drivers = keyword_points(body, ("ผลิตภัณฑ์", "สินค้า", "รายได้", "ลูกค้า", "product", "revenue", "customer", "segment", "business"), 4)
        risks = keyword_points(body, ("risk", "competition", "เสี่ยง", "การแข่งขัน", "regulatory", "ความเสี่ยง"), 3)
        guidance = []
        metrics = []
        flags = []
    else:
        summary_text = section_after(body, r"executive summary") or snippet or body
        drivers = keyword_points(body, ("revenue", "gross profit", "margin", "volume", "profit", "cash flow", "รายได้", "กำไร", "ปริมาณ"), 4)
        risks = keyword_points(body, ("risk", "tariff", "fx", "usd", "pressure", "decline", "impair", "ลดลง", "กดดัน", "เสี่ยง"), 3)
        guidance = section_points(body, r"management|guidance|outlook|แนวโน้ม|เป้าหมาย", 3)
        metrics = metric_lines(section_after(body, r"executive summary") or body, 4)
        flags = keyword_points(body, ("primary driver", "margin decline", "operating leverage", "customer concentration", "tariff", "hedge", "rpt"), 3)

    takeaway = clean_snippet(summary_text, 300) or snippet
    all_lines = [takeaway, *drivers, *risks, *guidance, *flags]
    return {
        "takeaway": takeaway,
        "drivers": drivers,
        "risks": risks,
        "guidance": guidance,
        "metrics": metrics,
        "flags": flags,
        "tone": tone_from(all_lines, flags),
    }


def section_after(body: str, heading_pattern: str) -> str:
    lines = body.splitlines()
    start = None
    pat = re.compile(heading_pattern, re.I)
    for i, line in enumerate(lines):
        if line.startswith("##") and pat.search(line):
            start = i + 1
            break
    if start is None:
        return ""
    out: list[str] = []
    for line in lines[start:]:
        if line.startswith("## "):
            break
        out.append(line)
    return "\n".join(out).strip()


def flagged_snippet(body: str) -> str:
    hits = []
    pat = re.compile(
        r"(flag|critical|high|mt/rpt|rpt|size test|going concern|covenant|default|impair|pledge|loan)",
        re.I,
    )
    for line in body.splitlines():
        if pat.search(line):
            s = clean_line(line)
            if len(s) >= 24:
                hits.append(s)
        if len(hits) >= 3:
            break
    return clean_snippet("\n".join(hits)) if hits else ""


def filing_flag_snippet(body: str, limit: int = 6) -> str:
    """Extract HIGH/MED/LOW flag bullet lines from filing-summary notes."""
    hits = []
    pat = re.compile(r"(HIGH|MED|LOW|🔴|🟡|🟢)", re.I)
    for line in body.splitlines():
        if pat.search(line):
            s = clean_line(line)
            if len(s) >= 10:
                hits.append(s)
        if len(hits) >= limit:
            break
    return clean_snippet("\n".join(hits)) if hits else ""


def period_from_name(path: Path) -> str:
    m = re.search(r"(20\d{2}(?:Q[1-4]|FY)|\d{4}Q[1-4]|\d{4}FY|YE\d{4})", path.stem, re.I)
    return m.group(1).upper() if m else ""


def lang_from_name(path: Path) -> str:
    m = re.search(r"_([ET])$", path.stem, re.I)
    return m.group(1).upper() if m else ""


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return path.name


def item_key(item: dict[str, Any]) -> str:
    return str(item.get("eventDate") or item.get("period") or item.get("mtime") or "")


def add_item(out: dict[str, dict[str, list[dict[str, Any]]]], ticker: str, bucket: str, item: dict[str, Any]) -> None:
    out.setdefault(ticker, {"calls": [], "mda": [], "fsNotes": [], "filingSummary": [], "bizProfile": []})
    out[ticker].setdefault(bucket, [])
    out[ticker][bucket].append(item)


def build_file_item(path: Path, listed_root: Path, bucket: str, ticker: str) -> dict[str, Any]:
    text = read_text(path)
    meta, body = split_frontmatter(text)
    title = first_heading(body) or path.stem
    snippet = ""
    if bucket == "calls":
        snippet = clean_snippet(section_after(body, r"executive summary") or body)
    elif bucket == "fsNotes":
        snippet = flagged_snippet(body) or clean_snippet(body)
    elif bucket == "filingSummary":
        snippet = filing_flag_snippet(body) or clean_snippet(body)
    elif bucket == "bizProfile":
        snippet = clean_snippet(body)
    else:
        snippet = clean_snippet(section_after(body, r"executive summary|revenue analysis|management") or body)
    analysis = analyze_body(body, bucket, snippet)
    return {
        "title": title,
        "period": str(meta.get("period") or meta.get("period_label") or period_from_name(path)),
        "eventDate": str(meta.get("event_date") or meta.get("date_logged") or ""),
        "eventType": str(meta.get("event_type") or meta.get("kind") or bucket),
        "language": str(meta.get("language") or lang_from_name(path)),
        "snippet": snippet,
        "analysis": analysis,
        "sourcePath": rel(path, listed_root),
        "mtime": dt.datetime.fromtimestamp(path.stat().st_mtime, tz=dt.timezone.utc).isoformat(),
        "needsReview": bool(meta.get("needs_review", False)),
        "verified": bool(meta.get("verified", False)),
        "youtubeId": str(meta.get("youtube_id") or ""),
        "presentationId": str(meta.get("presentation_id") or ""),
    }


def scan_vault(listed_root: Path, tickers: set[str]) -> dict[str, dict[str, list[dict[str, Any]]]]:
    out: dict[str, dict[str, list[dict[str, Any]]]] = {}

    for bucket, subpath in (("mda", MDA_SUBPATH), ("fsNotes", FS_NOTES_SUBPATH)):
        base = listed_root / subpath
        if not base.is_dir():
            continue
        for ticker_dir in base.iterdir():
            ticker = ticker_dir.name.upper()
            if ticker not in tickers or not ticker_dir.is_dir():
                continue
            for path in ticker_dir.glob("*.md"):
                add_item(out, ticker, bucket, build_file_item(path, listed_root, bucket, ticker))

    calls_base = listed_root / CALLS_SUBPATH
    if calls_base.is_dir():
        for path in calls_base.rglob("*.md"):
            if path.name.startswith("_"):
                continue
            meta, _body = split_frontmatter(read_text(path))
            ticker = str(meta.get("ticker") or path.parent.name or "").upper()
            if ticker in tickers:
                add_item(out, ticker, "calls", build_file_item(path, listed_root, "calls", ticker))

    # Filing summaries: flat inbox dir, ticker extracted from filename prefix
    fs_sum_base = listed_root / FILING_SUMMARY_SUBPATH
    if fs_sum_base.is_dir():
        for path in fs_sum_base.glob("*-filing-summary-*.md"):
            m = re.match(r"^([A-Z0-9]+)-filing-summary-", path.name, re.I)
            if not m:
                continue
            ticker = m.group(1).upper()
            if ticker in tickers:
                add_item(out, ticker, "filingSummary", build_file_item(path, listed_root, "filingSummary", ticker))

    # OneReport biz sections: by ticker subdir
    biz_base = listed_root / ONEREPORT_BIZ_SUBPATH
    if biz_base.is_dir():
        for ticker_dir in biz_base.iterdir():
            ticker = ticker_dir.name.upper()
            if ticker not in tickers or not ticker_dir.is_dir():
                continue
            for path in ticker_dir.glob("*_BIZ.md"):
                add_item(out, ticker, "bizProfile", build_file_item(path, listed_root, "bizProfile", ticker))

    for ticker, buckets in out.items():
        for bucket, items in buckets.items():
            items.sort(key=item_key, reverse=True)
            del items[MAX_PER_BUCKET:]
    return out


def scan_selected(
    listed_root: Path,
    wanted: set[str],
    existing: dict[str, dict[str, list[dict[str, Any]]]],
) -> dict[str, dict[str, list[dict[str, Any]]]]:
    out = dict(existing)
    for ticker in wanted:
        preserved_calls = (out.get(ticker) or {}).get("calls") or []
        out[ticker] = {"calls": preserved_calls, "mda": [], "fsNotes": [], "filingSummary": [], "bizProfile": []}

    for bucket, subpath in (("mda", MDA_SUBPATH), ("fsNotes", FS_NOTES_SUBPATH)):
        base = listed_root / subpath
        for ticker in wanted:
            ticker_dir = base / ticker
            if not ticker_dir.is_dir():
                continue
            for path in ticker_dir.glob("*.md"):
                add_item(out, ticker, bucket, build_file_item(path, listed_root, bucket, ticker))

    # Refresh filing summaries for wanted tickers
    fs_sum_base = listed_root / FILING_SUMMARY_SUBPATH
    if fs_sum_base.is_dir():
        for path in fs_sum_base.glob("*-filing-summary-*.md"):
            m = re.match(r"^([A-Z0-9]+)-filing-summary-", path.name, re.I)
            if not m:
                continue
            ticker = m.group(1).upper()
            if ticker in wanted:
                add_item(out, ticker, "filingSummary", build_file_item(path, listed_root, "filingSummary", ticker))

    # Refresh biz profiles for wanted tickers
    biz_base = listed_root / ONEREPORT_BIZ_SUBPATH
    if biz_base.is_dir():
        for ticker in wanted:
            ticker_dir = biz_base / ticker
            if not ticker_dir.is_dir():
                continue
            for path in ticker_dir.glob("*_BIZ.md"):
                add_item(out, ticker, "bizProfile", build_file_item(path, listed_root, "bizProfile", ticker))

    for ticker in wanted:
        for bucket, items in out.get(ticker, {}).items():
            items.sort(key=item_key, reverse=True)
            del items[MAX_PER_BUCKET:]
        if not any(out.get(ticker, {}).values()):
            out.pop(ticker, None)
    return out


def find_vault_root() -> Path:
    if os.environ.get("VAULT_ROOT"):
        return Path(os.environ["VAULT_ROOT"]).expanduser()
    for root in (DEFAULT_VAULT, ALT_VAULT):
        if (root / LISTED_SUBPATH).is_dir():
            return root
    return DEFAULT_VAULT


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", action="append", default=[], help="Ticker to refresh. Repeatable.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    vault = find_vault_root()
    listed_root = vault / LISTED_SUBPATH
    if not listed_root.is_dir():
        print(f"[build_vault_ticker_notes] vault not found; keeping existing JSON: {listed_root}")
        return 0

    tickers = load_tickers()
    wanted = {t.upper() for t in args.ticker if t}
    if wanted:
        unknown = sorted(wanted - tickers)
        if unknown:
            print(f"[build_vault_ticker_notes] ignoring unknown tickers: {', '.join(unknown)}")
        wanted &= tickers
        existing_payload = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
        notes = scan_selected(listed_root, wanted, existing_payload.get("tickers") or {})
    else:
        notes = scan_vault(listed_root, tickers)
    totals = {
        "tickers": len(notes),
        "calls": sum(len(v.get("calls", [])) for v in notes.values()),
        "mda": sum(len(v.get("mda", [])) for v in notes.values()),
        "fsNotes": sum(len(v.get("fsNotes", [])) for v in notes.values()),
        "filingSummary": sum(len(v.get("filingSummary", [])) for v in notes.values()),
        "bizProfile": sum(len(v.get("bizProfile", [])) for v in notes.values()),
    }
    payload = {
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "source": "OneDrive Obsidian vault compact excerpts",
        "totals": totals,
        "tickers": notes,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.name}: {totals}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
