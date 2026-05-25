"""Email alert client + composer.

Two-tier routing:
  - critical -> batched email per RM (one or more chunks if very large)
  - material -> per-RM digest email
  - routine  -> not alerted (already in DB)

Idempotency: every send is recorded in `alerts_sent` keyed on (news_id, channel),
so re-runs never double-alert.
"""

from __future__ import annotations

import os
import smtplib
import ssl
import time
import uuid
from collections import defaultdict
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from typing import Iterable

from dotenv import load_dotenv

from store import conn

load_dotenv(Path(__file__).parent / ".env")

EMAIL_CHANNEL = "email"
MAX_LEN = 4000  # max chars per chunk; matches old Telegram limit, kept for safety


class EmailClient:
    """Sends Gmail SMTP messages.

    Subject is the first non-empty line of `text`; body is everything after.
    Uses Gmail's standard submission port (587) with STARTTLS and a Gmail
    App Password (NOT the account password) — generated at
    https://myaccount.google.com/apppasswords.
    """

    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        from_addr: str | None = None,
        to_addr: str | None = None,
        host: str = "smtp.gmail.com",
        port: int = 587,
        timeout: float = 15.0,
    ) -> None:
        self.username = username or os.environ.get("EMAIL_USERNAME")
        self.password = (password or os.environ.get("EMAIL_APP_PASSWORD") or "").replace(" ", "")
        self.from_addr = from_addr or os.environ.get("EMAIL_FROM") or self.username
        self.to_addr = to_addr or os.environ.get("EMAIL_TO") or self.username
        self.host = host
        self.port = port
        self.timeout = timeout
        if not (self.username and self.password and self.from_addr and self.to_addr):
            raise RuntimeError(
                "Email credentials missing. Set EMAIL_USERNAME, EMAIL_APP_PASSWORD, "
                "EMAIL_FROM (optional), EMAIL_TO (optional)."
            )

    def __enter__(self) -> "EmailClient":
        return self

    def __exit__(self, *_: object) -> None:
        pass

    def send(self, text: str, *, priority: str | None = None) -> str:
        """Send a single email. First non-empty line is the subject; rest is the body.
        Returns a synthetic 8-char id used to keep alerts_sent.message_id populated.
        `priority="high"` adds X-Priority/Importance headers so Outlook + Gmail flag the
        message."""
        lines = text.split("\n", 1)
        subject = (lines[0].strip() or "SET surveillance alert")[:200]
        body = lines[1].lstrip() if len(lines) > 1 else ""

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.from_addr
        msg["To"] = self.to_addr
        if priority == "high":
            msg["X-Priority"] = "1"
            msg["X-MSMail-Priority"] = "High"
            msg["Importance"] = "High"
        msg.set_content(body or subject)

        last_exc: Exception | None = None
        for attempt in range(3):
            try:
                with smtplib.SMTP(self.host, self.port, timeout=self.timeout) as s:
                    s.ehlo()
                    s.starttls(context=ssl.create_default_context())
                    s.login(self.username, self.password)
                    s.send_message(msg)
                return uuid.uuid4().hex[:8]
            except Exception as e:  # noqa: BLE001
                last_exc = e
                time.sleep(2 ** attempt)
        raise RuntimeError(f"Email send failed after 3 attempts: {last_exc}")


# ---------------------------- formatters --------------------------------- #

def _bkk_date(iso: str) -> str:
    return iso.split("T")[0] if "T" in iso else iso


def _financials_line_for(symbol: str, datetime_iso: str) -> str | None:
    """Return a one-line YoY/QoQ delta summary if the most-recent quarter
    snapshot for `symbol` is dated within 120 days BEFORE `datetime_iso`."""
    disclosure_date = (datetime_iso or "")[:10]
    if not disclosure_date:
        return None
    sql = """
    SELECT year, quarter, date_as_of,
           rev_yoy_pct, ni_yoy_pct, npm_yoy_bps, ocf_yoy_pct,
           rev_qoq_pct, ni_qoq_pct
    FROM financials_snapshots
    WHERE symbol = ?
      AND date_as_of IS NOT NULL
      AND date_as_of <= ?
    ORDER BY date_as_of DESC
    LIMIT 1
    """
    with conn() as c:
        row = c.execute(sql, [symbol, disclosure_date]).fetchone()
    if not row:
        return None
    y, q, asof, rev_y, ni_y, npm_y, ocf_y, rev_q, ni_q = row
    try:
        d_disc = datetime.strptime(disclosure_date, "%Y-%m-%d")
        d_asof = datetime.strptime(asof, "%Y-%m-%d")
        if (d_disc - d_asof).days > 120:
            return None
    except (ValueError, TypeError):
        return None

    def pct(v: float | None) -> str:
        return f"{v:+.1f}%" if v is not None else "n/a"

    def bps(v: float | None) -> str:
        return f"{v:+.0f}bp" if v is not None else "n/a"

    return (
        f"Q{q}/{y}: rev {pct(rev_y)} YoY ({pct(rev_q)} QoQ) · "
        f"NPM {bps(npm_y)} YoY · NI {pct(ni_y)} YoY · OCF {pct(ocf_y)} YoY"
    )


