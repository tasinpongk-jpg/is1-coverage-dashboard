"""Daily fetch of non-SETLink data sources.

Four scrapers, one entry point. All run once per day, alongside the SETLink
poller, in the same surveillance job. Each scraper is best-effort: a network
failure on one source must not break the others.

Sources:
  - external_news: RSS feeds from RYT9, Kaohoon, Hoonsmart, Prachachat,
    Bangkok Biznews. Ticker-matched against the 231-name coverage.
  - trading_signs: SET trading-sign HTML page (SP/NP/NC/CC/C/ST/DS/CB).
  - sec_enforcement: SEC iDisc Enforce/Recent table.
  - macro_overlays: ThaiBMA Daily Highlight, REIC news, OAE EN news, BLS
    research browse. Stored without per-ticker matching.

Run:
  python surveillance/external_sources.py            # all four
  python surveillance/external_sources.py --only rss # one source family
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import ssl
import sys
import traceback
from datetime import datetime, timezone, timedelta
from typing import Any, Iterable
from xml.etree import ElementTree as ET

import httpx

from coverage import ALL_TICKERS, SECTOR_OF
from store import conn

# Shared HTTP client config — most Thai news sites are picky about UA.
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)
HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "th,en-US;q=0.7,en;q=0.3",
}
TIMEOUT = httpx.Timeout(20.0, connect=10.0)


def _legacy_ssl_context() -> ssl.SSLContext:
    """Some Thai broker / govt sites still run on legacy TLS that modern OpenSSL
    rejects with SSLV3_ALERT_HANDSHAKE_FAILURE. Drop to SECLEVEL=0 and accept
    TLSv1+ for those endpoints only."""
    ctx = ssl.create_default_context()
    try:
        ctx.set_ciphers("DEFAULT@SECLEVEL=0")
    except ssl.SSLError:
        pass
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

BKK = timezone(timedelta(hours=7))


# ---------------------------------------------------------------------------
# Ticker matcher
# ---------------------------------------------------------------------------

TICKER_SET: set[str] = set(ALL_TICKERS)

# Sort by length descending so longer tickers (AMATAV) match before shorter
# substrings (AMATA). Escape for special chars (F&D, Q-CON).
_BRACKET_RE = re.compile(r"[\[(]([A-Z][A-Z0-9&\-]{0,9})[\])]")
_STANDALONE_RE = re.compile(r"(?<![A-Z0-9])([A-Z][A-Z0-9&\-]{2,9})(?![A-Z0-9])")
_THAI_CTX_RE = re.compile(
    r"(?:หุ้น|บมจ\.?|บริษัท)\s*([A-Z][A-Z0-9&\-]{0,9})"
)


def find_tickers(text: str) -> set[str]:
    """Return coverage tickers mentioned in `text`.

    Three-pass strategy:
      1. Bracketed/parens — high confidence, any length (catches [A], [M], [J])
      2. Standalone — requires length >= 3 to avoid false positives
      3. Thai-context — "หุ้น X" or "บมจ. X" — any length
    """
    if not text:
        return set()
    found: set[str] = set()
    for m in _BRACKET_RE.finditer(text):
        tok = m.group(1).upper()
        if tok in TICKER_SET:
            found.add(tok)
    for m in _STANDALONE_RE.finditer(text):
        tok = m.group(1).upper()
        if tok in TICKER_SET:
            found.add(tok)
    for m in _THAI_CTX_RE.finditer(text):
        tok = m.group(1).upper()
        if tok in TICKER_SET:
            found.add(tok)
    return found


def _hash(*parts: str) -> str:
    return hashlib.sha1("\x1f".join(parts).encode("utf-8")).hexdigest()[:16]


def _strip_html(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def _parse_rfc822(s: str) -> str:
    """Convert an RFC822 / W3C-DTF date to ISO 8601 in +07:00. Tolerant of
    odd formats — falls back to current BKK time on parse failure so the row
    still persists rather than getting dropped."""
    if not s:
        return datetime.now(BKK).isoformat(timespec="seconds")
    for fmt in (
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(s.strip(), fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=BKK)
            return dt.astimezone(BKK).isoformat(timespec="seconds")
        except ValueError:
            continue
    return datetime.now(BKK).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# external_news — RSS feeds
# ---------------------------------------------------------------------------

RSS_FEEDS: list[dict[str, str]] = [
    {"source": "RYT9", "url": "https://www.ryt9.com/stock/rss.xml", "lang": "th"},
    {"source": "KAOHOON", "url": "https://www.kaohoon.com/feed", "lang": "th"},
    {"source": "HOONSMART", "url": "https://hoonsmart.com/feed", "lang": "th"},
    {"source": "PRACHACHAT", "url": "https://www.prachachat.net/feed", "lang": "th"},
    # BangkokBiznews retired RSS in their 2025 Next.js redesign — the /rss URL
    # now serves a React HTML page. Dropped pending a working alternative.
]


def _parse_rss(xml_text: str) -> list[dict[str, str]]:
    """Parse an RSS 2.0 feed. Tolerant of namespaced feeds, broken CDATA."""
    items: list[dict[str, str]] = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        # Try wrapping in a synthetic root in case there's leading junk
        cleaned = re.search(r"<rss\b[\s\S]*</rss>", xml_text)
        if not cleaned:
            return items
        try:
            root = ET.fromstring(cleaned.group(0))
        except ET.ParseError:
            return items
    for it in root.iter():
        if not it.tag.endswith("item"):
            continue
        d: dict[str, str] = {}
        for child in it:
            tag = child.tag.split("}", 1)[-1]
            if child.text:
                d[tag] = child.text.strip()
        if d.get("title") or d.get("link"):
            items.append(d)
    return items


def fetch_external_news(client: httpx.Client) -> tuple[int, int]:
    """Fetch all RSS feeds, match tickers, upsert. Returns (rows_inserted, sources_ok)."""
    inserted = 0
    sources_ok = 0
    for feed in RSS_FEEDS:
        try:
            r = client.get(feed["url"])
            r.raise_for_status()
            items = _parse_rss(r.text)
        except Exception as e:  # noqa: BLE001
            print(f"  [rss/{feed['source']}] FAIL {type(e).__name__}: {e}", flush=True)
            continue
        sources_ok += 1
        matched_rows: list[tuple[Any, ...]] = []
        for it in items:
            title = _strip_html(it.get("title", ""))
            desc = _strip_html(it.get("description", "") or it.get("content:encoded", ""))
            link = it.get("link", "")
            pub = _parse_rfc822(it.get("pubDate", "") or it.get("dc:date", ""))
            text_pool = f"{title}\n{desc}"
            tickers = find_tickers(text_pool)
            if not tickers:
                continue
            base_id = _hash(feed["source"], link or title)
            for tk in tickers:
                matched_rows.append((
                    base_id,
                    feed["source"],
                    tk,
                    SECTOR_OF.get(tk),
                    pub,
                    title[:500],
                    link,
                    desc[:500],
                    feed["lang"],
                ))
        if not matched_rows:
            print(f"  [rss/{feed['source']}] {len(items)} items, 0 ticker matches", flush=True)
            continue
        with conn() as c:
            existing = {
                (row[0], row[1])
                for row in c.execute(
                    "SELECT id, symbol FROM external_news "
                    "WHERE id = ANY (?)",
                    [[r[0] for r in matched_rows]],
                ).fetchall()
            }
            new = [r for r in matched_rows if (r[0], r[2]) not in existing]
            if new:
                c.executemany(
                    """
                    INSERT INTO external_news
                      (id, source, symbol, sector, datetime_iso, headline, url, body_excerpt, lang)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    new,
                )
            inserted += len(new)
        print(f"  [rss/{feed['source']}] {len(items)} items, {len(matched_rows)} matched, {len(new) if matched_rows else 0} new", flush=True)
    return inserted, sources_ok


