"""
SETSMART proxy for the Coverage Morning Brief artifact.

Why this exists
---------------
The Cowork live artifact runs in a browser sandbox. SETSMART's API requires
authenticated calls and (in practice) does not permit cross-origin browser
requests. This thin proxy:

  1. Holds the API key server-side so it never lives in artifact source.
  2. Calls SETSMART REST endpoints, normalises the response into the shape
     the artifact expects.
  3. Returns CORS-permissive JSON to the artifact.
  4. Caches the aggregate response for COVERAGE_TTL_SEC seconds.

How to run
----------
  pip install fastapi uvicorn httpx
  export SETSMART_API_KEY="<your-uuid-key>"     # bash/zsh
  setx SETSMART_API_KEY "<your-uuid-key>"       # Windows
  uvicorn setsmart_proxy:app --host 127.0.0.1 --port 8765 --reload

Then in the artifact, open Settings → Mode = "Local proxy",
Proxy URL = http://127.0.0.1:8765/morning-brief, Save & reload.

The endpoint paths below are placeholders. Replace the URLs and JSON-parsing
in `fetch_ticker_snapshot` once you confirm them from the SETSMART Developer
Portal (under your subscription). The contract returned to the artifact is
fixed — fill in the parsing only.
"""

import os
import asyncio
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

try:
    from disclosure_thai import _enrich_thai
except ImportError:
    from scripts.disclosure_thai import _enrich_thai

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
# SETSMART's documented Company Fundamental Data API uses a simple header:
#     api-key: <UUID>
# That's it — no OAuth flow, no token exchange. Confirmed against the
# Company Fundamental spec V1.0 (2023-12-13).
#
# The earlier OAuth probing was hitting the wrong product surface (the
# SETSMART web app's session-bound endpoints). The /api/listed-company-api/
# routes documented in the spec just want the api-key header.

SETSMART_BASE       = os.environ.get("SETSMART_BASE", "https://www.setsmart.com/api").rstrip("/")
LISTED_BASE         = f"{SETSMART_BASE}/listed-company-api"
API_KEY             = (os.environ.get("SETSMART_API_KEY") or os.environ.get("SETSMART_ACCESS_TOKEN") or "").strip()
COVERAGE_TTL_SEC    = int(os.environ.get("COVERAGE_TTL_SEC", "600"))    # 10 min
HTTP_TIMEOUT        = float(os.environ.get("HTTP_TIMEOUT", "30"))

# Surveillance bridge: if set, Disclosure Pulse reads classified items
# from your surveillance DuckDB instead of polling news/search live.
# The pipeline at c:\!VSCODE_Folder\SET_SETSMART_API\surveillance\ writes
# classifier output (Sonnet 4.6 critical/material tags). This proxy reads.
SURVEILLANCE_DB_PATH    = os.environ.get("SURVEILLANCE_DB_PATH", "").strip()
SURVEILLANCE_TABLE      = os.environ.get("SURVEILLANCE_TABLE", "news_items").strip()
SURVEILLANCE_SQL        = os.environ.get("SURVEILLANCE_SQL", "").strip()    # full custom override
# SETSMART rate-limits aggressively at concurrency ≥ 2 on this tier — empirical
# testing showed silent drops of one of every two simultaneous EOD requests
# even with retry. Sequential (=1) is the only fully reliable mode.
# Tune up via env var only if your subscription explicitly supports it.
# Cost of sequential: ~0.8s per call → ~40s for the full 50-name morning brief
# scan (cached COVERAGE_TTL_SEC = 10 min, so this only hits on first request).
MAX_CONCURRENT      = int(os.environ.get("SETSMART_MAX_CONCURRENT", "1"))

# Segment mapping — sub-sector overlay for the heatmap. Adjust as your
# coverage classification evolves.
SEGMENT: Dict[str, str] = {
    # FOOD
    "TU":"Seafood", "ASIAN":"Seafood", "CFRESH":"Seafood",
    "ITC":"Pet Food", "AAI":"Pet Food",
    "TFMAMA":"Noodles", "SST":"Noodles",
    "PRG":"Snacks/Bakery", "SNP":"Snacks/Bakery", "SSF":"Snacks/Bakery", "PB":"Snacks/Bakery",
    "M":"Restaurant", "ZEN":"Restaurant", "OKJ":"Restaurant", "MADAME":"Restaurant",
    "PQS":"Other Food", "TWPC":"Other Food", "CHOTI":"Other Food", "TC":"Other Food", "XBIO":"Other Food",
    # PROP
    "CPN":"Retail", "MBK":"Retail", "PLAT":"Retail",
    "WHA":"IE", "AMATA":"IE", "AMATAV":"IE", "ROJNA":"IE", "NNCL":"IE", "PIN":"IE",
    "AWC":"Mixed/Hospitality", "J":"Residential", "BLAND":"Residential", "JCK":"Residential", "WIN":"Residential",
    # PFREIT
    "WHART":"Industrial REIT", "FTREIT":"Industrial REIT", "WHAIR":"Industrial REIT",
    "AMATAR":"Industrial REIT", "TIF1":"Industrial PF", "TTLPF":"Industrial PF", "TNPF":"Industrial PF",
    "CPNREIT":"Retail REIT", "LHSC":"Retail REIT", "ALLY":"Retail REIT",
    "AIMCG":"Office/Mixed REIT", "IMPACT":"Office/Mixed REIT",
    "SSTRT":"Hospitality REIT",
    "HPF":"Other PF", "MJLF":"Other PF", "AXTRART":"Other REIT",
}

COVERAGE: List[Dict[str, str]] = [
    # FOOD (20)
    *[{"tk": t, "sector": "FOOD",   "segment": SEGMENT.get(t, "Other")} for t in [
        "PRG","ITC","AAI","CFRESH","TU","PQS","TFMAMA","TWPC","SNP","SSF",
        "M","ZEN","PB","ASIAN","CHOTI","OKJ","TC","SST","MADAME","XBIO"
    ]],
    # PROP (14)
    *[{"tk": t, "sector": "PROP",   "segment": SEGMENT.get(t, "Other")} for t in [
        "CPN","WHA","PIN","MBK","AMATAV","AWC","AMATA","PLAT","NNCL","J",
        "BLAND","WIN","JCK","ROJNA"
    ]],
    # PFREIT (16)
    *[{"tk": t, "sector": "PFREIT", "segment": SEGMENT.get(t, "Other")} for t in [
        "SSTRT","TNPF","AIMCG","FTREIT","ALLY","CPNREIT","IMPACT","AMATAR",
        "HPF","TIF1","TTLPF","WHAIR","WHART","LHSC","AXTRART","MJLF"
    ]],
]

# ------------------------------------------------------------------
# Risk keyword scanner (Disclosure Pulse)
# ------------------------------------------------------------------
# Keywords are matched case-insensitively against the announcement title
# (and body if your SETSMART tier returns it). Each keyword carries a
# severity weight. A filing's severity = max(keyword weights) it matches,
# floored by its filing type (Material Info > Cap Action > MD&A > AGM > Other).

