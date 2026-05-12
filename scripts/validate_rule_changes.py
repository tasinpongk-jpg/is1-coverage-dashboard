"""Replay every Haiku-classified headline through the (updated) rule engine.

For each row classified by Haiku, ask: would the new rule set match it?
If so, would the rule's severity AGREE with Haiku's decision?

Outputs three buckets:
  - new_match_agree    : rule now matches AND agrees with Haiku — pure win, will save API spend
  - new_match_disagree : rule now matches BUT changes the label — review before merging!
  - no_match           : still falls through to Haiku (expected for ambiguous content)
"""

import sys
sys.path.insert(0, "surveillance")

import duckdb  # noqa: E402
from rules import match_rules_with_diagnostics  # noqa: E402

DB = "surveillance/surveillance.duckdb"

con = duckdb.connect(DB)
rows = con.execute("""
    SELECT n.id, n.symbol, n.headline,
           c.severity AS haiku_sev, c.category AS haiku_cat
    FROM news_items n
    JOIN classifications c ON c.news_id = n.id
    WHERE c.model LIKE 'claude-haiku%' AND n.lang = 'en' AND n.headline IS NOT NULL
""").fetchall()

new_match_agree: list[tuple] = []
new_match_disagree: list[tuple] = []
no_match: list[tuple] = []

for nid, sym, headline, haiku_sev, haiku_cat in rows:
    cls, rule_name = match_rules_with_diagnostics(symbol=sym, headline_en=headline)
    if cls is None:
        no_match.append((nid, sym, headline, haiku_sev, haiku_cat))
        continue
    if cls.severity == haiku_sev and cls.category == haiku_cat:
        new_match_agree.append((rule_name, sym, headline, haiku_sev, haiku_cat))
    else:
        new_match_disagree.append((rule_name, sym, headline, haiku_sev, haiku_cat,
                                    cls.severity, cls.category))

print(f"Total Haiku-classified EN rows: {len(rows)}")
print(f"  + new_match_agree    : {len(new_match_agree)}  (would now be FREE rule classifications)")
print(f"  ! new_match_disagree : {len(new_match_disagree)}  (rule label differs from Haiku — review)")
print(f"  ~ no_match           : {len(no_match)}  (still Haiku — expected for ambiguous)")
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
        print(f"  [{rule_name}] {sym}: Haiku={hs}/{hc}  Rule={ns}/{nc}")
        print(f"    headline: {headline[:95]}")
    if len(new_match_disagree) > 20:
        print(f"  ... and {len(new_match_disagree) - 20} more")
