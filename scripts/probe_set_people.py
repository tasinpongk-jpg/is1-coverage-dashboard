#!/usr/bin/env python3
"""Read-only probe: which SET API endpoints carry the board and the major
shareholders shown on the factsheet page, and what shape they return.

Discovery first (the factsheet page's own JS bundles name the API paths it
calls), then a call per candidate path for a few tickers. Prints status, top
level keys and a short sample. Writes nothing. Run in CI, where set.or.th is
reachable:  python scripts/probe_set_people.py
"""
import json
import re
import sys
import time

import httpx

sys.path.insert(0, "scripts")
from build_ticker_summary import SET_BASE, SET_HEADERS  # noqa: E402

TICKERS = ["AWC", "CPN", "PRG", "FTREIT"]   # a PROP, a big PROP, a FOOD, a REIT
CANDIDATES = [
    "/api/set/stock/{s}/shareholder?lang={l}",
    "/api/set/stock/{s}/major-shareholder?lang={l}",
    "/api/set/company/{s}/board-of-director?lang={l}",
    "/api/set/company/{s}/board-of-directors?lang={l}",
    "/api/set/company/{s}/management?lang={l}",
    "/api/set/company/{s}/profile?lang={l}",
    "/api/set/stock/{s}/profile?lang={l}",
]


def shape(obj, depth=0):
    if isinstance(obj, dict):
        return {k: shape(v, depth + 1) if depth < 1 else type(v).__name__ for k, v in obj.items()}
    if isinstance(obj, list):
        return [f"list[{len(obj)}]", shape(obj[0], depth + 1) if obj else None]
    return type(obj).__name__


def main():
    page_hdrs = {**SET_HEADERS, "Accept": "text/html,application/xhtml+xml,*/*"}
    with httpx.Client(follow_redirects=True, timeout=20) as c:
        # Warm cookies the same way build_ticker_summary does.
        for u in [SET_BASE + "/", SET_BASE + "/th/market/product/stock/quote/AWC/factsheet"]:
            try:
                r = c.get(u, headers=page_hdrs)
                print(f"WARMUP {r.status_code} {u} ({len(r.text)} chars)")
            except Exception as e:
                print(f"WARMUP ERR {u}: {e}")
        html = r.text if r is not None else ""

        # 1. Discovery: API paths named in the page and its JS bundles.
        found = set(re.findall(r"/api/set/[A-Za-z0-9_\-/{}$.]+", html))
        bundles = sorted(set(re.findall(r'(?:src|href)="(/_nuxt/[^"]+\.js)"', html)))
        print(f"\nDISCOVERY: {len(bundles)} JS bundles referenced by the factsheet page")
        for b in bundles[:60]:
            try:
                js = c.get(SET_BASE + b, headers={**SET_HEADERS, "Accept": "*/*"}).text
                found |= set(re.findall(r"/api/set/[A-Za-z0-9_\-/{}$.]+", js))
                found |= {m for m in re.findall(r'["`](/?(?:stock|company|factsheet)/\$\{[^}]+\}/[A-Za-z0-9_\-/]+)', js)}
            except Exception as e:
                print(f"  bundle ERR {b}: {e}")
        interesting = sorted(p for p in found if re.search(r"share|holder|board|director|manage|people|executive", p, re.I))
        print("API paths mentioning shareholder / board / director / management:")
        for p in interesting:
            print("  ", p)
        print(f"({len(found)} API-like paths found in total)")

        # 2. Candidate calls.
        for tk in TICKERS:
            ref = {**SET_HEADERS, "Referer": f"{SET_BASE}/th/market/product/stock/quote/{tk}/factsheet"}
            for tmpl in CANDIDATES:
                for lang in ("en", "th"):
                    path = tmpl.format(s=tk, l=lang)
                    time.sleep(0.35)
                    try:
                        r = c.get(SET_BASE + path, headers=ref)
                    except Exception as e:
                        print(f"\n{tk} {path} ERR {e}")
                        continue
                    print(f"\n{tk} {r.status_code} {path}")
                    if r.status_code != 200:
                        continue
                    try:
                        d = r.json()
                    except Exception:
                        print("  not JSON:", r.text[:200].replace("\n", " "))
                        continue
                    print("  shape:", json.dumps(shape(d), ensure_ascii=False)[:900])
                    print("  sample:", json.dumps(d, ensure_ascii=False)[:1500])
                    if lang == "en" and "profile" in path:
                        break  # the profile shape is the same in both languages


if __name__ == "__main__":
    main()
