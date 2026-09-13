#!/usr/bin/env python3
"""Build the 6M26 company / segment / sector panels for the Sector Review deck.

Reads the Q2/2026 MD&A markdown the harvest wrote into the Obsidian vault, runs
the reconciling extractor in ``extract_6m26_figures``, and emits the same three
CSV surfaces the FY2025 audited snapshot provides, plus PROVENANCE and
QA_SUMMARY files.

The FY2025 company CSV is required: it is the authoritative 118-company
perimeter and segment mapping, and its FY totals are used as an order-of-
magnitude check on each extracted half-year figure.

Panel discipline mirrors the FY build. A company enters the RFO panel only when
its 6M26 and 6M25 revenue both reconcile, and the NPAT panel only when owner
NPAT reconciles; margin is computed strictly on the intersection. Every
excluded company carries a reason, and every included figure carries the label
and source line it came from, so any number in the deck can be traced back to a
line of a filing.

Usage:
    python scripts/build_6m26_panel.py \
        --vault-root "$VAULT/Work-SET/Listed Company" \
        --fy-company-csv .../food_prop_company_fy2024_2025_audited_2026-08-07.csv \
        --out-dir .../data/6m26-<date> \
        --as-of 2026-08-17
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from extract_6m26_figures import CompanyExtract, extract_company  # noqa: E402

PERIOD = "2026Q2"
MDA_SUBPATH = Path("1-Raw") / "01-Filings" / "MDA"

# A half year that lands outside this share of the audited full year means the
# extractor latched onto the wrong row or the wrong scale. Wide on purpose:
# genuinely seasonal issuers exist, and this is a blunder detector, not a
# forecast check.
FY_SHARE_FLOOR_PCT = 20.0
FY_SHARE_CEILING_PCT = 85.0


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def number(value) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result


def yoy_pct(prior: float | None, current: float | None) -> float | None:
    """YoY only on a positive base — matching the FY panel's convention."""
    if prior is None or current is None or prior <= 0:
        return None
    return (current - prior) / prior * 100.0


def npat_state(prior: float | None, current: float | None) -> str:
    if prior is None or current is None:
        return "unknown"
    if prior > 0 and current > 0:
        return "profit_increased" if current >= prior else "profit_decreased"
    if prior > 0 >= current:
        return "turned_to_loss"
    if prior <= 0 < current:
        return "turned_to_profit"
    return "loss_narrowed" if current >= prior else "loss_widened"


@dataclass
class CompanyRow:
    ticker: str
    sector: str
    segment: str
    extract: CompanyExtract | None = None
    source_path: str = ""
    source_sha256: str = ""
    fy2025_rfo_mb: float | None = None
    # Blocks the company from *both* panels (no filing, or a figure that failed
    # the plausibility band). A measure that simply did not reconcile blocks only
    # its own panel — the FY build likewise keeps RFO and NPAT coverage
    # independent, so a company can be in one and not the other.
    blocking_exclusion: str = ""
    checks: list[str] = field(default_factory=list)

    @property
    def rfo_prior(self) -> float | None:
        return self.extract.rfo.prior if self.extract else None

    @property
    def rfo_current(self) -> float | None:
        return self.extract.rfo.current if self.extract else None

    @property
    def npat_prior(self) -> float | None:
        return self.extract.npat.prior if self.extract else None

    @property
    def npat_current(self) -> float | None:
        return self.extract.npat.current if self.extract else None

    @property
    def in_rfo_panel(self) -> bool:
        return bool(self.extract and self.extract.rfo.verified and not self.blocking_exclusion)

    @property
    def in_npat_panel(self) -> bool:
        return bool(self.extract and self.extract.npat.verified and not self.blocking_exclusion)

    @property
    def in_margin_panel(self) -> bool:
        return self.in_rfo_panel and self.in_npat_panel

    @property
    def exclusion_reason(self) -> str:
        """Why this company misses a panel — blocking reason, else per-measure."""
        if self.blocking_exclusion:
            return self.blocking_exclusion
        if not self.extract:
            return ""
        parts = []
        if not self.in_rfo_panel:
            parts.append(f"rfo: {self.extract.rfo.reason}")
        if not self.in_npat_panel:
            parts.append(f"npat: {self.extract.npat.reason}")
        return "; ".join(parts)


