/**
 * IS1 coverage dashboard worker.
 *
 * Static assets are served by the assets pipeline (this code only runs for
 * paths that don't match an asset). One API route:
 *
 *   POST /api/chat   { agent: "atlas"|"hermes"|"pythia"|"lex", messages: [...] }
 *     -> { reply: "...", agent: "...", model: "..." }
 *
 * Four named agents, each grounded in the deployed JSON assets so they answer
 * from the same data and rulebook pages the dashboard uses:
 *
 *   atlas  — market data: prices, movers, alerts, strict threshold math
 *   hermes — news messenger: external news, disclosures, oppday minutes
 *   pythia — IS1 sector screens: performance, breadth, relative ranking
 *   lex     — SET/SEC rules: deterministic retrieval over page-level PDF text
 *
 * Gated by a shared token: Authorization: Bearer <CHAT_TOKEN worker secret>.
 * Inference: MiniMax M3, called server-side with the MINIMAX_API_KEY secret.
 */

const CHAT_MODEL = "MiniMax-M3";
const MINIMAX_CHAT_URL = "https://api.minimax.io/v1/text/chatcompletion_v2";
const MINIMAX_TIMEOUT_MS = 60_000;
const MAX_HISTORY = 12; // user+assistant turns kept from the client
const MAX_USER_CHARS = 2000;
const MAX_JSON_BODY_BYTES = 64 * 1024;
const VALID_AGENTS = new Set(["atlas", "hermes", "pythia", "lex"]);
const VALID_RMS = new Set(["C", "K", "O", "G", "P", "T"]);

// Lex uses the same MiniMax M3 endpoint as the other agents. Retrieval stays
// deterministic inside the Worker over page-level text extracted from the SET
// rulebook PDFs by scripts/build_lex_corpus.py.
const LEX_CORPUS = "lex-regulations";
const LEX_MAX_CHUNKS = 8;
const LEX_MAX_CHUNKS_PER_DOCUMENT = 3;
const LEX_SYSTEM =
  "You are Lex, the rules & regulations agent on the IS1 coverage dashboard. " +
  "You answer questions about SET/SEC listing rules, disclosure obligations and " +
  "related Thai securities regulation, using ONLY the regulation documents " +
  "retrieved for you. If the documents do not cover the question, say so plainly " +
  "— never guess or cite outside knowledge. Be concise and quote the rule's own " +
  "wording where it matters. Reply in the user's language (Thai or English). " +
  "Keep the final answer under 350 words and use no more than eight bullets. " +
  "You are not a lawyer; surface what the documents say, not legal advice.\n" +
  "ANSWER SHAPE: lead with the direct answer in one line, then the basis — the " +
  "rule's own wording (quoted) and any numeric trigger (thresholds, %, day " +
  "counts, deadlines) stated EXACTLY as written. If conditions or exemptions " +
  "apply, list them as short bullets. If two retrieved rules differ or the " +
  "documents are ambiguous, say so rather than smoothing it over. When the " +
  "answer hinges on a defined term (e.g. 'connected person', 'material'), give " +
  "the document's definition before applying it. Every material number, " +
  "threshold, deadline and condition MUST cite one of the retrieved source " +
  "IDs exactly as [S1], [S2], etc. Use only IDs shown in the context. Do not " +
  "write or shorten document names yourself; the Worker expands valid source " +
  "IDs after generation. Never fabricate a rule, clause, source or page.\n" +
  "SAMPLE FORMAT — user asks when shareholder approval is required:\n" +
  "Direct answer in one line.\n" +
  "• Trigger or threshold, stated exactly [S1]\n" +
  "• Approval condition or exemption [S2]\n" +
  "If the retrieved pages do not establish the answer, state that the corpus " +
  "does not establish it and name the missing rule topic.";

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
        return json({ error: `chat failed: ${e.message}` }, e.status || 500);
      }
    }
    if (url.pathname === "/api/feedback") {
      try {
        if (request.method === "POST") return await handleFeedback(request, env);
        if (request.method === "GET") return await handleFeedbackExport(request, env);
        return json({ error: "GET or POST only" }, 405);
      } catch (e) {
        return json({ error: `feedback failed: ${e.message}` }, 500);
      }
    }
    return env.ASSETS.fetch(request);
  },
};

// Record a 👍/👎 on an agent reply so failing answers become training data.
// Durable storage uses a KV namespace IF bound as `FEEDBACK`; until then it
// logs (reviewable via `wrangler tail`). To enable durable, queryable votes:
//   1) npx wrangler kv namespace create FEEDBACK
//   2) add to wrangler.jsonc: "kv_namespaces":[{"binding":"FEEDBACK","id":"<id>"}]
//   3) redeploy. Then: npx wrangler kv key list --binding FEEDBACK
async function handleFeedback(request, env) {
  if (!authorized(request, env)) return json({ error: "missing or wrong access token" }, 401);
  const b = await request.json().catch(() => ({}));
  const vote = b.vote === "up" || b.vote === "down" ? b.vote : null;
  if (!vote) return json({ error: "vote must be 'up' or 'down'" }, 400);
  const s = (v, n) => (typeof v === "string" ? v.slice(0, n) : "");
  const agent = normalizeAgent(b.agent);
  const rm = normalizeRm(b.rm) || "";
  const rec = {
    ts: new Date().toISOString(),
    agent, vote, rm,
    question: s(b.question, 500), reply: s(b.reply, 1500),
  };
  if (env.FEEDBACK) {
    const key = `fb:${rec.ts}:${crypto.randomUUID().slice(0, 8)}`;
    await env.FEEDBACK.put(key, JSON.stringify(rec), { expirationTtl: 60 * 60 * 24 * 180 });
    return json({ ok: true, stored: "kv" });
  }
  console.log("FEEDBACK " + JSON.stringify(rec)); // visible in `wrangler tail`
  return json({ ok: true, stored: "log" });
}

// Export collected votes (token-gated) so scripts/mine_feedback.mjs can pull the
// 👎s and turn them into eval cases / few-shots. The worker reads its own KV.
async function handleFeedbackExport(request, env) {
  if (!authorized(request, env)) return json({ error: "missing or wrong access token" }, 401);
  if (!env.FEEDBACK) return json({ votes: [], note: "no KV bound; votes are console-logged only" });
  const out = [];
  let cursor;
  do {
    const page = await env.FEEDBACK.list({ prefix: "fb:", limit: 1000, cursor });
    const vals = await Promise.all(page.keys.map((k) => env.FEEDBACK.get(k.name)));
    for (const v of vals) { try { if (v) out.push(JSON.parse(v)); } catch { /* skip */ } }
    cursor = page.list_complete ? null : page.cursor;
  } while (cursor && out.length < 5000);
  out.sort((a, b) => String(b.ts).localeCompare(String(a.ts)));
  return json({ count: out.length, votes: out });
}

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

function normalizeAgent(v) {
  const agent = typeof v === "string" ? v.trim().toLowerCase() : "";
  return VALID_AGENTS.has(agent) ? agent : "";
}

function normalizeRm(v) {
  const rm = typeof v === "string" ? v.trim().toUpperCase() : "";
  return VALID_RMS.has(rm) ? rm : null;
}

async function parseJsonBody(request) {
  const type = (request.headers.get("Content-Type") || "").trim();
  if (!/^application\/json(?:\s*;|$)/i.test(type)) {
    return { response: json({ error: "Content-Type must be application/json" }, 415) };
  }
  const lenRaw = request.headers.get("Content-Length");
  if (lenRaw != null) {
    const len = Number(lenRaw);
    if (Number.isFinite(len) && len > MAX_JSON_BODY_BYTES) {
      return { response: json({ error: "request body too large" }, 413) };
    }
  }
  let text;
  try {
    text = await request.text();
  } catch {
    return { response: json({ error: "could not read request body" }, 400) };
  }
  if (new TextEncoder().encode(text).length > MAX_JSON_BODY_BYTES) {
    return { response: json({ error: "request body too large" }, 413) };
  }
  try {
    const body = JSON.parse(text || "{}");
    return { body: body && typeof body === "object" ? body : {} };
  } catch {
    return { response: json({ error: "malformed JSON" }, 400) };
  }
}

