"""Build FY2025 issuer performance-driver cards from audited facts and MD&A.

Deterministic only: never invent a causal bridge from RFO/NPAT arithmetic.
"""
from __future__ import annotations

import json
import re
import copy
import hashlib
from pathlib import Path


def bi(en: str, th: str) -> dict:
    return {"en": en, "th": th}


CURATED = {
    "CPF": {
        "rfo": [bi("Management's sales line fell 2% because baht appreciation reduced translated overseas sales; excluding FX, sales grew about 3%. The audited RFO shown above remains the SET 01 Sale line.", "ยอดขายตามนิยามของบริษัทลด 2% เพราะเงินบาทแข็งกดรายได้ต่างประเทศเมื่อแปลงเป็นบาท; หากตัด FX ยอดขายยังโตประมาณ 3% ขณะที่ตัวเลข RFO ด้านบนคงใช้ SET 01 Sale")],
        "npat": [bi("Gross margin rose to 16.9% from 14.6% on production-cost control, lower soybean-meal cost, stronger biosecurity and higher regional hog prices; these outweighed the softer reported sales base.", "อัตรากำไรขั้นต้นเพิ่มเป็น 16.9% จาก 14.6% จากการควบคุมต้นทุน ต้นทุนกากถั่วเหลืองลดลง biosecurity ที่ดีขึ้น และราคาสุกรในภูมิภาคสูงขึ้น จึงชดเชยยอดขายรายงานที่อ่อนลง")],
    },
    "TFG": {
        "rfo": [bi("Revenue grew 11% as chicken volume rose 6%, Vietnam swine volume 18%, feed volume 23%, and retail shops expanded from 401 to 615.", "รายได้โต 11% จากปริมาณไก่เพิ่ม 6% สุกรเวียดนามเพิ่ม 18% อาหารสัตว์เพิ่ม 23% และสาขาค้าปลีกขยายจาก 401 เป็น 615 แห่ง")],
        "npat": [bi("Owner profit rose 137% as gross profit increased 71%; higher protein volume, retail expansion, better distribution/inventory management and lower raw-material cost per unit expanded margin.", "กำไรส่วนผู้ถือหุ้นเพิ่ม 137% ตามกำไรขั้นต้นที่เพิ่ม 71%; ปริมาณโปรตีนและสาขาค้าปลีกที่สูงขึ้น การบริหารช่องทาง/สต็อกที่ดีขึ้น และต้นทุนวัตถุดิบต่อหน่วยลดลงช่วยขยาย margin")],
    },
    "BTG": {
        "rfo": [bi("Sales expanded with the livestock/food platform and a greater contribution from processed food, ready-to-eat, foodservice, modern trade and exports.", "ยอดขายขยายตัวจากแพลตฟอร์มปศุสัตว์และอาหาร รวมถึงสัดส่วนสินค้าแปรรูป อาหารพร้อมทาน foodservice modern trade และส่งออกที่เพิ่มขึ้น")],
        "npat": [bi("Profit rose sharply as corn, soybean-meal and wheat costs declined, domestic pork prices improved, product mix shifted to higher-margin channels and cost control became more efficient.", "กำไรเพิ่มขึ้นมากจากต้นทุนข้าวโพด กากถั่วเหลือง และข้าวสาลีลดลง ราคาสุกรในประเทศดีขึ้น mix ขยับสู่ช่องทาง margin สูง และควบคุมต้นทุนมีประสิทธิภาพขึ้น")],
    },
    "TU": {
        "rfo": [bi("FY2025 sales fell about 4% in reported baht despite continued volume growth; baht appreciation and translation offset the operating volume signal.", "ยอดขาย FY2025 ลดประมาณ 4% ในรูปเงินบาท แม้ปริมาณขายยังเติบโต เพราะเงินบาทแข็งและผลแปลงค่างบหักล้างสัญญาณด้านปริมาณ")],
        "npat": [bi("Net profit declined 7.5% even with record 18.9% gross margin because transformation costs and operating expenses absorbed the gross-profit improvement.", "กำไรสุทธิลด 7.5% แม้อัตรากำไรขั้นต้นทำสถิติ 18.9% เพราะต้นทุน transformation และค่าใช้จ่ายดำเนินงานดูดซับกำไรขั้นต้นที่ดีขึ้น")],
    },
    "ITC": {
        "rfo": [bi("Revenue was supported by higher volume and premium product mix, but baht appreciation reduced translated export revenue.", "รายได้ได้แรงหนุนจากปริมาณและ premium product mix ที่ดีขึ้น แต่เงินบาทแข็งกดรายได้ส่งออกเมื่อแปลงเป็นบาท")],
        "npat": [bi("Profit fell despite revenue growth because raw-material pressure, FX and transformation/start-up costs compressed conversion from sales to owner profit.", "กำไรลดลงสวนรายได้ เพราะแรงกดดันวัตถุดิบ FX และต้นทุน transformation/เริ่มเดินเครื่อง ทำให้การแปลงรายได้เป็นกำไรส่วนผู้ถือหุ้นอ่อนลง")],
    },
    "OSP": {
        "rfo": [bi("Reported revenue softened as domestic beverages fell sharply in 1H25 before recovering in 2H25; international beverages grew, led by Myanmar and Laos.", "รายได้รายงานอ่อนตัวจากเครื่องดื่มในประเทศที่ลดแรงใน 1H25 ก่อนฟื้นใน 2H25 ขณะที่ต่างประเทศโตจากเมียนมาและลาว")],
        "npat": [bi("Profit more than doubled as gross margin reached 40.1%, supported by manufacturing efficiency, cost discipline and ROI-led marketing.", "กำไรมากกว่าสองเท่าเมื่อ gross margin เพิ่มเป็น 40.1% จากประสิทธิภาพการผลิต วินัยต้นทุน และการตลาดแบบเน้น ROI")],
    },
    "ICHI": {
        "rfo": [bi("FY2025 sales fell 5.9% to THB8.09bn as domestic sales declined 8.6% amid a weak economy and a shorter-than-usual summer; international sales rose 37.2% on continued export-OEM growth.", "ยอดขาย FY2025 ลด 5.9% เหลือ 8.09 พันลบ. จากยอดขายในประเทศลด 8.6% เพราะเศรษฐกิจซบเซาและฤดูร้อนสั้นกว่าปกติ ขณะที่ยอดขายต่างประเทศโต 37.2% จาก OEM เพื่อส่งออกที่ขยายต่อเนื่อง")],
        "npat": [
            bi("Net profit rose 1.6% to THB1.33bn and net margin increased to 16.4% from 15.2%.", "กำไรสุทธิเพิ่ม 1.6% เป็น 1.33 พันลบ. และ net margin เพิ่มเป็น 16.4% จาก 15.2%"),
            bi("Tax expense fell 56.9% because operating profit was lower and the company received BOI benefits under community and social development measures.", "ภาษีลด 56.9% เพราะกำไรดำเนินงานลดลงและบริษัทได้รับสิทธิ BOI ภายใต้มาตรการพัฒนาชุมชนและสังคม"),
            bi("Share of JV profit increased by THB7.3m after new-product launches and an expansion of distributors widened market coverage.", "ส่วนแบ่งกำไร JV เพิ่ม 7.3 ลบ. หลังเปิดสินค้าใหม่และเพิ่มจำนวนผู้จัดจำหน่ายให้ครอบคลุมพื้นที่มากขึ้น"),
        ],

    },    "SAPPE": {
        "rfo": [bi("Revenue fell about 23% as major overseas markets slowed and baht appreciation reduced export proceeds.", "รายได้ลดประมาณ 23% จากตลาดต่างประเทศหลักชะลอและเงินบาทแข็งกดรายรับส่งออก")],
        "npat": [bi("Profit fell about 38% because the lower export base reduced operating leverage while FX and market-development costs pressured margin.", "กำไรลดประมาณ 38% เพราะฐานส่งออกที่ลดลงทำให้ operating leverage อ่อนลง ขณะที่ FX และค่าใช้จ่ายพัฒนาตลาดกด margin")],
    },
    "M": {
        "rfo": [bi("Revenue fell 2.5% and same-store sales declined 2.8% as purchasing power stayed weak, despite the THB299 buffet campaign and Bonus Suki expansion.", "รายได้ลด 2.5% และ SSSG ลด 2.8% จากกำลังซื้ออ่อน แม้มีแคมเปญบุฟเฟต์ 299 บาทและการขยาย Bonus Suki")],
        "npat": [bi("Profit fell 41.9% as gross margin dropped to 64.6% from 67.4%; value-buffet formats carry higher food cost while competition limited price pass-through.", "กำไรลด 41.9% เมื่อ gross margin ลดเป็น 64.6% จาก 67.4%; รูปแบบบุฟเฟต์ราคาคุ้มค่ามี food cost สูงขึ้น ขณะที่การแข่งขันจำกัดการส่งผ่านต้นทุนไปยังราคา")],
    },
    "OKJ": {
        "rfo": [bi("Revenue grew 12.6% as ten new stores enlarged the network, but flagship same-store sales fell 21.6%; growth came from space rather than store productivity.", "รายได้โต 12.6% จากการเพิ่ม 10 สาขา แต่ SSSG แบรนด์หลักลด 21.6%; การเติบโตมาจากพื้นที่ขาย ไม่ใช่ productivity ต่อสาขา")],
        "npat": [bi("Profit fell 65.1% because new-store fixed costs rose faster than sales and weak same-store sales produced negative operating leverage; 4Q25 also included THB17m of write-offs.", "กำไรลด 65.1% เพราะต้นทุนคงที่จากสาขาใหม่เพิ่มเร็วกว่ายอดขายและ SSSG ที่อ่อนทำให้เกิด negative operating leverage; 4Q25 ยังมี write-off 17 ลบ.")],
        "special": [bi("Management slowed the core-store rollout and deferred a large southern investment; the turnaround depends on higher sales per store and new-format economics.", "ฝ่ายจัดการชะลอการเปิดสาขาหลักและเลื่อนลงทุนขนาดใหญ่ภาคใต้ การฟื้นจึงขึ้นกับยอดขายต่อสาขาและ economics ของ format ใหม่")],
    },
    "TVO": {
        "rfo": [bi("Sales fell 9.2% because average selling prices followed lower global soybean prices; export volume also faced intense price competition.", "ยอดขายลด 9.2% เพราะราคาขายเฉลี่ยปรับตามราคาถั่วเหลืองโลกที่ลดลง และปริมาณส่งออกเผชิญการแข่งขันด้านราคาสูง")],
        "npat": [bi("Profit still rose 4.1% as cheaper soybean input and inventory/cost management lifted gross margin to 12.9% from 10.7%.", "กำไรยังเพิ่ม 4.1% เพราะต้นทุนถั่วเหลืองและการบริหารสต็อก/ต้นทุนช่วยให้ gross margin เพิ่มเป็น 12.9% จาก 10.7%")],
        "special": [bi("FX/derivative results swung to a THB116m loss from an THB87m gain, a recurring source of volatility.", "ผล FX/อนุพันธ์พลิกจากกำไร 87 ลบ. เป็นขาดทุน 116 ลบ. เป็นแหล่งความผันผวนที่ต้องแยกจากการดำเนินงาน")],
    },
    "BRR": {
        "rfo": [bi("Revenue declined with lower realised sugar prices and weaker sugar-related activity; hedging helped limit FX volatility.", "รายได้ลดตามราคาขายน้ำตาลจริงและกิจกรรมที่เกี่ยวข้องกับน้ำตาลที่อ่อนลง ขณะที่ hedging ช่วยจำกัดความผันผวน FX")],
        "npat": [bi("Profit fell 73% as gross margin dropped to 15.5% from 25.8% and the company recorded THB176m of inventory devaluation after global sugar prices declined.", "กำไรลด 73% เมื่อ gross margin ลดเป็น 15.5% จาก 25.8% และบันทึกขาดทุนด้อยค่าสินค้าคงเหลือ 176 ลบ. หลังราคาน้ำตาลโลกลดลง")],
    },
    "CH": {
        "rfo": [bi("Sales fell 25.9%, led by a 30.2% decline in dehydrated fruit, the main revenue contributor.", "ยอดขายลด 25.9% นำโดยผลไม้อบแห้งซึ่งเป็นรายได้หลักลด 30.2%")],
        "npat": [bi("The company turned to loss because dehydrated-fruit revenue fell and gross margin declined across all three product groups, despite expense control and lower finance cost.", "บริษัทพลิกเป็นขาดทุนจากรายได้ผลไม้อบแห้งลดลงและ gross margin ลดทุก 3 กลุ่มสินค้า แม้ควบคุมค่าใช้จ่ายและดอกเบี้ยลดลง")],
    },
    "SUN": {
        "rfo": [bi("Sales grew 2.2% on higher customer-brand volume, but baht appreciation reduced export revenue and weakened the fourth-quarter exit rate.", "ยอดขายโต 2.2% จากปริมาณ customer brand ที่เพิ่มขึ้น แต่เงินบาทแข็งกดรายได้ส่งออกและทำให้ momentum ปลายปีอ่อนลง")],
        "npat": [bi("Profit fell 39.1% as gross margin compressed to 15.6% from 20.0%; FX and cost pressure more than offset the volume gain.", "กำไรลด 39.1% เมื่อ gross margin ลดเป็น 15.6% จาก 20.0%; แรงกดดัน FX และต้นทุนมากกว่าประโยชน์จากปริมาณที่เพิ่ม")],
    },
    "LH": {
        "rfo": [bi("Revenue fell 15.9% as housing transfers weakened; tighter credit and soft residential demand outweighed growth in hotel/recurring income.", "รายได้ลด 15.9% จากยอดโอนที่อยู่อาศัยอ่อนตัว ข้อจำกัดสินเชื่อและอุปสงค์บ้านที่ซบเซามากกว่าการเติบโตของโรงแรม/รายได้ประจำ")],
        "npat": [bi("Owner profit fell 32% as gross profit declined about THB899m and the contribution from associates weakened alongside the lower transfer base.", "กำไรส่วนผู้ถือหุ้นลด 32% จากกำไรขั้นต้นลดประมาณ 899 ลบ. และส่วนแบ่งกำไรบริษัทร่วมอ่อนลงตามฐานยอดโอนที่ต่ำลง")],
    },
    "SPALI": {
        "rfo": [bi("Revenue fell about 23% as transfers declined from a high FY2024 base; mortgage rejection and a slower residential market delayed backlog conversion.", "รายได้ลดประมาณ 23% จากยอดโอนลดบนฐาน FY2024 ที่สูง การปฏิเสธสินเชื่อและตลาดที่อยู่อาศัยชะลอทำให้ backlog แปลงเป็นรายได้ช้าลง")],
        "npat": [bi("Profit fell about 35% as lower transfers reduced operating leverage while land/construction cost inflation and mix pressured gross margin.", "กำไรลดประมาณ 35% เพราะยอดโอนที่ต่ำลงกด operating leverage ขณะที่ต้นทุนที่ดิน/ก่อสร้างและ mix กด gross margin")],
    },
    "PSH": {
        "rfo": [bi("Revenue fell about 29%, with real-estate revenue down roughly 34%, as transfers and new demand weakened under tight mortgage approval.", "รายได้ลดประมาณ 29% โดยรายได้อสังหาฯ ลดราว 34% จากยอดโอนและอุปสงค์ใหม่อ่อนตัวภายใต้การอนุมัติสินเชื่อที่เข้มงวด")],
        "npat": [bi("The company turned to loss because the sharp volume decline created negative operating leverage and weaker gross-profit absorption.", "บริษัทพลิกเป็นขาดทุนเพราะปริมาณที่ลดแรงทำให้เกิด negative operating leverage และการดูดซับต้นทุนผ่านกำไรขั้นต้นอ่อนลง")],
    },
    "WHA": {
        "rfo": [bi("RFO rose 34.7% on land transfers and recurring utilities/logistics income, with demand linked to FDI, data centres and supply-chain relocation.", "RFO เพิ่ม 34.7% จากการโอนที่ดินและรายได้ประจำด้านสาธารณูปโภค/โลจิสติกส์ โดยอุปสงค์เชื่อมโยง FDI data centre และการย้ายฐาน supply chain")],
        "npat": [bi("Profit rose, but land mix and lower-margin asset sales compressed conversion; early-stage mobility investment remained a drag.", "กำไรเพิ่มขึ้น แต่ mix ที่ดินและการขายสินทรัพย์ margin ต่ำกดการแปลงรายได้เป็นกำไร ขณะที่ธุรกิจ mobility ระยะเริ่มต้นยังเป็นตัวฉุด")],
    },
    "AMATA": {
        "rfo": [bi("Revenue fell about 3% as land-transfer timing lagged, despite a healthy industrial-estate demand pipeline.", "รายได้ลดประมาณ 3% จากจังหวะการโอนที่ดินล่าช้า แม้ pipeline ความต้องการนิคมอุตสาหกรรมยังดี")],
        "npat": [bi("Record profit rose 28% because higher-margin transfer mix and share of profit from Amata B.Grimm Power outweighed the softer revenue base.", "กำไรทำสถิติเพิ่ม 28% เพราะ mix การโอน margin สูงและส่วนแบ่งกำไรจาก Amata B.Grimm Power ชดเชยฐานรายได้ที่อ่อนลง")],
        "special": [bi("Reported profit included a THB564m subsidiary-disposal gain and a THB215m Vietnam development-cost adjustment; these require a core bridge.", "กำไรรายงานรวมกำไรขายบริษัทย่อย 564 ลบ. และการปรับต้นทุนพัฒนาเวียดนาม 215 ลบ. จึงต้องทำ core bridge")],
    },
    "ROJNA": {
        "rfo": [bi("Revenue fell about 25% as industrial-land transfers weakened and power revenue declined after solar Adder roll-offs, a lower Ft tariff and SPP1 contract expiry.", "รายได้ลดประมาณ 25% จากการโอนที่ดินนิคมลดลง และรายได้ไฟฟ้าหดหลัง Adder โซลาร์ทยอยหมด ค่า Ft ลด และสัญญา SPP1 สิ้นสุด")],
        "npat": [bi("The company swung to loss mainly because financial-asset fair value reversed to a THB1.821bn loss from a THB1.601bn gain, a roughly THB3.4bn adverse swing.", "บริษัทพลิกเป็นขาดทุนหลักจาก fair value สินทรัพย์การเงินพลิกเป็นขาดทุน 1.821 พันลบ. จากกำไร 1.601 พันลบ. หรือแกว่งลบราว 3.4 พันลบ.")],
        "special": [bi("The fair-value swing is non-cash; power-contract expiry is the structural operating item.", "fair-value เป็นรายการไม่ใช่เงินสด ขณะที่การหมดสัญญาไฟฟ้าเป็นประเด็นดำเนินงานเชิงโครงสร้าง")],
    },
    "CPN": {
        "rfo": [bi("Recurring rental/service income grew with Central Park, traffic, occupancy and same-store rent; residential revenue fell 30% on transfer schedules and tighter bank lending.", "รายได้ประจำค่าเช่า/บริการโตจาก Central Park traffic occupancy และค่าเช่าเดิม ขณะที่รายได้ที่อยู่อาศัยลด 30% จากตารางโอนและธนาคารเข้มสินเชื่อ")],
        "npat": [bi("Core profit grew about 7% on higher gross profit, other income and controlled SG&A; reported profit was higher because of THB2.119bn non-recurring items.", "กำไรหลักโตประมาณ 7% จากกำไรขั้นต้น รายได้อื่น และการคุม SG&A ขณะที่กำไรรายงานสูงกว่าเพราะรายการไม่ประจำ 2.119 พันลบ.")],
        "special": [bi("Non-recurring items comprised the Rama 2/CPNREIT lease-renewal gain and finance-lease interest; use core profit for trend analysis.", "รายการไม่ประจำมาจากต่อสัญญาเช่า Rama 2/CPNREIT และดอกเบี้ย finance lease จึงควรใช้กำไรหลักอ่านแนวโน้ม")],
    },
    "AWC": {
        "rfo": [bi("Revenue grew about 10% as five new hotels and commercial attractions/space expanded the portfolio.", "รายได้โตประมาณ 10% จากโรงแรมใหม่ 5 แห่งและพื้นที่/แหล่งท่องเที่ยวเชิงพาณิชย์ที่เพิ่มขึ้น")],
        "npat": [bi("Reported profit rose 9%, but included a THB5.555bn investment-property fair-value gain; core cash earnings were materially below headline NPAT.", "กำไรรายงานเพิ่ม 9% แต่รวม fair-value gain อสังหาริมทรัพย์เพื่อการลงทุน 5.555 พันลบ. ทำให้กำไรเงินสดหลักต่ำกว่า NPAT headline มาก")],
    },
    "S": {
        "rfo": [bi("Sales/service revenue fell about 7% as residential transfers softened, although hotel and commercial normalized operations remained profitable.", "รายได้ขาย/บริการลดประมาณ 7% จากยอดโอนที่อยู่อาศัยอ่อนตัว แม้การดำเนินงานปกติของโรงแรมและ commercial ยังมีกำไร")],
        "npat": [bi("The company swung to a reported loss mainly from hotel-asset impairment; management cited THB531m normalized profit after excluding impairment and non-operating items.", "บริษัทพลิกเป็นขาดทุนรายงานหลักจากด้อยค่าสินทรัพย์โรงแรม โดยฝ่ายจัดการระบุกำไรปกติ 531 ลบ. หลังตัดด้อยค่าและรายการไม่ดำเนินงาน")],
    },
    "J": {
        "rfo": [bi("Revenue increased as community-mall and senior-care income expanded, partly offset by lower IT Junction rental revenue.", "รายได้เพิ่มจาก community mall และ senior care ขยายตัว ชดเชยบางส่วนด้วยรายได้เช่าพื้นที่ IT Junction ที่ลดลง")],
        "npat": [bi("The company swung to a large loss after a THB550.5m investment-property fair-value loss and THB116.4m asset impairment, both non-cash.", "บริษัทพลิกเป็นขาดทุนมากจาก fair-value loss อสังหาริมทรัพย์เพื่อการลงทุน 550.5 ลบ. และด้อยค่าสินทรัพย์ 116.4 ลบ. ซึ่งเป็นรายการไม่ใช่เงินสด")],
    },
    "RABBIT": {
        "rfo": [bi("Revenue rose 42% as real-estate sales and insurance/financial-services income expanded.", "รายได้เพิ่ม 42% จากยอดขายอสังหาริมทรัพย์และรายได้ประกัน/บริการการเงินที่ขยายตัว")],
        "npat": [bi("The company returned to profit as the higher revenue base and below-line items outweighed a THB457m share of losses from associates/JVs.", "บริษัทกลับมามีกำไรเมื่อฐานรายได้ที่สูงขึ้นและรายการต่ำกว่าการดำเนินงานชดเชยส่วนแบ่งขาดทุนบริษัทร่วม/JV 457 ลบ.")],
    },
    "FPT": {
        "rfo": [bi("Operating revenue fell 3% as residential sales declined 5.8% under weak demand, high household debt and tighter lending; this was partly offset by 5.4% growth in industrial rental/services from factory and warehouse demand.", "รายได้จากการประกอบธุรกิจลด 3% จากยอดขายที่อยู่อาศัยลด 5.8% ภายใต้อุปสงค์อ่อน หนี้ครัวเรือนสูง และสินเชื่อเข้มขึ้น ชดเชยบางส่วนด้วยค่าเช่า/บริการอุตสาหกรรมโต 5.4% จากความต้องการโรงงานและคลังสินค้า")],
        "npat": [bi("Owner profit still rose 1.6% because a THB1.33bn investment-property disposal gain and higher associate/JV profit offset weaker residential margin, impairments, higher SG&A and finance cost.", "กำไรส่วนผู้ถือหุ้นยังเพิ่ม 1.6% เพราะกำไรขายอสังหาฯ เพื่อการลงทุน 1.33 พันลบ. และส่วนแบ่งกำไรบริษัทร่วม/JV ที่สูงขึ้น ชดเชย margin ที่อยู่อาศัยลด ด้อยค่า SG&A และดอกเบี้ยที่เพิ่ม")],
        "special": [bi("Residential gross margin fell to 19.9% from 25.9%, partly due to a stricter NRV allowance for completed inventory older than one year.", "gross margin ที่อยู่อาศัยลดเป็น 19.9% จาก 25.9% ส่วนหนึ่งจากเกณฑ์ตั้ง NRV ที่เข้มขึ้นสำหรับสินค้าสร้างเสร็จเกิน 1 ปี")],
    },
    "AP": {
        "rfo": [
            bi("FY2025 total revenue rose 1.0% to THB37,345m: property sales increased 1.7%, while service revenue fell 18.2%.", "รายได้รวม FY2025 เพิ่ม 1.0% เป็น 37,345 ลบ. โดยรายได้ขายอสังหาฯ เพิ่ม 1.7% ขณะที่รายได้บริการลด 18.2%"),
            bi("Low-rise revenue grew 6.5% to THB34,342m despite a challenging housing market.", "รายได้แนวราบโต 6.5% เป็น 34,342 ลบ. แม้ตลาดที่อยู่อาศัยเผชิญภาวะท้าทาย"),
            bi("JV condominium revenue fell 14.7% as the post-earthquake slowdown weakened transfer momentum.", "รายได้คอนโด JV ลด 14.7% เพราะผลกระทบหลังแผ่นดินไหวทำให้ momentum การโอนอ่อนลง"),
        ],
        "npat": [
            bi("Owner profit fell 14.0% to THB4,316m from THB5,020m.", "กำไรส่วนผู้ถือหุ้นลด 14.0% เหลือ 4,316 ลบ. จาก 5,020 ลบ."),
            bi("Overall gross margin declined to 31.9% from 34.3%.", "gross margin รวมลดเป็น 31.9% จาก 34.3%"),
            bi("Management attributed Q4 margin pressure mainly to market conditions.", "ฝ่ายจัดการระบุว่าแรงกดดัน margin ในไตรมาส 4 มาจากภาวะตลาดเป็นหลัก"),
            bi("Share of JV profit fell 29.0% as the post-earthquake slowdown weakened condominium transfer momentum.", "ส่วนแบ่งกำไร JV ลด 29.0% เพราะผลกระทบหลังแผ่นดินไหวทำให้ momentum การโอนคอนโดอ่อนลง"),
        ],
    },    "UV": {
        "rfo": [bi("Core sales/service/rental revenue fell 9% to THB14.17bn, mainly because property revenue fell 38% on fewer condominium transfers amid the post-earthquake slowdown and tighter mortgages; industrial revenue also fell 8% on lower zinc-oxide volume.", "รายได้หลักจากขาย บริการ และให้เช่าลด 9% เหลือ 14.17 พันลบ. หลักจากรายได้อสังหาฯ ลด 38% เพราะโอนคอนโดลดหลังแผ่นดินไหวและสินเชื่อเข้มขึ้น ขณะที่อุตสาหกรรมลด 8% จากปริมาณ zinc oxide ลดลง")],
        "npat": [bi("Normalized profit fell as the lower property base and higher administration/tax expense outweighed lower finance cost; owner NPAT turned to a THB45m loss even though consolidated net profit was positive.", "กำไรปกติลดลงเพราะฐานอสังหาฯ ที่ต่ำลงและค่าใช้จ่ายบริหาร/ภาษีเพิ่ม มากกว่าดอกเบี้ยที่ลดลง; NPAT ส่วนบริษัทใหญ่พลิกเป็นขาดทุน 45 ลบ. แม้กำไรสุทธิรวมยังเป็นบวก")],
        "special": [bi("Consolidated net profit included THB241m insurance compensation, THB24.5m unrealised FX gain and THB18.4m investment-property fair-value gain; owner NPAT must be read separately.", "กำไรสุทธิรวมมีค่าสินไหมประกัน 241 ลบ. กำไร FX ที่ยังไม่เกิด 24.5 ลบ. และ fair-value gain 18.4 ลบ. จึงต้องแยกอ่าน NPAT ส่วนบริษัทใหญ่")],
    },    "AKS": {
        "rfo": [bi("FY2025 revenue was only about THB210m and the company has not filed the annual MD&A in the canonical corpus; no management causal attribution is asserted.", "รายได้ FY2025 เหลือเพียงประมาณ 210 ลบ. และยังไม่มี MD&A ประจำปีในคลังหลัก จึงไม่อ้างสาเหตุว่าเป็นคำอธิบายจากฝ่ายจัดการ")],
        "npat": [bi("The THB315m loss, negative EBITDA and negative equity indicate operating and solvency distress, but the missing filing prevents a management-attributed profit bridge.", "ขาดทุน 315 ลบ. EBITDA ติดลบ และส่วนผู้ถือหุ้นติดลบสะท้อนความเสี่ยงดำเนินงาน/ฐานะการเงิน แต่การไม่มี filing ทำให้ยังทำ profit bridge จากฝ่ายจัดการไม่ได้")],
    },
}

