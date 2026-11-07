# Independent verification report — T6

**Session:** `session-a00d318d` / platform branch `arena/a00d318d-rentincreasesf5`  
**Initial report date:** 2026-11-07 UTC  
**Release status:** NOT A RELEASE PASS — the published combined site is present, but the independent audit found blocking publication defects. Existing session generators/checks pass; the stricter audit does not.

## Ownership and repo review

The initial repository contained only `README.md`, line 1: `# RentincreaseSF5`. A concurrent session subsequently published `COORDINATION.md` at commit `528c731` and claimed T1–T5 and integration T7. This session preserved that commit, claimed only T6, and pushed the claim before implementation. No research, data, index, navigation, or site page owned by the other session has been edited here.

## Implemented checks

- `scripts/verify.py`: standard-library-only CSV/JSON, HTML, source-domain, local-link/fragment, row-to-render mapping, privacy-term, optional external-HTTP and arithmetic checks.
- `scripts/tests/test_verify.py`: 26 synthetic tests, all passing at this checkpoint. No actual tenant identifiers are used in fixtures.
- `.github/workflows/verify.yml`: PR/dispatch verification job. Action revisions were checked against the official GitHub repositories and pinned by commit SHA.
- `docs/VERIFICATION-CONTRACT.md`: integration schema and release criteria, published for the owner of the shared outputs.

The published-tree audit now runs against the combined multi-set site. At the 2026-11-07 checkpoint it scanned 52 HTML pages, 974 HTML data rows and 152 CSV/JSON records. It confirms the existing local-link checks but fails release gates for unresolved hub tokens, row-level source gaps, review-link gaps and legacy provenance gaps. CI's exact-private-term audit is deliberately not claimed: that check requires private runtime input and must be run locally before release. CI also does not constitute a lawyer's review.

### Confirmed publication defects logged to the owning sessions

- `index.html` and `site/index.html` expose `CURRENT_PERIOD`, `A_DOLLAR`, `A_BASE`, `B_DOLLAR`, `B_BASE`; the live Pages hub showed the same unresolved tokens. Generator: `tools/pages_1.py:index()`.
- `data/units.json` / `dashboard/units.html` describe Unit 1 as one original tenant replaced. The owner supplied three initial occupants and two current occupants with one continuing original: two original occupants left and one new occupant joined. Do not infer a new tenancy or a §6.14 notice.
- Multiple table rows lack their own official-source hyperlink, including the pending-ordinance row in `pages/units.html`, benchmark/pending rows in `pages/executive-summary.html`, and unit summary rows in `dashboard/executive-summary.html`.
- `COORDINATION.md` on main contains leftover merge markers at lines 175/201.
- `dashboard/units.html` states no increase has been imposed since 2019/2025 as a fact; the owner did not supply a complete increase history. Keep calculations conditional.

These were posted to PR #5 and recorded in `COORDINATION.md` as change requests. This session did not edit the owned site/data files.

## Official-source reading performed for the audit contract

These checks support the verification requirements; they are not a substitute for the pending line-by-line review of the integrated research.

| Check | Official evidence read | Result |
|---|---|---|
| Individual owners and license | [SF Rent Board Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) requires residential owners to report; tenant-occupied reporting generates a license; a current license is needed before an annual/banked increase takes effect. | Confirmed agency guidance. No individual-owner exemption found in this guidance. Do not infer this property's actual license status. |
| Public-file privacy | [SF Rent Board Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) says submitted information is public and lists owner/business contact information among required filings. | Confirmed. Anonymous website labels do not make mandatory government filings anonymous. |
| Current increase rate | [SF Rent Board current rates](https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit) states 1.6% for March 1, 2026–February 28, 2027. | Confirmed rate and effective period, not an entitlement to increase either unit without the other prerequisites. |
| Notice and roommate rule | [SF Rent Board rent-increase guidance](https://www.sf.gov/learn-about-rent-increases-san-francisco) states 30 days, 90 days above 10%, five more days if mailed; it also says no additional rent merely for an additional roommate with an existing tenant. | Confirmed guidance. Actual prior increases, lease terms and service dates remain unverified. |
| Banking examples | [SF Rent Board rent-increase guidance](https://www.sf.gov/learn-about-rent-increases-san-francisco) explains anniversary changes and loss of an unbanked increase. [Rules Part IV](https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring) is the official rule page. | Confirmed guidance. Do not infer a banking balance from a lease date and rent alone. |
| Banking page wording irregularity | [Rent Board banking page](https://www.sf.gov/information--banked-rent-increases) has an August 1, 2025 effective-date example that subsequently refers to the annual rate “in effect on August 1, 2024” while giving 1.4%. | Flag for integration review: apparent date typo in the example; do not silently correct or use it to infer this property's bank. Use the rate table and Rule 4.12. |
| Fee is separate from inventory/license | [Rent Board Fee](https://www.sf.gov/rent-board-fee) states $59 per dwelling unit for 2026–2027, due March 1; fee-exemption requests do not satisfy Housing Inventory reporting. | Confirmed general rule. This owner's payment/exemption status is not verified. |
| State notice statute | [California Civil Code §827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=827&lawCode=CIV) states personal/mail service and 30/90-day thresholds for periodic residential tenancies. | Confirmed statutory text; do not apply periodic-tenancy rules to an unexamined fixed-term lease. |
| State cap/local overlap | [California Civil Code §1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12) includes the state cap and an exemption for stricter local rent control at (d)(3). | Confirmed text. The state 5%+CPI/10% formula is not a substitute for the local cap on a locally covered unit. |
| Retaliation | [California Civil Code §1942.5](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1942.5) prohibits retaliatory rent increases and preserves lawful-cause rights. | Confirmed text. No conclusion about either tenant's actual circumstances is possible without the missing history. |
| Coverage cannot be inferred from ZIP | [SF rental-law guidance](https://www.sf.gov/learn-about-san-francisco-rental-laws) describes the pre-June 14, 1979 category and exceptions and directs owners to property records/counselors. | Confirmed general guidance. Owner's 1940 construction statement is not an official certificate-of-occupancy or exemption determination. |
| Code-source irregularity | A guessed SF.gov ordinance URL returned a visible Not Found page; search then located [SF Administrative Code §37.15 on the official code publisher](https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_admin/0-0-0-16540). | Guessed URL rejected, not used as evidence. Official code location identified for proposition-level integration review. |
| CI action provenance | [checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1), [setup-python v7.1.0](https://github.com/actions/setup-python/releases/tag/v7.1.0), [upload-artifact v7.0.2](https://github.com/actions/upload-artifact/releases/tag/v7.0.2), and GitHub tag APIs for the pinned revisions. | Confirmed official action repositories/revisions. |

## Outstanding release gates

1. Owning integration sessions resolve the logged publication defects without discarding parallel work.
2. Read every substantive row against its official source; record mismatches and missing evidence, not just working URLs.
3. Run the strict external/local-link audit and exact sensitive-term audit with private input that is never committed or echoed.
4. Inspect the site at desktop/mobile sizes and verify the GitHub Pages base path and live deployment.
5. Hand findings to the owning integration session through `COORDINATION.md`; T7 remains its claimed task unless a documented stale-claim handoff occurs.

No tenant attorney has reviewed or approved this project. No such approval is claimed.
