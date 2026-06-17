// Tests for worker.js /api/chat — run with `node --test tests/` from repo root.
// Stubs env.ASSETS (reads local data/*.json) and env.AI (echoes prompt stats),
// so this exercises routing, auth, agent selection, context building and the
// RM-priority slicing without touching Cloudflare.

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import worker from "../worker.js";

let lastSystem = "";
const env = {
  CHAT_TOKEN: "testtoken",
  ASSETS: {
    fetch: async (req) => {
      const p = new URL(req.url).pathname;
      try { return new Response(await readFile("." + p)); }
      catch { return new Response("not found", { status: 404 }); }
    },
  },
  AI: {
    run: async (_model, opts) => {
      lastSystem = opts.messages[0].content;
      return { response: "stub-reply" };
    },
  },
};

function chatReq(body, token = "testtoken") {
  return new Request("https://x.test/api/chat", {
    method: "POST",
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    body: JSON.stringify(body),
  });
}
const userMsg = [{ role: "user", content: "hi" }];

test("each agent responds 200 and reports its name", async () => {
  for (const agent of ["atlas", "hermes", "pythia"]) {
    const r = await worker.fetch(chatReq({ agent, messages: userMsg }), env);
    assert.equal(r.status, 200);
    const d = await r.json();
    assert.equal(d.agent, agent);
    assert.equal(d.reply, "stub-reply");
  }
});

test("unknown agent falls back to atlas", async () => {
  const r = await worker.fetch(chatReq({ agent: "zeus", messages: userMsg }), env);
  assert.equal((await r.json()).agent, "atlas");
});

test("auth: missing or wrong token is 401", async () => {
  for (const token of [null, "wrong"]) {
    const r = await worker.fetch(chatReq({ messages: userMsg }, token), env);
    assert.equal(r.status, 401);
  }
});

test("messages must end with a user turn", async () => {
  const r = await worker.fetch(chatReq({ messages: [] }), env);
  assert.equal(r.status, 400);
});

test("non-chat paths pass through to assets", async () => {
  const r = await worker.fetch(new Request("https://x.test/index.html"), env);
  assert.equal(r.status, 200);
});

test("valid rm pins the user line; invalid rm is ignored", async () => {
  await worker.fetch(chatReq({ agent: "hermes", rm: "Champ", messages: userMsg }), env);
  assert.ok(lastSystem.includes("The user is RM Champ"));
  await worker.fetch(chatReq({ agent: "hermes", rm: "HACKER", messages: userMsg }), env);
  assert.ok(!lastSystem.includes("The user is RM"));
});

test("hermes context carries rm= ownership tags", async () => {
  await worker.fetch(chatReq({ agent: "hermes", messages: userMsg }), env);
  assert.ok((lastSystem.match(/rm=/g) || []).length > 20, "expected many rm= tags");
});

test("RM-priority slicing: the user's filing rows fill the cap first", async () => {
  const pulse = JSON.parse(await readFile("./data/disclosure-pulse.json", "utf-8"));
  const tickers = JSON.parse(await readFile("./data/tickers.json", "utf-8"));
  const champTks = new Set(tickers.tickers.filter((t) => t.rm === "Champ").map((t) => t.tk));
  const champRows = pulse.filings.filter((f) => champTks.has(f.tk)).length;
  const CAP = 60; // keep in sync with ctxFilings

  await worker.fetch(chatReq({ agent: "hermes", rm: "Champ", messages: userMsg }), env);
  // Anchor on the data-section header ("SET DISCLOSURES (last N days…"), not the
  // bare phrase — the Hermes persona now also mentions "SET DISCLOSURES" by name.
  const section = lastSystem.split("SET DISCLOSURES (last")[1]?.split("OVERDUE")[0] || "";
  // count data rows only ("YYYY-MM-DD TK rm=Champ ..."), not the header note
  const got = (section.match(/^\d{4}-\d{2}-\d{2} \S+ rm=Champ /gm) || []).length;
  // min(cap, all of Champ's rows) must be Champ's — none displaced by others
  assert.equal(got, Math.min(CAP, champRows),
    `expected ${Math.min(CAP, champRows)} Champ filing rows in context, got ${got}`);
});

