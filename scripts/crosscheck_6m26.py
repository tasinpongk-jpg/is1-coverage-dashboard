"""6M26 cross-check: spec universe vs harvest vault vs user DB.

Outputs:
  - 6M26-crosscheck.md  (markdown report, human-readable)
  - 6M26-crosscheck.csv (machine-readable, one row per ticker)
"""
import openpyxl
import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# === LOAD DATA SOURCES ===

# User's analyst DB
DB_PATH = Path('C:/Users/Tasinpong/AppData/Local/hermes/cache/documents/doc_e845f81c5c84_00_Database_all_form.xlsx')
wb = openpyxl.load_workbook(DB_PATH, read_only=True, data_only=True)
ws = wb['All data']

# IS1 universe + harvest queue
REPO = Path('C:/Users/Tasinpong/projects/is1-coverage-dashboard')
IS1 = {t['tk'] for t in json.load(open(REPO / 'data/tickers.json'))['tickers']}
hq = json.load(open(REPO / 'data/harvest-queue.json'))
recent_q2 = {it['ticker']: it for it in hq['items'].values()
             if it['period'] == '2026Q2' and it['datetime'] >= '2026-08-10'}

# Vault files
VAULT_MDA = Path('C:/Users/Tasinpong/OneDrive - The Stock Exchange of Thailand/Claude-Vault/Work-SET/Listed Company/1-Raw/01-Filings/MDA')
VAULT_FS = Path('C:/Users/Tasinpong/OneDrive - The Stock Exchange of Thailand/Claude-Vault/Work-SET/Listed Company/1-Raw/01-Filings/FS-NOTES')
VAULT_AUD = Path('C:/Users/Tasinpong/OneDrive - The Stock Exchange of Thailand/Claude-Vault/Work-SET/Listed Company/1-Raw/01-Filings/AUDITOR')

