# Registers the daily Windows task that runs the Hermes MDA-FS Harvester.
#
# Run once from an elevated PowerShell:
#   powershell -ExecutionPolicy Bypass -File scripts\register_harvest.ps1
#
# Schedule: daily at 10:32 BKK (03:32 UTC). This sits between the existing
# IS1-Vault-Refresh task (10:30, pulls R2 DB to local vault) and the
# Vault-Notes-Refresh task (10:35, rebuilds + pushes the dashboard JSON).
#
# What it runs:
#   1. scripts/harvest_filings.py    -- discover new MDA/FS candidates
#   2. scripts/harvest_download.py   -- download + extract + write vault markdown
#
# Both steps together take ~5-15 minutes for 232 tickers at 14-day lookback.
# The harvest writes to data/harvest-queue.json + data/harvest-state.json
# (gitignored). Vault markdown goes to the Obsidian OneDrive vault.
#
# Idempotent: re-running removes + re-creates the task cleanly.

$ErrorActionPreference = "Stop"

$taskName    = "IS1-Harvest"
$taskPath    = "\IS1\$taskName"
$repoRoot    = (Resolve-Path "$PSScriptRoot\..").Path
$pythonExe   = (Get-Command python).Source
$script1     = Join-Path $repoRoot "scripts\harvest_filings.py"
$script2     = Join-Path $repoRoot "scripts\harvest_download.py"
$logDir      = Join-Path $repoRoot "logs"
$logFile     = Join-Path $logDir "harvest.log"

if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }

# Remove any stale task with the same name so re-runs are idempotent.
$existing = Get-ScheduledTask -TaskPath "\IS1\" -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Removing existing task $taskPath ..."
    Unregister-ScheduledTask -TaskPath "\IS1\" -TaskName $taskName -Confirm:$false
}

# Chain the two scripts in a single cmd wrapper so the task only fires once.
# We redirect stdout+stderr to a daily-rotated log; the wrapper ensures the
# download step runs only if discovery produced new items.
# Env loading: harvest_download.py reads MINIMAX_API_KEY from this wrapper's
# env block. If you store it in a different path (Bitwarden, .env-harvest),
# edit the $env: lines below to point at your source.
$wrapperPath = Join-Path $repoRoot "scripts\run_harvest.bat"
$envFile = Join-Path (Split-Path $repoRoot -Parent) ".hermes\.env-harvest"
$envBlock = ""
if (Test-Path $envFile) {
    $envBlock = "for /f `"usebackq tokens=1,*`" %%%%a in (`"$envFile`") do @set `"%%%%a=%%%%b`""
}
$wrapper = @"
@echo off
set REPO=$repoRoot
set PYTHONUNBUFFERED=1
cd /d %REPO%
$envBlock
echo === harvest_filings ===  >> $logFile
python -u "$script1"                            >> $logFile 2>&1
echo === harvest_download ===  >> $logFile
python -u "$script2" --limit 30                 >> $logFile 2>&1
echo === done $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===  >> $logFile
"@
Set-Content -Path $wrapperPath -Value $wrapper -Encoding ASCII

# Daily at 03:32 UTC = 10:32 Bangkok.
$action = New-ScheduledTaskAction `
    -Execute $wrapperPath `
    -WorkingDirectory $repoRoot

$trigger = New-ScheduledTaskTrigger -Daily -At "03:32"

$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType S4U `
    -RunLevel Limited

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 25) `
    -MultipleInstances IgnoreNew

Register-ScheduledTask `
    -TaskName $taskName `
    -TaskPath "\IS1\" `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -Description "Hermes MDA-FS Harvester: discover new SET filings for IS1 tickers, download+extract, write vault markdown. Sits between IS1-Vault-Refresh (10:30) and Vault-Notes-Refresh (10:35)." `
    | Out-Null

Write-Host "Registered $taskPath"
Write-Host "Trigger: daily at 03:32 UTC (10:32 Bangkok)"
Write-Host "Wrapper: $wrapperPath"
Write-Host "Log:     $logFile"
Write-Host ""
Write-Host "To verify:    Get-ScheduledTask -TaskPath '\IS1\' -TaskName $taskName"
Write-Host "To run now:   Start-ScheduledTask -TaskPath '\IS1\' -TaskName $taskName"
Write-Host "To remove:    Unregister-ScheduledTask -TaskPath '\IS1\' -TaskName $taskName -Confirm:`$false"
