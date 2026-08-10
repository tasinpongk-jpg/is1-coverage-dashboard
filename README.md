# IS1 Team Coverage Dashboard

Static site with daily-refreshed dashboards covering 232 SET-listed tickers across 6 RMs (Champ, Orn, Kae, Tony, Pim, Gift).

Hosted on **Cloudflare Pages** (free tier). No backend — GitHub Actions runs the
daily build in the cloud, commits JSON snapshots to this repo, Cloudflare
auto-deploys on push. See `SYSTEM.md` for the full system reference.

## Live URL

`https://<project-name>.pages.dev` — set after Cloudflare Pages connection.

## Architecture

```
  Cloudflare Worker Cron Triggers (cloudflare-cron/)            GitHub Actions cron
   09:50 BKK ──► daily.yml                  ──┐                  (redundant backup)
   14:00 BKK ──► disclosure-refresh.yml     ──┤                   same times in each YAML
   18:00 BKK ──► disclosure-refresh.yml     ──┤
                                              │ workflow_dispatch (Cloudflare path)
                                              │ schedule:         (GHA backup)
                                              ▼
        ┌──────────────────────────────────────────────┐
        │  daily.yml: surveillance + 4-route build     │
        │  disclosure-refresh.yml: disclosure-only,    │
        │    no emails, no SETSMART scan               │
        │  git commit + push data/*.json   ───►        │
        └──────────────────────────────────────────────┘
                                                │
                                                ▼
                                        Cloudflare Pages
                                        ─ auto-deploys on push
                                        ─ serves static HTML + JSON
                                        ─ free CDN, never sleeps
```

The Cloudflare Worker is the reliable primary scheduler for **all three**
fire times. GHA's built-in `schedule:` events in both workflows are kept as
redundant backups — `concurrency:group=daily` (shared between the two
workflows) prevents simultaneous runs. See `cloudflare-cron/README.md`
for deploy steps and the per-cron routing table.

## Agent chat (✦ Ask the agents)

Every page carries a floating chat dock (`chat-dock.js`) talking to four
named agents served by `worker.js`. All four answer through MiniMax M3; Lex
first retrieves page-level text from the local regulation corpus. Each agent is
grounded in a different data slice:

| Agent | Specialty | Grounded in |
|---|---|---|
| ⚡ Hermes | News & catalysts, Form 59 trades, silent filers, Oppday | `external-news`, `disclosure-pulse`, `sec-form59`, `oppday-minutes` |
| 🗺 Atlas | Prices, movers, alerts, threshold math | `morning-brief`, `tickers`, `unusual-trading` |
| Pythia | IS1 sector performance, breadth and relative ranking | verified calculator over `morning-brief` |
| ⚖️ Lex | SET/SEC rules & disclosure obligations | `lex-regulations.json` built from regulation PDFs (page-cited) |

This dashboard pairs with a private local CLI (`~/VSCoder/AI Agent`) that reads
these same snapshots and hands back `data/visits.json`. They are separate repos
by design; their shared contract (data schema, SET PDF recipe, agent cousins)
is documented once in [INTEGRATION.md](INTEGRATION.md).

Dock features: per-agent threads (survive navigation), RM picker for
personalized suggestion chips, ticker chips in replies deep-linking to
`company-summary.html?tk=X`, and select-any-text → "✦ ask". Token-gated by the
`CHAT_TOKEN` worker secret (`localStorage is1_chat_token` client-side). The
MiniMax credential stays server-side in the `MINIMAX_API_KEY` worker secret.
Rebuild the Lex corpus after changing source PDFs with
`python3 scripts/build_lex_corpus.py /path/to/regulations`.
"Ask the agents" cards on `index.html` open the dock via `IS1Dock.open(name)`.

## Live eFinanceThai headlines

`efinance-news.html` calls `GET /api/efinance-news` for the fast headline list,
then `GET /api/efinance-news/summaries` for three Thai bullet points per story.
The Worker extracts public structured data, allows only canonical eFinanceThai
article URLs, summarizes article text with MiniMax M3, and stores results by
article ID in KV. If the model is unavailable, an honest extractive fallback is
used. Article bodies and images remain on the source site.

