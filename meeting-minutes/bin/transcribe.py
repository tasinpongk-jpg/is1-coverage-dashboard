#!/usr/bin/env python3
"""Standalone local transcription on Apple Silicon via mlx-whisper.

A thin slice of pipeline.py: just audio -> transcript. No diarization, no
LLM minutes, no docx rendering, no HF gated models, no launchd. Use this
when you only want a transcript and don't need SET-style formal minutes.

Usage
-----
    transcribe.py [options] AUDIO [AUDIO ...]

Examples
--------
    # Auto-detect language, write .txt + .json next to each input
    ./transcribe.py meeting.m4a

    # Thai meeting, also produce .srt subtitles
    ./transcribe.py --language th --formats txt,srt,json talk.m4a

    # Use the smaller/faster turbo model (default) but route output elsewhere
    ./transcribe.py --output-dir ~/Transcripts/2026-06 *.m4a

Notes
-----
Outputs are written next to each input file by default. Existing files are
overwritten. JSON includes per-segment timestamps and Whisper's detected
language; .txt is plain UTF-8 lines, one per segment.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

MODEL_ALIASES = {
    "tiny":     "mlx-community/whisper-tiny",
    "base":     "mlx-community/whisper-base",
    "small":    "mlx-community/whisper-small",
    "medium":   "mlx-community/whisper-medium",
    "large":    "mlx-community/whisper-large-v3-turbo",
    "turbo":    "mlx-community/whisper-large-v3-turbo",
    "large-v3": "mlx-community/whisper-large-v3",
}

VALID_FORMATS = {"txt", "srt", "vtt", "json"}


def fmt_ts(seconds: float, *, vtt: bool = False) -> str:
    if seconds < 0:
        seconds = 0.0
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    sep = "." if vtt else ","
    ms = int(round((s - int(s)) * 1000))
    if ms == 1000:
        ms, s = 0, s + 1
    return f"{h:02d}:{m:02d}:{int(s):02d}{sep}{ms:03d}"


def write_txt(segments: list[dict], path: Path) -> None:
    path.write_text(
        "\n".join(s["text"].strip() for s in segments) + "\n",
        encoding="utf-8",
    )


def write_srt(segments: list[dict], path: Path) -> None:
    lines: list[str] = []
    for i, s in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f"{fmt_ts(s['start'])} --> {fmt_ts(s['end'])}")
        lines.append(s["text"].strip())
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_vtt(segments: list[dict], path: Path) -> None:
    lines: list[str] = ["WEBVTT", ""]
    for s in segments:
        lines.append(
            f"{fmt_ts(s['start'], vtt=True)} --> {fmt_ts(s['end'], vtt=True)}"
        )
        lines.append(s["text"].strip())
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_json(result: dict, path: Path) -> None:
    path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def transcribe_one(
    audio: Path,
    model: str,
    language: str | None,
    initial_prompt: str | None,
    formats: set[str],
    out_dir: Path | None,
    quiet: bool,
) -> None:
    t0 = time.time()
    if not quiet:
        lang_str = language or "auto"
        print(f"▸ {audio.name}  model={model.split('/')[-1]} lang={lang_str}", flush=True)

    import mlx_whisper  # lazy: lets --help / lint work without the dep installed

    result = mlx_whisper.transcribe(
        str(audio),
        path_or_hf_repo=model,
        language=language,
        word_timestamps=False,
        condition_on_previous_text=False,
        initial_prompt=initial_prompt,
    )

    stem = audio.stem
    out_root = out_dir if out_dir is not None else audio.parent
    out_root.mkdir(parents=True, exist_ok=True)
    segments = result.get("segments") or []

    if "txt" in formats:
        write_txt(segments, out_root / f"{stem}.txt")
    if "srt" in formats:
        write_srt(segments, out_root / f"{stem}.srt")
    if "vtt" in formats:
        write_vtt(segments, out_root / f"{stem}.vtt")
    if "json" in formats:
        write_json(result, out_root / f"{stem}.json")

    if not quiet:
        dur = time.time() - t0
        detected = result.get("language", language or "auto")
        n = len(segments)
        outs = ",".join(sorted(formats))
        print(
            f"  done in {dur:.1f}s · detected={detected} · {n} segments → "
            f"{out_root}/{stem}.{{{outs}}}",
            flush=True,
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("audio", nargs="+", type=Path, help="Audio file(s)")
    p.add_argument(
        "--model",
        default="turbo",
        help=(
            "Whisper model. Aliases: "
            + ", ".join(sorted(MODEL_ALIASES))
            + ". Or pass any mlx-community/whisper-* repo. Default: turbo."
        ),
    )
    p.add_argument(
        "--language",
        default=None,
        help="ISO 639-1 code (e.g. th, en, ja). Default: auto-detect.",
    )
    p.add_argument(
        "--initial-prompt",
        default=None,
        help="Vocabulary hint to bias Whisper (e.g. domain jargon).",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Write outputs here. Default: alongside each input file.",
    )
    p.add_argument(
        "--formats",
        default="txt,json",
        help="Comma-separated subset of: " + ",".join(sorted(VALID_FORMATS)),
    )
    p.add_argument("--quiet", action="store_true", help="Suppress progress lines.")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    model = MODEL_ALIASES.get(args.model, args.model)
    formats = {f.strip() for f in args.formats.split(",") if f.strip()}
    unknown = formats - VALID_FORMATS
    if unknown:
        print(
            f"✗ unknown format(s): {','.join(sorted(unknown))} "
            f"(valid: {','.join(sorted(VALID_FORMATS))})",
            file=sys.stderr,
        )
        return 2
    if not formats:
        print("✗ at least one --formats value required", file=sys.stderr)
        return 2

    rc = 0
    for audio in args.audio:
        if not audio.exists():
            print(f"✗ {audio}: not found", file=sys.stderr)
            rc = 1
            continue
        try:
            transcribe_one(
                audio,
                model,
                args.language,
                args.initial_prompt,
                formats,
                args.output_dir,
                args.quiet,
            )
        except Exception as e:
            print(f"✗ {audio.name}: {type(e).__name__}: {e}", file=sys.stderr)
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
