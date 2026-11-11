# Verification log - session F46F7D0F (November 11, 2026)

Scope claimed in `COORDINATION.md`: `f46f7d0f/**`, `EXECUTIVE-SUMMARY-F46F7D0F.md`,
`VERIFICATION-F46F7D0F.md`, and this session's `COORDINATION.md` entries. No other session's files are
modified; irregularities found in them are published (flagged), not edited.

## Method

1. Re-read the full repository state after rebasing onto the latest `origin/main`; audited the files in
   scope line by line.
2. Fetched every official source live on November 11, 2026 (see register below). Form 571, the
   Sec. 37.15 text, the rent-increase guide (File No. 261020 notice) and the Rent Board Fee page were
   fetched twice - once during initial research and again after the mid-session rebase - with identical
   results.
3. Recomputed every dollar figure with exact decimal arithmetic and every serve-by date with calendar
   arithmetic inside the site's builder; assertions fail the build if any number drifts.
4. Self-check then enforces on every generated file: no initial-shaped or street-shaped personal
   patterns, no merge markers, balanced HTML, unique ids, exactly one h1, lang/main/title/viewport
   present, every data-table row carrying at least one direct official source link, all local links and
   anchors resolving, and no external URL outside the official allowlist.
5. The continuous-integration suite was then run locally: `scripts/build.py` (twice - reproducible),
   `scripts/check.py`, `scripts/independent_audit.py`, `tools/check_links.py`, `tools/release_gate.py`,
   `tools/repository_audit.py --no-page`, `tools/followup_audit.py` - all results recorded in the pull
   request and `COORDINATION.md`.

## Official source register (fetched November 11, 2026)

| ID | Publisher | Title | URL |
|---|---|---|---|
| S01 | City and County of San Francisco | Rent Board Housing Inventory - reporting instructions and portal access | <https://www.sf.gov/rent-board-housing-inventory> |
| S02 | City and County of San Francisco | San Francisco Administrative Code Sec. 37.15 - Reporting Obligations; Licensing | <https://www.sf.gov/information--sec-3715-reporting-obligations-licensing> |
| S03 | City and County of San Francisco | Learn about rent increases in San Francisco (Rent Board) | <https://www.sf.gov/learn-about-rent-increases-san-francisco> |
| S04 | City and County of San Francisco | Form 571 - Allowable Annual Rent Increases, 2026-27 edition (PDF) | <https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf> |
| S05 | City and County of San Francisco | Banked rent increases (Rent Board) | <https://www.sf.gov/information--banked-rent-increases> |
| S06 | City and County of San Francisco | Annual rent increases for multiple years (Rent Board) | <https://www.sf.gov/information/annual-rent-increase-multiple-years> |
| S07 | City and County of San Francisco | Rent Board Rules and Regulations Part IV - Rent increases not requiring approval (December 2022) | <https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring> |
| S08 | City and County of San Francisco | San Francisco Administrative Code Sec. 37.2 - Definitions | <https://www.sf.gov/information/sec-372-definitions> |
| S09 | City and County of San Francisco | San Francisco Administrative Code Sec. 37.3 - Rent Limitations | <https://www.sf.gov/information/sec-373-rent-limitations> |
| S10 | City and County of San Francisco | San Francisco Administrative Code Sec. 37.10B - Tenant harassment | <https://www.sf.gov/information/sec-3710b-tenant-harassment> |
| S11 | City and County of San Francisco | San Francisco Administrative Code Sec. 37.10C - Use and sale of algorithmic devices prohibited | <https://www.sf.gov/information--sec-3710c-use-and-sale-algorithmic-devices-prohibited> |
| S12 | City and County of San Francisco | Petition determination pursuant to Section 6.14 and Costa-Hawkins (Rent Board) | <https://www.sf.gov/information--petition-determination-pursuant-section-614-andor-costa-hawkins> |
| S13 | City and County of San Francisco | The Rent Board Fee | <https://www.sf.gov/rent-board-fee> |
| S14 | City and County of San Francisco | Landlord petitions and passthroughs (Rent Board) | <https://www.sf.gov/landlord-petitions-and-passthroughs/> |
| S15 | City and County of San Francisco | Learn about San Francisco rental laws - coverage guide (Rent Board) | <https://www.sf.gov/learn-about-san-francisco-rental-laws/> |
| S16 | City and County of San Francisco | California Tenant Protection Act of 2019 (state bill 1482) - Rent Board guide | <https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482> |
| S17 | City and County of San Francisco | Report an unlawful rent increase or request a review of your rent history (Rent Board) | <https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history/> |
| S18 | City and County of San Francisco | Form 1007 - Notice to Tenant required by Sec. 37.9(c) (multilingual PDF) | <https://www.sf.gov/sites/default/files/2023-08/1007%20Notice%20to%20Tenant%20Req%27d%20by%2037.%209(c)-Eng-Sp-Ch-Viet-Rus-Tag%5B74%5D.pdf> |
| S19 | State of California | California Civil Code Sec. 827 - written notice of rent increase | <https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=827&lawCode=CIV> |
| S20 | State of California | California Civil Code Sec. 1942.5 - retaliatory actions prohibited | <https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1942.5&lawCode=CIV> |
| S21 | State of California | California Civil Code Sec. 1947.12 - Tenant Protection Act rent cap | <https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1947.12&lawCode=CIV> |
| S22 | State of California | California Civil Code Sec. 1954.53 - Costa-Hawkins Rental Housing Act | <https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1954.53&lawCode=CIV> |
| S23 | State of California | California Government Code Sec. 12955 - FEHA housing discrimination prohibitions | <https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=12955&lawCode=GOV> |
| S24 | State of California | California Civil Rights Department - housing discrimination | <https://calcivilrights.ca.gov/housing/> |
| S25 | United States government | HUD - Fair Housing Act overview | <https://www.hud.gov/helping-americans/fair-housing-act-overview> |