## Files

| Path | Purpose |
|---|---|
| `index.html` | Landing page with links to the coverage dashboards |
| `price-movement.html` | EOD prices + sparklines, RM/sector tabs |
| `sector-intelligence.html` | Interactive FOOD/PROP meeting brief: segment earnings, market, valuation, drivers, risks, evidence and company drill-down |
| `disclosure-pulse.html` | Recent SET filings, severity-tagged |
| `efinance-news.html` | Live eFinanceThai headlines with Thai summaries, search, filters, and quick navigation |
| `sec-form59.html` | SEC Form 59 management/related-person buy/sell reports |
| `multiples-comparison.html` | PE/PBV/DY/EV-EBITDA/NPM heatmap |
| `unusual-trading.html` | Volume / price / 52W alerts |
| `data/tickers.json` | Master ticker → RM + sector map (rebuild via Excel) |
| `data/*.json` | Daily snapshot files, including SEC Form 59 rows in `sec-form59.json` |
| `data/regulations-manifest.json` | Expected SET rulebook PDF source list |
| `data/lex-regulations.json` | Page-level Lex corpus deployed with the Worker |
| `data/build-status.json` | Last build timestamp + per-route status |
| `data/company-reports.json` | Generated per-company analyst reports for the ticker drawer Report tab |
| `scripts/build_daily.py` | Calls SETSMART proxy in-process for all 232 tickers |
| `scripts/build_sector_intelligence_audited.py` | Builds schema-v4 `data/sector-intelligence.json` from audited FY2024–25 panels, official SET EOD data, and claim-level FY2025 MD&A excerpts (no browser-side API key) |
| `scripts/build_company_reports.py` | Local report agent; saves Markdown to Obsidian and dashboard JSON |
| `scripts/build_lex_corpus.py` | Extracts the local regulation PDFs into the Lex corpus |
| `scripts/setsmart_proxy.py` | Vendored FastAPI proxy used by `build_daily.py` |
| `surveillance/` | Polling, classification, R2 sync, email routing |
| `.github/workflows/daily.yml` | Consolidated CI: surveillance job + build job (09:50 BKK Mon–Fri) |
| `.github/workflows/disclosure-refresh.yml` | Intra-day disclosure-pulse refresh only (14:00 + 18:00 BKK Mon–Fri, no emails) |
| `cloudflare-cron/` | Worker that triggers `daily.yml` via workflow_dispatch (replaces flaky GHA cron) |

### Sector Intelligence data refresh

The FOOD/PROP route is built from audited local project snapshots. It never calls
SETSMART from the browser and never ships an API key. Pass both the pinned snapshot
directory and its effective completed EOD explicitly:

```powershell
py -3 scripts\build_sector_intelligence_audited.py `
  --theme-root "C:\Users\tasin\OneDrive - The Stock Exchange of Thailand\Claude-Vault\Work-SET\Listed Company\2-Analysis\AI-Generated\05-Themes\Sector-Review-6M26" `
  --legacy-script scripts\build_sector_intelligence.py `
  --snapshot-dir "C:\Users\tasin\OneDrive - The Stock Exchange of Thailand\Claude-Vault\Work-SET\Listed Company\2-Analysis\AI-Generated\05-Themes\Sector-Review-6M26\data\official-2026-08-08-eod-2026-08-07" `
  --effective-eod 2026-08-07 `
  --out data\sector-intelligence.json
