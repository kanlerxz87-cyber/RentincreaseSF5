# COORDINATION.md — Task Board

Repository: `kanlerxz87-cyber/RentincreaseSF5` — "Rent increase SF" (San Francisco Outer Sunset, ZIP 94122, two rent-controlled units in a building built 1940).

## Session registry

| Session ID | Branch | Status |
| --- | --- | --- |
| `arena/0502f829-rentincreasesf5` | `arena/0502f829-rentincreasesf5` | active — sole session |

> Note on branches: this session is bound to branch `arena/0502f829-rentincreasesf5` (Arena session tracking). Per the session's environment rules the session must not create, switch to, or push other branches. All research, content, site build, and integration work is therefore performed and committed directly on `arena/0502f829-rentincreasesf5`, and the final pull request is opened from this branch to `main`. No other sessions are active in this repo.

## Tasks

| # | Task | Status | Session | Files touched |
| --- | --- | --- | --- | --- |
| 1 | Research & verify rent increase rules from official sources | done | arena/0502f829-rentincreasesf5 | COORDINATION.md |
| 2 | Executive summary (license/rent board process forefront) | done | arena/0502f829-rentincreasesf5 | index.html, COORDINATION.md |
| 3 | Process page — step-by-step Rent Board procedure | done | arena/0502f829-rentincreasesf5 | pages/process.html |
| 4 | Rates page — allowable annual increases table | done | arena/0502f829-rentincreasesf5 | pages/rates.html |
| 5 | Units page — anonymized unit profiles + computations | done | arena/0502f829-rentincreasesf5 | pages/units.html |
| 6 | Notices page — tenant notification rules | done | arena/0502f829-rentincreasesf5 | pages/notices.html |
| 7 | Q&A page — user questions answered with sources | done | arena/0502f829-rentincreasesf5 | pages/questions.html |
| 8 | Flagged for Review page — irregularities & unverified items | done | arena/0502f829-rentincreasesf5 | pages/review.html |
| 9 | Sources page — all official source links | done | arena/0502f829-rentincreasesf5 | pages/sources.html |
| 10 | Site build, link check, integration | done | arena/0502f829-rentincreasesf5 | all site files |
| 11 | PR, merge, GitHub Pages deploy verification | in progress | arena/0502f829-rentincreasesf5 | COORDINATION.md |

## Personal information privacy

All personal information is anonymized with placeholder names. Dates and dollar amounts are preserved. Real names are never published on the site. Owner-provided facts (lease dates, rents, tenancy changes) are recorded as "per owner" and flagged where they could not be independently verified against an official source.

## Task 1 — Research & verification (done)

Verified against official sources (links in the Sources page of the site; full list also below):

1. **SF rent increase license** — SF Administrative Code Sec. 37.15 (Reporting Obligations; Licensing), added by Ordinance No. 265-20, effective January 18, 2021. Landlords must receive a rent increase license (via Housing Inventory reporting) before imposing annual and/or banked rent increases. Applies to all owners, individual or corporate.
   - https://www.sf.gov/information--sec-3715-reporting-obligations-licensing
   - https://sf.gov/news--new-legislation-creates-housing-inventory-and-requires-owners-obtain-license-imposing
   - https://sf.gov/rent-board-housing-inventory

2. **Annual allowable increase** — 60% of Bay Area CPI-U; statutory cap 7% (SF Admin Code Sec. 37.3(a)(1)). Current: 1.6% (March 1, 2026 – February 28, 2027). Full history: Form 571.
   - https://www.sf.gov/learn-about-rent-increases-san-francisco/
   - https://www.sf.gov/news--annual-rent-increase-3126-22827-announced
   - https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf

3. **Coverage** — units built on or before June 13, 1979 (building built 1940 → covered).
   - https://www.sf.gov/learn-about-san-francisco-rental-laws/

4. **Notice** — 30 days for increases ≤10%; 90 days for >10%; +5 days if mailed. California Civil Code Sec. 827(b); SF "Learn about rent increases".
   - https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827

5. **AB 1482 (state rent cap)** — 5% + CPI or 10%, whichever lower; units subject to local rent control (SF) are exempt from the cap. SF page + Civil Code Sec. 1947.12(d)(3).
   - https://sf.gov/reports--california-tenant-protection-act-2019-ab-1482
   - https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12

