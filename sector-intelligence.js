(function () {
  "use strict";

  var COPY = {
    en: {
      pageTitle:"Sector Intelligence", pageSubtitle:"Interactive sector briefing for RM meetings",
      sectorLabel:"Sector", modeLabel:"Mode", meeting:"Meeting mode", explore:"Explore data",
      structureLens:"Market structure", earningsLens:"FY2025 earnings", marketLens:"Market view",
      marketCap:"Market cap", companies:"Companies", largestSegment:"Largest segment",
      deliveredSegments:"Delivered segments", ytdPrice:"YTD adjusted", aggregatePe:"Aggregate P/E",
      priceLeading:"Price-leading segments", matrixTitle:"Ranked segment map",
      matrixSubtitle:"Market-cap order • click a row to open the analyst view", rank:"Rank", segment:"Segment",
      ytd:"YTD price", leader:"Leader", signal:"Signal", delivered:"Earnings confirmed",
      expectation:"Price leads", pressure:"Under pressure", event:"Event-driven", whyChanged:"Why it changed",
      causalChain:"Causal proof chain", roles:"Segment roles", trigger:"Trigger", risk:"Risk",
      flowOverview:"Sector view", flowSegment:"Segment", flowCompany:"Companies", flowEvidence:"Evidence",
      ticker:"Ticker", role:"Role", margin:"Margin", methodology:"Methodology & boundaries",
      evidenceRegister:"Evidence register", openEvidence:"Open evidence", copyLink:"Copy deep link",
      copied:"Copied", observed:"Observed fact", marketPaying:"Market is paying for — inference",
      deliveredLabel:"Delivered earnings / observed", pressureLabel:"Current pressure / observed",
      eventLabel:"Event-driven / limited comparability", companyPanel:"Company drill-down",
      companyPanelSub:"Meeting mode highlights leaders; Explore mode lists every company in the same audited segment perimeter",
      noRole:"Constituent", open:"Open", source:"Source", keyboard:"Use ↑ / ↓ to move • Enter or click to open • E for evidence",
      loss:"Loss", lossNarrowed:"Loss narrowed", lossWidened:"Loss widened", turnedProfit:"Turned profitable", notMeaningful:"n.m.", dataError:"Could not load Sector Intelligence data",
      marketCutoff:"Market data as of {date} • {period}", sourceLineage:"Sources: {sources}",
      definitions:"RFO = Revenue from Operations • NPAT = net profit to owners • Price = adjusted, excludes cash dividends",
      fact:"Fact", fact_calculated:"Calculated fact", management:"Management", management_explanation:"Management explanation", forward:"Forward view", credit_analysis:"Credit analysis", analyst_inference:"Analyst inference", analyst_test:"Analyst test", claimsRegister:"Claim register", known:"known",
      alternativeFiscal:"Alternative issuer-FY view", sourceId:"Source ID", sourceRole:"Role", sourcePath:"Path", sourceHash:"SHA-256",
      mixChart:"Market-cap mix", mixChartSub:"Segment share and market leader", earningsChart:"RFO and owner NPAT direction", earningsChartSub:"FY2025 YoY • zero-centred bars", marketMap:"Price versus earnings map", marketMapSub:"X = NPAT YoY • Y = YTD price • bubble = market cap", peChart:"Aggregate positive-earner P/E", peChartSub:"Coverage shown beside every multiple", companyWhyTitle:"Company performance read-through", rfoWhy:"RFO — why", npatWhy:"NPAT — why", auditedReadThrough:"Audited read-through", managementContext:"Issuer-specific context", noDirectCause:"Driver-specific MD&A attribution is not mapped for this issuer; do not present the read-through as management guidance.", selectedCompany:"Selected company", scaleNote:"Visual scale is capped; labels and tooltips show actual values."
    },
    th: {
      pageTitle:"บทวิเคราะห์รายกลุ่ม", pageSubtitle:"Interactive briefing สำหรับนำเสนอในที่ประชุม RM",
      sectorLabel:"กลุ่มอุตสาหกรรม", modeLabel:"โหมด", meeting:"โหมดประชุม", explore:"สำรวจข้อมูล",
      structureLens:"โครงสร้างตลาด", earningsLens:"ผลประกอบการ FY2025", marketLens:"มุมมองตลาด",
      marketCap:"Market cap", companies:"บริษัท", largestSegment:"Segment ใหญ่สุด",
      deliveredSegments:"Segment ที่กำไรยืนยัน", ytdPrice:"ราคา YTD ปรับแล้ว", aggregatePe:"P/E รวม",
      priceLeading:"Segment ราคานำ", matrixTitle:"แผนที่ Segment เรียงตาม Market Cap",
      matrixSubtitle:"เรียงจากใหญ่ไปเล็ก • คลิกเพื่อเปิดมุมมองนักวิเคราะห์", rank:"อันดับ", segment:"Segment",
      ytd:"ราคา YTD", leader:"ผู้นำ", signal:"สัญญาณ", delivered:"กำไรยืนยันราคา",
      expectation:"ราคานำพื้นฐาน", pressure:"ยังถูกกดดัน", event:"Event-driven", whyChanged:"เหตุผลที่เปลี่ยน",
      causalChain:"ห่วงโซ่เหตุและผล", roles:"บทบาทในกลุ่ม", trigger:"Trigger", risk:"Risk",
      flowOverview:"ภาพรวม Sector", flowSegment:"Segment", flowCompany:"รายบริษัท", flowEvidence:"หลักฐาน",
      ticker:"Ticker", role:"บทบาท", margin:"Margin", methodology:"วิธีคำนวณและขอบเขต",
      evidenceRegister:"ทะเบียนหลักฐาน", openEvidence:"เปิดหลักฐาน", copyLink:"คัดลอก Deep link",
      copied:"คัดลอกแล้ว", observed:"ข้อเท็จจริงที่สังเกตได้", marketPaying:"ตลาดกำลังจ่ายเพื่อ — ข้ออนุมาน",
      deliveredLabel:"กำไรที่เกิดขึ้นแล้ว / ข้อเท็จจริง", pressureLabel:"แรงกดดันปัจจุบัน / ข้อเท็จจริง",
      eventLabel:"Event-driven / เปรียบเทียบจำกัด", companyPanel:"วิเคราะห์รายบริษัท",
      companyPanelSub:"โหมดประชุมเน้นบริษัทหลัก; โหมดสำรวจแสดงทุกบริษัทใน perimeter ของ Segment ที่สอบทาน",
      noRole:"บริษัทในกลุ่ม", open:"เปิด", source:"แหล่งข้อมูล", keyboard:"ใช้ ↑ / ↓ เพื่อเลื่อน • Enter หรือคลิกเพื่อเปิด • กด E เพื่อดูหลักฐาน",
      loss:"ขาดทุน", lossNarrowed:"ขาดทุนลดลง", lossWidened:"ขาดทุนเพิ่มขึ้น", turnedProfit:"กลับเป็นกำไร", notMeaningful:"n.m.", dataError:"ไม่สามารถโหลดข้อมูล Sector Intelligence ได้",
      marketCutoff:"ข้อมูลตลาด ณ {date} • {period}", sourceLineage:"แหล่งข้อมูล: {sources}",
      definitions:"RFO = Revenue from Operations • NPAT = กำไรส่วนผู้ถือหุ้น • ราคา = adjusted ไม่รวมเงินปันผล",
      fact:"ข้อเท็จจริง", fact_calculated:"ข้อเท็จจริงจากการคำนวณ", management:"ฝ่ายจัดการ", management_explanation:"คำอธิบายฝ่ายจัดการ", forward:"มุมมองล่วงหน้า", credit_analysis:"บทวิเคราะห์เครดิต", analyst_inference:"ข้ออนุมานนักวิเคราะห์", analyst_test:"ประเด็นที่ต้องพิสูจน์", claimsRegister:"ทะเบียนข้อสรุป", known:"มีข้อมูล",
      alternativeFiscal:"มุมมองตามปีบัญชีของผู้ออก", sourceId:"รหัสแหล่งข้อมูล", sourceRole:"บทบาท", sourcePath:"พาธ", sourceHash:"SHA-256",
      mixChart:"สัดส่วน Market Cap", mixChartSub:"ขนาด Segment และผู้นำตลาด", earningsChart:"ทิศทาง RFO และ NPAT ส่วนผู้ถือหุ้น", earningsChartSub:"FY2025 YoY • แถบเทียบจากแกนศูนย์", marketMap:"ราคาเทียบกับทิศทางกำไร", marketMapSub:"X = NPAT YoY • Y = ราคา YTD • ขนาดวง = Market Cap", peChart:"P/E รวมของบริษัทที่มีกำไร", peChartSub:"แสดงความครอบคลุมของข้อมูลควบคู่ทุกค่า", companyWhyTitle:"อ่านผลประกอบการรายบริษัท", rfoWhy:"RFO — เพราะอะไร", npatWhy:"NPAT — เพราะอะไร", auditedReadThrough:"ข้อสรุปจากตัวเลขที่สอบทาน", managementContext:"บริบทเฉพาะบริษัท", noDirectCause:"ยังไม่ได้ผูกสาเหตุจาก MD&A รายบริษัทโดยตรง จึงห้ามนำข้อสรุปเชิงวิเคราะห์นี้ไปกล่าวเป็นคำอธิบายของฝ่ายจัดการ", selectedCompany:"บริษัทที่เลือก", scaleNote:"กราฟจำกัดช่วงเพื่อให้อ่านง่าย; ป้ายค่าและคำอธิบายเมื่อชี้แสดงค่าจริง"
    }
  };

  var state = { data:null, tickerMeta:{}, sector:"FOOD", segment:null, company:null, mode:"meeting", flow:"overview" };
  var SEGMENT_COLORS = ["#ef8b16","#0f7f78","#285f89","#d8a329","#6b6f9b","#4f9b91","#a2674a","#75818d","#b7799b"];
  var app = document.getElementById("sectorIntelligenceApp");
  var query = new URLSearchParams(location.search);
  if (/^(FOOD|PROP)$/.test(query.get("sector") || "")) state.sector = query.get("sector");
  if (/^[FP]\d$/.test(query.get("segment") || "")) state.segment = query.get("segment");
  if (/^[A-Z0-9&-]{1,12}$/.test(query.get("company") || "")) state.company = query.get("company");
  if (/^(meeting|explore)$/.test(query.get("mode") || "")) state.mode = query.get("mode");
  if (/^(overview|segment|company|evidence)$/.test(query.get("flow") || "")) state.flow = query.get("flow");

  function language() { return window.I18N && I18N.lang === "th" ? "th" : "en"; }
  function t(key) { return (COPY[language()] && COPY[language()][key]) || COPY.en[key] || key; }
  function loc(value) {
    if (value == null) return "";
    if (typeof value === "string") return value;
    return value[language()] || value.en || value.th || "";
  }
  function esc(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g,function (char) {
      return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[char];
    });
  }
  function finite(value) { return value !== null && value !== "" && Number.isFinite(Number(value)); }
  function signClass(value) { return !finite(value) ? "neutral" : Number(value) > .049 ? "positive" : Number(value) < -.049 ? "negative" : "neutral"; }
  function fmtPct(value,digits) {
    if (!finite(value)) return "—";
    var number = Number(value);
    return (number > .049 ? "+" : "") + number.toFixed(digits == null ? 1 : digits) + "%";
  }
  function fmtNpat(metrics) {
    if (metrics.npatState === "turned_to_loss") return t("loss");
    if (metrics.npatState === "loss_narrowed") return t("lossNarrowed") + (finite(metrics.npatYoYPct) ? " " + fmtPct(metrics.npatYoYPct,1) : "");
    if (metrics.npatState === "loss_widened") return t("lossWidened") + (finite(metrics.npatYoYPct) ? " " + fmtPct(metrics.npatYoYPct,1) : "");
    if (metrics.npatState === "turned_to_profit" && !finite(metrics.npatYoYPct)) return t("turnedProfit");
    return fmtPct(metrics.npatYoYPct,1);
  }
  function fmtPe(value) { return finite(value) ? Number(value).toFixed(1) + "x" : t("notMeaningful"); }
  function fmtMcap(value) {
    if (!finite(value)) return "—";
    var n = Number(value);
    return n >= 1000 ? "THB " + (n / 1000).toFixed(n >= 100000 ? 0 : 1) + "bn" : "THB " + n.toFixed(0) + "m";
  }
  function fmtAmount(value) {
    if (!finite(value)) return "—";
    var n = Number(value), sign = n < 0 ? "−" : "", absolute = Math.abs(n);
    if (absolute >= 1000000) return sign + "THB " + (absolute / 1000000).toFixed(2) + "tn";
    if (absolute >= 1000) return sign + "THB " + (absolute / 1000).toFixed(absolute >= 100000 ? 0 : 1) + "bn";
    return sign + "THB " + absolute.toFixed(0) + "m";
  }
  function fmtAmountDelta(value) {
    if (!finite(value)) return "—";
    return (Number(value) > 0 ? "+" : "") + fmtAmount(value).replace("THB ","");
  }
  function fill(template,vars) {
    return String(template).replace(/\{(\w+)\}/g,function (_,key) { return vars[key] == null ? "" : vars[key]; });
  }
  function safeUrl(url) {
    try {
      var parsed = new URL(url,location.href);
      return /^https?:$/.test(parsed.protocol) ? parsed.href : "";
    } catch (_) { return ""; }
  }
  function coverageText(coverage,includeMcap) {
    if (!coverage) return "—";
    var text = String(coverage.count) + "/" + String(coverage.total);
    if (includeMcap && finite(coverage.marketCapPct)) text += " • " + Number(coverage.marketCapPct).toFixed(0) + "% M-cap";
    return text;
  }
  function selectedSector() { return state.data.sectors[state.sector]; }
  function selectedSegment() {
    var sector = selectedSector();
    return sector.segments.find(function (segment) { return segment.code === state.segment; }) || sector.segments[0];
  }
  function statusLabel(status) { return t(status === "event" ? "event" : status); }
  function valuationLabel(status) {
    if (status === "delivered") return t("deliveredLabel");
    if (status === "pressure") return t("pressureLabel");
    if (status === "event") return t("eventLabel");
    return t("marketPaying");
  }
  function displayDate(iso) {
    if (!iso) return "—";
    var parts = iso.split("-");
    if (language() === "th") return Number(parts[2]) + " ส.ค. " + (Number(parts[0]) + 543);
    return new Date(iso + "T00:00:00Z").toLocaleDateString("en-GB",{day:"numeric",month:"short",year:"numeric",timeZone:"UTC"});
  }

  function clamp(value,min,max) { return Math.max(min,Math.min(max,value)); }
  function chartColor(index) { return SEGMENT_COLORS[index % SEGMENT_COLORS.length]; }
  function copy(en,th) { return language() === "th" ? th : en; }
  function metricActual(value) { return finite(value) ? fmtPct(value,1) : "—"; }
  function polar(cx,cy,r,angle) {
    var radians = (angle - 90) * Math.PI / 180;
    return {x:cx + r * Math.cos(radians),y:cy + r * Math.sin(radians)};
  }
  function donutPath(cx,cy,outer,inner,start,end) {
    var a = polar(cx,cy,outer,start), b = polar(cx,cy,outer,end);
    var c = polar(cx,cy,inner,end), d = polar(cx,cy,inner,start);
    var large = end - start > 180 ? 1 : 0;
    return "M " + a.x.toFixed(3) + " " + a.y.toFixed(3) + " A " + outer + " " + outer + " 0 " + large + " 1 " + b.x.toFixed(3) + " " + b.y.toFixed(3) + " L " + c.x.toFixed(3) + " " + c.y.toFixed(3) + " A " + inner + " " + inner + " 0 " + large + " 0 " + d.x.toFixed(3) + " " + d.y.toFixed(3) + " Z";
  }
  function renderMarketCapMix(sector) {
    var angle = 0;
    var paths = sector.segments.map(function (segment,index) {
      var start = angle;
      angle += Number(segment.marketCapSharePct) * 3.6;
      var selected = segment.code === state.segment;
      return '<g class="si-chart-target ' + (selected ? 'selected' : '') + '" data-segment="' + esc(segment.code) + '" tabindex="0" role="button" aria-label="' + esc(segment.code + ' ' + loc(segment.name) + ' ' + Number(segment.marketCapSharePct).toFixed(1) + '%') + '"><path d="' + donutPath(72,72,60,37,start,angle) + '" fill="' + chartColor(index) + '"><title>' + esc(segment.code + ' ' + loc(segment.name) + ' · ' + Number(segment.marketCapSharePct).toFixed(1) + '% · ' + t('leader') + ' ' + (segment.leader.ticker || '—')) + '</title></path></g>';
    }).join('');
    document.getElementById('marketCapDonut').innerHTML = '<svg viewBox="0 0 144 144" role="img" aria-label="' + esc(t('mixChart')) + '">' + paths + '<circle cx="72" cy="72" r="33" class="si-donut-hole"></circle><text x="72" y="68" class="si-donut-value">' + esc(fmtMcap(sector.metrics.marketCapMb).replace('THB ','')) + '</text><text x="72" y="84" class="si-donut-label">' + esc(t('marketCap')) + '</text></svg>';
    document.getElementById('marketCapLegend').innerHTML = sector.segments.map(function (segment,index) {
      var selected = segment.code === state.segment;
      return '<button type="button" class="si-legend-row ' + (selected ? 'selected' : '') + '" data-segment="' + esc(segment.code) + '"><i style="--segment-color:' + chartColor(index) + '"></i><span><b>' + esc(segment.code + ' ' + loc(segment.name)) + '</b><small>' + esc(t('leader') + ' ' + (segment.leader.ticker || '—')) + '</small></span><strong>' + Number(segment.marketCapSharePct).toFixed(1) + '%</strong></button>';
    }).join('');
  }
  function divergingBar(value,scale,label,stateName,amount) {
    var amountText = fmtAmount(amount);
    if (!finite(value)) return '<div class="si-div-cell neutral"><span class="si-div-track"></span><span class="si-div-label"><b>—</b><small>' + esc(amountText) + '</small></span></div>';
    var number = Number(value), clipped = Math.abs(number) > scale;
    var width = clamp(Math.abs(number) / scale * 48,1.2,48);
    var left = number >= 0 ? 50 : 50 - width;
    var cls = number >= 0 ? 'positive' : 'negative';
    if (/^(turned_to_loss|loss_widened)$/.test(stateName || '')) cls = 'negative';
    return '<div class="si-div-cell ' + cls + (clipped ? ' clipped' : '') + '" title="' + esc(label + ' · FY2025 ' + amountText) + '"><span class="si-div-track"><i style="left:' + left.toFixed(2) + '%;width:' + width.toFixed(2) + '%"></i></span><span class="si-div-label"><b>' + esc(label) + '</b><small>' + esc(amountText) + '</small></span></div>';
  }
  function renderEarningsBars(sector) {
    var metrics = sector.metrics;
    document.querySelector('.si-earnings-totals .rfo span').textContent = copy('RFO FY2025','RFO FY2025');
    document.querySelector('.si-earnings-totals .npat span').textContent = copy('Owner NPAT FY2025','NPAT ส่วนผู้ถือหุ้น FY2025');
    document.getElementById('earningsRfoTotal').textContent = fmtAmount(metrics.rfoFy2025Mb);
    document.getElementById('earningsRfoTotal').className = signClass(metrics.rfoYoYPct);
    document.getElementById('earningsRfoCoverage').textContent = copy('FY2024 ' + fmtAmount(metrics.rfoFy2024Mb) + ' · panel ' + sector.coverage.rfo,'FY2024 ' + fmtAmount(metrics.rfoFy2024Mb) + ' · ชุดข้อมูล ' + sector.coverage.rfo);
    document.getElementById('earningsNpatTotal').textContent = fmtAmount(metrics.npatOwnersFy2025Mb);
    document.getElementById('earningsNpatTotal').className = signClass(metrics.npatYoYPct);
    document.getElementById('earningsNpatCoverage').textContent = copy('FY2024 ' + fmtAmount(metrics.npatOwnersFy2024Mb) + ' · panel ' + sector.coverage.npat,'FY2024 ' + fmtAmount(metrics.npatOwnersFy2024Mb) + ' · ชุดข้อมูล ' + sector.coverage.npat);
    var axis = document.querySelectorAll('.si-earnings-axis span');
    if (axis.length === 2) { axis[0].textContent = 'RFO YoY · ±50%'; axis[1].textContent = 'NPAT YoY · ±100%'; }
    document.getElementById('earningsBars').innerHTML = sector.segments.map(function (segment) {
      var selected = segment.code === state.segment;
      return '<button type="button" class="si-earnings-row ' + (selected ? 'selected' : '') + '" data-segment="' + esc(segment.code) + '"><span class="si-earnings-name"><b>' + esc(segment.code) + '</b><small>' + esc(loc(segment.name)) + '</small></span>' + divergingBar(segment.metrics.rfoYoYPct,50,metricActual(segment.metrics.rfoYoYPct),null,segment.metrics.rfoFy2025Mb) + divergingBar(segment.metrics.npatYoYPct,100,fmtNpat(segment.metrics),segment.metrics.npatState,segment.metrics.npatOwnersFy2025Mb) + '</button>';
    }).join('') + '<p class="si-scale-note">' + esc(t('scaleNote')) + '</p>';
  }
  function renderMarketMap(sector) {
    var quadrant = language() === 'th' ? ['ราคานำ • กำไรยังไม่ยืนยัน','ราคาและกำไรตอบรับ','ราคาและกำไรถูกกดดัน','กำไรนำ • ราคายัง lag'] : ['Price leads • profit unconfirmed','Price and profit aligned','Price and profit pressured','Profit leads • price lags'];
    var bubbles = sector.segments.map(function (segment,index) {
      if (!finite(segment.metrics.npatYoYPct) || !finite(segment.metrics.ytdAdjustedReturnPct)) return '';
      var xActual = Number(segment.metrics.npatYoYPct), yActual = Number(segment.metrics.ytdAdjustedReturnPct);
      var x = 350 + clamp(xActual,-100,100) * 2.75;
      var y = 160 - clamp(yActual,-50,50) * 2.25;
      var radius = 7 + Math.sqrt(Math.max(0,Number(segment.marketCapSharePct))) * 2.25;
      var clipped = Math.abs(xActual) > 100 || Math.abs(yActual) > 50;
      var selected = segment.code === state.segment;
      return '<g class="si-map-bubble si-chart-target ' + (selected ? 'selected ' : '') + (clipped ? 'clipped' : '') + '" data-segment="' + esc(segment.code) + '" tabindex="0" role="button" aria-label="' + esc(segment.code + ' NPAT ' + metricActual(xActual) + ' YTD ' + metricActual(yActual)) + '"><circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="' + radius.toFixed(1) + '" fill="' + chartColor(index) + '"><title>' + esc(segment.code + ' ' + loc(segment.name) + ' · NPAT ' + metricActual(xActual) + ' · YTD ' + metricActual(yActual) + ' · M-cap ' + Number(segment.marketCapSharePct).toFixed(1) + '%') + '</title></circle><text x="' + (x + radius + 4).toFixed(1) + '" y="' + (y + 3).toFixed(1) + '">' + esc(segment.code) + '</text></g>';
    }).join('');
    document.getElementById('marketMap').innerHTML = '<svg viewBox="0 0 700 330" role="img" aria-label="' + esc(t('marketMap')) + '"><rect x="50" y="30" width="300" height="130" class="si-q price-leads"></rect><rect x="350" y="30" width="300" height="130" class="si-q aligned"></rect><rect x="50" y="160" width="300" height="125" class="si-q pressured"></rect><rect x="350" y="160" width="300" height="125" class="si-q profit-leads"></rect><line x1="350" y1="30" x2="350" y2="285" class="si-axis-line"></line><line x1="50" y1="160" x2="650" y2="160" class="si-axis-line"></line><text x="62" y="49" class="si-q-label">' + esc(quadrant[0]) + '</text><text x="638" y="49" text-anchor="end" class="si-q-label">' + esc(quadrant[1]) + '</text><text x="62" y="276" class="si-q-label">' + esc(quadrant[2]) + '</text><text x="638" y="276" text-anchor="end" class="si-q-label">' + esc(quadrant[3]) + '</text>' + bubbles + '<text x="350" y="317" text-anchor="middle" class="si-axis-label">NPAT YoY · -100% ← 0 → +100%</text><text transform="translate(16 160) rotate(-90)" text-anchor="middle" class="si-axis-label">YTD price · -50% ← 0 → +50%</text></svg>';
  }
  function renderPeStrip(sector) {
    var scale = 40;
    document.getElementById('peStrip').innerHTML = sector.segments.map(function (segment,index) {
      var pe = segment.metrics.aggregatePositiveEarningsPe;
      var selected = segment.code === state.segment;
      var eligible = finite(pe);
      var position = eligible ? clamp(Number(pe),0,scale) / scale * 100 : 0;
      var clipped = eligible && Number(pe) > scale;
      return '<button type="button" class="si-pe-row ' + (selected ? 'selected ' : '') + (!eligible ? 'not-meaningful ' : '') + (clipped ? 'clipped' : '') + '" data-segment="' + esc(segment.code) + '"><span><b>' + esc(segment.code) + '</b><small>' + esc(loc(segment.name)) + '</small></span><i class="si-pe-track">' + (eligible ? '<em style="left:' + position.toFixed(1) + '%;--segment-color:' + chartColor(index) + '"></em>' : '') + '</i><strong>' + esc(fmtPe(pe)) + '</strong><small>' + esc(coverageText(segment.coverage.positivePe,true)) + '</small></button>';
    }).join('') + '<div class="si-pe-axis"><span>0x</span><span>20x</span><span>40x+</span></div>';
  }
  function renderVisuals() {
    var sector = selectedSector();
    renderMarketCapMix(sector);
    renderEarningsBars(sector);
    renderMarketMap(sector);
    renderPeStrip(sector);
  }
  function mentionsTicker(value,ticker) {
    var escaped = ticker.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
    var pattern = new RegExp('(^|[^A-Z0-9])' + escaped + '([^A-Z0-9]|$)','i');
    return pattern.test(String(value || ''));
  }
  function directCompanyClaim(segment,ticker) {
    return segment.claims.find(function (claim) {
      if (claim.section !== 'why') return false;
      var text = claim.text || {};
      return mentionsTicker(text.en,ticker) || mentionsTicker(text.th,ticker);
    }) || null;
  }
  function rfoNarrative(company) {
    if (!company.rfoPanel) return copy('Not in the comparable RFO panel' + (company.panelExclusionReason ? ': ' + company.panelExclusionReason : '.') + ' No operating-revenue direction is asserted.','ไม่อยู่ในชุดข้อมูล RFO ที่เปรียบเทียบได้' + (company.panelExclusionReason ? ': ' + company.panelExclusionReason : '') + ' จึงไม่สรุปทิศทางรายได้จากการดำเนินงาน');
    var value = Number(company.rfoYoYPct);
    if (value > 1) return copy('RFO increased ' + Math.abs(value).toFixed(1) + '%. The audited panel confirms operating-revenue expansion, but the split between volume, price/mix and FX still requires issuer MD&A.','RFO เพิ่ม ' + Math.abs(value).toFixed(1) + '% ตัวเลขที่สอบทานยืนยันการขยายตัวของรายได้ดำเนินงาน แต่ยังต้องใช้ MD&A แยก ปริมาณขาย ราคาขาย/ส่วนผสมผลิตภัณฑ์ และผลอัตราแลกเปลี่ยน');
    if (value < -1) return copy('RFO decreased ' + Math.abs(value).toFixed(1) + '%. The audited panel confirms weaker operating scale; volume, price/mix and FX attribution must come from issuer MD&A.','RFO ลด ' + Math.abs(value).toFixed(1) + '% ตัวเลขที่สอบทานยืนยันฐานรายได้ดำเนินงานที่อ่อนลง แต่สาเหตุด้าน ปริมาณขาย ราคาขาย/ส่วนผสมผลิตภัณฑ์ และผลอัตราแลกเปลี่ยน ต้องยืนยันจาก MD&A');
    return copy('RFO was broadly flat at ' + fmtPct(value,1) + '. Revenue scale was stable; the number alone does not identify offsets within volume, price/mix or FX.','RFO ทรงตัวที่ ' + fmtPct(value,1) + ' สะท้อนฐานรายได้ค่อนข้างคงที่ แต่ตัวเลขอย่างเดียวไม่ระบุแรงชดเชยระหว่างปริมาณขาย ราคาขาย/ส่วนผสมผลิตภัณฑ์ หรือผลอัตราแลกเปลี่ยน');
  }
  function npatNarrative(company) {
    if (!company.npatPanel) return copy('Not in the comparable owner-NPAT panel. Raw values are retained for audit but are not used for the company read-through.','ไม่อยู่ในชุดข้อมูล NPAT ส่วนผู้ถือหุ้นที่เปรียบเทียบได้ โดยคงตัวเลขดิบไว้เพื่อการสอบทานแต่ไม่นำมาใช้สรุปบริษัท');
    if (company.npatState === 'turned_to_loss') return copy('Owner NPAT turned to a loss. The profit bridge broke below the operating-revenue line; the exact margin, impairment or financing driver requires issuer evidence.','NPAT ส่วนผู้ถือหุ้นพลิกเป็นขาดทุน สะท้อนว่าการเปลี่ยนรายได้เป็นกำไรอ่อนลง แต่ต้องใช้หลักฐานบริษัทแยกผลจากอัตรากำไร การด้อยค่า หรือต้นทุนทางการเงิน');
    if (company.npatState === 'loss_narrowed') return copy('The owner loss narrowed. This is an improving profit direction, but it is not equivalent to a profitable earnings base.','ขาดทุนส่วนผู้ถือหุ้นลดลง เป็นทิศทางกำไรที่ดีขึ้น แต่ยังไม่เท่ากับมีฐานกำไรเป็นบวก');
    if (company.npatState === 'loss_widened') return copy('The owner loss widened. Profit pressure intensified even if revenue moved differently; issuer evidence is required before naming the cost driver.','ขาดทุนส่วนผู้ถือหุ้นเพิ่มขึ้น สะท้อนแรงกดดันกำไรรุนแรงขึ้น แม้รายได้อาจเคลื่อนไหวต่างกัน ต้องใช้หลักฐานบริษัทก่อนระบุต้นทุนที่เป็นสาเหตุ');
    if (company.npatState === 'turned_to_profit' && !finite(company.npatYoYPct)) return copy('Owner NPAT turned profitable. Treat this as a turnaround state rather than a meaningful growth percentage.','NPAT ส่วนผู้ถือหุ้นพลิกกลับเป็นกำไร ควรอ่านเป็นสถานะฟื้นตัว ไม่ใช่อัตราเติบโตที่มีความหมาย');
    if (!finite(company.npatYoYPct)) return copy('Owner-NPAT growth is not meaningful on the available base.','อัตราเติบโต NPAT ส่วนผู้ถือหุ้นไม่มีความหมายบนฐานที่มี');
    var npat = Number(company.npatYoYPct);
    if (!company.rfoPanel || !finite(company.rfoYoYPct)) return copy('Owner NPAT changed ' + fmtPct(npat,1) + ', but there is no identical RFO panel for a conversion read-through.','NPAT ส่วนผู้ถือหุ้นเปลี่ยน ' + fmtPct(npat,1) + ' แต่ไม่มีชุดข้อมูล RFO ฐานเดียวกันสำหรับวิเคราะห์การเปลี่ยนรายได้เป็นกำไร');
    var gap = npat - Number(company.rfoYoYPct);
    if (gap > 5) return copy('Owner NPAT ' + fmtPct(npat,1) + ' outpaced RFO by ' + gap.toFixed(1) + ' ppts. This points to margin, cost or below-line uplift; it is an analyst read-through, not causal proof.','NPAT ส่วนผู้ถือหุ้น ' + fmtPct(npat,1) + ' เติบโตเร็วกว่า RFO ' + gap.toFixed(1) + ' จุด สะท้อนแรงหนุนจากอัตรากำไร ต้นทุน หรือรายการต่ำกว่ารายได้ แต่เป็นการอนุมานของนักวิเคราะห์ ไม่ใช่หลักฐานเชิงสาเหตุ');
    if (gap < -5) return copy('Owner NPAT ' + fmtPct(npat,1) + ' lagged RFO by ' + Math.abs(gap).toFixed(1) + ' ppts. Profit conversion weakened, pointing to margin or below-line drag that must be verified in MD&A.','NPAT ส่วนผู้ถือหุ้น ' + fmtPct(npat,1) + ' แย่กว่า RFO ' + Math.abs(gap).toFixed(1) + ' จุด สะท้อนการเปลี่ยนรายได้เป็นกำไรที่อ่อนลงจากอัตรากำไรหรือรายการต่ำกว่ารายได้ ซึ่งต้องยืนยันใน MD&A');
    return copy('Owner NPAT ' + fmtPct(npat,1) + ' moved broadly with RFO. Profit conversion was directionally aligned, subject to issuer-level MD&A confirmation.','NPAT ส่วนผู้ถือหุ้น ' + fmtPct(npat,1) + ' เคลื่อนไหวใกล้เคียง RFO สะท้อนการเปลี่ยนรายได้เป็นกำไรที่สอดคล้องกัน แต่ยังต้องยืนยันระดับบริษัทจาก MD&A');
  }
  function companyBridge(company) {
    if (!company.rfoPanel || !company.npatPanel) return copy('Panel-limited: avoid a causal bridge','ข้อมูลเทียบเคียงจำกัด: ไม่ควรสรุปเหตุเชื่อมโยงระหว่างรายได้กับกำไร');
    if (/^(turned_to_loss|loss_widened)$/.test(company.npatState)) return copy('Profit pressure exceeded the revenue signal','แรงกดดันกำไรมากกว่าสัญญาณรายได้');
    if (company.npatState === 'loss_narrowed' || company.npatState === 'turned_to_profit') return copy('Turnaround state; growth rate is secondary','อยู่ในภาวะฟื้นตัว; อัตราเติบโตมีความสำคัญรองลงมา');
    var gap = Number(company.npatYoYPct) - Number(company.rfoYoYPct);
    if (gap > 5) return copy('Profit outpaced operating revenue','กำไรเติบโตเร็วกว่ารายได้ดำเนินงาน');
    if (gap < -5) return copy('Profit conversion lagged revenue','กำไรแปลงจากรายได้ได้อ่อนลง');
    return copy('Revenue and profit moved together','รายได้และกำไรเคลื่อนไหวสอดคล้องกัน');
  }
  function applyStaticLabels() {
    document.querySelectorAll("[data-si]").forEach(function (node) { node.textContent = t(node.dataset.si); });
    document.querySelector('#modeSwitch [data-mode="meeting"]').textContent = t("meeting");
    document.querySelector('#modeSwitch [data-mode="explore"]').textContent = t("explore");
    document.getElementById("keyboardHint").textContent = t("keyboard");
    document.getElementById("copyDeepLink").textContent = t("copyLink");
    document.documentElement.lang = language();
  }

  function renderControls() {
    document.querySelectorAll("#sectorSwitch [data-sector]").forEach(function (button) {
      var active = button.dataset.sector === state.sector;
      button.classList.toggle("active",active);
      button.setAttribute("aria-pressed",String(active));
    });
    document.querySelectorAll("#modeSwitch [data-mode]").forEach(function (button) {
      var active = button.dataset.mode === state.mode;
      button.classList.toggle("active",active);
      button.setAttribute("aria-pressed",String(active));
    });
    app.dataset.mode = state.mode;
  }

  function renderOverview() {
    var sector = selectedSector();
    var metrics = sector.metrics;
    var largest = sector.segments[0];
    document.getElementById("sectorHeadline").textContent = loc(sector.title);
    document.getElementById("sectorThesis").textContent = loc(sector.thesis);
    document.getElementById("sectorTakeaways").innerHTML = sector.takeaways.map(function (item) { return "<li>" + esc(loc(item)) + "</li>"; }).join("");
    document.getElementById("sectorMarketCap").textContent = fmtMcap(metrics.marketCapMb);
    document.getElementById("sectorMarketCap").nextElementSibling.textContent = t("marketCap") + " • " + sector.coverage.marketCap + " " + t("known");
    document.getElementById("sectorCompanies").textContent = String(metrics.companyCount);
    document.getElementById("largestSegment").textContent = largest.code + " · " + Number(largest.marketCapSharePct).toFixed(1) + "%";
    setDirectional("sectorRfo",metrics.rfoYoYPct,fmtPct(metrics.rfoYoYPct,1));
    setDirectional("sectorNpat",metrics.npatYoYPct,fmtPct(metrics.npatYoYPct,1));
    document.getElementById("deliveredCount").textContent = sector.segments.filter(function (s) { return s.status === "delivered"; }).length + "/" + sector.segments.length;
    setDirectional("sectorYtd",metrics.ytdAdjustedReturnPct,fmtPct(metrics.ytdAdjustedReturnPct,1));
    document.getElementById("sectorPe").textContent = fmtPe(metrics.aggregatePositiveEarningsPe);
    document.getElementById("expectationCount").textContent = sector.segments.filter(function (s) { return s.status === "expectation" || s.status === "event"; }).length + "/" + sector.segments.length;
    document.getElementById("cutoffLabel").textContent = fill(t("marketCutoff"),{date:displayDate(state.data.meta.effectiveMarketEod),period:state.data.meta.earningsPeriod});
    document.getElementById("definitions").textContent = t("definitions");
    document.getElementById("sourceLineage").textContent = fill(t("sourceLineage"),{sources:state.data.meta.sourceLineage.join(" / ")});
  }

  function setDirectional(id,value,text) {
    var node = document.getElementById(id);
    node.textContent = text;
    node.classList.remove("positive","negative","neutral");
    node.classList.add(signClass(value));
  }

  function renderSegments() {
    var sector = selectedSector();
    document.getElementById("segmentRows").innerHTML = sector.segments.map(function (segment,index) {
      var metrics = segment.metrics;
      var selected = segment.code === state.segment;
      var shareWidth = Math.min(100,Math.max(3,Number(segment.marketCapSharePct) * 2));
      var npatText = fmtNpat(metrics);
      var npatClass = /^(turned_to_loss|loss_narrowed|loss_widened)$/.test(metrics.npatState) ? "negative" : signClass(metrics.npatYoYPct);
      return '<tr tabindex="0" role="button" aria-selected="' + selected + '" class="' + (selected ? "selected" : "") + '" data-segment="' + esc(segment.code) + '">' +
        '<td class="si-rank-cell">' + (index + 1) + '</td>' +
        '<td class="si-segment-cell"><strong>' + esc(segment.code + " " + loc(segment.name)) + '</strong><small>' + esc(segment.companyCount + " " + t("companies")) + '</small></td>' +
        '<td><div class="si-share"><span class="si-share-track"><i style="--share:' + shareWidth.toFixed(1) + '%"></i></span><span class="si-value">' + Number(segment.marketCapSharePct).toFixed(1) + '%</span></div><small class="si-metric-coverage">' + esc(coverageText(segment.coverage.marketCap,false) + " " + t("known")) + '</small></td>' +
        '<td><span class="si-value ' + signClass(metrics.rfoYoYPct) + '">' + fmtPct(metrics.rfoYoYPct,1) + '</span><small class="si-metric-coverage">' + esc(coverageText(segment.coverage.rfo,false)) + '</small></td>' +
        '<td><span class="si-value ' + npatClass + '">' + esc(npatText) + '</span><small class="si-metric-coverage">' + esc(coverageText(segment.coverage.npat,false)) + '</small></td>' +
        '<td><span class="si-value ' + signClass(metrics.ytdAdjustedReturnPct) + '">' + fmtPct(metrics.ytdAdjustedReturnPct,1) + '</span><small class="si-metric-coverage">' + esc(coverageText(segment.coverage.ytd,true)) + '</small></td>' +
        '<td><span class="si-value">' + esc(fmtPe(metrics.aggregatePositiveEarningsPe)) + '</span><small class="si-metric-coverage">' + esc(coverageText(segment.coverage.positivePe,true)) + '</small></td>' +
        '<td class="si-leader"><strong>' + esc(segment.leader.ticker || "—") + '</strong><small>' + (finite(segment.leader.sharePct) ? Number(segment.leader.sharePct).toFixed(0) + '% share' : '') + '</small></td>' +
        '<td><span class="si-status ' + esc(segment.status) + '">' + esc(statusLabel(segment.status)) + '</span></td>' +
      '</tr>';
    }).join("");
  }

  function observedText(segment) {
    var m = segment.metrics;
    var npat = fmtNpat(m);
    var panelCoverage = "RFO " + coverageText(segment.coverage.rfo,false) + " • NPAT " + coverageText(segment.coverage.npat,false);
    if (language() === "th") {
      return "FY2025: RFO " + fmtPct(m.rfoYoYPct,1) + " • NPAT " + npat + " • ราคา YTD " + fmtPct(m.ytdAdjustedReturnPct,1) + " • P/E " + fmtPe(m.aggregatePositiveEarningsPe) + " • Coverage " + panelCoverage;
    }
    return "FY2025: RFO " + fmtPct(m.rfoYoYPct,1) + " • NPAT " + npat + " • YTD price " + fmtPct(m.ytdAdjustedReturnPct,1) + " • P/E " + fmtPe(m.aggregatePositiveEarningsPe) + " • Coverage " + panelCoverage;
  }

  function driverKey(item) { return ((item && item.en) || "") + " " + ((item && item.th) || ""); }
  function driverIconSvg(item) {
    var key = driverKey(item).toLowerCase(), paths;
    if (/livestock|animal|ปศุสัตว์|สัตว์/.test(key)) paths = '<path d="M4 10c0-3 3-5 7-5h3l2-2 1 4c2 .6 3 2 3 4v4h-3v3h-3v-3H8v3H5v-4H3v-4h1Z"/><circle cx="17" cy="10" r=".8"/>';
    else if (/commodity|crop|input|soy|feed cost|ต้นทุน|ถั่ว|วัตถุดิบ|พืช/.test(key)) paths = '<path d="M12 20V9"/><path d="M12 13C7 13 4 10 4 5c5 0 8 3 8 8Z"/><path d="M12 10c5 0 8-3 8-7-5 0-8 2-8 7Z"/>';
    else if (/margin|spread|mix|unit cost|cost control|อัตรากำไร|สเปรด|ต้นทุน/.test(key)) paths = '<circle cx="7" cy="7" r="2"/><circle cx="17" cy="17" r="2"/><path d="m6 18 12-12"/>';
    else if (/npat|profit|earnings|ebitda|กำไร/.test(key)) paths = '<path d="M4 20V10h4v10M10 20V5h4v15M16 20v-7h4v7"/><path d="M3 20h18"/>';
    else if (/valuation|premium|re-rating|p\/e|มูลค่า|พรีเมียม/.test(key)) paths = '<path d="M12 3v18M6 6h12M4 6l-3 7h6L4 6Zm16 0-3 7h6l-3-7Z"/><path d="M8 21h8"/>';
    else if (/export|fx|ส่งออก|อัตราแลกเปลี่ยน/.test(key)) paths = '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18"/>';
    else if (/rent|occupancy|asset|store|land|transfer|โรงแรม|พื้นที่|สินทรัพย์|โอน/.test(key)) paths = '<path d="M4 21V7l8-4 8 4v14M8 10h2M14 10h2M8 14h2M14 14h2M10 21v-4h4v4"/>';
    else if (/cash|debt|liquidity|solvency|เงินสด|หนี้|สภาพคล่อง/.test(key)) paths = '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M16 14h2"/>';
    else if (/volume|traffic|demand|orders|arrivals|ปริมาณ|ลูกค้า|คำสั่งซื้อ/.test(key)) paths = '<path d="M4 18h16M5 15l4-4 3 2 6-7"/><path d="m14 6h4v4"/>';
    else paths = '<path d="M4 18h16M5 15l4-4 3 2 6-7"/><path d="m14 6h4v4"/>';
    return '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.65" stroke-linecap="round" stroke-linejoin="round">' + paths + '</svg>';
  }
  function driverPresentation(segment,item,index) {
    var key = driverKey(item).toLowerCase(), metrics = segment.metrics;
    var presentation = { label:loc(item), value:"", detail:"", tone:"neutral" };
    if (segment.code === "F1" && index === 0) presentation = {label:copy("Livestock price","ราคาสัตว์"),value:"↑",detail:copy("recovery driver","แรงหนุนการฟื้นตัว"),tone:"positive"};
    if (segment.code === "F1" && index === 1) presentation = {label:copy("Feed cost / soybean","ต้นทุนอาหารสัตว์ / ถั่วเหลือง"),value:"↓",detail:copy("cost tailwind","ต้นทุนเอื้อต่อกำไร"),tone:"positive"};
    if (/margin|อัตรากำไร/.test(key)) {
      var delta = finite(metrics.netMarginPct) && finite(metrics.netMarginFy2024Pct) ? Number(metrics.netMarginPct) - Number(metrics.netMarginFy2024Pct) : null;
      presentation.value = finite(metrics.netMarginPct) ? Number(metrics.netMarginPct).toFixed(1) + "%" : "—";
      presentation.detail = finite(delta) ? (delta > 0 ? "+" : "") + delta.toFixed(1) + " ppt YoY" : "FY2025";
      presentation.tone = signClass(delta);
    }
    if (/npat|profit|earnings|ebitda|กำไร/.test(key)) {
      presentation.value = fmtNpat(metrics);
      presentation.detail = fmtAmount(metrics.npatOwnersFy2025Mb) + " FY2025";
      presentation.tone = /^(turned_to_loss|loss_widened)$/.test(metrics.npatState) ? "negative" : signClass(metrics.npatYoYPct);
    }
    if (/valuation|premium|re-rating|p\/e|มูลค่า|พรีเมียม/.test(key)) {
      presentation.value = fmtPe(metrics.aggregatePositiveEarningsPe);
      presentation.detail = "YTD " + fmtPct(metrics.ytdAdjustedReturnPct,1);
      presentation.tone = signClass(metrics.ytdAdjustedReturnPct);
    }
    return presentation;
  }
  function renderDriverChain(segment) {
    document.getElementById("causalChain").innerHTML = segment.chain.map(function (item,index) {
      var p = driverPresentation(segment,item,index);
      return '<article class="si-driver-node ' + esc(p.tone) + '" title="' + esc(segment.why[index % segment.why.length] ? loc(segment.why[index % segment.why.length]) : p.label) + '"><span class="si-driver-icon">' + driverIconSvg(item) + '</span><div><small>' + esc(p.label) + '</small>' + (p.value ? '<b>' + esc(p.value) + '</b>' : '') + (p.detail ? '<em>' + esc(p.detail) + '</em>' : '') + '</div></article>';
    }).join("");
  }
  function logoMarkup(ticker) {
    var meta = state.tickerMeta[ticker] || {}, url = safeUrl(meta.logoUrl);
    return '<span class="si-role-logo"><span>' + esc(String(ticker).slice(0,3)) + '</span>' + (url ? '<img src="' + esc(url) + '" alt="' + esc(ticker + ' logo') + '" loading="lazy" onerror="this.remove()">' : '') + '</span>';
  }
  function roleMetric(segment,role) {
    var company = segment.companies.find(function (item) { return item.ticker === role.ticker; });
    if (!company) return {value:"—",caption:copy("No audited company row","ไม่มีข้อมูลบริษัทในชุด audit"),tone:"neutral"};
    var key = (((role.label && role.label.en) || "") + " " + ((role.label && role.label.th) || "")).toLowerCase();
    if (/leader|ผู้นำ/.test(key)) return {value:finite(company.marketCapSharePct) ? Number(company.marketCapSharePct).toFixed(0) + "%" : "—",caption:copy("segment M-cap share","สัดส่วน Market Cap ในกลุ่ม"),tone:"neutral"};
    if (/rfo|revenue|รายได้/.test(key)) return {value:company.rfoPanel ? fmtPct(company.rfoYoYPct,1) : "—",caption:"RFO YoY · Δ " + fmtAmountDelta(company.rfoChangeMb),tone:company.rfoPanel ? signClass(company.rfoYoYPct) : "neutral"};
    if (/profit|earnings|npat|loss|กำไร|ขาดทุน/.test(key)) return {value:company.npatPanel ? fmtNpat(company) : "—",caption:"NPAT YoY · Δ " + fmtAmountDelta(company.npatChangeMb),tone:company.npatPanel ? (/^(turned_to_loss|loss_widened)$/.test(company.npatState) ? "negative" : signClass(company.npatYoYPct)) : "neutral"};
    if (/price|rising|ดาวรุ่ง|ราคา/.test(key)) return {value:fmtPct(company.ytdAdjustedReturnPct,1),caption:copy("YTD adjusted price","ราคา YTD ปรับแล้ว"),tone:signClass(company.ytdAdjustedReturnPct)};
    return {value:fmtPe(company.pe),caption:"P/E · YTD " + fmtPct(company.ytdAdjustedReturnPct,1),tone:signClass(company.ytdAdjustedReturnPct)};
  }
  function renderRoleCards(segment) {
    document.getElementById("roleList").innerHTML = segment.roles.map(function (role) {
      var metric = roleMetric(segment,role);
      return '<a class="si-role ' + esc(metric.tone) + '" href="company-summary.html?tk=' + encodeURIComponent(role.ticker) + '">' + logoMarkup(role.ticker) + '<span><small>' + esc(loc(role.label)) + '</small><strong>' + esc(role.ticker) + '</strong><b>' + esc(metric.value) + '</b><em>' + esc(metric.caption) + '</em></span></a>';
    }).join("");
  }

  function renderDetail() {
    var segment = selectedSegment();
    document.getElementById("detailKicker").textContent = segment.code + " · " + Number(segment.marketCapSharePct).toFixed(1) + "% M-cap";
    document.getElementById("detailTitle").textContent = loc(segment.headline);
    document.getElementById("observedFact").textContent = t("observed") + " — " + observedText(segment);
    var alternative = document.getElementById("alternativeFiscalView");
    if (segment.alternativeFiscalView) {
      var fiscal = segment.alternativeFiscalView;
      alternative.hidden = false;
      alternative.textContent = t("alternativeFiscal") + " — " + loc(fiscal.label) + " • " +
        fiscal.companyCount + "/" + segment.companyCount + " " + t("companies") +
        " • RFO " + fmtPct(fiscal.rfoYoYPct,1) + " • NPAT " + fmtPct(fiscal.npatYoYPct,1) +
        " • Margin " + fmtPct(fiscal.netMarginPct,1);
    } else {
      alternative.hidden = true;
      alternative.textContent = "";
    }
    document.getElementById("whyList").innerHTML = segment.why.map(function (item) { return "<li>" + esc(loc(item)) + "</li>"; }).join("");
    renderDriverChain(segment);
    renderRoleCards(segment);
    var valuation = document.getElementById("valuationBlock");
    valuation.className = "si-valuation " + segment.status;
    document.getElementById("valuationLabel").textContent = valuationLabel(segment.status);
    document.getElementById("valuationText").textContent = loc(segment.valuation);
    document.getElementById("triggerList").innerHTML = segment.triggers.map(function (item) { return "<li>" + esc(loc(item)) + "</li>"; }).join("");
    document.getElementById("riskList").innerHTML = segment.risks.map(function (item) { return "<li>" + esc(loc(item)) + "</li>"; }).join("");
    document.getElementById("mustProve").textContent = loc(segment.mustProve);
    document.getElementById("evidenceButton").textContent = t("openEvidence") + " " + segment.sources.length + " " + (language() === "th" ? "แหล่ง" : "sources");
    renderCompanies(segment);
  }

  function renderCompanies(segment) {
    document.getElementById("companyPanelTitle").textContent = t("companyPanel") + " — " + segment.code + " " + loc(segment.name);
    document.getElementById("companyPanelSubtitle").textContent = t("companyPanelSub");
    var roleMap = {};
    segment.roles.forEach(function (role) { roleMap[role.ticker] = loc(role.label); });
    var companies = segment.companies.slice(0,state.mode === 'meeting' ? 6 : segment.companies.length);
    if (!state.company || !segment.companies.some(function (company) { return company.ticker === state.company; })) state.company = companies[0] ? companies[0].ticker : null;
    document.getElementById('companyCardList').innerHTML = companies.map(function (company,index) {
      var selected = company.ticker === state.company;
      var share = finite(company.marketCapSharePct) ? clamp(Number(company.marketCapSharePct),0,100) : 0;
      var npatClass = company.npatPanel ? (/^(turned_to_loss|loss_narrowed|loss_widened)$/.test(company.npatState) ? 'negative' : signClass(company.npatYoYPct)) : 'neutral';
      return '<button type="button" class="si-company-card ' + (selected ? 'selected' : '') + '" data-company="' + esc(company.ticker) + '"><span class="si-company-card-rank">' + (index + 1) + '</span><span class="si-company-card-main"><b>' + esc(company.ticker) + '</b><small>' + esc(roleMap[company.ticker] || t('noRole')) + '</small><i><em style="--company-share:' + share.toFixed(1) + '%"></em></i></span><span class="si-company-card-metrics"><b class="' + signClass(company.rfoPanel ? company.rfoYoYPct : null) + '">RFO ' + (company.rfoPanel ? fmtPct(company.rfoYoYPct,1) : '—') + '</b><b class="' + npatClass + '">NPAT ' + (company.npatPanel ? fmtNpat(company) : '—') + '</b></span></button>';
    }).join('');
    var selectedCompany = segment.companies.find(function (company) { return company.ticker === state.company; }) || companies[0];
    if (selectedCompany) renderCompanyStory(segment,selectedCompany,roleMap[selectedCompany.ticker] || t('noRole'));
    document.getElementById("companyRows").innerHTML = segment.companies.map(function (company) {
      var npatText = company.npatPanel ? fmtNpat(company) : "—";
      return '<tr data-company="' + esc(company.ticker) + '" class="' + (company.ticker === state.company ? 'selected' : '') + '"><td><a href="company-summary.html?tk=' + encodeURIComponent(company.ticker) + '">' + esc(company.ticker) + '</a></td>' +
        '<td><span class="si-company-role">' + esc(roleMap[company.ticker] || t("noRole")) + '</span></td>' +
        '<td class="si-value">' + esc(fmtMcap(company.marketCapMb)) + '</td>' +
        '<td><span class="si-value ' + signClass(company.rfoPanel ? company.rfoYoYPct : null) + '">' + (company.rfoPanel ? fmtPct(company.rfoYoYPct,1) : "—") + '</span></td>' +
        '<td><span class="si-value ' + (company.npatPanel ? (/^(turned_to_loss|loss_narrowed|loss_widened)$/.test(company.npatState) ? "negative" : signClass(company.npatYoYPct)) : "neutral") + '">' + esc(npatText) + '</span></td>' +
        '<td><span class="si-value ' + signClass(company.ytdAdjustedReturnPct) + '">' + fmtPct(company.ytdAdjustedReturnPct,1) + '</span></td>' +
        '<td class="si-value">' + esc(fmtPe(company.pe)) + '</td>' +
        '<td class="si-value">' + (company.marginPanel && finite(company.netMarginPct) ? Number(company.netMarginPct).toFixed(1) + '%' : '—') + '</td></tr>';
    }).join("");
  }

  function companyDriverList(items) {
    if (!Array.isArray(items) || !items.length) return '<p class="si-driver-gap">' + esc(copy('No attributable driver is available.','ยังไม่มีปัจจัยขับเคลื่อนที่ระบุสาเหตุได้')) + '</p>';
    return '<ul class="si-company-driver-list">' + items.map(function (item) { return '<li>' + esc(loc(item)) + '</li>'; }).join('') + '</ul>';
  }
  function driverBasis(driver) {
    if (driver && driver.basis === 'mda_backed_synthesis') return copy('MD&A-backed synthesis','สังเคราะห์โดยมี MD&A รองรับ');
    return copy('Secondary synthesis · primary MD&A gap','สังเคราะห์จากแหล่งข้อมูลรอง · ยังไม่มี MD&A ฉบับหลัก');
  }
  function materialityLabel(level) {
    if (level === 'high') return copy('Material mover','เปลี่ยนแปลงมีนัยสำคัญ');
    if (level === 'medium') return copy('Monitor','ติดตาม');
    return copy('Standard review','ทบทวนปกติ');
  }
  function performanceLine(company,kind) {
    var isRfo = kind === 'rfo';
    var prior = isRfo ? company.rfoFy2024Mb : company.npatOwnersFy2024Mb;
    var current = isRfo ? company.rfoFy2025Mb : company.npatOwnersFy2025Mb;
    var delta = isRfo ? company.rfoChangeMb : company.npatChangeMb;
    var pct = isRfo ? company.rfoYoYPct : company.npatYoYPct;
    var panel = isRfo ? company.rfoPanel : company.npatPanel;
    return '<div class="si-performance-line"><span>FY2024 <b>' + esc(fmtAmount(prior)) + '</b></span><i>→</i><span>FY2025 <b>' + esc(fmtAmount(current)) + '</b></span><strong class="' + signClass(delta) + '">' + esc(fmtAmountDelta(delta)) + (panel && finite(pct) ? ' · ' + esc(fmtPct(pct,1)) : '') + '</strong></div>';
  }
  function renderCompanyStory(segment,company,role) {
    var driver = company.performanceDrivers || {basis:'secondary_synthesis_source_gap',materiality:'standard',rfoDrivers:[rfoNarrative(company)],npatDrivers:[npatNarrative(company)],specialItems:[],sourceIds:['FY_PANEL']};
    var npatClass = company.npatPanel ? (/^(turned_to_loss|loss_widened)$/.test(company.npatState) ? 'negative' : signClass(company.npatYoYPct)) : 'neutral';
    var basisClass = driver.primaryMdaAvailable ? 'management_explanation' : 'source_gap';
    var special = Array.isArray(driver.specialItems) && driver.specialItems.length ? '<section class="si-company-special"><div><span class="si-source-kind analyst_inference">' + esc(copy('Special / non-recurring','รายการพิเศษ / ไม่ประจำ')) + '</span><b>' + esc(copy('Reported-to-core bridge','เชื่อมจากกำไรรายงานสู่กำไรหลัก')) + '</b></div>' + companyDriverList(driver.specialItems) + '</section>' : '';
    document.getElementById('companyStory').innerHTML = '<header class="si-company-story-head"><div><span>' + esc(t('selectedCompany') + ' · ' + role) + '</span><div class="si-company-title-row"><h4>' + esc(company.ticker) + '</h4><em class="si-materiality ' + esc(driver.materiality) + '">' + esc(materialityLabel(driver.materiality)) + '</em></div><p>' + esc(companyBridge(company)) + '</p></div><a href="company-summary.html?tk=' + encodeURIComponent(company.ticker) + '">' + esc(copy('Open company','เปิดหน้าบริษัท')) + ' ↗</a></header>' +
      '<div class="si-company-kpis"><div><b>' + esc(fmtMcap(company.marketCapMb)) + '</b><small>M-cap</small></div><div><b>' + (finite(company.priceThb) ? Number(company.priceThb).toFixed(2) : '—') + '</b><small>' + esc(copy('Price THB','ราคา บาท')) + '</small></div><div><b class="' + signClass(company.ytdAdjustedReturnPct) + '">' + fmtPct(company.ytdAdjustedReturnPct,1) + '</b><small>YTD</small></div><div><b>' + esc(fmtPe(company.pe)) + '</b><small>P/E</small></div><div><b>' + (company.marginPanel && finite(company.netMarginPct) ? Number(company.netMarginPct).toFixed(1) + '%' : '—') + '</b><small>NPAT / RFO</small></div></div>' +
      '<div class="si-company-why-grid"><section class="si-driver-panel rfo"><div><span class="si-source-kind ' + basisClass + '">' + esc(driverBasis(driver)) + '</span><b class="' + signClass(company.rfoPanel ? company.rfoYoYPct : null) + '">' + esc(t('rfoWhy')) + '</b></div>' + performanceLine(company,'rfo') + companyDriverList(driver.rfoDrivers) + '</section><section class="si-driver-panel npat"><div><span class="si-source-kind ' + basisClass + '">' + esc(driverBasis(driver)) + '</span><b class="' + npatClass + '">' + esc(t('npatWhy')) + '</b></div>' + performanceLine(company,'npat') + companyDriverList(driver.npatDrivers) + '</section></div>' +
      special + '<div class="si-company-context si-company-evidence-bar"><div><span class="si-source-kind ' + basisClass + '">' + esc(driver.primaryMdaAvailable ? copy('Primary filing checked','ตรวจเอกสาร MD&A หลักแล้ว') : copy('Primary-source gap','ขาดเอกสารต้นทางหลัก')) + '</span><b>' + esc(copy('Evidence trail','เส้นทางหลักฐาน')) + '</b></div><p>' + esc(copy('Audited RFO and owner-NPAT amounts are kept separate from the causal explanation. Open evidence to inspect the FY2025 MD&A path, URL and SHA-256.','ตัวเลข RFO และ NPAT ส่วนผู้ถือหุ้นที่สอบทานแล้วแยกจากคำอธิบายสาเหตุ เปิดหลักฐานเพื่อตรวจเส้นทางไฟล์ ลิงก์ และค่า SHA-256 ของ MD&A ปี 2568')) + '</p><button type="button" data-open-evidence>' + esc(t('source')) + ' · ' + esc((driver.sourceIds || ['FY_PANEL']).join(' / ')) + ' ↗</button></div>';
  }  function renderFlow() {
    document.querySelectorAll("[data-flow]").forEach(function (button) { button.classList.toggle("active",button.dataset.flow === state.flow); });
  }

  function render() {
    applyStaticLabels();
    renderControls();
    renderOverview();
    renderVisuals();
    renderSegments();
    renderDetail();
    renderFlow();
    updateUrl();
  }

  function updateUrl() {
    var params = new URLSearchParams(location.search);
    params.set("sector",state.sector);
    params.set("segment",state.segment);
    if (state.company) params.set("company",state.company); else params.delete("company");
    params.set("mode",state.mode);
    params.set("flow",state.flow);
    history.replaceState(null,"",location.pathname + "?" + params.toString() + location.hash);
  }

  function selectSegment(code,moveFocus) {
    var exists = selectedSector().segments.some(function (segment) { return segment.code === code; });
    if (!exists) return;
    state.segment = code;
    state.company = null;
    state.flow = "segment";
    render();
    if (moveFocus) {
      var row = document.querySelector('[data-segment="' + CSS.escape(code) + '"]');
      if (row) row.focus({preventScroll:true});
    }
  }

  function selectCompany(ticker) {
    var segment = selectedSegment();
    if (!segment.companies.some(function (company) { return company.ticker === ticker; })) return;
    state.company = ticker;
    state.flow = 'company';
    render();
  }
  function moveSegment(delta) {
    var segments = selectedSector().segments;
    var index = segments.findIndex(function (segment) { return segment.code === state.segment; });
    var next = segments[Math.max(0,Math.min(segments.length - 1,index + delta))];
    if (next) selectSegment(next.code,true);
  }

  function openEvidence() {
    var segment = selectedSegment();
    var meta = state.data.meta;
    var sourceMap = {};
    segment.sources.forEach(function (source) { sourceMap[source.sourceId] = source; });
    state.flow = "evidence";
    renderFlow();
    updateUrl();
    document.getElementById("dialogKicker").textContent = t("source") + " · " + segment.code;
    document.getElementById("dialogTitle").textContent = loc(segment.name);
    document.getElementById("methodologyList").innerHTML = Object.keys(meta.definitions).map(function (key) {
      return "<dt>" + esc(key.toUpperCase()) + "</dt><dd>" + esc(meta.definitions[key]) + "</dd>";
    }).join("");
    var evidenceClaims = segment.claims.slice();
    var evidenceCompany = segment.companies.find(function (company) { return company.ticker === state.company; });
    if (evidenceCompany && evidenceCompany.performanceDrivers) {
      var driver = evidenceCompany.performanceDrivers;
      var driverKind = driver.primaryMdaAvailable ? 'management_explanation' : 'analyst_inference';
      (driver.rfoDrivers || []).forEach(function (text) { evidenceClaims.push({section:'company_rfo_' + evidenceCompany.ticker,kind:driverKind,text:text,sourceIds:driver.sourceIds || ['FY_PANEL']}); });
      (driver.npatDrivers || []).forEach(function (text) { evidenceClaims.push({section:'company_npat_' + evidenceCompany.ticker,kind:driverKind,text:text,sourceIds:driver.sourceIds || ['FY_PANEL']}); });
      (driver.specialItems || []).forEach(function (text) { evidenceClaims.push({section:'company_special_' + evidenceCompany.ticker,kind:'analyst_inference',text:text,sourceIds:driver.sourceIds || ['FY_PANEL']}); });
      document.getElementById("dialogTitle").textContent = loc(segment.name) + ' · ' + evidenceCompany.ticker;
    }
    document.getElementById("claimList").innerHTML = evidenceClaims.map(function (claim) {
      var links = claim.sourceIds.map(function (sourceId) {
        var source = sourceMap[sourceId] || {};
        return '<span title="' + esc(source.label || sourceId) + '">' + esc(sourceId) + '</span>';
      }).join("");
      return '<article class="si-claim-item ' + esc(claim.kind) + '">' +
        '<div class="si-claim-head"><span class="si-source-kind">' + esc(t(claim.kind) || claim.kind) + '</span><code>' + esc(claim.section) + '</code></div>' +
        '<p>' + esc(loc(claim.text)) + '</p><div class="si-claim-sources">' + links + '</div></article>';
    }).join("");
    document.getElementById("sourceList").innerHTML = segment.sources.map(function (source) {
      var href = safeUrl(source.url);
      var metadata = '<dl class="si-source-meta"><dt>' + esc(t("sourceId")) + '</dt><dd><code>' + esc(source.sourceId) + '</code></dd>' +
        '<dt>' + esc(t("sourceRole")) + '</dt><dd>' + esc(source.role || "—") + '</dd>' +
        '<dt>' + esc(t("sourcePath")) + '</dt><dd><code>' + esc(source.path || "—") + '</code></dd>' +
        '<dt>' + esc(t("sourceHash")) + '</dt><dd><code>' + esc(source.sha256 || "—") + '</code></dd></dl>';
      return '<article class="si-source-item ' + esc(source.kind) + '"><span class="si-source-kind">' + esc(t(source.kind) || source.kind) + '</span><div><strong>' + esc(source.label) + '</strong><p>' + esc(source.detail) + '</p>' + metadata + '</div>' + (href ? '<a href="' + esc(href) + '" target="_blank" rel="noopener">' + esc(t("open")) + ' ↗</a>' : '') + '</article>';
    }).join("");
    document.getElementById("sourceWarning").textContent = meta.warning;
    var dialog = document.getElementById("evidenceDialog");
    if (!dialog.open) dialog.showModal();
  }

  function bindEvents() {
    document.getElementById("sectorSwitch").addEventListener("click",function (event) {
      var button = event.target.closest("[data-sector]");
      if (!button) return;
      state.sector = button.dataset.sector;
      state.segment = selectedSector().focusSegment;
      state.company = null;
      state.flow = "overview";
      render();
    });
    document.getElementById("modeSwitch").addEventListener("click",function (event) {
      var button = event.target.closest("[data-mode]");
      if (!button) return;
      state.mode = button.dataset.mode;
      render();
    });
    document.getElementById("segmentRows").addEventListener("click",function (event) {
      var row = event.target.closest("[data-segment]");
      if (row) selectSegment(row.dataset.segment,false);
    });
    document.getElementById("segmentRows").addEventListener("keydown",function (event) {
      var row = event.target.closest("[data-segment]");
      if (!row) return;
      if (event.key === "Enter" || event.key === " ") { event.preventDefault(); selectSegment(row.dataset.segment,true); }
      if (event.key === "ArrowDown") { event.preventDefault(); moveSegment(1); }
      if (event.key === "ArrowUp") { event.preventDefault(); moveSegment(-1); }
    });
    document.getElementById('visualStorySection').addEventListener('click',function (event) {
      var target = event.target.closest('[data-segment]');
      if (target) selectSegment(target.dataset.segment,false);
    });
    document.getElementById('visualStorySection').addEventListener('keydown',function (event) {
      var target = event.target.closest('[data-segment]');
      if (target && (event.key === 'Enter' || event.key === ' ')) { event.preventDefault(); selectSegment(target.dataset.segment,false); }
    });
    document.getElementById('companyCardList').addEventListener('click',function (event) {
      var target = event.target.closest('[data-company]');
      if (target) selectCompany(target.dataset.company);
    });
    document.getElementById('companyStory').addEventListener('click',function (event) {
      if (event.target.closest('[data-open-evidence]')) openEvidence();
    });
    document.getElementById('companyRows').addEventListener('click',function (event) {
      if (event.target.closest('a')) return;
      var target = event.target.closest('[data-company]');
      if (target) selectCompany(target.dataset.company);
    });    document.getElementById("evidenceButton").addEventListener("click",openEvidence);
    document.getElementById("closeEvidence").addEventListener("click",function () { document.getElementById("evidenceDialog").close(); });
    document.getElementById("evidenceDialog").addEventListener("click",function (event) {
      if (event.target === event.currentTarget) event.currentTarget.close();
    });
    document.getElementById("copyDeepLink").addEventListener("click",async function (event) {
      try {
        await navigator.clipboard.writeText(location.href);
        event.currentTarget.textContent = t("copied");
        setTimeout(function () { event.currentTarget.textContent = t("copyLink"); },1200);
      } catch (_) {
        event.currentTarget.textContent = t("copyLink");
      }
    });
    document.querySelectorAll(".si-flow").forEach(function (flowNav) {
      flowNav.addEventListener("click",function (event) {
        var button = event.target.closest("[data-flow]");
        if (!button) return;
        var flow = button.dataset.flow;
        state.flow = flow;
        renderFlow();
        updateUrl();
        if (flow === "overview") document.getElementById("overviewSection").scrollIntoView({behavior:"smooth",block:"start"});
        if (flow === "segment") document.getElementById("segmentSection").scrollIntoView({behavior:"smooth",block:"start"});
        if (flow === "company") {
          state.mode = "explore";
          render();
          document.getElementById("companyPanel").scrollIntoView({behavior:"smooth",block:"start"});
        }
        if (flow === "evidence") openEvidence();
      });
    });
    window.addEventListener("keydown",function (event) {
      if (event.target && /INPUT|TEXTAREA|SELECT/.test(event.target.tagName)) return;
      if (event.key.toLowerCase() === "e") openEvidence();
    });
    window.addEventListener("i18n:change",function () {
      if (window.I18N) I18N.apply();
      if (state.data) render();
    });
  }

  async function init() {
    bindEvents();
    try {
      var tickerPromise = fetch("./data/ticker-summary.json",{cache:"no-store"}).then(function (response) { return response.ok ? response.json() : {tickers:[]}; }).catch(function () { return {tickers:[]}; });
      var response = await fetch("./data/sector-intelligence.json",{cache:"no-store"});
      if (!response.ok) throw new Error("HTTP " + response.status);
      var payloads = await Promise.all([response.json(),tickerPromise]);
      state.data = payloads[0];
      (payloads[1].tickers || []).forEach(function (ticker) { if (ticker && ticker.tk) state.tickerMeta[ticker.tk] = ticker; });
      var sector = selectedSector();
      if (!state.segment || !sector.segments.some(function (segment) { return segment.code === state.segment; })) state.segment = sector.focusSegment || sector.segments[0].code;
      var initialSegment = selectedSegment();
      if (!state.company || !initialSegment.companies.some(function (company) { return company.ticker === state.company; })) state.company = initialSegment.companies[0] ? initialSegment.companies[0].ticker : null;
      document.getElementById("loadingState").hidden = true;
      document.getElementById("contentState").hidden = false;
      app.setAttribute("aria-busy","false");
      render();
      if (state.flow === "evidence") openEvidence();
    } catch (error) {
      document.getElementById("loadingState").hidden = true;
      var errorState = document.getElementById("errorState");
      errorState.hidden = false;
      errorState.textContent = t("dataError") + ": " + error.message;
      app.setAttribute("aria-busy","false");
    }
  }

  init();
})();
