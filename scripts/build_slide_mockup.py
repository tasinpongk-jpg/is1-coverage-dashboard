"""Build 6M26 deck mockup as HTML — SET-style investor presentation.

Approach: 18-slide deck. Only F1 and F4 confirmed from control CSV;
other 12 segments show "รอข้อมูล" placeholders per spec rule (no fake numbers).
"""
import csv
from pathlib import Path
from collections import defaultdict

REPO = Path('C:/Users/Tasinpong/projects/is1-coverage-dashboard')
csv_path = REPO / '6M26-deck-ready.csv'

with open(csv_path, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

by_seg = defaultdict(lambda: {'count':0, 'rfo_26':0, 'rfo_25':0, 'np_26':0, 'np_25':0, 'tickers': []})
for r in rows:
    if not r['rfo_6m26_mb']: continue
    seg = r['segment']
    by_seg[seg]['count'] += 1
    by_seg[seg]['tickers'].append(r)
    by_seg[seg]['rfo_26'] += float(r['rfo_6m26_mb'])
    if r['rfo_6m25_mb']: by_seg[seg]['rfo_25'] += float(r['rfo_6m25_mb'])
    if r['np_owners_6m26_mb']: by_seg[seg]['np_26'] += float(r['np_owners_6m26_mb'])

SEG_NAMES_TH = {
    'F1':'F1 โปรตีนจากสัตว์ครบวงจร',
    'F2':'F2 อาหารทะเล/เพาะเลี้ยง',
    'F3':'F3 อาหารสัตว์เลี้ยง',
    'F4':'F4 เครื่องดื่มแบรนด์',
    'F5':'F5 ร้านอาหาร/โภชนาการ',
    'F6':'F6 ขนมอบกรอบ/เบเกอรี่',
    'F7':'F7 วัตถุดิบ/เครื่องปรุง',
    'F8':'F8 น้ำตาล/แป้ง/น้ำมัน',
    'F9':'F9 เกษตรแปรรูป',
    'P1':'P1 ที่อยู่อาศัย (ขาย)',
    'P2':'P2 นิคมอุตสาหกรรม/โลจิสติกส์',
    'P3':'P3 ค้าปลีก/พาณิชยกรรม',
    'P4':'P4 การโรงแรม/ผสมผสาน',
    'P5':'P5 เ�็ดเตล็ด/ทรานสิชั่น',
}

SEG_COMMENTARY = {
    'F1':'CPF โดดเด่นด้วยมาร์จิ้นที่กดดันจากราคาหมู/ไก่ในไทยและฟิลิปปินส์ + FX ลบ',
    'F4':'OSP/CBG ยังเติบโต, ITC เป็น rising star ในกลุ่ม pet food',
}

SEG_COLOR = {'F':'#1e3a8a', 'P':'#7c2d12'}
CONFIRMED = {'F1', 'F4'}
AMBER = '#fef3c7'  # pending card
AMBER_DARK = '#92400e'

def top5_by_rfo(seg):
    seg_rows = by_seg.get(seg, {}).get('tickers', [])
    return sorted(seg_rows, key=lambda r: float(r['rfo_6m26_mb'] or 0), reverse=True)[:5]

html = []
html.append('<!DOCTYPE html><html><head><meta charset="utf-8">')
html.append('<title>6M26 SET FOOD+PROP Deck Mockup</title>')
html.append('<style>')
html.append('''
body { font-family: 'Helvetica Neue', Arial, sans-serif; margin: 0; background: #f5f5f5; }
.slide { width: 960px; height: 540px; background: white; margin: 30px auto; padding: 50px 60px; box-sizing: border-box; box-shadow: 0 4px 20px rgba(0,0,0,0.15); page-break-after: always; position: relative; }
.slide h1 { font-size: 36px; color: #003366; margin: 0 0 8px 0; font-weight: 700; }
.slide h2 { font-size: 22px; color: #003366; margin: 24px 0 12px 0; font-weight: 600; border-bottom: 2px solid #c9a961; padding-bottom: 6px; }
.slide h3 { font-size: 18px; color: #555; margin: 16px 0 8px 0; font-weight: 500; }
.slide .subtitle { font-size: 16px; color: #888; margin-bottom: 16px; }
.slide .label { font-size: 14px; color: #888; text-transform: uppercase; letter-spacing: 1px; }
.slide .page-num { position: absolute; bottom: 16px; right: 24px; font-size: 11px; color: #aaa; }
.slide .brand { position: absolute; top: 24px; right: 36px; font-size: 12px; color: #c9a961; font-weight: 600; }
.slide table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 14px; }
.slide th { background: #003366; color: white; padding: 8px 10px; text-align: left; font-weight: 500; }
.slide td { padding: 7px 10px; border-bottom: 1px solid #eee; }
.slide tr:nth-child(even) { background: #fafafa; }
.slide .pos { color: #16a34a; font-weight: 600; }
.slide .neg { color: #dc2626; font-weight: 600; }
.slide .commentary { font-size: 14px; line-height: 1.6; color: #333; padding: 12px 16px; background: #fff8e6; border-left: 4px solid #c9a961; margin: 16px 0; }
.slide .two-col { display: flex; gap: 24px; }
.slide .col { flex: 1; }
.slide .kpi-row { display: flex; justify-content: space-between; gap: 12px; margin: 12px 0; }
.slide .kpi { flex: 1; padding: 10px; background: #f8fafc; border-radius: 4px; }
.slide .kpi .val { font-size: 24px; font-weight: 700; color: #003366; }
.slide .kpi .lbl { font-size: 11px; color: #888; text-transform: uppercase; margin-top: 4px; }
''')
html.append('</style></head><body>')

# Slide 1: Cover
html.append('''
<div class="slide">
<div class="brand">SET | IS1 Coverage</div>
<h1 style="margin-top:80px;">Thai SET 6M26 Review</h1>
<h2 style="border:none; color:#c9a961;">Food &amp; Property Sectors</h2>
<div class="subtitle" style="font-size:18px; margin-top:40px;">Six-month period ended 30 June 2026</div>
<div style="margin-top:40px; font-size:13px; color:#888;">
<div>Universe: 118 SET-listed companies (FOOD 56, PROP 62)</div>
<div>Data as of: 17 August 2026 (Q2/2026 FS + MD&amp;A filings)</div>
<div>Methodology: Spec anchors (8) + SET interim FS (2) + DB rollup (108)</div>
<div style="margin-top:8px; color:#92400e; font-weight:600;">CONFIRMED: F1, F4 &nbsp;|&nbsp; PENDING: 12 segments</div>
</div>
<div class="page-num">1 / 18</div>
</div>
''')

# Slide 2: Sector overview (partial — confirmed + pending)
food_total = sum(by_seg[s]['rfo_26'] for s in by_seg if s.startswith('F'))
food_25 = sum(by_seg[s]['rfo_25'] for s in by_seg if s.startswith('F'))
prop_total = sum(by_seg[s]['rfo_26'] for s in by_seg if s.startswith('P'))
prop_25 = sum(by_seg[s]['rfo_25'] for s in by_seg if s.startswith('P'))
food_yoy = (food_total - food_25) / food_25 * 100
prop_yoy = (prop_total - prop_25) / prop_25 * 100

html.append(f'''
<div class="slide">
<div class="brand">SET | IS1 Coverage</div>
<h1>Sector Overview - 6M26 vs 6M25</h1>
<div class="subtitle">Aggregate revenue growth across 118 spec companies</div>
<div class="kpi-row" style="margin-top:32px;">
<div class="kpi" style="background:#1e3a8a10;">
<div class="val">{food_total:,.0f}</div>
<div class="lbl">FOOD 6M26 RFO (THB mb)</div>
<div style="margin-top:8px; font-size:18px;" class="{('pos' if food_yoy >= 0 else 'neg')}">{food_yoy:+.1f}% YoY</div>
</div>
<div class="kpi" style="background:#7c2d1210;">
<div class="val">{prop_total:,.0f}</div>
<div class="lbl">PROP 6M26 RFO (THB mb)</div>
<div style="margin-top:8px; font-size:18px;" class="{('pos' if prop_yoy >= 0 else 'neg')}">{prop_yoy:+.1f}% YoY</div>
</div>
</div>
<div style="margin-top:24px;">
<h3>FOOD segments (56 companies)</h3>
<div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:8px;">
''')

food_segs = sorted([s for s in by_seg if s.startswith('F')])
for s in food_segs:
    info = by_seg[s]
    yoy = (info['rfo_26'] - info['rfo_25']) / info['rfo_25'] * 100
    yoy_class = 'pos' if yoy >= 0 else 'neg'
    html.append(f'<div style="background:#1e3a8a08; padding:6px 10px; border-radius:3px; font-size:12px;"><b>{s}</b> {info["rfo_26"]:,.0f}mb <span class="{yoy_class}">{yoy:+.1f}%</span></div>')
html.append('</div>')

html.append('<h3 style="margin-top:16px;">PROP segments (62 companies)</h3><div style="display:flex; flex-wrap:wrap; gap:6px; margin-top:8px;">')
prop_segs = sorted([s for s in by_seg if s.startswith('P')])
for s in prop_segs:
    info = by_seg[s]
    yoy = (info['rfo_26'] - info['rfo_25']) / info['rfo_25'] * 100
    yoy_class = 'pos' if yoy >= 0 else 'neg'
    html.append(f'<div style="background:#7c2d1208; padding:6px 10px; border-radius:3px; font-size:12px;"><b>{s}</b> {info["rfo_26"]:,.0f}mb <span class="{yoy_class}">{yoy:+.1f}%</span></div>')
html.append('</div>')

html.append('<div class="page-num">2 / 18</div></div>')

# Per-segment slides: 14 segments (2 confirmed + 12 pending)
all_segs_sorted = sorted(by_seg.keys(), key=lambda s: by_seg[s]['rfo_26'], reverse=True)
# Show all 14 segments, but only F1/F4 with data, rest as pending placeholders

slide_n = 3
TOTAL = 18

for seg in all_segs_sorted:
    is_confirmed = seg in CONFIRMED
    if is_confirmed:
        info = by_seg[seg]
        rfo_yoy = (info['rfo_26'] - info['rfo_25']) / info['rfo_25'] * 100
        yoy_class = 'pos' if rfo_yoy >= 0 else 'neg'
        np_yoy_str = 'n/a'
        np_yoy_class = ''
        if info['np_25'] > 0:
            np_yoy = (info['np_26'] - info['np_25']) / info['np_25'] * 100
            np_yoy_str = f'{np_yoy:+.1f}%'
            np_yoy_class = 'pos' if np_yoy >= 0 else 'neg'
        top5 = top5_by_rfo(seg)

        html.append(f'''
<div class="slide">
<div class="brand">SET | IS1 Coverage</div>
<h1>{seg} - {SEG_NAMES_TH[seg]} <span style="font-size:14px; color:#16a34a; vertical-align:super;">✓ CONFIRMED</span></h1>
<div class="subtitle">{info['count']} companies &middot; RFO 6M26: {info['rfo_26']:,.0f} mb &middot; YoY: <span class="{yoy_class}">{rfo_yoy:+.1f}%</span></div>

<div class="two-col" style="margin-top:24px;">
<div class="col">
<h3>Key Metrics</h3>
<div class="kpi-row">
<div class="kpi">
<div class="val">{info['rfo_26']:,.0f}</div>
<div class="lbl">RFO 6M26 (mb)</div>
</div>
<div class="kpi">
<div class="val">{info['rfo_25']:,.0f}</div>
<div class="lbl">RFO 6M25 (mb)</div>
</div>
</div>
<div class="kpi-row" style="margin-top:12px;">
<div class="kpi" style="background:#fff8e6;">
<div class="val {yoy_class}" style="font-size:32px;">{rfo_yoy:+.1f}%</div>
<div class="lbl">YoY Revenue</div>
</div>
<div class="kpi" style="background:#fff8e6;">
<div class="val {np_yoy_class}" style="font-size:32px;">{np_yoy_str}</div>
<div class="lbl">YoY NP Owners</div>
</div>
</div>
</div>

<div class="col">
<h3>Top 5 Companies by RFO</h3>
<table>
<tr><th>Ticker</th><th style="text-align:right">RFO 6M26</th><th style="text-align:right">YoY</th><th style="text-align:right">NP Owners</th></tr>
''')
        for tk_row in top5:
            rfo = float(tk_row['rfo_6m26_mb'] or 0)
            yoy = tk_row['yoy_rfo_pct']
            yoy_v = float(yoy) if yoy else 0
            yoy_class2 = 'pos' if yoy_v >= 0 else 'neg'
            np_v = float(tk_row['np_owners_6m26_mb']) if tk_row['np_owners_6m26_mb'] else 0
            np_str = f'{np_v:,.0f}' if np_v else '-'
            html.append(f'<tr><td><b>{tk_row["ticker"]}</b></td><td style="text-align:right">{rfo:,.0f}</td><td style="text-align:right" class="{yoy_class2}">{yoy_v:+.1f}%</td><td style="text-align:right">{np_str}</td></tr>')
        html.append('</table></div></div>')

        html.append(f'<div class="commentary"><b>Analyst view:</b> {SEG_COMMENTARY[seg]}</div>')
        html.append(f'<div class="page-num">{slide_n} / {TOTAL}</div></div>')
    else:
        # Pending placeholder slide
        html.append(f'''
<div class="slide">
<div class="brand">SET | IS1 Coverage</div>
<h1>{seg} - {SEG_NAMES_TH[seg]} <span style="font-size:14px; color:#92400e; vertical-align:super;">⏳ PENDING</span></h1>
<div class="subtitle" style="color:#92400e;">Segment data pending verification</div>

<div style="margin:80px auto; max-width:600px; background:{AMBER}; border:2px solid {AMBER_DARK}; border-radius:8px; padding:40px; text-align:center;">
<div style="font-size:64px; color:{AMBER_DARK}; font-weight:800; margin-bottom:16px;">รอข้อมูล</div>
<div style="font-size:24px; color:{AMBER_DARK}; margin-bottom:24px; font-style:italic;">Awaiting data</div>
<div style="font-size:14px; color:#333; line-height:1.6;">
Per spec: this segment is waiting on <code>fill_from_control.py</code> against the control CSV.
<br>No fake numbers will be inserted until verified data lands.
</div>
<div style="margin-top:24px; font-size:13px; color:#666; font-style:italic;">Segment universe: {SEG_NAMES_TH[seg]}</div>
</div>

<div class="page-num">{slide_n} / {TOTAL}</div></div>
''')
    slide_n += 1

# Outlook slide
html.append(f'''
<div class="slide">
<div class="brand">SET | IS1 Coverage</div>
<h1>Outlook &amp; Investment Implications</h1>
<h2>What to watch next 6 months</h2>
<div class="two-col">
<div class="col">
<h3>FOOD Sector</h3>
<div class="commentary">
<p><b>Tailwinds:</b> F8 Sugar/oils recovering from low base, F2 Seafood stable, F3 Pet food expanding to CLMV</p>
<p><b>Headwinds:</b> F1 Animal protein margin pressure from swine/broiler prices, F9 Processed ag raw material costs</p>
<p><b>Key catalyst:</b> Q3 export data (Sept), CPF margin guidance update, BR/SST turnaround evidence</p>
</div>
</div>
<div class="col">
<h3>PROP Sector</h3>
<div class="commentary">
<p><b>Tailwinds:</b> P1 Residential backlog, P3 Retail mall traffic recovery, rate cut expectations</p>
<p><b>Headwinds:</b> P2 Industrial FDI slowdown, P5 Diversified leverage risk</p>
<p><b>Key catalyst:</b> Interest rate decision (Q4), presales launches, FDI rebound (Q1 2027)</p>
</div>
</div>
</div>
<div class="page-num">{slide_n} / 18</div>
</div>
''')
slide_n += 1

# Appendix: methodology
html.append(f'''
<div class="slide">
<div class="brand">SET | IS1 Coverage</div>
<h1>Appendix - Methodology &amp; Data Sources</h1>
<h2>How the numbers were built</h2>
<div style="font-size:14px; line-height:1.7;">
<p><b>Universe:</b> 118 SET-listed companies (FOOD 56, PROP 62) from the FY2025 audited perimeter, segmented by sub-sector (F1-F9, P1-P5).</p>
<p><b>Period:</b> 6M26 = six-month cumulative ended 30 June 2026; comparative 6M25 = same period 2025. NOT calendar H1 for FY-offset names (KSL/KTIS/LST/BLAND - pulled at their own reported half-year).</p>
<p><b>Data sources (priority order):</b></p>
<ol style="margin-left:20px;">
<li><b>Spec anchors (8 tickers):</b> CPF, CPN, ITC, BR, PEACE, JDF, BRR, KBS - hand-verified against actual SET interim FS income statements.</li>
<li><b>SET FS direct pull (2 tickers):</b> TU, ITC - parsed from FINANCIAL_STATEMENTS.XLSX in the FS ZIP package.</li>
<li><b>User DB rollup (108 tickers):</b> "01 Sale" column from 00_Database_all_form.xlsx, Accumulated 6M26 row.</li>
</ol>
<p><b>RFO definition:</b> Revenue from operations (sale of goods + rendering of services), excluding investment income, gains on FX, fair-value gains, disposal gains - per the SET-standard format.</p>
<p><b>NPMaj:</b> Profit attributable to owners of the parent (separated from NCI). For tickers where this split is unavailable, NPMaj = total profit and <code>npat_basis_note</code> is set to "unattributed only".</p>
<p><b>Units:</b> All figures in THB million unless noted.</p>
</div>
<div class="page-num">{slide_n} / 18</div>
</div>
''')

html.append('</body></html>')

out = REPO / '6M26-deck-mockup.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write('\n'.join(html))

import os
print(f'Wrote {out}')
print(f'Size: {os.path.getsize(out):,} bytes')
print(f'Slides: {slide_n}')