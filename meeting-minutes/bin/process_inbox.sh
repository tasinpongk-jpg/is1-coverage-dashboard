#!/bin/bash
# Watcher entry point invoked by launchd whenever ~/Meetings/inbox/ changes.
# Iterates new audio files, runs pipeline.py, and archives originals.
set -euo pipefail

INBOX=~/Meetings/inbox
WORK=~/Meetings/processing
DONE=~/Meetings/done
VENV=~/Meetings/venv/bin/python
LOG=~/Meetings/logs/pipeline.log

mkdir -p "$WORK" "$DONE" "$(dirname "$LOG")"

shopt -s nullglob
for f in "$INBOX"/*.{wav,m4a,mp3,mp4,m4v,mov}; do
  base=$(basename "$f")

  # Debounce: skip files still being written (e.g. in-flight network copy).
  s1=$(stat -f%z "$f"); sleep 5; s2=$(stat -f%z "$f")
  if [ "$s1" != "$s2" ]; then
    echo "[$(date '+%F %T')] SKIP $base (still growing)" >> "$LOG"
    continue
  fi

  echo "[$(date '+%F %T')] Processing $base" >> "$LOG"
  mv "$f" "$WORK/"

  if "$VENV" ~/Meetings/bin/pipeline.py "$WORK/$base" >> "$LOG" 2>&1; then
    mv "$WORK/$base" "$DONE/"
    echo "[$(date '+%F %T')] OK $base" >> "$LOG"
    # Privacy log: this run was local-only.
    printf '%s %s local-only=true cloud-llm=false m365-upload=false\n' \
      "$(date -u '+%FT%TZ')" "$base" >> ~/Meetings/logs/privacy.log
  else
    echo "[$(date '+%F %T')] FAIL $base — left in processing/" >> "$LOG"
  fi
done
