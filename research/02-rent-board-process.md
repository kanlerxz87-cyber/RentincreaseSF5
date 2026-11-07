# Rent Board Process — line-by-line verification

Companion to `data/process.json` and `data/requirements.json`. Every assertion is checked against an official government page. This document exists so a reviewer can walk the same lines without relying on the rendered site.

## A. The question asked

> "I read that I need to inform the rent board and apply for a license in order to prevent the rent increase from being challenged. I am just an individual property owner and not part of a corporation, so do I still need to apply for the license and inform the rent board before notifying tenants of a rent increase?"

**Verified answer, decomposed:**

| Claim in the question | Official finding | Source |
|---|---|---|
| "inform the Rent Board" | Yes, but the mechanism is the **annual Housing Inventory report**, not a notice of the specific increase. | [§ 37.15(a)-(c)](https://www.sf.gov/information--sec-3715-reporting-obligations-licensing), [Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) |
| "apply for a license" | Not a separate application: "**a rent increase license will be automatically generated for non-owner occupied units**" after reporting. | [Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) |
| "in order to prevent the rent increase from being challenged" | Incorrect premise. A license does not immunize an increase; tenant petitions are free with **no time limit**. | [Report an unlawful rent increase](https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history/), [Tenant Summary Petitions](https://www.sf.gov/information--tenant-summary-petitions/) |
| "before notifying tenants" | The controlling moment is the **effective date** of the increase, not the notice date. Rule 13.14: "the effective date of the rent increase, not the date of service, shall be used." | [Part XIII, § 13.14](https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-xiii-reporting-obligations-under-rent) |
| "I am just an individual property owner" | No exemption. § 37.15 applies to "**Owners**"; § 37.2(h) defines landlord without an entity-type carve-out. Buildings with fewer than 10 residential units (and condos) have been covered since **March 1, 2023**. | [§ 37.15](https://www.sf.gov/information--sec-3715-reporting-obligations-licensing), [§ 37.2](https://www.sf.gov/information--sec-372-definitions), [Housing Inventory](https://www.sf.gov/rent-board-housing-inventory), [Ord. 265-20](https://www.sf.gov/news--new-legislation-creates-housing-inventory-and-requires-owners-obtain-license-imposing) |

**Direct quotations checked:**

1. "All owners of residential property are required to report." — [sf.gov Housing Inventory](https://www.sf.gov/rent-board-housing-inventory)
2. "once you have reported into the Housing Inventory, a rent increase license will be automatically generated for non-owner occupied units." — same page.
3. "A landlord must have a current rent increase license on file with the Rent Board before any annual or banked rent increase can go into effect. The rent increase license does not need to be included with your rent increase notice." — same page.
4. "A current Rent Increase License must be on file with the San Francisco Rent Board before any annual or banked rent increase goes into effect." — [Notice of Owner Noncompliance](https://www.sf.gov/notice-of-owner-noncompliance-with-housing-inventory)
5. "A landlord may increase the tenant's base rent once every 12 months by the amount of the allowable annual rent increase without filing a petition at the Rent Board." — [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf)
6. "Any rent increase under Ordinance Sections 37.3(a)(1)-(2) purporting to be effective while the landlord is unlicensed shall render the entire rent increase null and void." — [§ 13.14](https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-xiii-reporting-obligations-under-rent)
7. "If a landlord has substantially complied … the landlord shall receive a license … If the landlord has not substantially complied … the license … shall be temporarily suspended." — [§ 37.15(e)](https://www.sf.gov/information--sec-3715-reporting-obligations-licensing)
8. "You can still make a Housing Inventory submission and receive a rent increase license after the deadline. However, your rent increase notice will not be enforceable without having a rent increase license on the effective date of the notice." — [Housing Inventory](https://www.sf.gov/rent-board-housing-inventory)

## B. Sequence, with the governing provision for each step

1. **Coverage** — [sf.gov rental laws](https://www.sf.gov/learn-about-san-francisco-rental-laws/), [Property Information Map](https://sfplanninggis.org/PIM/). Built on/before June 13, 1979, not single-family → "may have both" rent control and eviction protection.
2. **Annual report (March 1)** — [§ 37.15(b),(c)](https://www.sf.gov/information--sec-3715-reporting-obligations-licensing); required data list (A)–(G); under penalty of perjury; 30-day update for contact changes.
3. **License generated** — [Housing Inventory](https://www.sf.gov/rent-board-housing-inventory); [§ 37.15(e)](https://www.sf.gov/information--sec-3715-reporting-obligations-licensing).
4. **Verify in Portal** — [sf.gov noncompliance notice](https://www.sf.gov/notice-of-owner-noncompliance-with-housing-inventory), [Portal](https://portal.sfrb.org/).
5. **Fee** — [Rent Board Fee](https://www.sf.gov/rent-board-fee) ($59.00 per dwelling unit 2026-27; 50% recoverable).
6. **Amount + timing** — [sf.gov rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco), [Current Rates](https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit), [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf), [§ 37.3(a)(1)-(2)](https://www.sf.gov/information--sec-373-rent-limitations).
7. **Notice** — [Civil Code § 827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=827&lawCode=CIV), [§ 37.3(b)](https://www.sf.gov/information--sec-373-rent-limitations), [Rule 4.10](https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring).
8. **Effective date** — license still current; [§ 13.14](https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-xiii-reporting-obligations-under-rent).
9. **Records / challenge** — [Report an unlawful rent increase](https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history/).

## C. When a petition IS required

[sf.gov — Landlord Petitions and Passthroughs](https://www.sf.gov/landlord-petitions-and-passthroughs): "For certain types of rent increases, landlords must file a petition at the Rent Board **before** serving the tenants with a notice of the increase. The tenants are not required to pay the increase until the Rent Board approves it." Six categories: capital improvement passthrough; O&M expense increase; special circumstances/comparable rents; Proposition I past rent history; utility passthrough; Rule 1.21. Optional petitions: § 6.14 / Costa-Hawkins determination, exemption determination, protected status, lawful-rent determination, housing-services reduction.

## D. Contradictions found (see Flagged for Review)

- **Licensing start dates:** § 37.15(c)/Rule 13.14 (7/1/2022, 3/1/2023) vs official [Form 538](https://www.sf.gov/sites/default/files/2024-10/538%202024-25%20Bond%20Measure%20Worksheet%2010.24%20.pdf) (7/1/2020, 3/1/2021).
- **Remedy:** § 37.15(e) (tenant not obligated for months during suspension) vs § 13.14 (entire increase null and void).
- **Banking window:** [Rule 4.12(a)](https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring) (full 12 months) vs [sf.gov banked page](https://www.sf.gov/information--banked-rent-increases) (at least 24 full months).
- **Ordinance text authority:** [Rent Ordinance index](https://www.sf.gov/reports--rent-ordinance) disclaims being the official record.
- **Third-party errors:** "apply for" the license / notice-before-license / 60-day notice for ≥10% — all contradicted by official sources listed above.
