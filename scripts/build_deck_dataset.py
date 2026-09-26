"""Build deck-ready 6M26 dataset combining:
  1. 8 hand-verified spec anchors (highest trust)
  2. User DB values where spec doesn't have anchors
  3. Flags for the 3 basis-discrepancy tickers

Output: 6M26-deck-ready.csv with one row per ticker, all 118 spec companies.
This is the dataset Claude should use for the slide deck.
"""
import openpyxl, json
from pathlib import Path
from collections import defaultdict

DB_PATH = Path('C:/Users/Tasinpong/AppData/Local/hermes/cache/documents/doc_e845f81c5c84_00_Database_all_form.xlsx')
REPO = Path('C:/Users/Tasinpong/projects/is1-coverage-dashboard')

wb = openpyxl.load_workbook(DB_PATH, read_only=True, data_only=True)
ws = wb['All data']

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

# Hand-verified anchors from spec (highest trust)
ANCHORS_6M26 = {
    'CPF':  {'rfo': 283883, 'np_owners': None, 'np_basis': 'unattributed_only', 'src': 'spec_anchor'},
    'CPN':  {'rfo': 25224,  'np_owners': 9721,  'np_basis': 'owners_direct',     'src': 'spec_anchor'},
    'ITC':  {'rfo': 9704,   'np_owners': None, 'np_basis': 'unattributed_only', 'src': 'spec_anchor'},
    'BR':   {'rfo': 3585,   'np_owners': 103,   'np_basis': 'owners_direct',     'src': 'spec_anchor'},
    'PEACE':{'rfo': 634.32, 'np_owners': 35.25, 'np_basis': 'owners_direct',     'src': 'spec_anchor'},
    'JDF':  {'rfo': 394.15, 'np_owners': 53.80, 'np_basis': 'owners_direct',     'src': 'spec_anchor'},
    'BRR':  {'rfo': 3168.53,'np_owners': 238.62,'np_basis': 'owners_direct',     'src': 'spec_anchor'},
    'KBS':  {'rfo': 6426.6, 'np_owners': 615.9, 'np_basis': 'owners_direct',     'src': 'spec_anchor'},
}

# Build DB lookup: 6M26 Accum + 6M25 Accum
db_accum = {}
db_accum_25 = {}
# 6M25 anchors from spec (used for YoY computation)
ANCHORS_6M25_RFO = {'CPF':291770,'CPN':23582,'ITC':8722,'BR':3608,'PEACE':354.40,'JDF':346.94,'BRR':3926.27,'KBS':6472.2}
ANCHORS_6M25_NP  = {'CPN':8532,'BR':63,'PEACE':1.46,'JDF':25.35,'BRR':433.09,'KBS':947.8}

for row in ws.iter_rows(min_row=4, values_only=True):
    if row[1] is None: continue
    sym = row[1]
    if row[2] != 'Accum': continue
    if row[7] == 2026 and row[8] == 2:
        db_accum[sym] = {'rfo': row[9], 'np_total': row[24], 'np_owners': row[25]}
    elif row[7] == 2025 and row[8] == 2:
        db_accum_25[sym] = {'rfo': row[9], 'np_total': row[24], 'np_owners': row[25]}

# Load IS1 universe + queue for vault/file refs
IS1 = {t['tk'] for t in json.load(open(REPO/'data/tickers.json'))['tickers']}
hq = json.load(open(REPO/'data/harvest-queue.json'))
queue_ids = {}
for nid, it in hq['items'].items():
    if it['period'] != '2026Q2': continue
    if it['kind'] == 'FS':
        queue_ids.setdefault(it['ticker'], nid)

