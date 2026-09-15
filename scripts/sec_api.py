#!/usr/bin/env python3
"""Thin client for the SEC Thailand Open Data API (api.sec.or.th).

Portal : https://secopendata.sec.or.th/sec-open-apis
Auth   : header  Ocp-Apim-Subscription-Key: <key>
Limit  : 3,000 calls / 300 s (shared across all product groups)
Paging : v2 endpoints -> page_size (1-100) + next_cursor
         v1 endpoints -> no paging, one call returns the whole array

The subscription key is read from the environment. It is NEVER written to the
repo. Set it before running anything that imports this module:

    export SEC_API_KEY=<primary key>
    export SEC_API_KEY_SECONDARY=<secondary key>   # optional failover

stdlib only, to match scripts/build_sec_bonds.py.

CLI probe (use this first to confirm the key and the v1/v2 split):

    python3 scripts/sec_api.py ping
    python3 scripts/sec_api.py get /v1/one-report/sbo/2024/info/T
    python3 scripts/sec_api.py get /v2/fund/general-info/amcs --page-size 5
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = os.environ.get("SEC_API_BASE", "https://api.sec.or.th")
KEY_ENV = "SEC_API_KEY"
KEY_ENV_SECONDARY = "SEC_API_KEY_SECONDARY"

# 3,000 calls / 300 s == 10 calls/s. Stay under it with a floor between calls.
MIN_INTERVAL = float(os.environ.get("SEC_API_MIN_INTERVAL", "0.12"))
TIMEOUT = float(os.environ.get("SEC_API_TIMEOUT", "60"))
MAX_RETRY = 4

_last_call = [0.0]


class SecApiError(RuntimeError):
    def __init__(self, status, path, body):
        self.status = status
        self.path = path
        self.body = body
        super().__init__(f"{status} on {path}: {body[:300]}")


def _keys():
    keys = [os.environ.get(KEY_ENV), os.environ.get(KEY_ENV_SECONDARY)]
    keys = [k.strip() for k in keys if k and k.strip()]
    if not keys:
        raise SystemExit(
            f"No subscription key. Set {KEY_ENV} (and optionally "
            f"{KEY_ENV_SECONDARY}) in the environment — do not hardcode it."
        )
    return keys


def _throttle():
    gap = time.monotonic() - _last_call[0]
    if gap < MIN_INTERVAL:
        time.sleep(MIN_INTERVAL - gap)
    _last_call[0] = time.monotonic()


def request(path, params=None, method="GET", body=None, key=None):
    """One call. Returns the decoded JSON body.

    Retries on 429 and 5xx with exponential backoff; rotates to the secondary
    key on 401/403 if one is configured.
    """
    keys = [key] if key else _keys()
    url = BASE.rstrip("/") + path
    if params:
        clean = {k: v for k, v in params.items() if v is not None and v != ""}
        if clean:
            url += "?" + urllib.parse.urlencode(clean)

    payload = json.dumps(body).encode() if body is not None else None
    last_exc = None

    for key_i, k in enumerate(keys):
        for attempt in range(MAX_RETRY):
            _throttle()
            req = urllib.request.Request(url, data=payload, method=method)
            req.add_header("Ocp-Apim-Subscription-Key", k)
            req.add_header("Accept", "application/json")
            if payload is not None:
                req.add_header("Content-Type", "application/json")
            try:
                with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                    raw = resp.read().decode("utf-8", "replace")
                return json.loads(raw) if raw.strip() else None
            except urllib.error.HTTPError as e:
                detail = e.read().decode("utf-8", "replace")
                if e.code in (401, 403) and key_i + 1 < len(keys):
                    last_exc = SecApiError(e.code, path, detail)
                    break  # try the next key
                if e.code == 429 or e.code >= 500:
                    last_exc = SecApiError(e.code, path, detail)
                    time.sleep(2 ** attempt)
                    continue
                raise SecApiError(e.code, path, detail) from None
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
                last_exc = e
                time.sleep(2 ** attempt)
    raise last_exc if last_exc else SecApiError(0, path, "exhausted retries")


def get_v1(path):
    """v1 (one-report / pvd / license-check): single call, array or {items:[...]}.

    The portal's v1 examples show a bare JSON array. Some deployments wrap it
    in {"items": [...]}. Handle both rather than guessing.
    """
    data = request(path)
    if data is None:
        return []
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        return data.get("items", []) or []
    return []


def paginate_v2(path, params=None, page_size=100, max_pages=None):
    """v2 (fund / bond): yield every item across next_cursor pages."""
    params = dict(params or {})
    params["page_size"] = page_size
    cursor = None
    pages = 0
    seen = set()
    while True:
        if cursor:
            params["next_cursor"] = cursor
        data = request(path, params) or {}
        items = data.get("items") or []
        for it in items:
            yield it
        pages += 1
        cursor = data.get("next_cursor")
        if not cursor or not items:
            return
        if cursor in seen:  # guard against a server that echoes the cursor
            return
        seen.add(cursor)
        if max_pages and pages >= max_pages:
            return


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("ping", help="cheapest v1 + v2 call, to validate the key")

    g = sub.add_parser("get", help="raw GET against a path")
    g.add_argument("path")
    g.add_argument("--param", action="append", default=[],
                   metavar="K=V", help="query param, repeatable")
    g.add_argument("--page-size", type=int, default=None)
    g.add_argument("--all", action="store_true",
                   help="follow next_cursor and print every item (v2 only)")
    g.add_argument("--max-pages", type=int, default=None)

    a = ap.parse_args()

    if a.cmd == "ping":
        for label, path in (("v2 fund", "/v2/fund/general-info/amcs"),
                            ("v1 one-report", "/v1/one-report/sbo/2024/info/T")):
            try:
                if path.startswith("/v2"):
                    d = request(path, {"page_size": 1})
                    n = len((d or {}).get("items") or [])
                else:
                    n = len(get_v1(path))
                print(f"OK   {label:14s} {path}  -> {n} item(s)")
            except Exception as e:  # noqa: BLE001 - probe reports, never raises
                print(f"FAIL {label:14s} {path}  -> {e}")
        return

    params = {}
    for kv in a.param:
        k, _, v = kv.partition("=")
        params[k] = v
    if a.page_size:
        params["page_size"] = a.page_size

    if a.all:
        out = list(paginate_v2(a.path, params,
                               page_size=a.page_size or 100,
                               max_pages=a.max_pages))
    elif a.path.startswith("/v1"):
        out = get_v1(a.path)
    else:
        out = request(a.path, params)
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
