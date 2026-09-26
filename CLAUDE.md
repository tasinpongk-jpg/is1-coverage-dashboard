# IS1 Coverage Dashboard — Project Context for Claude Code

> **Load this file on every Claude Code session in this repo.** It encodes
> the universe, the snapshot pipeline, the vault layout, and the hard-won
> pitfalls. Without it, every session re-discovers the same context.
>
> If anything below is wrong or stale, fix THIS file, not a session transcript.

---

## 1. What this repo is

A daily-refreshed dashboard for **232 Thai SET listed companies** in the
coverage universe of SET Issuer Department 1 (IS1). The dashboard is
**static HTML + JSON**, deployed to Cloudflare Pages, with a Cloudflare
Worker chat dock (`chat-dock.js` → `worker.js`) for grounded Q&A against
four named agents (Atlas, Hermes, Pythia, Lex).

Sector split (`sector` field in `data/tickers.json`, 232 entries, hand-curated):
PROP, FOOD, PF&REIT, CONS, CONMAT, AGRI. PF&REIT is its own sector, not part
of PROP. Count from the file when you need numbers; do not copy them here.

---

## 2. The 5 critical snapshots in `data/`

These drive every HTML page and the chat dock. If any is stale, the dashboard is lying.

| File | Source | HTML consumer | Builder | CI trigger? |
|---|---|---|---|---|
| `data/tickers.json` | hand-curated | All pages | `scripts/build_tickers.py` | manual |
| `data/disclosure-pulse.json` | SET surveillance R2 DB | `index.html`, `disclosure-pulse.html` | `scripts/build_daily.py` | daily.yml |
| `data/morning-brief.json` | SETSMART prices + TA engine | `index.html`, Discord push | `scripts/build_daily_brief.py` | daily.yml |
| `data/company-reports.json` | in-session LLM synthesis | `company-summary.html` hero | `scripts/build_company_reports.py` | manual |
| `data/vault-ticker-notes.json` | OneDrive Obsidian vault | `company-summary.html` drawer | `scripts/build_vault_ticker_notes.py` | workflow_dispatch only |
| `data/filing-summaries.json` | SET filing PDFs → MiniMax M3 (laptop cron) | home newsroom, `company-summary.html` drawer, `disclosure-pulse.html` | `scripts/enrich_filing.py --dashboard` | laptop cron only |

`filing-summaries.json` covers every coverage ticker, Critical + Material
filings only, financial statements skipped, MD&A kept. A bullet is published
only when every number in it is found in the filing's extracted text; scanned
PDFs (no text to check against) are held back. Like the vault snapshot it only
refreshes from the laptop: `scripts/enrich_filing_cron.py` runs it after the
Discord alert and pushes it when `IS1_FILING_SUMMARY_PUSH=1`.

**The single biggest drift risk is `vault-ticker-notes.json`** — it has no CI
trigger. It only rebuilds when someone runs the script locally on a laptop
that has the OneDrive vault. Current `generated` timestamp is in the JSON
itself; if it's >7 days old, the MD&A / Notes tabs on `company-summary.html`
are stale.

---

## 3. The vault layout (OneDrive)

```
~/OneDrive - The Stock Exchange of Thailand/Claude-Vault/
  Work-SET/
    Listed Company/
      1-Raw/01-Filings/
        MDA/<TICKER>/*.md           # 1066 files, 232 tickers
        FS-NOTES/<TICKER>/*.md      # 1064 files, 232 tickers
        calls/<TICKER>/*.md         # 176 transcripts
        filingSummary/<TICKER>/*.md # 70 m3 summaries
        bizProfile/<TICKER>/*.md    # 39 profiles
```

Set `VAULT_ROOT` env var if you need to override the default path. The
script `find_vault_root()` in `scripts/build_vault_ticker_notes.py` accepts:
- `DEFAULT_VAULT` = `~/OneDrive - The Stock Exchange of Thailand/Claude-Vault`
- `ALT_VAULT` = `~/Library/CloudStorage/OneDrive2-TheStockExchangeofThailand/Claude-Vault` (macOS)

---

## 4. Common commands