ANNUAL_RE = re.compile(r"(?i)\b(?:FY\s*2025|FY25|2025FY|full[- ]year 2025|year 2025|2025 full year)\b")
QUARTER_RE = re.compile(r"(?i)\bQ[1-4]\s*[/ -]?\s*(?:2026|26|69)\b|FY\s*2026|FY26|FY2569|2026 guidance")
CAUSE_RE = re.compile(r"(?i)driv|due to|because|attribut|mainly|result|supported|offset|pressure|impact|from |สาเหตุ|เนื่องจาก|เป็นผล|หลักจาก")
RFO_RE = re.compile(r"(?i)revenue|sales|ยอดขาย|รายได้")
NPAT_RE = re.compile(r"(?i)profit|loss|margin|cost|impair|กำไร|ขาดทุน|ต้นทุน|ด้อยค่า")
SPECIAL_RE = re.compile(r"(?i)one[- ]off|non[- ]recurring|impair|fair value|write[- ]off|disposal|FX|foreign exchange|ด้อยค่า|มูลค่ายุติธรรม|รายการไม่ประจำ")


def _clean(text) -> str:
    text = re.sub(r"\(cid:\d+\)", " ", str(text or ""))
    text = re.sub(r"\s+", " ", text).strip(" -•\t\r\n")
    return text[:700]


