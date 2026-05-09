#!/bin/bash
# Installer for the Thai meeting-minutes pipeline.
# Idempotent — safe to re-run after partial failure or repo update.
#
# Usage:   ./meeting-minutes/bin/install.sh
# Skip homebrew/ollama/python steps with: SKIP_BREW=1 SKIP_OLLAMA=1 SKIP_PY=1 ./install.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
SRC_DIR="$REPO_DIR/meeting-minutes"
HOME_DIR="$HOME"
MEET_DIR="$HOME/Meetings"

step() { printf '\n\033[1;36m▸ %s\033[0m\n' "$*"; }
note() { printf '  %s\n' "$*"; }
warn() { printf '  \033[33m⚠  %s\033[0m\n' "$*"; }
die()  { printf '  \033[31m✗  %s\033[0m\n' "$*" >&2; exit 1; }

if [ "$(uname)" != "Darwin" ]; then
  die "This installer targets macOS. Use it on the M5 Pro Mac, not in CI."
fi

step "Pre-flight"
"$SCRIPT_DIR/preflight.sh" || die "Pre-flight failed. Fix the FAIL items and re-run."

# ---------- 1. Folder structure ----------
step "Creating ~/Meetings/ folder structure"
mkdir -p \
  "$MEET_DIR"/{inbox,live,processing,done,minutes/set,minutes/generic,minutes/_archive,bin,logs} \
  "$MEET_DIR/templates/system_prompts"
note "Folders ready."

# ---------- 2. Symlink scripts and templates ----------
step "Linking pipeline scripts and templates"
link() {
  local src="$1" dst="$2"
  [ -e "$src" ] || die "Missing source: $src"
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
    note "ok  $dst"; return
  fi
  if [ -e "$dst" ] && [ ! -L "$dst" ]; then
    mv "$dst" "$dst.preinstall.$(date +%s)"
    note "backed up existing file: $dst.preinstall.*"
  fi
  ln -sfn "$src" "$dst"
  note "link $dst → $src"
}

link "$SRC_DIR/bin/pipeline.py"             "$MEET_DIR/bin/pipeline.py"
link "$SRC_DIR/bin/process_inbox.sh"        "$MEET_DIR/bin/process_inbox.sh"
link "$SRC_DIR/bin/cleanup_processing.sh"   "$MEET_DIR/bin/cleanup_processing.sh"
link "$SRC_DIR/templates/Modelfile.typhoon-minutes"     "$MEET_DIR/templates/Modelfile.typhoon-minutes"
link "$SRC_DIR/templates/Modelfile.typhoon-minutes-4b"  "$MEET_DIR/templates/Modelfile.typhoon-minutes-4b"
link "$SRC_DIR/templates/system_prompts/set_th.txt"     "$MEET_DIR/templates/system_prompts/set_th.txt"
link "$SRC_DIR/templates/system_prompts/generic_th.txt" "$MEET_DIR/templates/system_prompts/generic_th.txt"
link "$SRC_DIR/cowork/CLAUDE.md"            "$MEET_DIR/CLAUDE.md"

chmod +x "$SRC_DIR/bin/"*.sh "$SRC_DIR/bin/"*.py

# ---------- 3. Hammerspoon config ----------
step "Linking Hammerspoon config (~/.hammerspoon/init.lua)"
mkdir -p "$HOME_DIR/.hammerspoon"
link "$SRC_DIR/hammerspoon/init.lua" "$HOME_DIR/.hammerspoon/init.lua"

# ---------- 4. Cowork skill ----------
step "Linking Cowork skill (~/.claude/skills/meeting-minutes/SKILL.md)"
mkdir -p "$HOME_DIR/.claude/skills/meeting-minutes"
link "$SRC_DIR/cowork/skills/meeting-minutes/SKILL.md" \
     "$HOME_DIR/.claude/skills/meeting-minutes/SKILL.md"

# ---------- 5. Homebrew packages ----------
if [ "${SKIP_BREW:-0}" != "1" ]; then
  step "Installing Homebrew packages"
  command -v brew >/dev/null || die "Install Homebrew first: https://brew.sh"
  brew install ffmpeg sox jq fswatch git pandoc whisper-cpp uv 2>/dev/null || true
  brew install --cask blackhole-2ch hammerspoon ollama 2>/dev/null || true
  # Optional: lm-studio, audio-hijack — uncomment if wanted
  # brew install --cask lm-studio audio-hijack
  note "Re-registering coreaudiod for BlackHole..."
  sudo killall coreaudiod || true
else
  note "SKIP_BREW=1 set — skipping Homebrew step"
fi

# ---------- 6. Ollama setup ----------
if [ "${SKIP_OLLAMA:-0}" != "1" ]; then
  step "Configuring Ollama (Apple-Silicon-optimized env vars)"
  launchctl setenv OLLAMA_FLASH_ATTENTION 1
  launchctl setenv OLLAMA_KV_CACHE_TYPE   q8_0
  launchctl setenv OLLAMA_NUM_PARALLEL    1
  launchctl setenv OLLAMA_MAX_LOADED_MODELS 1
  launchctl setenv OLLAMA_KEEP_ALIVE      30m
  launchctl setenv OLLAMA_CONTEXT_LENGTH  24576

  if ! pgrep -x Ollama >/dev/null && ! pgrep -x ollama >/dev/null; then
    note "Starting Ollama..."
    open -a Ollama || warn "Could not auto-start Ollama; launch it manually"
    sleep 5
  fi

  step "Pulling Ollama models (this can take a while; ~28 GB total)"
  ollama pull scb10x/typhoon2.5-qwen3-30b-a3b
  ollama pull scb10x/typhoon2.5-qwen3-4b
  ollama pull qwen3:8b
  ollama pull bge-m3

  step "Building custom Modelfiles"
  ollama create typhoon-minutes:24k    -f "$MEET_DIR/templates/Modelfile.typhoon-minutes"
  ollama create typhoon-minutes-4b:32k -f "$MEET_DIR/templates/Modelfile.typhoon-minutes-4b"
