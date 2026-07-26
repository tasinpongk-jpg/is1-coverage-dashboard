# Scale IS1 Coverage Dashboard to 900 tickers / 60 RMs

## Context

The IS1 Coverage Dashboard currently tracks **232 SET tickers across 6 RMs and 6 sectors**.
A daily GitHub Actions pipeline (`.github/workflows/daily.yml`) polls SET disclosures, scans
every ticker against the SETSMART API, builds 4 JSON snapshots, emails per-RM briefs, and
deploys to Cloudflare. The goal is to expand coverage to the **full SET + MAI universe
(~900 tickers) under 60 RMs**, generalize the 6-sector model to the full SET taxonomy
(~28 sectors), switch email delivery from per-RM to **team-based (6 teams, 6 group inboxes)**,
and **remove the two manual-input pages (Opp Day, Visits)** so the dashboard runs itself daily
with no human data entry.

### Decisions (confirmed)
- **SETSMART throughput:** higher API tier available → raise concurrency via env, don't re-architect.
- **Email:** team-based. 6 teams, each with one group email; each team email contains the per-RM
  sections for every RM on that team (longer content). 60 RMs → 6 emails.
- **Sectors:** generalize to the full SET taxonomy, driven dynamically from `tickers.json`.
- **Pages:** remove **both** Opp Day and Visits.

### Inputs needed during implementation
- The 900-ticker Excel (`IS1 Port Summary.xlsx` equivalent) with columns **Company, Sector,
  RM Name, Team** (Team is a new 4th column).
- The 6 team → group-email-address mapping (for `TEAM_EMAIL_TO`).
- The real SETSMART concurrency ceiling for the tier.

---

## Work breakdown

### 1. Data model: add `team`, generalize sectors, unify the second source of truth
**`scripts/build_tickers.py`** — turns the Excel into `data/tickers.json`.
- Read a new **`Team`** column (`row[3]`); add `"team"` to each ticker row (guard missing col).
- Emit a normalized **`sectorKey`** per row (strip `&`/spaces, e.g. `PF&REIT`→`PFREIT`) alongside the
  display `sector`, so CSS/class names never contain `&`. Drop the lossy 6-entry `SECTOR_BUCKET`
  (keep only normalization) so all ~28 SET sectors pass through.
- Add to the payload: `"teams"`, `"rm_team": {rm: team}`, and `totals.by_team`.

**`surveillance/coverage.py` + `surveillance/alerts.py`** — *critical hidden coupling.* The
surveillance pipeline does **not** read `tickers.json`: `_sector_lookup()` imports the static 232-name
`COVERAGE` dict in `coverage.py`, and `_rm_lookup()` reads `rm_db/rm.duckdb`. At 900 names these go
stale and surveillance ignores new tickers. Repoint both to read `data/tickers.json` (add
`_team_lookup()` while there). Unifies on one source of truth.

### 2. SETSMART scaling + workflow timeouts
**`.github/workflows/daily.yml`** — set `SETSMART_MAX_CONCURRENT` / `SET_MAX_CONCURRENT` to
tier-appropriate values (env already plumbed through `scripts/setsmart_proxy.py:74`,
`scripts/build_ticker_summary.py:37,42`), lower `SET_THROTTLE_S` if the tier allows, and raise the
**build job `timeout-minutes: 30`** (line 174) — the scan grows ~4x at 900 tickers. No proxy code
change; concurrency is fully env-driven. Keep the `SETSMART API probe` step (fails fast).

### 3. Team-based email routing
**`scripts/build_morning_push.py`** (morning brief):
- Delete hardcoded `RMS` (line 39); derive `RMS` and `RM_TEAM` from `tickers.json` via `_read()`.
  Drop the static `choices=RMS` on `--rm`.
- Refactor `render()` to take an RM subset so a team body = concatenated RM sections for that team.
- In `send()`, parse a new env var **`TEAM_EMAIL_TO="Team1:addr1,Team2:addr2,..."`** (reuse the
  `BRIEF_EMAIL_TO` `split(":",1)` idiom), loop teams, send one email per team to its address
  (fallback `EMAIL_TO`); team name in the subject. Loop the Groq "AI take" call **per team** (a single
  call would blow context/timeout at 60 RMs).

**`surveillance/alerts.py` + `surveillance/route_alerts.py`** (critical + digest alerts):
- `alerts.py`: add `_team_lookup()` and `_team_addresses()` (parse `TEAM_EMAIL_TO`); add an optional
  `to_addr` param to `EmailClient.send()` (`to_addr or self.to_addr`) to target a team inbox.
- Change `format_critical_digest()` and the digest grouping in `route_alerts.py:_send_digest()` from
  group-**by-RM** to group-**by-team**, keeping RM as a sub-heading inside each team block; send each
  team's chunk to its team address.
- Replace the hardcoded `"📌 Champ — Issuer Department 1, SET"` signature (`route_alerts.py:47,91`)
  with a generic department signature (optional per-team override).