def _flatten(value):
    if isinstance(value, list):
        for item in value:
            yield from _flatten(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from _flatten(item)
    elif value:
        yield str(value)


def _annual_items(report: dict) -> list[str]:
    raw = []
    for field in ("summary", "financialSnapshot", "mdaSynthesis"):
        raw.extend(_flatten(report.get(field)))
    items = []
    for block in raw:
        for item in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])|\n+", block):
            item = _clean(item)
            if len(item) < 45 or not ANNUAL_RE.search(item) or QUARTER_RE.search(item):
                continue
            if item not in items:
                items.append(item)
    return items


def _best(items: list[str], category: str) -> list[str]:
    target = RFO_RE if category == "rfo" else NPAT_RE
    scored = []
    for item in items:
        if not target.search(item):
            continue
        score = 3 * bool(CAUSE_RE.search(item)) + 2 * bool(SPECIAL_RE.search(item)) + len(target.findall(item))
        scored.append((score, item))
    return [item for _, item in sorted(scored, key=lambda pair: (-pair[0], len(pair[1])))[:2]]


def _strip_frontmatter(text: str) -> str:
    return re.sub(r"\A\ufeff?---\s*\n.*?\n---\s*\n", "", text, count=1, flags=re.S)


def _contains_thai(text: str) -> bool:
    return bool(re.search(r"[\u0E00-\u0E7F]", text or ""))


