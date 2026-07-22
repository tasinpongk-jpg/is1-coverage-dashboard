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
 *   pythia — macro/sector: AI commentary, sector aggregates
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
const GEMINI_PDF_MODEL = "gemini-2.5-flash";
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
        max_tokens: options.maxTokens || 2200,
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
  if (typeof reply !== "string" || !reply.trim()) {
    throw new ChatServiceError("MiniMax M3 returned an empty answer; retry the question", 502);
  }
  return { reply: reply.trim(), model: payload.model || CHAT_MODEL };
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
  else if (q?.sector) rows = rows.filter((r) => (cov[r.tk]?.sector || r.sector) === q.sector);
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
  else if (q?.sector) items = items.filter((n) => n.sector === q.sector);
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
  else if (q?.sector) filings = filings.filter((f) => f.sector === q.sector);
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
  return { reply: appendLexSources(citedReply, chunks), model: result.model };
}

// ---------------------------------------------------- on-demand PDF summaries
//
// Canonical recipe + gotchas: INTEGRATION.md §2 (shared with the AI Agent CLI's
// filing_tools.py — keep the two in sync).
//
// Hermes can summarize the ACTUAL filed document, not just its headline. SET
// serves a newsdetails HTML page (the filing.url) that links the real PDF on
// weblink.set.or.th; the PDF goes straight to Gemini (which reads PDFs natively
// — no JS PDF parser needed). Summaries are cached by SET news id so a document
// is fetched once. Header-only fetch clears SET's bot wall from a normal IP;
// if Cloudflare egress is challenged, every step fails soft and Hermes simply
// reports it couldn't open the document.

const SET_HEADERS = {
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " +
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
  "Referer": "https://www.set.or.th/en/market/news-and-alert/news",
  "Origin": "https://www.set.or.th",
};

// "summarize / explain / detail / what does it say" — Thai and English.
function wantsDocSummary(text) {
  return /\b(summar(?:y|ise|ize|ising|izing)|explain|detail|details|breakdown|full text|what (?:does|do|did)\b.*\bsay)\b/i
    .test(String(text || "")) || /สรุป|รายละเอียด|อธิบาย|เนื้อหา/.test(String(text || ""));
}

function bytesToBase64(bytes) {
  let out = "";
  const chunk = 0x8000;
  for (let i = 0; i < bytes.length; i += chunk) {
    out += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
  }
  return btoa(out);
}