async function loadJson(env, origin, name) {
  const r = await env.ASSETS.fetch(new Request(`${origin}/data/${name}.json`));
  return r.ok ? r.json() : null;
}

async function chatResponseMeta(env, origin, agent) {
  const files = agent === "atlas"
    ? ["morning-brief", "unusual-trading"]
    : agent === "hermes"
      ? ["external-news", "disclosure-pulse", "sec-form59", "oppday-minutes"]
      : agent === "pythia"
        ? ["morning-brief"]
        : [LEX_CORPUS];
  const snapshots = await Promise.all(files.map((name) => loadJson(env, origin, name)));
  const dates = snapshots
    .map((data) => data?.asOf || data?.builtAt || data?._built_at || null)
    .filter(Boolean)
    .map((value) => String(value).slice(0, 10))
    .sort();
  return {
    asOf: dates[0] || null,
    sources: files,
  };
}

async function loadCovered(env, origin) {
  const tickers = await loadJson(env, origin, "tickers");
  return new Set((tickers?.tickers || []).map((t) => t.tk));
}

// Covered ticker symbols appearing in a piece of text. Normalize multi-letter
// symbols so users can type cpn as naturally as CPN. Single-letter symbols must
// stay uppercase so the m in contractions such as I'm is not treated as M.
function coveredIn(text, covered) {
  const source = String(text || "");
  const out = new Set();
  for (const match of source.matchAll(/\b[A-Z][A-Z0-9]{0,7}\b/gi)) {
    const raw = match[0];
    if (raw.length === 1 && raw !== raw.toUpperCase()) continue;
    if (raw.toUpperCase() === "PF" && /^\s*&\s*REIT\b/i.test(source.slice(match.index + raw.length))) continue;
    if (raw.length === 1) {
      const before = source[match.index - 1] || "";
      const after = source[match.index + 1] || "";
      if (before === "&" || before === "/" || after === "&" || after === "/") continue;
    }
    const tok = raw.toUpperCase();
    if (covered.has(tok)) out.add(tok);
  }
  return out;
}

// Tickers the user explicitly named in their latest message — empty for a broad
// question (movers, sector, book). Drives deterministic context filtering.
async function focusTickers(env, origin, text) {
  return coveredIn(text, await loadCovered(env, origin));
}

// Grounding check: any covered ticker the reply names that was NOT in the data
// the model was given is ungrounded (a pretraining leak or cross-contamination)
// — the model should only speak about names it was shown. Returns that list.
function ungroundedTickers(reply, context, covered) {
  const ctx = coveredIn(context, covered);
  return [...coveredIn(reply, covered)].filter((t) => !ctx.has(t));
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

// Parse a "movers beyond X%" style threshold out of the user's question so the
// price context can be filtered deterministically — the 70B model will not
// reliably stop at a cutoff itself. Returns {x, dir} or null.
const UP_WORDS = /\b(gain|gainer|gainers|gaining|up|rise|rising|rose|advanc|surg|jump|jumping|soar|outperform|best)\b/;
const DOWN_WORDS = /\b(los(?:s|er|ers|ing)|down|fall|falling|fell|drop|dropp|declin|sank|slump|plunge|underperform|worst)\b/;
const WORD_NUM = { one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9, ten: 10 };

// Parse an Atlas price-screen request into a deterministic intent the 70B model
// can't be trusted to execute itself: a threshold, a range, or a top-N — over a
// chosen metric. ctxPrices then filters/sorts the rows so the model only narrates.
function parsePriceQuery(text) {
  const t = String(text || "").toLowerCase();
  let metric = "pct1d";
  if (/\b(ytd|year[\s-]?to[\s-]?date|this year)\b/.test(t)) metric = "pctYtd";
  else if (/\b(5[\s-]?d(?:ay)?|five[\s-]?day|this week|past week|weekly)\b/.test(t)) metric = "pct5d";
  else if (/\b(volume|vol(?:ume)?[\s-]?ratio|turnover|volratio)\b/.test(t)) metric = "volRatio";
  const dir = UP_WORDS.test(t) ? "up" : DOWN_WORDS.test(t) ? "down" : "abs";

  // range: "between -2% and -1.5%" / "between 1 to 3 percent"
  const rng = t.match(/between\s*(-?[0-9]+(?:\.[0-9]+)?)\s*%?\s*(?:and|to|&|-)\s*(-?[0-9]+(?:\.[0-9]+)?)\s*(?:%|percent|pct)/);
  if (rng) {
    let lo = parseFloat(rng[1]), hi = parseFloat(rng[2]);
    if (lo > hi) [lo, hi] = [hi, lo];
    if (isFinite(lo) && isFinite(hi)) return { mode: "range", metric, lo, hi };
  }
  // top-N: "top 5", "biggest 10 movers", "5 biggest gainers", "worst 3" (explicit count only)
  const topM = t.match(/\b(?:top|biggest|largest|highest|leading|worst|bottom)\s+(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\b/)
    || t.match(/\b(\d+)\s+(?:biggest|largest|top|leading|worst)\b/);
  if (topM) {
    const n = parseInt(topM[1], 10) || WORD_NUM[topM[1]] || 5;
    const d = /\b(worst|bottom)\b/.test(t) ? "down" : dir; // "worst/bottom" = losers
    return { mode: "topN", metric, n: Math.min(Math.max(n, 1), 30), dir: d };
  }
  // threshold: "beyond ±X%", "up/down more than X%"
  const m = t.match(
    /(?:beyond|above|over|more than|greater than|at least|exceed(?:ing|s)?|bigger than|>=?|±|\+\/-|\+-)\s*[±+\/\-]*\s*([0-9]+(?:\.[0-9]+)?)\s*(?:%|percent|pct)/);
  if (m) {
    const x = parseFloat(m[1]);
    if (isFinite(x) && x > 0) return { mode: "threshold", metric, x, dir };
  }
  return null;
}

// Parse a "today / this week / last N days" window so news & filings can be
// date-filtered server-side instead of asking the model to compare dates.
function parseRecency(text) {
  const t = String(text || "").toLowerCase();
  if (/\btoday\b|วันนี้/.test(t)) return { days: 1, label: "today" };
  if (/\byesterday\b|เมื่อวาน/.test(t)) return { days: 2, label: "the last 2 days" };
  if (/\b(?:this week|past week|last 7 days|last week)\b|สัปดาห์นี้|7 วัน/.test(t)) return { days: 7, label: "the last 7 days" };
  if (/\b(?:this month|past month|last 30 days)\b|เดือนนี้|30 วัน/.test(t)) return { days: 30, label: "the last 30 days" };
  const m = t.match(/\b(?:last|past|in the last)\s+(\d{1,3})\s+days?\b/);
  if (m) { const d = parseInt(m[1], 10); if (d > 0) return { days: d, label: `the last ${d} days` }; }
  return null;
}

class ChatServiceError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

async function runMiniMax(env, messages, options = {}) {
  if (!env.MINIMAX_API_KEY) {
    throw new ChatServiceError(
      "MiniMax M3 is not configured (missing MINIMAX_API_KEY worker secret)",
      503,
    );
  }

  const fetcher = typeof env.MINIMAX_FETCH === "function" ? env.MINIMAX_FETCH : fetch;
  const firstBudget = options.maxTokens || 2200;
  const budgets = [firstBudget, Math.min(Math.max(firstBudget * 2, 5000), 8000)];
  for (let attempt = 0; attempt < budgets.length; attempt += 1) {
    let response;
    try {
      response = await fetcher(MINIMAX_CHAT_URL, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${env.MINIMAX_API_KEY}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: CHAT_MODEL,
          messages,
          max_tokens: budgets[attempt],
          temperature: options.temperature ?? 0.2,
        }),
        signal: AbortSignal.timeout(MINIMAX_TIMEOUT_MS),
      });
    } catch (error) {
      const timedOut = error?.name === "TimeoutError" || error?.name === "AbortError";
      throw new ChatServiceError(
        timedOut ? "MiniMax M3 timed out; retry the question" : "MiniMax M3 is temporarily unavailable",
        timedOut ? 504 : 502,
      );
    }

    const payload = await response.json().catch(() => null);
    const apiStatus = payload?.base_resp?.status_code;
    if (!response.ok || (apiStatus != null && apiStatus !== 0)) {
      console.error("MiniMax M3 request failed", {
        httpStatus: response.status,
        apiStatus,
        apiMessage: payload?.base_resp?.status_msg || "",
      });
      throw new ChatServiceError("MiniMax M3 rejected the request; retry shortly", 502);
    }

    const reply = payload?.choices?.[0]?.message?.content;
    if (typeof reply === "string" && reply.trim()) {
      return { reply: reply.trim(), model: payload.model || CHAT_MODEL };
    }
    if (attempt === 0) {
      console.warn("MiniMax M3 returned an empty answer; retrying with a larger budget", {
        firstBudget,
        retryBudget: budgets[1],
        finishReason: payload?.choices?.[0]?.finish_reason || "",
      });
    }
  }
  throw new ChatServiceError("MiniMax M3 returned an empty answer; retry the question", 502);
}

