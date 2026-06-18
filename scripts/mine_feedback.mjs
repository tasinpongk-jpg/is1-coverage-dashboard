#!/usr/bin/env node
/**
 * Feedback miner — pull the dock 👍/👎 votes from the worker and surface what's
 * failing, so downvotes become eval cases / few-shots (closing the loop).
 *
 * The worker reads its own KV and returns the votes (GET /api/feedback,
 * token-gated); this script summarizes them. With --themes, Groq clusters the
 * downvotes into recurring failure themes.
 *
 *   node scripts/mine_feedback.mjs                 # stats + list downvotes
 *   node scripts/mine_feedback.mjs --agent atlas   # one agent
 *   node scripts/mine_feedback.mjs --themes        # + Groq theme clustering
 *
 * Token from env IS1_CHAT_TOKEN or ../AI Agent/.env. URL via IS1_DASHBOARD_URL.
 */
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
function fromEnvFile(name) {
  for (const p of [join(HERE, "..", "..", "AI Agent", ".env"), join(HERE, "..", ".env")]) {
    try { const m = readFileSync(p, "utf8").match(new RegExp(`^${name}\\s*=\\s*(.+)$`, "m")); if (m) return m[1].trim(); }
    catch { /* next */ }
  }
  return null;
}
const TOKEN = process.env.IS1_CHAT_TOKEN || fromEnvFile("IS1_CHAT_TOKEN");
if (!TOKEN) { console.error("No IS1_CHAT_TOKEN (env or ../AI Agent/.env)"); process.exit(2); }
const BASE = (process.env.IS1_DASHBOARD_URL || "https://is1-coverage-dashboard.tasinpong-k.workers.dev").replace(/\/$/, "");
const arg = (f) => { const i = process.argv.indexOf(f); return i > -1 ? process.argv[i + 1] : null; };
const onlyAgent = arg("--agent");
const doThemes = process.argv.includes("--themes");

const res = await fetch(`${BASE}/api/feedback`, { headers: { Authorization: "Bearer " + TOKEN } });
const data = await res.json();
if (data.error) { console.error("export failed:", data.error); process.exit(1); }
let votes = data.votes || [];
if (data.note) console.log(`(note: ${data.note})`);
if (onlyAgent) votes = votes.filter((v) => v.agent === onlyAgent);

const up = votes.filter((v) => v.vote === "up").length;
const down = votes.filter((v) => v.vote === "down");
console.log(`\n${votes.length} votes — 👍 ${up}  👎 ${down.length}` +
  (votes.length ? `  (${Math.round(100 * up / votes.length)}% positive)` : "") + "\n");

const byAgent = {};
for (const v of votes) { (byAgent[v.agent] ||= { up: 0, down: 0 }); byAgent[v.agent][v.vote === "up" ? "up" : "down"]++; }
console.log("By agent:");
for (const [a, c] of Object.entries(byAgent)) console.log(`  ${a.padEnd(7)} 👍 ${c.up}  👎 ${c.down}`);

if (down.length) {
  console.log(`\n👎 Downvotes (turn each into an eval case or few-shot):`);
  for (const v of down.slice(0, 40)) {
    console.log(`\n  [${v.agent}] ${v.ts?.slice(0, 16)} rm=${v.rm}`);
    console.log(`  Q: ${String(v.question || "").slice(0, 160)}`);
    console.log(`  A: ${String(v.reply || "").replace(/\s+/g, " ").slice(0, 200)}`);
  }
}

if (doThemes && down.length) {
  const KEY = process.env.GROQ_API_KEY || fromEnvFile("GROQ_API_KEY");
  if (!KEY) { console.log("\n(--themes needs GROQ_API_KEY)"); }
  else {
    const sample = down.slice(0, 30).map((v, i) => `${i + 1}. [${v.agent}] Q:${v.question} | A:${String(v.reply).slice(0, 160)}`).join("\n");
    const r = await fetch("https://api.groq.com/openai/v1/chat/completions", {
      method: "POST", headers: { "Content-Type": "application/json", Authorization: "Bearer " + KEY },
      body: JSON.stringify({
        model: process.env.GROQ_JUDGE_MODEL || "llama-3.3-70b-versatile", temperature: 0.2, max_tokens: 400,
        messages: [{ role: "system", content: "You triage downvoted AI answers for a stock-desk assistant. Cluster them into 3-6 recurring failure themes; for each give a short title, count, and a one-line fix (prompt/context/data). Be concrete." },
          { role: "user", content: sample }],
      }),
    });
    const j = await r.json();
    console.log("\n=== Failure themes (Groq) ===\n" + (j.choices?.[0]?.message?.content || "(no themes)"));
  }
}