def _maybe_attach_financials(row: dict) -> str | None:
    if (row.get("category") or "").lower() != "earnings":
        return None
    return _financials_line_for(row["symbol"], row.get("datetime_iso") or "")


def _price_anomaly_line_for(symbol: str, datetime_iso: str) -> str | None:
    disclosure_date = (datetime_iso or "")[:10]
    if not disclosure_date:
        return None
    sql = """
    SELECT trade_date, daily_return, return_z, volume_ratio,
           is_return_anom, is_volume_anom, is_new_high, is_new_low
    FROM price_anomalies
    WHERE symbol = ? AND trade_date <= ?
    ORDER BY trade_date DESC
    LIMIT 1
    """
    with conn() as c:
        row = c.execute(sql, [symbol, disclosure_date]).fetchone()
    if not row:
        return None
    trade_date, ret, z, vol_ratio, ret_anom, vol_anom, new_hi, new_lo = row
    try:
        d_disc = datetime.strptime(disclosure_date, "%Y-%m-%d")
        d_trade = datetime.strptime(trade_date, "%Y-%m-%d")
        if (d_disc - d_trade).days > 3:
            return None
    except (ValueError, TypeError):
        return None
    if not (ret_anom or vol_anom or new_hi or new_lo):
        return None
    parts = []
    if ret is not None:
        parts.append(f"{ret*100:+.1f}%")
    if z is not None and ret_anom:
        parts.append(f"z={z:+.1f}")
    if vol_ratio is not None and vol_anom:
        parts.append(f"vol {vol_ratio:.1f}×")
    if new_hi:
        parts.append("60d-high")
    if new_lo:
        parts.append("60d-low")
    return f"{trade_date}: " + " · ".join(parts)


def _maybe_attach_price_anomaly(row: dict) -> str | None:
    return _price_anomaly_line_for(row["symbol"], row.get("datetime_iso") or "")


def format_digest(rows: list[dict]) -> list[str]:
    """Material-only digest — sector-grouped inside one severity section."""
    today = time.strftime("%Y-%m-%d")
    if not rows:
        return [f"🟡 MATERIAL DIGEST — {today}\n\n_No new material disclosures._"]

    sec_map = _sector_lookup()
    by_sector: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_sector[sec_map.get(r["symbol"], "OTHER")].append(r)

    sector_keys = [s for s in SECTOR_ORDER if s in by_sector] + \
                  sorted(s for s in by_sector if s not in SECTOR_ORDER)

    header = f"🟡 MATERIAL DIGEST — {today}  ({len(rows)} item{'s' if len(rows) != 1 else ''})\n\n"
    body_chunks: list[str] = []
    current = header

    def _flush(buf: str) -> None:
        if buf.strip():
            body_chunks.append(buf.rstrip())

    for sector in sector_keys:
        sec_rows = by_sector[sector]
        sec_block = f"▼ {sector} ({len(sec_rows)})\n"

        by_ticker: dict[str, list[dict]] = defaultdict(list)
        for r in sec_rows:
            by_ticker[r["symbol"]].append(r)

        for sym in sorted(by_ticker, key=lambda s: (-len(by_ticker[s]), s)):
            items = by_ticker[sym]
            sec_block += f"  ━━ {sym} ({len(items)}) ━━\n"
            for r in sorted(items, key=lambda x: x["datetime_iso"], reverse=True):
                time_short = r["datetime_iso"].split("T")[1][:5] if "T" in r["datetime_iso"] else ""
                summary = r["summary_en"][:140]
                if len(r["summary_en"]) > 140:
                    summary += "…"
                sec_block += f"  · {time_short}  {r['category']}: {summary}\n"
                fin = _maybe_attach_financials(r)
                if fin:
                    sec_block += f"        📊 {fin}\n"
        sec_block += "\n"

        if len(current) + len(sec_block) > MAX_LEN:
            _flush(current)
            current = "🟡 MATERIAL DIGEST (cont'd)\n\n" + sec_block
        else:
            current += sec_block

    _flush(current)
    return body_chunks