def load_universe(fy_company_csv: Path) -> list[CompanyRow]:
    """Read the audited FY perimeter: tickers, their segment, and FY2025 RFO."""
    rows: list[CompanyRow] = []
    with fy_company_csv.open(encoding="utf-8-sig", newline="") as handle:
        for record in csv.DictReader(handle):
            rows.append(CompanyRow(
                ticker=record["ticker"],
                sector=record.get("sector", ""),
                segment=record["primary_segment_code"],
                fy2025_rfo_mb=number(record.get("fy2025_rfo_mb")),
            ))
    return rows


def find_mda(vault_root: Path, ticker: str) -> Path | None:
    """Prefer the English Q2/2026 MD&A; fall back to the Thai filing."""
    folder = vault_root / MDA_SUBPATH / ticker
    if not folder.is_dir():
        return None
    for language in ("E", "T"):
        candidate = folder / f"MDA_{ticker}_{PERIOD}_{language}.md"
        if candidate.is_file():
            return candidate
    matches = sorted(folder.glob(f"MDA_{ticker}_{PERIOD}_*.md"))
    return matches[0] if matches else None


def apply_fy_share_check(row: CompanyRow) -> None:
    """Flag a half-year revenue that is implausible against the audited FY."""
    if not (row.extract and row.extract.rfo.verified):
        return
    if not row.fy2025_rfo_mb or row.fy2025_rfo_mb <= 0 or row.rfo_current is None:
        return
    share = row.rfo_current / row.fy2025_rfo_mb * 100.0
    row.checks.append(f"6M26 RFO is {share:.1f}% of FY2025 RFO")
    if not (FY_SHARE_FLOOR_PCT <= share <= FY_SHARE_CEILING_PCT):
        row.blocking_exclusion = (
            f"6M26 RFO is {share:.1f}% of audited FY2025 RFO, outside the "
            f"{FY_SHARE_FLOOR_PCT:.0f}-{FY_SHARE_CEILING_PCT:.0f}% plausibility band")


def build_company_rows(vault_root: Path, universe: list[CompanyRow]) -> list[CompanyRow]:
    for row in universe:
        path = find_mda(vault_root, row.ticker)
        if path is None:
            row.blocking_exclusion = f"no {PERIOD} MD&A in the vault"
            continue
        row.source_path = str(path.relative_to(vault_root)).replace("\\", "/")
        row.source_sha256 = sha256_file(path)
        row.extract = extract_company(row.ticker, path.read_text(encoding="utf-8", errors="replace"))
        row.checks.extend(row.extract.checks)
        apply_fy_share_check(row)
    return universe


COMPANY_FIELDS = [
    "ticker", "sector", "primary_segment_code",
    "rfo_6m25_mb", "rfo_6m26_mb", "rfo_change_mb", "rfo_yoy_pct",
    "npat_owners_6m25_mb", "npat_owners_6m26_mb", "npat_change_mb",
    "npat_yoy_pct_positive_base_only", "npat_state", "net_margin_6m26_pct",
    "rfo_panel_included", "npat_panel_included", "margin_panel_included",
    "panel_exclusion_reason",
    "rfo_basis", "rfo_label", "rfo_derivation", "rfo_evidence",
    "npat_basis", "npat_label", "npat_evidence",
    "npat_unattributed_6m26_mb", "npat_unattributed_basis",
    "fy2025_rfo_mb", "half_year_share_of_fy2025_pct",
    "extraction_checks", "source_path", "source_sha256",
]