### Audit coverage (read-only, ~10s, no LLM)
```bash
echo "" | python -c "
import json, re
from pathlib import Path
REPO = Path.home() / 'projects/is1-coverage-dashboard'
VAULT = Path('C:/Users/Tasinpong/OneDrive - The Stock Exchange of Thailand/Claude-Vault/Work-SET/Listed Company')
MDA = VAULT / '1-Raw/01-Filings/MDA'
FS  = VAULT / '1-Raw/01-Filings/FS-NOTES'
tickers = {t['tk'] for t in json.load(open(REPO/'data/tickers.json'))['tickers']}
PR = re.compile(r'(20\d{2}(?:Q[1-4]|FY)|\d{4}Q[1-4]|\d{4}FY)')
def scan(base, tk):
    d = base / tk
    if not d.is_dir(): return (0, None)
    files = sorted(d.glob('*.md'))
    periods = [PR.search(f.stem).group(1) for f in files if PR.search(f.stem)]
    return (len(files), max(periods) if periods else None)
missing = [tk for tk in tickers if not (MDA/tk).is_dir() or not (FS/tk).is_dir()]
print(f'Universe: {len(tickers)} | Missing MDA-or-FS: {len(missing)} -> {missing[:10]}')
"
```

### Rebuild the vault snapshot (only if vault content has drifted)
```bash
cd ~/projects/is1-coverage-dashboard
python scripts/build_vault_ticker_notes.py
# Expect: "Wrote vault-ticker-notes.json: {'tickers': 232, 'calls': N, 'mda': N, 'fsNotes': N, ...}"
```

