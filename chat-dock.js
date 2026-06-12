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
 *  - RM picker ("I'm Champ") in localStorage -> personalized suggestion chips
 *  - status lines while waiting ("reading external-news…") matching the
 *    snapshots each agent is grounded in
 *  - ticker symbols in replies become chips linking to ticker-summary.html
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
      data: ["external-news", "disclosure-pulse", "oppday-minutes"],
      chips: [
        "What news moved my names today? I'm {rm}.",
        "Any overdue or silent filers in my coverage? I'm {rm}.",
        "อัปเดตข่าวกลุ่ม FOOD วันนี้",
      ],
    },
    atlas: {
      label: "Atlas", emoji: "🗺", color: "#3b82f6",
      tag: "Market data — movers, alerts, threshold checks",
      data: ["morning-brief", "tickers", "unusual-trading"],
      chips: [
        "Top movers beyond ±2% in my coverage. I'm {rm}.",
        "Any high-severity alerts today? I'm {rm}.",
        "Which names hit a 52-week low?",
      ],
    },
    pythia: {
      label: "Pythia", emoji: "🔮", color: "#8b5cf6",
      tag: "Macro & sectors — overlays, breadth, commentary",
      data: ["macro-overlays", "morning-brief", "ai-insights"],
      chips: [
        "Which sector leads and which lags today?",
        "What macro prints matter for PROP this week?",
        "สรุปภาพรวมตลาดวันนี้",
      ],
    },
  };
  var ORDER = ["hermes", "atlas", "pythia"];
  var RMS = ["Champ", "Kae", "Orn", "Gift", "Pim", "Tony"];

  var state = {
    open: false,
    agent: sessionStorage.getItem("is1_dock_agent") || "hermes",
    busy: false,
    tickers: null, // Set of covered symbols, lazy-loaded
  };

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

  var btn = el("button", { id: "is1-dock-btn", title: "Ask the IS1 agents" }, "✦ Ask the agents");
  var dock = el("div", { id: "is1-dock" });
  dock.innerHTML =
    '<div class="is1d-tabs">' +
    ORDER.map(function (a) {
      return '<button class="is1d-tab" data-agent="' + a + '">' +
        AGENTS[a].emoji + " " + AGENTS[a].label + "</button>";
    }).join("") +
    '<button class="is1d-close" title="close">✕</button></div>' +
    '<div class="is1d-sub"><span class="is1d-tag"></span>' +
    '<label>I\'m <select class="is1d-rm">' +
    RMS.map(function (r) { return "<option>" + r + "</option>"; }).join("") +
    "</select></label></div>" +
    '<div class="is1d-log"></div>' +
    '<div class="is1d-chips"></div>' +
    '<form class="is1d-form"><input type="text" autocomplete="off">' +
    "<button type=\"submit\">send</button></form>";
  var askSel = el("button", { id: "is1-ask-sel" }, "✦ ask");
  document.body.appendChild(btn);
  document.body.appendChild(dock);
  document.body.appendChild(askSel);

  var $ = function (sel) { return dock.querySelector(sel); };
  var log = $(".is1d-log"), input = $(".is1d-form input"), send = $(".is1d-form button");
  var rmSel = $(".is1d-rm");
  rmSel.value = localStorage.getItem("is1_rm") || "Champ";
  rmSel.onchange = function () { localStorage.setItem("is1_rm", rmSel.value); renderChips(); };

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
      h = h.replace(/\b([A-Z][A-Z0-9]{1,7})\b/g, function (m, tk) {
        return state.tickers.has(tk)
          ? '<a class="is1d-tk" href="ticker-summary.html?tk=' + tk + '">' + tk + "</a>" : m;
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
  function renderChips() {
    var rm = rmSel.value, box = $(".is1d-chips");
    box.innerHTML = "";
    AGENTS[state.agent].chips.forEach(function (c) {
      var chip = el("button", { class: "is1d-chip", type: "button" }, esc(c.replace("{rm}", rm)));
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
    $(".is1d-tag").textContent = a.tag;
    input.placeholder = "ask " + a.label.toLowerCase() + "…";
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
      t = (prompt("Enter the IS1 chat access token (ask Champ):") || "").trim();
      if (t) localStorage.setItem("is1_chat_token", t);
    }
    return t;
  }

  // ---------------------------------------------------------------- send
  function statusTicker(agent) {
    var files = AGENTS[agent].data, i = 0;
    var s = el("div", { class: "is1d-status" }, "reading " + files[0] + "…");
    log.appendChild(s);
    log.scrollTop = log.scrollHeight;
    var iv = setInterval(function () {
      i += 1;
      s.textContent = i < files.length ? "reading " + files[i] + "…" : "thinking…";
      if (i >= files.length) clearInterval(iv);
    }, 700);
    return { el: s, stop: function () { clearInterval(iv); s.remove(); } };
  }

  function ask(text) {
    if (state.busy || !text.trim()) return;
    var token = getToken(true);
    if (!token) { addMsg("err", "No token entered — chat is token-gated."); return; }
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
      body: JSON.stringify({ agent: agent, messages: msgs }),
    }).then(function (r) {
      if (r.status === 401) {
        localStorage.removeItem("is1_chat_token");
        throw new Error("Wrong token — it has been forgotten; send again to retry.");
      }
      return r.json();
    }).then(function (d) {
      if (d.error) throw new Error(d.error);
      msgs.push({ role: "assistant", content: d.reply });
      saveThread(agent, msgs);
      status.stop();
      addMsg("bot", d.reply, agent);
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
    openDock(state.agent, "Tell me about " + q);
  };

  window.IS1Dock = { open: openDock };
})();
