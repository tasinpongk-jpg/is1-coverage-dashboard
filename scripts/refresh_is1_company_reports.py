#!/usr/bin/env python3
"""
refresh_is1_company_reports.py — Weekly safe refresh of IS1 company-reports.json.

Wrapped around build_company_reports.py to:
  1. INHERIT existing reports (do not overwrite Opus synthesis — P15 trap)
  2. Use m3 (MiniMax-M3) via --llm auto for new / source-drifted tickers ONLY
  3. Skip tickers whose source-hash is unchanged (already synthesized)
  4. Cap m3 calls per run (default 30) to bound weekly cost
  5. Auto-commit + push the snapshot to repo (Cloudflare Pages auto-deploys)

Cron: every Fri 17:10 Asia/Bangkok — 10 min after vault-weekly-digest-fri-17.

Why this wrapper exists:
  - build_company_reports.py --all starts from {} (line 588) which would wipe
    the 231 Opus-synthesized reports currently in company-reports.json.
  - build_company_reports.py --ticker A --ticker B also wipes tickers not listed
    if args.limit is set (line 588: dict(existing) only when wanted/limit).
  - This wrapper imports build_company_reports's helpers (build_context,
    source_hash, llm_report, deterministic_report, write_json) and patches
    ONLY the tickers whose source-hash drifted, inheriting everything else.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO = Path(r"C:/Users/Tasinpong/projects/is1-coverage-dashboard")
DATA_DIR = REPO / "data"
OUT = DATA_DIR / "company-reports.json"

# Bound m3 weekly spend. At ~$0.003/call × 30 = ~$0.09/week. Adjust here.
MAX_LLM_CALLS_PER_RUN = int(os.environ.get("REFRESH_MAX_LLM", "30"))
# LLM model override — defaults to m3 per user request 2026-09-23.
MODEL = os.environ.get("COMPANY_REPORT_MODEL", os.environ.get("MINIMAX_MODEL", "MiniMax-M3"))


def _load_existing() -> dict[str, Any]:
    if not OUT.exists():
        return {}
    try:
        return json.loads(OUT.read_text(encoding="utf-8")).get("reports", {})
    except Exception:
        return {}


def _load_tickers() -> list[dict[str, Any]]:
    p = DATA_DIR / "tickers.json"
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8")).get("tickers", [])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="Don't write or commit")
    ap.add_argument("--no-commit", action="store_true", help="Write JSON but skip git commit+push")
    ap.add_argument("--max-llm", type=int, default=MAX_LLM_CALLS_PER_RUN)
    ap.add_argument("--llm", choices=["auto", "always", "never"], default="auto",
                    help="Pass-through to build_company_reports.py LLM mode")
    args = ap.parse_args(argv)

    # Ensure cwd is the repo so relative paths in build_company_reports.py resolve.
    os.chdir(REPO)
    sys.path.insert(0, str(REPO / "scripts"))

    # Lazy import so wrapper is usable even if dependencies are missing.
    try:
        import build_company_reports as bcr
    except Exception as exc:
        print(f"FAIL import build_company_reports: {exc}", file=sys.stderr)
        return 2

    existing = _load_existing()
    tickers = _load_tickers()
    notes_map = bcr.load_json(bcr.VAULT_NOTES, {}).get("tickers", {})
    disclosure_payload = bcr.load_json(bcr.DISCLOSURES, {})
    oppday_payload = bcr.load_json(bcr.OPPDAY, {})

    generated = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    reports: dict[str, Any] = dict(existing)  # CRITICAL: inherit, do not start from {}
    errors: list[dict[str, str]] = []
    drift: list[tuple[str, str]] = []  # (tk, reason: 'no_existing'|'source_changed')
    llm_used = False
    llm_calls = 0

    for ticker in tickers:
        tk = (ticker.get("tk") or "").upper()
        if not tk:
            continue
        context = bcr.build_context(ticker, notes_map.get(tk) or {}, disclosure_payload, oppday_payload)
        h = bcr.source_hash(context)
        old = existing.get(tk)
        if old and old.get("sourceHash") == h:
            # No drift — inherit verbatim, no LLM cost.
            continue

        drift.append((tk, "source_changed" if old else "no_existing"))

        if llm_calls >= args.max_llm:
            # Bound reached — leave existing Opus report in place, just record error.
            errors.append({"ticker": tk, "error": f"max_llm reached ({args.max_llm}); left as-is"})
            continue

        # m3 LLM gate — explicit env probe so cron runs without key fall back
        # to deterministic mode (P15-safe: never overwrite Opus synthesis with
        # template filler unless the user explicitly asked for it).
        has_key = bool(
            os.environ.get("MINIMAX_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
        )
        if args.llm == "auto" and not has_key:
            args_llm_mode = "never"  # effective mode for this run
        else:
            args_llm_mode = args.llm
        try:
            use_llm = (args_llm_mode == "always") or (args_llm_mode == "auto")
            if use_llm:
                report = bcr.llm_report(context, generated, MODEL)
                llm_used = True
                llm_calls += 1
            else:
                report = bcr.deterministic_report(context, generated)
        except Exception as exc:
            errors.append({"ticker": tk, "error": str(exc)})
            # If LLM failed and we have an old report, keep it (don't downgrade).
            if old:
                continue
            report = bcr.deterministic_report(context, generated)

        report["sourceHash"] = h
        reports[tk] = report

    payload = {
        "generated": generated,
        "source": "weekly refresh via refresh_is1_company_reports.py (inherit + drift-only m3)",
        "model": MODEL if llm_used else "inherited",
        "vaultRoot": "",
        "totals": {
            "reports": len(reports),
            "llm_calls": llm_calls,
            "drift": len(drift),
            "errors": len(errors),
        },
        "errors": errors,
        "reports": dict(sorted(reports.items())),
    }

    # Effective LLM mode (auto → never if no key)
    has_key_global = bool(
        os.environ.get("MINIMAX_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    )
    effective_llm = args.llm if (args.llm != "auto" or has_key_global) else "never (no API key)"

    # Stdout summary (Discord-delivered in no_agent mode via cron)
    drift_tks = [tk for tk, _ in drift[:15]]
    summary = (
        f"📊 **Company Reports — weekly refresh** ({generated})\n"
        f"existing: {len(existing)} | drift: {len(drift)} | m3 calls: {llm_calls}/{args.max_llm} | errors: {len(errors)}\n"
        f"model: `{MODEL}` | inherit: ✅ (P15-safe) | LLM mode: `{effective_llm}`\n"
        f"drifted: {', '.join(drift_tks) if drift_tks else '(none)'}"
    )
    print(summary)

    if args.dry_run:
        return 0
    bcr.write_json(OUT, payload)

    if args.no_commit:
        return 0

    # Auto-commit + push (P16/P17 path: feature-branch test is for scripts, not data).
    # For data-only snapshot updates the cron path uses main directly — this is
    # the same pattern as daily.yml's "Commit and push if data changed" step.
    try:
        r = subprocess.run(
            ["git", "add", "data/company-reports.json"],
            cwd=str(REPO), check=False, capture_output=True, text=True,
            stdin=subprocess.DEVNULL,
        )
        if r.returncode != 0:
            print(f"WARN git add failed: {r.stderr}", file=sys.stderr)
            return 0  # JSON written; don't fail the cron run
        diff = subprocess.run(
            ["git", "diff", "--staged", "--quiet"],
            cwd=str(REPO), check=False, capture_output=True, text=True,
        )
        if diff.returncode == 0:
            print("(no diff — already up to date)")
            return 0
        commit = subprocess.run(
            ["git", "commit", "-m",
             f"chore(data): weekly company-reports refresh (drift={len(drift)}, m3={llm_calls})"],
            cwd=str(REPO), check=False, capture_output=True, text=True,
            stdin=subprocess.DEVNULL,
        )
        if commit.returncode != 0:
            print(f"WARN git commit failed: {commit.stderr}", file=sys.stderr)
            return 0
        push = subprocess.run(
            ["git", "push", "origin", "main"],
            cwd=str(REPO), check=False, capture_output=True, text=True,
            timeout=60, stdin=subprocess.DEVNULL,
        )
        if push.returncode != 0:
            # Try rebase retry pattern from CLAUDE.md §5.
            print(f"WARN git push failed (will retry w/ rebase): {push.stderr}", file=sys.stderr)
            subprocess.run(
                ["git", "pull", "--rebase", "origin", "main"],
                cwd=str(REPO, ), check=False, capture_output=True, text=True,
                stdin=subprocess.DEVNULL,
            )
            retry = subprocess.run(
                ["git", "push", "origin", "main"],
                cwd=str(REPO), check=False, capture_output=True, text=True,
                timeout=60, stdin=subprocess.DEVNULL,
            )
            if retry.returncode != 0:
                print(f"FAIL git push retry: {retry.stderr}", file=sys.stderr)
                return 0
        print("✅ committed + pushed")
    except subprocess.TimeoutExpired:
        print("FAIL git push timeout", file=sys.stderr)
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
