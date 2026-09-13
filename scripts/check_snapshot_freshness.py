#!/usr/bin/env python3
"""
check_snapshot_freshness.py — Daily freshness probe for IS1 dashboard
=====================================================================

Reads the 5 critical data snapshots and emits a Discord-ready summary.
Thresholds:
  - ≤7d   fresh (no output if all are fresh and quiet mode)
  - 7-14d warn (yellow flag in summary)
  - >14d  stale (red flag in summary)

Mode:
  --quiet     Only output if at least one snapshot is stale (>14d).
              Default behaviour is to always output (so daily run gives
              a green dashboard).
  --threshold  Override the warn/stale thresholds in days. Comma-separated,
              e.g. --threshold 7,14 (default).

Exit codes:
  0  all snapshots within warn threshold
  1  at least one snapshot is warn (7-14d)
  2  at least one snapshot is stale (>14d)

Cron-friendly: prints plain markdown on stdout, exits non-zero on alerts
so the user can grep exit code if they want.

Related:
- CLAUDE.md §2 (which JSON drives which HTML)
- is1-coverage-health skill (the manual diagnostic)
- index.html snapshots-bar (the visual counterpart of this script)
"""

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

# Anchor: each critical snapshot. `field` is the timestamp key, `label` is
# the human name, `file` is the JSON path under data/. Keep this list in
# sync with CLAUDE.md §2.
SNAPS = [
    ("vault-ticker-notes", "vault-ticker-notes.json", "generated"),
    ("disclosure-pulse",   "disclosure-pulse.json",   "asOf"),
    ("morning-brief",      "morning-brief.json",      "asOf"),
    ("company-reports",    "company-reports.json",    "generated"),
    ("tickers",            "tickers.json",            "version"),
]


def _has_data(p):
    """True if a directory looks like the IS1 repo (has a `data/` with at least one snapshot)."""
    if not isinstance(p, Path):
        return False
    d = p / "data"
    return d.is_dir() and any((d / fn).is_file() for _, fn, _ in SNAPS)


def _resolve_repo_root():
    """Find the IS1 repo root. Tries multiple candidates; returns the first that looks right.

    Order:
      1. IS1_REPO_ROOT env var (explicit override for CI / cron / test)
      2. __file__-relative: parent/scripts/.. if `data/` exists there
      3. __file__ parent/.. if `data/` exists there (handles /scripts/ subdir)
      4. Common laptop path: ~/projects/is1-coverage-dashboard
      5. CWD: parent/.. / parent/.. / parent/.. (walk up looking for data/)

    The point is to be robust whether this file lives at:
      - the repo's scripts/ dir (development)
      - ~/.hermes/scripts/ as a copy (cron deploy — MSYS symlink on Windows
        becomes a file copy, so os.path.realpath doesn't follow it)
      - anywhere else the cron scheduler picks
    """
    # 1. Env var
    env = os.environ.get("IS1_REPO_ROOT")
    if env:
        p = Path(env)
        if _has_data(p):
            return p

    # 2 & 3. __file__-relative candidates
    if "__file__" in globals():
        here = Path(__file__).resolve().parent
        for ancestor in (here.parent, here.parent.parent):
            if _has_data(ancestor):
                return ancestor

    # 4. Laptop common path
    common = Path.home() / "projects" / "is1-coverage-dashboard"
    if _has_data(common):
        return common

    # 5. Walk up from CWD
    cwd = Path.cwd().resolve()
    for ancestor in [cwd, *cwd.parents]:
        if _has_data(ancestor):
            return ancestor

    # Nothing matched — return the env var (or common) so the caller gets
    # a useful error message rather than a silent None.
    return Path(env) if env else common


REPO_ROOT = _resolve_repo_root()
DATA = REPO_ROOT / "data"


def parse_age(stamp, field):
    """Return (age_days, parsed_datetime_or_None). version field returns (None, None)."""
    if field == "version":
        return None, None
    try:
        d = dt.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None, None
    now = dt.datetime.now(d.tzinfo)
    return (now - d).total_seconds() / 86400.0, d


def probe(threshold_warn, threshold_stale, quiet):
    """Return (rows, max_severity) where max_severity is 0/1/2."""
    rows = []
    max_sev = 0
    for key, fn, field in SNAPS:
        path = DATA / fn
        if not path.is_file():
            rows.append((key, "(missing)", None, "stale", "⚠"))
            max_sev = max(max_sev, 2)
            continue
        try:
            d = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            rows.append((key, f"parse-err: {e}", None, "stale", "⚠"))
            max_sev = max(max_sev, 2)
            continue
        stamp = d.get(field)
        if not stamp:
            rows.append((key, f"(no {field})", None, "warn", "?"))
            max_sev = max(max_sev, 1)
            continue
        if field == "version":
            rows.append((key, f"v{stamp}", None, "ok", "·"))
            continue
        age_d, parsed = parse_age(stamp, field)
        if age_d is None:
            rows.append((key, stamp, None, "warn", "?"))
            max_sev = max(max_sev, 1)
            continue
        if age_d > threshold_stale:
            sev, label, mark = 2, "stale", "🔴"
        elif age_d > threshold_warn:
            sev, label, mark = 1, "warn", "🟡"
        else:
            sev, label, mark = 0, "fresh", "🟢"
        max_sev = max(max_sev, sev)
        rows.append((key, stamp, age_d, label, mark))

    if quiet and max_sev == 0:
        return rows, max_sev

    return rows, max_sev


def render_markdown(rows, threshold_warn, threshold_stale):
    """Render Discord-friendly markdown."""
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M BKK")
    lines = [f"**IS1 dashboard snapshot freshness** · {now}",
             f"_thresholds: warn {threshold_warn}d · stale {threshold_stale}d_",
             "",
             "| snapshot | asOf | age | status |",
             "|---|---|---:|---|"]
    for key, stamp, age_d, label, mark in rows:
        age_str = f"{age_d:.1f}d" if age_d is not None else "—"
        lines.append(f"| `{key}` | {stamp} | {age_str} | {mark} {label} |")
    stale_count = sum(1 for r in rows if r[3] == "stale")
    warn_count = sum(1 for r in rows if r[3] == "warn")
    if stale_count:
        lines.append("")
        lines.append(f"⚠️ **{stale_count} stale** — rebuild via `python scripts/build_<name>.py`")
    elif warn_count:
        lines.append("")
        lines.append(f"🟡 {warn_count} approaching stale")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--quiet", action="store_true",
                    help="Only emit output if at least one snapshot is stale.")
    ap.add_argument("--threshold", default="7,14",
                    help="warn,stale thresholds in days (default: 7,14)")
    args = ap.parse_args()

    # Default to quiet when stdout is not a TTY (cron / pipe). On a TTY
    # (manual run) we want to always see the freshness table.
    if not args.quiet and not sys.stdout.isatty():
        args.quiet = True

    try:
        tw, ts = (int(x) for x in args.threshold.split(","))
    except ValueError:
        print("Invalid --threshold; expected 'warn,stale' days", file=sys.stderr)
        return 3

    rows, max_sev = probe(tw, ts, args.quiet)

    if args.quiet and max_sev == 0:
        return 0

    print(render_markdown(rows, tw, ts))
    return max_sev


if __name__ == "__main__":
    sys.exit(main())
