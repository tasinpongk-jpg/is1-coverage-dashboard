"""Read DuckDB → write 4 new JSON snapshots for the expanded dashboard.

Pairs with surveillance/external_sources.py. Runs in CI right after
build_daily.py; the DuckDB has already been downloaded as an artifact from
the surveillance job.

Outputs (under data/):
  external-news.json     — wire/RSS hits matched to coverage tickers
  trading-signs.json     — current SP/NP/CC/etc. on coverage names
  sec-enforcement.json   — SEC actions, matched + unmatched
  sec-form59.json        — SEC Form 59 management/related-person trades
  diagnostics.json       — coverage-gap + unclassified queue + per-RM staleness
"""

from __future__ import annotations

import json
import os
import sys
from html import unescape
from datetime import datetime, timezone, timedelta
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_PATH = Path(os.environ.get("SURVEILLANCE_DB_PATH") or
               (ROOT / "surveillance" / "surveillance.duckdb"))
BKK = timezone(timedelta(hours=7))


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _load_tickers() -> dict[str, dict]:
    j = json.loads((DATA_DIR / "tickers.json").read_text(encoding="utf-8"))
    out = {}
    for t in j["tickers"]:
        rm = t.get("rm")
        # Anonymise RM to its initial (privacy), defensively — even if
        # tickers.json ever regresses to full names upstream.
        if rm not in (None, ""):
            t = {**t, "rm": str(rm).strip()[:1].upper()}
        out[t["tk"]] = t
    return out


def _write(path: Path, payload: dict) -> None:
    payload["_built_at"] = _now_iso()
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    print(f"  -> wrote {path.name}  ({len(json.dumps(payload, default=str))} bytes)")


def _preserve_nonempty_snapshot(path: Path, payload: dict) -> bool:
    """Keep the last good external snapshot when a best-effort scrape is empty."""
    if payload.get("total") != 0 or not path.exists():
        return False
    try:
        existing = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return bool(existing.get("total", 0) > 0 and existing.get("items"))

def build_external_news(con: duckdb.DuckDBPyConnection, tickers: dict) -> None:
    rows = con.execute("""
        SELECT id, source, symbol, sector, datetime_iso, headline, url, body_excerpt, lang
        FROM external_news
        WHERE datetime_iso >= ?
        ORDER BY datetime_iso DESC
        LIMIT 2000
    """, [(datetime.now(BKK) - timedelta(days=30)).isoformat()]).fetchall()
    items = [
        {
            "id": r[0], "source": r[1], "tk": r[2], "sector": r[3],
            "ts": r[4], "title": r[5], "url": r[6], "excerpt": r[7], "lang": r[8],
            "rm": (tickers.get(r[2]) or {}).get("rm"),
        }
        for r in rows
    ]
    sources = sorted({i["source"] for i in items})
    _write(DATA_DIR / "external-news.json", {
        "asOf": datetime.now(BKK).date().isoformat(),
        "windowDays": 30,
        "sources": sources,
        "items": items,
    })


def build_trading_signs(con: duckdb.DuckDBPyConnection, tickers: dict) -> None:
    rows = con.execute("""
        SELECT symbol, sign, effective_date, reason, scraped_at
        FROM trading_signs
        ORDER BY sign, symbol
    """).fetchall()
    items = [
        {
            "tk": r[0], "sign": r[1], "effective_date": r[2], "reason": r[3],
            "scraped_at": r[4].isoformat() if r[4] else None,
            "rm": (tickers.get(r[0]) or {}).get("rm"),
            "sector": (tickers.get(r[0]) or {}).get("sector"),
        }
        for r in rows
    ]
    by_sign: dict[str, int] = {}
    for it in items:
        by_sign[it["sign"]] = by_sign.get(it["sign"], 0) + 1
    _write(DATA_DIR / "trading-signs.json", {
        "asOf": datetime.now(BKK).date().isoformat(),
        "total": len(items),
        "bySign": by_sign,
        "items": items,
    })


def _parse_sec_action_date(value: str | None) -> datetime | None:
    try:
        return datetime.strptime((value or "").strip(), "%d/%m/%Y")
    except ValueError:
        return None


def _sec_columns(description: str | None) -> list[str]:
    return [
        unescape(part).replace("\xa0", " ").strip()
        for part in (description or "").split("|")
    ]


def _sec_scraped_key(value) -> datetime:
    if isinstance(value, datetime):
        return value.replace(tzinfo=None)
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
        except ValueError:
            return datetime.min
    return datetime.min


