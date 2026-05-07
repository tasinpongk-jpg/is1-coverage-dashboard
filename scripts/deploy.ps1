# Daily deploy: regenerate JSON snapshots and push to Cloudflare Pages via Git.
# Runs from a Windows scheduled task at 06:30 every weekday.
# Idempotent: safe to run manually anytime.
#
# Logs to logs/deploy-YYYYMMDD.log so failed scheduled runs can be diagnosed.

$ErrorActionPreference = "Continue"   # don't bail on first non-terminating error; we want full log
$root    = "C:\SET API Manual\SET_Coverage_Cloud"
$venv    = "C:\!VSCODE_Folder\SET_SETSMART_API\set_mcp\.venv\Scripts\python.exe"
$logDir  = "$root\logs"
$logFile = "$logDir\deploy-$(Get-Date -Format 'yyyyMMdd').log"

if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }

function Log($msg) {
    $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $msg"
    Write-Output $line
    Add-Content -Path $logFile -Value $line
}

Log "===== deploy.ps1 START ====="
Log "User: $env:USERNAME  PID: $PID  HostName: $env:COMPUTERNAME"

# Env vars
$env:SETSMART_API_KEY     = "4a053d9a-9f46-40f0-a6a0-2f04103d20dc"
$env:SURVEILLANCE_DB_PATH = "C:\!VSCODE_Folder\SET_SETSMART_API\surveillance\surveillance.duckdb"
$env:SURVEILLANCE_SQL     = [Environment]::GetEnvironmentVariable("SURVEILLANCE_SQL", "User")
$env:PYTHONIOENCODING     = "utf-8"
Log ("SURVEILLANCE_SQL: " + $(if ($env:SURVEILLANCE_SQL) { "set ($($env:SURVEILLANCE_SQL.Length) chars)" } else { "NOT SET -- disclosure-pulse will fall back to live mode" }))

Set-Location $root
Log "cwd: $root"

# Build phase -- capture all output to log
Log "Phase 1/3: Building daily snapshots (~15 min for 231-ticker SETSMART scan)..."
& $venv "$root\scripts\build_daily.py" 2>&1 | Tee-Object -FilePath $logFile -Append | Out-Null
$buildExit = $LASTEXITCODE
Log "Build exited with code $buildExit"
if ($buildExit -ne 0) {
    Log "FATAL: Build failed. See log above."
    exit 1
}

# Stage + check for changes
Log "Phase 2/3: Staging changes..."
git add data/*.json 2>&1 | Tee-Object -FilePath $logFile -Append | Out-Null
$changes = git status --porcelain data/ 2>&1
Log "git status output: $changes"
if (-not $changes) {
    Log "No data changes; exiting clean (this is normal if nothing actually changed)"
    exit 0
}

# Commit + push
Log "Phase 3/3: Committing and pushing..."
$today = Get-Date -Format "yyyy-MM-dd"
git commit -m "daily snapshot $today" 2>&1 | Tee-Object -FilePath $logFile -Append | Out-Null
$commitExit = $LASTEXITCODE
Log "git commit exited with code $commitExit"
if ($commitExit -ne 0) { Log "FATAL: commit failed"; exit 1 }

git push origin main 2>&1 | Tee-Object -FilePath $logFile -Append | Out-Null
$pushExit = $LASTEXITCODE
Log "git push exited with code $pushExit"
if ($pushExit -ne 0) { Log "FATAL: push failed (auth? network?)"; exit 1 }

Log "===== deploy.ps1 SUCCESS -- Cloudflare will redeploy in ~30s ====="
exit 0
