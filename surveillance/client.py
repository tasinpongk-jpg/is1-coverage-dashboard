"""SET news API client.

Wraps the undocumented but stable endpoint:
    https://www.set.or.th/api/set/news/search

Required headers: realistic browser UA + Referer + Origin (Cloudflare otherwise 403s).
Required params: symbol, lang. Optional: fromDate, toDate (DD/MM/YYYY format).
"""

from __future__ import annotations

import time
from datetime import date, datetime, timedelta
from typing import Any, Literal

import httpx

BASE_URL = "https://www.set.or.th/api/set/news/search"
WARMUP_URL = "https://www.set.or.th/en/market/news-and-alert/news"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
HEADERS = {
    "User-Agent": UA,
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9,th;q=0.8",
    "Referer": "https://www.set.or.th/en/market/news-and-alert/news",
    "Origin": "https://www.set.or.th",
    "sec-ch-ua": '"Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
}

MIN_INTERVAL_SEC = 0.6  # ~1.6 req/s — well below the ~10 req/s Cloudflare threshold


def _fmt(d: date) -> str:
    return d.strftime("%d/%m/%Y")


class SetNewsClient:
    """Polite client that warms up the SPA cookie jar then streams JSON requests."""

    def __init__(self, timeout: float = 20.0) -> None:
        self._client = httpx.Client(headers=HEADERS, timeout=timeout, follow_redirects=True)
        self._last_request_at: float = 0.0
        self._warmed = False

    def __enter__(self) -> "SetNewsClient":
        return self

    def __exit__(self, *_: object) -> None:
        self._client.close()

    def _throttle(self) -> None:
        delta = time.monotonic() - self._last_request_at
        if delta < MIN_INTERVAL_SEC:
            time.sleep(MIN_INTERVAL_SEC - delta)
        self._last_request_at = time.monotonic()

    def warmup(self) -> None:
        """Hit the SPA root once so Imperva/Incapsula sets cookies."""
        if self._warmed:
            return
        self._client.get(WARMUP_URL).raise_for_status()
        self._warmed = True

    def search(
        self,
        symbol: str,
        lang: Literal["en", "th"] = "en",
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """Return raw newsInfoList for a symbol, optionally bounded by date."""
        self.warmup()
        self._throttle()
        params: dict[str, Any] = {"symbol": symbol, "lang": lang}
        if from_date:
            params["fromDate"] = _fmt(from_date)
        if to_date:
            params["toDate"] = _fmt(to_date)
        r = self._client.get(BASE_URL, params=params)
        r.raise_for_status()
        body = r.json()
        return body.get("newsInfoList", [])

    def search_recent(self, symbol: str, lookback_days: int = 7) -> list[dict[str, Any]]:
        """Convenience: fetch both EN + TH disclosures for the trailing N days."""
        today = datetime.now().date()
        from_d = today - timedelta(days=lookback_days)
        en = self.search(symbol, "en", from_d, today)
        th = self.search(symbol, "th", from_d, today)
        return en + th
