"""Extract rule-mining input from the surveillance DB.

This script is the data-prep half of the offline rule-mining loop. It pulls
two cohorts from the classifications table:

  1. LLM-labeled rows (model LIKE 'claude-%') — these are training examples.
     The LLM has already assigned a high-confidence severity/category to each.
     We mine their headline patterns to promote them into deterministic rules.

  2. Unclassified rows (model = 'unclassified', severity = 'unclassified')
     — these are the new gaps after classify_batch.py rule-only mode rejected
     them. The subagent decides their classification fresh and drafts a rule.

For each cohort, we cluster headlines by the leading 8 lower-cased words
(strips digits, dates, ticker tokens, and trailing detail). A cluster is
'rule-worthy' if it has >= MIN_CLUSTER_SIZE rows AND the LLM labels agree
on a single severity for >= AGREEMENT_THRESHOLD of the rows.

Output: a JSON file the orchestrating Claude session feeds into the
rule-mining subagent. See `scripts/rule_mining_input.json` for the schema.

CLI:
    python scripts/mine_rules.py
    SURVEILLANCE_DB_PATH=C:/path/surveillance.duckdb python scripts/mine_rules.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = Path(os.environ.get("SURVEILLANCE_DB_PATH") or
               (ROOT / "surveillance" / "surveillance.duckdb"))
OUTPUT_PATH = ROOT / "scripts" / "rule_mining_input.json"

# Clustering thresholds.
MIN_CLUSTER_SIZE = 2        # don't promote a one-off into a rule
AGREEMENT_THRESHOLD = 0.80  # majority must agree on severity to promote
LEADING_WORDS = 8           # cluster key = first N normalized words

# Tokens to strip from headlines before clustering (digits, dates, ticker
# tokens, common punctuation). Anything that varies row-to-row without
# changing the disclosure type belongs here.
_NORMALIZE_PATTERNS = [
    (re.compile(r"\b\d{1,4}/\d{1,4}(/\d{2,4})?\b"), " "),   # dates like 1/2026 or 12/05/2026
    (re.compile(r"\bno\.?\s*\d+/\d+\b", re.I), " "),         # "No. 4/2026"
    (re.compile(r"\b\d+\b"), " "),                            # bare numbers
    (re.compile(r"[\(\)\[\],;:.\-/]+"), " "),                # punctuation
    (re.compile(r"\s+"), " "),
]


def _normalize(text: str) -> str:
    s = text.strip()
    for pat, repl in _NORMALIZE_PATTERNS:
        s = pat.sub(repl, s)
    return s.strip().lower()


def _cluster_key(text: str) -> str:
    """Cluster key = first LEADING_WORDS words of the normalized headline."""
    return " ".join(_normalize(text).split()[:LEADING_WORDS])


def _fetch_labeled() -> list[dict]:
    """LLM-classified rows. These are the training examples."""
    sql = """
    SELECT c.news_id, c.symbol, c.severity, c.category, c.model,
           n.lang, n.headline, n.url, n.datetime_iso
    FROM classifications c
    JOIN news_items n ON n.id = c.news_id
    WHERE c.model LIKE 'claude-%'
    """
    cols = ["news_id", "symbol", "severity", "category", "model",
            "lang", "headline", "url", "datetime_iso"]
    with duckdb.connect(str(DB_PATH), read_only=True) as conn:
        return [dict(zip(cols, r)) for r in conn.execute(sql).fetchall()]


def _fetch_unclassified() -> list[dict]:
    """Rows the current rules.py couldn't classify."""
    sql = """
    SELECT c.news_id, c.symbol, c.severity, c.category, c.model,
           n.lang, n.headline, n.url, n.datetime_iso
    FROM classifications c
    JOIN news_items n ON n.id = c.news_id
    WHERE c.severity = 'unclassified' OR c.model = 'unclassified'
    """
    cols = ["news_id", "symbol", "severity", "category", "model",
            "lang", "headline", "url", "datetime_iso"]
    with duckdb.connect(str(DB_PATH), read_only=True) as conn:
        return [dict(zip(cols, r)) for r in conn.execute(sql).fetchall()]


