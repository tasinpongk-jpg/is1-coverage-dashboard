#!/bin/bash
# Pre-flight check for the Thai meeting-minutes pipeline.
# Reports PASS/FAIL/WARN for each item; exits non-zero on any FAIL.
set -uo pipefail

PASS=0; FAIL=0; WARN=0
ok()   { printf '  \033[32mPASS\033[0m  %s\n' "$1"; PASS=$((PASS+1)); }
bad()  { printf '  \033[31mFAIL\033[0m  %s\n' "$1"; FAIL=$((FAIL+1)); }
warn() { printf '  \033[33mWARN\033[0m  %s\n' "$1"; WARN=$((WARN+1)); }

echo "=== meeting-minutes pre-flight ==="

# macOS version
if [ "$(uname)" != "Darwin" ]; then
  bad "Not macOS (uname=$(uname)). This pipeline targets macOS 26+."
else
  ver=$(sw_vers -productVersion)
  major=${ver%%.*}
  if [ "$major" -ge 26 ]; then
    ok "macOS $ver"
  else
    bad "macOS $ver — need 26 (Tahoe) or later"
  fi
fi

# Apple Silicon
chip=$(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo unknown)
case "$chip" in
  *Apple*M[5-9]*) ok "Chip: $chip" ;;
  *Apple*M[3-4]*) warn "Chip: $chip — pipeline targets M5; should still work, expect slower ASR" ;;
  *Apple*) warn "Chip: $chip — older Apple Silicon; expect significantly slower ASR + LLM" ;;
  *) bad "Chip: $chip — pipeline requires Apple Silicon" ;;
esac

# RAM
mem_bytes=$(sysctl -n hw.memsize 2>/dev/null || echo 0)
mem_gb=$(( mem_bytes / 1024 / 1024 / 1024 ))
if [ "$mem_gb" -ge 24 ]; then
  ok "RAM: ${mem_gb} GB"
else
  bad "RAM: ${mem_gb} GB — need ≥ 24 GB for Typhoon 30B"
fi

# Free disk
free_gb=$(df -g / | awk 'NR==2 {print $4}')
if [ "${free_gb:-0}" -ge 60 ]; then
  ok "Free disk: ${free_gb} GB on /"
else
  bad "Free disk: ${free_gb} GB on / — need ≥ 60 GB"
fi

# Homebrew
if command -v brew >/dev/null 2>&1; then
  ok "Homebrew: $(brew --version | head -1)"
else
  bad "Homebrew not installed (https://brew.sh)"
fi

# Python 3.11
if command -v python3.11 >/dev/null 2>&1; then
  ok "python3.11: $(python3.11 --version)"
else
  bad "python3.11 not found (brew install python@3.11)"
fi

# Xcode CLT
if xcode-select -p >/dev/null 2>&1; then
  ok "Xcode Command Line Tools: $(xcode-select -p)"
else
  bad "Xcode CLT missing (xcode-select --install)"
fi

# ffmpeg
if command -v ffmpeg >/dev/null 2>&1; then
  ok "ffmpeg: $(ffmpeg -version | head -1 | awk '{print $3}')"
else
  warn "ffmpeg not yet installed (installer will brew it)"
fi

# Ollama daemon
if curl -s --max-time 2 http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
  ok "Ollama daemon responding on :11434"
  for m in typhoon-minutes:24k scb10x/typhoon2.5-qwen3-4b; do
    if curl -s http://127.0.0.1:11434/api/tags | grep -q "\"$m"; then
      ok "Ollama model present: $m"
    else
      warn "Ollama model missing: $m (installer will pull/build)"
    fi
  done
else
  warn "Ollama daemon not running yet (installer will start it)"
fi

# launchd agent
if launchctl print "gui/$(id -u)/com.user.meetingpipeline" >/dev/null 2>&1; then
  ok "launchd agent loaded: com.user.meetingpipeline"
else
  warn "launchd agent not yet loaded (installer will bootstrap)"
fi

# HF token
if [ -n "${HF_TOKEN:-}" ]; then
  ok "HF_TOKEN env var set (length=${#HF_TOKEN})"
elif [ -f ~/.cache/huggingface/token ]; then
  ok "Hugging Face CLI token found"
else
  warn "No HF token found (huggingface-cli login required for pyannote)"
fi

# Folders
if [ -d ~/Meetings ]; then
  ok "~/Meetings exists"
else
  warn "~/Meetings missing (installer will create)"
fi

echo
printf "Result: \033[32m%d PASS\033[0m, \033[33m%d WARN\033[0m, \033[31m%d FAIL\033[0m\n" \
  "$PASS" "$WARN" "$FAIL"
[ "$FAIL" -eq 0 ]
