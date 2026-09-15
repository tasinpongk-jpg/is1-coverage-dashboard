# IS1 Coverage Dashboard — Redesign Brief for Claude Design

Audit date: 2026-09-15. Everything below was read out of this repo, not assumed.
If you change the codebase, update this file in the same commit.

**How to use this file:** paste §0 into Claude Design as the prompt. Attach or
paste §1–§10 as the reference dossier. §11 is the acceptance checklist.

---

## §0 — THE PROMPT (paste this)

> Redesign the theme and interface of an internal equity-surveillance dashboard
> used by six analysts at the Stock Exchange of Thailand, Issuer Department 1.
> It covers 232 SET-listed companies across six sectors and is read every
> weekday morning before the market opens, mostly on a 1440px+ desktop, in a
> bright office, for 5–15 minutes at a time.
>
> It is a working instrument, not a marketing site. The user is a professional
> analyst reading dense numeric tables. Priorities in order: scan speed,
> numeric legibility, signal-vs-noise, then aesthetics. Decoration that costs a
> row of data is a bad trade.
>
> **Hard constraints — a design that violates these cannot ship:**
> 1. Static HTML/CSS/JS only. No React, no Vue, no Tailwind, no build step, no
>    npm. Cloudflare Pages serves the files as-is. Only external requests
>    allowed: Google Fonts and one `marked.min.js` CDN script.
> 2. Every color, radius, shadow and spacing value must be a CSS custom
>    property defined once in a single `theme.css`. No hard-coded hex anywhere
>    else. A runtime script flips `data-theme="light"|"dark"` on `<html>`, so
>    both palettes must be complete and defined at the same specificity.
> 3. Bilingual EN/TH. Thai (Sarabun) runs ~15% wider and taller than the
>    English string at the same size. No fixed-width labels, no single-line
>    truncation on anything a Thai string lands in, no ALL-CAPS treatment that
>    Thai script cannot take.
> 4. Every number is `font-variant-numeric: tabular-nums` and right-aligned in
>    tables. Percentages, prices, ratios and counts must align down the column.
> 5. Accessible: 4.5:1 body contrast in both themes, visible `:focus-visible`,
>    `prefers-reduced-motion` honored, semantic color never the only carrier of
>    meaning (add a glyph or label alongside red/green).
> 6. Must survive being wrong. Data is a daily JSON snapshot that sometimes
>    goes stale or fails. Loading, empty, stale and error states are first-class
>    design work here, not afterthoughts.
>
> **What I want from you:**
> - A design language: palette (light + dark), type scale, spacing scale,
>   radius/elevation scale, border treatment, data-density rules.
> - The app shell: a left icon rail + module sidebar + topbar + right context
>   drawer. I want this rethought, not repainted — tell me if the four-surface
>   shell is wrong for this workload.
> - Three page archetypes designed to pixel level: (a) the morning-overview
>   home, (b) a dense sortable/filterable 232-row data table, (c) a
>   single-company detail page with nine tabs.
> - The repeating components: KPI tile, filing/news feed row, alert card,
>   ticker chip, severity badge, RM badge, sector tag, inline sparkline, tab
>   bar, filter bar, freshness pill, drawer, empty/stale/error state.
> - A full `theme.css` token block I can drop in, both themes.
>
> **Deliver as:** a design canvas with artboards, plus the token CSS as copyable
> code. Annotate the rationale for each major decision — I will be defending
> these choices to a department head.
>
> The current build is functional but incoherent: eighteen of twenty pages
> redefine the same design tokens locally, and the shared stylesheet fights
> them back with 87 `!important` declarations. Assume nothing about the current
> look is load-bearing except the information architecture. See the attached
> dossier for the current state, the data, and the page inventory.

---

## §1 — What the product is