def company_record(row: CompanyRow) -> dict:
    extract = row.extract
    rfo_change = (row.rfo_current - row.rfo_prior) if row.in_rfo_panel else None
    npat_change = (row.npat_current - row.npat_prior) if row.in_npat_panel else None
    margin = None
    if row.in_margin_panel and row.rfo_current:
        margin = row.npat_current / row.rfo_current * 100.0
    share = None
    if row.fy2025_rfo_mb and row.rfo_current is not None and row.fy2025_rfo_mb > 0:
        share = row.rfo_current / row.fy2025_rfo_mb * 100.0
    unattributed = extract.npat_unattributed if extract else None
    return {
        "ticker": row.ticker, "sector": row.sector, "primary_segment_code": row.segment,
        "rfo_6m25_mb": row.rfo_prior if row.in_rfo_panel else None,
        "rfo_6m26_mb": row.rfo_current if row.in_rfo_panel else None,
        "rfo_change_mb": rfo_change,
        "rfo_yoy_pct": yoy_pct(row.rfo_prior, row.rfo_current) if row.in_rfo_panel else None,
        "npat_owners_6m25_mb": row.npat_prior if row.in_npat_panel else None,
        "npat_owners_6m26_mb": row.npat_current if row.in_npat_panel else None,
        "npat_change_mb": npat_change,
        "npat_yoy_pct_positive_base_only": (yoy_pct(row.npat_prior, row.npat_current)
                                            if row.in_npat_panel else None),
        "npat_state": npat_state(row.npat_prior, row.npat_current) if row.in_npat_panel else "",
        "net_margin_6m26_pct": margin,
        "rfo_panel_included": "yes" if row.in_rfo_panel else "no",
        "npat_panel_included": "yes" if row.in_npat_panel else "no",
        "margin_panel_included": "yes" if row.in_margin_panel else "no",
        "panel_exclusion_reason": row.exclusion_reason,
        "rfo_basis": extract.rfo.measure if extract else "",
        "rfo_label": extract.rfo.label if extract else "",
        "rfo_derivation": extract.rfo.derivation if extract else "",
        "rfo_evidence": extract.rfo.evidence if extract else "",
        "npat_basis": extract.npat.measure if extract else "",
        "npat_label": extract.npat.label if extract else "",
        "npat_evidence": extract.npat.evidence if extract else "",
        "npat_unattributed_6m26_mb": (unattributed.current
                                      if unattributed and unattributed.verified else None),
        "npat_unattributed_basis": (unattributed.measure
                                    if unattributed and unattributed.verified else ""),
        "fy2025_rfo_mb": row.fy2025_rfo_mb,
        "half_year_share_of_fy2025_pct": share,
        "extraction_checks": " | ".join(row.checks),
        "source_path": row.source_path, "source_sha256": row.source_sha256,
    }


SEGMENT_FIELDS = [
    "sector", "primary_segment_code", "universe_company_count", "universe_tickers",
    "rfo_panel_company_count", "rfo_panel_tickers", "rfo_panel_excluded_tickers",
    "npat_panel_company_count", "npat_panel_tickers", "npat_panel_excluded_tickers",
    "margin_panel_company_count", "margin_panel_tickers",
    "rfo_6m25_mb", "rfo_6m26_mb", "rfo_yoy_pct",
    "npat_owners_6m25_mb", "npat_owners_6m26_mb", "npat_change_mb",
    "npat_yoy_pct_positive_base_only", "npat_state",
    "net_margin_6m25_pct_comparable", "net_margin_6m26_pct_comparable",
    "rfo_direction_driver", "rfo_direction_driver_change_mb",
    "npat_direction_driver", "npat_direction_driver_change_mb",
]


