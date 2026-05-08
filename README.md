# IS1 Team Coverage Dashboard

Static site with 4 daily-refreshed dashboards covering 231 SET-listed tickers across 6 RMs (Champ, Orn, Kae, Tony, Pim, Gift).

Hosted on **Cloudflare Pages** (free tier). No backend — GitHub Actions runs the
daily build in the cloud, commits JSON snapshots to this repo, Cloudflare
auto-deploys on push. See `MIGRATION.md` for the full system reference.

## Live URL

`https://<project-name>.pages.dev` — set after Cloudflare Pages connection.

## Architecture

```
        GitHub Actions (.github/workflows/daily.yml)
        ┌──────────────────────────────────────────────┐
  cron  │  Job 1: surveillance                         │
  ─────►│   poll SET → rules+Haiku → email → R2 upload │
        │  Job 2: build (needs Job 1)                  │
        │   build_daily.py (231-ticker SETSMART scan)  │
        │   git commit + push data/*.json   ───►       │
        └──────────────────────────────────────────────┘
                                                │
                                                ▼
                                        Cloudflare Pages
                                        ─ auto-deploys on push
                                        ─ serves 4 HTML + JSON
                                        ─ free CDN, never sleeps
```

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
| `scripts/build_daily.py` | Calls SETSMART proxy in-process for all 231 tickers |
| `scripts/setsmart_proxy.py` | Vendored FastAPI proxy used by `build_daily.py` |
| `surveillance/` | Polling, classification, R2 sync, email routing |
| `.github/workflows/daily.yml` | Consolidated CI: surveillance job + build job |

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

## Daily refresh — GitHub Actions cron

Scheduled in `.github/workflows/daily.yml` (Mon–Fri):

| Cron (UTC) | Bangkok local | Mode | Emails sent |
|---|---|---|---|
| `50 2 * * 1-5` | 09:50 | full | critical + digest + coverage-feed |
| `30 10 * * 1-5` | 17:30 | critical-only | critical (digest/coverage-feed skipped) |

Manual runs: `gh workflow run daily.yml -f mode=full` (or `critical-only`).

The build job takes ~15–20 min (sequential SETSMART scan of 231 tickers).
Critical alerts are idempotent (only fire on UNSENT items); the afternoon run
re-checks for newly-arrived critical filings without duplicating digest noise.

### Local-only piece (laptop)

`IS1-Vault-Refresh` Windows task runs daily at 10:30 BKK (after the morning
CI completes). It downloads `surveillance.duckdb` from R2 and patches the
local Obsidian vault. The old `IS1-Coverage-Daily-Build` and
`SET-Surveillance-Daily` tasks are disabled — see `MIGRATION.md`.

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

- **Dashboards show "updated 36h+ ago"** — daily build failed. Check `data/build-status.json` and the GitHub Actions run log at https://github.com/tasinpongk-jpg/is1-coverage-dashboard/actions.
- **Empty `disclosure-pulse`** — usually a DuckDB version mismatch between CI and the local writer (both pinned at 1.5.2). See `MIGRATION.md` "known gotchas". Surveillance now covers all 231 tickers across 6 RMs.
- **Cloudflare Pages build fails** — there's no build step (static site). Make sure Build Command is empty.
- **Surveillance/build job failed in CI** — see Actions tab. Common causes: SETSMART API quota, Anthropic API key rotation, R2 credential drift. Secrets live in repo settings.