// Keep items whose ts is within `days` of now (worker has real Date).
function withinDays(items, days, tsOf) {
  if (!days) return items;
  const cutoff = Date.now() - days * 86400000;
  return items.filter((it) => { const p = Date.parse(tsOf(it)); return !isFinite(p) || p >= cutoff; });
}

// Map a sector mentioned in the query to its data code, so news/filings/prices
// can be scoped to it deterministically (like a ticker focus, but sector-wide).
// Order matters: REIT before PROP, CONMAT before CONS.
function parseSector(text) {
  const t = String(text || "").toLowerCase();
  if (/\bpf\s*&?\s*reit\b|\bpfreit\b|\breits?\b|property fund/.test(t)) return "PF&REIT";
  if (/\bconmat\b|construction material|cement\b/.test(t)) return "CONMAT";
  if (/\bcons\b|commerce|retailer/.test(t)) return "CONS";
  if (/\bprop(erty)?\b|real estate|developer|residential/.test(t)) return "PROP";
  if (/\bagri(business|culture)?\b/.test(t)) return "AGRI";
  if (/\bfood\b|beverage|\bf&b\b/.test(t)) return "FOOD";
  return null;
}

function canonicalSector(value) {
  return String(value || "").toUpperCase().replace(/\s+/g, "") === "PFREIT"
    ? "PF&REIT"
    : String(value || "").toUpperCase();
}

// Structural/query words that must NOT count as topical keywords.
const STOPWORDS = new Set((
  "news update updates latest recent recently happening happened give show tell about what which whats " +
  "any some have has there their this that these those with from into over under more most need want know your " +
  "coverage names name ticker tickers symbol symbols stock stocks share shares company companies " +
  "filing filings disclosure disclosures disclosed report reports announce announced announcement announcements " +
  "today week month year days yesterday morning recent " +
  "overview situation status story picture going happening update briefing roundup " +
  "sector sectors market markets thai thailand " +
  "food prop property reit reits agri agriculture cons commerce conmat construction cement " +
  "champ kae orn gift pim tony " +
  "please summarize summary detail details explain anything something").split(/\s+/));

// Topical latin keywords from the query (>=4 chars, not structural). Used to
// rank news/filings so a relevant item past the recency cap still surfaces.
function parseTopic(text) {
  const toks = (String(text || "").toLowerCase().match(/[a-z][a-z]{3,}/g) || [])
    .filter((w) => !STOPWORDS.has(w));
  return [...new Set(toks)].slice(0, 6);
}

// Stable re-rank by keyword hits (recency order preserved within ties / zero-hits).
function relevanceRank(items, kws, textOf) {
  if (!kws.length) return items;
  const score = (it) => {
    const s = String(textOf(it)).toLowerCase();
    return kws.reduce((a, k) => a + (s.includes(k) ? 1 : 0), 0);
  };
  return items.map((it, i) => ({ it, i, sc: score(it) }))
    .sort((a, b) => b.sc - a.sc || a.i - b.i).map((x) => x.it);
}

const METRIC_LABEL = { pct1d: "1-day %", pct5d: "5-day %", pctYtd: "YTD %", volRatio: "vol ratio" };

// The snapshot is previous-close; for an explicit live/intraday price ask, fetch
// a real-time quote so Atlas can answer instead of refusing. Returns the symbol
// to quote (uppercase, may be outside coverage) or null. Gated on intent so an
// ordinary price question never triggers an outbound fetch.
const NOT_TICKERS = new Set("SET RM AI US EPS ROE PE PBV DY YTD FY THB CEO CFO IPO MD ESG NAV REIT SEC USD EUR GDP CPI".split(" "));
function parseLiveQuote(text) {
  const t = String(text || "");
  const wantsLive = /\b(live|intraday|real[\s-]?time|right now|currently|current)\b/i.test(t) &&
    /\b(price|quote|trading|worth|at)\b/i.test(t);
  if (!wantsLive) return null;
  for (const tok of t.match(/\b[A-Z][A-Z0-9]{1,7}\b/g) || []) if (!NOT_TICKERS.has(tok)) return tok;
  return null;
}

async function fetchLiveQuote(symbol) {
  try {
    const r = await fetch(
      `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(symbol)}.BK?interval=1d&range=1d`,
      { headers: { "User-Agent": "Mozilla/5.0" } });
    if (!r.ok) return null;
    const m = (await r.json())?.chart?.result?.[0]?.meta;
    if (!m || m.regularMarketPrice == null) return null;
    const last = m.regularMarketPrice, prev = m.previousClose ?? m.chartPreviousClose ?? null;
    return {
      symbol, last, prev,
      pct: prev ? ((last - prev) / prev) * 100 : null,
      currency: m.currency || "THB",
      state: m.marketState || "?",
      time: m.regularMarketTime ? new Date(m.regularMarketTime * 1000).toISOString() : "?",
    };
  } catch { return null; }
}

function liveQuoteBlock(q) {
  const f = (x, d = 2) => (x == null ? "?" : Number(x).toFixed(d));
  return `LIVE QUOTE (real-time via Yahoo Finance — NOT the previous-close snapshot) for ${q.symbol}:\n` +
    `last ${f(q.last)} ${q.currency}, prev close ${f(q.prev)}, change ${q.pct == null ? "?" : (q.pct >= 0 ? "+" : "") + f(q.pct)}%, ` +
    `market ${q.state}, quote time ${q.time}. Answer the live-price question from THIS, and say it is live + the quote time / market state.`;
}

