# IS1 Coverage Dashboard — System Reference

This doc captures the full system state after the 2026-05-07 migration from
local Windows scheduled tasks to GitHub Actions cloud-autonomous flow.

**Treat this as the source of truth.** If you set up a new laptop, this
doc tells you exactly what's where and what to recreate.

---

## What this system does

A daily intelligence pipeline for 232 SET-listed tickers under the IS1 team's
coverage (FOOD, PROP, PFREIT, AGRI, CONS, CONMAT sectors):

1. **Polls** new SET disclosures from public news/search API
2. **Classifies** each disclosure as critical / material / routine / unclassified
   using a 112-pattern deterministic rules engine (~85% match rate). Rule-misses
   are persisted as `severity='unclassified'` (silent — no email, no dashboard
   alert) and queued for the offline rule-mining loop (`scripts/mine_rules.py`),
   which clusters them against historical LLM-labeled rows and promotes new
   patterns into `rules.py`. UPSERT semantics let promoted patterns auto-relabel
   previously-unclassified rows on the next CI run.
3. **Emails** two streams: critical alerts grouped by RM, material digest
   grouped by RM (routine + unclassified items stored only, not emailed)
4. **Builds** four JSON snapshots that drive the public dashboard (morning
   brief, sector heatmap, unusual trading, disclosure pulse)
5. **Updates** the local Obsidian vault notes with classified disclosures
   (laptop-on, daily 10:30 AM Bangkok)

**Cost:** Anthropic API $0 in steady state (down from $5–7/month before the
2026-05-25 cutover that removed Haiku fall-through). Offline rule-mining
subagent invocations are interactive-session token cost only, run on demand.
GitHub Actions free tier, Cloudflare Pages free tier, Cloudflare R2 free tier.

---

## Architecture (where everything lives)

```
                                    GitHub Actions
                            ┌──────────────────────────────┐
   02:15 UTC  ─── full ────►│  daily.yml (cron)            │
   (09:15 BKK)               │   ├─ surveillance job       │
                             │   │   poll → rules-only →   │
                             │   │   unclassified queue    │
                             │   │   email + R2 upload     │
                             │   └─ build job              │
                             │       JSONs + git push      │
                             └──────────────────────────────┘
                                    │           │
                                    ▼           ▼
                            ┌─────────────┐  ┌─────────────────┐
                            │ Cloudflare  │  │ GitHub repo     │
                            │ R2 bucket   │  │ tasinpongk-jpg/ │
                            │ setsmart-   │  │ is1-coverage-   │
                            │ data        │  │ dashboard       │
                            │ surveillance│  │ (Cloudflare     │
                            │ .duckdb     │  │  Pages auto-    │
                            └─────────────┘  │  deploys)       │
                                    │        └─────────────────┘
                                    │                │
   03:30 UTC  (laptop)              ▼                ▼
   (10:30 BKK)               ┌─────────────┐   ┌──────────┐
   IS1-Vault-Refresh ───────►│ rm_db/      │   │ Public   │
   (Windows task)            │ update_     │   │ dashboard│
                             │ vault.py    │   │ URL      │
                             │ → Obsidian  │   └──────────┘
                             └─────────────┘
```

---

## File locations (current laptop)

