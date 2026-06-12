"""Run the rules-based classifier across un-classified disclosures.

Single-tier flow:
  - Rules-based pre-classifier (rules.py) handles every disclosure deterministically.
  - Rows that no rule matches are persisted with severity='unclassified'.
  - The offline rule-miner subagent (scripts/mine_rules.py) reviews the
    unclassified set + the historical LLM-labeled rows and promotes new
    patterns into rules.py. After each rules.py upgrade, this batch re-runs
    against rows where severity='unclassified' (UPSERT) so newly covered
    patterns get the correct label without manual intervention.

Haiku fall-through was removed 2026-05-25 (cost was ~$5/mo + the offline
mining loop fully covers what Haiku would have caught, deterministically).

CLI:
    classify_batch.py                 # classify all rows missing/unclassified
    classify_batch.py --limit 10      # smoke test
    classify_batch.py --dry-run       # print rows that would be classified
"""

from __future__ import annotations

import argparse
import sys
import time

import classifier_groq
from rules import match_rules_with_diagnostics
from store import conn

# Pseudo-model identifier for rule-based classifications (so the model column
# in DuckDB can distinguish rule-classified rows from LLM-classified rows).
RULES_MODEL_TAG = "rules-v1"

# Tag for rows that no rule matched. Persisted as severity='unclassified'
# so the offline mine_rules.py subagent can WHERE model='unclassified'.
UNCLASSIFIED_TAG = "unclassified"


def _fetch_unclassified(limit: int | None) -> list[dict]:
    """Rows needing (re)classification. Three cases:

      1. EN row that has no classification yet (the original path) — joins TH
         twin headline when present so the model can disambiguate.
      2. TH-only row whose `id` stem has no EN counterpart and which has no
         classification. Catches genuinely TH-first filings (e.g. quarterly
         financials filed Thai-only on the day, SEC News pass-throughs).
      3. Rows previously tagged severity='unclassified' — these are retried
         every run so newly-added rules in rules.py can promote them.

    EN/TH dedup pairing is by `id` stem: SET assigns paired rows IDs ending
    `00` (EN) and `01` (TH). 89.6% of TH rows already have an EN pair and are
    skipped here to avoid duplicate-spend on the same disclosure.
    """
    # NOTE on the TH-twin lookup: 9-digit news IDs follow the EN/TH twin
    # convention (EN ends in `00`, TH ends in `01`, so stripping the last 2
    # chars yields a unique stem per pair). 14-digit Financial Statement IDs
    # (like 17786285863310) do NOT follow that — multiple rows can share a
    # stem, so a plain LEFT JOIN multiplies the EN side and the same news_id
    # gets queued for INSERT twice → PK violation. Using a scalar subquery
    # for headline_th guarantees one EN row maps to at most one TH headline.
    sql = """
    WITH stems AS (
        SELECT
            id,
            substring(id, 1, length(id) - 2) AS stem,
            lang,
            symbol,
            datetime_iso,
            headline,
            url
        FROM news_items
    )
    -- Path 1: EN rows missing classification OR previously unclassified
    SELECT
        en.id           AS id,
        en.symbol       AS symbol,
        en.datetime_iso AS datetime_iso,
        en.headline     AS headline_en,
        en.url          AS url,
        (SELECT th.headline FROM stems th
          WHERE th.stem = en.stem AND th.lang = 'th'
          LIMIT 1) AS headline_th,
        'en'            AS lang_primary
    FROM stems en
    LEFT JOIN classifications c ON c.news_id = en.id
    WHERE en.lang = 'en'
      AND (c.news_id IS NULL OR c.severity = 'unclassified')

    UNION ALL

    -- Path 2: TH-only rows (no EN twin) missing classification OR previously unclassified
    SELECT
        th.id           AS id,
        th.symbol       AS symbol,
        th.datetime_iso AS datetime_iso,
        NULL            AS headline_en,
        th.url          AS url,
        th.headline     AS headline_th,
        'th'            AS lang_primary
    FROM stems th
    LEFT JOIN classifications c ON c.news_id = th.id
    WHERE th.lang = 'th'
      AND (c.news_id IS NULL OR c.severity = 'unclassified')
      AND NOT EXISTS (
          SELECT 1 FROM stems en
          WHERE en.stem = th.stem AND en.lang = 'en'
      )

    ORDER BY datetime_iso DESC
    """
    if limit:
        sql += f" LIMIT {int(limit)}"
    with conn() as c:
        cols = ["id", "symbol", "datetime_iso", "headline_en", "url",
                "headline_th", "lang_primary"]
        return [dict(zip(cols, row)) for row in c.execute(sql).fetchall()]


