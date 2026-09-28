"""Daily laptop job: rebuild data/vault-ticker-notes.json and push it to main.

The vault snapshot has no CI path (the OneDrive vault only exists on the
laptop), so it goes stale whenever nobody remembers to run the builder. This
wrapper is meant for a daily Hermes cron:

    python scripts/vault_notes_cron.py            # rebuild, commit, push
    python scripts/vault_notes_cron.py --dry-run  # rebuild, show the diff, restore

It works from the repo or from a copy in %LOCALAPPDATA%\\hermes\\scripts\\: the
repo is IS1_REPO if set, else this file's repo, else the laptop default.

Exit codes: 0 done (or nothing changed), 1 build or git step failed,
2 vault not found (the JSON is left untouched, so the page stays stale; fix
VAULT_ROOT or the OneDrive sync).
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

DEFAULT_REPO = Path(r"C:\Users\Tasinpong\projects\is1-coverage-dashboard")
TARGET = "data/vault-ticker-notes.json"
TAG = "[vault_notes_cron]"


def repo_root() -> Path:
    env = os.environ.get("IS1_REPO")
    if env:
        return Path(env)
    here = Path(__file__).resolve().parent.parent
    if (here / "scripts" / "build_vault_ticker_notes.py").is_file():
        return here
    return DEFAULT_REPO


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def publish(repo: Path) -> int:
    """Commit and push TARGET if it changed. Only from main."""
    branch = _git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if branch != "main":
        print(f"{TAG} not pushing: repo is on '{branch}', not main", file=sys.stderr)
        return 1
    if not _git(repo, "status", "--porcelain", "--", TARGET).stdout.strip():
        print(f"{TAG} no change")
        return 0
    steps = [
        ("add", "--", TARGET),
        ("commit", "-m", "chore(data): rebuild vault ticker notes", "--", TARGET),
        ("pull", "--rebase", "--autostash", "origin", "main"),
        ("push", "origin", "HEAD:main"),
    ]
    for step in steps:
        proc = _git(repo, *step)
        if proc.returncode != 0:
            print(f"{TAG} git {step[0]} failed: {proc.stderr.strip()[:300]}", file=sys.stderr)
            return 1
    print(f"{TAG} pushed {TARGET}")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    dry = "--dry-run" in argv
    repo = repo_root()
    builder = repo / "scripts" / "build_vault_ticker_notes.py"
    if not builder.is_file():
        print(f"{TAG} builder not found: {builder}", file=sys.stderr)
        return 1
    proc = subprocess.run([sys.executable, str(builder)], cwd=repo, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    print(out, end="")
    if proc.returncode != 0:
        print(f"{TAG} build failed (exit {proc.returncode})", file=sys.stderr)
        return 1
    if "vault not found" in out:
        print(f"{TAG} vault not found; snapshot not rebuilt", file=sys.stderr)
        return 2
    if dry:
        print(_git(repo, "diff", "--stat", "--", TARGET).stdout, end="")
        _git(repo, "checkout", "--", TARGET)
        print(f"{TAG} dry run: change shown above, file restored")
        return 0
    return publish(repo)


if __name__ == "__main__":
    sys.exit(main())
