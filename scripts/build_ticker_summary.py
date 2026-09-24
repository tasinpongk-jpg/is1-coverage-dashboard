"""
Build data/ticker-summary.json — enriched per-ticker snapshot for Ticker Summary page.

Data sources (no extra API keys needed beyond what's already in the project):
  1. SETSMART eod-price-by-symbol  → price, sparkline, PE/PBV/DY, market cap
     (requires SETSMART_API_KEY; gracefully skipped if absent)
  2. SET /api/set/stock/{sym}/profile       → IPO, par, free float, foreign %, NVDR %
  3. SET /api/set/company/{sym}/profile     → name, logo, business, CG, ESG, CAC, auditors, mgmt
  4. SET /api/set/stock/{sym}/company-highlight → multi-year annual financials

SET.or.th API needs NO key — browser headers + one-time cookie warmup is sufficient
(same technique used by the disclosure-pulse route).

Usage:
    python scripts/build_ticker_summary.py
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

# ── SETSMART config ──────────────────────────────────────────────────────────
SETSMART_BASE = os.environ.get("SETSMART_BASE", "https://www.setsmart.com/api").rstrip("/")
LISTED_BASE   = f"{SETSMART_BASE}/listed-company-api"
API_KEY       = (os.environ.get("SETSMART_API_KEY") or "").strip()
HTTP_TIMEOUT  = float(os.environ.get("HTTP_TIMEOUT", "30"))
SETSMART_MAX  = int(os.environ.get("SETSMART_MAX_CONCURRENT", "1"))

# ── SET.or.th config ─────────────────────────────────────────────────────────
SET_BASE     = "https://www.set.or.th"
SET_THROTTLE = float(os.environ.get("SET_THROTTLE_S", "0.28"))
SET_MAX      = int(os.environ.get("SET_MAX_CONCURRENT", "3"))
SET_UA       = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
SET_HEADERS  = {
    "User-Agent": SET_UA,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9,th;q=0.8",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
}

SEGMENT: dict[str, str] = {
    "TU":"Seafood","ASIAN":"Seafood","CFRESH":"Seafood",
    "ITC":"Pet Food","AAI":"Pet Food",
    "TFMAMA":"Noodles","SST":"Noodles",
    "PRG":"Snacks/Bakery","SNP":"Snacks/Bakery","SSF":"Snacks/Bakery","PB":"Snacks/Bakery",
    "M":"Restaurant","ZEN":"Restaurant","OKJ":"Restaurant","MADAME":"Restaurant",
    "PQS":"Other Food","TWPC":"Other Food","CHOTI":"Other Food","TC":"Other Food","XBIO":"Other Food",
    "CPN":"Retail","MBK":"Retail","PLAT":"Retail",
    "WHA":"IE","AMATA":"IE","AMATAV":"IE","ROJNA":"IE","NNCL":"IE","PIN":"IE",
    "AWC":"Mixed/Hosp","J":"Residential","BLAND":"Residential","JCK":"Residential","WIN":"Residential",
    "WHART":"Industrial REIT","FTREIT":"Industrial REIT","WHAIR":"Industrial REIT",
    "AMATAR":"Industrial REIT","TIF1":"Industrial PF","TTLPF":"Industrial PF","TNPF":"Industrial PF",
    "CPNREIT":"Retail REIT","LHSC":"Retail REIT","ALLY":"Retail REIT",
    "AIMCG":"Office REIT","IMPACT":"Office REIT","SSTRT":"Hospitality REIT",
    "HPF":"Other PF","MJLF":"Other PF","AXTRART":"Other REIT",
}

# ── SETSMART helpers ─────────────────────────────────────────────────────────

async def _sm_get(client: httpx.AsyncClient, url: str, params: dict) -> list | None:
    hdrs = {"api-key": API_KEY, "Accept": "application/json"}
    for attempt in range(3):
        try:
            r = await client.get(url, headers=hdrs, params=params, timeout=HTTP_TIMEOUT)
            if r.status_code in (429, 500, 502, 503, 504):
                await asyncio.sleep(0.5 * (attempt + 1)); continue
            if r.status_code >= 400: return None
            body = r.json()
            return body if isinstance(body, list) else None
        except Exception:
            await asyncio.sleep(0.5 * (attempt + 1))
    return None

async def fetch_eod(client: httpx.AsyncClient, tk: str) -> list[dict]:
    today = date.today()
    params = {
        "symbol": tk,
        "startDate": (today - timedelta(days=375)).isoformat(),
        "endDate": today.isoformat(),
        "adjustedPriceFlag": "Y",
    }
    return (await _sm_get(client, f"{LISTED_BASE}/eod-price-by-symbol", params)) or []

def _pct(curr, base):
    if curr is None or base in (None, 0): return None
    return round((curr / base - 1) * 100, 2)

def process_eod(rows: list[dict]) -> dict:
    rows = sorted(rows, key=lambda r: r.get("date") or "")
    closes = [r["close"] for r in rows if r.get("close")]
    vols   = [r["totalVolume"] for r in rows if r.get("totalVolume")]
    if not closes: return {"_eod_err": True}
    last = closes[-1]
    prev_1d = closes[-2] if len(closes) >= 2 else None
    prev_5d = closes[-6] if len(closes) >= 6 else None
    today_iso = date.today().isoformat()
    month_str, year_str = today_iso[:7], today_iso[:4]
    prev_mtd = prev_ytd = None
    for r in reversed(rows):
        d, c = (r.get("date") or ""), r.get("close")
        if not c: continue
        if prev_mtd is None and d[:7] < month_str: prev_mtd = c
        if prev_ytd is None and d[:4] < year_str: prev_ytd = c
        if prev_mtd and prev_ytd: break
    last_252 = closes[-252:] if len(closes) >= 252 else closes
    hi52, lo52 = round(max(last_252), 3), round(min(last_252), 3)
    last_row = next((r for r in reversed(rows) if r.get("close")), {})
    avg_vol = sum(vols[-20:]) / len(vols[-20:]) if len(vols) >= 20 else None
    last_vol = vols[-1] if vols else None
    return {
        "last": last, "pct1d": _pct(last, prev_1d), "pct5d": _pct(last, prev_5d),
        "pctMtd": _pct(last, prev_mtd), "pctYtd": _pct(last, prev_ytd),
        "hi52": hi52, "lo52": lo52,
        "atHi52": bool(last >= hi52 * 0.998), "atLo52": bool(last <= lo52 * 1.002),
        "pe": last_row.get("pe"), "pbv": last_row.get("pbv"),
        "dy": last_row.get("dividendYield"), "mktcap": last_row.get("marketCap"),
        "bvps": last_row.get("bvps"), "sparkline": closes[-20:],
        "volRatio": round(last_vol / avg_vol, 2) if last_vol and avg_vol else None,
    }

# ── SET.or.th helpers ────────────────────────────────────────────────────────

async def _set_warmup(client: httpx.AsyncClient):
    warmup_hdrs = {**SET_HEADERS, "Accept": "text/html,application/xhtml+xml,*/*"}
    for url in [SET_BASE + "/", SET_BASE + "/en/market/product/stock/quote/PTT/factsheet"]:
        try: await client.get(url, headers=warmup_hdrs, timeout=12)
        except Exception: pass
    await asyncio.sleep(0.5)

async def _set_get(client: httpx.AsyncClient, path: str, sem: asyncio.Semaphore,
                   sym: str) -> dict | list | None:
    url = SET_BASE + path
    hdrs = {**SET_HEADERS, "Referer": f"{SET_BASE}/en/market/product/stock/quote/{sym}/factsheet"}
    async with sem:
        await asyncio.sleep(SET_THROTTLE)
        for attempt in range(2):
            try:
                r = await client.get(url, headers=hdrs, timeout=15)
                if r.status_code == 200: return r.json()
                return None
            except Exception:
                await asyncio.sleep(0.4)
    return None

async def fetch_stock_profile(client: httpx.AsyncClient, tk: str, sem: asyncio.Semaphore) -> dict:
    d = await _set_get(client, f"/api/set/stock/{tk}/profile?lang=en", sem, tk)
    if not isinstance(d, dict): return {}
    return {
        "listedDate":   (d.get("listedDate") or "")[:10] or None,
        "ipo":          d.get("ipo"),
        "par":          d.get("par"),
        "listedShare":  d.get("listedShare"),
        "freeFloat":    d.get("percentFreeFloat"),
        "foreignLimit": d.get("percentForeignLimit"),
        "foreignRoom":  d.get("percentForeignRoom"),
        "isinLocal":    d.get("isinLocal"),
        "fiscalYearEnd":d.get("fiscalYearEndDisplay"),
    }

async def fetch_company_profile(client: httpx.AsyncClient, tk: str, sem: asyncio.Semaphore) -> dict:
    d, d_th = await asyncio.gather(
        _set_get(client, f"/api/set/company/{tk}/profile?lang=en", sem, tk),
        _set_get(client, f"/api/set/company/{tk}/profile?lang=th", sem, tk),
    )
    if not isinstance(d, dict):
        d = {}
    if not isinstance(d_th, dict):
        d_th = {}
    if not d and not d_th:
        return {}
    return {
        "name":           d.get("name") or d_th.get("name"),
        "nameTh":         d_th.get("name"),
        "logoUrl":        d.get("logoUrl") or d_th.get("logoUrl"),
        "businessType":   (d.get("businessType") or "").strip(),
        "businessTypeTh": (d_th.get("businessType") or "").strip(),
        "website":        d.get("url") or d_th.get("url"),
        "address":        d.get("address") or d_th.get("address"),
        "tel":            d.get("telephone") or d_th.get("telephone"),
        "dividendPolicy": d.get("dividendPolicy") or d_th.get("dividendPolicy"),
        "cgScore":        d.get("cgScore"),
        "cacFlag":        d.get("cacFlag"),
        "esgRating":      d.get("setesgRating"),
        "established":    d.get("establishedDate"),
        "auditOpinion":   d.get("auditChoice"),
        "auditors": [{"name": a.get("name"), "company": a.get("company")}
                     for a in (d.get("auditors") or [])][:3],
        "managements": [{"position": m.get("position"), "name": m.get("name")}
                        for m in (d.get("managements") or [])][:4],
    }

async def fetch_highlights(client: httpx.AsyncClient, tk: str, sem: asyncio.Semaphore) -> list:
    d = await _set_get(client, f"/api/set/stock/{tk}/company-highlight?lang=en", sem, tk)
    if not isinstance(d, list): return []
    out = []
    for item in sorted(d, key=lambda x: x.get("year", 0)):
        fd = item.get("financialData") or {}
        ts = item.get("tradingStat") or {}
        # financialData values are in thousands THB → divide by 1000 for M฿
        def mbht(v): return round(v / 1000, 1) if v else None
        # quarter field: Q1=3M, Q2=6M, Q3=9M, Q9=full year (annual)
        quarter = fd.get("quarter") or ""
        months = {"Q1": 3, "Q2": 6, "Q3": 9, "Q4": 12, "Q9": 12}.get(quarter, 12)
        out.append({
            "year":        item.get("year"),
            "quarter":     quarter,
            "months":      months,
            "revenue":     mbht(fd.get("totalRevenue")),
            "sales":       mbht(fd.get("sales")),
            "ebitda":      mbht(fd.get("ebitda")),
            "netProfit":   mbht(fd.get("netProfit")),
            "eps":         fd.get("eps"),
            "totalAsset":  mbht(fd.get("totalAsset")),
            "equity":      mbht(fd.get("equity")),
            "totalLiab":   mbht(fd.get("totalLiability")),
            "netOperating":mbht(fd.get("netOperating")),
            "netInvesting":mbht(fd.get("netInvesting")),
            "netFinancing":mbht(fd.get("netFinancing")),
            "roe":         fd.get("roe"),
            "roa":         fd.get("roa"),
            "npm":         fd.get("netProfitMargin"),
            "gpm":         fd.get("grossProfitMargin"),
            "deRatio":     fd.get("deRatio"),
            "currentRatio":fd.get("currentRatio"),
            "quickRatio":  fd.get("quickRatio"),
            "pe":  ts.get("pe"),
            "pbv": ts.get("pbv"),
            "dy":  ts.get("dividendYield"),
        })
    return out[-5:]

# ── per-ticker orchestration ─────────────────────────────────────────────────

async def build_one(sm_client: httpx.AsyncClient, set_client: httpx.AsyncClient,
                    meta: dict, sm_sem: asyncio.Semaphore,
                    set_sem: asyncio.Semaphore) -> dict:
    tk = meta["tk"]

    async def _eod():
        if not API_KEY: return {}
        async with sm_sem:
            rows = await fetch_eod(sm_client, tk)
            return process_eod(rows)

    eod, sp, cp, hl = await asyncio.gather(
        _eod(),
        fetch_stock_profile(set_client, tk, set_sem),
        fetch_company_profile(set_client, tk, set_sem),
        fetch_highlights(set_client, tk, set_sem),
    )

    has_data = bool(eod or sp or cp or hl)
    if not has_data:
        return {**meta, "segment": SEGMENT.get(tk, meta["sector"]), "_err": "no_data"}

    result = {
        "tk": tk,
        "sector": meta["sector"],
        "segment": SEGMENT.get(tk, meta["sector"]),
        "rm": meta["rm"],
        **{k: v for k, v in eod.items() if k != "_eod_err"},
        **sp, **cp,
        "highlights": hl,
    }
    return result

# ── main ─────────────────────────────────────────────────────────────────────

async def main():
    tkr_path = DATA_DIR / "tickers.json"
    if not tkr_path.exists():
        sys.exit(f"Missing {tkr_path}")
    tickers = json.loads(tkr_path.read_text(encoding="utf-8"))["tickers"]
    for t in tickers:
        # Anonymise RM to its initial (privacy), defensively — even if
        # tickers.json ever regresses to full names upstream.
        rm = t.get("rm")
        if rm not in (None, ""):
            t["rm"] = str(rm).strip()[:1].upper()
    if not API_KEY:
        print("Note: SETSMART_API_KEY not set — price/sparkline data will be absent")
    print(f"Building summaries for {len(tickers)} tickers "
          f"(SETSMART={bool(API_KEY)}, SET_MAX={SET_MAX}, throttle={SET_THROTTLE}s) …")

    sm_sem  = asyncio.Semaphore(SETSMART_MAX)
    set_sem = asyncio.Semaphore(SET_MAX)

    async with (httpx.AsyncClient(timeout=HTTP_TIMEOUT, follow_redirects=True) as sm_client,
                httpx.AsyncClient(timeout=HTTP_TIMEOUT, follow_redirects=True) as set_client):
        print("  → warming up SET session …")
        await _set_warmup(set_client)
        results = await asyncio.gather(*[
            build_one(sm_client, set_client, t, sm_sem, set_sem) for t in tickers
        ])

    ok   = [r for r in results if "_err" not in r]
    errs = [{"tk": r["tk"], "err": r.get("_err")} for r in results if "_err" in r]
    for r in ok:
        print(f"  {r['tk']:<10s}  last={str(r.get('last','—')):<8}  {r.get('name','?')[:35]}")

    payload = {
        "version": 2,
        "asOf": date.today().isoformat(),
        "tickers": ok,
        "errors": errs,
        "_built_at": datetime.now(timezone.utc).isoformat(),
        "_coverage_size": len(tickers),
        "source": f"SETSMART + SET.or.th API · {len(ok)}/{len(tickers)} ok"
                  + (f" · {len(errs)} errors" if errs else ""),
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {len(ok)} tickers → {OUT}")
    if errs:
        print(f"Errors ({len(errs)}): {[e['tk'] for e in errs]}")

if __name__ == "__main__":
    asyncio.run(main())
