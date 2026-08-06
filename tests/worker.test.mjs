// Tests for worker.js /api/chat — run with `node --test tests/` from repo root.
// Stubs env.ASSETS (reads local data/*.json) and the MiniMax HTTP endpoint,
// so this exercises routing, auth, agent selection, context building and the
// RM-priority slicing without touching Cloudflare.

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import worker, { buildSectorMetrics, parseEfinanceNewsHtml, resolveLexCitations, retrieveLexChunks } from "../worker.js";

let lastSystem = "";
let lastMiniMaxRequest = null;
const env = {
  CHAT_TOKEN: "testtoken",
  MINIMAX_API_KEY: "test-minimax-key",
  ASSETS: {
    fetch: async (req) => {
      const p = new URL(req.url).pathname;
      try { return new Response(await readFile("." + p)); }
      catch { return new Response("not found", { status: 404 }); }
    },
  },
  MINIMAX_FETCH: async (url, opts) => {
    const body = JSON.parse(opts.body);
    lastSystem = body.messages[0].content;
    lastMiniMaxRequest = { url, opts, body };
    return new Response(JSON.stringify({
      model: "MiniMax-M3",
      choices: [{ finish_reason: "stop", message: { role: "assistant", content: "stub-reply" } }],
      base_resp: { status_code: 0, status_msg: "" },
    }), { headers: { "Content-Type": "application/json" } });
  },
};

function chatReq(body, token = "testtoken") {
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;
  return new Request("https://x.test/api/chat", {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });
}
const userMsg = [{ role: "user", content: "hi" }];
const lexCorpus = JSON.parse(await readFile("./data/lex-regulations.json", "utf-8"));

test("Lex corpus records a complete page-level source set", () => {
  assert.equal(lexCorpus.schemaVersion, 1);
  assert.equal(lexCorpus.documentCount, 79);
  assert.equal(lexCorpus.documents.length, 79);
  assert.equal(lexCorpus.pageCount, 560);
  assert.equal(lexCorpus.chunkCount, lexCorpus.chunks.length);
  assert.ok(lexCorpus.documents.every((doc) => /^[a-f0-9]{64}$/.test(doc.sha256)));
  assert.ok(lexCorpus.chunks.every((chunk) =>
    chunk.document.endsWith(".pdf") && chunk.page > 0 && chunk.text.length > 0));
});

test("eFinanceThai parser extracts safe headline links from embedded JSON", () => {
  const upstream = {
    TotalPage: 36,
    PageSize: 15,
    Data: [
      {
        id: 7628623,
        LastUpdate: "2026-08-06 10:01:00",
        title: "CPN reports {growth} and says \"outlook strong\"",
        security: "cpn",
        full_path_link: "https://www.efinancethai.com/LastestNews/LatestNewsMain.aspx?id=abc",
      },
      {
        id: 2,
        LastUpdate: "2026-08-06 09:00:00",
        title: "Unsafe host",
        security: "BAD",
        full_path_link: "https://example.com/LastestNews/LatestNewsMain.aspx?id=bad",
      },
    ],
  };
  const parsed = parseEfinanceNewsHtml(`<script>var jsonscript = ${JSON.stringify(upstream)};jQuery("ignored");</script>`);
  assert.equal(parsed.totalPages, 36);
  assert.equal(parsed.pageSize, 15);
  assert.equal(parsed.count, 1);
  assert.equal(parsed.items[0].id, 7628623);
  assert.equal(parsed.items[0].ticker, "CPN");
  assert.equal(parsed.items[0].publishedAt, "2026-08-06T03:01:00.000Z");
  assert.match(parsed.items[0].url, /^https:\/\/www\.efinancethai\.com\/LastestNews\/LatestNewsMain\.aspx\?id=abc$/);
});

