"""Build analyst-style company reports for ticker-summary.html.

This local agent reads dashboard company data plus compact Obsidian excerpts,
creates one per-ticker report, saves Markdown back to the Obsidian vault, and
writes data/company-reports.json for the static dashboard.

LLM use is optional:
  - default auto mode uses Anthropic only when ANTHROPIC_API_KEY is set
  - --llm never produces deterministic drafts for wiring/tests
  - --llm always fails fast if the key or package is unavailable

Deep mode (--deep) reads the FULL vault sources per ticker (MD&A, FS-note and
auditor extracts, quarterly health check, earnings calls, coverage + triage
notes) instead of 520-char snippets, and asks for an IS1-grade schema:
6-Theme view, HIGH/MED/LOW surveillance flags, RPT/MT watch.

Agent-agnostic path: --dump-context writes the per-ticker context bundle so an
external agent (Claude Code, JARVIS, Codex) can author the report JSON, then
--inject applies it to the vault note + data/company-reports.json. Deep/injected
reports are protected from being overwritten by shallow stub runs (use --force).

Run examples:
  python scripts/build_company_reports.py --ticker AAI
  python scripts/build_company_reports.py --all --llm auto
  python scripts/build_company_reports.py --ticker TU --deep --llm always
  python scripts/build_company_reports.py --ticker TU --deep --dump-context /tmp/ctx
  python scripts/build_company_reports.py --inject /tmp/ctx/TU-report.json
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

DEFAULT_MODEL = os.environ.get("COMPANY_REPORT_MODEL", "claude-sonnet-4-6")
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
    for kind, label in (("mda", "MD&A"), ("fsNotes", "FS Note"), ("calls", "Call")):
        for note in (notes.get(kind) or [])[:MAX_SOURCE_NOTES]:
            rows.append(
                {
                    "kind": label,
                    "title": clean_text(note.get("title"), 120),
                    "period": clean_text(note.get("period") or note.get("eventDate"), 40),
                    "sourcePath": clean_text(note.get("sourcePath"), 180),
                }
            )
    return rows[:10]


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


# --- Deep source collection (full vault notes, not snippets) -----------------

PERIOD_RE = re.compile(r"_(\d{4})(Q[1-4]|FY)_([ET])\.md$")

# subfolder under 1-Raw/01-Filings, periods to include, char budget per bucket
DEEP_FILING_SPEC = {
    "mda": ("MDA", 2, 30000),
    "fsNotes": ("FS-NOTES", 1, 45000),
    "auditor": ("AUDITOR", 2, 9000),
}


def read_clip(path: Path, budget: int, listed_root: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return {
        "sourcePath": relative_vault_path(path, listed_root),
        "chars": len(text),
        "truncated": len(text) > budget,
        "text": text[:budget],
    }


def pick_filings(folder: Path, periods: int) -> list[Path]:
    """Latest N filing periods for a ticker; prefer the English extract when both languages exist."""
    if not folder.is_dir():
        return []
    by_period: dict[tuple[str, str], dict[str, Path]] = {}
    for f in folder.glob("*.md"):
        m = PERIOD_RE.search(f.name)
        if not m:
            continue
        year, q, lang = m.groups()
        by_period.setdefault((year, "Q9" if q == "FY" else q), {})[lang] = f
    ordered = sorted(by_period.items(), key=lambda kv: kv[0], reverse=True)
    return [langs.get("E") or langs.get("T") for _, langs in ordered[:periods]]


def collect_deep_sources(listed_root: Path, tk: str, sector: str) -> dict[str, Any]:
    """Full-text vault sources for one ticker, clipped to per-bucket budgets."""
    deep: dict[str, Any] = {}
    for key, (sub, periods, budget) in DEEP_FILING_SPEC.items():
        files = pick_filings(listed_root / "1-Raw" / "01-Filings" / sub / tk, periods)
        per_file = budget // max(len(files), 1)
        deep[key] = [read_clip(f, per_file, listed_root) for f in files]

    analysis = listed_root / "2-Analysis" / "AI-Generated"
    hc_files = sorted((analysis / "02-Health Check Log").glob(f"*/{tk}.md"))
    deep["healthCheck"] = [read_clip(hc_files[-1], 26000, listed_root)] if hc_files else []

    calls_dir = analysis / "03-Earning Calls" / tk
    calls = sorted(calls_dir.glob("OPPDAY-*.md"))[-2:] if calls_dir.is_dir() else []
    deep["earningCalls"] = [read_clip(f, 11000, listed_root) for f in calls]

    sector_folder = clean_text(sector or "OTHER").replace("&", "").replace("/", "-")
    cov = analysis / "04-Coverage" / sector_folder / f"{tk}.md"
    deep["coverageNote"] = [read_clip(cov, 14000, listed_root)] if cov.exists() else []

    nb = analysis / "01-NotebookLM Snapshots" / f"{tk}.md"
    deep["notebookSnapshot"] = [read_clip(nb, 8000, listed_root)] if nb.exists() else []

    # {TK}-{TOPIC}-YYYY-MM-DD.md only; the single-alpha-segment rule avoids
    # cross-matching hyphenated sibling tickers (TU- must not pick up TU-PF-*).
    inbox = analysis / "06-Inbox"
    triage_re = re.compile(rf"^{re.escape(tk)}-[A-Za-z]+-\d{{4}}-\d{{2}}-\d{{2}}")
    triage = sorted(f for f in inbox.glob(f"{tk}-*.md") if triage_re.match(f.name))[-3:] if inbox.is_dir() else []
    deep["inboxTriage"] = [read_clip(f, 8000, listed_root) for f in triage]
    return deep


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
        "business": clean_text(context.get("businessType"), 360),
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


def report_schema(deep: bool) -> dict[str, Any]:
    schema: dict[str, Any] = {
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
    if deep:
        schema.update(
            {
                "sixThemes": {
                    "preCb": "Pre-CB signals: going-concern, D/E covenants, equity erosion (1-3 sentences)",
                    "salesQuality": "revenue recognition quality, channel/customer concentration",
                    "costMargin": "gross/operating margin trend and drivers",
                    "workingCapital": "receivables/inventory/payables cycle and red flags",
                    "cashFunding": "operating CF vs profit, funding needs, maturities",
                    "outlook": "management guidance vs evidence",
                },
                "surveillanceFlags": [
                    {
                        "severity": "HIGH | MED | LOW",
                        "item": "what was found",
                        "evidence": "the specific number/statement supporting it",
                        "sourcePath": "vault path of the source note",
                    }
                ],
                "rptMtWatch": ["related-party / material-transaction items to monitor (ทจ. 45-46/2568 lens)"],
            }
        )
    return schema


def llm_report(context: dict[str, Any], generated: str, model: str) -> dict[str, Any]:
    try:
        import anthropic  # type: ignore
    except ImportError as exc:
        raise RuntimeError("Install anthropic or run with --llm never") from exc

    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set")

    deep = bool(context.get("deepSources"))
    system = (
        "You are an IS1 equity coverage analyst at the Stock Exchange of Thailand. "
        "Write concise, evidence-grounded company reports for SET-listed companies. "
        "Do not invent facts. Pin every claim to a source path or filing from the "
        "context; if the source is weak, say what needs verification. Lead with red "
        "flags, never bury them. Return JSON only."
    )
    schema = report_schema(deep)
    prompt = (
        "Create a per-company analyst report from this context."
        + (
            " The deepSources field contains full vault notes (MD&A, FS notes, auditor"
            " report, quarterly health check, earnings calls, coverage and triage"
            " notes) - base the report on those primary texts, using the compact"
            " fields only as a cross-check.\n\n"
            if deep
            else "\n\n"
        )
        + f"Required JSON schema:\n{json.dumps(schema, ensure_ascii=False, indent=2)}\n\n"
        "Context:\n"
        f"{json.dumps(context, ensure_ascii=False, indent=2, default=str)}"
    )
    client = anthropic.Anthropic(api_key=key)
    message = client.messages.create(
        model=model,
        max_tokens=6000 if deep else 2200,
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
    if deep:
        base["deep"] = True
        base["sourceNotes"] = deep_source_rows(context["deepSources"])
    return base


DEEP_KIND_LABELS = {
    "mda": "MD&A",
    "fsNotes": "FS Note",
    "auditor": "Auditor",
    "healthCheck": "Health Check",
    "earningCalls": "Call",
    "coverageNote": "Coverage",
    "notebookSnapshot": "NotebookLM",
    "inboxTriage": "Triage",
}


def deep_source_rows(deep: dict[str, Any]) -> list[dict[str, str]]:
    rows = []
    for kind, items in deep.items():
        for item in items or []:
            rows.append(
                {
                    "kind": DEEP_KIND_LABELS.get(kind, kind),
                    "title": Path(item.get("sourcePath", "")).name,
                    "period": "",
                    "sourcePath": item.get("sourcePath", ""),
                }
            )
    return rows


def markdown_report(report: dict[str, Any], context_hash: str) -> str:
    def bullets(items: list[Any]) -> str:
        vals = compact_list(items, limit=12, max_chars=420)
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
    is_stub = (report.get("model") or "") == "deterministic-draft"
    # Vault provenance convention (AI OS/vault-map.md): source_type must be one of
    # raw|manual-analysis|ai-generated|deliverable, with generated_by alongside.
    frontmatter = textwrap.dedent(
        f"""\
        ---
        ticker: {report.get('tk')}
        sector: {report.get('sector') or ''}
        segment: {report.get('segment') or ''}
        rm: {report.get('rm') or ''}
        source_type: ai-generated
        generated_by: {report.get('generatedBy') or 'codex'}
        report_type: company-report
        status: {'stub' if is_stub else 'full'}
        generated_at: {generated}
        model: {report.get('model') or ''}
        source_hash: {context_hash}
        dashboard_json: data/company-reports.json
        tags: [company-report]
        ---
        """
    )
    stub_callout = (
        "\n> [!warning] Auto-generated stub (deterministic draft)\n"
        "> Not analyst-reviewed and may lack current-quarter sources. "
        "Verify against `1-Raw/01-Filings/` before citing in any deliverable.\n"
        if is_stub
        else ""
    )
    six = report.get("sixThemes") or {}
    theme_labels = [
        ("preCb", "Pre-CB"),
        ("salesQuality", "Sales Quality"),
        ("costMargin", "Cost & Margin"),
        ("workingCapital", "Working Capital"),
        ("cashFunding", "Cash & Funding"),
        ("outlook", "Outlook"),
    ]
    six_block = "\n".join(f"- **{label}** — {clean_text(six.get(key), 420)}" for key, label in theme_labels if six.get(key))
    flags = report.get("surveillanceFlags") or []
    flag_block = "\n".join(
        f"- **{clean_text(f.get('severity'), 8).upper()}** — {clean_text(f.get('item'), 240)} "
        f"— {clean_text(f.get('evidence'), 460)}"
        + (f" (`{clean_text(f.get('sourcePath'), 180)}`)" if f.get("sourcePath") else "")
        for f in flags
    )
    rpt_block = "\n".join(f"- {clean_text(x, 280)}" for x in (report.get("rptMtWatch") or []))
    deep_sections = ""
    if six_block:
        deep_sections += f"\n## 6-Theme view\n{six_block}\n"
    if flag_block:
        deep_sections += f"\n## Surveillance flags\n{flag_block}\n"
    if rpt_block:
        deep_sections += f"\n## RPT / MT watch\n{rpt_block}\n"
    body = f"""
