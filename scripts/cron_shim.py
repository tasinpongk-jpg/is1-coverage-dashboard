"""Hermes cron entry point for the IS1 filing-summary job (Windows laptop).

Installed as ~/AppData/Local/hermes/scripts/enrich_filing_cron.py by
scripts/bootstrap_cron.py. The Hermes scheduler resolves bare script names
against that AppData folder, and enrich_filing_cron.py finds the repo from its
own file location, so a plain AppData copy of the wrapper looks for the repo in
the wrong place. This shim runs the repo's wrapper instead, so editing the repo
is enough to change what the cron does.

`setx` writes to HKCU\\Environment but running processes (the Hermes
scheduler, and so every cron worker it spawns) keep their old environment.
The shim copies the few variables the job needs from the registry when they
are missing from the process. Values are never printed.

Repo path: IS1_REPO env var if set, else the default below.
"""
import os
import runpy
import sys
from pathlib import Path

DEFAULT_REPO = r"C:\Users\Tasinpong\projects\is1-coverage-dashboard"
NEEDED = ("MINIMAX_API_KEY", "DISCORD_WEBHOOK_URL", "DAILY_BRIEF_WEBHOOK",
          "IS1_FILING_SUMMARY_PUSH", "IS1_REPO")


def _load_user_env() -> None:
    try:
        import winreg
    except ImportError:
        return  # not Windows
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
            for name in NEEDED:
                if os.environ.get(name):
                    continue
                try:
                    value, _ = winreg.QueryValueEx(key, name)
                except OSError:
                    continue
                if value:
                    os.environ[name] = str(value)
    except OSError:
        pass


def main() -> None:
    _load_user_env()
    wrapper = Path(os.environ.get("IS1_REPO") or DEFAULT_REPO) / "scripts" / "enrich_filing_cron.py"
    if not wrapper.is_file():
        sys.exit(f"[cron_shim] repo wrapper not found: {wrapper}")
    sys.argv = [str(wrapper), *sys.argv[1:]]
    runpy.run_path(str(wrapper), run_name="__main__")


if __name__ == "__main__":
    main()