# ---------------------------------------------------------------------------
# trading_signs — derived from SET market-alert news feed
# ---------------------------------------------------------------------------
#
# SET doesn't expose a direct "current sign list" JSON API. The trading-sign
# web page is a Nuxt SPA whose data comes from /api/set/news/market-alert.
# We scan recent market-alert news for sign-related headlines (SP/NP/CC/etc.)
# and rebuild a per-ticker current-state view from that. Cookie warmup via
# the public page is required to avoid HTTP 452.

SET_WARMUP_URL = "https://www.set.or.th/en/market/news-and-alert/trading-alert/trading-sign"
SET_MARKET_ALERT_URL = "https://www.set.or.th/api/set/news/market-alert"

# Sign-token detection — match common headline patterns from SET English news.
# Order matters: longer tokens first so 'NC' doesn't shadow 'NC sign posted'.
_SIGN_RE = re.compile(
    r"\b(SP|CC|NP|NC|C|ST|DS|CB)\b\s*(?:sign|sign\s+posted|symbol|notice)?",
    re.I,
)
_SIGN_KEYWORDS = ("sign", "suspension", "suspended", "caution", "notice pending",
                  "non-compliance", "designated", "stabilization", "circuit breaker")


def _set_warmup(client: httpx.Client) -> None:
    """Hit the public page once so Cloudflare hands back a cookie jar that
    the JSON API will accept. Without this, /api/set/* returns HTTP 452."""
    try:
        client.get(SET_WARMUP_URL, headers={"Accept-Language": "th,en-US;q=0.7"})
    except Exception:  # noqa: BLE001
        pass


