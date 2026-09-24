"""Build data/ai-insights.json — AI analyst commentary over today's snapshots.

Runs in the daily build job AFTER the snapshot builders, so it reads the
fresh data/*.json from disk, condenses them into a compact digest, and asks
MiniMax M3 for a structured morning commentary: headline, market take,
sector notes, watchlist and risk flags.

Pure stdlib. Skips gracefully (keeps yesterday's file) when MINIMAX_API_KEY is
unset or the API call fails — the dashboard page tolerates a stale file.

Env:
    MINIMAX_API_KEY     required to actually generate (otherwise skip + exit 0)
    MINIMAX_MODEL       override model (default MiniMax-M3)
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
OUT = DATA / "ai-insights.json"

import minimax_chat

SYSTEM_PROMPT = (
    "You are the morning analyst for IS1, Issuer Department 1 of the Stock "
    "Exchange of Thailand, whose RMs cover 232 SET tickers (FOOD, PROP, PF&REIT, "
    "AGRI, CONS, CONMAT). RMs: C, K, O, G, P, T. You receive a digest of "
    "today's coverage data: price moves, volume, unusual-trading alerts and "
    "disclosure filings. Write a concise, factual morning commentary an RM can "
    "skim in 60 seconds at the start of the day.\n"
    "Rules: only reference tickers and numbers present in the digest — never "
    "invent data. Quote percentages exactly as given. Connect alerts to filings "
    "when both exist for the same ticker. Plain professional English.\n"
    "Respond with ONLY a JSON object, no markdown fences, in this shape:\n"
    "{\n"
    '  "headline": "one sentence, the single most important thing today",\n'
    '  "market_take": "2-4 sentences on the overall coverage picture",\n'
    '  "sector_notes": [{"sector": "FOOD", "note": "1-2 sentences"}],\n'
    '  "watchlist": [{"tk": "ABC", "rm": "C", "reason": "1 sentence"}],\n'
    '  "risk_flags": ["short sentence per flag"]\n'
    "}\n"
    "sector_notes: only sectors with something worth saying (max 6). "
    "watchlist: max 8 names, ordered by urgency. risk_flags: max 5."
)


def _read(name):
    return json.loads((DATA / f"{name}.json").read_text(encoding="utf-8"))


def build_digest():
    """Condense today's snapshots into a compact text digest for the model."""
    tickers = {t["tk"]: t for t in _read("tickers")["tickers"]}
    brief = _read("morning-brief")
    unusual = _read("unusual-trading")
    pulse = _read("disclosure-pulse")

    def rm(tk):
        # Anonymise RM to its initial (privacy), defensively — even if
        # tickers.json ever regresses to full names upstream.
        r = tickers.get(tk, {}).get("rm", "?")
        return str(r).strip()[:1].upper() if r not in (None, "", "?") else r

    def sector(tk):
        return tickers.get(tk, {}).get("sector", "?")

    lines = [f"AS-OF: {brief.get('asOf')} (prices are previous close)"]

    rows = [r for r in brief["rows"] if r.get("pct1d") is not None]
    movers = sorted(rows, key=lambda r: abs(r["pct1d"]), reverse=True)[:15]
    lines.append("\nTOP MOVERS (tk sector rm last pct1d volRatio):")
    for r in movers:
        lines.append(f"  {r['tk']} {sector(r['tk'])} {rm(r['tk'])} "
                     f"{r['last']} {r['pct1d']:+.2f}% vol×{r.get('volRatio')}")

    week = sorted(rows, key=lambda r: abs(r.get("pct5d") or 0), reverse=True)[:8]
    lines.append("\nBIGGEST 5-DAY MOVES (tk pct5d):")
    lines.append("  " + ", ".join(
        f"{r['tk']} {r['pct5d']:+.1f}%" for r in week if r.get("pct5d")))

    alerts = unusual.get("alerts", [])
    high = [a for a in alerts if a.get("severity") == "high"][:20]
    lines.append(f"\nUNUSUAL-TRADING ALERTS ({len(alerts)} total, "
                 f"{len(high)} high shown):")
    for a in high:
        lines.append(f"  {a['tk']} {a['sector']} {rm(a['tk'])}: "
                     f"{a['type']} {a['label']}")

    sev_rank = {"high": 0, "medium": 1}
    filings = [f for f in pulse.get("filings", [])
               if f.get("severity") in sev_rank]
    filings.sort(key=lambda f: (f["ts"], -sev_rank[f["severity"]]),
                 reverse=True)
    lines.append("\nRECENT NOTABLE FILINGS (newest first, max 20):")
    for f in filings[:20]:
        lines.append(f"  {f['ts'][:10]} {f['tk']} {f['sector']} {rm(f['tk'])} "
                     f"[{f['severity']}] {f['type']}: {f['title'][:100]}")

    silent = sorted((s for s in pulse.get("status", []) if s.get("overdue")),
                    key=lambda s: -s.get("silentDays", 0))[:8]
    if silent:
        lines.append("\nOVERDUE / LONG-SILENT TICKERS:")
        for s in silent:
            lines.append(f"  {s['tk']} {s['sector']} {rm(s['tk'])}: "
                         f"silent {s['silentDays']}d, overdue {s['overdue']}")

    return brief.get("asOf"), "\n".join(lines)


def call_model(digest):
    # parse_insights strips markdown fences, so no strict JSON mode is needed.
    return minimax_chat.chat(SYSTEM_PROMPT, digest, max_tokens=6000, temperature=0.2)


def parse_insights(raw):
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("```")[1].removeprefix("json").strip()
    data = json.loads(text)
    for key in ("headline", "market_take", "sector_notes",
                "watchlist", "risk_flags"):
        if key not in data:
            raise ValueError(f"model response missing {key!r}")
    return data


def main():
    if not minimax_chat.available():
        print("MINIMAX_API_KEY not set — skipping AI insights (keeping last file).")
        return
    as_of, digest = build_digest()
    print(f"digest: {len(digest)} chars, asOf {as_of}")
    try:
        insights = parse_insights(call_model(digest))
    except (ValueError, json.JSONDecodeError) as e:
        print(f"unparseable model output ({e}), retrying once...")
        insights = parse_insights(call_model(digest))
    insights = {
        "asOf": as_of,
        "model": minimax_chat.MODEL,
        "_built_at": datetime.now(timezone.utc).isoformat(),
        **insights,
    }
    OUT.write_text(json.dumps(insights, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(f"wrote {OUT.name}: {insights['headline']!r}, "
          f"{len(insights['sector_notes'])} sector notes, "
          f"{len(insights['watchlist'])} watchlist, "
          f"{len(insights['risk_flags'])} risk flags")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Never fail the build over commentary — the page tolerates stale data.
        print(f"AI insights failed (non-fatal): {e}", file=sys.stderr)
        sys.exit(0)