```

The generated file carries its market-data cutoff, independent RFO/NPAT/margin
coverage, definitions, source-file paths and SHA-256 hashes, claim-level source IDs,
and a warning that price/valuation explanations remain inference unless a dated
management or market source supports causation.

Schema v4 records a per-company MD&A source state and evidence coverage. The current
118-company perimeter has 117 usable FY2025 MD&A files and one missing annual MD&A
(AKS). AP and ICHI were recovered from official issuer/SET image-only PDFs and
OCR-extracted with source hashes. Each verified RFO/NPAT
driver carries an exact source excerpt plus a SHA-256 hash for reproducible review.

`scripts/build_sector_intelligence.py` is imported only for governed bilingual
narrative scaffolding. Do not execute it directly for audited refreshes.

Pre-deployment checks:

```powershell
node --test tests\theme.test.mjs tests\worker.test.mjs tests\sector-intelligence.test.mjs
node tests\i18n-check.mjs
py -3 "<theme-root>\verify_dashboard_against_audited_panels.py" `
  --json data\sector-intelligence.json `
  --company-csv "<snapshot-dir>\food_prop_company_fy2024_2025_audited_2026-08-07.csv" `
  --segment-csv "<snapshot-dir>\food_prop_segment_fy2024_2025_audited_2026-08-07.csv" `
  --sector-csv "<snapshot-dir>\food_prop_sector_fy2024_2025_audited_2026-08-07.csv" `
  --qa-json "<snapshot-dir>\QA_SUMMARY_FY2024_2025_AUDITED_2026-08-08.json" `
  --work-set-root "C:\Users\tasin\OneDrive - The Stock Exchange of Thailand\Claude-Vault\Work-SET" `
  --market-reconciliation "<snapshot-dir>\food_prop_set_public_surface_reconciliation_2026-08-07.csv"
py -3.11 "<theme-root>\qa_sector_dashboard_browser.py" `
  --base-url http://127.0.0.1:8765 `
  --report "<snapshot-dir>\QA_DASHBOARD_BROWSER_2026-08-08.json" `
  --screenshot-dir "<snapshot-dir>\qa-screenshots"
```

Serve locally (for example `py -3 -m http.server 8765`) before browser QA; the
browser suite checks desktop/mobile layout, both languages, navigation, evidence
deep links, claim/source lineage and important null/coverage cases.

> **SEC Form 59 scrape needs a real browser.** The SEC iDisc site
> (`market.sec.or.th`) is behind an F5 bot-defense WAF — plain `httpx` gets a
> JS challenge page, never the data table. `surveillance/external_sources.py`
> therefore renders the Form 59 page with headless Chromium via Playwright.
> It queries one transaction date at a time over a rolling window so the SEC
> result cap cannot hide later tickers in the coverage universe. A stale or
> empty snapshot triggers a 90-day backfill; subsequent runs refresh 7 days.
> The daily workflow installs it with `python -m playwright install chromium`;
> if the browser is missing the scrape logs a warning and skips (best-effort),
> never breaking the rest of the pipeline.

## First-time deployment (one-time setup)

1. **Create GitHub repo** named `is1-coverage-dashboard` (private).
2. From this folder:
   ```powershell
   cd "C:\!VSCODE_Folder\SET_Coverage_Cloud"
   git init
   git add .
   git commit -m "initial"
   git branch -M main
   git remote add origin https://github.com/<your-username>/is1-coverage-dashboard.git
   git push -u origin main
   ```
