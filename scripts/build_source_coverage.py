"""Build source coverage and filing-fetch queue for the company report agent.

This answers the practical question: which tickers have enough current
MD&A / financial-statement note evidence to analyze now, and which should be
fetched first from the SET news page.

Run:
  python scripts/build_source_coverage.py --period 2026Q1

Outputs:
  data/source-coverage.json
  data/source-coverage-fetch-queue.csv
  Obsidian queue note under Work-SET/Listed Company/2-Analysis/AI-Generated
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data"
TICKER_SUMMARY = DATA_DIR / "ticker-summary.json"
TICKERS_FILE = DATA_DIR / "tickers.json"
VAULT_NOTES = DATA_DIR / "vault-ticker-notes.json"
OUT_JSON = DATA_DIR / "source-coverage.json"
OUT_CSV = DATA_DIR / "source-coverage-fetch-queue.csv"

LISTED_SUBPATH = Path("Work-SET") / "Listed Company"
MDA_SUBPATH = Path("1-Raw") / "01-Filings" / "MDA"
FS_NOTES_SUBPATH = Path("1-Raw") / "01-Filings" / "FS-NOTES"
AUDITOR_SUBPATH = Path("1-Raw") / "01-Filings" / "AUDITOR"
COVERAGE_NOTE_SUBPATH = (
    Path("2-Analysis") / "AI-Generated" / "08-Source Coverage"
)

DEFAULT_PERIOD = os.environ.get("SOURCE_COVERAGE_PERIOD", "2026Q1")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def canonical_period(value: Any) -> str:
    text = clean(value).upper()
    if not text:
        return ""
    text = text.replace("_", "-").replace(" ", "")

    patterns = [
        (r"(20\d{2})[-/]?(Q[1-4])", lambda m: f"{m.group(1)}{m.group(2)}"),
        (r"(Q[1-4])[-/]?(20\d{2})", lambda m: f"{m.group(2)}{m.group(1)}"),
        (r"(20\d{2})[-/]?(?:FY|YE|YEARLY)", lambda m: f"{m.group(1)}FY"),
        (r"(?:FY|YE|YEARLY)[-/]?(20\d{2})", lambda m: f"{m.group(1)}FY"),
    ]
    for pat, convert in patterns:
        m = re.search(pat, text)
        if m:
            return convert(m)

    m = re.search(r"Q([1-4])[-/]?(25\d{2})", text)
    if m:
        return f"{int(m.group(2)) - 543}Q{m.group(1)}"

    m = re.search(r"Q([1-4])[-/]?(\d{2})", text)
    if m:
        yy = int(m.group(2))
        if yy >= 50:
            return f"{1957 + yy}Q{m.group(1)}"

    return ""


def display_period(period: str) -> str:
    period = canonical_period(period)
    if not period:
        return ""
    if period.endswith("FY"):
        return f"FY-{period[:4]}"
    return f"{period[4:]}-{period[:4]}"


def period_sort_key(period: str) -> tuple[int, int]:
    period = canonical_period(period)
    if not period:
        return (0, 0)
    year = int(period[:4])
    quarter = 5 if period.endswith("FY") else int(period[-1])
    return (year, quarter)


def period_from_file(path: Path) -> str:
    period = canonical_period(path.stem)
    if period:
        return period

    try:
        lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()[:80]
    except OSError:
        return ""
    if not lines or lines[0].strip() != "---":
        return ""
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        if key.strip().lower() in {"period", "period_label"}:
            return canonical_period(val)
    return ""


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path)


def candidate_vault_roots() -> list[Path]:
    roots: list[Path] = []
    if os.environ.get("VAULT_ROOT"):
        roots.append(Path(os.environ["VAULT_ROOT"]).expanduser())
    home = Path.home()
    roots.extend(
        [
            home / "OneDrive - The Stock Exchange of Thailand" / "Claude-Vault",
            home / "Library" / "CloudStorage" / "OneDrive2-TheStockExchangeofThailand" / "Claude-Vault",
        ]
    )
    return roots


def find_listed_root(explicit: str = "") -> Path | None:
    roots = [Path(explicit).expanduser()] if explicit else candidate_vault_roots()
    for root in roots:
        listed = root / LISTED_SUBPATH
        if listed.is_dir():
            return listed
    return None


def candidate_sec_idisc_roots() -> list[Path]:
    roots: list[Path] = []
    if os.environ.get("SEC_IDISC_ROOT"):
        roots.append(Path(os.environ["SEC_IDISC_ROOT"]).expanduser())
    home = Path.home()
    roots.extend(
        [
            home / "Projects" / "SET_AI-Build-Roadmap" / "sec_idisc",
            REPO.parent / "SET_AI-Build-Roadmap" / "sec_idisc",
        ]
    )
    return roots


def find_sec_idisc_root(explicit: str = "") -> Path | None:
    roots = [Path(explicit).expanduser()] if explicit else candidate_sec_idisc_roots()
    for root in roots:
        if root.is_dir():
            return root
    return None


def load_tickers() -> list[dict[str, Any]]:
    summary = load_json(TICKER_SUMMARY, {})
    rows = summary.get("tickers") or []
    if rows:
        return sorted(rows, key=lambda r: str(r.get("tk") or ""))

    tickers = load_json(TICKERS_FILE, {}).get("tickers") or []
    return sorted(tickers, key=lambda r: str(r.get("tk") or ""))


def scan_vault_bucket(
    listed_root: Path | None, subpath: Path, tickers: set[str]
) -> dict[str, list[dict[str, str]]]:
    out: dict[str, list[dict[str, str]]] = {tk: [] for tk in tickers}
    if not listed_root:
        return out
    base = listed_root / subpath
    if not base.is_dir():
        return out
    for ticker_dir in base.iterdir():
        tk = ticker_dir.name.upper()
        if tk not in tickers or not ticker_dir.is_dir():
            continue
        for path in ticker_dir.glob("*.md"):
            period = period_from_file(path)
            out[tk].append(
                {
                    "period": period,
                    "path": rel(path, listed_root),
                    "name": path.name,
                    "mtime": dt.datetime.fromtimestamp(
                        path.stat().st_mtime, tz=dt.timezone.utc
                    ).isoformat(timespec="seconds"),
                }
            )
    for items in out.values():
        items.sort(key=lambda x: period_sort_key(x.get("period", "")), reverse=True)
    return out


def items_from_notes_json(
    notes_payload: dict[str, Any], tickers: set[str], bucket: str
) -> dict[str, list[dict[str, str]]]:
    out: dict[str, list[dict[str, str]]] = {tk: [] for tk in tickers}
    notes_map = notes_payload.get("tickers") or {}
    for tk in tickers:
        for item in (notes_map.get(tk) or {}).get(bucket) or []:
            period = canonical_period(item.get("period") or item.get("title") or "")
            out[tk].append(
                {
                    "period": period,
                    "path": clean(item.get("sourcePath")),
                    "name": clean(item.get("title")),
                    "mtime": clean(item.get("mtime")),
                }
            )
    for items in out.values():
        items.sort(key=lambda x: period_sort_key(x.get("period", "")), reverse=True)
    return out


def merge_items(*groups: dict[str, list[dict[str, str]]]) -> dict[str, list[dict[str, str]]]:
    tickers = set().union(*(set(g) for g in groups))
    out: dict[str, list[dict[str, str]]] = {tk: [] for tk in tickers}
    for tk in tickers:
        seen: set[tuple[str, str]] = set()
        for group in groups:
            for item in group.get(tk) or []:
                key = (item.get("period", ""), item.get("path") or item.get("name", ""))
                if key in seen:
                    continue
                seen.add(key)
                out[tk].append(item)
        out[tk].sort(key=lambda x: period_sort_key(x.get("period", "")), reverse=True)
    return out


def latest_period(items: list[dict[str, str]]) -> str:
    periods = [canonical_period(i.get("period")) for i in items if canonical_period(i.get("period"))]
    if not periods:
        return ""
    return sorted(periods, key=period_sort_key, reverse=True)[0]


def has_period(items: list[dict[str, str]], target: str) -> bool:
    return any(canonical_period(i.get("period")) == target for i in items)


def source_paths_for_period(items: list[dict[str, str]], target: str, limit: int = 3) -> list[str]:
    paths = [
        clean(i.get("path") or i.get("name"))
        for i in items
        if canonical_period(i.get("period")) == target
    ]
    return [p for p in paths if p][:limit]


def scan_sec_idisc(
    sec_root: Path | None, tickers: set[str]
) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {tk: [] for tk in tickers}
    if not sec_root:
        return out
    for tk in tickers:
        quarterly = sec_root / tk / "quarterly"
        if not quarterly.is_dir():
            continue
        for folder in quarterly.iterdir():
            if not folder.is_dir():
                continue
            period = canonical_period(folder.name)
            files = {
                "mda_pdf": (folder / "md-and-a.pdf").exists(),
                "auditor_doc": (folder / "auditor-report.docx").exists()
                or (folder / "auditor-report.doc").exists(),
                "auditor_md": (folder / "auditor-report.md").exists(),
                "financial_xlsx": (folder / "financial-statements.xlsx").exists()
                or (folder / "financial-statements.xls").exists(),
                "financial_md": (folder / "financial-statements.md").exists(),
                "notes_doc": (folder / "notes.docx").exists() or (folder / "notes.doc").exists(),
                "notes_md": (folder / "notes.md").exists(),
            }
            filing_date = ""
            m = re.match(r"(\d{4}-\d{2}-\d{2})", folder.name)
            if m:
                filing_date = m.group(1)
            out[tk].append(
                {
                    "period": period,
                    "folder": rel(folder, sec_root),
                    "filingDate": filing_date,
                    "files": files,
                }
            )
    for items in out.values():
        items.sort(key=lambda x: period_sort_key(x.get("period", "")), reverse=True)
    return out


def sec_current_item(items: list[dict[str, Any]], target: str) -> dict[str, Any] | None:
    for item in items:
        if canonical_period(item.get("period")) == target:
            return item
    return None


def build_row(
    ticker: dict[str, Any],
    target: str,
    mda_items: list[dict[str, str]],
    fs_items: list[dict[str, str]],
    auditor_items: list[dict[str, str]],
    call_items: list[dict[str, str]],
    sec_items: list[dict[str, Any]],
) -> dict[str, Any]:
    tk = str(ticker.get("tk") or "").upper()
    sec_current = sec_current_item(sec_items, target)
    sec_files = (sec_current or {}).get("files") or {}

    mda_current = has_period(mda_items, target)
    fs_current = has_period(fs_items, target)
    auditor_current = has_period(auditor_items, target) or bool(
        sec_files.get("auditor_md") or sec_files.get("auditor_doc")
    )
    call_current = has_period(call_items, target)

    current_sec_has_mda = bool(sec_files.get("mda_pdf"))
    current_sec_has_fs = bool(sec_files.get("financial_xlsx") and sec_files.get("notes_doc"))
    current_sec_has_extracts = bool(
        sec_files.get("auditor_md") and sec_files.get("financial_md") and sec_files.get("notes_md")
    )

    missing: list[str] = []
    ingestable: list[str] = []

    if not mda_current:
        if current_sec_has_mda:
            ingestable.append("MDA")
        else:
            missing.append("MDA")
    if not fs_current:
        if sec_files.get("notes_md") or sec_files.get("financial_md"):
            ingestable.append("FS notes")
        elif current_sec_has_fs:
            ingestable.append("FS package extract")
        else:
            missing.append("FS notes")
    if not auditor_current:
        if sec_files.get("auditor_doc"):
            ingestable.append("auditor extract")
        else:
            missing.append("auditor")

    can_analyze = mda_current and fs_current
    if can_analyze:
        action = "analyze_ready"
        rank = 3
    elif ingestable and not missing:
        action = "extract_or_ingest_existing_sec_idisc"
        rank = 0
    elif ingestable:
        action = "fetch_missing_then_ingest_existing"
        rank = 1
    else:
        action = "fetch_set_news_current_quarter"
        rank = 1 if {"MDA", "FS notes"}.issubset(set(missing)) else 2

    latest = {
        "mda": latest_period(mda_items),
        "fsNotes": latest_period(fs_items),
        "auditor": latest_period(auditor_items),
        "calls": latest_period(call_items),
        "secIdisc": latest_period([
            {"period": str(item.get("period") or "")} for item in sec_items
        ]),
    }

    return {
        "tk": tk,
        "name": ticker.get("name"),
        "sector": ticker.get("sector"),
        "segment": ticker.get("segment"),
        "rm": ticker.get("rm"),
        "targetPeriod": target,
        "canAnalyzeNow": can_analyze,
        "action": action,
        "queueRank": rank,
        "missingCurrent": missing,
        "ingestableCurrent": ingestable,
        "currentCoverage": {
            "mda": mda_current,
            "fsNotes": fs_current,
            "auditor": auditor_current,
            "calls": call_current,
            "secIdiscFolder": bool(sec_current),
            "secIdiscMdaPdf": current_sec_has_mda,
            "secIdiscFsPackage": current_sec_has_fs,
            "secIdiscExtracts": current_sec_has_extracts,
        },
        "latestPeriods": latest,
        "sourcePaths": {
            "mda": source_paths_for_period(mda_items, target),
            "fsNotes": source_paths_for_period(fs_items, target),
            "auditor": source_paths_for_period(auditor_items, target),
            "calls": source_paths_for_period(call_items, target),
            "secIdisc": [sec_current.get("folder")] if sec_current else [],
        },
    }


def summarize(rows: list[dict[str, Any]], target: str) -> dict[str, Any]:
    def count(path: str) -> int:
        keys = path.split(".")
        total = 0
        for row in rows:
            val: Any = row
            for key in keys:
                val = val.get(key) if isinstance(val, dict) else None
            if val:
                total += 1
        return total

    by_action: dict[str, int] = {}
    by_rm_missing: dict[str, int] = {}
    for row in rows:
        by_action[row["action"]] = by_action.get(row["action"], 0) + 1
        if not row["canAnalyzeNow"]:
            rm = clean(row.get("rm")) or "Unassigned"
            by_rm_missing[rm] = by_rm_missing.get(rm, 0) + 1

    return {
        "targetPeriod": target,
        "tickers": len(rows),
        "canAnalyzeNow": sum(1 for r in rows if r["canAnalyzeNow"]),
        "needsBeforeReport": sum(1 for r in rows if not r["canAnalyzeNow"]),
        "currentMda": count("currentCoverage.mda"),
        "currentFsNotes": count("currentCoverage.fsNotes"),
        "currentAuditor": count("currentCoverage.auditor"),
        "currentCalls": count("currentCoverage.calls"),
        "currentSecIdiscFolder": count("currentCoverage.secIdiscFolder"),
        "currentSecIdiscMdaPdf": count("currentCoverage.secIdiscMdaPdf"),
        "currentSecIdiscFsPackage": count("currentCoverage.secIdiscFsPackage"),
        "actions": dict(sorted(by_action.items())),
        "missingByRm": dict(sorted(by_rm_missing.items())),
    }


def csv_rows(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for row in sorted(rows, key=lambda r: (r["queueRank"], clean(r.get("rm")), clean(r.get("sector")), r["tk"])):
        if row["canAnalyzeNow"]:
            continue
        out.append(
            {
                "queue_rank": str(row["queueRank"]),
                "ticker": row["tk"],
                "rm": clean(row.get("rm")),
                "sector": clean(row.get("sector")),
                "action": row["action"],
                "missing_current": ", ".join(row["missingCurrent"]),
                "ingestable_current": ", ".join(row["ingestableCurrent"]),
                "latest_mda": display_period(row["latestPeriods"].get("mda", "")),
                "latest_fs_notes": display_period(row["latestPeriods"].get("fsNotes", "")),
                "latest_sec_idisc": display_period(row["latestPeriods"].get("secIdisc", "")),
            }
        )
    return out


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    records = csv_rows(rows)
    fields = [
        "queue_rank",
        "ticker",
        "rm",
        "sector",
        "action",
        "missing_current",
        "ingestable_current",
        "latest_mda",
        "latest_fs_notes",
        "latest_sec_idisc",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)


def markdown_note(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    target = display_period(summary["targetPeriod"])
    rows = payload["rows"]
    queue = [r for r in rows if not r["canAnalyzeNow"]]
    queue.sort(key=lambda r: (r["queueRank"], clean(r.get("rm")), clean(r.get("sector")), r["tk"]))
    ready = [r for r in rows if r["canAnalyzeNow"]]

    rm_lines = "\n".join(
        f"- {rm}: {count}" for rm, count in summary.get("missingByRm", {}).items()
    ) or "- n/a"
    action_lines = "\n".join(
        f"- {action}: {count}" for action, count in summary.get("actions", {}).items()
    ) or "- n/a"

    table_lines = [
        "| Rank | Ticker | RM | Sector | Action | Missing | Ingestable | Latest MDA | Latest FS |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in queue:
        table_lines.append(
            "| {rank} | {tk} | {rm} | {sector} | {action} | {missing} | {ingestable} | {mda} | {fs} |".format(
                rank=row["queueRank"],
                tk=row["tk"],
                rm=clean(row.get("rm")),
                sector=clean(row.get("sector")),
                action=row["action"],
                missing=", ".join(row["missingCurrent"]) or "-",
                ingestable=", ".join(row["ingestableCurrent"]) or "-",
                mda=display_period(row["latestPeriods"].get("mda", "")) or "-",
                fs=display_period(row["latestPeriods"].get("fsNotes", "")) or "-",
            )
        )

    ready_preview = ", ".join(r["tk"] for r in sorted(ready, key=lambda r: r["tk"])[:80])
    if len(ready) > 80:
        ready_preview += f", ... +{len(ready) - 80}"
    ready_preview = ready_preview or "n/a"

    generated = payload["generated"]
    source_roots = payload["sourceRoots"]
    return f"""---
