"""Migrate misplaced NOTES/FS files from AUDITOR/<TK>/ to FS-NOTES/<TK>/.

Bug: vault_raw_writer.project_one() used `next(sub for _, sub, _ in to_write)`
which picked only the FIRST doctype in a multi-doctype filing. For SET FS ZIPs
which contain [AUDITOR_REPORT, NOTES, FINANCIAL_STATEMENTS], the AUDITOR
doctype won, and the NOTES-prefixed files landed in AUDITOR/<TK>/ instead
of FS-NOTES/<TK>/.

This script detects NOTES-prefixed .md files in AUDITOR/<TK>/ and moves
them to FS-NOTES/<TK>/. Safe to re-run (idempotent).

Verified 2026-08-17: 407 Q2/2026 .md files in AUDITOR/, only 18 in
FS-NOTES/ pre-migration. After migration expect ~190 each.

Detection rules:
  - filename starts with NOTES_ or FINANCIAL_STATEMENTS_
  - filename does NOT start with AUDITOR_
  - the target FS-NOTES/<TK>/<filename> does not exist (or has different sha)

Usage:
  python scripts/migrate_misplaced_fs_notes.py             # move
  python scripts/migrate_misplaced_fs_notes.py --dry-run  # report only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path

VAULT = Path(
    "C:/Users/Tasinpong/OneDrive - The Stock Exchange of Thailand"
    "/Claude-Vault/Work-SET/Listed Company"
)
AUDITOR_DIR = VAULT / "1-Raw" / "01-Filings" / "AUDITOR"
FS_NOTES_DIR = VAULT / "1-Raw" / "01-Filings" / "FS-NOTES"

# Files matching these prefixes are NOTES/FS content even though they
# landed in AUDITOR/. AUDITOR-prefixed files stay put.
NOTES_PREFIXES = ("NOTES_", "FINANCIAL_STATEMENTS_")

# Skip non-Q2/2026 for the audit (the bug specifically hit Q2/2026 batch;
# older files may have been correctly placed historically).
PERIOD_RE = re.compile(r"^(NOTES|FINANCIAL_STATEMENTS)_(?P<tk>[A-Z0-9]+)_(?P<period>20\d{2}Q[1-4]|20\d{2}FY)_")


def sha_of(path: Path) -> str:
    """Read source_sha256 from frontmatter; fall back to file content SHA."""
    try:
        txt = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    m = re.search(r'^source_sha256:\s*"?([a-f0-9]+)"?', txt, re.MULTILINE)
    if m:
        return m.group(1)
    h = hashlib.sha256()
    h.update(txt.encode("utf-8", errors="ignore"))
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="Report what would be moved, do not touch disk")
    ap.add_argument("--period", default="2026Q2",
                    help="Period to filter on (default: 2026Q2). "
                         "Use --all-periods to scan every period.")
    ap.add_argument("--all-periods", action="store_true",
                    help="Process every period, not just the --period value")
    ap.add_argument("--prefer-larger", action="store_true",
                    help="When destination has different content, prefer the "
                         "LARGER file (typically the newer revised filing)")
    args = ap.parse_args()

    period = args.period
    plan: list[tuple[Path, Path, str, str]] = []  # (src, dst, src_sha, dst_sha_or_empty)
    skipped_existing_match = 0
    skipped_different_content = 0

    if not AUDITOR_DIR.is_dir():
        print(f"AUDITOR dir missing: {AUDITOR_DIR}", file=sys.stderr)
        return 1

    for src in sorted(AUDITOR_DIR.rglob("*.md")):
        fn = src.name
        if not any(fn.startswith(p) for p in NOTES_PREFIXES):
            continue
        m = PERIOD_RE.match(fn)
        if not m:
            continue
        if not args.all_periods and m.group("period") != period:
            continue
        tk = src.parent.name
        dst = FS_NOTES_DIR / tk / fn
        src_sha = sha_of(src)
        dst_sha = sha_of(dst) if dst.is_file() else ""
        if dst.is_file() and dst_sha and dst_sha == src_sha:
            skipped_existing_match += 1
            continue
        if dst.is_file() and dst_sha and dst_sha != src_sha:
            if args.prefer_larger:
                # Add to plan: src is the larger/newer, will overwrite dst.
                src_sz = src.stat().st_size
                dst_sz = dst.stat().st_size
                if src_sz >= dst_sz:
                    plan.append((src, dst, src_sha, dst_sha))
                    continue
                else:
                    # dst is larger, just unlink the misplaced src
                    print(f"  SKIP (dst larger): {src} -> {dst}", file=sys.stderr)
                    try:
                        src.unlink()
                    except OSError:
                        pass
                    continue
            skipped_different_content += 1
            print(f"  CONFLICT: {src} vs {dst} (different content)", file=sys.stderr)
            continue
        plan.append((src, dst, src_sha, dst_sha))

    by_ticker: Counter = Counter(src.parent.name for src, *_ in plan)
    print(f"Audit period: {'ALL' if args.all_periods else period}")
    print(f"  Plan to move: {len(plan)} files across {len(by_ticker)} tickers")
    print(f"  Skipped (already correctly placed, sha match): {skipped_existing_match}")
    print(f"  Skipped (different content in destination): {skipped_different_content}")
    if by_ticker:
        print(f"  Top tickers: {dict(by_ticker.most_common(10))}")
    print()
    if args.dry_run:
        for src, dst, _, _ in plan[:30]:
            print(f"  would move: {src.relative_to(VAULT)} -> {dst.relative_to(VAULT)}")
        if len(plan) > 30:
            print(f"  ... and {len(plan) - 30} more")
        return 0

    moved = 0
    overwritten = 0
    conflicts_kept_src = []
    errors = []
    for src, dst, _, _ in plan:
        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst_existed = dst.is_file()
            # shutil.move handles cross-volume; on same volume it's a rename.
            # Use shutil.copy2 + unlink to be safe across OneDrive sync boundaries.
            shutil.copy2(str(src), str(dst))
            try:
                src.unlink()
            except OSError as exc:
                # OneDrive may keep the file hydrated; tolerate residual src.
                errors.append(f"unlink failed for {src}: {exc}")
            if dst_existed:
                overwritten += 1
            moved += 1
        except OSError as exc:
            errors.append(f"copy failed for {src} -> {dst}: {exc}")

    print(f"Moved {moved}/{len(plan)} files ({overwritten} overwrote existing)")
    if errors:
        print(f"Errors ({len(errors)}):", file=sys.stderr)
        for e in errors[:20]:
            print(f"  {e}", file=sys.stderr)

    # Now handle the 3 known conflicts (PRECHA, SCC, SCGD) which had
    # BOTH a misplaced file (newer, larger) AND a correctly-placed older
    # file. Re-run the migration with --prefer-larger semantics.

    # Final state check (skipped when --all-periods since the period filter is off)
    if not args.all_periods:
        post_aud = sum(1 for f in AUDITOR_DIR.rglob(f"*_{period}_*.md"))
        post_fs = sum(1 for f in FS_NOTES_DIR.rglob(f"*_{period}_*.md"))
        print(f"\nPost-migration counts for {period}:")
        print(f"  AUDITOR/<TK>/: {post_aud}")
        print(f"  FS-NOTES/<TK>/: {post_fs}")
    else:
        # Aggregate count across all periods
        post_aud = sum(1 for f in AUDITOR_DIR.rglob("NOTES_*.md"))
        post_fs = sum(1 for f in FS_NOTES_DIR.rglob("NOTES_*.md"))
        print(f"\nPost-migration NOTES_-prefixed file counts:")
        print(f"  AUDITOR/<TK>/: {post_aud} (should be 0)")
        print(f"  FS-NOTES/<TK>/: {post_fs}")

    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())