# IS1 Coverage Dashboard — Project Context for Claude Code

> **Load this file on every Claude Code session in this repo.** It encodes
> the universe, the snapshot pipeline, the vault layout, and the hard-won
> pitfalls. Without it, every session re-discovers the same context.
>
> If anything below is wrong or stale, fix THIS file, not a session transcript.

---

## 1. What this repo is

A daily-refreshed dashboard for **232 Thai SET listed companies** under the IS1
broker's coverage universe. The dashboard is **static HTML + JSON**, deployed
to Cloudflare Pages, with a Cloudflare Worker chat dock (`chat-dock.js` →
`worker.js`) for grounded Q&A against four named agents (Atlas, Hermes, Pythia, Lex).

| Sector | Count (approx) |
|---|---|
| FOOD (F1-F10) | ~50 |
| PROP (P1-P5, includes PFREIT bucket) | ~80 |
| CONS (C1-C3) | ~30 |
| CONMAT (M1-M3) | ~30 |
| AGRI (A1-A2) | ~20 |
| Other | ~20 |

Full ticker list in `data/tickers.json` (232 entries, hand-curated).

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
2. **Never run `python -c "..."` from the terminal tool bare.** Python 3.14
   + MSYS bash non-TTY stdin hangs silently with exit 0. Always use
   `echo "" | python -c "..."` or write a `.py` file and invoke it.
3. **Never use `execute_code` for cron-mode work.** It's blocked there. Use
   standalone `.py` scripts invoked via `terminal` or `cronjob.script`.
4. **Never commit `data/audit-*.md`.** Those are one-shot diagnostics.
5. **Period strings compare lexicographically.** `'2024Q3' < '2025FY' < '2026Q1'`
   is correct — do not reach for `datetime` parsing.
6. **`vault-ticker-notes.json` is the silent-staleness trap.** No CI
   trigger. Always check its `generated` field before trusting the
   `company-summary.html` drawer content.
7. **One orphan dir as of 2026-08-08:** `MDA/CPALL/` exists but CPALL is
   not in IS1 universe. Pull it into coverage or delete it — not re-fixed
   in 2026-08-19 ship.
8. **PFREIT bucket has no upstream parent / no Note 5 subsidiary table.**
   47 tickers. Filter out before any Note-5 / shareholder extraction. List
   at `C:/Users/Tasinpong/data/pfreit_exclude.json`.
9. **Filing alert cron (`is1-filing-alert`, id `0d496976df4a`) only posts
   `high` severity + RM C tickers.** A silent cron ≠ no filings.
10. **Cloudflare Worker model contract: Hermes (MiniMax M3) only.** Pythia
    is deterministic; Lex is MiniMax M3 + local retrieval. Do not route
    any agent through a non-MiniMax provider without an explicit reason.

---

## 6. Subagent fan-out pattern (for Note 5 / shareholder extraction)

Proven working pattern from 2026-08-28 shareholder extraction:
- 3 concurrent subagents max (`delegation.max_concurrent_children=3`)
- 15-22 tickers per subagent (~50 tool-call budget)
- Orchestrator pre-extracts sections via `terminal` (NOT `execute_code`),
  saves to `C:/Users/Tasinpong/data/sections/<TK>.txt`
- Each subagent reads sections via `read_file`, writes JSON output
- Recovery if subagent hits budget before write: parse the summary log at
  `C:/Users/Tasinpong/AppData/Local/hermes/cache/delegation/subagent-summary-N-*.txt`

---

## 7. When NOT to use Codex for IS1 work

Deterministic Python scans (audit, count, regex, glob) → use `terminal` with
inline `python`. Codex adds 100-200s sandbox startup vs ~10s of `python -c`.
Only delegate to Codex when the work involves writing >200 LOC of new logic
or non-trivial refactoring.

---

## 8. Key references

- `CLAUDE-INSTRUCTIONS.md` — chat-template for the 6M26 deck project
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
