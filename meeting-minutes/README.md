# Thai meeting-minutes pipeline (M5 Pro / Cowork)

A fully local, privacy-aware Thai meeting-minutes pipeline for MacBook Pro M5
Pro (24 GB, macOS 26 Tahoe), orchestrated by **Claude Cowork** for trigger and
reporting, with all heavy ASR / diarization / LLM work running on the host
Mac. Designed for SET Issuer-Department workflows where transcripts may
contain MNPI and must never leave the device.

## Quick start

```bash
# 1. Clone this repo (already done if you're reading this)
# 2. Run the installer from the repo root
./meeting-minutes/bin/install.sh

# 3. Complete the manual steps the installer prints
#    (Audio MIDI Setup, TCC permissions, HF gated-model agreements,
#     Cowork trusted folder)

# 4. Drop a Thai .m4a into the inbox and watch
cp my-meeting.m4a ~/Meetings/inbox/2026-05-14-test-set.m4a
tail -f ~/Meetings/logs/pipeline.log
```

Filename suffix selects the output template:

| Suffix         | Template                            | Output dir                    |
|----------------|-------------------------------------|-------------------------------|
| `…-set.m4a`    | SET-style รายงานการประชุม (formal)  | `~/Meetings/minutes/set/`     |
| `…-gen.m4a`    | Generic professional minutes        | `~/Meetings/minutes/generic/` |
| `…-both.m4a`   | Both                                | both folders                  |
| (no suffix)    | Generic                             | `~/Meetings/minutes/generic/` |

## Architecture

```
        Hammerspoon              File drop
        Cmd+Shift+R              into ~/Meetings/inbox/
              │                          │
              ▼                          ▼
        ffmpeg → ~/Meetings/live/        launchd WatchPath
              │                          │ (10s throttle, 5s debounce)
              └──────────► inbox/ ──────►┘
                                         │
                                         ▼
                          process_inbox.sh   (~/Meetings/bin/)
                                         │
                                         ▼
                          pipeline.py — strictly sequential
                            ├─ ffmpeg preprocess (16 kHz mono)
                            ├─ mlx-whisper large-v3-turbo  (Thai)
                            ├─ pyannote-audio diarization  (MPS)
                            ├─ merge speaker turns
                            ├─ Ollama Typhoon 2.5 30B-A3B  (4B fallback)
                            └─ pandoc → .md + .docx
                                         │
                                         ▼
                          ~/Meetings/minutes/{set,generic}/
                                         │
                                         ▼
                          Cowork reads, summarizes for the user
```

The pipeline is **strictly sequential** because Whisper-large + pyannote +
Typhoon-30B + Keynote will not co-exist in 24 GB. Each stage flushes MLX/MPS
caches before the next loads. The pipeline auto-falls back to the 4B Typhoon
model on out-of-memory errors.

Cowork runs inside Apple Virtualization Framework's Linux VM and **cannot**
directly use the host's Neural Engine, BlackHole, or Ollama. So Cowork is the
**orchestrator and reporter only** — the host CLI does all the heavy lifting,
triggered by file drop into `~/Meetings/inbox/`.

## What's in this directory

```
meeting-minutes/
├── README.md                                  this file
├── bin/
│   ├── install.sh                             one-command installer (idempotent)
│   ├── uninstall.sh                           removes launchd + symlinks
│   ├── preflight.sh                           PASS/FAIL/WARN environment check
│   ├── pipeline.py                            6-stage Python orchestrator
│   ├── process_inbox.sh                       launchd-invoked watcher
│   └── cleanup_processing.sh                  30-day GC for stale jobs
├── templates/
│   ├── Modelfile.typhoon-minutes              30B Ollama Modelfile (24k ctx)
│   ├── Modelfile.typhoon-minutes-4b           4B fallback (32k ctx)
│   └── system_prompts/
│       ├── set_th.txt                         SET-style รายงานการประชุม
│       └── generic_th.txt                     Generic Thai minutes
├── hammerspoon/
│   └── init.lua                               Cmd+Shift+R recorder toggle
├── launchd/
│   └── com.user.meetingpipeline.plist         template (USERNAME placeholder)
├── cowork/
│   ├── CLAUDE.md                              folder instructions for ~/Meetings/
│   └── skills/meeting-minutes/SKILL.md        Cowork skill definition
└── docs/
    ├── audio-setup.md                         Audio MIDI Setup walkthrough
    └── troubleshooting.md                     symptom → fix table
```

