# Verification record — session `arena-d4b68642`

**Date:** 2026-11-07 (UTC) · **Branch:** `arena/d4b68642-rentincreasesf5`
**Role:** final integration and independent re-verification

This session re-read the controlling official sources, re-verified the repository's data
line by line, repaired two publication defects, and consolidated four overlapping research
sets into one landing page with category subpages. No earlier session's work was deleted.

---

## 1. What was retrieved and read this session

Every source below was opened and read, not merely returned by a search. Only official
publishers are used.

| Ref | Source | Publisher |
| --- | --- | --- |
| S1 | [The Rent Board Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) | SF Rent Board |
| S2 | [Admin Code §37.15 — Reporting Obligations; Licensing](https://www.sf.gov/information--sec-3715-reporting-obligations-licensing) | SF Rent Board |
| S3 | [Admin Code §37.3 — Rent Limitations](https://www.sf.gov/information--sec-373-rent-limitations) | SF Rent Board |
| S4 | [Form 571 — Allowable Annual Increases, full history](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) | SF Rent Board |
| S5 | [Learn about rent increases in San Francisco](https://www.sf.gov/learn-about-rent-increases-san-francisco) | SF Rent Board |
| S6 | [Banked rent increases](https://www.sf.gov/information--banked-rent-increases) | SF Rent Board |
| S7 | [Rules & Regulations Part IV — §4.10 notice, §4.12 banking](https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring) | SF Rent Board |
| S8 | [Civil Code §827 — notice of rent increase](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) | California Legislature |
| S9 | [Civil Code §1947.12 — statewide rent cap](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12) | California Legislature |
| S10 | [California Tenant Protection Act (AB 1482)](https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482) | SF Rent Board |
| S11 | [Learn about San Francisco rental laws](https://www.sf.gov/learn-about-san-francisco-rental-laws) | SF Rent Board |
| S12 | [The Rent Board Fee](https://www.sf.gov/rent-board-fee) | SF Rent Board |
| S13 | [Annual rent increase for multiple years](https://www.sf.gov/information--annual-rent-increase-multiple-years) | SF Rent Board |
| S14 | [Rule 6.14 / Costa-Hawkins petitions](https://www.sf.gov/information--petition-determination-pursuant-section-614-andor-costa-hawkins) | SF Rent Board |
| S15 | [Admin Code §37.10B — Tenant Harassment](https://www.sf.gov/information/sec-3710b-tenant-harassment) | SF Rent Board |
| S16 | [Admin Code §37.10C — Algorithmic devices prohibited](https://www.sf.gov/information--sec-3710c-use-and-sale-algorithmic-devices-prohibited) | SF Rent Board |
| S17 | [Civil Code §1942.5 — retaliation](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1942.5) | California Legislature |
| S18 | [Housing discrimination (FEHA)](https://calcivilrights.ca.gov/housing/) | California Civil Rights Dept. |
| S19 | [Housing discrimination under the Fair Housing Act](https://www.hud.gov/helping-americans/fair-housing-act-overview) | U.S. HUD |
| S20 | [Report an unlawful rent increase (Form 516C)](https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history/) | SF Rent Board |
| S21 | [Form 1007 — Notice to Tenant / Right to Counsel](https://www.sf.gov/sites/default/files/2023-08/1007%20Notice%20to%20Tenant%20Req%27d%20by%2037.%209(c)-Eng-Sp-Ch-Viet-Rus-Tag[74].pdf) | SF Rent Board |

### URLs corrected during verification

- `https://www.sf.gov/tenants-right-counsel-program` → **404**. The right-to-counsel statement is
  verified from Form 1007 (S21) instead, which is the operative Rent Board document.
- Several §-pages redirect from `/information/sec-…` to `/information--sec-…`. Both resolve; the
  register uses the form that returned content.
- The HUD Fair Housing overview now redirects to `/helping-americans/fair-housing-act-overview`.
  The register uses the destination.

---

## 2. The licence question — verified verbatim

§37.15(a) reads: *"Owners of residential dwelling units subject to this Chapter 37 shall be
required to report certain information about their units to the Rent Board."* There is **no**
entity-form or portfolio-size threshold in the text.

§37.15(e) reads: *"If a landlord has substantially complied … the landlord shall receive a license
to impose rent increases … If the landlord has not substantially complied … the license … shall be
temporarily suspended … the license … shall be restored prospectively, but a tenant shall not be
obligated to pay the increased rent for months during the period of suspension."*

The Housing Inventory page states the licence is **"automatically generated"** for non-owner-occupied
units and **"does not need to be included with your rent increase notice."**

**Conclusion:** an individual owner must be licensed, but there is no application and no approval
step. Report first, then serve. Late reporting does not revive suspended months.

---

## 3. The banking conflict — resolved, and why it does not change the numbers

Earlier sessions flagged this as an unresolvable conflict and priced Unit 1 conservatively at 1.6%.
The three official statements are:

| Source | Statement |
| --- | --- |
| S6, banking page | "A skipped increase is only banked if at least **24 full months** pass without any rent increase." |
| S7, Rule 4.12(a) | "A full **12 months** must have elapsed from the date that an annual rent increase … **could have been imposed** before this banking section becomes applicable." |
| S3, §37.3(a)(2) | Accumulation permitted, subject to §37.15. No month-count condition. |

The **worked example on S5** settles the measuring point. Tenant moved in 6/1/2023; increase imposed
5/1/2026. The 1.7% available 6/1/2024 **is** banked; the 1.4% available 6/1/2025 is **not**, and is
"permanently lost due to the change in anniversary date." The clock therefore runs **12 months from
the date each increase became available**.

Because the first increase becomes available 12 months after the tenancy starts, and banks 12 months
after that, the banking page's "24 months" is measured from **tenancy start** while Rule 4.12's
"12 months" is measured from **availability**. They describe the same instant.

**This reconciliation is analysis, not a quoted rule** (published as F04). It is also unnecessary for
the decision, because both readings agree on these two units:

- **Unit 1** — tenancy began 2025-02-01. On the target effective date 2027-02-01 exactly 24 months have
  passed with no increase, and exactly 12 months since the 1.4% became available. Both tests pass.
- **Unit 2** — no increase since 2019-06-01. Every skipped year from 2020 to 2025 is far beyond both
  thresholds.

So the earlier "safe option" discount on Unit 1 was unnecessary. The 3.0% figure stands on either reading.

---

## 4. Line-by-line data verification

| Data file | Method | Result |
| --- | --- | --- |
| `data/allowable-increases.csv` | Each period normalised and compared to Form 571 | **27 matched, 0 mismatches** (20 rows predate the transcribed range) |
| `data/allowance-ledger.csv` | Each rate compared to the Form 571 period cited on the same row | **9 matched, 0 problems** |
| `data/units.json` rates | Each `pct` compared to Form 571 for its period | **8 matched, 0 problems** |
| Scenario arithmetic | Recomputed independently from the published percentages | **5 of 5 match to the cent** |
| Notice periods | Recomputed from Civil Code §827(b) thresholds | **All correct**, including the 5-day mailing addition |

Arithmetic confirmed: 3,995 × 1.6% = 63.92 · 3,995 × 3.0% = 119.85 · 3,150 × 1.6% = 50.40 ·
3,150 × 13.1% = 412.65 · 3,150 × 10% = 315.00. No result is rounded up.

Unit 2's banked subtotal was re-derived year by year: 1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 = **11.5%**,
plus the 1.6% annual in effect = **13.1%**. The 1.6% that became available 6/1/2026 is **not yet banked**
at a February 2027 effective date; it is the current annual increase, not a banked one. Earlier sets
described the same 13.1% as "seven skipped years," which reaches the right total by the wrong route.

---

## 5. Defects found and repaired

| # | Defect | Impact | Repair |
| --- | --- | --- | --- |
| 1 | `tools/pages_1.py` emitted `CURRENT_PERIOD`, `A_DOLLAR`, `A_BASE`, `B_DOLLAR`, `B_BASE` verbatim into the **published landing page** | Visitors saw raw template tokens instead of the period and dollar figures | Added the missing substitution step; verified the tokens no longer appear in any generated HTML |
| 2 | `COORDINATION.md` carried unresolved `=======` and `>>>>>>> origin/main` markers at lines 175 and 201 | The shared task board was internally corrupted | Markers replaced with an explanatory comment. The enclosed block was confirmed to duplicate an earlier section and was **preserved verbatim**, not deleted |

Both are now guarded by `tools/release_gate.py`, so neither can recur silently.

---

## 6. Release gate

`python3 tools/release_gate.py` — **PASS**

```
pages                          14
data rows                      296
links                          740
files scanned for markers      81
mirror pairs                   15
scenarios recomputed           5
register findings              62
```

Checks enforced: one `<h1>` / `lang` / main landmark per page · internal links and stylesheets resolve ·
external links https and on the official allowlist · **every table data row carries an official source
link** · no supplied initials, street address or tracker · no unsubstituted template token · no merge
conflict marker · root/`site/` mirror parity · HTML tag balance · rate table matches Form 571 ·
arithmetic recomputes and is never rounded up · unverified rows are actually blank.

The template-token check was tightened during development: a naive `}}` substring test flagged
legitimate JavaScript closing braces. It now matches mustache/Jinja placeholders only, and scans prose
with inline script excluded. The check was made more precise, not removed.

Other checks still passing: `scripts/check.py`, `scripts/independent_audit.py`, `tools/check_links.py`,
`tools/build_site.py` (0 broken links, 0 unsourced rows). CI additionally asserts that a fresh
`python scripts/build.py` produces **zero** uncommitted drift.

---

## 7. Privacy

No tenant name, initial or street address is published anywhere. Occupants are described by role only
("three original occupants; one original occupant remains, one later co-tenant added"). Dates and dollar
amounts are preserved exactly as supplied, and are labelled **owner-supplied** because they cannot be
confirmed from an official source. The gate scans every published page for the six supplied initial
pairs on every build.

One privacy consequence worth flagging to the owner: the Housing Inventory submission is **public**
(S1). Owner business contact details, occupancy dates and base rent in $250 increments become
searchable. That is a requirement of the licence, not an optional disclosure.

---

## 8. Limits of this verification

- No lease, rent ledger, parcel record, portal account or attorney opinion was available. Nothing here
  certifies that a specific increase on a specific unit is lawful.
- External links are checked for publisher and shape at build time, not for perpetual availability.
- The 3/1/2027–2/29/2028 allowance is not published and is left blank.
- No official ZIP-94122 market rent was confirmed; none is estimated. For a rent-controlled unit the
  lawful increase does not depend on market rent.
- Reported 2026 proposals to cap banked increases at 10% a year could not be confirmed on an official
  legislative status page. No value is asserted (F09).

---

# Re-verification record — session `arena/bcfbbb8d` — 2026-11-08

A fresh, independent read of every controlling source behind the consolidated set. Nothing was taken
from an earlier session's summary: each point below was retrieved again on 2026-11-08, quoted, and
compared with the value the site publishes. The full point-by-point table is generated by
`tools/build_hub.py` into [`AUDIT-2026-11-08-bcfbbb8d.md`](AUDIT-2026-11-08-bcfbbb8d.md) and rendered at
`hub/audit.html`, so the record and the page cannot drift apart.

## Sources retrieved and read in this pass

| Ref | Source | Publisher |
| --- | --- | --- |
| S1 | [The Rent Board Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) | SF Rent Board |
| S2 | [Admin Code §37.15 — Reporting Obligations; Licensing](https://www.sf.gov/information--sec-3715-reporting-obligations-licensing) | SF Rent Board |
| S3 | [Admin Code §37.3 — Rent Limitations](https://www.sf.gov/information--sec-373-rent-limitations) | SF Rent Board |
| S4 | [Form 571 — Allowable Annual Increases](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) | SF Rent Board |
| S5 | [Learn about rent increases in San Francisco](https://www.sf.gov/learn-about-rent-increases-san-francisco) | SF Rent Board |
| S6 | [Banked rent increases](https://www.sf.gov/information--banked-rent-increases) | SF Rent Board |
| S7 | [Rules Part IV — §4.10 notice, §4.12 banking](https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring) | SF Rent Board |
| S8 | [Civil Code §827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) | California Legislature |
| S9 | [Civil Code §1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12) | California Legislature |
| S10 | [AB 1482 guidance, 8.8% for SF](https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482) | SF Rent Board |
| S11 | [Learn about San Francisco rental laws](https://www.sf.gov/learn-about-san-francisco-rental-laws) | SF Rent Board |
| S12 | [The Rent Board Fee](https://www.sf.gov/rent-board-fee) | SF Rent Board |
| S13 | [Annual rent increase for multiple years](https://www.sf.gov/information--annual-rent-increase-multiple-years) | SF Rent Board |
| S14 | [§6.14 / Costa-Hawkins petitions](https://www.sf.gov/information--petition-determination-pursuant-section-614-andor-costa-hawkins) | SF Rent Board |
| S15 | [Admin Code §37.10B — Tenant Harassment](https://www.sf.gov/information--sec-3710b-tenant-harassment) | SF Rent Board |
| S16 | [Admin Code §37.10C — Algorithmic devices](https://www.sf.gov/information--sec-3710c-use-and-sale-algorithmic-devices-prohibited) | SF Rent Board |
| S18 | [Housing discrimination (FEHA)](https://calcivilrights.ca.gov/housing/) | California Civil Rights Dept. |
| S20 | [Report an unlawful rent increase (Form 516C)](https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history) | SF Rent Board |
| S21 | [Form 1007 — Tenant Right to Counsel](https://www.sf.gov/sites/default/files/2023-08/1007%20Notice%20to%20Tenant%20Req%27d%20by%2037.%209(c)-Eng-Sp-Ch-Viet-Rus-Tag[74].pdf) | SF Rent Board |
| S22 | [Failure to Repair and Maintain Petitions (Form 516B)](https://www.sf.gov/information--failure-repair-and-maintain-petitions) | SF Rent Board |
| S23 | [Rules Part X — §10.11 repair deferral](https://www.sf.gov/reports/august-2024/rent-board-rules-and-regulations-part-x-tenant-petition-arbitration) | SF Rent Board |

## What was confirmed, in the words that decide it

- **Individual owners are included.** §37.15(a): *"Owners of residential dwelling units subject to this
  Chapter 37 shall be required to report certain information about their units to the Rent Board."* No
  entity or portfolio threshold appears anywhere in the section.
- **No application exists.** Housing Inventory page: *"once you have reported into the Housing Inventory,
  a rent increase license will be automatically generated for non-owner occupied units."*
- **The licence must exist on the effective date.** Same page: *"your rent increase notice will not be
  enforceable without having a rent increase license on the effective date of the notice."*
- **Suspension is not retroactive.** §37.15(e): *"a tenant shall not be obligated to pay the increased
  rent for months during the period of suspension."*
- **No petition for an annual increase.** Form 571: *"may increase the tenant's base rent once every 12
  months … without filing a petition at the Rent Board."*
- **Rate and period.** Form 571: *"Effective March 1, 2026 through February 28, 2027, the allowable
  annual increase amount is 1.6%."* The full 46-period table was re-read; every historical value the site
  uses matches.
- **Notice periods.** Civil Code §827(b)(2)–(3): 30 days at 10 percent or less, 90 days when *greater
  than* 10 percent, measured against the rent charged at any time in the previous 12 months and combined
  with any other increase in that window.
- **Notice content.** §37.3(b)(1) and Rule 4.10(a)(1) require the annual and banked portions to be
  identified in writing on or before the date notice is given; Rule 4.12(b) adds the dates the banked
  amount is based on.
- **Consequence of a defective notice.** Rule 4.10(b): *"shall render the entire rent increase null and
  void"*, subject to the half-of-one-percent good-faith readjustment.
- **Repair-based deferral.** Form 516B page: *"The petition must be filed no later than 60 days following
  the tenant's receipt of the rent increase notice."* Rule 10.11(a) confirms the mechanism and the refund.
- **No fee, no deadline for a tenant challenge.** Form 516C page: *"There is no charge for filing the
  petition"* and *"There is no time limit for filing a petition."*
- **AB 1482 does not apply.** Civil Code §1947.12(d)(3) exempts housing under a local ordinance that
  restricts increases below the state cap, and the Rent Board's page states: *"This does NOT apply for
  units under the rent increase limitations of the San Francisco Rent Ordinance."*
- **Arithmetic.** 3,995.00 × 3.0% = 119.85; 3,995.00 × 1.6% = 63.92; 3,150.00 × 13.1% = 412.65;
  3,150.00 × 10% = 315.00. Nothing rounded up.

## What changed as a result of this pass

1. **F04 rewritten.** The previous text said the 12-month and 24-month wording had been *reconciled* as
   two measurements of the same instant. That does not survive a close reading. The banking page says a
   skipped increase banks only after *"at least 24 full months pass without any rent increase"* — but its
   own worked example banks a 1.7% increase twelve months after it became available, and the rent-increase
   page permanently loses a 1.4% increase eleven months after it became available even though 35 months had
   passed since move-in. The time-stamped examples and Rule 4.12 are treated as controlling, and the
   conflict is published as a conflict. It still does not change either unit's figure: Unit 1 hits twelve
   months after its skipped increase and twenty-four months after the tenancy began on the same date,
   2027-02-01.
2. **F19 added.** The units page previously asserted that the 2026-04-01 occupant change *did not* create a
   new tenancy. That fact was never supplied. The page now sets out both branches and the different
   effective dates each produces.
3. **F20 added.** The complete Rules and Regulations compilation (document 625, amended 13 January 2026)
   was linked but not read end to end; Part IV and Part X were read in full text on sf.gov.
4. **Notice kit added.** The notice-content duties are split across §37.3(b), Rule 4.10(a) and Rule 4.12(b),
   which is where a compliant increase most often fails. The kit sets out the elements, a model notice, a
   pre-service checklist and the four ways a notice fails.
5. **Nine new register rows** and **two new flags** were published; the register now holds 71 findings,
   57 of them verified against an official source. Flags F17 and F18 belong to the parallel session
   `arena-75594f57`, whose follow-up audit was merged into this branch before publication. Its F17 (no
   official empirical norm for corporate practice or customary increases) and F18 (banked scenarios assume
   an unprovided rent history) are kept exactly as published, and this session's flags were numbered F19
   and F20 to avoid a collision.

## Limits of this pass

No lease, rent ledger, portal account, property record or construction record was examined. The build
year, the unit count and both base rents remain owner-supplied. External links are checked for publisher
and shape at build time, not for perpetual availability. No browser rendering test was run. Nothing here
is legal advice and no notice, petition or licence action was taken.

## Build and checks run after the changes

```
python3 scripts/build.py              # all sets rebuilt, consolidated hub last
python3 tools/release_gate.py         # PASS - 16 pages, 369 data rows, 957 links, 0 orphans, 71 findings
python3 scripts/check.py              # PASS - links, source allowlist, row sourcing, headings
python3 scripts/independent_audit.py  # PASS - 7 pages, 60 sourced rows, mirror parity, identifiers
python3 tools/check_links.py          # 342 internal / 36 external links, no problems
python3 tools/verify_site.py          # OK across the pages/ set
```
