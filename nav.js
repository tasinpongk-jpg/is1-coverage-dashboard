/**
 * ISSUER INTELLIGENT TERMINAL — shared top chrome (Phosphor theme), on every dashboard page.
 *
 *   <script src="nav.js" defer></script>
 *
 * One source of truth for the header + banner, identical on every page:
 *   1. Loads the terminal fonts (JetBrains Mono + IBM Plex Sans Thai).
 *   2. Rebuilds <header> into the black/amber ISSUER INTELLIGENT TERMINAL top bar — brand +
 *      blinking caret on the LEFT, colour-dot nav-group dropdowns, and a
 *      PRIVILEGED & CONFIDENTIAL chip + the page's live freshness badge on the right.
 *   3. Injects a per-page banner right after <header> (square icon tile + group
 *      tag + title + tagline·<live meta>), bordered in the page's nav-group colour.
 *   4. Sets document.title to "<Page> · ISSUER INTELLIGENT TERMINAL".
 *
 * The chrome paints its OWN Phosphor colours (it does not depend on page tokens),
 * so it looks right even on pages whose body isn't themed yet. #staleBadge is
 * MOVED (not recreated) and #meta is folded into the banner tagline — both stay
 * live for page scripts that update them by id.
 */
(function () {
  "use strict";

  // ── Shared sector utils (exposed on window for every page) ──────────────────
  function sectorKey(name) {
    return String(name == null ? "" : name).replace(/[^A-Za-z0-9]/g, "").toUpperCase();
  }
  function hslToHex(h, s, l) {
    s /= 100; l /= 100;
    var c = (1 - Math.abs(2 * l - 1)) * s;
    var x = c * (1 - Math.abs(((h / 60) % 2) - 1));
    var m = l - c / 2, r = 0, g = 0, b = 0;
    if (h < 60) { r = c; g = x; } else if (h < 120) { r = x; g = c; }
    else if (h < 180) { g = c; b = x; } else if (h < 240) { g = x; b = c; }
    else if (h < 300) { r = x; b = c; } else { r = c; b = x; }
    function hx(v) { var n = Math.round((v + m) * 255).toString(16); return n.length === 1 ? "0" + n : n; }
    return "#" + hx(r) + hx(g) + hx(b);
  }
  function sectorColor(name) {
    var s = sectorKey(name), h = 0;
    for (var i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) % 360;
    return hslToHex(h, 60, 60);
  }
  if (typeof window !== "undefined") {
    window.sectorKey = window.sectorKey || sectorKey;
    window.sectorColor = window.sectorColor || sectorColor;
  }

  // ── Brand + confidentiality copy ────────────────────────────────────────────
  var BRAND_NAME = "IS1 COVERAGE DESK";
  var BRAND_SUB  = "SET COVERAGE DESK · ISSUER SURVEILLANCE";
  var BRAND_MARK = "IS";
  var CONF_SHORT = "PRIVILEGED & CONFIDENTIAL";
  var CONF_FULL  = "Privileged & confidential — internal SET coverage desk use only. Issuer surveillance and capital markets data.";

  // ── Nav groups (4-group IS1 taxonomy) ────────────────────────────────────────
  var MARKET_PAGES = [
    ["coverage-morning-brief.html", "Morning Brief"],
    ["sector-heatmap.html", "Sector Heatmap"],
    ["sector-comparison.html", "Sector Comparison"],
    ["ticker-summary.html", "Ticker Summary"],
    ["macro-overlays.html", "Macro Overlays"],
  ];
  var NEWS_PAGES = [
    ["disclosure-pulse.html", "Disclosure Pulse"],
    ["external-news.html", "External News"],
    ["oppday-minutes.html", "Opportunity Day"],
  ];
  var SURVEILLANCE_PAGES = [
    ["trading-signs.html", "Trading Signs"],
    ["unusual-trading.html", "Unusual Trading"],
    ["sec-enforcement.html", "SEC Enforcement"],
  ];
  var BOND_PAGES = [
    ["bond-summary.html", "Bond Summary"],
  ];
  // group order: Market → News → Surveillance → Bond Data
  var GROUPS = [
    { label: "Market",       color: "#3b82f6", pages: MARKET_PAGES },
    { label: "News",         color: "#f59e0b", pages: NEWS_PAGES },
    { label: "Surveillance", color: "#ef4444", pages: SURVEILLANCE_PAGES },
    { label: "Bond Data",    color: "#06b6d4", pages: BOND_PAGES },
  ];
  var GROUP_COLOR = {
    "Market":       "#3b82f6",
    "News":         "#f59e0b",
    "Surveillance": "#ef4444",
    "Bond Data":    "#06b6d4",
  };
  GROUPS.forEach(function (g) { GROUP_COLOR[g.label] = g.color; });

  // ── Per-page banner metadata (group drives the colour) ──────────────────────
  var PAGES = {
    "coverage-morning-brief.html": { group: "Market",       title: "Morning Brief",         icon: "chart",    tagline: "Daily price moves, returns and 20-day paths across coverage" },
    "sector-heatmap.html":         { group: "Market",       title: "Sector Heatmap",        icon: "grid",     tagline: "PE / PBV / DY / EV-EBITDA / NPM heat-coloured by sector percentile" },
    "sector-comparison.html":      { group: "Market",       title: "Sector Comparison",     icon: "bars",     tagline: "Valuation distributions across every sector" },
    "ticker-summary.html":         { group: "Market",       title: "Ticker Summary",        icon: "building", tagline: "Per-name fundamentals, valuation and a full detail drawer" },
    "macro-overlays.html":         { group: "Market",       title: "Macro Overlays",        icon: "chart",    tagline: "Macro indicators layered onto coverage tickers" },
    "disclosure-pulse.html":       { group: "News",         title: "Disclosure Pulse",      icon: "pulse",    tagline: "Live SET filings, ranked by importance" },
    "external-news.html":          { group: "News",         title: "External News",         icon: "globe",    tagline: "Ticker-matched wire flow from Thai news sources" },
    "oppday-minutes.html":         { group: "News",         title: "Opportunity Day Minutes", icon: "doc",    tagline: "Issuer Q&A transcripts from opportunity-day sessions" },
    "trading-signs.html":          { group: "Surveillance", title: "Trading Signs",         icon: "alert",    tagline: "Caution / trading signs SET has actually posted — ground truth" },
    "unusual-trading.html":        { group: "Surveillance", title: "Unusual Trading",       icon: "alert",    tagline: "Volume spikes, price gaps and intraday moves, severity-ranked" },
    "sec-enforcement.html":        { group: "Surveillance", title: "SEC Enforcement",       icon: "shield",   tagline: "Thai SEC actions matched to coverage — ground truth" },
    "bond-summary.html":           { group: "Bond Data",    title: "Bond Summary",          icon: "bank",     tagline: "Outstanding bonds, maturity wall, ESG & TTM by issuer" },
  };

  // ── Inline icon set (stroke = currentColor) ─────────────────────────────────
  var ICON_PATHS = {
    chart:    '<path d="M3 17l5-6 4 4 8-9"/><path d="M3 21h18"/>',
    building: '<path d="M4 21V5a1 1 0 0 1 1-1h9a1 1 0 0 1 1 1v16"/><path d="M15 9h4a1 1 0 0 1 1 1v11"/><path d="M3 21h18"/><path d="M8 8h2M8 12h2M8 16h2"/>',
    grid:     '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    bars:     '<path d="M3 21h18"/><rect x="5" y="11" width="3.4" height="8"/><rect x="10.3" y="5" width="3.4" height="14"/><rect x="15.6" y="14" width="3.4" height="5"/>',
    pulse:    '<path d="M3 12h4l2 6 4-15 2 9h6"/>',
    globe:    '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
    spark:    '<path d="M12 3l1.9 5.6L19.5 10l-5.6 1.9L12 17.5l-1.9-5.6L4.5 10l5.6-1.4z"/>',
    alert:    '<path d="M12 3.5l8.5 15h-17z"/><path d="M12 10v4"/><path d="M12 17h.01"/>',
    flag:     '<path d="M5 21V4"/><path d="M5 5h11l-2 3 2 3H5"/>',
    shield:   '<path d="M12 3l8 3v6c0 5-3.5 8-8 9c-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    bank:     '<path d="M3 9l9-5 9 5"/><path d="M4 9h16"/><path d="M5 9v8M9 9v8M15 9v8M19 9v8"/><path d="M3 21h18"/>',
    doc:      '<path d="M6 3h8l5 5v13H6z"/><path d="M14 3v5h5"/><path d="M9 13h6M9 17h6"/>',
    lock:     '<rect x="5" y="11" width="14" height="9" rx="1"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
  };
  function iconSVG(name, w) {
    var p = ICON_PATHS[name] || ICON_PATHS.chart, s = w || 24;
    return '<svg viewBox="0 0 24 24" width="' + s + '" height="' + s + '" fill="none" ' +
      'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + p + '</svg>';
  }

  // ── Load terminal fonts once ────────────────────────────────────────────────
  (function loadFonts() {
    if (document.querySelector('link[data-it-fonts]')) return;
    var pc = document.createElement("link"); pc.rel = "preconnect"; pc.href = "https://fonts.gstatic.com"; pc.crossOrigin = "";
    var l = document.createElement("link"); l.rel = "stylesheet"; l.setAttribute("data-it-fonts", "1");
    l.href = "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700;800&family=IBM+Plex+Sans+Thai:wght@400;500;600;700&display=swap";
    document.head.appendChild(pc); document.head.appendChild(l);
  })();

  var MONO = "'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,monospace";

  // ── Inject chrome CSS (hardcoded Phosphor — independent of page tokens) ──────
  var css = "\
header.term-header{display:flex;align-items:center;gap:18px;flex-wrap:wrap;height:52px;padding:0 24px;\
 position:sticky;top:0;z-index:200;background:#000;border-bottom:1px solid rgba(255,176,0,.2);\
 font-family:" + MONO + ";color:#e8e2cf}\
.term-left{display:flex;align-items:center;gap:18px;flex-wrap:wrap;min-width:0}\
.term-right{display:flex;align-items:center;gap:13px;margin-left:auto}\
.term-brand{display:flex;align-items:center;gap:9px;text-decoration:none}\
.term-logo{width:28px;height:28px;flex:none;display:flex;align-items:center;justify-content:center;\
 border:1px solid rgba(255,176,0,.55);font:700 12px " + MONO + ";color:#ffa028}\
.term-name{font:700 14px " + MONO + ";color:#ffa028;letter-spacing:.02em}\
.term-caret{color:#ffa028;font:700 14px " + MONO + ";animation:itblink 1.1s step-end infinite}\
@keyframes itblink{0%,49%{opacity:1}50%,100%{opacity:0}}\
.term-divider{width:1px;height:18px;background:rgba(255,176,0,.2)}\
nav.nav{display:flex;align-items:center;gap:16px;position:relative;flex-wrap:wrap;font:600 12px " + MONO + "}\
nav.nav .gnav-home{display:flex;align-items:center;gap:6px;color:#8a7a4a;text-decoration:none;padding:0 0 4px;border-bottom:2px solid transparent}\
nav.nav .gnav-home:hover{color:#cdbf90}\
nav.nav .gnav-home .hdot{width:6px;height:6px;border-radius:50%;background:#ffa028;flex:none}\
nav.nav .gnav-home:hover .hdot,nav.nav .gnav-home.here .hdot{box-shadow:0 0 7px #ffa028}\
.gnav-group{position:relative;display:flex;align-items:center}\
.gnav-btn{display:flex;align-items:center;gap:6px;background:none;border:none;cursor:pointer;\
 font:600 12px " + MONO + ";color:#8a7a4a;padding:0 0 2px;border-bottom:2px solid transparent}\
.gnav-btn:hover{color:#cdbf90}\
.gnav-btn .dot{width:6px;height:6px;border-radius:50%;background:var(--gn);flex:none}\
.gnav-btn .chev{font-size:9px;opacity:.7}\
.gnav-group.active .gnav-btn{color:var(--gn);border-bottom-color:var(--gn)}\
.gnav-group.active .gnav-btn .dot{box-shadow:0 0 7px var(--gn)}\
.gnav-panel{position:absolute;top:calc(100% + 9px);left:-6px;min-width:188px;display:none;z-index:300;\
 background:#070707;border:1px solid rgba(255,176,0,.22);box-shadow:0 12px 34px #000b;padding:5px;flex-direction:column}\
.gnav-panel::before{content:'';position:absolute;top:-11px;left:0;right:0;height:11px}\
.gnav-group.open .gnav-panel{display:flex}\
.gnav-group.secondary .gnav-panel{min-width:236px;max-height:72vh;overflow:auto}\
nav.nav .gnav-panel a{font:500 12px " + MONO + ";color:#9a8f5e;text-decoration:none;padding:7px 11px;\
 display:flex;align-items:center;gap:8px;white-space:nowrap;border-left:2px solid transparent}\
nav.nav .gnav-panel a:hover{color:#e8e2cf;background:rgba(255,176,0,.06)}\
nav.nav .gnav-panel a.here{color:var(--gn);border-left-color:var(--gn);background:rgba(255,176,0,.05)}\
nav.nav .gnav-panel a .pdot{width:5px;height:5px;border-radius:50%;background:var(--gn);opacity:.7;flex:none}\
.term-conf{display:inline-flex;align-items:center;gap:5px;font:600 10px " + MONO + ";letter-spacing:.05em;\
 color:#ffa028;border:1px solid rgba(255,176,0,.32);padding:5px 9px;white-space:nowrap;cursor:default}\
.term-conf svg{width:11px;height:11px}\
#staleBadge,.term-right .stale{font:500 11px " + MONO + ";color:#00d46a;white-space:nowrap}\
.term-banner{position:relative;overflow:hidden;background:#000;border-bottom:2px solid var(--bnr,#ffa028);padding:17px 24px}\
.term-banner::after{content:'';position:absolute;top:-90px;right:140px;width:300px;height:300px;border-radius:50%;\
 background:radial-gradient(circle,color-mix(in srgb,var(--bnr,#ffa028) 18%,transparent),transparent 65%);pointer-events:none}\
.term-banner-inner{max-width:1560px;margin:0 auto;display:flex;align-items:center;gap:14px;position:relative}\
.term-banner-icon{width:46px;height:46px;flex:none;display:flex;align-items:center;justify-content:center;\
 background:color-mix(in srgb,var(--bnr,#ffa028) 24%,#000);border:1px solid var(--bnr,#ffa028);\
 color:color-mix(in srgb,var(--bnr,#ffa028) 55%,#fff)}\
.term-banner-icon svg{width:22px;height:22px}\
.term-banner-tag{font:700 10px " + MONO + ";letter-spacing:.2em;color:#fff;background:var(--bnr,#ffa028);padding:3px 9px}\
.term-banner-title{font:800 25px " + MONO + ";color:#fff;letter-spacing:-.01em;margin-top:9px}\
.term-banner-tagline{font:400 12px " + MONO + ";color:#9a8f63;margin-top:4px}\
.term-banner-tagline .meta{color:#6f6440}\
@media(max-width:760px){.term-conf{display:none}.gnav-panel{position:fixed;left:10px;right:10px;top:auto;min-width:0}\
 .term-banner-title{font-size:20px}.term-banner-icon{width:40px;height:40px}}";
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  var here = location.pathname.split("/").pop() || "index.html";
  var meta = PAGES[here] || null;

  // ── Build grouped navigation into a <nav class="nav"> ───────────────────────
  function buildNav(nav) {
    var home = document.createElement("a");
    home.className = "gnav-home"; home.href = "index.html";
    home.innerHTML = '<span class="hdot"></span>Main page';
    if (here === "index.html") { home.classList.add("here"); home.style.color = "#cdbf90"; }
    nav.appendChild(home);

    GROUPS.forEach(function (g) {
      var wrap = document.createElement("div");
      wrap.className = "gnav-group"; wrap.style.setProperty("--gn", g.color);
      if (g.secondary) wrap.classList.add("secondary");
      var btn = document.createElement("button");
      btn.type = "button"; btn.className = "gnav-btn";
      btn.setAttribute("aria-haspopup", "true"); btn.setAttribute("aria-expanded", "false");
      btn.innerHTML = '<span class="dot"></span>' + g.label + '<span class="chev">▾</span>';
      var panel = document.createElement("div");
      panel.className = "gnav-panel";
      g.pages.forEach(function (p) {
        var a = document.createElement("a");
        a.href = p[0]; a.innerHTML = '<span class="pdot"></span>' + p[1];
        if (p[0] === here) { a.classList.add("here"); wrap.classList.add("active"); }
        panel.appendChild(a);
      });
      btn.addEventListener("click", function (e) {
        e.stopPropagation();
        var was = wrap.classList.contains("open"); closeAll();
        if (!was) { wrap.classList.add("open"); btn.setAttribute("aria-expanded", "true"); }
      });
      var t = null;
      wrap.addEventListener("mouseenter", function () { clearTimeout(t); closeAll(); wrap.classList.add("open"); btn.setAttribute("aria-expanded", "true"); });
      wrap.addEventListener("mouseleave", function () { clearTimeout(t); t = setTimeout(function () { wrap.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); }, 350); });
      wrap.appendChild(btn); wrap.appendChild(panel); nav.appendChild(wrap);
    });
    function closeAll() {
      nav.querySelectorAll(".gnav-group.open").forEach(function (w) { w.classList.remove("open"); w.querySelector(".gnav-btn").setAttribute("aria-expanded", "false"); });
    }
    document.addEventListener("click", closeAll);
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeAll(); });
  }

  // ── 1. Rebuild the header ───────────────────────────────────────────────────
  var header = document.querySelector("header");
  if (header) {
    var keep = {};
    Array.prototype.forEach.call(header.querySelectorAll("[id]"), function (el) {
      keep[el.id] = el; if (el.parentNode) el.parentNode.removeChild(el);
    });
    var stale = keep["staleBadge"], metaEl = keep["meta"];

    header.className = (header.className ? header.className + " " : "") + "term-header";
    header.innerHTML = "";

    var left = document.createElement("div"); left.className = "term-left";
    var brand = document.createElement("a"); brand.className = "term-brand"; brand.href = "index.html";
    brand.innerHTML = '<span class="term-logo">' + BRAND_MARK + '</span>' +
      '<span class="term-name">' + BRAND_NAME + '</span><span class="term-caret">▮</span>';
    left.appendChild(brand);
    var div = document.createElement("span"); div.className = "term-divider"; left.appendChild(div);
    var nav = document.createElement("nav"); nav.className = "nav"; buildNav(nav); left.appendChild(nav);

    var right = document.createElement("div"); right.className = "term-right";
    var conf = document.createElement("span"); conf.className = "term-conf"; conf.title = CONF_FULL;
    conf.innerHTML = iconSVG("lock", 11) + CONF_SHORT; right.appendChild(conf);
    if (!stale) { stale = document.createElement("span"); stale.id = "staleBadge"; stale.textContent = "● loading"; }
    right.appendChild(stale);

    header.appendChild(left); header.appendChild(right);

    var hidden = document.createElement("div"); hidden.style.display = "none";
    Object.keys(keep).forEach(function (id) { if (id !== "staleBadge" && id !== "meta") hidden.appendChild(keep[id]); });
    if (hidden.childNodes.length) header.appendChild(hidden);
  }

  // ── 2. Inject the per-page banner right after <header> ──────────────────────
  if (header && meta) {
    var color = GROUP_COLOR[meta.group] || "#ffa028";
    var banner = document.createElement("div");
    banner.className = "term-banner"; banner.style.setProperty("--bnr", color);
    banner.innerHTML =
      '<div class="term-banner-inner">' +
        '<div class="term-banner-icon">' + iconSVG(meta.icon, 22) + '</div>' +
        '<div style="flex:1;min-width:0">' +
          '<span class="term-banner-tag">' + meta.group.toUpperCase() + '</span>' +
          '<div class="term-banner-title">' + meta.title + '</div>' +
          '<div class="term-banner-tagline"><span>' + meta.tagline + '</span></div>' +
        '</div>' +
      '</div>';
    if (metaEl) {
      var tagline = banner.querySelector(".term-banner-tagline");
      var sep = document.createElement("span"); sep.textContent = " · "; sep.style.color = "#6f6440";
      metaEl.classList.add("meta");
      metaEl.style.cssText += ";display:inline;font:inherit;letter-spacing:normal;margin:0;text-transform:none";
      tagline.appendChild(sep); tagline.appendChild(metaEl);
    }
    header.parentNode.insertBefore(banner, header.nextSibling);
  }

  // ── 3. Browser tab ──────────────────────────────────────────────────────────
  if (meta) document.title = meta.title + " · " + BRAND_NAME;
  else if (here === "index.html") document.title = BRAND_NAME + " — SET Coverage Desk";
})();