A daily-refreshed intelligence desk for **232 Thai SET-listed companies** under
IS1 (Issuer Department 1) coverage. Static HTML + JSON snapshots on Cloudflare
Pages; a Cloudflare Worker (`worker.js`) serves `/api/chat`, `/api/feedback`
and `/api/efinance-news` for the embedded agent console.

There is no backend and no build step. GitHub Actions rebuilds the JSON
snapshots on cron, commits them, and Cloudflare auto-deploys on push.

**Coverage shape** (`data/tickers.json`, 232 entries):

| Sector | Tickers |
|---|---|
| PROP | 60 |
| FOOD | 58 |
| PF&REIT | 47 |
| CONS | 32 |
| CONMAT | 21 |
| AGRI | 14 |

**Six RMs** own the book: C (51), O (44), K (38), T (36), P (35), G (28).
RM identity is a first-class filter on almost every page — the shell holds a
selected RM in `localStorage` (`is1_rm`, default `C`) and pages filter to it.

## §2 — Who reads it and when

- Six analysts. Primary session: 08:30–09:30 BKK, before the SET open.
- Desktop-first, 1440–1920px. Mobile is a real but secondary path (the shell
  has a full mobile mode under 840px).
- The reader knows the domain cold. No explanatory chrome, no tooltips
  defining what P/E means, no onboarding.
- They are looking for exceptions: what moved, what filed, what is silent,
  what is flagged. The design job is to make exceptions surface without the
  reader hunting.

## §3 — Tech constraints (non-negotiable)

| Constraint | Detail |
|---|---|
| Framework | None. Vanilla HTML/CSS/JS. Each page is a self-contained file with an inline `<style>` and inline `<script>`. |
| Build | None. Files are served verbatim. `.assetsignore` ships only root HTML + `data/*.json` to the edge. |
| External deps | `fonts.googleapis.com` (Sarabun 400/500/600/700, JetBrains Mono 500/600/700) and `cdn.jsdelivr.net/npm/marked/marked.min.js` (one page). Nothing else. |
| Charts | Zero chart libraries. All charts are hand-rolled inline SVG (`<polyline>`/`<path>` sparklines, bar rows built from divs). A redesign that assumes Chart.js/D3 is unbuildable here. |
| Icons | Inline SVG path strings in a JS lookup table (Lucide-style, 24×24 viewBox, `stroke-width:1.8`, `fill:none`, `currentColor`). Two separate tables: `nav.js` (~30 icons) and `chat-dock.js` (~13). |
| Cache-busting | Assets are versioned by query string (`theme.css?v=8`). Bumping the version is a manual edit in all 20 HTML files. |

## §4 — Current shell anatomy

Every page loads the same five shared assets. Order matters and is identical
on all 20 pages:

```html
<head>
  <style> …page-local CSS, includes its own :root{} … </style>   <!-- the problem -->
  <script src="theme.js?v=8"></script>      <!-- blocking, pre-paint -->
  <link rel="stylesheet" href="theme.css?v=8">
  <script src="i18n.js?v=9"></script>
</head>
<body>
  …page markup…
  <script src="nav.js?v=9" defer></script>
  <script src="chat-dock.js?v=8" defer></script>
</body>
```

**`theme.js`** (6.6 KB) — reads `localStorage.is1_theme` (`system`/`light`/
`dark`), sets `data-theme` + `data-theme-mode` on `<html>` before paint, injects
the three-button theme switch into the topbar, and runs a scroll-reveal motion
system (IntersectionObserver, `.motion-reveal` → `.is-revealed`, staggered
38ms). Uses the View Transition API for theme flips when available. Exposes
`window.IS1Theme`.

**`theme.css`** (45 KB, 1299 lines) — three jobs fused into one file:
1. the token definitions for both themes,
2. the entire app-shell layout (179 `.is1s-*` rules) and the home dashboard
   panels (`.is1-home-*`),
3. a "legacy correction" layer that overrides page-local hard-coded colors with
   **87 `!important` declarations**.

