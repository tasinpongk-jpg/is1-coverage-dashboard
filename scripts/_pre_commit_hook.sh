#!/bin/bash
# IS1 coverage dashboard — pre-commit hook
# Auto-syncs scripts/*.py to ~/AppData/Local/hermes/scripts/ when the
# basename matches an already-deployed script there. This is how the
# cron scheduler (which only looks in AppData, not the repo) stays in
# sync with repo edits — see CLAUDE.md §4 "If you edit the script,
# also copy it to that path".
#
# Install once per clone:
#   cp scripts/_pre_commit_hook.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# Or run manually:
#   bash scripts/_pre_commit_hook.sh

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
HERMES_SCRIPTS="/c/Users/Tasinpong/AppData/Local/hermes/scripts"

# Skip if the deploy target doesn't exist (CI runner, fresh laptop, etc.)
if [ ! -d "$HERMES_SCRIPTS" ]; then
    echo "pre-commit: $HERMES_SCRIPTS not found — skipping deploy sync"
    exit 0
fi

# Detect staged changes to scripts/*.py
STAGED=$(git diff --cached --name-only --diff-filter=ACMR | grep -E '^scripts/.*\.py$' || true)

if [ -z "$STAGED" ]; then
    exit 0
fi

# For each staged script, if its basename is already deployed, copy it
synced=0
for src in $STAGED; do
    fname=$(basename "$src")
    if [ -f "$HERMES_SCRIPTS/$fname" ]; then
        cp "$REPO_ROOT/$src" "$HERMES_SCRIPTS/$fname"
        echo "pre-commit: synced $src -> $HERMES_SCRIPTS/$fname"
        synced=$((synced + 1))
    fi
done

if [ "$synced" -gt 0 ]; then
    echo "pre-commit: $synced script(s) synced to AppData. Cron will pick up on next run."
fi

exit 0
