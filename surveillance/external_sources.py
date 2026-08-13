"""Daily fetch of non-SETLink data sources.

Four scrapers, one entry point. All run once per day, alongside the SETLink
poller, in the same surveillance job. Each scraper is best-effort: a network
failure on one source must not break the others.

Sources:
  - external_news: RSS feeds from RYT9, Kaohoon, Hoonsmart, Prachachat,
    Bangkok Biznews. Ticker-matched against the 232-name coverage.
  - trading_signs: SET trading-sign HTML page (SP/NP/NC/CC/C/ST/DS/CB).
  - sec_enforcement: SEC iDisc Enforce/Recent table.
  - sec_form59: SEC iDisc Form 59 management/related-person trades.

Run:
  python surveillance/external_sources.py            # all source families
  python surveillance/external_sources.py --only rss # one source family
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import traceback
from datetime import datetime, timezone, timedelta
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urljoin
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
# Some Thai wire feeds are slow rather than down; one retry on a longer budget
# recovers them without holding the whole run hostage.
RSS_RETRY_TIMEOUT = httpx.Timeout(45.0, connect=15.0)


BKK = timezone(timedelta(hours=7))

# Hard failures (a render that never returned HTML, a feed that never
# answered) recorded per source. A source that returns 0 rows because the day
# was quiet and one that returns 0 rows because the site is unreachable look
# identical in the summary line — this is what tells them apart.
SOURCE_FAILURES: dict[str, list[str]] = {}


def _note_failure(source: str, reason: str) -> None:
    SOURCE_FAILURES.setdefault(source, []).append(reason)


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
            print(
                f"  [rss/{feed['source']}] {type(e).__name__}: {e} — retrying "
                f"on a longer timeout",
                flush=True,
            )
            try:
                r = client.get(feed["url"], timeout=RSS_RETRY_TIMEOUT)
                r.raise_for_status()
                items = _parse_rss(r.text)
            except Exception as e2:  # noqa: BLE001
                print(f"  [rss/{feed['source']}] FAIL {type(e2).__name__}: {e2}", flush=True)
                _note_failure("external_news", f"{feed['source']}: {type(e2).__name__}")
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


def fetch_sec_enforcement(client: httpx.Client) -> int:  # noqa: ARG001 (WAF needs a real browser, not httpx)
    # SEC iDisc is behind an F5 bot-defense WAF, so the old flow (GET the page to
    # scrape data-rtk, then POST GetEnforces) now just gets a JS challenge and
    # finds no rtk. Render the page with headless Chromium instead and parse the
    # table the page's own JS draws — same columns, same parser as before.
    html = _fetch_idisc_html_via_browser(SEC_ENFORCE_PAGE)
    if not html:
        print("  [sec_enforcement] no HTML rendered from SEC Enforce page", flush=True)
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
        if date_val.lower() == "enforcement date" or respondent.lower() == "name":
            continue
        if not respondent or len(respondent) < 3:
            continue
        # Try to find a coverage ticker anywhere in the row. Many SEC rows put
        # the listed-company ticker in the summarized facts, not the name cell.
        matches = find_tickers(" | ".join(clean))
        matched = sorted(matches)[0] if matches else None
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
# sec_form59 — SEC iDisc Form 59 daily management trades
# ---------------------------------------------------------------------------
#
# The daily SET disclosure "SEC News : Form 59 summary" is only a pointer. The
# structured rows live on SEC iDisc's Form 59 page. The default page renders
# only the current day, while the search result is capped at 100 rows. The
# scraper therefore queries one transaction date at a time: 90 days when the
# store is empty or stale, then a 7-day overlap for incremental refreshes.

SEC_R59_PAGES = [
    ("en", "https://market.sec.or.th/public/idisc/en/r59"),
    ("th", "https://market.sec.or.th/public/idisc/th/r59"),
]
SEC_R59_ORIGIN = "https://market.sec.or.th"


class _HtmlTableParser(HTMLParser):
    """Tiny table extractor for SEC server-rendered pages."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[list[dict[str, Any]]] = []
        self._in_tr = False
        self._in_cell = False
        self._cell_parts: list[str] = []
        self._cell_links: list[str] = []
        self._row: list[dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag_l = tag.lower()
        if tag_l == "tr":
            self._in_tr = True
            self._row = []
        elif self._in_tr and tag_l in {"td", "th"}:
            self._in_cell = True
            self._cell_parts = []
            self._cell_links = []
        elif self._in_cell and tag_l == "a":
            href = dict(attrs).get("href")
            if href:
                self._cell_links.append(href)
        elif self._in_cell and tag_l in {"br", "p", "div"}:
            self._cell_parts.append(" ")

    def handle_data(self, data: str) -> None:
        if self._in_cell:
            self._cell_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag_l = tag.lower()
        if tag_l in {"td", "th"} and self._in_cell:
            text = re.sub(r"\s+", " ", "".join(self._cell_parts)).strip()
            self._row.append({"text": text, "links": self._cell_links[:]})
            self._in_cell = False
        elif tag_l == "tr" and self._in_tr:
            if self._row:
                self.rows.append(self._row)
            self._in_tr = False


def _parse_number(value: str | None) -> float | None:
    if not value:
        return None
    # Preserve the last numeric token so "Revoked by Reporter 0.72" still yields
    # the disclosed average price while the revoked flag captures the caveat.
    nums = re.findall(r"-?\d+(?:,\d{3})*(?:\.\d+)?|-?\d+(?:\.\d+)?", value)
    if not nums:
        return None
    try:
        return float(nums[-1].replace(",", ""))
    except ValueError:
        return None


def _parse_form59_date(value: str | None) -> str | None:
    m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", value or "")
    if not m:
        return None
    day, month, year = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if year > 2400:
        year -= 543
    return f"{year:04d}-{month:02d}-{day:02d}"


_EN_MONTHS = {
    "jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3,
    "apr": 4, "april": 4, "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7,
    "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9, "oct": 10,
    "october": 10, "nov": 11, "november": 11, "dec": 12, "december": 12,
}
_TH_MONTHS = {
    "ม.ค.": 1, "มกราคม": 1, "ก.พ.": 2, "กุมภาพันธ์": 2, "มี.ค.": 3,
    "มีนาคม": 3, "เม.ย.": 4, "เมษายน": 4, "พ.ค.": 5, "พฤษภาคม": 5,
    "มิ.ย.": 6, "มิถุนายน": 6, "ก.ค.": 7, "กรกฎาคม": 7, "ส.ค.": 8,
    "สิงหาคม": 8, "ก.ย.": 9, "กันยายน": 9, "ต.ค.": 10, "ตุลาคม": 10,
    "พ.ย.": 11, "พฤศจิกายน": 11, "ธ.ค.": 12, "ธันวาคม": 12,
}


def _parse_snapshot_date(text: str, lang: str) -> str | None:
    flat = re.sub(r"\s+", " ", text)
    if lang == "en":
        m = re.search(
            r"(?:Information|Last updated)\s+on\s+(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})",
            flat,
            re.I,
        )
        if not m:
            return None
        month = _EN_MONTHS.get(m.group(2).lower())
        year = int(m.group(3))
    else:
        m = re.search(
            r"(?:ข้อมูลประจำวันที่|Last updated on)\s+(\d{1,2})\s+([^\s]+)\s+(\d{4})",
            flat,
            re.I,
        )
        if not m:
            return None
        month = _TH_MONTHS.get(m.group(2))
        year = int(m.group(3))
        if year > 2400:
            year -= 543
    if not month:
        return None
    return f"{year:04d}-{month:02d}-{int(m.group(1)):02d}"


def _company_symbol(value: str) -> tuple[str | None, str]:
    text = re.sub(r"\s+", " ", value or "").strip()
    matches = re.findall(r"\(([A-Z][A-Z0-9&.\-]{0,12})\)", text)
    if not matches:
        return None, text
    symbol = matches[-1].upper().replace(".", "")
    company = re.sub(r"\s*\(" + re.escape(matches[-1]) + r"\)\s*$", "", text).strip()
    return symbol, company


def _normalize_form59_side(value: str) -> tuple[str, str]:
    raw = re.sub(r"\s+", " ", value or "").strip()
    low = raw.lower()
    if "purchase" in low or "acquisition" in low or "ซื้อ" in raw:
        return "buy", raw or "Purchase"
    if "sale" in low or "disposition" in low or "ขาย" in raw:
        return "sell", raw or "Sale"
    if "transfer" in low or "โอน" in raw:
        return "transfer", raw or "Transfer"
    return (low or "other"), raw


def _extract_form59_rows(html: str, *, lang: str, source_url: str) -> list[dict[str, Any]]:
    parser = _HtmlTableParser()
    parser.feed(html)
    page_text = _strip_html(html)
    # The page label is the SEC snapshot refresh date, not each row's filing
    # date. Treating it as filing_date makes historical searches look as though
    # every transaction was filed today and also destabilizes row IDs.
    source_as_of = _parse_snapshot_date(page_text, lang)
    rows: list[dict[str, Any]] = []
    for cells in parser.rows:
        texts = [c["text"] for c in cells]
        if len(texts) < 8:
            continue
        if any("name of company" in t.lower() for t in texts[:2]):
            continue
        symbol, company = _company_symbol(texts[0])
        if not symbol or symbol not in TICKER_SET:
            continue
        row_text = " ".join(texts)
        links = [
            urljoin(SEC_R59_ORIGIN, href)
            for c in cells
            for href in c.get("links", [])
            if href
        ]
        amount = _parse_number(texts[5] if len(texts) > 5 else "")
        price = _parse_number(texts[6] if len(texts) > 6 else "")
        side, side_label = _normalize_form59_side(texts[7] if len(texts) > 7 else "")
        remark = " | ".join(t for t in texts[8:] if t) if len(texts) > 8 else ""
        revoked = bool(re.search(r"\b(revoked|cancel|ยกเลิก)\b", row_text, re.I))
        transaction_date = _parse_form59_date(texts[4] if len(texts) > 4 else "")
        rid = _hash(
            "R59", symbol, transaction_date or "",
            texts[1] if len(texts) > 1 else "", texts[2] if len(texts) > 2 else "",
            texts[3] if len(texts) > 3 else "", texts[5] if len(texts) > 5 else "",
            texts[6] if len(texts) > 6 else "", texts[7] if len(texts) > 7 else "",
            links[0] if links else "",
        )
        rows.append({
            "id": rid,
            "symbol": symbol,
            "company_name": company[:300],
            "reporter": (texts[1] if len(texts) > 1 else "")[:300],
            "relationship": (texts[2] if len(texts) > 2 else "")[:300],
            "security_type": (texts[3] if len(texts) > 3 else "")[:200],
            "transaction_date": transaction_date,
            "filing_date": None,
            "amount": amount,
            "price": price,
            "side": side[:40],
            "side_label": side_label[:80],
            "remark": remark[:500],
            "is_revoked": revoked,
            "detail_url": links[0] if links else "",
            "source_url": source_url,
            "source_lang": lang,
            "source_as_of": source_as_of,
            "raw": texts,
        })
    return rows


def _fetch_idisc_html_via_browser(url: str) -> str:
    """Render a SEC iDisc page (Form 59, Enforce/Recent, …) with headless Chromium.

    The SEC iDisc site sits behind an F5 bot-defense WAF that serves a
    JavaScript challenge to plain HTTP clients: httpx/requests get either a
    244-byte "Request Rejected" shell or a ~47 KB obfuscated challenge script,
    never the data table. Only a real browser that executes the challenge JS,
    reloads, and then runs the page's AJAX fetch ends up with the rendered
    table. So we drive a headless browser, wait for the table to populate, and
    return the full page HTML for the caller's row parser.

    Best-effort: returns "" if Playwright/Chromium isn't available or the
    render fails, so the rest of the external-source run is unaffected.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  [idisc] playwright not installed — cannot pass SEC WAF", flush=True)
        return ""
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
            )
            context = browser.new_context(
                user_agent=UA,
                locale="en-US",
                viewport={"width": 1366, "height": 900},
            )
            # Hide the automation flag F5 Shape probes for.
            context.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
            )
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            # The WAF challenge reloads the page, then the page's own AJAX fills
            # the table. Wait for the table element, then for at least one data
            # row beyond the header. On a zero-filing day only the header exists
            # — tolerate that timeout and parse whatever rendered.
            page.wait_for_selector("table", timeout=45000)
            try:
                page.wait_for_function(
                    "() => document.querySelectorAll('table tr').length > 1",
                    timeout=15000,
                )
            except Exception:  # noqa: BLE001
                pass
            html = page.content()
            browser.close()
            return html
    except Exception as e:  # noqa: BLE001
        print(f"  [idisc] browser render failed {type(e).__name__}: {e}", flush=True)
        _note_failure("sec_enforcement", f"idisc render: {type(e).__name__}")
        return ""


def _form59_lookback_days() -> int:
    """Use a deep backfill for an empty/stale store, then a cheap overlap."""
    override = os.environ.get("SEC_FORM59_LOOKBACK_DAYS")
    if override:
        try:
            return max(1, min(365, int(override)))
        except ValueError:
            print(f"  [sec_form59] invalid SEC_FORM59_LOOKBACK_DAYS={override!r}; using auto", flush=True)
    latest: str | None = None
    try:
        with conn() as c:
            row = c.execute(
                "SELECT MAX(COALESCE(transaction_date, filing_date)) FROM sec_form59"
            ).fetchone()
            latest = row[0] if row else None
    except Exception:  # noqa: BLE001
        latest = None
    if latest:
        try:
            age = datetime.now(BKK).date() - datetime.fromisoformat(str(latest)).date()
            if age.days <= 14:
                return 7
        except ValueError:
            pass
    return 90


def _fetch_form59_history_via_browser(
    url: str, *, lookback_days: int
) -> list[tuple[str, str]]:
    """Render one SEC transaction-date result page per weekday.

    The SEC result table is capped at 100 rows and sorted by company. A single
    90-day request therefore silently drops most names. Day-by-day requests
    stay below that cap in normal operation and let an empty database bootstrap
    a useful rolling history.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  [idisc] playwright not installed — cannot pass SEC WAF", flush=True)
        return []

    today = datetime.now(BKK).date()
    days = [
        today - timedelta(days=offset)
        for offset in range(lookback_days)
        if (today - timedelta(days=offset)).weekday() < 5
    ]
    pages: list[tuple[str, str]] = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-blink-features=AutomationControlled"],
            )
            context = browser.new_context(
                user_agent=UA,
                locale="en-US",
                viewport={"width": 1366, "height": 900},
            )
            context.add_init_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
            )
            page = context.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_selector("table", timeout=45000)
            page.check("#ctl00_CPH_rblDateType_0")

            for index, day in enumerate(days):
                display_date = day.strftime("%d/%m/%Y")
                try:
                    page.fill("#BSDateFrom", display_date)
                    page.fill("#BSDateTo", display_date)
                    page.click("#ctl00_CPH_btSearch", timeout=15000)
                    page.wait_for_load_state("domcontentloaded", timeout=60000)
                    page.wait_for_selector("table", timeout=30000)
                    html = page.content()
                    parser = _HtmlTableParser()
                    parser.feed(html)
                    data_rows = max(0, len(parser.rows) - 1)
                    if data_rows >= 100:
                        print(
                            f"  [sec_form59] warning: SEC result cap reached on {day.isoformat()}",
                            flush=True,
                        )
                    pages.append((day.isoformat(), html))
                    if (index + 1) % 15 == 0:
                        print(
                            f"  [sec_form59] fetched {index + 1}/{len(days)} weekdays",
                            flush=True,
                        )
                except Exception as e:  # noqa: BLE001
                    print(
                        f"  [sec_form59] {day.isoformat()} render FAIL "
                        f"{type(e).__name__}: {e}",
                        flush=True,
                    )
                    page.goto(url, wait_until="domcontentloaded", timeout=60000)
                    page.wait_for_selector("table", timeout=45000)
                    page.check("#ctl00_CPH_rblDateType_0")
            browser.close()
    except Exception as e:  # noqa: BLE001
        print(f"  [sec_form59] history render failed {type(e).__name__}: {e}", flush=True)
        _note_failure("sec_form59", f"r59 render: {type(e).__name__}")
    return pages