async function ctxPrices(env, origin, _userRm, focus, q) {
  const pq = q?.priceQuery || null;
  const [tickers, brief] = await Promise.all([
    loadJson(env, origin, "tickers"),
    loadJson(env, origin, "morning-brief"),
  ]);
  const cov = {};
  for (const t of tickers?.tickers || []) cov[t.tk] = t;
  const metric = pq?.metric || "pct1d";
  const mlabel = METRIC_LABEL[metric];
  const mval = (r) => {
    const v = r[metric];
    if (v == null) return null;
    const n = Number(v);
    return Number.isFinite(n) ? n : null;
  };
  const sortVal = (r) => mval(r) ?? 0;
  // The model should not filter/sort a 230-row list. Pre-sort by |metric| so it
  // reads top-down; for a parsed screen, hard-filter so it can only narrate.
  let rows = (brief?.rows || []).slice().sort((a, b) => Math.abs(sortVal(b)) - Math.abs(sortVal(a)));
  if (focus && focus.size) rows = rows.filter((r) => focus.has(r.tk));
  else if (q?.sector) rows = rows.filter((r) => canonicalSector(cov[r.tk]?.sector || r.sector) === q.sector);
  let note = `Rows are sorted by |${mlabel}| descending (biggest movers first).` +
    (q?.sector && !(focus && focus.size) ? ` Scoped to the ${q.sector} sector.` : "");
  if (pq?.mode === "threshold") {
    const pass = (v) => pq.dir === "up" ? v >= pq.x : pq.dir === "down" ? v <= -pq.x : Math.abs(v) >= pq.x;
    rows = rows.filter((r) => { const v = mval(r); return v != null && pass(v); });
    const sign = pq.dir === "up" ? "+" : pq.dir === "down" ? "-" : "±";
    note = `PRE-FILTERED: every row below ALREADY clears the ${sign}${pq.x}% ${mlabel} ` +
      `bar (${rows.length} names). List them ALL and ONLY these — there are no others.`;
  } else if (pq?.mode === "range") {
    rows = rows.filter((r) => { const v = mval(r); return v != null && v >= pq.lo && v <= pq.hi; })
      .sort((a, b) => mval(a) - mval(b));
    note = `PRE-FILTERED: every row below has ${mlabel} between ${pq.lo}% and ${pq.hi}% ` +
      `inclusive (${rows.length} names). List them ALL and ONLY these.`;
  } else if (pq?.mode === "topN") {
    rows = rows.filter((r) => mval(r) != null);
    if (pq.dir === "up") rows = rows.slice().sort((a, b) => mval(b) - mval(a));
    else if (pq.dir === "down") rows = rows.slice().sort((a, b) => mval(a) - mval(b));
    rows = rows.slice(0, pq.n);
    const which = pq.dir === "up" ? "top gainers" : pq.dir === "down" ? "top losers" : "biggest movers";
    note = `PRE-FILTERED: these are the ${which} by ${mlabel} (top ${rows.length}), already in order. ` +
      `List them ALL and ONLY these, in this order.`;
  }
  const lines = [`AS-OF: ${brief?.asOf || "?"} (prices are previous close)` +
    (focus && focus.size ? `; focused on ${[...focus].join(", ")}` : "") +
    "\n" + note];
  lines.push("TICKERS (tk sector rm | last pct1d pct5d pctYtd volRatio):");
  for (const r of rows) {
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

async function ctxNews(env, origin, userRm, focus, q) {
  const [news, rms] = await Promise.all([
    loadJson(env, origin, "external-news"), rmMap(env, origin)]);
  let items = news?.items || [];
  const focused = focus && focus.size;
  // When the user named specific covered tickers, show ONLY their news, so the
  // model never pads "news on CPN" with unrelated names. Else, scope to a sector
  // if one was named.
  if (focused) items = items.filter((n) => focus.has(n.tk));
  else if (q?.sector) items = items.filter((n) => canonicalSector(n.sector) === q.sector);
  const recency = q?.recency;
  if (recency) items = withinDays(items, recency.days, (n) => n.ts);
  // Rank-then-cap on topical keywords so a relevant item beyond the recency cap
  // still surfaces; otherwise keep RM-priority recency order.
  const topic = !focused && q?.topic?.length ? q.topic : null;
  let picked;
  if (focused) picked = items;
  else if (topic) picked = relevanceRank(items, topic, (n) => `${n.title} ${n.excerpt || ""}`).slice(0, 50);
  else picked = rmFirst(items, 50, rms, userRm, (n) => n.tk);
  const lines = [`EXTERNAL NEWS (last ${news?.windowDays || "?"} days, ${items.length} items, asOf ${news?.asOf || "?"}; rm=owning RM` +
    (recency ? `; FILTERED to ${recency.label}` : "") +
    (focused ? `; FILTERED to ${[...focus].join(", ")} — if a name has no rows here it has NO external news` : "") +
    (!focused && q?.sector ? `; SCOPED to ${q.sector}` : "") +
    (topic ? `; ranked by relevance to: ${topic.join(", ")}` : "") +
    (!focused && !topic && userRm ? `; the user's rm=${userRm} rows are listed first` : "") + "):"];
  for (const n of picked) {
    const rm = rms[n.tk] ? ` rm=${rms[n.tk]}` : "";
    lines.push(`${(n.ts || "").slice(0, 10)} ${n.tk || n.sector || "-"}${rm} [${n.source}] ${n.title}` +
      (n.excerpt ? ` — ${n.excerpt.slice(0, 90)}` : ""));
  }
  return lines.join("\n");
}

async function ctxFilings(env, origin, userRm, focus, q) {
  const [pulse, rms] = await Promise.all([
    loadJson(env, origin, "disclosure-pulse"), rmMap(env, origin)]);
  let filings = pulse?.filings || [];
  const focused = focus && focus.size;
  if (focused) filings = filings.filter((f) => focus.has(f.tk));
  else if (q?.sector) filings = filings.filter((f) => canonicalSector(f.sector) === q.sector);
  const recency = q?.recency;
  if (recency) filings = withinDays(filings, recency.days, (f) => f.ts);
  const topic = !focused && q?.topic?.length ? q.topic : null;
  let picked;
  if (focused) picked = filings;
  else if (topic) picked = relevanceRank(filings, topic, (f) => f.title || "").slice(0, 60);
  else picked = rmFirst(filings, 60, rms, userRm, (f) => f.tk);
  const lines = [`SET DISCLOSURES (last ${pulse?.windowDays || "?"} days, asOf ${pulse?.asOf || "?"}; rm=owning RM` +
    (recency ? `; FILTERED to ${recency.label}` : "") +
    (focused ? `; FILTERED to ${[...focus].join(", ")} — if a name has no rows here it has NO recent disclosure` : "") +
    (!focused && q?.sector ? `; SCOPED to ${q.sector}` : "") +
    (topic ? `; ranked by relevance to: ${topic.join(", ")}` : "") +
    (!focused && !topic && userRm ? `; the user's rm=${userRm} rows are listed first` : "") + "):"];
  for (const f of picked) {
    const rm = rms[f.tk] ? ` rm=${rms[f.tk]}` : "";
    lines.push(`${(f.ts || "").slice(0, 10)} ${f.tk}${rm} ${f.sector}: ${String(f.title).slice(0, 110)}`);
  }
  let silent = (pulse?.status || [])
    .filter((s) => s.overdue)
    .sort((a, b) => (b.silentDays || 0) - (a.silentDays || 0));
  if (focus && focus.size) silent = silent.filter((s) => focus.has(s.tk));
  if (silent.length) {
    lines.push(`\nOVERDUE / SILENT TICKERS (${silent.length}):`);
    for (const s of (focus && focus.size ? silent : rmFirst(silent, 30, rms, userRm, (x) => x.tk))) {
      const rm = rms[s.tk] ? ` rm=${rms[s.tk]}` : "";
      lines.push(`${s.tk}${rm} ${s.sector}: silent ${s.silentDays}d (last filed ${(s.lastFiledTs || "?").slice(0, 10)})`);
    }
  }
  return lines.join("\n");
}

async function ctxForm59(env, origin, userRm, focus) {
  const [form59, rms] = await Promise.all([
    loadJson(env, origin, "sec-form59"), rmMap(env, origin)]);
  let items = form59?.items || [];
  if (focus && focus.size) items = items.filter((it) => focus.has(it.tk));
  const picked = focus && focus.size ? items : rmFirst(items, 60, rms, userRm, (it) => it.tk);
  const lines = [`SEC FORM 59 MANAGEMENT/RELATED-PERSON TRADES (last ${form59?.windowDays || "?"} days, ${items.length} rows, asOf ${form59?.asOf || "?"}; rm=owning RM` +
    (focus && focus.size ? `; FILTERED to ${[...focus].join(", ")} — if a name has no rows here it has NO Form 59 rows` : "") +
    (!(focus && focus.size) && userRm ? `; the user's rm=${userRm} rows are listed first` : "") +
    "):"];
  for (const it of picked) {
    const rm = rms[it.tk] ? ` rm=${rms[it.tk]}` : "";
    const side = (it.side || "?").toUpperCase();
    const amt = it.amount == null ? "-" : it.amount;
    const px = it.price == null ? "-" : it.price;
    const val = it.notional == null ? "-" : it.notional;
    lines.push(`${it.filing_date || it.transaction_date || "?"} ${it.tk}${rm} ${side} ` +
      `${amt} @ ${px} value=${val} reporter="${String(it.reporter || "").slice(0, 60)}" ` +
      `relationship="${String(it.relationship || "").slice(0, 70)}"` +
      (it.is_revoked ? " REVOKED" : ""));
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
  const metrics = buildSectorMetrics(brief);
  const lines = [`SECTOR AGGREGATES (from morning brief, asOf ${brief?.asOf || "?"}):`];
  for (const row of metrics) {
    lines.push(`${row.sector}: ${row.count1d} names with 1d data, avg 1d ${fmtPct(row.avg1d)}, ` +
      `median 1d ${fmtPct(row.median1d)}, avg 5d ${fmtPct(row.avg5d)}, ` +
      `avg YTD ${fmtPct(row.avgYtd)}, breadth ${row.up}/${row.count1d} up`);
  }
  return lines.join("\n");
}

function finiteValues(rows, key) {
  return rows
    .map((row) => row[key])
    .filter((value) => value !== null && value !== undefined && value !== "" && Number.isFinite(Number(value)))
    .map(Number);
}

function hasFiniteValue(value) {
  return value !== null && value !== undefined && value !== "" && Number.isFinite(Number(value));
}

function average(values) {
  return values.length ? values.reduce((sum, value) => sum + value, 0) / values.length : null;
}

function median(values) {
  if (!values.length) return null;
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}

function fmtPct(value) {
  if (!Number.isFinite(value)) return "n/a";
  return `${value >= 0 ? "+" : ""}${value.toFixed(2)}%`;
}

export function buildSectorMetrics(brief) {
  const grouped = new Map();
  for (const row of brief?.rows || []) {
    const sector = canonicalSector(row.sector);
    if (!sector) continue;
    if (!grouped.has(sector)) grouped.set(sector, []);
    grouped.get(sector).push(row);
  }
  return [...grouped.entries()].map(([sector, rows]) => {
    const oneDay = finiteValues(rows, "pct1d");
    const fiveDay = finiteValues(rows, "pct5d");
    const ytd = finiteValues(rows, "pctYtd");
    const ranked = rows.filter((row) => hasFiniteValue(row.pct1d))
      .sort((a, b) => Number(b.pct1d) - Number(a.pct1d));
    return {
      sector,
      count: rows.length,
      count1d: oneDay.length,
      avg1d: average(oneDay),
      median1d: median(oneDay),
      avg5d: average(fiveDay),
      avgYtd: average(ytd),
      up: oneDay.filter((value) => value > 0).length,
      down: oneDay.filter((value) => value < 0).length,
      flat: oneDay.filter((value) => value === 0).length,
      breadth: oneDay.length ? oneDay.filter((value) => value > 0).length / oneDay.length : null,
      top: ranked[0] || null,
      bottom: ranked.at(-1) || null,
    };
  }).sort((a, b) => (b.avg1d ?? -Infinity) - (a.avg1d ?? -Infinity));
}

function pythiaTable(metrics, lang) {
  const thai = lang === "th";
  const head = thai
    ? "| Sector | เฉลี่ย 1 วัน | มัธยฐาน 1 วัน | เฉลี่ย 5 วัน | เฉลี่ย YTD | Breadth |"
    : "| Sector | Avg 1d | Median 1d | Avg 5d | Avg YTD | Breadth |";
  const align = "|---|---:|---:|---:|---:|---:|";
  const rows = metrics.map((row) =>
    `| ${row.sector} | ${fmtPct(row.avg1d)} | ${fmtPct(row.median1d)} | ${fmtPct(row.avg5d)} | ` +
    `${fmtPct(row.avgYtd)} | ${row.up}/${row.count1d} |`);
  return [head, align, ...rows].join("\n");
}

function pythiaSupportedPrompts(lang) {
  return lang === "th"
    ? [
      "จัดอันดับ 6 sector ใน IS1 coverage ตามผลตอบแทน 1 วันและ breadth",
      "เปรียบเทียบ FOOD, PROP และ PF&REIT ทั้ง 1 วัน 5 วัน และ YTD",
      "Sector ไหนมี breadth อ่อนที่สุดวันนี้",
    ]
    : [
      "Rank all 6 IS1 sectors by 1-day return and breadth",
      "Compare FOOD, PROP and PF&REIT on 1-day, 5-day and YTD performance",
      "Which sectors have the weakest breadth today",
    ];
}

function pythiaScopeReply(lang, asOf) {
  const prompts = pythiaSupportedPrompts(lang);
  if (lang === "th") {
    return `Pythia ไม่มีข้อมูล SET Index, fund flow, macro forecast หรือข้อมูลอนาคตใน snapshot ${asOf || "ล่าสุด"}\n\n` +
      `คำถามที่ตอบได้จากข้อมูลจริง:\n${prompts.map((prompt) => `• ${prompt}`).join("\n")}`;
  }
  return `Pythia does not have SET Index, fund-flow, macro-forecast or future data in the ${asOf || "latest"} snapshot.\n\n` +
    `Questions supported by the current data:\n${prompts.map((prompt) => `• ${prompt}`).join("\n")}`;
}

async function handlePythia(env, origin, cleaned) {
  const question = cleaned.at(-1)?.content || "";
  const lang = /[฀-๿]/.test(question) ? "th" : "en";
  const brief = await loadJson(env, origin, "morning-brief");
  const metrics = buildSectorMetrics(brief);
  const unsupported = /\b(?:set\s*(?:index|50|100)|foreign (?:fund )?flow|fund flow|interest rate|gdp|fx|exchange rate|oil price|forecast|target price|next week|next month)\b|ต่างชาติ|ซื้อสุทธิ|ขายสุทธิ|ดอกเบี้ย|จีดีพี|ค่าเงินบาท|ราคาน้ำมัน|คาดการณ์|แนวโน้ม|ราคาเป้าหมาย|สัปดาห์หน้า|เดือนหน้า/iu;
  if (unsupported.test(question)) {
    return { reply: pythiaScopeReply(lang, brief?.asOf), model: "deterministic", asOf: brief?.asOf };
  }

  const coreCompare = /compare[\s\S]*(?:food|prop|reit)|เปรียบเทียบ[\s\S]*(?:food|prop|reit)/iu.test(question);
  const weakBreadth = /weak(?:est)? breadth|breadth[\s\S]*(?:weak|low)|breadth[\s\S]*(?:อ่อน|แย่)|(?:อ่อน|แย่)[\s\S]*breadth/iu.test(question);
  const leaderboard = /lead|lag|rank|leaderboard|sector[\s\S]*(?:today|performance)|จัดอันดับ|sector[\s\S]*(?:นำ|รั้งท้าย|วันนี้)|ภาพรวม[\s\S]*(?:coverage|sector)/iu.test(question);
  const namedSector = parseSector(question);

  let selected = metrics;
  let lead = "";
  if (coreCompare) {
    const core = new Set(["FOOD", "PROP", "PF&REIT"]);
    selected = metrics.filter((row) => core.has(row.sector));
    lead = lang === "th"
      ? `เปรียบเทียบ 3 กลุ่มหลักใน IS1 coverage ณ ${brief?.asOf || "?"}`
      : `Core-sector comparison for IS1 coverage as of ${brief?.asOf || "?"}`;
  } else if (weakBreadth) {
    selected = [...metrics].sort((a, b) => (a.breadth ?? Infinity) - (b.breadth ?? Infinity));
    lead = lang === "th"
      ? `เรียงจาก breadth อ่อนที่สุด ณ ${brief?.asOf || "?"}`
      : `Ranked from weakest breadth as of ${brief?.asOf || "?"}`;
  } else if (namedSector) {
    selected = metrics.filter((row) => row.sector === namedSector);
    const row = selected[0];
    if (row) {
      const movers = row.top && row.bottom
        ? `${row.top.tk} ${fmtPct(Number(row.top.pct1d))}; ${row.bottom.tk} ${fmtPct(Number(row.bottom.pct1d))}`
        : "n/a";
      lead = lang === "th"
        ? `${namedSector} ณ ${brief?.asOf || "?"} ตัวเด่น/อ่อนสุด: ${movers}`
        : `${namedSector} as of ${brief?.asOf || "?"}. Top/bottom 1d: ${movers}`;
    }
  } else if (leaderboard) {
    lead = lang === "th"
      ? `อันดับ sector ใน IS1 coverage ณ ${brief?.asOf || "?"} ตามค่าเฉลี่ย 1 วัน`
      : `IS1 coverage sector ranking as of ${brief?.asOf || "?"}, sorted by equal-weight 1-day average`;
  } else {
    return {
      reply: pythiaScopeReply(lang, brief?.asOf),
      model: "deterministic",
      asOf: brief?.asOf,
    };
  }

  const note = lang === "th"
    ? "คำนวณจากหุ้นที่มีข้อมูลในแต่ละ metric เท่านั้น จึงไม่แทนภาพ SET ทั้งตลาด"
    : "Each metric uses only tickers with available values; this is not the full SET market.";
  return {
    reply: `${lead}\n\n${pythiaTable(selected, lang)}\n\n${note}`,
    model: "deterministic",
    asOf: brief?.asOf,
  };
}

// ---------------------------------------------------------- Lex retrieval

const LEX_STOPWORDS = new Set((
  "a an and are as at be by do does for from how i in is it me of on or the " +
  "this to what when which who why with company listed rule rules about after " +
  "การ ของ ที่ ใน และ หรือ เป็น ให้ ได้ ต้อง มี เมื่อ กรณี บริษัท"
).split(/\s+/));
const LEX_CORPUS_CACHE = new WeakMap();
const LEX_SEARCH_CACHE = new WeakMap();

const LEX_QUERY_ALIASES = [
  {
    test: /connected|related[\s-]?party|connected person|รายการที่เกี่ยวโยง|บุคคลที่เกี่ยวโยง/iu,
    terms: ["รายการที่เกี่ยวโยงกัน", "บุคคลที่เกี่ยวโยงกัน", "ผู้ถือหุ้น", "NTA", "3 ใน 4"],
  },
  {
    test: /free[\s-]?float|ผู้ถือหุ้นรายย่อย|กระจายการถือหุ้น/iu,
    terms: ["การกระจายการถือหุ้นโดยผู้ถือหุ้นรายย่อย", "free float", "ผู้ถือหุ้นรายย่อย"],
  },
  {
    test: /board resolution|board meeting|มติคณะกรรมการ|ประชุมคณะกรรมการ/iu,
    terms: ["การเปิดเผยข้อมูลตามเหตุการณ์", "มติคณะกรรมการ", "เปิดเผยสารสนเทศ", "ทันที"],
  },
  {
    test: /acquisition|disposal|asset transaction|ได้มาหรือจำหน่าย|สินทรัพย์/iu,
    terms: ["การได้มาหรือจำหน่ายไปซึ่งสินทรัพย์", "ขนาดรายการ", "ผู้ถือหุ้น"],
  },
  {
    test: /dividend|ปันผล/iu,
    terms: ["การจ่ายปันผล", "วันกำหนดรายชื่อผู้ถือหุ้น", "เปิดเผยสารสนเทศ"],
  },
  {
    test: /share repurchase|treasury stock|ซื้อหุ้นคืน/iu,
    terms: ["ซื้อหุ้นคืน", "จำหน่ายหุ้นที่ซื้อคืน", "เปิดเผยสารสนเทศ"],
  },
  {
    test: /financial statement|งบการเงิน|annual report|รายงานประจำปี/iu,
    terms: ["การจัดทำและส่งงบการเงิน", "เปิดเผยข้อมูลตามระยะเวลา", "กำหนดเวลา"],
  },
  {
    test: /shareholder meeting|general meeting|ประชุมผู้ถือหุ้น/iu,
    terms: ["การประชุมผู้ถือหุ้น", "หนังสือนัดประชุม", "มติผู้ถือหุ้น"],
  },
];

function lexNormalize(value) {
  return String(value || "").normalize("NFKC").toLowerCase().replace(/\s+/g, " ").trim();
}

function lexQueryParts(query) {
  const phrases = [String(query || "")];
  for (const alias of LEX_QUERY_ALIASES) {
    if (alias.test.test(query)) phrases.push(...alias.terms);
  }
  const expanded = phrases.join(" ");
  const tokens = new Set();
  if (typeof Intl?.Segmenter === "function") {
    const segmenter = new Intl.Segmenter("th", { granularity: "word" });
    for (const part of segmenter.segment(lexNormalize(expanded))) {
      const token = part.segment.replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}%]+$/gu, "");
      if (part.isWordLike && token && !LEX_STOPWORDS.has(token) && (token.length > 1 || /^\d+$/.test(token))) {
        tokens.add(token);
      }
    }
  } else {
    for (const match of lexNormalize(expanded).matchAll(/[\p{L}\p{N}][\p{L}\p{N}%.-]*/gu)) {
      const token = match[0];
      if (!LEX_STOPWORDS.has(token) && (token.length > 1 || /^\d+$/.test(token))) tokens.add(token);
    }
  }
  for (const match of expanded.matchAll(/\d+(?:\.\d+)?%?/g)) tokens.add(match[0].toLowerCase());
  return {
    phrases: [...new Set(phrases.map(lexNormalize).filter((part) => part.length >= 3))],
    tokens: [...tokens],
  };
}

