# IS1 Team Coverage Dashboard

Static site with 4 daily-refreshed dashboards covering 232 SET-listed tickers across 6 RMs (Champ, Orn, Kae, Tony, Pim, Gift).

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
                                        ─ serves 4 HTML + JSON
                                        ─ free CDN, never sleeps
```

The Cloudflare Worker is the reliable primary scheduler for **all three**
fire times. GHA's built-in `schedule:` events in both workflows are kept as
redundant backups — `concurrency:group=daily` (shared between the two
workflows) prevents simultaneous runs. See `cloudflare-cron/README.md`
for deploy steps and the per-cron routing table.

## Files

| Path | Purpose |
|---|---|
| `index.html` | Landing page with links to the 4 dashboards |
| `coverage-morning-brief.html` | EOD prices + sparklines, RM/sector tabs |
| `disclosure-pulse.html` | Recent SET filings, severity-tagged |
| `sector-heatmap.html` | PE/PBV/DY/EV-EBITDA/NPM heatmap |
| `unusual-trading.html` | Volume / price / 52W alerts |
| `data/tickers.json` | Master ticker → RM + sector map (rebuild via Excel) |
| `data/*.json` | Daily snapshot files |
| `data/build-status.json` | Last build timestamp + per-route status |
| `scripts/build_daily.py` | Calls SETSMART proxy in-process for all 232 tickers |
| `scripts/setsmart_proxy.py` | Vendored FastAPI proxy used by `build_daily.py` |
| `surveillance/` | Polling, classification, R2 sync, email routing |
| `.github/workflows/daily.yml` | Consolidated CI: surveillance job + build job (09:50 BKK Mon–Fri) |
| `.github/workflows/disclosure-refresh.yml` | Intra-day disclosure-pulse refresh only (14:00 + 18:00 BKK Mon–Fri, no emails) |
| `cloudflare-cron/` | Worker that triggers `daily.yml` via workflow_dispatch (replaces flaky GHA cron) |

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

## Troubleshooting

- **Dashboards show "updated 36h+ ago"** — daily build failed _and_ both triggers missed (very rare). Check (1) `data/build-status.json`, (2) the GitHub Actions run log at https://github.com/tasinpongk-jpg/is1-coverage-dashboard/actions, and (3) the Cloudflare Worker logs (`wrangler tail` from `cloudflare-cron/` or the dashboard). The healthchecks.io check will also email when a daily dispatch is missed.
- **Empty `disclosure-pulse`** — usually a DuckDB version mismatch between CI and the local writer (both pinned at 1.5.2). See `SYSTEM.md` "known gotchas". Surveillance now covers all 232 tickers across 6 RMs.
- **Cloudflare Pages build fails** — there's no build step (static site). Make sure Build Command is empty.
- **Surveillance/build job failed in CI** — see Actions tab. Common causes: SETSMART API quota, Anthropic API key rotation, R2 credential drift. Secrets live in repo settings.
