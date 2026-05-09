#!/usr/bin/env python3
"""Thai meeting-minutes pipeline.

Stages (strictly sequential to fit 24 GB unified memory on M5 Pro):
  1. preprocess - ffmpeg -> 16 kHz mono WAV
  2. asr        - mlx-whisper large-v3-turbo (--language th)
  3. diarize    - pyannote-audio community-1 (MPS)
  4. merge      - speaker-attributed transcript JSONL
  5. minutes    - Ollama Typhoon 2.5 30B-A3B map-reduce (4B fallback)
  6. render     - .md + .docx via pandoc, copy to ~/Meetings/minutes/<kind>/

Idempotent: each stage skips if its output exists. STATE file tracks progress.
Filename suffix selects template: -set, -gen, -both. Default = generic.
"""
import sys
import os
import re
import json
import gc
import hashlib
import subprocess
import shutil
from pathlib import Path

import torch
import mlx.core as mx
import ollama
from pyannote.audio import Pipeline as DiarPipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
import mlx_whisper

ROOT      = Path.home() / "Meetings"
WORK_ROOT = ROOT / "processing"
TPL_DIR   = ROOT / "templates"
SP_DIR    = TPL_DIR / "system_prompts"
MIN_DIR   = ROOT / "minutes"

WHISPER_MODEL = "mlx-community/whisper-large-v3-turbo"
LLM_MODEL     = "typhoon-minutes:24k"
LLM_FALLBACK  = "scb10x/typhoon2.5-qwen3-4b"


def sha1(p):
    return hashlib.sha1(str(p).encode()).hexdigest()[:12]


def detect_kind(name: str) -> list[str]:
    if name.endswith("-set"):
        return ["set"]
    if name.endswith("-both"):
        return ["set", "generic"]
    return ["generic"]


def free_memory():
    gc.collect()
    if torch.backends.mps.is_available():
        torch.mps.empty_cache()
    try:
        mx.metal.clear_cache()
    except Exception:
        pass


# ---------- Stage 1: preprocess ----------
def preprocess(src: Path, work: Path) -> Path:
    out = work / "raw.wav"
    if out.exists():
        return out
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(src),
         "-ac", "1", "-ar", "16000",
         "-c:a", "pcm_s16le", str(out)],
        check=True,
    )
    return out


# ---------- Stage 2: ASR ----------
def asr(wav: Path, work: Path) -> dict:
    out = work / "asr.json"
    if out.exists():
        return json.loads(out.read_text())
    result = mlx_whisper.transcribe(
        str(wav),
        path_or_hf_repo=WHISPER_MODEL,
        language="th",
        word_timestamps=True,
        condition_on_previous_text=False,
        initial_prompt="ประชุมผู้ถือหุ้น AGM EGM EBITDA NPL ROE EPS วาระ มติที่ประชุม",
    )
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2))
    free_memory()
    return result


# ---------- Stage 3: diarization ----------
def diarize(wav: Path, work: Path) -> list[dict]:
    out = work / "diar.json"
    if out.exists():
        return json.loads(out.read_text())
    pipe = DiarPipeline.from_pretrained(
        "pyannote/speaker-diarization-community-1",
        token=os.environ["HF_TOKEN"],
    )
    pipe.to(torch.device("mps" if torch.backends.mps.is_available() else "cpu"))
    with ProgressHook() as hook:
        ann = pipe(str(wav), hook=hook)
    segs = [
        {"start": float(t.start), "end": float(t.end), "speaker": s}
        for t, _, s in ann.itertracks(yield_label=True)
    ]
    out.write_text(json.dumps(segs, ensure_ascii=False, indent=2))
    del pipe
    free_memory()
    return segs


# ---------- Stage 4: merge ----------
def merge(asr_res: dict, diar: list[dict], work: Path) -> Path:
    out = work / "merged.jsonl"
    if out.exists():
        return out

    def speaker_at(t):
        for s in diar:
            if s["start"] <= t <= s["end"]:
                return s["speaker"]
        return "UNK"

    lines = []
    for seg in asr_res["segments"]:
        mid = (seg["start"] + seg["end"]) / 2
        lines.append({
            "start": seg["start"],
            "end": seg["end"],
            "speaker": speaker_at(mid),
            "text": seg["text"].strip(),
        })

    grouped, cur = [], None
    for line in lines:
        if cur and cur["speaker"] == line["speaker"]:
            cur["text"] += " " + line["text"]
            cur["end"] = line["end"]
        else:
            if cur:
                grouped.append(cur)
            cur = dict(line)
    if cur:
        grouped.append(cur)

    out.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in grouped))
    return out


