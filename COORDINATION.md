# COORDINATION.md — Shared Task Board

**Repo:** `kanlerxz87-cyber/RentincreaseSF5`
**Project:** San Francisco rental-increase compliance research + public dashboard (SF Outer Sunset, ZIP 94122)
**This file is the single source of truth for who is doing what.** Update it *before* starting work and *after* finishing work, then commit.

---

## Session registry

| Session ID | Branch | Scope | Started (UTC) | Status |
|---|---|---|---|---|
| `SES-8b5ad092` | `arena/8b5ad092-rentincreasesf5` | All tasks T1–T10 (sole active session) | 2026-11-07 | active |

> **Branch convention for future sessions:** `session-<id>/<task>` from `main`. Never push to another session's branch.
> **Takeover rule:** if a claim is >60 minutes old with no commits, any other session may take the task over and must log the handoff here.

---

## Task board

| ID | Task | Files / scope (owner only) | Status | Owner |
|---|---|---|---|---|
| T1 | Scaffold repo, coordination board, README | `COORDINATION.md`, `README.md`, `.gitignore` | **done** | SES-8b5ad092 |
| T2 | Source register (official sources only) | `data/sources.json` | **done** | SES-8b5ad092 |
| T3 | Verified fact table (local / state / federal) | `data/facts.json` | **done** | SES-8b5ad092 |
| T4 | Rent-increase license + notice step-by-step process | `data/process.json` | **done** | SES-8b5ad092 |
| T5 | Unit 1 / Unit 2 calculations (arithmetic shown) | `data/units.json` | **done** | SES-8b5ad092 |
| T6 | Outer Sunset / ZIP 94122 market context (SF Open Data) | `data/market.json` | **done** | SES-8b5ad092 |
| T7 | Q&A: corporations vs individuals, notice, reasons, review, one-vs-both | `data/questions.json` | **done** | SES-8b5ad092 |
| T8 | Flagged-for-review register (unverified / conflicting) | `data/flagged.json` | **done** | SES-8b5ad092 |
| T9 | Executive summary (license question first) | `docs/executive-summary.html`, `EXECUTIVE-SUMMARY.md` | **done** | SES-8b5ad092 |
| T10 | Site build + integration, PR, merge, GitHub Pages deploy, link check | `build.py`, `docs/**`, `tools/check_links.py` | **done** | SES-8b5ad092 |

### Locked / shared files

`docs/index.html`, `docs/assets/*` and the nav are **shared outputs**. Only the final integration session edits them. In this run the same session performed integration (T10) after all data tasks were complete, so no cross-session conflict was possible.

---

## Claims log

| UTC time | Session | Action |
|---|---|---|
| 2026-11-07T20:05Z | SES-8b5ad092 | Read repo: empty except `README.md`; no prior `COORDINATION.md`. No other sessions detected. Claiming T1–T10 in a single non-overlapping scope. |
| 2026-11-07T20:05Z | SES-8b5ad092 | Confirmed GitHub auth OK; repo `isPrivate: false`; GitHub Pages already enabled (`main`, path `/`, `legacy` builder). Site will be moved to `main:/docs` at integration. |
| 2026-11-07T20:06Z | SES-8b5ad092 | Research pass started. Official sources only (`sf.gov` / Rent Board, `leginfo.legislature.ca.gov`, `hud.gov`, `data.sfgov.org`). |

---

## Verification record (per task)

### T2 — Source register
- 32 sources logged in `data/sources.json`. Every source is a government publisher: City and County of San Francisco (`sf.gov`, including Rent Board PDFs), California Legislative Information (`leginfo.legislature.ca.gov`), U.S. HUD (`hud.gov`, `huduser.gov`), SF Open Data (`data.sfgov.org`).
- Rejected as sources (not used for any verified row): law-firm blogs, property-management marketing pages, Reddit, calculator sites. They surfaced in search only.
- `huduser.gov` FY2026 FMR page loaded but rendered **no numeric FMR values** in this environment → no HUD dollar figure is published on the site. Logged in `data/flagged.json` (F-08).
- `api.census.gov` requires a key → no ACS figure published. Logged as F-09.

