"""Generate 6M26 deck (PPTX) — ONLY F1 and F4 show confirmed numbers.

Per the spec, only F1 (Integrated animal protein) and F4 (Branded beverages)
have verified data from the control CSV (00_Database_all_form.xlsx). The other
12 segments (F2, F3, F5-F9, P1-P5) are waiting on fill_from_control.py.

Per spec rule "no fake numbers", we show:
  - F1, F4: full data with YoY%, top-5 tickers, analyst commentary
  - Other 12 segments: explicit "รอข้อมูล" placeholder slides
  - Sector overview: only confirms F1 + F4 totals; other segments show pending
  - Outlook / methodology: full prose (these don't depend on segment numbers)
"""
import csv
from pathlib import Path
from collections import defaultdict
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

REPO = Path('C:/Users/Tasinpong/projects/is1-coverage-dashboard')
csv_path = REPO / '6M26-deck-ready.csv'

# === Brand colors ===
NAVY = RGBColor(0x00, 0x33, 0x66)
GOLD = RGBColor(0xC9, 0xA9, 0x61)
LIGHT_NAVY = RGBColor(0xE8, 0xEE, 0xF7)
LIGHT_BROWN = RGBColor(0xF7, 0xEE, 0xE8)
LIGHT_GREY = RGBColor(0xF5, 0xF5, 0xF5)
AMBER_PENDING = RGBColor(0xFE, 0xF3, 0xC7)  # for "รอข้อมูล" placeholder
AMBER_DARK = RGBColor(0x92, 0x40, 0x0E)
CREAM = RGBColor(0xFF, 0xF8, 0xE6)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREY = RGBColor(0x88, 0x88, 0x88)
DARK_GREY = RGBColor(0x33, 0x33, 0x33)
GREEN = RGBColor(0x16, 0xA3, 0x4A)
RED = RGBColor(0xDC, 0x26, 0x26)
BLACK = RGBColor(0x00, 0x00, 0x00)
BROWN = RGBColor(0x7C, 0x2D, 0x12)

# === Load data ===
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

# === CONFIRMED segments per spec ===
CONFIRMED = {'F1', 'F4'}
# All 14 segments with Thai names
SEG_NAMES_TH = {
    'F1':'F1 โปรตีนจากสัตว์ครบวงจร', 'F2':'F2 อาหารทะเล/เพาะเลี้ยง',
    'F3':'F3 อาหารสัตว์เลี้ยง', 'F4':'F4 เครื่องดื่มแบรนด์',
    'F5':'F5 ร้านอาหาร/โภชนาการ', 'F6':'F6 ขนมอบกรอบ/เบเกอรี่',
    'F7':'F7 วัตถุดิบ/เครื่องปรุง', 'F8':'F8 น้ำตาล/แป้ง/น้ำมัน',
    'F9':'F9 เกษตรแปรรูป',
    'P1':'P1 ที่อยู่อาศัย (ขาย)', 'P2':'P2 นิคมอุตสาหกรรม/โลจิสติกส์',
    'P3':'P3 ค้าปลีก/พา�ิชยกรรม', 'P4':'P4 การโรงแรม/ผสมผสาน',
    'P5':'P5 เบ็ดเตล็ด/ทรานสิชั่น',
}

SEG_COMMENTARY = {
    'F1':'CPF margin pressured by swine/broiler prices + FX drag; BTG/TFG stable, FM/BR flat from low base',
    'F4':'OSP weak (-8.6%), CBG steady, HTC/ICHI growing, MALEE under pressure',
}

# === Setup PPTX (16:9) ===
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def add_text(slide, x, y, w, h, text, size=14, color=BLACK, bold=False,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font='Calibri', italic=False):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.name = font
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return tb