source_type: ai-generated
generated_by: codex
report_type: source-coverage-queue
target_period: {summary["targetPeriod"]}
generated_at: {generated}
dashboard_json: data/source-coverage.json
tags: [source-coverage]
---

# IS1 Source Coverage Queue - {target}

## Summary
- Total tickers: {summary["tickers"]}
- Ready for report analysis now: {summary["canAnalyzeNow"]}
- Need source work before report: {summary["needsBeforeReport"]}
- Current MD&A notes: {summary["currentMda"]}
- Current FS-note notes: {summary["currentFsNotes"]}
- Current auditor evidence: {summary["currentAuditor"]}
- Current earning-call notes: {summary["currentCalls"]}
- Current `sec_idisc` folders: {summary["currentSecIdiscFolder"]}
- Current `sec_idisc` FS packages: {summary["currentSecIdiscFsPackage"]}
- Current `sec_idisc` MD&A PDFs: {summary["currentSecIdiscMdaPdf"]}

## Recommended order
1. Use `extract_or_ingest_existing_sec_idisc` rows first. The raw filing folder already exists; finish the vault briefing layer.
2. Use `fetch_set_news_current_quarter` rows next. These need SET news FS/MD&A before analyst reports.
3. Run company-report generation only after both current MD&A and FS-note evidence exist.

