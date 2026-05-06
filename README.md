# IS1 Team Coverage Dashboard

Static site with 4 daily-refreshed dashboards covering 231 SET-listed tickers across 6 RMs (Champ, Orn, Kae, Tony, Pim, Gift).

Hosted on **Cloudflare Pages** (free tier). No backend — daily build script on an SET laptop pushes JSON snapshots to this Git repo, Cloudflare auto-deploys on push.

## Live URL

`https://<project-name>.pages.dev` — set after Cloudflare Pages connection.

## Architecture

```
[Tasinpong's laptop, 06:30 daily]              [Cloud, free, always-up]
  Windows scheduled task                          Cloudflare Pages
  ─ runs scripts\deploy.ps1                       ─ auto-deploys on push
  ─ build_daily.py: 231-ticker SETSMART scan      ─ serves 4 HTML + JSON
  ─ writes data/*.json                            ─ free CDN, never sleeps
  ─ git commit + push                  ───►       ─ public URL
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
| `scripts/deploy.ps1` | Build + git commit + push (run by scheduled task) |

## First-time deployment (one-time setup)

1. **Create GitHub repo** named `is1-coverage-dashboard` (private).
2. From this folder:
   ```powershell
   cd "C:\SET API Manual\SET_Coverage_Cloud"
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

## Daily refresh — Windows scheduled task

Register once (run as Tasinpong):

```powershell
$action  = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"C:\SET API Manual\SET_Coverage_Cloud\scripts\deploy.ps1`""
$trigger = New-ScheduledTaskTrigger -Daily -At 06:30
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RestartCount 2 -RestartInterval (New-TimeSpan -Minutes 5)
Register-ScheduledTask -TaskName "IS1-Coverage-Daily-Build" -Action $action -Trigger $trigger -Settings $settings -Description "Daily 06:30 build + push for IS1 coverage dashboard"
```

The task takes ~20 min (sequential SETSMART scan of 231 tickers). Don't run before market open — it pulls EOD prices from the previous day, so any time after 23:00 the night before works equally well. 06:30 leaves the laptop time to wake from sleep + run.

## Updating the ticker list

When the team's portfolio changes, regenerate `data/tickers.json`:

```powershell
& "C:\!VSCODE_Folder\SET_SETSMART_API\set_mcp\.venv\Scripts\python.exe" `
  scripts\build_tickers.py "<path to new IS1 Port Summary.xlsx>"
```

(The `build_tickers.py` script is the same logic that generated the initial `tickers.json` — extract company/sector/RM columns from the Excel, write JSON.)

Then rerun `scripts\deploy.ps1` to push.

## Troubleshooting

- **Dashboards show "updated 36h+ ago"** — daily build failed. Check `data/build-status.json` and the laptop's scheduled task history.
- **Empty `disclosure-pulse`** — surveillance DuckDB only covers Champ's 50 tickers. Other RMs' filings won't appear until surveillance pipeline is expanded.
- **Cloudflare Pages build fails** — there's no build step (static site). Make sure Build Command is empty.
