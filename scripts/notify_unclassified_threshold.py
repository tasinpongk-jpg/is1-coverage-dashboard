"""Weekly notifier: open a GitHub issue when ≥THRESHOLD unclassified rows accumulate.

Runs from the unclassified-notifier.yml workflow on a Sunday-10:00-BKK cron.
The workflow downloads the production R2 DB to /tmp/surveillance.duckdb,
then calls this script. The script:

  1. Counts rows where severity='unclassified' in the freshly-pulled DB.
  2. Clusters their headlines (same normalization as scripts/mine_rules.py).
  3. If count >= THRESHOLD: ensures one open GitHub issue exists with label
     'unclassified-mining'. If no open issue: opens one with the cluster
     summary as the body. If an issue is already open: leaves it alone
     (avoids spam — user closes when they've mined).
  4. If count < THRESHOLD and an open issue exists: comments on it and
     closes (the latest CI run reclassified enough rows that the queue is
     no longer worth mining).

GitHub interactions go through the `gh` CLI, which auto-authenticates in
GH Actions via `GH_TOKEN` (workflow sets it from `secrets.GITHUB_TOKEN`).

CLI:
    python scripts/notify_unclassified_threshold.py
    python scripts/notify_unclassified_threshold.py --threshold 50 --dry-run
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = Path(os.environ.get("SURVEILLANCE_DB_PATH") or
               (ROOT / "surveillance" / "surveillance.duckdb"))

DEFAULT_THRESHOLD = 30
ISSUE_LABEL = "unclassified-mining"
ISSUE_TITLE_TEMPLATE = "Unclassified disclosures ready for rule-mining ({count} rows)"

# Same normalization as scripts/mine_rules.py — keep in sync if either changes.
_NORMALIZE_PATTERNS = [
    (re.compile(r"\b\d{1,4}/\d{1,4}(/\d{2,4})?\b"), " "),
    (re.compile(r"\bno\.?\s*\d+/\d+\b", re.I), " "),
    (re.compile(r"\b\d+\b"), " "),
    (re.compile(r"[\(\)\[\],;:.\-/]+"), " "),
    (re.compile(r"\s+"), " "),
]
LEADING_WORDS = 8


def _normalize(text: str) -> str:
    s = text.strip()
    for pat, repl in _NORMALIZE_PATTERNS:
        s = pat.sub(repl, s)
    return s.strip().lower()


def _cluster_key(text: str) -> str:
    return " ".join(_normalize(text).split()[:LEADING_WORDS])


def _fetch_unclassified_clusters() -> tuple[int, list[dict]]:
    """Return (total_count, clusters_sorted_by_size_desc)."""
    sql = """
    SELECT n.symbol, n.lang, n.headline, n.url, n.datetime_iso
    FROM classifications c
    JOIN news_items n ON n.id = c.news_id
    WHERE c.severity = 'unclassified'
    ORDER BY n.datetime_iso DESC
    """
    with duckdb.connect(str(DB_PATH), read_only=True) as conn:
        rows = conn.execute(sql).fetchall()

    total = len(rows)
    buckets: dict[str, list[tuple]] = defaultdict(list)
    for sym, lang, headline, url, dt in rows:
        if not headline:
            continue
        buckets[_cluster_key(headline)].append((sym, lang, headline, url, dt))

    clusters = []
    for key, members in buckets.items():
        if not key:
            continue
        clusters.append({
            "key": key,
            "size": len(members),
            "languages": sorted({m[1] for m in members}),
            "sample_headlines": [m[2][:200] for m in members[:3]],
            "sample_symbols": sorted({m[0] for m in members})[:6],
            "latest_datetime": max(m[4] for m in members),
        })
    clusters.sort(key=lambda c: c["size"], reverse=True)
    return total, clusters


def _build_issue_body(total: int, clusters: list[dict]) -> str:
    """Markdown body for the GitHub issue."""
    lines = [
        f"**{total} rows** currently tagged `severity='unclassified'` in the production DB.",
        "",
        "These accumulated since the last rule-mining pass. Cluster them, draft new "
        "regex rules in `surveillance/rules.py`, and the next CI run will auto-relabel "
        "previously-unclassified rows via the UPSERT path in `classify_batch.py`.",
        "",
        "## How to mine",
        "",
        "Ask Elisa in a Claude Code session: **\"mine the unclassified rules\"**.",
        "",
        "Manual path:",
        "```powershell",
        "$env:SURVEILLANCE_DB_PATH = \"C:/Users/tasin/AppData/Local/Temp/surveillance_fresh.duckdb\"",
        "$env:AWS_ACCESS_KEY_ID = $env:R2_ACCESS_KEY_ID",
        "$env:AWS_SECRET_ACCESS_KEY = $env:R2_SECRET_ACCESS_KEY",
        "python surveillance/r2_sync.py download",
        "python scripts/mine_rules.py",
        "# review scripts/rule_mining_input.json, draft rules, edit surveillance/rules.py",
        "python scripts/validate_rule_changes.py",
        "git add surveillance/rules.py",
        "git commit -m \"perf(rules): mining pass #N — <summary>\"",
        "git push origin main",
        "```",
        "",
        f"## Top {min(len(clusters), 15)} clusters by size",
        "",
        "| Size | Lang | Sample headline | Symbols |",
        "|------|------|-----------------|---------|",
    ]
    for c in clusters[:15]:
        sample = (c["sample_headlines"][0] if c["sample_headlines"] else "").replace("|", "\\|")[:90]
        syms = ", ".join(c["sample_symbols"][:4])
        lang = "/".join(c["languages"])
        lines.append(f"| {c['size']} | {lang} | {sample} | {syms} |")

    if len(clusters) > 15:
        lines.append("")
        lines.append(f"_… and {len(clusters) - 15} more clusters of size 1._")

    lines.extend([
        "",
        "---",
        "_This issue is auto-opened by `.github/workflows/unclassified-notifier.yml` "
        "when the unclassified-row count crosses the threshold. Close it after you've "
        "mined + pushed new rules; the next weekly check will auto-close it if the "
        "count drops on its own._",
    ])
    return "\n".join(lines)


def _gh(*args: str, check: bool = True, **kwargs) -> subprocess.CompletedProcess:
    """Run a gh CLI command. In CI, GH_TOKEN env var auto-authenticates."""
    result = subprocess.run(
        ["gh", *args],
        capture_output=True, text=True, check=False, **kwargs,
    )
    if check and result.returncode != 0:
        sys.stderr.write(f"gh {' '.join(args)} failed (exit {result.returncode}):\n")
        sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)
    return result


def _find_open_issue() -> str | None:
    """Return the number of the open mining-notifier issue, or None."""
    r = _gh("issue", "list", "--label", ISSUE_LABEL, "--state", "open",
            "--limit", "1", "--json", "number")
    out = r.stdout.strip()
    if not out or out == "[]":
        return None
    import json
    return str(json.loads(out)[0]["number"])


def _ensure_label_exists() -> None:
    """Create the label if missing. Idempotent — gh exits 0 even if it exists."""
    _gh("label", "create", ISSUE_LABEL,
        "--description", "Cron-opened issues nudging the user to mine unclassified rules.",
        "--color", "FBCA04",
        "--force",  # update if exists, don't fail
        check=False)


def _open_issue(title: str, body: str) -> str:
    r = _gh("issue", "create", "--title", title, "--body", body, "--label", ISSUE_LABEL)
    # gh prints the URL on success; the issue number is the trailing path segment
    url = r.stdout.strip()
    return url.rsplit("/", 1)[-1]


def _close_issue(number: str, comment: str) -> None:
    _gh("issue", "comment", number, "--body", comment)
    _gh("issue", "close", number)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--threshold", type=int, default=DEFAULT_THRESHOLD,
                   help=f"Minimum unclassified count to open an issue (default {DEFAULT_THRESHOLD}).")
    p.add_argument("--dry-run", action="store_true",
                   help="Print what would happen, don't touch GitHub.")
    args = p.parse_args()

    if not DB_PATH.exists():
        print(f"::error::DB not found: {DB_PATH}", file=sys.stderr)
        return 1

    total, clusters = _fetch_unclassified_clusters()
    print(f"unclassified rows: {total}  threshold: {args.threshold}")
    print(f"clusters         : {len(clusters)}  largest: {clusters[0]['size'] if clusters else 0}")

    if args.dry_run:
        existing = "unknown (dry-run)"
        print(f"existing open issue: {existing}")
        if total >= args.threshold:
            print(f"\nWOULD open issue. Body preview:\n{'-'*60}")
            print(_build_issue_body(total, clusters)[:1200])
            print(f"{'-'*60}\n... (truncated)")
        else:
            print("WOULD do nothing (below threshold).")
        return 0

    _ensure_label_exists()
    existing = _find_open_issue()
    print(f"existing open issue: {existing or 'none'}")

    if total >= args.threshold:
        if existing:
            print(f"Threshold met (≥{args.threshold}) but issue #{existing} already open — leaving alone.")
            return 0
        body = _build_issue_body(total, clusters)
        title = ISSUE_TITLE_TEMPLATE.format(count=total)
        number = _open_issue(title, body)
        print(f"Opened issue #{number}: {title}")
        return 0

    # Below threshold
    if existing:
        comment = (
            f"Unclassified row count dropped to **{total}** "
            f"(threshold {args.threshold}). Auto-closing — the queue has shrunk "
            "(either you pushed new rules or the firehose was quiet this week)."
        )
        _close_issue(existing, comment)
        print(f"Auto-closed issue #{existing} (count {total} < {args.threshold}).")
    else:
        print(f"Below threshold ({total} < {args.threshold}), no open issue — no action.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
