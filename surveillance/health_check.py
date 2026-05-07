"""Schema-drift smoke test for the SET news endpoint.

Runs at the start of every scheduled cycle. If the SET API shape drifts
(undocumented endpoint can change without notice), this exits non-zero so
the cycle aborts BEFORE polling 34 names with broken assumptions, and
sends a Telegram alert so the operator notices.
"""

from __future__ import annotations

import sys

from client import SetNewsClient

REQUIRED_KEYS = {"id", "datetime", "symbol", "headline", "url", "lang"}
PROBE_TICKER = "PRG"
LOOKBACK_DAYS = 30


def _alert(msg: str) -> None:
    try:
        from alerts import EmailClient
        with EmailClient() as em:
            em.send(f"[SETSURV] 🚨 ALERT: health check failed\n\n{msg}")
    except Exception as e:  # noqa: BLE001
        print(f"(could not send email alert: {e})")


def main() -> int:
    try:
        with SetNewsClient() as c:
            items = c.search_recent(PROBE_TICKER, lookback_days=LOOKBACK_DAYS)
    except Exception as e:  # noqa: BLE001
        msg = f"network/HTTP failure on SET news endpoint: {type(e).__name__}: {e}"
        print(f"ERROR: {msg}")
        _alert(msg)
        return 1

    if not items:
        msg = f"no items returned for {PROBE_TICKER} over {LOOKBACK_DAYS}d — endpoint may be down or symbol changed"
        print(f"WARN: {msg}")
        _alert(msg)
        return 1

    sample = items[0]
    missing = REQUIRED_KEYS - set(sample.keys())
    if missing:
        msg = f"schema drift — missing keys {missing}. Sample: {sample}"
        print(f"ERROR: {msg}")
        _alert(msg)
        return 1

    print(f"OK: schema check passed ({len(items)} items, {PROBE_TICKER})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