Textual-only legislative cite (portal host sits outside the repository audit allowlist): Board of
Supervisors File No. 261020, legislative record 8217304, introduced 2026-09-15, pending Land Use and
Transportation Committee action as of November 11, 2026; the proposal is summarized and linked by
the City's own rent-increase page (S03).

## Arithmetic re-checks asserted in the builder

- Unit A: 3995.00 x 1.6% = 63.92 -> 4,058.92; 3995.00 x 3.0% = 119.85 -> 4,114.85.
- Unit B: 3150.00 x 1.6% = 50.40 -> 3,200.40; 3150.00 x 10.0% = 315.00 -> 3,465.00;
  3150.00 x 13.1% = 412.65 -> 3,562.65.
- Unit B banking stack: 1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 = 11.5 (additive only, Rule 4.12).
- Serve-by dates (verified by day count): 2027-01-01 minus 30/35 = 2026-12-02 / 2026-11-27;
  2027-02-01 minus 30/35 = 2027-01-02 / 2026-12-28; 2027-02-15 minus 90/95 = 2026-11-17 / 2026-11-12.
- Form 571: 46 published periods transcribed; 2027-28 deliberately blank; full match with
  `data/allowable-increases.csv` (repo audit row V01).

## Source irregularities caught while verifying

- The City's rent-increase page worked example attaches 1.6% to a June 1, 2025 effective date; the
  2025-26 allowance is 1.4%. The 2026-27 heading (1.6% for 2026-03-01 to 2027-02-28) is the correct
  statement. Persisting on November 11, 2026 (FR-12).
- The City's banked-increases page example mislabels an August 1, 2024 date with 1.4% (that period's
  rate was 1.7%); the rules text and Form 571 govern (FR-13).
- Repository items: internal notes cite 261015 instead of File No. 261020; Form 1007 URL appears with
  literal [74] rather than %5B74%5D in two places; two leginfo citations carry trailing periods; the
  archived base pages are stamped 07 Nov 2026, predating the 2026-11-09 File No. 261020 notice;
  historical public git history contains literal identifier tokens (earlier sessions' F15-class
  finding) that current-file edits cannot erase (FR-14 through FR-17).

## Limits

- Owner intake values (rents, dates, coverage, 1940 construction, occupant history) are not
  authenticated by any URL; they drive conditional arithmetic only and appear flagged.
- No inventory submission, license filing, tenant notice or attorney review was performed.
- The 2027-28 allowance was unpublished at research time; File No. 261020 was pending; recheck both
  before serving anything.
- Privacy: placeholder identities only in every tracked file; real identifiers were never committed.