def _dedupe_form59_store(c: Any) -> int:
    """Remove legacy duplicates whose old IDs included the page refresh date."""
    duplicate_ids = [
        row[0]
        for row in c.execute(
            """
            SELECT id
            FROM sec_form59
            QUALIFY ROW_NUMBER() OVER (
                PARTITION BY symbol,
                             COALESCE(transaction_date, ''),
                             COALESCE(reporter, ''),
                             COALESCE(relationship, ''),
                             COALESCE(security_type, ''),
                             amount,
                             price,
                             COALESCE(side, ''),
                             COALESCE(side_label, ''),
                             COALESCE(remark, ''),
                             is_revoked,
                             COALESCE(detail_url, '')
                ORDER BY scraped_at DESC NULLS LAST, id DESC
            ) > 1
            """
        ).fetchall()
    ]
    if duplicate_ids:
        c.execute("DELETE FROM sec_form59 WHERE id = ANY (?)", [duplicate_ids])
    return len(duplicate_ids)


def fetch_sec_form59(client: httpx.Client) -> int:  # noqa: ARG001 (WAF needs a real browser, not httpx)
    parsed: list[dict[str, Any]] = []
    source_used = ""
    lookback_days = _form59_lookback_days()
    print(f"  [sec_form59] querying {lookback_days}-day rolling history", flush=True)
    for lang, url in SEC_R59_PAGES:
        rendered_pages = _fetch_form59_history_via_browser(
            url, lookback_days=lookback_days
        )
        if not rendered_pages:
            continue
        for query_date, html in rendered_pages:
            try:
                rows = _extract_form59_rows(html, lang=lang, source_url=url)
                for row in rows:
                    row["query_date"] = query_date
                parsed.extend(rows)
            except Exception as e:  # noqa: BLE001
                print(
                    f"  [sec_form59/{lang}] {query_date} parse FAIL "
                    f"{type(e).__name__}: {e}",
                    flush=True,
                )
        source_used = url
        # EN and TH carry the same rows. Once EN rendered successfully, parsing
        # zero coverage rows is a valid result and must not launch another full
        # history run in Thai.
        break

    parsed = list({row["id"]: row for row in parsed}.values())
    if not parsed:
        print(
            f"  [sec_form59] no coverage rows in the {lookback_days}-day SEC history",
            flush=True,
        )
        return 0

    with conn() as c:
        ids = [r["id"] for r in parsed]
        existing = {
            row[0]
            for row in c.execute("SELECT id FROM sec_form59 WHERE id = ANY (?)", [ids]).fetchall()
        }
        new = [r for r in parsed if r["id"] not in existing]
        if new:
            c.executemany(
                """
                INSERT INTO sec_form59
                  (id, symbol, company_name, reporter, relationship, security_type,
                   transaction_date, filing_date, amount, price, side, side_label,
                   remark, is_revoked, detail_url, source_url, source_lang, raw_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        r["id"], r["symbol"], r["company_name"], r["reporter"],
                        r["relationship"], r["security_type"], r["transaction_date"],
                        r["filing_date"], r["amount"], r["price"], r["side"],
                        r["side_label"], r["remark"], r["is_revoked"], r["detail_url"],
                        r["source_url"], r["source_lang"],
                        json.dumps(r.get("raw", []), ensure_ascii=False),
                    )
                    for r in new
                ],
            )
        removed = _dedupe_form59_store(c)
    buys = sum(1 for r in parsed if r["side"] == "buy")
    sells = sum(1 for r in parsed if r["side"] == "sell")
    print(
        f"  [sec_form59] {len(parsed)} coverage rows ({buys} buy, {sells} sell), "
        f"{len(new)} new, {removed} legacy duplicates removed via {source_used}",
        flush=True,
    )
    return len(new)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _source_health_path() -> str:
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "source-health.json",
    )


def _write_source_health(results: dict[str, Any], path: str | None = None) -> None:
    """Publish per-source ingest status so a dead scraper is visible off-log.

    Every fetcher swallows its own errors and returns 0 so that one dead site
    cannot take the run down. The cost is that "no news today" and "this site
    has been unreachable for weeks" print the same summary line. This file
    keeps the two apart, and survives a --only run by merging rather than
    replacing the sources it did not touch.
    """
    path = path or _source_health_path()
    try:
        with open(path, encoding="utf-8") as f:
            sources = (json.load(f) or {}).get("sources", {})
    except (OSError, json.JSONDecodeError):
        sources = {}

    for label, value in results.items():
        rows = value[0] if isinstance(value, tuple) else value
        failures = SOURCE_FAILURES.get(label) or []
        sources[label] = {
            "rows": rows,
            "ok": not failures and rows != -1,
            "failures": failures,
            "checkedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }

    payload = {
        "asOf": datetime.now(BKK).date().isoformat(),
        "checkedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "failingCount": sum(1 for s in sources.values() if not s.get("ok")),
        "sources": sources,
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(
            f"  -> wrote source-health.json ({payload['failingCount']} failing)",
            flush=True,
        )
    except OSError as e:  # noqa: BLE001
        print(f"  [source_health] write FAIL {type(e).__name__}: {e}", flush=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--only",
        choices=["rss", "signs", "sec", "r59"],
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
            "r59":   ("sec_form59", lambda: fetch_sec_form59(client)),
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
        failures = SOURCE_FAILURES.get(k) or []
        print(f"  {k:20s}  {v}" + (f"   FAILED: {'; '.join(failures)}" if failures else ""))

    # GitHub renders these in the run summary, so an unreachable source stops
    # looking like a quiet day in a green build.
    for k, failures in SOURCE_FAILURES.items():
        print(f"::warning::{k} did not ingest — {'; '.join(failures)}", flush=True)

    _write_source_health(results)

    elapsed = (datetime.now() - started).total_seconds()
    print(f"=== done in {elapsed:.1f}s ===")


if __name__ == "__main__":
    main()
