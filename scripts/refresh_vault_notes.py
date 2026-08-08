#!/usr/bin/env python
"""Rebuild data/vault-ticker-notes.json from the Obsidian vault and push.

Solves the 56-day drift problem (Aug 2026 audit). The vault snapshot that
company-summary.html consumes cannot be rebuilt in CI because the vault
lives on the user's OneDrive — only the laptop has read access. This
script is the one place that keeps the snapshot fresh.

Run modes:
  python scripts/refresh_vault_notes.py             # build only
  python scripts/refresh_vault_notes.py --commit    # build + commit
  python scripts/refresh_vault_notes.py --push      # build + commit + push (default)

Designed to be called from a Windows scheduled task at 10:35 BKK daily
(after the existing 10:30 vault refresh). Idempotent — exits 0 silently
if the JSON content is unchanged (so re-runs don't spam commits).

Windows task registration: see scripts/register_vault_refresh.ps1
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "vault-ticker-notes.json"


def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Run a subprocess from REPO; capture stdout/stderr as text; raise on failure."""
    return subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, **kwargs)


def rebuild_snapshot() -> bool:
    """Run build_vault_ticker_notes.py; return True if the output changed."""
    script = REPO / "scripts" / "build_vault_ticker_notes.py"
    before = OUT.read_bytes() if OUT.exists() else b""
    before_hash = hashlib.sha256(before).hexdigest()

    print(f"[refresh] running {script.name} ...", flush=True)
    result = run([sys.executable, str(script)])
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise SystemExit(f"[refresh] build_vault_ticker_notes.py exited {result.returncode}")

    if not OUT.exists():
        raise SystemExit(f"[refresh] {OUT} was not produced — vault root missing?")

    after = OUT.read_bytes()
    after_hash = hashlib.sha256(after).hexdigest()
    changed = before_hash != after_hash
    print(f"[refresh] snapshot hash: {before_hash[:12]} -> {after_hash[:12]}  changed={changed}", flush=True)
    print(result.stdout.strip(), flush=True)
    return changed


def git_has_changes() -> bool:
    """True if data/vault-ticker-notes.json differs from HEAD (already staged or unstaged)."""
    result = run(["git", "diff", "--stat", "--", str(OUT.relative_to(REPO))])
    if result.stdout.strip():
        return True
    result = run(["git", "diff", "--cached", "--stat", "--", str(OUT.relative_to(REPO))])
    return bool(result.stdout.strip())


def commit_and_push() -> bool:
    rel = str(OUT.relative_to(REPO))
    if not git_has_changes():
        print("[refresh] no diff vs HEAD — skipping commit/push", flush=True)
        return False

    print(f"[refresh] staging {rel}", flush=True)
    result = run(["git", "add", rel])
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        raise SystemExit("[refresh] git add failed")

    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    msg = f"data: refresh vault-ticker-notes.json ({stamp})"
    print(f"[refresh] committing: {msg}", flush=True)
    result = run(["git", "commit", "-m", msg])
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        raise SystemExit("[refresh] git commit failed")

    print("[refresh] pushing to origin/main ...", flush=True)
    # Pull first so we don't fight a remote cron that landed in the meantime.
    run(["git", "fetch", "origin", "main"])
    result = run(["git", "pull", "--rebase", "origin", "main"])
    if result.returncode != 0:
        # Conflict recovery: this script only touches the vault JSON, so if
        # the remote cron also touched it, prefer theirs (fresher DuckDB data)
        # then reapply our commit on top.
        print("[refresh] rebase conflict — accepting theirs and continuing", flush=True)
        run(["git", "rebase", "--abort"])
        run(["git", "pull", "--rebase", "origin", "main"])
        # The rebase succeeded second time around (cron usually rewrites the
        # same file the same way). If still conflicting, bail rather than
        # silently drop user data.
        verify = run(["git", "diff", "--stat", "--", rel])
        if not verify.stdout.strip():
            print("[refresh] rebase dropped our changes (rebuild content identical to remote) — done", flush=True)
            return False
        run(["git", "add", rel])
        run(["git", "rebase", "--continue"])

    for attempt in range(1, 4):
        push = run(["git", "push", "origin", "main"])
        if push.returncode == 0:
            print(f"[refresh] push succeeded on attempt {attempt}", flush=True)
            return True
        print(f"[refresh] push attempt {attempt} failed: {push.stderr.strip()}", flush=True)
        run(["git", "rebase", "--abort"])
        run(["git", "pull", "--rebase", "origin", "main"])
    raise SystemExit("[refresh] push failed after 3 attempts")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--commit", action="store_true", help="commit if changed")
    p.add_argument("--push", action="store_true", help="commit + push if changed (implies --commit)")
    args = p.parse_args()
    if args.push:
        args.commit = True
    return args


def main() -> int:
    args = parse_args()
    try:
        rebuild_snapshot()
    except SystemExit:
        raise
    except Exception as e:
        print(f"[refresh] rebuild failed: {type(e).__name__}: {e}", flush=True)
        return 1

    if args.commit:
        try:
            commit_and_push()
        except SystemExit as e:
            print(str(e), flush=True)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
