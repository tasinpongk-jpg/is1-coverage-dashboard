import { test } from "node:test";
import assert from "node:assert/strict";
import { readFile, readdir } from "node:fs/promises";

const htmlFiles = (await readdir(".")).filter((name) => name.endsWith(".html"));

test("every page loads the appearance runtime before the shared theme", async () => {
  assert.ok(htmlFiles.length >= 17, "expected the full dashboard page set");
  for (const file of htmlFiles) {
    const source = await readFile(file, "utf8");
    const runtime = source.search(/src="theme\.js(?:\?[^"#]*)?"/);
    const styles = source.search(/href="theme\.css(?:\?[^"#]*)?"/);
    assert.ok(runtime >= 0, `${file} must load theme.js`);
    assert.ok(styles >= 0, `${file} must load theme.css`);
    assert.ok(runtime < styles, `${file} must apply the saved theme before shared CSS`);
  }
});

test("shared CSS defines both modes and reduced-motion behavior", async () => {
  const css = await readFile("theme.css", "utf8");
  assert.match(css, /:root\[data-theme="dark"\]/);
  assert.match(css, /:root\[data-theme="light"\]/);
  assert.match(css, /prefers-reduced-motion:reduce/);
  assert.match(css, /\.theme-switch/);
  assert.match(css, /\.motion-reveal\.is-revealed/);
});

test("theme runtime is included in the deployed asset set", async () => {
  const ignored = await readFile(".assetsignore", "utf8");
  assert.doesNotMatch(ignored, /^theme\.js$/m);
});

test("all shared assets use the current cache version", async () => {
  for (const file of htmlFiles) {
    const source = await readFile(file, "utf8");
    for (const asset of ["theme.js", "theme.css", "i18n.js", "nav.js"]) {
      assert.match(source, new RegExp(`${asset.replace(".", "\\.")}\\?v=6`), `${file} must load ${asset} v6`);
    }
  }
});

test("external dashboards open in the embedded right workspace", async () => {
  const nav = await readFile("nav.js", "utf8");
  assert.match(nav, /data-shell-embed/);
  assert.match(nav, /searchParams\.set\("embedded","1"\)/);
  assert.match(nav, /new URLSearchParams\(location\.search\)\.get\("embedded"\) === "1"/);
  assert.match(nav, /className = "is1s-workspace"/);

  const dock = await readFile("chat-dock.js", "utf8");
  assert.match(dock, /get\("embedded"\) === "1"\) return/);
});

test("RM-aware pages hydrate from and follow the shared RM selector", async () => {
  const pages = [
    "ai-insights.html", "bond-data-sec.html", "bond-summary.html", "company-summary.html",
    "disclosure-pulse.html", "external-news.html", "multiples-band.html",
    "multiples-comparison.html", "oppday-minutes.html", "price-movement.html",
    "sec-enforcement.html", "sec-form59.html", "trading-signs.html",
    "unusual-trading.html", "visits.html",
  ];
  for (const file of pages) {
    const source = await readFile(file, "utf8");
    assert.match(source, /localStorage\.getItem\(['"]is1_rm['"]\)/, `${file} must hydrate the saved RM`);
    assert.match(source, /is1:rm-change/, `${file} must react to RM changes`);
  }
});

test("Oppday drawer owns its scroll area and Form 59 has a populated snapshot", async () => {
  const oppday = await readFile("oppday-minutes.html", "utf8");
  assert.match(oppday, /\.drawer-body\s*\{[^}]*overflow-y\s*:\s*auto/s);
  assert.match(oppday, /querySelector\(['"]\.drawer-body['"]\)\.scrollTop\s*=\s*0/);

  const form59 = JSON.parse(await readFile("data/sec-form59.json", "utf8"));
  assert.ok(form59.total > 0, "Form 59 snapshot must not be empty");
  assert.equal(form59.total, form59.items.length);
  assert.ok(form59.windowDays >= 7);
});
