"""DuckDB persistence + dedup for SET disclosure items.

Schema is intentionally narrow at the storage layer — classifier output
goes into a sibling table once the Phase 2 classifier lands.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

import duckdb

# CI sets SURVEILLANCE_DB_PATH to /tmp/surveillance.duckdb (downloaded from R2).
# Local default keeps existing behavior when the env var is unset.
DB_PATH = Path(os.environ.get("SURVEILLANCE_DB_PATH") or
               (Path(__file__).parent / "surveillance.duckdb"))


@contextmanager
def conn() -> Iterator[duckdb.DuckDBPyConnection]:
    c = duckdb.connect(str(DB_PATH))
    try:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS news_items (
                id            VARCHAR PRIMARY KEY,
                symbol        VARCHAR NOT NULL,
                lang          VARCHAR NOT NULL,
                datetime_iso  VARCHAR NOT NULL,
                source        VARCHAR,
                headline      VARCHAR,
                url           VARCHAR,
                product       VARCHAR,
                tag           VARCHAR,
                raw_json      VARCHAR,
                first_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS alerts_sent (
                news_id     VARCHAR NOT NULL,
                channel     VARCHAR NOT NULL,
                tier        VARCHAR NOT NULL,
                sent_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                message_id  VARCHAR,
                PRIMARY KEY (news_id, channel)
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS classifications (
                news_id          VARCHAR PRIMARY KEY,
                symbol           VARCHAR NOT NULL,
                severity         VARCHAR NOT NULL,
                category         VARCHAR NOT NULL,
                summary_en       VARCHAR,
                summary_th       VARCHAR,
                suggested_action VARCHAR,
                rationale        VARCHAR,
                model            VARCHAR,
                input_tokens     INTEGER,
                output_tokens    INTEGER,
                cache_read_tokens  INTEGER,
                cache_write_tokens INTEGER,
                classified_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS title_translations (
                news_id    TEXT PRIMARY KEY,
                title_th   TEXT,
                model      TEXT,
                created_at TIMESTAMP DEFAULT current_timestamp
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS financials_snapshots (
                symbol           VARCHAR NOT NULL,
                year             INTEGER NOT NULL,
                quarter          INTEGER NOT NULL,
                date_as_of       VARCHAR,
                total_revenue_q  DOUBLE,
                ebit_q           DOUBLE,
                net_profit_q     DOUBLE,
                npm_q            DOUBLE,
                op_cash_flow     DOUBLE,
                total_assets     DOUBLE,
                total_liab       DOUBLE,
                total_equity     DOUBLE,
                de_ratio         DOUBLE,
                roe              DOUBLE,
                eps_q            DOUBLE,
                rev_yoy_pct      DOUBLE,
                ebit_yoy_pct     DOUBLE,
                ni_yoy_pct       DOUBLE,
                npm_yoy_bps      DOUBLE,
                ocf_yoy_pct      DOUBLE,
                de_yoy_delta     DOUBLE,
                rev_qoq_pct      DOUBLE,
                ebit_qoq_pct     DOUBLE,
                ni_qoq_pct       DOUBLE,
                npm_qoq_bps      DOUBLE,
                first_seen_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (symbol, year, quarter)
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS price_anomalies (
                symbol         VARCHAR NOT NULL,
                trade_date     VARCHAR NOT NULL,
                close          DOUBLE,
                prior_close    DOUBLE,
                daily_return   DOUBLE,
                stdev_60d      DOUBLE,
                return_z       DOUBLE,
                volume         DOUBLE,
                vol_med_30d    DOUBLE,
                volume_ratio   DOUBLE,
                high_60d       DOUBLE,
                low_60d        DOUBLE,
                is_return_anom BOOLEAN,
                is_volume_anom BOOLEAN,
                is_new_high    BOOLEAN,
                is_new_low     BOOLEAN,
                detected_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (symbol, trade_date)
            )
            """
        )
        # External RSS / wire-news matched to coverage tickers. One row per
        # (source, url) — multi-ticker hits expand into multiple rows.
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS external_news (
                id              VARCHAR NOT NULL,
                source          VARCHAR NOT NULL,
                symbol          VARCHAR NOT NULL,
                sector          VARCHAR,
                datetime_iso    VARCHAR NOT NULL,
                headline        VARCHAR,
                url             VARCHAR,
                body_excerpt    VARCHAR,
                lang            VARCHAR,
                first_seen_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id, symbol)
            )
            """
        )
        # SET trading-sign daily snapshot. Current-state table — one row per
        # active (symbol, sign) pair; cleared and rewritten each scrape.
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS trading_signs (
                symbol          VARCHAR NOT NULL,
                sign            VARCHAR NOT NULL,
                effective_date  VARCHAR,
                reason          VARCHAR,
                scraped_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (symbol, sign)
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS sec_enforcement (
                id              VARCHAR PRIMARY KEY,
                case_no         VARCHAR,
                action_date     VARCHAR,
                respondent      VARCHAR,
                action_type     VARCHAR,
                matched_ticker  VARCHAR,
                description     VARCHAR,
                url             VARCHAR,
                scraped_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS sec_form59 (
                id                VARCHAR PRIMARY KEY,
                symbol            VARCHAR NOT NULL,
                company_name      VARCHAR,
                reporter          VARCHAR,
                relationship      VARCHAR,
                security_type     VARCHAR,
                transaction_date  VARCHAR,
                filing_date       VARCHAR,
                amount            DOUBLE,
                price             DOUBLE,
                side              VARCHAR,
                side_label        VARCHAR,
                remark            VARCHAR,
                is_revoked        BOOLEAN,
                detail_url        VARCHAR,
                source_url        VARCHAR,
                source_lang       VARCHAR,
                raw_json          VARCHAR,
                scraped_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        yield c
    finally:
        c.close()


def insert_new_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Insert items not already in the table; return only the genuinely new ones.

    The firehose endpoint emits one row per (id, symbol) pair, so a single
    news item that tags multiple covered tickers appears multiple times in
    `items`. We keep the first occurrence and skip later duplicates within
    the batch.
    """
    if not items:
        return []
    new_items: list[dict[str, Any]] = []
    seen_in_batch: set[str] = set()
    with conn() as c:
        existing = {
            row[0]
            for row in c.execute(
                "SELECT id FROM news_items WHERE id = ANY (?)",
                [[str(item["id"]) for item in items]],
            ).fetchall()
        }
        for item in items:
            iid = str(item["id"])
            if iid in existing or iid in seen_in_batch:
                continue
            seen_in_batch.add(iid)
            c.execute(
                """
                INSERT INTO news_items
                  (id, symbol, lang, datetime_iso, source, headline, url, product, tag, raw_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    iid,
                    item.get("symbol"),
                    item.get("lang"),
                    item.get("datetime"),
                    item.get("source"),
                    item.get("headline"),
                    item.get("url"),
                    item.get("product"),
                    item.get("tag"),
                    __import__("json").dumps(item, ensure_ascii=False),
                ],
            )
            new_items.append(item)
    return new_items


def stats() -> dict[str, Any]:
    with conn() as c:
        total = c.execute("SELECT COUNT(*) FROM news_items").fetchone()[0]
        per_symbol = c.execute(
            "SELECT symbol, COUNT(*) FROM news_items GROUP BY symbol ORDER BY 2 DESC"
        ).fetchall()
        latest = c.execute(
            "SELECT symbol, datetime_iso, headline FROM news_items "
            "ORDER BY datetime_iso DESC LIMIT 5"
        ).fetchall()
    return {"total": total, "per_symbol": per_symbol, "latest": latest}