# {report.get('tk')} - Company Report
{stub_callout}
> Thesis: {clean_text(report.get('thesis'), 500)}

## Executive read
{clean_text(report.get('summary'), 2000)}

## Business
{clean_text(report.get('business'), 800) or 'n/a'}

## Financial snapshot
{bullets(report.get('financialSnapshot') or [])}

## MD&A and call synthesis
{bullets(report.get('mdaSynthesis') or [])}

## Financial statement notes
{bullets(report.get('fsNotesSynthesis') or [])}
{deep_sections}
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
    vault_listed = find_listed_root()
    if (args.deep or args.dump_context) and not vault_listed:
        raise RuntimeError("--deep/--dump-context need the Obsidian vault; set VAULT_ROOT")

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
        if (args.deep or args.dump_context) and vault_listed:
            context["deepSources"] = collect_deep_sources(vault_listed, tk, ticker.get("sector") or "")
        h = source_hash(context)
        if args.dump_context:
            dump_dir = Path(args.dump_context)
            dump_dir.mkdir(parents=True, exist_ok=True)
            write_json(dump_dir / f"{tk}-context.json", {"sourceHash": h, "context": context})
            print(f"Dumped {tk} context -> {dump_dir / f'{tk}-context.json'}")
            continue
        old = existing.get(tk)
        if old and old.get("sourceHash") == h and not args.force:
            reports[tk] = old
            continue
        # never let a shallow/stub run overwrite a deep report — only --force or
        # another deep run may replace it
        if old and old.get("deep") and not args.deep and not args.force:
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
    parser.add_argument(
        "--deep",
        action="store_true",
        help="Read full vault sources (MD&A, FS notes, auditor, health check, calls, coverage, triage) into the LLM context.",
    )
    parser.add_argument(
        "--dump-context",
        default="",
        help="Write per-ticker context JSON to this directory and exit without generating reports. "
        "Lets an external agent (Claude Code, JARVIS, Codex) author the report, then apply it with --inject.",
    )
    parser.add_argument(
        "--inject",
        default="",
        help="Path to a report JSON authored by an external agent (single report object or a list). "
        "Writes the vault note and the company-reports.json entry.",
    )
    parser.set_defaults(write_vault=True)
    args = parser.parse_args(argv)
    if not args.all and not args.ticker and not args.inject:
        parser.error("Use --all, at least one --ticker, or --inject.")
    return args


