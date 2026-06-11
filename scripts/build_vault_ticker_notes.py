"""Build data/vault-ticker-notes.json from local Obsidian vault notes.

The ticker-summary page uses this as a compact per-ticker briefing layer:
earnings-call notes, MD&A snippets, and financial-statement note flags. The
full vault remains local; this file intentionally keeps only short excerpts.

Run:
  python scripts/build_vault_ticker_notes.py

VAULT_ROOT can override the default OneDrive path.
"""

from __future__ import annotations

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
LISTED_SUBPATH = Path("Work-SET") / "Listed Company"

MDA_SUBPATH = Path("1-Raw") / "01-Filings" / "MDA"
FS_NOTES_SUBPATH = Path("1-Raw") / "01-Filings" / "FS-NOTES"
CALLS_SUBPATH = Path("2-Analysis") / "AI-Generated" / "03-Earning Calls"

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
        s = clean_line(raw)
        if not s:
            continue
        low = s.lower()
        if set(s) <= {"-", "|", " "}:
            continue
        if low.startswith(("filing id:", "filed:", "source:", "extracted:", "tags:", "format:")):
            continue
        if s.startswith("#"):
            continue
        lines.append(s)
        if sum(len(x) + 1 for x in lines) >= max_chars:
            break
    snippet = " ".join(lines)
    return snippet[: max_chars - 1].rstrip() + ("..." if len(snippet) >= max_chars else "")


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
    out.setdefault(ticker, {"calls": [], "mda": [], "fsNotes": []})
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
    else:
        snippet = clean_snippet(section_after(body, r"executive summary|revenue analysis|management") or body)
    return {
        "title": title,
        "period": str(meta.get("period") or meta.get("period_label") or period_from_name(path)),
        "eventDate": str(meta.get("event_date") or meta.get("date_logged") or ""),
        "eventType": str(meta.get("event_type") or meta.get("kind") or bucket),
        "language": str(meta.get("language") or lang_from_name(path)),
        "snippet": snippet,
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

    for ticker, buckets in out.items():
        for bucket, items in buckets.items():
            items.sort(key=item_key, reverse=True)
            del items[MAX_PER_BUCKET:]
    return out


def main() -> int:
    vault = Path(os.environ.get("VAULT_ROOT", DEFAULT_VAULT))
    listed_root = vault / LISTED_SUBPATH
    if not listed_root.is_dir():
        print(f"[build_vault_ticker_notes] vault not found; keeping existing JSON: {listed_root}")
        return 0

    tickers = load_tickers()
    notes = scan_vault(listed_root, tickers)
    totals = {
        "tickers": len(notes),
        "calls": sum(len(v["calls"]) for v in notes.values()),
        "mda": sum(len(v["mda"]) for v in notes.values()),
        "fsNotes": sum(len(v["fsNotes"]) for v in notes.values()),
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
