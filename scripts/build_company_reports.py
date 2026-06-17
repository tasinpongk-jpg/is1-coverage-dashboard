"""Build analyst-style company reports for company-summary.html.

This local agent reads dashboard company data plus compact Obsidian excerpts,
creates one per-ticker report, saves Markdown back to the Obsidian vault, and
writes data/company-reports.json for the static dashboard.

LLM use is optional:
  - default auto mode uses Anthropic only when ANTHROPIC_API_KEY is set
  - --llm never produces deterministic drafts for wiring/tests
  - --llm always fails fast if the key or package is unavailable

Run examples:
  python scripts/build_company_reports.py --ticker AAI
  python scripts/build_company_reports.py --all --llm auto
  VAULT_ROOT="/path/to/Claude-Vault" python scripts/build_company_reports.py --all
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
import textwrap
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
DATA_DIR = REPO / "data"
TICKER_SUMMARY = DATA_DIR / "ticker-summary.json"
VAULT_NOTES = DATA_DIR / "vault-ticker-notes.json"
DISCLOSURES = DATA_DIR / "disclosure-pulse.json"
OPPDAY = DATA_DIR / "oppday-minutes.json"
OUT = DATA_DIR / "company-reports.json"

LISTED_SUBPATH = Path("Work-SET") / "Listed Company"
REPORT_SUBPATH = Path("2-Analysis") / "AI-Generated" / "07-Company Reports"

DEFAULT_MODEL = os.environ.get("COMPANY_REPORT_MODEL", "claude-sonnet-4-5")
MAX_SOURCE_NOTES = 4


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean_text(value: Any, limit: int | None = None) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if limit and len(text) > limit:
        return text[: limit - 1].rstrip() + "..."
    return text


def compact_list(items: list[Any], limit: int = 4, max_chars: int = 180) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        text = clean_text(item, max_chars)
        if not text:
            continue
        key = text.lower()[:90]
        if key in seen:
            continue
        seen.add(key)
        out.append(text)
        if len(out) >= limit:
            break
    return out


def fmt_num(value: Any, suffix: str = "", digits: int = 1) -> str:
    if value is None:
        return "n/a"
    try:
        n = float(value)
    except (TypeError, ValueError):
        return str(value)
    return f"{n:,.{digits}f}{suffix}"


def fmt_money_m(value: Any) -> str:
    if value is None:
        return "n/a"
    try:
        n = float(value)
    except (TypeError, ValueError):
        return str(value)
    if abs(n) >= 1000:
        return f"THB {n/1000:,.1f}bn"
    return f"THB {n:,.0f}m"


def pct_change(now: Any, prev: Any) -> float | None:
    try:
        now_f = float(now)
        prev_f = float(prev)
    except (TypeError, ValueError):
        return None
    if prev_f == 0:
        return None
    return (now_f / prev_f - 1) * 100


def fmt_change(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:+.1f}%"


def period_label(row: dict[str, Any] | None) -> str:
    if not row:
        return "n/a"
    year = row.get("year", "")
    q = row.get("quarter") or ""
    months = row.get("months")
    if q == "Q9" or months == 12:
        return str(year)
    return f"{year} {q}".strip()


def latest_full_year(highlights: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    full = [h for h in highlights if (h.get("months") or 12) == 12]
    if not full:
        return None, None
    return full[-1], full[-2] if len(full) >= 2 else None


def latest_period(highlights: list[dict[str, Any]]) -> dict[str, Any] | None:
    return highlights[-1] if highlights else None


def note_analysis_points(notes: list[dict[str, Any]], fields: tuple[str, ...], limit: int = 5) -> list[str]:
    points: list[str] = []
    for note in notes:
        analysis = note.get("analysis") or {}
        for field in fields:
            value = analysis.get(field)
            if isinstance(value, list):
                points.extend(value)
            elif value:
                points.append(value)
    return compact_list(points, limit=limit)


def context_points(notes: list[dict[str, Any]], fields: tuple[str, ...], limit: int = 5) -> list[str]:
    points: list[str] = []
    for note in notes:
        for field in fields:
            value = note.get(field)
            if isinstance(value, list):
                points.extend(value)
            elif value:
                points.append(value)
    return compact_list(points, limit=limit)


def source_note_rows(notes: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for kind, label in (
        ("mda", "MD&A"),
        ("fsNotes", "FS Note"),
        ("calls", "Call"),
        ("filingSummary", "Filing Digest"),
        ("bizProfile", "Biz Profile"),
    ):
        for note in (notes.get(kind) or [])[:MAX_SOURCE_NOTES]:
            rows.append(
                {
                    "kind": label,
                    "title": clean_text(note.get("title"), 120),
                    "period": clean_text(note.get("period") or note.get("eventDate"), 40),
                    "sourcePath": clean_text(note.get("sourcePath"), 180),
                }
            )
    return rows[:16]


def recent_disclosures(disclosure_payload: dict[str, Any], ticker: str) -> list[dict[str, Any]]:
    filings = disclosure_payload.get("filings") or disclosure_payload.get("items") or []
    rows = [f for f in filings if str(f.get("tk") or "").upper() == ticker]
    rows.sort(key=lambda x: str(x.get("ts") or ""), reverse=True)
    return rows[:8]


def oppday_for(oppday_payload: dict[str, Any], ticker: str) -> dict[str, Any] | None:
    for row in oppday_payload.get("summaries") or []:
        if str(row.get("ticker") or "").upper() == ticker:
            return row
    return None


def build_context(
    ticker: dict[str, Any],
    notes: dict[str, list[dict[str, Any]]],
    disclosure_payload: dict[str, Any],
    oppday_payload: dict[str, Any],
) -> dict[str, Any]:
    highlights = ticker.get("highlights") or []
    latest = latest_period(highlights)
    fy, prev_fy = latest_full_year(highlights)
    disclosures = recent_disclosures(disclosure_payload, ticker["tk"])
    opp = oppday_for(oppday_payload, ticker["tk"])

    context = {
        "ticker": ticker["tk"],
        "name": ticker.get("name"),
        "sector": ticker.get("sector"),
        "segment": ticker.get("segment"),
        "rm": ticker.get("rm"),
        "businessType": ticker.get("businessType"),
        "website": ticker.get("website"),
        "market": {
            "last": ticker.get("last"),
            "pctYtd": ticker.get("pctYtd"),
            "pe": ticker.get("pe"),
            "pbv": ticker.get("pbv"),
            "dy": ticker.get("dy"),
            "mktcap": ticker.get("mktcap"),
            "atHi52": ticker.get("atHi52"),
            "atLo52": ticker.get("atLo52"),
        },
        "latestPeriod": latest,
        "latestFullYear": fy,
        "previousFullYear": prev_fy,
        "mda": [
            {
                "title": n.get("title"),
                "period": n.get("period"),
                "takeaway": (n.get("analysis") or {}).get("takeaway") or n.get("snippet"),
                "drivers": (n.get("analysis") or {}).get("drivers") or [],
                "risks": (n.get("analysis") or {}).get("risks") or [],
                "guidance": (n.get("analysis") or {}).get("guidance") or [],
                "sourcePath": n.get("sourcePath"),
            }
            for n in (notes.get("mda") or [])[:4]
        ],
        "fsNotes": [
            {
                "title": n.get("title"),
                "period": n.get("period"),
                "takeaway": (n.get("analysis") or {}).get("takeaway") or n.get("snippet"),
                "flags": (n.get("analysis") or {}).get("flags") or [],
                "risks": (n.get("analysis") or {}).get("risks") or [],
                "sourcePath": n.get("sourcePath"),
            }
            for n in (notes.get("fsNotes") or [])[:4]
        ],
        "calls": [
            {
                "title": n.get("title"),
                "period": n.get("period"),
                "takeaway": (n.get("analysis") or {}).get("takeaway") or n.get("snippet"),
                "guidance": (n.get("analysis") or {}).get("guidance") or [],
                "sourcePath": n.get("sourcePath"),
            }
            for n in (notes.get("calls") or [])[:3]
        ],
        "filingSummary": [
            {
                "title": n.get("title"),
                "period": n.get("period"),
                "snippet": n.get("snippet"),
                "flags": (n.get("analysis") or {}).get("flags") or [],
                "risks": (n.get("analysis") or {}).get("risks") or [],
                "sourcePath": n.get("sourcePath"),
            }
            for n in (notes.get("filingSummary") or [])[:3]
        ],
        "bizProfile": [
            {
                "title": n.get("title"),
                "snippet": n.get("snippet"),
                "sourcePath": n.get("sourcePath"),
            }
            for n in (notes.get("bizProfile") or [])[:1]
        ],
        "oppday": opp,
        "recentDisclosures": [
            {
                "ts": f.get("ts"),
                "severity": f.get("severity") or f.get("_classifier_raw"),
                "title": f.get("title") or f.get("headline"),
                "summary": f.get("_summary"),
                "url": f.get("url"),
            }
            for f in disclosures
        ],
    }
    return context


def source_hash(context: dict[str, Any]) -> str:
    raw = json.dumps(context, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def deterministic_report(context: dict[str, Any], generated: str) -> dict[str, Any]:
    tk = context["ticker"]
    name = context.get("name") or tk
    latest = context.get("latestPeriod") or {}
    fy = context.get("latestFullYear") or {}
    prev = context.get("previousFullYear") or {}
    market = context.get("market") or {}

    rev_chg = pct_change(fy.get("revenue"), prev.get("revenue"))
    np_chg = pct_change(fy.get("netProfit"), prev.get("netProfit"))
    latest_np = latest.get("netProfit")
    latest_npm = latest.get("npm")

    mda_points = context_points(context.get("mda") or [], ("takeaway", "drivers", "guidance", "risks"), 5)
    fs_flags = context_points(context.get("fsNotes") or [], ("flags", "risks", "takeaway"), 5)
    filing_flags = context_points(context.get("filingSummary") or [], ("flags", "risks", "snippet"), 5)
    biz_snippet = context_points(context.get("bizProfile") or [], ("snippet",), 1)
    call_points = context_points(context.get("calls") or [], ("takeaway", "guidance"), 4)

    high_disc = [
        clean_text(d.get("summary") or d.get("title"), 160)
        for d in context.get("recentDisclosures") or []
        if str(d.get("severity") or "").lower() in {"high", "critical", "medium", "material"}
    ]

    financial_snapshot = compact_list(
        [
            f"{period_label(latest)}: revenue {fmt_money_m(latest.get('revenue'))}, net profit {fmt_money_m(latest_np)}, NPM {fmt_num(latest_npm, '%')}.",
            f"FY {period_label(fy)}: revenue {fmt_money_m(fy.get('revenue'))} ({fmt_change(rev_chg)} YoY), net profit {fmt_money_m(fy.get('netProfit'))} ({fmt_change(np_chg)} YoY).",
            f"Balance sheet: D/E {fmt_num(latest.get('deRatio'), 'x', 2)}, current ratio {fmt_num(latest.get('currentRatio'), 'x', 2)}, operating CF {fmt_money_m(latest.get('netOperating'))}.",
            f"Market: price {fmt_num(market.get('last'), ' THB', 2)}, PE {fmt_num(market.get('pe'), 'x', 1)}, PBV {fmt_num(market.get('pbv'), 'x', 2)}, DY {fmt_num(market.get('dy'), '%', 2)}, YTD {fmt_num(market.get('pctYtd'), '%', 1)}.",
        ],
        limit=4,
        max_chars=220,
    )

    watch_items = compact_list(
        [
            *(fs_flags[:3]),
            *(filing_flags[:3]),
            *(high_disc[:3]),
            *([f"FY net profit declined {abs(np_chg):.1f}% YoY; confirm whether margin pressure is cyclical or structural."] if np_chg is not None and np_chg < -10 else []),
            *([f"Latest period NPM is {latest_npm:.1f}%; monitor gross margin and operating leverage."] if latest_npm is not None and latest_npm < 8 else []),
            *([f"Share price is down {abs(market.get('pctYtd')):.1f}% YTD; check whether fundamentals or liquidity explain the move."] if isinstance(market.get("pctYtd"), (int, float)) and market.get("pctYtd") < -15 else []),
        ],
        limit=5,
        max_chars=190,
    )

    questions = compact_list(
        [
            "What are the two biggest drivers management expects to move revenue and margin over the next two quarters?",
            "Which accounting note or related-party item needs explicit follow-up before the next meeting?",
            "What evidence would change the coverage stance from Watch/Neutral to Positive?",
            *(f"What changed behind: {item}" for item in watch_items[:2]),
        ],
        limit=5,
        max_chars=170,
    )

    tone = "Watch" if watch_items or (np_chg is not None and np_chg < -10) else "Positive" if np_chg and np_chg > 10 else "Neutral"
    thesis = (
        f"{name} is a {context.get('segment') or context.get('sector')} coverage name with "
        f"{fmt_money_m(latest.get('revenue'))} latest-period revenue and a {tone.lower()} setup; "
        "focus on the latest margin trend, cash conversion, and flagged filing notes."
    )

    summary_parts = [
        clean_text(context.get("businessType"), 220),
        financial_snapshot[0] if financial_snapshot else "",
        (mda_points[0] if mda_points else ""),
    ]

    return {
        "tk": tk,
        "name": name,
        "sector": context.get("sector"),
        "segment": context.get("segment"),
        "rm": context.get("rm"),
        "generated": generated,
        "model": "deterministic-draft",
        "tone": tone,
        "thesis": thesis,
        "summary": clean_text(" ".join(x for x in summary_parts if x), 520),
        "business": clean_text(context.get("businessType") or (biz_snippet[0] if biz_snippet else None), 360),
        "financialSnapshot": financial_snapshot,
        "mdaSynthesis": compact_list([*mda_points, *call_points], 6, 200),
        "fsNotesSynthesis": compact_list(fs_flags, 5, 200),
        "watchItems": watch_items,
        "questions": questions,
        "qualityFlags": [
            "Generated from compact dashboard and vault excerpts; verify primary filings before escalation.",
            "Use LLM mode with ANTHROPIC_API_KEY for richer narrative synthesis.",
        ],
        "sourceNotes": source_note_rows(
            {
                "mda": context.get("mda") or [],
                "fsNotes": context.get("fsNotes") or [],
                "calls": context.get("calls") or [],
                "filingSummary": context.get("filingSummary") or [],
                "bizProfile": context.get("bizProfile") or [],
            }
        ),
    }


def extract_json(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if stripped.startswith("{"):
        return json.loads(stripped)
    match = re.search(r"\{.*\}", stripped, re.S)
    if not match:
        raise ValueError("LLM response did not contain a JSON object")
    return json.loads(match.group(0))


def llm_report(context: dict[str, Any], generated: str, model: str) -> dict[str, Any]:
    try:
        import anthropic  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Install anthropic or run with --llm never") from exc

    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")

    system = (
        "You are an IS1 equity coverage analyst. Write concise, evidence-grounded "
        "company reports for SET-listed companies. Do not invent facts. If the "
        "source is weak, say what needs verification. Return JSON only."
    )
    schema = {
        "tone": "Positive | Neutral | Watch",
        "thesis": "one-line investment/coverage thesis",
        "summary": "120-180 word analyst summary",
        "business": "compact business description",
        "financialSnapshot": ["3-5 concrete financial observations"],
        "mdaSynthesis": ["3-6 MD&A/call synthesis points"],
        "fsNotesSynthesis": ["2-5 accounting/FS note points"],
        "watchItems": ["3-6 monitoring items or risks"],
        "questions": ["3-5 questions for next company contact"],
        "qualityFlags": ["data caveats and primary-source checks"],
    }
    prompt = (
        "Create a per-company analyst report from this context.\n\n"
        f"Required JSON schema:\n{json.dumps(schema, ensure_ascii=False, indent=2)}\n\n"
        "Context:\n"
        f"{json.dumps(context, ensure_ascii=False, indent=2, default=str)}"
    )
    client = anthropic.Anthropic(api_key=key)
    message = client.messages.create(
        model=model,
        max_tokens=2200,
        temperature=0.2,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "\n".join(block.text for block in message.content if getattr(block, "type", "") == "text")
    data = extract_json(text)
    base = deterministic_report(context, generated)
    base.update({k: data.get(k, base.get(k)) for k in data.keys()})
    base["model"] = model
    base["generated"] = generated
    return base


def markdown_report(report: dict[str, Any], context_hash: str) -> str:
    def bullets(items: list[Any]) -> str:
        vals = compact_list(items, limit=12, max_chars=260)
        return "\n".join(f"- {v}" for v in vals) if vals else "- n/a"

    sources = report.get("sourceNotes") or []
    source_lines = [
        f"- {s.get('kind', 'Source')}: {s.get('title') or 'Untitled'}"
        + (f" ({s.get('period')})" if s.get("period") else "")
        + (f" - `{s.get('sourcePath')}`" if s.get("sourcePath") else "")
        for s in sources
    ]
    source_block = "\n".join(source_lines) if source_lines else "- n/a"
    generated = report.get("generated") or dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    frontmatter = textwrap.dedent(
        f"""\
        ---
        ticker: {report.get('tk')}
        sector: {report.get('sector') or ''}
        segment: {report.get('segment') or ''}
        rm: {report.get('rm') or ''}
        source_type: ai-generated-company-report
        generated_at: {generated}
        model: {report.get('model') or ''}
        source_hash: {context_hash}
        dashboard_json: data/company-reports.json
        ---
        """
    )
    body = f"""