function countOccurrences(haystack, needle) {
  if (!needle) return 0;
  let count = 0;
  let index = 0;
  while (count < 4 && (index = haystack.indexOf(needle, index)) !== -1) {
    count += 1;
    index += needle.length;
  }
  return count;
}

export function retrieveLexChunks(corpus, query) {
  const chunks = Array.isArray(corpus?.chunks) ? corpus.chunks : [];
  const { phrases, tokens } = lexQueryParts(query);
  const canCache = corpus !== null && (typeof corpus === "object" || typeof corpus === "function");
  let searchable = canCache ? LEX_SEARCH_CACHE.get(corpus) : null;
  if (!searchable) {
    searchable = chunks.map((chunk, index) => ({
      chunk,
      index,
      title: lexNormalize(chunk.title),
      text: lexNormalize(chunk.text),
    }));
    if (canCache) LEX_SEARCH_CACHE.set(corpus, searchable);
  }
  const ranked = searchable.map(({ chunk, index, title, text }) => {
    let score = 0;
    for (const phrase of phrases) {
      if (title.includes(phrase)) score += 48;
      if (text.includes(phrase)) score += 20;
    }
    for (const token of tokens) {
      const normalized = lexNormalize(token);
      if (!normalized) continue;
      if (title.includes(normalized)) score += 12;
      score += countOccurrences(text, normalized) * 3;
    }
    return { ...chunk, score, index };
  }).filter((chunk) => chunk.score > 0)
    .sort((a, b) => b.score - a.score || a.document.localeCompare(b.document) || a.page - b.page || a.index - b.index);

  const selected = [];
  const perDocument = new Map();
  for (const chunk of ranked) {
    const count = perDocument.get(chunk.document) || 0;
    if (count >= LEX_MAX_CHUNKS_PER_DOCUMENT) continue;
    selected.push(chunk);
    perDocument.set(chunk.document, count + 1);
    if (selected.length >= LEX_MAX_CHUNKS) break;
  }
  return selected;
}