## Source roots
- Vault listed root: `{source_roots.get("listedRoot") or "not found"}`
- sec_idisc root: `{source_roots.get("secIdiscRoot") or "not found"}`

## Actions
{action_lines}

## Missing by RM
{rm_lines}

## Fetch / Ingest Queue
{chr(10).join(table_lines)}

## Ready now
{ready_preview}
"""


def write_vault_note(listed_root: Path | None, payload: dict[str, Any]) -> str:
    if not listed_root:
        return ""
    date = dt.datetime.now().date().isoformat()
    path = listed_root / COVERAGE_NOTE_SUBPATH / f"{date} Source Coverage Queue.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown_note(payload), encoding="utf-8")
    return rel(path, listed_root)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--period", default=DEFAULT_PERIOD, help="Target period, e.g. 2026Q1 or Q1-2026.")
    parser.add_argument("--vault-root", default="", help="Override Obsidian vault root.")
    parser.add_argument("--sec-idisc-root", default="", help="Override sec_idisc root.")
    parser.add_argument("--no-write-vault", dest="write_vault", action="store_false")
    parser.add_argument("--no-csv", dest="write_csv", action="store_false")
    parser.set_defaults(write_vault=True, write_csv=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    target = canonical_period(args.period)
    if not target:
        raise SystemExit(f"Cannot parse period: {args.period}")

    tickers = load_tickers()
    ticker_set = {str(t.get("tk") or "").upper() for t in tickers}
    ticker_set.discard("")
    listed_root = find_listed_root(args.vault_root)
    sec_root = find_sec_idisc_root(args.sec_idisc_root)
    notes_payload = load_json(VAULT_NOTES, {})

    vault_mda = scan_vault_bucket(listed_root, MDA_SUBPATH, ticker_set)
    vault_fs = scan_vault_bucket(listed_root, FS_NOTES_SUBPATH, ticker_set)
    vault_auditor = scan_vault_bucket(listed_root, AUDITOR_SUBPATH, ticker_set)
    notes_mda = items_from_notes_json(notes_payload, ticker_set, "mda")
    notes_fs = items_from_notes_json(notes_payload, ticker_set, "fsNotes")
    notes_calls = items_from_notes_json(notes_payload, ticker_set, "calls")
    sec_items = scan_sec_idisc(sec_root, ticker_set)

    mda_items = merge_items(vault_mda, notes_mda)
    fs_items = merge_items(vault_fs, notes_fs)

    rows = [
        build_row(
            ticker,
            target,
            mda_items.get(str(ticker.get("tk") or "").upper()) or [],
            fs_items.get(str(ticker.get("tk") or "").upper()) or [],
            vault_auditor.get(str(ticker.get("tk") or "").upper()) or [],
            notes_calls.get(str(ticker.get("tk") or "").upper()) or [],
            sec_items.get(str(ticker.get("tk") or "").upper()) or [],
        )
        for ticker in tickers
        if str(ticker.get("tk") or "").upper() in ticker_set
    ]
    rows.sort(key=lambda r: r["tk"])

    generated = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    payload = {
        "generated": generated,
        "source": "ticker-summary.json + vault filing notes + sec_idisc folder scan",
        "sourceRoots": {
            "listedRoot": str(listed_root) if listed_root else "",
            "secIdiscRoot": str(sec_root) if sec_root else "",
        },
        "summary": summarize(rows, target),
        "rows": rows,
    }
    payload["vaultQueuePath"] = (
        write_vault_note(listed_root, payload) if args.write_vault else ""
    )

    write_json(OUT_JSON, payload)
    if args.write_csv:
        write_csv(OUT_CSV, rows)

    print(
        f"Wrote {OUT_JSON.name}: "
        f"{payload['summary']['canAnalyzeNow']} ready, "
        f"{payload['summary']['needsBeforeReport']} need source work"
    )
    if payload.get("vaultQueuePath"):
        print(f"Wrote vault queue: {payload['vaultQueuePath']}")
    if args.write_csv:
        print(f"Wrote {OUT_CSV.name}: {len(csv_rows(rows))} queue rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