test("GET /api/efinance-news returns cached headline-link JSON", async () => {
  const upstream = {
    TotalPage: 1,
    PageSize: 15,
    Data: [{
      id: 7628623,
      LastUpdate: "2026-08-06 10:01:00",
      title: "Latest SET headline",
      security: "CPN",
      full_path_link: "https://www.efinancethai.com/LastestNews/LatestNewsMain.aspx?id=abc",
    }],
  };
  let upstreamRequest = null;
  const newsEnv = {
    ...env,
    EFINANCE_FETCH: async (url, options) => {
      upstreamRequest = { url, options };
      return new Response(`<script>var jsonscript = ${JSON.stringify(upstream)};jQuery("ok");</script>`);
    },
  };
  const response = await worker.fetch(new Request("https://x.test/api/efinance-news"), newsEnv);
  assert.equal(response.status, 200);
  assert.match(response.headers.get("Cache-Control"), /s-maxage=300/);
  assert.equal(response.headers.get("X-Content-Type-Options"), "nosniff");
  assert.equal(upstreamRequest.url, "https://www.efinancethai.com/LastestNews/AllLatestNews.aspx");
  assert.equal(upstreamRequest.options.cf.cacheTtl, 300);
  const data = await response.json();
  assert.equal(data.source, "eFinanceThai");
  assert.equal(data.count, 1);
  assert.equal(data.items[0].title, "Latest SET headline");
  assert.ok(data.fetchedAt);
});

test("/api/efinance-news rejects non-GET methods", async () => {
  const response = await worker.fetch(new Request("https://x.test/api/efinance-news", { method: "POST" }), env);
  assert.equal(response.status, 405);
  assert.equal(response.headers.get("Allow"), "GET");
});

test("MiniMax-backed agents respond 200 and report grounded metadata", async () => {
  for (const agent of ["atlas", "hermes"]) {
    const r = await worker.fetch(chatReq({ agent, messages: userMsg }), env);
    assert.equal(r.status, 200);
    const d = await r.json();
    assert.equal(d.agent, agent);
    assert.match(d.reply, /^stub-reply/);
    assert.match(d.reply, /Data as of \d{4}-\d{2}-\d{2}/);
    assert.equal(d.model, "MiniMax-M3");
    assert.ok(d.meta.asOf);
    assert.ok(d.meta.sources.length >= 2);
  }
});

test("Pythia redirects unsupported questions without calling an LLM", async () => {
  lastMiniMaxRequest = null;
  const r = await worker.fetch(chatReq({ agent: "pythia", messages: userMsg }), env);
  assert.equal(r.status, 200);
  const d = await r.json();
  assert.equal(d.agent, "pythia");
  assert.equal(d.model, "deterministic");
  assert.match(d.reply, /Questions supported by the current data/);
  assert.equal(lastMiniMaxRequest, null);
});

test("chat calls the MiniMax M3 server API with grounded messages", async () => {
  const r = await worker.fetch(chatReq({ agent: "atlas", messages: userMsg }), env);
  assert.equal(r.status, 200);
  assert.equal(lastMiniMaxRequest.url, "https://api.minimax.io/v1/text/chatcompletion_v2");
  assert.equal(lastMiniMaxRequest.opts.method, "POST");
  assert.equal(lastMiniMaxRequest.opts.headers.Authorization, "Bearer test-minimax-key");
  assert.equal(lastMiniMaxRequest.body.model, "MiniMax-M3");
  assert.equal(lastMiniMaxRequest.body.messages.at(-1).content, "hi");
  assert.match(lastMiniMaxRequest.body.messages[0].content, /DATA:/);
  assert.equal(lastMiniMaxRequest.body.max_tokens, 2200);
});

test("sector metrics canonicalize PF&REIT and exclude null values from averages", () => {
  const metrics = buildSectorMetrics({ rows: [
    { tk: "A", sector: "PFREIT", pct1d: 2, pct5d: 4, pctYtd: null },
    { tk: "B", sector: "PF&REIT", pct1d: null, pct5d: 8, pctYtd: 10 },
    { tk: "C", sector: "FOOD", pct1d: -1, pct5d: null, pctYtd: -5 },
  ] });
  const reit = metrics.find((row) => row.sector === "PF&REIT");
  assert.equal(reit.count, 2);
  assert.equal(reit.count1d, 1);
  assert.equal(reit.avg1d, 2);
  assert.equal(reit.avg5d, 6);
  assert.equal(reit.avgYtd, 10);
  assert.equal(reit.up, 1);
});

