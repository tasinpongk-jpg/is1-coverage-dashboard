# SEC Open Data API — what IS1 can actually pull

Portal: <https://secopendata.sec.or.th/sec-open-apis> (SPA behind a WAF)
Base URL: `https://api.sec.or.th`
Auth: header `Ocp-Apim-Subscription-Key: <key>` — one subscription covers every product group.
Rate limit: 3,000 calls / 300 s, shared across groups.
Support: repcenter@sec.or.th

> **Portal migration.** The new portal went live 12 Jan 2026; the old
> `api-portal.sec.or.th` was retired 30 Jun 2026. Anything you find online
> using `/FundFactsheet/fund/{proj_id}/...` paths is the dead v1 fund API —
> the live fund paths are `/v2/fund/...`.

## Keys

Never in the repo, never in a commit. Two keys are issued (primary + secondary
for rotation). Set them in the shell:

```bash
export SEC_API_KEY=<primary>
export SEC_API_KEY_SECONDARY=<secondary>   # optional; client fails over on 401/403
```

`scripts/sec_api.py` reads only those two variables. `.env` is already
gitignored — put them there if you would rather not re-export each session.

## Two API shapes

| | v1 (`one-report`, `pvd`, `license-check`, `digital-asset`) | v2 (`fund`, `bond`) |
|---|---|---|
| Selector | path params — `{report_year}`, `{unique_id}`, `{proj_id}` | query params — `proj_id`, `bond_id`, `search` |
| Paging | none; one call returns the array | `page_size` (1–100) + `next_cursor` |
| Latest record | n/a | `latest=true` on most factsheet endpoints |
| Shape | bare JSON array (some deployments wrap in `items`) | `{message, page_size, next_cursor, items[]}` |

`scripts/sec_api.py` exposes `get_v1(path)` and `paginate_v2(path, params)` for
the two shapes and handles throttling, 429/5xx backoff, and key failover.

## The join key: unique_id, not ticker

SEC keys issuers on `unique_id` (`C0000000013`), not the SET symbol. Endpoint
`01-SBO-Info` (`/v1/one-report/sbo/{report_year}/info/{language}`) is the only
place the two are published together — it returns `unique_id` + `symbol` +
`corp_name` for every issuer that filed a One Report that year. Resolve the map
once per year, cache it, join everything else off it.

`scripts/build_sec_onereport.py --map-only` does exactly that and prints the map.

## What is worth pulling, ranked for IS1

**1. One Report (23 endpoints) — the highest-value group.**
The only structured annual issuer data SEC publishes. Four datasets have no
other machine-readable source in this repo:

| Dataset | Endpoint | Why it matters |
|---|---|---|
| Revenue by segment | `03-SBO-Product-Income` | Direct input to the sector alignment review — actual top revenue segment vs registered SET sector. Carries 3 years of value and % share, so the shift is visible without a second call. |
| Auditor + fees | `19-CGS-AuditorCompany` | `auditor_company_name_th`, `audit_fee`, `non_audit_fee`. Auditor change YoY and a non-audit / audit fee ratio are both surveillance flags the dashboard has no feed for today. |
| AGM + meeting cadence | `20-CGS-DirectorPerformance` | `agm_meeting_date`, `total_board_meeting`, `total_audit_meeting`, `egm_meeting`. Audit committee that met twice in a year is a flag. |
| Board composition | `17-CGS-Board` | headcount, independent, executive, non-executive, gender split. |

Also there and cheap: `16-CGP-FinancialStatement` (full FS line items with
`set_code`, 3 years — a free cross-check against the vault FS-NOTES),
`21-CGS-Bods` / `22-CGS-Executives` (director and executive rosters, with
`start_date` / `end_date` — turnover detection), `05-SBO-Risk-Detail`,
`04-SBO-Export-Income`, and the sustainability / social-performance blocks.

Caveat: annual, and it lags the SET filing feed by months. Cross-check layer,
not a timeliness layer.

