# Thai meeting-minutes pipeline — Windows ARM64 (Snapdragon X Elite)

Batch-only variant of the meeting-minutes pipeline, sized for a 16 GB
Snapdragon X Elite Windows 11 laptop (no GPU). Uses **whisper.cpp**
(native ARM64) and **Ollama Typhoon 4B** (4-bit, CPU). No recording,
no live capture, no diarization — just `Make-Minutes -Audio file.m4a` and
get `.md` + `.docx` out.

For the full M5 Pro / Cowork variant with live recording and Typhoon 30B,
see `../meeting-minutes/`.

## Quick start

```powershell
# from the repo root
.\meeting-minutes-win\bin\install.ps1

# process an audio file (auto = uses suffix on filename, default generic)
.\meeting-minutes-win\bin\Make-Minutes.ps1 -Audio C:\path\to\meeting.m4a

# or force SET-style without renaming the file
.\meeting-minutes-win\bin\Make-Minutes.ps1 -Audio C:\path\to\meeting.m4a -Kind set

# both styles in one run
.\meeting-minutes-win\bin\Make-Minutes.ps1 -Audio C:\path\to\meeting.m4a -Kind both
```

Output lands in `%USERPROFILE%\Meetings\minutes\{set,generic}\`.

## Filename suffix → template

| Suffix         | Template                            | Output                                    |
|----------------|-------------------------------------|-------------------------------------------|
| `…-set.m4a`    | SET-style รายงานการประชุม (formal)  | `%USERPROFILE%\Meetings\minutes\set\`     |
| `…-gen.m4a`    | Generic professional minutes        | `%USERPROFILE%\Meetings\minutes\generic\` |
| `…-both.m4a`   | Both                                | both folders                              |
| (no suffix)    | Generic                             | `…\generic\`                              |

`Make-Minutes.ps1 -Kind set` adds the suffix for you (creates a copy with
the right name); the Python script reads the suffix from the filename.

## What runs and what doesn't

| Component | Status on Snapdragon X Elite | Notes |
|---|---|---|
| Python 3.12 (orchestrator) | Native ARM64 ✓ | `urllib`, `subprocess` only — zero ML deps |
| ffmpeg | Native ARM64 ✓ | Gyan.FFmpeg via winget |
| whisper.cpp `whisper-cli.exe` | Native ARM64 ✓ | NEON SIMD; ~1× real-time for large-v3-turbo q5_0 |
| Ollama + Typhoon 4B | Native ARM64 ✓ | llama.cpp ARM optimizations; ~10–20 min for 60-min meeting |
| pandoc | Native ARM64 ✓ | since pandoc 3.5 |
| pyannote diarization | **Skipped** | PyTorch ARM64 Windows wheels are unreliable. Speakers labeled "ผู้พูดที่ ๑/๒/..." by the LLM from context. See `docs/snapdragon-notes.md` for adding it later via WSL2. |
| Live recording | **Out of scope** for v1 | Use OBS Studio / Voice Recorder / Audio Hijack equivalent and drop the file in. |
| launchd file watcher | **Not used** | Manual run via `Make-Minutes.ps1`. |
| Cowork orchestration | **Not available** | Cowork's macOS Virtualization-framework VM is Mac-only. Use Claude Code or Claude Desktop chat to drive the script. |

## Realistic timing on Snapdragon X Elite (X1E78100, 12-core Oryon @ 3.4 GHz)

| Audio length | Preprocess | ASR (whisper-large-v3-turbo q5_0) | Minutes (Typhoon 4B) | Total       |
|--------------|------------|-----------------------------------|----------------------|-------------|
| 30 min       | ~10 s      | 4–6 min                           | 5–8 min              | **~10–15 m** |
| 60 min       | ~20 s      | 8–12 min                          | 10–15 min            | **~20–30 m** |
| 3 hr (AGM)   | ~60 s      | 25–35 min                         | 20–30 min            | **~50–70 m** |

These are usable for occasional meetings. Daily AGM-style use is borderline
without a GPU; for that, either swap to a Linux box with NVIDIA, or run
the M5 Pro variant on a separate Mac.

## What's in this directory

```
meeting-minutes-win/
├── README.md
├── bin/
│   ├── install.ps1            idempotent installer (winget + Ollama + whisper.cpp + model)
│   ├── preflight.ps1          PASS/WARN/FAIL environment check
│   ├── pipeline.py            Python orchestrator (no diarization)
│   └── Make-Minutes.ps1       PowerShell wrapper that adds suffix + memory warning
└── docs/
    └── snapdragon-notes.md    ARM64-specific gotchas, NPU notes, adding diarization later
```

The Modelfiles and Thai system prompts are **shared** with the macOS variant
in `../meeting-minutes/templates/` — edits stay in sync. The Windows
installer points Ollama at `../meeting-minutes/templates/Modelfile.typhoon-minutes-4b`
when building the model.

## Memory tips (16 GB shared LPDDR5x)

- Typhoon 4B resident: ~2.5–3 GB
- whisper.cpp during ASR: ~1.5–2 GB
- ffmpeg + Python: < 500 MB
- Windows + browser + Teams: easily 6–8 GB

**Close Chrome, Slack, Teams, OneDrive, and any IDE before kicking off a long
job.** `Make-Minutes.ps1` will warn and ask for confirmation if free memory
is below 4 GB.

## Privacy boundary

Same as the macOS variant — fully local:

- `whisper.cpp` runs offline once the model is downloaded
- Ollama with Typhoon 4B runs offline (`ollama` listens only on 127.0.0.1)
- No cloud LLM is called for summarization
- Output `.md` / `.docx` stay on your laptop until you choose to share

The only cloud touchpoints during install are:
- winget (Microsoft Store) for ffmpeg / pandoc / Python
- ollama.com for the Ollama installer
- huggingface.co for the whisper.cpp model file (anonymous download, no telemetry)
- github.com release assets for whisper.cpp binaries

After install, run `meeting-minutes-win\bin\preflight.ps1` to confirm
nothing dialed home unexpectedly.

## See also

- `docs/snapdragon-notes.md` — ARM64 caveats, why no diarization in v1, NPU acceleration future
- `../meeting-minutes/README.md` — the M5 Pro / Cowork variant
- `../meeting-minutes/templates/system_prompts/` — the Thai system prompts used by both variants
