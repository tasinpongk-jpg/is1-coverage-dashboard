#!/usr/bin/env node
/**
 * Agent eval harness — fires a fixed battery at the DEPLOYED worker and scores
 * each agent's key behaviours with property checks (pass/fail), so a prompt or
 * context change can be measured instead of eyeballed.
 *
 * This hits the live worker (Workers AI + Gemini cost real quota), so it is a
 * MANUAL tool, not a CI gate. The committed unit tests (tests/worker.test.mjs)
 * cover the deterministic context logic with no network; this covers the model.
 *
 * Run:
 *   IS1_CHAT_TOKEN=... node scripts/eval_agents.mjs
 *   node scripts/eval_agents.mjs              # auto-reads token from ../AI Agent/.env
 *   node scripts/eval_agents.mjs --agent atlas    # one agent only
 *
 * Env: IS1_CHAT_TOKEN (required), IS1_DASHBOARD_URL (optional override), IS1_RM.
 * Exit code is the number of failed checks (0 = all pass).
 */
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));

function loadToken() {
  if (process.env.IS1_CHAT_TOKEN) return process.env.IS1_CHAT_TOKEN.trim();
  // sibling AI Agent CLI keeps the same token in its .env
  for (const p of [join(HERE, "..", "..", "AI Agent", ".env"), join(HERE, "..", ".env")]) {
    try {
      const m = readFileSync(p, "utf8").match(/^IS1_CHAT_TOKEN\s*=\s*(.+)$/m);
      if (m) return m[1].trim();
    } catch { /* next */ }
  }
  console.error("No token. Set IS1_CHAT_TOKEN or put it in ../AI Agent/.env");
  process.exit(2);
}

const TOKEN = loadToken();
const URL = (process.env.IS1_DASHBOARD_URL || "https://is1-coverage-dashboard.tasinpong-k.workers.dev").replace(/\/$/, "") + "/api/chat";
const RM = process.env.IS1_RM || "Champ";

async function ask(agent, content) {
  const r = await fetch(URL, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: "Bearer " + TOKEN },
    body: JSON.stringify({ agent, rm: RM, messages: [{ role: "user", content }] }),
  });
  const d = await r.json().catch(() => ({ error: `non-json ${r.status}` }));
  if (d.error) throw new Error(d.error);
  return d.reply || "";
}

// ---- reusable property checks (return {ok, detail}) -----------------------
const has = (s) => (r) => ({ ok: r.includes(s), detail: `contains "${s}"` });
const hasRe = (re, label) => (r) => ({ ok: re.test(r), detail: label || re.source });
const notRe = (re, label) => (r) => ({ ok: !re.test(r), detail: "NOT " + (label || re.source) });
// pull "1d%" column out of markdown table rows: | TK | last | 1d% | flag |
function tableMoves(r) {
  return [...r.matchAll(/^\|\s*[A-Z][A-Z0-9]{1,7}\s*\|\s*[\d.]+\s*\|\s*(-?\d+(?:\.\d+)?)\s*\|/gm)].map((m) => +m[1]);
}
const allMovesClear = (x) => (r) => {
  const mv = tableMoves(r);
  if (!mv.length) return { ok: false, detail: `no table rows parsed (need rows clearing ±${x})` };
  const bad = mv.filter((v) => Math.abs(v) < x);
  return { ok: bad.length === 0, detail: `${mv.length} rows; offenders ${JSON.stringify(bad)}` };
};
const hasFigure = (r) => ({ ok: /-?\d+(?:[.,]\d+)?\s*(%|baht|bn|mn|m\b|million|พันบาท|บาท)/i.test(r) || /\d{2,}/.test(r), detail: "mentions a number" });

// ---- the battery ----------------------------------------------------------
const CASES = [
  { agent: "atlas", q: "Top movers beyond +/-2% in my coverage. I'm Champ. Table.",
    checks: [["only rows clearing ±2", allMovesClear(2)], ["states as-of", hasRe(/as[- ]?of/i)]] },
  { agent: "atlas", q: "Names between -2% and -1.5% today. I'm Champ.",
    checks: [["no row beyond the band", (r) => { const mv = tableMoves(r); const bad = mv.filter((v) => v < -2 || v > -1.5); return { ok: mv.length === 0 || bad.length === 0, detail: `offenders ${JSON.stringify(bad)}` }; }]] },
  { agent: "atlas", q: "Top 5 names by YTD. I'm Champ.",
    checks: [["mentions YTD", hasRe(/ytd|year/i)], ["has figures", hasFigure]] },
  { agent: "atlas", q: "What's the live intraday price of CPN right now?",
    checks: [["refuses intraday", hasRe(/previous close|don'?t have|not have|real[- ]?time|intraday/i)]] },
  { agent: "pythia", q: "Which sector leads and which lags today? Figures and breadth.",
    checks: [["has a % figure", hasRe(/-?\d+(?:\.\d+)?\s*%/)], ["mentions breadth", hasRe(/breadth|\d+\s*\/\s*\d+|up\b/i)]] },
  { agent: "pythia", q: "Give me a specific catalyst explaining why FOOD outperformed today.",
    checks: [["does not fabricate", hasRe(/no specific|don'?t see|not (?:in|available)|the daily ai|my read/i)]] },
  { agent: "hermes", q: "Any news on CPN? I'm Champ.",
    checks: [["shows external-news header", has("📰")], ["shows disclosures header", has("📄")]] },
  { agent: "hermes", q: "Summarize CPN's latest SET filing. I'm Champ.",
    checks: [["leads with a filing summary", has("📄")], ["has concrete figures", hasFigure]] },
  { agent: "lex", q: "When is a connected transaction subject to shareholder approval?",
    checks: [["gives a threshold/rule", hasRe(/\d|threshold|approval|three[- ]?quarter|3\/4/i)], ["cites a source", hasRe(/source|p\.\s*\d|page/i)]] },
  { agent: "lex", q: "How do I cook pad thai?",
    checks: [["declines off-topic", hasRe(/do not|don'?t|cannot|outside|only|regulat/i)]] },
];

// ---------------------------------------------------------------------------
const only = (() => { const i = process.argv.indexOf("--agent"); return i > -1 ? process.argv[i + 1] : null; })();
const cases = only ? CASES.filter((c) => c.agent === only) : CASES;

let pass = 0, fail = 0;
console.log(`\nAgent eval — ${URL} (rm=${RM})\n`);
for (const c of cases) {
  let reply = "";
  try { reply = await ask(c.agent, c.q); }
  catch (e) { console.log(`✗ [${c.agent}] ${c.q}\n    request failed: ${e.message}`); fail += c.checks.length; continue; }
  console.log(`[${c.agent}] ${c.q}`);
  for (const [name, fn] of c.checks) {
    const { ok, detail } = fn(reply);
    if (ok) { pass++; console.log(`  ✓ ${name}`); }
    else { fail++; console.log(`  ✗ ${name} — ${detail}`); }
  }
  await new Promise((r) => setTimeout(r, 1200)); // be gentle on free-tier quota
}
console.log(`\n${pass} passed, ${fail} failed (${cases.length} cases)\n`);
process.exit(fail);