def build_sec_enforcement(con: duckdb.DuckDBPyConnection, tickers: dict) -> None:
    raw_rows = con.execute("""
        SELECT id, case_no, action_date, respondent, action_type, matched_ticker, description, url, scraped_at
        FROM sec_enforcement
    """).fetchall()
    rows = [
        r for r in raw_rows
        if (r[2] or "").strip().lower() != "enforcement date"
        and (r[3] or "").strip().lower() != "name"
    ]
    rows.sort(
        key=lambda r: (
            _parse_sec_action_date(r[2]) or datetime.min,
            _sec_scraped_key(r[8]),
        ),
        reverse=True,
    )
    rows = rows[:200]
    items = []
    for r in rows:
        cols = _sec_columns(r[6])
        items.append({
            "id": r[0], "case_no": r[1], "action_date": r[2],
            "respondent": r[3], "action_type": r[4],
            "law": cols[3] if len(cols) > 3 else None,
            "facts": cols[4] if len(cols) > 4 else r[4],
            "enforcement_type": cols[6] if len(cols) > 6 else None,
            "details": cols[7] if len(cols) > 7 else None,
            "matched_ticker": r[5], "description": r[6], "url": r[7],
            "scraped_at": r[8].isoformat() if r[8] else None,
            "rm": (tickers.get(r[5]) or {}).get("rm") if r[5] else None,
            "sector": (tickers.get(r[5]) or {}).get("sector") if r[5] else None,
        })
    _write(DATA_DIR / "sec-enforcement.json", {
        "asOf": datetime.now(BKK).date().isoformat(),
        "total": len(items),
        "in_coverage_count": sum(1 for i in items if i["matched_ticker"]),
        "items": items,
    })


def build_sec_form59(con: duckdb.DuckDBPyConnection, tickers: dict) -> None:
    cutoff = (datetime.now(BKK) - timedelta(days=90)).date().isoformat()
    try:
        rows = con.execute(
            """
            SELECT id, symbol, company_name, reporter, relationship, security_type,
                   transaction_date, filing_date, amount, price, side, side_label,
                   remark, is_revoked, detail_url, source_url, source_lang, scraped_at
            FROM sec_form59
            WHERE COALESCE(filing_date, transaction_date, '') >= ?
            ORDER BY COALESCE(filing_date, transaction_date, '') DESC,
                     transaction_date DESC NULLS LAST,
                     symbol,
                     reporter
            LIMIT 1000
            """,
            [cutoff],
        ).fetchall()
    except duckdb.Error:
        rows = []

    items = []
    by_ticker: dict[str, dict] = {}
    by_side = {"buy": 0, "sell": 0, "transfer": 0, "other": 0}
    net_value = 0.0

    for r in rows:
        tk = r[1]
        amount = r[8]
        price = r[9]
        side = (r[10] or "other").lower()
        notional = None
        if amount is not None and price is not None:
            notional = round(float(amount) * float(price), 2)
            if side == "buy":
                net_value += notional
            elif side == "sell":
                net_value -= notional
        side_key = side if side in by_side else "other"
        by_side[side_key] += 1
        ticker_meta = tickers.get(tk) or {}
        item = {
            "id": r[0],
            "tk": tk,
            "sector": ticker_meta.get("sector"),
            "rm": ticker_meta.get("rm"),
            "company": r[2],
            "reporter": r[3],
            "relationship": r[4],
            "security_type": r[5],
            "transaction_date": r[6],
            "filing_date": r[7],
            "amount": amount,
            "price": price,
            "notional": notional,
            "side": side,
            "side_label": r[11],
            "remark": r[12],
            "is_revoked": bool(r[13]),
            "url": r[14],
            "source_url": r[15],
            "source_lang": r[16],
            "scraped_at": r[17].isoformat() if r[17] else None,
        }
        items.append(item)

        agg = by_ticker.setdefault(tk, {
            "tk": tk,
            "sector": ticker_meta.get("sector"),
            "rm": ticker_meta.get("rm"),
            "buy_count": 0,
            "sell_count": 0,
            "transfer_count": 0,
            "buy_value": 0.0,
            "sell_value": 0.0,
            "net_value": 0.0,
            "latest_filing_date": None,
        })
        if side == "buy":
            agg["buy_count"] += 1
            if notional is not None:
                agg["buy_value"] += notional
                agg["net_value"] += notional
        elif side == "sell":
            agg["sell_count"] += 1
            if notional is not None:
                agg["sell_value"] += notional
                agg["net_value"] -= notional
        elif side == "transfer":
            agg["transfer_count"] += 1
        fdate = r[7] or r[6]
        if fdate and (not agg["latest_filing_date"] or fdate > agg["latest_filing_date"]):
            agg["latest_filing_date"] = fdate

    aggregates = []
    for agg in by_ticker.values():
        for k in ("buy_value", "sell_value", "net_value"):
            agg[k] = round(agg[k], 2)
        aggregates.append(agg)
    aggregates.sort(key=lambda a: (abs(a["net_value"]), a["buy_count"] + a["sell_count"]), reverse=True)

    target = DATA_DIR / "sec-form59.json"
    payload = {
        "asOf": datetime.now(BKK).date().isoformat(),
        "windowDays": 90,
        "total": len(items),
        "bySide": by_side,
        "netNotional": round(net_value, 2),
        "tickers": aggregates,
        "items": items,
    }
    if _preserve_nonempty_snapshot(target, payload):
        print("  -> kept previous non-empty sec-form59.json (current SEC scrape returned 0 rows)")
        return
    _write(target, payload)