async function loadLexCorpus(env, origin) {
  const assets = env?.ASSETS;
  if (!assets || (typeof assets !== "object" && typeof assets !== "function")) {
    return loadJson(env, origin, LEX_CORPUS);
  }
  let pending = LEX_CORPUS_CACHE.get(assets);
  if (!pending) {
    pending = loadJson(env, origin, LEX_CORPUS);
    LEX_CORPUS_CACHE.set(assets, pending);
  }
  const corpus = await pending;
  if (!corpus) LEX_CORPUS_CACHE.delete(assets);
  return corpus;
}

function isLexDomainQuestion(text) {
  return /\b(?:set|sec|rule|regulat|disclos|listed|shareholder|board|connected|related[\s-]?party|free[\s-]?float|dividend|capital|financial statement|acquisition|disposal|tender|audit|director)\b|กฎ|เกณฑ์|เปิดเผย|จดทะเบียน|ผู้ถือหุ้น|คณะกรรมการ|เกี่ยวโยง|รายการ|กระจายการถือหุ้น|ปันผล|ทุน|งบการเงิน|ได้มาหรือจำหน่าย|ประชุม|ตรวจสอบ|กรรมการ|ตลาดหลักทรัพย์|ก\.ล\.ต\.|มาตรา/iu.test(text);
}

