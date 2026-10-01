Verbatim excerpt of MDA_AWC_2026Q2_E.md (vault 1-Raw/01-Filings/MDA/AWC/),
source PDF 1523NWS140820261245106240E.pdf, source_sha256
c26a684481bdd9d4b5a46e1462b2abfcbe9f65de6fe0710cb67c301c162a9e89, extractor
pypdf-v5.

A hostile third layout, kept as a regression case for what the parser must
REFUSE. Three separate pypdf artefacts stack up here:

  1. The column header line is emitted *after* the data rows, not before.
  2. The "%Change YoY / QoQ" headers sit on their own lines, so the header line
     names 5 columns while each data row carries 8 numeric fields.
  3. Every row label except "Total Revenue" is detached and reprinted in a
     block at the bottom, so those rows cannot be attributed to a measure.

Ground truth, read by hand: 6M/2026 total revenue 12,278 and 6M/2025 11,401
(stated +7.7%; computed +7.69%); 6M/2026 net profit 3,455 and 6M/2025 3,374
(stated +2.4%; computed +2.40%). The parser must publish NEITHER, because it
cannot prove the column mapping from this text — a silently wrong number is
worse than a company reported as needing review.

Total Revenue 
In 2Q/2026, the Company recorded total revenue of THB 5,502 million, representing y ear-on-year growth of 5.6%. 

%Change %Change %Change
YoY QoQ YoY
Total Revenue 5,502      6,776      5,211      5.6% -18.8% 12,278    11,401    7.7%
2,460      2,882      2,344      5.0% -14.6% 5,342      4,871      9.7%
2,850      3,531      2,723      4.6% -19.3% 6,381      6,140      3.9%
51.8% 52.1% 52.3% -0.5% -0.3% 52.0% 53.9% -1.9%
1,468      1,986      1,404      4.6% -26.1% 3,455      3,374      2.4%
26.7% 29.3% 27.0% -0.3% -2.6% 28.1% 29.6% -1.5%
Unit: THB Million 2Q/2026 1Q/2026 2Q/2025 6M/2026 6M/2025
Earnings Before Interest, Taxes, Depreciation, and Amortization (EBITDA)
Costs and Expenses1
EBITDA Margin
Net Profit
Net Profit Margin
