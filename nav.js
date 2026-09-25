/**
 * IS1 Modular Control Room shell.
 *
 * Every page already loads nav.js, so this file is the single app-shell
 * runtime for desktop and mobile navigation, ticker search, RM context and
 * the right-side analyst drawer. Existing page markup and data logic remain
 * untouched behind the shell.
 */
(function () {
  "use strict";

  if (new URLSearchParams(location.search).get("embedded") === "1") {
    document.documentElement.classList.add("is1-embedded");
    return;
  }

  if (document.querySelector(".is1s-rail")) return;

  var GROUPS = [
    {
      id:"home", label:["Home","หน้าหลัก"], short:["Home","หน้าหลัก"], icon:"layout-dashboard", color:"#f2aa1f",
      pages:[
        ["index.html","Morning overview","ภาพรวมเช้า","activity"],
        ["visits.html","Visit planner","แผนเยี่ยมบริษัท","calendar-days"],
        ["ai-insights.html","AI insights","AI insights","sparkles"],
      ],
    },
    {
      id:"market", label:["Market","ตลาด"], short:["Market","ตลาด"], icon:"chart-no-axes-combined", color:"#5d96ff",
      pages:[
        ["price-movement.html","Price movement","ความเคลื่อนไหวราคา","trending-up"],
        ["sector-intelligence.html","Sector intelligence","บทวิเคราะห์รายกลุ่ม","chart-no-axes-combined"],
        ["multiples-comparison.html","Multiples comparison","เปรียบเทียบ multiples","columns-3"],
        ["multiples-band.html","Multiples band","ช่วง multiples","chart-spline"],
        ["https://tradingview-daily-dashboard.tasinpong-k.workers.dev/","Daily market board","กระดานตลาดรายวัน","monitor-up"],
      ],
    },
    {
      id:"companies", label:["Companies","บริษัท"], short:["Companies","บริษัท"], icon:"building-2", color:"#35bdd0",
      pages:[
        ["company-summary.html","Company summary","ข้อมูลรายบริษัท","notebook-tabs"],
        ["oppday-minutes.html","Oppday minutes","สรุป Oppday","presentation"],
        ["sec-form59.html","SEC Form 59","แบบ 59","contact-round"],
      ],
    },
    {
      id:"news", label:["News","ข่าว"], short:["News","ข่าว"], icon:"newspaper", color:"#31c77b",
      pages:[
        ["disclosure-pulse.html","SET disclosures","ข่าวเปิดเผยข้อมูล","radio-tower","filings"],
        ["external-news.html","External news","ข่าวภายนอก","rss","news"],
        ["efinance-news.html","eFinanceThai live","ข่าว eFinanceThai","newspaper"],
        ["https://macro-brief-buy.pages.dev","Global-macro brief","สรุปมหภาคโลก","globe-2"],
      ],
    },
    {
      id:"surveillance", label:["Risk & surveillance","เฝ้าระวัง"], short:["Risk","เฝ้าระวัง"], icon:"shield-alert", color:"#ef6464",
      pages:[
        ["unusual-trading.html","Unusual trading","การซื้อขายผิดปกติ","siren","alerts"],
        ["trading-signs.html","Trading signs","เครื่องหมายซื้อขาย","flag"],
        ["sec-enforcement.html","SEC enforcement","การบังคับใช้กฎหมาย","shield-check"],
        ["governance-screen.html","Governance screen","ตรวจสอบธรรมาภิบาล","scale"],
      ],
    },
    {
      id:"bonds", label:["Bonds","หุ้นกู้"], short:["Bonds","หุ้นกู้"], icon:"landmark", color:"#b17cff",
      pages:[
        ["bond-summary.html","Bond summary","สรุปหุ้นกู้","chart-pie"],
        ["bond-data-sec.html","SEC bond filings","ข้อมูลหุ้นกู้ SEC","database"],
      ],
    },
  ];

  var EMBEDDED_WORKSPACES = {
    "https://tradingview-daily-dashboard.tasinpong-k.workers.dev/": {
      title:["Daily market board","กระดานตลาดรายวัน"],
      description:["Live market dashboard","Dashboard ตลาดแบบ live"],
    },
    "https://macro-brief-buy.pages.dev": {
      title:["Global-macro brief","สรุปมหภาคโลก"],
      description:["Macro signals and global context","สัญญาณมหภาคและบริบทตลาดโลก"],
    },
  };

  var PAGE_META = {
    "price-movement":      ["Market","Daily price moves across coverage","ความเคลื่อนไหวราคารายวันใน coverage","#5d96ff","trending-up"],
    "sector-intelligence": ["Market","Meeting-ready FOOD and PROP sector briefing","บทวิเคราะห์ FOOD และ PROP สำหรับนำเสนอในที่ประชุม","#f2aa1f","chart-no-axes-combined"],
    "company-summary":     ["Companies","Fundamentals and profile per company","ข้อมูลพื้นฐานและ profile รายบริษัท","#35bdd0","notebook-tabs"],
    "multiples-comparison":["Market","Valuation multiples side by side","เปรียบเทียบ valuation multiples","#5d96ff","columns-3"],
    "multiples-band":      ["Market","Valuation ranges across all sectors","ช่วง valuation ของทุก sector","#5d96ff","chart-spline"],
    "disclosure-pulse":    ["News","Live SET filings ranked by importance","ข่าว SET ล่าสุดเรียงตามความสำคัญ","#31c77b","radio-tower"],
    "external-news":       ["News","Ticker-matched external headlines","ข่าวภายนอกที่จับคู่กับ ticker","#31c77b","rss"],
    "efinance-news":       ["News","Live headlines from eFinanceThai","พาดหัวข่าวล่าสุดจาก eFinanceThai","#31c77b","newspaper"],
    "oppday-minutes":      ["Companies","Earnings-call notes and takeaways","สรุปประเด็นจาก Oppday","#35bdd0","presentation"],
    "ai-insights":         ["Home","Validated commentary from daily snapshots","บทวิเคราะห์จาก daily snapshots","#f2aa1f","sparkles"],
    "unusual-trading":     ["Risk & surveillance","Volume and price anomalies","ความผิดปกติด้านราคาและปริมาณซื้อขาย","#ef6464","siren"],
    "trading-signs":       ["Risk & surveillance","Current SET trading signs","เครื่องหมายซื้อขายของ SET","#ef6464","flag"],
    "sec-enforcement":     ["Risk & surveillance","Thai SEC enforcement actions","การบังคับใช้กฎหมายของ SEC","#ef6464","shield-check"],
    "sec-form59":          ["Companies","Management and related-person trades","รายการซื้อขายของผู้บริหารและบุคคลที่เกี่ยวข้อง","#35bdd0","contact-round"],
    "bond-summary":        ["Bonds","Outstanding bonds across coverage","หุ้นกู้คงค้างใน coverage","#b17cff","chart-pie"],
    "bond-data-sec":       ["Bonds","Bond filings from the SEC","ข้อมูล filing หุ้นกู้จาก SEC","#b17cff","database"],
    "governance-screen":   ["Risk & surveillance","Auditor fees, AGM timing and board independence","ค่าสอบบัญชี กำหนดประชุมสามัญผู้ถือหุ้น และสัดส่วนกรรมการอิสระ","#ef6464","scale"],
    "visits":              ["Home","Plan and track company visits","วางแผนและติดตามการเยี่ยมบริษัท","#f2aa1f","calendar-days"],
  };

  var ICONS = {
    "activity":'<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "arrow-right":'<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "arrow-up-right":'<path d="M7 17 17 7"/><path d="M7 7h10v10"/>',
    "building-2":'<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18"/><path d="M6 12H4a2 2 0 0 0-2 2v8h20v-8a2 2 0 0 0-2-2h-2"/><path d="M10 6h4M10 10h4M10 14h4M10 18h4"/>',
    "calendar-days":'<path d="M8 2v4M16 2v4M3 10h18"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M8 14h.01M12 14h.01M16 14h.01M8 18h.01M12 18h.01"/>',
    "chart-no-axes-combined":'<path d="M12 16v5M16 14v7M20 10v11M4 18v3M8 14v7"/><path d="m3 7 5 5 4-4 5 5 4-4"/>',
    "chart-pie":'<path d="M21 12c.552 0 1.005-.449.95-.998a10 10 0 0 0-8.953-8.953C12.449 1.995 12 2.448 12 3v8a1 1 0 0 0 1 1z"/><path d="M21.21 15.89A10 10 0 1 1 8.11 2.79"/>',
    "chart-spline":'<path d="M3 3v18h18"/><path d="M7 16c.5-2 1.5-3 3-3 2 0 2 3 4 3 1.5 0 2.5-2 3-4 .5-2 1.5-3 3-3"/>',
    "columns-3":'<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18M15 3v18"/>',
    "contact-round":'<path d="M16 2v2M17.915 22a6 6 0 0 0-12 0"/><circle cx="12" cy="12" r="4"/><rect width="18" height="18" x="3" y="4" rx="2"/>',
    "database":'<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.7 4 3 9 3s9-1.3 9-3V5"/><path d="M3 12c0 1.7 4 3 9 3s9-1.3 9-3"/>',
    "flag":'<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><path d="M4 22v-7"/>',
    "globe-2":'<path d="M12 22a10 10 0 1 0 0-20 10 10 0 0 0 0 20Z"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 0 20M12 2a15.3 15.3 0 0 0 0 20"/>',
    "landmark":'<path d="M3 22h18M6 18v-7M10 18v-7M14 18v-7M18 18v-7M12 2l9 5H3z"/>',
    "layout-dashboard":'<rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>',
    "menu":'<path d="M4 12h16M4 6h16M4 18h16"/>',
    "monitor-up":'<path d="m9 10 2 2 4-4"/><rect width="20" height="14" x="2" y="3" rx="2"/><path d="M12 17v4M8 21h8"/>',
    "newspaper":'<path d="M4 22h16a2 2 0 0 0 2-2V4H6v16a2 2 0 0 1-4 0V6h4"/><path d="M10 8h8M10 12h8M10 16h5"/>',
    "notebook-tabs":'<path d="M2 6h4M2 10h4M2 14h4M2 18h4"/><rect width="16" height="20" x="4" y="2" rx="2"/><path d="M15 2v20M15 7h5M15 12h5M15 17h5"/>',
    "panel-left-close":'<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18M16 15l-3-3 3-3"/>',
    "panel-right-close":'<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M15 3v18M8 9l3 3-3 3"/>',
    "panel-right-open":'<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M15 3v18M10 15l-3-3 3-3"/>',
    "presentation":'<path d="M2 3h20M3 3v11a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V3M12 15v6M8 21h8"/>',
    "radio-tower":'<path d="M4.9 19.1C1 15.2 1 8.8 4.9 4.9M7.8 16.2a6 6 0 0 1 0-8.4M19.1 4.9c3.9 3.9 3.9 10.3 0 14.2M16.2 7.8a6 6 0 0 1 0 8.4"/><circle cx="12" cy="12" r="2"/><path d="m8.5 22 3.5-8 3.5 8M9 18h6"/>',
    "rss":'<path d="M4 11a9 9 0 0 1 9 9M4 4a16 16 0 0 1 16 16"/><circle cx="5" cy="19" r="1"/>',
    "search":'<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "scale":'<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    "shield-alert":'<path d="M20 13c0 5-3.5 7.5-7.7 9a1 1 0 0 1-.6 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.2-2.7a1.2 1.2 0 0 1 1.6 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/><path d="M12 8v4M12 16h.01"/>',
    "shield-check":'<path d="M20 13c0 5-3.5 7.5-7.7 9a1 1 0 0 1-.6 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.2-2.7a1.2 1.2 0 0 1 1.6 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "siren":'<path d="M7 18v-6a5 5 0 0 1 10 0v6M5 22h14M5 18h14M12 2v3M4.9 4.9 7 7M19.1 4.9 17 7"/>',
    "sparkles":'<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/><path d="M5 3v4M3 5h4M19 17v4M17 19h4"/>',
    "trending-up":'<path d="m3 17 6-6 4 4 8-8"/><path d="M14 7h7v7"/>',
  };

  var RMS = ["C","K","O","G","P","T"];
  var RM_CHOICES = ["ALL"].concat(RMS);
  var state = {
    rm:localStorage.getItem("is1_rm") || "C",
    context:"coverage",
    selectedTicker:null,
    data:null,
  };
  if (RM_CHOICES.indexOf(state.rm) < 0) state.rm = "C";

  var script = document.currentScript;
  if (!script) {
    var scripts = document.querySelectorAll('script[src*="nav.js"]');
    script = scripts[scripts.length - 1];
  }
  var base = "";
  try { base = new URL(script.src).origin; } catch (e) {}
  var here = location.pathname.split("/").pop() || "index.html";
  var hereKey = here.replace(/\.html$/,"") || "index";
  var isHome = hereKey === "index" || hereKey === "";

  function L(en,th) { return window.I18N && I18N.lang === "th" ? th : en; }
  function rmLabel(rm) { return rm === "ALL" ? L("All RMs","ทุก RM") : "RM " + rm; }
  // Same windows the News pages open with, so a badge matches the list behind it:
  // SET disclosures default to 1d, External news to 7d.
  function withinHours(ts,hours) {
    var t = Date.parse(ts);
    return Number.isFinite(t) && Date.now() - t <= hours * 3600 * 1000;
  }
  function icon(name,cls) {
    return '<svg class="' + (cls || "is1s-icon") + '" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' +
      (ICONS[name] || ICONS.activity) + "</svg>";
  }
  function esc(value) {
    return String(value == null ? "" : value).replace(/[&<>"']/g,function (c) {
      return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
    });
  }
  function safeHttpUrl(value) {
    try {
      var parsed = new URL(String(value || ""),location.href);
      return parsed.protocol === "http:" || parsed.protocol === "https:" ? parsed.href : "";
    } catch (e) {
      return "";
    }
  }
  function href(path) {
    if (/^https?:\/\//.test(path)) return path;
    return base ? base + "/" + path : path;
  }
  function finite(value) { return value !== null && value !== "" && Number.isFinite(Number(value)); }
  function average(values) {
    var nums = values.filter(finite).map(Number);
    return nums.length ? nums.reduce(function (sum,value) { return sum + value; },0) / nums.length : null;
  }
  function fmtPct(value,digits) {
    if (!finite(value)) return "n/a";
    var n = Number(value);
    return (n > 0 ? "+" : "") + n.toFixed(digits == null ? 2 : digits) + "%";
  }
  function canonicalSector(value) { return value === "PFREIT" ? "PF&REIT" : value; }
  function firstPage(group) {
    var local = group.pages.filter(function (page) { return !/^https?:/.test(page[0]); });
    return (local[0] || group.pages[0])[0];
  }
  function currentPage() {
    var found = null;
    GROUPS.some(function (group) {
      return group.pages.some(function (page) {
        if (/^https?:/.test(page[0])) return false;
        if (page[0].replace(/\.html$/,"") === hereKey) {
          found = { group:group, page:page };
          return true;
        }
        return false;
      });
    });
    return found;
  }

  var pageInfo = currentPage();
  var selectedModuleId = pageInfo ? pageInfo.group.id : "home";
  var legacyHeader = Array.prototype.find.call(document.body.children,function (node) { return node.tagName === "HEADER"; });
  if (legacyHeader) legacyHeader.classList.add("is1s-legacy-header");
  document.body.classList.add("is1-shell-ready");
  document.body.classList.add("is1s-page-" + hereKey.replace(/[^a-z0-9-]/g,""));

  var rail = document.createElement("aside");
  rail.className = "is1s-rail";
  rail.setAttribute("aria-label",L("Primary modules","เมนูหลัก"));
  rail.innerHTML =
    '<a class="is1s-mark" href="' + href("index.html") + '" aria-label="IS1 Control Room">IS</a>' +
    '<nav class="is1s-rail-nav">' +
      GROUPS.map(function (group) {
        var active = selectedModuleId === group.id;
        var name = esc(L(group.label[0],group.label[1]));
        var inner = icon(group.icon) + '<span class="is1s-rail-label">' + esc(L(group.short[0],group.short[1])) + "</span>";
        // The current page's group toggles the page panel; any other group
        // opens that group's first page, so one click always goes somewhere.
        if (!active) {
          return '<a class="is1s-rail-btn" data-module="' + group.id + '" href="' + esc(href(firstPage(group))) +
            '" aria-label="' + name + '" title="' + name + '">' + inner + "</a>";
        }
        return '<button class="is1s-rail-btn active" type="button" data-module="' + group.id + '" aria-label="' + name +
          '" aria-pressed="true" title="' + name + '">' + inner + "</button>";
      }).join("") +
    '</nav><div class="is1s-rail-bottom">' +
      '<button class="is1s-rail-btn" type="button" data-shell-action="context" title="' + esc(L("My book: coverage, alerts and REX agents","งานของฉัน: บริษัทที่ดูแล การแจ้งเตือน และ REX agents")) + '">' + icon("panel-right-open") +
        '<span class="is1s-rail-label">' + esc(L("My book","งานของฉัน")) + "</span></button>" +
    "</div>";

  var modulePanel = document.createElement("aside");
  modulePanel.className = "is1s-modules";
  modulePanel.setAttribute("aria-label",L("Dashboard pages","รายการหน้า"));

  function moduleMarkup() {
    return '<div class="is1s-module-head"><div><strong>Control Room</strong><span>IS1 Coverage Desk</span></div>' +
      '<button class="is1s-icon-btn" type="button" data-shell-action="collapse" title="' + esc(L("Collapse sidebar","ย่อ sidebar")) + '">' + icon("panel-left-close") + "</button></div>" +
      '<div class="is1s-module-scroll">' +
      GROUPS.map(function (group) {
        return '<section class="is1s-nav-section' + (selectedModuleId === group.id ? " is-selected" : "") +
          '" data-module-section="' + group.id + '" aria-label="' + esc(L(group.label[0],group.label[1])) +
          '"><div class="is1s-nav-label">' + esc(L(group.label[0],group.label[1])) + "</div>" +
          group.pages.map(function (page) {
            var active = !/^https?:/.test(page[0]) && page[0].replace(/\.html$/,"") === hereKey;
            var embedded = EMBEDDED_WORKSPACES[page[0]];
            var tag = embedded ? "button" : "a";
            var target = embedded ? ' type="button" data-shell-embed="' + esc(page[0]) + '"' : ' href="' + esc(href(page[0])) + '"';
            return '<' + tag + ' class="is1s-module-link' + (active ? " active" : "") + '"' + target +
              (active ? ' aria-current="page"' : "") + '>' +
              icon(page[3]) + '<span>' + esc(L(page[1],page[2])) + '</span>' +
              (page[4] ? '<span class="is1s-count" data-count="' + page[4] + '">—</span>' : "") +
              (embedded ? icon("panel-right-open","is1s-link-arrow") : "") + "</" + tag + ">";
          }).join("") + "</section>";
      }).join("") + '<div class="is1s-module-spacer" aria-hidden="true"></div></div><div class="is1s-module-foot"><span class="is1s-live-dot"></span><span data-shell-freshness>' +
      esc(L("Loading snapshot","กำลังโหลด snapshot")) + "</span></div>";
  }
  modulePanel.innerHTML = moduleMarkup();

  var topbar = document.createElement("header");
  topbar.className = "is1s-topbar";
  var pageTitle = pageInfo ? L(pageInfo.page[1],pageInfo.page[2]) : L("Control Room","Control Room");
  topbar.innerHTML =
    '<button class="is1s-icon-btn is1s-mobile-menu" type="button" data-shell-action="mobile-menu" title="' + esc(L("Open menu","เปิดเมนู")) + '">' + icon("menu") + "</button>" +
    '<div class="is1s-crumb"><strong>' + esc(pageTitle) + '</strong><span>/ IS1</span></div>' +
    '<form class="is1s-search" data-shell-search>' + icon("search") +
      '<input type="search" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="is1s-search-pop" autocomplete="off" spellcheck="false" placeholder="' +
        esc(L("Search ticker or company","ค้นหา ticker หรือชื่อบริษัท")) + '" aria-label="' + esc(L("Search ticker or company","ค้นหา ticker หรือชื่อบริษัท")) + '">' +
      '<span class="is1s-kbd">/</span>' +
      '<button type="submit" title="' + esc(L("Open company page","เปิดหน้าข้อมูลบริษัท")) + '">' + icon("arrow-right") + "</button>" +
      '<div class="is1s-search-pop" id="is1s-search-pop" hidden></div></form>' +
    '<select class="is1s-rm" aria-label="' + esc(L("Context RM","เลือก RM")) + '">' +
      RM_CHOICES.map(function (rm) { return '<option value="' + rm + '"' + (state.rm === rm ? " selected" : "") + '>' + esc(rmLabel(rm)) + "</option>"; }).join("") +
    '</select><div class="is1s-controls"></div>' +
    '<button class="is1s-icon-btn" type="button" data-shell-action="context" title="' + esc(L("My book: coverage, alerts and REX agents","งานของฉัน: บริษัทที่ดูแล การแจ้งเตือน และ REX agents")) + '">' + icon("panel-right-open") + "</button>";

  var pageHead = null;
  if (!isHome && PAGE_META[hereKey]) {
    var meta = PAGE_META[hereKey];
    pageHead = document.createElement("section");
    pageHead.className = "is1s-page-head";
    pageHead.style.setProperty("--page-accent",meta[3]);
    pageHead.innerHTML =
      '<span class="is1s-page-icon">' + icon(meta[4]) + '</span><div><span class="is1s-page-group">' + esc(L(meta[0],meta[0])) +
      '</span><h1>' + esc(pageTitle) + '</h1><p><span>' + esc(L(meta[1],meta[2])) + '</span></p></div>';
    var existingMeta = document.getElementById("meta");
    if (existingMeta) pageHead.querySelector("p").appendChild(existingMeta);
  }

  var contextPanel = document.createElement("aside");
  contextPanel.className = "is1s-context";
  contextPanel.setAttribute("aria-label",L("Analyst context","ข้อมูลประกอบ"));
  contextPanel.innerHTML =
    '<div class="is1s-context-head"><div><strong data-context-title>' + esc(rmLabel(state.rm)) + ' workspace</strong><span>' + esc(L("Context follows your selection","Context ตามสิ่งที่เลือก")) + '</span></div>' +
      '<button class="is1s-icon-btn" type="button" data-shell-action="close-context" title="' + esc(L("Close my book","ปิดงานของฉัน")) + '">' + icon("panel-right-close") + "</button></div>" +
    '<div class="is1s-context-tabs"><button class="active" type="button" data-context="coverage">' + esc(L("My book","My book")) + '</button>' +
      '<button type="button" data-context="alerts">Alerts</button><button type="button" data-context="agents">REX agents</button></div>' +
    '<div class="is1s-context-body"><div class="is1s-empty">' + esc(L("Loading coverage","กำลังโหลด coverage")) + "</div></div>";

  var scrim = document.createElement("div");
  scrim.className = "is1s-scrim";
  var workspaceScrim = document.createElement("div");
  workspaceScrim.className = "is1s-workspace-scrim";
  workspaceScrim.setAttribute("data-shell-workspace-close","");
  var workspace = document.createElement("section");
  workspace.className = "is1s-workspace";
  workspace.setAttribute("role","dialog");
  workspace.setAttribute("aria-modal","true");
  workspace.setAttribute("aria-hidden","true");
  workspace.setAttribute("aria-label",L("Embedded workspace","พื้นที่ทำงานด้านขวา"));
  workspace.innerHTML =
    '<header class="is1s-workspace-head"><div><strong data-workspace-title></strong><span data-workspace-description></span></div>' +
      '<div class="is1s-workspace-actions"><button class="is1s-icon-btn" type="button" data-shell-workspace-reload title="' +
        esc(L("Reload workspace","โหลดพื้นที่ทำงานใหม่")) + '">' + icon("activity") + '</button>' +
      '<button class="is1s-icon-btn" type="button" data-shell-workspace-close title="' + esc(L("Close workspace","ปิดพื้นที่ทำงาน")) + '">' +
        icon("panel-right-close") + '</button></div></header>' +
    '<div class="is1s-workspace-stage"><div class="is1s-workspace-loading"><span></span>' + esc(L("Loading workspace","กำลังโหลดพื้นที่ทำงาน")) +
      '</div><iframe title="' + esc(L("Embedded dashboard","Dashboard ที่ฝังในหน้านี้")) + '" loading="eager" referrerpolicy="strict-origin-when-cross-origin" ' +
      'sandbox="allow-forms allow-modals allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts allow-downloads"></iframe></div>';
  var insertPoint = legacyHeader || document.body.firstChild;
  document.body.insertBefore(topbar,insertPoint);
  if (pageHead) document.body.insertBefore(pageHead,insertPoint);
  document.body.appendChild(rail);
  document.body.appendChild(modulePanel);
  document.body.appendChild(contextPanel);
  document.body.appendChild(scrim);
  document.body.appendChild(workspaceScrim);
  document.body.appendChild(workspace);

  var staleNode = document.getElementById("staleBadge");
  if (staleNode) {
    staleNode.classList.add("is1s-status");
    topbar.querySelector(".is1s-controls").appendChild(staleNode);
    // Pages write this badge in their own formats (a bare ISO date, "exported
    // <timestamp>", "data as of ..."). Keep "updated Xh ago" as is and show any
    // raw date as one format; also restore the shell class when a page resets
    // className.
    var tidyStale = function () {
      if (!staleNode.classList.contains("is1s-status")) staleNode.classList.add("is1s-status");
      var text = staleNode.textContent || "";
      if (/ago|ที่แล้ว/.test(text) || staleNode.dataset.tidy === text) return;
      var match = text.match(/(\d{4}-\d{2}-\d{2})/);
      if (!match) return;
      var tidy = "● " + L("data as of ","ข้อมูล ณ ") + thaiDate(match[1]);
      staleNode.dataset.tidy = tidy;
      staleNode.textContent = tidy;
    };
    new MutationObserver(tidyStale).observe(staleNode,{ childList:true, characterData:true, subtree:true, attributes:true, attributeFilter:["class"] });
    tidyStale();
  }
  if (window.I18N && I18N.createToggle && !topbar.querySelector(".i18n-toggle")) {
    topbar.querySelector(".is1s-controls").appendChild(I18N.createToggle());
  }

  var savedCollapsed = localStorage.getItem("is1_shell_modules") === "collapsed";
  if (savedCollapsed) document.body.classList.add("is1s-modules-collapsed");
  var savedContext = localStorage.getItem("is1_shell_context");
  if (isHome && (savedContext === "open" || savedContext == null) && innerWidth > 1250) {
    document.body.classList.add("is1s-context-open");
  }

  function closeOverlays() {
    document.body.classList.remove("is1s-mobile-modules","is1s-mobile-context");
  }
  function closeWorkspace() {
    document.body.classList.remove("is1s-workspace-open");
    workspace.setAttribute("aria-hidden","true");
  }
  function openWorkspace(url) {
    var meta = EMBEDDED_WORKSPACES[url];
    if (!meta) return;
    closeOverlays();
    if (window.IS1Dock) window.IS1Dock.close();
    workspace.querySelector("[data-workspace-title]").textContent = L(meta.title[0],meta.title[1]);
    workspace.querySelector("[data-workspace-description]").textContent = L(meta.description[0],meta.description[1]);
    var frame = workspace.querySelector("iframe");
    var embeddedUrl = new URL(url);
    embeddedUrl.searchParams.set("embedded","1");
    embeddedUrl = embeddedUrl.toString();
    workspace.classList.add("loading");
    if (frame.dataset.src !== embeddedUrl) {
      frame.dataset.src = embeddedUrl;
      frame.src = embeddedUrl;
    }
    document.body.classList.add("is1s-workspace-open");
    workspace.removeAttribute("aria-hidden");
    workspace.querySelector("[data-shell-workspace-close]").focus();
  }
  workspace.querySelector("iframe").addEventListener("load",function () { workspace.classList.remove("loading"); });
  workspace.querySelector("[data-shell-workspace-reload]").addEventListener("click",function () {
    var frame = workspace.querySelector("iframe");
    if (!frame.dataset.src) return;
    workspace.classList.add("loading");
    frame.src = frame.dataset.src;
  });
  workspace.querySelector("[data-shell-workspace-close]").addEventListener("click",closeWorkspace);
  workspaceScrim.addEventListener("click",closeWorkspace);
  function toggleContext(open) {
    if (innerWidth <= 1250) {
      document.body.classList.toggle("is1s-mobile-context",open == null ? !document.body.classList.contains("is1s-mobile-context") : open);
      return;
    }
    var next = open == null ? !document.body.classList.contains("is1s-context-open") : open;
    document.body.classList.toggle("is1s-context-open",next);
    localStorage.setItem("is1_shell_context",next ? "open" : "closed");
  }
  function setModuleActive(id) {
    selectedModuleId = id;
    rail.querySelectorAll("[data-module]").forEach(function (button) {
      var active = button.dataset.module === id;
      button.classList.toggle("active",active);
      button.setAttribute("aria-pressed",active ? "true" : "false");
    });
    modulePanel.querySelectorAll("[data-module-section]").forEach(function (candidate) {
      candidate.classList.toggle("is-selected",candidate.dataset.moduleSection === id);
    });
    var section = modulePanel.querySelector('[data-module-section="' + id + '"]');
    var scroller = modulePanel.querySelector(".is1s-module-scroll");
    if (section && scroller) {
      var spacer = scroller.querySelector(".is1s-module-spacer");
      if (spacer) spacer.style.height = "0px";
      var target = section.getBoundingClientRect().top - scroller.getBoundingClientRect().top + scroller.scrollTop;
      var available = Math.max(0,scroller.scrollHeight - scroller.clientHeight);
      if (spacer && target > available) spacer.style.height = Math.ceil(target - available) + "px";
      var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      requestAnimationFrame(function () {
        scroller.scrollTo({ top:Math.max(0,target), behavior:reduceMotion ? "auto" : "smooth" });
      });
    }
    if (innerWidth <= 840) document.body.classList.add("is1s-mobile-modules");
    else document.body.classList.remove("is1s-modules-collapsed");
  }

  rail.querySelectorAll("button[data-module]").forEach(function (button) {
    button.addEventListener("click",function () { setModuleActive(button.dataset.module); });
  });
  modulePanel.querySelectorAll("[data-shell-embed]").forEach(function (button) {
    button.addEventListener("click",function () { openWorkspace(button.dataset.shellEmbed); });
  });
  document.querySelectorAll("[data-shell-action]").forEach(function (button) {
    button.addEventListener("click",function () {
      var action = button.dataset.shellAction;
      if (action === "context") toggleContext();
      if (action === "close-context") toggleContext(false);
      if (action === "mobile-menu") document.body.classList.add("is1s-mobile-modules");
      if (action === "collapse") {
        if (innerWidth <= 840) document.body.classList.remove("is1s-mobile-modules");
        else {
          var collapsed = document.body.classList.toggle("is1s-modules-collapsed");
          localStorage.setItem("is1_shell_modules",collapsed ? "collapsed" : "open");
        }
      }
    });
  });
  scrim.addEventListener("click",closeOverlays);
  document.addEventListener("keydown",function (event) {
    if (event.key === "Escape" && document.body.classList.contains("is1s-workspace-open")) closeWorkspace();
    else if (event.key === "Escape") closeOverlays();
    if (event.key === "/" && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)) {
      event.preventDefault();
      topbar.querySelector(".is1s-search input").focus();
    }
  });

  var rmSelect = topbar.querySelector(".is1s-rm");
  function dispatchRmChange() {
    window.dispatchEvent(new CustomEvent("is1:rm-change",{ detail:{ rm:state.rm } }));
  }
  rmSelect.addEventListener("change",function () {
    state.rm = rmSelect.value;
    state.selectedTicker = null;
    localStorage.setItem("is1_rm",state.rm);
    renderShellData();
    dispatchRmChange();
  });
  contextPanel.querySelectorAll("[data-context]").forEach(function (button) {
    button.addEventListener("click",function () {
      state.context = button.dataset.context;
      contextPanel.querySelectorAll("[data-context]").forEach(function (tab) { tab.classList.toggle("active",tab === button); });
      renderContext();
    });
  });

  function asset(name) { return href("data/" + name + ".json"); }
  var dataPromise = Promise.all([
    fetch(asset("tickers")).then(function (r) { if (!r.ok) throw new Error("tickers"); return r.json(); }),
    fetch(asset("morning-brief")).then(function (r) { if (!r.ok) throw new Error("morning-brief"); return r.json(); }),
    fetch(asset("unusual-trading")).then(function (r) { if (!r.ok) throw new Error("unusual-trading"); return r.json(); }),
    fetch(asset("disclosure-pulse")).then(function (r) { if (!r.ok) throw new Error("disclosure-pulse"); return r.json(); }),
    fetch(asset("external-news")).then(function (r) { if (!r.ok) throw new Error("external-news"); return r.json(); }),
  ]).then(function (items) {
    state.data = { tickers:items[0], brief:items[1], unusual:items[2], pulse:items[3], news:items[4] };
    state.data.tickerMap = new Map(state.data.tickers.tickers.map(function (ticker) { return [ticker.tk,ticker]; }));
    if (document.activeElement === searchInput && searchInput.value.trim()) renderSearch();
    var queryTicker = new URLSearchParams(location.search).get("tk");
    if (queryTicker && state.data.tickerMap.has(queryTicker.toUpperCase())) state.selectedTicker = queryTicker.toUpperCase();
    renderShellData();
  }).catch(function () {
    contextPanel.querySelector(".is1s-context-body").innerHTML = '<div class="is1s-empty">' + esc(L("Snapshot unavailable","โหลด snapshot ไม่สำเร็จ")) + "</div>";
  });

  // Ticker typeahead: matches ticker, English and Thai company name, and
  // previews the highlighted company (profile, valuation, alerts, latest
  // SET filings and external news) before the analyst leaves the page.
  // ticker-summary.json is ~1.7 MB, so it loads on first focus, not on boot.
  var searchForm = topbar.querySelector("[data-shell-search]");
  var searchInput = searchForm.querySelector("input");
  var searchPop = searchForm.querySelector(".is1s-search-pop");
  var search = { matches:[], active:0, summary:null, summaryPromise:null };

  function loadSummary() {
    if (!search.summaryPromise) {
      search.summaryPromise = fetch(asset("ticker-summary")).then(function (r) {
        if (!r.ok) throw new Error("ticker-summary");
        return r.json();
      }).then(function (json) {
        search.summary = new Map((json.tickers || []).map(function (row) { return [row.tk,row]; }));
        if (!searchPop.hidden) renderSearch();
      }).catch(function () { search.summary = new Map(); });
    }
    return search.summaryPromise;
  }
  function companyHref(tk,tab) {
    return href("company-summary.html?tk=" + encodeURIComponent(tk) + (tab ? "&tab=" + tab : ""));
  }
  function fmtNum(value,digits) {
    if (!finite(value)) return "n/a";
    return Number(value).toLocaleString("en-US",{ minimumFractionDigits:digits, maximumFractionDigits:digits });
  }
  function fmtMktcap(value) {
    return finite(value) ? fmtNum(Number(value) / 1e6,0) : "n/a";
  }
  function signClass(value) { return !finite(value) ? "" : Number(value) >= 0 ? "positive" : "negative"; }
  function companyName(tk) {
    var row = search.summary && search.summary.get(tk);
    if (!row) return "";
    return L(row.name || row.nameTh || "",row.nameTh || row.name || "");
  }
  function findMatches(query) {
    if (!state.data) return [];
    var q = query.trim().toUpperCase();
    if (!q) return [];
    var lower = query.trim().toLowerCase();
    var scored = [];
    state.data.tickers.tickers.forEach(function (ticker) {
      var score = -1;
      if (ticker.tk === q) score = 0;
      else if (ticker.tk.indexOf(q) === 0) score = 1;
      else if (ticker.tk.indexOf(q) > 0) score = 3;
      else if (lower.length >= 2 && search.summary) {
        var row = search.summary.get(ticker.tk);
        if (row && ((row.name || "").toLowerCase().indexOf(lower) >= 0 || (row.nameTh || "").indexOf(query.trim()) >= 0)) score = 4;
      }
      if (score < 0) return;
      // Within a tier, the selected RM's names come first.
      if (state.rm !== "ALL" && ticker.rm !== state.rm) score += 0.5;
      scored.push({ score:score, ticker:ticker });
    });
    return scored.sort(function (a,b) { return a.score - b.score || a.ticker.tk.localeCompare(b.ticker.tk); })
      .slice(0,8).map(function (item) { return item.ticker; });
  }
  function latestFeed(tk) {
    var filings = (state.data.pulse.filings || []).filter(function (f) { return f.tk === tk; }).map(function (f) {
      return { kind:"SET", ts:f.ts, severity:f.severity, title:L(f.title || f.title_th,f.title_th || f.title), url:safeHttpUrl(L(f.url || f.url_th,f.url_th || f.url)) };
    });
    var news = (state.data.news.items || []).filter(function (n) { return n.tk === tk; }).map(function (n) {
      return { kind:n.source || L("News","ข่าว"), ts:n.ts, severity:null, title:n.title, url:safeHttpUrl(n.url) };
    });
    return filings.concat(news).sort(function (a,b) { return String(b.ts || "").localeCompare(String(a.ts || "")); });
  }
  function previewMarkup(ticker) {
    var tk = ticker.tk;
    var row = search.summary ? search.summary.get(tk) : null;
    var quote = row || state.data.brief.rows.find(function (r) { return r.tk === tk; }) || {};
    var alerts = (state.data.unusual.alerts || []).filter(function (a) { return a.tk === tk; });
    var feed = latestFeed(tk);
    var name = companyName(tk);
    var business = row ? L(row.businessType || row.businessTypeTh,row.businessTypeTh || row.businessType) : "";
    var stat = function (label,value,cls) { return '<span>' + esc(label) + '<strong class="' + (cls || "") + '">' + esc(value) + "</strong></span>"; };
    return '<div class="is1s-sp-head"><div><h3>' + esc(tk) + '</h3><p>' + esc(canonicalSector(ticker.sector)) + " · RM " + esc(ticker.rm) +
        (row && row.fiscalYearEnd ? " · FYE " + esc(row.fiscalYearEnd) : "") + '</p></div>' +
        (alerts.length ? '<b class="is1s-sp-alert">' + severityDot(alerts[0].severity) + esc(alerts[0].label) + "</b>" : "") + "</div>" +
      (name ? '<p class="is1s-sp-name">' + esc(name) + "</p>" : (search.summary ? "" : '<p class="is1s-sp-name is1s-sp-loading">' + esc(L("Loading profile","กำลังโหลดข้อมูลบริษัท")) + "</p>")) +
      (business ? '<p class="is1s-sp-biz">' + esc(business) + "</p>" : "") +
      '<div class="is1s-sp-stats">' +
        stat(L("Last","ราคาล่าสุด"),fmtNum(quote.last,2)) +
        stat(L("1 day","1 วัน"),fmtPct(quote.pct1d,1),signClass(quote.pct1d)) +
        stat("YTD",fmtPct(quote.pctYtd,1),signClass(quote.pctYtd)) +
        stat("P/E",fmtNum(row && row.pe,2)) +
        stat("P/BV",fmtNum(row && row.pbv,2)) +
        stat(L("Mkt cap (THB mn)","มูลค่าตลาด (ล้านบาท)"),fmtMktcap(row && row.mktcap)) +
        (row && finite(row.lo52) && finite(row.hi52) ? stat(L("52-week range","ช่วง 52 สัปดาห์"),fmtNum(row.lo52,2) + " – " + fmtNum(row.hi52,2)) : "") +
        (row && finite(row.dy) ? stat(L("Div. yield","อัตราปันผล"),fmtNum(row.dy,2) + "%") : "") +
      "</div>" +
      '<div class="is1s-sp-feed"><div class="is1s-sp-label">' + esc(L("Latest filings and news","ข่าวและการเปิดเผยข้อมูลล่าสุด")) + "</div>" +
        (feed.slice(0,4).map(function (item) {
          var inner = (item.severity ? severityDot(item.severity) : '<span class="is1s-sp-src"></span>') +
            '<div><small>' + esc(item.kind) + " · " + esc(feedTime(item.ts)) + "</small><span>" + esc(item.title) + "</span></div>";
          return item.url ? '<a href="' + esc(item.url) + '" target="_blank" rel="noopener">' + inner + "</a>" : "<div>" + inner + "</div>";
        }).join("") || '<p class="is1s-empty">' + esc(L("No filings or news in the current snapshot window","ไม่มีข่าวในช่วงเวลาของ snapshot ปัจจุบัน")) + "</p>") +
      "</div>" +
      '<div class="is1s-sp-actions">' +
        '<a class="primary" href="' + esc(companyHref(tk)) + '">' + esc(L("Company page","หน้าข้อมูลบริษัท")) + icon("arrow-right") + "</a>" +
        '<a href="' + esc(companyHref(tk,"disclosures")) + '">' + esc(L("Disclosures","ข่าวเปิดเผยข้อมูล")) + "</a>" +
        '<a href="' + esc(href("one-page.html?tk=" + encodeURIComponent(tk))) + '">One-page</a>' +
        '<a href="https://www.set.or.th/' + L("en","th") + '/market/product/stock/quote/' + encodeURIComponent(tk) + '/factsheet" target="_blank" rel="noopener">SET factsheet' + icon("arrow-up-right") + "</a>" +
        '<button type="button" data-sp-context="' + esc(tk) + '">' + esc(L("My book","งานของฉัน")) + "</button>" +
      "</div>";
  }
  function closeSearch() {
    searchPop.hidden = true;
    searchInput.setAttribute("aria-expanded","false");
    searchInput.removeAttribute("aria-activedescendant");
  }
  function renderSearch() {
    var query = searchInput.value;
    if (!query.trim()) { closeSearch(); return; }
    if (!state.data) {
      searchPop.innerHTML = '<div class="is1s-empty">' + esc(L("Loading snapshot","กำลังโหลด snapshot")) + "</div>";
    } else {
      search.matches = findMatches(query);
      if (search.active >= search.matches.length) search.active = 0;
      if (!search.matches.length) {
        searchPop.innerHTML = '<div class="is1s-empty">' + esc(L("No ticker or company in IS1 coverage matches ","ไม่พบ ticker หรือบริษัทใน coverage ของ IS1 ที่ตรงกับ ")) + esc(query.trim()) + "</div>";
      } else {
        searchPop.innerHTML = '<ul class="is1s-sp-list" role="listbox">' + search.matches.map(function (ticker,index) {
          var name = companyName(ticker.tk);
          return '<li id="is1s-sp-opt-' + index + '" role="option" aria-selected="' + (index === search.active) + '" data-sp-index="' + index + '"' +
            (index === search.active ? ' class="active"' : "") + '><strong>' + esc(ticker.tk) + "</strong><small>" +
            esc(name || canonicalSector(ticker.sector)) + "</small><em>" + esc(canonicalSector(ticker.sector)) + " · " + esc(ticker.rm) + "</em></li>";
        }).join("") + '</ul><div class="is1s-sp-preview">' + previewMarkup(search.matches[search.active]) + "</div>";
        searchInput.setAttribute("aria-activedescendant","is1s-sp-opt-" + search.active);
      }
    }
    searchPop.hidden = false;
    searchInput.setAttribute("aria-expanded","true");
  }
  function openCompany(tk) {
    closeSearch();
    location.href = companyHref(tk);
  }

  searchInput.addEventListener("focus",function () {
    loadSummary();
    if (searchInput.value.trim()) renderSearch();
  });
  searchInput.addEventListener("input",function () {
    search.active = 0;
    loadSummary();
    renderSearch();
  });
  searchInput.addEventListener("keydown",function (event) {
    if (searchPop.hidden || !search.matches.length) {
      if (event.key === "Escape") { closeSearch(); searchInput.blur(); }
      return;
    }
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      var step = event.key === "ArrowDown" ? 1 : -1;
      search.active = (search.active + step + search.matches.length) % search.matches.length;
      renderSearch();
    } else if (event.key === "Escape") {
      event.stopPropagation();
      closeSearch();
    }
  });
  searchPop.addEventListener("mousedown",function (event) {
    // Keep focus in the input so blur does not close the popup mid-click.
    if (!event.target.closest("a")) event.preventDefault();
  });
  searchPop.addEventListener("mouseover",function (event) {
    var item = event.target.closest("[data-sp-index]");
    if (!item || Number(item.dataset.spIndex) === search.active) return;
    search.active = Number(item.dataset.spIndex);
    renderSearch();
  });
  searchPop.addEventListener("click",function (event) {
    var item = event.target.closest("[data-sp-index]");
    if (item) { openCompany(search.matches[Number(item.dataset.spIndex)].tk); return; }
    var ctx = event.target.closest("[data-sp-context]");
    if (ctx) {
      state.selectedTicker = ctx.dataset.spContext;
      state.context = "coverage";
      contextPanel.querySelectorAll("[data-context]").forEach(function (tab) { tab.classList.toggle("active",tab.dataset.context === "coverage"); });
      closeSearch();
      renderContext();
      toggleContext(true);
    }
  });
  document.addEventListener("mousedown",function (event) {
    if (!searchForm.contains(event.target)) closeSearch();
  });
  searchForm.addEventListener("submit",function (event) {
    event.preventDefault();
    if (!state.data) return;
    if (searchPop.hidden) renderSearch();
    var pick = search.matches[search.active];
    if (pick) openCompany(pick.tk);
  });

  function ownedSet() {
    return new Set(state.data.tickers.tickers.filter(function (ticker) { return state.rm === "ALL" || ticker.rm === state.rm; }).map(function (ticker) { return ticker.tk; }));
  }
  function rmRows() {
    var owned = ownedSet();
    return state.data.brief.rows.filter(function (row) { return owned.has(row.tk); });
  }
  function rmAlerts() {
    var owned = ownedSet();
    return state.data.unusual.alerts.filter(function (alert) { return owned.has(alert.tk); });
  }
  function rmFilings() {
    var owned = ownedSet();
    return state.data.pulse.filings.filter(function (filing) { return owned.has(filing.tk); });
  }
  function rmNews() {
    var owned = ownedSet();
    return state.data.news.items.filter(function (item) { return owned.has(item.tk); });
  }
  function movers(limit) {
    return rmRows().filter(function (row) { return finite(row.pct1d); })
      .sort(function (a,b) { return Math.abs(Number(b.pct1d)) - Math.abs(Number(a.pct1d)); }).slice(0,limit);
  }
  function sectorMetrics() {
    var grouped = new Map();
    state.data.brief.rows.forEach(function (row) {
      var sector = canonicalSector(row.sector);
      if (!grouped.has(sector)) grouped.set(sector,[]);
      grouped.get(sector).push(row);
    });
    return Array.from(grouped.entries()).map(function (entry) {
      var rows = entry[1];
      var oneDay = rows.map(function (row) { return row.pct1d; }).filter(finite).map(Number);
      return {
        sector:entry[0],
        count:rows.length,
        avg1d:average(oneDay),
        avg5d:average(rows.map(function (row) { return row.pct5d; })),
        avgYtd:average(rows.map(function (row) { return row.pctYtd; })),
        up:oneDay.filter(function (value) { return value > 0; }).length,
        valid:oneDay.length,
      };
    }).sort(function (a,b) { return (b.avg1d || 0) - (a.avg1d || 0); });
  }
  function thaiDate(value) {
    if (!value) return "?";
    return new Intl.DateTimeFormat(I18N && I18N.lang === "th" ? "th-TH" : "en-GB",{ day:"numeric",month:"short",year:"numeric",timeZone:"Asia/Bangkok" }).format(new Date(value + "T00:00:00+07:00"));
  }
  function feedTime(value) {
    if (!value) return "";
    var date = new Date(value);
    if (!Number.isFinite(date.getTime())) return "";
    return new Intl.DateTimeFormat(I18N && I18N.lang === "th" ? "th-TH" : "en-GB",{
      day:"numeric",month:"short",hour:"2-digit",minute:"2-digit",timeZone:"Asia/Bangkok",
    }).format(date);
  }
  function severityDot(value) { return '<span class="is1s-severity ' + (value === "high" || value === "critical" ? "high" : "medium") + '"></span>'; }

  function renderContext() {
    if (!state.data) return;
    var body = contextPanel.querySelector(".is1s-context-body");
    contextPanel.querySelector("[data-context-title]").textContent = state.selectedTicker ? state.selectedTicker + " context" : rmLabel(state.rm) + " workspace";
    if (state.context === "agents") {
      var agents = [
        ["H","Hermes","#d98e16",L("SET filings, external news and Oppday","ข่าว SET, external news และ Oppday"),"hermes"],
        ["A","Atlas","#3f7fdc",L("Movers, alerts and threshold checks","Movers, alerts และ threshold checks"),"atlas"],
        ["P","Pythia","#14899a",L("Sector performance and breadth","Sector performance และ breadth"),"pythia"],
        ["L","Lex","#238d60",L("Rules cited to PDF and page","กฎเกณฑ์พร้อม PDF และเลขหน้า"),"lex"],
      ];
      body.innerHTML = '<div class="is1s-context-summary"><strong>4</strong><span>' + esc(L("specialist agents","บอตเฉพาะทาง")) + "</span></div>" +
        agents.map(function (agent) {
          return '<button class="is1s-agent-row" type="button" data-agent="' + agent[4] + '"><span style="background:' + agent[2] + '">' + agent[0] +
            '</span><div><strong>' + agent[1] + '</strong><small>' + esc(agent[3]) + '</small></div>' + icon("arrow-up-right") + "</button>";
        }).join("");
      body.querySelectorAll("[data-agent]").forEach(function (button) {
        button.addEventListener("click",function () {
          if (window.IS1Dock) window.IS1Dock.open(button.dataset.agent);
        });
      });
      return;
    }
    if (state.context === "alerts") {
      var alerts = rmAlerts().slice(0,24);
      body.innerHTML = '<div class="is1s-context-summary"><strong>' + alerts.filter(function (alert) { return alert.severity === "high"; }).length +
        '</strong><span>' + esc(L("high-severity alerts","high-severity alerts")) + "</span></div>" +
        alerts.map(function (alert) {
          return '<button class="is1s-watch-row" type="button" data-ticker="' + esc(alert.tk) + '">' +
            severityDot(alert.severity) + '<div><strong>' + esc(alert.tk) + '</strong><small>' + esc(alert.type) + '</small></div><b>' + esc(alert.label) + "</b></button>";
        }).join("") || '<div class="is1s-empty">' + esc(L("No alerts","ไม่มี alert")) + "</div>";
    } else {
      var rows = movers(24);
      var selected = "";
      if (state.selectedTicker) {
        var quote = state.data.brief.rows.find(function (row) { return row.tk === state.selectedTicker; });
        var ticker = state.data.tickerMap.get(state.selectedTicker);
        if (quote && ticker) {
          selected = '<div class="is1s-selected"><h3>' + esc(quote.tk) + '</h3><p>' + esc(ticker.sector) + " · RM " + esc(ticker.rm) +
            '</p><div><span>Last<strong>' + esc(quote.last == null ? "n/a" : quote.last) + '</strong></span><span>1 day<strong class="' +
            (quote.pct1d >= 0 ? "positive" : "negative") + '">' + fmtPct(quote.pct1d) + '</strong></span><span>5 days<strong>' +
            fmtPct(quote.pct5d) + '</strong></span><span>YTD<strong>' + fmtPct(quote.pctYtd) + "</strong></span></div></div>";
        }
      }
      body.innerHTML = selected + '<div class="is1s-context-summary"><strong>' + rmRows().length + '</strong><span>' +
        esc(L("covered names sorted by movement","หลักทรัพย์เรียงตาม movement")) + "</span></div>" +
        rows.map(function (row) {
          return '<button class="is1s-watch-row" type="button" data-ticker="' + esc(row.tk) + '"><div><strong>' + esc(row.tk) +
            '</strong><small>' + esc(canonicalSector(row.sector)) + '</small></div><span class="is1s-mini-bar"><i style="width:' +
            Math.min(100,Math.max(4,Math.abs(Number(row.pct1d)) * 10)) + '%"></i></span><b class="' + (row.pct1d >= 0 ? "positive" : "negative") +
            '">' + fmtPct(row.pct1d) + "</b></button>";
        }).join("");
    }
    body.querySelectorAll("[data-ticker]").forEach(function (button) {
      button.addEventListener("click",function () {
        state.selectedTicker = button.dataset.ticker;
        state.context = "coverage";
        contextPanel.querySelectorAll("[data-context]").forEach(function (tab) { tab.classList.toggle("active",tab.dataset.context === "coverage"); });
        renderContext();
      });
    });
  }

  function renderCounts() {
    var counts = {
      filings:rmFilings().filter(function (filing) { return withinHours(filing.ts,24); }).length,
      news:rmNews().filter(function (item) { return withinHours(item.ts,24 * 7); }).length,
      alerts:rmAlerts().filter(function (alert) { return alert.severity === "high"; }).length,
    };
    modulePanel.querySelectorAll("[data-count]").forEach(function (node) { node.textContent = counts[node.dataset.count]; });
    var fresh = modulePanel.querySelector("[data-shell-freshness]");
    if (fresh) fresh.textContent = L("Prices as of ","ราคา ณ ") + thaiDate(state.data.brief.asOf);
  }

  function renderHome() {
    var host = document.querySelector(".is1-home-control");
    if (!host || !state.data) return;
    var rows = rmRows();
    var highAlerts = rmAlerts().filter(function (alert) { return alert.severity === "high"; });
    var todayFilings = rmFilings().filter(function (filing) { return withinHours(filing.ts,24); });
    var avg = average(rows.map(function (row) { return row.pct1d; }));
    host.querySelector("[data-home-date]").textContent = L("Prices as of ","ราคา ณ ") + thaiDate(state.data.brief.asOf);
    host.querySelector("[data-home-kpis]").innerHTML =
      '<div><span>' + esc(L("My coverage","My coverage")) + '</span><strong>' + rows.length + '</strong><small>' + esc(rmLabel(state.rm)) + "</small></div>" +
      '<div><span>High alerts</span><strong class="negative">' + highAlerts.length + '</strong><small>' + esc(L("review today","ต้องตรวจสอบวันนี้")) + "</small></div>" +
      '<div><span>' + esc(L("SET filings · 24h","SET filings · 24 ชม.")) + '</span><strong class="' + (todayFilings.length ? "gold" : "") + '">' + todayFilings.length + '</strong><small>' + esc(L("current coverage","ใน coverage ปัจจุบัน")) + "</small></div>" +
      '<div><span>Average 1-day move</span><strong class="' + (avg >= 0 ? "positive" : "negative") + '">' + fmtPct(avg) + '</strong><small>' +
      rows.filter(function (row) { return finite(row.pct1d) && Math.abs(Number(row.pct1d)) >= 2; }).length + " " + esc(L("names beyond ±2%","ตัวเกิน ±2%")) + "</small></div>";

    var metrics = sectorMetrics();
    var maxAbs = Math.max.apply(null,metrics.map(function (metric) { return Math.abs(metric.avg1d || 0); }).concat([1]));
    host.querySelector("[data-home-sectors]").innerHTML = metrics.map(function (metric,index) {
      return '<div class="is1-home-sector"><strong>' + esc(metric.sector) + '</strong><span><i style="--sector-width:' +
        Math.max(5,Math.abs(metric.avg1d || 0) / maxAbs * 100) + '%;--sector-color:' + (metric.avg1d >= 0 ? "var(--green)" : "var(--red)") +
        ';--sector-delay:' + index * 55 + 'ms"></i></span><b class="' + (metric.avg1d >= 0 ? "positive" : "negative") + '">' +
        fmtPct(metric.avg1d) + '</b><small>' + metric.up + "/" + metric.valid + "</small></div>";
    }).join("");

    host.querySelector("[data-home-movers]").innerHTML = movers(7).map(function (row) {
      return '<button type="button" data-home-ticker="' + esc(row.tk) + '"><span><strong>' + esc(row.tk) + '</strong><small>' +
        esc(canonicalSector(row.sector)) + '</small></span><b>' + esc(row.last == null ? "n/a" : row.last) + '</b><em class="' +
        (row.pct1d >= 0 ? "positive" : "negative") + '">' + fmtPct(row.pct1d) + "</em></button>";
    }).join("");

    var attention = highAlerts.slice(0,5).map(function (alert) {
      return { tk:alert.tk, severity:alert.severity, title:alert.type + " · " + alert.label, meta:canonicalSector(alert.sector) };
    });
    rmFilings().filter(function (filing) { return filing.severity === "critical" || filing.severity === "material"; }).slice(0,5).forEach(function (filing) {
      attention.push({ tk:filing.tk, severity:filing.severity, title:filing.title_th || filing.title, meta:"SET · " + canonicalSector(filing.sector) });
    });
    host.querySelector("[data-home-attention]").innerHTML = attention.slice(0,8).map(function (item) {
      return '<div>' + severityDot(item.severity) + '<strong>' + esc(item.tk) + '</strong><span>' + esc(item.title) + '</span><small>' + esc(item.meta) + "</small></div>";
    }).join("") || '<p class="is1s-empty">' + esc(L("No urgent items","ไม่มีรายการเร่งด่วน")) + "</p>";

    host.querySelector("[data-home-market-table]").innerHTML =
      '<table><thead><tr><th>Sector</th><th>1 day</th><th>5 days</th><th>YTD</th><th>Breadth</th></tr></thead><tbody>' +
      metrics.map(function (metric) {
        return "<tr><td><strong>" + esc(metric.sector) + "</strong><small>" + metric.count + "</small></td><td class='" +
          (metric.avg1d >= 0 ? "positive" : "negative") + "'>" + fmtPct(metric.avg1d) + "</td><td>" + fmtPct(metric.avg5d) +
          "</td><td>" + fmtPct(metric.avgYtd) + "</td><td>" + metric.up + "/" + metric.valid + "</td></tr>";
      }).join("") + "</tbody></table>";

    host.querySelector("[data-home-filing-list]").innerHTML = rmFilings().slice(0,12).map(function (filing) {
      var filingUrl = safeHttpUrl(filing.url_th || filing.url) || href("disclosure-pulse.html");
      return '<a href="' + esc(filingUrl) + '" target="_blank" rel="noopener">' + severityDot(filing.severity) + '<strong>' +
        esc(filing.tk) + '</strong><span>' + esc(filing.title_th || filing.title) + '<small>SET · ' + esc(canonicalSector(filing.sector)) + "</small></span></a>";
    }).join("") || '<p class="is1s-empty">' + esc(L("No filings","ไม่มี filing")) + "</p>";

    renderNewsDesk(host);

    host.querySelectorAll("[data-home-ticker]").forEach(function (button) {
      button.addEventListener("click",function () {
        state.selectedTicker = button.dataset.homeTicker;
        renderContext();
        toggleContext(true);
      });
    });
  }

  // Newsroom: disclosures outrank prices on the home page. One pool of SET
  // filings and external news for the selected RM, ranked by severity then
  // recency for the lead stories, and by time alone for the timeline.
  var NEWS_TYPES = {
    agm_resolution:["AGM resolution","มติประชุมผู้ถือหุ้น"],
    auditor_change:["Auditor change","เปลี่ยนผู้สอบบัญชี"],
    capital_change:["Capital change","เปลี่ยนแปลงทุน"],
    connected_transaction:["Connected transaction","รายการที่เกี่ยวโยงกัน"],
    director_mgmt_change:["Board / management change","เปลี่ยนแปลงกรรมการและผู้บริหาร"],
    dividend:["Dividend","เงินปันผล"],
    earnings:["Earnings","ผลประกอบการ"],
    guidance_change:["Guidance change","เปลี่ยนแปลงประมาณการ"],
    information_memo:["Information memo","สารสนเทศ"],
    ma_acquisition_disposal:["Acquisition / disposal","การได้มาหรือจำหน่ายไปซึ่งสินทรัพย์"],
    other:["Other","อื่น ๆ"],
    regulatory_filing:["Regulatory filing","รายงานตามเกณฑ์"],
    set_clarification:["SET clarification","ชี้แจงตามที่ตลาดหลักทรัพย์สอบถาม"],
    trading_sign:["Trading sign","เครื่องหมายการซื้อขาย"],
    warrant_exercise:["Warrant exercise","การใช้สิทธิใบสำคัญแสดงสิทธิ"],
  };
  function newsType(code) { var m = NEWS_TYPES[code]; return m ? L(m[0],m[1]) : (code || ""); }
  function severityRank(value) { return value === "critical" || value === "high" ? 3 : value === "material" || value === "medium" ? 2 : 1; }
  function relTime(ts) {
    var t = Date.parse(ts);
    if (!Number.isFinite(t)) return "";
    var mins = Math.max(0,Math.round((Date.now() - t) / 60000));
    if (mins < 60) return L(mins + "m ago",mins + " นาทีที่แล้ว");
    var hours = Math.round(mins / 60);
    if (hours < 24) return L(hours + "h ago",hours + " ชม. ที่แล้ว");
    var days = Math.round(hours / 24);
    return days < 8 ? L(days + "d ago",days + " วันที่แล้ว") : feedTime(ts);
  }
  function newsPool() {
    var filings = rmFilings().map(function (f) {
      return { kind:"set", id:String(f._id || ""), tk:f.tk, ts:f.ts, severity:f.severity, rank:severityRank(f.severity), type:newsType(f.type), sector:canonicalSector(f.sector),
        title:L(f.title || f.title_th,f.title_th || f.title), summary:L(f._summary || f._summary_th,f._summary_th || f._summary) || "",
        url:safeHttpUrl(L(f.url || f.url_th,f.url_th || f.url)) || href("disclosure-pulse.html"), source:"SET" };
    });
    var news = rmNews().map(function (n) {
      return { kind:"ext", tk:n.tk, ts:n.ts, severity:null, rank:1, type:n.source || L("External","ภายนอก"), sector:canonicalSector(n.sector),
        title:n.title || "", summary:n.excerpt || "", url:safeHttpUrl(n.url) || href("external-news.html"), source:n.source || L("External","ภายนอก") };
    });
    return filings.concat(news).sort(function (a,b) { return String(b.ts || "").localeCompare(String(a.ts || "")); });
  }
  function storyTone(item) { return item.kind === "ext" ? "ext" : item.rank === 3 ? "high" : item.rank === 2 ? "mid" : "low"; }
  function storyChip(item) {
    return '<a class="is1-news-tk" href="' + esc(href("company-summary.html?tk=" + encodeURIComponent(item.tk))) + '">' + esc(item.tk) + "</a>";
  }
  function storyMeta(item) {
    return '<span class="is1-news-kind ' + storyTone(item) + '">' + esc(item.kind === "set" ? "SET · " + item.type : item.source) + "</span>" +
      '<time datetime="' + esc(item.ts || "") + '" title="' + esc(feedTime(item.ts)) + '">' + esc(relTime(item.ts)) + "</time>";
  }
  // AI summaries of the filing PDFs (scripts/enrich_filing.py --dashboard).
  // Loaded only on the home page and only once; the desk re-renders on arrival.
  function aiSummary(item) {
    var map = search.aiSums;
    var entry = item && item.kind === "set" && map ? map[item.id] : null;
    return entry && entry.bullets && entry.bullets.length ? entry : null;
  }
  function aiSummaryHtml(entry) {
    return '<div class="is1-ai-sum"><div class="is1-ai-sum-head">✦ ' + esc(L("Summary of the filing PDF · MiniMax M3","สรุปจากเอกสารแนบ · MiniMax M3")) +
      "<span>· " + esc(L("numbers checked against the document","ตัวเลขตรวจกับต้นฉบับแล้ว")) + "</span></div><ul>" +
      entry.bullets.map(function (b) { return "<li>" + esc(b) + "</li>"; }).join("") + "</ul></div>";
  }
  function loadAiSummaries(host) {
    if (search.aiSumsPromise) return;
    search.aiSumsPromise = fetch(asset("filing-summaries")).then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        search.aiSums = (d && d.summaries) || {};
        if (state.data && Object.keys(search.aiSums).length) renderNewsDesk(host);
      }).catch(function () { search.aiSums = {}; });
  }
  function renderNewsDesk(host) {
    loadAiSummaries(host);
    var pool = newsPool();
    var fresh = pool.filter(function (item) { return withinHours(item.ts,24 * 7); });
    var ranked = (fresh.length >= 3 ? fresh : pool).slice().sort(function (a,b) {
      return b.rank - a.rank || String(b.ts || "").localeCompare(String(a.ts || ""));
    });
    var lead = ranked[0];
    var seconds = ranked.slice(1,3);
    var leadNode = host.querySelector("[data-home-lead]");
    if (!leadNode) return;
    host.querySelector("[data-home-news-rm]").textContent = rmLabel(state.rm);
    var set24 = pool.filter(function (item) { return item.kind === "set" && withinHours(item.ts,24); }).length;
    var key7 = fresh.filter(function (item) { return item.rank >= 2; }).length;
    var ext7 = fresh.filter(function (item) { return item.kind === "ext"; }).length;
    host.querySelector("[data-home-news-stats]").innerHTML =
      '<div><strong>' + set24 + '</strong><span>' + esc(L("SET filings · 24h","ข่าว SET · 24 ชม.")) + '</span></div>' +
      '<div class="gold"><strong>' + key7 + '</strong><span>' + esc(L("material · 7 days","ข่าวสำคัญ · 7 วัน")) + '</span></div>' +
      '<div><strong>' + ext7 + '</strong><span>' + esc(L("external · 7 days","ข่าวภายนอก · 7 วัน")) + '</span></div>';

    leadNode.className = "is1-news-lead" + (lead ? " tone-" + storyTone(lead) : "");
    leadNode.innerHTML = lead
      ? '<div class="is1-news-lead-top"><span class="is1-news-flag">' + esc(lead.rank === 3 ? L("Top priority","สำคัญที่สุด") : L("Lead story","ข่าวเด่น")) + "</span>" + storyMeta(lead) + "</div>" +
        '<div class="is1-news-lead-body">' + storyChip(lead) + '<div><h3><a href="' + esc(lead.url) + '" target="_blank" rel="noopener">' + esc(lead.title) + "</a></h3>" +
        (aiSummary(lead) ? aiSummaryHtml(aiSummary(lead)) : lead.summary && lead.summary !== lead.title ? "<p>" + esc(lead.summary) + "</p>" : "") + "</div></div>" +
        '<div class="is1-news-lead-foot"><span>' + esc(lead.sector) + " · " + esc(feedTime(lead.ts)) + '</span><a href="' + esc(lead.url) + '" target="_blank" rel="noopener">' +
        esc(lead.kind === "set" ? L("Read on SET","อ่านต่อที่ SET") : L("Read source","อ่านต้นฉบับ")) + icon("arrow-up-right") + "</a></div>"
      : '<p class="is1s-empty">' + esc(L("No news for this RM in the current snapshot","ยังไม่มีข่าวของ RM นี้ใน snapshot ปัจจุบัน")) + "</p>";

    host.querySelector("[data-home-seconds]").innerHTML = seconds.map(function (item,i) {
      return '<a class="is1-news-card tone-' + storyTone(item) + '" style="--news-delay:' + (120 + i * 70) + 'ms" href="' + esc(item.url) + '" target="_blank" rel="noopener">' +
        '<div class="is1-news-card-top"><b>' + esc(item.tk) + '</b><time title="' + esc(feedTime(item.ts)) + '">' + esc(relTime(item.ts)) + "</time></div>" +
        '<span class="is1-news-kind ' + storyTone(item) + '">' + esc(item.kind === "set" ? "SET · " + item.type : item.source) + "</span><h4>" + esc(item.title) + "</h4>" +
        (aiSummary(item) ? '<p class="is1-news-ai">✦ ' + esc(aiSummary(item).bullets[0]) + "</p>" :
          item.summary && item.summary !== item.title ? "<p>" + esc(item.summary) + "</p>" : "") + "</a>";
    }).join("");

    var filter = state.newsFilter || "all";
    var tests = {
      all:function () { return true; },
      key:function (item) { return item.rank >= 2; },
      set:function (item) { return item.kind === "set"; },
      ext:function (item) { return item.kind === "ext"; },
    };
    var shown = pool.filter(tests[filter]).slice(0,12);
    var lastDay = "";
    host.querySelector("[data-home-timeline]").innerHTML = shown.map(function (item,i) {
      var day = feedTime(item.ts).replace(/,?\s*\d{1,2}:\d{2}.*$/,"");
      var divider = day && day !== lastDay ? '<div class="is1-news-day">' + esc(day) + "</div>" : "";
      lastDay = day || lastDay;
      var clock = (feedTime(item.ts).match(/\d{1,2}:\d{2}/) || [""])[0];
      return divider + '<a class="is1-news-row tone-' + storyTone(item) + '" style="--news-delay:' + Math.min(i,8) * 35 + 'ms" href="' + esc(item.url) +
        '" target="_blank" rel="noopener" data-home-feed="' + (item.kind === "set" ? "disclosure" : "external") + '" data-home-feed-ticker="' + esc(item.tk) + '">' +
        '<time>' + esc(clock) + '</time><i></i><div><div class="is1-news-row-meta"><b>' + esc(item.tk) + "</b><span>" +
        esc(item.kind === "set" ? item.type : item.source) + "</span></div><p>" + esc(item.title) + "</p></div></a>";
    }).join("") || '<p class="is1s-empty">' + esc(L("Nothing in this filter","ไม่มีข่าวในตัวกรองนี้")) + "</p>";
  }

  function renderShellData() {
    if (!state.data) return;
    renderCounts();
    renderContext();
    renderHome();
  }

  function buildHome() {
    if (!isHome) return;
    var main = document.querySelector("main");
    if (!main || main.querySelector(".is1-home-control")) return;
    document.body.classList.add("is1s-home");
    var oldBlocks = [main.querySelector(".today-bar"),main.querySelector("#aiTake"),main.querySelector("#moverChips"),main.querySelector("#actionChips"),main.querySelector(".agent-strip")];
    oldBlocks.forEach(function (node) { if (node) node.classList.add("is1s-home-legacy"); });
    var agentStrip = main.querySelector(".agent-strip");
    if (agentStrip && agentStrip.previousElementSibling) agentStrip.previousElementSibling.classList.add("is1s-home-legacy");
    var control = document.createElement("section");
    control.className = "is1-home-control";
    control.innerHTML =
      '<div class="is1-home-head"><div><span>' + esc(L("Daily command center","Daily command center")) + '</span><h1>' +
      esc(L("What matters before the day starts","สิ่งที่ต้องรู้ก่อนเริ่มวัน")) + '</h1><p>' +
      esc(L("Market pulse, urgent work and RM coverage in one workspace","ภาพรวมตลาด งานเร่งด่วน และ coverage ของ RM ในหน้าจอเดียว")) +
      '</p></div><b data-home-date>' + esc(L("Loading snapshot","กำลังโหลด snapshot")) + '</b></div>' +
      '<div class="is1-home-tabs"><button class="active" type="button" data-home-view="overview">' + esc(L("Overview","ภาพรวม")) +
      '</button><button type="button" data-home-view="market">Market pulse</button><button type="button" data-home-view="filings">Filing flow</button></div>' +
      '<div class="is1-home-view active" data-home-panel="overview"><div class="is1-home-kpis" data-home-kpis></div>' +
        '<div class="is1-home-grid"><section class="is1-home-panel"><header><div><strong>Sector pulse</strong><span>Equal-weight return · market breadth</span></div>' +
        '<button type="button" data-home-jump="market">' + esc(L("Details","รายละเอียด")) + '</button></header><div class="is1-home-sectors" data-home-sectors></div></section>' +
        '<section class="is1-home-panel"><header><div><strong>' + esc(L("Top movers in coverage","Top movers ใน coverage")) +
        '</strong><span>Previous close · RM context</span></div><a href="price-movement.html">' + esc(L("Full page","หน้าเต็ม")) +
        '</a></header><div class="is1-home-movers" data-home-movers></div></section>' +
        '<section class="is1-home-panel wide"><header><div><strong>Attention queue</strong><span>' +
        esc(L("High-severity alerts and material filings","High-severity alerts และ material filings")) +
        '</span></div><a href="unusual-trading.html">' + esc(L("Review all","ตรวจทั้งหมด")) + '</a></header><div class="is1-home-attention" data-home-attention></div></section></div></div>' +
      '<div class="is1-home-view" data-home-panel="market"><section class="is1-home-panel"><header><div><strong>All-sector leaderboard</strong>' +
        '<span>1 day · 5 days · YTD · breadth</span></div><a href="price-movement.html">Price movement</a></header><div class="is1-home-table" data-home-market-table></div></section></div>' +
      '<div class="is1-home-view" data-home-panel="filings"><section class="is1-home-panel"><header><div><strong>Latest SET disclosures</strong>' +
        '<span>Newest first · current RM</span></div><a href="disclosure-pulse.html">Disclosure pulse</a></header><div class="is1-home-filings" data-home-filing-list></div></section></div>';
    var desk = document.createElement("section");
    desk.className = "is1-home-news";
    desk.innerHTML =
      '<header class="is1-home-news-head"><div><span><i class="is1-live-pulse"></i>' + esc(L("Newsroom","ห้องข่าว")) + ' · <b data-home-news-rm>' + esc(rmLabel(state.rm)) +
      '</b></span><p>' +
      esc(L("SET disclosures and external news for your coverage, ranked by importance","ข่าวเปิดเผยข้อมูล SET และข่าวภายนอกของหลักทรัพย์ที่ดูแล เรียงตามความสำคัญ")) + '</p></div>' +
      '<div class="is1-news-stats" data-home-news-stats></div></header>' +
      '<div class="is1-news-grid"><div class="is1-news-main"><article class="is1-news-lead" data-home-lead></article>' +
      '<div class="is1-news-seconds" data-home-seconds></div></div>' +
      '<aside class="is1-news-rail"><div class="is1-news-rail-head"><strong>' + esc(L("Latest timeline","ไทม์ไลน์ล่าสุด")) + '</strong>' +
      '<div class="is1-news-chips" role="tablist">' +
        [["all",L("All","ทั้งหมด")],["key",L("Material","สำคัญ")],["set","SET"],["ext",L("External","ข่าวภายนอก")]].map(function (chip,i) {
          return '<button type="button" role="tab" data-news-filter="' + chip[0] + '"' + (i ? "" : ' class="active" aria-selected="true"') + '>' + esc(chip[1]) + '</button>';
        }).join("") +
      '</div></div><div class="is1-news-timeline" data-home-timeline></div>' +
      '<footer><a href="disclosure-pulse.html">' + esc(L("All SET disclosures","ข่าว SET ทั้งหมด")) + icon("arrow-right") + '</a><a href="external-news.html">' +
      esc(L("All external news","ข่าวภายนอกทั้งหมด")) + icon("arrow-right") + '</a></footer></aside></div>';
    control.insertBefore(desk,control.querySelector(".is1-home-tabs"));
    desk.querySelectorAll("[data-news-filter]").forEach(function (button) {
      button.addEventListener("click",function () {
        state.newsFilter = button.dataset.newsFilter;
        desk.querySelectorAll("[data-news-filter]").forEach(function (chip) {
          var on = chip === button;
          chip.classList.toggle("active",on);
          chip.setAttribute("aria-selected",on ? "true" : "false");
        });
        renderNewsDesk(control);
      });
    });
    main.insertBefore(control,main.firstChild);
    control.querySelectorAll("[data-home-view]").forEach(function (button) {
      button.addEventListener("click",function () {
        control.querySelectorAll("[data-home-view]").forEach(function (tab) { tab.classList.toggle("active",tab === button); });
        control.querySelectorAll("[data-home-panel]").forEach(function (panel) { panel.classList.toggle("active",panel.dataset.homePanel === button.dataset.homeView); });
      });
    });
    control.querySelectorAll("[data-home-jump]").forEach(function (button) {
      button.addEventListener("click",function () {
        var tab = control.querySelector('[data-home-view="' + button.dataset.homeJump + '"]');
        if (tab) tab.click();
      });
    });
  }

  buildHome();

  function rerenderLanguage() {
    modulePanel.innerHTML = moduleMarkup();
    location.reload();
  }
  window.addEventListener("i18n:change",rerenderLanguage,{ once:true });
  window.IS1Shell = {
    openContext:function (ticker) {
      if (ticker) state.selectedTicker = String(ticker).toUpperCase();
      if (state.data) renderContext();
      toggleContext(true);
    },
    setRm:function (rm) {
      if (RM_CHOICES.indexOf(rm) < 0) return;
      state.rm = rm;
      rmSelect.value = rm;
      localStorage.setItem("is1_rm",rm);
      renderShellData();
      dispatchRmChange();
    },
    openWorkspace:openWorkspace,
    closeWorkspace:closeWorkspace,
  };
  setTimeout(dispatchRmChange,0);
})();