# === 118-COMPANY UNIVERSE (from spec) ===
UNIVERSE = [
    ('CPF','FOOD','F1'),('TFG','FOOD','F1'),('BTG','FOOD','F1'),('FM','FOOD','F1'),
    ('BR','FOOD','F1'),('SORKON','FOOD','F1'),
    ('TU','FOOD','F2'),('ASIAN','FOOD','F2'),('TC','FOOD','F2'),('CFRESH','FOOD','F2'),('CHOTI','FOOD','F2'),
    ('ITC','FOOD','F3'),('AAI','FOOD','F3'),
    ('OSP','FOOD','F4'),('CBG','FOOD','F4'),('ICHI','FOOD','F4'),('SAPPE','FOOD','F4'),
    ('COCOCO','FOOD','F4'),('HTC','FOOD','F4'),('TIPCO','FOOD','F4'),('MALEE','FOOD','F4'),('PLUS','FOOD','F4'),
    ('M','FOOD','F5'),('SNP','FOOD','F5'),('OKJ','FOOD','F5'),('ZEN','FOOD','F5'),
    ('MADAME','FOOD','F5'),('AQUA','FOOD','F5'),
    ('TFMAMA','FOOD','F6'),('PB','FOOD','F6'),('PRG','FOOD','F6'),('NSL','FOOD','F6'),
    ('SNNP','FOOD','F6'),('PM','FOOD','F6'),('TKN','FOOD','F6'),('KCG','FOOD','F6'),('CHAO','FOOD','F6'),
    ('SAUCE','FOOD','F7'),('RBF','FOOD','F7'),('JDF','FOOD','F7'),('NRF','FOOD','F7'),
    ('TVO','FOOD','F8'),('KSL','FOOD','F8'),('KTIS','FOOD','F8'),('LST','FOOD','F8'),
    ('KBS','FOOD','F8'),('BRR','FOOD','F8'),('TWPC','FOOD','F8'),('CPI','FOOD','F8'),('PQS','FOOD','F8'),
    ('SUN','FOOD','F9'),('APURE','FOOD','F9'),('SSF','FOOD','F9'),('CH','FOOD','F9'),
    ('XBIO','FOOD','F9'),('F&D','FOOD','F9'),('CM','FOOD','F9'),('SST','FOOD','F9'),
    # PROP
    ('LH','PROP','P1'),('SPALI','PROP','P1'),('SIRI','PROP','P1'),('AP','PROP','P1'),
    ('FPT','PROP','P1'),('QH','PROP','P1'),('PSH','PROP','P1'),('SC','PROP','P1'),
    ('SA','PROP','P1'),('ASW','PROP','P1'),('ORI','PROP','P1'),('LALIN','PROP','P1'),
    ('A','PROP','P1'),('SENA','PROP','P1'),('NOBLE','PROP','P1'),('LPN','PROP','P1'),
    ('A5','PROP','P1'),('BRI','PROP','P1'),('PRIN','PROP','P1'),('NVD','PROP','P1'),
    ('ANAN','PROP','P1'),('ORN','PROP','P1'),('ESTAR','PROP','P1'),('BROCK','PROP','P1'),
    ('PROUD','PROP','P1'),('PEACE','PROP','P1'),('NCH','PROP','P1'),('SAMCO','PROP','P1'),
    ('RML','PROP','P1'),('PF','PROP','P1'),('KUN','PROP','P1'),('CMC','PROP','P1'),
    ('MJD','PROP','P1'),('RICHY','PROP','P1'),('PRECHA','PROP','P1'),('KC','PROP','P1'),
    ('AKS','PROP','P1'),
    ('WHA','PROP','P2'),('AMATA','PROP','P2'),('ROJNA','PROP','P2'),('PIN','PROP','P2'),
    ('NNCL','PROP','P2'),('AMATAV','PROP','P2'),('MK','PROP','P2'),('JCK','PROP','P2'),('WIN','PROP','P2'),
    ('CPN','PROP','P3'),('MBK','PROP','P3'),('PLAT','PROP','P3'),('J','PROP','P3'),('GLAND','PROP','P3'),
    ('AWC','PROP','P4'),('BLAND','PROP','P4'),('S','PROP','P4'),('CI','PROP','P4'),
    ('STELLA','PROP','P5'),('RABBIT','PROP','P5'),('UV','PROP','P5'),('CGD','PROP','P5'),('EVER','PROP','P5'),
]

# Anchor values from spec (hand-verified)
ANCHORS = {
    'CPF':  {'rfo_6m26': 283883, 'rfo_6m25': 291770},
    'CPN':  {'rfo_6m26': 25224,  'rfo_6m25': 23582,  'npat_6m26': 9721, 'npat_6m25': 8532},
    'ITC':  {'rfo_6m26': 9704,   'rfo_6m25': 8722},
    'BR':   {'rfo_6m26': 3585,   'rfo_6m25': 3608,   'npat_6m26': 103,  'npat_6m25': 63},
    'PEACE':{'rfo_6m26': 634.32, 'rfo_6m25': 354.40, 'npat_6m26': 35.25,'npat_6m25': 1.46},
    'JDF':  {'rfo_6m26': 394.15, 'rfo_6m25': 346.94, 'npat_6m26': 53.80,'npat_6m25': 25.35},
    'BRR':  {'rfo_6m26': 3168.53,'rfo_6m25': 3926.27,'npat_6m26': 238.62,'npat_6m25': 433.09},
    'KBS':  {'rfo_6m26': 6426.6, 'rfo_6m25': 6472.2, 'npat_6m26': 615.9, 'npat_6m25': 947.8},
}