RISK_KEYWORDS = [
    # severity, label,           regex (case-insensitive)
    ("high",   "going concern",      r"going concern|ความสามารถในการดำเนินงาน"),
    ("high",   "qualified opinion",  r"qualified opinion|มีเงื่อนไข|ไม่แสดงความเห็น|adverse opinion|disclaimer of opinion"),
    ("high",   "default",            r"\bdefault\b|ผิดนัด|ผิดเงื่อนไข"),
    ("high",   "restatement",        r"restate|แก้ไขงบ"),
    ("high",   "material weakness",  r"material weakness"),
    ("medium", "impairment",         r"impair|ด้อยค่า"),
    ("medium", "related party",      r"related party|รายการเกี่ยวโยง|connected (transaction|party)"),
    ("medium", "contingent",         r"contingent (liabilit|asset)|หนี้สินที่อาจเกิด"),
    ("medium", "loss",               r"\bnet loss\b|ขาดทุนสุทธิ"),
    ("medium", "delay",              r"delay|ล่าช้า|extension to file"),
    ("low",    "dividend",           r"dividend|เงินปันผล|XD"),
    ("low",    "AGM",                r"\bAGM\b|annual general meeting|สามัญผู้ถือหุ้น"),
]

TYPE_FLOOR = {
    "Material":   "high",
    "Cap Action": "medium",
    "FS":         "medium",
    "MD&A":       "low",
    "Governance": "low",
    "AGM":        "low",
    "Other":      "low",
}

SEVERITY_RANK = {"low": 0, "medium": 1, "high": 2}


def scan_keywords(text: str):
    """Return list of {label, severity} for keywords matched in `text`."""
    import re as _re
    if not text:
        return []
    hits = []
    seen = set()
    for sev, label, pat in RISK_KEYWORDS:
        if label in seen:
            continue
        if _re.search(pat, text, _re.IGNORECASE):
            hits.append({"label": label, "severity": sev})
            seen.add(label)
    return hits


def classify_type(raw_type: str, title: str) -> str:
    """Map SETSMART filing types to one of the artifact's bins."""
    s = ((raw_type or "") + " " + (title or "")).lower()
    if any(k in s for k in ("material", "ข้อมูลที่มีนัยสำคัญ", "สารสนเทศ")): return "Material"
    if any(k in s for k in ("right offering", "private placement", "warrant", "capital reduction", "ทุนจดทะเบียน", "เพิ่มทุน", "ลดทุน")): return "Cap Action"
    if any(k in s for k in ("md&a", "management discussion", "คำอธิบายและการวิเคราะห์")): return "MD&A"
    if any(k in s for k in ("financial statement", "f45", "งบการเงิน", "56-1")): return "FS"
    if any(k in s for k in ("agm", "egm", "annual general meeting", "ผู้ถือหุ้น")): return "AGM"
    if any(k in s for k in ("director", "audit committee", "related party", "connected", "กรรมการ", "เกี่ยวโยง")): return "Governance"
    return "Other"


# ------------------------------------------------------------------
# In-memory cache (per-route)
# ------------------------------------------------------------------
_cache: Dict[str, Any] = {"ts": 0.0, "payload": None}
_disc_cache: Dict[str, Any] = {"ts": 0.0, "payload": None, "days": None}
_heat_cache: Dict[str, Any] = {"ts": 0.0, "payload": None}
_alert_cache: Dict[str, Any] = {"ts": 0.0, "payload": None}

# ------------------------------------------------------------------
# Unusual Trading Alert — thresholds
# ------------------------------------------------------------------
# Each alert type has three thresholds (low / medium / high). The lowest
# is the trigger floor — readings below `low` produce no alert. The base
# severity is the highest band the value clears. If no SET filing exists
# within ±24h of the alert, severity is bumped one notch (max "high").

ALERT_THRESHOLDS = {
    "vol_spike":   {"low": 2.0,  "medium": 3.0,  "high": 4.0,  "unit": "σ"},
    "gap":         {"low": 3.0,  "medium": 5.0,  "high": 8.0,  "unit": "%"},
    "intraday":    {"low": 4.0,  "medium": 6.0,  "high": 9.0,  "unit": "%"},
}

ALERT_LABELS = {
    "vol_spike":  "Volume spike",
    "gap":        "Price gap",
    "intraday":   "Intraday move",
}

# Metric definitions used by the heatmap. `direction`:
#   "cheap-good" — low value is favourable (PE, PBV, EV/EBITDA)
#   "high-good"  — high value is favourable (DY, NPM)
HEATMAP_METRICS = [
    {"key": "PE",       "label": "PE",        "direction": "cheap-good", "decimals": 1},
    {"key": "PBV",      "label": "PBV",       "direction": "cheap-good", "decimals": 2},
    {"key": "DY",       "label": "DY %",      "direction": "high-good",  "decimals": 2},
    {"key": "EVEBITDA", "label": "EV/EBITDA", "direction": "cheap-good", "decimals": 1},
    {"key": "NPM",      "label": "NPM %",     "direction": "high-good",  "decimals": 2},
]


# ------------------------------------------------------------------
# Auth — SETSMART Company Fundamental API uses a single api-key header
# ------------------------------------------------------------------
def _auth_headers_sync() -> Dict[str, str]:
    if not API_KEY:
        raise HTTPException(500, "SETSMART_API_KEY env var is not set.")
    return {"api-key": API_KEY, "Accept": "application/json"}


async def _auth_headers() -> Dict[str, str]:
    return _auth_headers_sync()


# ------------------------------------------------------------------
# SETSMART fetch — adjust endpoints to match your subscription
# ------------------------------------------------------------------
async def _get_with_retry(client: Optional[httpx.AsyncClient], url: str, params: Dict[str, Any],
                          *, retries: int = 3) -> Optional[Any]:
    """SETSMART drops requests under concurrent load on a shared client.
    Retry with back-off and switch to a fresh client on connection errors
    / empty responses. Returns parsed JSON or None on permanent failure."""
    own_client = client is None
    for attempt in range(retries + 1):
        c = client if (client is not None and attempt == 0) else None
        owns_this = c is None
        if owns_this:
            c = httpx.AsyncClient(timeout=HTTP_TIMEOUT)
        try:
            r = await c.get(url, headers=_auth_headers_sync(), params=params)
            if r.status_code in (429, 500, 502, 503, 504):
                await asyncio.sleep(0.4 * (attempt + 1))
                continue
            if r.status_code >= 400:
                return None
            try:
                return r.json()
            except Exception:
                return None
        except (httpx.RequestError, httpx.TimeoutException):
            await asyncio.sleep(0.4 * (attempt + 1))
        finally:
            if owns_this and c is not None:
                await c.aclose()
    return None


async def fetch_eod_series(client: httpx.AsyncClient, tk: str, *, years: int = 1) -> List[Dict[str, Any]]:
    """Pull `years` of EOD daily snapshots for one ticker.

    Endpoint: GET /api/listed-company-api/eod-price-by-symbol
    Per-row fields used downstream: date, close, totalVolume, pe, pbv,
    bvps, dividendYield, marketCap.
    """
    end = datetime.now(timezone.utc).astimezone().date()
    start = (end - __import__("datetime").timedelta(days=int(years * 366) + 5)).isoformat()
    params = {
        "symbol": tk,
        "startDate": start,
        "endDate": end.isoformat(),
        "adjustedPriceFlag": "Y",
    }
    data = await _get_with_retry(client, f"{LISTED_BASE}/eod-price-by-symbol", params)
    return data if isinstance(data, list) else []