**2. Fund (21 endpoints) — partial PF&REIT cover.**
`/v2/fund/general-info/profiles`, `factsheet/performance`, `factsheet/fees`,
`outstanding/portfolio` (quarterly holdings), `daily-info/nav`,
`daily-info/dividend-history`. Property funds are SEC-registered mutual funds,
so the PF side of the 16-ticker PF&REIT book should resolve by `proj_id`.
**REITs are trusts, not mutual funds — unverified whether they appear in this
group at all.** Test with a known PF (TTLPF, HPF, TIF1) and a known REIT
(FTREIT, WHART, CPNREIT) before building anything on it.

**3. Bond (6 endpoints).**
`/v2/bond/issuers`, `outstanding-values`, `credit-ratings`, `investor-holdings`.
This is the same source `setlake-sec-bond` already materialises into the vault
for `scripts/build_sec_bonds.py` — pulling it here directly would drop the
vault-note middle step and the staleness that comes with it.

**4. License Check (15 endpoints).**
`/v1/license-check/licensee/auditors` and `/auditingFirm` give the SEC-approved
auditor register. Join against the One Report `auditor_company_name_th` to flag
an issuer whose named auditor is not on the approved list, or whose approval
lapsed. `/licensee/{unique_id}/enforcement` covers licensed persons and firms —
not issuer enforcement.

**5. PVD (15) and Digital Asset (1) — nothing for IS1.**

## What this API does NOT give you

Do not plan around these — they stay on the existing scrapers:

- Daily SET prices, TA inputs → SETSMART (`build_daily_brief.py`)
- SET filing / disclosure feed → SET surveillance DB (`build_daily.py`)
- Form 59 / 246-2 insider reports → `market.sec.or.th` iDisc scrape, behind an
  F5 bot-defense WAF (`surveillance/external_sources.py`)
- Enforcement actions against issuers → same iDisc scrape
- MD&A and FS notes prose → the OneDrive vault

## Endpoint catalogue

### Bond — 6 endpoints

| Method | Path | What |
|---|---|---|
| GET | `/v2/bond/issuers` | Bond Issuer |
| GET | `/v2/bond/features` | Bond Feature |
| GET | `/v2/bond/credit-ratings` | Bond Credit Rating By Period |
| GET | `/v2/bond/outstanding-values` | Bond Outstanding Value By Period |
| GET | `/v2/bond/involve-parties` | Bond Involve Party By Period |
| GET | `/v2/bond/investor-holdings` | Bond Investor Holding by Investor Type |

### Digital Asset — 1 endpoints

| Method | Path | What |
|---|---|---|
| POST | `/v1/digital-asset/profile/intermediary` | Digital Asset Business Operator |

### Fund — 21 endpoints

| Method | Path | What |
|---|---|---|
| GET | `/v2/fund/general-info/amcs` | Asset Management Company : AMC |
| GET | `/v2/fund/general-info/profiles` | Fund Profile under AMC Management & General Information |
| GET | `/v2/fund/general-info/specifications` | Fund Specification |
| GET | `/v2/fund/general-info/mutual-fund-fees` | Mutual Fund Fee and Total Fee |
| GET | `/v2/fund/general-info/involve-parties` | Fund Involve Party |
| GET | `/v2/fund/factsheet/urls` | Fund Factsheet URL and PDF File |
| GET | `/v2/fund/factsheet/ipos` | IPO Offering Period |
| GET | `/v2/fund/factsheet/benchmarks` | Fund Benchmark |
| GET | `/v2/fund/factsheet/subscription-redemption-minimums` | Minimum Subscription, Redemption, and Balance Amounts and Units |
| GET | `/v2/fund/factsheet/subscription-redemption-periods` | Subscription and Redemption Dealing Periods and Settlement Times |
| GET | `/v2/fund/factsheet/risk-spectrum` | Fund Risk Spectrum |
| GET | `/v2/fund/factsheet/statistics` | Fund Statistics |
| GET | `/v2/fund/factsheet/dividend-policy` | Fund Dividend Policy |
| GET | `/v2/fund/factsheet/fees` | Fund Fee |
| GET | `/v2/fund/factsheet/performance` | Historical Fund Performance |
| GET | `/v2/fund/factsheet/asset-allocation` | Fund Asset Allocation |
| GET | `/v2/fund/factsheet/top5-holdings` | Top 5 Holding |
| GET | `/v2/fund/outstanding/portfolio` | Quarterly Fund Portfolio |
| GET | `/v2/fund/outstanding/portfolio-asset-type` | Monthly Fund Portfolio by Asset Type |
| GET | `/v2/fund/daily-info/nav` | Daily Fund NAV Information |
| GET | `/v2/fund/daily-info/dividend-history` | Fund Dividend History |

