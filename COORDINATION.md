# COORDINATION — Shared Task Board

This file is the shared task board for all agent sessions working in this repository.
Protocol: claim a task by adding your session ID and file scope below, **commit and push the
claim immediately**, never start a task another session has claimed, keep scopes non-overlapping,
run `git pull --rebase` before every push, make small frequent commits, and log every handoff,
conflict, and completion here. Marking anything "verified" requires checking it against an official
source with a linked URL.

## Sessions

| Session ID | Branch | Notes |
|---|---|---|
| `6f06d5b3-rentincreasesf5` | `arena/6f06d5b3-rentincreasesf5` | Owner-directed session. Sole session active so far; **also designated final integration session** (merges data, re-verifies line by line, publishes site, opens & merges PR to `main`). |

## Task Board

| ID | Task | Status | Owner (session ID) | File scope |
|---|---|---|---|---|
| T1 | Research & verify SF rent-increase rules (local/state/federal) from official sources; build per-row sourced findings table | **done** | `6f06d5b3-rentincreasesf5` | `data/findings.csv`, `data/sources.md` |
| T2 | Unit & tenancy data (anonymized; dates/amounts unchanged) + allowed-increase analysis per unit | **done** | `6f06d5b3-rentincreasesf5` | `data/units.csv`, `data/analysis.md` |
| T3 | Executive summary (license/notice question front and center, step-by-step, official links) | **done** | `6f06d5b3-rentincreasesf5` | `pages/executive-summary.html`, `pages/process.html` |
| T4 | Site build: landing dashboard + subpages (rules, units, practice, legal, flagged) | **done** | `6f06d5b3-rentincreasesf5` | `index.html`, `css/style.css`, `pages/*.html`, `data/flagged.csv` |
| T5 | Final integration: re-verify combined data line by line, broken-link check, PR to main, merge, confirm Pages deploy | in progress | `6f06d5b3-rentincreasesf5` | repo-wide read-only review + this file |

Shared outputs (table data, site index & navigation) are touched **only** by the final integration
session (T5) — here, the same sole session, which is noted in the log.

## Log

- 2026-11-07 — Session `6f06d5b3-rentincreasesf5` started. Repo surveyed: initial commit only
  (`README.md`). GitHub Pages already enabled: public, source = `main` branch, path `/`,
  URL `https://kanlerxz87-cyber.github.io/RentincreaseSF5/`. Claimed T1–T5 (pushing this claim now).
  Anonymization policy: real tenant initials are **never written in this repo or site**; placeholder
  IDs (e.g., `U1-TA`) are used; dates and dollar amounts are kept unchanged. The placeholder→identity
  mapping is held by the property owner only and is intentionally not stored in the repo.
- 2026-11-07 — **T1 done.** 53-row findings table (`data/findings.csv`), every row with a source link
  and verification status; 33-source register (`data/sources.md`). Official pages fetched and read
  directly: sf.gov "Learn about rent increases", sf.gov Housing Inventory, sf.gov Rent Board Fee,
  Cal. Civ. Code §827, §1947.12 (leginfo), 42 U.S.C. §3604 (govinfo). All other official URLs come from
  search results on official domains (sf.gov / leginfo / federalregister / congress.gov / sfplanning).
  Key verified facts: 2026-27 cap 1.6% (official announcement 2026-01-14); rent increase **license is
  required for ALL owners incl. individuals** (auto-generated via annual Housing Inventory report, due
  3/1; unlicensed annual/banked increases unenforceable); 30/90-day written notice (+5 mailed); banked
  increases add (not compound); Rent Board fee $59/unit (2026-27, 50% pass-through); §37.9(d)
  anti-retaliation; §37.9F circumvention; FHA §3604(b) terms discrimination; SCRA does **not** cap tenant
  rent increases (clarified — no 15% rule in current text). Irregularities: none in the repo itself
  (fresh repo). Unverified items (O&M 7% cap; 94122 neighborhood label; 2026-27 methodology note) are
  flagged F-06/F-07/F-08, not presented as official.
- 2026-11-07 — **T2 done.** `data/units.csv` (anonymized; dates/amounts unchanged), `data/analysis.md`
  (Unit 2: 12.1% available at 2026-06-01 → $3,531.15, or 1.6% → $3,200.40; Unit 1: two scenarios
  bounded by the undocumented pre-2025 ledger, upper bound 15.7% → $4,622.22). `data/flagged.csv` holds
  12 items (F-01…F-12). All unit inputs are owner-provided and labeled internal; no values inferred.
- 2026-11-07 — **T3 done.** Executive summary written with the license/notice question at the top
  (answer: yes, individual owners need the license too), 8-step process, per-unit summary, risks.
  Every step links to an official source.
- 2026-11-07 — **T4 done.** Static site: `index.html` dashboard + 7 subpages + `css/style.css`;
  no build step (Pages source = main /). Broken-link check: 156 local links across 8 HTML files — 0 broken.
  CSV integrity check: only intentional blank source (F-K04 bedroom counts — flagged F-05).

## Open Requests to Other Sessions

None (sole session).