async def fetch_ticker_snapshot(client: httpx.AsyncClient, tk: str) -> Dict[str, Any]:
    """Morning-brief fields from SETSMART eod-price-by-symbol.

    The Company Fundamental API does not expose announcements; the
    `filings` field is populated by build_morning_brief by joining with
    the public news/search counts.
    """
    rows = await fetch_eod_series(client, tk, years=1)
    if not rows:
        return {"_err": "no_eod_data", "tk": tk}

    # Newest last
    rows.sort(key=lambda r: r.get("date") or "")
    # Drop both null AND 0 closes/volumes. SETSMART returns close=0 with
    # volume=0 on days the ticker didn't trade (illiquid stocks, pre-EOD
    # builds on a trading day, suspensions). Treating those as real prices
    # produces spurious -100% returns and zeroed sparklines.
    closes = [r.get("close") for r in rows if r.get("close")]
    vols   = [r.get("totalVolume") for r in rows if r.get("totalVolume")]
    today_iso = datetime.now(timezone.utc).astimezone().date().isoformat()
    year_str  = today_iso[:4]
    month_str = today_iso[:7]

    last = closes[-1] if closes else None
    prev_1d = closes[-2] if len(closes) >= 2 else None
    prev_5d = closes[-6] if len(closes) >= 6 else None
    # MTD reference = last close BEFORE current month started (i.e., end of prior month).
    # YTD reference = last close BEFORE current year started (i.e., end of prior year).
    # If the latest available data is itself before today's month/year, fall back to
    # the first close inside the most recent month/year present in the series.
    prev_mtd = None
    prev_ytd = None
    for r in reversed(rows):
        d = r.get("date") or ""
        c = r.get("close")
        if not c: continue  # skip no-trade days
        if prev_mtd is None and d[:7] < month_str: prev_mtd = c
        if prev_ytd is None and d[:4] < year_str: prev_ytd = c
        if prev_mtd is not None and prev_ytd is not None: break

    avg_vol_20d = (sum(vols[-20:]) / 20) if len(vols) >= 20 else None
    last_vol    = vols[-1] if vols else None

    last_252   = closes[-252:] if len(closes) >= 252 else closes
    hi52 = bool(last is not None and last_252 and last >= max(last_252) * 0.998)
    lo52 = bool(last is not None and last_252 and last <= min(last_252) * 1.002)

    def _pct(curr, base):
        if curr is None or base in (None, 0): return None
        return round((curr / base - 1) * 100, 2)

    return {
        "tk": tk,
        "last": last,
        "pct1d":  _pct(last, prev_1d),
        "pct5d":  _pct(last, prev_5d),
        "pctMtd": _pct(last, prev_mtd),
        "pctYtd": _pct(last, prev_ytd),
        "volRatio": round(last_vol / avg_vol_20d, 2) if last_vol and avg_vol_20d else None,
        # `filings` is populated by the news cross-ref pass in build_morning_brief.
        "filings": None,
        "hi52": hi52, "lo52": lo52,
        "path": closes[-20:],
    }


async def build_morning_brief() -> Dict[str, Any]:
    sem = asyncio.Semaphore(MAX_CONCURRENT)
    async def _one(client, tk):
        async with sem:
            return await fetch_ticker_snapshot(client, tk)
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        snaps = await asyncio.gather(*[_one(client, c["tk"]) for c in COVERAGE])
    rows = []
    errors = 0
    for meta, snap in zip(COVERAGE, snaps):
        if "_err" in snap:
            errors += 1
            continue
        snap["sector"] = meta["sector"]
        rows.append(snap)
    return {
        "rows": rows,
        "asOf": datetime.now(timezone.utc).astimezone().date().isoformat(),
        "source": f"SETSMART API · {len(rows)}/{len(COVERAGE)} ok" + (f" · {errors} errs" if errors else ""),
    }


# ------------------------------------------------------------------
# Disclosure Pulse — fetch + aggregate
# ------------------------------------------------------------------
async def fetch_disclosures(client: httpx.AsyncClient, tk: str, days: int) -> List[Dict[str, Any]]:
    """News for one ticker via SET's PUBLIC news/search endpoint.

    The SETSMART Company Fundamental subscription does not include news.
    The official IR Website News API is on a separate subscription that
    this api-key does not authorise.

    The set.or.th public news/search endpoint is undocumented but stable
    — same source the user's surveillance project (set_mcp/surveillance)
    has been polling for 90+ days. Requires:
      - browser-style User-Agent + Accept headers
      - cookie warmup against the homepage to clear Incapsula
      - throttle ≥ 0.6 s/req (~1.6 req/s) — see SET_NEWS_THROTTLE_S
      - date format DD/MM/YYYY (Thai convention, ISO returns 400)

    Returns each item shaped to the disclosure-pulse contract.
    """
    await _set_news_session_init()            # cookies + warmup, idempotent
    items_en = await _set_news_search(client, tk, lang="en", days=days)
    # Optional: also pull TH for headlines that aren't bilingual; the user
    # noted EN/TH IDs are paired (ending 00 / 01). Pulling EN-only is enough
    # for surveillance because both languages cover the same disclosure.
    out = []
    for it in items_en:
        ts   = it.get("datetime")
        url  = it.get("url") or ""
        head = it.get("headline") or ""
        out.append({
            "ts":       ts,
            "raw_type": (it.get("source") or ""),
            "title":    head,
            "lang":     (it.get("lang") or "en").upper()[:2],
            "url":      url,
            "_id":      str(it.get("id") or ""),
        })
    return out


# ------------------------------------------------------------------
# Surveillance DuckDB bridge — read classified items, skip live polling
# ------------------------------------------------------------------
# When SURVEILLANCE_DB_PATH is set the proxy reads from your existing
# surveillance pipeline's DuckDB. That pipeline already polled news/search,
# deduplicated, and classified each disclosure with Sonnet 4.6 (critical /
# material / noise). The bridge:
#
#   - opens DuckDB read-only so it can't lock out the writer cron
#   - introspects the table to handle whatever column names you chose
#   - runs ONE SQL across all 50 names instead of 50 HTTP calls
#   - maps your classifier's severity to the artifact's high/medium/low
#   - falls back to live polling if the DB is missing or empty
#
# Severity mapping (case-insensitive):
#   critical / high / red                → "high"
#   material / medium / amber / yellow   → "medium"
#   anything else (noise / routine /
#       low / null / unclassified)       → "low"

# Column synonyms — first match wins. Extend if your schema uses other names.
_DB_COL_SYNONYMS: Dict[str, List[str]] = {
    "id":       ["id", "news_id", "newsId", "newsid"],
    "datetime": ["datetime", "publish_date", "published_at", "publish_at", "ts", "publishDate", "publishedat", "datetime_utc"],
    "symbol":   ["symbol", "ticker", "tk"],
    "headline": ["headline", "title", "head_line", "subject"],
    "url":      ["url", "link", "newsUrl", "news_url"],
    "lang":     ["lang", "language", "lang_code"],
    "severity": ["severity", "severity_level", "classification_severity", "classification_level",
                 "level", "tier", "classified_severity", "alert_tier"],
    "summary":  ["analyst_summary", "summary", "classified_summary", "rationale", "analyst_rationale", "explanation"],
    "category": ["event_type", "category", "type", "classification_type", "event_category", "kind"],
    "classified_at": ["classified_at", "classification_ts", "classified_on", "classify_ts"],
}

_SEVERITY_TO_ARTIFACT = {
    "critical": "high", "high": "high", "red": "high", "h": "high",
    "material": "medium", "medium": "medium", "amber": "medium", "yellow": "medium", "m": "medium",
    # everything else => low
}


