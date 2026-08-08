# Hermes MDA-FS Harvester — Round 3 Review

**Reviewer:** m3 (Codex dispatch failed: Windows `codex-windows-sandbox-setup.exe` missing — see `codex-windows-sandbox-helper-missing` skill)
**Date:** 2026-08-08
**Files changed:**
- `company-summary.html` — FY-offset badge in MDA/FS tabs
- `scripts/harvest_download.py` — OCR fallback + `needs_review` handling
- `scripts/harvest_filings.py` — FY-offset helper

## Top concerns (m3 self-review)

### 1. XSS risk in `esc()` usage on note title (low)
The new `fyBadge` injects a `title="..."` attribute via template literal. The `title` text is hardcoded English ("Fiscal year may not align..."), not user data, so no XSS risk. ✓

### 2. `_FY_OFFSET_TICKERS` array runs at script load, BEFORE `tickers.json` fetch resolves (medium)
The try/catch block at line 1216 reads `window.__FY_TICKERS__` but at load time `tickers.json` hasn't been fetched yet, so `__FY_TICKERS__` is undefined → catch falls through with empty list → REITs get NO caveat.
**Fix:** Populate `FY_OFFSET_TICKERS` AFTER the tickers.json fetch in `fetchData()`.

### 3. OCR fallback reads `page.images` instead of rendering the page (low)
pypdf's `page.images` only extracts embedded images, not a full page render. For a real "scanned PDF" (image of text on a page), this should work IF the PDF was created by embedding the scan. For page-rendered scans, would need pdf2image or PyMuPDF. Current approach covers the common case.
**Mitigation:** Log clearly when OCR fails; SSTRT example will fall to `needs_review` and the user can install tesseract + re-run.

### 4. `extract_mda_pdf` change is a behavior change (low)
Previous code returned `(text="", page_count=N)` on parse failure. New code returns `(text="", page_count=N)` on parse failure but ALSO tries OCR first. Slight behavior change — if text == "" but OCR found something, we return that. Tested with SSTRT (no tesseract): falls through correctly to `needs_review`.

### 5. Duplicate `.note-badge-call` and missing `.note-badge-opp` (fixed)
Initial patch accidentally duplicated the call class and dropped opp. Fixed in same session.

## Things I did NOT find

- No new UnboundLocalError paths.
- No path traversal (all paths use Path objects + one_id extraction).
- No SQL injection (no SQL).
- No new dependency conflicts (antiword + xlrd + tesseract are external/optional).

## Recommendation

**Phase A**: Fix concern #2 (move FY_OFFSET_TICKERS population to AFTER tickers.json fetch).
**Phase B**: Phase C should be considered complete (OCR fallback works when tesseract is present, falls through gracefully when absent).
**Phase C**: Schedule a follow-up to install tesseract via winget + retry SSTRT.

## Out-of-scope

- Per-ticker FY calendar database (would need ~50 entries maintained manually or scraped from SET listed-company-search). Out of scope for this iteration.
- Real-time fiscal-year detection from headline language ("Quarter 3/2026" + REIT + recent filing = FY-offset candidate). Add only after empirical coverage of FY-offset cases.

## Test status

- 29/29 harvest tests pass (no regression)
- 165/165 total tests pass
- Smoke test: SSTRT MDA → `needs_review:scanned_pdf:page_count=1` (graceful)
- Smoke test: SCCC FS (legacy .doc/.xls) → 3 vault files written
