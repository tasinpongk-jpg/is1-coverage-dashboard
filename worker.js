/**
 * IS1 coverage dashboard worker.
 *
 * Static assets are served by the assets pipeline (this code only runs for
 * paths that don't match an asset). One API route:
 *
 *   POST /api/chat   { messages: [{role, content}, ...] }
 *     -> { reply: "..." }
 *
 * Grounded in the daily snapshot JSONs (read back from the deployed assets,
 * so the bot always answers from the same data the dashboard shows). Gated
 * by a shared token: Authorization: Bearer <CHAT_TOKEN worker secret>.
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

/** Compact text context from today's snapshots — small enough for the
 *  model's window, complete enough to answer per-ticker questions. */
async function buildContext(env, origin) {
  const [tickers, brief, unusual, insights] = await Promise.all([
    loadJson(env, origin, "tickers"),
    loadJson(env, origin, "morning-brief"),
    loadJson(env, origin, "unusual-trading"),
    loadJson(env, origin, "ai-insights"),
  ]);
  const cov = {};
  for (const t of tickers?.tickers || []) cov[t.tk] = t;

  const lines = [];
  lines.push(`AS-OF: ${brief?.asOf || "?"} (prices are previous close)`);
  if (tickers?.totals) {
    lines.push(`COVERAGE: ${tickers.totals.all} tickers. By RM: ` +
      Object.entries(tickers.totals.by_rm).map(([k, v]) => `${k} ${v}`).join(", ") +
      ". By sector: " +
      Object.entries(tickers.totals.by_sector).map(([k, v]) => `${k} ${v}`).join(", "));
  }

  lines.push("\nTICKERS (tk sector rm | last pct1d pct5d pctYtd volRatio):");
  for (const r of brief?.rows || []) {
    const c = cov[r.tk] || {};
    const f = (x) => (x == null ? "-" : x);
    lines.push(`${r.tk} ${c.sector || "?"} ${c.rm || "?"} | ${f(r.last)} ` +
      `${f(r.pct1d)} ${f(r.pct5d)} ${f(r.pctYtd)} ${f(r.volRatio)}` +
      (r.hi52 ? " 52wHI" : "") + (r.lo52 ? " 52wLO" : ""));
  }

  const alerts = (unusual?.alerts || []).filter(
    (a) => a.severity === "high" || a.severity === "medium");
  lines.push(`\nUNUSUAL-TRADING ALERTS (${alerts.length} high/medium):`);
  for (const a of alerts.slice(0, 60)) {
    lines.push(`${a.tk} ${a.sector}: ${a.type} ${a.label} [${a.severity}]`);
  }

  if (insights) {
    lines.push(`\nTODAY'S AI COMMENTARY (asOf ${insights.asOf}):`);
    lines.push(`Headline: ${insights.headline}`);
    lines.push(`Take: ${insights.market_take}`);
    for (const s of insights.sector_notes || []) {
      lines.push(`${s.sector}: ${s.note}`);
    }
    for (const w of insights.watchlist || []) {
      lines.push(`Watch ${w.tk} (${w.rm}): ${w.reason}`);
    }
  }
  return lines.join("\n");
}

const SYSTEM_PROMPT =
  "You are the coverage assistant on the IS1 team dashboard. IS1 is a " +
  "relationship-manager team at a Thai securities firm covering SET-listed " +
  "tickers in FOOD, PROP, PF&REIT, AGRI, CONS and CONMAT. RMs: Champ, Kae, " +
  "Orn, Gift, Pim, Tony.\n" +
  "Answer ONLY from the coverage data below. If something is not in the " +
  "data (intraday prices, news details, tickers outside coverage), say so " +
  "and suggest where to look (morning brief, disclosure pulse, SET website). " +
  "Quote numbers exactly as given — never round across a threshold. Be " +
  "concise: short answers, tables only when listing several tickers. Reply " +
  "in the user's language (Thai or English).\n\nCOVERAGE DATA:\n";

async function handleChat(request, env, origin) {
  if (!authorized(request, env)) {
    return json({ error: "missing or wrong access token" }, 401);
  }
  const body = await request.json().catch(() => ({}));
  const history = Array.isArray(body.messages) ? body.messages : [];
  const cleaned = history
    .filter((m) => (m.role === "user" || m.role === "assistant") &&
                   typeof m.content === "string")
    .slice(-MAX_HISTORY)
    .map((m) => ({ role: m.role, content: m.content.slice(0, MAX_USER_CHARS) }));
  if (!cleaned.length || cleaned[cleaned.length - 1].role !== "user") {
    return json({ error: "messages must end with a user turn" }, 400);
  }

  const context = await buildContext(env, origin);
  const result = await env.AI.run(CHAT_MODEL, {
    messages: [
      { role: "system", content: SYSTEM_PROMPT + context },
      ...cleaned,
    ],
    max_tokens: 800,
    temperature: 0.2,
  });
  return json({ reply: result.response ?? "", model: CHAT_MODEL });
}
