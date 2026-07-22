# Training the IS1 Dashboard Agents — Method, Techniques & Results

How four grounded chat agents on the IS1 coverage dashboard were made accurate,
honest, and measurable — without fine-tuning. Written as a reusable playbook.

---

## 1. The system

Every dashboard page carries a chat dock talking to four named agents
(`worker.js`, Cloudflare Worker):

| Agent | Job | Model |
|---|---|---|
| 🗺 **Atlas** | prices, % moves, movers, threshold checks | MiniMax M3 |
| ⚡ **Hermes** | external news + SET disclosures, silent filers, filing summaries | MiniMax M3 (+ Gemini for PDFs) |
| 🔮 **Pythia** | sector aggregates + daily AI commentary | MiniMax M3 |
| ⚖️ **Lex** | SET/SEC rules, cited to the source PDF | MiniMax M3 + local page retrieval |

Each is grounded in the same daily JSON snapshots the dashboard shows, so the
chat never diverges from the pages.

## 2. The core thesis

**No application-specific fine-tune is configured. So "training" = prompt +
context + evaluation engineering.** The single highest-leverage principle we
proved over and over:

> **Move structured work out of the model and into deterministic code.** A model
> is not the authority for filtering, counting, sorting, and date math. Every time we did
> those *for* it — handing it a pre-filtered, pre-sorted, scoped context — answer
> quality jumped. Every time we relied on a prompt rule alone, it eventually
> failed.

The model's job shrinks to **narrating a context that is already correct.**

## 3. Techniques applied (in order of leverage)

### 3.1 Deterministic context filtering (biggest win)
The model never sees a 230-row list it must filter. The worker parses the query
into a structured intent and filters the context server-side:

- **Ticker focus** — a covered symbol in the query → news/filings/prices scoped to
  *only* that name (so "news on CPN" can't pad with other tickers; an empty
  section truthfully means "none").
- **Price screens** (`parsePriceQuery`) — `threshold` ("beyond ±2%"), `range`
  ("between −2% and −1.5%"), `top-N` ("top 5 by YTD", "worst 3") over a chosen
  metric (1d/5d/YTD/volume). Rows are hard-filtered & sorted; the model lists
  only what survives. **This fixed the flagship failure** where the model listed
  sub-threshold names as "movers."
- **Sector scope** (`parseSector`) — a named sector scopes prices/news/filings.
- **Recency** (`parseRecency`) — "today / this week / last N days" date-filters
  news & filings (the worker does the date math, not the model).
- **RM ownership** — strict per-RM slicing so "my coverage" never leaks another
  RM's names.

### 3.2 Retrieval quality
- **Rank-then-cap** (`relevanceRank`) — topical keywords re-rank news/filings so a
  relevant item *beyond* the recency cap still surfaces, instead of the model
  hunting through recency-ordered noise.
- **Lex page retrieval** (`retrieveLexChunks`) — `build_lex_corpus.py` extracts
  all rulebook PDFs page by page, records each source hash, and builds one
  deployable JSON asset. The worker expands Thai/English rule aliases, scores
  title and page text deterministically, caps pages per document, then sends
  only the selected pages to MiniMax M3. A source list is appended in code.

### 3.3 Route PDF tasks to a PDF-capable model
- **Hermes filing summaries → Gemini.** A "summarize CPN's filing" request reads
  the *actual filed PDF*: the worker resolves the SET newsdetails page → the
  `weblink.set.or.th` PDF → hands the bytes to Gemini (which reads PDFs natively,
  no JS parser) → returns the summary **directly, bypassing MiniMax** (the chat
  path mangled injected summaries). Cached by news-id + language.

### 3.4 Persona engineering + few-shot
Each persona has explicit rules **plus one worked example** — few-shot locks in
format far better than rules alone. Shared rules enforce: tickers-only
(never hallucinate company names; the data has no name field), strict threshold
math ("−1.93 is NOT beyond −2"), RM-scoping, reply in the user's language.

### 3.5 Output verification (catch the model when it's still wrong)
After every reply, a deterministic pass checks **every covered ticker the model
named was actually in the context it was given.** Ungrounded names (pretraining
leaks / cross-contamination) get a visible `⚠ Unverified` flag before the user —
and before the dock turns them into clickable ticker chips.

### 3.6 Real-time data (close capability gaps)
Atlas used to *refuse* all intraday questions (snapshot is previous-close). Now an
explicit live-price ask fetches a real-time Yahoo Finance quote for the named
symbol and answers from it, flagged as live with the quote time. Fails soft to the
snapshot if the fetch is blocked.

### 3.7 Measurement loop
- **Eval harness** (`scripts/eval_agents.mjs`) — fires a fixed battery at the live
  worker and runs property checks per agent (no sub-threshold rows; both news
  sections present; figures + breadth; cited rule; off-topic refusal). Exit code =
  failures.
