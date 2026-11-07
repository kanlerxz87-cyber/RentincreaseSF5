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
| T8 | Independent substantive fact-check: official-source evidence register (one row per legal/numeric fact: verbatim excerpt + official URL + retrieval date + verified/unverified flag) and read-only cross-check of other sessions' published outputs; discrepancies logged here and marked `needs review` | in progress | session-a872cd08 | `evidence/**` (new directory; read-only on every other path) |

## Claims log

- 2026-11-07 — `session-635908db` claimed T1–T5 with the file scopes above. Claim committed and pushed immediately.
- 2026-11-07 — Repo review result: initial commit `b747350` contained only `README.md` (`# RentincreaseSF5`, no newline). No other files, no site, no data, no COORDINATION.md. Flagged for review: empty repo / no pre-existing findings to verify.

## Session a872cd08 — claim, observed overlaps, requests (added 2026-11-07T20:12Z)

- Session ID: `session-a872cd08`. Platform-fixed branch: `arena/a872cd08-rentincreasesf5` (cannot create/switch to a `session-*` branch). Started from `origin/main` (`b747350`), then fast-forwarded to `a00d318d`'s published board (`77e931e`, which contains `635908db`'s `528c731`) so the earliest published board is preserved. No already-claimed task has been started by this session.
- **Claim: T8** (row above). Scope is `evidence/**` only; it touches no file named in T1–T7. T8 does not replace `data/SOURCES.md` (T4) or `scripts/verify.py` (T6); it is an independent second-source check. `evidence/register.csv` is offered as a reference table that T6 may consume and the integration session may link from the Sources / Flagged for Review pages. T7 is left as listed (not claimed).
- Branch/board survey (`git fetch` of `refs/heads/arena/*`, 2026-11-07T20:07Z):

| Session | Branch | Board commit (UTC) | What its board claims |
|---|---|---|---|
| 635908db | `arena/635908db-rentincreasesf5` | `528c731` (20:02:16) | T1–T5 research / data / site; lists T6, T7 |
| 6f06d5b3 | `arena/6f06d5b3-rentincreasesf5` | `5a4d399` (20:04:23) | separate board, not based on 635908db's: `data/findings.csv`, `data/sources.md`, `data/units.csv`, `data/analysis.md`, `pages/*.html`, `index.html`, `css/style.css`, `data/flagged.csv`, plus final integration |
| a00d318d | `arena/a00d318d-rentincreasesf5` | `77e931e` (20:04:45) | T6 only (built on 635908db's board) |
| f5ead75b | `arena/f5ead75b-rentincreasesf5` | `ede0e00` (20:05:02) | separate board: `site/**`, `scripts/**`, `.github/workflows/**`, `README.md`, "sole integration scope" |

- Overlaps found (for the owners to resolve; nothing edited by this session):
  1. Research / data / executive summary / site (T2–T5) is claimed by both `635908db` (earliest, 20:02:16Z) and `6f06d5b3` (20:04:23Z). The protocol says the earliest published claim stands. (`data/SOURCES.md` vs `data/sources.md` would also be two different files on Linux.)
  2. `f5ead75b`'s `site/**` overlaps T5 (site); its `scripts/**` and `.github/workflows/**` overlap T6 (`a00d318d`).
  3. Three boards each designate their own session as final integration; four COORDINATION.md files were created independently, so merging to `main` will hit add/add conflicts unless boards are reconciled.
- Requests (each owner decides; logged here instead of editing anyone's files):
  - `6f06d5b3`, `f5ead75b`: re-run `git fetch origin 'refs/heads/arena/*:refs/remotes/origin/arena/*'`, read `635908db`'s board, then re-scope to unclaimed work or log a handoff here. Base your `COORDINATION.md` on `528c731` rather than a new file.
  - Per the owner's rules, only ONE session may own `index.html` / navigation / final integration. On the earliest published board that is `635908db`, unless it declares otherwise or its claim goes stale (>60 min with no commits, i.e. after 21:02Z).
  - Any session may append requests for T8 to its own board; T8 will re-fetch all `arena/*` branches before each cross-check pass.

## Handoffs / conflicts

- No conflicts so far. No handoffs from crashed sessions.
- 2026-11-07T20:04Z — `session-a00d318d` read the remotely published task board before claiming T6. Preserved `session-635908db`'s board and all T1–T5/T7 claims by fast-forwarding to its published claim commit `528c731`; did not start any claimed task. This session's platform-fixed working branch is `arena/a00d318d-rentincreasesf5` (it cannot create, switch to, or push a `session-*` branch). T6 scope is limited to verification tooling/tests/report/workflow and this board entry. No research/data/site files will be edited by this session while their claims are active.
- Integration request to `session-635908db`: please provide a documented CSV/schema or manifest and static site entry points; retain an official-source URL on EVERY data row (including unverified rows); use blank values and a Flagged for Review reference for unconfirmed facts; publish only occupant placeholders, never supplied initials or a re-identification key. Keep unit facts explicitly owner-reported, not government-verified. Please record source retrieval dates and distinguish legal rules from arithmetic/scenarios. T6 will audit these outputs after integration, not claim ownership of them.

## Sources, verification, irregularities log

_(Filled in per task as work completes. Nothing is marked verified without checking an official source and linking it.)_

### T1
- Verified: repository is public, default branch `main`, GitHub Pages is already configured (`build_type: legacy`, source `main` / `/`, https://kanlerxz87-cyber.github.io/RentincreaseSF5/). Source: GitHub API `repos/kanlerxz87-cyber/RentincreaseSF5/pages` via `gh api` (official GitHub, 2026-11-07).
- Irregularity flagged: empty repository; no prior research, data, or site to review line-by-line.

## Final integration record

_(PR link, merge result, deploy confirmation recorded here at completion.)_
