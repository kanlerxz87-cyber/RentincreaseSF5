#!/usr/bin/env python3
"""Reproducible standalone summary and regression checks for the November 8 audit.

Official pages were read with the page-fetch tool; these checks are local regression
checks, not a live legal-verification service or a substitute for lawyer review.
"""
from pathlib import Path
from decimal import Decimal

SUMMARY = '''# Executive summary — San Francisco rent increases

Key rules rechecked November 11, 2026 (re-verified against live official pages; prior recheck November 8, 2026). Research, not legal advice or permission to serve notices.

## First: an individual owner needs the rent-increase license too

**Yes: report the covered units to the Rent Board Housing Inventory. No: there is no separate license application or ordinary annual-increase approval petition.** Reporting a tenant-occupied unit automatically generates its license. It must be current **on the increase’s effective date**. The City does not say it must precede service of the notice; checking it before service is the recommended safer workflow. The license need not be attached to the notice, and it does not prevent a challenge for other violations.

The obligation applies to owners, not only corporations. Annual reporting is free and due March 1. Late reporting is possible, but noncompliance suspends the license; restoration is prospective, not a right to collect increases for suspended months. Required inventory submissions are public and made under penalty of perjury. Do not file public research placeholders as real facts.

Official sources: [Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) · [Administrative Code §37.15](https://www.sf.gov/information--sec-3715-reporting-obligations-licensing) · [Annual-increase guidance](https://www.sf.gov/learn-about-rent-increases-san-francisco).

## Beginner’s sequence

1. **Confirm coverage and lease restrictions.** The reported 1940 construction date and local rent-control status are intake statements, not property findings. Review the actual lease and any subsidy requirements. [Official coverage guide](https://www.sf.gov/learn-about-san-francisco-rental-laws).
2. **Check both units in the Rent Board Portal and report/update the Inventory.** Use authentic records, retain the submission and confirm a current license. Reporting is not a request to approve a particular percentage. [Inventory instructions and Portal link](https://www.sf.gov/rent-board-housing-inventory).
3. **Authenticate the lawful base rent and rent history.** Starting rent is not a complete ledger. Check increases, concessions and housing services; do not add temporary passthroughs to the base. A roommate change alone does not authorize a surcharge. [Annual rules](https://www.sf.gov/learn-about-rent-increases-san-francisco).
4. **Choose the effective date and calculate.** Ordinary annual increases require at least 12 months since tenancy start or the last increase. Use the allowance in force on the effective date, not service date. Delaying an increase can reset the anniversary; exact lease anniversaries are not mandatory forever. [Timing guidance](https://www.sf.gov/learn-about-rent-increases-san-francisco).
5. **Use banking only after reconstructing eligibility.** Eligible skipped percentages are added, not compounded; no rounding up. A proper ordinary annual/banked increase does not need a petition. Special petitions/passthroughs have separate rules. [Banking](https://www.sf.gov/information--banked-rent-increases) · [Multiple-year rules](https://www.sf.gov/information--annual-rent-increase-multiple-years).
6. **Prepare and serve the written notice.** State the dollar increase, percentage and effective date; identify any banked portion and its dates. Ordinary residential periodic-tenancy notices require at least 30 days for increases up to 10%, or 90 days above 10%, accounting for cumulative increases in the preceding 12 months. The City says to add five days for mailing; the statute incorporates the applicable mailing procedure. Do not assume email or text is sufficient. Review fixed-term lease restrictions separately. [Civil Code §827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) · [City notice guidance](https://www.sf.gov/information--banked-rent-increases).
7. **Retain the evidence and screen for unlawful motive.** Preserve leases, rent receipts, calculations, license evidence, notice and service proof. Review discrimination, accommodation, retaliation and harassment issues before acting. A neutral written policy is useful, not immunity. [CRD](https://calcivilrights.ca.gov/housing/) · [Civil Code §1942.5](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1942.5).

## What amount is reasonable?

For confirmed locally rent-controlled units, **1.6% is the published ordinary annual allowance for March 1, 2026–February 28, 2027**. It is a legal allowance, not proof of customary increases in ZIP 94122 or a requirement to impose the maximum. A smaller or zero increase is possible. Operating-cost concerns do not independently authorize exceeding the local allowance.

The following are **conditional arithmetic only**, not verified lawful rents. The amounts supplied by the owner remain unverified. They assume the stated amount is the present lawful base, the annual interval is satisfied, no lease/subsidy restriction bars the increase, and the license and notice requirements are met.

| Placeholder unit | Conditional annual-only increase | Conditional new monthly rent | Status | Official calculation source |
|---|---:|---:|---|---|
| Unit 1, using $3,995 | $63.92 (1.6%) | $4,058.92 | Computed, not cleared for service | [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) |
| Unit 2, using $3,150 | $50.40 (1.6%) | $3,200.40 | Computed, not cleared for service | [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) |

More aggressive banked scenarios on the site are conditional, not recommendations or verified entitlements. In particular, no intervening Unit 2 increases since 2019 was **not** established by the supplied information. The 12-month/24-month banking wording is discussed as interpretation, not an official property-specific ruling. No later annual rate is asserted here. A proposed temporary 10% cap on combined banked and capital-improvement increases (Board of Supervisors File No. 261020, noticed by the Rent Board on 9 November 2026) has not been enacted and is subject to change; recheck before serving any banked increase. [Official notice](https://www.sf.gov/learn-about-rent-increases-san-francisco). [Official banking rules](https://www.sf.gov/information--banked-rent-increases).

## Local, state and federal layers

San Francisco’s stricter applicable local cap is not replaced by AB 1482’s statewide cap. The City publishes 8.8% for AB 1482-covered SF units for August 1, 2026–July 31, 2027, but explicitly says that figure does not apply to units under the local rent-increase limits. Do not use 8.8% for the reported locally controlled units. [Official AB 1482 guide](https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482).

Federal fair-housing protections prohibit discrimination in housing terms. The reviewed HUD page does not establish a general federal numerical rent cap; subsidy status is unknown and may add separate restrictions. [HUD Fair Housing Act overview](https://www.hud.gov/helping-americans/fair-housing-act-overview).

## Corporations, individual owners, and raising one unit or both

No official empirical study of how the two owner types actually impose increases was confirmed. Suggested workflow for **either**: a compliance calendar, per-unit ledger, documented lawful calculation, proper written notice and service evidence. This is a recommendation, not a verified industry practice. [Official requirements](https://www.sf.gov/learn-about-rent-increases-san-francisco).

No uniform-increase requirement was identified in the reviewed rules. That does **not** prove that a particular selective increase is lawful. Raising both units is not automatic protection against discrimination; raising only one demands a factual review of motive, protected characteristics/activity, accommodation duties and tenancy history. Do not invent a business justification or use repair complaints as a reason. [CRD housing protections](https://calcivilrights.ca.gov/housing/) · [Retaliation statute](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1942.5).

## Tenant-side scrutiny and unresolved facts

No lawyer reviewed or approved an actual increase. Neither a license nor cap compliance guarantees a favorable legal review. Property coverage, complete rent history, license status, lease terms, service facts and discrimination/retaliation context remain unverified. The site's tenant-review page is a checklist, not certification. Free eviction defense does not imply automatic free representation for every rent-increase dispute.

The supplied tenancy dates and amounts remain preserved in the site’s anonymized intake ledger: February 1, 2025 at $3,995; continuing tenancy April 1, 2026 at $3,995; and June 1, 2019 at $3,150. They are not authenticated official records. No tenant names, initials, exact address or identifying documents are reproduced here. Dates and amounts may still permit re-identification.

See [Flagged for Review](hub/flagged.html), especially F01–F03, F15 (prior public-history privacy exposure), F17 (unsupported empirical norms), and F18 (banking assumptions). Earlier archived research may use stronger wording; this summary and the consolidated warnings control the follow-up audit. The historical privacy exposure has **not** been erased from git history, caches or forks. No notices or inventory submissions were made by this project.
'''


def write_summary(root):
    (Path(root) / 'EXECUTIVE-SUMMARY.md').write_text(SUMMARY, encoding='utf-8')


def check(root):
    root = Path(root)
    assert (root / 'EXECUTIVE-SUMMARY.md').read_text() == SUMMARY
    for base, amount in [('3995', '63.92'), ('3150', '50.40')]:
        assert Decimal(base) * Decimal('.016') == Decimal(amount)
    practices = (root / 'hub/practices.html').read_text()
    assert 'larger operators run a written annual' not in practices
    assert 'not a verified description of industry practice' in practices
    flagged = (root / 'hub/flagged.html').read_text()
    assert 'F17' in flagged and 'F18' in flagged
    assert 'Conditional illustration only' in (root / 'hub/executive-summary.html').read_text()
    print('PASS: follow-up summary reproducibility, conditional arithmetic and disclosure regressions')


if __name__ == '__main__':
    check(Path(__file__).resolve().parent.parent)
