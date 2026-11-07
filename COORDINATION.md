# COORDINATION.md — Shared Task Board

**Repository:** kanlerxz87-cyber/RentincreaseSF5
**Purpose:** SF residential rent-increase research, verification, and GitHub Pages site.
**Last updated:** 2026-11-07 (UTC)

## Session conventions / platform constraints

- **Branch/worktree reconciliation (logged exception):** this session runs on the platform-fixed branch `arena/635908db-rentincreasesf5`. The platform does not permit this session to switch to, create, or push any other branch, so a separate `session-<id>/<task>` branch and a separate worktree could not be created here. The requested convention is reconciled by treating the platform-fixed branch as **the integration branch** and by enforcing **non-overlapping file scopes per task** in the table below; each task's claim names its session ID and its exclusive file scope. No other session was active, so there was no concurrent writer. Other sessions should still use their own `session-<id>/<task>` branches/worktrees as requested by the owner.
- Session ID for this board: `session-635908db`.
- Checked `origin` for other sessions' branches on 2026-11-07: only `origin/main`, `origin/HEAD` and this branch existed. No other active claims were found. No stale/crashed claim was taken over.
- Shared outputs (table data, site index/navigation) are owned by this final integration session; other sessions must log requests here rather than editing them.
- **Privacy rule (owner instruction):** personal information is internal only. All published pages use placeholder occupant labels (Occupant A–F). Real tenant identifiers supplied by the owner are NOT stored in this public repository. Dates and dollar amounts are preserved exactly as provided.
- Push discipline: `git pull --rebase` before every push. Small, frequent commits. Stop on conflict; resolve without discarding others' work and log it here.
- `needs review` means published on the site's **Flagged for Review** page with official source links; it does not block the merge.

## Task board

| Task ID | Task | Status | Owner session | Files in scope |
|---|---|---|---|---|
| T1 | Repo review + create shared task board | done | session-635908db | `COORDINATION.md`, `README.md` |
| T2 | Research: SF Rent Board process — "license"/registration/petition question, annual allowable increase, notice, banking, 12-month rule, executive summary | done | session-635908db | `research/01-executive-summary.md`, `research/02-rent-board-process.md` |
| T3 | Research: local / state / federal legal framework; fair housing; corporations vs individual owners; notice content; one-unit vs both-units analysis | done | session-635908db | `research/03-legal-framework.md`, `research/04-practice-and-notice.md`, `research/05-units-and-calculations.md` |
| T4 | Verified data tables — every row carries an official-source link; blank + flag where unverifiable | done | session-635908db | `data/*.json` (sources, process, requirements, legal, rates, units, practice, discrimination, flags, verification) |
| T5 | GitHub Pages site: clean dashboard landing + category subpages, tables, analysis, Flagged for Review page | done | session-635908db | `index.html`, `pages/*`, `assets/*`, `.nojekyll`, `scripts/build_site.py` |
| T6 | Line-by-line verification, build check, broken-link check, anonymization audit | in progress | session-635908db | `scripts/verify.py`, `VERIFICATION.md` |
| T7 | PR to main, merge, confirm Pages deploy, record PR link + result here | in progress | session-635908db | `COORDINATION.md` |

## Claims log

- 2026-11-07 — `session-635908db` claimed T1–T5 with the file scopes above. Claim committed and pushed immediately (`528c731`).
- 2026-11-07 — `session-635908db` marked T2–T5 `done` and claimed **T6** (`scripts/verify.py`, `VERIFICATION.md`) and **T7** (`COORDINATION.md`). Claim committed and pushed immediately. T6/T7 are the final-integration tasks; flagged/unverified items are published on Flagged for Review and do not block them.
- 2026-11-07 — Repo review result: initial commit `b747350` contained only `README.md` (`# RentincreaseSF5`, no newline). No other files, no site, no data, no COORDINATION.md. Flagged for review: empty repo / no pre-existing findings to verify.

## Handoffs / conflicts

- No other session was active; no handoffs from crashed sessions.
- `git pull --rebase origin arena/635908db-rentincreasesf5` before the first push failed because the remote branch did not yet exist; `git push` created it (`528c731`). Subsequent rebase pulls succeeded with no conflicts. Nothing from another session was ever discarded or overwritten.
- No merge/rebase conflicts occurred. No cross-scope requests were received from other sessions.

## Sources, verification, irregularities log

