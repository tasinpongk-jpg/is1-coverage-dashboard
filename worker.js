/**
 * IS1 coverage dashboard worker.
 *
 * Static assets are served by the assets pipeline (this code only runs for
 * paths that don't match an asset). One API route:
 *
 *   POST /api/chat   { agent: "atlas"|"hermes"|"pythia", messages: [...] }
 *     -> { reply: "...", agent: "...", model: "..." }
 *
 * Three named agents, each grounded in a different slice of the daily
 * snapshot JSONs (read back from the deployed assets, so they always answer
 * from the same data the dashboard shows):
 *
 *   atlas  — market data: prices, movers, alerts, strict threshold math
 *   hermes — news messenger: external news, disclosures, oppday minutes
 *   pythia — macro/sector: AI commentary, sector aggregates
 *
 * Gated by a shared token: Authorization: Bearer <CHAT_TOKEN worker secret>.
 * Inference: Cloudflare Workers AI (free-tier neuron allocation).
 */

const CHAT_MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast";
const MAX_HISTORY = 12; // user+assistant turns kept from the client
const MAX_USER_CHARS = 2000;

// Lex — the rules & regulations agent. Unlike the other three, it does NOT use
// Workers AI: Gemini File Search does the retrieval AND generation over the
// regulation PDFs indexed by scripts/index_regulations.py, returning page-level
// citations. The store name is read from data/regulations-index.json (built by
// that script); only the GEMINI_API_KEY is a worker secret.
const LEX_MODEL = "gemini-2.5-flash"; // generation model; bump as newer flash ships
const LEX_SYSTEM =
  "You are Lex, the rules & regulations agent on the IS1 coverage dashboard. " +
  "You answer questions about SET/SEC listing rules, disclosure obligations and " +
  "related Thai securities regulation, using ONLY the regulation documents " +
  "retrieved for you. If the documents do not cover the question, say so plainly " +
  "— never guess or cite outside knowledge. Be concise and quote the rule's own " +
  "wording where it matters. Reply in the user's language (Thai or English). " +
  "You are not a lawyer; surface what the documents say, not legal advice.\n" +
  "ANSWER SHAPE: lead with the direct answer in one line, then the basis — the " +
  "rule's own wording (quoted) and any numeric trigger (thresholds, %, day " +
  "counts, deadlines) stated EXACTLY as written. If conditions or exemptions " +
  "apply, list them as short bullets. If two retrieved rules differ or the " +
  "documents are ambiguous, say so rather than smoothing it over. When the " +
  "answer hinges on a defined term (e.g. 'connected person', 'material'), give " +
  "the document's definition before applying it. The page-level citations are " +
  "appended automatically — do not fabricate rule or clause numbers.";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/chat") {
      if (request.method !== "POST") {
        return json({ error: "POST only" }, 405);
      }
      try {
        return await handleChat(request, env, url.origin);
      } catch (e) {
        return json({ error: `chat failed: ${e.message}` }, 500);
      }
    }
    return env.ASSETS.fetch(request);
  },
};

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}

function authorized(request, env) {
  const header = request.headers.get("Authorization") || "";
  const token = header.replace(/^Bearer\s+/i, "").trim();
  return env.CHAT_TOKEN && token === env.CHAT_TOKEN;
}

async function loadJson(env, origin, name) {
  const r = await env.ASSETS.fetch(new Request(`${origin}/data/${name}.json`));
  return r.ok ? r.json() : null;
}

// ---------------------------------------------------------------- contexts
//
// Each builder turns one snapshot family into compact text lines. Agents
// declare which builders they use; everything stays well inside the model's
// 24k window.

async function ctxCoverage(env, origin) {
  const tickers = await loadJson(env, origin, "tickers");
  if (!tickers?.totals) return "";
  return (
    `COVERAGE: ${tickers.totals.all} tickers. By RM: ` +
    Object.entries(tickers.totals.by_rm).map(([k, v]) => `${k} ${v}`).join(", ") +
    ". By sector: " +
    Object.entries(tickers.totals.by_sector).map(([k, v]) => `${k} ${v}`).join(", ")
  );
}

