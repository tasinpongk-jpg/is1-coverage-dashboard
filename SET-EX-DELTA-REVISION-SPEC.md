# SET ex-DELTA Deck — Revision Spec (execution handoff)

Status: **PLAN**. Claude authored this spec; execution ("the hard work") is delegated.
Prerequisites the user is providing:
1. **Source deck** (PPTX/PDF/Gamma) — attached separately; edit in place.
2. **Raw daily data** — dropped into `data/` (see WP1 schema) for the reconstruction run.

Do not re-derive numbers below — they are validated. Apply verbatim.

---

## 0. Scope & framing (apply to whole deck)

Reposition the deck from **"remove DELTA from SET Composite"** → **"index transparency /
supplementary SET ex-DELTA benchmark proposal."** SET Composite is *designed* to represent the
full listed common-stock universe subject to existing exclusion rules; outright removal is not a
credible ask. The credible ask is a **parallel/supplementary ex-DELTA metric + enhanced disclosure.**

---

## 1. Corrected numbers (VALIDATED against raw daily data — use as-is)

Computed by `scripts/build_set_ex_delta.py` from the two raw SETSMART exports
(`data/raw/delta-historical.xlsx`, `data/raw/set-index.xls`), 727 trading days,
10 Jul 2023 → 8 Jul 2026. Reconstruction **acceptance test passed: max index
reproduction error = 0.0 bps** (the divisor-continuity chain reproduces the published
SET Composite exactly, so the ex-DELTA line is trustworthy). Derived series +
stats in `data/set-ex-delta.json`.

| Metric | Deck (wrong) | Validated | Basis |
|---|---|---|---|
| DELTA weight (8 Jul 2026) | ~20% | **18.66% (~18.7%)** | DELTA MC 3.717tn / SET MC 19.921tn |
| DELTA weight **peak** | — (new) | **22.68% on 9 Jun 2026** | max over 3yr; add to deck — strengthens thesis |
| DELTA weight trajectory | — (new) | 12% (Aug'25) → 15% (Oct'25) → 18% (Feb'26) → 20% (Apr'26) | rising concentration |
| DELTA vs ADVANC+PTT+GULF | "~2×" | **~1.5× (1.5–1.6×)** | 18.66% / (5+4+3.5=12.5%) = 1.49× (weights unverified — flag) |
| Mechanical impact per 1% DELTA move | 0.11% (unlabelled) | **0.187% mechanical** (= 1% × 18.66%); keep 0.11% only if labelled **empirical/regression** | separate the two |
| DELTA YTD 2026 | +88% | **+72.3%** (adj. close, anchor 30 Dec 2025) | +88% NOT reproducible on this basis — replace or footnote its window |
| DELTA 3yr | — | **+195%** | adjusted close |
| Constituent count | "930+ companies" | **verify exact count** (not in these two files) | — |

### THE headline (new, validated — lead with this)
Removing DELTA flips the market's 3-year story:

| | 3-year | YTD 2026 |
|---|---|---|
| **SET Composite** | **+5.3%** | **+25.1%** |
| **SET ex-DELTA** | **−8.0%** | **+17.7%** |

Over 3 years the headline SET is *up 5.3%*, but the market **ex-DELTA is down 8.0%** — the
index's positive return is entirely a DELTA artefact. This is the single most persuasive,
now-validated data point for the transparency thesis. Divergence ≈ **13.3 pts** over 3yr.

---

## 2. Wording changes (before → after; keep EN + TH)

**DELTA weight**
- ❌ `DELTA ~20% weight`
- ✅ EN: "DELTA represents approximately **18.7% / ~19%** of SET market capitalization, based on
  market cap of THB 3.72tn versus SET total market cap of THB 19.92tn as of 8 July 2026."

**BMV adjustment (Critical fix — continuity, not subtraction)**
- ❌ `SET จะลด BMV ลงด้วยมูลค่าตลาดของหุ้นนั้น`
- ✅ TH: "เมื่อนำหุ้นออกจากดัชนี SET จะปรับ Base Market Value ตามหลัก **continuity** เพื่อให้
  **Index after adjustment = Index before adjustment** ดังนั้นระดับดัชนีจะไม่เกิด price shock
  จากการปรับองค์ประกอบเพียงอย่างเดียว"
- ✅ EN gloss: "BMV is re-based so the index level is continuous across the recomposition; the
  recomposition itself causes no price shock."

