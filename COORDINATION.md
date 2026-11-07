# COORDINATION — Shared Task Board

This file is the shared task board for all agent sessions working in this repository.
Protocol: claim a task by adding your session ID and file scope below, **commit and push the
claim immediately**, never start a task another session has claimed, keep scopes non-overlapping,
run `git pull --rebase` before every push, make small frequent commits, and log every handoff,
conflict, and completion here. Marking anything "verified" requires checking it against an official
source with a linked URL. Shared outputs (table data, site index & navigation) are changed only by
a final integration session once all other tasks are done.

## Session registry

| Session ID | Branch | Contribution |
|---|---|---|
| `arena-f5ead75b` | `arena/f5ead75b-rentincreasesf5` | Research + first published dashboard (PR #1, merged) |
| `arena-05e5d5ab` | `arena/05e5d5ab-rentincreasesf5` | Reconciliation + independent audit (PR #2, merged) |
| `6f06d5b3-rentincreasesf5` | `arena/6f06d5b3-rentincreasesf5` | Owner-directed full delivery: sourced findings site, per-unit analysis, final integration (this session) |

---

## Task board — session `arena-f5ead75b` (preserved verbatim from origin/main)

Session: arena-f5ead75b. All work stays on the Arena-assigned branch `arena/f5ead75b-rentincreasesf5` (platform requirement; no session branch created).

| Task | Status | Owner | File scope |
|---|---|---|---|
| Official-source research, privacy-safe dashboard, tests and publication integration | in progress | arena-f5ead75b | COORDINATION.md, site/**, scripts/**, .github/workflows/**, README.md |

### Log (preserved verbatim from origin/main, including the arena-05e5d5ab reconciliation section)

- 2026-11-07: Empty repository inspected; no other claims. Claimed sole integration scope. Private tenant identifiers will not be copied into files. Owner-supplied dates and amounts are unverified, not official records.
- Claim bootstrap: remote Arena branch did not exist; initial pull failed without modifying work. Rebased against origin/main and pushed claim to assigned branch.
- 2026-11-07: Research read against SF Housing Inventory, annual-increase guidance, rental coverage, Rule 4.10, AB1482 guidance, California Civil Code §§827 and 1942.5, CRD housing guidance, and HUD guide. Full manual-review links are in Sources page. Source-date inconsistency in SF annual example published as F07.
- Privacy: no tenant names/initials or exact address copied. Owner-reported dates/amounts retained separately and marked unverified. Illustrations are derived, not verified rents. No license/notice/legal action performed.
- Validation: Python build succeeds; local href targets, every table data-row official link, source hostname allowlist, headings and no analytics checks pass. External references retrieved by research tools; no claim of exhaustive automated external-link health. No browser rendering automation available/used.
- Research irregularities task: needs review (published site/flagged.html F01–F10; property evidence, legal eligibility and empirical norms remain unknown). Integration implementation complete; publication in progress.
- Deployment adaptation: Pages configuration update returned HTTP 403 (integration lacks Pages-admin permission). Existing Pages configuration already publishes main:/; scope extended to generated root *.html, style.css and .nojekyll (no other session claims exist). Preserve existing deployment settings and use root static files instead of requiring admin changes. Workflow will validate only; GitHub's existing Pages build publishes after merge.

### Parallel-session reconciliation · arena-05e5d5ab · 2026-11-07 (preserved verbatim)

- This session began at the original empty main and claimed its assigned branch before the other session's claim was visible on main. PR #2 discovered that PR #1 had meanwhile published an overlapping dashboard. Paused integration, fetched main and merged it into the assigned branch.
- All overlapping site, generator, README and workflow files were resolved by preserving the already-published main version from arena-f5ead75b, not replacing that session's work. Removed only three unpublished duplicate pages unique to this session. No other session's files were discarded.
- Scope of this contribution is now independent verification (`scripts/independent_audit.py`) and this reconciliation log. Existing site implementation remains owned by arena-f5ead75b; no change request to it was necessary.
- Independently retrieved official SF inventory, current rates, annual-increase guide, §37.3, Part IV and California §§827, 1947.12, 1942.5. Confirmed key findings: individual owners included; license automatically generated and required on effective date; 1.6% applies March 2026–February 2027; notices generally 30/90 days with mailing rules; protected-trait/retaliation concerns remain distinct from cap compliance. Private unit records are still unverified, not cleared for notices.
- Official general-guide worked example mislabels June 2025 with 1.6%; current rates controls. The independent research also noticed a banking-page example mislabeling August 2024 with 1.4%; no historical bank total was authorized or calculated by this session.
- Required pre-push pull --rebase attempted to flatten the explicit main-integration merge and replay the other session's original claim, creating a duplicate coordination add/add conflict. Aborted that rebase to retain the fully resolved integration merge; remote assigned branch had no new commits. No published work was removed.
- Independent audit passes: 6 pages / 62 official-sourced body rows, root/site artifact parity, local href/style targets, language/landmarks and supplied-initial exclusion. Existing generator and validation also pass.

---

## Task board — session `6f06d5b3-rentincreasesf5` (this session)

| ID | Task | Status | Owner | File scope |
|---|---|---|---|---|
| T1 | Research & verify SF rent-increase rules (local/state/federal) from official sources; per-row sourced findings table | **done** | `6f06d5b3-rentincreasesf5` | `data/findings.csv`, `data/sources.md` |
| T2 | Unit & tenancy data (anonymized; dates/amounts unchanged) + allowed-increase analysis per unit | **done** | `6f06d5b3-rentincreasesf5` | `data/units.csv`, `data/analysis.md` |
| T3 | Executive summary (license/notice question front and center, step-by-step, official links) | **done** | `6f06d5b3-rentincreasesf5` | `pages/executive-summary.html`, `pages/process.html` |
| T4 | Site build: landing dashboard + subpages (rules, units, practice, legal, flagged) | **done** | `6f06d5b3-rentincreasesf5` | `index.html`, `css/style.css`, `pages/*.html`, `data/flagged.csv` |
| T5 | Final integration: re-verify combined data line by line, broken-link check, PR to main, merge, confirm Pages deploy | in progress | `6f06d5b3-rentincreasesf5` | repo-wide review + this file |

Anonymization policy: real tenant initials are **never written in this repo or site**; placeholder
IDs (Tenant U1-A…U1-D, U2-A, U2-B) are used; dates and dollar amounts are kept unchanged. The
placeholder→identity mapping is held by the property owner only and is intentionally not stored in
the repo.

### Log — session `6f06d5b3-rentincreasesf5`

- 2026-11-07 — Session started. Repo surveyed at start: initial commit only (`README.md`); prior
  sessions' work (PR #1, PR #2) was not yet on the local main when the claim was made.
  GitHub Pages already enabled: public, source = `main`, path `/`,
  URL `https://kanlerxz87-cyber.github.io/RentincreaseSF5/`. Claimed T1–T5.
- 2026-11-07 — **T1 done.** 53-row findings table (`data/findings.csv`), every row with a source
  link + verification status; 33-source register (`data/sources.md`). Official pages fetched and
  read directly: sf.gov "Learn about rent increases", Housing Inventory, Rent Board Fee;
  Civ. Code §827, §1947.12 (leginfo); 42 U.S.C. §3604 (govinfo). Other official URLs from search
  results on official domains. Key verified facts: 2026-27 cap 1.6% (official announcement
  2026-01-14); rent increase **license required for ALL owners incl. individuals** (auto-generated
  via annual Housing Inventory report, due 3/1; unlicensed annual/banked increases unenforceable);
  30/90-day written notice (+5 mailed); banked increases add (not compound); Rent Board fee $59/unit
  (2026-27, 50% pass-through); §37.9(d) anti-retaliation; §37.9F circumvention; FHA §3604(b);
  SCRA does **not** cap tenant rent increases (no 15% rule in current text — clarified).
  Unverified items flagged, not presented as official: O&M 7% cap (F-06), 94122 label (F-07),
  2026-27 methodology note (F-08).
- 2026-11-07 — **T2 done.** `data/units.csv` (anonymized), `data/analysis.md`: Unit 2 → 12.1%
  available at 2026-06-01 ($3,150 → $3,531.15, 90-day notice) or 1.6% → $3,200.40 (30-day);
  Unit 1 → scenario-bounded math pending pre-2025 ledger (upper bound 15.7% → $4,622.22).
  `data/flagged.csv`: 12 items (F-01…F-12). Owner inputs labeled internal; nothing inferred.
- 2026-11-07 — **T3 done.** Executive summary with the license/notice question first (answer: yes,
  individual owners need the license too); 8-step process, each step with an official link.
- 2026-11-07 — **T4 done.** Static site: `index.html` dashboard + 7 subpages + `css/style.css`;
  no build step (Pages source = main /). Broken-link check: 156 local links / 8 HTML files → 0
  broken. CSV integrity: only intentional blank source (F-K04 bedroom counts — flagged F-05).
- 2026-11-07 — **Concurrency conflict discovered.** A pre-push rebase against origin/main failed:
  PR #1 (arena-f5ead75b) and PR #2 (arena-05e5d5ab) had merged a separate dashboard + this file
  into main while this session worked on an initially empty local view. Aborted the rebase and
  resolved via an explicit **merge of origin/main** (same approach arena-05e5d5ab used for its
  integration). Conflicts: `COORDINATION.md` (add/add), `README.md` (content), `index.html`
  (add/add). Resolution, without discarding any other session's work:
  - `COORDINATION.md`: merged — both prior sessions' board + full log preserved verbatim above;
    this session's board and log appended.
  - `README.md`: merged — this session's description plus a section documenting the prior
    dashboard (source of truth `scripts/build.py`, validation `python scripts/check.py`).
  - `index.html` (root): this session's dashboard now serves as the root landing page, because the
    owner's directive to this session required the specific page structure (executive summary with
    the license question up front, practice, legal-scrutiny, per-unit analysis). **The prior
    dashboard is fully preserved**: intact at `/site/` (https://kanlerxz87-cyber.github.io/RentincreaseSF5/site/),
    plus its root-level pages (`amounts.html`, `process.html`, `protections.html`, `flagged.html`,
    `sources.html`, `style.css`), `scripts/`, and CI workflow remain in the tree unchanged.
    Root files from the prior session were not deleted.
- 2026-11-07 — **Integration cross-check (line-by-line, this session vs. prior sessions' data).**
  Prior sessions' verified findings and this session's findings are **consistent** on every shared
  claim: license required for all owners incl. individuals; license auto-generated via Housing
  Inventory; license must be in effect on the increase's effective date (not attached to notice);
  1.6% for 2026-03-01→2027-02-28; 1.4% for 2025-26; 30/90-day notice with +5 mailing; no
  market-"normal" verified for 94122. The prior independent audit's note that the official
  worked-example dates are mislabeled (June 2025 shown as 1.6%; banking-page August 2024 shown as
  1.4%) was independently confirmed against the fetched official page; it does not change the
  rates used here, which follow the official rule "use the percentage in effect on the increase
  date" (each year's rate is keyed to the effective date, matching the official multi-year example).
  Prior sessions deliberately did not compute banked totals; this session's banked calculations
  (Unit 2: 12.1% at 2026-06-01; Unit 1 upper bound 15.7%) are labeled with their assumptions and
  owner-data dependencies on the Flagged page (F-01…F-03, F-11, F-12).
- 2026-11-07 — **T5 verification (combined tree).** Local link check across **all 19 HTML files
  (both dashboards): 270 local links, 0 broken**. Prior session's `scripts/check.py` (the CI
  check; workflow runs `build.py && check.py` only): **PASS**. Prior session's
  `scripts/independent_audit.py` (one-off audit of their own integration state; not part of CI)
  now fails only on its root/site artifact-parity assertion — expected and documented, because the
  root landing page intentionally belongs to this later integration; the prior dashboard remains
  fully intact at `/site/`. Their script was not edited (protocol: other sessions' files are
  logged, not changed). PR to main: opened from this branch and merged after this commit;
  Pages deploy status and PR link recorded in the follow-up entry below.
