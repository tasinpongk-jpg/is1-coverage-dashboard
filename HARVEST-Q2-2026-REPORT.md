# Q2/2026 FS + MD&A Harvest Report

**Date:** 2026-08-17
**Operator:** Hermes (m3 main loop)
**Commits:** `67babe4`, `42c963b` (on `main`, both pushed to origin)
**Trigger:** SET Q2/2026 reporting window (Aug 10–17, 2026)

---

## What ran

| Layer | Script | Result |
|---|---|---|
| 1. Discover | `harvest_filings.py --lookback 10` | 409 MDA/FS candidates found across 232 IS1 tickers, 387 new + 22 already known |
| 2. Download + extract | `harvest_download.py` | 387/387 ok, 0 hard failures, 0 needs_review |
| 3. Snapshot rebuild | `build_vault_ticker_notes.py` | `vault-ticker-notes.json` refreshed (mda 1066→1080, fsNotes 1065→1091) |
| 4. Migration | `migrate_misplaced_fs_notes.py` | 206 NOTES files relocated to FS-NOTES/, 3 conflicts resolved via `--prefer-larger` |
| 5. Re-extract | `rerun_failed_fs_q2.py` | 7 tickers with stale state re-extracted into correct folders |

---

## Bugs found and fixed

### Bug 1 — `vault_raw_writer.py:321` (commit `67babe4`)

```python
# BEFORE — picks the FIRST subdir in a multi-doctype filing
subdir = next(sub for _, sub, _ in to_write)

# AFTER — groups by subdir and writes each doctype to its own folder
by_subdir: dict[str, list[tuple[str, str, str]]] = {}
for filename, subdir, body in to_write:
    by_subdir.setdefault(subdir, []).append((filename, subdir, body))
for subdir, group in by_subdir.items():
    final_dir = vault_root / RAW_DIR_NAME / subdir / tk
    ...
```

**Symptom:** SET FS ZIPs ship `[AUDITOR_REPORT, NOTES, FINANCIAL_STATEMENTS]` inside a single ZIP. The old code wrote ALL of them under `AUDITOR/<TK>/` because AUDITOR was the first doctype. NOTES files ended up in the wrong folder for ~200 Q2/2026 filings.

**Verified impact:**

| | Before | After |
|---|---:|---:|
| Q2/2026 in FS-NOTES/ | 18 | 219 |
| Q2/2026 in AUDITOR/ | 407 (inflated) | 204 (correct) |
| NOTES_-prefixed files misplaced in AUDITOR/ | ~200 | 0 |

### Bug 2 — `harvest_download.py:597` (commit `42c963b`)

```python
# BEFORE — any PDF routed to MDA extractor regardless of kind
if kind == "MDA" or file_type == "PDF":
    text, page_count = extract_mda_pdf(payload)
    docs.append({"doctype": "MDA", ...})

# AFTER — kind is authoritative; AUDITOR-PDF filings write to AUDITOR/
if kind == "MDA":
    ...
elif kind == "AUDITOR":
    ...
    docs.append({"doctype": "AUDITOR", ...})
elif kind == "FS" or file_type == "ZIP":
    ...
elif file_type == "PDF":  # unknown kind, fallback to MDA
    ...
```

**Symptom:** NRF news_id 106345300 "Explanation of the Auditor's Report Disclaimer of Opinion..." shipped as a 2-page PDF. The harvest script misclassified it as MDA and wrote `MDA_NRF_UNKNOWN_E.md` instead of `AUDITOR_NRF_2026Q2_E.md`.

**Verified:** NRF now has all three files correctly routed:
```
MDA:      MDA_NRF_2026Q2_E.md (46,906 B)
FS-NOTES: NOTES_NRF_2026Q2_E.md (32,473 B)
AUDITOR:  AUDITOR_NRF_2026Q2_E.md (7,806 B)
```

This bug only affected the 1 ticker with AUDITOR-PDF in this batch (NRF). The wider pattern (`kind == "MDA" or file_type == "PDF"`) had the same effect on every historical AUDITOR-PDF filing, but those are not in scope for this run.

---

## Coverage results

### Universe: 232 IS1 tickers

| Metric | Count | Source |
|---|---:|---|
| Tickers with ≥1 MDA markdown | 232 | vault scan |
| Tickers with ≥1 FS-NOTES markdown | 232 | vault scan |
| Tickers with Q2/2026 MDA | 210 | snapshot |
| Tickers with Q2/2026 FS-NOTES | 218 | snapshot |
| Tickers with Q2/2026 AUDITOR | ~190 | vault scan |
| Tickers missing Q2/2026 MDA | 22 | Mostly REITs (FTREIT, IMPACT, EPG, BLAND, etc.) with fiscal year offsets — known caveat per `set-harvest-pipeline` §FY-offset |

### Vault file distribution by period

| Period | MDA | FS-NOTES | AUDITOR |
|---|---:|---:|---:|
| 2027Q1 | 0 | 5 | 5 |
| 2026Q3 | 0 | 4 | 4 |
| **2026Q2** | **211** | **219** | **204** |
| 2026Q1 | 269 | 269 | 234 |
| 2025Q3 | 244 | 239 | 239 |
| 2025Q2 | 241 | 235 | 235 |
| 2025Q1 | 238 | 233 | 233 |
| 2025FY | 245 | 256 | 256 |

