# Daily deploy: regenerate JSON snapshots and push to Cloudflare Pages via Git.
# Runs from a Windows scheduled task at 06:30 every weekday.
# Idempotent: safe to run manually anytime.

$ErrorActionPreference = "Stop"
$root  = "C:\SET API Manual\SET_Coverage_Cloud"
$venv  = "C:\!VSCODE_Folder\SET_SETSMART_API\set_mcp\.venv\Scripts\python.exe"

$env:SETSMART_API_KEY     = "4a053d9a-9f46-40f0-a6a0-2f04103d20dc"
$env:SURVEILLANCE_DB_PATH = "C:\!VSCODE_Folder\SET_SETSMART_API\surveillance\surveillance.duckdb"
# SURVEILLANCE_SQL bridges news_items <-> classifications tables for severity/summary/category.
# Stored as a User-level env var via setx; read it back here in case this shell didn't inherit.
$env:SURVEILLANCE_SQL     = [Environment]::GetEnvironmentVariable("SURVEILLANCE_SQL", "User")
$env:PYTHONIOENCODING     = "utf-8"

Set-Location $root

Write-Output "[$(Get-Date -Format 'HH:mm:ss')] Building daily snapshots..."
& $venv "$root\scripts\build_daily.py"
if ($LASTEXITCODE -ne 0) { Write-Error "Build failed"; exit 1 }

Write-Output "[$(Get-Date -Format 'HH:mm:ss')] Committing and pushing..."
git add data/*.json
$changes = git status --porcelain data/
if (-not $changes) { Write-Output "No changes to commit."; exit 0 }

$today = Get-Date -Format "yyyy-MM-dd"
git commit -m "daily snapshot $today"
git push origin main

Write-Output "[$(Get-Date -Format 'HH:mm:ss')] Deployed. Cloudflare Pages will auto-build in ~30s."
