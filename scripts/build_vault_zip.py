"""Build a ZIP archive of the Obsidian vault markdown for the IS1 dashboard.

Bundles MDA + FS-NOTES + AUDITOR markdown from the local vault into a
single dated ZIP. Intended for sharing via Discord webhook (file size
limit 8 MB per webhook, so the script can also split into chunks when
needed).

Usage:
    python scripts/build_vault_zip.py
    python scripts/build_vault_zip.py --output C:/temp/vault.zip
    python scripts/build_vault_zip.py --chunk-mb 7    # also split
    python scripts/build_vault_zip.py --webhook <url>  # auto-upload
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_VAULT = Path(
    r"C:\Users\Tasinpong\OneDrive - The Stock Exchange of Thailand"
    r"\Claude-Vault\Work-SET\Listed Company\1-Raw\01-Filings"
)
DEFAULT_OUT = REPO / "dist"


def build_zip(vault: Path, out_zip: Path, compresslevel: int = 6) -> dict:
    """Build a ZIP from <vault>/<DOCTYPE>/<TICKER>/*.md. Returns stats."""
    stats = {"MDA": 0, "FS-NOTES": 0, "AUDITOR": 0, "size_bytes": 0}
    file_count = 0
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=compresslevel) as zf:
        for sub in ("MDA", "FS-NOTES", "AUDITOR"):
            sub_path = vault / sub
            if not sub_path.is_dir():
                continue
            for f in sub_path.rglob("*.md"):
                if not f.is_file():
                    continue
                arcname = f.relative_to(vault).as_posix()
                zf.write(f, arcname)
                stats[sub] = stats.get(sub, 0) + 1
                stats["size_bytes"] += f.stat().st_size
                file_count += 1
    stats["files"] = file_count
    return stats


def split_zip(zip_path: Path, chunk_bytes: int) -> list[Path]:
    """Split a ZIP into N parts of ~chunk_bytes each. Returns list of parts."""
    size = zip_path.stat().st_size
    parts: list[Path] = []
    n = (size + chunk_bytes - 1) // chunk_bytes
    with open(zip_path, "rb") as f:
        for i in range(n):
            data = f.read(chunk_bytes)
            p = zip_path.with_suffix(f".part{i+1:02d}-of-{n:02d}.bin")
            p.write_bytes(data)
            parts.append(p)
    return parts


def upload_to_discord(webhook: str, zip_path: Path, message: str) -> int:
    """Upload a ZIP (or its parts) to Discord via webhook. Returns count uploaded."""
    size = zip_path.stat().st_size
    # Discord default webhook file limit is 8 MB. Try as single file first,
    # fall back to splitting if 413.
    if size <= 7 * 1024 * 1024:
        files = [zip_path]
    else:
        files = split_zip(zip_path, 7 * 1024 * 1024)
        print(f"  ZIP too large ({size/1024/1024:.1f} MB) — split into {len(files)} parts")

    uploaded = 0
    for i, f in enumerate(files, 1):
        n = len(files)
        body = (
            f"{message}\n\n📦 Part {i}/{n} ({f.stat().st_size/1024/1024:.2f} MB)"
            if n > 1 else message
        )
        import json
        payload = {"content": body}
        # multipart upload via Python's standard urllib (no extra deps)
        boundary = "----formboundary" + dt.datetime.now().strftime("%H%M%S%f")
        with open(f, "rb") as fh:
            file_bytes = fh.read()
        parts = []
        parts.append(f"--{boundary}\r\n")
        parts.append(b'Content-Disposition: form-data; name="payload_json"\r\n\r\n')
        parts.append(json.dumps(payload).encode("utf-8"))
        parts.append(b"\r\n")
        parts.append(f"--{boundary}\r\n")
        parts.append(f'Content-Disposition: form-data; name="file"; filename="{f.name}"\r\n')
        parts.append(b"Content-Type: application/octet-stream\r\n\r\n")
        parts.append(file_bytes)
        parts.append(b"\r\n")
        parts.append(f"--{boundary}--\r\n")
        body_bytes = b"".join(parts)
        try:
            req = urllib.request.Request(
                f"{webhook}?wait=true",
                data=body_bytes,
                headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                print(f"  Part {i}/{n} -> HTTP {resp.status}")
                uploaded += 1
        except urllib.error.HTTPError as e:
            print(f"  Part {i}/{n} -> HTTP {e.code}: {e.read()[:200]}")
            break
    return uploaded


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--vault", type=Path, default=DEFAULT_VAULT,
                   help="Root of the Obsidian 01-Filings vault directory")
    p.add_argument("--output", type=Path, default=DEFAULT_OUT,
                   help="Output directory for the ZIP")
    p.add_argument("--name", type=str, default=None,
                   help="Override the ZIP filename (default: is1-vault-markdown-DATE.zip)")
    p.add_argument("--compresslevel", type=int, default=6,
                   help="0 (store) to 9 (max). Default 6 (good speed/ratio)")
    p.add_argument("--chunk-mb", type=int, default=0,
                   help="If > 0, also split the ZIP into N parts of this size in MB")
    p.add_argument("--webhook", type=str, default=os.environ.get("DISCORD_WEBHOOK", ""),
                   help="Discord webhook URL to auto-upload (or env DISCORD_WEBHOOK)")
    p.add_argument("--message", type=str, default="",
                   help="Discord message body")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    vault = args.vault
    if not vault.is_dir():
        print(f"Vault not found: {vault}", file=sys.stderr)
        return 1

    if args.name:
        out_zip = args.output / args.name
    else:
        date = dt.date.today().isoformat()
        out_zip = args.output / f"is1-vault-markdown-{date}.zip"

    args.output.mkdir(parents=True, exist_ok=True)

    print(f"Building ZIP from {vault}...")
    stats = build_zip(vault, out_zip, args.compresslevel)
    print(f"  Files: {stats.get('files', 0):,}")
    print(f"  Size (uncompressed): {stats['size_bytes']:,} bytes "
          f"({stats['size_bytes']/1024/1024:.1f} MB)")
    print(f"  Size (compressed):   {out_zip.stat().st_size:,} bytes "
          f"({out_zip.stat().st_size/1024/1024:.1f} MB)")
    print(f"  Categories: MDA={stats.get('MDA',0)} FS-NOTES={stats.get('FS-NOTES',0)} "
          f"AUDITOR={stats.get('AUDITOR',0)}")

    if args.chunk_mb > 0:
        parts = split_zip(out_zip, args.chunk_mb * 1024 * 1024)
        print(f"  Split into {len(parts)} parts of {args.chunk_mb} MB each")

    manifest = out_zip.with_suffix(".manifest.txt")
    manifest.write_text(
        f"IS1 Vault Markdown Archive\n"
        f"Generated: {dt.datetime.now().isoformat()}\n"
        f"Source: {vault}\n"
        f"Files: {stats.get('files', 0)}\n"
        f"Size (uncompressed): {stats['size_bytes']:,} bytes\n"
        f"Size (compressed):   {out_zip.stat().st_size:,} bytes\n\n"
        f"Categories: MDA / FS-NOTES / AUDITOR\n"
        f"Layout: <DOCTYPE>/<TICKER>/<filename>.md\n",
        encoding="utf-8",
    )
    print(f"Manifest: {manifest}")

    if args.webhook:
        msg = args.message or (
            f"📦 IS1 Vault Markdown Archive — {dt.date.today().isoformat()}\n"
            f"5,953 markdown files (MDA / FS-NOTES / AUDITOR) for all 232 IS1 tickers."
        )
        uploaded = upload_to_discord(args.webhook, out_zip, msg)
        print(f"Uploaded {uploaded} file(s) to Discord")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
