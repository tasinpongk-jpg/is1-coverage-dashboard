# บทวิเคราะห์รายกลุ่ม — IS1 Coverage Desk

_Interactive briefing สำหรับนำเสนอในที่ประชุม RM_

ข้อมูลตลาด ณ 7 ส.ค. 2569 • FY2025 vs FY2024  
ขอบเขต: FOOD and PROP; audited primary-segment perimeter  
QA: PASS (43 pass / 0 fail) · สร้างเมื่อ: 2026-08-10T08:01:17+00:00  
`schemaVersion 4` · ที่มา: data/sector-intelligence.json

> Facts, management explanations, analyst inferences and analyst tests are explicitly separated. Price/valuation explanations are inference, not proof of causality. MD&A source exceptions are surfaced per company.

## สารบัญ

- [FOOD — FOOD: กำไรฟื้น แต่กระจุกในโปรตีนสัตว์](#food--food-กำไรฟื้น-แต่กระจุกในโปรตีนสัตว์)
  - [F1 · โปรตีนสัตว์ครบวงจร — กำไรฟื้นชัด แต่ตลาดยังให้ส่วนลดแบบหุ้นวัฏจักร](#f1--โปรตีนสัตว์ครบวงจร--กำไรฟื้นชัด-แต่ตลาดยังให้ส่วนลดแบบหุ้นวัฏจักร)
  - [F4 · เครื่องดื่มแบรนด์ — กำไรที่โตจาก margin ช่วยรองรับ premium ของแบรนด์](#f4--เครื่องดื่มแบรนด์--กำไรที่โตจาก-margin-ช่วยรองรับ-premium-ของแบรนด์)
  - [F6 · อาหารหลัก ขนม และเบเกอรี่ — ขนาดและความ defensive ช่วยพยุง valuation แต่กำไรอ่อนลง](#f6--อาหารหลัก-ขนม-และเบเกอรี่--ขนาดและความ-defensive-ช่วยพยุง-valuation-แต่กำไรอ่อนลง)
  - [F2 · อาหารทะเลและเพาะเลี้ยง — ราคาปรับดีขึ้นแม้ผลประกอบการ FY2025 ยังถูกกดดัน](#f2--อาหารทะเลและเพาะเลี้ยง--ราคาปรับดีขึ้นแม้ผลประกอบการ-fy2025-ยังถูกกดดัน)
  - [F3 · อาหารสัตว์เลี้ยง — รายได้เชิงโครงสร้างยังโต แต่การแปลงเป็นกำไรอ่อนลง](#f3--อาหารสัตว์เลี้ยง--รายได้เชิงโครงสร้างยังโต-แต่การแปลงเป็นกำไรอ่อนลง)
  - [F8 · น้ำตาล แป้ง และน้ำมันบริโภค — งวดปฏิทินอ่อนตัว และมุมทุกปีบัญชีแย่กว่าชัดเจน](#f8--น้ำตาล-แป้ง-และน้ำมันบริโภค--งวดปฏิทินอ่อนตัว-และมุมทุกปีบัญชีแย่กว่าชัดเจน)
  - [F5 · ร้านอาหารและบริการอาหาร — อุปสงค์ร้านอาหารอ่อนแอ และกำไรส่วนผู้ถือหุ้นของกลุ่มที่ map แล้วลดเร็วกกว่า RFO](#f5--ร้านอาหารและบริการอาหาร--อุปสงค์ร้านอาหารอ่อนแอ-และกำไรส่วนผู้ถือหุ้นของกลุ่มที่-map-แล้วลดเร็วกกว่า-rfo)
  - [F7 · วัตถุดิบและเครื่องปรุง — รายได้หดตัว แต่ขาดทุน NRF ที่ลดลงช่วยยกกำไรส่วนผู้ถือหุ้น](#f7--วัตถุดิบและเครื่องปรุง--รายได้หดตัว-แต่ขาดทุน-nrf-ที่ลดลงช่วยยกกำไรส่วนผู้ถือหุ้น)
  - [F9 · เกษตรแปรรูปและธุรกิจหลากหลาย — กลุ่มที่สอบทานแล้วพลิกเป็นขาดทุน และ P/E headline ไม่เป็นตัวแทน](#f9--เกษตรแปรรูปและธุรกิจหลากหลาย--กลุ่มที่สอบทานแล้วพลิกเป็นขาดทุน-และ-pe-headline-ไม่เป็นตัวแทน)
- [PROP — PROP: รายได้ประจำส่งมอบกำไร ขณะที่ FDI optionality ขับเคลื่อนความคาดหวัง](#prop--prop-รายได้ประจำส่งมอบกำไร-ขณะที่-fdi-optionality-ขับเคลื่อนความคาดหวัง)
  - [P3 · ศูนย์การค้าและรายได้ประจำ — รายได้ประจำส่งมอบความสอดคล้องของกำไรและราคาชัดที่สุด](#p3--ศูนย์การค้าและรายได้ประจำ--รายได้ประจำส่งมอบความสอดคล้องของกำไรและราคาชัดที่สุด)
  - [P1 · ที่อยู่อาศัยเพื่อขาย — ข้อจำกัดสินเชื่อกดดันผลประกอบการในวงกว้าง](#p1--ที่อยู่อาศัยเพื่อขาย--ข้อจำกัดสินเชื่อกดดันผลประกอบการในวงกว้าง)
  - [P2 · นิคมอุตสาหกรรมและโลจิสติกส์ — FDI optionality ผลักราคานำกำไรรายงาน](#p2--นิคมอุตสาหกรรมและโลจิสติกส์--fdi-optionality-ผลักราคานำกำไรรายงาน)
  - [P4 · โรงแรมและมิกซ์ยูส — AWC ส่งมอบการเติบโต แต่ด้อยค่าของ S ฉุดภาพรวม](#p4--โรงแรมและมิกซ์ยูส--awc-ส่งมอบการเติบโต-แต่ด้อยค่าของ-s-ฉุดภาพรวม)
  - [P5 · กระจายธุรกิจและปรับโครงสร้าง — กลุ่มที่ปรับใหม่ยังขาดทุน แต่ขาดทุนลดลง](#p5--กระจายธุรกิจและปรับโครงสร้าง--กลุ่มที่ปรับใหม่ยังขาดทุน-แต่ขาดทุนลดลง)

---

## FOOD — FOOD: กำไรฟื้น แต่กระจุกในโปรตีนสัตว์

โปรตีนสัตว์และเครื่องดื่มส่งมอบกำไรที่ดีขึ้น ขณะที่หลายกลุ่มราคาปรับขึ้นนำผลประกอบการ FY2025

1. F1 ใหญ่ที่สุดและเป็นการฟื้นที่กำไรยืนยันชัดที่สุด
2. F7, F5, F3 และ F8 ต้องใช้ความคาดหวังล่วงหน้าอธิบายราคา
3. F9 ยังเป็น outlier ที่ขาดทุนและ P/E headline ไม่เป็นตัวแทน

### กรอบการตัดสินใจ 3 มุมมอง

| มุมมอง | ตัวชี้วัด | ค่า | ครอบคลุม |
|---|---|---|---|
| 01 โครงสร้างตลาด | Market cap | THB 812bn | 58/58 มีข้อมูล |
|  | บริษัท | 58 |  |
|  | Segment ใหญ่สุด | F1 · 34.8% |  |
| 02 ผลประกอบการ FY2025 | RFO YoY | -0.9% | 55/58 |
|  | NPAT YoY | +14.9% | 56/58 |
|  | Segment ที่กำไรยืนยัน | 1/9 |  |
| 03 มุมมองตลาด | ราคา YTD ปรับแล้ว | +10.2% | 58/58 · 100.0% M-cap |
|  | P/E รวม | 11.2x | 43/58 · 96.7% M-cap |
|  | Segment ราคานำ | 3/9 |  |

FY2025 RFO THB 1.26tn (FY2024 THB 1.27tn) • FY2025 owner NPAT THB 70.7bn (FY2024 THB 61.5bn) • Margin 5.7% (FY2024 4.9%)

### ภาพรวมเชิงกราฟ

#### 01 · โครงสร้างตลาด — สัดส่วน Market Cap

_ขนาด Segment และผู้นำตลาด_

| Segment | สัดส่วน | Market cap | ผู้นำ |
|---|---|---|---|
| F1 โปรตีนสัตว์ครบวงจร | 34.8% | THB 282bn | CPF · 63% |
| F4 เครื่องดื่มแบรนด์ | 19.3% | THB 157bn | OSP · 34% |
| F6 อาหารหลัก ขนม และเบเกอรี่ | 15.3% | THB 124bn | TFMAMA · 50% |
| F2 อาหารทะเลและเพาะเลี้ยง | 8.2% | THB 66.9bn | TU · 85% |
| F3 อาหารสัตว์เลี้ยง | 7.6% | THB 61.6bn | ITC · 86% |
| F8 น้ำตาล แป้ง และน้ำมันบริโภค | 6.8% | THB 54.9bn | TVO · 44% |
| F5 ร้านอาหารและบริการอาหาร | 3.6% | THB 29.2bn | M · 67% |
| F7 วัตถุดิบและเครื่องปรุง | 3.3% | THB 26.8bn | SAUCE · 56% |
| F9 เกษตรแปรรูปและธุรกิจหลากหลาย | 1.2% | THB 9.4bn | SUN · 21% |

#### 02 · ผลประกอบการ FY2025 — ทิศทาง RFO และ NPAT ส่วนผู้ถือหุ้น

_FY2025 YoY_

| Segment | RFO YoY | RFO FY2025 | NPAT YoY | NPAT FY2025 |
|---|---|---|---|---|
| F1 โปรตีนสัตว์ครบวงจร | +0.8% | THB 785bn | +54.2% | THB 40.3bn |
| F4 เครื่องดื่มแบรนด์ | -3.3% | THB 87.0bn | +7.8% | THB 9.3bn |
| F6 อาหารหลัก ขนม และเบเกอรี่ | 0.0% | THB 71.2bn | -14.3% | THB 8.3bn |
| F2 อาหารทะเลและเพาะเลี้ยง | -3.3% | THB 160bn | -14.3% | THB 5.1bn |
| F3 อาหารสัตว์เลี้ยง | +2.6% | THB 25.2bn | -19.2% | THB 3.7bn |
| F8 น้ำตาล แป้ง และน้ำมันบริโภค | -7.0% | THB 74.0bn | -21.0% | THB 4.1bn |
| F5 ร้านอาหารและบริการอาหาร | -4.2% | THB 28.9bn | -76.6% | THB 189m |
| F7 วัตถุดิบและเครื่องปรุง | -7.0% | THB 11.5bn | +311.9% | THB 700m |
| F9 เกษตรแปรรูปและธุรกิจหลากหลาย | -9.8% | THB 17.3bn | ขาดทุน | −THB 914m |

#### 03 · มุมมองตลาด — ราคาเทียบกับทิศทางกำไร

_NPAT YoY เทียบกับราคา YTD_

| Segment | NPAT YoY | ราคา YTD | Market cap | ควอดรันต์ |
|---|---|---|---|---|
| F1 โปรตีนสัตว์ครบวงจร | +54.2% | +13.6% | 34.8% | ราคาและกำไรตอบรับ |
| F4 เครื่องดื่มแบรนด์ | +7.8% | +13.1% | 19.3% | ราคาและกำไรตอบรับ |
| F6 อาหารหลัก ขนม และเบเกอรี่ | -14.3% | -0.2% | 15.3% | ราคาและกำไรถูกกดดัน |
| F2 อาหารทะเลและเพาะเลี้ยง | -14.3% | +6.0% | 8.2% | ราคานำ • กำไรยังไม่ยืนยัน |
| F3 อาหารสัตว์เลี้ยง | -19.2% | +14.0% | 7.6% | ราคานำ • กำไรยังไม่ยืนยัน |
| F8 น้ำตาล แป้ง และน้ำมันบริโภค | -21.0% | +12.1% | 6.8% | ราคานำ • กำไรยังไม่ยืนยัน |
| F5 ร้านอาหารและบริการอาหาร | -76.6% | +6.2% | 3.6% | ราคานำ • กำไรยังไม่ยืนยัน |
| F7 วัตถุดิบและเครื่องปรุง | +311.9% | +25.6% | 3.3% | ราคาและกำไรตอบรับ |
| F9 เกษตรแปรรูปและธุรกิจหลากหลาย | — | -10.4% | 1.2% | — |

#### 04 · มูลค่า — P/E รวมของบริษัทที่มีกำไร

_แสดงความครอบคลุมของข้อมูลควบคู่ทุกค่า_

| Segment | P/E | ครอบคลุม |
|---|---|---|
| F1 โปรตีนสัตว์ครบวงจร | 7.8x | 6/6 • 100% M-cap |
| F4 เครื่องดื่มแบรนด์ | 17.2x | 8/9 • 99% M-cap |
| F6 อาหารหลัก ขนม และเบเกอรี่ | 15.5x | 9/9 • 100% M-cap |
| F2 อาหารทะเลและเพาะเลี้ยง | 10.9x | 4/5 • 99% M-cap |
| F3 อาหารสัตว์เลี้ยง | 15.7x | 2/2 • 100% M-cap |
| F8 น้ำตาล แป้ง และน้ำมันบริโภค | 9.8x | 6/9 • 72% M-cap |
| F5 ร้านอาหารและบริการอาหาร | 23.6x | 3/6 • 89% M-cap |
| F7 วัตถุดิบและเครื่องปรุง | 19.3x | 3/4 • 99% M-cap |
| F9 เกษตรแปรรูปและธุรกิจหลากหลาย | 12.7x | 2/8 • 36% M-cap |

### แผนที่ Segment เรียงตาม Market Cap

_เรียงจากใหญ่ไปเล็ก_

| อันดับ | Segment | M-cap | RFO YoY | NPAT YoY | ราคา YTD | P/E | ผู้นำ | สัญญาณ |
|---|---|---|---|---|---|---|---|---|
| 1 | F1 โปรตีนสัตว์ครบวงจร (6 บริษัท) | 34.8% (6/6) | +0.8% (6/6) | +54.2% (6/6) | +13.6% (6/6 • 100% M-cap) | 7.8x (6/6 • 100% M-cap) | CPF · 63% | กำไรยืนยันราคา |
| 2 | F4 เครื่องดื่มแบรนด์ (9 บริษัท) | 19.3% (9/9) | -3.3% (9/9) | +7.8% (9/9) | +13.1% (9/9 • 100% M-cap) | 17.2x (8/9 • 99% M-cap) | OSP · 34% | ราคานำพื้นฐาน |
| 3 | F6 อาหารหลัก ขนม และเบเกอรี่ (9 บริษัท) | 15.3% (9/9) | 0.0% (9/9) | -14.3% (9/9) | -0.2% (9/9 • 100% M-cap) | 15.5x (9/9 • 100% M-cap) | TFMAMA · 50% | ยังถูกกดดัน |
| 4 | F2 อาหารทะเลและเพาะเลี้ยง (5 บริษัท) | 8.2% (5/5) | -3.3% (5/5) | -14.3% (5/5) | +6.0% (5/5 • 100% M-cap) | 10.9x (4/5 • 99% M-cap) | TU · 85% | ยังถูกกดดัน |
| 5 | F3 อาหารสัตว์เลี้ยง (2 บริษัท) | 7.6% (2/2) | +2.6% (2/2) | -19.2% (2/2) | +14.0% (2/2 • 100% M-cap) | 15.7x (2/2 • 100% M-cap) | ITC · 86% | ราคานำพื้นฐาน |
| 6 | F8 น้ำตาล แป้ง และน้ำมันบริโภค (9 บริษัท) | 6.8% (9/9) | -7.0% (7/9) | -21.0% (7/9) | +12.1% (9/9 • 100% M-cap) | 9.8x (6/9 • 72% M-cap) | TVO · 44% | ยังถูกกดดัน |
| 7 | F5 ร้านอาหารและบริการอาหาร (6 บริษัท) | 3.6% (6/6) | -4.2% (5/6) | -76.6% (6/6) | +6.2% (6/6 • 100% M-cap) | 23.6x (3/6 • 89% M-cap) | M · 67% | ยังถูกกดดัน |
| 8 | F7 วัตถุดิบและเครื่องปรุง (4 บริษัท) | 3.3% (4/4) | -7.0% (4/4) | +311.9% (4/4) | +25.6% (4/4 • 100% M-cap) | 19.3x (3/4 • 99% M-cap) | SAUCE · 56% | ราคานำพื้นฐาน |
| 9 | F9 เกษตรแปรรูปและธุรกิจหลากหลาย (8 บริษัท) | 1.2% (8/8) | -9.8% (8/8) | ขาดทุน (8/8) | -10.4% (8/8 • 100% M-cap) | 12.7x (2/8 • 36% M-cap) | SUN · 21% | ยังถูกกดดัน |

### บทวิเคราะห์รายกลุ่มย่อย

### F1 · โปรตีนสัตว์ครบวงจร — กำไรฟื้นชัด แต่ตลาดยังให้ส่วนลดแบบหุ้นวัฏจักร

`กำไรยืนยันราคา` · 34.8% M-cap · THB 282bn · 6 บริษัท

| ตัวชี้วัด | RFO | NPAT | ราคา | P/E |
|---|---|---|---|---|
| ช่วง | FY2025 YoY | ส่วนผู้ถือหุ้น FY2025 YoY | ราคา YTD ปรับแล้ว | เฉพาะบริษัทที่มีกำไร |
| ค่า | +0.8% | +54.2% | +13.6% | 7.8x |
| จำนวน | THB 785bn FY2025 | THB 40.3bn FY2025 | ณ 7 ส.ค. 2569 | ค่าเฉลี่ยรวม |
| ครอบคลุม | 6/6 | 6/6 | 6/6 • 100% M-cap | 6/6 • 100% M-cap |

**ข้อเท็จจริงที่สังเกตได้** — FY2025: RFO +0.8% • NPAT +54.2% • ราคา YTD +13.6% • P/E 7.8x • ครอบคลุม RFO 6/6 • NPAT 6/6

#### เหตุผลที่เปลี่ยน

1. _ข้อเท็จจริงจากการคำนวณ_ · ราคาสัตว์ **↑** — FY2025 RFO เกือบทรงตัว (+0.8%) ขณะที่ NPAT ส่วนผู้ถือหุ้นเพิ่ม 54.2% จึงเป็นการฟื้นจาก margin
2. _คำอธิบายฝ่ายจัดการ_ · ต้นทุนอาหารสัตว์ / ถั่วเหลือง **↓** — CPF ระบุปัจจัยจากการควบคุมต้นทุน ต้นทุนกากถั่วเหลืองลดลง biosecurity และราคาสุกรสูงขึ้น
3. _ข้อเท็จจริงจากการคำนวณ_ · Margin **5.1%** — TFG และ BTG ทำให้การฟื้นกระจายออกจาก CPF ตามการคำนวณ panel ที่สอบทาน
4. _ข้ออนุมานนักวิเคราะห์_ · NPAT **+54.2%** — ข้อสรุปกลุ่มผสานการคำนวณ panel ที่สอบทานกับ MD&A รายบริษัท ไม่ใช่หลักฐานเหตุเชิงสาเหตุจากบริษัทเดียว

#### ห่วงโซ่เหตุและผล

**ราคาสัตว์** (↑ แรงหนุนการฟื้นตัว) → **ต้นทุนอาหารสัตว์ / ถั่วเหลือง** (↓ ต้นทุนเอื้อต่อกำไร) → **Margin** (5.1% +1.8 ppt YoY) → **NPAT** (+54.2% THB 40.3bn FY2025) → **Valuation** (7.8x YTD +13.6%)

#### บทบาทในกลุ่ม

| บทบาท | Ticker | ค่า | ที่มาของค่า |
|---|---|---|---|
| ผู้นำ | CPF | 63% | สัดส่วน Market Cap ในกลุ่ม |
| ตัวเพิ่ม RFO | BTG | +7.1% | RFO YoY · Δ +8.1bn |
| ดาวรุ่ง | TFG | +114.1% | ราคา YTD ปรับแล้ว |

#### มูลค่า

**กำไรที่เกิดขึ้นแล้ว / ข้อเท็จจริง** — P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 7.8x ครอบคลุม 6/6 บริษัท และ 100.0% ของ market cap ที่มีข้อมูล. ส่วนลดวัฏจักรสะท้อนความเสี่ยงสินค้าโภคภัณฑ์และการกลับทิศ

| Trigger | Risk |
|---|---|
| ราคาหมูและไก่ยืนเหนือแรงกดดันต้นทุนอาหารสัตว์ | โรคระบาดสัตว์หรืออุปทานล้นตลาด |
| อุปสงค์ส่งออกและการบริโภคในประเทศยังแข็งแรง | ต้นทุนอาหารสัตว์กลับมาสูงขึ้น |
| วินัยด้าน margin ต่อเนื่องถึง 6M26 | ความผันผวนด้านส่งออกและค่าเงิน |

**6M26 ต้องพิสูจน์** — 6M26 ต้องพิสูจน์ว่า margin ที่ฟื้นตัวอยู่ได้แม้ฐานวัฏจักรเอื้อประโยชน์น้อยลง

#### วิเคราะห์รายบริษัท — F1 โปรตีนสัตว์ครบวงจร

_ทุกบริษัทใน perimeter ของ Segment ที่สอบทาน_

| Ticker | บทบาท | M-cap | RFO YoY | NPAT YoY | ราคา YTD | P/E | Margin |
|---|---|---|---|---|---|---|---|
| CPF | ผู้นำ | THB 178bn | -1.7% | +28.8% | -0.9% | 8.2x | 4.4% |
| TFG | ดาวรุ่ง | THB 56.7bn | +11.2% | +136.7% | +114.1% | 7.6x | 10.2% |
| BTG | ตัวเพิ่ม RFO | THB 40.4bn | +7.1% | +171.1% | +14.8% | 6.9x | 5.5% |
| FM | บริษัทในกลุ่ม | THB 4.2bn | -2.7% | -3.9% | +19.0% | 6.1x | 9.4% |
| BR | บริษัทในกลุ่ม | THB 1.8bn | +2.0% | +16.5% | +22.1% | 9.9x | 1.9% |
| SORKON | บริษัทในกลุ่ม | THB 1.1bn | +4.7% | +1.3% | -1.7% | 14.5x | 3.8% |

##### CPF — ผู้นำ · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เจริญโภคภัณฑ์อาหาร จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัทประกอบธุรกิจเกษตรอุตสาหกรรมและอาหารที่จำแนกธุรกิจหลักตามลักษณะของผลิตภัณฑ์ ออกเป็น 3 ประเภท คือ 1) ธุรกิจอาหารสัตว์ (Feed) ได้แก่ การผลิตและจำหน่ายอาหารสัตว์ 2) ธุรกิจเลี้ยงสัตว์-แปรรูป (Farm-Processing) ได้แก่ การเพาะพันธุ์สัตว์ การเลี้ยงสัตว์เพื่อการค้า และการแปรรูปเนื้อสัตว์ขั้นพื้นฐาน 3) ธุรกิจอาหาร (Food) ได้แก่ การผลิตเนื้อสัตว์แปรรูปกึ่งปรุงสุกและปรุงสุก และการผลิตผลิตภัณฑ์อาหารสำเร็จรูปหรืออาหารพร้อม…

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 178bn | 21.60 | -0.9% | 8.2x | 4.4% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 581bn → FY2025 THB 571bn · −9.6bn · -1.7%

- ยอดขายตามนิยามของบริษัทลด 2% เพราะเงินบาทแข็งกดรายได้ต่างประเทศเมื่อแปลงเป็นบาท; หากตัด FX ยอดขายยังโตประมาณ 3% ขณะที่ตัวเลข RFO ด้านบนคงใช้ รายการขาย SET 01
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > โดยรายได้จากการขายเป็นสดั ส่วนของกิจการต่างประเทศร้อยละ 62 และกิจการในประเทศไทย

  `MDA_CPF_FY2025` · `p004` · SHA 931dbeff36b3
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 19.6bn → FY2025 THB 25.2bn · +5.6bn · +28.8%

- อัตรากำไรขั้นต้นเพิ่มเป็น 16.9% จาก 14.6% จากการควบคุมต้นทุน ต้นทุนกากถั่วเหลืองลดลง มาตรการความปลอดภัยทางชีวภาพ ที่ดีขึ้น และราคาสุกรในภูมิภาคสูงขึ้น จึงชดเชยยอดขายรายงานที่อ่อนลง
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > 2.1 การเพม ิ ประสทิ ธภิ าพดา้ นการควบคุมต้นทุนการผลติ และราคากากถวั เหลอื งโลกทล ี ดลงจาก ปีก่อน ซ ึงเป็นผลมาจากปริมาณผลผลิตท ลี ้นตลาดในประเทศผู้ผลิตรายใหญ่ (บราซิลและ

  `MDA_CPF_FY2025` · `p007` · SHA 92dfc4c139dc
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_CPF_FY2025`

##### TFG — ดาวรุ่ง · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ไทยฟู้ดส์ กรุ๊ป จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัทประกอบธุรกิจหลักเกี่ยวกับการผลิตไก่และจำหน่ายไก่สด แช่เย็นและแช่แข็งและผลิตภัณฑ์แปรรูปจากไก่ ผลิตและจำหน่ายสุกร และผลิตและจำหน่ายอาหารสัตว์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 56.7bn | 9.55 | +114.1% | 7.6x | 10.2% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 65.5bn → FY2025 THB 72.8bn · +7.3bn · +11.2%

- รายได้โต 11% จากปริมาณไก่เพิ่ม 6% สุกรเวียดนามเพิ่ม 18% อาหารสัตว์เพิ่ม 23% และสาขาค้าปลีกขยายจาก 401 เป็น 615 แห่ง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The revenue from retail shop business for the year 2025 was Baht 27,394.96 million increased by 14.27% from Baht 23,973.50 million in the same period of 2024. The number of retail shops at the end of 2024 and 2025 was 401 shops and 615 shops respectively.

  `MDA_TFG_FY2025` · `p015` · SHA ea3f2ef7d419
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 3.1bn → FY2025 THB 7.4bn · +4.3bn · +136.7%

- กำไรส่วนผู้ถือหุ้นเพิ่ม 137% ตามกำไรขั้นต้นที่เพิ่ม 71%; ปริมาณโปรตีนและสาขาค้าปลีกที่สูงขึ้น การบริหารช่องทาง/สต็อกที่ดีขึ้น และต้นทุนวัตถุดิบต่อหน่วยลดลงช่วยขยาย อัตรากำไร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In the year of 2025, the Company's gross profit from sales of goods and rendering was Baht 15,001.17 million increased by 70.95% from Baht 8,775.30 million the same period of 2024 mainly due to volume sold of chicken, swine in Thailand and swine in Vietnam increased, revenue increased from the retail shop expansion and raw material per unit decrease.

  `MDA_TFG_FY2025` · `p016` · SHA bb52e8bf9d4f
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_TFG_FY2025`

##### BTG — ตัวเพิ่ม RFO · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เบทาโกร จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ธุรกิจเกษตรอุตสาหกรรมและอาหารครบวงจร

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 40.4bn | 20.90 | +14.8% | 6.9x | 5.5% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 114bn → FY2025 THB 122bn · +8.1bn · +7.1%

- ยอดขายขยายตัวจากแพลตฟอร์มปศุสัตว์และอาหาร รวมถึงสัดส่วนสินค้าแปรรูป อาหารพร้อมทาน ช่องทางบริการอาหาร ช่องทางค้าปลีกสมัยใหม่ และส่งออกที่เพิ่มขึ้น
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > EBITDA and EBITDA Margin The Company’s EBITDA was at THB13,924.3 million in 2025, an increase of 50.5% from THB9,250.6 million in 2024. Meanwhile, EBITDA margin was at 11.3% in 2025, up from 8.0% in 2024. The increase in EBITDA and EBITDA margin was mainly attributable to an increase in gross profit and gross profit margin of consumer food business. Moreover, the Company was able to control expenses efficiently, which resulted in SG&A to Sales Ratio at 10.5% in 2025 which was similar to the last year.

  `MDA_BTG_FY2025` · `p009` · SHA 396a2b9f6d83
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 2.5bn → FY2025 THB 6.7bn · +4.2bn · +171.1%

- กำไรเพิ่มขึ้นมากจากต้นทุนข้าวโพด กากถั่วเหลือง และข้าวสาลีลดลง ราคาสุกรในประเทศดีขึ้น ส่วนผสมธุรกิจ ขยับสู่ช่องทาง อัตรากำไร สูง และควบคุมต้นทุนมีประสิทธิภาพขึ้น
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross Profit and Gross Profit Margin The Company’s gross profit was at THB20,640.2 million in 2025, an increase of 34.0% from THB15,401.1 million in 2024. Meanwhile, gross profit margin was at 16.9% in 2025, up from 13.5% in 2024. The increase in gross profit and gross profit margin were primarily due to 1) raw material cost decreased following lower animal feed prices particularly for corn, soybean meal and wheat, 2) increased domestic pork prices, 3) product portfolio optimization which focused on high-margin products and channels such as processed food and ready-to-eat products, along with expanding foodservice, modern trade and export channels.

  `MDA_BTG_FY2025` · `p008` · SHA 6089116bfd9e
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_BTG_FY2025`

##### FM — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท ฟู้ดโมเม้นท์ จำกัด (มหาชน)** — รายได้และกำไรเคลื่อนไหวสอดคล้องกัน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัทประกอบธุรกิจโดยการถือหุ้นในบริษัทอื่น (Holding Company) โดยมีบริษัทย่อยที่ประกอบธุรกิจหลัก 2 ธุรกิจ คือ ผลิตและจำหน่ายไก่ชำแหละ และผลิตและจำหน่ายชิ้นส่วนไก่แปรรูปปรุงสุก

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 4.2bn | 4.26 | +19.0% | 6.1x | 9.4% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 10 · NPAT 14 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 7.3bn → FY2025 THB 7.1bn · −195m · -2.7%

- RFO ปี 2568 อยู่ที่ 7,145 ลบ. ลด 2.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Group reported total revenue of THB 1,763 million in Q4/2025, comprised of 49% from the CAV business and 51% from the RAW business (Q4/2024: THB 1,878 million with 42% from CAV and 58% from RAW). Total revenue decreased by THB 115 million (-6.12%), as due to sale of RAW business decreased by THB 191 million while sales of CAV increased THB 76 million. The overall gross profit margin was 13.95% (Q4/2024: 13.63%), an incline of 0.32%.

  `MDA_FM_FY2025` · `p009` · SHA 9c9e0fc98e59
  </details>
- RFO ปี 2568 อยู่ที่ 7,145 ลบ. ลด 2.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Group reported total revenue of THB 7,145 million for Y2025, with 42% from the CAV business and 58% from the RAW business (2024: THB 7,340 million with 40% from CAV and 60% from RAW). Total revenue decreased by THB 195 million (-2.65%), mainly caused by RAW revenue decrease. The overall gross profit margin was 15.26% (2024: 14.86%).

  `MDA_FM_FY2025` · `p021` · SHA 5ba1928faabb
  </details>
- RFO ปี 2568 อยู่ที่ 7,145 ลบ. ลด 2.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ปริมาณขายและปริมาณการผลิต และ ราคาขายและส่วนผสมผลิตภัณฑ์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Sales volume was 79,020 tons (2024: 76,900 tons) with sales value of THB 4,128 million (2024: THB 4,402 million) at an average price of THB 52.23 per kilogram (2024: THB 57.24 per kilogram). The gross profit margin was 15.38% (2024: 12.97%). Revenue declined due to slowing export demand in 2025. Average selling prices decreased because of market pricing mechanisms. Despite the lower selling prices, the Group benefited positively from continuously decreasing raw material costs for animal feed compared to the previous year, resulting in a good and stable gross profit margin.

  `MDA_FM_FY2025` · `p026` · SHA 6bd43bc7c2be
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 702m → FY2025 THB 674m · −28m · -3.9%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 674 ลบ. ลด 3.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ปริมาณขายและปริมาณการผลิต และ ราคาขายและส่วนผสมผลิตภัณฑ์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Sales volume was 79,020 tons (2024: 76,900 tons) with sales value of THB 4,128 million (2024: THB 4,402 million) at an average price of THB 52.23 per kilogram (2024: THB 57.24 per kilogram). The gross profit margin was 15.38% (2024: 12.97%). Revenue declined due to slowing export demand in 2025. Average selling prices decreased because of market pricing mechanisms. Despite the lower selling prices, the Group benefited positively from continuously decreasing raw material costs for animal feed compared to the previous year, resulting in a good and stable gross profit margin.

  `MDA_FM_FY2025` · `p026` · SHA 6bd43bc7c2be
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 674 ลบ. ลด 3.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Group reported total revenue of THB 1,763 million in Q4/2025, comprised of 49% from the CAV business and 51% from the RAW business (Q4/2024: THB 1,878 million with 42% from CAV and 58% from RAW). Total revenue decreased by THB 115 million (-6.12%), as due to sale of RAW business decreased by THB 191 million while sales of CAV increased THB 76 million. The overall gross profit margin was 13.95% (Q4/2024: 13.63%), an incline of 0.32%.

  `MDA_FM_FY2025` · `p009` · SHA 9c9e0fc98e59
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 674 ลบ. ลด 3.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Group reported total revenue of THB 7,145 million for Y2025, with 42% from the CAV business and 58% from the RAW business (2024: THB 7,340 million with 40% from CAV and 60% from RAW). Total revenue decreased by THB 195 million (-2.65%), mainly caused by RAW revenue decrease. The overall gross profit margin was 15.26% (2024: 14.86%).

  `MDA_FM_FY2025` · `p021` · SHA 5ba1928faabb
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 674 ลบ. ลด 3.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ต้นทุนถั่วเหลืองและกากถั่วเหลือง และ ราคาและปริมาณปศุสัตว์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Chicken market in Thailand this year is expanding, benefiting from higher pork prices, which have increased domestic demand for chicken meat. Chicken is a high-protein meat that is more affordable, resulting in average selling prices remaining favorable, despite ongoing market fluctuations. At the same time, feed costs such as soybean meal and corn continue to stay at relatively low levels. This eases in raw materials costs helps reduce cost pressure on Thai poultry producers. The Group continues to implement cost management measures to maintain competitiveness in the market. However, in 2026, when Thailand market opens for imports of animal feed corn from the United States, it can somewhat

  `MDA_FM_FY2025` · `p006` · SHA d7e6ad208af9
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_FM_FY2025`

##### BR — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท บางกอกแร้นช์ จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัท บางกอกแร้นช์ จำกัด (มหาชน) ("บริษัทฯ") เป็นผู้นำในธุรกิจผลิตอาหารจากเนื้อเป็ดแบบครบวงจร โดยดำเนินธุรกิจเกษตรอุตสาหกรรมและผลิตอาหารจากเนื้อเป็ดที่มีคุณภาพในระดับพรีเมี่ยม และจำแนกธุรกิจของกลุ่มบริษัทออกเป็น 5 ประเภท ได้แก่ 1) ธุรกิจอาหารสัตว์ 2) ธุรกิจฟาร์มพ่อแม่พันธุ์เป็ด 3) ธุรกิจโรงฟักไข่เป็ด 4) ธุรกิจฟาร์มเลี้ยงเป็ดเนื้อ และ 5) ธุรกิจโรงงานชำแหละและแปรรูปเนื้อเป็ด เพื่อผลิตเป็นผลิตภัณฑ์อาหารแปรรูปพร้อมปร…

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.8bn | 1.99 | +22.1% | 9.9x | 1.9% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 1 · NPAT 3 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 7.4bn → FY2025 THB 7.5bn · +148m · +2.0%

- RFO ปี 2568 อยู่ที่ 7,533 ลบ. เพิ่ม 2.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Factors affecting the Group's performance in the future Bank interest rates, inflation, and high energy costs still are factors impacting the performance of the Group. On the other hand, the company manage to maintain a consistant EBITDA this year due to successful sales strategies and stronger internal control. Moreover, foreign exchange rates, global market volatility, and country policies continues to be an on going risk factor. With most measures related to Covid-19 lifted globally; the group still continues to place high importance on taking care of employees and creating a safe working environment. We strive to continue implementing strict measures on controlling the possible spread of

  `MDA_BR_FY2025` · `p006` · SHA 7e12e3c1e965
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 121m → FY2025 THB 142m · +20m · +16.5%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 142 ลบ. เพิ่ม 16.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าเสื่อมราคาและค่าตัดจำหน่าย และ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 7) As of 31 December 2025, the Group's total assets is 9,811 million Baht, a decrease of 697 million Baht from 31 December 2024, mainly from inventory, other financial current assets and depreciation. As of 31 December 2025, the Group's total liabilities is 4,905 million Baht, a decrease of 859 million Baht from 31 December 2024, mainly from repayment of long-term loans and decreased from Account payable. Total shareholders' equity increased from profit for the year ended 31 December 2025.

  `MDA_BR_FY2025` · `p005` · SHA 27fc17ec8a1c
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 142 ลบ. เพิ่ม 16.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net profit for the period attributable to equity holders of the Company

  `MDA_BR_FY2025` · `p002` · SHA 8873e9ffdf1b
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 142 ลบ. เพิ่ม 16.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Factors affecting the Group's performance in the future Bank interest rates, inflation, and high energy costs still are factors impacting the performance of the Group. On the other hand, the company manage to maintain a consistant EBITDA this year due to successful sales strategies and stronger internal control. Moreover, foreign exchange rates, global market volatility, and country policies continues to be an on going risk factor. With most measures related to Covid-19 lifted globally; the group still continues to place high importance on taking care of employees and creating a safe working environment. We strive to continue implementing strict measures on controlling the possible spread of

  `MDA_BR_FY2025` · `p006` · SHA 7e12e3c1e965
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Factors affecting the Group's performance in the future Bank interest rates, inflation, and high energy costs still are factors impacting the performance of the Group. On the other hand, the company manage to maintain a consistant EBITDA this year due to successful sales strategies and stronger internal control. Moreover, foreign exchange rates, global market volatility, and country policies continues to be an on going risk factor. With most measures related to Covid-19 lifted globally; the group still continues to place high importance on taking care of employees and creating a safe working environment. We strive to continue implementing strict measures on controlling the possible spread of

  `MDA_BR_FY2025` · `p006` · SHA 7e12e3c1e965
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_BR_FY2025`

##### SORKON — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท ส. ขอนแก่นฟู้ดส์ จำกัด (มหาชน)** — รายได้และกำไรเคลื่อนไหวสอดคล้องกัน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัทฯ เป็นผู้ผลิตและจำหน่ายอาหาร ซึ่งจำแนกธุรกิจหลักออกเป็น 4 ประเภทธุรกิจ คือ 1) ธุรกิจอาหารแปรรูปจากเนื้อสัตว์2) ธุรกิจอาหารทะเลแปรรูป3) ธุรกิจฟาร์มเลี้ยงสุกร4) ธุรกิจร้านอาหารประเภท Quick Service Restaurant (QSR) 5) ธุรกิจต่างประเทศ 6) ธุรกิจอื่นๆ

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.1bn | 3.54 | -1.7% | 14.5x | 3.8% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 14 · NPAT 12 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 2

**RFO — เพราะอะไร** — FY2024 THB 3.4bn → FY2025 THB 3.5bn · +157m · +4.7%

- RFO ปี 2568 อยู่ที่ 3,515 ลบ. เพิ่ม 4.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Q3/2025) The Group has accumulated revenue from sales from processed food from meat for 12 months of THB 1,887.2 million, which accounted for 54.0 percent of total revenue from sales. This represented a growth rate of 1.8 percent compared to the same period of previous year. The accumulated gross profit from this business segment was THB 509.1 million, which accounted for 27.0 percent of revenue from processed food from meat. This showed a growth of 5.6 percent compared to the same period of previous year. The continued growth in sales and gross profit margin from the processed food from meat business was supported by effective labor cost control and the benefit from lower raw material price

  `MDA_SORKON_FY2025` · `p013` · SHA 6862082da29f
  </details>
- RFO ปี 2568 อยู่ที่ 3,515 ลบ. เพิ่ม 4.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from rental and services The Group has revenue from rental and service of THB 4.7 million in Q4/2025, which accounted for 0.5 percent of revenue from sales. The represents an increase of growth 13.8 percent as compared to the same period of previous year (an increase of 10.8 percent compared to Q3/2025). The Group has accumulated revenue from rental and service for 12 months amounting to THB 17.7 million, which accounted for 0.5 percent of revenue from sales. The represents a growth of 9.7 percent compared to the same period of previous year. The increase in rental and service income was due to the Group's success in acquiring new tenants, as well as improved management of fixed cost

  `MDA_SORKON_FY2025` · `p020` · SHA 023a2cf02958
  </details>
- RFO ปี 2568 อยู่ที่ 3,515 ลบ. เพิ่ม 4.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ราคาและปริมาณปศุสัตว์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 4. Swine Farming The Group has revenue from swine farming of THB 73.2 million in Q4/2025, which accounted for 8.4 percent of total sales. This represents a decrease of 26.2 percent as compared to the same quarter of previous year (a decrease of 19.5 percent compared to Q3/2025). The gross profit from this business segment was THB 3.8 million, which accounted for 5.2% of revenue from swine farming. This showed a decrease of 83.8 percent compared to the same quarter of previous year (a decrease of 64.9 percent compared to Q3/2025). The Group has revenue from swine farming for 12 months amounting to THB 383.8 million, which accounted for 11.0 percent of revenue from sales. This represents a gro

  `MDA_SORKON_FY2025` · `p018` · SHA f7971bfb87a9
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 133m → FY2025 THB 135m · +2m · +1.3%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 135 ลบ. เพิ่ม 1.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Q3/2025) The Group has accumulated revenue from sales from processed food from meat for 12 months of THB 1,887.2 million, which accounted for 54.0 percent of total revenue from sales. This represented a growth rate of 1.8 percent compared to the same period of previous year. The accumulated gross profit from this business segment was THB 509.1 million, which accounted for 27.0 percent of revenue from processed food from meat. This showed a growth of 5.6 percent compared to the same period of previous year. The continued growth in sales and gross profit margin from the processed food from meat business was supported by effective labor cost control and the benefit from lower raw material price

  `MDA_SORKON_FY2025` · `p013` · SHA 6862082da29f
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 135 ลบ. เพิ่ม 1.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > percent compared to the same period of previous year. The main reason for the increase in gross profit in Q4/2025 primarily supported by more effective cost management across both labor and raw material expenses. In particular, lower pork raw material prices contributed positively to cost control. As a result, the group’s gross profit margin improved compared to the same period last year. Others : The Group recognized a gain of THB 30.5 million from change in fair value of biological assets net cost of sales in Q4/2025, which accounted for 3.5 percent of revenue from sales. The change in fair value increased by 1,293.1 percent compared to the same period of previous year. (an increase of 172

  `MDA_SORKON_FY2025` · `p009` · SHA fba7b3d0a786
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 135 ลบ. เพิ่ม 1.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ราคาและปริมาณปศุสัตว์ และ ความเสี่ยงด้านภูมิรัฐศาสตร์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > market prices of swine, whereas during the same period last year, swine prices were trending downward. Net profit The Group has net profit attributable to the Company of THB 47.4 million in Q4/2025, which accounted for 5.5 percent of revenue from sales. The net profit increased 51.3 percent compared to the same quarter of the previous attributable to the Company : year (an increase of 421.1 percent compared to Q3/2025). The Group has accumulated net profit attributable to the Company for 12 months amounting to THB 135.2 million, which accounted for 3.9 percent of revenue from sales. The accumulated net profit attributable to the Company increased 1.3 percent compared to the same period of pr

  `MDA_SORKON_FY2025` · `p010` · SHA 76a873c21796
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 135 ลบ. เพิ่ม 1.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > previous year (a decreased of 13.2 percent from Q3/2025). The gross profit from this business segment was THB 7.2 million, which accounted for 38.3 percent of revenue from quick service restaurants. This showed a decrease of 24.0% compared to the same quarter of previous year (a decrease of 19.0 percent compared to Q3/2025). The Group has accumulated revenue from quick service restaurants for 12 months amounted to THB 88.5 million, which accounted for 2.5 percent of total revenue from sales. This represents a growth of 13.9% compared to the same period of previous year. The accumulated gross profit from this business segment was THB 36.1 million which accounted for 40.8 percent of revenue fr

  `MDA_SORKON_FY2025` · `p017` · SHA 8914e89b3ad4
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: อัตรากำไรดีขึ้น และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > percent compared to the same period of previous year. The main reason for the increase in gross profit in Q4/2025 primarily supported by more effective cost management across both labor and raw material expenses. In particular, lower pork raw material prices contributed positively to cost control. As a result, the group’s gross profit margin improved compared to the same period last year. Others : The Group recognized a gain of THB 30.5 million from change in fair value of biological assets net cost of sales in Q4/2025, which accounted for 3.5 percent of revenue from sales. The change in fair value increased by 1,293.1 percent compared to the same period of previous year. (an increase of 172

  `MDA_SORKON_FY2025` · `p009` · SHA fba7b3d0a786
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ ค่าใช้จ่ายขายและบริหาร และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Selling and Distribution Expenses (109.0) -12.6% (89.9) -9.9% 21.3% Administrative Expenses (90.9) -10.5% (102.4) -11.3% -11.2% Loss from rental and service (0.1) 0.0% (1.4) -0.2% -89.8% Gain (Loss) on changes in fair value less 30.5 3.5% 2.2 0.2% 1293.1% cost to sale of biological assets

  `MDA_SORKON_FY2025` · `p006` · SHA 9cd65954c91f
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_SORKON_FY2025`

#### ทะเบียนข้อสรุป — F1

| ส่วน | ประเภท | ข้อสรุป | รหัสแหล่งข้อมูล |
|---|---|---|---|
| headline | ข้ออนุมานนักวิเคราะห์ | กำไรฟื้นชัด แต่ตลาดยังให้ส่วนลดแบบหุ้นวัฏจักร | FY_PANEL, F1_E1, F1_E2 |
| earnings_fact | ข้อเท็จจริงจากการคำนวณ | FY2025 RFO +0.8%; สถานะ NPAT ส่วนผู้ถือหุ้น: profit_increased | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | FY2025 RFO เกือบทรงตัว (+0.8%) ขณะที่ NPAT ส่วนผู้ถือหุ้นเพิ่ม 54.2% จึงเป็นการฟื้นจาก margin | FY_PANEL |
| why | คำอธิบายฝ่ายจัดการ | CPF ระบุปัจจัยจากการควบคุมต้นทุน ต้นทุนกากถั่วเหลืองลดลง biosecurity และราคาสุกรสูงขึ้น | F1_E1 |
| why | ข้อเท็จจริงจากการคำนวณ | TFG และ BTG ทำให้การฟื้นกระจายออกจาก CPF ตามการคำนวณ panel ที่สอบทาน | FY_PANEL |
| why | ข้ออนุมานนักวิเคราะห์ | ข้อสรุปกลุ่มผสานการคำนวณ panel ที่สอบทานกับ MD&A รายบริษัท ไม่ใช่หลักฐานเหตุเชิงสาเหตุจากบริษัทเดียว | FY_PANEL, F1_E1, F1_E2 |
| causal_chain | ข้ออนุมานนักวิเคราะห์ | ห่วงโซ่เหตุ: ราคาสัตว์ → ส่วนต่าง → Margin → NPAT → Valuation | F1_E1, F1_E2 |
| roles | ข้ออนุมานนักวิเคราะห์ | บทบาท: ผู้นำ — CPF; ตัวเพิ่ม RFO — BTG; ดาวรุ่ง — TFG | FY_PANEL, F1_E1, F1_E2 |
| valuation | ข้ออนุมานนักวิเคราะห์ | P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 7.8x ครอบคลุม 6/6 บริษัท และ 100.0% ของ market cap ที่มีข้อมูล. ส่วนลดวัฏจักรสะท้อนความเสี่ยงสินค้าโภคภัณฑ์และการกลับทิศ | SET_PUBLIC_EOD, F1_E1, F1_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | ราคาหมูและไก่ยืนเหนือแรงกดดันต้นทุนอาหารสัตว์ | F1_E1, F1_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | อุปสงค์ส่งออกและการบริโภคในประเทศยังแข็งแรง | F1_E1, F1_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | วินัยด้าน margin ต่อเนื่องถึง 6M26 | F1_E1, F1_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | โรคระบาดสัตว์หรืออุปทานล้นตลาด | F1_E1, F1_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | ต้นทุนอาหารสัตว์กลับมาสูงขึ้น | F1_E1, F1_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | ความผันผวนด้านส่งออกและค่าเงิน | F1_E1, F1_E2 |
| must_prove | ประเด็นที่ต้องพิสูจน์ | 6M26 ต้องพิสูจน์ว่า margin ที่ฟื้นตัวอยู่ได้แม้ฐานวัฏจักรเอื้อประโยชน์น้อยลง | F1_E1, F1_E2 |

#### ทะเบียนหลักฐาน — F1

- **`FY_PANEL`** · _ข้อเท็จจริงจากการคำนวณ_ — Audited FY2024-25 company panel
  - RFO / NPAT-to-owners / independent panel membership; QA 43 pass / 0 fail
  - บทบาท: historical fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_company_fy2024_2025_audited_2026-08-07.csv`
  - SHA-256: `e5e04dbc40ffcc79fed58545a93dc4549c29cdaecf260bea73711bc6d0720481`
- **`SET_PUBLIC_EOD`** · _ข้อเท็จจริงจากการคำนวณ_ — SET public Company Highlights — EOD 2026-08-07
  - Adjusted YTD; unadjusted price, market cap and valuation; factsheet-surface cross-check
  - บทบาท: current market fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_set_public_surface_reconciliation_2026-08-07.csv`
  - SHA-256: `544c1f29fe2d409ee398822ac2bf32b769081718962ae2d1138985b0146b9530`
- **`SET_COMPANY_PROFILE`** · _ข้อเท็จจริง_ — SET company profiles — English and Thai
  - Official company names and business descriptions refreshed and validated for the 118-company perimeter from the public SET profile API
  - บทบาท: company business profile
  - URL: <https://www.set.or.th/th/market/product/stock/overview>
- **`COMPANY_REPORTS`** · _ข้ออนุมานนักวิเคราะห์_ — Company report synthesis corpus
  - Annual-only draft synthesis; reconciled to the ticker FY2025 MD&A where available
  - บทบาท: secondary synthesis; not management attribution
  - พาธ: `data/company-reports.json`
  - SHA-256: `c1a2bc40cbe21a2058aa596c362e4d47ad117360831b847de78ec414831fd2d2`
- **`MDA_CPF_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — CPF FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/CPF/MDA_CPF_2025FY_T.md`
  - SHA-256: `328cbbfa14a3282822bd0b561aef491ddadc42dad2db68d96aa33d74001733a1`
  - URL: <https://weblink.set.or.th/dat/news/202602/0101NWS260220261709011470T.pdf>
- **`MDA_TFG_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — TFG FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/TFG/MDA_TFG_2025FY_E.md`
  - SHA-256: `b802918c495922b1a9274d367aa72331efafe309a0dc84eaa780d4b0504dbb6b`
  - URL: <https://weblink.set.or.th/dat/news/202602/1202NWS180220262218103450E.pdf>
- **`MDA_BTG_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — BTG FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/BTG/MDA_BTG_2025FY_E.md`
  - SHA-256: `954ea8c529d886f5483a48787844960fb7692aca454e37bd6b9d367b264c9cf6`
  - URL: <https://weblink.set.or.th/dat/news/202602/0612NWS240220261720139810E.pdf>
- **`MDA_FM_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — FM FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/FM/MDA_FM_2025FY_E.md`
  - SHA-256: `c923a1165b72331ed44b40565bff8c2589ce0dc2910104bb58eb55bdcb0023b0`
  - URL: <https://weblink.set.or.th/dat/news/202602/1870NWS270220261735257390E.pdf>
- **`MDA_BR_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — BR FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/BR/MDA_BR_2025FY_E.md`
  - SHA-256: `331549320db2d864580a387e833c57a180082bc532f07ac44044b6a6b5ab49b2`
  - URL: <https://weblink.set.or.th/dat/news/202602/1267NWS240220260829252830E.pdf>
- **`MDA_SORKON_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — SORKON FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SORKON/MDA_SORKON_2025FY_E.md`
  - SHA-256: `7b0154bf31919ad84183f0be39329ea026c6364fe91ed6fa3a2448cc48203eb9`
  - URL: <https://weblink.set.or.th/dat/news/202602/0345NWS240220261945297370E.pdf>
- **`F1_E1`** · _ฝ่ายจัดการ_ — CPF FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/CPF/MDA_CPF_2025FY_T.md`
  - SHA-256: `328cbbfa14a3282822bd0b561aef491ddadc42dad2db68d96aa33d74001733a1`
- **`F1_E2`** · _มุมมองล่วงหน้า_ — KSS TFG research
  - Historical explanation or forward cross-check; see source role
  - บทบาท: forward/credit context
  - พาธ: `Listed Company/1-Raw/06-Market Reference/Broker Research/2026/FOOD/KSS_TFG_345421.md`
  - SHA-256: `dd225193976b27c15141d02f21eaf29cb405320a669c31c9390e9d91eb38166d`
- **`F1_FACTSHEET`** · _ข้อเท็จจริงจากการคำนวณ_ — SET Factsheet — CPF
  - Live leader cross-check
  - บทบาท: presentation-surface check
  - URL: <https://www.set.or.th/th/market/product/stock/quote/cpf/factsheet>

### F4 · เครื่องดื่มแบรนด์ — กำไรที่โตจาก margin ช่วยรองรับ premium ของแบรนด์

`ราคานำพื้นฐาน` · 19.3% M-cap · THB 157bn · 9 บริษัท

| ตัวชี้วัด | RFO | NPAT | ราคา | P/E |
|---|---|---|---|---|
| ช่วง | FY2025 YoY | ส่วนผู้ถือหุ้น FY2025 YoY | ราคา YTD ปรับแล้ว | เฉพาะบริษัทที่มีกำไร |
| ค่า | -3.3% | +7.8% | +13.1% | 17.2x |
| จำนวน | THB 87.0bn FY2025 | THB 9.3bn FY2025 | ณ 7 ส.ค. 2569 | ค่าเฉลี่ยรวม |
| ครอบคลุม | 9/9 | 9/9 | 9/9 • 100% M-cap | 8/9 • 99% M-cap |

**ข้อเท็จจริงที่สังเกตได้** — FY2025: RFO -3.3% • NPAT +7.8% • ราคา YTD +13.1% • P/E 17.2x • ครอบคลุม RFO 9/9 • NPAT 9/9

#### เหตุผลที่เปลี่ยน

1. _ข้อเท็จจริงจากการคำนวณ_ · ปริมาณ — รายได้ลดลงแต่ NPAT เพิ่ม โดย OSP เป็นตัวเพิ่มกำไรหลัก
2. _คำอธิบายฝ่ายจัดการ_ · แบรนด์ / mix — เครือข่ายจำหน่าย domestic mix และการคุมต้นทุนสำคัญกว่าการเติบโตของยอดขาย
3. _ข้อเท็จจริงจากการคำนวณ_ · คุมต้นทุน — CBG เป็นตัวผลักราคาหลัก ทำให้สัญญาณตลาดไม่ได้พึ่งบริษัทเดียว

#### ห่วงโซ่เหตุและผล

**ปริมาณ** → **แบรนด์ / mix** → **คุมต้นทุน** → **Margin** (10.6% +1.1 ppt YoY) → **NPAT** (+7.8% THB 9.3bn FY2025)

#### บทบาทในกลุ่ม

| บทบาท | Ticker | ค่า | ที่มาของค่า |
|---|---|---|---|
| ผู้นำและตัวเพิ่มกำไร | OSP | 34% | สัดส่วน Market Cap ในกลุ่ม |
| ตัวผลักราคา | CBG | +17.8% | ราคา YTD ปรับแล้ว |

#### มูลค่า

**ตลาดกำลังจ่ายเพื่อ — ข้ออนุมาน** — P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 17.2x ครอบคลุม 8/9 บริษัท และ 99.4% ของ market cap ที่มีข้อมูล. แบรนด์และช่องทางจำหน่ายสนับสนุน premium โดยมีเงื่อนไขว่า volume ต้องฟื้น

| Trigger | Risk |
|---|---|
| ยอดขายในประเทศฟื้น | กำลังซื้ออ่อน |
| product mix ดีขึ้น | การแข่งขันด้านโปรโมชั่น |
| การส่งออกและกระจายสินค้าทำได้ตามแผน | ต้นทุนบรรจุภัณฑ์และน้ำตาล |

**6M26 ต้องพิสูจน์** — 6M26 ต้องเพิ่มการฟื้นของ volume ต่อจาก margin ที่ดีขึ้นใน FY2025

#### วิเคราะห์รายบริษัท — F4 เครื่องดื่มแบรนด์

_ทุกบริษัทใน perimeter ของ Segment ที่สอบทาน_

| Ticker | บทบาท | M-cap | RFO YoY | NPAT YoY | ราคา YTD | P/E | Margin |
|---|---|---|---|---|---|---|---|
| OSP | ผู้นำและตัวเพิ่มกำไร | THB 53.5bn | -5.6% | +123.8% | +10.6% | 15.0x | 14.3% |
| CBG | ตัวผลักราคา | THB 51.3bn | +5.1% | -18.4% | +17.8% | 23.6x | 10.5% |
| ICHI | บริษัทในกลุ่ม | THB 19.5bn | -5.9% | +1.6% | +11.9% | 14.2x | 16.4% |
| SAPPE | บริษัทในกลุ่ม | THB 10.6bn | -22.5% | -38.0% | +11.4% | 14.1x | 14.8% |
| COCOCO | บริษัทในกลุ่ม | THB 9.1bn | +1.7% | -64.5% | +24.5% | 34.9x | 3.6% |
| HTC | บริษัทในกลุ่ม | THB 6.7bn | +1.6% | -5.6% | +12.1% | 11.5x | 6.9% |
| TIPCO | บริษัทในกลุ่ม | THB 3.3bn | +0.7% | กลับเป็นกำไร | -11.2% | 13.6x | 11.9% |
| MALEE | บริษัทในกลุ่ม | THB 2.2bn | -7.2% | -35.9% | -2.9% | 15.2x | 2.5% |
| PLUS | บริษัทในกลุ่ม | THB 898m | -7.8% | ขาดทุน | +16.5% | n.m. | -6.0% |

##### OSP — ผู้นำและตัวเพิ่มกำไร · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท โอสถสภา จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — การดำเนินธุุรกิจหลักของโอสถสภาแบ่งเป็น 3 กลุ่ม ตามลักษณะธุุรกิจ กลยุทธ์ทางการตลาด และกลุ่มลูกค้า โดยมีกลุ่มธุรกิจหลักประกอบด้วย (1) กลุ่มผลิตภัณฑ์เครื่องดื่ม (2) กลุ่มผลิตภััณฑ์ของใช้ส่วนบุุคคล (3) กลุ่มผลิตภัณฑ์เพื่อสุขภาพและลูกอม ส่วนธุรกิจอื่นที่ไม่ใช่ธุรกิจหลักคืือ ธุรกิจให้บริการรับจ้างผลิตสินค้าและบรรจุภััณฑ์ (OEM)

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 53.5bn | 17.80 | +10.6% | 15.0x | 14.3% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 5

**RFO — เพราะอะไร** — FY2024 THB 27.1bn → FY2025 THB 25.6bn · −1.5bn · -5.6%

- รายได้รายงานอ่อนตัวจากเครื่องดื่มในประเทศที่ลดแรงใน 1H25 ก่อนฟื้นใน 2H25 ขณะที่ต่างประเทศโตจากเมียนมาและลาว
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > YoY: 4Q/25 vs 4Q/24 QoQ: 4Q/25 vs 3Q/25 YoY: 2025 vs 2024 +33.8% YoY +17.5% QoQ +15.3% YoY Revenue (+) Expanded by 1.0% from (+) Expanded by 50.8% driven (+) Expanded by 4.8%, driven from domestic beverage sales, mainly by sales growth in international primarily by strong sales growth Sales driven by the functional drink beverage segment, particularly in the international beverage segment significant growth in Myanmar segment, particularly in (-) Overall slight declined by market, supported by seasonal Myanmar and Laos. 1.6% due to lower factors and brand strength. (–) Overall declined by 5.6%, international personal care sales (+) Expanded by 13.6% came mainly due to the slowdown in from My

  `MDA_OSP_FY2025` · `p013` · SHA 171476de05dd
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 1.6bn → FY2025 THB 3.7bn · +2.0bn · +123.8%

- กำไรมากกว่าสองเท่าเมื่อ อัตรากำไรขั้นต้น เพิ่มเป็น 40.1% จากประสิทธิภาพการผลิต วินัยต้นทุน และการตลาดแบบเน้น ROI
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Route-to-Market strategy, combined with appropriate, ROI-driven marketing and trade promotion activities, contributed to a 7.2% YoY reduction in distribution and administrative expenses. As a result of the aforementioned operational strategies, in 2025 the Company reported a gross profit margin of 40.1%, an increase of 2.8% YoY. Net profit attributable to the Company totaled 3,667 million Baht, increasing 123.8% YoY, while normalized net profit reached 3,503 million Baht, up 15.3% YoY. During 2025, the Company recognized a gain of 295 million Baht from the disposal of its investment in the glass bottle manufacturing and distribution business in Myanmar (MGE Group) as part of a business restr

  `MDA_OSP_FY2025` · `p006` · SHA 5f1d8d56241c
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 1) Comprising loss on disposal of investments in associates and bad debt write-offs. 2) Excluding non-recurring items from restructuring and the consolidation of production facilities Remark: The exchange rate used for converting the Myanmar financial statements in the consolidated financial report is based on the Central Bank of Myanmar, equivalent to USD/MMK 2,100. This rate differs from the market exchange rate due to foreign exchange risks arising from the fluctuations of the

  `MDA_OSP_FY2025` · `p052` · SHA b0f750b7bc18
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: การแข่งขันและการส่งเสริมการขาย และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Route-to-Market strategy, combined with appropriate, ROI-driven marketing and trade promotion activities, contributed to a 7.2% YoY reduction in distribution and administrative expenses. As a result of the aforementioned operational strategies, in 2025 the Company reported a gross profit margin of 40.1%, an increase of 2.8% YoY. Net profit attributable to the Company totaled 3,667 million Baht, increasing 123.8% YoY, while normalized net profit reached 3,503 million Baht, up 15.3% YoY. During 2025, the Company recognized a gain of 295 million Baht from the disposal of its investment in the glass bottle manufacturing and distribution business in Myanmar (MGE Group) as part of a business restr

  `MDA_OSP_FY2025` · `p006` · SHA 5f1d8d56241c
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_OSP_FY2025`

##### CBG — ตัวผลักราคา · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท คาราบาวกรุ๊ป จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ประกอบธุรกิจโดยการถือหุ้นในบริษัทอื่น (Holding Company) ซึ่งมีการลงทุนหลักในบริษัทย่อยที่ประกอบธุรกิจ ผลิต ทำการตลาด จำหน่าย และบริหารจัดการการจัดจำหน่ายเครื่องดื่มบำรุงกำลังและเครื่องดื่มอื่น ๆ อย่างครบวงจร

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 51.3bn | 51.25 | +17.8% | 23.6x | 10.5% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 9 · NPAT 7 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 21.0bn → FY2025 THB 22.0bn · +1.1bn · +5.1%

- RFO ปี 2568 อยู่ที่ 22,042 ลบ. เพิ่ม 5.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ และ ความเสี่ยงด้านภูมิรัฐศาสตร์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 1. Revenue from sales In 2025, the Company reported total sales revenue of THB 22,042 million, representing an increase of THB 1,077 million or 5% YoY from the same period of the previous year. Of this amount, revenue from the manufacture and sale of products under the Company’s own trademarks totaled THB 11,845 million, decreasing by THB 345 million or 3% YoY, this performance reflected strong growth in domestic Carabao Dang sales, which reached a record high, primarily due to lower export sales, particularly to Cambodia, as a result of geopolitical tensions and border conflicts during the period, which adversely impacted sales in the second half of the year. However, revenue from distribut

  `MDA_CBG_FY2025` · `p004` · SHA e6ccbef63ed3
  </details>
- RFO ปี 2568 อยู่ที่ 22,042 ลบ. เพิ่ม 5.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ และ ความเสี่ยงด้านภูมิรัฐศาสตร์ และ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > well as launching sales promotion campaigns in convenience stores nationwide. These combined efforts enhanced brand awareness and drove domestic sales growth of Carabao Dang energy drink, resulting in continued market share expansion, with market share in Thailand increasing by 2.8% And, the Company recorded export revenue of THB 4,144 million, decreasing by THB 1,468 million or 26% YoY. The decline was primarily attributable to lower exports to the CLMV countries, particularly Cambodia, with overall exports to the CLMV market decreasing by 27% YoY due to geopolitical tensions and border conflicts during the period, which adversely affected sales performance in the second half of the year. I

  `MDA_CBG_FY2025` · `p008` · SHA b268af678ea7
  </details>
- RFO ปี 2568 อยู่ที่ 22,042 ลบ. เพิ่ม 5.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Company’s revenue contribution from domestic and international operations was 81%:19% In 2025, the Company recorded domestic sales revenue of THB 17,898 million, increasing by THB 2,546 million or 17% YoY, primarily driven by the strong performance of Carabao Dang energy drink, which achieved a new record high in 2025. This growth was supported by the Company’s continued implementation of its core strategy of maintaining the retail price at THB 10 per bottle to help alleviate consumers’ cost of living, alongside the continuation of marketing activities in collaboration with Thairath under the “Carabao Dang Supporting Thai People’s Careers” campaign on Thairath TV for the fifth consecutive ye

  `MDA_CBG_FY2025` · `p007` · SHA 7842af04c227
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 2.8bn → FY2025 THB 2.3bn · −523m · -18.4%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 2,320 ลบ. ลด 18.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 6. Net profits and net profits margin In 2025, the Company reported normalized net profit of THB 2,837 million, decreasing by THB 6 million or 0.2% YoY compared to the same period last year. The slight decline was primarily attributable to lower export revenue as previously discussed. Nevertheless, overall sales continued to grow, supported by the strong performance of Carabao Dang energy drink in the domestic market and the successful expansion of distribution services in the alcoholic beverage business, which continued to gain popularity among consumers. However, in 2025, the Company recognized an impairment loss on goodwill of THB 518 million, relating to its investment in Carabao Holding

  `MDA_CBG_FY2025` · `p018` · SHA 133d9be2fedf
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 2,320 ลบ. ลด 18.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ความเสี่ยงด้านภูมิรัฐศาสตร์ และ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Public In 2025, the Company reported gross profit of THB 5,844 million, increasing by THB 123 million or 2% YoY, representing a gross profit margin of 27%, stable compared to 2024. This performance was supported by the Company’s effective management of key raw materials and packaging costs, including aluminum, sugar, and cullet, through efficient procurement and inventory management to optimize costs. In addition, energy costs particularly natural gas continued to trend downward. The Company also enhanced production efficiency through weight reduction of glass bottles and thickness reduction of aluminum cans, contributing to lower packaging costs.

  `MDA_CBG_FY2025` · `p012` · SHA f41bec758ecf
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 2,320 ลบ. ลด 18.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ การแข่งขันและการส่งเสริมการขาย และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 3. Selling, general and administrative (SG&A) expenses In 2025, the Company recorded selling and administrative expenses of THB 2,400 million, increasing by THB 51 million or 14% YoY. However, such expenses accounted for 10.9% of total sales revenue, slightly decreasing from 11.2% in 2024. The increase was primarily attributable to the Company’s continued investment in marketing, promotional, and operating activities, while maintaining strict cost control to ensure cost-effectiveness and operational efficiency, which remains a key strategic focus. In addition, football sponsorship fees decreased by THB 65 million or 33% YoY following the expiration of a two-season sponsorship agreement with

  `MDA_CBG_FY2025` · `p013` · SHA 17e654c05cd3
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 2,320 ลบ. ลด 18.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Company’s revenue contribution from domestic and international operations was 81%:19% In 2025, the Company recorded domestic sales revenue of THB 17,898 million, increasing by THB 2,546 million or 17% YoY, primarily driven by the strong performance of Carabao Dang energy drink, which achieved a new record high in 2025. This growth was supported by the Company’s continued implementation of its core strategy of maintaining the retail price at THB 10 per bottle to help alleviate consumers’ cost of living, alongside the continuation of marketing activities in collaboration with Thairath under the “Carabao Dang Supporting Thai People’s Careers” campaign on Thairath TV for the fifth consecutive ye

  `MDA_CBG_FY2025` · `p007` · SHA 7842af04c227
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ยอดขายส่งออกและตลาดต่างประเทศ และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 6. Net profits and net profits margin In 2025, the Company reported normalized net profit of THB 2,837 million, decreasing by THB 6 million or 0.2% YoY compared to the same period last year. The slight decline was primarily attributable to lower export revenue as previously discussed. Nevertheless, overall sales continued to grow, supported by the strong performance of Carabao Dang energy drink in the domestic market and the successful expansion of distribution services in the alcoholic beverage business, which continued to gain popularity among consumers. However, in 2025, the Company recognized an impairment loss on goodwill of THB 518 million, relating to its investment in Carabao Holding

  `MDA_CBG_FY2025` · `p018` · SHA 133d9be2fedf
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_CBG_FY2025`

##### ICHI — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท อิชิตัน กรุ๊ป จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัท อิชิตัน กรุ๊ป จำกัด (มหาชน) ประกอบธุรกิจเครื่องดื่ม เป็นผู้ผลิตและจำหน่ายเครื่องดื่มชาเขียวพร้อมดื่ม อิชิตัน กรีนที, เครื่องดื่มสมุนไพร เย็นเย็น โดยอิชิตัน และเครื่องดื่มน้ำผลไม้ไม่อัดลม ?ไบเล่? ในปี 2557 บริษัทได้เข้าทำสัญญาร่วมลงทุนกับบริษัท พีที อาทรี่ แปซิฟิค (?AP?) ซึ่งเป็นนิติบุคคลที่จัดตั้งขึ้นในประเทศอินโดนีเซีย เพื่อร่วมลงทุนในบริษัท พีที อิชิ ตัน อินโดนีเซีย ซึ่งเป็นกิจการร่วมค้าที่จะจัดตั้งขึ้นให…

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 19.5bn | 15.00 | +11.9% | 14.2x | 16.4% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 3 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 8.6bn → FY2025 THB 8.1bn · −508m · -5.9%

- ยอดขาย FY2025 ลด 5.9% เหลือ 8.09 พันลบ. จากยอดขายในประเทศลด 8.6% เพราะเศรษฐกิจซบเซาและฤดูร้อนสั้นกว่าปกติ ขณะที่ยอดขายต่างประเทศโต 37.2% จาก OEM เพื่อส่งออกที่ขยายต่อเนื่อง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue In the year 2025, the Company earned sales revenue of 8,086.2 million baht, decreased by 5.9% fromlastyearasrevenueof8,594.4millionbaht.Salesrevenuedecreasedby508.2million bahtresultingfrom domestic sales decreasedby8.6%fromthedomestic economicdownturn and a shorter-than-usual summer season this year, on the other hand the overseas sales increased by 37.2% due to the continued growth in revenue from contract manufacturing (OEM) for exports.

  `MDA_ICHI_FY2025` · `p010` · SHA 822f7042768a
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 1.3bn → FY2025 THB 1.3bn · +21m · +1.6%

- กำไรสุทธิเพิ่ม 1.6% เป็น 1.33 พันลบ. และ net อัตรากำไร เพิ่มเป็น 16.4% จาก 15.2%
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Profit In the year 2025, the Company earned net profit of 1,327.6 million baht or equivalent to net profit margin of 16.4% of sales revenue, as compared to the previous year net profit earned 1,306.3 million baht or equivalent to net profit margin of 15.2% of sales revenue, net profit increased by 21.3millionbaht or equal to 1.6%from the same period of thelast year.

  `MDA_ICHI_FY2025` · `p019` · SHA b88699b47c26
  </details>
- ภาษีลด 56.9% เพราะกำไรดำเนินงานลดลงและบริษัทได้รับสิทธิ BOI ภายใต้มาตรการพัฒนาชุมชนและสังคม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Tax Expense In the year 2025 and year 2024, the Company had tax expense were 173.2 million baht and 402.2 million baht respectively. Tax expense decreased from the previous year by 229.0 million baht or equal to 56.9% due to decrease in operating profit and benefits received from the Board of Investment under the investment promotion measures for community and social development.

  `MDA_ICHI_FY2025` · `p017` · SHA e1e8c4c49f8d
  </details>
- ส่วนแบ่งกำไร JV เพิ่ม 7.3 ลบ. หลังเปิดสินค้าใหม่และเพิ่มจำนวนผู้จัดจำหน่ายให้ครอบคลุมพื้นที่มากขึ้น
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Share of profit of investmentinjoint venture In year 2025 and year 2024, the Company had share of profit of investment in joint venture were 16.6 million baht and 9.3 million baht respectively. The share of profit of investment in jointventure hadbeen increased by7.3 million bahtdue to increased sales from the launchof the new product“Ichitan Greentea& Cheese milk tea"and adjustments weremadeto increase the number of distributors in order to cover a wider distribution area.

  `MDA_ICHI_FY2025` · `p018` · SHA ccf2b7eaef4c
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_ICHI_FY2025`

##### SAPPE — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เซ็ปเป้ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — เซ็ปเป้ เจ้าของแบรนด์เครื่องดื่มนวัตกรรมชั้นนำของเมืองไทย ดำเนินธุรกิจด้วยปณิธาน ?เราจะทำให้ชีวิตของผู้คนดีขึ้น ผ่านจิตวิญญาณที่สร้างสรรค์ของเรา?นำนวัตกรรมมาเป็นตัวขับเคลื่อนองค์กรให้ออกมาอย่างสร้างสรรค์ มีพลัง และสนุกสนาน ถ่ายทอดผ่านสินค้า และวัฒนธรรมองค์กรได้อย่างลงตัว ปัจจุบัน เซ็ปเป้ มีสินค้าคุณภาพ 5 กลุ่มสินค้า เพื่อรองรับความต้องการของผู้บริโภคทั้งในและต่างประเทศ 1.…

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 10.6bn | 34.25 | +11.4% | 14.1x | 14.8% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 3

**RFO — เพราะอะไร** — FY2024 THB 6.8bn → FY2025 THB 5.3bn · −1.5bn · -22.5%

- รายได้ลดประมาณ 23% จากตลาดต่างประเทศหลักชะลอและเงินบาทแข็งกดรายรับส่งออก
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > International sales totaled at THB 881 million, a decrease of 14.3% YoY. This was driven by the global economic slowdown, the volatility of Thai Baht, the ongoing conflict of geopolitics, and the U.S. trade measures, which remained uncertain. Nevertheless, sales in Europe have gradually recovered from Q3/2025, besides sales in America have also improved from Q3/2025. However, sales in the Middle East were affected by external factors. In Asia, performance remained under pressure due to intensified competition in key markets such as South Korea and distributor management issues in Indonesia.

  `MDA_SAPPE_FY2025` · `p010` · SHA 6416745952f5
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 1.3bn → FY2025 THB 776m · −476m · -38.0%

- กำไรลดประมาณ 38% เพราะฐานส่งออกที่ลดลงทำให้ ผลของต้นทุนคงที่ต่อกำไร อ่อนลง ขณะที่ FX และค่าใช้จ่ายพัฒนาตลาดกด อัตรากำไร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In Q4/2025, the cost of goods sold (COGS) ratio was 56.5% of revenue from selling goods, an identical proportion of the previous quarter. Throughout 2025, the company faced cost management challenges arising from the appreciation of the Thai Baht and lower production capacity utilization compared to the previous year. Nevertheless, the company effectively managed costs through several key initiatives, including automation projects, production and HR planning, solar rooftop and floating systems, and the application of machine learning in quality control processes. As a result, the overall COGS ratio remained stable.

  `MDA_SAPPE_FY2025` · `p012` · SHA 403f9f7a0d3e
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Administrative expenses in Q4/2025 totaled THB 149.6 million, or 12.3% of revenue from selling goods, slightly increasing from THB 147.5 million YoY. This increase was primarily due to trademark expenses arising from the write-off of certain trademarks amounting to THB 11.7 million. This was one-time, non-recurring item.

  `MDA_SAPPE_FY2025` · `p014` · SHA aa0c32dcc428
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ต้นทุนวัตถุดิบและต้นทุนการผลิต และ เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Profit & Loss statementQ4/2568%Q4/2567%Q3/2568%YoY%QoQ%FY2568%FY2567%YoY%Total Revenue1,243,544 102.5%1,442,013 104.7%1,378,264 102.2%-13.8%-9.8%5,386,950 102.6%7,052,789 104.1%-23.6%Revenue from selling goods1,213,699 100.0%1,376,920 100.0%1,348,625 100.0%-11.9%-10.0%5,252,606 100.0%6,775,377 100.0%-22.5%Net gain from foreign exchange3,565 0.3%7,928 0.6%3,775 0.3%-55.0%-5.6%14,041 0.3%19,237 0.3%-27.0%Gain from changes in interest in associate- - - 0.0%- - Others income26,280 2.2%57,165 4.2%25,864 1.9%-54.0%1.6%120,303 2.3%258,175 3.8%-53.4%Cost of goods sold685,235 56.5%738,534 53.6%762,184 56.5%-7.2%-10.1%2,926,529 55.7%3,631,766 53.6%-19.4%Gross profit528,464 43.5%638,386 46.4%586,441 43

  `MDA_SAPPE_FY2025` · `p004` · SHA a13bada86131
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_SAPPE_FY2025`

##### COCOCO — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ไทย โคโคนัท จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ประกอบธุรกิจผลิตและจำหน่ายผลิตภัณฑ์แปรรูปจากมะพร้าวและผลไม้ต่างๆ เช่น กะทิกระป๋อง กะทิพาสเจอไรซ์ น้ำมะพร้าว น้ำมะพร้าวบรรจุกระป๋อง น้ำมะพร้าวพาสเจอไรซ์ ขนมมะพร้าว และอาหารสำเร็จรูป ภายใต้ตราสินค้า Thaicoco และ Cocoburi รวมถึงการผลิตสินค้าเพื่อการอุตสาหกรรม นอกจากนี้ บริษัทฯ ยังได้ประกอบธุรกิจผลิตอาหารสัตว์เลี้ยงแบบเปียกเพื่อสุขภาพสำหรับสุนัขและแมวภายใต้ชิ่อผลิตภัณฑ์ Moochie…

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 9.1bn | 6.20 | +24.5% | 34.9x | 3.6% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 16 · NPAT 10 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 2

**RFO — เพราะอะไร** — FY2024 THB 6.6bn → FY2025 THB 6.7bn · +112m · +1.7%

- RFO ปี 2568 อยู่ที่ 6,697 ลบ. เพิ่ม 1.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ มาตรการภาษีนำเข้าและข้อกีดกันทางการค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company reported revenue from sales and services for the year 2025 of 6,697.14 million Baht, representing an increase of 112.16 million Baht or 1.70% compared to the previous year. The growth was primarily supported by the expansion of sales in the Americas region , which maintained its positive growth momentum despite the United States’ announcement of a 19% import tariff on certain products originating from Thailand. Furthermore, such tariff measures have not had a material impact on the Company’s operating results. For the fourth quarter of 2025, revenue from sales and services amounted to 1,620.85 million Baht, decreasing by 105.87 million Baht or 6.13% compared to the same quarter o

  `MDA_COCOCO_FY2025` · `p006` · SHA 29b8d6c1f568
  </details>
- RFO ปี 2568 อยู่ที่ 6,697 ลบ. เพิ่ม 1.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Overseas revenue from sales and services for the year 2025 amounted to 5,704.48 million Baht, decreasing by 69.63 million Baht or 1.21% compared to the previous year. Export sales accounted for 85.18% of total sales and service revenue. By region, sales in the Americas increased by 36.90%, Oceania increased by 16.73%, Europe increased by 1.39%, and the Middle East increased by 1.04%, while Asia and Africa declined. For the fourth quarter of 2025, overseas revenue totaled 1,362.76 million Baht, decreasing by 126.94 million Baht or 8.52% compared to the same quarter of the previous year and decreasing by 134.93 million Baht or 9.01% compared to the preceding quarter. Export sales represented 8

  `MDA_COCOCO_FY2025` · `p007` · SHA 91ce3280e493
  </details>
- RFO ปี 2568 อยู่ที่ 6,697 ลบ. เพิ่ม 1.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Cost of sales and services for the year 2025 amounted to 5,458.33 million baht, representing an increase of 450.08 million baht, or 8.99%, compared to the previous year. The cost of sales and services as a percentage of revenue from sales and services was 81.50%, increasing from 76.06% in the prior year, or an increase of 5.45 percentage points. The increase in cost of sales was primarily attributable to stronger-than- expected growth in coconut milk product sales, which required the Company to procure additional raw materials during the first half of the year when coconut prices were elevated. Although the Company had secured partial raw material reserves, such reserves were insufficient to

  `MDA_COCOCO_FY2025` · `p011` · SHA 423a703214a4
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 686m → FY2025 THB 244m · −442m · -64.5%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 244 ลบ. ลด 64.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ปริมาณขายและปริมาณการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company reported a gross profit margin on revenue from sales and services of 18.50% for the year 2025, decreasing from 23.94%, compared to the previous year. For the fourth quarter of 2025, the gross profit margin was 20.22%, improving from 17.52% in the same quarter of the previous year and from 18.78% in the preceding quarter. The improvement in the fourth quarter was primarily driven by sales expansion in the coconut milk and pet food product segments in the Americas region, the implementation of pricing strategy adjustments, and effective cost management. In addition, coconut raw material costs began to decline from the third quarter onward, while higher production volumes in the pet

  `MDA_COCOCO_FY2025` · `p014` · SHA beff45a6cfb0
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 244 ลบ. ลด 64.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company recorded finance costs of 88.24 million baht for the year 2025, representing an increase of 40.29 million baht, or 84.05%, compared to the previous year. Finance costs as a percentage of revenue from sales and services were 1.32%, increasing by 0.59 percentage points from the prior year. For the fourth quarter of 2025, finance costs amounted to 26.76 million baht, increasing by 12.74 million baht, or 90.81%, compared to the same quarter of the previous year, and by 0.79 million baht, or 3.03%, compared to the preceding quarter. Finance costs as a percentage of revenue from sales and services were 1.65%, increasing by 0.84 percentage points from the same quarter of the previous ye

  `MDA_COCOCO_FY2025` · `p017` · SHA b7c6c87e867b
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 244 ลบ. ลด 64.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company recorded distribution costs of 417.99 million baht for the year 2025, representing a decrease of 8.86 million baht, or 2.08%, compared to the previous year. Distribution costs as a percentage of revenue from sales and services were 6.24%, decreasing by 0.24 percentage points from the prior year. The improvement was mainly attributable to more effective control of marketing media expenses and other related selling expenses. For the fourth quarter of 2025, distribution costs amounted to 108.14 million baht, decreasing by 23.60 million baht, or 17.92%, compared to the same quarter of the previous year, but increasing by 1.63 million baht, or 1.53%, compared to the preceding quarter.

  `MDA_COCOCO_FY2025` · `p015` · SHA 46c85928e6e0
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 244 ลบ. ลด 64.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ปริมาณขายและปริมาณการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > revenue from sales and services was 79.78%, improving from 82.48% in the same quarter of the previous year a decrease of 2.70 percentage points and from 81.22% in the preceding quarter (a decrease of 1.44 percentage points).The decline was mainly attributable to lower coconut raw material costs in the second half of the year, improved production efficiency in the coconut milk product segment, and higher production volumes in the pet food segment, which generated economies of scale and reduced unit costs.

  `MDA_COCOCO_FY2025` · `p013` · SHA ceca6bc880fb
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > % YoY% QoQ% YoYTotal Revenue from sale of goods1,629,327 100.521,770,959 100.981,756,282 101.71(7.23) (8.00) 6,735,912 100.586,619,164 100.521.76 Revenue from sale and services1,620,851 100.001,753,747 100.001,726,723 100.00(6.13) (7.58) 6,697,142 100.006,584,978 100.001.70 Interest and Other income6,870 0.429,034 0.525,979 0.3514.90 (23.95) 29,660 0.4434,186 0.52(13.24) Net gain on foreign exchange- - 8,178 0.47 23,580 1.37 (100.00) (100.00) - - - - N/A Gain on derivatives fair value remeasurement1,606 0.10- 0.00- - N/AN/A9,110 0.14- - N/ACosts of sale of goods and services1,293,072 79.781,424,462 81.221,424,268 82.48(9.21) (9.22) 5,458,329 81.505,008,253 76.068.99 Gross profit327,779 20.22

  `MDA_COCOCO_FY2025` · `p004` · SHA 40029141dd06
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ยอดขายส่งออกและตลาดต่างประเทศ และ เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ มาตรการภาษีนำเข้าและข้อกีดกันทางการค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company operates in a highly competitive and constantly evolving business environment, both domestically and internationally, particularly in the health beverage segment, where market growth may be affected by consumer behavior, production costs, and global economic conditions. Volatility in raw material and packaging prices, as well as fluctuations in foreign exchange rates, are key factors that may impact the Company’s costs and operating results, especially export revenue. In addition, there are potential risks arising from changes in import tariff policies in certain trading partner countries, which could affect the price competitiveness of the Company’s products. With respect to the

  `MDA_COCOCO_FY2025` · `p023` · SHA dc526fc7cd4b
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_COCOCO_FY2025`

##### HTC — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท หาดทิพย์ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — จำหน่ายเครื่องดื่มน้ำอัดลมและเครื่องดื่มต่างๆ ซึ่งได้รับลิขสิทธิ์จาก เดอะ โคคา-โคลา คัมปะนี (ประเทศสหรัฐอเมริกา) เมืองแอตแลนตา มลรัฐจอร์เจีย ให้ผลิตและจำหน่ายภายใต้เครื่องหมายการค้า โคคา-โคลา แฟนต้า สไปร์ท และผลิตภัณฑ์อื่นที่ เดอะ โคคา-โคลา คัมปะนี เป็นเจ้าของ ได้แก่ กลุ่มผลิตภัณฑ์น้ำผลไม้ มินิทเมด และน้ำดื่มน้ำทิพย์ มีขอบเขตการผลิตเพื่อจำหน่ายเฉพาะใน 14 จังหวัดภาคใต้

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 6.7bn | 16.70 | +12.1% | 11.5x | 6.9% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 6 · NPAT 5 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 2

**RFO — เพราะอะไร** — FY2024 THB 8.1bn → FY2025 THB 8.3bn · +129m · +1.6%

- RFO ปี 2568 อยู่ที่ 8,258 ลบ. เพิ่ม 1.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ปริมาณขายและปริมาณการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company reported sales revenue for year 2025 amounting to 8,258.4 million baht, an increase of 128.6 million Baht or 1.6% YoY, as a result of; - Beverage sales volume for year 2025 totaled 73.0 million unit cases, representing a 0.7%YoY increase. Despite the overall softening in the sparkling soft drink market, this growth reflects the effectiveness of the Company’s sales strategy adjustment and its ability to proactively execute in the market - The Company employs a strategic approach to Revenue Growth Management through price mix, pack mix, channel mix, and market execution capabilities to maintain sales volume amid a softening market condition. Throughout 2025, the Company implemented

  `MDA_HTC_FY2025` · `p006` · SHA 9ca401ad2ebb
  </details>
- RFO ปี 2568 อยู่ที่ 8,258 ลบ. เพิ่ม 1.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ กำลังการผลิตและเครื่องจักรใหม่ และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ต้นทุนทางการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Selling and administrative expenses (SG&A) totaled 2,840.7 million baht, representing a 2.5% YoY increase, this was primarily driven by increased selling expenses aimed at stimulating sales in a softening market. Finance costs amounted to 40.5 million baht, an increase of 19.0 million baht or 88.7% YoY. This was attributable to long-term loans obtained to invest in machinery for the PET Line 3 production and the glass bottling line, as part of the Company’s long-term capacity expansion and operational efficiency strategy. Net profit, as reported in the consolidated financial statements, was 568.3 million baht, a decrease of 5.6% YoY, primarily due to provision of impairment costs of certain

  `MDA_HTC_FY2025` · `p010` · SHA 55e813d09698
  </details>
- RFO ปี 2568 อยู่ที่ 8,258 ลบ. เพิ่ม 1.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Other income amounted to 109.8 million baht, an increase of 50.6 million baht or 85.4 percent YoY, mainly driven by support received from The Coca-Cola Company to help stimulate sales amid the softening non‑alcoholic beverage market.

  `MDA_HTC_FY2025` · `p009` · SHA e5b2582c4def
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 602m → FY2025 THB 568m · −33m · -5.6%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 568 ลบ. ลด 5.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ กำลังการผลิตและเครื่องจักรใหม่ และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ต้นทุนทางการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Selling and administrative expenses (SG&A) totaled 2,840.7 million baht, representing a 2.5% YoY increase, this was primarily driven by increased selling expenses aimed at stimulating sales in a softening market. Finance costs amounted to 40.5 million baht, an increase of 19.0 million baht or 88.7% YoY. This was attributable to long-term loans obtained to invest in machinery for the PET Line 3 production and the glass bottling line, as part of the Company’s long-term capacity expansion and operational efficiency strategy. Net profit, as reported in the consolidated financial statements, was 568.3 million baht, a decrease of 5.6% YoY, primarily due to provision of impairment costs of certain

  `MDA_HTC_FY2025` · `p010` · SHA 55e813d09698
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 568 ลบ. ลด 5.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ภาระหนี้และโครงสร้างเงินทุน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In terms of operations for year 2025, the Company maintained a good cash cycle, with a duration of 29.9 days, which increased from 29.0 days in the same period last year due to an increase in collection day. The Company's debt repayment ability is at a good level with a debt-to-equity ratio of 0.8 times. The Company is able to cover its debt payment obligations by 4 times. The Company's gross profit margin for year 2025 was 42.2%, a decrease compared to 42.7% in the same period last year, The EBITDA margin was 14.7%, and the net profit margin was 6.9%.

  `MDA_HTC_FY2025` · `p017` · SHA bb1af50f4034
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 568 ลบ. ลด 5.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ กำลังการผลิตและเครื่องจักรใหม่ และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายขายและบริหาร และ ภาระหนี้และโครงสร้างเงินทุน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > YoY, due to provision of impairment costs of certain machinery and equipment, and higher selling expenses aimed at stimulating sales in a softening market. The Company recorded a net profit margin of 6.9 %, representing a decrease of 0.5 percentage point from the same period last year. - The Company's financial position continues to remain in a good position, with a debt-to-equity ratio of 0.8X and a favorable liquidity position as a cash cycle of 29.9 days.

  `MDA_HTC_FY2025` · `p005` · SHA fa3aa13a6335
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 568 ลบ. ลด 5.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross profit margin for year 2025 was 42.2%, a decrease of 0.5 percentage points YoY. This was mainly due to a higher sales proportion of packaging sizes above 500 milliliters (pack mix), aiming to enhance value for consumers and sustain beverage sales amid softening market conditions.

  `MDA_HTC_FY2025` · `p008` · SHA 43035ef3688e
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ กำลังการผลิตและเครื่องจักรใหม่ และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ต้นทุนทางการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Selling and administrative expenses (SG&A) totaled 2,840.7 million baht, representing a 2.5% YoY increase, this was primarily driven by increased selling expenses aimed at stimulating sales in a softening market. Finance costs amounted to 40.5 million baht, an increase of 19.0 million baht or 88.7% YoY. This was attributable to long-term loans obtained to invest in machinery for the PET Line 3 production and the glass bottling line, as part of the Company’s long-term capacity expansion and operational efficiency strategy. Net profit, as reported in the consolidated financial statements, was 568.3 million baht, a decrease of 5.6% YoY, primarily due to provision of impairment costs of certain

  `MDA_HTC_FY2025` · `p010` · SHA 55e813d09698
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำลังการผลิตและเครื่องจักรใหม่ และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายขายและบริหาร และ ภาระหนี้และโครงสร้างเงินทุน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > YoY, due to provision of impairment costs of certain machinery and equipment, and higher selling expenses aimed at stimulating sales in a softening market. The Company recorded a net profit margin of 6.9 %, representing a decrease of 0.5 percentage point from the same period last year. - The Company's financial position continues to remain in a good position, with a debt-to-equity ratio of 0.8X and a favorable liquidity position as a cash cycle of 29.9 days.

  `MDA_HTC_FY2025` · `p005` · SHA fa3aa13a6335
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_HTC_FY2025`

##### TIPCO — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ทิปโก้ฟูดส์ จำกัด (มหาชน)** — อยู่ในภาวะฟื้นตัว; อัตราเติบโตมีความสำคัญรองลงมา

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและจำหน่ายน้ำแร่ธรรมชาติพร้อมดื่ม ภายใต้เครื่องหมายการค้าหลัก ออรา

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 3.3bn | 6.75 | -11.2% | 13.6x | 11.9% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 9 · NPAT 9 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 2.0bn → FY2025 THB 2.0bn · +14m · +0.7%

- RFO ปี 2568 อยู่ที่ 1,969 ลบ. เพิ่ม 0.7% YoY; MD&A ระบุว่า Gross Profit (Loss) อัตรากำไร 36% 28% 8% 46% 49% (3%) 30% 0% 30% 37% 30% 7% In 2025, the Company and its subsidiaries generated total sales revenue of 1,969 million baht from continuing operations, representing a decrease of 27 million baht or 1% compared to last year. This change was mainly driven by two business segments, as follows: 1.1. Beverage Business In 2025, sales revenue from the beverage business decreased by 81 million baht, or 4%, compared with last year. The decline was primarily driven by lower revenue from the fruit juice product group. สำ น
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross Profit (Loss) Margin 36% 28% 8% 46% 49% (3%) 30% 0% 30% 37% 30% 7% In 2025, the Company and its subsidiaries generated total sales revenue of 1,969 million baht from continuing operations, representing a decrease of 27 million baht or 1% compared to last year. This change was mainly driven by two business segments, as follows: 1.1. Beverage Business In 2025, sales revenue from the beverage business decreased by 81 million baht, or 4%, compared with last year. The decline was primarily driven by lower revenue from the fruit juice product group. สำ นกั งำนใหญ่ : เลขที่ 118/1 อำคำรทิปโก ้ถนนพระรำม 6 แขวงพญำไท เขตพญำไท กรุงเทพมหำนคร 10400, โทร (02) 273 6200 โรงงำนเชียงใหม่ : เลขที่ 205/1 ห

  `MDA_TIPCO_FY2025` · `p026` · SHA 0b5b3a6f14e8
  </details>
- RFO ปี 2568 อยู่ที่ 1,969 ลบ. เพิ่ม 0.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ราคาขายและส่วนผสมผลิตภัณฑ์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > baht, or 36%, compared with last year. The growth was primarily supported by the strong performance of the Homsuwan fresh pineapple business, which achieved higher sales driven by harvest volumes in line with plan. Distribution channels were also expanded to include hypermarkets, whereas sales were previously concentrated mainly in supermarkets. The extracts business recorded strong growth as well, supported by the continued increase in product delivery volumes. The segment reported a gross profit margin of 46% in 2025, compared with 49% last year. The decline was mainly attributable to changes in the product mix, even though the new pineapple cultivation cycle delivered improved cost effici

  `MDA_TIPCO_FY2025` · `p030` · SHA 2ca9e0545e5a
  </details>
- RFO ปี 2568 อยู่ที่ 1,969 ลบ. เพิ่ม 0.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from fruit juice decreased in line with the contraction of the domestic market, impacted by the slowing economic environment, nationwide campaigns encouraging reduced sugar consumption, and the continuing effects of the sugar tax, all of which influenced consumer purchasing behavior. In the export market, although strong growth was observed early in the year, demand softened during the second half, particularly in ASEAN markets and the Philippines, which were affected by natural disaster events. However, revenue from the mineral water business continued to grow, supported by the strengthening of the brand in a market segment with favorable growth prospects. The increase in revenue ca

  `MDA_TIPCO_FY2025` · `p029` · SHA 41d10223a640
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 92m → FY2025 THB 234m · +326m

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 234 ลบ. จากขาดทุน -92.1 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ อัตรากำไรลดลง และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ราคาขายและส่วนผสมผลิตภัณฑ์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company and its subsidiaries reported a gross profit margin of 37%, an improvement from last year. This reflects the impact of systematic cost‑management initiatives, including cost‑reduction programs, SKU rationalization, reduction in the variety of raw material used, increased utilization of production capacity, optimization of the product mix toward higher‑margin items, and appropriate pricing adjustments. The EBITDA margin increased from 25% last year to 27% in 2025, supported by reduced losses in the beverage business, sustained profitability in the extracts business, and higher sales of Homsuwan fresh pineapples. These factors contributed to greater stability in the overall profit

  `MDA_TIPCO_FY2025` · `p060` · SHA 79d34da88252
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 234 ลบ. จากขาดทุน -92.1 ลบ.; MD&A ระบุว่า Gross Profit (Loss) อัตรากำไร 36% 28% 8% 46% 49% (3%) 30% 0% 30% 37% 30% 7% In 2025, the Company and its subsidiaries generated total sales revenue of 1,969 million baht from continuing operations, representing a decrease of 27 million baht or 1% compared to last year. This change was mainly driven by two business segments, as follows: 1.1. Beverage Business In 2025, sales revenue from the beverage business decreased by 81 million baht, or 4%, compared with last year. The decline was primarily driven by lower revenue from the fruit juice product group. สำ น
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross Profit (Loss) Margin 36% 28% 8% 46% 49% (3%) 30% 0% 30% 37% 30% 7% In 2025, the Company and its subsidiaries generated total sales revenue of 1,969 million baht from continuing operations, representing a decrease of 27 million baht or 1% compared to last year. This change was mainly driven by two business segments, as follows: 1.1. Beverage Business In 2025, sales revenue from the beverage business decreased by 81 million baht, or 4%, compared with last year. The decline was primarily driven by lower revenue from the fruit juice product group. สำ นกั งำนใหญ่ : เลขที่ 118/1 อำคำรทิปโก ้ถนนพระรำม 6 แขวงพญำไท เขตพญำไท กรุงเทพมหำนคร 10400, โทร (02) 273 6200 โรงงำนเชียงใหม่ : เลขที่ 205/1 ห

  `MDA_TIPCO_FY2025` · `p026` · SHA 0b5b3a6f14e8
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 234 ลบ. จากขาดทุน -92.1 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ราคาขายและส่วนผสมผลิตภัณฑ์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > baht, or 36%, compared with last year. The growth was primarily supported by the strong performance of the Homsuwan fresh pineapple business, which achieved higher sales driven by harvest volumes in line with plan. Distribution channels were also expanded to include hypermarkets, whereas sales were previously concentrated mainly in supermarkets. The extracts business recorded strong growth as well, supported by the continued increase in product delivery volumes. The segment reported a gross profit margin of 46% in 2025, compared with 49% last year. The decline was mainly attributable to changes in the product mix, even though the new pineapple cultivation cycle delivered improved cost effici

  `MDA_TIPCO_FY2025` · `p030` · SHA 2ca9e0545e5a
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 234 ลบ. จากขาดทุน -92.1 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ การยุติธุรกิจหรือสายผลิตภัณฑ์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the year 2025, Tipco Foods Public Company Limited (“the Company”) and its subsidiaries recorded a total net profit of 234 million baht. This consisted of a profit from continuing operations of 264 million baht and a loss from discontinued operations of 30 million baht. The performance of the continuing operations improved compared to 2024, reflecting effective cost management aligned with sales levels, adjustments to business strategies to match changing market trends, and the Company’s ability to maintain consistent profitability despite fluctuations in raw material costs and a slowing economic environment. On September 24, 2024, the Company discontinued the operations of Tipco Pineappl

  `MDA_TIPCO_FY2025` · `p012` · SHA 37d6740df5a2
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_TIPCO_FY2025`

##### MALEE — บริษัทในกลุ่ม · ติดตาม

**บริษัท มาลีกรุ๊ป จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผู้ผลิตและจัดจำหน่ายผลิตภัณฑ์อาหารและเครื่องดื่ม

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 2.2bn | 4.08 | -2.9% | 15.2x | 2.5% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 20 · NPAT 17 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 5

**RFO — เพราะอะไร** — FY2024 THB 8.5bn → FY2025 THB 7.8bn · −607m · -7.2%

- RFO ปี 2568 อยู่ที่ 7,848 ลบ. ลด 7.2% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Q4/2025 vs Q4/2024 (YoY) FY2025 vs FY2024 (YoY) The Group recorded revenue from sales and services of THB 1,995.4 The Group recorded revenue from sales and services of THB 7,848.3 million, a decrease of 0.4% YoY, with details as follows: million, a decrease of 7.2% YoY, with details as follows: • Sales and services from domestic amounted to THB 1,491.2 million, • Sales and services from domestic amounted to THB 5,168.2 million, increasing 21.4% YoY, mainly driven by higher sales of the Company’s increasing 1.1% YoY, mainly driven by revenue growth from CMG branded products in the fruit juice segment, Malee COCO coconut customers in the ready-to-drink tea and coffee segment, as well as water,

  `MDA_MALEE_FY2025` · `p041` · SHA bfc948814d3f
  </details>
- RFO ปี 2568 อยู่ที่ 7,848 ลบ. ลด 7.2% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ความเสี่ยงด้านภูมิรัฐศาสตร์ และ อุปสงค์และกำลังซื้อในประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Group recorded revenue from sales and services of THB 1,995.4 The Group recorded revenue from sales and services of THB 7,848.3 million, a decrease of 1.6% YoY, with details as follows: million, a decrease of 7.2% YoY, with details as follows: • Branded business sales amounted to THB 663.7 million, down 22.7% • Branded business sales totaled THB 2,597.3 million, decreasing YoY, mainly due to a slowdown in dairy product sales caused by the 14.2% YoY, mainly due to a slowdown in dairy product sales caused by border conflict, as well as lower sales in the canned fruit category. the border conflict, as well as lower sales in the canned fruit and juice categories. • Contract Manufacturing (CM

  `MDA_MALEE_FY2025` · `p033` · SHA 810edf4b289b
  </details>
- RFO ปี 2568 อยู่ที่ 7,848 ลบ. ลด 7.2% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ และ อุปสงค์และกำลังซื้อในประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Q4/2025 vs Q4/2024 (YoY) FY2025 vs FY2024 (YoY) • The Group recorded total operating revenue of THB 1,995.4 million, a • The Group recorded total operating revenue of THB 7,848.3 million, a decrease of 0.4% YoY, mainly due to a slowdown in sales of dairy decrease of 7.2% YoY, primarily due to lower sales from contract products resulting from the Thailand–Cambodia border situation, as well manufacturing dairy customers affected by the Thailand–Cambodia border as lower sales in canned fruit and overseas CMG businesses. situation, as well as a decline in the juice category in Vietnam. However, part Nevertheless, part of the revenue decline was offset by continued of the revenue decline was offs

  `MDA_MALEE_FY2025` · `p009` · SHA 9fda0b6d5044
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 308m → FY2025 THB 197m · −111m · -35.9%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 197 ลบ. ลด 35.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > ready-to-drink canned coffee business. ready-to-drink canned coffee segment, which continues to gain consumer • The gross profit margin was 15.5%, decreasing by 2.9% YoY due to popularity, and from higher purchase orders from customers in the dairy the recognition of obsolete inventory provisions. products segment. • Net profit attributable to the Company’s shareholders, as reported, • The gross profit margin was 18.0%, decreasing by 1.3% YoY due to the amounted to THB 23.6 million, declining by 1.7% YoY, primarily due to recognition of obsolete inventory provisions. lower gross profit as a result of one-off items totaling THB 33.4 million, • Net profit attributable to the Company’s sharehol

  `MDA_MALEE_FY2025` · `p010` · SHA 020f6f71e95b
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 197 ลบ. ลด 35.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ ปริมาณขายและปริมาณการผลิต และ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross Profit Gross Profit The Group recorded a gross profit of THB 309.1 million, a decrease of The Group recorded a gross profit of THB 1,409.2 million, a decrease of 16.1% YoY, resulting in a gross profit margin of 15.5%, down 2.9 13.7% YoY. The gross profit margin was 18.0%, declining by 1.3 percentage points. The decline was due to lower sales volume combined percentage points YoY due to lower sales volume and the recognition of with obsolete inventory provisions, which were non-recurring one-off obsolete inventory provisions, which were non-recurring one-off items. items. Excluding this one-off item, the adjusted gross profit would be THB Excluding this one-off item, the adjusted gross

  `MDA_MALEE_FY2025` · `p045` · SHA 4e9cf367a1ac
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 197 ลบ. ลด 35.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Profit Margin Attributable to Equity Holders (Adjusted) (%)4/ 2.9% 3.1% 2.9% 0.0% (0.2%) 3.6% 4.2% 0.6% Note : Figures may differ slightly due to rounding. 1/ Adjusted gross profit excludes one-off items. 2/ Adjusted net profit (loss) attributable to equity holders of the company excludes one-off items. 3/ Adjusted gross profit margin excludes one-off items. 4/ Adjusted net profit margin attributable to equity holders excludes one-off items.

  `MDA_MALEE_FY2025` · `p006` · SHA e17907fd4a60
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 197 ลบ. ลด 35.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Group recorded a net profit attributable to the Company’s shareholders of THB 197.4 million, a decrease of 35.9% YoY, due to the shareholders of THB 23.6 million, a decrease of 1.8% YoY, mainly due to decline in sales as mentioned above and lower gross profit resulting from the decline in sales as mentioned above and lower gross profit resulting one-off items totaling THB 128.4 million. The majority of this amount was from one-off items totaling THB 33.4 million. The majority of this amount related to obsolete inventory provision of dairy products arising from the was related to obsolete inventory provision for dairy products, driven by Thailand–Cambodia border situation. Excluding this

  `MDA_MALEE_FY2025` · `p050` · SHA c4e0a675c490
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: อัตรากำไรลดลง และ ปริมาณขายและปริมาณการผลิต และ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross Profit Gross Profit The Group recorded a gross profit of THB 309.1 million, a decrease of The Group recorded a gross profit of THB 1,409.2 million, a decrease of 16.1% YoY, resulting in a gross profit margin of 15.5%, down 2.9 13.7% YoY. The gross profit margin was 18.0%, declining by 1.3 percentage points. The decline was due to lower sales volume combined percentage points YoY due to lower sales volume and the recognition of with obsolete inventory provisions, which were non-recurring one-off obsolete inventory provisions, which were non-recurring one-off items. items. Excluding this one-off item, the adjusted gross profit would be THB Excluding this one-off item, the adjusted gross

  `MDA_MALEE_FY2025` · `p045` · SHA 4e9cf367a1ac
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Group recorded a net profit attributable to the Company’s shareholders of THB 197.4 million, a decrease of 35.9% YoY, due to the shareholders of THB 23.6 million, a decrease of 1.8% YoY, mainly due to decline in sales as mentioned above and lower gross profit resulting from the decline in sales as mentioned above and lower gross profit resulting one-off items totaling THB 128.4 million. The majority of this amount was from one-off items totaling THB 33.4 million. The majority of this amount related to obsolete inventory provision of dairy products arising from the was related to obsolete inventory provision for dairy products, driven by Thailand–Cambodia border situation. Excluding this

  `MDA_MALEE_FY2025` · `p050` · SHA c4e0a675c490
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_MALEE_FY2025`

##### PLUS — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท โรแยล พลัส จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ธุรกิจผลิตและจำหน่ายเครื่องดื่มน้ำผลไม้ ได้แก่ น้ำมะพร้าว น้ำนมมะพร้าว น้ำผลไม้ผสมเม็ดแมงลักและเมล็ดเชีย และน้ำผลไม้ผสมอื่นๆ รวมทั้งเครื่องดื่มต่างๆ

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 898m | 1.34 | +16.5% | n.m. | -6.0% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 10 · NPAT 10 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 2

**RFO — เพราะอะไร** — FY2024 THB 1.4bn → FY2025 THB 1.3bn · −111m · -7.8%

- RFO ปี 2568 อยู่ที่ 1,312 ลบ. ลด 7.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ กำลังการผลิตและเครื่องจักรใหม่ และ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Assets As of December 31, 2025, the Company had total assets of 1,816.9 million baht, an increase of 7.4% compared to the end of 2024. Current assets amounted to 355.9 million baht, up 9.5%, primarily due to higher cash and cash equivalents and an increase in inventories to support sales in the upcoming quarter. Other current assets decreased, mainly due to the recognition of input tax refund receivables and a reduction in trade receivables in line with sales revenue. Non-current assets totaled 1,461.0 million baht, an increase of 6.9% from the end of 2024, mainly driven by additions to property, plant, and equipment, as well as assets under construction and installation including machinery,

  `MDA_PLUS_FY2025` · `p019` · SHA 599b43e23558
  </details>
- RFO ปี 2568 อยู่ที่ 1,312 ลบ. ลด 7.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ปริมาณขายและปริมาณการผลิต และ ความเสี่ยงด้านภูมิรัฐศาสตร์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Cost of sales The Company’s total cost of sales for the year 2025 amounted to 1,168.8 million baht, an increase of 26.5 million baht, or 2.3%, compared to the previous year. Variable costs, particularly direct raw material costs, decreased in line with lower sales volume, supported by effective procurement cost control. However, cost of sales accounted for 89.1% of sales revenue in 2025, compared to 80.3% in the previous year. This was primarily attributable to the development phase of the new Aseptic and Warm Fill plastic bottle production line. During this period, the Company incurred additional expenses related to machinery performance testing and product development, while production cap

  `MDA_PLUS_FY2025` · `p010` · SHA b89e30552340
  </details>
- RFO ปี 2568 อยู่ที่ 1,312 ลบ. ลด 7.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ มาตรการภาษีนำเข้าและข้อกีดกันทางการค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Overview of business operations Royal Plus Public Company Limited (the “Company”) reported its financial performance for the year ended December 31, 2025. The Company recorded total revenue of 1,325.6 million baht, a decrease of 7.4% compared to the same period of the previous year. This comprised sales revenue of 1,312.3 million baht, other income of 7.7 million baht, and a net foreign exchange gain of 5.6 million baht. Sales revenue declined by 110.8 million baht, or 7.8%, compared to the same period of the previous year. The decrease was primarily attributable to external factors, including trade protection measures, particularly tariff barriers on agricultural-based products in Europe, i

  `MDA_PLUS_FY2025` · `p004` · SHA c85f2e9ed25b
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 43m → FY2025 −THB 78m · −121m

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -78.2 ลบ. จากกำไร 43.0 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ การออกผลิตภัณฑ์ใหม่ และ กำลังการผลิตและเครื่องจักรใหม่ และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Profit (Loss) The Company reported a net loss of 78.2 million baht for 2025, representing of 6.0% of total sales revenue, a decline of 121.2 million baht, or 281.9%, compared to a net profit of 43.0 million baht in the same period of the previous year. The loss was primarily attributable to a decline in sales revenue in certain product categories, while the Company was in the initial phase of developing a new production line, which resulted in higher fixed costs. The rise in cost of sales, coupled with higher selling and administrative expenses, further contributed to a decline in the Company’s net profit margin. page3/5

  `MDA_PLUS_FY2025` · `p017` · SHA 37791932f6c3
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -78.2 ลบ. จากกำไร 43.0 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ การออกผลิตภัณฑ์ใหม่ และ กำลังการผลิตและเครื่องจักรใหม่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross profit The Company reported gross profit of 143.5 million baht for 2025, representing a decrease of 137.3 million baht, or 48.9%, compared to the same period of the previous year. Gross profit margin declined to 10.9%, compared with 19.7% in the prior year. The decrease was primarily attributable to the development phase of the new production line, which resulted in higher fixed costs, together with a slight decline in sales revenue. Nevertheless, the Company continues to place strong emphasis on cost control while enhancing product development to better meet evolving consumer demand. The Company is also expanding distribution channels both internationally and domestically to strengthe

  `MDA_PLUS_FY2025` · `p014` · SHA 94558948dbb6
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -78.2 ลบ. จากกำไร 43.0 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ปริมาณขายและปริมาณการผลิต และ ความเสี่ยงด้านภูมิรัฐศาสตร์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Cost of sales The Company’s total cost of sales for the year 2025 amounted to 1,168.8 million baht, an increase of 26.5 million baht, or 2.3%, compared to the previous year. Variable costs, particularly direct raw material costs, decreased in line with lower sales volume, supported by effective procurement cost control. However, cost of sales accounted for 89.1% of sales revenue in 2025, compared to 80.3% in the previous year. This was primarily attributable to the development phase of the new Aseptic and Warm Fill plastic bottle production line. During this period, the Company incurred additional expenses related to machinery performance testing and product development, while production cap

  `MDA_PLUS_FY2025` · `p010` · SHA b89e30552340
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -78.2 ลบ. จากกำไร 43.0 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Shareholder's Equity As of December 31, 2025, the Company’s total shareholders’ equity stood at 1,197.0 million baht, a decrease of 9.1% compared to the end of 2024. The decrease was primarily due to the dividend payment of 40.2 million baht from the Company’s 2024 operating results and the net loss of 78.2 million baht recorded in 2025. page4/5

  `MDA_PLUS_FY2025` · `p021` · SHA 25b2446373b3
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net gain (loss) in foreign exchange The Company recorded a net foreign exchange gain of 5.6 million baht in 2025, representing 0.4% of sales revenue. This compares to a net foreign exchange loss of 12.6 million baht in the same period of the previous year. The Company maintains a prudent and effective foreign exchange risk management policy, focusing on minimizing page2/5

  `MDA_PLUS_FY2025` · `p012` · SHA db4461c03921
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ มาตรการภาษีนำเข้าและข้อกีดกันทางการค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Overview of business operations Royal Plus Public Company Limited (the “Company”) reported its financial performance for the year ended December 31, 2025. The Company recorded total revenue of 1,325.6 million baht, a decrease of 7.4% compared to the same period of the previous year. This comprised sales revenue of 1,312.3 million baht, other income of 7.7 million baht, and a net foreign exchange gain of 5.6 million baht. Sales revenue declined by 110.8 million baht, or 7.8%, compared to the same period of the previous year. The decrease was primarily attributable to external factors, including trade protection measures, particularly tariff barriers on agricultural-based products in Europe, i

  `MDA_PLUS_FY2025` · `p004` · SHA c85f2e9ed25b
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_PLUS_FY2025`

#### ทะเบียนข้อสรุป — F4

| ส่วน | ประเภท | ข้อสรุป | รหัสแหล่งข้อมูล |
|---|---|---|---|
| headline | ข้ออนุมานนักวิเคราะห์ | กำไรที่โตจาก margin ช่วยรองรับ premium ของแบรนด์ | FY_PANEL, F4_E1, F4_E2 |
| earnings_fact | ข้อเท็จจริงจากการคำนวณ | FY2025 RFO -3.3%; สถานะ NPAT ส่วนผู้ถือหุ้น: profit_increased | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | รายได้ลดลงแต่ NPAT เพิ่ม โดย OSP เป็นตัวเพิ่มกำไรหลัก | FY_PANEL |
| why | คำอธิบายฝ่ายจัดการ | เครือข่ายจำหน่าย domestic mix และการคุมต้นทุนสำคัญกว่าการเติบโตของยอดขาย | F4_E1, F4_E2 |
| why | ข้อเท็จจริงจากการคำนวณ | CBG เป็นตัวผลักราคาหลัก ทำให้สัญญาณตลาดไม่ได้พึ่งบริษัทเดียว | FY_PANEL, SET_PUBLIC_EOD |
| causal_chain | ข้ออนุมานนักวิเคราะห์ | ห่วงโซ่เหตุ: ปริมาณ → แบรนด์ / mix → คุมต้นทุน → Margin → NPAT | F4_E1, F4_E2 |
| roles | ข้ออนุมานนักวิเคราะห์ | บทบาท: ผู้นำและตัวเพิ่มกำไร — OSP; ตัวผลักราคา — CBG | FY_PANEL, F4_E1, F4_E2 |
| valuation | ข้ออนุมานนักวิเคราะห์ | P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 17.2x ครอบคลุม 8/9 บริษัท และ 99.4% ของ market cap ที่มีข้อมูล. แบรนด์และช่องทางจำหน่ายสนับสนุน premium โดยมีเงื่อนไขว่า volume ต้องฟื้น | SET_PUBLIC_EOD, F4_E1, F4_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | ยอดขายในประเทศฟื้น | F4_E1, F4_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | product mix ดีขึ้น | F4_E1, F4_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | การส่งออกและกระจายสินค้าทำได้ตามแผน | F4_E1, F4_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | กำลังซื้ออ่อน | F4_E1, F4_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | การแข่งขันด้านโปรโมชั่น | F4_E1, F4_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | ต้นทุนบรรจุภัณฑ์และน้ำตาล | F4_E1, F4_E2 |
| must_prove | ประเด็นที่ต้องพิสูจน์ | 6M26 ต้องเพิ่มการฟื้นของ volume ต่อจาก margin ที่ดีขึ้นใน FY2025 | F4_E1, F4_E2 |

#### ทะเบียนหลักฐาน — F4

- **`FY_PANEL`** · _ข้อเท็จจริงจากการคำนวณ_ — Audited FY2024-25 company panel
  - RFO / NPAT-to-owners / independent panel membership; QA 43 pass / 0 fail
  - บทบาท: historical fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_company_fy2024_2025_audited_2026-08-07.csv`
  - SHA-256: `e5e04dbc40ffcc79fed58545a93dc4549c29cdaecf260bea73711bc6d0720481`
- **`SET_PUBLIC_EOD`** · _ข้อเท็จจริงจากการคำนวณ_ — SET public Company Highlights — EOD 2026-08-07
  - Adjusted YTD; unadjusted price, market cap and valuation; factsheet-surface cross-check
  - บทบาท: current market fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_set_public_surface_reconciliation_2026-08-07.csv`
  - SHA-256: `544c1f29fe2d409ee398822ac2bf32b769081718962ae2d1138985b0146b9530`
- **`SET_COMPANY_PROFILE`** · _ข้อเท็จจริง_ — SET company profiles — English and Thai
  - Official company names and business descriptions refreshed and validated for the 118-company perimeter from the public SET profile API
  - บทบาท: company business profile
  - URL: <https://www.set.or.th/th/market/product/stock/overview>
- **`COMPANY_REPORTS`** · _ข้ออนุมานนักวิเคราะห์_ — Company report synthesis corpus
  - Annual-only draft synthesis; reconciled to the ticker FY2025 MD&A where available
  - บทบาท: secondary synthesis; not management attribution
  - พาธ: `data/company-reports.json`
  - SHA-256: `c1a2bc40cbe21a2058aa596c362e4d47ad117360831b847de78ec414831fd2d2`
- **`MDA_OSP_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — OSP FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/OSP/MDA_OSP_2025FY_E.md`
  - SHA-256: `323015cc37c85e9aaf0a950f0281ff7db1ef946f0b657d6b7be67c478b76f592`
  - URL: <https://weblink.set.or.th/dat/news/202602/1450NWS250220261911372340E.pdf>
- **`MDA_CBG_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — CBG FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/CBG/MDA_CBG_2025FY_E.md`
  - SHA-256: `995510d6dac07721416f62d70c729f7df047e259097b078b13684abd561b57a8`
  - URL: <https://weblink.set.or.th/dat/news/202602/1200NWS200220262120051500E.pdf>
- **`MDA_ICHI_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — ICHI FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/ICHI/MDA_ICHI_2025FY_E.md`
  - SHA-256: `8b193276ba92ee2772dd5e35495ec5f26f78042ec1b049bbcdb9fade969a23aa`
  - URL: <https://weblink.set.or.th/dat/news/202602/1178NWS190220261717276750E.pdf>
- **`MDA_SAPPE_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — SAPPE FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SAPPE/MDA_SAPPE_2025FY_E.md`
  - SHA-256: `2cb86c8e85afd557c052fb6a025e447faadedb725edc6260c7d656e2dd8de30b`
  - URL: <https://weblink.set.or.th/dat/news/202602/1190NWS270220260733539490E.pdf>
- **`MDA_COCOCO_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — COCOCO FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/COCOCO/MDA_COCOCO_2025FY_E.md`
  - SHA-256: `3a2562b931e7623b9438ee7675a9dc09c2e512abb58bebaf1a2b743ed5aff013`
  - URL: <https://weblink.set.or.th/dat/news/202602/1830NWS250220262106089810E.pdf>
- **`MDA_HTC_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — HTC FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/HTC/MDA_HTC_2025FY_E.md`
  - SHA-256: `70b688c5b5356cf7f14a6dd0db8729a0875210228bc6d0df9419af018ea5065a`
  - URL: <https://weblink.set.or.th/dat/news/202603/0140NWS020320261230450980E.pdf>
- **`MDA_TIPCO_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — TIPCO FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/TIPCO/MDA_TIPCO_2025FY_E.md`
  - SHA-256: `f086b21ad1d8a192b6641e57d8b534db4952d38a1f1c58684815a6cce27d6c5b`
  - URL: <https://weblink.set.or.th/dat/news/202602/0154NWS200220261753313150E.pdf>
- **`MDA_MALEE_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — MALEE FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/MALEE/MDA_MALEE_2025FY_E.md`
  - SHA-256: `1eba81100e9d154f84344e5a37055bc5c949898c007533647c98f8e3eeeb62f5`
  - URL: <https://weblink.set.or.th/dat/news/202602/0293NWS250220262041292120E.pdf>
- **`MDA_PLUS_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — PLUS FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/PLUS/MDA_PLUS_2025FY_E.md`
  - SHA-256: `078e55bc53d13681fc27e59ab4141a1ce8eb495be5181330da87bebf011ab13a`
  - URL: <https://weblink.set.or.th/dat/news/202602/1692NWS200220261747044250E.pdf>
- **`F4_E1`** · _ฝ่ายจัดการ_ — OSP FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/OSP/MDA_OSP_2025FY_E.md`
  - SHA-256: `323015cc37c85e9aaf0a950f0281ff7db1ef946f0b657d6b7be67c478b76f592`
- **`F4_E2`** · _มุมมองล่วงหน้า_ — BLS CBG research
  - Historical explanation or forward cross-check; see source role
  - บทบาท: forward/credit context
  - พาธ: `Listed Company/1-Raw/06-Market Reference/Broker Research/2026/FOOD/BLS_CBG_345849.md`
  - SHA-256: `0c678edb6761e74c03d7cd507d81faa31240e6570dfb66d6fb732657ade23b8e`
- **`F4_FACTSHEET`** · _ข้อเท็จจริงจากการคำนวณ_ — SET Factsheet — OSP
  - Live leader cross-check
  - บทบาท: presentation-surface check
  - URL: <https://www.set.or.th/th/market/product/stock/quote/osp/factsheet>

### F6 · อาหารหลัก ขนม และเบเกอรี่ — ขนาดและความ defensive ช่วยพยุง valuation แต่กำไรอ่อนลง

`ยังถูกกดดัน` · 15.3% M-cap · THB 124bn · 9 บริษัท

| ตัวชี้วัด | RFO | NPAT | ราคา | P/E |
|---|---|---|---|---|
| ช่วง | FY2025 YoY | ส่วนผู้ถือหุ้น FY2025 YoY | ราคา YTD ปรับแล้ว | เฉพาะบริษัทที่มีกำไร |
| ค่า | 0.0% | -14.3% | -0.2% | 15.5x |
| จำนวน | THB 71.2bn FY2025 | THB 8.3bn FY2025 | ณ 7 ส.ค. 2569 | ค่าเฉลี่ยรวม |
| ครอบคลุม | 9/9 | 9/9 | 9/9 • 100% M-cap | 9/9 • 100% M-cap |

**ข้อเท็จจริงที่สังเกตได้** — FY2025: RFO 0.0% • NPAT -14.3% • ราคา YTD -0.2% • P/E 15.5x • ครอบคลุม RFO 9/9 • NPAT 9/9

#### เหตุผลที่เปลี่ยน

1. _ข้อเท็จจริงจากการคำนวณ_ · อุปสงค์ในประเทศ — RFO ทรงตัวแต่ NPAT ลด สะท้อน margin compression
2. _ข้อเท็จจริงจากการคำนวณ_ · ส่งออก — TFMAMA มีสัดส่วนประมาณครึ่งกลุ่มและเป็นตัวฉุดกำไรหลัก
3. _ข้อเท็จจริงจากการคำนวณ_ · ต้นทุนวัตถุดิบ — NSL เป็นตัวเพิ่มรายได้ที่ชัดที่สุด

#### ห่วงโซ่เหตุและผล

**อุปสงค์ในประเทศ** → **ส่งออก** → **ต้นทุนวัตถุดิบ** → **Margin** (11.6% -1.9 ppt YoY) → **NPAT** (-14.3% THB 8.3bn FY2025)

#### บทบาทในกลุ่ม

| บทบาท | Ticker | ค่า | ที่มาของค่า |
|---|---|---|---|
| ผู้นำและตัวฉุดกำไร | TFMAMA | 50% | สัดส่วน Market Cap ในกลุ่ม |
| ตัวเพิ่ม RFO | NSL | +18.5% | RFO YoY · Δ +1.1bn |

#### มูลค่า

**แรงกดดันปัจจุบัน / ข้อเท็จจริง** — P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 15.5x ครอบคลุม 9/9 บริษัท และ 100.0% ของ market cap ที่มีข้อมูล. แบรนด์ defensive พยุงมูลค่า แต่ RFO ที่ทรงตัวจำกัด upside

| Trigger | Risk |
|---|---|
| คำสั่งซื้อส่งออกฟื้น | ตลาดในประเทศโตต่ำ |
| ต้นทุนวัตถุดิบผ่อนคลาย | วัตถุดิบแพงขึ้น |
| สินค้าใหม่ช่วยเพิ่มรายได้ | ส่งออกอ่อนตัว |

**6M26 ต้องพิสูจน์** — 6M26 ต้องกลับมาโตด้านกำไรโดยยังรักษากระแสเงินสดแบบ defensive

#### วิเคราะห์รายบริษัท — F6 อาหารหลัก ขนม และเบเกอรี่

_ทุกบริษัทใน perimeter ของ Segment ที่สอบทาน_

| Ticker | บทบาท | M-cap | RFO YoY | NPAT YoY | ราคา YTD | P/E | Margin |
|---|---|---|---|---|---|---|---|
| TFMAMA | ผู้นำและตัวฉุดกำไร | THB 61.7bn | -6.6% | -17.3% | -2.9% | 17.1x | 13.4% |
| PB | บริษัทในกลุ่ม | THB 21.6bn | -5.9% | -20.9% | -4.0% | 17.8x | 17.9% |
| PRG | บริษัทในกลุ่ม | THB 8.4bn | +13.1% | +39.2% | +22.2% | 14.0x | 22.3% |
| NSL | ตัวเพิ่ม RFO | THB 6.9bn | +18.5% | +11.7% | -0.9% | 11.5x | 8.7% |
| SNNP | บริษัทในกลุ่ม | THB 6.4bn | -5.4% | -20.4% | -3.4% | 15.7x | 9.2% |
| PM | บริษัทในกลุ่ม | THB 6.4bn | +20.3% | +3.6% | -4.2% | 11.5x | 10.5% |
| TKN | บริษัทในกลุ่ม | THB 5.9bn | -7.1% | -51.0% | +7.0% | 14.2x | 7.7% |
| KCG | บริษัทในกลุ่ม | THB 5.7bn | +11.6% | +24.0% | +27.3% | 10.7x | 5.8% |
| CHAO | บริษัทในกลุ่ม | THB 1.2bn | -9.7% | -47.3% | -8.4% | 15.8x | 5.0% |

##### TFMAMA — ผู้นำและตัวฉุดกำไร · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ไทยเพรซิเดนท์ฟูดส์ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ธุรกิจหลักของบริษัทฯคือ ผลิตและจำหน่ายบะหมี่และอาหารกึ่งสำเร็จรูป ขนมปังกรอบ

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 61.7bn | 187.00 | -2.9% | 17.1x | 13.4% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 18 · NPAT 12 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 29.6bn → FY2025 THB 27.6bn · −2.0bn · -6.6%

- RFO ปี 2568 อยู่ที่ 27,649 ลบ. ลด 6.6% YoY; MD&A ระบุว่า รายได้จากการขาย ในปี2568 บริษัทฯมีรายได้จากการขายรวม27,649.40 ล้านบาทลดลง1,956.60 ล้านบาทหรือร้อยละ6.61 จากปีก่อนหน้าโดยยอดขายเฉพาะกิจการ(TFMAMA) ลดลงร้อยละ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้จากการขาย ในปี2568 บริษัทฯมีรายได้จากการขายรวม27,649.40 ล้านบาทลดลง1,956.60 ล้านบาทหรือร้อยละ6.61 จากปีก่อนหน้าโดยยอดขายเฉพาะกิจการ(TFMAMA) ลดลงร้อยละ

  `MDA_TFMAMA_FY2025` · `p017` · SHA 669de1348965
  </details>
- RFO ปี 2568 อยู่ที่ 27,649 ลบ. ลด 6.6% YoY; MD&A ระบุว่า สินค้าอันเป็นผลจากสถานการณ์ความไม่สงบบริเวณชายแดนไทย-กัมพูชาในบางพื้นที่ กลุ่มบรรจุภัณฑ์มีสัดส่วนร้อยละ4.51 ของยอดขายภายในประเทศและยอดขายลดลง y
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > สินค้าอันเป็นผลจากสถานการณ์ความไม่สงบบริเวณชายแดนไทย-กัมพูชาในบางพื้นที่ กลุ่มบรรจุภัณฑ์มีสัดส่วนร้อยละ4.51 ของยอดขายภายในประเทศและยอดขายลดลง y

  `MDA_TFMAMA_FY2025` · `p040` · SHA bf6ea0f244dc
  </details>
- RFO ปี 2568 อยู่ที่ 27,649 ลบ. ลด 6.6% YoY; MD&A ระบุว่า จากปีก่อนหน้าโครงสร้างรายได้หลักอยู่ในภูมิภาคเอเชียคิดเป็นร้อยละ43.4 ของรายได้ ต่างประเทศรองลงมาคือยุโรปร้อยละ30.0 สหรัฐอเมริการ้อยละ17.1 ออสเตรเลียร้อยละ4.8
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > จากปีก่อนหน้าโครงสร้างรายได้หลักอยู่ในภูมิภาคเอเชียคิดเป็นร้อยละ43.4 ของรายได้ ต่างประเทศรองลงมาคือยุโรปร้อยละ30.0 สหรัฐอเมริการ้อยละ17.1 ออสเตรเลียร้อยละ4.8

  `MDA_TFMAMA_FY2025` · `p045` · SHA b41b4b8f5d0a
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 4.5bn → FY2025 THB 3.7bn · −774m · -17.3%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 3,708 ลบ. ลด 17.3% YoY; MD&A ระบุว่า หรือร้อยละ 17.27 จากปีก่อนหน้าอัตรากำไรสุทธิอยู่ที่ร้อยละ12.81 ขณะทีกำไรสุทธิ ของงบเฉพาะกิจการ(TFMAMA) อยู่ที่3,000.62 ล้านบาทลดลงร้อยละ15.84
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > หรือร้อยละ 17.27 จากปีก่อนหน้าอัตรากำไรสุทธิอยู่ที่ร้อยละ12.81 ขณะทีกำไรสุทธิ ของงบเฉพาะกิจการ(TFMAMA) อยู่ที่3,000.62 ล้านบาทลดลงร้อยละ15.84

  `MDA_TFMAMA_FY2025` · `p058` · SHA 9649391ddab2
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 3,708 ลบ. ลด 17.3% YoY; MD&A ระบุว่า บริษั ทฯรับรู้ส่วนแบ่งกำไรจากเงินลงทุนตามวิธีส่วนได้ส่วนเสียจำนวน109.31 ล้านบาท ลดลงร้อยละ45.54 จากปีก่อนหน้าสาเหตุหลักมาจากผลประกอบการของบริษัทร่วมทีปรับตัว
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > บริษั ทฯรับรู้ส่วนแบ่งกำไรจากเงินลงทุนตามวิธีส่วนได้ส่วนเสียจำนวน109.31 ล้านบาท ลดลงร้อยละ45.54 จากปีก่อนหน้าสาเหตุหลักมาจากผลประกอบการของบริษัทร่วมทีปรับตัว

  `MDA_TFMAMA_FY2025` · `p056` · SHA 3d9fbb76590f
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 3,708 ลบ. ลด 17.3% YoY; MD&A ระบุว่า Aw i.) a vy ปี2567 เป็นจำนวน2,251.38 ล้านบาท หรือร้อยละ5.04 เนื่องจากบริษัทฯมีกำไรสุทธิเข้ามาใน
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > Aw i.) a vy ปี2567 เป็นจำนวน2,251.38 ล้านบาท หรือร้อยละ5.04 เนื่องจากบริษัทฯมีกำไรสุทธิเข้ามาใน

  `MDA_TFMAMA_FY2025` · `p083` · SHA 3ba9891bdb57
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 3,708 ลบ. ลด 17.3% YoY; MD&A ระบุว่า ก่อนหน้าสาเหตุหลักมาจากต้นทุนนำมันปาล์มซึ่งเป็นวัตถุดิบหลักในการผลิตบะหมีและอาหาร
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ก่อนหน้าสาเหตุหลักมาจากต้นทุนนำมันปาล์มซึ่งเป็นวัตถุดิบหลักในการผลิตบะหมีและอาหาร

  `MDA_TFMAMA_FY2025` · `p050` · SHA f8ecfa87d609
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_TFMAMA_FY2025`

##### PB — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท เพรซิเดนท์ เบเกอรี่ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและจำหน่ายขนมปัง และเบเกอรี่ ภายใต้แบรนด์ ฟาร์มเฮ้าส์ โดยมีสายธุรกิจแบ่งเป็น 1. ธุรกิจเบเกอรี่ค้าส่ง 2. ธุรกิจค้าปลีก 3. ธุรกิจฟาสต์ฟู้ด 4. ขายต่างประเทศ (ผ่านผู้ค้าในประเทศ)

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 21.6bn | 48.00 | -4.0% | 17.8x | 17.9% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 6 · NPAT 4 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 7.5bn → FY2025 THB 7.0bn · −444m · -5.9%

- RFO ปี 2568 อยู่ที่ 7,036 ลบ. ลด 5.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ กำลังการผลิตและเครื่องจักรใหม่ และ ค่าเสื่อมราคาและค่าตัดจำหน่าย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Cost of Sales In 2025, cost of sales amounted to Baht 3,918.26 million, decreasing by Baht 133.01 million or 3.28% from Baht 4,051.27 million in 2024. The reduction was mainly in line with lower sales and reduced prices of key raw materials, although certain raw material costs increased. Additionally, personnel expenses rose due to the minimum wage adjustment announced by the Ministry of Labour, along with higher depreciation expenses from newly installed production line machinery. As a result, the gross profit margin declined to 44.31% from 45.84% in the previous year

  `MDA_PB_FY2025` · `p006` · SHA ba45ac02a0a8
  </details>
- RFO ปี 2568 อยู่ที่ 7,036 ลบ. ลด 5.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ อุปสงค์และกำลังซื้อในประเทศ และ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Sales In 2025, the Company generated sales revenue of Baht 7,036.05 million, representing 99.11% of total revenue. This decreased from Baht 7,480.31 million in 2024, a decline of Baht 444.26 million or 5.94% year-on-year. The decrease was primarily attributable to the economic slowdown, intensified market competition, and product price adjustments in line with lower prices of key raw materials.

  `MDA_PB_FY2025` · `p005` · SHA 42c297a6662c
  </details>
- RFO ปี 2568 อยู่ที่ 7,036 ลบ. ลด 5.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าเสื่อมราคาและค่าตัดจำหน่าย และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Selling and Administrative expenses In 2025, selling and administrative expenses totaled Baht 1,880.32 million, representing 26.49% of total revenue. This reflects an increase of Baht 82.72 million or 4.60% compared with 2024. The increase was mainly due to annual salary adjustments, depreciation of newly acquired vehicles replacing long-used trucks, depreciation of vending machines, and depreciation of the newly completed distribution center building now ready for operation.

  `MDA_PB_FY2025` · `p007` · SHA c090e8e05dd3
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 1.6bn → FY2025 THB 1.3bn · −333m · -20.9%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,258 ลบ. ลด 20.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ กำลังการผลิตและเครื่องจักรใหม่ และ ค่าเสื่อมราคาและค่าตัดจำหน่าย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Cost of Sales In 2025, cost of sales amounted to Baht 3,918.26 million, decreasing by Baht 133.01 million or 3.28% from Baht 4,051.27 million in 2024. The reduction was mainly in line with lower sales and reduced prices of key raw materials, although certain raw material costs increased. Additionally, personnel expenses rose due to the minimum wage adjustment announced by the Ministry of Labour, along with higher depreciation expenses from newly installed production line machinery. As a result, the gross profit margin declined to 44.31% from 45.84% in the previous year

  `MDA_PB_FY2025` · `p006` · SHA ba45ac02a0a8
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,258 ลบ. ลด 20.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Shareholders' Equity As of 31 December 2025, shareholders’ equity totaled Baht 12,860.02 million, an increase of Baht 416.69 million or 3.35% from 31 December 2024. The increase was mainly attributable to net profit for the year of Baht 1,257.69 million, offset by dividend payments totaling Baht 774 million.

  `MDA_PB_FY2025` · `p022` · SHA 1e265613f252
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,258 ลบ. ลด 20.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Profit for the year The Company reported net profit of Baht 1, 257. 69 million in 2025, representing 17.72% of total revenue. This marked a decrease of Baht 332.90 million or 20.93% compared with 2024. In addition, the Company recognized a share of profit from investment in a joint venture amounting to Baht 0.35 million for the year ended 31 December 2025.

  `MDA_PB_FY2025` · `p008` · SHA 830213b9ed8d
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,258 ลบ. ลด 20.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Remark: Percentage in Statement of comprehensive income derived from total revenues, while percentage of cost of sales and gross profit from sales.

  `MDA_PB_FY2025` · `p004` · SHA 99102d8c8130
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_PB_FY2025`

##### PRG — บริษัทในกลุ่ม · ติดตาม

**บริษัท พี อาร์ จี คอร์ปอเรชั่น จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — เป็นผู้ผลิตและจำหน่ายข้าวสารในประเทศ ธุรกิจศูนย์อาหาร ธุรกิจพัฒนาที่ดินและอสังหาริมทรัพย์ และธุรกิจที่เกี่ยวข้อง

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 8.4bn | 11.00 | +22.2% | 14.0x | 22.3% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 7 · NPAT 9 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 2.4bn → FY2025 THB 2.7bn · +309m · +13.1%

- RFO ปี 2568 อยู่ที่ 2,678 ลบ. เพิ่ม 13.1% YoY; MD&A ระบุว่า วันที่ 31 ธันวาคม 2568 2567 เพิ่มขึ้น/ลดลง 1) รายได้จากการขาย 2,633.3 2,331.5 301.8 13% 2) รายได้จากการให้เช่าและบริการ 44.6 37.2 7.4 20% 3) รายได้เงินปันผล 584.1 496.6 87.4 18% 4) รายได้อื่น 13.3 12.4 0.9 7% 5) รวมรายได้ 3,275.2 2,877.7 397.6 14% 6) ต้นทุนขาย 2,376.9 2,133.1 243.9 11% 7) ต้นทุนการให้เช่าและบริการ 45.6 36.6 9.1 25% 8) ค่าใช้จ่ายในการขายและจัดจำหน่าย 151.4 168.8 (17.5) -10% 9) ค่าใช้จ่ายในการบริหาร 95.5 90.4 5.2 6% 10) ค่าใช้จ่ายอื่น - 0.1 (0.1) -100% 11) รวมค่าใช้จ่าย 2,669.5 2,428.9 240.5 10% 12) กำไรจากการดำเนินงาน 605.8 448.7 157.0 35
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > วันที่ 31 ธันวาคม 2568 2567 เพิ่มขึ้น/ลดลง 1) รายได้จากการขาย 2,633.3 2,331.5 301.8 13% 2) รายได้จากการให้เช่าและบริการ 44.6 37.2 7.4 20% 3) รายได้เงินปันผล 584.1 496.6 87.4 18% 4) รายได้อื่น 13.3 12.4 0.9 7% 5) รวมรายได้ 3,275.2 2,877.7 397.6 14% 6) ต้นทุนขาย 2,376.9 2,133.1 243.9 11% 7) ต้นทุนการให้เช่าและบริการ 45.6 36.6 9.1 25% 8) ค่าใช้จ่ายในการขายและจัดจำหน่าย 151.4 168.8 (17.5) -10% 9) ค่าใช้จ่ายในการบริหาร 95.5 90.4 5.2 6% 10) ค่าใช้จ่ายอื่น - 0.1 (0.1) -100% 11) รวมค่าใช้จ่าย 2,669.5 2,428.9 240.5 10% 12) กำไรจากการดำเนินงาน 605.8 448.7 157.0 35% 13) รายได้ทางการเงิน 0.2 0.2 0.0 2% 14) ต้นทุนการการเงิน (7.3) (15.8) 8.5 -54% 15) กำไรก่อนภาษีเงินได้ 598.7 433.1 165.6 38% 16) ค่าใช้จ่า

  `MDA_PRG_FY2025` · `p005` · SHA 117cd9c615d2
  </details>
- RFO ปี 2568 อยู่ที่ 2,678 ลบ. เพิ่ม 13.1% YoY; MD&A ระบุว่า ผลการดำเนินงานสำหรับปี 2568 ในภาพรวมกลุ่มบริษัทมีกำไรสุทธิสำหรับปีสิ้นสุดวันที่ 31 ธันวาคม 2568 จำนวนเงิน 597.3 ล้านบาท โดยเพิ่มขึ้นจากปีก่อน 168.2 ล้านบาทหรือร้อยละ 39 นั้นมาจากรายได้ของบริษัทที่เพิ่มขึ้นจากการขาย การให้เช่าและบริการ และรายได้เงินปันผล ซึ่งรายได้รวมปี 2568 เพิ่มขึ้น 397.6 ล้านบาท หรือคิดเป็นร้อยละ 14 โดยจะอธิบายไว้เพิ่มเติมในรายได้จำแนกตามส่วนงานหน้าถัดไป
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ผลการดำเนินงานสำหรับปี 2568 ในภาพรวมกลุ่มบริษัทมีกำไรสุทธิสำหรับปีสิ้นสุดวันที่ 31 ธันวาคม 2568 จำนวนเงิน 597.3 ล้านบาท โดยเพิ่มขึ้นจากปีก่อน 168.2 ล้านบาทหรือร้อยละ 39 นั้นมาจากรายได้ของบริษัทที่เพิ่มขึ้นจากการขาย การให้เช่าและบริการ และรายได้เงินปันผล ซึ่งรายได้รวมปี 2568 เพิ่มขึ้น 397.6 ล้านบาท หรือคิดเป็นร้อยละ 14 โดยจะอธิบายไว้เพิ่มเติมในรายได้จำแนกตามส่วนงานหน้าถัดไป

  `MDA_PRG_FY2025` · `p006` · SHA bc7ed9c5f319
  </details>
- RFO ปี 2568 อยู่ที่ 2,678 ลบ. เพิ่ม 13.1% YoY; MD&A ระบุว่า วันที่ 31 ธันวาคม วันที่ 31 ธันวาคม 2568 2567 เพิ่มขึ้น/ลดลง 2568 2567 เพิ่มขึ้น/ลดลง ธุรกิจปรับปรุงคุณภาพและบรรจุข้าวสาร 2,435.8 2,131.6 304.1 14% 39.6 (50.6) 90.1 178% ธุรกิจศูนย์อาหาร 217.1 217.9 (0.8) 0% 16.6 14.0 2.6 18% ธุรกิจบริหารสินทรัพย์ 23.6 22.3 1.3 6% (19.2) (15.3) (3.9) -26% ธุรกิจพลังงานแสงอาทิตย์ 7.9 - 7.9 100% (3.1) - (3.1) 100% การตัดรายการบัญชีระหว่างกัน (6.4) (3.1) (3.3) 200% (4.5) 0.0 (4.5) 200% รวมทั้งสิ้น 2,677.9 2,368.7 309.2 13% 29.3 (51.9) 81.2 157% รายได้จากการขายจำแนกตามส่วนงานสำหรับปี 2568 โดยภาพรวมกลุ่มบริษัทมีรายได้จากลูกค้
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > วันที่ 31 ธันวาคม วันที่ 31 ธันวาคม 2568 2567 เพิ่มขึ้น/ลดลง 2568 2567 เพิ่มขึ้น/ลดลง ธุรกิจปรับปรุงคุณภาพและบรรจุข้าวสาร 2,435.8 2,131.6 304.1 14% 39.6 (50.6) 90.1 178% ธุรกิจศูนย์อาหาร 217.1 217.9 (0.8) 0% 16.6 14.0 2.6 18% ธุรกิจบริหารสินทรัพย์ 23.6 22.3 1.3 6% (19.2) (15.3) (3.9) -26% ธุรกิจพลังงานแสงอาทิตย์ 7.9 - 7.9 100% (3.1) - (3.1) 100% การตัดรายการบัญชีระหว่างกัน (6.4) (3.1) (3.3) 200% (4.5) 0.0 (4.5) 200% รวมทั้งสิ้น 2,677.9 2,368.7 309.2 13% 29.3 (51.9) 81.2 157% รายได้จากการขายจำแนกตามส่วนงานสำหรับปี 2568 โดยภาพรวมกลุ่มบริษัทมีรายได้จากลูกค้าภายนอกสำหรับปี 2568 จำนวน รวม 2,677.9 ล้านบาท เพิ่มขึ้น 309.2 ล้านบาทหรือร้อยละ 13 โดยหลักเพิ่มมาจากธุรกิจปรับปรุงคุณภาพและบรรจุข้าวสารจากก

  `MDA_PRG_FY2025` · `p007` · SHA b61d6152b6fd
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 429m → FY2025 THB 597m · +168m · +39.2%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 597 ลบ. เพิ่ม 39.2% YoY; MD&A ระบุว่า การวิเคราะห์ต้นทุนและค่าใช้จ่าย • ต้นทุนขาย ต้นทุนขายสำหรับปีเพิ่มจากปีก่อนโดยสัดส่วนที่เพิ่มขึ้นของต้นทุนขายต่ำกว่าเมื่อเทียบกับร้อยละของรายได้ที่เพิ่มขึ้น โดยต้นทุน ขายสำหรับปีเพิ่มจากปีก่อนในอัตราร้อยละ 11 จากการที่บริษัทบริหารจัดการต้นทุนในการผลิตที่ดียิ่งขึ้น และจากการปรับเปลี่ยนกลยุทธ์
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > การวิเคราะห์ต้นทุนและค่าใช้จ่าย • ต้นทุนขาย ต้นทุนขายสำหรับปีเพิ่มจากปีก่อนโดยสัดส่วนที่เพิ่มขึ้นของต้นทุนขายต่ำกว่าเมื่อเทียบกับร้อยละของรายได้ที่เพิ่มขึ้น โดยต้นทุน ขายสำหรับปีเพิ่มจากปีก่อนในอัตราร้อยละ 11 จากการที่บริษัทบริหารจัดการต้นทุนในการผลิตที่ดียิ่งขึ้น และจากการปรับเปลี่ยนกลยุทธ์

  `MDA_PRG_FY2025` · `p009` · SHA 47e9857905c8
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 597 ลบ. เพิ่ม 39.2% YoY; MD&A ระบุว่า วันที่ 31 ธันวาคม 2568 2567 เพิ่มขึ้น/ลดลง 1) รายได้จากการขาย 2,633.3 2,331.5 301.8 13% 2) รายได้จากการให้เช่าและบริการ 44.6 37.2 7.4 20% 3) รายได้เงินปันผล 584.1 496.6 87.4 18% 4) รายได้อื่น 13.3 12.4 0.9 7% 5) รวมรายได้ 3,275.2 2,877.7 397.6 14% 6) ต้นทุนขาย 2,376.9 2,133.1 243.9 11% 7) ต้นทุนการให้เช่าและบริการ 45.6 36.6 9.1 25% 8) ค่าใช้จ่ายในการขายและจัดจำหน่าย 151.4 168.8 (17.5) -10% 9) ค่าใช้จ่ายในการบริหาร 95.5 90.4 5.2 6% 10) ค่าใช้จ่ายอื่น - 0.1 (0.1) -100% 11) รวมค่าใช้จ่าย 2,669.5 2,428.9 240.5 10% 12) กำไรจากการดำเนินงาน 605.8 448.7 157.0 35
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > วันที่ 31 ธันวาคม 2568 2567 เพิ่มขึ้น/ลดลง 1) รายได้จากการขาย 2,633.3 2,331.5 301.8 13% 2) รายได้จากการให้เช่าและบริการ 44.6 37.2 7.4 20% 3) รายได้เงินปันผล 584.1 496.6 87.4 18% 4) รายได้อื่น 13.3 12.4 0.9 7% 5) รวมรายได้ 3,275.2 2,877.7 397.6 14% 6) ต้นทุนขาย 2,376.9 2,133.1 243.9 11% 7) ต้นทุนการให้เช่าและบริการ 45.6 36.6 9.1 25% 8) ค่าใช้จ่ายในการขายและจัดจำหน่าย 151.4 168.8 (17.5) -10% 9) ค่าใช้จ่ายในการบริหาร 95.5 90.4 5.2 6% 10) ค่าใช้จ่ายอื่น - 0.1 (0.1) -100% 11) รวมค่าใช้จ่าย 2,669.5 2,428.9 240.5 10% 12) กำไรจากการดำเนินงาน 605.8 448.7 157.0 35% 13) รายได้ทางการเงิน 0.2 0.2 0.0 2% 14) ต้นทุนการการเงิน (7.3) (15.8) 8.5 -54% 15) กำไรก่อนภาษีเงินได้ 598.7 433.1 165.6 38% 16) ค่าใช้จ่า

  `MDA_PRG_FY2025` · `p005` · SHA 117cd9c615d2
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 597 ลบ. เพิ่ม 39.2% YoY; MD&A ระบุว่า วิเคราะห์อัตราส่วนทางการเงินที่สำคัญ อัตรากำไรสุทธิเพิ่มขึ้นร้อยละ 4.33 อัตรากำไรขั้นต้นเพิ่มขึ้นร้อยละ 1.23 และกำไรสุทธิต่อหุ้นเพิ่มขึ้น 0.18 บาท จากรายได้ ที่เพิ่มขึ้นและต้นทุนที่ลดลงส่งผลดีต่อทั้งอัตราผลตอบแทนต่อผู้ถือหุ้นและผลตอบแทนต่อสินทรัพย์รวมด้วย อีกทั้งในด้านอัตราส่วนสภาพ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > วิเคราะห์อัตราส่วนทางการเงินที่สำคัญ อัตรากำไรสุทธิเพิ่มขึ้นร้อยละ 4.33 อัตรากำไรขั้นต้นเพิ่มขึ้นร้อยละ 1.23 และกำไรสุทธิต่อหุ้นเพิ่มขึ้น 0.18 บาท จากรายได้ ที่เพิ่มขึ้นและต้นทุนที่ลดลงส่งผลดีต่อทั้งอัตราผลตอบแทนต่อผู้ถือหุ้นและผลตอบแทนต่อสินทรัพย์รวมด้วย อีกทั้งในด้านอัตราส่วนสภาพ

  `MDA_PRG_FY2025` · `p018` · SHA a391eb08e819
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 597 ลบ. เพิ่ม 39.2% YoY; MD&A ระบุว่า เพิ่มขึ้นจากธุรกิจบริหารทรัพย์สิน เนื่องจากมีค่าเสื่อมราคาเพิ่มขึ้น • ค่าใช้จ่ายในการขายและจัดจำหน่าย ค่าใช้จ่ายในการขายและจัดจำหน่ายเมื่อเทียบกับปีก่อนลดลงจำนวนเงิน 17.5 ล้านบาท หรือร้อยละ 10 ส่วนใหญ่เกิดจากการ ยกเลิกส่วนงานการส่งออกข้าวทำให้ไม่มีค่าใช้จ่ายเกี่ยวกับการส่งออกแล้ว เช่น ค่าระวางเรือซึ่งลดลงจำนวน 17.9 ล้านบาท และนอกจากนั้น บริษัทบริหารค่าใช้จ่ายบุคลากรได้ดียิ่งขึ้นโดยมีค่าใช้จ่ายบุคลากรลดลงสำหรับปีจำนวน 7.48 ล้านบาท หรือร้อยละ 17.8 • ค่าใช้จ่ายในการบริหาร ค่าใช้จ่ายในการบริหารสำหรับปีเพิ่มขึ้นจำนวนเงิน 5.2 ล้านบาทโดยส่วนใหญ่เพิ่มขึ้นจากค่าน
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > เพิ่มขึ้นจากธุรกิจบริหารทรัพย์สิน เนื่องจากมีค่าเสื่อมราคาเพิ่มขึ้น • ค่าใช้จ่ายในการขายและจัดจำหน่าย ค่าใช้จ่ายในการขายและจัดจำหน่ายเมื่อเทียบกับปีก่อนลดลงจำนวนเงิน 17.5 ล้านบาท หรือร้อยละ 10 ส่วนใหญ่เกิดจากการ ยกเลิกส่วนงานการส่งออกข้าวทำให้ไม่มีค่าใช้จ่ายเกี่ยวกับการส่งออกแล้ว เช่น ค่าระวางเรือซึ่งลดลงจำนวน 17.9 ล้านบาท และนอกจากนั้น บริษัทบริหารค่าใช้จ่ายบุคลากรได้ดียิ่งขึ้นโดยมีค่าใช้จ่ายบุคลากรลดลงสำหรับปีจำนวน 7.48 ล้านบาท หรือร้อยละ 17.8 • ค่าใช้จ่ายในการบริหาร ค่าใช้จ่ายในการบริหารสำหรับปีเพิ่มขึ้นจำนวนเงิน 5.2 ล้านบาทโดยส่วนใหญ่เพิ่มขึ้นจากค่านายหน้าขายที่ดินในบริษัทย่อยเป็น จำนวนเงินประมาณ 3.3 ล้านบาท • ต้นทุนทางการเงิน ต้นทุนทางการเงินสำหรับปีลดลงจากอัตราดอกเบี้ยธนาคารลดลงเมื่อเท

  `MDA_PRG_FY2025` · `p011` · SHA 4d45c5b66b29
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_PRG_FY2025`

##### NSL — ตัวเพิ่ม RFO · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เอ็นเอสแอล ฟู้ดส์ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและจำหน่ายสินค้าเบเกอรี่ อาหารรองท้อง และขนมขบเคี้ยว รวมทั้งนำเข้าและจำหน่ายเนื้อสัตว์และผักแช่แข็ง

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 6.9bn | 22.90 | -0.9% | 11.5x | 8.7% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 7 · NPAT 10 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 5.8bn → FY2025 THB 6.9bn · +1.1bn · +18.5%

- RFO ปี 2568 อยู่ที่ 6,922 ลบ. เพิ่ม 18.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ และ การออกผลิตภัณฑ์ใหม่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue In 2025, NSL group’s revenue from sales, Revenue from franchise license and other income were accounted for 99.4%, 0.2% and 0.4% of total revenue, respectively. Revenue from sales consisted of products from the bakery and appetizers, products under NSL’s brands and trading, food services, export and other agricultural products and others. In 2025, the Group had revenue from sales of Baht 6,910.5 million, increased from 2024 by Baht 1,083.6 million, equivalent to 18.6%, mainly due to the group’s sale volume increased because of NSL group launching more new products in all product categories.

  `MDA_NSL_FY2025` · `p013` · SHA af560c0f80b3
  </details>
- RFO ปี 2568 อยู่ที่ 6,922 ลบ. เพิ่ม 18.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ยอดขายส่งออกและตลาดต่างประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from sales 6,910.5 100.0% 5,826.9 100.0% 1,083.6 18.6% Cost of sales 5,565.4 80.5% 4,629.9 79.5% 935.5 20.2% Gross Profit 1,345.1 19.5% 1,197.0 20.5% 148.1 12.4% In 2025, gross profit margin was slightly decreased from the previous year mainly due to adjustment of minimum wage, raw material usage and increasing of export sales for agricultural product which gross profit margin less than bakery product. However, the Group continuously has cost and expenses control in order to be economy of scale.

  `MDA_NSL_FY2025` · `p015` · SHA 457136328c27
  </details>
- RFO ปี 2568 อยู่ที่ 6,922 ลบ. เพิ่ม 18.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The distribution costs in 2025 increased from the previous year by Baht 41.8 million. It was mainly due to the increase in transportation expenses from increasing of sale volume in 2025, increase in rental and service fee in other distribution costs and increase in salaries, wages, overtime, bonuses, and employee benefits from increasing in personnel in sales and marketing departments.

  `MDA_NSL_FY2025` · `p018` · SHA 3cb2f2badd66
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 541m → FY2025 THB 604m · +63m · +11.7%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 604 ลบ. เพิ่ม 11.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ยอดขายส่งออกและตลาดต่างประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from sales 6,910.5 100.0% 5,826.9 100.0% 1,083.6 18.6% Cost of sales 5,565.4 80.5% 4,629.9 79.5% 935.5 20.2% Gross Profit 1,345.1 19.5% 1,197.0 20.5% 148.1 12.4% In 2025, gross profit margin was slightly decreased from the previous year mainly due to adjustment of minimum wage, raw material usage and increasing of export sales for agricultural product which gross profit margin less than bakery product. However, the Group continuously has cost and expenses control in order to be economy of scale.

  `MDA_NSL_FY2025` · `p015` · SHA 457136328c27
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 604 ลบ. เพิ่ม 11.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ การซื้อกิจการและการรวมงบการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, NSL had net profit in the separate financial statement of Baht 603.1 million, which increased from the previous year by 63.3 million from increasing in revenue in all product categories. However, net profit margins in 2025 decreased when compared with the previous year by 0.2%, because of raw material usage and increasing in salaries, wages, overtime, and employee benefits. In addition, for consolidated financial statement, in 2025, NSL had recognized share of profit and loss from invested in Pro Natural Foods Co., Ltd, NSL Bake A Wish Co., Ltd., NSL Intertrade (2023) Co., Ltd. and NSL Inno Foods Co, Ltd. which loss was occurred from selling and operating expense, as such, net profi

  `MDA_NSL_FY2025` · `p023` · SHA 75a130102cc6
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 604 ลบ. เพิ่ม 11.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The distribution costs in 2025 increased from the previous year by Baht 41.8 million. It was mainly due to the increase in transportation expenses from increasing of sale volume in 2025, increase in rental and service fee in other distribution costs and increase in salaries, wages, overtime, bonuses, and employee benefits from increasing in personnel in sales and marketing departments.

  `MDA_NSL_FY2025` · `p018` · SHA 3cb2f2badd66
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 604 ลบ. เพิ่ม 11.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Shareholders’ equity as at December 31, 2025, was Baht 2,207.3 million, increased by Baht 286.8 million from previous year or equivalent to 14.9%. It resulted from the increase of retained earnings from net profit for the period by Baht 602.6 million, dividend payment in 2025 by Baht 315.0 million and increase in change in ownership interest in a subsidiary Baht 0.9 million.

  `MDA_NSL_FY2025` · `p030` · SHA b8cf2f3534bf
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_NSL_FY2025`

##### SNNP — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท ศรีนานาพร มาร์เก็ตติ้ง จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและจำหน่ายเครื่องดื่มและขนมขบเคี้ยว เช่น เยลลี่พร้อมดื่มและเยลลี่คาราจีแนน ภายใต้ตราสินค้าเจเล่ ปลาหมึกอบ ปลาหมึกเส้น และปลาเส้น ภายใต้ตราสินค้าเบนโตะ และขนมขึ้นรูปและขนมปังแท่งภายใต้ตราสินค้าดอกบัว โลตัส เป็นต้น

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 6.4bn | 7.10 | -3.4% | 15.7x | 9.2% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 12 · NPAT 12 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 5.9bn → FY2025 THB 5.6bn · −324m · -5.4%

- RFO ปี 2568 อยู่ที่ 5,624 ลบ. ลด 5.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ และ อุปสงค์และกำลังซื้อในประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > QoQ (%) YoY (%) YoY (%) Revenue from domestic sales 1,259.1 1,134.5 1,094.2 -3.5% -13.1% 4,654.1 4,552.2 -2.2% Revenue from overseas sales 353.6 242.2 279.6 15.4% -20.9% 1,293.5 1,071.8 -17.1% Total revenue from sales 1,612.7 1,376.7 1,373.8 -0.2% -14.8% 5,947.6 5,624.0 -5.4% Revenue from sales in Q4/2025 was THB 1,373.8 million, a decrease of THB 2.8 million or 0.2% compared to Q3/2025, which was THB 1,376.7 million, and a decrease of THB 238.9 million or 14.8% compared to Q4/2024, which was THB 1,612.7 million. The decline was mainly due to the slowdown in domestic revenue from sales. Domestic sales revenue in Q4/2025 was THB 1,094.2 million, compared to THB 1,134.5 million in Q3/2025, a d

  `MDA_SNNP_FY2025` · `p032` · SHA 428e553030ff
  </details>
- RFO ปี 2568 อยู่ที่ 5,624 ลบ. ลด 5.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ และ อุปสงค์และกำลังซื้อในประเทศ และ สภาพอากาศและฤดูกาล
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue In 2025, the Company’s revenue from sales was THB 5,624.0 million, a decrease of THB 323.6 million or 5.4% compared to THB 5,947.6 million in 2024. Domestic sales revenue was THB 4,552.2 million, a decrease of THB 101.9 million or 2.2% compared to THB 4,654.1 million in the previous year, mainly due to the slowdown in the domestic economy, the shorter-than-usual summer season, and severe flooding in the southern region during Q4/2025. However, domestic sales gradually improved in line with the Company’s customer base expansion strategy. Overseas sales revenue in 2025 was THB 1,071.8 million, a decrease of THB 221.7 million or 17.1% compared to THB 1,293.5 million in 2024, mainly driv

  `MDA_SNNP_FY2025` · `p029` · SHA 5dc636d1b2f9
  </details>
- RFO ปี 2568 อยู่ที่ 5,624 ลบ. ลด 5.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > measures(3), consumer purchasing power continued to recover gradually, which affected the Company’s domestic revenue from sales in 2025. Nevertheless, in Q4/2025, the Company recorded a positive recovery in overseas sales of THB 279.6 million, an increase of THB 37.4 million or 15.4% compared to Q3/2025. The improvement was mainly driven by the normalization of sales in Vietnam following the completion and easing of tax system restructuring and provincial mergers, together with improved management systems. These factors are expected to support improved performance in the following year. However, overseas sales for the full year still declined compared to 2024 due to the Thai Cambodian border

  `MDA_SNNP_FY2025` · `p005` · SHA c53dbc27e7ed
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 651m → FY2025 THB 518m · −133m · -20.4%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 518 ลบ. ลด 20.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ อุปสงค์และกำลังซื้อในประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross Profit Gross profit in 2025 was THB 1,661.5 million, a decrease of THB 99.0 million or 5.6%, in line with the slowdown in revenue from sales. However, the gross profit margin was 29.5%, a slight decrease of 0.1% from 29.6% in the previous year, reflecting the Company’s ability to maintain its margin despite lower total revenue, supported by effective raw material and packaging cost management. Gross profit in Q4/2025 was THB 390.8 million, compared to THB 412.7 million in Q3/2025, a decrease of THB 21.9 million or 5.3%. Compared to Q4/2024, which was THB 482.8 million, gross profit decreased by THB 92.0 million or 19.1%. Gross profit margin in Q4/2025 was 28.4%, a decrease of 1.6% from

  `MDA_SNNP_FY2025` · `p036` · SHA c1e2392de929
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 518 ลบ. ลด 20.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net profit attribute to owners of the parent 10.7% 9.7% 6.8% 11.4% 9.5% from core business margin Net profit attributable to owners of the parent in 2025 was THB 518.3 million, a decrease of THB 132.9 million or 20.4% compared to the previous year. Net profit from core operations in 2025 was THB 537.0 million, a decrease of THB 141.5 million or 20.8% compared to the previous year. Earnings per share in 2025 were THB 0.57. In Q4/2025, net profit attributable to owners of the parent was THB 88.6 million, compared to THB 129.6 million in Q3/2025, a decrease of THB 41.0 million or 31.6%. Compared to Q4/2024, which was THB 168.0 million, net profit decreased by THB 79.4 million or 47.3%, mainly d

  `MDA_SNNP_FY2025` · `p043` · SHA cb55ed76f609
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 518 ลบ. ลด 20.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ อุปสงค์และกำลังซื้อในประเทศ และ การแข่งขันและการส่งเสริมการขาย และ ค่าใช้จ่ายภาษี
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Management Discussion and Analysis for the year ended 31 December 2025 The Company continued to maintain its gross profit margin at a stable level. In 2026, the gross profit margin stood at 29.5%, remaining close to the previous year, despite a decline in total sales revenue. This was attributable to the effective management of raw material and packaging costs. As gross profit declined in line with the slowdown in sales revenue, together with higher selling and administrative expenses from marketing and promotional activities under the business plan, as well as the recognition of corporate income tax following the expiration of tax exemption privileges in Vietnam, with 2025 being the first y

  `MDA_SNNP_FY2025` · `p006` · SHA d57fea7e547d
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 518 ลบ. ลด 20.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Cost of sales Cost of sales in 2025 was THB 3,962.5 million, a decrease of THB 224.6 million or 5.4% compared to the previous year, in line with the decline in sales at a similar proportion. Cost of sales in Q4/2025 was THB 983.0 million, compared to THB 964.0 million in Q3/2025, an increase of THB 19.0 million or 2.0%. Compared to Q4/2024, which was THB 1,129.9 million, cost of sales decreased by THB 146.9 million or 13.0%.

  `MDA_SNNP_FY2025` · `p034` · SHA d958a7f332a1
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_SNNP_FY2025`

##### PM — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท พรีเมียร์ มาร์เก็ตติ้ง จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — จัดจำหน่ายและเป็นตัวแทนจำหน่ายสินค้าอุปโภคและบริโภค แบ่งเป็น 4 กลุ่ม ได้แก่ กลุุ่มผลิตภัณฑ์ขนมขบเคี้ยวและผลิตภัณฑ์ลูกอม กลุ่มผลิตภัณฑ์อาหารและเครื่องดื่ม กลุ่มผลิตภัณฑ์ของใช้ส่วนตัวและผลิตภัณฑ์ทำความสะอาดในครัวเรือน และกลุ่มผลิตภัณฑ์อาหารสัตว์เลี้ยง โดยมีร้านค้ากว่า 100,000 แห่ง ทั่วประเทศติดต่อค้าขายโดยตรงกับบริษัท

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 6.4bn | 11.40 | -4.2% | 11.5x | 10.5% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 2 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 4.9bn → FY2025 THB 5.9bn · +996m · +20.3%

- RFO ปี 2568 อยู่ที่ 5,914 ลบ. เพิ่ม 20.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Key changing items are as follows: 1. Net revenue from sales and services in the period was THB 5,914.5 million, an increase of THB 996.4 million or 20.3 percent from the same period of the previous year, consisting of; • Domestic sales were THB 3,036.5 million, an increase of THB 154.4 million from the same period of the previous year due to consumer product distribution business increasing by THB 143.7 million and food production business increasing by THB 10.7 million, mainly from coffee business, • International sales were THB 2,878.0 million, an increase of THB 842.0 million from the same period of the previous year. Such increase resulted from cat food production business of THB 854.8

  `MDA_PM_FY2025` · `p001` · SHA efa5fc8a2e01
  </details>
- RFO ปี 2568 อยู่ที่ 5,914 ลบ. เพิ่ม 20.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ มาตรการภาษีนำเข้าและข้อกีดกันทางการค้า และ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > also caused by price adjustments impacted by the increase in import tariffs for customers in the United States of America. 2. Distribution cost in the period amounted to THB 472.1 million, an increase of THB 45.2 million from the same period of the previous year due to advertising and promotional costs in the "Taro Rak Loak Chok Deng" project. The ratio of distribution cost to revenue of sales and services was 8.0 percent, a decrease of 0.7 percent from the same period of the previous year. 3. Other income in the period amounted to THB 63.6 million, an increase of THB 32.1 million or 102.1 percent from the same period of the previous year due to an increase in a gain from exchange rate of TH

  `MDA_PM_FY2025` · `p002` · SHA 1dde96edd622
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 600m → FY2025 THB 622m · +21m · +3.6%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 622 ลบ. เพิ่ม 3.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ มาตรการภาษีนำเข้าและข้อกีดกันทางการค้า และ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > also caused by price adjustments impacted by the increase in import tariffs for customers in the United States of America. 2. Distribution cost in the period amounted to THB 472.1 million, an increase of THB 45.2 million from the same period of the previous year due to advertising and promotional costs in the "Taro Rak Loak Chok Deng" project. The ratio of distribution cost to revenue of sales and services was 8.0 percent, a decrease of 0.7 percent from the same period of the previous year. 3. Other income in the period amounted to THB 63.6 million, an increase of THB 32.1 million or 102.1 percent from the same period of the previous year due to an increase in a gain from exchange rate of TH

  `MDA_PM_FY2025` · `p002` · SHA 1dde96edd622
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_PM_FY2025`

##### TKN — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เถ้าแก่น้อย ฟู๊ดแอนด์มาร์เก็ตติ้ง จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัทประกอบธุรกิจผลิตและจำหน่ายขนมขบเคี้ยวประเภทสาหร่ายทั้งในและต่างประเทศภายใต้ตราสินค้า "เถ้าแก่น้อย" รวมถึงขนมขบเคี้ยวและผลิตภัณฑ์อาหารเพื่อสุขภาพ

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 5.9bn | 4.28 | +7.0% | 14.2x | 7.7% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 19 · NPAT 9 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 5.7bn → FY2025 THB 5.3bn · −404m · -7.1%

- RFO ปี 2568 อยู่ที่ 5,308 ลบ. ลด 7.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from Sales The Company has revenue from sales in the fourth quarter in the amount of 1,376.3 million Baht, decreased by 6.3 percent from the same quarter of the previous year (increased by 6.5 percent from Q3/2025), which are accounted for by domestic sales in the amount of 615.6 million Baht, increased by 2.8 percent, and international sales in the amount of 759.8 million Baht, decreased by 12.7 percent from the same quarter of the previous year. Domestic sales continued to grow in every quarter of this year, and caused sales in the fourth quarter to achieve the new highest quarterly sales over the past several years, thanks to both the growth of seaweed products and the addition of

  `MDA_TKN_FY2025` · `p007` · SHA 46a90c56bfa2
  </details>
- RFO ปี 2568 อยู่ที่ 5,308 ลบ. ลด 7.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Administrative Expenses The Company has the administrative expenses in the fourth quarter in the amount of 104.1 million Baht, representing 7.6 percent of revenue from sales. The ratio of administrative expenses to sales revenue is increased by 1.4 percent from the same period of the previous year (decreased by 0.6 percent from Q3/2025). In 2025, the Company has the total administrative expenses in the amount of 412.8 million Baht, representing 7.8 percent of revenue from sales, increased by 0.8 percent of revenue from sales as compared to the same period of the previous year. However, the Company carefully controlled the administrative expenses regularly throughout the year, and as such, th

  `MDA_TKN_FY2025` · `p023` · SHA 8a9adbe6fc98
  </details>
- RFO ปี 2568 อยู่ที่ 5,308 ลบ. ลด 7.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > of the previous year, whereby China accounted for 1,120.5 million Baht, decreased by 5.1 percent from the same period of the previous years, and other international markets for 1,847.4 million Baht, decreased by 23.0 percent from the same period of the previous year. Sales in China started to improve in every quarter of 2025 due to ongoing marketing promotion, both online and offline, introduction of the new Brand Ambassador, and expansion of the distribution channels. However, in 2025, other international markets encountered fluctuations and were affected by exchange rates due to the ongoing Baht strengthening which resulted in declining revenues, including price competition from products l

  `MDA_TKN_FY2025` · `p017` · SHA f5ba923a0b45
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 836m → FY2025 THB 409m · −427m · -51.0%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 409 ลบ. ลด 51.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การเปลี่ยนแปลงของอัตรากำไร และ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross Margin The Company has gross profit in the fourth quarter in the amount of 432.6 million Baht, representing 31.4 percent of revenue from sales. The ratio of gross profit to sales revenue is increased by 3.8 percent as compared to the same quarter of the previous year, and increased by 2.1 percent as compared to that of Q3/2025. Such increase in gross margin in the fourth quarter was due to the average cost of seaweed raw materials which started to decline from the third quarter for the fact that the cost of seaweed purchased in 2024 was higher than that of 2025, which was used up in the middle of the fourth quarter, thereby causing the average cost of seaweed in the fourth quarter to b

  `MDA_TKN_FY2025` · `p019` · SHA 4c0df646728a
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 409 ลบ. ลด 51.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > revenue from sales, decreased by 4.5 percent as compared to the same period of the previous year. This was due to impact of several factors, such as, the costs of goods, particularly the cost of seaweed which, on average, was higher than 2024, including this year’s declining sales by 7.1 percent, which increased the fixed unit costs, and the fluctuations of exchange rates in various countries and the Baht strengthening more than the previous year which also caused revenue to reduce. However, the Company has managed to minimize impact of the increasing cost of seaweed by negotiating for packaging costs which were reduced by 10-20% for a variety of major packages, effective in the fourth quart

  `MDA_TKN_FY2025` · `p020` · SHA e566ce914ab8
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 409 ลบ. ลด 51.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Distribution Costs The Company has the distribution costs in the fourth quarter in the amount of 200.3 million Baht, representing 14.6 percent of revenue from sales. The ratio of distribution costs to sales revenue is increased by 3.4 percent from the same quarter of the previous year (increased by 2.1 percent from Q3/2025). Such increase was due to the

  `MDA_TKN_FY2025` · `p021` · SHA a8768f4a9c5c
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 409 ลบ. ลด 51.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การเปลี่ยนแปลงของอัตรากำไร และ ค่าใช้จ่ายภาษี และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Financial Statements (Million Baht) (%) (Million Baht) (%) (%) Revenue from Sales 1,376.3 100.0 % 1,291.9 100.0 % 6.5 % Cost of Sales (943.6) (68.6 %) (912.3) (70.6 %) 3.4 % Gross Margin 432.6 31.4 % 379.6 29.4 % 14.0 % Distribution Costs (200.3) (14.6 %) (156.9) (12.1 %) 27.6 % Administrative Expenses (104.1) (7.6 %) (105.2) (8.1 %) (1.0 %) Profit before Income Tax Expenses 130.9 9.5 % 126.6 9.8 % 3.4 % Income Tax Expenses ( 18.7) (1.4 %) ( 14.4) (1.1 %) 29.9 % Net Profit : Owners of the Parent 112.4 8.2 % 112.2 8.7 % 0.2 %

  `MDA_TKN_FY2025` · `p006` · SHA 3e90e7f7cc23
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: การเปลี่ยนแปลงของอัตรากำไร และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Increasing margins in distribution via the respective channels by addition of various products with a good rate of gross margin, including optimizing the efficiency of marketing expenses. - Focusing on productivity in terms of both yield improvement and reduction of loss in the process, including adjustment of the Demand and Supply Planning to minimize stock write-off. For the purpose of achieving both primary goals, the Company has given priority to potential development of personnel on an ongoing basis, building of a GREAT culture, and upskilling of work units, as our driving force in parallel to improvement of work process, application of artificial intelligence (AI) to work process to en

  `MDA_TKN_FY2025` · `p028` · SHA faba4df3cdd3
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_TKN_FY2025`

##### KCG — บริษัทในกลุ่ม · ติดตาม

**บริษัท เคซีจี คอร์ปอเรชั่น จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและจัดจำหน่ายอาหารและขนมตะวันตก (Western foods) แบ่งเป็น 3 กลุ่มผลิตภัณฑ์หลัก ได้แก่ ผลิตภัณฑ์ที่ทำจากนม (Dairy Products) ผลิตภัณฑ์เกี่ยวกับการประกอบอาหารและเบเกอรี่ (Food and Bakery Ingredients) และผลิตภัณฑ์บิสกิต (Biscuits)

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 5.7bn | 10.50 | +27.3% | 10.7x | 5.8% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 20 · NPAT 20 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 2

**RFO — เพราะอะไร** — FY2024 THB 7.7bn → FY2025 THB 8.6bn · +902m · +11.6%

- RFO ปี 2568 อยู่ที่ 8,645 ลบ. เพิ่ม 11.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ อัตรากำไรลดลง และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Q4/2025 vs Q3/2025 (QoQ) In Q4/2025, the Company recorded net profit of THB 193.5 million, increased by THB 104.7 million or 118.1% QoQ, mainly due to the following reasons: Total revenue increased by 39.2% QoQ, mainly supported by sales growth of 39.5% QoQ, driven by growth across all product categories and sales channels, following the high sales season, as Q4 is typically the highest sales quarter of the year. Gross profit margin increased by 2.8% QoQ, supported by higher capacity utilization, improved production efficiency, and effective production cost management. The overall average cost of raw materials remained relatively stable QoQ. %SG&A to sales decreased by 0.2% QoQ, mainly suppo

  `MDA_KCG_FY2025` · `p062` · SHA edeaa80b0aab
  </details>
- RFO ปี 2568 อยู่ที่ 8,645 ลบ. เพิ่ม 11.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ อัตรากำไรลดลง และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > YoY, supported by the following reasons: Total revenue increased by 8.9% YoY, mainly supported by sales growth of 9.1% YoY resulting from growth across all sales channels including B2B (business-to-business), B2C (business-to-consumer), and export, driven by higher sales in dairy products and food and bakery ingredients (FBI). Gross profit margin increased by 1.2% YoY, supported by higher capacity utilization rate, improved production efficiency, and effective production cost management. The overall average cost of raw materials remained relatively stable YoY. Finance costs decreased by 30.0% YoY, supported by decreased loans and lower interest rates. Effective tax rate decreased by 0.1% YoY

  `MDA_KCG_FY2025` · `p061` · SHA 9390d285ee59
  </details>
- RFO ปี 2568 อยู่ที่ 8,645 ลบ. เพิ่ม 11.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ยอดขายส่งออกและตลาดต่างประเทศ และ กำลังการผลิตและเครื่องจักรใหม่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > record-high sales for the fourth consecutive year, with growth across all sales channels, including B2B (business-to-business), B2C (business-to-consumer), and export, driven by higher sales in dairy products and food and bakery ingredients (FBI). Gross profit margin was maintained at 30.9%, remaining at the same level as in 2024, supported by improved production efficiency and effective production cost management, despite an increase in the overall average cost of raw materials and lower capacity utilization rate mainly due to a decline in the production of biscuits. %SG&A to sales decreased by 0.5% YoY, supported by increased sales and effective expense management, including benefits from

  `MDA_KCG_FY2025` · `p063` · SHA e6ec840ca50e
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 406m → FY2025 THB 503m · +97m · +24.0%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 503 ลบ. เพิ่ม 24.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ อัตรากำไรลดลง และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > YoY, supported by the following reasons: Total revenue increased by 8.9% YoY, mainly supported by sales growth of 9.1% YoY resulting from growth across all sales channels including B2B (business-to-business), B2C (business-to-consumer), and export, driven by higher sales in dairy products and food and bakery ingredients (FBI). Gross profit margin increased by 1.2% YoY, supported by higher capacity utilization rate, improved production efficiency, and effective production cost management. The overall average cost of raw materials remained relatively stable YoY. Finance costs decreased by 30.0% YoY, supported by decreased loans and lower interest rates. Effective tax rate decreased by 0.1% YoY

  `MDA_KCG_FY2025` · `p061` · SHA 9390d285ee59
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 503 ลบ. เพิ่ม 24.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ อัตรากำไรลดลง และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Q4/2025 vs Q3/2025 (QoQ) In Q4/2025, the Company recorded net profit of THB 193.5 million, increased by THB 104.7 million or 118.1% QoQ, mainly due to the following reasons: Total revenue increased by 39.2% QoQ, mainly supported by sales growth of 39.5% QoQ, driven by growth across all product categories and sales channels, following the high sales season, as Q4 is typically the highest sales quarter of the year. Gross profit margin increased by 2.8% QoQ, supported by higher capacity utilization, improved production efficiency, and effective production cost management. The overall average cost of raw materials remained relatively stable QoQ. %SG&A to sales decreased by 0.2% QoQ, mainly suppo

  `MDA_KCG_FY2025` · `p062` · SHA edeaa80b0aab
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 503 ลบ. เพิ่ม 24.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ อัตรากำไรลดลง และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Q4/2025 vs Q4/2024 (YoY) In Q4/2025, the Company recorded net profit of THB 193.5 million, increased by 18.7% YoY, with the following key matters: Sales increased by 9.1% YoY across all sales channels, including B2B (business-to-business), B2C (business-to- consumer), and export, driven by higher sales in dairy products and food and bakery ingredients (FBI). Gross profit margin increased by 1.2% YoY, supported by higher capacity utilization rate, improved production efficiency, and effective production cost management. The overall average cost of raw materials remained relatively stable YoY. SG&A increased by 11.4% YoY, following the higher sales. Increased expenditure mainly came from (1) a

  `MDA_KCG_FY2025` · `p010` · SHA 56a6ff580f13
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 503 ลบ. เพิ่ม 24.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ กำลังการผลิตและเครื่องจักรใหม่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2025 vs 2024 (YoY) In 2025, the Company recorded a record-high net profit for the third consecutive year of THB 503.3 million, increased by 24.0% YoY, with the following key matters: Record-high sales for the fourth consecutive year of THB 8,645.5 million, increased by 11.6% YoY across all sales channels, driven by higher sales in dairy products and food and bakery ingredients (FBI). Gross profit margin was maintained at the same level as in 2024 at 30.9%, supported by improved production efficiency and effective production cost management, despite an increase in the overall average cost of raw materials and a lower capacity utilization rate mainly due to a decline in the production of biscu

  `MDA_KCG_FY2025` · `p013` · SHA 41f6af85a49f
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ กำลังการผลิตและเครื่องจักรใหม่ และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายภาษี
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > the end of 2024. Income tax expense increased by 19.1% YoY following the higher profit before income tax expense. The Company did not incur an impairment loss on machinery and equipment as occurred in the same period last year, totaling THB 21.1 million, resulting from machinery upgrades, production process improvements, and factory re-layouts aimed at increasing production capacity, enhancing production efficiency, and reducing production cost. The Board of Directors resolved to propose a dividend payment for the 2025 operating results of Baht 0.51 per share, representing a dividend payout ratio of 55.2%, an increase from Baht 0.41 per share with a payout ratio of 55.1% in the previous year

  `MDA_KCG_FY2025` · `p014` · SHA d4ef8e2b482d
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำลังการผลิตและเครื่องจักรใหม่ และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ต้นทุนทางการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Impairment loss on 0.0 0.0 0.0 - - 21.1 0.0 -100.0% machinery and equipment Finance costs 13.3 11.6 9.3 -30.0% -19.8% 53.1 43.4 -18.2%

  `MDA_KCG_FY2025` · `p006` · SHA 88b35c83451a
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_KCG_FY2025`

##### CHAO — บริษัทในกลุ่ม · ติดตาม

**บริษัท เจ้าสัว ฟู้ดส์ อินดัสทรี จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและจัดจำหน่ายขนมขบเคี้ยวและผลิตภัณฑ์แปรรูปจากเนื้อสัตว์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.2bn | 4.12 | -8.4% | 15.8x | 5.0% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 20 · NPAT 18 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 3

**RFO — เพราะอะไร** — FY2024 THB 1.6bn → FY2025 THB 1.4bn · −152m · -9.7%

- RFO ปี 2568 อยู่ที่ 1,416 ลบ. ลด 9.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > QoQ: Q4/2025 vs Q3/2025 +20.4% In Q4/2025, the Company reported operating revenue of THB 410.8 million, increased by THB 69.5 million or 20.4% from Q3/2025, mainly due to the following factors: • Domestic sales contributed for 76.9% of total operating revenue in Q4/2025, increased by 20.4% from Q3/2025,mainly due to the increase in operating revenue across all distribution channels, driven by 1) the growth in Modern Trade from successful promotional campaigns, improved in-store merchandising efficiency, and the launch of New Year Gift Sets, which helped stimulate sales and enhance brand visibility in this channel 2) the success of the Company’s strategy to adjust its wholesale distribution m

  `MDA_CHAO_FY2025` · `p024` · SHA 5c1cdf9eda9f
  </details>
- RFO ปี 2568 อยู่ที่ 1,416 ลบ. ลด 9.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ราคาวัตถุดิบและปริมาณอาหารทะเล และ การแข่งขันและการส่งเสริมการขาย และ การออกผลิตภัณฑ์ใหม่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company’s Overview Performance Q4/2025 • In Q4/2025, the Company reported total Operating Revenue of THB 410.8 million, increased by THB 69.5 million or 20.4% from Q3/2025, mainly due to 1) the increase in operating revenue across all domestic distribution channels and 2) the significant increase in sales in China, driven by promotional activities together with the successful launch of the new product “Shrimp Floss Rice Crackers with Pad Thai Sauce,” which received positive feedback from consumers in China. • Gross Profit was THB 159.9 million, increased by THB 38.8 million or 32.0% from Q3/2025, mainly due to 1) the ongoing execution of proactive cost- management initiatives, focusing o

  `MDA_CHAO_FY2025` · `p006` · SHA e01154c51434
  </details>
- RFO ปี 2568 อยู่ที่ 1,416 ลบ. ลด 9.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ยอดขายส่งออกและตลาดต่างประเทศ และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > YoY: 2025 vs 2024 -0.4% In 2025, the Company reported selling and administrative expenses of THB 432.9 million, decreased by THB 1.9 million or 0.4% from2024, mainly due to the efficient management of marketing expenses, with marketing activities adjusted to align with current consumer behavior. However, the decrease in domestic and international sales, resulting in selling and administrative expenses to total revenue in 2025 was 30.2%, increased by 2.8% from 2024. • Selling and distribution expenses In 2025, the Company reported selling and distribution expenses of THB 233.8 million, increased by THB 5.9 million or 2.6% from 2024, mainly due to the expansion of the domestic sales team, part

  `MDA_CHAO_FY2025` · `p038` · SHA 87160807e712
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 133m → FY2025 THB 70m · −63m · -47.3%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 70.3 ลบ. ลด 47.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ราคาวัตถุดิบและปริมาณอาหารทะเล และ การแข่งขันและการส่งเสริมการขาย และ การออกผลิตภัณฑ์ใหม่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company’s Overview Performance Q4/2025 • In Q4/2025, the Company reported total Operating Revenue of THB 410.8 million, increased by THB 69.5 million or 20.4% from Q3/2025, mainly due to 1) the increase in operating revenue across all domestic distribution channels and 2) the significant increase in sales in China, driven by promotional activities together with the successful launch of the new product “Shrimp Floss Rice Crackers with Pad Thai Sauce,” which received positive feedback from consumers in China. • Gross Profit was THB 159.9 million, increased by THB 38.8 million or 32.0% from Q3/2025, mainly due to 1) the ongoing execution of proactive cost- management initiatives, focusing o

  `MDA_CHAO_FY2025` · `p006` · SHA e01154c51434
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 70.3 ลบ. ลด 47.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ ยอดขายส่งออกและตลาดต่างประเทศ และ อุปสงค์และกำลังซื้อในประเทศ และ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > YoY: 2025 vs 2024 -11.6% Gross Profit:In 2568, the Company reported gross profit of THB 505.1 million, decreased by THB 66.3 million or 11.6% from 2024, mainly due to the following factors: 1) The decreased domestic sales, impacted by the slowdown in the domestic economy and weaker consumer purchasing power, as well as a decrease in international sales, particularly in markets with higher gross profit margins 2) The decrease in international sales, particularly in the decreased sales in China, as a result of a major promotional campaign held at Sam’s Club during 2024 3) The impact of exchange rate fluctuations from the appreciation of the Thai Baht. However, the Company closely monitors fore

  `MDA_CHAO_FY2025` · `p033` · SHA 2180e261a302
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 70.3 ลบ. ลด 47.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ การเปลี่ยนแปลงของอัตรากำไร และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ราคาขายและส่วนผสมผลิตภัณฑ์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > YoY: Q4/2025 vs Q4/2024 +8.1% Gross Profit:In Q4/2025, the Company reported gross profit of THB 159.9 million, increased by THB 12.0 million or 8.1% from Q4/2024, mainly due to the following factors: 1) The Company’s ability to effectively manage and control costs despite a continuous upward trend in overall production and operating costs, focusing on productivity improvement within the manufacturing facilities and ensuring waste reduction to enhance operational efficiency, maintain appropriate cost control, and to strengthen long-term profitability. 2) More effective product portfolio management through shifting the product mix toward higher gross margin segments, such as Better-for-You Sna

  `MDA_CHAO_FY2025` · `p032` · SHA f7e90775a289
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 70.3 ลบ. ลด 47.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Unit: Million THB %YoY %QoQ % YoY Operating Revenue 433.9 341.3 410.8 (5.3%) 20.4% 1,567.1 1,415.6 (9.7%) Gross Profit 147.8 121.1 159.9 8.1% 32.0% 571.4 505.1 (11.6%) EBITDA 35.4 24.4 68.3 93.1% 180.0% 201.9 136.8 (32.3%) Net (Loss) Profit 20.0 9.5 46.2 131.4% 388.2% 133.4 68.9 (48.3%) Gross Profit Margin (%) 34.1% 35.5% 38.9% 4.8% 3.4% 36.5% 35.7% (0.8%) EBITDA Margin(%) 8.1% 7.1% 16.5% 8.5% 9.4% 12.7% 9.5% (3.2%) Net (Loss) Profit Margin (%) 4.5% 2.7% 11.2% 6.6% 8.4% 8.4% 4.8% (3.6%)

  `MDA_CHAO_FY2025` · `p004` · SHA e687946eb791
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: อัตรากำไรดีขึ้น และ อัตรากำไรลดลง และ ยอดขายส่งออกและตลาดต่างประเทศ และ เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 1) The decreased domestic sales, impacted by the slowdown in the domestic economy and weaker consumer purchasing power, as well as a decrease in international sales, particularly in markets with higher gross profit margins. 2) The expansion of the domestic sales team, particularly in the Traditional Trade channel, which enhanced the Company’s ability to reach a broader consumer base. 3) The impact of exchange rate fluctuations from the appreciation of the Thai Baht. However, the Company closely monitors foreign exchange movements and implements risk management measures to sustain profitability on a continuous long-term basis. As a result, net profit margin in 2025 was 4.8%, decreased by 3.6%

  `MDA_CHAO_FY2025` · `p043` · SHA 3181574a4695
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: อัตรากำไรดีขึ้น และ การเปลี่ยนแปลงของอัตรากำไร และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ราคาขายและส่วนผสมผลิตภัณฑ์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > QoQ: Q4/2025 vs Q3/2025 +32.0% Gross Profit:In Q4/2025, the Company reported gross profit of THB 159.9 million, increased by THB 38.8 million or 32.0% from Q3/2025, mainly due to the following factors: 1) The ongoing execution of proactive cost-management initiatives, focusing on productivity improvement within the manufacturing facilities and ensuring waste reduction to enhance operational efficiency, maintain appropriate cost control, and to strengthen long-term profitability. 2) More effective product portfolio management through shifting the product mix toward higher gross margin segments, such as Better-for-You Snacks. 3) The Company closely monitors foreign exchange movements and imple

  `MDA_CHAO_FY2025` · `p031` · SHA 2452b27c56f9
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_CHAO_FY2025`

#### ทะเบียนข้อสรุป — F6

| ส่วน | ประเภท | ข้อสรุป | รหัสแหล่งข้อมูล |
|---|---|---|---|
| headline | ข้ออนุมานนักวิเคราะห์ | ขนาดและความ defensive ช่วยพยุง valuation แต่กำไรอ่อนลง | FY_PANEL, F6_E1, F6_E2 |
| earnings_fact | ข้อเท็จจริงจากการคำนวณ | FY2025 RFO +0.0%; สถานะ NPAT ส่วนผู้ถือหุ้น: profit_decreased | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | RFO ทรงตัวแต่ NPAT ลด สะท้อน margin compression | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | TFMAMA มีสัดส่วนประมาณครึ่งกลุ่มและเป็นตัวฉุดกำไรหลัก | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | NSL เป็นตัวเพิ่มรายได้ที่ชัดที่สุด | FY_PANEL |
| causal_chain | ข้ออนุมานนักวิเคราะห์ | ห่วงโซ่เหตุ: อุปสงค์ในประเทศ → ส่งออก → ต้นทุนวัตถุดิบ → Margin → NPAT | F6_E1, F6_E2 |
| roles | ข้ออนุมานนักวิเคราะห์ | บทบาท: ผู้นำและตัวฉุดกำไร — TFMAMA; ตัวเพิ่ม RFO — NSL | FY_PANEL, F6_E1, F6_E2 |
| valuation | ข้ออนุมานนักวิเคราะห์ | P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 15.5x ครอบคลุม 9/9 บริษัท และ 100.0% ของ market cap ที่มีข้อมูล. แบรนด์ defensive พยุงมูลค่า แต่ RFO ที่ทรงตัวจำกัด upside | SET_PUBLIC_EOD, F6_E1, F6_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | คำสั่งซื้อส่งออกฟื้น | F6_E1, F6_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | ต้นทุนวัตถุดิบผ่อนคลาย | F6_E1, F6_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | สินค้าใหม่ช่วยเพิ่มรายได้ | F6_E1, F6_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | ตลาดในประเทศโตต่ำ | F6_E1, F6_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | วัตถุดิบแพงขึ้น | F6_E1, F6_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | ส่งออกอ่อนตัว | F6_E1, F6_E2 |
| must_prove | ประเด็นที่ต้องพิสูจน์ | 6M26 ต้องกลับมาโตด้านกำไรโดยยังรักษากระแสเงินสดแบบ defensive | F6_E1, F6_E2 |

#### ทะเบียนหลักฐาน — F6

- **`FY_PANEL`** · _ข้อเท็จจริงจากการคำนวณ_ — Audited FY2024-25 company panel
  - RFO / NPAT-to-owners / independent panel membership; QA 43 pass / 0 fail
  - บทบาท: historical fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_company_fy2024_2025_audited_2026-08-07.csv`
  - SHA-256: `e5e04dbc40ffcc79fed58545a93dc4549c29cdaecf260bea73711bc6d0720481`
- **`SET_PUBLIC_EOD`** · _ข้อเท็จจริงจากการคำนวณ_ — SET public Company Highlights — EOD 2026-08-07
  - Adjusted YTD; unadjusted price, market cap and valuation; factsheet-surface cross-check
  - บทบาท: current market fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_set_public_surface_reconciliation_2026-08-07.csv`
  - SHA-256: `544c1f29fe2d409ee398822ac2bf32b769081718962ae2d1138985b0146b9530`
- **`SET_COMPANY_PROFILE`** · _ข้อเท็จจริง_ — SET company profiles — English and Thai
  - Official company names and business descriptions refreshed and validated for the 118-company perimeter from the public SET profile API
  - บทบาท: company business profile
  - URL: <https://www.set.or.th/th/market/product/stock/overview>
- **`COMPANY_REPORTS`** · _ข้ออนุมานนักวิเคราะห์_ — Company report synthesis corpus
  - Annual-only draft synthesis; reconciled to the ticker FY2025 MD&A where available
  - บทบาท: secondary synthesis; not management attribution
  - พาธ: `data/company-reports.json`
  - SHA-256: `c1a2bc40cbe21a2058aa596c362e4d47ad117360831b847de78ec414831fd2d2`
- **`MDA_TFMAMA_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — TFMAMA FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/TFMAMA/MDA_TFMAMA_2025FY_T.md`
  - SHA-256: `ad43c94caa000229877d9a19e25877a6bdb178e4b89273e63a2aa80e54138c11`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/1390NWS250220261739070230T.pdf>
- **`MDA_PB_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — PB FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/PB/MDA_PB_2025FY_E.md`
  - SHA-256: `4b92dfbe80923ef9aacfe6335f6a93bd0e6595fa1c4a0067346cc21d446eead3`
  - URL: <https://weblink.set.or.th/dat/news/202602/0687NWS230220262116212930E.pdf>
- **`MDA_PRG_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — PRG FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/PRG/MDA_PRG_2025FY_T.md`
  - SHA-256: `d7573a48b4f6464f8bdf4ff5251f11ab60cf110225889b1eb24cbcca3414f40d`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/0366NWS240220261936132680T.pdf>
- **`MDA_NSL_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — NSL FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/NSL/MDA_NSL_2025FY_E.md`
  - SHA-256: `bb1e2e54be906cba92ad90a7469529df8aef23e3359510adc6788c375f50fe61`
  - URL: <https://weblink.set.or.th/dat/news/202603/1621NWS020320260706505900E.pdf>
- **`MDA_SNNP_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — SNNP FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SNNP/MDA_SNNP_2025FY_E.md`
  - SHA-256: `8ee275b3e72fd36550465342cdd3d5e329ce370182a6ea92c028c20801cf108d`
  - URL: <https://weblink.set.or.th/dat/news/202602/1568NWS270220261711378860E.pdf>
- **`MDA_PM_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — PM FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/PM/MDA_PM_2025FY_E.md`
  - SHA-256: `a1014b0ea3d0dff6121497431ce31f7974b1abd599a31bacc63199f85a24755c`
  - URL: <https://weblink.set.or.th/dat/news/202602/0977NWS200220261232000210E.pdf>
- **`MDA_TKN_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — TKN FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/TKN/MDA_TKN_2025FY_E.md`
  - SHA-256: `47883c0e07ebf6879988ed71bec687f6583322991386381b2d8068afde65ee0f`
  - URL: <https://weblink.set.or.th/dat/news/202602/1279NWS240220260735512280E.pdf>
- **`MDA_KCG_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — KCG FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/KCG/MDA_KCG_2025FY_E.md`
  - SHA-256: `86f7e5f85d0a2f7138f524a1af454d1889f42924bac15e8fcf1b08ce7cf7c198`
  - URL: <https://weblink.set.or.th/dat/news/202602/1763NWS250220261756223880E.pdf>
- **`MDA_CHAO_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — CHAO FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/CHAO/MDA_CHAO_2025FY_E.md`
  - SHA-256: `20a357dd4130102d6c8d2bb159eab48bd55ec36b277cf6b3418ab42338b84829`
  - URL: <https://weblink.set.or.th/dat/news/202602/1874NWS260220261704349210E.pdf>
- **`F6_E1`** · _ฝ่ายจัดการ_ — TFMAMA FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/TFMAMA/MDA_TFMAMA_2025FY_E.md`
  - SHA-256: `c362f072977506b4807df547a00f0993fa9934d0c1c79c3b79b6dae618ca655d`
- **`F6_E2`** · _ฝ่ายจัดการ_ — NSL FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/NSL/MDA_NSL_2025FY_E.md`
  - SHA-256: `bb1e2e54be906cba92ad90a7469529df8aef23e3359510adc6788c375f50fe61`
- **`F6_FACTSHEET`** · _ข้อเท็จจริงจากการคำนวณ_ — SET Factsheet — TFMAMA
  - Live leader cross-check
  - บทบาท: presentation-surface check
  - URL: <https://www.set.or.th/th/market/product/stock/quote/tfmama/factsheet>

### F2 · อาหารทะเลและเพาะเลี้ยง — ราคาปรับดีขึ้นแม้ผลประกอบการ FY2025 ยังถูกกดดัน

`ยังถูกกดดัน` · 8.2% M-cap · THB 66.9bn · 5 บริษัท

| ตัวชี้วัด | RFO | NPAT | ราคา | P/E |
|---|---|---|---|---|
| ช่วง | FY2025 YoY | ส่วนผู้ถือหุ้น FY2025 YoY | ราคา YTD ปรับแล้ว | เฉพาะบริษัทที่มีกำไร |
| ค่า | -3.3% | -14.3% | +6.0% | 10.9x |
| จำนวน | THB 160bn FY2025 | THB 5.1bn FY2025 | ณ 7 ส.ค. 2569 | ค่าเฉลี่ยรวม |
| ครอบคลุม | 5/5 | 5/5 | 5/5 • 100% M-cap | 4/5 • 99% M-cap |

**ข้อเท็จจริงที่สังเกตได้** — FY2025: RFO -3.3% • NPAT -14.3% • ราคา YTD +6.0% • P/E 10.9x • ครอบคลุม RFO 5/5 • NPAT 5/5

#### เหตุผลที่เปลี่ยน

1. _ข้อเท็จจริงจากการคำนวณ_ · ปริมาณส่งออก — TU เป็นตัวหลักของการลดลงทั้งรายได้และกำไรรวม
2. _ข้ออนุมานนักวิเคราะห์_ · Mix / ค่าเงิน — product mix ส่งออก ต้นทุนทูน่า และค่าเงินยังเป็นตัวแปรหลัก
3. _ข้ออนุมานนักวิเคราะห์_ · Gross margin **3.2%** — ราคาบวกในวงกว้างสะท้อนความคาดหวังการฟื้น มากกว่าผลประกอบการ FY2025 ที่เกิดขึ้นแล้ว

#### ห่วงโซ่เหตุและผล

**ปริมาณส่งออก** → **Mix / ค่าเงิน** → **Gross margin** (3.2% -0.4 ppt YoY) → **NPAT** (-14.3% THB 5.1bn FY2025) → **Re-rating** (10.9x YTD +6.0%)

#### บทบาทในกลุ่ม

| บทบาท | Ticker | ค่า | ที่มาของค่า |
|---|---|---|---|
| ผู้นำและกำหนดทิศ | TU | 85% | สัดส่วน Market Cap ในกลุ่ม |
| ตัวเทียบ | CFRESH | 16.6x | P/E · YTD +97.2% |

#### มูลค่า

**แรงกดดันปัจจุบัน / ข้อเท็จจริง** — P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 10.9x ครอบคลุม 4/5 บริษัท และ 99.2% ของ market cap ที่มีข้อมูล. ส่วนลดสะท้อนความไม่แน่นอนด้านส่งออก วัตถุดิบ และ margin

| Trigger | Risk |
|---|---|
| ต้นทุนทูน่าและค่าระวางผ่อนคลาย | วัตถุดิบผันผวน |
| ปริมาณส่งออกและสัดส่วนแบรนด์ดีขึ้น | อุปสงค์ต่างประเทศอ่อนตัว |
| ค่าเงินเอื้อต่อผู้ส่งออก | เงินบาทแข็งค่า |

**6M26 ต้องพิสูจน์** — 6M26 ต้องต่อยอดยอดขายที่เริ่มทรงตัวใน 4Q25 ไปสู่การฟื้นของ gross margin และกำไรส่วนผู้ถือหุ้น โดยยอดขาย FY2025 ยังลดลง

#### วิเคราะห์รายบริษัท — F2 อาหารทะเลและเพาะเลี้ยง

_ทุกบริษัทใน perimeter ของ Segment ที่สอบทาน_

| Ticker | บทบาท | M-cap | RFO YoY | NPAT YoY | ราคา YTD | P/E | Margin |
|---|---|---|---|---|---|---|---|
| TU | ผู้นำและกำหนดทิศ | THB 56.6bn | -4.1% | -7.5% | +3.9% | 10.9x | 3.5% |
| ASIAN | บริษัทในกลุ่ม | THB 6.2bn | -0.1% | -19.6% | +5.6% | 10.2x | 6.3% |
| TC | บริษัทในกลุ่ม | THB 2.3bn | -2.5% | -37.0% | +40.6% | 11.0x | 3.2% |
| CFRESH | ตัวเทียบ | THB 1.3bn | +6.8% | กลับเป็นกำไร | +97.2% | 16.6x | 0.4% |
| CHOTI | บริษัทในกลุ่ม | THB 525m | -4.5% | ขาดทุนเพิ่มขึ้น | +13.8% | n.m. | -17.6% |

##### TU — ผู้นำและกำหนดทิศ · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ไทยยูเนี่ยน กรุ๊ป จำกัด (มหาชน)** — รายได้และกำไรเคลื่อนไหวสอดคล้องกัน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและส่งออกอาหารสำเร็จรูปแช่แข็งและบรรจุกระป๋อง และขยายธุรกิจให้ครบวงจรด้วยธุรกิจอาหารสำเร็จรูปและอาหารว่าง โดยเน้นอาหารทะเล ธุรกิจบรรจุภัณฑ์และสิ่งพิมพ์ ธุรกิจการตลาดภายในประเทศ ธุรกิจอาหารสัตว์ และธุรกิจพัฒนาสายพันธุ์กุ้งเพื่อจำหน่าย

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 56.6bn | 13.30 | +3.9% | 10.9x | 3.5% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 138bn → FY2025 THB 133bn · −5.7bn · -4.1%

- ยอดขาย FY2025 ลดประมาณ 4% ในรูปเงินบาท แม้ปริมาณขายยังเติบโต เพราะเงินบาทแข็งและผลแปลงค่างบหักล้างสัญญาณด้านปริมาณ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ธุรกิจอาหารทะเลแช่เย็น 3) ธุรกิจอาหารสัตว์ และ 4) ธุรกิจอื่นๆ ยอดขายของธุรกิจอาหารทะเลแช่แข็งอยู่ที่ 12,340 ล้านบาท เพิ่มขึ้น 3.4% จากช่วงเดียวกันของปีก่อน โดยมีสาเหตุ หลักจากปริมาณขายที่เพิ่มขึ้น 5.6% จากช่วงเดียวกันของปีก่อน แม้ว่าจะมีแรงกดดันจากอัตราแลกเปลี่ยนที่ส่งผลกระทบ บางส่วนต่อยอดขาย ทั้งนี้การเติบโตของยอดขายดังกล่าวมีสาเหตุหลักจากการปรับราคาขายเพื่อสะท้อนผลกระทบจาก มาตรการภาษีนำเข้าของสหรัฐฯ และผลการดำเนินงานที่แข็งแกร่งของธุรกิจอาหารสัตว์ สำหรับการเติบโตของปริมาณขาย ส่วนใหญ่มาจากธุรกิจอาหารสัตว์เป็นหลัก ขณะที่ปริมาณขายในตลาดสหรัฐฯ ยังคงเผชิญแรงกดดันจากผลกระทบของ

  `MDA_TU_FY2025` · `p050` · SHA d511aa9e9377
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 5.0bn → FY2025 THB 4.6bn · −375m · -7.5%

- กำไรสุทธิลด 7.5% แม้อัตรากำไรขั้นต้นทำสถิติ 18.9% เพราะต้นทุน การปรับโครงสร้าง และค่าใช้จ่ายดำเนินงานดูดซับกำไรขั้นต้นที่ดีขึ้น
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > อำนาจควบคุม กำไรสุทธิตามที่ประกาศ 1,213 1,304 1,013 -22.3% -16.5% 4,985 4,609 -7.5% Transformation costs (299) (211) (156) -26.0% -47.8% (701) (899) 28.3% กำไรสุทธิตามที่ปรับปรุง* 1,512 1,515 1,169 -22.8% -22.7% 5,685 5,508 -3.1% EBITDA 3,201 3,419 2,998 -12.3% -6.3% 13,361 12,217 -8.6% EBITDA ตามที่ปรับปรุง* 3,500 3,630 3,154 -13.1% -9.9% 14,062 13,115 -6.7% กำไรต่อหุ้น (บาท/หุ้น) 0.26 0.34 0.26 -24.1% -3.0% 1.08 1.16 7.2% อัตรากำไรขั้นต้น 18.7% 19.0% 18.3% -0.7% -0.4% 18.5% 18.9% 0.4%

  `MDA_TU_FY2025` · `p025` · SHA 8c8964a9342b
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: คำนิยาม ค่าใช้จ่ายในการขายและการบริหาร = ค่าใช้จ่ายในการขาย ค่าใช้จ่ายในการบริหาร และ กลับรายการจากการด้อยค่าสินทรัพย์ทางการเงิน สุทธิ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > คำนิยาม ค่าใช้จ่ายในการขายและการบริหาร = ค่าใช้จ่ายในการขาย ค่าใช้จ่ายในการบริหาร และ กลับรายการจากการด้อยค่าสินทรัพย์ทางการเงิน สุทธิ

  `MDA_TU_FY2025` · `p112` · SHA d1b8b7ef26a3
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_TU_FY2025`

##### ASIAN — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท เอเชี่ยนซี คอร์ปอเรชั่น จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — แปรรูปอาหารแช่เยือกแข็ง เพื่อจำหน่ายและส่งออก ทั้งที่เป็นผลิตภัณฑ์ภายใต้เครื่องหมายการค้าของบริษัท และผลิตภัณฑ์ภายใต้เครื่องหมายการค้าของลูกค้า

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 6.2bn | 7.60 | +5.6% | 10.2x | 6.3% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 20 · NPAT 20 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 2

**RFO — เพราะอะไร** — FY2024 THB 10.8bn → FY2025 THB 10.8bn · −13m · -0.1%

- RFO ปี 2568 อยู่ที่ 10,767 ลบ. ลด 0.1% YoY; MD&A ระบุว่า ธุรกิจอาหารสัตว์เลี้ยงและปลาป๋น ธุรกิจอาหารสัตว์เลี้ยงยังคงเป็นกลุ่มธุรกิจหลักที่สร้างรายได้สูงสุดให้แก่บริษัทฯ โดยในไตรมาส 4 ปี 2568 มี ยอดขาย 11,373 ตัน เพิ่มขึ้น 14.7% จากช่วงเดียวกันของปีก่อน (YOY) และเพิ่มขึ้นจากไตรมาสก่อนหน้าอีกด้วย ในขณะที่รายได้ของธุรกิจนี้อยู่ที่ 1,614 ล้านบาท เพิ่มขึ้น 4.2% จากช่วงเดียวกันของปีก่อน (YOY) อย่างไรก็ดีรายได้ที่ ได้รับ ควรจะมีผลดำเนินงานที่สูงกว่านี้ แต่เนื่องจากผลกระทบจากการแข็งค่าของเงินบาท จึงกดดันรายได้จากการ ส่งออก ทั้งที่ปริมาณการขายเพิ่มขึ้นถึง 14.7% แต่รายได้กลับเพิ่มขึ้นเพียง 4.2% โดยที่ตลาดหลักยังคงเป็น ส
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ธุรกิจอาหารสัตว์เลี้ยงและปลาป๋น ธุรกิจอาหารสัตว์เลี้ยงยังคงเป็นกลุ่มธุรกิจหลักที่สร้างรายได้สูงสุดให้แก่บริษัทฯ โดยในไตรมาส 4 ปี 2568 มี ยอดขาย 11,373 ตัน เพิ่มขึ้น 14.7% จากช่วงเดียวกันของปีก่อน (YOY) และเพิ่มขึ้นจากไตรมาสก่อนหน้าอีกด้วย ในขณะที่รายได้ของธุรกิจนี้อยู่ที่ 1,614 ล้านบาท เพิ่มขึ้น 4.2% จากช่วงเดียวกันของปีก่อน (YOY) อย่างไรก็ดีรายได้ที่ ได้รับ ควรจะมีผลดำเนินงานที่สูงกว่านี้ แต่เนื่องจากผลกระทบจากการแข็งค่าของเงินบาท จึงกดดันรายได้จากการ ส่งออก ทั้งที่ปริมาณการขายเพิ่มขึ้นถึง 14.7% แต่รายได้กลับเพิ่มขึ้นเพียง 4.2% โดยที่ตลาดหลักยังคงเป็น สหรัฐอเมริกา ตามมาด้วย ยุโรป ซึ่งรวมถึงสหราชอาณาจักร เยอรมนี และอิตาลีทั้งสองตลาดยังคงมีความต้องการสูง โดยเฉพาะในกลุ่มผลิตภัณฑ์อาหารสัตว์แบบเ

  `MDA_ASIAN_FY2025` · `p015` · SHA 1e510dbddb5c
  </details>
- RFO ปี 2568 อยู่ที่ 10,767 ลบ. ลด 0.1% YoY; MD&A ระบุว่า ธุรกิจอาหารสัตว์น้ำ ในไตรมาส 4 ปี 2568 ธุรกิจอาหารสัตว์น้ำมียอดขาย 5,413 ตัน ลดลง 2.2% จากช่วงเดียวกันของปีก่อน (YOY) และ ลดลง 14.6% จากไตรมาสก่อน (QOQ) ขณะที่รายได้อยู่ที่ 210 ล้านบาท ลดลง 4.4% (YOY) และ 14.9% (QOQ) สาเหตุหลักมาจากการฤดูกาลเลี้ยงกุ้งที่มีการชะลอตัวในช่วงเดือน พ.ย. - กพ. สำหรับปี 2568 นั้น ธุรกิจอาหารสัตว์น้ำมียอดขายรวม 21,271 ตัน ลดลง 5.6% จากปีก่อนหน้า (YOY) และมี รายได้รวม 835 ล้านบาท ลดลง 6.4% (YOY) การปรับตัวลดลงดังกล่าวเป็นผลจาก การคัดเลือกกลุ่มลูกค้าที่มีคุณภาพ โดยบริษัทฯ มุ่งเน้นเฉพาะลูกค้าที่มีศักยภาพในการชำระเงินและมีวินัยทางกา
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ธุรกิจอาหารสัตว์น้ำ ในไตรมาส 4 ปี 2568 ธุรกิจอาหารสัตว์น้ำมียอดขาย 5,413 ตัน ลดลง 2.2% จากช่วงเดียวกันของปีก่อน (YOY) และ ลดลง 14.6% จากไตรมาสก่อน (QOQ) ขณะที่รายได้อยู่ที่ 210 ล้านบาท ลดลง 4.4% (YOY) และ 14.9% (QOQ) สาเหตุหลักมาจากการฤดูกาลเลี้ยงกุ้งที่มีการชะลอตัวในช่วงเดือน พ.ย. - กพ. สำหรับปี 2568 นั้น ธุรกิจอาหารสัตว์น้ำมียอดขายรวม 21,271 ตัน ลดลง 5.6% จากปีก่อนหน้า (YOY) และมี รายได้รวม 835 ล้านบาท ลดลง 6.4% (YOY) การปรับตัวลดลงดังกล่าวเป็นผลจาก การคัดเลือกกลุ่มลูกค้าที่มีคุณภาพ โดยบริษัทฯ มุ่งเน้นเฉพาะลูกค้าที่มีศักยภาพในการชำระเงินและมีวินัยทางการเงินที่ดี เพื่อยกระดับคุณภาพของพอร์ต

  `MDA_ASIAN_FY2025` · `p020` · SHA b0f1a4e0a8a9
  </details>
- RFO ปี 2568 อยู่ที่ 10,767 ลบ. ลด 0.1% YoY; MD&A ระบุว่า ภาพรวมผลการดำเนินงานตามกลุ่มธรกิจ ในไตรมาส 4 ปี 2568 บริษัทฯ มีปริมาณการขายรวม 20,916 ตัน เพิ่มขึ้น 8.1% จากช่วงเดียวกันของปีก่อน (YOY) สะท้อนการฟืนตัวของธุรกิจอาหารทะเลแช่เยือกแข็งและความต่อเนื่องของธุรกิจอาหารสัตว์เลี้ยง ทำให้รายได้ รวมในไตรมาสนี้อยู่ที่ 2,957 ล้านบาท เพิ่มขึ้น 9.1% (YOY) จากปริมาณการขายดังกล่าวข้างต้น สำหรับผลดำเนินงานในปี 2568 บริษัทฯ มีปริมาณการขายรวม 78,943 ตัน เพิ่มขึ้น 4.6% จากปี 2567 (YOY) ซึ่งเป็นผลจากเจริญเติบโตของธุรกิจอาหารสัตว์เลี้ยง ถึงแม้ว่าธุรกิจอื่นจะมีการชะลอตัวเล็กน้อยก็ตาม รายได้จากการ ขายและบริการรวมอยู่ที่ 10,784
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ภาพรวมผลการดำเนินงานตามกลุ่มธรกิจ ในไตรมาส 4 ปี 2568 บริษัทฯ มีปริมาณการขายรวม 20,916 ตัน เพิ่มขึ้น 8.1% จากช่วงเดียวกันของปีก่อน (YOY) สะท้อนการฟืนตัวของธุรกิจอาหารทะเลแช่เยือกแข็งและความต่อเนื่องของธุรกิจอาหารสัตว์เลี้ยง ทำให้รายได้ รวมในไตรมาสนี้อยู่ที่ 2,957 ล้านบาท เพิ่มขึ้น 9.1% (YOY) จากปริมาณการขายดังกล่าวข้างต้น สำหรับผลดำเนินงานในปี 2568 บริษัทฯ มีปริมาณการขายรวม 78,943 ตัน เพิ่มขึ้น 4.6% จากปี 2567 (YOY) ซึ่งเป็นผลจากเจริญเติบโตของธุรกิจอาหารสัตว์เลี้ยง ถึงแม้ว่าธุรกิจอื่นจะมีการชะลอตัวเล็กน้อยก็ตาม รายได้จากการ ขายและบริการรวมอยู่ที่ 10,784 ล้านบาท ลดลง 0.5% จากปี 2567 (10,833 ล้านบาท) การลดลงของรายได้ดังกล่าว เป็นผลจากผลกระทบจากการแข็งค่าของเงินบาท ซึ่งทำให้รายได้ส่วนหลักที่มาจ

  `MDA_ASIAN_FY2025` · `p007` · SHA 92daa4288784
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 848m → FY2025 THB 682m · −167m · -19.6%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 682 ลบ. ลด 19.6% YoY; MD&A ระบุว่า กำไรสุทธิและกำไรต่อหุ้น ในไตรมาส 4 ปี 2568 บริษัทฯ มีกำไรสุทธิส่วนที่เป็นของบริษัทใหญ่เท่ากับ 148 ล้านบาท เพิ่มขึ้นจาก 114 ล้านบาทในไตรมาส 4 ปี 2567 (29.9% YOY) แต่ลดลงจาก 169 ล้านบาทในไตรมาส 3 ปี 2568 (12.6% QOQ) ในไตร มาส 4 ปี 2568 บริษัทฯ มีกำไรต่อหุ้นพื้นฐาน (BASIC EPS) อยู่ที่ 0.18 บาทต่อหุ้น เพิ่มขึ้นจาก 0.14 บาทต่อหุ้นในไตร มาส 4 ปี 2567 (27.7% YOY) แต่ลดลงจาก 0.21 บาทในไตรมาส 3 ปี 2568 (14.1% QOQ) การเพิ่มขึ้นของกำไรสุทธิ ส่วนที่เป็นของบริษัทใหญ่ เป็นผลจากการลดค่าใช้จ่ายในการดำเนินงาน และการลดการขาดทุนจากอัตราแลกเปลี่ยน สำหรับปี 2568 บริษัทฯ มีกำ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไรสุทธิและกำไรต่อหุ้น ในไตรมาส 4 ปี 2568 บริษัทฯ มีกำไรสุทธิส่วนที่เป็นของบริษัทใหญ่เท่ากับ 148 ล้านบาท เพิ่มขึ้นจาก 114 ล้านบาทในไตรมาส 4 ปี 2567 (29.9% YOY) แต่ลดลงจาก 169 ล้านบาทในไตรมาส 3 ปี 2568 (12.6% QOQ) ในไตร มาส 4 ปี 2568 บริษัทฯ มีกำไรต่อหุ้นพื้นฐาน (BASIC EPS) อยู่ที่ 0.18 บาทต่อหุ้น เพิ่มขึ้นจาก 0.14 บาทต่อหุ้นในไตร มาส 4 ปี 2567 (27.7% YOY) แต่ลดลงจาก 0.21 บาทในไตรมาส 3 ปี 2568 (14.1% QOQ) การเพิ่มขึ้นของกำไรสุทธิ ส่วนที่เป็นของบริษัทใหญ่ เป็นผลจากการลดค่าใช้จ่ายในการดำเนินงาน และการลดการขาดทุนจากอัตราแลกเปลี่ยน สำหรับปี 2568 บริษัทฯ มีกำไรส่วนที่เป็นของบริษัทใหญ่เท่ากับ 682 ล้านบาท ลดลง 19.6% YOY ซึ่ง สอดคล้องกับการลดลงของอัตรากำไรขั้นต้นและรายได้รวม อย่างไรก็ดีบริษัทฯ สามาร

  `MDA_ASIAN_FY2025` · `p050` · SHA 2a7239d92dce
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 682 ลบ. ลด 19.6% YoY; MD&A ระบุว่า กำไรขั้นต้น บริษัทมีกำไรขั้นต้นในไตรมาส 4 ปี 2568 จำนวน 365 ล้านบาท คิดเป็นอัตรากำไรขั้นต้น 12.4% ลดลงจาก 14.8% ในช่วงเดียวกันของปีก่อน และใกล้เคียงกับไตรมาสก่อน (13.2%) การลดลงของอัตรากำไรขั้นต้นสะท้อน ผลกระทบจากการแข็งค่าของเงินบาท ราคาขายเฉลี่ยลดลงส่งผลให้กำไรขั้นต้นลดลงตามไปด้วย แม้ว่าบริษัทจะ สามารถปรับราคาขายกับลูกค้าบางรายได้ แต่ยังไม่เพียงพอที่จะชดเชยผลจากการแข็งค่าของเงินบาทได้ สำหรับปี 2568 บริษัทมีกำไรขั้นต้น 1,485 ล้านบาท ลดลง 21.8% จากงวดเดียวกันของปีก่อน (1,898 ล้าน บาท) โดยอัตรากำไรขั้นต้นลดลงจาก 17.6% เหลือ 13.8% สาเหตุหลักผลกระทบจากการแข
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไรขั้นต้น บริษัทมีกำไรขั้นต้นในไตรมาส 4 ปี 2568 จำนวน 365 ล้านบาท คิดเป็นอัตรากำไรขั้นต้น 12.4% ลดลงจาก 14.8% ในช่วงเดียวกันของปีก่อน และใกล้เคียงกับไตรมาสก่อน (13.2%) การลดลงของอัตรากำไรขั้นต้นสะท้อน ผลกระทบจากการแข็งค่าของเงินบาท ราคาขายเฉลี่ยลดลงส่งผลให้กำไรขั้นต้นลดลงตามไปด้วย แม้ว่าบริษัทจะ สามารถปรับราคาขายกับลูกค้าบางรายได้ แต่ยังไม่เพียงพอที่จะชดเชยผลจากการแข็งค่าของเงินบาทได้ สำหรับปี 2568 บริษัทมีกำไรขั้นต้น 1,485 ล้านบาท ลดลง 21.8% จากงวดเดียวกันของปีก่อน (1,898 ล้าน บาท) โดยอัตรากำไรขั้นต้นลดลงจาก 17.6% เหลือ 13.8% สาเหตุหลักผลกระทบจากการแข็งค่าของเงินบาท โดยเฉพาะในธุรกิจอาหารสัตว์เลี้ยง ที่มีปริมาณการขายที่ 58 % ของรายได้ทั้งหมด และมีปริมาณการขายเพิ่มขึ้น 16% จากปีก่อน

  `MDA_ASIAN_FY2025` · `p035` · SHA 60cbc45667f2
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 682 ลบ. ลด 19.6% YoY; MD&A ระบุว่า งบกำไรขาดทุน ปี 2568 % ปี 2567 % % YoY รายได้จากการขายและบริการ 10,767 100 10,780 100 (0.1) ต้นทุนขายและบริการ (9,282) (86) (8,882) (82) 4.5 กำไรขัҟนต้น 1,485 14 1,898 18 (21.8) ค่าใช้จ่ายในการดำเนินงาน (656) (6) (757) (7) (13.4) กำไรจากการดำเนินงาน 829 8 1,141 11 (27.3) รายได้อืѷน 145 1 115 1 25.6 กำไร(ขาดทุน)จากอัตราแลกเปลีѷยน 18 0 (2) (0) (1,220.9) ค่าใช้จ่ายอืѷน (3) (0) (2) (0) 77.2 รายได้ (ต้นทุน) ทางการเงิน 17 0 22 0 (20.1) กำไรก่อนภาษีเงินได้ 1,006 9 1,274 12 (21.1) ค่าใช้จ่ายภาษีเงินได้ (103) (1) (125) (1) (17.8) กำไรสุทธิ 903 8 1,149 11 (21.4)
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > งบกำไรขาดทุน ปี 2568 % ปี 2567 % % YoY รายได้จากการขายและบริการ 10,767 100 10,780 100 (0.1) ต้นทุนขายและบริการ (9,282) (86) (8,882) (82) 4.5 กำไรขัҟนต้น 1,485 14 1,898 18 (21.8) ค่าใช้จ่ายในการดำเนินงาน (656) (6) (757) (7) (13.4) กำไรจากการดำเนินงาน 829 8 1,141 11 (27.3) รายได้อืѷน 145 1 115 1 25.6 กำไร(ขาดทุน)จากอัตราแลกเปลีѷยน 18 0 (2) (0) (1,220.9) ค่าใช้จ่ายอืѷน (3) (0) (2) (0) 77.2 รายได้ (ต้นทุน) ทางการเงิน 17 0 22 0 (20.1) กำไรก่อนภาษีเงินได้ 1,006 9 1,274 12 (21.1) ค่าใช้จ่ายภาษีเงินได้ (103) (1) (125) (1) (17.8) กำไรสุทธิ 903 8 1,149 11 (21.4)

  `MDA_ASIAN_FY2025` · `p028` · SHA 1618d9de3c5b
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 682 ลบ. ลด 19.6% YoY; MD&A ระบุว่า ผลกระทบเชิงลบจากการแข็งค่าของเงินบาท ที่เกิดขึ้นในปี 2568  ในไตรมาส 4 ปี 2568 บริษัทฯ มีกำไรสุทธิ 148 ล้านบาท เพิ่มขึ้น 29.9% เมื่อเทียบกับช่วงเดียวกันของปีก่อน (YOY) และ ลดลง 12.6% เมื่อเทียบกับไตรมาสก่อนหน้า (QOQ) และ มีกำไรต่อหุ้น (EPS) อยู่ที่ 0.18 บาท (ลดลงจาก 0.21 บาท ในไตรมาสเดียวกันของปีก่อน)  กำไรสุทธิสำหรับปี 2568 อยู่ที่ 682 ล้านบาท ลดลง 19.6% เมื่อเทียบกับปีก่อนหน้า สาเหตุหลักมาจากอัตรา กำไรขั้นต้นที่ลดลงอย่างมาก (13.8% ลดลง จาก 17.6% ในปี 2567) ซึ่งเป็นผลกระทบโดยตรงจากการแข็ง ค่าของเงินบาท มีกำไรต่อหุ้น (EPS) อยู่ที่ 0.84 บาท (ลดลง 19.1% จ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ผลกระทบเชิงลบจากการแข็งค่าของเงินบาท ที่เกิดขึ้นในปี 2568  ในไตรมาส 4 ปี 2568 บริษัทฯ มีกำไรสุทธิ 148 ล้านบาท เพิ่มขึ้น 29.9% เมื่อเทียบกับช่วงเดียวกันของปีก่อน (YOY) และ ลดลง 12.6% เมื่อเทียบกับไตรมาสก่อนหน้า (QOQ) และ มีกำไรต่อหุ้น (EPS) อยู่ที่ 0.18 บาท (ลดลงจาก 0.21 บาท ในไตรมาสเดียวกันของปีก่อน)  กำไรสุทธิสำหรับปี 2568 อยู่ที่ 682 ล้านบาท ลดลง 19.6% เมื่อเทียบกับปีก่อนหน้า สาเหตุหลักมาจากอัตรา กำไรขั้นต้นที่ลดลงอย่างมาก (13.8% ลดลง จาก 17.6% ในปี 2567) ซึ่งเป็นผลกระทบโดยตรงจากการแข็ง ค่าของเงินบาท มีกำไรต่อหุ้น (EPS) อยู่ที่ 0.84 บาท (ลดลง 19.1% จาก 1.04 บาท ในปี 2567) คำอธิบายและวิเคราะห์ของฝ๋ายจัดการไตรมาส 4 ปี 2568 และปี 2568 สิ้นสุดวันที่ 31 ธันวาคม 2568 หน้า 1

  `MDA_ASIAN_FY2025` · `p005` · SHA 975729cc985c
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: สินทรัพย์ไม่หมุนเวียน ณ สิ้นปี 2568 บริษัทฯ มีสินทรัพย์ไม่หมุนเวียนรวม 4,160 ล้านบาท เพิ่มขึ้น 4.2% จากสิ้นปี 2567 ที่ 3,995 ล้านบาท การเพิ่มขึ้นส่วนใหญ่มาจาก การลงทุนในที่ดิน อาคาร และอุปกรณ์ ซึ่งเพิ่มขึ้นเป็น 3,614 ล้านบาท จาก 3,396 ล้านบาท หรือเพิ่มขึ้น 6.4% สะท้อนถึงการลงทุนต่อเนื่องเพื่อขยายกำลังการผลิตและปรับปรุงประสิทธิภาพใน สายการผลิตอาหารสัตว์เลี้ยง ทั้งในส่วนของเครื่องจักรและอาคารโรงงาน เพื่อรองรับคำสั่งซื้อที่มีแนวโน้มเพิ่มขึ้นใน อนาคต ขณะที่ เงินลงทุนในบริษัทร่วม ลดลงเล็กน้อยตามการปรับมูลค่ายุติธรรมของเงินลงทุนบางรายการ ส่วน สินทรัพย์ไม่หมุนเ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > สินทรัพย์ไม่หมุนเวียน ณ สิ้นปี 2568 บริษัทฯ มีสินทรัพย์ไม่หมุนเวียนรวม 4,160 ล้านบาท เพิ่มขึ้น 4.2% จากสิ้นปี 2567 ที่ 3,995 ล้านบาท การเพิ่มขึ้นส่วนใหญ่มาจาก การลงทุนในที่ดิน อาคาร และอุปกรณ์ ซึ่งเพิ่มขึ้นเป็น 3,614 ล้านบาท จาก 3,396 ล้านบาท หรือเพิ่มขึ้น 6.4% สะท้อนถึงการลงทุนต่อเนื่องเพื่อขยายกำลังการผลิตและปรับปรุงประสิทธิภาพใน สายการผลิตอาหารสัตว์เลี้ยง ทั้งในส่วนของเครื่องจักรและอาคารโรงงาน เพื่อรองรับคำสั่งซื้อที่มีแนวโน้มเพิ่มขึ้นใน อนาคต ขณะที่ เงินลงทุนในบริษัทร่วม ลดลงเล็กน้อยตามการปรับมูลค่ายุติธรรมของเงินลงทุนบางรายการ ส่วน สินทรัพย์ไม่หมุนเวียนอื่น ๆ ทรงตัวอยู่ในระดับใกล้เคียงกับสิ้นปี 2567 ซึ่งส่วนใหญ่เป็นเงินมัดจำระยะยาวและ

  `MDA_ASIAN_FY2025` · `p062` · SHA 726100b23856
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: แตกต่างจากปีก่อนซึ่งมีการบันทึก ค่าใช้จ่ายด้อยค่าการลงทุนในบริษัทร่วม จำนวน 30 ล้านบาท
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > แตกต่างจากปีก่อนซึ่งมีการบันทึก ค่าใช้จ่ายด้อยค่าการลงทุนในบริษัทร่วม จำนวน 30 ล้านบาท

  `MDA_ASIAN_FY2025` · `p043` · SHA f2fbfee53cff
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_ASIAN_FY2025`

##### TC — บริษัทในกลุ่ม · ติดตาม

**บริษัท ทรอปิคอลแคนนิ่ง (ประเทศไทย) จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและส่งออกอาหารทะเลบรรจุกระป๋องและซอง แบ่งเป็น 3 กลุ่ม คือ1)กลุ่มผลิตภัณฑ์ปลาทูน่าบรรจุกระป๋องและบรรจุซอง (Regular Tuna Products) มีผลิตภัณฑ์หลักคือ ปลาทูน่าในน้ำแร่ ปลาทูน่าในน้ำเกลือ ปลาทูน่าในน้ำมัน2)กลุ่มผลิตภัณฑ์แปรรูปพร้อมทานบรรจุกระป๋องและบรรจุซอง (Ready-To-Serve Products) มีผลิตภัณฑ์หลักคือ ปลาซาร์ดีนในซอสมะเขือเทศ ปลาแมคเคอเรลในซอสมะเขือเทศ ปลาทูน่าแปรรูปพร้อมทาน ปลาแซลมอนแปรรูปพร้อมทาน3) กลุ่มอาหารสัต…

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 2.3bn | 7.00 | +40.6% | 11.0x | 3.2% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 12 · NPAT 5 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 6.6bn → FY2025 THB 6.4bn · −164m · -2.5%

- RFO ปี 2568 อยู่ที่ 6,406 ลบ. ลด 2.5% YoY; MD&A ระบุว่า สูงขึ้น - ค่าใช้จ่ายในการขายและบริหารในปี 2568 มีจำนวน 298.89 ล้านบาท หรือคิดเป็นร้อยละ 4.67 ของ รายได้จากการขายสินค้า ลดลง 14.91 ล้านบาทหรือลดลงร้อยละ 4.75 เมื่อเทียบปี 2567 เนื่องจากค่าระวางเรือ และการตั้งค่าเผื่อหนี้สงสัยจะสูญที่ปรับลดลง ทำให้ค่าใช้จ่ายในการขายลดลง 6.14 ล้านบาท และค่าใช้จ่ายในการ บริหารที่ลดลง 8.77 ล้านบาท - ต้นทุนทางการเงินในที่ปี 2568 มีจำนวน 10.96 ล้านบาท คิดเป็นร้อยละ 0.17 ของรายได้จากการขาย ลดลง 5.43 ล้านบาท หรือลดลงร้อยละ 33.09 เมื่อเทียบกับในปี 2567
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > สูงขึ้น - ค่าใช้จ่ายในการขายและบริหารในปี 2568 มีจำนวน 298.89 ล้านบาท หรือคิดเป็นร้อยละ 4.67 ของ รายได้จากการขายสินค้า ลดลง 14.91 ล้านบาทหรือลดลงร้อยละ 4.75 เมื่อเทียบปี 2567 เนื่องจากค่าระวางเรือ และการตั้งค่าเผื่อหนี้สงสัยจะสูญที่ปรับลดลง ทำให้ค่าใช้จ่ายในการขายลดลง 6.14 ล้านบาท และค่าใช้จ่ายในการ บริหารที่ลดลง 8.77 ล้านบาท - ต้นทุนทางการเงินในที่ปี 2568 มีจำนวน 10.96 ล้านบาท คิดเป็นร้อยละ 0.17 ของรายได้จากการขาย ลดลง 5.43 ล้านบาท หรือลดลงร้อยละ 33.09 เมื่อเทียบกับในปี 2567

  `MDA_TC_FY2025` · `p016` · SHA 42cbd28290b4
  </details>
- RFO ปี 2568 อยู่ที่ 6,406 ลบ. ลด 2.5% YoY; MD&A ระบุว่า กำไรขั้นต้นและอัตรากำไรขั้นต้น ในปี 2568 บริษัทและบริษัทย่อยมีก1.50% ำไรขั้นต้น 501.76 ล้านบาท ลดลง 214.71 ล้านบาท หรือลดลง ร้อยละ 29.97 เมื่อเทียบกับปี 2567 โดยมีสาเหตุหลักมาจากต้นทุนการผลิตสูงขึ้นจากราคาวัตถุดิบที่ปรับตัว1.50% สูงขึ้น และการปรับขึ้นค่าแรงขั้นต่ำในเขตอำเภอหาดใหญ่จังหวัดสงขลา อีกทั้งรายได้จากการขายลดลงจาก อัตราแลกเปลี่ยนเงินบาทที่แข็งค่าขึ้น โดยต้นทุนขายคิดเป็นร้อยละ 92.17 ของรายได้จากการขาย (ในปี 2567 มี ต้นทุนขายคิดเป็นร้อยละ 89.09 ของรายได้จากการขาย) ส่งผลต่ออัตรากำไรขั้นต้นที่เปลี่ยนแปลงไป อัตรากำไรขั้นต้นในปี 2568 ลดลงเป็นร้อยละ 7.8
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไรขั้นต้นและอัตรากำไรขั้นต้น ในปี 2568 บริษัทและบริษัทย่อยมีก1.50% ำไรขั้นต้น 501.76 ล้านบาท ลดลง 214.71 ล้านบาท หรือลดลง ร้อยละ 29.97 เมื่อเทียบกับปี 2567 โดยมีสาเหตุหลักมาจากต้นทุนการผลิตสูงขึ้นจากราคาวัตถุดิบที่ปรับตัว1.50% สูงขึ้น และการปรับขึ้นค่าแรงขั้นต่ำในเขตอำเภอหาดใหญ่จังหวัดสงขลา อีกทั้งรายได้จากการขายลดลงจาก อัตราแลกเปลี่ยนเงินบาทที่แข็งค่าขึ้น โดยต้นทุนขายคิดเป็นร้อยละ 92.17 ของรายได้จากการขาย (ในปี 2567 มี ต้นทุนขายคิดเป็นร้อยละ 89.09 ของรายได้จากการขาย) ส่งผลต่ออัตรากำไรขั้นต้นที่เปลี่ยนแปลงไป อัตรากำไรขั้นต้นในปี 2568 ลดลงเป็นร้อยละ 7.83 ในขณะที่ในปี 2567 คิดเป็นร้อยละ 10.91

  `MDA_TC_FY2025` · `p012` · SHA e8b61fc42d40
  </details>
- RFO ปี 2568 อยู่ที่ 6,406 ลบ. ลด 2.5% YoY; MD&A ระบุว่า ค่าใช้จ่าย บริษัทและบริษัทย่อยมีค่าใช้จ่ายรวมในปี 2568 จำนวน 6,202.85 ล้านบาท เพิ่มขึ้น 36.29 ล้านบาท หรือคิดเป็นร้อยละ 0.59 เมื่อเทียบกับปี 2567 โดยมีสาเหตุหลักมาจาก - ต้นทุนขายในปี 2568 มีจำนวน 5,903.96 ล้านบาท หรือคิดเป็นร้อยละ 92.17 ของรายได้จากการขาย เพิ่มขึ้น 51.20 ล้านบาท หรือเพิ่มขึ้นร้อยละ 0.87 เมื่อเทียบกับปี 2567 เนื่องจากต้นทุนค่าแรงและวัตถุดิบเพิ่ม
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ค่าใช้จ่าย บริษัทและบริษัทย่อยมีค่าใช้จ่ายรวมในปี 2568 จำนวน 6,202.85 ล้านบาท เพิ่มขึ้น 36.29 ล้านบาท หรือคิดเป็นร้อยละ 0.59 เมื่อเทียบกับปี 2567 โดยมีสาเหตุหลักมาจาก - ต้นทุนขายในปี 2568 มีจำนวน 5,903.96 ล้านบาท หรือคิดเป็นร้อยละ 92.17 ของรายได้จากการขาย เพิ่มขึ้น 51.20 ล้านบาท หรือเพิ่มขึ้นร้อยละ 0.87 เมื่อเทียบกับปี 2567 เนื่องจากต้นทุนค่าแรงและวัตถุดิบเพิ่ม

  `MDA_TC_FY2025` · `p015` · SHA f14700da2890
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 329m → FY2025 THB 208m · −122m · -37.0%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 208 ลบ. ลด 37.0% YoY; MD&A ระบุว่า กำไรขั้นต้นและอัตรากำไรขั้นต้น ในปี 2568 บริษัทและบริษัทย่อยมีก1.50% ำไรขั้นต้น 501.76 ล้านบาท ลดลง 214.71 ล้านบาท หรือลดลง ร้อยละ 29.97 เมื่อเทียบกับปี 2567 โดยมีสาเหตุหลักมาจากต้นทุนการผลิตสูงขึ้นจากราคาวัตถุดิบที่ปรับตัว1.50% สูงขึ้น และการปรับขึ้นค่าแรงขั้นต่ำในเขตอำเภอหาดใหญ่จังหวัดสงขลา อีกทั้งรายได้จากการขายลดลงจาก อัตราแลกเปลี่ยนเงินบาทที่แข็งค่าขึ้น โดยต้นทุนขายคิดเป็นร้อยละ 92.17 ของรายได้จากการขาย (ในปี 2567 มี ต้นทุนขายคิดเป็นร้อยละ 89.09 ของรายได้จากการขาย) ส่งผลต่ออัตรากำไรขั้นต้นที่เปลี่ยนแปลงไป อัตรากำไรขั้นต้นในปี 2568 ลดลงเป็นร้อยละ 7.8
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไรขั้นต้นและอัตรากำไรขั้นต้น ในปี 2568 บริษัทและบริษัทย่อยมีก1.50% ำไรขั้นต้น 501.76 ล้านบาท ลดลง 214.71 ล้านบาท หรือลดลง ร้อยละ 29.97 เมื่อเทียบกับปี 2567 โดยมีสาเหตุหลักมาจากต้นทุนการผลิตสูงขึ้นจากราคาวัตถุดิบที่ปรับตัว1.50% สูงขึ้น และการปรับขึ้นค่าแรงขั้นต่ำในเขตอำเภอหาดใหญ่จังหวัดสงขลา อีกทั้งรายได้จากการขายลดลงจาก อัตราแลกเปลี่ยนเงินบาทที่แข็งค่าขึ้น โดยต้นทุนขายคิดเป็นร้อยละ 92.17 ของรายได้จากการขาย (ในปี 2567 มี ต้นทุนขายคิดเป็นร้อยละ 89.09 ของรายได้จากการขาย) ส่งผลต่ออัตรากำไรขั้นต้นที่เปลี่ยนแปลงไป อัตรากำไรขั้นต้นในปี 2568 ลดลงเป็นร้อยละ 7.83 ในขณะที่ในปี 2567 คิดเป็นร้อยละ 10.91

  `MDA_TC_FY2025` · `p012` · SHA e8b61fc42d40
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 208 ลบ. ลด 37.0% YoY; MD&A ระบุว่า ค่าใช้จ่าย บริษัทและบริษัทย่อยมีค่าใช้จ่ายรวมในปี 2568 จำนวน 6,202.85 ล้านบาท เพิ่มขึ้น 36.29 ล้านบาท หรือคิดเป็นร้อยละ 0.59 เมื่อเทียบกับปี 2567 โดยมีสาเหตุหลักมาจาก - ต้นทุนขายในปี 2568 มีจำนวน 5,903.96 ล้านบาท หรือคิดเป็นร้อยละ 92.17 ของรายได้จากการขาย เพิ่มขึ้น 51.20 ล้านบาท หรือเพิ่มขึ้นร้อยละ 0.87 เมื่อเทียบกับปี 2567 เนื่องจากต้นทุนค่าแรงและวัตถุดิบเพิ่ม
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ค่าใช้จ่าย บริษัทและบริษัทย่อยมีค่าใช้จ่ายรวมในปี 2568 จำนวน 6,202.85 ล้านบาท เพิ่มขึ้น 36.29 ล้านบาท หรือคิดเป็นร้อยละ 0.59 เมื่อเทียบกับปี 2567 โดยมีสาเหตุหลักมาจาก - ต้นทุนขายในปี 2568 มีจำนวน 5,903.96 ล้านบาท หรือคิดเป็นร้อยละ 92.17 ของรายได้จากการขาย เพิ่มขึ้น 51.20 ล้านบาท หรือเพิ่มขึ้นร้อยละ 0.87 เมื่อเทียบกับปี 2567 เนื่องจากต้นทุนค่าแรงและวัตถุดิบเพิ่ม

  `MDA_TC_FY2025` · `p015` · SHA f14700da2890
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 208 ลบ. ลด 37.0% YoY; MD&A ระบุว่า กำไรจากอัตราแลกเปลี่ยน ในปี 2568 บริษัทและบริษัทย่อยมีกำไรจากอัตราแลกเปลี่ยน 12.02 ล้านบาท คิดเป็นร้อยละ 0.19 ของ รายได้รวม เพิ่มขึ้น 8.95 ล้านบาท หรือเพิ่มขึ้นร้อยละ 291.04 เมื่อเทียบกับในปี 2567 เนื่องจากบริษัทได้เพิ่ม อัตราส่วนการป้องกันความเสี่ยงเงินตราต่างประเทศจากความผันผวนของสกุลเงินต่างประเทศและเงินบาทที่
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไรจากอัตราแลกเปลี่ยน ในปี 2568 บริษัทและบริษัทย่อยมีกำไรจากอัตราแลกเปลี่ยน 12.02 ล้านบาท คิดเป็นร้อยละ 0.19 ของ รายได้รวม เพิ่มขึ้น 8.95 ล้านบาท หรือเพิ่มขึ้นร้อยละ 291.04 เมื่อเทียบกับในปี 2567 เนื่องจากบริษัทได้เพิ่ม อัตราส่วนการป้องกันความเสี่ยงเงินตราต่างประเทศจากความผันผวนของสกุลเงินต่างประเทศและเงินบาทที่

  `MDA_TC_FY2025` · `p013` · SHA cdc3a6236bc5
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 208 ลบ. ลด 37.0% YoY; MD&A ระบุว่า สูงขึ้น - ค่าใช้จ่ายในการขายและบริหารในปี 2568 มีจำนวน 298.89 ล้านบาท หรือคิดเป็นร้อยละ 4.67 ของ รายได้จากการขายสินค้า ลดลง 14.91 ล้านบาทหรือลดลงร้อยละ 4.75 เมื่อเทียบปี 2567 เนื่องจากค่าระวางเรือ และการตั้งค่าเผื่อหนี้สงสัยจะสูญที่ปรับลดลง ทำให้ค่าใช้จ่ายในการขายลดลง 6.14 ล้านบาท และค่าใช้จ่ายในการ บริหารที่ลดลง 8.77 ล้านบาท - ต้นทุนทางการเงินในที่ปี 2568 มีจำนวน 10.96 ล้านบาท คิดเป็นร้อยละ 0.17 ของรายได้จากการขาย ลดลง 5.43 ล้านบาท หรือลดลงร้อยละ 33.09 เมื่อเทียบกับในปี 2567
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > สูงขึ้น - ค่าใช้จ่ายในการขายและบริหารในปี 2568 มีจำนวน 298.89 ล้านบาท หรือคิดเป็นร้อยละ 4.67 ของ รายได้จากการขายสินค้า ลดลง 14.91 ล้านบาทหรือลดลงร้อยละ 4.75 เมื่อเทียบปี 2567 เนื่องจากค่าระวางเรือ และการตั้งค่าเผื่อหนี้สงสัยจะสูญที่ปรับลดลง ทำให้ค่าใช้จ่ายในการขายลดลง 6.14 ล้านบาท และค่าใช้จ่ายในการ บริหารที่ลดลง 8.77 ล้านบาท - ต้นทุนทางการเงินในที่ปี 2568 มีจำนวน 10.96 ล้านบาท คิดเป็นร้อยละ 0.17 ของรายได้จากการขาย ลดลง 5.43 ล้านบาท หรือลดลงร้อยละ 33.09 เมื่อเทียบกับในปี 2567

  `MDA_TC_FY2025` · `p016` · SHA 42cbd28290b4
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_TC_FY2025`

##### CFRESH — ตัวเทียบ · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ซีเฟรชอินดัสตรี จำกัด (มหาชน)** — อยู่ในภาวะฟื้นตัว; อัตราเติบโตมีความสำคัญรองลงมา

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและจำหน่ายผลิตภัณฑ์กุ้งและอาหารทะเลแช่แข็งทั้งในประเทศและต่างประเทศ โดยส่งออกไปจำหน่ายยังต่างประเทศส่วนใหญ่ ภายใต้เครื่องหมายการค้าของบริษัท ได้แก่ Seafresh, Sea Angel, Go-Go, Ultra และเครื่องหมายการค้าของลูกค้า

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.3bn | 1.40 | +97.2% | 16.6x | 0.4% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 1 · NPAT 3 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 7.4bn → FY2025 THB 7.9bn · +501m · +6.8%

- RFO ปี 2568 อยู่ที่ 7,910 ลบ. เพิ่ม 6.8% YoY; MD&A ระบุว่า รายได้จากการขาย รายได้จากการขายของบริษัทฯและบริษัทย่อยสำหรับปี2568 จำนวน7,902.93 ล้านบาทเพิ่มขึ้น505.84 ล้าน
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้จากการขาย รายได้จากการขายของบริษัทฯและบริษัทย่อยสำหรับปี2568 จำนวน7,902.93 ล้านบาทเพิ่มขึ้น505.84 ล้าน

  `MDA_CFRESH_FY2025` · `p004` · SHA 15e311904a33
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 82m → FY2025 THB 29m · +110m

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 28.8 ลบ. จากขาดทุน -81.5 ลบ.; MD&A ระบุว่า ริหารจัดการต้นทุนทีมีประสิทธิภาพส่งผลให้อัตรากำไรจากการ ie
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ริหารจัดการต้นทุนทีมีประสิทธิภาพส่งผลให้อัตรากำไรจากการ ie

  `MDA_CFRESH_FY2025` · `p008` · SHA f6bad5563717
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 28.8 ลบ. จากขาดทุน -81.5 ลบ.; MD&A ระบุว่า อบกับผลขาดทุนจากอัตราแลกเปลี่ยนทีลดลงรวมถึงค่าใช้จ่ายภาษีเงินได้ทีลดลงเมื่อเทียบกับ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > อบกับผลขาดทุนจากอัตราแลกเปลี่ยนทีลดลงรวมถึงค่าใช้จ่ายภาษีเงินได้ทีลดลงเมื่อเทียบกับ

  `MDA_CFRESH_FY2025` · `p009` · SHA 24203932d9f4
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 28.8 ลบ. จากขาดทุน -81.5 ลบ.; MD&A ระบุว่า ก่อนที่มีขาดทุนสุทธิส่วนที่เป็นของผู้ถือหุ้น บริษัทฯจำนวน81.52 ล้านบาท a a ' a : a a v a a a
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ก่อนที่มีขาดทุนสุทธิส่วนที่เป็นของผู้ถือหุ้น บริษัทฯจำนวน81.52 ล้านบาท a a ' a : a a v a a a

  `MDA_CFRESH_FY2025` · `p007` · SHA 097148898e55
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_CFRESH_FY2025`

##### CHOTI — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ห้องเย็นโชติวัฒน์หาดใหญ่ จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผู้ผลิตและส่งออกอาหารทะเลแช่แข็ง

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 525m | 70.00 | +13.8% | n.m. | -17.6% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 3 · NPAT 7 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 2.5bn → FY2025 THB 2.4bn · −114m · -4.5%

- RFO ปี 2568 อยู่ที่ 2,429 ลบ. ลด 4.5% YoY; MD&A ระบุว่า ส่งผลให้รายได้ของบริษัทลดลงจากแผนที่คาดไว้เมื่อเทียบกับช่วงเวลาเดียวกันของปีก่อน 1.2 นอกจากนี้การแข็งค่าของเงินบาทยังส่งผลกระทบโดยตรงต่อรายได้ที่มาจากตลาดต่างประเทศ ซึ่งเป็น รายได้หลักของบริษัทฯ แม้ว่าระดับคำสั่งซื้อจะยังอยู่ในระดับที่ใกล้เคียงกับช่วงเดียวกันของปีก่อนก็ตาม 2. ต้นทุนขายและการให้บริการสำหรับปี 2568 จำนวน 2,717.41 ล้านบาท เพิ่มขึ้น 234.58 ล้านบาท หรือ คิดเป็นเพิ่มขึ้นร้อยละ 9.45 จากช่วงเดียวกันของปีก่อน สาเหตุหลักมาจากผลกระทบของเหตุการณ์อุทกภัยที่ส่งผลให้คุณภาพ สินค้าแช่แข็ง (บางส่วน) ได้รับความเสียหายในเรื่องของอุณหภูมิที่ไม่เป็นไปตามมาตรฐ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ส่งผลให้รายได้ของบริษัทลดลงจากแผนที่คาดไว้เมื่อเทียบกับช่วงเวลาเดียวกันของปีก่อน 1.2 นอกจากนี้การแข็งค่าของเงินบาทยังส่งผลกระทบโดยตรงต่อรายได้ที่มาจากตลาดต่างประเทศ ซึ่งเป็น รายได้หลักของบริษัทฯ แม้ว่าระดับคำสั่งซื้อจะยังอยู่ในระดับที่ใกล้เคียงกับช่วงเดียวกันของปีก่อนก็ตาม 2. ต้นทุนขายและการให้บริการสำหรับปี 2568 จำนวน 2,717.41 ล้านบาท เพิ่มขึ้น 234.58 ล้านบาท หรือ คิดเป็นเพิ่มขึ้นร้อยละ 9.45 จากช่วงเดียวกันของปีก่อน สาเหตุหลักมาจากผลกระทบของเหตุการณ์อุทกภัยที่ส่งผลให้คุณภาพ สินค้าแช่แข็ง (บางส่วน) ได้รับความเสียหายในเรื่องของอุณหภูมิที่ไม่เป็นไปตามมาตรฐานที่กำหนด เนื่องจากน้ำได้เข้าท่วม พื้นที่ของบริษัทฯ เป็นเหตุจำเป็นให้ต้องหยุดจ่ายกระแสไฟฟ้าในพื้นที่บริษัทฯ เพื่อความปลอดภัย ส่งผลกระทบต่ออ

  `MDA_CHOTI_FY2025` · `p005` · SHA 66e8286b6cb6
  </details>
- RFO ปี 2568 อยู่ที่ 2,429 ลบ. ลด 4.5% YoY; MD&A ระบุว่า ผลการดำเนินงาน สำหรับงวดปีสิ้นสุดวันที่ 31 ธันวาคม 2568 บริษัทฯ และบริษัทย่อยมีผลขาดทุนสุทธิจำนวน 428.01 ล้านบาท เพิ่มขึ้นเมื่อเปรียบเทียบกับปีก่อนซึ่งมีขาดทุนสุทธิจำนวน 130.63 ล้านบาท คิดเป็นการเปลี่ยนแปลงขาดทุนสุทธิเพิ่มขึ้น ร้อยละ 227.65 จึงขอชี้แจงถึงสาเหตุการเปลี่ยนแปลงของผลการดำเนินงานของบริษัทฯ และบริษัทย่อย ดังนี้ 1. รายได้จากการขายและการให้บริการสำหรับปี 2568 จำนวน 2,429.13 ล้านบาท ปรับลดลงจำนวน 114.35 ล้านบาท หรือคิดเป็นลดลงร้อยละ 5.39 โดยมีป้จจัยสำคัญมาจาก 1.1 สถานการณ์อุทกภัยในจังหวัดสงขลา ซึ่งเป็นที่ตั้งของบริษัทและโรงงานผลิตสินค้าอาหารทะเลแ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ผลการดำเนินงาน สำหรับงวดปีสิ้นสุดวันที่ 31 ธันวาคม 2568 บริษัทฯ และบริษัทย่อยมีผลขาดทุนสุทธิจำนวน 428.01 ล้านบาท เพิ่มขึ้นเมื่อเปรียบเทียบกับปีก่อนซึ่งมีขาดทุนสุทธิจำนวน 130.63 ล้านบาท คิดเป็นการเปลี่ยนแปลงขาดทุนสุทธิเพิ่มขึ้น ร้อยละ 227.65 จึงขอชี้แจงถึงสาเหตุการเปลี่ยนแปลงของผลการดำเนินงานของบริษัทฯ และบริษัทย่อย ดังนี้ 1. รายได้จากการขายและการให้บริการสำหรับปี 2568 จำนวน 2,429.13 ล้านบาท ปรับลดลงจำนวน 114.35 ล้านบาท หรือคิดเป็นลดลงร้อยละ 5.39 โดยมีป้จจัยสำคัญมาจาก 1.1 สถานการณ์อุทกภัยในจังหวัดสงขลา ซึ่งเป็นที่ตั้งของบริษัทและโรงงานผลิตสินค้าอาหารทะเลแช่แข็ง และผลไม้แช่แข็ง สถานการณ์ดังกล่าวที่เกิดขึ้นในช่วงปลายปีได้ส่งผลต่อการส่งมอบสินค้าให้กับลูกค้าอย่างมีนัยสำคัญ และ

  `MDA_CHOTI_FY2025` · `p004` · SHA 999ac383ae4c
  </details>
- RFO ปี 2568 อยู่ที่ 2,429 ลบ. ลด 4.5% YoY; MD&A ระบุว่า 8. รายได้ภาษีเงินได้ในปี 2568 จำนวน 53.36 ล้านบาท เพิ่มขึ้นร้อยละ 703.61 เมื่อเทียบกับช่วงเดียวกันของ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > 8. รายได้ภาษีเงินได้ในปี 2568 จำนวน 53.36 ล้านบาท เพิ่มขึ้นร้อยละ 703.61 เมื่อเทียบกับช่วงเดียวกันของ

  `MDA_CHOTI_FY2025` · `p011` · SHA 537669967505
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 131m → FY2025 −THB 428m · −297m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -428 ลบ. จาก -131 ลบ.; MD&A ระบุว่า ผลการดำเนินงาน สำหรับงวดปีสิ้นสุดวันที่ 31 ธันวาคม 2568 บริษัทฯ และบริษัทย่อยมีผลขาดทุนสุทธิจำนวน 428.01 ล้านบาท เพิ่มขึ้นเมื่อเปรียบเทียบกับปีก่อนซึ่งมีขาดทุนสุทธิจำนวน 130.63 ล้านบาท คิดเป็นการเปลี่ยนแปลงขาดทุนสุทธิเพิ่มขึ้น ร้อยละ 227.65 จึงขอชี้แจงถึงสาเหตุการเปลี่ยนแปลงของผลการดำเนินงานของบริษัทฯ และบริษัทย่อย ดังนี้ 1. รายได้จากการขายและการให้บริการสำหรับปี 2568 จำนวน 2,429.13 ล้านบาท ปรับลดลงจำนวน 114.35 ล้านบาท หรือคิดเป็นลดลงร้อยละ 5.39 โดยมีป้จจัยสำคัญมาจาก 1.1 สถานการณ์อุทกภัยในจังหวัดสงขลา ซึ่งเป็นที่ตั้งของบริษัทและโรงงานผลิตสินค้าอาหารทะเลแ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ผลการดำเนินงาน สำหรับงวดปีสิ้นสุดวันที่ 31 ธันวาคม 2568 บริษัทฯ และบริษัทย่อยมีผลขาดทุนสุทธิจำนวน 428.01 ล้านบาท เพิ่มขึ้นเมื่อเปรียบเทียบกับปีก่อนซึ่งมีขาดทุนสุทธิจำนวน 130.63 ล้านบาท คิดเป็นการเปลี่ยนแปลงขาดทุนสุทธิเพิ่มขึ้น ร้อยละ 227.65 จึงขอชี้แจงถึงสาเหตุการเปลี่ยนแปลงของผลการดำเนินงานของบริษัทฯ และบริษัทย่อย ดังนี้ 1. รายได้จากการขายและการให้บริการสำหรับปี 2568 จำนวน 2,429.13 ล้านบาท ปรับลดลงจำนวน 114.35 ล้านบาท หรือคิดเป็นลดลงร้อยละ 5.39 โดยมีป้จจัยสำคัญมาจาก 1.1 สถานการณ์อุทกภัยในจังหวัดสงขลา ซึ่งเป็นที่ตั้งของบริษัทและโรงงานผลิตสินค้าอาหารทะเลแช่แข็ง และผลไม้แช่แข็ง สถานการณ์ดังกล่าวที่เกิดขึ้นในช่วงปลายปีได้ส่งผลต่อการส่งมอบสินค้าให้กับลูกค้าอย่างมีนัยสำคัญ และ

  `MDA_CHOTI_FY2025` · `p004` · SHA 999ac383ae4c
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -428 ลบ. จาก -131 ลบ.; MD&A ระบุว่า ซึ่งอาจจะต้องใช้เวลาอีกระยะหนึ่ง 3. จากสาเหตุที่ได้กล่าวมาในข้อ 1 และข้อ 2 ส่งผลให้บริษัทมีอัตราขาดทุนขั้นต้นจากการดำเนินธุรกิจ ในปี 2568 เพิ่มขึ้นคิดเป็นร้อยละ 576.89 เมื่อเทียบกับปี 2567 4. ต้นทุนในการจัดจำหน่ายลดลงร้อยละ 2.46 สำหรับปี 2568 ซึ่งใกล้เคียงกับงวดเดียวกันของปีก่อน
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ซึ่งอาจจะต้องใช้เวลาอีกระยะหนึ่ง 3. จากสาเหตุที่ได้กล่าวมาในข้อ 1 และข้อ 2 ส่งผลให้บริษัทมีอัตราขาดทุนขั้นต้นจากการดำเนินธุรกิจ ในปี 2568 เพิ่มขึ้นคิดเป็นร้อยละ 576.89 เมื่อเทียบกับปี 2567 4. ต้นทุนในการจัดจำหน่ายลดลงร้อยละ 2.46 สำหรับปี 2568 ซึ่งใกล้เคียงกับงวดเดียวกันของปีก่อน

  `MDA_CHOTI_FY2025` · `p007` · SHA 27a4d5f163d7
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -428 ลบ. จาก -131 ลบ.; MD&A ระบุว่า ส่งผลให้รายได้ของบริษัทลดลงจากแผนที่คาดไว้เมื่อเทียบกับช่วงเวลาเดียวกันของปีก่อน 1.2 นอกจากนี้การแข็งค่าของเงินบาทยังส่งผลกระทบโดยตรงต่อรายได้ที่มาจากตลาดต่างประเทศ ซึ่งเป็น รายได้หลักของบริษัทฯ แม้ว่าระดับคำสั่งซื้อจะยังอยู่ในระดับที่ใกล้เคียงกับช่วงเดียวกันของปีก่อนก็ตาม 2. ต้นทุนขายและการให้บริการสำหรับปี 2568 จำนวน 2,717.41 ล้านบาท เพิ่มขึ้น 234.58 ล้านบาท หรือ คิดเป็นเพิ่มขึ้นร้อยละ 9.45 จากช่วงเดียวกันของปีก่อน สาเหตุหลักมาจากผลกระทบของเหตุการณ์อุทกภัยที่ส่งผลให้คุณภาพ สินค้าแช่แข็ง (บางส่วน) ได้รับความเสียหายในเรื่องของอุณหภูมิที่ไม่เป็นไปตามมาตรฐ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ส่งผลให้รายได้ของบริษัทลดลงจากแผนที่คาดไว้เมื่อเทียบกับช่วงเวลาเดียวกันของปีก่อน 1.2 นอกจากนี้การแข็งค่าของเงินบาทยังส่งผลกระทบโดยตรงต่อรายได้ที่มาจากตลาดต่างประเทศ ซึ่งเป็น รายได้หลักของบริษัทฯ แม้ว่าระดับคำสั่งซื้อจะยังอยู่ในระดับที่ใกล้เคียงกับช่วงเดียวกันของปีก่อนก็ตาม 2. ต้นทุนขายและการให้บริการสำหรับปี 2568 จำนวน 2,717.41 ล้านบาท เพิ่มขึ้น 234.58 ล้านบาท หรือ คิดเป็นเพิ่มขึ้นร้อยละ 9.45 จากช่วงเดียวกันของปีก่อน สาเหตุหลักมาจากผลกระทบของเหตุการณ์อุทกภัยที่ส่งผลให้คุณภาพ สินค้าแช่แข็ง (บางส่วน) ได้รับความเสียหายในเรื่องของอุณหภูมิที่ไม่เป็นไปตามมาตรฐานที่กำหนด เนื่องจากน้ำได้เข้าท่วม พื้นที่ของบริษัทฯ เป็นเหตุจำเป็นให้ต้องหยุดจ่ายกระแสไฟฟ้าในพื้นที่บริษัทฯ เพื่อความปลอดภัย ส่งผลกระทบต่ออ

  `MDA_CHOTI_FY2025` · `p005` · SHA 66e8286b6cb6
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -428 ลบ. จาก -131 ลบ.; MD&A ระบุว่า เนื่องจากบริษัทฯ สามารถบริหารจัดการต้นทุนในการจัดจำหน่ายได้มีประสิทธิภาพมากขึ้น 5. ค่าใช้จ่ายในการบริหารเพิ่มขึ้นร้อยละ 10.79 สำหรับปี 2568 เมื่อเทียบกับปี 2567 เนื่องจากเหตุการณ์
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > เนื่องจากบริษัทฯ สามารถบริหารจัดการต้นทุนในการจัดจำหน่ายได้มีประสิทธิภาพมากขึ้น 5. ค่าใช้จ่ายในการบริหารเพิ่มขึ้นร้อยละ 10.79 สำหรับปี 2568 เมื่อเทียบกับปี 2567 เนื่องจากเหตุการณ์

  `MDA_CHOTI_FY2025` · `p008` · SHA c5349fec7437
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_CHOTI_FY2025`

#### ทะเบียนข้อสรุป — F2

| ส่วน | ประเภท | ข้อสรุป | รหัสแหล่งข้อมูล |
|---|---|---|---|
| headline | ข้ออนุมานนักวิเคราะห์ | ราคาปรับดีขึ้นแม้ผลประกอบการ FY2025 ยังถูกกดดัน | FY_PANEL, F2_E1 |
| earnings_fact | ข้อเท็จจริงจากการคำนวณ | FY2025 RFO -3.3%; สถานะ NPAT ส่วนผู้ถือหุ้น: profit_decreased | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | TU เป็นตัวหลักของการลดลงทั้งรายได้และกำไรรวม | FY_PANEL |
| why | ข้ออนุมานนักวิเคราะห์ | product mix ส่งออก ต้นทุนทูน่า และค่าเงินยังเป็นตัวแปรหลัก | FY_PANEL, F2_E1 |
| why | ข้ออนุมานนักวิเคราะห์ | ราคาบวกในวงกว้างสะท้อนความคาดหวังการฟื้น มากกว่าผลประกอบการ FY2025 ที่เกิดขึ้นแล้ว | FY_PANEL, F2_E1, SET_PUBLIC_EOD |
| causal_chain | ข้ออนุมานนักวิเคราะห์ | ห่วงโซ่เหตุ: ปริมาณส่งออก → Mix / ค่าเงิน → Gross margin → NPAT → Re-rating | F2_E1 |
| roles | ข้ออนุมานนักวิเคราะห์ | บทบาท: ผู้นำและกำหนดทิศ — TU; ตัวเทียบ — CFRESH | FY_PANEL, F2_E1 |
| valuation | ข้ออนุมานนักวิเคราะห์ | P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 10.9x ครอบคลุม 4/5 บริษัท และ 99.2% ของ market cap ที่มีข้อมูล. ส่วนลดสะท้อนความไม่แน่นอนด้านส่งออก วัตถุดิบ และ margin | SET_PUBLIC_EOD, F2_E1 |
| trigger | ประเด็นที่ต้องพิสูจน์ | ต้นทุนทูน่าและค่าระวางผ่อนคลาย | F2_E1 |
| trigger | ประเด็นที่ต้องพิสูจน์ | ปริมาณส่งออกและสัดส่วนแบรนด์ดีขึ้น | F2_E1 |
| trigger | ประเด็นที่ต้องพิสูจน์ | ค่าเงินเอื้อต่อผู้ส่งออก | F2_E1 |
| risk | ประเด็นที่ต้องพิสูจน์ | วัตถุดิบผันผวน | F2_E1 |
| risk | ประเด็นที่ต้องพิสูจน์ | อุปสงค์ต่างประเทศอ่อนตัว | F2_E1 |
| risk | ประเด็นที่ต้องพิสูจน์ | เงินบาทแข็งค่า | F2_E1 |
| must_prove | ประเด็นที่ต้องพิสูจน์ | 6M26 ต้องต่อยอดยอดขายที่เริ่มทรงตัวใน 4Q25 ไปสู่การฟื้นของ gross margin และกำไรส่วนผู้ถือหุ้น โดยยอดขาย FY2025 ยังลดลง | F2_E1 |

#### ทะเบียนหลักฐาน — F2

- **`FY_PANEL`** · _ข้อเท็จจริงจากการคำนวณ_ — Audited FY2024-25 company panel
  - RFO / NPAT-to-owners / independent panel membership; QA 43 pass / 0 fail
  - บทบาท: historical fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_company_fy2024_2025_audited_2026-08-07.csv`
  - SHA-256: `e5e04dbc40ffcc79fed58545a93dc4549c29cdaecf260bea73711bc6d0720481`
- **`SET_PUBLIC_EOD`** · _ข้อเท็จจริงจากการคำนวณ_ — SET public Company Highlights — EOD 2026-08-07
  - Adjusted YTD; unadjusted price, market cap and valuation; factsheet-surface cross-check
  - บทบาท: current market fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_set_public_surface_reconciliation_2026-08-07.csv`
  - SHA-256: `544c1f29fe2d409ee398822ac2bf32b769081718962ae2d1138985b0146b9530`
- **`SET_COMPANY_PROFILE`** · _ข้อเท็จจริง_ — SET company profiles — English and Thai
  - Official company names and business descriptions refreshed and validated for the 118-company perimeter from the public SET profile API
  - บทบาท: company business profile
  - URL: <https://www.set.or.th/th/market/product/stock/overview>
- **`COMPANY_REPORTS`** · _ข้ออนุมานนักวิเคราะห์_ — Company report synthesis corpus
  - Annual-only draft synthesis; reconciled to the ticker FY2025 MD&A where available
  - บทบาท: secondary synthesis; not management attribution
  - พาธ: `data/company-reports.json`
  - SHA-256: `c1a2bc40cbe21a2058aa596c362e4d47ad117360831b847de78ec414831fd2d2`
- **`MDA_TU_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — TU FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/TU/MDA_TU_2025FY_T.md`
  - SHA-256: `92c90a25d2a2fbf7597229293ff5cdde7728b33527e46a286f9f1ad7a50f67de`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/0450NWS180220261829424330T.pdf>
- **`MDA_ASIAN_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — ASIAN FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/ASIAN/MDA_ASIAN_2025FY_T.md`
  - SHA-256: `bc1ad53f0a312eda7fe8e2f3990e9466c54dd022d06f94f1bf5e2fdcf2fc8f37`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/0405NWS200220261716446820T.pdf>
- **`MDA_TC_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — TC FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/TC/MDA_TC_2025FY_T.md`
  - SHA-256: `15c9f07c42dd92aeabd9642967b08997e8eeb56e93a38c7fcd636f908d5ed4f6`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/0178NWS240220261714584950T.pdf>
- **`MDA_CFRESH_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — CFRESH FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/CFRESH/MDA_CFRESH_2025FY_T.md`
  - SHA-256: `d3cb51fb4311dafb393c9ec20e510b07753c4863f021cc4a4e2cc60c993b0f30`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/0359NWS260220261914045980T.pdf>
- **`MDA_CHOTI_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — CHOTI FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/CHOTI/MDA_CHOTI_2025FY_T.md`
  - SHA-256: `45b79661c7ee05a51cef2f3f0f16c13228cf3efc8b289c47a5d074a7255cb3de`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202603/0300NWS020320260721181760T.pdf>
- **`F2_E1`** · _ฝ่ายจัดการ_ — TU FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/TU/MDA_TU_2025FY_E.md`
  - SHA-256: `e6259e403f566de07daecdc2242759024c81ce077e865c2c25b4089d08171b52`
- **`F2_FACTSHEET`** · _ข้อเท็จจริงจากการคำนวณ_ — SET Factsheet — TU
  - Live leader cross-check
  - บทบาท: presentation-surface check
  - URL: <https://www.set.or.th/th/market/product/stock/quote/tu/factsheet>

### F3 · อาหารสัตว์เลี้ยง — รายได้เชิงโครงสร้างยังโต แต่การแปลงเป็นกำไรอ่อนลง

`ราคานำพื้นฐาน` · 7.6% M-cap · THB 61.6bn · 2 บริษัท

| ตัวชี้วัด | RFO | NPAT | ราคา | P/E |
|---|---|---|---|---|
| ช่วง | FY2025 YoY | ส่วนผู้ถือหุ้น FY2025 YoY | ราคา YTD ปรับแล้ว | เฉพาะบริษัทที่มีกำไร |
| ค่า | +2.6% | -19.2% | +14.0% | 15.7x |
| จำนวน | THB 25.2bn FY2025 | THB 3.7bn FY2025 | ณ 7 ส.ค. 2569 | ค่าเฉลี่ยรวม |
| ครอบคลุม | 2/2 | 2/2 | 2/2 • 100% M-cap | 2/2 • 100% M-cap |

**ข้อเท็จจริงที่สังเกตได้** — FY2025: RFO +2.6% • NPAT -19.2% • ราคา YTD +14.0% • P/E 15.7x • ครอบคลุม RFO 2/2 • NPAT 2/2

#### เหตุผลที่เปลี่ยน

1. _ข้อเท็จจริงจากการคำนวณ_ · คำสั่งซื้อ — ITC สร้างการเติบโตของ RFO ส่วนใหญ่ แต่เป็นตัวฉุดกำไรมากที่สุด
2. _คำอธิบายฝ่ายจัดการ_ · Product mix — premium mix และปริมาณขายที่เพิ่มถูกหักล้างด้วยเงินบาทแข็ง ต้นทุนวัตถุดิบ และต้นทุน transformation
3. _ประเด็นที่ต้องพิสูจน์_ · Utilization — utilisation ของกำลังผลิตใหม่เป็นประเด็นที่ต้องพิสูจน์ใน 6M26 ไม่ใช่คำอธิบายเหตุของ FY2025 ที่ยืนยันแล้ว

#### ห่วงโซ่เหตุและผล

**คำสั่งซื้อ** → **Product mix** → **Utilization** → **Margin** (14.7% -4.0 ppt YoY) → **NPAT** (-19.2% THB 3.7bn FY2025)

#### บทบาทในกลุ่ม

| บทบาท | Ticker | ค่า | ที่มาของค่า |
|---|---|---|---|
| ผู้นำและตัวขับเคลื่อน | ITC | 86% | สัดส่วน Market Cap ในกลุ่ม |
| ตัวเทียบ | AAI | 14.5x | P/E · YTD +0.5% |

#### มูลค่า

**ตลาดกำลังจ่ายเพื่อ — ข้ออนุมาน** — P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 15.7x ครอบคลุม 2/2 บริษัท และ 100.0% ของ market cap ที่มีข้อมูล. premium สะท้อนการเติบโตและ margin ของ pet food แต่ต้องพิสูจน์ execution

| Trigger | Risk |
|---|---|
| สัดส่วนสินค้าพรีเมียมดีขึ้น | การกระจุกตัวของลูกค้า |
| กำลังผลิตใหม่เข้าสู่ utilization ที่มีประสิทธิภาพ | ต้นทุนช่วง ramp-up |
| คำสั่งซื้อกระจายตัวในหลายลูกค้า | ค่าเงินและต้นทุนทูน่า |

**6M26 ต้องพิสูจน์** — 6M26 ต้องเห็นทั้งปริมาณและ margin ฟื้น ไม่ใช่เพียงยอดขายเพิ่ม

#### วิเคราะห์รายบริษัท — F3 อาหารสัตว์เลี้ยง

_ทุกบริษัทใน perimeter ของ Segment ที่สอบทาน_

| Ticker | บทบาท | M-cap | RFO YoY | NPAT YoY | ราคา YTD | P/E | Margin |
|---|---|---|---|---|---|---|---|
| ITC | ผู้นำและตัวขับเคลื่อน | THB 52.8bn | +2.8% | -17.2% | +16.6% | 15.9x | 16.3% |
| AAI | ตัวเทียบ | THB 8.8bn | +2.2% | -26.2% | +0.5% | 14.5x | 10.6% |

##### ITC — ผู้นำและตัวขับเคลื่อน · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ไอ-เทล คอร์ปอเรชั่น จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — รับจ้างผลิตและจัดจำหน่ายอาหารสัตว์เลี้ยง

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 52.8bn | 17.60 | +16.6% | 15.9x | 16.3% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 17.7bn → FY2025 THB 18.2bn · +494m · +2.8%

- รายได้ได้แรงหนุนจากปริมาณและ สัดส่วนสินค้าพรีเมียม ที่ดีขึ้น แต่เงินบาทแข็งกดรายได้ส่งออกเมื่อแปลงเป็นบาท
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ผลการดำเนินงานไตรมาส 4/2568 รายได้ในไตรมาส 4/2568 บริษัทมีรายได้จากการขาย 4,780 ล้านบาท เพิ่มขึ้น 1.2% QoQ และ 1.8% YoY โดยการเติบโตทั้งรายไตรมาสและรายปี ได้รับแรงหนุนจากความต้องการที่เพิ่มขึ้นของลูกค้ารายสำคัญในสหรัฐอเมริกา รวมถึงบริษัทอาหารสัตว์เลี้ยงระดับโลก ขณะที่ยอดขายในยุโรปยังคง เป็นไปตามแผนที่วางไว้ทั้งนี้ผลการดำเนินงานโดยรวมได้รับการสนับสนุนจากปริมาณขายสินค้าที่ปรับเพิ่มขึ้น 2.8% YoY และเพิ่มขึ้น 1.2% QoQ แม้ค่าเงินบาทที่แข็งค่าตลอดไตรมาสจะกดดันอัตราการเติบโตของยอดขายเมื่อคิดเป็นสกุลบาท แต่ยอดขายในสกุลดอลลาร์สหรัฐยังคงขยายตัวได้

  `MDA_ITC_FY2025` · `p032` · SHA f566cd3ba81d
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 3.6bn → FY2025 THB 3.0bn · −619m · -17.2%

- กำไรลดลงสวนรายได้ เพราะแรงกดดันวัตถุดิบ FX และต้นทุน การปรับโครงสร้าง/เริ่มเดินเครื่อง ทำให้การแปลงรายได้เป็นกำไรส่วนผู้ถือหุ้นอ่อนลง
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > อย่างแข็งแกร่ง อัตรากำไรขั้นต้นในไตรมาส 4/2568 อยู่ที่ 25.8% เพิ่มขึ้น 0.4 จุด QoQ และ 0.3 จุด YoY จากระดับ 25.4% ในไตรมาส 3/2568 และ 25.5% ใน ไตรมาส 4/2567 โดยมีป้จจัยสนับสนุนจากปริมาณการขายที่เพิ่มขึ้น ขณะที่สัดส่วนผลิตภัณฑ์พรีเมียมยังอยู่ในระดับสูงที่ 53.0% ของยอดขาย แม้ว่า จะต่ำกว่าระดับ 55.1% ในไตรมาส 3/2568 และ 54.7% ในไตรมาส 4/2567 เล็กน้อย 1 กำไรสุทธิปรับปรุง (Adjusted Net Profit) และอัตรากำไรสุทธิปรับปรุง (Adjusted Net Profit Margin) คำนวณโดยไม่รวมค่าใช้จ่ายที่เกี่ยวข้องกับโครงการ Transformation

  `MDA_ITC_FY2025` · `p033` · SHA a6d979b0b036
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_ITC_FY2025`

##### AAI — ตัวเทียบ · ติดตาม

**บริษัท เอเชี่ยน อะไลอันซ์ อินเตอร์เนชั่นแนล จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ธุรกิจรับจ้างผลิตและจำหน่ายอาหารสัตว์เลี้ยง (Pet food) อาหารพร้อมทานบรรจุภาชนะปิดผนึก (Human food) และผลิตภัณฑ์ผลพลอยได้จากการแปรรูปปลาทูน่า

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 8.8bn | 4.14 | +0.5% | 14.5x | 10.6% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 20 · NPAT 20 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 4

**RFO — เพราะอะไร** — FY2024 THB 6.8bn → FY2025 THB 7.0bn · +151m · +2.2%

- RFO ปี 2568 อยู่ที่ 7,000 ลบ. เพิ่ม 2.2% YoY; MD&A ระบุว่า บทสรุปผู้บริหาร สำหรับไตรมาสที่ 4 ปี 2568 • รายได้จากการขายและบริการ: กลุ่มบริษัทฯ บันทึกรายได้จำนวน 1,763 ล้านบาท ทรงตัวในระดับใกล้เคียงกับช่วงเดียวกันของปีก่อนแต่เติบโตขึ้นร้อย 6.7 จากไตรมาสก่อนสาเหตุจากการลดลงจากรายได้ของกลุ่มอาหารพร้อมทานในขณะที่รายได้จากอาหารสัตว์เลี้ยงยังคงเติบโตได้ ในขณะที่ปริมาณขาย รวม (Sales Volume) เพิ่มขึ้นเป็น 12,543 ตัน หรือเพิ่มขึ้นร้อยละ 9.5 จากช่วงเดียวกันของปีก่อน สะท้อนถึงอุปสงค์ที่ยังขยายตัวอย่างต่อเนื่องแต่เนื่องจาก บริษัทประกอบธุรกิจเพื่อการส่งออกเป็นหลักและรับรายได้ในรูปแบบของค่าเงินเหรียญสหรัฐฯ จึงได้รับผลกระทบจากก
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > บทสรุปผู้บริหาร สำหรับไตรมาสที่ 4 ปี 2568 • รายได้จากการขายและบริการ: กลุ่มบริษัทฯ บันทึกรายได้จำนวน 1,763 ล้านบาท ทรงตัวในระดับใกล้เคียงกับช่วงเดียวกันของปีก่อนแต่เติบโตขึ้นร้อย 6.7 จากไตรมาสก่อนสาเหตุจากการลดลงจากรายได้ของกลุ่มอาหารพร้อมทานในขณะที่รายได้จากอาหารสัตว์เลี้ยงยังคงเติบโตได้ ในขณะที่ปริมาณขาย รวม (Sales Volume) เพิ่มขึ้นเป็น 12,543 ตัน หรือเพิ่มขึ้นร้อยละ 9.5 จากช่วงเดียวกันของปีก่อน สะท้อนถึงอุปสงค์ที่ยังขยายตัวอย่างต่อเนื่องแต่เนื่องจาก บริษัทประกอบธุรกิจเพื่อการส่งออกเป็นหลักและรับรายได้ในรูปแบบของค่าเงินเหรียญสหรัฐฯ จึงได้รับผลกระทบจากการอ่อนค่าเงินเหรียญสหรัฐฯเมื่อ

  `MDA_AAI_FY2025` · `p005` · SHA 5fbb6d8f8632
  </details>
- RFO ปี 2568 อยู่ที่ 7,000 ลบ. เพิ่ม 2.2% YoY; MD&A ระบุว่า มาสก่อนหน้า ทั้งปริมาณขายและรายได้มีการปรับตัวดีขึ้นตามลำดับ สำหรับรายได้จากการรับจ้างผลิต ในไตรมาส 4 ปี 2568 อยู่ที่ 1,546 ล้านบาท เพิ่มขึ้นร้อยละ 3.5 จากช่วงเดียวกันของปีก่อน สอดคล้องกับปริมาณการ ขายที่เพิ่มขึ้นร้อยละ 13.5 โดยตลาดหลักอย่างสหรัฐอเมริกาและยุโรปยังคงเป็นฐานรายได้สำคัญ แม้ว่าจะได้รับแรงกดดันจากอัตราแลกเปลี่ยนที่ทำให้การรับรู้รายได้ ในรูปเงินบาทไม่สูงเท่าที่ควร แต่คำสั่งซื้อจากลูกค้าเริ่มกลับมาฟื้นตัวอย่างชัดเจนหลังมีความชัดเจนเรื่องนโยบายภาษีตอบโต้ของสหรัฐอเมริกา ในส่วนของผลิตภัณฑ์อาหารสัตว์เลี้ยงภายใต้แบรนด์ของบริษัทฯ มีผลการดำเนินงานที่โ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > มาสก่อนหน้า ทั้งปริมาณขายและรายได้มีการปรับตัวดีขึ้นตามลำดับ สำหรับรายได้จากการรับจ้างผลิต ในไตรมาส 4 ปี 2568 อยู่ที่ 1,546 ล้านบาท เพิ่มขึ้นร้อยละ 3.5 จากช่วงเดียวกันของปีก่อน สอดคล้องกับปริมาณการ ขายที่เพิ่มขึ้นร้อยละ 13.5 โดยตลาดหลักอย่างสหรัฐอเมริกาและยุโรปยังคงเป็นฐานรายได้สำคัญ แม้ว่าจะได้รับแรงกดดันจากอัตราแลกเปลี่ยนที่ทำให้การรับรู้รายได้ ในรูปเงินบาทไม่สูงเท่าที่ควร แต่คำสั่งซื้อจากลูกค้าเริ่มกลับมาฟื้นตัวอย่างชัดเจนหลังมีความชัดเจนเรื่องนโยบายภาษีตอบโต้ของสหรัฐอเมริกา ในส่วนของผลิตภัณฑ์อาหารสัตว์เลี้ยงภายใต้แบรนด์ของบริษัทฯ มีผลการดำเนินงานที่โดดเด่น โดยปริมาณการขายเพิ่มขึ้นอย่างมีนัยสำคัญถึงร้อยละ 71.3 มาอยู่ที่ 1,004 ตัน และสร้างรายได้ประมาณ 48 ล้านบาท เพิ่มขึ้นร้อยละ 28.6 จากช่ว

  `MDA_AAI_FY2025` · `p046` · SHA b740b441b802
  </details>
- RFO ปี 2568 อยู่ที่ 7,000 ลบ. เพิ่ม 2.2% YoY; MD&A ระบุว่า รายได้จากการขายและบริการ ในปี 2568 กลุ่มบริษัทฯ มีรายได้จากการขายและบริการรวมทั้งสิ้น 7,000 ล้านบาท ปรับตัวเพิ่มขึ้นร้อยละ 2.2 เมื่อเทียบกับ 6,849 ล้านบาท ในปี 2567 โดยปัจจัยขับเคลื่อนหลักมาจากการเติบโตของปริมาณการขายที่เพิ่มขึ้นถึงร้อยละ 12.3 มาอยู่ที่ 48,701 ตัน ซึ่งเป็นการเติบโตในกลุ่มธุรกิจอาหารสัตว์เลี้ยงเป็น สำคัญ อย่างไรก็ตาม อัตราการเติบโตของรายได้ต่ำกว่าการเติบโตของปริมาณขายอย่างมีนัยสำคัญ เนื่องจากได้รับผลกระทบจากการอ่อนค่าของดอลลาร์สหรัฐฯเมื่อ เทียบกับเงินบาทตลอดทั้งปีส่งผลให้รายได้ที่ได้รับจากการส่งออกเมื่อแปลงค่าเป็นเงินบาทลดลง ประกอบกับผลกร
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้จากการขายและบริการ ในปี 2568 กลุ่มบริษัทฯ มีรายได้จากการขายและบริการรวมทั้งสิ้น 7,000 ล้านบาท ปรับตัวเพิ่มขึ้นร้อยละ 2.2 เมื่อเทียบกับ 6,849 ล้านบาท ในปี 2567 โดยปัจจัยขับเคลื่อนหลักมาจากการเติบโตของปริมาณการขายที่เพิ่มขึ้นถึงร้อยละ 12.3 มาอยู่ที่ 48,701 ตัน ซึ่งเป็นการเติบโตในกลุ่มธุรกิจอาหารสัตว์เลี้ยงเป็น สำคัญ อย่างไรก็ตาม อัตราการเติบโตของรายได้ต่ำกว่าการเติบโตของปริมาณขายอย่างมีนัยสำคัญ เนื่องจากได้รับผลกระทบจากการอ่อนค่าของดอลลาร์สหรัฐฯเมื่อ เทียบกับเงินบาทตลอดทั้งปีส่งผลให้รายได้ที่ได้รับจากการส่งออกเมื่อแปลงค่าเป็นเงินบาทลดลง ประกอบกับผลกระทบจากมาตรการภาษีตอบโต้ (Reciprocal

  `MDA_AAI_FY2025` · `p066` · SHA dac25227cdfa
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 1.0bn → FY2025 THB 741m · −263m · -26.2%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 741 ลบ. ลด 26.2% YoY; MD&A ระบุว่า สหรัฐอเมริกา แคนาดา และยุโรป • กำไรขั้นต้น: สำหรับปี 2568 อยู่ที่ 1,056 ล้านบาท ปรับตัวลดลงร้อยละ 24.5 เมื่อเทียบกับปี 2567 ส่งผลให้อัตรากำไรขั้นต้น ในปีนี้อยู่ที่ร้อยละ 15.1 ชะลอตัวลงจากร้อยละ 20.4 ในปีก่อนหน้า สาเหตุหลักของการปรับลดลงในปีนี้ยังคงถูกกดดันด้วยเรื่องค่าเงินสหรัฐที่อ่อนค่าเมื่อเทียบกับเงินบาท • กำไรสุทธิ: มีจำนวน 741 ล้านบาท คิดเป็นอัตรากำไรสุทธิร้อยละ 10.6 และมีกำไรต่อหุ้นอยู่ที่ 0.35 บาทต่อหุ้น เมื่อเปรียบเทียบกับปี 2567 กำไรสุทธิ ปรับตัวลดลงร้อยละ 26.2 จาก 1,003 ล้านบาท และกำไรต่อหุ้นที่ลดลงจาก 0.47 บาท โดยปัจจัยกดดันหลักมาจากการชะลอตัว
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > สหรัฐอเมริกา แคนาดา และยุโรป • กำไรขั้นต้น: สำหรับปี 2568 อยู่ที่ 1,056 ล้านบาท ปรับตัวลดลงร้อยละ 24.5 เมื่อเทียบกับปี 2567 ส่งผลให้อัตรากำไรขั้นต้น ในปีนี้อยู่ที่ร้อยละ 15.1 ชะลอตัวลงจากร้อยละ 20.4 ในปีก่อนหน้า สาเหตุหลักของการปรับลดลงในปีนี้ยังคงถูกกดดันด้วยเรื่องค่าเงินสหรัฐที่อ่อนค่าเมื่อเทียบกับเงินบาท • กำไรสุทธิ: มีจำนวน 741 ล้านบาท คิดเป็นอัตรากำไรสุทธิร้อยละ 10.6 และมีกำไรต่อหุ้นอยู่ที่ 0.35 บาทต่อหุ้น เมื่อเปรียบเทียบกับปี 2567 กำไรสุทธิ ปรับตัวลดลงร้อยละ 26.2 จาก 1,003 ล้านบาท และกำไรต่อหุ้นที่ลดลงจาก 0.47 บาท โดยปัจจัยกดดันหลักมาจากการชะลอตัวของอัตรากำไรขั้นต้นที่ ได้รับผลกระทบจากความผันผวนของค่าเงินบาทและต้นทุนวัตถุดิบ แม้ว่าบริษัทฯ จะสามารถเพิ่มประสิทธิภาพในการบริหารจัดการค่าใช

  `MDA_AAI_FY2025` · `p009` · SHA 3888b09124be
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 741 ลบ. ลด 26.2% YoY; MD&A ระบุว่า มาสก่อนหน้าตามปริมาณการผลิตที่ปรับตัวสูงขึ้น • กำไรสุทธิ: มีมูลค่า 110 ล้านบาท ลดลงร้อยละ 36.4 เมื่อเทียบกับปีก่อน และลดลงร้อยละ 38.2 จากไตรมาสก่อนหน้า สาเหตุหลักมาจากการลดลงของ ความสามารถในการทำกำไรขั้นต้น ประกอบกับในไตรมาสนี้กลุ่มบริษัทฯ รับรู้ผลขาดทุนจากอัตราแลกเปลี่ยนจำนวน 14 ล้านบาท จากที่มีกำไรจากอัตรา แลกเปลี่ยน 8.0 ล้านบาท ในไตรมาสก่อนหน้า ส่งผลให้อัตรากำไรสุทธิลดลงเหลือร้อยละ 6.2 เทียบกับร้อยละ 9.7 ในปีก่อน และร้อยละ 10.8 ในไตรมาส ก่อนหน้า คิดเป็นกำไรต่อหุ้นที่ 0.05 บาทจาก 0.08 ในปีก่อนและ 0.08 จากไตรมาสก่อนหน้า
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > มาสก่อนหน้าตามปริมาณการผลิตที่ปรับตัวสูงขึ้น • กำไรสุทธิ: มีมูลค่า 110 ล้านบาท ลดลงร้อยละ 36.4 เมื่อเทียบกับปีก่อน และลดลงร้อยละ 38.2 จากไตรมาสก่อนหน้า สาเหตุหลักมาจากการลดลงของ ความสามารถในการทำกำไรขั้นต้น ประกอบกับในไตรมาสนี้กลุ่มบริษัทฯ รับรู้ผลขาดทุนจากอัตราแลกเปลี่ยนจำนวน 14 ล้านบาท จากที่มีกำไรจากอัตรา แลกเปลี่ยน 8.0 ล้านบาท ในไตรมาสก่อนหน้า ส่งผลให้อัตรากำไรสุทธิลดลงเหลือร้อยละ 6.2 เทียบกับร้อยละ 9.7 ในปีก่อน และร้อยละ 10.8 ในไตรมาส ก่อนหน้า คิดเป็นกำไรต่อหุ้นที่ 0.05 บาทจาก 0.08 ในปีก่อนและ 0.08 จากไตรมาสก่อนหน้า

  `MDA_AAI_FY2025` · `p007` · SHA 85b5b31388dc
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 741 ลบ. ลด 26.2% YoY; MD&A ระบุว่า กำไรสุทธิและกำไรต่อหุ้น จากแรงกดดันของอัตรากำไรขั้นต้นที่ชะลอตัวจากการอ่อนค่าเงินสหรัฐฯเมื่อเทียบกับเงินบาทเป็นสำคัญและผลขาดทุนจากอัตราแลกเปลี่ยน ส่งผลให้ กำไรสุทธิในไตรมาส 4 ปี 2568 มีมูลค่า 110 ล้านบาท ปรับตัวลดลง ร้อยละ 36.4 เมื่อเทียบกับ 173 ล้านบาท ในช่วงเดียวกันของปีก่อนหน้า และลดลงร้อยละ 38.2 จาก 178 ล้านบาท ในไตรมาสก่อนหน้า ทำให้อัตรากำไรสุทธิอยู่ที่ร้อยละ 6.2 (ลดลงจากร้อยละ 9.7 ในปีก่อนและร้อยละ 10.8 จากไตรมาสก่อนหน้า) โดยมีกำไรต่อ หุ้นขั้นพื้นฐาน (EPS) อยู่ที่ 0.05 บาทต่อหุ้น
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไรสุทธิและกำไรต่อหุ้น จากแรงกดดันของอัตรากำไรขั้นต้นที่ชะลอตัวจากการอ่อนค่าเงินสหรัฐฯเมื่อเทียบกับเงินบาทเป็นสำคัญและผลขาดทุนจากอัตราแลกเปลี่ยน ส่งผลให้ กำไรสุทธิในไตรมาส 4 ปี 2568 มีมูลค่า 110 ล้านบาท ปรับตัวลดลง ร้อยละ 36.4 เมื่อเทียบกับ 173 ล้านบาท ในช่วงเดียวกันของปีก่อนหน้า และลดลงร้อยละ 38.2 จาก 178 ล้านบาท ในไตรมาสก่อนหน้า ทำให้อัตรากำไรสุทธิอยู่ที่ร้อยละ 6.2 (ลดลงจากร้อยละ 9.7 ในปีก่อนและร้อยละ 10.8 จากไตรมาสก่อนหน้า) โดยมีกำไรต่อ หุ้นขั้นพื้นฐาน (EPS) อยู่ที่ 0.05 บาทต่อหุ้น

  `MDA_AAI_FY2025` · `p058` · SHA 3698bb81e9f6
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 741 ลบ. ลด 26.2% YoY; MD&A ระบุว่า กำไรขั้นต้น ในไตรมาส 4 ปี 2568 กลุ่มบริษัทฯ มีกำไรขั้นต้นจำนวน 210 ล้านบาท ปรับตัวลดลงร้อยละ 28.0 เมื่อเทียบกับช่วงเดียวกันของปีก่อนหน้าที่มีจำนวน 292 ล้านบาท และลดลงร้อยละ 8.2 เมื่อเทียบกับไตรมาสก่อน ส่งผลให้อัตรากำไรขั้นต้นในไตรมาสนี้ชะลอตัวลงมาอยู่ที่ระดับร้อยละ 11.9 ลดลงจากร้อยละ 16.5 และ ร้อยละ 13.9 ตามลำดับ การชะลอตัวของอัตรากำไรขั้นต้นสะท้อนถึงสัดส่วนต้นทุนขายและบริการที่ปรับตัวสูงขึ้นเป็นร้อยละ 88.1 ของรายได้รวม เทียบกับร้อยละ 83.5 ในปีก่อนและร้อยละ 86.1 ในไตรมาสก่อนหน้า โดยมีสาเหตุสำคัญมาจากผลกระทบอัตราแลกเปลี่ยน ซึ่งแม้ว่าปริมาณการขายรวมจะเติบโ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไรขั้นต้น ในไตรมาส 4 ปี 2568 กลุ่มบริษัทฯ มีกำไรขั้นต้นจำนวน 210 ล้านบาท ปรับตัวลดลงร้อยละ 28.0 เมื่อเทียบกับช่วงเดียวกันของปีก่อนหน้าที่มีจำนวน 292 ล้านบาท และลดลงร้อยละ 8.2 เมื่อเทียบกับไตรมาสก่อน ส่งผลให้อัตรากำไรขั้นต้นในไตรมาสนี้ชะลอตัวลงมาอยู่ที่ระดับร้อยละ 11.9 ลดลงจากร้อยละ 16.5 และ ร้อยละ 13.9 ตามลำดับ การชะลอตัวของอัตรากำไรขั้นต้นสะท้อนถึงสัดส่วนต้นทุนขายและบริการที่ปรับตัวสูงขึ้นเป็นร้อยละ 88.1 ของรายได้รวม เทียบกับร้อยละ 83.5 ในปีก่อนและร้อยละ 86.1 ในไตรมาสก่อนหน้า โดยมีสาเหตุสำคัญมาจากผลกระทบอัตราแลกเปลี่ยน ซึ่งแม้ว่าปริมาณการขายรวมจะเติบโตถึงร้อยละ 9.5 จาก ปีก่อนและเพิ่มขึ้นร้อยละ 4.7 จากไตรมาสก่อน มาอยู่ที่ 12,543 ตัน แต่รายได้จากการขายกลับทรงตัว แสดงให้เห็นว่ารายได้ต่อหน่วย

  `MDA_AAI_FY2025` · `p051` · SHA 3f4015f9e9ca
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายได้อื่น กลุ่มบริษัทฯ มีรายได้อื่นจำนวน 105 ล้านบาท เพิ่มขึ้นร้อยละ 36.5 จากปีก่อนหน้า ส่วนใหญ่เป็นการเพิ่มขึ้นจากการรับรู้เงินปันผลรับจากกองทุนวายุภักดิ์ และผลกำไรจากการปรับมูลค่ายุติธรรมของสินทรัพย์ทางการเงิน ในขณะที่บริษัทฯ สามารถบันทึกกำไรจากอัตราแลกเปลี่ยน จำนวน 7 ล้านบาท (พลิกฟื้นจากผล ขาดทุน 14 ล้านบาทในปีก่อนหน้า) ซึ่งเป็นผลจากการบริหารความเสี่ยงอย่างมีประสิทธิภาพจากอัตราแลกเปลี่ยนในช่วงที่ค่าเงินมีความผันผวนสูง
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้อื่น กลุ่มบริษัทฯ มีรายได้อื่นจำนวน 105 ล้านบาท เพิ่มขึ้นร้อยละ 36.5 จากปีก่อนหน้า ส่วนใหญ่เป็นการเพิ่มขึ้นจากการรับรู้เงินปันผลรับจากกองทุนวายุภักดิ์ และผลกำไรจากการปรับมูลค่ายุติธรรมของสินทรัพย์ทางการเงิน ในขณะที่บริษัทฯ สามารถบันทึกกำไรจากอัตราแลกเปลี่ยน จำนวน 7 ล้านบาท (พลิกฟื้นจากผล ขาดทุน 14 ล้านบาทในปีก่อนหน้า) ซึ่งเป็นผลจากการบริหารความเสี่ยงอย่างมีประสิทธิภาพจากอัตราแลกเปลี่ยนในช่วงที่ค่าเงินมีความผันผวนสูง

  `MDA_AAI_FY2025` · `p084` · SHA 873232a4c365
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ค่าใช้จ่ายในการดำเนินงาน บริษัทฯ มีค่าใช้จ่ายในการดำเนินงาน ซึ่งประกอบไปด้วยค่าใช้จ่ายในการดำเนินงาน รวม 383 ล้านบาท คิดเป็น ร้อยละ 5.5 ของรายได้จากการขาย ปรับตัวลดลงจากปีก่อนหน้าร้อยละ 5.9 (403 ล้านบาท) สาเหตุหลักมาจากการบริหารค่าใช้จ่ายที่มีประสิทธิภาพ รวมทั้งในปีก่อนหน้ามีการตั้งด้อยค่าเงินลงทุนของ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ค่าใช้จ่ายในการดำเนินงาน บริษัทฯ มีค่าใช้จ่ายในการดำเนินงาน ซึ่งประกอบไปด้วยค่าใช้จ่ายในการดำเนินงาน รวม 383 ล้านบาท คิดเป็น ร้อยละ 5.5 ของรายได้จากการขาย ปรับตัวลดลงจากปีก่อนหน้าร้อยละ 5.9 (403 ล้านบาท) สาเหตุหลักมาจากการบริหารค่าใช้จ่ายที่มีประสิทธิภาพ รวมทั้งในปีก่อนหน้ามีการตั้งด้อยค่าเงินลงทุนของ

  `MDA_AAI_FY2025` · `p082` · SHA d0a1a979563c
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_AAI_FY2025`

#### ทะเบียนข้อสรุป — F3

| ส่วน | ประเภท | ข้อสรุป | รหัสแหล่งข้อมูล |
|---|---|---|---|
| headline | ข้ออนุมานนักวิเคราะห์ | รายได้เชิงโครงสร้างยังโต แต่การแปลงเป็นกำไรอ่อนลง | FY_PANEL, F3_E1, F3_E2 |
| earnings_fact | ข้อเท็จจริงจากการคำนวณ | FY2025 RFO +2.6%; สถานะ NPAT ส่วนผู้ถือหุ้น: profit_decreased | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | ITC สร้างการเติบโตของ RFO ส่วนใหญ่ แต่เป็นตัวฉุดกำไรมากที่สุด | FY_PANEL |
| why | คำอธิบายฝ่ายจัดการ | premium mix และปริมาณขายที่เพิ่มถูกหักล้างด้วยเงินบาทแข็ง ต้นทุนวัตถุดิบ และต้นทุน transformation | F3_E1, F3_E2 |
| why | ประเด็นที่ต้องพิสูจน์ | utilisation ของกำลังผลิตใหม่เป็นประเด็นที่ต้องพิสูจน์ใน 6M26 ไม่ใช่คำอธิบายเหตุของ FY2025 ที่ยืนยันแล้ว | FY_PANEL, F3_E1, F3_E2, SET_PUBLIC_EOD |
| causal_chain | ข้ออนุมานนักวิเคราะห์ | ห่วงโซ่เหตุ: คำสั่งซื้อ → Product mix → Utilization → Margin → NPAT | F3_E1, F3_E2 |
| roles | ข้ออนุมานนักวิเคราะห์ | บทบาท: ผู้นำและตัวขับเคลื่อน — ITC; ตัวเทียบ — AAI | FY_PANEL, F3_E1, F3_E2 |
| valuation | ข้ออนุมานนักวิเคราะห์ | P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 15.7x ครอบคลุม 2/2 บริษัท และ 100.0% ของ market cap ที่มีข้อมูล. premium สะท้อนการเติบโตและ margin ของ pet food แต่ต้องพิสูจน์ execution | SET_PUBLIC_EOD, F3_E1, F3_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | สัดส่วนสินค้าพรีเมียมดีขึ้น | F3_E1, F3_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | กำลังผลิตใหม่เข้าสู่ utilization ที่มีประสิทธิภาพ | F3_E1, F3_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | คำสั่งซื้อกระจายตัวในหลายลูกค้า | F3_E1, F3_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | การกระจุกตัวของลูกค้า | F3_E1, F3_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | ต้นทุนช่วง ramp-up | F3_E1, F3_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | ค่าเงินและต้นทุนทูน่า | F3_E1, F3_E2 |
| must_prove | ประเด็นที่ต้องพิสูจน์ | 6M26 ต้องเห็นทั้งปริมาณและ margin ฟื้น ไม่ใช่เพียงยอดขายเพิ่ม | F3_E1, F3_E2 |

#### ทะเบียนหลักฐาน — F3

- **`FY_PANEL`** · _ข้อเท็จจริงจากการคำนวณ_ — Audited FY2024-25 company panel
  - RFO / NPAT-to-owners / independent panel membership; QA 43 pass / 0 fail
  - บทบาท: historical fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_company_fy2024_2025_audited_2026-08-07.csv`
  - SHA-256: `e5e04dbc40ffcc79fed58545a93dc4549c29cdaecf260bea73711bc6d0720481`
- **`SET_PUBLIC_EOD`** · _ข้อเท็จจริงจากการคำนวณ_ — SET public Company Highlights — EOD 2026-08-07
  - Adjusted YTD; unadjusted price, market cap and valuation; factsheet-surface cross-check
  - บทบาท: current market fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_set_public_surface_reconciliation_2026-08-07.csv`
  - SHA-256: `544c1f29fe2d409ee398822ac2bf32b769081718962ae2d1138985b0146b9530`
- **`SET_COMPANY_PROFILE`** · _ข้อเท็จจริง_ — SET company profiles — English and Thai
  - Official company names and business descriptions refreshed and validated for the 118-company perimeter from the public SET profile API
  - บทบาท: company business profile
  - URL: <https://www.set.or.th/th/market/product/stock/overview>
- **`COMPANY_REPORTS`** · _ข้ออนุมานนักวิเคราะห์_ — Company report synthesis corpus
  - Annual-only draft synthesis; reconciled to the ticker FY2025 MD&A where available
  - บทบาท: secondary synthesis; not management attribution
  - พาธ: `data/company-reports.json`
  - SHA-256: `c1a2bc40cbe21a2058aa596c362e4d47ad117360831b847de78ec414831fd2d2`
- **`MDA_ITC_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — ITC FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/ITC/MDA_ITC_2025FY_T.md`
  - SHA-256: `5453172b9273ec3b68f8ba6c6f3862d0436b6d68af3d77aa4bfdb4e56e7c3fc1`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/1725NWS180220261247299300T.pdf>
- **`MDA_AAI_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — AAI FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/AAI/MDA_AAI_2025FY_T.md`
  - SHA-256: `17a0421893115c8b63ce4dd5c6320745e7a442498f0095f2798e2320a1807f0e`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/1723NWS200220261708333270T.pdf>
- **`F3_E1`** · _ฝ่ายจัดการ_ — ITC FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/ITC/MDA_ITC_2025FY_E.md`
  - SHA-256: `5b2480fe874636d597dbf9989fb2721aed25087548af73941a3216174af4745a`
- **`F3_E2`** · _ฝ่ายจัดการ_ — AAI FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/AAI/MDA_AAI_2025FY_E.md`
  - SHA-256: `670e112b8b5f02df41828084535393092e5656196325f5d6236ce65ebda2a964`
- **`F3_FACTSHEET`** · _ข้อเท็จจริงจากการคำนวณ_ — SET Factsheet — ITC
  - Live leader cross-check
  - บทบาท: presentation-surface check
  - URL: <https://www.set.or.th/th/market/product/stock/quote/itc/factsheet>

### F8 · น้ำตาล แป้ง และน้ำมันบริโภค — งวดปฏิทินอ่อนตัว และมุมทุกปีบัญชีแย่กว่าชัดเจน

`ยังถูกกดดัน` · 6.8% M-cap · THB 54.9bn · 9 บริษัท

| ตัวชี้วัด | RFO | NPAT | ราคา | P/E |
|---|---|---|---|---|
| ช่วง | FY2025 YoY | ส่วนผู้ถือหุ้น FY2025 YoY | ราคา YTD ปรับแล้ว | เฉพาะบริษัทที่มีกำไร |
| ค่า | -7.0% | -21.0% | +12.1% | 9.8x |
| จำนวน | THB 74.0bn FY2025 | THB 4.1bn FY2025 | ณ 7 ส.ค. 2569 | ค่าเฉลี่ยรวม |
| ครอบคลุม | 7/9 | 7/9 | 9/9 • 100% M-cap | 6/9 • 72% M-cap |

**ข้อเท็จจริงที่สังเกตได้** — FY2025: RFO -7.0% • NPAT -21.0% • ราคา YTD +12.1% • P/E 9.8x • ครอบคลุม RFO 7/9 • NPAT 7/9

**มุมมองตามปีบัญชีของผู้ออก** — Mixed issuer FY closes: 30-Sep, 31-Oct and 31-Dec • 9/9 บริษัท • RFO -5.2% • NPAT -60.0% • Margin +2.1%

#### เหตุผลที่เปลี่ยน

1. _ข้อเท็จจริงจากการคำนวณ_ · ราคาสินค้าโภคภัณฑ์ — กลุ่มปิดงบธันวาคม: RFO -7.0% และ NPAT ส่วนผู้ถือหุ้น -21.0% ครอบคลุม 7/9 บริษัท
2. _ข้อเท็จจริงจากการคำนวณ_ · ส่วนต่างผลิต — มุมทุกปีบัญชี: RFO -5.2% และ NPAT -60.0%; ผสมรอบปิดงบ 30 ก.ย., 31 ต.ค. และ 31 ธ.ค. จึงแสดงแยก
3. _ข้อเท็จจริงจากการคำนวณ_ · สินค้าคงคลัง — TVO เป็นตัวฉุดรายได้ และ KSL เป็นตัวฉุดกำไรในมุมทุกปีบัญชี

#### ห่วงโซ่เหตุและผล

**ราคาสินค้าโภคภัณฑ์** → **ส่วนต่างผลิต** → **สินค้าคงคลัง** → **Margin** (5.5% -1.0 ppt YoY) → **NPAT** (-21.0% THB 4.1bn FY2025)

#### บทบาทในกลุ่ม

| บทบาท | Ticker | ค่า | ที่มาของค่า |
|---|---|---|---|
| ผู้นำและตัวฉุดรายได้ | TVO | 44% | สัดส่วน Market Cap ในกลุ่ม |
| ตัวฉุดกำไรมุมทุกปีบัญชี | KSL | — | NPAT YoY · Δ −1.6bn |

#### มูลค่า

**แรงกดดันปัจจุบัน / ข้อเท็จจริง** — P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 9.8x ครอบคลุม 6/9 บริษัท และ 71.8% ของ market cap ที่มีข้อมูล. multiple ของกลุ่มผู้มีกำไรสะท้อนวัฏจักรสินค้าโภคภัณฑ์ที่แตกต่าง ส่วน KSL เพิ่มความเสี่ยงด้าน leverage คดีความ และ refinancing แยกต่างหาก โดย KSL ไม่อยู่ในชุดบริษัทที่ใช้คำนวณ P/E

| Trigger | Risk |
|---|---|
| crush margin ถั่วเหลืองและ bridge inventory/NRV ของ TVO ดีขึ้น | ราคาวัตถุดิบและผลิตภัณฑ์ถั่วเหลืองของ TVO ไม่สอดคล้อง |
| ปริมาณอ้อยและราคาขายน้ำตาลจริงของ KSL/KTIS ดีขึ้น | ราคาน้ำตาลลดลง สภาพอากาศ และปริมาณอ้อยผันผวนที่ KSL/KTIS |
| กระแสเงินสดดำเนินงานรายบริษัทครอบคลุมภาระหนี้ | ความเสี่ยงเฉพาะ KSL ด้าน leverage คดีความ และ refinancing |

**6M26 ต้องพิสูจน์** — 6M26 ต้อง bridge แยก TVO ด้าน crush/NRV และ KSL/KTIS ด้านปริมาณอ้อย ราคาน้ำตาลจริง hedging ด้อยค่า และการชำระหนี้

#### วิเคราะห์รายบริษัท — F8 น้ำตาล แป้ง และน้ำมันบริโภค

_ทุกบริษัทใน perimeter ของ Segment ที่สอบทาน_

| Ticker | บทบาท | M-cap | RFO YoY | NPAT YoY | ราคา YTD | P/E | Margin |
|---|---|---|---|---|---|---|---|
| TVO | ผู้นำและตัวฉุดรายได้ | THB 24.2bn | -9.2% | +4.1% | +21.7% | 10.3x | 7.9% |
| KSL | ตัวฉุดกำไรมุมทุกปีบัญชี | THB 7.2bn | — | — | +30.2% | n.m. | — |
| KTIS | บริษัทในกลุ่ม | THB 7.0bn | — | — | -7.6% | n.m. | — |
| LST | บริษัทในกลุ่ม | THB 3.9bn | +10.6% | +2.2% | +0.9% | 6.9x | 4.1% |
| KBS | บริษัทในกลุ่ม | THB 3.6bn | -8.0% | -41.3% | +4.3% | 7.2x | 5.6% |
| BRR | บริษัทในกลุ่ม | THB 3.0bn | -21.2% | -73.4% | +0.6% | 26.0x | 4.6% |
| TWPC | บริษัทในกลุ่ม | THB 2.5bn | -8.3% | กลับเป็นกำไร | -1.4% | 12.2x | 1.7% |
| CPI | บริษัทในกลุ่ม | THB 2.2bn | +2.6% | +30.5% | +5.5% | 8.5x | 7.9% |
| PQS | บริษัทในกลุ่ม | THB 1.2bn | -27.9% | ขาดทุน | +23.8% | n.m. | -4.0% |

##### TVO — ผู้นำและตัวฉุดรายได้ · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท น้ำมันพืชไทย จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและจำหน่ายน้ำมันถั่วเหลือง ตราองุ่น และวัตถุดิบอาหารสัตว์ ได้แก่ กากถั่วเหลือง, ดีฮัล ซอยมีล, ฟูลแฟตซอย, ดีฮัล ฟูลแฟตซอย รวมทั้ง เลซิติน ซอยฮัล น้ำมันข้าวโพด น้ำมันทานตะวัน น้ำมันคาโนลา และน้ำมันมะกอก

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 24.2bn | 27.25 | +21.7% | 10.3x | 7.9% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 30.6bn → FY2025 THB 27.8bn · −2.8bn · -9.2%

- ยอดขายลด 9.2% เพราะราคาขายเฉลี่ยปรับตามราคาถั่วเหลืองโลกที่ลดลง และปริมาณส่งออกเผชิญการแข่งขันด้านราคาสูง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 1. Sales Revenues The Company and its subsidiary had total sales revenue of Baht 27,793 million, a decrease of Baht 2,803 million or 9.2% from Baht 30,596 million compared to 2024. Revenue from sales of products was Baht 27,453 million, decreased by Baht 2,752 million or 9.1% from Baht 30,205 million compared to 2024. Revenue from sales of packaging materials was Baht 341 million, a decrease of Baht 50 million or 12.9% from Baht 391 million compared to 2024. The details were as follows • Revenue from sales of soybean meal and other animal feed ingredients decreased compared to the previous year, primarily due to a decline in the average selling price per unit, in line with the downward trend

  `MDA_TVO_FY2025` · `p009` · SHA 9d94b5b99fde
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 2.1bn → FY2025 THB 2.2bn · +86m · +4.1%

- กำไรยังเพิ่ม 4.1% เพราะต้นทุนถั่วเหลืองและการบริหารสต็อก/ต้นทุนช่วยให้ อัตรากำไรขั้นต้น เพิ่มเป็น 12.9% จาก 10.7%
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Conclusion of the operational performance in 2025 For the year 2025, the Company and its subsidiary reported total sales revenue of Baht 27,793 million, a decrease of Baht 2,803 million or 9.2%. Total cost of sales amounted to Baht 24,203 million, down Baht 3,116 million or 11.4%, resulting in a gross profit of Baht 3,590 million, an increase of Baht 313 million or 9.6%. Selling expenses totaled Baht 614 million, rising by Baht 32 million or 5.5%, while administrative expenses reached Baht 335 million, an increase of Baht 49 million or 17.0%. Overall, the company and its subsidiaries achieved a net profit of Baht 2,189 million, an increase of Baht 86 million or 4.1% compared to 2024

  `MDA_TVO_FY2025` · `p020` · SHA 16c92e3d2be0
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- ผล FX/อนุพันธ์พลิกจากกำไร 87 ลบ. เป็นขาดทุน 116 ลบ. เป็นแหล่งความผันผวนที่ต้องแยกจากการดำเนินงาน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 3. Profit (loss) on exchange rate / derivatives The company managed and hedged foreign exchange risk through forward exchange contracts, resulting in a foreign exchange and derivatives loss of Baht 116 million. This represents a decrease of Baht 203 million or 233.6% from the Baht 87 million gain recorded in 2024. The primary reason was the significant appreciation trend of the Thai

  `MDA_TVO_FY2025` · `p013` · SHA f3aa2a56d7ba
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_TVO_FY2025`

##### KSL — ตัวฉุดกำไรมุมทุกปีบัญชี · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท น้ำตาลขอนแก่น จำกัด (มหาชน)** — ข้อมูลเทียบเคียงจำกัด: ไม่ควรสรุปเหตุเชื่อมโยงระหว่างรายได้กับกำไร

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัท และบริษัทย่อยเเป็นผู้ผลิตและจำหน่ายน้ำตาลทราย รวมทั้งผลิตภัณฑ์เกี่ยวเนื่อง เช่น ไฟฟ้า เอทานอล และปุ๋ยอินทรีย์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 7.2bn | 1.64 | +30.2% | n.m. | — |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 4 · NPAT 4 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 16.4bn → FY2025 THB 15.9bn · −540m

- RFO ปี 2568 อยู่ที่ 15,902 ลบ. ลด 3.3% YoY; MD&A ระบุว่า รายได้อื่น รายได้อื่นในปี 2568 เพิ่มขึ้น 285 ล้านบาท หรือเพิ่มขึ้นร้อยละ109 เนื่องจากบริษัทได้รับรายได้ค่าสิทธิ์จากการ จำหน่ายน้ำตาลทรายในประเทศ และรายได้ค่าผลตอบแทนการผลิตและจำหน่ายน้ำตาลทรายที่บริษัทคาดว่าจะได้รับจาก
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้อื่น รายได้อื่นในปี 2568 เพิ่มขึ้น 285 ล้านบาท หรือเพิ่มขึ้นร้อยละ109 เนื่องจากบริษัทได้รับรายได้ค่าสิทธิ์จากการ จำหน่ายน้ำตาลทรายในประเทศ และรายได้ค่าผลตอบแทนการผลิตและจำหน่ายน้ำตาลทรายที่บริษัทคาดว่าจะได้รับจาก

  `MDA_KSL_FY2025` · `p009` · SHA 4a2c3c3b5b7b
  </details>
- RFO ปี 2568 อยู่ที่ 15,902 ลบ. ลด 3.3% YoY; MD&A ระบุว่า เข้าหีบที่เพิ่มขึ้น ในขณะที่ราคาขายน้ำตาลเฉลี่ยโดยรวมลดลงร้อยละ 16 (2) รายได้จากการขายไฟฟ้าลดลง จาก 1,521 ล้านบาท เป็น 1,417 ล้านบาท หรือลดลงร้อยละ 7 โดยมีสาเหตุจาก
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > เข้าหีบที่เพิ่มขึ้น ในขณะที่ราคาขายน้ำตาลเฉลี่ยโดยรวมลดลงร้อยละ 16 (2) รายได้จากการขายไฟฟ้าลดลง จาก 1,521 ล้านบาท เป็น 1,417 ล้านบาท หรือลดลงร้อยละ 7 โดยมีสาเหตุจาก

  `MDA_KSL_FY2025` · `p005` · SHA 4c355b37aeb4
  </details>
- RFO ปี 2568 อยู่ที่ 15,902 ลบ. ลด 3.3% YoY; MD&A ระบุว่า ปริมาณการขายไฟฟ้าลดลงร้อยละ 7 (3) รายได้จากธุรกิจสนับสนุนเพิ่มขึ้น จาก 803 ล้านบาท เป็น 919 ล้านบาท หรือเพิ่มขึ้นร้อยละ 14 เนื่องจากปริมาณ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ปริมาณการขายไฟฟ้าลดลงร้อยละ 7 (3) รายได้จากธุรกิจสนับสนุนเพิ่มขึ้น จาก 803 ล้านบาท เป็น 919 ล้านบาท หรือเพิ่มขึ้นร้อยละ 14 เนื่องจากปริมาณ

  `MDA_KSL_FY2025` · `p006` · SHA 51397b0cde52
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 918m → FY2025 −THB 660m · −1.6bn

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -660 ลบ. จากกำไร 918 ลบ.; MD&A ระบุว่า ผลขาดทุนจากการด้อยค่า ขาดทุนจากการด้อยค่าในปี 2568 เพิ่มขึ้น 706 ล้านบาท เนื่องจากการตั้งสำรองค่าเผื่อการด้อยค่าของทรัพย์สิน ในธุรกิจต่างประเทศ จากการประเมินมูลค่าที่คาดว่าจะได้รับคืนของทรัพย์สิน โดยพิจารณามูลค่าจากการใช้ต่ำกว่ามูลค่า
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ผลขาดทุนจากการด้อยค่า ขาดทุนจากการด้อยค่าในปี 2568 เพิ่มขึ้น 706 ล้านบาท เนื่องจากการตั้งสำรองค่าเผื่อการด้อยค่าของทรัพย์สิน ในธุรกิจต่างประเทศ จากการประเมินมูลค่าที่คาดว่าจะได้รับคืนของทรัพย์สิน โดยพิจารณามูลค่าจากการใช้ต่ำกว่ามูลค่า

  `MDA_KSL_FY2025` · `p012` · SHA bab2280277ce
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -660 ลบ. จากกำไร 918 ลบ.; MD&A ระบุว่า กำไรขั้นต้น กำไรขั้นต้น ลดลงจาก 2,741 ล้านบาทในปี 2567 เป็น 1,596 ล้านบาท ในปี 2568 และอัตรากำไรขั้นต้นลดลง จากร้อยละ 17 ในปี 2567 เป็นร้อยละ 10 ในปี 2568 สาเหตุหลักมาจากราคาขายน้ำตาลตลาดโลกถัวเฉลี่ยที่ลดลง
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไรขั้นต้น กำไรขั้นต้น ลดลงจาก 2,741 ล้านบาทในปี 2567 เป็น 1,596 ล้านบาท ในปี 2568 และอัตรากำไรขั้นต้นลดลง จากร้อยละ 17 ในปี 2567 เป็นร้อยละ 10 ในปี 2568 สาเหตุหลักมาจากราคาขายน้ำตาลตลาดโลกถัวเฉลี่ยที่ลดลง

  `MDA_KSL_FY2025` · `p008` · SHA 24f0013db7c7
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -660 ลบ. จากกำไร 918 ลบ.; MD&A ระบุว่า บริษัท น้ำตาลขอนแก่น จำกัด (มหาชน) และบริษัทย่อย (KSL) ขอชี้แจงผลการดำเนินงานประจำ ปีบัญชี 2568 (ตั้งแต่วันที่ 1 พฤศจิกายน 2567 ถึงวันที่ 31 ตุลาคม 2568) บริษัทมีผลขาดทุนสุทธิส่วนที่เป็นของบริษัทใหญ่ จำนวน (660) ล้านบาท ขาดทุนเพิ่มขึ้นเมื่อเปรียบเทียบกับผลประกอบการสำหรับปีบัญชี 2567 ซึ่งมีกำไรสุทธิ จำนวน
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > บริษัท น้ำตาลขอนแก่น จำกัด (มหาชน) และบริษัทย่อย (KSL) ขอชี้แจงผลการดำเนินงานประจำ ปีบัญชี 2568 (ตั้งแต่วันที่ 1 พฤศจิกายน 2567 ถึงวันที่ 31 ตุลาคม 2568) บริษัทมีผลขาดทุนสุทธิส่วนที่เป็นของบริษัทใหญ่ จำนวน (660) ล้านบาท ขาดทุนเพิ่มขึ้นเมื่อเปรียบเทียบกับผลประกอบการสำหรับปีบัญชี 2567 ซึ่งมีกำไรสุทธิ จำนวน

  `MDA_KSL_FY2025` · `p002` · SHA 481a121b9fd5
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -660 ลบ. จากกำไร 918 ลบ.; MD&A ระบุว่า ต้นทุนในการจัดจำหน่าย ต้นทุนในการจัดจำหน่ายในปี 2568 เพิ่มขึ้น 133 ล้านบาท หรือเพิ่มขึ้นร้อยละ 34 จากค่าขนส่งและค่าใช้จ่ายใน
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ต้นทุนในการจัดจำหน่าย ต้นทุนในการจัดจำหน่ายในปี 2568 เพิ่มขึ้น 133 ล้านบาท หรือเพิ่มขึ้นร้อยละ 34 จากค่าขนส่งและค่าใช้จ่ายใน

  `MDA_KSL_FY2025` · `p011` · SHA adbfe86a67f2
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ผลขาดทุนจากการด้อยค่า ขาดทุนจากการด้อยค่าในปี 2568 เพิ่มขึ้น 706 ล้านบาท เนื่องจากการตั้งสำรองค่าเผื่อการด้อยค่าของทรัพย์สิน ในธุรกิจต่างประเทศ จากการประเมินมูลค่าที่คาดว่าจะได้รับคืนของทรัพย์สิน โดยพิจารณามูลค่าจากการใช้ต่ำกว่ามูลค่า
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ผลขาดทุนจากการด้อยค่า ขาดทุนจากการด้อยค่าในปี 2568 เพิ่มขึ้น 706 ล้านบาท เนื่องจากการตั้งสำรองค่าเผื่อการด้อยค่าของทรัพย์สิน ในธุรกิจต่างประเทศ จากการประเมินมูลค่าที่คาดว่าจะได้รับคืนของทรัพย์สิน โดยพิจารณามูลค่าจากการใช้ต่ำกว่ามูลค่า

  `MDA_KSL_FY2025` · `p012` · SHA bab2280277ce
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_KSL_FY2025`

##### KTIS — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เกษตรไทย อินเตอร์เนชั่นแนล ชูการ์ คอร์ปอเรชั่น จำกัด (มหาชน)** — ข้อมูลเทียบเคียงจำกัด: ไม่ควรสรุปเหตุเชื่อมโยงระหว่างรายได้กับกำไร

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — กลุ่มบริษัทดำเนินธุรกิจน้ำตาลทราย และอุตสาหกรรมต่อเนื่องครบวงจรที่เกี่ยวกับผลพลอยได้จากการผลิตน้ำตาลทราย ได้แก่ โรงงานผลิตเอทานอล โรงงานผลิตเยื่อกระดาษฟอกขาวจากชานอ้อย โรงไฟฟ้าชีวมวล และโรงงานผลิตวัสดุปรับปรุงดินชีวภาพ

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 7.0bn | 1.82 | -7.6% | n.m. | — |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 9 · NPAT 7 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 2

**RFO — เพราะอะไร** — FY2024 THB 14.4bn → FY2025 THB 14.8bn · +387m

- RFO ปี 2568 อยู่ที่ 14,806 ลบ. เพิ่ม 2.7% YoY; MD&A ระบุว่า ต่อลิตรที่ลดลง " รายได้จากการขายไฟฟ้าเพิ่มขึ้นร้อยละ 24.0 จากปริมาณการขายไฟฟ้าเพิ่มขึ้น " รายได้จากการขายและการให้บริการอื่นเพิ่มขึ้นร้อยละ 27.4 จากการให้บริการจักรกลทางการ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ต่อลิตรที่ลดลง " รายได้จากการขายไฟฟ้าเพิ่มขึ้นร้อยละ 24.0 จากปริมาณการขายไฟฟ้าเพิ่มขึ้น " รายได้จากการขายและการให้บริการอื่นเพิ่มขึ้นร้อยละ 27.4 จากการให้บริการจักรกลทางการ

  `MDA_KTIS_FY2025` · `p008` · SHA 84f1a30572a7
  </details>
- RFO ปี 2568 อยู่ที่ 14,806 ลบ. เพิ่ม 2.7% YoY; MD&A ระบุว่า ผลิตและจำหน่ายน้ำตาลทรายขั้นสุดท้ายเป็นรายได้ค่าผลตอบแทนการผลิตและจำหน่ายน้ำตาลทราย 1.3 รายได้อื่นในปี 2568 จำนวน 347.3 ล้านบาท เพิ่มขึ้นร้อยละ 15.5 จากปีก่อนที่ 300.8 ล้านบาท โดยมี สาเหตุหลักมาจากมีกำไรจากอัตราแลกเปลี่ยน, กำไรจากการซื้อขายน้ำตาลล่วงหน้า และอื่นๆ เพิ่มขึ้น 2. ต้นทุนขายและบริการในปี 2568 จำนวน 13,444.1 ล้านบาท เพิ่มขึ้นร้อยละ 5.1 จาก 12,788.7 ล้านบาท ในช่วง
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ผลิตและจำหน่ายน้ำตาลทรายขั้นสุดท้ายเป็นรายได้ค่าผลตอบแทนการผลิตและจำหน่ายน้ำตาลทราย 1.3 รายได้อื่นในปี 2568 จำนวน 347.3 ล้านบาท เพิ่มขึ้นร้อยละ 15.5 จากปีก่อนที่ 300.8 ล้านบาท โดยมี สาเหตุหลักมาจากมีกำไรจากอัตราแลกเปลี่ยน, กำไรจากการซื้อขายน้ำตาลล่วงหน้า และอื่นๆ เพิ่มขึ้น 2. ต้นทุนขายและบริการในปี 2568 จำนวน 13,444.1 ล้านบาท เพิ่มขึ้นร้อยละ 5.1 จาก 12,788.7 ล้านบาท ในช่วง

  `MDA_KTIS_FY2025` · `p018` · SHA 4c0781e2239d
  </details>
- RFO ปี 2568 อยู่ที่ 14,806 ลบ. เพิ่ม 2.7% YoY; MD&A ระบุว่า เดียวกันของปี 2567 เป็นสัดส่วนกับรายได้จากการขายและบริการที่เพิ่มขึ้น 3. ค่าใช้จ่ายในการขายและการบริหาร 1,674.9 ล้านบาท ในปี 2568 เพิ่มขึ้นร้อยละ 25.8 จาก 1,331.6 ล้านบาท ใน ปีก่อน โดยมีสาเหตุหลักมาจากค่าเผื่อหนี้สงสัยจะสูญและหนี้สูญ, ค่าขนส่ง, ค่าฝากน้ำตาลทรายและกากน้ำตาล,
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > เดียวกันของปี 2567 เป็นสัดส่วนกับรายได้จากการขายและบริการที่เพิ่มขึ้น 3. ค่าใช้จ่ายในการขายและการบริหาร 1,674.9 ล้านบาท ในปี 2568 เพิ่มขึ้นร้อยละ 25.8 จาก 1,331.6 ล้านบาท ใน ปีก่อน โดยมีสาเหตุหลักมาจากค่าเผื่อหนี้สงสัยจะสูญและหนี้สูญ, ค่าขนส่ง, ค่าฝากน้ำตาลทรายและกากน้ำตาล,

  `MDA_KTIS_FY2025` · `p019` · SHA f7ff84b19259
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 690m → FY2025 −THB 1.3bn · −579m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -1,270 ลบ. จาก -690 ลบ.; MD&A ระบุว่า ผลิตและจำหน่ายน้ำตาลทรายขั้นสุดท้ายเป็นรายได้ค่าผลตอบแทนการผลิตและจำหน่ายน้ำตาลทราย 1.3 รายได้อื่นในปี 2568 จำนวน 347.3 ล้านบาท เพิ่มขึ้นร้อยละ 15.5 จากปีก่อนที่ 300.8 ล้านบาท โดยมี สาเหตุหลักมาจากมีกำไรจากอัตราแลกเปลี่ยน, กำไรจากการซื้อขายน้ำตาลล่วงหน้า และอื่นๆ เพิ่มขึ้น 2. ต้นทุนขายและบริการในปี 2568 จำนวน 13,444.1 ล้านบาท เพิ่มขึ้นร้อยละ 5.1 จาก 12,788.7 ล้านบาท ในช่วง
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ผลิตและจำหน่ายน้ำตาลทรายขั้นสุดท้ายเป็นรายได้ค่าผลตอบแทนการผลิตและจำหน่ายน้ำตาลทราย 1.3 รายได้อื่นในปี 2568 จำนวน 347.3 ล้านบาท เพิ่มขึ้นร้อยละ 15.5 จากปีก่อนที่ 300.8 ล้านบาท โดยมี สาเหตุหลักมาจากมีกำไรจากอัตราแลกเปลี่ยน, กำไรจากการซื้อขายน้ำตาลล่วงหน้า และอื่นๆ เพิ่มขึ้น 2. ต้นทุนขายและบริการในปี 2568 จำนวน 13,444.1 ล้านบาท เพิ่มขึ้นร้อยละ 5.1 จาก 12,788.7 ล้านบาท ในช่วง

  `MDA_KTIS_FY2025` · `p018` · SHA 4c0781e2239d
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -1,270 ลบ. จาก -690 ลบ.; MD&A ระบุว่า ตามลำดับ จากผลการดำเนินงานของกิจการร่วมค้าที่ประสบผลขาดทุน 8. บริษัทฯ มีต้นทุนทางการเงิน 262.3 ล้านบาท ในปี 2568 ลดลงเล็กน้อยร้อยละ 1.7 จากต้นทุนทางการเงิน 266.9 ล้านบาท ในปี 2567 จากค่าใช้จ่ายดอกเบี้ยของเงินกู้ยืม และค่าใช้จ่ายดอกเบี้ยของหนี้สินตามสัญญาเช่าลดลง 9. สำหรับผลประโยชน์ (ค่าใช้จ่าย) ภาษีเงินได้ บริษัทฯ มีผลประโยชน์ภาษีเงินได้ 77.3 ล้านบาท ในปี 2568 เทียบกับ ค่าใช้จ่ายภาษีเงินได้ในปี 2567 ที่ 209.4 ล้านบาท เนื่องจากภาษีเงินได้รอการตัดบัญชีเพิ่มขึ้น
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ตามลำดับ จากผลการดำเนินงานของกิจการร่วมค้าที่ประสบผลขาดทุน 8. บริษัทฯ มีต้นทุนทางการเงิน 262.3 ล้านบาท ในปี 2568 ลดลงเล็กน้อยร้อยละ 1.7 จากต้นทุนทางการเงิน 266.9 ล้านบาท ในปี 2567 จากค่าใช้จ่ายดอกเบี้ยของเงินกู้ยืม และค่าใช้จ่ายดอกเบี้ยของหนี้สินตามสัญญาเช่าลดลง 9. สำหรับผลประโยชน์ (ค่าใช้จ่าย) ภาษีเงินได้ บริษัทฯ มีผลประโยชน์ภาษีเงินได้ 77.3 ล้านบาท ในปี 2568 เทียบกับ ค่าใช้จ่ายภาษีเงินได้ในปี 2567 ที่ 209.4 ล้านบาท เนื่องจากภาษีเงินได้รอการตัดบัญชีเพิ่มขึ้น

  `MDA_KTIS_FY2025` · `p023` · SHA 5b58ab19abec
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -1,270 ลบ. จาก -690 ลบ.; MD&A ระบุว่า ตลาดหลักทรัพย์แห่งประเทศไทย บริษัท เกษตรไทย อินเตอร์เนชั่นแนล ชูการ์ คอร์ปอเรชั่น จำกัด (มหาชน) ("บริษัทฯ") ขอชี้แจงผลการดำเนินงานของ บริษัทและบริษัทย่อยสำหรับปี 2568 สิ้นสุดวันที่ 30 กันยายน 2568 ซึ่งมีผลขาดทุนสุทธิ 1,269.8 ล้านบาท ลดลงร้อยละ 83.9 จากปี 2567 สิ้นสุดวันที่ 30 กันยายน 2567 ซึ่งขาดทุนสุทธิ 690.4 ล้านบาท ทั้งนี้เป็นผลจากปัจจัยดังต่อไปนี้ 1. บริษัทฯ มีรายได้รวมในปี 2568 จำนวน 15,190.9 ล้านบาท เพิ่มขึ้นร้อยละ 2.8 จาก 14,775.3 ล้านบาท ในปี
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ตลาดหลักทรัพย์แห่งประเทศไทย บริษัท เกษตรไทย อินเตอร์เนชั่นแนล ชูการ์ คอร์ปอเรชั่น จำกัด (มหาชน) ("บริษัทฯ") ขอชี้แจงผลการดำเนินงานของ บริษัทและบริษัทย่อยสำหรับปี 2568 สิ้นสุดวันที่ 30 กันยายน 2568 ซึ่งมีผลขาดทุนสุทธิ 1,269.8 ล้านบาท ลดลงร้อยละ 83.9 จากปี 2567 สิ้นสุดวันที่ 30 กันยายน 2567 ซึ่งขาดทุนสุทธิ 690.4 ล้านบาท ทั้งนี้เป็นผลจากปัจจัยดังต่อไปนี้ 1. บริษัทฯ มีรายได้รวมในปี 2568 จำนวน 15,190.9 ล้านบาท เพิ่มขึ้นร้อยละ 2.8 จาก 14,775.3 ล้านบาท ในปี

  `MDA_KTIS_FY2025` · `p003` · SHA 5d70d560dcc4
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -1,270 ลบ. จาก -690 ลบ.; MD&A ระบุว่า ปี 2567 จากความผันผวนของอัตราแลกเปลี่ยนเงินตราต่างประเทศ และราคาสินค้าโภคภัณฑ์ 6. บริษัทฯ มีกำไรจากการซื้อขายน้ำตาลล่วงหน้า 26.7 ล้านบาท ในปี 2568 เทียบกับผลขาดทุนจากการซื้อขาย น้ำตาลล่วงหน้า 242.6 ล้านบาท ปี 2567 จากราคาน้ำตาลในตลาดโลกมีความผันผวนสูง 7. บริษัทฯ รับรู้ส่วนแบ่งขาดทุนจากการร่วมค้า 851.8 ล้านบาท ในปี 2568 และ 556.6 ล้านบาท ในปี 2567
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ปี 2567 จากความผันผวนของอัตราแลกเปลี่ยนเงินตราต่างประเทศ และราคาสินค้าโภคภัณฑ์ 6. บริษัทฯ มีกำไรจากการซื้อขายน้ำตาลล่วงหน้า 26.7 ล้านบาท ในปี 2568 เทียบกับผลขาดทุนจากการซื้อขาย น้ำตาลล่วงหน้า 242.6 ล้านบาท ปี 2567 จากราคาน้ำตาลในตลาดโลกมีความผันผวนสูง 7. บริษัทฯ รับรู้ส่วนแบ่งขาดทุนจากการร่วมค้า 851.8 ล้านบาท ในปี 2568 และ 556.6 ล้านบาท ในปี 2567

  `MDA_KTIS_FY2025` · `p022` · SHA e820d9566428
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: 2567 ตามลำดับ จากลูกหนี้ชาวไร่ด้อยคุณภาพที่เพิ่มขึ้น 5. บริษัทฯ ขาดทุนจากการปรับมูลค่ายุติธรรมของตราสารอนุพันธ์ 52.8 ล้านบาท ในปี 2568 และ 10.5 ล้านบาท ใน
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > 2567 ตามลำดับ จากลูกหนี้ชาวไร่ด้อยคุณภาพที่เพิ่มขึ้น 5. บริษัทฯ ขาดทุนจากการปรับมูลค่ายุติธรรมของตราสารอนุพันธ์ 52.8 ล้านบาท ในปี 2568 และ 10.5 ล้านบาท ใน

  `MDA_KTIS_FY2025` · `p021` · SHA 856febdc15ec
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ค่าใช้จ่ายในการส่งออก, ค่าเสื่อมราคา และค่าใช้จ่ายอื่นๆ ที่เพิ่มขึ้น 4. บริษัทฯ ขาดทุนจากการด้อยค่าของสินทรัพย์ทางการเงิน 275.6 ล้านบาท และ82.6 ล้านบาท ในปี 2568 และ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ค่าใช้จ่ายในการส่งออก, ค่าเสื่อมราคา และค่าใช้จ่ายอื่นๆ ที่เพิ่มขึ้น 4. บริษัทฯ ขาดทุนจากการด้อยค่าของสินทรัพย์ทางการเงิน 275.6 ล้านบาท และ82.6 ล้านบาท ในปี 2568 และ

  `MDA_KTIS_FY2025` · `p020` · SHA f3178ceccd73
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_KTIS_FY2025`

##### LST — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ล่ำสูง (ประเทศไทย) จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและจำหน่ายผลิตภัณฑ์น้ำมันพืช มาการีนและไขมันพืชผสม

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 3.9bn | 4.74 | +0.9% | 6.9x | 4.1% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 7 · NPAT 6 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 11.6bn → FY2025 THB 12.8bn · +1.2bn · +10.6%

- RFO ปี 2568 อยู่ที่ 12,818 ลบ. เพิ่ม 10.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 1. Revenues Revenues from contracts with customers: Revenue from sales of the company and its subsidiaries increased by Baht 1,228.3 million or 10.6%, compared to 2024 mainly driven from higher sales of both the Company and subsidiary (UPOIC). Sales revenue in each product group is shown as the table below.

  `MDA_LST_FY2025` · `p006` · SHA c1449be0b8e9
  </details>
- RFO ปี 2568 อยู่ที่ 12,818 ลบ. เพิ่ม 10.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ปริมาณขายและปริมาณการผลิต และ ราคาขายและส่วนผสมผลิตภัณฑ์ และ อุปสงค์และกำลังซื้อในประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Financial performance analysis and explanation For the year 2025, the company's revenue from sales increased by Baht 1,106.1 million or 13.9% compared to 2024. This was due to a 15.2% increase in the average selling price per unit against a 1.1% decrease in the sales volume. Gross profit increased by Baht 109.0 million or 16.0%, making profit increased by Baht 24.0 million or 7.8% mainly driven from an increase in the average selling price per unit from raw material shortage between Q4/2024 and Q1/2025 while sale volume decreased from lower demand of HORECA customers as a consequence from economic slowdown and lower number of tourists. However, the focus has been strategically shifted to inc

  `MDA_LST_FY2025` · `p004` · SHA f99199936676
  </details>
- RFO ปี 2568 อยู่ที่ 12,818 ลบ. เพิ่ม 10.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ความเสี่ยงด้านภูมิรัฐศาสตร์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2. Expenses Cost of sales: The Company and its subsidiaries recorded cost of sales ratio for the period at 88.0% (2024: 87.1%). The cost of sales ratio under LST was 91.3% (2024: 91.4%). Subsidiary (UPOIC) recorded cost of sales ratio at 84.6% (2024: 84.9%). The CPO extraction rate increased by 7.5% and CPKO’s extraction rate increased by 2.6%. Subsidiary (UFC) recorded cost of sales ratio at 81.5% (2024: 78.6%). Selling and distribution expenses: The Company and its subsidiaries recorded selling and distribution expenses at Baht 602.6 million (2024: Baht 588.2 million), increasing by Baht 14.4 million. LST’s expenses increased by Baht 42.6 million mainly from warehouse rent, transportation

  `MDA_LST_FY2025` · `p010` · SHA b6641f37a7a4
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 517m → FY2025 THB 528m · +11m · +2.2%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 528 ลบ. เพิ่ม 2.2% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ปริมาณขายและปริมาณการผลิต และ ราคาขายและส่วนผสมผลิตภัณฑ์ และ อุปสงค์และกำลังซื้อในประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Financial performance analysis and explanation For the year 2025, the company's revenue from sales increased by Baht 1,106.1 million or 13.9% compared to 2024. This was due to a 15.2% increase in the average selling price per unit against a 1.1% decrease in the sales volume. Gross profit increased by Baht 109.0 million or 16.0%, making profit increased by Baht 24.0 million or 7.8% mainly driven from an increase in the average selling price per unit from raw material shortage between Q4/2024 and Q1/2025 while sale volume decreased from lower demand of HORECA customers as a consequence from economic slowdown and lower number of tourists. However, the focus has been strategically shifted to inc

  `MDA_LST_FY2025` · `p004` · SHA f99199936676
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 528 ลบ. เพิ่ม 2.2% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ความเสี่ยงด้านภูมิรัฐศาสตร์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2. Expenses Cost of sales: The Company and its subsidiaries recorded cost of sales ratio for the period at 88.0% (2024: 87.1%). The cost of sales ratio under LST was 91.3% (2024: 91.4%). Subsidiary (UPOIC) recorded cost of sales ratio at 84.6% (2024: 84.9%). The CPO extraction rate increased by 7.5% and CPKO’s extraction rate increased by 2.6%. Subsidiary (UFC) recorded cost of sales ratio at 81.5% (2024: 78.6%). Selling and distribution expenses: The Company and its subsidiaries recorded selling and distribution expenses at Baht 602.6 million (2024: Baht 588.2 million), increasing by Baht 14.4 million. LST’s expenses increased by Baht 42.6 million mainly from warehouse rent, transportation

  `MDA_LST_FY2025` · `p010` · SHA b6641f37a7a4
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 528 ลบ. เพิ่ม 2.2% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > provider’s fire incident. The subsidiaries’ expenses increased by Baht 15.1 million mainly from loss on exchange rate due to the appreciation of Thai Baht. Loss from change in fair value of biological assets: Subsidiary (UPOIC) had loss arising from change in fair value of biological assets Baht 0.6 million (2024: Baht 14.7 million).

  `MDA_LST_FY2025` · `p011` · SHA 420031b888c9
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 528 ลบ. เพิ่ม 2.2% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 3. Profits Gross profit (GP): GP of the Company and its subsidiaries increased by Baht 43.9 million or 2.9%. The Gross profit ratio of total sales was 12.0% (2024: 12.9%). Profit for the year: Profit attributable to equity holders of the Company was Baht 527.9 million (2024: Baht 516.6 million), increasing by Baht 11.3 million or 2.2%.

  `MDA_LST_FY2025` · `p013` · SHA 3347f56e32fe
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > provider’s fire incident. The subsidiaries’ expenses increased by Baht 15.1 million mainly from loss on exchange rate due to the appreciation of Thai Baht. Loss from change in fair value of biological assets: Subsidiary (UPOIC) had loss arising from change in fair value of biological assets Baht 0.6 million (2024: Baht 14.7 million).

  `MDA_LST_FY2025` · `p011` · SHA 420031b888c9
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_LST_FY2025`

##### KBS — บริษัทในกลุ่ม · ติดตาม

**บริษัท น้ำตาลครบุรี จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและจำหน่ายน้ำตาลทราย และธุรกิจที่เกี่ยวกับผลิตภัณฑ์พลอยได้ที่ได้จากการผลิตน้ำตาลทราย ได้แก่ การขายกากน้ำตาล การขายไฟฟ้า

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 3.6bn | 6.00 | +4.3% | 7.2x | 5.6% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 3 · NPAT 7 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 11.9bn → FY2025 THB 10.9bn · −954m · -8.0%

- RFO ปี 2568 อยู่ที่ 10,920 ลบ. ลด 8.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ปริมาณขายและปริมาณการผลิต และ ราคาขายและส่วนผสมผลิตภัณฑ์ และ รายได้และเงื่อนไขของธุรกิจไฟฟ้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > selling price, despite a 14.3% increase in sales volume. 1.3) Gross profit from the utilities segment increased by THB 44 million or 9.7%, compared to the previous year because of the following factors: - The subsidiary's electricity sales revenue to the government sector increased by THB 25 million, or 2.9%, compared to the previous year, driven by a 4.6% increase in electricity sales volume.

  `MDA_KBS_FY2025` · `p009` · SHA d29bd4823c6c
  </details>
- RFO ปี 2568 อยู่ที่ 10,920 ลบ. ลด 8.0% YoY; MD&A ระบุว่า vนงบน NY lE ru yuci yoali primarily due to a 38.8% decline in the average selling price of molasses. - Sales of agricultural products, gasoline, and agricultural services increased by THB 43.7 million, or 5.4% year-on-year, mainly due to the Company providing greater support to farmers through increased sugarcane การส่งเสริมการขาย. - The Company crushed a total of 4.1 million tons of cane in the 2024/25 crop year, an increase of 0.55 million tons, or 15.4%, compared to the 2023/24 crop year. - The final sugarcane price for the 2024/25 crop year was THB 1,163.83
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > vนงบน NY lE ru yuci yoali primarily due to a 38.8% decline in the average selling price of molasses. - Sales of agricultural products, gasoline, and agricultural services increased by THB 43.7 million, or 5.4% year-on-year, mainly due to the Company providing greater support to farmers through increased sugarcane promotion. - The Company crushed a total of 4.1 million tons of cane in the 2024/25 crop year, an increase of 0.55 million tons, or 15.4%, compared to the 2023/24 crop year. - The final sugarcane price for the 2024/25 crop year was THB 1,163.83 per ton of cane at 10 C.C.S., a decrease of THB 261.54 per ton, or 18.3%, from the 2023/24 crop year. 1.2) Gross profit from the molasses an

  `MDA_KBS_FY2025` · `p008` · SHA cc6ab86c1063
  </details>
- RFO ปี 2568 อยู่ที่ 10,920 ลบ. ลด 8.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The change in operating results was as following main factors below: 1) Total gross profit from sales and service revenue (before eliminated from inter-companies) decreased by THB 627.1 million or 27.2%, compared with the previous year. (2024: Gross profit 2,307.5 million) Sales and services revenue and gross profit by a segment of the

  `MDA_KBS_FY2025` · `p002` · SHA f79a5f0e3ab6
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 1.0bn → FY2025 THB 611m · −429m · -41.3%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 611 ลบ. ลด 41.3% YoY; MD&A ระบุว่า vนงบน NY lE ru yuci yoali primarily due to a 38.8% decline in the average selling price of molasses. - Sales of agricultural products, gasoline, and agricultural services increased by THB 43.7 million, or 5.4% year-on-year, mainly due to the Company providing greater support to farmers through increased sugarcane การส่งเสริมการขาย. - The Company crushed a total of 4.1 million tons of cane in the 2024/25 crop year, an increase of 0.55 million tons, or 15.4%, compared to the 2023/24 crop year. - The final sugarcane price for the 2024/25 crop year was THB 1,163.83
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > vนงบน NY lE ru yuci yoali primarily due to a 38.8% decline in the average selling price of molasses. - Sales of agricultural products, gasoline, and agricultural services increased by THB 43.7 million, or 5.4% year-on-year, mainly due to the Company providing greater support to farmers through increased sugarcane promotion. - The Company crushed a total of 4.1 million tons of cane in the 2024/25 crop year, an increase of 0.55 million tons, or 15.4%, compared to the 2023/24 crop year. - The final sugarcane price for the 2024/25 crop year was THB 1,163.83 per ton of cane at 10 C.C.S., a decrease of THB 261.54 per ton, or 18.3%, from the 2023/24 crop year. 1.2) Gross profit from the molasses an

  `MDA_KBS_FY2025` · `p008` · SHA cc6ab86c1063
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 611 ลบ. ลด 41.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าเสื่อมราคาและค่าตัดจำหน่าย และ ต้นทุนทางการเงิน และ การซื้อกิจการและการรวมงบการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > provide an explanation of the operating result for the year 2025. For the year ended 31 December 2025, the Company had consolidated net profit amounting to THB 610.8 million which decreased THB 429.4 million or 41.3% compared with the previous year which net profit of THB 1,040.2 million. The Company had Earning before Finance Costs, Taxes, Depreciation, and Amortization (EBITDA) of THB 1,844.5 million which was decreased by THB 559.5 million or 23.3% from the previous year.

  `MDA_KBS_FY2025` · `p001` · SHA ba601d26707b
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 611 ลบ. ลด 41.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The change in operating results was as following main factors below: 1) Total gross profit from sales and service revenue (before eliminated from inter-companies) decreased by THB 627.1 million or 27.2%, compared with the previous year. (2024: Gross profit 2,307.5 million) Sales and services revenue and gross profit by a segment of the

  `MDA_KBS_FY2025` · `p002` · SHA f79a5f0e3ab6
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 611 ลบ. ลด 41.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ปริมาณขายและปริมาณการผลิต และ ราคาขายและส่วนผสมผลิตภัณฑ์ และ รายได้และเงื่อนไขของธุรกิจไฟฟ้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > selling price, despite a 14.3% increase in sales volume. 1.3) Gross profit from the utilities segment increased by THB 44 million or 9.7%, compared to the previous year because of the following factors: - The subsidiary's electricity sales revenue to the government sector increased by THB 25 million, or 2.9%, compared to the previous year, driven by a 4.6% increase in electricity sales volume.

  `MDA_KBS_FY2025` · `p009` · SHA d29bd4823c6c
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_KBS_FY2025`

##### BRR — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท น้ำตาลบุรีรัมย์ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัทดำเนินธุรกิจลงทุนในบริษัทอื่น (Holding Company) โดยลงทุนในบริษัทย่อยที่ถือหุ้นร้อยละ 99.99 ซึ่งดำเนินธุรกิจจำนวน 6 บริษัท โดยมีธุรกิจหลักเป็นธุรกิจผลิตและจำหน่ายน้ำตาลทราย และอุตสาหกรรมต่อเนื่อง ได้แก่ 1) ธุรกิจผลิตและจำหน่ายน้ำตาลทราย โดยมีบริษัท โรงงานน้ำตาลบุรีรัมย์ จำกัด เป็นบริษัทแกน 2) ธุรกิจผลิตและจำหน่ายไฟฟ้าจากพลังงานชีวมวล โดยบริษัท บุรีรัมย์พลังงาน จำกัด…

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 3.0bn | 3.64 | +0.6% | 26.0x | 4.6% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 7.5bn → FY2025 THB 5.9bn · −1.6bn · -21.2%

- รายได้ลดตามราคาขายน้ำตาลจริงและกิจกรรมที่เกี่ยวข้องกับน้ำตาลที่อ่อนลง ขณะที่ การป้องกันความเสี่ยง ช่วยจำกัดความผันผวน FX
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > pressured by the appreciation of the Thai Baht and a decrease in sugar sales volume 10,745 tons or 4%, consistent with lower sugarcane crushing volume. Additionally, the average selling by-product price decreased by 37%, further reducing total revenue. Nevertheless, proactive foreign exchange risk management strategies helped mitigate the impact of currency fluctuations and stabilize total revenue performance. • Other income totaled THB 223.58 million, decreasing by THB 54.71 million or 19.66% compared with the same period of previous year mainly from declined gain on sale of investment in subsidiary and gain on exchange rate. However, the company recognized revenue of THB 85.25 million from

  `MDA_BRR_FY2025` · `p004` · SHA 8eb7a771a498
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 1.0bn → FY2025 THB 275m · −759m · -73.4%

- กำไรลด 73% เมื่อ อัตรากำไรขั้นต้น ลดเป็น 15.5% จาก 25.8% และบันทึกขาดทุนด้อยค่าสินค้าคงเหลือ 176 ลบ. หลังราคาน้ำตาลโลกลดลง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > TNEDIDEY L LLLI Buriram Sugar Public Company Limited and its subsidiaries ("the Company") hereby disclose consolidated operating results for year 2025 period ended 31 December 2025, which had a net profit of THB 266.43 million, decreased by THB 755.40 million or 73.93% compared with the same period of previous year with details are as follows:

  `MDA_BRR_FY2025` · `p001` · SHA 371ea0194947
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ปริมาณขายและปริมาณการผลิต และ เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > pressured by the appreciation of the Thai Baht and a decrease in sugar sales volume 10,745 tons or 4%, consistent with lower sugarcane crushing volume. Additionally, the average selling by-product price decreased by 37%, further reducing total revenue. Nevertheless, proactive foreign exchange risk management strategies helped mitigate the impact of currency fluctuations and stabilize total revenue performance. • Other income totaled THB 223.58 million, decreasing by THB 54.71 million or 19.66% compared with the same period of previous year mainly from declined gain on sale of investment in subsidiary and gain on exchange rate. However, the company recognized revenue of THB 85.25 million from

  `MDA_BRR_FY2025` · `p004` · SHA 8eb7a771a498
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_BRR_FY2025`

##### TWPC — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ไทยวา จำกัด (มหาชน)** — อยู่ในภาวะฟื้นตัว; อัตราเติบโตมีความสำคัญรองลงมา

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและจําหน่ายผลิตภัณฑ์แป้งและที่เกี่ยวข้อง ผลิตภัณฑ์อาหาร และผลิตภัณฑ์ที่ย่อยสลายได้ตามธรรมชาติ

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 2.5bn | 2.86 | -1.4% | 12.2x | 1.7% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 17 · NPAT 20 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 10.0bn → FY2025 THB 9.2bn · −831m · -8.3%

- RFO ปี 2568 อยู่ที่ 9,206 ลบ. ลด 8.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ปริมาณขายและปริมาณการผลิต และ ต้นทุนทางการเงิน และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > THB 9,205.9 million due to starch market price remains at a cyclical low, the food business grew 7.8% YoY. Administrative expenses declined 15.4%, reflecting the Company's ongoing cost discipline and organizational efficiency. However, selling expenses increased attributed to higher distribution costs corresponding to volume growth. Strong cash from operation, with EBITDA at THB 796.5 million and IBD/E at 0.22x. Cash received from the partnership with Fuji Nihon (Thailand) was allocated to repay high-interest debt, leading to a 42.8% reduction in finance cost to THB 55.7 million in 2025. • Food Business: Sales increased by 7.8% YoY, reaching THB 2,558.4 million from THB 2,372.9 million. This

  `MDA_TWPC_FY2025` · `p009` · SHA ba36c4acf1ed
  </details>
- RFO ปี 2568 อยู่ที่ 9,206 ลบ. ลด 8.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การเปลี่ยนแปลงของอัตรากำไร และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ปริมาณขายและปริมาณการผลิต และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, TWPC recorded another turnaround net profit of THB 155.9 million, compared to a net loss of THB 71.4 million in the previous year. This change was attributed to 7.4% increase in volume, and GPM rise to 21.3%, up from 15.0% in 2024. Though total revenue declined 8.3% to THB 9,205.9 million due to lower tapioca starch market prices, the food business grew 7.8% YoY. Administrative expenses declined 15.4%, reflecting the Company's ongoing cost discipline and organizational efficiency. However, selling expenses increased attributed to higher distribution costs corresponding to volume growth. Strong cash from operation, with EBITDA at THB 796.5 million and IBD/E at 0.22x. Cash received fr

  `MDA_TWPC_FY2025` · `p048` · SHA fef2c2ad2f57
  </details>
- RFO ปี 2568 อยู่ที่ 9,206 ลบ. ลด 8.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ปริมาณขายและปริมาณการผลิต และ ราคาขายและส่วนผสมผลิตภัณฑ์ และ ความเสี่ยงด้านภูมิรัฐศาสตร์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > TWPC demonstrated disciplined management of its Starch business in 2025, delivering volume growth of 11.8% YoY despite a challenging commodity pricing environment. While native starch revenue reflected softer market conditions at THB 3,470.1 million compared to THB 4,145.9 million in 2024, the Company responded proactively by driving volume expansion, optimizing raw material sourcing, and maintaining rigorous cost discipline to protect margins. The Company is actively accelerating its shift toward a larger and higher-value HVA portfolio, where the HVA segment now represents 47% of total starch revenue, up from 45% in the prior year, with volume growth of 1.7% YoY driven by strategic expansio

  `MDA_TWPC_FY2025` · `p053` · SHA 43b87ccaeb6d
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 71m → FY2025 THB 156m · +227m

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 156 ลบ. จากขาดทุน -71.4 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Key ratios (%) Gross profit margin 15.0% 21.3% 6.3% SG&A to net sale ratio 15.6% 18.6% 3.1% EBIT margin 0.3% 3.6% 3.3% EBITDA margin 5.0% 8.7% 3.7% Net profit margin for the period (0.9%) 1.8% 2.6% Net profit margin to the owner of the parent (0.7%) 1.7% 2.4% Core Profit margin from operation (1.6%) 2.1% 3.7% (1) Including net exchange gain (loss) and profit (loss) on fair value of derivatives (2) Excluding non-recurring item from restructuring

  `MDA_TWPC_FY2025` · `p044` · SHA f4fe123ac0c6
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 156 ลบ. จากขาดทุน -71.4 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ การเปลี่ยนแปลงของอัตรากำไร และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross Profit and Gross Profit Margin In 2025, the Company achieved gross profit of THB 1,961.5 million, an increase of 30.1% YoY, lifting GPM to 21.3% from 15.0% in 2024. All segments recorded gross profit margin improvement, driven by a combination of robust volume growth that improved production efficiency and absorption of fixed manufacturing costs, disciplined cost control measures, and efficient raw material management, particularly in the starch business where both raw material costs and production efficiency improved significantly. Favorable product mix and volume gains in the HVA segment and food business further contributed to margin expansion.

  `MDA_TWPC_FY2025` · `p056` · SHA 5219e44b8dda
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 156 ลบ. จากขาดทุน -71.4 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ การเปลี่ยนแปลงของอัตรากำไร และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ปริมาณขายและปริมาณการผลิต และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, TWPC recorded another turnaround net profit of THB 155.9 million, compared to a net loss of THB 71.4 million in the previous year. This change was attributed to 7.4% increase in volume, and GPM rise to 21.3%, up from 15.0% in 2024. Though total revenue declined 8.3% to THB 9,205.9 million due to lower tapioca starch market prices, the food business grew 7.8% YoY. Administrative expenses declined 15.4%, reflecting the Company's ongoing cost discipline and organizational efficiency. However, selling expenses increased attributed to higher distribution costs corresponding to volume growth. Strong cash from operation, with EBITDA at THB 796.5 million and IBD/E at 0.22x. Cash received fr

  `MDA_TWPC_FY2025` · `p048` · SHA fef2c2ad2f57
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 156 ลบ. จากขาดทุน -71.4 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ การเปลี่ยนแปลงของอัตรากำไร และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Key Performance Highlights In 2025, TWPC recorded a turnaround net profit of THB 155.9 million, compared to a net loss of THB 71.4 million in the previous year. This change was attributed to 7.4% increase in volume, and a Gross Profit Margin (GPM) rise to 21.3%, up from 15.0% in 2024, driven by GPM improvement in all businesses from effective cost management and favorable portfolio mix. Though total revenue declined 8.3% to

  `MDA_TWPC_FY2025` · `p008` · SHA ee2db9aa1f8b
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Key ratios (%) Gross profit margin 15.0% 21.3% 6.3% SG&A to net sale ratio 15.6% 18.6% 3.1% EBIT margin 0.3% 3.6% 3.3% EBITDA margin 5.0% 8.7% 3.7% Net profit margin for the period (0.9%) 1.8% 2.6% Net profit margin to the owner of the parent (0.7%) 1.7% 2.4% Core Profit margin from operation (1.6%) 2.1% 3.7% (1) Including net exchange gain (loss) and profit (loss) on fair value of derivatives (2) Excluding non-recurring item from restructuring

  `MDA_TWPC_FY2025` · `p044` · SHA f4fe123ac0c6
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_TWPC_FY2025`

##### CPI — บริษัทในกลุ่ม · ติดตาม

**บริษัท ชุมพรอุตสาหกรรมน้ำมันปาล์ม จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ประกอบธุรกิจผลิตและจำหน่ายผลิตภัณฑ์น้ำมันปาล์ม เช่น น้ำมันปาล์มดิบ น้ำมันเมล็ดในปาล์ม น้ำมันปาล์มบริสุทธิ์ น้ำมันเมล็ดในปาล์มบริสุทธิ์ น้ำมันปาล์มโอเลอินผ่านกรรมวิธีบรรจุขวด ปี๊บและถุง ตรา ?ลีลา? รวมทั้งยังมีผลิตภัณฑ์พลอยได้อื่นๆ เช่น ไขปาล์มบริสุทธิ์ กรดไขมันปาล์ม และกากเมล็ดในปาล์ม เป็นต้น

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 2.2bn | 3.46 | +5.5% | 8.5x | 7.9% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 3 · NPAT 2 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 5.2bn → FY2025 THB 5.3bn · +133m · +2.6%

- RFO ปี 2568 อยู่ที่ 5,326 ลบ. เพิ่ม 2.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2) The cost of sales Baht 4,367.90 million during the Year 2025 decreased by Baht 50.54 million or 1.14% from the previous year due to decrease in the average cost of direct materials, which a result in the percentage of gross profit increased from 14.91% to 17.98%.

  `MDA_CPI_FY2025` · `p004` · SHA 20f60487fa10
  </details>
- RFO ปี 2568 อยู่ที่ 5,326 ลบ. เพิ่ม 2.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ปริมาณขายและปริมาณการผลิต และ ราคาขายและส่วนผสมผลิตภัณฑ์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Financial Performance Analysis 1) The turnover Baht 5,325.53 million during the Year 2025 increased Baht 132.64 million or 2.55% from the previous year. The main reason was the average selling price increased 2.97% but the sales volume of the main products decreased 4.5%.

  `MDA_CPI_FY2025` · `p003` · SHA e38d5b5bda6a
  </details>
- RFO ปี 2568 อยู่ที่ 5,326 ลบ. เพิ่ม 2.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 0.96%. The main reason was increased in sales promotion expenses.

  `MDA_CPI_FY2025` · `p006` · SHA 8ea39777dee6
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 321m → FY2025 THB 418m · +98m · +30.5%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 418 ลบ. เพิ่ม 30.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2) The cost of sales Baht 4,367.90 million during the Year 2025 decreased by Baht 50.54 million or 1.14% from the previous year due to decrease in the average cost of direct materials, which a result in the percentage of gross profit increased from 14.91% to 17.98%.

  `MDA_CPI_FY2025` · `p004` · SHA 20f60487fa10
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 418 ลบ. เพิ่ม 30.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ราคาน้ำมันปาล์ม และ ค่าเสื่อมราคาและค่าตัดจำหน่าย และ การซื้อกิจการและการรวมงบการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Chumporn Palm Oil Industry Public Company Limited would like to report on the performance of the Company and its subsidiaries for the Year 2025. The consolidated financial statement had a net profit of Baht 418.49 million, whereas in the previous year it had a net profit of Baht 320.59 million. The Company and its subsidiaries had earnings before interest, tax and depreciation and amortization expenses for the Year 2025 amounting to Baht 735.59 million, which was increased of Baht 97.90 million when compared with the previous year.

  `MDA_CPI_FY2025` · `p002` · SHA 4ecdde4def76
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_CPI_FY2025`

##### PQS — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท พรีเมียร์ควอลิตี้สตาร์ช จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ธุรกิจผลิตและจำหน่ายแป้งมันสำปะหลัง (Native Starch) แป้งมันสำปะหลังดัดแปร (Modified Starch) และแป้งแปรรูปอื่นๆที่เกี่ยวข้อง รวมถึงการจำหน่ายกระแสไฟฟ้าจากก๊าซชีวภาพ (Biogas)

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.2bn | 1.82 | +23.8% | n.m. | -4.0% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 20 · NPAT 20 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 2.7bn → FY2025 THB 2.0bn · −757m · -27.9%

- RFO ปี 2568 อยู่ที่ 1,953 ลบ. ลด 27.9% YoY; MD&A ระบุว่า สัดส่วนรายได้รวมไตรมาส 4 ปี 2568 บาท เพิ่มขึ้น 10.9% QoQ จาก 462.0 ล้านบาทในไตรมาสก่อน อย่างไรก็ดีลดลง 23.4% YoY จาก 669.3 ล้านบาทในงวดเดียวกันของปีก่อน โดยรายได้จากการ รายได้อื่น, 1.0% ขายสินค้าแป้งมันสำปะหลัง มีมูลค่า 505.7 ล้านบาทในไตรมาส 4/2568 ขยายตัว 10.1% จากไตรมาส 3/2568 ที่มีรายได้ 459.2 ล้านบาท เนื่องจากปริมาณขาย เพิ่มขึ้นจากไตรมาสก่อนกว่า 10.1% ตามปัจจัยฤดูกาล อย่างไรก็ดีเมื่อเทียบกับปี รายได้จากการขายและ ก่อน รายได้จากการขายสินค้าแป้งมันสำปะหลังลดลง 23.5% YoY จาก 661.3 ล้าน บริการ, 99.0%
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > สัดส่วนรายได้รวมไตรมาส 4 ปี 2568 บาท เพิ่มขึ้น 10.9% QoQ จาก 462.0 ล้านบาทในไตรมาสก่อน อย่างไรก็ดีลดลง 23.4% YoY จาก 669.3 ล้านบาทในงวดเดียวกันของปีก่อน โดยรายได้จากการ รายได้อื่น, 1.0% ขายสินค้าแป้งมันสำปะหลัง มีมูลค่า 505.7 ล้านบาทในไตรมาส 4/2568 ขยายตัว 10.1% จากไตรมาส 3/2568 ที่มีรายได้ 459.2 ล้านบาท เนื่องจากปริมาณขาย เพิ่มขึ้นจากไตรมาสก่อนกว่า 10.1% ตามปัจจัยฤดูกาล อย่างไรก็ดีเมื่อเทียบกับปี รายได้จากการขายและ ก่อน รายได้จากการขายสินค้าแป้งมันสำปะหลังลดลง 23.5% YoY จาก 661.3 ล้าน บริการ, 99.0%

  `MDA_PQS_FY2025` · `p051` · SHA 41c2e3c3ba4f
  </details>
- RFO ปี 2568 อยู่ที่ 1,953 ลบ. ลด 27.9% YoY; MD&A ระบุว่า จากรายได้จากการขายแป้งมันสำปะหลัง รายได้จากการขายไฟฟ้าไบโอ ก๊าซ และรายได้จากบริการขนส่งและโลจิสติกส์ โดยเมื่อเทียบกับปีก่อน รายได้อื่น, 2.5% รายได้จากการขายและบริการรวมลดลง 757.2 ล้านบาท หรือลดลง 27.9% YoY โดยรายได้จากการขายแป้งมันสำปะหลังลดลง 761.9 ล้านบาท หรือ ลดลง 28.3% YoY สะท้อนถึงสภาวะตลาดที่ท้าทายจากคำสั่งซื้อจากตลาดจีน รายได้จากการขายและ ที่ลดลงดังที่อธิบายข้างต้น แม้ว่าในปีนี้บริษัทยังสามารถรักษาปริมาณขายได้บริการ, 97.5%
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > จากรายได้จากการขายแป้งมันสำปะหลัง รายได้จากการขายไฟฟ้าไบโอ ก๊าซ และรายได้จากบริการขนส่งและโลจิสติกส์ โดยเมื่อเทียบกับปีก่อน รายได้อื่น, 2.5% รายได้จากการขายและบริการรวมลดลง 757.2 ล้านบาท หรือลดลง 27.9% YoY โดยรายได้จากการขายแป้งมันสำปะหลังลดลง 761.9 ล้านบาท หรือ ลดลง 28.3% YoY สะท้อนถึงสภาวะตลาดที่ท้าทายจากคำสั่งซื้อจากตลาดจีน รายได้จากการขายและ ที่ลดลงดังที่อธิบายข้างต้น แม้ว่าในปีนี้บริษัทยังสามารถรักษาปริมาณขายได้บริการ, 97.5%

  `MDA_PQS_FY2025` · `p036` · SHA 1135117c2171
  </details>
- RFO ปี 2568 อยู่ที่ 1,953 ลบ. ลด 27.9% YoY; MD&A ระบุว่า รายได้อื่น รายได้อื่นส่วนใหญ่เป็นรายได้จากการขายผลพลอยได้ที่เหลือจากการผลิตแป้งสำปะหลัง เช่น กากมัน เหง้ามัน เปลือกดิน เปลือกล้าง น้ำเสีย ดอกเบี้ยรับ และเงินสนับสนุนจากหน่วยงานราชการ เป็นต้น รายได้อื่นในปี 2568 มีมูลค่า 38.6 ล้านบาท แทบไม่เปลี่ยนแปลง จากปี 2567 ซึ่งมีรายได้อื่น 38.7 ล้านบาท หรือลดลงเพียง 0.1% YoY สาเหตุจากรายได้จากการขายผลพลอยได้ที่ใกล้เคียงกับปีก่อน
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้อื่น รายได้อื่นส่วนใหญ่เป็นรายได้จากการขายผลพลอยได้ที่เหลือจากการผลิตแป้งสำปะหลัง เช่น กากมัน เหง้ามัน เปลือกดิน เปลือกล้าง น้ำเสีย ดอกเบี้ยรับ และเงินสนับสนุนจากหน่วยงานราชการ เป็นต้น รายได้อื่นในปี 2568 มีมูลค่า 38.6 ล้านบาท แทบไม่เปลี่ยนแปลง จากปี 2567 ซึ่งมีรายได้อื่น 38.7 ล้านบาท หรือลดลงเพียง 0.1% YoY สาเหตุจากรายได้จากการขายผลพลอยได้ที่ใกล้เคียงกับปีก่อน

  `MDA_PQS_FY2025` · `p040` · SHA 47fda6271345
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 241m → FY2025 −THB 79m · −320m

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -79.1 ลบ. จากกำไร 241 ลบ.; MD&A ระบุว่า เนื่องจากราคาขายที่ปรับตัวขึ้นมาอยู่ในระดับที่เหมาะสม ต้นทุนขายและบริการ ต้นทุนขายและบริการในไตรมาส 4/2568 อยู่ที่ 468.7 ล้านบาท ลดลง 11.2% จากไตรมาส 4/2567 ที่มีต้นทุน 527.9 ล้านบาท ตามรายได้ที่ลดลง อย่างไรก็ดีต้นทุนขายและบริการเพิ่มขึ้นเพียงเล็กน้อย 0.3% QoQ เมื่อเทียบกับไตรมาสก่อนซึ่งมี ต้นทุน 467.3 ล้านบาท เนื่องจากต้นทุนส่วนใหญ่เป็นต้นทุนคงที่ทำให้ต้นทุนไม่ได้เพิ่มตามรายได้ที่เพิ่มขึ้นมากนัก ส่งผล ให้กำไรขั้นต้นในไตรมาส 4/2568 กลับมาเป็นบวกที่ 43.7 ล้านบาท และมีอัตรากำไรขั้นต้นอยู่ที่ 8.5% ซึ่งเป็นการปรับตัวดีขึ้น อย่างมากจากไตรมาสก่อนที่มีผลขาดทุนข
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > เนื่องจากราคาขายที่ปรับตัวขึ้นมาอยู่ในระดับที่เหมาะสม ต้นทุนขายและบริการ ต้นทุนขายและบริการในไตรมาส 4/2568 อยู่ที่ 468.7 ล้านบาท ลดลง 11.2% จากไตรมาส 4/2567 ที่มีต้นทุน 527.9 ล้านบาท ตามรายได้ที่ลดลง อย่างไรก็ดีต้นทุนขายและบริการเพิ่มขึ้นเพียงเล็กน้อย 0.3% QoQ เมื่อเทียบกับไตรมาสก่อนซึ่งมี ต้นทุน 467.3 ล้านบาท เนื่องจากต้นทุนส่วนใหญ่เป็นต้นทุนคงที่ทำให้ต้นทุนไม่ได้เพิ่มตามรายได้ที่เพิ่มขึ้นมากนัก ส่งผล ให้กำไรขั้นต้นในไตรมาส 4/2568 กลับมาเป็นบวกที่ 43.7 ล้านบาท และมีอัตรากำไรขั้นต้นอยู่ที่ 8.5% ซึ่งเป็นการปรับตัวดีขึ้น อย่างมากจากไตรมาสก่อนที่มีผลขาดทุนขั้นต้น 5.2 ล้านบาท ทั้งนี้เนื่องจากปัจจัยฤดูกาลที่ทำให้รายได้เพิ่มขึ้นจนถึงระดับที่สูงกว่า จุดคุ้มทุน ประกอบกับการควบคุมต้นทุนได้อย่างมีประส

  `MDA_PQS_FY2025` · `p054` · SHA c87c5d8c8ee4
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -79.1 ลบ. จากกำไร 241 ลบ.; MD&A ระบุว่า กำไร (ขาดทุน) ขั้นต้น และอัตรากำไร (ขาดทุน) ขั้นต้น กำไรขั้นต้นในปี 2568 อยู่ที่ 226.9 ล้านบาท ลดลงจากปี 2567 ซึ่งมีกำไรขั้นต้น 561.4 ล้านบาท หรือลดลง 59.6% YoY ตามรายได้ที่ ลดลง ในด้านอัตรากำไรขั้นต้น ปี 2568 อยู่ที่ 11.6% ลดลงจากปี 2567 ซึ่งมีอัตรากำไรขั้นต้น 20.7% สาเหตุจากในปี 2568 บริษัท มีต้นทุนคงที่เพิ่มขึ้น ทำให้ภาพรวมต้นทุนไม่ลดลงเป็นสัดส่วนเดียวกับรายได้ที่ลดลง อย่างไรก็ดีแม้จะเผชิญกับความผันผวนของตลาด ในปีนี้บริษัทยังคงสามารถสร้างกำไรขั้นต้นและมีอัตรากำไรขั้นต้นในระดับบวก บริษัทมีความมั่นใจในพื้นฐานในการดำเนินงานที่ยังคง สร้างมูลค่าได้เมื่อตลา
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไร (ขาดทุน) ขั้นต้น และอัตรากำไร (ขาดทุน) ขั้นต้น กำไรขั้นต้นในปี 2568 อยู่ที่ 226.9 ล้านบาท ลดลงจากปี 2567 ซึ่งมีกำไรขั้นต้น 561.4 ล้านบาท หรือลดลง 59.6% YoY ตามรายได้ที่ ลดลง ในด้านอัตรากำไรขั้นต้น ปี 2568 อยู่ที่ 11.6% ลดลงจากปี 2567 ซึ่งมีอัตรากำไรขั้นต้น 20.7% สาเหตุจากในปี 2568 บริษัท มีต้นทุนคงที่เพิ่มขึ้น ทำให้ภาพรวมต้นทุนไม่ลดลงเป็นสัดส่วนเดียวกับรายได้ที่ลดลง อย่างไรก็ดีแม้จะเผชิญกับความผันผวนของตลาด ในปีนี้บริษัทยังคงสามารถสร้างกำไรขั้นต้นและมีอัตรากำไรขั้นต้นในระดับบวก บริษัทมีความมั่นใจในพื้นฐานในการดำเนินงานที่ยังคง สร้างมูลค่าได้เมื่อตลาดฟื้นตัว โดยบริษัทยังคงมุ่งเน้นการขายสินค้าใหม่เพื่อเพิ่มยอดขาย และปรับปรุงประสิทธิภาพการผลิตเพื่อ

  `MDA_PQS_FY2025` · `p043` · SHA ec8675a52906
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -79.1 ลบ. จากกำไร 241 ลบ.; MD&A ระบุว่า กำไร (ขาดทุน) สุทธิและอัตรากำไร (ขาดทุน) สุทธิ ในปี 2568 บริษัทมีผลขาดสุทธิ 79.1 ล้านบาท เมื่อเทียบกับปี 2567 ที่มีกำไรสุทธิ 231.3 ล้านบาท โดยมีอัตราขาดทุนสุทธิในปีนี้อยู่ที่ - 4.0% ซึ่งลดลงจากปี 2567 ที่มีอัตรากำไรสุทธิ 8.4% การขาดทุนนี้เป็นผลจากแรงกดดันด้านรายได้หลักที่ลดลงอย่างมากจากปัจจัยตลาดภายนอกซึ่งเป็นปัจจัยชั่วคราว อย่างไรก็ตาม การ ขาดทุนนี้เกิดขึ้นในสภาวะเฉพาะกิจและบริษัทยังคงมีฐานะการเงินที่มั่นคงและความสามารถในการสร้างกระแสเงินสด ฝ่ายบริหาร ตระหนักถึงสถานการณ์นี้ดีและได้เตรียมพร้อมมาตรการปรับตัวที่ชัดเจนโดยเตรียมโครงสร้างพื้นฐานสำหรับแหล่งราย
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไร (ขาดทุน) สุทธิและอัตรากำไร (ขาดทุน) สุทธิ ในปี 2568 บริษัทมีผลขาดสุทธิ 79.1 ล้านบาท เมื่อเทียบกับปี 2567 ที่มีกำไรสุทธิ 231.3 ล้านบาท โดยมีอัตราขาดทุนสุทธิในปีนี้อยู่ที่ - 4.0% ซึ่งลดลงจากปี 2567 ที่มีอัตรากำไรสุทธิ 8.4% การขาดทุนนี้เป็นผลจากแรงกดดันด้านรายได้หลักที่ลดลงอย่างมากจากปัจจัยตลาดภายนอกซึ่งเป็นปัจจัยชั่วคราว อย่างไรก็ตาม การ ขาดทุนนี้เกิดขึ้นในสภาวะเฉพาะกิจและบริษัทยังคงมีฐานะการเงินที่มั่นคงและความสามารถในการสร้างกระแสเงินสด ฝ่ายบริหาร ตระหนักถึงสถานการณ์นี้ดีและได้เตรียมพร้อมมาตรการปรับตัวที่ชัดเจนโดยเตรียมโครงสร้างพื้นฐานสำหรับแหล่งรายได้ใหม่เรียบร้อย แล้ว คือ โรงงานงานผลิตแป้งมันสำปะหลังดัดแปรซึ่งมีฐานลูกค้าที่กว้างขึ้น และแป้งมันสำปะหลังคาร์บอนต่ำซึ่งเป็นสินค้าที่อยู่ในค

  `MDA_PQS_FY2025` · `p049` · SHA 47cefb484d35
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -79.1 ลบ. จากกำไร 241 ลบ.; MD&A ระบุว่า ปี 2567 ปี 2568 ปี 2568 กำไรก่อนดอกเบี้ยจ่าย ภาษีค่าเสื่อม 74.5 (28.6) 19.8 169.2% (73.5%) 373.9 121.7 (67.5%) อัตรากำไร EBITDA (%) 11.1% (6.0%) 3.8% 9.8 ppts (7.2 ppts) 13.6% 6.1% (7.5 ppts) กำไรก่อนดอกเบี้ยจ่าย และภาษี 36.8 (74.0) (26.6) 64.0% (172.4%) 260.7 (55.0) (121.1%) อัตรากำไร EBIT (%) 5.5% (15.5%) (5.1%) 10.4 ppts (10.6 ppts) 9.5% (2.7%) (12.2 ppts) กำไร (ขาดทุน) สุทธิ (ล้านบาท) 34.9 (78.3) (32.2) 58.8% (192.5%) 231.3 (79.1) (134.2%) อัตรากำไรสุทธิ (%) 5.2% (16.4%) (6.2%) 10.2 ppts (11.4 ppts) 8.4% (4.0%) (12.4 ppts) กำไรสุทธิต่อหุ้น (บาท) 0.05
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ปี 2567 ปี 2568 ปี 2568 กำไรก่อนดอกเบี้ยจ่าย ภาษีค่าเสื่อม 74.5 (28.6) 19.8 169.2% (73.5%) 373.9 121.7 (67.5%) อัตรากำไร EBITDA (%) 11.1% (6.0%) 3.8% 9.8 ppts (7.2 ppts) 13.6% 6.1% (7.5 ppts) กำไรก่อนดอกเบี้ยจ่าย และภาษี 36.8 (74.0) (26.6) 64.0% (172.4%) 260.7 (55.0) (121.1%) อัตรากำไร EBIT (%) 5.5% (15.5%) (5.1%) 10.4 ppts (10.6 ppts) 9.5% (2.7%) (12.2 ppts) กำไร (ขาดทุน) สุทธิ (ล้านบาท) 34.9 (78.3) (32.2) 58.8% (192.5%) 231.3 (79.1) (134.2%) อัตรากำไรสุทธิ (%) 5.2% (16.4%) (6.2%) 10.2 ppts (11.4 ppts) 8.4% (4.0%) (12.4 ppts) กำไรสุทธิต่อหุ้น (บาท) 0.052 (0.117) (0.048) 58.8% (192.5%) 0.345 (0.118) (134.2%)

  `MDA_PQS_FY2025` · `p057` · SHA cb78226c787d
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไร (ขาดทุน) จากการวัดมูลค่ายุติธรรมตราสารอนุพันธ์ (4.1) 2.5 (4.0) (261.0%) 1.9% (16.4) 10.7 164.8%
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไร (ขาดทุน) จากการวัดมูลค่ายุติธรรมตราสารอนุพันธ์ (4.1) 2.5 (4.0) (261.0%) 1.9% (16.4) 10.7 164.8%

  `MDA_PQS_FY2025` · `p032` · SHA e7e087493eb8
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_PQS_FY2025`

#### ทะเบียนข้อสรุป — F8

| ส่วน | ประเภท | ข้อสรุป | รหัสแหล่งข้อมูล |
|---|---|---|---|
| headline | ข้ออนุมานนักวิเคราะห์ | งวดปฏิทินอ่อนตัว และมุมทุกปีบัญชีแย่กว่าชัดเจน | FY_PANEL, F8_E1, F8_E2, F8_E3, F8_E4 |
| earnings_fact | ข้อเท็จจริงจากการคำนวณ | FY2025 RFO -7.0%; สถานะ NPAT ส่วนผู้ถือหุ้น: profit_decreased | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | กลุ่มปิดงบธันวาคม: RFO -7.0% และ NPAT ส่วนผู้ถือหุ้น -21.0% ครอบคลุม 7/9 บริษัท | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | มุมทุกปีบัญชี: RFO -5.2% และ NPAT -60.0%; ผสมรอบปิดงบ 30 ก.ย., 31 ต.ค. และ 31 ธ.ค. จึงแสดงแยก | FY_PANEL, KSL_FY2025_MDA, KTIS_FY2025_MDA |
| why | ข้อเท็จจริงจากการคำนวณ | TVO เป็นตัวฉุดรายได้ และ KSL เป็นตัวฉุดกำไรในมุมทุกปีบัญชี | FY_PANEL, KSL_FY2025_MDA, KTIS_FY2025_MDA |
| causal_chain | ข้ออนุมานนักวิเคราะห์ | ห่วงโซ่เหตุ: ราคาสินค้าโภคภัณฑ์ → ส่วนต่างผลิต → สินค้าคงคลัง → Margin → NPAT | F8_E1, F8_E2, F8_E3, F8_E4 |
| roles | ข้ออนุมานนักวิเคราะห์ | บทบาท: ผู้นำและตัวฉุดรายได้ — TVO; ตัวฉุดกำไรมุมทุกปีบัญชี — KSL | FY_PANEL, F8_E1, F8_E2, F8_E3, F8_E4 |
| valuation | ข้ออนุมานนักวิเคราะห์ | P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 9.8x ครอบคลุม 6/9 บริษัท และ 71.8% ของ market cap ที่มีข้อมูล. multiple ของกลุ่มผู้มีกำไรสะท้อนวัฏจักรสินค้าโภคภัณฑ์ที่แตกต่าง ส่วน KSL เพิ่มความเสี่ยงด้าน leverage คดีความ และ refinancing แยกต่างหาก โดย KSL ไม่อยู่ในชุดบริษัทที่ใช้คำนวณ P/E | SET_PUBLIC_EOD, F8_E1, F8_E2, F8_E3, F8_E4 |
| trigger | ประเด็นที่ต้องพิสูจน์ | crush margin ถั่วเหลืองและ bridge inventory/NRV ของ TVO ดีขึ้น | F8_E1, F8_E2, F8_E3, F8_E4 |
| trigger | ประเด็นที่ต้องพิสูจน์ | ปริมาณอ้อยและราคาขายน้ำตาลจริงของ KSL/KTIS ดีขึ้น | F8_E1, F8_E2, F8_E3, F8_E4 |
| trigger | ประเด็นที่ต้องพิสูจน์ | กระแสเงินสดดำเนินงานรายบริษัทครอบคลุมภาระหนี้ | F8_E1, F8_E2, F8_E3, F8_E4 |
| risk | ประเด็นที่ต้องพิสูจน์ | ราคาวัตถุดิบและผลิตภัณฑ์ถั่วเหลืองของ TVO ไม่สอดคล้อง | F8_E1, F8_E2, F8_E3, F8_E4 |
| risk | ประเด็นที่ต้องพิสูจน์ | ราคาน้ำตาลลดลง สภาพอากาศ และปริมาณอ้อยผันผวนที่ KSL/KTIS | F8_E1, F8_E2, F8_E3, F8_E4 |
| risk | ประเด็นที่ต้องพิสูจน์ | ความเสี่ยงเฉพาะ KSL ด้าน leverage คดีความ และ refinancing | F8_E1, F8_E2, F8_E3, F8_E4 |
| must_prove | ประเด็นที่ต้องพิสูจน์ | 6M26 ต้อง bridge แยก TVO ด้าน crush/NRV และ KSL/KTIS ด้านปริมาณอ้อย ราคาน้ำตาลจริง hedging ด้อยค่า และการชำระหนี้ | F8_E1, F8_E2, F8_E3, F8_E4 |

#### ทะเบียนหลักฐาน — F8

- **`FY_PANEL`** · _ข้อเท็จจริงจากการคำนวณ_ — Audited FY2024-25 company panel
  - RFO / NPAT-to-owners / independent panel membership; QA 43 pass / 0 fail
  - บทบาท: historical fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_company_fy2024_2025_audited_2026-08-07.csv`
  - SHA-256: `e5e04dbc40ffcc79fed58545a93dc4549c29cdaecf260bea73711bc6d0720481`
- **`SET_PUBLIC_EOD`** · _ข้อเท็จจริงจากการคำนวณ_ — SET public Company Highlights — EOD 2026-08-07
  - Adjusted YTD; unadjusted price, market cap and valuation; factsheet-surface cross-check
  - บทบาท: current market fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_set_public_surface_reconciliation_2026-08-07.csv`
  - SHA-256: `544c1f29fe2d409ee398822ac2bf32b769081718962ae2d1138985b0146b9530`
- **`SET_COMPANY_PROFILE`** · _ข้อเท็จจริง_ — SET company profiles — English and Thai
  - Official company names and business descriptions refreshed and validated for the 118-company perimeter from the public SET profile API
  - บทบาท: company business profile
  - URL: <https://www.set.or.th/th/market/product/stock/overview>
- **`COMPANY_REPORTS`** · _ข้ออนุมานนักวิเคราะห์_ — Company report synthesis corpus
  - Annual-only draft synthesis; reconciled to the ticker FY2025 MD&A where available
  - บทบาท: secondary synthesis; not management attribution
  - พาธ: `data/company-reports.json`
  - SHA-256: `c1a2bc40cbe21a2058aa596c362e4d47ad117360831b847de78ec414831fd2d2`
- **`MDA_TVO_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — TVO FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/TVO/MDA_TVO_2025FY_E.md`
  - SHA-256: `635a8f9baa994b06239858cd0e3a28d79348bfc58882346a90d3539ff51f8912`
  - URL: <https://weblink.set.or.th/dat/news/202602/0209NWS270220261950134700E.pdf>
- **`MDA_KSL_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — KSL FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/KSL/MDA_KSL_2025FY_T.md`
  - SHA-256: `96b12c18ce3011df256f91ab06627f5fa4647988abf98c21106fba53e785bae7`
  - URL: <https://weblink.set.or.th/dat/news/202512/0828NWS191220252050318610T.pdf>
- **`MDA_KTIS_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — KTIS FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/KTIS/MDA_KTIS_2025FY_T.md`
  - SHA-256: `d1d5d7b21687a514036b8f2128e3caf5a220e7b4aa13f31d0c9f7be2364178d0`
  - URL: <https://weblink.set.or.th/dat/news/202511/1149NWS281120252051060920T.pdf>
- **`MDA_LST_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — LST FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/LST/MDA_LST_2025FY_E.md`
  - SHA-256: `fb6fb0c54f4c9cd29756ea8c8c486285c046ceacead860a7615e90b681c1e504`
  - URL: <https://weblink.set.or.th/dat/news/202602/0574NWS230220261703114820E.pdf>
- **`MDA_KBS_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — KBS FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/KBS/MDA_KBS_2025FY_E.md`
  - SHA-256: `ab1578c03a9d775e20e0eb7de98541a0d8bf0a0d22cb6e047453ae4c628f4299`
  - URL: <https://weblink.set.or.th/dat/news/202602/1061NWS230220261823241270E.pdf>
- **`MDA_BRR_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — BRR FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/BRR/MDA_BRR_2025FY_E.md`
  - SHA-256: `70b7ce0c7b9b9a2d231217c73d08f8b88fb667256e042c83db61e91c2920c9ec`
  - URL: <https://weblink.set.or.th/dat/news/202602/1224NWS260220261711067010E.pdf>
- **`MDA_TWPC_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — TWPC FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/TWPC/MDA_TWPC_2025FY_E.md`
  - SHA-256: `ddb4afbb9c6eb188c562b91f60c7d6fbb10b57d3598df97cc82b831008eb1dc6`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/1286NWS240220261848436670E.pdf>
- **`MDA_CPI_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — CPI FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/CPI/MDA_CPI_2025FY_E.md`
  - SHA-256: `688bc4d333b4e112a57b55e34a6bf6be63071dd0cd6a1b58fd11d893b3331dee`
  - URL: <https://weblink.set.or.th/dat/news/202602/0389NWS270220261705010630E.pdf>
- **`MDA_PQS_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — PQS FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/PQS/MDA_PQS_2025FY_T.md`
  - SHA-256: `edbec201c88c9be7edb7852eebabe25877e835f38fadb562a46c70a37cdfbd82`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/1749NWS270220261830218320T.pdf>
- **`KSL_FY2025_MDA`** · _คำอธิบายฝ่ายจัดการ_ — KSL FY2025 filing / MD&A
  - Direct filing evidence for explicitly labelled RFO or NPAT override values
  - บทบาท: override value evidence
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/KSL/MDA_KSL_2025FY_T.md`
  - SHA-256: `96b12c18ce3011df256f91ab06627f5fa4647988abf98c21106fba53e785bae7`
- **`KTIS_FY2025_MDA`** · _คำอธิบายฝ่ายจัดการ_ — KTIS FY2025 filing / MD&A
  - Direct filing evidence for explicitly labelled RFO or NPAT override values
  - บทบาท: override value evidence
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/KTIS/MDA_KTIS_2025FY_T.md`
  - SHA-256: `d1d5d7b21687a514036b8f2128e3caf5a220e7b4aa13f31d0c9f7be2364178d0`
- **`F8_E1`** · _ฝ่ายจัดการ_ — TVO FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/TVO/MDA_TVO_2025FY_E.md`
  - SHA-256: `635a8f9baa994b06239858cd0e3a28d79348bfc58882346a90d3539ff51f8912`
- **`F8_E2`** · _ฝ่ายจัดการ_ — KSL FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/KSL/MDA_KSL_2025FY_T.md`
  - SHA-256: `96b12c18ce3011df256f91ab06627f5fa4647988abf98c21106fba53e785bae7`
- **`F8_E3`** · _ฝ่ายจัดการ_ — KTIS FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/KTIS/MDA_KTIS_2025FY_T.md`
  - SHA-256: `d1d5d7b21687a514036b8f2128e3caf5a220e7b4aa13f31d0c9f7be2364178d0`
- **`F8_E4`** · _บทวิเคราะห์เครดิต_ — TRIS KSL credit analysis
  - Historical explanation or forward cross-check; see source role
  - บทบาท: forward/credit context
  - พาธ: `Listed Company/1-Raw/06-Market Reference/Credit Rating Research/2025/FOOD/TRIS_KSL_149-2025.md`
  - SHA-256: `6983df783e9b86efc2e8243a2fa42178c37beb6c0a578a8dba1b7a049ee4dff0`
- **`F8_FACTSHEET`** · _ข้อเท็จจริงจากการคำนวณ_ — SET Factsheet — TVO
  - Live leader cross-check
  - บทบาท: presentation-surface check
  - URL: <https://www.set.or.th/th/market/product/stock/quote/tvo/factsheet>

### F5 · ร้านอาหารและบริการอาหาร — อุปสงค์ร้านอาหารอ่อนแอ และกำไรส่วนผู้ถือหุ้นของกลุ่มที่ map แล้วลดเร็วกกว่า RFO

`ยังถูกกดดัน` · 3.6% M-cap · THB 29.2bn · 6 บริษัท

| ตัวชี้วัด | RFO | NPAT | ราคา | P/E |
|---|---|---|---|---|
| ช่วง | FY2025 YoY | ส่วนผู้ถือหุ้น FY2025 YoY | ราคา YTD ปรับแล้ว | เฉพาะบริษัทที่มีกำไร |
| ค่า | -4.2% | -76.6% | +6.2% | 23.6x |
| จำนวน | THB 28.9bn FY2025 | THB 189m FY2025 | ณ 7 ส.ค. 2569 | ค่าเฉลี่ยรวม |
| ครอบคลุม | 5/6 | 6/6 | 6/6 • 100% M-cap | 3/6 • 89% M-cap |

**ข้อเท็จจริงที่สังเกตได้** — FY2025: RFO -4.2% • NPAT -76.6% • ราคา YTD +6.2% • P/E 23.6x • ครอบคลุม RFO 5/6 • NPAT 6/6

#### เหตุผลที่เปลี่ยน

1. _ข้อเท็จจริงจากการคำนวณ_ · Traffic — RFO ที่เทียบได้ 5 บริษัทลด 4.2%; AQUA ไม่มี RFO เทียบเคียงและไม่ใช้รายได้รวมแทน
2. _ข้อเท็จจริงจากการคำนวณ_ · Ticket size — NPAT ส่วนผู้ถือหุ้นของทั้ง 6 บริษัทลด 76.6% รวมขาดทุนของ AQUA
3. _คำอธิบายฝ่ายจัดการ_ · SSSG — M ระบุกำลังซื้ออ่อนและ same-store sales ติดลบ ขณะที่ OKJ เป็นตัวเทียบด้านการเติบโต

#### ห่วงโซ่เหตุและผล

**Traffic** → **Ticket size** → **SSSG** → **Store margin** (4.4% -1.6 ppt YoY) → **NPAT** (-76.6% THB 189m FY2025)

#### บทบาทในกลุ่ม

| บทบาท | Ticker | ค่า | ที่มาของค่า |
|---|---|---|---|
| ผู้นำและตัวฉุดกำไร | M | 67% | สัดส่วน Market Cap ในกลุ่ม |
| ตัวเทียบการเติบโต | OKJ | n.m. | P/E · YTD -16.8% |
| ตัวแปรขาดทุน | AQUA | ขาดทุนเพิ่มขึ้น | NPAT YoY · Δ −94m |

#### มูลค่า

**แรงกดดันปัจจุบัน / ข้อเท็จจริง** — P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 23.6x ครอบคลุม 3/6 บริษัท และ 88.7% ของ market cap ที่มีข้อมูล. multiple ให้ค่ากับ turnaround ขณะที่กำไรปัจจุบันยังอ่อน

| Trigger | Risk |
|---|---|
| SSSG กลับมาเป็นบวก | กำลังซื้ออ่อนต่อเนื่อง |
| traffic ดีขึ้นโดยไม่เสีย margin จากส่วนลด | โปรโมชั่นกด margin |
| productivity ต่อสาขาดีขึ้น | ขยายสาขาเร็วกว่าความต้องการ |

**6M26 ต้องพิสูจน์** — 6M26 ต้องเห็น SSSG และ store EBITDA ของธุรกิจร้านอาหารหลักเป็นบวก พร้อม bridge แยกของ AQUA สำหรับขาดทุนบริษัทร่วม ด้อยค่า และกระแสเงินสดดำเนินงาน

#### วิเคราะห์รายบริษัท — F5 ร้านอาหารและบริการอาหาร

_ทุกบริษัทใน perimeter ของ Segment ที่สอบทาน_

| Ticker | บทบาท | M-cap | RFO YoY | NPAT YoY | ราคา YTD | P/E | Margin |
|---|---|---|---|---|---|---|---|
| M | ผู้นำและตัวฉุดกำไร | THB 19.7bn | -2.0% | -41.9% | +17.6% | 25.2x | 5.5% |
| SNP | บริษัทในกลุ่ม | THB 4.5bn | -8.1% | -36.6% | -9.7% | 16.9x | 4.8% |
| OKJ | ตัวเทียบการเติบโต | THB 2.0bn | +12.6% | -65.1% | -16.8% | n.m. | 2.6% |
| ZEN | บริษัทในกลุ่ม | THB 1.7bn | -2.9% | -19.4% | -8.2% | 34.3x | 1.2% |
| MADAME | บริษัทในกลุ่ม | THB 670m | -30.4% | กลับเป็นกำไร | +18.6% | n.m. | 3.1% |
| AQUA | ตัวแปรขาดทุน | THB 571m | — | ขาดทุนเพิ่มขึ้น | -33.3% | n.m. | — |

##### M — ผู้นำและตัวฉุดกำไร · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เอ็มเค เรสโตรองต์ กรุ๊ป จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ประกอบธุรกิจร้านอาหาร "เอ็ม เค สุกี้" "ร้านโบนัส สุกี้" ร้านอาหารญี่ปุ่น "ยาโยอิ" และ "ฮิคินิคุ โตะ โคเมะ" ซึ่งได้รับสิทธิแฟรนไชส์จากประเทศญี่ปุ่น รวมถึงร้านอาหารญี่ปุ่นแบรนด์อื่นๆ อีก 2 แบรนด์ ได้แก่ "ฮากาตะ" และ "มิยาซากิ" ร้านอาหารไทย "แหลมเจริญ ซีฟู้ด" "ณ สยาม" และ "เลอสยาม" ร้านกาแฟ/เบเกอรี่ "เลอ เพอทิท"

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 19.7bn | 21.40 | +17.6% | 25.2x | 5.5% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 15.4bn → FY2025 THB 15.1bn · −309m · -2.0%

- รายได้ลด 2.5% และ SSSG ลด 2.8% จากกำลังซื้ออ่อน แม้มีแคมเปญบุฟเฟต์ 299 บาทและการขยาย Bonus Suki
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > revenues from sales and services. The same-store sales growth also declined by 2.8% compared to the previous

  `MDA_M_FY2025` · `p014` · SHA 95029af0dac8
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 1.4bn → FY2025 THB 838m · −604m · -41.9%

- กำไรลด 41.9% เมื่อ อัตรากำไรขั้นต้น ลดเป็น 64.6% จาก 67.4%; รูปแบบบุฟเฟต์ราคาคุ้มค่ามี ต้นทุนอาหาร สูงขึ้น ขณะที่การแข่งขันจำกัดการส่งผ่านต้นทุนไปยังราคา
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > included the cost of raw materials, transportation and warehousing costs. For the year 2025, gross profit of the Company and its subsidiaries amounted to Baht 9,766 million, a decrease of 6.0% compared to the previous year. As a result, the gross profit margin declined from 67.4% in 2024 to 64.6% for this year due mainly to the MK Buffet “Koom Gern Koom” promotion launched in June 2025 as well as the launch of “Bonus Suki” brand, a full buffet model, with the continuous expansion. These led to an increase in raw material costs relative to sales, reflecting the cost structure

  `MDA_M_FY2025` · `p024` · SHA d1e1232b6c65
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_M_FY2025`

##### SNP — บริษัทในกลุ่ม · ติดตาม

**บริษัท เอส แอนด์ พี ซินดิเคท จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ธุรกิจร้านอาหารและร้านเบเกอรี รวมทั้งจำหน่ายผลิตภัณฑ์ แบ่งเป็น 1) ร้านอาหารและร้านเบเกอรีในประเทศ 2) ร้านอาหาร ในต่างประเทศ 3) ผลิตและจำหน่ายสินค้าเบเกอรี อาหารสำเร็จรูปแช่แข็ง ผ่านสาขาร้านอาหารและเบเกอรี่ และซุปเปอร์มาร์เก็ต รวมทั้งส่งสินค้าออกไปต่างประเทศ 4)ให้บริการที่เกี่ยวเนื่องอื่นๆ เช่น บริการจัดส่งอาหารถึงบ้าน และบริการรับจัดเลี้ยงนอกสถานที่

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 4.5bn | 8.80 | -9.7% | 16.9x | 4.8% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 10 · NPAT 9 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 6.1bn → FY2025 THB 5.6bn · −497m · -8.1%

- RFO ปี 2568 อยู่ที่ 5,642 ลบ. ลด 8.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อุปสงค์และกำลังซื้อในประเทศ และ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Domestic Stores Retail and Food Service International Stores Revenue: In 4Q25, revenue amounted to 1,519 million Baht, representing a 7% decrease year-on-year. The main3M contributing factors were as follows: • Domestic Restaurants: Revenue decreased by 58 million Baht compared to the previous year, primarily due to lower takeaway sales, particularly from branches located in shopping malls and hypermarkets. This was a result of the economic slowdown and intense competition in the food and bakery industry. • Retail and Food Service: Revenue decreased by 22 million Baht compared to the previous year, primarily due to lower sales in retail channels, particularly from reduced cookie sales. • Ove

  `MDA_SNP_FY2025` · `p019` · SHA b91937d5499f
  </details>
- RFO ปี 2568 อยู่ที่ 5,642 ลบ. ลด 8.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อุปสงค์และกำลังซื้อในประเทศ และ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > FY The key contributing factors were as follows: • Domestic Restaurants: Revenue decreased by 407 million Baht compared to the previous year. The decline was mainly caused by lower takeaway sales (-9%), dine-in sales (-6%), and food delivery services (-5%). This was impacted by the economic slowdown and weakened purchasing power, a decline in tourist arrivals, intense competition in the food industry, and the closure of four Maisen branches due to the expiration of their lease contracts. • Retail and OEM Business: Revenue decreased by 13 million Baht compared to the previous year, primarily due to lower sales in retail channels, particularly from mooncake products, as well as lower sales in

  `MDA_SNP_FY2025` · `p020` · SHA 0ff33a5d1223
  </details>
- RFO ปี 2568 อยู่ที่ 5,642 ลบ. ลด 8.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อุปสงค์และกำลังซื้อในประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Profit – share of the owners 127 107 (20) 427 271 (156) Net Profit Margin (%) 7.3% 7.0% (0.3%) 7.0% 4.8% (2.2%) Revenue: The Company reported revenue of 1,519 million Baht in 4Q25 and total revenue of 5,642 million Baht for FY25, representing a decline of 8% from last year. The decrease was primarily attributable to lower sales from the domestic restaurant segment due to the economic slowdown. Revenue was also impacted by the closure of four Maisen Japanese restaurant branches and the closure of S&P stores in Cambodia due to the military conflict with Thailand. Gross Profit Margin (%): Gross profit margin in 4Q25 was 56.2%, a decrease of 0.5 percentage points, while FY25 gross profit mar

  `MDA_SNP_FY2025` · `p016` · SHA d8cabe0c7228
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 427m → FY2025 THB 271m · −156m · -36.6%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 271 ลบ. ลด 36.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 4Q24 4Q25 FY24 FY25 %Gross Profit Margin: In 4Q25, this was 56.2%, a decrease of 0.5% from the previous year. The main reason 3M was due to higher raw material costs compared to last year. However, improved cost management at the store level helped partially mitigate the impact of rising costs. %Gross Profit Margin: In FY25, this was 55.7%, a decrease of 0.6% from the previous year. The decline was FY primarily due to higher raw material costs. Nevertheless, the Company continued to implement LEAN production practices, reduce factory costs, and enhance procurement efficiency to maintain stable raw material costs. 6 | P a g e

  `MDA_SNP_FY2025` · `p024` · SHA 8dcfd05758b2
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 271 ลบ. ลด 36.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อุปสงค์และกำลังซื้อในประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Profit – share of the owners 127 107 (20) 427 271 (156) Net Profit Margin (%) 7.3% 7.0% (0.3%) 7.0% 4.8% (2.2%) Revenue: The Company reported revenue of 1,519 million Baht in 4Q25 and total revenue of 5,642 million Baht for FY25, representing a decline of 8% from last year. The decrease was primarily attributable to lower sales from the domestic restaurant segment due to the economic slowdown. Revenue was also impacted by the closure of four Maisen Japanese restaurant branches and the closure of S&P stores in Cambodia due to the military conflict with Thailand. Gross Profit Margin (%): Gross profit margin in 4Q25 was 56.2%, a decrease of 0.5 percentage points, while FY25 gross profit mar

  `MDA_SNP_FY2025` · `p016` · SHA d8cabe0c7228
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 271 ลบ. ลด 36.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ อุปสงค์และกำลังซื้อในประเทศ และ การแข่งขันและการส่งเสริมการขาย และ ภาระหนี้และโครงสร้างเงินทุน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 5. Factors That May Affect Operations or Future Growth In 2026, Thailand’s restaurant and bakery industry will face a critical test amid slower economic growth, high household debt, and weakened consumer purchasing power. As a result, consumer spending on dining out and premium bakery products will be more carefully considered. At the same time, operators continue to face cost pressures, including rising rental expenses, higher delivery platform fees, volatility in imported raw material prices, as well as increasing utility, labor, and transportation costs — all of which directly impact profit margins. In addition, market competition has intensified as new players are able to enter the marke

  `MDA_SNP_FY2025` · `p034` · SHA bee5005d4f75
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 271 ลบ. ลด 36.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 4Q24 4Q25 FY24 FY25 3M Net profit: In 4Q25, this was 107 million Baht, a decrease of 15% year-on-year, primarily due to lower revenue. Net profit: In FY25, this was 271 million Baht, a decrease of 37% year-on-year. The decline was mainly FY attributable to lower revenue and an increase in expenses with a proportion that was higher than the growth in revenue. 7 | P a g e

  `MDA_SNP_FY2025` · `p028` · SHA f5e1623cb226
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_SNP_FY2025`

##### OKJ — ตัวเทียบการเติบโต · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ปลูกผักเพราะรักแม่ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ให้บริการและจำหน่ายอาหาร เครื่องดื่ม และผลิตภัณฑ์เพื่อสุขภาพ

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 2.0bn | 3.36 | -16.8% | n.m. | 2.6% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 2.4bn → FY2025 THB 2.7bn · +305m · +12.6%

- รายได้โต 12.6% จากการเพิ่ม 10 สาขา แต่ SSSG แบรนด์หลักลด 21.6%; การเติบโตมาจากพื้นที่ขาย ไม่ใช่ ประสิทธิภาพต่อสาขา ต่อสาขา
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > 1 สาขา ทำให้มีช่องทางรายได้ใหม่เพิ่มขึ้น ในขณะที่อัตราการเติบโตของรายได้จากการขายของสาขาเดิม (SSSG คำนวณจากแบรนด์โอ้กะจู๋จำนวน 29 สาขา) อยู่ที่ร้อยละ -21.6 สาเหตุหลักจากการลดลงของยอดขายสาขาในเมืองและสาขาในโซนที่มีการแข่งขันสูง และฐานเปรียบเทียบที่สูงจากปีก่อนเนื่องจากการออก ผลิตภัณฑ์ใหม่ของแบรนด์โอ้กะจู๋ที่ได้รับการตอบรับเป็นอย่างดีและมียอดขายติดอันดับต้น นอกจากนี้ยังได้รับผลกระทบจากฤดูฝน รวมถึงภาวะ

  `MDA_OKJ_FY2025` · `p039` · SHA 11cb4914eca5
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 202m → FY2025 THB 70m · −131m · -65.1%

- กำไรลด 65.1% เพราะต้นทุนคงที่จากสาขาใหม่เพิ่มเร็วกว่ายอดขายและ SSSG ที่อ่อนทำให้เกิด ผลลบจากต้นทุนคงที่เมื่อยอดขายลดลง; 4Q25 ยังมี การตัดจำหน่าย 17 ลบ.
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > หมายเหตุ: กำไรขั้นต้น = รายได้จากการขาย หักด้วยต้นทุนขาย ต้นทุนขายของบริษัทฯ ประกอบด้วย ต้นทุนวัตถุดิบ ค่าโสหุ้ยการผลิต ค่าแรง ค่าเสื่อมราคาและค่าตัดจำหน่าย เป็นต้น โดยต้นทุนวัตถุดิบจะรวมถึงต้นทุนเมล็ด และต้นทุนที่เกิดขึ้น จากกระบวนการเพาะปลูก เป็นต้น และค่าแรง จะรวมค่าแรงตั้งแต่กระบวนการเพาะปลูก ผลิต ไปจนถึงการประกอบอาหารที่หน้าร้านสาขา บริษัทฯ รายงานกำไรขั้นต้นในไตรมาส 4/68 อยู่ที่ 249.0 ล้านบาท ลดลง 54.1 ล้านบาท หรือคิดเป็นร้อยละ 17.9 เมื่อเทียบกับปีก่อน โดยอัตรากำไรขั้นต้นอยู่ที่ร้อยละ 40.0 ลดลงร้อยละ 3.9 เมื่อเทียบกับปีก่อน เนื่องจากต้นทุนค่าแรงงานคงที่ที่บริษัทฯ ยังต้องรับรู้อยู่ในขณะที่

  `MDA_OKJ_FY2025` · `p044` · SHA e67c36e0f9ac
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- ฝ่ายจัดการชะลอการเปิดสาขาหลักและเลื่อนลงทุนขนาดใหญ่ภาคใต้ การฟื้นจึงขึ้นกับยอดขายต่อสาขาและ ความคุ้มค่าทางเศรษฐศาสตร์ ของ รูปแบบร้าน ใหม่

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_OKJ_FY2025`

##### ZEN — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท เซ็น คอร์ปอเรชั่น กรุ๊ป จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ประกอบธุรกิจโดยการถือหุ้นในบริษัทอื่น (Holding Company) โดยมีบริษัทแกน คือ บริษัท เซ็นเรสเตอร์รองโฮลดิ้ง จำกัด ซึ่งประกอบธุรกิจร้านอาหารญี่ปุ่นภายใต้แบรนด์ "ZEN" และธุรกิจเกี่ยวเนื่องอื่น

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.7bn | 5.60 | -8.2% | 34.3x | 1.2% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 20 · NPAT 17 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 4.1bn → FY2025 THB 3.9bn · −118m · -2.9%

- RFO ปี 2568 อยู่ที่ 3,948 ลบ. ลด 2.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In Q4/2025, the Company recorded administrative expenses of THB 117Mn, a decrease of THB 16Mn, or 12%, compared to the same period last year. The ratio of these expenses to total revenue declined by 1.0 percentage point from Q4/2024. For year 2025, administrative expenses totaled THB 505Mn, increasing slightly by THB 1Mn from 2024. The increase was mainly due to higher losses from branch closures of THB 12Mn, partially offset by THB 8Mn lower allowance for doubtful accounts in the franchise business and THB 3Mn lower bank fees, compared to 2024. The ratio of administrative expenses to total revenue increased by 0.4 percentage points compared to 2024, as total revenue declined at a greater ra

  `MDA_ZEN_FY2025` · `p042` · SHA 9914d78ed139
  </details>
- RFO ปี 2568 อยู่ที่ 3,948 ลบ. ลด 2.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Manufacturing and Trading Business: Revenue in Q4/2025 rose by THB 36Mn or 17% YoY. For the full year 2025, revenue grew by THB 185Mn or 25% YoY, driven by product diversification and a new distribution hub in the southern region. Furthermore, to enhance sales efficiency, a subsidiary discontinued the distribution partner and instead supplied products to modern trade channels directly through its own sales team. • Franchise Fees Income: This includes initial fee, royalty and marketing fees charged to franchisees, and franchise renewal fees. In Q4/2025, revenue decreased by THB 3Mn, or 16% YoY, due to fewer new franchise openings. For the full year 2025, revenue declined by THB 5Mn, or 7%, co

  `MDA_ZEN_FY2025` · `p033` · SHA 54893b708e60
  </details>
- RFO ปี 2568 อยู่ที่ 3,948 ลบ. ลด 2.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การแข่งขันและการส่งเสริมการขาย และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Selling and distribution expenses consist of marketing expenses, staff costs, rent, service fees and utilities expenses (service area), commission fees and selling expenses related to the manufacturing and trading business. In Q4/2025, the selling and distribution expenses totaled THB 214Mn, decreased by THB 16Mn, or 7%, from Q4/2024. For year 2025, these expenses were THB 919Mn, a decrease of THB 95Mn or 9% from year 2024. The reduction was mainly due to 1) Tighter control of marketing and promotional expenses in line with the decline in restaurant revenue, and 2) A reduction in company-owned branches, resulting in lower in service-area expenses. As a result, the selling and distribution ex

  `MDA_ZEN_FY2025` · `p041` · SHA 3bcdfcdde500
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 57m → FY2025 THB 46m · −11m · -19.4%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 45.8 ลบ. ลด 19.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > YOY Gross Profit is derived revenue from sales and service (main revenue) deduct cost of sales and service. Cost of Sales and Service mainly consists of raw material costs, staff cost, rent, service fees and utilities (kitchen area). In Q4/2025, the Company’s gross profit was THB 362Mn, decreased by THB 38Mn, or 9% YoY. Gross profit margin was 37.1%, representing a decline of 1.8 percentage points from Q4/2024. For year 2025, gross profit totaled THB 1,545Mn, decreased by THB 95Mn, or 6% YoY, with a 39.1% margin, or down 1.2 percentage points compared to 2024.

  `MDA_ZEN_FY2025` · `p037` · SHA 5e6c0207f948
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 45.8 ลบ. ลด 19.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายภาษี
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > launches, the expansion of distribution hubs, and the addition of new customer bases. In this quarter, the Company recorded a total net profit of THB 15Mn, decreased by THB 9Mn or 36% from Q4/2024. Net profit attributable to owners of the parent amounted to THB 11Mn, a decrease of THB 7Mn, or 38%, compared to the same period last year. For the year 2025, the Company reported total revenue of THB 3,979Mn, a decrease of THB 113Mn, or 3%, from 2024. However, profit before tax increased to THB 97Mn, up THB 6Mn, or 6%, from the prior year. Income tax expense rose by THB 19Mn compared to 2024. As a result, net profit totaled THB 70Mn, decreased by THB 13Mn, or 15%, from 2024. Net profit attributab

  `MDA_ZEN_FY2025` · `p005` · SHA d42105c03bbf
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 45.8 ลบ. ลด 19.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In Q4/2025, the Company’s net profit was THB 15Mn, a decrease of THB 9Mn, or 36%, compared to Q4/2024. The net profit margin decreased by 0.7 percentage points compared to the same periods last year. Attributable to - Parent Company of THB 11Mn, which decreased by THB 7Mn, or 38% YoY. - Minority Equity of Subsidiaries of THB 4Mn, which decreased by THB 2Mn, or 30% YoY. For year 2025, the Company’s net profit totaled THB 70Mn, a decrease of THB 13Mn, or 15% YoY, with net profit margin slightly decreased by 0.2 percentage points from 2024. Attributable to - Parent Company of THB 46Mn, which decreased by THB 11Mn, or 19% YoY. - Minority Equity of Subsidiaries of THB 24Mn, which decreased by THB

  `MDA_ZEN_FY2025` · `p046` · SHA 6f1b97f5fbc5
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 45.8 ลบ. ลด 19.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การแข่งขันและการส่งเสริมการขาย และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Selling and distribution expenses consist of marketing expenses, staff costs, rent, service fees and utilities expenses (service area), commission fees and selling expenses related to the manufacturing and trading business. In Q4/2025, the selling and distribution expenses totaled THB 214Mn, decreased by THB 16Mn, or 7%, from Q4/2024. For year 2025, these expenses were THB 919Mn, a decrease of THB 95Mn or 9% from year 2024. The reduction was mainly due to 1) Tighter control of marketing and promotional expenses in line with the decline in restaurant revenue, and 2) A reduction in company-owned branches, resulting in lower in service-area expenses. As a result, the selling and distribution ex

  `MDA_ZEN_FY2025` · `p041` · SHA 3bcdfcdde500
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_ZEN_FY2025`

##### MADAME — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท มาดาม ไบโอไซเอนซ์ จํากัด (มหาชน)** — อยู่ในภาวะฟื้นตัว; อัตราเติบโตมีความสำคัญรองลงมา

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ธรุกิจหลักของบริษัท ประกอบด้วย 2 ธุรกิจหลักประกอบด้วย(1) ธุรกิจผลิตและจำหน่ายบรรจุภัณฑ์พลาสติกประเภทต่างๆ เช่น พลาสติกชนิดอ่อนตัว, ขวดพีอีที และบรรจุภัณฑ์พลาสติกขึ้นรูปด้วยระบบ Vacuum เช่น ถาดบรรจุอาหาร เพื่อใช้สำหรับบรรจุสินค้าอุปโภคและบริโภคประเภทต่างๆ โดยเฉพาะในกลุ่มอุตสาหกรรมอาหาร (บริษัท โกลบอล คอนซูเมอร์ จำกัด (มหาชน)) (?GLOCON?) และ (บริษัท พร้อมแพค จำกัด) (?PP?)(2) ธุรกิจอาหาร โดยแบ่งประเภทเป็น (2.1)ธุรกิจ…

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 670m | 0.83 | +18.6% | n.m. | 3.1% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 1 · NPAT 7 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 2.1bn → FY2025 THB 1.5bn · −645m · -30.4%

- RFO ปี 2568 อยู่ที่ 1,478 ลบ. ลด 30.4% YoY; MD&A ระบุว่า ภายหลังการเข้าซื้อกิจการเสร็จสิ้นในช่วงปลายเดือนเมษายน 2568 Madame Louise มีส่วนสนับสนุนกำไรสุทธิ 58 ล้าน บาท ในปี 2568 โดยรับรู้กำไรตั้งแต่เดือนพฤษภาคมถึงธันวาคม 2568 (เพียง 8 เดือน) แม้จะรับรู้ผลประกอบการเพียง 8 เดือน แต่ Madame Louise ได้กลายเป็นแหล่งสร้างกำไรหลักของกลุ่ม โดยคิดเป็นสัดส่วนกำไรส่วนใหญ่ของงบการเงิน รวมปี 2568 เมื่อพิจารณาในลักษณะปรับเป็นเต็มปี (annualized basis) อัตราการทำกำไรสะท้อนศักยภาพการดำเนินงาน ที่สูงขึ้นอย่างมีนัยสำคัญ แสดงให้เห็นถึงความแข็งแกร่งและความสามารถในการขยายตัวของโมเดลธุรกิจ รายได้มีแนวโน้มเติบโตอย่างเร่งตัว และฝ่ายบริ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ภายหลังการเข้าซื้อกิจการเสร็จสิ้นในช่วงปลายเดือนเมษายน 2568 Madame Louise มีส่วนสนับสนุนกำไรสุทธิ 58 ล้าน บาท ในปี 2568 โดยรับรู้กำไรตั้งแต่เดือนพฤษภาคมถึงธันวาคม 2568 (เพียง 8 เดือน) แม้จะรับรู้ผลประกอบการเพียง 8 เดือน แต่ Madame Louise ได้กลายเป็นแหล่งสร้างกำไรหลักของกลุ่ม โดยคิดเป็นสัดส่วนกำไรส่วนใหญ่ของงบการเงิน รวมปี 2568 เมื่อพิจารณาในลักษณะปรับเป็นเต็มปี (annualized basis) อัตราการทำกำไรสะท้อนศักยภาพการดำเนินงาน ที่สูงขึ้นอย่างมีนัยสำคัญ แสดงให้เห็นถึงความแข็งแกร่งและความสามารถในการขยายตัวของโมเดลธุรกิจ รายได้มีแนวโน้มเติบโตอย่างเร่งตัว และฝ่ายบริหารคาดว่ารายได้ในปี 2569 จะเพิ่มขึ้นประมาณเท่าตัวเมื่อเทียบกับปี 2568 โดยได้รับแรงสนับสนุนจากการขยายพอร์ตสินค้าการเพิ่มการเข้าถึงตลาดในประเท

  `MDA_MADAME_FY2025` · `p006` · SHA 910ab06b2ec6
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 332m → FY2025 THB 46m · +378m

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 45.8 ลบ. จากขาดทุน -332 ลบ.; MD&A ระบุว่า การปรับโครงสร้างพอร์ตธุรกิจเชิงกลยุทธ์ – การจำหน่ายเงินลงทุนใน Fruity Dry ในเดือนธันวาคม 2568 บริษัทได้ดำเนินการจำหน่ายเงินลงทุนใน Fruity Dry ซึ่งเป็นบริษัทย่อยที่มีผลการดำเนินงานต่ำ กว่าคาด โดยธุรกรรมดังกล่าวส่งผลให้เกิดการขาดทุนจากการจำหน่ายจำนวน 77.18 ล้านบาท แม้ว่าผลกระทบทางบัญชี จะมีนัยสำคัญ แต่การตัดสินใจดังกล่าวมีความจำเป็นในเชิงกลยุทธ์ เนื่องจาก Fruity Dry มีผลขาดทุนจากการดำเนินงาน อย่างต่อเนื่องประมาณ 5–6 ล้านบาทต่อเดือน ส่งผลให้กำไรของกลุ่มลดลงอย่างต่อเนื่องและสร้างแรงกดดันต่อกระแสเงิน สดการจำหน่ายกิจการครั้งนี้ช่วยยุติการขาดทุนประจำยกระดับคุณภ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > การปรับโครงสร้างพอร์ตธุรกิจเชิงกลยุทธ์ – การจำหน่ายเงินลงทุนใน Fruity Dry ในเดือนธันวาคม 2568 บริษัทได้ดำเนินการจำหน่ายเงินลงทุนใน Fruity Dry ซึ่งเป็นบริษัทย่อยที่มีผลการดำเนินงานต่ำ กว่าคาด โดยธุรกรรมดังกล่าวส่งผลให้เกิดการขาดทุนจากการจำหน่ายจำนวน 77.18 ล้านบาท แม้ว่าผลกระทบทางบัญชี จะมีนัยสำคัญ แต่การตัดสินใจดังกล่าวมีความจำเป็นในเชิงกลยุทธ์ เนื่องจาก Fruity Dry มีผลขาดทุนจากการดำเนินงาน อย่างต่อเนื่องประมาณ 5–6 ล้านบาทต่อเดือน ส่งผลให้กำไรของกลุ่มลดลงอย่างต่อเนื่องและสร้างแรงกดดันต่อกระแสเงิน สดการจำหน่ายกิจการครั้งนี้ช่วยยุติการขาดทุนประจำยกระดับคุณภาพกำไรของงบการเงินรวมเพิ่มเสถียรภาพกระแส เงินสดเปิดโอกาสให้ฝ่ายบริหารมุ่งเน้นทรัพยากรไปยังธุรกิจที่มีอัตรากำไรสูงและมีศักยภาพการเติบโต

  `MDA_MADAME_FY2025` · `p004` · SHA a07dfc630928
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 45.8 ลบ. จากขาดทุน -332 ลบ.; MD&A ระบุว่า ภายหลังการเข้าซื้อกิจการเสร็จสิ้นในช่วงปลายเดือนเมษายน 2568 Madame Louise มีส่วนสนับสนุนกำไรสุทธิ 58 ล้าน บาท ในปี 2568 โดยรับรู้กำไรตั้งแต่เดือนพฤษภาคมถึงธันวาคม 2568 (เพียง 8 เดือน) แม้จะรับรู้ผลประกอบการเพียง 8 เดือน แต่ Madame Louise ได้กลายเป็นแหล่งสร้างกำไรหลักของกลุ่ม โดยคิดเป็นสัดส่วนกำไรส่วนใหญ่ของงบการเงิน รวมปี 2568 เมื่อพิจารณาในลักษณะปรับเป็นเต็มปี (annualized basis) อัตราการทำกำไรสะท้อนศักยภาพการดำเนินงาน ที่สูงขึ้นอย่างมีนัยสำคัญ แสดงให้เห็นถึงความแข็งแกร่งและความสามารถในการขยายตัวของโมเดลธุรกิจ รายได้มีแนวโน้มเติบโตอย่างเร่งตัว และฝ่ายบริ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ภายหลังการเข้าซื้อกิจการเสร็จสิ้นในช่วงปลายเดือนเมษายน 2568 Madame Louise มีส่วนสนับสนุนกำไรสุทธิ 58 ล้าน บาท ในปี 2568 โดยรับรู้กำไรตั้งแต่เดือนพฤษภาคมถึงธันวาคม 2568 (เพียง 8 เดือน) แม้จะรับรู้ผลประกอบการเพียง 8 เดือน แต่ Madame Louise ได้กลายเป็นแหล่งสร้างกำไรหลักของกลุ่ม โดยคิดเป็นสัดส่วนกำไรส่วนใหญ่ของงบการเงิน รวมปี 2568 เมื่อพิจารณาในลักษณะปรับเป็นเต็มปี (annualized basis) อัตราการทำกำไรสะท้อนศักยภาพการดำเนินงาน ที่สูงขึ้นอย่างมีนัยสำคัญ แสดงให้เห็นถึงความแข็งแกร่งและความสามารถในการขยายตัวของโมเดลธุรกิจ รายได้มีแนวโน้มเติบโตอย่างเร่งตัว และฝ่ายบริหารคาดว่ารายได้ในปี 2569 จะเพิ่มขึ้นประมาณเท่าตัวเมื่อเทียบกับปี 2568 โดยได้รับแรงสนับสนุนจากการขยายพอร์ตสินค้าการเพิ่มการเข้าถึงตลาดในประเท

  `MDA_MADAME_FY2025` · `p006` · SHA 910ab06b2ec6
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 45.8 ลบ. จากขาดทุน -332 ลบ.; MD&A ระบุว่า แนวโน้มปี 2569 ภายหลังการจำหน่ายธุรกิจที่ขาดทุนและการทำกำไรได้ครบทุกบริษัทย่อยกลุ่มบริษัทก้าวเข้าสู่ปี 2569 ด้วยฐานะการเงิน ที่แข็งแกร่งขึ้นโครงสร้างงบดุลที่มั่นคงความชัดเจนของแนวโน้มกำไรที่ดีขึ้นฝ่ายบริหารคาดว่าปี 2569 จะยังคงมี โมเมนตัมการเติบโตที่แข็งแกร่ง โดยมีปัจจัยขับเคลื่อนหลักจากการขยายตัวของ Madame Louise การเพิ่มประสิทธิภาพ การดำเนินงานของบริษัทย่อยการจัดสรรเงินทุนอย่างมีวินัยบริษัทยังคงมุ่งมั่นสร้างความสามารถทำกำไรอย่างยั่งยืนและ เพิ่มมูลค่าแก่ผู้ถือหุ้นในระยะยาว ผ่านการดำเนินกลยุทธ์ที่ชัดเจนและความเป็นเลิศด้านการบริหารจัดการ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > แนวโน้มปี 2569 ภายหลังการจำหน่ายธุรกิจที่ขาดทุนและการทำกำไรได้ครบทุกบริษัทย่อยกลุ่มบริษัทก้าวเข้าสู่ปี 2569 ด้วยฐานะการเงิน ที่แข็งแกร่งขึ้นโครงสร้างงบดุลที่มั่นคงความชัดเจนของแนวโน้มกำไรที่ดีขึ้นฝ่ายบริหารคาดว่าปี 2569 จะยังคงมี โมเมนตัมการเติบโตที่แข็งแกร่ง โดยมีปัจจัยขับเคลื่อนหลักจากการขยายตัวของ Madame Louise การเพิ่มประสิทธิภาพ การดำเนินงานของบริษัทย่อยการจัดสรรเงินทุนอย่างมีวินัยบริษัทยังคงมุ่งมั่นสร้างความสามารถทำกำไรอย่างยั่งยืนและ เพิ่มมูลค่าแก่ผู้ถือหุ้นในระยะยาว ผ่านการดำเนินกลยุทธ์ที่ชัดเจนและความเป็นเลิศด้านการบริหารจัดการ

  `MDA_MADAME_FY2025` · `p012` · SHA 814d8c9114b7
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 45.8 ลบ. จากขาดทุน -332 ลบ.; MD&A ระบุว่า กำไร (ขาดทุน) สำหรับงวด 7 20 -13 -63% พงศรารายงานกำไรสุทธิ 7 ล้านบาท ในปี 2568 โดยได้รับแรงสนับสนุนจากการบริหารต้นทุนวัตถุดิบอย่างมีประสิทธิภาพ การควบคุมค่าใช้จ่ายการผลิตการปรับโครงสร้างทีมขายการพัฒนาผลิตภัณฑ์ที่หลากหลายฝ่ายบริหารคาดว่ากำไรขั้นต้น
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไร (ขาดทุน) สำหรับงวด 7 20 -13 -63% พงศรารายงานกำไรสุทธิ 7 ล้านบาท ในปี 2568 โดยได้รับแรงสนับสนุนจากการบริหารต้นทุนวัตถุดิบอย่างมีประสิทธิภาพ การควบคุมค่าใช้จ่ายการผลิตการปรับโครงสร้างทีมขายการพัฒนาผลิตภัณฑ์ที่หลากหลายฝ่ายบริหารคาดว่ากำไรขั้นต้น

  `MDA_MADAME_FY2025` · `p007` · SHA ad5bd793ec03
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_MADAME_FY2025`

##### AQUA — ตัวแปรขาดทุน · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท อควา คอร์เปอเรชั่น จำกัด (มหาชน)** — ข้อมูลเทียบเคียงจำกัด: ไม่ควรสรุปเหตุเชื่อมโยงระหว่างรายได้กับกำไร

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริหารการลงทุนในธุรกิจต่าง ๆ

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 571m | 0.10 | -33.3% | n.m. | — |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 9 · NPAT 14 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 7

**RFO — เพราะอะไร** — FY2024 — → FY2025 — · —

- RFO ปี 2568 อยู่ที่ ไม่ปรากฏตัวเลขที่เปรียบเทียบได้ ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้; ปัจจัยที่MD&Aระบุ ได้แก่ การเปลี่ยนแปลงของอัตรากำไร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > AQUA CORPORATION PUBLIC COMPANY LIMITED The Company began gradually recognizing revenue from newly invested subsidiaries during Q2– Q3 2025. As a result, the restaurant business generated total revenue of THB 710.5 million, increasing by THB 667.1 million from the prior year, accounting for 67.3% of the Group’s total revenue. The restaurant business is considered a key growth driver for the Company in the future. The Company expects clearer revenue development following full recognition of operating results after completion of the merger in 2025. Gross profit was THB 117.8 million (gross margin of 16.57%), reflecting profitability below initial estimates and the Company’s expected benchmark.

  `MDA_AQUA_FY2025` · `p019` · SHA f28eae80f223
  </details>
- RFO ปี 2568 อยู่ที่ ไม่ปรากฏตัวเลขที่เปรียบเทียบได้ ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ การเปลี่ยนแปลงของอัตรากำไร และ การซื้อกิจการและการรวมงบการเงิน และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Executive Summary FY2025 • Total Revenue: THB 1,056.31 million. Core revenue increased by 62.2% due to the consolidation of the food business (FAB), which expanded to 143 branches nationwide. Rental and service revenue remained stable at 336.7 million baht from long-term contracts. • Gross Profit: THB 366.14 million, a 27.37% growth. However, the average Gross Profit Margin (GPM) decreased to 32.09% due to the different cost structures of the food business compared to the original rental business. • Operating Profit: THB 78.72 million, a decrease of 54.76%, primarily due to initial costs for the restaurant business.

  `MDA_AQUA_FY2025` · `p005` · SHA 13d7339ce380
  </details>
- RFO ปี 2568 อยู่ที่ ไม่ปรากฏตัวเลขที่เปรียบเทียบได้ ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ การเปลี่ยนแปลงของอัตรากำไร และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ อุปสงค์และกำลังซื้อในประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 1. Slight sales slowdown, with negative average Same Store Sales Growth (%SSSG) across brands due to macroeconomic slowdown and the government’s “Half-Half” scheme in Q4, resulting in a slight decline in gross margin. The Company is revising sales strategies to stimulate revenue and improve cost efficiency.

  `MDA_AQUA_FY2025` · `p020` · SHA 3be10dc11852
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 988m → FY2025 −THB 1.1bn · −94m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -1,082 ลบ. จาก -988 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Share of Loss from Investments in Associates In 2025, the Company recognized a share of loss from associates totaling THB 729.02 million, consisting of: • Eastern Power Group Public Company Limited (“EP”): THB 615.8 million The loss was mainly due to foreign exchange losses on USD intercompany loans and impairment of wind power projects in Vietnam. • Peer For You Public Company Limited (“PEER”): THB 97.6 million Loss resulted from goodwill impairment of Happy Products and Services Co., Ltd., and goodwill and intangible asset impairment of Nestifly Co., Ltd. • Thai Parcel Public Company Limited (“TPL”): THB 15.6 million Loss recognized from TPL’s operating performance. Further details can be

  `MDA_AQUA_FY2025` · `p025` · SHA bf702da067d7
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -1,082 ลบ. จาก -988 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ การเปลี่ยนแปลงของอัตรากำไร และ การซื้อกิจการและการรวมงบการเงิน และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Executive Summary FY2025 • Total Revenue: THB 1,056.31 million. Core revenue increased by 62.2% due to the consolidation of the food business (FAB), which expanded to 143 branches nationwide. Rental and service revenue remained stable at 336.7 million baht from long-term contracts. • Gross Profit: THB 366.14 million, a 27.37% growth. However, the average Gross Profit Margin (GPM) decreased to 32.09% due to the different cost structures of the food business compared to the original rental business. • Operating Profit: THB 78.72 million, a decrease of 54.76%, primarily due to initial costs for the restaurant business.

  `MDA_AQUA_FY2025` · `p005` · SHA 13d7339ce380
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -1,082 ลบ. จาก -988 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ภาระหนี้และโครงสร้างเงินทุน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2. Central expenses incurred to prepare infrastructure and shared support systems for merger integration and long-term operations. 3. Two major non-cash accounting adjustments: Asset impairment loss of THB 27.69 million And Goodwill impairment loss of THB 85.19 million. Excluding normal business operations, net loss would have been THB 110.54 million. Despite pressure on net profit from the above special items, the Restaurant business maintains a strong financial position. FAB generated positive EBITDA of THB 37.74 million and has no debt obligations, providing high financial flexibility to execute its strategy for revenue enhancement and sustainable margin improvement in the coming year.

  `MDA_AQUA_FY2025` · `p021` · SHA 40baed598e11
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -1,082 ลบ. จาก -988 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ การยุติธุรกิจหรือสายผลิตภัณฑ์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Loss Attributable to Owners of the Parent In 2025, the Company reported net loss attributable to shareholders of THB 1,081.72 million, an increase in loss of THB 988.15 million compared to the previous year. The primary reasons were: • Share of loss from associates: THB 729.02 million • Non-recurring items: THB 290.04 million • Loss from discontinued operations: THB 53.79 million

  `MDA_AQUA_FY2025` · `p028` · SHA fc0438dc4af6
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Share of Loss from Investments in Associates In 2025, the Company recognized a share of loss from associates totaling THB 729.02 million, consisting of: • Eastern Power Group Public Company Limited (“EP”): THB 615.8 million The loss was mainly due to foreign exchange losses on USD intercompany loans and impairment of wind power projects in Vietnam. • Peer For You Public Company Limited (“PEER”): THB 97.6 million Loss resulted from goodwill impairment of Happy Products and Services Co., Ltd., and goodwill and intangible asset impairment of Nestifly Co., Ltd. • Thai Parcel Public Company Limited (“TPL”): THB 15.6 million Loss recognized from TPL’s operating performance. Further details can be

  `MDA_AQUA_FY2025` · `p025` · SHA bf702da067d7
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Non-recurring items The Company recorded net non-recurring losses after tax totaling THB 290.0 million, including: • Fair value losses on investment properties of TCDC and Mantra totaling THB 173.4 million • Goodwill impairment and asset impairment in the FAB totaling THB 85.2 million and THB 27.7 million, respectively • Loss on disposal of investments in Chalermpat Corporation Co., Ltd. and X Bio Science Public Company Limited (“XBIO”) totaling THB 40.2 million • Reversal of expected credit loss (ECL) allowance of THB 18.7 million

  `MDA_AQUA_FY2025` · `p026` · SHA faaa463d9877
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_AQUA_FY2025`

#### ทะเบียนข้อสรุป — F5

| ส่วน | ประเภท | ข้อสรุป | รหัสแหล่งข้อมูล |
|---|---|---|---|
| headline | ข้ออนุมานนักวิเคราะห์ | อุปสงค์ร้านอาหารอ่อนแอ และกำไรส่วนผู้ถือหุ้นของกลุ่มที่ map แล้วลดเร็วกกว่า RFO | FY_PANEL, F5_E1, F5_E2 |
| earnings_fact | ข้อเท็จจริงจากการคำนวณ | FY2025 RFO -4.2%; สถานะ NPAT ส่วนผู้ถือหุ้น: profit_decreased | FY_PANEL, AQUA_FY2025_MDA |
| why | ข้อเท็จจริงจากการคำนวณ | RFO ที่เทียบได้ 5 บริษัทลด 4.2%; AQUA ไม่มี RFO เทียบเคียงและไม่ใช้รายได้รวมแทน | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | NPAT ส่วนผู้ถือหุ้นของทั้ง 6 บริษัทลด 76.6% รวมขาดทุนของ AQUA | FY_PANEL |
| why | คำอธิบายฝ่ายจัดการ | M ระบุกำลังซื้ออ่อนและ same-store sales ติดลบ ขณะที่ OKJ เป็นตัวเทียบด้านการเติบโต | F5_E1, F5_E2 |
| causal_chain | ข้ออนุมานนักวิเคราะห์ | ห่วงโซ่เหตุ: Traffic → Ticket size → SSSG → Store margin → NPAT | F5_E1, F5_E2 |
| roles | ข้ออนุมานนักวิเคราะห์ | บทบาท: ผู้นำและตัวฉุดกำไร — M; ตัวเทียบการเติบโต — OKJ; ตัวแปรขาดทุน — AQUA | FY_PANEL, F5_E1, F5_E2 |
| valuation | ข้ออนุมานนักวิเคราะห์ | P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 23.6x ครอบคลุม 3/6 บริษัท และ 88.7% ของ market cap ที่มีข้อมูล. multiple ให้ค่ากับ turnaround ขณะที่กำไรปัจจุบันยังอ่อน | SET_PUBLIC_EOD, F5_E1, F5_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | SSSG กลับมาเป็นบวก | F5_E1, F5_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | traffic ดีขึ้นโดยไม่เสีย margin จากส่วนลด | F5_E1, F5_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | productivity ต่อสาขาดีขึ้น | F5_E1, F5_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | กำลังซื้ออ่อนต่อเนื่อง | F5_E1, F5_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | โปรโมชั่นกด margin | F5_E1, F5_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | ขยายสาขาเร็วกว่าความต้องการ | F5_E1, F5_E2 |
| must_prove | ประเด็นที่ต้องพิสูจน์ | 6M26 ต้องเห็น SSSG และ store EBITDA ของธุรกิจร้านอาหารหลักเป็นบวก พร้อม bridge แยกของ AQUA สำหรับขาดทุนบริษัทร่วม ด้อยค่า และกระแสเงินสดดำเนินงาน | F5_E1, F5_E2 |

#### ทะเบียนหลักฐาน — F5

- **`FY_PANEL`** · _ข้อเท็จจริงจากการคำนวณ_ — Audited FY2024-25 company panel
  - RFO / NPAT-to-owners / independent panel membership; QA 43 pass / 0 fail
  - บทบาท: historical fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_company_fy2024_2025_audited_2026-08-07.csv`
  - SHA-256: `e5e04dbc40ffcc79fed58545a93dc4549c29cdaecf260bea73711bc6d0720481`
- **`SET_PUBLIC_EOD`** · _ข้อเท็จจริงจากการคำนวณ_ — SET public Company Highlights — EOD 2026-08-07
  - Adjusted YTD; unadjusted price, market cap and valuation; factsheet-surface cross-check
  - บทบาท: current market fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_set_public_surface_reconciliation_2026-08-07.csv`
  - SHA-256: `544c1f29fe2d409ee398822ac2bf32b769081718962ae2d1138985b0146b9530`
- **`SET_COMPANY_PROFILE`** · _ข้อเท็จจริง_ — SET company profiles — English and Thai
  - Official company names and business descriptions refreshed and validated for the 118-company perimeter from the public SET profile API
  - บทบาท: company business profile
  - URL: <https://www.set.or.th/th/market/product/stock/overview>
- **`COMPANY_REPORTS`** · _ข้ออนุมานนักวิเคราะห์_ — Company report synthesis corpus
  - Annual-only draft synthesis; reconciled to the ticker FY2025 MD&A where available
  - บทบาท: secondary synthesis; not management attribution
  - พาธ: `data/company-reports.json`
  - SHA-256: `c1a2bc40cbe21a2058aa596c362e4d47ad117360831b847de78ec414831fd2d2`
- **`MDA_M_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — M FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/M/MDA_M_2025FY_E.md`
  - SHA-256: `db3b643c357c4808a61e7bfbd46c2a57ecbcbc0f82d4e373270859d371bf4e74`
  - URL: <https://weblink.set.or.th/dat/news/202602/1145NWS260220261829429510E.pdf>
- **`MDA_SNP_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — SNP FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SNP/MDA_SNP_2025FY_E.md`
  - SHA-256: `a50cfb3ad75f9516d96a97948aa9e9f48dfd4d1ef81a953c29b0fe4f6265445b`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/0146NWS260220261756174130E.pdf>
- **`MDA_OKJ_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — OKJ FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/OKJ/MDA_OKJ_2025FY_T.md`
  - SHA-256: `c857909f1877f5a8d2bf79f4578bc86ddfcf1c166b0126f78d97bc435506f588`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/1882NWS060220261718446310T.pdf>
- **`MDA_ZEN_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — ZEN FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/ZEN/MDA_ZEN_2025FY_E.md`
  - SHA-256: `c8bdf3592277f0a169266641db0998f497ef77027ca7f1afafcdd7792b0c7275`
  - URL: <https://weblink.set.or.th/dat/news/202602/1479NWS250220260715430160E.pdf>
- **`MDA_MADAME_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — MADAME FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/MADAME/MDA_MADAME_2025FY_T.md`
  - SHA-256: `2aeeaad28f690f2d2133c8185f75389e4b34ba775457b3136343ef6fca30a158`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/0404NWS270220260722008440T.pdf>
- **`MDA_AQUA_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — AQUA FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/AQUA/MDA_AQUA_2025FY_E.md`
  - SHA-256: `6b7f76fdd10f69e78da0f8725dfde087a670b993a2e0bc2f0574667a18b8d7aa`
  - URL: <https://weblink.set.or.th/dat/news/202603/0793NWS020320260807251290E.pdf>
- **`AQUA_FY2025_MDA`** · _คำอธิบายฝ่ายจัดการ_ — AQUA FY2025 filing / MD&A
  - Direct filing evidence for explicitly labelled RFO or NPAT override values
  - บทบาท: override value evidence
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/AQUA/MDA_AQUA_2025FY_E.md`
  - SHA-256: `6b7f76fdd10f69e78da0f8725dfde087a670b993a2e0bc2f0574667a18b8d7aa`
- **`F5_E1`** · _ฝ่ายจัดการ_ — M FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/M/MDA_M_2025FY_E.md`
  - SHA-256: `db3b643c357c4808a61e7bfbd46c2a57ecbcbc0f82d4e373270859d371bf4e74`
- **`F5_E2`** · _ฝ่ายจัดการ_ — AQUA FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/AQUA/MDA_AQUA_2025FY_E.md`
  - SHA-256: `6b7f76fdd10f69e78da0f8725dfde087a670b993a2e0bc2f0574667a18b8d7aa`
- **`F5_FACTSHEET`** · _ข้อเท็จจริงจากการคำนวณ_ — SET Factsheet — M
  - Live leader cross-check
  - บทบาท: presentation-surface check
  - URL: <https://www.set.or.th/th/market/product/stock/quote/m/factsheet>

### F7 · วัตถุดิบและเครื่องปรุง — รายได้หดตัว แต่ขาดทุน NRF ที่ลดลงช่วยยกกำไรส่วนผู้ถือหุ้น

`ราคานำพื้นฐาน` · 3.3% M-cap · THB 26.8bn · 4 บริษัท

| ตัวชี้วัด | RFO | NPAT | ราคา | P/E |
|---|---|---|---|---|
| ช่วง | FY2025 YoY | ส่วนผู้ถือหุ้น FY2025 YoY | ราคา YTD ปรับแล้ว | เฉพาะบริษัทที่มีกำไร |
| ค่า | -7.0% | +311.9% | +25.6% | 19.3x |
| จำนวน | THB 11.5bn FY2025 | THB 700m FY2025 | ณ 7 ส.ค. 2569 | ค่าเฉลี่ยรวม |
| ครอบคลุม | 4/4 | 4/4 | 4/4 • 100% M-cap | 3/4 • 99% M-cap |

**ข้อเท็จจริงที่สังเกตได้** — FY2025: RFO -7.0% • NPAT +311.9% • ราคา YTD +25.6% • P/E 19.3x • ครอบคลุม RFO 4/4 • NPAT 4/4

#### เหตุผลที่เปลี่ยน

1. _ข้อเท็จจริงจากการคำนวณ_ · ปริมาณ — RFO ลด 7.0% โดยมี NRF เป็นตัวฉุดหลัก
2. _ข้อเท็จจริงจากการคำนวณ_ · ส่งออก / OEM — NPAT ส่วนผู้ถือหุ้นเพิ่มจาก 169.9 ล้านบาทเป็น 700.0 ล้านบาท จากขาดทุน NRF ที่ลดลง
3. _ข้ออนุมานนักวิเคราะห์_ · Mix — RBF ยังเป็นตัวฉุดกำไรหลักในกลุ่มบริษัทที่มีกำไร ขณะที่ SAUCE เป็น quality anchor

#### ห่วงโซ่เหตุและผล

**ปริมาณ** → **ส่งออก / OEM** → **Mix** → **Cash margin** (6.1% +4.7 ppt YoY) → **Premium** (19.3x YTD +25.6%)

#### บทบาทในกลุ่ม

| บทบาท | Ticker | ค่า | ที่มาของค่า |
|---|---|---|---|
| ผู้นำและตัวแทนคุณภาพ | SAUCE | 56% | สัดส่วน Market Cap ในกลุ่ม |
| ตัวขับเคลื่อนจากขาดทุนลด | NRF | ขาดทุนลดลง | NPAT YoY · Δ +560m |
| ตัวฉุดกำไร | RBF | -15.8% | NPAT YoY · Δ −81m |

#### มูลค่า

**ตลาดกำลังจ่ายเพื่อ — ข้ออนุมาน** — P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 19.3x ครอบคลุม 3/4 บริษัท และ 98.7% ของ market cap ที่มีข้อมูล. premium สะท้อนคุณภาพ SAUCE และ optionality ของ RBF ไม่ใช่การเติบโตรายได้ทั้งกลุ่ม

| Trigger | Risk |
|---|---|
| คำสั่งซื้อ OEM และส่งออกเร่งตัว | premium สูงแต่กำไรไม่ตาม |
| สัดส่วนสินค้ามูลค่าสูงดีขึ้น | ลูกค้ากระจุกตัว |
| margin ของ RBF ฟื้น | ต้นทุนและค่าเงินผันผวน |

**6M26 ต้องพิสูจน์** — 6M26 ต้องเปลี่ยน price momentum ให้เป็นการโตของรายได้และกำไรในวงกว้าง

#### วิเคราะห์รายบริษัท — F7 วัตถุดิบและเครื่องปรุง

_ทุกบริษัทใน perimeter ของ Segment ที่สอบทาน_

| Ticker | บทบาท | M-cap | RFO YoY | NPAT YoY | ราคา YTD | P/E | Margin |
|---|---|---|---|---|---|---|---|
| SAUCE | ผู้นำและตัวแทนคุณภาพ | THB 14.9bn | -0.4% | +6.0% | +7.1% | 18.9x | 22.6% |
| RBF | ตัวฉุดกำไร | THB 10.2bn | -2.1% | -15.8% | +67.8% | 21.3x | 10.0% |
| JDF | บริษัทในกลุ่ม | THB 1.3bn | +11.2% | +8.5% | +54.9% | 12.6x | 11.8% |
| NRF | ตัวขับเคลื่อนจากขาดทุนลด | THB 361m | -21.8% | ขาดทุนลดลง | -22.6% | n.m. | -20.2% |

##### SAUCE — ผู้นำและตัวแทนคุณภาพ · ติดตาม

**บริษัท ไทยเทพรส จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผู้ผลิตและจำหน่ายผลิตภัณฑ์เครื่องปรุงรสอาหาร ภายใต้เครื่องหมายการค้า ภูเขาทอง ประกอบด้วยซอสปรุงรส ซอสพริก น้ำส้มสายชูกลั่น ซอสมะเขือเทศ ซอสพริกผสมมะเขือเทศ ซอสหอยนางรม ซีอิ๊วขาว ซอสผง ซีอิ๊วผง ซอสพริก ตราศรีราชาพานิช และซีอิ๊วญี่ปุ่น ตรา คินซัน นอกจากนี้ยังผลิตตามเครื่องหมายการค้าของลูกค้าด้วย

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 14.9bn | 41.50 | +7.1% | 18.9x | 22.6% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 11 · NPAT 8 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 3.5bn → FY2025 THB 3.5bn · −13m · -0.4%

- RFO ปี 2568 อยู่ที่ 3,496 ลบ. ลด 0.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Overview Operating results of the company in 2025, net profit increased by Bt. 44.91 million or 6.04 % from 2024. Domestic sales in 2025, amounted to Bt. 2,771.52 million, a increased from 2024 by Bt. 53.06 million or 1.95%, resulted from modern trade distribution channel increased by Bt. 96.98 million or 8.94% traditional trade decreased by Bt.48.60 million or 4.15%. Sales in the industrial in 2025, amounted to Bt. 428.83 million, a increased from 2024 by Bt. 38.38 million or 9.83%, driven by the growth of the reade-to-eat food manufacturing plants. Export sales in 2025, amounted to Bt. 300.56 million, a decreased from 2024 by Bt. 73.62 million or 19.68%. The primary causes are attributed t

  `MDA_SAUCE_FY2025` · `p002` · SHA ab3201f545ba
  </details>
- RFO ปี 2568 อยู่ที่ 3,496 ลบ. ลด 0.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Profitability Domestic sales in 2025 increased from 2024 by Bt. 53.06 million, or 1.95% increased from modern trade distribution channel an increased by Bt. 96.98 million, or 8.94%, traditional trade sales decreased by Bt. 48.61 million, or 4.15% due to the economic downturn, as customers are purchasing only enough stock for immediate sale and some major clients have ceased operations. Sales in the industrial in 2025 increased from 2024 by Bt. 38.38 million, or 9.83%, %, driven by the growth of the ready-to-eat food manufacturing plants. However, we start to see slow down in June 2025.

  `MDA_SAUCE_FY2025` · `p006` · SHA e4da8d137c1d
  </details>
- RFO ปี 2568 อยู่ที่ 3,496 ลบ. ลด 0.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ และ อุปสงค์และกำลังซื้อในประเทศ และ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Export sales in 2025 decreased from 2024 by Bt. 73.62 million, or 19.68%. The primary causes are uncontrollable external factors, including the economic slowdown in the Americas and border trade disruptions resulting from the Thailand-Cambodia conflict and internal instability in Myanmar. These issues have directly impacted shipping volumes and trade value across Asia. Strong Thai Currency around 9% against USD in second half of 2025, our product became less competitive therefore our customers also try to reduce their inventory. .

  `MDA_SAUCE_FY2025` · `p009` · SHA e527e580b39a
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 744m → FY2025 THB 789m · +45m · +6.0%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 789 ลบ. เพิ่ม 6.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Overview Operating results of the company in 2025, net profit increased by Bt. 44.91 million or 6.04 % from 2024. Domestic sales in 2025, amounted to Bt. 2,771.52 million, a increased from 2024 by Bt. 53.06 million or 1.95%, resulted from modern trade distribution channel increased by Bt. 96.98 million or 8.94% traditional trade decreased by Bt.48.60 million or 4.15%. Sales in the industrial in 2025, amounted to Bt. 428.83 million, a increased from 2024 by Bt. 38.38 million or 9.83%, driven by the growth of the reade-to-eat food manufacturing plants. Export sales in 2025, amounted to Bt. 300.56 million, a decreased from 2024 by Bt. 73.62 million or 19.68%. The primary causes are attributed t

  `MDA_SAUCE_FY2025` · `p002` · SHA ab3201f545ba
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 789 ลบ. เพิ่ม 6.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Profitability Domestic sales in 2025 increased from 2024 by Bt. 53.06 million, or 1.95% increased from modern trade distribution channel an increased by Bt. 96.98 million, or 8.94%, traditional trade sales decreased by Bt. 48.61 million, or 4.15% due to the economic downturn, as customers are purchasing only enough stock for immediate sale and some major clients have ceased operations. Sales in the industrial in 2025 increased from 2024 by Bt. 38.38 million, or 9.83%, %, driven by the growth of the ready-to-eat food manufacturing plants. However, we start to see slow down in June 2025.

  `MDA_SAUCE_FY2025` · `p006` · SHA e4da8d137c1d
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 789 ลบ. เพิ่ม 6.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Cost of goods sold in 2025 decreased from 61.84% percentage of sales in 2024 compare to 59.94% percentage of sales in 2025 decreased 1.90%, Due to the costs of grain materials have decreased, the appreciation of the Thai Baht, and more efficient production processes.

  `MDA_SAUCE_FY2025` · `p012` · SHA 973ef448dbcb
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 789 ลบ. เพิ่ม 6.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > From the reasons mentioned above performance for the year as of December 31, 2025. The company had a net profit of Bt. 788.76 million, and increase of Bt. 44.91 million than the same of 2024, an increased of 6.04%

  `MDA_SAUCE_FY2025` · `p016` · SHA 9a26bc5204a8
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Less allowance for impairment losses - - - - Net 204.07 210.23 6.16 3.02 The company has the land not used in operations which had been acquired for the purpose of plant expansion in 1994. The company had reconsidered the purpose and cancelled the expansion project since current plant is able to support the growth of the company. In Q3/2025 there was the land improvement amounting of Bt. 6.16 million.

  `MDA_SAUCE_FY2025` · `p039` · SHA f8e5fd811b4f
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_SAUCE_FY2025`

##### RBF — ตัวฉุดกำไร · ติดตาม

**บริษัท อาร์ แอนด์ บี ฟู้ด ซัพพลาย จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและจำหน่ายวัตถุที่ใช้เป็นส่วนผสมในอาหาร (Food Ingredients) ตามคำสั่งซื้อของลูกค้า และ ภายใต้ตราสินค้าของบริษัท เช่น อังเคิลบาร์นส์, เบสท์ โอเดอร์ และ super-find เป็นต้น

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 10.2bn | 5.10 | +67.8% | 21.3x | 10.0% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 8 · NPAT 10 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 4.4bn → FY2025 THB 4.3bn · −94m · -2.1%

- RFO ปี 2568 อยู่ที่ 4,297 ลบ. ลด 2.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Year 2025 Performance Analysis For the year 2025, the Group had revenues from sales and services of Baht 4,297.06 million, which decreased by Baht 94.03 million or -2.14% YoY, when compared with the year 2024, which had revenues from sales and services of Baht 4,391.09 million. The decrease in revenue from sales of Baht 94.03 million was driven by the following key factors; 1.) Source of Revenues - Domestic sales decreased by Baht 116.96 million (-3.39% YoY) - Overseas sales increased by Baht 22.93 million (2.43% YoY) 2.) Product Group - Flavour, Fragrance & Color group decreased by Baht 114.45 million (-8.31% YoY) - Trading goods group decreased by Baht 9.75 million (-2.29% YoY) - Frozen pr

  `MDA_RBF_FY2025` · `p010` · SHA af3402e4ce78
  </details>
- RFO ปี 2568 อยู่ที่ 4,297 ลบ. ลด 2.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การเปลี่ยนแปลงของอัตรากำไร และ ยอดขายส่งออกและตลาดต่างประเทศ และ อุปสงค์และกำลังซื้อในประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > in revenue was primarily due to a reduction in customer’s orders from industrial customers for the Group’s core products, Furthermore, the overall economic slowdown and decreased of consumer purchasing power, resulted in lower growth than expected in other product group. Although the Group has implemented a proactive strategy to expand its market in the Asian region, overseas sales increased by only Baht 22.93 million, or 2.43% when compared to the previous year, mainly due to the appreciation of Thai Baht. Gross profit was Baht 1,498.90 million, a 3.09% decrease compared to previous year. This was mainly due to decrease in revenues from product group with high gross margin. Additionally, it

  `MDA_RBF_FY2025` · `p011` · SHA 8a82f4d3c7bb
  </details>
- RFO ปี 2568 อยู่ที่ 4,297 ลบ. ลด 2.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การเปลี่ยนแปลงของอัตรากำไร และ เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > P ro fit fo r th e y e a r 4 2 9 .0 1 5 1 2 .7 0 (8 3 .6 9 ) -1 6 .3 2 % P ro p o rtio n to re v e n u e s fro m s a le s a n d re n d e rin g s e rv ic e s 9 .9 8 % 1 1 .6 8 % -1 .7 0 % Profit for the year decreased, mainly due to decrease in revenues from product group with high gross margin, which impacted the Group’s overall profitability. Furthermore, in 2025, the Group was also affected by the appreciation of Thai Baht against U.S. Dollar and other currencies, resulting in decrease in sales, gain on foreign exchange rate, and profit for the year compared to the previous year. Simultaneously, selling and administrative expenses increased, particularly personnel costs, consulting fees re

  `MDA_RBF_FY2025` · `p015` · SHA 8da31c12de68
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 513m → FY2025 THB 432m · −81m · -15.8%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 432 ลบ. ลด 15.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ กำลังการผลิตและเครื่องจักรใหม่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2) Profitability Ratios 2.1 The gross profit margin for the year ended 31 December 2025 was 34.88%, a decrease from the gross profit margin for the year ended 31 December 2024, which was 35.22%. This was primarily due to the decrease in revenues from product groups with high gross profit margin. To mitigate this, the Group has diversified its production bases to Indonesia and Vietnam, where production costs are lower and enhancing more efficient cost management. In addition, the Group is in the preparing process to open its new factory in India, which is expected to reduce raw materials and transportation costs while enhancing production efficiency in the future. Management believes that whe

  `MDA_RBF_FY2025` · `p028` · SHA 1a2c6bb6a9a3
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 432 ลบ. ลด 15.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การเปลี่ยนแปลงของอัตรากำไร และ เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > P ro fit fo r th e y e a r 4 2 9 .0 1 5 1 2 .7 0 (8 3 .6 9 ) -1 6 .3 2 % P ro p o rtio n to re v e n u e s fro m s a le s a n d re n d e rin g s e rv ic e s 9 .9 8 % 1 1 .6 8 % -1 .7 0 % Profit for the year decreased, mainly due to decrease in revenues from product group with high gross margin, which impacted the Group’s overall profitability. Furthermore, in 2025, the Group was also affected by the appreciation of Thai Baht against U.S. Dollar and other currencies, resulting in decrease in sales, gain on foreign exchange rate, and profit for the year compared to the previous year. Simultaneously, selling and administrative expenses increased, particularly personnel costs, consulting fees re

  `MDA_RBF_FY2025` · `p015` · SHA 8da31c12de68
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 432 ลบ. ลด 15.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การเปลี่ยนแปลงของอัตรากำไร และ ยอดขายส่งออกและตลาดต่างประเทศ และ อุปสงค์และกำลังซื้อในประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > in revenue was primarily due to a reduction in customer’s orders from industrial customers for the Group’s core products, Furthermore, the overall economic slowdown and decreased of consumer purchasing power, resulted in lower growth than expected in other product group. Although the Group has implemented a proactive strategy to expand its market in the Asian region, overseas sales increased by only Baht 22.93 million, or 2.43% when compared to the previous year, mainly due to the appreciation of Thai Baht. Gross profit was Baht 1,498.90 million, a 3.09% decrease compared to previous year. This was mainly due to decrease in revenues from product group with high gross margin. Additionally, it

  `MDA_RBF_FY2025` · `p011` · SHA 8a82f4d3c7bb
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 432 ลบ. ลด 15.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Profitability Ratio Gross Profit Margin (%) 34.88 35.22 Operating Profit Margin (%) 12.17 13.60 Net Profit Margin (%) 9.94 11.64 Return on Equity (ROE %) 8.88 10.50

  `MDA_RBF_FY2025` · `p030` · SHA f6a2334fb4f6
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: การเปลี่ยนแปลงของอัตรากำไร และ เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > P ro fit fo r th e y e a r 4 2 9 .0 1 5 1 2 .7 0 (8 3 .6 9 ) -1 6 .3 2 % P ro p o rtio n to re v e n u e s fro m s a le s a n d re n d e rin g s e rv ic e s 9 .9 8 % 1 1 .6 8 % -1 .7 0 % Profit for the year decreased, mainly due to decrease in revenues from product group with high gross margin, which impacted the Group’s overall profitability. Furthermore, in 2025, the Group was also affected by the appreciation of Thai Baht against U.S. Dollar and other currencies, resulting in decrease in sales, gain on foreign exchange rate, and profit for the year compared to the previous year. Simultaneously, selling and administrative expenses increased, particularly personnel costs, consulting fees re

  `MDA_RBF_FY2025` · `p015` · SHA 8da31c12de68
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_RBF_FY2025`

##### JDF — บริษัทในกลุ่ม · ติดตาม

**บริษัท เจดีฟู้ด จำกัด (มหาชน)** — รายได้และกำไรเคลื่อนไหวสอดคล้องกัน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและจำหน่ายสินค้าเครื่องปรุงรสอาหาร ซอส ไส้ขนม และอาหารอบแห้ง

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.3bn | 2.20 | +54.9% | 12.6x | 11.8% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 5 · NPAT 3 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 660m → FY2025 THB 733m · +74m · +11.2%

- RFO ปี 2568 อยู่ที่ 733 ลบ. เพิ่ม 11.2% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ และ กำลังการผลิตและเครื่องจักรใหม่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The increase in sales was primarily derived from seasoning products supplied to snack manufacturers, instant noodle producers, and customers in the HORECA segment. During the year, the Company expanded its fried snack production line to support customer demand. However, sales from some customer groups, including dietary supplement products, selected snack categories, and restaurant customers, declined compared with the previous year due to the challenging economic environment. Sales revenue from overseas customers amounted to Baht 50.60 million, increasing by Baht 2.93 million compared with the previous year. The increase was mainly attributable to higher sales of coconut chip products, part

  `MDA_JDF_FY2025` · `p005` · SHA 3939772f6f26
  </details>
- RFO ปี 2568 อยู่ที่ 733 ลบ. เพิ่ม 11.2% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from Sales For the year 2025, the Company recorded sales revenue of Baht 733.45 million, representing an increase of 11.41% compared with the previous year. The increase was mainly attributable to sales from domestic customers, particularly in ODM /OEM products, which amounted to Baht 671.06 million, an increase of 11.67% compared with the previous year.

  `MDA_JDF_FY2025` · `p004` · SHA f0e12458a059
  </details>
- RFO ปี 2568 อยู่ที่ 733 ลบ. เพิ่ม 11.2% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > sales revenue, an increase of 29.50% compared with the previous year. The increase was primarily due to higher expenses from the expansion of sales and marketing teams, listing fees incurred from entering new distribution channels, promotional activities, and market research expenses.

  `MDA_JDF_FY2025` · `p009` · SHA ad0d23352207
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 80m → FY2025 THB 87m · +7m · +8.5%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 86.6 ลบ. เพิ่ม 8.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Profit For the year 2025, the Company reported net profit of Baht 86.56 million, representing 11.80% of sales revenue, an increase of 8.55% compared with the previous year, or Baht 6.82 million. The increase in net profit resulted from the improvement in operating results.

  `MDA_JDF_FY2025` · `p011` · SHA 8735bd91bf4d
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 86.6 ลบ. เพิ่ม 8.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายภาษี
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > However, income tax expense increased during the year as a portion of profits was not eligible as the BOI tax incentives for certain projects expired, resulting in net profit growth at a lower rate than the increase in profit before income tax.

  `MDA_JDF_FY2025` · `p012` · SHA cce3a5d1c7fa
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 86.6 ลบ. เพิ่ม 8.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Profit for the period (%) 99.18 0.82 100.00 495.06 70.01 79.54 644.61 92.86 0.14 92.72 6.16 86.56 67.50 9.55 10.84 87.89 12.59 0.02 12.57 0.84 11.74 449.23 54.06 80.83 584.12 79.70 0.85 78.85 (0.89) 79.74 68.23 8.21 12.28 88.72 12.01 0.13 11.88 0.14 12.01

  `MDA_JDF_FY2025` · `p003` · SHA 05137bc07024
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_JDF_FY2025`

##### NRF — ตัวขับเคลื่อนจากขาดทุนลด · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เอ็นอาร์ อินสแตนท์ โปรดิวซ์ จำกัด (มหาชน)** — อยู่ในภาวะฟื้นตัว; อัตราเติบโตมีความสำคัญรองลงมา

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิต จัดหา และจำหน่ายผลิตภัณฑ์ปรุงรสอาหาร อาหารสำเร็จรูป เครื่องปรุงสำหรับประกอบอาหาร อาหารมังสวิรัตที่ไม่มีส่วนผสมของไข่และนม อาหารโปรตีนจากพืช และเครื่องดื่มสำเร็จรูปชนิดผงและน้ำ

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 361m | 0.24 | -22.6% | n.m. | -20.2% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 10 · NPAT 17 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 4

**RFO — เพราะอะไร** — FY2024 THB 3.8bn → FY2025 THB 3.0bn · −836m · -21.8%

- RFO ปี 2568 อยู่ที่ 2,999 ลบ. ลด 21.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ มาตรการภาษีนำเข้าและข้อกีดกันทางการค้า และ อุปสงค์และกำลังซื้อในประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Discussion In the fourth quarter of 2025, NR Instant Produce Public Company Limited (the "Company") recorded sales revenue of THB 727.5 million, representing a decrease of 19% year-on-year (YoY), attributable to a slowdown in orders from the United States arising from tariff policies implemented under the administration of President Trump, the appreciation of the Thai Baht, and the divestiture of the Pet food business. On a quarter-on-quarter (QoQ) basis, sales revenue declined by 7%. In 2025, the Company reported sales revenue of THB 2,999.3 million, representing a 22% decrease compared to the same period last year (YoY). The decline was mainly due to a slowdown in orders from the United St

  `MDA_NRF_FY2025` · `p001` · SHA 17305d932726
  </details>
- RFO ปี 2568 อยู่ที่ 2,999 ลบ. ลด 21.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 1. Ethnic and Specialty Food Business o OEM: Sales declined 6.9% QoQ, from THB 310.1 million in Q3/2025 to THB 288.8 million in Q4/2025. o Own Brand: Sales increased 11.1% QoQ, from THB 74.4 million in Q3/2025 to THB 82.7 million in Q4/2025, driven by the Company's proactive sales promotion strategies and product development initiatives tailored to customer demand. 2. Pet Food Business — Sales declined 74.9% QoQ, from THB 88.6 million in Q3/2025 to THB 22.2 million in Q4/2025, due to liquidity issues at a subsidiary that prevented the Company from fulfilling customer orders. The pet food business was divested in November 2025, resulting in reduced revenue recognition. 3. Direct-to-Consumer (

  `MDA_NRF_FY2025` · `p031` · SHA 9b50be3d9449
  </details>
- RFO ปี 2568 อยู่ที่ 2,999 ลบ. ลด 21.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2025 VS 2024 Sales revenue declined from THB 3,835.4 million in 2024 to THB 2,999.3 million in 2025, a decrease of 21.8%, driven by the following key factors: 1. Pet Food Business — In 2025, liquidity issues at a subsidiary prevented the company from fulfilling customer orders. The pet food business was divested in November 2025. 2. Direct-to-Consumer (DTC) Business — Revenue was impacted by the divestiture of an e-commerce operation that had generated significant revenue in Q3/2024. 3. Thai Baht Appreciation — The strengthening of the Thai Baht weighed on overall sales revenue. 4. Ethnic and Specialty Food Business (OEM & Own Brand) — Sales were affected by order deferrals from the United S

  `MDA_NRF_FY2025` · `p032` · SHA a22a3f7375dd
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 1.2bn → FY2025 −THB 607m · +560m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -607 ลบ. จาก -1,166 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ การซื้อกิจการและการรวมงบการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2025 VS 2024 In 2025, the Company's EBITDA is projected at THB -263.8 million, a decrease of THB 463.3 million or 64%, due to losses in 2024 from the acquisition of KAL and KACL assets totaling THB 421.1 million, losses from the sale of investments in subsidiaries (Boosted NRF) totaling THB 282 million, losses from impairment of goodwill totaling 93.4 million baht, a share of losses from investments in joint ventures totaling THB 59.5 million, and a share of losses from investments in associates totaling THB 58.6 million. In contrast, 2025 will see losses from impairment of goodwill totaling THB 83.4 million and a share of losses from investments in joint ventures totaling THB 25.1 million.

  `MDA_NRF_FY2025` · `p041` · SHA a213d1ca2881
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -607 ลบ. จาก -1,166 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ การซื้อกิจการและการรวมงบการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2025 VS 2024 In 2025, the Company reported a net loss of THB 643.6 million, compared with a net loss of THB 1,180.8 million in 2024, representing a decrease in net loss of THB 537.2 million, or 45%. The higher loss in 2024 was mainly due to several non-recurring items, including a loss from the acquisition of assets of KAL and KACL amounting to THB 421.1 million, a loss from the sale of investment in a subsidiary (Boosted NRF) of THB 282 million, a goodwill impairment loss of THB 93.4 million, a share of loss from investment in joint ventures of THB 59.5 million, and a share of loss from investment in associates of THB 58.6 million. In contrast, in 2025 the Company recognized a goodwill impa

  `MDA_NRF_FY2025` · `p044` · SHA 20228341f631
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -607 ลบ. จาก -1,166 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2025 VS 2024 In 2025, the Company reported a gross profit of THB 666.2 million, a decrease from THB 1,006.5 million in 2024, representing a decline of approximately 34%. Meanwhile, the gross profit margin decreased from 26% in 2024 to 22% in 2025. This decline was mainly attributable to the Company’s divestment of its E-Commerce business, which had generated high sales and gross profit margins in the third quarter of 2024. In addition, sales in the local food and specialty food business segments decreased, resulting in a decline in the Group’s overall gross profit and gross profit margin compared with the previous year.

  `MDA_NRF_FY2025` · `p035` · SHA 702fd3787b72
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -607 ลบ. จาก -1,166 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ อัตรากำไรลดลง และ การเปลี่ยนแปลงของอัตรากำไร และ ปริมาณขายและปริมาณการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Q4/2025 vs Q4/2024 In Q4/2025, the Company reported gross profit of THB 158.1 million, up 10% YoY from THB 144.2 million in Q4/2024. Gross margin expanded from 16% in Q4/2024 to 22% in Q4/2025, primarily driven by: • Direct-to-Consumer (DTC) Business — Gross margin improved significantly YoY, supported by higher sales and increased gross profit contribution. • Pet Food Business Divestiture — The pet food business was divested in November 2025. In Q4/2024, the pet food segment had weighed heavily on overall gross margin due to a sharp decline in both sales and production volumes. Its removal from the consolidation therefore had a positive impact on the overall gross margin in Q4/2025.

  `MDA_NRF_FY2025` · `p033` · SHA f982218510ff
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ การซื้อกิจการและการรวมงบการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2025 VS 2024 In 2025, the Company's EBITDA is projected at THB -263.8 million, a decrease of THB 463.3 million or 64%, due to losses in 2024 from the acquisition of KAL and KACL assets totaling THB 421.1 million, losses from the sale of investments in subsidiaries (Boosted NRF) totaling THB 282 million, losses from impairment of goodwill totaling 93.4 million baht, a share of losses from investments in joint ventures totaling THB 59.5 million, and a share of losses from investments in associates totaling THB 58.6 million. In contrast, 2025 will see losses from impairment of goodwill totaling THB 83.4 million and a share of losses from investments in joint ventures totaling THB 25.1 million.

  `MDA_NRF_FY2025` · `p041` · SHA a213d1ca2881
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ การซื้อกิจการและการรวมงบการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2025 VS 2024 In 2025, the Company reported a net loss of THB 643.6 million, compared with a net loss of THB 1,180.8 million in 2024, representing a decrease in net loss of THB 537.2 million, or 45%. The higher loss in 2024 was mainly due to several non-recurring items, including a loss from the acquisition of assets of KAL and KACL amounting to THB 421.1 million, a loss from the sale of investment in a subsidiary (Boosted NRF) of THB 282 million, a goodwill impairment loss of THB 93.4 million, a share of loss from investment in joint ventures of THB 59.5 million, and a share of loss from investment in associates of THB 58.6 million. In contrast, in 2025 the Company recognized a goodwill impa

  `MDA_NRF_FY2025` · `p044` · SHA 20228341f631
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_NRF_FY2025`

#### ทะเบียนข้อสรุป — F7

| ส่วน | ประเภท | ข้อสรุป | รหัสแหล่งข้อมูล |
|---|---|---|---|
| headline | ข้ออนุมานนักวิเคราะห์ | รายได้หดตัว แต่ขาดทุน NRF ที่ลดลงช่วยยกกำไรส่วนผู้ถือหุ้น | FY_PANEL, F7_E1, F7_E2, F7_E3 |
| earnings_fact | ข้อเท็จจริงจากการคำนวณ | FY2025 RFO -7.0%; สถานะ NPAT ส่วนผู้ถือหุ้น: profit_increased | FY_PANEL, NRF_FY2025_MDA |
| why | ข้อเท็จจริงจากการคำนวณ | RFO ลด 7.0% โดยมี NRF เป็นตัวฉุดหลัก | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | NPAT ส่วนผู้ถือหุ้นเพิ่มจาก 169.9 ล้านบาทเป็น 700.0 ล้านบาท จากขาดทุน NRF ที่ลดลง | FY_PANEL |
| why | ข้ออนุมานนักวิเคราะห์ | RBF ยังเป็นตัวฉุดกำไรหลักในกลุ่มบริษัทที่มีกำไร ขณะที่ SAUCE เป็น quality anchor | FY_PANEL, F7_E1, F7_E2, F7_E3 |
| causal_chain | ข้ออนุมานนักวิเคราะห์ | ห่วงโซ่เหตุ: ปริมาณ → ส่งออก / OEM → Mix → Cash margin → Premium | F7_E1, F7_E2, F7_E3 |
| roles | ข้ออนุมานนักวิเคราะห์ | บทบาท: ผู้นำและตัวแทนคุณภาพ — SAUCE; ตัวขับเคลื่อนจากขาดทุนลด — NRF; ตัวฉุดกำไร — RBF | FY_PANEL, F7_E1, F7_E2, F7_E3 |
| valuation | ข้ออนุมานนักวิเคราะห์ | P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 19.3x ครอบคลุม 3/4 บริษัท และ 98.7% ของ market cap ที่มีข้อมูล. premium สะท้อนคุณภาพ SAUCE และ optionality ของ RBF ไม่ใช่การเติบโตรายได้ทั้งกลุ่ม | SET_PUBLIC_EOD, F7_E1, F7_E2, F7_E3 |
| trigger | ประเด็นที่ต้องพิสูจน์ | คำสั่งซื้อ OEM และส่งออกเร่งตัว | F7_E1, F7_E2, F7_E3 |
| trigger | ประเด็นที่ต้องพิสูจน์ | สัดส่วนสินค้ามูลค่าสูงดีขึ้น | F7_E1, F7_E2, F7_E3 |
| trigger | ประเด็นที่ต้องพิสูจน์ | margin ของ RBF ฟื้น | F7_E1, F7_E2, F7_E3 |
| risk | ประเด็นที่ต้องพิสูจน์ | premium สูงแต่กำไรไม่ตาม | F7_E1, F7_E2, F7_E3 |
| risk | ประเด็นที่ต้องพิสูจน์ | ลูกค้ากระจุกตัว | F7_E1, F7_E2, F7_E3 |
| risk | ประเด็นที่ต้องพิสูจน์ | ต้นทุนและค่าเงินผันผวน | F7_E1, F7_E2, F7_E3 |
| must_prove | ประเด็นที่ต้องพิสูจน์ | 6M26 ต้องเปลี่ยน price momentum ให้เป็นการโตของรายได้และกำไรในวงกว้าง | F7_E1, F7_E2, F7_E3 |

#### ทะเบียนหลักฐาน — F7

- **`FY_PANEL`** · _ข้อเท็จจริงจากการคำนวณ_ — Audited FY2024-25 company panel
  - RFO / NPAT-to-owners / independent panel membership; QA 43 pass / 0 fail
  - บทบาท: historical fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_company_fy2024_2025_audited_2026-08-07.csv`
  - SHA-256: `e5e04dbc40ffcc79fed58545a93dc4549c29cdaecf260bea73711bc6d0720481`
- **`SET_PUBLIC_EOD`** · _ข้อเท็จจริงจากการคำนวณ_ — SET public Company Highlights — EOD 2026-08-07
  - Adjusted YTD; unadjusted price, market cap and valuation; factsheet-surface cross-check
  - บทบาท: current market fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_set_public_surface_reconciliation_2026-08-07.csv`
  - SHA-256: `544c1f29fe2d409ee398822ac2bf32b769081718962ae2d1138985b0146b9530`
- **`SET_COMPANY_PROFILE`** · _ข้อเท็จจริง_ — SET company profiles — English and Thai
  - Official company names and business descriptions refreshed and validated for the 118-company perimeter from the public SET profile API
  - บทบาท: company business profile
  - URL: <https://www.set.or.th/th/market/product/stock/overview>
- **`COMPANY_REPORTS`** · _ข้ออนุมานนักวิเคราะห์_ — Company report synthesis corpus
  - Annual-only draft synthesis; reconciled to the ticker FY2025 MD&A where available
  - บทบาท: secondary synthesis; not management attribution
  - พาธ: `data/company-reports.json`
  - SHA-256: `c1a2bc40cbe21a2058aa596c362e4d47ad117360831b847de78ec414831fd2d2`
- **`MDA_SAUCE_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — SAUCE FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SAUCE/MDA_SAUCE_2025FY_E.md`
  - SHA-256: `72a467e7eb2c6b64953feae81e27b91f800f29d3b68d2281831b69bf6a646f8a`
  - URL: <https://weblink.set.or.th/dat/news/202602/0460NWS260220261940274130E.pdf>
- **`MDA_RBF_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — RBF FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/RBF/MDA_RBF_2025FY_E.md`
  - SHA-256: `0794c50c19f02cb2551e47f377c94a3543a7e4e94c432e5d4d185b9326be85c7`
  - URL: <https://weblink.set.or.th/dat/news/202602/1527NWS270220262217094640E.pdf>
- **`MDA_JDF_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — JDF FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/JDF/MDA_JDF_2025FY_E.md`
  - SHA-256: `225eddbdf077c35ae86d47c9ad327ced5cef421c283475aea45a575133c4785a`
  - URL: <https://weblink.set.or.th/dat/news/202602/1695NWS120220261752559070E.pdf>
- **`MDA_NRF_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — NRF FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/NRF/MDA_NRF_2025FY_E.md`
  - SHA-256: `370885e845bd64e543413af760d0dde24e42c4c4b49b04681f3b8047d67be5be`
  - URL: <https://weblink.set.or.th/dat/news/202603/1586NWS160320260850217950E.pdf>
- **`NRF_FY2025_MDA`** · _คำอธิบายฝ่ายจัดการ_ — NRF FY2025 filing / MD&A
  - Direct filing evidence for explicitly labelled RFO or NPAT override values
  - บทบาท: override value evidence
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/NRF/MDA_NRF_2025FY_E.md`
  - SHA-256: `370885e845bd64e543413af760d0dde24e42c4c4b49b04681f3b8047d67be5be`
- **`F7_E1`** · _ฝ่ายจัดการ_ — NRF FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/NRF/MDA_NRF_2025FY_E.md`
  - SHA-256: `370885e845bd64e543413af760d0dde24e42c4c4b49b04681f3b8047d67be5be`
- **`F7_E2`** · _ฝ่ายจัดการ_ — SAUCE FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SAUCE/MDA_SAUCE_2025FY_E.md`
  - SHA-256: `72a467e7eb2c6b64953feae81e27b91f800f29d3b68d2281831b69bf6a646f8a`
- **`F7_E3`** · _มุมมองล่วงหน้า_ — FSSIA RBF research
  - Historical explanation or forward cross-check; see source role
  - บทบาท: forward/credit context
  - พาธ: `Listed Company/1-Raw/06-Market Reference/Broker Research/2026/FOOD/FSSIA_RBF_347820.md`
  - SHA-256: `e1789d9d0137c42f3d8cb399832df8a462c04de48fec41ff4bdb260d30241295`
- **`F7_FACTSHEET`** · _ข้อเท็จจริงจากการคำนวณ_ — SET Factsheet — SAUCE
  - Live leader cross-check
  - บทบาท: presentation-surface check
  - URL: <https://www.set.or.th/th/market/product/stock/quote/sauce/factsheet>

### F9 · เกษตรแปรรูปและธุรกิจหลากหลาย — กลุ่มที่สอบทานแล้วพลิกเป็นขาดทุน และ P/E headline ไม่เป็นตัวแทน

`ยังถูกกดดัน` · 1.2% M-cap · THB 9.4bn · 8 บริษัท

| ตัวชี้วัด | RFO | NPAT | ราคา | P/E |
|---|---|---|---|---|
| ช่วง | FY2025 YoY | ส่วนผู้ถือหุ้น FY2025 YoY | ราคา YTD ปรับแล้ว | เฉพาะบริษัทที่มีกำไร |
| ค่า | -9.8% | ขาดทุน | -10.4% | 12.7x |
| จำนวน | THB 17.3bn FY2025 | −THB 914m FY2025 | ณ 7 ส.ค. 2569 | ค่าเฉลี่ยรวม |
| ครอบคลุม | 8/8 | 8/8 | 8/8 • 100% M-cap | 2/8 • 36% M-cap |

**ข้อเท็จจริงที่สังเกตได้** — FY2025: RFO -9.8% • NPAT ขาดทุน • ราคา YTD -10.4% • P/E 12.7x • ครอบคลุม RFO 8/8 • NPAT 8/8

#### เหตุผลที่เปลี่ยน

1. _ข้อเท็จจริงจากการคำนวณ_ · ผลผลิต / คำสั่งซื้อ — กลุ่ม 8 บริษัทมี RFO -9.8% และพลิกจากกำไร 450.6 ล้านบาทเป็นขาดทุน 914.5 ล้านบาท
2. _ข้อเท็จจริงจากการคำนวณ_ · Utilization — CM ใช้ FY2024 แบบงบเฉพาะกิจการให้ฐานตรงกัน และยกเลิกการเทียบ consolidated กับ separate
3. _ข้อเท็จจริงจากการคำนวณ_ · ต้นทุนต่อหน่วย — P/E ของผู้มีกำไรครอบคลุมเพียง SUN และ SSF จึงอธิบายกลุ่มที่ขาดทุนไม่ได้

#### ห่วงโซ่เหตุและผล

**ผลผลิต / คำสั่งซื้อ** → **Utilization** → **ต้นทุนต่อหน่วย** → **Cash flow** → **ฐานะการเงิน**

#### บทบาทในกลุ่ม

| บทบาท | Ticker | ค่า | ที่มาของค่า |
|---|---|---|---|
| ผู้นำและตัวฉุดราคามากสุด | SUN | 21% | สัดส่วน Market Cap ในกลุ่ม |
| ตัวฉุด RFO | SST | -20.7% | RFO YoY · Δ −700m |
| ตัวฉุดกำไร | APURE | ขาดทุน | NPAT YoY · Δ −511m |

#### มูลค่า

**แรงกดดันปัจจุบัน / ข้อเท็จจริง** — P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 12.7x ครอบคลุม 2/8 บริษัท และ 35.8% ของ market cap ที่มีข้อมูล. P/E ของผู้มีกำไรไม่เป็นตัวแทนกลุ่มที่ขาดทุน

| Trigger | Risk |
|---|---|
| คำสั่งซื้อฟื้น | ขาดทุนดำเนินงานต่อเนื่อง |
| utilization ดีขึ้น | เงินทุนหมุนเวียนตึงตัว |
| ปรับโครงสร้างหน่วยธุรกิจขาดทุน | สภาพคล่องหุ้นต่ำและ event risk |

**6M26 ต้องพิสูจน์** — 6M26 ต้องเห็นขาดทุนดำเนินงานลดลง การฟื้นของ ECL และลูกหนี้ APURE และกระแสเงินสดดำเนินงานกลับปกติก่อนที่ valuation จะมีความหมาย

#### วิเคราะห์รายบริษัท — F9 เกษตรแปรรูปและธุรกิจหลากหลาย

_ทุกบริษัทใน perimeter ของ Segment ที่สอบทาน_

| Ticker | บทบาท | M-cap | RFO YoY | NPAT YoY | ราคา YTD | P/E | Margin |
|---|---|---|---|---|---|---|---|
| SUN | ผู้นำและตัวฉุดราคามากสุด | THB 2.0bn | +2.2% | -39.1% | -15.8% | 13.9x | 5.0% |
| APURE | ตัวฉุดกำไร | THB 2.0bn | -9.1% | ขาดทุน | -5.6% | n.m. | -11.9% |
| SSF | บริษัทในกลุ่ม | THB 1.4bn | +0.7% | +0.1% | +3.0% | 11.2x | 2.5% |
| CH | บริษัทในกลุ่ม | THB 1.2bn | -25.8% | ขาดทุน | -5.8% | n.m. | -1.1% |
| XBIO | บริษัทในกลุ่ม | THB 973m | -59.4% | ขาดทุนเพิ่มขึ้น | -11.6% | n.m. | -361.6% |
| F&D | บริษัทในกลุ่ม | THB 806m | -26.7% | -99.8% | -18.3% | n.m. | 0.0% |
| CM | บริษัทในกลุ่ม | THB 598m | -10.4% | -78.6% | -7.6% | n.m. | 1.9% |
| SST | ตัวฉุด RFO | THB 537m | -20.7% | ขาดทุนเพิ่มขึ้น | -30.1% | n.m. | -19.9% |

##### SUN — ผู้นำและตัวฉุดราคามากสุด · ติดตาม

**บริษัท ซันสวีท จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัทประกอบธุรกิจผลิตและจำหน่ายข้าวโพดหวานแปรรูปและผลิตภัณฑ์แปรรูปสินค้าเกษตรอื่นๆ ภายใต้ตราสินค้าของบริษัท "KC" และภายใต้ตราสินค้าของลูกค้า รวมทั้งธุรกิจจัดหาและซื้อมาจำหน่ายไปซึ่งผลิตภัณฑ์อาหารและผลผลิตทางการเกษตร

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 2.0bn | 2.56 | -15.8% | 13.9x | 5.0% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 2

**RFO — เพราะอะไร** — FY2024 THB 3.5bn → FY2025 THB 3.6bn · +78m · +2.2%

- ยอดขายโต 2.2% จากปริมาณ แบรนด์ของลูกค้า ที่เพิ่มขึ้น แต่เงินบาทแข็งกดรายได้ส่งออกและทำให้ แนวโน้ม ปลายปีอ่อนลง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from sales of goods in 4Q2025 was Baht 927.6 million, representing a decrease of 8.1% from the same quarter last year. The decline was primarily attributable to the adverse impact of exchange rate volatility, as the Thai baht appreciated by 5.4% against the US dollar compared with the same period last year. This appreciation negatively affected export revenues. For the year 2025, the Company reported product sales revenue of Baht 3,592.4 million, an increase of 2.2% year-on-year, driven by higher customer demand in both domestic and international markets. Notably, the domestic market continued to demonstrate strong growth, particularly in the ready-to-eat (RTE) product segment, which

  `MDA_SUN_FY2025` · `p002` · SHA 84de87ff597b
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 294m → FY2025 THB 179m · −115m · -39.1%

- กำไรลด 39.1% เมื่อ อัตรากำไรขั้นต้น ลดเป็น 15.6% จาก 20.0%; แรงกดดัน FX และต้นทุนมากกว่าประโยชน์จากปริมาณที่เพิ่ม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company’s gross profit margin for 4Q2025 was 12.8%, decrease by 2.0% from the same period last year. For the year 2025, the gross profit margin was 15.6%, a decline of 4.4 % year-over-year, primarily due to the reasons mentioned above.

  `MDA_SUN_FY2025` · `p010` · SHA 8580b87c9514
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ ความเสี่ยงด้านภูมิรัฐศาสตร์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 4Q2025, the Company recorded a net gain from foreign exchange and derivative instruments of Baht 7.8 million, representing an increase of 181.7% compared to the same period last year. For the year 2025, the net gain totaled Baht 43.9 million, reflecting a year-on-year increase of 176.4%. These gains were primarily attributable to the appreciation of the Thai baht against the US dollar on an average basis during 4Q2025 and throughout the year 2025, driven by the weakening of the US dollar amid global economic volatility. Nevertheless, the Company continued to actively manage foreign exchange risk by regularly entering into forward foreign exchange contracts, in order to mitigate the impact

  `MDA_SUN_FY2025` · `p012` · SHA faa07cbfd82d
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net gain (loss) from foreign exchange and derivative instruments

  `MDA_SUN_FY2025` · `p011` · SHA 5681204afdfa
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_SUN_FY2025`

##### APURE — ตัวฉุดกำไร · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท อกริเพียว โฮลดิ้งส์ จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — เป็นบริษัทลงทุน (Holding Company) โดยดำเนินธุรกิจผ่านทางบริษัทย่อยซึ่งดำเนินธุรกิจหลักเกี่ยวกับการผลิตและจำหน่ายผลิตภัณฑ์ทางการเกษตรแปรรูป ประเภทข้าวโพดบรรจุกระป๋อง ผัก ผลไม้สดและเมล็ดพันธุ์ข้าวโพด

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 2.0bn | 2.04 | -5.6% | n.m. | -11.9% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 8 · NPAT 19 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 5

**RFO — เพราะอะไร** — FY2024 THB 2.1bn → FY2025 THB 2.0bn · −196m · -9.1%

- RFO ปี 2568 อยู่ที่ 1,952 ลบ. ลด 9.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ปริมาณขายและปริมาณการผลิต และ ยอดขายส่งออกและตลาดต่างประเทศ และ เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from Sales and Services For the fiscal years ended December 31, 2024 and 2025, the Company’s consolidated financial statements reported revenue from sales and services of 2,148.87 million Baht and 1,952.38 million Baht, respectively. This represents a decrease of 196.49 million Baht, or 9.14% year-on-year.The decline in revenue was primarily driven by the following factors Heightened competition from foreign manufacturers, particularly regarding price strategies and lead-time efficiencies. Macroeconomic Volatility: A slowdown in the global economy and fluctuations in foreign exchange rates, which directly impacted sales volumes in key export markets.Changes in the tax policies of maj

  `MDA_APURE_FY2025` · `p010` · SHA f68a55965167
  </details>
- RFO ปี 2568 อยู่ที่ 1,952 ลบ. ลด 9.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the fiscal years ended December 31, 2024 and 2025, the Company’s cost of goods sold amounted to 1,578.02 million Baht and 1,565.89 million Baht, respectively, representing a slight decrease of 12.14 million Baht, or 0.77%. The cost performance can be summarized as follows. The decrease in COGS was primarily in line with the reduction in total sales revenue. Despite the persistence of fixed monthly operating costs, the Company successfully implemented rigorous cost control measures and enhanced operational efficiencies. This mitigated the impact of fixed overheads and contributed to the overall reduction in costs. Cost Stability and Resilience Through these strategic measures, the Company

  `MDA_APURE_FY2025` · `p014` · SHA 562139946aa6
  </details>
- RFO ปี 2568 อยู่ที่ 1,952 ลบ. ลด 9.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross Profit For the fiscal years ended December 31, 2024 and 2025, the Company reported a gross profit of 570.85 million Baht and 386.49 million Baht, respectively. This represents a decrease of 184.36 million Baht, or 32.30%, compared to the previous year. The contraction in gross profit was primarily in line with the decline in sales revenue and the various operational challenges detailed in the preceding section.

  `MDA_APURE_FY2025` · `p015` · SHA 4974d34cd6cf
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 278m → FY2025 −THB 233m · −511m

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -233 ลบ. จากกำไร 278 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the fiscal years ended December 31, 2024 and 2025, the Company’s cost of goods sold amounted to 1,578.02 million Baht and 1,565.89 million Baht, respectively, representing a slight decrease of 12.14 million Baht, or 0.77%. The cost performance can be summarized as follows. The decrease in COGS was primarily in line with the reduction in total sales revenue. Despite the persistence of fixed monthly operating costs, the Company successfully implemented rigorous cost control measures and enhanced operational efficiencies. This mitigated the impact of fixed overheads and contributed to the overall reduction in costs. Cost Stability and Resilience Through these strategic measures, the Company

  `MDA_APURE_FY2025` · `p014` · SHA 562139946aa6
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -233 ลบ. จากกำไร 278 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ภาระหนี้และโครงสร้างเงินทุน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Profit (Loss) for the Year For the fiscal years ended December 31, 2024 and 2025, the Company reported a net profit of 278.29 million Baht and a net loss of 232.66 million Baht, respectively. This represents a significant decrease in performance of 510.95 million Baht, or 183.60% compared to the previous year.The recording of bad debts and expected credit losses (ECL) related to a subsidiary, RKI, amounting to 438.59 million Baht.This mandatory accounting adjustment resulted from advance payments for packaging (cans) made to the subsidiary's suppliers, which are currently being assessed for recoverability. ❖ Financial Position Statement

  `MDA_APURE_FY2025` · `p018` · SHA e114903bf20c
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -233 ลบ. จากกำไร 278 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Shareholders' Equity As of December 31, 2024, and December 31, 2025, the Company’s shareholders’ equity stood at 2,609.16 million Baht and 2,164.73 million Baht, respectively, reflecting a decrease of 17.03% compared to the previous year. The decline in shareholders’ equity was primarily attributable to the net loss incurred during the period. This was mainly due to the recognition of Expected Credit Losses (ECL) by a subsidiary (RKI) regarding advance payments for production materials (cans), which directly impacted the Company’s retained earnings.

  `MDA_APURE_FY2025` · `p022` · SHA a996444f8430
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -233 ลบ. จากกำไร 278 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Company’s overall profitability is projected to experience a decline, primarily driven by a contraction in the gross profit margin and an increase in operating expenses. Consequently, both the net profit and Return on Equity (ROE) are expected to transition into negative territory for the current fiscal year.

  `MDA_APURE_FY2025` · `p027` · SHA fa76e9e37d2b
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ปริมาณขายและปริมาณการผลิต และ ยอดขายส่งออกและตลาดต่างประเทศ และ เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from Sales and Services For the fiscal years ended December 31, 2024 and 2025, the Company’s consolidated financial statements reported revenue from sales and services of 2,148.87 million Baht and 1,952.38 million Baht, respectively. This represents a decrease of 196.49 million Baht, or 9.14% year-on-year.The decline in revenue was primarily driven by the following factors Heightened competition from foreign manufacturers, particularly regarding price strategies and lead-time efficiencies. Macroeconomic Volatility: A slowdown in the global economy and fluctuations in foreign exchange rates, which directly impacted sales volumes in key export markets.Changes in the tax policies of maj

  `MDA_APURE_FY2025` · `p010` · SHA f68a55965167
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้ และ ภาระหนี้และโครงสร้างเงินทุน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The net cash flow from operating activities was primarily influenced by: • Inventory Management: An increase in inventory levels to support production and sales requirements. • Non-cash Adjustments: The recognition of bad debts and Expected Credit Losses (ECL), which are non-cash expenses. • Fair Value Measurement: Gains arising from the fair value adjustments of other non-current financial assets.

  `MDA_APURE_FY2025` · `p024` · SHA 5ef16855080b
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_APURE_FY2025`

##### SSF — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท สุรพลฟู้ดส์ จำกัด (มหาชน)** — รายได้และกำไรเคลื่อนไหวสอดคล้องกัน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและจัดจำหน่ายอาหารแช่เยือกแข็ง ทั้งผลิตภัณฑ์ในกลุ่มพร้อมปรุง (Ready-to-cook) และกลุ่มพร้อมรับประทาน (Ready-to-eat) ที่มีคุณภาพ และผ่านการรับรองมาตรฐานคุณภาพระหว่างประเทศ เช่น GHPs, BRC, HACCP, ISO 22000

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.4bn | 5.15 | +3.0% | 11.2x | 2.5% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 2 · NPAT 3 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 5.6bn → FY2025 THB 5.6bn · +41m · +0.7%

- RFO ปี 2568 อยู่ที่ 5,632 ลบ. เพิ่ม 0.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ และ อุปสงค์และกำลังซื้อในประเทศ และ การออกผลิตภัณฑ์ใหม่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > performance of the Company’s customers in both countries, despite the products remaining high in quality and trusted by the customers. 1.2 Sales in Thailand market increased by Baht 55.5 million or 9.0%. Even though Thailand’s economy grew at a slower rate and consumers were careful with their spending, the Company and its subsidiaries adjusted its strategy to push domestic sales to offset the slowdown in export sales. This was achieved by special focusing on some high-growth sales channels as we as launching new products that align with consumer demand and purchasing power. 2. Gross profit margin from the sale of goods in the year 2025 was 12.0%, lower than the previous year which was 13.5%

  `MDA_SSF_FY2025` · `p003` · SHA b6e3f1b97bd1
  </details>
- RFO ปี 2568 อยู่ที่ 5,632 ลบ. เพิ่ม 0.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > as well as assess and monitor the exchange rate volatility to benefit production and sales planning based on customer orders. Please be informed accordingly.

  `MDA_SSF_FY2025` · `p005` · SHA c813d3d13316
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 139m → FY2025 THB 139m · +0m · +0.1%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 139 ลบ. เพิ่ม 0.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ ความเสี่ยงด้านภูมิรัฐศาสตร์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > from temperature-controlled storage and transportation services, particularly from customers in the restaurants, beverages, and imported fruit businesses. In addition, gross profit margin from rendering of services in the year 2025 increased compared to the previous year. 4. In the year 2025, Thai baht was significantly volatile. The Company and its subsidiaries entered into forward foreign exchange contracts to hedge against this risk, resulting in a net gain from exchange rates for the year 2025 and the year 2024 amounting to Baht 53.6 million and Baht 52.1 million, respectively. However, the Company and its subsidiaries will continue to enter into forward foreign exchange contracts to hed

  `MDA_SSF_FY2025` · `p004` · SHA c59a45b00559
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 139 ลบ. เพิ่ม 0.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การซื้อกิจการและการรวมงบการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Stock Exchange of Thailand Surapon Foods Public Company Limited (“the Company”) hereby reports and clarifies the operating results of the Company and its subsidiaries as shown in the consolidated financial statements for the year ended December 31, 2025, which have been audited by the certified public accountant. The Company and its subsidiaries posted a net profit of Baht 256.3 million (the profit attributable to owners of the parent was Baht 138.9 million), a decrease of 15.0% compared to the year ended December 31, 2024, which posted a net profit of Baht 301.6 million (the profit attributable to owners of the parent was Baht 138.8 million). Significant events that cause such change ca

  `MDA_SSF_FY2025` · `p002` · SHA 1be4c303d762
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 139 ลบ. เพิ่ม 0.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายส่งออกและตลาดต่างประเทศ และ อุปสงค์และกำลังซื้อในประเทศ และ การออกผลิตภัณฑ์ใหม่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > performance of the Company’s customers in both countries, despite the products remaining high in quality and trusted by the customers. 1.2 Sales in Thailand market increased by Baht 55.5 million or 9.0%. Even though Thailand’s economy grew at a slower rate and consumers were careful with their spending, the Company and its subsidiaries adjusted its strategy to push domestic sales to offset the slowdown in export sales. This was achieved by special focusing on some high-growth sales channels as we as launching new products that align with consumer demand and purchasing power. 2. Gross profit margin from the sale of goods in the year 2025 was 12.0%, lower than the previous year which was 13.5%

  `MDA_SSF_FY2025` · `p003` · SHA b6e3f1b97bd1
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ ความเสี่ยงด้านภูมิรัฐศาสตร์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > from temperature-controlled storage and transportation services, particularly from customers in the restaurants, beverages, and imported fruit businesses. In addition, gross profit margin from rendering of services in the year 2025 increased compared to the previous year. 4. In the year 2025, Thai baht was significantly volatile. The Company and its subsidiaries entered into forward foreign exchange contracts to hedge against this risk, resulting in a net gain from exchange rates for the year 2025 and the year 2024 amounting to Baht 53.6 million and Baht 52.1 million, respectively. However, the Company and its subsidiaries will continue to enter into forward foreign exchange contracts to hed

  `MDA_SSF_FY2025` · `p004` · SHA c59a45b00559
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_SSF_FY2025`

##### CH — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เจริญอุตสาหกรรม จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ธุรกิจผลิตและจำหน่ายผลไม้และอาหารแปรรูป ได้แก่ ผลไม้อบแห้ง ปลากระป๋อง และขนม

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.2bn | 1.47 | -5.8% | n.m. | -1.1% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 2

**RFO — เพราะอะไร** — FY2024 THB 2.3bn → FY2025 THB 1.7bn · −588m · -25.8%

- ยอดขายลด 25.9% นำโดยผลไม้อบแห้งซึ่งเป็นรายได้หลักลด 30.2%
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Profit and Net Profit Margin: 2025 vs 2024 The Group reported a net loss of Baht 17.82 million due to the decline in sales revenue from the dehydrated fruit segment, which is the main revenue contributor, and the lower gross profit margins across all three product segments for the reasons previously mentioned, despite effective expense management and lower finance costs. ____________________________________________________________________________________________________________________________________

  `MDA_CH_FY2025` · `p034` · SHA 07152c9bc603
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 127m → FY2025 −THB 18m · −145m

- บริษัทพลิกเป็นขาดทุนจากรายได้ผลไม้อบแห้งลดลงและ อัตรากำไรขั้นต้น ลดทุก 3 กลุ่มสินค้า แม้ควบคุมค่าใช้จ่ายและดอกเบี้ยลดลง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Profit and Net Profit Margin: 2025 vs 2024 The Group reported a net loss of Baht 17.82 million due to the decline in sales revenue from the dehydrated fruit segment, which is the main revenue contributor, and the lower gross profit margins across all three product segments for the reasons previously mentioned, despite effective expense management and lower finance costs. ____________________________________________________________________________________________________________________________________

  `MDA_CH_FY2025` · `p034` · SHA 07152c9bc603
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ปริมาณขายและปริมาณการผลิต และ ยอดขายส่งออกและตลาดต่างประเทศ และ เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ ความเสี่ยงด้านภูมิรัฐศาสตร์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Other Income and Foreign Exchange Gain (Loss): 2025 vs 2024 Other income increased by 7.82% compared to the same period of the previous year. The main reason was the recognition of gains from fair value measurement of forward contracts, reflecting significantly improved foreign exchange risk management for import and export transactions compared to the previous year when the Group recorded losses from this item. In addition, income from the sale of scrap materials from the healthy snacks segment increased in line with higher production volumes. The Company also received non-recurring income, including refunds of social security contributions under Sections 33 and 39 for flood relief assistan

  `MDA_CH_FY2025` · `p030` · SHA 26532591a802
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ยอดขายส่งออกและตลาดต่างประเทศ และ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายภาษี
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Profit (Loss) before income tax expenses (17.15) -1.01% 154.63 6.80% N.A. Income tax expenses (0.67) -0.04% (27.48) (1.21%) -97.56% Profit (Loss) for the year (17.82) -1.05% 127.15 5.59% N.A. Remark: /1 - Other incomes include income from export compensation, profit from asset disposal, income from scrap sales, rental income, and profit from fair value measurement of derivative instruments. ____________________________________________________________________________________________________________________________________

  `MDA_CH_FY2025` · `p016` · SHA d1207c89a679
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_CH_FY2025`

##### XBIO — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เอ็กซ์ ไบโอไซเอนซ์ จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัทฯ มีการลงทุนในธุรกิจอาหาร

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 973m | 0.08 | -11.6% | n.m. | -361.6% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 6 · NPAT 14 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 8

**RFO — เพราะอะไร** — FY2024 THB 319m → FY2025 THB 130m · −190m · -59.4%

- RFO ปี 2568 อยู่ที่ 130 ลบ. ลด 59.4% YoY; MD&A ระบุว่า รายได้ รายได้ค่าบริหารจัดการ 0.10 - 0.10 0.00% รายได้จากการขาย 129.55 319.24 (189.69) -59.42% ต้นทุนขาย (76.61) (180.63) 104.02 -57.59% กำไรขัÊนต้น 53.04 138.61 (85.57) -61.73% กำไรจากการสูญเสียการควบคุม 18.53 - 18.53 0.00% รายได้อืÉน 6.26 7.58 (1.32) -17.41% กำไรก่อนค่าใช้จ่าย 77.83 146.19 (68.36) -46.76% ค่าใช้จ่ายในการขาย (77.06) (166.97) 89.91 -53.85% ค่าใช้จ่ายในการบริหาร (173.54) (123.53) (50.01) 40.48% ค่าตัดจำหน่ายเครืÉองหมายการค้าและค่าความนิยม (109.81) (99.32) (10.49) 10.56% ผลขาดทุนจากการด้อยค่าสินทรัพย์ไม่หมุนเวียนทีÉถือไว้เพืÉอขาย (146.94) -
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้ รายได้ค่าบริหารจัดการ 0.10 - 0.10 0.00% รายได้จากการขาย 129.55 319.24 (189.69) -59.42% ต้นทุนขาย (76.61) (180.63) 104.02 -57.59% กำไรขัÊนต้น 53.04 138.61 (85.57) -61.73% กำไรจากการสูญเสียการควบคุม 18.53 - 18.53 0.00% รายได้อืÉน 6.26 7.58 (1.32) -17.41% กำไรก่อนค่าใช้จ่าย 77.83 146.19 (68.36) -46.76% ค่าใช้จ่ายในการขาย (77.06) (166.97) 89.91 -53.85% ค่าใช้จ่ายในการบริหาร (173.54) (123.53) (50.01) 40.48% ค่าตัดจำหน่ายเครืÉองหมายการค้าและค่าความนิยม (109.81) (99.32) (10.49) 10.56% ผลขาดทุนจากการด้อยค่าสินทรัพย์ไม่หมุนเวียนทีÉถือไว้เพืÉอขาย (146.94) - (146.94) 0.00% รวมค่าใช้จ่าย (507.35) (389.82) (117.53) 30.15% ขาดทุนก่อนต้นทุนทางการเงินและรายได้ภาษีเงินได้ (429.52) (243.63) (185.89) 76

  `MDA_XBIO_FY2025` · `p007` · SHA 4a3262849378
  </details>
- RFO ปี 2568 อยู่ที่ 130 ลบ. ลด 59.4% YoY; MD&A ระบุว่า สาเหตุสำคัญมาจากการด้อยค่าของสินทรัพย์ การลดจำนวนสาขาของร้านอาหารและการยกเลิกร้านขนมอบ ดังนีÊ  รายได้จากการขาย รายได้จากการขายของบริษัทและบริษัทย่อยสำหรับปี 2568 ลดลงจากปี 2567 เป็นจำนวน 189.69 ล้าน บาท หรือประมาณร้อยละ 59.42 เป็นผลมาจากจำนวนสาขาในปี 2568 มีจำนวนน้อยกว่าปี 2567 จำนวน 7 สาขา ในปี 2568 และตามสภาวะเศรษฐกิจของประเทศทีÉอยู่ในช่วงซบเซา ส่งผลให้การจับจ่ายใช้สอยของประชาชนใน
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > สาเหตุสำคัญมาจากการด้อยค่าของสินทรัพย์ การลดจำนวนสาขาของร้านอาหารและการยกเลิกร้านขนมอบ ดังนีÊ  รายได้จากการขาย รายได้จากการขายของบริษัทและบริษัทย่อยสำหรับปี 2568 ลดลงจากปี 2567 เป็นจำนวน 189.69 ล้าน บาท หรือประมาณร้อยละ 59.42 เป็นผลมาจากจำนวนสาขาในปี 2568 มีจำนวนน้อยกว่าปี 2567 จำนวน 7 สาขา ในปี 2568 และตามสภาวะเศรษฐกิจของประเทศทีÉอยู่ในช่วงซบเซา ส่งผลให้การจับจ่ายใช้สอยของประชาชนใน

  `MDA_XBIO_FY2025` · `p008` · SHA 1b069d5fc519
  </details>
- RFO ปี 2568 อยู่ที่ 130 ลบ. ลด 59.4% YoY; MD&A ระบุว่า ด้อยค่าดังกล่าว  ต้นทุนทางการเงิน ต้นทุนทางการเงินของบริษัท และบริษัทย่อยลดลงจากปี 2567 จำนวน 8.07 ล้านบาท หรือคิดเป็นร้อยละ 23.53 เนืÉองจากการทยอยชำระหนีÊเจ้าหนีÊบุคคลภายนอก  รายได้ภาษีเงินได้ รายได้ภาษีเงินได้ของบริษัท และบริษัทย่อยลดลงจากปี 2567 จำนวน 12.59 ล้านบาท หรือคิดเป็นร้อย ละ 79.48 เนืÉองจากบริษัทได้กลับรายการหนีÊสินภาษีรอตัดบัญชีในระหว่างปีจากการตัดจำหน่ายเครืÉองหมาย
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ด้อยค่าดังกล่าว  ต้นทุนทางการเงิน ต้นทุนทางการเงินของบริษัท และบริษัทย่อยลดลงจากปี 2567 จำนวน 8.07 ล้านบาท หรือคิดเป็นร้อยละ 23.53 เนืÉองจากการทยอยชำระหนีÊเจ้าหนีÊบุคคลภายนอก  รายได้ภาษีเงินได้ รายได้ภาษีเงินได้ของบริษัท และบริษัทย่อยลดลงจากปี 2567 จำนวน 12.59 ล้านบาท หรือคิดเป็นร้อย ละ 79.48 เนืÉองจากบริษัทได้กลับรายการหนีÊสินภาษีรอตัดบัญชีในระหว่างปีจากการตัดจำหน่ายเครืÉองหมาย

  `MDA_XBIO_FY2025` · `p014` · SHA 984309bd0f7b
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 260m → FY2025 −THB 469m · −209m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -469 ลบ. จาก -260 ลบ.; MD&A ระบุว่า รายได้ รายได้ค่าบริหารจัดการ 0.10 - 0.10 0.00% รายได้จากการขาย 129.55 319.24 (189.69) -59.42% ต้นทุนขาย (76.61) (180.63) 104.02 -57.59% กำไรขัÊนต้น 53.04 138.61 (85.57) -61.73% กำไรจากการสูญเสียการควบคุม 18.53 - 18.53 0.00% รายได้อืÉน 6.26 7.58 (1.32) -17.41% กำไรก่อนค่าใช้จ่าย 77.83 146.19 (68.36) -46.76% ค่าใช้จ่ายในการขาย (77.06) (166.97) 89.91 -53.85% ค่าใช้จ่ายในการบริหาร (173.54) (123.53) (50.01) 40.48% ค่าตัดจำหน่ายเครืÉองหมายการค้าและค่าความนิยม (109.81) (99.32) (10.49) 10.56% ผลขาดทุนจากการด้อยค่าสินทรัพย์ไม่หมุนเวียนทีÉถือไว้เพืÉอขาย (146.94) -
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้ รายได้ค่าบริหารจัดการ 0.10 - 0.10 0.00% รายได้จากการขาย 129.55 319.24 (189.69) -59.42% ต้นทุนขาย (76.61) (180.63) 104.02 -57.59% กำไรขัÊนต้น 53.04 138.61 (85.57) -61.73% กำไรจากการสูญเสียการควบคุม 18.53 - 18.53 0.00% รายได้อืÉน 6.26 7.58 (1.32) -17.41% กำไรก่อนค่าใช้จ่าย 77.83 146.19 (68.36) -46.76% ค่าใช้จ่ายในการขาย (77.06) (166.97) 89.91 -53.85% ค่าใช้จ่ายในการบริหาร (173.54) (123.53) (50.01) 40.48% ค่าตัดจำหน่ายเครืÉองหมายการค้าและค่าความนิยม (109.81) (99.32) (10.49) 10.56% ผลขาดทุนจากการด้อยค่าสินทรัพย์ไม่หมุนเวียนทีÉถือไว้เพืÉอขาย (146.94) - (146.94) 0.00% รวมค่าใช้จ่าย (507.35) (389.82) (117.53) 30.15% ขาดทุนก่อนต้นทุนทางการเงินและรายได้ภาษีเงินได้ (429.52) (243.63) (185.89) 76

  `MDA_XBIO_FY2025` · `p007` · SHA 4a3262849378
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -469 ลบ. จาก -260 ลบ.; MD&A ระบุว่า  ต้นทุนขายและกำไรขัÊนต้น ต้นทุนขายลดลงเป็นจำนวน 104.42 ล้านบาท หรือร้อยละ 57.59 และกำไรขัÊนต้นของบริษัทลดลงเป็น จำนวน 85.57 ล้านบาท หรือคิดเป็นร้อยละ 61.73 ซึÉงเป็นไปในทิศทางเดียวกันกับรายได้ทีÉลดลง  กำไรจากการสูญเสียการควบคุม ในระหว่างปี 2568 บริษัทได้มีการลดสัดส่วนการถือครองหุ้นของบริษัทย่อยจำนวนหนึÉง โดยบริษัทรับรู้ รายการดังกล่าวหลังจากลดสัดส่วนการถือหุ้นเป็นสินทรัพย์ไม่หมุนเวียนทีÉถือไว้เพืÉอขาย ส่งผลให้บริษัทได้รับรู้กำไร
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  >  ต้นทุนขายและกำไรขัÊนต้น ต้นทุนขายลดลงเป็นจำนวน 104.42 ล้านบาท หรือร้อยละ 57.59 และกำไรขัÊนต้นของบริษัทลดลงเป็น จำนวน 85.57 ล้านบาท หรือคิดเป็นร้อยละ 61.73 ซึÉงเป็นไปในทิศทางเดียวกันกับรายได้ทีÉลดลง  กำไรจากการสูญเสียการควบคุม ในระหว่างปี 2568 บริษัทได้มีการลดสัดส่วนการถือครองหุ้นของบริษัทย่อยจำนวนหนึÉง โดยบริษัทรับรู้ รายการดังกล่าวหลังจากลดสัดส่วนการถือหุ้นเป็นสินทรัพย์ไม่หมุนเวียนทีÉถือไว้เพืÉอขาย ส่งผลให้บริษัทได้รับรู้กำไร

  `MDA_XBIO_FY2025` · `p009` · SHA d3ae29f09949
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -469 ลบ. จาก -260 ลบ.; MD&A ระบุว่า รายการ 31 ธันวาคม 2568 31 ธันวาคม 2567 1. อัตราส่วนประสิทธิภาพในการทำกำไรต่อสินทรัพย์รวม (ROA) (74.26) % (18.50) % 2.อัตราส่วนเงินทุนหมุนเวียน(Current Ratio) เท่า 0.93 เท่า 0.25 เท่า 3.อัตราส่วนหนีÊสินต่อส่วนของผู้ถือหุ้น (Debt to Equity Ratio) เท่า 1.73 เท่า 0.71เท่า 4.อัตราส่วนหนีÊสินทีÉมีภาระดอกเบีÊยต่อทุน (IBD/E Ratio) เท่า 1.08 เท่า 0.43เท่า  อัตราส่วนประสิทธิภาพในการทำกำไรต่อสินทรัพย์รวม (ROA) อัตราส่วน ROA ของบริษัทในปี 2568 ลดลง เมืÉอเปรียบเทียบกับอัตราส่วน ณ. วันสิÊนปี 2567จากผล ขาดทุนจากการดำเนินงานและการด้อยค่าค่าความนิยมและเครืÉองหมายการค้า
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายการ 31 ธันวาคม 2568 31 ธันวาคม 2567 1. อัตราส่วนประสิทธิภาพในการทำกำไรต่อสินทรัพย์รวม (ROA) (74.26) % (18.50) % 2.อัตราส่วนเงินทุนหมุนเวียน(Current Ratio) เท่า 0.93 เท่า 0.25 เท่า 3.อัตราส่วนหนีÊสินต่อส่วนของผู้ถือหุ้น (Debt to Equity Ratio) เท่า 1.73 เท่า 0.71เท่า 4.อัตราส่วนหนีÊสินทีÉมีภาระดอกเบีÊยต่อทุน (IBD/E Ratio) เท่า 1.08 เท่า 0.43เท่า  อัตราส่วนประสิทธิภาพในการทำกำไรต่อสินทรัพย์รวม (ROA) อัตราส่วน ROA ของบริษัทในปี 2568 ลดลง เมืÉอเปรียบเทียบกับอัตราส่วน ณ. วันสิÊนปี 2567จากผล ขาดทุนจากการดำเนินงานและการด้อยค่าค่าความนิยมและเครืÉองหมายการค้า รวมถึงการด้อยค่าสินทรัพย์ทีÉ

  `MDA_XBIO_FY2025` · `p020` · SHA 85116833b580
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -469 ลบ. จาก -260 ลบ.; MD&A ระบุว่า ด้อยค่าดังกล่าว  ต้นทุนทางการเงิน ต้นทุนทางการเงินของบริษัท และบริษัทย่อยลดลงจากปี 2567 จำนวน 8.07 ล้านบาท หรือคิดเป็นร้อยละ 23.53 เนืÉองจากการทยอยชำระหนีÊเจ้าหนีÊบุคคลภายนอก  รายได้ภาษีเงินได้ รายได้ภาษีเงินได้ของบริษัท และบริษัทย่อยลดลงจากปี 2567 จำนวน 12.59 ล้านบาท หรือคิดเป็นร้อย ละ 79.48 เนืÉองจากบริษัทได้กลับรายการหนีÊสินภาษีรอตัดบัญชีในระหว่างปีจากการตัดจำหน่ายเครืÉองหมาย
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ด้อยค่าดังกล่าว  ต้นทุนทางการเงิน ต้นทุนทางการเงินของบริษัท และบริษัทย่อยลดลงจากปี 2567 จำนวน 8.07 ล้านบาท หรือคิดเป็นร้อยละ 23.53 เนืÉองจากการทยอยชำระหนีÊเจ้าหนีÊบุคคลภายนอก  รายได้ภาษีเงินได้ รายได้ภาษีเงินได้ของบริษัท และบริษัทย่อยลดลงจากปี 2567 จำนวน 12.59 ล้านบาท หรือคิดเป็นร้อย ละ 79.48 เนืÉองจากบริษัทได้กลับรายการหนีÊสินภาษีรอตัดบัญชีในระหว่างปีจากการตัดจำหน่ายเครืÉองหมาย

  `MDA_XBIO_FY2025` · `p014` · SHA 984309bd0f7b
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: สาเหตุสำคัญมาจากการด้อยค่าของสินทรัพย์ การลดจำนวนสาขาของร้านอาหารและการยกเลิกร้านขนมอบ ดังนีÊ  รายได้จากการขาย รายได้จากการขายของบริษัทและบริษัทย่อยสำหรับปี 2568 ลดลงจากปี 2567 เป็นจำนวน 189.69 ล้าน บาท หรือประมาณร้อยละ 59.42 เป็นผลมาจากจำนวนสาขาในปี 2568 มีจำนวนน้อยกว่าปี 2567 จำนวน 7 สาขา ในปี 2568 และตามสภาวะเศรษฐกิจของประเทศทีÉอยู่ในช่วงซบเซา ส่งผลให้การจับจ่ายใช้สอยของประชาชนใน
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > สาเหตุสำคัญมาจากการด้อยค่าของสินทรัพย์ การลดจำนวนสาขาของร้านอาหารและการยกเลิกร้านขนมอบ ดังนีÊ  รายได้จากการขาย รายได้จากการขายของบริษัทและบริษัทย่อยสำหรับปี 2568 ลดลงจากปี 2567 เป็นจำนวน 189.69 ล้าน บาท หรือประมาณร้อยละ 59.42 เป็นผลมาจากจำนวนสาขาในปี 2568 มีจำนวนน้อยกว่าปี 2567 จำนวน 7 สาขา ในปี 2568 และตามสภาวะเศรษฐกิจของประเทศทีÉอยู่ในช่วงซบเซา ส่งผลให้การจับจ่ายใช้สอยของประชาชนใน

  `MDA_XBIO_FY2025` · `p008` · SHA 1b069d5fc519
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ในระหว่างปี 2568 บริษัทมีการรับรู้ขาดทุนจากการด้อยค่าค่าความนิยมและเครืÉองหมายการค้าของ บริษัทย่อยในค่าใช้จ่ายบริหาร จำนวน 98.57 ล้านบาทและ 16.73 ล้านบาทตามลำดับ การด้อยค่าเครืÉองหมาย การค้าและค่าความนิยมเพิÉมขึÊน 10.49 ล้านบาทหรือร้อยละ 10.56 เนืÉองจากมูลค่าทีÉคาดว่าจะได้รับมีมูลค่าตํÉากว่า มูลค่ากลุ่มของสินทรัพย์ทีÉก่อให้เกิดกระแสเงินสดเพราะยอดขายลดลงกว่าทีÉคาดการณ์ไว้ณ วันทีÉ 31 ธันวาคม 2568 บริษัทมีบัญชีค่าความนิยมและเครืÉองหมายการค้าคงเหลือจำนวน 123.38 ล้านบาทและ 53.06 ล้านบาท
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ในระหว่างปี 2568 บริษัทมีการรับรู้ขาดทุนจากการด้อยค่าค่าความนิยมและเครืÉองหมายการค้าของ บริษัทย่อยในค่าใช้จ่ายบริหาร จำนวน 98.57 ล้านบาทและ 16.73 ล้านบาทตามลำดับ การด้อยค่าเครืÉองหมาย การค้าและค่าความนิยมเพิÉมขึÊน 10.49 ล้านบาทหรือร้อยละ 10.56 เนืÉองจากมูลค่าทีÉคาดว่าจะได้รับมีมูลค่าตํÉากว่า มูลค่ากลุ่มของสินทรัพย์ทีÉก่อให้เกิดกระแสเงินสดเพราะยอดขายลดลงกว่าทีÉคาดการณ์ไว้ณ วันทีÉ 31 ธันวาคม 2568 บริษัทมีบัญชีค่าความนิยมและเครืÉองหมายการค้าคงเหลือจำนวน 123.38 ล้านบาทและ 53.06 ล้านบาท

  `MDA_XBIO_FY2025` · `p012` · SHA ca421223aa04
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_XBIO_FY2025`

##### F&D — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ฟู้ดแอนด์ดริ๊งส์ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัทประกอบธุรกิจหลักคือ ผลิตและจำหน่ายอาหารเพื่อส่งออกและขายในประเทศ โดยสินค้าอาหารดังกล่าว เป็นการแปรรูปผัก ผลไม้และเนื้อสัตว์เป็นอาหารนานาชนิด ขึ้นอยู่กับความต้องการของลูกค้า ทั้งนี้ สินค้าที่ผลิตรวมถึง ผัก ผลไม้ เครื่องเทศ อาหารบรรจุภาชนะปิดผนึก ผลิตภัณฑ์เนื้อปรุงรสบรรจุกระป๋อง และซอสเนื้อ ผัก ผลไม้ อาหารสำเร็จรูปพร้อมบริโภค (ready-to-eat) อาหารสำเร็จรูปแช่แข็ง น้ำผัก ผลไม้ และเครื่องดื่ม

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 806m | 45.75 | -18.3% | n.m. | 0.0% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 2 · NPAT 3 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 793m → FY2025 THB 581m · −212m · -26.7%

- RFO ปี 2568 อยู่ที่ 581 ลบ. ลด 26.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 1) Revenue from sales amounted to THB 581.10 million, a decrease of THB 208.91 million, or 26.44%, from 2024 (THB 790.01 million), mainly due to a decline in sales to customers in Cambodia.

  `MDA_F&D_FY2025` · `p004` · SHA 214084038b6c
  </details>
- RFO ปี 2568 อยู่ที่ 581 ลบ. ลด 26.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2) Cost of sales decreased by THB 150.12 million, in line with the reduction in

  `MDA_F&D_FY2025` · `p005` · SHA 625dc7840fab
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 81m → FY2025 THB 0m · −80m · -99.8%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 0.1 ลบ. ลด 99.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company reported a net profit of THB 0.13 million for the year 2025, representing a decrease of THB 80.50 million compared with the previous year, which recorded a net profit of THB 80.63 million. Earnings per share were THB 0.01 (2024: THB 4.57 per share), and the book value per share as of 31 December 2025 was THB 84.64 (2024: THB 81.13).

  `MDA_F&D_FY2025` · `p003` · SHA c9ceed8c9bdc
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 0.1 ลบ. ลด 99.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายภาษี และ การยุติธุรกิจหรือสายผลิตภัณฑ์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 3) Loss from discontinued operations, net of income tax, amounted to THB 27.59

  `MDA_F&D_FY2025` · `p006` · SHA d92b793f87bb
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 0.1 ลบ. ลด 99.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2) Cost of sales decreased by THB 150.12 million, in line with the reduction in

  `MDA_F&D_FY2025` · `p005` · SHA 625dc7840fab
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_F&D_FY2025`

##### CM — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เชียงใหม่โฟรเซ่นฟูดส์ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ผลิตและส่งออก ผักแปรรูปแช่แข็ง เช่น ถั่วแขกแช่แข็ง, ถั่วแระแช่แข็ง,ข้าวโพดหวานแช่แข็ง, ข้าวโพดฝักอ่อนแช่แข็ง และ ผักผสมแช่แข็ง

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 598m | 1.57 | -7.6% | n.m. | 1.9% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 3 · NPAT 5 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 1.2bn → FY2025 THB 1.1bn · −123m · -10.4%

- RFO ปี 2568 อยู่ที่ 1,058 ลบ. ลด 10.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ปริมาณขายและปริมาณการผลิต และ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > o Revenue from sales in quarter 4/2025 amounted to 238.07 million baht. This was an increase of 28.47 million baht or 13.6% compared to the same period in 2024, mainly due to an increase in sales volume of more than 11.7% compared to the same period last year. Revenue from sales in 2025 amounted to 1,057.52 million baht. This was partly due to a decrease in sales volume in the first half of the year. In addition, there is a shortage of raw materials due to the quality of agricultural raw materials due to the climate in the northern farming areas in 2024. There is also a shortage of raw materials due to a decrease in cultivation area due to price competition. And the continuous increase in th

  `MDA_CM_FY2025` · `p004` · SHA ea6f495aa88a
  </details>
- RFO ปี 2568 อยู่ที่ 1,058 ลบ. ลด 10.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ปริมาณขายและปริมาณการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > o Cost of sales in the quarter 4/2025 amounted to 219.16 million baht. An increase of 31.93 million baht or 17.1% compared to the same period in 2024. The cost of sales in 2025 amounted to 906.90 million baht, or a decrease of 3.2%, in line with a slight decrease in overall sales volume.

  `MDA_CM_FY2025` · `p005` · SHA f1600a083826
  </details>
- RFO ปี 2568 อยู่ที่ 1,058 ลบ. ลด 10.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2025-Q32024-Q42025-Q4YoYQoQ20242025Sales Revenue269.86 209.60 238.07 13.6%-11.8%1,180.72 1,057.52 -10.4%Cost of Goods Sold(224.43) (187.23) (219.16) 17.1%-2.3%(936.43) (906.90) -3.2%Gross Profit45.43 22.37 18.91 -15.5%-58.4%244.29 150.62 -38.3%Gain (Loss) on exchange rate10.43 17.22 2.99 -82.6%-71.3%3.80 24.73 551.2%Cost of Distributions(17.41) (17.97) (15.13) -15.8%-13.1%(77.62) (68.85) -11.3%Administrative Expenses(22.75) (24.86) (22.69) -8.7%-0.3%(87.48) (90.59) 3.6%Profit (Loss) before Tax18.63 (1.89) (14.72) 679.8%-179.0%93.29 25.02 -73.2%Tax income (expenses)(4.96) 0.24 (0.41) -273.7%-91.7%(0.45) (5.18) 1062.9%Net Profit (Loss)13.67 (1.65) (15.13) 816.0%-210.7%92.84 19.84 -78.6%Unit :

  `MDA_CM_FY2025` · `p006` · SHA 0f8a4aa45fec
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 93m → FY2025 THB 20m · −73m · -78.6%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 19.8 ลบ. ลด 78.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2025-Q32024-Q42025-Q4YoYQoQ20242025Sales Revenue269.86 209.60 238.07 13.6%-11.8%1,180.72 1,057.52 -10.4%Cost of Goods Sold(224.43) (187.23) (219.16) 17.1%-2.3%(936.43) (906.90) -3.2%Gross Profit45.43 22.37 18.91 -15.5%-58.4%244.29 150.62 -38.3%Gain (Loss) on exchange rate10.43 17.22 2.99 -82.6%-71.3%3.80 24.73 551.2%Cost of Distributions(17.41) (17.97) (15.13) -15.8%-13.1%(77.62) (68.85) -11.3%Administrative Expenses(22.75) (24.86) (22.69) -8.7%-0.3%(87.48) (90.59) 3.6%Profit (Loss) before Tax18.63 (1.89) (14.72) 679.8%-179.0%93.29 25.02 -73.2%Tax income (expenses)(4.96) 0.24 (0.41) -273.7%-91.7%(0.45) (5.18) 1062.9%Net Profit (Loss)13.67 (1.65) (15.13) 816.0%-210.7%92.84 19.84 -78.6%Unit :

  `MDA_CM_FY2025` · `p006` · SHA 0f8a4aa45fec
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 19.8 ลบ. ลด 78.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > o Net profit (loss) in 2025 was 19.84 million baht. This was a decrease of 73.01 million baht or 78.6% compared to 2024 due to the adjustment of deferred tax assets and reasons for income, costs, and especially the appreciation of the Baht mentioned above.

  `MDA_CM_FY2025` · `p012` · SHA fa4f07ccfd49
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 19.8 ลบ. ลด 78.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ปริมาณขายและปริมาณการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > o Cost of sales in the quarter 4/2025 amounted to 219.16 million baht. An increase of 31.93 million baht or 17.1% compared to the same period in 2024. The cost of sales in 2025 amounted to 906.90 million baht, or a decrease of 3.2%, in line with a slight decrease in overall sales volume.

  `MDA_CM_FY2025` · `p005` · SHA f1600a083826
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 19.8 ลบ. ลด 78.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > o Distribution and administrative expenses in 2025, the amount is 159.44 million baht. A slight decrease from last year amount 5.66 million baht or a decrease of 3.4% due to more effective overall cost control.

  `MDA_CM_FY2025` · `p011` · SHA 90f6e7ad1716
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ่ในเอกสำร ให้ใช้แท็บ 'เครื baht. The Company has a foreign exchange risk management policy by entering into foreign exchange
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > ่ในเอกสำร ให้ใช้แท็บ 'เครื baht. The Company has a foreign exchange risk management policy by entering into foreign exchange

  `MDA_CM_FY2025` · `p009` · SHA 982ea3c5f6d1
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_CM_FY2025`

##### SST — ตัวฉุด RFO · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ทรัพย์ศรีไทย จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ให้บริการจัดเก็บเอกสาร/ทรัพย์สิน ให้เช่าและบริหารพื้นที่เพื่อรองรับการจัดเก็บสินค้า รับบริหารจัดการสต๊อกสินค้า กิจการท่าเทียบเรือ รวมทั้งลงทุนในกิจการอาหาร เครื่องดื่ม และสินค้าแฟชั่นผ่านการถือหุ้นของบริษัทย่อย

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 537m | 1.02 | -30.1% | n.m. | -19.9% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 9 · NPAT 11 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 2

**RFO — เพราะอะไร** — FY2024 THB 3.4bn → FY2025 THB 2.7bn · −700m · -20.7%

- RFO ปี 2568 อยู่ที่ 2,685 ลบ. ลด 20.7% YoY; MD&A ระบุว่า ล้านบาท หรือลดลงร้อยละ 23 จากยอดขายธุรกิจอาหารที่ลดลง โดยสัดส่วน ต้นทุนในการขายสินค้าต่อ รายได้ รวมในปี 2568 และ ปี 2567 เท่ากับ 34.21% และ 34.35% ตามลำดับ 2.2) ต้นทุนในการบริการ 216 ล้านบาท (ปี 2567 มีต้นทุนในการบริการ 228 ล้านบาท) ลดลง 12 ล้านบาท หรือลดลงร้อยละ 5 โดยสัดส่วนต้นทุนในการบริการต่อรายได้รวมในปี 2567 และ ปี 2567 เท่ากับ 7.70% และ 6.35% ตามลำดับ 3.
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ล้านบาท หรือลดลงร้อยละ 23 จากยอดขายธุรกิจอาหารที่ลดลง โดยสัดส่วน ต้นทุนในการขายสินค้าต่อ รายได้ รวมในปี 2568 และ ปี 2567 เท่ากับ 34.21% และ 34.35% ตามลำดับ 2.2) ต้นทุนในการบริการ 216 ล้านบาท (ปี 2567 มีต้นทุนในการบริการ 228 ล้านบาท) ลดลง 12 ล้านบาท หรือลดลงร้อยละ 5 โดยสัดส่วนต้นทุนในการบริการต่อรายได้รวมในปี 2567 และ ปี 2567 เท่ากับ 7.70% และ 6.35% ตามลำดับ 3.

  `MDA_SST_FY2025` · `p013` · SHA 63af9e58d5d6
  </details>
- RFO ปี 2568 อยู่ที่ 2,685 ลบ. ลด 20.7% YoY; MD&A ระบุว่า ให้บริการรวม 366 ล้านบาท) ลดลงจากปีก่อน 26 ล้านบาท หรือลดลงร้อยละ 7 1.2) ธุรกิจอาหารและเครื่องดื่ม มีรายได้จากการขายรวม 2,088 ล้านบาท (ปี 2567 มีรายได้จากการขายรวม 2,724 ล้านบาท) ลดลงจากปีก่อน 636 ล้านบาท หรือลดลงร้อยละ 23 เนื่องจากกำลังซื้อของประชากร
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ให้บริการรวม 366 ล้านบาท) ลดลงจากปีก่อน 26 ล้านบาท หรือลดลงร้อยละ 7 1.2) ธุรกิจอาหารและเครื่องดื่ม มีรายได้จากการขายรวม 2,088 ล้านบาท (ปี 2567 มีรายได้จากการขายรวม 2,724 ล้านบาท) ลดลงจากปีก่อน 636 ล้านบาท หรือลดลงร้อยละ 23 เนื่องจากกำลังซื้อของประชากร

  `MDA_SST_FY2025` · `p006` · SHA c7c238d622bd
  </details>
- RFO ปี 2568 อยู่ที่ 2,685 ลบ. ลด 20.7% YoY; MD&A ระบุว่า ในประเทศที่ลดลง รวมถึงการปิดสาขาที่มีรายได้น้อยและสาขาที่ขาดทุนในระหว่างปี 1.3) ธุรกิจเสื้อผ้าสำเร็จรูป มีรายได้จากการขายรวม 257 ล้านบาท (ปี 2567 มีรายได้จากการขายรวม 295
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ในประเทศที่ลดลง รวมถึงการปิดสาขาที่มีรายได้น้อยและสาขาที่ขาดทุนในระหว่างปี 1.3) ธุรกิจเสื้อผ้าสำเร็จรูป มีรายได้จากการขายรวม 257 ล้านบาท (ปี 2567 มีรายได้จากการขายรวม 295

  `MDA_SST_FY2025` · `p007` · SHA cbc36b4b48b9
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 301m → FY2025 −THB 533m · −232m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -533 ลบ. จาก -301 ลบ.; MD&A ระบุว่า ล้านบาท หรือลดลงร้อยละ 23 จากยอดขายธุรกิจอาหารที่ลดลง โดยสัดส่วน ต้นทุนในการขายสินค้าต่อ รายได้ รวมในปี 2568 และ ปี 2567 เท่ากับ 34.21% และ 34.35% ตามลำดับ 2.2) ต้นทุนในการบริการ 216 ล้านบาท (ปี 2567 มีต้นทุนในการบริการ 228 ล้านบาท) ลดลง 12 ล้านบาท หรือลดลงร้อยละ 5 โดยสัดส่วนต้นทุนในการบริการต่อรายได้รวมในปี 2567 และ ปี 2567 เท่ากับ 7.70% และ 6.35% ตามลำดับ 3.
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ล้านบาท หรือลดลงร้อยละ 23 จากยอดขายธุรกิจอาหารที่ลดลง โดยสัดส่วน ต้นทุนในการขายสินค้าต่อ รายได้ รวมในปี 2568 และ ปี 2567 เท่ากับ 34.21% และ 34.35% ตามลำดับ 2.2) ต้นทุนในการบริการ 216 ล้านบาท (ปี 2567 มีต้นทุนในการบริการ 228 ล้านบาท) ลดลง 12 ล้านบาท หรือลดลงร้อยละ 5 โดยสัดส่วนต้นทุนในการบริการต่อรายได้รวมในปี 2567 และ ปี 2567 เท่ากับ 7.70% และ 6.35% ตามลำดับ 3.

  `MDA_SST_FY2025` · `p013` · SHA 63af9e58d5d6
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -533 ลบ. จาก -301 ลบ.; MD&A ระบุว่า และ ปี 2567 เท่ากับ 51.14 และ 48.90% ตามลำดับ 3.2) ค่าใช้จ่ายในการบริหาร 394 ล้านบาท (ปี 2567 มีค่าใช้จ่ายในการบริหาร 428 ล้านบาท) เพิ่มขึ้น 59 ล้าน บาท หรือเพิ่มขึ้นร้อยละ 16 จากค่าใช้จ่ายเกี่ยวกับพนักงาน ค่าใช้จ่ายจากการปิดสาขาที่ไม่ทำกำไร และ ค่าใช้จ่ายที่เกี่ยวข้องอื่นๆ ของร้านอาหารสาขาในต่างประเทศ โดยสัดส่วนค่าใช้จ่ายในการบริหารต่อ รายได้รวมในปี 2568 และ ปี 2567 เท่ากับ 14.06% และ 12.25% ตามลำดับ 3.3) ค่าใช้จ่ายอื่น 428 ล้านบาท (ปี 2567 มีค่าใช้จ่ายอื่นและผลขากทุนจากเงินตราต่างประเทศ 166 ล้าน บาท) เพิ่มขึ้น 262 ล้านบาท หรือเพิ่มขึ้นร้อยละ 157 จากการ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > และ ปี 2567 เท่ากับ 51.14 และ 48.90% ตามลำดับ 3.2) ค่าใช้จ่ายในการบริหาร 394 ล้านบาท (ปี 2567 มีค่าใช้จ่ายในการบริหาร 428 ล้านบาท) เพิ่มขึ้น 59 ล้าน บาท หรือเพิ่มขึ้นร้อยละ 16 จากค่าใช้จ่ายเกี่ยวกับพนักงาน ค่าใช้จ่ายจากการปิดสาขาที่ไม่ทำกำไร และ ค่าใช้จ่ายที่เกี่ยวข้องอื่นๆ ของร้านอาหารสาขาในต่างประเทศ โดยสัดส่วนค่าใช้จ่ายในการบริหารต่อ รายได้รวมในปี 2568 และ ปี 2567 เท่ากับ 14.06% และ 12.25% ตามลำดับ 3.3) ค่าใช้จ่ายอื่น 428 ล้านบาท (ปี 2567 มีค่าใช้จ่ายอื่นและผลขากทุนจากเงินตราต่างประเทศ 166 ล้าน บาท) เพิ่มขึ้น 262 ล้านบาท หรือเพิ่มขึ้นร้อยละ 157 จากการบันทึกด้อยค่าร้านอาหารที่ไม่มีกำไร และ

  `MDA_SST_FY2025` · `p019` · SHA 0d1948318c09
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -533 ลบ. จาก -301 ลบ.; MD&A ระบุว่า ตามที่บริษัทฯ ได้แจ้งผลการดำเนินงานประจำปี 2568 บริษัทฯและบริษัทย่อยมีผลขาดทุนสำหรับปี จำนวน 809.60 ล้านบาท เปรียบเทียบกับปี 2567 ซึ่งมีผลขาดทุนสำหรับปี จำนวน 430.29 ล้านบาท มีผลต่าง จำนวน 379.31 ล้านบาท หรือคิดเป็นอัตราร้อยละ 88 และ มีผลขาดทุนที่เป็นส่วนของผู้ถือหุ้นของบริษัท จำนวน 533.21 ล้านบาท เทียบกับปี 2567 ซึ่งมีผลขาดทุนที่เป็นส่วนของผู้ถือหุ้นของบริษัท จำนวน 300.76 ล้านบาท มี ผลต่าง 232.45 ล้านบาท หรือคิดเป็นอัตราร้อยละ 77 บริษัทฯ ขอเรียนชี้แจงสาเหตุหลักดังต่อไปนี้ รายได้จากการขายและให้บริการลูกค้าแยกตามส่วนงาน รวมทั้งรายได้อื่น ดังนี้ (ตามหมายเห
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ตามที่บริษัทฯ ได้แจ้งผลการดำเนินงานประจำปี 2568 บริษัทฯและบริษัทย่อยมีผลขาดทุนสำหรับปี จำนวน 809.60 ล้านบาท เปรียบเทียบกับปี 2567 ซึ่งมีผลขาดทุนสำหรับปี จำนวน 430.29 ล้านบาท มีผลต่าง จำนวน 379.31 ล้านบาท หรือคิดเป็นอัตราร้อยละ 88 และ มีผลขาดทุนที่เป็นส่วนของผู้ถือหุ้นของบริษัท จำนวน 533.21 ล้านบาท เทียบกับปี 2567 ซึ่งมีผลขาดทุนที่เป็นส่วนของผู้ถือหุ้นของบริษัท จำนวน 300.76 ล้านบาท มี ผลต่าง 232.45 ล้านบาท หรือคิดเป็นอัตราร้อยละ 77 บริษัทฯ ขอเรียนชี้แจงสาเหตุหลักดังต่อไปนี้ รายได้จากการขายและให้บริการลูกค้าแยกตามส่วนงาน รวมทั้งรายได้อื่น ดังนี้ (ตามหมายเหตุประกอบงบ

  `MDA_SST_FY2025` · `p004` · SHA ed4745c44f0d
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -533 ลบ. จาก -301 ลบ.; MD&A ระบุว่า หรือเพิ่มขึ้นร้อยละ 8 สำหรับงบแสดงฐานะการเงิน สิ้นสุดวันที่ 31 ธันวาคม 2568 บริษัทฯมีสินทรัพย์รวม 6,267 ล้านบาท (ปี 2567 มีสินทรัพย์รวม 7,271 ล้านบาท) ลดลง 1,004 ล้านบาท หรือลดลงร้อยละ 15 และ มีหนี้สินรวม 4,600 ล้านบาท (ปี 2567 มีหนี้สินรวม 4,809 ล้านบาท) ลดลง 208 ล้านบาท หรือ ลดลงร้อยละ 4 ทรัพย์สินรวมและหนี้สินรวมที่ลดลง หลักๆจาก การบันทึกด้อยค่าค่าความนิยม การตัดจำหน่ายทรัพย์สินและสัญญาเช่าที่เกี่ยวข้องกับสาขาที่ปิด ดำเนินการ และ การคืนหุ้นกู้ที่ครบกำหนด สำหรับอัตราส่วน หนี้สินรวมต่อส่วนของผู้ถือหุ้นรวม (D/E Ratio) ปี 2568 เท่ากับ 2.76เท่า (ปี 2567 เท่
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > หรือเพิ่มขึ้นร้อยละ 8 สำหรับงบแสดงฐานะการเงิน สิ้นสุดวันที่ 31 ธันวาคม 2568 บริษัทฯมีสินทรัพย์รวม 6,267 ล้านบาท (ปี 2567 มีสินทรัพย์รวม 7,271 ล้านบาท) ลดลง 1,004 ล้านบาท หรือลดลงร้อยละ 15 และ มีหนี้สินรวม 4,600 ล้านบาท (ปี 2567 มีหนี้สินรวม 4,809 ล้านบาท) ลดลง 208 ล้านบาท หรือ ลดลงร้อยละ 4 ทรัพย์สินรวมและหนี้สินรวมที่ลดลง หลักๆจาก การบันทึกด้อยค่าค่าความนิยม การตัดจำหน่ายทรัพย์สินและสัญญาเช่าที่เกี่ยวข้องกับสาขาที่ปิด ดำเนินการ และ การคืนหุ้นกู้ที่ครบกำหนด สำหรับอัตราส่วน หนี้สินรวมต่อส่วนของผู้ถือหุ้นรวม (D/E Ratio) ปี 2568 เท่ากับ 2.76เท่า (ปี 2567 เท่ากับ 1.95 เท่า) เพิ่มขึ้น 0.81 เท่า หรือเพิ่มขึ้นร้อยละ 41

  `MDA_SST_FY2025` · `p022` · SHA 0124fba9ec92
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: และ ปี 2567 เท่ากับ 51.14 และ 48.90% ตามลำดับ 3.2) ค่าใช้จ่ายในการบริหาร 394 ล้านบาท (ปี 2567 มีค่าใช้จ่ายในการบริหาร 428 ล้านบาท) เพิ่มขึ้น 59 ล้าน บาท หรือเพิ่มขึ้นร้อยละ 16 จากค่าใช้จ่ายเกี่ยวกับพนักงาน ค่าใช้จ่ายจากการปิดสาขาที่ไม่ทำกำไร และ ค่าใช้จ่ายที่เกี่ยวข้องอื่นๆ ของร้านอาหารสาขาในต่างประเทศ โดยสัดส่วนค่าใช้จ่ายในการบริหารต่อ รายได้รวมในปี 2568 และ ปี 2567 เท่ากับ 14.06% และ 12.25% ตามลำดับ 3.3) ค่าใช้จ่ายอื่น 428 ล้านบาท (ปี 2567 มีค่าใช้จ่ายอื่นและผลขากทุนจากเงินตราต่างประเทศ 166 ล้าน บาท) เพิ่มขึ้น 262 ล้านบาท หรือเพิ่มขึ้นร้อยละ 157 จากการ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > และ ปี 2567 เท่ากับ 51.14 และ 48.90% ตามลำดับ 3.2) ค่าใช้จ่ายในการบริหาร 394 ล้านบาท (ปี 2567 มีค่าใช้จ่ายในการบริหาร 428 ล้านบาท) เพิ่มขึ้น 59 ล้าน บาท หรือเพิ่มขึ้นร้อยละ 16 จากค่าใช้จ่ายเกี่ยวกับพนักงาน ค่าใช้จ่ายจากการปิดสาขาที่ไม่ทำกำไร และ ค่าใช้จ่ายที่เกี่ยวข้องอื่นๆ ของร้านอาหารสาขาในต่างประเทศ โดยสัดส่วนค่าใช้จ่ายในการบริหารต่อ รายได้รวมในปี 2568 และ ปี 2567 เท่ากับ 14.06% และ 12.25% ตามลำดับ 3.3) ค่าใช้จ่ายอื่น 428 ล้านบาท (ปี 2567 มีค่าใช้จ่ายอื่นและผลขากทุนจากเงินตราต่างประเทศ 166 ล้าน บาท) เพิ่มขึ้น 262 ล้านบาท หรือเพิ่มขึ้นร้อยละ 157 จากการบันทึกด้อยค่าร้านอาหารที่ไม่มีกำไร และ

  `MDA_SST_FY2025` · `p019` · SHA 0d1948318c09
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: หรือเพิ่มขึ้นร้อยละ 8 สำหรับงบแสดงฐานะการเงิน สิ้นสุดวันที่ 31 ธันวาคม 2568 บริษัทฯมีสินทรัพย์รวม 6,267 ล้านบาท (ปี 2567 มีสินทรัพย์รวม 7,271 ล้านบาท) ลดลง 1,004 ล้านบาท หรือลดลงร้อยละ 15 และ มีหนี้สินรวม 4,600 ล้านบาท (ปี 2567 มีหนี้สินรวม 4,809 ล้านบาท) ลดลง 208 ล้านบาท หรือ ลดลงร้อยละ 4 ทรัพย์สินรวมและหนี้สินรวมที่ลดลง หลักๆจาก การบันทึกด้อยค่าค่าความนิยม การตัดจำหน่ายทรัพย์สินและสัญญาเช่าที่เกี่ยวข้องกับสาขาที่ปิด ดำเนินการ และ การคืนหุ้นกู้ที่ครบกำหนด สำหรับอัตราส่วน หนี้สินรวมต่อส่วนของผู้ถือหุ้นรวม (D/E Ratio) ปี 2568 เท่ากับ 2.76เท่า (ปี 2567 เท่
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > หรือเพิ่มขึ้นร้อยละ 8 สำหรับงบแสดงฐานะการเงิน สิ้นสุดวันที่ 31 ธันวาคม 2568 บริษัทฯมีสินทรัพย์รวม 6,267 ล้านบาท (ปี 2567 มีสินทรัพย์รวม 7,271 ล้านบาท) ลดลง 1,004 ล้านบาท หรือลดลงร้อยละ 15 และ มีหนี้สินรวม 4,600 ล้านบาท (ปี 2567 มีหนี้สินรวม 4,809 ล้านบาท) ลดลง 208 ล้านบาท หรือ ลดลงร้อยละ 4 ทรัพย์สินรวมและหนี้สินรวมที่ลดลง หลักๆจาก การบันทึกด้อยค่าค่าความนิยม การตัดจำหน่ายทรัพย์สินและสัญญาเช่าที่เกี่ยวข้องกับสาขาที่ปิด ดำเนินการ และ การคืนหุ้นกู้ที่ครบกำหนด สำหรับอัตราส่วน หนี้สินรวมต่อส่วนของผู้ถือหุ้นรวม (D/E Ratio) ปี 2568 เท่ากับ 2.76เท่า (ปี 2567 เท่ากับ 1.95 เท่า) เพิ่มขึ้น 0.81 เท่า หรือเพิ่มขึ้นร้อยละ 41

  `MDA_SST_FY2025` · `p022` · SHA 0124fba9ec92
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_SST_FY2025`

#### ทะเบียนข้อสรุป — F9

| ส่วน | ประเภท | ข้อสรุป | รหัสแหล่งข้อมูล |
|---|---|---|---|
| headline | ข้ออนุมานนักวิเคราะห์ | กลุ่มที่สอบทานแล้วพลิกเป็นขาดทุน และ P/E headline ไม่เป็นตัวแทน | FY_PANEL, F9_E1, F9_E2, F9_E3, F9_E4 |
| earnings_fact | ข้อเท็จจริงจากการคำนวณ | FY2025 RFO -9.8%; สถานะ NPAT ส่วนผู้ถือหุ้น: turned_to_loss | FY_PANEL, CM_FY2025_MDA |
| why | ข้อเท็จจริงจากการคำนวณ | กลุ่ม 8 บริษัทมี RFO -9.8% และพลิกจากกำไร 450.6 ล้านบาทเป็นขาดทุน 914.5 ล้านบาท | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | CM ใช้ FY2024 แบบงบเฉพาะกิจการให้ฐานตรงกัน และยกเลิกการเทียบ consolidated กับ separate | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | P/E ของผู้มีกำไรครอบคลุมเพียง SUN และ SSF จึงอธิบายกลุ่มที่ขาดทุนไม่ได้ | FY_PANEL |
| causal_chain | ข้ออนุมานนักวิเคราะห์ | ห่วงโซ่เหตุ: ผลผลิต / คำสั่งซื้อ → Utilization → ต้นทุนต่อหน่วย → Cash flow → ฐานะการเงิน | F9_E1, F9_E2, F9_E3, F9_E4 |
| roles | ข้ออนุมานนักวิเคราะห์ | บทบาท: ผู้นำและตัวฉุดราคามากสุด — SUN; ตัวฉุด RFO — SST; ตัวฉุดกำไร — APURE | FY_PANEL, F9_E1, F9_E2, F9_E3, F9_E4 |
| valuation | ข้ออนุมานนักวิเคราะห์ | P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 12.7x ครอบคลุม 2/8 บริษัท และ 35.8% ของ market cap ที่มีข้อมูล. P/E ของผู้มีกำไรไม่เป็นตัวแทนกลุ่มที่ขาดทุน | SET_PUBLIC_EOD, F9_E1, F9_E2, F9_E3, F9_E4 |
| trigger | ประเด็นที่ต้องพิสูจน์ | คำสั่งซื้อฟื้น | F9_E1, F9_E2, F9_E3, F9_E4 |
| trigger | ประเด็นที่ต้องพิสูจน์ | utilization ดีขึ้น | F9_E1, F9_E2, F9_E3, F9_E4 |
| trigger | ประเด็นที่ต้องพิสูจน์ | ปรับโครงสร้างหน่วยธุรกิจขาดทุน | F9_E1, F9_E2, F9_E3, F9_E4 |
| risk | ประเด็นที่ต้องพิสูจน์ | ขาดทุนดำเนินงานต่อเนื่อง | F9_E1, F9_E2, F9_E3, F9_E4 |
| risk | ประเด็นที่ต้องพิสูจน์ | เงินทุนหมุนเวียนตึงตัว | F9_E1, F9_E2, F9_E3, F9_E4 |
| risk | ประเด็นที่ต้องพิสูจน์ | สภาพคล่องหุ้นต่ำและ event risk | F9_E1, F9_E2, F9_E3, F9_E4 |
| must_prove | ประเด็นที่ต้องพิสูจน์ | 6M26 ต้องเห็นขาดทุนดำเนินงานลดลง การฟื้นของ ECL และลูกหนี้ APURE และกระแสเงินสดดำเนินงานกลับปกติก่อนที่ valuation จะมีความหมาย | F9_E1, F9_E2, F9_E3, F9_E4 |

#### ทะเบียนหลักฐาน — F9

- **`FY_PANEL`** · _ข้อเท็จจริงจากการคำนวณ_ — Audited FY2024-25 company panel
  - RFO / NPAT-to-owners / independent panel membership; QA 43 pass / 0 fail
  - บทบาท: historical fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_company_fy2024_2025_audited_2026-08-07.csv`
  - SHA-256: `e5e04dbc40ffcc79fed58545a93dc4549c29cdaecf260bea73711bc6d0720481`
- **`SET_PUBLIC_EOD`** · _ข้อเท็จจริงจากการคำนวณ_ — SET public Company Highlights — EOD 2026-08-07
  - Adjusted YTD; unadjusted price, market cap and valuation; factsheet-surface cross-check
  - บทบาท: current market fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_set_public_surface_reconciliation_2026-08-07.csv`
  - SHA-256: `544c1f29fe2d409ee398822ac2bf32b769081718962ae2d1138985b0146b9530`
- **`SET_COMPANY_PROFILE`** · _ข้อเท็จจริง_ — SET company profiles — English and Thai
  - Official company names and business descriptions refreshed and validated for the 118-company perimeter from the public SET profile API
  - บทบาท: company business profile
  - URL: <https://www.set.or.th/th/market/product/stock/overview>
- **`COMPANY_REPORTS`** · _ข้ออนุมานนักวิเคราะห์_ — Company report synthesis corpus
  - Annual-only draft synthesis; reconciled to the ticker FY2025 MD&A where available
  - บทบาท: secondary synthesis; not management attribution
  - พาธ: `data/company-reports.json`
  - SHA-256: `c1a2bc40cbe21a2058aa596c362e4d47ad117360831b847de78ec414831fd2d2`
- **`MDA_SUN_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — SUN FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SUN/MDA_SUN_2025FY_E.md`
  - SHA-256: `33dea696bb638ca4ced93333c309c4260f87e787cce8d82aeae77f114ce60094`
  - URL: <https://weblink.set.or.th/dat/news/202602/1407NWS230220261805031970E.pdf>
- **`MDA_APURE_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — APURE FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/APURE/MDA_APURE_2025FY_E.md`
  - SHA-256: `7ee093c2089be290c9d2f179595c9eadcfb115cc52082de467b3eabbc22605d8`
  - URL: <https://weblink.set.or.th/dat/news/202602/0343NWS270220260821066910E.pdf>
- **`MDA_SSF_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — SSF FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SSF/MDA_SSF_2025FY_E.md`
  - SHA-256: `ce0e390c15fc1807c8f22f880eb6c977c8c6b7e8e376c8eb623ef1efc2c68da2`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/0159NWS260220260632521690E.pdf>
- **`MDA_CH_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — CH FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/CH/MDA_CH_2025FY_E.md`
  - SHA-256: `697209f4ce7ffb13d2c21d059c4106ed9d2477c4c38e219d7e279cd837b979ab`
  - URL: <https://weblink.set.or.th/dat/news/202602/1715NWS240220262211025550E.pdf>
- **`MDA_XBIO_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — XBIO FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/XBIO/MDA_XBIO_2025FY_T.md`
  - SHA-256: `1023a6fb9954f87c038b9a34caa9d025fb8ca4644015e4ec5e5fd274f83f8e6d`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/0753NWS240220262155276290T.pdf>
- **`MDA_F&D_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — F&D FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/F&D/MDA_F&D_2025FY_E.md`
  - SHA-256: `22538e7f8ea622558475099d3c4596be852437b95de6695b2770efb2bb90c894`
  - URL: <https://weblink.set.or.th/dat/news/202603/0410NWS020320260637194240E.pdf>
- **`MDA_CM_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — CM FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/CM/MDA_CM_2025FY_E.md`
  - SHA-256: `38538e84ecba8d549ffd4e713125960ba55719b782c8b759659086362d21e6f9`
  - URL: <https://weblink.set.or.th/dat/news/202602/0317NWS270220260828105800E.pdf>
- **`MDA_SST_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — SST FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SST/MDA_SST_2025FY_T.md`
  - SHA-256: `eaec9fc78e1d9d372276b6a9eacb8c6de9c92a65629cf28f54f3974f3a4f0682`
  - URL: <https://weblink.set.or.th/dat/news/202603/0092NWS020320260733216940T.pdf>
- **`CM_FY2025_MDA`** · _คำอธิบายฝ่ายจัดการ_ — CM FY2025 filing / MD&A
  - Direct filing evidence for explicitly labelled RFO or NPAT override values
  - บทบาท: override value evidence
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/CM/MDA_CM_2025FY_E.md`
  - SHA-256: `38538e84ecba8d549ffd4e713125960ba55719b782c8b759659086362d21e6f9`
- **`F9_E1`** · _ฝ่ายจัดการ_ — SUN FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SUN/MDA_SUN_2025FY_E.md`
  - SHA-256: `33dea696bb638ca4ced93333c309c4260f87e787cce8d82aeae77f114ce60094`
- **`F9_E2`** · _ฝ่ายจัดการ_ — CM FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/CM/MDA_CM_2025FY_E.md`
  - SHA-256: `38538e84ecba8d549ffd4e713125960ba55719b782c8b759659086362d21e6f9`
- **`F9_E3`** · _ฝ่ายจัดการ_ — SST FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SST/MDA_SST_2025FY_T.md`
  - SHA-256: `eaec9fc78e1d9d372276b6a9eacb8c6de9c92a65629cf28f54f3974f3a4f0682`
- **`F9_E4`** · _ฝ่ายจัดการ_ — APURE FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/APURE/MDA_APURE_2025FY_E.md`
  - SHA-256: `7ee093c2089be290c9d2f179595c9eadcfb115cc52082de467b3eabbc22605d8`
- **`F9_FACTSHEET`** · _ข้อเท็จจริงจากการคำนวณ_ — SET Factsheet — SUN
  - Live leader cross-check
  - บทบาท: presentation-surface check
  - URL: <https://www.set.or.th/th/market/product/stock/quote/sun/factsheet>

---

## PROP — PROP: รายได้ประจำส่งมอบกำไร ขณะที่ FDI optionality ขับเคลื่อนความคาดหวัง

P3 มีความสอดคล้องระหว่างกำไรกับราคาชัดที่สุด ส่วน P2 และ P4 ราคาวิ่งนำกำไร ขณะที่ที่อยู่อาศัยยังถูกกดดันเชิงโครงสร้าง

1. P3 ใหญ่ที่สุดและเป็นกลุ่มเดียวที่ทั้ง RFO และ NPAT เติบโต
2. P2 เป็น mismatch แบบ expectation-led ที่สำคัญที่สุดสำหรับ 6M26
3. P/E ต่ำของ P1 สะท้อนความเสี่ยงกำลังซื้อ การโอน และ cash conversion

### กรอบการตัดสินใจ 3 มุมมอง

| มุมมอง | ตัวชี้วัด | ค่า | ครอบคลุม |
|---|---|---|---|
| 01 โครงสร้างตลาด | Market cap | THB 843bn | 58/60 มีข้อมูล |
|  | บริษัท | 60 |  |
|  | Segment ใหญ่สุด | P3 · 42.6% |  |
| 02 ผลประกอบการ FY2025 | RFO YoY | -9.2% | 54/60 |
|  | NPAT YoY | -17.7% | 54/60 |
|  | Segment ที่กำไรยืนยัน | 1/5 |  |
| 03 มุมมองตลาด | ราคา YTD ปรับแล้ว | +22.3% | 59/60 · 100.0% M-cap |
|  | P/E รวม | 11.4x | 38/60 · 96.4% M-cap |
|  | Segment ราคานำ | 3/5 |  |

FY2025 RFO THB 393bn (FY2024 THB 433bn) • FY2025 owner NPAT THB 54.0bn (FY2024 THB 65.6bn) • Margin 13.7% (FY2024 15.2%)

### ภาพรวมเชิงกราฟ

#### 01 · โครงสร้างตลาด — สัดส่วน Market Cap

_ขนาด Segment และผู้นำตลาด_

| Segment | สัดส่วน | Market cap | ผู้นำ |
|---|---|---|---|
| P3 ศูนย์การค้าและรายได้ประจำ | 42.6% | THB 359bn | CPN · 85% |
| P1 ที่อยู่อาศัยเพื่อขาย | 27.4% | THB 231bn | LH · 20% |
| P2 นิคมอุตสาหกรรมและโลจิสติกส์ | 15.8% | THB 133bn | WHA · 56% |
| P4 โรงแรมและมิกซ์ยูส | 13.0% | THB 109bn | AWC · 87% |
| P5 กระจายธุรกิจและปรับโครงสร้าง | 1.4% | THB 11.4bn | STELLA · 50% |

#### 02 · ผลประกอบการ FY2025 — ทิศทาง RFO และ NPAT ส่วนผู้ถือหุ้น

_FY2025 YoY_

| Segment | RFO YoY | RFO FY2025 | NPAT YoY | NPAT FY2025 |
|---|---|---|---|---|
| P3 ศูนย์การค้าและรายได้ประจำ | +0.6% | THB 68.6bn | +13.7% | THB 23.2bn |
| P1 ที่อยู่อาศัยเพื่อขาย | -11.8% | THB 231bn | -33.8% | THB 20.1bn |
| P2 นิคมอุตสาหกรรมและโลจิสติกส์ | -12.4% | THB 52.9bn | -29.8% | THB 8.6bn |
| P4 โรงแรมและมิกซ์ยูส | -2.0% | THB 33.1bn | -15.8% | THB 4.8bn |
| P5 กระจายธุรกิจและปรับโครงสร้าง | -14.2% | THB 7.9bn | ขาดทุนลดลง | −THB 2.7bn |

#### 03 · มุมมองตลาด — ราคาเทียบกับทิศทางกำไร

_NPAT YoY เทียบกับราคา YTD_

| Segment | NPAT YoY | ราคา YTD | Market cap | ควอดรันต์ |
|---|---|---|---|---|
| P3 ศูนย์การค้าและรายได้ประจำ | +13.7% | +25.1% | 42.6% | ราคาและกำไรตอบรับ |
| P1 ที่อยู่อาศัยเพื่อขาย | -33.8% | +1.6% | 27.4% | ราคานำ • กำไรยังไม่ยืนยัน |
| P2 นิคมอุตสาหกรรมและโลจิสติกส์ | -29.8% | +50.2% | 15.8% | ราคานำ • กำไรยังไม่ยืนยัน |
| P4 โรงแรมและมิกซ์ยูส | -15.8% | +38.2% | 13.0% | ราคานำ • กำไรยังไม่ยืนยัน |
| P5 กระจายธุรกิจและปรับโครงสร้าง | — | +42.3% | 1.4% | — |

#### 04 · มูลค่า — P/E รวมของบริษัทที่มีกำไร

_แสดงความครอบคลุมของข้อมูลควบคู่ทุกค่า_

| Segment | P/E | ครอบคลุม |
|---|---|---|
| P3 ศูนย์การค้าและรายได้ประจำ | 14.6x | 3/5 • 100% M-cap |
| P1 ที่อยู่อาศัยเพื่อขาย | 7.9x | 26/37 • 93% M-cap |
| P2 นิคมอุตสาหกรรมและโลจิสติกส์ | 10.7x | 6/9 • 99% M-cap |
| P4 โรงแรมและมิกซ์ยูส | 14.9x | 2/4 • 96% M-cap |
| P5 กระจายธุรกิจและปรับโครงสร้าง | 8.5x | 1/5 • 24% M-cap |

### แผนที่ Segment เรียงตาม Market Cap

_เรียงจากใหญ่ไปเล็ก_

| อันดับ | Segment | M-cap | RFO YoY | NPAT YoY | ราคา YTD | P/E | ผู้นำ | สัญญาณ |
|---|---|---|---|---|---|---|---|---|
| 1 | P3 ศูนย์การค้าและรายได้ประจำ (5 บริษัท) | 42.6% (4/5) | +0.6% (5/5) | +13.7% (5/5) | +25.1% (4/5 • 100% M-cap) | 14.6x (3/5 • 100% M-cap) | CPN · 85% | กำไรยืนยันราคา |
| 2 | P1 ที่อยู่อาศัยเพื่อขาย (37 บริษัท) | 27.4% (36/37) | -11.8% (33/37) | -33.8% (33/37) | +1.6% (37/37 • 100% M-cap) | 7.9x (26/37 • 93% M-cap) | LH · 20% | ยังถูกกดดัน |
| 3 | P2 นิคมอุตสาหกรรมและโลจิสติกส์ (9 บริษัท) | 15.8% (9/9) | -12.4% (9/9) | -29.8% (9/9) | +50.2% (9/9 • 100% M-cap) | 10.7x (6/9 • 99% M-cap) | WHA · 56% | ราคานำพื้นฐาน |
| 4 | P4 โรงแรมและมิกซ์ยูส (4 บริษัท) | 13.0% (4/4) | -2.0% (3/4) | -15.8% (3/4) | +38.2% (4/4 • 100% M-cap) | 14.9x (2/4 • 96% M-cap) | AWC · 87% | ราคานำพื้นฐาน |
| 5 | P5 กระจายธุรกิจและปรับโครงสร้าง (5 บริษัท) | 1.4% (5/5) | -14.2% (4/5) | ขาดทุนลดลง (4/5) | +42.3% (5/5 • 100% M-cap) | 8.5x (1/5 • 24% M-cap) | STELLA · 50% | Event-driven |

### บทวิเคราะห์รายกลุ่มย่อย

### P3 · ศูนย์การค้าและรายได้ประจำ — รายได้ประจำส่งมอบความสอดคล้องของกำไรและราคาชัดที่สุด

`กำไรยืนยันราคา` · 42.6% M-cap · THB 359bn · 5 บริษัท

| ตัวชี้วัด | RFO | NPAT | ราคา | P/E |
|---|---|---|---|---|
| ช่วง | FY2025 YoY | ส่วนผู้ถือหุ้น FY2025 YoY | ราคา YTD ปรับแล้ว | เฉพาะบริษัทที่มีกำไร |
| ค่า | +0.6% | +13.7% | +25.1% | 14.6x |
| จำนวน | THB 68.6bn FY2025 | THB 23.2bn FY2025 | ณ 7 ส.ค. 2569 | ค่าเฉลี่ยรวม |
| ครอบคลุม | 5/5 | 5/5 | 4/5 • 100% M-cap | 3/5 • 100% M-cap |

**ข้อเท็จจริงที่สังเกตได้** — FY2025: RFO +0.6% • NPAT +13.7% • ราคา YTD +25.1% • P/E 14.6x • ครอบคลุม RFO 5/5 • NPAT 5/5

#### เหตุผลที่เปลี่ยน

1. _ข้อเท็จจริงจากการคำนวณ_ · Traffic — RFO เพิ่ม 0.6% และ NPAT ส่วนผู้ถือหุ้นเพิ่ม 13.7% ครบทั้ง 5 บริษัท
2. _คำอธิบายฝ่ายจัดการ_ · Occupancy — traffic, occupancy และรายได้ค่าเช่าประจำของ CPN เป็นฐานของกลุ่ม
3. _ข้ออนุมานนักวิเคราะห์_ · ค่าเช่า / NOI — MBK เป็นตัวเทียบแบบ diversified และกำไรทั้งหมดไม่ใช่หลักฐานการดำเนินงานศูนย์การค้า

#### ห่วงโซ่เหตุและผล

**Traffic** → **Occupancy** → **ค่าเช่า / NOI** → **Cash flow** → **Premium** (14.6x YTD +25.1%)

#### บทบาทในกลุ่ม

| บทบาท | Ticker | ค่า | ที่มาของค่า |
|---|---|---|---|
| ผู้นำและตัวเพิ่มกำไร | CPN | 85% | สัดส่วน Market Cap ในกลุ่ม |
| ตัวเทียบแบบ diversified | MBK | 10.4x | P/E · YTD +36.0% |

#### มูลค่า

**กำไรที่เกิดขึ้นแล้ว / ข้อเท็จจริง** — P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 14.6x ครอบคลุม 3/5 บริษัท และ 99.6% ของ market cap ที่มีข้อมูล. กระแสเงินสดประจำและคุณภาพ CPN สนับสนุน premium

| Trigger | Risk |
|---|---|
| traffic และ occupancy ดีขึ้น | การบริโภคชะลอ |
| rental reversion ยังเป็นบวก | กลุ่มกระจุกตัวใน CPN สูง |
| โครงการใหม่ ramp-up โดยไม่ลด margin | ความเสี่ยง capex และ ramp-up |

**6M26 ต้องพิสูจน์** — 6M26 ต้องรักษา NOI และ cash conversion ระหว่างขยายโครงการใหม่

#### วิเคราะห์รายบริษัท — P3 ศูนย์การค้าและรายได้ประจำ

_ทุกบริษัทใน perimeter ของ Segment ที่สอบทาน_

| Ticker | บทบาท | M-cap | RFO YoY | NPAT YoY | ราคา YTD | P/E | Margin |
|---|---|---|---|---|---|---|---|
| CPN | ผู้นำและตัวเพิ่มกำไร | THB 306bn | -1.1% | +12.6% | +23.5% | 15.6x | 36.5% |
| MBK | ตัวเทียบแบบ diversified | THB 47.2bn | +7.4% | +59.3% | +36.0% | 10.4x | 35.3% |
| PLAT | บริษัทในกลุ่ม | THB 3.9bn | +6.0% | +5.1% | +21.9% | 9.0x | 16.0% |
| J | บริษัทในกลุ่ม | THB 1.4bn | +8.8% | ขาดทุน | +34.3% | n.m. | -114.3% |
| GLAND | บริษัทในกลุ่ม | — | -3.6% | +3.1% | — | n.m. | 28.0% |

##### CPN — ผู้นำและตัวเพิ่มกำไร · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เซ็นทรัลพัฒนา จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาและให้เช่าพื้นที่ศูนย์การค้าขนาดใหญ่และประกอบธุรกิจอื่นที่เกี่ยวเนื่องและส่งเสริมธุรกิจพัฒนาศูนย์การค้า เช่น อาคารสำนักงาน ศูนย์อาหาร โรงแรม และที่พักอาศัย เป็นต้น รวมถึงการลงทุนในกองทุนรวมสิทธิการเช่าอสังหาริมทรัพย์ (CPNCG) และทรัสต์เพื่อการลงทุนในสิทธิการเช่าอสังหาริมทรัพย์ (CPNREIT) และเป็นผู้บริหารอสังหาริมทรัพย์ของกองทุนรวมฯ และกองทรัสต์ฯ

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 306bn | 68.25 | +23.5% | 15.6x | 36.5% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 52.2bn → FY2025 THB 51.6bn · −587m · -1.1%

- รายได้ประจำค่าเช่า/บริการโตจาก Central Park จำนวนผู้ใช้บริการ อัตราการเช่าพื้นที่ และค่าเช่าเดิม ขณะที่รายได้ที่อยู่อาศัยลด 30% จากตารางโอนและธนาคารเข้มสินเชื่อ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้จากการขายอสังหาริมทรัพย์ 1,976 626 2,630 33% 320% 6,231 4,351 (30%)

  `MDA_CPN_FY2025` · `p039` · SHA 9eedf8f88a77
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 16.7bn → FY2025 THB 18.8bn · +2.1bn · +12.6%

- กำไรหลักโตประมาณ 7% จากกำไรขั้นต้น รายได้อื่น และการคุม SG&A ขณะที่กำไรรายงานสูงกว่าเพราะรายการไม่ประจำ 2.119 พันลบ.
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไรสุทธิ ในไตรมาส 4 ปี 2568 บริษัทฯ มีกำไรสุทธิหลัก 4,786 ล้านบาท ปรับตัวดีขึ้นร้อยละ 19 จากปีก่อน และร้อยละ 14 จาก ไตรมาสก่อน ด้วยอัตรากำไรสุทธิที่ร้อยละ 32 (ไตรมาส 3 ปี 2568 อยู่ที่ร้อยละ 34 และไตรมาส 4 ปี 2567 อยู่ที่ร้อยละ 29) ส่งผลให้บริษัทฯ มีกำไรสุทธิปี 2568 สูงสุดเป็นประวัติการณ์ที่ 16,722 ล้านบาท เพิ่มขึ้นร้อยละ 7 จากปีก่อน

  `MDA_CPN_FY2025` · `p061` · SHA 95fd181709e7
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการไม่ประจำมาจากต่อสัญญาเช่า Rama 2/CPNREIT และดอกเบี้ย สัญญาเช่าการเงิน จึงควรใช้กำไรหลักอ่านแนวโน้ม

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_CPN_FY2025`

##### MBK — ตัวเทียบแบบ diversified · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เอ็ม บี เค จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ดำเนินธุรกิจศูนย์การค้า ธุรกิจโรงแรมและการท่องเที่ยว ธุรกิจกอล์ฟ ธุรกิจอสังหาริมทรัพย์ ธุรกิจอาหาร ธุรกิจการเงิน และธุรกิจการประมูล

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 47.2bn | 23.80 | +36.0% | 10.4x | 35.3% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 20 · NPAT 20 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 8

**RFO — เพราะอะไร** — FY2024 THB 11.3bn → FY2025 THB 12.1bn · +832m · +7.4%

- RFO ปี 2568 อยู่ที่ 12,110 ลบ. เพิ่ม 7.4% YoY; MD&A ระบุว่า มีการเปลี่ยนแปลงของรายได้ที่สำคัญมีดังนี้ ก) ธุรกิจศูนย์การค้ามีรายได้เพิ่มขึ้น 402 ล้านบาท คิดเป็นร้อยละ 12 โดยรายได้หลักที่เพิ่มขึ้นมาจาก ศูนย์การค้า เอ็มบีเค เซ็นเตอร์ จำนวน 317 ล้านบาท และศูนย์การค้าพาราไดซ์ พาร์ค จำนวน 55 ล้านบาท การเติบโตของรายได้ดังกล่าวเป็นผลมาจากการเพิ่มขึ้นของจำนวนนักท่องเที่ยวทั้งชาวไทยและชาวต่างชาติ ที่เข้ามาใช้บริการในศูนย์การค้ามากขึ้น การปรับเปลี่ยน Tenant ส่วนผสมธุรกิจ ให้สอดคล้องกับพฤติกรรมของผู้บริโภค ในยุคใหม่การเพิ่มพื้นที่สำหรับร้านอาหารและเครื่องดื่มยอดนิยมเพื่อให้มีการใช้พื้นที่อย่างมีประสิทธิภาพ มากขึ้น การจัดกิจกรรมส่งเสริ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > มีการเปลี่ยนแปลงของรายได้ที่สำคัญมีดังนี้ ก) ธุรกิจศูนย์การค้ามีรายได้เพิ่มขึ้น 402 ล้านบาท คิดเป็นร้อยละ 12 โดยรายได้หลักที่เพิ่มขึ้นมาจาก ศูนย์การค้า เอ็มบีเค เซ็นเตอร์ จำนวน 317 ล้านบาท และศูนย์การค้าพาราไดซ์ พาร์ค จำนวน 55 ล้านบาท การเติบโตของรายได้ดังกล่าวเป็นผลมาจากการเพิ่มขึ้นของจำนวนนักท่องเที่ยวทั้งชาวไทยและชาวต่างชาติ ที่เข้ามาใช้บริการในศูนย์การค้ามากขึ้น การปรับเปลี่ยน Tenant Mix ให้สอดคล้องกับพฤติกรรมของผู้บริโภค ในยุคใหม่การเพิ่มพื้นที่สำหรับร้านอาหารและเครื่องดื่มยอดนิยมเพื่อให้มีการใช้พื้นที่อย่างมีประสิทธิภาพ มากขึ้น การจัดกิจกรรมส่งเสริมการขายและอีเวนต์ที่ดึงดูดผู้บริโภค และการปรับปรุงครั้งใหญ่ของศูนย์การค้า พาราไดซ์ พาร์ค ซึ่งแล้วเสร็จในไตรมาสที่ 2 ของปี 2567 ปัจจัยเหล่านี

  `MDA_MBK_FY2025` · `p042` · SHA 50ff6c843e86
  </details>
- RFO ปี 2568 อยู่ที่ 12,110 ลบ. เพิ่ม 7.4% YoY; MD&A ระบุว่า 1.3 รายได้อื่น รายได้อื่นเพิ่มขึ้น 151 ล้านบาท คิดเป็นร้อยละ 83 โดยมีสาเหตุหลักจากการเพิ่มสัดส่วนการลงทุนในตราสารทุน ในความต้องการตลาด เพื่อบริหารจัดการสภาพคล่องส่วนเกินให้เกิดประโยชน์สูงสุด โดยมุ่งเน้นการลงทุนใน หลักทรัพย์ที่มีศักยภาพและมีประวัติการจ่ายเงินปันผลที่ดีอย่างสม่ำเสมอ ส่งผลให้รายได้เงินปันผลเพิ่มขึ้น
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > 1.3 รายได้อื่น รายได้อื่นเพิ่มขึ้น 151 ล้านบาท คิดเป็นร้อยละ 83 โดยมีสาเหตุหลักจากการเพิ่มสัดส่วนการลงทุนในตราสารทุน ในความต้องการตลาด เพื่อบริหารจัดการสภาพคล่องส่วนเกินให้เกิดประโยชน์สูงสุด โดยมุ่งเน้นการลงทุนใน หลักทรัพย์ที่มีศักยภาพและมีประวัติการจ่ายเงินปันผลที่ดีอย่างสม่ำเสมอ ส่งผลให้รายได้เงินปันผลเพิ่มขึ้น

  `MDA_MBK_FY2025` · `p031` · SHA 8214132237a2
  </details>
- RFO ปี 2568 อยู่ที่ 12,110 ลบ. เพิ่ม 7.4% YoY; MD&A ระบุว่า สินเชื่อที่มีคุณภาพเป็นหลัก ส่งผลให้หนี้ที่ไม่ก่อให้เกิดรายได้ (NPL) ลดลง • ธุรกิจให้กู้ยืมเงินโดยมีหลักทรัพย์ค้ำประกันมีรายได้เพิ่มขึ้น 53 ล้านบาท คิดเป็นร้อยละ 6 ช) ธุรกิจการประมูลมีรายได้ลดลง 49 ล้านบาท คิดเป็นร้อยละ 7 เนื่องจากจำนวนรถยนต์ที่เข้าลานประมูลลดลง
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > สินเชื่อที่มีคุณภาพเป็นหลัก ส่งผลให้หนี้ที่ไม่ก่อให้เกิดรายได้ (NPL) ลดลง • ธุรกิจให้กู้ยืมเงินโดยมีหลักทรัพย์ค้ำประกันมีรายได้เพิ่มขึ้น 53 ล้านบาท คิดเป็นร้อยละ 6 ช) ธุรกิจการประมูลมีรายได้ลดลง 49 ล้านบาท คิดเป็นร้อยละ 7 เนื่องจากจำนวนรถยนต์ที่เข้าลานประมูลลดลง

  `MDA_MBK_FY2025` · `p066` · SHA 89f76848f8d8
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 2.7bn → FY2025 THB 4.3bn · +1.6bn · +59.3%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 4,280 ลบ. เพิ่ม 59.3% YoY; MD&A ระบุว่า การเงินสำหรับปี 2567 ดังนี้ • ผลของรายการปรับปรุงต่องบกำไรขาดทุนเบ็ดเสร็จสำหรับปี 2567 มีดังนี้ส่วนแบ่งกำไรในบริษัทในบริษัท ร่วมเพิ่มขึ้น 2.4 ล้านบาท ค่าใช้จ่ายภาษีเงินได้เพิ่มขึ้น 0.5 ล้านบาท กำไรสุทธิสำหรับปีเพิ่มขึ้น 1.9 ล้านบาท และส่วนแบ่งกำไรขาดทุนเบ็ดเสร็จอื่นจากเงินลงทุนในบริษัทร่วมลดลง 0.6 ล้านบาท • ผลของรายการปรับปรุงต่องบฐานะการเงิน ณ วันที่ 31 ธันวาคม 2567 มีดังนี้ เงินลงทุนในบริษัทร่วมเพิ่มขึ้น 279 ล้านบาท (1%) หนี้สินภาษีเงินได้รอตัดบัญชีเพิ่มขึ้น 56 ล้านบาท (3%) กำไรสะสมที่ยังไม่ได้จัดสรร
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > การเงินสำหรับปี 2567 ดังนี้ • ผลของรายการปรับปรุงต่องบกำไรขาดทุนเบ็ดเสร็จสำหรับปี 2567 มีดังนี้ส่วนแบ่งกำไรในบริษัทในบริษัท ร่วมเพิ่มขึ้น 2.4 ล้านบาท ค่าใช้จ่ายภาษีเงินได้เพิ่มขึ้น 0.5 ล้านบาท กำไรสุทธิสำหรับปีเพิ่มขึ้น 1.9 ล้านบาท และส่วนแบ่งกำไรขาดทุนเบ็ดเสร็จอื่นจากเงินลงทุนในบริษัทร่วมลดลง 0.6 ล้านบาท • ผลของรายการปรับปรุงต่องบฐานะการเงิน ณ วันที่ 31 ธันวาคม 2567 มีดังนี้ เงินลงทุนในบริษัทร่วมเพิ่มขึ้น 279 ล้านบาท (1%) หนี้สินภาษีเงินได้รอตัดบัญชีเพิ่มขึ้น 56 ล้านบาท (3%) กำไรสะสมที่ยังไม่ได้จัดสรร

  `MDA_MBK_FY2025` · `p026` · SHA a61029246ff9
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 4,280 ลบ. เพิ่ม 59.3% YoY; MD&A ระบุว่า วางไว้ การตั้งค่าเผื่อการด้อยค่าดังกล่าวคำนวณโดยวิธีมูลค่าปัจจุบันของกระแสเงินสดสุทธิ (Discounted Cash Flows - DCF) ซึ่งแม้จะส่งผลกระทบต่อกำไรสุทธิในระยะสั้น แต่ถือเป็นการปรับฐานสินทรัพย์และค่าใช้จ่าย เพื่อสะท้อนสภาวะเศรษฐกิจในปัจจุบันอย่างเหมาะสม ทั้งนี้การลดลงของมูลค่าสินทรัพย์จะส่งผลให้ค่ำเสื่อม ราคาในอนาคตลดลง ซึ่งจะช่วยยกระดับอัตรากำไร (Profit อัตรากำไร) และสะท้อนภาพรวมผลการดำเนินงานที่ แท้จริงได้ดียิ่งขึ้นในอนาคต อย่างไรก็ตาม รายการปรับปรุงดังกล่าวเป็นรายการทางบัญชีที่ไม่มีผลกระทบต่อ กระแสเงินสด (Non-cash transaction) โดยบริษัทฯ ยังคงรักษาฐานะทางการเง
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > วางไว้ การตั้งค่าเผื่อการด้อยค่าดังกล่าวคำนวณโดยวิธีมูลค่าปัจจุบันของกระแสเงินสดสุทธิ (Discounted Cash Flows - DCF) ซึ่งแม้จะส่งผลกระทบต่อกำไรสุทธิในระยะสั้น แต่ถือเป็นการปรับฐานสินทรัพย์และค่าใช้จ่าย เพื่อสะท้อนสภาวะเศรษฐกิจในปัจจุบันอย่างเหมาะสม ทั้งนี้การลดลงของมูลค่าสินทรัพย์จะส่งผลให้ค่ำเสื่อม ราคาในอนาคตลดลง ซึ่งจะช่วยยกระดับอัตรากำไร (Profit Margin) และสะท้อนภาพรวมผลการดำเนินงานที่ แท้จริงได้ดียิ่งขึ้นในอนาคต อย่างไรก็ตาม รายการปรับปรุงดังกล่าวเป็นรายการทางบัญชีที่ไม่มีผลกระทบต่อ กระแสเงินสด (Non-cash transaction) โดยบริษัทฯ ยังคงรักษาฐานะทางการเงินที่แข็งแกร่งและมีสภาพ

  `MDA_MBK_FY2025` · `p080` · SHA 024dffc4fbf3
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 4,280 ลบ. เพิ่ม 59.3% YoY; MD&A ระบุว่า ก) สินทรัพย์ทางการเงินหมุนเวียนอื่น ส่วนใหญ่เป็นเงินลงทุนในตราสารหนี้และตราสารทุนในความ ต้องการตลาดที่วัดมูลค่ายุติธรรมผ่านกำไรขาดทุน (FVPL) และผ่านกำไรขาดทุนเบ็ดเสร็จ (FVOCI) มี ยอดคงเหลือเพิ่มขึ้น 3,180 ล้านบาท คิดเป็นร้อยละ 417 เนื่องจากมีการซื้อเงินลงทุนในตราสารทุนใน
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ก) สินทรัพย์ทางการเงินหมุนเวียนอื่น ส่วนใหญ่เป็นเงินลงทุนในตราสารหนี้และตราสารทุนในความ ต้องการตลาดที่วัดมูลค่ายุติธรรมผ่านกำไรขาดทุน (FVPL) และผ่านกำไรขาดทุนเบ็ดเสร็จ (FVOCI) มี ยอดคงเหลือเพิ่มขึ้น 3,180 ล้านบาท คิดเป็นร้อยละ 417 เนื่องจากมีการซื้อเงินลงทุนในตราสารทุนใน

  `MDA_MBK_FY2025` · `p085` · SHA 96586a3bcdaf
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 4,280 ลบ. เพิ่ม 59.3% YoY; MD&A ระบุว่า ได้ค่อนข้างแน่ที่จะมีกำไรทางภาษีในอนาคตเพียงพอที่จะใช้ประโยชน์จากผลขาดทุนดังกล่าว ตามที่ ระบุไว้ในข้อ 1.4 (ข) - ค่าใช้จ่ายภาษีเงินได้นอกจากนี้ยังมีการเพิ่มขึ้นจากการรับรู้ผลแตกต่าง ชั่วคราวจากการตั้งค่าเผื่อการด้อยค่าอาคารของธุรกิจศูนย์การค้าเป็นจำนวน 41 ล้านบาท ตามที่ระบุ ไว้ในข้อ 2.2 (ค) - กำไร(ขาดทุน)จากการดำเนินงาน – ตามส่วนงานธุรกิจ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ได้ค่อนข้างแน่ที่จะมีกำไรทางภาษีในอนาคตเพียงพอที่จะใช้ประโยชน์จากผลขาดทุนดังกล่าว ตามที่ ระบุไว้ในข้อ 1.4 (ข) - ค่าใช้จ่ายภาษีเงินได้นอกจากนี้ยังมีการเพิ่มขึ้นจากการรับรู้ผลแตกต่าง ชั่วคราวจากการตั้งค่าเผื่อการด้อยค่าอาคารของธุรกิจศูนย์การค้าเป็นจำนวน 41 ล้านบาท ตามที่ระบุ ไว้ในข้อ 2.2 (ค) - กำไร(ขาดทุน)จากการดำเนินงาน – ตามส่วนงานธุรกิจ

  `MDA_MBK_FY2025` · `p098` · SHA a1b9e18487b2
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ความต้องการตลาดที่วัดมูลค่ายุติธรรมผ่านกำไรขาดทุนเบ็ดเสร็จ-สุทธิจากการขาย จำนวน 2,749 ล้านบาท การซื้อเงินลงทุนเพิ่มขึ้นนี้เพื่อเป็นการบริหารสภาพคล่องทางการเงินให้เกิด ประโยชน์สูงสุด โดยได้เลือกลงทุนในหุ้นที่มีพื้นฐานแข็งแกร่งและฐานะการเงินมั่นคง และยอดเพิ่มขึ้น จำนวน 431 ล้านบาท เกิดจากการปรับเพิ่มขึ้นในมูลค่ายุติธรรมของเงินลงทุนซึ่งรับรู้การเปลี่ยนแปลง
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ความต้องการตลาดที่วัดมูลค่ายุติธรรมผ่านกำไรขาดทุนเบ็ดเสร็จ-สุทธิจากการขาย จำนวน 2,749 ล้านบาท การซื้อเงินลงทุนเพิ่มขึ้นนี้เพื่อเป็นการบริหารสภาพคล่องทางการเงินให้เกิด ประโยชน์สูงสุด โดยได้เลือกลงทุนในหุ้นที่มีพื้นฐานแข็งแกร่งและฐานะการเงินมั่นคง และยอดเพิ่มขึ้น จำนวน 431 ล้านบาท เกิดจากการปรับเพิ่มขึ้นในมูลค่ายุติธรรมของเงินลงทุนซึ่งรับรู้การเปลี่ยนแปลง

  `MDA_MBK_FY2025` · `p086` · SHA 898d25243bd2
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ก) สินทรัพย์ทางการเงินหมุนเวียนอื่น ส่วนใหญ่เป็นเงินลงทุนในตราสารหนี้และตราสารทุนในความ ต้องการตลาดที่วัดมูลค่ายุติธรรมผ่านกำไรขาดทุน (FVPL) และผ่านกำไรขาดทุนเบ็ดเสร็จ (FVOCI) มี ยอดคงเหลือเพิ่มขึ้น 3,180 ล้านบาท คิดเป็นร้อยละ 417 เนื่องจากมีการซื้อเงินลงทุนในตราสารทุนใน
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ก) สินทรัพย์ทางการเงินหมุนเวียนอื่น ส่วนใหญ่เป็นเงินลงทุนในตราสารหนี้และตราสารทุนในความ ต้องการตลาดที่วัดมูลค่ายุติธรรมผ่านกำไรขาดทุน (FVPL) และผ่านกำไรขาดทุนเบ็ดเสร็จ (FVOCI) มี ยอดคงเหลือเพิ่มขึ้น 3,180 ล้านบาท คิดเป็นร้อยละ 417 เนื่องจากมีการซื้อเงินลงทุนในตราสารทุนใน

  `MDA_MBK_FY2025` · `p085` · SHA 96586a3bcdaf
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_MBK_FY2025`

##### PLAT — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท เดอะ แพลทินัม กรุ๊ป จำกัด (มหาชน)** — รายได้และกำไรเคลื่อนไหวสอดคล้องกัน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาและให้เช่าอสังหาริมทรัพย์เพื่อการพาณิชย์ ประกอบด้วย1. ธุรกิจให้เช่าและบริการ 2. ธุรกิจโรงแรม 3. ธุรกิจอาคารสำนักงานให้เช่า4. ธุรกิจจําหน่ายอาหารและเครื่องดื่ม

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 3.9bn | 1.39 | +21.9% | 9.0x | 16.0% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 11 · NPAT 12 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 2.5bn → FY2025 THB 2.7bn · +152m · +6.0%

- RFO ปี 2568 อยู่ที่ 2,679 ลบ. เพิ่ม 6.0% YoY; MD&A ระบุว่า 3. โรงแรมม็อกซีÉ แบงคอก ราชประสงค์ 62% 63% 56% 49% 1.3 รายได้จากการขายอาหารและเครืÉองดืÉม ในไตรมาส 4/2568 บริษัทฯ มีรายได้จากการขายอาหารและเครืÉองดืÉม จำนวน 48.3 ล้านบาท ลดลงจำนวน 6.0 ล้านบาท หรือคิดเป็นร้อยละ 11 เมืÉอเทียบกับไตรมาส 4/2567 และสำหรับปี 2568 จำนวน 182.6 ล้านบาท ลดลง 30.0 ล้านบาท หรือคิดเป็นร้อยละ 14.1 เนืÉองจากจำนวนนักท่องเทีÉยวทีÉเข้ามาใช้บริการภายในศูนย์อาหารลดลง 1.4 รายได้อืÉน ในไตรมาส 4/2568 บริษัทฯ มีรายได้อืÉน จำนวน 2.6 ล้านบาท ลดลงจำนวน 7.1 ล้านบาท หรือคิดเป็นร้อยละ 73.2 เทียบกับไตรมาส 4/2567 และสำหรับปี 2568 จำนวน 28.0 ล้านบาท ลดลง
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > 3. โรงแรมม็อกซีÉ แบงคอก ราชประสงค์ 62% 63% 56% 49% 1.3 รายได้จากการขายอาหารและเครืÉองดืÉม ในไตรมาส 4/2568 บริษัทฯ มีรายได้จากการขายอาหารและเครืÉองดืÉม จำนวน 48.3 ล้านบาท ลดลงจำนวน 6.0 ล้านบาท หรือคิดเป็นร้อยละ 11 เมืÉอเทียบกับไตรมาส 4/2567 และสำหรับปี 2568 จำนวน 182.6 ล้านบาท ลดลง 30.0 ล้านบาท หรือคิดเป็นร้อยละ 14.1 เนืÉองจากจำนวนนักท่องเทีÉยวทีÉเข้ามาใช้บริการภายในศูนย์อาหารลดลง 1.4 รายได้อืÉน ในไตรมาส 4/2568 บริษัทฯ มีรายได้อืÉน จำนวน 2.6 ล้านบาท ลดลงจำนวน 7.1 ล้านบาท หรือคิดเป็นร้อยละ 73.2 เทียบกับไตรมาส 4/2567 และสำหรับปี 2568 จำนวน 28.0 ล้านบาท ลดลงจำนวน 2.8 ล้านบาท หรือคิดเป็นร้อยละ 9.1 เทียบ กับช่วงเวลาเดียวกันของปีก่อน โดยสาเหตุหลักเนืÉองจากการริบเงินประกันการเช่า เมืÉอเทียบกับปี 256

  `MDA_PLAT_FY2025` · `p031` · SHA 14444613aae6
  </details>
- RFO ปี 2568 อยู่ที่ 2,679 ลบ. เพิ่ม 6.0% YoY; MD&A ระบุว่า 1. รายได้รวม ไตรมาส 4/2568 บริษัทฯ มีรายได้รวมจำนวน 678.4 ล้านบาท ลดลงจำนวน 38.2 ล้านบาท หรือคิดเป็นร้อยละ 5.3 จากไตรมาสเดียวกันของปีก่อน และสำหรับปี 2568 บริษัทฯ มีรายได้รวม 2,707.0 ล้านบาท เพิÉมขึÊน 149.0 ล้านบาท คิดเป็นร้อยละ 5.8 โดยแยกตามประเภทธุรกิจของบริษัทฯ ตามรายละเอียดดังนีÊ 1.1 รายได้จากการให้เช่าและบริการ ในไตรมาส 4/2568 บริษัทฯ มีรายได้จากการให้เช่าและบริการ จำนวน 288.8 ล้านบาท เพิÉมขึÊนจำนวน 10.6 ล้านบาท หรือคิดเป็นร้อยละ 3.8 เทียบกับไตรมาส 4/2567 และสำหรับปี 2568 จำนวน 1,156.5 ล้านบาท เพิÉมขึÊนจำนวน 93.0 ล้านบาท คิดเป็นร้อยละ 8.7 เทียบกับช่
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > 1. รายได้รวม ไตรมาส 4/2568 บริษัทฯ มีรายได้รวมจำนวน 678.4 ล้านบาท ลดลงจำนวน 38.2 ล้านบาท หรือคิดเป็นร้อยละ 5.3 จากไตรมาสเดียวกันของปีก่อน และสำหรับปี 2568 บริษัทฯ มีรายได้รวม 2,707.0 ล้านบาท เพิÉมขึÊน 149.0 ล้านบาท คิดเป็นร้อยละ 5.8 โดยแยกตามประเภทธุรกิจของบริษัทฯ ตามรายละเอียดดังนีÊ 1.1 รายได้จากการให้เช่าและบริการ ในไตรมาส 4/2568 บริษัทฯ มีรายได้จากการให้เช่าและบริการ จำนวน 288.8 ล้านบาท เพิÉมขึÊนจำนวน 10.6 ล้านบาท หรือคิดเป็นร้อยละ 3.8 เทียบกับไตรมาส 4/2567 และสำหรับปี 2568 จำนวน 1,156.5 ล้านบาท เพิÉมขึÊนจำนวน 93.0 ล้านบาท คิดเป็นร้อยละ 8.7 เทียบกับช่วงเวลาเดียวกันของปีก่อน โดยการเพิÉมขึÊนของรายได้ เนืÉองจากศูนย์การค้า เดอะ แพลทินัม แฟชัÉนมอลล์ มีอัตราการเช่าพืÊนทีÉเฉลีÉยร้อยละ 93 ซึÉงเพิ

  `MDA_PLAT_FY2025` · `p025` · SHA 40b16897736c
  </details>
- RFO ปี 2568 อยู่ที่ 2,679 ลบ. เพิ่ม 6.0% YoY; MD&A ระบุว่า ภาพรวมธุรกิจสำหรับปี 2568 ผลการดำเนินงานของกลุ่ม บริษัท เดอะ แพลทินัม กรุ๊ป จำกัด (มหาชน) และ บริษัทย่อย (“บริษัทฯ”) ใน ไตรมาส 4 ปี 2568 กลุ่มบริษัทมีรายได้รวม 678.4 ล้านบาท และมีกำไรสุทธิ 108.6 ล้านบาท ลดลงเมืÉอเทียบกับไตรมาส 4 ปี 2567 (QoQ) เท่ากับ 38.2 ล้านบาท และ 37.8 ล้านบาท คิดเป็นร้อยละ 5 และ ร้อยละ 26 ตามลำดับ สำหรับผลการ ดำเนินงานสำหรับปีสิÊนสุดวันทีÉ 31 ธันวาคม 2568 กลุ่มบริษัทมีรายได้รวม 2,707.0 ล้านบาท และมีกำไรสุทธิ 429.8 ล้าน บาท เพิÉมขึÊนเมืÉอเทียบกับปี 2567 (YoY) เท่ากับ 149.0 ล้านบาท และ 20.8 ล้านบาท คิดเป็นร้อยละ 6 และร้อยละ 5 ตามลำดับ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ภาพรวมธุรกิจสำหรับปี 2568 ผลการดำเนินงานของกลุ่ม บริษัท เดอะ แพลทินัม กรุ๊ป จำกัด (มหาชน) และ บริษัทย่อย (“บริษัทฯ”) ใน ไตรมาส 4 ปี 2568 กลุ่มบริษัทมีรายได้รวม 678.4 ล้านบาท และมีกำไรสุทธิ 108.6 ล้านบาท ลดลงเมืÉอเทียบกับไตรมาส 4 ปี 2567 (QoQ) เท่ากับ 38.2 ล้านบาท และ 37.8 ล้านบาท คิดเป็นร้อยละ 5 และ ร้อยละ 26 ตามลำดับ สำหรับผลการ ดำเนินงานสำหรับปีสิÊนสุดวันทีÉ 31 ธันวาคม 2568 กลุ่มบริษัทมีรายได้รวม 2,707.0 ล้านบาท และมีกำไรสุทธิ 429.8 ล้าน บาท เพิÉมขึÊนเมืÉอเทียบกับปี 2567 (YoY) เท่ากับ 149.0 ล้านบาท และ 20.8 ล้านบาท คิดเป็นร้อยละ 6 และร้อยละ 5 ตามลำดับ โดยกลุ่มธุรกิจศูนย์การค้า และโรงแรม ยังมีอัตราการเติบโตอย่างต่อเนืÉองทัÊงจากอัตราการเช่าพืÊนทีÉ และอัตรา การเข้าพักทีÉเพิÉมขึÊน รวมถึงการปรั

  `MDA_PLAT_FY2025` · `p002` · SHA 2ec35442c6a4
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 409m → FY2025 THB 430m · +21m · +5.1%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 430 ลบ. เพิ่ม 5.1% YoY; MD&A ระบุว่า ราคาในส่วนของธุรกิจให้เช่าอาคารสำนักงาน 2.2 ต้นทุนการประกอบกิจการโรงแรม ในไตรมาส 4/2568 บริษัทฯ มีต้นทุนการประกอบกิจการโรงแรม จำนวน 152.6 ล้านบาท ลดลง 8.6 ล้านบาท หรือคิดเป็นร้อยละ 5.3 เทียบกับไตรมาส 4/2567 และสำหรับปี 2568 จำนวน 602.7 ล้านบาท เพิÉมขึÊน 30.2 ล้านบาท หรือ คิดเป็นร้อยละ 5.3 โดยการเพิÉมขึÊนของต้นทุนสัมพันธ์กับรายได้ และอัตราการเข้าพักทีÉเพิÉมขึÊน ซึÉงสัดส่วนการเพิÉมขึÊนของ ต้นทุนยังตํÉากว่าสัดส่วนของรายได้ทีÉเพิÉมขึÊน จากการทีÉบริษัทมีการควบคุมต้นทุนได้มีประสิทธิภาพ 2.3 ต้นทุนการขายอาหารและเครืÉองดืÉม ในไตรมาส 4/2568 บริษัทฯ มีต้นทุนขายอาหา
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ราคาในส่วนของธุรกิจให้เช่าอาคารสำนักงาน 2.2 ต้นทุนการประกอบกิจการโรงแรม ในไตรมาส 4/2568 บริษัทฯ มีต้นทุนการประกอบกิจการโรงแรม จำนวน 152.6 ล้านบาท ลดลง 8.6 ล้านบาท หรือคิดเป็นร้อยละ 5.3 เทียบกับไตรมาส 4/2567 และสำหรับปี 2568 จำนวน 602.7 ล้านบาท เพิÉมขึÊน 30.2 ล้านบาท หรือ คิดเป็นร้อยละ 5.3 โดยการเพิÉมขึÊนของต้นทุนสัมพันธ์กับรายได้ และอัตราการเข้าพักทีÉเพิÉมขึÊน ซึÉงสัดส่วนการเพิÉมขึÊนของ ต้นทุนยังตํÉากว่าสัดส่วนของรายได้ทีÉเพิÉมขึÊน จากการทีÉบริษัทมีการควบคุมต้นทุนได้มีประสิทธิภาพ 2.3 ต้นทุนการขายอาหารและเครืÉองดืÉม ในไตรมาส 4/2568 บริษัทฯ มีต้นทุนขายอาหารและเครืÉองดืÉม จำนวน 36.7 ล้านบาท ลดลง 3.3 ล้านบาท หรือคิด เป็นร้อยละ 8.3 เทียบกับไตรมาส 4/2567 และสำหรับปี 2568 จำนวน 137.5 ล้านบาท ลดลง 2

  `MDA_PLAT_FY2025` · `p034` · SHA 85e8743e7dc2
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 430 ลบ. เพิ่ม 5.1% YoY; MD&A ระบุว่า รายการ งวด ś เดือน งวด řŚ เดือน (หน่วย : ล้านบาท) 2568 2567 เพิÉมขึÊน (ลดลง) 2568 2567 เพิÉมขึÊน (ลดลง) ต้นทุนการให้เช่าและบริการ 159.4 130.1 29.3 22.5% 621.9 522.3 99.6 19.1% ต้นทุนการประกอบกิจการโรงแรม 152.6 161.2 (8.6) (5.3%) 602.7 572.5 30.2 5.3% ต้นทุนขายอาหารและเครืÉองดืÉม 36.7 40.0 (3.3) (8.3%) 137.5 160.0 (22.5) (14.1%) รวมต้นทุน 348.7 331.3 17.4 5.25% 1,362.1 1,254.8 107.3 8.5% 2.1 ต้นทุนในการให้เช่าและบริการ ในไตรมาส 4/2568 บริษัทฯ มีต้นทุนในการให้เช่าและบริการ จำนวน 159.4 ล้านบาท เพิÉมขึÊนจำนวน 29.3 ล้านบาท หรือคิดเป็นร้อยละ 22.5 เทียบกับไตรมา
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายการ งวด ś เดือน งวด řŚ เดือน (หน่วย : ล้านบาท) 2568 2567 เพิÉมขึÊน (ลดลง) 2568 2567 เพิÉมขึÊน (ลดลง) ต้นทุนการให้เช่าและบริการ 159.4 130.1 29.3 22.5% 621.9 522.3 99.6 19.1% ต้นทุนการประกอบกิจการโรงแรม 152.6 161.2 (8.6) (5.3%) 602.7 572.5 30.2 5.3% ต้นทุนขายอาหารและเครืÉองดืÉม 36.7 40.0 (3.3) (8.3%) 137.5 160.0 (22.5) (14.1%) รวมต้นทุน 348.7 331.3 17.4 5.25% 1,362.1 1,254.8 107.3 8.5% 2.1 ต้นทุนในการให้เช่าและบริการ ในไตรมาส 4/2568 บริษัทฯ มีต้นทุนในการให้เช่าและบริการ จำนวน 159.4 ล้านบาท เพิÉมขึÊนจำนวน 29.3 ล้านบาท หรือคิดเป็นร้อยละ 22.5 เทียบกับไตรมาส 4/2567 และสำหรับปี 2568 จำนวน 621.9 ล้านบาท เพิÉมขึÊนจำนวน 99.6 ล้านบาท หรือคิดเป็นร้อยละ 19.1 เทียบกับช่วงเวลาเดียวกันของปีก่อน โดยมีรายล

  `MDA_PLAT_FY2025` · `p033` · SHA ebeac5844884
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 430 ลบ. เพิ่ม 5.1% YoY; MD&A ระบุว่า อินน์ รีสอร์ท สมุย และโรงแรมม็อกซีÉ แบงคอก ราชประสงค์ - ค่าใช้จ่ายในการขายและบริหาร ธุรกิจให้เช่าอาคารสำนักงาน ไตรมาส 4/2568 เพิÉมขึÊน 2.8 ล้านบาท และ สำหรับปี 2568 เพิÉมขึÊน 2.9 ล้านบาท เนืÉองจากมีการจ่ายค่าบริหารจัดการอาคารในปี 2568 3.2 ต้นทุนทางการเงิน ในไตรมาส 4/2568 บริษัทฯ มีต้นทุนทางการเงิน จำนวน 42.3 ล้านบาท เพิÉมขึÊน 3.9 ล้านบาท หรือคิดเป็นร้อย ละ 10.2 เทียบกับไตรมาส 4/2567 และสำหรับปี 2568 จำนวน 170.8 ล้านบาท เพิÉมขึÊน 17.6 ล้านบาท หรือคิดเป็นร้อย ละ 11.5 โดยทีÉต้นทุนทางการเงินเกิดจากการรับรู้ต้นทุนทางการเงินจากสิทธิการเช่าและดอกเบีÊยเงินกู้ยืม
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > อินน์ รีสอร์ท สมุย และโรงแรมม็อกซีÉ แบงคอก ราชประสงค์ - ค่าใช้จ่ายในการขายและบริหาร ธุรกิจให้เช่าอาคารสำนักงาน ไตรมาส 4/2568 เพิÉมขึÊน 2.8 ล้านบาท และ สำหรับปี 2568 เพิÉมขึÊน 2.9 ล้านบาท เนืÉองจากมีการจ่ายค่าบริหารจัดการอาคารในปี 2568 3.2 ต้นทุนทางการเงิน ในไตรมาส 4/2568 บริษัทฯ มีต้นทุนทางการเงิน จำนวน 42.3 ล้านบาท เพิÉมขึÊน 3.9 ล้านบาท หรือคิดเป็นร้อย ละ 10.2 เทียบกับไตรมาส 4/2567 และสำหรับปี 2568 จำนวน 170.8 ล้านบาท เพิÉมขึÊน 17.6 ล้านบาท หรือคิดเป็นร้อย ละ 11.5 โดยทีÉต้นทุนทางการเงินเกิดจากการรับรู้ต้นทุนทางการเงินจากสิทธิการเช่าและดอกเบีÊยเงินกู้ยืมสถาบันการเงิน 3.3 ค่าใช้จ่ายภาษีเงินได้ ในไตรมาส 4/2568 บริษัทฯ มีค่าใช้จ่ายภาษีเงินได้จำนวน 53.2 ล้านบาท ลดลง 0.2 ล้านบาท หรือคิดเป็นร้อยละ

  `MDA_PLAT_FY2025` · `p037` · SHA 5018c40ea6f0
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 430 ลบ. เพิ่ม 5.1% YoY; MD&A ระบุว่า ภาพรวมธุรกิจสำหรับปี 2568 ผลการดำเนินงานของกลุ่ม บริษัท เดอะ แพลทินัม กรุ๊ป จำกัด (มหาชน) และ บริษัทย่อย (“บริษัทฯ”) ใน ไตรมาส 4 ปี 2568 กลุ่มบริษัทมีรายได้รวม 678.4 ล้านบาท และมีกำไรสุทธิ 108.6 ล้านบาท ลดลงเมืÉอเทียบกับไตรมาส 4 ปี 2567 (QoQ) เท่ากับ 38.2 ล้านบาท และ 37.8 ล้านบาท คิดเป็นร้อยละ 5 และ ร้อยละ 26 ตามลำดับ สำหรับผลการ ดำเนินงานสำหรับปีสิÊนสุดวันทีÉ 31 ธันวาคม 2568 กลุ่มบริษัทมีรายได้รวม 2,707.0 ล้านบาท และมีกำไรสุทธิ 429.8 ล้าน บาท เพิÉมขึÊนเมืÉอเทียบกับปี 2567 (YoY) เท่ากับ 149.0 ล้านบาท และ 20.8 ล้านบาท คิดเป็นร้อยละ 6 และร้อยละ 5 ตามลำดับ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ภาพรวมธุรกิจสำหรับปี 2568 ผลการดำเนินงานของกลุ่ม บริษัท เดอะ แพลทินัม กรุ๊ป จำกัด (มหาชน) และ บริษัทย่อย (“บริษัทฯ”) ใน ไตรมาส 4 ปี 2568 กลุ่มบริษัทมีรายได้รวม 678.4 ล้านบาท และมีกำไรสุทธิ 108.6 ล้านบาท ลดลงเมืÉอเทียบกับไตรมาส 4 ปี 2567 (QoQ) เท่ากับ 38.2 ล้านบาท และ 37.8 ล้านบาท คิดเป็นร้อยละ 5 และ ร้อยละ 26 ตามลำดับ สำหรับผลการ ดำเนินงานสำหรับปีสิÊนสุดวันทีÉ 31 ธันวาคม 2568 กลุ่มบริษัทมีรายได้รวม 2,707.0 ล้านบาท และมีกำไรสุทธิ 429.8 ล้าน บาท เพิÉมขึÊนเมืÉอเทียบกับปี 2567 (YoY) เท่ากับ 149.0 ล้านบาท และ 20.8 ล้านบาท คิดเป็นร้อยละ 6 และร้อยละ 5 ตามลำดับ โดยกลุ่มธุรกิจศูนย์การค้า และโรงแรม ยังมีอัตราการเติบโตอย่างต่อเนืÉองทัÊงจากอัตราการเช่าพืÊนทีÉ และอัตรา การเข้าพักทีÉเพิÉมขึÊน รวมถึงการปรั

  `MDA_PLAT_FY2025` · `p002` · SHA 2ec35442c6a4
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_PLAT_FY2025`

##### J — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เจเอเอส แอสเซ็ท จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ธุรกิจของบริษัทแบ่งออกเป็น 3 รูปแบบหลัก ดังนี้1. การบริหารจัดการพื้นที่เช่าภายในศูนย์การค้าในส่วนโทรศัพท์เคลื่อนที่และสินค้าเทคโนโลยี ภายใต้ชื่อ "IT Junction" 2. การพัฒนาและบริหารพื้นที่ในรูปแบบตลาดชุมชน ภายใต้ชื่อ "J Market" 3. การพัฒนาและบริหารพื้นที่ในรูปแบบศูนย์การค้าชุมชน ภายใต้ชื่อ "The Jas"

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.4bn | 0.94 | +34.3% | n.m. | -114.3% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 8

**RFO — เพราะอะไร** — FY2024 THB 631m → FY2025 THB 687m · +56m · +8.8%

- รายได้เพิ่มจาก ศูนย์การค้าชุมชน และ ธุรกิจดูแลผู้สูงอายุ ขยายตัว ชดเชยบางส่วนด้วยรายได้เช่าพื้นที่ IT Junction ที่ลดลง
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > 1) ธุรกิจพัฒนาศูนย์การค้าชุมชน 2) ธุรกิจการบริหารพื้นที่เช่า IT Junction บริษัทฯ มีรายได้จากธุรกิจพัฒนาศูนย์การค้าชุมชน บริษัทฯ มีรายได้จากธุรกิจการบริหารพื้นที่เช่า IT สำหรับปี 2568 เท่ากับ 508.1 ล้านบาท เพิ่มขึ้น 74 ล้าน Junction สำหรับปี 2568 เท่ากับ 117.4 ล้านบาท ลดลง บาท หรือเพิ่มขึ้นร้อยละ 17 จากปีก่อน 15.9 ล้านบาท หรือลดลงร้อยละ 11.9 จากปีก่อน รายได้จากธุรกิจพัฒนาศูนย์การค้าชุมชนคิดเป็นร้อยละ รายได้จากธุรกิจการบริหารพื้นที่เช่า IT Junction คิดเป็น 74 ของรายได้รวม ซึ่งเป็นรายได้หลักของบริษัท ร้อยละ 17.1 ของรายได้รวม

  `MDA_J_FY2025` · `p011` · SHA 006c3dc053ec
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 166m → FY2025 −THB 785m · −951m

- บริษัทพลิกเป็นขาดทุนมากจาก ขาดทุนจากการวัดมูลค่ายุติธรรม อสังหาริมทรัพย์เพื่อการลงทุน 550.5 ลบ. และด้อยค่าสินทรัพย์ 116.4 ลบ. ซึ่งเป็นรายการไม่ใช่เงินสด
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กลุ่มธุรกิจ ปี 2568 บริษัทฯ มีผลขาดทุนสุทธิจำนวน 785 ล้านบาท กำไรลดลงจำนวน 950.6 ล้านบาท หรือลดลงร้อยละ 574 จากปีก่อน มีสาเหตุหลักจากการรับรู้ผลขาดทุนจากการปรับมูลค่ายุติธรรมของอสังหาริมทรัพย์เพื่อการลงทุนจำนวน 550.5 ล้านบาท ตามมาตรฐานการรายงานทางการเงินที่กำหนดให้บริษัทฯ ซึ่งเลือกใช้รูปแบบการวัดมูลค่ายุติธรรม (Fair Value Model) ต้องประเมินมูลค่าสินทรัพย์ ณ วันสิ้นงวดและรับรู้ผลต่างในงบกำไรขาดทุนทันทีนอกจากนี้บริษัทฯ ยังมีการรับรู้ ผลขาดทุนจากการด้อยค่าของสินทรัพย์อีกจำนวน 116.4 ล้านบาท ส่งผลให้ภาพรวมผลการดำเนินงานในงวดดังกล่าวลดลง อย่างมีนัยสำคัญ อย่างไรก็ตาม รายการขาดทุนทั้งสองส่วนถือเป็นรายการทางบัญชีที่ไม่มีผลกระทบต่อกระแสเงินสด (Non- cash items) ของบริษัทฯ การปรับลดมูลค่ายุติธรรมในงวดนี

  `MDA_J_FY2025` · `p008` · SHA dfcc0e916ce3
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กลุ่มธุรกิจ ปี 2568 บริษัทฯ มีผลขาดทุนสุทธิจำนวน 785 ล้านบาท กำไรลดลงจำนวน 950.6 ล้านบาท หรือลดลงร้อยละ 574 จากปีก่อน มีสาเหตุหลักจากการรับรู้ผลขาดทุนจากการปรับมูลค่ายุติธรรมของอสังหาริมทรัพย์เพื่อการลงทุนจำนวน 550.5 ล้านบาท ตามมาตรฐานการรายงานทางการเงินที่กำหนดให้บริษัทฯ ซึ่งเลือกใช้รูปแบบการวัดมูลค่ายุติธรรม (มูลค่ายุติธรรม Model) ต้องประเมินมูลค่าสินทรัพย์ ณ วันสิ้นงวดและรับรู้ผลต่างในงบกำไรขาดทุนทันทีนอกจากนี้บริษัทฯ ยังมีการรับรู้ ผลขาดทุนจากการด้อยค่าของสินทรัพย์อีกจำนวน 116.4 ล้านบาท ส่งผลให้ภาพรวมผลการดำเนินงานในงวดดังกล่าวลดลง อย่างมีนัยสำคัญ อย่างไ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กลุ่มธุรกิจ ปี 2568 บริษัทฯ มีผลขาดทุนสุทธิจำนวน 785 ล้านบาท กำไรลดลงจำนวน 950.6 ล้านบาท หรือลดลงร้อยละ 574 จากปีก่อน มีสาเหตุหลักจากการรับรู้ผลขาดทุนจากการปรับมูลค่ายุติธรรมของอสังหาริมทรัพย์เพื่อการลงทุนจำนวน 550.5 ล้านบาท ตามมาตรฐานการรายงานทางการเงินที่กำหนดให้บริษัทฯ ซึ่งเลือกใช้รูปแบบการวัดมูลค่ายุติธรรม (Fair Value Model) ต้องประเมินมูลค่าสินทรัพย์ ณ วันสิ้นงวดและรับรู้ผลต่างในงบกำไรขาดทุนทันทีนอกจากนี้บริษัทฯ ยังมีการรับรู้ ผลขาดทุนจากการด้อยค่าของสินทรัพย์อีกจำนวน 116.4 ล้านบาท ส่งผลให้ภาพรวมผลการดำเนินงานในงวดดังกล่าวลดลง อย่างมีนัยสำคัญ อย่างไรก็ตาม รายการขาดทุนทั้งสองส่วนถือเป็นรายการทางบัญชีที่ไม่มีผลกระทบต่อกระแสเงินสด (Non- cash items) ของบริษัทฯ การปรับลดมูลค่ายุติธรรมในงวดนี

  `MDA_J_FY2025` · `p008` · SHA dfcc0e916ce3
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายได้จากการขายและบริการ ขาดทุนจากการปรับมูลค่ายุติธรรมของ สำหรับปี 2568 มีรายได้เท่ากับ 686.9 ล้านบาท อสังหาริมทรัพย์เพื่อการลงทุน เพิ่มขึ้นจากปีก่อนเท่ากับ 55.7 ล้านบาท หรือเพิ่มขึ้นร้อย บริษัทฯ มีผลขาดทุนจากการปรับมูลค่ายุติธรรม ละ 8.8 การเพิ่มขึ้นมีสาเหตุจากการเปิดคอมมูนิตี้มอลล์ ของอสังหาริมทรัพย์เพื่อการลงทุน สำหรับปี 2568 ใหม่ของบริษัทฯ ในช่วงครึ่งปีหลังของปี 2567 ที่บริษัทฯ เท่ากับ 550.5 ล้านบาท ลดลงจากปีก่อนเท่ากับ 791.8 ทำการเปิดศูนย์การค้า JAS Green Village ประเวศ ใน ล้านบาท หรือลดลงร้อยละ 328.1 สาเหตุหลักมาจากการ ไตรมาสที่ 2/2567 และ JAS Gree
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้จากการขายและบริการ ขาดทุนจากการปรับมูลค่ายุติธรรมของ สำหรับปี 2568 มีรายได้เท่ากับ 686.9 ล้านบาท อสังหาริมทรัพย์เพื่อการลงทุน เพิ่มขึ้นจากปีก่อนเท่ากับ 55.7 ล้านบาท หรือเพิ่มขึ้นร้อย บริษัทฯ มีผลขาดทุนจากการปรับมูลค่ายุติธรรม ละ 8.8 การเพิ่มขึ้นมีสาเหตุจากการเปิดคอมมูนิตี้มอลล์ ของอสังหาริมทรัพย์เพื่อการลงทุน สำหรับปี 2568 ใหม่ของบริษัทฯ ในช่วงครึ่งปีหลังของปี 2567 ที่บริษัทฯ เท่ากับ 550.5 ล้านบาท ลดลงจากปีก่อนเท่ากับ 791.8 ทำการเปิดศูนย์การค้า JAS Green Village ประเวศ ใน ล้านบาท หรือลดลงร้อยละ 328.1 สาเหตุหลักมาจากการ ไตรมาสที่ 2/2567 และ JAS Green Village รามคำแหง ลดลงของมูลค่ายุติธรรมของอสังหาริมทรัพย์เพื่อการ

  `MDA_J_FY2025` · `p018` · SHA 5334fdfe4911
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_J_FY2025`

##### GLAND — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท แกรนด์ คาแนล แลนด์ จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| — | — | — | n.m. | 28.0% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 6 · NPAT 6 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 1.6bn → FY2025 THB 1.6bn · −58m · -3.6%

- RFO ปี 2568 อยู่ที่ 1,552 ลบ. ลด 3.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company’s operating income was 1,551 million baht, representing an decrease of 58 million baht or 4% compared to the previous year. This growth was primarily driven by the rental and service business, the Company’s core business. The income increased as business conditions gradually recovered, particularly from retail space rentals across various projects, while office building rental rates remained at levels similar to the previous year as a result of a shift in tenant behavior, with some existing tenants reducing their office space. In the real estate business, income from sales showed a significant decrease compared to the previous year.

  `MDA_GLAND_FY2025` · `p013` · SHA 6cc2dc846b2a
  </details>
- RFO ปี 2568 อยู่ที่ 1,552 ลบ. ลด 3.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การแข่งขันและการส่งเสริมการขาย และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Retail area leases business: The retail leasing segment benefited from a resurgence in footfall, driven by an increase in the office working population and a recovery in overall visitor traffic across the projects. Furthermore, the Company consistently implemented marketing and promotional campaigns while focusing on curating high- quality tenants that align with the target customer profile. Consequently, these efforts resulted in improved tenant sales performance and a subsequent increase in demand for retail leasing space.

  `MDA_GLAND_FY2025` · `p008` · SHA ce3b607f3a9e
  </details>
- RFO ปี 2568 อยู่ที่ 1,552 ลบ. ลด 3.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Implementation of the mixed-use projects that await development in Grand Rama 9 and Phaholyothin Road areas. Development plans have progressed significantly compared to the previous year. Once operational, these projects are expected to be major drivers of the Company’s robust long-term growth. • Implementation of the development plan of residential projects in Don Mueang and Kamphaeng Phet areas to strengthen the revenue base from the real estate sales business. Currently, the Company is

  `MDA_GLAND_FY2025` · `p031` · SHA 34794a4c2218
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 421m → FY2025 THB 434m · +13m · +3.1%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 434 ลบ. เพิ่ม 3.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company had a net profit of 434 million baht, a 13 million baht or 3% increase from the previous year. When excluding the impact of financial reporting standards, such as gains or losses from fair value adjustments of investment properties in both the current and previous periods, the Company’s net profit increased 11% or 59 million baht.

  `MDA_GLAND_FY2025` · `p017` · SHA 46de2a99507d
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 434 ลบ. เพิ่ม 3.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Company had a gross profit of 1,196 million baht, with a gross profit margin of 77%, higher than the previous year. This was largely due to improved efficiency in overall office building management, particularly through reductions in energy and service costs.

  `MDA_GLAND_FY2025` · `p014` · SHA 03baabfbbbcc
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 434 ลบ. เพิ่ม 3.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ภาระหนี้และโครงสร้างเงินทุน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Company's financial cost was 195 million baht, an decrease of 15% or 36 million baht from 2024. The reduction was primarily due to an decrease in interest-bearing debt from and the interest rates on loans could decrease slightly.

  `MDA_GLAND_FY2025` · `p016` · SHA 705eb2fcc531
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 434 ลบ. เพิ่ม 3.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ความเสี่ยงด้านภูมิรัฐศาสตร์ และ ภาระหนี้และโครงสร้างเงินทุน และ รายได้และเงื่อนไขของธุรกิจไฟฟ้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Headline inflation for the year dropped into negative territory at -0.14%. This was primarily driven by energy prices—specifically electricity and fuel costs—declining in line with government subsidies and a continuous downward trend in global energy market prices. Consequently, the Monetary Policy Committee (MPC) resolved to cut the policy interest rate consistently throughout the year, totaling a cumulative reduction of 1.00% (across four adjustments). The rate decreased from 2.25% at the end of the previous year to 1.25% per annum by the end of 2025. These measures aimed to alleviate debt burdens for households and the business sector while managing deflationary risks (Source: Ministry of

  `MDA_GLAND_FY2025` · `p004` · SHA d9dfe4b3bda9
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company had a net profit of 434 million baht, a 13 million baht or 3% increase from the previous year. When excluding the impact of financial reporting standards, such as gains or losses from fair value adjustments of investment properties in both the current and previous periods, the Company’s net profit increased 11% or 59 million baht.

  `MDA_GLAND_FY2025` · `p017` · SHA 46de2a99507d
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_GLAND_FY2025`

#### ทะเบียนข้อสรุป — P3

| ส่วน | ประเภท | ข้อสรุป | รหัสแหล่งข้อมูล |
|---|---|---|---|
| headline | ข้ออนุมานนักวิเคราะห์ | รายได้ประจำส่งมอบความสอดคล้องของกำไรและราคาชัดที่สุด | FY_PANEL, P3_E1, P3_E2, P3_E3 |
| earnings_fact | ข้อเท็จจริงจากการคำนวณ | FY2025 RFO +0.6%; สถานะ NPAT ส่วนผู้ถือหุ้น: profit_increased | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | RFO เพิ่ม 0.6% และ NPAT ส่วนผู้ถือหุ้นเพิ่ม 13.7% ครบทั้ง 5 บริษัท | FY_PANEL |
| why | คำอธิบายฝ่ายจัดการ | traffic, occupancy และรายได้ค่าเช่าประจำของ CPN เป็นฐานของกลุ่ม | P3_E1, P3_E2, P3_E3 |
| why | ข้ออนุมานนักวิเคราะห์ | MBK เป็นตัวเทียบแบบ diversified และกำไรทั้งหมดไม่ใช่หลักฐานการดำเนินงานศูนย์การค้า | FY_PANEL, P3_E1, P3_E2, P3_E3 |
| causal_chain | ข้ออนุมานนักวิเคราะห์ | ห่วงโซ่เหตุ: Traffic → Occupancy → ค่าเช่า / NOI → Cash flow → Premium | P3_E1, P3_E2, P3_E3 |
| roles | ข้ออนุมานนักวิเคราะห์ | บทบาท: ผู้นำและตัวเพิ่มกำไร — CPN; ตัวเทียบแบบ diversified — MBK | FY_PANEL, P3_E1, P3_E2, P3_E3 |
| valuation | ข้ออนุมานนักวิเคราะห์ | P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 14.6x ครอบคลุม 3/5 บริษัท และ 99.6% ของ market cap ที่มีข้อมูล. กระแสเงินสดประจำและคุณภาพ CPN สนับสนุน premium | SET_PUBLIC_EOD, P3_E1, P3_E2, P3_E3 |
| trigger | ประเด็นที่ต้องพิสูจน์ | traffic และ occupancy ดีขึ้น | P3_E1, P3_E2, P3_E3 |
| trigger | ประเด็นที่ต้องพิสูจน์ | rental reversion ยังเป็นบวก | P3_E1, P3_E2, P3_E3 |
| trigger | ประเด็นที่ต้องพิสูจน์ | โครงการใหม่ ramp-up โดยไม่ลด margin | P3_E1, P3_E2, P3_E3 |
| risk | ประเด็นที่ต้องพิสูจน์ | การบริโภคชะลอ | P3_E1, P3_E2, P3_E3 |
| risk | ประเด็นที่ต้องพิสูจน์ | กลุ่มกระจุกตัวใน CPN สูง | P3_E1, P3_E2, P3_E3 |
| risk | ประเด็นที่ต้องพิสูจน์ | ความเสี่ยง capex และ ramp-up | P3_E1, P3_E2, P3_E3 |
| must_prove | ประเด็นที่ต้องพิสูจน์ | 6M26 ต้องรักษา NOI และ cash conversion ระหว่างขยายโครงการใหม่ | P3_E1, P3_E2, P3_E3 |

#### ทะเบียนหลักฐาน — P3

- **`FY_PANEL`** · _ข้อเท็จจริงจากการคำนวณ_ — Audited FY2024-25 company panel
  - RFO / NPAT-to-owners / independent panel membership; QA 43 pass / 0 fail
  - บทบาท: historical fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_company_fy2024_2025_audited_2026-08-07.csv`
  - SHA-256: `e5e04dbc40ffcc79fed58545a93dc4549c29cdaecf260bea73711bc6d0720481`
- **`SET_PUBLIC_EOD`** · _ข้อเท็จจริงจากการคำนวณ_ — SET public Company Highlights — EOD 2026-08-07
  - Adjusted YTD; unadjusted price, market cap and valuation; factsheet-surface cross-check
  - บทบาท: current market fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_set_public_surface_reconciliation_2026-08-07.csv`
  - SHA-256: `544c1f29fe2d409ee398822ac2bf32b769081718962ae2d1138985b0146b9530`
- **`SET_COMPANY_PROFILE`** · _ข้อเท็จจริง_ — SET company profiles — English and Thai
  - Official company names and business descriptions refreshed and validated for the 118-company perimeter from the public SET profile API
  - บทบาท: company business profile
  - URL: <https://www.set.or.th/th/market/product/stock/overview>
- **`COMPANY_REPORTS`** · _ข้ออนุมานนักวิเคราะห์_ — Company report synthesis corpus
  - Annual-only draft synthesis; reconciled to the ticker FY2025 MD&A where available
  - บทบาท: secondary synthesis; not management attribution
  - พาธ: `data/company-reports.json`
  - SHA-256: `c1a2bc40cbe21a2058aa596c362e4d47ad117360831b847de78ec414831fd2d2`
- **`MDA_CPN_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — CPN FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/CPN/MDA_CPN_2025FY_T.md`
  - SHA-256: `d435c77d5e916eef9754a2fc314f855f2d5d69925273ff32b9fccebff77275ad`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/0481NWS230220260802173500T.pdf>
- **`MDA_MBK_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — MBK FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/MBK/MDA_MBK_2025FY_T.md`
  - SHA-256: `8ebabd273748ab435249ecae1fd513b0d738713f542c2ae6d0305c80638eeb57`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/0480NWS260220262052034310T.pdf>
- **`MDA_PLAT_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — PLAT FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/PLAT/MDA_PLAT_2025FY_T.md`
  - SHA-256: `1c29cf2d2627b3b41bfac4f2fb5b5a5f21619377609c52f1b511fb14fb747e98`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/1252NWS250220261828176240T.pdf>
- **`MDA_J_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — J FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/J/MDA_J_2025FY_T.md`
  - SHA-256: `8652e454beb29a0291cd23d842661408f1bcdedabf8531bfe93b9eb741f523a0`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/1285NWS110220262203575470T.pdf>
- **`MDA_GLAND_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — GLAND FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/GLAND/MDA_GLAND_2025FY_E.md`
  - SHA-256: `b1bc48b9d2b5a863d50f38a4a8adaa766c959dca9e7a5e2e86b46d1b5b2b9ff5`
  - URL: <https://weblink.set.or.th/dat/news/202602/0538NWS130220260708223940E.pdf>
- **`P3_E1`** · _ฝ่ายจัดการ_ — CPN FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/CPN/MDA_CPN_2025FY_E.md`
  - SHA-256: `2c2101021bbe710bdf4d3a6764429313c35882cd94d37aa1857efbabe9854d60`
- **`P3_E2`** · _ฝ่ายจัดการ_ — GLAND FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/GLAND/MDA_GLAND_2025FY_E.md`
  - SHA-256: `b1bc48b9d2b5a863d50f38a4a8adaa766c959dca9e7a5e2e86b46d1b5b2b9ff5`
- **`P3_E3`** · _บทวิเคราะห์เครดิต_ — TRIS MBK credit analysis
  - Historical explanation or forward cross-check; see source role
  - บทบาท: forward/credit context
  - พาธ: `Listed Company/1-Raw/06-Market Reference/Credit Rating Research/2025/PROP/TRIS_MBK_180-2025.md`
  - SHA-256: `e1e5317030ac94ded96572cec5783781f407e35c3709446d9a3a1efe136e8900`
- **`P3_FACTSHEET`** · _ข้อเท็จจริงจากการคำนวณ_ — SET Factsheet — CPN
  - Live leader cross-check
  - บทบาท: presentation-surface check
  - URL: <https://www.set.or.th/th/market/product/stock/quote/cpn/factsheet>

### P1 · ที่อยู่อาศัยเพื่อขาย — ข้อจำกัดสินเชื่อกดดันผลประกอบการในวงกว้าง

`ยังถูกกดดัน` · 27.4% M-cap · THB 231bn · 37 บริษัท

| ตัวชี้วัด | RFO | NPAT | ราคา | P/E |
|---|---|---|---|---|
| ช่วง | FY2025 YoY | ส่วนผู้ถือหุ้น FY2025 YoY | ราคา YTD ปรับแล้ว | เฉพาะบริษัทที่มีกำไร |
| ค่า | -11.8% | -33.8% | +1.6% | 7.9x |
| จำนวน | THB 231bn FY2025 | THB 20.1bn FY2025 | ณ 7 ส.ค. 2569 | ค่าเฉลี่ยรวม |
| ครอบคลุม | 33/37 | 33/37 | 37/37 • 100% M-cap | 26/37 • 93% M-cap |

**ข้อเท็จจริงที่สังเกตได้** — FY2025: RFO -11.8% • NPAT -33.8% • ราคา YTD +1.6% • P/E 7.9x • ครอบคลุม RFO 33/37 • NPAT 33/37

#### เหตุผลที่เปลี่ยน

1. _ข้อเท็จจริงจากการคำนวณ_ · อุปสงค์ — RFO ที่สอบทานแล้วลด 11.8% และ NPAT ส่วนผู้ถือหุ้นลด 33.8% ใน 33/37 บริษัท
2. _คำอธิบายฝ่ายจัดการ_ · อนุมัติสินเชื่อ — ยอดโอน mix และ gross margin อ่อนตัว ขณะที่การปฏิเสธสินเชื่อยังสูง
3. _ข้อเท็จจริงจากการคำนวณ_ · โอน — ASW นำราคา YTD ปัจจุบัน แต่กำไร FY2025 ยังไม่ยืนยันการฟื้นในวงกว้าง

#### ห่วงโซ่เหตุและผล

**อุปสงค์** → **อนุมัติสินเชื่อ** → **โอน** → **Margin** (8.7% -2.9 ppt YoY) → **Cash**

#### บทบาทในกลุ่ม

| บทบาท | Ticker | ค่า | ที่มาของค่า |
|---|---|---|---|
| ผู้นำ | LH | 20% | สัดส่วน Market Cap ในกลุ่ม |
| ตัวฉุดผลประกอบการ | SPALI | -35.1% | NPAT YoY · Δ −2.2bn |
| ผู้นำราคา YTD | ASW | 3% | สัดส่วน Market Cap ในกลุ่ม |

#### มูลค่า

**แรงกดดันปัจจุบัน / ข้อเท็จจริง** — P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 7.9x ครอบคลุม 26/37 บริษัท และ 93.5% ของ market cap ที่มีข้อมูล. ส่วนลดสะท้อนกำลังซื้อ การโอน และ cash-conversion risk

| Trigger | Risk |
|---|---|
| อัตราปฏิเสธสินเชื่อลด | กำลังซื้ออ่อนยาว |
| การโอนและแปลง backlog ดีขึ้น | ส่วนลดกด margin |
| inventory และ leverage ลด | inventory และ cash cycle แย่ลง |

**6M26 ต้องพิสูจน์** — 6M26 ต้องเห็นการโอน margin และ operating cash flow ดีขึ้นพร้อมกัน

#### วิเคราะห์รายบริษัท — P1 ที่อยู่อาศัยเพื่อขาย

_ทุกบริษัทใน perimeter ของ Segment ที่สอบทาน_

| Ticker | บทบาท | M-cap | RFO YoY | NPAT YoY | ราคา YTD | P/E | Margin |
|---|---|---|---|---|---|---|---|
| LH | ผู้นำ | THB 45.2bn | -16.0% | -32.3% | 0.0% | 12.6x | 17.2% |
| SPALI | ตัวฉุดผลประกอบการ | THB 31.1bn | -22.7% | -35.1% | -6.5% | 7.5x | 16.6% |
| SIRI | บริษัทในกลุ่ม | THB 26.9bn | -13.1% | -14.1% | +14.2% | 5.9x | 13.7% |
| AP | บริษัทในกลุ่ม | THB 25.6bn | +1.0% | -14.0% | -5.2% | 5.9x | 11.6% |
| FPT | บริษัทในกลุ่ม | THB 16.2bn | — | — | +16.7% | 6.9x | — |
| QH | บริษัทในกลุ่ม | THB 15.3bn | -10.3% | -19.6% | +7.5% | 8.5x | 22.8% |
| PSH | บริษัทในกลุ่ม | THB 8.7bn | -29.1% | ขาดทุน | +11.2% | n.m. | -3.8% |
| SC | บริษัทในกลุ่ม | THB 8.6bn | -0.3% | -10.1% | +18.3% | 5.5x | 7.6% |
| SA | บริษัทในกลุ่ม | THB 8.5bn | -48.8% | -69.8% | -2.8% | 211.9x | 5.0% |
| ASW | ผู้นำราคา YTD | THB 7.2bn | -5.6% | -26.0% | +32.5% | 4.9x | 11.6% |
| ORI | บริษัทในกลุ่ม | THB 5.0bn | -24.4% | -31.6% | +12.8% | 7.0x | 8.9% |
| LALIN | บริษัทในกลุ่ม | THB 4.1bn | -17.3% | -21.4% | -8.7% | 9.2x | 15.2% |
| A | บริษัทในกลุ่ม | THB 2.7bn | — | — | -43.2% | n.m. | — |
| SENA | บริษัทในกลุ่ม | THB 2.6bn | +52.9% | -19.0% | +4.7% | 9.7x | 6.3% |
| NOBLE | บริษัทในกลุ่ม | THB 2.5bn | -37.0% | +37.4% | -14.4% | 4.6x | 8.6% |
| LPN | บริษัทในกลุ่ม | THB 2.4bn | -16.0% | -74.1% | +6.6% | 260.1x | 0.4% |
| A5 | บริษัทในกลุ่ม | THB 2.1bn | -27.4% | -77.3% | -5.4% | 33.9x | 7.9% |
| BRI | บริษัทในกลุ่ม | THB 2.0bn | -32.8% | -70.5% | -8.6% | 18.5x | 5.5% |
| PRIN | บริษัทในกลุ่ม | THB 1.7bn | -17.6% | -71.9% | -22.3% | 24.9x | 1.9% |
| NVD | บริษัทในกลุ่ม | THB 1.5bn | +11.8% | +80.7% | +5.1% | 8.8x | 9.7% |
| ANAN | บริษัทในกลุ่ม | THB 1.4bn | -3.0% | -83.3% | -17.1% | 5.9x | 1.0% |
| ORN | บริษัทในกลุ่ม | THB 1.3bn | +54.7% | +61.0% | +24.6% | 5.7x | 10.7% |
| ESTAR | บริษัทในกลุ่ม | THB 1.3bn | +7.4% | +270.6% | +25.0% | 7.3x | 6.3% |
| BROCK | บริษัทในกลุ่ม | THB 1.2bn | +86.4% | ขาดทุนลดลง | -9.4% | n.m. | -11.5% |
| PROUD | บริษัทในกลุ่ม | THB 1.1bn | +186.6% | +196.4% | +23.9% | 6.7x | 2.6% |
| PEACE | บริษัทในกลุ่ม | THB 726m | +6.0% | -74.5% | -25.4% | 36.4x | 1.9% |
| NCH | บริษัทในกลุ่ม | THB 573m | -12.0% | ขาดทุนเพิ่มขึ้น | +9.5% | n.m. | -11.6% |
| SAMCO | บริษัทในกลุ่ม | THB 571m | -2.0% | ขาดทุนลดลง | +23.6% | 4.6x | -1.3% |
| RML | บริษัทในกลุ่ม | THB 522m | -11.7% | ขาดทุนลดลง | -30.8% | n.m. | -704.6% |
| PF | บริษัทในกลุ่ม | THB 501m | — | — | -16.7% | n.m. | — |
| KUN | บริษัทในกลุ่ม | THB 492m | -22.5% | -87.9% | -27.7% | 633.5x | 0.7% |
| CMC | บริษัทในกลุ่ม | THB 485m | -39.2% | กลับเป็นกำไร | -10.2% | 7.0x | 1.6% |
| MJD | บริษัทในกลุ่ม | THB 293m | -16.0% | ขาดทุนเพิ่มขึ้น | 0.0% | n.m. | -106.3% |
| RICHY | บริษัทในกลุ่ม | THB 277m | -26.7% | ขาดทุนเพิ่มขึ้น | +13.3% | n.m. | -16.4% |
| PRECHA | บริษัทในกลุ่ม | THB 148m | +11.8% | ขาดทุนเพิ่มขึ้น | +4.8% | n.m. | -251.6% |
| KC | บริษัทในกลุ่ม | THB 104m | -69.9% | ขาดทุนเพิ่มขึ้น | -50.0% | n.m. | -952.8% |
| AKS | บริษัทในกลุ่ม | — | — | — | -50.0% | n.m. | — |

##### LH — ผู้นำ · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัทแลนด์แอนด์เฮ้าส์ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาโครงการที่พักอาศัยประเภทบ้านเดี่ยว ทาวน์เฮ้าส์ และอาคารชุดพักอาศัยที่มีคุณภาพ เพื่อจำหน่ายให้แก่กลุ่มลูกค้าเป้าหมายตามระดับความต้องการของลูกค้าในแต่ละระดับราคาที่แตกต่างกันไป โดยเน้นการพัฒนาโครงการในเขตกรุงเทพมหานครและปริมณฑล และโครงการตามจังหวัด ใหญ่ๆ ได้แก่ เชียงใหม่ เชียงราย นครราชสีมา ขอนแก่น มหาสารคาม อุดรธานี ประจวบคีรีขันธ์ อยุธยา และภูเก็ต

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 45.2bn | 3.78 | 0.0% | 12.6x | 17.2% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 25.7bn → FY2025 THB 21.6bn · −4.1bn · -16.0%

- รายได้ลด 15.9% จากยอดโอนที่อยู่อาศัยอ่อนตัว ข้อจำกัดสินเชื่อและอุปสงค์บ้านที่ซบเซามากกว่าการเติบโตของโรงแรม/รายได้ประจำ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Million baht % Million baht % Million baht % Sales income 13,131.2 61.9% 16,099.5 63.8% (2,968.3) -18.4% Rental and service income 8,089.5 38.1% 9,121.5 36.2% (1,032.0) -11.3% Total Revenues 21,220.7 100.0% 25,221.0 100.0% (4,000.3) -15.9% Selling expenses 1,216.2 5.7% 1,469.0 5.8% (252.8) -17.2% Administrative expenses 2,654.3 12.5% 2,833.4 11.2% (179.1) -6.3% Loss on exchange rate 411.5 1.9% 226.3 0.9% 185.2 81.8% Specific business tax 503.3 2.4% 622.7 2.5% (119.4) -19.2% Finance cost 2,093.9 9.9% 2,081.3 8.3% 12.6 0.6% Income tax 243.2 1.2% 638.2 2.5% (395.0) -61.9% Total Expenses 7,122.4 33.6% 7,870.9 31.2% (748.5) -9.5% The overall expenses decreased by 9.5% or Baht 748.5 million. Selli

  `MDA_LH_FY2025` · `p015` · SHA ffc389335921
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 5.5bn → FY2025 THB 3.7bn · −1.8bn · -32.3%

- กำไรส่วนผู้ถือหุ้นลด 32% จากกำไรขั้นต้นลดประมาณ 899 ลบ. และส่วนแบ่งกำไรบริษัทร่วมอ่อนลงตามฐานยอดโอนที่ต่ำลง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In the year end of 2025, the Company recorded the net profit (equity holders of the Company) Baht 3,716.2 million, representing a decrease of 32.3% or Baht 1,774.4 million, compared to the last year. Details are as follows; 1. Revenue from sales of 2025 was Baht 13,131.2 million, decreased by 18.4% or Baht 2,968.3 million, YoY. 2. Gross profit margin of 2025 was 23.7%, slightly decreased by 1.2% YoY. The overall from 1. and 2. make the decrease in gross profit by Baht 898.8 million YoY. 3. In 2025, the Company has gains on sales of assets of Baht 118.7 million (net of related expenses) from entering into an agreement with LH Shopping Centers Leasehold Real

  `MDA_LH_FY2025` · `p004` · SHA 3d51d30b34dc
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_LH_FY2025`

##### SPALI — ตัวฉุดผลประกอบการ · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ศุภาลัย จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์ประเภท 1) ที่อยู่อาศัย ทั้งบ้านและที่ดินจัดสรร อาคารชุด ในทำเลทั่วเขตกรุงเทพมหานคร ปริมณฑล รวมถึงต่างจังหวัด 2) เพื่อการพาณิชย์ ได้แก่ อาคารสำนักงานให้เช่า และ 3) ธุรกิจรีสอร์ทโรงแรมในต่างจังหวัด

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 31.1bn | 15.90 | -6.5% | 7.5x | 16.6% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 31.2bn → FY2025 THB 24.1bn · −7.1bn · -22.7%

- รายได้ลดประมาณ 23% จากยอดโอนลดบนฐาน FY2024 ที่สูง การปฏิเสธสินเชื่อและตลาดที่อยู่อาศัยชะลอทำให้ ยอดขายรอโอน แปลงเป็นรายได้ช้าลง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 1. Revenue from sales of real estate amounted to 23,713.62 million Baht, a decrease of 7,103.03 million Baht or 23% from the previous year. The revenue comprised 79% from the transfer of ownership of detached houses and townhouses, and the remaining 21% from the transfer of ownership of condominiums. The main reason for the decrease was lower revenue from condominium transfers. In 2025, the Company had 1 completed condominium project ready for ownership transfer, with transfers commencing in the late second quarter and continuing through the fourth quarter. In contrast, in 2024, the Company had 5 completed condominium projects ready for transfer. The higher proportion of low-rise property tr

  `MDA_SPALI_FY2025` · `p011` · SHA f1b76ae13ccf
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 6.2bn → FY2025 THB 4.0bn · −2.2bn · -35.1%

- กำไรลดประมาณ 35% เพราะยอดโอนที่ต่ำลงกด ผลของต้นทุนคงที่ต่อกำไร ขณะที่ต้นทุนที่ดิน/ก่อสร้างและ ส่วนผสมธุรกิจ กด อัตรากำไรขั้นต้น
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > due to the decline in total revenues which led to a higher expense ratio. 3. Share of profit from investments in joint ventures and associates amounted to 730.40 million Baht, increased by 336.68 million Baht or 86%. The increase was mainly due to higher revenue recognition from ownership transfers of projects operated by joint ventures and associates in Australia, particularly from new projects invested in 2024. 4. Finance cost amounted to 724.55 million Baht, increased by 16.05 million Baht from the previous year, representing a slight increase of only 2%. 5. Profit for the year amounted to 4,015.03 million Baht, decreased by 2,174.51 million Baht, representing a decrease of 35% from the p

  `MDA_SPALI_FY2025` · `p012` · SHA 52aef8eb20b4
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_SPALI_FY2025`

##### SIRI — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท แสนสิริ จำกัด (มหาชน)** — รายได้และกำไรเคลื่อนไหวสอดคล้องกัน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์เป็นหลัก โดยพัฒนาโครงการที่อยู่อาศัยประเภทบ้านเดี่ยว บ้านแฝด ทาวน์โฮม และคอนโดมิเนียม ในพื้นที่กรุงเทพมหานครและปริมณฑล ตลอดจนจังหวัดต่าง ๆ ที่สำคัญ นอกจากนี้ ยังมีธุรกิจบริการอสังหาริมทรัพย์ โดยให้บริการด้านการบริหารและจัดการโครงการอสังหาริมทรัพย์ บริหารงานขายโครงการ และบริการตัวแทนซื้อ-ขายอสังหาริมทรัพย์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 26.9bn | 1.53 | +14.2% | 5.9x | 13.7% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 14 · NPAT 6 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 37.8bn → FY2025 THB 32.9bn · −4.9bn · -13.1%

- RFO ปี 2568 อยู่ที่ 32,853 ลบ. ลด 13.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from low-rise projects, comprising single-detached houses, townhomes, and mixed products, totaling 18,529 million Baht, representing 63% of total revenue from project sales. Of this amount, revenue from single-detached house projects was 12,725 million Baht, a decrease of 30.1% or 5,487 million Baht YoY. The revenue from single-detached houses was mainly driven by Setthasiri Don Mueang, Narasiri Phahol-Watcharapol, Setthasiri Wongwaen-Chatuchot, Setthasiri Watcharapol-Theprak, BuGaan Krungthep Kreetha, as well as Saransiri Kohkaew Retreat which began to transfer during the last quarter of the year. Altogether, these 6 projects contributed 14% of total revenue from project sales.

  `MDA_SIRI_FY2025` · `p006` · SHA 2627ff812d31
  </details>
- RFO ปี 2568 อยู่ที่ 32,853 ลบ. ลด 13.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ค่าใช้จ่ายขายและบริหาร และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, Sansiri reported total revenue of 34,395 million Baht, down 12.3% or 4,810 million Baht YoY, primarily due to a 15.6% decline in revenue from project sales to 29,352 million Baht. The decrease was due to lower revenue from low-rise projects. Net profit attributable to equity holders of the Company was 4,513 million Baht, a 14.1% or 740 million Baht decrease YoY, driven by a contraction in gross profit margin and share of profit from joint ventures, partly offset by decreased selling and administrative expenses.

  `MDA_SIRI_FY2025` · `p003` · SHA 9888ba235d50
  </details>
- RFO ปี 2568 อยู่ที่ 32,853 ลบ. ลด 13.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, Sansiri reported revenue from project sales amounted to 29,352 million Baht, a decrease of 15.6% or 5,406 million Baht YoY. The decrease was largely from lower revenue from low-rise projects, while revenue from condominium increased.

  `MDA_SIRI_FY2025` · `p005` · SHA 76857369690f
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 5.3bn → FY2025 THB 4.5bn · −740m · -14.1%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 4,513 ลบ. ลด 14.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ค่าใช้จ่ายภาษี และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For 2025, Sansiri and its subsidiaries reported net profit (equity holders of the Company) of 4,513 million Baht, a decrease of 14.1% or 740 million Baht YoY. The decline was mainly attributable to lower gross profit and share of profit from joint ventures, partially offset by lower selling and administrative expenses. As a result, net profit margin in 2025 slightly declined to 13.1% from 13.4% in the previous year. The corporate income tax rate for 2025 was 20.6% of profit before corporate income tax.

  `MDA_SIRI_FY2025` · `p018` · SHA e43918ad9586
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 4,513 ลบ. ลด 14.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ค่าใช้จ่ายขายและบริหาร และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, Sansiri reported total revenue of 34,395 million Baht, down 12.3% or 4,810 million Baht YoY, primarily due to a 15.6% decline in revenue from project sales to 29,352 million Baht. The decrease was due to lower revenue from low-rise projects. Net profit attributable to equity holders of the Company was 4,513 million Baht, a 14.1% or 740 million Baht decrease YoY, driven by a contraction in gross profit margin and share of profit from joint ventures, partly offset by decreased selling and administrative expenses.

  `MDA_SIRI_FY2025` · `p003` · SHA 9888ba235d50
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 4,513 ลบ. ลด 14.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Costs in other businesses also declined, including the cost of construction material sales and cost of projects for rent, which decreased by 47.9% and 2.2%, respectively in 2025. However, hotel business costs increased by 64.8% YoY, in line with the increase in revenue from hotels, which resume normal operations in 2025. In addition, cost of business management services also increased by 5.1% from last year.

  `MDA_SIRI_FY2025` · `p015` · SHA d7f1f59b5275
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 4,513 ลบ. ลด 14.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน และ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, finance cost was 505 million Baht, an increase of 21.6% or 90 million Baht from 2024. The increase was due to the temporary closure of The Manner hotel in the United States for renovations during 2024. Consequently, the related interest expenses incurred during the renovation period were capitalised as project costs rather than being recorded as finance costs. Therefore, after resumed operation in 2025, the related interest expenses are now recorded as finance costs as usual.

  `MDA_SIRI_FY2025` · `p017` · SHA 54082bc8349c
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_SIRI_FY2025`

##### AP — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เอพี (ไทยแลนด์) จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 25.6bn | 8.15 | -5.2% | 5.9x | 11.6% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 3 · NPAT 4 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 37.0bn → FY2025 THB 37.3bn · +356m · +1.0%

- รายได้รวม FY2025 เพิ่ม 1.0% เป็น 37,345 ลบ. โดยรายได้ขายอสังหาฯ เพิ่ม 1.7% ขณะที่รายได้บริการลด 18.2%
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Q4 2025 Management Discussion and Analysis Share of profit from joint ventures (JV) was reported at THB 146 million (-53.7% QoQ and -57.3% YoY), driven by Station"whichbegan unittransfers inQ22025. InQ42025,total revenue showed solid performance,reachingTHB10,584million (+16.0%QoQand+13.7%YoY). Propertysalesaccountedforthemajority,withrevenueofTHB10,279million (+15.9%QoQand+14.0%YoY),whilethe total revenue of THB 37,345 million (+1.0% YoY), comprising THB 36,281 million (+1.7% YoY) from property sales and THB 1,064 million (-18.2% YoY) from services. LowRise: Thelow-rise segmentproved its resilience,withrevenueof THB 9,138million (+6.1% QoQand+4.0%YoY). This strongperformancewassupportedbybo

  `MDA_AP_FY2025` · `p017` · SHA b79335f9d571
  </details>
- รายได้แนวราบโต 6.5% เป็น 34,342 ลบ. แม้ตลาดที่อยู่อาศัยเผชิญภาวะท้าทาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In Y2025, the low-rise segment maintained strong momentum despite a challenging market, with revenue of THB 34,342million,representinga6.5%increasecomparedwithY2024.

  `MDA_AP_FY2025` · `p018` · SHA 4e0c0c1295f3
  </details>
- รายได้คอนโด JV ลด 14.7% เพราะผลกระทบหลังแผ่นดินไหวทำให้ แนวโน้ม การโอนอ่อนลง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > ForY2025,JV condominiumrevenuetotaled THB8,649million (-14.7%YoY),while shareofprofitfromJV investments amounted to THB 690 million (-29.0% YoY).The decline was primarily attributable to challenging market conditions following the earthquake at the end of Q1 2025, which adversely affected transfer momentum during the period.

  `MDA_AP_FY2025` · `p026` · SHA 4898957b4527
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 5.0bn → FY2025 THB 4.3bn · −703m · -14.0%

- กำไรส่วนผู้ถือหุ้นลด 14.0% เหลือ 4,316 ลบ. จาก 5,020 ลบ.
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Profit from Operation (THB million) 1,291 1,155 1,293 4,316 5,020 -0.1% 11.8% -14.0% 11.8% 1,291 5,020 1,155 1,293 -0.1% 4,316

  `MDA_AP_FY2025` · `p008` · SHA c7c367eec416
  </details>
- อัตรากำไรขั้นต้น รวมลดเป็น 31.9% จาก 34.3%
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross Margin 31.6% 32.0% 33.5% 31.9% 34.3% 17.1% 19.3% 19.3% 18.6%

  `MDA_AP_FY2025` · `p009` · SHA 5ac385d8862a
  </details>
- ฝ่ายจัดการระบุว่าแรงกดดัน อัตรากำไร ในไตรมาส 4 มาจากภาวะตลาดเป็นหลัก
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > InQ42o25,theCompanyreportedanoverallgrossmarginof31.6%ofrevenue,representinga19obpsYoYdecline and a 4o bps QoQ decline, mainly due to market conditions. The property margin stood at 30.0%, while the service margin was73.0%.

  `MDA_AP_FY2025` · `p021` · SHA 5d271c41fdbb
  </details>
- ส่วนแบ่งกำไร JV ลด 29.0% เพราะผลกระทบหลังแผ่นดินไหวทำให้ แนวโน้ม การโอนคอนโดอ่อนลง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > ForY2025,JV condominiumrevenuetotaled THB8,649million (-14.7%YoY),while shareofprofitfromJV investments amounted to THB 690 million (-29.0% YoY).The decline was primarily attributable to challenging market conditions following the earthquake at the end of Q1 2025, which adversely affected transfer momentum during the period.

  `MDA_AP_FY2025` · `p026` · SHA 4898957b4527
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_AP_FY2025`

##### FPT — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท เฟรเซอร์ส พร็อพเพอร์ตี้ (ประเทศไทย) จำกัด (มหาชน)** — ข้อมูลเทียบเคียงจำกัด: ไม่ควรสรุปเหตุเชื่อมโยงระหว่างรายได้กับกำไร

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาและบริหารจัดการกลุ่มอสังหาริมทรัพย์ ในรูปแบบครบวงจร ครอบคลุมอสังหาริมทรัพย์เพื่อการอุตสาหกรรม ที่อยู่อาศัย พาณิชยกรรม และฮอสพิทาลิตี้ รวมถึงลงทุนและได้รับแต่งตั้งเป็นผู้บริหารอสังหาริมทรัพย์ของกองทรัสต์ฯ (FTREIT และ GVREIT) และกองทุนรวมสิทธิการเช่าอสังหาริมทรัพย์ (GOLDPF)

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 16.2bn | 7.00 | +16.7% | 6.9x | — |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 14.3bn → FY2025 THB 13.8bn · −454m

- รายได้จากการประกอบธุรกิจลด 3% จากยอดขายที่อยู่อาศัยลด 5.8% ภายใต้อุปสงค์อ่อน หนี้ครัวเรือนสูง และสินเชื่อเข้มขึ้น ชดเชยบางส่วนด้วยค่าเช่า/บริการอุตสาหกรรมโต 5.4% จากความต้องการโรงงานและคลังสินค้า
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ส่วนได้เสียทุกกลุ่มในระยะยาวต่อไป สำหรับปี 2568 สิ้นสุดวันที่ 30 กันยายน 2568 บริษัทฯ รายงานรายได้จากการประกอบธุรกิจ จำนวน 13,118.5 ล้านบาท ลดลงร้อย ละ 3.0 หรือ 407.4 ล้านบาท เมื่อเทียบกับปีก่อน ในขณะที่รายงานรายได้รวม จำนวน 14,685.9 ล้านบาท เพิ่มขึ้นร้อยละ 0.4 หรือ 65.3 ล้านบาท ทั้งนี้ บริษัทฯ บันทึกกำไรสำหรับปี จำนวน 1,454.5 ล้านบาท ลดลงร้อยละ 0.9 หรือ 12.5 ล้านบาท และมีกำไรส่วนที่เป็นของผู้ ถือหุ้นบริษัทใหญ่ จำนวน 1,460.8 ล้านบาท เพิ่มขึ้นร้อยละ 1.6 หรือ 22.7 ล้านบาท โดยมีรายละเอียดดังต่อไปนี้ • รายได้จากการขายอสังหาริมทรัพย์ ปรับตัวลดลง 531.6 ล้านบาท หรือร้อยละ 5.8 มาอยู่ที่ 8,642.0 ล้านบาท จาก 9,173.6 ล้านบาทในปีก่อน ด้วยสภาวะตลาดที่ยังคงเผชิญแรงกดด้นจากสภาพเศรษฐกิจที่ชะลอตัว ภาระหนี้คร

  `MDA_FPT_FY2025` · `p003` · SHA f3ebdbc79419
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 1.9bn → FY2025 THB 1.4bn · −405m

- กำไรส่วนผู้ถือหุ้นยังเพิ่ม 1.6% เพราะกำไรขายอสังหาฯ เพื่อการลงทุน 1.33 พันลบ. และส่วนแบ่งกำไรบริษัทร่วม/JV ที่สูงขึ้น ชดเชย อัตรากำไร ที่อยู่อาศัยลด ด้อยค่า SG&A และดอกเบี้ยที่เพิ่ม
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > บันทึกดอกเบี้ยเข้าต้นทุนโครงการของโครงการในเวียดนามเนื่องจากการก่อสร้างโครงการแล้วเสร็จ จากรายได้และต้นทุนที่กล่าวมาข้างต้น ส่งผลให้บริษัทฯ มีกำไรสำหรับปี จำนวน 1,454.5 ล้านบาท ลดลง 12.5 ล้านบาท หรือ ร้อย ละ 0.9 ในขณะที่มีกำไรส่วนที่เป็นของผู้ถือหุ้นบริษัทใหญ่ จำนวน 1,460.8 ล้านบาท เพิ่มขึ้น 22.7 ล้านบาท หรือร้อยละ 1.6 กำไรต่อ หุ้นส่วนที่เป็นของผู้ถือหุ้นบริษัทใหญ่อยู่ที่ 0.63 บาทต่อหุ้นในปี 2568 เพิ่มขึ้นจาก 0.62 บาทต่อหุ้นในปีก่อน

  `MDA_FPT_FY2025` · `p014` · SHA a2e2c425dc2d
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- อัตรากำไรขั้นต้น ที่อยู่อาศัยลดเป็น 19.9% จาก 25.9% ส่วนหนึ่งจากเกณฑ์ตั้ง NRV ที่เข้มขึ้นสำหรับสินค้าสร้างเสร็จเกิน 1 ปี
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ย่านมิตรทาวน์ที่ปรับตัวดีขึ้นอย่างต่อเนื่อง • บริษัทฯ มีต้นทุนจากการประกอบธุรกิจเพิ่มขึ้นร้อยละ 2.1 หรือเพิ่มขึ้น 185.3 ล้านบาท มาอยู่ที่ 9,113.3 ล้านบาท โดยมีสาเหตุหลัก จากการตั้งค่าเผื่อการลดมูลค่าอสังหาริมทรัพย์เพื่อการอยู่อาศัย ซึ่งประเมินจากมูลค่าที่คาดว่าจะขายได้ในอนาคตที่ลดลงตามสภาวะ ตลาดที่ชะลอตัว ส่งผลให้อัตรากำไรขั้นต้นลดลงจากร้อยละ 34.0 ในปีก่อน มาอยู่ที่ร้อยละ 30.5 ในขณะเดียวกัน ต้นทุนในการจัด จำหน่ายและค่าใช้จ่ายในการบริหารของบริษัทฯ เพิ่มขึ้นร้อยละ 2.0 หรือ 59.4 ล้านบาท มาอยู่ที่ 3,040.2 ล้านบาท โดยมีสาเหตุหลัก มาจากการตั้งค่าเผื่อการด้อยค่าสินทรัพย์อสังหาริมทรัพย์เพื่อการอุตสาหกรรมตามมูลค่ายุติธรรมที่ลดลง ส่งผลให้บริษัทฯ มีต้นทุน และค่าใช้จ่ายรวมจำนวน 12,153.5 ล้านบาท เพิ่มขึ้

  `MDA_FPT_FY2025` · `p013` · SHA 74c6670c299d
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_FPT_FY2025`

##### QH — บริษัทในกลุ่ม · ติดตาม

**บริษัท ควอลิตี้เฮ้าส์ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์เพื่อขายและให้เช่า บ้านพร้อมที่ดิน หน่วยในอาคารชุดพักอาศัย อาคารที่พักอาศัยให้เช่า (ธุรกิจโรงแรม) อาคารสำนักงาน รวมทั้งรับจ้างบริหารอสังหาริมทรัพย์ให้เช่า และร่วมลงทุนในธุรกิจอื่นๆ

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 15.3bn | 1.43 | +7.5% | 8.5x | 22.8% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 6 · NPAT 6 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 8.4bn → FY2025 THB 7.6bn · −870m · -10.3%

- RFO ปี 2568 อยู่ที่ 7,569 ลบ. ลด 10.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In summary, the Company generated total revenues for the year 2025 and 2024 at Baht 7,882 million and Baht 8,695 million respectively, decreasing by Baht 813 million or 9% decrease compared to 2024. Details are as follows: 1. Revenue from sales of real estate for the year 2025 decreased by Baht 830 million or 12% decrease compared to 2024. This was due to an decrease in revenue from housing projects by Baht 1,548 million or 26% decrease. While revenue from condominium projects increased by Baht 718 million or 77% increase compared to 2024. In 2025, the Company launched 3 new housing projects with value of Baht 5,478 million and closed 4 sold-out housing and condominium projects. 2. Revenue f

  `MDA_QH_FY2025` · `p005` · SHA 7f0b7ed2c5f3
  </details>
- RFO ปี 2568 อยู่ที่ 7,569 ลบ. ลด 10.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In summary, the Company’s total costs for the year 2025 decreased by Baht 234 million or 4% decrease compared to 2024. This was due to cost from sales of real estate decreased by Baht 346 million or 7% decrease while cost of hotel operations increased by Baht 133 million or 16% increase, mainly due to an increase in rental costs. Meanwhile, cost from office rental operations decreased by Baht 21 million or 48% decrease, due to the land lease of Q.House Sathorn, which expired on December 31, 2025.

  `MDA_QH_FY2025` · `p006` · SHA 6855c2006528
  </details>
- RFO ปี 2568 อยู่ที่ 7,569 ลบ. ลด 10.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ต้นทุนทางการเงิน และ ค่าใช้จ่ายภาษี และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company’s net profit for the year 2025 decreased by Baht 422 million, or 20% decrease compared to 2024. This was mainly due to gross profit from sales of real estate decreased by Baht 485 million, gross profit from hotel operations decreased by Baht 102 million, gross profit from office rental operations decreased by Baht 50 million, share of profit from investments in associates increased by Baht 44 million and other income increased by Baht 56 million , administrative expenses decreased by Baht 4 million, interest income increased by Baht 8 million , finance cost decreased by Baht 42 million and income tax expenses decreased by Baht 61 million .

  `MDA_QH_FY2025` · `p012` · SHA ca32e1bf186c
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 2.2bn → FY2025 THB 1.7bn · −422m · -19.6%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,728 ลบ. ลด 19.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ต้นทุนทางการเงิน และ ค่าใช้จ่ายภาษี และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company’s net profit for the year 2025 decreased by Baht 422 million, or 20% decrease compared to 2024. This was mainly due to gross profit from sales of real estate decreased by Baht 485 million, gross profit from hotel operations decreased by Baht 102 million, gross profit from office rental operations decreased by Baht 50 million, share of profit from investments in associates increased by Baht 44 million and other income increased by Baht 56 million , administrative expenses decreased by Baht 4 million, interest income increased by Baht 8 million , finance cost decreased by Baht 42 million and income tax expenses decreased by Baht 61 million .

  `MDA_QH_FY2025` · `p012` · SHA ca32e1bf186c
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,728 ลบ. ลด 19.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In summary, the Company’s total costs for the year 2025 decreased by Baht 234 million or 4% decrease compared to 2024. This was due to cost from sales of real estate decreased by Baht 346 million or 7% decrease while cost of hotel operations increased by Baht 133 million or 16% increase, mainly due to an increase in rental costs. Meanwhile, cost from office rental operations decreased by Baht 21 million or 48% decrease, due to the land lease of Q.House Sathorn, which expired on December 31, 2025.

  `MDA_QH_FY2025` · `p006` · SHA 6855c2006528
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,728 ลบ. ลด 19.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > As of 31 December 2025, the Company’s total assets decreased by Baht 2,742 million or 6% decrease from the end of 2024 (as of 31 December 2024), mainly decrease from land and construction in progress and land and project development costs decreased by Baht 3,092 million and right-of-use assets decreased by Baht 222 million. Meanwhile, investments in associates increased by Baht 671 million. Total liabilities decreased by Baht 3,676 million or 24% decrease from the end of 2024 (as of 31 December 2024), due to during this period the Company issued unsecured debentures amount of Baht 2,000 million , repayment short term loan at amount of Baht 1,000 million , repayment of unsecured debentures am

  `MDA_QH_FY2025` · `p014` · SHA a6eda6310ca4
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,728 ลบ. ลด 19.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > III Share of profit from investments in associates In 2025, the Company’s share of profit from investments in associates was Baht 1,781 million, which increased by Baht 44 million or 3% increase compared to 2024. Details of the Company’s share of profit from 4 associate companies are as follows:

  `MDA_QH_FY2025` · `p007` · SHA c79fbd238fcb
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_QH_FY2025`

##### PSH — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท พฤกษา โฮลดิ้ง จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ถือหุ้นในบริษัทอื่น (Holding Company)

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 8.7bn | 3.98 | +11.2% | n.m. | -3.8% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 4

**RFO — เพราะอะไร** — FY2024 THB 19.9bn → FY2025 THB 14.1bn · −5.8bn · -29.1%

- รายได้ลดประมาณ 29% โดยรายได้อสังหาฯ ลดราว 34% จากยอดโอนและอุปสงค์ใหม่อ่อนตัวภายใต้การอนุมัติสินเชื่อที่เข้มงวด
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Cost of Sales and Services During Q4/2025 and the year 2025, the Company recorded cost of real estate sales of THB 2,866 million and THB 7,939 million, decreases of 14.0 percent and 36.6 percent YoY, respectively, due to lower revenue and the use of pricing strategies to align with industry conditions in Q4. However, the accelerated establishment of juristic entities and the handover of public utilities increased in Q2 and Q3, along with condominium transfers in Q4, improved cost of sales effectively, resulting in a higher full-year average gross profit margin than the previous year. For the healthcare business, cost of sales amounted to THB 477 million and THB 1,759 million, increases of 1.

  `MDA_PSH_FY2025` · `p017` · SHA dd00d55586e3
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 456m → FY2025 −THB 540m · −996m

- บริษัทพลิกเป็นขาดทุนเพราะปริมาณที่ลดแรงทำให้เกิด ผลลบจากต้นทุนคงที่เมื่อยอดขายลดลง และการดูดซับต้นทุนผ่านกำไรขั้นต้นอ่อนลง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Profit/(Loss) Excluding non-recurring special items totaling THB 787 million, the Company would report net profit attributable to the parent for Q4/2025 and the year 2025 of THB 52 million and THB 247 million, respectively. Throughout 2025, the Company accelerated project sales to manage cash flow, launched new projects by providing healthcare services from group businesses, expedited project closures, cost management, and controlled selling and administrative expenses and finance costs to align with intense price competition in the real estate market. However, these efforts were insufficient to offset the decline in real estate revenue. The Company also reported losses from associates and j

  `MDA_PSH_FY2025` · `p022` · SHA 3366be5e9966
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > As of January 1, 2025, the Company had cash on hand totaling THB 2,452 million. Cash inflows from operating activities amounted to THB 1,383 million, and cash inflows from investing activities of THB 1,351 million, primarily from proceeds from the disposal of all ordinary shares in a logistics-related company, the sale of investments, and the management of excess liquidity. Cash outflows from financing activities amounted to THB 2,755 million, mainly for debenture repayments, following the reduction of foreign-currency and non-core investments, and dividend payments. As a result, the Company had a remaining cash balance of THB 2,432 million as of December 31, 2025.

  `MDA_PSH_FY2025` · `p037` · SHA 1d49d01649cd
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ยอดขายส่งออกและตลาดต่างประเทศ และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Selling & Administrative Expenses During Q4/2025, the Company recorded non-recurring special items, including a loss on measurement fair value of long-term loans and accrued interest income of THB 758 million. This was recognized in relation to loans extended for overseas investments. In addition, the Company recorded a loss from impairment of investment in an associate of THB 29 million. The associate is engaged in a comprehensive elderly care business. To align with the Company’s investment policy based on the principle of prudence, and to reflect the actual operating performance of the invested companies, the total amount of THB 787 million represents the maximum loss that the Company is

  `MDA_PSH_FY2025` · `p018` · SHA 557a6f649a46
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_PSH_FY2025`

##### SC — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท เอสซี แอสเสท คอร์ปอเรชั่น จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 8.6bn | 2.00 | +18.3% | 5.5x | 7.6% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 4 · NPAT 4 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 20.3bn → FY2025 THB 20.2bn · −69m · -0.3%

- RFO ปี 2568 อยู่ที่ 20,233 ลบ. ลด 0.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  >  Total operating revenues for the year 2025 was Baht 20,233.21 million, decreased by 0.34% compared with the previous year, due to lower revenue from sales offset by an increase in revenue from rental and rendering services and revenue from consulting and management services.

  `MDA_SC_FY2025` · `p009` · SHA 0dbe82300cb3
  </details>
- RFO ปี 2568 อยู่ที่ 20,233 ลบ. ลด 0.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ความเสี่ยงด้านภูมิรัฐศาสตร์ และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  >  Revenue from rental and rendering services was Baht 1,126.19 million, increased by 5.39% from the previous year. This was due to a full-year revenue recognition from the warehouse business and an increase in after-sales services income.

  `MDA_SC_FY2025` · `p010` · SHA e9de23dd6090
  </details>
- RFO ปี 2568 อยู่ที่ 20,233 ลบ. ลด 0.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  >  Revenue from consulting and management services was Baht 731.34 million, increased by Baht 452.71 million or 162.48%, which was in line with the higher number of services rendered to juristic person management and joint ventures’ projects.

  `MDA_SC_FY2025` · `p011` · SHA 0d7ede3358de
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 1.7bn → FY2025 THB 1.5bn · −173m · -10.1%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,533 ลบ. ลด 10.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  >  Profits attributable to owners of parent for the year 2025 amounting to Baht 1,532.70 million, decreased by 10.13%, compared with the previous year. It was mainly due to a decrease in the gain on fair value adjustment of investment properties and share of loss from joint ventures, which are still in their initial phase of operation, particularly some condominium projects that are currently under construction.

  `MDA_SC_FY2025` · `p017` · SHA 45f28b608109
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,533 ลบ. ลด 10.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Total assets as of December 31, 2025, were Baht 63,955.19 million, decreased by Baht 3,302.85 million from December 31, 2024. The decrease was mainly attributable to real estate development costs.

  `MDA_SC_FY2025` · `p018` · SHA c76c3e01e0a2
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,533 ลบ. ลด 10.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross profit margin was 29.42%, increased from 27.99% in 2024.

  `MDA_SC_FY2025` · `p015` · SHA 82e50b52ab78
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,533 ลบ. ลด 10.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  >  Gross profit for the year 2025 increased by 1.80% from consulting and management services.

  `MDA_SC_FY2025` · `p014` · SHA 6d294e4bb163
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  >  Profits attributable to owners of parent for the year 2025 amounting to Baht 1,532.70 million, decreased by 10.13%, compared with the previous year. It was mainly due to a decrease in the gain on fair value adjustment of investment properties and share of loss from joint ventures, which are still in their initial phase of operation, particularly some condominium projects that are currently under construction.

  `MDA_SC_FY2025` · `p017` · SHA 45f28b608109
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_SC_FY2025`

##### SA — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ไซมิส แอสเสท จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์เพื่อที่อยู่อาศัยเพื่อจำหน่าย ทั้งประเภทโครงการคอนโดมิเนียม บ้านจัดสรร ทาวน์โฮม และโฮมออฟฟิศ และให้บริการบริหารงานนิติบุคคลให้กับโครงการต่างๆ ของบริษัท

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 8.5bn | 7.05 | -2.8% | 211.9x | 5.0% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 19 · NPAT 11 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 2

**RFO — เพราะอะไร** — FY2024 THB 4.6bn → FY2025 THB 2.3bn · −2.2bn · -48.8%

- RFO ปี 2568 อยู่ที่ 2,340 ลบ. ลด 48.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้ และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Company recognized revenue from real estate sales from 5 key projects—Landmark At MRTA Station, Monsane Ratchapruek–Chaengwattana, Siamese Holm Phahol–Vibhavadi, Siamese Blossom Phahol–Vibhavadi, and Siamese Exclusive Queens—totaling THB 1,345.48 million, and THB 160.03 million from other projects. In addition, the Company recorded merchandise sales of THB 52.61 million, bringing total revenue from real estate and merchandise sales to THB 1,558.12 million, or 57.32% of total revenue. This represented a decrease of THB 2,546.89 million, or 62.04%, from the same period of the previous year, primarily due to the reduction of inventory following the gradual transfer of condominium u

  `MDA_SA_FY2025` · `p025` · SHA b0b4fdbadd38
  </details>
- RFO ปี 2568 อยู่ที่ 2,340 ลบ. ลด 48.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the year 2025, the Company reported total revenue of THB 2,718.26 million, representing a decrease from the same period of the previous year by THB 2,021.80 million, or 42.65%. The revenue comprised THB 1,558.12 million from real estate and merchandise sales, THB 609.69 million from hotel operations, THB 110.96 million from rental operations, THB 60.88 million from service income, and THB 378.61 million from other income.

  `MDA_SA_FY2025` · `p022` · SHA cacfb4b1c697
  </details>
- RFO ปี 2568 อยู่ที่ 2,340 ลบ. ลด 48.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การแข่งขันและการส่งเสริมการขาย และ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, Thailand’s hotel and accommodation sector faced pressure from several negative factors, resulting in a decline in the industry’s total revenue and marking the first contraction in five years. The key drivers were the decrease in international tourist arrivals and the nationwide occupancy rate, amid intense price competition and a persistently high level of accumulated room supply in the market. Although domestic tourism continued to show growth, most trips were non-overnight stays. Meanwhile, revenue from meetings and seminar activities remained weak, particularly in the first half of the year when the number of events declined. Nevertheless, government measures, such as the “We Tra

  `MDA_SA_FY2025` · `p010` · SHA 69e04c452618
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 386m → FY2025 THB 116m · −270m · -69.8%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 116 ลบ. ลด 69.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > As a result, the Company recorded total net profit of THB 137.95 million, decreasing by THB 273.24 million from the same period of the previous year. Of this amount, profit attributable to owners of the parent was THB 116.49 million, while profit attributable to non-controlling interests was THB 21.46 million, representing 4.29% and 0.79% of total revenue, respectively.

  `MDA_SA_FY2025` · `p023` · SHA 800f6f5f6a68
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 116 ลบ. ลด 69.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้ และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Company recognized revenue from real estate sales from 5 key projects—Landmark At MRTA Station, Monsane Ratchapruek–Chaengwattana, Siamese Holm Phahol–Vibhavadi, Siamese Blossom Phahol–Vibhavadi, and Siamese Exclusive Queens—totaling THB 1,345.48 million, and THB 160.03 million from other projects. In addition, the Company recorded merchandise sales of THB 52.61 million, bringing total revenue from real estate and merchandise sales to THB 1,558.12 million, or 57.32% of total revenue. This represented a decrease of THB 2,546.89 million, or 62.04%, from the same period of the previous year, primarily due to the reduction of inventory following the gradual transfer of condominium u

  `MDA_SA_FY2025` · `p025` · SHA b0b4fdbadd38
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 116 ลบ. ลด 69.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Company reported net profit of THB 137.95 million, decreasing by THB 273.24 million, or 66.45%, from the same period of the previous year. The net profit margin for 2025 was 5.08% of total revenue. Of the total net profit, profit attributable

  `MDA_SA_FY2025` · `p044` · SHA f66958a54b73
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 116 ลบ. ลด 69.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ราคาขายและส่วนผสมผลิตภัณฑ์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Based on the above table, the analysis is as follows: The gross profit margin from real estate and merchandise sales in 2025 was 34.28%, decreasing from 40.32% in the same period of the previous year. This decline was mainly due to the adjustment of the pricing strategy to align with competitive market conditions and the overall economic environment.

  `MDA_SA_FY2025` · `p038` · SHA 97d49b96b314
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Company reported other income of THB 378.61 million, representing 13.93% of total revenue. This increased by THB 311.25 million, or 462.11%, from the same period of the previous year. The increase was primarily attributable to gains from the fair value adjustment of investment properties.

  `MDA_SA_FY2025` · `p034` · SHA a094c30c3f01
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In addition, the Company recorded an impairment loss in accordance with TFRS 9 amounting to THB 4.97 million in 2025.

  `MDA_SA_FY2025` · `p041` · SHA 61acec0b9510
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_SA_FY2025`

##### ASW — ผู้นำราคา YTD · ติดตาม

**บริษัท แอสเซทไวส์ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัทประกอบธุรกิจโดยการถือหุ้นในบริษัทอื่น (Holding Company) โดยมีบริษัทย่อยที่ประกอบธุรกิจหลักเกี่ยวกับธุรกิจพัฒนาอสังหาริมทรัพย์เพื่อขายทั้งประเภท โครงการคอนโดมิเนียม บ้านจัดสรร ทาวน์โฮม และโฮมออฟฟิศ

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 7.2bn | 7.95 | +32.5% | 4.9x | 11.6% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 9 · NPAT 12 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 9.9bn → FY2025 THB 9.3bn · −554m · -5.6%

- RFO ปี 2568 อยู่ที่ 9,306 ลบ. ลด 5.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Group recorded revenues from sales of real estate and rental and services income of THB 9,226.35 million which decreased by THB 565.23 million or decreased 5.77% from THB 9,791.58 million in 2024. The real estate development for sales business of THB 8,628.83 million, which was recognized when the Group had completely transferred the ownership to their customers or revenue recognition criteria was me, and the rental and services income of THB 597.52 million contributed most of the revenue.

  `MDA_ASW_FY2025` · `p004` · SHA f23f42d939df
  </details>
- RFO ปี 2568 อยู่ที่ 9,306 ลบ. ลด 5.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Group recorded distribution cost of THB 1,269.85 million, increased THB 8.00 million or increased 0.63% from THB 1,261.86 million in 2024. Although in 2025, sales of real estate decreased, the distribution cost increased because of selling expense related agents’ commission increased of THB 192.88 million, which mostly were from transfer of the TITLE Group.

  `MDA_ASW_FY2025` · `p029` · SHA 8bb8a251cc52
  </details>
- RFO ปี 2568 อยู่ที่ 9,306 ลบ. ลด 5.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Financial performance for the year ended 31 December 2025, the Group recorded sales and service revenue of THB 9,226.35 million which main source of revenue came from sales of real estate. The Group had gross profit of THB 3,794.17 million, or equivalent to 40.08%. While distribution costs and administrative expenses were THB 1,269.85 million and THB 899.56 million, respectively. The Group recorded net profit of THB 1,077.66 million, or equivalent to 11.38%.

  `MDA_ASW_FY2025` · `p002` · SHA 71bdd8786a7a
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 1.5bn → FY2025 THB 1.1bn · −379m · -26.0%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,078 ลบ. ลด 26.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ อัตรากำไรลดลง และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนทางการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Group recorded net profit of THB 1,077.66 million which decreased by THB 379.14 million or decreased 26.03% from THB 1,456.72 million in 2024, equivalent to the net profit margin of 11.38% and 14.59% of the year 2025 and 2024 respectively. The net profit margin decreased because of a significant increase in finance costs as mentioned above and profit was attributed to non-controlling interests of the TITLE. However, the Group was able to maintain their profit continually for the year 2025, gross profit margin of the year 2025 was 40.08% ; higher than 39.39%.of the year 2024. The Group keep selective sourcing potential development sites and effective cost control management, espe

  `MDA_ASW_FY2025` · `p034` · SHA b184a2b30628
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,078 ลบ. ลด 26.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ราคาขายและส่วนผสมผลิตภัณฑ์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Group had gross profit of THB 3,794.17 million which decreased by THB 139.76 million or decreased 3.55% from THB 3,933.93 million in 2024. In 2025, the Gross profit margin 40.08%, was slightly higher than the gross profit margin of THB 39.39% in the previous year. The gross profit margin was in line with the sales of real estate, which was the main income of the Group. However, the Group was able to maintain gross profit margin over the industry because of their emphasis on the sales pricing policy and monitor cost control activities especially for land selection and project development cost control process.

  `MDA_ASW_FY2025` · `p028` · SHA afacc051cb85
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,078 ลบ. ลด 26.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Group recorded their cost of real estate units sold at THB 5,068.88 million which decreased by THB 480.30 million or decreased 8.66% from THB 5,549.18 million in 2024. The amount decreased in line with a decrease in sales of real estate. The cost of real estate comprised cost of land and land improvement, construction costs, interest cost and other development expenses; for example, project and landscape design cost, construction consultant fees, and related license fees issued by the government authorities etc.

  `MDA_ASW_FY2025` · `p026` · SHA 0e6c48ba35be
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,078 ลบ. ลด 26.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน และ การซื้อกิจการและการรวมงบการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Group recorded finance cost of THB 317.42 million, increased THB 254.34 million or increased 403.19% from THB 63.08 million in 2024. The main reasons were there are many projects were completed in 2025 that interest could not be capitalised in the cost of project and an finance cost increased because of an increase in acquisition of land plots to support future projects which cost of acquired land plots were recorded as deposits for purchase of land and land held for development.

  `MDA_ASW_FY2025` · `p033` · SHA 1bc7f36f2edf
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gains on disposal of investment In 2025, the Group recorded gains on disposals of investments of THB 79.56 million, increased THB 10.86 million or increased 15.81% from THB 68.70 million in 2024. The gain on disposals of investments increased because the Group disposed investment in a subsidiary which develops condominium project to business partner, which the project’s size of a disposed subsidiary is bigger than a disposed subsidiary in the last year. In 2025, the Group disposed Wise Estate 22 Co., Ltd., (“WE22”), which develop Kavalon project, while Wise Estate 13 Co., Ltd., (“WE13”), which develop Modiz Vault Kaset - Sripatum project, was disposed in 2024.

  `MDA_ASW_FY2025` · `p025` · SHA 91884171f03d
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_ASW_FY2025`

##### ORI — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ออริจิ้น พร็อพเพอร์ตี้ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์ประเภทคอนโดมิเนียมตามแนวสถานีขนส่งมวลชนระบบรางในเขตกรุงเทพมหานครและปริมณฑล และธุรกิจให้บริการที่เกี่ยวเนื่องกับธุรกิจอสังหาริมทรัพย์ ได้แก่ บริการจัดหาผู้เช่าห้องชุด และบริการรับจ้างบริหารโครงการนิติบุคคลอาคารชุดแก่โครงการที่บริษัทเป็นผู้พัฒนาเท่านั้น

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 5.0bn | 2.02 | +12.8% | 7.0x | 8.9% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 20 · NPAT 20 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 7

**RFO — เพราะอะไร** — FY2024 THB 10.6bn → FY2025 THB 8.1bn · −2.6bn · -24.4%

- RFO ปี 2568 อยู่ที่ 8,052 ลบ. ลด 24.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Group has total revenues for for the year ended December 31st, 2024 and for the year ended December 31st, 2025 amount of 11,985.3 million baht and 9,223.4 million baht respectively, a decrease of 2,761.9 million baht, or 23.0 % compared with the same period of the previous year. The decline was primarily driven by lower revenues from real estate sales, project management service fees and Gain on disposals of investments in subsidiary. However, this decrease was partially offset by an increase in gain on disposal of investments in joint ventures, hotel operating income and rental income, and other income.

  `MDA_ORI_FY2025` · `p039` · SHA 6ebb070f3160
  </details>
- RFO ปี 2568 อยู่ที่ 8,052 ลบ. ลด 24.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ ยอดขายและการโอนโครงการที่อยู่อาศัย และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Shareholders’ Equity as of December 31st, 2025. The Group has an increase of Shareholders’ Equity amount of 698.1 million baht, or 3.3%, compared to the year 2024 (as of December 31st, 2024). The Group has retained earnings from operating for the year ended December 31st, 2025 was 719.9 million baht from projects that transferred of condominiums, housing estates, service income, revenues from hotel operations and rental, and revenues from project management according to the plan. Including the share of profit from joint ventures, etc.

  `MDA_ORI_FY2025` · `p085` · SHA 52334c2e0ad6
  </details>
- RFO ปี 2568 อยู่ที่ 8,052 ลบ. ลด 24.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, The Group successfully achieved total Presales of 24,942.0 million baht from both landed property and condominium projects. This includes 20,327.0 million baht from the condominium segment, operated under Origin Vertical Corporation Co., Ltd. (“ORIGIN VERTICAL”), representing 81.0% of total sales. The landed property segment, operated under Britania PCL (“BRI”), contributed 4,615.0 million baht, representing approximately 19.0%. Classified by investment structure, sales from The Group’s own developments amounted to 14,923.0 million baht, while Joint Venture (JV) projects contributed 10,018.0 million baht. In terms of project status, the "Ready-to-Move" segment was highly successful

  `MDA_ORI_FY2025` · `p007` · SHA 6e50e4bb7318
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 1.1bn → FY2025 THB 720m · −332m · -31.6%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 720 ลบ. ลด 31.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 7. Impairment loss on investment in subsidiaries, for the year ended December 31st, 2025, The Group recorded an impairment loss reversal of 2.6 million baht, representing 0.1% of total revenues. This is an increase of 2.6 million baht, or 100.0%, compared to the same period of the previous year. This increase was primarily driven by the recognition of loss from the estimated impairment of investment in subsidiaries.

  `MDA_ORI_FY2025` · `p062` · SHA 25b1c985c270
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 720 ลบ. ลด 31.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 5. Administrative expenses, for the year ended December 31st, 2025, amount of 1,017.6 million baht, or 11.0% of total revenues, a decrease of 118.9 million baht, or 10.5%. This decrease was principally due to the provision for losses on guaranteed lease contracts (IP Program) associated with recently completed projects and impairment losses on other assets. Such provision is expected to be reversed if The Group secures additional tenants as planned or if these costs can be recognized as part of future project costs. However, some administrative expenses are related to project management services, including project feasibility study planning and management services fees after the signed of a

  `MDA_ORI_FY2025` · `p060` · SHA 811f83fb938f
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 720 ลบ. ลด 31.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ การซื้อกิจการและการรวมงบการเงิน และ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Property, plant and equipment, a decreased from 2024 (as of December 31st, 2024) amounting to 159.2 million baht, or 4.2%, Due to the reclassification of land from the hotel and rental business group to the cost of real estate development projects for sale by the condominium business group, as well as the reclassification of projects from the same business group to assets held for sale. And an increase from the acquisition of joint venture to subsidiary.

  `MDA_ORI_FY2025` · `p075` · SHA 4ddbf65f4143
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 720 ลบ. ลด 31.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ ยอดขายและการโอนโครงการที่อยู่อาศัย และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Shareholders’ Equity as of December 31st, 2025. The Group has an increase of Shareholders’ Equity amount of 698.1 million baht, or 3.3%, compared to the year 2024 (as of December 31st, 2024). The Group has retained earnings from operating for the year ended December 31st, 2025 was 719.9 million baht from projects that transferred of condominiums, housing estates, service income, revenues from hotel operations and rental, and revenues from project management according to the plan. Including the share of profit from joint ventures, etc.

  `MDA_ORI_FY2025` · `p085` · SHA 52334c2e0ad6
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 7. Impairment loss on investment in subsidiaries, for the year ended December 31st, 2025, The Group recorded an impairment loss reversal of 2.6 million baht, representing 0.1% of total revenues. This is an increase of 2.6 million baht, or 100.0%, compared to the same period of the previous year. This increase was primarily driven by the recognition of loss from the estimated impairment of investment in subsidiaries.

  `MDA_ORI_FY2025` · `p062` · SHA 25b1c985c270
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Group has total revenues for for the year ended December 31st, 2024 and for the year ended December 31st, 2025 amount of 11,985.3 million baht and 9,223.4 million baht respectively, a decrease of 2,761.9 million baht, or 23.0 % compared with the same period of the previous year. The decline was primarily driven by lower revenues from real estate sales, project management service fees and Gain on disposals of investments in subsidiary. However, this decrease was partially offset by an increase in gain on disposal of investments in joint ventures, hotel operating income and rental income, and other income.

  `MDA_ORI_FY2025` · `p039` · SHA 6ebb070f3160
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_ORI_FY2025`

##### LALIN — บริษัทในกลุ่ม · ติดตาม

**บริษัท ลลิล พร็อพเพอร์ตี้ จำกัด (มหาชน)** — รายได้และกำไรเคลื่อนไหวสอดคล้องกัน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ประกอบธุรกิจพัฒนาอสังหาริมทรัพย์เพื่อขาย

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 4.1bn | 4.40 | -8.7% | 9.2x | 15.2% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 2 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 3.7bn → FY2025 THB 3.0bn · −634m · -17.3%

- RFO ปี 2568 อยู่ที่ 3,038 ลบ. ลด 17.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the company’s selling and administrative expenses were 485.4 million baht decreased from 554.2 million baht showed in the corresponding period last year, or 12.41% decreased. The revenue from sales; however, decreased by 17.3% result to SG&A/Sales increase from 15.09% in 2024 to 15.98% in 2025.

  `MDA_LALIN_FY2025` · `p003` · SHA c74263a319b9
  </details>
- RFO ปี 2568 อยู่ที่ 3,038 ลบ. ลด 17.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the company’s revenue from sale was 3,037.7 million baht decreased from 3,671.9 million baht showed in the last year, or 17.3% decreased which was consistent with overall market conditions that slowed down.

  `MDA_LALIN_FY2025` · `p002` · SHA 41696377dd93
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 588m → FY2025 THB 462m · −126m · -21.4%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 462 ลบ. ลด 21.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In year 2025, Lalin Property Public Co., Ltd., showed a profit at 462.3 million baht decreased from 588 million baht showed in 2024, or decreased by 21.4%. The company would like to clarify reasons why 2025’s profit showed changing over 20% as follows.

  `MDA_LALIN_FY2025` · `p001` · SHA edcb2d4339d2
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_LALIN_FY2025`

##### A — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท อารียา พรอพเพอร์ตี้ จำกัด (มหาชน)** — ข้อมูลเทียบเคียงจำกัด: ไม่ควรสรุปเหตุเชื่อมโยงระหว่างรายได้กับกำไร

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ธุรกิจอสังหาริมทรัพย์ แบ่งเป็น 3 ประเภท 1) โครงการบ้านเดี่ยว โดยจะขายที่ดินเปล่าซึ่งเป็นกรรมสิทธิ์ของบริษัท และรับจ้างปลูกสร้างบ้านบนที่ดินนั้น หรือขายที่ดินพร้อมบ้านสร้างเสร็จ 2) โครงการทาวน์เฮาส์ และ 3) โครงการคอนโดมิเนียม โดยเน้นทำเลใจกลางเมืองบริษัทมีการพัฒนาโครงการประเภทธุรกิจศูนย์การค้าหรือคอมมิวนิตี้มอลล์ ในชื่อว่า Pickadaily Bangkok

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 2.7bn | 2.76 | -43.2% | n.m. | — |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 5 · NPAT 6 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 1.4bn → FY2025 — · —

- RFO ปี 2568 อยู่ที่ ไม่ปรากฏตัวเลขที่เปรียบเทียบได้ ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนที่ดินนิคมอุตสาหกรรม และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Company’s revenue from condominium sales decreased by Baht 79.5 million compared to the same period of the previous year. Revenue from land sales also declined by THB 163.7 million compared to 2024. In addition, revenue from townhouse and single-detached house sales decreased by THB 396.4 million from the prior year.

  `MDA_A_FY2025` · `p005` · SHA 2a48ed5fff54
  </details>
- RFO ปี 2568 อยู่ที่ ไม่ปรากฏตัวเลขที่เปรียบเทียบได้ ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายภาษี
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, Distribution cost decreased by Baht 39.1 million compared to the previous year. This was mainly attributable to two factors. First, transfer fees and specific business tax expenses decreased in line with the decline in revenue from real estate sales. Second, the reduction was due to tighter control over marketing expenses.

  `MDA_A_FY2025` · `p012` · SHA c120655a26f9
  </details>
- RFO ปี 2568 อยู่ที่ ไม่ปรากฏตัวเลขที่เปรียบเทียบได้ ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > As a result, total revenue from real estate sales for 2025 amounted to Baht 636.5 million,

  `MDA_A_FY2025` · `p006` · SHA 3be3ddfcdbcd
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 426m → FY2025 — · —

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ ไม่ปรากฏตัวเลขที่เปรียบเทียบได้ ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายภาษี
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, Distribution cost decreased by Baht 39.1 million compared to the previous year. This was mainly attributable to two factors. First, transfer fees and specific business tax expenses decreased in line with the decline in revenue from real estate sales. Second, the reduction was due to tighter control over marketing expenses.

  `MDA_A_FY2025` · `p012` · SHA c120655a26f9
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ ไม่ปรากฏตัวเลขที่เปรียบเทียบได้ ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Cost of sale of real estate Cost of real estate sales decreased in line with the decline in revenue, and the gross profit margin

  `MDA_A_FY2025` · `p009` · SHA 483c5d4231d9
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ ไม่ปรากฏตัวเลขที่เปรียบเทียบได้ ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายภาษี
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Income tax expense in 2025 primarily resulted from the reversal of deferred tax assets relating to tax losses that are not expected to be utilized. In contrast, for the same period in 2024, it mainly arose from the recognition of deferred tax assets.

  `MDA_A_FY2025` · `p014` · SHA 73fb4c4df5e4
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ ไม่ปรากฏตัวเลขที่เปรียบเทียบได้ ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue and Cost of construction services In 2025, the Group’s revenue and cost of construction services decreased compared to 2024. This was primarily because, in 2025, the Company undertook construction projects consisting mainly of single-detached houses and other smaller-scale construction works, which were of lower value compared to 2024, when the projects primarily involved condominium developments..

  `MDA_A_FY2025` · `p010` · SHA 444ea9013c6a
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Unrealised gain (loss) on fair value of investment properties In 2025, the Company recognized a loss on revaluation of investment property amounting to Baht 157.4 million, whereas in 2024, it recognized a gain on revaluation of investment property of Baht 8.6 million.

  `MDA_A_FY2025` · `p013` · SHA 12faba81cb4a
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_A_FY2025`

##### SENA — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เสนาดีเวลลอปเม้นท์ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — -ธุรกิจพัฒนาอสังหาริมทรัพย์ประเภทที่อยู่อาศัยเพื่อขาย-ธุรกิจเช่า เช่น Livnex Program Rentnex Program อพาร์ทเม้น ศูนย์การค้าขนาดเล็ก อาคารสำนักงาน-ธุรกิจสนามกอล์ฟ-ธุรกิจไฟฟ้าพลังงานแสงอาทิตย์-ธุรกิจบริหารงานนิติบุคคล-ธุรกิจตัวแทนและนายหน้าให้บริการซื้อขายอสังหาริมทรัพย์-ธุรกิจปลูกและดูแลฟื้นฟูป่า-ธุรกิจตัวแทนจำหน่ายรถยนต์ไฟฟ้า

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 2.6bn | 1.77 | +4.7% | 9.7x | 6.3% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 17 · NPAT 13 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 3.4bn → FY2025 THB 5.2bn · +1.8bn · +52.9%

- RFO ปี 2568 อยู่ที่ 5,152 ลบ. เพิ่ม 52.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from real estate sales in 2025 was mainly derived from the Sena Hankyu Group, which generated total revenue of THB 2,559 million, mainly from ownership transfers of completed condominium projects under the following brands:The Kith : THB 676 million, The Niche : THB 767 million, Flexi : THB 1,214 million, Low-rise projects : THB 287 million. Ownership transfers were carried out continuously throughout the year and were the key factor contributing to the increase in revenue from real estate sales compared to the previous year. In addition, the Company reported revenue from real estate sales from Sena Group and its subsidiaries of THB 825 million, mainly from ownership transfers of com

  `MDA_SENA_FY2025` · `p025` · SHA bd0ee0aa6ca2
  </details>
- RFO ปี 2568 อยู่ที่ 5,152 ลบ. เพิ่ม 52.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ การซื้อกิจการและการรวมงบการเงิน และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 1. Revenue 1.1 Revenue from Real Estate Sales In 2025, the Company reported revenue from real estate sales of THB 4,075 million, representing an increase of THB 2,413 million (+145%) from THB 1,662 million in the previous year. The increase was mainly attributable to higher ownership transfers of residential projects, including the full-year revenue recognition of the Sena Hankyu Group in 2025, whereas in 2024 such group was accounted for as an associate and was consolidated as a subsidiary only during late December for a short period, resulting in a significant increase in revenue from real estate sales compared to the previous year.

  `MDA_SENA_FY2025` · `p008` · SHA ff480f9b612b
  </details>
- RFO ปี 2568 อยู่ที่ 5,152 ลบ. เพิ่ม 52.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ปริมาณขายและปริมาณการผลิต และ รายได้และเงื่อนไขของธุรกิจไฟฟ้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > SMARTIFY income increased to THB 17 million from THB 13 million (+32%) Golf course income remained stable at approximately THB 129 million, reflecting relatively stable service utilization compared to the previous year. 1.4 Solar Business Revenue In 2025, the Company reported solar business revenue of THB 51 million, representing an increase of THB 22 million (+77%) from THB 29 million in the previous year. The increase was attributable to higher revenue recognition in line with service and sales volume during the period. Overall, solar business revenue remained a small proportion of total revenue; however, revenue growth in 2025 supported total revenue growth compared to the previous year.

  `MDA_SENA_FY2025` · `p032` · SHA 85616ac9ba73
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 400m → FY2025 THB 324m · −76m · -19.0%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 324 ลบ. ลด 19.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross profit from real estate sales amounted to THB 1,331 million, representing an increase of THB 822 million (+161%) from THB 509 million in the previous year. The gross profit margin from real estate sales was approximately 33%, increasing from 31% in the previous year, reflecting cost management and differences in project transfer composition.However, the Company was able to maintain gross profit margins at a comparable level. 2.2 Cost of Rental and Gross Profit – Rental Business In 2025, the Company reported cost of rental of real estate of THB 87 million, representing an increase of THB 34 million (+64%) from THB 53 million in the previous year. Gross profit from rental business amount

  `MDA_SENA_FY2025` · `p036` · SHA cd74075e31c3
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 324 ลบ. ลด 19.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายได้และเงื่อนไขของธุรกิจไฟฟ้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > service income as explained in the revenue section above.Gross profit from service business amounted to THB 143 million, representing a decrease of THB 372 million (-72%) from THB 515 million in the previous year.The gross profit margin was approximately 42%, close to approximately 39% in the previous year. 2.4 Cost of Sales and Gross Profit – Solar Business In 2025, the Company reported solar business costs of THB 30 million, representing an increase of THB 10 million (+50%) from THB 20 million in the previous year.Gross profit from solar business amounted to THB 21 million, representing an increase of THB 12 million (+133%) from THB 9 million in the previous year.The gross profit margin wa

  `MDA_SENA_FY2025` · `p037` · SHA df1c5e6c8c06
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 324 ลบ. ลด 19.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ การซื้อกิจการและการรวมงบการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 4. Share of Profit (Loss) from Associates and Joint Ventures In 2025, the Company recognized share of profit from investments in associates and joint ventures of THB 92 million, representing a decrease of THB 229 million (-71%) from THB 321 million in the previous year.The decrease was mainly attributable to the Sena Hankyu joint venture group changing status to subsidiaries since late 2024. As a result, in 2025 the Company recognized operating results of such entities as revenues and expenses in consolidated financial statements instead of share of profit from associates and joint ventures, whereas in 2024 share of profit was recognized prior to the change in status.

  `MDA_SENA_FY2025` · `p040` · SHA 7aee3190af72
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 324 ลบ. ลด 19.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 7. Net Profit In 2025, the Company reported net profit of THB 500 million, representing a decrease of THB 8 million (-2%) from THB 509 million in the previous year. Although total revenue increased to THB 5,152 million, representing an increase of THB 1,822 million (+55%) from the previous year, gross profit increased in line with higher revenue from real estate sales, particularly projects under the Sena Hankyu Group which were recognized for the full year in 2025. However, higher selling and administrative expenses as well as higher finance costs resulted in net profit remaining at a level close to the previous year.

  `MDA_SENA_FY2025` · `p043` · SHA c61351c22a47
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_SENA_FY2025`

##### NOBLE — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท โนเบิล ดีเวลลอปเมนท์ จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์เพื่อขาย รับจ้างก่อสร้าง ให้เช่าและให้บริการ

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 2.5bn | 1.85 | -14.4% | 4.6x | 8.6% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 13 · NPAT 13 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 4

**RFO — เพราะอะไร** — FY2024 THB 11.0bn → FY2025 THB 6.9bn · −4.1bn · -37.0%

- RFO ปี 2568 อยู่ที่ 6,930 ลบ. ลด 37.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from Sales – Real Estate Development Business for the year 2025 amounted to THB 4,685.9 mm, representing a decrease of 29.6% compared to the previous year. The decline was mainly attributable to lower revenue recognition from ownership transfers of completed condominium units. Revenue from ownership transfers was primarily derived from Nue Evo Ari and Noble Form Thonglor, which commenced transfers in 3Q’25, as well as from Nue Mega Plus Bangna and Noble Terra Rama 9 – Ekkamai, which continued to record transfers throughout the year. ii) Revenue from Rental and Services Revenue from Rental and Services for the year 2025 amounted to THB 2,243.8 mm, representing a decrease of 48.3% comp

  `MDA_NOBLE_FY2025` · `p022` · SHA 1b862f2142b2
  </details>
- RFO ปี 2568 อยู่ที่ 6,930 ลบ. ลด 37.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อุปสงค์และกำลังซื้อในประเทศ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Key Highlights • Total revenue for 2025 amounted to THB 7,590.6 mm, representing a decrease of 34.4% compared to the previous year. The decline was mainly attributable to the slowdown in ownership transfers in line with the economic conditions, as well as lower revenue from rental and service businesses following the progressive completion of management and construction services for joint venture projects. However, other income increased, primarily driven by higher recognition of project management fees from joint venture projects, particularly those under the Khu Khot project. • For the year 2025, the Company reported a net profit of THB 593.1 mm, representing an increase of 37.4% compared

  `MDA_NOBLE_FY2025` · `p003` · SHA 4e3191e87889
  </details>
- RFO ปี 2568 อยู่ที่ 6,930 ลบ. ลด 37.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายขายและบริหาร และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Total Expenses i) Cost of Sales - Real Estate Development Business Cost of Sales - Real Estate Development Business for the year 2025 amounted to THB 3,432.9 mm, representing a decrease of 30.0% compared to the previous year, in line with the decline in revenue from Sales – Real Estate Development Business. ii) Cost of Rental and Services Cost of Rental and Services for the year 2025 amounted to THB 2,120.9 mm, representing a decrease of 44.9% compared to the previous year, in line with the decline in revenue from Rental and Services. iii) Selling & Administrative Expenses Selling and Administrative Expenses for the year 2025 amounted to THB 1,615.8 mm, representing a decrease of 2.7% compar

  `MDA_NOBLE_FY2025` · `p024` · SHA ab6efa975a7a
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 432m → FY2025 THB 593m · +162m · +37.4%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 593 ลบ. เพิ่ม 37.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ภาระหนี้และโครงสร้างเงินทุน และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the 12-month period ending 2024 ending 2025 (Restated) Gross Profit Margin (%) 20.4% 19.9% Net Profit Margin (%) /1 3.7% 7.8% Return on Equity (%)/2 6.8% 9.1% Return on Asset (%)/3 4.2% 4.5% Debt to Equity (times) 3.32x 2.58x Net Debt to Equity (times) 3.12x 2.37x Net Interest- Bearing Debt to Equity (times) 2.15x 1.71x Note : /1 Net Profit Margin is calculated by dividing the Net Income attributable to equity holders of the Company by Total Revenue (Total Revenue = Revenue from Sales-Real Estate Development Business + Revenue from Sale of Goods,Rental and Services + Other Income) /2 Return on Equity is calculated by Net Income trailing 12 months dividing average total shareholder’s equi

  `MDA_NOBLE_FY2025` · `p038` · SHA c23c087731ed
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 593 ลบ. เพิ่ม 37.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Total Gross Profit Total gross profit for the year 2025 amounted to THB 1,375.9 mm, representing a decrease of 38.7% compared to the previous year, in line with the decline in total revenue. The overall gross profit margin for 2025 was 19.9%, while the gross profit margin from the Real Estate Development Business was 26.7% for the year.

  `MDA_NOBLE_FY2025` · `p027` · SHA e606b26e7297
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 593 ลบ. เพิ่ม 37.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Income (Loss) Net Profit for the year 2025 amounted to THB 593.1 mm, representing an increase of 37.4% compared to 2024. The improvement was mainly attributable to higher other gains from the disposal of investment in the Nue Epic Asok–Rama 9 project, under Vertical Rama 9 Alliance 1 Co., Ltd., to Stecx Ventures Co., Ltd. in 3Q’25. In addition, other income increased from higher recognition of project management fees from joint venture projects.

  `MDA_NOBLE_FY2025` · `p029` · SHA 1753ffdd26e9
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 593 ลบ. เพิ่ม 37.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายขายและบริหาร และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Total Expenses i) Cost of Sales - Real Estate Development Business Cost of Sales - Real Estate Development Business for the year 2025 amounted to THB 3,432.9 mm, representing a decrease of 30.0% compared to the previous year, in line with the decline in revenue from Sales – Real Estate Development Business. ii) Cost of Rental and Services Cost of Rental and Services for the year 2025 amounted to THB 2,120.9 mm, representing a decrease of 44.9% compared to the previous year, in line with the decline in revenue from Rental and Services. iii) Selling & Administrative Expenses Selling and Administrative Expenses for the year 2025 amounted to THB 1,615.8 mm, representing a decrease of 2.7% compar

  `MDA_NOBLE_FY2025` · `p024` · SHA ab6efa975a7a
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Total Liabilities As of 31 December 2025, the Company’s total Liabilities was THB 17,376.3 mm, decreased by THB 3,568.4 mm from year-end 2024, primarily due to (i) a decrease in financial liabilities of THB 1,885.5, resulting from the repayment of loans from financial institutions following the ownership transfers of completed projects and the disposal of investment in the Nue Epic Asok–Rama 9 project; and (ii) a decrease in deposits and advances received from customers of THB 1,258.0 mm, mainly due to lower deposits and advances for the Nue Epic Asok– Rama 9 project. The key components of Liabilities in the Company consist of i) Bond of THB 8,870.9 mm, ii) Loan from Financial Institutions o

  `MDA_NOBLE_FY2025` · `p034` · SHA d0fe62b081b2
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Other Gain (Loss) Other gains for the year 2025 amounted to THB 924.6 mm, representing an increase of 19,516.1% compared to the previous year. The significant increase was mainly attributable to recognized gain from the disposal of investment in Nue Epic Asok–Rama 9 Project, under Vertical Rama 9 Alliance 1 Co., Ltd., to Stecx Ventures Co., Ltd., representing a 50% shareholding, as well as the gain from the fair value adjustment of land in the project in 3Q’25.

  `MDA_NOBLE_FY2025` · `p025` · SHA e260301f9456
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_NOBLE_FY2025`

##### LPN — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท แอล.พี.เอ็น.ดีเวลลอปเมนท์ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัท แอล.พี.เอ็น.ดีเวลลอปเมนท์ จำกัด (มหาชน) ประกอบธุรกิจพัฒนาอสังหาริมทรัพย์ในรูปแบบอาคารชุดพักอาศัยและบ้านพักอาศัย

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 2.4bn | 1.62 | +6.6% | 260.1x | 0.4% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 18 · NPAT 20 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 2

**RFO — เพราะอะไร** — FY2024 THB 8.0bn → FY2025 THB 6.7bn · −1.3bn · -16.0%

- RFO ปี 2568 อยู่ที่ 6,717 ลบ. ลด 16.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 790.36 million baht, resulting from the management of cash flow from operations to support debenture repayments in the first quarter of 2026. 5. Trade and other receivables increased by 111.99 million baht, or 28.59%, driven by an increase in management service business revenue and billing cycles as per contractual terms. From the aforementioned reasons, the value of total assets decreased by 478.75 million baht, or 1.98%. Total liabilities of the Company decreased by 245.89 million baht, or 2.01%, from 12.25779 billion baht to 12.01190 billion baht. The primary reasons were as follows: 1. Bank overdrafts and short-term borrowings decreased by 1.52413 billion baht, or 22.03%, from 6.91745 bi

  `MDA_LPN_FY2025` · `p027` · SHA 4e567f82318c
  </details>
- RFO ปี 2568 อยู่ที่ 6,717 ลบ. ลด 16.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2. Profitability Ratio % (Total revenue of main business – Total cost of goods sold) / Total 2.1 Gross Profit Margin from Main business revenue of main business 2.2 Gross Profit Margin from Sales of Real Estate % (Net sales - COGS) / Net Sales 2.3 Gross Profit Margin from Rental and Service % Rental and service revenue – Cost of rental and service / Rental and service revenue 2.4 Gross Profit Margin from Management Service % Revenue from management service – Cost of management service /

  `MDA_LPN_FY2025` · `p042` · SHA 55e119f70bac
  </details>
- RFO ปี 2568 อยู่ที่ 6,717 ลบ. ลด 16.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายขายและบริหาร และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Amount Unit: Million baht 1.Total revenue 1,983.59 2,033.60 (2.46%) 6,734.14 8,011.20 (15.94%) 2. Total revenue from sales 1,975.58 2,031.29 (2.74%) 6,717.26 7,991.98 (15.95%) 1) Revenue from sales of real estate 1,282.80 1,399.20 (8.32%) 4,063.39 5,490.01 (25.99%) 2) Rental and service business income 63.31 90.67 (30.18%) 336.69 375.92 (10.44%) 3) Income from management business 629.48 541.42 16.26% 2,317.18 2,126.05 8.99% 3. Total other income 8.01 2.31 246.35% 16.88 19.21 (12.12%) 4. Gross profit 319.76 289.85 10.32% 1,324.02 1,503.47 (11.94%) 5. Selling and administrative expenses 298.58 366.02 (18.42%) 1,088.70 1,166.06 (6.63%) 1) Selling expenses 124.76 132.01 (5.49%) 452.29 424.83 6.4

  `MDA_LPN_FY2025` · `p005` · SHA 7f6c8ddea755
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 111m → FY2025 THB 29m · −82m · -74.1%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 28.6 ลบ. ลด 74.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายขายและบริหาร และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Significant Financial Ration (%) 11. Total Gross Profit Margin 16.19% 14.27% 1.92% 19.71% 18.81% 0.90% 1) Gross Profit Margin from Real Estate Sales 15.66% 11.38% 4.28% 19.99% 17.41% 2.58% 2) Gross Profit Margin from Rental and Service Business 32.17% 31.51% 0.66% 29.40% 31.40% (2.00%) 3) Gross Profit Margin from Management Business 15.64% 18.84% (3.19%) 17.81% 20.20% (2.39%) 12. Total selling and administrative expenses to total 15.05% 18.00% (2.95%) 16.17% 14.56% 1.61% sales revenue 13. EBIT margin 1.13% (4.04%) 5.17% 2.93% 3.79% (0.86%) 14. EBITDA margin 2.42% (3.16%) 5.58% 4.57% 4.73% (0.16%) 15. Net Profit Margin (for the quarter) (2.61%) (5.52%) 2.92% 0.55% 1.50% (0.95%) 16. Net Profit

  `MDA_LPN_FY2025` · `p006` · SHA bfc2605cfc54
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 28.6 ลบ. ลด 74.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2. Profitability Ratio % (Total revenue of main business – Total cost of goods sold) / Total 2.1 Gross Profit Margin from Main business revenue of main business 2.2 Gross Profit Margin from Sales of Real Estate % (Net sales - COGS) / Net Sales 2.3 Gross Profit Margin from Rental and Service % Rental and service revenue – Cost of rental and service / Rental and service revenue 2.4 Gross Profit Margin from Management Service % Revenue from management service – Cost of management service /

  `MDA_LPN_FY2025` · `p042` · SHA 55e119f70bac
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 28.6 ลบ. ลด 74.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Translation - as buyers are required to undergo stricter loan approval processes by financial institutions. In addition, the decline in gross profit margin and net profit margin was affected by the recognition of inventory impairment and impairment of projects under development, as well as the provision for expenses related to project handovers and the establishment of the housing estate juristic person. Furthermore, the Company recognized a share of loss from investments in associates, which resulted in a significant year-on-year decrease in both gross and net profit margins. The Company’s efficiency ratios, particularly return on assets, decreased in line with the decline in profitability

  `MDA_LPN_FY2025` · `p039` · SHA e75f5d0e11f5
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 28.6 ลบ. ลด 74.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2.1 Gross Profit Margin from Main Business % 16.19 14.27 19.71 18.81 2.2 Gross Profit Margin from Sales of Real Estates % 15.66 11.38 19.99 17.41 2.3 Gross Profit Margin from Rental and Services % 32.17 31.51 29.40 31.40 2.4 Gross Profit Margin from Management services % 15.64 18.84 17.81 20.20 2.5 Net Profit Margin Ratio % (2.71) (5.68) 0.42 1.38 2.6 Gross Sales to Equity Ratio % 10.88 11.73 34.46 46.04

  `MDA_LPN_FY2025` · `p035` · SHA 0f021b7b2eb8
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายขายและบริหาร และ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > baht in the previous year. Income from the management service business rose to 629.48 million baht, an increase of 16.26% from 541.42 million baht, due to the expansion of condominium juristic person management, engineering services, and building facility management services, which helped strengthen recurring income and cash flow stability. The overall gross profit margin in Q4 2025 was 16.19%, increasing from 14.27% in the previous year, reflecting effective project cost management and the absence of inventory impairment provisions at a level as high as the previous year. Selling and administrative expenses in Q4 2025 were 298.58 million baht, decreasing by 18.42% from 366.02 million baht d

  `MDA_LPN_FY2025` · `p009` · SHA f0376ab91543
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: อัตรากำไรลดลง และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Translation - as buyers are required to undergo stricter loan approval processes by financial institutions. In addition, the decline in gross profit margin and net profit margin was affected by the recognition of inventory impairment and impairment of projects under development, as well as the provision for expenses related to project handovers and the establishment of the housing estate juristic person. Furthermore, the Company recognized a share of loss from investments in associates, which resulted in a significant year-on-year decrease in both gross and net profit margins. The Company’s efficiency ratios, particularly return on assets, decreased in line with the decline in profitability

  `MDA_LPN_FY2025` · `p039` · SHA e75f5d0e11f5
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_LPN_FY2025`

##### A5 — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท แอสเซท ไฟว์ กรุ๊ป จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ประกอบธุรกิจลงทุนในบริษัทอื่น โดยมีนโยบายลงทุนในบริษัทที่ประกอบธุรกิจอสังหาริมทรัพย์ และธุรกิจที่เกี่ยวข้อง (Holding Company)

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 2.1bn | 1.75 | -5.4% | 33.9x | 7.9% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 5 · NPAT 7 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 3

**RFO — เพราะอะไร** — FY2024 THB 1.8bn → FY2025 THB 1.3bn · −493m · -27.4%

- RFO ปี 2568 อยู่ที่ 1,308 ลบ. ลด 27.4% YoY; MD&A ระบุว่า บริษทั แอสเซท ไฟว ์กรุ๊ป จาํกดั (มหาชน) เลขที่ 199 อาคารเอส โอเอซิส ช้นั ที่ 12 ห้องเลขที่ 1210, 1211, 1212 ถนนวิภาวดีรังสิต แขวงจอมพล เขตจตุจกั ร กรุงเทพฯ 10900 Asset Five Group Public Company Limited 199 S-OASIS Building, 12th Floors, Unit 1210, 1211, 1212 Vibhavadi-Rangsit Rd., Chompol, Chatuchak, Bangkok 10900 Tel : 02-026-3512 1. Revenue from real estate sales for the year ended December 31, 2025 amounted to THB 1,307.59 million, comprising revenue from projects in the Bangkok metropolitan area of THB 1,243.05 million and from provincial area projec
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > บริษทั แอสเซท ไฟว ์กรุ๊ป จาํกดั (มหาชน) เลขที่ 199 อาคารเอส โอเอซิส ช้นั ที่ 12 ห้องเลขที่ 1210, 1211, 1212 ถนนวิภาวดีรังสิต แขวงจอมพล เขตจตุจกั ร กรุงเทพฯ 10900 Asset Five Group Public Company Limited 199 S-OASIS Building, 12th Floors, Unit 1210, 1211, 1212 Vibhavadi-Rangsit Rd., Chompol, Chatuchak, Bangkok 10900 Tel : 02-026-3512 1. Revenue from real estate sales for the year ended December 31, 2025 amounted to THB 1,307.59 million, comprising revenue from projects in the Bangkok metropolitan area of THB 1,243.05 million and from provincial area projects of THB 64.54 million. This represents a decrease of THB 463.37 million, or 26.17%, from the prior year, attributable to a reduction in re

  `MDA_A5_FY2025` · `p014` · SHA 40e25282ada6
  </details>
- RFO ปี 2568 อยู่ที่ 1,308 ลบ. ลด 27.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Overview of Operations Performance For the fiscal year ended December 31, 2025, the Company recorded total revenue of THB 1,317.72 million, a decrease of THB 491.87 million, or 27.18%, from the prior year. Net profit amounted to THB 102.95 million, a decline of THB 350.34 million, or 77.29% from the prior year, representing a net profit margin of 7.81%, down 17.24% from the prior year's net profit margin of 25.05%. The primary factors contributing to the decline in operating performance were a reduction in the number of property ownership transfers compared to the prior year, as well as a decrease in the share of profit from investments in joint ventures. No share of profit from associates w

  `MDA_A5_FY2025` · `p011` · SHA de45329536d4
  </details>
- RFO ปี 2568 อยู่ที่ 1,308 ลบ. ลด 27.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ ราคาขายและส่วนผสมผลิตภัณฑ์ และ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > the impact of selling price adjustments and promotional campaigns implemented to stimulate sales demand. As a result of these factors, gross profit decreased by THB 360.41 million. The gross profit margin for the current year stood at 31.01%, compared to 43.25% in the prior year, representing a contraction of 12.24%. 4. Cost of rendering renovation and interior decoration services decreased by THB 20.22 million in its entirety compared to the prior year, consistent with the corresponding decline in service revenue, as no revenue was recognized under this segment during the current year. 5. Distribution costs increased by THB 4.11 million, or 3.27%, compared to the prior year. This was primar

  `MDA_A5_FY2025` · `p015` · SHA 46566fa253ed
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 453m → FY2025 THB 103m · −350m · -77.3%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 103 ลบ. ลด 77.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Overview of Operations Performance For the fiscal year ended December 31, 2025, the Company recorded total revenue of THB 1,317.72 million, a decrease of THB 491.87 million, or 27.18%, from the prior year. Net profit amounted to THB 102.95 million, a decline of THB 350.34 million, or 77.29% from the prior year, representing a net profit margin of 7.81%, down 17.24% from the prior year's net profit margin of 25.05%. The primary factors contributing to the decline in operating performance were a reduction in the number of property ownership transfers compared to the prior year, as well as a decrease in the share of profit from investments in joint ventures. No share of profit from associates w

  `MDA_A5_FY2025` · `p011` · SHA de45329536d4
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 103 ลบ. ลด 77.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ ราคาขายและส่วนผสมผลิตภัณฑ์ และ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > the impact of selling price adjustments and promotional campaigns implemented to stimulate sales demand. As a result of these factors, gross profit decreased by THB 360.41 million. The gross profit margin for the current year stood at 31.01%, compared to 43.25% in the prior year, representing a contraction of 12.24%. 4. Cost of rendering renovation and interior decoration services decreased by THB 20.22 million in its entirety compared to the prior year, consistent with the corresponding decline in service revenue, as no revenue was recognized under this segment during the current year. 5. Distribution costs increased by THB 4.11 million, or 3.27%, compared to the prior year. This was primar

  `MDA_A5_FY2025` · `p015` · SHA 46566fa253ed
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 103 ลบ. ลด 77.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ค่าใช้จ่ายขายและบริหาร และ ยอดขายและการโอนที่ดินนิคมอุตสาหกรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > primarily attributable to a loss on the land sale of one subsidiary amounting to THB 13.24 million. In addition, the Company incurred common area maintenance expenses for completed projects that had commenced ownership transfer to customers, resulting in an increase of THB 9.77 million in project management-related administrative expenses. 7. Impairment loss on investment in joint venture decreased by THB 73.55 million in its entirety, as in 2024, the Company had assessed the recoverable amount of the investment and determined that the carrying value exceeded the recoverable amount, thereby recognizing the impairment loss accordingly. The Company subsequently disposed of its entire remaining

  `MDA_A5_FY2025` · `p016` · SHA ff3cc055bc31
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 103 ลบ. ลด 77.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Total revenues 1,314,095,371 1,806,104,520 (492,009,149) (27.24) Cost of real estate sales 902,079,717 1,005,038,500 (102,958,783) (10.24) Cost of rendering renovation and interior - 20,218,492 (20,218,492) (100.00) decoration services Distribution costs 129,691,209 125,583,380 4,107,829 3.27 Administrative expenses 111,425,318 96,557,698 14,867,620 15.40 Impairment loss on investments in joint - 73,546,137 (73,546,137) (100.00) venture Total expenses 1,143,196,244 1,320,944,207 (177,747,963) (13.46) Profit from operating activities 170,899,127 485,160,313 (314,261,186) (64.77)

  `MDA_A5_FY2025` · `p007` · SHA 2757be1ab8ff
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ค่าใช้จ่ายขายและบริหาร และ ยอดขายและการโอนที่ดินนิคมอุตสาหกรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > primarily attributable to a loss on the land sale of one subsidiary amounting to THB 13.24 million. In addition, the Company incurred common area maintenance expenses for completed projects that had commenced ownership transfer to customers, resulting in an increase of THB 9.77 million in project management-related administrative expenses. 7. Impairment loss on investment in joint venture decreased by THB 73.55 million in its entirety, as in 2024, the Company had assessed the recoverable amount of the investment and determined that the carrying value exceeded the recoverable amount, thereby recognizing the impairment loss accordingly. The Company subsequently disposed of its entire remaining

  `MDA_A5_FY2025` · `p016` · SHA ff3cc055bc31
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Total revenues 1,314,095,371 1,806,104,520 (492,009,149) (27.24) Cost of real estate sales 902,079,717 1,005,038,500 (102,958,783) (10.24) Cost of rendering renovation and interior - 20,218,492 (20,218,492) (100.00) decoration services Distribution costs 129,691,209 125,583,380 4,107,829 3.27 Administrative expenses 111,425,318 96,557,698 14,867,620 15.40 Impairment loss on investments in joint - 73,546,137 (73,546,137) (100.00) venture Total expenses 1,143,196,244 1,320,944,207 (177,747,963) (13.46) Profit from operating activities 170,899,127 485,160,313 (314,261,186) (64.77)

  `MDA_A5_FY2025` · `p007` · SHA 2757be1ab8ff
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_A5_FY2025`

##### BRI — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท บริทาเนีย จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์ประเภทที่อยู่อาศัยแนวราบ ได้แก่ บ้านเดีี่ยว บ้านแฝด และทาวน์โฮม

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 2.0bn | 1.39 | -8.6% | 18.5x | 5.5% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 20 · NPAT 20 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 2

**RFO — เพราะอะไร** — FY2024 THB 3.4bn → FY2025 THB 2.3bn · −1.1bn · -32.8%

- RFO ปี 2568 อยู่ที่ 2,275 ลบ. ลด 32.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, Revenues from sales of real estate amounted to Baht 1,839.1 million. In addition, the group has Revenues from project management amounted to Baht 128.8 million, Service Income amounted to Baht 307.5 million, and Other Income amounted to Baht 179.6 million. From the aforementioned revenue, the Group has total revenue of 2025 amounted to Baht 2,455.1 million, decreased by 36.4 percent from the same period of last year. And the group made profit for the period of 2025 amounted to Baht 125.8 million.

  `MDA_BRI_FY2025` · `p005` · SHA 954e4c8b655b
  </details>
- RFO ปี 2568 อยู่ที่ 2,275 ลบ. ลด 32.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, selling expenses of the Group amounted to Baht 343.9 million, accounted for 14.0 percent of total revenues and decreased by Baht 94.8 million or decreased by 21.6 percent from the same period of last year. This was mainly due to the group has managed Special business tax and ownership transfer fees, which varies according to revenues from sales of real estate, other selling expenses and employee expense.

  `MDA_BRI_FY2025` · `p045` · SHA 57e50d70ae0d
  </details>
- RFO ปี 2568 อยู่ที่ 2,275 ลบ. ลด 32.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, cost of real estate sales of the Group amounted to Baht 1,521.6 million, accounted for 62.0 percent of total revenues, decreased by Baht 552.1 million or decreased by 26.6 percent from the same period of last year, which varies according to revenues from sales of real estate.

  `MDA_BRI_FY2025` · `p043` · SHA 20475f87c7c2
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 427m → FY2025 THB 126m · −301m · -70.5%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 126 ลบ. ลด 70.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, Revenues from sales of real estate amounted to Baht 1,839.1 million. In addition, the group has Revenues from project management amounted to Baht 128.8 million, Service Income amounted to Baht 307.5 million, and Other Income amounted to Baht 179.6 million. From the aforementioned revenue, the Group has total revenue of 2025 amounted to Baht 2,455.1 million, decreased by 36.4 percent from the same period of last year. And the group made profit for the period of 2025 amounted to Baht 125.8 million.

  `MDA_BRI_FY2025` · `p005` · SHA 954e4c8b655b
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 126 ลบ. ลด 70.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, cost of real estate sales of the Group amounted to Baht 1,521.6 million, accounted for 62.0 percent of total revenues, decreased by Baht 552.1 million or decreased by 26.6 percent from the same period of last year, which varies according to revenues from sales of real estate.

  `MDA_BRI_FY2025` · `p043` · SHA 20475f87c7c2
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 126 ลบ. ลด 70.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > mainly from cash receipt from project development costs for sale amounted Baht 920.0 million and other

  `MDA_BRI_FY2025` · `p098` · SHA 96f09a8eb409
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 126 ลบ. ลด 70.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Finance cost of the Group was mainly from interest payment of short-term loans from parent

  `MDA_BRI_FY2025` · `p069` · SHA 1f123d15b8f0
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, there is no Gain on disposal of investments in subsidiaries because the Group has not new

  `MDA_BRI_FY2025` · `p037` · SHA 2e905fbed7d4
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ยอดขายและการโอนที่ดินนิคมอุตสาหกรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gain on disposal of investments in subsidiaries and land transfer rights

  `MDA_BRI_FY2025` · `p008` · SHA 097be720ecbf
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_BRI_FY2025`

##### PRIN — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ปริญสิริ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัทและบริษัทย่อยประกอบธุรกิจพัฒนาอสังหาริมทรัพย์ ประเภทหมู่บ้านจัดสรร และประเภทอาคารชุดพักอาศัย

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.7bn | 1.36 | -22.3% | 24.9x | 1.9% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 7 · NPAT 7 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 2.0bn → FY2025 THB 1.7bn · −355m · -17.6%

- RFO ปี 2568 อยู่ที่ 1,667 ลบ. ลด 17.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Total Revenue In 2025, the Company and its subsidiaries generated total revenue of 1,694.33 million baht, which was a decrease of 358.15 million baht or 17.45% decrease from 2024. The main reason for the decrease in real estate sales. Income from real estate sales was 1,630.24 million baht, a decrease of 355.34 million baht or 17.90% compared to 2024.

  `MDA_PRIN_FY2025` · `p013` · SHA cc86711a3bf3
  </details>
- RFO ปี 2568 อยู่ที่ 1,667 ลบ. ลด 17.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Amount % (348.70) (28.22) 28.54 5.51 (35.19) (15.16) (355.34) (17.90) In 2025, in comparison with 2024 revenue from townhouses was 886.97 million baht, a decrease of 348.70 million baht 28.22%. Revenue from the single-detached house was 546.41 million baht, a increase of 28.54 million baht or 5.51%. Revenue from condominiums was 196.86 million baht, an decrease of 35.19 million baht or 15.16%

  `MDA_PRIN_FY2025` · `p014` · SHA 7d9690a96764
  </details>
- RFO ปี 2568 อยู่ที่ 1,667 ลบ. ลด 17.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ราคาขายและส่วนผสมผลิตภัณฑ์ และ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Company and its subsidiaries incurred a cost of real estate sales of 1,108.51 million baht or 68.00% of the revenue from sales of real estate. In 2024, the cost of real estate sales was 1,301.61 million baht or 65.55%, a decrease of 193.10 million baht or 14.84%. Due to fierce competition in the industry, cause to maintain selling prices in order to remain competitive. www.prinsiri.com

  `MDA_PRIN_FY2025` · `p015` · SHA 6d3a145d9d36
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 111m → FY2025 THB 31m · −80m · -71.9%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 31.1 ลบ. ลด 71.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Financing cost In 2025, the Company and its subsidiaries incurred a financing cost of 117.50 million baht or 6.94% of total revenue, a increase of 14.07 million baht or 13.60% compared with 2024. This increase is due to a decrease in inventory, resulting in lower project costs, and an increase in land awaiting development.

  `MDA_PRIN_FY2025` · `p017` · SHA 2aed29cc1ca6
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 31.1 ลบ. ลด 71.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net profit In 2024, the net profit of the Company and its subsidiaries was 31.10 million baht or 1.84% of total revenue, a decrease of 79.58 million baht or 71.90% decrease from 2024, a decrease from the aforementioned reasons. Please be informed accordingly. (Mr. Chairat Kovitchindachai)

  `MDA_PRIN_FY2025` · `p018` · SHA 68d379c49a38
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 31.1 ลบ. ลด 71.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ราคาขายและส่วนผสมผลิตภัณฑ์ และ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Company and its subsidiaries incurred a cost of real estate sales of 1,108.51 million baht or 68.00% of the revenue from sales of real estate. In 2024, the cost of real estate sales was 1,301.61 million baht or 65.55%, a decrease of 193.10 million baht or 14.84%. Due to fierce competition in the industry, cause to maintain selling prices in order to remain competitive. www.prinsiri.com

  `MDA_PRIN_FY2025` · `p015` · SHA 6d3a145d9d36
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 31.1 ลบ. ลด 71.9% YoY; MD&A ระบุว่า ทะเบียนเลขที่ 0107547000320 โทร. 02-022-8988, 02-022-8989, 02-022-8998 Tel. 02-022-8988, 02-022-8989, 02-022-8998 In 2025, the Company and its subsidiaries incurred distribution costs of 118.34 million baht or 6.98% of total revenue, a decrease of 24.91 million baht or 17.39% compared to 2024, correlated with a decrease in revenues and cost control efficiency.
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > ทะเบียนเลขที่ 0107547000320 โทร. 02-022-8988, 02-022-8989, 02-022-8998 Tel. 02-022-8988, 02-022-8989, 02-022-8998 In 2025, the Company and its subsidiaries incurred distribution costs of 118.34 million baht or 6.98% of total revenue, a decrease of 24.91 million baht or 17.39% compared to 2024, correlated with a decrease in revenues and cost control efficiency.

  `MDA_PRIN_FY2025` · `p016` · SHA 3b0b3a3f165a
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_PRIN_FY2025`

##### NVD — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เนอวานา ดีเวลลอปเม้นท์ จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัทฯ ประกอบธุรกิจพัฒนาอสังหาริมทรัพย์ประเภทบ้านจัดสรร คอนโดมิเนียม และขยายการพัฒนาโครงการอสังหาริมทรัพย์เพื่อเช่า เช่น อาคารจอดรถ คอมมูนิตี้มอลล์ และธุรกิจรับจ้างก่อสร้างทั่วไป ทั้งที่เป็นการก่อสร้างเพื่อการพักอาศัย และไม่พักอาศัย เช่น งานก่อสร้างวิลล่าให้กับรีสอร์ท หอพักคนงาน สถานีบริการน้ำมัน เป็นต้น ประกอบกับ การขายสินค้าประเภทวัสดุก่อสร้างที่ทางบริษัทฯ ผลิตเองให้กับบุคคลภายนอก ได้แก่ รั้วสำเร็จรูป เสา-คาน-แ…

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.5bn | 0.83 | +5.1% | 8.8x | 9.7% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 5 · NPAT 9 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 2

**RFO — เพราะอะไร** — FY2024 THB 1.4bn → FY2025 THB 1.6bn · +168m · +11.8%

- RFO ปี 2568 อยู่ที่ 1,599 ลบ. เพิ่ม 11.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การซื้อกิจการและการรวมงบการเงิน และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenues NVD reported total consolidated revenues of Bt. 1,842 m. for YE25, increased 15% yoy Compared to the same period last year, segmented revenues consist of: • Revenues from Sales of Real Estate up 15% yoy, • Revenues from Construction Contracts down 87% yoy • Other income up 42% yoy, Revenues from Sales of Real Estate were Bt. 1,593m. up 15% yoy. The YE25 revenue contribution was mainly from the residential projects such as DEFINE Krungthep Kreetha, DEFINE Ekkamai-Ramintra, ABSOLUTE Krungthep Kreetha , @Work Krungthep Kreetha and Land Krungthep Kreetha , Ekkamai – Ramintra, Pattaya. Revenues from Construction Service Contracts down 87% yoy. The perform ance in this revenue line was ma

  `MDA_NVD_FY2025` · `p012` · SHA 6cae83a23fdf
  </details>
- RFO ปี 2568 อยู่ที่ 1,599 ลบ. เพิ่ม 11.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ ค่าใช้จ่ายขายและบริหาร และ การซื้อกิจการและการรวมงบการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Car Park Soi Choeiphuang management fees, services incomes, interest incomes and other miscellaneous incomes. Gain from fair value adjustment of investment property were Bt. 139 m. resulting from the increase in the fair value assessed anew. This pertains to the company's land in the newly developed Krungthep Kreetha area, which has shown clear economic development (as assessed by an independent appraiser) in the investment propertie s. Cost of Sales , Distribution cost , Administrative expenses and Profit from operating activities Total consolidated costs for YE25 were Bt. 1,489m. up 9% yoy in line with revenue increase. The total costs consist of: • Costs Real Estate Sold of Bt. 1,106m. •

  `MDA_NVD_FY2025` · `p013` · SHA e24aa43e5982
  </details>
- RFO ปี 2568 อยู่ที่ 1,599 ลบ. เพิ่ม 11.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Stock Exchange of Thailand According to the resolution of the Board of Directors’ Meeting No. 1/2026 of Nirvana Development Public Company Limited (“Company” or “NVD” or “Nirvana”) held on 23th February 2026 to approve the financial statements for the year ended 31 December 2025, the Company would like to report the financial performance for the year ended 31 December 2025 as follows. NVD recorded total revenues of Bt. 1,842m in 2025, up 15% yoy and up 147% qoq. The YE25 net profit attributable to the owners of the parent company was Bt. 156m, compared to Bt. 86m in YE24 The year 2025 continues to present significant challenges. Pressures arising from prevailing circumstances including t

  `MDA_NVD_FY2025` · `p002` · SHA 5df271254515
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 86m → FY2025 THB 156m · +70m · +80.7%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 156 ลบ. เพิ่ม 80.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ ค่าใช้จ่ายขายและบริหาร และ การซื้อกิจการและการรวมงบการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Car Park Soi Choeiphuang management fees, services incomes, interest incomes and other miscellaneous incomes. Gain from fair value adjustment of investment property were Bt. 139 m. resulting from the increase in the fair value assessed anew. This pertains to the company's land in the newly developed Krungthep Kreetha area, which has shown clear economic development (as assessed by an independent appraiser) in the investment propertie s. Cost of Sales , Distribution cost , Administrative expenses and Profit from operating activities Total consolidated costs for YE25 were Bt. 1,489m. up 9% yoy in line with revenue increase. The total costs consist of: • Costs Real Estate Sold of Bt. 1,106m. •

  `MDA_NVD_FY2025` · `p013` · SHA e24aa43e5982
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 156 ลบ. เพิ่ม 80.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ อุปสงค์และกำลังซื้อในประเทศ และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Distribution cost and Administrative Expenses Distribution cost during YE25 of Bt. 155m. decreased 20% yoy NVD has managed its selling and distribution expenses in alignment with the slowdown in revenue, initially scaling up marketing and media activities during the second half of the year to stimulate sales. At the same time, variable expenses linked to revenu e have increased, including transfer . Administrative Expenses in YE25 of Bt. 221m. increased 15% yoy. NVD has recognized provisions for the impairment of slow-moving inventory and for doubtful accounts, Bt.151m. NVD continues to place strong emphasis on effective cost management in order to improve profit margins and to ensure alignm

  `MDA_NVD_FY2025` · `p014` · SHA cac0d6ba9fe4
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 156 ลบ. เพิ่ม 80.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Profit from operating activities increased significantly from 14% at End FY24 to 19% in FY25 Total liabilities-to-equity ratio at End YE25 was 1.67x, decreased from 1.95x at End FY24, and the net interest-bearing

  `MDA_NVD_FY2025` · `p031` · SHA 9457ec148dad
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 156 ลบ. เพิ่ม 80.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้ และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Assets Total assets End-YE25 were Bt.15,045m, increased 0% yoy. The primary factors were the reclassification of bills of exchange receivable related to property transfers, totaling Bt.322m. which will mature in 2026. In addition, there was a net decrease in inventories and property development costs amounting to Bt.338m. mainly attributable to the Nirvana @ WORK , Nirvana DEFINE , and Nirvana ABSOLUTE projects across both locations —Krungthep Kreetha and Ekkamai–Ram Intra. Furthermore, investment properties increased by Bt.139 m. Significant changes in line items are summarized as follows:

  `MDA_NVD_FY2025` · `p017` · SHA 34d8f19ff72d
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ ค่าใช้จ่ายขายและบริหาร และ การซื้อกิจการและการรวมงบการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Car Park Soi Choeiphuang management fees, services incomes, interest incomes and other miscellaneous incomes. Gain from fair value adjustment of investment property were Bt. 139 m. resulting from the increase in the fair value assessed anew. This pertains to the company's land in the newly developed Krungthep Kreetha area, which has shown clear economic development (as assessed by an independent appraiser) in the investment propertie s. Cost of Sales , Distribution cost , Administrative expenses and Profit from operating activities Total consolidated costs for YE25 were Bt. 1,489m. up 9% yoy in line with revenue increase. The total costs consist of: • Costs Real Estate Sold of Bt. 1,106m. •

  `MDA_NVD_FY2025` · `p013` · SHA e24aa43e5982
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: อัตรากำไรดีขึ้น และ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ อุปสงค์และกำลังซื้อในประเทศ และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Distribution cost and Administrative Expenses Distribution cost during YE25 of Bt. 155m. decreased 20% yoy NVD has managed its selling and distribution expenses in alignment with the slowdown in revenue, initially scaling up marketing and media activities during the second half of the year to stimulate sales. At the same time, variable expenses linked to revenu e have increased, including transfer . Administrative Expenses in YE25 of Bt. 221m. increased 15% yoy. NVD has recognized provisions for the impairment of slow-moving inventory and for doubtful accounts, Bt.151m. NVD continues to place strong emphasis on effective cost management in order to improve profit margins and to ensure alignm

  `MDA_NVD_FY2025` · `p014` · SHA cac0d6ba9fe4
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_NVD_FY2025`

##### ANAN — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท อนันดา ดีเวลลอปเม้นท์ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์ 1) คอนโดมิเนียมติดสถานีขนส่งมวลชนระบบรางในเขตกรุงเทพและปริมณฑล 2) บ้านจัดสรรแนวราบ นอกจากนี้ บริษัทยังประกอบธุรกิจภายใต้บริษัทย่อยอื่นๆ ได้แก่ ธุรกิจการเป็นตัวแทนการซื้อขายห้องชุด ธุรกิจรับบริหารโครงการอสังหาริมทรัพย์ให้กับนิติบุคคลบ้านจัดสรร และนิติบุคคลอาคารชุด

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.4bn | 0.34 | -17.1% | 5.9x | 1.0% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 6 · NPAT 15 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 5

**RFO — เพราะอะไร** — FY2024 THB 5.8bn → FY2025 THB 5.6bn · −176m · -3.0%

- RFO ปี 2568 อยู่ที่ 5,630 ลบ. ลด 3.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อุปสงค์และกำลังซื้อในประเทศ
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue Total revenue in 2025 is accounted for Baht 6,554.8 million, a decrease of Baht 105.7 million or 1.6% YoY, consisting of :- Revenue from Real Estate Sales in 2025, revenue from real estate sales totalled of Baht 4,964.4 million, slightly decreasing of Baht 69.6 million or 1.4% YoY. This decline was mainly attributable to the slowdown in ownership transfers in line with economic conditions and pressures on purchasing power, which affected customers’ decision-making. In addition, several projects under the Company and its subsidiaries were completed and closed during the year. However, the Company and its subsidiaries were supported by the acceleration of ownership transfers of ready-t

  `MDA_ANAN_FY2025` · `p016` · SHA 6864e21d6abb
  </details>
- RFO ปี 2568 อยู่ที่ 5,630 ลบ. ลด 3.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenues Revenue from sales of real estate 4,964.4 5,034.3 (69.9) (1.4) Revenue from project management services and commission income 338.6 486.7 (148.1) (30.4) Revenue from rental and services 326.8 284.4 42.4 14.9 Other incomes 925.0 855.1 70.0 8.2 Total Revenues 6,554.8 6,660.5 (105.7) (1.6)

  `MDA_ANAN_FY2025` · `p010` · SHA 6d30c6fa37b8
  </details>
- RFO ปี 2568 อยู่ที่ 5,630 ลบ. ลด 3.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Profit attributable to equity holders of the Company In 2025, the Company and its subsidiaries reported net profit attributable to owners of the parent of Baht 55.7 million, a decrease of Baht 307.5 million, or 84.7% YoY. Total revenue remained relatively stable at Baht 6,554.8 million, slightly decreasing by 1.6% YoY. Gross profit declined by Baht 331.5 million, or 13.5% YoY, mainly due to an increase in cost of real estate sales of Baht 232.4 million, or 6.4% YoY, together with a rise in finance costs of Baht 145.4 million, or 35.4% YoY. However, the Company effectively managed its selling and administrative expenses, which decreased by Baht 273.4 million, or 15.8% YoY, driven by conti

  `MDA_ANAN_FY2025` · `p014` · SHA efe25d4d49b2
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 334m → FY2025 THB 56m · −279m · -83.3%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 55.7 ลบ. ลด 83.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Profit (loss) for the periods from discontinuing oprations - - - - Profit (loss) for the period 59.2 417.5 (358.3) (85.8) Profit attributable to non-controlling interests 3.6 54.4 (50.8) (93.4) Profit (loss) attributable to equity holders of the Company 55.7 363.2 (307.5) (84.7) * The 2024 financial statements have been restated due to a change in accounting policy regarding the measurement of investment properties, transitioning from the cost method to the fair value method.

  `MDA_ANAN_FY2025` · `p013` · SHA 78b22cdf2100
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 55.7 ลบ. ลด 83.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Profit attributable to equity holders of the Company In 2025, the Company and its subsidiaries reported net profit attributable to owners of the parent of Baht 55.7 million, a decrease of Baht 307.5 million, or 84.7% YoY. Total revenue remained relatively stable at Baht 6,554.8 million, slightly decreasing by 1.6% YoY. Gross profit declined by Baht 331.5 million, or 13.5% YoY, mainly due to an increase in cost of real estate sales of Baht 232.4 million, or 6.4% YoY, together with a rise in finance costs of Baht 145.4 million, or 35.4% YoY. However, the Company effectively managed its selling and administrative expenses, which decreased by Baht 273.4 million, or 15.8% YoY, driven by conti

  `MDA_ANAN_FY2025` · `p014` · SHA efe25d4d49b2
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 55.7 ลบ. ลด 83.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ต้นทุนทางการเงิน และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Selling & Administrative Expenses - - - - Selling expenses 743.6 816.9 (73.3) (9.0) Administrative expenses 714.4 914.5 (200.1) (21.9) Total Selling & Administrative Expenses 1,458.0 1,731.4 (273.4) (15.8) Operating Profit (loss) 667.6 725.7 (58.1) (8.0) Finance cost (556.0) (410.7) (145.4) 35.4 Tax income (expenses) (212.6) (378.4) 165.8 (43.8) Profit (loss) before share of profit from investments in joint ventures (101.1) (63.4) (37.7) 59.4 Share of profit from investments in joint ventures 160.3 480.9 (320.6) (66.7) Profit (loss) for the periods from continuing oprations 59.2 417.5 (358.3) (85.8)

  `MDA_ANAN_FY2025` · `p012` · SHA 59cc959953ca
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 55.7 ลบ. ลด 83.3% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Costs Total costs in 2025 amounted to Baht 4,429.2 million, an increase of Baht 225.8 million, or 5.4% YoY, consisting of :- 1. Cost of real estate sales in 2025 amounted to Baht 3,868.0 million, increasing by Baht 232.4 million, or 6.4% YoY. 2. Cost of project management and commission in 2025 amounted to Baht 372.6 million, a decrease of Baht 36.4 million, or 8.9% YoY. 3. Cost of rental and service operations in 2025 amounted to Baht 188.6 million, an increase of Baht 29.8 million, or 18.8% YoY.

  `MDA_ANAN_FY2025` · `p019` · SHA 5ec94e3d0e5e
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ความเสี่ยงด้านภูมิรัฐศาสตร์ และ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > and Ideo Mobi Rangnam condominiums project. In addition, the Group changed its accounting policy regarding the measurement of investment properties from the cost model to the fair value model, effective for the financial statements from 30 June 2025 onwards. As a result, investment properties increased by Baht 1,355.0 million, or 220.0%, from the end of 2024, to better reflect the fair value of the Group’s assets in the financial statements.

  `MDA_ANAN_FY2025` · `p028` · SHA fcd0c9ec208e
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > compared to the same period of the prior year. 2. Rental and service income in 2025 amounted to Baht 326.8 million, increasing by Baht 42.4 million or 14.9% YoY. 3. Other income in 2025 totalled Baht 925.0 million, an increase of Baht 70.0 million or 8.2% YoY. The increase was mainly attributable to the recognition of gains from the fair value adjustment of investment properties, which the Company began recording from the second quarter of 2025 and continued to recognize on an ongoing basis thereafter.

  `MDA_ANAN_FY2025` · `p017` · SHA 8c35eba7ebd3
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_ANAN_FY2025`

##### ORN — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท อรสิริน โฮลดิ้ง จํากัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัทประกอบธุรกิจโดยการเข้าถือหุ้นในบริษัทอื่น (Holding Company) ที่ประกอบธุรกิจพัฒนาอสังหาริมทรัพย์ประเภทที่อยู่อาศัยเพื่อขาย ทั้งโครงการอสังหาริมทรัพย์แนวราบและแนวสูง

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.3bn | 0.86 | +24.6% | 5.7x | 10.7% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 8 · NPAT 7 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 1.4bn → FY2025 THB 2.1bn · +746m · +54.7%

- RFO ปี 2568 อยู่ที่ 2,108 ลบ. เพิ่ม 54.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue In 2025, ending on December 31, 2025, the company reported total sales revenue of 2,108.25 million baht. Compared to the same period last year, the revenue increased by 745.60 million baht or 74.72%, which had total sales revenue of 1,362.65 million baht. The proportion of revenue from the transfer of ownership of housing project amounted to 913.03 million baht, while the transfer of ownership of high-rise projects amounted to 1,178.71 million baht. These revenues represented 43.12% and 55.66% of the total revenue respectively. Additionally, the company earned 10.77 million baht in revenue from Mill Hill International School Thailand and 5.74 million baht in rental and service income

  `MDA_ORN_FY2025` · `p006` · SHA 4a5abf471ced
  </details>
- RFO ปี 2568 อยู่ที่ 2,108 ลบ. เพิ่ม 54.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Distribution Costs In 2025, the company group incurred distribution costs of 362.33 million baht which is an increase of 75.95% from 205.93 million baht in the same period last year. The increase was mainly due to higher promotional and advertising expenses for new projects, as well as commission costs for sales agents of high-rise projects. Also, transfer expenses that varied in line with the increase in sales revenue.

  `MDA_ORN_FY2025` · `p011` · SHA 5bd1ef85184b
  </details>
- RFO ปี 2568 อยู่ที่ 2,108 ลบ. เพิ่ม 54.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > operations. Overall, the Company reported gross profit of 868.54 million baht and 547.06 million baht in 2025 and 2024, respectively, representing an increase of 321.48 million baht or 58.77% compared to the same period of the prior year. In 2025, the Group’s gross profit margin was 41.20% of sales revenue, an increase of 1.05 percentage points from 40.15% in the same period of the prior year, primarily driven by higher contributions from low-rise housing projects.

  `MDA_ORN_FY2025` · `p010` · SHA b855b937d6f2
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 141m → FY2025 THB 226m · +86m · +61.0%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 226 ลบ. เพิ่ม 61.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Profit (Loss) Attributable to Parent Company In 2025 and 2024, the company group recorded a net loss attributable to the parent company of 226.28 million baht and 140.56 million baht respectively. This represents a net profit (loss) margin of 10.69% and 10.29% of total revenue respectively.

  `MDA_ORN_FY2025` · `p014` · SHA d608a3f3894a
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 226 ลบ. เพิ่ม 61.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Cost of Goods Sold and Gross Profit In 2025 and 2024, the Group reported cost of sales and services of 1,239.71 million baht and 815.58 million baht, respectively, representing an increase of 424.13 million baht or 52.00% compared to the same period of the prior year. Such costs can be classified into the property development business and Mill Hill International School Thailand business, as detailed below: For the property development business, in 2025 and 2024, the Group recorded cost of sales of 1,219.03 million baht and 815.58 million baht, respectively, representing an increase of 403.45 million baht or 49.47% compared to the same period of the prior year. Gross profit amounted to 872.72

  `MDA_ORN_FY2025` · `p009` · SHA 2370a1d22e05
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 226 ลบ. เพิ่ม 61.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > operations. Overall, the Company reported gross profit of 868.54 million baht and 547.06 million baht in 2025 and 2024, respectively, representing an increase of 321.48 million baht or 58.77% compared to the same period of the prior year. In 2025, the Group’s gross profit margin was 41.20% of sales revenue, an increase of 1.05 percentage points from 40.15% in the same period of the prior year, primarily driven by higher contributions from low-rise housing projects.

  `MDA_ORN_FY2025` · `p010` · SHA b855b937d6f2
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 226 ลบ. เพิ่ม 61.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Distribution Costs In 2025, the company group incurred distribution costs of 362.33 million baht which is an increase of 75.95% from 205.93 million baht in the same period last year. The increase was mainly due to higher promotional and advertising expenses for new projects, as well as commission costs for sales agents of high-rise projects. Also, transfer expenses that varied in line with the increase in sales revenue.

  `MDA_ORN_FY2025` · `p011` · SHA 5bd1ef85184b
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_ORN_FY2025`

##### ESTAR — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท อีสเทอร์น สตาร์ เรียล เอสเตท จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ดำเนินธุรกิจหลักเกี่ยวกับการพัฒนาอสังหาริมทรัพย์เพื่อขาย หรือให้เช่า และธุรกิจสนามกอล์ฟ ในกรุงเทพมหานครและจังหวัดระยอง

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.3bn | 0.25 | +25.0% | 7.3x | 6.3% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 3 · NPAT 7 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 1.9bn → FY2025 THB 2.0bn · +139m · +7.4%

- RFO ปี 2568 อยู่ที่ 2,022 ลบ. เพิ่ม 7.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > This was primarily due to the rate of revenue growth exceeding the rate of increase in cost, as detailed below: 1.1 Revenue from sales of real estate increased by Baht 128.08 million, or 7% compared to the previous year. The principal reason was the transfer of ownership of new projects during the year, including both condominium and low-rise projects.

  `MDA_ESTAR_FY2025` · `p004` · SHA 89240dd713eb
  </details>
- RFO ปี 2568 อยู่ที่ 2,022 ลบ. เพิ่ม 7.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Selling and administrative expenses increased by Baht 3.84 million, or 0.97% compared to the previous year, which was lower than the rate of revenue growth. This was primarily due to prudent control of selling and administrative expenses in accordance with the approved budget.

  `MDA_ESTAR_FY2025` · `p008` · SHA da13509dc517
  </details>
- RFO ปี 2568 อยู่ที่ 2,022 ลบ. เพิ่ม 7.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 1.2 Cost of real estate sales increased by only Baht 24.78 million, or 2% compared to the previous year,

  `MDA_ESTAR_FY2025` · `p005` · SHA b53f1e32f3a7
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 34m → FY2025 THB 126m · +92m · +270.6%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 126 ลบ. เพิ่ม 270.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Finance costs increased by Baht 4.92 million, or 30 % compared to the previous year. This was mainly due to the completion and commencement of ownership transfers of condominium projects during the year, resulting in the recognition of higher interest expenses as finance costs.

  `MDA_ESTAR_FY2025` · `p010` · SHA 6fbb3f879152
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 126 ลบ. เพิ่ม 270.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > This was primarily due to the rate of revenue growth exceeding the rate of increase in cost, as detailed below: 1.1 Revenue from sales of real estate increased by Baht 128.08 million, or 7% compared to the previous year. The principal reason was the transfer of ownership of new projects during the year, including both condominium and low-rise projects.

  `MDA_ESTAR_FY2025` · `p004` · SHA 89240dd713eb
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 126 ลบ. เพิ่ม 270.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > mainly attributable to improved cost management efficiency.

  `MDA_ESTAR_FY2025` · `p006` · SHA e297dd1cd38f
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 126 ลบ. เพิ่ม 270.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the year ended December, 31 2025, Eastern Star Real Estate Public Company Limited and its subsidiaries (the Company) reported a net profit attributable to equity holders of the Company of Baht 126.40 million, which increased of Baht 92.30 million or 271% compared to the previous year. The company would like to clarify the main reasons for the change as follows:

  `MDA_ESTAR_FY2025` · `p002` · SHA 531657135e6f
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_ESTAR_FY2025`

##### BROCK — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท บ้านร็อคการ์เด้น จำกัด (มหาชน)** — อยู่ในภาวะฟื้นตัว; อัตราเติบโตมีความสำคัญรองลงมา

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์ประเภทบ้านจัดสรรเพื่อจำหน่าย ในกรุงเทพมหานคร ภูเก็ตและสมุทรปราการ

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.2bn | 1.16 | -9.4% | n.m. | -11.5% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 3 · NPAT 4 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 46m → FY2025 THB 85m · +40m · +86.4%

- RFO ปี 2568 อยู่ที่ 85.5 ลบ. เพิ่ม 86.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue For financial statement in Year 2025, the Company had the sales revenue of 85.45 Million Baht, an increased from the same period last year by approximately 39.61 Million Baht 86.41% As a result of the current situation, The projects currently underway by the company have attracted increasing interest from customers.

  `MDA_BROCK_FY2025` · `p007` · SHA 96c296ca36af
  </details>
- RFO ปี 2568 อยู่ที่ 85.5 ลบ. เพิ่ม 86.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Cost of Sales For financial statement in Year 2025, the cost of sales was recorded at 50.61 Million Baht, an increased from the same period last year by approximately 25.71 Million Baht 103.27% which the cost of sales increased by in the same direction with the sales revenue.

  `MDA_BROCK_FY2025` · `p008` · SHA 44d62df91dcb
  </details>
- RFO ปี 2568 อยู่ที่ 85.5 ลบ. เพิ่ม 86.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Profit (Loss) for the Period For financial statement in the Year 2025, the Company had the net profit of (9.81) Million Baht a decreased from the same period last year by approximately 5.95 Million Baht 37.5% Due to the current situation, The recognized increased revenue compared to the previous year and were able to better control the cost of goods sold and expenses. Please be informed accordingly.

  `MDA_BROCK_FY2025` · `p011` · SHA 2eea88b4190b
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 16m → FY2025 −THB 10m · +6m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -9.8 ลบ. จาก -15.8 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนวัตถุดิบและต้นทุนการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Profit (Loss) for the Period For financial statement in the Year 2025, the Company had the net profit of (9.81) Million Baht a decreased from the same period last year by approximately 5.95 Million Baht 37.5% Due to the current situation, The recognized increased revenue compared to the previous year and were able to better control the cost of goods sold and expenses. Please be informed accordingly.

  `MDA_BROCK_FY2025` · `p011` · SHA 2eea88b4190b
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -9.8 ลบ. จาก -15.8 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Cost of Sales For financial statement in Year 2025, the cost of sales was recorded at 50.61 Million Baht, an increased from the same period last year by approximately 25.71 Million Baht 103.27% which the cost of sales increased by in the same direction with the sales revenue.

  `MDA_BROCK_FY2025` · `p008` · SHA 44d62df91dcb
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -9.8 ลบ. จาก -15.8 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross Profit The Company’s gross profit margin for financial statement in Year 2025 was recorded at 34.84 Million Baht, an increased from the same period last year by approximately 13.90 Million Baht 66.35%.

  `MDA_BROCK_FY2025` · `p010` · SHA d45802a24294
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -9.8 ลบ. จาก -15.8 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > (170.04) Profit (Loss) for the Period (9,813.53) (15,765.16) (37.75)

  `MDA_BROCK_FY2025` · `p005` · SHA 3631b45efe33
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_BROCK_FY2025`

##### PROUD — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท พราว เรียล เอสเตท จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.1bn | 1.09 | +23.9% | 6.7x | 2.6% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 10 · NPAT 10 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 2

**RFO — เพราะอะไร** — FY2024 THB 2.2bn → FY2025 THB 6.4bn · +4.1bn · +186.6%

- RFO ปี 2568 อยู่ที่ 6,367 ลบ. เพิ่ม 186.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from sales of real estate For the 4th quarter of 2025, the Company reported revenue from real estate sales totaling THB 1,362.38 million, an increase of THB 1,112.31 million or 444.80% from the same period last year. This significant increase was primarily attributable to the transfer of condominium units at Nue District R9, VEHHA Hua Hin, and VI Ari, all of which have been completed and are ready for transfer. As of the end of the quarter, cumulative transfers accounted for 71%, 53%, and 80% of the total project value of each project, respectively. For 2025, the Company reported revenue from real estate sales totaling THB 6,367.17 million, an increase of THB 4,145.92 million or 186.

  `MDA_PROUD_FY2025` · `p005` · SHA 9d643f989de4
  </details>
- RFO ปี 2568 อยู่ที่ 6,367 ลบ. เพิ่ม 186.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Other income For the 4th quarter of 2025, the Company recorded other income of THB 31.52 million, an increase of THB 28.60 million or 979.45% from the same period last year. The increase was primarily attributable to forfeited booking deposits and down payments from customers in certain projects This was in connection with the management of the sales process and contract administration during the period of accelerated unit transfers. For 2025, the Company recorded other income of THB 39.63 million, a decrease of THB 6.94 million or 14.90% from the previous year. The decline was primarily attributable to the absence of certain non-recurring items recognized in 2024, including income from forf

  `MDA_PROUD_FY2025` · `p009` · SHA 056424952bfa
  </details>
- RFO ปี 2568 อยู่ที่ 6,367 ลบ. เพิ่ม 186.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ปริมาณขายและปริมาณการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Cost of real estate sold For the 4th quarter of 2025, the Company recorded cost of real estate sales amounting to THB 1,090.68 million, an increase of THB 894.53 million or 456.04% from the same period last year. The increase was primarily driven by a higher volume of unit transfers from completed projects. Consequently, the Company reported a gross profit of THB 271.70 million for the 4th quarter of 2025, representing a gross profit margin of 19.94%. For 2025, the Company recorded cost of real estate sales totaling THB 4,978.25 million, an increase of THB 3,221.26 million or 183.34% from the previous year, in line with the growth in revenue from the transfer of ownership of key projects thr

  `MDA_PROUD_FY2025` · `p008` · SHA 6ae406b465af
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 57m → FY2025 THB 168m · +111m · +196.4%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 168 ลบ. เพิ่ม 196.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ปริมาณขายและปริมาณการผลิต
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Cost of real estate sold For the 4th quarter of 2025, the Company recorded cost of real estate sales amounting to THB 1,090.68 million, an increase of THB 894.53 million or 456.04% from the same period last year. The increase was primarily driven by a higher volume of unit transfers from completed projects. Consequently, the Company reported a gross profit of THB 271.70 million for the 4th quarter of 2025, representing a gross profit margin of 19.94%. For 2025, the Company recorded cost of real estate sales totaling THB 4,978.25 million, an increase of THB 3,221.26 million or 183.34% from the previous year, in line with the growth in revenue from the transfer of ownership of key projects thr

  `MDA_PROUD_FY2025` · `p008` · SHA 6ae406b465af
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 168 ลบ. เพิ่ม 196.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Proud Real Estate Public Company Limited For 2025, the Company recorded a net profit of THB 167.83 million, an increase of THB 111.21 million or 196.41% from the previous year. The improvement was primarily attributable to the transfer of completed units from projects delivered in line with the business plan, together with effective management of cost of sales and operating expenses, resulting in enhanced profitability. Despite continued pressure on the real estate sector and overall purchasing power in 2025 amid economic challenges and elevated financing costs, the Company delivered sustained growth in operating performance. This was supported by its differentiated project development strat

  `MDA_PROUD_FY2025` · `p019` · SHA 38a0be4599e7
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 168 ลบ. เพิ่ม 196.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Finance income and finance cost For the 4th quarter of 2025, the Company recorded finance income of THB 1.27 million, a decrease of THB 0.57 million or 30.98% from the same period last year. The Company also recorded finance costs of THB 25.32 million, an increase of THB 16.17 million or 176.72% from the same period last year. The increase was primarily attributable to interest expenses recognized from projects that entered the transfer phase during the year. However, interest expenses began to moderate compared to the previous quarter following the continuous partial repayment of borrowings. As a result, the Company reported operating profit of THB 57.24 million for the 4th quarter of 2025,

  `MDA_PROUD_FY2025` · `p014` · SHA 1a7066ce8f0c
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 168 ลบ. เพิ่ม 196.4% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net profit for the year For the 4th quarter of 2025, the Company reported a net profit of THB 23.08 million, an increase of THB 58.14 million or 165.83% from the same period last year. The growth was primarily attributable to the transfer of completed units from projects completed in accordance with plan and progressively delivered during the quarter. Meanwhile, the Company’s cost structure and expenses remained aligned with transfer volumes, resulting in improved profitability compared to the same period last year.

  `MDA_PROUD_FY2025` · `p016` · SHA 402ea7241743
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- เอกสารที่มีอยู่ยังไม่ระบุรายการพิเศษหรือรายการต่ำกว่าการดำเนินงานอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Other income For the 4th quarter of 2025, the Company recorded other income of THB 31.52 million, an increase of THB 28.60 million or 979.45% from the same period last year. The increase was primarily attributable to forfeited booking deposits and down payments from customers in certain projects This was in connection with the management of the sales process and contract administration during the period of accelerated unit transfers. For 2025, the Company recorded other income of THB 39.63 million, a decrease of THB 6.94 million or 14.90% from the previous year. The decline was primarily attributable to the absence of certain non-recurring items recognized in 2024, including income from forf

  `MDA_PROUD_FY2025` · `p009` · SHA 056424952bfa
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > As of 31 December 2025, the Company had total assets of THB 7,490.65 million, representing a decrease of THB 3,165.90 million or 29.71% from the end of 2024. The decrease was primarily due to the following factors: • Real estate development costs decreased by THB 2,695.27 million or 29.80%, mainly due to ownership transfers of the Nue District R9, VEHHA Hua Hin, VI Ari and Nue Cross Khu Khot Station projects. • Other current assets decreased by THB 479.43 million or 67.19%, primarily due to the write-off of commission expenses, prepaid marketing expenses, and construction deposits related to projects that had already completed ownership transfers. • Cash and cash equivalents decreased by THB

  `MDA_PROUD_FY2025` · `p027` · SHA a2c89a2c5dd9
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_PROUD_FY2025`

##### PEACE — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท พีซแอนด์ลีฟวิ่ง จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์เพื่อขาย

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 726m | 1.44 | -25.4% | 36.4x | 1.9% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 9 · NPAT 8 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 854m → FY2025 THB 906m · +51m · +6.0%

- RFO ปี 2568 อยู่ที่ 906 ลบ. เพิ่ม 6.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Total assets as of 31 December 2025 increased by THB 282.96 million or 8.08% from that as of 31 December 2024. The main reasons are as follows: 1) Property development costs for sales increased by THB 230.06 million as a result of the development of five new projects. 2) Cash and cash equivalents increased by THB 41.74 million, resulting from net cash inflows of THB 188.13 million from financing activities, offset by net cash outflows of THB 132.84 million from operating activities and THB 13.55 million from investing activities. 3) Building and equipment increased by THB 5.02 million, resulting from the increase of furniture and office equipment of the new projects launched in 2025.

  `MDA_PEACE_FY2025` · `p024` · SHA 7395b90c738a
  </details>
- RFO ปี 2568 อยู่ที่ 906 ลบ. เพิ่ม 6.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Key Operating Revenue Revenue from sales of real estate for the year ended 31 December 2025 and 31 December 2024 was THB 905.58 million and THB 854.35 million, respectively. The revenue from sales of real estate according to the project are as follows:

  `MDA_PEACE_FY2025` · `p012` · SHA 4182ccd25ae9
  </details>
- RFO ปี 2568 อยู่ที่ 906 ลบ. เพิ่ม 6.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Total 55.69 91.37 224.49 96.15 123.77 80.36 17.28 25.34 69.31 92.91 28.91 905.58 6.15 10.09 24.79 10.62 13.67 8.87 1.91 2.80 7.65 10.26 3.19 100.00 5.60 54.46 118.36 106.82 193.55 190.25 149.92 35.39 0.66 6.37 13.85 12.50 22.65 22.27 17.55 4.15 854.35 100.00 Revenue from sales of real estate for the year ended 31 December 2025 increased by THB 51.23 million, or 6.00%, compared with the year ended 31 December 2024. The increase was primarily attributable to the transfer of ownership from five new projects launched in 2025, as follows: - CHER Vibhavadi Rangsit - CHER Pinklao - Wongwaen - CHER Sathorn - Suksawat - INNER PEACE Sathorn - ThaPhra - CHERENE Phahol - Watcharapol

  `MDA_PEACE_FY2025` · `p013` · SHA ac882f68cd1c
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 68m → FY2025 THB 17m · −50m · -74.5%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 17.2 ลบ. ลด 74.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Total assets as of 31 December 2025 increased by THB 282.96 million or 8.08% from that as of 31 December 2024. The main reasons are as follows: 1) Property development costs for sales increased by THB 230.06 million as a result of the development of five new projects. 2) Cash and cash equivalents increased by THB 41.74 million, resulting from net cash inflows of THB 188.13 million from financing activities, offset by net cash outflows of THB 132.84 million from operating activities and THB 13.55 million from investing activities. 3) Building and equipment increased by THB 5.02 million, resulting from the increase of furniture and office equipment of the new projects launched in 2025.

  `MDA_PEACE_FY2025` · `p024` · SHA 7395b90c738a
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 17.2 ลบ. ลด 74.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อุปสงค์และกำลังซื้อในประเทศ และ การแข่งขันและการส่งเสริมการขาย และ ยอดขายและการโอนที่ดินนิคมอุตสาหกรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Profit Net profit for the year period ended 31 December 2025 and 31 December 2024 was THB 17.20 million and THB 67.57 million, representing net profit margins of 1.90 % and 7.67%, respectively. Net profit for the year ended 31 December 2025 declined by THB 50.37 million, or 74.55%, from the year ended 31 December 2024, mainly attributable to intense market competition and the economic slowdown. Furthermore, profit from the transfer of rights and obligations under land sale and purchase agreements recognized as other revenue in 2024 decreased. Meanwhile, a portion of the Company's expenses remained fixed in nature.

  `MDA_PEACE_FY2025` · `p019` · SHA bde76c46f886
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 17.2 ลบ. ลด 74.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อุปสงค์และกำลังซื้อในประเทศ และ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross profit Gross profit for the year ended 31 December 2025 and 31 December 2024 was THB 272.07 million and THB 278.23 million accounted for the gross profit margin of 30.04% and 32.57%, respectively. Gross profit for the year ended 31 December 2025 decreased by 6.16 million Baht, or 2.21%, compared with the year ended 31 December 2024, reflecting intensified market competition and the economic slowdown.

  `MDA_PEACE_FY2025` · `p014` · SHA 196b73c9124d
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 17.2 ลบ. ลด 74.5% YoY; MD&A ระบุว่า แขวงคลองตันเหนือ เขตวัฒนา กรุงเทพมหานคร 10110 02 392 1066 / www.peaceandliving.co.th Shareholders' equity as of 31 December 2025 decreased by THB 13.04 million or 0.58% from that as of 31 December 2024 mainly due to dividend payment from the operating results of the year 2024 and the decline in net profit, as previously mentioned.
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > แขวงคลองตันเหนือ เขตวัฒนา กรุงเทพมหานคร 10110 02 392 1066 / www.peaceandliving.co.th Shareholders' equity as of 31 December 2025 decreased by THB 13.04 million or 0.58% from that as of 31 December 2024 mainly due to dividend payment from the operating results of the year 2024 and the decline in net profit, as previously mentioned.

  `MDA_PEACE_FY2025` · `p028` · SHA e9360c3dc7fd
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_PEACE_FY2025`

##### NCH — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เอ็น. ซี. เฮ้าส์ซิ่ง จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์เพื่อการค้า ได้แก่ จัดสรรที่ดินและปลูกบ้านสำเร็จรูปและคอนโดมิเนียม งานก่อสร้าง การบริการและเช่าภายในสโมสรหมู่บ้าน เป็นต้น

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 573m | 0.46 | +9.5% | n.m. | -11.6% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 10 · NPAT 20 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 1.3bn → FY2025 THB 1.1bn · −151m · -12.0%

- RFO ปี 2568 อยู่ที่ 1,102 ลบ. ลด 12.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Total Revenues For the three-month period ended December 31, 2025, the Company and its subsidiaries reported total operating revenue of THB 277.94 million, representing an increase of THB 20.93 million, or 8.14% YoY, compared to 4Q/2024. The growth was primarily driven by higher revenue from sales, which increased by THB 18.72 million, or 7.89% YoY. In addition, rental and service income particularly from NC Regen Sport & Wellness Center and the rehabilitation and elderly care service business-continued to expand, rising by THB 2.97 million, or 17.75% YoY compared to 4Q/2024.

  `MDA_NCH_FY2025` · `p003` · SHA e16a17e50d4e
  </details>
- RFO ปี 2568 อยู่ที่ 1,102 ลบ. ลด 12.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the full-year period ended December 31, 2025, The Company and its subsidiaries reported cost of sales of THB 772.28 million, representing a decrease of THB 25.46 million, or 3.19%, compared to THB 7 9 7 .74 million in the previous year. The reduction in cost of sales was in line with the decrease in revenue from property sales. However, the decline was not solely attributable to lower transfer volumes, but also reflected the Company’s systematic cost structure management amid an economic environment characterized by high interest rates and inflationary pressures, which continued to impact construction material prices and overall project development costs. The Company adjusted its project

  `MDA_NCH_FY2025` · `p014` · SHA 3f7eb73584f7
  </details>
- RFO ปี 2568 อยู่ที่ 1,102 ลบ. ลด 12.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the full-year period ended December 31, 2025, The Company and its subsidiaries reported revenue from sales of THB 1,031.44 million, representing a decrease of THB 157.27 million or 13.23% from THB 1 ,1 8 8 .7 1 million in the previous year. The decline in revenue in 2025 was in line with the overall direction of the real estate market, which remained in a structural adjustment phase following a recovery that did not materialize as previously anticipated since late 2024. Market conditions continued to reflect pressure from affordability constraints and tightened lending standards, particularly in the low to mid- priced segments, which constitute the primary customer base for most develope

  `MDA_NCH_FY2025` · `p009` · SHA f9bc15e2cd74
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 34m → FY2025 −THB 128m · −94m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -128 ลบ. จาก -33.7 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the full-year period ended December 31, 2025, The Company and its subsidiaries reported cost of sales of THB 772.28 million, representing a decrease of THB 25.46 million, or 3.19%, compared to THB 7 9 7 .74 million in the previous year. The reduction in cost of sales was in line with the decrease in revenue from property sales. However, the decline was not solely attributable to lower transfer volumes, but also reflected the Company’s systematic cost structure management amid an economic environment characterized by high interest rates and inflationary pressures, which continued to impact construction material prices and overall project development costs. The Company adjusted its project

  `MDA_NCH_FY2025` · `p014` · SHA 3f7eb73584f7
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -128 ลบ. จาก -33.7 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนวัตถุดิบและต้นทุนการผลิต และ ราคาขายและส่วนผสมผลิตภัณฑ์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > construction side, the Company enhanced operational processes from the design phase and budget planning to quality control, with the objective of improving cost accuracy and efficiency. Despite ongoing pressures from labor costs and certain construction materials, close monitoring and disciplined cost management enabled the Company to maintain competitive unit cost levels. In terms of procurement, the Company strengthened supplier relationships and implemented structured purchasing plans with clearly defined pricing frameworks. This strategy mitigated risks associated with raw material price volatility and

  `MDA_NCH_FY2025` · `p015` · SHA 9ad1c306c84f
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -128 ลบ. จาก -33.7 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ กำลังการผลิตและเครื่องจักรใหม่ และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the full-year period ended December 31, 2025, The Company and its subsidiaries reported rental and service costs of THB 67.58 million, representing an increase of THB 0.57 million, or 0.85%, compared to the same period last year. The increase was in line with higher revenue from the rental and service business, particularly from the rehabilitation and elderly care services, reflecting the expansion in business activities. The higher costs corresponded with increased service capacity and resource readiness to accommodate growing demand. The Company adjusted its cost structure to align with the level of operations, emphasizing appropriate resource management, including workforce allocation

  `MDA_NCH_FY2025` · `p018` · SHA ee8774255570
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -128 ลบ. จาก -33.7 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the full-year period ended December 31, 2025, The Company and its subsidiaries reported a net loss of THB 1 2 8.00 million in 2025, representing a decrease of THB 9 4.33 million, or 2 80.16%, compared to net profit of THB 33.67 million in 2024. In 2025, the Company’s operating results reflected pressures in the real estate market amid a still-fragile economic environment. Constraints in consumer purchasing power, interest rate trends, and the risk management approach of financial institutions resulted in longer decision-making and property transfer processes than usual, leading to a decline in revenue. The Company recognizes this context and views the current period as one of reassessmen

  `MDA_NCH_FY2025` · `p032` · SHA ca70e3f78e7d
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_NCH_FY2025`

##### SAMCO — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท สัมมากร จำกัด (มหาชน)** — อยู่ในภาวะฟื้นตัว; อัตราเติบโตมีความสำคัญรองลงมา

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — เพื่อประกอบธุรกิจพัฒนาอสังหาริมทรัพย์ และพัฒนาที่ดินในรูปแบบที่มีรายได้จากการให้เช่า

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 571m | 0.89 | +23.6% | 4.6x | -1.3% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 2 · NPAT 2 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 1.5bn → FY2025 THB 1.5bn · −31m · -2.0%

- RFO ปี 2568 อยู่ที่ 1,487 ลบ. ลด 2.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อุปสงค์และกำลังซื้อในประเทศ และ การซื้อกิจการและการรวมงบการเงิน และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Consolidated financial statements Results of Operations for the Year 2025, The Company reported net loss of THB 19.46 million, representing a decreased loss of THB 31.31 million or 61.67% compared to the 2024 year. Total revenue was THB 1,561.62 million compared to the previous year, which recorded total revenue of THB 1,582.64 million a decrease of THB 21.02 million or 1.33% with revenue from real estate sales declining by THB 20.98 million. which was primarily attributable to real estate sales, resulting from a slowdown in the real estate market including the continued sluggish recovery of the domestic economy. Revenue from service and rental operations decreased by THB 11.23 million, whil

  `MDA_SAMCO_FY2025` · `p003` · SHA 278b8e578ce3
  </details>
- RFO ปี 2568 อยู่ที่ 1,487 ลบ. ลด 2.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายขายและบริหาร และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > THB 4.30 million. Meanwhile, the cost of services and rental income decreased by THB 2.09 million. Selling and administrative expenses in 2025 decreased by THB 49.01 million, or 12.26%, Compared to the previous year, which had selling and administrative expenses amounting to THB 399.69 million. In 2025, had selling expenses amounted to THB 133.48 million, down THB 9.79 million compared to 2024, which varied in line with the decline in sales. Meanwhile, administrative expenses decreased by THB 39.22 million compared to 2024, as in 2024 a subsidiary recognized an impairment loss on investment amounting to THB 20.43 million. The Company’s total assets stood at THB 5,392.64 million, a decrease o

  `MDA_SAMCO_FY2025` · `p004` · SHA bc8c0e250d84
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 51m → FY2025 −THB 19m · +31m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -19.5 ลบ. จาก -50.8 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ อุปสงค์และกำลังซื้อในประเทศ และ การซื้อกิจการและการรวมงบการเงิน และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Consolidated financial statements Results of Operations for the Year 2025, The Company reported net loss of THB 19.46 million, representing a decreased loss of THB 31.31 million or 61.67% compared to the 2024 year. Total revenue was THB 1,561.62 million compared to the previous year, which recorded total revenue of THB 1,582.64 million a decrease of THB 21.02 million or 1.33% with revenue from real estate sales declining by THB 20.98 million. which was primarily attributable to real estate sales, resulting from a slowdown in the real estate market including the continued sluggish recovery of the domestic economy. Revenue from service and rental operations decreased by THB 11.23 million, whil

  `MDA_SAMCO_FY2025` · `p003` · SHA 278b8e578ce3
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -19.5 ลบ. จาก -50.8 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายขายและบริหาร และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > THB 4.30 million. Meanwhile, the cost of services and rental income decreased by THB 2.09 million. Selling and administrative expenses in 2025 decreased by THB 49.01 million, or 12.26%, Compared to the previous year, which had selling and administrative expenses amounting to THB 399.69 million. In 2025, had selling expenses amounted to THB 133.48 million, down THB 9.79 million compared to 2024, which varied in line with the decline in sales. Meanwhile, administrative expenses decreased by THB 39.22 million compared to 2024, as in 2024 a subsidiary recognized an impairment loss on investment amounting to THB 20.43 million. The Company’s total assets stood at THB 5,392.64 million, a decrease o

  `MDA_SAMCO_FY2025` · `p004` · SHA bc8c0e250d84
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายขายและบริหาร และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > THB 4.30 million. Meanwhile, the cost of services and rental income decreased by THB 2.09 million. Selling and administrative expenses in 2025 decreased by THB 49.01 million, or 12.26%, Compared to the previous year, which had selling and administrative expenses amounting to THB 399.69 million. In 2025, had selling expenses amounted to THB 133.48 million, down THB 9.79 million compared to 2024, which varied in line with the decline in sales. Meanwhile, administrative expenses decreased by THB 39.22 million compared to 2024, as in 2024 a subsidiary recognized an impairment loss on investment amounting to THB 20.43 million. The Company’s total assets stood at THB 5,392.64 million, a decrease o

  `MDA_SAMCO_FY2025` · `p004` · SHA bc8c0e250d84
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_SAMCO_FY2025`

##### RML — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ไรมอน แลนด์ จำกัด (มหาชน)** — อยู่ในภาวะฟื้นตัว; อัตราเติบโตมีความสำคัญรองลงมา

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์ มุ่งเน้นการพัฒนาโครงการคอนโดมิเนียมสำหรับลูกค้าระดับกลางถึงระดับบน โครงการวิลล่าเฉพาะกลุ่มลูกค้า ทั้งในเขตกรุงเทพมหานครและแหล่งที่พักตากอากาศ

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 522m | 0.09 | -30.8% | n.m. | -704.6% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 5 · NPAT 7 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 147m → FY2025 THB 130m · −17m · -11.7%

- RFO ปี 2568 อยู่ที่ 130 ลบ. ลด 11.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Summary of Comprehensive Income Statement Presales and Backlog: During Q4 2025, the Company recorded presales of 71.2 million Baht, a decrease from 158.8 million Baht in the same period last year. For the full year 2025, presales totaled 231.0 million Baht, down from 336.4 million Baht in 2024. As of December 31, 2025, the total backlog value stood at 142.6 million Baht. Revenue from Sales, Rentals, and Services: In Q4 2025 and for the full year 2025, the Company recorded revenue from sales, rentals, and services at 19.7 million Baht and 129.6 million Baht, respectively.

  `MDA_RML_FY2025` · `p030` · SHA 8d2e3448ee48
  </details>
- RFO ปี 2568 อยู่ที่ 130 ลบ. ลด 11.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ภาระหนี้และโครงสร้างเงินทุน และ ยอดขายและการโอนโครงการที่อยู่อาศัย และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Summary of Key Operating Results for Q4 and FY 2025 The Company's total Backlog was valued at 142.6 million Baht as of December 31, 2025. • Presales for the year 2025 stood at 231.0 million Baht. • Total revenue for the year 2025 was 329.5 million Baht, consisting of revenue from sales, rentals, • and services amounting to 129.6 million Baht. As of December 31, 2025, the Company had total assets of 6,465.1 million Baht and total • liabilities of 4,377.4 million Baht. The Interest-bearing Debt to Equity ratio was 1.54 times as of December 31, 2025, an increase • from 1.14 times at the end of 2024.

  `MDA_RML_FY2025` · `p024` · SHA 82b3c0569c28
  </details>
- RFO ปี 2568 อยู่ที่ 130 ลบ. ลด 11.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ค่าใช้จ่ายขายและบริหาร และ ยอดขายและการโอนโครงการที่อยู่อาศัย และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Project Management Fee Revenue: This revenue derives from fees charged to joint venture companies for construction management and juristic person administration of various residential projects. In Q4 2025 and for the full year 2025, the Company reported revenue of 8.8 million Baht and 35.6 million Baht, respectively. Cost of Sales, Rentals, and Services: In Q4 2025, the cost of real estate sales was 19.4 million Baht. For the full year 2025, the cost of real estate sales was 119.5 million Baht. Selling, General and Administrative Expenses (SG&A): Selling expenses include advertising, marketing, commissions, and expenses related to unit transfers, while administrative expenses are mostly fixe

  `MDA_RML_FY2025` · `p031` · SHA 6a9dd059a0df
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 1.2bn → FY2025 −THB 913m · +300m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -913 ลบ. จาก -1,213 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > from 40.4 million Baht, and administrative expenses also declined compared to the same period last year. Net Finance Costs: Currently, the Company raises funds via debentures and financial institution loans. Most of the finance costs stem from the interest on these instruments. In Q4 2025, net finance costs were 78.9 million Baht, a decrease of 19.1 million Baht from the same period last year. For the full year 2025, net finance costs amounted to 373.2 million Baht, an increase of 29.1 million Baht year- over-year. Net Profit (Loss): In Q4 2025, the Company reported a net loss of 263.9 million Baht. For the full year 2025, the net loss was 930.1 million Baht, equivalent to a net loss of 0.16

  `MDA_RML_FY2025` · `p032` · SHA ae25d4ba9fec
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -913 ลบ. จาก -1,213 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ต้นทุนทางการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net gain (loss) on disposal and write-off of buildings and equipment, and investment properties (0.5) (0.7) - - (0.5) N/A 11.0 3.4 - - 11.0 N/A Net gain (loss) on exchange rate (0.4) (0.5) (0.1) (0.1) (0.3) 337.3 0.5 0.1 (16.9) (5.0) 17.3 (102.8) Finance costs (78.9) (110.8) (97.9) ( 61.7) 19.1 (19.5) (373.2) (113.3) (344.1) (102.3) (29.1) 8.5 Total expenses (234.2) (328.9) (584.3) (367.9) 350.1 (59.9) (934.0) (283.5) (1,420.8) (422.3) 486.8 (34.3) Loss from operating activities (163.0) (228.9) (425.5) (267.9) 262.5 (61.7) (604.5) (183.5) (1,084.4) (322.3) 479.9 (44.3) Share of loss from investments in joint ventures (99.8) (140.1) (83.0) ( 52.3) (16.8) 20.2 (314.7) ( 95.5) (131.3) ( 39.0) (

  `MDA_RML_FY2025` · `p028` · SHA d9567f46d7fb
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -913 ลบ. จาก -1,213 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ต้นทุนทางการเงิน และ ค่าใช้จ่ายภาษี
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Cash Flow Movement in 2025 In 2025, the Company used net cash in operating activities amounting to 85.4 million Baht, which included payments for finance costs of 200.3 million Baht and income tax of 30.1 million Baht. Therefore, the Company recorded net cash used in operating activities of 85.4 million Baht. Key changes in operating activities included: 1) Loss before tax of 919.3 million Baht, 2) Share of loss from investments in joint ventures of 314.7 million Baht, and 3) Finance costs of 308.3 million Baht. For investing activities, the Company used net cash of 22.0 million Baht. Key transactions included: 1) Cash received from the sale of investment properties and equipment of 162.3 mi

  `MDA_RML_FY2025` · `p038` · SHA 4a88c7d32ea2
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -913 ลบ. จาก -1,213 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Total 1,129.5 To support sustainable growth and maintain financial discipline according to the business plan, the Company continues to drive its business through a Joint Venture strategy alongside an "Asset Light" business model. This involves collaborating with landowners and leading business partners for project development. This investment model not only significantly increases efficiency in managing land costs and reduces financial cost burdens, but it also results in a stronger and more stable performance structure for the Company by recognizing the Share of Profit from Joint Ventures, rather than bearing the entire investment risk alone. Building on the success of this model, the Compa

  `MDA_RML_FY2025` · `p021` · SHA 50a47e50eafc
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ต้นทุนทางการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net gain (loss) on disposal and write-off of buildings and equipment, and investment properties (0.5) (0.7) - - (0.5) N/A 11.0 3.4 - - 11.0 N/A Net gain (loss) on exchange rate (0.4) (0.5) (0.1) (0.1) (0.3) 337.3 0.5 0.1 (16.9) (5.0) 17.3 (102.8) Finance costs (78.9) (110.8) (97.9) ( 61.7) 19.1 (19.5) (373.2) (113.3) (344.1) (102.3) (29.1) 8.5 Total expenses (234.2) (328.9) (584.3) (367.9) 350.1 (59.9) (934.0) (283.5) (1,420.8) (422.3) 486.8 (34.3) Loss from operating activities (163.0) (228.9) (425.5) (267.9) 262.5 (61.7) (604.5) (183.5) (1,084.4) (322.3) 479.9 (44.3) Share of loss from investments in joint ventures (99.8) (140.1) (83.0) ( 52.3) (16.8) 20.2 (314.7) ( 95.5) (131.3) ( 39.0) (

  `MDA_RML_FY2025` · `p028` · SHA d9567f46d7fb
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_RML_FY2025`

##### PF — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท พร็อพเพอร์ตี้ เพอร์เฟค จำกัด (มหาชน)** — ข้อมูลเทียบเคียงจำกัด: ไม่ควรสรุปเหตุเชื่อมโยงระหว่างรายได้กับกำไร

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัทและบริษัทย่อยดำเนินการพัฒนาโครงการบ้านเดี่ยว โครงการทาวน์เฮ้าส์และบ้านแฝด และโครงการคอนโดมิเนียมในรูปแบบที่หลากหลายในเขตกรุงเทพมหานครและปริมณฑลเป็นหลัก โดยเน้นทำเลที่ตั้งที่มีศักยภาพสูง ใกล้แนวรถไฟฟ้า

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 501m | 0.05 | -16.7% | n.m. | — |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 2 · NPAT 5 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 8.9bn → FY2025 — · —

- RFO ปี 2568 อยู่ที่ ไม่ปรากฏตัวเลขที่เปรียบเทียบได้ ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2. Hotel business: 2.1 The revenues from hotel operations were Baht 1,985.9 million, decreased from the corresponding period of year 2024 by Baht 543.8 million or 21.5 %. Due to sale of a hotel in fourth quarter of year 2024 2.2 The gross profit of Baht 961.5 million, decreased from the corresponding period of year 2024 by Bath 350.5 Million or 26.7% 2.3 The gross profit margin was 48.4% decreased from 51.9% of the corresponding period of year 2024. 3. Revenue from rental and service business amounted to Baht 483.3 million, decreased from the corresponding period of year 2024 by Baht 19.0 million or 3.8% 4. Other income amounted to Baht 319.6 million, increased from the corresponding period

  `MDA_PF_FY2025` · `p004` · SHA ff542fe7f233
  </details>
- RFO ปี 2568 อยู่ที่ ไม่ปรากฏตัวเลขที่เปรียบเทียบได้ ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ การแข่งขันและการส่งเสริมการขาย และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 1. Real estate development business 1.1 Revenue from real estate development business were Baht 2,284.5 million, decreased from the corresponding period of year 2024 by Baht 3,600.3 million or 61.2%. The changes were from the economic condition and the competition in the residential property market. 1.2 The gross profit was Baht 529.2 million, decreased from the corresponding period of year 2024 by Baht 1,171.8 million or 68.9% 1.3 The gross profit margin was 23.2% decreased from 28.9% of the corresponding period of year 2024.

  `MDA_PF_FY2025` · `p003` · SHA ba2acbf5c33e
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 1.0bn → FY2025 — · —

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ ไม่ปรากฏตัวเลขที่เปรียบเทียบได้ ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2. Hotel business: 2.1 The revenues from hotel operations were Baht 1,985.9 million, decreased from the corresponding period of year 2024 by Baht 543.8 million or 21.5 %. Due to sale of a hotel in fourth quarter of year 2024 2.2 The gross profit of Baht 961.5 million, decreased from the corresponding period of year 2024 by Bath 350.5 Million or 26.7% 2.3 The gross profit margin was 48.4% decreased from 51.9% of the corresponding period of year 2024. 3. Revenue from rental and service business amounted to Baht 483.3 million, decreased from the corresponding period of year 2024 by Baht 19.0 million or 3.8% 4. Other income amounted to Baht 319.6 million, increased from the corresponding period

  `MDA_PF_FY2025` · `p004` · SHA ff542fe7f233
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ ไม่ปรากฏตัวเลขที่เปรียบเทียบได้ ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง และ การแข่งขันและการส่งเสริมการขาย และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 1. Real estate development business 1.1 Revenue from real estate development business were Baht 2,284.5 million, decreased from the corresponding period of year 2024 by Baht 3,600.3 million or 61.2%. The changes were from the economic condition and the competition in the residential property market. 1.2 The gross profit was Baht 529.2 million, decreased from the corresponding period of year 2024 by Baht 1,171.8 million or 68.9% 1.3 The gross profit margin was 23.2% decreased from 28.9% of the corresponding period of year 2024.

  `MDA_PF_FY2025` · `p003` · SHA ba2acbf5c33e
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ ไม่ปรากฏตัวเลขที่เปรียบเทียบได้ ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > According to the Company' s statement of comprehensive income for the year 2025, the Company and its subsidiaries recorded net loss of Baht 3,677.0 million (net loss of owners of the parent company presented loss of Baht 2,813. 3 million) . Comparing with the corresponding period of the year 2024, the increasing loss of Baht 2,264.3 million (net loss of owners of the parent company presented increasing loss of Baht 1,803.3 million due to the followings:

  `MDA_PF_FY2025` · `p002` · SHA 2db014203a57
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ ไม่ปรากฏตัวเลขที่เปรียบเทียบได้ ยังคำนวณอัตราเปลี่ยนแปลงไม่ได้; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน และ ค่าใช้จ่ายภาษี
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 6. Finance costs were Baht 1,934.0 million, increased from the corresponding period of year 2024 by Baht 125.3 million or 6.9% 7. The income tax of the group company was Baht 470.9 million, increased by Baht 580.1 million from the same period of the year 2024 caused by recognition of deferred income tax assets of the subsidiaries.

  `MDA_PF_FY2025` · `p005` · SHA 6f789b7140bc
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_PF_FY2025`

##### KUN — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท วิลล่า คุณาลัย จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์เพื่อขาย

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 492m | 0.60 | -27.7% | 633.5x | 0.7% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 6 · NPAT 10 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 663m → FY2025 THB 514m · −149m · -22.5%

- RFO ปี 2568 อยู่ที่ 514 ลบ. ลด 22.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อุปสงค์และกำลังซื้อในประเทศ และ การแข่งขันและการส่งเสริมการขาย และ ยอดขายและการโอนที่ดินนิคมอุตสาหกรรม และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The main reasons were:  Economic slowdown in the early part of the year  Intense market competition Revenue from land sales amounted to THB 76.86 million, significantly increasing from THB 1.68 million in the previous year. This reflects the Company’s strategy to manage assets in order to enhance liquidity. In 2025, revenue from single detached houses totaled THB 366.49 million, representing 83.83% of total real estate sales revenue. The Company focuses on single detached housing projects, particularly Navara Rama 2 and Navara Rangsit, priced at approximately THB 5 million, which target customers with stronger mortgage approval potential. This strategic focus resulted in a significant incr

  `MDA_KUN_FY2025` · `p009` · SHA 118ec9836061
  </details>
- RFO ปี 2568 อยู่ที่ 514 ลบ. ลด 22.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from sales of real estates 437.15 100.00% 661.41 100.00% (224.26) -33.91% Revenue from sales of land 76.86 17.58% 1.68 0.25% 75.18 4474.83% Cost of sales of real estate (348.22) -79.66% (505.42) -76.42% 157.20 -31.10% Cost of sales of land (31.22) -7.14% (0.47) -0.07% (30.75) 6543.25%

  `MDA_KUN_FY2025` · `p003` · SHA 7274149ff3a6
  </details>
- RFO ปี 2568 อยู่ที่ 514 ลบ. ลด 22.5% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from sales of real estates In 2025, the Company recorded revenue from real estate sales of THB 437.15 million, decreasing from THB 661.41 million in 2024.

  `MDA_KUN_FY2025` · `p008` · SHA 796a9b01d471
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 30m → FY2025 THB 4m · −26m · -87.9%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 3.6 ลบ. ลด 87.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from sales of real estates 437.15 100.00% 661.41 100.00% (224.26) -33.91% Revenue from sales of land 76.86 17.58% 1.68 0.25% 75.18 4474.83% Cost of sales of real estate (348.22) -79.66% (505.42) -76.42% 157.20 -31.10% Cost of sales of land (31.22) -7.14% (0.47) -0.07% (30.75) 6543.25%

  `MDA_KUN_FY2025` · `p003` · SHA 7274149ff3a6
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 3.6 ลบ. ลด 87.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Gross Profit Total gross profit in 2025 was THB 134.57 million, representing a gross profit margin of approximately 26.18%, compared to THB 157.20 million in 2024.

  `MDA_KUN_FY2025` · `p010` · SHA 3838d0a4869e
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 3.6 ลบ. ลด 87.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Finance Costs Finance costs increased significantly from THB 7.36 million in 2024 to THB 18.29 million in 2025, representing an increase of 148.57%.

  `MDA_KUN_FY2025` · `p014` · SHA 5377ebf53e95
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 3.6 ลบ. ลด 87.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การแข่งขันและการส่งเสริมการขาย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The decrease in gross profit was mainly attributable to:  Lower real estate sales revenue  Increased competitive pressure, leading to higher promotional expenses and sales incentives

  `MDA_KUN_FY2025` · `p011` · SHA 7ef9dd53b468
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_KUN_FY2025`

##### CMC — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เจ้าพระยามหานคร จำกัด (มหาชน)** — อยู่ในภาวะฟื้นตัว; อัตราเติบโตมีความสำคัญรองลงมา

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — CMC ประกอบธุรกิจ 3 กลุ่มดังนี้ 1. พัฒนาอสังหาริมทรัพย์เพื่อที่อยู่อาศัย ประกอบด้วยคอนโดมิเนียม ทาวน์เฮ้าส์ ทาวน์โฮม และบ้านเดี่ยว โดยเน้นพัฒนาโครงการประเภทคอนโดมิเนียมเป็นหลัก 2. พัฒนาอสังหาริมทรัพย์เพื่อใหเ้ช่า 3. รับเหมาก่อสร้างและโรงงานผลิตเฟอร์นิเจอร์และผนัง

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 485m | 0.44 | -10.2% | 7.0x | 1.6% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 11 · NPAT 13 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 4

**RFO — เพราะอะไร** — FY2024 THB 2.0bn → FY2025 THB 1.2bn · −768m · -39.2%

- RFO ปี 2568 อยู่ที่ 1,190 ลบ. ลด 39.2% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the year 2025, the Company generated total revenue of THB 1,866.8 million, a decrease of THB (124.2) million, or (6.2%), from THB 1,990.9 million in the same period of 2024. Revenue mainly came from real estate development for sale. Details by business segment are as follows:

  `MDA_CMC_FY2025` · `p012` · SHA ebf8d6cdfd94
  </details>
- RFO ปี 2568 อยู่ที่ 1,190 ลบ. ลด 39.2% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย และ สินเชื่อที่อยู่อาศัยที่เข้มงวดและหนี้ครัวเรือน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > million or (45.2%). The overall decline in revenue was consistent with the sluggish real estate market, particularly in the mid-to-high-end condominium segment, which remained affected by limited purchasing power and strict mortgage lending policies. However, the increase in service-related income partially offset the impact of lower property sales, reflecting the Company’s efforts to build a recurring income portfolio.

  `MDA_CMC_FY2025` · `p017` · SHA 0e1a9ed4971b
  </details>
- RFO ปี 2568 อยู่ที่ 1,190 ลบ. ลด 39.2% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Although the Company reported a net profit in its financial statements, its core revenue, namely revenue from the sale of real estate declined significantly by THB 783.9 million, or 47.2%. This decrease was in contrast to finance costs, which increased by 27.8%, equivalent to THB 71.7 million.

  `MDA_CMC_FY2025` · `p027` · SHA 781c7921780b
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 214m → FY2025 THB 18m · +232m

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 18.5 ลบ. จากขาดทุน -214 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ต้นทุนทางการเงิน และ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้ และ ภาระหนี้และโครงสร้างเงินทุน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Finance costs for the year 2025 amounted THB 329.8 million, increase THB 71.7 million in the same period of 2024 or 27.8%. The increase was primarily due to higher interest expenses from working capital loans and financing for new project developments. The Company is actively managing its financial costs through debt restructuring initiatives and optimizing the proportion of low-cost borrowings to improve long-term financial efficiency.

  `MDA_CMC_FY2025` · `p024` · SHA 0ec126f196c2
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 18.5 ลบ. จากขาดทุน -214 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ อัตรากำไรลดลง และ การแข่งขันและการส่งเสริมการขาย และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The reduction in gross profit margin was mainly due to a higher proportion of lower-margin projects, and the price competition in the mid- to low-end condominium market. Moreover, the wellness business— currently in its initial investment phase—has yet to contribute meaningful profit during the period.

  `MDA_CMC_FY2025` · `p019` · SHA 97c4bede66c7
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 18.5 ลบ. จากขาดทุน -214 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรลดลง
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The Company reported a gross profit of THB 262.0 million, a decrease of THB (273.7 ) million, or (51.1%), compared to the same period of 2024. The gross profit margin declined from 27.4% in 2024 to 22.0% in 2025.

  `MDA_CMC_FY2025` · `p018` · SHA dfd053368525
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นกำไร 18.5 ลบ. จากขาดทุน -214 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > operating expenses. Total liabilities stood at THB 4,806.9 million, a decrease of THB (119.7) million, or (2.4%), mainly from repayment of project-related loans. Total shareholders’ equity amounted to THB 2,197.1 million, an increase of THB 14.3 million, or 0.7%, due to the net loss recognized during the period.

  `MDA_CMC_FY2025` · `p032` · SHA 8e41bef0a9e2
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Other income for the year 2025 amounted to THB 676.4 million, a significant increase from THB 32.5 million in 2024, an increase of THB 643.9 million. The increase was primarily attributable to a change in accounting policy for the measurement of investment properties from the book value model to the fair value

  `MDA_CMC_FY2025` · `p020` · SHA 3a446bad8f76
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > However, in 2025, the Company recorded an impairment provision of THB 89.51 million for property under development and land held for development that had been reclassified as investment properties. Excluding the impact of such impairment provision, the Company’s expenses for 2025 would amount to THB 320.4 million, representing 17.2% of total revenue. This reflects a decrease of THB 199.0 million, or 38.3%, compared to the previous year.

  `MDA_CMC_FY2025` · `p023` · SHA 83e10a28460d
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_CMC_FY2025`

##### MJD — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เมเจอร์ ดีเวลลอปเม้นท์ จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์เพื่อขายและธุรกิจโรงแรม โดยเน้นโครงการอาคารที่อยู่อาศัยประเภทอาคารสูง หรือ คอนโดมิเนียม ในระดับไฮเอนด์ ที่มีความหรูหราในการอยู่อาศัย

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 293m | 0.34 | 0.0% | n.m. | -106.3% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 2 · NPAT 4 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 4

**RFO — เพราะอะไร** — FY2024 THB 2.4bn → FY2025 THB 2.0bn · −378m · -16.0%

- RFO ปี 2568 อยู่ที่ 1,984 ลบ. ลด 16.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > DEVELOPMENT 1. Total revenue for the year 2025 amounted to THB 2,201.46 million, representing a decrease of THB 314.79 million or 12.51% compared to 2024. The decline was primarily attributable to the following: • Sales revenue in 2025 amounted to THB 1,259.58 million, compared to THB 1,668.97 million in 2024, representing a decrease of THB 409.39 million or 24.53%. The decline was primarily due to lower revenue recognition from ownership transfers in low-rise projects, including Malton Gates Krungthep Kreetha, Metris Pattanakarn-Ekkamai, and condominium projects that were progressively recognized and completed in

  `MDA_MJD_FY2025` · `p009` · SHA 90a7da55523e
  </details>
- RFO ปี 2568 อยู่ที่ 1,984 ลบ. ลด 16.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2024. The Company commenced ownership transfers and began recognizing revenue from Metris District Ladprao in October 2025. Revenues from hotel operations for 2025 amounted to THB 206.56 million, compared to THB 290.86 million in 2024, representing a decrease of THB 84.30 million or 28.98%

  `MDA_MJD_FY2025` · `p010` · SHA 84c0065cb1a7
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 299m → FY2025 −THB 2.1bn · −1.8bn

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -2,110 ลบ. จาก -299 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Company's review and adjustment of property values based on updated appraisals to reflect the expected recoverable amount. • Allowance for diminution in value of investment properties increased by THB 471.61 million from the previous year, following a review of the fair value of an office building for Lease for which the Company entered into a sale and purchase agreement in February 2026. 3. Share of profit (Loss) from investments in joint ventures in 2025 amounted to a loss of THB 75.22 million, compared to a share of profit of THB 4.12 million in 2024, representing a decrease of THB 79.34 million, or more than 100%. The decline was primarily due to a reduction in ownership transfers in joi

  `MDA_MJD_FY2025` · `p015` · SHA 0a479ca3ea42
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -2,110 ลบ. จาก -299 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > DEVELOPMENT 2. Total costs and expenses in 2025 amounted to THB 3,358.89 million, representing an increase of THB 906.65 million or 36.97% compared to 2024. The increase was primarily attributable to the following: • Allowance for diminution in value of properties for sale in 2025 amounted to THB 826.55 million, increasing from the previous year. The increase was due to the

  `MDA_MJD_FY2025` · `p014` · SHA a5becd96f512
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -2,110 ลบ. จาก -299 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ ต้นทุนทางการเงิน และ ค่าใช้จ่ายภาษี
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > due to the cessation of interest capitalization for certain completed projects and projects for which construction was suspended pending sale, in line with the Company's capital restructuring plan. In addition, higher interest rates and increased fees associated with newly issued debentures during the year also contributed to the rise in finance costs. 5. Income tax expense in 2025 amounted to THB 237.95 million, compared to THB 3.19 million in 2024, representing an increase of THB 234.76 million, or more than 100%. The increase was primarily attributable to the recognition of income tax expense by a subsidiary following the reversal of deferred tax assets previously recognized in prior peri

  `MDA_MJD_FY2025` · `p016` · SHA 10c181d2d3b5
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -2,110 ลบ. จาก -299 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The decline was primarily attributable to ownership transfers of units at Metris District Ladprao, which was completed in the fourth quarter of 2025, as well as the reduction in the carrying value of property development project costs to reflect their expected recoverable amounts in 2025.

  `MDA_MJD_FY2025` · `p019` · SHA 41f080673759
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The decline was primarily attributable to the disposal of a hotel property in Pattaya at the end of the second quarter of 2025, in line with the Company's portfolio restructuring plan. Management fee income in 2025 totaled THB 238.43 million, compared to THB 193.24 million in 2024, representing an increase of THB 45.19 million or 23.39%. The increase was mainly attributable to a higher number of project management and brokerage service agreements for joint venture developments, particularly Mavista Phrom Phong. MUNIQ Charoenkrung. Maru Chula, and Malton Reserve Pinklao-Kanchana.

  `MDA_MJD_FY2025` · `p011` · SHA 14f98f3242e3
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Company's review and adjustment of property values based on updated appraisals to reflect the expected recoverable amount. • Allowance for diminution in value of investment properties increased by THB 471.61 million from the previous year, following a review of the fair value of an office building for Lease for which the Company entered into a sale and purchase agreement in February 2026. 3. Share of profit (Loss) from investments in joint ventures in 2025 amounted to a loss of THB 75.22 million, compared to a share of profit of THB 4.12 million in 2024, representing a decrease of THB 79.34 million, or more than 100%. The decline was primarily due to a reduction in ownership transfers in joi

  `MDA_MJD_FY2025` · `p015` · SHA 0a479ca3ea42
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_MJD_FY2025`

##### RICHY — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ริชี่ เพลซ 2002 จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 277m | 0.17 | +13.3% | n.m. | -16.4% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 10 · NPAT 9 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 2

**RFO — เพราะอะไร** — FY2024 THB 1.1bn → FY2025 THB 783m · −286m · -26.7%

- RFO ปี 2568 อยู่ที่ 783 ลบ. ลด 26.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อุปสงค์และกำลังซื้อในประเทศ และ ภาระหนี้และโครงสร้างเงินทุน และ สินเชื่อที่อยู่อาศัยที่เข้มงวดและหนี้ครัวเรือน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the year 2025, the Company reported total revenue of Baht 531.50 million, representing a decrease of Baht 344.33 million or 39.31% compared to the same period of the previous year. The decline was primarily attributable to the continued decrease in revenue from real estate sales. This was mainly due to the still-fragile economic conditions, elevated interest rates, and increasing household debt levels, which constrained customers’ ability to obtain mortgage financing and led to more cautious consumer spending behavior.

  `MDA_RICHY_FY2025` · `p006` · SHA d17823b1bbdc
  </details>
- RFO ปี 2568 อยู่ที่ 783 ลบ. ลด 26.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue from townhouse sales amounted to Baht 56.03 million, decreasing by Baht 38.26 million or 40.58%. The decrease was mainly attributable to a 50% reduction in sales at The Rich Ville Ratchaphruek project, while The Rich Biz Home Sukhumvit 105 project and The Rich Avenue @ Damrongrak project recorded no unit transfers compared to the previous year.

  `MDA_RICHY_FY2025` · `p016` · SHA 7f4026ea435c
  </details>
- RFO ปี 2568 อยู่ที่ 783 ลบ. ลด 26.7% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2024, cost of real estate sales was Baht 564.43 million, representing 64.45% of revenue from real estate sales, while cost of rental and service business totaled Baht 94.49 million, representing 45.98% of revenue from rental and services.

  `MDA_RICHY_FY2025` · `p018` · SHA 09d4b1369b73
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 68m → FY2025 −THB 128m · −60m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -128 ลบ. จาก -67.9 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ อัตรากำไรดีขึ้น และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > The decrease in costs was primarily attributable to changes in the Company’s revenue structure, with a higher proportion of revenue derived from the rental and service business, which carries a higher gross profit margin. As a result, the overall cost-to-revenue ratio declined.

  `MDA_RICHY_FY2025` · `p019` · SHA bc5a40a37582
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -128 ลบ. จาก -67.9 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2024, cost of real estate sales was Baht 564.43 million, representing 64.45% of revenue from real estate sales, while cost of rental and service business totaled Baht 94.49 million, representing 45.98% of revenue from rental and services.

  `MDA_RICHY_FY2025` · `p018` · SHA 09d4b1369b73
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -128 ลบ. จาก -67.9 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Company recorded cost of real estate sales of Baht 340.18 million, representing 64.00% of revenue from real estate sales. The cost of rental and service business amounted to Baht 116.67 million, representing 46.47% of revenue from rental and services.

  `MDA_RICHY_FY2025` · `p017` · SHA 89a900d6ba2a
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -128 ลบ. จาก -67.9 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน และ ภาระหนี้และโครงสร้างเงินทุน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In 2025, the Company recorded finance costs of Baht 275.85 million, an increase of Baht 71.79 million or 35.18% compared to the previous year. The increase was primarily due to higher interest rates in line with market trends during 2025, as well as the management of credit facilities and debt structure that incurred higher interest expenses in the prevailing economic conditions.

  `MDA_RICHY_FY2025` · `p026` · SHA 1e795409fa86
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Subsequently, Sukhumvit Gold Property Co., Ltd. informed the Company of its business restructuring plan, which includes the disposal of land assets as its principal asset in order to repay the loan. The Company has therefore temporarily deferred the amendment of the loan agreement pending clarity on the asset disposal plan and the borrower’s ability to execute such plan.

  `MDA_RICHY_FY2025` · `p032` · SHA 8c1e82dbfd78
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > As at the end of 2025, Sukhumvit Gold Property Co., Ltd. is in the process of implementing its business restructuring and preparing conditions related to the land disposal. The Company has been receiving periodic progress updates and continues to closely monitor and assess the borrower’s repayment capability in order to manage potential credit risk.

  `MDA_RICHY_FY2025` · `p034` · SHA 7b1b8921f348
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_RICHY_FY2025`

##### PRECHA — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ปรีชากรุ๊ป จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ประกอบธุรกิจการพัฒนาอสังหาริมทรัพย์ เพื่ออยู่อาศัย ทั้งแนวราบและแนวสูง

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 148m | 0.44 | +4.8% | n.m. | -251.6% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 4 · NPAT 4 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 29m → FY2025 THB 33m · +3m · +11.8%

- RFO ปี 2568 อยู่ที่ 32.9 ลบ. เพิ่ม 11.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ปริมาณขายและปริมาณการผลิต และ ต้นทุนทางการเงิน และ ค่าใช้จ่ายขายและบริหาร และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Costs and Expenses • Cost of real estate sales increased by THB 2 million or 34%, in line with higher sales volumes. • Cost of rental and services of THB 8 million, broadly in line with the prior year. • Selling expenses increased by THB 2 million or 41%, reflecting a more active marketing effort to stimulate sales, which contributed to the meaningful revenue uplift. • Administrative expenses increased by THB 33 million or 62% due to the recognition of additional special provisions. Excluding the provisions, core administrative expenses declined by THB 13 million (FY2025: THB 41 million; FY2024: THB 54 million), reflecting improved cost discipline. • Finance costs rose by THB 5 million or 23

  `MDA_PRECHA_FY2025` · `p009` · SHA 46a20de68cd3
  </details>
- RFO ปี 2568 อยู่ที่ 32.9 ลบ. เพิ่ม 11.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Executive Summary Precha Group Public Company Limited and its subsidiaries (the "Company") hereby reports its operating results for the year ended 31 December 2025 as follows. The Company recorded total revenues of THB 34 million, an increase of 15% year-on-year (2024: THB 29 million), reflecting the Company's continued ability to sustain and grow its core revenue base despite economic headwinds and industry-wide structural challenges. The Company reported a net loss of THB 83 million, up 80% from the prior year (2024: loss of THB 46 million). The increase was largely attributable to the recognition of non-recurring special expense items unrelated to core business operations. Notably, the op

  `MDA_PRECHA_FY2025` · `p003` · SHA 05d3d833b036
  </details>
- RFO ปี 2568 อยู่ที่ 32.9 ลบ. เพิ่ม 11.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue • Real estate sales revenue of THB 13.17 million, up THB 4 million or 44% year-on-year, driven by a higher number of units sold. • Rental and service income of THB 21 million, broadly unchanged from the prior year, consistent with stable leasing market conditions.

  `MDA_PRECHA_FY2025` · `p007` · SHA 96fb55f10124
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 46m → FY2025 −THB 83m · −37m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -82.9 ลบ. จาก -46.0 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ปริมาณขายและปริมาณการผลิต และ ต้นทุนทางการเงิน และ ค่าใช้จ่ายขายและบริหาร และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Costs and Expenses • Cost of real estate sales increased by THB 2 million or 34%, in line with higher sales volumes. • Cost of rental and services of THB 8 million, broadly in line with the prior year. • Selling expenses increased by THB 2 million or 41%, reflecting a more active marketing effort to stimulate sales, which contributed to the meaningful revenue uplift. • Administrative expenses increased by THB 33 million or 62% due to the recognition of additional special provisions. Excluding the provisions, core administrative expenses declined by THB 13 million (FY2025: THB 41 million; FY2024: THB 54 million), reflecting improved cost discipline. • Finance costs rose by THB 5 million or 23

  `MDA_PRECHA_FY2025` · `p009` · SHA 46a20de68cd3
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -82.9 ลบ. จาก -46.0 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Executive Summary Precha Group Public Company Limited and its subsidiaries (the "Company") hereby reports its operating results for the year ended 31 December 2025 as follows. The Company recorded total revenues of THB 34 million, an increase of 15% year-on-year (2024: THB 29 million), reflecting the Company's continued ability to sustain and grow its core revenue base despite economic headwinds and industry-wide structural challenges. The Company reported a net loss of THB 83 million, up 80% from the prior year (2024: loss of THB 46 million). The increase was largely attributable to the recognition of non-recurring special expense items unrelated to core business operations. Notably, the op

  `MDA_PRECHA_FY2025` · `p003` · SHA 05d3d833b036
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -82.9 ลบ. จาก -46.0 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Income Statement Overview The income statement for the year ended 31 December 2025, compared with the prior year, reflected the following material items: • Net loss of THB 83 million, up 80% year-on-year (2024: loss of THB 46 million). • Operating loss of THB 38 million, down 26% year-on-year (2024: loss of THB 51 million).

  `MDA_PRECHA_FY2025` · `p006` · SHA d3286036dc04
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -82.9 ลบ. จาก -46.0 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ปริมาณขายและปริมาณการผลิต และ กำลังการผลิตและเครื่องจักรใหม่ และ ภาระหนี้และโครงสร้างเงินทุน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Industry Overview — FY2025 Residential Real Estate. The mid-to-low-end residential segment faced structural headwinds including persistently elevated interest rates, rising household debt levels, and tightened mortgage lending standards at financial institutions—all of which dampened consumer purchasing power. The Company responded by recalibrating its marketing strategy to align with actual purchasing capacity, successfully preserving sales volumes in its key projects. Office Space Leasing. The office leasing market remained highly competitive. Demand for space recovered gradually alongside broader economic recovery, though tenants continued to prioritize cost management and Hybrid Working

  `MDA_PRECHA_FY2025` · `p004` · SHA 695aea9720e0
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- เอกสารที่มีอยู่ยังไม่ระบุรายการพิเศษหรือรายการต่ำกว่าการดำเนินงานอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Executive Summary Precha Group Public Company Limited and its subsidiaries (the "Company") hereby reports its operating results for the year ended 31 December 2025 as follows. The Company recorded total revenues of THB 34 million, an increase of 15% year-on-year (2024: THB 29 million), reflecting the Company's continued ability to sustain and grow its core revenue base despite economic headwinds and industry-wide structural challenges. The Company reported a net loss of THB 83 million, up 80% from the prior year (2024: loss of THB 46 million). The increase was largely attributable to the recognition of non-recurring special expense items unrelated to core business operations. Notably, the op

  `MDA_PRECHA_FY2025` · `p003` · SHA 05d3d833b036
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_PRECHA_FY2025`

##### KC — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เค.ซี. พร็อพเพอร์ตี้ จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัทประกอบธุรกิจในด้านพัฒนาอสังหาริมทรัพย์ และธุรกิจให้เช่าและบริการพื้นที่อาคารสำนักงาน

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 104m | 0.02 | -50.0% | n.m. | -952.8% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 14 · NPAT 16 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 6

**RFO — เพราะอะไร** — FY2024 THB 52m → FY2025 THB 16m · −37m · -69.9%

- RFO ปี 2568 อยู่ที่ 15.7 ลบ. ลด 69.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 1. Revenues Income The Company and its subsidiaries reported total revenues of Baht 27.17 million and Baht 59.18 million for the years ended December 31, 2025, and 2024, respectively. Total revenue decreased by Baht 32.01 million, or 54.09%, compared to the same period last year, with details as follows: 1.1 Revenues from sales For the years 2025 and 2024, the Company recorded revenue from real estate sales of Baht 15.73 million and Baht 52.31 million, respectively. This represents a decrease of Baht 36.58 million or 69.93% compared to the same period last year. Sales revenue was derived from low-rise housing projects, consistent with the previous year. The decrease in sales revenue for 2025

  `MDA_KC_FY2025` · `p012` · SHA 5f5dcf781aaa
  </details>
- RFO ปี 2568 อยู่ที่ 15.7 ลบ. ลด 69.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2. Cost of sales and rendering of services 2.1 Cost of sales The Company’s cost of real estate sales for 2025 and 2024 amounted to Baht 14.65 million and Baht 42.83 million, respectively. This represents a decrease of Baht 28.18 million, or 65.80%, compared to the same period last year. When compared to sales revenue, the cost of real estate sales for 2025 was 11.25% higher than in 2024. This increase in the cost-to-revenue ratio was primarily due to the decline in sales revenue, resulting in a higher proportion of costs relative to revenue compared to the previous year. As per the details shown in the Revenue from Sales table. (Unit: million Baht) Statements of Comprehensive Income Consolid

  `MDA_KC_FY2025` · `p014` · SHA 89584d572b17
  </details>
- RFO ปี 2568 อยู่ที่ 15.7 ลบ. ลด 69.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For year, ended of Dec 31 2025 2024 Increase / Decrease 2025 2024 Revenue from sales and services 1 5.73 5 2.31 (36.58) 69.93% 100.00% 100.00% Distribution costs (4.55) (7.68) 3.13 40.76% 28.93% 14.68% Distribution costs as a percentage of sales revenue for 2025 and 2024 were 28.93% and 14.68%, respectively. The 2025 ratio increased by 14.24% compared to 2024, primarily due to the Baht 36.58 million or 69.93% decline in real estate sales revenue. Distribution costs consist of both variable costs—which fluctuate according to revenue—and operational selling expenses, such as marketing expenses and sales-related costs, including personnel expenses. 4.2 Administrative expenses The Company and it

  `MDA_KC_FY2025` · `p019` · SHA 72b4808c4dd0
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 136m → FY2025 −THB 150m · −14m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -150 ลบ. จาก -136 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ต้นทุนทางการเงิน และ ค่าใช้จ่ายภาษี และ ภาระหนี้และโครงสร้างเงินทุน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Other expenses Loss from litigation (reversal) - 0 .17 (0.17) 1 00.00 - 0 .32 Loss from litigation (12.61) (33.99) 21.38 62.90 (80.17) (64.98) Loss from impairment of Investment Property (38.56) - (38.56) (100.00) (245.14) - Loss on breach of ineffective debt restructuring agreement (18.34) - (18.34) (100.00) (116.59) - Loss from impairment of land held for development (1.30) (9.86) 8.56 86.82 (8.26) (18.85) Profit (loss) from operating activities (134.69) (105.72) (28.97) (27.40) (856.26) (202.10) Finance costs (15.05) (29.75) 14.70 49.41 (95.68) (56.87) Profit (loss) before income tax expense (149.74) (135.47) (14.27) (10.53) (951.94) (258.98) Tax income (expense) (0.14) (0.09) (0.05) (0.1

  `MDA_KC_FY2025` · `p006` · SHA fd92548b6fe9
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -150 ลบ. จาก -136 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2. Cost of sales and rendering of services 2.1 Cost of sales The Company’s cost of real estate sales for 2025 and 2024 amounted to Baht 14.65 million and Baht 42.83 million, respectively. This represents a decrease of Baht 28.18 million, or 65.80%, compared to the same period last year. When compared to sales revenue, the cost of real estate sales for 2025 was 11.25% higher than in 2024. This increase in the cost-to-revenue ratio was primarily due to the decline in sales revenue, resulting in a higher proportion of costs relative to revenue compared to the previous year. As per the details shown in the Revenue from Sales table. (Unit: million Baht) Statements of Comprehensive Income Consolid

  `MDA_KC_FY2025` · `p014` · SHA 89584d572b17
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -150 ลบ. จาก -136 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 3. Gross profit (loss) The Company and its subsidiaries reported a gross profit (loss) for the years 2025 and 2024 of Baht (4.89) million and Baht 9.48 million, respectively. Gross profit decreased by Baht 14.37 million, or 151.58%, compared to the same period last year. The gross loss of Baht (4.89) million includes a gross loss of Baht (5.97) million from the rental and office space service business at a single location on Ladprao Road. This business has not yet generated any rental or service revenue (as the Company received the Building Occupancy Certificate (Form Or. 5) in June 2025), as previously mentioned in Note 2.2, ' Cost of rental and rendering of service business. The gross prof

  `MDA_KC_FY2025` · `p016` · SHA 3af77a3251f3
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -150 ลบ. จาก -136 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าเสื่อมราคาและค่าตัดจำหน่าย และ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For year, ended of Dec 31 2025 2024 Increase / Decrease 2025 2024 Revenue from sales 1 5.73 5 2.31 (36.58) 69.93% 100.00% 100.00% Cost of sales (14.65) (42.83) 28.18 65.80% 93.13% 81.88% Gross profit 1 .08 9 .48 (8.40) (88.61%) 6.87% 18.12% 2.2 Cost of rental and rendering of service business For the year 2025, the Company incurred costs from its rental and office space services for a single location amounting to Baht 5.97 million. These costs were recognized following the issuance of the Building Occupancy Certificate (Form Or. 5) on June 4, 2025. The total cost consists of depreciation of Baht 5.94 million and maintenance expenses of Baht 0.03 million.

  `MDA_KC_FY2025` · `p015` · SHA 44bb4ae4fc37
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Impairment loss on investment property totaling Baht 38.56 million. Of this amount, Baht 32.98 million relates to right-of-use (ROU) assets for land, buildings, and improvements at an office rental and service location. Although the Building Occupancy Certificate (Form Or. 5) was received in June 2025, no rental or service revenue was generated in 2025. As of December 31, 2025, the carrying value exceeded the fair value as assessed by an independent appraiser. The fair value of land and land improvements was determined using the Market Approach, while the fair value of the office building was determined using the Income Approach. Key assumptions used in the valuation included the yield rate,

  `MDA_KC_FY2025` · `p022` · SHA 7e65490019cb
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ต้นทุนทางการเงิน และ ค่าใช้จ่ายภาษี และ ภาระหนี้และโครงสร้างเงินทุน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Other expenses Loss from litigation (reversal) - 0 .17 (0.17) 1 00.00 - 0 .32 Loss from litigation (12.61) (33.99) 21.38 62.90 (80.17) (64.98) Loss from impairment of Investment Property (38.56) - (38.56) (100.00) (245.14) - Loss on breach of ineffective debt restructuring agreement (18.34) - (18.34) (100.00) (116.59) - Loss from impairment of land held for development (1.30) (9.86) 8.56 86.82 (8.26) (18.85) Profit (loss) from operating activities (134.69) (105.72) (28.97) (27.40) (856.26) (202.10) Finance costs (15.05) (29.75) 14.70 49.41 (95.68) (56.87) Profit (loss) before income tax expense (149.74) (135.47) (14.27) (10.53) (951.94) (258.98) Tax income (expense) (0.14) (0.09) (0.05) (0.1

  `MDA_KC_FY2025` · `p006` · SHA fd92548b6fe9
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_KC_FY2025`

##### AKS — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท เอเคเอส คอร์ปอเรชั่น จำกัด (มหาชน)** — ข้อมูลเทียบเคียงจำกัด: ไม่ควรสรุปเหตุเชื่อมโยงระหว่างรายได้กับกำไร

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาและค้าอสังหาริมทรัพย์ ทั้งแนวราบและแนวสูง และบริการให้เช่าอสังหาริมทรัพย์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| — | 0.01 | -50.0% | n.m. | — |

สังเคราะห์จากแหล่งข้อมูลรอง · ยังไม่มี MD&A ฉบับหลัก · หลักฐานรายข้อ — RFO 0 · NPAT 0 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 339m → FY2025 — · —

- รายได้ FY2025 เหลือเพียงประมาณ 210 ลบ. และยังไม่มี MD&A ประจำปีในคลังหลัก จึงไม่อ้างสาเหตุว่าเป็นคำอธิบายจากฝ่ายจัดการ

**NPAT — เพราะอะไร** — FY2024 −THB 2.7bn → FY2025 — · —

- ขาดทุน 315 ลบ. EBITDA ติดลบ และส่วนผู้ถือหุ้นติดลบสะท้อนความเสี่ยงดำเนินงาน/ฐานะการเงิน แต่การไม่มี เอกสารที่ยื่นต่อตลาดหลักทรัพย์ ทำให้ยังทำ การแจกแจงสาเหตุกำไร จากฝ่ายจัดการไม่ได้

> **เส้นทางหลักฐาน · ไม่มี MD&A FY2025 ฉบับหลัก** — ตัวเลขยังเป็นตัวเลขสอบทาน แต่คำอธิบายสาเหตุเป็นข้อมูลรองที่ติดป้ายชัดเจนจนกว่าจะได้ MD&A ประจำปี  
> แหล่งข้อมูล: `FY_PANEL / COMPANY_REPORTS`

#### ทะเบียนข้อสรุป — P1

| ส่วน | ประเภท | ข้อสรุป | รหัสแหล่งข้อมูล |
|---|---|---|---|
| headline | ข้ออนุมานนักวิเคราะห์ | ข้อจำกัดสินเชื่อกดดันผลประกอบการในวงกว้าง | FY_PANEL, P1_E1, P1_E2, P1_E3, P1_E4 |
| earnings_fact | ข้อเท็จจริงจากการคำนวณ | FY2025 RFO -11.8%; สถานะ NPAT ส่วนผู้ถือหุ้น: profit_decreased | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | RFO ที่สอบทานแล้วลด 11.8% และ NPAT ส่วนผู้ถือหุ้นลด 33.8% ใน 33/37 บริษัท | FY_PANEL |
| why | คำอธิบายฝ่ายจัดการ | ยอดโอน mix และ gross margin อ่อนตัว ขณะที่การปฏิเสธสินเชื่อยังสูง | P1_E1, P1_E2, P1_E3, P1_E4 |
| why | ข้อเท็จจริงจากการคำนวณ | ASW นำราคา YTD ปัจจุบัน แต่กำไร FY2025 ยังไม่ยืนยันการฟื้นในวงกว้าง | FY_PANEL, SET_PUBLIC_EOD |
| causal_chain | ข้ออนุมานนักวิเคราะห์ | ห่วงโซ่เหตุ: อุปสงค์ → อนุมัติสินเชื่อ → โอน → Margin → Cash | P1_E1, P1_E2, P1_E3, P1_E4 |
| roles | ข้ออนุมานนักวิเคราะห์ | บทบาท: ผู้นำ — LH; ตัวฉุดผลประกอบการ — SPALI; ผู้นำราคา YTD — ASW | FY_PANEL, P1_E1, P1_E2, P1_E3, P1_E4 |
| valuation | ข้ออนุมานนักวิเคราะห์ | P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 7.9x ครอบคลุม 26/37 บริษัท และ 93.5% ของ market cap ที่มีข้อมูล. ส่วนลดสะท้อนกำลังซื้อ การโอน และ cash-conversion risk | SET_PUBLIC_EOD, P1_E1, P1_E2, P1_E3, P1_E4 |
| trigger | ประเด็นที่ต้องพิสูจน์ | อัตราปฏิเสธสินเชื่อลด | P1_E1, P1_E2, P1_E3, P1_E4 |
| trigger | ประเด็นที่ต้องพิสูจน์ | การโอนและแปลง backlog ดีขึ้น | P1_E1, P1_E2, P1_E3, P1_E4 |
| trigger | ประเด็นที่ต้องพิสูจน์ | inventory และ leverage ลด | P1_E1, P1_E2, P1_E3, P1_E4 |
| risk | ประเด็นที่ต้องพิสูจน์ | กำลังซื้ออ่อนยาว | P1_E1, P1_E2, P1_E3, P1_E4 |
| risk | ประเด็นที่ต้องพิสูจน์ | ส่วนลดกด margin | P1_E1, P1_E2, P1_E3, P1_E4 |
| risk | ประเด็นที่ต้องพิสูจน์ | inventory และ cash cycle แย่ลง | P1_E1, P1_E2, P1_E3, P1_E4 |
| must_prove | ประเด็นที่ต้องพิสูจน์ | 6M26 ต้องเห็นการโอน margin และ operating cash flow ดีขึ้นพร้อมกัน | P1_E1, P1_E2, P1_E3, P1_E4 |

#### ทะเบียนหลักฐาน — P1

- **`FY_PANEL`** · _ข้อเท็จจริงจากการคำนวณ_ — Audited FY2024-25 company panel
  - RFO / NPAT-to-owners / independent panel membership; QA 43 pass / 0 fail
  - บทบาท: historical fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_company_fy2024_2025_audited_2026-08-07.csv`
  - SHA-256: `e5e04dbc40ffcc79fed58545a93dc4549c29cdaecf260bea73711bc6d0720481`
- **`SET_PUBLIC_EOD`** · _ข้อเท็จจริงจากการคำนวณ_ — SET public Company Highlights — EOD 2026-08-07
  - Adjusted YTD; unadjusted price, market cap and valuation; factsheet-surface cross-check
  - บทบาท: current market fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_set_public_surface_reconciliation_2026-08-07.csv`
  - SHA-256: `544c1f29fe2d409ee398822ac2bf32b769081718962ae2d1138985b0146b9530`
- **`SET_COMPANY_PROFILE`** · _ข้อเท็จจริง_ — SET company profiles — English and Thai
  - Official company names and business descriptions refreshed and validated for the 118-company perimeter from the public SET profile API
  - บทบาท: company business profile
  - URL: <https://www.set.or.th/th/market/product/stock/overview>
- **`COMPANY_REPORTS`** · _ข้ออนุมานนักวิเคราะห์_ — Company report synthesis corpus
  - Annual-only draft synthesis; reconciled to the ticker FY2025 MD&A where available
  - บทบาท: secondary synthesis; not management attribution
  - พาธ: `data/company-reports.json`
  - SHA-256: `c1a2bc40cbe21a2058aa596c362e4d47ad117360831b847de78ec414831fd2d2`
- **`MDA_LH_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — LH FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/LH/MDA_LH_2025FY_E.md`
  - SHA-256: `c176f0854c095249d113d8ddbc502f5130b58c51cd37ed94858c612b774e4e2a`
  - URL: <https://weblink.set.or.th/dat/news/202602/0143NWS270220262110056660E.pdf>
- **`MDA_SPALI_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — SPALI FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SPALI/MDA_SPALI_2025FY_E.md`
  - SHA-256: `bcdbb87564056d2d15f7886a30d8a457a64471510e54aabf4922c601adf63f4a`
  - URL: <https://weblink.set.or.th/dat/news/202602/0371NWS240220261913091210E.pdf>
- **`MDA_SIRI_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — SIRI FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SIRI/MDA_SIRI_2025FY_E.md`
  - SHA-256: `bbae98821f3684d30b28c91b9ac27db7fc178d516ca7f45a88a9597eaf5346ef`
  - URL: <https://weblink.set.or.th/dat/news/202602/0577NWS270220260817561540E.pdf>
- **`MDA_AP_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — AP FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/AP/MDA_AP_2025FY_E.md`
  - SHA-256: `b1c58d96f9aeb27549bbec454e913747567eddc404d96b05afbba0c0486e67b3`
  - URL: <https://ap.listedcompany.com/misc/MDNA/20260226-ap-mdna-4q2025-en.pdf>
- **`MDA_FPT_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — FPT FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/FPT/MDA_FPT_2025FY_T.md`
  - SHA-256: `860f90c5c2fc1c2718523e293f49040acc66556db4f820db16ded4f8053b9ee9`
  - URL: <https://weblink.set.or.th/dat/news/202511/0675NWS061120251837343970T.pdf>
- **`MDA_QH_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — QH FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/QH/MDA_QH_2025FY_E.md`
  - SHA-256: `e1073e6dcbdec540c6b38e8cedbf985aa458baa0acb3cd100dfa60b9736c83f7`
  - URL: <https://weblink.set.or.th/dat/news/202602/0256NWS240220262140391050E.pdf>
- **`MDA_PSH_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — PSH FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/PSH/MDA_PSH_2025FY_E.md`
  - SHA-256: `57eb6dad9b706762909842ceac9fb1f315d979cc340247454c3a3e2c8e4852f5`
  - URL: <https://weblink.set.or.th/dat/news/202602/1337NWS270220262118397830E.pdf>
- **`MDA_SC_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — SC FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SC/MDA_SC_2025FY_E.md`
  - SHA-256: `179856723188ce76a8f1e62ba66de2d5d057acd37d8793e0c85ffec2ef459879`
  - URL: <https://weblink.set.or.th/dat/news/202602/0747NWS250220261230068760E.pdf>
- **`MDA_SA_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — SA FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SA/MDA_SA_2025FY_E.md`
  - SHA-256: `bf819edbfffcbb0fe13a03ba540558d69b01f64e7c8df215036e5ea493d6d169`
  - URL: <https://weblink.set.or.th/dat/news/202603/1284NWS020320261715439840E.pdf>
- **`MDA_ASW_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — ASW FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/ASW/MDA_ASW_2025FY_E.md`
  - SHA-256: `6a58dd0fa9fd29e55e375e436032c875726801f551ccdb50cf5a18d32217b6f4`
  - URL: <https://weblink.set.or.th/dat/news/202602/1638NWS190220262039369330E.pdf>
- **`MDA_ORI_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — ORI FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/ORI/MDA_ORI_2025FY_E.md`
  - SHA-256: `972eef54c4917177ce2898aa543ca555da3f88034c2ada5c497e8901b6b18085`
  - URL: <https://weblink.set.or.th/dat/news/202602/1260NWS270220262209559080E.pdf>
- **`MDA_LALIN_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — LALIN FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/LALIN/MDA_LALIN_2025FY_E.md`
  - SHA-256: `24d8f99c404665e0874a993a3f07c6379cd8504c78b0e04711d1456a29335d74`
  - URL: <https://weblink.set.or.th/dat/news/202602/0693NWS270220260701169730E.pdf>
- **`MDA_A_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — A FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/A/MDA_A_2025FY_E.md`
  - SHA-256: `be0f10bbc5fb67ffe4afe86a05610627e7516179ac2a7c3b2410fa383643547a`
  - URL: <https://weblink.set.or.th/dat/news/202604/0770NWS160420260750218970E.pdf>
- **`MDA_SENA_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — SENA FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SENA/MDA_SENA_2025FY_E.md`
  - SHA-256: `046287cf448102dd281c238f2724376568692a97a921b25a80ba024145bb0738`
  - URL: <https://weblink.set.or.th/dat/news/202602/1011NWS270220260706520610E.pdf>
- **`MDA_NOBLE_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — NOBLE FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/NOBLE/MDA_NOBLE_2025FY_E.md`
  - SHA-256: `ca0aa75ddb249e957c54c392e2445e27e5971dac32eb042f9d5d1f24265f3a4e`
  - URL: <https://weblink.set.or.th/dat/news/202603/0564NWS020320260741522150E.pdf>
- **`MDA_LPN_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — LPN FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/LPN/MDA_LPN_2025FY_E.md`
  - SHA-256: `c670e2f2661c7ecc15dd43ce090208a11121df3c5debabf6f8cfd86163e19e24`
  - URL: <https://weblink.set.or.th/dat/news/202602/0456NWS260220261251420230E.pdf>
- **`MDA_A5_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — A5 FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/A5/MDA_A5_2025FY_E.md`
  - SHA-256: `b0758caaaff875c8afd3c894db0dc7dc5385f3d4f5f0567cfdfe8cd9fc53f10e`
  - URL: <https://weblink.set.or.th/dat/news/202602/0746NWS260220262210593120E.pdf>
- **`MDA_BRI_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — BRI FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/BRI/MDA_BRI_2025FY_E.md`
  - SHA-256: `35a089a847403da9a8d7ce9fe8d4acfb0e1f0b55d97f7ca35d478e0729cd2594`
  - URL: <https://weblink.set.or.th/dat/news/202602/1675NWS270220260835052430E.pdf>
- **`MDA_PRIN_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — PRIN FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/PRIN/MDA_PRIN_2025FY_E.md`
  - SHA-256: `a2dbf55a07b215ffee34b70f0f7f19247dd29a854141f4120c95dc555479d552`
  - URL: <https://weblink.set.or.th/dat/news/202602/0865NWS260220261806222570E.pdf>
- **`MDA_NVD_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — NVD FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/NVD/MDA_NVD_2025FY_E.md`
  - SHA-256: `c2713659aa4be7b6bd49708778b0a4769c2e16196ce7636b6b91a4513c47b7e2`
  - URL: <https://weblink.set.or.th/dat/news/202602/1262NWS230220261849135350E.pdf>
- **`MDA_ANAN_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — ANAN FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/ANAN/MDA_ANAN_2025FY_E.md`
  - SHA-256: `c644401953d86c3c1bbab4807394ab92270eebe4fba3b3e98704bc0bb0513063`
  - URL: <https://weblink.set.or.th/dat/news/202602/1099NWS230220262015053170E.pdf>
- **`MDA_ORN_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — ORN FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/ORN/MDA_ORN_2025FY_E.md`
  - SHA-256: `1a98980ccf66b62dfdf9bc1c0d0b0cf44215e04348620d99adb816385b323775`
  - URL: <https://weblink.set.or.th/dat/news/202602/1833NWS200220261904469390E.pdf>
- **`MDA_ESTAR_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — ESTAR FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/ESTAR/MDA_ESTAR_2025FY_E.md`
  - SHA-256: `161c53b2ed88976bb8b4c6101ac0042e63b2fa6c0e0b635d64e67f85db65eaf0`
  - URL: <https://weblink.set.or.th/dat/news/202602/0381NWS270220262049166930E.pdf>
- **`MDA_BROCK_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — BROCK FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/BROCK/MDA_BROCK_2025FY_E.md`
  - SHA-256: `9edb32f1dab52c5786b93a4e6352762f2866976c9beda1fb81920881e4274b2d`
  - URL: <https://weblink.set.or.th/dat/news/202602/0887NWS240220261856268030E.pdf>
- **`MDA_PROUD_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — PROUD FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/PROUD/MDA_PROUD_2025FY_E.md`
  - SHA-256: `132be92c9ac0194c9b241f2ce95e0a9765dc13c7cdfc02adf15de6de8e8ae162`
  - URL: <https://weblink.set.or.th/dat/news/202602/0797NWS250220262204314430E.pdf>
- **`MDA_PEACE_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — PEACE FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/PEACE/MDA_PEACE_2025FY_E.md`
  - SHA-256: `0d7a4223080712abd50f1d2983ebaafc3154bbdbd96240b9813bbd7e8fcc4d6c`
  - URL: <https://weblink.set.or.th/dat/news/202602/1679NWS260220261756492730E.pdf>
- **`MDA_NCH_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — NCH FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/NCH/MDA_NCH_2025FY_E.md`
  - SHA-256: `6c7059145bf7fba66be2f4b9905b988da41a505f82824731e66c55d7754f9234`
  - URL: <https://weblink.set.or.th/dat/news/202602/0769NWS270220262229247240E.pdf>
- **`MDA_SAMCO_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — SAMCO FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SAMCO/MDA_SAMCO_2025FY_E.md`
  - SHA-256: `5da52f216c65532076b538af392288a8c551e5b8cd1e2e53ec755352acba1898`
  - URL: <https://weblink.set.or.th/dat/news/202602/0349NWS240220261952127050E.pdf>
- **`MDA_RML_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — RML FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/RML/MDA_RML_2025FY_E.md`
  - SHA-256: `12881886b418ee4fcd60c9eaa87431b07fb2e1c79910e119c676cfcffb96a51f`
  - URL: <https://weblink.set.or.th/dat/news/202603/0364NWS020320262042012550E.pdf>
- **`MDA_PF_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — PF FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/PF/MDA_PF_2025FY_E.md`
  - SHA-256: `900e67049b798d2469d8164104c7c56dc93efb094164ecb08e68bb3c71e355c3`
  - URL: <https://weblink.set.or.th/dat/news/202604/0352NWS070420261232270310E.pdf>
- **`MDA_KUN_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — KUN FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/KUN/MDA_KUN_2025FY_E.md`
  - SHA-256: `752bc3b53b82824570c8970864e9050e66c986aee9713f88abdef141bf14f836`
  - URL: <https://weblink.set.or.th/dat/news/202602/1525NWS250220261947218030E.pdf>
- **`MDA_CMC_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — CMC FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/CMC/MDA_CMC_2025FY_E.md`
  - SHA-256: `8039e2efcc56f3e6d14f2779895b847ed8fa93919c7dbcc186d1fb23fa12fddf`
  - URL: <https://weblink.set.or.th/dat/news/202602/1301NWS250220260730555900E.pdf>
- **`MDA_MJD_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — MJD FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/MJD/MDA_MJD_2025FY_E.md`
  - SHA-256: `3b0f0c670e4585e3090f6737bf4cd6626247a33706f9ebb7f81f36dd9a9d39ba`
  - URL: <https://weblink.set.or.th/dat/news/202603/0960NWS020320260654168230E.pdf>
- **`MDA_RICHY_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — RICHY FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/RICHY/MDA_RICHY_2025FY_E.md`
  - SHA-256: `003307889301939906dc34083f8a823c0c80226cff168d93ddbc55593b4e5719`
  - URL: <https://weblink.set.or.th/dat/news/202602/1187NWS270220261833310230E.pdf>
- **`MDA_PRECHA_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — PRECHA FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/PRECHA/MDA_PRECHA_2025FY_E.md`
  - SHA-256: `66c3835d35a962f2d349683a2e1fa2e3c88e6f9c6fa96cb33c9f2bd144a2f7c1`
  - URL: <https://weblink.set.or.th/dat/news/202603/0548NWS020320260819435610E.pdf>
- **`MDA_KC_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — KC FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/KC/MDA_KC_2025FY_E.md`
  - SHA-256: `365e61297c8de4ce368b386adf08ed1f2f7f5650a28c9724c4073773307e903e`
  - URL: <https://weblink.set.or.th/dat/news/202603/0446NWS020320260828587670E.pdf>
- **`P1_E1`** · _ฝ่ายจัดการ_ — SPALI FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SPALI/MDA_SPALI_2025FY_E.md`
  - SHA-256: `bcdbb87564056d2d15f7886a30d8a457a64471510e54aabf4922c601adf63f4a`
- **`P1_E2`** · _ฝ่ายจัดการ_ — PSH FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/PSH/MDA_PSH_2025FY_E.md`
  - SHA-256: `57eb6dad9b706762909842ceac9fb1f315d979cc340247454c3a3e2c8e4852f5`
- **`P1_E3`** · _ฝ่ายจัดการ_ — SAMCO FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/SAMCO/MDA_SAMCO_2025FY_E.md`
  - SHA-256: `5da52f216c65532076b538af392288a8c551e5b8cd1e2e53ec755352acba1898`
- **`P1_E4`** · _มุมมองล่วงหน้า_ — INVX LH research
  - Historical explanation or forward cross-check; see source role
  - บทบาท: forward/credit context
  - พาธ: `Listed Company/1-Raw/06-Market Reference/Broker Research/2026/PROP/INVX_LH_343581.md`
  - SHA-256: `6bd150ca11e48b63481d2607cd46d70777673d2c2e4f4d5793bc8cbf788c3266`
- **`P1_FACTSHEET`** · _ข้อเท็จจริงจากการคำนวณ_ — SET Factsheet — LH
  - Live leader cross-check
  - บทบาท: presentation-surface check
  - URL: <https://www.set.or.th/th/market/product/stock/quote/lh/factsheet>

### P2 · นิคมอุตสาหกรรมและโลจิสติกส์ — FDI optionality ผลักราคานำกำไรรายงาน

`ราคานำพื้นฐาน` · 15.8% M-cap · THB 133bn · 9 บริษัท

| ตัวชี้วัด | RFO | NPAT | ราคา | P/E |
|---|---|---|---|---|
| ช่วง | FY2025 YoY | ส่วนผู้ถือหุ้น FY2025 YoY | ราคา YTD ปรับแล้ว | เฉพาะบริษัทที่มีกำไร |
| ค่า | -12.4% | -29.8% | +50.2% | 10.7x |
| จำนวน | THB 52.9bn FY2025 | THB 8.6bn FY2025 | ณ 7 ส.ค. 2569 | ค่าเฉลี่ยรวม |
| ครอบคลุม | 9/9 | 9/9 | 9/9 • 100% M-cap | 6/9 • 99% M-cap |

**ข้อเท็จจริงที่สังเกตได้** — FY2025: RFO -12.4% • NPAT -29.8% • ราคา YTD +50.2% • P/E 10.7x • ครอบคลุม RFO 9/9 • NPAT 9/9

#### เหตุผลที่เปลี่ยน

1. _ข้อเท็จจริงจากการคำนวณ_ · BOI / FDI — RFO ลด 12.4% และ NPAT ส่วนผู้ถือหุ้นลด 29.8% แม้ราคา YTD แข็งแรง
2. _คำอธิบายฝ่ายจัดการ_ · ยอดขายที่ดิน — การโอนที่ดินต่ำกว่าคาด ขณะที่ FDI และความพร้อม data centre สนับสนุน optionality
3. _ข้ออนุมานนักวิเคราะห์_ · โอน — ROJNA เป็นตัวแปรกำไรรายงานและ mark-to-market ไม่ใช่หลักฐานการดำเนินงานที่สะอาด

#### ห่วงโซ่เหตุและผล

**BOI / FDI** → **ยอดขายที่ดิน** → **โอน** → **Utility / ค่าเช่า** → **NPAT** (-29.8% THB 8.6bn FY2025)

#### บทบาทในกลุ่ม

| บทบาท | Ticker | ค่า | ที่มาของค่า |
|---|---|---|---|
| ผู้นำ | WHA | 56% | สัดส่วน Market Cap ในกลุ่ม |
| ตัวแทน FDI และราคา | AMATA | +77.7% | ราคา YTD ปรับแล้ว |
| ตัวแปรกำไรรายงาน | ROJNA | ขาดทุน | NPAT YoY · Δ −4.0bn |

#### มูลค่า

**ตลาดกำลังจ่ายเพื่อ — ข้ออนุมาน** — P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 10.7x ครอบคลุม 6/9 บริษัท และ 98.9% ของ market cap ที่มีข้อมูล. rerating สอดคล้องกับความคาดหวัง FDI/data centre แต่ยังไม่ใช่หลักฐานกำไร

| Trigger | Risk |
|---|---|
| ยอดขายที่ดินและการโอนเกิดจริง | FDI แปลงเป็นการลงทุนจริงล่าช้า |
| ความพร้อมด้านไฟฟ้าสำหรับ data center | โอนและโครงสร้างพื้นฐานล่าช้า |
| ปริมาณ utility เพิ่ม | ข้อจำกัดที่ดิน ไฟฟ้า และกฎระเบียบ |

**6M26 ต้องพิสูจน์** — 6M26 ต้องเปลี่ยนข่าวนโยบายและ presales ให้เป็นการโอน utility และ cash earnings

#### วิเคราะห์รายบริษัท — P2 นิคมอุตสาหกรรมและโลจิสติกส์

_ทุกบริษัทใน perimeter ของ Segment ที่สอบทาน_

| Ticker | บทบาท | M-cap | RFO YoY | NPAT YoY | ราคา YTD | P/E | Margin |
|---|---|---|---|---|---|---|---|
| WHA | ผู้นำ | THB 73.8bn | +34.7% | +17.8% | +50.6% | 16.2x | 33.6% |
| AMATA | ตัวแทน FDI และราคา | THB 33.9bn | -3.0% | +27.6% | +77.7% | 9.2x | 22.0% |
| ROJNA | ตัวแปรกำไรรายงาน | THB 12.3bn | -23.7% | ขาดทุน | +38.6% | 4.7x | -0.8% |
| PIN | บริษัทในกลุ่ม | THB 5.4bn | -69.0% | -71.3% | +10.4% | 7.9x | 38.5% |
| NNCL | บริษัทในกลุ่ม | THB 3.7bn | +2.4% | -22.4% | +20.0% | 13.3x | 34.7% |
| AMATAV | บริษัทในกลุ่ม | THB 2.2bn | -25.4% | +507.1% | +15.6% | 4.9x | 11.6% |
| MK | บริษัทในกลุ่ม | THB 840m | -33.8% | ขาดทุนลดลง | 0.0% | n.m. | -34.3% |
| JCK | บริษัทในกลุ่ม | THB 456m | -70.8% | ขาดทุน | -7.7% | n.m. | -61.3% |
| WIN | บริษัทในกลุ่ม | THB 163m | +129.9% | -26.8% | -17.1% | n.m. | 0.7% |

##### WHA — ผู้นำ · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ดับบลิวเอชเอ คอร์ปอเรชั่น จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — กลุ่มบริษัท ดับบลิวเอชเอ คอร์ปอเรชั่น จำกัด (มหาชน) ดำเนินธุรกิจที่ครอบคลุม 5 ธุรกิจหลัก ได้แก่ (1) ธุรกิจพัฒนาและบริหารจัดการด้านโลจิสติกส์ (Logistics Business) พัฒนาโครงการคลังสินค้า ศูนย์กระจายสินค้า และโรงงานคุณภาพสูง (2) ธุรกิจพัฒนานิคมอุตสาหกรรม (Industrial Development Business) พัฒนาที่ดินอุตสาหกรรมและโรงงาน/คลังสินค้าสำเร็จรูป พร้อมโครงสร้างพื้นฐานครบครัน (3) ธุรกิจให้บริการสาธารณูปโภคและพลังงาน (Utilities…

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 73.8bn | 4.94 | +50.6% | 16.2x | 33.6% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 11.3bn → FY2025 THB 15.3bn · +3.9bn · +34.7%

- RFO เพิ่ม 34.7% จากการโอนที่ดินและรายได้ประจำด้านสาธารณูปโภค/โลจิสติกส์ โดยอุปสงค์เชื่อมโยง FDI ศูนย์ข้อมูล และการย้ายฐาน ห่วงโซ่อุปทาน
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้อื่น รายได้จากเงินปันผลและการบริหารจัดการ /1 (ล้านบาท) 44.4 97.0 118.2% 303.9 353.9 16.5% รายได้อื่นๆ /2 (ล้านบาท) 118.6 87.8 (25.9%) 365.7 258.9 (29.2%) รวมรายได้อื่น (ล้านบาท) 163.0 184.8 13.4% 669.6 612.8 (8.5%) /1 รายได้จากเงินปันผลและการบริหารจัดการ ไม่รวมรายได้ค่าบริหารจัดการจากกองทุนรวมและทรัสต์ และเงินปันผลจากบริษัท โกลว์ ไอพีพีจำกัด /2 รายได้อื่นๆ ประกอบด้วย ดอกเบี้ยรับ และรายได้อื่นๆ รายได้อื่น สำหรับไตรมาส 4/2568 เท่ากับ 184.8 ล้านบาท ซึ่งเพิ่มขึ้น 13.4% และปี 2568 เท่ากับ 612.8 ล้านบาท ซึ่งลดลง 8.5% จากช่วงเวลาเดียวกันของปีก่อน โดยมีสาเหตุหลักดังต่อไปนี้ - รายได้เงินปันผลและค่าบริหารจัดการ สำหรับไตรมาส 4/2568 เท่ากับ 97.0 ล้านบาท เพิ่มขึ้น 118.2% จาก ช่วงเวลาเดียวกันของปีก่

  `MDA_WHA_FY2025` · `p076` · SHA c03f6e99463c
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 4.4bn → FY2025 THB 5.1bn · +776m · +17.8%

- กำไรเพิ่มขึ้น แต่ ส่วนผสมธุรกิจ ที่ดินและการขายสินทรัพย์ อัตรากำไร ต่ำกดการแปลงรายได้เป็นกำไร ขณะที่ธุรกิจ ธุรกิจโมบิลิตี้ ระยะเริ่มต้นยังเป็นตัวฉุด
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > พลังงานไฟฟ้าที่ขายได้ - รายได้เงินปันผลรับจากบริษัท โกลว์ ไอพีพีจำกัด สำหรับปี 2568 เท่ากับ 49.7 ล้านบาท ลดลง 13.5% จากปี 2567 - ส่วนแบ่งกำไรจากการลงทุนในธุรกิจไฟฟ้าจากการดำเนินงาน (Normalized Share of Profit from Investments in Power Business) สำหรับไตรมาส 4/2568 เท่ากับ 173.9 ล้านบาท ซึ่งเพิ่มขึ้น 2.4% เมื่อเทียบกับช่วงเวลาเดียวกัน ของปีก่อน โดยมีสาเหตุหลักจากการลดลงของส่วนแบ่งขาดทุนฯใน IPP ซึ่งส่วนใหญ่เป็นผลจากอัตรากำไรด้าน พลังงาน (Energy Margin) ที่สูงขึ้น และสำหรับปี 2568 เท่ากับ 769.2 ล้านบาท ลดลง 6.3% เมื่อเทียบกับช่วงเวลา เดียวกันของปีก่อน โดยมีสาเหตุหลักจากส่วนแบ่งกำไรฯใน SPP ลดลง ซึ่งเป็นผลจากการคืนต้นทุนก๊าซ การเพิ่มขึ้น

  `MDA_WHA_FY2025` · `p073` · SHA f54fc7f9f49e
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_WHA_FY2025`

##### AMATA — ตัวแทน FDI และราคา · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท อมตะ คอร์ปอเรชัน จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนานิคมอุตสาหกรรมทั้งในประเทศและต่างประเทศ โดยมีบริษัทในกลุ่มดำเนินธุรกิจด้านสาธารณูปโภค สิ่งอำนวยความสะดวกและบริการหลังการขาย ทั้งน้ำประปา กระแสไฟฟ้า และจัดจำหน่ายก๊าซธรรมชาติ เป็นต้น

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 33.9bn | 29.50 | +77.7% | 9.2x | 22.0% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 14.7bn → FY2025 THB 14.3bn · −442m · -3.0%

- รายได้ลดประมาณ 3% จากจังหวะการโอนที่ดินล่าช้า แม้ อุปสงค์ในมือ ความต้องการนิคมอุตสาหกรรมยังดี
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > บทสรุปผู้บริหารสำหรับผลการดำเนินงานประจำปี 2568 บริษัทฯ มีรายได้รวมสำหรับปี 2568 จำนวน 14,524 ล้านบาท ลดลงร้อยละ 3.09 จากปีก่อน ซึ่งประกอบด้วย 1) รายได้การขายอสังหาริมทรัพย์ 8,703 ล้านบาท ลดลงร้อยละ 3.35 เนื่องจากการโอนที่ดินลดลงเล็กน้อยเมื่อเทียบกับ ปีก่อน โดยในปี 2568 บริษัทฯ มีการโอนกรรมสิทธิ์ที่ดินรวมทั้งสิ้นจำนวน 1,645 ไร่ (ไทย 1,493 ไร่ และเวียดนาม 152 ไร่) 2) รายได้ค่าสาธารณูปโภค 4,545 ล้านบาท ลดลงร้อยละ 4.90 จากปีก่อน สาเหตุหลักมาจากรายได้ค่าสาธารณูปโภคจาก ประเทศเวียดนามที่ลดลง และ 3) รายได้จากการให้เช่า 1,034 ล้านบาท เพิ่มขึ้นร้อยละ 9.92 จากปีก่อน เนื่องจากพื้นที่ให้เช่า ที่เพิ่มขึ้น อัตรากำไรขั้นต้นของธุรกิจหลักคิดเป็นร้อยละ 44.56 เพิ่มขึ้นเมื่อเทียบกับร้อยละ 33.74 ในปีก่อน เป็นผลจ

  `MDA_AMATA_FY2025` · `p004` · SHA c01cf1127ff9
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 2.5bn → FY2025 THB 3.1bn · +682m · +27.6%

- กำไรทำสถิติเพิ่ม 28% เพราะ ส่วนผสมธุรกิจ การโอน อัตรากำไร สูงและส่วนแบ่งกำไรจาก Amata B.Grimm Power ชดเชยฐานรายได้ที่อ่อนลง
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > หน่วย : ล้านบาท 2568 2567 เปลี่ยนแปลง ร้อยละ ค่าใช้จ่ายในการขายและต้นทุนในการจัดจำหน่าย 551 441 110 24.98 ค่าใช้จ่ายในการบริหาร 1,205 1,006 199 19.77 ขาดทุนจากอัตราแลกเปลี่ยน 131 85 46 54.03 ต้นทุนทางการเงิน 664 707 (42) (5.96) ค่าใช้จ่ายภาษีเงินได้ 884 495 389 78.44 ค่าใช้จ่ายในการขายและต้นทุนในการจัดจำหน่ายสำหรับปี 2568 อยู่ที่จำนวน 551 ล้านบาท เพิ่มขึ้น 110 ล้านบาท หรือ ร้อยละ 24.98 จากปี 2567 โดยมีค่าใช้จ่ายในการบริหารของปี 2568 จำนวน 1,205 ล้านบาท เพิ่มขึ้น 199 ล้านบาท หรือร้อยละ 19.77 มื่อเทียบกับปี 2567 บริษัทฯ มีผลขาดทุนจากอัตราแลกเปลี่ยนในปี 2568 จำนวน 131 ล้านบาท ขณะที่ปีก่อนมีผลขาดทุนจากอัตราแลกเปลี่ยน 85 ล้านบาท สาเหตุหลักจากการอ่อนค่ำของสกุลเงินเวียดนามด่งเมื่อเทียบ กับสกุลเงินด

  `MDA_AMATA_FY2025` · `p022` · SHA 80436cab4d64
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- กำไรรายงานรวมกำไรขายบริษัทย่อย 564 ลบ. และการปรับต้นทุนพัฒนาเวียดนาม 215 ลบ. จึงต้องทำ การกระทบยอดกำไรหลัก

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_AMATA_FY2025`

##### ROJNA — ตัวแปรกำไรรายงาน · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท สวนอุตสาหกรรมโรจนะ จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์ในรูปนิคมอุตสาหกรรมและธุรกิจต่อเนื่อง เช่น ธุรกิจผลิตกระแสไฟฟ้า ธุรกิจกิจผลิตน้ำเพื่ออุตสาหกรรม

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 12.3bn | 6.10 | +38.6% | 4.7x | -0.8% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 19.7bn → FY2025 THB 15.0bn · −4.7bn · -23.7%

- รายได้ลดประมาณ 25% จากการโอนที่ดินนิคมลดลง และรายได้ไฟฟ้าหดหลัง Adder โซลาร์ทยอยหมด ค่า Ft ลด และสัญญา SPP1 สิ้นสุด
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้จากการขายไฟฟ้าลดลงสาเหตุหลักจากโครงการโซลาร์ฟาร์ม3 ฟาร์มตามสัญญาAdder ทยอยหมดอายุ ตังแต่เดือนเมษายน2567 เป็นต้นไปประกอบกับค่าFT ที่ลดลงและSPP 1 สัญญาหมดอายุตังแต่เดือนตุลาคม

  `MDA_ROJNA_FY2025` · `p010` · SHA 34cf8e65833c
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 3.9bn → FY2025 −THB 125m · −4.0bn

- บริษัทพลิกเป็นขาดทุนหลักจาก มูลค่ายุติธรรม สินทรัพย์การเงินพลิกเป็นขาดทุน 1.821 พันลบ. จากกำไร 1.601 พันลบ. หรือแกว่งลบราว 3.4 พันลบ.
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไร(ขาดทุน) สุทธิส่วนของผู้ถือหุ้นบริษัทใหญ่ (125,074) 3,853,525 (103.25) ° dive dm

  `MDA_ROJNA_FY2025` · `p007` · SHA 4fa01f7ce320
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- มูลค่ายุติธรรม เป็นรายการไม่ใช่เงินสด ขณะที่การหมดสัญญาไฟฟ้าเป็นประเด็นดำเนินงานเชิงโครงสร้าง
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ขายซึงเป็นหลักทรัพย์ในความต้องการของตลาดแสดงตามมูลค่ายุติธรรม

  `MDA_ROJNA_FY2025` · `p013` · SHA eb68a30e8fa5
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_ROJNA_FY2025`

##### PIN — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ปิ่นทอง อินดัสเตรียล ปาร์ค จำกัด (มหาชน)** — รายได้และกำไรเคลื่อนไหวสอดคล้องกัน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ประกอบธุรกิจพัฒนาและบริหารจัดการนิคมอุตสาหกรรม พร้อมระบบสาธารณูปโภค สิ่งอำนวยความสะดวกและพื้นที่พาณิชยกรรม และประกอบธุรกิจพัฒนาอสังหาริมทรัพย์ ประเภทอาคารโรงงานและคลังสินค้าเพื่อเช่าและขายสำหรับ ผู้ประกอบการอุตสาหกรรม รวมถึงลงทุนและได้รับแต่งตั้งเป็นผู้บริหารอสังหาริมทรัพย์ ของกองทุนรวมสิทธิการเช่าอสังหาริมทรัพย์ (AIMIRT)

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 5.4bn | 4.68 | +10.4% | 7.9x | 38.5% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 20 · NPAT 20 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 4.2bn → FY2025 THB 1.3bn · −2.9bn · -69.0%

- RFO ปี 2568 อยู่ที่ 1,290 ลบ. ลด 69.0% YoY; MD&A ระบุว่า Executive Summary • ในไตรมาส4 ปี2568 บริษัทปิ่นทองอินดัสเตรียลปาร์คจำกัด(มหาชน) (“บริษัทฯ”) มีรายได้จากการดำเนินงานจำนวน100.6 ล้านบาท เนื่องจากไม่มีการโอนที่ดินในไตรมาสนี้อย่างไรก็ตามรายได้ประจำของบริษัทฯยังคงเติบโตต่อเนื่องโดยรายได้จากการให้เช่าและบริการที่ เพิ่มขึ้น 14.1% QoQ และ69.9% YoY ขณะที่รายได้จากระบบสาธารณูปโภคเพิ่มขึ้น9.9% QoQ และ 38.5% YoY สะท้อนจากอัตราการเช่า
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > Executive Summary • ในไตรมาส4 ปี2568 บริษัทปิ่นทองอินดัสเตรียลปาร์คจำกัด(มหาชน) (“บริษัทฯ”) มีรายได้จากการดำเนินงานจำนวน100.6 ล้านบาท เนื่องจากไม่มีการโอนที่ดินในไตรมาสนี้อย่างไรก็ตามรายได้ประจำของบริษัทฯยังคงเติบโตต่อเนื่องโดยรายได้จากการให้เช่าและบริการที่ เพิ่มขึ้น 14.1% QoQ และ69.9% YoY ขณะที่รายได้จากระบบสาธารณูปโภคเพิ่มขึ้น9.9% QoQ และ 38.5% YoY สะท้อนจากอัตราการเช่า

  `MDA_PIN_FY2025` · `p002` · SHA 24eb779545e4
  </details>
- RFO ปี 2568 อยู่ที่ 1,290 ลบ. ลด 69.0% YoY; MD&A ระบุว่า อสังหาริมทรัพย์ รายได้จากการให้เช่าและบริการ 16.5 24.6 28.1 69.9% 14.1% 66.4 92.9 39.9% รายได้ค่าสาธารณูปโภค 52.3 66.0 72.5 38.5% 9.9% 199.9 267.2 33.7% รวมรายได้จากการดำเนินงาน 1,113.5 174.9 100.6 (91.0%) (42.5%) 4,167.4 1,290.4 (69.0%) รายได้อื่น (4.4) 12.7 299.6 (6,867.6%) 2,250.4% 97.6 336.4 244.7% รวมรายได้ 1,109.1 187.6 400.2 (63.9%) 113.3% 4,265.0 1,626.8 (61.9%)
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > อสังหาริมทรัพย์ รายได้จากการให้เช่าและบริการ 16.5 24.6 28.1 69.9% 14.1% 66.4 92.9 39.9% รายได้ค่าสาธารณูปโภค 52.3 66.0 72.5 38.5% 9.9% 199.9 267.2 33.7% รวมรายได้จากการดำเนินงาน 1,113.5 174.9 100.6 (91.0%) (42.5%) 4,167.4 1,290.4 (69.0%) รายได้อื่น (4.4) 12.7 299.6 (6,867.6%) 2,250.4% 97.6 336.4 244.7% รวมรายได้ 1,109.1 187.6 400.2 (63.9%) 113.3% 4,265.0 1,626.8 (61.9%)

  `MDA_PIN_FY2025` · `p041` · SHA 7afdc40bbf49
  </details>
- RFO ปี 2568 อยู่ที่ 1,290 ลบ. ลด 69.0% YoY; MD&A ระบุว่า ในหมวดนี้เติบโตอย่างต่อเนื่อง Q4/2568: บริษัทฯ มีรายได้จากการดำเนินงาน จำนวน 100.6 ล้าน • รายได้อื่น บริษัทฯ มีรายได้อื่นจำนวน 299.6 ล้านบาทบาท ลดลง 42.5% QoQ และลดลง 91.0% YoY สาเหตุการลดลง เพิ่มขึ้น 2,250.4% QoQ และ 6,867.6% YoY จากการรับรู้ประกอบด้วย 3 ส่วนหลัก ได้แก่
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ในหมวดนี้เติบโตอย่างต่อเนื่อง Q4/2568: บริษัทฯ มีรายได้จากการดำเนินงาน จำนวน 100.6 ล้าน • รายได้อื่น บริษัทฯ มีรายได้อื่นจำนวน 299.6 ล้านบาทบาท ลดลง 42.5% QoQ และลดลง 91.0% YoY สาเหตุการลดลง เพิ่มขึ้น 2,250.4% QoQ และ 6,867.6% YoY จากการรับรู้ประกอบด้วย 3 ส่วนหลัก ได้แก่

  `MDA_PIN_FY2025` · `p036` · SHA 6c12531ccc57
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 1.7bn → FY2025 THB 497m · −1.2bn · -71.3%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 497 ลบ. ลด 71.3% YoY; MD&A ระบุว่า รายละเอียด Q4/67 Q3/68 Q4/68 เปลี่ยนแปลง%YoY เปลี่ยนแปลง%QoQ FY/67 FY/68 เปลี่ยนแปลง%YoY EBITDA (หน่วย: ล้านบาท) 477.9 104.3 307.8 (35.6%) 195.2% 1,944.2 769.1 (60.4%) EBITDA อัตรากำไร (%) 43.1% 55.6% 76.9% 45.6% 47.3% กำไรสุทธิ (หน่วย: ล้านบาท) 385.9 56.3 212.2 (45.0%) 276.6% 1,733.7 497.3 (71.3%) อัตรากำไรสุทธิ (%) 34.8% 30.0% 53.1% 40.7% 30.6% กำไรสุทธิต่อหุ้น (บาท) 0.33 0.05 0.18 (45.5%) 260.0% 1.49 0.43 (71.3%) Q4/2568: บริษัทฯ มีกำไรสุทธิจำนวน 212.2 ล้านบาท เพิ่มขึ้น 276.6% QoQ แต่ลดลง 45.0% YoY โดยการปรับตัวเพิ่มขึ้นเมื่อเทียบกับ ไตรมาสก่อนหน้ามาจากก
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายละเอียด Q4/67 Q3/68 Q4/68 เปลี่ยนแปลง%YoY เปลี่ยนแปลง%QoQ FY/67 FY/68 เปลี่ยนแปลง%YoY EBITDA (หน่วย: ล้านบาท) 477.9 104.3 307.8 (35.6%) 195.2% 1,944.2 769.1 (60.4%) EBITDA Margin (%) 43.1% 55.6% 76.9% 45.6% 47.3% กำไรสุทธิ (หน่วย: ล้านบาท) 385.9 56.3 212.2 (45.0%) 276.6% 1,733.7 497.3 (71.3%) อัตรากำไรสุทธิ (%) 34.8% 30.0% 53.1% 40.7% 30.6% กำไรสุทธิต่อหุ้น (บาท) 0.33 0.05 0.18 (45.5%) 260.0% 1.49 0.43 (71.3%) Q4/2568: บริษัทฯ มีกำไรสุทธิจำนวน 212.2 ล้านบาท เพิ่มขึ้น 276.6% QoQ แต่ลดลง 45.0% YoY โดยการปรับตัวเพิ่มขึ้นเมื่อเทียบกับ ไตรมาสก่อนหน้ามาจากการรับรู้รายได้อื่นจากกำไรจากสินทรัพย์ที่ถือไว้เพื่อขาย (ขายโรงงานเช่า) ขณะที่เมื่อเทียบกับช่วงเดียวกันของปี

  `MDA_PIN_FY2025` · `p054` · SHA b19c9f1fb7d7
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 497 ลบ. ลด 71.3% YoY; MD&A ระบุว่า ภาพรวมผลการดำเนินงาน ภาพรวมผลการดำเนินงาน เปลี่ยนแปลง เปลี่ยนแปลง เปลี่ยนแปลง Q4/67 Q3/68 Q4/68 %YoY %QoQ FY/67 FY/68 %YoY (หน่วย : ล้านบาท) รายได้จากการดำเนินงาน 1,113.5 174.9 100.6 (91.0%) (42.5%) 4,167.4 1,290.4 (69.0%) กำไรขั้นต้น 535.8 84.1 28.9 (94.6%) (65.6%) 2,029.4 538.7 (73.5%) EBITDA 477.9 104.3 307.8 (35.6%) 195.2% 1,944.2 769.1 (60.4%) กำไร (ขาดทุน) สุทธิ 385.9 56.3 212.2 (45.0%) 276.6% 1,733.7 497.3 (71.3%) อัตรากำไรขั้นต้น (%) 48.1% 48.1% 28.8% (40.2%) (40.2%) 48.7% 41.8% (14.3%) อัตรา EBITDA (%) 43.1% 55.6% 76.9% 78.5% 38.4% 45.6% 47.3% 3
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ภาพรวมผลการดำเนินงาน ภาพรวมผลการดำเนินงาน เปลี่ยนแปลง เปลี่ยนแปลง เปลี่ยนแปลง Q4/67 Q3/68 Q4/68 %YoY %QoQ FY/67 FY/68 %YoY (หน่วย : ล้านบาท) รายได้จากการดำเนินงาน 1,113.5 174.9 100.6 (91.0%) (42.5%) 4,167.4 1,290.4 (69.0%) กำไรขั้นต้น 535.8 84.1 28.9 (94.6%) (65.6%) 2,029.4 538.7 (73.5%) EBITDA 477.9 104.3 307.8 (35.6%) 195.2% 1,944.2 769.1 (60.4%) กำไร (ขาดทุน) สุทธิ 385.9 56.3 212.2 (45.0%) 276.6% 1,733.7 497.3 (71.3%) อัตรากำไรขั้นต้น (%) 48.1% 48.1% 28.8% (40.2%) (40.2%) 48.7% 41.8% (14.3%) อัตรา EBITDA (%) 43.1% 55.6% 76.9% 78.5% 38.4% 45.6% 47.3% 3.7% อัตรากำไร (ขาดทุน) สุทธิ(%) 34.8% 30.0% 53.0% 52.4% 76.6% 40.7% 30.6% (24.8%)

  `MDA_PIN_FY2025` · `p005` · SHA db54e97f8e96
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 497 ลบ. ลด 71.3% YoY; MD&A ระบุว่า Q4/67 Q3/68 Q4/68 %YoY %QoQ FY/67 FY/68 %YoY (หน่วย: ล้านบาท) 529.4 27.4 0.0 (100.0%) (100.0%) 1,944.1 486.3 (75.0%) ต้นทุนจากการขายอสังหาริมทรัพย์ 9.0 15.2 15.2 68.2% 0.3% 21.7 58.5 169.3% ต้นทุนจากการให้เช่าและบริการ ต้นทุนค่าสาธารณูปโภค 39.2 48.3 56.4 44.2% 16.9% 172.2 206.9 20.2% ค่าใช้จ่ายในการขาย 18.1 4.5 7.7 (57.5%) 69.9% 57.7 42.3 (26.7%) ค่าใช้จ่ายในการบริหาร 60.1 17.0 47.8 (20.4%) 181.4% 178.1 182.9 2.7% ต้นทุนทางการเงิน (สุทธิ) 5.8 5.2 4.8 (16.6%) (7.5%) 18.8 19.6 4.1% ภาษีเงินได้ 61.6 13.8 56.1 (8.9%) 306.5% 111.4 133.0 19.4% รวมต้นทุนและค่าใ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > Q4/67 Q3/68 Q4/68 %YoY %QoQ FY/67 FY/68 %YoY (หน่วย: ล้านบาท) 529.4 27.4 0.0 (100.0%) (100.0%) 1,944.1 486.3 (75.0%) ต้นทุนจากการขายอสังหาริมทรัพย์ 9.0 15.2 15.2 68.2% 0.3% 21.7 58.5 169.3% ต้นทุนจากการให้เช่าและบริการ ต้นทุนค่าสาธารณูปโภค 39.2 48.3 56.4 44.2% 16.9% 172.2 206.9 20.2% ค่าใช้จ่ายในการขาย 18.1 4.5 7.7 (57.5%) 69.9% 57.7 42.3 (26.7%) ค่าใช้จ่ายในการบริหาร 60.1 17.0 47.8 (20.4%) 181.4% 178.1 182.9 2.7% ต้นทุนทางการเงิน (สุทธิ) 5.8 5.2 4.8 (16.6%) (7.5%) 18.8 19.6 4.1% ภาษีเงินได้ 61.6 13.8 56.1 (8.9%) 306.5% 111.4 133.0 19.4% รวมต้นทุนและค่าใช้จ่าย 723.1 131.3 188.0 (74.0%) 43.2% 2,531.2 1,129.5 (55.4%)

  `MDA_PIN_FY2025` · `p050` · SHA 77725366ae8a
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 497 ลบ. ลด 71.3% YoY; MD&A ระบุว่า ภาษีเงินได้ รายได้ (ค่าใช้จ่าย) ภาษีเงินได้ 61.6 13.8 56.1 (8.9%) 306.5% 111.4 133.0 19.4% กำไร (ขาดทุน) สุทธิ 385.9 56.3 212.2 (45.0%) 276.6% 1,733.7 497.3 (71.3%) กำไรขาดทุนสุทธิต่อหุ้น (บาท) 0.33 0.05 0.18 (45.5%) 260.0% 1.49 0.43 (71.3%)
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ภาษีเงินได้ รายได้ (ค่าใช้จ่าย) ภาษีเงินได้ 61.6 13.8 56.1 (8.9%) 306.5% 111.4 133.0 19.4% กำไร (ขาดทุน) สุทธิ 385.9 56.3 212.2 (45.0%) 276.6% 1,733.7 497.3 (71.3%) กำไรขาดทุนสุทธิต่อหุ้น (บาท) 0.33 0.05 0.18 (45.5%) 260.0% 1.49 0.43 (71.3%)

  `MDA_PIN_FY2025` · `p030` · SHA 8d7e5f4af873
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ค่าใช้จ่ายในการขายและการบริหาร Q4/2568: บริษัทฯมีค่าใช้จ่ายในการขายและบริหารรวม 55.5 ล้านบาท เพิ่มขึ้น 34.0 ล้านบาท หรือ 157.9% QoQ แต่ลดลง 22.7 ล้าน บาท หรือ 29.0% YoY เนื่องจากบริษัทมีค่าใช้จ่ายในการขายและค่าใช้จ่ายในการบริหารเพิ่มขึ้นตามกิจกรรมการดำเนินงานที่สูงขึ้นเมื่อ เทียบกับไตรมาสก่อนหน้า ขณะที่เมื่อเทียบกับช่วงเดียวกันของปีก่อนบริษัทมีค่าใช้จ่ายในการขายและบริหารลดลงจากการที่ในไตรมาส 4/2567 บริษัทฯ รับรู้ขาดทุนจากการวัดมูลค่ายุติธรรมของเงินลงทุนจำนวน 17.8 ล้านบาท แต่ในไตรมาสนี้ไม่มีการรับรู้รายการดังกล่าว
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ค่าใช้จ่ายในการขายและการบริหาร Q4/2568: บริษัทฯมีค่าใช้จ่ายในการขายและบริหารรวม 55.5 ล้านบาท เพิ่มขึ้น 34.0 ล้านบาท หรือ 157.9% QoQ แต่ลดลง 22.7 ล้าน บาท หรือ 29.0% YoY เนื่องจากบริษัทมีค่าใช้จ่ายในการขายและค่าใช้จ่ายในการบริหารเพิ่มขึ้นตามกิจกรรมการดำเนินงานที่สูงขึ้นเมื่อ เทียบกับไตรมาสก่อนหน้า ขณะที่เมื่อเทียบกับช่วงเดียวกันของปีก่อนบริษัทมีค่าใช้จ่ายในการขายและบริหารลดลงจากการที่ในไตรมาส 4/2567 บริษัทฯ รับรู้ขาดทุนจากการวัดมูลค่ายุติธรรมของเงินลงทุนจำนวน 17.8 ล้านบาท แต่ในไตรมาสนี้ไม่มีการรับรู้รายการดังกล่าว

  `MDA_PIN_FY2025` · `p052` · SHA 41f107d5ba5e
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_PIN_FY2025`

##### NNCL — บริษัทในกลุ่ม · ทบทวนปกติ

**บริษัท นวนคร จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาโครงการอสังหาริมทรัพย์และเขตอุตสาหกรรมเพื่อขายและให้เช่า และการให้บริการสาธารณูปโภคและสิ่งอำนวยความสะดวกต่าง ๆ ในเขตอุตสาหกรรม

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 3.7bn | 1.80 | +20.0% | 13.3x | 34.7% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 9 · NPAT 3 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 864m → FY2025 THB 884m · +20m · +2.4%

- RFO ปี 2568 อยู่ที่ 884 ลบ. เพิ่ม 2.4% YoY; MD&A ระบุว่า สรุปข้อมูลทางการเงินที่สำคัญ 1. รายได้จากการขายโครงการพัฒนาอสังหาริมทรัพย์รายได้จากการให้บริการรายได้ค่าเช่าและรายได้อื่น
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > สรุปข้อมูลทางการเงินที่สำคัญ 1. รายได้จากการขายโครงการพัฒนาอสังหาริมทรัพย์รายได้จากการให้บริการรายได้ค่าเช่าและรายได้อื่น

  `MDA_NNCL_FY2025` · `p001` · SHA 16221018ee17
  </details>
- RFO ปี 2568 อยู่ที่ 884 ลบ. เพิ่ม 2.4% YoY; MD&A ระบุว่า ยที่ดินอยู่ที่131 ล้านบาทเพิ่มขึ้นร้อยละ25 ส่วนของกลุ่มรายได้อื่นสำหรับปีสิ้นสุดวันที่31 ธันวาคม2568 ประกอบด้วยรายได้เงินอุดหนุนรัฐบาล จำนวน21.6 ล้านบาท เปรียบเทียบกับงวดเดียวกันปี2567รับรู้รายได้จำนวน23.2 ล้านบาทลดลงจำนวน1.6 ล้านบาท
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ยที่ดินอยู่ที่131 ล้านบาทเพิ่มขึ้นร้อยละ25 ส่วนของกลุ่มรายได้อื่นสำหรับปีสิ้นสุดวันที่31 ธันวาคม2568 ประกอบด้วยรายได้เงินอุดหนุนรัฐบาล จำนวน21.6 ล้านบาท เปรียบเทียบกับงวดเดียวกันปี2567รับรู้รายได้จำนวน23.2 ล้านบาทลดลงจำนวน1.6 ล้านบาท

  `MDA_NNCL_FY2025` · `p008` · SHA 5a5a66866e1e
  </details>
- RFO ปี 2568 อยู่ที่ 884 ลบ. เพิ่ม 2.4% YoY; MD&A ระบุว่า เปรียบเทียบปี2568 กับปี2567 ©) บริษัทฯมีรายได้จากการให้บริการและรายได้ค่าเช่าเป็นรายได้ประจำ(:๐๕นหหก6 income) สำหรับปีสิ้นสุด วันที่31 ธันวาคม2568 จำนวนเงิน718.9 ล้ านบาทเปรียบเทียบกับงวดเดียวกันปี2567 จำนวนเงิน736.5 ล้านบาท ลดลง17.6 ล้านบาท
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > เปรียบเทียบปี2568 กับปี2567 ©) บริษัทฯมีรายได้จากการให้บริการและรายได้ค่าเช่าเป็นรายได้ประจำ(:๐๕นหหก6 income) สำหรับปีสิ้นสุด วันที่31 ธันวาคม2568 จำนวนเงิน718.9 ล้ านบาทเปรียบเทียบกับงวดเดียวกันปี2567 จำนวนเงิน736.5 ล้านบาท ลดลง17.6 ล้านบาท

  `MDA_NNCL_FY2025` · `p002` · SHA 1fe5d911f445
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 396m → FY2025 THB 307m · −89m · -22.4%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 307 ลบ. ลด 22.4% YoY; MD&A ระบุว่า ๑ต้นทุนบริการปรับเพิ่มเล็กน้อยตามการบำรุงรักษาสินทรัพย์ทำให้กำไรขั้นต้นลดลงบางส่วน ๑ต้นทุนขายโครงการพัฒนาอสังหาริมทรัพย์อยู่ที่34.9 ล้านบาทโดยกำไรขั้นต้นเพิ่มขึ้น25% จาก
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ๑ต้นทุนบริการปรับเพิ่มเล็กน้อยตามการบำรุงรักษาสินทรัพย์ทำให้กำไรขั้นต้นลดลงบางส่วน ๑ต้นทุนขายโครงการพัฒนาอสังหาริมทรัพย์อยู่ที่34.9 ล้านบาทโดยกำไรขั้นต้นเพิ่มขึ้น25% จาก

  `MDA_NNCL_FY2025` · `p013` · SHA 2314f0e88920
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 307 ลบ. ลด 22.4% YoY; MD&A ระบุว่า ดทุน) จากการร่วมคำ ๑ปี2568บริษัทรับรู้ขาดทุน3.9 ล้านบาทเทียบกับกำไร75.7 ล้านบาทในปีที่ผ่านมาปัจจั
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ดทุน) จากการร่วมคำ ๑ปี2568บริษัทรับรู้ขาดทุน3.9 ล้านบาทเทียบกับกำไร75.7 ล้านบาทในปีที่ผ่านมาปัจจั

  `MDA_NNCL_FY2025` · `p015` · SHA 4e60c1332f0d
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 307 ลบ. ลด 22.4% YoY; MD&A ระบุว่า ๑ค่าเสื่อม ราคาเพิ่มขึ้นตามการใช้สินทรัพย์ที่ใช้งานขณะที่ต้นทุนทางการเงินอยู่ที่1.2
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ๑ค่าเสื่อม ราคาเพิ่มขึ้นตามการใช้สินทรัพย์ที่ใช้งานขณะที่ต้นทุนทางการเงินอยู่ที่1.2

  `MDA_NNCL_FY2025` · `p016` · SHA 6fa99c52da8b
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_NNCL_FY2025`

##### AMATAV — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท อมตะ วีเอ็น จำกัด (มหาชน)** — กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัท อมตะ วีเอ็น จำกัด (มหาชน) ประกอบธุรกิจการลงทุนในบริษัทอื่น (Holding Company)

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 2.2bn | 2.08 | +15.6% | 4.9x | 11.6% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 10 · NPAT 11 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 5.3bn → FY2025 THB 4.0bn · −1.3bn · -25.4%

- RFO ปี 2568 อยู่ที่ 3,956 ลบ. ลด 25.4% YoY; MD&A ระบุว่า หน่วย: ล้านบาท ปี 2568 เปลี่ยนแปลง ร้อยละ (ปรับปรุงใหม่) รายได้จากการขายอสังหาริมทรัพย์ 1,417.94 2,397.41 (979.47) (40.86) รายได้ค่าสาธารณูปโภค 2,512.05 2,880.30 (368.25) (12.78) รายได้จากการให้เช่า 26.01 26.96 (0.95) (3.54) รายได้ทางการเงิน 52.92 53.55 (0.63) (1.17) รายได้อื่น 13.68 21.18 (7.50) (35.42) รวมรายได้ 4,022.60 5,379.40 (1,356.80) (25.22)
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > หน่วย: ล้านบาท ปี 2568 เปลี่ยนแปลง ร้อยละ (ปรับปรุงใหม่) รายได้จากการขายอสังหาริมทรัพย์ 1,417.94 2,397.41 (979.47) (40.86) รายได้ค่าสาธารณูปโภค 2,512.05 2,880.30 (368.25) (12.78) รายได้จากการให้เช่า 26.01 26.96 (0.95) (3.54) รายได้ทางการเงิน 52.92 53.55 (0.63) (1.17) รายได้อื่น 13.68 21.18 (7.50) (35.42) รวมรายได้ 4,022.60 5,379.40 (1,356.80) (25.22)

  `MDA_AMATAV_FY2025` · `p013` · SHA 1d8f7af9b9bb
  </details>
- RFO ปี 2568 อยู่ที่ 3,956 ลบ. ลด 25.4% YoY; MD&A ระบุว่า รายได้ค่าสาธารณูปโภค รายได้ค่าสาธารณูปโภคสำหรับปี 2568 เท่ากับ 2,512.05 ลดลงจาก 2,880.30 ล้านบาท ในปี 2567 หรือ ปรับตัว ลดลงร้อยละ 12.78 สาเหตุหลักมาจากลูกค้ามีการใช้สาธารณูปโภคจาก ACHL ที่ปรับตัวลดลง 412.01 ล้านบาท หรือลดลง ร้อยละ 15.58 จากช่วงเดียวกันของปีก่อน อย่างไรก็ตาม การปรับตัวลดลงดังกล่าวมีแนวโน้มที่ดีขึ้นในไตรมาส 4/2568
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้ค่าสาธารณูปโภค รายได้ค่าสาธารณูปโภคสำหรับปี 2568 เท่ากับ 2,512.05 ลดลงจาก 2,880.30 ล้านบาท ในปี 2567 หรือ ปรับตัว ลดลงร้อยละ 12.78 สาเหตุหลักมาจากลูกค้ามีการใช้สาธารณูปโภคจาก ACHL ที่ปรับตัวลดลง 412.01 ล้านบาท หรือลดลง ร้อยละ 15.58 จากช่วงเดียวกันของปีก่อน อย่างไรก็ตาม การปรับตัวลดลงดังกล่าวมีแนวโน้มที่ดีขึ้นในไตรมาส 4/2568

  `MDA_AMATAV_FY2025` · `p015` · SHA 1ef7a8a50727
  </details>
- RFO ปี 2568 อยู่ที่ 3,956 ลบ. ลด 25.4% YoY; MD&A ระบุว่า รายได้จากการขายอสังหาริมทรัพย์ รายได้จากการขายอสังหาริมทรัพย์สำหรับปี 2568 เท่ากับ 1,417.94 ล้านบาท ลดลงจากงวดเดียวกันของปีก่อน 979.47 ล้านบาท หรือลดลงร้อยละ 40.86 ซึ่งประกอบด้วยรายได้จากการขายอสังหาริมทรัพย์จากนิคม อมตะซิตี้ฮาลอง (“ACHL”) คิดเป็นพื้นที่ 6.4 เฮกตาร์ และนิคม อมตะซิตี้ลองถั่น (“ACLT”) คิดเป็นพื้นที่ 17.9 เฮกตาร์ รวมเป็น 24.3 เฮกตาร์ ซึ่งลงลงจาก 75.0 เฮกตาร์ ในปี 2567
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้จากการขายอสังหาริมทรัพย์ รายได้จากการขายอสังหาริมทรัพย์สำหรับปี 2568 เท่ากับ 1,417.94 ล้านบาท ลดลงจากงวดเดียวกันของปีก่อน 979.47 ล้านบาท หรือลดลงร้อยละ 40.86 ซึ่งประกอบด้วยรายได้จากการขายอสังหาริมทรัพย์จากนิคม อมตะซิตี้ฮาลอง (“ACHL”) คิดเป็นพื้นที่ 6.4 เฮกตาร์ และนิคม อมตะซิตี้ลองถั่น (“ACLT”) คิดเป็นพื้นที่ 17.9 เฮกตาร์ รวมเป็น 24.3 เฮกตาร์ ซึ่งลงลงจาก 75.0 เฮกตาร์ ในปี 2567

  `MDA_AMATAV_FY2025` · `p014` · SHA 2c486dece437
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 76m → FY2025 THB 460m · +384m · +507.1%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 460 ลบ. เพิ่ม 507.1% YoY; MD&A ระบุว่า รายได้จากการขายอสังหาริมทรัพย์สำหรับปี 2568 มีกำไรขั้นต้น 945.58 ล้านบาท หรืออัตรากำไรขั้นต้นร้อยละ 66.69 เพิ่มขึ้นจากปี 2567 ที่มีอัตรากำไรขั้นต้นร้อยละ 21.71 เนื่องจาก ACHL ได้ทำการปรับปรุงขนาดพื้นที่ที่ใช้ในการคำนวณต้นทุน การพัฒนาอสังหาริมทรัพย์ของทั้งโครงการ โดยหักพื้นที่ถนน 6 เลน ออกจากพื้นที่ที่เคยคำนวณไว้ เนื่องจากรัฐบาลจะเป็น ผู้รับผิดชอบในการก่อสร้างถนนดังกล่าว ส่งผลให้ต้นทุนในการพัฒนาอสังหาริมทรัพย์ที่เคยขายไปในอดีตลดลง 215 ล้านบาท ทั้งนี้หากไม่รวมผลจากรายการดังกล่าว อัตรากำไรขั้นต้นจากการขายอสังหาริมทรัพย์ยังคงเพิ่มขึ้นจากปีก่อน เนื่องราคาขายท
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้จากการขายอสังหาริมทรัพย์สำหรับปี 2568 มีกำไรขั้นต้น 945.58 ล้านบาท หรืออัตรากำไรขั้นต้นร้อยละ 66.69 เพิ่มขึ้นจากปี 2567 ที่มีอัตรากำไรขั้นต้นร้อยละ 21.71 เนื่องจาก ACHL ได้ทำการปรับปรุงขนาดพื้นที่ที่ใช้ในการคำนวณต้นทุน การพัฒนาอสังหาริมทรัพย์ของทั้งโครงการ โดยหักพื้นที่ถนน 6 เลน ออกจากพื้นที่ที่เคยคำนวณไว้ เนื่องจากรัฐบาลจะเป็น ผู้รับผิดชอบในการก่อสร้างถนนดังกล่าว ส่งผลให้ต้นทุนในการพัฒนาอสังหาริมทรัพย์ที่เคยขายไปในอดีตลดลง 215 ล้านบาท ทั้งนี้หากไม่รวมผลจากรายการดังกล่าว อัตรากำไรขั้นต้นจากการขายอสังหาริมทรัพย์ยังคงเพิ่มขึ้นจากปีก่อน เนื่องราคาขายที่ นิคม ACHL ที่ปรับเพิ่มสูงขึ้น ประกอบกับการบริหารจัดการต้นทุนที่มีประสิทธิภาพทำให้ต้นทุนในการขายโดยเฉลี่ยต่อเฮกตาร์

  `MDA_AMATAV_FY2025` · `p020` · SHA a1699e817d97
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 460 ลบ. เพิ่ม 507.1% YoY; MD&A ระบุว่า กำไรสุทธิ บริษัทฯ มีกำไรสุทธิตามงบการเงินรวมสำหรับปี 2568 จำนวน 530.68 ล้านบาท เพิ่มขึ้นจากช่วงเดียวกันของปีก่อน 424.02 ล้านบาท หรือเพิ่มขึ้นร้อยละ 397.53 โดยหลักมาจากการปรับปรุงขนาดพื้นที่ที่ใช้ในการคำนวณต้นทุนการพัฒนา อสังหาริมทรัพย์ของ ACHL ประกอบกับอัตรากำไรขั้นต้นจากธุรกิจอสังหาริมทรัพย์ที่ปรับดีขึ้นเนื่องจากการบริหารจัดการ ต้นทุนอย่างมีประสิทธิภาพ ค่าใช้จ่ายในการขายและบริหารที่ลดลง และส่วนแบ่งกำไรจากบริษัทร่วมที่เพิ่มขึ้น โดยบริษัทฯ มีกำไรสุทธิส่วนที่เป็นของผู้ถือหุ้นสำหรับปี 2568 จำนวน 459.85 ล้านบาท หรือคิดเป็น 0.43 บาทต่อหุ้น
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไรสุทธิ บริษัทฯ มีกำไรสุทธิตามงบการเงินรวมสำหรับปี 2568 จำนวน 530.68 ล้านบาท เพิ่มขึ้นจากช่วงเดียวกันของปีก่อน 424.02 ล้านบาท หรือเพิ่มขึ้นร้อยละ 397.53 โดยหลักมาจากการปรับปรุงขนาดพื้นที่ที่ใช้ในการคำนวณต้นทุนการพัฒนา อสังหาริมทรัพย์ของ ACHL ประกอบกับอัตรากำไรขั้นต้นจากธุรกิจอสังหาริมทรัพย์ที่ปรับดีขึ้นเนื่องจากการบริหารจัดการ ต้นทุนอย่างมีประสิทธิภาพ ค่าใช้จ่ายในการขายและบริหารที่ลดลง และส่วนแบ่งกำไรจากบริษัทร่วมที่เพิ่มขึ้น โดยบริษัทฯ มีกำไรสุทธิส่วนที่เป็นของผู้ถือหุ้นสำหรับปี 2568 จำนวน 459.85 ล้านบาท หรือคิดเป็น 0.43 บาทต่อหุ้น

  `MDA_AMATAV_FY2025` · `p025` · SHA 4cd9e19f3374
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 460 ลบ. เพิ่ม 507.1% YoY; MD&A ระบุว่า ปี 2567 หน่วย: ล้านบาท ปี 2568 เปลี่ยนแปลง ร้อยละ (ปรับปรุงใหม่) รายได้จากการขายอสังหาริมทรัพย์ 1,417.94 2,397.41 (979.47) (40.86) ต้นทุนจากการขายอสังหาริมทรัพย์ 472.36 1,877.01 (1,404.65) (74.83) กำไรขั้นต้น 945.58 520.40 425.18 81.70 อัตรากำไรขั้นต้น (ร้อยละ) 66.69 21.71 รายได้ค่าสาธารณูปโภค 2,512.05 2,880.30 (368.25) (12.78) ต้นทุนบริการสาธารณูปโภค 2,314.05 2,651.30 (337.25) (12.72) กำไรขันต้น 198.00 229.00 (31.00) (13.54) อัตรากำไรขั้นต้น (ร้อยละ) 7.88 7.95 รายได้จากการให้เช่า 26.01 26.96 (0.95) (3.54) ต้นทุนจากการให้เช่า 10.88 13.68 (2.80) (20.48) ก
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ปี 2567 หน่วย: ล้านบาท ปี 2568 เปลี่ยนแปลง ร้อยละ (ปรับปรุงใหม่) รายได้จากการขายอสังหาริมทรัพย์ 1,417.94 2,397.41 (979.47) (40.86) ต้นทุนจากการขายอสังหาริมทรัพย์ 472.36 1,877.01 (1,404.65) (74.83) กำไรขั้นต้น 945.58 520.40 425.18 81.70 อัตรากำไรขั้นต้น (ร้อยละ) 66.69 21.71 รายได้ค่าสาธารณูปโภค 2,512.05 2,880.30 (368.25) (12.78) ต้นทุนบริการสาธารณูปโภค 2,314.05 2,651.30 (337.25) (12.72) กำไรขันต้น 198.00 229.00 (31.00) (13.54) อัตรากำไรขั้นต้น (ร้อยละ) 7.88 7.95 รายได้จากการให้เช่า 26.01 26.96 (0.95) (3.54) ต้นทุนจากการให้เช่า 10.88 13.68 (2.80) (20.48) กำไรขั้นต้น 15.13 13.28 1.85 13.91 อัตรากำไรขั้นต้น (ร้อยละ) 58.17 49.27

  `MDA_AMATAV_FY2025` · `p019` · SHA 3a51427a7c75
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 460 ลบ. เพิ่ม 507.1% YoY; MD&A ระบุว่า ของทั้งนิคม ACHL และ ACLT ปรับลดลง รายได้ค่าสาธารณูปโภคสำหรับปี 2568 มีกำไรขั้นต้น 198.00 ล้านบาท ลดลง 31.00 ล้านบาท หรือลดลงร้อยละ 13.54 มีอัตรากำไรขั้นต้นอยู่ที่ร้อยละ 7.88 ลดลงจากปี 2567 เล็กน้อยที่มีอัตรากำไรขั้นต้นร้อยละ 7.95 รายได้จากการให้เช่าสำหรับปี 2568 มีกำไรขั้นต้นอยู่ที่ 15.13 ล้านบาท หรืออัตรากำไรขั้นต้นร้อยละ 58.17 ปรับตัว เพิ่มขึ้นจากปีก่อน ที่มีอัตรากำไรขั้นต้นอยู่ที่ร้อยละ 49.27
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ของทั้งนิคม ACHL และ ACLT ปรับลดลง รายได้ค่าสาธารณูปโภคสำหรับปี 2568 มีกำไรขั้นต้น 198.00 ล้านบาท ลดลง 31.00 ล้านบาท หรือลดลงร้อยละ 13.54 มีอัตรากำไรขั้นต้นอยู่ที่ร้อยละ 7.88 ลดลงจากปี 2567 เล็กน้อยที่มีอัตรากำไรขั้นต้นร้อยละ 7.95 รายได้จากการให้เช่าสำหรับปี 2568 มีกำไรขั้นต้นอยู่ที่ 15.13 ล้านบาท หรืออัตรากำไรขั้นต้นร้อยละ 58.17 ปรับตัว เพิ่มขึ้นจากปีก่อน ที่มีอัตรากำไรขั้นต้นอยู่ที่ร้อยละ 49.27

  `MDA_AMATAV_FY2025` · `p021` · SHA 6f8476cf64fb
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_AMATAV_FY2025`

##### MK — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท มั่นคงเคหะการ จำกัด (มหาชน)** — อยู่ในภาวะฟื้นตัว; อัตราเติบโตมีความสำคัญรองลงมา

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์เพื่อขาย เพื่อการให้เช่าและบริการ

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 840m | 0.59 | 0.0% | n.m. | -34.3% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 5 · NPAT 7 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 3

**RFO — เพราะอะไร** — FY2024 THB 2.1bn → FY2025 THB 1.4bn · −694m · -33.8%

- RFO ปี 2568 อยู่ที่ 1,357 ลบ. ลด 33.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนที่ดินนิคมอุตสาหกรรม และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the year 2 0 2 5, revenues from the residential real estate business were THB 450.91 million ( comprised of revenues from the sale of residential property of THB 344.90 million, and from the sale of undeveloped land of THB 106.01 million), compared with THB 488.67 million (comprised of revenues from the sale of residential property of THB 443.49 million, and from the sale of undeveloped land of THB 45.18 million) recorded in 2024. This represents a decrease of THB 37.76 million or 7.73% from 2024. Residential property sales revenue decreased due to various unfavorable factors, while revenue from undeveloped land sales increased. Gross profit was THB 106.77 million ( a gross profit margin

  `MDA_MK_FY2025` · `p006` · SHA 386cd53f7574
  </details>
- RFO ปี 2568 อยู่ที่ 1,357 ลบ. ลด 33.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ความเสี่ยงด้านภูมิรัฐศาสตร์ และ การซื้อกิจการและการรวมงบการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the year 2025, revenues from industrial real estate development were THB 720.06 million, a decrease of THB 177.26 million or 19.75% from THB 897.32 million recorded in 2024. This consisted of revenue from rent and services amounting to THB 513.75 million, a decrease of THB 76.06 million or 12.90% due to a reduction in leasable area resulting from the sale of assets to the PROSPECT REIT. In addition, the Group had revenue from real estate management amounting to THB 206.31 million, an increase of THB 65.71 million or 46.74% as the PROSPECT REIT management subsidiary received the assets acquisition fee from acquiring assets which comprised leaseholds land, land, factory, warehouse, office

  `MDA_MK_FY2025` · `p007` · SHA 344c5f56283d
  </details>
- RFO ปี 2568 อยู่ที่ 1,357 ลบ. ลด 33.8% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Total revenues in 2025 were THB 1,865.24 million, a decrease of THB 362.91 million or 16.29% from 2024. Total revenues from sales and services were THB 1,170.97 million, a decrease of THB 276.56 million or 19.11% from 2024. These revenues derive from the main businesses operated by the Company and its subsidiaries, which are:

  `MDA_MK_FY2025` · `p004` · SHA b4034125ca23
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 844m → FY2025 −THB 465m · +379m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -465 ลบ. จาก -844 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the year 2025, total cost of business amounted to THB 739.67 million, a decrease of THB 286.28 million or 27.90% from the previous year, due to lower sales and service revenue and improved cost management. The selling and administrative expenses totaled THB 627.59 million, a decrease of THB 81.93 million from last year. The decrease was in line with the absence of expenses from the Wellness business and the efficiency of expense management. Other expenses included a loss from the sale of investments of THB 36.09 million and a loss from impairment from the fair value measurement of assets held for sale of THB 24.34 million. While other expenses for 2024 consisted of impairment losses on a

  `MDA_MK_FY2025` · `p013` · SHA cc3851e245b4
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -465 ลบ. จาก -844 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนที่ดินนิคมอุตสาหกรรม และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the year 2 0 2 5, revenues from the residential real estate business were THB 450.91 million ( comprised of revenues from the sale of residential property of THB 344.90 million, and from the sale of undeveloped land of THB 106.01 million), compared with THB 488.67 million (comprised of revenues from the sale of residential property of THB 443.49 million, and from the sale of undeveloped land of THB 45.18 million) recorded in 2024. This represents a decrease of THB 37.76 million or 7.73% from 2024. Residential property sales revenue decreased due to various unfavorable factors, while revenue from undeveloped land sales increased. Gross profit was THB 106.77 million ( a gross profit margin

  `MDA_MK_FY2025` · `p006` · SHA 386cd53f7574
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -465 ลบ. จาก -844 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In summary, the Company was able to manage costs of its core businesses. As a result, the Company recorded a gross profit for the year 2025 of THB 431.31 million ( a gross profit margin of 36.83%), an increase of THB 9.71 million or 2.30% from a gross profit of THB 421.59 million (a gross profit margin of 29.12%), recorded in 2024.

  `MDA_MK_FY2025` · `p008` · SHA 8f527d790cb8
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -465 ลบ. จาก -844 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ความเสี่ยงด้านภูมิรัฐศาสตร์ และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In addition, a key source of revenue in 2025 came from a gain from the sale of leaseholds land, land, factory, warehouse, office and other constructions to the PROSPECT REIT and a profit from contract cancellations which totaled THB 399.94 million. Other income for 2025 comprised investment income of THB 186.11 million and other income THB 108.22 million, while other income for 2024 consisted of gains from the sale of investments in subsidiaries and investment income of THB 603.09 million and other income of THB 177.52 million. Most investment income came from dividends, while most other income came from common area maintenance fees from the residential real estate development business and m

  `MDA_MK_FY2025` · `p009` · SHA bcf0ce8f97cc
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > For the year 2025, total cost of business amounted to THB 739.67 million, a decrease of THB 286.28 million or 27.90% from the previous year, due to lower sales and service revenue and improved cost management. The selling and administrative expenses totaled THB 627.59 million, a decrease of THB 81.93 million from last year. The decrease was in line with the absence of expenses from the Wellness business and the efficiency of expense management. Other expenses included a loss from the sale of investments of THB 36.09 million and a loss from impairment from the fair value measurement of assets held for sale of THB 24.34 million. While other expenses for 2024 consisted of impairment losses on a

  `MDA_MK_FY2025` · `p013` · SHA cc3851e245b4
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ความเสี่ยงด้านภูมิรัฐศาสตร์ และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > As for the significant asset and liability items that changed substantially from normal operations, these included a decrease in investment properties due to a subsidiary’s disposal of the sale of leaseholds land, land, factory, warehouse, office and other constructions, together with their components, to PROSPECT REIT; a decrease in loans from financial institutions and debentures due to scheduled and early repayments; and a decrease in trade payables and other current payables.

  `MDA_MK_FY2025` · `p020` · SHA f330fa1d2ed6
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_MK_FY2025`

##### JCK — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เจซีเค อินเตอร์เนชั่นแนล จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 456m | 0.12 | -7.7% | n.m. | -61.3% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 3 · NPAT 3 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 2.2bn → FY2025 THB 630m · −1.5bn · -70.8%

- RFO ปี 2568 อยู่ที่ 630 ลบ. ลด 70.8% YoY; MD&A ระบุว่า สำหรับปี2568 สินสุดวันที่31 ธันวาคม2568ดังนี่ 1. บริษัทฯมีรายได้รวมเท่ากับ652.30 ล้านบาทลดลงจากช่วงเดียวกันของปีก่อนจำนวน1,534.52 ล้านบาทหรือคิด เป็นร้อยละ70.17 เนื่องจากมีรายได้จากการขายที่ดินในนิคมฯลดลง 2. บริษัทฯมีต้นทุนขายและต้นทุนให้เช่าและบริการและต้นทุนประกอบกิจการโรงแรมเท่ากับ334.05 ล้านบาทโดย ลดลงจากช่วงเดียวกันของปีก่อนจำนวน764.84 ล้านบาท หรือคิดเป็นร้อยละ69.60 เกิดจากต้นทุนขายที่ดินลดลง 3. บริษัทฯมีค่าใช้จ่ายในการขายและบริหารเท่ากับ320.69 ล้านบาทลดลงจากช่วงเดียวกันของปีก่อนจำนวน131.63
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > สำหรับปี2568 สินสุดวันที่31 ธันวาคม2568ดังนี่ 1. บริษัทฯมีรายได้รวมเท่ากับ652.30 ล้านบาทลดลงจากช่วงเดียวกันของปีก่อนจำนวน1,534.52 ล้านบาทหรือคิด เป็นร้อยละ70.17 เนื่องจากมีรายได้จากการขายที่ดินในนิคมฯลดลง 2. บริษัทฯมีต้นทุนขายและต้นทุนให้เช่าและบริการและต้นทุนประกอบกิจการโรงแรมเท่ากับ334.05 ล้านบาทโดย ลดลงจากช่วงเดียวกันของปีก่อนจำนวน764.84 ล้านบาท หรือคิดเป็นร้อยละ69.60 เกิดจากต้นทุนขายที่ดินลดลง 3. บริษัทฯมีค่าใช้จ่ายในการขายและบริหารเท่ากับ320.69 ล้านบาทลดลงจากช่วงเดียวกันของปีก่อนจำนวน131.63

  `MDA_JCK_FY2025` · `p003` · SHA ab5be5b65fa9
  </details>
- RFO ปี 2568 อยู่ที่ 630 ลบ. ลด 70.8% YoY; MD&A ระบุว่า ซ่ a aw al aw argue aia ล้านบาทหรือคิดเป็นร้อยละ29.10 เนืองจากบริษัทฯเนื่องจากบริษัทฯมีค่าใช้จ่ายในการขายทีดินฯลดลง 4. บริษัทฯมีส่วนแบ่งกำไรในกิจการร่วมคำเท่ากับ9.01 ล้านบาทลดลงจากช่วงเดียวกันของปีก่อนจำนวน9.84 ล้าน บาทหรือคิดเป็นร้อยละ52.20 เกิดจากบริษัทร่วมคำมีรายได้ลดลง ' 5, บริษัทฯมีผลขาดทุนสุทธิเท่ากับ386.70 ล้านบาทลดลงจากช่วงเดียวกันของปีก่อนจำนวน560.26 ล้านบาท
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ซ่ a aw al aw argue aia ล้านบาทหรือคิดเป็นร้อยละ29.10 เนืองจากบริษัทฯเนื่องจากบริษัทฯมีค่าใช้จ่ายในการขายทีดินฯลดลง 4. บริษัทฯมีส่วนแบ่งกำไรในกิจการร่วมคำเท่ากับ9.01 ล้านบาทลดลงจากช่วงเดียวกันของปีก่อนจำนวน9.84 ล้าน บาทหรือคิดเป็นร้อยละ52.20 เกิดจากบริษัทร่วมคำมีรายได้ลดลง ' 5, บริษัทฯมีผลขาดทุนสุทธิเท่ากับ386.70 ล้านบาทลดลงจากช่วงเดียวกันของปีก่อนจำนวน560.26 ล้านบาท

  `MDA_JCK_FY2025` · `p004` · SHA 697e18031f63
  </details>
- RFO ปี 2568 อยู่ที่ 630 ลบ. ลด 70.8% YoY; MD&A ระบุว่า ทีมี กำไร173.56 ล้านบาท หรือคิดเป็นร้อยละ322.80 เกิดจากบริษัทฯมีรายได้จากการขายที่ดินนิคมฯ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ทีมี กำไร173.56 ล้านบาท หรือคิดเป็นร้อยละ322.80 เกิดจากบริษัทฯมีรายได้จากการขายที่ดินนิคมฯ

  `MDA_JCK_FY2025` · `p005` · SHA badca0f8536a
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 174m → FY2025 −THB 387m · −560m

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -387 ลบ. จากกำไร 174 ลบ.; MD&A ระบุว่า สำหรับปี2568 สินสุดวันที่31 ธันวาคม2568ดังนี่ 1. บริษัทฯมีรายได้รวมเท่ากับ652.30 ล้านบาทลดลงจากช่วงเดียวกันของปีก่อนจำนวน1,534.52 ล้านบาทหรือคิด เป็นร้อยละ70.17 เนื่องจากมีรายได้จากการขายที่ดินในนิคมฯลดลง 2. บริษัทฯมีต้นทุนขายและต้นทุนให้เช่าและบริการและต้นทุนประกอบกิจการโรงแรมเท่ากับ334.05 ล้านบาทโดย ลดลงจากช่วงเดียวกันของปีก่อนจำนวน764.84 ล้านบาท หรือคิดเป็นร้อยละ69.60 เกิดจากต้นทุนขายที่ดินลดลง 3. บริษัทฯมีค่าใช้จ่ายในการขายและบริหารเท่ากับ320.69 ล้านบาทลดลงจากช่วงเดียวกันของปีก่อนจำนวน131.63
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > สำหรับปี2568 สินสุดวันที่31 ธันวาคม2568ดังนี่ 1. บริษัทฯมีรายได้รวมเท่ากับ652.30 ล้านบาทลดลงจากช่วงเดียวกันของปีก่อนจำนวน1,534.52 ล้านบาทหรือคิด เป็นร้อยละ70.17 เนื่องจากมีรายได้จากการขายที่ดินในนิคมฯลดลง 2. บริษัทฯมีต้นทุนขายและต้นทุนให้เช่าและบริการและต้นทุนประกอบกิจการโรงแรมเท่ากับ334.05 ล้านบาทโดย ลดลงจากช่วงเดียวกันของปีก่อนจำนวน764.84 ล้านบาท หรือคิดเป็นร้อยละ69.60 เกิดจากต้นทุนขายที่ดินลดลง 3. บริษัทฯมีค่าใช้จ่ายในการขายและบริหารเท่ากับ320.69 ล้านบาทลดลงจากช่วงเดียวกันของปีก่อนจำนวน131.63

  `MDA_JCK_FY2025` · `p003` · SHA ab5be5b65fa9
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -387 ลบ. จากกำไร 174 ลบ.; MD&A ระบุว่า ซ่ a aw al aw argue aia ล้านบาทหรือคิดเป็นร้อยละ29.10 เนืองจากบริษัทฯเนื่องจากบริษัทฯมีค่าใช้จ่ายในการขายทีดินฯลดลง 4. บริษัทฯมีส่วนแบ่งกำไรในกิจการร่วมคำเท่ากับ9.01 ล้านบาทลดลงจากช่วงเดียวกันของปีก่อนจำนวน9.84 ล้าน บาทหรือคิดเป็นร้อยละ52.20 เกิดจากบริษัทร่วมคำมีรายได้ลดลง ' 5, บริษัทฯมีผลขาดทุนสุทธิเท่ากับ386.70 ล้านบาทลดลงจากช่วงเดียวกันของปีก่อนจำนวน560.26 ล้านบาท
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ซ่ a aw al aw argue aia ล้านบาทหรือคิดเป็นร้อยละ29.10 เนืองจากบริษัทฯเนื่องจากบริษัทฯมีค่าใช้จ่ายในการขายทีดินฯลดลง 4. บริษัทฯมีส่วนแบ่งกำไรในกิจการร่วมคำเท่ากับ9.01 ล้านบาทลดลงจากช่วงเดียวกันของปีก่อนจำนวน9.84 ล้าน บาทหรือคิดเป็นร้อยละ52.20 เกิดจากบริษัทร่วมคำมีรายได้ลดลง ' 5, บริษัทฯมีผลขาดทุนสุทธิเท่ากับ386.70 ล้านบาทลดลงจากช่วงเดียวกันของปีก่อนจำนวน560.26 ล้านบาท

  `MDA_JCK_FY2025` · `p004` · SHA 697e18031f63
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 พลิกเป็นขาดทุน -387 ลบ. จากกำไร 174 ลบ.; MD&A ระบุว่า ทีมี กำไร173.56 ล้านบาท หรือคิดเป็นร้อยละ322.80 เกิดจากบริษัทฯมีรายได้จากการขายที่ดินนิคมฯ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ทีมี กำไร173.56 ล้านบาท หรือคิดเป็นร้อยละ322.80 เกิดจากบริษัทฯมีรายได้จากการขายที่ดินนิคมฯ

  `MDA_JCK_FY2025` · `p005` · SHA badca0f8536a
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_JCK_FY2025`

##### WIN — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท สวนอุตสาหกรรม วินโคสท์ จำกัด (มหาชน)** — กำไรแปลงจากรายได้ได้อ่อนลง

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ให้เช่าอสังหาริมทรัพย์ ประเภทพื้นที่ อาคารโรงงาน บริเวณติดถนนบางนา-ตราด ก.ม 52 โดยแบ่งเป็น 3 ส่วน คือ 1) พื้นที่ให้เช่าและบริการในเขตปลอดอากร (Free Zone)2) พื้นที่ให้เช่าและบริการนอกเขตปลอดอากร3) พื้นที่ให้เช่าและบริการบนหลังคา

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 163m | 0.29 | -17.1% | n.m. | 0.7% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 5 · NPAT 6 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 92m → FY2025 THB 212m · +120m · +129.9%

- RFO ปี 2568 อยู่ที่ 212 ลบ. เพิ่ม 129.9% YoY; MD&A ระบุว่า เกินกว่าร้อยละ 20 เมื่อเปรียบเทียบกับช่วงเวลาเดียวกันของปี 2567 สาเหตุหลักเนื่องจาก 1. รายได้รวมประจำปี 2568 เพิ่มขึ้นจากช่วงเวลาเดียวกันของปีก่อนร้อยละ 114.64 โดยมีรายละเอียดดังนี้ 1.1 รายได้จากการให้เช่าและบริการเพิ่มขึ้น 0.63 ล้านบาท หรือเพิ่มขึ้นคิดเป็นอัตราร้อยละ 1.51 เนื่องจากมีลูกค้าเช่าและบริการพื้นที่เพิ่มขึ้นจากงวดเดียวกันของปีก่อน ส่งผลให้รายได้จากการให้เช่าและบริการเพิ่มขึ้น ณ วันที่ 31 ธันวาคม 2568 มีอัตราการเช่าพื้นที่ทั้งในและนอกเขตปลอดอากร โดยมีรายละเอียดดังนี้
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > เกินกว่าร้อยละ 20 เมื่อเปรียบเทียบกับช่วงเวลาเดียวกันของปี 2567 สาเหตุหลักเนื่องจาก 1. รายได้รวมประจำปี 2568 เพิ่มขึ้นจากช่วงเวลาเดียวกันของปีก่อนร้อยละ 114.64 โดยมีรายละเอียดดังนี้ 1.1 รายได้จากการให้เช่าและบริการเพิ่มขึ้น 0.63 ล้านบาท หรือเพิ่มขึ้นคิดเป็นอัตราร้อยละ 1.51 เนื่องจากมีลูกค้าเช่าและบริการพื้นที่เพิ่มขึ้นจากงวดเดียวกันของปีก่อน ส่งผลให้รายได้จากการให้เช่าและบริการเพิ่มขึ้น ณ วันที่ 31 ธันวาคม 2568 มีอัตราการเช่าพื้นที่ทั้งในและนอกเขตปลอดอากร โดยมีรายละเอียดดังนี้

  `MDA_WIN_FY2025` · `p002` · SHA afa325f0a211
  </details>
- RFO ปี 2568 อยู่ที่ 212 ลบ. เพิ่ม 129.9% YoY; MD&A ระบุว่า จึงทำให้รายได้จากสัญญาก่อสร้างเพิ่มขึ้น 1.3 รายได้จากการขายและบริการเพิ่มขึ้น 30.56 ล้านบาท หรือเพิ่มขึ้นคิดเป็นอัตราร้อยละ 89.34 เมื่อ เปรียบเทียบกับงวดเดียวกันของปีก่อน สาเหตุหลักเนื่องจากการเพิ่มขึ้นของสินค้าที่มีไว้เพื่อขายของบริษัท รวมถึงรายได้
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > จึงทำให้รายได้จากสัญญาก่อสร้างเพิ่มขึ้น 1.3 รายได้จากการขายและบริการเพิ่มขึ้น 30.56 ล้านบาท หรือเพิ่มขึ้นคิดเป็นอัตราร้อยละ 89.34 เมื่อ เปรียบเทียบกับงวดเดียวกันของปีก่อน สาเหตุหลักเนื่องจากการเพิ่มขึ้นของสินค้าที่มีไว้เพื่อขายของบริษัท รวมถึงรายได้

  `MDA_WIN_FY2025` · `p004` · SHA 0ec2ee524d85
  </details>
- RFO ปี 2568 อยู่ที่ 212 ลบ. เพิ่ม 129.9% YoY; MD&A ระบุว่า จากการขายไฟฟ้าของบริษัทย่อย 1.4 รายได้อื่นลดลง 4.82 ล้านบาท หรือลดลงคิดเป็นอัตราร้อยละ 59.89 เมื่อเปรียบเทียบกับงวด เดียวกันของปีก่อน สาเหตุหลักเนื่องจากการลดลงของดอกเบี้ยเงินกู้ยืมของบริษัทย่อย รวมถึงผลต่างรายได้ภาษี
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > จากการขายไฟฟ้าของบริษัทย่อย 1.4 รายได้อื่นลดลง 4.82 ล้านบาท หรือลดลงคิดเป็นอัตราร้อยละ 59.89 เมื่อเปรียบเทียบกับงวด เดียวกันของปีก่อน สาเหตุหลักเนื่องจากการลดลงของดอกเบี้ยเงินกู้ยืมของบริษัทย่อย รวมถึงผลต่างรายได้ภาษี

  `MDA_WIN_FY2025` · `p005` · SHA ce21cb934cb8
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 2m → FY2025 THB 1m · −1m · -26.8%

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1.4 ลบ. ลด 26.8% YoY; MD&A ระบุว่า ทรัพย์สินลดลง ส่งผลให้ต้นทุนให้เช่าและบริการลดลง 2.2 ต้นทุนจากสัญญาก่อสร้างเพิ่มขึ้นจำนวน 55.92 ล้านบาท หรือเพิ่มขึ้นคิดเป็นร้อยละ 478.98 เมื่อ เปรียบเทียบกับงวดเดียวกันของปีก่อน เนื่องจากรายได้ค่าก่อสร้างเพิ่มขึ้น ต้นทุนจากสัญญาก่อสร้างจึงเพิ่มขึ้น 2.3 ต้นทุนขายและบริการ เพิ่มขึ้นจำนวน 29.78 ล้านบาท หรือเพิ่มขึ้นคิดเป็นร้อยละ 129.49 เมื่อ เปรียบเทียบกับงวดเดียวกันของปีก่อน เนื่องจากบริษัทมีการขายสินค้าอุปกรณ์โซล่าเซลล์ ส่งผลให้ต้นทุนขายและบริการ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ทรัพย์สินลดลง ส่งผลให้ต้นทุนให้เช่าและบริการลดลง 2.2 ต้นทุนจากสัญญาก่อสร้างเพิ่มขึ้นจำนวน 55.92 ล้านบาท หรือเพิ่มขึ้นคิดเป็นร้อยละ 478.98 เมื่อ เปรียบเทียบกับงวดเดียวกันของปีก่อน เนื่องจากรายได้ค่าก่อสร้างเพิ่มขึ้น ต้นทุนจากสัญญาก่อสร้างจึงเพิ่มขึ้น 2.3 ต้นทุนขายและบริการ เพิ่มขึ้นจำนวน 29.78 ล้านบาท หรือเพิ่มขึ้นคิดเป็นร้อยละ 129.49 เมื่อ เปรียบเทียบกับงวดเดียวกันของปีก่อน เนื่องจากบริษัทมีการขายสินค้าอุปกรณ์โซล่าเซลล์ ส่งผลให้ต้นทุนขายและบริการ

  `MDA_WIN_FY2025` · `p008` · SHA 6918eca76898
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1.4 ลบ. ลด 26.8% YoY; MD&A ระบุว่า เนื่องจาก 2.1 ต้นทุนการให้เช่าและบริการลดลง จำนวน 0.35 ล้านบาท หรือลดลงคิดเป็นร้อยละ 6.86 เมื่อ เปรียบเทียบกับงวดเดียวกันของปีก่อน สาเหตุหลักเนื่องจากต้นทุนบริการค่าไฟฟ้าลดลง รวมถึงต้นทุนค่าเสื่อมราคา
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > เนื่องจาก 2.1 ต้นทุนการให้เช่าและบริการลดลง จำนวน 0.35 ล้านบาท หรือลดลงคิดเป็นร้อยละ 6.86 เมื่อ เปรียบเทียบกับงวดเดียวกันของปีก่อน สาเหตุหลักเนื่องจากต้นทุนบริการค่าไฟฟ้าลดลง รวมถึงต้นทุนค่าเสื่อมราคา

  `MDA_WIN_FY2025` · `p007` · SHA 5016a1696ed9
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1.4 ลบ. ลด 26.8% YoY; MD&A ระบุว่า โดยมีรายละเอียดดังนี้ 3.1 ต้นทุนในการจัดจำหน่ายและบริการ (ค่าใช้จ่ายในการขายและบริการ) เพิ่มขึ้นจำนวน 0.39 ล้าน บาท หรือเพิ่มขึ้นคิดเป็นร้อยละ 15.49 เมื่อเปรียบเทียบกับงวดเดียวกันของปีก่อน สาเหตุหลักเนื่องจากการเพิ่มขึ้นของ
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > โดยมีรายละเอียดดังนี้ 3.1 ต้นทุนในการจัดจำหน่ายและบริการ (ค่าใช้จ่ายในการขายและบริการ) เพิ่มขึ้นจำนวน 0.39 ล้าน บาท หรือเพิ่มขึ้นคิดเป็นร้อยละ 15.49 เมื่อเปรียบเทียบกับงวดเดียวกันของปีก่อน สาเหตุหลักเนื่องจากการเพิ่มขึ้นของ

  `MDA_WIN_FY2025` · `p010` · SHA 2e9ee381f974
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1.4 ลบ. ลด 26.8% YoY; MD&A ระบุว่า โรงเรือนที่บริษัทจัดเก็บลูกค้าเช่าพื้นที่ลดลง 2. ต้นทุนรวมของบริษัทประจำปี 2568 เพิ่มขึ้นจากช่วงเวลาเดียวกันของปีก่อน ร้อยละ 214.66 สาเหตุหลัก
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > โรงเรือนที่บริษัทจัดเก็บลูกค้าเช่าพื้นที่ลดลง 2. ต้นทุนรวมของบริษัทประจำปี 2568 เพิ่มขึ้นจากช่วงเวลาเดียวกันของปีก่อน ร้อยละ 214.66 สาเหตุหลัก

  `MDA_WIN_FY2025` · `p006` · SHA 4d0a29e7e181
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_WIN_FY2025`

#### ทะเบียนข้อสรุป — P2

| ส่วน | ประเภท | ข้อสรุป | รหัสแหล่งข้อมูล |
|---|---|---|---|
| headline | ข้ออนุมานนักวิเคราะห์ | FDI optionality ผลักราคานำกำไรรายงาน | FY_PANEL, P2_E1, P2_E2, P2_E3, P2_E4, P2_E5 |
| earnings_fact | ข้อเท็จจริงจากการคำนวณ | FY2025 RFO -12.4%; สถานะ NPAT ส่วนผู้ถือหุ้น: profit_decreased | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | RFO ลด 12.4% และ NPAT ส่วนผู้ถือหุ้นลด 29.8% แม้ราคา YTD แข็งแรง | FY_PANEL, SET_PUBLIC_EOD |
| why | คำอธิบายฝ่ายจัดการ | การโอนที่ดินต่ำกว่าคาด ขณะที่ FDI และความพร้อม data centre สนับสนุน optionality | P2_E1, P2_E2, P2_E3, P2_E4, P2_E5 |
| why | ข้ออนุมานนักวิเคราะห์ | ROJNA เป็นตัวแปรกำไรรายงานและ mark-to-market ไม่ใช่หลักฐานการดำเนินงานที่สะอาด | FY_PANEL, P2_E1, P2_E2, P2_E3, P2_E4, P2_E5 |
| causal_chain | ข้ออนุมานนักวิเคราะห์ | ห่วงโซ่เหตุ: BOI / FDI → ยอดขายที่ดิน → โอน → Utility / ค่าเช่า → NPAT | P2_E1, P2_E2, P2_E3, P2_E4, P2_E5 |
| roles | ข้ออนุมานนักวิเคราะห์ | บทบาท: ผู้นำ — WHA; ตัวแทน FDI และราคา — AMATA; ตัวแปรกำไรรายงาน — ROJNA | FY_PANEL, P2_E1, P2_E2, P2_E3, P2_E4, P2_E5 |
| valuation | ข้ออนุมานนักวิเคราะห์ | P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 10.7x ครอบคลุม 6/9 บริษัท และ 98.9% ของ market cap ที่มีข้อมูล. rerating สอดคล้องกับความคาดหวัง FDI/data centre แต่ยังไม่ใช่หลักฐานกำไร | SET_PUBLIC_EOD, P2_E1, P2_E2, P2_E3, P2_E4, P2_E5 |
| trigger | ประเด็นที่ต้องพิสูจน์ | ยอดขายที่ดินและการโอนเกิดจริง | P2_E1, P2_E2, P2_E3, P2_E4, P2_E5 |
| trigger | ประเด็นที่ต้องพิสูจน์ | ความพร้อมด้านไฟฟ้าสำหรับ data center | P2_E1, P2_E2, P2_E3, P2_E4, P2_E5 |
| trigger | ประเด็นที่ต้องพิสูจน์ | ปริมาณ utility เพิ่ม | P2_E1, P2_E2, P2_E3, P2_E4, P2_E5 |
| risk | ประเด็นที่ต้องพิสูจน์ | FDI แปลงเป็นการลงทุนจริงล่าช้า | P2_E1, P2_E2, P2_E3, P2_E4, P2_E5 |
| risk | ประเด็นที่ต้องพิสูจน์ | โอนและโครงสร้างพื้นฐานล่าช้า | P2_E1, P2_E2, P2_E3, P2_E4, P2_E5 |
| risk | ประเด็นที่ต้องพิสูจน์ | ข้อจำกัดที่ดิน ไฟฟ้า และกฎระเบียบ | P2_E1, P2_E2, P2_E3, P2_E4, P2_E5 |
| must_prove | ประเด็นที่ต้องพิสูจน์ | 6M26 ต้องเปลี่ยนข่าวนโยบายและ presales ให้เป็นการโอน utility และ cash earnings | P2_E1, P2_E2, P2_E3, P2_E4, P2_E5 |

#### ทะเบียนหลักฐาน — P2

- **`FY_PANEL`** · _ข้อเท็จจริงจากการคำนวณ_ — Audited FY2024-25 company panel
  - RFO / NPAT-to-owners / independent panel membership; QA 43 pass / 0 fail
  - บทบาท: historical fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_company_fy2024_2025_audited_2026-08-07.csv`
  - SHA-256: `e5e04dbc40ffcc79fed58545a93dc4549c29cdaecf260bea73711bc6d0720481`
- **`SET_PUBLIC_EOD`** · _ข้อเท็จจริงจากการคำนวณ_ — SET public Company Highlights — EOD 2026-08-07
  - Adjusted YTD; unadjusted price, market cap and valuation; factsheet-surface cross-check
  - บทบาท: current market fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_set_public_surface_reconciliation_2026-08-07.csv`
  - SHA-256: `544c1f29fe2d409ee398822ac2bf32b769081718962ae2d1138985b0146b9530`
- **`SET_COMPANY_PROFILE`** · _ข้อเท็จจริง_ — SET company profiles — English and Thai
  - Official company names and business descriptions refreshed and validated for the 118-company perimeter from the public SET profile API
  - บทบาท: company business profile
  - URL: <https://www.set.or.th/th/market/product/stock/overview>
- **`COMPANY_REPORTS`** · _ข้ออนุมานนักวิเคราะห์_ — Company report synthesis corpus
  - Annual-only draft synthesis; reconciled to the ticker FY2025 MD&A where available
  - บทบาท: secondary synthesis; not management attribution
  - พาธ: `data/company-reports.json`
  - SHA-256: `c1a2bc40cbe21a2058aa596c362e4d47ad117360831b847de78ec414831fd2d2`
- **`MDA_WHA_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — WHA FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/WHA/MDA_WHA_2025FY_T.md`
  - SHA-256: `7ab1fdd520232d425c0b06c02e1e898628e70e310efed1614b8ed549de9ce1ba`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/1107NWS260220260801344400T.pdf>
- **`MDA_AMATA_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — AMATA FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/AMATA/MDA_AMATA_2025FY_T.md`
  - SHA-256: `3838382301944044f6e2ac567047fbdd6d3016191f6e55bb6bc8cb5735f256ad`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202603/0617NWS020320262153211530T.pdf>
- **`MDA_ROJNA_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — ROJNA FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/ROJNA/MDA_ROJNA_2025FY_T.md`
  - SHA-256: `8afa625113239a6d686521f514192ef646941cd8191cd3b59b9fee3404232c26`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202603/0477NWS020320261232106990T.pdf>
- **`MDA_PIN_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — PIN FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/PIN/MDA_PIN_2025FY_T.md`
  - SHA-256: `6ade19ccba1b1a67833ad2ca1c6a36aa302b65f9b9307d107b58747c78c6deef`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/1661NWS250220260859481690T.pdf>
- **`MDA_NNCL_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — NNCL FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/NNCL/MDA_NNCL_2025FY_T.md`
  - SHA-256: `bc55b76b50bf2383d09e2edb16411e2c34146a76907c54bb995b44356ded1522`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/0702NWS240220261959396200T.pdf>
- **`MDA_AMATAV_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — AMATAV FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/AMATAV/MDA_AMATAV_2025FY_T.md`
  - SHA-256: `b7cdac09515cdbdbcb8dd17688ac136fa704e5a001211f5f1031364739b7e991`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/1270NWS250220260711172450T.pdf>
- **`MDA_MK_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — MK FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/MK/MDA_MK_2025FY_E.md`
  - SHA-256: `b16edf1bd8c861543369ecb3f427b3c0b2bc15182ce8cbd1626794ec431435b8`
  - URL: <https://weblink.set.or.th/dat/news/202603/0182NWS040320260718492360E.pdf>
- **`MDA_JCK_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — JCK FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/JCK/MDA_JCK_2025FY_T.md`
  - SHA-256: `06d08c484d4900b0048be5d44da1b20e937e1a3ead861124cdd50121bffe7bf4`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/0235NWS260220261902149920T.pdf>
- **`MDA_WIN_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — WIN FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/WIN/MDA_WIN_2025FY_T.md`
  - SHA-256: `9ed6f02b7c23e49b08aa49de0060743ba57ca76e6188a41138e55f7f7d440b3f`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/0188NWS270220261804517540T.pdf>
- **`P2_E1`** · _ฝ่ายจัดการ_ — AMATA FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/AMATA/MDA_AMATA_2025FY_E.md`
  - SHA-256: `2933c30c940ee0cf92b1d62b6702b294a91ebf3dae73ff0db96661f236b03c62`
- **`P2_E2`** · _ฝ่ายจัดการ_ — ROJNA FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/ROJNA/MDA_ROJNA_2025FY_E.md`
  - SHA-256: `6e62bbc9fbd5fe85b85353d0a5be09fa843da7a22814aa6290993b38c1dbf82e`
- **`P2_E3`** · _ฝ่ายจัดการ_ — MK FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/MK/MDA_MK_2025FY_E.md`
  - SHA-256: `b16edf1bd8c861543369ecb3f427b3c0b2bc15182ce8cbd1626794ec431435b8`
- **`P2_E4`** · _ฝ่ายจัดการ_ — JCK FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/JCK/MDA_JCK_2025FY_E.md`
  - SHA-256: `383645d1b9c70605c85db68b9b72c87bd77f129018f1d654729029c3ac0a03c0`
- **`P2_E5`** · _มุมมองล่วงหน้า_ — MST WHA research
  - Historical explanation or forward cross-check; see source role
  - บทบาท: forward/credit context
  - พาธ: `Listed Company/1-Raw/06-Market Reference/Broker Research/2026/PROP/MST_WHA_348118.md`
  - SHA-256: `7b4823fe973a5bee3493b5de290a4ad814b82c4c07d9cf80310400901407744a`
- **`P2_FACTSHEET`** · _ข้อเท็จจริงจากการคำนวณ_ — SET Factsheet — WHA
  - Live leader cross-check
  - บทบาท: presentation-surface check
  - URL: <https://www.set.or.th/th/market/product/stock/quote/wha/factsheet>

### P4 · โรงแรมและมิกซ์ยูส — AWC ส่งมอบการเติบโต แต่ด้อยค่าของ S ฉุดภาพรวม

`ราคานำพื้นฐาน` · 13.0% M-cap · THB 109bn · 4 บริษัท

| ตัวชี้วัด | RFO | NPAT | ราคา | P/E |
|---|---|---|---|---|
| ช่วง | FY2025 YoY | ส่วนผู้ถือหุ้น FY2025 YoY | ราคา YTD ปรับแล้ว | เฉพาะบริษัทที่มีกำไร |
| ค่า | -2.0% | -15.8% | +38.2% | 14.9x |
| จำนวน | THB 33.1bn FY2025 | THB 4.8bn FY2025 | ณ 7 ส.ค. 2569 | ค่าเฉลี่ยรวม |
| ครอบคลุม | 3/4 | 3/4 | 4/4 • 100% M-cap | 2/4 • 96% M-cap |

**ข้อเท็จจริงที่สังเกตได้** — FY2025: RFO -2.0% • NPAT -15.8% • ราคา YTD +38.2% • P/E 14.9x • ครอบคลุม RFO 3/4 • NPAT 3/4

#### เหตุผลที่เปลี่ยน

1. _ข้อเท็จจริงจากการคำนวณ_ · นักท่องเที่ยว — กลุ่มปิดงบธันวาคม 3/4 บริษัทมี RFO -2.0% และ NPAT -15.8%; BLAND ถูกตัดออกเพราะปิดงบมีนาคม
2. _คำอธิบายฝ่ายจัดการ_ · Occupancy / ADR — AWC เพิ่ม RFO และ NPAT แต่มี fair-value gain 5,555 ล้านบาท จึงต้อง bridge จาก operating ไป reported
3. _คำอธิบายฝ่ายจัดการ_ · Asset ramp — S บันทึกด้อยค่า 1,963 ล้านบาท ขณะที่กำไรปกติ 531 ล้านบาท

#### ห่วงโซ่เหตุและผล

**นักท่องเที่ยว** → **Occupancy / ADR** → **Asset ramp** → **EBITDA** (-15.8% THB 4.8bn FY2025) → **NPAT** (-15.8% THB 4.8bn FY2025)

#### บทบาทในกลุ่ม

| บทบาท | Ticker | ค่า | ที่มาของค่า |
|---|---|---|---|
| ผู้นำและส่งมอบการดำเนินงาน | AWC | 87% | สัดส่วน Market Cap ในกลุ่ม |
| ตัวฉุดจากด้อยค่า | S | n.m. | P/E · YTD +12.2% |

#### มูลค่า

**ตลาดกำลังจ่ายเพื่อ — ข้ออนุมาน** — P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 14.9x ครอบคลุม 2/4 บริษัท และ 96.2% ของ market cap ที่มีข้อมูล. ราคาสะท้อน tourism และ asset optionality แต่ต้องพิสูจน์กำไรเงินสดปกติ

| Trigger | Risk |
|---|---|
| occupancy และ ADR เพิ่ม | ความเสี่ยงท่องเที่ยว |
| สินทรัพย์ใหม่ ramp-up ตามแผน | ต้นทุนคงที่และ leverage สูง |
| นักท่องเที่ยวฟื้นหลายตลาด | asset ramp-up ล่าช้า |

**6M26 ต้องพิสูจน์** — 6M26 ต้องแปลง occupancy และ ADR เป็นกำไรส่วนผู้ถือหุ้นและ cash flow

#### วิเคราะห์รายบริษัท — P4 โรงแรมและมิกซ์ยูส

_ทุกบริษัทใน perimeter ของ Segment ที่สอบทาน_

| Ticker | บทบาท | M-cap | RFO YoY | NPAT YoY | ราคา YTD | P/E | Margin |
|---|---|---|---|---|---|---|---|
| AWC | ผู้นำและส่งมอบการดำเนินงาน | THB 95.4bn | +9.1% | +9.2% | +40.6% | 14.9x | 36.8% |
| BLAND | บริษัทในกลุ่ม | THB 9.7bn | — | — | +30.2% | 14.7x | — |
| S | ตัวฉุดจากด้อยค่า | THB 3.8bn | -7.3% | ขาดทุน | +12.2% | n.m. | -9.8% |
| CI | บริษัทในกลุ่ม | THB 405m | -36.6% | ขาดทุนลดลง | +8.6% | n.m. | -14.9% |

##### AWC — ผู้นำและส่งมอบการดำเนินงาน · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท แอสเสท เวิรด์ คอร์ป จำกัด (มหาชน)** — รายได้และกำไรเคลื่อนไหวสอดคล้องกัน

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัท แอสเสท เวิรด์ คอร์ป จำกัด (มหาชน) หรือ AWC คือกลุ่มบริษัทพัฒนาอสังหาริมทรัพย์ชั้นนำของไทยที่มุ่งเน้นตอบสนองไลฟ์สไตล์แบบครบวงจร และเป็นสมาชิกในเครือทีซีซี กรุ๊ป (TCC Group) โดยดำเนินธุรกิจภายใต้พันธกิจ "สร้างสรรค์อนาคตที่ดีกว่าให้ทุกคน" บริษัทฯ มุ่งมั่นพัฒนาและบริหารพอร์ตโฟลิโออสังหาริมทรัพย์คุณภาพสูงที่หลากหลาย ครอบคลุมกลุ่มธุรกิจโรงแรมและการบริการ กลุ่มจุดหมายปลายทางด้านไลฟ์สไตล์ และกลุ่มอาคารสำนักงาน เพื่…

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 95.4bn | 2.98 | +40.6% | 14.9x | 36.8% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 3

**RFO — เพราะอะไร** — FY2024 THB 15.9bn → FY2025 THB 17.4bn · +1.5bn · +9.1%

- รายได้โตประมาณ 10% จากโรงแรมใหม่ 5 แห่งและพื้นที่/แหล่งท่องเที่ยวเชิงพาณิชย์ที่เพิ่มขึ้น
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > วันที่ 20-28 ธันวาคม 2568 Netflix ได้จัดงานพิเศษ “One Last Adventure in Thailand” เพื่อเฉลิมฉลองการกลับมาของซีรีส์ระดับโลก Stranger Things (Season 5) โดยมีไฮไลต์สำคัญ ได้แก่ โซน THE WSQK และ One Last Ride Together ภายในงานได้รับความสนใจและมีผู้เข้าร่วม ทั้งชาวไทยและชาวต่างประเทศเป็นจำนวนมาก สะท้อนถึงประสิทธิภาพของกลยุทธ์ New Value & Experience Model ของบริษัทในการ ยกระดับความน่าสนใจของย่านทรงวาด และดึงดูดกลุ่มผู้เข้าชมคุณภาพจากทั้งตลาดในประเทศและต่างประเทศได้อย่างโดดเด่น • กลุ่มธุรกิจโรงแรมและบริการสร้างกระแสเงินสดอย่างมั่นคง ด้วยรายได้รวม 12,813 ล้านบาท เติบโตร้อยละ 4.5 จากปีก่อน และร้อยละ 47 จาก ปี 2562 จากการรับรู้รายได้ของทรัพย์สินใหม่จากการเปิด 3 โรงแรม ซึ่งสร้างรายได้ส่วนเพิ่มกว่า 720

  `MDA_AWC_FY2025` · `p005` · SHA e3066cbf8f47
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 5.9bn → FY2025 THB 6.4bn · +538m · +9.2%

- กำไรรายงานเพิ่ม 9% แต่รวม กำไรจากการวัดมูลค่ายุติธรรม อสังหาริมทรัพย์เพื่อการลงทุน 5.555 พันลบ. ทำให้กำไรเงินสดหลักต่ำกว่า NPAT ตัวเลขรายงาน มาก
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไรจากการดำเนินงาน (อิบิทดำ) ของกลุ่มธุรกิจคอมเมอร์เชียล ปี 2568 บริษัทมีกำไรจากการดำเนินงาน (อิบิทดา) ของกลุ่มธุรกิจคอมเมอร์เชียลอยู่ที่ 8,114 ล้านบาท เพิ่มขึ้นร้อยละ 5.0 จากปีก่อน หากไม่รวมกำไรจาก การเปลี่ยนแปลงมูลค่ายุติธรรมของอสังหาริมทรัพย์เพื่อการลงทุน กำไรจากการดำเนินงาน (อิบิทดา) ของกลุ่มธุรกิจคอมเมอร์เชียลอยู่ที่ 2,980 ล้านบาท เพิ่มขึ้นร้อยละ 13.8 จากปีก่อน เนื่องจากการรับรู้ผลการดำเนินงานของ Jurassic World: The Experience และเครื่องเล่น Skyflyers: Wings of Garudapterus ที่โครงการเอเชียทีค เดอะ ริเวอร์ฟร้อนท์ เดสติเนชั่น รวมทั้งการปรับตำแหน่งทางการตลาดของศูนย์การค้าอย่างต่อเนื่อง ทำให้ มีลูกค้าเข้าใช้บริการเพิ่มมากขึ้น โดยกลุ่มธุรกิจศูนย์การค้ามีกำไรจากการดำเนินงาน (อิบิทดา) เติบโต

  `MDA_AWC_FY2025` · `p031` · SHA 2d6a7123fbff
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรจากการดำเนินงาน (อิบิทดำ) ของกลุ่มธุรกิจคอมเมอร์เชียล ปี 2568 บริษัทมีกำไรจากการดำเนินงาน (อิบิทดา) ของกลุ่มธุรกิจคอมเมอร์เชียลอยู่ที่ 8,114 ล้านบาท เพิ่มขึ้นร้อยละ 5.0 จากปีก่อน หากไม่รวมกำไรจาก การเปลี่ยนแปลงมูลค่ายุติธรรมของอสังหาริมทรัพย์เพื่อการลงทุน กำไรจากการดำเนินงาน (อิบิทดา) ของกลุ่มธุรกิจคอมเมอร์เชียลอยู่ที่ 2,980 ล้านบาท เพิ่มขึ้นร้อยละ 13.8 จากปีก่อน เนื่องจากการรับรู้ผลการดำเนินงานของ Jurassic World: The Experience และเครื่องเล่น Skyflyers: Wings of Garudapterus ที่โครงการเอเชียทีค เดอะ ริเวอร์ฟร้อนท์ เดสติเนชั่น รวมทั้งการปรับตำแหน่งทา
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไรจากการดำเนินงาน (อิบิทดำ) ของกลุ่มธุรกิจคอมเมอร์เชียล ปี 2568 บริษัทมีกำไรจากการดำเนินงาน (อิบิทดา) ของกลุ่มธุรกิจคอมเมอร์เชียลอยู่ที่ 8,114 ล้านบาท เพิ่มขึ้นร้อยละ 5.0 จากปีก่อน หากไม่รวมกำไรจาก การเปลี่ยนแปลงมูลค่ายุติธรรมของอสังหาริมทรัพย์เพื่อการลงทุน กำไรจากการดำเนินงาน (อิบิทดา) ของกลุ่มธุรกิจคอมเมอร์เชียลอยู่ที่ 2,980 ล้านบาท เพิ่มขึ้นร้อยละ 13.8 จากปีก่อน เนื่องจากการรับรู้ผลการดำเนินงานของ Jurassic World: The Experience และเครื่องเล่น Skyflyers: Wings of Garudapterus ที่โครงการเอเชียทีค เดอะ ริเวอร์ฟร้อนท์ เดสติเนชั่น รวมทั้งการปรับตำแหน่งทางการตลาดของศูนย์การค้าอย่างต่อเนื่อง ทำให้ มีลูกค้าเข้าใช้บริการเพิ่มมากขึ้น โดยกลุ่มธุรกิจศูนย์การค้ามีกำไรจากการดำเนินงาน (อิบิทดา) เติบโต

  `MDA_AWC_FY2025` · `p031` · SHA 2d6a7123fbff
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายได้กลุ่มธุรกิจคอมเมอร์เชียล ภาพรวมอุตสาหกรรมค้าปลีกในปี 2568 เติบโตเล็กน้อยจากปีก่อน จากการมุ่งขยายสาขาของห้างค้าปลีกขนาดใหญ่การเติบโตของ Local ช่องทางค้าปลีกสมัยใหม่ รวมทั้งอานิสงส์จากโครงการ “คนละครึ่ง พลัส” ในช่วงไตรมาส 4/2568 ซึ่งช่วยกระตุ้นการใช้จ่ายของผู้บริโภค และกระจายเม็ดเงินสู่ร้านค้าขนาด กลางและขนาดย่อม โดยในปี 2568 บริษัทมีรายได้ของกลุ่มธุรกิจคอมเมอร์เชียลอยู่ที่ 9,602 ล้านบาท เพิ่มขึ้นร้อยละ 6.9 จากช่วงเดียวกันของปีก่อน หากไม่รวมกำไรจากการเปลี่ยนแปลงมูลค่ายุติธรรมของอสังหาริมทรัพย์เพื่อการลงทุน รายได้ของกลุ่มธุรกิจคอมเมอร์เชียลอยู่ที่ 4,467 ล้านบาท
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้กลุ่มธุรกิจคอมเมอร์เชียล ภาพรวมอุตสาหกรรมค้าปลีกในปี 2568 เติบโตเล็กน้อยจากปีก่อน จากการมุ่งขยายสาขาของห้างค้าปลีกขนาดใหญ่การเติบโตของ Local Modern Trade รวมทั้งอานิสงส์จากโครงการ “คนละครึ่ง พลัส” ในช่วงไตรมาส 4/2568 ซึ่งช่วยกระตุ้นการใช้จ่ายของผู้บริโภค และกระจายเม็ดเงินสู่ร้านค้าขนาด กลางและขนาดย่อม โดยในปี 2568 บริษัทมีรายได้ของกลุ่มธุรกิจคอมเมอร์เชียลอยู่ที่ 9,602 ล้านบาท เพิ่มขึ้นร้อยละ 6.9 จากช่วงเดียวกันของปีก่อน หากไม่รวมกำไรจากการเปลี่ยนแปลงมูลค่ายุติธรรมของอสังหาริมทรัพย์เพื่อการลงทุน รายได้ของกลุ่มธุรกิจคอมเมอร์เชียลอยู่ที่ 4,467 ล้านบาท เพิ่มขึ้น ร้อยละ 15.3 จากปีก่อน สะท้อนกลยุทธ์การปรับตำแหน่งทางการตลาดของศูนย์การค้าภายใต้แนวคิด AWC’s Lifestyle Destination ซึ่งช่วยเพิ่มอั

  `MDA_AWC_FY2025` · `p026` · SHA bd6408f8778b
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_AWC_FY2025`

##### BLAND — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท บางกอกแลนด์ จำกัด (มหาชน)** — ข้อมูลเทียบเคียงจำกัด: ไม่ควรสรุปเหตุเชื่อมโยงระหว่างรายได้กับกำไร

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ธุรกิจหลักของบริษัทและบริษัทย่อย ได้แก่ ธุรกิจด้านการพัฒนาอสังหาริมทรัพย์เพื่อขาย ธุรกิจอื่นของกลุ่มบริษัทประกอบด้วยธุรกิจค้าปลีก การให้บริการดูแลและบริหารอาคาร ให้เช่าอสังหาริมทรัพย์และให้บริการและบริหารศูนย์นิทรรศการเอนกประสงค์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 9.7bn | 0.56 | +30.2% | 14.7x | — |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 2 · NPAT 2 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 4.0bn → FY2025 THB 4.9bn · +918m

- RFO ปี 2568 อยู่ที่ 4,933 ลบ. เพิ่ม 22.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > IMPACT recorded 4,018 million Baht in rental and service revenue before elimination Related Party Transactions compared to the same period last year 3,3493 million Baht, increased 525 million Baht or 15.0%. IMPACT’s revenue continued to be driven by exhibition space, conference center services, and the food, beverage, and hotel businesses. IMPACT had gross profit margin from rental and services before elimination Related Party Transactions of 37.2% compared to the same period last year 33.4%, increased by 3.8%. This increase was due to the increase of rental and service income, resulting 327 million Baht increase in gross profit.

  `MDA_BLAND_FY2025` · `p009` · SHA 425763ceafa3
  </details>
- RFO ปี 2568 อยู่ที่ 4,933 ลบ. เพิ่ม 22.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนที่ดินนิคมอุตสาหกรรม และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Overview of the Business Operation for year 2024/2025 ended 31 March 2025 The Company and its subsidiaries reported a net profit attributable to the parent company of 656 million Baht, compared to a net profit attributable to the parent company of 958 million Baht in the previous year. This represents an increase of 302 million Baht or 31.5%.The main reasons were as follows: The Company recorded 1,330 million Baht in real estate sales revenue before elimination Related Party Transactions compared to the same period 622 million Baht, increased 708 million Baht or 113.8% which consisted of increased 9 million Baht in land transfers, increased 753 million Baht in condominium transfers, decrease

  `MDA_BLAND_FY2025` · `p008` · SHA fa3c0b6c4fd0
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 579m → FY2025 THB 1.1bn · +555m

- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,134 ลบ. เพิ่ม 95.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ รายได้ค่าเช่าและอัตราการเช่าพื้นที่
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > IMPACT recorded 4,018 million Baht in rental and service revenue before elimination Related Party Transactions compared to the same period last year 3,3493 million Baht, increased 525 million Baht or 15.0%. IMPACT’s revenue continued to be driven by exhibition space, conference center services, and the food, beverage, and hotel businesses. IMPACT had gross profit margin from rental and services before elimination Related Party Transactions of 37.2% compared to the same period last year 33.4%, increased by 3.8%. This increase was due to the increase of rental and service income, resulting 327 million Baht increase in gross profit.

  `MDA_BLAND_FY2025` · `p009` · SHA 425763ceafa3
  </details>
- กำไรสุทธิส่วนผู้ถือหุ้นปี 2568 อยู่ที่ 1,134 ลบ. เพิ่ม 95.9% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนที่ดินนิคมอุตสาหกรรม และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Overview of the Business Operation for year 2024/2025 ended 31 March 2025 The Company and its subsidiaries reported a net profit attributable to the parent company of 656 million Baht, compared to a net profit attributable to the parent company of 958 million Baht in the previous year. This represents an increase of 302 million Baht or 31.5%.The main reasons were as follows: The Company recorded 1,330 million Baht in real estate sales revenue before elimination Related Party Transactions compared to the same period 622 million Baht, increased 708 million Baht or 113.8% which consisted of increased 9 million Baht in land transfers, increased 753 million Baht in condominium transfers, decrease

  `MDA_BLAND_FY2025` · `p008` · SHA fa3c0b6c4fd0
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_BLAND_FY2025`

##### S — ตัวฉุดจากด้อยค่า · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท สิงห์ เอสเตท จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาและลงทุนในอสังหาริมทรัพย์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 3.8bn | 0.55 | +12.2% | n.m. | -9.8% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 5

**RFO — เพราะอะไร** — FY2024 THB 15.1bn → FY2025 THB 14.0bn · −1.1bn · -7.3%

- รายได้ขาย/บริการลดประมาณ 7% จากยอดโอนที่อยู่อาศัยอ่อนตัว แม้การดำเนินงานปกติของโรงแรมและ ธุรกิจพาณิชย์ ยังมีกำไร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > reached THB 88 million, increased 7% from the same period last year, primarily from construction revenue from LA SOIE de S. For 2026, company expects the revenue base to continue being driven by recurring income businesses both hotel and commercial business, alongside continued efforts to enhance the profitability of both segments. Supported revenue and profit growth from real estate sales contribution particularly the land sale from industrial estate, which is currently in strong demand from foreign investors. 1 | Singha Estate PCL. [ General ]

  `MDA_S_FY2025` · `p005` · SHA 04fd35109e7a
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 66m → FY2025 −THB 1.4bn · −1.4bn

- บริษัทพลิกเป็นขาดทุนรายงานหลักจากด้อยค่าสินทรัพย์โรงแรม โดยฝ่ายจัดการระบุกำไรปกติ 531 ลบ. หลังตัดด้อยค่าและรายการไม่ดำเนินงาน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > of accounting losses from asset impairment in the hotel business group. However, if excluding impairment and non-operating items, the company reported normalized net profit amounted to THB 531 million. The revenue from sales of real estate in 2025 amounted to THB 2,358 million comprised of (1) Revenue from sales of houses and condominium units amounted to THB 2,039 million decreased by 38% from the same period last year. Mainly due to lower ownership transferred from The EXTRO Phayathai-Rangnam Condominium project which started transferred in March 2024 after the construction completion. (2) Revenue from sales of industrial estate amounted to THB 319 million from 84 rais of ownership transfe

  `MDA_S_FY2025` · `p004` · SHA 15cfc6b19d96
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: เงินบาทและผลกระทบจากอัตราแลกเปลี่ยน และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Note: Excluded unrealized gain from foreign exchange rate, gain from fair value adjustment on investment properties, loss from impairment, gain from fair value adjustment on investment in joint venture company prior to becoming the Company’s subsidiary, impact from disposal of the Company’s subsidiary, Consulting fees, one-time expenses including expenses related to project initiation, expenses from restructuring, and non-recurring expenses.

  `MDA_S_FY2025` · `p049` · SHA ae887d7a47db
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Profit (loss) attributable to Equity holders of the Company The Company announced total net loss for the fourth quarter of 2025 amounting to THB (2,101) million, which decreased from THB 88 million from the same period last year. The portion attributable to the Owners of the parent in an amount of THB (1,378) million in Q4/2025, declined from THB 32 million in the same period last year. While in 2025 the company reported a total net loss of THB (1,966) million, declining from THB 115 million in 2024. Total attributable to the owners of the parent in an amount of THB (1,366) million decreased from THB 65 million in 2024 mainly due to an accounting impact from asset impairment loss recognition

  `MDA_S_FY2025` · `p069` · SHA b4790821b1a6
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_S_FY2025`

##### CI — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ชาญอิสสระ ดีเวล็อปเมนท์ จำกัด (มหาชน)** — อยู่ในภาวะฟื้นตัว; อัตราเติบโตมีความสำคัญรองลงมา

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — บริษัทดำเนินธุรกิจใน 4 ลักษณะ คือ 1. พัฒนาธุรกิจจัดสรรบ้านและที่ดิน, คอนโดมิเนียมอยู่อาศัยเพื่อขาย 2. ให้เช่าหรือขายอาคารสำนักงานและศูนย์การค้า 3. ประกอบกิจการโรงแรม 4. รับบริหารอาคารสำนักงาน คอนโดมิเนียม บ้านจัดสรร และบริหารโครงการอสังหาริมทรัพย์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 405m | 0.38 | +8.6% | n.m. | -14.9% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 5 · NPAT 6 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 0

**RFO — เพราะอะไร** — FY2024 THB 2.8bn → FY2025 THB 1.8bn · −1.0bn · -36.6%

- RFO ปี 2568 อยู่ที่ 1,762 ลบ. ลด 36.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อุปสงค์และกำลังซื้อในประเทศ และ ภาระหนี้และโครงสร้างเงินทุน และ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ สินเชื่อที่อยู่อาศัยที่เข้มงวดและหนี้ครัวเรือน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue: The company's total revenue was 2,009.3 million baht, a decrease of 933.3 million baht or 31.7% compared to the previous year. The main change came from a 927.1 million baht or 54.4% decrease in real estate sales revenue due to the economic slowdown, high levels of household debt, and tighter lending policies by financial institutions, resulting in customers delaying their home purchase decisions. Furthermore, the economic downturn also impacted the company's hotel business, causing revenue to decrease by 76.1 million baht or 8.2% compared to the previous year. Meanwhile, the company recorded a profit of 63.8 million baht from the sale of its investment in International Resource Dev

  `MDA_CI_FY2025` · `p004` · SHA b56e24586b56
  </details>
- RFO ปี 2568 อยู่ที่ 1,762 ลบ. ลด 36.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายภาษี และ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้ และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  >  The cost of real estate development projects for sale decreased by 202.3 million baht due to the transfer of ownership of properties, mainly condominium units in The Issara Sathorn and Sasara Hua Hin projects, to customers during the period, net of the development costs of The Sky Series Phuket, Sasara Hua Hin, and Baan Issara Bangna projects, which are currently under development.  Income tax assets for the current period decreased by 9.7 million baht due to the reclassification of items to trade receivables and other non-current receivables - deferred income tax from the Revenue Department. In addition, the company had a decrease in real estate transfers during the year, resulting in a

  `MDA_CI_FY2025` · `p010` · SHA a779df6026d5
  </details>
- RFO ปี 2568 อยู่ที่ 1,762 ลบ. ลด 36.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Sales and administrative Expenses: The company had selling and administrative expenses of 604.9 million baht, a decrease of 114.4 million baht, or 15.5%. The overall decrease in expenses stemmed from lower selling expenses, which mirrored the decrease in revenue. Examples include specific business tax, transfer fees, and commissions, administrative expenses decreased as a result of the company's cost control and reduction measures.

  `MDA_CI_FY2025` · `p006` · SHA a00d1cf86d12
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 264m → FY2025 −THB 263m · +2m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -263 ลบ. จาก -264 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ อุปสงค์และกำลังซื้อในประเทศ และ ภาระหนี้และโครงสร้างเงินทุน และ การฟื้นตัวของโรงแรม การท่องเที่ยว และอัตราเข้าพัก และ สินเชื่อที่อยู่อาศัยที่เข้มงวดและหนี้ครัวเรือน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue: The company's total revenue was 2,009.3 million baht, a decrease of 933.3 million baht or 31.7% compared to the previous year. The main change came from a 927.1 million baht or 54.4% decrease in real estate sales revenue due to the economic slowdown, high levels of household debt, and tighter lending policies by financial institutions, resulting in customers delaying their home purchase decisions. Furthermore, the economic downturn also impacted the company's hotel business, causing revenue to decrease by 76.1 million baht or 8.2% compared to the previous year. Meanwhile, the company recorded a profit of 63.8 million baht from the sale of its investment in International Resource Dev

  `MDA_CI_FY2025` · `p004` · SHA b56e24586b56
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -263 ลบ. จาก -264 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ค่าใช้จ่ายภาษี และ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้ และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  >  The cost of real estate development projects for sale decreased by 202.3 million baht due to the transfer of ownership of properties, mainly condominium units in The Issara Sathorn and Sasara Hua Hin projects, to customers during the period, net of the development costs of The Sky Series Phuket, Sasara Hua Hin, and Baan Issara Bangna projects, which are currently under development.  Income tax assets for the current period decreased by 9.7 million baht due to the reclassification of items to trade receivables and other non-current receivables - deferred income tax from the Revenue Department. In addition, the company had a decrease in real estate transfers during the year, resulting in a

  `MDA_CI_FY2025` · `p010` · SHA a779df6026d5
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -263 ลบ. จาก -264 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ การควบคุมต้นทุนและประสิทธิภาพการดำเนินงาน และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Sales and administrative Expenses: The company had selling and administrative expenses of 604.9 million baht, a decrease of 114.4 million baht, or 15.5%. The overall decrease in expenses stemmed from lower selling expenses, which mirrored the decrease in revenue. Examples include specific business tax, transfer fees, and commissions, administrative expenses decreased as a result of the company's cost control and reduction measures.

  `MDA_CI_FY2025` · `p006` · SHA a00d1cf86d12
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -263 ลบ. จาก -264 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Costs: The company's total cost of sales amounted to 1,322.6 million baht, a decrease of 656.6 million baht or 33.2 percent. This change is in line with the decrease in revenue from the company's real estate sales.

  `MDA_CI_FY2025` · `p005` · SHA 5443f4c1d550
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_CI_FY2025`

#### ทะเบียนข้อสรุป — P4

| ส่วน | ประเภท | ข้อสรุป | รหัสแหล่งข้อมูล |
|---|---|---|---|
| headline | ข้ออนุมานนักวิเคราะห์ | AWC ส่งมอบการเติบโต แต่ด้อยค่าของ S ฉุดภาพรวม | FY_PANEL, P4_E1, P4_E2 |
| earnings_fact | ข้อเท็จจริงจากการคำนวณ | FY2025 RFO -2.0%; สถานะ NPAT ส่วนผู้ถือหุ้น: profit_decreased | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | กลุ่มปิดงบธันวาคม 3/4 บริษัทมี RFO -2.0% และ NPAT -15.8%; BLAND ถูกตัดออกเพราะปิดงบมีนาคม | FY_PANEL |
| why | คำอธิบายฝ่ายจัดการ | AWC เพิ่ม RFO และ NPAT แต่มี fair-value gain 5,555 ล้านบาท จึงต้อง bridge จาก operating ไป reported | P4_E1, P4_E2 |
| why | คำอธิบายฝ่ายจัดการ | S บันทึกด้อยค่า 1,963 ล้านบาท ขณะที่กำไรปกติ 531 ล้านบาท | P4_E1, P4_E2 |
| causal_chain | ข้ออนุมานนักวิเคราะห์ | ห่วงโซ่เหตุ: นักท่องเที่ยว → Occupancy / ADR → Asset ramp → EBITDA → NPAT | P4_E1, P4_E2 |
| roles | ข้ออนุมานนักวิเคราะห์ | บทบาท: ผู้นำและส่งมอบการดำเนินงาน — AWC; ตัวฉุดจากด้อยค่า — S | FY_PANEL, P4_E1, P4_E2 |
| valuation | ข้ออนุมานนักวิเคราะห์ | P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 14.9x ครอบคลุม 2/4 บริษัท และ 96.2% ของ market cap ที่มีข้อมูล. ราคาสะท้อน tourism และ asset optionality แต่ต้องพิสูจน์กำไรเงินสดปกติ | SET_PUBLIC_EOD, P4_E1, P4_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | occupancy และ ADR เพิ่ม | P4_E1, P4_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | สินทรัพย์ใหม่ ramp-up ตามแผน | P4_E1, P4_E2 |
| trigger | ประเด็นที่ต้องพิสูจน์ | นักท่องเที่ยวฟื้นหลายตลาด | P4_E1, P4_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | ความเสี่ยงท่องเที่ยว | P4_E1, P4_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | ต้นทุนคงที่และ leverage สูง | P4_E1, P4_E2 |
| risk | ประเด็นที่ต้องพิสูจน์ | asset ramp-up ล่าช้า | P4_E1, P4_E2 |
| must_prove | ประเด็นที่ต้องพิสูจน์ | 6M26 ต้องแปลง occupancy และ ADR เป็นกำไรส่วนผู้ถือหุ้นและ cash flow | P4_E1, P4_E2 |

#### ทะเบียนหลักฐาน — P4

- **`FY_PANEL`** · _ข้อเท็จจริงจากการคำนวณ_ — Audited FY2024-25 company panel
  - RFO / NPAT-to-owners / independent panel membership; QA 43 pass / 0 fail
  - บทบาท: historical fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_company_fy2024_2025_audited_2026-08-07.csv`
  - SHA-256: `e5e04dbc40ffcc79fed58545a93dc4549c29cdaecf260bea73711bc6d0720481`
- **`SET_PUBLIC_EOD`** · _ข้อเท็จจริงจากการคำนวณ_ — SET public Company Highlights — EOD 2026-08-07
  - Adjusted YTD; unadjusted price, market cap and valuation; factsheet-surface cross-check
  - บทบาท: current market fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_set_public_surface_reconciliation_2026-08-07.csv`
  - SHA-256: `544c1f29fe2d409ee398822ac2bf32b769081718962ae2d1138985b0146b9530`
- **`SET_COMPANY_PROFILE`** · _ข้อเท็จจริง_ — SET company profiles — English and Thai
  - Official company names and business descriptions refreshed and validated for the 118-company perimeter from the public SET profile API
  - บทบาท: company business profile
  - URL: <https://www.set.or.th/th/market/product/stock/overview>
- **`COMPANY_REPORTS`** · _ข้ออนุมานนักวิเคราะห์_ — Company report synthesis corpus
  - Annual-only draft synthesis; reconciled to the ticker FY2025 MD&A where available
  - บทบาท: secondary synthesis; not management attribution
  - พาธ: `data/company-reports.json`
  - SHA-256: `c1a2bc40cbe21a2058aa596c362e4d47ad117360831b847de78ec414831fd2d2`
- **`MDA_AWC_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — AWC FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/AWC/MDA_AWC_2025FY_T.md`
  - SHA-256: `2e9c4bd03a9250934e76fd46e9da933bffc6a7a15f2ab75fbaad9a0a2dede7b2`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202602/1523NWS260220262132193340T.pdf>
- **`MDA_BLAND_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — BLAND FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/BLAND/MDA_BLAND_2025FY_E.md`
  - SHA-256: `49b45a931911529d88a471a935d3626e9f87692e37ab48b7016bc2265f95360e`
  - URL: <https://market.sec.or.th/public/idisc/Download?FILEID=dat/news/202505/0285NWS290520251826560429E.pdf>
- **`MDA_S_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — S FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/S/MDA_S_2025FY_E.md`
  - SHA-256: `fae0ac3a16b6abd9a517af3bcbe17de7bf12f5725f89d7d953ca20d5280f3cee`
  - URL: <https://weblink.set.or.th/dat/news/202602/0940NWS270220261745304930E.pdf>
- **`MDA_CI_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — CI FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/CI/MDA_CI_2025FY_E.md`
  - SHA-256: `711e95310552b509604d74603e9910605c0ed319f07a7764745dcedf6161a082`
  - URL: <https://weblink.set.or.th/dat/news/202602/0696NWS270220261729328670E.pdf>
- **`P4_E1`** · _ฝ่ายจัดการ_ — AWC FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/AWC/MDA_AWC_2025FY_E.md`
  - SHA-256: `dce09f7118db4f73aa1f8b315feff5beb5e731e459441e1e91c0482686a54824`
- **`P4_E2`** · _ฝ่ายจัดการ_ — S FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/S/MDA_S_2025FY_E.md`
  - SHA-256: `fae0ac3a16b6abd9a517af3bcbe17de7bf12f5725f89d7d953ca20d5280f3cee`
- **`P4_FACTSHEET`** · _ข้อเท็จจริงจากการคำนวณ_ — SET Factsheet — AWC
  - Live leader cross-check
  - บทบาท: presentation-surface check
  - URL: <https://www.set.or.th/th/market/product/stock/quote/awc/factsheet>

### P5 · กระจายธุรกิจและปรับโครงสร้าง — กลุ่มที่ปรับใหม่ยังขาดทุน แต่ขาดทุนลดลง

`Event-driven` · 1.4% M-cap · THB 11.4bn · 5 บริษัท

| ตัวชี้วัด | RFO | NPAT | ราคา | P/E |
|---|---|---|---|---|
| ช่วง | FY2025 YoY | ส่วนผู้ถือหุ้น FY2025 YoY | ราคา YTD ปรับแล้ว | เฉพาะบริษัทที่มีกำไร |
| ค่า | -14.2% | ขาดทุนลดลง | +42.3% | 8.5x |
| จำนวน | THB 7.9bn FY2025 | −THB 2.7bn FY2025 | ณ 7 ส.ค. 2569 | ค่าเฉลี่ยรวม |
| ครอบคลุม | 4/5 | 4/5 | 5/5 • 100% M-cap | 1/5 • 24% M-cap |

**ข้อเท็จจริงที่สังเกตได้** — FY2025: RFO -14.2% • NPAT ขาดทุนลดลง • ราคา YTD +42.3% • P/E 8.5x • ครอบคลุม RFO 4/5 • NPAT 4/5

#### เหตุผลที่เปลี่ยน

1. _ข้อเท็จจริงจากการคำนวณ_ · ปรับโครงสร้าง — RFO ลด 14.2% ขณะที่ขาดทุนส่วนผู้ถือหุ้นลดจาก 3,020 ล้านบาทเป็น 2,653 ล้านบาท
2. _ข้ออนุมานนักวิเคราะห์_ · ขายสินทรัพย์ — การพลิกตัวที่ได้รับอิทธิพลจาก event ของ RABBIT ชดเชยการอ่อนตัวของ STELLA และ CGD
3. _ข้อเท็จจริงจากการคำนวณ_ · หนี้ / สภาพคล่อง — UV เป็นตัวเทียบต่างรอบปีและไม่รวมในกลุ่มผลประกอบการปิดงบธันวาคม

#### ห่วงโซ่เหตุและผล

**ปรับโครงสร้าง** → **ขายสินทรัพย์** → **หนี้ / สภาพคล่อง** → **กำไรหลัก** (ขาดทุนลดลง −THB 2.7bn FY2025) → **Re-rating** (8.5x YTD +42.3%)

#### บทบาทในกลุ่ม

| บทบาท | Ticker | ค่า | ที่มาของค่า |
|---|---|---|---|
| ผู้นำและตัวฉุดขาดทุน | STELLA | 50% | สัดส่วน Market Cap ในกลุ่ม |
| ตัวแปรกำไรจาก event | RABBIT | กลับเป็นกำไร | NPAT YoY · Δ +1.4bn |
| ตัวเทียบต่างรอบปี | UV | n.m. | P/E · YTD +18.8% |

#### มูลค่า

**Event-driven / เปรียบเทียบจำกัด** — P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 8.5x ครอบคลุม 1/5 บริษัท และ 23.6% ของ market cap ที่มีข้อมูล. P/E ขับเคลื่อนด้วย event และไม่เป็นตัวแทนกลุ่มที่ขาดทุน

| Trigger | Risk |
|---|---|
| ปรับโครงสร้างเสร็จและได้เงินสดจริง | กำไรพิเศษบดบังขาดทุนหลัก |
| หนี้และสภาพคล่องดีขึ้น | leverage และ refinancing |
| ธุรกิจหลักกลับมามีกำไร | ธรรมาภิบาลและ execution risk |

**6M26 ต้องพิสูจน์** — 6M26 ต้องแยกกำไรประจำออกจาก one-off และแสดงฐานะการเงินที่ดีขึ้น

#### วิเคราะห์รายบริษัท — P5 กระจายธุรกิจและปรับโครงสร้าง

_ทุกบริษัทใน perimeter ของ Segment ที่สอบทาน_

| Ticker | บทบาท | M-cap | RFO YoY | NPAT YoY | ราคา YTD | P/E | Margin |
|---|---|---|---|---|---|---|---|
| STELLA | ผู้นำและตัวฉุดขาดทุน | THB 5.7bn | -7.1% | ขาดทุนเพิ่มขึ้น | +73.3% | n.m. | -332.7% |
| RABBIT | ตัวแปรกำไรจาก event | THB 2.7bn | +12.7% | กลับเป็นกำไร | +33.3% | 8.5x | 19.6% |
| UV | ตัวเทียบต่างรอบปี | THB 1.9bn | — | — | +18.8% | n.m. | — |
| CGD | บริษัทในกลุ่ม | THB 827m | -72.0% | ขาดทุนเพิ่มขึ้น | -9.1% | n.m. | -101.1% |
| EVER | บริษัทในกลุ่ม | THB 291m | -22.6% | ขาดทุนลดลง | +50.0% | n.m. | -12.5% |

##### STELLA — ผู้นำและตัวฉุดขาดทุน · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท สเตลล่า เอ็กซ์ จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 5.7bn | 0.26 | +73.3% | n.m. | -332.7% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 4 · NPAT 10 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 6

**RFO — เพราะอะไร** — FY2024 THB 950m → FY2025 THB 882m · −68m · -7.1%

- RFO ปี 2568 อยู่ที่ 882 ลบ. ลด 7.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ราคาขายและส่วนผสมผลิตภัณฑ์ และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายขายและบริหาร และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Stella Cost of real estate sold increased by Baht 181 million, or 30% from the previous year, due to the recognition of impairment allowances on land and condominium units totaling Baht 321 million, in order to reflect the expected selling prices that the Company anticipates to receive from the future sale of such land and condominium units, Excluding this item, cost of sales from real estate would have amounted to Baht 456 million, representing a decrease of Baht 101 million or 17% from the previous year. Cost of rental and service decreased by Baht 56 million or 18% from the previous year, in line with the decrease in related revenue. Administrative expenses increased by Baht 106 million f

  `MDA_STELLA_FY2025` · `p018` · SHA cea792f661ce
  </details>
- RFO ปี 2568 อยู่ที่ 882 ลบ. ลด 7.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ อุปสงค์และกำลังซื้อในประเทศ และ รายได้เงินปันผล
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > from such investments), representing a 100% decrease, and a decline in dividend income of Baht 74 million, or 46%. The decrease in revenue was not related to the Company's core operating income. Revenue from the Company's core business experienced only a slight decline due to the economic slowdown, reflecting the underlying stability of the Company's core operations.

  `MDA_STELLA_FY2025` · `p003` · SHA 6fa0b341d45c
  </details>
- RFO ปี 2568 อยู่ที่ 882 ลบ. ลด 7.1% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Percentage 30% (100%) (18%) 23% (1%) 22% (100%) 45% 100% (100%) 100% (100%) 26% 62% (17%) (5%) 48% 100% 46% For the year ended 31 December 2025, compared to the previous year, the Company reported the following: • Net loss for 2025 was Baht 2,988 million, representing a increase of 46% (2024: net loss of Baht 2,052 million). • Loss from operating activities for 2025 was Baht 2,630 million, representing a increase of 62% (2024: loss of Baht 1,626 million). Revenue from the real estate amounted to Baht 462 million, representing a decrease of Baht 11 million or 2% from the previous year. The decrease was primarily attributable to the fact that, in 2024, the Company recorded a big lot sale of 16

  `MDA_STELLA_FY2025` · `p015` · SHA 5c565b68feaf
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 2.0bn → FY2025 −THB 2.9bn · −923m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -2,935 ลบ. จาก -2,012 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ราคาขายและส่วนผสมผลิตภัณฑ์ และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายขายและบริหาร และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Stella Cost of real estate sold increased by Baht 181 million, or 30% from the previous year, due to the recognition of impairment allowances on land and condominium units totaling Baht 321 million, in order to reflect the expected selling prices that the Company anticipates to receive from the future sale of such land and condominium units, Excluding this item, cost of sales from real estate would have amounted to Baht 456 million, representing a decrease of Baht 101 million or 17% from the previous year. Cost of rental and service decreased by Baht 56 million or 18% from the previous year, in line with the decrease in related revenue. Administrative expenses increased by Baht 106 million f

  `MDA_STELLA_FY2025` · `p018` · SHA cea792f661ce
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -2,935 ลบ. จาก -2,012 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Loss from impairment of assets amounted to Baht 118 million, arising from the recognition of impairment allowances on land deposits and investment properties, in order to reflect values consistent with expected future sales proceeds. Loss from investments in equity instruments designated at fair value through profit or loss amounted to Baht 56 million, resulting from fair value adjustments of such investments.

  `MDA_STELLA_FY2025` · `p019` · SHA ad98d2653d93
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -2,935 ลบ. จาก -2,012 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Percentage 30% (100%) (18%) 23% (1%) 22% (100%) 45% 100% (100%) 100% (100%) 26% 62% (17%) (5%) 48% 100% 46% For the year ended 31 December 2025, compared to the previous year, the Company reported the following: • Net loss for 2025 was Baht 2,988 million, representing a increase of 46% (2024: net loss of Baht 2,052 million). • Loss from operating activities for 2025 was Baht 2,630 million, representing a increase of 62% (2024: loss of Baht 1,626 million). Revenue from the real estate amounted to Baht 462 million, representing a decrease of Baht 11 million or 2% from the previous year. The decrease was primarily attributable to the fact that, in 2024, the Company recorded a big lot sale of 16

  `MDA_STELLA_FY2025` · `p015` · SHA 5c565b68feaf
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -2,935 ลบ. จาก -2,012 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ เงินทุนหมุนเวียน สินค้าคงเหลือ และลูกหนี้
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Executive Summary Stella X Public Company Limited and its subsidiaries ("the Company") would like to explain its operating results for the year ended 31 December 2025. The Company reported a net loss of Baht 2,988 million, compared with a net loss of Baht 2,052 million in the previous year, representing an increase in loss of Baht 936 million or 46%. The Company recognized additional allowances for impairment of land and deposits for purchase of land, as well as allowances for doubtful accounts in respect of accrued interest receivable and loans, in order to adjust the accounting records to reflect appropriate values consistent with the current situation. Such adjustments were made to ensure

  `MDA_STELLA_FY2025` · `p002` · SHA 7c65a58a9714
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Loss from impairment of assets amounted to Baht 118 million, arising from the recognition of impairment allowances on land deposits and investment properties, in order to reflect values consistent with expected future sales proceeds. Loss from investments in equity instruments designated at fair value through profit or loss amounted to Baht 56 million, resulting from fair value adjustments of such investments.

  `MDA_STELLA_FY2025` · `p019` · SHA ad98d2653d93
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ราคาขายและส่วนผสมผลิตภัณฑ์ และ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายขายและบริหาร และ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Stella Cost of real estate sold increased by Baht 181 million, or 30% from the previous year, due to the recognition of impairment allowances on land and condominium units totaling Baht 321 million, in order to reflect the expected selling prices that the Company anticipates to receive from the future sale of such land and condominium units, Excluding this item, cost of sales from real estate would have amounted to Baht 456 million, representing a decrease of Baht 101 million or 17% from the previous year. Cost of rental and service decreased by Baht 56 million or 18% from the previous year, in line with the decrease in related revenue. Administrative expenses increased by Baht 106 million f

  `MDA_STELLA_FY2025` · `p018` · SHA cea792f661ce
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_STELLA_FY2025`

##### RABBIT — ตัวแปรกำไรจาก event · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท แรบบิท โฮลดิ้งส์ จำกัด (มหาชน)** — อยู่ในภาวะฟื้นตัว; อัตราเติบโตมีความสำคัญรองลงมา

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — พัฒนาอสังหาริมทรัพย์เพื่อการให้เช่า บริการ จำหน่าย และบริหารอย่างครบวงจร

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 2.7bn | 0.36 | +33.3% | 8.5x | 19.6% |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 8

**RFO — เพราะอะไร** — FY2024 THB 4.6bn → FY2025 THB 5.2bn · +582m · +12.7%

- รายได้เพิ่ม 42% จากยอดขายอสังหาริมทรัพย์และรายได้ประกัน/บริการการเงินที่ขยายตัว
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In FY 2025, the Company reported total consolidated revenue of THB 7,837mn, increasing by THB 2,328mn or 42.3% YoY from THB 5,509mn compared to FY 2024. The increase in total consolidated revenue was chiefly attributed to (i) higher gain on sales of investment in subsidiaries and joint venture of THB 1,362mn due to the disposal of Diplomat Prague and KE, (ii) revenue from sale of real estate and construction of THB 657mn from The Residences 38, and (iii) higher gain on fair value measurement of financial assets of THB 197mn, mainly from life insurance business’s investments in financial assets. However, the increase was partially offset by decreases in (iv) revenue from hotel operation of TH

  `MDA_RABBIT_FY2025` · `p027` · SHA 169a0cd267b6
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 418m → FY2025 THB 1.0bn · +1.4bn

- บริษัทกลับมามีกำไรเมื่อฐานรายได้ที่สูงขึ้นและรายการต่ำกว่าการดำเนินงานชดเชยส่วนแบ่งขาดทุนบริษัทร่วม/JV 457 ลบ.
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 36.8% YoY, mainly from the decrease in insurance contracts with unavoidable losses, (ii) loss from exchange rate of THB 120mn, and (iii) loss on impairment of assets and expected credit loss of THB 99mn or 60.5% YoY. However, the decrease was supported by increases in (iv) cost of real estate sales and construction of THB 522mn, mainly from the transfer of the residential condominium units to the customers of The Residences 38, and (v) selling and servicing expenses of THB 73mn or 24.3% YoY. The reported share of loss from associate/JVs were THB 457mn, compared with share of profit of THB 236mn in FY 2024. The share of losses was attributable to (i) THB 521mn from investments in other JVs an

  `MDA_RABBIT_FY2025` · `p028` · SHA f59571227be1
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการวัดมูลค่ายุติธรรม และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า และ การซื้อกิจการและการรวมงบการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > In FY 2025, the Company reported total consolidated revenue of THB 7,837mn, increasing by THB 2,328mn or 42.3% YoY from THB 5,509mn compared to FY 2024. The increase in total consolidated revenue was chiefly attributed to (i) higher gain on sales of investment in subsidiaries and joint venture of THB 1,362mn due to the disposal of Diplomat Prague and KE, (ii) revenue from sale of real estate and construction of THB 657mn from The Residences 38, and (iii) higher gain on fair value measurement of financial assets of THB 197mn, mainly from life insurance business’s investments in financial assets. However, the increase was partially offset by decreases in (iv) revenue from hotel operation of TH

  `MDA_RABBIT_FY2025` · `p027` · SHA 169a0cd267b6
  </details>
- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์ และ ส่วนแบ่งกำไรหรือขาดทุนจากบริษัทร่วมและการร่วมค้า
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Total Liabilities as of 31 December 2025 were THB 28,134mn, decreasing by THB 1,413mn or 4.8%, from THB 29,547mn at the end of 2024. The decrease was attributed chiefly due to a decrease in (i) net portion of loans from financial institutions of THB 2,080mn, mainly from the repayment of loans after the disposal of investment in Diplomat Prague, (ii) provision for transaction under equity method of investments in joint ventures of THB 636mn, and (iii) deferred tax liabilities of THB 174mn. However, the decrease was partially supported by an increase in (iv) net portion of long-term investment contract liabilities of THB 1,051mn, mainly from the increase in short-term endowment insurance contr

  `MDA_RABBIT_FY2025` · `p061` · SHA c29ae4845f0b
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_RABBIT_FY2025`

##### UV — ตัวเทียบต่างรอบปี · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท ยูนิเวนเจอร์ จำกัด (มหาชน)** — ข้อมูลเทียบเคียงจำกัด: ไม่ควรสรุปเหตุเชื่อมโยงระหว่างรายได้กับกำไร

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ลงทุนในกิจการอื่น โดยกลุ่มบริษัทดำเนินธุรกิจหลัก 3 สายธุรกิจ ได้แก่ (1) ธุรกิจการลงทุน ซึ่งปัจจุบันบริษัทย่อยของบริษัทเข้าลงทุนในธุรกิจพลังงาน ธุรกิจตู้แช่เชิงพาณิชย์ และธุรกิจที่ปรึกษาบริหารและควบคุมงานก่อสร้าง (2) ธุรกิจอสังหาริมทรัพย์และธุรกิจที่เกี่ยวข้อง(3) ธุรกิจด้านอุตสาหกรรม ได้แก่ ธุรกิจผลิตและจำหน่ายผงสังกะสีออกไซด์และเคมีภัณฑ์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 1.9bn | 1.01 | +18.8% | n.m. | — |

สังเคราะห์โดยมี MD&A รองรับ · หลักฐานรายข้อ — RFO 1 · NPAT 1 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 16.1bn → FY2025 THB 15.3bn · −751m

- รายได้หลักจากขาย บริการ และให้เช่าลด 9% เหลือ 14.17 พันลบ. หลักจากรายได้อสังหาฯ ลด 38% เพราะโอนคอนโดลดหลังแผ่นดินไหวและสินเชื่อเข้มขึ้น ขณะที่อุตสาหกรรมลด 8% จากปริมาณ ซิงก์ออกไซด์ ลดลง
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > รายได้จากการขาย บริการและให้เช่า บริษัทฯ มีรายได้จากการขาย บริการและให้เช่า ("รายได้หลัก") สำหรับปีสิ้นสุดวันที่ 30 กันยายน 2568 จำนวน 14,172.3 ล้านบาท ปรับลดลง 1,464.0 ล้านบาท หรือคิดเป็นร้อยละ 9 เมื่อเปรียบเทียบกับปีก่อน สาเหตุหลักๆ เนื่องจาก • รายได้จากธุรกิจอสังหาริมทรัพย์และธุรกิจที่เกี่ยวข้องปรับลดลง 1,413.8 ล้านบาท หรือคิดเป็นร้อยละ 38 เมื่อเปรียบเทียบกับช่วงเดียวกันของปีก่อน จากการโอนกรรมสิทธิ์ห้องชุดของธุรกิจอสังหาริมทรัพย์ลดลง เป็นไป

  `MDA_UV_FY2025` · `p022` · SHA 167fbfd436ad
  </details>

**NPAT — เพราะอะไร** — FY2024 THB 367m → FY2025 THB 53m · −314m

- กำไรปกติลดลงเพราะฐานอสังหาฯ ที่ต่ำลงและค่าใช้จ่ายบริหาร/ภาษีเพิ่ม มากกว่าดอกเบี้ยที่ลดลง; NPAT ส่วนบริษัทใหญ่พลิกเป็นขาดทุน 45 ลบ. แม้กำไรสุทธิรวมยังเป็นบวก
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > ต้นทุนจากการขาย บริการและให้เช่า บริษัทฯ มีต้นทุนจากการขาย บริการและให้เช่า ("ต้นทุนหลัก") สำหรับปีสิ้นสุดวันที่ 30 กันยายน 2568 จำนวน 11,973.9 ล้านบาท ประกอบด้วย ต้นทุนขายและต้นทุนการให้บริการ 10,628.3 ล้านบาท ต้นทุนขายอสังหาริมทรัพย์ 1,289.6 ล้านบาท ต้นทุนจากการให้เช่าและบริการ 52.6 ล้านบาท และต้นทุนค่าการจัดการ 3.4 ล้านบาท โดยต้นทุนหลักปรับลดลง 1,172.9 ล้านบาท หรือคิดเป็นร้อยละ 9 เมื่อเปรียบเทียบกับปีก่อน สาเหตุหลักๆ เนื่องจาก • ต้นทุนขายอสังหาริมทรัพย์ปรับลดลง 1,020.1 ล้านบาท หรือคิดเป็นร้อยละ 44 เมื่อเปรียบเทียบกับช่วงเดียวกันของ ปีก่อน สอดคล้องกับการปรับลดลงของรายได้ ในขณะที่คงระดับอัตรากำไรขั้นต้นไว้ได้อยู่ที่ร้อยละ 23 • ต้นทุนขายธุรกิจอุตสาหกรรมปรับลดลง 54.4 ล้านบาทหรือคิดเป็นร้อยละ

  `MDA_UV_FY2025` · `p025` · SHA 029f780ed5cd
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- กำไรสุทธิรวมมีค่าสินไหมประกัน 241 ลบ. กำไร FX ที่ยังไม่เกิด 24.5 ลบ. และ กำไรจากการวัดมูลค่ายุติธรรม 18.4 ลบ. จึงต้องแยกอ่าน NPAT ส่วนบริษัทใหญ่
  <details><summary>ข้อความ MD&A ต้นทาง · TH</summary>

  > กำไรก่อนต้นทุนทางการเงิน ภาษี ค่าเสื่อมราคาและค่าตัดจำหน่าย บริษัทฯ มีกำไรก่อนต้นทุนทางการเงิน ภาษี ค่าเสื่อมราคาและค่าตัดจำหน่าย สำหรับปีสิ้นสุดวันที่ 30 กันยายน 2568 จำนวน 2,303.6 ล้านบาท (รวมกำไรที่ยังไม่เกิดขึ้นจากอัตราแลกเปลี่ยน 24.5 ล้านบาท กำไรจากการเปลี่ยนแปลงมูลค่ายุติธรรม ของอสังหาริมทรัพย์เพื่อการลงทุน 18.4 ล้านบาท และเงินชดเชยสินไหมทดแทนจากประกันภัย 241.3 ล้านบาท) ปรับลดลง 28.6 ล้านบาท จากช่วงเดียวกันของปีก่อนซึ่งอยู่ที่ 2,332.2 ล้านบาท บริษัทฯ มีกำไรจากการดำเนินงานตามงบการเงิน สำหรับปีสิ้นสุดวันที่ 30 กันยายน 2568 จำนวน 1,176.9 ล้านบาท ปรับลดลง 16.9 ล้านบาท เปรียบเทียบกับช่วงเดียวกันของปีก่อน ที่มีกำไรจากการดำเนินงานตามงบการเงินอยู่ที่ 1,193.88 ล้านบาท ซึ่งหากไม่รวมค่าตัดจำหน่าย

  `MDA_UV_FY2025` · `p030` · SHA c548b7a9bea8
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_UV_FY2025`

##### CGD — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท คันทรี่ กรุ๊ป ดีเวลลอปเมนท์ จำกัด (มหาชน)** — แรงกดดันกำไรมากกว่าสัญญาณรายได้

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ประกอบธุรกิจการลงทุนโดยถือหุ้นในบริษัทอื่น (Holding Company) และธุรกิจอสังหาริมทรัพย์

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 827m | 0.10 | -9.1% | n.m. | -101.1% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 7 · NPAT 9 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 2.0bn → FY2025 THB 561m · −1.4bn · -72.0%

- RFO ปี 2568 อยู่ที่ 561 ลบ. ลด 72.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ การเปลี่ยนแปลงของอัตรากำไร และ ปริมาณขายและปริมาณการผลิต และ ราคาขายและส่วนผสมผลิตภัณฑ์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue - The Group's total revenue for this period was Baht 968.5 million, representing a 59.8% decrease compared to the same period last year, primarily attributable to a market downturn in the real estate sector. We implemented a new pricing strategy that has allowed us to achieve higher selling prices. While this strategy has supported our overall profitability, it has also contributed to a decline in sales volume. However, due to our strategic pricing adjustments, the impact on our gross margin has been less severe than anticipated. Despite these challenges, ordinary revenue from sales of FSPR continued to be the primary contributor to our total revenues, with further details as follows

  `MDA_CGD_FY2025` · `p015` · SHA e91fc6b0e00a
  </details>
- RFO ปี 2568 อยู่ที่ 561 ลบ. ลด 72.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Operating performance - The Group reported a net loss amount of Baht 576.0 million compared with a net loss of Baht 148.5 million of the same period last year. This mainly resulted from a decrease in revenue and cost from sale of condominiums. page 4/4 Country Group Development PCL. 898 Ploenchit Tower, 20th Floor, Ploenchit Rd., Lumpini, Pathumwan, Bangkok 10330 Thailand T +66 2658 7888 | F +66 2658 7880 | www.cgd.co.th

  `MDA_CGD_FY2025` · `p021` · SHA 506ac0c84533
  </details>
- RFO ปี 2568 อยู่ที่ 561 ลบ. ลด 72.0% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Operating loss - The Group reported total operating loss of Baht 97.0 million, a decrease of 122.2% over the same period last year, due to decrease in revenues as mention above. Total cost, selling and administrative expense decreased by Baht 908.9 million which is a decrease of 46.0% in respect to decrease in revenue. In addition, the operating loss was further impacted by impairment losses in accordance with TFRS 19 and increased litigation expenses related to legal proceedings against the project contractor. Consequently, operating profits decreased compared to the same period last year.

  `MDA_CGD_FY2025` · `p019` · SHA c9b8630b9f55
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 252m → FY2025 −THB 568m · −316m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -568 ลบ. จาก -252 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Operating loss - The Group reported total operating loss of Baht 97.0 million, a decrease of 122.2% over the same period last year, due to decrease in revenues as mention above. Total cost, selling and administrative expense decreased by Baht 908.9 million which is a decrease of 46.0% in respect to decrease in revenue. In addition, the operating loss was further impacted by impairment losses in accordance with TFRS 19 and increased litigation expenses related to legal proceedings against the project contractor. Consequently, operating profits decreased compared to the same period last year.

  `MDA_CGD_FY2025` · `p019` · SHA c9b8630b9f55
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -568 ลบ. จาก -252 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Financial Income/Expense - The Group reported financial income of Baht 107.6 million, representing a decrease of 17.8% from the previous period. The decline was mainly due to lower interest income from loans to related companies and from deposits with financial institutions. - The Group reported finance costs of Baht 587.8 million, a decrease of 5.3% from the same period last year, primarily due to the repayment of debentures and short-term borrowings.

  `MDA_CGD_FY2025` · `p020` · SHA ae1558aa8110
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -568 ลบ. จาก -252 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ การเปลี่ยนแปลงของอัตรากำไร และ ปริมาณขายและปริมาณการผลิต และ ราคาขายและส่วนผสมผลิตภัณฑ์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Revenue - The Group's total revenue for this period was Baht 968.5 million, representing a 59.8% decrease compared to the same period last year, primarily attributable to a market downturn in the real estate sector. We implemented a new pricing strategy that has allowed us to achieve higher selling prices. While this strategy has supported our overall profitability, it has also contributed to a decline in sales volume. However, due to our strategic pricing adjustments, the impact on our gross margin has been less severe than anticipated. Despite these challenges, ordinary revenue from sales of FSPR continued to be the primary contributor to our total revenues, with further details as follows

  `MDA_CGD_FY2025` · `p015` · SHA e91fc6b0e00a
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 เพิ่มขึ้นเป็น -568 ลบ. จาก -252 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Net Operating performance - The Group reported a net loss amount of Baht 576.0 million compared with a net loss of Baht 148.5 million of the same period last year. This mainly resulted from a decrease in revenue and cost from sale of condominiums. page 4/4 Country Group Development PCL. 898 Ploenchit Tower, 20th Floor, Ploenchit Rd., Lumpini, Pathumwan, Bangkok 10330 Thailand T +66 2658 7888 | F +66 2658 7880 | www.cgd.co.th

  `MDA_CGD_FY2025` · `p021` · SHA 506ac0c84533
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: รายการด้อยค่าและการตัดจำหน่ายสินทรัพย์ และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Operating loss - The Group reported total operating loss of Baht 97.0 million, a decrease of 122.2% over the same period last year, due to decrease in revenues as mention above. Total cost, selling and administrative expense decreased by Baht 908.9 million which is a decrease of 46.0% in respect to decrease in revenue. In addition, the operating loss was further impacted by impairment losses in accordance with TFRS 19 and increased litigation expenses related to legal proceedings against the project contractor. Consequently, operating profits decreased compared to the same period last year.

  `MDA_CGD_FY2025` · `p019` · SHA c9b8630b9f55
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_CGD_FY2025`

##### EVER — บริษัทในกลุ่ม · เปลี่ยนแปลงมีนัยสำคัญ

**บริษัท เอเวอร์แลนด์ จำกัด (มหาชน)** — อยู่ในภาวะฟื้นตัว; อัตราเติบโตมีความสำคัญรองลงมา

_ธุรกิจหลัก · SET Factsheet ผ่าน IS1 Coverage_ — ธุรกิจอสังหาริมทรัพย์และธุรกิจโรงพยาบาล

| M-cap | ราคา (THB) | YTD | P/E | NPAT / RFO |
|---|---|---|---|---|
| THB 291m | 0.06 | +50.0% | n.m. | -12.5% |

ดึงคำอธิบายตรงจาก MD&A · หลักฐานรายข้อ — RFO 15 · NPAT 17 · รายการพิเศษ / ต่ำกว่าการดำเนินงาน 1

**RFO — เพราะอะไร** — FY2024 THB 1.7bn → FY2025 THB 1.3bn · −379m · -22.6%

- RFO ปี 2568 อยู่ที่ 1,302 ลบ. ลด 22.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > MB %to total MB %to total MB % Change income income Revenues from sales - Realrestate 846.20 54.99% 1,235.39 72.36% (389.19) (31.50%) Revenues from sales - Hospital 455.56 29.60% 445.74 26.11% 9.82 2.20% Total revenues from sales 1,301.76 84.59% 1,681.13 98.47% (379.37) (22.57%)

  `MDA_EVER_FY2025` · `p011` · SHA 479887862e74
  </details>
- RFO ปี 2568 อยู่ที่ 1,302 ลบ. ลด 22.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Amount % To Amount % To Amount % To (MB) Revenue (MB) Revenue (MB) Revenue Revenues from sales and revenues from services 1,301.76 84.57% 1,681.13 98.45% (379.37) -22.57% Costs of sales of goods and costs of rendering of services (1,096.19) -71.21% (1,348.95) -78.99% (252.76) -18.74% Gross profit 205.57 13.36% 332.18 19.45% (126.61) -38.11% Other income 237.18 15.41% 26.19 1.53% 210.99 805.61% Distribution costs (117.78) -7.65% (134.88) -7.90% (17.10) -12.68% Administrative expenses (263.83) -17.14% (319.43) -18.71% (55.60) -17.41% Profit (loss) from operating activities 61.13 3.97% (95.94) -5.62% (157.07) -163.72% Finance income 0.33 0.02% 0.32 0.02% 0.01 3.13% Finance costs (218.40) -14.19

  `MDA_EVER_FY2025` · `p008` · SHA d10b7899f945
  </details>
- RFO ปี 2568 อยู่ที่ 1,302 ลบ. ลด 22.6% YoY; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2.1 Revenues from sales or revenues from services In 2025, the Company had total sales and service revenue of 1,301.76 million baht, Compared to 2024, which was 1,681.13 million baht, decrease by 379.37 million baht or 22.57%, due to the following main reasons:

  `MDA_EVER_FY2025` · `p010` · SHA 92e84912813a
  </details>

**NPAT — เพราะอะไร** — FY2024 −THB 339m → FY2025 −THB 163m · +176m

- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -163 ลบ. จาก -339 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Amount % To Amount % To Amount % To (MB) Revenue (MB) Revenue (MB) Revenue Revenues from sales and revenues from services 1,301.76 84.57% 1,681.13 98.45% (379.37) -22.57% Costs of sales of goods and costs of rendering of services (1,096.19) -71.21% (1,348.95) -78.99% (252.76) -18.74% Gross profit 205.57 13.36% 332.18 19.45% (126.61) -38.11% Other income 237.18 15.41% 26.19 1.53% 210.99 805.61% Distribution costs (117.78) -7.65% (134.88) -7.90% (17.10) -12.68% Administrative expenses (263.83) -17.14% (319.43) -18.71% (55.60) -17.41% Profit (loss) from operating activities 61.13 3.97% (95.94) -5.62% (157.07) -163.72% Finance income 0.33 0.02% 0.32 0.02% 0.01 3.13% Finance costs (218.40) -14.19

  `MDA_EVER_FY2025` · `p008` · SHA d10b7899f945
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -163 ลบ. จาก -339 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ยอดขายและการโอนโครงการที่อยู่อาศัย
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > 2) Hospital • Revenue from the hospital group amounted to 455.56 million baht, increase of 9.82 million baht or 2.20% compared to the same period of the previous year, resulting from increase patient visits. 2.2 Other income In 2025, the Company had other income of 237.18 million baht, compared to 26.19 million baht in 2024, increase of 210.99 million baht or 805.61% Because the company has sold land and condominiums that were its assets. 2.3 Costs of sales of goods and costs of rendering of services In 2025, the Company and its subsidiaries had a total Costs of sales of goods and costs of rendering of services of 1,096.19 million baht, compared to 2024, which was 1,348.95 million baht, decr

  `MDA_EVER_FY2025` · `p013` · SHA 41139e72b94e
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -163 ลบ. จาก -339 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ เอกสารที่มีอยู่ยังไม่แจกแจงสาเหตุเชิงปริมาณอย่างชัดเจน
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > MB %to total MB %to total MB %to total income income income Costs of sales of goods and costs of 719.91 46.77% 971.40 56.89% (251.49) (25.89%) rendering of services - Realrestate Costs of sales of goods and costs of 376.28 24.45% 377.55 22.11% (1.27) (0.34%) rendering of services - Hospital Total costs of sales of goods and costs of 1,096.19 71.21% 1,348.95 78.99% (252.76) (18.74%) rendering of services

  `MDA_EVER_FY2025` · `p014` · SHA a46d2749e70b
  </details>
- ขาดทุนสุทธิส่วนผู้ถือหุ้นปี 2568 ลดลงเหลือ -163 ลบ. จาก -339 ลบ.; ปัจจัยที่MD&Aระบุ ได้แก่ ต้นทุนทางการเงิน และ ค่าใช้จ่ายขายและบริหาร
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > MB %to total MB %to total MB %to total income income income Distribution costs - Realrestate 114.36 7.43% 130.89 7.67% (16.53) (12.63%) Distribution costs - Hospital 3.42 0.22% 3.99 0.23% (0.57) (14.29%) Total distribution costs 117.78 7.65% 134.88 7.90% (17.10) (12.68%) Administrative expenses - Realrestate 190.10 12.35% 243.03 14.23% (52.93) (21.78%) Administrative expenses - Hospital 73.74 4.79% 76.40 4.47% (2.66) (3.48%) Total administrative expenses 263.84 17.14% 319.43 18.71% (55.59) (17.40%) Total operating expenses 381.62 24.80% 454.31 26.61% (72.69) (16.00%) 2.5 Finance costs In 2025, the Company and its subsidiaries had financial costs of 218.40 million baht, compared to 237.43 mil

  `MDA_EVER_FY2025` · `p018` · SHA 3f6785544a77
  </details>

**รายการพิเศษ / ต่ำกว่าการดำเนินงาน — เชื่อมกำไรรายงานกับผลดำเนินงาน**

- รายการที่ต้องแยกพิจารณาจากผลการดำเนินงานหลัก: ความเสี่ยงด้านภูมิรัฐศาสตร์ และ กำไรหรือขาดทุนจากการจำหน่ายสินทรัพย์
  <details><summary>ข้อความ MD&A ต้นทาง · EN</summary>

  > Key Sustainable Business Operations in 2025 The Company believes that conducting business responsibly and engaging and growing with all stakeholders by adhering to the principles of corporate governance, having a business code of conduct and complying with the law will create long-term value for the organization. In 2025, the Company and its subsidiaries supported various sustainability activities as follows: • To create awareness of sustainable environmental management, the company has a policy of waste separation to promote waste separation before disposal, resulting in knowledge of waste disposal in the correct and appropriate way for each type of waste. Waste separation can increase recy

  `MDA_EVER_FY2025` · `p036` · SHA aa06dec52416
  </details>

> **เส้นทางหลักฐาน · ตรวจ MD&A ฉบับหลักแล้ว** — ทั้ง RFO และ NPAT มีข้อความสนับสนุนจาก MD&A ปี 2568 คำสรุปแบบ curated ยังคงเป็นบทสังเคราะห์ของนักวิเคราะห์ โดยมี excerpt และ hash ให้ย้อนทดสอบได้  
> แหล่งข้อมูล: `FY_PANEL / MDA_EVER_FY2025`

#### ทะเบียนข้อสรุป — P5

| ส่วน | ประเภท | ข้อสรุป | รหัสแหล่งข้อมูล |
|---|---|---|---|
| headline | ข้ออนุมานนักวิเคราะห์ | กลุ่มที่ปรับใหม่ยังขาดทุน แต่ขาดทุนลดลง | FY_PANEL, P5_E1, P5_E2, P5_E3 |
| earnings_fact | ข้อเท็จจริงจากการคำนวณ | FY2025 RFO -14.2%; สถานะ NPAT ส่วนผู้ถือหุ้น: loss_narrowed | FY_PANEL |
| why | ข้อเท็จจริงจากการคำนวณ | RFO ลด 14.2% ขณะที่ขาดทุนส่วนผู้ถือหุ้นลดจาก 3,020 ล้านบาทเป็น 2,653 ล้านบาท | FY_PANEL |
| why | ข้ออนุมานนักวิเคราะห์ | การพลิกตัวที่ได้รับอิทธิพลจาก event ของ RABBIT ชดเชยการอ่อนตัวของ STELLA และ CGD | FY_PANEL, P5_E1, P5_E2, P5_E3 |
| why | ข้อเท็จจริงจากการคำนวณ | UV เป็นตัวเทียบต่างรอบปีและไม่รวมในกลุ่มผลประกอบการปิดงบธันวาคม | FY_PANEL |
| causal_chain | ข้ออนุมานนักวิเคราะห์ | ห่วงโซ่เหตุ: ปรับโครงสร้าง → ขายสินทรัพย์ → หนี้ / สภาพคล่อง → กำไรหลัก → Re-rating | P5_E1, P5_E2, P5_E3 |
| roles | ข้ออนุมานนักวิเคราะห์ | บทบาท: ผู้นำและตัวฉุดขาดทุน — STELLA; ตัวแปรกำไรจาก event — RABBIT; ตัวเทียบต่างรอบปี — UV | FY_PANEL, P5_E1, P5_E2, P5_E3 |
| valuation | ข้ออนุมานนักวิเคราะห์ | P/E ของผู้มีกำไรปัจจุบันอยู่ที่ 8.5x ครอบคลุม 1/5 บริษัท และ 23.6% ของ market cap ที่มีข้อมูล. P/E ขับเคลื่อนด้วย event และไม่เป็นตัวแทนกลุ่มที่ขาดทุน | SET_PUBLIC_EOD, P5_E1, P5_E2, P5_E3 |
| trigger | ประเด็นที่ต้องพิสูจน์ | ปรับโครงสร้างเสร็จและได้เงินสดจริง | P5_E1, P5_E2, P5_E3 |
| trigger | ประเด็นที่ต้องพิสูจน์ | หนี้และสภาพคล่องดีขึ้น | P5_E1, P5_E2, P5_E3 |
| trigger | ประเด็นที่ต้องพิสูจน์ | ธุรกิจหลักกลับมามีกำไร | P5_E1, P5_E2, P5_E3 |
| risk | ประเด็นที่ต้องพิสูจน์ | กำไรพิเศษบดบังขาดทุนหลัก | P5_E1, P5_E2, P5_E3 |
| risk | ประเด็นที่ต้องพิสูจน์ | leverage และ refinancing | P5_E1, P5_E2, P5_E3 |
| risk | ประเด็นที่ต้องพิสูจน์ | ธรรมาภิบาลและ execution risk | P5_E1, P5_E2, P5_E3 |
| must_prove | ประเด็นที่ต้องพิสูจน์ | 6M26 ต้องแยกกำไรประจำออกจาก one-off และแสดงฐานะการเงินที่ดีขึ้น | P5_E1, P5_E2, P5_E3 |

#### ทะเบียนหลักฐาน — P5

- **`FY_PANEL`** · _ข้อเท็จจริงจากการคำนวณ_ — Audited FY2024-25 company panel
  - RFO / NPAT-to-owners / independent panel membership; QA 43 pass / 0 fail
  - บทบาท: historical fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_company_fy2024_2025_audited_2026-08-07.csv`
  - SHA-256: `e5e04dbc40ffcc79fed58545a93dc4549c29cdaecf260bea73711bc6d0720481`
- **`SET_PUBLIC_EOD`** · _ข้อเท็จจริงจากการคำนวณ_ — SET public Company Highlights — EOD 2026-08-07
  - Adjusted YTD; unadjusted price, market cap and valuation; factsheet-surface cross-check
  - บทบาท: current market fact
  - พาธ: `Listed Company/2-Analysis/AI-Generated/05-Themes/Sector-Review-6M26/data/official-2026-08-08-eod-2026-08-07/food_prop_set_public_surface_reconciliation_2026-08-07.csv`
  - SHA-256: `544c1f29fe2d409ee398822ac2bf32b769081718962ae2d1138985b0146b9530`
- **`SET_COMPANY_PROFILE`** · _ข้อเท็จจริง_ — SET company profiles — English and Thai
  - Official company names and business descriptions refreshed and validated for the 118-company perimeter from the public SET profile API
  - บทบาท: company business profile
  - URL: <https://www.set.or.th/th/market/product/stock/overview>
- **`COMPANY_REPORTS`** · _ข้ออนุมานนักวิเคราะห์_ — Company report synthesis corpus
  - Annual-only draft synthesis; reconciled to the ticker FY2025 MD&A where available
  - บทบาท: secondary synthesis; not management attribution
  - พาธ: `data/company-reports.json`
  - SHA-256: `c1a2bc40cbe21a2058aa596c362e4d47ad117360831b847de78ec414831fd2d2`
- **`MDA_STELLA_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — STELLA FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/STELLA/MDA_STELLA_2025FY_E.md`
  - SHA-256: `e723bed5d9068d22458d9a0fe4a9addcba021ea0a802611a562083c8ee9293f1`
  - URL: <https://weblink.set.or.th/dat/news/202602/0305NWS270220260854551060E.pdf>
- **`MDA_RABBIT_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — RABBIT FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/RABBIT/MDA_RABBIT_2025FY_E.md`
  - SHA-256: `a46ebc3215946a50b0e1437e707c798d7c73fcf1657881b2d796bb34595fc6ca`
  - URL: <https://weblink.set.or.th/dat/news/202602/0329NWS160220261759585900E.pdf>
- **`MDA_UV_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — UV FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/UV/MDA_UV_2025FY_T.md`
  - SHA-256: `db5391584df792fe144214732940dfff7637ac9ae610bb8bcb3458818eeaa3c3`
  - URL: <https://weblink.set.or.th/dat/news/202511/0136NWS241120251748489400T.pdf>
- **`MDA_CGD_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — CGD FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/CGD/MDA_CGD_2025FY_E.md`
  - SHA-256: `f12a3a34444cdee7fcefa3b5bc5d72c26270eeaa59b3f6f7c3fbc8aa1a7147cc`
  - URL: <https://weblink.set.or.th/dat/news/202603/0605NWS020320260823087470E.pdf>
- **`MDA_EVER_FY2025`** · _คำอธิบายฝ่ายจัดการ_ — EVER FY2025 MD&A
  - Primary annual management explanation with claim-level excerpts and excerpt SHA-256
  - บทบาท: FY2025 operating-performance attribution
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/EVER/MDA_EVER_2025FY_E.md`
  - SHA-256: `76b31a5993e7d93d972963e94d07a68b1b9c64c8d4c2454599b4bf25c260673d`
  - URL: <https://weblink.set.or.th/dat/news/202602/0391NWS250220262059542110E.pdf>
- **`P5_E1`** · _ฝ่ายจัดการ_ — STELLA FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/STELLA/MDA_STELLA_2025FY_E.md`
  - SHA-256: `e723bed5d9068d22458d9a0fe4a9addcba021ea0a802611a562083c8ee9293f1`
- **`P5_E2`** · _ฝ่ายจัดการ_ — RABBIT FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/RABBIT/MDA_RABBIT_2025FY_E.md`
  - SHA-256: `a46ebc3215946a50b0e1437e707c798d7c73fcf1657881b2d796bb34595fc6ca`
- **`P5_E3`** · _ฝ่ายจัดการ_ — UV FY2025 MD&A
  - Historical explanation or forward cross-check; see source role
  - บทบาท: management explanation
  - พาธ: `Listed Company/1-Raw/01-Filings/MDA/UV/MDA_UV_2025FY_T.md`
  - SHA-256: `db5391584df792fe144214732940dfff7637ac9ae610bb8bcb3458818eeaa3c3`
- **`P5_FACTSHEET`** · _ข้อเท็จจริงจากการคำนวณ_ — SET Factsheet — STELLA
  - Live leader cross-check
  - บทบาท: presentation-surface check
  - URL: <https://www.set.or.th/th/market/product/stock/quote/stella/factsheet>

---

## วิธีคำนวณและขอบเขต

RFO = Revenue from Operations • NPAT = กำไรส่วนผู้ถือหุ้น • ราคา = adjusted ไม่รวมเงินปันผล

### วิธีคำนวณและขอบเขต

| คำ | นิยาม |
|---|---|
| RFO | Revenue from Operations (01 Sale); December-FYE comparable panel unless separately labelled |
| RFOAMOUNT | FY2024/FY2025 audited RFO amount in THB million on the stated RFO panel |
| NPAT | Net profit attributable to owners of the parent; independent panel from RFO |
| NPATAMOUNT | FY2024/FY2025 owner NPAT amount in THB million on the stated NPAT panel |
| MARGIN | NPAT / RFO only on the identical issuer intersection |
| PRICE | Adjusted YTD price return; excludes cash dividends |
| VALUATION | Aggregate positive-earner P/E; identical numerator/denominator issuer set |
| MARKETCAP | Point-in-time market capitalisation; official null remains null |

### ลำดับชั้นแหล่งข้อมูล

- Audited RFO workbook / filing overrides
- NPAT attributable to owners
- SET public Company Highlights
- SET Factsheet
- FY2025 MD&A with claim-level excerpts and hashes
- Broker/credit research as fallback/forward context

### ไฟล์ต้นทาง

- `data/official-2026-08-08-eod-2026-08-07/food_prop_company_fy2024_2025_audited_2026-08-07.csv`
- `data/official-2026-08-08-eod-2026-08-07/food_prop_segment_fy2024_2025_audited_2026-08-07.csv`
- `data/official-2026-08-08-eod-2026-08-07/food_prop_sector_fy2024_2025_audited_2026-08-07.csv`
- `data/official-2026-08-08-eod-2026-08-07/QA_SUMMARY_FY2024_2025_AUDITED_2026-08-08.json`
- `data/official-2026-08-08-eod-2026-08-07/PROVENANCE_FY2024_2025_AUDITED_2026-08-08.json`