test("Pythia answers supported sector screens deterministically", async () => {
  lastMiniMaxRequest = null;
  const r = await worker.fetch(chatReq({
    agent: "pythia",
    messages: [{ role: "user", content: "Rank all 6 IS1 sectors by 1-day return and breadth" }],
  }), env);
  assert.equal(r.status, 200);
  const d = await r.json();
  assert.equal(d.model, "deterministic");
  assert.equal(d.meta.asOf, "2026-07-22");
  assert.match(d.reply, /Median 1d/);
  assert.match(d.reply, /Avg 5d/);
  assert.match(d.reply, /PF&REIT/);
  assert.equal(lastMiniMaxRequest, null);
});

test("Pythia rejects unsupported macro questions with answerable alternatives", async () => {
  lastMiniMaxRequest = null;
  const r = await worker.fetch(chatReq({
    agent: "pythia",
    messages: [{ role: "user", content: "What is the SET Index outlook and foreign fund flow today?" }],
  }), env);
  assert.equal(r.status, 200);
  const d = await r.json();
  assert.equal(d.model, "deterministic");
  assert.match(d.reply, /does not have SET Index/i);
  assert.match(d.reply, /Rank all 6 IS1 sectors/);
  assert.equal(lastMiniMaxRequest, null);
});

test("Lex retrieves page-level rules and answers through MiniMax M3", async () => {
  const r = await worker.fetch(chatReq({
    agent: "lex",
    messages: [{ role: "user", content: "When is a connected transaction subject to shareholder approval?" }],
  }), env);
  assert.equal(r.status, 200);
  const d = await r.json();
  assert.equal(d.agent, "lex");
  assert.equal(d.model, "MiniMax-M3");
  assert.match(d.reply, /Sources retrieved:/);
  assert.match(lastSystem, /REGULATION CORPUS: 79 documents/);
  assert.match(lastSystem, /รายการที่เกี่ยวโยงกัน\.pdf \| p\.6/);
  assert.doesNotMatch(lastMiniMaxRequest.url, /googleapis|gemini/i);
  assert.equal(lastMiniMaxRequest.body.max_tokens, 5000);
  assert.equal(lastMiniMaxRequest.body.temperature, 0.1);
});

test("Lex retrieval finds the intended documents for every sample question", () => {
  const cases = [
    ["When is a connected transaction subject to shareholder approval?", /รายการที่เกี่ยวโยงกัน\.pdf/],
    ["What must a listed company disclose after a board resolution?", /การเปิดเผยข้อมูลตามเหตุการณ์\.pdf/],
    ["อธิบายเกณฑ์ free float ของ SET", /Free_Float\.pdf/],
  ];
  for (const [question, expected] of cases) {
    const rows = retrieveLexChunks(lexCorpus, question);
    assert.equal(rows.length, 8);
    assert.match(rows[0].document, expected);
    assert.ok(rows.every((row) => row.page > 0 && row.text.length > 0));
  }
});

test("Lex expands source IDs and removes non-retrieved citation labels", () => {
  const chunks = [
    { document: "กฎหนึ่ง.pdf", page: 2 },
    { document: "rule-two.pdf", page: 7 },
  ];
  const reply = resolveLexCitations(
    "Threshold [S1]. Condition [S2]. Unknown [S9]. Fake [short-name.pdf p.4].",
    chunks,
  );
  assert.match(reply, /\[กฎหนึ่ง\.pdf p\.2\]/);
  assert.match(reply, /\[rule-two\.pdf p\.7\]/);
  assert.doesNotMatch(reply, /S9|short-name/);
});

test("Lex rejects off-topic questions without calling an LLM", async () => {
  lastMiniMaxRequest = null;
  const r = await worker.fetch(chatReq({
    agent: "lex",
    messages: [{ role: "user", content: "How do I cook pad thai?" }],
  }), env);
  assert.equal(r.status, 200);
  const d = await r.json();
  assert.equal(d.model, "MiniMax-M3");
  assert.match(d.reply, /only answers SET\/SEC rules/i);
  assert.equal(lastMiniMaxRequest, null);
});

