import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";

const root = process.cwd();
const src = fs.readFileSync(path.join(root, "i18n.js"), "utf8");
const match = src.match(/var\s+MSG\s*=\s*({[\s\S]*?});\s*\(function\s*\(\)/);

if (!match) {
  console.error("Could not find MSG object in i18n.js");
  process.exit(1);
}

let MSG;
try {
  MSG = vm.runInNewContext(`(${match[1]})`);
} catch (err) {
  console.error("Could not parse MSG object:", err.message);
  process.exit(1);
}

const en = new Set(Object.keys(MSG.en || {}));
const th = new Set(Object.keys(MSG.th || {}));
const failures = [];

for (const key of en) {
  if (!th.has(key)) failures.push(`Missing TH key: ${key}`);
}
for (const key of th) {
  if (!en.has(key)) failures.push(`Missing EN key: ${key}`);
}

const htmlFiles = fs.readdirSync(root)
  .filter((name) => name.endsWith(".html"))
  .map((name) => path.join(root, name));

const files = [
  ...htmlFiles,
  path.join(root, "nav.js"),
  path.join(root, "chat-dock.js"),
  path.join(root, "i18n.js"),
].filter((f) => fs.existsSync(f));

const used = new Map();
const addUse = (key, file) => {
  if (!used.has(key)) used.set(key, new Set());
  used.get(key).add(path.basename(file));
};

const patterns = [
  /\bdata-i18n(?:-title|-placeholder)?=["']([^"']+)["']/g,
  /\bI18N\.t\(\s*["']([^"']+)["']/g,
  /\btt\(\s*["']([^"']+)["']/g,
  /\btx\(\s*["']([^"']+)["']/g,
  /\btr\(\s*["']([^"']+)["']/g,
];

for (const file of files) {
  const text = fs.readFileSync(file, "utf8");
  for (const re of patterns) {
    re.lastIndex = 0;
    let m;
    while ((m = re.exec(text))) addUse(m[1], file);
  }
}

for (const [key, where] of [...used.entries()].sort()) {
  if (!en.has(key) || !th.has(key)) {
    failures.push(`Missing dictionary key: ${key} (${[...where].join(", ")})`);
  }
}

// Every page (except 404.html) must carry data-i18n coverage, and if it uses
// tt()/tx() for dynamic strings it must re-apply translations on language
// switch via an 'i18n:change' listener.
for (const file of htmlFiles) {
  const name = path.basename(file);
  if (name === "404.html") continue;
  const text = fs.readFileSync(file, "utf8");
  if (!/\bdata-i18n(?:-title|-placeholder)?=/.test(text)) {
    failures.push(`${name}: no data-i18n attributes found`);
    continue;
  }
  const usesDynamicTt = /\btt\(|\btx\(/.test(text);
  const hasListener = /i18n:change/.test(text);
  if (usesDynamicTt && !hasListener) {
    failures.push(`${name}: uses tt()/tx() but has no 'i18n:change' listener to refresh on language switch`);
  }
}

// Thai strings must be plain text — no markup allowed in the dictionary.
for (const [key, val] of Object.entries(MSG.th || {})) {
  if (typeof val === "string" && /[<>]/.test(val)) {
    failures.push(`TH value for "${key}" contains '<' or '>' — dictionary values must be plain text`);
  }
}

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}

console.log(`i18n check passed: ${en.size} keys, ${used.size} referenced keys`);
