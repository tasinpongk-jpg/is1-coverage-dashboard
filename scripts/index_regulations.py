"""Index a folder of regulation PDFs into a Gemini File Search store.

One-time / occasional LOCAL setup script for the "Lex" agent — NOT part of the
daily CI build (regulations are static, so re-run only when the PDFs change).

Gemini File Search is a fully managed RAG: it parses the PDFs, chunks + embeds
them, and serves grounded answers with page-level citations at query time.
This script just uploads each PDF into a store and records the store name in
data/regulations-index.json, which worker.js reads back (like every other
snapshot) to point the Lex agent at the right store.

Flow per file (REST, pure stdlib — no SDK):
    1. resumable upload to the Files API           -> files/<id>
    2. importFile into the File Search store       -> long-running operation
    3. poll the operation until done

Re-runs reuse the store from the manifest and skip PDFs already imported
(matched by filename); pass --reset to create a fresh store from scratch.

Usage:
    GEMINI_API_KEY=... python scripts/index_regulations.py [PDF_DIR] [--reset]

Env:
    GEMINI_API_KEY     required
    REGULATIONS_DIR    PDF folder (default: <repo>/regulations; overridden by arg)
    LEX_EMBED_MODEL    optional embedding model override for the store
"""

import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "regulations-index.json"
PDF_DIR = Path(
    next((a for a in sys.argv[1:] if not a.startswith("-")),
         os.environ.get("REGULATIONS_DIR", ROOT / "regulations"))
)
RESET = "--reset" in sys.argv

API = "https://generativelanguage.googleapis.com/v1beta"
UPLOAD_API = "https://generativelanguage.googleapis.com/upload/v1beta"
KEY = os.environ.get("GEMINI_API_KEY", "")
STORE_DISPLAY = "is1-regulations"


def _req(url, *, method="GET", data=None, headers=None):
    """Minimal JSON/bytes HTTP helper returning (status, headers, parsed_body)."""
    req = urllib.request.Request(url, data=data, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            raw = r.read()
            body = json.loads(raw) if raw and r.headers.get(
                "Content-Type", "").startswith("application/json") else (raw or None)
            return r.status, dict(r.headers), body
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code} {method} {url}\n{e.read().decode(errors='replace')}")


def find_or_create_store(reuse=True):
    """Reuse the store with our display name if it exists (Gemini caps projects
    at 10 stores), otherwise create one. With reuse=False (--reset) always make a
    fresh store so stale documents don't linger."""
    if reuse:
        _, _, b = _req(f"{API}/fileSearchStores?key={KEY}")
        for s in (b or {}).get("fileSearchStores", []):
            if s.get("displayName") == STORE_DISPLAY:
                print(f"reusing store {s['name']}")
                return s["name"]
    body = {"displayName": STORE_DISPLAY}
    embed = os.environ.get("LEX_EMBED_MODEL")
    if embed:
        body["embeddingModel"] = embed
    _, _, b = _req(f"{API}/fileSearchStores?key={KEY}", method="POST",
                   data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    name = b["name"]
    print(f"created store {name}")
    return name


def doc_name(pdf: Path) -> str:
    """Citation title for a PDF. File Search caps display_name at 512 chars and
    long Thai filenames blow past it, so truncate to a safe UTF-8 byte budget
    while keeping a readable prefix."""
    name = pdf.stem
    budget = 480  # bytes, comfortably under the 512 limit either way it's counted
    if len(name.encode("utf-8")) <= budget:
        return name
    return name.encode("utf-8")[:budget].decode("utf-8", "ignore").rstrip() + "…"


def upload_to_store(store: str, pdf: Path):
    """One-step resumable upload + import into the File Search store, naming the
    created document `displayName` so citations show a readable title (importFile
    has no displayName field; uploadToFileSearchStore does). Polls the resulting
    long-running operation to completion."""
    size = pdf.stat().st_size
    ctype = mimetypes.guess_type(pdf.name)[0] or "application/pdf"
    # 1. start a resumable session, carrying the document metadata
    _, hdrs, _ = _req(
        f"{UPLOAD_API}/{store}:uploadToFileSearchStore?key={KEY}", method="POST",
        data=json.dumps({"displayName": doc_name(pdf), "mimeType": ctype}).encode(),
        headers={
            "X-Goog-Upload-Protocol": "resumable",
            "X-Goog-Upload-Command": "start",
            "X-Goog-Upload-Header-Content-Length": str(size),
            "X-Goog-Upload-Header-Content-Type": ctype,
            "Content-Type": "application/json",
        })
    upload_url = hdrs.get("X-Goog-Upload-URL") or hdrs.get("x-goog-upload-url")
    if not upload_url:
        raise SystemExit(f"no upload URL returned for {pdf.name}")
    # 2. send the bytes and finalize -> long-running operation
    _, _, op = _req(upload_url, method="POST", data=pdf.read_bytes(), headers={
        "X-Goog-Upload-Command": "upload, finalize",
        "X-Goog-Upload-Offset": "0",
        "Content-Type": ctype,
    })
    # 3. poll the operation until the document is indexed
    name = (op or {}).get("name")
    for _ in range(90):
        if not name or op.get("done"):
            if op.get("error"):
                raise SystemExit(f"upload failed for {pdf.name}: {op['error']}")
            return
        time.sleep(2)
        _, _, op = _req(f"{API}/{name}?key={KEY}")
    raise SystemExit(f"upload timed out for {pdf.name}")


def main():
    if not KEY:
        raise SystemExit("GEMINI_API_KEY is not set")
    pdfs = sorted(PDF_DIR.glob("*.pdf"))
    if not pdfs:
        raise SystemExit(f"no PDFs found in {PDF_DIR}")

    manifest = {}
    if OUT.exists() and not RESET:
        manifest = json.loads(OUT.read_text(encoding="utf-8"))
    store = manifest.get("store")
    if not store or RESET:
        store = find_or_create_store(reuse=not RESET)
        manifest = {"store": store, "files": []}

    done = {f["name"] for f in manifest.get("files", [])}
    print(f"store={store}  {len(pdfs)} PDFs in {PDF_DIR}  ({len(done)} already indexed)")

    for pdf in pdfs:
        if pdf.name in done:
            continue
        print(f"  uploading {pdf.name} ...", flush=True)
        upload_to_store(store, pdf)
        manifest["files"].append({"name": pdf.name, "title": doc_name(pdf)})
        manifest["indexedAt"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"    indexed ({len(manifest['files'])}/{len(pdfs)})")

    print(f"done — manifest written to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
