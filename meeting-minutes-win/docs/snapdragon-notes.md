# Snapdragon X Elite / Windows 11 ARM64 — engineering notes

Notes on the architecture-specific decisions made for the Windows variant
of the meeting-minutes pipeline.

## Why no diarization in v1

The macOS variant uses **pyannote.audio** (community-1) for speaker
diarization. On Windows ARM64, the dependency chain is fragile:

- `pyannote.audio` requires `torch` + `torchaudio`
- PyTorch on Windows ARM64 has only had **preview wheels** since PyTorch 2.7
  (2025), with limited operator coverage
- `torchaudio` builds for Windows ARM64 lag PyTorch even further
- Even when wheels install, ONNX Runtime / sentencepiece / faiss often fall
  back to x64 emulation (Prism), wiping out any speed gain

Result: a brittle install path that frequently breaks on minor pip upgrades.
v1 ships without diarization to keep the install bulletproof.

The pipeline labels every turn as `"speaker": "UNK"` in `merged.jsonl`. The
Thai system prompts (shared with the macOS variant) instruct the LLM to use
"ผู้พูดที่ ๑ / ๒ / ..." and infer turn changes from context (greeting
phrases, question/answer markers, timestamp gaps).

## Adding diarization later (when you want it)

Two paths, in order of effort:

### Option A: WSL2 + the macOS pipeline.py

```powershell
wsl --install -d Ubuntu-24.04
# inside WSL2:
sudo apt install python3.11 python3.11-venv ffmpeg
git clone <this-repo>
cd <this-repo>/meeting-minutes
# follow the macOS install but skip Hammerspoon/launchd; run pipeline.py directly
```

WSL2 on Snapdragon X Elite gives you **ARM64 Linux**, where PyTorch wheels
are stable. Audio files in `\\wsl$\Ubuntu-24.04\home\you\Meetings\inbox\`
or via `/mnt/c/Users/.../Meetings/inbox/`.

Caveats:
- WSL2 reserves ~50% of system RAM by default; Typhoon 30B still won't fit
  in 16 GB total
- WSL2 adds ~1 GB resident overhead while running
- Audio device passthrough is messy; stay batch-only

### Option B: ONNX Runtime + community ONNX export of pyannote

Some folks have exported the pyannote segmentation model to ONNX. ONNX
Runtime has a native Windows ARM64 build with an optional **QNN execution
provider** that uses the Snapdragon Hexagon NPU. Worth investigating once
the upstream pyannote ONNX export stabilizes.

I have not validated this end-to-end — flag for future work.

## The NPU (Hexagon, 45 TOPS) — currently unused

Snapdragon X Elite includes a Hexagon NPU rated at 45 TOPS. None of the
tools in v1 use it:

| Tool       | Backend used        | NPU available? |
|------------|---------------------|----------------|
| whisper.cpp | CPU (NEON SIMD)    | Experimental QNN backend exists in upstream; not in release builds |
| Ollama (llama.cpp) | CPU (NEON)  | No QNN backend yet (as of late 2025) |
| pyannote (skipped) | n/a         | n/a            |

If/when whisper.cpp ships a stable QNN execution provider, Whisper inference
would speed up substantially (rough estimate: 3–5× over NEON CPU). Same
story for llama.cpp once a QNN backend lands. Until then, we stay on the
CPU path which is what's actually shipping.

The Microsoft **Windows AI Foundry** (Phi Silica, etc.) is NPU-accelerated
but is closed to the model — it can't run Typhoon. Not useful here.

## Why whisper.cpp instead of faster-whisper

`faster-whisper` wraps `CTranslate2`. CTranslate2 publishes wheels for:

- Linux x86_64 ✓
- Linux ARM64 ✓
- macOS ✓ (Universal)
- Windows x86_64 ✓
- **Windows ARM64** ✗ (no official wheel as of late 2025)

On Windows ARM64, faster-whisper installs only by pulling the x86_64 wheel,
which Prism then emulates. End-to-end perf is ~2× *slower* than the native
ARM64 whisper.cpp build. So we use whisper.cpp directly.

Quality is functionally identical — both wrap the same Whisper weights.

## Why Typhoon 4B and not 8B / 14B

| Model | Disk | RAM resident (4-bit) | OK on 16 GB shared? |
|-------|------|----------------------|---------------------|
| 4B    | 2.5 GB | ~3 GB             | Yes — leaves headroom for whisper.cpp + Windows |
| 8B    | 5 GB   | ~6 GB             | Borderline — must close everything |
| 14B   | 9 GB   | ~10 GB            | No on 16 GB shared with OS + GPU |
| 30B-A3B | 19 GB | ~22 GB            | No |

Typhoon 4B is the largest model that leaves room for the OS. It's smaller
than the Mac variant uses, so SET-formal Thai output quality is lower —
plan to review/lightly edit before sending.

## Why no `inotifywait`-style watcher

The macOS variant uses launchd to auto-fire the pipeline on file drops.
Windows equivalents:

- PowerShell `FileSystemWatcher` event sink — works but spawning a long-lived
  PowerShell session is awkward
- Windows Service via NSSM — proper but requires elevation and adds an
  install dependency
- Task Scheduler with file-trigger — Windows Task Scheduler has a "Custom
  event filter" trigger type but file-watching requires WMI, which is
  cumbersome

Per the v1 scope decision (smallest, fastest to ship), we skipped this.
Run `Make-Minutes.ps1` manually. If you find yourself doing it daily, the
PowerShell `FileSystemWatcher` route is the most idiomatic to add.

## Locale / IME considerations

Your laptop is set to **SE Asia Standard Time** (Bangkok) and **United
States** locale. Both work fine for the pipeline:

- whisper.cpp `--language th` is explicit, ignores OS locale
- Ollama / llama.cpp tokenizer handles Thai script regardless of locale
- pandoc renders Thai script correctly with the default font *only if* a
  Thai-capable font is installed. Windows 11 ships with **Leelawadee UI**
  which works. For SET-formal output use **TH Sarabun PSK** (free from
  https://www.f0nt.com/release/thsarabun-psk-pro/) and add a `thai-ref.docx`
  reference doc to `%USERPROFILE%\Meetings\templates\` — pipeline.py picks
  it up automatically.

## File-system path quirks the Python script handles

- `\` vs `/`: pipeline.py uses `pathlib.Path` throughout, so paths print as
  `\` on Windows and `/` on POSIX without code changes.
- Long paths: jobs are stored under `%USERPROFILE%\Meetings\processing\
  <12-char-sha>\<src-stem>\`. Total path length stays under the 260-char
  legacy limit even for AGM-style filenames.
- Non-ASCII filenames (Thai meeting names) work as long as the Windows
  console is set to UTF-8 (`chcp 65001`). The installer doesn't change this
  for you — if you see `?` characters in pipeline output, run `chcp 65001`
  in your shell first.