def build_diagnostics(con: duckdb.DuckDBPyConnection, tickers: dict) -> None:
    """Coverage-gap + unclassified queue + per-RM staleness.

    All cheap reads off the existing tables — no extra scrape needed.
    """
    # Per-RM staleness: max(datetime_iso) per RM across coverage's classified items
    last_per_rm = con.execute("""
        SELECT n.symbol, MAX(n.datetime_iso)
        FROM news_items n
        WHERE n.datetime_iso IS NOT NULL
        GROUP BY n.symbol
    """).fetchall()
    by_rm_latest: dict[str, str] = {}
    for sym, ts in last_per_rm:
        rm = (tickers.get(sym) or {}).get("rm")
        if not rm:
            continue
        if rm not in by_rm_latest or (ts or "") > by_rm_latest[rm]:
            by_rm_latest[rm] = ts or ""

    now = datetime.now(BKK)
    rm_staleness = []
    for rm, last_ts in sorted(by_rm_latest.items()):
        age_h = None
        try:
            t = datetime.fromisoformat(last_ts.replace("Z", "+00:00"))
            age_h = round((now - t.astimezone(BKK)).total_seconds() / 3600, 1)
        except Exception:  # noqa: BLE001
            pass
        rm_staleness.append({"rm": rm, "last_ts": last_ts, "age_hours": age_h})

    # Unclassified queue
    try:
        unclass_total = con.execute(
            "SELECT COUNT(*) FROM classifications WHERE severity='unclassified'"
        ).fetchone()[0]
        unclass_recent = con.execute("""
            SELECT c.symbol, n.headline, n.datetime_iso
            FROM classifications c
            LEFT JOIN news_items n ON n.id = c.news_id
            WHERE c.severity='unclassified'
            ORDER BY n.datetime_iso DESC NULLS LAST
            LIMIT 8
        """).fetchall()
    except duckdb.Error:
        unclass_total = 0
        unclass_recent = []

    # Coverage-gap: out-of-coverage symbols seen in news_items in the last 14d
    cov_set = set(tickers.keys())
    last_14d = (datetime.now() - timedelta(days=14)).isoformat()
    seen_recent = con.execute(
        "SELECT symbol, COUNT(*) FROM news_items WHERE datetime_iso >= ? GROUP BY 1",
        [last_14d],
    ).fetchall()
    # Anything we see classifications for that's NOT in tickers.json
    gap = [
        {"tk": sym, "count_14d": n}
        for sym, n in seen_recent
        if sym and sym not in cov_set
    ]
    gap.sort(key=lambda r: -r["count_14d"])

    _write(DATA_DIR / "diagnostics.json", {
        "asOf": datetime.now(BKK).date().isoformat(),
        "rm_staleness": rm_staleness,
        "unclassified": {
            "total": unclass_total,
            "recent": [
                {"tk": s, "headline": h, "ts": t}
                for s, h, t in unclass_recent
            ],
        },
        "coverage_gap": gap[:30],
    })


def main() -> int:
    if not DB_PATH.exists():
        # Don't zero out the existing committed JSONs just because the DB is
        # missing on this run — that would replace yesterday's good snapshot
        # with empty stubs and break the dashboard. Log loudly and exit 0.
        print(f"[build_external] DB not found at {DB_PATH} — skipping (existing JSONs left in place).")
        return 0

    tickers = _load_tickers()
    print(f"[build_external] DB: {DB_PATH}  tickers: {len(tickers)}")
    con = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        build_external_news(con, tickers)
        build_trading_signs(con, tickers)
        build_sec_enforcement(con, tickers)
        build_sec_form59(con, tickers)
        build_diagnostics(con, tickers)
    finally:
        con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
