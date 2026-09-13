#!/usr/bin/env python3
"""Render sector-intelligence.html into a static Markdown briefing.

The page is fully data-driven from ``data/sector-intelligence.json``; this
exporter mirrors the rendering logic in ``sector-intelligence.js`` (same
formatters, same section order, same claim/evidence registers) so the Markdown
stays a faithful text copy of what the browser shows.

    python3 scripts/export_sector_intelligence_md.py            # EN + TH, full
    python3 scripts/export_sector_intelligence_md.py --lang th  # TH only
    python3 scripts/export_sector_intelligence_md.py --brief    # no per-company read-through
"""

import argparse
import json
import os
import re
import unicodedata
from decimal import Decimal, ROUND_HALF_UP

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "sector-intelligence.json")
TICKERS = os.path.join(ROOT, "data", "ticker-summary.json")

COPY = {
    "en": {
        "pageTitle": "Sector Intelligence", "pageSubtitle": "Interactive sector briefing for RM meetings",
        "structureLens": "Market structure", "earningsLens": "FY2025 earnings", "marketLens": "Market view",
        "marketCap": "Market cap", "companies": "Companies", "largestSegment": "Largest segment",
        "deliveredSegments": "Delivered segments", "ytdPrice": "YTD adjusted", "aggregatePe": "Aggregate P/E",
        "priceLeading": "Price-leading segments", "matrixTitle": "Ranked segment map",
        "matrixSubtitle": "Market-cap order", "rank": "Rank", "segment": "Segment",
        "ytd": "YTD price", "leader": "Leader", "signal": "Signal", "delivered": "Earnings confirmed",
        "expectation": "Price leads", "pressure": "Under pressure", "event": "Event-driven",
        "whyChanged": "Why it changed", "causalChain": "Causal proof chain", "roles": "Segment roles",
        "trigger": "Trigger", "risk": "Risk", "ticker": "Ticker", "role": "Role", "margin": "Margin",
        "methodology": "Methodology & boundaries", "evidenceRegister": "Evidence register",
        "observed": "Observed fact", "marketPaying": "Market is paying for — inference",
        "deliveredLabel": "Delivered earnings / observed", "pressureLabel": "Current pressure / observed",
        "eventLabel": "Event-driven / limited comparability", "companyPanel": "Company drill-down",
        "companyPanelSub": "Every company in the audited segment perimeter",
        "noRole": "Constituent", "source": "Source",
        "loss": "Loss", "lossNarrowed": "Loss narrowed", "lossWidened": "Loss widened",
        "turnedProfit": "Turned profitable", "notMeaningful": "n.m.",
        "marketCutoff": "Market data as of {date} • {period}", "sourceLineage": "Sources: {sources}",
        "definitions": "RFO = Revenue from Operations • NPAT = net profit to owners • Price = adjusted, excludes cash dividends",
        "fact": "Fact", "fact_calculated": "Calculated fact", "management": "Management",
        "management_explanation": "Management explanation", "forward": "Forward view",
        "credit_analysis": "Credit analysis", "analyst_inference": "Analyst inference",
        "analyst_test": "Analyst test", "claimsRegister": "Claim register", "known": "known",
        "alternativeFiscal": "Alternative issuer-FY view", "sourceId": "Source ID", "sourceRole": "Role",
        "sourcePath": "Path", "sourceHash": "SHA-256",
        "mixChart": "Market-cap mix", "mixChartSub": "Segment share and market leader",
        "earningsChart": "RFO and owner NPAT direction", "earningsChartSub": "FY2025 YoY",
        "marketMap": "Price versus earnings map", "marketMapSub": "NPAT YoY versus YTD price",
        "peChart": "Aggregate positive-earner P/E", "peChartSub": "Coverage shown beside every multiple",
        "rfoWhy": "RFO — why", "npatWhy": "NPAT — why",
        "selectedCompany": "Company", "coverage": "Coverage", "share": "Share",
        "quadrant": "Quadrant", "amount": "Amount", "period": "Period", "value": "Value",
        "contents": "Contents", "sectorBrief": "Segment briefs", "visualStory": "Visual story",
        "methodStrip": "Method & boundaries", "scope": "Scope", "qa": "QA",
        "builtAt": "Built at", "sourceFiles": "Source files", "claimEvidence": "Claim evidence",
        "special": "Special / below-line", "bridge": "Reported-to-operating bridge",
        "evidenceTrail": "Evidence trail", "mdaExcerpt": "Primary MD&A excerpt",
        "coreBusiness": "Core business · SET Factsheet via IS1 Coverage",
        "mustProve": "6M26 must prove", "status": "Status", "price": "Price",
    },
    "th": {
        "pageTitle": "บทวิเคราะห์รายกลุ่ม", "pageSubtitle": "Interactive briefing สำหรับนำเสนอในที่ประชุม RM",
        "structureLens": "โครงสร้างตลาด", "earningsLens": "ผลประกอบการ FY2025", "marketLens": "มุมมองตลาด",
        "marketCap": "Market cap", "companies": "บริษัท", "largestSegment": "Segment ใหญ่สุด",
        "deliveredSegments": "Segment ที่กำไรยืนยัน", "ytdPrice": "ราคา YTD ปรับแล้ว", "aggregatePe": "P/E รวม",
        "priceLeading": "Segment ราคานำ", "matrixTitle": "แผนที่ Segment เรียงตาม Market Cap",
        "matrixSubtitle": "เรียงจากใหญ่ไปเล็ก", "rank": "อันดับ", "segment": "Segment",
        "ytd": "ราคา YTD", "leader": "ผู้นำ", "signal": "สัญญาณ", "delivered": "กำไรยืนยันราคา",
        "expectation": "ราคานำพื้นฐาน", "pressure": "ยังถูกกดดัน", "event": "Event-driven",
        "whyChanged": "เหตุผลที่เปลี่ยน", "causalChain": "ห่วงโซ่เหตุและผล", "roles": "บทบาทในกลุ่ม",
        "trigger": "Trigger", "risk": "Risk", "ticker": "Ticker", "role": "บทบาท", "margin": "Margin",
        "methodology": "วิธีคำนวณและขอบเขต", "evidenceRegister": "ทะเบียนหลักฐาน",
        "observed": "ข้อเท็จจริงที่สังเกตได้", "marketPaying": "ตลาดกำลังจ่ายเพื่อ — ข้ออนุมาน",
        "deliveredLabel": "กำไรที่เกิดขึ้นแล้ว / ข้อเท็จจริง", "pressureLabel": "แรงกดดันปัจจุบัน / ข้อเท็จจริง",
        "eventLabel": "Event-driven / เปรียบเทียบจำกัด", "companyPanel": "วิเคราะห์รายบริษัท",
        "companyPanelSub": "ทุกบริษัทใน perimeter ของ Segment ที่สอบทาน",
        "noRole": "บริษัทในกลุ่ม", "source": "แหล่งข้อมูล",
        "loss": "ขาดทุน", "lossNarrowed": "ขาดทุนลดลง", "lossWidened": "ขาดทุนเพิ่มขึ้น",
        "turnedProfit": "กลับเป็นกำไร", "notMeaningful": "n.m.",
        "marketCutoff": "ข้อมูลตลาด ณ {date} • {period}", "sourceLineage": "แหล่งข้อมูล: {sources}",
        "definitions": "RFO = Revenue from Operations • NPAT = กำไรส่วนผู้ถือหุ้น • ราคา = adjusted ไม่รวมเงินปันผล",
        "fact": "ข้อเท็จจริง", "fact_calculated": "ข้อเท็จจริงจากการคำนวณ", "management": "ฝ่ายจัดการ",
        "management_explanation": "คำอธิบายฝ่ายจัดการ", "forward": "มุมมองล่วงหน้า",
        "credit_analysis": "บทวิเคราะห์เครดิต", "analyst_inference": "ข้ออนุมานนักวิเคราะห์",
        "analyst_test": "ประเด็นที่ต้องพิสูจน์", "claimsRegister": "ทะเบียนข้อสรุป", "known": "มีข้อมูล",
        "alternativeFiscal": "มุมมองตามปีบัญชีของผู้ออก", "sourceId": "รหัสแหล่งข้อมูล", "sourceRole": "บทบาท",
        "sourcePath": "พาธ", "sourceHash": "SHA-256",
        "mixChart": "สัดส่วน Market Cap", "mixChartSub": "ขนาด Segment และผู้นำตลาด",
        "earningsChart": "ทิศทาง RFO และ NPAT ส่วนผู้ถือหุ้น", "earningsChartSub": "FY2025 YoY",
        "marketMap": "ราคาเทียบกับทิศทางกำไร", "marketMapSub": "NPAT YoY เทียบกับราคา YTD",
        "peChart": "P/E รวมของบริษัทที่มีกำไร", "peChartSub": "แสดงความครอบคลุมของข้อมูลควบคู่ทุกค่า",
        "rfoWhy": "RFO — เพราะอะไร", "npatWhy": "NPAT — เพราะอะไร",
        "selectedCompany": "บริษัท", "coverage": "ครอบคลุม", "share": "สัดส่วน",
        "quadrant": "ควอดรันต์", "amount": "จำนวน", "period": "ช่วง", "value": "ค่า",
        "contents": "สารบัญ", "sectorBrief": "บทวิเคราะห์รายกลุ่มย่อย", "visualStory": "ภาพรวมเชิงกราฟ",
        "methodStrip": "วิธีคำนวณและขอบเขต", "scope": "ขอบเขต", "qa": "QA",
        "builtAt": "สร้างเมื่อ", "sourceFiles": "ไฟล์ต้นทาง", "claimEvidence": "หลักฐานรายข้อ",
        "special": "รายการพิเศษ / ต่ำกว่าการดำเนินงาน", "bridge": "เชื่อมกำไรรายงานกับผลดำเนินงาน",
        "evidenceTrail": "เส้นทางหลักฐาน", "mdaExcerpt": "ข้อความ MD&A ต้นทาง",
        "coreBusiness": "ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage",
        "mustProve": "6M26 ต้องพิสูจน์", "status": "สถานะ", "price": "ราคา",
    },
}