def _build_clusters(rows: list[dict]) -> list[dict]:
    """Group rows by cluster_key and compute majority label."""
    buckets: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        hl = r.get("headline") or ""
        if not hl.strip():
            continue
        buckets[_cluster_key(hl)].append(r)

    clusters: list[dict] = []
    for key, members in buckets.items():
        if not key:
            continue
        sev_counts = Counter(m["severity"] for m in members)
        cat_counts = Counter(m["category"] for m in members)
        top_sev, top_sev_n = sev_counts.most_common(1)[0]
        top_cat, top_cat_n = cat_counts.most_common(1)[0]
        agreement = top_sev_n / len(members)
        clusters.append({
            "key": key,
            "size": len(members),
            "majority_severity": top_sev,
            "majority_category": top_cat,
            "severity_agreement": round(agreement, 3),
            "severity_distribution": dict(sev_counts),
            "category_distribution": dict(cat_counts),
            "languages": sorted({m["lang"] for m in members}),
            "sample_headlines": [m["headline"][:200] for m in members[:5]],
            "sample_symbols": sorted({m["symbol"] for m in members})[:8],
            "n_distinct_symbols": len({m["symbol"] for m in members}),
        })

    # Rank by (size * agreement) descending — biggest, most-agreed clusters first.
    clusters.sort(key=lambda c: c["size"] * c["severity_agreement"], reverse=True)
    return clusters


def _rule_worthy(cluster: dict) -> bool:
    """Heuristic: cluster is worth promoting to a rule."""
    return (cluster["size"] >= MIN_CLUSTER_SIZE
            and cluster["severity_agreement"] >= AGREEMENT_THRESHOLD)


def _summarize_unclassified(clusters: list[dict]) -> list[dict]:
    """For unclassified rows the LLM hasn't labeled them, so 'majority_severity'
    is always 'unclassified'. We still surface clusters of size >= 2 so the
    subagent can decide a severity and draft a rule."""
    return [c for c in clusters if c["size"] >= MIN_CLUSTER_SIZE]


def main() -> int:
    if not DB_PATH.exists():
        print(f"::error::DB not found: {DB_PATH}", file=sys.stderr)
        return 1

    print(f"Reading from {DB_PATH}")
    labeled = _fetch_labeled()
    unclass = _fetch_unclassified()
    print(f"  labeled    rows: {len(labeled):>5}")
    print(f"  unclass    rows: {len(unclass):>5}")

    labeled_clusters = _build_clusters(labeled)
    unclass_clusters = _build_clusters(unclass)

    rule_worthy = [c for c in labeled_clusters if _rule_worthy(c)]
    unclass_worthy = _summarize_unclassified(unclass_clusters)

    print(f"  labeled clusters total          : {len(labeled_clusters):>4}")
    print(f"  labeled clusters rule-worthy    : {len(rule_worthy):>4}  "
          f"(size>={MIN_CLUSTER_SIZE} AND agreement>={AGREEMENT_THRESHOLD:.0%})")
    print(f"  unclassified clusters total     : {len(unclass_clusters):>4}")
    print(f"  unclassified clusters size>={MIN_CLUSTER_SIZE}: {len(unclass_worthy):>4}")

    output = {
        "db_path": str(DB_PATH),
        "thresholds": {
            "min_cluster_size": MIN_CLUSTER_SIZE,
            "agreement_threshold": AGREEMENT_THRESHOLD,
            "leading_words_for_cluster": LEADING_WORDS,
        },
        "counts": {
            "labeled_rows": len(labeled),
            "unclassified_rows": len(unclass),
            "labeled_clusters_total": len(labeled_clusters),
            "labeled_clusters_rule_worthy": len(rule_worthy),
            "unclassified_clusters_total": len(unclass_clusters),
            "unclassified_clusters_worthy": len(unclass_worthy),
        },
        "labeled_clusters_rule_worthy": rule_worthy,
        "unclassified_clusters_worthy": unclass_worthy,
    }
    OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2),
                            encoding="utf-8")
    print(f"\nWrote {OUTPUT_PATH}  ({OUTPUT_PATH.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
