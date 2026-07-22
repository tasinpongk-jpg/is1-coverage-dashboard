/**
 * IS1 agent dock — floating chat with the named coverage agents.
 *
 * Included by every dashboard page (<script src="chat-dock.js" defer>).
 * Talks to POST /api/chat (worker.js). Self-contained: injects its own CSS,
 * no dependencies.
 *
 * Features:
 *  - agent tabs (Hermes / Atlas / Pythia), separate thread per agent,
 *    threads survive page navigation via sessionStorage
 *  - RM picker ("I'm C") in localStorage -> personalized suggestion chips
 *  - status lines while waiting ("reading external-news…") matching the
 *    snapshots each agent is grounded in
 *  - ticker symbols in replies become chips linking to company-summary.html
 *  - select any text on a page -> floating "✦ ask" button prefills the dock
 *  - token-gated like the old chat card: localStorage is1_chat_token
 *  - window.IS1Dock.open(agent, prefill) for "Meet the team" cards
 */
(function () {
  "use strict";

  var AGENTS = {
    hermes: {
      label: "Hermes", emoji: "⚡", color: "#f59e0b",
      tag: "News messenger — catalysts, disclosures, Oppday",
      tagKey: "chat.hermes.tag",
      data: ["external-news", "disclosure-pulse", "oppday-minutes"],
      chips: [
        { key: "chat.hermes.chip.news", text: "What news moved my names today? I'm {rm}." },
        { key: "chat.hermes.chip.silent", text: "Any overdue or silent filers in my coverage? I'm {rm}." },
        { key: "chat.hermes.chip.cpn", text: "Show CPN's latest SET filings and filing dates." },
        { key: "chat.hermes.chip.food", text: "อัปเดตข่าวกลุ่ม FOOD วันนี้" },
      ],
    },
    atlas: {
      label: "Atlas", emoji: "🗺", color: "#3b82f6",
      tag: "Market data — movers, alerts, threshold checks",
      tagKey: "chat.atlas.tag",
      data: ["morning-brief", "tickers", "unusual-trading"],
      chips: [
        { key: "chat.atlas.chip.movers", text: "Top movers beyond ±2% in my coverage. I'm {rm}." },
        { key: "chat.atlas.chip.alerts", text: "Any high-severity alerts today? I'm {rm}." },
        { key: "chat.atlas.chip.low", text: "Which names hit a 52-week low?" },
      ],
    },
    pythia: {
      label: "Pythia", emoji: "🔮", color: "#8b5cf6",
      tag: "Macro & sectors — breadth, commentary",
      tagKey: "chat.pythia.tag",
      data: ["morning-brief", "ai-insights"],
      chips: [
        { key: "chat.pythia.chip.sector", text: "Which sector leads and which lags today?" },
        { key: "chat.pythia.chip.prop", text: "What should I watch in PROP this week?" },
        { key: "chat.pythia.chip.market", text: "สรุปภาพรวมตลาดวันนี้" },
      ],
    },
    lex: {
      label: "Lex", emoji: "⚖️", color: "#10b981",
      tag: "Rules & regulations — answers cited to the source PDF & page",
      tagKey: "chat.lex.tag",
      data: ["regulations"],
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
    tickers: null, // Set of covered symbols, lazy-loaded
  };

  function tr(key, fallback, vars) {
    var s = window.I18N && typeof window.I18N.t === "function" ? window.I18N.t(key) : fallback;
    if (s === key) s = fallback;
    return String(s).replace(/\{(\w+)\}/g, function (_, k) {
      return vars && vars[k] != null ? vars[k] : "";
    });
  }

  // ---------------------------------------------------------------- css
  var css = "\
#is1-dock-btn{position:fixed;right:18px;bottom:18px;z-index:9000;display:flex;align-items:center;gap:8px;\
 background:linear-gradient(135deg,#3b82f6,#8b5cf6);color:#fff;border:none;border-radius:999px;\
 padding:11px 18px;font:600 13px/1 'Inter','Segoe UI',system-ui,sans-serif;cursor:pointer;\
 box-shadow:0 6px 24px #0008;transition:transform .15s}\
#is1-dock-btn:hover{transform:translateY(-2px)}\
#is1-dock{position:fixed;right:18px;bottom:18px;z-index:9001;width:400px;max-width:calc(100vw - 24px);\
 height:560px;max-height:calc(100vh - 40px);display:none;flex-direction:column;\
 background:var(--card,#14171f);border:1px solid var(--border2,#2a2f3d);border-radius:14px;\
 box-shadow:0 12px 48px #000a;font-family:'Inter','Segoe UI',system-ui,sans-serif;overflow:hidden}\
#is1-dock.open{display:flex}\
.is1d-tabs{display:flex;border-bottom:1px solid var(--border,#232733);background:var(--bg2,#0f1117)}\
.is1d-tab{flex:1;padding:11px 4px;text-align:center;cursor:pointer;border:none;background:none;\
 color:var(--muted,#8089a0);font:600 12.5px/1 inherit;border-bottom:2px solid transparent}\
.is1d-tab.on{color:var(--text,#e6e8ed);border-bottom-color:var(--ac,#3b82f6)}\
.is1d-close{border:none;background:none;color:var(--muted,#8089a0);font-size:15px;cursor:pointer;padding:0 12px}\
.is1d-sub{display:flex;align-items:center;justify-content:space-between;gap:8px;\
 padding:8px 14px;border-bottom:1px solid var(--border,#232733);font-size:11px;color:var(--muted,#8089a0)}\
.is1d-sub select{background:var(--bg2,#0f1117);color:var(--text,#e6e8ed);border:1px solid var(--border,#232733);\
 border-radius:6px;font:inherit;font-size:11px;padding:3px 6px}\
.is1d-log{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px}\
.is1d-msg{max-width:88%;padding:9px 12px;border-radius:10px;font-size:13px;line-height:1.5;\
 white-space:pre-wrap;word-break:break-word}\
.is1d-msg.user{align-self:flex-end;background:#1d4ed833;border:1px solid #1d4ed855;color:var(--text,#e6e8ed)}\
.is1d-msg.bot{align-self:flex-start;background:var(--card2,#1a1d27);border:1px solid var(--border,#232733);color:var(--text,#e6e8ed)}\
.is1d-fb{display:flex;gap:4px;margin-top:7px;opacity:.5;transition:opacity .15s}\
.is1d-msg.bot:hover .is1d-fb{opacity:.9}\
.is1d-fbb{background:none;border:none;cursor:pointer;font-size:13px;line-height:1;padding:2px 5px;border-radius:6px;filter:grayscale(.5)}\
.is1d-fbb:hover{background:var(--bg2,#0f1117);filter:none}\
.is1d-fbb.on{filter:none;background:var(--bg2,#0f1117)}\
.is1d-fbb:disabled{cursor:default}\
.is1d-fb .thanks{font-size:10.5px;color:var(--dim,#5a627a);align-self:center;margin-left:2px}\
.is1d-msg.err{align-self:center;color:#f87171;font-size:12px;background:none}\
.is1d-msg .agent-name{display:block;font-size:10.5px;font-weight:700;letter-spacing:.4px;\
 text-transform:uppercase;color:var(--ac,#3b82f6);margin-bottom:3px}\
.is1d-status{align-self:flex-start;color:var(--dim,#5a627a);font-size:11.5px;font-style:italic;padding:0 4px}\
.is1d-chips{display:flex;flex-wrap:wrap;gap:6px;padding:0 14px 10px}\
.is1d-chip{background:var(--bg2,#0f1117);border:1px solid var(--border2,#2a2f3d);color:var(--muted,#8089a0);\
 border-radius:999px;padding:5px 11px;font:500 11.5px/1.3 inherit;cursor:pointer}\
.is1d-chip:hover{color:var(--text,#e6e8ed);border-color:var(--ac,#3b82f6)}\
.is1d-form{display:flex;gap:8px;padding:11px 14px;border-top:1px solid var(--border,#232733)}\
.is1d-form input{flex:1;background:var(--bg2,#0f1117);border:1px solid var(--border,#232733);border-radius:8px;\
 color:var(--text,#e6e8ed);padding:9px 12px;font:inherit;font-size:13px}\
.is1d-form input:focus{outline:none;border-color:var(--ac,#3b82f6)}\
.is1d-form button{background:var(--ac,#3b82f6);border:none;border-radius:8px;color:#fff;\
 padding:0 16px;font:600 13px/1 inherit;cursor:pointer}\
.is1d-form button:disabled{opacity:.5;cursor:wait}\
a.is1d-tk{display:inline-block;background:#3b82f622;border:1px solid #3b82f655;color:#93c5fd;\
 border-radius:5px;padding:0 5px;font-weight:700;font-size:12px;text-decoration:none}\
a.is1d-tk:hover{background:#3b82f644}\
#is1-ask-sel{position:absolute;z-index:9002;background:linear-gradient(135deg,#3b82f6,#8b5cf6);color:#fff;\
 border:none;border-radius:999px;padding:5px 12px;font:600 11.5px/1 'Inter',system-ui,sans-serif;\
 cursor:pointer;box-shadow:0 4px 16px #0008;display:none}\
@media(max-width:640px){#is1-dock{right:0;bottom:0;width:100vw;max-width:100vw;height:100dvh;\
 max-height:100dvh;border-radius:0}}";
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  // ---------------------------------------------------------------- dom
  function el(tag, attrs, html) {
    var e = document.createElement(tag);
    for (var k in attrs || {}) e.setAttribute(k, attrs[k]);
    if (html != null) e.innerHTML = html;
    return e;
  }

  var btn = el("button", { id: "is1-dock-btn", title: tr("chat.openTitle", "Ask the IS1 agents") }, tr("chat.openButton", "✦ Ask the agents"));
  var dock = el("div", { id: "is1-dock" });
  dock.innerHTML =
    '<div class="is1d-tabs">' +
    ORDER.map(function (a) {
      return '<button class="is1d-tab" data-agent="' + a + '">' +
        AGENTS[a].emoji + " " + AGENTS[a].label + "</button>";
    }).join("") +
    '<button class="is1d-close" title="' + esc(tr("chat.closeTitle", "close")) + '">✕</button></div>' +
    '<div class="is1d-sub"><span class="is1d-tag"></span>' +
    '<label><span class="is1d-rm-label">' + esc(tr("chat.rmLabel", "I'm")) + '</span> <select class="is1d-rm">' +
    RMS.map(function (r) { return "<option>" + r + "</option>"; }).join("") +
    "</select></label></div>" +
    '<div class="is1d-log"></div>' +
    '<div class="is1d-chips"></div>' +
    '<form class="is1d-form"><input type="text" autocomplete="off">' +
    '<button type="submit">' + esc(tr("chat.send", "send")) + "</button></form>";
  var askSel = el("button", { id: "is1-ask-sel" }, tr("chat.askSelection", "✦ ask"));
  document.body.appendChild(btn);
  document.body.appendChild(dock);
  document.body.appendChild(askSel);

  var $ = function (sel) { return dock.querySelector(sel); };
  var log = $(".is1d-log"), input = $(".is1d-form input"), send = $(".is1d-form button");
  var rmSel = $(".is1d-rm");
  var storedRm = localStorage.getItem("is1_rm") || "C";
  if (RM_ALIASES[storedRm]) {
    storedRm = RM_ALIASES[storedRm];
    localStorage.setItem("is1_rm", storedRm);
  }
  if (RMS.indexOf(storedRm) === -1) {
    storedRm = "C";
    localStorage.setItem("is1_rm", storedRm);
  }
  rmSel.value = storedRm;
  rmSel.onchange = function () { localStorage.setItem("is1_rm", rmSel.value); renderChips(); };

  function renderDockLabels() {
    btn.title = tr("chat.openTitle", "Ask the IS1 agents");
    btn.textContent = tr("chat.openButton", "✦ Ask the agents");
    $(".is1d-close").title = tr("chat.closeTitle", "close");
    $(".is1d-rm-label").textContent = tr("chat.rmLabel", "I'm");
    send.textContent = tr("chat.send", "send");
    askSel.textContent = tr("chat.askSelection", "✦ ask");
    if (state.open) {
      var a = AGENTS[state.agent];
      $(".is1d-tag").textContent = tr(a.tagKey, a.tag);
      input.placeholder = tr("chat.placeholder", "ask {agent}…", { agent: a.label.toLowerCase() });
      renderChips();
    }
  }

  // ---------------------------------------------------------------- threads
  function thread(agent) {
    try { return JSON.parse(sessionStorage.getItem("is1_dock_thread_" + agent)) || []; }
    catch (e) { return []; }
  }
  function saveThread(agent, msgs) {
    sessionStorage.setItem("is1_dock_thread_" + agent, JSON.stringify(msgs.slice(-12)));
  }

  // ---------------------------------------------------------------- render
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function md(s) { // escape, then bold + ticker chips
    var h = esc(s).replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>");
    if (state.tickers) {
      h = h.replace(/\b([A-Z][A-Z0-9]{0,7})\b/g, function (m, tk) {
        return state.tickers.has(tk)
          ? '<a class="is1d-tk" href="company-summary.html?tk=' + tk + '">' + tk + "</a>" : m;
      });
    }
    return h;
  }
  function addMsg(cls, text, agent) {
    var m = el("div", { class: "is1d-msg " + cls });
    m.innerHTML = (cls === "bot" && agent
      ? '<span class="agent-name">' + AGENTS[agent].emoji + " " + AGENTS[agent].label + "</span>" : "") +
      (cls === "bot" ? md(text) : esc(text));
    log.appendChild(m);
    log.scrollTop = log.scrollHeight;
    return m;
  }
  // 👍/👎 under a live bot reply -> POST /api/feedback (failing answers become
  // training data). Only on fresh replies, not restored thread history.
  function attachFeedback(msgEl, agent, question, reply) {
    var bar = el("div", { class: "is1d-fb" });
    var up = el("button", { class: "is1d-fbb", type: "button", title: tr("chat.helpful", "helpful") }, "👍");
    var down = el("button", { class: "is1d-fbb", type: "button", title: tr("chat.notHelpful", "not helpful") }, "👎");
    function vote(v, btn) {
      if (bar.dataset.voted) return;
      bar.dataset.voted = v;
      btn.classList.add("on");
      up.disabled = down.disabled = true;
      bar.appendChild(el("span", { class: "thanks" }, tr("chat.thanks", "thanks")));
      var token = localStorage.getItem("is1_chat_token") || "";
      fetch("/api/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json", Authorization: "Bearer " + token },
        body: JSON.stringify({ agent: agent, vote: v, question: question, reply: reply, rm: rmSel.value }),
      }).catch(function () { /* feedback is best-effort */ });
    }
    up.onclick = function () { vote("up", up); };
    down.onclick = function () { vote("down", down); };
    bar.appendChild(up); bar.appendChild(down);
    msgEl.appendChild(bar);
  }
  function renderChips() {
    var rm = rmSel.value, box = $(".is1d-chips");
    box.innerHTML = "";
    AGENTS[state.agent].chips.forEach(function (c) {
      var chip = el("button", { class: "is1d-chip", type: "button" }, esc(tr(c.key, c.text, { rm: rm })));
      chip.onclick = function () { input.value = chip.textContent; input.focus(); };
      box.appendChild(chip);
    });
  }
  function setAgent(agent) {
    state.agent = agent;
    sessionStorage.setItem("is1_dock_agent", agent);
    var a = AGENTS[agent];
    dock.style.setProperty("--ac", a.color);
    dock.querySelectorAll(".is1d-tab").forEach(function (t) {
      t.classList.toggle("on", t.dataset.agent === agent);
    });
    $(".is1d-tag").textContent = tr(a.tagKey, a.tag);
    input.placeholder = tr("chat.placeholder", "ask {agent}…", { agent: a.label.toLowerCase() });
    log.innerHTML = "";
    thread(agent).forEach(function (m) {
      addMsg(m.role === "user" ? "user" : "bot", m.content, agent);
    });
    renderChips();
  }

  // ---------------------------------------------------------------- token
  function getToken(forcePrompt) {
    var t = localStorage.getItem("is1_chat_token");
    if (!t && forcePrompt) {
      t = (prompt(tr("chat.tokenPrompt", "Enter the IS1 chat access token (ask your team lead):")) || "").trim();
      if (t) localStorage.setItem("is1_chat_token", t);
    }
    return t;
  }

  // ---------------------------------------------------------------- send
  function statusTicker(agent) {
    var files = AGENTS[agent].data, i = 0;
    var s = el("div", { class: "is1d-status" }, tr("chat.reading", "reading {file}…", { file: files[0] }));
    log.appendChild(s);
    log.scrollTop = log.scrollHeight;
    var iv = setInterval(function () {
      i += 1;
      s.textContent = i < files.length ? tr("chat.reading", "reading {file}…", { file: files[i] }) : tr("chat.thinking", "thinking…");
      if (i >= files.length) clearInterval(iv);
    }, 700);
    return { el: s, stop: function () { clearInterval(iv); s.remove(); } };
  }

  function ask(text) {
    if (state.busy || !text.trim()) return;
    var token = getToken(true);
    if (!token) { addMsg("err", tr("chat.noToken", "No token entered — chat is token-gated.")); return; }
    var agent = state.agent;
    var msgs = thread(agent);
    msgs.push({ role: "user", content: text.trim() });
    saveThread(agent, msgs);
    addMsg("user", text.trim());
    input.value = "";
    state.busy = true; send.disabled = true;
    var status = statusTicker(agent);
    fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: "Bearer " + token },
      body: JSON.stringify({ agent: agent, messages: msgs, rm: rmSel.value }),
    }).then(function (r) {
      if (r.status === 401) {
        localStorage.removeItem("is1_chat_token");
        throw new Error(tr("chat.wrongToken", "Wrong token — it has been forgotten; send again to retry."));
      }
      return r.json();
    }).then(function (d) {
      if (d.error) throw new Error(d.error);
      msgs.push({ role: "assistant", content: d.reply });
      saveThread(agent, msgs);
      status.stop();
      var bot = addMsg("bot", d.reply, agent);
      attachFeedback(bot, agent, text.trim(), d.reply);
    }).catch(function (e) {
      status.stop();
      addMsg("err", e.message);
    }).finally(function () {
      state.busy = false; send.disabled = false;
    });
  }

  // ---------------------------------------------------------------- wiring
  btn.onclick = function () { openDock(); };
  $(".is1d-close").onclick = function () { closeDock(); };
  dock.querySelectorAll(".is1d-tab").forEach(function (t) {
    t.onclick = function () { setAgent(t.dataset.agent); };
  });
  $(".is1d-form").onsubmit = function (e) { e.preventDefault(); ask(input.value); };
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && state.open) closeDock();
  });
  window.addEventListener("i18n:change", renderDockLabels);

  function openDock(agent, prefill) {
    state.open = true;
    dock.classList.add("open");
    btn.style.display = "none";
    if (agent && AGENTS[agent]) setAgent(agent); else setAgent(state.agent);
    if (prefill) input.value = prefill;
    input.focus();
    if (!state.tickers) {
      fetch("data/tickers.json").then(function (r) { return r.json(); }).then(function (d) {
        state.tickers = new Set((d.tickers || []).map(function (t) { return t.tk; }));
      }).catch(function () { state.tickers = new Set(); });
    }
  }
  function closeDock() {
    state.open = false;
    dock.classList.remove("open");
    btn.style.display = "flex";
  }

  // select text anywhere -> "✦ ask" bubble
  document.addEventListener("mouseup", function (e) {
    if (dock.contains(e.target) || e.target === askSel) return;
    setTimeout(function () {
      var sel = window.getSelection();
      var text = sel ? String(sel).trim() : "";
      if (text && text.length >= 2 && text.length <= 80 && sel.rangeCount) {
        var r = sel.getRangeAt(0).getBoundingClientRect();
        askSel.style.left = Math.max(8, r.left + window.scrollX + r.width / 2 - 28) + "px";
        askSel.style.top = (r.bottom + window.scrollY + 6) + "px";
        askSel.style.display = "block";
        askSel.dataset.q = text;
      } else {
        askSel.style.display = "none";
      }
    }, 0);
  });
  askSel.onclick = function () {
    var q = askSel.dataset.q || "";
    askSel.style.display = "none";
    window.getSelection().removeAllRanges();
    openDock(state.agent, tr("chat.tellMeAbout", "Tell me about {text}", { text: q }));
  };

  window.IS1Dock = { open: openDock };
})();