def _open_surveillance_db():
    """Open the surveillance DuckDB read-only. Returns a connection or None
    if the bridge is disabled / DB missing / duckdb not installed.

    Logs to stderr when a configured DB path fails to open — silent failure
    here previously cost an hour debugging a duckdb version mismatch.
    """
    if not SURVEILLANCE_DB_PATH:
        return None
    if not os.path.exists(SURVEILLANCE_DB_PATH):
        import sys as _sys
        print(f"[disclosure-pulse] DB path set but not found: {SURVEILLANCE_DB_PATH}",
              file=_sys.stderr, flush=True)
        return None
    try:
        import duckdb  # type: ignore
    except ImportError:
        import sys as _sys
        print("[disclosure-pulse] duckdb not installed — cannot use bridge",
              file=_sys.stderr, flush=True)
        return None
    try:
        # read_only=True is critical: prevents locking out the writer cron
        return duckdb.connect(SURVEILLANCE_DB_PATH, read_only=True)
    except Exception as e:
        import sys as _sys
        print(f"[disclosure-pulse] duckdb.connect failed for {SURVEILLANCE_DB_PATH}: "
              f"{type(e).__name__}: {e}", file=_sys.stderr, flush=True)
        return None


def _resolve_columns(con, table: str) -> Dict[str, Optional[str]]:
    """Inspect the table; return {standard_name: actual_column_name_or_None}."""
    try:
        rows = con.execute(f"PRAGMA table_info('{table}')").fetchall()
    except Exception:
        try:
            rows = con.execute(
                "SELECT column_name FROM information_schema.columns WHERE table_name = ?",
                [table]
            ).fetchall()
            rows = [(0, r[0]) for r in rows]
        except Exception:
            return {k: None for k in _DB_COL_SYNONYMS}
    available = {str(r[1]).lower(): str(r[1]) for r in rows} if rows else {}
    out: Dict[str, Optional[str]] = {}
    for std, candidates in _DB_COL_SYNONYMS.items():
        out[std] = next((available[c.lower()] for c in candidates if c.lower() in available), None)
    return out


def _classifier_severity(raw: Optional[str]) -> str:
    if not raw:
        return "low"
    return _SEVERITY_TO_ARTIFACT.get(str(raw).strip().lower(), "low")


def _build_db_select(cols: Dict[str, Optional[str]], table: str) -> Optional[str]:
    """Build a SELECT that returns standard column names, or None if the
    minimal-required set is missing."""
    required = ["id", "datetime", "symbol", "headline"]
    if not all(cols.get(k) for k in required):
        return None
    def _col(std: str) -> str:
        c = cols.get(std)
        return f'"{c}" AS {std}' if c else f"NULL AS {std}"
    sel = ",\n        ".join(_col(k) for k in _DB_COL_SYNONYMS.keys())
    sym = cols["symbol"]
    dt  = cols["datetime"]
    return f"""
SELECT
        {sel}
FROM "{table}"
WHERE upper("{sym}") IN ({{symbols_in}})
  AND "{dt}" >= ?
ORDER BY "{dt}" DESC
"""


async def fetch_classified_disclosures(days: int) -> Optional[List[Dict[str, Any]]]:
    """Return classified disclosures for the full coverage from DuckDB.
    Returns None if the bridge is unavailable (so the caller can fall back).
    Returns [] if the DB is reachable but has no rows in the window."""
    con = _open_surveillance_db()
    if con is None:
        return None
    try:
        if SURVEILLANCE_SQL:
            sql = SURVEILLANCE_SQL
            symbols_param = [c["tk"] for c in COVERAGE]
            cutoff = datetime.now(timezone.utc).astimezone() - __import__("datetime").timedelta(days=days)
            try:
                rows = con.execute(sql, [symbols_param, cutoff]).fetchall()
            except Exception:
                rows = con.execute(sql, [tuple(symbols_param), cutoff]).fetchall()
            cols = list(_DB_COL_SYNONYMS.keys())
        else:
            col_map = _resolve_columns(con, SURVEILLANCE_TABLE)
            base = _build_db_select(col_map, SURVEILLANCE_TABLE)
            if not base:
                return None
            symbols = [c["tk"] for c in COVERAGE]
            placeholders = ",".join("?" * len(symbols))
            sql = base.format(symbols_in=placeholders)
            cutoff = datetime.now(timezone.utc).astimezone() - __import__("datetime").timedelta(days=days)
            rows = con.execute(sql, [*[s.upper() for s in symbols], cutoff]).fetchall()
            cols = list(_DB_COL_SYNONYMS.keys())

        # Build a lookup: which row index is which standard name
        idx = {name: i for i, name in enumerate(cols)}
        out: List[Dict[str, Any]] = []
        sector_by_tk = {c["tk"]: c["sector"] for c in COVERAGE}
        for r in rows:
            tk = (r[idx["symbol"]] or "").upper()
            if tk not in sector_by_tk:
                continue
            ts_raw = r[idx["datetime"]]
            if hasattr(ts_raw, "isoformat"):
                ts = ts_raw.isoformat()
            else:
                ts = str(ts_raw) if ts_raw else None
            head = r[idx["headline"]] or ""
            sev_raw = r[idx["severity"]] if idx.get("severity") is not None else None
            sev = _classifier_severity(sev_raw)
            kws = scan_keywords(head) if not sev_raw else []      # only run scanner when classifier silent
            cat = r[idx["category"]] if idx.get("category") is not None else None
            ftype = cat or classify_type("", head)
            out.append({
                "tk": tk, "sector": sector_by_tk[tk],
                "ts": ts, "type": ftype,
                "title": head,
                "lang": str(r[idx["lang"]] or "EN").upper()[:2] if idx.get("lang") is not None else "EN",
                "url":  r[idx["url"]] or "" if idx.get("url") is not None else "",
                "keywords": kws,
                "severity": sev,
                "_id": str(r[idx["id"]] or ""),
                "_source": "duckdb",
                "_classifier_raw": (str(sev_raw).strip() if sev_raw else None),
                "_summary": (r[idx["summary"]] if idx.get("summary") is not None else None),
            })
        return _enrich_thai(con, out)
    except Exception:
        return None
    finally:
        try:
            con.close()
        except Exception:
            pass


# ------------------------------------------------------------------
# SET public news/search client (Incapsula-aware, throttled)
# ------------------------------------------------------------------
SET_PUBLIC_BASE       = os.environ.get("SET_PUBLIC_BASE", "https://www.set.or.th").rstrip("/")
SET_NEWS_THROTTLE_S   = float(os.environ.get("SET_NEWS_THROTTLE_S", "0.65"))
_set_news_state: Dict[str, Any] = {
    "cookies": None,         # httpx.Cookies after warmup
    "init_at": 0.0,
    "last_call": 0.0,
    "init_lock": asyncio.Lock(),
    "throttle_lock": asyncio.Lock(),
}
_SET_BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Referer": "https://www.set.or.th/en/market/news-and-alert/news",
}


async def _set_news_session_init() -> None:
    """One-time-per-hour cookie warmup against the homepage. Without this,
    Incapsula returns 403 with a self-loading challenge iframe."""
    async with _set_news_state["init_lock"]:
        # Re-warm every 50 minutes to be safe vs Incapsula session expiry
        if _set_news_state["cookies"] is not None and (time.time() - _set_news_state["init_at"]) < 3000:
            return
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, follow_redirects=True) as c:
            warm_headers = {
                "User-Agent": _SET_BROWSER_HEADERS["User-Agent"],
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": _SET_BROWSER_HEADERS["Accept-Language"],
                "Sec-Fetch-Dest": "document",
            }
            try:
                r = await c.get(f"{SET_PUBLIC_BASE}/", headers=warm_headers)
                _set_news_state["cookies"] = r.cookies
            except Exception:
                _set_news_state["cookies"] = None
            _set_news_state["init_at"] = time.time()


