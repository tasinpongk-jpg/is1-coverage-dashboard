"""Run the classifier across un-classified disclosures.

Two-tier flow:
  1. Rules-based pre-classifier (rules.py) handles ~65% of disclosures
     deterministically (no API call). Rules are validated to agree with
     Haiku on >94% of severity labels.
  2. Genuinely ambiguous headlines fall through to Claude Haiku 4.5.

CLI:
    classify_batch.py                 # all unclassified rows (rules + Haiku)
    classify_batch.py --limit 10      # smoke test
    classify_batch.py --rules-only    # don't call Haiku at all (dry-run on rules)
    classify_batch.py --no-rules      # legacy mode: Haiku-only
"""

from __future__ import annotations

import argparse
import sys
import time
import traceback

from classifier import MODEL_EN, MODEL_TH, _client, classify_one
from rules import match_rules_with_diagnostics
from store import conn

# Pseudo-model identifier for rule-based classifications (so the model column
# in DuckDB can distinguish rule-classified rows from Haiku-classified rows).
RULES_MODEL_TAG = "rules-v1"


def _fetch_unclassified(limit: int | None) -> list[dict]:
    """Rows needing classification. Two cases:

      1. EN row that has no classification yet (the original path) — joins TH
         twin headline when present so the model can disambiguate.
      2. TH-only row whose `id` stem has no EN counterpart and which has no
         classification. Catches genuinely TH-first filings (e.g. quarterly
         financials filed Thai-only on the day, SEC News pass-throughs).

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
    -- Path 1: EN rows missing classification (TH twin headline via scalar subquery)
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
    WHERE en.lang = 'en' AND c.news_id IS NULL

    UNION ALL

    -- Path 2: TH-only rows (no EN twin) missing classification
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
      AND c.news_id IS NULL
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


def _persist(news_id: str, symbol: str, parsed, usage: dict, model: str) -> None:
    with conn() as c:
        c.execute(
            """
            INSERT INTO classifications
              (news_id, symbol, severity, category, summary_en, summary_th,
               suggested_action, rationale, model,
               input_tokens, output_tokens, cache_read_tokens, cache_write_tokens)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                news_id,
                symbol,
                parsed.severity,
                parsed.category,
                parsed.summary_en,
                parsed.summary_th,
                parsed.suggested_action,
                parsed.rationale,
                model,
                usage["input"],
                usage["output"],
                usage["cache_read"],
                usage["cache_write"],
            ],
        )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=None, help="Max rows to classify")
    p.add_argument("--dry-run", action="store_true", help="Print rows that would be classified, don't call API")
    p.add_argument("--rules-only", action="store_true",
                   help="Apply rules but do NOT fall through to Haiku for ambiguous rows")
    p.add_argument("--no-rules", action="store_true",
                   help="Legacy mode: skip rules, send everything to Haiku")
    args = p.parse_args()

    if args.rules_only and args.no_rules:
        raise SystemExit("--rules-only and --no-rules are mutually exclusive")

    rows = _fetch_unclassified(args.limit)
    # Defense-in-depth: even if _fetch_unclassified's SQL ever returns a row
    # twice (it shouldn't post-scalar-subquery, but if it does, the second
    # INSERT into classifications would crash on the PK), keep only the first
    # occurrence of each id.
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
        print("Nothing to classify — all EN rows already have a classification row.")
        return 0

    n_en = sum(1 for r in rows if r["lang_primary"] == "en")
    n_th = sum(1 for r in rows if r["lang_primary"] == "th")
    print(f"Found {len(rows)} unclassified row(s)  (EN={n_en}, TH-only={n_th}).")
    if args.dry_run:
        for r in rows[:20]:
            primary = r["headline_en"] if r["lang_primary"] == "en" else r["headline_th"]
            print(f"  [{r['lang_primary']}] {r['datetime_iso']} {r['symbol']:8s} {(primary or '')[:90]}")
        if len(rows) > 20:
            print(f"  ... and {len(rows) - 20} more.")
        return 0

    client = None  # lazy-init: only needed if we actually call Haiku
    started = time.monotonic()
    counts = {"critical": 0, "material": 0, "routine": 0}
    tot = {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0}
    failures = 0
    rule_hits = 0
    haiku_hits = 0

    for i, row in enumerate(rows, 1):
        is_th_only = row["lang_primary"] == "th"

        # ---- Tier 1: rules-based pre-classifier ----
        # Tries EN rules against headline_en first; if no match (or this is a
        # TH-only filing with headline_en=None), falls through to TH-only rules
        # against headline_th. See rules._TH_RULES for what's matched.
        rule_cls = None
        rule_name = None
        if not args.no_rules:
            rule_cls, rule_name = match_rules_with_diagnostics(
                symbol=row["symbol"] or "",
                headline_en=row["headline_en"],
                headline_th=row.get("headline_th"),
            )

        if rule_cls is not None:
            # Persist with zero-token usage and rules-model tag
            _persist(
                row["id"], row["symbol"], rule_cls,
                {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0},
                RULES_MODEL_TAG,
            )
            counts[rule_cls.severity] += 1
            rule_hits += 1
            marker = {"critical": "!!!", "material": " * ", "routine": "   "}[rule_cls.severity]
            print(
                f"[{i}/{len(rows)}] {marker} [RULE] {row['symbol']:8s} {rule_cls.severity:8s} "
                f"{rule_cls.category:25s} ({rule_name}) {(row['headline_en'] or '')[:60]}"
            )
            continue

        if args.rules_only:
            print(f"[{i}/{len(rows)}]   ?   [skip] {row['symbol']:8s} (no rule match, --rules-only)")
            continue

        # ---- Tier 2: fall through to Haiku ----
        if is_th_only:
            primary_headline = f"[TH-only filing] {row['headline_th'] or ''}"
            secondary_th: str | None = None
            row_model = MODEL_TH
        else:
            primary_headline = row["headline_en"] or ""
            secondary_th = row["headline_th"]
            row_model = MODEL_EN

        if client is None:
            client = _client()

        try:
            parsed, usage = classify_one(
                client,
                symbol=row["symbol"],
                datetime_iso=row["datetime_iso"],
                headline_en=primary_headline,
                headline_th=secondary_th,
                url=row["url"] or "",
                model=row_model,
            )
        except Exception as e:  # noqa: BLE001
            failures += 1
            print(
                f"[{i}/{len(rows)}] FAIL {row['symbol']} {row['id']}  "
                f"{type(e).__name__}: {str(e)[:200]}"
            )
            traceback.print_exc()
            continue

        _persist(row["id"], row["symbol"], parsed, usage, row_model)
        counts[parsed.severity] += 1
        haiku_hits += 1
        for k in tot:
            tot[k] += usage[k]

        marker = {"critical": "!!!", "material": " * ", "routine": "   "}[parsed.severity]
        lang_tag = "TH" if is_th_only else "EN"
        print(
            f"[{i}/{len(rows)}] {marker} [{lang_tag}] {row['symbol']:8s} {parsed.severity:8s} "
            f"{parsed.category:25s} {parsed.summary_en[:60]}"
        )

    elapsed = time.monotonic() - started
    total = rule_hits + haiku_hits
    print(f"\n=== batch complete in {elapsed:.1f}s ===")
    print(f"counts: {counts}  failures: {failures}")
    if total:
        rule_pct = rule_hits / total * 100
        print(f"rules : {rule_hits:,}/{total:,} ({rule_pct:.1f}%) — zero API cost")
        print(f"haiku : {haiku_hits:,}/{total:,} ({100-rule_pct:.1f}%) — billable")
    if haiku_hits:
        print(f"tokens: input={tot['input']:,}  output={tot['output']:,}  "
              f"cache_read={tot['cache_read']:,}  cache_write={tot['cache_write']:,}")
        cache_ratio = tot["cache_read"] / max(tot["input"] + tot["cache_read"], 1) * 100
        print(f"cache hit ratio (input side): {cache_ratio:.1f}%")

    # Loud-fail the step if the Haiku tier was reached but every attempt failed.
    # That's the auth-error / network-outage / spend-cap pattern — silently
    # exiting 0 here previously let CI go green while ~40% of disclosures
    # stayed unclassified. Partial failures (some hits, some failures, e.g.
    # transient rate limits) still exit 0.
    if failures > 0 and haiku_hits == 0:
        print(
            f"::error::All {failures} Haiku attempt(s) failed; no successful "
            "classifications this run. Check the FAIL lines above for the "
            "exception type — common causes: invalid ANTHROPIC_API_KEY, "
            "workspace spend cap reached, network outage."
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