### Check freshness of all 5 critical snapshots
```bash
cd ~/projects/is1-coverage-dashboard
python scripts/check_snapshot_freshness.py
# 7d warn / 14d stale thresholds. Exit 0 if all fresh, 1 if any warn, 2 if any stale.
# When invoked via pipe (cron / no_agent), auto-quiet: only emits output on warn/stale.
```
The cron `is1-snapshot-freshness` (job `e178ed60c87a`, schedule `30 8 * * 1-5`)
runs this script at 08:30 BKK weekdays before market open and posts a Discord
alert to channel `1533468684784242778` (same channel as `is1-daily-brief`) only
when something is stale. The script is copied to `~/AppData/Local/hermes/scripts/`
(the scheduler's actual script directory, NOT `~/.hermes/scripts/`). The
**pre-commit hook** (`scripts/_pre_commit_hook.sh`, installed at
`.git/hooks/pre-commit`) auto-syncs any staged `scripts/*.py` whose basename
matches an already-deployed file. Edit the script in the repo, commit,
and the AppData copy updates automatically — no manual step.

### Commit + push (triggers Cloudflare Pages auto-deploy)
```bash
cd ~/projects/is1-coverage-dashboard
git add data/vault-ticker-notes.json
git commit -m "chore(data): rebuild vault ticker notes"
git pull --rebase origin main  # if remote moved
git push origin main
```

### Run the daily pipeline locally (mirror CI)
```bash
cd ~/projects/is1-coverage-dashboard
python scripts/build_daily.py
python scripts/build_daily_brief.py
```

---

## 5. Hard rules (read these before touching anything)

1. **Never invent data.** Every number must trace to a vault file, a JSON
   snapshot, a SET filing URL, or a documented script output. If you can't
   source it, write "not provided" — do NOT estimate.
2. **On the Windows laptop (Python 3.14 + MSYS bash), bare `python -c "..."`
   hangs silently with exit 0** because non-TTY stdin blocks. Use
   `echo "" | python -c "..."` or write a `.py` file and invoke it.
3. **Hermes agent harness only:** `execute_code` is blocked in cron mode, so
   cron work runs as standalone `.py` scripts via `terminal` or `cronjob.script`.
4. **Never commit `data/audit-*.md`.** Those are one-shot diagnostics.
5. **Period strings compare lexicographically.** `'2024Q3' < '2025FY' < '2026Q1'`
   is correct — do not reach for `datetime` parsing.
6. **`vault-ticker-notes.json` is the silent-staleness trap.** No CI
   trigger. Always check its `generated` field before trusting the
   `company-summary.html` drawer content.
7. **PFREIT bucket has no upstream parent / no Note 5 subsidiary table.**
   47 tickers. Filter out before any Note-5 / shareholder extraction. List
   at `C:/Users/Tasinpong/data/pfreit_exclude.json`.
8. **Filing alert cron (`is1-filing-alert`, id `0d496976df4a`) only posts
   `high` severity + RM C tickers.** A silent cron ≠ no filings.
9. **Model contract: MiniMax M3 for every LLM call in this repo.** Worker:
   Atlas, Hermes and Lex call MiniMax M3 (Lex adds deterministic local
   retrieval); Pythia is a deterministic calculator with no model call.
   Pipeline: the classifier fall-through, headline translation, AI insights,
   the morning push, the eval judge and feedback themes all use MiniMax M3
   (`scripts/minimax_chat.py` / `.mjs` for stdlib callers). Only secret
   needed: `MINIMAX_API_KEY`. Do not add a second provider without an
   explicit reason.

---

## 6. Subagent fan-out pattern (for Note 5 / shareholder extraction)

Hermes agent harness settings (tool names below are Hermes tools, not Claude
Code tools):
- 3 concurrent subagents max (`delegation.max_concurrent_children=3`)
- 15-22 tickers per subagent (~50 tool-call budget)
- Orchestrator pre-extracts sections via `terminal` (NOT `execute_code`),
  saves to `C:/Users/Tasinpong/data/sections/<TK>.txt`
- Each subagent reads sections via `read_file`, writes JSON output
- Recovery if subagent hits budget before write: parse the summary log at
  `C:/Users/Tasinpong/AppData/Local/hermes/cache/delegation/subagent-summary-N-*.txt`

---

## 7. When NOT to use Codex for IS1 work (Hermes harness)

Deterministic Python scans (audit, count, regex, glob) → use `terminal` with
inline `python`. Codex adds 100-200s sandbox startup vs ~10s of `python -c`.
Only delegate to Codex when the work involves writing >200 LOC of new logic
or non-trivial refactoring.

---

## 8. Key references

- `AGENT-TRAINING.md` — how the 4 chat-dock agents were trained
- `INTEGRATION.md` — how snapshots feed HTML pages
- `docs/harvest/` — Q2/2026 harvest pipeline
- `scripts/build_vault_ticker_notes.py` — the 5-bucket snapshot builder
- `~/.hermes/skills/is1-coverage-health/SKILL.md` — full diagnostic + rebuild skill

---

## 9. Definition of done (project-wide)

A change to this repo is "done" when:
1. The relevant `data/*.json` snapshot was rebuilt (if data-side change)
2. The HTML consumer was smoke-tested (open page, confirm field renders)
3. `git status --short data/` is clean OR shows only the intentional snapshot
4. `git log -1 -- <touched-file>` shows the new commit
5. If a rebuild script changed, the script was run end-to-end on local
6. The change is summarized in the commit message: which files, why,
   which JSON shape keys changed, which HTML page was verified

---

## 10. Windows laptop: filing-summary cron bootstrap

The `is1-filing-alert` cron (job `0d496976df4a`, `*/30 7-19 * * 1-5` BKK) runs
`enrich_filing_cron.py`: the RM C Discord alert, then the IS1-wide dashboard
summaries, then a push of `data/filing-summaries.json` to main.

| Variable | Needed for | Set via |
|---|---|---|
| `MINIMAX_API_KEY` | every summary | `setx MINIMAX_API_KEY <value>` |
| `DISCORD_WEBHOOK_URL` or `DAILY_BRIEF_WEBHOOK` | the Discord alert; either key works, env or `~/.hermes/secrets/*.env` | already in `daily_brief.env` |
| `IS1_FILING_SUMMARY_PUSH` | push to main; must be `1` | `setx IS1_FILING_SUMMARY_PUSH 1` |
| `IS1_REPO` | only if the repo is not at `C:\Users\Tasinpong\projects\is1-coverage-dashboard` | `setx IS1_REPO <path>` |

`setx` stores values in HKCU in plain text. Single-user laptop only.

**Fresh laptop, or the cron stopped committing:**
```bash
python scripts/bootstrap_cron.py   # installs the shim and pypdf, reports each variable as set/MISSING
python scripts/enrich_filing_cron.py --dry-run   # both steps, no Discord post, no commit
```

**Why the AppData file is a shim.** Hermes runs `enrich_filing_cron.py` from
`%LOCALAPPDATA%\hermes\scripts\`. The wrapper finds the repo from its own
location, so a plain copy there looks in the wrong folder. The AppData file is
`scripts/cron_shim.py`, which runs the repo's wrapper, so repo edits apply on the
next run. The pre-commit hook never copies `enrich_filing_cron.py` to AppData
(that would overwrite the shim) and syncs `cron_shim.py` into that name instead.

**Why the shim reads HKCU\Environment.** `setx` does not reach processes that are
already running, so the cron worker inherits the scheduler's old environment. The
shim fills in the variables above from the registry when they are missing.

**Why published summaries survive a cache loss.** The m3 cache
(`~/.hermes/cache/filing_summary.json`) is per machine. A publish keeps every
summary already in `data/filing-summaries.json` whose filing is still in the pulse
window and was written under the current `DASHBOARD_PROMPT_VERSION`, and an
alert `PROMPT_VERSION` bump clears only alert entries.
