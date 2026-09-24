# Integration contract — IS1 dashboard ⇄ "AI Agent" CLI

Single source of truth for what the **is1-coverage-dashboard** (this repo, the
deployed product) and the **AI Agent** CLI (`~/VSCoder/AI Agent`, a private local
workbench) share. They are **separate repos on purpose** and must stay that way:

- the dashboard is multi-user and cloud-deployed (Cloudflare Worker + static
  site) — it must stay deployable with **no dependency** on the local Python CLI;
- the CLI is single-user and private — its `@clio` scribe is **forced local-only**
  so client data never leaves the Mac. Merging would couple a public deploy to a
  private workbench and put client-sensitive code beside a shared-token service.

They share **data and recipes, not code**. When you change anything below, update
this file and check the *other* implementation against it. (Repos are assumed to
be siblings under `~/VSCoder`; cross-links use relative paths.)

## 1. Data contract

**Dashboard → CLI.** The daily CI publishes JSON snapshots under
[`data/`](data/); the CLI's `is1_tools.py` reads them (freshest first: GitHub
repo → live Worker → local clone). Key snapshots and their consumers:

| Snapshot | Produced by | Consumed by |
|---|---|---|
| `tickers.json` | build pipeline | `is1_ticker`, RM/sector ownership everywhere |
| `morning-brief.json` | build pipeline | `is1_movers`, Atlas prices |
| `disclosure-pulse.json` | `surveillance/` | `is1_filings`, Hermes (each filing carries `url`, `_id`, `severity`) |
| `external-news.json` | `scripts/build_external.py` | Hermes news |
| `unusual-trading.json` | build pipeline | `is1_alerts`, Atlas alerts |
| `oppday-minutes.json`, `ai-insights.json`, `sector-heatmap.json` | build pipeline | Pythia, briefs |

**CLI → Dashboard.** `vault_visits.py export` writes
[`data/visits.json`](data/visits.json), which feeds the **Visit Planner** page
(`visits.html`). This is the only artifact the CLI pushes back.

If a snapshot's field names change, both the producer (here) and `is1_tools.py`
must change together.

## 2. SET PDF-resolution recipe

The private CLI turns a filing into a readable document with this canonical
recipe. The dashboard Worker does not download or summarize binary PDFs; Hermes
uses the deployed filing metadata and must not claim to have read the document.

1. Each filing's `url` is a SET **newsdetails** page
   (`www.set.or.th/.../newsdetails?id=…&symbol=…`).
2. **GET that page with a browser `User-Agent` + `Referer` header.** The
   newsdetails HTML and the `weblink.set.or.th` PDF host accept plain
   header-only fetches — **only the `/api/` endpoints are Incapsula/Cloudflare-
   strict** (a bare `/api/set/news/{id}` returns a bot wall). This holds even
   from Cloudflare Worker egress.
3. Regex the attached PDF link: `https?://weblink\.set\.or\.th/[^\s"'<>]+\.pdf`
   — take the first match (there is normally one).
4. Download the PDF (no cookies needed) → summarize.

Runtime-specific behavior:

| | CLI (`filing_tools.py`) | Worker (`worker.js`) |
|---|---|---|
| Extract | `pypdf` → raw text, then a Groq summary | none; filing title, date and classification only |
| Gotcha | scanned PDFs yield no text | a request for document detail can only be answered to metadata depth |
| Cache / store | auto-archives full text to local SQLite (`notes/agent.db`) | daily JSON snapshots deployed as static assets |

## 3. Agents — cloud cousins, not clones

| Concept | Dashboard (MiniMax M3 + verified calculators) | CLI (`agents/*.json`, tool-calling) |
|---|---|---|
| Hermes | snapshot-grounded; merges external news + SET disclosure metadata | live `web_search` + `read_filing`; news sweeps |
| Atlas | snapshot prices; server-side threshold pre-filter | live `get_stock_quote` + `calculator` |
| Pythia | deterministic sector performance, breadth and ranking screens | (no CLI cousin) |
| Lex | deterministic page retrieval over `lex-regulations.json`, then MiniMax M3 | (no CLI cousin) |
| Clio | — (stays local for privacy) | private client-reply drafter, forced `local` |

**One genuinely shared rule** (keep identical in both): strict threshold math —
*"-1.93 is NOT beyond -2"* (dashboard `SHARED_RULES`; CLI `agents/atlas.json`).
Other dashboard rules (tickers-only-never-names, always-both-news-sections) are
**dashboard-specific** because its data is name-less pre-computed snapshots; the
CLI has live tools, so it legitimately differs. Don't force those onto the CLI.

## 4. Shared secret

The CLI's `IS1_CHAT_TOKEN` (`AI Agent/.env`) is the same value as the `CHAT_TOKEN`
Worker secret here. Used to hit `POST /api/chat` on the deployed Worker. Never
commit it.