3. **Cloudflare Pages**:
   - Sign in to [dash.cloudflare.com](https://dash.cloudflare.com) (free tier).
   - Workers & Pages → Create → Pages → Connect to Git → pick the repo.
   - Build settings: **leave all blank** (this is a pure static site, no build command).
   - Output directory: `/` (root).
   - Click Save & Deploy. Done in ~30 seconds.
4. Cloudflare will give you a URL like `is1-coverage-dashboard.pages.dev`. Share with the team.

## Daily refresh — dual trigger

| Trigger | Cron (UTC) | Bangkok local | Source | Reliability |
|---|---|---|---|---|
| **Primary** | `50 2 * * 1-5` | 09:50 | `cloudflare-cron/` Worker | Cloudflare cron — fires within seconds of the scheduled minute |
| Backup | `50 2 * * 1-5` | 09:50 | `.github/workflows/daily.yml` schedule | GHA cron — best-effort, may drop or delay |

Both fire at the same minute. `concurrency:group=daily` in `daily.yml` queues
the second arrival so only one pipeline runs end-to-end. On the rare day
both trigger and the primary completes first, the backup's commit step is a
no-op (data unchanged), so no duplicate snapshot commits.

Manual re-runs (no inputs): `gh workflow run daily.yml`.

The build job takes ~15–20 min (sequential SETSMART scan of 232 tickers).
Critical alerts are idempotent — re-running is safe and only fires on
disclosures not yet emailed.

### Intra-day disclosure refresh (afternoon + evening)

A separate lightweight workflow `disclosure-refresh.yml` runs twice on
weekdays and refreshes `data/disclosure-pulse.json` only:

| Cron (UTC) | Bangkok local | Purpose |
|---|---|---|
| `0 7 * * 1-5` | 14:00 | afternoon catch-up for late-morning filings |
| `0 11 * * 1-5` | 18:00 | end-of-day sweep for after-market filings |

- ✅ Poll SET, classify with rules + Haiku fallback, update DuckDB on R2.
- ✅ Regenerate `data/disclosure-pulse.json` (DuckDB query, ~0.1s).
- ❌ No emails (critical/material alerts wait for next morning's daily run).
- ❌ No SETSMART scan (the other 3 dashboards stay on the morning snapshot).
- ⏱  ~3 min wall time per run; ~132 GHA min/month (2 runs/day × 22 weekdays).
- 🔒 Concurrency group `daily` — never runs simultaneously with `daily.yml`.

### Local-only piece (laptop)

`IS1-Vault-Refresh` Windows task runs daily at 10:30 BKK (after the morning
CI completes). It downloads `surveillance.duckdb` from R2 and patches the
local Obsidian vault. The old `IS1-Coverage-Daily-Build` and
`SET-Surveillance-Daily` tasks are gone — see `SYSTEM.md`.

## Updating the ticker list

When the team's portfolio changes, regenerate `data/tickers.json`:

```powershell
& "C:\!VSCODE_Folder\SET_SETSMART_API\set_mcp\.venv\Scripts\python.exe" `
  scripts\build_tickers.py "<path to new IS1 Port Summary.xlsx>"
```

(The `build_tickers.py` script is the same logic that generated the initial `tickers.json` — extract company/sector/RM columns from the Excel, write JSON.)

Commit and push the regenerated `data/tickers.json`. The next scheduled CI run
(or a manual `gh workflow run daily.yml`) will pick it up.

## Refreshing company reports

The ticker drawer's **Report** tab is built locally from dashboard data plus
Obsidian MD&A / FS-note / call excerpts. It writes full Markdown reports to the
vault and compact report cards to `data/company-reports.json`.

First check whether the current filing layer is good enough to analyze. This
writes `data/source-coverage.json`, `data/source-coverage-fetch-queue.csv`, and
a queue note back to the Obsidian vault:

```powershell
python scripts\build_source_coverage.py --period 2026Q1
```

```powershell
# deterministic draft mode, no API key needed
python scripts\build_company_reports.py --all --llm never

# richer agent mode, when MINIMAX_API_KEY (or ANTHROPIC_API_KEY fallback) is available
python scripts\build_company_reports.py --all --llm auto
```

After reviewing the output, commit `data/company-reports.json` and run the
fast static deploy:

```powershell
gh workflow run static-deploy.yml
```

## Troubleshooting

- **Dashboards show "updated 36h+ ago"** — daily build failed _and_ both triggers missed (very rare). Check (1) `data/build-status.json`, (2) the GitHub Actions run log at https://github.com/tasinpongk-jpg/is1-coverage-dashboard/actions, and (3) the Cloudflare Worker logs (`wrangler tail` from `cloudflare-cron/` or the dashboard). The healthchecks.io check will also email when a daily dispatch is missed.
- **Empty `disclosure-pulse`** — usually a DuckDB version mismatch between CI and the local writer (both pinned at 1.5.2). See `SYSTEM.md` "known gotchas". Surveillance now covers all 232 tickers across 6 RMs.
- **Cloudflare Pages build fails** — there's no build step (static site). Make sure Build Command is empty.
- **Surveillance/build job failed in CI** — see Actions tab. Common causes: SETSMART API quota, MiniMax API key rotation, R2 credential drift. Secrets live in repo settings.
