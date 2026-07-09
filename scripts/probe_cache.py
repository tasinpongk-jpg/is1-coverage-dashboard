"""Quick diagnostic: fire classify_one twice back-to-back; print usage dicts.

If prompt caching is wired correctly we expect:
  Call 1: cache_write > 0, cache_read = 0
  Call 2 (within 5 min): cache_read > 0, cache_write = 0

Provider-agnostic: works on any Anthropic-compatible endpoint that supports cache_control.
"""

import sys
sys.path.insert(0, "surveillance")

from classifier import _client, classify_one  # noqa: E402

client = _client()

for i in (1, 2):
    parsed, usage = classify_one(
        client,
        symbol="CPF",
        datetime_iso="2026-05-12T10:00:00+07:00",
        headline_en="Notification of Dividend Payment",
        headline_th=None,
        url="https://example.com",
    )
    print(f"Call {i}: input={usage['input']:>6}  output={usage['output']:>4}  "
          f"cache_write={usage['cache_write']:>6}  cache_read={usage['cache_read']:>6}")
    print(f"  -> severity={parsed.severity}, category={parsed.category}")
