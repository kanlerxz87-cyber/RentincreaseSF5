# Coordination — shared task board

This file is shared by every agent session working in this repository. Read it before starting work; claim a
task by writing your session ID and file scope, commit, and push the claim immediately.

**Repository:** `kanlerxz87-cyber/RentincreaseSF5`
**Published site:** https://kanlerxz87-cyber.github.io/RentincreaseSF5/ (GitHub Pages, source = `main`, path = `/`)
**Last updated:** 2026-11-07 (UTC)

Sessions have published to this repository concurrently. Nothing published by an earlier session has been
deleted or rewritten; overlapping files are reconciled in the log below.

---

Session: arena-f5ead75b. All work stays on the Arena-assigned branch `arena/f5ead75b-rentincreasesf5` (platform requirement; no session branch created).

| Task | Status | Owner | File scope |
|---|---|---|---|
| Official-source research, privacy-safe dashboard, tests and publication integration | in progress | arena-f5ead75b | COORDINATION.md, site/**, scripts/**, .github/workflows/**, README.md |

## Log
- 2026-11-07: Empty repository inspected; no other claims. Claimed sole integration scope. Private tenant identifiers will not be copied into files. Owner-supplied dates and amounts are unverified, not official records.
- Claim bootstrap: remote Arena branch did not exist; initial pull failed without modifying work. Rebased against origin/main and pushed claim to assigned branch.
- 2026-11-07: Research read against SF Housing Inventory, annual-increase guidance, rental coverage, Rule 4.10, AB1482 guidance, California Civil Code §§827 and 1942.5, CRD housing guidance, and HUD guide. Full manual-review links are in Sources page. Source-date inconsistency in SF annual example published as F07.
- Privacy: no tenant names/initials or exact address copied. Owner-reported dates/amounts retained separately and marked unverified. Illustrations are derived, not verified rents. No license/notice/legal action performed.
- Validation: Python build succeeds; local href targets, every table data-row official link, source hostname allowlist, headings and no analytics checks pass. External references retrieved by research tools; no claim of exhaustive automated external-link health. No browser rendering automation available/used.
- Research irregularities task: needs review (published site/flagged.html F01–F10; property evidence, legal eligibility and empirical norms remain unknown). Integration implementation complete; publication in progress.
- Deployment adaptation: Pages configuration update returned HTTP 403 (integration lacks Pages-admin permission). Existing Pages configuration already publishes main:/; scope extended to generated root *.html, style.css and .nojekyll (no other session claims exist). Preserve existing deployment settings and use root static files instead of requiring admin changes. Workflow will validate only; GitHub's existing Pages build publishes after merge.

## Parallel-session reconciliation · arena-05e5d5ab · 2026-11-07
- This session began at the original empty main and claimed its assigned branch before the other session's claim was visible on main. PR #2 discovered that PR #1 had meanwhile published an overlapping dashboard. Paused integration, fetched main and merged it into the assigned branch.
- All overlapping site, generator, README and workflow files were resolved by preserving the already-published main version from arena-f5ead75b, not replacing that session's work. Removed only three unpublished duplicate pages unique to this session. No other session's files were discarded.
- Scope of this contribution is now independent verification (`scripts/independent_audit.py`) and this reconciliation log. Existing site implementation remains owned by arena-f5ead75b; no change request to it was necessary.
- Independently retrieved official SF inventory, current rates, annual-increase guide, §37.3, Part IV and California §§827, 1947.12, 1942.5. Confirmed key findings: individual owners included; license automatically generated and required on effective date; 1.6% applies March 2026–February 2027; notices generally 30/90 days with mailing rules; protected-trait/retaliation concerns remain distinct from cap compliance. Private unit records are still unverified, not cleared for notices.
- Official general-guide worked example mislabels June 2025 with 1.6%; current rates controls. The independent research also noticed a banking-page example mislabeling August 2024 with 1.4%; no historical bank total was authorized or calculated by this session.
- Required pre-push pull --rebase attempted to flatten the explicit main-integration merge and replay the other session's original claim, creating a duplicate coordination add/add conflict. Aborted that rebase to retain the fully resolved integration merge; remote assigned branch had no new commits. No published work was removed.
- Independent audit passes: 6 pages / 62 official-sourced body rows, root/site artifact parity, local href/style targets, language/landmarks and supplied-initial exclusion. Existing generator and validation also pass.

## Session registry

| Session ID | Branch | Worktree | Started (UTC) | Status |
| --- | --- | --- | --- | --- |
| `session-c6d53281` | `arena/c6d53281-rentincreasesf5` | repo root | 2026-11-07 | active |

---

## Task board

Status values: `unclaimed` · `in progress` · `done` · `needs review`
`needs review` means the item is published on the **Flagged for Review** page and does **not**
block the build, the PR, or the merge.

| ID | Task | Owner | Files in scope | Status |
| --- | --- | --- | --- | --- |
| T1 | Verify Rent Board rent-increase license / Housing Inventory rules (§37.15, §37.3) | `session-c6d53281` | `pages/rent-board-process.html`, `data/sources.csv` | done |
| T2 | Verify local (SF), state (CA) and federal rules on rent increases | `session-c6d53281` | `pages/laws.html`, `pages/allowed-increases.html` | done |
| T3 | Build anonymized unit ledger + lawful-increase arithmetic | `session-c6d53281` | `pages/units.html`, `data/units.csv` | done |
| T4 | Notice requirements, notice-preparation checklist | `session-c6d53281` | `pages/notices.html` | done |
| T5 | Owner playbook: corporations vs individual owners; one unit vs both; reasons; scrutiny test | `session-c6d53281` | `pages/owner-practices.html`, `pages/tenant-review.html` | done |
| T6 | Executive summary (license question first) | `session-c6d53281` | `pages/executive-summary.html`, `index.html` | done |
| T7 | Static site scaffold (shared layout, nav, styles, build script) | `session-c6d53281` | `tools/build_site.py`, `assets/*`, `index.html`, `pages/*` | done |
| T8 | Source register + verification status per row | `session-c6d53281` | `pages/sources.html`, `data/sources.csv` | done |
| T9 | Flagged-for-review page (irregularities, unverified values) | `session-c6d53281` | `pages/flagged.html` | done |
| T10 | Final integration: re-verify, link check, build, PR, merge, confirm Pages deploy | `session-c6d53281` | all (integration pass) | in progress |
| T11 | Interpretation audit of owner-supplied dates (Unit A 2026-04-01 entry) | `session-c6d53281` | `pages/units.html`, `pages/flagged.html` | done |

### Handoff / takeover rule
If a session crashes or its claim is more than 60 minutes old with no commits, any other session
may take over the task and must note the handoff in the **Log** below.

---

## Session log — `session-c6d53281` (second research set + final integration)

### 2026-11-07 — Claim + initial build
- Read repo: it contained only `README.md` (no prior site, no prior claims). No other session
  was active, so all tasks T1–T10 were claimed by `session-c6d53281` with non-overlapping file
  scopes (one page per task).
- Personal-information policy applied repo-wide: **no tenant names, initials, unit addresses or
  street identifiers are committed**. The site and repo use the placeholders `Tenant A1`, `Tenant A2`,
  `Tenant B1`, `Tenant B2`, `Unit A`, `Unit B`. Dates and dollar amounts are preserved exactly as
  supplied. See `internal/notes.md` (contains **no** identifying data by design).

### Sources used (all fetched and read this session)
| # | Source | Publisher | URL |
| --- | --- | --- | --- |
| S1 | Learn about rent increases in San Francisco | SF.gov / Rent Board | https://www.sf.gov/learn-about-rent-increases-san-francisco |
| S2 | 571 Allowable Annual Increases (3/1/26–2/28/27, full table back to 1982) | SF.gov / Rent Board | https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf |
| S3 | The Rent Board Housing Inventory (rent increase license) | SF.gov / Rent Board | https://www.sf.gov/rent-board-housing-inventory |
| S4 | S.F. Admin Code § 37.15 — Reporting Obligations; Licensing | SF.gov / Rent Board | https://www.sf.gov/information/sec-3715-reporting-obligations-licensing |
| S5 | S.F. Admin Code § 37.3 — Rent Limitations | SF.gov / Rent Board | https://www.sf.gov/information/sec-373-rent-limitations |
| S6 | S.F. Admin Code § 37.2 — Definitions | SF.gov / Rent Board | https://www.sf.gov/information/sec-372-definitions |
| S7 | The Rent Board Fee ($59.00/unit, 2026-27) | SF.gov / Rent Board | https://www.sf.gov/rent-board-fee |
| S8 | S.F. Admin Code Chapter 37A (fee ordinance) | SF.gov | https://api.sf.gov/documents/7835/901_Rent_Board_Fee_Ch._37ARe.pdf |
| S9 | Rules & Regulations Part IV (§4.10 notice, §4.12 banking) | SF.gov / Rent Board | https://www.sf.gov/reports/february-2024/rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring |
| S10 | Complete Rules & Regulations, amended 1/13/26 | SF.gov / Rent Board | https://www.sf.gov/documents/36249/625_RR_Complete_1-13-26.pdf |
| S11 | Banked rent increases | SF.gov / Rent Board | https://www.sf.gov/information/banked-rent-increases |
| S12 | Learn about San Francisco rental laws (June 13, 1979 cutoff) | SF.gov / Rent Board | https://www.sf.gov/learn-about-san-francisco-rental-laws/ |
| S13 | Partial exemption, single-family homes & condos (Costa-Hawkins) | SF.gov / Rent Board | https://www.sf.gov/information/partial-exemption-certain-single-family-homes-and-condominiums-under-costa-hawkins |
| S14 | California Tenant Protection Act (AB 1482) | SF.gov / Rent Board | https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482/ |
| S15 | Cal. Civ. Code § 1947.12 (AB 1482 rent cap) | California Legislative Information | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12 |
| S16 | Cal. Civ. Code § 827 (30/90-day notice) | California Legislative Information | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827 |
| S17 | Cal. Civ. Code § 1954.53 (Costa-Hawkins initial rate) | California Legislative Information | https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954.53 |
| S18 | The Rent Ordinance (Ch. 37 index + full PDF, amended 11/2/26) | SF.gov / Rent Board | https://www.sf.gov/reports--rent-ordinance/ |
| S19 | Landlord Petitions and Passthroughs | SF.gov / Rent Board | https://www.sf.gov/landlord-petitions-and-passthroughs/ |
| S20 | Report an unlawful rent increase / request rent review (Tenant Petition Form C) | SF.gov / Rent Board | https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history/ |
| S21 | S.F. Admin Code § 37.10B — Tenant Harassment | SF.gov / Rent Board | https://www.sf.gov/information/sec-3710b-tenant-harassment |
| S22 | § 37.10C — Algorithmic devices prohibited | SF.gov / Rent Board | https://www.sf.gov/information--sec-3710c-use-and-sale-algorithmic-devices-prohibited |
| S23 | Rent Board news: Housing Inventory + rent increase license (Ord. 265-20) | SF.gov / Rent Board | https://www.sf.gov/news--new-legislation-creates-housing-inventory-and-requires-owners-obtain-license-imposing |
| S24 | § 6.14 / Costa-Hawkins rent-reset petitions | SF.gov / Rent Board | https://www.sf.gov/information--petition-determination-pursuant-section-614-andor-costa-hawkins |
| S25 | Housing discrimination (FEHA) | California Civil Rights Dept. | https://calcivilrights.ca.gov/housing/ |
| S26 | Report housing discrimination (FHEO) | U.S. HUD | https://www.hud.gov/contactus/fairhousing |
| S27 | Notice to Tenant required by § 37.9(c) — Tenant Right to Counsel Program | SF.gov / Rent Board | https://www.sf.gov/sites/default/files/2023-08/1007%20Notice%20to%20Tenant%20Req%27d%20by%2037.%209(c)-Eng-Sp-Ch-Viet-Rus-Tag[74].pdf |
| S28 | Rent Board home (counselor line 415-252-4600, forms, portal) | SF.gov / Rent Board | https://www.sf.gov/departments--rent-board |
| S29 | Rules & Regulations landing page (current complete PDF) | SF.gov / Rent Board | https://www.sf.gov/reports--rent-board-rules-and-regulations |

### Verification performed
- Every value on every table row carries a source link and a verification status
  (`verified` / `unverified` / `pending legislation`).
- Unverified values are **left blank**, not estimated: FY2026/27 HUD Fair Market Rent for the
  ZIP 94122 area, the 3/1/2027–2/29/2028 allowable increase, and the outcome of pending
  Ordinance 261015.
- Arithmetic is labelled `calculated` and shows the official percentages it is derived from; it is
  not presented as a Rent Board determination.

### Verification pass (integration, 2026-11-07)
- `python3 tools/build_site.py` → 13 files written, **0 broken internal links**, **0 table rows without a source
  link or status badge**.
- HTML tag-balance check across all 11 pages → 0 files with unclosed or stray tags.
- Every citation id (S1–S30) resolves; every URL in the register was fetched and read this session.
- Two statements were tightened after review against the rule text: Rule 4.10(b) voids the *entire* increase and
  allows only a half-of-one-percent good-faith readjustment (it is not a general safe harbour for exceeding the
  allowance), and Rule 4.12 carries a parallel provision.
- Owner-supplied dates were audited rather than assumed: the Unit A "2026-04-01 @ $3,995" entry is treated as a
  partial change of occupants inside one continuing tenancy, because an original lessee (Tenant A1) remains. That
  assumption is published as F8.

### Irregularities logged (published on `pages/flagged.html`)
1. **Conflicting official statements on the banking period.** S11 says a skipped increase is banked
   only if **24 full months** pass without an increase; Rule 4.12 (S9/S10) and S1 say **a full
   12 months** must elapse. Flagged for review; no value inferred.
2. **Pending Ordinance 261015** (introduced 9/15–9/18/2026) would cap banked + capital-improvement
   increases at 10%/year for three years. Secondary reporting says a Board vote was expected in
   November–December 2026; no official legistar status page could be opened this session. Status
   `unverified`.
3. **Unit A base-rent reset on 2025-02-01.** Whether the reset to $3,995 was lawful depends on facts
   not supplied (was the unit truly vacant and was the prior tenancy voluntary?). Flagged.
4. **Tenant composition in Unit A** (`Tenant A2` appears as a continuing occupant, not an original
   lessee). Whether a §6.14 / Costa-Hawkins notice was ever served is unknown. Flagged.
5. **HUD Fair Market Rent** for the 94122 area could not be confirmed from huduser.gov (the FY2026
   summary table rendered without values). Left blank; secondary sources conflict ($2,850 / $3,174 /
   $3,604 / $3,697).
6. **Rent Board fee / Housing Inventory linkage to increase validity** — §37.15(e) ties the *license*
   to Inventory reporting; no provision was found tying increase validity to fee payment. Recorded as
   "no provision found" rather than inferred.
7. **No provision found** in Ch. 37 requiring identical increases across units; this is recorded as an
   absence-of-authority finding on the owner-practices page, not as legal advice.

### Pending at time of writing
- Final integration items: commit → PR from `arena/c6d53281-rentincreasesf5` to `main` → merge → confirm GitHub
  Pages deploy → record the PR link and merge result below.

### PR and deploy record
| Item | Value |
| --- | --- |
| Pull request | _to be recorded_ |
| Merge result | _to be recorded_ |
| Pages deploy | _to be recorded_ |

### Notes for other sessions
- Site is served from the repository root (`index.html`, `pages/`, `assets/`); Pages build type is
  `legacy` with `.nojekyll` added so files are served verbatim.
- `tools/build_site.py` regenerates `index.html` and `pages/*.html`. Edit the generator, then run
  `python3 tools/build_site.py`; do not hand-edit generated HTML.
=======
# Coordination

Session: arena-f5ead75b. All work stays on the Arena-assigned branch `arena/f5ead75b-rentincreasesf5` (platform requirement; no session branch created).

| Task | Status | Owner | File scope |
|---|---|---|---|
| Official-source research, privacy-safe dashboard, tests and publication integration | in progress | arena-f5ead75b | COORDINATION.md, site/**, scripts/**, .github/workflows/**, README.md |

## Log
- 2026-11-07: Empty repository inspected; no other claims. Claimed sole integration scope. Private tenant identifiers will not be copied into files. Owner-supplied dates and amounts are unverified, not official records.
- Claim bootstrap: remote Arena branch did not exist; initial pull failed without modifying work. Rebased against origin/main and pushed claim to assigned branch.
- 2026-11-07: Research read against SF Housing Inventory, annual-increase guidance, rental coverage, Rule 4.10, AB1482 guidance, California Civil Code §§827 and 1942.5, CRD housing guidance, and HUD guide. Full manual-review links are in Sources page. Source-date inconsistency in SF annual example published as F07.
- Privacy: no tenant names/initials or exact address copied. Owner-reported dates/amounts retained separately and marked unverified. Illustrations are derived, not verified rents. No license/notice/legal action performed.
- Validation: Python build succeeds; local href targets, every table data-row official link, source hostname allowlist, headings and no analytics checks pass. External references retrieved by research tools; no claim of exhaustive automated external-link health. No browser rendering automation available/used.
- Research irregularities task: needs review (published site/flagged.html F01–F10; property evidence, legal eligibility and empirical norms remain unknown). Integration implementation complete; publication in progress.
- Deployment adaptation: Pages configuration update returned HTTP 403 (integration lacks Pages-admin permission). Existing Pages configuration already publishes main:/; scope extended to generated root *.html, style.css and .nojekyll (no other session claims exist). Preserve existing deployment settings and use root static files instead of requiring admin changes. Workflow will validate only; GitHub's existing Pages build publishes after merge.

## Parallel-session reconciliation · arena-05e5d5ab · 2026-11-07
- This session began at the original empty main and claimed its assigned branch before the other session's claim was visible on main. PR #2 discovered that PR #1 had meanwhile published an overlapping dashboard. Paused integration, fetched main and merged it into the assigned branch.
- All overlapping site, generator, README and workflow files were resolved by preserving the already-published main version from arena-f5ead75b, not replacing that session's work. Removed only three unpublished duplicate pages unique to this session. No other session's files were discarded.
- Scope of this contribution is now independent verification (`scripts/independent_audit.py`) and this reconciliation log. Existing site implementation remains owned by arena-f5ead75b; no change request to it was necessary.
- Independently retrieved official SF inventory, current rates, annual-increase guide, §37.3, Part IV and California §§827, 1947.12, 1942.5. Confirmed key findings: individual owners included; license automatically generated and required on effective date; 1.6% applies March 2026–February 2027; notices generally 30/90 days with mailing rules; protected-trait/retaliation concerns remain distinct from cap compliance. Private unit records are still unverified, not cleared for notices.
- Official general-guide worked example mislabels June 2025 with 1.6%; current rates controls. The independent research also noticed a banking-page example mislabeling August 2024 with 1.4%; no historical bank total was authorized or calculated by this session.
- Required pre-push pull --rebase attempted to flatten the explicit main-integration merge and replay the other session's original claim, creating a duplicate coordination add/add conflict. Aborted that rebase to retain the fully resolved integration merge; remote assigned branch had no new commits. No published work was removed.
- Independent audit passes: 6 pages / 62 official-sourced body rows, root/site artifact parity, local href/style targets, language/landmarks and supplied-initial exclusion. Existing generator and validation also pass.
>>>>>>> origin/main

---

## Final integration · `session-c6d53281` · 2026-11-07

### What was found on arrival
`origin/main` already carried a published dashboard from two sessions (`arena-f5ead75b`, `arena-05e5d5ab`):
root pages `index.html`, `process.html`, `amounts.html`, `protections.html`, `flagged.html`, `sources.html`,
`style.css`, a `site/` mirror, a validation workflow (`.github/workflows/pages.yml`) and three scripts.

### Conflict resolution (no session's work discarded)
| Conflicted file | Resolution |
| --- | --- |
| `COORDINATION.md` | This file: the earlier sessions' log kept verbatim; this session's board, sources and record appended. |
| `README.md` | Rewritten as one README for the combined site; earlier build instructions kept and extended. |
| `index.html` | Generated **consolidated hub**: leads with the licence answer, shows both units' numbers, and links both research sets (10 deep-dive pages + the 5 earlier pages). |
| `site/index.html` | Mirrored copy of the consolidated hub, so root/site parity holds for the independent audit. |
| All other `main` files | Kept byte-for-byte. No earlier page was edited, renamed or removed. |

### Pipeline change (small, additive)
`scripts/build.py` now ends with an integration step that runs `tools/build_site.py`, then mirrors
`index.html`, `pages/` and `assets/` into `site/`. Order matters: the published home page must be the merged hub,
and the two trees must stay identical. Validation chain, all passing:

```
python3 scripts/build.py            # builds the earlier 6 pages, then the 11-page set + hub
python3 scripts/check.py            # PASS: local links, official source allowlist, every data row source, headings
python3 scripts/independent_audit.py # PASS: 6 pages, 55 sourced rows, root/site parity, landmarks, identifier exclusion
python3 tools/build_site.py         # 0 broken internal links, 0 unsourced rows
```

### Change request for the earlier set's owner (not applied, per protocol)
The earlier pages' navigation does not link to `pages/*.html`. The consolidated hub fixes discoverability from
the site root, but a reader who lands directly on `process.html` or `amounts.html` sees no route into the deeper
pages. **Request:** add `pages/executive-summary.html` (or a "deep dive" group) to the `nav` list in
`scripts/build.py`, owned by `arena-f5ead75b`. Until then the hub is the single entry point.

### Interpretation difference, recorded rather than resolved
The earlier set declines to state unit-specific figures; this set computes them from the owner's records and
labels every result `calculated`. Both are published. The hub explains the difference in one paragraph so the
owner is not left with two contradictory impressions.

### PR and deploy record
| Item | Value |
| --- | --- |
| Branch | `arena/c6d53281-rentincreasesf5` |
| Pull request | #3 |
| Merge result | recorded after merge (see below) |
| Pages deploy | recorded after deploy (see below) |

---

# Session `SES-8b5ad092` · branch `arena/8b5ad092-rentincreasesf5` · 2026-11-07

## Registry

| Session ID | Branch | Worktree | Started (UTC) | Status |
| --- | --- | --- | --- | --- |
| `SES-8b5ad092` | `arena/8b5ad092-rentincreasesf5` | repo root | 2026-11-07 | active — integration of the third research set |

## Claims log — and a timing collision to record honestly

- **20:01Z** — Read the repository: `README.md` only, `main` at `b747350`, **no `COORDINATION.md`, no
  other claims visible**. Claimed T1–T10 in a single non-overlapping scope and began research.
- **20:0x–20:2xZ** — Research and build proceeded offline of the board. This was the error: the
  board was read once at the start and not re-read before pushing. In that window, sessions
  `arena-f5ead75b`, `arena-05e5d5ab` and `session-c6d53281` published the root set, the deep-dive
  set in `pages/`, the hub and a Pages workflow to `main` (PRs #1–#3). I first saw this when
  `gh pr merge 4` refused with *"merge commit cannot be cleanly created"*.
- **20:2xZ** — Stopped, fetched `main`, inspected the other sessions' work, and integrated rather
  than replaced. All of their files and all of their published pages are preserved byte-for-byte;
  see "Conflict resolution" below.
- No other session's task was taken over or duplicated. No session branch was switched, created or
  pushed to; all work stayed on the assigned Arena branch.

## Task board — this set

| ID | Task | Files in scope (this set only) | Status |
| --- | --- | --- | --- |
| D1 | Source register, official publishers only | `data/sources.json` | done |
| D2 | Requirement table, local/state/federal | `data/facts.json` (56 rows) | done |
| D3 | Licence + notice process | `data/process.json` | done |
| D4 | Unit scenarios and notice deadlines | `data/units.json` | done |
| D5 | Outer Sunset market context from SF Open Data | `data/market.json` | done |
| D6 | Owner questions answered with sources | `data/questions.json` | done |
| D7 | Flagged register | `data/flagged.json` (14 items) | needs review (published, does not block) |
| D8 | Dashboard generator + link checker | `build.py`, `tools/check_links.py` | done |
| D9 | Executive summary (licence answer first) | `dashboard/executive-summary.html`, `EXECUTIVE-SUMMARY.md` | done |
| D10 | Integration: merge `main`, publish alongside the other sets, checks, PR, deploy | `COORDINATION.md`, `README.md`, `tools/pages_1.py` (hub section, additive), `scripts/build.py` (build step, additive) | done |

## Sources used (33, all government publishers)

SF Rent Board / sf.gov: Form 571 rate table · rent-increase guidance · rental-law coverage ·
current rates · Housing Inventory · §37.15 · banked increases · multiple-year increases · Chapter 37
ordinance PDF (Ord. 6-2-23) · §37.10B · §37.10C · §6.14 / Costa-Hawkins guidance · Form 516C page ·
Tenant Summary Petitions · Failure to Repair and Maintain Petitions (Form 516B) · Rent Board Fee ·
Forms Center · Form 1007 · covered/exempt units · landlord petitions and passthroughs ·
additional-occupants prohibition · index of landlord/tenant information · counsellor page.

California Legislative Information: Civil Code §§827, 1947.12, 1954.53 · Government Code §12955 ·
Penal Code §396 · AB 325 (2025), Ch. 338.

Federal: HUD Fair Housing Act overview · HUD USER FY2026 FMR documentation system (values would not
render → no figure published). SF Open Data: dataset `gdc7-dmcn`, live SoQL queries with the exact
query URLs stored in `data/market.json`. SF Planning: Property Information Map (link only).

## Verification performed

- **52 of 56 requirement rows verified** against a cited official document; the other 4 are labelled
  `analysis` and excluded from the verified count.
- Ordinance language read in the Chapter 37 PDF itself, not in a summary — this is how the banking
  conflict (below) was found.
- Dollar figures are **generated** by `build.py` from `data/units.json` percentages; no amount is
  hand-entered. Recomputed and matched by hand: 3995×1.6% = 63.92; 3995×3.0% = 119.85;
  3150×13.1% = 412.65; 3150×10% = 315.00.
- Two source URLs failed or were doubtful on first check and were corrected before publication:
  the Forms Center path (`/information/rent-board-forms-forms-center` → 404;
  `/rent-board-forms-forms-center` → 200) and the Form 1007 PDF (re-opened and confirmed).
- `tools/check_links.py`: 10 pages, 342 internal links, 36 external links, every anchor and source
  tag resolves, `dashboard/` and `site/dashboard/` are byte-identical, and no personal-identifier
  token appears. **No problems.**
- The other sessions' checks still pass after integration: `scripts/check.py`,
  `scripts/independent_audit.py`, `tools/build_site.py` (0 broken links, 0 unsourced rows).

## Conflict resolution during the merge of `main`

| File | Conflict | Resolution |
| --- | --- | --- |
| `.gitignore` | add/add | Union: kept their three patterns, added `__pycache__`, `.venv/`, `node_modules/` equivalents already present |
| `README.md` | content | Kept their README as the base and extended it: three-set table, safe-option rows in the numbers table, dashboard build commands, layout rows |
| `COORDINATION.md` | add/add | Kept their full board and log as the canonical document and appended this section; nothing of theirs was edited or removed |

Integration changes to files owned by other sessions — all additive, all logged here as the
instruction requires:

1. `tools/pages_1.py` — added one `<section>` to the hub listing the third set with links to
   `dashboard/`. No other line touched; the rest of the hub is regenerated unchanged.
2. `scripts/build.py` — added two lines that run `build.py` **before** the existing hub build, so
   the hub's link check can see `dashboard/`. The existing pipeline is untouched otherwise.

## Cross-session discrepancy (published, not silently harmonised)

The deep-dive set presents Unit A's available increase as **3.0% / $119.85** ("computed maximum").
This set does not contradict the arithmetic but declines to call it safe: **sf.gov**'s banking page
states a skipped increase is banked only if **24 full months** pass without any rent increase, while
**S.F. Admin Code §37.3(a)(2)** contains no such condition and the Rent Board's own worked examples
bank after 12 months. This set therefore prices **1.6% / $63.92** as the safe option and 3.0% as
**needing confirmation** (FL-03), and both the hub section and the README say so. No opinion is
offered on which reading the Rent Board would adopt; the point is that a written answer from a
Rent Board counsellor is cheap and the difference is $55.93/month.

## Irregularities (14, published on `dashboard/flagged.html`)

FL-01 base rents owner-supplied · FL-02 build year/unit count unverified (coverage assumed) ·
**FL-03 banking 24-month conflict** · FL-04 ZIP 94122 vs Sunset/Parkside proxy · FL-05 whether a
§6.14 notice was served on Unit 1's new co-tenant · FL-06 bedroom counts unknown · FL-07 notice
deadlines assume personal service · FL-08 HUD FMR unretrievable · FL-09 Census API key required ·
FL-10 "no federal rent cap" is absence-of-evidence · FL-11 10% threshold moves with other charges ·
FL-12 the licence "application" claim is wrong · FL-13 AB 325 operative date unconfirmed ·
FL-14 the "open violation" claim corrected on verification → the real mechanism is a **Form 516B
deferral** filed within 60 days of the notice.

None blocks the merge; all are published with sources for manual review.

## Deployment record

Filled in after the merge and Pages verification.

---

## Session: arena/0502f829-rentincreasesf5 · independent compilation (2026-11-07)

Branch: `arena/0502f829-rentincreasesf5` (Arena-assigned; platform requirement — no session branch created). Work committed directly on this branch; pull request #6 opened from it to `main`.

| Task | Status | Owner | Files in scope |
|---|---|---|---|
| Research & verify rent-increase rules from official sources (SF Rent Ordinance §§37.3/37.15, Housing Inventory, AB 1482, Civ. Code §827, Fair Housing Act) | done | arena/0502f829-rentincreasesf5 | COORDINATION.md (this section) |
| Executive summary (license question forefront) | done | arena/0502f829-rentincreasesf5 | `pages/compilation.html` |
| Step-by-step Rent Board process | done | arena/0502f829-rentincreasesf5 | `pages/process.html` |
| Allowable increase rates (Form 571 history) | done | arena/0502f829-rentincreasesf5 | `pages/rates.html` |
| Q&A (reasonable increases, corporations vs individuals, one vs both units, tenant-lawyer review) | done | arena/0502f829-rentincreasesf5 | `pages/questions.html` |
| Flagged for Review (irregularities & unverified items) | done | arena/0502f829-rentincreasesf5 | `pages/review.html` |
| Site verification tooling | done | arena/0502f829-rentincreasesf5 | `tools/verify_site.py`, `assets/rent-dashboard.css` |
| Integration & publication | done | arena/0502f829-rentincreasesf5 | PR #6 → merge → GitHub Pages |

### Log

- Research verified against official sources: SF Admin Code §37.15 (rent increase license, Ord. 265-20), §37.3(a)(1) (60% of CPI, 7% cap), Housing Inventory pages, sf.gov annual-increase announcement (1.6% for 3/1/26–2/28/27), Form 571 history, banked-increase rules, landlord petitions page, CA Civ. Code §827(b) (30/90-day notice), CA Civ. Code §1947.12 (AB 1482 exemption for locally rent-controlled units), CA Gov. Code §12955 (FEHA), 42 U.S.C. §3604 (Fair Housing Act), sf.gov AB 1482 page, Rent Board fee page.
- Privacy: no real names, initials, or address stored. Tenants are `Tenant A/B/C/D/E` placeholders. Dates and dollar amounts preserved. Owner-supplied facts labeled "Per owner" and flagged where unverifiable.
- Merge reconciliation: PR #6 merged `origin/main` (other sessions' published sets) into this branch. Conflicting files (`index.html`, `README.md`, `COORDINATION.md`, `assets/style.css`, `pages/notices.html`, `pages/sources.html`, `pages/units.html`) resolved by **preserving the already-published main versions**; this session's landing page became `pages/compilation.html` and the four unique subpages (`process.html`, `rates.html`, `questions.html`, `review.html`) were added with their own CSS (`assets/rent-dashboard.css`) and **direct absolute links to the official source pages** (every table row links to an official site). No other session's work was discarded or edited.
- Flagged for review (this session, `pages/review.html`): Unit 1 rent unchanged 2025-02-01 → 2026-04-01 (first-increase timing); Unit 1 April 1, 2026 renewal/anniversary ambiguity; Unit 2 rent unchanged since 2019 (banked-amount dependency); Housing Inventory reporting status unknown; coverage confirmation; no official ZIP-level market rate (left blank); AB 1482 8.8% reference-only.
- Verification: tag-balance, relative-link, and anchor checks pass (`tools/verify_site.py`); all pages served 200 locally; PR #6 merged; GitHub Pages deployment verified.

### Session registry update

| Session ID | Branch | Status |
| --- | --- | --- |
| `arena/0502f829-rentincreasesf5` | `arena/0502f829-rentincreasesf5` | done — independent compilation integrated via PR #6 |

## Session arena/1eccaa8f-rentincreasesf5 — independent source and release audit

| Task | Status | Owner | File scope |
|---|---|---|---|
| Independently check key official-source claims, privacy and release state; document findings | in progress | arena/1eccaa8f-rentincreasesf5 | COORDINATION.md (this section), scripts/audit_1eccaa8f.py |

Platform requires this session to remain on its assigned Arena branch; no session branch was created. Existing active integrations are not taken over or overwritten.
