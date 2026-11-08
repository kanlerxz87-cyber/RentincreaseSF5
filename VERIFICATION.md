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

# Re-verification record — session `arena-fcb4d524` (2026-11-08)

Independent re-read of every controlling source on the consolidated hub, with the register and the
published pages checked line by line. One substantive error was found and corrected; nothing was
published that asserts a value no official page states.

## 1. Sources re-read in full this session

| Ref | Source | Publisher | What it was checked against |
| --- | --- | --- | --- |
| S1 | [The Rent Board Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) | SF Rent Board | R01–R10: automatic licence, public submission, no late fee, licence not attached to notice |
| S2 | [Admin Code §37.15](https://www.sf.gov/information--sec-3715-reporting-obligations-licensing) | SF Rent Board | R01–R06: no entity-type or size threshold; suspension is prospective only |
| S3 | [Admin Code §37.3](https://www.sf.gov/information--sec-373-rent-limitations) | SF Rent Board | R11, R16, R17, R24: 60% of CPI, 7% ceiling, banking, no petition |
| S4 | [Form 571 rate table](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) | SF Rent Board | All seven rates used in the scenarios: 1.8, 0.7, 2.3, 3.6, 1.7, 1.4, 1.6 |
| S5 | [Learn about rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco) | SF Rent Board | 1.6% period; 30/90-day notice; 5-day mailing addition; the four worked examples |
| S6 | [Banked rent increases](https://www.sf.gov/information--banked-rent-increases) | SF Rent Board | The 24-month sentence, the "added not compounded" rule, the worked example used in §2 below |
| S7 | [Rules & Regulations Part IV](https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring) | SF Rent Board | §4.10(a)–(b) notice and nullity; §4.12(a) 12-month test; §4.12(b) banked-portion disclosure |
| S8 | [Civil Code §827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) | California Legislature | 827(b)(1)(A)–(B) service; 827(b)(2)–(3) 30/90-day thresholds, 12-month look-back |
| S9 | [Civil Code §1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12) | California Legislature | §1947.12(d)(3) local-ordinance exemption |
| S10 | [AB 1482 guidance](https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482) | SF Rent Board | 8.8% state figure for 2026-08-01 to 2027-07-31; does not apply to units under the SF ordinance |
| S11 | [Learn about San Francisco rental laws](https://www.sf.gov/learn-about-san-francisco-rental-laws) | SF Rent Board | 14 June 1979 coverage line; counsellor 415-252-4600; hours 9–12 and 1–4 weekdays |
| S12 | [The Rent Board Fee](https://www.sf.gov/rent-board-fee) | SF Rent Board | $59.00 per dwelling unit for 2026-2027; 5% monthly penalty capped at 15% |
| S14 | [Rule 6.14 / Costa-Hawkins petition page](https://www.sf.gov/information--petition-determination-pursuant-section-614-andor-costa-hawkins) | SF Rent Board | "generally, sixty days is considered reasonable"; co-tenants not subject to a Costa-Hawkins increase |
| S15 | [Admin Code §37.10B](https://www.sf.gov/information/sec-3710b-tenant-harassment) | SF Rent Board | (a)(5) rent increase to influence a tenant to vacate; (a)(9) discrimination; treble or $1,000 damages |
| S16 | [Admin Code §37.10C](https://www.sf.gov/information--sec-3710c-use-and-sale-algorithmic-devices-prohibited) | SF Rent Board | Algorithmic-device prohibition; private right of action for tenants and tenant nonprofits |
| S20 | [Report an unlawful rent increase](https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history/) | SF Rent Board | Form 516C box C; no fee; no time limit; hearing format |
| S21 | [Form 1007](https://www.sf.gov/sites/default/files/2023-08/1007%20Notice%20to%20Tenant%20Req%27d%20by%2037.%209(c)-Eng-Sp-Ch-Viet-Rus-Tag%5B74%5D.pdf) | SF Rent Board | Tenant Right to Counsel intake: Eviction Defense Collaborative, (415) 659-9184 |
| — | [Civil Code §1942.5](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1942.5) | California Legislature | 180-day retaliation window; §1942.5(d) retaliation for organising, no time limit |
| — | [CRD housing discrimination](https://calcivilrights.ca.gov/housing/) | California Civil Rights Dept. | Protected-characteristics list compared with R48 |

Every quoted value in the register reproduced. No value was changed on re-reading; the correction
below is to the *reasoning* attached to one value, not to a rate, date or amount.

## 2. The error that was corrected

The previous version of this repository (and of the live site) stated that the 24-month wording and the
12-month Rule reconcile, because "the first increase becomes available 12 months after the tenancy
starts; it banks 12 months after that = 24 months after tenancy start". That reasoning is not supported
by the Board's published examples, and the claim that "both readings produce the same result for both
units" is therefore unsafe. The examples are decisive:

| Example (official) | Increase available | Increase imposed | Gap | Outcome published |
| --- | --- | --- | --- | --- |
| "Banked rent increases" worked example (S6) | 2024-08-01 (1.7%) | 2025-08-01 | 12 months | **Banked** |
| "Learn about rent increases", first banked year (S5) | 2024-06-01 (1.7%) | 2026-05-01 | 23 months | **Banked** |
| "Learn about rent increases", second banked year (S5) | 2025-06-01 (1.4%) | 2026-05-01 | 11 months | **Not banked; permanently lost** |

A 24-month requirement excludes the 12-month and 23-month rows, which the Board publishes as banked.
The 12-month test explains all three rows. The correct statement is therefore: **Rule 4.12's 12-month
test is the test demonstrated by the Board's own examples, and the 24-month sentence on the banking
page is an unresolved inconsistency.** It is published as F04.

Effect on the two units:

| Unit | Rule 4.12 (applied) | If the 24-month sentence were applied to each increase |
| --- | --- | --- |
| Unit 1 | 1.4% banked + 1.6% annual = **3.0%**, $119.85 | 1.6% only = **$63.92** |
| Unit 2 | 11.5% banked + 1.6% annual = **13.1%**, $412.65 | 1.4% excluded = 11.7%, **$368.55** |

Arithmetic rechecked: 3,995 × 3.0% = 119.85 · 3,995 × 1.6% = 63.92 · 3,150 × 13.1% = 412.65 ·
3,150 × 11.7% = 368.55. None rounded up.

## 3. Checks run

`python3 scripts/build.py`, `scripts/check.py`, `scripts/independent_audit.py`, `tools/check_links.py`,
`tools/build_site.py`, `build.py`, `tools/dashboard_check_links.py` and `tools/release_gate.py` all
pass on the merged tree. The gate reports 14 pages, 299 source-bearing data rows, 763 links, 0 orphans,
0 unsourced rows, 0 privacy hits, 15 identical mirror pairs and 62 register findings.

## 4. New flag

**F17 — what happened in Unit 1 on 2026-04-01.** The owner's wording supports two readings: a
continuing tenancy with an added co-tenant (anniversary stays 1 February, no rent reset), or a new
tenancy if every original occupant vacated (anniversary 1 April; no increase before 1 April 2027). The
site prices only the first reading and now flags the second. The lease and rent ledger settle it.

## 5. Limits

Unchanged from the previous record: no lease, rent ledger, parcel record, portal record or attorney
opinion was available, so nothing here certifies that a particular increase on a particular unit is
lawful. External links are validated for publisher and shape, not for perpetual availability.

## 6. Addendum — remaining sources re-read (2026-11-08)

| Source | What it confirmed |
| --- | --- |
| [Annual rent increase for multiple years](https://www.sf.gov/information--annual-rent-increase-multiple-years) | Increases are added, not compounded; no petition is required; no rounding up; at least 30 days' notice, 35 if mailed; base rent only. Supports R11, R30 and R37. |
| [HUD — Fair Housing Act overview](https://www.hud.gov/helping-americans/fair-housing-act-overview) | Federal protected classes: race, colour, national origin, religion, sex, familial status, disability. No federal rent ceiling is stated. Supports R46 and R47. |
| [Landlord Petitions and Passthroughs](https://www.sf.gov/landlord-petitions-and-passthroughs) | Six increase types require a petition **before** the notice; an annual or banked increase is not one of them. Added as **S22** and cited on R11 and on the process page. |

## 7. Additions to the published hub

- A "Your questions, answered" table on the landing page: the owner's seven questions, each with a
  short answer, the page that develops it, and the official source for the row.
- Source **S22** added to the source register and cited where the petition rule is stated.
- Footer verification date moved to 8 November 2026 for the consolidated set.
