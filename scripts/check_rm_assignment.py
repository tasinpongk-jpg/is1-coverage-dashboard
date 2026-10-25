#!/usr/bin/env python3
"""Fail when the morning brief or a SETSURV digest would go out without RMs.

Check mode only. This script does not import the mail client and does not
send email. It does not need the private nickname map: data/tickers.json
codes are enough.

    python scripts/check_rm_assignment.py
    python scripts/check_rm_assignment.py --brief-only
    python scripts/check_rm_assignment.py --digest-only

Exit 1 when the brief universe has zero tickers, when no RM code has a
ticker, or when a digest of the coverage universe would label any symbol
Unassigned.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_morning_push as brief  # noqa: E402
from rm_privacy import UNASSIGNED, coverage_rm_map, digest_label  # noqa: E402

TICKERS = ROOT / "data" / "tickers.json"


def brief_problems():
    doc = brief._read("tickers") or {"tickers": []}
    universe = [t for t in (doc.get("tickers") or []) if t.get("tk")]
    coverage = brief.rm_coverage()
    problems = []
    if not universe:
        problems.append("brief has zero tickers")
    if not any(coverage.values()):
        problems.append("brief has zero RM slices")
    return problems


def digest_problems():
    """Symbols a digest would label Unassigned, using the CI ticker map."""
    import json

    rm_map = coverage_rm_map(TICKERS)
    if TICKERS.is_file():
        doc = json.loads(TICKERS.read_text(encoding="utf-8"))
    else:
        doc = {"tickers": []}
    problems = []
    for row in doc.get("tickers") or []:
        sym = row.get("tk")
        if not sym:
            continue
        if digest_label(sym, rm_map) == UNASSIGNED:
            problems.append(f"digest would contain RM: Unassigned for {sym}")
    return problems


def main(argv=None):
    p = argparse.ArgumentParser(description="Check RM assignment. Sends nothing.")
    p.add_argument("--brief-only", action="store_true")
    p.add_argument("--digest-only", action="store_true")
    args = p.parse_args(argv)
    problems = []
    if not args.digest_only:
        problems.extend(brief_problems())
    if not args.brief_only:
        problems.extend(digest_problems())
    if problems:
        print(f"RM assignment check failed ({len(problems)}):", file=sys.stderr)
        for item in problems[:50]:
            print(f"  {item}", file=sys.stderr)
        extra = len(problems) - 50
        if extra > 0:
            print(f"  ... {extra} more", file=sys.stderr)
        return 1
    coverage = brief.rm_coverage()
    n_tickers = sum(len(v) for v in coverage.values())
    n_slices = sum(1 for v in coverage.values() if v)
    which = "digest" if args.digest_only else "brief" if args.brief_only else "brief+digest"
    print(f"RM assignment ok ({which}): tickers={n_tickers} rm_slices={n_slices}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