def fetch_trading_signs(client: httpx.Client) -> int:  # noqa: ARG001 (client unused — derived from local DB)
    """Derive current trading-sign state from sign-change disclosures already
    in news_items (e.g. "CC sign posted on XBIO's securities").

    Two reasons we go to the local DB instead of scraping SET directly:
      1. /api/set/news/market-alert is a 5-item "today's widgets" endpoint —
         doesn't accept historical date filters.
      2. The trading-sign HTML page is a Nuxt SPA whose data binding we don't
         have a clean entry point for.

    Sign events flow naturally through the SETLink firehose anyway. We scan
    the last 180 days of news_items headlines for sign-token patterns and
    rebuild the active-state table from posted/lifted pairs.
    """
    sign_codes = {"SP", "CC", "NP", "NC", "C", "ST", "DS", "CB"}
    # Token must be uppercase and either followed by 'sign' word or itself the
    # last token before 'sign'. Tolerant of "CC sign posted on XBIO" and
    # "Trading suspension (SP) of <sym>".
    detect_re = re.compile(r"\b(SP|CC|NP|NC|ST|DS|CB|C)\b\s*(?:sign|symbol|measure|caution)?", re.I)
    removal_re = re.compile(r"\b(lift|lifted|remove|removed|release[ds]?)\b", re.I)
    coverage = TICKER_SET

    cutoff = (datetime.now(BKK) - timedelta(days=180)).isoformat()
    with conn() as c:
        rows = c.execute(
            """
            SELECT symbol, headline, datetime_iso
            FROM news_items
            WHERE datetime_iso >= ?
              AND headline IS NOT NULL
              AND (
                lower(headline) LIKE '%sign%'
                OR lower(headline) LIKE '%suspension%'
                OR lower(headline) LIKE '%caution%'
                OR lower(headline) LIKE '%notice pending%'
                OR lower(headline) LIKE '%non-compliance%'
                OR lower(headline) LIKE '%designated%'
                OR lower(headline) LIKE '%circuit breaker%'
              )
            ORDER BY datetime_iso ASC
            """,
            [cutoff],
        ).fetchall()

    # symbol -> { sign -> (date, headline) }; later events override earlier.
    state: dict[str, dict[str, tuple[str | None, str | None]]] = {}
    for sym_raw, headline, dt in rows:
        sym = (sym_raw or "").upper()
        if sym not in coverage or not headline:
            continue
        is_removal = bool(removal_re.search(headline))
        # Try to attribute the sign token. If multiple appear, posted/removed
        # both apply.
        for m in detect_re.finditer(headline):
            sg = m.group(1).upper()
            if sg not in sign_codes:
                continue
            if is_removal:
                state.setdefault(sym, {}).pop(sg, None)
            else:
                state.setdefault(sym, {})[sg] = (
                    (dt or "")[:10],
                    headline[:200],
                )

    out_rows = [
        (sym, sg, d, reason)
        for sym, signs in state.items()
        for sg, (d, reason) in signs.items()
    ]
    with conn() as c:
        c.execute("DELETE FROM trading_signs")
        if out_rows:
            c.executemany(
                "INSERT INTO trading_signs (symbol, sign, effective_date, reason) VALUES (?, ?, ?, ?)",
                out_rows,
            )
    print(f"  [trading_signs] {len(out_rows)} active signs on coverage (scanned {len(rows)} sign-related news rows)", flush=True)
    return len(out_rows)