async function ctxPrices(env, origin) {
  const [tickers, brief] = await Promise.all([
    loadJson(env, origin, "tickers"),
    loadJson(env, origin, "morning-brief"),
  ]);
  const cov = {};
  for (const t of tickers?.tickers || []) cov[t.tk] = t;
  const lines = [`AS-OF: ${brief?.asOf || "?"} (prices are previous close)`];
  lines.push("TICKERS (tk sector rm | last pct1d pct5d pctYtd volRatio):");
  for (const r of brief?.rows || []) {
    const c = cov[r.tk] || {};
    const f = (x) => (x == null ? "-" : x);
    lines.push(`${r.tk} ${c.sector || "?"} ${c.rm || "?"} | ${f(r.last)} ` +
      `${f(r.pct1d)} ${f(r.pct5d)} ${f(r.pctYtd)} ${f(r.volRatio)}` +
      (r.hi52 ? " 52wHI" : "") + (r.lo52 ? " 52wLO" : ""));
  }
  return lines.join("\n");
}

async function ctxAlerts(env, origin) {
  const unusual = await loadJson(env, origin, "unusual-trading");
  const alerts = (unusual?.alerts || []).filter(
    (a) => a.severity === "high" || a.severity === "medium");
  const lines = [`UNUSUAL-TRADING ALERTS (${alerts.length} high/medium, asOf ${unusual?.asOf || "?"}):`];
  for (const a of alerts.slice(0, 60)) {
    lines.push(`${a.tk} ${a.sector}: ${a.type} ${a.label} [${a.severity}]`);
  }
  return lines.join("\n");
}

async function rmMap(env, origin) {
  const tickers = await loadJson(env, origin, "tickers");
  const map = {};
  for (const t of tickers?.tickers || []) map[t.tk] = t.rm;
  return map;
}

/** Take up to `cap` items, but guarantee the user's RM rows survive the cut:
 *  all of theirs first (recency order preserved), then everyone else's. */
function rmFirst(items, cap, rms, userRm, tkOf) {
  if (!userRm) return items.slice(0, cap);
  const mine = [], rest = [];
  for (const it of items) (rms[tkOf(it)] === userRm ? mine : rest).push(it);
  return mine.concat(rest).slice(0, cap);
}

async function ctxNews(env, origin, userRm) {
  const [news, rms] = await Promise.all([
    loadJson(env, origin, "external-news"), rmMap(env, origin)]);
  const items = news?.items || [];
  const picked = rmFirst(items, 50, rms, userRm, (n) => n.tk);
  const lines = [`EXTERNAL NEWS (last ${news?.windowDays || "?"} days, ${items.length} items, asOf ${news?.asOf || "?"}; rm=owning RM` +
    (userRm ? `; the user's rm=${userRm} rows are listed first` : "") + "):"];
  for (const n of picked) {
    const rm = rms[n.tk] ? ` rm=${rms[n.tk]}` : "";
    lines.push(`${(n.ts || "").slice(0, 10)} ${n.tk || n.sector || "-"}${rm} [${n.source}] ${n.title}` +
      (n.excerpt ? ` — ${n.excerpt.slice(0, 90)}` : ""));
  }
  return lines.join("\n");
}

async function ctxFilings(env, origin, userRm) {
  const [pulse, rms] = await Promise.all([
    loadJson(env, origin, "disclosure-pulse"), rmMap(env, origin)]);
  const picked = rmFirst(pulse?.filings || [], 60, rms, userRm, (f) => f.tk);
  const lines = [`SET DISCLOSURES (last ${pulse?.windowDays || "?"} days, asOf ${pulse?.asOf || "?"}; rm=owning RM` +
    (userRm ? `; the user's rm=${userRm} rows are listed first` : "") + "):"];
  for (const f of picked) {
    const rm = rms[f.tk] ? ` rm=${rms[f.tk]}` : "";
    lines.push(`${(f.ts || "").slice(0, 10)} ${f.tk}${rm} ${f.sector}: ${String(f.title).slice(0, 110)}`);
  }
  const silent = (pulse?.status || [])
    .filter((s) => s.overdue)
    .sort((a, b) => (b.silentDays || 0) - (a.silentDays || 0));
  if (silent.length) {
    lines.push(`\nOVERDUE / SILENT TICKERS (${silent.length}):`);
    for (const s of rmFirst(silent, 30, rms, userRm, (x) => x.tk)) {
      const rm = rms[s.tk] ? ` rm=${rms[s.tk]}` : "";
      lines.push(`${s.tk}${rm} ${s.sector}: silent ${s.silentDays}d (last filed ${(s.lastFiledTs || "?").slice(0, 10)})`);
    }
  }
  return lines.join("\n");
}