| Component | Path | Purpose |
|---|---|---|
| Dashboard repo | `C:\!VSCODE_Folder\SET_Coverage_Cloud\` | Canonical CI source. Contains workflow, vendored proxy, vendored surveillance |
| Original surveillance | `C:\!VSCODE_Folder\SET_SETSMART_API\surveillance\` | Stale copy; kept as a cache because `update_vault.py` writes the downloaded R2 DB here |
| Original proxy | `C:\!VSCODE_Folder\SETSMART_Proxy\` | Used by `SETSMART-Proxy` Windows task for interactive Claude MCP. |
| MCP server | `C:\!VSCODE_Folder\SET_SETSMART_API\set_mcp\` | Active — Claude Code uses this as the SET-data MCP |
| Vault tooling | `C:\!VSCODE_Folder\SET_SETSMART_API\rm_db\` | `update_vault.py`, `migrate_classifier_findings.py`, `scaffold_vault.py` |
| Obsidian vault | `C:\!VSCODE_Folder\SET_SETSMART_API\Claude-Vault\Work-SET\Listed Company\` | Local-only |
| venv | `C:\!VSCODE_Folder\SET_SETSMART_API\set_mcp\.venv\` | Python 3.11+ with anthropic, duckdb 1.5.2, boto3, etc. |

---

## Cloud schedule (GitHub Actions)

| Cron | Bangkok local | Emails sent |
|---|---|---|
| `15 2 * * 1-5` | 09:15 weekdays | critical + material digest |

Single morning run, full pipeline. Manual dispatch via `workflow_dispatch`
(no inputs) re-runs the same flow — critical alerts are idempotent against
`alerts_sent` so re-running is safe.

The 17:30 BKK afternoon cron was retired together with the coverage-feed
mode and Telegram channel during the 2026-05-09 simplification.

## Offline rule-mining loop (manual cadence)

The 2026-05-25 cutover removed Claude Haiku from the daily pipeline. New
disclosures the rules engine can't classify are tagged `unclassified` silently.
To harvest those into new patterns:

```powershell
# 1. Pull fresh DB from R2
$env:SURVEILLANCE_DB_PATH = "C:/Users/tasin/AppData/Local/Temp/surveillance_fresh.duckdb"
$env:AWS_ACCESS_KEY_ID = $env:R2_ACCESS_KEY_ID
$env:AWS_SECRET_ACCESS_KEY = $env:R2_SECRET_ACCESS_KEY
python surveillance/r2_sync.py download

# 2. Extract mining input (clusters labeled + unclassified rows)
python scripts/mine_rules.py
# -> writes scripts/rule_mining_input.json (gitignored)

# 3. Ask Elisa to dispatch the rule-mining subagent.
#    It reads rule_mining_input.json, edits surveillance/rules.py directly,
#    then validates via scripts/validate_rule_changes.py and returns a summary.

# 4. Review the diff, commit, push:
git diff surveillance/rules.py
git add surveillance/rules.py
git commit -m "perf(rules): mining pass #N — <description>"
git push origin main
```

Run cadence: when you notice ≥30 rows accumulating with `severity='unclassified'`
on the dashboard (typically every few weeks). The next daily CI run after a
push will auto-relabel previously-unclassified rows that the new patterns now
catch (UPSERT path in `classify_batch.py`).

## Active scheduled tasks (Windows)

Only the still-active local tasks are listed here. The pre-cloud Windows
tasks (`IS1-Coverage-Daily-Build`, `SET-Surveillance-Daily`) and the
`run_*.bat` files in `surveillance/` are gone — replaced by GitHub Actions.

| Task | Trigger | Purpose |
|---|---|---|
| `IS1-Vault-Refresh` | Daily 10:30 BKK | Pulls R2 DB → patches Obsidian (runs after morning CI). Skips silently if laptop is off. |
| `SETSMART-Proxy` | Login | `localhost:8765` FastAPI for interactive Claude MCP queries. |

---

## User-scope Windows env vars (must recreate on new laptop)

| Var | Value source | Used by |
|---|---|---|
| `MINIMAX_API_KEY` (or `ANTHROPIC_API_KEY` fallback) | console.minimax.io — your personal interactive key (Anthropic key works as fallback) | Local Claude Code, ad-hoc surveillance runs |
| `SETSMART_API_KEY` | SETSMART subscription | Local proxy + ad-hoc API calls |
| `SURVEILLANCE_SQL` | 490-char SQL JOIN (news_items + classifications) | Proxy disclosure-pulse route |
| `R2_ACCESS_KEY_ID` | Cloudflare R2 token | `update_vault.py` |
| `R2_SECRET_ACCESS_KEY` | Cloudflare R2 token | `update_vault.py` |
| `R2_ENDPOINT` | `https://7c2b01e43fdb4ecfb6e578ace9bd3adc.r2.cloudflarestorage.com` | `update_vault.py` |
| `R2_BUCKET` | `setsmart-data` | `update_vault.py` |

