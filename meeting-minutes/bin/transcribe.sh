#!/bin/bash
# Wrapper for transcribe.py — finds the right Python venv and forwards args.
#
# Looks for, in order:
#   1. ~/Meetings/venv               (created by ./install.sh — full pipeline)
#   2. ~/Meetings/transcribe-venv    (created by ./install-transcribe.sh)
#
# If neither exists, prints the install command and exits 1.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRANSCRIBE_PY="$SCRIPT_DIR/transcribe.py"

if [ ! -f "$TRANSCRIBE_PY" ]; then
  echo "✗ transcribe.py not found next to transcribe.sh ($TRANSCRIBE_PY)" >&2
  exit 1
fi

VENV_PYTHON=""
for candidate in \
  "$HOME/Meetings/venv/bin/python" \
  "$HOME/Meetings/transcribe-venv/bin/python"
do
  if [ -x "$candidate" ]; then
    VENV_PYTHON="$candidate"
    break
  fi
done

if [ -z "$VENV_PYTHON" ]; then
  cat >&2 <<'EOF'
✗ No mlx-whisper venv found. Run one of these first:

  Transcription only (light, ~5 min):
    ./meeting-minutes/bin/install-transcribe.sh

  Full meeting-minutes pipeline (heavy, ~30 min + manual steps):
    ./meeting-minutes/bin/install.sh
EOF
  exit 1
fi

if ! "$VENV_PYTHON" -c 'import mlx_whisper' >/dev/null 2>&1; then
  echo "✗ $VENV_PYTHON is missing mlx_whisper. Re-run install-transcribe.sh." >&2
  exit 1
fi

exec "$VENV_PYTHON" "$TRANSCRIBE_PY" "$@"