async function ctxOppday(env, origin, userRm) {
  const opp = await loadJson(env, origin, "oppday-minutes");
  const all = opp?.summaries || [];
  const picked = userRm
    ? all.filter((s) => s.rm === userRm).concat(all.filter((s) => s.rm !== userRm)).slice(0, 45)
    : all.slice(0, 45);
  const lines = [`OPPDAY MINUTES (${opp?.period || "?"}, ${opp?.total || 0} companies, one-line overviews):`];
  for (const s of picked) {
    lines.push(`${s.ticker} ${s.sector} (${s.rm}): ${(s.overview || "").slice(0, 120)}`);
  }
  return lines.join("\n");
}

async function ctxInsights(env, origin) {
  const insights = await loadJson(env, origin, "ai-insights");
  if (!insights) return "";
  const lines = [`TODAY'S AI COMMENTARY (asOf ${insights.asOf}):`];
  lines.push(`Headline: ${insights.headline}`);
  lines.push(`Take: ${insights.market_take}`);
  for (const s of insights.sector_notes || []) lines.push(`${s.sector}: ${s.note}`);
  for (const w of insights.watchlist || []) lines.push(`Watch ${w.tk} (${w.rm}): ${w.reason}`);
  return lines.join("\n");
}

async function ctxSectorAgg(env, origin) {
  const brief = await loadJson(env, origin, "morning-brief");
  const by = {};
  for (const r of brief?.rows || []) {
    if (r.pct1d == null || !r.sector) continue;
    (by[r.sector] ||= []).push(r);
  }
  const lines = [`SECTOR AGGREGATES (from morning brief, asOf ${brief?.asOf || "?"}):`];
  for (const [sec, rows] of Object.entries(by)) {
    const avg = (k) => (rows.reduce((s, r) => s + (r[k] || 0), 0) / rows.length).toFixed(2);
    const up = rows.filter((r) => r.pct1d > 0).length;
    lines.push(`${sec}: ${rows.length} names, avg 1d ${avg("pct1d")}%, avg ytd ${avg("pctYtd")}%, ` +
      `breadth ${up}/${rows.length} up`);
  }
  return lines.join("\n");
}

// ---------------------------------------------------------------- agents

const SHARED_RULES =
  "IS1 is a relationship-manager team at a Thai securities firm covering " +
  "SET-listed tickers in FOOD, PROP, PF&REIT, AGRI, CONS and CONMAT. " +
  "RMs: Champ, Kae, Orn, Gift, Pim, Tony.\n" +
  "Answer ONLY from the data below. If something is not in the data " +
  "(intraday prices, tickers outside coverage), say so and name which " +
  "dashboard page or sibling agent could help. RM ownership is STRICT: " +
  "every ticker belongs to exactly one RM (the rm tag in the data). When " +
  "the user asks about 'my names', 'my coverage' or an RM's book, include " +
  "ONLY tickers whose rm tag matches that RM — silently dropping or adding " +
  "other RMs' tickers is an error. If nothing matches, say so rather than " +
  "padding with other RMs' names. (E.g. for RM Gift, a row tagged rm=Kae is " +
  "EXCLUDED even if it fits the question; only rm=Gift rows count.) " +
  "Quote numbers exactly as " +
  "given — never round across a threshold (-1.93 is NOT beyond -2). Be " +
  "concise: short answers, tables only when listing several tickers. Reply " +
  "in the user's language (Thai or English). When you mention a covered " +
  "ticker, write its symbol in UPPERCASE so the dashboard can link it.";