def _source_language(path: Path | None, text: str = "") -> str:
    if path and path.stem.endswith("_T"):
        return "th"
    if path and path.stem.endswith("_E"):
        return "en"
    return "th" if _contains_thai(text) else "en"


def mda_source_status(path: Path | None) -> str:
    if not path:
        return "missing_primary_source"
    text = _strip_frontmatter(path.read_text(encoding="utf-8", errors="ignore"))
    lowered = text.lower()
    substantive = len(re.sub(r"\s+", "", text)) >= 1000
    stub = ("revenue: n/a" in lowered and "net profit: n/a" in lowered) or "\n- n/a\n" in lowered
    has_metric = bool(RFO_RE.search(text) and NPAT_RE.search(text))
    has_explanation = bool(CAUSE_RE.search(text))
    return "primary_verified" if substantive and not stub and has_metric and has_explanation else "reextract_required"


def _mda_passages(path: Path | None) -> list[dict]:
    if not path:
        return []
    raw = _strip_frontmatter(path.read_text(encoding="utf-8", errors="ignore"))
    language = _source_language(path, raw)
    passages = []
    current = []

    def flush():
        if not current:
            return
        text = _clean(" ".join(current))
        current.clear()
        if not 55 <= len(text) <= 1400:
            return
        lowered = text.lower()
        if "n/a (n/a" in lowered or lowered in {"n/a", "- n/a"}:
            return
        passages.append({"passageId": f"p{len(passages) + 1:03d}", "text": text, "language": language})

    for raw_line in raw.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            flush()
            continue
        if line.startswith("|") or re.fullmatch(r"[-–—\s\d/]+", line):
            flush()
            continue
        if len(line) < 90 and re.match(r"^(?:\d+[.)]?\s*)?[A-Z\u0E00-\u0E7F][^.!?]{0,88}$", line):
            flush()
            current.append(line)
            continue
        current.append(line)
        if len(" ".join(current)) >= 1150:
            flush()
    flush()
    return passages


