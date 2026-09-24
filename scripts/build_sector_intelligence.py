#!/usr/bin/env python3
"""Build the static FOOD/PROP Sector Intelligence snapshot.

The quantitative layer is derived from the audited Sector Review CSV files.
Editorial copy is deliberately curated here so facts, forward expectations,
and analyst inference remain visibly separated in the web UI.

This script never reads credentials and never calls SET APIs. Refresh the
audited source pack first, then rebuild this public static snapshot.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path


SEGMENT_NAMES = {
    "F1": ("Integrated animal protein", "โปรตีนสัตว์ครบวงจร"),
    "F2": ("Seafood & aquaculture", "อาหารทะเลและเพาะเลี้ยง"),
    "F3": ("Pet food", "อาหารสัตว์เลี้ยง"),
    "F4": ("Branded beverages", "เครื่องดื่มแบรนด์"),
    "F5": ("Restaurants & food service", "ร้านอาหารและบริการอาหาร"),
    "F6": ("Snacks, bakery & staples", "อาหารหลัก ขนม และเบเกอรี่"),
    "F7": ("Ingredients & seasoning", "วัตถุดิบและเครื่องปรุง"),
    "F8": ("Sugar, starch & edible oils", "น้ำตาล แป้ง และน้ำมันบริโภค"),
    "F9": ("Processed agriculture & diversified", "เกษตรแปรรูปและธุรกิจหลากหลาย"),
    "P1": ("Residential for sale", "ที่อยู่อาศัยเพื่อขาย"),
    "P2": ("Industrial estates & logistics", "นิคมอุตสาหกรรมและโลจิสติกส์"),
    "P3": ("Retail & commercial recurring", "ศูนย์การค้าและรายได้ประจำ"),
    "P4": ("Hospitality & mixed use", "โรงแรมและมิกซ์ยูส"),
    "P5": ("Diversified / transition", "กระจายธุรกิจและปรับโครงสร้าง"),
}


def bi(en: str, th: str) -> dict[str, str]:
    return {"en": en, "th": th}


CONTENT = {
    "F1": {
        "headline": bi("Earnings-led recovery, still priced as a cycle", "กำไรฟื้นชัด แต่ตลาดยังให้ส่วนลดแบบหุ้นวัฏจักร"),
        "why": [
            bi("Livestock spreads and processing margins normalised from a weak base.", "ส่วนต่างราคาปศุสัตว์และ margin แปรรูปฟื้นจากฐานต่ำ"),
            bi("CPF supplied the largest profit delta; TFG and BTG broadened the recovery.", "CPF เป็นตัวเพิ่มกำไรหลัก ขณะที่ TFG และ BTG ทำให้การฟื้นตัวกระจายตัวขึ้น"),
            bi("RFO was nearly flat, so the earnings step-up was primarily margin-led.", "RFO เกือบทรงตัว จึงเป็นการฟื้นของกำไรจาก margin มากกว่ารายได้"),
        ],
        "chain": [bi("Livestock price", "ราคาสัตว์"), bi("Spread", "ส่วนต่าง"), bi("Margin", "Margin"), bi("NPAT", "NPAT"), bi("Valuation", "Valuation")],
        "roles": [{"label": bi("Leader", "ผู้นำ"), "ticker": "CPF"}, {"label": bi("Profit driver", "ตัวเพิ่มกำไร"), "ticker": "CPF"}, {"label": bi("Rising star", "ดาวรุ่ง"), "ticker": "TFG"}],
        "valuation": bi("A 7.9x P/E recognises the delivered recovery but retains a commodity-cycle discount for earnings volatility and reversal risk.", "P/E 7.9x สะท้อนว่าตลาดยอมรับการฟื้นของกำไรแล้ว แต่ยังหักส่วนลดวัฏจักรสินค้าโภคภัณฑ์จากความผันผวนและความเสี่ยงที่ spread จะกลับทิศ"),
        "triggers": [bi("Pork/chicken prices hold above feed-cost inflation", "ราคาหมูและไก่ยืนเหนือแรงกดดันต้นทุนอาหารสัตว์"), bi("Export demand and domestic consumption remain firm", "อุปสงค์ส่งออกและการบริโภคในประเทศยังแข็งแรง"), bi("Margin discipline persists into 6M26", "วินัยด้าน margin ต่อเนื่องถึง 6M26")],
        "risks": [bi("Livestock disease or oversupply", "โรคระบาดสัตว์หรืออุปทานล้นตลาด"), bi("Feed-cost reversal", "ต้นทุนอาหารสัตว์กลับมาสูงขึ้น"), bi("Export and FX volatility", "ความผันผวนด้านส่งออกและค่าเงิน")],
        "status": "delivered",
        "must_prove": bi("6M26 must show that margin recovery survives a less favourable commodity base.", "6M26 ต้องพิสูจน์ว่า margin ที่ฟื้นตัวอยู่ได้แม้ฐานวัฏจักรเอื้อประโยชน์น้อยลง"),
    },
    "F2": {
        "headline": bi("Price stabilised before earnings", "ราคาเริ่มทรงตัวก่อนที่กำไรจะฟื้น"),
        "why": [bi("TU drove both the revenue and profit contraction in the segment aggregate.", "TU เป็นตัวหลักของการลดลงทั้งรายได้และกำไรรวม"), bi("Export mix, tuna input costs and FX remain the core earnings variables.", "product mix ส่งออก ต้นทุนทูน่า และค่าเงินยังเป็นตัวแปรหลัก"), bi("Positive YTD breadth points to recovery expectations rather than delivered FY2025 growth.", "ราคาบวกในวงกว้างสะท้อนความคาดหวังการฟื้น มากกว่าผลประกอบการ FY2025 ที่เกิดขึ้นแล้ว")],
        "chain": [bi("Export volume", "ปริมาณส่งออก"), bi("Mix / FX", "Mix / ค่าเงิน"), bi("Gross margin", "Gross margin"), bi("NPAT", "NPAT"), bi("Re-rating", "Re-rating")],
        "roles": [{"label": bi("Leader", "ผู้นำ"), "ticker": "TU"}, {"label": bi("Direction driver", "ตัวกำหนดทิศทาง"), "ticker": "TU"}, {"label": bi("Comparator", "ตัวเทียบ"), "ticker": "CFRESH"}],
        "valuation": bi("The 10.9x P/E is below branded-growth segments; the modest price rise is an expectation of stabilisation, not confirmation of FY2025 earnings growth.", "P/E 10.9x ต่ำกว่ากลุ่มแบรนด์เติบโต การปรับขึ้นของราคาจึงเป็นการคาดหวังเสถียรภาพมากกว่าการยืนยันกำไร FY2025"),
        "triggers": [bi("Tuna and freight-cost relief", "ต้นทุนทูน่าและค่าระวางผ่อนคลาย"), bi("Export volume and branded mix improve", "ปริมาณส่งออกและสัดส่วนแบรนด์ดีขึ้น"), bi("FX becomes supportive", "ค่าเงินเอื้อต่อผู้ส่งออก")],
        "risks": [bi("Raw-material volatility", "วัตถุดิบผันผวน"), bi("Weak overseas demand", "อุปสงค์ต่างประเทศอ่อนตัว"), bi("Currency appreciation", "เงินบาทแข็งค่า")],
        "status": "expectation",
        "must_prove": bi("6M26 must convert stable sales into gross-margin and owner-profit recovery.", "6M26 ต้องเปลี่ยนยอดขายที่ทรงตัวให้เป็นการฟื้นของ gross margin และกำไรส่วนผู้ถือหุ้น"),
    },
    "F3": {
        "headline": bi("Structural growth, but profit conversion weakened", "รายได้เชิงโครงสร้างยังโต แต่การแปลงเป็นกำไรอ่อนลง"),
        "why": [bi("ITC delivered most of the RFO growth but also the largest profit decline.", "ITC สร้างการเติบโตของ RFO ส่วนใหญ่ แต่เป็นตัวฉุดกำไรมากที่สุด"), bi("Customer/product mix and utilisation explain the divergence between sales and profit.", "customer mix, product mix และ utilization อธิบายความต่างระหว่างยอดขายกับกำไร"), bi("Price performance is therefore forward-looking rather than FY2025-confirmed.", "ราคาที่ปรับขึ้นจึงเป็นมุมมองล่วงหน้า ไม่ใช่การยืนยันจากกำไร FY2025")],
        "chain": [bi("Orders", "คำสั่งซื้อ"), bi("Mix", "Product mix"), bi("Utilisation", "Utilization"), bi("Margin", "Margin"), bi("NPAT", "NPAT")],
        "roles": [{"label": bi("Leader", "ผู้นำ"), "ticker": "ITC"}, {"label": bi("Revenue driver", "ตัวเพิ่มรายได้"), "ticker": "ITC"}, {"label": bi("Comparator", "ตัวเทียบ"), "ticker": "AAI"}],
        "valuation": bi("A 15.5x P/E prices structural pet-food growth and high margins, but the FY2025 profit decline raises execution risk around mix and utilisation.", "P/E 15.5x สะท้อนการเติบโตเชิงโครงสร้างและ margin สูงของ pet food แต่กำไร FY2025 ที่ลดลงเพิ่ม execution risk ด้าน mix และ utilization"),
        "triggers": [bi("Premium-product mix improves", "สัดส่วนสินค้าพรีเมียมดีขึ้น"), bi("New capacity reaches efficient utilisation", "กำลังผลิตใหม่เข้าสู่ utilization ที่มีประสิทธิภาพ"), bi("Orders broaden across customers", "คำสั่งซื้อกระจายตัวในหลายลูกค้า")],
        "risks": [bi("Customer concentration", "การกระจุกตัวของลูกค้า"), bi("Ramp-up costs", "ต้นทุนช่วง ramp-up"), bi("FX and tuna inputs", "ค่าเงินและต้นทุนทูน่า")],
        "status": "expectation",
        "must_prove": bi("6M26 must show volume growth with margin recovery, not volume alone.", "6M26 ต้องเห็นทั้งปริมาณและ margin ฟื้น ไม่ใช่เพียงยอดขายเพิ่ม"),
    },
    "F4": {
        "headline": bi("Margin-led delivery supports the brand premium", "กำไรที่โตจาก margin ช่วยรองรับ premium ของแบรนด์"),
        "why": [bi("Revenue contracted, but NPAT rose as OSP supplied the main profit delta.", "รายได้ลดลงแต่ NPAT เพิ่ม โดย OSP เป็นตัวเพิ่มกำไรหลัก"), bi("Distribution, domestic mix and cost control mattered more than top-line growth.", "เครือข่ายจำหน่าย domestic mix และการคุมต้นทุนสำคัญกว่าการเติบโตของยอดขาย"), bi("CBG was the main positive price contributor, broadening the market signal.", "CBG เป็นตัวผลักราคาหลัก ทำให้สัญญาณตลาดไม่ได้พึ่งบริษัทเดียว")],
        "chain": [bi("Volume", "ปริมาณ"), bi("Brand / mix", "แบรนด์ / mix"), bi("Cost control", "คุมต้นทุน"), bi("Margin", "Margin"), bi("NPAT", "NPAT")],
        "roles": [{"label": bi("Leader", "ผู้นำ"), "ticker": "OSP"}, {"label": bi("Profit driver", "ตัวเพิ่มกำไร"), "ticker": "OSP"}, {"label": bi("Price driver", "ตัวผลักราคา"), "ticker": "CBG"}],
        "valuation": bi("The 17.1x P/E reflects brand, distribution and margin resilience. The premium is defensible only if volume stabilises after FY2025 revenue contraction.", "P/E 17.1x สะท้อนคุณค่าแบรนด์ ช่องทางจำหน่าย และความยืดหยุ่นของ margin แต่ premium จะยั่งยืนเมื่อ volume กลับมาทรงตัวหลังรายได้ FY2025 ลดลง"),
        "triggers": [bi("Domestic volume recovery", "ยอดขายในประเทศฟื้น"), bi("Favourable product mix", "product mix ดีขึ้น"), bi("Export/distribution execution", "การส่งออกและกระจายสินค้าทำได้ตามแผน")],
        "risks": [bi("Weak consumption", "กำลังซื้ออ่อน"), bi("Promotional intensity", "การแข่งขันด้านโปรโมชั่น"), bi("Packaging and sugar costs", "ต้นทุนบรรจุภัณฑ์และน้ำตาล")],
        "status": "delivered",
        "must_prove": bi("6M26 must add volume growth to the FY2025 margin recovery.", "6M26 ต้องเพิ่มการฟื้นของ volume ต่อจาก margin ที่ดีขึ้นใน FY2025"),
    },
    "F5": {
        "headline": bi("The highest multiple is paying for a turnaround, not current delivery", "Multiple สูงสุดกำลังจ่ายเพื่อ turnaround ไม่ใช่กำไรปัจจุบัน"),
        "why": [bi("RFO and NPAT both fell; M supplied the largest profit drag.", "RFO และ NPAT ลดลง โดย M เป็นตัวฉุดกำไรหลัก"), bi("Weak purchasing power and negative same-store sales pressured operating leverage.", "กำลังซื้อและ SSSG ที่อ่อนตัวกด operating leverage"), bi("The price recovery is expectation-led and remains uneven across companies.", "ราคาที่ฟื้นเป็น expectation-led และยังกระจายไม่สม่ำเสมอ")],
        "chain": [bi("Traffic", "Traffic"), bi("Ticket size", "Ticket size"), bi("SSSG", "SSSG"), bi("Store margin", "Store margin"), bi("NPAT", "NPAT")],
        "roles": [{"label": bi("Leader", "ผู้นำ"), "ticker": "M"}, {"label": bi("Profit drag", "ตัวฉุดกำไร"), "ticker": "M"}, {"label": bi("Growth contrast", "ตัวเปรียบเทียบการโต"), "ticker": "OKJ"}],
        "valuation": bi("At 23.6x, the segment carries FOOD's highest P/E despite falling earnings. The market is pricing recovery and strategic optionality; evidence must come from SSSG and margins.", "P/E 23.6x สูงสุดใน FOOD แม้กำไรลด ตลาดกำลังให้มูลค่ากับการฟื้นและ strategic optionality ซึ่งต้องพิสูจน์ด้วย SSSG และ margin"),
        "triggers": [bi("SSSG turns positive", "SSSG กลับมาเป็นบวก"), bi("Traffic improves without discount leakage", "traffic ดีขึ้นโดยไม่เสีย margin จากส่วนลด"), bi("Store productivity rises", "productivity ต่อสาขาดีขึ้น")],
        "risks": [bi("Persistent weak consumption", "กำลังซื้ออ่อนต่อเนื่อง"), bi("Promotion-driven margin pressure", "โปรโมชั่นกด margin"), bi("Expansion ahead of demand", "ขยายสาขาเร็วกว่าความต้องการ")],
        "status": "expectation",
        "must_prove": bi("6M26 must show positive SSSG and margin conversion, not just store growth.", "6M26 ต้องเห็น SSSG เป็นบวกและแปลงเป็น margin ไม่ใช่เพียงจำนวนสาขาเพิ่ม"),
    },
    "F6": {
        "headline": bi("Defensive scale held valuation, but earnings softened", "ขนาดและความ defensive ช่วยพยุง valuation แต่กำไรอ่อนลง"),
        "why": [bi("RFO was flat while NPAT declined, signalling margin compression.", "RFO ทรงตัวแต่ NPAT ลด สะท้อน margin compression"), bi("TFMAMA anchors half the segment and drove the largest profit decline.", "TFMAMA มีสัดส่วนประมาณครึ่งกลุ่มและเป็นตัวฉุดกำไรหลัก"), bi("NSL provided the clearest positive revenue delta.", "NSL เป็นตัวเพิ่มรายได้ที่ชัดที่สุด")],
        "chain": [bi("Domestic demand", "อุปสงค์ในประเทศ"), bi("Export", "ส่งออก"), bi("Input cost", "ต้นทุนวัตถุดิบ"), bi("Margin", "Margin"), bi("NPAT", "NPAT")],
        "roles": [{"label": bi("Leader", "ผู้นำ"), "ticker": "TFMAMA"}, {"label": bi("Revenue driver", "ตัวเพิ่มรายได้"), "ticker": "NSL"}, {"label": bi("Profit drag", "ตัวฉุดกำไร"), "ticker": "TFMAMA"}],
        "valuation": bi("The 15.5x P/E reflects defensive brands and cash flows, but flat RFO and lower profit cap the case for further premium expansion.", "P/E 15.5x สะท้อนแบรนด์ defensive และกระแสเงินสด แต่ RFO ที่ทรงตัวและกำไรลดจำกัดการขยาย premium"),
        "triggers": [bi("Export orders recover", "คำสั่งซื้อส่งออกฟื้น"), bi("Input-cost relief", "ต้นทุนวัตถุดิบผ่อนคลาย"), bi("New-product mix lifts revenue", "สินค้าใหม่ช่วยเพิ่มรายได้")],
        "risks": [bi("Mature domestic categories", "ตลาดในประเทศโตต่ำ"), bi("Commodity inflation", "วัตถุดิบแพงขึ้น"), bi("Export softness", "ส่งออกอ่อนตัว")],
        "status": "pressure",
        "must_prove": bi("6M26 must restore profit growth while preserving defensive cash generation.", "6M26 ต้องกลับมาโตด้านกำไรโดยยังรักษากระแสเงินสดแบบ defensive"),
    },
    "F7": {
        "headline": bi("Strong price momentum outran near-flat earnings", "ราคาปรับเด่นกว่าพื้นฐานที่เกือบทรงตัว"),
        "why": [bi("RFO and NPAT were nearly flat for the segment.", "RFO และ NPAT ของกลุ่มเกือบทรงตัว"), bi("RBF drove the negative direction in both revenue and profit.", "RBF เป็นตัวกำหนดทิศทางลบทั้งรายได้และกำไร"), bi("SAUCE's leadership and quality profile supported a premium market view.", "ความเป็นผู้นำและคุณภาพของ SAUCE ช่วยรองรับมุมมอง premium")],
        "chain": [bi("Volume", "ปริมาณ"), bi("Export / OEM", "ส่งออก / OEM"), bi("Mix", "Mix"), bi("Cash margin", "Cash margin"), bi("Premium", "Premium")],
        "roles": [{"label": bi("Leader", "ผู้นำ"), "ticker": "SAUCE"}, {"label": bi("Direction driver", "ตัวกำหนดทิศทาง"), "ticker": "RBF"}, {"label": bi("Quality anchor", "ตัวแทนคุณภาพ"), "ticker": "SAUCE"}],
        "valuation": bi("The 19.1x P/E and strongest FOOD YTD return imply a quality/optionality premium. FY2025 did not yet deliver enough growth to fully validate the re-rating.", "P/E 19.1x และ YTD สูงสุดใน FOOD สะท้อน quality/optionality premium แต่ FY2025 ยังโตไม่มากพอที่จะยืนยัน re-rating ทั้งหมด"),
        "triggers": [bi("OEM/export orders accelerate", "คำสั่งซื้อ OEM และส่งออกเร่งตัว"), bi("Higher-value mix improves", "สัดส่วนสินค้ามูลค่าสูงดีขึ้น"), bi("Margin recovers at RBF", "margin ของ RBF ฟื้น")],
        "risks": [bi("Premium without earnings follow-through", "premium สูงแต่กำไรไม่ตาม"), bi("Customer concentration", "ลูกค้ากระจุกตัว"), bi("Input and FX volatility", "ต้นทุนและค่าเงินผันผวน")],
        "status": "expectation",
        "must_prove": bi("6M26 must turn price momentum into broad-based revenue and profit growth.", "6M26 ต้องเปลี่ยน price momentum ให้เป็นการโตของรายได้และกำไรในวงกว้าง"),
    },
    "F8": {
        "headline": bi("Commodity expectations lifted prices while FY2025 earnings fell", "คาดการณ์วัฏจักรหนุนราคา แม้กำไร FY2025 ลด"),
        "why": [bi("TVO drove the largest revenue decline and BRR the largest profit decline.", "TVO เป็นตัวฉุดรายได้หลัก และ BRR เป็นตัวฉุดกำไรหลัก"), bi("The YTD rise reflects commodity-cycle expectations rather than delivered FY2025 improvement.", "ราคา YTD ที่เพิ่มสะท้อนความคาดหวังวัฏจักร มากกว่าผล FY2025 ที่ดีขึ้น"), bi("Wide business diversity makes company-level drivers essential.", "โครงสร้างธุรกิจต่างกันมาก จึงต้องอ่าน driver รายบริษัท")],
        "chain": [bi("Commodity price", "ราคาสินค้าโภคภัณฑ์"), bi("Crush / refining spread", "ส่วนต่างผลิต"), bi("Inventory", "สินค้าคงคลัง"), bi("Margin", "Margin"), bi("NPAT", "NPAT")],
        "roles": [{"label": bi("Leader", "ผู้นำ"), "ticker": "TVO"}, {"label": bi("Revenue drag", "ตัวฉุดรายได้"), "ticker": "TVO"}, {"label": bi("Profit drag", "ตัวฉุดกำไร"), "ticker": "BRR"}],
        "valuation": bi("A 9.5x P/E embeds a cyclical discount. Price gains require confirmation from spreads, inventory gains and the next crop cycle.", "P/E 9.5x มีส่วนลดเชิงวัฏจักร ราคาที่เพิ่มต้องยืนยันด้วย spread กำไรสต็อก และผลผลิตฤดูกาลถัดไป"),
        "triggers": [bi("Favourable crop and commodity prices", "ราคาพืชผลและสินค้าโภคภัณฑ์เอื้อ"), bi("Crush/refining spreads widen", "ส่วนต่างผลิตกว้างขึ้น"), bi("Inventory gains materialise", "เกิดกำไรสต็อก")],
        "risks": [bi("Commodity reversal", "ราคาสินค้าโภคภัณฑ์กลับทิศ"), bi("Policy intervention", "นโยบายแทรกแซง"), bi("Weather and crop volatility", "สภาพอากาศและผลผลิตผันผวน")],
        "status": "expectation",
        "must_prove": bi("6M26 must validate the price move with realised spreads and cash earnings.", "6M26 ต้องยืนยันราคาที่ขึ้นด้วย spread ที่เกิดจริงและ cash earnings"),
    },
    "F9": {
        "headline": bi("Loss-making aggregate keeps the segment under pressure", "ภาพรวมขาดทุนทำให้กลุ่มยังถูกกดดัน"),
        "why": [bi("RFO contracted sharply and the aggregate turned to a loss.", "RFO ลดแรงและกำไรรวมพลิกเป็นขาดทุน"), bi("Company dispersion is high; one aggregate P/E cannot represent the full segment.", "ผลประกอบการรายบริษัทแตกต่างสูง P/E รวมจึงไม่แทนทั้งกลุ่ม"), bi("SUN is the largest issuer but accounts for only about one-fifth of segment market cap.", "SUN เป็นบริษัทใหญ่สุดแต่มีสัดส่วนเพียงประมาณหนึ่งในห้าของ market cap กลุ่ม")],
        "chain": [bi("Crop / order", "ผลผลิต / คำสั่งซื้อ"), bi("Utilisation", "Utilization"), bi("Unit cost", "ต้นทุนต่อหน่วย"), bi("Cash flow", "Cash flow"), bi("Solvency", "ฐานะการเงิน")],
        "roles": [{"label": bi("Leader", "ผู้นำ"), "ticker": "SUN"}, {"label": bi("Loss driver", "ตัวฉุดขาดทุน"), "ticker": "APURE"}, {"label": bi("Watch", "เฝ้าระวัง"), "ticker": "SST"}],
        "valuation": bi("The displayed 12.8x P/E uses only positive-earnings constituents and is not representative of a segment that turned to a loss.", "P/E 12.8x คำนวณจากเฉพาะบริษัทที่มีกำไร จึงไม่เป็นตัวแทนของกลุ่มที่กำไรรวมพลิกเป็นขาดทุน"),
        "triggers": [bi("Order recovery", "คำสั่งซื้อฟื้น"), bi("Utilisation improves", "utilization ดีขึ้น"), bi("Loss-making units are restructured", "ปรับโครงสร้างหน่วยธุรกิจขาดทุน")],
        "risks": [bi("Persistent operating losses", "ขาดทุนดำเนินงานต่อเนื่อง"), bi("Working-capital stress", "เงินทุนหมุนเวียนตึงตัว"), bi("Low liquidity and event risk", "สภาพคล่องหุ้นต่ำและ event risk")],
        "status": "pressure",
        "must_prove": bi("6M26 must show loss reduction and cash-flow normalisation before valuation is meaningful.", "6M26 ต้องเห็นขาดทุนลดและ cash flow กลับปกติก่อนที่ valuation จะตีความได้")
    },
    "P1": {
        "headline": bi("Low valuation reflects structural demand and cash-conversion pressure", "Valuation ต่ำสะท้อนแรงกดดันเชิงโครงสร้างต่ออุปสงค์และ cash conversion"),
        "why": [bi("RFO and NPAT contracted broadly across the residential panel.", "RFO และ NPAT ลดลงในวงกว้าง"), bi("Affordability, mortgage rejection and margin pressure slowed transfers.", "ความสามารถซื้อ อัตราปฏิเสธสินเชื่อ และ margin ที่ลดกดการโอน"), bi("Dividend yield supports selected names but does not remove earnings risk.", "dividend yield ช่วยพยุงบางบริษัท แต่ไม่ลบความเสี่ยงกำไร")],
        "chain": [bi("Demand", "อุปสงค์"), bi("Mortgage approval", "อนุมัติสินเชื่อ"), bi("Transfer", "โอน"), bi("Margin", "Margin"), bi("Cash", "Cash")],
        "roles": [{"label": bi("Leader", "ผู้นำ"), "ticker": "LH"}, {"label": bi("Revenue drag", "ตัวฉุดรายได้"), "ticker": "SPALI"}, {"label": bi("Relative gainer", "ตัวเด่นเชิงราคา"), "ticker": "AP"}],
        "valuation": bi("The 8.0x P/E and high yield compensate for weak presales-to-transfer conversion, inventory and affordability risk.", "P/E 8.0x และ yield สูงชดเชยความเสี่ยงจาก presales ที่แปลงเป็นโอนได้ช้า inventory และกำลังซื้อ"),
        "triggers": [bi("Mortgage rejection eases", "อัตราปฏิเสธสินเชื่อลด"), bi("Transfers and backlog conversion improve", "การโอนและแปลง backlog ดีขึ้น"), bi("Inventory and leverage decline", "inventory และ leverage ลด")],
        "risks": [bi("Prolonged weak affordability", "กำลังซื้ออ่อนยาว"), bi("Discounting compresses margin", "ส่วนลดกด margin"), bi("Inventory/cash-cycle deterioration", "inventory และ cash cycle แย่ลง")],
        "status": "pressure",
        "must_prove": bi("6M26 must show transfer, margin and operating cash flow moving together.", "6M26 ต้องเห็นการโอน margin และ operating cash flow ดีขึ้นพร้อมกัน"),
    },
    "P2": {
        "headline": bi("Expectation-led re-rating on FDI optionality", "ราคา re-rate จาก FDI optionality ก่อนกำไรเกิดจริง"),
        "why": [bi("FY2025 RFO and NPAT fell, creating a clear earnings-price mismatch.", "RFO และ NPAT FY2025 ลดลง สวนทางกับราคาที่เพิ่มชัดเจน"), bi("The market is paying for FDI relocation, data centres and future land transfers.", "ตลาดให้มูลค่ากับ FDI relocation, data center และการโอนที่ดินในอนาคต"), bi("The proof chain remains presales to transfers to utilities and rent.", "สิ่งที่ต้องพิสูจน์คือ presales แปลงเป็น transfer แล้วต่อยอด utility และค่าเช่า")],
        "chain": [bi("BOI / FDI", "BOI / FDI"), bi("Land presales", "ยอดขายที่ดิน"), bi("Transfers", "โอน"), bi("Utility / rent", "Utility / ค่าเช่า"), bi("NPAT", "NPAT")],
        "roles": [{"label": bi("Leader", "ผู้นำ"), "ticker": "WHA"}, {"label": bi("FDI bellwether", "ตัวแทน FDI"), "ticker": "AMATA"}, {"label": bi("Earnings swing", "ตัวแปรกำไร"), "ticker": "ROJNA"}],
        "valuation": bi("The 10.6x P/E looks moderate, but the +48.9% YTD move is forward expectation. Valuation needs signed land sales, transfer timing and recurring utility evidence.", "P/E 10.6x ดูไม่สูง แต่ราคา YTD +48.9% เป็นความคาดหวังล่วงหน้า จึงต้องยืนยันด้วยยอดขายที่ดิน การโอน และรายได้ utility ที่เกิดจริง"),
        "triggers": [bi("Signed land sales and transfers", "ยอดขายที่ดินและการโอนเกิดจริง"), bi("Data-centre power readiness", "ความพร้อมด้านไฟฟ้าสำหรับ data center"), bi("Utility volume rises", "ปริมาณ utility เพิ่ม")],
        "risks": [bi("FDI conversion lag", "FDI แปลงเป็นการลงทุนจริงล่าช้า"), bi("Transfer and infrastructure delays", "โอนและโครงสร้างพื้นฐานล่าช้า"), bi("Land, power and regulatory constraints", "ข้อจำกัดที่ดิน ไฟฟ้า และกฎระเบียบ")],
        "status": "expectation",
        "must_prove": bi("6M26 must convert policy and presales headlines into transfers, utilities and cash earnings.", "6M26 ต้องเปลี่ยนข่าวนโยบายและ presales ให้เป็นการโอน utility และ cash earnings"),
    },
    "P3": {
        "headline": bi("Recurring income delivered the cleanest earnings-price alignment", "Recurring income ให้ภาพกำไรและราคาที่สอดคล้องชัดที่สุด"),
        "why": [bi("P3 was the only PROP segment with positive RFO and NPAT growth.", "P3 เป็น segment เดียวใน PROP ที่ RFO และ NPAT เติบโต"), bi("CPN supplied most of the profit increase and anchors 85% of market cap.", "CPN เป็นตัวเพิ่มกำไรหลักและมีสัดส่วน 85% ของ market cap"), bi("Occupancy, traffic and rental economics provide observable recurring proof.", "occupancy, traffic และค่าเช่าเป็นหลักฐาน recurring ที่ติดตามได้")],
        "chain": [bi("Traffic", "Traffic"), bi("Occupancy", "Occupancy"), bi("Rent / NOI", "ค่าเช่า / NOI"), bi("Cash flow", "Cash flow"), bi("Premium", "Premium")],
        "roles": [{"label": bi("Leader", "ผู้นำ"), "ticker": "CPN"}, {"label": bi("Profit driver", "ตัวเพิ่มกำไร"), "ticker": "CPN"}, {"label": bi("Diversified comparator", "ตัวเทียบ"), "ticker": "MBK"}],
        "valuation": bi("The 14.6x P/E premium is supported by recurring NOI, high margins and CPN's dominant asset quality; concentration remains the key caveat.", "P/E 14.6x ได้รับการรองรับจาก recurring NOI, margin สูง และคุณภาพสินทรัพย์ของ CPN แต่ต้องระวังการกระจุกตัวสูง") ,
        "triggers": [bi("Traffic and occupancy improve", "traffic และ occupancy ดีขึ้น"), bi("Rental reversion remains positive", "rental reversion ยังเป็นบวก"), bi("New projects ramp without margin dilution", "โครงการใหม่ ramp-up โดยไม่ลด margin")],
        "risks": [bi("Consumption slowdown", "การบริโภคชะลอ"), bi("High segment concentration", "กลุ่มกระจุกตัวใน CPN สูง"), bi("Project capex and ramp-up risk", "ความเสี่ยง capex และ ramp-up")],
        "status": "delivered",
        "must_prove": bi("6M26 must sustain NOI and cash conversion as new projects scale.", "6M26 ต้องรักษา NOI และ cash conversion ระหว่างขยายโครงการใหม่"),
    },
    "P4": {
        "headline": bi("Tourism and asset optionality led prices ahead of FY2025 profit", "ท่องเที่ยวและ asset optionality ดันราคานำกำไร FY2025"),
        "why": [bi("RFO and NPAT declined despite a strong YTD market move.", "RFO และ NPAT ลดลงแม้ราคาปรับขึ้นมาก"), bi("AWC dominates market cap, so its occupancy, ADR and project ramp set the segment view.", "AWC ครอง market cap กลุ่ม จึงต้องติดตาม occupancy, ADR และ ramp-up ของโครงการ"), bi("The market is discounting tourism normalisation and future asset productivity.", "ตลาดกำลัง discount การฟื้นท่องเที่ยวและ productivity สินทรัพย์ในอนาคต")],
        "chain": [bi("Arrivals", "นักท่องเที่ยว"), bi("Occupancy / ADR", "Occupancy / ADR"), bi("Asset ramp", "Asset ramp"), bi("EBITDA", "EBITDA"), bi("NPAT", "NPAT")],
        "roles": [{"label": bi("Leader", "ผู้นำ"), "ticker": "AWC"}, {"label": bi("Direction driver", "ตัวกำหนดทิศทาง"), "ticker": "AWC"}, {"label": bi("Profit drag", "ตัวฉุดกำไร"), "ticker": "S"}],
        "valuation": bi("A 14.9x P/E and +38.4% YTD move reflect tourism and asset-ramp expectations. FY2025 earnings did not yet confirm that optimism.", "P/E 14.9x และ YTD +38.4% สะท้อนความคาดหวังท่องเที่ยวและ asset ramp แต่กำไร FY2025 ยังไม่ยืนยันเต็มที่"),
        "triggers": [bi("Occupancy and ADR rise", "occupancy และ ADR เพิ่ม"), bi("New assets ramp on schedule", "สินทรัพย์ใหม่ ramp-up ตามแผน"), bi("Tourist arrivals broaden", "นักท่องเที่ยวฟื้นหลายตลาด")],
        "risks": [bi("Tourism shock", "ความเสี่ยงท่องเที่ยว"), bi("High fixed cost and leverage", "ต้นทุนคงที่และ leverage สูง"), bi("Slow asset ramp-up", "asset ramp-up ล่าช้า")],
        "status": "expectation",
        "must_prove": bi("6M26 must translate occupancy and ADR into owner-profit and cash flow.", "6M26 ต้องแปลง occupancy และ ADR เป็นกำไรส่วนผู้ถือหุ้นและ cash flow"),
    },
    "P5": {
        "headline": bi("Event-driven prices are not a substitute for operating proof", "ราคาที่ขับเคลื่อนด้วย event ไม่ทดแทนหลักฐานการดำเนินงาน"),
        "why": [bi("RFO contracted sharply and the segment turned to a loss.", "RFO ลดลงแรงและกลุ่มพลิกเป็นขาดทุน"), bi("Price moves are dominated by restructuring and holding-company events.", "ราคาเคลื่อนไหวจากการปรับโครงสร้างและ event ของ holding company"), bi("A positive-earnings P/E excludes loss-makers and is not representative.", "P/E จากบริษัทที่มีกำไรไม่เป็นตัวแทนของกลุ่มทั้งหมด")],
        "chain": [bi("Restructuring", "ปรับโครงสร้าง"), bi("Asset sale", "ขายสินทรัพย์"), bi("Debt / liquidity", "หนี้ / สภาพคล่อง"), bi("Core earnings", "กำไรหลัก"), bi("Re-rating", "Re-rating")],
        "roles": [{"label": bi("Market-cap leader", "ผู้นำ market cap"), "ticker": "STELLA"}, {"label": bi("Operating swing", "ตัวแปรดำเนินงาน"), "ticker": "PSH"}, {"label": bi("Event comparator", "ตัวเทียบ event"), "ticker": "UV"}],
        "valuation": bi("The 8.3x P/E is calculated only from profitable constituents. With aggregate losses, balance-sheet and event evidence are more decision-useful than the headline multiple.", "P/E 8.3x คำนวณจากเฉพาะบริษัทที่มีกำไร เมื่อกำไรรวมติดลบ ฐานะการเงินและหลักฐานของ event มีประโยชน์กว่าค่า multiple headline"),
        "triggers": [bi("Restructuring closes with cash proceeds", "ปรับโครงสร้างเสร็จและได้เงินสดจริง"), bi("Debt and liquidity improve", "หนี้และสภาพคล่องดีขึ้น"), bi("Core operations return to profit", "ธุรกิจหลักกลับมามีกำไร")],
        "risks": [bi("One-off gains obscure core losses", "กำไรพิเศษบดบังขาดทุนหลัก"), bi("Leverage and refinancing", "leverage และ refinancing"), bi("Governance and execution risk", "ธรรมาภิบาลและ execution risk")],
        "status": "event",
        "must_prove": bi("6M26 must separate recurring earnings from one-offs and show balance-sheet improvement.", "6M26 ต้องแยกกำไรประจำออกจาก one-off และแสดงฐานะการเงินที่ดีขึ้น"),
    },
}


EVIDENCE = {
    "F1": ["MDA_CPF_2025FY_E.md", "KS_CPF_346557", "YUANTA_CPF_346571", "KSS_TFG_345421", "YUANTA_BTG_347822"],
    "F2": ["MDA_TU_2025FY_E.md", "BLS_TU_348878", "BYD_TU_348932", "MST_TU_346135"],
    "F3": ["MDA_ITC_2025FY_E.md", "BLS_ITC_348446", "MST_ITC_346337", "MDA_AAI_2025FY_E.md"],
    "F4": ["MDA_OSP_2025FY_E.md", "KS_OSP_347156", "YUANTA_OSP_347068", "BLS_CBG_345849"],
    "F5": ["MDA_M_2025FY_E.md", "KSS_M_348366", "research_35576_1_20260529-OKJ_U_EN"],
    "F6": ["MDA_TFMAMA_2025FY_E.md", "MDA_NSL_2025FY_E.md", "MDA_PRG_2025FY_E.md"],
    "F7": ["MDA_SAUCE_2025FY_E.md", "Top-Pick-240769---SAUCE", "FSSIA_RBF_347820"],
    "F8": ["MDA_TVO_2025FY_E.md", "KSS_TVO_341634", "KSL149-e"],
    "F9": ["MDA_SUN_2025FY_E.md", "MDA_APURE_2025FY_E.md", "MDA_SST_2025FY_E.md"],
    "P1": ["MDA_LH_2025FY_E.md", "INVX_LH_343581", "KSS_LH_339494", "KSS_SPALI_348498", "INVX_AP_348384"],
    "P2": ["MDA_WHA_2025FY_E.md", "MST_WHA_348118", "YUANTA_WHA_347866", "BLS_AMATA_347904", "ER_ROJNA_251118"],
    "P3": ["MDA_CPN_2025FY_E.md", "BLS_CPN_344659", "KSS_CPN_340982", "MBK180-e"],
    "P4": ["MDA_AWC_2025FY_E.md", "BLS_AWC_347910", "KGI_AWC_348756"],
    "P5": ["MDA_STELLA_2025FY_E.md", "MDA_PSH_2025FY_E.md", "MDA_UV_2025FY_E.md"],
}


SECTOR_COPY = {
    "FOOD": {
        "focus": "F1",
        "title": bi("FOOD: profit recovered, but concentrated in animal protein", "FOOD: กำไรฟื้น แต่กระจุกในโปรตีนสัตว์"),
        "thesis": bi("Animal protein and beverages delivered profit growth; several other segments saw prices rise ahead of FY2025 earnings.", "โปรตีนสัตว์และเครื่องดื่มส่งมอบกำไรที่ดีขึ้น ขณะที่หลายกลุ่มราคาปรับขึ้นนำผลประกอบการ FY2025"),
        "takeaways": [bi("F1 is the largest segment and the clearest earnings-led recovery.", "F1 ใหญ่ที่สุดและเป็นการฟื้นที่กำไรยืนยันชัดที่สุด"), bi("F7, F5, F3 and F8 require forward expectations to justify market pricing.", "F7, F5, F3 และ F8 ต้องใช้ความคาดหวังล่วงหน้าอธิบายราคา"), bi("F9 remains a loss-making outlier where headline P/E is not representative.", "F9 ยังเป็น outlier ที่ขาดทุนและ P/E headline ไม่เป็นตัวแทน")],
    },
    "PROP": {
        "focus": "P2",
        "title": bi("PROP: recurring income delivered; FDI optionality drove expectations", "PROP: รายได้ประจำส่งมอบกำไร ขณะที่ FDI optionality ขับเคลื่อนความคาดหวัง"),
        "thesis": bi("P3 showed the cleanest earnings-price alignment. P2 and P4 rallied ahead of FY2025 earnings, while residential remained structurally constrained.", "P3 มีความสอดคล้องระหว่างกำไรกับราคาชัดที่สุด ส่วน P2 และ P4 ราคาวิ่งนำกำไร ขณะที่ที่อยู่อาศัยยังถูกกดดันเชิงโครงสร้าง"),
        "takeaways": [bi("P3 is the largest segment and the only one with both RFO and NPAT growth.", "P3 ใหญ่ที่สุดและเป็นกลุ่มเดียวที่ทั้ง RFO และ NPAT เติบโต"), bi("P2 is the most important expectation-led mismatch to monitor into 6M26.", "P2 เป็น mismatch แบบ expectation-led ที่สำคัญที่สุดสำหรับ 6M26"), bi("P1's low P/E reflects affordability, transfer and cash-conversion risk.", "P/E ต่ำของ P1 สะท้อนความเสี่ยงกำลังซื้อ การโอน และ cash conversion")],
    },
}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def number(value):
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def aggregate_pe(rows: list[dict], mcap_key: str, pe_key: str) -> float | None:
    earnings = 0.0
    market_cap = 0.0
    for row in rows:
        mcap = number(row.get(mcap_key))
        pe = number(row.get(pe_key))
        if mcap is not None and pe is not None and pe > 0:
            market_cap += mcap
            earnings += mcap / pe
    return market_cap / earnings if earnings else None


def weighted_return(rows: list[dict]) -> float | None:
    numerator = 0.0
    denominator = 0.0
    for row in rows:
        weight = number(row.get("ytd_base_market_cap_mb"))
        ret = number(row.get("ytd_return_pct"))
        if weight is not None and ret is not None:
            numerator += weight * ret
            denominator += weight
    return numerator / denominator if denominator else None


def fact_source(label: str, detail: str, url: str | None = None) -> dict:
    return {"kind": "fact", "label": label, "detail": detail, "url": url}


def build(theme_root: Path) -> dict:
    current_dir = theme_root / "data" / "official-2026-08-07-v2"
    fy_dir = theme_root / "data" / "official-2026-08-06"
    current_segments = read_rows(current_dir / "food_prop_segment_official_2026-08-06.csv")
    current_companies = read_rows(current_dir / "food_prop_company_official_2026-08-06.csv")
    fy_segments = read_rows(fy_dir / "food_prop_segment_fy2024_2025_three_lens_2026-08-06.csv")
    fy_companies = read_rows(fy_dir / "food_prop_company_fy2024_2025_selection_base_2026-08-06.csv")

    seg_current = {(r["sector"], r["primary_segment_code"]): r for r in current_segments}
    seg_fy = {(r["sector"], r["primary_segment_code"]): r for r in fy_segments}
    company_fy = {(r["sector"], r["ticker"]): r for r in fy_companies}

    sectors = {}
    for sector in ("FOOD", "PROP"):
        sector_rows = [r for r in current_segments if r["sector"] == sector]
        sector_companies = [r for r in current_companies if r["sector"] == sector]
        total_mcap = sum(number(r["market_cap_mb"]) or 0 for r in sector_rows)
        fy24_rfo = sum(number(seg_fy[(sector, r["primary_segment_code"])]["fy2024_revenue_from_operations_mb"]) or 0 for r in sector_rows)
        fy25_rfo = sum(number(seg_fy[(sector, r["primary_segment_code"])]["fy2025_revenue_from_operations_mb"]) or 0 for r in sector_rows)
        fy24_np = sum(number(seg_fy[(sector, r["primary_segment_code"])]["fy2024_net_profit_mb"]) or 0 for r in sector_rows)
        fy25_np = sum(number(seg_fy[(sector, r["primary_segment_code"])]["fy2025_net_profit_mb"]) or 0 for r in sector_rows)
        segments = []
        for current in sorted(sector_rows, key=lambda r: number(r["market_cap_mb"]) or 0, reverse=True):
            code = current["primary_segment_code"]
            fy = seg_fy[(sector, code)]
            copy = CONTENT[code]
            segment_companies = []
            for company in sorted(
                [r for r in sector_companies if r["primary_segment_code"] == code],
                key=lambda r: number(r["market_cap_mb"]) or 0,
                reverse=True,
            ):
                frow = company_fy.get((sector, company["ticker"]), {})
                segment_companies.append({
                    "ticker": company["ticker"],
                    "priceThb": number(company.get("price_thb")),
                    "marketCapMb": number(company.get("market_cap_mb")),
                    "marketCapSharePct": (number(company.get("market_cap_mb")) or 0) / (number(current["market_cap_mb"]) or 1) * 100,
                    "pe": number(company.get("pe")),
                    "pbv": number(company.get("pbv")),
                    "dividendYieldPct": number(company.get("dividend_yield_pct")),
                    "ytdAdjustedReturnPct": number(company.get("ytd_return_pct")),
                    "rfoYoYPct": number(frow.get("fy2025_revenue_from_operations_yoy_pct")),
                    "npatYoYPct": number(frow.get("fy2025_net_profit_yoy_pct_positive_base_only")),
                    "npatState": frow.get("fy2025_net_profit_state") or None,
                    "netMarginPct": number(frow.get("fy2025_net_margin_on_operating_revenue_pct")),
                })
            leader_token = (current.get("top3") or "").split(";")[0].strip().split(" ")
            leader = leader_token[0] if leader_token else None
            leader_share = None
            if len(leader_token) > 1:
                leader_share = number(leader_token[1].replace("%", ""))
            factsheet_url = f"https://www.set.or.th/th/market/product/stock/quote/{leader.lower()}/factsheet" if leader else None
            sources = [
                fact_source("SETSMART Company Fundamental API", "Market and FY financial fields; effective EOD 2026-08-06"),
                fact_source(f"SET Factsheet — {leader}", "Leader and market-data cross-check", factsheet_url),
            ]
            sources += [
                {"kind": "management" if item.startswith("MDA_") else "forward", "label": item, "detail": "FY2025 management evidence" if item.startswith("MDA_") else "Broker view; forward cross-check, not proof of price causality", "url": None}
                for item in EVIDENCE[code]
            ]
            segments.append({
                "code": code,
                "name": {"en": SEGMENT_NAMES[code][0], "th": SEGMENT_NAMES[code][1]},
                "companyCount": int(float(current["company_count"])),
                "marketCapMb": number(current["market_cap_mb"]),
                "marketCapSharePct": (number(current["market_cap_mb"]) or 0) / total_mcap * 100 if total_mcap else None,
                "leader": {"ticker": leader, "sharePct": leader_share},
                "metrics": {
                    "rfoYoYPct": number(fy["fy2025_revenue_from_operations_yoy_pct"]),
                    "npatYoYPct": number(fy["fy2025_net_profit_yoy_pct_positive_base_only"]),
                    "npatState": fy["fy2025_net_profit_state"],
                    "netMarginPct": number(fy["fy2025_net_margin_on_operating_revenue_pct"]),
                    "ytdAdjustedReturnPct": number(current["ytd_start_mcap_weighted_return_pct"]),
                    "ytdPositiveBreadthPct": number(current["ytd_positive_breadth_pct"]),
                    "aggregatePositiveEarningsPe": number(current["aggregate_positive_earnings_pe"]),
                    "aggregatePbv": number(current["aggregate_pbv"]),
                    "dividendYieldPct": number(current["weighted_dividend_yield_pct"]),
                },
                "headline": copy["headline"],
                "why": copy["why"],
                "chain": copy["chain"],
                "roles": copy["roles"],
                "valuation": copy["valuation"],
                "triggers": copy["triggers"],
                "risks": copy["risks"],
                "status": copy["status"],
                "mustProve": copy["must_prove"],
                "companies": segment_companies,
                "sources": sources,
            })

        sectors[sector] = {
            "code": sector,
            "focusSegment": SECTOR_COPY[sector]["focus"],
            "title": SECTOR_COPY[sector]["title"],
            "thesis": SECTOR_COPY[sector]["thesis"],
            "takeaways": SECTOR_COPY[sector]["takeaways"],
            "metrics": {
                "marketCapMb": total_mcap,
                "companyCount": len(sector_companies),
                "rfoYoYPct": ((fy25_rfo / fy24_rfo) - 1) * 100 if fy24_rfo else None,
                "npatYoYPct": ((fy25_np / fy24_np) - 1) * 100 if fy24_np > 0 else None,
                "ytdAdjustedReturnPct": weighted_return(sector_companies),
                "aggregatePositiveEarningsPe": aggregate_pe(sector_companies, "market_cap_mb", "pe"),
            },
            "segments": segments,
        }

    return {
        "meta": {
            "schemaVersion": 1,
            "builtAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "effectiveMarketEod": "2026-08-06",
            "earningsPeriod": "FY2025 vs FY2024",
            "scope": "FOOD and PROP; audited primary-segment perimeter",
            "definitions": {
                "rfo": "Revenue from Operations (accountCode 01 Sale); December-FYE comparable panel",
                "npat": "Net profit attributable to owners of the parent",
                "price": "Adjusted price return; excludes cash dividends",
                "valuation": "Aggregate positive-earnings P/E; loss-makers stay null/excluded from the denominator",
                "marketCap": "Point-in-time market capitalisation; adjusted=N",
            },
            "sourceLineage": ["SETSMART Company Fundamental API", "SET Factsheet", "FY2025 MD&A", "Broker research (forward cross-check)"],
            "sourceFiles": [
                "food_prop_segment_official_2026-08-06.csv",
                "food_prop_company_official_2026-08-06.csv",
                "food_prop_segment_fy2024_2025_three_lens_2026-08-06.csv",
                "food_prop_company_fy2024_2025_selection_base_2026-08-06.csv",
            ],
            "warning": "Price/valuation explanations are labelled inference unless directly supported by management or a dated market source.",
        },
        "sectors": sectors,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("data/sector-intelligence.json"))
    args = parser.parse_args()
    payload = build(args.theme_root)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out} ({sum(len(s['segments']) for s in payload['sectors'].values())} segments)")


if __name__ == "__main__":
    main()