### T3 — Verified fact table
- 52 rows, each with a verbatim-checked requirement, an authority (statute / ordinance / agency page), and a source ID that resolves to a clickable official URL.
- Ordinance text verified against the Rent Board's bookmarked Chapter 37 PDF (Ord. 6-2-23): §37.3(a)(1) (60% of CPI, 7% cap), §37.3(a)(2) (banking), §37.3(a)(8) (petitions for anything above), §37.3(a)(11) (additional occupants), §37.3(b)(1)-(5) (notice content; nonconforming increase null and void), §37.10B, §37.15.
- Anything that could not be confirmed was left out of `facts.json` and moved to `flagged.json`.

### T4 — Process
- 11 steps, each mapped to the ordinance/agency instruction that requires it. Sequence verified: Housing Inventory → license (auto-generated) → calculation → 30/90-day notice → service.

### T5 — Unit calculations
- Arithmetic performed by `build.py` at build time from the official rate table (`S01`) — no hard-coded dollar results, so the numbers cannot drift from the rates.
- Two calculation inputs are owner-supplied and unverifiable from an official source (base rent history, build year) → flagged F-01, F-02.

### T6 — Market context
- Counts pulled live from SF Open Data dataset `gdc7-dmcn` (Rent Board Housing Inventory), 2026 submission year, `Sunset/Parkside` analysis neighbourhood, `Occupied by non-owner`. Query URLs recorded so any row can be re-run.
- `94122` is not a field in the dataset; `Sunset/Parkside` is the closest published geography → flagged F-04 (geography proxy).

### T7 — Q&A
- Each answer cites statute/agency text. Items that are judgement rather than law are labelled **Analysis** (not "verified") and cross-referenced to `flagged.json`.

### T8 — Flagged register
- 12 items. Includes one genuine internal conflict inside official guidance (24-month banking rule on `sf.gov` vs §37.3(a)(2) and the Rent Board's own worked examples) → F-03.

### T10 — Integration
- `build.py` renders all pages from `data/*.json`; `tools/check_links.py` verifies every internal link resolves and every external row has a URL.
- Link check result recorded in the deployment log below.

---

## Deployment log

| Step | Result |
|---|---|
| Branch | `arena/8b5ad092-rentincreasesf5` |
| Build (`python3 build.py`) | see `BUILD-REPORT.md` |
| Link check (`python3 tools/check_links.py`) | see `BUILD-REPORT.md` |
| Pull request | see `PR-LOG.md` |
| Merge | see `PR-LOG.md` |
| GitHub Pages | see `PR-LOG.md` |

---

## Irregularities found (full detail on the site's "Flagged for Review" page)

1. **F-03 (highest impact).** `sf.gov`'s "Banked rent increases" page says a skipped increase is only banked if **24 full months** pass without any rent increase. Ordinance §37.3(a)(2) says a landlord may accumulate a skipped increase and impose it on the tenant's **subsequent rent increase anniversary dates**, with no 24-month condition, and the Rent Board's own worked examples bank increases after **12 months**. This changes the answer for Unit 1. Flagged, both readings shown, Rent Board confirmation recommended.
2. **F-06.** Some third-party pages describe a "rent increase licence **application**". There is no application: the licence is generated automatically after the Housing Inventory report (`S05`, `S06`). The user's premise is right about the requirement but wrong about the mechanics.
3. **F-01 / F-02.** Build year (1940) and base-rent history are owner-supplied; not verifiable from an official source without the address. Both flagged, not asserted.
4. **F-04.** ZIP 94122 has no direct field in the Rent Board's public inventory; `Sunset/Parkside` used as the published proxy.

No merge blockers: flagged and unverified items are published on the Flagged for Review page with source links, per the project rule.