test("Lex reports a missing regulation corpus as 503", async () => {
  const missingCorpusEnv = {
    ...env,
    ASSETS: {
      fetch: async (req) => new URL(req.url).pathname === "/data/lex-regulations.json"
        ? new Response("not found", { status: 404 })
        : env.ASSETS.fetch(req),
    },
  };
  const r = await worker.fetch(chatReq({
    agent: "lex",
    messages: [{ role: "user", content: "Explain the free float rule" }],
  }), missingCorpusEnv);
  assert.equal(r.status, 503);
  assert.match((await r.json()).error, /regulation corpus is missing/);
});

test("chat reports missing MiniMax configuration without calling an alternate model", async () => {
  const r = await worker.fetch(chatReq({ agent: "atlas", messages: userMsg }), {
    ...env,
    MINIMAX_API_KEY: "",
  });
  assert.equal(r.status, 503);
  assert.match((await r.json()).error, /missing MINIMAX_API_KEY/);
});

test("chat converts MiniMax upstream failures and empty answers to 502", async () => {
  let r = await worker.fetch(chatReq({ agent: "atlas", messages: userMsg }), {
    ...env,
    MINIMAX_FETCH: async () => new Response(JSON.stringify({
      base_resp: { status_code: 1001, status_msg: "bad request" },
    }), { status: 400, headers: { "Content-Type": "application/json" } }),
  });
  assert.equal(r.status, 502);

  r = await worker.fetch(chatReq({ agent: "atlas", messages: userMsg }), {
    ...env,
    MINIMAX_FETCH: async () => new Response(JSON.stringify({
      model: "MiniMax-M3",
      choices: [{ message: { content: "" } }],
      base_resp: { status_code: 0, status_msg: "" },
    }), { headers: { "Content-Type": "application/json" } }),
  });
  assert.equal(r.status, 502);
});

