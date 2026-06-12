/**
 * IS1 grouped navigation — shared across all dashboard pages.
 *
 * Replaces each page's flat <nav class="nav"> with four color-coded group
 * dropdowns matching the index page's sections (Market / News /
 * Surveillance / Macro). The original flat links remain in the HTML as a
 * no-JS fallback; this script swaps them out at load.
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
        ["coverage-morning-brief.html", "Morning Brief"],
        ["ticker-summary.html", "Ticker Summary"],
        ["sector-heatmap.html", "Sector Heatmap"],
        ["sector-comparison.html", "Sector Compare"],
      ],
    },
    {
      label: "News", color: "#f59e0b",
      pages: [
        ["disclosure-pulse.html", "Disclosure Pulse"],
        ["external-news.html", "External News"],
        ["oppday-minutes.html", "Oppday Minutes"],
        ["ai-insights.html", "AI Insights"],
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
      label: "Macro", color: "#06b6d4",
      pages: [
        ["bond-summary.html", "Bond Summary"],
        ["macro-overlays.html", "Macro Overlays"],
      ],
    },
  ];

  var nav = document.querySelector("nav.nav");
  if (!nav) return; // index has its own layout

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
@media(max-width:760px){\
 .gnav-panel{position:fixed;left:10px;right:10px;top:auto;min-width:0}\
 .gnav-btn{padding:7px 7px}.gnav-home{padding:7px 7px}}";
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  var here = location.pathname.split("/").pop() || "index.html";

  // keep non-link extras (stale badge etc.) to re-append after rebuild
  var extras = Array.prototype.filter.call(nav.children, function (el) {
    return el.tagName !== "A";
  });

  nav.innerHTML = "";
  var home = document.createElement("a");
  home.className = "gnav-home";
  home.href = "index.html";
  home.textContent = "Index";
  nav.appendChild(home);

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
      a.href = p[0];
      a.innerHTML = '<span class="pdot"></span>' + p[1];
      if (p[0] === here) {
        a.classList.add("here");
        wrap.classList.add("active");
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
