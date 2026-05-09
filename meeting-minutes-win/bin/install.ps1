# install.ps1 — installer for the Windows ARM64 meeting-minutes pipeline.
# Idempotent. Skip individual stages with: -SkipWinget, -SkipOllama, -SkipWhisper.
#
# Usage (from repo root):
#   .\meeting-minutes-win\bin\install.ps1
#
# Run from a regular (non-elevated) PowerShell. winget will UAC-prompt as needed.

[CmdletBinding()]
param(
  [switch]$SkipWinget,
  [switch]$SkipOllama,
  [switch]$SkipWhisper
)

$ErrorActionPreference = 'Stop'
$ProgressPreference    = 'SilentlyContinue'   # speeds up Invoke-WebRequest

function Step ($m) { Write-Host "`n>>> $m" -ForegroundColor Cyan }
function Note ($m) { Write-Host "    $m" }
function Warn ($m) { Write-Host "  ! $m" -ForegroundColor Yellow }
function Die  ($m) { Write-Host "  X $m" -ForegroundColor Red; exit 1 }

$RepoRoot = (Resolve-Path "$PSScriptRoot\..\..").Path
$WinDir   = (Resolve-Path "$PSScriptRoot\..").Path
$MeetDir  = Join-Path $env:USERPROFILE 'Meetings'
$WingetArgs = @('--accept-package-agreements','--accept-source-agreements','--silent')

if ($env:OS -ne 'Windows_NT') { Die "This installer targets Windows. You're on $($env:OS)." }

Step "Pre-flight"
& "$PSScriptRoot\preflight.ps1"
if ($LASTEXITCODE -ne 0) { Die "Pre-flight failed. Fix the FAIL items and re-run." }

# ---------- 1. Folder structure ----------
Step "Creating $MeetDir folder structure"
foreach ($d in @('inbox','processing','done',
                 'minutes\set','minutes\generic','minutes\_archive',
                 'logs','models')) {
  $p = Join-Path $MeetDir $d
  if (-not (Test-Path $p)) { New-Item -ItemType Directory -Path $p -Force | Out-Null }
}
Note "ok"

# ---------- 2. winget packages ----------
if (-not $SkipWinget) {
  Step "Installing prerequisites via winget"
  if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Die "winget not available. Install App Installer from the Microsoft Store first."
  }
  $pkgs = @(
    'Gyan.FFmpeg',
    'JohnMacFarlane.Pandoc',
    'Python.Python.3.12'
  )
  foreach ($p in $pkgs) {
    Note "winget install $p"
    winget install --id $p @WingetArgs 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne -1978335189) {  # exit code for already-installed varies
      Warn "winget exit code $LASTEXITCODE for $p — may already be installed"
    }
  }
  # Refresh PATH so freshly-installed binaries are visible in this session
  $env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' +
              [Environment]::GetEnvironmentVariable('Path','User')
} else { Note "SkipWinget set" }

# ---------- 3. Ollama ----------
if (-not $SkipOllama) {
  Step "Installing / starting Ollama"
  if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    $url = 'https://ollama.com/download/OllamaSetup.exe'
    $tmp = Join-Path $env:TEMP 'OllamaSetup.exe'
    Note "Downloading $url"
    Invoke-WebRequest -Uri $url -OutFile $tmp -UseBasicParsing
    Note "Running OllamaSetup.exe (may UAC-prompt)"
    Start-Process -FilePath $tmp -ArgumentList '/SILENT' -Wait
    Remove-Item $tmp
    $env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' +
                [Environment]::GetEnvironmentVariable('Path','User')
  }
  if (-not (Get-Process ollama -ErrorAction SilentlyContinue)) {
    Note "Starting Ollama background process"
    Start-Process ollama -ArgumentList 'serve' -WindowStyle Hidden
    Start-Sleep -Seconds 5
  }

  Step "Pulling Typhoon 4B (~2.5 GB) — this can take several minutes"
  ollama pull scb10x/typhoon2.5-qwen3-4b

  Step "Building typhoon-minutes-4b:32k from Modelfile"
  $modelfile = Join-Path $RepoRoot 'meeting-minutes\templates\Modelfile.typhoon-minutes-4b'
  if (-not (Test-Path $modelfile)) {
    Die "Modelfile missing: $modelfile (did the macOS pipeline get committed?)"
  }
  ollama create typhoon-minutes-4b:32k -f $modelfile
} else { Note "SkipOllama set" }

