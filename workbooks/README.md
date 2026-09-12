# workbooks/

Analyst working workbooks. **Excluded from the Cloudflare asset upload** via
`.assetsignore` (`workbooks/` and `*.xlsx`), so nothing here is served from the
public site.

## IS1_Sector_Review_6M26.xlsx — current

The database behind `Sector_Review_6M26`. Six sectors, two industries,
39 segments, 241 SET-listed issuers.

| Industry | Sectors | Issuers |
|---|---|---|
| AGRO | AGRI (13), FOOD (58) | 71 |
| PROPCON | CONMAT (21), CONS (32), PROP (61), PF&REIT (56) | 170 |

It follows the deck flow — industry, sector, segment, then the issuers that
moved the segment — and carries the deck's own figure beside every computed
one so the two can be cross-checked without leaving the sheet.

- `Version Log` — what changed in each build (v1 to v4), which sheets it
  touched, and which `Deck Data` blocks the deck must pull again. Read it
  before rebuilding a slide from an older copy of this file.
- `Deck Guide` — how to turn this workbook into the PowerPoint: what to build
  on each slide, which block to read, design rules, pre-send checks. Attach the
  workbook with the PPTX and follow it.
- `Deck Data` — slide-ready blocks B1–B16, every figure the deck needs, already
  computed. Literal values, not formulas, so an LLM reading the file sees
  numbers rather than blanks.
- `Control` — period, the NPAT measure per sector, QA panel. The only sheet
  you edit to roll the period.
- `Verify` — type a ticker, see everything about it plus a tie-out ladder from
  issuer to industry. Start here when checking a number.
- `Ticker Detail` — the 241-issuer roster. Sales and NPAT pulled from `Raw DB`;
  market cap at 31 Aug 2026 and 5 Jan 2026.
- `Movers` — which issuers moved each sector and segment, by contribution.
- `MD&A` — one row per segment keyed to that segment's top mover, over a
  47-ticker commentary library. All 39 segments now carry commentary; every
  entry states the period it actually covers.
- `Revenue Structure` — FY2025 OneReport top lines and SET alignment, 182 of 241.
- `Deck Recon` — every place the deck and the database disagree, with the cause.
- Open in Excel and let it calculate; formula cells ship without cached results.

**Sales comes from the raw panel, not the deck.** `01 Sale` (column J) is the
primary revenue measure at every level, all six sectors including PF&REIT. The
deck's Sales YoY never reconciled under any aggregation and is kept only as a
greyed reference column.

**Analyst-supplied figures live in `Raw DB` with a cell comment**, not as
overrides: ITC 6M26 (Sales 9,703.74, NPAT 1,715.37), BAREIT 6M26 from the
official reviewed statements (revenue 590.165, net increase in net assets
462.503), and the PF&REIT top line for all 56 funds. Hover any yellow cell in
`Raw DB` for its source. Overrides is now only the five non-calendar-FYE issuers.

**Only 9 of the 22 newest MD&A entries are a clean six months.** Eight quote
Q2 in the summary sentence (FUTURERT, LEE, NRF, PPP, RABBIT, SCGD, TASCO, TOA),
EPG is Q1 FY26/27, FTREIT is a special fiscal year, CBG has no six-month
aggregate at all, DREIT mixes Q2 into a 6M commentary and XBIO does not state
its period. Column C of the MD&A library carries the basis and those rows are
filled orange; a caption built from one of them will not tie to the bar beside
it unless the period is said out loud. NRF also carries a going-concern
disclaimer.

**The PF&REIT decline in the deck is overstated by 462 THB m.** Both the deck and
the raw panel had BAREIT missing for the current period. It did file. R6 is
+193, not −270; the sector is −321, not −783.

**Market cap sits on one date.** All six sectors are priced at 31 Aug 2026 from
the SETSMART export, with 5 Jan 2026 carried alongside as the start-of-year
base. FOOD and PROP tie to the deck exactly.

**The NPAT measure is not the same for every sector.** AGRI, FOOD, CONMAT, CONS
and PROP use `36 Net profit-majority`; PF&REIT uses `35 Net profit`, because the
majority column is empty for all 56 funds. Sales is unavailable for PF&REIT
entirely — the panel carries no top line for property funds and REITs.

## IS1_Segment_Database_6M26.xlsx — superseded

The FOOD + PROP only predecessor (119 issuers). Kept for reference; the six-sector
workbook above replaces it.