### License Check — 15 endpoints

| Method | Path | What |
|---|---|---|
| POST | `/v1/license-check/licensee/person` | Approved Person |
| GET | `/v1/license-check/licensee/company` | Licensed or Registered Juristic Person |
| POST | `/v1/license-check/licensee/company` | Licensed or Registered Juristic Person |
| GET | `/v1/license-check/licensee/person/{unique_id}/license` | Approved Person Approval Details |
| GET | `/v1/license-check/licensee/company/{unique_id}/personnel` | Personnel Role under Juristic Person |
| GET | `/v1/license-check/licensee/person/{unique_id}/work_info` | Personnel Role by Approved Person |
| GET | `/v1/license-check/licensee/company/{unique_id}/license` | Juristic Person License and Registration Types |
| GET | `/v1/license-check/licensee/company/{unique_id}/business_act` | Current Business Operations of Licensed Juristic Person |
| GET | `/v1/license-check/licensee/{unique_id}/enforcement` | Type of Violation and Enforcement Action for Approved Person and Licensed Juristic Person |
| GET | `/v1/license-check/licensee/{unique_id}/enforcement/{case_id}` | Enforcement Action Against Violation by Approved Person and Licensed Juristic Person |
| GET | `/v1/license-check/licensee/investoralert/alertdetail` | Investor Alert Information |
| GET | `/v1/license-check/licensee/investoralert/{case_id}/alertaction` | Investor Alert Misconduct Information |
| GET | `/v1/license-check/licensee/auditors` | Approved Auditor |
| GET | `/v1/license-check/licensee/auditingFirm` | Audit Firm |
| GET | `/v1/license-check/licensee/auditors/search/name/{person_name}` | Approved Auditor (Search by Auditor Name) |

### One Report — 23 endpoints

