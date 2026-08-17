#!/usr/bin/env python3
"""Extract 6M26 / 6M25 revenue and owner NPAT from harvested filing markdown.

Design rule: **verify or exclude**. Every figure this module marks ``verified``
has been reconciled against something the issuer itself published — the YoY
percentage printed beside the 6M26 column. A row that cannot be reconciled is
returned unverified and the panel builder drops it with a reason. Nothing is
inferred from a single unchecked number, because one wrong column silently
becomes a wrong sector aggregate.

The parser targets the interim MD&A layout SET issuers file for Q2, where a
profit-and-loss block carries explicit ``6M25`` and ``6M26`` columns:

    Profit & Loss Statement (Baht mn) 2Q25 1Q26 2Q26 YoY (%) QoQ (%) 6M25 6M26 YoY (%)
    Total Revenue                     12,147 13,352 13,105  8%  (2%)  24,308 26,457 9%
    Profit to Parent Company           4,305  4,971  4,750 10%  (4%)   8,532  9,721 14%

Text arrives from ``pypdf``/``pdfium`` extraction, so the parser tolerates the
artefacts that introduces: spaces inside numbers ("13 ,105"), non-breaking
spaces, and unicode dashes standing in for nil.

The reconciliation is what makes this safe. Picking the wrong column produces a
YoY that disagrees with the issuer's printed YoY, so the row is rejected rather
than published.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

# --------------------------------------------------------------- normalising

_SPACE_RUN = re.compile(r"[^\S\n]+")
# pypdf routinely splits number tokens: "13 ,105" / "4 ,750" / "1, 234".
_NUM_GAP = re.compile(r"(?<=\d)\s+(?=[,.]\d)|(?<=[,.])\s+(?=\d)")


def normalise_text(text: str) -> str:
    """Canonicalise unicode and repair number tokens split by PDF extraction."""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("−", "-")  # unicode minus
    for dash in ("–", "—"):  # en/em dash used as a nil marker
        text = text.replace(dash, "-")
    lines = []
    for line in text.split("\n"):
        line = _SPACE_RUN.sub(" ", line)
        line = _NUM_GAP.sub("", line)
        lines.append(line.strip())
    return "\n".join(lines)


_MONEY_RE = re.compile(r"^\(?-?\d{1,3}(?:,\d{3})*(?:\.\d+)?\)?$|^\(?-?\d+(?:\.\d+)?\)?$")
_NIL = {"-", "--", "n.a.", "n/a", "nm", "n.m.", ""}


def parse_money(token: str) -> float | None:
    """Parse one money token to a float; parentheses denote a negative."""
    token = token.strip()
    if token.lower() in _NIL or not _MONEY_RE.match(token):
        return None
    negative = token.startswith("(") and token.endswith(")")
    token = token.strip("()").replace(",", "").strip()
    if token.startswith("-"):
        negative, token = True, token[1:]
    if not re.fullmatch(r"\d+(?:\.\d+)?", token):
        return None
    value = float(token)
    return -value if negative else value


def parse_pct(token: str) -> float | None:
    """Parse a percentage token, including the parenthesised-negative forms.

    Issuers print negatives as "(2%)" and occasionally "(2)%", so the percent
    sign is removed first and the remainder handed to ``parse_money``, which
    already reads parentheses as a minus sign.
    """
    token = token.strip()
    if "%" not in token:
        return None
    return parse_money(token.replace("%", "").strip())


def is_data_token(token: str) -> bool:
    return parse_pct(token) is not None or parse_money(token) is not None


def is_nil_token(token: str) -> bool:
    """A cell that occupies a column but holds no value ("n.m.", "-", "n/a").

    These must stay inside the data block: an issuer reporting a loss prints
    "n.m." in the YoY column, and dropping it would shift every column left.
    """
    return token.strip().lower() in _NIL


# ----------------------------------------------------------- column geometry

# A column header naming a period: 2Q25, Q2 2025, 6M26, 1H26, FY25, 9M25.
_PERIOD_COL = re.compile(
    r"^(?:[1-4]Q|Q[1-4]|6M|9M|1H|2H|H1|H2|FY)\s*(?:20)?\d{2}$", re.I
)
# Tokens that continue a column name rather than starting a new one.
_COL_SUFFIX = {"(%)", "%", "(chg)", "chg", "(x)", "(times)"}


def _merge_column_tokens(tokens: list[str]) -> list[str]:
    """Fold "(%)"/"(Chg)" suffixes into the preceding token.

    "YoY (%)" is one column printed as two whitespace-separated tokens; without
    merging, every column right of it would be off by one.
    """
    merged: list[str] = []
    for token in tokens:
        if merged and token.lower() in _COL_SUFFIX:
            merged[-1] = f"{merged[-1]} {token}"
        else:
            merged.append(token)
    return merged


def _period_token(year_two: str) -> re.Pattern[str]:
    return re.compile(
        rf"^(?:6M|1H|H1)\s*(?:20)?{year_two}$", re.I
    )


HEADER_PRIOR = _period_token("25")
HEADER_CURRENT = _period_token("26")


@dataclass
class PeriodColumns:
    """Zero-based positions of the 6M25 / 6M26 columns among a table's columns."""

    prior: int
    current: int
    count: int
    header: str


