#!/usr/bin/env python3
"""Thai meeting-minutes pipeline — Windows ARM64 (Snapdragon X Elite, CPU-only).

Stages (sequential, fits on 16 GB):
  1. preprocess - ffmpeg -> 16 kHz mono WAV
  2. asr        - whisper.cpp large-v3-turbo q5_0 (CPU + NEON), language=th
  3. minutes    - Ollama Typhoon 2.5 4B map-reduce, 4-bit on CPU
  4. render     - .md + .docx via pandoc

No diarization (pyannote PyTorch wheels are not viable on Windows ARM64).
Speakers are labeled "ผู้พูดที่ ๑/๒/..." by the LLM from context.

Idempotent: each stage skips if its output exists. STATE file tracks progress.
Filename suffix selects template: -set, -gen, -both. Default = generic.

Usage:  python pipeline.py <audio-file>
Env:    OLLAMA_HOST (default http://127.0.0.1:11434)
        WHISPER_BIN (default whisper-cli.exe on PATH)
        WHISPER_MODEL (default %USERPROFILE%\\Meetings\\models\\ggml-large-v3-turbo-q5_0.bin)
        MEETINGS_ROOT (default %USERPROFILE%\\Meetings)
        SHARED_TEMPLATES (default <repo>/meeting-minutes/templates)
"""
import sys
import os
import re
import json
import hashlib
import shutil
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(os.environ.get("MEETINGS_ROOT",
                           Path.home() / "Meetings"))
WORK_ROOT = ROOT / "processing"
MIN_DIR = ROOT / "minutes"

# Shared templates live in the repo so macOS and Windows variants stay in sync.
SHARED_TEMPLATES = Path(os.environ.get(
    "SHARED_TEMPLATES",
    Path(__file__).resolve().parent.parent.parent / "meeting-minutes" / "templates",
))
SP_DIR = SHARED_TEMPLATES / "system_prompts"

WHISPER_BIN = os.environ.get("WHISPER_BIN", "whisper-cli.exe")
WHISPER_MODEL = Path(os.environ.get(
    "WHISPER_MODEL",
    ROOT / "models" / "ggml-large-v3-turbo-q5_0.bin",
))
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")
LLM_MODEL = "typhoon-minutes-4b:32k"
LLM_FALLBACK = "scb10x/typhoon2.5-qwen3-4b"


def sha1(p: Path) -> str:
    return hashlib.sha1(str(p).encode()).hexdigest()[:12]


def detect_kind(stem: str) -> list[str]:
    if stem.endswith("-set"):
        return ["set"]
    if stem.endswith("-both"):
        return ["set", "generic"]
    return ["generic"]


# ---------- Stage 1: preprocess ----------
def preprocess(src: Path, work: Path) -> Path:
    out = work / "raw.wav"
    if out.exists():
        return out
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src),
         "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(out)],
        check=True,
    )
    return out


# ---------- Stage 2: ASR via whisper.cpp ----------
def asr(wav: Path, work: Path) -> dict:
    out = work / "asr.json"
    if out.exists():
        return json.loads(out.read_text(encoding="utf-8"))
    if not WHISPER_MODEL.exists():
        raise FileNotFoundError(
            f"whisper.cpp model not found: {WHISPER_MODEL}\n"
            "Re-run install.ps1 or download manually from "
            "https://huggingface.co/ggerganov/whisper.cpp/tree/main"
        )
    # whisper.cpp writes <basename>.json next to <basename>.wav when -oj is set.
    subprocess.run(
        [WHISPER_BIN,
         "-m", str(WHISPER_MODEL),
         "-f", str(wav),
         "-l", "th",
         "-oj",                       # JSON output
         "-of", str(work / "raw"),    # output basename (no extension)
         "--prompt", "ประชุมผู้ถือหุ้น AGM EGM EBITDA NPL ROE EPS วาระ มติที่ประชุม"],
        check=True,
    )
    raw_json = work / "raw.json"
    data = json.loads(raw_json.read_text(encoding="utf-8"))
    # Normalize whisper.cpp's schema to look like OpenAI Whisper's `segments`.
    segments = []
    for s in data.get("transcription", []):
        # whisper.cpp timestamps are HH:MM:SS,mmm strings; offsets are in ms.
        offsets = s.get("offsets", {})
        segments.append({
            "start": offsets.get("from", 0) / 1000.0,
            "end":   offsets.get("to", 0) / 1000.0,
            "text":  s.get("text", "").strip(),
        })
    normalized = {"segments": segments}
    out.write_text(json.dumps(normalized, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    return normalized


# ---------- Stage 3: merge (no diarization → all speaker UNK) ----------
def merge(asr_res: dict, work: Path) -> Path:
    out = work / "merged.jsonl"
    if out.exists():
        return out
    lines = []
    for seg in asr_res["segments"]:
        if not seg["text"]:
            continue
        lines.append({
            "start": seg["start"],
            "end": seg["end"],
            "speaker": "UNK",
            "text": seg["text"],
        })
    out.write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in lines),
        encoding="utf-8",
    )
    return out