async def _set_news_throttle() -> None:
    async with _set_news_state["throttle_lock"]:
        wait = (_set_news_state["last_call"] + SET_NEWS_THROTTLE_S) - time.time()
        if wait > 0:
            await asyncio.sleep(wait)
        _set_news_state["last_call"] = time.time()


async def _set_news_search(_client: httpx.AsyncClient, symbol: str, *, lang: str = "en", days: int = 7) -> List[Dict[str, Any]]:
    """One symbol. Returns the raw newsInfoList items (or empty on failure)."""
    await _set_news_session_init()
    await _set_news_throttle()
    end = datetime.now(timezone.utc).astimezone().date()
    start = end - __import__("datetime").timedelta(days=max(1, days))
    params = {
        "symbol": symbol,
        "lang": lang,
        "fromDate": start.strftime("%d/%m/%Y"),
        "toDate":   end.strftime("%d/%m/%Y"),
    }
    cookies = _set_news_state.get("cookies")
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT, cookies=cookies, follow_redirects=True) as c:
            r = await c.get(f"{SET_PUBLIC_BASE}/api/set/news/search",
                            headers=_SET_BROWSER_HEADERS, params=params)
        if r.status_code != 200:
            return []
        data = r.json()
        return data.get("newsInfoList") or []
    except Exception:
        return []

    # SETSMART responses commonly wrap items in a "data" or "items" key.
    items = data.get("data") or data.get("items") or data if isinstance(data, list) else []
    out = []
    for it in items:
        out.append({
            "ts":       it.get("publishedAt") or it.get("postDate") or it.get("date"),
            "raw_type": it.get("type") or it.get("category") or "",
            "title":    it.get("title") or it.get("headline") or "",
            "lang":     (it.get("language") or "EN").upper()[:2],
            "url":      it.get("url") or it.get("link") or "",
        })
    return out


async def build_disclosure_pulse(days: int = 7) -> Dict[str, Any]:
    # PATH A — bridge to surveillance DuckDB when configured.
    # Uses Sonnet-classified severity (critical/material) directly. One
    # SQL query returns all 50 names, no Incapsula concerns, no throttling.
    db_items = await fetch_classified_disclosures(days)
    if db_items is not None:
        return _shape_disclosure_payload(
            flat_filings=db_items,
            days=days,
            source=f"surveillance DuckDB ({len(db_items)} classified items, {days}d)",
            mode="duckdb",
        )

    # PATH B — live polling of public news/search.
    # The throttle in _set_news_search paces calls (~1.6 req/s).
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        all_items = await asyncio.gather(*[
            fetch_disclosures(client, c["tk"], days) for c in COVERAGE
        ])

    flat: List[Dict[str, Any]] = []
    for meta, raw_items in zip(COVERAGE, all_items):
        for it in raw_items:
            ftype = classify_type(it["raw_type"], it["title"])
            kws = scan_keywords(it["title"])
            sev = TYPE_FLOOR.get(ftype, "low")
            for h in kws:
                if SEVERITY_RANK[h["severity"]] > SEVERITY_RANK[sev]:
                    sev = h["severity"]
            flat.append({
                "tk": meta["tk"], "sector": meta["sector"],
                "ts": it["ts"], "type": ftype,
                "title": it["title"], "lang": it["lang"], "url": it["url"],
                "keywords": kws, "severity": sev,
                "_id": str(it.get("_id") or ""),
                "_source": "live",
            })
    return _shape_disclosure_payload(
        flat_filings=flat,
        days=days,
        source=f"public news/search · {len(COVERAGE)} symbols · {days}d window",
        mode="live",
    )


def _shape_disclosure_payload(*, flat_filings: List[Dict[str, Any]], days: int,
                              source: str, mode: str) -> Dict[str, Any]:
    """Produce the canonical disclosure-pulse payload (filings + per-ticker status)
    from a flat list of filing dicts. Used by both the DuckDB and live paths."""
    now = datetime.now(timezone.utc).astimezone()

    local_tz = now.tzinfo
    def _parse(ts):
        if not ts: return None
        try:
            d = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        except Exception:
            return None
        # Naive datetimes (e.g. from DuckDB without tz) — assume local tz
        if d.tzinfo is None:
            d = d.replace(tzinfo=local_tz)
        return d

    # Group by ticker for status rollup
    by_tk: Dict[str, List[Dict[str, Any]]] = {}
    for f in flat_filings:
        by_tk.setdefault(f["tk"], []).append(f)

    status: List[Dict[str, Any]] = []
    sector_lookup = {c["tk"]: c["sector"] for c in COVERAGE}
    for meta in COVERAGE:
        tk = meta["tk"]
        tk_items = by_tk.get(tk, [])
        parsed = [(_parse(f["ts"]), f) for f in tk_items]
        parsed = [(d, f) for d, f in parsed if d is not None]
        last_filed_ts = max((d for d, _ in parsed), default=None)
        n24h = sum(1 for d, _ in parsed if (now - d).total_seconds() <= 86400)
        n7d  = sum(1 for d, _ in parsed if (now - d).days <= 7)
        n30d = sum(1 for d, _ in parsed if (now - d).days <= 30)
        status.append({
            "tk": tk, "sector": meta["sector"],
            "lastFiledTs": last_filed_ts.isoformat() if last_filed_ts else None,
            "n24h": n24h, "n7d": n7d, "n30d": n30d,
            "silentDays": (now - last_filed_ts).days if last_filed_ts else None,
            "overdue": [],
        })

    def _sort_key(f):
        d = _parse(f.get("ts"))
        return d if d else datetime.min.replace(tzinfo=timezone.utc)
    flat_filings = sorted(flat_filings, key=_sort_key, reverse=True)

    return {
        "asOf": now.date().isoformat(),
        "windowDays": days,
        "source": source,
        "mode": mode,
        "filings": flat_filings,
        "status": status,
    }


# ------------------------------------------------------------------
# Sector Heatmap — fetch + aggregate
# ------------------------------------------------------------------
def percentile_rank(value: Optional[float], series: List[float]) -> Optional[float]:
    """Return the percentile rank (0-100) of `value` within `series`. Treats
    None / NaN as missing — returns None if either input is unusable."""
    if value is None or series is None:
        return None
    cleaned = [x for x in series if x is not None and not (isinstance(x, float) and (x != x))]
    if not cleaned:
        return None
    n = sum(1 for x in cleaned if x <= value)
    return round(100.0 * n / len(cleaned), 1)


async def fetch_financial_quarters(client: httpx.AsyncClient, tk: str, *, since_year: int = 2019) -> List[Dict[str, Any]]:
    """Pull quarterly fundamentals from financial-data-and-ratio-by-symbol.
    Returns the array sorted oldest → newest by (year, quarter).

    NOTE: endYear/endQuarter are nominally optional in the spec, but in
    practice omitting them returns only the single startYear/startQuarter
    record. Both are set explicitly here to cover the full range.
    """
    today = datetime.now(timezone.utc).astimezone().date()
    end_year = today.year
    end_quarter = (today.month - 1) // 3 + 1
    params = {
        "symbol": tk,
        "startYear":   str(since_year),
        "startQuarter": "1",
        "endYear":     str(end_year),
        "endQuarter":  str(end_quarter),
    }
    data = await _get_with_retry(client, f"{LISTED_BASE}/financial-data-and-ratio-by-symbol", params)
    if not isinstance(data, list):
        return []
    data.sort(key=lambda x: (str(x.get("year") or ""), str(x.get("quarter") or "")))
    return data