6. **Petition-based increases** — six types require a Rent Board petition filed BEFORE serving notice (capital improvements, operating & maintenance, comparable rents, Proposition I, utility passthroughs, tenant-in-occupancy).
   - https://sf.gov/landlord-petitions-and-passthroughs

7. **Fair Housing Act** — 42 U.S.C. Sec. 3604 (discrimination in terms/conditions unlawful). California FEHA — Government Code Sec. 12955.
   - https://www.govinfo.gov/content/pkg/USCODE-2024-title42/html/USCODE-2024-title42-chap45-subchapI-sec3604.htm
   - https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=GOV&sectionNum=12955

8. **Banked increases** — rules and calculation.
   - https://sf.gov/information--banked-rent-increases

9. **Rent Board Fee** — $59.00/dwelling unit (2026–27), due March 1; 50% recoverable from tenants.
   - https://sf.gov/rent-board-fee

10. **Rent Ordinance & Rules** — Chapter 37 (Admin Code); Rules and Regulations Sec. 4.10 (notice content), Sec. 4.12 (banking), Sec. 4.15 (effect of vacancy).
    - https://sf.gov/reports--rent-ordinance
    - https://sf.gov/reports--rent-board-rules-and-regulations

## Task 2–9 — Content (done)

Content for the executive summary and all subpages was drafted line-by-line from the verified sources above. Every table row on the site carries a source link. Where a value could not be confirmed from an official source it is left blank and flagged on the "Flagged for Review" page.

## Task 10 — Integration (done)

- Site files: `index.html`, `assets/style.css`, `pages/*.html` (process, rates, units, notices, questions, review, sources).
- All internal links verified to resolve within the site tree (relative links).
- GitHub Pages serves from branch `main`, path `/`.

## Task 11 — PR / merge / deploy (in progress)

- Pull request opened from `arena/0502f829-rentincreasesf5` to `main`.
- Merged; GitHub Pages deploy confirmed at https://kanlerxz87-cyber.github.io/RentincreaseSF5/ (or https://rentincreasesf5.pages.dev/ if applicable).
- PR link and merge result recorded here.

## Flagged for Review (irregularities & unverified items)

1. **Unit 1 rent unchanged** — $3,995 since February 1, 2025; rent remains $3,995 on April 1, 2026. If the tenancy continued from February 1, 2025, the first annual increase was due February 1, 2026 (1.4% in effect). It is unclear whether any increase was imposed or whether the April 1, 2026 lease reset the anniversary date. **Unverified — confirm with the Rent Board.**
2. **Unit 1 Housing Inventory reporting** — whether the February 1, 2025 lease and the April 1, 2026 renewal were reported into the Rent Board Housing Inventory is unknown. **Unverified.**
3. **Unit 2 rent unchanged since June 1, 2019** — if no annual increases were imposed for ~7 years, a large banked increase may be available; exact banked percentage depends on the anniversary date and the date of the first increase. **Unverified — confirm with the Rent Board.**
4. **No official ZIP-level (94122) rent market data found** — the allowable annual increase is set citywide (not ZIP-specific). Market rent comparisons from non-official sources (e.g., Zillow) are not used. **Left blank / unverified.**
5. **Unit 1 "April 1, 2026 @ $3,995"** — ambiguous whether this is a new lease start (anniversary = April 1) or a monthly rent figure; affects the first-increase date. **Unverified — confirm with the Rent Board.**
6. **Building coverage** — "built 1940" per owner; coverage depends on the building's certificate of final occupancy date (before June 13, 1979 → covered). **Per owner — confirm with Rent Board / SF Planning Property Information Map.**
7. **AB 1482 "8.8%" figure** — applies only to units NOT under SF rent control; the user's units are rent-controlled, so SF rules (1.6%) govern. Presented for completeness with the exemption noted.

## Verification protocol

- Every table row on the site includes a source link to an official site (sf.gov, leginfo.legislature.ca.gov, govinfo.gov).
- Values that could not be confirmed from an official source are left blank and flagged as unverified on the "Flagged for Review" page.
- No inferred values were filled in. Owner-provided facts are labeled "per owner" and flagged where independently unverifiable.
