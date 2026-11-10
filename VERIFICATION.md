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
| S8 | [Civil Code §827 — notice of rent increase](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=827&lawCode=CIV) | California Legislature |
| S9 | [Civil Code §1947.12 — statewide rent cap](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1947.12&lawCode=CIV) | California Legislature |
| S10 | [California Tenant Protection Act (AB 1482)](https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482) | SF Rent Board |
| S11 | [Learn about San Francisco rental laws](https://www.sf.gov/learn-about-san-francisco-rental-laws) | SF Rent Board |
| S12 | [The Rent Board Fee](https://www.sf.gov/rent-board-fee) | SF Rent Board |
| S13 | [Annual rent increase for multiple years](https://www.sf.gov/information--annual-rent-increase-multiple-years) | SF Rent Board |
| S14 | [Rule 6.14 / Costa-Hawkins petitions](https://www.sf.gov/information--petition-determination-pursuant-section-614-andor-costa-hawkins) | SF Rent Board |
| S15 | [Admin Code §37.10B — Tenant Harassment](https://www.sf.gov/information/sec-3710b-tenant-harassment) | SF Rent Board |
| S16 | [Admin Code §37.10C — Algorithmic devices prohibited](https://www.sf.gov/information--sec-3710c-use-and-sale-algorithmic-devices-prohibited) | SF Rent Board |
| S17 | [Civil Code §1942.5 — retaliation](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1942.5&lawCode=CIV) | California Legislature |
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

# Independent re-verification — session `arena-0691d955`

**Date:** 2026-11-08 (UTC) · **Branch:** `arena/0691d955-rentincreasesf5`
**Role:** line-by-line re-verification of the published consolidated set, defect repair, publication.

## A. Sources re-fetched and re-read in full this session

| Ref | Source | Publisher | Used to check |
| --- | --- | --- | --- |
| S1 | [The Rent Board Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) | SF Rent Board | licence is automatic on reporting; must be current on the effective date; no penalty for late filing; inventory data is public; no licence needed with the notice |
| S2 | [Admin Code §37.15](https://www.sf.gov/information/sec-3715-reporting-obligations-licensing) | SF Rent Board | "owners of residential dwelling units"; no entity/size exemption; suspension and prospective restoration in (e) |
| S3 | [Admin Code §37.3](https://www.sf.gov/information/sec-373-rent-limitations) | SF Rent Board | 60% of CPI, 7% maximum; banking in (a)(2); "landlords" not limited by entity form |
| S4 | [Form 571 allowable increases](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) | SF Rent Board | all 46 periods, row by row, including the 1992-93 caution |
| S5 | [Learn about rent increases in San Francisco](https://www.sf.gov/learn-about-rent-increases-san-francisco) | SF Rent Board | 1.6% for 3/1/2026-2/28/2027; 12-month rule; base rent only; no rounding up; 30/90 days plus 5 for mail; worked examples |
| S6 | [Banked rent increases](https://www.sf.gov/information/banked-rent-increases) | SF Rent Board | "24 full months", no cap, not compounded or prorated, notice must state the banked portion |
| S7 | [Rules Part IV (§4.10, §4.12)](https://www.sf.gov/reports/february-2024/rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring) | SF Rent Board | notice content; null-and-void rule and the 0.5% readjustment; "full 12 months must have elapsed"; §4.12(b) content and its no-void proviso |
| S8 | [Civil Code §827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=827&lawCode=CIV) | California Legislature | 30-day and 90-day notice; service personally or by mail under CCP §1013 |
| S9 | [Civil Code §1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1947.12&lawCode=CIV) | California Legislature | (d)(3) local-control exemption; (d)(6) two-unit owner-occupied exemption; 5% + CPI, 10% ceiling |
| S10 | [AB 1482 guidance](https://www.sf.gov/reports/august-2023/california-tenant-protection-act-2019-ab-1482) | SF Rent Board | 8.8% for 8/1/2026-7/31/2027; does not apply to units under the SF Ordinance |
| S11 | [Learn about San Francisco rental laws](https://www.sf.gov/learn-about-san-francisco-rental-laws/) | SF Rent Board | coverage for units built on or before 13 June 1979, excluding single-family dwellings |
| S12 | [The Rent Board Fee](https://www.sf.gov/rent-board-fee) | SF Rent Board | $59.00 per dwelling unit 2026-27; 1 March deadline; 5% monthly penalty capped at 15%; exemption deadline 14 Dec 2026; exemption does not satisfy the Inventory |
| S13 | [Annual rent increase for multiple years](https://www.sf.gov/information/annual-rent-increase-multiple-years) | SF Rent Board | percentages added, not compounded; no petition; no rounding up |
| S14 | [§6.14 / Costa-Hawkins petition](https://www.sf.gov/information/petition-determination-pursuant-section-614-andor-costa-hawkins) | SF Rent Board | 6.14 notice within a reasonable time, "generally sixty days"; co-tenants not subject to Costa-Hawkins |
| S15 | [Admin Code §37.10B](https://www.sf.gov/information/sec-3710b-tenant-harassment) | SF Rent Board | (a)(5) coercion to vacate; (a)(9) discrimination; treble or $1,000 minimum plus fees |
| S16 | [Admin Code §37.10C](https://www.sf.gov/information--sec-3710c-use-and-sale-algorithmic-devices-prohibited) | SF Rent Board | algorithmic-device prohibition; monthly and per-unit violations; private right of action |
| S17 | [Civil Code §1942.5](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1942.5&lawCode=CIV) | California Legislature | 180-day retaliation bar in (a); separate bar in (d) |
| S18 | [CRD housing discrimination](https://calcivilrights.ca.gov/housing/) | California Civil Rights Department | protected-characteristics list, matched item by item |
| S20 | [Report an unlawful rent increase (516C)](https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history) | SF Rent Board | no filing fee, no time limit, evidence asked for, hearing format |
| S21 | [Form 1007](https://www.sf.gov/sites/default/files/2023-08/1007%20Notice%20to%20Tenant%20Req%27d%20by%2037.%209(c)-Eng-Sp-Ch-Viet-Rus-Tag%5B74%5D.pdf) | SF Rent Board | Tenant Right to Counsel intake number (415) 659-9184 |

## B. Arithmetic recomputed independently

| Unit | Option | Base | Rate | Increase | New rent | Matches published |
| --- | --- | --- | --- | --- | --- | --- |
| Unit 1 | Annual only | $3,995.00 | 1.6% | $63.92 | $4,058.92 | yes |
| Unit 1 | Annual + banked 2026 | $3,995.00 | 3.0% (1.4 + 1.6) | $119.85 | $4,114.85 | yes |
| Unit 2 | Annual only | $3,150.00 | 1.6% | $50.40 | $3,200.40 | yes |
| Unit 2 | Banked + annual | $3,150.00 | 13.1% (11.5 + 1.6) | $412.65 | $3,562.65 | yes |
| Unit 2 | Capped at 10% by choice | $3,150.00 | 10.0% | $315.00 | $3,465.00 | yes |

Unit 2's 11.5% banked subtotal is the sum of the rates available on each skipped anniversary:
1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 = 11.5. Percentages added, never compounded, and no result
rounded up. Serve-by dates re-derived from the effective dates (30 or 90 days, plus 5 if mailed).

## C. Defects found and repaired

1. **F19 — rate-table years were published in the wrong century.** `_d()` in `tools/build_hub.py`
   mapped every two-digit year to 20xx, so the Form 571 rows for 1982-1999 were printed as
   2082-2099 (e.g. "2082-04-01 - 2083-02-28"). Percentages were correct; years were not. Fixed,
   the whole table re-read against Form 571 (46 rows), and the release gate now fails if any
   effective period falls outside 1982-2027.
2. Stale "today" wording removed from the serve-by note; the dates are derived from the effective
   date, not from the day the page was built.
3. Research date refreshed to 8 November 2026 on the consolidated hub only. Earlier sets keep their
   own dates, which remain true for them.

## D. Release gates re-run after the repairs

`python3 scripts/build.py` (16 files), `scripts/check.py`, `scripts/independent_audit.py`,
`tools/check_links.py`, `tools/dashboard_check_links.py`, `tools/release_gate.py` — all pass:
14 pages, 303 table data rows, 777 links, 0 orphans, 0 unsourced rows, 15 mirror pairs, 5 scenarios
recomputed, 62 register findings, 19 flagged items (F01-F19).

## E. What is still not verified

Unchanged from the earlier record: the owner-supplied base rents, tenancy dates, build year and
unit count (F01, F02); the Inventory/licence status (F03); the unpublished 2027-28 rate (F06);
no official ZIP-level market rent (F10); no federal rent ceiling found (F07); no uniform-increase
requirement found (F08); reported but unconfirmed 2026 banking-cap proposals (F09).

# Verification pass — 8 November 2026 (session `arena/aa463593`)

Independent re-check against the official pages, performed on the merged tree (my branch + PR #13).
Nothing below is taken from another session's notes: every value was re-read from the official URL.

## Sources retrieved and read this pass

| # | Official page | What was checked |
|---|---|---|
| 1 | [Learn about rent increases in San Francisco](https://www.sf.gov/learn-about-rent-increases-san-francisco) | 1.6% headline; 12-month rule; first increase at 12 months; base rent only; no rounding up; rate in effect on the *effective* date; 30/90-day notice and +5 days by mail; notice contents; roommate surcharge unlawful; all four worked examples; licence requirement and its July 2022 / March 2023 dates |
| 2 | [Form 571 — Allowable Annual Increases](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) | All 46 rate periods, 3/1/1982 → 2/28/2027, transcribed and machine-compared |
| 3 | [The Rent Board Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) | "All owners … required to report"; licence auto-generated for non-owner-occupied units; current on the effective date; no monetary penalty for late filing; licence need not be attached; inventory information is public; $250 rent increments |
| 4 | [Admin Code §37.15](https://www.sf.gov/information--sec-3715-reporting-obligations-licensing) | Full text of (a)–(e), including the prospective-only restoration in (e) |
| 5 | [Admin Code §37.3](https://www.sf.gov/information--sec-373-rent-limitations) | (a)(1) 60%-of-CPI, 7% ceiling; (a)(2) banking with **no** 24-month condition |
| 6 | [Banked rent increases](https://www.sf.gov/information--banked-rent-increases) | "24 full months"; added not compounded; no proration; no expiry; no carry-over to a new tenant |
| 7 | [Rules & Regulations Part IV](https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring) | §4.10(a) notice content, §4.10(b) null-and-void, §4.12(a) 12-month test and half-percent readjustment, §4.12(b) banked-part disclosure |
| 8 | [Annual rent increase for multiple years](https://www.sf.gov/information--annual-rent-increase-multiple-years) | No compounding; no petition; no rounding up |
| 9 | [Civ. Code §827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=827&lawCode=CIV) | (b)(1) personal delivery or CCP §1013 mail; (b)(2) 30 days ≤10%; (b)(3)(A) 90 days >10% |
| 10 | [Civ. Code §1947.12](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1947.12&lawCode=CIV) | (a) 5%+CPI / 10%; (b) new-tenancy initial rate; (d)(3) local-ordinance exemption |
| 11 | [SF AB 1482 guide](https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482) | 8.8% for 8/1/2026–7/31/2027 and that it "does NOT apply" to locally controlled units; two-unit owner-occupied exemption |
| 12 | [Civ. Code §1942.5](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1942.5&lawCode=CIV) | (a) 180 days; (d) retaliation for organising, no time limit |
| 13 | [§37.10B tenant harassment](https://www.sf.gov/information/sec-3710b-tenant-harassment) | (a)(5) coercion to vacate; (a)(9) discrimination; (c)(5) treble damages / $1,000 minimum plus fees |
| 14 | [§37.10C algorithmic devices](https://www.sf.gov/information--sec-3710c-use-and-sale-algorithmic-devices-prohibited) | Prohibition on use, per-month and per-unit violations, tenant and nonprofit private right of action |
| 15 | [§6.14 / Costa-Hawkins guidance](https://www.sf.gov/information--petition-determination-pursuant-section-614-andor-costa-hawkins) | 6.14 notice to each subsequent occupant; 60 days generally reasonable; co-tenants not subject to a Costa-Hawkins increase |
| 16 | [Report an unlawful rent increase (516C)](https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history/) | No filing charge, no time limit, Box C; hearing needs no attorney; judge confined to the served record |
| 17 | [Rent Board fee](https://www.sf.gov/rent-board-fee) | $59.00 per dwelling unit for 2026-27; due 1 March; 5% monthly late penalty capped at 15%; fee exemption ≠ inventory reporting |
| 18 | [Learn about SF rental laws](https://www.sf.gov/learn-about-san-francisco-rental-laws/) | 13 June 1979 coverage line; counsellor line and hours |
| 19 | [Form 1007](https://www.sf.gov/sites/default/files/2023-08/1007%20Notice%20to%20Tenant%20Req%27d%20by%2037.%209(c)-Eng-Sp-Ch-Viet-Rus-Tag[74].pdf) | Right-to-Counsel intake (415) 659-9184; counsellor hours 9–12 and 1–4 |
| 20 | [CRD housing discrimination](https://calcivilrights.ca.gov/housing/) | California protected characteristics, including source of income, primary language, immigration status |

## Machine checks run this pass

| Check | Result |
|---|---|
| Form 571 rate table vs `data/allowable-increases.csv` (47 rows) | **0 mismatches** |
| Form 571 vs `docs/data/allowable_increases.json` (45 periods) | **0 mismatches**; the 1992 split period is correctly shown as one row with both rates |
| Form 571 vs `data/allowance-ledger.csv` (9 rows) | **0 mismatches** |
| Independent recomputation of every published dollar figure | all match to the cent, none rounded up |
| Serve-by dates (30/90-day, +5 by mail) | recomputed for 2027-02-01 and 2027-02-28: 2027-01-02, 2026-12-28, 2026-11-30, 2026-11-25, 2027-01-29 — all match |
| Banked ledger for Unit 2 (2020→2025 available, 2026 annual) | 1.8+0.7+2.3+3.6+1.7+1.4 = 11.5% banked, +1.6% = 13.1% — matches |
| Supplied initials across all 167 tracked files | **0 matches** |
| Supplied initials across all 53 commits of history | 4 files in earlier commits — **flagged, not rewritten** (F15) |
| Merge-conflict markers in published files | 0 |
| Unsubstituted template tokens | 0 |
| Every generator + checker | all pass (see below) |
| `python3 scripts/build.py` twice | no uncommitted drift — reproducible |

## Defects found and fixed this pass

1. **`internal/notes.md` stated it was not published.** It is: Pages serves `main:/`, and the file
   returns 200 at the live URL. Corrected, with the exposure explained (F20).
2. **The site's verification stamp said 7 November** while the governing pages had been re-read on
   8 November. Changed to "sources rechecked 8 Nov 2026", and `TODAY` moved to 2026-11-08 so the
   serve-by arithmetic and the "computed from" caption are consistent.
3. **Two sources cited in prose but absent from the register** (the multiple-year guidance page and
   the Rent Ordinance index) were added as S22 and S23.

## Queried, not adopted (published as F19–F20)

- The multiple-year guidance example's 8.2% total appears to use the 2018-19 rate for a September
  2019 anniversary. No figure on this site depends on it; every rate comes from Form 571.
- "Licence current on the effective date" is the documented rule; "obtain it before service" is
  prudent practice, not a quoted requirement.
- The publication surface is the whole repository root, not just the HTML pages.

## Limits of this pass

Every figure was checked against the official page it cites, and every rate against Form 571. What
could **not** be checked, and is left blank or flagged: whether either unit is actually in the
Housing Inventory, the lawful base rent and complete rent history (owner-supplied only), the 1940
construction date, whether a §6.14 notice was served on the later occupant, the 3/1/2027 rate, and
any ZIP-level market rent. No notice, filing or lawyer review was performed, and no amount here is
certified to pass a tenant-side challenge. Research, not legal advice.

## A candidate flag was withdrawn after re-derivation

An earlier draft of this pass added a flag suggesting the multiple-year guidance example
("tenants from 2016, increase on 1 September 2020, total 8.2% = 2.2 + 1.6 + 2.6 + 1.8") used a
mis-indexed year. Re-derived against Form 571 anniversary by anniversary: 1 Sep 2017 → 2.2%,
1 Sep 2018 → 1.6%, 1 Sep 2019 → 2.6%, 1 Sep 2020 → 1.8%. **The example is correct**, so the flag was
wrong and has been removed before publication. It is recorded here rather than quietly dropped.

# Re-verification — session `arena/d448f2f5`

**Date:** 2026-11-10 (UTC) · **Branch:** `arena/d448f2f5-rentincreasesf5`
**Role:** live-site and official-source re-verification; F09 update; publication.

## A. Sources re-fetched and re-read this session

| Ref | Source | Publisher | What was confirmed |
| --- | --- | --- | --- |
| S1 | [The Rent Board Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) | SF Rent Board | All owners must report; licence auto-generated for tenant-occupied units; must be current on effective date; free; March 1 deadline; submissions public under penalty of perjury |
| S5 | [Learn about rent increases in San Francisco](https://www.sf.gov/learn-about-rent-increases-san-francisco) | SF Rent Board | 1.6% for 2026-03-01–2027-02-28; 12-month interval; banking; 30/90-day notice + 5 days if mailed; **new notice posted 2026-11-09 re File No. 261020 (proposed 10% cap, not enacted)** |
| — | [Live site landing page](https://kanlerxz87-cyber.github.io/RentincreaseSF5/) | GitHub Pages | Licence-first answer, 1.6% tile, five computed scenarios, category nav all present and matching the generators |

The Legistar detail page for File No. 261020 (status: Pending Committee Action; introduced 2026-09-15) was read for corroboration only. It is not linked from the site because the release gate's official-publisher allowlist covers sf.gov, leginfo, CRD and HUD only; the site cites the SF Rent Board notice (S5), which contains the same facts.

## B. F09 update (the only content change this session)

F09 previously read "No official legislative status page was confirmed in this session." The 2026-11-09 Rent Board notice now confirms the proposal on an official page. F09 now states the proposal, its proposed applicability date (banked increases noticed on/after 2026-09-15), and that it has not been enacted and is subject to change. No new figure is asserted; the Unit 2 full-bank option (13.1%) is flagged as affected if enacted as proposed. The executive summary (hub + `EXECUTIVE-SUMMARY.md`) carries the same caveat. Site stamp updated to "sources rechecked 10 Nov 2026".

## C. Verification performed

- Full pipeline `python3 scripts/build.py`: exit 0, no drift on second run.
- `scripts/check.py`, `scripts/independent_audit.py`, `tools/check_links.py`, `tools/release_gate.py`, `tools/followup_audit.py`: all PASS.
- Arithmetic recomputed independently (Decimal, round-down): $63.92 / $4,058.92; $119.85 / $4,114.85; $50.40 / $3,200.40; $412.65 / $3,562.65; $315.00 / $3,465.00; Unit 2 banked sum 13.1%. All match to the cent, none rounded up.
- Privacy: no tenant name, initial, address or parcel in the diff; placeholders only. Dates and amounts preserved as owner-supplied and labelled unverified.

## D. Limits (unchanged)

No lease, ledger, portal account or attorney opinion was available. Nothing here certifies that a specific increase is lawful. The 2027–2028 rate remains unpublished and blank. The proposal in F09 may change or lapse; recheck before serving.