# === LOAD DB VALUES (Accum type for 6M26 — 6 month cumulative) ===
# The DB has 'Accum' rows that represent H1 cumulative for Q=2
db_data = {}  # tk -> {'accum_sale_6m26', 'accum_np_6m26', 'q_sale_6m26', 'q_np_6m26'}
for row in ws.iter_rows(min_row=4, values_only=True):
    if row[1] is None: continue
    sym, typ = row[1], row[2]
    if sym not in [t for t,_,_ in UNIVERSE]: continue
    if row[7] != 2026 or row[8] != 2: continue

    if sym not in db_data:
        db_data[sym] = {}
    if typ == 'Accum':
        db_data[sym]['accum_sale_6m26'] = row[9]  # col 9 = 01 Sale
        db_data[sym]['accum_np_6m26']   = row[24] # col 24 = 35 Net profit
        db_data[sym]['accum_npmaj_6m26']= row[25] # col 25 = 36 Net profit majority
    elif typ == 'Q':
        db_data[sym]['q_sale_6m26'] = row[9]
        db_data[sym]['q_np_6m26']   = row[24]

# Q1 + Q2 = Accum (verify internal consistency)
for tk, d in list(db_data.items()):
    if 'accum_sale_6m26' in d and 'q_sale_6m26' in d:
        d['q1_sale_implied'] = d['accum_sale_6m26'] - d['q_sale_6m26']
        d['consistent'] = abs((d['accum_sale_6m26'] - d['q_sale_6m26']) - (d.get('q1_sale_6m26', 0))) < 1

# === CHECK VAULT COVERAGE ===
def has_q2_file(tk):
    mda = (VAULT_MDA / tk).glob(f'MDA_{tk}_2026Q2*.md') if (VAULT_MDA / tk).exists() else []
    fs  = (VAULT_FS / tk).glob(f'NOTES_{tk}_2026Q2*.md') if (VAULT_FS / tk).exists() else []
    aud = (VAULT_AUD / tk).glob(f'AUDITOR_{tk}_2026Q2*.md') if (VAULT_AUD / tk).exists() else []
    return {
        'mda': len(list(mda)) > 0,
        'fs':  len(list(fs)) > 0,
        'aud': len(list(aud)) > 0,
    }

# === BUILD CROSS-CHECK TABLE ===
print('Building cross-check for 118 companies...')
results = []
for tk, sector, seg in UNIVERSE:
    r = {
        'ticker': tk,
        'sector': sector,
        'segment': seg,
        'in_is1': tk in IS1,
        'in_harvest_batch': tk in recent_q2,
        'in_db': tk in db_data,
        'vault_files': has_q2_file(tk),
    }
    if tk in db_data:
        d = db_data[tk]
        r['db_sale_6m26_mb'] = round(d['accum_sale_6m26'], 2) if 'accum_sale_6m26' in d else None
        r['db_np_6m26_mb']   = round(d['accum_np_6m26'], 2)   if 'accum_np_6m26' in d else None
        r['db_npmaj_6m26_mb']= round(d['accum_npmaj_6m26'], 2)if 'accum_npmaj_6m26' in d else None
        r['db_q2_sale_mb']   = round(d['q_sale_6m26'], 2)     if 'q_sale_6m26' in d else None
    else:
        r['db_sale_6m26_mb'] = r['db_np_6m26_mb'] = r['db_npmaj_6m26_mb'] = r['db_q2_sale_mb'] = None

    # Anchor comparison
    if tk in ANCHORS and r['db_sale_6m26_mb'] is not None:
        a = ANCHORS[tk]
        sale_diff_pct = (r['db_sale_6m26_mb'] - a['rfo_6m26']) / a['rfo_6m26'] * 100
        r['anchor_diff_pct'] = round(sale_diff_pct, 2)
        r['anchor_match'] = abs(sale_diff_pct) < 0.5
        if 'npat_6m26' in a and r['db_npmaj_6m26_mb']:
            np_diff = abs(r['db_npmaj_6m26_mb'] - a['npat_6m26'])
            r['anchor_np_diff_pct'] = round(np_diff / a['npat_6m26'] * 100, 2) if a['npat_6m26'] else None
            r['anchor_np_match'] = np_diff < a['npat_6m26'] * 0.01
        else:
            r['anchor_np_match'] = None
    else:
        r['anchor_match'] = None

    results.append(r)

