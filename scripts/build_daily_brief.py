"""Build a daily Discord digest from the deployed IS1 dashboard and push it.

Stdlib-only (matches house style in scripts/push_rm_c_digest.py).
Reads from https://is1-coverage-dashboard.tasinpong-k.workers.dev/data/*
live, aggregates into 4 embeds, POSTs to a Discord webhook.

Schedule: 09:30 BKK Mon-Fri (cron `30 9 * * 1-5`). Hermes runs cron in
local timezone; verify with `hermes cron status`.

Inputs (env vars):
  DAILY_BRIEF_WEBHOOK   — Discord webhook URL. **Required** — fail
                          closed if missing (we don't silently dry-run).
  DAILY_BRIEF_RM        — letter code (default "C" = IS1 user Champ).
                          Thai display names accepted via alias map.
  DAILY_BRIEF_BASE_URL  — dashboard base (default deployed URL).
  DAILY_BRIEF_DRY_RUN   — if "1", print payload + skip POST (for tests).
  DAILY_BRIEF_STATE_DIR — state file location (default
                          ~/.hermes/cron/daily_brief_state.json).

Logic:
  1. Atomic file lock (single-host only; multi-host is known limit).
  2. Idempotency check: skip if last_posted_date == today(BKK).
  3. Fetch ai-insights, morning-brief, tickers, disclosure-pulse.
  4. Freshness gate: skip if any asOf < BKK-today.
  5. Build 4 embeds; deterministic truncation in _format_* helpers.
  6. POST via _post_one (copied from push_rm_c_digest.py).
  7. Update state ONLY on successful POST.

Failure modes: see daily-brief-design.md §6.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------- constants

DEFAULT_BASE_URL = "https://is1-coverage-dashboard.tasinpong-k.workers.dev"
DEFAULT_RM = "C"
STATE_FILE_DEFAULT = Path.home() / ".hermes" / "cron" / "daily_brief_state.json"
# State filename in cron job state dir (legacy filename kept for history).
STATE_FILE = Path(os.environ.get("DAILY_BRIEF_STATE_DIR", str(STATE_FILE_DEFAULT))) / "state.json"

# Letter code is authoritative. Thai display names are deprecated aliases.
THAI_TO_LETTER = {"ฑศินพงศ์": "C"}

# Discord hard limits (https://discord.com/developers/docs/resources/message#embed-object-embed-limits)
DISCORD_MAX_EMBEDS_PER_MSG = 10
DISCORD_TOTAL_CHARS_MAX = 6000
EMBED_TITLE_MAX = 256
EMBED_DESC_MAX = 4096
EMBED_FIELD_NAME_MAX = 256
EMBED_FIELD_VALUE_MAX = 1024
EMBED_FOOTER_MAX = 2048

# Upstream build typically lands by ~12:30 BKK on weekdays. Hard gate.
REQUIRED_ASOF = "today_bkk"  # marker; actual check below

POST_INTERVAL_SEC = float(os.environ.get("POST_INTERVAL_SEC", "2.0"))


# ---------------------------------------------------------------- logging

def _log(msg: str) -> None:
    print(f"[build_daily_brief] {msg}", flush=True)


# ---------------------------------------------------------------- helpers

def _load_json(path: Path) -> dict | None:
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return None
    except (json.JSONDecodeError, OSError) as e:
        _log(f"WARN: json file {path} corrupt: {e}")
        return None


def _load_state(rm_key: str) -> dict:
    """Load state file. Defensive against tampering — returns empty dict
    if the file is corrupt or not a JSON object at top level."""
    s = _load_json(STATE_FILE)
    # Tamper defense: state must be a dict. If it's a list/string/etc,
    # treat as corrupt and start fresh. (Codex P0 #2 finding.)
    if not isinstance(s, dict):
        if s is not None:
            _log(f"WARN: state file {STATE_FILE} is not a dict (got {type(s).__name__}); ignoring")
        s = {}
    s.setdefault("last_posted_date", None)
    s.setdefault("last_posted_at", None)
    s.setdefault("seen_ids", [])
    s.setdefault("rm", rm_key)
    s.setdefault("ts_index", {})  # _id -> iso ts, for TTL-aware trim
    return s


def _resolve_rm(name: str) -> str:
    if not name:
        return DEFAULT_RM
    if name in THAI_TO_LETTER:
        return THAI_TO_LETTER[name]
    return name


def _atomic_write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2, sort_keys=True)
    os.replace(tmp, path)

def _bkk_today() -> str:
    """Return today's date in BKK as ISO date string."""
    bkk = timezone(timedelta(hours=7))
    return datetime.now(bkk).date().isoformat()


