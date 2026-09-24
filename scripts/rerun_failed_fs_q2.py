"""Force re-extract of FS Q2/2026 filings whose markdown didn't reach FS-NOTES/.

After the migration, 7 tickers still lack FS-NOTES/Q2 markdown because their
state.completed entry was written by the buggy run (claimed success without
actually placing files in FS-NOTES/).

This script clears the state for those 7 news_ids, then runs process_one on
each (which will download again, re-extract, and write via the now-fixed
vault_raw_writer.project_one that groups by subdir).

Usage:
  python scripts/rerun_failed_fs_q2.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "surveillance"))

from client import SetNewsClient  # noqa: E402

import harvest_download as hd  # noqa: E402

DATA_DIR = REPO / "data"
QUEUE_FILE = DATA_DIR / "harvest-queue.json"
STATE_FILE = DATA_DIR / "harvest-state.json"
VAULT = Path(
    "C:/Users/Tasinpong/OneDrive - The Stock Exchange of Thailand"
    "/Claude-Vault/Work-SET/Listed Company"
)
FS_NOTES = VAULT / "1-Raw" / "01-Filings" / "FS-NOTES"


def main() -> int:
    q = json.load(open(QUEUE_FILE))
    s = json.load(open(STATE_FILE))
    completed = s.setdefault("completed", {})

    # Find FS Q2/2026 items whose ticker has NO Q2 markdown in FS-NOTES/
    targets: list[tuple[str, dict]] = []
    for nid, item in q["items"].items():
        if item.get("kind") != "FS" or item.get("period") != "2026Q2":
            continue
        tk = item["ticker"]
        d = FS_NOTES / tk
        has_q2 = d.is_dir() and any(d.glob(f"*{tk}_2026Q2*.md"))
        if not has_q2:
            targets.append((nid, item))

    print(f"Targets needing re-extract: {len(targets)}")
    for nid, item in targets:
        print(f"  {item['ticker']:8} {nid} {item.get('datetime','')[:16]}")

    if not targets:
        return 0

    # Clear stale state entries
    cleared = 0
    for nid, _ in targets:
        if nid in completed:
            del completed[nid]
            cleared += 1
    print(f"\nCleared {cleared} stale state entries")

    # Persist state BEFORE running (so a Ctrl-C doesn't re-leak stale state)
    hd.save_state(s)

    # Run process_one for each target with fresh state
    print("\n--- Re-extracting ---")
    successes = 0
    failures = []
    with SetNewsClient() as client:
        for nid, item in targets:
            # Reload state each iteration so dedup uses the cleared state.
            state = hd.load_state()
            try:
                status = hd.process_one(client, item, state)
            except Exception as exc:  # noqa: BLE001
                status = f"failed:exception:{type(exc).__name__}:{exc}"
            if status in ("done", "skipped:sha_match"):
                successes += 1
                print(f"  {item['ticker']:8} {nid} -> {status}")
            else:
                failures.append((item['ticker'], nid, status))
                print(f"  {item['ticker']:8} {nid} -> {status}")

    print(f"\n{successes}/{len(targets)} succeeded")
    if failures:
        print("Failures:")
        for tk, nid, status in failures:
            print(f"  {tk} {nid}: {status}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())