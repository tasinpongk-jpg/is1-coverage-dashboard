# IS1 Vault Coverage Audit — MD&A + FS-NOTES

**Generated:** 2026-08-08
**Universe source:** `data/tickers.json` — 232 tickers under IS1 coverage (FOOD, PROP, PFREIT, AGRI, CONS, CONMAT)
**Vault root:** `C:/Users/Tasinpong/OneDrive - The Stock Exchange of Thailand/Claude-Vault/Work-SET/Listed Company`
**Audit method:** Python `pathlib` scan + regex period extraction from filenames. Read-only. No file modifications.

## Headline result

| Metric | Count | Note |
|---|---:|---|
| Universe tickers | 232 | All under IS1 RM coverage |
| Tickers with **MD&A** folder | 232 | 100% — every ticker dir present |
| Tickers with **FS-NOTES** folder | 232 | 100% — every ticker dir present |
| Tickers **missing** MD&A | **0** | None |
| Tickers **missing** FS-NOTES | **0** | None |
| MDA files total | 1066 | avg 4.6 per ticker |
| FS-NOTES files total | 1064 | avg 4.6 per ticker |
| MDA current (latest ≥ 2025Q3) | 232 | **100% recency** |
| MDA stale (2025Q1–2025Q2) | 0 | None |
| MDA very stale (≤ 2024FY) | 0 | None |
| Orphan vault dirs (in vault, not in universe) | 1 | `CPALL` only — IS1 does not cover it |

**No gaps.** Every ticker in the IS1 universe has current-period MD&A and FS-NOTES markdown in the Obsidian vault, and the dashboard pipeline that surfaces them (`scripts/build_vault_ticker_notes.py` → `data/vault-ticker-notes.json` → `company-summary.html`) is wired and working.

## Depth distribution (file count per ticker)

| Files per ticker | MDA | FS-NOTES |
|---|---:|---:|
| ≥ 10 files | 44 | 41 |
| ≥ 5 files | 204 | 201 |
| ≥ 3 files | 209 | 205 |
| 1–2 files | 23 | 27 |
| 0 files | 0 | 0 |

A handful of recently-onboarded tickers have only 1–2 historical notes; the rest carry 3+ quarters/years of MD&A + FS analysis.

## What was checked

```text
MDA/<TICKER>/MDA_<TICKER>_<PERIOD>_[E|T].md
FS-NOTES/<TICKER>/NOTES_<TICKER>_<PERIOD>_[E|T].md
```

Period regex: `(20\d{2}(?:Q[1-4]|FY)|\d{4}Q[1-4]|\d{4}FY)` — matches `2024Q3`, `2025FY`, `2026Q1`, etc.

## Pipeline state — all green

| Stage | Status | Evidence |
|---|---|---|
| Vault write (m3 filing summaries) | ✓ Live | Commit `0c81806 feat(rm-c): persist m3 filing summaries to Obsidian vault (Loop 4 v4)` |
| Vault write (raw filings as MD) | ✓ Live | Commit `ea826c5 feat(rm-c): persist raw filings as Markdown to vault (Loop 4 v5)` |
| DOCX/XLSX extraction in FS ZIPs | ✓ Live | Commit `97064ed feat(rm-c): DOCX/XLSX extraction in FS ZIPs (Loop 4 v3)` |
| JSON snapshot builder | ✓ Live | `scripts/build_vault_ticker_notes.py` — 513 lines, 5 buckets (`mda`, `fsNotes`, `calls`, `filingSummary`, `bizProfile`) |
| Snapshot file | ✓ Rebuilt 2026-08-08 | `data/vault-ticker-notes.json` — 6.08 MB, 232 tickers, 1066 MDA + 1064 FS |
| Dashboard consumer | ✓ Wired | `company-summary.html` line 1422: `fetch('data/vault-ticker-notes.json') → VAULT_MAP[d.tickers]` |
| MDA tab | ✓ Rendered | `company-summary.html` line 1107–1110: `if(tab==='mda') render noteSection(vault.mda, 'MD&A')` |
| FS-NOTES tab | ✓ Rendered | Line 1115: same pattern under `notes` tab |

## What was NOT in place before today (and is now fixed)

- **`data/vault-ticker-notes.json` was missing from the local working tree.** Last commit touching it: `4fceb6f` (2026-06-14). The build script exists and works; the file simply hadn't been regenerated locally in 8 weeks. Today: rebuilt fresh via `python scripts/build_vault_ticker_notes.py`. **No upstream change to the pipeline was needed.**

## Recommended maintenance

1. **Wire the rebuild into the CI daily job** — add a step to `daily.yml` after `disclosure-pulse` that runs `python scripts/build_vault_ticker_notes.py` and commits the result. This prevents the local-only drift that caused today's stale state. (Already on the laptop via the `IS1-Vault-Refresh` Windows task, but the CI path on GitHub Actions skips it.)
2. **Investigate the orphan `CPALL` dir.** It exists in `MDA/CPALL/` and `FS-NOTES/CPALL/` but is not in the IS1 universe. Either pull it into coverage (it's a major SET ticker) or remove the orphan folders.
3. **Surface `analysis.flags` more aggressively in the UI** — the snapshot already extracts MT/RPT/covenant/impairment flags per filing, but the dashboard `mda` tab currently renders only `snippet + drivers + risks + metrics`. Adding a `🚩 flags` row would make the IS1 coverage view catch covenant trips faster.

## Files referenced

- `~/projects/is1-coverage-dashboard/scripts/build_vault_ticker_notes.py` — line 358–407 (`scan_vault`), lines 207–213 (`analyze_body` for `fsNotes` bucket)
- `~/projects/is1-coverage-dashboard/data/vault-ticker-notes.json` — rebuilt 2026-08-08
- `~/projects/is1-coverage-dashboard/company-summary.html` — line 1422 (fetch), 1107–1115 (render MDA + notes tabs)
- `~/projects/is1-coverage-dashboard/SYSTEM.md` — system reference for the vault refresh cadence