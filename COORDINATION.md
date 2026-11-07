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
| T6 | Line-by-line verification, build check, broken-link check, anonymization audit | unclaimed | session-635908db | `scripts/verify.py`, `VERIFICATION.md` |
| T7 | PR to main, merge, confirm Pages deploy, record PR link + result here | unclaimed | session-635908db | `COORDINATION.md` |

## Claims log

- 2026-11-07 — `session-635908db` claimed T1–T5 with the file scopes above. Claim committed and pushed immediately.
- 2026-11-07 — Repo review result: initial commit `b747350` contained only `README.md` (`# RentincreaseSF5`, no newline). No other files, no site, no data, no COORDINATION.md. Flagged for review: empty repo / no pre-existing findings to verify.

## Handoffs / conflicts

- No conflicts so far. No handoffs from crashed sessions.

## Sources, verification, irregularities log

_(Filled in per task as work completes. Nothing is marked verified without checking an official source and linking it.)_

### T1
- Verified: repository is public, default branch `main`, GitHub Pages is already configured (`build_type: legacy`, source `main` / `/`, https://kanlerxz87-cyber.github.io/RentincreaseSF5/). Source: GitHub API `repos/kanlerxz87-cyber/RentincreaseSF5/pages` via `gh api` (official GitHub, 2026-11-07).
- Irregularity flagged: empty repository; no prior research, data, or site to review line-by-line.

## Final integration record

_(PR link, merge result, deploy confirmation recorded here at completion.)_
