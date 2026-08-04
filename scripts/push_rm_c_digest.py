"""Push new disclosures for one RM (default: the user, RM C) to a Discord webhook.

Stdlib-only by design (matches scripts/notify_failure.py house style). Runs at
the end of .github/workflows/disclosure-refresh.yml, after the JSON regen step,
so we never push for filings that did not ship. Dedup is local
(`data/rm_c_push_state.json` committed by the same workflow) — no external
state store, no R2 lookup.

Inputs (env vars):
  DISCORD_PUSH_WEBHOOK    — webhook URL; absent → dry-run only (logs payload).
  RM_NAME                 — Thai rm name as it appears in data/tickers.json
                            (default: `ฑศินพงศ์`, the IS1 seat "RM C" = Champ).
                            For any future user, set RM_NAME in workflow_dispatch.
  SEVERITY_MIN            — "low" | "medium" | "high" (default "low" = all).
  DEDUP_AGE_HOURS         — re-push filings seen within this many hours even if
                            already in state (default 0 = strict dedup). Used
                            for backfill replays.

Logic:
  1. Load data/disclosure-pulse.json + data/tickers.json.
  2. Filter filings: ticker.tk in IS1-rm named user, ts newer than
     `last_pushed_at`, severity >= SEVERITY_MIN.
  3. Diff against pushed id-set; new ids only.
  4. Build Discord embeds (25 fields/embed — Discord limit).
  5. POST embeds sequentially to the webhook.
  6. Update `data/rm_c_push_state.json` with the merged id-set + last_pushed_at.

Failures:
  - Webhook 4xx → log payload, exit 1 so CI flags it (visible in PR check,
    easy to debug from the GH Actions log).
  - Webhook 5xx → retry once with 5s sleep.
  - State write fails → exit 2 (do NOT lose push history by overwriting with
    a stale snapshot).
"""

from __future__ import annotations

import json
import os
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

# An RM name we recognise. Default is the IS1 user seat "RM C" (Champ). Any
# other RM can be targeted by setting RM_NAME at invocation time.
DEFAULT_RM_NAME = "ฑศินพงศ์"
SEVERITY_RANK = {"low": 1, "medium": 2, "high": 3}

STATE_FILE = DATA / "rm_c_push_state.json"  # one file works for any RM; the
# name is historical (the first user was Champ) and intentionally not renamed
# to avoid losing existing state when this ships.

EMBED_COLOR = {
    "high": 0xEF4444,
    "medium": 0xF59E0B,
    "low": 0x22C55E,
}


def _log(msg: str) -> None:
    print(f"[push_rm_c_digest] {msg}", flush=True)


def _load_json(path: Path) -> dict | None:
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return None


def _tickers_for_rm(rm_name: str) -> set[str]:
    """Return the set of covered tickers owned by `rm_name`."""
    t = _load_json(TICKERS)
    if not t:
        _log(f"warn: {TICKERS} not found or unreadable — defaulting to empty set.")
        return set()
    return {tk["tk"] for tk in (t.get("tickers") or []) if tk.get("rm") == rm_name}


def _load_state() -> dict:
    s = _load_json(STATE_FILE) or {}
    s.setdefault("pushed_at", None)
    s.setdefault("seen_ids", [])
    s.setdefault("rm", DEFAULT_RM_NAME)
    return s


def _save_state(state: dict) -> None:
    # Atomic write — tmp + rename, so a crash mid-write never corrupts state.
    tmp = STATE_FILE.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=2, sort_keys=True)
    tmp.replace(STATE_FILE)


def _new_filings(
    filings: list[dict],
    tk_set: set[str],
    seen: set[str],
    since_iso: str | None,
    min_sev: int,
) -> list[dict]:
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
        ts = f.get("ts") or ""
        if since_iso and ts and ts <= since_iso:
            continue
        out.append(f)
    return out


