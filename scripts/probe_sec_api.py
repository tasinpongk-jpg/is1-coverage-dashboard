#!/usr/bin/env python3
"""Ladder-test the SEC Open Data API against the IS1 universe. Read-only.

Answers, in order, the five things that decide whether anything can be built
on this API. Each rung prints PASS / FAIL / WARN and the evidence behind it.
A FAIL stops the rungs that depend on it — later rungs still run where they
are independent.

  1 KEY       does the subscription key work, on both v1 and v2?
  2 YEAR      which report_year actually has One Report data, and how much?
  3 COVERAGE  how many of the book resolve to a unique_id at that year?
  4 PAYLOAD   do the four datasets that matter return real rows per ticker?
  5 PF/REIT   do property funds and REITs appear in the v2 fund group?

Usage:
  export SEC_API_KEY=...
  python3 scripts/probe_sec_api.py                    # rm=C book (51 tickers)
  python3 scripts/probe_sec_api.py --rm all           # full 232 universe
  python3 scripts/probe_sec_api.py --years 2023,2024,2025
  python3 scripts/probe_sec_api.py --sample CPN,ITC,FTREIT
  python3 scripts/probe_sec_api.py --json out.json    # also dump raw evidence

Cost: roughly 10 + (3 x len(sample)) calls. Default run is well under 50,
against a 3,000 / 300 s limit.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sec_api import request, get_v1, paginate_v2, SecApiError  # noqa: E402

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
TICKERS = os.path.join(REPO, "data", "tickers.json")

# the four datasets the PR argues are worth pulling, plus FS as a bonus check
PROBE_DATASETS = {
    "product_income": "/v1/one-report/sbo/{year}/product_income/{uid}",
    "auditor":        "/v1/one-report/cgs/{year}/auditor_company/{uid}",
    "director_perf":  "/v1/one-report/cgs/{year}/director_performance/{uid}",
    "board":          "/v1/one-report/cgs/{year}/board/{uid}",
    "financials":     "/v1/one-report/fs/{year}/financial_statement/{uid}",
}

PF_SAMPLE = ["TTLPF", "HPF", "TIF1"]        # property funds — mutual funds
REIT_SAMPLE = ["FTREIT", "WHART", "CPNREIT"]  # trusts — may not appear at all

R = {"PASS": "PASS", "FAIL": "FAIL", "WARN": "WARN", "SKIP": "SKIP"}
results = []


def rung(n, name, verdict, detail):
    results.append({"rung": n, "name": name, "verdict": verdict, "detail": detail})
    print(f"\n[{n}] {name}: {R[verdict]}")
    for line in detail.splitlines():
        print(f"    {line}")


def load_book(rm):
    with open(TICKERS, encoding="utf-8") as fh:
        rows = json.load(fh)["tickers"]
    if rm and rm.lower() != "all":
        rows = [r for r in rows if r.get("rm") == rm]
    return {r["tk"]: r for r in rows}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rm", default="C",
                    help="RM code to scope the book, or 'all' for the 232 universe (default: C)")
    ap.add_argument("--years", default="2025,2024,2023,2022,2021",
                    help="report years to probe, newest first")
    ap.add_argument("--sample", help="comma-separated tickers for rung 4; "
                                     "default = one from each bucket in the book")
    ap.add_argument("--language", default="T", choices=["T", "E"])
    ap.add_argument("--json", help="write the raw evidence to this path")
    a = ap.parse_args()

    if not (os.environ.get("SEC_API_KEY") or os.environ.get("SEC_API_KEY_SECONDARY")):
        print("[1] KEY: FAIL\n    SEC_API_KEY is not set in this shell.\n"
              "    export SEC_API_KEY=<primary key>   # and re-run")
        sys.exit(1)

    book = load_book(a.rm)
    scope = f"rm={a.rm}" if a.rm.lower() != "all" else "full universe"
    print(f"SEC Open Data API probe — {scope}, {len(book)} tickers")
    print(f"base: {os.environ.get('SEC_API_BASE', 'https://api.sec.or.th')}")

    evidence = {"generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "scope": scope, "book_size": len(book)}

    # ---- rung 1: key -------------------------------------------------------
    v1_ok = v2_ok = False
    lines = []
    try:
        d = request("/v2/fund/general-info/amcs", {"page_size": 1})
        n = len((d or {}).get("items") or [])
        v2_ok = True
        lines.append(f"v2 /v2/fund/general-info/amcs -> {n} item(s), "
                     f"keys={sorted((d or {}).keys())}")
    except Exception as e:  # noqa: BLE001
        lines.append(f"v2 /v2/fund/general-info/amcs -> {e}")
    try:
        raw = request(f"/v1/one-report/sbo/{a.years.split(',')[0]}/info/{a.language}")
        shape = ("bare array" if isinstance(raw, list)
                 else f"wrapped dict, keys={sorted(raw.keys())}" if isinstance(raw, dict)
                 else type(raw).__name__)
        v1_ok = True
        lines.append(f"v1 /v1/one-report/sbo/.../info/{a.language} -> {shape}")
        evidence["v1_shape"] = shape
    except Exception as e:  # noqa: BLE001
        lines.append(f"v1 /v1/one-report/sbo/.../info/{a.language} -> {e}")

    rung(1, "KEY", "PASS" if (v1_ok and v2_ok) else
         "WARN" if (v1_ok or v2_ok) else "FAIL", "\n".join(lines))

    if not v1_ok and not v2_ok:
        print("\nKey rejected on both shapes. Nothing below can run. "
              "Check SEC_API_KEY, then the subscription's product-group access.")
        return _finish(a, evidence)

    # ---- rung 2: which year has data --------------------------------------
    year_counts, best_year, id_map = {}, None, {}
    if v1_ok:
        lines = []
        for y in [y.strip() for y in a.years.split(",") if y.strip()]:
            try:
                rows = get_v1(f"/v1/one-report/sbo/{y}/info/{a.language}")
                syms = {(r.get("symbol") or "").strip().upper() for r in rows}
                syms.discard("")
                year_counts[y] = len(syms)
                lines.append(f"{y}: {len(rows):5d} rows, {len(syms):5d} distinct symbols")
                if len(syms) > 0 and best_year is None:
                    best_year, id_map = y, {}
                    for r in rows:
                        s = (r.get("symbol") or "").strip().upper()
                        if not s:
                            continue
                        prev = id_map.get(s)
                        if prev and (prev.get("last_upd_date") or "") >= (r.get("last_upd_date") or ""):
                            continue
                        id_map[s] = r
            except SecApiError as e:
                year_counts[y] = f"HTTP {e.status}"
                lines.append(f"{y}: HTTP {e.status}")
            except Exception as e:  # noqa: BLE001
                year_counts[y] = str(e)
                lines.append(f"{y}: {e}")
        if best_year:
            lines.append(f"-> newest year with data: {best_year}")
        rung(2, "YEAR", "PASS" if best_year else "FAIL", "\n".join(lines))
    else:
        rung(2, "YEAR", "SKIP", "v1 unavailable")
    evidence["year_counts"] = year_counts
    evidence["best_year"] = best_year

    # ---- rung 3: coverage of the book -------------------------------------
    resolved, unresolved = {}, []
    if best_year:
        resolved = {t: id_map[t] for t in book if t in id_map}
        unresolved = sorted(t for t in book if t not in id_map)
        pct = 100.0 * len(resolved) / len(book) if book else 0
        lines = [f"report_year {best_year}: {len(resolved)}/{len(book)} resolved ({pct:.1f}%)"]
        by_bucket = {}
        for t in book:
            b = book[t].get("bucket") or "?"
            hit, tot = by_bucket.get(b, (0, 0))
            by_bucket[b] = (hit + (1 if t in id_map else 0), tot + 1)
        for b in sorted(by_bucket):
            hit, tot = by_bucket[b]
            lines.append(f"  {b:8s} {hit:3d}/{tot:3d}")
        if unresolved:
            lines.append(f"unresolved: {', '.join(unresolved)}")
            lines.append("(a PF&REIT miss here is expected — funds and trusts do not "
                         "file a One Report)")
        rung(3, "COVERAGE", "PASS" if pct >= 80 else "WARN" if pct > 0 else "FAIL",
             "\n".join(lines))
        evidence["resolved"] = {t: resolved[t].get("unique_id") for t in resolved}
        evidence["unresolved"] = unresolved
    else:
        rung(3, "COVERAGE", "SKIP", "no usable report year")

    # ---- rung 4: do the datasets carry rows --------------------------------
    if resolved:
        if a.sample:
            sample = [s.strip().upper() for s in a.sample.split(",") if s.strip()]
        else:  # one resolved ticker per bucket
            sample, seen = [], set()
            for t in sorted(resolved):
                b = book[t].get("bucket")
                if b not in seen:
                    seen.add(b)
                    sample.append(t)
        sample = [t for t in sample if t in resolved]
        lines, payload, any_rows = [], {}, False
        for tk in sample:
            uid = resolved[tk]["unique_id"]
            row = {}
            bits = []
            for ds, tmpl in PROBE_DATASETS.items():
                try:
                    got = get_v1(tmpl.format(year=best_year, uid=uid))
                    row[ds] = got
                    bits.append(f"{ds}={len(got)}")
                    if got:
                        any_rows = True
                except SecApiError as e:
                    row[ds] = None
                    bits.append(f"{ds}=HTTP{e.status}")
            payload[tk] = row
            lines.append(f"{tk:9s} {uid:12s} " + "  ".join(bits))
        # show one concrete revenue row, so the numbers are visible not implied
        for tk in sample:
            pi = (payload.get(tk) or {}).get("product_income") or []
            if pi:
                r0 = pi[0]
                lines.append(f"sample {tk} product_income[0]: "
                             f"{r0.get('business_income_desc')} = "
                             f"{r0.get('asof_year')} ({r0.get('asof_year_percent')}%)")
                break
        rung(4, "PAYLOAD", "PASS" if any_rows else "FAIL", "\n".join(lines))
        evidence["payload"] = payload
    else:
        rung(4, "PAYLOAD", "SKIP", "nothing resolved")

    # ---- rung 5: PF vs REIT in the fund group ------------------------------
    if v2_ok:
        lines, fundhits = [], {}
        for label, names in (("PF  ", PF_SAMPLE), ("REIT", REIT_SAMPLE)):
            for nm in names:
                try:
                    items = list(paginate_v2("/v2/fund/general-info/profiles",
                                             {"project_info": nm},
                                             page_size=20, max_pages=1))
                    fundhits[nm] = [{"proj_id": i.get("proj_id"),
                                     "proj_abbr_name": i.get("proj_abbr_name"),
                                     "proj_name_en": i.get("proj_name_en"),
                                     "fund_status": i.get("fund_status")} for i in items[:3]]
                    if items:
                        i0 = items[0]
                        lines.append(f"{label} {nm:9s} {len(items)} hit(s) -> "
                                     f"proj_id={i0.get('proj_id')} "
                                     f"abbr={i0.get('proj_abbr_name')} "
                                     f"status={i0.get('fund_status')}")
                    else:
                        lines.append(f"{label} {nm:9s} 0 hits")
                except SecApiError as e:
                    fundhits[nm] = f"HTTP {e.status}"
                    lines.append(f"{label} {nm:9s} HTTP {e.status}")
        pf_hit = any(isinstance(fundhits.get(n), list) and fundhits[n] for n in PF_SAMPLE)
        reit_hit = any(isinstance(fundhits.get(n), list) and fundhits[n] for n in REIT_SAMPLE)
        lines.append(f"-> property funds in /v2/fund: {'yes' if pf_hit else 'no'}; "
                     f"REITs in /v2/fund: {'yes' if reit_hit else 'no'}")
        if pf_hit and not reit_hit:
            lines.append("   as expected: PFs are SEC-registered mutual funds, "
                         "REITs are trusts and sit outside this group")
        rung(5, "PF/REIT", "PASS" if pf_hit else "WARN",
             "\n".join(lines))
        evidence["fund_lookup"] = fundhits
    else:
        rung(5, "PF/REIT", "SKIP", "v2 unavailable")

    _finish(a, evidence)


def _finish(a, evidence):
    print("\n" + "=" * 64)
    for r in results:
        print(f"  [{r['rung']}] {r['name']:9s} {R[r['verdict']]}")
    evidence["results"] = results
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump(evidence, fh, ensure_ascii=False, indent=1)
        print(f"\nraw evidence -> {a.json}")
    bad = [r for r in results if r["verdict"] == "FAIL"]
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