else
  note "SKIP_OLLAMA=1 set — skipping Ollama step"
fi

# ---------- 7. Python venv ----------
if [ "${SKIP_PY:-0}" != "1" ]; then
  step "Creating Python venv at ~/Meetings/venv"
  command -v uv >/dev/null || die "uv not installed (brew install uv)"
  if [ ! -d "$MEET_DIR/venv" ]; then
    uv venv "$MEET_DIR/venv" --python 3.11
  fi
  # shellcheck disable=SC1091
  source "$MEET_DIR/venv/bin/activate"
  uv pip install --upgrade pip
  uv pip install \
    "mlx-whisper>=0.4" "mlx-audio>=0.5" \
    "pyannote.audio>=4.0.4" \
    torch torchaudio \
    silero-vad soundfile pydub \
    ollama python-docx jinja2 typer rich \
    huggingface_hub \
    qdrant-client
  # whisperx-mlx may not always resolve; fall back gracefully
  uv pip install whisperx-mlx 2>/dev/null || uv pip install whispermlx 2>/dev/null || \
    warn "whisperx-mlx/whispermlx not available; pipeline still works without"
  deactivate
else
  note "SKIP_PY=1 set — skipping Python step"
fi

# ---------- 8. launchd agent ----------
step "Installing launchd agent"
PLIST_DST="$HOME/Library/LaunchAgents/com.user.meetingpipeline.plist"
TMP_PLIST="$(mktemp)"

# Resolve HF token: prefer env var, fall back to HF CLI cached token, else placeholder.
HF_TOKEN_VALUE="${HF_TOKEN:-}"
if [ -z "$HF_TOKEN_VALUE" ] && [ -f ~/.cache/huggingface/token ]; then
  HF_TOKEN_VALUE="$(cat ~/.cache/huggingface/token)"
fi
if [ -z "$HF_TOKEN_VALUE" ]; then
  warn "No HF_TOKEN found. Pyannote diarization will fail until you run:"
  warn "  huggingface-cli login   # then re-run install.sh"
  HF_TOKEN_VALUE="hf_REPLACE_ME"
fi

sed -e "s|USERNAME|$(whoami)|g" \
    -e "s|HF_TOKEN_VALUE|$HF_TOKEN_VALUE|g" \
    "$SRC_DIR/launchd/com.user.meetingpipeline.plist" > "$TMP_PLIST"

mkdir -p "$HOME/Library/LaunchAgents"
mv "$TMP_PLIST" "$PLIST_DST"
chmod 644 "$PLIST_DST"

# Reload (bootout then bootstrap so updates apply).
if launchctl print "gui/$(id -u)/com.user.meetingpipeline" >/dev/null 2>&1; then
  launchctl bootout "gui/$(id -u)/com.user.meetingpipeline" 2>/dev/null || true
fi
launchctl bootstrap "gui/$(id -u)" "$PLIST_DST"
launchctl enable    "gui/$(id -u)/com.user.meetingpipeline"
note "launchd agent active: com.user.meetingpipeline"

# ---------- 9. Reload Hammerspoon ----------
if pgrep -x Hammerspoon >/dev/null; then
  step "Reloading Hammerspoon config"
  osascript -e 'tell application "Hammerspoon" to execute lua code "hs.reload()"' || \
    warn "Could not auto-reload Hammerspoon; click menubar icon → Reload Config"
else
  warn "Hammerspoon not running — open it once to grant Accessibility permission"
fi

# ---------- 10. Reminders ----------
cat <<EOF

$(printf '\033[1;32m✓ install.sh completed.\033[0m')

Manual steps still required (cannot be automated):

  1. \033[1mAudio MIDI Setup\033[0m (one-time): create Multi-Output Device
     (MacBook Pro Speakers + BlackHole 2ch) and Aggregate Device named
     "Mic+BH" (MacBook Pro Microphone + BlackHole 2ch). See docs/audio-setup.md.

  2. \033[1mTCC permissions\033[0m: System Settings → Privacy & Security
     - Microphone: Terminal, Hammerspoon, Claude.app
     - Screen Recording: Terminal (only needed if capturing system audio)
     - Accessibility: Hammerspoon
     - Full Disk Access: Terminal, Claude.app

  3. \033[1mHugging Face gated models\033[0m — visit each and click Agree:
     https://huggingface.co/pyannote/segmentation-3.0
     https://huggingface.co/pyannote/speaker-diarization-3.1
     https://huggingface.co/pyannote/speaker-diarization-community-1

  4. \033[1mCowork trusted folder\033[0m: in Claude Desktop → Cowork →
     Customize → Folders → Add: ~/Meetings

  5. Test with a short Thai audio file:
     cp my-test.m4a ~/Meetings/inbox/test-set.m4a
     tail -f ~/Meetings/logs/pipeline.log
EOF