def _parse_iso_date(s: str) -> str | None:
    """Extract YYYY-MM-DD from an ISO datetime string."""
    if not s or len(s) < 10:
        return None
    return s[:10]


class _FileLock:
    """Cross-platform single-process file lock.

    Uses msvcrt.locking on Windows, fcntl.flock on Linux/macOS. Held for
    the lifetime of the context manager; released on exit.

    NOTE: this is intra-machine only. If Hermes ever runs on multiple
    machines, replace with a shared lock service.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self._fh = None

    def __enter__(self) -> bool:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self.path.open("w", encoding="utf-8")
        try:
            if sys.platform == "win32":
                import msvcrt
                # msvcrt.locking wants the number of bytes to lock; we
                # lock just the first byte as a sentinel.
                msvcrt.locking(self._fh.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self._fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except (OSError, IOError):
            self._fh.close()
            self._fh = None
            return False

    def __exit__(self, *exc) -> None:
        if self._fh is not None:
            try:
                if sys.platform == "win32":
                    import msvcrt
                    msvcrt.locking(self._fh.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(self._fh.fileno(), fcntl.LOCK_UN)
            except (OSError, IOError):
                pass
            self._fh.close()
            self._fh = None


# ---------------------------------------------------------------- HTTP

def _fetch_json(url: str, timeout: int = 30) -> dict | None:
    """Fetch JSON. Returns None on any failure."""
    req = urllib.request.Request(url, headers={"User-Agent": "IS1-daily-brief/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            if r.status != 200:
                _log(f"fetch {url}: HTTP {r.status}")
                return None
            body = r.read(5_000_000).decode("utf-8", "replace")
            return json.loads(body)
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError, ValueError) as e:
        _log(f"fetch {url}: {e}")
        return None


def _parse_retry_after(value: str | None) -> float:
    """Parse Retry-After header per RFC 7231 §7.1.3.

    Accepts either:
      - delta-seconds: e.g. "120"
      - HTTP-date:     e.g. "Wed, 05 Aug 2026 03:00:00 GMT"

    Returns seconds-to-wait. Falls back to 2s if the value is unparseable.
    """
    if not value:
        return 2.0
    s = value.strip()
    # Try delta-seconds first (cheap)
    try:
        return float(s)
    except ValueError:
        pass
    # Try HTTP-date (RFC 7231 §7.1.1.1 — IMF-fixdate preferred)
    from datetime import datetime, timezone
    for fmt in (
        "%a, %d %b %Y %H:%M:%S GMT",      # IMF-fixdate
        "%A, %d-%b-%y %H:%M:%S GMT",      # RFC 850 (obsolete)
        "%a %b %d %H:%M:%S %Y",            # asctime (C locale)
    ):
        try:
            target = datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            delta = (target - now).total_seconds()
            return max(0.0, min(delta, 300.0))  # clamp [0, 300s]
        except ValueError:
            continue
    # Unparseable — Discord specs delta-seconds only in practice, but be safe
    return 2.0


def _post_one(url: str, payload: dict, *, dry_run: bool, max_429_retries: int = 3) -> tuple[bool, int]:
    """Copy of push_rm_c_digest._post_one — kept here intentionally rather
    than imported, so this script is self-contained and CI-runnable from
    any path."""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json", "User-Agent": "IS1-daily-brief/1.0"},
        method="POST",
    )
    if dry_run:
        snippet = json.dumps(payload, ensure_ascii=False, indent=2)[:800]
        _log(f"DRY_RUN: POST {len(body)}B:\n{snippet}{'…' if len(body) > 800 else ''}")
        return True, 200

    attempts_429 = 0
    while True:
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status in (200, 204), r.status
        except urllib.error.HTTPError as e:
            status = e.code
            headers = {k.lower(): v for k, v in (e.headers or {}).items()}
            try:
                body_preview = e.read(200).decode("utf-8", "replace") if e.fp else ""
            except Exception:  # noqa: BLE001
                body_preview = ""
            if status == 429:
                if attempts_429 >= max_429_retries:
                    _log(f"429 exhausted: {body_preview!r}")
                    return False, status
                retry_after = _parse_retry_after(headers.get("retry-after"))
                _log(f"429; sleep {retry_after}s (retry {attempts_429+1}/{max_429_retries})")
                time.sleep(retry_after)
                attempts_429 += 1
                continue
            if 500 <= status < 600:
                _log(f"5xx {status}: {body_preview!r}; one 5s retry")
                time.sleep(5)
                try:
                    with urllib.request.urlopen(req, timeout=20) as r:
                        return r.status in (200, 204), r.status
                except Exception as e2:  # noqa: BLE001
                    _log(f"5xx retry failed: {e2}")
                    return False, status
            _log(f"4xx {status}: {body_preview!r}")
            return False, status
        except urllib.error.URLError as e:
            _log(f"URL error: {e}")
            return False, 0


def _truncate(s: str | None, n: int) -> str:
    """Deterministic truncation: keep first (n-1) chars + ellipsis."""
    if not s:
        return ""
    if len(s) <= n:
        return s
    return s[: n - 1] + "…"


def _validate_total_chars(embeds: list[dict]) -> list[dict]:
    """Ensure total embed characters ≤ DISCORD_TOTAL_CHARS_MAX by
    progressively dropping the last embed. The caller is responsible
    for keeping individual fields within their own limits."""
    total = 0
    out = []
    for e in embeds:
        title = e.get("title") or ""
        desc = e.get("description") or ""
        footer_text = (e.get("footer") or {}).get("text") or ""
        fields_chars = sum(
            len((f.get("name") or "")) + len((f.get("value") or ""))
            for f in (e.get("fields") or [])
        )
        e_chars = len(title) + len(desc) + fields_chars + len(footer_text)
        if total + e_chars > DISCORD_TOTAL_CHARS_MAX:
            _log(f"WARN: dropping embed {e.get('title', '?')[:40]!r} — would exceed 6000 chars")
            continue
        total += e_chars
        out.append(e)
    return out


def _clamp_fields(embeds: list[dict]) -> list[dict]:
    """Clamp every field's name/value/title to Discord per-embed limits."""
    for e in embeds:
        e["title"] = _truncate(e.get("title", ""), EMBED_TITLE_MAX)
        e["description"] = _truncate(e.get("description", ""), EMBED_DESC_MAX)
        if "footer" in e and "text" in e["footer"]:
            e["footer"]["text"] = _truncate(e["footer"]["text"], EMBED_FOOTER_MAX)
        for f in e.get("fields", []):
            f["name"] = _truncate(f.get("name", ""), EMBED_FIELD_NAME_MAX)
            f["value"] = _truncate(f.get("value", ""), EMBED_FIELD_VALUE_MAX)
    return embeds


