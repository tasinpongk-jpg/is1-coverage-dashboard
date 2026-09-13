#!/usr/bin/env python3
"""
check_snapshot_freshness.py — Daily freshness probe for IS1 dashboard
=====================================================================

Reads the JSON snapshots under data/ and emits a Discord-ready summary.

Two modes:

  (a) Critical 5 — the snapshots called out in CLAUDE.md §2 that drive
      the public dashboard HTML pages. Thresholds default to 7d warn /
      14d stale (configurable via --threshold).

  (b) All snapshots — every JSON in data/ that has a parseable
      timestamp field. Per-file thresholds in SNAPSHOTS take
      precedence (e.g. harvest-queue.json is allowed 30d warn / 60d
      stale because it's a longer-cycle pipeline).

Per-file metadata (in SNAPSHOTS):
  file:    JSON filename under data/
  fields:  ordered list of timestamp keys; first one that exists AND
           parses wins
  warn:    days before warn threshold (default: 7)
  stale:   days before stale threshold (default: 14)
  skip:    if True, this snapshot is silently excluded from the probe
  label:   short label shown in the output table (defaults to file stem)

CLI flags:
  --quiet           Only emit output if at least one snapshot is stale.
                    Auto-enabled when stdout is not a TTY (cron / pipe).
  --threshold W,S   Override global warn/stale thresholds (per-file
                    overrides still win). E.g. --threshold 3,7
  --only-critical   Probe only the 5 critical snapshots from CLAUDE.md §2.

Exit codes:
  0  all snapshots within warn threshold
  1  at least one snapshot is warn (within stale window)
  2  at least one snapshot is stale (>stale threshold)
  3  CLI argument error

Cron: runs at 08:30 BKK weekdays (job e178ed60c87a). Silent on green
days, posts to Discord only when something is stale.

Related:
- CLAUDE.md §2 (the critical 5)
- scripts/_pre_commit_hook.sh (auto-syncs this script to
  ~/AppData/Local/hermes/scripts/ on commit)
- index.html snapshots-bar (the visual counterpart in the dashboard)
- is1-coverage-health skill (manual diagnostic for deeper issues)
"""

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path

