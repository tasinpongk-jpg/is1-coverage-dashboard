"""Schema-drift smoke test for the SET news endpoint.

Runs at the start of every scheduled cycle. If the SET API shape drifts
(undocumented endpoint can change without notice), this exits non-zero so
the cycle aborts BEFORE polling 34 names with broken assumptions, and
sends a Telegram alert so the operator notices.

Also validates data/tickers.json internal consistency: the hand-maintained
`totals` block must match a recount of the ticker array (guards the
AQUA-class bug where a ticker is added but totals go stale — dashboards
and chat agents quote the totals).
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from client import SetNewsClient

TICKERS_JSON = Path(__file__).resolve().parent.parent / "data" / "tickers.json"

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


def check_tickers_totals() -> str | None:
    """Returns an error message if tickers.json totals don't match the array."""
    d = json.loads(TICKERS_JSON.read_text(encoding="utf-8"))
    ts = d["tickers"]
    stored = d["totals"]
    by_rm = Counter(t["rm"] for t in ts)
    by_sector = Counter(t["sector"] for t in ts)
    problems = []
    if stored["all"] != len(ts):
        problems.append(f"totals.all={stored['all']} but array has {len(ts)}")
    if dict(stored["by_rm"]) != dict(by_rm):
        problems.append(f"by_rm stored {dict(stored['by_rm'])} != actual {dict(by_rm)}")
    if dict(stored["by_sector"]) != dict(by_sector):
        problems.append(f"by_sector stored {dict(stored['by_sector'])} != actual {dict(by_sector)}")
    dupes = [tk for tk, n in Counter(t["tk"] for t in ts).items() if n > 1]
    if dupes:
        problems.append(f"duplicate tickers: {dupes}")
    if problems:
        return ("tickers.json totals out of sync — recompute after editing "
                "coverage: " + "; ".join(problems))
    return None


def main() -> int:
    err = check_tickers_totals()
    if err:
        print(f"ERROR: {err}")
        _alert(err)
        return 1
    print(f"OK: tickers.json totals consistent")

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