# ---------- 4. whisper.cpp ARM64 ----------
if (-not $SkipWhisper) {
  Step "Installing whisper.cpp (ARM64 Windows build)"
  $whisperDir = Join-Path $env:USERPROFILE '.local\whisper.cpp'
  $whisperBin = Join-Path $whisperDir 'whisper-cli.exe'
  if (-not (Test-Path $whisperBin)) {
    New-Item -ItemType Directory -Path $whisperDir -Force | Out-Null
    Note "Querying whisper.cpp latest release"
    try {
      $rel = Invoke-RestMethod 'https://api.github.com/repos/ggerganov/whisper.cpp/releases/latest' `
              -Headers @{ 'User-Agent' = 'meeting-minutes-installer' }
      $asset = $rel.assets |
        Where-Object { $_.name -match 'Win-?arm64|win-arm64' -and $_.name -match '\.zip$' } |
        Select-Object -First 1
      if (-not $asset) { throw "no ARM64 Windows asset in latest release ($($rel.tag_name))" }
      $zip = Join-Path $env:TEMP $asset.name
      Note "Downloading $($asset.name)"
      Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $zip -UseBasicParsing
      Expand-Archive -Path $zip -DestinationPath $whisperDir -Force
      Remove-Item $zip
      # GH releases sometimes nest binaries one level deep; flatten if needed.
      $exe = Get-ChildItem -Path $whisperDir -Recurse -Filter 'whisper-cli.exe' | Select-Object -First 1
      if ($exe -and $exe.FullName -ne $whisperBin) {
        Copy-Item $exe.FullName $whisperBin -Force
      }
    } catch {
      Warn "Auto-download failed: $_"
      Warn "Manual: https://github.com/ggerganov/whisper.cpp/releases — grab the Win-arm64 zip,"
      Warn "extract whisper-cli.exe to $whisperBin, then re-run install.ps1"
      Die  "Cannot continue without whisper-cli.exe"
    }
  } else {
    Note "whisper-cli.exe already at $whisperBin"
  }

  # Add to PATH for this user (idempotent)
  $userPath = [Environment]::GetEnvironmentVariable('Path','User')
  if ($userPath -notlike "*$whisperDir*") {
    Note "Adding $whisperDir to user PATH"
    [Environment]::SetEnvironmentVariable('Path', "$userPath;$whisperDir", 'User')
    $env:Path += ";$whisperDir"
  }

  Step "Downloading Whisper model (large-v3-turbo q5_0, ~870 MB)"
  $modelPath = Join-Path $MeetDir 'models\ggml-large-v3-turbo-q5_0.bin'
  if (-not (Test-Path $modelPath)) {
    $modelUrl = 'https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo-q5_0.bin'
    Note "Downloading $modelUrl"
    Invoke-WebRequest -Uri $modelUrl -OutFile $modelPath -UseBasicParsing
  } else {
    Note "Model already at $modelPath"
  }
} else { Note "SkipWhisper set" }

# ---------- 5. Reminders ----------
Write-Host ""
Write-Host "*** install.ps1 completed. ***" -ForegroundColor Green
Write-Host ""
Write-Host "Test it with a short Thai .m4a or .wav:" -ForegroundColor Cyan
Write-Host "  .\meeting-minutes-win\bin\Make-Minutes.ps1 -Audio .\sample-set.m4a"
Write-Host ""
Write-Host "Or invoke the Python orchestrator directly:" -ForegroundColor Cyan
Write-Host "  python .\meeting-minutes-win\bin\pipeline.py .\sample-set.m4a"
Write-Host ""
Write-Host "Memory tip: close Chrome / Slack / Teams before running." -ForegroundColor Yellow
Write-Host "Filename suffix selects template: -set, -gen, -both. No suffix = generic."
