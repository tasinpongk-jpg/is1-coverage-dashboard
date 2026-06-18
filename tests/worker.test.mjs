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

test("feedback endpoint records a vote (auth + validation)", async () => {
  const fb = (body, token = "testtoken") => new Request("https://x.test/api/feedback", {
    method: "POST", headers: token ? { Authorization: `Bearer ${token}` } : {}, body: JSON.stringify(body),
  });
  // happy path: logs (no KV bound in test env)
  let r = await worker.fetch(fb({ agent: "atlas", vote: "down", question: "q", reply: "a" }), env);
  assert.equal(r.status, 200);
  assert.equal((await r.json()).stored, "log");
  // invalid vote -> 400
  r = await worker.fetch(fb({ agent: "atlas", vote: "meh" }), env);
  assert.equal(r.status, 400);
  // bad token -> 401
  r = await worker.fetch(fb({ vote: "up" }, "wrong"), env);
  assert.equal(r.status, 401);
  // GET export with token -> 200 (no KV bound in test -> empty + note)
  r = await worker.fetch(new Request("https://x.test/api/feedback", { method: "GET", headers: { Authorization: "Bearer testtoken" } }), env);
  assert.equal(r.status, 200);
  assert.deepEqual((await r.json()).votes, []);
  // GET export without token -> 401
  r = await worker.fetch(new Request("https://x.test/api/feedback", { method: "GET" }), env);
  assert.equal(r.status, 401);
  // PUT -> 405
  r = await worker.fetch(new Request("https://x.test/api/feedback", { method: "PUT" }), env);
  assert.equal(r.status, 405);
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
  // a generic question (no ticker, no date word) must NOT trigger filtering
  await worker.fetch(chatReq({ agent: "hermes", messages: [{ role: "user", content: "give me an overview of the market" }] }), env);
  assert.ok(!/FILTERED to/.test(lastSystem), "generic question should not filter");
});

test("plain 'news on X' does NOT trigger the on-demand PDF summary path", async () => {
  // No summarize/explain intent -> docSummaryBlock must not run (no network fetch).
  const tk = JSON.parse(await readFile("./data/tickers.json", "utf-8")).tickers[0].tk;
  const r = await worker.fetch(chatReq({ agent: "hermes", messages: [{ role: "user", content: `any news on ${tk}?` }] }), env);
  assert.equal(r.status, 200);
  const d = await r.json();
  // The summarize path short-circuits to Gemini (model=gemini-*). A plain news
  // query must take the normal chat-model path instead — proves it didn't fire.
  assert.ok(/llama/i.test(d.model), `plain news should use the chat model, got ${d.model}`);
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

test("atlas range query keeps only rows inside the band", async () => {
  await worker.fetch(chatReq({ agent: "atlas", messages: [{ role: "user", content: "names between -2% and -1.5% today" }] }), env);
  assert.ok(/between -2% and -1.5%/.test(lastSystem), "expected the range pre-filter note");
  const block = lastSystem.split("TICKERS (tk")[1] || "";
  const moves = [...block.matchAll(/^\S+ \S+ \S+ \| \S+ (-?\d+(?:\.\d+)?)/gm)].map((m) => +m[1]);
  assert.ok(moves.every((v) => v >= -2 && v <= -1.5), `rows must be in [-2,-1.5]; got ${moves.filter(v => v < -2 || v > -1.5)}`);
});

test("atlas top-N by metric returns exactly N rows, sorted", async () => {
  await worker.fetch(chatReq({ agent: "atlas", messages: [{ role: "user", content: "top 5 names by YTD" }] }), env);
  assert.ok(/top 5|YTD %/.test(lastSystem), "expected top-N + YTD metric note");
  const block = lastSystem.split("TICKERS (tk")[1] || "";
  const rows = (block.match(/^\S+ \S+ \S+ \| /gm) || []).length;
  assert.ok(rows === 5, `expected exactly 5 rows, got ${rows}`);
});

test("recency word date-filters Hermes news/filings context", async () => {
  await worker.fetch(chatReq({ agent: "hermes", messages: [{ role: "user", content: "any disclosures this week?" }] }), env);
  assert.ok(/FILTERED to the last 7 days/.test(lastSystem), "expected a 7-day recency filter note");
});

test("naming a sector scopes Atlas prices to that sector", async () => {
  await worker.fetch(chatReq({ agent: "atlas", messages: [{ role: "user", content: "show me movers in FOOD" }] }), env);
  assert.ok(/Scoped to the FOOD sector/.test(lastSystem), "expected FOOD sector scope note");
  const block = lastSystem.split("TICKERS (tk")[1] || "";
  const sectors = [...block.matchAll(/^\S+ (\S+) \S+ \| /gm)].map((m) => m[1]);
  assert.ok(sectors.length > 0 && sectors.every((s) => s === "FOOD"), `all rows must be FOOD; got ${[...new Set(sectors)]}`);
});

test("naming a sector scopes Hermes news/filings", async () => {
  await worker.fetch(chatReq({ agent: "hermes", messages: [{ role: "user", content: "any news in PROP?" }] }), env);
  assert.ok(/SCOPED to PROP/.test(lastSystem), "expected PROP sector scope note");
});

test("topical keywords switch news/filings to relevance ranking", async () => {
  await worker.fetch(chatReq({ agent: "hermes", messages: [{ role: "user", content: "any dividend announcements?" }] }), env);
  assert.ok(/ranked by relevance to: .*dividend/.test(lastSystem), "expected relevance ranking on 'dividend'");
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

test("output verification flags an ungrounded ticker the model invents", async () => {
  // Make the stub model emit a covered ticker that is NOT in its context.
  const tickers = JSON.parse(await readFile("./data/tickers.json", "utf-8")).tickers;
  // a covered ticker very unlikely to be in a single-ticker focused context
  const other = tickers[tickers.length - 1].tk;
  const saved = env.AI.run;
  env.AI.run = async (_m, opts) => { lastSystem = opts.messages[0].content; return { response: `You might also look at ${other}.` }; };
  try {
    // focus on tickers[0] so the context is a different name; reply names `other`
    const r = await worker.fetch(chatReq({ agent: "atlas", messages: [{ role: "user", content: `price of ${tickers[0].tk}?` }] }), env);
    const d = await r.json();
    // `other` only counts as ungrounded if it wasn't in the (focused) context
    if (!lastSystem.includes(` ${other} `)) {
      assert.ok(d.reply.includes("⚠ Unverified") && d.reply.includes(other),
        "expected an Unverified flag for the ungrounded ticker");
    }
  } finally { env.AI.run = saved; }
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
