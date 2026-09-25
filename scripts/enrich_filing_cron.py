"""Wrapper for Hermes cron invocation.

The Hermes cron `--no-agent --script` mode runs the script without
arguments. This wrapper invokes `enrich_filing.py --auto-alert` (Discord,
RM C Critical) and then `--dashboard` (IS1-wide Critical + Material ->
data/filing-summaries.json). With IS1_FILING_SUMMARY_PUSH=1 it also
commits and pushes that file so the dashboard picks it up.

Why a wrapper instead of changing the script signature? Because
`enrich_filing.py` is also callable as `python enrich_filing.py
--ticker TU` for ad-hoc use, and we want both modes to work.

Exit code: propagates the script's exit code.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "enrich_filing.py"


def _run(args: list[str]) -> int:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    # Print stdout (Hermes will deliver this to the cron channel;
    # silent for happy path because --auto-alert only prints when
    # there's work to do or when something errors).
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    return proc.returncode


def _push_summaries() -> None:
    """Commit data/filing-summaries.json when it changed (opt-in).

    Set IS1_FILING_SUMMARY_PUSH=1 on the laptop to publish each run; the
    dashboard only sees summaries that reach main. Rebase first so the
    daily CI data commit never blocks the push.
    """
    target = "data/filing-summaries.json"
    git = ["git", "-C", str(REPO)]
    # Only publish from main. On any other branch, "push HEAD:main" would carry
    # that branch's unreviewed commits into main with the data file.
    branch = subprocess.run(git + ["rev-parse", "--abbrev-ref", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    if branch != "main":
        print(f"[enrich_filing_cron] not pushing: repo is on '{branch}', not main",
              file=sys.stderr)
        return
    if not subprocess.run(git + ["status", "--porcelain", "--", target],
                          capture_output=True, text=True).stdout.strip():
        return
    steps = [
        git + ["add", "--", target],
        git + ["commit", "-m", "chore(data): refresh filing summaries", "--", target],
        git + ["pull", "--rebase", "--autostash", "origin", "main"],
        git + ["push", "origin", "HEAD:main"],
    ]
    for step in steps:
        proc = subprocess.run(step, capture_output=True, text=True)
        if proc.returncode != 0:
            print(f"[enrich_filing_cron] {' '.join(step[3:5])} failed: {proc.stderr.strip()[:300]}",
                  file=sys.stderr)
            return


def main() -> int:
    code = _run(["--auto-alert"])
    # IS1-wide Critical + Material summaries for the dashboard. Runs even
    # when the Discord alert failed; the two outputs are independent.
    dash = _run(["--dashboard"])
    if dash == 0 and os.environ.get("IS1_FILING_SUMMARY_PUSH") == "1":
        _push_summaries()
    return code or dash


if __name__ == "__main__":
    sys.exit(main())