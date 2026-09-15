# IS1 Coverage Dashboard — Navigation Regrouping Brief

Audit date: 2026-09-15. Everything below was read out of this repo, not assumed.
If you change the codebase, update this file in the same commit.

**Scope of this brief: the top-level navigation grouping only.**
Not a redesign. No page layout, no body content, no palette change, no
component restyling. The twenty pages stay exactly as they are.

Paste §1–§2 into the design tool as the prompt. §3–§6 are the reference it
needs to stay inside what is actually buildable. §7 is the acceptance bar.

---

## §1 — THE PROMPT (paste this)

> I have an internal equity-surveillance dashboard used by six analysts at the
> Stock Exchange of Thailand, Issuer Department 1. Twenty pages covering 232
> listed companies. It works. I am not redesigning it.
>
> **The one thing I want fixed: the top-level navigation groups are not clear.**
> Today there are six groups — Workspace, Market, Companies, News flow,
> Surveillance, Bond data — and the boundaries between them do not match how
> anyone actually thinks about the work. "Surveillance" holds both price
> anomalies and governance data. "Bond data" is a whole top-level group for two
> pages. Nobody can predict which group a page lives in.
>
> The mental model I want the navigation to express is three kinds of question:
>
> 1. **ราคาและตลาด — price and market.** What moved, how it trades, what it is
>    worth.
> 2. **ข่าวและการเปิดเผยข้อมูล — news and disclosure.** What was announced,
>    filed, or reported.
> 3. **ข้อมูลบริษัท — company data.** What a company *is*: fundamentals,
>    governance, debt, meetings.
>
> Regroup all twenty pages against those three, design how the groups are
> presented, and tell me where you disagree with the three-way split.
>
> **Hard constraints:**
> - Bilingual EN/TH. Every group label needs both. Thai runs ~15% wider and
>   taller than English at the same size — no fixed-width labels, no
>   truncation on a group name.
> - The navigation is built at runtime from a single JavaScript array. You are
>   editing that array and the CSS that styles the shell. You are not editing
>   the twenty pages, so anything requiring per-page markup is out of scope.
> - Colours, fonts, spacing and components stay as they are. If a group's
>   accent colour has to change because groups merged, say so — but do not
>   propose a new palette.
> - Keep the existing shell behaviour: collapse toggle, ticker search with `/`
>   hotkey, RM selector, language toggle, theme switch, right context drawer,
>   mobile drawer under 840px.
>
> **Deliver:**
> - The full page-to-group mapping for all twenty pages, with a one-line
>   reason for every page you move.
> - The group labels in EN and TH, plus an icon choice per group from a
>   Lucide-style 24×24 stroke set.
> - A layout for how the groups are presented — see the open question below.
> - Annotated artboards at 1440px and at 390px.
>
> **The open question I want you to answer:** today the groups are a fixed 64px
> icon rail on the far left, with a 228px sidebar next to it listing that
> group's pages. With only three or four groups instead of six, is the icon
> rail still earning its 64px? Show me both — (a) keep the rail, (b) drop the
> rail and put the groups as a horizontal tab row in the existing 66px topbar,
> freeing 64px of horizontal space on every page. Recommend one and say why.
>
> **What I am not asking for:** a visual refresh, a new colour system, new page
> layouts, or anything that touches the content area of any page.

---

## §2 — The regrouping, as I would do it

Start from this and argue with it. Twenty pages; the "Now" column is the group
the page sits in today.

**ราคาและตลาด · Market & Price**
| Page | Now | Why here |
|---|---|---|
| `price-movement.html` | Market | unchanged |
| `sector-intelligence.html` | Market | unchanged |
| `multiples-comparison.html` | Market | unchanged |
| `multiples-band.html` | Market | unchanged |
| Daily market board (external) | Market | unchanged |
| `unusual-trading.html` | **Surveillance** | volume and price anomalies — this is price data, not a separate discipline |
| `trading-signs.html` | **Surveillance** | SP/NP/H trading status — how the stock trades |

**ข่าวและการเปิดเผยข้อมูล · News & Disclosure**
| Page | Now | Why here |
|---|---|---|
| `disclosure-pulse.html` | News flow | unchanged |
| `external-news.html` | News flow | unchanged |
| `efinance-news.html` | News flow | unchanged |
| Global-macro brief (external) | News flow | unchanged |
| `sec-enforcement.html` | **Surveillance** | an enforcement action is a published event — you read it like news |

**ข้อมูลบริษัท · Company Data**
| Page | Now | Why here |
|---|---|---|
| `company-summary.html` | Companies | unchanged |
| `oppday-minutes.html` | Companies | unchanged |
| `sec-form59.html` | Companies | unchanged |
| `governance-screen.html` | **Surveillance** | auditor fees, AGM timing, board independence — this is company attribute data |
| `bond-summary.html` | **Bond data** | a company's debt is company data; two pages do not need a top-level group |
| `bond-data-sec.html` | **Bond data** | same |

Net effect: Surveillance and Bond data disappear as groups, their six pages
redistributed. Nothing is removed from the product.

**The problem with a pure three-way split**, and you should push back on this:
three pages are neither price, news, nor company data — they are the analyst's
own workspace.

| Page | What it is |
|---|---|
| `index.html` | the morning overview — the landing page |
| `visits.html` | the RM's own visit planning |
| `ai-insights.html` | daily generated commentary across coverage |

Two ways to handle it:

- **A — three groups, no fourth.** `index.html` becomes the home link on the
  logo (it already is). `visits.html` and `ai-insights.html` move into the
  right-hand context drawer, which is already the analyst's personal panel.
  Purest three-way split; costs two pages some discoverability.
- **B — three groups plus a small "งานของฉัน · My desk".** Holds those three.
  The three content groups stay genuinely pure.

