"""Compare canonical SETSMART exports (sample news/*.xlsx) against our DB.

For each row in the SETSMART export, extract the news id from the URL and
check whether it's in news_items. Report:
  - rows present in DB              (firehose poll captured them)
  - rows missing from DB            (firehose missed them — potential bug)
  - rows whose symbol is off-coverage (we'd never expect to capture)

Inputs:  sample news/News (2).xlsx (AGRO), sample news/News (3).xlsx (PROPCON)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import duckdb
import openpyxl

sys.path.insert(0, "surveillance")
from coverage import ALL_TICKERS  # noqa: E402

ID_RX = re.compile(r"/news/(\d+)")

DB = duckdb.connect("surveillance/surveillance.duckdb")
in_db: set[str] = {row[0] for row in DB.execute("SELECT id FROM news_items").fetchall()}

coverage_set = {t.upper() for t in ALL_TICKERS}

files = [
    ("AGRO",    Path("sample news") / "News (2).xlsx"),
    ("PROPCON", Path("sample news") / "News (3).xlsx"),
]

for label, path in files:
    print(f"\n=== {label} — {path.name} ===")
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb["Sheet1"]

    rows: list[tuple[str, str, str, str, str]] = []  # date, sym, src, subject, news_id
    for r in ws.iter_rows(values_only=True):
        if not r or r[0] is None:
            continue
        dt, sym, src, subj, url = (r + (None,) * 5)[:5]
        if not isinstance(url, str):
            continue
        m = ID_RX.search(url)
        if not m:
            continue
        rows.append((str(dt), str(sym), str(src), str(subj), m.group(1)))

    in_cov = [r for r in rows if r[1].upper() in coverage_set]
    off_cov = [r for r in rows if r[1].upper() not in coverage_set]
    found = [r for r in in_cov if r[4] in in_db]
    missed = [r for r in in_cov if r[4] not in in_db]

    print(f"  total disclosures in export:     {len(rows)}")
    print(f"  on-coverage tickers:             {len(in_cov)}")
    print(f"  off-coverage tickers (skipped):  {len(off_cov)}")
    print(f"  captured in DB:                  {len(found)}  ({100*len(found)/max(len(in_cov),1):.1f}% of on-coverage)")
    print(f"  MISSING from DB:                 {len(missed)}")
    if missed:
        print()
        print(f"  --- missing rows ({label}) ---")
        for dt, sym, _src, subj, nid in missed:
            print(f"    {dt}  {sym:8s}  id={nid:>16s}  {subj[:75]}")
    if off_cov:
        # Brief — only show distinct off-coverage symbols
        distinct_off = sorted({r[1] for r in off_cov})
        print(f"  off-coverage symbols seen: {', '.join(distinct_off[:20])}{'...' if len(distinct_off) > 20 else ''}")