**`i18n.js`** (98 KB) — EN/TH dictionary. Static text uses `data-i18n="key"`
attributes; JS-generated text calls `I18N.t(key)`. Dictionary values are plain
text only — several pages interpolate them into `innerHTML`, so markup in the
dictionary would render unescaped. Body carries `lang-en`/`lang-th`; `.lx-th`
and `.lx-en` classes gate per-language spans.

**`nav.js`** (55 KB) — the app shell, injected at runtime into every page:

| Surface | Width/height | Behavior |
|---|---|---|
| Icon rail `.is1s-rail` | `--is1-rail-w: 64px`, fixed left, full height | 6 module buttons, each with its own accent color; hard-coded near-black `#0b0d10` background in **both** themes |
| Module sidebar `.is1s-modules` | `--is1-module-w: 228px` | Per-module page list, live counts, collapse toggle (persisted), freshness footer with live dot |
| Topbar `.is1s-topbar` | `66px`, sticky | Breadcrumb, ticker search with `/` hotkey + datalist of all 232, RM selector, language toggle, theme switch, context toggle |
| Context drawer `.is1s-context` | `--is1-context-w: 310px`, fixed right, slide-in | Three tabs: My book / Alerts / Agents |
| Embedded workspace | full-bleed overlay | iframes two external dashboards with `?embedded=1`, which makes `nav.js` and `chat-dock.js` self-disable |

Body padding is driven by `.is1-shell-ready { padding-left: calc(rail + module) }`
and `.is1s-context-open { padding-right: 310px }`. Under 840px both panels
become scrim-backed drawers.

**`chat-dock.js`** (30 KB) — "REX" agent console. Injects its own `<style>`
block (does not use `theme.css`). Bottom-right FAB → 460×680 panel with four
agent tabs: **Hermes** (news/disclosures, amber `#f59e0b`), **Atlas**
(prices/alerts, blue `#3b82f6`), **Pythia** (sector screens, violet `#8b5cf6`),
**Lex** (SET/SEC regulations, green `#10b981`). Threads in `sessionStorage`,
credentials in `localStorage`, calls the Worker. Also a text-selection "Ask"
button. Renders bot replies as bold/bullets/tables, with thumbs feedback.

## §5 — Current design tokens (`theme.css`)

Dark (`:root`, `:root[data-theme="dark"]`, `color-scheme: dark`):

```
--bg #0c0e12   --bg2 #11141a   --card #171a20   --card2 #1d2129  --panel2 #12151a
--border #2a2f39  --border2 #373d49  --line #2a2f39  --line-soft #20242c
--text #f0f2f5  --text2 #c9ced7  --muted #9aa3b2  --dim #6f7887
--accent #817cf3  --accent-strong #9b97ff  --accent-soft rgba(129,124,243,.13)
--accent-border rgba(129,124,243,.36)  --glow rgba(129,124,243,.20)
--green #35c979  --red #ff6262  --yellow #f5ad42  --blue #5c92ff  --violet #b17cff
--header-bg rgba(12,14,18,.88)  --overlay rgba(0,0,0,.58)
--shadow-sm 0 1px 2px rgba(0,0,0,.24)
--shadow-md 0 10px 30px rgba(0,0,0,.28)
--shadow-lg 0 20px 56px rgba(0,0,0,.38)
--surface-hover #20242c  --scroll-track #0c0e12  --scroll-thumb #3c4350
```

Light (`:root[data-theme="light"]`, `color-scheme: light`):

```
--bg #f3f5f8   --bg2 #e9edf2   --card #ffffff   --card2 #f7f8fa
--border #d9dee7  --border2 #c8d0dc
--text #171a21  --text2 #343a46  --muted #5f6878  --dim #7b8493
--accent #5855c9  --accent-strong #4542b7
--green #168449  --red #d23f43  --yellow #a96000  --blue #2463d4  --violet #7f46c8
--header-bg rgba(255,255,255,.90)  --overlay rgba(18,22,30,.38)
--surface-hover #f0f2f6  --scroll-track #edf0f4  --scroll-thumb #b9c1cd
```