REQUIRED_INJECT_KEYS = ("tk", "thesis", "summary")


def inject_reports(args: argparse.Namespace) -> dict[str, Any]:
    """Apply externally authored report JSON: vault note + dashboard database entry."""
    raw = load_json(Path(args.inject), None)
    if raw is None:
        raise RuntimeError(f"Cannot read {args.inject}")
    incoming = raw if isinstance(raw, list) else [raw]
    payload = load_json(OUT, {})
    reports = payload.get("reports") or {}
    listed_root = find_listed_root() if args.write_vault else None
    generated = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

    for report in incoming:
        missing = [k for k in REQUIRED_INJECT_KEYS if not report.get(k)]
        if missing:
            raise RuntimeError(f"Injected report missing keys: {missing}")
        tk = str(report["tk"]).upper()
        report["tk"] = tk
        report.setdefault("generated", generated)
        report.setdefault("model", "external-agent")
        report.setdefault("deep", True)
        report.setdefault("sourceHash", "injected")
        if listed_root:
            out_path = report_path(listed_root, report)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(markdown_report(report, report["sourceHash"]), encoding="utf-8")
            report["vaultPath"] = relative_vault_path(out_path, listed_root)
        reports[tk] = report
        print(f"Injected {tk} ({report.get('model')})" + (f" -> {report.get('vaultPath')}" if report.get("vaultPath") else ""))

    payload["generated"] = generated
    payload["reports"] = dict(sorted(reports.items()))
    payload.setdefault("totals", {})["reports"] = len(reports)
    return payload


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.inject:
        payload = inject_reports(args)
        write_json(OUT, payload)
        print(f"Wrote {OUT}: {payload['totals']}")
        return 0
    payload = build_reports(args)
    if args.dump_context:
        return 0
    write_json(OUT, payload)
    print(f"Wrote {OUT}: {payload['totals']}")
    if payload.get("errors"):
        print(json.dumps(payload["errors"][:5], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
