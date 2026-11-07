# RentincreaseSF5 — SF Rent Increase Compliance & Analysis

Research, verification, and planning for lawful rent increases on **two rent-controlled units** in
San Francisco (Outer Sunset, ZIP 94122), building c. 1940 (owner-stated), under the San Francisco Rent
Ordinance, California state law, and federal law.

**Live site (GitHub Pages):** https://kanlerxz87-cyber.github.io/RentincreaseSF5/

> **Not legal advice.** Prepared 2026-11-07 by agent session `6f06d5b3-rentincreasesf5`.
> Verify decisions with the [SF Rent Board](https://www.sf.gov/departments--rent-board/) (free counseling: 311) or an attorney.

## Site map

| Page | Contents |
|---|---|
| [Executive Summary](pages/executive-summary.html) | License/notice question up front, step-by-step process with official links, per-unit summary, risks |
| [Process](pages/process.html) | 8 steps: coverage → Housing Inventory → license → fee → math → timing → notice → records |
| [Rules & Caps](pages/rules.html) | Local / state / federal rules in tables; every row has a source link |
| [Units & Analysis](pages/units.html) | Anonymized unit data + exact allowable-increase math per unit |
| [Practice](pages/practice.html) | Corporate vs. individual practice, how to notify, reasonable reasons |
| [Legal Scrutiny](pages/legal-scrutiny.html) | Reviewers (Rent Board, Prop F counsel, HRC, HUD), 10-point review checklist, one-unit vs. both |
| [Flagged for Review](pages/flagged.html) | 12 unverified / owner-data / business-judgment items with sources |

## Data

- `data/findings.csv` — all 56 findings with per-row source links and verification status
- `data/units.csv` — anonymized unit/tenancy data (owner-provided)
- `data/flagged.csv` — flagged items (unverified / needs owner data / review / judgment)
- `data/analysis.md` — full per-unit calculations and assumptions
- `data/sources.md` — sources register (33 sources, access date, verification method)
- `COORDINATION.md` — shared task board for parallel sessions (protocol, claims, log)

## Privacy policy

All personal information is **anonymized** in this repository and on the site: tenant names appear only as
placeholder IDs (Tenant U1-A … U1-D, U2-A, U2-B). **Dates and dollar amounts are kept unchanged.**
The placeholder-to-identity mapping is held by the property owner only and is intentionally **not** stored
in this repository or published on the site.

## Verification policy

- Every table row carries a source link; official sources (sf.gov, leginfo.legislature.ca.gov, govinfo,
  federalregister.gov, congress.gov) are cited directly.
- Values that could not be confirmed from an official source are left blank or marked
  *unverified* / *secondary* and listed on the [Flagged for Review](pages/flagged.html) page.
  Nothing is inferred or filled in.
