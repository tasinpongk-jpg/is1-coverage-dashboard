# workbooks/

Analyst working workbooks. **Excluded from the Cloudflare asset upload** via
`.assetsignore` (`workbooks/` and `*.xlsx`), so nothing here is served from the
public site.

## IS1_Segment_Database_6M26.xlsx

FOOD and PROP segment database for the 6M26 sector review — 119 issuers across
14 segments, rebuilt from `00_Database_all_form.xlsx`.

- `Control` is the only sheet you edit to roll the period.
- `Ticker Detail` is the single roster; NPAT is pulled from `Raw DB` by SUMIFS.
- `Overrides` holds every manually entered figure with its reason and a live
  reconciliation against `Raw DB`.
- Open in Excel and let it calculate before reading any number — formula cells
  ship without cached results.

Two current-period figures (KSL, ITC) do not reconcile to the raw panel and are
flagged orange on `Overrides` and listed as open items on `Change Log`.