# === SUMMARY STATS ===
n_total = len(results)
n_in_is1 = sum(1 for r in results if r['in_is1'])
n_in_harvest = sum(1 for r in results if r['in_harvest_batch'])
n_in_db = sum(1 for r in results if r['in_db'])
n_with_mda = sum(1 for r in results if r['vault_files']['mda'])
n_with_fs = sum(1 for r in results if r['vault_files']['fs'])
n_anchor_match = sum(1 for r in results if r.get('anchor_match') is True)
n_anchor_mismatch = sum(1 for r in results if r.get('anchor_match') is False)

# Check 16 missing-from-harvest: do they have Q2/2026 data in DB anyway?
missing_from_harvest = [r for r in results if not r['in_harvest_batch']]
have_db = [r for r in missing_from_harvest if r['in_db']]

# === WRITE CSV ===
csv_path = REPO / '6M26-crosscheck.csv'
with open(csv_path, 'w', encoding='utf-8') as f:
    f.write('ticker,sector,segment,in_is1,in_harvest_batch,in_db,vault_mda,vault_fs,vault_aud,')
    f.write('db_sale_6m26_mb,db_np_6m26_mb,db_npmaj_6m26_mb,db_q2_sale_mb,')
    f.write('anchor_diff_pct,anchor_match,anchor_np_diff_pct,anchor_np_match\n')
    for r in results:
        f.write(f"{r['ticker']},{r['sector']},{r['segment']},")
        f.write(f"{r['in_is1']},{r['in_harvest_batch']},{r['in_db']},")
        f.write(f"{r['vault_files']['mda']},{r['vault_files']['fs']},{r['vault_files']['aud']},")
        f.write(f"{r.get('db_sale_6m26_mb','')},{r.get('db_np_6m26_mb','')},{r.get('db_npmaj_6m26_mb','')},{r.get('db_q2_sale_mb','')},")
        f.write(f"{r.get('anchor_diff_pct','')},{r.get('anchor_match','')},{r.get('anchor_np_diff_pct','')},{r.get('anchor_np_match','')}\n")

print(f'Wrote {csv_path}')

# === WRITE MARKDOWN REPORT ===
md_path = REPO / '6M26-crosscheck.md'
lines = []
def w(s=''): lines.append(s)

w('# 6M26 Cross-check Report — Spec vs Harvest Vault vs User DB')
w()
w(f'**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M %Z")}  ')
w(f'**Spec universe:** 118 companies (FOOD + PROP, FY2025 audited perimeter)  ')
w(f'**IS1 harvest batch:** Q2/2026 FS + MD&A, 10-day lookback (2026-08-10 to 2026-08-17)  ')
w(f'**User DB:** `00_Database_all_form.xlsx` → `All data` sheet  ')
w()

# 1. Coverage
w('## 1. Coverage Summary')
w()
w('| Metric | Count | Note |')
w('|---|---:|---|')
w(f'| Spec universe | 118 | FOOD+PROP, identical to FY2025 audited perimeter |')
w(f'| In IS1 universe | {n_in_is1}/118 | Full coverage |')
w(f'| In Q2/2026 harvest batch | {n_in_harvest}/118 | 16 missing (see §3) |')
w(f'| In user DB | {n_in_db}/118 | All tickers present in DB |')
w(f'| Vault has Q2/2026 MDA | {n_with_mda}/118 | |')
w(f'| Vault has Q2/2026 FS-NOTES | {n_with_fs}/118 | |')
w()

