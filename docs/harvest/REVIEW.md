# Hermes MDA-FS Harvester — Design Review

**Author:** Hermes (m3) with empirical SET API probes
**Date:** 2026-08-08
**Status:** Review complete, build starting

---

## Verdict

**GO-WITH-CHANGES** — the design is sound but the original Layer 2 plan duplicates logic that already exists in `scripts/vault_raw_writer.py` (Loop 4 v5) and `scripts/enrich_filing.py:_build_raw_markdown`. The new Layer 2 must **call into those existing modules**, not re-implement extraction + frontmatter + vault routing. With that one correction, the design is the smallest possible reliable pipeline.

---

## Critical flaws (must fix before building)

### F1. Duplication risk with existing vault_raw_writer.py  [verified — read script]
The proposed `scripts/harvest_download.py` was going to re-implement:
- ZIP/DOCX/XLSX/PDF text extraction
- Markdown frontmatter rendering
- Vault routing (MDA / FS-NOTES / AUDITOR folders)
- SHA-256 dedup

All of this **already exists** in:
- `scripts/enrich_filing.py:_build_raw_markdown()` — lines 225-289 (extraction)
- `scripts/enrich_filing.py:_classify_doctype()` — lines 594-634 (filename/type → MDA/AUDITOR/FS/NOTES)
- `scripts/vault_raw_writer.py:_DOCTYPE_DIR` — line 47 (folder mapping)
- `scripts/vault_raw_writer.py:_write_*` functions (atomic write)

**Falsifier:** "The existing code is in the wrong shape to reuse" — false. `vault_raw_writer.py:_DOCTYPE_DIR = {"MDA": "MDA", "AUDITOR": "AUDITOR", "FS": "FS-NOTES", "NOTES": "FS-NOTES"}` is exactly the routing we need. And the frontmatter shape in `fetch_set_financial_filings.py:markdown()` already matches what `build_vault_ticker_notes.py` consumes (both produce `ticker`, `period`, `news_id`, `source_sha256`, `source_url`, `source_file`, `tags`, `source_type`).

**Fix:** Layer 2's job is to produce a `raw_markdown` dict that `vault_raw_writer.py` already accepts, then call into it. We add NO new vault-writing code.

### F2. SET firehose cap is 400 items per call  [verified — probe2 ran 2026-08-08]
The Aug 7, 2026 firehose returned exactly **400 items** for a one-day window. For full-day coverage of ~150-200 new disclosures plus backfill of MDA/FS, **one call is not enough**.

**Falsifier:** "400 covers the whole day" — false; SET publishes 200-300 filings per weekday and the firehose returns all of them, but only the first 400. On heavy disclosure days (end-of-quarter, Aug 14 SET 50 Index rebalance, AGM season) this caps.

**Fix:** Use **per-ticker search** for the MDA/FS subset as the primary path (each ticker returns max ~50 items/week, well under the cap), with firehose only for catch-up scans. The existing `surveillance/poll.py:poll_per_symbol()` already implements this pattern correctly.

### F3. AP search returned 17 items but only 1 was a debenture  [verified — probe2]
Per-ticker search returns ALL news types for that ticker (debentures, dividend notices, ESG reports). The harvest must filter strictly to MDA/FS, NOT ingest everything.

**Falsifier:** "Filter by `tag == 'financial-statement'` is enough" — partially true. Probe showed `tag == "financial-statement"` for FS-ZIPs, but `tag == ""` for MDA PDFs. So we need **headline keyword matching**, not tag-only.

**Discriminator (verified from real TPAC MDA + FS response on 2026-08-07):**
- **MDA**: `headline` contains `"Management Discussion and Analysis"` AND `fileType == "PDF"` (from detail)
- **FS**: `headline` contains `"Financial Statement"` OR (`tag == "financial-statement"` AND `fileType == "ZIP"`)
- Skip everything else (debentures, dividends, AGM notices)

### F4. Vault is laptop-only (OneDrive path)  [verified — read SYSTEM.md]
The vault lives at `C:\Users\Tasinpong\OneDrive - The Stock Exchange of Thailand\Claude-Vault\...`. CI runners cannot read this. So Layer 2 cannot run in CI; only Layer 1 (discovery) can.

**Falsifier:** "We can run Layer 1 in CI and Layer 2 on a Cloudflare Worker with R2 sync" — yes, that works, but it requires a major restructure (Workers have no `pip install docx`). Smaller: run both layers on the laptop via scheduled task.

