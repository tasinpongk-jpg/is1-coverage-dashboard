"""CLI for sending alerts.

Modes:
  --mode critical        send each unsent critical disclosure as its own message
  --mode digest          send one combined digest of unsent material disclosures
  --mode both            run critical first, then digest (used by the scheduler)
  --mode coverage-feed   daily 'all news' summary — every classified item from
                         the past --hours-back, grouped by ticker, regardless of
                         whether it was already alerted in critical or digest.
                         NOT idempotent — run once per day from the scheduler.

  --dry-run              print messages, do not actually send
  --max N                cap critical messages per run (default 5)
  --hours-back N         lookback window for coverage-feed mode (default 24)
"""

from __future__ import annotations

import argparse
import time

from alerts import (
    CHANNEL,
    EMAIL_CHANNEL,
    EmailClient,
    TelegramClient,
    fetch_recent_classified,
    fetch_unsent,
    format_coverage_feed,
    format_critical,
    format_critical_digest,
    format_digest,
    mark_all_unsent_as_sent,
    mark_sent,
)


def _client_for(channel: str):
    if channel == "telegram":
        return TelegramClient()
    if channel == "email":
        return EmailClient()
    raise ValueError(f"unknown channel {channel!r}")


def _send_critical(client, max_send: int, dry_run: bool, since: str | None, channel: str) -> int:
    rows = fetch_unsent("critical", channel=channel, since=since)
    if not rows:
        print("[critical] nothing to send.")
        return 0

    rows_to_send = rows[:max_send]
    print(f"[critical] {len(rows)} unsent (will batch up to {max_send} this run, channel={channel}).")

    # BATCH MODE: format as digest grouped by RM instead of one email per disclosure
    chunks = format_critical_digest(rows_to_send)

    if dry_run:
        for i, ch in enumerate(chunks, 1):
            print("---DRY---"); print(ch); print()
        print(f"[critical] dry_run={dry_run} (would have sent {len(chunks)} batched message(s))")
        return 0

    last_msg_id = "0"
    for i, ch in enumerate(chunks, 1):
        body = ch + "\n\n---\n📌 Champ — Issuer Department 1, SET"
        text = (
            f"[SETSURV] 🔴 Critical disclosures batch ({i}/{len(chunks)})\n\n" + body
            if channel == "email"
            else ch
        )
        last_msg_id = client.send(text, priority="high") if client else "0"
        time.sleep(1.1)  # polite throttle

    mark_sent([r["news_id"] for r in rows_to_send], tier="critical", channel=channel, message_id=last_msg_id)
    print(f"[critical] sent {len(chunks)} batched message(s) covering {len(rows_to_send)} item(s)")
    return len(rows_to_send)


def _send_coverage_feed(client, dry_run: bool, hours_back: int, channel: str) -> int:
    rows = fetch_recent_classified(hours_back=hours_back)
    chunks = format_coverage_feed(rows, hours_back=hours_back)
    print(f"[coverage-feed] {len(rows)} classified item(s) in past {hours_back}h "
          f"-> {len(chunks)} chunk(s) (channel={channel}).")
    if dry_run:
        for ch in chunks:
            print("---DRY---"); print(ch); print()
        return 0

    for i, ch in enumerate(chunks, 1):
        text = (
            f"[SETSURV] 📰 Daily coverage feed ({i}/{len(chunks)})\n\n" + ch
            if channel == "email"
            else ch
        )
        client.send(text)
        time.sleep(1.1)
    print(f"[coverage-feed] sent {len(chunks)} chunk(s) covering {len(rows)} item(s)")
    return len(rows)


def _send_digest(client, dry_run: bool, since: str | None, channel: str) -> int:
    rows = fetch_unsent("material", channel=channel, since=since)
    if not rows:
        print("[digest] nothing to send.")
        return 0

    # Import RM lookup for grouping
    from alerts import _rm_lookup
    rm_map = _rm_lookup()

    # Group by RM, then format digest for each RM
    from collections import defaultdict
    by_rm = defaultdict(list)
    for r in rows:
        rm = rm_map.get(r["symbol"], "Unassigned")
        by_rm[rm].append(r)

    total_chunks = 0
    all_news_ids = [r["news_id"] for r in rows]
    last_msg_id = "0"

    if dry_run:
        for rm in sorted(by_rm.keys()):
            rm_rows = by_rm[rm]
            chunks = format_digest(rm_rows)
            for i, ch in enumerate(chunks, 1):
                preview = f"[SETSURV] 🟡 Material disclosure digest — RM: {rm} ({i}/{len(chunks)})\n\n" + ch if channel == "email" else ch
                print("---DRY---"); print(preview); print()
            total_chunks += len(chunks)
        print(f"[digest] dry_run={dry_run} (would have sent {total_chunks} message(s) across {len(by_rm)} RM(s))")
        return 0

    print(f"[digest] {len(rows)} unsent material item(s) grouped by {len(by_rm)} RM(s) (channel={channel}).")
    for rm in sorted(by_rm.keys()):
        rm_rows = by_rm[rm]
        chunks = format_digest(rm_rows)

        for i, ch in enumerate(chunks, 1):
            body = ch + "\n\n---\n📌 Champ — Issuer Department 1, SET"
            # On email: include RM in subject and add numeric suffix for threading
            text = f"[SETSURV] 🟡 Material — {rm} ({i}/{len(chunks)})\n\n" + body if channel == "email" else ch
            last_msg_id = client.send(text)
            time.sleep(1.1)
        total_chunks += len(chunks)

    mark_sent(all_news_ids, tier="digest", channel=channel, message_id=last_msg_id)
    print(f"[digest] sent {total_chunks} chunk(s) across {len(by_rm)} RM(s) covering {len(rows)} item(s)")
    return len(rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--mode", choices=["critical", "digest", "both", "coverage-feed"], default="both")
    p.add_argument("--hours-back", type=int, default=24,
                   help="Coverage-feed lookback window in hours (default 24).")
    p.add_argument("--channel", choices=["email", "telegram"], default="email",
                   help="Alert channel (default email).")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--max", type=int, default=5,
                   help="Cap critical messages per run (default 5; raise for batch sends).")
    p.add_argument("--since",
                   help="Only alert on disclosures dated on/after YYYY-MM-DD (defends against floods).")
    p.add_argument("--mark-only", action="store_true",
                   help="One-time cutover: mark every unsent classified item as already sent "
                        "(no actual messages sent). Run this once per channel after wiring it "
                        "up so the historical backlog doesn't flood you.")
    args = p.parse_args()

    if args.mark_only:
        counts = mark_all_unsent_as_sent(channel=args.channel)
        print(f"[mark-only] marked as sent without alerting on channel={args.channel}: {counts}")
        return

    client = None if args.dry_run else _client_for(args.channel)

    started = time.monotonic()
    sent_crit = sent_dig = sent_feed = 0
    if args.mode in ("critical", "both"):
        sent_crit = _send_critical(client, args.max, args.dry_run, args.since, args.channel)
    if args.mode in ("digest", "both"):
        sent_dig = _send_digest(client, args.dry_run, args.since, args.channel)
    if args.mode == "coverage-feed":
        sent_feed = _send_coverage_feed(client, args.dry_run, args.hours_back, args.channel)

    elapsed = time.monotonic() - started
    print(f"\n=== route_alerts done in {elapsed:.1f}s "
          f"(channel={args.channel}, dry_run={args.dry_run})  "
          f"critical_sent={sent_crit}  digest_items={sent_dig}  feed_items={sent_feed} ===")


if __name__ == "__main__":
    main()