def find_period_columns(line: str) -> PeriodColumns | None:
    """Locate the 6M25 and 6M26 columns in a table header line.

    Positions are counted among *columns only* — the leading descriptive label
    ("Profit & Loss Statement (Baht mn)") is excluded, so the indices line up
    with the numeric fields of the data rows beneath.
    """
    tokens = _merge_column_tokens(line.split())
    first_col = next((i for i, t in enumerate(tokens) if _PERIOD_COL.match(t)), None)
    if first_col is None:
        return None
    columns = tokens[first_col:]
    prior = next((i for i, t in enumerate(columns) if HEADER_PRIOR.match(t)), None)
    current = next((i for i, t in enumerate(columns) if HEADER_CURRENT.match(t)), None)
    if prior is None or current is None or current <= prior:
        return None
    return PeriodColumns(prior=prior, current=current, count=len(columns), header=line.strip())


def split_row(line: str) -> tuple[str, list[str]]:
    """Split a data row into (label, numeric fields).

    The data block is the *trailing* run of money/percentage tokens, so a label
    that itself contains a number ("Central Rama 2 lease") stays in the label.
    """
    tokens = line.split()
    index = len(tokens)
    while index > 0 and (is_data_token(tokens[index - 1]) or is_nil_token(tokens[index - 1])):
        index -= 1
    fields = tokens[index:]
    # A run made only of nil markers is not a data block — it is punctuation.
    if index == len(tokens) or not any(is_data_token(token) for token in fields):
        return line.strip(), []
    return " ".join(tokens[:index]).strip(" .:…-"), fields


# ------------------------------------------------------------- row selection

# Ordered most-specific first. ``revenue_from_operations`` matches the SET
# "01 Sale" basis the FY panel uses; ``total_revenue`` includes other income and
# is therefore a *different* basis, flagged as such downstream.
REVENUE_PATTERNS: tuple[tuple[str, str], ...] = (
    ("revenue_from_operations", r"^total\s+revenues?\s+from\s+(?:sale|operation)"),
    ("revenue_from_operations", r"^revenues?\s+from\s+sales?\s+and\s+(?:rendering\s+of\s+)?services?"),
    ("revenue_from_operations", r"^revenues?\s+from\s+sale\s+of\s+goods"),
    ("revenue_from_operations", r"^sales?\s+and\s+services?\s+incomes?$"),
    ("revenue_from_operations", r"^sales?\s+and\s+services?$"),
    ("revenue_from_operations", r"^revenues?\s+from\s+sales?$"),
    ("revenue_from_operations", r"^total\s+sales?(?:\s+revenues?)?$"),
    ("total_revenue", r"^total\s+revenues?$"),
    ("total_revenue", r"^total\s+revenues?\b"),
)

# Other income is subtracted from total revenue to recover the SET 01 Sale
# basis when an issuer only prints a combined total.
OTHER_INCOME_PATTERNS: tuple[tuple[str, str], ...] = (
    ("other_income", r"^other\s+incomes?$"),
    ("other_income", r"^other\s+revenues?$"),
    ("other_income", r"^other\s+operating\s+incomes?$"),
)

NPAT_PATTERNS: tuple[tuple[str, str], ...] = (
    ("npat_owners", r"^(?:net\s+)?profit\s*(?:\(loss\))?\s+to\s+(?:the\s+)?parent"),
    ("npat_owners", r"^(?:net\s+)?profit\s*(?:\(loss\))?\s+attributable\s+to\s+(?:the\s+)?(?:parent|owners?|equity\s+holders?|shareholders?)"),
    ("npat_owners", r"^(?:net\s+)?(?:profit|income)\s*(?:\(loss\))?\s+for\s+the\s+periods?\s+attributable\s+to"),
)

# Many issuers print only "Net profit", which is profit *before* the split
# between owners and non-controlling interests. That is a different measure from
# the FY panel's NPAT-to-owners, so it is captured separately and never enters a
# panel automatically — an analyst promotes it only where NCI is immaterial.
NPAT_UNATTRIBUTED_PATTERNS: tuple[tuple[str, str], ...] = (
    ("net_profit_unattributed", r"^net\s+profits?\s*(?:\(loss\))?$"),
    ("net_profit_unattributed", r"^net\s+profits?\s*(?:\(loss\))?\s+for\s+the\s+periods?$"),
    ("net_profit_unattributed", r"^profits?\s*(?:\(loss\))?\s+for\s+the\s+periods?$"),
)

