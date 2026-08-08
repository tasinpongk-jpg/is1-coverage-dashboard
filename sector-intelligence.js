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
      companyPanelSub:"Top companies by current market cap; data uses the same segment perimeter",
      noRole:"Constituent", open:"Open", source:"Source", keyboard:"Use ↑ / ↓ to move • Enter or click to open • E for evidence",
      loss:"Loss", lossNarrowed:"Loss narrowed", lossWidened:"Loss widened", turnedProfit:"Turned profitable", notMeaningful:"n.m.", dataError:"Could not load Sector Intelligence data",
      marketCutoff:"Market data as of {date} • {period}", sourceLineage:"Sources: {sources}",
      definitions:"RFO = Revenue from Operations • NPAT = net profit to owners • Price = adjusted, excludes cash dividends",
      fact:"Fact", fact_calculated:"Calculated fact", management:"Management", management_explanation:"Management explanation", forward:"Forward view", credit_analysis:"Credit analysis", analyst_inference:"Analyst inference", analyst_test:"Analyst test", claimsRegister:"Claim register", known:"known",
      alternativeFiscal:"Alternative issuer-FY view", sourceId:"Source ID", sourceRole:"Role", sourcePath:"Path", sourceHash:"SHA-256"
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
      companyPanelSub:"บริษัทเรียงตาม Market Cap ปัจจุบัน โดยใช้ perimeter เดียวกับ Segment",
      noRole:"บริษัทในกลุ่ม", open:"เปิด", source:"แหล่งข้อมูล", keyboard:"ใช้ ↑ / ↓ เพื่อเลื่อน • Enter หรือคลิกเพื่อเปิด • กด E เพื่อดูหลักฐาน",
      loss:"ขาดทุน", lossNarrowed:"ขาดทุนลดลง", lossWidened:"ขาดทุนเพิ่มขึ้น", turnedProfit:"กลับเป็นกำไร", notMeaningful:"n.m.", dataError:"ไม่สามารถโหลดข้อมูล Sector Intelligence ได้",
      marketCutoff:"ข้อมูลตลาด ณ {date} • {period}", sourceLineage:"แหล่งข้อมูล: {sources}",
      definitions:"RFO = Revenue from Operations • NPAT = กำไรส่วนผู้ถือหุ้น • ราคา = adjusted ไม่รวมเงินปันผล",
      fact:"ข้อเท็จจริง", fact_calculated:"ข้อเท็จจริงจากการคำนวณ", management:"ฝ่ายจัดการ", management_explanation:"คำอธิบายฝ่ายจัดการ", forward:"มุมมองล่วงหน้า", credit_analysis:"บทวิเคราะห์เครดิต", analyst_inference:"ข้ออนุมานนักวิเคราะห์", analyst_test:"ประเด็นที่ต้องพิสูจน์", claimsRegister:"ทะเบียนข้อสรุป", known:"มีข้อมูล",
      alternativeFiscal:"มุมมองตามปีบัญชีของผู้ออก", sourceId:"รหัสแหล่งข้อมูล", sourceRole:"บทบาท", sourcePath:"พาธ", sourceHash:"SHA-256"
    }
  };

  var state = { data:null, sector:"FOOD", segment:null, mode:"meeting", flow:"overview" };
  var app = document.getElementById("sectorIntelligenceApp");
  var query = new URLSearchParams(location.search);
  if (/^(FOOD|PROP)$/.test(query.get("sector") || "")) state.sector = query.get("sector");
  if (/^[FP]\d$/.test(query.get("segment") || "")) state.segment = query.get("segment");
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
    document.getElementById("causalChain").innerHTML = segment.chain.map(function (item) { return "<span>" + esc(loc(item)) + "</span>"; }).join("");
    document.getElementById("roleList").innerHTML = segment.roles.map(function (role) {
      return '<a class="si-role" href="company-summary.html?tk=' + encodeURIComponent(role.ticker) + '"><small>' + esc(loc(role.label)) + '</small><strong>' + esc(role.ticker) + '</strong></a>';
    }).join("");
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
    document.getElementById("companyRows").innerHTML = segment.companies.slice(0,10).map(function (company) {
      var npatText = company.npatPanel ? fmtNpat(company) : "—";
      return '<tr><td><a href="company-summary.html?tk=' + encodeURIComponent(company.ticker) + '">' + esc(company.ticker) + '</a></td>' +
        '<td><span class="si-company-role">' + esc(roleMap[company.ticker] || t("noRole")) + '</span></td>' +
        '<td class="si-value">' + esc(fmtMcap(company.marketCapMb)) + '</td>' +
        '<td><span class="si-value ' + signClass(company.rfoPanel ? company.rfoYoYPct : null) + '">' + (company.rfoPanel ? fmtPct(company.rfoYoYPct,1) : "—") + '</span></td>' +
        '<td><span class="si-value ' + (company.npatPanel ? (/^(turned_to_loss|loss_narrowed|loss_widened)$/.test(company.npatState) ? "negative" : signClass(company.npatYoYPct)) : "neutral") + '">' + esc(npatText) + '</span></td>' +
        '<td><span class="si-value ' + signClass(company.ytdAdjustedReturnPct) + '">' + fmtPct(company.ytdAdjustedReturnPct,1) + '</span></td>' +
        '<td class="si-value">' + esc(fmtPe(company.pe)) + '</td>' +
        '<td class="si-value">' + (company.marginPanel && finite(company.netMarginPct) ? Number(company.netMarginPct).toFixed(1) + '%' : '—') + '</td></tr>';
    }).join("");
  }

  function renderFlow() {
    document.querySelectorAll("[data-flow]").forEach(function (button) { button.classList.toggle("active",button.dataset.flow === state.flow); });
  }

  function render() {
    applyStaticLabels();
    renderControls();
    renderOverview();
    renderSegments();
    renderDetail();
    renderFlow();
    updateUrl();
  }

  function updateUrl() {
    var params = new URLSearchParams(location.search);
    params.set("sector",state.sector);
    params.set("segment",state.segment);
    params.set("mode",state.mode);
    params.set("flow",state.flow);
    history.replaceState(null,"",location.pathname + "?" + params.toString() + location.hash);
  }

  function selectSegment(code,moveFocus) {
    var exists = selectedSector().segments.some(function (segment) { return segment.code === code; });
    if (!exists) return;
    state.segment = code;
    state.flow = "segment";
    render();
    if (moveFocus) {
      var row = document.querySelector('[data-segment="' + CSS.escape(code) + '"]');
      if (row) row.focus({preventScroll:true});
    }
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
    document.getElementById("claimList").innerHTML = segment.claims.map(function (claim) {
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
    document.getElementById("evidenceButton").addEventListener("click",openEvidence);
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
      var response = await fetch("./data/sector-intelligence.json",{cache:"no-store"});
      if (!response.ok) throw new Error("HTTP " + response.status);
      state.data = await response.json();
      var sector = selectedSector();
      if (!state.segment || !sector.segments.some(function (segment) { return segment.code === state.segment; })) state.segment = sector.focusSegment || sector.segments[0].code;
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