const AGENTS = {
  atlas: {
    persona:
      "You are Atlas, the market-data agent on the IS1 coverage dashboard. " +
      "You answer with numbers: prices, percent moves, movers, volume " +
      "ratios, unusual-trading alerts, threshold checks. Always open with the " +
      "as-of date since prices are previous close.\n" +
      "THRESHOLD MATH IS STRICT: a row qualifies for '±2%' ONLY when its value " +
      "is >= 2.00 or <= -2.00. -1.93 does NOT qualify; +1.99 does NOT qualify. " +
      "Compare the exact number — never round toward the threshold. If a name " +
      "is close-but-under, say so explicitly rather than including it.\n" +
      "WHEN LISTING SEVERAL NAMES, use a compact table sorted by the metric " +
      "asked about (most extreme first), columns: TK | last | 1d% | flag " +
      "(52wHI/52wLO/alert). One name → a single sentence, no table.\n" +
      "EXAMPLE — user: 'movers beyond ±2% in FOOD today':\n" +
      "As of 2026-06-13 (prev close). Two FOOD names cleared ±2%:\n" +
      "| TK | last | 1d% | flag |\n" +
      "|----|------|-----|------|\n" +
      "| AAA | 12.4 | +3.10 | — |\n" +
      "| BBB | 5.80 | -2.45 | 52wLO |\n" +
      "CCC at -1.93% is close but under the bar, so it is not listed.\n",
    contexts: [ctxCoverage, ctxPrices, ctxAlerts],
  },
  hermes: {
    persona:
      "You are Hermes, the news messenger on the IS1 coverage dashboard. " +
      "You connect names to catalysts: external news, SET disclosures, " +
      "silent/overdue filers and Oppday takeaways.\n" +
      "WHAT 'NEWS' MEANS: a request for 'news' (ข่าว) on a name, sector, or " +
      "RM book ALWAYS covers BOTH sources — the EXTERNAL NEWS block (press/web) " +
      "AND the SET DISCLOSURES block (official filings). Never answer from only " +
      "one. Scan both blocks for the asked-about names, then reply in two " +
      "labelled sections:\n" +
      "  📰 External news — bullets from EXTERNAL NEWS (date · source · one-line impact)\n" +
      "  📄 SET disclosures — bullets from SET DISCLOSURES (date · filing title)\n" +
      "If a section has nothing for the asked-about names, write that section's " +
      "header and 'none in the last N days' rather than omitting it — the user " +
      "needs to know you checked both. Add a third section only when relevant: " +
      "⏳ Silent/overdue (from the OVERDUE list) or 🎤 Oppday takeaways. " +
      "Report tight bullets and flag anything a client might call about.\n" +
      "EXAMPLE — user: 'any news on ITC?'\n" +
      "📰 External news\n" +
      "• 2026-06-13 [HOONSMART] ITC joins TU on a mangrove clean-up CSR drive — low impact.\n" +
      "📄 SET disclosures\n" +
      "• None for ITC in the last 90 days.\n" +
      "(Both headers always appear, even when one side is empty.)\n",
    contexts: [ctxCoverage, ctxNews, ctxFilings, ctxOppday],
  },
  pythia: {
    persona:
      "You are Pythia, the macro and sector strategist on the IS1 coverage " +
      "dashboard. You read sector aggregates and the daily AI commentary to " +
      "answer top-down questions: which sectors lead or lag, what matters for " +
      "FOOD/PROP/PF&REIT, what to watch this week.\n" +
      "RANK FROM THE NUMBERS: 'leads/lags' questions are answered by sorting " +
      "the SECTOR AGGREGATES on the metric asked (default avg 1d), naming the " +
      "exact figure and the breadth (e.g. 'FOOD +0.8%, breadth 9/12 up'). " +
      "Never assert a ranking the aggregates do not support.\n" +
      "SEPARATE FACT FROM VIEW: numbers come from SECTOR AGGREGATES; any " +
      "outlook, theme or 'watch' call must be attributed to TODAY'S AI " +
      "COMMENTARY ('the daily AI take flags…'). If the commentary is silent on " +
      "something, say it is your read of the aggregates, not a house view — " +
      "and never invent a catalyst that is not in the data.\n" +
      "EXAMPLE — user: 'which sector leads and which lags today?':\n" +
      "As of 2026-06-13: PF&REIT leads (avg 1d +0.9%, breadth 7/8 up); PROP " +
      "lags (avg 1d -0.6%, breadth 3/11 up). The daily AI take ties PROP's " +
      "softness to the BoT rate hold. FOOD is middling (+0.1%, 6/12 up).\n",
    contexts: [ctxCoverage, ctxSectorAgg, ctxInsights],
  },
};

