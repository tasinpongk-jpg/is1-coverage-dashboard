---
name: meeting-minutes
description: Use when an audio file (.m4a/.wav/.mp3/.mp4) needs to be turned into Thai meeting minutes (SET-style or generic). Runs a fully local ASR + diarization + Typhoon 2.5 pipeline on the host Mac via launchd file watcher. Suffix `-set`, `-gen`, or `-both` on the filename selects the template.
---

# Meeting minutes skill

## How to invoke

1. Confirm with the user which template they want: SET-style (formal Thai
   รายงานการประชุม) or generic professional minutes, or both.
2. Ask whether the audio is already in `~/Meetings/inbox/` or somewhere
   else.
3. If elsewhere, copy/move it into `~/Meetings/inbox/` with the correct
   suffix:
   - SET → rename to `<original>-set.<ext>`
   - Generic → `<original>-gen.<ext>`
   - Both → `<original>-both.<ext>`
4. Tail `~/Meetings/logs/pipeline.log` until you see `DONE <filename>`
   (typically 5–25 min depending on audio length).
5. Read the resulting `.md` from `~/Meetings/minutes/set/` and/or
   `~/Meetings/minutes/generic/`.
6. Respond to the user in their language with file paths, summary,
   decisions, action items, and governance flags (SET only).

## Live recording flow

The user records via Hammerspoon (Cmd+Shift+R toggle). Files land in
`~/Meetings/live/` and are auto-moved to `~/Meetings/inbox/` with a
`-meet` suffix. With no template suffix the pipeline processes them as
"generic". To force SET-style, rename the inbox file to add `-set`
*before* launchd's debounce window expires (~5 s after move), or move the
in-progress job from `processing/` back to `inbox/` with the right suffix.
Do not start or stop recordings yourself — Cowork's VM cannot drive the
host audio devices.

## Sub-tools available

- `bash` (in-VM): used to `ls`, `mv`, `tail`, `cat` host-mounted folders
  only.
- No `ollama` CLI inside the VM — host runs Ollama; you only watch logs.

## What you must NOT do

- Do not summarize the transcript yourself with Anthropic models.
  Summarization is local-only via `pipeline.py` → Typhoon 2.5. You only
  present the result.
- Do not modify minutes content beyond fixing obvious typos the user
  explicitly asks you to fix.
- Do not upload to cloud, OneDrive, or Teams unless the user explicitly
  says so.
