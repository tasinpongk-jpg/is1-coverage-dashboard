# 6M26 panel extraction — runbook

Builds the 6M26-vs-6M25 company / segment / sector panels that the Sector Review
deck needs, from the Q2/2026 filings already harvested into the vault.

## Why this exists

`Sector_Review_FOOD_PROP_FY2025_Audited_6M26_Update_v1.0_2026-08-09.pptx` was
built before the Q2/2026 filing wave. Its own provenance records the gap:

> `"limitations": ["6M26 actual RFO/NPAT and MD&A are pending", ...]`

`data/sector-intelligence.json` still carries `"earningsPeriod": "FY2025 vs
FY2024"` and has no 6M26 field. The filings themselves arrived on 10–17 Aug 2026
and are in the vault; what was missing was a way to turn them into numbers.

## The extraction contract

`scripts/extract_6m26_figures.py` — **verify or exclude.**

A figure is published only when one of two things is true:

1. **Self-reconciliation.** The YoY percentage the issuer printed beside the
   6M26 column matches the YoY computed from the extracted 6M25/6M26 pair,
   within 1.0pp (issuers round to whole percents). Picking the wrong column
   breaks this check, so a wrong column is rejected rather than published.
2. **Proven geometry.** A loss-making issuer prints no usable YoY on its NPAT
   line. That row is accepted only when a *different* row in the same table
   self-reconciled, which proves where the 6M columns sit. A row whose own YoY
   *disagreed* is never rescued this way — that is a wrong pick, not a missing
   percentage.

Everything else is returned unverified with a reason and excluded from the
panel. Nothing is estimated, interpolated, or summed from quarters.

### Basis discipline

| Deck measure | What the parser accepts |
| --- | --- |
| RFO (SET 01 Sale) | A revenue line that already excludes other income, or `total revenue − other income` where both rows independently reconciled. The subtraction is recorded in `rfo_derivation`. |
| NPAT to owners | Only a line explicitly attributable to the parent/owners. A plain "Net profit" is captured separately as `npat_unattributed_6m26_mb` and never enters the panel — an analyst promotes it once NCI is confirmed immaterial. |

Rows labelled core, adjusted, normalised, or per-share are never selected.

### Independent panels

RFO and NPAT coverage are tracked separately, matching the FY build — a company
can be in the revenue panel and out of the profit panel. Margin is computed
strictly on the intersection.

### Blunder checks

- Implied 6M26 net margin outside −200%…100% rejects the NPAT row.
- 6M26 RFO outside 20–85% of audited FY2025 RFO blocks the company from both
  panels. Deliberately wide: this catches scale and row errors, not seasonality.

## Format variants observed in real filings

Sampling real Q2/2026 MD&A from the vault turned up three distinct layouts. The
first two extract cleanly; the third is the reason the reconciliation gate
exists.

| Issuer | Layout | Outcome |
| --- | --- | --- |
| CPN | `6M25` / `6M26` columns, `YoY (%)` split across two tokens, combined total revenue | Both measures published; RFO derived as total less other income |
| ITC | `1H25` / `1H26` columns, `%YoY` as one token, "Sales and service" already on the 01 Sale basis | Revenue published; owner NPAT withheld — the filing prints only an unattributed "Net profit" |
| AWC | `6M/2026` before `6M/2025`, header emitted *after* the data rows, `%Change` headers on their own lines, row labels detached and reprinted in a block | Nothing published |

AWC is kept as a fixture precisely because its true figures are recoverable by
eye (12,278 / 11,401 revenue; 3,455 / 3,374 net profit) but not provably by
machine. A test asserts the parser never emits those numbers, so a future change
that reads the right cells by accident still fails the suite.

Two safe generalisations came out of this sampling: half-year columns may be
written with a slash (`6M/2026`), and the current period may be printed before
the prior one. Position is always read from the header, never assumed.

## Prerequisite: re-extract the DOCX filings

`harvest_download.py:_docx_text` read only `doc.paragraphs`, so **every table in
every DOCX filing was silently discarded** while the extraction still reported
`extraction_status: ok`. In a SET financial statement essentially all numbers
live in tables. `NOTES_CPF_2026Q2_E.md` shows the symptom — "Revenue and results
… were as follows:" followed by nothing.

This is fixed (tables now emit tab-separated rows in document order, matching the
XLS path), but **the fix does not repair files already in the vault.** Q2/2026
FS-NOTES must be re-harvested to recover their numbers:

```bash
python scripts/harvest_filings.py --lookback 10
python scripts/harvest_download.py
```

`python-docx` is now pinned in `requirements.txt`; without it that helper returns
an empty string and DOCX filings land empty.

MD&A filings are mostly PDF and were never affected — the half-year tables they
carry are what this pipeline reads today.

## Running it

```bash
python scripts/build_6m26_panel.py \
  --vault-root "$VAULT/Work-SET/Listed Company" \
  --fy-company-csv ".../official-2026-08-08-eod-2026-08-07/food_prop_company_fy2024_2025_audited_2026-08-07.csv" \
  --out-dir ".../data/6m26-$(date +%F)" \
  --as-of "$(date +%F)"
```

The FY company CSV is required — it is the authoritative 118-company perimeter,
supplies the segment mapping, and provides the FY totals used by the
plausibility band. Exit code is non-zero if QA fails.

### Outputs

| File | Contents |
| --- | --- |
| `food_prop_company_6m25_6m26_<date>.csv` | One row per company: figures, panel flags, exclusion reason, and for every published number its matched label, evidence line, source path and SHA-256 |
| `food_prop_segment_6m25_6m26_<date>.csv` | Segment aggregates, panel membership and direction drivers |
| `food_prop_sector_6m25_6m26_<date>.csv` | FOOD / PROP totals |
| `QA_SUMMARY_6M25_6M26_<date>.json` | Structural checks; `verdict` must be `PASS` |
| `PROVENANCE_6M25_6M26_<date>.json` | Per-ticker source hashes, output hashes, method and limitations |

Every published figure is traceable to a line of a filing. When a reviewer
challenges a number, `rfo_evidence` / `npat_evidence` hold the exact source row.

## Tests

```bash
python tests/test_6m26_extraction.py   # parser + the DOCX table fix
python tests/test_6m26_panel.py        # end-to-end panel build
```

Fixtures under `tests/fixtures/` are verbatim excerpts of real vault filings
(CPN and ITC Q2/2026), kept unedited including pypdf spacing artefacts, so the
parser is tested against what the vault actually holds. They cover two
deliberately different layouts: `6M25/6M26` with `YoY (%)` split across tokens,
and `1H25/1H26` with `%YoY` as one token.

## Known limitations

- MD&A half-year tables are management-prepared and can differ from the reviewed
  interim financial statements. Once the DOCX re-extraction lands, FS-NOTES can
  corroborate them.
- Issuers whose MD&A carries no half-year table are excluded, not inferred.
- `PROUD` 2026Q2 MD&A extracted as 65 bytes of glyph noise (scanned PDF, no OCR)
  and needs the tesseract/`MINIMAX_API_KEY` fallback described in
  `HARVEST-Q2-2026-REPORT.md`.
- `PM` and `AP` have no Q2/2026 MD&A in the vault at all.
