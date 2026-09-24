"""Build the page-cited regulation corpus used by Lex on MiniMax M3.

The source PDFs stay local and untracked. This script extracts their text with
Poppler, splits long pages into compact chunks, and writes one deployable JSON
asset for deterministic retrieval inside worker.js.

Usage:
    python3 scripts/build_lex_corpus.py [PDF_DIR]

Env:
    REGULATIONS_DIR  PDF folder when no positional path is supplied
    PDFTOTEXT        optional path to the pdftotext executable
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "lex-regulations.json"
SOURCE_MANIFEST = ROOT / "data" / "regulations-manifest.json"
PDF_DIR = Path(
    next(
        (arg for arg in sys.argv[1:] if not arg.startswith("-")),
        os.environ.get("REGULATIONS_DIR", ROOT / "regulations"),
    )
)
PDFTOTEXT = os.environ.get("PDFTOTEXT") or shutil.which("pdftotext")
MAX_CHARS = 4_200


def clean_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).replace("\x00", "")
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r" *\n *", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def split_long(value: str, limit: int = MAX_CHARS) -> list[str]:
    if len(value) <= limit:
        return [value] if value else []
    parts: list[str] = []
    rest = value
    while len(rest) > limit:
        cut = max(rest.rfind("\n", 0, limit), rest.rfind(" ", 0, limit))
        if cut < limit // 2:
            cut = limit
        parts.append(rest[:cut].strip())
        rest = rest[cut:].strip()
    if rest:
        parts.append(rest)
    return parts


def extract_pages(pdf: Path) -> list[str]:
    result = subprocess.run(
        [PDFTOTEXT, "-raw", "-enc", "UTF-8", str(pdf), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    pages = [clean_text(page) for page in result.stdout.split("\f")]
    while pages and not pages[-1]:
        pages.pop()
    return pages


def expected_names() -> set[str] | None:
    if not SOURCE_MANIFEST.exists():
        return None
    data = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))
    return {str(row["name"]) for row in data.get("files", [])}


def main() -> int:
    if not PDFTOTEXT:
        raise SystemExit("pdftotext is required; install Poppler or set PDFTOTEXT")
    if not PDF_DIR.is_dir():
        raise SystemExit(f"regulation PDF directory not found: {PDF_DIR}")

    pdfs = sorted(PDF_DIR.glob("*.pdf"), key=lambda path: path.name)
    if not pdfs:
        raise SystemExit(f"no PDFs found in {PDF_DIR}")

    expected = expected_names()
    actual = {pdf.name for pdf in pdfs}
    if expected is not None and actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise SystemExit(
            "PDF set does not match regulations-manifest.json: "
            f"missing={missing[:5]} extra={extra[:5]}"
        )

    documents: list[dict[str, object]] = []
    chunks: list[dict[str, object]] = []
    page_count = 0
    empty_pages = 0

    for pdf in pdfs:
        pages = extract_pages(pdf)
        usable_pages = 0
        for page_number, text in enumerate(pages, start=1):
            if not text:
                empty_pages += 1
                continue
            usable_pages += 1
            page_count += 1
            for part_number, part in enumerate(split_long(text), start=1):
                chunks.append(
                    {
                        "document": pdf.name,
                        "title": pdf.stem,
                        "page": page_number,
                        "part": part_number,
                        "text": part,
                    }
                )
        documents.append(
            {
                "name": pdf.name,
                "title": pdf.stem,
                "pages": usable_pages,
                "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            }
        )
        print(f"extracted {pdf.name}: {usable_pages} text pages")

    payload = {
        "schemaVersion": 1,
        "builtAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "SET Rulebook PDFs",
        "documentCount": len(documents),
        "pageCount": page_count,
        "chunkCount": len(chunks),
        "emptyPageCount": empty_pages,
        "documents": documents,
        "chunks": chunks,
    }
    OUT.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    print(
        f"wrote {OUT.relative_to(ROOT)}: {len(documents)} documents, "
        f"{page_count} pages, {len(chunks)} chunks, {OUT.stat().st_size:,} bytes"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
