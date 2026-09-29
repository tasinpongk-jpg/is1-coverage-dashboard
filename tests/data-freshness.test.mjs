import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const read = (name) => readFile(path.join(root, name), "utf8");

// Both SEC feeds went stale for weeks while the daily job kept rewriting the
// JSON (refreshing asOf and _built_at) over rows that were months old. Their
// pages are gone, but the one-page summary and the Hermes agent still read
// sec-enforcement.json and sec-form59.json, so the builder must keep stamping
// the age of the rows, not the age of the file.
test("the builder emits freshness fields downstream readers depend on", async () => {
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
