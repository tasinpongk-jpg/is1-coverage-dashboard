#!/usr/bin/env python3
"""Build data/sec-onereport.json from the SEC Open API One Report endpoints.

Source : https://api.sec.or.th/v1/one-report/*   (see docs/sec-open-api.md)
Key    : env SEC_API_KEY  (never committed)

Why this snapshot exists
------------------------
One Report is the only *structured* annual filing SEC publishes per issuer.
It carries four things the dashboard has no other machine-readable source for:

  revenue by business segment  -> feeds the sector-alignment review
  auditor + audit / non-audit fee -> auditor change + fee-ratio surveillance
  AGM date + board meeting counts -> governance cadence flags
  board composition (independent / exec / gender split)

Everything here is annual and lags the SET filing feed by months. It is a
cross-check layer, not a timeliness layer.

The join key
------------
SEC identifies issuers by unique_id (e.g. C0000000013), not by SET ticker.
Endpoint 01-SBO-Info returns report_year + unique_id + symbol for every
issuer, so it is called first and cached as the ticker -> unique_id map.
A ticker with no unique_id for the requested year is reported, not guessed.

Usage
-----
  export SEC_API_KEY=...
  python3 scripts/build_sec_onereport.py --year 2024
  python3 scripts/build_sec_onereport.py --year 2024 --tickers CPN,WHA,ITC
  python3 scripts/build_sec_onereport.py --year 2024 --datasets product_income,auditor
  python3 scripts/build_sec_onereport.py --year 2024 --map-only   # just the id map

Calls: 1 + (len(datasets) x len(tickers)). The default set over the full
232-ticker universe is ~930 calls, inside the 3,000 / 300 s window.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sec_api import get_v1, SecApiError  # noqa: E402

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TICKERS = os.path.join(REPO, "data", "tickers.json")
OUT = os.path.join(REPO, "data", "sec-onereport.json")

# dataset key -> (path template, what it is)
DATASETS = {
    "product_income": ("/v1/one-report/sbo/{year}/product_income/{uid}",
                       "revenue by business segment, 3 years + % share"),
    "export_income":  ("/v1/one-report/sbo/{year}/export_income/{uid}",
                       "domestic vs export revenue split"),
    "auditor":        ("/v1/one-report/cgs/{year}/auditor_company/{uid}",
                       "audit firm, audit fee, non-audit fee"),
    "director_perf":  ("/v1/one-report/cgs/{year}/director_performance/{uid}",
                       "AGM date, board / audit committee meeting counts"),
    "board":          ("/v1/one-report/cgs/{year}/board/{uid}",
                       "board headcount, independent / exec / gender split"),
    "rd":             ("/v1/one-report/sbo/{year}/rd/{uid}",
                       "R&D spend, 3 years"),
    "risk":           ("/v1/one-report/sbo/{year}/risk/{uid}",
                       "declared risk factors"),
    "financials":     ("/v1/one-report/fs/{year}/financial_statement/{uid}",
                       "full FS line items by set_code — large, off by default"),
    "bods":           ("/v1/one-report/cgs/{year}/bods/{uid}",
                       "board roster, one row per director"),
    "executives":     ("/v1/one-report/cgs/{year}/executives/{uid}",
                       "executive roster"),
}
DEFAULT_DATASETS = ["product_income", "auditor", "director_perf", "board"]


def load_universe(only=None):
    with open(TICKERS, encoding="utf-8") as fh:
        rows = json.load(fh)["tickers"]
    meta = {r["tk"]: {"sector": r.get("sector"), "rm": r.get("rm"),
                      "bucket": r.get("bucket")} for r in rows}
    if only:
        want = [t.strip().upper() for t in only if t.strip()]
        missing = [t for t in want if t not in meta]
        if missing:
            print(f"  ! not in data/tickers.json: {', '.join(missing)}", file=sys.stderr)
        meta = {t: meta[t] for t in want if t in meta}
    return meta


def build_id_map(year, language="T"):
    """symbol -> {unique_id, corp_name, business_type, ...} for the given year."""
    rows = get_v1(f"/v1/one-report/sbo/{year}/info/{language}")
    out = {}
    for r in rows:
        sym = (r.get("symbol") or "").strip().upper()
        if not sym:
            continue
        # A ticker can appear more than once (amended filings). Keep the row
        # with the latest last_upd_date — string ISO8601 sorts correctly.
        prev = out.get(sym)
        if prev and (prev.get("last_upd_date") or "") >= (r.get("last_upd_date") or ""):
            continue
        out[sym] = r
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", required=True, help="One Report year, AD (e.g. 2024)")
    ap.add_argument("--language", default="T", choices=["T", "E"])
    ap.add_argument("--tickers", help="comma-separated subset; default = all of data/tickers.json")
    ap.add_argument("--datasets", default=",".join(DEFAULT_DATASETS),
                    help=f"comma-separated. available: {', '.join(DATASETS)}")
    ap.add_argument("--map-only", action="store_true",
                    help="resolve ticker -> unique_id and stop (1 API call)")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()

    datasets = [d.strip() for d in a.datasets.split(",") if d.strip()]
    unknown = [d for d in datasets if d not in DATASETS]
    if unknown:
        raise SystemExit(f"unknown dataset(s): {', '.join(unknown)}. "
                         f"available: {', '.join(DATASETS)}")

    universe = load_universe(a.tickers.split(",") if a.tickers else None)
    print(f"Universe: {len(universe)} tickers | year {a.year} | datasets {datasets}")

    print("Resolving ticker -> unique_id via 01-SBO-Info ...")
    id_map = build_id_map(a.year, a.language)
    print(f"  SEC returned {len(id_map)} symbols for report_year {a.year}")

    resolved = {t: id_map[t] for t in universe if t in id_map}
    unresolved = sorted(t for t in universe if t not in id_map)
    print(f"  matched {len(resolved)}/{len(universe)}; unmatched: {len(unresolved)}")
    if unresolved:
        print(f"  unmatched -> {', '.join(unresolved)}")

    if a.map_only:
        for tk in sorted(resolved):
            print(f"  {tk:10s} {resolved[tk]['unique_id']}  {resolved[tk].get('corp_name','')}")
        return

    companies, errors = {}, []
    for i, tk in enumerate(sorted(resolved), 1):
        info = resolved[tk]
        uid = info["unique_id"]
        rec = {
            "ticker": tk,
            "unique_id": uid,
            "corp_name": info.get("corp_name"),
            "business_type": info.get("business_type"),
            "registered_number": info.get("registered_number"),
            "province": info.get("province"),
            "website": info.get("website"),
            "common_paidup_share": info.get("common_paidup_share"),
            "preferred_paidup_share": info.get("preferred_paidup_share"),
            "last_upd_date": info.get("last_upd_date"),
            **universe[tk],
        }
        for ds in datasets:
            path = DATASETS[ds][0].format(year=a.year, uid=uid)
            try:
                rec[ds] = get_v1(path)
            except SecApiError as e:
                rec[ds] = None
                errors.append({"ticker": tk, "dataset": ds,
                               "status": e.status, "path": path})
        print(f"  [{i}/{len(resolved)}] {tk:10s} {uid}  "
              + " ".join(f"{d}={len(rec[d]) if isinstance(rec[d], list) else 'ERR'}"
                         for d in datasets))
        companies[tk] = rec

    payload = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "SEC Open Data API /v1/one-report (api.sec.or.th)",
        "report_year": a.year,
        "language": a.language,
        "datasets": {d: DATASETS[d][1] for d in datasets},
        "counts": {
            "universe": len(universe),
            "resolved": len(resolved),
            "unresolved": len(unresolved),
            "errors": len(errors),
        },
        "unresolved": unresolved,
        "errors": errors,
        "companies": companies,
    }
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
    print(f"Wrote {a.out}: {payload['counts']}")


if __name__ == "__main__":
    main()