def _aggregate(rows: list[CompanyRow], key: str) -> dict:
    """Aggregate one segment or sector from its member companies."""
    universe = [row.ticker for row in rows]
    rfo_panel = [row for row in rows if row.in_rfo_panel]
    npat_panel = [row for row in rows if row.in_npat_panel]
    margin_panel = [row for row in rows if row.in_margin_panel]

    rfo_prior = sum(row.rfo_prior for row in rfo_panel) if rfo_panel else None
    rfo_current = sum(row.rfo_current for row in rfo_panel) if rfo_panel else None
    npat_prior = sum(row.npat_prior for row in npat_panel) if npat_panel else None
    npat_current = sum(row.npat_current for row in npat_panel) if npat_panel else None

    margin_prior = margin_current = None
    if margin_panel:
        margin_rfo_prior = sum(row.rfo_prior for row in margin_panel)
        margin_rfo_current = sum(row.rfo_current for row in margin_panel)
        if margin_rfo_prior:
            margin_prior = sum(row.npat_prior for row in margin_panel) / margin_rfo_prior * 100.0
        if margin_rfo_current:
            margin_current = sum(row.npat_current for row in margin_panel) / margin_rfo_current * 100.0

    rfo_driver = max(rfo_panel, key=lambda r: abs(r.rfo_current - r.rfo_prior), default=None)
    npat_driver = max(npat_panel, key=lambda r: abs(r.npat_current - r.npat_prior), default=None)

    return {
        key: rows[0].segment if key == "primary_segment_code" else rows[0].sector,
        "universe_company_count": len(rows), "universe_tickers": ";".join(universe),
        "rfo_panel_company_count": len(rfo_panel),
        "rfo_panel_tickers": ";".join(row.ticker for row in rfo_panel),
        "rfo_panel_excluded_tickers": ";".join(row.ticker for row in rows if not row.in_rfo_panel),
        "npat_panel_company_count": len(npat_panel),
        "npat_panel_tickers": ";".join(row.ticker for row in npat_panel),
        "npat_panel_excluded_tickers": ";".join(row.ticker for row in rows if not row.in_npat_panel),
        "margin_panel_company_count": len(margin_panel),
        "margin_panel_tickers": ";".join(row.ticker for row in margin_panel),
        "rfo_6m25_mb": rfo_prior, "rfo_6m26_mb": rfo_current,
        "rfo_yoy_pct": yoy_pct(rfo_prior, rfo_current),
        "npat_owners_6m25_mb": npat_prior, "npat_owners_6m26_mb": npat_current,
        "npat_change_mb": (npat_current - npat_prior) if npat_panel else None,
        "npat_yoy_pct_positive_base_only": yoy_pct(npat_prior, npat_current),
        "npat_state": npat_state(npat_prior, npat_current) if npat_panel else "",
        "net_margin_6m25_pct_comparable": margin_prior,
        "net_margin_6m26_pct_comparable": margin_current,
        "rfo_direction_driver": rfo_driver.ticker if rfo_driver else "",
        "rfo_direction_driver_change_mb": (rfo_driver.rfo_current - rfo_driver.rfo_prior) if rfo_driver else None,
        "npat_direction_driver": npat_driver.ticker if npat_driver else "",
        "npat_direction_driver_change_mb": (npat_driver.npat_current - npat_driver.npat_prior) if npat_driver else None,
    }


def build_segments(rows: list[CompanyRow]) -> list[dict]:
    segments: dict[str, list[CompanyRow]] = {}
    for row in rows:
        segments.setdefault(row.segment, []).append(row)
    output = []
    for code in sorted(segments):
        record = _aggregate(segments[code], "primary_segment_code")
        record["sector"] = segments[code][0].sector
        record["primary_segment_code"] = code
        output.append(record)
    return output


def build_sectors(rows: list[CompanyRow]) -> list[dict]:
    sectors: dict[str, list[CompanyRow]] = {}
    for row in rows:
        sectors.setdefault(row.sector, []).append(row)
    output = []
    for sector in sorted(sectors):
        record = _aggregate(sectors[sector], "sector")
        record["sector"] = sector
        record.pop("primary_segment_code", None)
        output.append(record)
    return output


def run_qa(rows: list[CompanyRow], segments: list[dict], sectors: list[dict]) -> dict:
    """Structural checks. Any failure blocks the panel from being published."""
    checks: list[dict] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"check": name, "result": "pass" if ok else "fail", "detail": detail})

    for row in rows:
        if row.in_rfo_panel:
            check(f"{row.ticker}: RFO reconciled", row.extract.rfo.verified, row.extract.rfo.reason)
        if row.in_npat_panel:
            check(f"{row.ticker}: NPAT reconciled", row.extract.npat.verified, row.extract.npat.reason)
        if not row.in_rfo_panel and not row.in_npat_panel:
            check(f"{row.ticker}: exclusion carries a reason",
                  bool(row.exclusion_reason), row.exclusion_reason)

    margin_exact = all(
        (row.in_margin_panel) == (row.in_rfo_panel and row.in_npat_panel) for row in rows)
    check("margin panel is the exact RFO/NPAT intersection", margin_exact)

    seen: dict[str, str] = {}
    duplicated = [row.ticker for row in rows
                  if seen.setdefault(row.ticker, row.segment) != row.segment]
    check("each ticker belongs to exactly one segment", not duplicated, ";".join(duplicated))

    for record in segments:
        members = [row for row in rows
                   if row.segment == record["primary_segment_code"] and row.in_rfo_panel]
        expected = sum(row.rfo_current for row in members) if members else None
        actual = record["rfo_6m26_mb"]
        ok = (expected is None and actual is None) or (
            expected is not None and actual is not None and abs(expected - actual) < 0.01)
        check(f"segment {record['primary_segment_code']}: RFO equals member sum", ok)

    sector_total = sum(record["rfo_6m26_mb"] or 0 for record in sectors)
    segment_total = sum(record["rfo_6m26_mb"] or 0 for record in segments)
    check("sector totals equal segment totals",
          abs(sector_total - segment_total) < 0.01,
          f"{sector_total:.2f} vs {segment_total:.2f}")

    counts = {
        "pass": sum(1 for item in checks if item["result"] == "pass"),
        "fail": sum(1 for item in checks if item["result"] == "fail"),
    }
    return {"verdict": "PASS" if counts["fail"] == 0 else "FAIL",
            "counts": counts, "checks": checks}