function formatLexContext(chunks, corpus) {
  const head = `REGULATION CORPUS: ${corpus?.documentCount || "?"} documents, ` +
    `${corpus?.pageCount || "?"} pages, built ${corpus?.builtAt || "?"}.`;
  const blocks = chunks.map((chunk, index) =>
    `[SOURCE S${index + 1} | ${chunk.document} | p.${chunk.page}]\n${chunk.text}`);
  return [head, ...blocks].join("\n\n");
}

export function resolveLexCitations(reply, chunks) {
  const labels = chunks.map((chunk) => `${chunk.document} p.${chunk.page}`);
  const allowed = new Set(labels);
  let invalidCount = 0;
  let output = String(reply || "").replace(/\[S(\d+)\]/gi, (_full, rawIndex) => {
    const label = labels[Number(rawIndex) - 1];
    if (!label) { invalidCount += 1; return ""; }
    return `[${label}]`;
  });

  output = output.replace(/\[([^\]\n]+\.pdf\s+p\.\d+(?:\s*,\s*p\.\d+)*)\]/gi, (full, inner) => {
    const match = inner.match(/^(.*\.pdf)\s+p\.(\d+(?:\s*,\s*p\.\d+)*)$/i);
    if (!match) { invalidCount += 1; return ""; }
    const document = match[1];
    const pages = match[2].split(/\s*,\s*p\./).map((page) => Number(page));
    const exact = pages.map((page) => `${document} p.${page}`);
    if (!exact.every((label) => allowed.has(label))) {
      invalidCount += 1;
      return "";
    }
    return exact.map((label) => `[${label}]`).join(" ");
  });

  if (invalidCount) {
    console.warn("Lex removed non-retrieved citation markers", { invalidCount });
  }
  return output.replace(/[ \t]+\n/g, "\n").replace(/ {2,}/g, " ").trim();
}

function appendLexSources(reply, chunks) {
  const labels = [];
  const seen = new Set();
  for (const chunk of chunks) {
    const label = `${chunk.document} p.${chunk.page}`;
    if (!seen.has(label)) { seen.add(label); labels.push(label); }
  }
  if (!labels.length) return reply;
  return `${reply.trim()}\n\nSources retrieved:\n${labels.map((label) => `• ${label}`).join("\n")}`;
}

// ---------------------------------------------------------------- agents

const SHARED_RULES =
  "IS1 is a relationship-manager team at a Thai securities firm covering " +
  "SET-listed tickers in FOOD, PROP, PF&REIT, AGRI, CONS and CONMAT. " +
  "RMs: C, K, O, G, P, T.\n" +
  "Answer ONLY from the data below. If something is not in the data " +
  "(intraday prices, tickers outside coverage), say so and name which " +
  "dashboard page or sibling agent could help. RM ownership is STRICT: " +
  "every ticker belongs to exactly one RM (the rm tag in the data). When " +
  "the user asks about 'my names', 'my coverage' or an RM's book, include " +
  "ONLY tickers whose rm tag matches that RM — silently dropping or adding " +
  "other RMs' tickers is an error. If nothing matches, say so rather than " +
  "padding with other RMs' names. (E.g. for RM G, a row tagged rm=K is " +
  "EXCLUDED even if it fits the question; only rm=G rows count.) " +
  "Quote numbers exactly as " +
  "given — never round across a threshold (-1.93 is NOT beyond -2). Be " +
  "concise: short answers, tables only when listing several tickers. Reply " +
  "in the user's language (Thai or English). TICKERS ONLY, NEVER NAMES: the " +
  "data identifies every holding by its ticker SYMBOL — there is no company-" +
  "name field. Refer to each holding by that exact symbol in UPPERCASE (e.g. " +
  "AQUA, CPN) so the dashboard can link it. Do NOT expand a symbol into a " +
  "company name or guess one — you do not have the name mapping and a guessed " +
  "name is an error. If you don't know the symbol, say so; never substitute a " +
  "plausible-sounding name.";

const AGENTS = {
  atlas: {
    persona:
      "You are Atlas, the market-data agent on the IS1 coverage dashboard. " +
      "You answer with numbers: prices, percent moves, movers, volume " +
      "ratios, unusual-trading alerts, threshold checks. The TICKERS block is a " +
      "previous-close snapshot — open with its as-of date. EXCEPTION: if a LIVE " +
      "QUOTE block is present, the user asked for the current/intraday price — " +
      "answer from that real-time quote, state it is live with the quote time and " +
      "market state, and don't claim it's previous close.\n" +
      "THRESHOLD MATH IS STRICT: a row qualifies for '±2%' ONLY when its value " +
      "is >= 2.00 or <= -2.00. -1.93 does NOT qualify; +1.99 does NOT qualify. " +
      "Compare the exact number — never round toward the threshold. If a name " +
      "is close-but-under, say so explicitly rather than including it.\n" +
      "The TICKERS block is pre-sorted by |1-day %| descending. For a '|move| " +
      "beyond X%' question, read DOWN from the top and STOP at the first row " +
      "whose |1d%| < X — every row below it is also under the bar, so never " +
      "include them. Include a row ONLY if you can point to its exact 1d% " +
      "clearing the threshold.\n" +
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
      "Form 59 management/related-person trades, silent/overdue filers and " +
      "Oppday takeaways.\n" +
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
    contexts: [ctxCoverage, ctxNews, ctxFilings, ctxForm59, ctxOppday],
  },
  pythia: {
    persona:
      "You are Pythia, the IS1 sector analyst on the coverage dashboard. " +
      "You answer only from sector aggregates and daily coverage snapshots. " +
      "You do not have SET Index, fund-flow, macro forecasts, target prices or " +
      "future data. Redirect those requests to a supported sector screen.\n" +
      "RANK FROM THE NUMBERS: 'leads/lags' questions are answered by sorting " +
      "the SECTOR AGGREGATES on the metric asked (default avg 1d), naming the " +
      "exact figure and the breadth (e.g. 'FOOD +0.8%, breadth 9/12 up'). " +
      "Never assert a ranking the aggregates do not support.\n" +
      "SEPARATE FACT FROM VIEW: numbers come from SECTOR AGGREGATES. Do not " +
      "convert relative performance into a market or macro conclusion. Never " +
      "invent a catalyst that is not in the data.\n" +
      "EXAMPLE — user: 'which sector leads and which lags today?':\n" +
      "As of 2026-06-13: PF&REIT leads (avg 1d +0.9%, breadth 7/8 up); PROP " +
      "lags (avg 1d -0.6%, breadth 3/11 up). FOOD is middling (+0.1%, 6/12 up).\n",
    contexts: [ctxCoverage, ctxSectorAgg],
  },
};

function needsHermesSections(text) {
  return /\bnews\b|ข่าว/iu.test(String(text || ""));
}

