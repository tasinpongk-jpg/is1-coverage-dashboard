#!/usr/bin/env python3
"""Reconstruct a SET ex-DELTA index from raw daily data and validate it.

Inputs (raw daily exports, ~3 years):
  * DELTA HistoricalTrading.xlsx  — daily Close + Market Cap (M.Baht) + Listed Shares
  * SET sectoralDataPrice .xls    — daily SET Composite Close (index level) + Market Cap (Baht)

Method (divisor-continuity chain — reproduces the published index by construction):
  The SET Composite is market-cap weighted: Index_t = MC_t / D_t, where D_t is the
  divisor embedding all base-market-value adjustments. We recover the divisor daily as
  D_t = MC_t / Index_t, and its day-on-day ratio g_t = D_t / D_{t-1} isolates the pure
  corporate-action / recomposition effect (g_t = 1 on ordinary days).

  ex-DELTA market cap:  exMC_t = MC_t - DELTA_MC_t
  ex-DELTA daily return: r'_t = exMC_t / (exMC_{t-1} * g_t) - 1
  ex-DELTA index:        ex_t = ex_{t-1} * (1 + r'_t),  ex_0 = Index_0

  Applying the SAME g_t to the FULL market cap reproduces the published index exactly:
    MC_t / (MC_{t-1} * g_t) - 1 = Index_t / Index_{t-1} - 1
  which is the acceptance test (self-validating construction). Continuity holds because
  a recomposition changes D (and thus g) so no fake return is injected — Index_after =
  Index_before, i.e. no price shock from recomposition alone (the BMV continuity point).

Assumption: DELTA prices are adjustment-clean (the export uses "Adjusted Price: Yes"),
so DELTA-specific corporate actions do not distort exMC. Documented, not hidden.

Outputs: data/set-ex-delta.json  (daily series + headline stats + validation report)
"""
from __future__ import annotations
import json, sys, datetime as dt
from pathlib import Path

import openpyxl
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DELTA_XLSX = sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "data" / "raw" / "delta-historical.xlsx")
SET_XLS = sys.argv[2] if len(sys.argv) > 2 else str(ROOT / "data" / "raw" / "set-index.xls")
OUT = ROOT / "data" / "set-ex-delta.json"


def load_delta(path: str) -> dict[dt.date, dict]:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb["Sheet1"]
    rows = list(ws.iter_rows(values_only=True))
    # locate header row ("Date", "Prior", ... "Close" ...)
    hi = next(i for i, r in enumerate(rows) if r and r[0] == "Date" and "Close" in r)
    hdr = rows[hi]
    ci = {name: idx for idx, name in enumerate(hdr) if isinstance(name, str)}
    close_i = ci["Close"]
    mcap_i = ci["Market Cap. (M.Baht)"]
    shares_i = ci["Listed Shares"]
    out: dict[dt.date, dict] = {}
    for r in rows[hi + 1:]:
        d = r[0]
        if not isinstance(d, dt.datetime):
            continue
        close = r[close_i]
        mcap = r[mcap_i]
        if close in (None, "-") or mcap in (None, "-"):
            continue
        out[d.date()] = {
            "close": float(close),
            "mcap": float(mcap) * 1e6,  # M.Baht -> Baht
            "shares": float(r[shares_i]) if r[shares_i] not in (None, "-") else None,
        }
    return out


def load_set(path: str) -> dict[dt.date, dict]:
    tbl = None
    for t in pd.read_html(path):
        if t.shape[1] >= 11 and (t.iloc[:2].astype(str).apply(
                lambda s: s.str.contains("Market Cap", na=False)).any().any()):
            tbl = t
            break
    if tbl is None:
        raise SystemExit("Could not find SET daily table with 'Market Cap' column")
    hdr = list(tbl.iloc[1])
    ci = {str(name): idx for idx, name in enumerate(hdr)}
    close_i = ci["Close"]
    mcap_i = ci["Market Cap (Baht)"]
    out: dict[dt.date, dict] = {}
    for _, row in tbl.iloc[2:].iterrows():
        raw = str(row[0])
        try:
            d = dt.datetime.strptime(raw, "%d/%m/%Y").date()
        except ValueError:
            continue
        try:
            close = float(str(row[close_i]).replace(",", ""))
            mcap = float(str(row[mcap_i]).replace(",", ""))
        except (ValueError, TypeError):
            continue
        out[d] = {"index": close, "mcap": mcap}
    return out


