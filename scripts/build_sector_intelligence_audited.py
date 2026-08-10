"""Generate the Sector Intelligence dashboard from the audited v1 panels.

This builder deliberately keeps narrative copy separate from calculations. All
displayed numbers and company membership come only from the audited company
table; segment and sector rows are read from the matching QA-passed snapshot.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import importlib.util
import json
import math
from datetime import datetime, timezone
from pathlib import Path

from build_company_performance_drivers import build_driver, find_mda, load_reports, source_url


def bi(en, th):
    return {"en": en, "th": th}


def number(value):
    try:
        result = float(value)
        return result if math.isfinite(result) else None
    except (TypeError, ValueError):
        return None


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_legacy_content(script_path):
    spec = importlib.util.spec_from_file_location("sector_intelligence_legacy_content", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


STATUS = {
    "F1": "delivered", "F2": "pressure", "F3": "expectation", "F4": "expectation",
    "F5": "pressure", "F6": "pressure", "F7": "expectation", "F8": "pressure", "F9": "pressure",
    "P1": "pressure", "P2": "expectation", "P3": "delivered", "P4": "expectation", "P5": "event",
}

WHY_CLAIM_KIND = {
    "F1": ["fact_calculated", "management_explanation", "fact_calculated", "analyst_inference"],
    "F2": ["fact_calculated", "analyst_inference", "analyst_inference"],
    "F3": ["fact_calculated", "management_explanation", "analyst_test"],
    "F4": ["fact_calculated", "management_explanation", "fact_calculated"],
    "F5": ["fact_calculated", "fact_calculated", "management_explanation"],
    "F6": ["fact_calculated", "fact_calculated", "fact_calculated"],
    "F7": ["fact_calculated", "fact_calculated", "analyst_inference"],
    "F8": ["fact_calculated", "fact_calculated", "fact_calculated"],
    "F9": ["fact_calculated", "fact_calculated", "fact_calculated"],
    "P1": ["fact_calculated", "management_explanation", "fact_calculated"],
    "P2": ["fact_calculated", "management_explanation", "analyst_inference"],
    "P3": ["fact_calculated", "management_explanation", "analyst_inference"],
    "P4": ["fact_calculated", "management_explanation", "management_explanation"],
    "P5": ["fact_calculated", "analyst_inference", "fact_calculated"],
}
WHY_MARKET_INDEXES = {"F2": {2}, "F3": {2}, "F4": {2}, "P1": {2}, "P2": {0}}
WHY_CLAIM_SOURCE_IDS = {
    ("F1", 1): ["F1_E1"],
}


ROLE_SPEC = {
    "F1": [("Leader", "ผู้นำ", "CPF"), ("RFO driver", "ตัวเพิ่ม RFO", "BTG"), ("Rising star", "ดาวรุ่ง", "TFG")],
    "F2": [("Leader / direction", "ผู้นำและกำหนดทิศ", "TU"), ("Comparator", "ตัวเทียบ", "CFRESH")],
    "F3": [("Leader / driver", "ผู้นำและตัวขับเคลื่อน", "ITC"), ("Comparator", "ตัวเทียบ", "AAI")],
    "F4": [("Leader / profit driver", "ผู้นำและตัวเพิ่มกำไร", "OSP"), ("Price driver", "ตัวผลักราคา", "CBG")],
    "F5": [("Leader / profit drag", "ผู้นำและตัวฉุดกำไร", "M"), ("Growth contrast", "ตัวเทียบการเติบโต", "OKJ"), ("Mapped loss swing", "ตัวแปรขาดทุน", "AQUA")],
    "F6": [("Leader / profit drag", "ผู้นำและตัวฉุดกำไร", "TFMAMA"), ("RFO driver", "ตัวเพิ่ม RFO", "NSL")],
    "F7": [("Leader / quality anchor", "ผู้นำและตัวแทนคุณภาพ", "SAUCE"), ("Loss-narrowing driver", "ตัวขับเคลื่อนจากขาดทุนลด", "NRF"), ("Profit drag", "ตัวฉุดกำไร", "RBF")],
    "F8": [("Leader / revenue drag", "ผู้นำและตัวฉุดรายได้", "TVO"), ("All-FY profit drag", "ตัวฉุดกำไรมุมทุกปีบัญชี", "KSL")],
    "F9": [("Leader / largest negative price contribution", "ผู้นำและตัวฉุดราคามากสุด", "SUN"), ("RFO drag", "ตัวฉุด RFO", "SST"), ("Profit drag", "ตัวฉุดกำไร", "APURE")],
    "P1": [("Leader", "ผู้นำ", "LH"), ("Earnings drag", "ตัวฉุดผลประกอบการ", "SPALI"), ("YTD price leader", "ผู้นำราคา YTD", "ASW")],
    "P2": [("Leader", "ผู้นำ", "WHA"), ("FDI / price bellwether", "ตัวแทน FDI และราคา", "AMATA"), ("Reported earnings swing", "ตัวแปรกำไรรายงาน", "ROJNA")],
    "P3": [("Leader / profit driver", "ผู้นำและตัวเพิ่มกำไร", "CPN"), ("Diversified comparator", "ตัวเทียบแบบ diversified", "MBK")],
    "P4": [("Leader / operating delivery", "ผู้นำและส่งมอบการดำเนินงาน", "AWC"), ("Impairment drag", "ตัวฉุดจากด้อยค่า", "S")],
    "P5": [("Leader / loss drag", "ผู้นำและตัวฉุดขาดทุน", "STELLA"), ("Event profit swing", "ตัวแปรกำไรจาก event", "RABBIT"), ("Non-calendar comparator", "ตัวเทียบต่างรอบปี", "UV")],
}

AFFECTED_COPY = {
    "F1": {
        "why": [bi("FY2025 RFO was nearly flat (+0.8%) while owner NPAT rose 54.2%, making the recovery margin-led.", "FY2025 RFO เกือบทรงตัว (+0.8%) ขณะที่ NPAT ส่วนผู้ถือหุ้นเพิ่ม 54.2% จึงเป็นการฟื้นจาก margin"), bi("CPF attributed improvement to production-cost control, lower soybean-meal costs, biosecurity and higher hog prices.", "CPF ระบุปัจจัยจากการควบคุมต้นทุน ต้นทุนกากถั่วเหลืองลดลง biosecurity และราคาสุกรสูงขึ้น"), bi("TFG and BTG broadened the recovery beyond CPF in the audited segment arithmetic.", "TFG และ BTG ทำให้การฟื้นกระจายออกจาก CPF ตามการคำนวณ panel ที่สอบทาน"), bi("The segment conclusion combines audited panel arithmetic with issuer-specific MD&A and is not a single-company causal proof.", "ข้อสรุปกลุ่มผสานการคำนวณ panel ที่สอบทานกับ MD&A รายบริษัท ไม่ใช่หลักฐานเหตุเชิงสาเหตุจากบริษัทเดียว")],
    },
    "F2": {
        "headline": bi("Prices improved despite FY2025 earnings pressure", "ราคาปรับดีขึ้นแม้ผลประกอบการ FY2025 ยังถูกกดดัน"),
        "must_prove": bi("6M26 must extend 4Q25 sales stabilisation into gross-margin and owner-profit recovery; FY2025 sales still declined.", "6M26 ต้องต่อยอดยอดขายที่เริ่มทรงตัวใน 4Q25 ไปสู่การฟื้นของ gross margin และกำไรส่วนผู้ถือหุ้น โดยยอดขาย FY2025 ยังลดลง"),
    },
    "F3": {
        "why": [bi("ITC delivered most of the RFO growth but also the largest profit decline.", "ITC สร้างการเติบโตของ RFO ส่วนใหญ่ แต่เป็นตัวฉุดกำไรมากที่สุด"), bi("Premium mix and volume growth were offset by baht appreciation, raw-material pressure and transformation costs.", "premium mix และปริมาณขายที่เพิ่มถูกหักล้างด้วยเงินบาทแข็ง ต้นทุนวัตถุดิบ และต้นทุน transformation"), bi("New-capacity utilisation is a 6M26 test, not an established FY2025 causal explanation.", "utilisation ของกำลังผลิตใหม่เป็นประเด็นที่ต้องพิสูจน์ใน 6M26 ไม่ใช่คำอธิบายเหตุของ FY2025 ที่ยืนยันแล้ว")],
    },
    "F5": {
        "headline": bi("Weak restaurant demand; mapped owner profit fell faster than RFO", "อุปสงค์ร้านอาหารอ่อนแอ และกำไรส่วนผู้ถือหุ้นของกลุ่มที่ map แล้วลดเร็วกกว่า RFO"),
        "why": [bi("Five-company comparable RFO fell 4.2%; AQUA has no comparable RFO and is not substituted with total revenue.", "RFO ที่เทียบได้ 5 บริษัทลด 4.2%; AQUA ไม่มี RFO เทียบเคียงและไม่ใช้รายได้รวมแทน"), bi("All-six owner NPAT fell 76.6%, including AQUA's loss attributable to owners.", "NPAT ส่วนผู้ถือหุ้นของทั้ง 6 บริษัทลด 76.6% รวมขาดทุนของ AQUA"), bi("M cited weak purchasing power and negative same-store sales; OKJ is the growth contrast.", "M ระบุกำลังซื้ออ่อนและ same-store sales ติดลบ ขณะที่ OKJ เป็นตัวเทียบด้านการเติบโต")],
        "must_prove": bi("6M26 must show positive core-restaurant SSSG and store EBITDA, plus a separate AQUA bridge for associate losses, impairments and operating cash flow.", "6M26 ต้องเห็น SSSG และ store EBITDA ของธุรกิจร้านอาหารหลักเป็นบวก พร้อม bridge แยกของ AQUA สำหรับขาดทุนบริษัทร่วม ด้อยค่า และกระแสเงินสดดำเนินงาน"),
    },
    "F7": {
        "headline": bi("Revenue contracted, but NRF's loss narrowing lifted owner profit", "รายได้หดตัว แต่ขาดทุน NRF ที่ลดลงช่วยยกกำไรส่วนผู้ถือหุ้น"),
        "why": [bi("RFO fell 7.0%, led by NRF's decline.", "RFO ลด 7.0% โดยมี NRF เป็นตัวฉุดหลัก"), bi("Owner NPAT rose from THB169.9m to THB700.0m as NRF's loss narrowed.", "NPAT ส่วนผู้ถือหุ้นเพิ่มจาก 169.9 ล้านบาทเป็น 700.0 ล้านบาท จากขาดทุน NRF ที่ลดลง"), bi("RBF remained the largest negative profit delta among profitable issuers; SAUCE anchors quality.", "RBF ยังเป็นตัวฉุดกำไรหลักในกลุ่มบริษัทที่มีกำไร ขณะที่ SAUCE เป็น quality anchor")],
    },
    "F8": {
        "headline": bi("Calendar panel weakened; the all-issuer FY view is materially worse", "งวดปฏิทินอ่อนตัว และมุมทุกปีบัญชีแย่กว่าชัดเจน"),
        "why": [bi("December-FYE panel: RFO -7.0% and owner NPAT -21.0% on 7/9 coverage.", "กลุ่มปิดงบธันวาคม: RFO -7.0% และ NPAT ส่วนผู้ถือหุ้น -21.0% ครอบคลุม 7/9 บริษัท"), bi("All-issuer FY view: RFO -5.2% and NPAT -60.0%; it mixes 30-Sep, 31-Oct and 31-Dec closes and is labelled separately.", "มุมทุกปีบัญชี: RFO -5.2% และ NPAT -60.0%; ผสมรอบปิดงบ 30 ก.ย., 31 ต.ค. และ 31 ธ.ค. จึงแสดงแยก"), bi("TVO was the revenue drag; KSL was the all-FY profit drag.", "TVO เป็นตัวฉุดรายได้ และ KSL เป็นตัวฉุดกำไรในมุมทุกปีบัญชี")],
        "triggers": [bi("TVO soybean-meal/oil crush margin and inventory/NRV bridge improve", "crush margin ถั่วเหลืองและ bridge inventory/NRV ของ TVO ดีขึ้น"), bi("KSL/KTIS cane volume and realised sugar price improve", "ปริมาณอ้อยและราคาขายน้ำตาลจริงของ KSL/KTIS ดีขึ้น"), bi("Issuer-level operating cash flow covers debt service", "กระแสเงินสดดำเนินงานรายบริษัทครอบคลุมภาระหนี้")],
        "risks": [bi("TVO soybean input/output price mismatch", "ราคาวัตถุดิบและผลิตภัณฑ์ถั่วเหลืองของ TVO ไม่สอดคล้อง"), bi("Lower sugar prices, weather and cane-volume volatility at KSL/KTIS", "ราคาน้ำตาลลดลง สภาพอากาศ และปริมาณอ้อยผันผวนที่ KSL/KTIS"), bi("KSL-specific leverage, litigation and refinancing risk", "ความเสี่ยงเฉพาะ KSL ด้าน leverage คดีความ และ refinancing")],
        "must_prove": bi("6M26 must separately bridge TVO crush/NRV and KSL/KTIS cane volume, realised sugar price, hedging, impairment and debt service.", "6M26 ต้อง bridge แยก TVO ด้าน crush/NRV และ KSL/KTIS ด้านปริมาณอ้อย ราคาน้ำตาลจริง hedging ด้อยค่า และการชำระหนี้"),
    },
    "F9": {
        "headline": bi("The audited cohort turned to loss; headline P/E is not representative", "กลุ่มที่สอบทานแล้วพลิกเป็นขาดทุน และ P/E headline ไม่เป็นตัวแทน"),
        "why": [bi("The eight-company cohort recorded RFO -9.8% and turned from THB450.6m profit to THB914.5m loss.", "กลุ่ม 8 บริษัทมี RFO -9.8% และพลิกจากกำไร 450.6 ล้านบาทเป็นขาดทุน 914.5 ล้านบาท"), bi("CM uses a same-basis FY2024 separate comparator; the prior consolidated/separate comparison was removed.", "CM ใช้ FY2024 แบบงบเฉพาะกิจการให้ฐานตรงกัน และยกเลิกการเทียบ consolidated กับ separate"), bi("The positive-earner P/E covers only SUN and SSF, so it cannot describe the loss-making cohort.", "P/E ของผู้มีกำไรครอบคลุมเพียง SUN และ SSF จึงอธิบายกลุ่มที่ขาดทุนไม่ได้")],
        "must_prove": bi("6M26 must show lower operating losses, APURE ECL and receivable recovery, and operating-cash-flow normalisation before valuation is meaningful.", "6M26 ต้องเห็นขาดทุนดำเนินงานลดลง การฟื้นของ ECL และลูกหนี้ APURE และกระแสเงินสดดำเนินงานกลับปกติก่อนที่ valuation จะมีความหมาย"),
    },
    "P1": {
        "headline": bi("Credit-constrained demand drove broad earnings pressure", "ข้อจำกัดสินเชื่อกดดันผลประกอบการในวงกว้าง"),
        "why": [bi("Audited RFO fell 11.8% and owner NPAT fell 33.8% across 33/37 companies.", "RFO ที่สอบทานแล้วลด 11.8% และ NPAT ส่วนผู้ถือหุ้นลด 33.8% ใน 33/37 บริษัท"), bi("Transfers, mix and gross margin weakened while mortgage rejection remained elevated.", "ยอดโอน mix และ gross margin อ่อนตัว ขณะที่การปฏิเสธสินเชื่อยังสูง"), bi("ASW led current YTD price, but FY2025 earnings did not confirm broad recovery.", "ASW นำราคา YTD ปัจจุบัน แต่กำไร FY2025 ยังไม่ยืนยันการฟื้นในวงกว้าง")],
    },
    "P2": {
        "headline": bi("FDI optionality drove price ahead of reported earnings", "FDI optionality ผลักราคานำกำไรรายงาน"),
        "why": [bi("Audited RFO fell 12.4% and owner NPAT fell 29.8%, despite strong YTD price performance.", "RFO ลด 12.4% และ NPAT ส่วนผู้ถือหุ้นลด 29.8% แม้ราคา YTD แข็งแรง"), bi("Land transfers lagged expectations while FDI and data-centre readiness supported optionality.", "การโอนที่ดินต่ำกว่าคาด ขณะที่ FDI และความพร้อม data centre สนับสนุน optionality"), bi("ROJNA is a reported-earnings and mark-to-market swing, not clean operating proof.", "ROJNA เป็นตัวแปรกำไรรายงานและ mark-to-market ไม่ใช่หลักฐานการดำเนินงานที่สะอาด")],
    },
    "P3": {
        "headline": bi("Recurring income delivered the cleanest earnings-price alignment", "รายได้ประจำส่งมอบความสอดคล้องของกำไรและราคาชัดที่สุด"),
        "why": [bi("Audited RFO rose 0.6% and owner NPAT rose 13.7% across all five companies.", "RFO เพิ่ม 0.6% และ NPAT ส่วนผู้ถือหุ้นเพิ่ม 13.7% ครบทั้ง 5 บริษัท"), bi("CPN's traffic, occupancy and recurring rental indicators anchored the segment.", "traffic, occupancy และรายได้ค่าเช่าประจำของ CPN เป็นฐานของกลุ่ม"), bi("MBK remains a diversified comparator; not all of its profit is shopping-centre operating evidence.", "MBK เป็นตัวเทียบแบบ diversified และกำไรทั้งหมดไม่ใช่หลักฐานการดำเนินงานศูนย์การค้า")],
    },
    "P4": {
        "headline": bi("AWC delivered operational growth, but S impairment pulled the panel down", "AWC ส่งมอบการเติบโต แต่ด้อยค่าของ S ฉุดภาพรวม"),
        "why": [bi("The 3/4 December-FYE panel recorded RFO -2.0% and owner NPAT -15.8%; BLAND is excluded for its March FYE.", "กลุ่มปิดงบธันวาคม 3/4 บริษัทมี RFO -2.0% และ NPAT -15.8%; BLAND ถูกตัดออกเพราะปิดงบมีนาคม"), bi("AWC grew RFO and NPAT, but a THB5.555bn fair-value gain requires an operating-to-reported bridge.", "AWC เพิ่ม RFO และ NPAT แต่มี fair-value gain 5,555 ล้านบาท จึงต้อง bridge จาก operating ไป reported"), bi("S recorded a THB1.963bn impairment; normalized profit was THB531m.", "S บันทึกด้อยค่า 1,963 ล้านบาท ขณะที่กำไรปกติ 531 ล้านบาท")],
    },
    "P5": {
        "headline": bi("The revised panel stayed loss-making, but the loss narrowed", "กลุ่มที่ปรับใหม่ยังขาดทุน แต่ขาดทุนลดลง"),
        "why": [bi("RFO fell 14.2%, while owner loss narrowed from THB3.020bn to THB2.653bn.", "RFO ลด 14.2% ขณะที่ขาดทุนส่วนผู้ถือหุ้นลดจาก 3,020 ล้านบาทเป็น 2,653 ล้านบาท"), bi("RABBIT's event-influenced turnaround offset deterioration at STELLA and CGD.", "การพลิกตัวที่ได้รับอิทธิพลจาก event ของ RABBIT ชดเชยการอ่อนตัวของ STELLA และ CGD"), bi("UV is a non-calendar comparator and is excluded from the December-FYE earnings panel.", "UV เป็นตัวเทียบต่างรอบปีและไม่รวมในกลุ่มผลประกอบการปิดงบธันวาคม")],
    },
}

EVIDENCE = {
    "F1": [("management", "CPF FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/CPF/MDA_CPF_2025FY_T.md"), ("forward", "KSS TFG research", "Listed Company/1-Raw/06-Market Reference/Broker Research/2026/FOOD/KSS_TFG_345421.md")],
    "F2": [("management", "TU FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/TU/MDA_TU_2025FY_E.md")],
    "F3": [("management", "ITC FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/ITC/MDA_ITC_2025FY_E.md"), ("management", "AAI FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/AAI/MDA_AAI_2025FY_E.md")],
    "F4": [("management", "OSP FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/OSP/MDA_OSP_2025FY_E.md"), ("forward", "BLS CBG research", "Listed Company/1-Raw/06-Market Reference/Broker Research/2026/FOOD/BLS_CBG_345849.md")],
    "F5": [("management", "M FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/M/MDA_M_2025FY_E.md"), ("management", "AQUA FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/AQUA/MDA_AQUA_2025FY_E.md")],
    "F6": [("management", "TFMAMA FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/TFMAMA/MDA_TFMAMA_2025FY_E.md"), ("management", "NSL FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/NSL/MDA_NSL_2025FY_E.md")],
    "F7": [("management", "NRF FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/NRF/MDA_NRF_2025FY_E.md"), ("management", "SAUCE FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/SAUCE/MDA_SAUCE_2025FY_E.md"), ("forward", "FSSIA RBF research", "Listed Company/1-Raw/06-Market Reference/Broker Research/2026/FOOD/FSSIA_RBF_347820.md")],
    "F8": [("management", "TVO FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/TVO/MDA_TVO_2025FY_E.md"), ("management", "KSL FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/KSL/MDA_KSL_2025FY_T.md"), ("management", "KTIS FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/KTIS/MDA_KTIS_2025FY_T.md"), ("credit_analysis", "TRIS KSL credit analysis", "Listed Company/1-Raw/06-Market Reference/Credit Rating Research/2025/FOOD/TRIS_KSL_149-2025.md")],
    "F9": [("management", "SUN FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/SUN/MDA_SUN_2025FY_E.md"), ("management", "CM FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/CM/MDA_CM_2025FY_E.md"), ("management", "SST FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/SST/MDA_SST_2025FY_T.md"), ("management", "APURE FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/APURE/MDA_APURE_2025FY_E.md")],
    "P1": [("management", "SPALI FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/SPALI/MDA_SPALI_2025FY_E.md"), ("management", "PSH FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/PSH/MDA_PSH_2025FY_E.md"), ("management", "SAMCO FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/SAMCO/MDA_SAMCO_2025FY_E.md"), ("forward", "INVX LH research", "Listed Company/1-Raw/06-Market Reference/Broker Research/2026/PROP/INVX_LH_343581.md")],
    "P2": [("management", "AMATA FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/AMATA/MDA_AMATA_2025FY_E.md"), ("management", "ROJNA FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/ROJNA/MDA_ROJNA_2025FY_E.md"), ("management", "MK FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/MK/MDA_MK_2025FY_E.md"), ("management", "JCK FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/JCK/MDA_JCK_2025FY_E.md"), ("forward", "MST WHA research", "Listed Company/1-Raw/06-Market Reference/Broker Research/2026/PROP/MST_WHA_348118.md")],
    "P3": [("management", "CPN FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/CPN/MDA_CPN_2025FY_E.md"), ("management", "GLAND FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/GLAND/MDA_GLAND_2025FY_E.md"), ("credit_analysis", "TRIS MBK credit analysis", "Listed Company/1-Raw/06-Market Reference/Credit Rating Research/2025/PROP/TRIS_MBK_180-2025.md")],
    "P4": [("management", "AWC FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/AWC/MDA_AWC_2025FY_E.md"), ("management", "S FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/S/MDA_S_2025FY_E.md")],
    "P5": [("management", "STELLA FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/STELLA/MDA_STELLA_2025FY_E.md"), ("management", "RABBIT FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/RABBIT/MDA_RABBIT_2025FY_E.md"), ("management", "UV FY2025 MD&A", "Listed Company/1-Raw/01-Filings/MDA/UV/MDA_UV_2025FY_T.md")],
}

VALUATION_LOGIC = {
    "F1": bi("Cycle discount reflects commodity and reversal risk.", "ส่วนลดวัฏจักรสะท้อนความเสี่ยงสินค้าโภคภัณฑ์และการกลับทิศ"),
    "F2": bi("Discount reflects export, raw-material and margin uncertainty.", "ส่วนลดสะท้อนความไม่แน่นอนด้านส่งออก วัตถุดิบ และ margin"),
    "F3": bi("Premium reflects pet-food growth and margins; execution must catch up.", "premium สะท้อนการเติบโตและ margin ของ pet food แต่ต้องพิสูจน์ execution"),
    "F4": bi("Brand and distribution support a premium, conditional on volume recovery.", "แบรนด์และช่องทางจำหน่ายสนับสนุน premium โดยมีเงื่อนไขว่า volume ต้องฟื้น"),
    "F5": bi("The multiple prices a turnaround while current earnings remain weak.", "multiple ให้ค่ากับ turnaround ขณะที่กำไรปัจจุบันยังอ่อน"),
    "F6": bi("Defensive brands support valuation, but flat RFO caps upside.", "แบรนด์ defensive พยุงมูลค่า แต่ RFO ที่ทรงตัวจำกัด upside"),
    "F7": bi("The premium reflects SAUCE quality and RBF optionality, not broad revenue delivery.", "premium สะท้อนคุณภาพ SAUCE และ optionality ของ RBF ไม่ใช่การเติบโตรายได้ทั้งกลุ่ม"),
    "F8": bi("The positive-earner panel multiple reflects heterogeneous commodity cycles. Separately, KSL adds leveraged-issuer, litigation and refinancing risk; that risk is not part of the P/E-eligible set.", "multiple ของกลุ่มผู้มีกำไรสะท้อนวัฏจักรสินค้าโภคภัณฑ์ที่แตกต่าง ส่วน KSL เพิ่มความเสี่ยงด้าน leverage คดีความ และ refinancing แยกต่างหาก โดย KSL ไม่อยู่ในชุดบริษัทที่ใช้คำนวณ P/E"),
    "F9": bi("A positive-earner P/E is not representative of a loss-making cohort.", "P/E ของผู้มีกำไรไม่เป็นตัวแทนกลุ่มที่ขาดทุน"),
    "P1": bi("The discount reflects affordability, transfers and cash-conversion risk.", "ส่วนลดสะท้อนกำลังซื้อ การโอน และ cash-conversion risk"),
    "P2": bi("The rerating is consistent with FDI/data-centre expectations, not yet earnings proof.", "rerating สอดคล้องกับความคาดหวัง FDI/data centre แต่ยังไม่ใช่หลักฐานกำไร"),
    "P3": bi("Recurring cash flow and CPN quality support the premium.", "กระแสเงินสดประจำและคุณภาพ CPN สนับสนุน premium"),
    "P4": bi("Price reflects tourism and asset optionality; normalized cash earnings remain the test.", "ราคาสะท้อน tourism และ asset optionality แต่ต้องพิสูจน์กำไรเงินสดปกติ"),
    "P5": bi("The P/E is event-led and not representative of the loss-making bucket.", "P/E ขับเคลื่อนด้วย event และไม่เป็นตัวแทนกลุ่มที่ขาดทุน"),
}


def valuation_text(code, metrics, coverage):
    pe = metrics["aggregatePositiveEarningsPe"]
    lead = f"Current positive-earner P/E is {pe:.1f}x" if pe is not None else "Current positive-earner P/E is not meaningful"
    en = f"{lead}, covering {coverage['positivePe']['count']}/{coverage['positivePe']['total']} issuers and {coverage['positivePe']['marketCapPct']:.1f}% of known market cap. {VALUATION_LOGIC[code]['en']}"
    th_lead = f"P/E ของผู้มีกำไรปัจจุบันอยู่ที่ {pe:.1f}x" if pe is not None else "P/E ของผู้มีกำไรปัจจุบันไม่มีนัยสำคัญ"
    th = f"{th_lead} ครอบคลุม {coverage['positivePe']['count']}/{coverage['positivePe']['total']} บริษัท และ {coverage['positivePe']['marketCapPct']:.1f}% ของ market cap ที่มีข้อมูล. {VALUATION_LOGIC[code]['th']}"
    return bi(en, th)


def build(theme_root, legacy_script, snapshot_dir, effective_eod):
    theme_root = theme_root.resolve()
    legacy_script = legacy_script.resolve()
    legacy = load_legacy_content(legacy_script)
    content = copy.deepcopy(legacy.CONTENT)
    for code, replacement in AFFECTED_COPY.items():
        content[code].update(replacement)
    for code, roles in ROLE_SPEC.items():
        content[code]["roles"] = [{"label": bi(en, th), "ticker": ticker} for en, th, ticker in roles]
        content[code]["status"] = STATUS[code]

    snapshot = snapshot_dir.resolve()
    company_path = snapshot / f"food_prop_company_fy2024_2025_audited_{effective_eod}.csv"
    segment_path = snapshot / f"food_prop_segment_fy2024_2025_audited_{effective_eod}.csv"
    sector_path = snapshot / f"food_prop_sector_fy2024_2025_audited_{effective_eod}.csv"
    qa_path = sorted(snapshot.glob("QA_SUMMARY_FY2024_2025_AUDITED_*.json"))[0]
    provenance_path = sorted(snapshot.glob("PROVENANCE_FY2024_2025_AUDITED_*.json"))[0]
    companies = read_csv(company_path)
    segments = read_csv(segment_path)
    sectors = read_csv(sector_path)
    qa = json.loads(qa_path.read_text(encoding="utf-8"))
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    if qa.get("verdict") != "PASS":
        raise ValueError("Audited FY panel QA is not PASS")
    if {row["market_date"] for row in companies} != {effective_eod}:
        raise ValueError("Company panel market dates do not match the requested effective EOD")
    override_sources = provenance.get("override_sources") or {}

    vault_root = next(parent for parent in [theme_root, *theme_root.parents] if parent.name == "Work-SET")
    repo_root = Path(__file__).resolve().parents[1]
    company_reports, company_reports_path = load_reports(repo_root)
    ticker_summary_path = repo_root / "data" / "ticker-summary.json"
    ticker_summary = json.loads(ticker_summary_path.read_text(encoding="utf-8"))
    ticker_profiles = {row["tk"]: row for row in ticker_summary.get("tickers", [])}
    perimeter_tickers = {row["ticker"] for row in companies}
    profile_gaps = sorted(
        ticker
        for ticker in perimeter_tickers
        if ticker not in ticker_profiles
        or not ticker_profiles[ticker].get("businessType")
        or not ticker_profiles[ticker].get("businessTypeTh")
        or not any("\u0e00" <= char <= "\u0e7f" for char in ticker_profiles[ticker].get("businessTypeTh", ""))
    )
    if profile_gaps:
        raise ValueError("Bilingual SET company profiles missing: " + ", ".join(profile_gaps))

    def business_description(ticker):
        profile = ticker_profiles[ticker]
        return bi(
            profile.get("businessType") or company_reports.get(ticker, {}).get("business") or "",
            profile["businessTypeTh"],
        )

    quant_sources = {
        "FY_PANEL": {"kind": "fact_calculated", "label": "Audited FY2024-25 company panel", "detail": f"RFO / NPAT-to-owners / independent panel membership; QA {qa['counts']['pass']} pass / {qa['counts']['fail']} fail", "path": str(company_path.relative_to(vault_root)).replace("\\", "/"), "sha256": sha256(company_path), "role": "historical fact", "url": None},
        "SET_PUBLIC_EOD": {"kind": "fact_calculated", "label": f"SET public Company Highlights — EOD {effective_eod}", "detail": "Adjusted YTD; unadjusted price, market cap and valuation; factsheet-surface cross-check", "path": str((snapshot / f"food_prop_set_public_surface_reconciliation_{effective_eod}.csv").relative_to(vault_root)).replace("\\", "/"), "sha256": sha256(snapshot / f"food_prop_set_public_surface_reconciliation_{effective_eod}.csv"), "role": "current market fact", "url": None},
        "SET_COMPANY_PROFILE": {"kind": "fact", "label": "SET company profiles — English and Thai", "detail": "Official company names and business descriptions refreshed and validated for the 118-company perimeter from the public SET profile API", "path": None, "sha256": None, "role": "company business profile", "url": "https://www.set.or.th/th/market/product/stock/overview"},
    }

    segment_payload = {}
    for row in segments:
        code = row["primary_segment_code"]
        segment_companies = [company for company in companies if company["primary_segment_code"] == code]
        segment_companies.sort(key=lambda company: -(number(company["market_cap_mb"]) or 0))
        coverage = {
            "rfo": {"count": int(row["rfo_panel_company_count"]), "total": int(row["universe_company_count"]), "included": row["rfo_panel_tickers"].split(";") if row["rfo_panel_tickers"] else [], "excluded": row["rfo_panel_excluded_tickers"].split(";") if row["rfo_panel_excluded_tickers"] else []},
            "npat": {"count": int(row["npat_panel_company_count"]), "total": int(row["universe_company_count"]), "included": row["npat_panel_tickers"].split(";") if row["npat_panel_tickers"] else [], "excluded": row["npat_panel_excluded_tickers"].split(";") if row["npat_panel_excluded_tickers"] else []},
            "margin": {"count": int(row["margin_panel_company_count"]), "total": int(row["universe_company_count"]), "included": row["margin_panel_tickers"].split(";") if row["margin_panel_tickers"] else [], "excluded": [ticker for ticker in row["universe_tickers"].split(";") if ticker not in set(row["margin_panel_tickers"].split(";"))]},
            "marketCap": {"count": int(row["known_market_cap_company_count"]), "total": int(row["universe_company_count"]), "missing": row["market_cap_missing_tickers"].split(";") if row["market_cap_missing_tickers"] else []},
            "ytd": {"count": int(row["ytd_company_count"]), "total": int(row["universe_company_count"]), "marketCapPct": number(row["ytd_market_cap_coverage_pct"]), "missing": row["ytd_missing_tickers"].split(";") if row["ytd_missing_tickers"] else []},
            "positivePe": {"count": int(row["positive_pe_company_count"]), "total": int(row["universe_company_count"]), "marketCapPct": number(row["positive_pe_market_cap_coverage_pct"]), "included": row["positive_pe_tickers"].split(";") if row["positive_pe_tickers"] else [], "excluded": row["positive_pe_excluded_tickers"].split(";") if row["positive_pe_excluded_tickers"] else []},
        }
        metrics = {
            "rfoFy2024Mb": number(row["fy2024_rfo_mb"]), "rfoFy2025Mb": number(row["fy2025_rfo_mb"]),
            "rfoYoYPct": number(row["rfo_yoy_pct"]),
            "npatOwnersFy2024Mb": number(row["fy2024_npat_owners_mb"]), "npatOwnersFy2025Mb": number(row["fy2025_npat_owners_mb"]),
            "npatChangeMb": number(row["npat_change_mb"]), "npatYoYPct": number(row["npat_yoy_pct_positive_base_only"]),
            "npatState": row["npat_state"], "netMarginFy2024Pct": number(row["fy2024_net_margin_pct_comparable"]), "netMarginPct": number(row["fy2025_net_margin_pct_comparable"]),
            "rfoDirectionDriver": row["rfo_direction_driver"], "rfoDirectionDriverChangeMb": number(row["rfo_direction_driver_change_mb"]),
            "npatDirectionDriver": row["npat_direction_driver"], "npatDirectionDriverChangeMb": number(row["npat_direction_driver_change_mb"]),
            "ytdAdjustedReturnPct": number(row["ytd_adjusted_return_pct"]), "ytdPositiveBreadthPct": number(row["ytd_positive_breadth_pct"]),
            "aggregatePositiveEarningsPe": number(row["aggregate_positive_earnings_pe"]), "aggregatePbv": number(row["aggregate_positive_pbv"]),
            "dividendYieldPct": number(row["market_cap_weighted_dividend_yield_pct"]),
        }
        copy_row = content[code]
        sources = [dict(sourceId=source_id, **source) for source_id, source in quant_sources.items()]
        sources.append({
            "sourceId": "COMPANY_REPORTS",
            "kind": "analyst_inference",
            "label": "Company report synthesis corpus",
            "detail": "Annual-only draft synthesis; reconciled to the ticker FY2025 MD&A where available",
            "path": "data/company-reports.json",
            "sha256": sha256(company_reports_path),
            "role": "secondary synthesis; not management attribution",
            "url": None,
        })
        role_tickers = {item["ticker"] for item in copy_row["roles"]}
        company_driver_map = {}
        for company in segment_companies:
            ticker = company["ticker"]
            mda_path = find_mda(vault_root, ticker)
            driver = build_driver(company, company_reports.get(ticker, {}), mda_path, role_tickers)
            company_driver_map[ticker] = driver
            if mda_path:
                relative_mda = str(mda_path.relative_to(vault_root)).replace("\\", "/")
                verified = driver["sourceStatus"] == "primary_verified"
                sources.append({
                    "sourceId": f"MDA_{ticker}_FY2025",
                    "kind": "management_explanation" if verified else "source_gap",
                    "label": f"{ticker} FY2025 MD&A" + ("" if verified else " · re-extraction required"),
                    "detail": ("Primary annual management explanation with claim-level excerpts and excerpt SHA-256"
                               if verified else
                               "A FY2025 MD&A file exists, but its markdown extraction is not substantive enough for causal attribution"),
                    "path": relative_mda,
                    "sha256": sha256(mda_path),
                    "role": "FY2025 operating-performance attribution" if verified else "source-quality exception",
                    "url": source_url(mda_path),
                })
        override_evidence_ids = []
        override_evidence_ids_main = []
        for company in segment_companies:
            override_source = override_sources.get(company["ticker"])
            if not override_source:
                continue
            source_path = vault_root / Path(override_source["path"])
            if sha256(source_path) != override_source["sha256"]:
                raise ValueError(f"Override source hash mismatch: {source_path}")
            source_id = override_source["source_id"]
            if source_id in override_evidence_ids:
                continue
            override_evidence_ids.append(source_id)
            if company["rfo_panel_included"] == "yes" or company["npat_panel_included"] == "yes":
                override_evidence_ids_main.append(source_id)
            sources.append({
                "sourceId": source_id,
                "kind": "management_explanation",
                "label": f"{company['ticker']} FY2025 filing / MD&A",
                "detail": "Direct filing evidence for explicitly labelled RFO or NPAT override values",
                "path": override_source["path"],
                "sha256": override_source["sha256"],
                "role": "override value evidence",
                "url": None,
            })
        for index, (kind, label, relative_path) in enumerate(EVIDENCE[code], 1):
            source_path = vault_root / Path(relative_path)
            if not source_path.exists():
                raise FileNotFoundError(source_path)
            sources.append({"sourceId": f"{code}_E{index}", "kind": kind, "label": label, "detail": "Historical explanation or forward cross-check; see source role", "path": relative_path, "sha256": sha256(source_path), "role": "management explanation" if kind == "management" else "forward/credit context", "url": None})
        leader = row["leader_ticker"]
        sources.append({"sourceId": f"{code}_FACTSHEET", "kind": "fact_calculated", "label": f"SET Factsheet — {leader}", "detail": "Live leader cross-check", "path": None, "sha256": None, "role": "presentation-surface check", "url": f"https://www.set.or.th/th/market/product/stock/quote/{leader.lower()}/factsheet"})
        evidence_ids = [source["sourceId"] for source in sources if source["sourceId"].startswith(code + "_E")]
        claims = [
            {"section": "headline", "kind": "analyst_inference", "text": copy_row["headline"], "sourceIds": ["FY_PANEL"] + evidence_ids},
            {"section": "earnings_fact", "kind": "fact_calculated", "text": bi(f"FY2025 RFO {metrics['rfoYoYPct']:+.1f}%; owner NPAT state: {metrics['npatState'].replace('_', ' ')}.", f"FY2025 RFO {metrics['rfoYoYPct']:+.1f}%; สถานะ NPAT ส่วนผู้ถือหุ้น: {metrics['npatState']}"), "sourceIds": ["FY_PANEL"] + override_evidence_ids_main},
        ]
        for why_index, item in enumerate(copy_row["why"]):
            kind = WHY_CLAIM_KIND[code][why_index]
            if kind == "management_explanation":
                source_ids = evidence_ids or ["FY_PANEL"]
            elif kind == "fact_calculated":
                source_ids = ["FY_PANEL"]
            else:
                source_ids = ["FY_PANEL"] + evidence_ids
            if why_index in WHY_MARKET_INDEXES.get(code, set()):
                source_ids = list(dict.fromkeys(source_ids + ["SET_PUBLIC_EOD"]))
            if (code, why_index) in WHY_CLAIM_SOURCE_IDS:
                source_ids = WHY_CLAIM_SOURCE_IDS[(code, why_index)]
            if code == "F8" and why_index in (1, 2):
                source_ids = list(dict.fromkeys(source_ids + override_evidence_ids))
            claims.append({"section": "why", "kind": kind, "text": item, "sourceIds": source_ids})
        claims.append({"section": "causal_chain", "kind": "analyst_inference", "text": bi("Causal chain: " + " → ".join(item["en"] for item in copy_row["chain"]), "ห่วงโซ่เหตุ: " + " → ".join(item["th"] for item in copy_row["chain"])), "sourceIds": evidence_ids or ["FY_PANEL"]})
        claims.append({"section": "roles", "kind": "analyst_inference", "text": bi("Roles: " + "; ".join(f"{item['label']['en']} — {item['ticker']}" for item in copy_row["roles"]), "บทบาท: " + "; ".join(f"{item['label']['th']} — {item['ticker']}" for item in copy_row["roles"])), "sourceIds": ["FY_PANEL"] + evidence_ids})
        claims.append({"section": "valuation", "kind": "analyst_inference", "text": valuation_text(code, metrics, coverage), "sourceIds": ["SET_PUBLIC_EOD"] + evidence_ids})
        claims.extend({"section": "trigger", "kind": "analyst_test", "text": item, "sourceIds": evidence_ids or ["FY_PANEL"]} for item in copy_row["triggers"])
        claims.extend({"section": "risk", "kind": "analyst_test", "text": item, "sourceIds": evidence_ids or ["FY_PANEL"]} for item in copy_row["risks"])
        claims.append({"section": "must_prove", "kind": "analyst_test", "text": copy_row["must_prove"], "sourceIds": evidence_ids or ["FY_PANEL"]})
        segment_payload[code] = {
            "code": code, "name": {"en": legacy.SEGMENT_NAMES[code][0], "th": legacy.SEGMENT_NAMES[code][1]},
            "companyCount": int(row["universe_company_count"]), "marketCapMb": number(row["market_cap_mb"]),
            "marketCapSharePct": number(row["sector_market_cap_share_pct"]),
            "leader": {"ticker": leader, "sharePct": number(row["leader_share_of_known_market_cap_pct"])},
            "metrics": metrics, "coverage": coverage,
            "headline": copy_row["headline"], "why": copy_row["why"], "chain": copy_row["chain"],
            "roles": copy_row["roles"], "valuation": valuation_text(code, metrics, coverage),
            "triggers": copy_row["triggers"], "risks": copy_row["risks"], "status": STATUS[code],
            "mustProve": copy_row["must_prove"], "claims": claims,
            "alternativeFiscalView": ({"label": row["all_issuer_fiscal_label"], "companyCount": int(row["all_issuer_fiscal_company_count"]), "rfoYoYPct": number(row["all_issuer_rfo_yoy_pct"]), "npatYoYPct": number(row["all_issuer_npat_yoy_pct_positive_base_only"]), "netMarginPct": number(row["all_issuer_fy2025_net_margin_pct"])} if code == "F8" else None),
            "companies": [{"ticker": company["ticker"], "businessDescription": (company_reports.get(company["ticker"], {}).get("business") or None), "rfoFy2024Mb": number(company["fy2024_rfo_mb"]), "rfoFy2025Mb": number(company["fy2025_rfo_mb"]), "rfoChangeMb": number(company["rfo_change_mb"]), "npatOwnersFy2024Mb": number(company["fy2024_npat_owners_mb"]), "npatOwnersFy2025Mb": number(company["fy2025_npat_owners_mb"]), "npatChangeMb": number(company["npat_change_mb"]), "priceThb": number(company["price_thb"]), "marketCapMb": number(company["market_cap_mb"]), "marketCapSharePct": number(company["market_cap_share_pct"]), "pe": number(company["pe"]), "pbv": number(company["pbv"]), "dividendYieldPct": number(company["dividend_yield_pct"]), "ytdAdjustedReturnPct": number(company["ytd_adjusted_return_pct"]), "rfoYoYPct": number(company["rfo_yoy_pct"]), "npatYoYPct": number(company["npat_yoy_pct_positive_base_only"]), "npatState": company["npat_state"], "netMarginPct": number(company["fy2025_net_margin_pct"]), "rfoPanel": company["rfo_panel_included"] == "yes", "npatPanel": company["npat_panel_included"] == "yes", "marginPanel": company["margin_panel_included"] == "yes", "panelExclusionReason": company["panel_exclusion_reason"], "rfoOverrideSourceIds": company["rfo_override_source_ids"].split(";") if company["rfo_override_source_ids"] else [], "npatOverrideSourceIds": company["npat_override_source_ids"].split(";") if company["npat_override_source_ids"] else [], "marketCapAvailable": company["market_cap_available"] == "yes", "positivePeEligible": company["positive_pe_eligible"] == "yes", "performanceDrivers": company_driver_map[company["ticker"]]} for company in segment_companies],
            "sources": sources,
        }
        for company_payload in segment_payload[code]["companies"]:
            company_payload["businessDescription"] = business_description(company_payload["ticker"])


    sector_payload = {}
    for sector_row in sectors:
        sector = sector_row["sector"]
        selected = sorted([segment_payload[row["primary_segment_code"]] for row in segments if row["sector"] == sector], key=lambda item: -item["marketCapMb"])
        sector_payload[sector] = {
            "code": sector, "focusSegment": legacy.SECTOR_COPY[sector]["focus"], "title": legacy.SECTOR_COPY[sector]["title"],
            "thesis": legacy.SECTOR_COPY[sector]["thesis"], "takeaways": legacy.SECTOR_COPY[sector]["takeaways"],
            "metrics": {"marketCapMb": number(sector_row["market_cap_mb"]), "companyCount": int(sector_row["universe_company_count"]), "rfoFy2024Mb": number(sector_row["fy2024_rfo_mb"]), "rfoFy2025Mb": number(sector_row["fy2025_rfo_mb"]), "rfoYoYPct": number(sector_row["rfo_yoy_pct"]), "npatOwnersFy2024Mb": number(sector_row["fy2024_npat_owners_mb"]), "npatOwnersFy2025Mb": number(sector_row["fy2025_npat_owners_mb"]), "npatChangeMb": number(sector_row["npat_change_mb"]), "npatYoYPct": number(sector_row["npat_yoy_pct_positive_base_only"]), "npatState": sector_row["npat_state"], "netMarginFy2024Pct": number(sector_row["fy2024_net_margin_pct_comparable"]), "netMarginPct": number(sector_row["fy2025_net_margin_pct_comparable"]), "rfoDirectionDriver": sector_row["rfo_direction_driver"], "rfoDirectionDriverChangeMb": number(sector_row["rfo_direction_driver_change_mb"]), "npatDirectionDriver": sector_row["npat_direction_driver"], "npatDirectionDriverChangeMb": number(sector_row["npat_direction_driver_change_mb"]), "ytdAdjustedReturnPct": number(sector_row["ytd_adjusted_return_pct"]), "aggregatePositiveEarningsPe": number(sector_row["aggregate_positive_earnings_pe"])},
            "coverage": {"rfo": f"{sector_row['rfo_panel_company_count']}/{sector_row['universe_company_count']}", "npat": f"{sector_row['npat_panel_company_count']}/{sector_row['universe_company_count']}", "marketCap": f"{sector_row['known_market_cap_company_count']}/{sector_row['universe_company_count']}", "positivePe": f"{sector_row['positive_pe_company_count']}/{sector_row['universe_company_count']} · {number(sector_row['positive_pe_market_cap_coverage_pct']):.1f}% M-cap", "ytd": f"{sector_row['ytd_company_count']}/{sector_row['universe_company_count']} · {number(sector_row['ytd_market_cap_coverage_pct']):.1f}% M-cap"},
            "segments": selected,
        }

    return {
        "meta": {"schemaVersion": 4, "builtAt": datetime.now(timezone.utc).isoformat(timespec="seconds"), "effectiveMarketEod": effective_eod, "earningsPeriod": "FY2025 vs FY2024", "scope": "FOOD and PROP; audited primary-segment perimeter", "qaVerdict": qa["verdict"], "qaChecks": qa["counts"], "definitions": {"rfo": "Revenue from Operations (01 Sale); December-FYE comparable panel unless separately labelled", "rfoAmount": "FY2024/FY2025 audited RFO amount in THB million on the stated RFO panel", "npat": "Net profit attributable to owners of the parent; independent panel from RFO", "npatAmount": "FY2024/FY2025 owner NPAT amount in THB million on the stated NPAT panel", "margin": "NPAT / RFO only on the identical issuer intersection", "price": "Adjusted YTD price return; excludes cash dividends", "valuation": "Aggregate positive-earner P/E; identical numerator/denominator issuer set", "marketCap": "Point-in-time market capitalisation; official null remains null"}, "sourceLineage": ["Audited RFO workbook / filing overrides", "NPAT attributable to owners", "SET public Company Highlights", "SET Factsheet", "FY2025 MD&A with claim-level excerpts and hashes", "Broker/credit research as fallback/forward context"], "sourceFiles": [str(path.relative_to(theme_root)).replace("\\", "/") for path in (company_path, segment_path, sector_path, qa_path, provenance_path)], "warning": "Facts, management explanations, analyst inferences and analyst tests are explicitly separated. Price/valuation explanations are inference, not proof of causality. MD&A source exceptions are surfaced per company."},
        "sectors": sector_payload,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme-root", type=Path, required=True)
    parser.add_argument("--legacy-script", type=Path, required=True)
    parser.add_argument("--snapshot-dir", type=Path, required=True)
    parser.add_argument("--effective-eod", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    payload = build(args.theme_root, args.legacy_script, args.snapshot_dir, args.effective_eod)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"schema": payload["meta"]["schemaVersion"], "eod": payload["meta"]["effectiveMarketEod"], "segments": sum(len(sector["segments"]) for sector in payload["sectors"].values())}))


if __name__ == "__main__":
    main()