# ---------------------------------------------------------------- sections

def _build_headline_embed(ai: dict, asof: str) -> dict:
    risk_count = len(ai.get("risk_flags") or [])
    color = 0xEF4444 if risk_count >= 4 else 0xF59E0B if risk_count >= 2 else 0x22C55E
    market_take = (ai.get("market_take") or "").strip()
    first_sentence = market_take.split(". ")[0] + ("." if market_take else "")
    return {
        "title": _truncate(f"📊 Daily Brief — {asof}", EMBED_TITLE_MAX),
        "description": _truncate(
            f"**{(ai.get('headline') or '').strip()}**\n\n{first_sentence}",
            EMBED_DESC_MAX,
        ),
        "color": color,
        "footer": {
            "text": _truncate(
                f"model={ai.get('model', '?')} · risk_flags={risk_count}", EMBED_FOOTER_MAX
            )
        },
    }


def _build_sector_pulse_embed(brief: dict) -> dict:
    """Top 3 + bottom 3 sectors by avg pct1d."""
    rows = brief.get("rows") or []
    by_sector: dict[str, list[float]] = {}
    for r in rows:
        pct = r.get("pct1d")
        sec = r.get("sector") or "?"
        if isinstance(pct, (int, float)) and not isinstance(pct, bool):
            by_sector.setdefault(sec, []).append(float(pct))

    avg_by_sec = []
    for sec, vals in by_sector.items():
        if not vals:
            continue
        up = sum(1 for v in vals if v > 0)
        avg_by_sec.append((sec, sum(vals) / len(vals), up, len(vals)))

    avg_by_sec.sort(key=lambda x: x[1])  # ascending by avg
    bottom3 = avg_by_sec[:3]
    top3 = list(reversed(avg_by_sec[-3:]))

    fields = []
    for sec, avg, up, n in top3:
        fields.append({
            "name": _truncate(f"▲ {sec}", EMBED_FIELD_NAME_MAX),
            "value": _truncate(f"+{avg:.2f}% ({up}/{n} up)", EMBED_FIELD_VALUE_MAX),
            "inline": True,
        })
    for sec, avg, up, n in bottom3:
        fields.append({
            "name": _truncate(f"▼ {sec}", EMBED_FIELD_NAME_MAX),
            "value": _truncate(f"{avg:.2f}% ({up}/{n} up)", EMBED_FIELD_VALUE_MAX),
            "inline": True,
        })

    return {
        "title": _truncate("📈 Sector Pulse — equal-weight 1-day %", EMBED_TITLE_MAX),
        "color": 0x3B82F6,
        "fields": fields,
    }


