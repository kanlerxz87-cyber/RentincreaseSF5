# SF Rent Review — rental increase research dashboard

Privacy-conscious, official-source research about two owner-reported rental units in San Francisco's Outer Sunset (ZIP 94122). The owner reports a 1940 construction year and rent-controlled status; this repository has not authenticated either property-specific fact. Coverage must be checked against the [SF Rent Board's rental-law guidance](https://www.sf.gov/learn-about-san-francisco-rental-laws/).

**Public site:** https://kanlerxz87-cyber.github.io/RentincreaseSF5/

The current entry point is the **consolidated dashboard** at `index.html`, with category pages in `hub/` for the Rent Board process, unit calculations, allowable increases, notices, state/local/federal protections, owner practices, tenant-side review, sources, verification, and items flagged for review. Its current verification register has 62 rows.

Older research outputs remain linked from `hub/archive.html` and preserved in `pages/`, `docs/`, `dashboard/`, and the earlier root pages. They may contain superseded assumptions or older research dates. Use the consolidated hub and its **Flagged for Review** page as the current summary; archived output is for provenance, not a separate legal determination.

## The first question: Rent Board reporting and the licence

*Does an individual owner need to inform the Rent Board and apply for a licence before notifying tenants?* **The owner must report; there is no separate licence application.** Section 37.15 applies to owners of residential units without a corporation-only exception. Reporting a tenant-occupied unit in the [Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) generates the rent-increase licence automatically. The licence must be current when an increase takes effect; it is prudent to check the portal before serving, but the rule is not a Rent Board approval of the proposed notice. See [S.F. Admin. Code §37.15](https://www.sf.gov/information--sec-3715-reporting-obligations-licensing).

An ordinary annual or properly calculated banked increase does **not** require a Rent Board petition or advance approval. Certain special increase types do require a petition. See [§37.3](https://www.sf.gov/information--sec-373-rent-limitations) and the official [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf). A licence is not immunity from a tenant challenge.

## What is a normal increase?

No official source reviewed establishes a customary rent-increase amount for ZIP 94122. If a unit is confirmed covered by San Francisco rent control, the official annual allowance is **1.6% for effective dates from 2026-03-01 through 2027-02-28**; that is a legal allowance, not a market norm or confirmation that a particular unit qualifies. See [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) and [SF rental-law coverage guidance](https://www.sf.gov/learn-about-san-francisco-rental-laws/). The state AB 1482 limit is not a substitute for a stricter applicable local limit; coverage must be checked first ([SF's AB 1482 guide](https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482/)). Federal fair-housing rules address discrimination, not a standard local rent-increase percentage; subsidy status was not supplied ([HUD Fair Housing Act guidance](https://www.hud.gov/helping-americans/fair-housing-act-overview)).

There is no verified empirical source here comparing how large real-estate companies usually raise rents with how individual owners do it. The reporting/licensing rule applies to owners, not only corporations ([§37.15](https://www.sf.gov/information--sec-3715-reporting-obligations-licensing)). Keeping a dated rent ledger, checking each lawful increase, using a clear written notice, and retaining service evidence are prudent recordkeeping practices—not claims about what every company does or additional Rent Board approvals.

No equal-increase rule across these units was identified in the sources reviewed. Raising both units does not automatically prevent a discrimination or retaliation claim, and raising only one is not automatically unlawful. Any difference should follow verifiable, neutral rent-history and tenancy facts, not a tenant's protected characteristic or protected activity. See [CRD housing protections](https://calcivilrights.ca.gov/housing/), [HUD fair-housing guidance](https://www.hud.gov/helping-americans/fair-housing-act-overview), and [California Civil Code §1942.5](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1942.5). No lawyer has reviewed or cleared an increase in this project. Do not assume free eviction-defense counsel automatically includes representation for every rent-increase dispute; check the official [Rent Board contact page](https://www.sf.gov/departments--rent-board) and [Tenant Right to Counsel notice](https://www.sf.gov/sites/default/files/2023-08/1007%20Notice%20to%20Tenant%20Req%27d%20by%2037.%209(c)-Eng-Sp-Ch-Viet-Rus-Tag[74].pdf) for current scope.

## Owner-reported inputs and conditional calculations

The owner reports a Unit 1 lease start of **2025-02-01 at $3,995 per month**, then a continuing-tenancy/current-rent entry of **2026-04-01 at $3,995 per month**. Unit 2 is reported as starting **2019-06-01 at $3,150 per month**. No names, initials, or exact address are published. These are owner-supplied records, not authenticated official records. In particular, whether the 2026-04-01 entry continues the same rent-controlled tenancy, what the correct anniversary is, and whether a §6.14 notice was required remain unresolved; see the official [§6.14 / Costa-Hawkins guidance](https://www.sf.gov/information--petition-determination-pursuant-section-614-andor-costa-hawkins). No complete Unit 2 rent-increase ledger was supplied, so its banked scenarios are assumptions, not confirmed entitlements.

The figures below are arithmetic illustrations only. They assume the reported base rent is lawful, the unit is covered, the right anniversary and increase history are confirmed, and a current licence and proper notice are in place. The official rate table verifies the percentages, not the owner-provided base rents or rental history. Notice periods are linked to [California Civil Code §827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827).

| Unit / scenario | Assumed owner-reported base rent | Rate calculation | Calculated increase → new rent | Notice | Status and official sources |
| --- | --- | --- | --- | --- | --- |
| Unit 1 — annual only | $3,995.00 | 1.6% | $63.92 → $4,058.92 | 30 days | Conditional calculation; owner input unverified. [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf); [§827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) |
| Unit 1 — annual plus one banked year | $3,995.00 | 1.4% + 1.6% = 3.0% | $119.85 → $4,114.85 | 30 days | Conditional on the correct tenancy anniversary and no intervening increase; not a legal clearance. [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf); [banking guidance](https://www.sf.gov/information--banked-rent-increases); [§827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) |
| Unit 2 — annual only | $3,150.00 | 1.6% | $50.40 → $3,200.40 | 30 days | Conditional calculation; owner input unverified. [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf); [§827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) |
| Unit 2 — all assumed banked years plus annual | $3,150.00 | 11.5% + 1.6% = 13.1% | $412.65 → $3,562.65 | 90 days | Assumes no increases since 2019; that history is unverified (F18). A proposed 10% cap is not enacted as of 2026-11-10 (F09). [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf); [banking guidance](https://www.sf.gov/information--banked-rent-increases); [Rent Board notice](https://www.sf.gov/learn-about-rent-increases-san-francisco); [§827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) |
| Unit 2 — illustrative 10% choice | $3,150.00 | 10.0% (owner choice, not a general legal cap) | $315.00 → $3,465.00 | 30 days | Illustration only; no claim that 10% is required or approved. [Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf); [Rent Board notice](https://www.sf.gov/learn-about-rent-increases-san-francisco); [§827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) |

The 12-month Rule 4.12 and 24-month wording on the Rent Board's banking page are discussed on the site as an interpretation, not a property-specific ruling; see [banking guidance](https://www.sf.gov/information--banked-rent-increases), [Part IV Rules](https://www.sf.gov/reports/february-2024/rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring), and Flag F04. Unit 2's full-bank calculation assumes no intervening increases since 2019, which was not established (F18). A 2026-11-09 Rent Board notice describes proposed Board of Supervisors File No. 261020: a temporary 10% cap on combined banked and capital-improvement increases if enacted as proposed. It **has not been enacted** and may change or lapse; recheck the [official Rent Board notice](https://www.sf.gov/learn-about-rent-increases-san-francisco) before serving any banked increase (F09). No amount is cleared for service or guaranteed to pass tenant-side legal review.

## Build and validate

Requires Python 3, no packages or external assets:

```
python3 scripts/build.py             # all sets; the consolidated hub in hub/ is built LAST
python3 tools/release_gate.py        # 11 release checks; blocks a broken, unsourced or private site
python3 scripts/check.py             # local links, official-source allowlist, every data row sourced, headings
python3 scripts/independent_audit.py # root/site parity, landmarks, identifier exclusion
python3 tools/build_site.py          # link + source-coverage check for the pages/ set
python3 build.py                     # verified dashboard -> dashboard/ and site/dashboard/
python3 tools/check_links.py         # dashboard links, anchors, source tags, mirror parity, identifier exclusion
python3 -m http.server 8000 --bind 0.0.0.0   # preview from the repository root
```

Generated HTML is written to the repository root (GitHub Pages publishes `main:/`) and mirrored into `site/`.
`.nojekyll` keeps Pages from processing the files.

## Repository layout

| Path | Purpose |
| --- | --- |
| `index.html` | Consolidated landing page (generated by `tools/build_hub.py`) |
| `hub/*.html`, `hub/hub.css` | Category subpages and stylesheet for the consolidated set |
| `data/verified-register.csv` | The 62-row register exported for manual review |
| `tools/build_hub.py` | Consolidated-set generator; register is the single source of truth |
| `tools/release_gate.py` | Release gate: sourcing, privacy, links, parity, rates, arithmetic |
| `previous-dashboard.html` | The previous merged hub, preserved and linked from the archive |
| `VERIFICATION.md` | What was read, what was checked, defects found, and limits |
| `pages/*.html`, `assets/style.css`, `data/*.csv` | Deep-dive set, its stylesheet and machine-readable tables |
| `process.html`, `amounts.html`, `protections.html`, `flagged.html`, `sources.html`, `style.css` | Earlier published set (unchanged) |
| `site/` | Mirror of the published root, used by the validation scripts |
| `tools/` | Generator for the deep-dive set (`site_lib.py`, `pages_1.py`, `pages_2.py`, `build_site.py`) |
| `scripts/` | Earlier set's generator, checks and independent audit |
| `dashboard/` | Third research set (verified dashboard), generated by `build.py` from `data/*.json` |
| `data/*.json` | Machine-readable inputs for the dashboard: sources, facts, process, units, market, questions, flagged |
| `build.py`, `tools/check_links.py` | Dashboard generator and its link/integrity checker |
| `COORDINATION.md` | Shared task board, source list and reconciliation log |

## Verification rules

- Every table row links the official page its value came from (SF.gov / Rent Board, California Legislative
  Information, California Civil Rights Department, U.S. HUD).
- Values are never inferred. If an official source could not confirm a value, the cell is blank and the gap is
  listed on the *Flagged for review* page.
- Arithmetic is labelled `calculated` and shows the official percentages it derives from.
- Research date: **7 November 2026**. Statutes, rules and rates change; re-check before acting.

## Privacy

No tenant names, initials, addresses, parcel numbers or personal documents are stored in the current files
or current site. The record uses `Tenant A1`, `Tenant A2`, `Tenant B1`, `Tenant B2`, `Unit A` and `Unit B`.
Dates and dollar amounts are preserved because the arithmetic depends on them. Housing Inventory submissions are
public and made under penalty of perjury — use truthful data in the official Rent Board portal, never placeholders.
An earlier public revision exposed tenant initials in verification scripts; those literals were removed, but shared
Git history was not rewritten. See F15 on the Flagged for Review page. Do not treat current-file remediation as
historical erasure.

## Not legal advice

Research only. No licence was obtained, no inventory report filed, and no notice served or approved by this
repository. Recommendations and hypothetical arithmetic are not official determinations. The controlling text is
on the official pages linked throughout; the Rent Board counsellor line is 415-252-4600.

## Independent compilation (session arena/0502f829-rentincreasesf5)

A fourth, independently verified compilation is also published here and linked from the hub: `pages/compilation.html` (executive summary — the licence answer first), `pages/process.html` (step-by-step Rent Board process), `pages/rates.html` (Form 571 allowable-increase history), `pages/questions.html` (owner Q&A) and `pages/review.html` (flagged items). It uses its own stylesheet (`assets/rent-dashboard.css`) and links every table row directly to the official source page. Where this compilation and the deep-dive set differ, the difference is one of approach, not of law. Its open items are listed on its own flagged page.

---

## Independent second dashboard — `docs/`

A complete second research dashboard lives in **`docs/`**, built and verified by another
session and merged alongside the pages above. It is published at:

**https://kanlerxz87-cyber.github.io/RentincreaseSF5/docs/**

Its 12 pages are: executive summary, the licence question, a step-by-step checklist,
allowable-increase rates, anonymized unit ledgers, notice requirements, petitions and
passthroughs, corporate vs. individual owners, discrimination risk, the federal/state/local
law breakdown, a Flagged for Review page, and a source registry.

Build and verify it with:

```bash
python3 tools/rent_calc.py            # recompute + 21 self-tests (all pass)
python3 tools/dashboard_build.py      # regenerate docs/
python3 tools/dashboard_check_links.py
```

It reaches the same headline conclusion by an independent route: **§37.15 requires every
owner — individual or corporate — to hold a current rent-increase licence before an annual
or banked increase takes effect, and no petition is needed for the increase itself.**

Its data files live in `docs/data/` and its scripts are prefixed `dashboard_`/`rent_` to
avoid colliding with the scripts above.

### Privacy

Tenant names and initials are anonymized throughout. The identity mapping exists only in
`PRIVATE.md` and `private/identifiers.txt`, both git-ignored and never published. Note that
GitHub Pages serves this repository's **root**, so anything committed anywhere is public.
