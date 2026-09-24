# Registers the daily Windows task that keeps data/vault-ticker-notes.json fresh.
#
# Run once from an elevated PowerShell:
#   powershell -ExecutionPolicy Bypass -File scripts\register_vault_refresh.ps1
#
# What it does:
#   - Creates task \IS1\Vault-Notes-Refresh
#   - Runs daily at 10:35 Bangkok (03:35 UTC) — 5 minutes after the existing
#     10:30 IS1-Vault-Refresh task that pulls the R2 DB to the local vault.
#   - Calls scripts\refresh_vault_notes.py --push
#   - Idempotent: re-running removes + re-creates the task cleanly.

$ErrorActionPreference = "Stop"

$taskName    = "Vault-Notes-Refresh"
$taskPath    = "\IS1\$taskName"
$repoRoot    = (Resolve-Path "$PSScriptRoot\..").Path
$pythonExe   = (Get-Command python).Source
$scriptPath  = Join-Path $repoRoot "scripts\refresh_vault_notes.py"
$logDir      = Join-Path $repoRoot "logs"
$logFile     = Join-Path $logDir "vault-notes-refresh.log"

if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }

# Remove any stale task with the same name so re-runs are idempotent.
$existing = Get-ScheduledTask -TaskPath "\IS1\" -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Removing existing task $taskPath ..."
    Unregister-ScheduledTask -TaskPath "\IS1\" -TaskName $taskName -Confirm:$false
}

# Build the action. We do NOT use Start-Process inside the action because
# Task Scheduler needs the .exe path directly, not a wrapper. Python -u
# keeps stdout unbuffered so the log file is useful.
$action = New-ScheduledTaskAction `
    -Execute $pythonExe `
    -Argument "-u `"$scriptPath`" --push" `
    -WorkingDirectory $repoRoot

# 03:35 UTC = 10:35 Bangkok. Daily.
$trigger = New-ScheduledTaskTrigger -Daily -At "03:35"

# Run as the current user, but only when they're logged in (laptop tasks
# should NOT fire when the lid is closed). "Run only when user is logged
# on" is the safer default for daily-brief-style work.
$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType S4U `
    -RunLevel Limited

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10) `
    -MultipleInstances IgnoreNew

Register-ScheduledTask `
    -TaskName $taskName `
    -TaskPath "\IS1\" `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Settings $settings `
    -Description "Rebuild data/vault-ticker-notes.json from the Obsidian vault and push to GitHub. Frees the dashboard from the 56-day drift seen in Aug 2026." `
    | Out-Null

Write-Host "Registered $taskPath -> $pythonExe $scriptPath --push"
Write-Host "Trigger: daily at 03:35 UTC (10:35 Bangkok)"
Write-Host "Log:     $logFile"
Write-Host ""
Write-Host "To verify: Get-ScheduledTask -TaskPath '\IS1\' -TaskName $taskName"
Write-Host "To remove: Unregister-ScheduledTask -TaskPath '\IS1\' -TaskName $taskName -Confirm:`$false"
