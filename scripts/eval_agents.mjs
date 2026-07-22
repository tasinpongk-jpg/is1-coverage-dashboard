#!/usr/bin/env node
/**
 * Agent eval harness — fires a fixed battery at the DEPLOYED worker and scores
 * each agent's key behaviours with property checks (pass/fail), so a prompt or
 * context change can be measured instead of eyeballed.
 *
 * This hits the live worker (MiniMax M3 plus Pythia verified calculations), so it is a
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
const RM = process.env.IS1_RM || "C";

async function ask(agent, content) {
  const r = await fetch(URL, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: "Bearer " + TOKEN },
    body: JSON.stringify({ agent, rm: RM, messages: [{ role: "user", content }] }),
  });
  const d = await r.json().catch(() => ({ error: `non-json ${r.status}` }));
  if (d.error) throw new Error(d.error);
  return { reply: d.reply || "", model: d.model || "unknown" };
}

// ---- LLM judge (optional, --judge) ---------------------------------------
// Grades each reply 0-100 with an independent model (Groq, a different family
// than MiniMax M3 under test) so quality regressions are measurable,
// not just the boolean property checks. Reads GROQ_API_KEY like the chat token.
function loadGroqKey() {
  if (process.env.GROQ_API_KEY) return process.env.GROQ_API_KEY.trim();
  for (const p of [join(HERE, "..", "..", "AI Agent", ".env"), join(HERE, "..", ".env")]) {
    try { const m = readFileSync(p, "utf8").match(/^GROQ_API_KEY\s*=\s*(.+)$/m); if (m) return m[1].trim(); }
    catch { /* next */ }
  }
  return null;
}
const GROQ_KEY = loadGroqKey();
const JUDGE_MODEL = process.env.GROQ_JUDGE_MODEL || "llama-3.3-70b-versatile";
const ROLE = {
  atlas: "market-data agent: prices, % moves, movers, threshold checks (previous-close data)",
  pythia: "IS1 sector analyst: deterministic performance, breadth and relative screens",
  hermes: "news messenger: external news + SET disclosures, silent filers, filing summaries",
  lex: "rules & regulations agent answering only from SET/SEC regulation documents",
};
async function judge(agent, question, reply) {
  if (!GROQ_KEY) return null;
  const sys = "You grade an AI assistant answering for a Thai equity relationship-manager desk. " +
    "Score the answer 0-100 on: directness & usefulness, specificity (concrete tickers/figures, " +
    "not vague), internal consistency (no contradictions or obvious fabrication), and staying in role. " +
    "Reply ONLY with JSON: {\"score\": <int 0-100>, \"verdict\": \"pass|weak|fail\", \"issues\": \"<=12 words\"}.";
  const user = `Agent role: ${ROLE[agent] || agent}\nUser question: ${question}\nAssistant answer:\n${reply}`;
  try {
    const r = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: "Bearer " + GROQ_KEY },
      body: JSON.stringify({
        model: JUDGE_MODEL, temperature: 0, max_tokens: 120,
        response_format: { type: "json_object" },
        messages: [{ role: "system", content: sys }, { role: "user", content: user }],
      }),
    });
    const d = await r.json();
    const txt = d.choices?.[0]?.message?.content || "{}";
    const j = JSON.parse(txt);
    return { score: Math.max(0, Math.min(100, +j.score || 0)), verdict: j.verdict || "?", issues: j.issues || "" };
  } catch (e) { return { score: null, verdict: "error", issues: e.message.slice(0, 40) }; }
}