test("hermes is told to merge external news + SET disclosures, both blocks present", async () => {
  await worker.fetch(chatReq({ agent: "hermes", messages: userMsg }), env);
  // persona instruction to use both sources
  assert.ok(/ALWAYS covers BOTH sources/.test(lastSystem),
    "expected the both-sources instruction in Hermes' persona");
  assert.ok(lastSystem.includes("📰 External news") && lastSystem.includes("📄 SET disclosures"),
    "expected both labelled-section headers in the persona/few-shot");
  // and both data blocks actually fed in as context
  assert.ok(/EXTERNAL NEWS \(last/.test(lastSystem), "expected EXTERNAL NEWS data block");
  assert.ok(/SET DISCLOSURES \(last/.test(lastSystem), "expected SET DISCLOSURES data block");
});

test("atlas persona enforces strict threshold math + table format", async () => {
  await worker.fetch(chatReq({ agent: "atlas", messages: userMsg }), env);
  assert.ok(/THRESHOLD MATH IS STRICT/.test(lastSystem), "expected strict-threshold rule");
  assert.ok(/never round toward the threshold/.test(lastSystem), "expected no-rounding rule");
  assert.ok(/EXAMPLE — user:/.test(lastSystem), "expected an Atlas few-shot example");
});

test("pythia persona ranks from aggregates + separates fact from AI view", async () => {
  await worker.fetch(chatReq({ agent: "pythia", messages: userMsg }), env);
  assert.ok(/RANK FROM THE NUMBERS/.test(lastSystem), "expected ranking-from-data rule");
  assert.ok(/SEPARATE FACT FROM VIEW/.test(lastSystem), "expected fact-vs-commentary rule");
  // both data blocks Pythia reasons over must be present
  assert.ok(/SECTOR AGGREGATES/.test(lastSystem), "expected SECTOR AGGREGATES block");
  assert.ok(/AI COMMENTARY/.test(lastSystem), "expected AI COMMENTARY reference");
});

test("naming a covered ticker filters Hermes context to that ticker", async () => {
  // pick a real covered symbol from the data
  const tickers = JSON.parse(await readFile("./data/tickers.json", "utf-8"));
  const tk = tickers.tickers[0].tk;
  await worker.fetch(chatReq({ agent: "hermes", messages: [{ role: "user", content: `any news on ${tk}?` }] }), env);
  assert.ok(lastSystem.includes(`FILTERED to ${tk}`),
    "expected news + disclosures context filtered to the named ticker");
  // a generic question must NOT trigger focus filtering
  await worker.fetch(chatReq({ agent: "hermes", messages: [{ role: "user", content: "what moved today?" }] }), env);
  assert.ok(!/FILTERED to/.test(lastSystem), "generic question should not filter");
});

test("plain 'news on X' does NOT trigger the on-demand PDF summary path", async () => {
  // No summarize/explain intent -> docSummaryBlock must not run (no network fetch).
  const tk = JSON.parse(await readFile("./data/tickers.json", "utf-8")).tickers[0].tk;
  const r = await worker.fetch(chatReq({ agent: "hermes", messages: [{ role: "user", content: `any news on ${tk}?` }] }), env);
  assert.equal(r.status, 200);
  assert.ok(!/FILED-DOCUMENT SUMMARIES/.test(lastSystem),
    "PDF summary block should only appear on an explicit summarize request");
});

test("atlas 'beyond ±X%' query hard-filters prices to qualifying rows only", async () => {
  await worker.fetch(chatReq({ agent: "atlas", messages: [{ role: "user", content: "movers beyond +/-2% today" }] }), env);
  assert.ok(/PRE-FILTERED/.test(lastSystem), "expected the pre-filter note");
  const block = lastSystem.split("TICKERS (tk")[1] || "";
  const moves = [...block.matchAll(/^\S+ \S+ \S+ \| \S+ (-?\d+(?:\.\d+)?)/gm)].map((m) => +m[1]);
  assert.ok(moves.length > 0, "expected some qualifying rows");
  assert.ok(moves.every((v) => Math.abs(v) >= 2), `every shown row must clear ±2; got ${moves.filter(v=>Math.abs(v)<2)}`);
  // a bare "top movers" (no threshold) must NOT pre-filter
  await worker.fetch(chatReq({ agent: "atlas", messages: [{ role: "user", content: "top movers today" }] }), env);
  assert.ok(!/PRE-FILTERED/.test(lastSystem), "no threshold should not pre-filter");
});

test("atlas prices are pre-sorted by absolute 1-day move", async () => {
  await worker.fetch(chatReq({ agent: "atlas", messages: userMsg }), env);
  const block = lastSystem.split("TICKERS (tk")[1] || "";
  const moves = [...block.matchAll(/^\S+ \S+ \S+ \| \S+ (-?\d+(?:\.\d+)?)/gm)].map((m) => Math.abs(+m[1]));
  const sorted = moves.every((v, i) => i === 0 || moves[i - 1] >= v);
  assert.ok(moves.length > 20 && sorted, "expected price rows sorted by |1d%| desc");
});

test("ticker symbols are uppercased instruction present (linkability)", async () => {
  await worker.fetch(chatReq({ agent: "atlas", messages: userMsg }), env);
  assert.ok(lastSystem.includes("UPPERCASE"));
});

test("agents are told to use ticker symbols only, never expand to company names", async () => {
  for (const agent of ["atlas", "hermes", "pythia"]) {
    await worker.fetch(chatReq({ agent, messages: userMsg }), env);
    assert.ok(/TICKERS ONLY, NEVER NAMES/.test(lastSystem),
      `expected the no-company-names rule for ${agent}`);
    assert.ok(/do not have the name mapping/i.test(lastSystem),
      `expected the no-guessing rationale for ${agent}`);
  }
});