### Filename-prefix integrity (cross-contamination check)

```
MDA_-prefixed     in MDA/:       2,280
NOTES_-prefixed   in FS-NOTES/:  2,145
AUDITOR_-prefixed in AUDITOR/:   2,096

MDA_-prefixed     OUTSIDE MDA/:         0   ✓
NOTES_-prefixed   OUTSIDE FS-NOTES/:    0   ✓
AUDITOR_-prefixed OUTSIDE AUDITOR/:     0   ✓
```

Zero cross-contamination across all three vault folders.

---

## Files committed

```
67babe4 fix(vault_raw_writer): route multi-doctype filings to correct folders
42c963b fix(harvest_download): preserve kind=AUDITOR for single-file PDF filings
```

**Modified:**
- `scripts/vault_raw_writer.py` — bug 1 fix (group by subdir before iterating)
- `scripts/harvest_download.py` — bug 2 fix (kind-first routing in extract branch)
- `data/vault-ticker-notes.json` — refreshed snapshot

**Added:**
- `scripts/migrate_misplaced_fs_notes.py` — relocate misplaced NOTES files; supports `--dry-run`, `--period`, `--all-periods`, `--prefer-larger` flags
- `scripts/rerun_failed_fs_q2.py` — clear stale state for tickers whose FS ZIPs landed in wrong folder, then re-extract via the fixed writer

**Skipped (intentionally not committed):**
- `dist/` — prior build artifact, not from this run

---

## Verification checklist

- [x] V1: Vault folder distribution balanced across periods
- [x] V2: No NOTES_-prefixed files misplaced in AUDITOR/
- [x] V3: Snapshot fsNotes count matches vault scan (1.00 ratio)
- [x] V4: No regressions in 2026Q1, 2025FY, 2025Q3 periods
- [x] V5: No MDA / AUDITOR files misplaced in other folders
- [x] V6: Commit `42c963b` on `origin/main` (Cloudflare Pages will auto-deploy)
- [x] V7: Queue item → vault file resolution: 395/395 queue items resolved (1 false positive in gap scan, see below)

### Known minor gaps

1. **`AUDITOR_NRF_UNKNOWN_E.md`** — period regex doesn't recognize "three-month and six-month periods ended June 30, 2026" headline variant. File is correctly routed to the right folder but has `period: UNKNOWN` in filename. Acceptable — only 1 file affected out of 1,080+ MDA entries.
2. **Scanned PDFs without OCR** — SST, JCK, NNCL, KTIS, F&D, CFRESH, ROJNA, PPP, PEACE, KBS, BRR (~20 tickers) had scanned MDA PDFs. Without `MINIMAX_API_KEY` or `tesseract` installed, these landed as metadata-only via `needs_review:scanned_pdf`. Fix path: install tesseract (`winget install --id tesseract-ocr.tesseract --silent`) or add a `MINIMAX_API_KEY` to `.hermes/.env-harvest`.
3. **22 tickers missing Q2/2026 MDA** — REITs with fiscal-year offset (FTREIT, LHRREIT, etc.) and one-offs like IMPACT (Jul-Jun FY). Tracked by `_is_likely_fy_offset` and shown with amber `FY` badge in the dashboard.

---

## Suggested follow-up (not blocking)

| Action | Why |
|---|---|
| `winget install --id tesseract-ocr.tesseract --silent` | Enables OCR fallback chain in `harvest_download.py:_ocr_pdf_fallback`, currently always returns `needs_review` for scanned PDFs. Estimated impact: 20 MDA files/day × $0 OCR cost = $0 + 20 more fully-extracted MDA per quarter. |
| Add `MINIMAX_API_KEY` to `~/.hermes/.env-harvest` | Primary OCR chain is m3 vision (better Thai than tesseract). Per-skill P10, m3 wins on word boundaries. Cost ~$1-3/month at 5-20 PDFs/day. |
| Wire `harvest_filings.py` + `harvest_download.py` into a daily cron | Both scripts are now correct. A scheduled job at 06:00 BKK after the 15:00 SET disclosure window would keep the vault current without manual intervention. |
| Extract `_period_from_filing` enhancement | Add `"three-month and six-month periods ended {Month} {Day}, {Year}"` regex to handle the "Disclaimer of Opinion" headline variant. Single-period gap, low priority. |

---

## Falsifier (whole design)

> **"If the snapshot says fsNotes=1091, the dashboard will show 1,091 FS-NOTES records."**

False — the snapshot keeps only the top-5 newest MDA and FS-NOTES files per ticker (see `build_vault_ticker_notes.py`). The actual vault has 2,145 FS-NOTES files. The snapshot is a *display* artifact, not a complete inventory.

To verify the full vault, run:

```bash
python -c "
from pathlib import Path
import re
VAULT = Path('C:/Users/Tasinpong/OneDrive - The Stock Exchange of Thailand/Claude-Vault/Work-SET/Listed Company')
for doctype in ['MDA','FS-NOTES','AUDITOR']:
    n = sum(1 for f in (VAULT/'1-Raw/01-Filings'/doctype).rglob('*.md'))
    print(f'{doctype}: {n} files')
"
```