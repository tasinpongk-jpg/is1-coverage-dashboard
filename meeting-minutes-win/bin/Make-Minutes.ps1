# Make-Minutes.ps1 — convenience wrapper around pipeline.py.
# Sets the env vars the Python script expects, prints memory warning,
# then runs the pipeline.
#
# Usage:
#   .\Make-Minutes.ps1 -Audio C:\path\to\meeting.m4a
#   .\Make-Minutes.ps1 -Audio C:\path\to\meeting.m4a -Kind set
#   .\Make-Minutes.ps1 -Audio C:\path\to\meeting.m4a -Kind both
#
# -Kind {set|gen|both} renames the file to add the matching suffix before
# running, so you don't have to remember the filename convention.

[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)]
  [string]$Audio,

  [ValidateSet('set','gen','both','auto')]
  [string]$Kind = 'auto'
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path $Audio)) { throw "Audio file not found: $Audio" }

$src = (Resolve-Path $Audio).Path
$dir = Split-Path $src -Parent
$base = [IO.Path]::GetFileNameWithoutExtension($src)
$ext  = [IO.Path]::GetExtension($src)

# Apply suffix if Kind != auto and the file doesn't already carry one
$validSuffixes = @('-set','-gen','-both')
$hasSuffix = $validSuffixes | Where-Object { $base.EndsWith($_) }
if ($Kind -ne 'auto' -and -not $hasSuffix) {
  $newBase = "$base-$Kind"
  $newPath = Join-Path $dir "$newBase$ext"
  Copy-Item $src $newPath -Force
  $src = $newPath
  Write-Host "Renamed to encode template choice: $newBase$ext" -ForegroundColor Cyan
}

# Memory warning
$os = Get-CimInstance Win32_OperatingSystem
$freeGB = [math]::Round($os.FreePhysicalMemory / 1MB, 1)
if ($freeGB -lt 4) {
  Write-Host ""
  Write-Host "WARNING: only $freeGB GB free RAM. Typhoon 4B needs ~3 GB resident." -ForegroundColor Yellow
  Write-Host "  Close Chrome / Slack / Teams before continuing for best results." -ForegroundColor Yellow
  $confirm = Read-Host "Continue anyway? [y/N]"
  if ($confirm -ne 'y') { exit 0 }
}

# Locate pipeline.py
$pipeline = Join-Path $PSScriptRoot 'pipeline.py'
if (-not (Test-Path $pipeline)) { throw "pipeline.py not found at $pipeline" }

# Run
Write-Host ""
Write-Host "Running pipeline on $src" -ForegroundColor Cyan
$start = Get-Date
python $pipeline $src
$elapsed = (Get-Date) - $start
Write-Host ""
Write-Host ("Done in {0:N1} min" -f $elapsed.TotalMinutes) -ForegroundColor Green
Write-Host "Output:  $env:USERPROFILE\Meetings\minutes\"
