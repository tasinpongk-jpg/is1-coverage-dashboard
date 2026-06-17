/**
 * IS1 grouped navigation — shared across all dashboard pages.
 *
 * Replaces each page's flat <nav class="nav"> with color-coded group
 * dropdowns matching the index page's sections (Market / News /
 * Surveillance / Bond Data / Visits). The original flat links remain in the
 * HTML as a no-JS fallback; this script swaps them out at load.
 *
 * The page's stale badge (and any other non-link elements inside the nav)
 * are MOVED, not recreated, so page scripts holding references keep working.
 *
 * Included by every page: <script src="nav.js" defer></script>
 */
(function () {
  "use strict";

  var GROUPS = [
    {
      label: "Market", color: "#3b82f6",
      pages: [
        ["price-movement.html", "Price Movement"],
        ["company-summary.html", "Company Summary"],
        ["multiples-comparison.html", "Multiples Comparison"],
        ["multiples-band.html", "Multiples Band"],
        ["https://tradingview-daily-dashboard.tasinpong-k.workers.dev/", "Daily Market Board"], // external (separate worker, opens new tab)
      ],
    },
    {
      label: "News", color: "#f59e0b",
      pages: [
        ["disclosure-pulse.html", "Disclosure Pulse"],
        ["external-news.html", "External News"],
        ["oppday-minutes.html", "Oppday Minutes"],
        ["ai-insights.html", "AI Insights"],
        ["https://macro-brief-buy.pages.dev", "Global-Macro Brief"], // external (Cloudflare Pages, opens new tab)
      ],
    },
    {
      label: "Surveillance", color: "#ef4444",
      pages: [
        ["unusual-trading.html", "Unusual Trading"],
        ["trading-signs.html", "Trading Signs"],
        ["sec-enforcement.html", "SEC Enforcement"],
      ],
    },
    {
      label: "Bond Data", color: "#06b6d4",
      pages: [
        ["bond-summary.html", "Bond Summary"],
        ["bond-data-sec.html", "BOND Data from SEC"],
      ],
    },
    {
      label: "Visits", color: "#22c55e",
      pages: [
        ["visits.html", "Visit Planner"],
      ],
    },
  ];

  // Per-page line icon + one-line description for the title banner.
  // Page NAME and COLOR come from GROUPS above (single source of truth, so the
  // banner title can never drift from the menu label).
  var META = {
    "price-movement.html":      { ic: '<path d="M3 17l6-6 4 4 7-7"/><path d="M17 8h4v4"/>',                                                                  desc: "Daily price moves across coverage" },
    "company-summary.html":     { ic: '<path d="M3 21h18"/><path d="M5 21V4a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v17"/><path d="M19 21V9a1 1 0 0 0-1-1h-3"/><path d="M9 7h2M9 11h2M9 15h2"/>', desc: "Fundamentals and profile per company" },
    "multiples-comparison.html":{ ic: '<path d="M3 3v18h18"/><path d="M7 14v3"/><path d="M12 9v8"/><path d="M17 5v12"/>',                                     desc: "Valuation multiples side by side" },
    "multiples-band.html":      { ic: '<path d="M3 12l4-4 4 3 4-6 6 5"/><path d="M3 18l4-4 4 3 4-6 6 5"/>',                                              desc: "Valuation ranges over time" },
    "disclosure-pulse.html":    { ic: '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',                                                                          desc: "Live SET filings, ranked by importance" },
    "external-news.html":       { ic: '<path d="M4 4h13a1 1 0 0 1 1 1v13a2 2 0 0 0 2 2H6a2 2 0 0 1-2-2V4Z"/><path d="M8 8h6M8 12h6M8 16h4"/>',          desc: "Wire & RSS headlines matched to coverage" },
    "oppday-minutes.html":      { ic: '<path d="M2 4h20"/><path d="M3 4v10a1 1 0 0 0 1 1h16a1 1 0 0 0 1-1V4"/><path d="M12 15v5"/><path d="M9 20h6"/>', desc: "Earnings-call notes and takeaways" },
    "ai-insights.html":         { ic: '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3Z"/>', desc: "Model-written commentary on the coverage" },
    "unusual-trading.html":     { ic: '<path d="M10.3 3.3 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.3a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4"/><path d="M12 17h.01"/>', desc: "Volume and price anomalies flagged" },
    "trading-signs.html":       { ic: '<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><path d="M4 22v-7"/>',                       desc: "Current SET trading signs on coverage" },
    "sec-enforcement.html":     { ic: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="M12 8v4"/><path d="M12 16h.01"/>',                desc: "Thai SEC enforcement actions" },
    "bond-summary.html":        { ic: '<path d="M3 22h18"/><path d="M4 10l8-6 8 6"/><path d="M6 22v-9M10 22v-9M14 22v-9M18 22v-9"/>',                    desc: "Outstanding bonds across coverage" },
    "bond-data-sec.html":       { ic: '<path d="M12 7c4.4 0 8-1.1 8-2.5S16.4 2 12 2 4 3.1 4 4.5 7.6 7 12 7Z"/><path d="M4 4.5v15C4 20.9 7.6 22 12 22s8-1.1 8-2.5v-15"/><path d="M4 12c0 1.4 3.6 2.5 8 2.5s8-1.1 8-2.5"/>', desc: "Bond filings from the SEC" },
    "visits.html":              { ic: '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><path d="M12 12a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z"/>', desc: "Plan and track company visits" },
  };

  var css = "\
nav.nav{display:flex;align-items:center;gap:2px;position:relative}\
.gnav-home{font-size:12.5px;color:var(--muted,#8089a0);text-decoration:none;padding:7px 10px;border-radius:7px}\
.gnav-home:hover{color:var(--text,#e6e8ed);background:var(--card2,#1a1d27)}\
.gnav-group{position:relative}\
.gnav-btn{display:flex;align-items:center;gap:6px;background:none;border:none;cursor:pointer;\
 font:600 12.5px/1 'Inter','Segoe UI',system-ui,sans-serif;color:var(--muted,#8089a0);\
 padding:7px 10px;border-radius:7px;border-bottom:2px solid transparent}\
.gnav-btn:hover{color:var(--text,#e6e8ed);background:var(--card2,#1a1d27)}\
.gnav-btn .dot{width:7px;height:7px;border-radius:50%;background:var(--gn);flex-shrink:0}\
.gnav-btn .chev{font-size:9px;opacity:.6}\
.gnav-group.active .gnav-btn{color:var(--text,#e6e8ed);border-bottom-color:var(--gn)}\
.gnav-panel{position:absolute;top:calc(100% + 6px);left:0;min-width:185px;display:none;z-index:300;\
 background:var(--card,#14171f);border:1px solid var(--border2,#2a2f3d);border-radius:10px;\
 box-shadow:0 10px 34px #000a;padding:6px;flex-direction:column}\
.gnav-panel::before{content:'';position:absolute;top:-10px;left:0;right:0;height:10px}\
.gnav-group.open .gnav-panel{display:flex}\
.gnav-panel a{font-size:12.5px;color:var(--muted,#8089a0);text-decoration:none;padding:8px 12px;\
 border-radius:7px;display:flex;align-items:center;gap:8px;white-space:nowrap}\
.gnav-panel a:hover{color:var(--text,#e6e8ed);background:var(--card2,#1a1d27)}\
.gnav-panel a.here{color:var(--gn);font-weight:700;background:color-mix(in srgb,var(--gn) 10%,transparent)}\
.gnav-panel a .pdot{width:5px;height:5px;border-radius:50%;background:var(--gn);opacity:.55;flex-shrink:0}\
.gnav-panel a .ext{margin-left:auto;padding-left:12px;font-size:11px;opacity:.5}\
.gnav-panel a:hover .ext{opacity:.8}\
@media(max-width:760px){\
 .gnav-panel{position:fixed;left:10px;right:10px;top:auto;min-width:0}\
 .gnav-btn{padding:7px 7px}.gnav-home{padding:7px 7px}}\
\
/* ── PAGE TITLE BANNER (full-width colored band, below the top bar) ── */\
.phbanner{position:relative;overflow:hidden;display:flex;align-items:center;gap:16px;padding:18px 32px;color:#fff;\
 background:linear-gradient(120deg,var(--ph) 0%,color-mix(in srgb,var(--ph) 42%,#0a0c12) 100%);\
 border-bottom:1px solid color-mix(in srgb,var(--ph) 45%,#0a0c12);animation:phin .4s ease both}\
.phbanner::before{content:'';position:absolute;inset:0;pointer-events:none;\
 background:radial-gradient(circle at 13% 25%,rgba(255,255,255,.20),transparent 45%)}\
.phbanner::after{content:'';position:absolute;right:-50px;top:-70px;width:260px;height:260px;border-radius:50%;pointer-events:none;\
 background:radial-gradient(circle,rgba(255,255,255,.13),transparent 70%)}\
.ph-ico{position:relative;width:46px;height:46px;border-radius:12px;flex-shrink:0;display:flex;align-items:center;justify-content:center;\
 background:rgba(255,255,255,.16);border:1px solid rgba(255,255,255,.28)}\
.ph-ico svg{width:24px;height:24px;fill:none;stroke:#fff;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}\
.ph-txt{position:relative;min-width:0}\
.ph-cat{display:inline-flex;align-items:center;gap:6px;font-size:10px;font-weight:700;letter-spacing:1.2px;text-transform:uppercase;\
 color:#fff;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.24);padding:3px 9px;border-radius:20px}\
.ph-title{font-size:24px;font-weight:800;letter-spacing:-.4px;margin-top:8px;line-height:1.1;color:#fff;text-shadow:0 1px 12px rgba(0,0,0,.22)}\
.ph-desc{font-size:12.5px;margin-top:4px;color:rgba(255,255,255,.82)}\
@keyframes phin{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:none}}\
@media(prefers-reduced-motion:reduce){.phbanner{animation:none}}\
@media(max-width:760px){.phbanner{padding:14px 16px;gap:12px}.ph-title{font-size:20px}.ph-ico{width:40px;height:40px}.ph-ico svg{width:21px;height:21px}}\
\
/* ── UNIFIED TOP BAR (identical to homepage: IS mark + The Terminal + status) ── */\
.gtopbar{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:18px 32px;\
 border-bottom:1px solid var(--border,#232733);position:sticky;top:0;z-index:200;\
 background:#0a0c12ee;backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);\
 font-family:'Inter','Segoe UI',system-ui,sans-serif}\
.gtopbar.ext-bar{position:relative;top:auto}\
.gbrand{display:flex;align-items:center;gap:14px;text-decoration:none;color:inherit;flex-shrink:0}\
.gbrand-mark{width:34px;height:34px;border-radius:9px;flex-shrink:0;display:flex;align-items:center;justify-content:center;\
 background:linear-gradient(135deg,#6366f1,#8b5cf6);font-weight:800;font-size:14px;letter-spacing:-.5px;color:#fff}\
.gbrand-text h1{font-size:16px;font-weight:700;letter-spacing:-.2px;color:var(--text,#e6e8ed);display:flex;align-items:center;border:0;margin:0;padding:0}\
.gbrand-text .sub{font-size:10px;color:var(--muted,#8089a0);margin-top:2px;letter-spacing:.4px;text-transform:uppercase}\
.gbrand .cursor{display:inline-block;width:8px;height:14px;margin-left:4px;border-radius:1px;background:#6366f1;vertical-align:-1px;animation:termblink 1.1s steps(1) infinite}\
@keyframes termblink{50%{opacity:0}}\
@media(prefers-reduced-motion:reduce){.gbrand .cursor{animation:none}}\
.gtopbar .stale,.gtopbar .stale-pill{font-size:11px;padding:5px 12px;border-radius:20px;white-space:nowrap;flex-shrink:0;\
 background:#22c55e15;color:#22c55e;border:1px solid #22c55e30}\
.gtopbar .stale.warn,.gtopbar .stale-pill.warn{background:#f59e0b15;color:#f59e0b;border-color:#f59e0b30}\
.gtopbar .stale.unknown,.gtopbar .stale-pill.unknown{background:#5a627a15;color:var(--muted,#8089a0);border-color:#5a627a30}\
.phbanner .ph-desc{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px}\
.phbanner .meta{display:inline;font-size:12.5px;color:rgba(255,255,255,.72);margin:0}\
.phbanner .meta::before{content:'\\00b7 ';opacity:.7}\
@media(max-width:760px){.gtopbar{padding:14px 16px;gap:12px}.gbrand-text h1{font-size:15px}}";
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  // Where this nav.js is served from. Lets the menu link back to the main
  // dashboard even when this script is loaded on another site (the Market Board).
  var BASE = "", offsite = false;
  try {
    var selfScript = document.currentScript;
    if (!selfScript) {
      var ss = document.querySelectorAll("script[src]");
      for (var i = 0; i < ss.length; i++) if (/nav\.js(\?|$)/.test(ss[i].src)) selfScript = ss[i];
    }
    if (selfScript && selfScript.src) {
      var u = new URL(selfScript.src);
      BASE = u.origin;
      offsite = (u.origin !== location.origin);
    }
  } catch (e) {}
  function link(href) { // absolute back to the dashboard when off-site; pass external URLs through
    return /^https?:\/\//.test(href) ? href : (BASE ? BASE + "/" + href : href);
  }

  // On the main site each page provides <nav class="nav">. When loaded on
  // another origin, there is none — build a Terminal top bar and prepend it.
  var nav = document.querySelector("nav.nav");
  if (!nav) {
    if (!offsite) return; // same-origin page without a nav (e.g. index) keeps its own layout
    var extBar = document.createElement("header");
    extBar.className = "gtopbar ext-bar";
    var xbrand = document.createElement("a");
    xbrand.className = "gbrand";
    xbrand.href = link("index.html");
    xbrand.innerHTML =
      '<div class="gbrand-mark">IS</div>' +
      '<div class="gbrand-text"><h1>The Terminal<span class="cursor"></span></h1>' +
      '<div class="sub">IS1 Coverage Desk · SET Issuer Department 1</div></div>';
    nav = document.createElement("nav");
    nav.className = "nav";
    extBar.appendChild(xbrand);
    extBar.appendChild(nav);
    document.body.insertBefore(extBar, document.body.firstChild);
  }

  var here = location.pathname.split("/").pop() || "index.html";
  // Live URLs are extensionless (/price-movement), local ones keep .html —
  // compare on the stem so both resolve to the same page.
  var hereKey = here.replace(/\.html$/, "");

  // keep non-link extras (stale badge etc.) to re-append after rebuild
  var extras = Array.prototype.filter.call(nav.children, function (el) {
    return el.tagName !== "A";
  });

  nav.innerHTML = "";
  var home = document.createElement("a");
  home.className = "gnav-home";
  home.href = link("index.html");
  home.textContent = "The Terminal";
  nav.appendChild(home);

  var heroTitle = null, heroColor = null, heroGroup = null, heroFile = null;
  GROUPS.forEach(function (g) {
    var wrap = document.createElement("div");
    wrap.className = "gnav-group";
    wrap.style.setProperty("--gn", g.color);

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "gnav-btn";
    btn.setAttribute("aria-haspopup", "true");
    btn.setAttribute("aria-expanded", "false");
    btn.innerHTML = '<span class="dot"></span>' + g.label + '<span class="chev">▾</span>';

    var panel = document.createElement("div");
    panel.className = "gnav-panel";
    g.pages.forEach(function (p) {
      var a = document.createElement("a");
      a.href = link(p[0]);
      var external = /^https?:\/\//.test(p[0]);
      // Every dashboard — including the external workers/Pages sites (Daily
      // Market Board, Global-Macro Brief) — navigates in the SAME tab so moving
      // between them feels like one app rather than spawning new windows.
      a.innerHTML = '<span class="pdot"></span>' + p[1];
      if (!external && p[0].replace(/\.html$/, "") === hereKey) {
        a.classList.add("here");
        wrap.classList.add("active");
        heroTitle = p[1];
        heroColor = g.color;
        heroGroup = g.label;
        heroFile = p[0];
      }
      panel.appendChild(a);
    });

    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var was = wrap.classList.contains("open");
      closeAll();
      if (!was) {
        wrap.classList.add("open");
        btn.setAttribute("aria-expanded", "true");
      }
    });
    // hover with forgiveness: a short close delay so crossing the gap (or
    // briefly overshooting) doesn't snap the menu shut mid-click
    var closeTimer = null;
    wrap.addEventListener("mouseenter", function () {
      clearTimeout(closeTimer);
      closeAll();
      wrap.classList.add("open");
      btn.setAttribute("aria-expanded", "true");
    });
    wrap.addEventListener("mouseleave", function () {
      clearTimeout(closeTimer);
      closeTimer = setTimeout(function () {
        wrap.classList.remove("open");
        btn.setAttribute("aria-expanded", "false");
      }, 350);
    });

    wrap.appendChild(btn);
    wrap.appendChild(panel);
    nav.appendChild(wrap);
  });

  extras.forEach(function (el) { nav.appendChild(el); });

  // ── Unified top bar + page title banner (subpages only; index keeps its own) ──
  if (heroTitle) {
    var header = nav.closest("header") || document.querySelector("header");
    if (header && !header.classList.contains("gtopbar")) {
      // Preserve the live status pill and detail line before we rebuild —
      // page scripts keep updating these same nodes by id.
      var staleNode = document.getElementById("staleBadge");
      var metaNode = document.getElementById("meta");

      // Rebuild the bar to match the homepage: IS mark · The Terminal
      // (blinking) · menu · status. The old page-specific title is dropped —
      // the colored banner below now carries the page identity.
      header.classList.add("gtopbar");
      header.innerHTML = "";

      var brand = document.createElement("a");
      brand.className = "gbrand";
      brand.href = "index.html";
      brand.innerHTML =
        '<div class="gbrand-mark">IS</div>' +
        '<div class="gbrand-text"><h1>The Terminal<span class="cursor"></span></h1>' +
        '<div class="sub">IS1 Coverage Desk · SET Issuer Department 1</div></div>';
      header.appendChild(brand);
      header.appendChild(nav);
      if (staleNode) header.appendChild(staleNode); // status pill, far right

      // Colored page banner directly below the bar; the live detail line
      // (counts / as-of) rides along next to the description.
      if (!document.querySelector(".phbanner")) {
        var meta = META[heroFile] || { ic: "", desc: "" };
        var banner = document.createElement("div");
        banner.className = "phbanner";
        banner.style.setProperty("--ph", heroColor);
        banner.innerHTML =
          '<div class="ph-ico"><svg viewBox="0 0 24 24" aria-hidden="true">' + meta.ic + '</svg></div>' +
          '<div class="ph-txt">' +
            '<span class="ph-cat">' + heroGroup + '</span>' +
            '<div class="ph-title">' + heroTitle + '</div>' +
            '<div class="ph-desc">' + (meta.desc ? '<span class="ph-d">' + meta.desc + '</span>' : '') + '</div>' +
          '</div>';
        if (metaNode) banner.querySelector(".ph-desc").appendChild(metaNode);
        header.parentNode.insertBefore(banner, header.nextSibling);
      }
    }
  }

  function closeAll() {
    nav.querySelectorAll(".gnav-group.open").forEach(function (w) {
      w.classList.remove("open");
      w.querySelector(".gnav-btn").setAttribute("aria-expanded", "false");
    });
  }
  document.addEventListener("click", closeAll);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeAll();
  });
})();
