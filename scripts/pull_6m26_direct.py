"""Build 6M26-direct.csv by directly pulling SET FS XLSX income statements.

Bypasses user DB "01 Sale" column (basis inconsistencies) and reads actual
SET income statement to get the correct RFO basis per ticker.
"""
import sys, zipfile, io, re, json
from pathlib import Path
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'surveillance')
from client import SetNewsClient
import harvest_download as hd
import openpyxl, xlrd

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

q = json.load(open('data/harvest-queue.json'))
fs_targets = {}
for nid, it in q['items'].items():
    if it['kind'] != 'FS': continue
    if not any(t == it['ticker'] for t,_,_ in UNIVERSE): continue
    if it['period'] != '2026Q2': continue
    fs_targets.setdefault(it['ticker'], nid)

print(f'Tickers with FS filing in queue: {len(fs_targets)}')

results = {}
with SetNewsClient() as client:
    for tk, sector, seg in UNIVERSE:
        if tk not in fs_targets:
            results[tk] = {'rfo': None, 'np_total': None, 'np_owners': None, 'basis': 'no FS filing in queue'}
            continue
        nid = fs_targets[tk]
        try:
            detail = hd.fetch_detail(client, nid)
            url = detail['downloadUrl']
            payload = hd.download_bytes(client, url, timeout=60.0)
            zf = zipfile.ZipFile(io.BytesIO(payload))
            fs_member = None
            for member in zf.namelist():
                if 'FINANCIAL' in member.upper() or 'STATEMENT' in member.upper():
                    fs_member = member
                    break
            if not fs_member:
                results[tk] = {'rfo': None, 'np_total': None, 'np_owners': None, 'basis': 'no FINANCIAL_STATEMENTS in ZIP'}
                continue
            content = zf.read(fs_member)

            if fs_member.lower().endswith('.xlsx'):
                wb2 = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
                sheet_names = wb2.sheetnames
                get_sheet = lambda name: wb2[name]
                iter_rows = lambda ws: ws.iter_rows(values_only=True)
            elif fs_member.lower().endswith('.xls'):
                wb2 = xlrd.open_workbook(file_contents=content)
                sheet_names = wb2.sheet_names()
                get_sheet = lambda name: wb2.sheet_by_name(name)
                iter_rows = lambda ws: ([ws.cell_value(r, c) for c in range(ws.ncols)] for r in range(ws.nrows))
            else:
                results[tk] = {'rfo': None, 'np_total': None, 'np_owners': None, 'basis': f'unknown format {fs_member}'}
                continue

            best_data = None
            best_sheet_name = None
            for sn in sheet_names:
                sn_lower = sn.lower()
                if 'pl' not in sn_lower: continue
                # Prefer 6M sheets
                if '6m' in sn_lower or '7-8' in sn_lower or '3m' in sn_lower or '5-6' in sn_lower:
                    ws2 = get_sheet(sn)
                    best_data = list(iter_rows(ws2))
                    best_sheet_name = sn
                    break
            if best_data is None:
                for sn in sheet_names:
                    if 'pl' in sn.lower():
                        ws2 = get_sheet(sn)
                        best_data = list(iter_rows(ws2))
                        best_sheet_name = sn
                        break

            if best_data is None:
                results[tk] = {'rfo': None, 'np_total': None, 'np_owners': None, 'basis': 'no PL sheet found'}
                continue

            rfo_val = rfo_basis = None
            np_total = np_owners = None
            for row in best_data[:50]:
                if not row or not any(row): continue
                row_str = ' | '.join(str(v) if v is not None else '' for v in row)
                row_lower = row_str.lower()
                if rfo_val is None and ('revenue' in row_lower or 'sales' in row_lower):
                    nums = []
                    for v in row:
                        if isinstance(v, (int, float)) and v > 100:
                            nums.append(v)
                    if nums:
                        rfo_val = max(nums)
                        if 'total' in row_lower:
                            rfo_basis = 'total_revenues'
                        elif 'rental' in row_lower or 'service' in row_lower:
                            rfo_basis = 'rental_services_or_sale'
                        else:
                            rfo_basis = 'revenue_or_sales'
                if 'profit for the period' in row_lower:
                    nums = [v for v in row if isinstance(v, (int, float)) and v > 100]
                    if nums and np_total is None:
                        np_total = max(nums)
                if 'owners' in row_lower and 'parent' in row_lower:
                    nums = [v for v in row if isinstance(v, (int, float)) and v > 100]
                    if nums:
                        np_owners = nums[0]

            results[tk] = {
                'rfo': rfo_val / 1000 if rfo_val else None,
                'np_total': np_total / 1000 if np_total else None,
                'np_owners': np_owners / 1000 if np_owners else None,
                'basis': rfo_basis,
            }
            wb2.close()
        except Exception as e:
            results[tk] = {'rfo': None, 'np_total': None, 'np_owners': None, 'basis': f'error: {type(e).__name__}: {e}'}

out = Path('6M26-direct.csv')
with open(out, 'w', encoding='utf-8') as f:
    f.write('ticker,sector,segment,rfo_6m26_mb,np_total_6m26_mb,np_owners_6m26_mb,rfo_basis,basis_note\n')
    for tk, sector, seg in UNIVERSE:
        r = results.get(tk, {})
        f.write(f"{tk},{sector},{seg},")
        f.write(f"{r.get('rfo','')},{r.get('np_total','')},{r.get('np_owners','')},{r.get('basis','')},\n")

print(f'\nWrote {out}')
print(f'Total: {len(results)} tickers processed')
n_rfo = sum(1 for r in results.values() if r.get('rfo'))
n_np = sum(1 for r in results.values() if r.get('np_total'))
print(f'With RFO: {n_rfo}/118')
print(f'With NP total: {n_np}/118')
print(f'With NP owners: {sum(1 for r in results.values() if r.get("np_owners"))}/118')

print('\n=== Sample successes ===')
for tk in ['CPF','CPN','TU','BR','KBS','JDF']:
    if tk in results and results[tk].get('rfo'):
        r = results[tk]
        print(f'  {tk}: RFO={r["rfo"]:.1f}, NP_total={r.get("np_total","")}, NP_owners={r.get("np_owners","")}, basis={r["basis"]}')

print('\n=== Sample failures (first 10) ===')
fail_count = 0
for tk, r in results.items():
    if not r.get('rfo'):
        print(f'  {tk}: {r["basis"]}')
        fail_count += 1
        if fail_count >= 10: break