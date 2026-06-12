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
 *   pythia — macro/sector: macro overlays, AI commentary, sector aggregates
 *
 * Gated by a shared token: Authorization: Bearer <CHAT_TOKEN worker secret>.
 * Inference: Cloudflare Workers AI (free-tier neuron allocation).
 */

const CHAT_MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast";
const MAX_HISTORY = 12; // user+assistant turns kept from the client
const MAX_USER_CHARS = 2000;

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

async function ctxMacro(env, origin) {
  const macro = await loadJson(env, origin, "macro-overlays");
  const lines = [`MACRO OVERLAYS (${macro?.total || 0} items, asOf ${macro?.asOf || "?"}):`];
  for (const m of (macro?.items || []).slice(0, 50)) {
    lines.push(`${(m.ts || "").slice(0, 10)} [${m.source}/${m.category}] ${m.title}` +
      (m.excerpt ? ` — ${m.excerpt.slice(0, 140)}` : ""));
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
  "padding with other RMs' names. Quote numbers exactly as " +
  "given — never round across a threshold (-1.93 is NOT beyond -2). Be " +
  "concise: short answers, tables only when listing several tickers. Reply " +
  "in the user's language (Thai or English). When you mention a covered " +
  "ticker, write its symbol in UPPERCASE so the dashboard can link it.";

const AGENTS = {
  atlas: {
    persona:
      "You are Atlas, the market-data agent on the IS1 coverage dashboard. " +
      "You answer with numbers: prices, percent moves, movers, volume " +
      "ratios, unusual-trading alerts, threshold checks. Always state the " +
      "as-of date since prices are previous close.\n",
    contexts: [ctxCoverage, ctxPrices, ctxAlerts],
  },
  hermes: {
    persona:
      "You are Hermes, the news messenger on the IS1 coverage dashboard. " +
      "You connect names to catalysts: external news, SET disclosures, " +
      "silent/overdue filers and Oppday takeaways. Report tight bullets — " +
      "date, source, one-line impact — and flag anything a client might " +
      "call about.\n",
    contexts: [ctxCoverage, ctxNews, ctxFilings, ctxOppday],
  },
  pythia: {
    persona:
      "You are Pythia, the macro and sector strategist on the IS1 coverage " +
      "dashboard. You read macro overlays (BLS, REIC, ThaiBMA), sector " +
      "aggregates and the daily AI commentary to answer top-down questions: " +
      "which sectors lead or lag, what macro prints matter for FOOD/PROP/" +
      "PF&REIT, what to watch this week.\n",
    contexts: [ctxCoverage, ctxSectorAgg, ctxMacro, ctxInsights],
  },
};

async function handleChat(request, env, origin) {
  if (!authorized(request, env)) {
    return json({ error: "missing or wrong access token" }, 401);
  }
  const body = await request.json().catch(() => ({}));
  const agentName = AGENTS[body.agent] ? body.agent : "atlas";
  const agent = AGENTS[agentName];

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
