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
  const section = lastSystem.split("SET DISCLOSURES")[1]?.split("OVERDUE")[0] || "";
  // count data rows only ("YYYY-MM-DD TK rm=Champ ..."), not the header note
  const got = (section.match(/^\d{4}-\d{2}-\d{2} \S+ rm=Champ /gm) || []).length;
  // min(cap, all of Champ's rows) must be Champ's — none displaced by others
  assert.equal(got, Math.min(CAP, champRows),
    `expected ${Math.min(CAP, champRows)} Champ filing rows in context, got ${got}`);
});

test("ticker symbols are uppercased instruction present (linkability)", async () => {
  await worker.fetch(chatReq({ agent: "atlas", messages: userMsg }), env);
  assert.ok(lastSystem.includes("UPPERCASE"));
});
