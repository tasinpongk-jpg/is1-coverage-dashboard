# Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Hammerspoon hotkey does nothing | Accessibility permission missing | System Settings → Privacy & Security → Accessibility → enable Hammerspoon, then click menubar icon → Reload Config |
| `ffmpeg: Input/output error` on `:2` | Aggregate device renamed or sample rates mismatched | Audio MIDI Setup: confirm `Mic+BH` exists, both subdevices at 48000 Hz, drift correction on BlackHole row |
| Recording produces silent file | System Output not set to Multi-Output Device | System Settings → Sound → Output = your Multi-Output Device |
| Recording captures only mic, not system audio | Same as above (apps play to system output, not BlackHole directly) | Set System Output to Multi-Output |
| `pyannote` raises `401 Unauthorized` | HF token missing or gated model not accepted | Run `huggingface-cli login`; visit each gated model page and click "Agree" (see installer output for URLs) |
| `mlx_whisper` very slow on first run | Model downloading from Hugging Face (~1.6 GB for turbo) | Wait; subsequent runs use `~/.cache/huggingface/` |
| Ollama returns "model not found" | Model not pulled or wrong tag | `ollama list`; if missing, re-run installer with `SKIP_BREW=1 SKIP_PY=1 ./install.sh` to redo only Ollama |
| Ollama generation gibberish in Thai | Loaded a non-Thai-tuned model by mistake | Confirm `typhoon-minutes:24k` (or fallback) is in `pipeline.py`, not `qwen3:8b` |
| Pipeline crashes with `metal::malloc failed` during LLM step | Insufficient unified memory | Quit Keynote/Zoom/Slack/Chrome; the script auto-falls back to 4B on next attempt; or lower `num_ctx` to 16384 in the Modelfile and rebuild |
| launchd doesn't trigger on file drop | USERNAME placeholder not substituted, or agent not loaded | `launchctl print gui/$(id -u)/com.user.meetingpipeline`; if absent, re-run `install.sh`; check the WatchPaths field is your real home |
| Cowork can't see `~/Meetings` | Folder not added as trusted | Cowork → Customize → Folders → Add `~/Meetings` |
| `.docx` output has wrong fonts for Thai | Pandoc default font lacks Thai glyphs | Create `~/Meetings/templates/thai-ref.docx` with Sarabun or TH Sarabun set as the default style; pipeline picks it up automatically |
| Microsoft 365 connector says "tenant consent required" | SET IT admin hasn't approved at tenant level | Submit a SET IT ticket. Until then, drag .docx into the OneDrive Finder folder manually |
| Audio Hijack hotkey conflicts with Hammerspoon | Same key bound twice | Pick one; if Audio Hijack, comment out the Hammerspoon `hs.hotkey.bind` line |
| Typhoon outputs random English / refuses Thai | System prompt not loaded (Modelfile not built or wrong `FROM`) | `ollama show typhoon-minutes:24k --system` should print the Thai system prompt; if empty, rebuild with `ollama create typhoon-minutes:24k -f ~/Meetings/templates/Modelfile.typhoon-minutes` |
| `pipeline.log` shows the same file repeatedly | Debounce missed; file still being written from network | Edit `process_inbox.sh` and increase `sleep 5` to `sleep 15` |
| Pipeline stuck in `processing/` after crash | Mac slept or process killed mid-run | Pipeline is idempotent; just `touch ~/Meetings/processing/<sha>/<name>/raw.wav` and re-run `~/Meetings/bin/pipeline.py <audio>` to resume from last STATE |
| `vm_stat` shows < 800 MB free | Memory pressure | Cowork's `CLAUDE.md` warns automatically; quit GUI apps before kicking off another job |

## Diagnosing a failed job

```bash
# Find the job folder
ls -lt ~/Meetings/processing/*/

# Inspect the last completed stage
cat ~/Meetings/processing/<sha>/<name>/STATE

# See the tail of the pipeline log
tail -200 ~/Meetings/logs/pipeline.log
tail -200 ~/Meetings/logs/pipeline.err.log

# Resume by re-invoking the pipeline; idempotent stages will skip
~/Meetings/venv/bin/python ~/Meetings/bin/pipeline.py \
  ~/Meetings/processing/<sha>/<name>/raw.wav
```

## Resetting a stuck Ollama

```bash
# Memory leak between models? Kick the server.
killall ollama
sleep 2
open -a Ollama

# Re-pull a corrupted model
ollama rm scb10x/typhoon2.5-qwen3-30b-a3b
ollama pull scb10x/typhoon2.5-qwen3-30b-a3b
ollama create typhoon-minutes:24k -f ~/Meetings/templates/Modelfile.typhoon-minutes
```

## Verifying privacy guarantees

```bash
# Audit log: every job logs whether any cloud step occurred
cat ~/Meetings/logs/privacy.log

# Confirm Ollama isn't sending telemetry
lsof -i -n | grep -i ollama   # should show only listens on 127.0.0.1:11434
```
