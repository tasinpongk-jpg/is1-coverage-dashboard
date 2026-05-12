"""Probe whether SET's public news/search endpoint exposes an industry-level
filter that returns the document types the per-symbol query drops.

Background — issue #12 (2026-05-12):
    The current poller in surveillance/client.py calls
        https://www.set.or.th/api/set/news/search?symbol=X
    per ticker. SETSMART export cross-check proved this endpoint silently
    omits PFREIT distributions, NAV reports, dividend payments, share
    repurchase notices, and "No Right Adjustment" notices — 12.3% miss rate
    overall, 100% on some doc types.

    Hypothesis: the SAME endpoint, queried by industry instead of symbol,
    returns the superset that SETSMART's "Index/Industry/Sector = AGRO/PROPCON"
    filter produces. This script proves or disproves that.

Coverage is 2 SET industries only — AGRO (AGRI+FOOD) and PROPCON
(PROP+CONMAT+CONS+PFREIT). See [[set-industry-mapping]] memory.

Smoking-gun IDs (from issue #12 comment) that the per-symbol poll missed:
    AGRO       TFG    104149800  Payment of Interim Dividend
    AGRO       TFG    104149900  No Right Adjustment of TFG-W4
    PROPCON    WHAIR  104113400  Report on NAV per unit
    PROPCON    WHAIR  104113500  Reviewed financial performance F45 (lowercase)
    PROPCON    WHAIR  104116100  Notification of distribution
    PROPCON    WHAIR  104129500  Notification of resolutions of the BoD

If the industry-walk recovers these 6, we ship Layer 2 (rewrite poll.py).

Run from repo root:
    python scripts/probe_industry_endpoint.py

Requires Incapsula cookie warmup to work — must be run from a machine that
can reach set.or.th normally (local laptop is fine, GHA runner is fine).
"""

from __future__ import annotations

import json
import sys
import time
from datetime import date
from typing import Any

import httpx

# ---- config ---------------------------------------------------------------

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
    "sec-ch-ua": '"Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
}

# Window that overlaps the smoking-gun IDs in issue #12 (filed 2026-05-11).
FROM_DATE = date(2026, 5, 1)
TO_DATE = date(2026, 5, 12)

# (symbol, news_id, doc_type, industry)
SMOKING_GUN_IDS: list[tuple[str, str, str, str]] = [
    ("TFG",   "104149800",      "Payment of Interim Dividend",        "AGRO"),
    ("TFG",   "104149900",      "No Right Adjustment of TFG-W4",      "AGRO"),
    ("WHAIR", "104113400",      "Report on NAV per unit",             "PROPCON"),
    ("WHAIR", "104113500",      "Reviewed financial performance F45", "PROPCON"),
    ("WHAIR", "104116100",      "Notification of distribution",       "PROPCON"),
    ("WHAIR", "104129500",      "BoD resolutions",                    "PROPCON"),
]

INDUSTRIES = ["AGRO", "PROPCON"]

# Candidate params to try. SET's portal isn't publicly documented for this
# filter, so we have to brute-force the spelling. First hit wins per industry.
def candidate_params(industry: str, from_d: date, to_d: date) -> list[tuple[str, dict[str, str]]]:
    fmt = lambda d: d.strftime("%d/%m/%Y")
    base = {"lang": "en", "fromDate": fmt(from_d), "toDate": fmt(to_d)}
    return [
        ("industry=<ind>",                     {**base, "industry": industry}),
        ("sectorIndustry=<ind>",               {**base, "sectorIndustry": industry}),
        ("industryCode=<ind>",                 {**base, "industryCode": industry}),
        ("industryId=<ind>",                   {**base, "industryId": industry}),
        ("searchBy=industry&value=<ind>",      {**base, "searchBy": "industry", "value": industry}),
        ("searchBy=INDUSTRY&filter=<ind>",     {**base, "searchBy": "INDUSTRY", "filter": industry}),
        ("keyword=<ind>",                      {**base, "keyword": industry}),
        ("group=industry&industry=<ind>",      {**base, "group": "industry", "industry": industry}),
        # No filter — full news firehose for the window. Always last; useful
        # as a fallback "we can post-filter" capture-rate measure.
        ("NO_FILTER",                          base),
    ]


def warmup(client: httpx.Client) -> None:
    """Touch the SPA root + the news page so Imperva sets cookies. Idempotent."""
    print("[warmup] GET /", flush=True)
    r = client.get("https://www.set.or.th/")
    print(f"[warmup]   -> {r.status_code}, cookies={len(client.cookies)}", flush=True)
    print(f"[warmup] GET {WARMUP_URL}", flush=True)
    r = client.get(WARMUP_URL)
    print(f"[warmup]   -> {r.status_code}, cookies={len(client.cookies)}", flush=True)
    if r.status_code != 200:
        print("[warmup] WARNING: warmup did not return 200 — Incapsula may still block.", flush=True)