def _candidate_score(text: str, category: str) -> float:
    lowered = text.lower()
    target = SPECIAL_RE if category == "special" else (RFO_RE if category == "rfo" else NPAT_RE)
    if not target.search(text):
        return -1
    cause_count = len(CAUSE_RE.findall(text))
    metric_count = len(target.findall(text))
    number_count = len(re.findall(r"(?:\b\d[\d,.]*\s*(?:%|million|mn|baht|thb)|(?:ร้อยละ|ล้านบาท)\s*\d)", text, flags=re.I))
    direction_count = len(re.findall(r"increase|decrease|grew|growth|declin|fell|rose|improv|higher|lower|เพิ่ม|ลด|เติบโต|หดตัว|พลิก", text, flags=re.I))
    score = 5 * cause_count + 3 * metric_count + 1.5 * min(number_count, 6) + 2 * min(direction_count, 4)
    if category == "special":
        score += 8 * len(SPECIAL_RE.findall(text))
    elif category == "rfo":
        score += 3 * len(RFO_RE.findall(text)) - 1.5 * len(NPAT_RE.findall(text))
    else:
        score += 3 * len(NPAT_RE.findall(text))
        score += 2 * len(SPECIAL_RE.findall(text))
    if re.search(r"gdp|economic outlook|เศรษฐกิจ(?:ไทย|โลก)|inflation|อัตราเงินเฟ้อ", lowered) and number_count < 2:
        score -= 8
    if re.search(r"subject|to:|เรียน กรรมการ|stock exchange of thailand", lowered):
        score -= 5
    return score


