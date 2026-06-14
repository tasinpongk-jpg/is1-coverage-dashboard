#!/usr/bin/env python3
"""Clean up oppday-minutes.json data quality.

Two safe, non-destructive operations (we never rewrite narrative figures —
that risks introducing NEW errors; we annotate and strip hard garbage):

1. Strip stray CJK (Chinese/Japanese) runs that leaked in at generation time
   (e.g. SAPPE's Q&A drifted into hallucinated Chinese). Pure-CJK lines are
   dropped; mixed Thai/CJK lines keep the Thai.

2. Attach a `dataQuality` annotation to every summary, reusing the oppday-vs-
   filed-financials divergence flags that the company-report synthesis agents
   already produced (data/synthesis/out/<TK>.json -> qualityFlags). Severity:
     high  = garbled/corrupted/contradicts filings -> don't trust slide numbers
     med   = figures differ / need reconciliation
     low   = approximate / indicative / pending
     none  = no oppday concern found

Writes a .bak alongside the JSON before overwriting.

Usage:  python scripts/clean_oppday.py
"""
from __future__ import annotations

import glob
import json
import os
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OPP = REPO / "data" / "oppday-minutes.json"
SYNTH = REPO / "data" / "synthesis" / "out"

CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿豈-﫿]")
OPP_PAT = re.compile(r"opp\s*day|oppday|slide|transcript|presentation", re.I)

HIGH = re.compile(r"garbl|corrupt|unreliable|disregard|do not use|don't use|"
                  r"exclude|contradict|wrong|mismatch|hallucinat|mis-?name|"
                  r"mis-?label|\bOCR\b|\bASR\b|implausible|erroneous|not match", re.I)
MED = re.compile(r"reconcile|conflict|differ|inconsistent|verify|confirm|"
                 r"discrepancy|treat .*cautious|indicative only", re.I)
LOW = re.compile(r"approximate|indicative|rounded|placeholder|pending|stale|"
                 r"minor|machine-?(extracted|generated)|management figures", re.I)


def strip_cjk(content: str) -> tuple[str, int]:
    removed = 0
    out_lines = []
    for line in content.splitlines():
        if CJK.search(line):
            cleaned = CJK.sub("", line)
            # collapse leftover punctuation/space
            cleaned_stripped = re.sub(r"^[\s：:。，、（）()*#>\-\.]+$", "", cleaned.strip())
            removed += len(CJK.findall(line))
            if cleaned_stripped:
                out_lines.append(cleaned)          # mixed line: keep the non-CJK part
            # pure-CJK (or now-empty) line: drop entirely
        else:
            out_lines.append(line)
    # collapse 3+ blank lines left behind
    text = "\n".join(out_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text, removed


def severity(flag: str) -> str:
    if HIGH.search(flag):
        return "high"
    if MED.search(flag):
        return "med"
    if LOW.search(flag):
        return "low"
    return "med"  # it mentioned oppday + a concern; default to reconcile


def load_oppday_flags() -> dict[str, str]:
    flags: dict[str, str] = {}
    for f in glob.glob(str(SYNTH / "*.json")):
        tk = os.path.basename(f)[:-5]
        try:
            d = json.loads(Path(f).read_text(encoding="utf-8"))
        except Exception:
            continue
        hits = [q for q in (d.get("qualityFlags") or []) if OPP_PAT.search(q)]
        if hits:
            # prefer the most severe-sounding flag
            hits.sort(key=lambda q: (0 if HIGH.search(q) else 1 if MED.search(q) else 2))
            flags[tk] = hits[0]
    return flags


def main() -> None:
    original = OPP.read_text(encoding="utf-8")
    OPP.with_suffix(".json.bak").write_text(original, encoding="utf-8")  # original snapshot
    payload = json.loads(original)
    summaries = payload.get("summaries") or []
    flags = load_oppday_flags()

    stripped_tk, annotated, sev_counts = [], 0, {"high": 0, "med": 0, "low": 0, "none": 0}
    for s in summaries:
        tk = s.get("ticker")
        content = s.get("content") or ""
        if CJK.search(content):
            new_content, n = strip_cjk(content)
            s["content"] = new_content
            stripped_tk.append((tk, n))
        # also clean stray CJK from overview
        if CJK.search(s.get("overview") or ""):
            s["overview"], _ = strip_cjk(s["overview"])

        flag = flags.get(tk)
        if flag:
            sev = severity(flag)
            s["dataQuality"] = {"severity": sev, "note": flag.strip()}
            sev_counts[sev] += 1
            annotated += 1
        else:
            s["dataQuality"] = {"severity": "none",
                                "note": "No oppday/filing divergence detected in cross-check."}
            sev_counts["none"] += 1

    payload.setdefault("meta", {})["dataQualityPass"] = {
        "annotated": annotated,
        "cjkStripped": [t for t, _ in stripped_tk],
        "severity": sev_counts,
        "method": "reused company-report synthesis cross-check vs filed financials",
    }

    OPP.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"summaries: {len(summaries)}")
    print(f"CJK-stripped: {stripped_tk}")
    print(f"annotated with dataQuality: {annotated}")
    print(f"severity counts: {sev_counts}")


if __name__ == "__main__":
    main()
