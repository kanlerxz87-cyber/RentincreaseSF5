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

# Independent re-verification — session `arena-847d013c` — 2026-11-08

Previous sections record earlier sessions' verification. This session re-checked the merged tree
**from the official sources outward**, not from the repository's own claims. Every URL below was
retrieved and read again on 2026-11-08.

## 1. Rate table — machine comparison, not eyeballing

The 46 periods in Form 571 were transcribed by hand from the PDF read this session and compared
programmatically against `data/allowable-increases.csv`:

```
compared 46 rows, 0 mismatches, official table has 46 periods
periods in official table but missing from repo: none
BLANK (as designed): 3/1/2027 - 2/29/2028 -> unverified - not yet published
```

The 2027–28 row remains blank by design: the Board publishes it on 1 March 2027, and it is stated
as anonymous-ineligible rather than estimated. `1.6%` for 3/1/2026–2/28/2027 is confirmed three ways
(Form 571 table, the guidance page, and the Board's own news release of 14 January 2026).

## 2. Arithmetic — recomputed independently to the cent

| Scenario | Computation | Result | Site value | Match |
| --- | --- | --- | --- | --- |
| Unit 1 annual | $3,995 × 1.6% | $63.9200 | $63.92 | yes |
| Unit 1 banked + annual | $3,995 × 3.0% | $119.8500 | $119.85 | yes |
| Unit 2 annual | $3,150 × 1.6% | $50.4000 | $50.40 | yes |
| Unit 2 banked + annual | $3,150 × 13.1% | $412.6500 | $412.65 | yes |
| Unit 2 held to 10% | $3,150 × 10% | $315.0000 | $315.00 | yes |

Bank chain: 1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 = **11.5%** banked, plus 1.6% current = **13.1%**.
The 2.6% for 3/1/2019–2/29/2020 is correctly excluded: that period expired before this tenancy's
first increase became available on 1 June 2020. No value is rounded up, per Rule 4.10 and Form 571.

Notice dates: 2027-02-01 minus 30 days = **2027-01-02**; 2027-02-28 minus 90 days = **2026-11-30**.
Both match the site. The 5-day mail extension is stated separately, not folded in.

## 3. The licence question — confirmed again in the ordinance text

- §37.15(a): *"Owners of residential dwelling units subject to this Chapter 37 shall be required to
  report…"* — no entity-type, no portfolio-size threshold. An **individual owner is covered**.
- §37.15(e): the licence is granted on substantial compliance, **suspended** on non-compliance,
  restored **prospectively only**, and *"a tenant shall not be obligated to pay the increased rent
  for months during the period of suspension."*
- The Housing Inventory page: the licence is *"automatically generated"* once a unit is reported as
  non-owner-occupied, and *"does not need to be included with your rent increase notice."*
- The same page: *"your rent increase notice will not be enforceable without having a rent increase
  license on the effective date of the notice."*

So: **report first, then serve.** There is no application and no approval decision.

## 4. Notice rules — statute against rule

Civ. Code §827(b)(2)–(3) read verbatim: 30 days for 10% or less, 90 days for more than 10%, each
measured *"at any time during the 12 months before the effective date"* and combined with other
increases in that window, service personally or by mail under CCP §1013. Rule 4.10(b) read verbatim:
a non-conforming increase is **null and void in its entirety**, with only a half-of-one-percent
good-faith readjustment. Both confirmed as the site states them.

## 5. State cap — the exemption is correctly applied

Civ. Code §1947.12(d)(3) exempts *"Housing subject to rent or price control through a public entity's
valid exercise of its police power … that restricts annual increases in the rental rate to an amount
less than that provided in subdivision (a)."* These units are under the Rent Ordinance, which restricts
increases to 1.6% — far below 5% + CPI. The statewide cap therefore does **not** govern them. The
8.8% figure (5% + 3.8% CPI for 8/1/2026–7/31/2027) is correctly labelled reference-only.

## 6. New this session

Two sources were added and read in full: the Rent Board's **Tenant Financial Hardship Applications**
page (S22) and the Board's **annual-rent-increase announcement** (S23). Two register rows were added
from S22, both directly quoted:

- **R63** — hardship *deferral* is unavailable for annual and banked increases. The page lists the
  five increase types that qualify and then states that *"for all other types of rent increases or
  passthroughs, including annual and banked rent increases … financial hardship relief is not
  available."* This matters to the owner: it is one route a tenant cannot use against a lawful banked
  increase, and it is stated as a verified fact rather than assumed.
- **R64** — what a tenant must produce to challenge the calculation, drawn from the petition page.

The register now holds **64 findings: 55 verified, 5 owner-supplied or computed, 4 blank or
no-authority-found.** No previously verified row changed value.

## 7. Defects found this session

| # | Defect | Action |
| --- | --- | --- |
| 1 | `internal/notes.md` claimed GitHub Pages serves only `index.html`, `pages/` and `assets/`. The live Pages configuration serves the repository **root**, so every tracked file — including that note — is publicly readable. | Note rewritten with a correct header; disclosed publicly as **F18** on the flagged page. No personal information was in the file. |
| 2 | Flag **F09** (reported 10% cap on banked increases) was vague and cited only the banking page. | Rewritten to state precisely what was reported, labelled *secondary reporting only*, with the specific effect on Unit 2 noted. Still **not** asserted as law: no official legislative record page was retrieved. |
| 3 | The register had no row on hardship deferral, a mechanism a tenant-side review would otherwise appear to have available. | Added R63/R64 from S22. |

## 8. Privacy audit of the whole published tree

Not just HTML. All 57 published HTML files were scanned for local-reference breakage (0 broken
local refs), and the whole tracked tree plus git history was searched for the supplied tenant
initials. **No tenant name, initial, address or parcel number appears in any tracked file or in any
commit.** The only matches for a two-letter pattern were the word "IS" in ordinary prose inside a
quoted worked example. The site footer's privacy statement is accurate as published.

Note for the owner: because Pages serves the root, `internal/` is **not** private and git history is
**not** private. Do not add personal information anywhere in this repository.

## 9. What remains unverified, and why

Nothing in this list blocks publication; each is on the flagged page.

- Owner-supplied base rents, tenancy dates and the absence of prior increases (F01).
- The 1940 build year and two-unit count, and therefore coverage itself (F02).
- Whether the Housing Inventory is current and a licence is on file — checkable only in the portal (F03).
- The exact banking boundary for Unit 1: 1 February 2027 is exactly 24 months after 1 February 2025,
  so "at least 24 full months" is satisfied on that date under the ordinary reading. This is an
  arithmetic reading of the Board's own wording, so it is published as analysis (F04), not as a rule,
  and a written counsellor answer is the way to close it.
- The 2027–28 rate (F06) and any official ZIP-level market figure (F10): left blank.
- The reported banked-increase cap (F09): no official legislative record retrieved.

## 10. Gates re-run after the changes

```
python3 scripts/build.py             # 16 files + 13 dashboard files + 6 earlier pages, register 64
python3 scripts/check.py             # PASS: local links, source allowlist, every row sourced, headings
python3 scripts/independent_audit.py # PASS: 7 pages, 60 sourced rows, root/site parity, identifier exclusion
python3 tools/release_gate.py        # PASS: 14 pages, 305 rows, 770 links, 0 orphans, 0 unsourced, 0 privacy hits
```

Independent from-scratch link audit of all 57 published HTML files: **0 broken local references.**