After `install.sh` runs, the live deployment looks like:

```
~/Meetings/
├── inbox/             ← drop audio here
├── live/              ← Hammerspoon writes here
├── processing/        ← per-job working dir (idempotent, sha-named)
├── done/              ← completed audio archived here
├── minutes/{set,generic,_archive}/
├── bin/               ← symlinks to repo's bin/
├── templates/         ← symlinks to repo's templates/
├── logs/              ← pipeline.log + privacy.log
├── venv/              ← Python 3.11 + mlx-whisper + pyannote
└── CLAUDE.md          ← symlink, auto-loaded by Cowork
```

Editing prompts or scripts in the repo immediately affects the live deployment
(symlinks). Re-run `install.sh` only after pulling repo updates that touch the
launchd plist, the Modelfiles, or installed packages.

## Daily flows

**Live recording (you are presenting):**

1. Confirm Hammerspoon menubar shows `●`.
2. System Settings → Sound → Output = your **Multi-Output Device**.
3. Press **Cmd+Shift+R** to start. Menubar → `🔴 REC`.
4. Press again to stop. File auto-moves to `~/Meetings/inbox/`.
5. The pipeline runs as generic by default. To force SET-style, rename the
   inbox file to add `-set` *before* launchd's debounce expires (~5 s),
   or ask Cowork to re-trigger after renaming.

**Imported audio:**

1. Rename to encode template choice: `2026-05-14-AGM-PTT-set.m4a`.
2. Drop into `~/Meetings/inbox/`. launchd fires within ~10 s.
3. Outputs: `~/Meetings/minutes/set/2026-05-14-AGM-PTT-set.md` (+ `.docx`).

**Cowork-driven workflow:**

1. Open Claude Desktop → Cowork (in `~/Meetings/`).
2. Cowork auto-loads `CLAUDE.md` for context.
3. Say "ประมวลผลไฟล์ล่าสุดเป็น SET-style" / "process the latest recording
   as SET-style" → Cowork moves the live file with the right suffix and
   tails the log.
4. ~8–14 min later (60-min audio), Cowork reports back with file paths,
   decision count, action-item count, and any Governance Flag entries.

## Privacy boundary

**Stays 100% local:** audio (`live/`, `inbox/`, `done/`), transcripts
(`asr.json`, `merged.jsonl`), diarization, LLM minutes (`.md`, `.docx`).

**Crosses the boundary** (only when user explicitly asks):
- Claude Desktop / Cowork prompts and tool I/O reach Anthropic when Cowork is
  active. The pipeline mitigates this by keeping summarization local-only —
  Cowork only reads the already-summarized `.md`, never the raw transcript.
  Cowork is forbidden by `CLAUDE.md` and `SKILL.md` from summarizing.
- M365 connector (read-only) when user invokes OneDrive/Teams operations.
- HF model downloads (one-time, anonymous).

The literal phrase **"อนุญาตคลาวด์"** / **"allow cloud"** is the only escape
hatch that lets Cowork escalate text to a cloud LLM — by user typing, never
inferred.

Each pipeline run appends one audit line to `~/Meetings/logs/privacy.log`:

```
2026-05-14T03:21:08Z 2026-05-14-AGM-PTT-set.m4a local-only=true cloud-llm=false m365-upload=false
```

## Memory and timing on M5 Pro 24 GB

| Audio length | Preprocess | ASR    | Diarize | Minutes | Total       |
|--------------|------------|--------|---------|---------|-------------|
| 30 min       | ~15 s      | 2–3 m  | 30–60 s | 2–3 m   | **~6 m**    |
| 60 min       | ~30 s      | 4–6 m  | 1–2 m   | 3–5 m   | **~10 m**   |
| 3 hr (AGM)   | ~90 s      | 12–18m | 4–7 m   | 6–10 m  | **~25–35m** |

Quit Keynote/Zoom/Slack/Chrome before kicking off long jobs. The pipeline
detects metal::malloc OOM and auto-retries the failing step on the 4B model.

## See also

- `docs/audio-setup.md` — BlackHole + Multi-Output + Aggregate Device
- `docs/troubleshooting.md` — symptom → fix table
- `cowork/CLAUDE.md` — what Cowork sees in `~/Meetings/`
- `cowork/skills/meeting-minutes/SKILL.md` — Cowork skill definition