def _build_rm_watch_embed(brief: dict, rm_tickers: set[str]) -> dict:
    """Top 5 + bottom 5 RM-C tickers by pct1d. Plus hi52/lo52 flags."""
    rows = brief.get("rows") or []
    rm_rows = []
    for r in rows:
        if r.get("tk") not in rm_tickers:
            continue
        pct = r.get("pct1d")
        if not isinstance(pct, (int, float)) or isinstance(pct, bool):
            continue
        rm_rows.append(r)
    rm_rows.sort(key=lambda r: r.get("pct1d", 0), reverse=True)

    fields = []
    if rm_rows:
        fields.append({
            "name": _truncate("▲ Top movers", EMBED_FIELD_NAME_MAX),
            "value": _truncate(
                "\n".join(
                    f"`{r['tk']}` {r.get('pct1d', 0):+.2f}% · {r.get('sector', '?')}"
                    for r in rm_rows[:5]
                ) or "—",
                EMBED_FIELD_VALUE_MAX,
            ),
            "inline": False,
        })
        fields.append({
            "name": _truncate("▼ Bottom movers", EMBED_FIELD_NAME_MAX),
            "value": _truncate(
                "\n".join(
                    f"`{r['tk']}` {r.get('pct1d', 0):+.2f}% · {r.get('sector', '?')}"
                    for r in rm_rows[-5:][::-1]
                ) or "—",
                EMBED_FIELD_VALUE_MAX,
            ),
            "inline": False,
        })

    hi = [r for r in rm_rows if r.get("hi52")]
    lo = [r for r in rm_rows if r.get("lo52")]
    if hi or lo:
        flags = []
        if hi:
            flags.append(f"52wHI: {', '.join(r['tk'] for r in hi[:8])}")
        if lo:
            flags.append(f"52wLO: {', '.join(r['tk'] for r in lo[:8])}")
        fields.append({
            "name": _truncate("Flags", EMBED_FIELD_NAME_MAX),
            "value": _truncate("\n".join(flags), EMBED_FIELD_VALUE_MAX),
            "inline": False,
        })

    # Color: red if any pct1d < -5, green if all > -2, yellow otherwise.
    if rm_rows:
        worst = min(r.get("pct1d", 0) for r in rm_rows)
        best = max(r.get("pct1d", 0) for r in rm_rows)
        if worst < -5:
            color = 0xEF4444
        elif best > -2:
            color = 0x22C55E
        else:
            color = 0xF59E0B
    else:
        color = 0x3B82F6

    return {
        "title": _truncate(f"🎯 Your RM coverage ({len(rm_rows)} tickers)", EMBED_TITLE_MAX),
        "color": color,
        "fields": fields,
    }


