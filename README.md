# IS1 Team Coverage Dashboard

Static site with 4 daily-refreshed dashboards covering 231 SET-listed tickers across 6 RMs (Champ, Orn, Kae, Tony, Pim, Gift).

Hosted on **Cloudflare Pages** (free tier). Daily build runs entirely on **GitHub Actions** — no laptop required. Cloudflare auto-deploys when the bot pushes new JSON snapshots.

> See [`MIGRATION.md`](./MIGRATION.md) for the full system reference (paths, env vars, secrets, new-laptop bootstrap).

## Live URL

`https://<project-name>.pages.dev` — set after Cloudflare Pages connection.

## Architecture

```
                       GitHub Actions (.github/workflows/daily.yml)
                       ┌────────────────────────────────────────┐
   02:50 UTC ──full──► │ Job 1 surveillance:                    │
   (09:50 BKK)         │   poll SET → classify (rules + Haiku)  │
                       │   → email (critical / digest / feed)   │
   10:30 UTC ──crit──► │   → upload duckdb to R2                │
   (17:30 BKK)         │ Job 2 build:                           │
                       │   download duckdb → run 4 routes       │
                       │   → commit data/*.json                 │
                       └────────────────────────────────────────┘
                                       │
                                       ▼
                       Cloudflare Pages auto-deploys on push
                       (free CDN, never sleeps)
```

## Daily schedule (Mon–Fri)

| Cron (UTC) | Bangkok | Mode | Emails |
|---|---|---|---|
| `50 2 * * 1-5` | 09:50 | full | critical + material digest + 24h coverage feed |
| `30 10 * * 1-5` | 17:30 | critical-only | critical alerts only (idempotent — silent if nothing new) |

The afternoon run skips digest + coverage-feed to avoid duplicate noise. Critical alerts are idempotent: they only fire on **unsent** items, so re-running is safe and a quiet 17:30 inbox usually means "no new critical disclosures since morning" — not a failure.

Manual trigger: GitHub → Actions → "Daily Surveillance + Build" → Run workflow (mode = `full` or `critical-only`).

## Files

| Path | Purpose |
|---|---|
| `index.html` | Landing page with links to the 4 dashboards |
| `coverage-morning-brief.html` | EOD prices + sparklines, RM/sector tabs |
| `disclosure-pulse.html` | Recent SET filings, severity-tagged |
| `sector-heatmap.html` | PE/PBV/DY/EV-EBITDA/NPM heatmap |
| `unusual-trading.html` | Volume / price / 52W alerts |
| `data/tickers.json` | Master ticker → RM + sector map |
| `data/*.json` | Daily snapshot files (committed by the bot) |
| `data/build-status.json` | Last build timestamp + per-route status |
| `scripts/build_daily.py` | 4-route SETSMART scan for all 231 tickers |
| `scripts/setsmart_proxy.py` | Vendored route handlers called in-process |
| `scripts/build_tickers.py` | Regenerate `tickers.json` from the IS1 Port Summary Excel |
| `surveillance/` | Polling + classification + email pipeline (run by Job 1) |
| `.github/workflows/daily.yml` | The CI workflow that runs everything |

## First-time deployment (one-time setup)

1. **Create GitHub repo** named `is1-coverage-dashboard`.
2. Push this folder to `main`.
3. **Add GitHub Actions secrets** (Settings → Secrets and variables → Actions):
   `SETSMART_API_KEY`, `ANTHROPIC_API_KEY`, `SURVEILLANCE_SQL`,
   `EMAIL_USERNAME`, `EMAIL_APP_PASSWORD`, `EMAIL_FROM`, `EMAIL_TO`,
   `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ENDPOINT`, `R2_BUCKET`.
4. **Cloudflare Pages**:
   - Sign in to [dash.cloudflare.com](https://dash.cloudflare.com) (free tier).
   - Workers & Pages → Create → Pages → Connect to Git → pick the repo.
   - Build settings: **leave all blank** (this is a pure static site, no build command).
   - Output directory: `/` (root).
   - Save & Deploy.
5. The first scheduled run (or a manual `workflow_dispatch`) populates `data/*.json`.

## Updating the ticker list

When the team's portfolio changes, regenerate `data/tickers.json` from the latest IS1 Port Summary Excel:

```
python scripts/build_tickers.py "<path to IS1 Port Summary.xlsx>"
```

Commit and push — the next scheduled run picks it up automatically.

## Troubleshooting

- **Dashboards show "updated 36h+ ago"** — check the Actions tab on GitHub: https://github.com/tasinpongk-jpg/is1-coverage-dashboard/actions
- **No 17:30 BKK email** — expected when no new critical-severity disclosure occurred since the morning sweep (alerts are idempotent). Confirm by checking the workflow run logs for `[critical] nothing to send`.
- **Empty `disclosure-pulse`** — surveillance DuckDB only covers Champ's 50 tickers. Other RMs' filings won't appear until the surveillance pipeline is expanded.
- **Cloudflare Pages build fails** — there is no build step (static site). Make sure Build Command is empty.
- **DuckDB version mismatch** — `surveillance/requirements.txt` pins duckdb 1.5.2; if you upgrade locally, bump CI too or `disclosure-pulse` silently falls back to empty.
