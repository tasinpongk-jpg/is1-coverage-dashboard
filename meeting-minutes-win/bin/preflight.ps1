# preflight.ps1 — environment check for the Windows ARM64 meeting-minutes pipeline.
# Reports PASS / FAIL / WARN per item; exits non-zero on any FAIL.

$ErrorActionPreference = 'Continue'
$Pass = 0; $Fail = 0; $Warn = 0
function Ok   ($m) { Write-Host "  PASS  $m" -ForegroundColor Green; $script:Pass++ }
function Bad  ($m) { Write-Host "  FAIL  $m" -ForegroundColor Red;   $script:Fail++ }
function Warn ($m) { Write-Host "  WARN  $m" -ForegroundColor Yellow; $script:Warn++ }

Write-Host "=== meeting-minutes-win pre-flight ===" -ForegroundColor Cyan

# OS
$os = Get-CimInstance Win32_OperatingSystem
if ($os.Caption -match 'Windows 11' -or [int]($os.BuildNumber) -ge 22000) {
  Ok "OS: $($os.Caption) build $($os.BuildNumber)"
} else {
  Bad "OS: $($os.Caption) — pipeline targets Windows 11"
}

# Architecture
$arch = $env:PROCESSOR_ARCHITECTURE
if ($arch -eq 'ARM64') {
  Ok "Architecture: ARM64 (native; will use Snapdragon NEON)"
} elseif ($arch -eq 'AMD64') {
  Warn "Architecture: AMD64 — pipeline tuned for ARM64 but should work; pick AMD64 binaries instead"
} else {
  Bad "Architecture: $arch — unsupported"
}

# CPU model (informational)
$cpu = (Get-CimInstance Win32_Processor).Name
Ok "CPU: $cpu"

# RAM
$totalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
$freeGB  = [math]::Round($os.FreePhysicalMemory   / 1MB, 1)
if ($totalGB -ge 16) { Ok "RAM total: $totalGB GB" } else { Bad "RAM total: $totalGB GB — need >= 16 GB" }
if ($freeGB -ge 4) {
  Ok "RAM free: $freeGB GB"
} elseif ($freeGB -ge 2) {
  Warn "RAM free: $freeGB GB — close Chrome/Slack/Teams before running (4B model needs ~3 GB)"
} else {
  Bad "RAM free: $freeGB GB — too low to load Typhoon 4B; close apps and retry"
}

# Disk
$drive = Get-PSDrive -Name C
$freeDiskGB = [math]::Round($drive.Free / 1GB, 1)
if ($freeDiskGB -ge 15) {
  Ok "Free disk on C: $freeDiskGB GB"
} else {
  Bad "Free disk on C: $freeDiskGB GB — need >= 15 GB (model files + working audio)"
}

# Tooling
function CheckCmd ($name, $msg) {
  if (Get-Command $name -ErrorAction SilentlyContinue) {
    Ok "$name on PATH"
  } else {
    Warn "$name not on PATH — $msg"
  }
}
CheckCmd 'ffmpeg'      'installer will winget Gyan.FFmpeg'
CheckCmd 'pandoc'      'installer will winget JohnMacFarlane.Pandoc'
CheckCmd 'python'      'installer will winget Python.Python.3.12'
CheckCmd 'ollama'      'installer will download Ollama for Windows ARM64'
CheckCmd 'whisper-cli' 'installer will download whisper.cpp ARM64 release'

# Ollama daemon
try {
  $r = Invoke-WebRequest -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 2 -UseBasicParsing
  if ($r.StatusCode -eq 200) {
    Ok "Ollama daemon responding on :11434"
    $body = $r.Content | ConvertFrom-Json
    $names = $body.models.name -join ' '
    foreach ($m in @('typhoon-minutes-4b:32k', 'scb10x/typhoon2.5-qwen3-4b')) {
      if ($names -match [regex]::Escape($m)) { Ok "Ollama model present: $m" }
      else { Warn "Ollama model missing: $m (installer will pull/build)" }
    }
  }
} catch {
  Warn "Ollama daemon not running yet (installer will start it)"
}

# Whisper model file
$model = "$env:USERPROFILE\Meetings\models\ggml-large-v3-turbo-q5_0.bin"
if (Test-Path $model) {
  $sz = [math]::Round((Get-Item $model).Length / 1MB, 0)
  Ok "Whisper model present: $model ($sz MB)"
} else {
  Warn "Whisper model not yet downloaded (installer will fetch ~870 MB)"
}

# Folders
if (Test-Path "$env:USERPROFILE\Meetings") {
  Ok "$env:USERPROFILE\Meetings exists"
} else {
  Warn "$env:USERPROFILE\Meetings missing (installer will create)"
}

Write-Host ""
Write-Host ("Result: {0} PASS, {1} WARN, {2} FAIL" -f $Pass, $Warn, $Fail)
if ($Fail -gt 0) { exit 1 }