| Method | Path | What |
|---|---|---|
| GET | `/v1/one-report/sbo/{report_year}/info/{language}` | 01.ข้อมูลทั่วไปของบริษัท |
| GET | `/v1/one-report/sbo/{report_year}/rd/{unique_id}` | 02.ข้อมูลการวิจัยและพัฒนา (R&D) |
| GET | `/v1/one-report/sbo/{report_year}/product_income/{unique_id}` | 03.ข้อมูลโครงสร้างรายได้แบ่งตามกลุ่มธุรกิจ |
| GET | `/v1/one-report/sbo/{report_year}/export_income/{unique_id}` | 04.ข้อมูลโครงสร้างรายได้แบ่งตามรายได้จากต่างประเทศ |
| GET | `/v1/one-report/sbo/{report_year}/risk/{unique_id}` | 05.ข้อมูลรายละเอียดการบริหารจัดการความเสี่ยง |
| GET | `/v1/one-report/sustainability/{report_year}/detail/{unique_id}` | 06.ข้อมูลนโยบายและเป้าหมายการจัดการด้านความยั่งยืน |
| GET | `/v1/one-report/sustainability/{report_year}/environment_issue/{unique_id}` | 07.ข้อมูลด้านสิ่งแวดล้อม |
| GET | `/v1/one-report/sustainability/{report_year}/humanrights_issue/{unique_id}` | 08.ข้อมูลนโยบายสิทธิมนุษยชน |
| GET | `/v1/one-report/scp/{report_year}/employee_info/{unique_id}` | 09.ข้อมูลผลการดำเนินงานด้านความยั่งยืนทางสังคม - พนักงานและค่าตอบแทน |
| GET | `/v1/one-report/scp/{report_year}/employee_development/{unique_id}` | 10.ข้อมูลผลการดำเนินงานด้านความยั่งยืนทางสังคม - การฝึกอบรมและความปลอดภัย |
| GET | `/v1/one-report/scp/{report_year}/labor_dispute/{unique_id}` | 11.ข้อมูลผลการดำเนินงานด้านความยั่งยืนทางสังคม - ข้อพิพาทด้านแรงงาน |
| GET | `/v1/one-report/scp/{report_year}/csr_activity/{unique_id}` | 12.ข้อมูลผลการดำเนินงานด้านความยั่งยืนทางสังคม - CSR |
| GET | `/v1/one-report/cgp/{report_year}/governance/{unique_id}` | 13.ข้อมูลนโยบายการกำกับดูแลกิจการ |
| GET | `/v1/one-report/cgp/{report_year}/director/{unique_id}` | 14.ข้อมูลนโยบายและแนวปฏิบัติที่เกี่ยวกับคณะกรรมการ |
| GET | `/v1/one-report/cgp/{report_year}/code_of_conduct/{unique_id}` | 15.ข้อมูลจรรยาบรรณธุรกิจ |
| GET | `/v1/one-report/fs/{report_year}/financial_statement/{unique_id}` | 16.งบการเงินและอัตราส่วนทางการเงิน |
| GET | `/v1/one-report/cgs/{report_year}/board/{unique_id}` | 17.ข้อมูลองค์ประกอบของคณะกรรมการบริษัท |
| GET | `/v1/one-report/cgs/{report_year}/employee/{unique_id}` | 18.ข้อมูลเกี่ยวกับพนักงาน |
| GET | `/v1/one-report/cgs/{report_year}/auditor_company/{unique_id}` | 19.ข้อมูลบริษัทผู้สอบบัญชี |
| GET | `/v1/one-report/cgs/{report_year}/director_performance/{unique_id}` | 20.ข้อมูลการเข้าร่วมประชุมคณะกรรมการบริษัท |
| GET | `/v1/one-report/cgs/{report_year}/bods/{unique_id}` | 21.ข้อมูลคณะกรรมการ (Board of directors) |
| GET | `/v1/one-report/cgs/{report_year}/executives/{unique_id}` | 22.ข้อมูลผู้บริหาร |
| GET | `/v1/one-report/cgs/{report_year}/committees/{unique_id}/others` | 23.ข้อมูลคณะกรรมการอื่น ๆ ของบริษัท |

### PVD — 15 endpoints

| Method | Path | What |
|---|---|---|
| GET | `/v1/pvd/factsheet/amc` | Asset Management Company : AMC |
| GET | `/v1/pvd/factsheet/{unique_id}/fund` | Provident Fund under AMC Management & General Information |
| POST | `/v1/pvd/factsheet/fund` | Provident Fund under AMC Management & General Information |
| GET | `/v1/pvd/factsheet/{proj_id}/policy` | Provident Fund Policy |
| GET | `/v1/pvd/factsheet/{proj_id}/return` | Provident Fund Return |
| GET | `/v1/pvd/factsheet/{proj_id}/trailreturn` | Provident Fund Trail Return |
| GET | `/v1/pvd/factsheet/{proj_id}/fee` | Provident Fund Fee |
| GET | `/v1/pvd/factsheet/{proj_id}/PVDFullPort/{period}` | Provident Fund Asset Allocation |
| GET | `/v1/pvd/factsheet/{proj_id}/statistics` | Provident Fund Statistics |
| GET | `/v1/pvd/factsheet/{proj_id}/top5/assettype` | Provident Fund Top 5 Holding by Asset Type |
| GET | `/v1/pvd/factsheet/{proj_id}/top5/securities` | Provident Fund Top 5 Holding by Security |
| GET | `/v1/pvd/factsheet/{proj_id}/top5/foreign` | Provident Fund Top 5 Foreign Country Investment Allocation (based on direct investments only) |
| GET | `/v1/pvd/factsheet/{proj_id}/top5/industry` | Top 5 Industry Allocation for Provident Fund Equity Direct Investment |
| GET | `/v1/pvd/factsheet/{proj_id}/top5/issuer` | Top 5 Issuer Allocation for Provident Fund Direct Bond Investment |
| GET | `/v1/pvd/factsheet/{proj_id}/nav/{nav_date}` | Monthly Fund NAV Information |

