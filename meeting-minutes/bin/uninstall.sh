#!/bin/bash
# Uninstaller for the Thai meeting-minutes pipeline.
# Removes launchd agent, symlinks, and Hammerspoon/Cowork links.
# Does NOT delete: ~/Meetings/{inbox,live,processing,done,minutes,logs} (your data).
# Does NOT uninstall: Homebrew packages, Ollama models, Python venv.
# Pass --purge-data to also delete ~/Meetings entirely (DANGEROUS).
set -euo pipefail

PURGE=0
for arg in "$@"; do
  [ "$arg" = "--purge-data" ] && PURGE=1
done

step() { printf '\n\033[1;36m▸ %s\033[0m\n' "$*"; }
note() { printf '  %s\n' "$*"; }

step "Removing launchd agent"
if launchctl print "gui/$(id -u)/com.user.meetingpipeline" >/dev/null 2>&1; then
  launchctl bootout "gui/$(id -u)/com.user.meetingpipeline" || true
  note "agent unloaded"
fi
rm -f "$HOME/Library/LaunchAgents/com.user.meetingpipeline.plist"
note "plist deleted"

step "Removing symlinks"
unlink_if_link() { [ -L "$1" ] && rm "$1" && note "removed $1"; }
unlink_if_link "$HOME/Meetings/bin/pipeline.py"
unlink_if_link "$HOME/Meetings/bin/process_inbox.sh"
unlink_if_link "$HOME/Meetings/bin/cleanup_processing.sh"
unlink_if_link "$HOME/Meetings/templates/Modelfile.typhoon-minutes"
unlink_if_link "$HOME/Meetings/templates/Modelfile.typhoon-minutes-4b"
unlink_if_link "$HOME/Meetings/templates/system_prompts/set_th.txt"
unlink_if_link "$HOME/Meetings/templates/system_prompts/generic_th.txt"
unlink_if_link "$HOME/Meetings/CLAUDE.md"
unlink_if_link "$HOME/.hammerspoon/init.lua"
unlink_if_link "$HOME/.claude/skills/meeting-minutes/SKILL.md"

if [ "$PURGE" = "1" ]; then
  step "PURGE: deleting ~/Meetings entirely"
  read -p "Are you sure? Type DELETE to confirm: " confirm
  if [ "$confirm" = "DELETE" ]; then
    rm -rf "$HOME/Meetings"
    note "~/Meetings removed"
  else
    note "aborted purge"
  fi
fi

cat <<EOF

$(printf '\033[1;32m✓ uninstall complete.\033[0m')

Data preserved (unless --purge-data was given):
  ~/Meetings/{inbox,live,processing,done,minutes,logs}

To also remove the heavy bits:
  ollama rm typhoon-minutes:24k typhoon-minutes-4b:32k
  ollama rm scb10x/typhoon2.5-qwen3-30b-a3b scb10x/typhoon2.5-qwen3-4b
  ollama rm qwen3:8b bge-m3
  rm -rf ~/Meetings/venv
  brew uninstall --cask blackhole-2ch hammerspoon ollama
EOF