# Thai-language red-flag keywords that flag a news item as risk-worthy.
# These are matched case-insensitively against title + excerpt. Keep small
# and high-precision; false positives are louder than misses here.
_RISK_KEYWORDS_TH = (
    "อายัด", "ฟ้องล้มละลาย", "ผิดนัดชำระหนี้", "พักการซื้อขาย", "delisting",
    "ถอดถอน", "ฉ้อโกง", "ทุจริต", "แจ้งความ", "ถูกกล่าวหา",
    "งบประมาณขาดทุน", "ขาดทุนต่อเนื่อง", "เข้าข่ายถูกเพิกถอน",
    "free-float ไม่ครบ", "ผู้สอบบัญชี", "ไม่แสดงความเห็น",
    "รายงานข้อสังเกต", "หยุดพักการซื้อขาย",
)

_RISK_KEYWORDS_EN = (
    "delisting", "bankruptcy", "default", "fraud", "restated",
    "qualified opinion", "audit qualification", "suspended trading",
    "insolvency", "going concern",
)

# Display-source → short emoji label for the embed (Thai readers
# recognise these brands at a glance).
_SOURCE_LABEL = {
    "HOONSMART": "🟠 HOONSMART",
    "KAOHOON": "🔵 KAOHOON",
    "PRACHACHAT": "🟢 PRACHACHAT",
    "RYT9": "🟡 RYT9",
}


def _is_risk_item(it: dict) -> bool:
    """True if a news item contains any high-severity keyword.

    Match against title + excerpt, case-insensitive. Title matches weigh
    slightly more — but we use a single boolean for the embed color.
    """
    haystack = " ".join([
        str(it.get("title", "") or ""),
        str(it.get("excerpt", "") or ""),
    ]).lower()
    if not haystack:
        return False
    for kw in _RISK_KEYWORDS_TH:
        if kw.lower() in haystack:
            return True
    for kw in _RISK_KEYWORDS_EN:
        if kw.lower() in haystack:
            return True
    return False


def _pick_news_for_embed(
    items: list[dict],
    rm_tickers: set[str],
    *,
    rm_min: int = 3,
    max_rows: int = 5,
) -> tuple[list[dict], str]:
    """Apply the RM-C-first, market-fallback rule.

    Returns (picked_items, source_label) where source_label is one of
    "rm-c", "market-fallback", "none". The picked items are already
    sorted newest-first and capped at max_rows.

    Rule:
      1. Filter to items whose tk is in rm_tickers (if any).
      2. If RM-C items >= rm_min: show RM-C only.
      3. Else: fall back to all items (market-wide).
      4. In either branch: newest first.
    """
    if not items:
        return [], "none"

    # Items may be missing tk — treat them as market-wide (never RM-C).
    def _ts(it: dict) -> str:
        return str(it.get("ts", "") or "")

    rm_items = [it for it in items if it.get("tk") in rm_tickers]
    rm_items.sort(key=_ts, reverse=True)

    if len(rm_items) >= rm_min:
        return rm_items[:max_rows], "rm-c"

    # Fallback: market-wide, newest first.
    market_items = sorted(items, key=_ts, reverse=True)
    return market_items[:max_rows], "market-fallback"


