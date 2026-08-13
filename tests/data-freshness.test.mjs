import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const read = (name) => readFile(path.join(root, name), "utf8");

// Both SEC feeds went stale for weeks without the dashboard showing it: the
// daily job rewrites the JSON (refreshing asOf and _built_at) even when the
// upstream scrape returned nothing, so a badge keyed off either timestamp
// reported "updated 2h ago" over rows that were months old. These guard the
// fix — the badge must reflect the age of the rows, not the age of the file.
const SEC_PAGES = ["sec-form59.html", "sec-enforcement.html"];

test("SEC pages badge staleness from the data, not from the build timestamp", async () => {
  for (const page of SEC_PAGES) {
    const html = await read(page);
    assert.match(html, /function dataFreshnessLabel\(payload\)/, `${page} must define dataFreshnessLabel`);
    assert.match(html, /const fresh = dataFreshnessLabel\(dj\)/, `${page} must badge via dataFreshnessLabel`);
    assert.doesNotMatch(
      html,
      /const fresh = freshnessLabel\(dj\._built_at\)/,
      `${page} must not badge straight off _built_at — that is refreshed even when the scrape failed`,
    );
    assert.match(html, /payload\.stale/, `${page} must honour the stale flag`);
    assert.match(html, /payload\.dataAsOf/, `${page} must surface dataAsOf`);
  }
});

test("stale-data strings are translated in both languages", async () => {
  const i18n = await read("i18n.js");
  for (const key of ["common.dataStaleAsOf", "common.dataNeverIngested"]) {
    const hits = i18n.match(new RegExp(`"${key.replace(".", "\\.")}"\\s*:`, "g")) || [];
    assert.equal(hits.length, 2, `${key} needs both an EN and a TH entry`);
  }
  // The pages fall back to a local map when i18n.js has not loaded yet.
  for (const page of SEC_PAGES) {
    const html = await read(page);
    assert.match(html, /"common\.dataStaleAsOf"/, `${page} needs a local fallback for the stale label`);
    assert.match(html, /"common\.dataNeverIngested"/, `${page} needs a local fallback for the empty label`);
  }
});

test("the builder emits freshness fields the pages depend on", async () => {
  const builder = await read("scripts/build_external.py");
  assert.match(builder, /def _stamp_freshness\(/);
  assert.match(builder, /payload\["dataAsOf"\]/);
  assert.match(builder, /payload\["dataAgeDays"\]/);
  assert.match(builder, /payload\["stale"\]/);
  // Both SEC snapshots must be stamped, or the badge silently falls back.
  assert.match(builder, /label="sec_enforcement"/);
  assert.match(builder, /label="sec_form59"/);
});

test("a source that failed to render is distinguishable from a quiet day", async () => {
  const src = await read("surveillance/external_sources.py");
  assert.match(src, /SOURCE_FAILURES/);
  assert.match(src, /def _note_failure\(/);
  // Each best-effort fetcher swallows its own errors, so every failure path
  // that returns empty must record why before it does.
  assert.match(src, /_note_failure\("sec_form59"/);
  assert.match(src, /_note_failure\("sec_enforcement"/);
  assert.match(src, /_note_failure\("external_news"/);
  assert.match(src, /::warning::/, "failures must surface as GitHub annotations");
  assert.match(src, /def _write_source_health\(/);
});