_(Nothing is marked verified without checking an official source and linking it. Full registry: `data/sources.json`, 51 sources; published on the site's Official Sources page.)_

### T1
- Verified: repository is public, default branch `main`, GitHub Pages is already configured (`build_type: legacy`, source `main` / `/`, https://kanlerxz87-cyber.github.io/RentincreaseSF5/). Source: GitHub API `repos/kanlerxz87-cyber/RentincreaseSF5/pages` via `gh api` (official GitHub, 2026-11-07).
- Irregularity flagged: empty repository; no prior research, data, or site to review line-by-line.

### T2 — Rent Board process + executive summary
- Verified from official sources S01–S17, S21–S23, S26, S37, S43, S45, S51: an individual (non-corporate) owner of a rent-controlled unit must report into the Housing Inventory; the Rent Increase License is **automatically generated** (not a separate application); no petition/notice about the specific increase is needed for annual/banked increases; the license must be **current on the effective date**; an unlicensed increase is null and void; tenant petitions are free with no time limit.
- Verified the current allowable annual increase is **1.6% for 3/1/2026–2/28/2027** (S02, S03, S04, S45) and the historical Form 571 table (S03).
- Verified 30/90-day written notice (+5 days if mailed) from Civil Code § 827 (S30) and notice content from § 37.3(b) / Rules 4.10, 4.12 (S13, S15).
- Irregularities flagged: 12-month vs 24-month banking conflict (S15 vs S10); conflicting license start dates (S07/S08 vs S43); differing remedies (S07 vs S08); third-party guides contradicted by official sources.

### T3 — Legal framework, fair housing, practice
- Verified local coverage/rate/licensing/banking/roommate rules (S13, S14, S16, S18, S19, S20), state statutes (S30 Civil 827, S31 Civil 1947.12, S32 Civil 1954.53, S33 Gov 12955), federal Fair Housing Act (S34 HUD, S35 govinfo 42 USC 3604), HUD program-specific rent rules (S47), free tenant legal help (S24, S25, S41, S44, S51).
- Verified there is no official 94122-specific rate, no federal numeric cap on private unsubsidized rents, no official model notice wording, and no official record-retention period. Those values were **left blank and flagged**, never inferred.
- Verified the Tenant Right to Counsel program from the official 37.9(c) notice (S44) and MOHCD's Housing Trust Fund report (S41).
- Irregularity flagged: official City Analysis of Impediments PDF (S48) section on additional local protected classes could not be retrieved line by line (PDF parser limited to 30 pages); a draft list was removed rather than published unverified. Value left blank and flagged.

### T4 — Data tables
- Ten datasets written; every row carries one or more `sources` IDs that resolve to official government URLs. Empty `value` cells for unverifiable items are enforced by `scripts/verify.py`.
- `data/rates.json` transcribed row by row from official Form 571 (S03); the 3/1/2027–2/28/2028 rate is intentionally blank.
- `data/units.json` uses Occupant A–F only; all date/amount facts are labelled `owner-provided` or `computed`, and no computed figure is labelled `verified`.

### T5 — Site
- 12 static HTML pages generated reproducibly by `scripts/build_site.py` from `data/*.json`; `.nojekyll` added so GitHub Pages serves plain static files. No external JS/CSS dependencies.
- Landing page, Executive Summary, Rent Board Process, Requirements Checklist, Legal Framework, Allowable Rates, Units & Calculations, Practice & Notice, Fair Housing / One vs Both, Official Sources, Verification Log, Flagged for Review.
- All entries/findings are in filterable tables; every row has an official-source link; the Flagged for Review page is clearly labelled and linked from every page footer and the sidebar.

### T6 — Verification (in progress)
- `scripts/verify.py` checks: (1) every rendered data row has ≥1 official-domain link; (2) every UNVERIFIED row has an empty value cell; (3) all internal links/assets resolve; (4) no owner-supplied tenant identifiers appear in published files; (5) every source ID used exists in `data/sources.json`; (6) every page has a title, navigation and the privacy footer. It writes `VERIFICATION.md`.
- Final integration re-verified the combined data line by line against the official pages, including re-fetching S39, S40(Forms Center), S41, S42, S43, S44, S45, S46, S47, S48, S51 and the Property Information Map / Rent Board Portal. Two corrections resulted: the HUD handbook is **4350.1 REV-1 ch. 7** (not 4350.3), and no specific additional SF-local protected class is asserted from S48.

## Final integration record

_(PR link, merge result, deploy confirmation recorded here at completion.)_
