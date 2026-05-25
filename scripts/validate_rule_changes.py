"""Replay every LLM-classified headline through the (updated) rule engine.

For each row classified by an LLM (Haiku or Sonnet), ask: would the new rule
set match it? If so, would the rule's severity AGREE with the LLM's decision?

Outputs three buckets:
  - new_match_agree    : rule now matches AND agrees with the LLM — pure win
  - new_match_disagree : rule now matches BUT changes the label — review before merging!
  - no_match           : would now be tagged 'unclassified' (no rule matched)
"""

import os
import sys
sys.path.insert(0, "surveillance")

import duckdb  # noqa: E402
from rules import match_rules_with_diagnostics  # noqa: E402

# Honor SURVEILLANCE_DB_PATH so we can validate against the fresh R2 download
# without overwriting the local stale copy.
DB = os.environ.get("SURVEILLANCE_DB_PATH", "surveillance/surveillance.duckdb")

con = duckdb.connect(DB, read_only=True)
# Pull every Haiku-classified row. We don't filter by lang here so TH-only rows
# (id ends in '01' with no '00' twin) are validated against the new TH rules too.
rows = con.execute("""
    WITH stems AS (
        SELECT id, substring(id, 1, length(id) - 2) AS stem, lang, symbol, headline
        FROM news_items
    )
    -- EN-twin rows (the headline_en path)
    SELECT en.id, en.symbol, en.headline AS h_en, th.headline AS h_th,
           c.severity, c.category
    FROM stems en
    LEFT JOIN stems th ON th.stem = en.stem AND th.lang = 'th'
    JOIN classifications c ON c.news_id = en.id
    WHERE en.lang = 'en' AND c.model LIKE 'claude-%' AND en.headline IS NOT NULL
    UNION ALL
    -- TH-only rows (no EN twin)
    SELECT th.id, th.symbol, NULL AS h_en, th.headline AS h_th,
           c.severity, c.category
    FROM stems th
    JOIN classifications c ON c.news_id = th.id
    WHERE th.lang = 'th' AND c.model LIKE 'claude-%'
      AND NOT EXISTS (SELECT 1 FROM stems en WHERE en.stem = th.stem AND en.lang = 'en')
""").fetchall()

new_match_agree: list[tuple] = []
new_match_disagree: list[tuple] = []
no_match: list[tuple] = []

for nid, sym, h_en, h_th, llm_sev, llm_cat in rows:
    headline = h_en or h_th  # for the no-match dump
    cls, rule_name = match_rules_with_diagnostics(
        symbol=sym, headline_en=h_en, headline_th=h_th,
    )
    if cls is None:
        no_match.append((nid, sym, headline, llm_sev, llm_cat))
        continue
    if cls.severity == llm_sev and cls.category == llm_cat:
        new_match_agree.append((rule_name, sym, headline, llm_sev, llm_cat))
    else:
        new_match_disagree.append((rule_name, sym, headline, llm_sev, llm_cat,
                                    cls.severity, cls.category))

print(f"DB: {DB}")
print(f"Total LLM-classified rows: {len(rows)}")
print(f"  + new_match_agree    : {len(new_match_agree)}  (rule now handles them, agrees with LLM)")
print(f"  ! new_match_disagree : {len(new_match_disagree)}  (rule label differs from LLM — review)")
print(f"  ~ no_match           : {len(no_match)}  (would be tagged 'unclassified')")
print()

# Summarize agree by rule_name
from collections import Counter
agree_by_rule = Counter(r[0] for r in new_match_agree)
print("=== new agreed matches by rule ===")
for rule_name, n in agree_by_rule.most_common():
    print(f"  {n:3d}x  {rule_name}")

if new_match_disagree:
    print()
    print("=== DISAGREEMENTS (review carefully) ===")
    for rule_name, sym, headline, hs, hc, ns, nc in new_match_disagree[:20]:
        print(f"  [{rule_name}] {sym}: LLM={hs}/{hc}  Rule={ns}/{nc}")
        print(f"    headline: {headline[:95]}")
    if len(new_match_disagree) > 20:
        print(f"  ... and {len(new_match_disagree) - 20} more")