# ---------------------------------------------------------------------------
# sec_enforcement — SEC iDisc Enforce/Recent
# ---------------------------------------------------------------------------
#
# The public page is an ASP.NET WebForms shell; the table is rendered by
# RecentEnforce.js doing a POST to /public/idisc/api/Enforce/GetEnforces with
# a payload containing rtk + Lang from the page. We replicate that POST.

SEC_ENFORCE_PAGE = "https://market.sec.or.th/public/idisc/en/Enforce/Recent"
SEC_ENFORCE_API = "https://market.sec.or.th/public/idisc/api/Enforce/GetEnforces"


def fetch_sec_enforcement(client: httpx.Client) -> int:
    try:
        page = client.get(SEC_ENFORCE_PAGE).text
        rtk_m = re.search(r'data-rtk="([^"]*)"', page)
        lang_m = re.search(r'data-lang="([^"]*)"', page)
        if not (rtk_m and rtk_m.group(1)):
            print("  [sec_enforcement] rtk not found on page — bailing", flush=True)
            return 0
        body = {
            "rtk": rtk_m.group(1),
            "Lang": (lang_m.group(1) if lang_m else "en"),
            "QueryType": "RECENT",
            "OffenderFlag": "", "OffenderTxt": "",
            "VioTypeTxt": "ALL",
            "DateFlag": "", "StartDateTxt": "", "EndDateTxt": "",
            "FreeSearchFlag": "", "FreeSearchTxt": "",
        }
        r = client.post(
            SEC_ENFORCE_API,
            headers={
                **HEADERS,
                "Content-Type": "application/json; charset=utf-8",
                "Accept": "application/json,text/plain,*/*",
                "Referer": SEC_ENFORCE_PAGE,
                "Origin": "https://market.sec.or.th",
            },
            json=body,
        )
        r.raise_for_status()
        # API returns a JSON string whose value is the rendered HTML table fragment.
        html = r.json() if r.headers.get("content-type", "").startswith("application/json") else r.text
        if not isinstance(html, str):
            html = json.dumps(html)
    except Exception as e:  # noqa: BLE001
        print(f"  [sec_enforcement] FAIL {type(e).__name__}: {e}", flush=True)
        return 0

    # Extract the data table from the response HTML
    table_match = re.search(r"<table[^>]*>([\s\S]*?)</table>", html, re.I)
    if not table_match:
        print("  [sec_enforcement] no <table> in API response", flush=True)
        return 0
    rows = re.findall(r"<tr[^>]*>([\s\S]*?)</tr>", table_match.group(1), re.I)
    out_rows: list[tuple[Any, ...]] = []
    coverage = TICKER_SET
    for raw in rows:
        cells = re.findall(r"<t[dh][^>]*>([\s\S]*?)</t[dh]>", raw, re.I)
        if len(cells) < 4:
            continue
        clean = [_strip_html(c) for c in cells]
        # SET English column layout observed:
        # [#] [Enforcement Date] [Name] [Relevant Section/Law] [Result] [Penalty?] ...
        # We're tolerant of variations.
        if all(not x for x in clean[1:]):
            continue
        date_val = clean[1] if len(clean) > 1 else ""
        respondent = clean[2] if len(clean) > 2 else ""
        law = clean[3] if len(clean) > 3 else ""
        action_type = clean[4] if len(clean) > 4 else law
        if not respondent or len(respondent) < 3:
            continue
        # Try to find a coverage ticker mentioned in the respondent name.
        matched = None
        resp_up = respondent.upper()
        for tk in coverage:
            # Word-boundary match to avoid e.g. "MK" inside "MARKETING"
            if re.search(rf"(?<![A-Z0-9]){re.escape(tk)}(?![A-Z0-9])", resp_up):
                matched = tk
                break
        rid = _hash("SEC", date_val, respondent[:120], law[:120])
        out_rows.append((
            rid, "", date_val, respondent[:300], action_type[:200], matched,
            " | ".join(clean)[:600], SEC_ENFORCE_PAGE,
        ))
    if not out_rows:
        print("  [sec_enforcement] table parsed but no rows extracted", flush=True)
        return 0
    # Collapse intra-batch dupes (same case shown twice on the page in EN+TH).
    dedup: dict[str, tuple[Any, ...]] = {}
    for row in out_rows:
        dedup.setdefault(row[0], row)
    deduped = list(dedup.values())
    with conn() as c:
        ids = [r[0] for r in deduped]
        existing = {row[0] for row in c.execute(
            "SELECT id FROM sec_enforcement WHERE id = ANY (?)", [ids]
        ).fetchall()}
        new = [r for r in deduped if r[0] not in existing]
        if new:
            c.executemany(
                """
                INSERT INTO sec_enforcement
                  (id, case_no, action_date, respondent, action_type, matched_ticker, description, url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                new,
            )
    print(f"  [sec_enforcement] {len(deduped)} unique rows, {len(new)} new (matched-to-coverage: {sum(1 for r in deduped if r[5])})", flush=True)
    return len(new)


# ---------------------------------------------------------------------------
# macro_overlays — ThaiBMA / REIC / OAE / BLS
# ---------------------------------------------------------------------------

MACRO_SOURCES = [
    {
        "source": "THAIBMA",
        "category": "bond",
        "url": "https://www.thaibma.or.th/EN/Market/Highlight1.aspx",
        "link_re": r'<a[^>]+href="(/EN/[^"]+)"[^>]*>\s*([^<]{8,200})\s*</a>',
        "base": "https://www.thaibma.or.th",
        "legacy_ssl": False,
    },
    {
        "source": "REIC",
        "category": "property",
        "url": "https://www.reic.or.th/News/RealEstate",
        "link_re": r'<a[^>]+href="(/News/[^"]+)"[^>]*>\s*([^<]{8,200})\s*</a>',
        "base": "https://www.reic.or.th",
        "legacy_ssl": False,
    },
    {
        "source": "BLS",
        "category": "broker_report",
        "url": "https://www2.bualuang.co.th/en/browse_research.php",
        # The visible report title sits in a <strong> tag, the link itself only
        # contains the literal text "more detail". Regex captures (title, href)
        # and the macro loop swaps for BLS so the surface contract stays
        # (href, label) like every other source.
        "link_re": r'<strong>([^<]{4,200})</strong>[\s\S]{0,400}?<a[^>]+href="(?:\.\./)?(att_browse\.php\?rep_id=\d+&att_id=\d+)"',
        "base": "https://www2.bualuang.co.th/",
        "legacy_ssl": True,
        "swap_groups": True,
    },
    # OAE (oae.go.th) is an Angular SPA — links are JS-rendered, so a static
    # HTML fetch returns no <a> tags. Dropped until a JSON endpoint surfaces or
    # we move scraping into a headless browser.
]


def fetch_macro_overlays(client: httpx.Client) -> int:
    """Fetch each macro page, extract first ~30 outgoing news/article/report
    links. We don't classify or ticker-match these — the dashboard surfaces
    them as a per-source list."""
    today_iso = datetime.now(BKK).isoformat(timespec="seconds")
    new_total = 0
    # Lazily build a legacy-SSL client only if needed (BLS).
    legacy_client: httpx.Client | None = None
    for s in MACRO_SOURCES:
        try:
            if s.get("legacy_ssl"):
                if legacy_client is None:
                    legacy_client = httpx.Client(
                        headers=HEADERS, timeout=TIMEOUT, follow_redirects=True,
                        verify=_legacy_ssl_context(),
                    )
                r = legacy_client.get(s["url"])
            else:
                r = client.get(s["url"])
            r.raise_for_status()
            html = r.text
        except Exception as e:  # noqa: BLE001
            print(f"  [macro/{s['source']}] FAIL {type(e).__name__}: {e}", flush=True)
            continue
        links = re.findall(s["link_re"], html, re.I)
        if s.get("swap_groups"):
            links = [(href, label) for label, href in links]
        seen_links = set()
        rows: list[tuple[Any, ...]] = []
        for href, label in links[:50]:
            href = href.strip()
            label = _strip_html(label).strip()
            if not label or len(label) < 6:
                continue
            if href.startswith("/"):
                full = s["base"].rstrip("/") + href
            elif href.startswith("http"):
                full = href
            else:
                full = s["base"].rstrip("/") + "/" + href
            if full in seen_links:
                continue
            seen_links.add(full)
            rid = _hash(s["source"], full, label[:120])
            rows.append((
                rid, s["source"], s["category"], today_iso,
                label[:400], full, label[:400], json.dumps([s["category"]]),
            ))
        if not rows:
            print(f"  [macro/{s['source']}] page fetched, 0 links extracted", flush=True)
            continue
        with conn() as c:
            ids = [r[0] for r in rows]
            existing = {row[0] for row in c.execute(
                "SELECT id FROM macro_items WHERE id = ANY (?)", [ids]
            ).fetchall()}
            new = [r for r in rows if r[0] not in existing]
            if new:
                c.executemany(
                    """
                    INSERT INTO macro_items
                      (id, source, category, datetime_iso, headline, url, body_excerpt, relevance_tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    new,
                )
            new_total += len(new)
        print(f"  [macro/{s['source']}] {len(rows)} links, {len(new) if rows else 0} new", flush=True)
    if legacy_client is not None:
        legacy_client.close()
    return new_total


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--only",
        choices=["rss", "signs", "sec", "macro"],
        help="Run only one source family.",
    )
    args = p.parse_args()

    started = datetime.now()
    print(f"=== external_sources @ {started.isoformat(timespec='seconds')} ===")

    results: dict[str, Any] = {}
    with httpx.Client(headers=HEADERS, timeout=TIMEOUT, follow_redirects=True) as client:
        plan = {
            "rss":   ("external_news", lambda: fetch_external_news(client)),
            "signs": ("trading_signs", lambda: fetch_trading_signs(client)),
            "sec":   ("sec_enforcement", lambda: fetch_sec_enforcement(client)),
            "macro": ("macro_overlays", lambda: fetch_macro_overlays(client)),
        }
        keys = [args.only] if args.only else list(plan.keys())
        for k in keys:
            label, fn = plan[k]
            print(f"\n-- {label} --", flush=True)
            try:
                results[label] = fn()
            except Exception as e:  # noqa: BLE001
                print(f"  [{label}] UNCAUGHT {type(e).__name__}: {e}", flush=True)
                traceback.print_exc()
                results[label] = -1

    print("\n=== summary ===")
    for k, v in results.items():
        print(f"  {k:20s}  {v}")
    elapsed = (datetime.now() - started).total_seconds()
    print(f"=== done in {elapsed:.1f}s ===")


if __name__ == "__main__":
    main()
