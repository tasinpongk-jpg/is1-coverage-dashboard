import sys
import unittest
from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "surveillance"))

import external_sources as sources  # noqa: E402


def form59_html(updated: str) -> str:
    return f"""
    <html><body>
      <p>Last updated on {updated}</p>
      <table>
        <tr>
          <th>Name of Company</th><th>Name of Management</th>
          <th>Relationship to Management</th><th>Types of Securities</th>
          <th>Transaction Date</th><th>Amount</th><th>Average Price (baht)</th>
          <th>The methods of Acquisition/Disposition</th><th>Remark</th>
        </tr>
        <tr>
          <td>CENTRAL PATTANA PUBLIC COMPANY LIMITED (CPN)</td>
          <td>Test Reporter</td><td>Reporter</td><td>Common Share</td>
          <td>21/07/2026</td><td>1,200</td><td>55.25</td>
          <td>Purchase</td>
          <td><a href="/r59/th/report?id=1">Link</a></td>
        </tr>
        <tr>
          <td>OUTSIDE COVERAGE PUBLIC COMPANY LIMITED (ZZZZ)</td>
          <td>Outside Reporter</td><td>Reporter</td><td>Common Share</td>
          <td>21/07/2026</td><td>10</td><td>1.00</td><td>Sale</td><td></td>
        </tr>
      </table>
    </body></html>
    """


class Form59ParsingTests(unittest.TestCase):
    def test_parses_ad_and_be_dates(self):
        self.assertEqual(sources._parse_form59_date("21/07/2026"), "2026-07-21")
        self.assertEqual(sources._parse_form59_date("21/07/2569"), "2026-07-21")

    def test_filters_to_coverage_and_normalizes_row(self):
        rows = sources._extract_form59_rows(
            form59_html("22 July 2026"),
            lang="en",
            source_url=sources.SEC_R59_PAGES[0][1],
        )
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["symbol"], "CPN")
        self.assertEqual(row["transaction_date"], "2026-07-21")
        self.assertIsNone(row["filing_date"])
        self.assertEqual(row["source_as_of"], "2026-07-22")
        self.assertEqual(row["amount"], 1200.0)
        self.assertEqual(row["price"], 55.25)
        self.assertEqual(row["side"], "buy")
        self.assertTrue(row["detail_url"].startswith("https://market.sec.or.th/"))

    def test_row_id_does_not_change_with_snapshot_refresh_date(self):
        first = sources._extract_form59_rows(
            form59_html("22 July 2026"), lang="en", source_url=sources.SEC_R59_PAGES[0][1]
        )[0]
        second = sources._extract_form59_rows(
            form59_html("23 July 2026"), lang="en", source_url=sources.SEC_R59_PAGES[0][1]
        )[0]
        self.assertEqual(first["id"], second["id"])

    def test_removes_legacy_rows_with_the_same_natural_transaction_key(self):
        c = duckdb.connect(":memory:")
        c.execute(
            """
            CREATE TABLE sec_form59 (
                id VARCHAR, symbol VARCHAR, transaction_date VARCHAR,
                reporter VARCHAR, relationship VARCHAR, security_type VARCHAR,
                amount DOUBLE, price DOUBLE, side VARCHAR, side_label VARCHAR,
                remark VARCHAR, is_revoked BOOLEAN, detail_url VARCHAR,
                scraped_at TIMESTAMP
            )
            """
        )
        values = (
            "CPN", "2026-07-21", "Test Reporter", "Reporter", "Common Share",
            1200.0, 55.25, "buy", "Purchase", "Link", False,
            "https://market.sec.or.th/r59/report?id=1",
        )
        c.execute("INSERT INTO sec_form59 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ("legacy", *values, "2026-07-22 01:00:00"))
        c.execute("INSERT INTO sec_form59 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ("stable", *values, "2026-07-23 01:00:00"))

        self.assertEqual(sources._dedupe_form59_store(c), 1)
        self.assertEqual(c.execute("SELECT id FROM sec_form59").fetchall(), [("stable",)])
        c.close()


if __name__ == "__main__":
    unittest.main()
