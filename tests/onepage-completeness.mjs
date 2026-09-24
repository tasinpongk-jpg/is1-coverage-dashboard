// Builds the One-Page Summary model for every covered ticker and reports data gaps.
// Fails only on renderer bugs (throw / required field missing when the source row has it);
// data gaps are printed, not failed.  Run: node tests/onepage-completeness.mjs
import fs from "node:fs";
import path from "node:path";
import assert from "node:assert/strict";
import { createRequire } from "node:module";

const root = process.cwd();
const { buildOnePageModel, ONEPAGE_SOURCES } = createRequire(import.meta.url)(path.join(root, "one-page-model.js"));

const D = {};
for (const s of ONEPAGE_SOURCES) {
  const f = path.join(root, "data", s + ".json");
  D[s] = fs.existsSync(f) ? JSON.parse(fs.readFileSync(f, "utf8")) : null;
}

// ── unit checks ──
assert.equal(buildOnePageModel("NOPE_TK", D), null, "unknown ticker -> null");
assert.equal(buildOnePageModel("PRG", {}), null, "empty data -> null, no throw");
{
  const syn = {
    "ticker-summary": { asOf: "2026-07-10", tickers: [{ tk: "ZZ", name: "Z Co", last: 1,
      highlights: [{ year: 2025, months: 12, revenue: 1 }, { year: 2026, months: 3, quarter: "Q1", revenue: 1 }] }] },
    "bond-summary": { issuers: [{ tk: "ZZ", totalOutstanding: 500, bonds: [{ symbol: "ZZ26", maturityDate: "2026-01-01", outstanding: 500 }] }] },
    "visits": { rows: [{ tk: "ZZ", thesis: "Good co *(draft — auto, edit me)*", thesisDraft: true }] },
  };
  const m = buildOnePageModel("zz", syn);
  assert.equal(m.debt.nextMaturity, null, "all maturities before asOf -> nextMaturity null");
  assert.equal(m.debt.outstandingBn, 0.5);
  assert.deepEqual(m.financials.rows.map((r) => r.period), ["FY2025", "Q1/2026"]);
  assert.equal(m.thesis, "Good co", "draft suffix stripped");
  assert.equal(m.thesisIsDraft, true);
  assert.deepEqual(m.missingRequired, []);
}

// ── full coverage sweep ──
const tickers = D["ticker-summary"].tickers;
const bugs = [], dataGaps = [], okCount = {}, gapCount = [];
for (const t of tickers) {
  let m;
  try { m = buildOnePageModel(t.tk, D); } catch (e) { bugs.push(`${t.tk}: threw ${e.message}`); continue; }
  if (!m) { bugs.push(`${t.tk}: model null`); continue; }
  for (const r of m.missingRequired) {
    const hasSource = (r === "name" && t.name) || (r === "price" && t.last != null) ||
      (r === "financials" && (t.highlights || []).length) || (r === "thesisOrBusiness" && t.businessType);
    (hasSource ? bugs : dataGaps).push(`${t.tk}: missing ${r}`);
  }
  let gaps = 0;
  for (const c of m.completeness) {
    okCount[c.key] = (okCount[c.key] || 0) + (c.ok ? 1 : 0);
    if (c.ok && !c.stale) okCount[c.key + " (current)"] = (okCount[c.key + " (current)"] || 0) + 1;
    if (!c.ok) gaps++;
  }
  gapCount.push([t.tk, gaps, m.completeness.filter((c) => !c.ok).map((c) => c.key).join(",")]);
}

const n = tickers.length;
console.log(`One-Page completeness — ${n} tickers, asOf ${D["ticker-summary"].asOf}`);
console.log(`All required fields present: ${n - new Set([...bugs, ...dataGaps].map((s) => s.split(":")[0])).size}/${n}\n`);
for (const [k, v] of Object.entries(okCount).filter(([k]) => !k.endsWith("(current)") || /^(mda|fsNotes)/.test(k))) console.log(`  ${k.padEnd(15)} ${String(v).padStart(3)}/${n}  ${"█".repeat(Math.round((v / n) * 30))}`);
console.log("\nTop 10 tickers with most gaps:");
gapCount.sort((a, b) => b[1] - a[1]).slice(0, 10).forEach(([tk, g, keys]) => console.log(`  ${tk.padEnd(8)} ${g}  ${keys}`));
if (dataGaps.length) console.log(`\nRequired-field DATA gaps (${dataGaps.length}):\n  ` + dataGaps.join("\n  "));
if (bugs.length) { console.error(`\nRENDERER BUGS (${bugs.length}):\n  ` + bugs.join("\n  ")); process.exit(1); }
console.log("\nonepage completeness check passed");