async def fetch_valuation(client: httpx.AsyncClient, tk: str) -> Dict[str, Any]:
    """Real SETSMART implementation:
        - PE, PBV, DY, marketCap come from eod-price-by-symbol (per-day)
        - NPM, ROE, ROA come from financial-data-and-ratio-by-symbol (quarterly)
        - EV/EBIT proxy (labelled EV/EBITDA in the heatmap for visual continuity)
          = (marketCap_baht + totalLiabilities_thousand_baht * 1000) / (ebit_TTM_thousand_baht * 1000)

    Pulls 5Y of EOD (sampled monthly for history) and all available quarters of FS.
    """
    # SETSMART occasionally drops one of two concurrent requests on the
    # same TCP session. Sequential is safer; data isn't time-critical
    # because the result is cached for COVERAGE_TTL_SEC.
    eod_rows = await fetch_eod_series(client, tk, years=5)
    fs_rows  = await fetch_financial_quarters(client, tk, since_year=datetime.now().year - 5)
    out_cur: Dict[str, Optional[float]] = {"PE": None, "PBV": None, "DY": None, "EVEBITDA": None, "NPM": None}
    out_hist: Dict[str, List[float]]    = {"PE": [], "PBV": [], "DY": [], "EVEBITDA": [], "NPM": []}

    if eod_rows:
        eod_rows.sort(key=lambda r: r.get("date") or "")
        last_row = next((r for r in reversed(eod_rows) if r.get("close") is not None), eod_rows[-1])
        out_cur["PE"]  = last_row.get("pe")
        out_cur["PBV"] = last_row.get("pbv")
        out_cur["DY"]  = last_row.get("dividendYield")
        # Sample one row per calendar month for history (last business day of the month)
        last_per_month: Dict[str, Dict[str, Any]] = {}
        for r in eod_rows:
            d = r.get("date") or ""
            if len(d) >= 7:
                last_per_month[d[:7]] = r          # last write wins (rows are sorted)
        sampled = [last_per_month[k] for k in sorted(last_per_month.keys())][-60:]
        out_hist["PE"]  = [r.get("pe")             for r in sampled if r.get("pe") is not None]
        out_hist["PBV"] = [r.get("pbv")            for r in sampled if r.get("pbv") is not None]
        out_hist["DY"]  = [r.get("dividendYield")  for r in sampled if r.get("dividendYield") is not None]

    # NPM (latest quarter), and 5Y of NPM history
    if fs_rows:
        last_fs = fs_rows[-1]
        # Prefer Accum NPM (consolidated YTD) for current snapshot
        out_cur["NPM"] = last_fs.get("netProfitMarginAccum") or last_fs.get("netProfitMarginQuarter")
        out_hist["NPM"] = [(q.get("netProfitMarginQuarter") or q.get("netProfitMarginAccum"))
                           for q in fs_rows if (q.get("netProfitMarginQuarter") is not None
                                                or q.get("netProfitMarginAccum") is not None)]

        # EV/EBIT proxy — use marketCap (Baht) + totalLiabilities (k Baht * 1000),
        # divided by trailing-4Q EBIT (k Baht * 1000).
        if eod_rows and last_fs.get("totalLiabilities") is not None:
            mc = last_row.get("marketCap")
            tl = last_fs.get("totalLiabilities") or 0
            # Trailing 4 quarters of ebitQuarter (filter Nones)
            ebit_ttm_q = [q.get("ebitQuarter") for q in fs_rows[-4:] if q.get("ebitQuarter") is not None]
            ebit_ttm = sum(ebit_ttm_q) if len(ebit_ttm_q) == 4 else None
            if mc and ebit_ttm and ebit_ttm > 0:
                ev_baht = mc + tl * 1000.0
                out_cur["EVEBITDA"] = round(ev_baht / (ebit_ttm * 1000.0), 2)

        # Quarter-by-quarter EV/EBIT proxy history (rough — uses each quarter's
        # trailing EBIT against the period-end marketCap if we can find one).
        if eod_rows:
            # Map of YYYY-MM-DD → marketCap (latest in month, sampled monthly)
            mcap_by_month = {d: r.get("marketCap") for d, r in
                             [(r.get("date"), r) for r in eod_rows] if d and r.get("marketCap") is not None}
            ev_hist = []
            for i in range(3, len(fs_rows)):
                window = fs_rows[i-3:i+1]
                ebit_q = [q.get("ebitQuarter") for q in window if q.get("ebitQuarter") is not None]
                if len(ebit_q) != 4 or sum(ebit_q) <= 0:
                    continue
                period_end = fs_rows[i].get("dateAsof") or ""
                # Find the closest mcap on/before period_end
                mcap = next((mcap_by_month[k] for k in sorted(mcap_by_month.keys(), reverse=True)
                             if k <= period_end), None)
                tl = fs_rows[i].get("totalLiabilities") or 0
                if mcap is None:
                    continue
                ev_hist.append(round((mcap + tl * 1000.0) / (sum(ebit_q) * 1000.0), 2))
            out_hist["EVEBITDA"] = ev_hist

    return {"current": out_cur, "history": out_hist}