# Rows that look like the target but report a different measure. Excluded so a
# "core"/"normalised" figure never enters a panel built on reported numbers.
ADJUSTED_MARKERS = (
    "excl", "exclud", "core", "normalis", "normaliz", "adjust", "recurring",
    "proforma", "pro forma", "before extraordinary", "margin", "per share",
    "growth", "%",
)


def is_adjusted(label: str) -> bool:
    low = label.lower()
    return any(marker in low for marker in ADJUSTED_MARKERS)


@dataclass
class Figure:
    """One measure for one company, with its reconciliation outcome."""

    measure: str = ""
    label: str = ""
    prior: float | None = None
    current: float | None = None
    stated_yoy_pct: float | None = None
    computed_yoy_pct: float | None = None
    status: str = "missing"
    reason: str = "no 6M25/6M26 table found"
    evidence: str = ""
    derivation: str = ""
    header: str = ""

    @property
    def verified(self) -> bool:
        return self.status == "verified"


def _match_measure(label: str, patterns: tuple[tuple[str, str], ...]) -> str | None:
    stripped = label.strip()
    for name, pattern in patterns:
        if re.match(pattern, stripped, re.I):
            return name
    return None


def extract_measure(
    text: str,
    patterns: tuple[tuple[str, str], ...],
    tolerance_pp: float = 1.0,
) -> Figure:
    """Find the first row matching ``patterns`` whose YoY reconciles.

    ``tolerance_pp`` is the allowed gap between the issuer's printed YoY% and the
    YoY% computed from the extracted pair. Issuers round YoY to a whole percent,
    so 1.0pp absorbs rounding while still rejecting a wrong column.
    """
    columns: PeriodColumns | None = None
    fallback = Figure()

    for line in text.split("\n"):
        header = find_period_columns(line)
        if header is not None:
            columns = header
            continue
        if columns is None:
            continue
        label, fields = split_row(line)
        if not fields or not label or is_adjusted(label):
            continue
        measure = _match_measure(label, patterns)
        if measure is None:
            continue

        base = Figure(measure=measure, label=label, evidence=line.strip(),
                      header=columns.header)
        if not (columns.prior < len(fields) and columns.current < len(fields)):
            base.status = "unreconciled"
            base.reason = (f"row has {len(fields)} numeric fields; 6M columns sit at "
                           f"{columns.prior}/{columns.current} of {columns.count}")
            fallback = base
            continue
        prior = parse_money(fields[columns.prior])
        current = parse_money(fields[columns.current])
        if prior is None or current is None:
            base.status = "unreconciled"
            base.reason = "a 6M column held a non-numeric value"
            fallback = base
            continue

        base.prior, base.current = prior, current
        if columns.current + 1 < len(fields):
            base.stated_yoy_pct = parse_pct(fields[columns.current + 1])
        if prior > 0:
            base.computed_yoy_pct = (current - prior) / prior * 100.0

        if base.stated_yoy_pct is None:
            base.status = "unreconciled"
            base.reason = "no issuer-stated YoY beside the 6M26 column"
        elif base.computed_yoy_pct is None:
            base.status = "unreconciled"
            base.reason = "non-positive prior-period base; YoY not reconcilable"
        elif abs(base.stated_yoy_pct - base.computed_yoy_pct) <= tolerance_pp:
            base.status = "verified"
            base.reason = (f"issuer YoY {base.stated_yoy_pct:+.0f}% reconciles to computed "
                           f"{base.computed_yoy_pct:+.2f}%")
            return base
        else:
            base.status = "unreconciled"
            base.reason = (f"stated YoY {base.stated_yoy_pct:+.1f}% vs computed "
                           f"{base.computed_yoy_pct:+.1f}% exceeds {tolerance_pp}pp")
        fallback = base
    return fallback


@dataclass
class CompanyExtract:
    """The reconciled 6M26 panel measures for one company."""

    ticker: str
    revenue: Figure = field(default_factory=Figure)
    other_income: Figure = field(default_factory=Figure)
    rfo: Figure = field(default_factory=Figure)
    npat: Figure = field(default_factory=Figure)
    npat_unattributed: Figure = field(default_factory=Figure)
    checks: list[str] = field(default_factory=list)

    @property
    def status(self) -> str:
        return "verified" if self.rfo.verified and self.npat.verified else "needs_review"

    @property
    def exclusion_reason(self) -> str:
        if self.status == "verified":
            return ""
        parts = []
        if not self.rfo.verified:
            parts.append(f"rfo: {self.rfo.reason}")
        if not self.npat.verified:
            parts.append(f"npat: {self.npat.reason}")
        return "; ".join(parts)