def _mda_candidates(path: Path | None, category: str, limit: int = 2) -> list[dict]:
    if mda_source_status(path) != "primary_verified":
        return []
    scored = []
    for passage in _mda_passages(path):
        score = _candidate_score(passage["text"], category)
        if score < 5:
            continue
        scored.append((score, passage))
    selected = []
    for score, passage in sorted(scored, key=lambda pair: (-pair[0], len(pair[1]["text"]))):
        words = set(re.findall(r"[A-Za-z\u0E00-\u0E7F]+", passage["text"].lower()))
        duplicate = False
        for item in selected:
            other = set(re.findall(r"[A-Za-z\u0E00-\u0E7F]+", item["text"].lower()))
            union = words | other
            if union and len(words & other) / len(union) > 0.68:
                duplicate = True
                break
        if duplicate:
            continue
        selected.append({**passage, "score": round(score, 1)})
        if len(selected) >= limit:
            break
    return selected


def _mda_candidate(path: Path | None, category: str) -> str | None:
    candidates = _mda_candidates(path, category, 1)
    return candidates[0]["text"] if candidates else None


def _source_evidence(path: Path, passage: dict, category: str) -> dict:
    quote = passage["text"][:950]
    return {
        "sourceId": f"MDA_{path.stem.split('_')[1]}_FY2025",
        "passageId": passage["passageId"],
        "category": category,
        "language": passage["language"],
        "quote": quote,
        "quoteSha256": hashlib.sha256(quote.encode("utf-8")).hexdigest(),
        "matchScore": passage["score"],
    }


AUTO_CAUSE_RULES = [
    (r"(?:margin|gpm|npm).{0,45}(?:rose|grew|expand|improv|higher)|(?:rose|grew|expand|improv|higher).{0,45}(?:margin|gpm|npm)", "อัตรากำไรดีขึ้น"),
    (r"(?:margin|gpm|npm).{0,45}(?:fell|declin|compress|eased|lower|drop)|(?:fell|declin|compress|eased|lower|drop).{0,45}(?:margin|gpm|npm)", "อัตรากำไรลดลง"),
    (r"gross margin|operating margin|net margin|\bgpm\b|\bnpm\b", "การเปลี่ยนแปลงของอัตรากำไร"),
    (r"cost control|cost management|efficien|productivity", "การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน"),
    (r"raw material|input cost|feed cost|ingredient cost|construction cost|cost of goods|\bcogs\b", "ต้นทุนวัตถุดิบและต้นทุนการผลิต"),
    (r"palm[- ]oil", "ราคาน้ำมันปาล์ม"),
    (r"soybean|soy meal", "ต้นทุนถั่วเหลืองและกากถั่วเหลือง"),
    (r"hog|swine|livestock|broiler|chicken", "ราคาและปริมาณปศุสัตว์"),
    (r"tuna|salmon|shrimp|seafood|fish price", "ราคาวัตถุดิบและปริมาณอาหารทะเล"),
    (r"sales volume|volume growth|volume rose|volume fell|lower volume|higher volume|production volume", "ปริมาณขายและปริมาณการผลิต"),
    (r"selling price|pricing|price/mix|product mix|sales mix|revenue mix", "ราคาขายและส่วนผสมผลิตภัณฑ์"),
    (r"export|overseas|international sales", "ยอดขายส่งออกและตลาดต่างประเทศ"),
    (r"strengthening baht|stronger baht|baht appreciation|currency translation|foreign exchange|\bfx\b", "เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน"),
    (r"tariff|trade measure|trade headwind", "มาตรการภาษีนำเข้าและข้อกีดกันทางการค้า"),
    (r"geopolit|war|border conflict", "ความเสี่ยงด้านภูมิรัฐศาสตร์"),
    (r"weak demand|soft demand|slowdown|slowing economy|weak economy|domestic economy|consumer spending", "อุปสงค์และกำลังซื้อในประเทศ"),
    (r"competition|promotion|discount", "การแข่งขันและการส่งเสริมการขาย"),
    (r"new store|new branch|branch expansion|outlet|retail shop|store expansion", "การขยายสาขาและช่องทางจำหน่าย"),
    (r"new product|product launch|innovation", "การออกผลิตภัณฑ์ใหม่"),
    (r"capacity|new plant|new factory|production line|machinery", "กำลังการผลิตและเครื่องจักรใหม่"),
    (r"depreciation|amortization", "ค่าเสื่อมราคาและค่าตัดจำหน่าย"),
    (r"impairment|write[- ]off|write down", "รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์"),
    (r"fair[- ]value|fair value", "กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม"),
    (r"disposal|asset sale|sale of investment", "กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์"),
    (r"associate|joint venture|\bjv\b|equity income|share of profit|share of loss", "ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า"),
    (r"finance cost|interest expense|borrowing cost", "ต้นทุนทางการเงิน"),
    (r"tax expense|income tax|global minimum tax", "ค่าใช้จ่ายภาษี"),
    (r"sg&a|selling expense|administrative expense|administration cost|overhead", "ค่าใช้จ่ายขายและบริหาร"),
    (r"dividend income", "รายได้เงินปันผล"),
    (r"insurance compensation|insurance claim", "ค่าสินไหมทดแทนจากประกันภัย"),
    (r"inventory|receivable|working capital", "เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้"),
    (r"debt|leverage|d/e", "ภาระหนี้และโครงสร้างเงินทุน"),
    (r"capex|capital expenditure|investment cycle", "การลงทุนและรายจ่ายลงทุน"),
    (r"acquisition|consolidat|business combination", "การซื้อกิจการและการรวมงบการเงิน"),
    (r"discontinued operation|discontinued line", "การยุติธุรกิจหรือสายผลิตภัณฑ์"),
    (r"hotel|occupancy|room rate|tourism|revpar", "การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก"),
    (r"industrial land|land sale|land transfer|industrial estate", "ยอดขายและการโอนที่ดินนิคมอุตสาหกรรม"),
    (r"residential|housing|condominium|low[- ]rise|property transfer|presales", "ยอดขายและการโอนโครงการที่อยู่อาศัย"),
    (r"mortgage|bank lending|household debt|loan rejection", "สินเชื่อที่อยู่อาศัยที่เข้มงวดและหนี้ครัวเรือน"),
    (r"rental|rent income|lease income|leasing|occupancy rate", "รายได้ค่าเช่าและอัตราการเช่าพื้นที่"),
    (r"power revenue|electricity|\bft\b|adder|solar|spp", "รายได้และเงื่อนไขของธุรกิจไฟฟ้า"),
    (r"weather|rainfall|drought|flood|heat", "สภาพอากาศและฤดูกาล"),
]


