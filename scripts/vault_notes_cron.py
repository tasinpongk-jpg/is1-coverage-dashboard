"""Daily laptop job: rebuild the vault-backed snapshots and push them to main.

Snapshots: data/vault-ticker-notes.json (required) and data/oppday-minutes.json
(best effort: a failure there is reported but never blocks the vault push).

The vault snapshot has no CI path (the OneDrive vault only exists on the
laptop), so it goes stale whenever nobody remembers to run the builder. This
wrapper is meant for a daily Hermes cron:

    python scripts/vault_notes_cron.py            # rebuild, commit, push
    python scripts/vault_notes_cron.py --dry-run  # rebuild, show the diff, restore

It works from the repo or from a copy in %LOCALAPPDATA%\\hermes\\scripts\\: the
repo is IS1_REPO if set, else this file's repo, else the laptop default.

Exit codes: 0 done (or nothing changed), 1 a build or git step failed
(including the oppday build, after the vault notes were still pushed),
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
OPPDAY = "data/oppday-minutes.json"
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


def publish(repo: Path, targets: list[str]) -> int:
    """Commit and push whichever targets changed, in one commit. Only from main."""
    branch = _git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if branch != "main":
        print(f"{TAG} not pushing: repo is on '{branch}', not main", file=sys.stderr)
        return 1
    changed = [t for t in targets if _git(repo, "status", "--porcelain", "--", t).stdout.strip()]
    if not changed:
        print(f"{TAG} no change")
        return 0
    names = " + ".join(Path(t).stem for t in changed)
    steps = [
        ("add", "--", *changed),
        ("commit", "-m", f"chore(data): rebuild {names}", "--", *changed),
        ("pull", "--rebase", "--autostash", "origin", "main"),
        ("push", "origin", "HEAD:main"),
    ]
    for step in steps:
        proc = _git(repo, *step)
        if proc.returncode != 0:
            print(f"{TAG} git {step[0]} failed: {proc.stderr.strip()[:300]}", file=sys.stderr)
            return 1
    print(f"{TAG} pushed {', '.join(changed)}")
    return 0


def _build(repo: Path, script: str) -> tuple[int, str]:
    builder = repo / "scripts" / script
    if not builder.is_file():
        return 1, f"{TAG} builder not found: {builder}\n"
    proc = subprocess.run([sys.executable, str(builder)], cwd=repo, capture_output=True, text=True)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    dry = "--dry-run" in argv
    repo = repo_root()

    code, out = _build(repo, "build_vault_ticker_notes.py")
    print(out, end="")
    if code != 0:
        print(f"{TAG} vault notes build failed (exit {code})", file=sys.stderr)
        return 1
    if "vault not found" in out:
        print(f"{TAG} vault not found; snapshot not rebuilt", file=sys.stderr)
        return 2
    targets = [TARGET]

    # Opp Day minutes: same vault, rewritten only when a summary changed.
    ocode, oout = _build(repo, "build_oppday_minutes.py")
    print(oout, end="")
    if ocode == 0:
        targets.append(OPPDAY)
    else:
        print(f"{TAG} oppday build failed (exit {ocode}); vault notes still published",
              file=sys.stderr)
        _git(repo, "checkout", "--", OPPDAY)

    if dry:
        print(_git(repo, "diff", "--stat", "--", *targets).stdout, end="")
        _git(repo, "checkout", "--", *targets)
        print(f"{TAG} dry run: change shown above, files restored")
        return 0 if ocode == 0 else 1
    rc = publish(repo, targets)
    return rc or (0 if ocode == 0 else 1)


if __name__ == "__main__":
    sys.exit(main())
