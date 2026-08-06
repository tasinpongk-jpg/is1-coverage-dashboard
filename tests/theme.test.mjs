import { test } from "node:test";
import assert from "node:assert/strict";
import { readFile, readdir } from "node:fs/promises";

const htmlFiles = (await readdir(".")).filter((name) => name.endsWith(".html"));

test("eFinanceThai news page is wired through the safe Worker proxy", async () => {
  const [page, nav, home, worker] = await Promise.all([
    readFile("efinance-news.html", "utf8"),
    readFile("nav.js", "utf8"),
    readFile("index.html", "utf8"),
    readFile("worker.js", "utf8"),
  ]);
  assert.match(page, /fetch\('\.\/api\/efinance-news'/);
  assert.match(page, /fetch\('\.\/api\/efinance-news\/summaries'/);
  assert.match(page, /class="summary-list"/);
  assert.match(page, /class="headline-index"/);
  assert.match(page, /record\.bullets\.length===3/);
  assert.match(page, /safeUrl\(item\.url\)/);
  assert.match(page, /rel="noopener noreferrer"/);
  assert.match(page, /data-filter="ticker"/);
  assert.match(nav, /\["efinance-news\.html","eFinanceThai live"/);
  assert.match(home, /href="efinance-news\.html"/);
  assert.match(worker, /url\.pathname === "\/api\/efinance-news"/);
});

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
      assert.match(source, new RegExp(`${asset.replace(".", "\\.")}\\?v=8`), `${file} must load ${asset} v8`);
    }
  }
});

test("module rail aligns the selected section to the top of its own scroller", async () => {
  const nav = await readFile("nav.js", "utf8");
  assert.match(nav, /modulePanel\.querySelector\("\.is1s-module-scroll"\)/);
  assert.match(nav, /is1s-module-spacer/);
  assert.match(nav, /target > available/);
  assert.match(nav, /scroller\.scrollTo\(\{ top:Math\.max\(0,target\)/);
  assert.doesNotMatch(nav, /section\.scrollIntoView/);
});

test("sidebar gives every module a distinct color and an accessible active state", async () => {
  const nav = await readFile("nav.js", "utf8");
  assert.match(nav, /aria-pressed=/);
  assert.match(nav, /aria-current="page"/);
  assert.match(nav, /is1s-nav-section.*is-selected/);
  assert.match(nav, /candidate\.classList\.toggle\("is-selected"/);

  const css = await readFile("theme.css", "utf8");
  for (const module of ["home", "market", "companies", "news", "surveillance", "bonds"]) {
    assert.match(css, new RegExp(`data-module-section="${module}"`), `${module} must define a module accent`);
  }
  assert.match(css, /\.is1s-rail-btn\.active\s*\{[^}]*var\(--module-accent\)/s);
  assert.match(css, /\.is1s-module-link\.active\s*\{[^}]*box-shadow:inset 3px 0 0 var\(--module-accent\)/s);
  assert.match(css, /:root\[data-theme="light"\] \.is1s-nav-section/);
});

test("homepage places RM-filtered disclosure and external-news feeds before dashboards", async () => {
  const nav = await readFile("nav.js", "utf8");
  assert.match(nav, /className = "is1-home-news"/);
  assert.match(nav, /data-home-disclosures/);
  assert.match(nav, /data-home-external/);
  assert.match(nav, /var disclosureRows = rmFilings\(\)/);
  assert.match(nav, /var externalRows = rmNews\(\)/);
  assert.match(nav, /data-home-news-rm/);
  assert.match(nav, /safeHttpUrl/);

  const css = await readFile("theme.css", "utf8");
  assert.match(css, /\.is1-home-news-grid\s*\{[^}]*grid-template-columns:repeat\(2/s);
  assert.match(css, /@media\(max-width:980px\)[\s\S]*\.is1-home-news-grid\s*\{\s*grid-template-columns:1fr/);
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

test("Oppday drawer owns its scroll area and Form 59 snapshot schema is coherent", async () => {
  const oppday = await readFile("oppday-minutes.html", "utf8");
  assert.match(oppday, /\.drawer-body\s*\{[^}]*overflow-y\s*:\s*auto/s);
  assert.match(oppday, /querySelector\(['"]\.drawer-body['"]\)\.scrollTop\s*=\s*0/);

  const form59 = JSON.parse(await readFile("data/sec-form59.json", "utf8"));
  assert.ok(Number.isInteger(form59.total) && form59.total >= 0);
  assert.equal(form59.total, form59.items.length);
  assert.ok(form59.windowDays >= 7);
  assert.ok(Array.isArray(form59.tickers));
  assert.equal(Object.values(form59.bySide).reduce((sum, value) => sum + value, 0), form59.total);
});
