#!/usr/bin/env python3
"""Build data/sec-bonds.json from the SEC-Bonds vault notes.

Source: SEC Open API (/v2/bond/*), materialised by setlake-sec-bond as one
markdown note per IS1 coverage ticker under
  Work-SET/Listed Company/1-Raw/06-Market-Data/SEC-Bonds/

Each note carries YAML frontmatter (ticker, company, sector, rm, counts, ...)
plus an "Outstanding bonds" markdown table. We parse both into a single JSON
the bond-data-sec.html page consumes. No external deps (no PyYAML needed).

Usage:
  python3 scripts/build_sec_bonds.py [SEC_BONDS_DIR]
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

DEFAULT_SRC = os.path.expanduser(
    "~/Library/CloudStorage/OneDrive2-TheStockExchangeofThailand/Claude-Vault/"
    "Work-SET/Listed Company/1-Raw/06-Market-Data/SEC-Bonds"
)
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "sec-bonds.json")

# notes that are not per-ticker issuer notes
SKIP = {"_Bond Coverage Map", "DASHBOARD"}


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    fm, body = {}, text[m.end():]
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip()
        if v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        elif v.startswith("[") and v.endswith("]"):
            v = [t.strip() for t in v[1:-1].split(",") if t.strip()]
        fm[k] = v
    return fm, body


def num(v, cast=float):
    try:
        return cast(str(v).replace(",", "").strip())
    except (ValueError, TypeError):
        return None


def parse_bonds(body):
    """Pull rows out of the 'Outstanding bonds' markdown table."""
    bonds = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 7:
            continue
        # skip header + separator rows
        if cells[0] in ("bond_id", "") or set(cells[0]) <= set("-: "):
            continue
        bonds.append({
            "bondId": cells[0],
            "isin": cells[1],
            "type": cells[2],
            "maturity": cells[3],
            "valueM": num(cells[4]),
            "ccy": cells[5],
            "rating": cells[6],
        })
    return bonds


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SRC
    if not os.path.isdir(src):
        sys.exit(f"SEC-Bonds dir not found: {src}")

    issuers = []
    for fn in sorted(os.listdir(src)):
        if not fn.endswith(".md") or fn[:-3] in SKIP:
            continue
        fm, body = parse_frontmatter(open(os.path.join(src, fn), encoding="utf-8").read())
        if not fm.get("ticker"):
            continue
        issuers.append({
            "ticker": fm.get("ticker"),
            "companyId": fm.get("company_id"),
            "company": fm.get("company_name"),
            "sector": fm.get("sector"),
            "rm": fm.get("rm"),
            "bondsTotal": num(fm.get("bonds_total"), int) or 0,
            "bondsOutstanding": num(fm.get("bonds_outstanding"), int) or 0,
            "outstandingThbBn": num(fm.get("outstanding_thb_bn")) or 0.0,
            "esgBonds": num(fm.get("esg_bonds"), int) or 0,
            "asOf": fm.get("as_of"),
            "bonds": parse_bonds(body),
        })

    # ----- aggregates -----
    with_bonds = [i for i in issuers if i["bondsOutstanding"] > 0]
    summary = {
        "tickers": len(issuers),
        "issuersWithBonds": len(with_bonds),
        "outstandingBonds": sum(i["bondsOutstanding"] for i in issuers),
        "outstandingThbBn": round(sum(i["outstandingThbBn"] for i in issuers), 2),
        "esgBonds": sum(i["esgBonds"] for i in issuers),
    }

    def group(key):
        g = {}
        for i in with_bonds:
            k = i.get(key) or "—"
            d = g.setdefault(k, {"issuers": 0, "bonds": 0, "thbBn": 0.0})
            d["issuers"] += 1
            d["bonds"] += i["bondsOutstanding"]
            d["thbBn"] += i["outstandingThbBn"]
        return {k: {**v, "thbBn": round(v["thbBn"], 2)} for k, v in
                sorted(g.items(), key=lambda kv: -kv[1]["thbBn"])}

    rating_mix = {}
    for i in issuers:
        for b in i["bonds"]:
            rating_mix[b["rating"]] = rating_mix.get(b["rating"], 0) + 1
    rating_mix = dict(sorted(rating_mix.items(), key=lambda kv: -kv[1]))

    as_of = max((i["asOf"] for i in issuers if i.get("asOf")), default=None)
    out = {
        "version": 1,
        "asOf": as_of,
        "_built_at": datetime.now(timezone.utc).isoformat(),
        "source": "SEC Open API /v2/bond/*",
        "generatedBy": "build_sec_bonds.py",
        "summary": summary,
        "byRM": group("rm"),
        "bySector": group("sector"),
        "ratingMix": rating_mix,
        "issuers": sorted(issuers, key=lambda i: -i["outstandingThbBn"]),
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Wrote {OUT}: {summary['tickers']} tickers, "
          f"{summary['issuersWithBonds']} issuers, "
          f"{summary['outstandingBonds']} bonds, "
          f"THB {summary['outstandingThbBn']:.1f} bn outstanding")


if __name__ == "__main__":
    main()
