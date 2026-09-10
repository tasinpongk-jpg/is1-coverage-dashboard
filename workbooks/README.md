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

- `Control` — period, the NPAT measure per sector, QA panel. The only sheet
  you edit to roll the period.
- `Ticker Detail` — the 241-issuer roster. Sales and NPAT pulled from `Raw DB`.
- `Movers` — which issuers moved each sector and segment, by contribution.
- `Deck Recon` — every place the deck and the database disagree, with the cause.
- Open in Excel and let it calculate; formula cells ship without cached results.

**The NPAT measure is not the same for every sector.** AGRI, FOOD, CONMAT, CONS
and PROP use `36 Net profit-majority`; PF&REIT uses `35 Net profit`, because the
majority column is empty for all 56 funds. Sales is unavailable for PF&REIT
entirely — the panel carries no top line for property funds and REITs.

## IS1_Segment_Database_6M26.xlsx — superseded

The FOOD + PROP only predecessor (119 issuers). Kept for reference; the six-sector
workbook above replaces it.