# ---------- Stage 4: LLM minutes ----------
def chunk_by_agenda(merged_path: Path, max_chars: int = 12000) -> list[str]:
    turns = [json.loads(line) for line in
             merged_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    text = "\n".join(f"[{t['speaker']} {t['start']:.0f}s] {t['text']}" for t in turns)
    parts = re.split(r"(?=วาระที่\s*\d+|วาระที่\s*[๑-๙])", text)
    if len(parts) < 2:
        parts = [text[i:i + max_chars]
                 for i in range(0, len(text), max_chars - 500)]
    return [p for p in parts if p.strip()]


def ollama_chat(model: str, system: str, user: str, options: dict | None = None) -> str:
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "options": options or {"temperature": 0.3, "num_ctx": 16384},
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{OLLAMA_HOST}/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=600) as resp:
        return json.loads(resp.read())["message"]["content"]


def generate_minutes(kind: str, merged_path: Path, work: Path) -> Path:
    out = work / f"minutes_{kind}.md"
    if out.exists():
        return out
    system = (SP_DIR / f"{kind}_th.txt").read_text(encoding="utf-8")
    chunks = chunk_by_agenda(merged_path)

    map_outs = []
    for i, c in enumerate(chunks):
        cache = work / f"map_{kind}_{i:03d}.txt"
        if cache.exists():
            map_outs.append(cache.read_text(encoding="utf-8"))
            continue
        prompt = (
            f"นี่คือส่วนที่ {i+1}/{len(chunks)} ของ transcript การประชุม "
            "กรุณาสกัดข้อมูล: หัวข้อ, ประเด็นอภิปราย, มติ, action items "
            "(พร้อมผู้รับผิดชอบและกำหนดเสร็จ), คำถาม-ตอบ, "
            f"ข้อความสำคัญพร้อมเวลาอ้างอิง\n\nTRANSCRIPT:\n{c}"
        )
        try:
            r = ollama_chat(LLM_MODEL, system, prompt)
        except (urllib.error.URLError, KeyError):
            r = ollama_chat(LLM_FALLBACK, system, prompt)
        cache.write_text(r, encoding="utf-8")
        map_outs.append(r)

    reduce_prompt = (
        "รวมและจัดเรียงข้อมูลทั้งหมดต่อไปนี้เป็น "
        f"\"{('รายงานการประชุม' if kind == 'set' else 'บันทึกการประชุม')}\" "
        "ตามโครงสร้างที่กำหนดในคำสั่งระบบ ห้ามแต่งเติมข้อมูลใหม่ "
        "รวมรายการที่ซ้ำกัน เรียงตามลำดับเวลา\n\n"
        + "\n---\n".join(map_outs)
    )
    try:
        final = ollama_chat(
            LLM_MODEL, system, reduce_prompt,
            options={"temperature": 0.2, "num_ctx": 16384, "num_predict": 8192},
        )
    except (urllib.error.URLError, KeyError):
        final = ollama_chat(LLM_FALLBACK, system, reduce_prompt)
    out.write_text(final, encoding="utf-8")
    return out


# ---------- Stage 5: render ----------
def render(md_path: Path, kind: str, src_name: str) -> tuple[Path, Path]:
    target_md = MIN_DIR / kind / md_path.name.replace("minutes_", f"{src_name}-")
    target_docx = target_md.with_suffix(".docx")
    target_md.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(md_path, target_md)
    pandoc_args = ["pandoc", str(target_md), "-o", str(target_docx)]
    ref_doc = ROOT / "templates" / "thai-ref.docx"
    if ref_doc.exists():
        pandoc_args.extend(["--reference-doc", str(ref_doc)])
    subprocess.run(pandoc_args, check=True)
    return target_md, target_docx


# ---------- main ----------
def main(src_arg: str) -> None:
    src = Path(src_arg).resolve()
    if not src.exists():
        sys.exit(f"audio file not found: {src}")
    job = WORK_ROOT / sha1(src) / src.stem
    job.mkdir(parents=True, exist_ok=True)
    state = job / "STATE"

    wav = preprocess(src, job)
    state.write_text("preprocess")

    asr_res = asr(wav, job)
    state.write_text("asr")

    merged = merge(asr_res, job)
    state.write_text("merge")

    base = src.stem
    base_clean = re.sub(r"-(set|gen|both|meet)$", "", base)
    for kind in detect_kind(base):
        md = generate_minutes(kind, merged, job)
        state.write_text(f"minutes:{kind}")
        md_out, docx_out = render(md, kind, base_clean)
        print(f"  {kind}: {md_out}")
        print(f"  {kind}: {docx_out}")

    state.write_text("done")
    print(f"DONE {src.name}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: pipeline.py <audio-file>")
    main(sys.argv[1])