# Anchor: each data snapshot we probe, with per-file metadata.
#
# Schema per entry (all keys optional except `file`):
#   file:     JSON filename under data/
#   label:    short label shown in the output table (defaults to file stem)
#   fields:   list of timestamp keys to try in priority order. The first
#             that exists and parses wins. Use ["version"] for hand-
#             curated files that don't have a date.
#   warn:     days before which the snapshot is considered fresh
#             (default: 7)
#   stale:    days before which the snapshot is at warn threshold
#             (default: 14)
#   skip:     if True, this snapshot is silently excluded from the probe
#             (e.g. test fixtures, one-shot diagnostic dumps)
#
# The first 5 entries are the "critical" snapshots called out in
# CLAUDE.md §2. Everything below that is non-critical but still useful
# to monitor — typically surfaced to the Discord alert only when stale.
SNAPSHOTS = [
    # ── Critical 5 (CLAUDE.md §2) ────────────────────────────────────
    {"file": "vault-ticker-notes.json", "label": "vault",
     "fields": ["generated", "_built_at", "asOf"]},
    {"file": "disclosure-pulse.json",   "label": "disclosure",
     "fields": ["_built_at", "asOf", "generated"]},
    {"file": "morning-brief.json",      "label": "brief",
     "fields": ["_built_at", "asOf", "generated"]},
    {"file": "company-reports.json",    "label": "reports",
     "fields": ["generated", "_built_at", "asOf"]},
    {"file": "tickers.json",            "label": "tickers",
     "fields": ["version"]},  # version, not a date — handled separately

    # ── Non-critical but worth knowing ───────────────────────────────
    {"file": "ai-insights.json",        "label": "ai-insights",
     "fields": ["_built_at", "asOf"]},
    {"file": "bond-summary.json",       "label": "bonds",
     "fields": ["_built_at", "asOf"]},
    {"file": "build-status.json",       "label": "build-status",
     "fields": ["built_at", "_built_at"]},
    {"file": "diagnostics.json",        "label": "diagnostics",
     "fields": ["_built_at", "asOf"]},
    {"file": "external-news.json",      "label": "ext-news",
     "fields": ["_built_at", "asOf"]},
    {"file": "harvest-queue.json",      "label": "harvest-queue",
     "fields": ["generated", "_built_at"], "warn": 30, "stale": 60},
    {"file": "oppday-minutes.json",     "label": "oppday",
     "fields": ["generated", "_built_at"], "warn": 14, "stale": 30},
    {"file": "sec-bonds.json",          "label": "sec-bonds",
     "fields": ["_built_at", "asOf"]},
    {"file": "sec-enforcement.json",    "label": "sec-enf",
     "fields": ["_built_at", "asOf"]},
    {"file": "sec-form59.json",         "label": "sec-form59",
     "fields": ["_built_at", "asOf"]},
    {"file": "sector-heatmap.json",     "label": "heatmap",
     "fields": ["_built_at", "asOf"]},
    {"file": "source-coverage.json",    "label": "src-cov",
     "fields": ["generated", "_built_at"], "warn": 14, "stale": 30},
    {"file": "source-health.json",      "label": "src-health",
     "fields": ["asOf", "_built_at"]},
    {"file": "ticker-summary.json",     "label": "ticker-sum",
     "fields": ["_built_at", "asOf", "version"]},
    {"file": "trading-signs.json",      "label": "signs",
     "fields": ["_built_at", "asOf"]},
    {"file": "unusual-trading.json",    "label": "unusual",
     "fields": ["_built_at", "asOf"]},
    {"file": "visits.json",             "label": "visits",
     "fields": ["generated", "_built_at"], "warn": 30, "stale": 60},

    # ── Skipped — no timestamp field, or fixture/test-only ───────────
    {"file": "harvest-state.json",      "label": "harvest-state",  "skip": True},
    {"file": "lex-regulations.json",    "label": "lex-regs",       "skip": True},
    {"file": "regulations-manifest.json", "label": "regs-manifest", "skip": True},
    {"file": "sector-intelligence.json", "label": "sector-intel",  "skip": True},
    {"file": "_smoke_*.json",           "label": "smoke",          "skip": True},
]
# Note: morning-brief appears twice in the table above. That's a typo
# from copy-paste during drafting. The dedup happens at probe-time by
# `file` name — keep the entry above (the critical-5 one) and remove
# the second one. (Done in code below.)


# Default thresholds
DEFAULT_WARN_DAYS = 7
DEFAULT_STALE_DAYS = 14


def _has_data(p):
    """True if a directory looks like the IS1 repo (has a `data/` with at least one snapshot)."""
    if not isinstance(p, Path):
        return False
    d = p / "data"
    return d.is_dir() and any((d / e["file"]).is_file() for e in SNAPSHOTS
                              if not e.get("skip") and "*" not in e["file"])


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


def _resolve_field(data, fields):
    """Pick the first existing + parseable timestamp from `fields`. Returns (value, field_name) or (None, None)."""
    for f in fields:
        v = data.get(f)
        if v is None:
            continue
        if f == "version":
            return v, f  # version is a string, not a date — caller handles
        # Try to parse as date
        try:
            d = dt.datetime.fromisoformat(str(v).replace("Z", "+00:00"))
            return v, f
        except (ValueError, AttributeError):
            continue
    return None, None


