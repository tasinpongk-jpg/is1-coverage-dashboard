#!/bin/bash
# Maintenance: remove processing/ subfolders older than 30 days that are
# either marked done or have no STATE file (abandoned).
# Run via cron or manually; never deletes done/ or minutes/ folders.
set -euo pipefail

PROC=~/Meetings/processing
KEEP_DAYS=${KEEP_DAYS:-30}
LOG=~/Meetings/logs/cleanup.log

mkdir -p "$(dirname "$LOG")"

if [ ! -d "$PROC" ]; then
  exit 0
fi

find "$PROC" -mindepth 2 -maxdepth 2 -type d -mtime +"$KEEP_DAYS" \
  -print0 | while IFS= read -r -d '' dir; do
    state_file="$dir/STATE"
    if [ -f "$state_file" ]; then
      state=$(cat "$state_file")
      if [ "$state" = "done" ]; then
        echo "[$(date '+%F %T')] purge done: $dir" >> "$LOG"
        rm -rf "$dir"
      else
        echo "[$(date '+%F %T')] keep failed (state=$state): $dir" >> "$LOG"
      fi
    else
      echo "[$(date '+%F %T')] purge stateless: $dir" >> "$LOG"
      rm -rf "$dir"
    fi
done