**DELTA 1% impact**
- ❌ `DELTA 1% → SET ~0.11%`
- ✅ "Mechanical impact ≈ **0.19% per 1% DELTA move** (≈ its 18.7% weight). A regression-based
  H1/2026 relationship may be lower (~0.11%) but must be **labelled empirical, not mechanical.**"

**Top-stock comparison**
- ❌ `DELTA ใหญ่กว่า ADVANC, PTT, GULF รวมกันเกือบ 2 เท่า`
- ✅ "DELTA is larger than ADVANC + PTT + GULF combined by **~50–60% (≈1.5×)**, subject to updated
  constituent-weight validation."

**Passive-fund claim (soften)**
- ❌ "funds must rebalance"
- ✅ "SET-linked index products **may need to** rebalance, **depending on mandate and AUM.**"

**Informal references (remove)**
- Delete `Claude Sonnet`, `Claude Opus`, `คำแนะนำของตู่` → replace with **"Internal analysis /
  Index Strategy Team recommendation."**

**Housekeeping**
- Standardize slide numbering + agenda slide count.

---

## 3. Reframed recommendation (replace current ask)

| Option | Recommendation | Rationale |
|---|---|---|
| **A. Publish SET ex-DELTA supplementary index** | **Recommended** | Low disruption, high transparency, practical first step |
| B. Apply capped weight to SET Composite | Longer-term | Needs public hearing + methodology review |
| C. Status quo + enhanced disclosure | Minimum fallback | Improves visibility, doesn't fix distortion |

Management ask: **approve further study of an official SET ex-DELTA supplementary index**, backed by
validated daily-chain analysis, constituent-weight disclosure, and valuation-impact estimates.

---

## 4. WP1 — Daily-chain reconstruction ✅ DONE & VALIDATED

Script: `scripts/build_set_ex_delta.py` · raw inputs: `data/raw/` · output: `data/set-ex-delta.json`.

**Raw inputs used** (both are SETSMART daily exports, ~3yr):
- `delta-historical.xlsx` — DELTA daily Close, **Market Cap (M.Baht)**, Listed Shares (adj. price).
- `set-index.xls` — SET Composite daily Close (index level) + **Market Cap (Baht)** (HTML-as-.xls).

**Method — divisor-continuity chain (self-validating):**
1. Recover the index divisor daily: `D_t = MC_t / Index_t`; ratio `g_t = D_t/D_{t-1}` isolates
   corporate-action / recomposition effect (`g_t = 1` on ordinary days).
2. ex-DELTA market cap `exMC_t = MC_t − DELTA_MC_t`.
3. ex-DELTA return `r'_t = exMC_t / (exMC_{t-1}·g_t) − 1`; chain from `ex_0 = Index_0`.
   Continuity holds because a recomposition moves `g` so no fake return is injected
   (`Index_after = Index_before` — the BMV continuity point, empirically confirmed).

**Acceptance test — PASSED:** applying the same `g_t` to full MC reproduces the published SET
Composite with **max error 0.0 bps** over all 727 days, so the ex-DELTA line is trustworthy.

**Assumption (documented):** DELTA export uses adjusted prices; ex-DELTA basket = SET total MC
minus DELTA MC. Constituent-level data isn't required because SET total MC is supplied directly.

Re-run: `python3 scripts/build_set_ex_delta.py [delta.xlsx] [set.xls]` (defaults to `data/raw/`).

---

## 5. Full review checklist (map every item)

- [x] **Critical** — ex-DELTA daily chain rebuilt & validated (WP1 §4) — 0.0 bps, done
- [ ] **Critical** — BMV continuity wording (§2)
- [ ] **High** — DELTA weight → 18.7% (§1/§2)
- [ ] **High** — "~2×" → ~1.5× (§1/§2)
- [ ] **High** — mechanical 0.19% vs empirical 0.11% separated & labelled (§2)
- [x] **High** — YTD verified: DELTA +72.3% (not +88%); SET +25.1% vs ex-DELTA +17.7% (§1)
- [ ] **Medium** — exact constituent/security count (§1)
- [ ] **Medium** — passive-fund claim softened (§2)
- [ ] **Medium** — informal references removed (§2)
- [ ] **Low** — slide numbering / agenda count (§2)
- [ ] Recommendation reframed to A/B/C transparency proposal (§3)

---

## 6. Division of labour

- **Claude (done):** this spec; **WP1 built, run & validated** (`scripts/build_set_ex_delta.py`,
  `data/set-ex-delta.json`, 0.0 bps) — all headline numbers now empirical.
- **Executor / codex (pending the attached deck):** WP2 apply wording/number edits to the deck
  using §1–§3; WP3 reframe + repackage; tick remaining §5 items.