def _build_news_embed(
    news: dict,
    rm_tickers: set[str],
    asof: str,
    dashboard_url: str = DEFAULT_BASE_URL,
) -> dict | None:
    """Build the 'News Watch' embed (embed #5).

    Returns None if no items at all — caller should skip rather than
    emit an empty embed. Otherwise returns a 1024-char-safe embed with
    up to 5 rows (newest first), source labels, ticker tags, and a
    link to the dashboard news explorer.
    """
    items = news.get("items") or []
    picked, src_label = _pick_news_for_embed(items, rm_tickers)

    if not picked:
        return None

    # Color: red if any row is a flagged risk item, blue otherwise.
    has_risk = any(_is_risk_item(it) for it in picked)
    color = 0xEF4444 if has_risk else 0x06B6D4  # cyan-500

    # Title changes per source label so the user knows whether this
    # is RM-C priority or a market fallback.
    if src_label == "rm-c":
        title = f"📰 RM-C News Watch — {asof} ({len(picked)} items)"
    else:
        title = f"📰 Market News Watch — {asof} ({len(picked)} items, no RM-C hits)"

    # Build fields. Up to 5 fields × 1024 chars each is well under the
    # 6000-char total embed cap (other embeds ~3000 chars combined).
    fields = []
    for it in picked:
        src = it.get("source", "?")
        src_disp = _SOURCE_LABEL.get(src, src)
        tk = it.get("tk", "")
        risk_marker = " 🔴" if _is_risk_item(it) else ""
        url = it.get("url", "")
        # Title line: **<ticker>** <short source> 🔴 if risk
        title_line = f"{src_disp}"
        if tk:
            title_line += f" · `{tk}`"
        title_line += risk_marker
        # Body line: hyperlink the title for click-through.
        news_title = _truncate(it.get("title", ""), 200)
        if url:
            body_line = f"[{news_title}]({url})"
        else:
            body_line = news_title
        # Combine into a single field value (one row per news item).
        fields.append({
            "name": _truncate(title_line, EMBED_FIELD_NAME_MAX),
            "value": _truncate(body_line, EMBED_FIELD_VALUE_MAX),
            "inline": False,
        })

    footer_text = f"src={','.join(news.get('sources', []) or [])}"
    if src_label == "rm-c":
        footer_text += " · scope=rm-c"
    else:
        footer_text += " · scope=market-fallback"
    if has_risk:
        footer_text += " · ⚠️ flagged keywords"

    return {
        "title": _truncate(title, EMBED_TITLE_MAX),
        "color": color,
        "fields": fields,
        "footer": {"text": _truncate(footer_text, EMBED_FOOTER_MAX)},
    }


def _build_filings_today_embed(pulse: dict, rm_tickers: set[str], asof: str) -> dict:
    """Count today's filings (BKK-day boundary) + recent RM-C filings."""
    filings = pulse.get("filings") or []
    bkk = timezone(timedelta(hours=7))
    today = _bkk_today()

    def _is_today(ts: str) -> bool:
        try:
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=bkk)
            return dt.astimezone(bkk).date().isoformat() == today
        except (ValueError, TypeError):
            return False

    today_all = [f for f in filings if _is_today(f.get("ts", ""))]
    today_rmc = [f for f in today_all if f.get("tk") in rm_tickers]
    high_all = [f for f in today_all if f.get("severity") == "high"]
    high_rmc = [f for f in today_rmc if f.get("severity") == "high"]

    recent_rmc = sorted(today_rmc, key=lambda f: f.get("ts", ""), reverse=True)[:5]
    fields = [
        {
            "name": _truncate("📊 Counts (BKK-day)", EMBED_FIELD_NAME_MAX),
            "value": _truncate(
                f"all: {len(today_all)} · RM C: {len(today_rmc)}\n"
                f"high-sev: {len(high_all)} · high RM C: {len(high_rmc)}",
                EMBED_FIELD_VALUE_MAX,
            ),
            "inline": False,
        },
    ]
    if recent_rmc:
        bullets = []
        for f in recent_rmc:
            sev = f.get("severity", "low")
            sev_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(sev, "⚪")
            type_ = f.get("type") or "?"
            bullets.append(f"{sev_emoji} `{f.get('tk', '?')}` {type_} ({sev})")
        fields.append({
            "name": _truncate(f"Latest RM C ({len(recent_rmc)})", EMBED_FIELD_NAME_MAX),
            "value": _truncate("\n".join(bullets), EMBED_FIELD_VALUE_MAX),
            "inline": False,
        })
    else:
        fields.append({
            "name": _truncate("Latest RM C", EMBED_FIELD_NAME_MAX),
            "value": _truncate("No RM C filings today.", EMBED_FIELD_VALUE_MAX),
            "inline": False,
        })

    color = 0xF59E0B if high_rmc else 0x3B82F6

    return {
        "title": _truncate(f"📄 Today ({asof}): {len(today_all)} filings", EMBED_TITLE_MAX),
        "color": color,
        "fields": fields,
    }