def add_rect(slide, x, y, w, h, fill_color, line_color=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = fill_color
    if line_color is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line_color
    return shp


def add_brand(slide, text='SET | IS1 Coverage'):
    add_text(slide, 11.5, 0.2, 1.7, 0.3, text, size=9, color=GOLD, bold=True)


def add_page_num(slide, n, total):
    add_text(slide, 12.6, 7.1, 0.6, 0.2, f'{n} / {total}', size=8, color=GREY, align=PP_ALIGN.RIGHT)


def add_table(slide, x, y, w, h, headers, rows, col_widths=None):
    n_cols = len(headers)
    n_rows = 1 + len(rows)
    table_shape = slide.shapes.add_table(n_rows, n_cols, Inches(x), Inches(y), Inches(w), Inches(h))
    table = table_shape.table
    if col_widths:
        for i, cw in enumerate(col_widths):
            table.columns[i].width = Inches(cw)
    for i, h_text in enumerate(headers):
        cell = table.cell(0, i)
        cell.text = ''
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT if i==0 else PP_ALIGN.RIGHT
        r = p.add_run()
        r.text = h_text
        r.font.name = 'Calibri'
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = WHITE
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
    for row_i, row_data in enumerate(rows, 1):
        for col_i, val in enumerate(row_data):
            cell = table.cell(row_i, col_i)
            cell.text = ''
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if col_i == 0 else PP_ALIGN.RIGHT
            r = p.add_run()
            r.text = str(val)
            r.font.name = 'Calibri'
            r.font.size = Pt(10)
            r.font.color.rgb = BLACK
            if col_i == 0:
                r.font.bold = True
            if col_i == 2:
                try:
                    s = str(val).replace('+','').replace('%','').replace(',','')
                    v = float(s) if s else 0
                    if v > 0:
                        r.font.color.rgb = GREEN
                    elif v < 0:
                        r.font.color.rgb = RED
                except:
                    pass
            if row_i % 2 == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(0xFA, 0xFA, 0xFA)
    return table


def top5_by_rfo(seg):
    seg_rows = by_seg.get(seg, {}).get('tickers', [])
    return sorted(seg_rows, key=lambda r: float(r['rfo_6m26_mb'] or 0), reverse=True)[:5]


def confirmed_segment_slide(seg, slide_n, total):
    """Build a full data slide for a CONFIRMED segment."""
    info = by_seg[seg]
    rfo_yoy = (info['rfo_26'] - info['rfo_25']) / info['rfo_25'] * 100
    color = NAVY if seg.startswith('F') else BROWN
    yoy_color = GREEN if rfo_yoy >= 0 else RED

    slide = prs.slides.add_slide(BLANK)
    add_text(slide, 0.6, 0.4, 12, 0.6, f'{seg} - {SEG_NAMES_TH[seg]}', size=26, color=NAVY, bold=True)
    add_text(slide, 0.6, 1.0, 12, 0.4,
             f'{info["count"]} companies  |  RFO 6M26: {info["rfo_26"]:,.0f} mb  |  YoY: ',
             size=12, color=GREY)
    add_text(slide, 6.5, 1.0, 2, 0.4, f'{rfo_yoy:+.1f}%', size=14, color=yoy_color, bold=True)
    add_rect(slide, 0.6, 1.45, 4, 0.04, GOLD)

    add_text(slide, 0.6, 1.7, 5.8, 0.3, 'Key Metrics', size=12, color=NAVY, bold=True)
    add_rect(slide, 0.6, 2.0, 2.8, 1.0, RGBColor(0xF8, 0xFA, 0xFC), NAVY)
    add_text(slide, 0.7, 2.1, 2.6, 0.3, 'RFO 6M26 (mb)', size=9, color=GREY)
    add_text(slide, 0.7, 2.4, 2.6, 0.6, f'{info["rfo_26"]:,.0f}', size=20, color=NAVY, bold=True)
    add_rect(slide, 3.6, 2.0, 2.8, 1.0, RGBColor(0xF8, 0xFA, 0xFC), NAVY)
    add_text(slide, 3.7, 2.1, 2.6, 0.3, 'RFO 6M25 (mb)', size=9, color=GREY)
    add_text(slide, 3.7, 2.4, 2.6, 0.6, f'{info["rfo_25"]:,.0f}', size=20, color=NAVY, bold=True)
    add_rect(slide, 0.6, 3.2, 2.8, 1.0, CREAM, GOLD)
    add_text(slide, 0.7, 3.3, 2.6, 0.3, 'YoY Revenue', size=9, color=GREY)
    add_text(slide, 0.7, 3.5, 2.6, 0.6, f'{rfo_yoy:+.1f}%', size=24, color=yoy_color, bold=True)
    n_companies = info['count']
    add_rect(slide, 3.6, 3.2, 2.8, 1.0, CREAM, GOLD)
    add_text(slide, 3.7, 3.3, 2.6, 0.3, '# Companies', size=9, color=GREY)
    add_text(slide, 3.7, 3.5, 2.6, 0.6, f'{n_companies}', size=24, color=NAVY, bold=True)

    add_text(slide, 6.8, 1.7, 6, 0.3, 'Top 5 Companies by RFO', size=12, color=NAVY, bold=True)
    rows = []
    for tr in top5_by_rfo(seg):
        rfo = float(tr['rfo_6m26_mb'] or 0)
        yoy = tr.get('yoy_rfo_pct', '')
        try: yoy_v = float(yoy) if yoy else 0
        except: yoy_v = 0
        np_v = float(tr['np_owners_6m26_mb']) if tr['np_owners_6m26_mb'] else 0
        np_s = f'{np_v:,.0f}' if np_v else '-'
        yoy_s = f'{yoy_v:+.1f}%' if yoy else '-'
        rows.append([tr['ticker'], f'{rfo:,.0f}', yoy_s, np_s])
    add_table(slide, 6.8, 2.0, 6.0, 2.2,
              headers=['Ticker', 'RFO 6M26', 'YoY', 'NP Owners'],
              rows=rows, col_widths=[1.5, 1.5, 1.5, 1.5])

    add_rect(slide, 0.6, 5.4, 12.2, 1.5, CREAM, GOLD)
    add_text(slide, 0.8, 5.5, 1.5, 0.3, 'Analyst view:', size=11, color=GOLD, bold=True)
    add_text(slide, 0.8, 5.8, 11.8, 1.0, SEG_COMMENTARY[seg], size=11, color=DARK_GREY)

    add_brand(slide)
    add_page_num(slide, slide_n, total)


def pending_segment_slide(seg, slide_n, total):
    """Build a placeholder slide for a non-confirmed segment."""
    slide = prs.slides.add_slide(BLANK)
    add_text(slide, 0.6, 0.4, 12, 0.6, f'{seg} - {SEG_NAMES_TH[seg]}', size=26, color=NAVY, bold=True)
    add_text(slide, 0.6, 1.0, 12, 0.4, 'Segment data pending verification', size=14, color=GREY, italic=True)
    add_rect(slide, 0.6, 1.45, 4, 0.04, AMBER_DARK)

    # Big pending card
    add_rect(slide, 1.5, 2.5, 10.3, 2.8, AMBER_PENDING, AMBER_DARK)
    add_text(slide, 1.5, 2.7, 10.3, 0.5, 'รอข้อมูล', size=44, color=AMBER_DARK, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, 1.5, 3.4, 10.3, 0.4, 'Awaiting data', size=18, color=AMBER_DARK, align=PP_ALIGN.CENTER, italic=True)
    add_text(slide, 1.5, 4.1, 10.3, 0.6,
             'Per spec: this segment is waiting on fill_from_control.py against the control CSV.\n'
             'No fake numbers will be inserted until verified data lands.',
             size=11, color=DARK_GREY, align=PP_ALIGN.CENTER)
    add_text(slide, 1.5, 4.8, 10.3, 0.4,
             f'Segment universe: {SEG_NAMES_TH[seg]}',
             size=10, color=GREY, align=PP_ALIGN.CENTER, italic=True)

    add_brand(slide)
    add_page_num(slide, slide_n, total)


# === Compute slide count: 1 cover + 1 overview + 2 confirmed + 12 pending + 1 outlook + 1 methodology = 18 ===
TOTAL_SLIDES = 18
slide_n = 1

# === SLIDE 1: COVER ===
slide = prs.slides.add_slide(BLANK)
add_text(slide, 0.8, 2.5, 11.7, 1.0, 'Thai SET 6M26 Review', size=44, color=NAVY, bold=True)
add_text(slide, 0.8, 3.5, 11.7, 0.6, 'Food & Property Sectors', size=28, color=GOLD, bold=False)
add_text(slide, 0.8, 4.5, 11.7, 0.4, 'Six-month period ended 30 June 2026', size=16, color=GREY)
add_text(slide, 0.8, 5.8, 11.7, 0.3, 'Universe: 118 SET-listed companies (FOOD 56, PROP 62)', size=11, color=DARK_GREY)
add_text(slide, 0.8, 6.1, 11.7, 0.3, 'Data as of: 17 August 2026 (Q2/2026 FS + MD&A filings)', size=11, color=DARK_GREY)
add_text(slide, 0.8, 6.4, 11.7, 0.3, 'CONFIRMED segments: F1, F4. Other 12 segments: pending control CSV.', size=11, color=AMBER_DARK, bold=True)
add_rect(slide, 0.8, 3.3, 4, 0.05, GOLD)
add_brand(slide)
add_page_num(slide, slide_n, TOTAL_SLIDES)
slide_n += 1

# === SLIDE 2: SECTOR OVERVIEW (partial) ===
slide = prs.slides.add_slide(BLANK)
add_text(slide, 0.6, 0.4, 12, 0.6, 'Sector Overview - 6M26 vs 6M25', size=28, color=NAVY, bold=True)
add_text(slide, 0.6, 1.0, 12, 0.4, 'Only F1 and F4 confirmed from control CSV (THB mb)', size=12, color=GREY, italic=True)
add_rect(slide, 0.6, 1.45, 4, 0.04, GOLD)

# Confirmed totals only
f1_total = by_seg['F1']['rfo_26']
f1_25 = by_seg['F1']['rfo_25']
f1_yoy = (f1_total - f1_25) / f1_25 * 100
f4_total = by_seg['F4']['rfo_26']
f4_25 = by_seg['F4']['rfo_25']
f4_yoy = (f4_total - f4_25) / f4_25 * 100

add_rect(slide, 0.6, 1.8, 5.9, 1.6, LIGHT_NAVY, NAVY)
add_text(slide, 0.8, 2.0, 5.5, 0.4, 'F1 (CONFIRMED)', size=12, color=NAVY, bold=True)
add_text(slide, 0.8, 2.4, 5.5, 0.8, f'{f1_total:,.0f}', size=44, color=NAVY, bold=True)
add_text(slide, 0.8, 3.0, 5.5, 0.4, f'{f1_yoy:+.1f}% YoY', size=18, color=GREEN if f1_yoy>=0 else RED, bold=True)

add_rect(slide, 6.8, 1.8, 5.9, 1.6, LIGHT_BROWN, BROWN)
add_text(slide, 7.0, 2.0, 5.5, 0.4, 'F4 (CONFIRMED)', size=12, color=BROWN, bold=True)
add_text(slide, 7.0, 2.4, 5.5, 0.8, f'{f4_total:,.0f}', size=44, color=BROWN, bold=True)
add_text(slide, 7.0, 3.0, 5.5, 0.4, f'{f4_yoy:+.1f}% YoY', size=18, color=GREEN if f4_yoy>=0 else RED, bold=True)

# Segment grid (CONFIRMED in green, pending in amber)
add_text(slide, 0.6, 3.7, 12, 0.3, 'All 14 segments - status', size=12, color=NAVY, bold=True)

all_segs = ['F1','F2','F3','F4','F5','F6','F7','F8','F9','P1','P2','P3','P4','P5']
y = 4.1
# Two rows of 7
for i, seg in enumerate(all_segs[:7]):
    x = 0.6 + i * 1.78
    if seg in CONFIRMED:
        info = by_seg[seg]
        yoy = (info['rfo_26'] - info['rfo_25']) / info['rfo_25'] * 100
        add_rect(slide, x, y, 1.7, 1.5, LIGHT_NAVY, NAVY)
        add_text(slide, x+0.05, y+0.05, 1.6, 0.3, f'{seg} ✓', size=11, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
        add_text(slide, x+0.05, y+0.4, 1.6, 0.5, f'{info["rfo_26"]:,.0f}', size=14, color=NAVY, bold=True, align=PP_ALIGN.CENTER)
        add_text(slide, x+0.05, y+0.9, 1.6, 0.3, f'{yoy:+.1f}% YoY', size=10, color=GREEN if yoy>=0 else RED, bold=True, align=PP_ALIGN.CENTER)
    else:
        add_rect(slide, x, y, 1.7, 1.5, AMBER_PENDING, AMBER_DARK)
        add_text(slide, x+0.05, y+0.05, 1.6, 0.3, seg, size=11, color=AMBER_DARK, bold=True, align=PP_ALIGN.CENTER)
        add_text(slide, x+0.05, y+0.45, 1.6, 0.5, 'รอข้อมูล', size=14, color=AMBER_DARK, bold=True, align=PP_ALIGN.CENTER)
        add_text(slide, x+0.05, y+1.0, 1.6, 0.4, 'pending', size=10, color=AMBER_DARK, align=PP_ALIGN.CENTER, italic=True)

# Row 2 (P1-P5, all pending)
y = 5.75
for i, seg in enumerate(all_segs[7:]):
    x = 0.6 + i * 1.78
    add_rect(slide, x, y, 1.7, 1.0, AMBER_PENDING, AMBER_DARK)
    add_text(slide, x+0.05, y+0.05, 1.6, 0.3, seg, size=11, color=AMBER_DARK, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x+0.05, y+0.4, 1.6, 0.4, 'รอข้อมูล', size=12, color=AMBER_DARK, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, x+0.05, y+0.85, 1.6, 0.3, 'pending', size=9, color=AMBER_DARK, align=PP_ALIGN.CENTER, italic=True)

add_brand(slide)
add_page_num(slide, slide_n, TOTAL_SLIDES)
slide_n += 1

# === SLIDES 3-4: CONFIRMED F1 + F4 ===
for seg in ['F1', 'F4']:
    confirmed_segment_slide(seg, slide_n, TOTAL_SLIDES)
    slide_n += 1

# === SLIDES 5-16: PENDING 12 segments ===
pending_segs = [s for s in all_segs if s not in CONFIRMED]
for seg in pending_segs:
    pending_segment_slide(seg, slide_n, TOTAL_SLIDES)
    slide_n += 1

# === SLIDE 17: OUTLOOK (general, not segment-specific) ===
slide = prs.slides.add_slide(BLANK)
add_text(slide, 0.6, 0.4, 12, 0.6, 'Outlook & Investment Implications', size=28, color=NAVY, bold=True)
add_text(slide, 0.6, 1.0, 12, 0.4, 'General framework (segment-specific views pending data)', size=14, color=GREY, italic=True)
add_rect(slide, 0.6, 1.45, 4, 0.04, GOLD)

# Food outlook (general, no segment numbers)
add_text(slide, 0.6, 1.7, 6, 0.3, 'FOOD Sector - General Themes', size=14, color=NAVY, bold=True)
add_rect(slide, 0.6, 2.0, 6, 4.5, LIGHT_NAVY, NAVY)
add_text(slide, 0.8, 2.2, 5.6, 0.3, 'TAILWINDS TO WATCH', size=10, color=NAVY, bold=True)
add_text(slide, 0.8, 2.5, 5.6, 1.3,
         '- Sugar/oils cycle (F8) recovery from low base\n'
         '- Seafood stable (F2) on tuna/salmon demand\n'
         '- Pet food (F3) expansion to CLMV markets',
         size=10, color=DARK_GREY)
add_text(slide, 0.8, 3.9, 5.6, 0.3, 'HEADWINDS TO WATCH', size=10, color=RED, bold=True)
add_text(slide, 0.8, 4.2, 5.6, 1.3,
         '- F1 Animal protein margin pressure (CPF)\n'
         '- Processed ag (F9) raw material costs\n'
         '- Beverages consumer slowdown (F4)',
         size=10, color=DARK_GREY)
add_text(slide, 0.8, 5.6, 5.6, 0.3, 'CATALYSTS TO TRACK', size=10, color=GOLD, bold=True)
add_text(slide, 0.8, 5.9, 5.6, 0.5,
         'Q3 export data (Sept), CPF margin guidance, BR turnaround',
         size=10, color=DARK_GREY)

# Property outlook (general)
add_text(slide, 6.8, 1.7, 6, 0.3, 'PROP Sector - General Themes', size=14, color=BROWN, bold=True)
add_rect(slide, 6.8, 2.0, 6, 4.5, LIGHT_BROWN, BROWN)
add_text(slide, 7.0, 2.2, 5.6, 0.3, 'TAILWINDS TO WATCH', size=10, color=BROWN, bold=True)
add_text(slide, 7.0, 2.5, 5.6, 1.3,
         '- Residential backlog (P1)\n'
         '- Retail mall traffic (P3)\n'
         '- Rate cut expectations in H2/2026',
         size=10, color=DARK_GREY)
add_text(slide, 7.0, 3.9, 5.6, 0.3, 'HEADWINDS TO WATCH', size=10, color=RED, bold=True)
add_text(slide, 7.0, 4.2, 5.6, 1.3,
         '- Industrial FDI slowdown (P2)\n'
         '- Diversified leverage risk (P5)\n'
         '- Interest rate uncertainty',
         size=10, color=DARK_GREY)
add_text(slide, 7.0, 5.6, 5.6, 0.3, 'CATALYSTS TO TRACK', size=10, color=GOLD, bold=True)
add_text(slide, 7.0, 5.9, 5.6, 0.5,
         'Interest rate decision (Q4), presales launches, FDI rebound',
         size=10, color=DARK_GREY)

add_brand(slide)
add_page_num(slide, slide_n, TOTAL_SLIDES)
slide_n += 1

# === SLIDE 18: METHODOLOGY ===
slide = prs.slides.add_slide(BLANK)
add_text(slide, 0.6, 0.4, 12, 0.6, 'Appendix - Methodology & Data Status', size=26, color=NAVY, bold=True)
add_text(slide, 0.6, 1.0, 12, 0.4, 'How the confirmed numbers were built', size=14, color=GREY)
add_rect(slide, 0.6, 1.45, 4, 0.04, GOLD)

add_text(slide, 0.6, 1.7, 12, 0.4, 'Universe', size=12, color=NAVY, bold=True)
add_text(slide, 0.6, 2.0, 12, 0.5,
         '118 SET-listed companies (FOOD 56, PROP 62) from the FY2025 audited perimeter, segmented by sub-sector (F1-F9, P1-P5).',
         size=10, color=DARK_GREY)

add_text(slide, 0.6, 2.7, 12, 0.4, 'Period', size=12, color=NAVY, bold=True)
add_text(slide, 0.6, 3.0, 12, 0.5,
         '6M26 = six-month cumulative ended 30 June 2026; comparative 6M25 = same period 2025.',
         size=10, color=DARK_GREY)

add_text(slide, 0.6, 3.7, 12, 0.4, 'Data status by segment', size=12, color=AMBER_DARK, bold=True)

y = 4.1
# F1 / F4 confirmed row
add_rect(slide, 0.6, y, 12.2, 0.65, LIGHT_NAVY, NAVY)
add_text(slide, 0.7, y+0.05, 1.5, 0.3, 'CONFIRMED (2)', size=10, color=NAVY, bold=True)
add_text(slide, 0.7, y+0.32, 11.4, 0.3, 'F1 โปรตีนจากสัตว์ (CPF/TFG/BTG/FM/BR/SORKON), F4 เครื่องดื่มแบรนด์ (OSP/CBG/ICHI/SAPPE/COCOCO/HTC/TIPCO/MALEE/PLUS) - verified from control CSV', size=10, color=DARK_GREY)
y += 0.72
# Pending row
add_rect(slide, 0.6, y, 12.2, 1.5, AMBER_PENDING, AMBER_DARK)
add_text(slide, 0.7, y+0.05, 1.5, 0.3, 'PENDING (12)', size=10, color=AMBER_DARK, bold=True)
add_text(slide, 0.7, y+0.32, 11.4, 0.3, 'Waiting on fill_from_control.py against 00_Database_all_form.xlsx control CSV.', size=10, color=DARK_GREY)
add_text(slide, 0.7, y+0.6, 11.4, 0.4, 'Per spec rule: "Do NOT estimate, interpolate, or carry forward a prior-period figure to fill a gap — leave it blank."', size=10, color=AMBER_DARK, italic=True)
add_text(slide, 0.7, y+1.0, 11.4, 0.4, 'Affected: F2, F3, F5, F6, F7, F8, F9 (FOOD) and P1, P2, P3, P4, P5 (PROP).', size=10, color=DARK_GREY)
y += 1.6

add_text(slide, 0.6, 6.0, 12, 0.4, 'Definitions', size=12, color=NAVY, bold=True)
add_text(slide, 0.6, 6.3, 12, 0.4,
         'RFO = Revenue from operations (sale of goods + rendering of services).  NP Owners = Profit attributable to owners of the parent.  Units: THB million.',
         size=10, color=DARK_GREY)
add_text(slide, 0.6, 6.6, 12, 0.4,
         'FY-offset names (KSL/KTIS/LST/BLAND): pull at their own reported half-year, NOT calendar H1.',
         size=10, color=DARK_GREY)

add_brand(slide)
add_page_num(slide, slide_n, TOTAL_SLIDES)


# Save
out = REPO / '6M26-deck.pptx'
prs.save(str(out))
import os
print(f'Wrote {out}')
print(f'Size: {os.path.getsize(out):,} bytes')
print(f'Slides: {len(prs.slides)}')
print(f'Confirmed: F1, F4 (2 segments)')
print(f'Pending: {len(pending_segs)} segments (F2, F3, F5-F9, P1-P5)')