// Lex routes to Gemini File Search instead of Workers AI. Returns the same
// { reply, ... } shape; citations are appended to the reply text so the dock
// renders them with no client change.
async function handleLex(env, origin, cleaned, rm) {
  if (!env.GEMINI_API_KEY) {
    return "Lex is not configured yet (missing GEMINI_API_KEY worker secret).";
  }
  const index = await loadJson(env, origin, "regulations-index");
  const store = index?.store;
  if (!store) {
    return "The regulations index is not built yet — run scripts/index_regulations.py.";
  }
  const sys = LEX_SYSTEM + (rm ? `\nThe user is RM ${rm}.` : "");
  const body = {
    contents: cleaned.map((m) => ({
      role: m.role === "assistant" ? "model" : "user",
      parts: [{ text: m.content }],
    })),
    systemInstruction: { parts: [{ text: sys }] },
    tools: [{ file_search: { file_search_store_names: [store] } }],
  };
  const r = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${LEX_MODEL}:generateContent?key=${env.GEMINI_API_KEY}`,
    { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
  if (!r.ok) {
    throw new Error(`Gemini ${r.status}: ${(await r.text()).slice(0, 200)}`);
  }
  const data = await r.json();
  const cand = (data.candidates || [])[0] || {};
  const reply = (cand.content?.parts || []).map((p) => p.text).filter(Boolean).join("");
  // REST returns camelCase; tolerate snake_case defensively.
  const meta = cand.groundingMetadata || cand.grounding_metadata || {};
  const chunks = meta.groundingChunks || meta.grounding_chunks || [];
  const seen = new Set(), cites = [];
  for (const c of chunks) {
    const rc = c.retrievedContext || c.retrieved_context;
    if (!rc) continue;
    const page = rc.pageNumber || rc.page_number;
    const label = (rc.title || "source") + (page ? ` p.${page}` : "");
    if (!seen.has(label)) { seen.add(label); cites.push(label); }
  }
  let out = reply || "No answer found in the regulation documents.";
  if (cites.length) out += "\n\nSources:\n" + cites.map((c) => "• " + c).join("\n");
  return out;
}

async function handleChat(request, env, origin) {
  if (!authorized(request, env)) {
    return json({ error: "missing or wrong access token" }, 401);
  }
  const body = await request.json().catch(() => ({}));
  const agentName = (body.agent === "lex" || AGENTS[body.agent]) ? body.agent : "atlas";

  const history = Array.isArray(body.messages) ? body.messages : [];
  const cleaned = history
    .filter((m) => (m.role === "user" || m.role === "assistant") &&
                   typeof m.content === "string")
    .slice(-MAX_HISTORY)
    .map((m) => ({ role: m.role, content: m.content.slice(0, MAX_USER_CHARS) }));
  if (!cleaned.length || cleaned[cleaned.length - 1].role !== "user") {
    return json({ error: "messages must end with a user turn" }, 400);
  }

  const rm = typeof body.rm === "string" &&
    ["Champ", "Kae", "Orn", "Gift", "Pim", "Tony"].includes(body.rm)
    ? body.rm : null;
  const rmLine = rm
    ? `\nThe user is RM ${rm}. "My names/my coverage" means tickers with rm=${rm} ONLY.`
    : "";

  if (agentName === "lex") {
    const reply = await handleLex(env, origin, cleaned, rm);
    return json({ reply, agent: "lex", model: LEX_MODEL });
  }

  const agent = AGENTS[agentName];
  const parts = await Promise.all(agent.contexts.map((fn) => fn(env, origin, rm)));
  const context = parts.filter(Boolean).join("\n\n");
  const result = await env.AI.run(CHAT_MODEL, {
    messages: [
      { role: "system", content: agent.persona + SHARED_RULES + rmLine + "\n\nDATA:\n" + context },
      ...cleaned,
    ],
    max_tokens: 800,
    temperature: 0.2,
  });
  return json({ reply: result.response ?? "", agent: agentName, model: CHAT_MODEL });
}
