"""Refresh official Thai SET company profiles for the Sector Intelligence perimeter.

The script patches only ``nameTh`` and ``businessTypeTh`` in ticker-summary.json.
Market, valuation, financial-history, and English profile fields are preserved.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import httpx

from build_ticker_summary import SET_HEADERS, _set_warmup, fetch_company_profile


ROOT = Path(__file__).resolve().parents[1]
THAI_RE = re.compile(r"[\u0e00-\u0e7f]")


def perimeter_tickers(path: Path) -> list[str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    tickers = {
        company["ticker"]
        for sector in payload["sectors"].values()
        for segment in sector["segments"]
        for company in segment["companies"]
    }
    return sorted(tickers)


def valid_thai(value: object, minimum: int = 20) -> bool:
    text = str(value or "").strip()
    return len(text) >= minimum and bool(THAI_RE.search(text))


async def fetch_profiles(tickers: list[str], max_concurrent: int) -> dict[str, dict]:
    semaphore = asyncio.Semaphore(max_concurrent)
    async with httpx.AsyncClient(headers=SET_HEADERS, follow_redirects=True) as client:
        await _set_warmup(client)

        async def one(ticker: str) -> tuple[str, dict]:
            return ticker, await fetch_company_profile(client, ticker, semaphore)

        return dict(await asyncio.gather(*(one(ticker) for ticker in tickers)))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sector-json", type=Path, default=ROOT / "data" / "sector-intelligence.json")
    parser.add_argument("--ticker-summary", type=Path, default=ROOT / "data" / "ticker-summary.json")
    parser.add_argument("--max-concurrent", type=int, default=3)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tickers = perimeter_tickers(args.sector_json)
    if len(tickers) != 118:
        raise ValueError(f"Expected the audited 118-company perimeter, found {len(tickers)}")

    profiles = asyncio.run(fetch_profiles(tickers, args.max_concurrent))
    failures = {
        ticker: {
            "nameTh": profile.get("nameTh"),
            "businessTypeThLength": len(str(profile.get("businessTypeTh") or "")),
        }
        for ticker, profile in profiles.items()
        if not valid_thai(profile.get("nameTh"), 4) or not valid_thai(profile.get("businessTypeTh"))
    }
    if failures:
        raise RuntimeError("Official Thai company-profile coverage failed: " + json.dumps(failures, ensure_ascii=False))

    summary = json.loads(args.ticker_summary.read_text(encoding="utf-8"))
    ticker_rows = {row["tk"]: row for row in summary["tickers"]}
    missing_rows = sorted(set(tickers) - set(ticker_rows))
    if missing_rows:
        raise ValueError("Ticker-summary rows missing: " + ", ".join(missing_rows))

    for ticker in tickers:
        row = ticker_rows[ticker]
        profile = profiles[ticker]
        row["nameTh"] = profile["nameTh"].strip()
        row["businessTypeTh"] = profile["businessTypeTh"].strip()

    summary["_business_profile_th_refreshed_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    summary["_business_profile_th_source"] = "SET public company profile API (?lang=th)"
    temporary = args.ticker_summary.with_suffix(args.ticker_summary.suffix + ".tmp")
    temporary.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(args.ticker_summary)

    print(json.dumps({
        "verdict": "PASS",
        "companies": len(tickers),
        "thaiNames": sum(valid_thai(profiles[ticker]["nameTh"], 4) for ticker in tickers),
        "thaiBusinessDescriptions": sum(valid_thai(profiles[ticker]["businessTypeTh"]) for ticker in tickers),
        "source": summary["_business_profile_th_source"],
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