async def build_sector_heatmap() -> Dict[str, Any]:
    sem = asyncio.Semaphore(MAX_CONCURRENT)
    async def _one(client, tk):
        async with sem:
            return await fetch_valuation(client, tk)
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        results = await asyncio.gather(*[_one(client, c["tk"]) for c in COVERAGE])

    rows = []
    # Build per-ticker entries with self-percentiles
    for meta, vr in zip(COVERAGE, results):
        cur = vr.get("current", {}) or {}
        hist = vr.get("history", {}) or {}
        own_pct, vals = {}, {}
        for m in HEATMAP_METRICS:
            v = cur.get(m["key"])
            vals[m["key"]] = v
            own_pct[m["key"]] = percentile_rank(v, hist.get(m["key"], []) or [])
        rows.append({
            "tk": meta["tk"], "sector": meta["sector"], "segment": meta["segment"],
            "values": vals, "ownPct": own_pct,
        })

    # Compute percentile within sector cohort (current values only)
    sector_pct = {r["tk"]: {} for r in rows}
    for sector in {r["sector"] for r in rows}:
        cohort = [r for r in rows if r["sector"] == sector]
        for m in HEATMAP_METRICS:
            series = [r["values"].get(m["key"]) for r in cohort]
            for r in cohort:
                sector_pct[r["tk"]][m["key"]] = percentile_rank(r["values"].get(m["key"]),
                                                                 [x for x in series if x is not None])
    for r in rows:
        r["secPct"] = sector_pct.get(r["tk"], {})

    # Sector aggregates (median of current values)
    def _median(xs):
        xs = sorted(x for x in xs if x is not None)
        if not xs: return None
        n = len(xs)
        return xs[n//2] if n % 2 else round((xs[n//2 - 1] + xs[n//2]) / 2, 4)
    aggs = []
    for sector in ["FOOD", "PROP", "PFREIT"]:
        cohort = [r for r in rows if r["sector"] == sector]
        if not cohort:
            continue
        agg = {"sector": sector, "n": len(cohort), "values": {}}
        for m in HEATMAP_METRICS:
            agg["values"][m["key"]] = _median([r["values"].get(m["key"]) for r in cohort])
        aggs.append(agg)

    return {
        "asOf": datetime.now(timezone.utc).astimezone().date().isoformat(),
        "source": f"SETSMART valuation API · {sum(1 for r in rows if any(v is not None for v in r['values'].values()))}/{len(rows)} ok",
        "metrics": HEATMAP_METRICS,
        "rows": rows,
        "sectorAgg": aggs,
    }


# ------------------------------------------------------------------
# Unusual Trading Alert — fetch + compute
# ------------------------------------------------------------------
async def fetch_trading_stats(client: httpx.AsyncClient, tk: str) -> Dict[str, Any]:
    """Surveillance stats from EOD data only.

    The Company Fundamental spec gives us close, open, high, low, totalVolume
    per day — enough to fire the volume-spike, price-gap, and intraday-move
    checks. The previous Short/Spread/NVDR/Foreign checks have been
    removed — they need separate SETSMART subscriptions that this api-key
    does not authorise.
    """
    rows = await fetch_eod_series(client, tk, years=1)
    if not rows:
        return {}
    rows.sort(key=lambda r: r.get("date") or "")
    closes = [r.get("close") for r in rows if r.get("close") is not None]
    vols   = [r.get("totalVolume") for r in rows if r.get("totalVolume") is not None]
    if not closes or not vols:
        return {}

    last_row = rows[-1]
    prev_row = rows[-2] if len(rows) >= 2 else None
    last_close = last_row.get("close")
    prev_close = prev_row.get("close") if prev_row else None
    today_open = last_row.get("open")
    today_high = last_row.get("high")
    today_low  = last_row.get("low")
    today_vol  = last_row.get("totalVolume")

    vol_20 = vols[-21:-1] if len(vols) >= 21 else vols[:-1]
    if vol_20:
        avg = sum(vol_20) / len(vol_20)
        var = sum((v - avg) ** 2 for v in vol_20) / len(vol_20)
        std = var ** 0.5
    else:
        avg = std = None

    return {
        "last_close": last_close, "prev_close": prev_close,
        "today_open": today_open, "today_high": today_high, "today_low": today_low,
        "today_volume": today_vol,
        "vol_20d_avg": avg, "vol_20d_std": std,
    }


def _band(value: float, t: Dict[str, float]) -> Optional[str]:
    """Map a value to severity band by clearing thresholds."""
    if value is None or value < t["low"]:
        return None
    if value >= t["high"]:    return "high"
    if value >= t["medium"]:  return "medium"
    return "low"


def _bump(sev: str) -> str:
    return {"low": "medium", "medium": "high", "high": "high"}.get(sev, sev)


def compute_alerts_for_ticker(meta: Dict[str, str], stats: Dict[str, Any],
                              same_day_filings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Apply all checks; return list of alerts (possibly empty)."""
    alerts: List[Dict[str, Any]] = []

    def push(atype: str, value: float, label: str, evidence: Dict[str, Any]):
        sev = _band(value, ALERT_THRESHOLDS[atype])
        if sev is None:
            return
        # Cross-ref: do we have a same-day filing? If not, bump severity.
        linked = list(same_day_filings)
        if not linked:
            sev = _bump(sev)
        alerts.append({
            "tk": meta["tk"], "sector": meta["sector"],
            "type": ALERT_LABELS[atype], "atype": atype,
            "severity": sev,
            "value": round(value, 3),
            "label": label,
            "evidence": evidence,
            "filingsLinked": len(linked),
            "filingsTitles": [(f.get("title") or "")[:120] for f in linked[:3]],
        })

    if not stats:
        return alerts

    last  = stats.get("last_close")
    prev  = stats.get("prev_close")
    op    = stats.get("today_open")
    hi    = stats.get("today_high")
    lo    = stats.get("today_low")
    vol   = stats.get("today_volume")
    vavg  = stats.get("vol_20d_avg")
    vstd  = stats.get("vol_20d_std")

    # Volume spike (z-score)
    if vol is not None and vavg and vstd and vstd > 0:
        z = (vol - vavg) / vstd
        push("vol_spike", z, f"{z:.1f}σ vs 20D avg",
             {"vol": vol, "vol20dAvg": vavg, "vol20dStd": vstd})

    # Price gap (open vs prev close)
    if op is not None and prev:
        gap = abs(op - prev) / prev * 100.0
        push("gap", gap, f"{(op-prev)/prev*100:+.2f}% open gap",
             {"open": op, "prevClose": prev})

    # Intraday move (last vs open)
    if last is not None and op:
        m = abs(last - op) / op * 100.0
        push("intraday", m, f"{(last-op)/op*100:+.2f}% intraday",
             {"last": last, "open": op, "high": hi, "low": lo})

    return alerts


def _filings_within_24h_by_tk(filings: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """Group filings posted in the last 24h by ticker."""
    out: Dict[str, List[Dict[str, Any]]] = {}
    now = datetime.now(timezone.utc).astimezone()
    for f in filings:
        ts = f.get("ts")
        if not ts:
            continue
        try:
            d = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        except Exception:
            continue
        if (now - d).total_seconds() <= 86400:
            out.setdefault(f["tk"], []).append(f)
    return out


async def build_unusual_trading() -> Dict[str, Any]:
    sem = asyncio.Semaphore(MAX_CONCURRENT)
    async def _one(client, tk):
        async with sem:
            return await fetch_trading_stats(client, tk)
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        stats_results = await asyncio.gather(*[_one(client, c["tk"]) for c in COVERAGE])
    disc = await build_disclosure_pulse(days=1)

    filings_by_tk = _filings_within_24h_by_tk(disc.get("filings") or [])
    all_alerts: List[Dict[str, Any]] = []
    for meta, st in zip(COVERAGE, stats_results):
        all_alerts.extend(compute_alerts_for_ticker(meta, st, filings_by_tk.get(meta["tk"], [])))

    # Per-ticker rollup
    by_tk: Dict[str, Dict[str, Any]] = {}
    for a in all_alerts:
        e = by_tk.setdefault(a["tk"], {
            "tk": a["tk"], "sector": a["sector"],
            "alertCount": 0, "highestSeverity": "low",
            "filingsLinked": a["filingsLinked"],
            "alertTypes": [], "summary": [],
        })
        e["alertCount"] += 1
        if SEVERITY_RANK[a["severity"]] > SEVERITY_RANK[e["highestSeverity"]]:
            e["highestSeverity"] = a["severity"]
        e["alertTypes"].append({"atype": a["atype"], "type": a["type"], "severity": a["severity"]})
        e["summary"].append(f"{a['type']}: {a['label']}")

    rollup = sorted(by_tk.values(), key=lambda e: (
        -SEVERITY_RANK[e["highestSeverity"]],
        -e["alertCount"],
        e["filingsLinked"],
        e["tk"],
    ))

    return {
        "asOf": datetime.now(timezone.utc).astimezone().date().isoformat(),
        "source": f"SETSMART intraday API · {len(all_alerts)} alerts across {len(by_tk)} tickers",
        "thresholds": ALERT_THRESHOLDS,
        "alerts": all_alerts,
        "byTicker": rollup,
    }


# ------------------------------------------------------------------
# FastAPI app
# ------------------------------------------------------------------
app = FastAPI(title="SETSMART proxy for Coverage Morning Brief")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # local-only proxy; tighten if hosting
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    db_state: Dict[str, Any] = {"configured": bool(SURVEILLANCE_DB_PATH)}
    if SURVEILLANCE_DB_PATH:
        db_state["path"] = SURVEILLANCE_DB_PATH
        db_state["exists"] = os.path.exists(SURVEILLANCE_DB_PATH)
        try:
            import duckdb  # noqa: F401
            db_state["duckdb_installed"] = True
        except ImportError:
            db_state["duckdb_installed"] = False
    return {
        "ok": True,
        "key_present": bool(API_KEY),
        "base": SETSMART_BASE,
        "listed_base": LISTED_BASE,
        "coverage": len(COVERAGE),
        "live_endpoints": ["eod-price-by-symbol", "financial-data-and-ratio-by-symbol",
                           "set.or.th/api/set/news/search (public)"],
        "disclosure_source": "duckdb" if SURVEILLANCE_DB_PATH else "live news/search",
        "surveillance_db": db_state,
        "live_artifacts": ["morning-brief", "sector-heatmap", "unusual-trading", "disclosure-pulse"],
        "routes": ["/health", "/probe", "/probe/auth", "/probe/db",
                   "/morning-brief", "/disclosure-pulse", "/sector-heatmap", "/unusual-trading"],
    }


@app.get("/probe/db")
async def probe_db():
    """Inspect the surveillance DuckDB the bridge is configured to read.
    Returns: connection state, resolved column mapping, recent row counts.
    Useful for confirming your schema lines up before flipping the artifact."""
    if not SURVEILLANCE_DB_PATH:
        return JSONResponse({"ok": False, "error": "SURVEILLANCE_DB_PATH env var not set."}, status_code=400)
    if not os.path.exists(SURVEILLANCE_DB_PATH):
        return JSONResponse({"ok": False, "error": f"DB not found at {SURVEILLANCE_DB_PATH}"}, status_code=404)
    try:
        import duckdb  # type: ignore
    except ImportError:
        return JSONResponse({"ok": False, "error": "duckdb not installed in proxy venv: pip install duckdb"}, status_code=500)

    con = _open_surveillance_db()
    if con is None:
        return JSONResponse({"ok": False, "error": "duckdb.connect failed (file lock? permissions?)"}, status_code=500)
    try:
        tables = [r[0] for r in con.execute("SHOW TABLES").fetchall()]
        resolved = _resolve_columns(con, SURVEILLANCE_TABLE)
        try:
            total = con.execute(f'SELECT COUNT(*) FROM "{SURVEILLANCE_TABLE}"').fetchone()[0]
        except Exception as e:
            return JSONResponse({"ok": False, "error": f"can't query {SURVEILLANCE_TABLE}: {e}",
                                 "tables": tables, "resolved": resolved}, status_code=500)
        # Recent counts by severity (best-effort)
        sev_col = resolved.get("severity")
        sev_breakdown = None
        if sev_col:
            try:
                sev_breakdown = dict(con.execute(
                    f'SELECT lower("{sev_col}"), COUNT(*) FROM "{SURVEILLANCE_TABLE}" GROUP BY 1'
                ).fetchall())
            except Exception:
                pass
        # Check coverage hit rate
        sym_col = resolved.get("symbol")
        symbols_in_db = None
        if sym_col:
            try:
                covered = ",".join(["?"] * len(COVERAGE))
                in_db = con.execute(
                    f'SELECT DISTINCT "{sym_col}" FROM "{SURVEILLANCE_TABLE}" WHERE upper("{sym_col}") IN ({covered})',
                    [c["tk"] for c in COVERAGE],
                ).fetchall()
                symbols_in_db = sorted({(r[0] or "").upper() for r in in_db})
            except Exception:
                pass
        return {
            "ok": True,
            "path": SURVEILLANCE_DB_PATH,
            "tables": tables,
            "target_table": SURVEILLANCE_TABLE,
            "row_count": total,
            "column_mapping_used": resolved,
            "severity_breakdown": sev_breakdown,
            "coverage_in_db": symbols_in_db,
            "coverage_missing": sorted(set(c["tk"] for c in COVERAGE) - set(symbols_in_db or [])) if symbols_in_db else None,
        }
    finally:
        try: con.close()
        except: pass


@app.get("/probe/auth")
async def probe_auth():
    """Confirm the api-key header is accepted by SETSMART. Calls
    eod-price-by-symbol for PTT (1 day) and reports status."""
    if not API_KEY:
        return JSONResponse({"ok": False, "error": "SETSMART_API_KEY env var is not set."}, status_code=500)
    today = datetime.now(timezone.utc).astimezone().date()
    url = f"{LISTED_BASE}/eod-price-by-symbol"
    params = {"symbol": "PTT", "startDate": today.isoformat(), "adjustedPriceFlag": "Y"}
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as c:
            r = await c.get(url, headers=_auth_headers_sync(), params=params)
        ok = r.status_code == 200
        try:
            body = r.json()
            shape = f"array len={len(body)}" if isinstance(body, list) else type(body).__name__
        except Exception:
            body = r.text[:300]; shape = "non-json"
        return {"ok": ok, "status": r.status_code, "url": str(r.url),
                "key_length": len(API_KEY), "response_shape": shape}
    except Exception as e:
        return JSONResponse({"ok": False, "error": str(e)}, status_code=502)


@app.get("/probe")
async def probe(path: str):
    """Hit any SETSMART path through the configured auth. Use to test
    arbitrary endpoints from your Developer Portal.

    Examples:
      /probe?path=listed-company-api/eod-price-by-symbol?symbol=TU&startDate=2026-04-01&adjustedPriceFlag=Y
      /probe?path=listed-company-api/financial-data-and-ratio-by-symbol?symbol=TU&startYear=2024&startQuarter=1
    """
    if not path or path.startswith(("http://", "https://")):
        raise HTTPException(400, "path must be relative")
    target = f"{SETSMART_BASE}/{path.lstrip('/')}"
    try:
        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as c:
            r = await c.get(target, headers=await _auth_headers())
        try:    body = r.json()
        except: body = r.text[:2000]
        return {"target": target, "status": r.status_code, "body": body}
    except HTTPException:
        raise
    except Exception as e:
        return {"target": target, "status": 0, "error": str(e)}


@app.get("/morning-brief")
async def morning_brief(force: bool = False):
    now = time.time()
    if not force and _cache["payload"] and (now - _cache["ts"]) < COVERAGE_TTL_SEC:
        return JSONResponse(_cache["payload"])
    payload = await build_morning_brief()
    _cache["payload"] = payload
    _cache["ts"] = now
    return JSONResponse(payload)


# ------------------------------------------------------------------
# Disclosure Pulse routes
# ------------------------------------------------------------------
@app.get("/disclosure-pulse")
async def disclosure_pulse(days: int = 7, force: bool = False):
    days = max(1, min(int(days or 7), 90))
    now = time.time()
    if (not force and _disc_cache["payload"] is not None
            and _disc_cache["days"] == days
            and (now - _disc_cache["ts"]) < COVERAGE_TTL_SEC):
        return JSONResponse(_disc_cache["payload"])
    payload = await build_disclosure_pulse(days)
    _disc_cache.update({"payload": payload, "ts": now, "days": days})
    return JSONResponse(payload)


# ------------------------------------------------------------------
# Unusual Trading Alert routes
# ------------------------------------------------------------------
@app.get("/unusual-trading")
async def unusual_trading(force: bool = False):
    now = time.time()
    # Shorter TTL — intraday data changes through the day
    ttl = max(60, COVERAGE_TTL_SEC // 4)
    if not force and _alert_cache["payload"] and (now - _alert_cache["ts"]) < ttl:
        return JSONResponse(_alert_cache["payload"])
    payload = await build_unusual_trading()
    _alert_cache.update({"payload": payload, "ts": now})
    return JSONResponse(payload)


# ------------------------------------------------------------------
# Sector Heatmap routes
# ------------------------------------------------------------------
@app.get("/sector-heatmap")
async def sector_heatmap(force: bool = False):
    now = time.time()
    if not force and _heat_cache["payload"] and (now - _heat_cache["ts"]) < COVERAGE_TTL_SEC:
        return JSONResponse(_heat_cache["payload"])
    payload = await build_sector_heatmap()
    _heat_cache["payload"] = payload
    _heat_cache["ts"] = now
    return JSONResponse(payload)