- Replace the legacy 3-sector `SECTOR_ORDER` (`alerts.py:326`) with a fuller/derived order (cosmetic).

### 4. Frontend sector generalization (6 → ~28)
Already dynamic (no change): `price-movement.html` sector/RM tabs, `index.html` counts,
`build_daily.py:_rebuild_sector_agg` (aggregates arbitrary sectors). What must change:
- **Shared util:** add `window.sectorColor(name)` to `nav.js` (loaded everywhere) — deterministic HSL
  hash with the legacy 6 as fixed overrides. Replace each page's local `SECTOR_COLOR` / `SCOL` /
  `SECT_ORDER` maps and reliance on `.s-FOOD`-style CSS with this util + inline styles. Pages:
  `index.html` (`SECTOR_COLOR`/`sectorOrder` ~720,807), `multiples-comparison.html` (`SCOL` ~104),
  `multiples-band.html` (`SCOL`/`SECT_ORDER` ~104-105 — **functional**: box plots iterate `SECT_ORDER`
  so today only the 6 show), `company-summary.html`, `price-movement.html`.
- **`build_daily.py`:** drop the 6-entry `sector_map` (lines 46-47) and hardcoded order in
  `_rebuild_sector_agg` (line 138); rely on normalized sectors from `tickers.json`.
- **`scripts/setsmart_proxy.py:963`** (`for sector in ["FOOD","PROP","PFREIT"]`) — dead in the
  `build_daily` path but fix to derive sectors from rows so the standalone path agrees (low priority).

### 5. Remove Opp Day + Visits
- **Delete:** `oppday-minutes.html`, `visits.html`, `data/oppday-minutes.json`, `data/visits.json`,
  `scripts/build_oppday_minutes.py`, `scripts/clean_oppday.py`, `scripts/run_oppday_refresh.bat`.
- **`nav.js`:** remove `oppday-minutes.html` from the News group (line 33) + its `META` (line 71);
  remove the entire **Visits** group (lines 53-58) + the `visits.html` `META` (line 78).
- **`index.html`:** remove the Oppday card + any Hermes copy referencing oppday.
- **`company-summary.html`:** remove the "Opp Day" tab (`data-tab="oppday"`) and its data loading.
- **`worker.js`:** remove oppday from Hermes grounding (`loadJson(... "oppday-minutes")` near line 245).
- **`chat-dock.js`:** remove `"oppday-minutes"` from the Hermes `data:` list (line 26).
- Confirm `scripts/ingest_synthesis.py` / `build_company_reports.py` oppday references are offline-only
  (not invoked by `daily.yml` — they aren't); leave or clean as desired.

### 6. Prompt + doc cleanup (accuracy, not blocking)
- `surveillance/classifier.py:51` SYSTEM_PROMPT ("50 listed names … FOOD, PROP, PFREIT") → describe the
  full SET+MAI universe generically.
- `worker.js` (~289,330,369-382) and `chat-dock.js` (RM list line 66; sector chips ~31,50) → load RM
  list from `tickers.json`, generalize sector mentions.
- `README.md` / `SYSTEM.md` → update the 232/6 counts and RM names.

---

## Suggested sequencing
1. `build_tickers.py` (team + normalized sectorKey + teams/rm_team/by_team) → regenerate `tickers.json`.
2. Unify surveillance source of truth (`coverage.py`/`alerts.py` read `tickers.json`).
3. Email: `alerts.py` → `route_alerts.py` → `build_morning_push.py` (team grouping + `TEAM_EMAIL_TO`).
4. Frontend: `sectorColor()` util in `nav.js`; swap per-page maps; fix `multiples-band` order.
5. Remove Opp Day + Visits.
6. SETSMART concurrency + timeouts in `daily.yml`.
7. Prompt/doc cleanup.

## Verification
- **Data:** `python scripts/build_tickers.py <new.xlsx>`; assert ~900 tickers, 60 RMs, 6 teams,
  `rm_team` covers every RM, sectors ≈ full SET taxonomy, no `&` in any `sectorKey`.
- **Email (no send):** `build_morning_push.py --dry-run` / `--team <T>` → exactly 6 team bodies, each
  with only its team's RM sections; `route_alerts.py --mode both --dry-run` → grouped by team with
  per-RM sub-blocks and correct `to_addr`.
- **Build:** `python scripts/build_daily.py` against the 900-ticker `tickers.json` (higher
  `SETSMART_MAX_CONCURRENT`); all 4 JSONs build, `sector-heatmap.json.sectorAgg` lists all present
  sectors, wall-clock fits inside the raised timeout.
- **Frontend:** open `index.html`, `price-movement.html`, `multiples-band.html`, `sector-heatmap.html`
  locally; all ~28 sectors render with distinct colors; RM/team filters populate from data.
- **Removal:** grep for `oppday`/`visits` → only expected offline residue; each remaining page loads with
  no Opp Day/Visits nav and no console errors.
- **CI dry run:** trigger `daily.yml` via `workflow_dispatch` on the feature branch (won't push from a
  non-main ref); confirm the build job completes within the new timeout.