# {report.get('tk')} - Company Report

> Thesis: {clean_text(report.get('thesis'), 500)}

## Executive read
{clean_text(report.get('summary'), 1000)}

## Business
{clean_text(report.get('business'), 800) or 'n/a'}

## Financial snapshot
{bullets(report.get('financialSnapshot') or [])}

## MD&A and call synthesis
{bullets(report.get('mdaSynthesis') or [])}

## Financial statement notes
{bullets(report.get('fsNotesSynthesis') or [])}

## Watch items
{bullets(report.get('watchItems') or [])}

## Questions for next contact
{bullets(report.get('questions') or [])}

## Data quality
{bullets(report.get('qualityFlags') or [])}

## Source notes
{source_block}
"""
    return frontmatter + body.lstrip()


def candidate_vault_roots() -> list[Path]:
    roots = []
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


def find_listed_root() -> Path | None:
    for root in candidate_vault_roots():
        listed = root / LISTED_SUBPATH
        if listed.is_dir():
            return listed
    return None


def report_path(listed_root: Path, report: dict[str, Any]) -> Path:
    sector = clean_text(report.get("sector") or "OTHER").replace("&", "").replace("/", "-")
    return listed_root / REPORT_SUBPATH / sector / f"{report['tk']}.md"


def relative_vault_path(path: Path, listed_root: Path) -> str:
    try:
        return str(path.relative_to(listed_root)).replace("\\", "/")
    except ValueError:
        return str(path)


def build_reports(args: argparse.Namespace) -> dict[str, Any]:
    summary = load_json(TICKER_SUMMARY, {})
    tickers = summary.get("tickers") or []
    notes_payload = load_json(VAULT_NOTES, {})
    notes_map = notes_payload.get("tickers") or {}
    disclosure_payload = load_json(DISCLOSURES, {})
    oppday_payload = load_json(OPPDAY, {})
    existing = load_json(OUT, {}).get("reports") or {}
    listed_root = find_listed_root() if args.write_vault else None

    wanted = {t.upper() for t in args.ticker} if args.ticker else None
    selected = [t for t in tickers if wanted is None or t.get("tk", "").upper() in wanted]
    if args.limit:
        selected = selected[: args.limit]

    generated = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    reports: dict[str, Any] = dict(existing) if (wanted is not None or args.limit) else {}
    errors: list[dict[str, str]] = []
    llm_used = False

    for ticker in selected:
        tk = ticker["tk"].upper()
        context = build_context(ticker, notes_map.get(tk) or {}, disclosure_payload, oppday_payload)
        h = source_hash(context)
        old = existing.get(tk)
        if old and old.get("sourceHash") == h and not args.force:
            reports[tk] = old
            continue
        try:
            use_llm = args.llm == "always" or (args.llm == "auto" and os.environ.get("ANTHROPIC_API_KEY"))
            if use_llm:
                report = llm_report(context, generated, args.model)
                llm_used = True
            else:
                report = deterministic_report(context, generated)
        except Exception as exc:
            if args.llm == "always":
                raise
            errors.append({"ticker": tk, "error": str(exc)})
            report = deterministic_report(context, generated)

        report["sourceHash"] = h
        if listed_root:
            out_path = report_path(listed_root, report)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(markdown_report(report, h), encoding="utf-8")
            report["vaultPath"] = relative_vault_path(out_path, listed_root)
        reports[tk] = report

    if wanted:
        missing = sorted(wanted - set(reports))
        for tk in missing:
            errors.append({"ticker": tk, "error": "ticker not found in data/ticker-summary.json"})

    payload = {
        "generated": generated,
        "source": "ticker-summary.json + vault-ticker-notes.json + disclosure-pulse.json",
        "model": args.model if llm_used else "deterministic-draft",
        "vaultRoot": relative_vault_path(listed_root, listed_root) if listed_root else "",
        "totals": {
            "reports": len(reports),
            "llm": llm_used,
            "errors": len(errors),
        },
        "errors": errors,
        "reports": dict(sorted(reports.items())),
    }
    return payload


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ticker", action="append", default=[], help="Ticker to build. Repeatable.")
    parser.add_argument("--all", action="store_true", help="Build all tickers.")
    parser.add_argument("--limit", type=int, default=0, help="Limit selected tickers for test runs.")
    parser.add_argument("--llm", choices=["auto", "always", "never"], default="auto")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--force", action="store_true", help="Regenerate even if source hash is unchanged.")
    parser.add_argument("--no-write-vault", dest="write_vault", action="store_false")
    parser.set_defaults(write_vault=True)
    args = parser.parse_args(argv)
    if not args.all and not args.ticker:
        parser.error("Use --all or at least one --ticker.")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    payload = build_reports(args)
    write_json(OUT, payload)
    print(f"Wrote {OUT}: {payload['totals']}")
    if payload.get("errors"):
        print(json.dumps(payload["errors"][:5], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
