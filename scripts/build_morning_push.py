"""Send the morning brief push — one email, a personalized section per RM.

Runs in the daily build job AFTER the snapshot builders (fresh data/*.json
on disk). For each RM it assembles: movers beyond +/-2%, 52-week extremes,
high/medium unusual-trading alerts, disclosures filed in the last ~26h and
overdue/silent filers — then asks the Groq free tier for a 2-3 sentence
"AI take" per RM (skipped gracefully if GROQ_API_KEY is unset or the call
fails; the data sections always go out).

Delivery follows the route_alerts.py house style: everything goes to
EMAIL_TO via Gmail SMTP, sections labeled per RM. When per-RM addresses
exist later, set BRIEF_EMAIL_TO="Champ:a@x,Kae:b@y" to split delivery.

Env:
    EMAIL_USERNAME, EMAIL_APP_PASSWORD, EMAIL_FROM, EMAIL_TO   (send)
    BRIEF_EMAIL_TO   optional per-RM map "RM:addr,RM:addr" or extra addrs
    GROQ_API_KEY     optional, enables the per-RM AI take

CLI:
    build_morning_push.py --dry-run    # print the email, send nothing
    build_morning_push.py --rm Champ   # single-RM email (testing)
"""

import argparse
import json
import os
import smtplib
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = os.environ.get("AI_INSIGHTS_MODEL", "openai/gpt-oss-120b")
BKK = timezone(timedelta(hours=7))
MOVER_PCT = 2.0
RMS = ["Champ", "Kae", "Orn", "Gift", "Pim", "Tony"]


def _read(name):
    p = DATA / f"{name}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def rm_slices():
    """rm -> {movers, extremes, alerts, filings, overdue} from the snapshots."""
    tickers = _read("tickers") or {"tickers": []}
    brief = _read("morning-brief") or {"rows": []}
    unusual = _read("unusual-trading") or {"alerts": []}
    pulse = _read("disclosure-pulse") or {"filings": [], "status": []}

    rm_of = {t["tk"]: t["rm"] for t in tickers["tickers"]}
    cutoff = (datetime.now(BKK) - timedelta(hours=26)).isoformat()

    out = {rm: {"movers": [], "extremes": [], "alerts": [], "filings": [],
                "overdue": []} for rm in RMS}

    for r in brief["rows"]:
        rm = rm_of.get(r["tk"])
        if rm not in out:
            continue
        if r.get("pct1d") is not None and abs(r["pct1d"]) >= MOVER_PCT:
            out[rm]["movers"].append(r)
        if r.get("hi52") or r.get("lo52"):
            out[rm]["extremes"].append(r)

    for a in unusual["alerts"]:
        rm = rm_of.get(a["tk"])
        if rm in out and a.get("severity") in ("high", "medium"):
            out[rm]["alerts"].append(a)

    for f in pulse["filings"]:
        rm = rm_of.get(f["tk"])
        if rm in out and (f.get("ts") or "") >= cutoff:
            out[rm]["filings"].append(f)

    for s in pulse.get("status", []):
        rm = rm_of.get(s["tk"])
        if rm in out and s.get("overdue"):
            out[rm]["overdue"].append(s)

    return out, brief.get("asOf", "?")


