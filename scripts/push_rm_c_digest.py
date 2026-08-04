"""Push new disclosures for one RM to a Discord webhook.

Stdlib-only by design (matches scripts/notify_failure.py house style). Runs
at the end of .github/workflows/disclosure-refresh.yml, after the JSON
regen commit, so we only push for filings that actually shipped to
data/disclosure-pulse.json. Dedup is local
(`data/rm_c_push_state.json` committed by the same workflow step) — no
external state store.

Identity convention: tickers.json stores `rm` as a letter code
("C", "K", "O", "G", "P", "T") for the IS1 team. The deployment's
chat-dock.js maps these to friendly Thai names at the UI layer, but the
authoritative key is the letter. We therefore default to "C" and treat
the Thai name (`ฑศินพงศ์`) as a documented alias. Switching display
names later MUST NOT replay the backlog.

Inputs (env vars):
  DISCORD_PUSH_WEBHOOK    — webhook URL; absent → dry-run (logs payload).
  RM_NAME                 — letter code (default "C" = IS1 user "Champ").
                            Aliases: Thai first names (ฑศินพงศ์ → C).
  SEVERITY_MIN            — "low" | "medium" | "high" (default "low" = all).
  DISCORD_USERNAME        — bot display name (default "IS1 Disclosure Pulse").

Logic:
  1. Load data/disclosure-pulse.json + data/tickers.json.
  2. Resolve RM_NAME to its letter code (handles Thai alias).
  3. Fail-closed: assert the resolved rm has a non-empty ticker set.
  4. Filter filings: ticker.tk in rm's coverage, severity >= SEVERITY_MIN,
     _id not already in state, ts <= 24h after state.pushed_at (skew guard).
  5. Build Discord embeds (≤10 embeds / message, 25 fields / embed — both
     are Discord limits; oversized payloads return 400).
  6. POST messages sequentially with 2s spacing. Honor Discord 429
     `Retry-After`. Cap retry attempts at 3.
  7. Persist ONLY successfully-posted filings to state file.
  8. Workflow step then `git add && commit && push` the state file.

Failures:
  - 4xx (non-429) → log, skip state update, exit 1.
  - 429 → honor Retry-After, retry up to 3 times.
  - 5xx → retry once with 5s sleep.
  - State write fails → exit 2 (don't lose history).
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PULSE = DATA / "disclosure-pulse.json"
TICKERS = DATA / "tickers.json"

# Stable digest key. Use the letter code (authoritative in tickers.json);
# treat Thai display names as deprecated aliases.
DEFAULT_RM_NAME = "C"
THAI_TO_LETTER = {"ฑศินพงศ์": "C"}  # extend if aliases change

SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3}

STATE_FILE = DATA / "rm_c_push_state.json"  # legacy filename — keeps history.

EMBED_COLOR = {"high": 0xEF4444, "medium": 0xF59E0B, "low": 0x22C55E}

# Discord hard limits (https://discord.com/developers/resources/message):
DISCORD_MAX_EMBEDS_PER_MSG = 10
DISCORD_MAX_FIELDS_PER_EMBED = 25
DISCORD_FIELD_VALUE_MAX = 1024
DISCORD_TITLE_MAX = 256

# Politeness: 2s spacing between posts keeps a 30 msg/min webhook safe even
# with backfills. Configurable via env for tests.
POST_INTERVAL_SEC = float(os.environ.get("POST_INTERVAL_SEC", "2.0"))


def _log(msg: str) -> None:
    print(f"[push_rm_c_digest] {msg}", flush=True)


def _load_json(path: Path) -> dict | None:
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return None


def _tickers_for_rm(rm_key: str) -> set[str]:
    """Return covered tickers owned by `rm_key` (letter code, authoritative)."""
    t = _load_json(TICKERS)
    if not t:
        return set()
    return {tk["tk"] for tk in (t.get("tickers") or []) if tk.get("rm") == rm_key}


def _resolve_rm(name: str) -> str:
    """Map Thai alias → letter code; pass through if already a code."""
    if not name:
        return DEFAULT_RM_NAME
    if name in THAI_TO_LETTER:
        return THAI_TO_LETTER[name]
    return name  # letter code or unrecognised; tickers.json decides.


def _load_state(rm_key: str) -> dict:
    s = _load_json(STATE_FILE) or {}
    s.setdefault("pushed_at", None)
    s.setdefault("seen_ids", [])
    s.setdefault("rm", rm_key)
    s.setdefault("ts_index", {})  # _id -> iso ts, for TTL-aware trim
    return s


def _save_state(state: dict) -> None:
    """Atomic write — tmp + rename."""
    tmp = STATE_FILE.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=2, sort_keys=True)
    tmp.replace(STATE_FILE)


def _new_filings(
    filings: list[dict],
    tk_set: set[str],
    seen: set[str],
    min_sev: int,
) -> list[dict]:
    """Filter for an rm's tickers, severity threshold, and unseen _ids.

    `pushed_at` is observability only — late/backfilled filings carry
    timestamps older than the last push and SHOULD be re-pushed if not
    already in `seen`. Dedup by `_id` is authoritative.
    """
    out: list[dict] = []
    for f in filings:
        tk = f.get("tk") or ""
        if tk_set and tk not in tk_set:
            continue
        sev = f.get("severity") or "low"
        if SEVERITY_RANK.get(sev, 1) < min_sev:
            continue
        fid = f.get("_id") or ""
        if not fid or fid in seen:
            continue
        out.append(f)
    return out


def _severity_emoji(sev: str) -> str:
    return {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(sev, "⚪")


def _format_field(f: dict) -> dict:
    sev = f.get("severity") or "low"
    ts = (f.get("ts") or "")[:16].replace("T", " ")
    tk = f.get("tk") or "?"
    type_ = f.get("type") or "?"
    title = (f.get("title") or "").strip().replace("\n", " ")[:240]
    url = f.get("url") or ""
    value = f"`{ts}` · {type_}\n{title}"
    if url:
        value += f"\n[SET filing]({url})"
    return {
        "name": f"{_severity_emoji(sev)} {tk} · {sev}"[:DISCORD_TITLE_MAX],
        "value": value[:DISCORD_FIELD_VALUE_MAX],
        "inline": False,
    }


def _chunk(items: list[dict], n: int) -> Iterable[list[dict]]:
    for i in range(0, len(items), n):
        yield items[i:i + n]


def _build_messages(
    filings: list[dict], rm_key: str, window_days: int, username: str
) -> list[dict]:
    """Slice filings into Discord message payloads (≤10 embeds × 25 fields)."""
    if not filings:
        return []
    total = len(filings)
    field_chunks = list(_chunk(filings, DISCORD_MAX_FIELDS_PER_EMBED))
    # Each message holds up to 10 embeds. With 25 fields/embed that's
    # 250 fields/message; we never get close in practice (RM C backfill
    # ~1961 filings → 79 embeds → 8 messages of 10+9).
    embed_chunks = list(_chunk(field_chunks, DISCORD_MAX_EMBEDS_PER_MSG))

    parts = len(embed_chunks)
    messages: list[dict] = []
    for part_i, embed_chunk in enumerate(embed_chunks, start=1):
        embeds = []
        for chunk in embed_chunk:
            worst = "high" if any(
                f.get("severity") == "high" for f in chunk
            ) else "medium" if any(
                f.get("severity") == "medium" for f in chunk
            ) else "low"
            hi = sum(1 for f in chunk if f.get("severity") == "high")
            med = sum(1 for f in chunk if f.get("severity") == "medium")
            lo = sum(1 for f in chunk if f.get("severity") == "low")
            title = (
                f"📄 RM {rm_key} — {total} new SET disclosures"
                if parts == 1
                else f"📄 RM {rm_key} — {total} new · part {part_i}/{parts}"
            )
            embeds.append({
                "title": title[:DISCORD_TITLE_MAX],
                "color": EMBED_COLOR.get(worst, EMBED_COLOR["low"]),
                "footer": {
                    "text": (
                        f"window {window_days}d · "
                        f"high {hi} · medium {med} · low {lo}"
                    )
                },
                "fields": [_format_field(f) for f in chunk],
            })
        messages.append({
            "username": username,
            "content": (
                f"**{total} new** SET disclosure"
                f"{'s' if total != 1 else ''} for RM {rm_key}. "
                f"Severity ≥ **{os.environ.get('SEVERITY_MIN', 'low')}**."
                if part_i == 1
                else f"(part {part_i}/{parts})"
            ),
            "embeds": embeds,
        })
    return messages


def _post_one(url: str, payload: dict, *, dry_run: bool, max_429_retries: int = 3) -> tuple[bool, int]:
    """POST a single payload. Returns (ok, http_status).

    Honors Discord 429 with Retry-After header. Retries up to max_429_retries
    times on 429 (with the requested delay). Single retry on 5xx.
    """
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json", "User-Agent": "IS1-push/2.0"},
        method="POST",
    )
    if dry_run:
        snippet = json.dumps(payload, ensure_ascii=False, indent=2)[:600]
        _log(f"DRY_RUN: POST {len(body)}B, {len(payload.get('embeds', []))} embeds:\n{snippet}{'…' if len(body) > 600 else ''}")
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
                    _log(f"429 exhausted after {max_429_retries} retries: {body_preview!r}")
                    return False, status
                # Honor Retry-After (seconds). Defaults to 2 if absent.
                retry_after = float(headers.get("retry-after", "2"))
                _log(f"429 rate-limited; sleeping {retry_after}s (retry {attempts_429+1}/{max_429_retries})")
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


def _post_messages(
    url: str, messages: list[dict], *, dry_run: bool
) -> list[bool]:
    """Sequentially POST each message. Returns per-message ok list."""
    results: list[bool] = []
    for i, msg in enumerate(messages):
        ok, _ = _post_one(url, msg, dry_run=dry_run)
        results.append(ok)
        if not ok:
            _log(f"message {i+1}/{len(messages)} FAILED — aborting sequence")
            # Mark remaining as failed so per-batch persistence is honest.
            results.extend([False] * (len(messages) - len(results)))
            break
        if i < len(messages) - 1 and not dry_run:
            time.sleep(POST_INTERVAL_SEC)
    return results


def _ts_skew_check(filings: list[dict]) -> None:
    """Log a warning if any filing's ts is >24h in the future (clock drift)."""
    now = datetime.now(timezone.utc)
    for f in filings[:50]:  # sample first 50 to keep log short
        ts = f.get("ts")
        if not ts:
            continue
        try:
            # Strip timezone; assume +07:00 if absent (BKK convention).
            dt = datetime.fromisoformat(ts)
            if dt.tzinfo is None:
                from datetime import timedelta
                dt = dt.replace(tzinfo=timezone(timedelta(hours=7)))
            delta = (dt - now).total_seconds()
            if abs(delta) > 86400 * 2:  # >48h skew
                _log(f"WARN: ts skew {_id_short(f.get('_id'))} ts={ts} delta_h={delta/3600:.1f}")
        except (ValueError, TypeError):
            pass