THAI_TERM_REPLACEMENTS = (
    ("gross margin", "อัตรากำไรขั้นต้น"), ("fair-value gain", "กำไรจากการวัดมูลค่ายุติธรรม"),
    ("fair value gain", "กำไรจากการวัดมูลค่ายุติธรรม"), ("fair-value loss", "ขาดทุนจากการวัดมูลค่ายุติธรรม"),
    ("fair value loss", "ขาดทุนจากการวัดมูลค่ายุติธรรม"), ("fair value", "มูลค่ายุติธรรม"),
    ("impairment", "การด้อยค่า"), ("low-rise", "โครงการแนวราบ"),
    ("community mall", "ศูนย์การค้าชุมชน"), ("senior care", "ธุรกิจดูแลผู้สูงอายุ"),
    ("headline", "ตัวเลขรายงาน"), ("primary filing", "เอกสารหลัก"),
    ("secondary synthesis", "บทวิเคราะห์จากแหล่งข้อมูลรอง"), ("filing", "เอกสารที่ยื่นต่อตลาดหลักทรัพย์"),
    ("margin", "อัตรากำไร"), ("biosecurity", "มาตรการความปลอดภัยทางชีวภาพ"),
    ("SET 01 Sale", "รายการขาย SET 01"), ("foodservice", "ช่องทางบริการอาหาร"),
    ("modern trade", "ช่องทางค้าปลีกสมัยใหม่"), ("premium product mix", "สัดส่วนสินค้าพรีเมียม"),
    ("product mix", "ส่วนผสมผลิตภัณฑ์"), ("revenue mix", "ส่วนผสมรายได้"),
    ("sales mix", "ส่วนผสมยอดขาย"), ("negative operating leverage", "ผลลบจากต้นทุนคงที่เมื่อยอดขายลดลง"),
    ("operating leverage", "ผลของต้นทุนคงที่ต่อกำไร"),
    ("transformation", "การปรับโครงสร้าง"), ("hedging", "การป้องกันความเสี่ยง"),
    ("food cost", "ต้นทุนอาหาร"), ("productivity", "ประสิทธิภาพต่อสาขา"),
    ("write-off", "การตัดจำหน่าย"), ("economics", "ความคุ้มค่าทางเศรษฐศาสตร์"),
    ("format", "รูปแบบร้าน"), ("customer brand", "แบรนด์ของลูกค้า"),
    ("momentum", "แนวโน้ม"), ("traffic", "จำนวนผู้ใช้บริการ"),
    ("occupancy", "อัตราการเช่าพื้นที่"), ("finance lease", "สัญญาเช่าการเงิน"),
    ("backlog", "ยอดขายรอโอน"), ("promotion", "การส่งเสริมการขาย"),
    ("canonical", "คลังข้อมูลหลัก"), ("profit bridge", "การแจกแจงสาเหตุกำไร"),
    ("data centre", "ศูนย์ข้อมูล"), ("data center", "ศูนย์ข้อมูล"),
    ("supply chain", "ห่วงโซ่อุปทาน"), ("mobility", "ธุรกิจโมบิลิตี้"),
    ("pipeline", "อุปสงค์ในมือ"), ("core bridge", "การกระทบยอดกำไรหลัก"),
    ("fair-value", "มูลค่ายุติธรรม"), ("commercial", "ธุรกิจพาณิชย์"),
    ("zinc oxide", "ซิงก์ออกไซด์"), ("mix", "ส่วนผสมธุรกิจ"),
)


def _normalize_thai(text: str) -> str:
    value = str(text or "")
    for english, thai in THAI_TERM_REPLACEMENTS:
        value = re.sub(re.escape(english), thai, value, flags=re.I)
    value = re.sub(r"\s+", " ", value).replace(" ;", ";").strip()
    return value


def _auto_causes(text: str) -> list[str]:
    value = str(text or "")
    causes = []
    for pattern, label in AUTO_CAUSE_RULES:
        if re.search(pattern, value, flags=re.I) and label not in causes:
            causes.append(label)
    return causes[:4]


def _fmt_mb(value) -> str:
    number = _num(value)
    if number is None:
        return "ไม่ปรากฏตัวเลขที่เปรียบเทียบได้"
    return f"{number:,.0f} ลบ." if abs(number) >= 100 else f"{number:,.1f} ลบ."


def _change_phrase(value) -> str:
    number = _num(value)
    if number is None:
        return "ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้"
    if abs(number) < 0.05:
        return "ทรงตัว YoY"
    return f"{'เพิ่ม' if number > 0 else 'ลด'} {abs(number):.1f}% YoY"


def _thai_metric_sentence(company: dict, category: str) -> str:
    if category == "rfo":
        return f"RFO ปี 2568 อยู่ที่ {_fmt_mb(company.get('fy2025_rfo_mb'))} {_change_phrase(company.get('rfo_yoy_pct'))}"
    current = _fmt_mb(company.get("fy2025_npat_owners_mb"))
    prior = _fmt_mb(company.get("fy2024_npat_owners_mb"))
    state = company.get("npat_state")
    if state == "turned_to_profit":
        return f"กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร {current} จากขาดทุน {prior}"
    if state == "turned_to_loss":
        return f"กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน {current} จากกำไร {prior}"
    if state == "loss_narrowed":
        return f"ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ {current} จาก {prior}"
    if state == "loss_widened":
        return f"ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น {current} จาก {prior}"
    return f"กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ {current} {_change_phrase(company.get('npat_yoy_pct_positive_base_only'))}"


def _auto_bilingual(company: dict, text: str, category: str, evidence: dict | None = None) -> dict:
    causes = _auto_causes(text)
    source_label = "MD&A" if evidence else "แหล่งข้อมูลรอง"
    if _contains_thai(text):
        excerpt = _clean(text)[:560]
        if category == "special":
            thai = f"รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: {excerpt}"
        else:
            thai = f"{_thai_metric_sentence(company, category)}; MD&A ระบุว่า {excerpt}"
    elif category == "special":
        thai = ("รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: " + " และ ".join(causes)) if causes else "เอกสารที่มีอยู่ยังไม่ระบุรายการพิเศษหรือรายการต่ำกว่าการดำเนินงานอย่างชัดเจน"
    else:
        bridge = " และ ".join(causes) if causes else "เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน"
        thai = f"{_thai_metric_sentence(company, category)}; ปัจจัยที่{source_label}ระบุ ได้แก่ {bridge}"
    result = bi(text, _normalize_thai(thai))
    result["claimBasis"] = "direct_mda_excerpt" if evidence else "secondary_synthesis"
    if evidence:
        result["evidence"] = evidence
    return result


def _claim_evidence_score(item: dict, passage: dict) -> float:
    claim = f"{item.get('en', '')} {item.get('th', '')}".lower()
    source = passage["text"].lower()
    stop = {"the", "and", "from", "with", "that", "this", "while", "after", "because", "under", "into", "ส่วน", "จาก", "และ", "ของ", "ที่", "เมื่อ"}
    claim_words = {word for word in re.findall(r"[a-z\u0E00-\u0E7F]+", claim) if len(word) >= 3 and word not in stop}
    source_words = {word for word in re.findall(r"[a-z\u0E00-\u0E7F]+", source) if len(word) >= 3 and word not in stop}
    overlap = len(claim_words & source_words)
    claim_numbers = set(re.findall(r"\d+(?:[.,]\d+)?", claim))
    source_numbers = set(re.findall(r"\d+(?:[.,]\d+)?", source))
    number_overlap = len(claim_numbers & source_numbers)
    phrase_overlap = sum(1 for phrase in ("gross margin", "net profit", "joint venture", "share of profit", "tax expense", "boi", "earthquake", "service revenue", "low-rise", "domestic sales", "international sales") if phrase in claim and phrase in source)
    return overlap + 5 * number_overlap + 4 * phrase_overlap + 0.03 * float(passage.get("score", 0))


