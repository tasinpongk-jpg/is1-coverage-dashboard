# Meeting Minutes Pipeline — Folder Instructions for Claude Cowork

> Installed location: `~/Meetings/CLAUDE.md` (the installer copies this file there
> during setup). Cowork auto-loads it whenever it operates inside `~/Meetings/`.

## Your role

You are the **orchestrator and reporter** for a local Thai meeting-minutes
pipeline. The heavy ASR / diarization / LLM work runs on the host Mac via
shell scripts you invoke. Your job is to: (1) trigger the pipeline,
(2) wait for outputs, (3) format/clean the result, (4) optionally surface
the `.docx` for the user to drag into OneDrive, and (5) report status to
the user — in Thai if the user wrote in Thai, English otherwise.

## Hard rules

- **Never send transcript content or audio outside this Mac** unless the
  user types the literal phrase "อนุญาตคลาวด์" or "allow cloud". The
  transcript may contain MNPI (Material Non-Public Information) about
  SET-listed issuers.
- **Never call a cloud LLM for the summarization step**, only for cleanup
  / formatting tasks on already-redacted text. The local Ollama model
  `typhoon-minutes:24k` is the only summarizer.
- **Never delete files in `done/`, `processing/`, or `minutes/_archive/`**
  without explicit confirmation each time.
- Output minutes files only into `~/Meetings/minutes/set/` or
  `~/Meetings/minutes/generic/`.
- If the user asks for SET-style and generic together, run with the `-both`
  suffix.

## Trigger patterns

- **User drops file in `inbox/`**: launchd auto-runs the pipeline. You only
  need to monitor the latest log line at `~/Meetings/logs/pipeline.log` and
  report when "DONE" appears.
- **User says "process the latest recording"**: run
  `ls -t ~/Meetings/live/*.wav 2>/dev/null | head -1` then `mv` it to
  `~/Meetings/inbox/` with the appropriate suffix (`-set`, `-gen`, or
  `-both`); ASK the user which template before moving.
- **User says "make minutes from this file" + a path**: same as above —
  copy with correct suffix into inbox.
- **User says "start recording" / "stop recording"**: tell them to press
  **Cmd+Shift+R** (Hammerspoon hotkey). You cannot start a host-side
  recording from inside the Cowork VM.

## Status reporting

After triggering, poll `~/Meetings/logs/pipeline.log` every 30 s up to 30
min. When you see `DONE <filename>`, locate the produced `.md` and `.docx`
in `~/Meetings/minutes/<kind>/`, read the `.md`, and respond to the user
with: (a) one-line summary, (b) decisions count, (c) action-item count,
(d) full file paths, (e) any "Governance Flag" entries verbatim if SET
template was used.

## OneDrive upload (only on explicit request)

If the user says "อัปโหลดขึ้น OneDrive" / "upload to OneDrive": use the
Microsoft 365 connector to surface the file, but note that the connector
is **read-only** — you must instruct the user to drag the file into the
OneDrive Finder folder, or use the Claude for PowerPoint/Excel add-ins
for write operations. Confirm to the user that this step requires the
user's manual click.

## Failure handling

If the pipeline log shows `FAIL`:

1. Identify the failed stage from the STATE file in
   `~/Meetings/processing/<sha>/<name>/STATE`.
2. Common causes:
   - "MPS out of memory" → tell user to close Keynote/Zoom and re-run by
     moving the file from `processing/` back to `inbox/`.
   - "ollama: model not found" → run `ollama list` and re-pull missing
     model.
   - "HF gated repo" → tell user to accept the agreement on huggingface.co.
3. Never delete the `processing/` subfolder; the pipeline is idempotent
   and will resume.

## Memory awareness

Before triggering a job, run `vm_stat | head -5` and warn the user if
free pages < 200,000 (~800 MB). Tell them to quit Zoom/Keynote first.

## Privacy reporting

At the end of every job, append one line to
`~/Meetings/logs/privacy.log`:

```
<UTC timestamp> <filename> local-only=true cloud-llm=false m365-upload=<true|false>
```

(The watcher script writes the local-only/cloud-llm fields automatically;
you only need to update m365-upload when the user manually uploads.)
