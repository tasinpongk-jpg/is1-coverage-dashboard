"""Update 6M26-deck-ready.csv with TU and ITC direct-from-SET-FS values.

TU 6M26 (Consolidated, from PL 6M sheet, thousand THB):
  Revenue from sales and services: 65,899,364
  Profit attributable to owners of the parent: 2,377,323
  Comparative 6M25: Revenue 63,178,025, Profit owners 2,291,818

ITC 6M26 (Consolidated, from SOI+CI 6M sheet, thousand THB):
  Revenue: 9,703,735 (matches spec anchor 9,704 exactly)
  Profit attributable to owners: 1,715,367
  Comparative 6M25: Revenue 8,949,499
"""
import csv
from pathlib import Path

REPO = Path('C:/Users/Tasinpong/projects/is1-coverage-dashboard')
csv_path = REPO / '6M26-deck-ready.csv'

# Read existing
with open(csv_path, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

# Update TU and ITC
for r in rows:
    if r['ticker'] == 'TU':
        r['rfo_6m26_mb'] = '65899.36'
        r['rfo_6m25_mb'] = '63178.03'
        r['np_owners_6m26_mb'] = '2377.32'
        r['np_total_6m26_mb'] = '2932.48'
        r['np_basis'] = 'owners_direct'
        r['rfo_source'] = 'set_fs_direct'
        r['notes'] = 'pulled from PL 6M sheet, Consolidated, thousand THB'
        # YoY
        rfo = 65899.36
        rfo_25 = 63178.03
        r['yoy_rfo_pct'] = f"{(rfo - rfo_25) / rfo_25 * 100:.2f}"
        np = 2377.32
        np_25 = 2291.82
        r['yoy_np_pct'] = f"{(np - np_25) / np_25 * 100:.2f}"
    elif r['ticker'] == 'ITC':
        r['rfo_6m26_mb'] = '9703.74'
        r['rfo_6m25_mb'] = '8949.50'
        r['np_owners_6m26_mb'] = '1715.37'
        r['np_total_6m26_mb'] = '1715.16'
        r['np_basis'] = 'owners_direct'
        r['rfo_source'] = 'set_fs_direct'
        r['notes'] = 'pulled from SOI+CI 6M sheet, Consolidated; RFO matches spec anchor 9,704 exactly'
        rfo = 9703.74
        rfo_25 = 8949.50
        r['yoy_rfo_pct'] = f"{(rfo - rfo_25) / rfo_25 * 100:.2f}"
        np = 1715.37
        np_25 = 1715.16  # approximate; spec didn't provide 6M25 NP for ITC

# Write back
with open(csv_path, 'w', encoding='utf-8', newline='') as f:
    fieldnames = list(rows[0].keys())
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

print(f'Updated {csv_path}')

# Verify
with open(csv_path, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
for r in rows:
    if r['ticker'] in ('TU','ITC'):
        print(f'\n{r["ticker"]}:')
        print(f'  RFO 6M26: {r["rfo_6m26_mb"]} mb  (source: {r["rfo_source"]})')
        print(f'  RFO 6M25: {r["rfo_6m25_mb"]} mb')
        print(f'  YoY RFO: {r["yoy_rfo_pct"]}%')
        print(f'  NP owners 6M26: {r["np_owners_6m26_mb"]} mb')
        print(f'  YoY NP: {r["yoy_np_pct"]}%')
        print(f'  Notes: {r["notes"]}')

# Update summary too
n_rfo = sum(1 for r in rows if r['rfo_6m26_mb'])
n_np = sum(1 for r in rows if r['np_owners_6m26_mb'])
print(f'\n\nTotal: {len(rows)} tickers, {n_rfo} with RFO, {n_np} with NP')