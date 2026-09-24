"""Wrapper for Hermes cron invocation.

The Hermes cron `--no-agent --script` mode runs the script without
arguments. This wrapper invokes `enrich_filing.py --auto-alert` with
the right args. Output is the same as the script's stdout.

Why a wrapper instead of changing the script signature? Because
`enrich_filing.py` is also callable as `python enrich_filing.py
--ticker TU` for ad-hoc use, and we want both modes to work.

Exit code: propagates the script's exit code.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "enrich_filing.py"


def main() -> int:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--auto-alert"],
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


if __name__ == "__main__":
    sys.exit(main())