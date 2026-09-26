"""One-time setup for the IS1 filing-summary cron on the Windows laptop.

Idempotent. Run after cloning, or whenever the cron stops producing commits:
    python scripts/bootstrap_cron.py

1. Installs scripts/cron_shim.py as
   %LOCALAPPDATA%/hermes/scripts/enrich_filing_cron.py (the name the
   is1-filing-alert cron runs).
2. Installs pypdf if it is missing.
3. Reports whether each variable the job needs is set, in the process
   environment or in HKCU\\Environment. Never prints a value.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SHIM_SRC = REPO / "scripts" / "cron_shim.py"
REQUIRED = ("MINIMAX_API_KEY", "IS1_FILING_SUMMARY_PUSH")
WEBHOOK = ("DISCORD_WEBHOOK_URL", "DAILY_BRIEF_WEBHOOK")  # either one


def _registry_names() -> set[str]:
    try:
        import winreg
    except ImportError:
        return set()
    names: set[str] = set()
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            i = 0
            while True:
                try:
                    names.add(winreg.EnumValue(key, i)[0])
                except OSError:
                    break
                i += 1
    except OSError:
        pass
    return names


def main() -> int:
    local = os.environ.get("LOCALAPPDATA")
    if not local:
        print("[bootstrap] LOCALAPPDATA not set; this script is for the Windows laptop")
        return 1
    dst_dir = Path(local) / "hermes" / "scripts"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / "enrich_filing_cron.py"
    shutil.copy2(SHIM_SRC, dst)
    print(f"[bootstrap] shim installed -> {dst}")
    if REPO.resolve() != Path(r"C:\Users\Tasinpong\projects\is1-coverage-dashboard").resolve():
        print(f"[bootstrap] repo is at {REPO}; run: setx IS1_REPO \"{REPO}\"")

    try:
        import pypdf  # noqa: F401
        print("[bootstrap] pypdf: installed")
    except ImportError:
        rc = subprocess.run([sys.executable, "-m", "pip", "install", "pypdf"]).returncode
        print(f"[bootstrap] pypdf: pip install exit {rc}")

    reg = _registry_names()
    def state(name: str) -> str:
        if os.environ.get(name):
            return "set (process)"
        return "set (registry)" if name in reg else "MISSING"
    missing = 0
    for name in REQUIRED:
        s = state(name)
        missing += s == "MISSING"
        print(f"[bootstrap] {name}: {s}")
    hooks = [f"{n}: {state(n)}" for n in WEBHOOK]
    print(f"[bootstrap] webhook (either) -> {'; '.join(hooks)}")
    if all(state(n) == "MISSING" for n in WEBHOOK):
        missing += 1
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