TH_MONTHS = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
             "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
EN_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


class Ctx:
    """Language-bound rendering helpers (mirrors the page's i18n layer)."""

    def __init__(self, lang, meta, ticker_meta, brief=False):
        self.lang = lang
        self.meta = meta
        self.ticker_meta = ticker_meta
        self.brief = brief

    # -- i18n ------------------------------------------------------------
    def t(self, key):
        return COPY[self.lang].get(key) or COPY["en"].get(key) or key

    def loc(self, value):
        if value is None:
            return ""
        if isinstance(value, str):
            return value
        return value.get(self.lang) or value.get("en") or value.get("th") or ""

    def copy(self, en, th):
        return th if self.lang == "th" else en


def to_fixed(value, digits):
    """JavaScript Number.prototype.toFixed semantics."""
    quant = Decimal(1).scaleb(-digits)
    return str(Decimal(float(value)).quantize(quant, rounding=ROUND_HALF_UP))


def finite(value):
    if value is None or value == "":
        return False
    try:
        number = float(value)
    except (TypeError, ValueError):
        return False
    return number == number and number not in (float("inf"), float("-inf"))


def fmt_pct(value, digits=1):
    if not finite(value):
        return "—"
    number = float(value)
    return ("+" if number > .049 else "") + to_fixed(number, digits) + "%"


def fmt_pe(ctx, value):
    return to_fixed(value, 1) + "x" if finite(value) else ctx.t("notMeaningful")


def fmt_mcap(value):
    if not finite(value):
        return "—"
    number = float(value)
    if number >= 1000:
        return "THB " + to_fixed(number / 1000, 0 if number >= 100000 else 1) + "bn"
    return "THB " + to_fixed(number, 0) + "m"


def fmt_amount(value):
    if not finite(value):
        return "—"
    number = float(value)
    sign = "−" if number < 0 else ""
    absolute = abs(number)
    if absolute >= 1000000:
        return sign + "THB " + to_fixed(absolute / 1000000, 2) + "tn"
    if absolute >= 1000:
        return sign + "THB " + to_fixed(absolute / 1000, 0 if absolute >= 100000 else 1) + "bn"
    return sign + "THB " + to_fixed(absolute, 0) + "m"


def fmt_amount_delta(value):
    if not finite(value):
        return "—"
    return ("+" if float(value) > 0 else "") + fmt_amount(value).replace("THB ", "")


def fmt_npat(ctx, metrics):
    state = metrics.get("npatState")
    pct = metrics.get("npatYoYPct")
    if state == "turned_to_loss":
        return ctx.t("loss")
    if state == "loss_narrowed":
        return ctx.t("lossNarrowed") + (" " + fmt_pct(pct) if finite(pct) else "")
    if state == "loss_widened":
        return ctx.t("lossWidened") + (" " + fmt_pct(pct) if finite(pct) else "")
    if state == "turned_to_profit" and not finite(pct):
        return ctx.t("turnedProfit")
    return fmt_pct(pct)


