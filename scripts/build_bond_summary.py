"""
Build data/bond-summary.json — ThaiBMA outstanding bond data for IS1 coverage.

Uses ThaiBMA's internal web API (no auth key required — same endpoints their
public site uses). Fetches long + short term outstanding bonds per ticker.

464 requests (232 tickers × 2) at ~0.3 s throttle ≈ 3–5 minutes.
Update monthly or quarterly — add workflow_dispatch to GHA for manual runs.

Usage:
    python scripts/build_bond_summary.py
"""
from __future__ import annotations

import asyncio
import json
from datetime import date, datetime, timezone
from pathlib import Path

import httpx

ROOT    = Path(__file__).resolve().parent.parent
DATA    = ROOT / "data"
OUT     = DATA / "bond-summary.json"
TKRS    = DATA / "tickers.json"

BASE    = "https://www.thaibma.or.th"
REFERER = BASE + "/EN/Issuer/IssuerDetail.aspx"
UA      = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
           "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Accept": "application/json, text/plain, */*",
           "Accept-Language": "en-US,en;q=0.9,th;q=0.8", "Referer": REFERER}
THROTTLE = 0.30
MAX_CONCURRENT = 3

SECTOR_NORM = {"PF&REIT": "PFREIT"}

# ── fetch ─────────────────────────────────────────────────────────────────────

async def fetch_bonds(client: httpx.AsyncClient, tk: str, term: str,
                      sem: asyncio.Semaphore) -> list[dict]:
    url = f"{BASE}/issuer/regissue?abbrName={tk}&term={term}"
    async with sem:
        await asyncio.sleep(THROTTLE)
        for attempt in range(3):
            try:
                r = await client.get(url, headers=HEADERS, timeout=15)
                if r.status_code == 200:
                    body = r.json()
                    return body if isinstance(body, list) else []
                return []
            except Exception:
                await asyncio.sleep(0.5 * (attempt + 1))
    return []

# ── process one ticker ────────────────────────────────────────────────────────

def process_bond(raw: dict, term: str) -> dict:
    """Normalise a raw ThaiBMA bond record into our schema."""
    mat = (raw.get("MaturityDate") or "")[:10]
    iss = (raw.get("IssuedDate") or "")[:10]
    return {
        "symbol":       raw.get("Symbol", ""),
        "type":         term,                       # "long" | "short"
        "issuedDate":   iss,
        "maturityDate": mat,
        "maturityYear": int(mat[:4]) if len(mat) >= 4 else None,
        "issueSize":    raw.get("IssueSize"),       # M฿
        "outstanding":  raw.get("IssueOutstanding"),# M฿
        "ttm":          raw.get("TTM"),             # years
        "secure":       raw.get("SecureCode", ""),
        "rating":       raw.get("IssueRating", "").strip() or raw.get("CompanyRating", "").strip(),
        "distribution": raw.get("DistributionDisplay", ""),
        "esg":          raw.get("ESGDisplay", "").strip(),
        "registrar":    raw.get("Registrar", ""),
        "crossDefault": raw.get("CrossDefaultAmount"),
        "attribute":    raw.get("AttributeDisplay", ""),
    }

async def fetch_issuer(client: httpx.AsyncClient, meta: dict,
                       sem: asyncio.Semaphore) -> dict | None:
    tk = meta["tk"]
    long_raw, short_raw = await asyncio.gather(
        fetch_bonds(client, tk, "long",  sem),
        fetch_bonds(client, tk, "short", sem),
    )
    bonds = ([process_bond(b, "long")  for b in long_raw] +
             [process_bond(b, "short") for b in short_raw])
    if not bonds:
        return None

    total_out  = sum(b["outstanding"] or 0 for b in bonds)
    company_rating = ""
    for raw in long_raw + short_raw:
        r = raw.get("CompanyRating", "").strip()
        if r:
            company_rating = r
            break

    return {
        "tk":           tk,
        "sector":       SECTOR_NORM.get(meta["sector"], meta["sector"]),
        "rm":           meta["rm"],
        "rating":       company_rating,
        "totalOutstanding": round(total_out, 2),
        "longCount":    len([b for b in bonds if b["type"] == "long"]),
        "shortCount":   len([b for b in bonds if b["type"] == "short"]),
        "bonds":        sorted(bonds, key=lambda b: b.get("maturityDate") or ""),
        "hasESG":       any(b["esg"] for b in bonds),
        "nearestMaturity": min((b["maturityDate"] for b in bonds if b["maturityDate"]), default=None),
    }