// ---- reusable property checks (return {ok, detail}) -----------------------
const has = (s) => (r) => ({ ok: r.includes(s), detail: `contains "${s}"` });
const hasRe = (re, label) => (r) => ({ ok: re.test(r), detail: label || re.source });
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
  {
    agent: "hermes", q: `What news moved my names today? I'm ${RM}.`, expectedModel: "MiniMax-M3",
    checks: [["shows external-news header", has("📰")], ["shows disclosures header", has("📄")], ["states today's scope", hasRe(/today|วันนี้|as[- ]?of/i)]],
  },
  {
    agent: "hermes", q: `Any overdue or silent filers in my coverage? I'm ${RM}.`, expectedModel: "MiniMax-M3",
    checks: [["answers overdue status", hasRe(/overdue|silent|day|\d+d|ไม่มี|ไม่พบ|none/i)], ["uses a concrete ticker or says none", hasRe(/\b[A-Z][A-Z0-9]{1,7}\b|ไม่มี|ไม่พบ|none/i)]],
  },
  {
    agent: "hermes", q: "Show CPN's latest SET filings and filing dates.", expectedModel: "MiniMax-M3",
    checks: [["focuses on CPN", hasRe(/\bCPN\b/)], ["identifies a filing or disclosure", hasRe(/filing|disclosure|filed|SET|เอกสาร|สารสนเทศ/i)], ["includes a filing date", hasRe(/\d{4}-\d{2}-\d{2}/)]],
  },
  {
    agent: "hermes", q: "อัปเดตข่าวกลุ่ม FOOD วันนี้", expectedModel: "MiniMax-M3",
    checks: [["shows external-news header", has("📰")], ["shows disclosures header", has("📄")], ["replies in Thai", hasRe(/[ก-๙]/)]],
  },
  {
    agent: "atlas", q: `Top movers beyond ±2% in my coverage. I'm ${RM}.`, expectedModel: "MiniMax-M3",
    checks: [["only rows clearing ±2", allMovesClear(2)], ["states as-of", hasRe(/as[- ]?of/i)]],
  },
  {
    agent: "atlas", q: `Any high-severity alerts today? I'm ${RM}.`, expectedModel: "MiniMax-M3",
    checks: [["answers alert severity", hasRe(/high|severity|alert|none|no .*alert|ไม่มี|ไม่พบ/i)], ["states timing", hasRe(/today|as[- ]?of|วันนี้|\d{4}-\d{2}-\d{2}/i)]],
  },
  {
    agent: "atlas", q: "Which names hit a 52-week low?", expectedModel: "MiniMax-M3",
    checks: [["answers the 52-week-low screen", hasRe(/52[- ]?week|52w|low|ไม่มี|ไม่พบ|none/i)], ["uses a ticker or says none", hasRe(/\b[A-Z][A-Z0-9]{1,7}\b|ไม่มี|ไม่พบ|none/i)]],
  },
  {
    agent: "pythia", q: "Rank all 6 IS1 sectors by 1-day return and breadth.", expectedModel: "deterministic",
    checks: [["has sector table", hasRe(/\| Sector \| Avg 1d/)], ["has a % figure", hasRe(/-?\d+(?:\.\d+)?\s*%/)], ["includes breadth", hasRe(/Breadth|\d+\s*\/\s*\d+/i)], ["covers core sectors", hasRe(/FOOD[\s\S]*PROP[\s\S]*PF&REIT|PF&REIT[\s\S]*PROP[\s\S]*FOOD/i)]],
  },
  {
    agent: "pythia", q: "Compare FOOD, PROP and PF&REIT on 1-day, 5-day and YTD performance.", expectedModel: "deterministic",
    checks: [["covers FOOD", hasRe(/\bFOOD\b/)], ["covers PROP", hasRe(/\bPROP\b/)], ["covers PF&REIT", hasRe(/PF&REIT/)], ["shows all periods", hasRe(/Avg 1d[\s\S]*Avg 5d[\s\S]*Avg YTD/)]],
  },
  {
    agent: "pythia", q: "Which sectors have the weakest breadth today?", expectedModel: "deterministic",
    checks: [["states weakest-breadth ordering", hasRe(/weakest breadth/i)], ["includes figures", hasFigure], ["includes breadth counts", hasRe(/\d+\s*\/\s*\d+/)]],
  },
  {
    agent: "lex", q: "What must a listed company disclose after a board resolution?", expectedModel: "MiniMax-M3",
    checks: [["answers disclosure timing", hasRe(/immediate|trading session|business day|ทันที|วันทำการ/i)], ["cites a PDF page", hasRe(/\[[^\]]+\.pdf p\.\d+\]/i)], ["shows retrieved sources", hasRe(/Sources retrieved:/)]],
  },
  {
    agent: "lex", q: "When is a connected transaction subject to shareholder approval?", expectedModel: "MiniMax-M3",
    checks: [["gives thresholds or vote rule", hasRe(/\d|threshold|three[- ]?quarter|3\s*\/\s*4|NTA/i)], ["cites a PDF page", hasRe(/\[[^\]]+\.pdf p\.\d+\]/i)], ["shows retrieved sources", hasRe(/Sources retrieved:/)]],
  },
  {
    agent: "lex", q: "อธิบายเกณฑ์ free float ของ SET", expectedModel: "MiniMax-M3",
    checks: [["states 150 holders", hasRe(/150/)], ["states 15 percent", hasRe(/(?:15\s*(?:%|เปอร์เซ็นต์)|ร้อยละ\s*15)/i)], ["cites a PDF page", hasRe(/\[[^\]]+\.pdf p\.\d+\]/i)], ["replies in Thai", hasRe(/[ก-๙]/)]],
  },
];

