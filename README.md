# Rental increase SF — verified research dashboard

A public, fully source-linked GitHub Pages dashboard for an individual owner of two rent-controlled units in San Francisco's Outer Sunset (ZIP 94122, reported built 1940).

**Live site:** https://kanlerxz87-cyber.github.io/RentincreaseSF5/

## The question answered first

> "As an individual property owner, do I still need to apply for a license and inform the Rent Board before notifying tenants of a rent increase?"

**Yes — the license requirement applies to individual owners too**, but: the Rent Increase License is **automatically generated** by the annual Housing Inventory report (it is not a separate application); no petition/notice about the specific increase is required for ordinary annual or banked increases; and the license must be **current on the effective date** of the increase — not merely before the tenant is notified. A license does not prevent a tenant challenge. See the [Executive Summary](pages/executive-summary.html) and the official sources linked on every row.

## What's here

| Path | Contents |
|---|---|
| `index.html` | Clean landing page / dashboard with key figures and navigation |
| `pages/executive-summary.html` | The license answer first, step-by-step process, and every other question answered |
| `pages/rent-board-process.html` | Rent Board licensing, reporting, fee, notice, petitions |
| `pages/requirements.html` | Full requirements checklist |
| `pages/legal-framework.html` | Local / state / federal rules |
| `pages/allowable-rates.html` | Official Form 571 rate table, 1982–2027 |
| `pages/units.html` | Anonymized unit facts and computed amounts, with formulas |
| `pages/practice-and-notice.html` | Corporations vs individuals, notice, reasons, tenant-lawyer scrutiny |
| `pages/fair-housing.html` | One-unit vs both-units discrimination analysis |
| `pages/sources.html` | Official source registry (51 sources) |
| `pages/verification.html` | Line-by-line verification log |
| `pages/flagged-for-review.html` | **Flagged for Review**: irregularities, conflicts, and every blank/unverified value |
| `research/*.md` | Detailed write-ups with official links for manual review |
| `data/*.json` | Verified datasets; every row has official source IDs |
| `scripts/build_site.py` | Reproducible static-site build from the datasets |
| `scripts/verify.py` | Build/link/privacy/source verification; writes `VERIFICATION.md` |
| `COORDINATION.md` | Shared task board, claims, sources, verification and integration record |

## Method and rules

- **Official verified trusted sources only** (sf.gov, media.api.sf.gov, portal.sfrb.org, leginfo.legislature.ca.gov, hud.gov, govinfo.gov, sfplanninggis.org, GitHub's own record of this repository). Commercial guides, press reports and forums were deliberately excluded.
- **Every table row carries an official source link.** If a value could not be confirmed from an official source, its cell is **blank** and the row is marked `UNVERIFIED` and listed on Flagged for Review. No value was inferred or filled in.
- Rows are labelled `verified`, `owner-provided`, `computed` (pure arithmetic on owner-provided rents and official rates) or `analysis` (editorial synthesis). Computed figures are never presented as official determinations.
- **Conflicting official sources are not silently resolved**; both readings are published with their links and flagged.
- **Privacy (owner instruction):** personal information is internal only. All published occupant identifiers are placeholders (Occupant A–F); no real tenant identifiers are stored in this public repository. Dates and amounts are preserved exactly as supplied.

## Rebuild and verify

```sh
python3 scripts/build_site.py   # regenerate index.html + pages/*.html from data/*.json
python3 scripts/verify.py       # line-by-line checks; writes VERIFICATION.md
```

The site is plain static HTML/CSS/JS with a `.nojekyll` file — no build toolchain, no external dependencies. GitHub Pages is configured to publish `main` at `/`.

## Scope

This is research and compliance documentation, **not legal advice**. The SF Rent Board itself states its counselors cannot give legal advice. Case-specific questions (coverage, license status, the 12-month vs 24-month banking conflict, the Unit 1 occupant change, and whether to increase one or both units) should be reviewed with a Rent Board counselor and a California attorney. Free tenant and landlord resources are listed on the site.

**Current key figure:** allowable annual increase **1.6%** for 3/1/2026–2/28/2027, citywide (official [Current Rates](https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit) and [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf)).