# ── global summary ────────────────────────────────────────────────────────────

def build_summary(issuers: list[dict]) -> dict:
    today = date.today()
    cur_year = today.year

    total_out  = round(sum(i["totalOutstanding"] for i in issuers), 2)
    total_bonds = sum(i["longCount"] + i["shortCount"] for i in issuers)
    esg_count  = sum(1 for i in issuers for b in i["bonds"] if b["esg"])
    all_bonds  = [b for i in issuers for b in i["bonds"]]

    # Maturing this year / next year
    mat_this   = sum((b["outstanding"] or 0) for b in all_bonds if (b["maturityDate"] or "")[:4] == str(cur_year))
    mat_next   = sum((b["outstanding"] or 0) for b in all_bonds if (b["maturityDate"] or "")[:4] == str(cur_year + 1))

    # By maturity year (group 7+ years into a bucket)
    by_year: dict[str, float] = {}
    by_year_sector: dict[str, dict[str, float]] = {}
    for i in issuers:
        s = i["sector"]
        for b in i["bonds"]:
            yr = b.get("maturityYear")
            if yr is None:
                continue
            label = str(yr) if yr <= cur_year + 6 else f"{cur_year + 7}+"
            by_year[label]         = round(by_year.get(label, 0) + (b["outstanding"] or 0), 2)
            by_year_sector.setdefault(label, {})
            by_year_sector[label][s] = round(by_year_sector[label].get(s, 0) + (b["outstanding"] or 0), 2)

    # By sector
    by_sector: dict[str, float] = {}
    for i in issuers:
        s = i["sector"]
        by_sector[s] = round(by_sector.get(s, 0) + i["totalOutstanding"], 2)

    # Avg TTM
    ttms = [b["ttm"] for i in issuers for b in i["bonds"] if b["ttm"] is not None]
    avg_ttm = round(sum(ttms) / len(ttms), 2) if ttms else None

    return {
        "totalOutstanding": total_out,
        "totalBonds":       total_bonds,
        "issuersWithBonds": len(issuers),
        "maturingThisYear": round(mat_this, 2),
        "maturingNextYear": round(mat_next, 2),
        "esgBondCount":     esg_count,
        "avgTTM":           avg_ttm,
        "byYear":           dict(sorted(by_year.items())),
        "byYearSector":     {k: dict(sorted(v.items())) for k, v in sorted(by_year_sector.items())},
        "bySector":         dict(sorted(by_sector.items(), key=lambda x: -x[1])),
    }

# ── main ──────────────────────────────────────────────────────────────────────

async def main():
    if not TKRS.exists():
        raise SystemExit(f"Missing {TKRS}")
    tickers = json.loads(TKRS.read_text(encoding="utf-8"))["tickers"]
    print(f"Fetching bonds for {len(tickers)} tickers (throttle={THROTTLE}s, concurrency={MAX_CONCURRENT}) …")

    sem = asyncio.Semaphore(MAX_CONCURRENT)
    async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
        results = await asyncio.gather(*[fetch_issuer(client, t, sem) for t in tickers])

    issuers = [r for r in results if r is not None]
    print(f"  {len(issuers)}/{len(tickers)} tickers have outstanding bonds on ThaiBMA")

    for i in issuers:
        n = i["longCount"] + i["shortCount"]
        print(f"  {i['tk']:<10}  {i['totalOutstanding']:>8,.0f} M฿  {n} bond(s)  {i['rating']}")

    payload = {
        "version":  1,
        "asOf":     date.today().isoformat(),
        "_built_at": datetime.now(timezone.utc).isoformat(),
        "source":   "ThaiBMA /issuer/regissue (no auth required)",
        "summary":  build_summary(issuers),
        "issuers":  sorted(issuers, key=lambda x: -x["totalOutstanding"]),
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {len(issuers)} issuers → {OUT}")

if __name__ == "__main__":
    asyncio.run(main())