- **LLM-judge** (`--judge`) — an independent model (Groq, a *different* family than
  MiniMax M3 under test) grades each reply 0–100 on directness/specificity/
  consistency/role. `--gate N` blocks a deploy if the mean drops below N.

### 3.8 Feedback loop
- Dock **👍/👎** on every reply → `POST /api/feedback` → durable **KV**.
- `scripts/mine_feedback.mjs` pulls the votes (`GET /api/feedback`), reports the
  positive-rate + per-agent breakdown, lists the 👎s, and with `--themes` clusters
  them into recurring failure modes via Groq. Downvotes become the next eval cases
  / few-shots — improvement driven by real questions, not guesses.

## 4. Failure-and-fix log (what the rigor looked like)

Real bugs found by **live-testing the deployed model**, not assuming:

| Symptom | Root cause | Fix |
|---|---|---|
| "Movers beyond ±2%" listed +0.9%, +1.7% names | A chat model should not own numeric filtering | Parse threshold; hard-filter rows server-side |
| Range query output was a garbled table | model free-handing a 2-sided numeric filter | `range` mode in `parsePriceQuery` |
| Atlas said company names, not tickers | data has **no** name field → model guessed from pretraining | "tickers-only, never names" rule + grounding check |
| "News on CPN" showed J/TIF1/BLAND filings | model padded an empty section | ticker-focus filters context; empty ⇒ honest "none" |
| Filing summaries were a generic half-sentence | The chat path did not faithfully reproduce injected text | bypass the chat model; serve Gemini's summary directly |
| Gemini summaries truncated to "…filed" | `gemini-2.5-flash` is a **thinking model**; thinking tokens ate the `maxOutputTokens` budget | `thinkingConfig.thinkingBudget=0` + bigger cap |
| Lex failed in production without a Gemini secret | its only retrieval/generation path depended on Gemini File Search | build a page-level corpus locally; retrieve in the Worker; answer through the existing MiniMax M3 secret |
| Lex returned an empty Thai free-float answer | MiniMax reasoning consumed the default 2,200-token output budget | use a Lex-specific 5,000-token budget and constrain the final answer to 350 words |
| A normal Hermes sample intermittently returned an empty answer | MiniMax can spend the whole output budget on reasoning for any agent | retry empty-only responses once at 5,000 tokens; Lex retries at 8,000 |
| Thai user got an English cached summary | cache key ignored language | key includes `lang` |
| A passing test silently broke | persona text contained the literal string a test split on (`SET DISCLOSURES`, `FILED-DOCUMENT…`) | anchor tests on data-only markers |
| Feedback verification looked broken for ~40 min | the deploy CLI's KV reads were an unreliable narrator (sandbox/consistency); data was always landing | confirmed in dashboard + via the worker's own export endpoint |

**Lesson:** prompt rules are necessary but not sufficient; the model must be
*verified against ground truth*, and the verification itself must be trusted.

## 5. Generalizable principles

1. **Determinism beats prompting** for filtering/counting/sorting/dates — parse
   the intent, compute the answer, let the model narrate.
2. **Route by capability** — use deterministic retrieval for static rulebooks;
   send binary PDFs to a model that can read them natively.
3. **Make "none" first-class** — scoping + honest empty sections kill the model's
   urge to pad/fabricate.
4. **Verify the output, not just the input** — a grounding check catches the last
   class of hallucination after the context is already clean.
5. **Measure or it didn't happen** — property checks + an independent LLM-judge +
   a deploy gate turn "feels better" into a number.
6. **Close the loop** — capture 👍/👎 from real use and feed the 👎s back as evals.
7. **Test on the deployed model, live** — most real bugs (thinking-budget
   truncation, padding, name hallucination) are invisible to unit tests.

## 6. Results

- All 13 suggestion-chip questions across the 4 agents are covered by the live
  eval harness; the latest MiniMax M3 run passed **49/49** property checks.
- Lex indexes 79 source PDFs into 560 page records and 561 retrieval chunks;
  all 3 Lex suggestion questions return page citations through MiniMax M3.
- Atlas threshold/range/top-N now deterministically correct; intraday answered.
- Hermes merges both news sources, scopes per-ticker, summarizes real PDFs
  (verified rich numeric output in EN + TH).
- 42 unit tests cover theme assets, chat routing, empty-answer recovery, source retrieval, citation
  validation and deterministic context logic.
- Measurement (eval + judge + gate) and feedback (votes + miner) loops in place.

## 7. Operating it

```bash
python3 scripts/build_lex_corpus.py /path/to/regulations
node scripts/eval_agents.mjs --judge --gate 80   # measure before/after a change
node scripts/mine_feedback.mjs --themes          # see what real users downvoted
```

Pointers: agent logic lives in `worker.js`; deterministic context logic is unit-
tested in `tests/worker.test.mjs`; the SET-PDF recipe + data contract with the
local CLI are in [INTEGRATION.md](INTEGRATION.md).