# ---------- Stage 5: LLM minutes (map-reduce) ----------
def chunk_by_agenda(merged_path: Path, max_chars=12000):
    turns = [json.loads(line) for line in merged_path.read_text().splitlines()]
    text = "\n".join(
        f"[{t['speaker']} {t['start']:.0f}s] {t['text']}" for t in turns
    )
    parts = re.split(r"(?=วาระที่\s*\d+|วาระที่\s*[๑-๙])", text)
    if len(parts) < 2:
        parts = [text[i:i + max_chars] for i in range(0, len(text), max_chars - 500)]
    return [p for p in parts if p.strip()]


def llm_call(model, system, user, options=None):
    return ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        options=options or {"temperature": 0.3, "num_ctx": 24576},
    )["message"]["content"]


def generate_minutes(kind: str, merged_path: Path, work: Path) -> Path:
    out = work / f"minutes_{kind}.md"
    if out.exists():
        return out
    system = (SP_DIR / f"{kind}_th.txt").read_text()
    chunks = chunk_by_agenda(merged_path)

    map_outs = []
    for i, c in enumerate(chunks):
        cache = work / f"map_{kind}_{i:03d}.json"
        if cache.exists():
            map_outs.append(cache.read_text())
            continue
        prompt = (
            f"นี่คือส่วนที่ {i+1}/{len(chunks)} ของ transcript การประชุม "
            "กรุณาสกัดข้อมูลในรูปแบบ JSON: หัวข้อ, ประเด็นอภิปราย, "
            "มติ, action items (พร้อมผู้รับผิดชอบและกำหนดเสร็จ), คำถาม-ตอบ, "
            f"ข้อความสำคัญพร้อมเวลาอ้างอิง\n\nTRANSCRIPT:\n{c}"
        )
        try:
            r = llm_call(LLM_MODEL, system, prompt)
        except Exception:
            r = llm_call(LLM_FALLBACK, system, prompt)
        cache.write_text(r)
        map_outs.append(r)

    reduce_prompt = (
        "รวมและจัดเรียงข้อมูลทั้งหมดต่อไปนี้เป็น "
        f"\"{('รายงานการประชุม' if kind == 'set' else 'บันทึกการประชุม')}\" "
        "ตามโครงสร้างที่กำหนดในคำสั่งระบบ ห้ามแต่งเติมข้อมูลใหม่ "
        "รวมรายการที่ซ้ำกัน เรียงตามลำดับเวลา\n\n"
        + "\n---\n".join(map_outs)
    )
    try:
        final = llm_call(
            LLM_MODEL, system, reduce_prompt,
            options={"temperature": 0.2, "num_ctx": 24576, "num_predict": 8192},
        )
    except Exception:
        final = llm_call(LLM_FALLBACK, system, reduce_prompt)
    out.write_text(final)
    free_memory()
    return out


# ---------- Stage 6: render ----------
def render(md_path: Path, kind: str, src_name: str):
    target_md = MIN_DIR / kind / md_path.name.replace("minutes_", f"{src_name}-")
    target_docx = target_md.with_suffix(".docx")
    target_md.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(md_path, target_md)
    pandoc_args = ["pandoc", str(target_md), "-o", str(target_docx)]
    ref_doc = TPL_DIR / "thai-ref.docx"
    if ref_doc.exists():
        pandoc_args.extend(["--reference-doc", str(ref_doc)])
    subprocess.run(pandoc_args, check=True)
    return target_md, target_docx


# ---------- main ----------
def main(src):
    src = Path(src).resolve()
    job = WORK_ROOT / sha1(src) / src.stem
    job.mkdir(parents=True, exist_ok=True)
    state = job / "STATE"

    wav = preprocess(src, job)
    state.write_text("preprocess")

    asr_res = asr(wav, job)
    state.write_text("asr")

    diar = diarize(wav, job)
    state.write_text("diarize")

    merged = merge(asr_res, diar, job)
    state.write_text("merge")

    base = src.stem
    base_clean = re.sub(r"-(set|gen|both|meet)$", "", base)
    for kind in detect_kind(base):
        md = generate_minutes(kind, merged, job)
        state.write_text(f"minutes:{kind}")
        render(md, kind, base_clean)

    state.write_text("done")
    print(f"DONE {src.name}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: pipeline.py <audio-file>", file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1])