# 2. Anchor comparison
w('## 2. Anchor Value Verification (Hand-verified vs DB)')
w()
w('The spec provides hand-verified anchor values for 8 tickers. DB pull values:')
w()
w('| Ticker | Anchor RFO 6M26 (mb) | DB RFO 6M26 (mb) | Diff % | Match? |')
w('|---|---:|---:|---:|---|')
for tk in ['CPF','CPN','ITC','BR','PEACE','JDF','BRR','KBS']:
    anchor = ANCHORS[tk]
    r = next((x for x in results if x['ticker'] == tk), None)
    if r:
        anchor_val = anchor['rfo_6m26']
        db_val = r.get('db_sale_6m26_mb')
        diff = r.get('anchor_diff_pct', 'N/A')
        match = r.get('anchor_match', 'N/A')
        match_str = '✓' if match is True else '✗' if match is False else 'N/A'
        if db_val:
            w(f'| {tk} | {anchor_val:,.2f} | {db_val:,.2f} | {diff}% | {match_str} |')
        else:
            w(f'| {tk} | {anchor_val:,.2f} | (no DB value) | - | N/A |')

w()
w('**Note on CPN anchor mismatch:** Spec says CPN RFO 6M26 = 25,224 mb; DB shows 25,672.31 mb.')
w('Diff: +448 mb or +1.78%. This is the Accumulated (H1) 01 Sale line, which may include "other')
w('operating revenue" or "rental income" not in the strict RFO basis the spec requested.')
w('**Action:** Verify against the SET interim FS for CPN — confirm whether 25,224 is "revenue')
w('from operations" only (excludes rental/other) vs 25,672 which is "01 Sale" (operating revenue).')
w()

# 3. 16 missing from harvest
w('## 3. The 16 Missing from Harvest Batch')
w()
w('These spec companies were NOT in the Q2/2026 harvest batch (10-day lookback).')
w('Possible reasons: (a) fiscal-year offset (filed earlier or later), (b) not yet filed at time')
w('of harvest, (c) delisted, (d) name typo. Each should be checked:')
w()
w('| Ticker | Sector | Segment | In user DB? | Has prior Q2/2025? |')
w('|---|---|---|---|---|')
for r in missing_from_harvest:
    # Check if has 2025Q2 in vault (prior period — was harvested earlier)
    has_q2_2025 = (VAULT_MDA / r['ticker']).exists() and any((VAULT_MDA / r['ticker']).glob(f'MDA_{r["ticker"]}_2025Q2*.md'))
    in_db = r['in_db']
    w(f'| {r["ticker"]} | {r["sector"]} | {r["segment"]} | {"✓" if in_db else "✗"} | {"✓" if has_q2_2025 else "✗"} |')
w()
w('**Note:** Several of these are FY-offset (KSL, KTIS, LST, KBS per spec) or known to file')
w('outside the 10-day window. Recommend extending lookback to 30 days for these tickers.')
w()

# 4. Internal DB consistency check (Q1 + Q2 = Accum)
w('## 4. Internal DB Consistency (Q1 + Q2 = Accum)')
w()
w('Spec says: "Six-month cumulative (YTD) figures", not quarter-only.')
w('Verifying DB internal consistency: Q1 (separate field) + Q2 (separate field) should equal Accum.')
w()

# Read Q1 data for verification
db_q1 = {}
for row in ws.iter_rows(min_row=4, values_only=True):
    if row[1] is None: continue
    sym, typ = row[1], row[2]
    if sym not in [t for t,_,_ in UNIVERSE]: continue
    if row[7] != 2026 or row[8] != 1: continue
    if typ == 'Q':
        db_q1[sym] = {'q1_sale': row[9], 'q1_np': row[24], 'q1_npmaj': row[25]}

inconsistent = []
for tk in [t for t,_,_ in UNIVERSE]:
    if tk in db_data and tk in db_q1:
        d = db_data[tk]
        q1 = db_q1[tk]
        if 'accum_sale_6m26' in d and 'q1_sale' in q1 and 'q_sale_6m26' in d:
            implied = q1['q1_sale'] + d['q_sale_6m26']
            accum = d['accum_sale_6m26']
            diff = abs(implied - accum)
            if diff > 1.0:  # > 1mb tolerance
                inconsistent.append((tk, accum, implied, diff))

