"""Follow-up to probe_industry_endpoint.py.

Previous probe showed every `industry=<single>` shape returns the same 2701
items as NO_FILTER — i.e. the param is silently dropped. Question: does
passing BOTH industries together (comma, repeated, array) change anything,
or does the firehose stay identical?
"""

from __future__ import annotations

import time
from datetime import date

import httpx

BASE_URL = "https://www.set.or.th/api/set/news/search"
WARMUP_URL = "https://www.set.or.th/en/market/news-and-alert/news"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
HEADERS = {
    "User-Agent": UA,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9,th;q=0.8",
    "Referer": WARMUP_URL,
    "Origin": "https://www.set.or.th",
}

FROM_DATE = date(2026, 5, 1)
TO_DATE = date(2026, 5, 12)
fmt = lambda d: d.strftime("%d/%m/%Y")
BASE = {"lang": "en", "fromDate": fmt(FROM_DATE), "toDate": fmt(TO_DATE)}

# Candidate shapes for "both industries at once".
PROBES: list[tuple[str, list[tuple[str, str]]]] = [
    ("NO_FILTER (baseline)",                   list(BASE.items())),
    ("industry=AGRO (single)",                 list(BASE.items()) + [("industry", "AGRO")]),
    ("industry=PROPCON (single)",              list(BASE.items()) + [("industry", "PROPCON")]),
    ("industry=AGRO,PROPCON (comma)",          list(BASE.items()) + [("industry", "AGRO,PROPCON")]),
    ("industry=AGRO|PROPCON (pipe)",           list(BASE.items()) + [("industry", "AGRO|PROPCON")]),
    ("industry=AGRO&industry=PROPCON (repeat)", list(BASE.items()) + [("industry", "AGRO"), ("industry", "PROPCON")]),
    ("industry[]=AGRO&industry[]=PROPCON",     list(BASE.items()) + [("industry[]", "AGRO"), ("industry[]", "PROPCON")]),
    ("industries=AGRO,PROPCON",                list(BASE.items()) + [("industries", "AGRO,PROPCON")]),
]


def warmup(c: httpx.Client) -> None:
    c.get("https://www.set.or.th/")
    c.get(WARMUP_URL)


def run() -> None:
    print(f"=== combined-industry probe @ {FROM_DATE} .. {TO_DATE} ===\n")
    with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=20.0) as c:
        warmup(c)
        baseline_ids: set[str] | None = None
        for label, params in PROBES:
            r = c.get(BASE_URL, params=params, timeout=30.0)
            if r.status_code != 200:
                print(f"  [{label:<42s}] HTTP {r.status_code}")
                time.sleep(0.7)
                continue
            try:
                body = r.json()
            except Exception:
                print(f"  [{label:<42s}] non-JSON")
                time.sleep(0.7)
                continue
            items = body.get("newsInfoList") or body.get("data") or body.get("items") or []
            ids = {str(it.get("id") or it.get("newsId") or "") for it in items}
            if baseline_ids is None:
                baseline_ids = ids
                delta_note = "(baseline)"
            else:
                diff = ids ^ baseline_ids
                if not diff:
                    delta_note = "identical to baseline"
                else:
                    only_here = ids - baseline_ids
                    only_baseline = baseline_ids - ids
                    delta_note = f"DIFFERENT: +{len(only_here)} -{len(only_baseline)}"
            print(f"  [{label:<42s}] items={len(items):<5d}  {delta_note}")
            time.sleep(0.7)


if __name__ == "__main__":
    run()