**I lean B.** The three content groups are only clear if nothing workflow-shaped
is stuffed into them, and a fourth group of three items is cheaper than
burying two pages in a drawer. Disagree if you see it differently.

## §3 — How the navigation is actually built

This is the part that makes the change cheap, and the part a designer will get
wrong if nobody says it.

**The entire navigation is generated at runtime from one array in `nav.js`.**
No page contains its own menu markup. Regrouping is a data edit.

`nav.js` line ~20, `GROUPS` — the whole menu:

```js
var GROUPS = [
  {
    id:"market", label:["Market","ตลาด"], icon:"chart-no-axes-combined", color:"#5d96ff",
    pages:[
      ["price-movement.html","Price movement","ความเคลื่อนไหวราคา","trending-up"],
      // [href, EN label, TH label, icon, optional count key]
    ],
  },
  // …five more groups
];
```

Each page entry is `[href, labelEn, labelTh, iconName]` with an optional fifth
element (`"filings"`, `"news"`, `"alerts"`) that renders a live count badge in
the sidebar.

Three couplings must move together, or the UI contradicts itself:

| # | Where | What it holds |
|---|---|---|
| 1 | `nav.js` → `GROUPS` | group id, EN/TH label, icon name, accent hex, page list |
| 2 | `nav.js` → `PAGE_META` | per-page header strip: `["Market","desc EN","desc TH","#5d96ff","icon"]`. **Field 0 is the group's display label** — if a page changes group, this changes too, or the page header names a group the menu no longer has. |
| 3 | `theme.css` lines 377–388 | `[data-module="<id>"] { --module-accent:… }`, twelve rules — six dark, six light. New group ids need new rules; removed ids leave dead ones. |

The accent hex is currently written in all three places. Worth collapsing to
one source while the file is open, but that is a cleanup, not the task.

Group ids are **not** persisted anywhere — `localStorage` holds only
`is1_rm`, `is1_shell_modules`, `is1_shell_context`, `is1_theme`. Renaming or
deleting a group id breaks no stored state.

Icons come from an `ICONS` lookup in `nav.js` (~30 entries, Lucide-style,
24×24 viewBox, `fill:none`, `stroke:currentColor`, `stroke-width:1.8`).
A new icon is a new path string in that table.

**Nothing above touches an HTML page.** Twenty pages, zero edits.

## §4 — The shell as it stands

| Surface | Size | Notes |
|---|---|---|
| Icon rail `.is1s-rail` | `--is1-rail-w: 64px`, fixed left, full height | one button per group; hard-coded `#0b0d10` ground in both themes |
| Module sidebar `.is1s-modules` | `--is1-module-w: 228px` | the selected group's page list, live counts, collapse toggle (persisted), freshness footer |
| Topbar `.is1s-topbar` | `66px`, sticky | breadcrumb, ticker search + `/` hotkey + datalist of all 232, RM selector, language toggle, theme switch, context toggle |
| Context drawer `.is1s-context` | `--is1-context-w: 310px`, right, slide-in | tabs: My book / Alerts / Agents |

Body padding is `calc(rail + module)` on the left, `310px` on the right when
the drawer is open. Under 840px both panels become scrim-backed drawers.

Option (b) in the open question — groups as topbar tabs — reclaims the 64px
rail on every page. The topbar is already crowded with six controls, so the
tab row probably needs its own 40px strip under the topbar rather than sitting
inside it. Worth showing both.

## §5 — The six groups today

| Group | Accent (dark / light) | Pages |
|---|---|---|
| Workspace · พื้นที่ทำงาน | `#f2aa1f` / `#965700` | index, visits, ai-insights |
| Market · ตลาด | `#5d96ff` / `#1f5fbd` | price-movement, sector-intelligence, multiples-comparison, multiples-band, daily board |
| Companies · บริษัท | `#35bdd0` / `#08798a` | company-summary, oppday-minutes, sec-form59 |
| News flow · ข่าวสาร | `#31c77b` / `#147947` | disclosure-pulse, external-news, efinance-news, macro brief |
| Surveillance · เฝ้าระวัง | `#ef6464` / `#bd3440` | unusual-trading, trading-signs, sec-enforcement, governance-screen |
| Bond data · ข้อมูลหุ้นกู้ | `#b17cff` / `#7039ae` | bond-summary, bond-data-sec |

Merging to three or four means three or four of these accents survive. Pick
from the existing six rather than introducing new hues — the pages themselves
carry these colours in their header strips via `PAGE_META`.

## §6 — Constraints the designer cannot see from a screenshot

- Static HTML/CSS/JS on Cloudflare Pages. No framework, no build step, no npm.
- Two external dashboards are embedded as full-bleed iframes with `?embedded=1`,
  which makes `nav.js` and `chat-dock.js` self-disable inside the frame. They
  must stay reachable from whatever navigation replaces the current one.
- A chat dock FAB sits bottom-right on every page and hides itself when a
  mobile nav drawer is open. A new nav must keep that interaction.
- Live count badges in the sidebar are fed by the daily JSON snapshots. If the
  new design drops the sidebar, those counts need somewhere to go.

## §7 — Acceptance

- [ ] All twenty pages mapped, every move justified in one line.
- [ ] EN and TH labels for every group, Thai checked at its rendered width.
- [ ] Both rail and topbar-tab options shown, one recommended with a reason.
- [ ] The three `nav.js`/`theme.css` couplings in §3 all accounted for.
- [ ] Zero changes proposed to any page's content area.
- [ ] Existing shell behaviours preserved: collapse, `/` search, RM selector,
      language toggle, theme switch, context drawer, 840px mobile drawers.
- [ ] Embedded workspaces and live count badges still have a home.