def format_critical_digest(rows: list[dict]) -> list[str]:
    """Batched critical disclosures — grouped by RM, then sector."""
    today = time.strftime("%Y-%m-%d")
    if not rows:
        return [f"🔴 CRITICAL DIGEST — {today}\n\n_No new critical disclosures._"]

    sec_map = _sector_lookup()
    rm_map = _rm_lookup()

    by_rm: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_rm[rm_map.get(r["symbol"], "Unassigned")].append(r)

    chunks: list[str] = []

    for rm in sorted(by_rm):
        rm_rows = by_rm[rm]
        header = (f"🔴 CRITICAL DIGEST — {today}  [RM: {rm}]  "
                  f"({len(rm_rows)} item{'s' if len(rm_rows) != 1 else ''})\n\n")
        current = header

        by_sector: dict[str, list[dict]] = defaultdict(list)
        for r in rm_rows:
            by_sector[sec_map.get(r["symbol"], "OTHER")].append(r)

        sector_keys = [s for s in SECTOR_ORDER if s in by_sector] + \
                      sorted(s for s in by_sector if s not in SECTOR_ORDER)

        def _flush(buf: str) -> None:
            if buf.strip():
                chunks.append(buf.rstrip())

        for sector in sector_keys:
            sec_rows = by_sector[sector]
            sec_block = f"▼ {sector} ({len(sec_rows)})\n"

            by_ticker: dict[str, list[dict]] = defaultdict(list)
            for r in sec_rows:
                by_ticker[r["symbol"]].append(r)

            for sym in sorted(by_ticker, key=lambda s: (-len(by_ticker[s]), s)):
                items = by_ticker[sym]
                sec_block += f"  ━━ {sym} ({len(items)}) ━━\n"
                for r in sorted(items, key=lambda x: x["datetime_iso"], reverse=True):
                    time_short = r["datetime_iso"].split("T")[1][:5] if "T" in r["datetime_iso"] else ""
                    summary = r["summary_en"][:140]
                    if len(r["summary_en"]) > 140:
                        summary += "…"
                    sec_block += f"  · {time_short}  {r['category']}: {summary}\n"
                    fin = _maybe_attach_financials(r)
                    if fin:
                        sec_block += f"        📊 {fin}\n"
            sec_block += "\n"

            if len(current) + len(sec_block) > MAX_LEN:
                _flush(current)
                current = f"🔴 CRITICAL DIGEST (cont'd) — {rm}\n\n" + sec_block
            else:
                current += sec_block

        _flush(current)

    return chunks


SEVERITY_EMOJI = {"critical": "🔴", "material": "🟡", "routine": "⚪"}
SEVERITY_ORDER = ["critical", "material", "routine"]
SECTOR_ORDER = ["PROP", "FOOD", "PFREIT"]


def _sector_lookup() -> dict[str, str]:
    from coverage import COVERAGE  # noqa: WPS433
    return {t: s for s, syms in COVERAGE.items() for t in syms}


def _rm_lookup() -> dict[str, str]:
    """Map ticker -> RM from rm.duckdb. Returns empty dict if rm.duckdb unavailable."""
    try:
        import duckdb
        rm_db = Path(__file__).parent.parent / "rm_db" / "rm.duckdb"
        if not rm_db.exists():
            return {}
        c = duckdb.connect(str(rm_db), read_only=True)
        result = c.execute("SELECT symbol, rm_name FROM tickers WHERE rm_name IS NOT NULL").fetchall()
        c.close()
        return {sym: rm for sym, rm in result}
    except Exception:
        return {}


# ---------------------------- DB queries --------------------------------- #

def fetch_unsent(severity: str, channel: str = EMAIL_CHANNEL,
                 since: str | None = None) -> list[dict]:
    """Classifier rows of `severity` not yet sent on `channel`.

    Optional `since` (YYYY-MM-DD) restricts to disclosures dated on or after
    that day — useful on first cutover so historical items don't flood the inbox.
    """
    where_extra = ""
    params: list = [channel, severity]
    if since:
        where_extra = " AND n.datetime_iso >= ?"
        params.append(since)
    sql = f"""
    SELECT n.id AS news_id, c.symbol, c.severity, c.category, n.datetime_iso,
           c.summary_en, c.summary_th, c.suggested_action, c.rationale,
           n.headline AS raw_headline, n.lang, n.url
    FROM classifications c
    JOIN news_items n ON n.id = c.news_id
    LEFT JOIN alerts_sent a ON a.news_id = c.news_id AND a.channel = ?
    WHERE c.severity = ? AND a.news_id IS NULL{where_extra}
    ORDER BY n.datetime_iso ASC
    """
    cols = ["news_id", "symbol", "severity", "category", "datetime_iso",
            "summary_en", "summary_th", "suggested_action", "rationale",
            "raw_headline", "lang", "url"]
    with conn() as c:
        return [dict(zip(cols, r)) for r in c.execute(sql, params).fetchall()]


def mark_all_unsent_as_sent(channel: str = EMAIL_CHANNEL) -> dict[str, int]:
    """First-run cutover: silently mark every unsent classified item as sent."""
    counts: dict[str, int] = {}
    for sev in ("critical", "material", "routine", "unclassified"):
        rows = fetch_unsent(sev, channel)
        if rows:
            mark_sent((r["news_id"] for r in rows), tier=f"backfill-{sev}",
                      channel=channel, message_id=None)
        counts[sev] = len(rows)
    return counts


def mark_sent(news_ids: Iterable[str], tier: str, channel: str = EMAIL_CHANNEL,
              message_id: str | None = None) -> None:
    with conn() as c:
        for nid in news_ids:
            c.execute(
                "INSERT INTO alerts_sent (news_id, channel, tier, message_id) VALUES (?, ?, ?, ?) "
                "ON CONFLICT (news_id, channel) DO NOTHING",
                [nid, channel, tier, message_id],
            )