def coverage_text(coverage, include_mcap=False):
    if not coverage:
        return "—"
    text = "%s/%s" % (coverage.get("count"), coverage.get("total"))
    if include_mcap and finite(coverage.get("marketCapPct")):
        text += " • " + to_fixed(coverage["marketCapPct"], 0) + "% M-cap"
    return text


def status_label(ctx, status):
    return ctx.t("event" if status == "event" else status)


def valuation_label(ctx, status):
    if status == "delivered":
        return ctx.t("deliveredLabel")
    if status == "pressure":
        return ctx.t("pressureLabel")
    if status == "event":
        return ctx.t("eventLabel")
    return ctx.t("marketPaying")


def display_date(ctx, iso):
    if not iso:
        return "—"
    year, month, day = (int(part) for part in iso.split("-"))
    if ctx.lang == "th":
        return "%d %s %d" % (day, TH_MONTHS[month - 1], year + 543)
    return "%d %s %d" % (day, EN_MONTHS[month - 1], year)


def cell(text):
    """Make a value safe inside a Markdown table cell."""
    return re.sub(r"\s+", " ", str(text or "")).replace("|", "\\|").strip()


def table(headers, rows):
    lines = ["| " + " | ".join(cell(h) for h in headers) + " |",
             "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(cell(value) for value in row) + " |")
    return lines


def anchor(text):
    """GitHub heading slug: lowercase, drop punctuation, spaces to hyphens.

    Letters, digits and combining marks are kept — Thai vowel and tone signs are
    marks, and dropping them would break every Thai anchor.
    """
    kept = "".join(char for char in str(text).lower()
                   if unicodedata.category(char)[0] in "LMN" or char in "-_ ")
    return kept.strip().replace(" ", "-")


# -- narrative fallbacks (used when a company carries no MD&A driver block) --

def rfo_narrative(ctx, company):
    if not company.get("rfoPanel"):
        reason = company.get("panelExclusionReason")
        return ctx.copy(
            "Not in the comparable RFO panel" + (": " + reason if reason else ".") +
            " No operating-revenue direction is asserted.",
            "ไม่อยู่ในชุดข้อมูล RFO ที่เปรียบเทียบได้" + (": " + reason if reason else "") +
            " จึงไม่สรุปทิศทางรายได้จากการดำเนินงาน")
    value = float(company.get("rfoYoYPct") or 0)
    if value > 1:
        return ctx.copy(
            "RFO increased %s%%. The audited panel confirms operating-revenue expansion." % to_fixed(abs(value), 1),
            "RFO เพิ่ม %s%% ตัวเลขที่สอบทานยืนยันการขยายตัวของรายได้ดำเนินงาน" % to_fixed(abs(value), 1))
    if value < -1:
        return ctx.copy(
            "RFO decreased %s%%. The audited panel confirms weaker operating scale." % to_fixed(abs(value), 1),
            "RFO ลด %s%% ตัวเลขที่สอบทานยืนยันฐานรายได้ดำเนินงานที่อ่อนลง" % to_fixed(abs(value), 1))
    return ctx.copy("RFO was broadly flat at %s." % fmt_pct(value),
                    "RFO ทรงตัวที่ %s" % fmt_pct(value))


def npat_narrative(ctx, company):
    if not company.get("npatPanel"):
        return ctx.copy("Not in the comparable owner-NPAT panel.",
                        "ไม่อยู่ในชุดข้อมูล NPAT ส่วนผู้ถือหุ้นที่เปรียบเทียบได้")
    state = company.get("npatState")
    if state == "turned_to_loss":
        return ctx.copy("Owner NPAT turned to a loss.", "NPAT ส่วนผู้ถือหุ้นพลิกเป็นขาดทุน")
    if state == "loss_narrowed":
        return ctx.copy("The owner loss narrowed.", "ขาดทุนส่วนผู้ถือหุ้นลดลง")
    if state == "loss_widened":
        return ctx.copy("The owner loss widened.", "ขาดทุนส่วนผู้ถือหุ้นเพิ่มขึ้น")
    if state == "turned_to_profit" and not finite(company.get("npatYoYPct")):
        return ctx.copy("Owner NPAT turned profitable.", "NPAT ส่วนผู้ถือหุ้นพลิกกลับเป็นกำไร")
    if not finite(company.get("npatYoYPct")):
        return ctx.copy("Owner-NPAT growth is not meaningful on the available base.",
                        "อัตราเติบโต NPAT ส่วนผู้ถือหุ้นไม่มีความหมายบนฐานที่มี")
    return ctx.copy("Owner NPAT changed %s." % fmt_pct(company["npatYoYPct"]),
                    "NPAT ส่วนผู้ถือหุ้นเปลี่ยน %s" % fmt_pct(company["npatYoYPct"]))


def company_bridge(ctx, company):
    if not company.get("rfoPanel") or not company.get("npatPanel"):
        return ctx.copy("Panel-limited: avoid a causal bridge",
                        "ข้อมูลเทียบเคียงจำกัด: ไม่ควรสรุปเหตุเชื่อมโยงระหว่างรายได้กับกำไร")
    if company.get("npatState") in ("turned_to_loss", "loss_widened"):
        return ctx.copy("Profit pressure exceeded the revenue signal", "แรงกดดันกำไรมากกว่าสัญญาณรายได้")
    if company.get("npatState") in ("loss_narrowed", "turned_to_profit"):
        return ctx.copy("Turnaround state; growth rate is secondary",
                        "อยู่ในภาวะฟื้นตัว; อัตราเติบโตมีความสำคัญรองลงมา")
    if not finite(company.get("npatYoYPct")) or not finite(company.get("rfoYoYPct")):
        return ctx.copy("Revenue and profit moved together", "รายได้และกำไรเคลื่อนไหวสอดคล้องกัน")
    gap = float(company["npatYoYPct"]) - float(company["rfoYoYPct"])
    if gap > 5:
        return ctx.copy("Profit outpaced operating revenue", "กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน")
    if gap < -5:
        return ctx.copy("Profit conversion lagged revenue", "กำไรแปลงจากรายได้ได้อ่อนลง")
    return ctx.copy("Revenue and profit moved together", "รายได้และกำไรเคลื่อนไหวสอดคล้องกัน")


def driver_basis(ctx, driver):
    basis = (driver or {}).get("basis")
    if basis == "mda_direct_extraction":
        return ctx.copy("Direct MD&A extraction", "ดึงคำอธิบายตรงจาก MD&A")
    if basis == "mda_backed_synthesis":
        return ctx.copy("MD&A-backed synthesis", "สังเคราะห์โดยมี MD&A รองรับ")
    if basis == "mixed_mda_and_secondary":
        return ctx.copy("MD&A + secondary cross-check", "MD&A ร่วมกับแหล่งข้อมูลรอง")
    return ctx.copy("Secondary synthesis · primary MD&A gap",
                    "สังเคราะห์จากแหล่งข้อมูลรอง · ยังไม่มี MD&A ฉบับหลัก")


def source_status(ctx, driver):
    status = (driver or {}).get("sourceStatus")
    if status == "primary_verified":
        return (ctx.copy("Primary MD&A verified", "ตรวจ MD&A ฉบับหลักแล้ว"),
                ctx.copy("RFO and NPAT each have a FY2025 MD&A supporting excerpt. Curated wording remains "
                         "analyst synthesis; the excerpt and hash make the evidence testable.",
                         "ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของ"
                         "นักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้"))
    if status == "reextract_required":
        return (ctx.copy("MD&A re-extraction required", "ต้องดึง MD&A ใหม่"),
                ctx.copy("A filing file exists, but its markdown contains no usable revenue/profit explanation. "
                         "Do not treat the secondary explanation as management attribution.",
                         "พบไฟล์ MD&A แต่ markdown ไม่มีคำอธิบายรายได้/กำไรที่ใช้ได้ จึงห้ามกล่าวว่าสรุปจากแหล่งข้อมูลรอง"
                         "เป็นคำอธิบายของฝ่ายจัดการ"))
    return (ctx.copy("Primary FY2025 MD&A missing", "ไม่มี MD&A FY2025 ฉบับหลัก"),
            ctx.copy("The figures remain audited, but the causal explanation is a labelled secondary synthesis "
                     "until the annual MD&A is obtained.",
                     "ตัวเลขยังเป็นตัวเลขสอบทาน แต่คำอธิบายสาเหตุเป็นข้อมูลรองที่ติดป้ายชัดเจนจนกว่าจะได้ MD&A ประจำปี"))


def materiality_label(ctx, level):
    if level == "high":
        return ctx.copy("Material mover", "เปลี่ยนแปลงมีนัยสำคัญ")
    if level == "medium":
        return ctx.copy("Monitor", "ติดตาม")
    return ctx.copy("Standard review", "ทบทวนปกติ")


def concise_business(value):
    text = re.sub(r"\s+", " ", str(value or "")).replace("?s ", "'s ").strip()
    if len(text) <= 420:
        return text
    clipped = text[:417]
    stop = max(clipped.rfind(". "), clipped.rfind("; "), clipped.rfind(", "))
    if stop > 250:
        clipped = clipped[:stop + 1]
    return clipped.rstrip(" ,;") + "…"


def business_profile(ctx, company):
    meta = ctx.ticker_meta.get(company["ticker"], {})
    embedded = concise_business(ctx.loc(company.get("businessDescription")))
    factsheet = concise_business(meta.get("businessTypeTh") if ctx.lang == "th" else meta.get("businessType"))
    description = factsheet if len(factsheet) >= 20 else embedded
    if ctx.lang == "th" and not re.search(r"[฀-๿]", description or ""):
        description = embedded or description
    if not description:
        description = ctx.copy("Business description is not yet available in IS1 Coverage.",
                               "ยังไม่มีคำอธิบายลักษณะธุรกิจใน IS1 Coverage")
    name = (meta.get("nameTh") or meta.get("name") or company["ticker"]) if ctx.lang == "th" \
        else (meta.get("name") or company["ticker"])
    return name, description


def driver_presentation(ctx, segment, item, index):
    key = ((item or {}).get("en", "") + " " + (item or {}).get("th", "")).lower()
    metrics = segment["metrics"]
    presentation = {"label": ctx.loc(item), "value": "", "detail": ""}
    if segment["code"] == "F1" and index == 0:
        presentation = {"label": ctx.copy("Livestock price", "ราคาสัตว์"), "value": "↑",
                        "detail": ctx.copy("recovery driver", "แรงหนุนการฟื้นตัว")}
    if segment["code"] == "F1" and index == 1:
        presentation = {"label": ctx.copy("Feed cost / soybean", "ต้นทุนอาหารสัตว์ / ถั่วเหลือง"), "value": "↓",
                        "detail": ctx.copy("cost tailwind", "ต้นทุนเอื้อต่อกำไร")}
    if re.search(r"margin|อัตรากำไร", key):
        current, prior = metrics.get("netMarginPct"), metrics.get("netMarginFy2024Pct")
        delta = float(current) - float(prior) if finite(current) and finite(prior) else None
        presentation["value"] = to_fixed(current, 1) + "%" if finite(current) else "—"
        presentation["detail"] = (("+" if delta > 0 else "") + to_fixed(delta, 1) + " ppt YoY") \
            if delta is not None else "FY2025"
    if re.search(r"npat|profit|earnings|ebitda|กำไร", key):
        presentation["value"] = fmt_npat(ctx, metrics)
        presentation["detail"] = fmt_amount(metrics.get("npatOwnersFy2025Mb")) + " FY2025"
    if re.search(r"valuation|premium|re-rating|p/e|มูลค่า|พรีเมียม", key):
        presentation["value"] = fmt_pe(ctx, metrics.get("aggregatePositiveEarningsPe"))
        presentation["detail"] = "YTD " + fmt_pct(metrics.get("ytdAdjustedReturnPct"))
    return presentation


def role_metric(ctx, segment, role):
    company = next((item for item in segment["companies"] if item["ticker"] == role["ticker"]), None)
    if not company:
        return "—", ctx.copy("No audited company row", "ไม่มีข้อมูลบริษัทในชุด audit")
    label = role.get("label") or {}
    key = (label.get("en", "") + " " + label.get("th", "")).lower()
    if re.search(r"leader|ผู้นำ", key):
        share = company.get("marketCapSharePct")
        return (to_fixed(share, 0) + "%" if finite(share) else "—",
                ctx.copy("segment M-cap share", "สัดส่วน Market Cap ในกลุ่ม"))
    if re.search(r"rfo|revenue|รายได้", key):
        return (fmt_pct(company["rfoYoYPct"]) if company.get("rfoPanel") else "—",
                "RFO YoY · Δ " + fmt_amount_delta(company.get("rfoChangeMb")))
    if re.search(r"profit|earnings|npat|loss|กำไร|ขาดทุน", key):
        return (fmt_npat(ctx, company) if company.get("npatPanel") else "—",
                "NPAT YoY · Δ " + fmt_amount_delta(company.get("npatChangeMb")))
    if re.search(r"price|rising|ดาวรุ่ง|ราคา", key):
        return fmt_pct(company.get("ytdAdjustedReturnPct")), ctx.copy("YTD adjusted price", "ราคา YTD ปรับแล้ว")
    return fmt_pe(ctx, company.get("pe")), "P/E · YTD " + fmt_pct(company.get("ytdAdjustedReturnPct"))


def quadrant(ctx, npat, ytd):
    if not finite(npat) or not finite(ytd):
        return "—"
    labels = ["Price leads • profit unconfirmed", "Price and profit aligned",
              "Price and profit pressured", "Profit leads • price lags"] if ctx.lang == "en" else \
             ["ราคานำ • กำไรยังไม่ยืนยัน", "ราคาและกำไรตอบรับ", "ราคาและกำไรถูกกดดัน", "กำไรนำ • ราคายัง lag"]
    x, y = float(npat), float(ytd)
    if x >= 0 and y >= 0:
        return labels[1]
    if x < 0 <= y:
        return labels[0]
    if x < 0 and y < 0:
        return labels[2]
    return labels[3]


# -- section renderers ----------------------------------------------------

def render_overview(ctx, sector, out):
    metrics, coverage = sector["metrics"], sector["coverage"]
    largest = sector["segments"][0]
    delivered = sum(1 for s in sector["segments"] if s["status"] == "delivered")
    leading = sum(1 for s in sector["segments"] if s["status"] in ("expectation", "event"))
    total = len(sector["segments"])

    out.append("## %s — %s" % (sector["code"], ctx.loc(sector["title"])))
    out.append("")
    out.append(ctx.loc(sector["thesis"]))
    out.append("")
    for index, item in enumerate(sector["takeaways"], start=1):
        out.append("%d. %s" % (index, ctx.loc(item)))
    out.append("")
    out.append("### %s" % ctx.copy("Three-lens decision framework", "กรอบการตัดสินใจ 3 มุมมอง"))
    out.append("")
    out += table([ctx.copy("Lens", "มุมมอง"), ctx.copy("Metric", "ตัวชี้วัด"), ctx.t("value"), ctx.t("coverage")],
                 [
                     ["01 " + ctx.t("structureLens"), ctx.t("marketCap"), fmt_mcap(metrics["marketCapMb"]),
                      "%s %s" % (coverage["marketCap"], ctx.t("known"))],
                     ["", ctx.t("companies"), str(metrics["companyCount"]), ""],
                     ["", ctx.t("largestSegment"),
                      "%s · %s%%" % (largest["code"], to_fixed(largest["marketCapSharePct"], 1)), ""],
                     ["02 " + ctx.t("earningsLens"), "RFO YoY", fmt_pct(metrics["rfoYoYPct"]), coverage["rfo"]],
                     ["", "NPAT YoY", fmt_pct(metrics["npatYoYPct"]), coverage["npat"]],
                     ["", ctx.t("deliveredSegments"), "%d/%d" % (delivered, total), ""],
                     ["03 " + ctx.t("marketLens"), ctx.t("ytdPrice"),
                      fmt_pct(metrics["ytdAdjustedReturnPct"]), coverage["ytd"]],
                     ["", ctx.t("aggregatePe"), fmt_pe(ctx, metrics["aggregatePositiveEarningsPe"]),
                      coverage["positivePe"]],
                     ["", ctx.t("priceLeading"), "%d/%d" % (leading, total), ""],
                 ])
    out.append("")
    out.append("FY2025 RFO %s (FY2024 %s) • FY2025 owner NPAT %s (FY2024 %s) • %s %s%% (FY2024 %s%%)" % (
        fmt_amount(metrics["rfoFy2025Mb"]), fmt_amount(metrics["rfoFy2024Mb"]),
        fmt_amount(metrics["npatOwnersFy2025Mb"]), fmt_amount(metrics["npatOwnersFy2024Mb"]),
        ctx.t("margin"), to_fixed(metrics["netMarginPct"], 1), to_fixed(metrics["netMarginFy2024Pct"], 1)))
    out.append("")


def render_visual_story(ctx, sector, out):
    out.append("### %s" % ctx.t("visualStory"))
    out.append("")

    out.append("#### 01 · %s — %s" % (ctx.t("structureLens").upper(), ctx.t("mixChart")))
    out.append("")
    out.append("_%s_" % ctx.t("mixChartSub"))
    out.append("")
    out += table([ctx.t("segment"), ctx.t("share"), ctx.t("marketCap"), ctx.t("leader")],
                 [[seg["code"] + " " + ctx.loc(seg["name"]),
                   to_fixed(seg["marketCapSharePct"], 1) + "%",
                   fmt_mcap(seg["marketCapMb"]),
                   "%s%s" % (seg["leader"].get("ticker") or "—",
                             " · " + to_fixed(seg["leader"]["sharePct"], 0) + "%"
                             if finite(seg["leader"].get("sharePct")) else "")]
                  for seg in sector["segments"]])
    out.append("")

    out.append("#### 02 · %s — %s" % (ctx.t("earningsLens").upper(), ctx.t("earningsChart")))
    out.append("")
    out.append("_%s_" % ctx.t("earningsChartSub"))
    out.append("")
    out += table([ctx.t("segment"), "RFO YoY", "RFO FY2025", "NPAT YoY", "NPAT FY2025"],
                 [[seg["code"] + " " + ctx.loc(seg["name"]),
                   fmt_pct(seg["metrics"]["rfoYoYPct"]), fmt_amount(seg["metrics"]["rfoFy2025Mb"]),
                   fmt_npat(ctx, seg["metrics"]), fmt_amount(seg["metrics"]["npatOwnersFy2025Mb"])]
                  for seg in sector["segments"]])
    out.append("")

    out.append("#### 03 · %s — %s" % (ctx.t("marketLens").upper(), ctx.t("marketMap")))
    out.append("")
    out.append("_%s_" % ctx.t("marketMapSub"))
    out.append("")
    out += table([ctx.t("segment"), "NPAT YoY", ctx.t("ytd"), ctx.t("marketCap"), ctx.t("quadrant")],
                 [[seg["code"] + " " + ctx.loc(seg["name"]),
                   fmt_pct(seg["metrics"]["npatYoYPct"]), fmt_pct(seg["metrics"]["ytdAdjustedReturnPct"]),
                   to_fixed(seg["marketCapSharePct"], 1) + "%",
                   quadrant(ctx, seg["metrics"]["npatYoYPct"], seg["metrics"]["ytdAdjustedReturnPct"])]
                  for seg in sector["segments"]])
    out.append("")

    out.append("#### 04 · %s — %s" % (ctx.copy("VALUATION", "มูลค่า").upper(), ctx.t("peChart")))
    out.append("")
    out.append("_%s_" % ctx.t("peChartSub"))
    out.append("")
    out += table([ctx.t("segment"), "P/E", ctx.t("coverage")],
                 [[seg["code"] + " " + ctx.loc(seg["name"]),
                   fmt_pe(ctx, seg["metrics"]["aggregatePositiveEarningsPe"]),
                   coverage_text(seg["coverage"]["positivePe"], True)]
                  for seg in sector["segments"]])
    out.append("")


def render_matrix(ctx, sector, out):
    out.append("### %s" % ctx.t("matrixTitle"))
    out.append("")
    out.append("_%s_" % ctx.t("matrixSubtitle"))
    out.append("")
    rows = []
    for index, seg in enumerate(sector["segments"], start=1):
        metrics = seg["metrics"]
        rows.append([
            index,
            "%s %s (%d %s)" % (seg["code"], ctx.loc(seg["name"]), seg["companyCount"], ctx.t("companies")),
            "%s%% (%s)" % (to_fixed(seg["marketCapSharePct"], 1), coverage_text(seg["coverage"]["marketCap"])),
            "%s (%s)" % (fmt_pct(metrics["rfoYoYPct"]), coverage_text(seg["coverage"]["rfo"])),
            "%s (%s)" % (fmt_npat(ctx, metrics), coverage_text(seg["coverage"]["npat"])),
            "%s (%s)" % (fmt_pct(metrics["ytdAdjustedReturnPct"]), coverage_text(seg["coverage"]["ytd"], True)),
            "%s (%s)" % (fmt_pe(ctx, metrics["aggregatePositiveEarningsPe"]),
                         coverage_text(seg["coverage"]["positivePe"], True)),
            "%s%s" % (seg["leader"].get("ticker") or "—",
                      " · " + to_fixed(seg["leader"]["sharePct"], 0) + "%"
                      if finite(seg["leader"].get("sharePct")) else ""),
            status_label(ctx, seg["status"]),
        ])
    out += table([ctx.t("rank"), ctx.t("segment"), "M-cap", "RFO YoY", "NPAT YoY",
                  ctx.t("ytd"), "P/E", ctx.t("leader"), ctx.t("signal")], rows)
    out.append("")


def render_company_story(ctx, segment, company, role, out):
    driver = company.get("performanceDrivers") or {
        "basis": "secondary_synthesis_source_gap", "sourceStatus": "missing_primary_source",
        "materiality": "standard", "rfoDrivers": [rfo_narrative(ctx, company)],
        "npatDrivers": [npat_narrative(ctx, company)], "specialItems": [], "sourceIds": ["FY_PANEL"],
    }
    name, description = business_profile(ctx, company)
    coverage = driver.get("evidenceCoverage") or {}
    status_title, status_detail = source_status(ctx, driver)

    out.append("##### %s — %s · %s" % (company["ticker"], role, materiality_label(ctx, driver.get("materiality"))))
    out.append("")
    out.append("**%s** — %s" % (name, company_bridge(ctx, company)))
    out.append("")
    out.append("_%s_ — %s" % (ctx.t("coreBusiness"), description))
    out.append("")
    out += table(["M-cap", ctx.t("price") + " (THB)", "YTD", "P/E", "NPAT / RFO"],
                 [[fmt_mcap(company.get("marketCapMb")),
                   to_fixed(company["priceThb"], 2) if finite(company.get("priceThb")) else "—",
                   fmt_pct(company.get("ytdAdjustedReturnPct")),
                   fmt_pe(ctx, company.get("pe")),
                   to_fixed(company["netMarginPct"], 1) + "%"
                   if company.get("marginPanel") and finite(company.get("netMarginPct")) else "—"]])
    out.append("")
    out.append("%s · %s — RFO %d · NPAT %d · %s %d" % (
        driver_basis(ctx, driver), ctx.t("claimEvidence"),
        coverage.get("rfo", 0), coverage.get("npat", 0), ctx.t("special"), coverage.get("special", 0)))
    out.append("")

    for kind, key, items in (("rfoWhy", "rfo", driver.get("rfoDrivers")),
                             ("npatWhy", "npat", driver.get("npatDrivers"))):
        prior = company["rfoFy2024Mb"] if key == "rfo" else company["npatOwnersFy2024Mb"]
        current = company["rfoFy2025Mb"] if key == "rfo" else company["npatOwnersFy2025Mb"]
        delta = company["rfoChangeMb"] if key == "rfo" else company["npatChangeMb"]
        pct = company["rfoYoYPct"] if key == "rfo" else company["npatYoYPct"]
        panel = company["rfoPanel"] if key == "rfo" else company["npatPanel"]
        out.append("**%s** — FY2024 %s → FY2025 %s · %s%s" % (
            ctx.t(kind), fmt_amount(prior), fmt_amount(current), fmt_amount_delta(delta),
            " · " + fmt_pct(pct) if panel and finite(pct) else ""))
        out.append("")
        out += render_driver_items(ctx, items)
        out.append("")

    if driver.get("specialItems"):
        out.append("**%s — %s**" % (ctx.t("special"), ctx.t("bridge")))
        out.append("")
        out += render_driver_items(ctx, driver["specialItems"])
        out.append("")

    out.append("> **%s · %s** — %s  " % (ctx.t("evidenceTrail"), status_title, status_detail))
    out.append("> %s: `%s`" % (ctx.t("source"), " / ".join(driver.get("sourceIds") or ["FY_PANEL"])))
    out.append("")


def render_driver_items(ctx, items):
    if not items:
        return ["- _%s_" % ctx.copy("No attributable driver is available.",
                                    "ยังไม่มีปัจจัยขับเคลื่อนที่ระบุสาเหตุได้")]
    lines = []
    for item in items:
        lines.append("- %s" % ctx.loc(item))
        evidence = (item or {}).get("evidence")
        if evidence:
            lines.append("  <details><summary>%s · %s</summary>" % (
                ctx.t("mdaExcerpt"), str(evidence.get("language") or "").upper()))
            lines.append("")
            lines.append("  > %s" % re.sub(r"\s+", " ", evidence.get("quote") or "").strip())
            lines.append("")
            lines.append("  `%s` · `%s` · SHA %s" % (
                evidence.get("sourceId") or "—", evidence.get("passageId") or "—",
                str(evidence.get("quoteSha256") or "")[:12]))
            lines.append("  </details>")
    return lines


def render_segment(ctx, sector, segment, out):
    metrics = segment["metrics"]
    role_map = {role["ticker"]: ctx.loc(role["label"]) for role in segment["roles"]}

    out.append("### %s · %s — %s" % (segment["code"], ctx.loc(segment["name"]), ctx.loc(segment["headline"])))
    out.append("")
    out.append("`%s` · %s%% M-cap · %s · %d %s" % (
        status_label(ctx, segment["status"]), to_fixed(segment["marketCapSharePct"], 1),
        fmt_mcap(segment["marketCapMb"]), segment["companyCount"], ctx.t("companies")))
    out.append("")
    out += table([ctx.copy("Metric", "ตัวชี้วัด"), "RFO", "NPAT", ctx.t("price"), "P/E"],
                 [[ctx.t("period"), "FY2025 YoY", ctx.copy("Owners FY2025 YoY", "ส่วนผู้ถือหุ้น FY2025 YoY"),
                   ctx.t("ytdPrice"), ctx.copy("Positive earners", "เฉพาะบริษัทที่มีกำไร")],
                  [ctx.t("value"), fmt_pct(metrics["rfoYoYPct"]), fmt_npat(ctx, metrics),
                   fmt_pct(metrics["ytdAdjustedReturnPct"]),
                   fmt_pe(ctx, metrics["aggregatePositiveEarningsPe"])],
                  [ctx.t("amount"), fmt_amount(metrics["rfoFy2025Mb"]) + " FY2025",
                   fmt_amount(metrics["npatOwnersFy2025Mb"]) + " FY2025",
                   ctx.copy("EOD ", "ณ ") + display_date(ctx, ctx.meta["effectiveMarketEod"]),
                   ctx.copy("Aggregate multiple", "ค่าเฉลี่ยรวม")],
                  [ctx.t("coverage"), coverage_text(segment["coverage"]["rfo"]),
                   coverage_text(segment["coverage"]["npat"]), coverage_text(segment["coverage"]["ytd"], True),
                   coverage_text(segment["coverage"]["positivePe"], True)]])
    out.append("")
    out.append("**%s** — FY2025: RFO %s • NPAT %s • %s %s • P/E %s • %s RFO %s • NPAT %s" % (
        ctx.t("observed"), fmt_pct(metrics["rfoYoYPct"]), fmt_npat(ctx, metrics),
        ctx.t("ytd"), fmt_pct(metrics["ytdAdjustedReturnPct"]),
        fmt_pe(ctx, metrics["aggregatePositiveEarningsPe"]), ctx.t("coverage"),
        coverage_text(segment["coverage"]["rfo"]), coverage_text(segment["coverage"]["npat"])))
    out.append("")

    fiscal = segment.get("alternativeFiscalView")
    if fiscal:
        out.append("**%s** — %s • %s/%s %s • RFO %s • NPAT %s • Margin %s" % (
            ctx.t("alternativeFiscal"), ctx.loc(fiscal.get("label")), fiscal.get("companyCount"),
            segment["companyCount"], ctx.t("companies"), fmt_pct(fiscal.get("rfoYoYPct")),
            fmt_pct(fiscal.get("npatYoYPct")), fmt_pct(fiscal.get("netMarginPct"))))
        out.append("")

    out.append("#### %s" % ctx.t("whyChanged"))
    out.append("")
    why_claims = [claim for claim in segment.get("claims", []) if claim.get("section") == "why"]
    for index, item in enumerate(segment["why"]):
        claim = why_claims[index] if index < len(why_claims) else {}
        chain_item = segment["chain"][min(index, len(segment["chain"]) - 1)] if segment["chain"] else item
        presentation = driver_presentation(ctx, segment, chain_item, index)
        kind = claim.get("kind") or "analyst_inference"
        headline = presentation["label"] or ctx.loc(chain_item)
        value = (" **%s**" % presentation["value"]) if presentation["value"] else ""
        out.append("%d. _%s_ · %s%s — %s" % (index + 1, ctx.t(kind), headline, value, ctx.loc(item)))
    out.append("")

    out.append("#### %s" % ctx.t("causalChain"))
    out.append("")
    nodes = []
    for index, item in enumerate(segment["chain"]):
        presentation = driver_presentation(ctx, segment, item, index)
        label = presentation["label"] or ctx.loc(item)
        extra = " ".join(part for part in (presentation["value"], presentation["detail"]) if part)
        nodes.append("**%s**%s" % (label, " (%s)" % extra if extra else ""))
    out.append(" → ".join(nodes))
    out.append("")

    out.append("#### %s" % ctx.t("roles"))
    out.append("")
    role_rows = []
    for role in segment["roles"]:
        value, caption = role_metric(ctx, segment, role)
        role_rows.append([ctx.loc(role["label"]), role["ticker"], value, caption])
    out += table([ctx.t("role"), ctx.t("ticker"), ctx.t("value"), ctx.copy("Basis", "ที่มาของค่า")], role_rows)
    out.append("")

    out.append("#### %s" % ctx.copy("Valuation", "มูลค่า"))
    out.append("")
    out.append("**%s** — %s" % (valuation_label(ctx, segment["status"]), ctx.loc(segment["valuation"])))
    out.append("")

    out.append("| %s | %s |" % (ctx.t("trigger"), ctx.t("risk")))
    out.append("|---|---|")
    triggers, risks = segment["triggers"], segment["risks"]
    for index in range(max(len(triggers), len(risks))):
        out.append("| %s | %s |" % (
            cell(ctx.loc(triggers[index])) if index < len(triggers) else "",
            cell(ctx.loc(risks[index])) if index < len(risks) else ""))
    out.append("")
    out.append("**%s** — %s" % (ctx.t("mustProve"), ctx.loc(segment["mustProve"])))
    out.append("")

    out.append("#### %s — %s %s" % (ctx.t("companyPanel"), segment["code"], ctx.loc(segment["name"])))
    out.append("")
    out.append("_%s_" % ctx.t("companyPanelSub"))
    out.append("")
    out += table([ctx.t("ticker"), ctx.t("role"), "M-cap", "RFO YoY", "NPAT YoY", ctx.t("ytd"), "P/E", ctx.t("margin")],
                 [[company["ticker"], role_map.get(company["ticker"], ctx.t("noRole")),
                   fmt_mcap(company.get("marketCapMb")),
                   fmt_pct(company["rfoYoYPct"]) if company.get("rfoPanel") else "—",
                   fmt_npat(ctx, company) if company.get("npatPanel") else "—",
                   fmt_pct(company.get("ytdAdjustedReturnPct")), fmt_pe(ctx, company.get("pe")),
                   to_fixed(company["netMarginPct"], 1) + "%"
                   if company.get("marginPanel") and finite(company.get("netMarginPct")) else "—"]
                  for company in segment["companies"]])
    out.append("")

    if ctx.brief:
        return

    for company in segment["companies"]:
        render_company_story(ctx, segment, company, role_map.get(company["ticker"], ctx.t("noRole")), out)

    render_evidence(ctx, segment, out)


def render_evidence(ctx, segment, out):
    out.append("#### %s — %s" % (ctx.t("claimsRegister"), segment["code"]))
    out.append("")
    out += table([ctx.copy("Section", "ส่วน"), ctx.copy("Kind", "ประเภท"),
                  ctx.copy("Claim", "ข้อสรุป"), ctx.t("sourceId")],
                 [[claim.get("section"), ctx.t(claim.get("kind") or ""), ctx.loc(claim.get("text")),
                   ", ".join(claim.get("sourceIds") or [])]
                  for claim in segment.get("claims", [])])
    out.append("")

    out.append("#### %s — %s" % (ctx.t("evidenceRegister"), segment["code"]))
    out.append("")
    for source in segment.get("sources", []):
        out.append("- **`%s`** · _%s_ — %s" % (source["sourceId"], ctx.t(source.get("kind") or ""), source.get("label")))
        if source.get("detail"):
            out.append("  - %s" % source["detail"])
        details = []
        if source.get("role"):
            details.append("%s: %s" % (ctx.t("sourceRole"), source["role"]))
        if source.get("path"):
            details.append("%s: `%s`" % (ctx.t("sourcePath"), source["path"]))
        if source.get("sha256"):
            details.append("%s: `%s`" % (ctx.t("sourceHash"), source["sha256"]))
        if source.get("url"):
            details.append("URL: <%s>" % source["url"])
        for line in details:
            out.append("  - %s" % line)
    out.append("")


def render(data, ticker_meta, lang, brief=False):
    meta = data["meta"]
    ctx = Ctx(lang, meta, ticker_meta, brief)
    out = []

    out.append("# %s — IS1 Coverage Desk" % ctx.t("pageTitle"))
    out.append("")
    out.append("_%s_" % ctx.t("pageSubtitle"))
    out.append("")
    out.append("%s  " % ctx.t("marketCutoff").format(date=display_date(ctx, meta["effectiveMarketEod"]),
                                                     period=meta["earningsPeriod"]))
    out.append("%s: %s  " % (ctx.t("scope"), meta["scope"]))
    out.append("%s: %s (%s pass / %s fail) · %s: %s  " % (
        ctx.t("qa"), meta["qaVerdict"], meta["qaChecks"]["pass"], meta["qaChecks"]["fail"],
        ctx.t("builtAt"), meta["builtAt"]))
    out.append("`schemaVersion %s` · %s" % (meta["schemaVersion"],
                                            ctx.copy("source: data/sector-intelligence.json",
                                                     "ที่มา: data/sector-intelligence.json")))
    out.append("")
    out.append("> %s" % meta["warning"])
    out.append("")

    out.append("## %s" % ctx.t("contents"))
    out.append("")
    for code, sector in data["sectors"].items():
        out.append("- [%s — %s](#%s)" % (code, ctx.loc(sector["title"]),
                                         anchor("%s — %s" % (code, ctx.loc(sector["title"])))))
        for segment in sector["segments"]:
            title = "%s · %s — %s" % (segment["code"], ctx.loc(segment["name"]), ctx.loc(segment["headline"]))
            out.append("  - [%s](#%s)" % (title, anchor(title)))
    out.append("")

    for code, sector in data["sectors"].items():
        out.append("---")
        out.append("")
        render_overview(ctx, sector, out)
        render_visual_story(ctx, sector, out)
        render_matrix(ctx, sector, out)
        out.append("### %s" % ctx.t("sectorBrief"))
        out.append("")
        for segment in sector["segments"]:
            render_segment(ctx, sector, segment, out)

    out.append("---")
    out.append("")
    out.append("## %s" % ctx.t("methodStrip"))
    out.append("")
    out.append("%s" % ctx.t("definitions"))
    out.append("")
    out.append("### %s" % ctx.t("methodology"))
    out.append("")
    out += table([ctx.copy("Term", "คำ"), ctx.copy("Definition", "นิยาม")],
                 [[key.upper(), value] for key, value in meta["definitions"].items()])
    out.append("")
    out.append("### %s" % ctx.copy("Source lineage", "ลำดับชั้นแหล่งข้อมูล"))
    out.append("")
    for item in meta["sourceLineage"]:
        out.append("- %s" % item)
    out.append("")
    out.append("### %s" % ctx.t("sourceFiles"))
    out.append("")
    for item in meta["sourceFiles"]:
        out.append("- `%s`" % item)
    out.append("")

    return "\n".join(out).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lang", choices=["en", "th", "both"], default="both")
    parser.add_argument("--out-dir", default=os.path.join(ROOT, "docs"))
    parser.add_argument("--brief", action="store_true",
                        help="meeting-length export: drop per-company read-through and the registers")
    args = parser.parse_args()

    with open(DATA, encoding="utf-8") as handle:
        data = json.load(handle)
    ticker_meta = {}
    if os.path.exists(TICKERS):
        with open(TICKERS, encoding="utf-8") as handle:
            for ticker in (json.load(handle).get("tickers") or []):
                if ticker.get("tk"):
                    ticker_meta[ticker["tk"]] = ticker

    os.makedirs(args.out_dir, exist_ok=True)
    languages = ["en", "th"] if args.lang == "both" else [args.lang]
    stem = "sector-intelligence-brief" if args.brief else "sector-intelligence"
    for lang in languages:
        name = "%s.md" % stem if lang == "en" else "%s.%s.md" % (stem, lang)
        path = os.path.join(args.out_dir, name)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(render(data, ticker_meta, lang, args.brief))
        print("wrote %s (%.1f KB)" % (os.path.relpath(path, ROOT), os.path.getsize(path) / 1024))


if __name__ == "__main__":
    main()