def _id_short(fid: str | None) -> str:
    return (fid or "")[:10]


def main() -> int:
    rm_input = os.environ.get("RM_NAME", DEFAULT_RM_NAME).strip() or DEFAULT_RM_NAME
    rm_key = _resolve_rm(rm_input)
    min_sev_name = (os.environ.get("SEVERITY_MIN") or "low").lower()
    if min_sev_name not in SEVERITY_RANK:
        _log(f"invalid SEVERITY_MIN={min_sev_name!r}; falling back to 'low'")
        min_sev_name = "low"
    min_sev = SEVERITY_RANK[min_sev_name]
    webhook = os.environ.get("DISCORD_PUSH_WEBHOOK", "").strip()
    dry_run = not webhook
    username = os.environ.get("DISCORD_USERNAME", "IS1 Disclosure Pulse")[:80]

    if dry_run:
        _log("no DISCORD_PUSH_WEBHOOK set — DRY RUN.")

    pulse = _load_json(PULSE)
    if not pulse:
        _log(f"FATAL: {PULSE} missing — nothing to push.")
        return 1

    tk_set = _tickers_for_rm(rm_key)
    if not tk_set:
        _log(
            f"FATAL: no tickers mapped to rm_key={rm_key!r} (input={rm_input!r}) "
            f"in {TICKERS}. Check the RM_NAME env var."
        )
        return 1

    state = _load_state(rm_key)
    seen: set[str] = set(state.get("seen_ids", []))
    ts_index: dict[str, str] = state.get("ts_index", {})

    new = _new_filings(
        pulse.get("filings") or [],
        tk_set,
        seen,
        min_sev,
    )
    new.sort(key=lambda f: f.get("ts") or "", reverse=True)
    _ts_skew_check(new)

    # Observability counters (Codex P1 — fail-closed invariant logging).
    total_filings = len(pulse.get("filings") or [])
    matched = sum(
        1 for f in (pulse.get("filings") or [])
        if f.get("tk") in tk_set
    )
    _log(
        f"counts: total={total_filings} matched_rm={matched} "
        f"severity>={min_sev_name} new={len(new)} state_size={len(seen)} "
        f"tickers_in_rm={len(tk_set)} rm={rm_key}"
    )

    if not new:
        _log("no new filings since last push — done.")
        # Don't bump pushed_at — backfills should still fire when state is
        # repopulated. Just exit 0.
        return 0

    messages = _build_messages(
        new, rm_key, int(pulse.get("windowDays") or 90), username
    )
    _log(f"posting {len(messages)} message(s) for {len(new)} new filings")

    results = _post_messages(webhook or "https://example.invalid/dry-run", messages, dry_run=dry_run)
    n_ok = sum(1 for r in results if r)
    n_failed = len(results) - n_ok

    # Per-batch persistence (Codex P1 — at-least-once delivery honesty).
    # Persist ONLY the filings whose message posted successfully. Failed
    # messages will be retried on the next run.
    persisted_ids: set[str] = set()
    if n_ok > 0:
        # Build cumulative-filing-id → success: the first N messages map to
        # the first N×embeds×fields filings.
        field_chunks = list(_chunk(new, DISCORD_MAX_FIELDS_PER_EMBED))
        embed_chunks = list(_chunk(field_chunks, DISCORD_MAX_EMBEDS_PER_MSG))
        msg_i = 0
        for embeds_chunk in embed_chunks:
            if msg_i >= n_ok:
                break
            for field_chunk in embeds_chunk:
                for f in field_chunk:
                    fid = f.get("_id")
                    if fid:
                        persisted_ids.add(fid)
                        ts_index[fid] = f.get("ts") or ""
            msg_i += 1

    state["seen_ids"] = list(seen | persisted_ids)
    state["ts_index"] = ts_index
    state["rm"] = rm_key
    if persisted_ids:
        # Use the latest successfully-posted filing's ts.
        latest_ts = max(
            (ts_index.get(fid, "") for fid in persisted_ids),
            default=state.get("pushed_at") or "",
        )
        if latest_ts:
            state["pushed_at"] = latest_ts

    if n_failed > 0 and not dry_run:
        _log(f"PARTIAL: {n_ok}/{len(results)} messages OK; {n_failed} failed. State updated for OK only.")
        # Still commit partial state so duplicates are bounded.

    if not dry_run:
        try:
            _save_state(state)
        except OSError as e:
            _log(f"FATAL: state write failed: {e}")
            return 2
    else:
        _log("DRY_RUN: state NOT written.")

    _log(
        f"done. ok={n_ok}/{len(results)} persisted_ids={len(persisted_ids)} "
        f"state_total={len(state['seen_ids'])}"
    )
    # Non-zero exit only if EVERYTHING failed (so retry on next run).
    return 0 if n_ok > 0 else 1


if __name__ == "__main__":
    sys.exit(main())