def ai_takes(slices):
    """rm -> 2-3 sentence take via Groq. {} on any failure (never blocks)."""
    if not os.environ.get("GROQ_API_KEY"):
        print("GROQ_API_KEY unset — sending data sections without AI takes.")
        return {}
    digest = {}
    for rm, s in slices.items():
        digest[rm] = {
            "movers": [f"{r['tk']} {r['pct1d']:+}%" for r in s["movers"][:10]],
            "alerts": [f"{a['tk']} {a['type']} [{a['severity']}]" for a in s["alerts"][:8]],
            "filings": [f"{f['tk']}: {str(f['title'])[:60]}" for f in s["filings"][:8]],
            "overdue": [f"{o['tk']} silent {o['silentDays']}d" for o in s["overdue"][:5]],
        }
    body = json.dumps({
        "model": MODEL,
        "temperature": 0.2,
        "messages": [
            {"role": "system", "content":
                "You write the morning push for IS1, a Thai securities coverage "
                "team. Input: per-RM JSON of movers, alerts, filings, overdue "
                "filers (today's data, prices are previous close). For each RM "
                "with anything notable, write 2-3 plain-English sentences: what "
                "to look at first and why, connecting alerts to filings when the "
                "same ticker appears in both. Mention only tickers in the input, "
                "quote percentages exactly. Reply ONLY with JSON: "
                '{"takes": {"Champ": "...", "Kae": "..."}} — omit RMs with '
                "nothing notable."},
            {"role": "user", "content": json.dumps(digest, ensure_ascii=False)},
        ],
        "response_format": {"type": "json_object"},
    }).encode()
    req = urllib.request.Request(GROQ_URL, data=body, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
        "User-Agent": "is1-morning-push/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            reply = json.load(r)["choices"][0]["message"]["content"]
        return json.loads(reply).get("takes", {})
    except Exception as e:
        print(f"AI takes skipped ({e}) — sending data sections only.")
        return {}


def render(slices, takes, as_of, only_rm=None):
    lines = [f"IS1 Morning Brief — {as_of} (prices are previous close)", ""]
    for rm in RMS:
        if only_rm and rm != only_rm:
            continue
        s = slices[rm]
        if not any(s.values()):
            continue
        lines.append(f"━━ {rm} " + "━" * max(1, 30 - len(rm)))
        if takes.get(rm):
            lines.append(f"☀️ {takes[rm]}")
        if s["movers"]:
            mv = ", ".join(f"{r['tk']} {r['pct1d']:+}%"
                           for r in sorted(s["movers"], key=lambda r: r["pct1d"]))
            lines.append(f"• Movers ±{MOVER_PCT}%: {mv}")
        if s["extremes"]:
            ex = ", ".join(f"{r['tk']} {'52wHI' if r.get('hi52') else '52wLO'}"
                           for r in s["extremes"][:8])
            lines.append(f"• 52-week: {ex}")
        for a in s["alerts"][:6]:
            lines.append(f"• Alert [{a['severity']}]: {a['tk']} {a['type']} {a.get('label', '')}")
        for f in s["filings"][:6]:
            lines.append(f"• Filed: {f['tk']} — {str(f['title'])[:80]}")
        if s["overdue"]:
            od = ", ".join(f"{o['tk']} ({o['silentDays']}d)" for o in s["overdue"][:5])
            lines.append(f"• Silent/overdue: {od}")
        lines.append("")
    lines.append("---")
    lines.append("Ask the agents for detail: https://is1-coverage-dashboard.tasinpong-k.workers.dev")
    return "\n".join(lines)


def send(text, as_of):
    user = os.environ.get("EMAIL_USERNAME")
    pw = (os.environ.get("EMAIL_APP_PASSWORD") or "").replace(" ", "")
    if not (user and pw):
        sys.exit("EMAIL_USERNAME / EMAIL_APP_PASSWORD missing")
    from_addr = os.environ.get("EMAIL_FROM") or user
    to_addrs = [a.strip() for a in (os.environ.get("EMAIL_TO") or user).split(",")]
    extra = os.environ.get("BRIEF_EMAIL_TO", "")
    to_addrs += [p.split(":", 1)[-1].strip() for p in extra.split(",") if p.strip()]

    msg = MIMEText(text, "plain", "utf-8")
    msg["Subject"] = f"[SETSURV] ☀️ IS1 Morning Brief — {as_of}"
    msg["From"] = from_addr
    msg["To"] = ", ".join(dict.fromkeys(to_addrs))
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as s:
        s.starttls()
        s.login(user, pw)
        s.send_message(msg)
    print(f"sent morning brief to {msg['To']}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--rm", choices=RMS, help="single-RM brief (testing)")
    args = p.parse_args()

    slices, as_of = rm_slices()
    takes = ai_takes({args.rm: slices[args.rm]} if args.rm else slices)
    text = render(slices, takes, as_of, only_rm=args.rm)

    if args.dry_run:
        print(text)
        return 0
    send(text, as_of)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception as e:  # never fail the build over the push email
        print(f"morning push failed: {e}")
        sys.exit(0)