Aliases kept for legacy markup: `--body`/`--ink` = `--text`, `--mut` = `--muted`,
`--crit` = `--red`, `--mat` = `--yellow`, `--low` = `--green`,
`--routine` = `--muted`, `--gov` = `--violet`.

Module accents (hard-coded in both `nav.js` and `theme.css` — currently
duplicated, should become tokens):

```
Workspace #f2aa1f · Market #5d96ff · Companies #35bdd0
News flow #31c77b · Surveillance #ef6464 · Bond data #b17cff
```

Shell geometry: `--is1-rail-w 64px`, `--is1-module-w 228px`,
`--is1-context-w 310px`. Radii are mostly 8px via a blanket
`.card,.dash-card,.kpi,… { border-radius:8px !important }` rule.

Typography: `'Sarabun','Segoe UI',system-ui,sans-serif` everywhere.
`'JetBrains Mono'` is loaded globally but currently used **only** in
`sector-intelligence.css` (9–18px numerics). There is no type scale — sizes
are ad-hoc per page, roughly 8px→26px.

## §6 — The CSS debt (what the redesign must actually fix)

This is the reason for the project. Be explicit about it with the designer.

1. **18 of 20 pages declare their own `:root{}`** with the same token names and
   different values. `index.html` alone carries 171 lines of inline CSS and sets
   `--accent:#6366f1` against `theme.css`'s `#817cf3`. Load order means
   `theme.css` usually wins, but page-local *rules* (not tokens) like
   `header{background:#0a0c12ee}` do not participate at all.
2. **87 `!important` in `theme.css`** exist solely to beat those page-local
   hard-coded colors back into token compliance. 110 across all CSS + HTML.
3. **Page-local `:root` blocks have no light variant.** They were written
   dark-only; light theme works only because `theme.css` defines
   `:root[data-theme="light"]` at higher specificity. Any new page-local rule
   with a literal hex silently breaks light mode.
4. **Two competing home layouts coexist.** `index.html` ships a `.dash-card`
   navigation grid; `nav.js` then injects a richer `.is1-home-control` panel
   set and hides the old blocks by adding `.is1s-home-legacy`. The redesign
   should collapse this to one.
5. **The legacy `<header>` on every page is hidden** with
   `.is1s-legacy-header{display:none !important}` once the shell loads — dead
   markup on 20 pages.
6. **The icon rail is hard-coded dark in light mode** (`#0b0d10`). Deliberate
   today, but it should be a stated decision with a token, not a literal.
7. **`chat-dock.js` styles itself independently** of `theme.css`, with
   `var(--token, #fallback)` everywhere. It will drift from any new palette
   unless the redesign covers it.

## §7 — Data the interface renders

All pages `fetch()` static JSON from `data/`. Shapes below are current.