def _attach_evidence(items: list[dict], path: Path | None, passages: list[dict], category: str) -> list[dict]:
    output = copy.deepcopy(items)
    unused = list(range(len(passages)))
    for item in output:
        if path and passages:
            pool = unused or list(range(len(passages)))
            best = max(pool, key=lambda index: _claim_evidence_score(item, passages[index]))
            passage = passages[best]
            if best in unused:
                unused.remove(best)
            item["evidence"] = _source_evidence(path, passage, category)
            item["claimBasis"] = "mda_backed_synthesis"
        else:
            item["claimBasis"] = "secondary_synthesis"
    return output


def _num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def materiality(company: dict, role_tickers: set[str]) -> str:
    rfo = _num(company.get("rfo_yoy_pct")); npat = _num(company.get("npat_yoy_pct_positive_base_only"))
    drfo = _num(company.get("rfo_change_mb")); dnpat = _num(company.get("npat_change_mb"))
    state = company.get("npat_state")
    high = (state in {"turned_to_profit", "turned_to_loss", "loss_narrowed", "loss_widened"}
            or (rfo is not None and abs(rfo) >= 20) or (npat is not None and abs(npat) >= 50)
            or (drfo is not None and abs(drfo) >= 1000) or (dnpat is not None and abs(dnpat) >= 500))
    if high:
        return "high"
    if company.get("ticker") in role_tickers or (rfo is not None and abs(rfo) >= 10) or (npat is not None and abs(npat) >= 25):
        return "medium"
    return "standard"


def source_url(path: Path | None) -> str | None:
    if not path:
        return None
    head = path.read_text(encoding="utf-8", errors="ignore")[:5000]
    match = re.search(r"(?m)^source_url:\s*[\"']?([^\"'\r\n]+)", head)
    return match.group(1).strip() if match else None


def build_driver(company: dict, report: dict, mda_path: Path | None, role_tickers: set[str]) -> dict:
    ticker = company["ticker"]
    curated = CURATED.get(ticker) or {}
    annual = _annual_items(report or {})
    status = mda_source_status(mda_path)
    primary = status == "primary_verified"
    rfo_passages = _mda_candidates(mda_path, "rfo", 20)
    npat_passages = _mda_candidates(mda_path, "npat", 20)
    special_passages = _mda_candidates(mda_path, "special", 8)
    used_secondary = False

    if curated.get("rfo"):
        rfo = _attach_evidence(curated["rfo"], mda_path if primary else None, rfo_passages, "rfo")
    else:
        rfo = [_auto_bilingual(company, passage["text"], "rfo", _source_evidence(mda_path, passage, "rfo"))
               for passage in rfo_passages] if mda_path else []
    if not rfo:
        candidates = _best(annual, "rfo")
        rfo = [_auto_bilingual(company, item, "rfo") for item in candidates[:2]]
        used_secondary = bool(rfo)

    if curated.get("npat"):
        npat = _attach_evidence(curated["npat"], mda_path if primary else None, npat_passages, "npat")
    else:
        npat = [_auto_bilingual(company, passage["text"], "npat", _source_evidence(mda_path, passage, "npat"))
                for passage in npat_passages] if mda_path else []
    if not npat:
        candidates = _best(annual, "npat")
        npat = [_auto_bilingual(company, item, "npat") for item in candidates[:2]]
        used_secondary = used_secondary or bool(npat)

    if curated.get("special"):
        special = _attach_evidence(curated["special"], mda_path if primary else None, special_passages, "special")
    else:
        special = [_auto_bilingual(company, passage["text"], "special", _source_evidence(mda_path, passage, "special"))
                   for passage in special_passages] if mda_path else []
    if not special and not primary:
        special_items = [item for item in annual if SPECIAL_RE.search(item)]
        special = [_auto_bilingual(company, item, "special") for item in special_items[:2]]
        used_secondary = used_secondary or bool(special)

    if not rfo:
        item = bi("No claim-level FY2025 revenue cause is available from the primary source.", "ยังไม่มีข้อความในเอกสารต้นทางที่อธิบายสาเหตุการเปลี่ยนแปลงของ RFO ปี 2568 ได้โดยตรง")
        item["claimBasis"] = "source_gap"
        rfo = [item]
    if not npat:
        item = bi("No claim-level FY2025 owner-profit cause is available from the primary source.", "ยังไม่มีข้อความในเอกสารต้นทางที่อธิบายสาเหตุการเปลี่ยนแปลงของกำไรส่วนผู้ถือหุ้นปี 2568 ได้โดยตรง")
        item["claimBasis"] = "source_gap"
        npat = [item]

    for item in rfo + npat + special:
        item["th"] = _normalize_thai(item.get("th", ""))
    evidence_count = sum(bool(item.get("evidence")) for item in rfo + npat + special)
    source_ids = ["FY_PANEL"]
    if mda_path:
        source_ids.append(f"MDA_{ticker}_FY2025")
    if used_secondary or not primary:
        source_ids.append("COMPANY_REPORTS")
    if primary and used_secondary:
        basis = "mixed_mda_and_secondary"
    elif primary and curated:
        basis = "mda_backed_synthesis"
    elif primary:
        basis = "mda_direct_extraction"
    else:
        basis = "secondary_synthesis_source_gap"
    return {
        "period": "FY2025 vs FY2024",
        "materiality": materiality(company, role_tickers),
        "basis": basis,
        "sourceStatus": status,
        "primaryMdaAvailable": primary,
        "hasClaimLevelEvidence": evidence_count > 0,
        "evidenceCoverage": {
            "rfo": sum(bool(item.get("evidence")) for item in rfo),
            "npat": sum(bool(item.get("evidence")) for item in npat),
            "special": sum(bool(item.get("evidence")) for item in special),
        },
        "rfoDrivers": rfo[:3],
        "npatDrivers": npat[:4],
        "specialItems": special[:2],
        "sourceIds": list(dict.fromkeys(source_ids)),
    }


def load_reports(repo_root: Path) -> tuple[dict, Path]:
    path = repo_root / "data" / "company-reports.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("reports", {}), path


def find_mda(vault_root: Path, ticker: str) -> Path | None:
    root = vault_root / "Listed Company" / "1-Raw" / "01-Filings" / "MDA"
    candidates = sorted(root.rglob(f"MDA_{ticker}_2025FY_[ET].md"))
    if not candidates:
        return None

    def rank(path: Path) -> tuple:
        status = mda_source_status(path)
        language = 1 if path.stem.endswith("_T") else 0
        return (1 if status == "primary_verified" else 0, language, path.stat().st_size)

    return max(candidates, key=rank)
