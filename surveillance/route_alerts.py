"""CLI for sending alerts (email-only).

Modes:
  --mode critical   send each unsent critical disclosure as one batched email per RM
  --mode digest     send one combined digest of unsent material disclosures
  --mode both       run critical first, then digest

  --dry-run         print messages, do not actually send
  --max N           cap critical messages per run (default 5)
"""

from __future__ import annotations

import argparse
import time

from collections import defaultdict

from alerts import (
    EMAIL_CHANNEL,
    EmailClient,
    _rm_lookup,
    fetch_unsent,
    format_critical_digest,
    format_digest,
    mark_all_unsent_as_sent,
    mark_sent,
)


def _send_critical(client, max_send: int, dry_run: bool, since: str | None) -> int:
    rows = fetch_unsent("critical", channel=EMAIL_CHANNEL, since=since)
    if not rows:
        print("[critical] nothing to send.")
        return 0

    rows_to_send = rows[:max_send]
    print(f"[critical] {len(rows)} unsent (will batch up to {max_send} this run).")

    # Pre-group by RM so mark_sent can fire per-RM after each RM's chunks
    # land. Previously a mid-loop SMTP failure left earlier RMs un-marked,
    # so the next run would re-send already-delivered Critical alerts.
    rm_map = _rm_lookup()
    by_rm: dict[str, list[dict]] = defaultdict(list)
    for r in rows_to_send:
        by_rm[rm_map.get(r["symbol"], "Unassigned")].append(r)

    if dry_run:
        total_chunks = 0
        for rm in sorted(by_rm):
            chunks = format_critical_digest(by_rm[rm])
            for ch in chunks:
                print("---DRY---"); print(ch); print()
            total_chunks += len(chunks)
        print(f"[critical] dry_run=True (would have sent {total_chunks} message(s) across {len(by_rm)} RM(s))")
        return 0

    sent_total = 0
    for rm in sorted(by_rm):
        rm_rows = by_rm[rm]
        chunks = format_critical_digest(rm_rows)
        try:
            last_msg_id = "0"
            for i, ch in enumerate(chunks, 1):
                body = ch + "\n\n---\n📌 Champ — Issuer Department 1, SET"
                text = f"[SETSURV] 🔴 Critical — {rm} ({i}/{len(chunks)})\n\n" + body
                last_msg_id = client.send(text, priority="high")
                time.sleep(1.1)  # polite throttle
        except Exception as e:  # noqa: BLE001
            print(f"[critical] FAIL for RM {rm}: {type(e).__name__}: {e} — leaving rows unsent for next run.")
            continue
        # All chunks for this RM landed — record delivery so we don't re-spam.
        mark_sent([r["news_id"] for r in rm_rows], tier="critical",
                  channel=EMAIL_CHANNEL, message_id=last_msg_id)
        sent_total += len(rm_rows)
        print(f"[critical] sent {len(chunks)} chunk(s) to RM {rm} covering {len(rm_rows)} item(s)")

    print(f"[critical] total sent: {sent_total} item(s) across {len(by_rm)} RM(s)")
    return sent_total


def _send_digest(client, dry_run: bool, since: str | None) -> int:
    rows = fetch_unsent("material", channel=EMAIL_CHANNEL, since=since)
    if not rows:
        print("[digest] nothing to send.")
        return 0

    rm_map = _rm_lookup()

    by_rm: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_rm[rm_map.get(r["symbol"], "Unassigned")].append(r)

    if dry_run:
        total_chunks = 0
        for rm in sorted(by_rm):
            chunks = format_digest(by_rm[rm])
            for i, ch in enumerate(chunks, 1):
                preview = f"[SETSURV] 🟡 Material disclosure digest — RM: {rm} ({i}/{len(chunks)})\n\n" + ch
                print("---DRY---"); print(preview); print()
            total_chunks += len(chunks)
        print(f"[digest] dry_run=True (would have sent {total_chunks} message(s) across {len(by_rm)} RM(s))")
        return 0

    print(f"[digest] {len(rows)} unsent material item(s) grouped by {len(by_rm)} RM(s).")
    sent_total = 0
    for rm in sorted(by_rm):
        rm_rows = by_rm[rm]
        chunks = format_digest(rm_rows)
        try:
            last_msg_id = "0"
            for i, ch in enumerate(chunks, 1):
                body = ch + "\n\n---\n📌 Champ — Issuer Department 1, SET"
                text = f"[SETSURV] 🟡 Material — {rm} ({i}/{len(chunks)})\n\n" + body
                last_msg_id = client.send(text)
                time.sleep(1.1)
        except Exception as e:  # noqa: BLE001
            print(f"[digest] FAIL for RM {rm}: {type(e).__name__}: {e} — leaving rows unsent for next run.")
            continue
        # Mark per-RM after success so a mid-batch SMTP failure on a later RM
        # doesn't trick later runs into re-sending already-delivered RMs.
        mark_sent([r["news_id"] for r in rm_rows], tier="digest",
                  channel=EMAIL_CHANNEL, message_id=last_msg_id)
        sent_total += len(rm_rows)
        print(f"[digest] sent {len(chunks)} chunk(s) to RM {rm} covering {len(rm_rows)} item(s)")

    print(f"[digest] total sent: {sent_total} item(s) across {len(by_rm)} RM(s)")
    return sent_total


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["critical", "digest", "both"], default="both")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--max", type=int, default=5,
                   help="Cap critical messages per run (default 5; raise for batch sends).")
    p.add_argument("--since",
                   help="Only alert on disclosures dated on/after YYYY-MM-DD (defends against floods).")
    p.add_argument("--mark-only", action="store_true",
                   help="One-time cutover: mark every unsent classified item as already sent. "
                        "Run this once after wiring up so the historical backlog doesn't flood you.")
    args = p.parse_args()

    if args.mark_only:
        counts = mark_all_unsent_as_sent(channel=EMAIL_CHANNEL)
        print(f"[mark-only] marked as sent without alerting: {counts}")
        return

    client = None if args.dry_run else EmailClient()

    started = time.monotonic()
    sent_crit = sent_dig = 0
    if args.mode in ("critical", "both"):
        sent_crit = _send_critical(client, args.max, args.dry_run, args.since)
    if args.mode in ("digest", "both"):
        sent_dig = _send_digest(client, args.dry_run, args.since)

    elapsed = time.monotonic() - started
    print(f"\n=== route_alerts done in {elapsed:.1f}s "
          f"(dry_run={args.dry_run})  critical_sent={sent_crit}  digest_items={sent_dig} ===")


if __name__ == "__main__":
    main()