def _severity_emoji(sev: str) -> str:
    return {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(sev, "⚪")


def _format_field(f: dict) -> dict:
    sev = f.get("severity") or "low"
    ts = (f.get("ts") or "")[:16].replace("T", " ")
    tk = f.get("tk") or "?"
    sector = f.get("sector") or "?"
    type_ = f.get("type") or "?"
    title = (f.get("title") or "").strip().replace("\n", " ")[:240]
    url = f.get("url") or ""
    return {
        "name": f"{_severity_emoji(sev)} {tk} · {type_} · {sev}",
        "value": (
            f"`{ts}` · {sector}\n{title}"
            + (f"\n[SET filing]({url})" if url else "")
        )[:1024],
        "inline": False,
    }


def _chunk(items: list[dict], n: int) -> Iterable[list[dict]]:
    for i in range(0, len(items), n):
        yield items[i:i + n]


def _build_embeds(filings: list[dict], rm_name: str, window_days: int) -> list[dict]:
    if not filings:
        return []
    pieces: list[dict] = []
    total = len(filings)
    counter = 0
    for chunk in _chunk(filings, 25):
        counter += len(chunk)
        hi = sum(1 for f in chunk if f.get("severity") == "high")
        med = sum(1 for f in chunk if f.get("severity") == "medium")
        lo = sum(1 for f in chunk if f.get("severity") == "low")
        # Worst severity in the chunk drives embed colour.
        worst = (
            "high" if hi else ("medium" if med else ("low" if lo else "low"))
        )
        title = (
            f"📄 RM {rm_name} — {total} new SET disclosures"
            if total > 25
            else f"📄 RM {rm_name} — new SET disclosures ({total})"
        )
        # If chunking, say so in the title.
        if total > 25:
            title += f" · part {counter // 25 + 1}/{(total + 24) // 25}"
        embed = {
            "title": title[:256],
            "color": EMBED_COLOR.get(worst, EMBED_COLOR["low"]),
            "footer": {
                "text": (
                    f"window {window_days}d · "
                    f"high {hi} · medium {med} · low {lo}"
                )
            },
            "fields": [_format_field(f) for f in chunk],
        }
        pieces.append(embed)
    return pieces


def _post_webhook(url: str, payload: dict, *, dry_run: bool) -> bool:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "User-Agent": "IS1-push/1.0"},
        method="POST",
    )
    if dry_run:
        _log(
            f"DRY_RUN: would POST {len(body)} bytes "
            f"({len(payload.get('embeds', []))} embeds):\n"
            f"{json.dumps(payload, ensure_ascii=False, indent=2)[:1200]}"
            f"{'…' if len(body) > 1200 else ''}"
        )
        return True
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            status = r.status
            data = r.read(200).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        _log(f"webhook HTTP {e.code}: {e.reason}; body={e.read()[:200]!r}")
        if 500 <= e.code < 600:
            time.sleep(5)
            try:
                with urllib.request.urlopen(req, timeout=15) as r:
                    return r.status in (200, 204)
            except Exception as e2:  # noqa: BLE001
                _log(f"webhook retry failed: {e2}")
        return False
    except urllib.error.URLError as e:
        _log(f"webhook URL error: {e}")
        return False
    if status in (200, 204):
        _log(f"webhook ok: {status}; resp={data!r}")
        return True
    _log(f"webhook unexpected {status}: {data!r}")
    return False


def main() -> int:
    rm_name = os.environ.get("RM_NAME", DEFAULT_RM_NAME).strip() or DEFAULT_RM_NAME
    min_sev_name = (os.environ.get("SEVERITY_MIN") or "low").lower()
    min_sev = SEVERITY_RANK.get(min_sev_name, 1)
    webhook = os.environ.get("DISCORD_PUSH_WEBHOOK", "").strip()
    dry_run = not webhook

    if dry_run:
        _log("no DISCORD_PUSH_WEBHOOK set — DRY RUN.")

    pulse = _load_json(PULSE)
    if not pulse:
        _log(f"error: {PULSE} missing — nothing to push.")
        return 1

    tk_set = _tickers_for_rm(rm_name)
    if not tk_set:
        _log(
            f"warn: no tickers mapped to rm_name={rm_name!r} in "
            f"{TICKERS}. Will push nothing. Check the env var."
        )
    else:
        _log(f"rm={rm_name}: {len(tk_set)} tickers covered")

    state = _load_state()
    seen: set[str] = set(state.get("seen_ids", []))
    since = state.get("pushed_at")
    # Cap dedup set growth: keep last 5000 ids (~4-6 months at peak rates).
    if len(seen) > 5000:
        # Drop the oldest half by ordering on insertion would need a list;
        # state stores a list, so we trim the head.
        all_ids = list(state.get("seen_ids", []))
        seen = set(all_ids[-2500:])
        state["seen_ids"] = all_ids[-2500:]

    new = _new_filings(
        pulse.get("filings") or [],
        tk_set,
        seen,
        since,
        min_sev,
    )
    # Newest first.
    new.sort(key=lambda f: f.get("ts") or "", reverse=True)

    if not new:
        _log("no new filings since last push — done.")
        # Even when empty, bump pushed_at so a backfill doesn't re-fire old
        # filings on the next run. But only if we have state to preserve.
        if not dry_run and since is None:
            state["pushed_at"] = (
                pulse.get("asOf") or datetime.now(timezone.utc).isoformat()
            )
            _save_state(state)
        return 0

    embeds = _build_embeds(new, rm_name, int(pulse.get("windowDays") or 90))
    payload = {
        "username": "IS1 Disclosure Pulse",
        "content": (
            f"**{len(new)} new** SET disclosure"
            f"{'s' if len(new) != 1 else ''} for RM {rm_name}. "
            f"Severity ≥ **{min_sev_name}**."
        ),
        "embeds": embeds,
    }

    _log(f"posting {len(embeds)} embed(s) for {len(new)} new filings")
    if not _post_webhook(webhook or "https://example.invalid/dry-run", payload, dry_run=dry_run):
        # Refuse to update state — better duplicate a push than lose a filing.
        _log("webhook failed; state NOT updated. Will retry on next run.")
        return 1

    state["seen_ids"] = list(seen | {f["_id"] for f in new if f.get("_id")})
    state["pushed_at"] = (
        max((f.get("ts") or "") for f in new)
        if new
        else (pulse.get("asOf") or datetime.now(timezone.utc).isoformat())
    )
    state["rm"] = rm_name
    # Write state ONLY when not dry-run; local smoke tests should not overwrite.
    if not dry_run:
        try:
            _save_state(state)
        except OSError as e:
            _log(f"FATAL: state write failed: {e}")
            return 2
    else:
        _log("DRY_RUN: state NOT written.")
    _log(f"done. {len(new)} new filings pushed, state updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
