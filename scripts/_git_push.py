#!/usr/bin/env python
"""Shared commit-and-push utility for local data-refresh scripts.

Centralizes the four things every data-refresh script was doing by hand:

  1. `git add <paths>`
  2. `git commit -m <message>`
  3. **optional delay** (so a human can pull + inspect before push)
  4. `git pull --rebase origin main` then `git push origin main`,
     with one round of conflict recovery.

Replaces the inline `git commit && git push` blocks in
`scripts/refresh_vault_notes.py` and `scripts/build_oppday_minutes.py`,
and is the right place for any future local script that wants to ship
a snapshot to GitHub.

CLI:
  python scripts/_git_push.py --paths data/X.json --message "chore: refresh X"

Env vars (all optional):
  PUSH_DELAY_SEC       Seconds to wait between commit and push. Default 0.
                       Set to e.g. 300 to get a 5-minute inspection window.
                       The script logs a countdown every 30s and exits
                       non-zero if the abort file appears.
  PUSH_ABORT_FILE      Path to a sentinel file. If it exists at push time,
                       the push is skipped (exit 0). Lets a human cancel
                       with `touch <path>` during the delay window.
  PUSH_REMOTE          Override `origin`. Default: origin.
  PUSH_BRANCH          Override `main`. Default: main.
  PUSH_NO_REBASE       If set (any value), skip the rebase step. Useful
                       when you know the remote hasn't moved.

Behavior notes:
  - The script runs from REPO (the parent of `scripts/`) so paths can be
    repo-relative or absolute.
  - All subprocess calls use `text=True` and capture stderr.
  - A push that hits a non-fast-forward is retried once after a rebase.
  - Exit codes: 0 = success (pushed OR nothing to push OR aborted cleanly),
    1 = git error, 2 = user abort via PUSH_ABORT_FILE, 3 = push failed
    after retry.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

DEFAULT_DELAY_SEC = int(os.environ.get("PUSH_DELAY_SEC", "0"))
ABORT_FILE = os.environ.get("PUSH_ABORT_FILE", "").strip()
REMOTE = os.environ.get("PUSH_REMOTE", "origin")
BRANCH = os.environ.get("PUSH_BRANCH", "main")
NO_REBASE = bool(os.environ.get("PUSH_NO_REBASE"))


def _log(msg: str) -> None:
    print(f"[git_push] {msg}", flush=True)


def _run(args: list[str], *, check: bool = True, cwd: Path = REPO) -> subprocess.CompletedProcess:
    """Run a git command from REPO. Capture stdout+stderr as text."""
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=check,
    )


def _has_changes(paths: list[Path]) -> bool:
    """True if any of `paths` differs from HEAD (staged, unstaged, or untracked)."""
    rels = [str(p.relative_to(REPO)) if p.is_absolute() else str(p) for p in paths]
    # unstaged
    diff = _run(["diff", "--stat", "--", *rels], check=False)
    if diff.stdout.strip():
        return True
    # staged
    diff_cached = _run(["diff", "--cached", "--stat", "--", *rels], check=False)
    if diff_cached.stdout.strip():
        return True
    # untracked / new files — `git diff` won't show these. Check porcelain
    # status and grep for each path. We don't trust `git status -uall`
    # output wholesale because of color codes; instead, iterate paths.
    status = _run(["status", "--porcelain", "--untracked-files=all", "--", *rels], check=False)
    for line in status.stdout.splitlines():
        # XY path  where X is index status, Y is worktree status. Untracked
        # files show up as `?? <path>`.
        if line.startswith("?? "):
            return True
        # Any non-empty X or Y means there's a diff.
        xy = line[:2]
        if xy.strip():  # ' M', 'M ', 'MM', 'A ', etc.
            return True
    return False


def _maybe_abort(stage: str) -> bool:
    """Returns True if the user has set the abort file."""
    if not ABORT_FILE:
        return False
    if Path(ABORT_FILE).exists():
        _log(f"ABORT: {ABORT_FILE} exists — skipping {stage}")
        try:
            Path(ABORT_FILE).unlink()
        except OSError:
            pass
        return True
    return False


def _wait_with_countdown(seconds: int) -> bool:
    """Sleep `seconds`, log every 30s, return True if aborted."""
    if seconds <= 0:
        return False
    _log(f"delay: {seconds}s before push (env PUSH_DELAY_SEC). "
         f"Inspect with `git log -1` and `git diff HEAD~1`. "
         f"Abort with: touch {ABORT_FILE or '<PUSH_ABORT_FILE>'}")
    end = time.monotonic() + seconds
    next_log = time.monotonic() + 30
    while True:
        remaining = int(end - time.monotonic())
        if remaining <= 0:
            break
        if _maybe_abort("push during delay"):
            return True
        if time.monotonic() >= next_log:
            _log(f"  ... {remaining}s remaining")
            next_log = time.monotonic() + 30
        time.sleep(min(5, remaining))
    return False


def _rebase_once() -> bool:
    """Pull --rebase once. Returns True if clean, False if conflict remains."""
    if NO_REBASE:
        _log("PUSH_NO_REBASE set — skipping rebase")
        return True
    _log(f"rebase: pulling {REMOTE}/{BRANCH}")
    res = _run(["fetch", REMOTE, BRANCH], check=False)
    if res.returncode != 0:
        _log(f"WARN: fetch failed: {res.stderr.strip()} — proceeding with push anyway")
        return True
    pull = _run(["pull", "--rebase", REMOTE, BRANCH], check=False)
    if pull.returncode == 0:
        return True
    # Conflict. Default strategy: prefer ours for snapshots (the local
    # rebuild is newer than any prior cron push). If a real human change
    # is on the remote, they should resolve manually — we surface the
    # conflict and bail.
    _log(f"rebase conflict — preferring ours (local rebuild is newer):\n{pull.stderr.strip()}")
    _run(["rebase", "--abort"], check=False)
    merge = _run(["pull", "--no-rebase", REMOTE, BRANCH, "-X", "ours"], check=False)
    if merge.returncode != 0:
        _log(f"rebase recovery failed: {merge.stderr.strip()}")
        return False
    return True


def _do_push() -> bool:
    """Push and return True on success. Caller handles retry."""
    res = _run(["push", REMOTE, BRANCH], check=False)
    if res.returncode == 0:
        return True
    _log(f"push rejected: {res.stderr.strip()}")
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Commit listed paths and push to origin/main with optional delay."
    )
    parser.add_argument(
        "--paths", nargs="+", required=True,
        help="One or more repo-relative paths to add and commit.",
    )
    parser.add_argument("--message", required=True, help="Commit message.")
    parser.add_argument(
        "--delay", type=int, default=DEFAULT_DELAY_SEC,
        help="Override PUSH_DELAY_SEC for this run (seconds).",
    )
    parser.add_argument(
        "--no-rebase", action="store_true",
        help="Skip `git pull --rebase` (use when remote is known empty).",
    )
    args = parser.parse_args(argv)

    paths = [Path(p).resolve() for p in args.paths]
    for p in paths:
        if not p.exists():
            _log(f"FATAL: path does not exist: {p}")
            return 1

    if not _has_changes(paths):
        _log("no diff vs HEAD — skipping commit/push")
        return 0

    rels = [str(p.relative_to(REPO)) for p in paths]
    _log(f"staging: {' '.join(rels)}")
    add = _run(["add", "--", *rels], check=False)
    if add.returncode != 0:
        _log(f"FATAL: git add failed: {add.stderr.strip()}")
        return 1

    _log(f"committing: {args.message}")
    commit = _run(["commit", "-m", args.message], check=False)
    if commit.returncode != 0:
        _log(f"FATAL: git commit failed: {commit.stderr.strip()}")
        return 1

    if _maybe_abort("after commit"):
        return 2

    if _wait_with_countdown(args.delay):
        return 2

    if not _rebase_once():
        _log("FATAL: rebase conflict could not be resolved automatically")
        return 1

    if _do_push():
        _log(f"pushed to {REMOTE}/{BRANCH}")
        return 0

    # One retry after another rebase round — handles the case where the
    # remote moved between fetch and push.
    _log("retrying after another rebase round")
    if _rebase_once() and _do_push():
        _log(f"pushed to {REMOTE}/{BRANCH} on retry")
        return 0

    _log("FATAL: push failed after retry")
    return 3


if __name__ == "__main__":
    sys.exit(main())