def _exclusion_cause(row: CompanyRow) -> str:
    """Bucket an exclusion into an actionable cause rather than a raw message."""
    reason = row.exclusion_reason
    if not reason:
        return ""
    if "no 2026Q2 MD&A" in reason:
        return "no Q2/2026 MD&A in the vault"
    if "plausibility band" in reason:
        return "figure failed the FY plausibility band"
    # Order matters: a company can miss both panels for different reasons, and
    # the specific cause is more actionable than the generic one.
    if "unattributed 'net profit'" in reason:
        return "no owner-attributed profit line (unattributed net profit only)"
    if "different basis than SET 01 Sale" in reason:
        return "only a combined total revenue, no other-income line to subtract"
    if "no 6M25/6M26 table found" in reason:
        return "MD&A carries no half-year table"
    if "exceeds" in reason and "computed" in reason:
        return "issuer-stated YoY did not reconcile"
    if "net margin" in reason:
        return "implied margin out of range"
    if "non-numeric" in reason or "numeric fields" in reason:
        return "half-year columns did not align with the row"
    return "other"


def build_report(rows: list[CompanyRow], segments: list[dict], qa: dict, as_of: str) -> str:
    """A human-readable summary of what landed in the panel and what did not."""
    total = len(rows)
    rfo = [row for row in rows if row.in_rfo_panel]
    npat = [row for row in rows if row.in_npat_panel]
    margin = [row for row in rows if row.in_margin_panel]

    lines = [
        f"# 6M26 panel coverage — {as_of}",
        "",
        f"QA verdict **{qa['verdict']}** ({qa['counts']['pass']} pass / {qa['counts']['fail']} fail)",
        "",
        "| Panel | Companies | Share of universe |",
        "| --- | ---: | ---: |",
        f"| Universe | {total} | 100.0% |",
        f"| RFO (6M26 revenue) | {len(rfo)} | {len(rfo) / total * 100:.1f}% |",
        f"| NPAT to owners | {len(npat)} | {len(npat) / total * 100:.1f}% |",
        f"| Margin (intersection) | {len(margin)} | {len(margin) / total * 100:.1f}% |",
        "",
    ]

    causes: dict[str, list[str]] = {}
    for row in rows:
        cause = _exclusion_cause(row)
        if cause:
            causes.setdefault(cause, []).append(row.ticker)
    if causes:
        lines += ["## Why companies are missing a panel", "",
                  "| Cause | Companies | Tickers |", "| --- | ---: | --- |"]
        for cause, tickers in sorted(causes.items(), key=lambda item: -len(item[1])):
            listed = ", ".join(sorted(tickers))
            if len(listed) > 300:
                listed = listed[:297] + "…"
            lines.append(f"| {cause} | {len(tickers)} | {listed} |")
        lines.append("")

    promotable = [row for row in rows
                  if not row.in_npat_panel and row.extract
                  and row.extract.npat_unattributed.verified]
    if promotable:
        lines += [
            "## Candidates for analyst promotion", "",
            "These print a reconcilable but unattributed \"net profit\". Confirm "
            "non-controlling interests are immaterial, then promote them into the "
            "NPAT panel by hand.", "",
            "| Ticker | Segment | 6M26 net profit (THB mn) |", "| --- | --- | ---: |",
        ]
        for row in sorted(promotable, key=lambda r: r.ticker):
            value = row.extract.npat_unattributed.current
            lines.append(f"| {row.ticker} | {row.segment} | {value:,.0f} |")
        lines.append("")

    lines += ["## Segment coverage", "",
              "| Segment | Universe | RFO panel | NPAT panel |", "| --- | ---: | ---: | ---: |"]
    for record in segments:
        lines.append(
            f"| {record['primary_segment_code']} | {record['universe_company_count']} "
            f"| {record['rfo_panel_company_count']} | {record['npat_panel_company_count']} |")
    lines += ["",
              "Every figure in the company CSV carries the row label and source line it "
              "came from; check `rfo_evidence` / `npat_evidence` before quoting a number.",
              ""]
    return "\n".join(lines)