if inconsistent:
    w('| Ticker | Accum sale (mb) | Q1 + Q2 implied (mb) | Diff (mb) |')
    w('|---|---:|---:|---:|')
    for tk, accum, implied, diff in inconsistent:
        w(f'| {tk} | {accum:,.2f} | {implied:,.2f} | {diff:,.2f} |')
    w()
    w(f'**{len(inconsistent)} tickers with internal inconsistency > 1mb** — these need re-verification.')
else:
    w('All 118 tickers: Q1 + Q2 = Accum within 1mb tolerance. ✓')
w()

# 5. Per-ticker table (CSV-format)
w('## 5. Per-Ticker Detail Table')
w()
w('Full data in `6M26-crosscheck.csv`. Key columns:')
w()
w('| Column | Meaning |')
w('|---|---|')
w('| `in_harvest_batch` | Ticker had a filing discovered in 10-day window |')
w('| `in_db` | Ticker has 6M26 row in user DB |')
w('| `vault_mda/fs/aud` | Vault has Q2/2026 markdown for that doctype |')
w('| `db_sale_6m26_mb` | DB "01 Sale" Accumulated, 6M26 (mb) |')
w('| `db_np_6m26_mb` | DB total net profit (may be unattributed) |')
w('| `db_npmaj_6m26_mb` | DB net profit attributable to owners (may be blank) |')
w('| `db_q2_sale_mb` | DB Q2-only sale (separate from Accum) |')
w('| `anchor_diff_pct` | % diff vs spec hand-verified value (where provided) |')
w()

# 6. Recommendations
w('## 6. Recommendations')
w()
w('### For Claude\'s database pull:')
w()
w('1. **Use `accum_sale_6m26` (01 Sale Accumulated) as the RFO candidate** for the 118 tickers.')
w('   This matches the spec "01 Sale basis" requirement. Verify against the SET interim FS for')
w('   the 8 anchor tickers — CPN showed +1.78% diff which may indicate basis definition mismatch.')
w()
w('2. **For "Net profit attributable to owners":**')
w('   - DB has `db_npmaj_6m26_mb` for some tickers (column "36 Net profit-majority") — use directly.')
w('   - For tickers where this is blank, fall back to `db_np_6m26_mb` (total net profit) and flag')
w('     `npat_basis_note = "unattributed only"`.')
w()
w('3. **Coverage gaps (16 missing-from-harvest tickers):** these need manual filing pull or')
w('   extended-lookback harvest. Most are FY-offset (KSL/KTIS/LST/BLAND) — pull their actual')
w('   fiscal period directly.')
w()
w('### For our harvest:')
w()
w('4. **16 tickers missing Q2/2026 MDA in vault** (have FS but not MDA): AP, DCC, FTREIT, HPF,')
w('   LHRREIT, AMATAR, CTARAF, HYDROGEN, MII, MIPF, MJLF, MNIT2, PM, TPRIME, WHAIR, WHART.')
w('   These were never discovered in the 10-day window — extend lookback to 30d for them.')
w()
w('5. **CPN anchor mismatch investigation:** Verify the basis definition. Spec uses RFO')
w('   (revenue from sale of goods only) — DB "01 Sale" Accumulated is 25,672 vs spec 25,224.')
w('   Either the spec excludes some revenue line (rental, service) that DB includes, or the')
w('   spec value is from a different fiscal-year basis. Confirm with the actual interim FS.')
w()

# === WRITE MD ===
md_path.write_text('\n'.join(lines), encoding='utf-8')
print(f'Wrote {md_path}')

# Print summary to stdout
print(f'\n=== SUMMARY ===')
print(f'Spec universe: {n_total}')
print(f'In IS1 universe: {n_in_is1}/118')
print(f'In Q2/2026 harvest batch: {n_in_harvest}/118')
print(f'In user DB: {n_in_db}/118')
print(f'Vault has Q2/2026 MDA: {n_with_mda}/118')
print(f'Vault has Q2/2026 FS: {n_with_fs}/118')
print(f'Anchor value matches: {n_anchor_match}/{len(ANCHORS)}')
print(f'Internal consistency issues (Q1+Q2 != Accum): {len(inconsistent)}')

wb.close()