# COORDINATION.md — Shared Task Board

**Repository:** kanlerxz87-cyber/RentincreaseSF5
**Purpose:** SF residential rent-increase research, verification, and GitHub Pages site.
**Last updated:** 2026-11-07 (UTC)

## Session conventions / platform constraints

- This session runs on the platform-fixed branch `arena/635908db-rentincreasesf5`. The platform does not permit this session to switch to, create, or push any other branch, so the integration work is done on this branch and merged to `main` via PR. Other sessions should use their own `session-<id>/<task>` branches as requested by the owner.
- Session ID for this board: `session-635908db`.
- Checked `origin` for other sessions' branches on 2026-11-07: only `origin/main` and `origin/HEAD` existed. No other active claims were found.
- Shared outputs (table data, site index/navigation) are owned by this final integration session; other sessions must log requests here rather than editing them.
- **Privacy rule (owner instruction):** personal information is internal only. All published pages use placeholder occupant labels. Real tenant identifiers supplied by the owner are NOT stored in this public repository. Dates and dollar amounts are preserved exactly as provided.
- Push discipline: `git pull --rebase` before every push. Small, frequent commits.

## Task board

| Task ID | Task | Status | Owner session | Files in scope |
|---|---|---|---|---|
| T1 | Repo review + create shared task board | done | session-635908db | `COORDINATION.md`, `README.md` |
| T2 | Research: SF Rent Board process — "license"/registration/petition question, annual allowable increase, notice, banking, 12-month rule, executive summary | in progress | session-635908db | `research/01-executive-summary.md`, `research/02-rent-board-process.md` |
| T3 | Research: local / state / federal legal framework; fair housing; corporations vs individual owners; notice content; one-unit vs both-units analysis | in progress | session-635908db | `research/03-legal-framework.md`, `research/04-practice-and-notice.md` |
| T4 | Verified data tables — every row carries an official-source link; blank + flag where unverifiable | in progress | session-635908db | `data/*.csv`, `data/SOURCES.md` |
| T5 | GitHub Pages site: clean dashboard landing + category subpages, tables, analysis, Flagged for Review page | in progress | session-635908db | `index.html`, `pages/*`, `assets/*`, `_config.yml`, `.nojekyll` |
| T6 | Line-by-line verification, build check, broken-link check, anonymization audit | in progress | session-a00d318d | `scripts/verify.py`, `scripts/tests/*`, `VERIFICATION.md`, `.github/workflows/verify.yml`, `docs/VERIFICATION-CONTRACT.md` |
| T7 | PR to main, merge, confirm Pages deploy, record PR link + result here | unclaimed | session-635908db | `COORDINATION.md` |

## Claims log

- 2026-11-07 — `session-635908db` claimed T1–T5 with the file scopes above. Claim committed and pushed immediately.
- 2026-11-07 — Repo review result: initial commit `b747350` contained only `README.md` (`# RentincreaseSF5`, no newline). No other files, no site, no data, no COORDINATION.md. Flagged for review: empty repo / no pre-existing findings to verify.

## Handoffs / conflicts

- No conflicts so far. No handoffs from crashed sessions.
- 2026-11-07T20:04Z — `session-a00d318d` read the remotely published task board before claiming T6. Preserved `session-635908db`'s board and all T1–T5/T7 claims by fast-forwarding to its published claim commit `528c731`; did not start any claimed task. This session's platform-fixed working branch is `arena/a00d318d-rentincreasesf5` (it cannot create, switch to, or push a `session-*` branch). T6 scope is limited to verification tooling/tests/report/workflow and this board entry. No research/data/site files will be edited by this session while their claims are active.
- Integration request to `session-635908db`: please provide a documented CSV/schema or manifest and static site entry points; retain an official-source URL on EVERY data row (including unverified rows); use blank values and a Flagged for Review reference for unconfirmed facts; publish only occupant placeholders, never supplied initials or a re-identification key. Keep unit facts explicitly owner-reported, not government-verified. Please record source retrieval dates and distinguish legal rules from arithmetic/scenarios. T6 will audit these outputs after integration, not claim ownership of them.

## Sources, verification, irregularities log

### T6 checkpoint (session-a00d318d, 2026-11-07)
- Published `docs/VERIFICATION-CONTRACT.md` on this session branch with the preferred row schema and required `data-row-id` mapping. Integration owner should read it before finalizing shared outputs; this session has not edited those outputs.
- Verifier and 25 synthetic tests are implemented in T6 scope; tests pass. The incomplete-tree audit correctly blocks on missing site/data/flag page. Full release verification remains pending.
- Official sources read independently: [Housing Inventory](https://www.sf.gov/rent-board-housing-inventory), [rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco), [current rates](https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit), [fee](https://www.sf.gov/rent-board-fee), [Rules Part IV](https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring), [Civil Code 827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=827&lawCode=CIV), [1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12), [1942.5](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1942.5).
- Irregularity for integration review: the official [banking page](https://www.sf.gov/information--banked-rent-increases) uses August 1, 2025 in its example, then says the annual rate in effect on August 1, 2024 while giving 1.4%. Treat as an apparent source-page date typo; do not silently correct it or infer a property-specific bank. Use the official rate table/Rule 4.12 and flag the wording.
- Privacy reminder: official Housing Inventory submissions are public. Do not put supplied occupant identifiers in the repo or public site; required official filings still need accurate information and are not anonymized by this website.
- T7 remains owned by session-635908db. No takeover: its claim is not yet 60 minutes old at this checkpoint.


_(Filled in per task as work completes. Nothing is marked verified without checking an official source and linking it.)_

### T1
- Verified: repository is public, default branch `main`, GitHub Pages is already configured (`build_type: legacy`, source `main` / `/`, https://kanlerxz87-cyber.github.io/RentincreaseSF5/). Source: GitHub API `repos/kanlerxz87-cyber/RentincreaseSF5/pages` via `gh api` (official GitHub, 2026-11-07).
- Irregularity flagged: empty repository; no prior research, data, or site to review line-by-line.

## Final integration record

_(PR link, merge result, deploy confirmation recorded here at completion.)_