| File | Size | Cadence | Key shape |
|---|---|---|---|
| `tickers.json` | 23 KB | manual | `{version, tickers:[{tk,sector,rm,bucket}], rms, sectors, totals}` |
| `morning-brief.json` | 128 KB | daily 09:15 BKK | `{asOf, rows:[{tk,last,pct1d,pct5d,pctMtd,pctYtd,volRatio,filings,hi52,lo52,path,sector}]}` — `path` is the sparkline point array |
| `ticker-summary.json` | 1.7 MB | daily | 232 rows, ~45 fields each: price, PE/PBV/DY/mktcap, free float, foreign room, CG score, ESG rating, auditors, management list, financial highlights |
| `disclosure-pulse.json` | 2.0 MB | daily + 14:00 + 18:00 | `{filings:[{tk,sector,ts,type,title,title_th,url,severity,_summary,_summary_th,…}]}` (1881 items, 90d) + `status:[{tk,lastFiledTs,n24h,n7d,n30d,silentDays,overdue}]` |
| `sector-heatmap.json` | 117 KB | daily | 5 metrics × 232 rows + `sectorAgg` |
| `unusual-trading.json` | 23 KB | daily | `{alerts:[{tk,type,severity,value,label,evidence,filingsLinked}], byTicker:[…]}` |
| `external-news.json` | 203 KB | daily | 130 items from HOONSMART/KAOHOON, ticker-matched |
| `ai-insights.json` | 3 KB | daily | `{headline, market_take, sector_notes[6], watchlist[8], risk_flags[]}` |
| `company-reports.json` | 1.5 MB | **manual** | per-ticker narrative synthesis |
| `vault-ticker-notes.json` | 6.0 MB | **manual, no CI trigger** | MD&A / FS-notes / call excerpts per ticker — the known silent-staleness trap |
| `visits.json` | 369 KB | manual | 232 rows: priority, thesis, lastVisit, nextAction, flags, questions |
| `oppday-minutes.json` | 713 KB | manual | earnings-call minutes, markdown bodies |
| `bond-summary.json` / `sec-bonds.json` | 342 / 50 KB | monthly | outstanding bonds |
| `sec-enforcement.json` / `sec-form59.json` | 149 KB / 300 B | daily | |
| `source-health.json`, `diagnostics.json`, `build-status.json` | small | daily | feed health, RM staleness, unclassified queue |

**Freshness is a designed concept, not a footnote.** The home page carries a
snapshot bar with per-file `asOf` and a three-state color cycle: green ≤7d,
yellow 7–14d, red >14d, plus a fourth grey "manual" state for files with no
fixed cadence. Two snapshots are manual-only and go stale silently. The
redesign must give staleness a stronger, more consistent visual treatment than
a row of small text.

**Severity vocabulary** (drives most color coding): `critical` / `material` /
`routine` / `unclassified` on filings; `high` / `medium` on alerts.

## §8 — Page inventory (20 pages, 6 modules)

### Workspace (accent `#f2aa1f`)
| Page | What it is | UI pattern |
|---|---|---|
| `index.html` | Morning overview. Today bar, AI take, mover chips, snapshot freshness bar, nav card grid, RM/sector stats, diagnostics fold | Mixed: chips, card grid, folds. **Two layouts fighting** (see §6.4) |
| `visits.html` | Visit planner — 232 rows, priority/thesis/next action | Filterable table + KPI row + expandable rows |
| `ai-insights.html` | Daily LLM commentary: headline, market take, 6 sector notes, watchlist, risk flags | Prose cards, two-column |

### Market (`#5d96ff`)
| Page | What it is | UI pattern |
|---|---|---|
| `price-movement.html` | Daily moves across 232 | Sortable table, tab bar, inline SVG sparklines, RM badges |
| `sector-intelligence.html` | Meeting-ready FOOD/PROP briefing — the most designed page, own 55 KB CSS | Custom: lens grid, driver chains, market map, earnings charts, PE bands. All hand-rolled SVG/divs |
| `multiples-comparison.html` | PE/PBV/DY side by side | Table + aggregate cards + legend bar |
| `multiples-band.html` | Valuation ranges per sector | Per-metric sections with SVG band charts |

### Companies (`#35bdd0`)
| Page | What it is | UI pattern |
|---|---|---|
| `company-summary.html` | 90 KB. The deepest page — 9 tabs: overview, company, financials, governance, disclosures, MD&A, notes, oppday, report | Hero + tab bar + drawer; SVG sparklines and hand-built financial charts |
| `oppday-minutes.html` | Earnings-call minutes | List + filter bar + right drawer with markdown body (`marked.js`) |
| `sec-form59.html` | Management/related-person trades | Feed list |

### News flow (`#31c77b`)
| Page | What it is | UI pattern |
|---|---|---|
| `disclosure-pulse.html` | Live SET filings ranked by severity | Feed with severity dots, ticker chips, TH/EN title toggle |
| `external-news.html` | Ticker-matched wire headlines | Feed with excerpt |
| `efinance-news.html` | eFinanceThai live (Worker-proxied) | Grouped feed + headline index sidebar — the most modern-looking page today |