def main() -> None:
    delta = load_delta(DELTA_XLSX)
    setix = load_set(SET_XLS)
    dates = sorted(set(delta) & set(setix))
    if len(dates) < 100:
        raise SystemExit(f"Too few overlapping dates: {len(dates)}")

    series = []
    ex_prev = None
    exmc_prev = None
    d_prev = None
    max_repro_err = 0.0
    repro_prev = None
    for d in dates:
        s = setix[d]
        de = delta[d]
        mc = s["mcap"]
        idx = s["index"]
        exmc = mc - de["mcap"]
        weight = de["mcap"] / mc
        div = mc / idx  # divisor D_t
        if ex_prev is None:
            ex = idx  # base ex-index at published level
            repro = idx
        else:
            g = div / d_prev
            r_ex = exmc / (exmc_prev * g) - 1.0
            ex = ex_prev * (1.0 + r_ex)
            r_full = mc / (mc_prev * g) - 1.0
            repro = repro_prev * (1.0 + r_full)
            max_repro_err = max(max_repro_err, abs(repro - idx) / idx)
        series.append({
            "date": d.isoformat(),
            "setIndex": round(idx, 2),
            "setExDelta": round(ex, 2),
            "deltaWeightPct": round(weight * 100, 4),
            "deltaClose": de["close"],
            "setMcapTHB": mc,
            "deltaMcapTHB": de["mcap"],
        })
        ex_prev, exmc_prev, d_prev, mc_prev, repro_prev = ex, exmc, div, mc, repro

    first, last = series[0], series[-1]
    # YTD anchor: last close of prior year
    yr = dt.date.fromisoformat(last["date"]).year
    ytd_base = next((r for r in reversed(series)
                     if dt.date.fromisoformat(r["date"]).year < yr), series[0])

    def perf(a, b, key):
        return round((b[key] / a[key] - 1.0) * 100, 2)

    weights = [r["deltaWeightPct"] for r in series]
    peak = max(series, key=lambda r: r["deltaWeightPct"])

    stats = {
        "asOf": last["date"],
        "rangeStart": first["date"],
        "tradingDays": len(series),
        "deltaWeightPct_latest": last["deltaWeightPct"],
        "deltaWeightPct_peak": peak["deltaWeightPct"],
        "deltaWeightPct_peakDate": peak["date"],
        "deltaWeightPct_min": round(min(weights), 4),
        "setMcapTHB_latest": last["setMcapTHB"],
        "deltaMcapTHB_latest": last["deltaMcapTHB"],
        "set_3y_pct": perf(first, last, "setIndex"),
        "setExDelta_3y_pct": perf(first, last, "setExDelta"),
        "set_ytd_pct": perf(ytd_base, last, "setIndex"),
        "setExDelta_ytd_pct": perf(ytd_base, last, "setExDelta"),
        "ytdAnchorDate": ytd_base["date"],
        "delta_ytd_pct": round((last["deltaClose"] / ytd_base["deltaClose"] - 1.0) * 100, 2),
        "delta_3y_pct": round((last["deltaClose"] / first["deltaClose"] - 1.0) * 100, 2),
        "mechanicalImpactPer1pct": round(last["deltaWeightPct"] / 100, 4),
        "validation_maxIndexReproErrorBps": round(max_repro_err * 1e4, 3),
    }

    payload = {
        "version": 1,
        "generated": "static",  # stamp externally; Date.now unavailable in some runners
        "method": "divisor-continuity chain (D_t = MC_t/Index_t); ex_t reproduces published index by construction",
        "assumptions": "DELTA export uses adjusted prices; ex-DELTA basket = SET total MC minus DELTA MC.",
        "stats": stats,
        "series": series,
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2))

    print(f"Wrote {OUT} — {len(series)} trading days {first['date']}..{last['date']}")
    print(f"  Validation: max index reproduction error = {stats['validation_maxIndexReproErrorBps']} bps")
    print(f"  DELTA weight latest ({last['date']}): {stats['deltaWeightPct_latest']}%")
    print(f"  DELTA weight peak: {stats['deltaWeightPct_peak']}% on {stats['deltaWeightPct_peakDate']}")
    print(f"  SET 3y: {stats['set_3y_pct']}%   SET ex-DELTA 3y: {stats['setExDelta_3y_pct']}%")
    print(f"  SET YTD: {stats['set_ytd_pct']}%   ex-DELTA YTD: {stats['setExDelta_ytd_pct']}%   (anchor {stats['ytdAnchorDate']})")
    print(f"  DELTA YTD: {stats['delta_ytd_pct']}%   DELTA 3y: {stats['delta_3y_pct']}%")


if __name__ == "__main__":
    main()