# ---------------------------------------------------------------- main

def _load_webhook_from_secret_file() -> str | None:
    """Last-resort lookup: read webhook URL from a secret file at
    ~/.hermes/secrets/daily_brief.env. Used when DAILY_BRIEF_WEBHOOK env
    var is unset (i.e. when the script is invoked by a Hermes cron that
    doesn't pass env vars). The file format is one KEY=VALUE per line,
    shell-style quoting allowed."""
    secret = Path.home() / ".hermes" / "secrets" / "daily_brief.env"
    if not secret.exists():
        return None
    try:
        for line in secret.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == "DAILY_BRIEF_WEBHOOK":
                # Strip optional surrounding quotes
                return v.strip().strip('"').strip("'")
    except OSError as e:
        _log(f"WARN: reading {secret}: {e}")
    return None


def main() -> int:
    # Resolve webhook: env var first, then secret file fallback.
    # This ordering lets cron pass env directly (test/dev) while still
    # working when cron doesn't (production).
    webhook = os.environ.get("DAILY_BRIEF_WEBHOOK", "").strip()
    if not webhook:
        webhook = _load_webhook_from_secret_file() or ""
    if not webhook:
        _log("FATAL: DAILY_BRIEF_WEBHOOK not set in env or secret file — fail closed (no silent dry-run).")
        return 1
    dry_run = os.environ.get("DAILY_BRIEF_DRY_RUN") == "1"
    if dry_run:
        _log("DAILY_BRIEF_DRY_RUN=1 — POSTs skipped, payload logged.")

    rm_input = os.environ.get("DAILY_BRIEF_RM", DEFAULT_RM).strip() or DEFAULT_RM
    rm_key = _resolve_rm(rm_input)
    base_url = os.environ.get("DAILY_BRIEF_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    state_path = Path(os.environ.get("DAILY_BRIEF_STATE_DIR", str(STATE_FILE_DEFAULT)))

    # ---- file lock
    lock = _FileLock(state_path.parent / ".daily_brief.lock")
    if not lock.__enter__():
        _log("another instance is already running — exiting 0.")
        return 0
    try:
        # ---- idempotency check (uses _load_state for tamper defense)
        state = _load_state(rm_key)
        last_posted_date = state.get("last_posted_date")
        last_posted_at = state.get("last_posted_at")
        today_bkk = _bkk_today()
        if last_posted_date == today_bkk:
            try:
                last_dt = datetime.fromisoformat(last_posted_at.replace("Z", "+00:00"))
                age_h = (datetime.now(timezone.utc) - last_dt).total_seconds() / 3600
                if age_h < 24:
                    _log(f"already posted today at {last_posted_at} ({age_h:.1f}h ago) — skipping.")
                    return 0
            except (ValueError, TypeError, AttributeError):
                pass  # corrupt last_posted_at; treat as no state

        # ---- fetch
        _log(f"fetching from {base_url} ...")
        ai = _fetch_json(f"{base_url}/data/ai-insights.json")
        brief = _fetch_json(f"{base_url}/data/morning-brief.json")
        tickers = _fetch_json(f"{base_url}/data/tickers.json")
        pulse = _fetch_json(f"{base_url}/data/disclosure-pulse.json")

        if not (ai and brief and tickers and pulse):
            _log(f"FATAL: required source missing — ai={bool(ai)} brief={bool(brief)} "
                  f"tickers={bool(tickers)} pulse={bool(pulse)}")
            return 1
        # News is OPTIONAL — we degrade gracefully if it's missing or stale.
        news = _fetch_json(f"{base_url}/data/external-news.json")

        # ---- freshness gate
        bkk = timezone(timedelta(hours=7))
        today_bkk_date = datetime.now(bkk).date()
        for name, obj in (("ai-insights", ai), ("morning-brief", brief)):
            asof = _parse_iso_date(obj.get("asOf") or "")
            if not asof:
                _log(f"WARN: {name} has no asOf — skipping freshness check for that source")
                continue
            try:
                asof_date = datetime.fromisoformat(asof).date()
                if asof_date < today_bkk_date:
                    _log(
                        f"SKIP: {name}.asOf={asof} < today {today_bkk_date.isoformat()} "
                        f"(stale data — do not label as today's brief)"
                    )
                    return 0
            except ValueError:
                continue

        # ---- RM C ticker list
        rm_tickers = {t["tk"] for t in (tickers.get("tickers") or []) if t.get("rm") == rm_key}
        if not rm_tickers:
            _log(f"FATAL: no tickers for rm={rm_key!r}")
            return 1
        _log(f"rm={rm_key}: {len(rm_tickers)} tickers covered")

        # ---- overall asOf (earlier of ai + brief)
        ai_asof = _parse_iso_date(ai.get("asOf") or "") or today_bkk
        brief_asof = _parse_iso_date(brief.get("asOf") or "") or today_bkk
        overall_asof = min(ai_asof, brief_asof)

        # ---- build embeds
        embeds: list[dict] = []
        if ai:
            embeds.append(_build_headline_embed(ai, overall_asof))
        if brief:
            embeds.append(_build_sector_pulse_embed(brief))
            embeds.append(_build_rm_watch_embed(brief, rm_tickers))
        if pulse:
            embeds.append(_build_filings_today_embed(pulse, rm_tickers, overall_asof))
        # News embed is optional — skipped silently if external-news.json
        # is missing/empty/stale, since it's a soft add-on, not a core
        # pillar. We do not gate the whole brief on it.
        if news and (news.get("items") or []):
            news_emb = _build_news_embed(news, rm_tickers, overall_asof)
            if news_emb:
                embeds.append(news_emb)
                _log(f"news embed added ({news_emb['footer']['text']})")
            else:
                _log("news source had items but picker returned none — skipped")

        # ---- clamp + validate
        embeds = _clamp_fields(embeds)
        embeds = _validate_total_chars(embeds)
        if len(embeds) > DISCORD_MAX_EMBEDS_PER_MSG:
            _log(f"WARN: dropping {len(embeds) - DISCORD_MAX_EMBEDS_PER_MSG} embeds "
                 f"to respect {DISCORD_MAX_EMBEDS_PER_MSG} cap")
            embeds = embeds[:DISCORD_MAX_EMBEDS_PER_MSG]
        if not embeds:
            _log("FATAL: no embeds built")
            return 1

        # ---- post
        payload = {
            "username": "IS1 Daily Brief",
            "content": _truncate(
                f"**Daily Brief — {overall_asof}** · {rm_key} coverage", 2000
            ),
            "embeds": embeds,
        }
        ok, status = _post_one(webhook, payload, dry_run=dry_run)
        if not ok:
            _log(f"webhook failed: status={status}")
            return 1

        # ---- state update ONLY after successful POST
        state["last_posted_date"] = today_bkk
        state["last_posted_at"] = datetime.now(timezone.utc).isoformat()
        state["rm"] = rm_key
        try:
            _atomic_write_json(state_path, state)
        except OSError as e:
            _log(f"WARN: state write failed: {e} (re-run may re-post — at-least-once)")
        _log(f"posted {len(embeds)} embed(s); state updated.")
        return 0
    finally:
        lock.__exit__()


if __name__ == "__main__":
    sys.exit(main())