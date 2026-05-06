"""
Daily build script: produces 4 JSON snapshots for the team coverage dashboards.

Reads tickers.json (the team portfolio) and calls the existing setsmart_proxy
route handlers in-process with COVERAGE expanded to all 231 tickers.

Run by Windows scheduled task at 7am every weekday. Output JSONs are written
under ../data/ and committed to the Cloudflare Pages Git repo.

Usage:
  python build_daily.py
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
PROXY_DIR = Path(r"C:\SET API Manual\SETSMART_Proxy")

sys.path.insert(0, str(PROXY_DIR))


def load_tickers() -> dict:
    with open(DATA_DIR / "tickers.json", encoding="utf-8") as f:
        return json.load(f)


def build_coverage(tickers_json: dict) -> list[dict]:
    """Build the proxy's COVERAGE list shape from tickers.json.

    Proxy expects: [{"tk": "...", "sector": "FOOD"|"PROP"|"PFREIT", "segment": str}]
    We map AGRI→FOOD bucket, CONS+CONMAT→PROP bucket, PF&REIT→PFREIT.
    """
    bucket_map = {"FOOD": "FOOD", "AGRI": "FOOD",
                  "PROP": "PROP", "CONS": "PROP", "CONMAT": "PROP",
                  "PF&REIT": "PFREIT"}
    out = []
    for t in tickers_json["tickers"]:
        out.append({
            "tk": t["tk"],
            "sector": bucket_map.get(t["sector"], t["sector"]),
            "segment": t["sector"],
        })
    return out


async def run_routes(out_dir: Path) -> dict:
    """Call each of the 4 route handlers and write JSON outputs."""
    import setsmart_proxy as proxy

    # Override COVERAGE with all 231 tickers — affects all routes that close over it.
    tickers_json = load_tickers()
    proxy.COVERAGE = build_coverage(tickers_json)

    # Bust any in-process cache
    proxy._cache.clear() if hasattr(proxy, "_cache") and isinstance(proxy._cache, dict) else None
    if hasattr(proxy, "_disc_cache") and isinstance(proxy._disc_cache, dict):
        proxy._disc_cache.clear()

    # Sequential per-route. Inside each route, the proxy already controls
    # concurrency via SETSMART_MAX_CONCURRENT. ~3-4 min total wall-clock.
    results = {}
    routes = [
        ("morning-brief.json", proxy.morning_brief, {"force": True}),
        ("sector-heatmap.json", proxy.sector_heatmap, {"force": True}),
        ("unusual-trading.json", proxy.unusual_trading, {"force": True}),
        ("disclosure-pulse.json", proxy.disclosure_pulse, {"days": 14, "force": True}),
    ]

    from fastapi.responses import JSONResponse
    for fname, fn, kwargs in routes:
        t0 = time.time()
        print(f"  -> {fname} ...", flush=True)
        try:
            resp = await fn(**kwargs)
            # Routes return JSONResponse — unwrap to dict
            if isinstance(resp, JSONResponse):
                payload = json.loads(resp.body.decode("utf-8"))
            else:
                payload = resp
            payload["_built_at"] = datetime.now(timezone.utc).isoformat()
            payload["_coverage_size"] = len(proxy.COVERAGE)
            (out_dir / fname).write_text(
                json.dumps(payload, ensure_ascii=False, indent=2, default=str),
                encoding="utf-8",
            )
            results[fname] = {"ok": True, "elapsed_s": round(time.time() - t0, 1)}
            print(f"    ok in {results[fname]['elapsed_s']}s", flush=True)
        except Exception as e:
            results[fname] = {"ok": False, "error": str(e), "elapsed_s": round(time.time() - t0, 1)}
            print(f"    FAILED: {e}", flush=True)

    return results


def main():
    if not (DATA_DIR / "tickers.json").exists():
        sys.exit(f"Missing {DATA_DIR / 'tickers.json'}")
    if not os.environ.get("SETSMART_API_KEY"):
        sys.exit("SETSMART_API_KEY not set in environment")

    print(f"=== Daily build at {datetime.now().isoformat(timespec='seconds')} ===")
    t0 = time.time()
    results = asyncio.run(run_routes(DATA_DIR))

    summary = {
        "built_at": datetime.now(timezone.utc).isoformat(),
        "elapsed_s": round(time.time() - t0, 1),
        "routes": results,
    }
    (DATA_DIR / "build-status.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(f"=== Done in {summary['elapsed_s']}s ===")
    print(json.dumps(results, indent=2))

    # Exit non-zero if any route failed (so scheduled task surfaces failure)
    if any(not r["ok"] for r in results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