def _upsert(news_id: str, symbol: str, severity: str, category: str,
            summary_en: str, summary_th: str, suggested_action: str,
            rationale: str, model: str) -> None:
    """INSERT-or-REPLACE so re-classification (unclassified → matched) overwrites."""
    with conn() as c:
        c.execute(
            """
            INSERT OR REPLACE INTO classifications
              (news_id, symbol, severity, category, summary_en, summary_th,
               suggested_action, rationale, model,
               input_tokens, output_tokens, cache_read_tokens, cache_write_tokens)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0, 0)
            """,
            [news_id, symbol, severity, category, summary_en, summary_th,
             suggested_action, rationale, model],
        )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=None, help="Max rows to classify")
    p.add_argument("--dry-run", action="store_true",
                   help="Print rows that would be classified, don't write to DB")
    args = p.parse_args()

    rows = _fetch_unclassified(args.limit)
    # Defense-in-depth: even if _fetch_unclassified's SQL ever returns a row
    # twice, keep only the first occurrence of each id.
    seen_ids: set[str] = set()
    deduped: list[dict] = []
    for r in rows:
        if r["id"] in seen_ids:
            continue
        seen_ids.add(r["id"])
        deduped.append(r)
    if len(deduped) != len(rows):
        print(f"WARNING: _fetch_unclassified returned {len(rows) - len(deduped)} "
              f"duplicate-id row(s); deduped before processing.")
    rows = deduped
    if not rows:
        print("Nothing to classify — all rows already covered by rules.")
        return 0

    n_en = sum(1 for r in rows if r["lang_primary"] == "en")
    n_th = sum(1 for r in rows if r["lang_primary"] == "th")
    print(f"Found {len(rows)} row(s) needing (re)classification  (EN={n_en}, TH-only={n_th}).")
    if args.dry_run:
        for r in rows[:20]:
            primary = r["headline_en"] if r["lang_primary"] == "en" else r["headline_th"]
            print(f"  [{r['lang_primary']}] {r['datetime_iso']} {r['symbol']:8s} {(primary or '')[:90]}")
        if len(rows) > 20:
            print(f"  ... and {len(rows) - 20} more.")
        return 0

    started = time.monotonic()
    counts = {"critical": 0, "material": 0, "routine": 0, "unclassified": 0}
    rule_hits = 0
    groq_hits = 0
    unclassified_hits = 0
    if classifier_groq.available():
        print(f"Groq fall-through ACTIVE ({classifier_groq.MODEL_TAG}) — "
              "rule-misses go to the free-tier model instead of the queue.")

    for i, row in enumerate(rows, 1):
        rule_cls, rule_name = match_rules_with_diagnostics(
            symbol=row["symbol"] or "",
            headline_en=row["headline_en"],
            headline_th=row.get("headline_th"),
        )

        if rule_cls is not None:
            _upsert(
                row["id"], row["symbol"],
                rule_cls.severity, rule_cls.category,
                rule_cls.summary_en, rule_cls.summary_th,
                rule_cls.suggested_action, rule_cls.rationale,
                RULES_MODEL_TAG,
            )
            counts[rule_cls.severity] += 1
            rule_hits += 1
            marker = {"critical": "!!!", "material": " * ", "routine": "   "}[rule_cls.severity]
            print(
                f"[{i}/{len(rows)}] {marker} [RULE] {row['symbol']:8s} {rule_cls.severity:12s} "
                f"{rule_cls.category:25s} ({rule_name}) {(row['headline_en'] or row.get('headline_th') or '')[:60]}"
            )
            continue

        # No rule matched → free-tier Groq fall-through when a key is set
        # (tagged groq/* so mine_rules.py mines these as LLM-labeled
        # examples). Without a key, or on failure, queue for the rule-miner.
        primary_hl = row["headline_en"] or row.get("headline_th") or ""
        if classifier_groq.available():
            try:
                cls, model_tag = classifier_groq.classify_one_groq(
                    symbol=row["symbol"] or "",
                    datetime_iso=row["datetime_iso"],
                    headline_en=row["headline_en"],
                    headline_th=row.get("headline_th"),
                    url=row["url"],
                )
                _upsert(
                    row["id"], row["symbol"],
                    cls.severity, cls.category,
                    cls.summary_en, cls.summary_th,
                    cls.suggested_action, cls.rationale,
                    model_tag,
                )
                counts[cls.severity] += 1
                groq_hits += 1
                marker = {"critical": "!!!", "material": " * ",
                          "routine": "   ", "unclassified": " ? "}[cls.severity]
                print(
                    f"[{i}/{len(rows)}] {marker} [GROQ] {row['symbol']:8s} {cls.severity:12s} "
                    f"{cls.category:25s} {primary_hl[:60]}"
                )
                continue
            except Exception as e:
                print(f"[{i}/{len(rows)}]  !  [GROQ-FAIL] {row['symbol']:8s} {e} "
                      f"— falling back to unclassified")
        _upsert(
            row["id"], row["symbol"],
            "unclassified", "other",
            f"{row['symbol']} unclassified disclosure: {primary_hl[:90]}",
            f"{row['symbol']} รายการที่ยังไม่จัดประเภท: {primary_hl[:90]}",
            "Pending offline rule-mining review; no rule pattern matched this headline yet.",
            "[unclassified] no rule pattern matched — queued for offline review by mine_rules.py.",
            UNCLASSIFIED_TAG,
        )
        counts["unclassified"] += 1
        unclassified_hits += 1
        lang_tag = "TH" if row["lang_primary"] == "th" else "EN"
        print(
            f"[{i}/{len(rows)}]  ?  [UNCL][{lang_tag}] {row['symbol']:8s} "
            f"{primary_hl[:80]}"
        )

    elapsed = time.monotonic() - started
    total = rule_hits + groq_hits + unclassified_hits
    print(f"\n=== batch complete in {elapsed:.1f}s ===")
    print(f"counts: {counts}")
    if total:
        pct = lambda n: n / total * 100  # noqa: E731
        print(f"rules        : {rule_hits:,}/{total:,} ({pct(rule_hits):.1f}%) — deterministic, zero cost")
        if groq_hits:
            print(f"groq         : {groq_hits:,}/{total:,} ({pct(groq_hits):.1f}%) — free-tier LLM fall-through")
        print(f"unclassified : {unclassified_hits:,}/{total:,} ({pct(unclassified_hits):.1f}%) — queued for mine_rules.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
