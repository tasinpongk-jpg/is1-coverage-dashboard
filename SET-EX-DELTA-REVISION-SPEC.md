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

## 1. Corrected numbers (validated — use as-is)

| Metric | Deck (wrong) | Correct | Basis |
|---|---|---|---|
| DELTA weight | ~20% | **18.7% (~19%)** | 3.72tn / 19.92tn = 0.1867, as of 8 Jul 2026 |
| DELTA vs ADVANC+PTT+GULF | "~2×" | **~1.5× (1.5–1.6×)** | 18.67% / (5+4+3.5=12.5%) = 1.49× |
| Mechanical impact per 1% DELTA move | 0.11% (unlabelled) | **0.19% mechanical** (= 1% × 18.67%); keep 0.11% only if labelled **empirical/regression (H1 2026)** | separate the two explicitly |
| YTD | +88% | **VERIFY** vs SETSMART before use; state start date + method or drop | — |
| Constituent count | "930+ companies" | **Use exact SET Composite security count as of data date** | — |

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

## 4. WP1 — Daily-chain reconstruction (needs the raw data the user is providing)

Target script: `scripts/build_set_ex_delta.py`.

**Expected raw input** (per trading day, ~3yr, full SET Composite universe):
`date, symbol, close, listed_shares` → daily market cap per name; plus official published
`SET Composite index level` per day for validation.

**Algorithm**
1. Daily total market cap `MC_t = Σ (close × listed_shares)` over all constituents.
2. Ex-DELTA aggregate `MC_t^exD = MC_t − (DELTA close × DELTA shares)_t`.
3. Chain-link with continuity: on any constituent add/drop or share-count change, recompute the
   divisor so `index_after = index_before` (no jump from recomposition alone).
4. Emit validated daily series (CSV + JSON) + the 3-yr headline stat.

**Acceptance test (must pass before trusting ex-DELTA line):**
Reconstructed **SET Composite (incl. DELTA)** must track the official published index within a
tight tolerance (e.g. ≤ a few bp daily / negligible cumulative drift). If it doesn't, the ex-DELTA
line is not trustworthy — fix the chain before publishing any headline number.

---

## 5. Full review checklist (map every item)

- [ ] **Critical** — ex-DELTA daily chain rebuilt & validated (WP1 §4)
- [ ] **Critical** — BMV continuity wording (§2)
- [ ] **High** — DELTA weight → 18.7% (§1/§2)
- [ ] **High** — "~2×" → ~1.5× (§1/§2)
- [ ] **High** — mechanical 0.19% vs empirical 0.11% separated & labelled (§2)
- [ ] **High** — YTD +88% verified or dropped (§1)
- [ ] **Medium** — exact constituent/security count (§1)
- [ ] **Medium** — passive-fund claim softened (§2)
- [ ] **Medium** — informal references removed (§2)
- [ ] **Low** — slide numbering / agenda count (§2)
- [ ] Recommendation reframed to A/B/C transparency proposal (§3)

---

## 6. Division of labour

- **Claude (done):** this spec — validated numbers, exact EN/TH wording, reconstruction algorithm,
  acceptance test.
- **Executor / codex (pending assets):** WP1 script + run on provided raw data; WP2 apply wording
  edits to attached deck; WP3 reframe + repackage; tick §5 checklist.
