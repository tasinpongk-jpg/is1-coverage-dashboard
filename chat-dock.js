/**
 * REX agent console shared by every dashboard page.
 * Threads stay in sessionStorage; credentials stay in localStorage and are sent
 * only to the Worker, where MiniMax M3 and deterministic tools are invoked.
 */
(function () {
  "use strict";

  var AGENTS = {
    hermes: {
      label: "Hermes", color: "#f59e0b", icon: "news",
      tag: "News, disclosures, silent filers and Oppday",
      tagKey: "chat.hermes.tag",
      data: ["external-news", "disclosure-pulse", "oppday-minutes"],
      chips: [
        { key: "chat.hermes.chip.news", text: "What news moved RM {rm} coverage today?" },
        { key: "chat.hermes.chip.silent", text: "Any overdue or silent filers in RM {rm} coverage?" },
        { key: "chat.hermes.chip.cpn", text: "Show CPN latest SET filings and filing dates." },
        { key: "chat.hermes.chip.food", text: "อัปเดตข่าวและ filing กลุ่ม FOOD วันนี้" },
      ],
    },
    atlas: {
      label: "Atlas", color: "#3b82f6", icon: "chart",
      tag: "Prices, movers, alerts and exact threshold screens",
      tagKey: "chat.atlas.tag",
      data: ["morning-brief", "unusual-trading"],
      chips: [
        { key: "chat.atlas.chip.movers", text: "Show movers beyond plus or minus 2% in RM {rm} coverage." },
        { key: "chat.atlas.chip.alerts", text: "Any high-severity alerts in RM {rm} coverage today?" },
        { key: "chat.atlas.chip.low", text: "Which covered tickers hit a 52-week low?" },
      ],
    },
    pythia: {
      label: "Pythia", color: "#8b5cf6", icon: "layers",
      tag: "IS1 sector performance, breadth and relative screens",
      tagKey: "chat.pythia.tag",
      data: ["morning-brief"],
      chips: [
        { key: "chat.pythia.chip.sector", text: "Rank all 6 IS1 sectors by 1-day return and breadth." },
        { key: "chat.pythia.chip.prop", text: "Compare FOOD, PROP and PF&REIT on 1-day, 5-day and YTD performance." },
        { key: "chat.pythia.chip.market", text: "Which sectors have the weakest breadth today?" },
      ],
    },
    lex: {
      label: "Lex", color: "#10b981", icon: "book",
      tag: "SET and SEC rules with retrieved PDF page citations",
      tagKey: "chat.lex.tag",
      data: ["lex-regulations"],
      chips: [
        { key: "chat.lex.chip.board", text: "What must a listed company disclose after a board resolution?" },
        { key: "chat.lex.chip.connected", text: "When is a connected transaction subject to shareholder approval?" },
        { key: "chat.lex.chip.freeFloat", text: "อธิบายเกณฑ์ free float ของ SET" },
      ],
    },
  };
  var ORDER = ["hermes", "atlas", "pythia", "lex"];
  var RMS = ["C", "K", "O", "G", "P", "T"];
  var RM_ALIASES = {};
  RM_ALIASES["Cha" + "mp"] = "C";
  RM_ALIASES["Ka" + "e"] = "K";
  RM_ALIASES["Or" + "n"] = "O";
  RM_ALIASES["Gi" + "ft"] = "G";
  RM_ALIASES["Pi" + "m"] = "P";
  RM_ALIASES["To" + "ny"] = "T";

  var state = {
    open: false,
    agent: sessionStorage.getItem("is1_dock_agent") || "hermes",
    busy: false,
    busyAgent: null,
    tickers: null,
  };

  function tr(key, fallback, vars) {
    var s = window.I18N && typeof window.I18N.t === "function" ? window.I18N.t(key) : fallback;
    if (s === key) s = fallback;
    return String(s).replace(/\{(\w+)\}/g, function (_, k) {
      return vars && vars[k] != null ? vars[k] : "";
    });
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  var ICONS = {
    news: '<path d="M4 5h16v14H4z"/><path d="M8 9h8M8 13h5"/>',
    chart: '<path d="M4 19V5M4 19h16"/><path d="m7 15 4-4 3 2 5-6"/>',
    layers: '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 12 9 5 9-5M3 16l9 5 9-5"/>',
    book: '<path d="M4 5a3 3 0 0 1 3-3h13v17H7a3 3 0 0 0-3 3V5Z"/><path d="M7 18h13"/>',
    close: '<path d="m6 6 12 12M18 6 6 18"/>',
    trash: '<path d="M3 6h18M8 6V4h8v2M19 6l-1 15H6L5 6M10 11v5M14 11v5"/>',
    send: '<path d="m22 2-7 20-4-9-9-4 20-7Z"/><path d="M22 2 11 13"/>',
    spark: '<path d="m12 3-1.7 5.3a3 3 0 0 1-2 2L3 12l5.3 1.7a3 3 0 0 1 2 2L12 21l1.7-5.3a3 3 0 0 1 2-2L21 12l-5.3-1.7a3 3 0 0 1-2-2L12 3Z"/>',
    thumbsUp: '<path d="M7 10v11H3V10h4ZM7 19h10.5a2 2 0 0 0 2-1.7l1-6A2 2 0 0 0 18.5 9H14l1-4a2.5 2.5 0 0 0-2.5-3L7 10"/>',
    thumbsDown: '<path d="M7 14V3H3v11h4ZM7 5h10.5a2 2 0 0 1 2 1.7l1 6a2 2 0 0 1-2 2.3H14l1 4a2.5 2.5 0 0 1-2.5 3L7 14"/>',
    refresh: '<path d="M20 11a8 8 0 1 0-2.3 5.7"/><path d="M20 4v7h-7"/>',
    database: '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v6c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 11v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>',
  };
  function icon(name, size) {
    return '<svg aria-hidden="true" width="' + (size || 16) + '" height="' + (size || 16) +
      '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' +
      ICONS[name] + "</svg>";
  }

  var css = `
#is1-dock-btn{position:fixed;right:18px;bottom:18px;z-index:9000;display:flex;align-items:center;gap:8px;height:42px;
 background:var(--text,#e7e9ee);color:var(--bg,#0b0d12);border:1px solid color-mix(in srgb,var(--text,#e7e9ee) 72%,transparent);border-radius:7px;
 padding:0 14px;font:700 12px/1 'Sarabun','Segoe UI',sans-serif;cursor:pointer;box-shadow:0 10px 30px #0007;
 transition:transform .18s ease,box-shadow .18s ease}
#is1-dock-btn:hover{transform:translateY(-2px);box-shadow:0 14px 34px #0009}
#is1-dock{position:fixed;right:18px;bottom:18px;z-index:9001;width:460px;max-width:calc(100vw - 24px);height:680px;
 max-height:calc(100dvh - 36px);display:none;flex-direction:column;background:var(--card,#14171f);border:1px solid var(--border2,#2a2f3d);
 border-radius:8px;box-shadow:0 18px 60px #000b;font-family:'Sarabun','Segoe UI',sans-serif;overflow:hidden;transform-origin:bottom right}
#is1-dock.open{display:flex;animation:is1d-in .22s ease-out both}
@keyframes is1d-in{from{opacity:0;transform:translateY(10px) scale(.985)}to{opacity:1;transform:none}}
.is1d-head{display:flex;align-items:center;justify-content:space-between;gap:10px;min-height:48px;padding:0 10px 0 14px;background:var(--bg2,#0f1117);border-bottom:1px solid var(--border,#232733)}
.is1d-brand{display:flex;align-items:center;gap:9px;color:var(--text,#e6e8ed);font-size:12px;font-weight:800;letter-spacing:0}
.is1d-brand svg{color:#8b5cf6}.is1d-head-actions{display:flex;align-items:center;gap:3px}
.is1d-icon-btn{width:34px;height:34px;display:grid;place-items:center;border:0;background:transparent;color:var(--muted,#8089a0);border-radius:6px;cursor:pointer}
.is1d-icon-btn:hover{background:var(--card2,#1a1d27);color:var(--text,#e6e8ed)}
.is1d-tabs{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid var(--border,#232733);background:var(--bg2,#0f1117)}
.is1d-tab{position:relative;display:flex;align-items:center;justify-content:center;gap:6px;min-width:0;height:44px;padding:0 5px;cursor:pointer;border:0;background:none;color:var(--muted,#8089a0);font:700 11.5px/1 inherit}
.is1d-tab::after{content:'';position:absolute;left:14px;right:14px;bottom:0;height:2px;background:var(--ac,#3b82f6);transform:scaleX(0);transition:transform .18s ease}
.is1d-tab.on{color:var(--text,#e6e8ed)}.is1d-tab.on::after{transform:scaleX(1)}.is1d-tab:disabled{opacity:.55;cursor:wait}
.is1d-sub{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;padding:9px 14px;border-bottom:1px solid var(--border,#232733);background:var(--card,#14171f)}
.is1d-agent-meta{min-width:0}.is1d-tag{display:block;color:var(--text,#e6e8ed);font-size:11.5px;line-height:1.35}.is1d-fresh{display:flex;align-items:center;gap:5px;margin-top:3px;color:var(--dim,#687086);font-size:10.5px}
.is1d-rm-wrap{display:flex;align-items:center;gap:6px;white-space:nowrap;color:var(--muted,#8089a0);font-size:10.5px}.is1d-rm{height:28px;background:var(--bg2,#0f1117);color:var(--text,#e6e8ed);border:1px solid var(--border,#232733);border-radius:5px;font:700 11px inherit;padding:2px 7px}
.is1d-log{flex:1;min-height:0;overflow-y:auto;padding:15px;display:flex;flex-direction:column;gap:10px;scrollbar-width:thin}
.is1d-empty{margin:auto 0;text-align:center;padding:22px 24px;color:var(--muted,#8089a0);animation:is1d-fade .2s ease both}
.is1d-empty-mark{width:42px;height:42px;display:grid;place-items:center;margin:0 auto 10px;border:1px solid color-mix(in srgb,var(--ac) 48%,var(--border));border-radius:8px;color:var(--ac);background:color-mix(in srgb,var(--ac) 9%,transparent)}
.is1d-empty strong{display:block;color:var(--text,#e6e8ed);font-size:14px}.is1d-empty span{display:block;margin-top:5px;font-size:11.5px;line-height:1.5}
@keyframes is1d-fade{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
.is1d-msg{max-width:92%;padding:9px 11px;border-radius:7px;font-size:12.5px;line-height:1.55;word-break:break-word;animation:is1d-fade .18s ease both}
.is1d-msg.user{align-self:flex-end;background:color-mix(in srgb,var(--ac,#3b82f6) 14%,var(--card));border:1px solid color-mix(in srgb,var(--ac,#3b82f6) 32%,var(--border));color:var(--text,#e6e8ed);white-space:pre-wrap}
.is1d-msg.bot{align-self:stretch;max-width:100%;background:var(--card2,#1a1d27);border:1px solid var(--border,#232733);color:var(--text,#e6e8ed)}
.is1d-msg.err{align-self:stretch;max-width:100%;color:#fca5a5;background:#ef444414;border:1px solid #ef44443d}
.is1d-agent-name{display:flex;align-items:center;gap:6px;margin-bottom:7px;font-size:10.5px;font-weight:800;color:var(--ac,#3b82f6)}
.is1d-copy{white-space:normal}.is1d-copy b{font-weight:800}.is1d-line{min-height:1.2em}.is1d-bullet{position:relative;padding-left:13px}.is1d-bullet::before{content:'•';position:absolute;left:1px;color:var(--ac)}
.is1d-table-wrap{overflow-x:auto;margin:7px 0}.is1d-table{width:100%;border-collapse:collapse;font-size:11px;white-space:nowrap}.is1d-table th,.is1d-table td{padding:5px 7px;border-bottom:1px solid var(--border,#232733);text-align:right}.is1d-table th:first-child,.is1d-table td:first-child{text-align:left}.is1d-table th{color:var(--muted,#8089a0);font-weight:700;background:var(--bg2,#0f1117)}
.is1d-response-meta{display:flex;align-items:center;gap:6px;margin-top:8px;padding-top:7px;border-top:1px solid var(--border,#232733);color:var(--dim,#687086);font-size:10px}
.is1d-fb{display:flex;align-items:center;gap:2px;margin-top:6px}.is1d-fbb{width:28px;height:25px;display:grid;place-items:center;background:none;border:0;color:var(--dim,#687086);cursor:pointer;border-radius:5px}.is1d-fbb:hover,.is1d-fbb.on{background:var(--bg2,#0f1117);color:var(--text,#e6e8ed)}.is1d-fbb:disabled{cursor:default}.is1d-thanks{font-size:10px;color:var(--dim,#687086);margin-left:3px}
.is1d-status{align-self:flex-start;display:flex;align-items:center;gap:7px;color:var(--muted,#8089a0);font-size:11px;padding:3px 4px}.is1d-status::before{content:'';width:7px;height:7px;border:2px solid var(--border2,#2a2f3d);border-top-color:var(--ac);border-radius:50%;animation:is1d-spin .7s linear infinite}@keyframes is1d-spin{to{transform:rotate(360deg)}}
.is1d-error-actions{margin-top:8px}.is1d-retry{display:inline-flex;align-items:center;gap:5px;height:28px;border:1px solid #ef44445c;border-radius:5px;background:transparent;color:#fecaca;font:700 10.5px inherit;cursor:pointer;padding:0 9px}
.is1d-prompts{padding:0 14px 11px;border-top:1px solid var(--border,#232733)}.is1d-prompts-label{padding:8px 0 6px;color:var(--dim,#687086);font-size:9.5px;font-weight:800;text-transform:uppercase;letter-spacing:.5px}
.is1d-chips{display:grid;grid-template-columns:1fr 1fr;gap:6px}.is1d-chip{min-width:0;text-align:left;background:var(--bg2,#0f1117);border:1px solid var(--border2,#2a2f3d);color:var(--muted,#8089a0);border-radius:6px;padding:7px 9px;font:600 10.5px/1.35 inherit;cursor:pointer;transition:border-color .15s,color .15s,transform .15s}
.is1d-chip:hover{color:var(--text,#e6e8ed);border-color:color-mix(in srgb,var(--ac) 58%,var(--border));transform:translateY(-1px)}
.is1d-form{display:flex;gap:7px;padding:10px 14px calc(10px + env(safe-area-inset-bottom));border-top:1px solid var(--border,#232733);background:var(--card,#14171f)}
.is1d-form input{flex:1;min-width:0;height:38px;background:var(--bg2,#0f1117);border:1px solid var(--border,#232733);border-radius:6px;color:var(--text,#e6e8ed);padding:0 11px;font:500 12.5px inherit}.is1d-form input:focus{outline:none;border-color:var(--ac,#3b82f6);box-shadow:0 0 0 2px color-mix(in srgb,var(--ac) 16%,transparent)}
.is1d-send{width:40px;height:38px;display:grid;place-items:center;background:var(--ac,#3b82f6);border:0;border-radius:6px;color:#fff;cursor:pointer}.is1d-send:disabled{opacity:.5;cursor:wait}
a.is1d-tk{display:inline-block;background:#3b82f61f;border:1px solid #3b82f64a;color:#93c5fd;border-radius:4px;padding:0 4px;font-weight:800;font-size:11.5px;text-decoration:none}a.is1d-tk:hover{background:#3b82f638}
#is1-ask-sel{position:absolute;z-index:9002;display:none;align-items:center;gap:5px;background:var(--text,#e7e9ee);color:var(--bg,#0b0d12);border:0;border-radius:6px;padding:6px 10px;font:700 10.5px/1 'Sarabun',sans-serif;cursor:pointer;box-shadow:0 6px 20px #0008}
@media(max-width:700px){#is1-dock-btn{right:12px;bottom:76px}.is1s-mobile-modules #is1-dock-btn,.is1s-mobile-context #is1-dock-btn{display:none!important}#is1-dock{left:0;right:0;bottom:0;width:auto;max-width:none;height:calc(100dvh - 55px);max-height:calc(100dvh - 55px);border-radius:8px 8px 0 0}.is1d-chips{grid-template-columns:1fr}.is1d-tab{font-size:10.5px}.is1d-tab svg{display:none}}
@media(prefers-reduced-motion:reduce){#is1-dock.open,.is1d-msg,.is1d-empty{animation:none}.is1d-status::before{animation-duration:1.8s}}
`;
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  function el(tag, attrs, html) {
    var e = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    if (html != null) e.innerHTML = html;
    return e;
  }

  var btn = el("button", { id: "is1-dock-btn", type: "button", title: tr("chat.openTitle", "Open REX agent console") }, icon("spark", 16) + '<span>' + esc(tr("chat.openButton", "Ask REX")) + "</span>");
  var dock = el("section", { id: "is1-dock", role: "dialog", "aria-modal": "false", "aria-label": "REX agent console" });
  dock.innerHTML =
    '<div class="is1d-head"><div class="is1d-brand">' + icon("spark", 16) + '<span>REX agent console</span></div>' +
    '<div class="is1d-head-actions"><button type="button" class="is1d-icon-btn is1d-clear" title="' + esc(tr("chat.clear", "Clear this thread")) + '">' + icon("trash", 15) + '</button>' +
    '<button type="button" class="is1d-icon-btn is1d-close" title="' + esc(tr("chat.closeTitle", "Close")) + '">' + icon("close", 17) + "</button></div></div>" +
    '<div class="is1d-tabs">' + ORDER.map(function (id) {
      var a = AGENTS[id];
      return '<button type="button" class="is1d-tab" data-agent="' + id + '">' + icon(a.icon, 14) + "<span>" + a.label + "</span></button>";
    }).join("") + "</div>" +
    '<div class="is1d-sub"><div class="is1d-agent-meta"><span class="is1d-tag"></span><span class="is1d-fresh">' + icon("database", 11) + '<span></span></span></div>' +
    '<label class="is1d-rm-wrap"><span class="is1d-rm-label">' + esc(tr("chat.rmLabel", "RM")) + '</span><select class="is1d-rm">' +
    RMS.map(function (r) { return "<option>" + r + "</option>"; }).join("") + "</select></label></div>" +
    '<div class="is1d-log" aria-live="polite"></div>' +
    '<div class="is1d-prompts"><div class="is1d-prompts-label">' + esc(tr("chat.supported", "Verified prompts")) + '</div><div class="is1d-chips"></div></div>' +
    '<form class="is1d-form"><input type="text" autocomplete="off"><button type="submit" class="is1d-send" title="' + esc(tr("chat.send", "Send")) + '">' + icon("send", 16) + "</button></form>";
  var askSel = el("button", { id: "is1-ask-sel", type: "button" }, icon("spark", 12) + "<span>" + esc(tr("chat.askSelection", "Ask REX")) + "</span>");
  document.body.appendChild(btn);
  document.body.appendChild(dock);
  document.body.appendChild(askSel);

  var $ = function (sel) { return dock.querySelector(sel); };
  var log = $(".is1d-log");
  var input = $(".is1d-form input");
  var send = $(".is1d-send");
  var rmSel = $(".is1d-rm");
  var storedRm = localStorage.getItem("is1_rm") || "C";
  if (RM_ALIASES[storedRm]) storedRm = RM_ALIASES[storedRm];
  if (RMS.indexOf(storedRm) === -1) storedRm = "C";
  localStorage.setItem("is1_rm", storedRm);
  rmSel.value = storedRm;

  function thread(agent) {
    try { return JSON.parse(sessionStorage.getItem("is1_dock_thread_" + agent)) || []; }
    catch (e) { return []; }
  }
  function saveThread(agent, msgs) {
    sessionStorage.setItem("is1_dock_thread_" + agent, JSON.stringify(msgs.slice(-12)));
  }

  function linkTickers(html) {
    if (!state.tickers) return html;
    return html.replace(/\b([A-Z][A-Z0-9]{0,7})\b/g, function (m, tk, offset, source) {
      if (tk === "PF" && /^&amp;REIT\b/i.test(source.slice(offset + tk.length))) return m;
      return state.tickers.has(tk) ? '<a class="is1d-tk" href="company-summary.html?tk=' + encodeURIComponent(tk) + '">' + tk + "</a>" : m;
    });
  }
  function inlineMd(text) {
    return linkTickers(esc(text).replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>"));
  }
  function replyHtml(text) {
    var lines = String(text || "").split(/\r?\n/);
    var out = [];
    for (var i = 0; i < lines.length;) {
      if (/^\s*\|/.test(lines[i]) && i + 1 < lines.length && /^\s*\|?\s*:?-{3}/.test(lines[i + 1])) {
        var header = lines[i].trim().replace(/^\||\|$/g, "").split("|");
        i += 2;
        var rows = [];
        while (i < lines.length && /^\s*\|/.test(lines[i])) {
          rows.push(lines[i].trim().replace(/^\||\|$/g, "").split("|"));
          i += 1;
        }
        out.push('<div class="is1d-table-wrap"><table class="is1d-table"><thead><tr>' + header.map(function (v) { return "<th>" + inlineMd(v.trim()) + "</th>"; }).join("") + "</tr></thead><tbody>" + rows.map(function (row) { return "<tr>" + row.map(function (v) { return "<td>" + inlineMd(v.trim()) + "</td>"; }).join("") + "</tr>"; }).join("") + "</tbody></table></div>");
        continue;
      }
      var bullet = lines[i].match(/^\s*(?:[-*•]|\d+[.)])\s+(.*)$/);
      if (bullet) out.push('<div class="is1d-line is1d-bullet">' + inlineMd(bullet[1]) + "</div>");
      else out.push('<div class="is1d-line">' + (lines[i] ? inlineMd(lines[i]) : "&nbsp;") + "</div>");
      i += 1;
    }
    return out.join("");
  }

  function formatDate(value) {
    if (!value) return "";
    var d = new Date(value.length === 10 ? value + "T00:00:00Z" : value);
    if (isNaN(d.getTime())) return String(value).slice(0, 10);
    return d.toLocaleDateString(document.documentElement.lang === "th" ? "th-TH" : "en-GB", { day: "2-digit", month: "short", year: "numeric" });
  }
  function responseMetaText(model, meta) {
    var bits = [model || "MiniMax-M3"];
    if (meta && meta.asOf) bits.push(tr("chat.dataAsOf", "data {date}", { date: formatDate(meta.asOf) }));
    if (meta && meta.sources && meta.sources.length) bits.push(meta.sources.join(" · "));
    return bits.join(" · ");
  }

  function emptyState() {
    log.innerHTML = '<div class="is1d-empty"><div class="is1d-empty-mark">' + icon(AGENTS[state.agent].icon, 20) + '</div><strong>' +
      esc(tr("chat.emptyTitle", "Ask what this agent can verify")) + '</strong><span>' + esc(tr("chat.emptyBody", "The prompts below are limited to the data currently available.")) + "</span></div>";
  }
  function addMsg(cls, text, agent, model, meta) {
    var m = el("div", { class: "is1d-msg " + cls });
    if (cls === "bot") {
      m.innerHTML = '<div class="is1d-agent-name">' + icon(AGENTS[agent].icon, 13) + "<span>" + AGENTS[agent].label + '</span></div><div class="is1d-copy">' + replyHtml(text) + "</div>" +
        '<div class="is1d-response-meta">' + icon("database", 10) + "<span>" + esc(responseMetaText(model, meta)) + "</span></div>";
    } else {
      m.textContent = text;
    }
    log.appendChild(m);
    log.scrollTop = log.scrollHeight;
    return m;
  }
  function addError(message, retryText) {
    var m = el("div", { class: "is1d-msg err" });
    m.appendChild(document.createTextNode(message));
    if (retryText) {
      var actions = el("div", { class: "is1d-error-actions" });
      var retry = el("button", { class: "is1d-retry", type: "button" }, icon("refresh", 12) + "<span>" + esc(tr("chat.retry", "Retry")) + "</span>");
      retry.onclick = function () { m.remove(); ask(retryText, true); };
      actions.appendChild(retry);
      m.appendChild(actions);
    }
    log.appendChild(m);
    log.scrollTop = log.scrollHeight;
  }
  function attachFeedback(msgEl, agent, question, reply) {
    var bar = el("div", { class: "is1d-fb" });
    var up = el("button", { class: "is1d-fbb", type: "button", title: tr("chat.helpful", "Helpful") }, icon("thumbsUp", 13));
    var down = el("button", { class: "is1d-fbb", type: "button", title: tr("chat.notHelpful", "Not helpful") }, icon("thumbsDown", 13));
    function vote(v, voteBtn) {
      if (bar.dataset.voted) return;
      bar.dataset.voted = v;
      voteBtn.classList.add("on");
      up.disabled = down.disabled = true;
      bar.appendChild(el("span", { class: "is1d-thanks" }, esc(tr("chat.thanks", "Recorded"))));
      fetch("/api/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: "Bearer " + (localStorage.getItem("is1_chat_token") || "") },
        body: JSON.stringify({ agent: agent, vote: v, question: question, reply: reply, rm: rmSel.value }),
      }).catch(function () {});
    }
    up.onclick = function () { vote("up", up); };
    down.onclick = function () { vote("down", down); };
    bar.appendChild(up);
    bar.appendChild(down);
    msgEl.appendChild(bar);
  }

  function renderChips() {
    var box = $(".is1d-chips");
    box.innerHTML = "";
    AGENTS[state.agent].chips.forEach(function (c) {
      var text = tr(c.key, c.text, { rm: rmSel.value });
      var chip = el("button", { class: "is1d-chip", type: "button" }, esc(text));
      chip.onclick = function () { input.value = text; input.focus(); };
      box.appendChild(chip);
    });
  }
  function renderThread() {
    var msgs = thread(state.agent);
    log.innerHTML = "";
    if (!msgs.length) emptyState();
    msgs.forEach(function (m) {
      addMsg(m.role === "user" ? "user" : "bot", m.content, state.agent, m.model, m.meta);
    });
  }
  function loadFreshness(agent) {
    var requestedAgent = agent;
    var file = AGENTS[agent].data[0];
    var label = $(".is1d-fresh span");
    label.textContent = tr("chat.loadingData", "Checking data freshness");
    fetch("data/" + file + ".json").then(function (r) {
      if (!r.ok) throw new Error("missing");
      return r.json();
    }).then(function (d) {
      if (state.agent !== requestedAgent) return;
      var asOf = d.asOf || d.builtAt || d._built_at;
      label.textContent = tr("chat.freshness", "{file} · {date}", { file: file, date: formatDate(asOf) || tr("chat.available", "available") });
    }).catch(function () {
      if (state.agent === requestedAgent) label.textContent = tr("chat.dataUnavailable", "Data status unavailable");
    });
  }
  function setAgent(agent) {
    if (!AGENTS[agent] || state.busy) return;
    state.agent = agent;
    sessionStorage.setItem("is1_dock_agent", agent);
    var a = AGENTS[agent];
    dock.style.setProperty("--ac", a.color);
    dock.querySelectorAll(".is1d-tab").forEach(function (tab) { tab.classList.toggle("on", tab.dataset.agent === agent); });
    $(".is1d-tag").textContent = tr(a.tagKey, a.tag);
    input.placeholder = tr("chat.placeholder", "Ask {agent}", { agent: a.label });
    renderThread();
    renderChips();
    loadFreshness(agent);
  }

  function renderDockLabels() {
    btn.title = tr("chat.openTitle", "Open REX agent console");
    btn.querySelector("span").textContent = tr("chat.openButton", "Ask REX");
    $(".is1d-close").title = tr("chat.closeTitle", "Close");
    $(".is1d-clear").title = tr("chat.clear", "Clear this thread");
    $(".is1d-rm-label").textContent = tr("chat.rmLabel", "RM");
    $(".is1d-prompts-label").textContent = tr("chat.supported", "Verified prompts");
    send.title = tr("chat.send", "Send");
    askSel.querySelector("span").textContent = tr("chat.askSelection", "Ask REX");
    setAgent(state.agent);
  }

  function getToken(forcePrompt) {
    var token = localStorage.getItem("is1_chat_token");
    if (!token && forcePrompt) {
      token = (prompt(tr("chat.tokenPrompt", "Enter the IS1 chat access token:")) || "").trim();
      if (token) localStorage.setItem("is1_chat_token", token);
    }
    return token;
  }
  function statusTicker(agent) {
    var files = AGENTS[agent].data;
    var i = 0;
    var s = el("div", { class: "is1d-status" }, esc(tr("chat.reading", "Reading {file}", { file: files[0] })));
    log.appendChild(s);
    log.scrollTop = log.scrollHeight;
    var iv = setInterval(function () {
      i += 1;
      s.textContent = i < files.length ? tr("chat.reading", "Reading {file}", { file: files[i] }) : tr("chat.thinking", "Checking the answer");
      if (i >= files.length) clearInterval(iv);
    }, 700);
    return { stop: function () { clearInterval(iv); s.remove(); } };
  }
  function setBusy(on, agent) {
    state.busy = on;
    state.busyAgent = on ? agent : null;
    send.disabled = on;
    input.disabled = on;
    dock.querySelectorAll(".is1d-tab").forEach(function (tab) { tab.disabled = on; });
  }
  function ask(text, reusePending) {
    var clean = String(text || "").trim();
    if (state.busy || !clean) return;
    var token = getToken(true);
    if (!token) { addError(tr("chat.noToken", "No access token entered.")); return; }
    var agent = state.agent;
    var msgs = thread(agent);
    var pending = reusePending && msgs.length && msgs[msgs.length - 1].role === "user" && msgs[msgs.length - 1].content === clean;
    if (!pending) {
      msgs.push({ role: "user", content: clean });
      saveThread(agent, msgs);
      if (log.querySelector(".is1d-empty")) log.innerHTML = "";
      addMsg("user", clean);
    }
    input.value = "";
    setBusy(true, agent);
    var status = statusTicker(agent);
    fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: "Bearer " + token },
      body: JSON.stringify({ agent: agent, messages: msgs, rm: rmSel.value }),
    }).then(function (r) {
      return r.json().catch(function () { return { error: "HTTP " + r.status }; }).then(function (data) {
        if (r.status === 401) localStorage.removeItem("is1_chat_token");
        if (!r.ok || data.error) throw new Error(data.error || "HTTP " + r.status);
        return data;
      });
    }).then(function (d) {
      msgs.push({ role: "assistant", content: d.reply, model: d.model, meta: d.meta || null });
      saveThread(agent, msgs);
      status.stop();
      if (state.agent === agent) {
        var bot = addMsg("bot", d.reply, agent, d.model, d.meta);
        attachFeedback(bot, agent, clean, d.reply);
      }
    }).catch(function (error) {
      status.stop();
      if (state.agent === agent) addError(error.message, clean);
    }).finally(function () {
      setBusy(false, null);
      input.focus();
    });
  }

  function openDock(agent, prefill) {
    state.open = true;
    dock.classList.add("open");
    btn.style.display = "none";
    setAgent(agent && AGENTS[agent] ? agent : state.agent);
    if (prefill) input.value = prefill;
    input.focus();
    if (!state.tickers) {
      fetch("data/tickers.json").then(function (r) { return r.json(); }).then(function (d) {
        state.tickers = new Set((d.tickers || []).map(function (t) { return t.tk; }));
        if (state.open) renderThread();
      }).catch(function () { state.tickers = new Set(); });
    }
  }
  function closeDock() {
    state.open = false;
    dock.classList.remove("open");
    btn.style.display = "flex";
  }

  btn.onclick = function () { openDock(); };
  $(".is1d-close").onclick = closeDock;
  $(".is1d-clear").onclick = function () {
    if (state.busy) return;
    sessionStorage.removeItem("is1_dock_thread_" + state.agent);
    renderThread();
  };
  dock.querySelectorAll(".is1d-tab").forEach(function (tab) { tab.onclick = function () { setAgent(tab.dataset.agent); }; });
  $(".is1d-form").onsubmit = function (event) { event.preventDefault(); ask(input.value); };
  rmSel.onchange = function () { localStorage.setItem("is1_rm", rmSel.value); renderChips(); };
  document.addEventListener("keydown", function (event) { if (event.key === "Escape" && state.open) closeDock(); });
  window.addEventListener("i18n:change", renderDockLabels);

  document.addEventListener("mouseup", function (event) {
    if (dock.contains(event.target) || event.target === askSel || askSel.contains(event.target)) return;
    setTimeout(function () {
      var selection = window.getSelection();
      var text = selection ? String(selection).trim() : "";
      if (text && text.length >= 2 && text.length <= 120 && selection.rangeCount) {
        var rect = selection.getRangeAt(0).getBoundingClientRect();
        askSel.style.left = Math.max(8, rect.left + window.scrollX + rect.width / 2 - 38) + "px";
        askSel.style.top = rect.bottom + window.scrollY + 6 + "px";
        askSel.style.display = "flex";
        askSel.dataset.q = text;
      } else askSel.style.display = "none";
    }, 0);
  });
  askSel.onclick = function () {
    var question = askSel.dataset.q || "";
    askSel.style.display = "none";
    window.getSelection().removeAllRanges();
    openDock(state.agent, tr("chat.tellMeAbout", "Explain this from the available dashboard data: {text}", { text: question }));
  };

  setAgent(state.agent);
  window.IS1Dock = { open: openDock, close: closeDock };
})();
