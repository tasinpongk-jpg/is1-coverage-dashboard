"""
Build data/ticker-summary.json — per-ticker snapshot for the Ticker Summary page.

Reads tickers.json for the full portfolio list, then calls SETSMART's
eod-price-by-symbol endpoint for each ticker to compute price, ratios, and
52-week high/low. Output is written to data/ticker-summary.json.

Usage:
    python scripts/build_ticker_summary.py

Requires:
    SETSMART_API_KEY env var (same key used by the rest of the daily pipeline)
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
OUT = DATA_DIR / "ticker-summary.json"

SETSMART_BASE = os.environ.get("SETSMART_BASE", "https://www.setsmart.com/api").rstrip("/")
LISTED_BASE = f"{SETSMART_BASE}/listed-company-api"
API_KEY = (os.environ.get("SETSMART_API_KEY") or "").strip()
HTTP_TIMEOUT = float(os.environ.get("HTTP_TIMEOUT", "30"))
MAX_CONCURRENT = int(os.environ.get("SETSMART_MAX_CONCURRENT", "1"))

# Sub-segment mapping (matches setsmart_proxy.py)
SEGMENT: dict[str, str] = {
    "TU": "Seafood", "ASIAN": "Seafood", "CFRESH": "Seafood",
    "ITC": "Pet Food", "AAI": "Pet Food",
    "TFMAMA": "Noodles", "SST": "Noodles",
    "PRG": "Snacks/Bakery", "SNP": "Snacks/Bakery", "SSF": "Snacks/Bakery", "PB": "Snacks/Bakery",
    "M": "Restaurant", "ZEN": "Restaurant", "OKJ": "Restaurant", "MADAME": "Restaurant",
    "PQS": "Other Food", "TWPC": "Other Food", "CHOTI": "Other Food", "TC": "Other Food", "XBIO": "Other Food",
    "CPN": "Retail", "MBK": "Retail", "PLAT": "Retail",
    "WHA": "IE", "AMATA": "IE", "AMATAV": "IE", "ROJNA": "IE", "NNCL": "IE", "PIN": "IE",
    "AWC": "Mixed/Hosp", "J": "Residential", "BLAND": "Residential", "JCK": "Residential", "WIN": "Residential",
    "WHART": "Industrial REIT", "FTREIT": "Industrial REIT", "WHAIR": "Industrial REIT",
    "AMATAR": "Industrial REIT", "TIF1": "Industrial PF", "TTLPF": "Industrial PF", "TNPF": "Industrial PF",
    "CPNREIT": "Retail REIT", "LHSC": "Retail REIT", "ALLY": "Retail REIT",
    "AIMCG": "Office REIT", "IMPACT": "Office REIT",
    "SSTRT": "Hospitality REIT",
    "HPF": "Other PF", "MJLF": "Other PF", "AXTRART": "Other REIT",
}


def _headers() -> dict[str, str]:
    if not API_KEY:
        sys.exit("SETSMART_API_KEY env var not set — cannot call SETSMART API")
    return {"api-key": API_KEY, "Accept": "application/json"}


async def _get(client: httpx.AsyncClient, url: str, params: dict) -> list | None:
    for attempt in range(3):
        try:
            r = await client.get(url, headers=_headers(), params=params, timeout=HTTP_TIMEOUT)
            if r.status_code in (429, 500, 502, 503, 504):
                await asyncio.sleep(0.5 * (attempt + 1))
                continue
            if r.status_code >= 400:
                return None
            body = r.json()
            return body if isinstance(body, list) else None
        except (httpx.RequestError, httpx.TimeoutException):
            await asyncio.sleep(0.5 * (attempt + 1))
    return None


async def fetch_eod(client: httpx.AsyncClient, tk: str) -> list[dict]:
    today = date.today()
    start = (today - timedelta(days=375)).isoformat()  # ~13 months for a full 52-week window
    params = {
        "symbol": tk,
        "startDate": start,
        "endDate": today.isoformat(),
        "adjustedPriceFlag": "Y",
    }
    rows = await _get(client, f"{LISTED_BASE}/eod-price-by-symbol", params)
    return rows or []


def _pct(curr, base):
    if curr is None or base in (None, 0):
        return None
    return round((curr / base - 1) * 100, 2)


async def build_snapshot(client: httpx.AsyncClient, meta: dict) -> dict:
    tk = meta["tk"]
    rows = sorted(await fetch_eod(client, tk), key=lambda r: r.get("date") or "")

    closes = [r["close"] for r in rows if r.get("close")]
    vols   = [r["totalVolume"] for r in rows if r.get("totalVolume")]

    if not closes:
        return {**meta, "segment": SEGMENT.get(tk, meta["sector"]), "_err": "no_eod_data"}

    last = closes[-1]
    prev_1d  = closes[-2]  if len(closes) >= 2  else None
    prev_5d  = closes[-6]  if len(closes) >= 6  else None

    today_iso = date.today().isoformat()
    month_str, year_str = today_iso[:7], today_iso[:4]
    prev_mtd = prev_ytd = None
    for r in reversed(rows):
        d, c = (r.get("date") or ""), r.get("close")
        if not c:
            continue
        if prev_mtd is None and d[:7] < month_str:
            prev_mtd = c
        if prev_ytd is None and d[:4] < year_str:
            prev_ytd = c
        if prev_mtd and prev_ytd:
            break

    last_252 = closes[-252:] if len(closes) >= 252 else closes
    hi52 = round(max(last_252), 3)
    lo52 = round(min(last_252), 3)

    last_row = next((r for r in reversed(rows) if r.get("close")), {})
    avg_vol  = (sum(vols[-20:]) / len(vols[-20:])) if len(vols) >= 20 else None
    last_vol = vols[-1] if vols else None

    return {
        "tk": tk,
        "sector": meta["sector"],
        "segment": SEGMENT.get(tk, meta["sector"]),
        "rm": meta["rm"],
        "last": last,
        "pct1d":  _pct(last, prev_1d),
        "pct5d":  _pct(last, prev_5d),
        "pctMtd": _pct(last, prev_mtd),
        "pctYtd": _pct(last, prev_ytd),
        "hi52": hi52,
        "lo52": lo52,
        "atHi52": bool(last >= hi52 * 0.998),
        "atLo52": bool(last <= lo52 * 1.002),
        "pe":       last_row.get("pe"),
        "pbv":      last_row.get("pbv"),
        "dy":       last_row.get("dividendYield"),
        "mktcap":   last_row.get("marketCap"),
        "bvps":     last_row.get("bvps"),
        "sparkline": closes[-20:],
        "volRatio": round(last_vol / avg_vol, 2) if last_vol and avg_vol else None,
    }


async def main():
    tkr_path = DATA_DIR / "tickers.json"
    if not tkr_path.exists():
        sys.exit(f"Missing {tkr_path}")

    tickers = json.loads(tkr_path.read_text(encoding="utf-8"))["tickers"]
    print(f"Building ticker summaries for {len(tickers)} tickers (concurrent={MAX_CONCURRENT}) …")

    sem = asyncio.Semaphore(MAX_CONCURRENT)

    async def _one(client, meta):
        async with sem:
            snap = await build_snapshot(client, meta)
            status = "ERR" if "_err" in snap else "ok"
            print(f"  {meta['tk']:<10s}  {status}  last={snap.get('last')}", flush=True)
            return snap

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        results = await asyncio.gather(*[_one(client, t) for t in tickers])

    ok   = [r for r in results if "_err" not in r]
    errs = [{"tk": r["tk"], "err": r["_err"]} for r in results if "_err" in r]

    payload = {
        "version": 1,
        "asOf": date.today().isoformat(),
        "tickers": ok,
        "errors": errs,
        "_built_at": datetime.now(timezone.utc).isoformat(),
        "_coverage_size": len(tickers),
        "source": f"SETSMART eod-price-by-symbol · {len(ok)}/{len(tickers)} ok"
                  + (f" · {len(errs)} errors" if errs else ""),
    }

    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {len(ok)} tickers → {OUT}")
    if errs:
        print(f"Errors ({len(errs)}): {[e['tk'] for e in errs]}")


if __name__ == "__main__":
    asyncio.run(main())