test("chat retries an empty MiniMax answer with a larger token budget", async () => {
  const budgets = [];
  const r = await worker.fetch(chatReq({ agent: "atlas", messages: userMsg }), {
    ...env,
    MINIMAX_FETCH: async (_url, opts) => {
      budgets.push(JSON.parse(opts.body).max_tokens);
      return new Response(JSON.stringify({
        model: "MiniMax-M3",
        choices: [{
          finish_reason: budgets.length === 1 ? "length" : "stop",
          message: { content: budgets.length === 1 ? "" : "recovered-reply" },
        }],
        base_resp: { status_code: 0, status_msg: "" },
      }), { headers: { "Content-Type": "application/json" } });
    },
  });
  assert.equal(r.status, 200);
  assert.match((await r.json()).reply, /^recovered-reply/);
  assert.deepEqual(budgets, [2200, 5000]);
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

  let bad = await worker.fetch(new Request("https://x.test/api/chat", {
    method: "POST",
    headers: { Authorization: "Bearer testtoken" },
    body: JSON.stringify({ messages: userMsg }),
  }), env);
  assert.equal(bad.status, 415);

  bad = await worker.fetch(new Request("https://x.test/api/chat", {
    method: "POST",
    headers: { Authorization: "Bearer testtoken", "Content-Type": "application/json", "Content-Length": String(64 * 1024 + 1) },
    body: "{}",
  }), env);
  assert.equal(bad.status, 413);

  bad = await worker.fetch(new Request("https://x.test/api/chat", {
    method: "POST",
    headers: { Authorization: "Bearer testtoken", "Content-Type": "application/json" },
    body: "{",
  }), env);
  assert.equal(bad.status, 400);

  bad = await worker.fetch(new Request("https://x.test/api/chat", {
    method: "POST",
    headers: { Authorization: "Bearer testtoken", "Content-Type": "application/json" },
    body: "null",
  }), env);
  assert.equal(bad.status, 400);
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
  // KV path normalizes known ids and drops unknown agent/rm values
  const stored = [];
  const fbEnv = { ...env, FEEDBACK: { put: async (_key, value) => { stored.push(JSON.parse(value)); } } };
  r = await worker.fetch(fb({ agent: "ATLAS", rm: "c", vote: "up" }), fbEnv);
  assert.equal(r.status, 200);
  assert.equal(stored[0].agent, "atlas");
  assert.equal(stored[0].rm, "C");
  r = await worker.fetch(fb({ agent: "<img>", rm: "Champ", vote: "up" }), fbEnv);
  assert.equal(r.status, 200);
  assert.equal(stored[1].agent, "");
  assert.equal(stored[1].rm, "");
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
  await worker.fetch(chatReq({ agent: "hermes", rm: "C", messages: userMsg }), env);
  assert.ok(lastSystem.includes("The user is RM C"));
  await worker.fetch(chatReq({ agent: "hermes", rm: "Champ", messages: userMsg }), env);
  assert.ok(!lastSystem.includes("The user is RM"), "legacy full-name rm must be rejected");
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

test("Pythia keeps unsupported market and macro questions inside its verified scope", async () => {
  lastMiniMaxRequest = null;
  const r = await worker.fetch(chatReq({
    agent: "pythia",
    messages: [{ role: "user", content: "Summarize the whole market and next-week outlook" }],
  }), env);
  const d = await r.json();
  assert.equal(d.model, "deterministic");
  assert.match(d.reply, /does not have SET Index/i);
  assert.match(d.reply, /Rank all 6 IS1 sectors/);
  assert.equal(lastMiniMaxRequest, null);
});

test("every generative agent prompt includes a worked response sample", async () => {
  const cases = [
    ["atlas", "top movers", /EXAMPLE — user:/],
    ["hermes", "news today", /EXAMPLE — user:/],
    ["lex", "Explain the free float rule", /SAMPLE FORMAT — user asks/],
  ];
  for (const [agent, question, marker] of cases) {
    await worker.fetch(chatReq({ agent, messages: [{ role: "user", content: question }] }), env);
    assert.match(lastSystem, marker, `expected a worked sample for ${agent}`);
  }
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

test("Hermes news requests always use MiniMax M3", async () => {
  const tk = JSON.parse(await readFile("./data/tickers.json", "utf-8")).tickers[0].tk;
  const r = await worker.fetch(chatReq({ agent: "hermes", messages: [{ role: "user", content: `any news on ${tk}?` }] }), env);
  assert.equal(r.status, 200);
  const d = await r.json();
  assert.equal(d.model, "MiniMax-M3", `plain news should use MiniMax M3, got ${d.model}`);
  assert.deepEqual(d.meta.sources, ["external-news", "disclosure-pulse", "sec-form59", "oppday-minutes"]);
});

test("Hermes normalizes required news sections and always appends snapshot provenance", async () => {
  let calls = 0;
  const sectionEnv = {
    ...env,
    MINIMAX_FETCH: async () => {
      calls += 1;
      return new Response(JSON.stringify({
        model: "MiniMax-M3",
        choices: [{ message: { content: "External news\n• one item\n\nSET disclosures\n• one filing" } }],
        base_resp: { status_code: 0 },
      }), { headers: { "Content-Type": "application/json" } });
    },
  };
  const r = await worker.fetch(chatReq({
    agent: "hermes",
    messages: [{ role: "user", content: "What news moved RM C coverage today?" }],
  }), sectionEnv);
  const d = await r.json();
  assert.equal(calls, 1);
  assert.match(d.reply, /📰 External news/);
  assert.match(d.reply, /📄 SET disclosures/);
  assert.match(d.reply, /Data as of \d{4}-\d{2}-\d{2}/);
});

test("Hermes falls back to grounded context when two model answers miss required sections", async () => {
  let calls = 0;
  const fallbackEnv = {
    ...env,
    MINIMAX_FETCH: async () => {
      calls += 1;
      return new Response(JSON.stringify({
        model: "MiniMax-M3",
        choices: [{ message: { content: "A paragraph without the required structure." } }],
        base_resp: { status_code: 0 },
      }), { headers: { "Content-Type": "application/json" } });
    },
  };
  const r = await worker.fetch(chatReq({
    agent: "hermes",
    messages: [{ role: "user", content: "Update FOOD sector news today" }],
  }), fallbackEnv);
  const d = await r.json();
  assert.equal(calls, 2);
  assert.match(d.reply, /📰 External news/);
  assert.match(d.reply, /📄 SET disclosures/);
  assert.match(d.reply, /\d{4}-\d{2}-\d{2}/);
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

  const savedFetch = env.ASSETS.fetch;
  env.ASSETS.fetch = async (req) => {
    const p = new URL(req.url).pathname;
    if (p === "/data/morning-brief.json") {
      return new Response(JSON.stringify({ asOf: "test", rows: [
        { tk: "MID", pct1d: 0.2, pct5d: 0, pctYtd: 0, volRatio: 1, last: 1, sector: "FOOD" },
        { tk: "NULLY", pct1d: null, pct5d: null, pctYtd: null, volRatio: null, last: 1, sector: "FOOD" },
        { tk: "OUT", pct1d: 5, pct5d: 0, pctYtd: 0, volRatio: 1, last: 1, sector: "FOOD" },
      ] }));
    }
    return savedFetch(req);
  };
  try {
    await worker.fetch(chatReq({ agent: "atlas", messages: [{ role: "user", content: "names between -1% and 1% today" }] }), env);
    const synthetic = lastSystem.split("TICKERS (tk")[1] || "";
    assert.ok(/^MID /m.test(synthetic), "valid in-range row should remain");
    assert.ok(!/^NULLY /m.test(synthetic), "null metric row must not pass range screen");
  } finally {
    env.ASSETS.fetch = savedFetch;
  }
});

test("atlas top-N by metric returns exactly N rows, sorted", async () => {
  await worker.fetch(chatReq({ agent: "atlas", messages: [{ role: "user", content: "top 5 names by YTD" }] }), env);
  assert.ok(/top 5|YTD %/.test(lastSystem), "expected top-N + YTD metric note");
  const block = lastSystem.split("TICKERS (tk")[1] || "";
  const rows = (block.match(/^\S+ \S+ \S+ \| /gm) || []).length;
  assert.ok(rows === 5, `expected exactly 5 rows, got ${rows}`);

  const savedFetch = env.ASSETS.fetch;
  env.ASSETS.fetch = async (req) => {
    const p = new URL(req.url).pathname;
    if (p === "/data/morning-brief.json") {
      return new Response(JSON.stringify({ asOf: "test", rows: [
        { tk: "TOP", pct1d: 1, pct5d: 1, pctYtd: 10, volRatio: 2, last: 1, sector: "FOOD" },
        { tk: "SECOND", pct1d: 1, pct5d: 1, pctYtd: 5, volRatio: 2, last: 1, sector: "FOOD" },
        { tk: "NULLY", pct1d: 1, pct5d: 1, pctYtd: null, volRatio: 2, last: 1, sector: "FOOD" },
      ] }));
    }
    return savedFetch(req);
  };
  try {
    await worker.fetch(chatReq({ agent: "atlas", messages: [{ role: "user", content: "top 3 names by YTD" }] }), env);
    const synthetic = lastSystem.split("TICKERS (tk")[1] || "";
    const syntheticRows = synthetic.match(/^\S+ \S+ \S+ \| /gm) || [];
    assert.equal(syntheticRows.length, 2);
    assert.ok(!/^NULLY /m.test(synthetic), "null metric row must not pass top-N screen");
  } finally {
    env.ASSETS.fetch = savedFetch;
  }
});

test("recency word date-filters Hermes news/filings context", async () => {
  await worker.fetch(chatReq({ agent: "hermes", messages: [{ role: "user", content: "any disclosures this week?" }] }), env);
  assert.ok(/FILTERED to the last 7 days/.test(lastSystem), "expected a 7-day recency filter note");
});

test("lowercase tickers focus context without treating contractions as ticker M", async () => {
  await worker.fetch(chatReq({ agent: "atlas", messages: [{ role: "user", content: "price of cpn" }] }), env);
  assert.match(lastSystem, /focused on CPN/);

  await worker.fetch(chatReq({ agent: "atlas", messages: [{ role: "user", content: "price of M" }] }), env);
  assert.match(lastSystem, /focused on M/);

  await worker.fetch(chatReq({ agent: "atlas", messages: [{ role: "user", content: "Top movers in my coverage. I'm Champ." }] }), env);
  assert.doesNotMatch(lastSystem, /focused on M/);
});

test("Thai recency words date-filter Hermes context", async () => {
  await worker.fetch(chatReq({ agent: "hermes", messages: [{ role: "user", content: "ข่าว CPN วันนี้" }] }), env);
  assert.match(lastSystem, /FILTERED to today/);

  await worker.fetch(chatReq({ agent: "hermes", messages: [{ role: "user", content: "ข่าว CPN เมื่อวาน" }] }), env);
  assert.match(lastSystem, /FILTERED to the last 2 days/);
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

test("PF&REIT sector aliases scope Atlas and Hermes data", async () => {
  await worker.fetch(chatReq({ agent: "atlas", messages: [{ role: "user", content: "show movers in PF&REIT" }] }), env);
  assert.match(lastSystem, /Scoped to the PF&REIT sector/);
  let block = lastSystem.split("TICKERS (tk")[1] || "";
  let sectors = [...block.matchAll(/^\S+ (\S+) \S+ \| /gm)].map((match) => match[1]);
  assert.ok(sectors.length > 0 && sectors.every((sector) => sector === "PF&REIT"));

  await worker.fetch(chatReq({ agent: "hermes", messages: [{ role: "user", content: "news in PFREIT" }] }), env);
  assert.match(lastSystem, /SCOPED to PF&REIT/);
  block = lastSystem.split("EXTERNAL NEWS")[1]?.split("SET DISCLOSURES")[0] || "";
  sectors = [...block.matchAll(/^\d{4}-\d{2}-\d{2} \S+ rm=\S+ (\S+):/gm)].map((match) => match[1]);
  assert.ok(sectors.every((sector) => sector === "PFREIT" || sector === "PF&REIT"));
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
  const saved = env.MINIMAX_FETCH;
  env.MINIMAX_FETCH = async (_url, opts) => {
    const body = JSON.parse(opts.body);
    lastSystem = body.messages[0].content;
    return new Response(JSON.stringify({
      model: "MiniMax-M3",
      choices: [{ message: { content: `You might also look at ${other}.` } }],
      base_resp: { status_code: 0, status_msg: "" },
    }), { headers: { "Content-Type": "application/json" } });
  };
  try {
    // focus on tickers[0] so the context is a different name; reply names `other`
    const r = await worker.fetch(chatReq({ agent: "atlas", messages: [{ role: "user", content: `price of ${tickers[0].tk}?` }] }), env);
    const d = await r.json();
    // `other` only counts as ungrounded if it wasn't in the (focused) context
    if (!lastSystem.includes(` ${other} `)) {
      assert.ok(d.reply.includes("⚠ Unverified") && d.reply.includes(other),
        "expected an Unverified flag for the ungrounded ticker");
    }
  } finally { env.MINIMAX_FETCH = saved; }
});

test("output verification does not treat MD&A as ticker A", async () => {
  const saved = env.MINIMAX_FETCH;
  env.MINIMAX_FETCH = async (_url, opts) => {
    const body = JSON.parse(opts.body);
    lastSystem = body.messages[0].content;
    return new Response(JSON.stringify({
      model: "MiniMax-M3",
      choices: [{ message: { content: "Review the MD&A filing." } }],
      base_resp: { status_code: 0, status_msg: "" },
    }), { headers: { "Content-Type": "application/json" } });
  };
  try {
    const r = await worker.fetch(chatReq({ agent: "hermes", messages: [{ role: "user", content: "summarize CPN filing" }] }), env);
    const d = await r.json();
    assert.match(d.reply, /^Review the MD&A filing\./);
    assert.doesNotMatch(d.reply, /Unverified.*\bA\b/);
  } finally { env.MINIMAX_FETCH = saved; }
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