def call(client: httpx.Client, label: str, params: dict[str, str]) -> dict[str, Any]:
    """Return a probe-result dict. Never raises; records errors instead."""
    t0 = time.monotonic()
    try:
        r = client.get(BASE_URL, params=params, timeout=30.0)
    except Exception as e:
        return {"label": label, "params": params, "ok": False, "error": f"{type(e).__name__}: {e}"}
    dt = time.monotonic() - t0
    out: dict[str, Any] = {
        "label": label,
        "params": params,
        "status": r.status_code,
        "elapsed_s": round(dt, 2),
        "url": str(r.url),
    }
    if r.status_code != 200:
        out["ok"] = False
        out["error"] = f"HTTP {r.status_code}"
        out["body_head"] = r.text[:200]
        return out
    try:
        body = r.json()
    except Exception as e:
        out["ok"] = False
        out["error"] = f"non-JSON: {type(e).__name__}: {e}"
        out["body_head"] = r.text[:200]
        return out
    items = body.get("newsInfoList") or body.get("data") or body.get("items") or []
    out["ok"] = True
    out["item_count"] = len(items)
    out["sample"] = []
    for it in items[:3]:
        out["sample"].append({
            "id": str(it.get("id") or it.get("newsId") or ""),
            "symbol": it.get("symbol") or "",
            "datetime": it.get("datetime") or it.get("publishDate") or "",
            "headline": (it.get("headline") or it.get("title") or "")[:100],
        })
    # Did this response include the smoking-gun IDs we expected for this industry?
    ids_returned = {str(it.get("id") or it.get("newsId") or "") for it in items}
    out["_ids_returned"] = ids_returned
    return out


def main() -> int:
    print(f"=== probe industry endpoint @ {FROM_DATE} .. {TO_DATE} ===\n")
    with httpx.Client(headers=HEADERS, follow_redirects=True, timeout=20.0) as client:
        warmup(client)
        # Light pause between requests to stay below SET's ~10 req/s threshold.
        all_results: list[dict[str, Any]] = []
        for industry in INDUSTRIES:
            print(f"\n--- industry: {industry} ---")
            for label, params in candidate_params(industry, FROM_DATE, TO_DATE):
                effective_label = label.replace("<ind>", industry)
                res = call(client, effective_label, params)
                res["_industry"] = industry
                all_results.append(res)
                if res["ok"]:
                    print(
                        f"  [{effective_label:<40s}] "
                        f"{res['status']}  items={res['item_count']:<5d} "
                        f"({res['elapsed_s']}s)"
                    )
                else:
                    print(
                        f"  [{effective_label:<40s}] "
                        f"FAIL: {res.get('error', '?')[:60]}"
                    )
                time.sleep(0.7)

    # ---- capture-rate analysis ---------------------------------------------
    print("\n\n=== smoking-gun ID capture per probe ===")
    expected_by_industry: dict[str, set[str]] = {"AGRO": set(), "PROPCON": set()}
    for _, news_id, _, industry in SMOKING_GUN_IDS:
        expected_by_industry[industry].add(news_id)

    print(f"{'probe':<45s} {'industry':<10s} {'items':>6s} {'hits':>5s} {'/':>2s} {'exp':>3s}")
    best: dict[str, dict[str, Any]] = {}  # industry -> best probe
    for res in all_results:
        if not res.get("ok"):
            continue
        industry = res["_industry"]
        expected = expected_by_industry[industry]
        hit = res["_ids_returned"] & expected
        line = (
            f"  {res['label']:<43s} {industry:<10s} "
            f"{res['item_count']:>6d} {len(hit):>5d}  /  {len(expected):>3d}"
        )
        print(line)
        cur = best.get(industry)
        if cur is None or len(hit) > len(cur["_hits"]):
            best[industry] = {**res, "_hits": hit}

    # ---- verdict -----------------------------------------------------------
    print("\n\n=== verdict ===")
    all_recovered = True
    for industry, expected in expected_by_industry.items():
        b = best.get(industry)
        if b is None:
            print(f"  {industry}: NO probe succeeded. Likely all 4xx / no JSON.")
            all_recovered = False
            continue
        hit = b["_hits"]
        missing = expected - hit
        rate = len(hit) / len(expected) if expected else 0.0
        ok_mark = "PASS" if not missing else "PARTIAL" if hit else "FAIL"
        print(
            f"  {industry}: {ok_mark}  "
            f"best probe = '{b['label']}'  "
            f"({len(hit)}/{len(expected)} smoking-gun IDs recovered, "
            f"{b['item_count']} total items)"
        )
        if missing:
            print(f"    missing IDs: {sorted(missing)}")
            all_recovered = False

    print("\nWrite full result dump to:")
    out_path = "scripts/probe_industry_endpoint_result.json"
    # Serialise — drop sets first.
    dump = []
    for res in all_results:
        r2 = {k: v for k, v in res.items() if k not in ("_ids_returned",)}
        r2["_hit_count"] = len(res.get("_ids_returned", set()))
        dump.append(r2)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(dump, fh, indent=2, default=str)
    print(f"  {out_path}\n")

    return 0 if all_recovered else 1


if __name__ == "__main__":
    sys.exit(main())