function normalizeHermesSections(reply) {
  let out = String(reply || "");
  if (!out.includes("📰")) {
    out = out.replace(
      /(^|\n)(\s*(?:#{1,4}\s*)?)(?:external\s+news|ข่าวภายนอก|ข่าวจากภายนอก)(\s*[:：-]?)/iu,
      "$1$2📰 External news$3",
    );
  }
  if (!out.includes("📄")) {
    out = out.replace(
      /(^|\n)(\s*(?:#{1,4}\s*)?)(?:set\s+disclosures?|disclosures?|การเปิดเผยข้อมูล(?:ต่อตลาดหลักทรัพย์)?|ข่าว\s*SET)(\s*[:：-]?)/iu,
      "$1$2📄 SET disclosures$3",
    );
  }
  return out;
}

function hasHermesSections(reply) {
  return String(reply || "").includes("📰") && String(reply || "").includes("📄");
}

function contextSectionRows(context, start, end) {
  const source = String(context || "");
  const from = source.indexOf(start);
  if (from < 0) return [];
  const tail = source.slice(from + start.length);
  const to = end ? tail.indexOf(end) : -1;
  return (to >= 0 ? tail.slice(0, to) : tail)
    .split("\n")
    .map((line) => line.trim().replace(/\s+rm=[A-Z]\b/g, ""))
    .filter((line) => /^\d{4}-\d{2}-\d{2}\s/.test(line));
}

function hermesDeterministicFallback(context, question) {
  const thai = /[฀-๿]/.test(String(question || ""));
  const news = contextSectionRows(context, "EXTERNAL NEWS", "SET DISCLOSURES").slice(0, 8);
  const filings = contextSectionRows(context, "SET DISCLOSURES", "SEC FORM 59").slice(0, 8);
  const none = thai ? "• ไม่พบรายการใน snapshot ที่เลือก" : "• None in the selected snapshot";
  const bullets = (rows) => rows.length ? rows.map((line) => `• ${line}`).join("\n") : none;
  return `📰 External news\n${bullets(news)}\n\n📄 SET disclosures\n${bullets(filings)}`;
}

function ensureAsOf(reply, asOf, question) {
  if (!asOf || String(reply || "").includes(asOf)) return reply;
  const label = /[฀-๿]/.test(String(question || "")) ? "ข้อมูล ณ" : "Data as of";
  return `${String(reply || "").trim()}\n\n${label} ${asOf}`;
}

// Lex retrieves the most relevant rulebook pages locally, then asks MiniMax M3
// to answer only from those pages. The deterministic source list makes every
// response auditable even when the model omits an inline citation.
async function handleLex(env, origin, cleaned, rm) {
  const question = cleaned[cleaned.length - 1]?.content || "";
  if (!isLexDomainQuestion(question)) {
    const thai = /[฀-๿]/.test(question);
    return {
      reply: thai
        ? "Lex ตอบเฉพาะกฎเกณฑ์ SET/SEC การเปิดเผยข้อมูล และหน้าที่ของบริษัทจดทะเบียน"
        : "Lex only answers SET/SEC rules, disclosure obligations and listed-company requirements.",
      model: CHAT_MODEL,
    };
  }
  const corpus = await loadLexCorpus(env, origin);
  if (!corpus?.chunks?.length) {
    throw new ChatServiceError(
      "Lex regulation corpus is missing; run scripts/build_lex_corpus.py",
      503,
    );
  }
  const chunks = retrieveLexChunks(corpus, question);
  if (!chunks.length) {
    return {
      reply: "The regulation corpus did not return a relevant source for this question.",
      model: CHAT_MODEL,
    };
  }

  const sys = LEX_SYSTEM + (rm ? `\nThe user is RM ${rm}.` : "");
  const result = await runMiniMax(env, [
    { role: "system", content: `${sys}\n\n${formatLexContext(chunks, corpus)}` },
    ...cleaned,
  ], { maxTokens: 5000, temperature: 0.1 });
  const citedReply = resolveLexCitations(result.reply, chunks);
  return {
    reply: appendLexSources(citedReply, chunks),
    model: result.model,
    meta: {
      asOf: String(corpus.builtAt || "").slice(0, 10) || null,
      sources: [LEX_CORPUS],
    },
  };
}

async function handleChat(request, env, origin) {
  if (!authorized(request, env)) {
    return json({ error: "missing or wrong access token" }, 401);
  }
  const parsed = await parseJsonBody(request);
  if (parsed.response) return parsed.response;
  const body = parsed.body;
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

  const rm = normalizeRm(body.rm);
  const rmLine = rm
    ? `\nThe user is RM ${rm}. "My names/my coverage" means tickers with rm=${rm} ONLY.`
    : "";

  if (agentName === "lex") {
    const result = await handleLex(env, origin, cleaned, rm);
    return json({ reply: result.reply, agent: "lex", model: result.model, meta: result.meta });
  }
  if (agentName === "pythia") {
    const direct = await handlePythia(env, origin, cleaned);
    if (direct) {
      return json({
        reply: direct.reply,
        agent: "pythia",
        model: direct.model,
        meta: { asOf: direct.asOf || null, sources: ["morning-brief"] },
      });
    }
  }

  const agent = AGENTS[agentName];
  // Tickers the user named in their last turn → context builders show ONLY
  // those rows, so the model can't pad "news on CPN" or miscount movers.
  const lastText = cleaned[cleaned.length - 1].content;
  const covered = await loadCovered(env, origin);
  const focus = coveredIn(lastText, covered);
  // Deterministic query intents the model can't execute reliably: an Atlas price
  // screen (threshold/range/top-N over a metric), a news/filing date window, a
  // sector scope, and topical keywords for relevance ranking. Ticker focus wins
  // over sector/topic, so those only apply when no specific ticker was named.
  const q = {
    priceQuery: parsePriceQuery(lastText),
    recency: parseRecency(lastText),
    sector: focus.size ? null : parseSector(lastText),
    topic: focus.size ? [] : parseTopic(lastText),
  };
  const parts = await Promise.all(agent.contexts.map((fn) => fn(env, origin, rm, focus, q)));
  let context = parts.filter(Boolean).join("\n\n");

  // Atlas only: an explicit live/intraday price ask fetches a real-time quote so
  // it can answer rather than refuse. Fails soft to the previous-close snapshot.
  if (agentName === "atlas") {
    const sym = parseLiveQuote(lastText);
    if (sym) { const lq = await fetchLiveQuote(sym); if (lq) context = liveQuoteBlock(lq) + "\n\n" + context; }
  }

  const baseSystem = agent.persona + SHARED_RULES + rmLine + "\n\nDATA:\n" + context;
  let result = await runMiniMax(env, [
    { role: "system", content: baseSystem },
    ...cleaned,
  ]);
  let reply = agentName === "hermes" ? normalizeHermesSections(result.reply) : result.reply;
  if (agentName === "hermes" && needsHermesSections(lastText) && !hasHermesSections(reply)) {
    result = await runMiniMax(env, [
      {
        role: "system",
        content: baseSystem + "\n\nOUTPUT CONTRACT: Return both labelled sections exactly: " +
          "📰 External news and 📄 SET disclosures. Include a section even when it has no rows.",
      },
      ...cleaned,
    ], { temperature: 0.1 });
    reply = normalizeHermesSections(result.reply);
    if (!hasHermesSections(reply)) reply = hermesDeterministicFallback(context, lastText);
  }
  // Output verification: flag any covered ticker the model named that wasn't in
  // its data — catches hallucinated / pretraining-leaked names before the user
  // (and the dock's ticker-chip linkifier) treats them as real.
  const ungrounded = ungroundedTickers(reply, context, covered);
  if (ungrounded.length) {
    reply += `\n\n⚠ Unverified: ${ungrounded.join(", ")} — not in the data I was ` +
      `given for this question. Treat with caution / re-ask naming the ticker.`;
  }
  const meta = await chatResponseMeta(env, origin, agentName);
  reply = ensureAsOf(reply, meta.asOf, lastText);
  return json({
    reply,
    agent: agentName,
    model: result.model,
    meta,
  });
}