# Build deck-ready dataset
out = REPO / '6M26-deck-ready.csv'
with open(out, 'w', encoding='utf-8') as f:
    f.write('ticker,sector,segment,')
    f.write('rfo_6m26_mb,np_total_6m26_mb,np_owners_6m26_mb,')
    f.write('rfo_source,np_basis,')
    f.write('yoy_rfo_pct,yoy_np_pct,')
    f.write('rfo_6m25_mb,np_total_6m25_mb,')
    f.write('in_vault,fs_news_id,notes\n')

    for tk, sector, seg in UNIVERSE:
        # Pull anchor if available, otherwise DB
        anchor = ANCHORS_6M26.get(tk, {})
        db = db_accum.get(tk, {})

        # RFO: use anchor if present, else DB
        if anchor.get('rfo'):
            rfo = anchor['rfo']
            rfo_src = 'spec_anchor_verified'
            notes = 'spec hand-verified'
        elif db.get('rfo'):
            rfo = db['rfo']
            rfo_src = 'db_01_sale_basis'
            notes = 'unverified vs SET FS — verify before use'
        else:
            rfo = None
            rfo_src = 'missing'
            notes = 'no source available'

        # NP owners: use anchor if present, else DB NPMaj, else DB NP total
        np_owners = None
        np_basis = ''
        if anchor.get('np_owners'):
            np_owners = anchor['np_owners']
            np_basis = anchor['np_basis']
        elif db.get('np_owners') is not None:
            np_owners = db['np_owners']
            np_basis = 'owners_direct'
        elif db.get('np_total') is not None:
            np_owners = db['np_total']
            np_basis = 'unattributed_only'
            notes = notes + '; NP unattributed' if notes else 'NP unattributed'

        np_total = db.get('np_total')

        # Vault file
        fs_dir = Path('C:/Users/Tasinpong/OneDrive - The Stock Exchange of Thailand/Claude-Vault/Work-SET/Listed Company/1-Raw/01-Filings/FS-NOTES') / tk
        in_vault = fs_dir.is_dir() and any(fs_dir.glob(f'NOTES_{tk}_2026Q2*.md'))

        # News ID from queue
        nid = queue_ids.get(tk, '')

        # 6M25 from DB (pre-loaded) or spec anchor
        db_25 = db_accum_25.get(tk, {})
        rfo_6m25 = ANCHORS_6M25_RFO.get(tk) or db_25.get('rfo')
        np_6m25 = ANCHORS_6M25_NP.get(tk) or db_25.get('np_total') or db_25.get('np_owners')

        # YoY %
        yoy_rfo = ''
        if rfo and rfo_6m25:
            yoy_rfo = f"{(rfo - rfo_6m25) / rfo_6m25 * 100:.2f}"
        yoy_np = ''
        if np_owners and np_6m25 and np_6m25 != 0:
            yoy_np = f"{(np_owners - np_6m25) / np_6m25 * 100:.2f}"

        def fmt(v):
            return f"{v:.2f}" if v is not None else ''
        f.write(f"{tk},{sector},{seg},")
        f.write(f"{fmt(rfo)},{fmt(np_total)},{fmt(np_owners)},")
        f.write(f"{rfo_src},{np_basis},")
        f.write(f"{yoy_rfo},{yoy_np},")
        f.write(f"{fmt(rfo_6m25)},{fmt(np_6m25)},")
        f.write(f"{'yes' if in_vault else 'no'},{nid},{notes}\n")

print(f'Wrote {out}')

# Summary
import csv
with open(out, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
print(f'Total rows: {len(rows)}')
n_with_rfo = sum(1 for r in rows if r['rfo_6m26_mb'])
n_with_np = sum(1 for r in rows if r['np_owners_6m26_mb'])
n_anchor = sum(1 for r in rows if r['rfo_source'] == 'spec_anchor_verified')
n_in_vault = sum(1 for r in rows if r['in_vault'] == 'yes')
print(f'With RFO: {n_with_rfo}/118 (anchor: {n_anchor}, DB: {118-n_anchor})')
print(f'With NP owners: {n_with_np}/118')
print(f'In vault (FS): {n_in_vault}/118')

# Segment rollup
print('\n=== Segment rollup (for slide 5) ===')
SEG_NAMES = {
    'F1':'F1 Animal protein','F2':'F2 Seafood','F3':'F3 Pet food','F4':'F4 Beverages',
    'F5':'F5 Restaurants','F6':'F6 Snacks/bakery','F7':'F7 Ingredients','F8':'F8 Sugar/oils',
    'F9':'F9 Processed ag',
    'P1':'P1 Residential','P2':'P2 Industrial','P3':'P3 Retail/commercial','P4':'P4 Hospitality','P5':'P5 Diversified',
}
by_seg = defaultdict(lambda: {'count':0, 'rfo':0, 'rfo_25':0, 'np':0})
for r in rows:
    seg = r['segment']
    by_seg[seg]['count'] += 1
    try: by_seg[seg]['rfo'] += float(r['rfo_6m26_mb']) if r['rfo_6m26_mb'] else 0
    except: pass
    try: by_seg[seg]['rfo_25'] += float(r['rfo_6m25_mb']) if r['rfo_6m25_mb'] else 0
    except: pass
    try: by_seg[seg]['np'] += float(r['np_owners_6m26_mb']) if r['np_owners_6m26_mb'] else 0
    except: pass

for seg in sorted(by_seg.keys()):
    s = by_seg[seg]
    yoy_rfo = (s['rfo'] - s['rfo_25']) / s['rfo_25'] * 100 if s['rfo_25'] > 0 else 0
    print(f'  {seg} {SEG_NAMES[seg]:25} count={s["count"]:>3} RFO_6M26={s["rfo"]:>10,.0f}mb YoY={yoy_rfo:+5.1f}%')

wb.close()