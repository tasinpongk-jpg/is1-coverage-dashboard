from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from disclosure_thai import _enrich_thai


def _build_fixture(con) -> None:
    con.execute(
        """
        CREATE TABLE news_items (
            id VARCHAR PRIMARY KEY,
            symbol VARCHAR,
            lang VARCHAR,
            datetime_iso VARCHAR,
            headline VARCHAR,
            url VARCHAR
        )
        """
    )
    con.execute(
        """
        CREATE TABLE classifications (
            news_id VARCHAR PRIMARY KEY,
            summary_th VARCHAR
        )
        """
    )
    con.execute(
        """
        CREATE TABLE title_translations (
            news_id TEXT PRIMARY KEY,
            title_th TEXT,
            model TEXT,
            created_at TIMESTAMP DEFAULT current_timestamp
        )
        """
    )
    con.executemany(
        """
        INSERT INTO news_items (id, symbol, lang, datetime_iso, headline, url)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            ("12345678900", "PRG", "en", "2026-07-10T09:00:00", "EN paired title", "https://set.example/en/paired"),
            ("12345678901", "PRG", "th", "2026-07-10T09:00:00", "หัวข้อไทยจาก SET", "https://set.example/th/paired"),
            ("22345678900", "TU", "en", "2026-07-10T08:00:00", "EN-only title", "https://set.example/en/only"),
            ("17786285863310", "CPN", "en", "2026-07-10T07:00:00", "Financial statement id", "https://set.example/en/fs"),
        ],
    )
    con.executemany(
        """
        INSERT INTO classifications (news_id, summary_th)
        VALUES (?, ?)
        """,
        [
            ("12345678900", "สรุปภาษาไทยของคู่ข่าว"),
            ("22345678900", "สรุปภาษาไทยของข่าวไม่มีคู่"),
            ("17786285863310", "สรุปภาษาไทยของงบการเงิน"),
        ],
    )
    con.executemany(
        """
        INSERT INTO title_translations (news_id, title_th, model)
        VALUES (?, ?, ?)
        """,
        [
            ("12345678900", "ไม่ควรใช้เพราะมีคู่ข่าว", "fixture"),
            ("22345678900", "หัวข้อไทยจากคำแปล", "fixture"),
        ],
    )


def test_enrich_thai() -> None:
    con = duckdb.connect(database=":memory:")
    try:
        _build_fixture(con)
        items = [
            {"_id": "12345678900", "title": "EN paired title", "url": "https://set.example/en/paired"},
            {"_id": "22345678900", "title": "EN-only title", "url": "https://set.example/en/only"},
            {"_id": "17786285863310", "title": "Financial statement id", "url": "https://set.example/en/fs"},
        ]

        enriched = _enrich_thai(con, items)
        by_id = {item["_id"]: item for item in enriched}

        paired = by_id["12345678900"]
        assert paired["title_th"] == "หัวข้อไทยจาก SET"
        assert paired["url_th"] == "https://set.example/th/paired"
        assert paired["_summary_th"] == "สรุปภาษาไทยของคู่ข่าว"

        twinless = by_id["22345678900"]
        assert twinless["title_th"] == "หัวข้อไทยจากคำแปล"
        assert "url_th" not in twinless
        assert twinless["_summary_th"] == "สรุปภาษาไทยของข่าวไม่มีคู่"

        financial_statement = by_id["17786285863310"]
        assert "title_th" not in financial_statement
        assert "url_th" not in financial_statement
        assert financial_statement["_summary_th"] == "สรุปภาษาไทยของงบการเงิน"
    finally:
        con.close()


def test_translate_titles_dry_run() -> None:
    with tempfile.TemporaryDirectory() as td:
        db_path = Path(td) / "surveillance.duckdb"
        con = duckdb.connect(str(db_path))
        try:
            _build_fixture(con)
        finally:
            con.close()

        env = os.environ.copy()
        env["SURVEILLANCE_DB_PATH"] = str(db_path)
        env.pop("MINIMAX_API_KEY", None)
        env.pop("GROQ_API_KEY", None)

        result = subprocess.run(
            [sys.executable, "surveillance/translate_titles.py", "--dry-run", "--limit", "10"],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            timeout=30,
        )
        output = result.stdout + result.stderr
        assert result.returncode == 0, output
        assert "Would translate 1 EN-only headline(s):" in result.stdout
        assert "17786285863310" in result.stdout
        assert "22345678900" not in result.stdout


def main() -> int:
    test_enrich_thai()
    test_translate_titles_dry_run()
    print("test_th_enrichment.py OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
