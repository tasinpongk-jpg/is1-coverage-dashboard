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

from alerts import (
    EMAIL_CHANNEL,
    EmailClient,
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

    chunks = format_critical_digest(rows_to_send)

    if dry_run:
        for i, ch in enumerate(chunks, 1):
            print("---DRY---"); print(ch); print()
        print(f"[critical] dry_run=True (would have sent {len(chunks)} batched message(s))")
        return 0

    last_msg_id = "0"
    for i, ch in enumerate(chunks, 1):
        body = ch + "\n\n---\n📌 Champ — Issuer Department 1, SET"
        text = f"[SETSURV] 🔴 Critical disclosures batch ({i}/{len(chunks)})\n\n" + body
        last_msg_id = client.send(text, priority="high")
        time.sleep(1.1)  # polite throttle

    mark_sent([r["news_id"] for r in rows_to_send], tier="critical",
              channel=EMAIL_CHANNEL, message_id=last_msg_id)
    print(f"[critical] sent {len(chunks)} batched message(s) covering {len(rows_to_send)} item(s)")
    return len(rows_to_send)


def _send_digest(client, dry_run: bool, since: str | None) -> int:
    rows = fetch_unsent("material", channel=EMAIL_CHANNEL, since=since)
    if not rows:
        print("[digest] nothing to send.")
        return 0

    from collections import defaultdict

    from alerts import _rm_lookup
    rm_map = _rm_lookup()

    by_rm: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_rm[rm_map.get(r["symbol"], "Unassigned")].append(r)

    total_chunks = 0
    all_news_ids = [r["news_id"] for r in rows]
    last_msg_id = "0"

    if dry_run:
        for rm in sorted(by_rm):
            chunks = format_digest(by_rm[rm])
            for i, ch in enumerate(chunks, 1):
                preview = f"[SETSURV] 🟡 Material disclosure digest — RM: {rm} ({i}/{len(chunks)})\n\n" + ch
                print("---DRY---"); print(preview); print()
            total_chunks += len(chunks)
        print(f"[digest] dry_run=True (would have sent {total_chunks} message(s) across {len(by_rm)} RM(s))")
        return 0

    print(f"[digest] {len(rows)} unsent material item(s) grouped by {len(by_rm)} RM(s).")
    for rm in sorted(by_rm):
        chunks = format_digest(by_rm[rm])
        for i, ch in enumerate(chunks, 1):
            body = ch + "\n\n---\n📌 Champ — Issuer Department 1, SET"
            text = f"[SETSURV] 🟡 Material — {rm} ({i}/{len(chunks)})\n\n" + body
            last_msg_id = client.send(text)
            time.sleep(1.1)
        total_chunks += len(chunks)

    mark_sent(all_news_ids, tier="digest", channel=EMAIL_CHANNEL, message_id=last_msg_id)
    print(f"[digest] sent {total_chunks} chunk(s) across {len(by_rm)} RM(s) covering {len(rows)} item(s)")
    return len(rows)


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
