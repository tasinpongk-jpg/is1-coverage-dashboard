"""Ad-hoc failure-injection tests for build_daily_brief.py.

Run: python tests/test_failure_injection.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import urllib.error
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import build_daily_brief as b

FIX = REPO / "tests" / "fixtures"
ai = json.loads((FIX / "ai_insights_2026-08-04.json").read_text(encoding="utf-8"))
brief = json.loads((FIX / "morning_brief_2026-08-04.json").read_text(encoding="utf-8"))
tickers = json.loads((FIX / "tickers_2026-08-04.json").read_text(encoding="utf-8"))
# disclosure_pulse.json fixture is gitignored (large); use a synthetic minimal
# pulse if missing so failure-injection tests can still run on CI.
_pulse_path = FIX / "disclosure_pulse_2026-08-04.json"
if _pulse_path.exists():
    pulse = json.loads(_pulse_path.read_text(encoding="utf-8"))
else:
    pulse = {"filings": []}

RESULTS = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, ok, detail))
    mark = "PASS" if ok else "FAIL"
    print(f"  [{mark}] {name}{(' — ' + detail) if detail else ''}")


# ---------------------------------------------------------------- tests

print("\n=== Failure: missing webhook URL ===")
env = {k: v for k, v in os.environ.items() if k != "DAILY_BRIEF_WEBHOOK"}
env["DAILY_BRIEF_DRY_RUN"] = "0"
env["DAILY_BRIEF_STATE_DIR"] = tempfile.mkdtemp()
# Run as subprocess so env really doesn't have the var
import subprocess
proc = subprocess.run(
    [sys.executable, str(REPO / "scripts" / "build_daily_brief.py")],
    env=env,
    capture_output=True, text=True, timeout=30,
)
check("missing webhook → exit 1 (fail closed)",
      proc.returncode == 1 and "FATAL" in (proc.stdout + proc.stderr))


print("\n=== Failure: stale asOf (yesterday) ===")
# Need DAILY_BRIEF_WEBHOOK set so we get past the fail-closed check.
os.environ["DAILY_BRIEF_WEBHOOK"] = "https://example.invalid/test"
os.environ["DAILY_BRIEF_DRY_RUN"] = "1"
# Patch the live AI fixture's asOf to yesterday
stale_ai = dict(ai)
stale_ai["asOf"] = "2026-08-03"
tmpdir = Path(tempfile.mkdtemp())
for name, d in (
    ("ai-insights.json", stale_ai),
    ("morning-brief.json", brief),
    ("tickers.json", tickers),
    ("disclosure-pulse.json", pulse),
):
    (tmpdir / name).write_text(json.dumps(d), encoding="utf-8")

# Patch _fetch_json to read from tmpdir
orig_fetch = b._fetch_json
def fake_fetch(url, timeout=30):
    name = url.rsplit("/", 1)[-1]
    p = tmpdir / name
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return None
b._fetch_json = fake_fetch
try:
    rc = b.main()
    log = ""  # main() doesn't return its log; capture via stdout
finally:
    b._fetch_json = orig_fetch
check("stale asOf → exit 0 (skipped, no post)",
      rc == 0,
      f"got rc={rc}")


print("\n=== Failure: source 404 ===")
def fetch_404(url, timeout=30):
    return None  # all sources 404
b._fetch_json = fetch_404
try:
    rc = b.main()
finally:
    b._fetch_json = orig_fetch
check("all sources 404 → exit 1",
      rc == 1,
      f"got rc={rc}")


print("\n=== Failure: webhook 429 → retry honors Retry-After ===")
sleeps = []
orig_sleep = b.time.sleep
b.time.sleep = lambda s: sleeps.append(s)

class Fake429(b.urllib.error.HTTPError):
    def __init__(self, ra="0.5"):
        super().__init__("http://x", 429, "Too Many", {}, b"")
        self.headers = {"Retry-After": ra}
        self._body = b""
    def read(self, n=200):
        return self._body[:n]

attempts = [0]
def fake_urlopen(req, timeout):
    attempts[0] += 1
    if attempts[0] <= 1:
        raise Fake429("0.5")
    class R:
        status = 200
        def read(self, n): return b"ok"
        def __enter__(self): return self
        def __exit__(self, *a): pass
    return R()

b.urllib.request.urlopen = fake_urlopen
ok, status = b._post_one("http://x", {"embeds": []}, dry_run=False, max_429_retries=2)
b.time.sleep = orig_sleep
check("429 → success on attempt 2", ok and attempts[0] == 2,
      f"ok={ok} attempts={attempts[0]}")
check("honors Retry-After=0.5", any(s >= 0.4 for s in sleeps))


print("\n=== Failure: 4xx → no retry ===")
attempts[0] = 0
class Fake400(Fake429):
    def __init__(self):
        super().__init__("")
        self.code = 400
def fake_400(req, timeout):
    attempts[0] += 1
    raise Fake400()
b.urllib.request.urlopen = fake_400
ok, status = b._post_one("http://x", {"embeds": []}, dry_run=False)
check("4xx fails immediately (no retry)",
      not ok and attempts[0] == 1,
      f"ok={ok} attempts={attempts[0]}")


# ---------------------------------------------------------------- summary
total = len(RESULTS)
passed = sum(1 for _, ok, _ in RESULTS if ok)
print(f"\n=== SUMMARY: {passed}/{total} passed ===\n")
if passed != total:
    for name, ok, detail in RESULTS:
        if not ok:
            print(f"  - {name}: {detail}")
    sys.exit(1)
print("All failure-injection checks green.")