### Surveillance (`#ef6464`)
| Page | What it is | UI pattern |
|---|---|---|
| `unusual-trading.html` | Volume/price anomalies with linked filings | Alert card grid, evidence rows |
| `trading-signs.html` | SET trading signs (SP/NP/C/H…) | Compact grid + legend |
| `sec-enforcement.html` | Thai SEC actions | Feed + filter note |
| `governance-screen.html` | Auditor fees, AGM timing, board independence | Wide table + coverage grid + controls |

### Bond data (`#b17cff`)
| Page | What it is | UI pattern |
|---|---|---|
| `bond-summary.html` | Outstanding bonds across coverage | Table + SVG charts + rating/ESG badges |
| `bond-data-sec.html` | SEC bond filings | Table + bar rows |

Plus `404.html`, and two external dashboards embedded as workspaces
(TradingView daily board, macro brief).

## §9 — Components that repeat across pages

Design these once, properly:

`.rm-badge` · severity dot/pill (4 states) · ticker chip (links to
`company-summary.html?tk=`) · sector tag · `.stale-pill` (3 states) ·
`.kpi` / `.hstat` tile · `.dash-card` · `.filing` / `.item` feed row ·
`.alert-card` · `.tab-bar` + `.tab` (with count) · `.filter-bar` ·
`.table-wrap` + sortable `<th>` · `.drawer` + `#overlay` · inline sparkline
(SVG, ~90×24 and 240×34) · `details.fold` disclosure · `details.howto`
help block · `.is1s-empty` · loading spinner · `.legend` / `.legend-bar`.

## §10 — Brand direction (pick one, tell me why)

**Option A — evolve the current indigo terminal.** Keep `--accent` in the
indigo/violet family, tighten everything else. Lowest migration risk; the
six module accents already read as a system.

**Option B — align to the SET house template.** The department's PPTX template
is dark `#2E2E2E` / `#252525` ground, gold accent `#FFA300` / `#FFC000`, white
text, Browallia New. Advantage: screenshots pasted into department decks stop
looking foreign. Disadvantage: Browallia New is a weak screen face at small
sizes and gold-on-dark is a harsh combination for 12px tabular data. If you go
this way, treat gold as an accent only and keep Sarabun for UI text.

**Option C — neutral instrument palette.** Near-monochrome surfaces, color
reserved exclusively for semantic meaning (up/down, severity, freshness). The
six module accents become the only chromatic wayfinding. This is what a
professional terminal usually converges on and is my default recommendation —
but argue against it if you disagree.

State the tradeoff you are making. I will be defending this to a department
head, so "it looks cleaner" is not an argument.

---

## §11 — Acceptance checklist

A redesign is accepted when:

- [ ] One `theme.css` owns every token; zero literal hex outside it (the icon
      rail's dark ground included — token it).
- [ ] Zero `!important` in the new stylesheet. If one is needed, it is a bug
      report against a page, not a solution.
- [ ] Light and dark are both complete, both defined at the same specificity,
      both pass 4.5:1 on body text and 3:1 on borders/icons.
- [ ] Every page's inline `:root{}` block is deleted, not overridden.
- [ ] A named type scale (no more ad-hoc 8px→26px) and spacing scale.
- [ ] Thai strings at the longest realistic length do not break any layout.
- [ ] All numerics tabular and column-aligned.
- [ ] Loading / empty / stale / error states specified for feeds, tables and
      KPI tiles.
- [ ] `chat-dock.js`'s injected CSS is covered by the same tokens.
- [ ] `prefers-reduced-motion` and `:focus-visible` preserved.
- [ ] The three page archetypes (home, dense table, company detail) are
      specified to pixel level, not just moodboarded.