# A 6M net margin outside this band means a mis-picked row (e.g. operating
# profit captured as owner NPAT), not a real company.
MARGIN_CEILING_PCT = 100.0
MARGIN_FLOOR_PCT = -200.0


def _derive_rfo(revenue: Figure, other_income: Figure) -> Figure:
    """Recover the SET 01 Sale basis from a combined total revenue line.

    The FY panel measures RFO excluding other income. When an issuer prints only
    a combined total, subtracting a separately reconciled "Other income" row
    reproduces that basis by exact arithmetic on two independently verified
    rows — no estimation involved.
    """
    if revenue.measure == "revenue_from_operations":
        return revenue
    if not (revenue.verified and other_income.verified):
        return Figure(
            measure="revenue_from_operations",
            label=revenue.label,
            status="unreconciled",
            reason=("total revenue is on a different basis than SET 01 Sale and no "
                    "reconcilable other-income row was found to subtract"),
            evidence=revenue.evidence,
        )
    prior = revenue.prior - other_income.prior
    current = revenue.current - other_income.current
    computed = (current - prior) / prior * 100.0 if prior > 0 else None
    return Figure(
        measure="revenue_from_operations",
        label=f"{revenue.label} less {other_income.label}",
        prior=prior,
        current=current,
        computed_yoy_pct=computed,
        status="verified",
        reason="derived from two independently reconciled rows",
        evidence=revenue.evidence,
        header=revenue.header,
        derivation=(f"{revenue.current:,.0f} - {other_income.current:,.0f} = {current:,.0f} (6M26); "
                    f"{revenue.prior:,.0f} - {other_income.prior:,.0f} = {prior:,.0f} (6M25)"),
    )


# Reasons that reflect a missing YoY rather than a wrong column pick. Only these
# are eligible for geometry-based reconciliation.
_GEOMETRY_ELIGIBLE = (
    "non-positive prior-period base",
    "no issuer-stated YoY",
)


def reconcile_by_geometry(figure: Figure, proven: Figure) -> Figure:
    """Accept a row whose column mapping was proven by another row in its table.

    A loss-making issuer prints no meaningful YoY next to its owner-NPAT line, so
    that row cannot self-reconcile. But the YoY check on a *different* row of the
    same table proves where the 6M25/6M26 columns sit; any row read from the same
    header is therefore read from the right columns. This never rescues a row
    whose own YoY disagreed — that signals a genuinely wrong pick.
    """
    if figure.verified or not proven.verified:
        return figure
    if not figure.header or figure.header != proven.header:
        return figure
    if not any(reason in figure.reason for reason in _GEOMETRY_ELIGIBLE):
        return figure
    if figure.prior is None or figure.current is None:
        return figure
    figure.status = "verified"
    figure.reason = (f"column mapping proven by the reconciled '{proven.label}' row "
                     f"in the same table")
    return figure


def extract_company(ticker: str, markdown: str) -> CompanyExtract:
    """Extract and reconcile the 6M26 panel measures for one company."""
    text = normalise_text(markdown)
    revenue = extract_measure(text, REVENUE_PATTERNS)
    other_income = extract_measure(text, OTHER_INCOME_PATTERNS)
    npat = extract_measure(text, NPAT_PATTERNS)
    # A loss-making issuer's NPAT row carries no reconcilable YoY; fall back to
    # the column geometry proven by the revenue row in the same table.
    npat = reconcile_by_geometry(npat, revenue)
    unattributed = reconcile_by_geometry(
        extract_measure(text, NPAT_UNATTRIBUTED_PATTERNS), revenue)
    result = CompanyExtract(
        ticker=ticker,
        revenue=revenue,
        other_income=other_income,
        rfo=_derive_rfo(revenue, other_income),
        npat=npat,
        npat_unattributed=unattributed,
    )
    if not npat.verified and unattributed.verified:
        result.checks.append(
            "only an unattributed 'net profit' line was found; the FY panel "
            "measures profit attributable to owners of the parent")
    if result.rfo.derivation:
        result.checks.append(f"RFO derived: {result.rfo.derivation}")
    if result.rfo.verified and result.npat.verified and result.rfo.current:
        margin = result.npat.current / result.rfo.current * 100.0
        result.checks.append(f"6M26 net margin {margin:.2f}%")
        if not (MARGIN_FLOOR_PCT <= margin <= MARGIN_CEILING_PCT):
            result.npat.status = "unreconciled"
            result.npat.reason = f"implied 6M26 net margin {margin:.1f}% is out of range"
    return result