async function resolvePdfUrl(newsUrl) {
  if (!newsUrl) return null;
  const r = await fetch(newsUrl, { headers: SET_HEADERS });
  if (!r.ok) return null;
  const html = await r.text();
  const m = html.match(/https?:\/\/weblink\.set\.or\.th\/[^\s"'<>]+\.pdf/i);
  return m ? m[0] : null;
}

// Returns a short summary string for one filing, or null if the document can't
// be retrieved. Cached in the colo Cache API by news id.
async function summarizeFiling(env, filing, lang) {
  if (!env.GEMINI_API_KEY || !filing?.url) return null;
  const cache = caches.default;
  // v2: v1 entries were truncated by gemini-2.5-flash thinking-token budget.
  // Key includes lang so an EN and a TH asker each get their own summary.
  const cacheKey = new Request(
    `https://is1-doc-summary/v2/${lang}/${filing._id || encodeURIComponent(filing.url)}`);
  const cached = await cache.match(cacheKey);
  if (cached) return await cached.text();

  const pdfUrl = await resolvePdfUrl(filing.url);
  if (!pdfUrl) return null;
  const pr = await fetch(pdfUrl, { headers: SET_HEADERS });
  if (!pr.ok) return null;
  const buf = new Uint8Array(await pr.arrayBuffer());
  if (buf.length < 1000 || buf.length > 15_000_000) return null; // empty / too big

  const prompt =
    "Summarize this SET (Stock Exchange of Thailand) disclosure document for a " +
    "relationship manager. Output ONLY 3-4 tight bullets — no preamble, no " +
    "'here is a summary', start directly with the first '•'. Cover: what was " +
    "filed, the key numbers / decisions / dates, and why a client might care. " +
    "EACH bullet MUST carry a concrete figure, date or decision from the " +
    "document (e.g. revenue/profit value, % change, THB amount, board resolution, " +
    "ex-date) — no vague 'filed its MD&A' lines. Use only what the document says. " +
    "Write in " + (lang === "th" ? "Thai." : "English.");
  const body = {
    contents: [{ role: "user", parts: [
      { inline_data: { mime_type: "application/pdf", data: bytesToBase64(buf) } },
      { text: prompt },
    ] }],
    // gemini-2.5-flash is a thinking model: thinking tokens count against
    // maxOutputTokens, so a low cap starves the actual text. Disable thinking
    // (summarization needs none) and give the output real room.
    generationConfig: {
      temperature: 0.2,
      maxOutputTokens: 1024,
      thinkingConfig: { thinkingBudget: 0 },
    },
  };
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_PDF_MODEL}:generateContent?key=${env.GEMINI_API_KEY}`;
  const init = { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
  let txt = "";
  for (let attempt = 0; attempt < 2 && !txt; attempt++) { // one retry absorbs cold transients
    try {
      const gr = await fetch(url, init);
      if (!gr.ok) continue;
      const data = await gr.json();
      txt = ((data.candidates || [])[0]?.content?.parts || [])
        .map((p) => p.text).filter(Boolean).join("").trim();
    } catch { /* retry */ }
  }
  if (!txt) return null;
  await cache.put(cacheKey, new Response(txt, { headers: { "Cache-Control": "max-age=2592000" } }));
  return txt;
}

// Build the full Hermes reply for a "summarize the filing" request directly
// from Gemini's PDF summaries (newest 1-2 filings for the focused ticker), plus
// an overdue-status line. Returns null if no PDF could be opened, so the caller
// can fall back to the chat model. Summaries run in parallel; cached by news id.
async function buildDocSummaryReply(env, origin, focus, lang) {
  const pulse = await loadJson(env, origin, "disclosure-pulse");
  const cand = (pulse?.filings || [])
    .filter((f) => focus.has(f.tk))
    .sort((a, b) => Date.parse(b.ts || 0) - Date.parse(a.ts || 0))
    .slice(0, 2);
  if (!cand.length) return null;
  const sums = await Promise.all(cand.map(async (f) => {
    const s = await summarizeFiling(env, f, lang);
    return s ? { f, s } : null;
  }));
  const got = sums.filter(Boolean);
  if (!got.length) return null;

  const tks = [...focus].join(", ");
  let reply = `📄 ${tks} — summarized from the filed PDF:\n`;
  for (const { f, s } of got) {
    reply += `\n${(f.ts || "").slice(0, 10)} — ${f.title}\n${s.trim()}\n`;
  }
  const overdue = (pulse?.status || []).filter((x) => x.overdue && focus.has(x.tk));
  if (overdue.length) {
    reply += "\n⏳ " + overdue
      .map((x) => `${x.tk} silent ${x.silentDays}d (last filed ${(x.lastFiledTs || "?").slice(0, 10)})`)
      .join("; ");
  }
  return reply.trim();
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
    return json({ reply: result.reply, agent: "lex", model: result.model });
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

  // On-demand: when a user asks Hermes to summarize a specific ticker's filing,
  // read the actual PDF, summarize via Gemini, and return that DIRECTLY. The
  // chat model won't faithfully reproduce an injected summary (it compresses to
  // a generic line), so we bypass it and serve Gemini's output verbatim.
  if (agentName === "hermes" && focus.size && wantsDocSummary(lastText)) {
    const lang = /[฀-๿]/.test(lastText) ? "th" : "en";
    const direct = await buildDocSummaryReply(env, origin, focus, lang);
    if (direct) return json({ reply: direct, agent: "hermes", model: GEMINI_PDF_MODEL });
    // couldn't open any PDF → fall through to the normal model, with a note
    context += "\n\nNOTE: the user asked to summarize a filing but the PDF could " +
      "not be opened; say so plainly and fall back to the disclosure title.";
  }
  const result = await runMiniMax(env, [
    { role: "system", content: agent.persona + SHARED_RULES + rmLine + "\n\nDATA:\n" + context },
    ...cleaned,
  ]);
  let reply = result.reply;
  // Output verification: flag any covered ticker the model named that wasn't in
  // its data — catches hallucinated / pretraining-leaked names before the user
  // (and the dock's ticker-chip linkifier) treats them as real.
  const ungrounded = ungroundedTickers(reply, context, covered);
  if (ungrounded.length) {
    reply += `\n\n⚠ Unverified: ${ungrounded.join(", ")} — not in the data I was ` +
      `given for this question. Treat with caution / re-ask naming the ticker.`;
  }
  return json({ reply, agent: agentName, model: result.model });
}