def write_csv(path: Path, fields: list[str], records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for record in records:
            writer.writerow(record)


def build(vault_root: Path, fy_company_csv: Path, out_dir: Path, as_of: str) -> dict:
    universe = load_universe(fy_company_csv)
    rows = build_company_rows(vault_root, universe)
    companies = [company_record(row) for row in rows]
    segments = build_segments(rows)
    sectors = build_sectors(rows)
    qa = run_qa(rows, segments, sectors)

    company_path = out_dir / f"food_prop_company_6m25_6m26_{as_of}.csv"
    segment_path = out_dir / f"food_prop_segment_6m25_6m26_{as_of}.csv"
    sector_path = out_dir / f"food_prop_sector_6m25_6m26_{as_of}.csv"
    write_csv(company_path, COMPANY_FIELDS, companies)
    write_csv(segment_path, SEGMENT_FIELDS, segments)
    write_csv(sector_path, [f for f in SEGMENT_FIELDS if f != "primary_segment_code"], sectors)

    qa_path = out_dir / f"QA_SUMMARY_6M25_6M26_{as_of}.json"
    qa_path.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report_path = out_dir / f"COVERAGE_REPORT_6M25_6M26_{as_of}.md"
    report_path.write_text(build_report(rows, segments, qa, as_of), encoding="utf-8")

    provenance = {
        "schema_version": "1.0",
        "period": "6M26 vs 6M25",
        "built_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "as_of": as_of,
        "filing_period": PERIOD,
        "universe_company_count": len(rows),
        "rfo_panel_company_count": sum(1 for row in rows if row.in_rfo_panel),
        "npat_panel_company_count": sum(1 for row in rows if row.in_npat_panel),
        "fy_company_csv": str(fy_company_csv),
        "fy_company_csv_sha256": sha256_file(fy_company_csv),
        "outputs": {
            path.name: sha256_file(path)
            for path in (company_path, segment_path, sector_path, qa_path, report_path)
        },
        "sources": [
            {"ticker": row.ticker, "path": row.source_path, "sha256": row.source_sha256}
            for row in rows if row.source_path
        ],
        "method": (
            "6M26 and 6M25 revenue and owner NPAT parsed from the Q2/2026 MD&A "
            "half-year columns. A figure is published only where the issuer's own "
            "printed YoY reconciles to the extracted pair, or where the column "
            "mapping was proven by another reconciled row in the same table."
        ),
        "limitations": [
            "MD&A half-year tables are management-prepared and may differ from the "
            "reviewed interim financial statements.",
            "Issuers printing only an unattributed 'net profit' are excluded from the "
            "NPAT panel; that figure is carried separately for analyst review.",
            "Revenue is reported on the SET 01 Sale basis, derived by subtracting a "
            "separately reconciled other-income line where the issuer prints only a total.",
        ],
        "qa_verdict": qa["verdict"],
        "qa_counts": qa["counts"],
    }
    provenance_path = out_dir / f"PROVENANCE_6M25_6M26_{as_of}.json"
    provenance_path.write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")

    return {
        "universe": len(rows),
        "rfo_panel": provenance["rfo_panel_company_count"],
        "npat_panel": provenance["npat_panel_company_count"],
        "qa": qa["verdict"],
        "qa_counts": qa["counts"],
        "out_dir": str(out_dir),
        "report": str(report_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault-root", type=Path, required=True,
                        help="Path to 'Work-SET/Listed Company' inside the vault")
    parser.add_argument("--fy-company-csv", type=Path, required=True,
                        help="Audited FY2024/FY2025 company CSV (the authoritative perimeter)")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--as-of", default=date.today().isoformat())
    args = parser.parse_args()

    summary = build(args.vault_root, args.fy_company_csv, args.out_dir, args.as_of)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["qa"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