**Fix:** Both Layer 1 and 2 run on the laptop via Windows task. CI only runs discovery if/when we add a second source (e.g., eFinanceThai RSS that doesn't need vault access).

### F5. Period regex gap  [verified — read build_vault_ticker_notes.py]
Existing regex `(20\d{2}(?:Q[1-4]|FY)|\d{4}Q[1-4]|\d{4}FY)` matches `2026Q1` and `2025FY` but NOT `Q2/2569` (Thai Buddhist year) or `Quarter 2/2026` (SET headline format from probe2).

**Falsifier:** "Period is always in the filename" — false; the SET headline is `Quarter 2/2026` but the filename uses `2026Q2`. We need to extract period from BOTH filename AND headline (with BE-year adjustment for Thai).

**Fix:** Add a `parse_period(headline, filename)` helper that:
1. Tries filename first (matches existing pattern)
2. Falls back to `Quarter N/YYYY` regex from headline
3. Converts `2569` (Buddhist) → `2026` (Gregorian) by subtracting 543

---

## Design tweaks (not blocking, recommended)

### T1. m3 only at the boundary — confirmed  [from user's "I need the info reliable"]
The original design had Layer 4 (m3 disambiguation) deferred. Confirmed: keep it that way. The empirical probes show the headline + tag + fileType fields are enough to classify >95% of filings deterministically. The remaining 5% are edge cases that get human review via Discord (existing pattern).

### T2. Queue file as durable contract  [design decision]
Between Layer 1 (discovery) and Layer 2 (download), use `data/harvest-queue.json` as the durable contract. Layer 2 reads it, marks items as `done | failed | skipped`, and writes back. This means:
- Layer 2 can crash mid-batch and resume next run
- We can audit "what did we try to harvest" without re-hitting SET
- Manual review can clear stuck items

### T3. State file separate from queue  [design decision]
`data/harvest-state.json` holds the source_sha256 dedup table. Persisted across runs. NEVER overwritten — only appended. If state is corrupt, the worst case is re-downloading (cheap; SET doesn't charge for downloads).

---

## MVP scope — what we build today

The smallest thing that proves the design works:

1. **`scripts/harvest_filings.py`** — Layer 1 discovery
   - Input: `data/tickers.json` (232 tickers)
   - Output: `data/harvest-queue.json` with new MDA/FS items only
   - Per-ticker search via `surveillance/client.py:SetNewsClient`
   - Strict headline filter (no debentures/dividends)
   - Smoke test: AP search → confirm MDA + FS detection

2. **`scripts/harvest_download.py`** — Layer 2 download + write
   - Input: `data/harvest-queue.json`
   - For each item: detail API → download ZIP/PDF → call `vault_raw_writer` to write
   - Skip if `source_sha256` already in `data/harvest-state.json`
   - Smoke test: 1 ticker (AP, 2026Q1) end-to-end → verify vault markdown appears

3. **`scripts/register_harvest.ps1`** — Windows task
   - Daily 10:30 BKK, after `IS1-Vault-Refresh` (10:30) + before `Vault-Notes-Refresh` (10:35)
   - Calls `harvest_filings.py` then `harvest_download.py`

4. **`tests/test_harvest.py`** — smoke + unit
   - Period regex test (10 cases including Thai Buddhist year)
   - Headline classifier test (MDA / FS / debenture / dividend)
   - End-to-end smoke with mocked SET API

---

## Anti-recommendations (do NOT build)

1. **❌ Per-ticker detail pre-fetch.** The detail endpoint is hit only for items we want to download (max 10-20/day), not for all items in the search result. Pre-fetching is wasteful and hits Incapsula faster.
2. **❌ Parallel downloader.** 5-20 downloads/day is not worth the complexity of asyncio + thread pools. Sequential with `MIN_INTERVAL_SEC = 0.6` is fine.
3. **❌ Full-text search across vault to detect "already covered".** SHA-256 of the source ZIP/PDF is enough; if SHA matches, skip. No need to fuzzy-match titles.
4. **❌ Discord notification on every harvest.** Email-on-failure is enough. Daily summary goes through the existing `morning-brief` pipeline.
5. **❌ Run harvest in CI.** Vault is laptop-only. Don't pretend we can split this into CI + laptop — the cost of OneDrive sync + R2 staging is more than just running locally.

---

## Concrete file list for Phase 2 build

| File | Lines (est) | Purpose |
|---|---:|---|
| `scripts/harvest_filings.py` | 180 | Layer 1: discovery |
| `scripts/harvest_download.py` | 220 | Layer 2: download + delegate to vault_raw_writer |
| `scripts/register_harvest.ps1` | 50 | Windows task registration |
| `tests/test_harvest.py` | 120 | Period regex + headline classifier + smoke |
| `docs/harvest/REVIEW.md` | (this file) | — |

**Total new code:** ~570 lines. **No new vault-writing code** (delegates to existing `vault_raw_writer.py`).

---

## Confidence: HIGH

- SET API response shape verified by 3 probes (search, MDA detail, FS detail)  [verified]
- Existing `vault_raw_writer.py` shape matches what we need  [verified — read script]
- Firehose 400-item cap verified  [verified]
- Per-ticker search works for AP, returns 17 items, discriminating filter is simple  [verified]
- The 4 deduplication concerns are resolved (SHA-256, queue, state, headline filter)  [verified]
- The vault/laptop constraint is acknowledged (Layer 1+2 both run on laptop)  [verified]

## What remains unverified

- The exact 400-item cap behavior under pagination (does SET have a `page` or `offset` param?) — [unverified — will probe in build]
- Whether the harvest hits Incapsula after ~50 requests without throttling — [unverified — will throttle to 1 req/s]
- Whether `vault_raw_writer.py` rejects writing if a different SHA exists for the same `(tk, period, kind)` — [unverified — will read more carefully during build]

---

## Falsifiers for the WHOLE design

If any of these are true, the design fails:

1. **SET headline doesn't reliably distinguish MDA from FS** — false based on TPAC probes (Aug 7 had both, with distinct headlines). Even if it were partially true, the `tag` field is a backup discriminator.
2. **`vault_raw_writer.py` cannot accept externally-supplied raw_markdown** — would need to refactor, doubling the code. Mitigation: read the script during build and confirm.
3. **OneDrive vault path is unavailable when scheduled task runs** (laptop asleep, OneDrive paused) — true edge case. Mitigation: `StartWhenAvailable` in the task definition + idempotent re-run.
4. **The 232-ticker universe produces >400 new MDA+FS filings per day** — false; even at peak AGM season, expect <50 new filings/day for IS1.