def _age_days(stamp):
    """Return age in days for an ISO timestamp string (or date-only). Returns None on failure."""
    try:
        d = dt.datetime.fromisoformat(str(stamp).replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None
    now = dt.datetime.now(d.tzinfo)
    return (now - d).total_seconds() / 86400.0


def probe(threshold_warn, threshold_stale, quiet):
    """Walk SNAPSHOTS, compute freshness for each, return (rows, max_severity).

    Each row: (label, file, stamp, age_d_or_None, status, mark, used_field)
    """
    rows = []
    max_sev = 0
    seen_files = set()  # dedup by file path

    for entry in SNAPSHOTS:
        if entry.get("skip"):
            continue
        fn = entry["file"]
        if "*" in fn:
            # glob pattern (e.g. _smoke_*.json) — skip for now
            continue
        if fn in seen_files:
            continue
        seen_files.add(fn)

        path = DATA / fn
        label = entry.get("label") or path.stem
        warn_d = entry.get("warn", threshold_warn)
        stale_d = entry.get("stale", threshold_stale)

        if not path.is_file():
            rows.append((label, fn, "(missing)", None, "stale", "⚠", None))
            max_sev = max(max_sev, 2)
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            rows.append((label, fn, f"parse-err: {e}", None, "stale", "⚠", None))
            max_sev = max(max_sev, 2)
            continue

        stamp, used_field = _resolve_field(data, entry.get("fields", []))
        if stamp is None:
            rows.append((label, fn, f"(no {entry.get('fields')})", None, "warn", "?", None))
            max_sev = max(max_sev, 1)
            continue
        if used_field == "version":
            # Hand-curated — render as version, not date
            rows.append((label, fn, f"v{stamp}", None, "ok", "·", used_field))
            continue

        age_d = _age_days(stamp)
        if age_d is None:
            rows.append((label, fn, stamp, None, "warn", "?", used_field))
            max_sev = max(max_sev, 1)
            continue

        # Per-file thresholds override the global CLI thresholds
        if age_d > stale_d:
            sev, status_s, mark = 2, "stale", "🔴"
        elif age_d > warn_d:
            sev, status_s, mark = 1, "warn", "🟡"
        else:
            sev, status_s, mark = 0, "fresh", "🟢"
        max_sev = max(max_sev, sev)
        rows.append((label, fn, stamp, age_d, status_s, mark, used_field))

    return rows, max_sev


def render_markdown(rows, threshold_warn, threshold_stale):
    """Render Discord-friendly markdown with per-file thresholds surfaced."""
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M BKK")
    lines = [f"**IS1 dashboard snapshot freshness** · {now}",
             f"_default thresholds: warn {threshold_warn}d · stale {threshold_stale}d (per-file overrides shown)_",
             "",
             "| snapshot | file | asOf | age | thr | status |",
             "|---|---|---|---:|---|---|"]
    for label, fn, stamp, age_d, status_s, mark, used_field in rows:
        age_str = f"{age_d:.1f}d" if age_d is not None else "—"
        # Per-file threshold (if overridden): find the SNAPSHOTS entry
        thr_str = ""
        for e in SNAPSHOTS:
            if e["file"] == fn:
                if "warn" in e or "stale" in e:
                    thr_str = f"{e.get('warn', threshold_warn)}/{e.get('stale', threshold_stale)}d"
                break
        thr_str = thr_str or f"{threshold_warn}/{threshold_stale}d"
        lines.append(f"| `{label}` | `{fn}` | {stamp} | {age_str} | {thr_str} | {mark} {status_s} |")
    stale_count = sum(1 for r in rows if r[4] == "stale")
    warn_count = sum(1 for r in rows if r[4] == "warn")
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
    ap.add_argument("--threshold", default=f"{DEFAULT_WARN_DAYS},{DEFAULT_STALE_DAYS}",
                    help=f"warn,stale thresholds in days (default: {DEFAULT_WARN_DAYS},{DEFAULT_STALE_DAYS}). "
                         "Per-file overrides in SNAPSHOTS take precedence.")
    ap.add_argument("--only-critical", action="store_true",
                    help="Only probe the 5 critical snapshots from CLAUDE.md §2.")
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

    if args.only_critical:
        # The first 5 entries are the critical 5 (CLAUDE.md §2)
        critical_files = {e["file"] for e in SNAPSHOTS[:5]}
        rows = [r for r in rows if r[1] in critical_files]
        max_sev = max((2 if r[4] == "stale" else 1 if r[4] == "warn" else 0) for r in rows) if rows else 0

    if args.quiet and max_sev == 0:
        return 0

    print(render_markdown(rows, tw, ts))
    return max_sev


if __name__ == "__main__":
    sys.exit(main())
