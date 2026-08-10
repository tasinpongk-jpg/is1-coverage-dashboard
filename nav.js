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
      id:"home", label:["Workspace","พื้นที่ทำงาน"], icon:"layout-dashboard", color:"#f2aa1f",
      pages:[
        ["index.html","Morning overview","ภาพรวมเช้า","activity"],
        ["visits.html","Visit planner","แผนเยี่ยมบริษัท","calendar-days"],
        ["ai-insights.html","AI insights","AI insights","sparkles"],
      ],
    },
    {
      id:"market", label:["Market","ตลาด"], icon:"chart-no-axes-combined", color:"#5d96ff",
      pages:[
        ["price-movement.html","Price movement","ความเคลื่อนไหวราคา","trending-up"],
        ["sector-intelligence.html","Sector intelligence","บทวิเคราะห์รายกลุ่ม","chart-no-axes-combined"],
        ["multiples-comparison.html","Multiples comparison","เปรียบเทียบ multiples","columns-3"],
        ["multiples-band.html","Multiples band","ช่วง multiples","chart-spline"],
        ["https://tradingview-daily-dashboard.tasinpong-k.workers.dev/","Daily market board","กระดานตลาดรายวัน","monitor-up"],
      ],
    },
    {
      id:"companies", label:["Companies","บริษัท"], icon:"building-2", color:"#35bdd0",
      pages:[
        ["company-summary.html","Company summary","ข้อมูลรายบริษัท","notebook-tabs"],
        ["oppday-minutes.html","Oppday minutes","สรุป Oppday","presentation"],
        ["sec-form59.html","SEC Form 59","แบบ 59","contact-round"],
      ],
    },
    {
      id:"news", label:["News flow","ข่าวสาร"], icon:"newspaper", color:"#31c77b",
      pages:[
        ["disclosure-pulse.html","SET disclosures","ข่าวเปิดเผยข้อมูล","radio-tower","filings"],
        ["external-news.html","External news","ข่าวภายนอก","rss","news"],
        ["efinance-news.html","eFinanceThai live","ข่าว eFinanceThai","newspaper"],
        ["https://macro-brief-buy.pages.dev","Global-macro brief","สรุปมหภาคโลก","globe-2"],
      ],
    },
    {
      id:"surveillance", label:["Surveillance","เฝ้าระวัง"], icon:"shield-alert", color:"#ef6464",
      pages:[
        ["unusual-trading.html","Unusual trading","การซื้อขายผิดปกติ","siren","alerts"],
        ["trading-signs.html","Trading signs","เครื่องหมายซื้อขาย","flag"],
        ["sec-enforcement.html","SEC enforcement","การบังคับใช้กฎหมาย","shield-check"],
      ],
    },
    {
      id:"bonds", label:["Bond data","ข้อมูลหุ้นกู้"], icon:"landmark", color:"#b17cff",
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
    "disclosure-pulse":    ["News flow","Live SET filings ranked by importance","ข่าว SET ล่าสุดเรียงตามความสำคัญ","#31c77b","radio-tower"],
    "external-news":       ["News flow","Ticker-matched external headlines","ข่าวภายนอกที่จับคู่กับ ticker","#31c77b","rss"],
    "efinance-news":       ["News flow","Live headlines from eFinanceThai","พาดหัวข่าวล่าสุดจาก eFinanceThai","#31c77b","newspaper"],
    "oppday-minutes":      ["Companies","Earnings-call notes and takeaways","สรุปประเด็นจาก Oppday","#35bdd0","presentation"],
    "ai-insights":         ["Workspace","Validated commentary from daily snapshots","บทวิเคราะห์จาก daily snapshots","#f2aa1f","sparkles"],
    "unusual-trading":     ["Surveillance","Volume and price anomalies","ความผิดปกติด้านราคาและปริมาณซื้อขาย","#ef6464","siren"],
    "trading-signs":       ["Surveillance","Current SET trading signs","เครื่องหมายซื้อขายของ SET","#ef6464","flag"],
    "sec-enforcement":     ["Surveillance","Thai SEC enforcement actions","การบังคับใช้กฎหมายของ SEC","#ef6464","shield-check"],
    "sec-form59":          ["Companies","Management and related-person trades","รายการซื้อขายของผู้บริหารและบุคคลที่เกี่ยวข้อง","#35bdd0","contact-round"],
    "bond-summary":        ["Bond data","Outstanding bonds across coverage","หุ้นกู้คงค้างใน coverage","#b17cff","chart-pie"],
    "bond-data-sec":       ["Bond data","Bond filings from the SEC","ข้อมูล filing หุ้นกู้จาก SEC","#b17cff","database"],
    "visits":              ["Workspace","Plan and track company visits","วางแผนและติดตามการเยี่ยมบริษัท","#f2aa1f","calendar-days"],
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
    "shield-alert":'<path d="M20 13c0 5-3.5 7.5-7.7 9a1 1 0 0 1-.6 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.2-2.7a1.2 1.2 0 0 1 1.6 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/><path d="M12 8v4M12 16h.01"/>',
    "shield-check":'<path d="M20 13c0 5-3.5 7.5-7.7 9a1 1 0 0 1-.6 0C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.2-2.7a1.2 1.2 0 0 1 1.6 0C14.5 3.8 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "siren":'<path d="M7 18v-6a5 5 0 0 1 10 0v6M5 22h14M5 18h14M12 2v3M4.9 4.9 7 7M19.1 4.9 17 7"/>',
    "sparkles":'<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/><path d="M5 3v4M3 5h4M19 17v4M17 19h4"/>',
    "trending-up":'<path d="m3 17 6-6 4 4 8-8"/><path d="M14 7h7v7"/>',
  };

  var RMS = ["C","K","O","G","P","T"];
  var state = {
    rm:localStorage.getItem("is1_rm") || "C",
    context:"coverage",
    selectedTicker:null,
    data:null,
  };
  if (RMS.indexOf(state.rm) < 0) state.rm = "C";

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
        return '<button class="is1s-rail-btn' + (active ? " active" : "") +
          '" type="button" data-module="' + group.id + '" aria-label="' + esc(L(group.label[0],group.label[1])) +
          '" aria-pressed="' + (active ? "true" : "false") + '" title="' + esc(L(group.label[0],group.label[1])) + '">' + icon(group.icon) + "</button>";
      }).join("") +
    '</nav><div class="is1s-rail-bottom">' +
      '<button class="is1s-rail-btn" type="button" data-shell-action="context" title="' + esc(L("Open context","เปิด context")) + '">' + icon("panel-right-open") + "</button>" +
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
      '<input list="is1s-ticker-list" autocomplete="off" placeholder="' + esc(L("Search ticker","ค้นหา ticker")) + '" aria-label="' + esc(L("Search ticker","ค้นหา ticker")) + '">' +
      '<datalist id="is1s-ticker-list"></datalist><span class="is1s-kbd">/</span>' +
      '<button type="submit" title="' + esc(L("Open ticker","เปิดข้อมูล ticker")) + '">' + icon("arrow-right") + "</button></form>" +
    '<select class="is1s-rm" aria-label="' + esc(L("Context RM","เลือก RM")) + '">' +
      RMS.map(function (rm) { return '<option value="' + rm + '"' + (state.rm === rm ? " selected" : "") + '>RM ' + rm + "</option>"; }).join("") +
    '</select><div class="is1s-controls"></div>' +
    '<button class="is1s-icon-btn" type="button" data-shell-action="context" title="' + esc(L("Open context","เปิด context panel")) + '">' + icon("panel-right-open") + "</button>";

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
    '<div class="is1s-context-head"><div><strong data-context-title>RM ' + state.rm + ' workspace</strong><span>' + esc(L("Context follows your selection","Context ตามสิ่งที่เลือก")) + '</span></div>' +
      '<button class="is1s-icon-btn" type="button" data-shell-action="close-context" title="' + esc(L("Close context","ปิด context panel")) + '">' + icon("panel-right-close") + "</button></div>" +
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

  rail.querySelectorAll("[data-module]").forEach(function (button) {
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
  topbar.querySelector("[data-shell-search]").addEventListener("submit",function (event) {
    event.preventDefault();
    var value = event.currentTarget.querySelector("input").value.trim().toUpperCase();
    if (!value || !state.data || !state.data.tickerMap.has(value)) return;
    state.selectedTicker = value;
    state.context = "coverage";
    contextPanel.querySelectorAll("[data-context]").forEach(function (tab) { tab.classList.toggle("active",tab.dataset.context === "coverage"); });
    renderContext();
    toggleContext(true);
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
    topbar.querySelector("#is1s-ticker-list").innerHTML = state.data.tickers.tickers.map(function (ticker) {
      return '<option value="' + esc(ticker.tk) + '">' + esc(ticker.sector) + " · RM " + esc(ticker.rm) + "</option>";
    }).join("");
    var queryTicker = new URLSearchParams(location.search).get("tk");
    if (queryTicker && state.data.tickerMap.has(queryTicker.toUpperCase())) state.selectedTicker = queryTicker.toUpperCase();
    renderShellData();
  }).catch(function () {
    contextPanel.querySelector(".is1s-context-body").innerHTML = '<div class="is1s-empty">' + esc(L("Snapshot unavailable","โหลด snapshot ไม่สำเร็จ")) + "</div>";
  });

  function ownedSet() {
    return new Set(state.data.tickers.tickers.filter(function (ticker) { return ticker.rm === state.rm; }).map(function (ticker) { return ticker.tk; }));
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
    return new Intl.DateTimeFormat(I18N && I18N.lang === "th" ? "th-TH" : "en-GB",{ day:"numeric",month:"short",year:"numeric" }).format(new Date(value + "T00:00:00+07:00"));
  }
  function feedTime(value) {
    if (!value) return "";
    var date = new Date(value);
    if (!Number.isFinite(date.getTime())) return "";
    return new Intl.DateTimeFormat(I18N && I18N.lang === "th" ? "th-TH" : "en-GB",{
      day:"numeric",month:"short",hour:"2-digit",minute:"2-digit",
    }).format(date);
  }
  function severityDot(value) { return '<span class="is1s-severity ' + (value === "high" || value === "critical" ? "high" : "medium") + '"></span>'; }

  function renderContext() {
    if (!state.data) return;
    var body = contextPanel.querySelector(".is1s-context-body");
    contextPanel.querySelector("[data-context-title]").textContent = state.selectedTicker ? state.selectedTicker + " context" : "RM " + state.rm + " workspace";
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
      filings:rmFilings().filter(function (filing) { return String(filing.ts).slice(0,10) === state.data.brief.asOf; }).length,
      news:rmNews().filter(function (item) { return String(item.ts).slice(0,10) === state.data.brief.asOf; }).length,
      alerts:rmAlerts().filter(function (alert) { return alert.severity === "high"; }).length,
    };
    modulePanel.querySelectorAll("[data-count]").forEach(function (node) { node.textContent = counts[node.dataset.count]; });
    var fresh = modulePanel.querySelector("[data-shell-freshness]");
    if (fresh) fresh.textContent = L("Snapshot ","Snapshot ") + thaiDate(state.data.brief.asOf);
  }

  function renderHome() {
    var host = document.querySelector(".is1-home-control");
    if (!host || !state.data) return;
    var rows = rmRows();
    var highAlerts = rmAlerts().filter(function (alert) { return alert.severity === "high"; });
    var todayFilings = rmFilings().filter(function (filing) { return String(filing.ts).slice(0,10) === state.data.brief.asOf; });
    var avg = average(rows.map(function (row) { return row.pct1d; }));
    host.querySelector("[data-home-date]").textContent = L("Data as of ","ข้อมูล ณ ") + thaiDate(state.data.brief.asOf);
    host.querySelector("[data-home-kpis]").innerHTML =
      '<div><span>' + esc(L("My coverage","My coverage")) + '</span><strong>' + rows.length + '</strong><small>RM ' + state.rm + "</small></div>" +
      '<div><span>High alerts</span><strong class="negative">' + highAlerts.length + '</strong><small>' + esc(L("review today","ต้องตรวจสอบวันนี้")) + "</small></div>" +
      '<div><span>' + esc(L("SET filings today","SET filings วันนี้")) + '</span><strong class="gold">' + todayFilings.length + '</strong><small>' + esc(L("current coverage","ใน coverage ปัจจุบัน")) + "</small></div>" +
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

    var disclosureRows = rmFilings().slice().sort(function (a,b) { return String(b.ts || "").localeCompare(String(a.ts || "")); }).slice(0,6);
    var externalRows = rmNews().slice().sort(function (a,b) { return String(b.ts || "").localeCompare(String(a.ts || "")); }).slice(0,6);
    host.querySelector("[data-home-news-rm]").textContent = "RM " + state.rm;
    host.querySelector("[data-home-disclosure-count]").textContent = disclosureRows.length;
    host.querySelector("[data-home-external-count]").textContent = externalRows.length;
    host.querySelector("[data-home-disclosures]").innerHTML = disclosureRows.map(function (filing) {
      var filingUrl = safeHttpUrl(filing.url_th || filing.url) || href("disclosure-pulse.html");
      return '<a class="is1-home-feed-row" data-home-feed="disclosure" data-home-feed-ticker="' + esc(filing.tk) + '" href="' + esc(filingUrl) +
        '" target="_blank" rel="noopener">' + severityDot(filing.severity) + '<div><div class="is1-home-feed-meta"><strong>' +
        esc(filing.tk) + '</strong><span>SET · ' + esc(canonicalSector(filing.sector)) + '</span><time>' + esc(feedTime(filing.ts)) +
        '</time></div><p>' + esc(filing.title_th || filing.title) + "</p></div></a>";
    }).join("") || '<p class="is1s-empty">' + esc(L("No disclosures for this RM","ไม่มีข่าวเปิดเผยข้อมูลของ RM นี้")) + "</p>";
    host.querySelector("[data-home-external]").innerHTML = externalRows.map(function (item) {
      var newsUrl = safeHttpUrl(item.url) || href("external-news.html");
      return '<a class="is1-home-feed-row" data-home-feed="external" data-home-feed-ticker="' + esc(item.tk) + '" href="' + esc(newsUrl) +
        '" target="_blank" rel="noopener"><span class="is1-home-source-dot"></span><div><div class="is1-home-feed-meta"><strong>' +
        esc(item.tk) + '</strong><span>' + esc(item.source || L("External","ภายนอก")) + ' · ' + esc(canonicalSector(item.sector)) + '</span><time>' +
        esc(feedTime(item.ts)) + '</time></div><p>' + esc(item.title) + "</p></div></a>";
    }).join("") || '<p class="is1s-empty">' + esc(L("No external news for this RM","ไม่มีข่าวภายนอกของ RM นี้")) + "</p>";

    host.querySelectorAll("[data-home-ticker]").forEach(function (button) {
      button.addEventListener("click",function () {
        state.selectedTicker = button.dataset.homeTicker;
        renderContext();
        toggleContext(true);
      });
    });
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
    var news = document.createElement("section");
    news.className = "is1-home-news";
    news.innerHTML =
      '<header class="is1-home-news-head"><div><span>' + esc(L("RM coverage flow","ข่าวใน coverage ของ RM")) + '</span><h2>' +
      esc(L("Latest disclosures and external news","ข่าวเปิดเผยข้อมูลและข่าวภายนอกล่าสุด")) + '</h2><p>' +
      esc(L("The feed follows the RM selected in the top bar","รายการจะเปลี่ยนตาม RM ที่เลือกด้านบน")) +
      '</p></div><b data-home-news-rm>RM ' + state.rm + '</b></header><div class="is1-home-news-grid">' +
      '<section class="is1-home-news-panel"><header><div><span class="is1-home-news-icon disclosure">' + icon("radio-tower") + '</span><div><strong>' +
      esc(L("SET disclosures","ข่าวเปิดเผยข้อมูล")) + '</strong><small>' + esc(L("Newest coverage filings","ข่าว coverage ล่าสุด")) +
      '</small></div></div><div><span data-home-disclosure-count>0</span><a href="disclosure-pulse.html">' + esc(L("View all","ดูทั้งหมด")) +
      '</a></div></header><div class="is1-home-feed" data-home-disclosures></div></section>' +
      '<section class="is1-home-news-panel"><header><div><span class="is1-home-news-icon external">' + icon("rss") + '</span><div><strong>' +
      esc(L("External news","ข่าวภายนอก")) + '</strong><small>' + esc(L("Ticker-matched sources","ข่าวที่จับคู่ ticker")) +
      '</small></div></div><div><span data-home-external-count>0</span><a href="external-news.html">' + esc(L("View all","ดูทั้งหมด")) +
      '</a></div></header><div class="is1-home-feed" data-home-external></div></section></div></section>';
    control.appendChild(news);
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
      if (RMS.indexOf(rm) < 0) return;
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