**To export from current laptop:**
```powershell
foreach ($n in 'MINIMAX_API_KEY','ANTHROPIC_API_KEY','SETSMART_API_KEY','SURVEILLANCE_SQL',
               'R2_ACCESS_KEY_ID','R2_SECRET_ACCESS_KEY','R2_ENDPOINT','R2_BUCKET') {
    $v = [Environment]::GetEnvironmentVariable($n,'User')
    if ($v) { Write-Output "$n=$v" } else { Write-Output "$n=<UNSET>" }
} | Out-File -Encoding utf8 "$HOME\Desktop\is1-env-vars-DO-NOT-COMMIT.txt"
```

The output file is sensitive — copy via secure means, then delete.

---

## GitHub Secrets (already in cloud — automatically present)

These are stored in the repo's GitHub Actions secrets (encrypted at rest by GitHub).
They follow the repo, NOT the laptop. You do not need to recreate them on a new laptop.

```
MINIMAX_API_KEY         EMAIL_APP_PASSWORD    EMAIL_FROM
EMAIL_TO              EMAIL_USERNAME        R2_ACCESS_KEY_ID
R2_BUCKET             R2_ENDPOINT           R2_SECRET_ACCESS_KEY
SETSMART_API_KEY      SURVEILLANCE_SQL
```

---

## New-laptop bootstrap

```powershell
# 0. Install prerequisites
#    - Git for Windows
#    - Python 3.11+
#    - GitHub CLI (gh)
#    - Obsidian
#    - VS Code (optional)

# 1. Clone the canonical repo
git clone https://github.com/tasinpongk-jpg/is1-coverage-dashboard.git C:\!VSCODE_Folder\SET_Coverage_Cloud
cd C:\!VSCODE_Folder\SET_Coverage_Cloud

# 2. Clone the original surveillance project (for set_mcp + rm_db + Obsidian vault tools)
git clone <wherever-it-lives> C:\!VSCODE_Folder\SET_SETSMART_API
# If never on GitHub: copy the folder via OneDrive/external drive

# 3. Create the venv
cd C:\!VSCODE_Folder\SET_SETSMART_API\set_mcp
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install anthropic boto3 duckdb fastapi httpx pydantic uvicorn python-dotenv

# 4. Restore user env vars (from the file you exported above)
#    For each line K=V: [Environment]::SetEnvironmentVariable('K', 'V', 'User')

# 5. Re-register the local Windows tasks
#    - IS1-Vault-Refresh:  see scripts/register_vault_refresh.ps1 (TODO: write this)
#    - SETSMART-Proxy:     see SETSMART_Proxy/start_proxy.ps1
#    Both reference paths under C:\!VSCODE_Folder\

# 6. Copy Obsidian vault contents
#    OneDrive sync, manual copy, or Obsidian Sync — whichever path you use

# 7. Verify
gh auth login
gh run list --repo tasinpongk-jpg/is1-coverage-dashboard --workflow daily.yml --limit 3
.\set_mcp\.venv\Scripts\python.exe rm_db\update_vault.py    # should download + patch
```

---

## Debug pointers

- **CI workflow status:** https://github.com/tasinpongk-jpg/is1-coverage-dashboard/actions
- **Public dashboard:** https://is1-coverage-dashboard.tasinpong-k.workers.dev/
  (the old `cloudflare-workers-autoconfig-…` worker is an orphaned first-setup
  deploy that CI never updates — delete it in the Cloudflare dash when convenient)
- **R2 console:** https://dash.cloudflare.com → R2 → setsmart-data
- **Local logs:**
  - Vault refresh: `surveillance/logs/vault_refresh_YYYYMMDD.log`
  - Old build (disabled): `logs/deploy-YYYYMMDD.log`

## Two known gotchas (recorded for future-you)

1. `duckdb` version pin in CI must match the writer's local version. Both
   are pinned at 1.4.4; if you upgrade locally, bump CI requirements too,
   or `_open_surveillance_db` silently fails and disclosure-pulse falls
   back to live mode (returns empty).

2. When using `gh secret set` to set GitHub Actions secrets, NEVER use
   `--body -`. That sets the value to literal `-`, not "read from stdin".
   Use `--body "value"` or pipe via stdin without the `--body` flag.
