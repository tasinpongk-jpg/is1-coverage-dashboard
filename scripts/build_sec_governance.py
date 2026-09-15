#!/usr/bin/env python3
"""Build data/sec-governance.json — the auditor / governance screen.

Source : SEC Open API /v1/one-report/cgs/*  (see docs/sec-open-api.md)
Key    : env SEC_API_KEY  (never committed)
Page   : governance-screen.html

Why a separate builder from build_sec_onereport.py
--------------------------------------------------
The screen needs TWO report years, not one: auditor change is only visible by
comparing the audit firm named this year against last year. build_sec_onereport
is a single-year snapshot and stays that way.

What it computes
----------------
Per ticker, from three endpoints:

  19-CGS-AuditorCompany     audit firm, audit_fee, non_audit_fee
  20-CGS-DirectorPerformance  AGM date, board / audit committee meeting counts
  17-CGS-Board              headcount, independent, gender split

and five flags. Three rest on a written rule, two are convention — the screen
labels which is which, because they are not the same kind of finding:

  auditor_change    RULE-FREE   audit firm differs from the prior report year.
                                Not a breach — a prompt to ask why.
  high_non_audit    CONVENTION  non-audit fee > audit fee. No Thai cap on the
                                ratio; the marker is independence-risk practice,
                                not a limit.
  low_independence  RULE        independent directors < 1/3 of the board.
                                SEC/SET require at least one third.
  late_agm          RULE        AGM held later than 4 months after fiscal year
                                end. Public Limited Companies Act B.E. 2535
                                s.98. Assumes a 31 Dec year end — a company on
                                a non-calendar year is flagged `agm_basis` and
                                excluded from the flag.
  thin_audit_cmte   CONVENTION  audit committee met fewer than 4 times. Quarterly
                                review tracks the reporting cycle; no statute
                                sets a floor.

Every flag carries the raw numbers alongside it, so the screen never asserts a
conclusion the underlying figure does not support. A missing figure is null and
excluded from the flag — never coerced to zero.

Usage
-----
  export SEC_API_KEY=...
  python3 scripts/build_sec_governance.py --year 2024
  python3 scripts/build_sec_governance.py --year 2024 --rm C
  python3 scripts/build_sec_governance.py --year 2024 --no-prior   # skip Y-1

Calls: 1 + (3 x tickers) + 1 + (1 x tickers) for the prior-year auditor pull.
Full 232 universe with prior year: ~930 calls, inside the 3,000 / 300 s window.
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
OUT = os.path.join(REPO, "data", "sec-governance.json")

EP_AUDITOR = "/v1/one-report/cgs/{year}/auditor_company/{uid}"
EP_DIRPERF = "/v1/one-report/cgs/{year}/director_performance/{uid}"
EP_BOARD = "/v1/one-report/cgs/{year}/board/{uid}"

MIN_INDEPENDENT_RATIO = 1.0 / 3.0   # SEC/SET: at least one third of the board
AGM_DEADLINE_MONTH_DAY = (4, 30)    # 4 months after a 31 Dec year end
MIN_AUDIT_MEETINGS = 4              # convention, not statute


def load_book(rm):
    with open(TICKERS, encoding="utf-8") as fh:
        rows = json.load(fh)["tickers"]
    if rm and rm.lower() != "all":
        rows = [r for r in rows if r.get("rm") == rm]
    return {r["tk"]: r for r in rows}


def build_id_map(year, language="T"):
    rows = get_v1(f"/v1/one-report/sbo/{year}/info/{language}")
    out = {}
    for r in rows:
        sym = (r.get("symbol") or "").strip().upper()
        if not sym:
            continue
        prev = out.get(sym)
        if prev and (prev.get("last_upd_date") or "") >= (r.get("last_upd_date") or ""):
            continue
        out[sym] = r
    return out


def num(v):
    """Return a float, or None. A blank or unparseable figure is NOT zero."""
    if v is None or v == "":
        return None
    try:
        return float(str(v).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def first(rows):
    return rows[0] if isinstance(rows, list) and rows else {}


def pull(path, errors, tk, label):
    try:
        return get_v1(path)
    except SecApiError as e:
        errors.append({"ticker": tk, "dataset": label, "status": e.status, "path": path})
        return None


def derive(tk, meta, auditor, dirperf, board, auditor_prior, year):
    a, d, b = first(auditor), first(dirperf), first(board)
    ap = first(auditor_prior) if auditor_prior is not None else {}

    audit_fee = num(a.get("audit_fee"))
    non_audit_fee = num(a.get("non_audit_fee"))
    ratio = (non_audit_fee / audit_fee) if (audit_fee and non_audit_fee is not None
                                            and audit_fee > 0) else None

    name = (a.get("auditor_company_name_th") or "").strip() or None
    name_en = (a.get("auditor_company_name_en") or "").strip() or None
    prior_name = (ap.get("auditor_company_name_th") or "").strip() or None
    code = (a.get("auditor_company_code") or "").strip() or None
    prior_code = (ap.get("auditor_company_code") or "").strip() or None

    # Compare on code where both sides have one — a firm can be renamed without
    # the engagement changing. Fall back to the Thai name.
    if code and prior_code:
        changed = code != prior_code
    elif name and prior_name:
        changed = name != prior_name
    else:
        changed = None  # no prior year pulled, or one side missing

    total = num(b.get("total"))
    indep = num(b.get("total_independent"))
    female = num(b.get("total_female"))
    indep_pct = (100.0 * indep / total) if (total and indep is not None and total > 0) else None
    female_pct = (100.0 * female / total) if (total and female is not None and total > 0) else None

    agm_raw = (d.get("agm_meeting_date") or "").strip() or None
    agm_date, late_agm, agm_basis = None, None, None
    if agm_raw:
        for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d", "%d/%m/%Y"):
            try:
                agm_date = datetime.strptime(agm_raw, fmt).date()
                break
            except ValueError:
                continue
        if agm_date:
            # The deadline is 4 months after fiscal year end. We only know the
            # report year, not the year end, so this holds for 31 Dec filers.
            deadline = agm_date.replace(year=int(year) + 1,
                                        month=AGM_DEADLINE_MONTH_DAY[0],
                                        day=AGM_DEADLINE_MONTH_DAY[1])
            late_agm = agm_date > deadline
            agm_basis = "assumes 31 Dec fiscal year end"
        else:
            agm_basis = f"unparsed date: {agm_raw}"

    audit_meetings = num(d.get("total_audit_meeting"))
    board_meetings = num(d.get("total_board_meeting"))

    flags = {
        "auditor_change":   changed,   # True / False / None (no prior year)
        "high_non_audit":   (ratio > 1.0) if ratio is not None else None,
        "low_independence": (indep_pct < MIN_INDEPENDENT_RATIO * 100) if indep_pct is not None else None,
        "late_agm":         late_agm,
        "thin_audit_cmte":  (audit_meetings < MIN_AUDIT_MEETINGS) if audit_meetings is not None else None,
    }
    return {
        "ticker": tk,
        "sector": meta.get("sector"),
        "bucket": meta.get("bucket"),
        "rm": meta.get("rm"),
        "auditor_name": name,
        "auditor_name_en": name_en,
        "auditor_code": code,
        "auditor_prior_name": prior_name,
        "auditor_prior_code": prior_code,
        "audit_fee": audit_fee,
        "non_audit_fee": non_audit_fee,
        "non_audit_ratio": round(ratio, 4) if ratio is not None else None,
        "non_audit_detail": (a.get("non_audit_detail") or "").strip() or None,
        "board_total": total,
        "board_independent": indep,
        "board_independent_pct": round(indep_pct, 1) if indep_pct is not None else None,
        "board_female": female,
        "board_female_pct": round(female_pct, 1) if female_pct is not None else None,
        "agm_date": agm_date.isoformat() if agm_date else None,
        "agm_basis": agm_basis,
        "board_meetings": board_meetings,
        "audit_meetings": audit_meetings,
        "egm_meetings": num(d.get("total_egm_meeting")),
        "flags": flags,
        "flag_count": sum(1 for v in flags.values() if v is True),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--year", required=True, help="One Report year, AD (e.g. 2024)")
    ap.add_argument("--rm", default="all", help="RM code to scope, or 'all' (default: all)")
    ap.add_argument("--language", default="T", choices=["T", "E"])
    ap.add_argument("--no-prior", action="store_true",
                    help="skip the Y-1 auditor pull (disables auditor_change)")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()

    year = a.year
    prior = str(int(year) - 1)
    book = load_book(a.rm)
    print(f"Governance screen — year {year}"
          + ("" if a.no_prior else f" (prior {prior} for auditor change)")
          + f" | scope rm={a.rm} | {len(book)} tickers")

    id_map = build_id_map(year, a.language)
    resolved = {t: id_map[t] for t in book if t in id_map}
    unresolved = sorted(t for t in book if t not in id_map)
    print(f"  resolved {len(resolved)}/{len(book)}; unresolved {len(unresolved)}")
    if unresolved:
        print(f"  unresolved -> {', '.join(unresolved)}")

    prior_map = {}
    if not a.no_prior:
        try:
            prior_map = build_id_map(prior, a.language)
            print(f"  prior year {prior}: {len(prior_map)} symbols")
        except SecApiError as e:
            print(f"  ! prior year {prior} unavailable (HTTP {e.status}) — "
                  f"auditor_change disabled")

    rows, errors = [], []
    for i, tk in enumerate(sorted(resolved), 1):
        uid = resolved[tk]["unique_id"]
        auditor = pull(EP_AUDITOR.format(year=year, uid=uid), errors, tk, "auditor")
        dirperf = pull(EP_DIRPERF.format(year=year, uid=uid), errors, tk, "director_perf")
        board = pull(EP_BOARD.format(year=year, uid=uid), errors, tk, "board")

        auditor_prior = None
        if tk in prior_map:
            auditor_prior = pull(EP_AUDITOR.format(year=prior, uid=prior_map[tk]["unique_id"]),
                                 errors, tk, "auditor_prior")

        rec = derive(tk, book[tk], auditor or [], dirperf or [], board or [],
                     auditor_prior, year)
        rec["corp_name"] = resolved[tk].get("corp_name")
        rec["unique_id"] = uid
        rows.append(rec)
        print(f"  [{i}/{len(resolved)}] {tk:10s} flags={rec['flag_count']} "
              f"auditor={(rec['auditor_name'] or '—')[:34]}")

    # coverage of each field, so a sparse dataset is visible rather than implied
    def filled(key):
        return sum(1 for r in rows if r.get(key) is not None)

    coverage = {k: filled(k) for k in
                ("audit_fee", "non_audit_fee", "non_audit_ratio", "board_total",
                 "board_independent_pct", "agm_date", "audit_meetings",
                 "auditor_name", "auditor_prior_name")}

    flag_totals = {}
    for f in ("auditor_change", "high_non_audit", "low_independence",
              "late_agm", "thin_audit_cmte"):
        flag_totals[f] = {
            "true": sum(1 for r in rows if r["flags"].get(f) is True),
            "assessed": sum(1 for r in rows if r["flags"].get(f) is not None),
        }

    payload = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": "SEC Open Data API /v1/one-report/cgs (api.sec.or.th)",
        "report_year": year,
        "prior_year": None if a.no_prior else prior,
        "scope": f"rm={a.rm}",
        "flag_basis": {
            "auditor_change":   {"kind": "prompt", "note": "audit firm differs from prior report year — not a breach"},
            "high_non_audit":   {"kind": "convention", "note": "non-audit fee exceeds audit fee; no Thai cap on the ratio"},
            "low_independence": {"kind": "rule", "note": "SEC/SET: independent directors must be at least one third of the board"},
            "late_agm":         {"kind": "rule", "note": "Public Limited Companies Act B.E. 2535 s.98 — AGM within 4 months of fiscal year end; assumes 31 Dec year end"},
            "thin_audit_cmte":  {"kind": "convention", "note": "fewer than 4 audit committee meetings; no statutory floor"},
        },
        "counts": {
            "scoped": len(book),
            "resolved": len(resolved),
            "unresolved": len(unresolved),
            "errors": len(errors),
        },
        "coverage": coverage,
        "flag_totals": flag_totals,
        "unresolved": unresolved,
        "errors": errors,
        "rows": sorted(rows, key=lambda r: (-r["flag_count"], r["ticker"])),
    }
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1)
    print(f"\nWrote {a.out}")
    print(f"  counts   {payload['counts']}")
    print(f"  coverage {coverage}")
    print(f"  flags    {flag_totals}")


if __name__ == "__main__":
    main()
