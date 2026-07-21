import { test } from "node:test";
import assert from "node:assert/strict";
import { readFile, readdir } from "node:fs/promises";

const htmlFiles = (await readdir(".")).filter((name) => name.endsWith(".html"));

test("every page loads the appearance runtime before the shared theme", async () => {
  assert.ok(htmlFiles.length >= 17, "expected the full dashboard page set");
  for (const file of htmlFiles) {
    const source = await readFile(file, "utf8");
    const runtime = source.indexOf('src="theme.js"');
    const styles = source.indexOf('href="theme.css"');
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