## Scripts in this repo

```bash
export SEC_API_KEY=...

# validate the key against one v1 and one v2 endpoint
python3 scripts/sec_api.py ping

# raw probe
python3 scripts/sec_api.py get /v1/one-report/sbo/2024/info/T
python3 scripts/sec_api.py get /v2/fund/general-info/profiles --param project_info=FTREIT --page-size 5
python3 scripts/sec_api.py get /v2/bond/issuers --param search=CPN --all

# resolve ticker -> unique_id for the 232-ticker universe (1 call)
python3 scripts/build_sec_onereport.py --year 2024 --map-only

# build the snapshot (~930 calls for the default 4 datasets over 232 tickers)
python3 scripts/build_sec_onereport.py --year 2024
python3 scripts/build_sec_onereport.py --year 2024 --tickers CPN,WHA,ITC --datasets product_income,auditor
```

Output: `data/sec-onereport.json`, keyed by ticker, with `counts`,
`unresolved`, and `errors` at the top level so a partial pull is visible rather
than silent.

## Provenance and what is unverified

The endpoint catalogue below was reconstructed from an unofficial machine-readable
mirror of the portal catalogue
([Sitthinut/sec-open-data-api-spec](https://github.com/Sitthinut/sec-open-data-api-spec),
captured 2026-05-26), because the portal SPA and `api.sec.or.th` are both
blocked by this repo's cloud-session network policy.

**Nothing here has been executed against the live API.** Paths, parameter names
and response field names come from the mirrored catalogue, not from a response.

`scripts/probe_sec_api.py` settles all of it in one run, on a machine that can
reach `api.sec.or.th`:

```bash
export SEC_API_KEY=<primary>
python3 scripts/probe_sec_api.py              # rm=C book, 51 tickers, ~25 calls
python3 scripts/probe_sec_api.py --rm all     # full 232 universe
python3 scripts/probe_sec_api.py --json /tmp/sec-probe.json   # keep the evidence
```

Five rungs, each PASS / FAIL / WARN with the evidence printed under it:

| Rung | Question it settles |
|---|---|
| 1 KEY | Does the key work, on both the v1 and the v2 shape? Prints whether v1 returns a bare array or a wrapped `{items:[...]}`. |
| 2 YEAR | Which `report_year` actually has One Report data, and how many distinct symbols. Walks 2025 → 2021. |
| 3 COVERAGE | How many of the book resolve to a `unique_id` at that year, broken out by bucket. A PF&REIT miss is expected — funds and trusts do not file a One Report. |
| 4 PAYLOAD | Do `product_income`, `auditor`, `director_perf`, `board` and `financials` return rows for real tickers? Prints one concrete revenue line so the numbers are visible, not implied. |
| 5 PF/REIT | Do property funds (TTLPF, HPF, TIF1) and REITs (FTREIT, WHART, CPNREIT) resolve in `/v2/fund/general-info/profiles`? |

Exit 0 if no rung failed, 1 otherwise. Rung 3 is the one to read first: if
coverage of the PROP and FOOD buckets is not near 100%, the report year is
wrong before anything else is.
