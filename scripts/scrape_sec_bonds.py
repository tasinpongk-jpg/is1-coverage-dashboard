#!/usr/bin/env python3
"""
scrape_sec_bonds.py — Monthly SEC Open API bond scrape (6 endpoints).

Pulls /v2/bond/{issuers,features,credit-ratings,outstanding-values,
involve-parties,investor-holdings} with paginate_v2(page_size=100),
saves raw JSON snapshots under the SEC-Bonds vault raw/ directory.

Used as the upstream feed for build_sec_bonds.py -> data/sec-bonds.json.
Auto-commits + pushes the vault raw/ snapshots so a separate join step
(not in this script — left for build_sec_bonds.py) can consume them.

Cron: monthly 15th 21:00 BKK (offset from ThaiBMA bond-refresh on the 1st).
Mode: no_agent. Stdout -> Discord.

Behaviour:
  - Loads SEC_API_KEY / SEC_API_KEY_SECONDARY from ~/.hermes/secrets/sec_bonds.env
    if not already in the environment.
  - Skips silently (exit 0, "[SILENT]" stdout) if no key is configured yet.
  - Each endpoint result -> vault raw/<endpoint>_<YYYYMMDD>.json.
  - Commit + push only if at least one snapshot wrote >0 items.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(r"C:/Users/Tasinpong/projects/is1-coverage-dashboard")
SECRETS_FILE = Path.home() / ".hermes" / "secrets" / "sec_bonds.env"

# Vault path for raw bond snapshots — sits next to the per-ticker markdown notes
# that build_sec_bonds.py currently reads.
VAULT_RAW = Path(
    r"C:/Users/Tasinpong/OneDrive - The Stock Exchange of Thailand/Claude-Vault"
    r"/Work-SET/Listed Company/1-Raw/06-Market-Data/SEC-Bonds/raw"
)

ENDPOINTS = [
    ("issuers",            "/v2/bond/issuers"),
    ("features",           "/v2/bond/features"),
    ("credit-ratings",     "/v2/bond/credit-ratings"),
    ("outstanding-values", "/v2/bond/outstanding-values"),
    ("involve-parties",    "/v2/bond/involve-parties"),
    ("investor-holdings",  "/v2/bond/investor-holdings"),
]


def _load_secrets() -> None:
    """Source ~/.hermes/secrets/sec_bonds.env if it exists (no-op if missing)."""
    if not SECRETS_FILE.exists():
        return
    for line in SECRETS_FILE.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, _, v = s.partition("=")
        k, v = k.strip(), v.strip()
        # Skip empty values, but don't overwrite real env vars.
        if v and k not in os.environ:
            os.environ[k] = v


def main(argv: list[str] | None = None) -> int:
    ap_args = argv if argv is not None else sys.argv[1:]
    dry_run = "--dry-run" in ap_args

    _load_secrets()

    # Silent skip if no key — same watchdog pattern as is1-snapshot-freshness.
    if not os.environ.get("SEC_API_KEY"):
        # Empty stdout = cron framework treats as silent (no Discord delivery).
        return 0

    # Lazy import after secrets load (sec_api raises SystemExit if no key).
    os.chdir(REPO)
    sys.path.insert(0, str(REPO / "scripts"))
    try:
        import sec_api as sa
    except Exception as exc:
        print(f"FAIL import sec_api: {exc}", file=sys.stderr)
        return 2

    VAULT_RAW.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d")
    today_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")

    summary_lines: list[str] = []
    total_items = 0
    wrote_files: list[Path] = []

    for label, path in ENDPOINTS:
        try:
            items = list(sa.paginate_v2(path, page_size=100))
            out = VAULT_RAW / f"{label}_{stamp}.json"
            if not dry_run:
                out.write_text(
                    json.dumps(items, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                wrote_files.append(out)
            summary_lines.append(f"  {label:20s} {len(items):5d} items")
            total_items += len(items)
        except Exception as exc:  # noqa: BLE001 — surface and continue
            summary_lines.append(f"  {label:20s} FAIL  {type(exc).__name__}: {str(exc)[:120]}")

    msg = (
        f"📊 **SEC Bonds scrape** ({today_iso})\n"
        f"endpoints: {len(ENDPOINTS)} | total items: {total_items}\n"
        f"vault: `{VAULT_RAW}`\n" + "\n".join(summary_lines)
    )
    print(msg)

    if dry_run or not wrote_files:
        return 0

    # Commit + push so the join step (build_sec_bonds.py future revision)
    # can pick up the snapshots next time it runs. Vault lives outside the
    # repo (OneDrive), so we only commit when build_sec_bonds.py itself
    # wants to consume — for now, this script's job is just to keep the
    # raw snapshots current locally.
    # -> Intentionally NO git commit/push in this layer. The vault raw/
    # directory is on OneDrive, not in the repo. build_sec_bonds.py reads
    # directly from there when run (cron, CI, or manual).
    return 0


if __name__ == "__main__":
    sys.exit(main())
