#!/bin/bash
# Minimal installer for the standalone transcribe.py tool.
#
# Subset of install.sh: just ffmpeg + uv + a Python venv with mlx-whisper.
# No Ollama, no Hugging Face gated models, no diarization, no launchd, no
# Hammerspoon. Run install.sh instead if you also want full SET-style
# meeting-minutes generation.
#
# Idempotent — safe to re-run.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEET_DIR="$HOME/Meetings"
VENV_DIR="$MEET_DIR/transcribe-venv"

step() { printf '\n\033[1;36m▸ %s\033[0m\n' "$*"; }
note() { printf '  %s\n' "$*"; }
die()  { printf '  \033[31m✗  %s\033[0m\n' "$*" >&2; exit 1; }

if [ "$(uname)" != "Darwin" ]; then
  die "This installer targets macOS / Apple Silicon."
fi

case "$(uname -m)" in
  arm64) ;;
  *)     die "mlx-whisper requires Apple Silicon (arm64). Detected: $(uname -m)" ;;
esac

step "Installing ffmpeg + uv via Homebrew"
command -v brew >/dev/null || die "Install Homebrew first: https://brew.sh"
brew install ffmpeg uv 2>/dev/null || true
note "ffmpeg: $(ffmpeg -version 2>/dev/null | head -1 | awk '{print $3}')"
note "uv:     $(uv --version 2>/dev/null)"

step "Creating Python 3.11 venv at $VENV_DIR"
mkdir -p "$MEET_DIR"
if [ ! -d "$VENV_DIR" ]; then
  uv venv "$VENV_DIR" --python 3.11
fi

step "Installing mlx-whisper into $VENV_DIR"
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
uv pip install --upgrade pip
uv pip install "mlx-whisper>=0.4"
deactivate

chmod +x "$SCRIPT_DIR/transcribe.sh" "$SCRIPT_DIR/transcribe.py"

cat <<EOF

$(printf '\033[1;32m✓ install-transcribe.sh completed.\033[0m')

Try it:
  ./meeting-minutes/bin/transcribe.sh path/to/audio.m4a
  ./meeting-minutes/bin/transcribe.sh --language th --formats txt,srt,json talk.m4a
  ./meeting-minutes/bin/transcribe.sh --model large-v3 --output-dir ~/Transcripts *.m4a

First run downloads the Whisper model (~1.5 GB for turbo) from Hugging Face
and caches it under ~/.cache/huggingface/. No HF login required — the
mlx-community Whisper models are public.

For the full SET-style meeting-minutes pipeline (diarization + Typhoon LLM
+ .docx output), run ./meeting-minutes/bin/install.sh — it creates its own
venv at ~/Meetings/venv with all six stages' dependencies.
EOF
