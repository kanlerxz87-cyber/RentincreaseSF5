# COORDINATION.md — Shared Task Board

**Repository:** `kanlerxz87-cyber/RentincreaseSF5`
**GitHub Pages:** https://kanlerxz87-cyber.github.io/RentincreaseSF5/ (legacy build, source = `main`, path = `/`)
**Last updated:** 2026-11-07 (UTC)

This file is the shared task board for all agent sessions working in this repo.
Read it before starting work. Claim a task by writing your session ID below, commit, and push
the claim immediately. Never start a task another session has claimed.

---

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

### Handoff / takeover rule
If a session crashes or its claim is more than 60 minutes old with no commits, any other session
may take over the task and must note the handoff in the **Log** below.

---

## Session log — `session-c6d53281`

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

### Notes for other sessions
- Site is served from the repository root (`index.html`, `pages/`, `assets/`); Pages build type is
  `legacy` with `.nojekyll` added so files are served verbatim.
- `tools/build_site.py` regenerates `index.html` and `pages/*.html`. Edit the generator, then run
  `python3 tools/build_site.py`; do not hand-edit generated HTML.