// ---------------------------------------------------------------------------
const arg = (f) => { const i = process.argv.indexOf(f); return i > -1 ? process.argv[i + 1] : null; };
const only = arg("--agent");
const doJudge = process.argv.includes("--judge");
const gate = arg("--gate") != null ? +arg("--gate") : null; // min mean judge score to pass
const cases = only ? CASES.filter((c) => c.agent === only) : CASES;

let pass = 0, fail = 0;
const scores = [];
console.log(`\nAgent eval — ${URL} (rm=${RM})${doJudge ? ` · judge=${JUDGE_MODEL}` : ""}\n`);
if (doJudge && !GROQ_KEY) console.log("(--judge requested but no GROQ_API_KEY found — skipping scores)\n");
for (const c of cases) {
  let result;
  try { result = await ask(c.agent, c.q); }
  catch (e) { console.log(`✗ [${c.agent}] ${c.q}\n    request failed: ${e.message}`); fail += c.checks.length + (c.expectedModel ? 1 : 0); continue; }
  const reply = result.reply;
  console.log(`[${c.agent}] ${c.q} [${result.model}]`);
  if (c.expectedModel) {
    if (result.model === c.expectedModel) { pass++; console.log(`  ✓ model ${c.expectedModel}`); }
    else { fail++; console.log(`  ✗ model — expected ${c.expectedModel}, got ${result.model}`); }
  }
  for (const [name, fn] of c.checks) {
    const { ok, detail } = fn(reply);
    if (ok) { pass++; console.log(`  ✓ ${name}`); }
    else { fail++; console.log(`  ✗ ${name} — ${detail}`); }
  }
  if (doJudge && GROQ_KEY) {
    const j = await judge(c.agent, c.q, reply);
    if (j && j.score != null) { scores.push(j.score); console.log(`  ⟂ judge ${j.score}/100 [${j.verdict}]${j.issues ? " — " + j.issues : ""}`); }
    else console.log(`  ⟂ judge: ${j?.issues || "unavailable"}`);
  }
  await new Promise((r) => setTimeout(r, 1200)); // be gentle on free-tier quota
}
const mean = scores.length ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : null;
console.log(`\n${pass} passed, ${fail} failed (${cases.length} cases)` +
  (mean != null ? ` · mean judge ${mean}/100` : "") + "\n");
// Exit non-zero on any property failure, or (if a gate is set) a sub-threshold mean.
let exit = fail;
if (gate != null && mean != null && mean < gate) {
  console.log(`GATE FAIL: mean judge ${mean} < ${gate}\n`);
  exit = exit || 1;
}
process.exit(exit);
