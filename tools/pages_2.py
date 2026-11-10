"""Pages: allowed increases, local/state/federal law, notices, owner playbook,
tenant-lawyer stress test, source register, flagged for review.

Citation convention: write [[S1]] inside any HTML string; resolve() converts it to a link.
"""

from site_lib import badge, page_head, tbl, legend, layout, resolve, SOURCES

ALLOWANCES = [
    ("3/1/2026 &ndash; 2/28/2027", "1.6"),
    ("3/1/2025 &ndash; 2/28/2026", "1.4"),
    ("3/1/2024 &ndash; 2/28/2025", "1.7"),
    ("3/1/2023 &ndash; 2/29/2024", "3.6"),
    ("3/1/2022 &ndash; 2/28/2023", "2.3"),
    ("3/1/2021 &ndash; 2/28/2022", "0.7"),
    ("3/1/2020 &ndash; 2/28/2021", "1.8"),
    ("3/1/2019 &ndash; 2/29/2020", "2.6"),
    ("3/1/2018 &ndash; 2/28/2019", "1.6"),
    ("3/1/2017 &ndash; 2/28/2018", "2.2"),
    ("3/1/2016 &ndash; 2/28/2017", "1.6"),
    ("3/1/2015 &ndash; 2/29/2016", "1.9"),
    ("3/1/2014 &ndash; 2/28/2015", "1.0"),
    ("3/1/2013 &ndash; 2/28/2014", "1.9"),
    ("3/1/2012 &ndash; 2/28/2013", "1.9"),
    ("3/1/2011 &ndash; 2/29/2012", "0.5"),
    ("3/1/2010 &ndash; 2/28/2011", "0.1"),
    ("3/1/2009 &ndash; 2/28/2010", "2.2"),
    ("3/1/2008 &ndash; 2/28/2009", "2.0"),
    ("3/1/2007 &ndash; 2/29/2008", "1.5"),
    ("3/1/2006 &ndash; 2/28/2007", "1.7"),
    ("3/1/2005 &ndash; 2/28/2006", "1.2"),
    ("3/1/2004 &ndash; 2/28/2005", "0.6"),
    ("3/1/2003 &ndash; 2/29/2004", "0.8"),
    ("3/1/2002 &ndash; 2/28/2003", "2.7"),
    ("3/1/2001 &ndash; 2/28/2002", "2.8"),
    ("3/1/2000 &ndash; 2/28/2001", "2.9"),
    ("3/1/1999 &ndash; 2/29/2000", "1.7"),
    ("3/1/1998 &ndash; 2/28/1999", "2.2"),
    ("3/1/1997 &ndash; 2/28/1998", "1.8"),
    ("3/1/1996 &ndash; 2/28/1997", "1.0"),
    ("3/1/1995 &ndash; 2/29/1996", "1.1"),
    ("3/1/1994 &ndash; 2/28/1995", "1.3"),
    ("3/1/1993 &ndash; 2/28/1994", "1.9"),
    ("12/8/1992 &ndash; 2/28/1993", "1.6"),
    ("3/1/1992 &ndash; 12/7/1992", "4.0"),
    ("3/1/1991 &ndash; 2/29/1992", "4.0"),
    ("3/1/1990 &ndash; 2/28/1991", "4.0"),
    ("3/1/1989 &ndash; 2/28/1990", "4.0"),
    ("3/1/1988 &ndash; 2/28/1989", "4.0"),
    ("3/1/1987 &ndash; 2/29/1988", "4.0"),
    ("3/1/1986 &ndash; 2/28/1987", "4.0"),
    ("3/1/1985 &ndash; 2/28/1986", "4.0"),
    ("3/1/1984 &ndash; 2/28/1985", "4.0"),
    ("3/1/1983 &ndash; 2/29/1984", "7.0"),
    ("4/1/1982 &ndash; 2/28/1983", "7.0"),
]


# ---------------------------------------------------------------------------
def allowed_increases():
    b = page_head(
        "Allowable annual increases",
        "The complete official table, matching the Rent Board's own rate sheet, plus how the annual figure is "
        "set and how it interacts with banked years.",
        crumb="Dashboard / Allowed increases")

    b += """
<section class="panel">
  <h2>How the annual figure is set</h2>
  <p>Each 1 March the Rent Board publishes the increase in the CPI for the preceding 12 months. A landlord who has
  reported the unit to the Rent Board &ldquo;shall have a licence to impose annually a rent increase which does
  not exceed a tenant's base rent by more than 60% of said published increase&rdquo;, and in no event more than
  <strong>7%</strong> [[S5]]. The current allowance is <strong>1.6%</strong> for 1 March 2026 to 28 February 2027
  [[S1]] [[S2]].</p>
  <p>Three mechanical rules matter as much as the percentage: an increase may be given only once in any 12 months
  [[S1]]; it is calculated on the base rent and cannot be rounded up [[S1]]; and skipped years are added, not
  compounded, and cannot be rounded up [[S9]].</p>
</section>

<section class="panel">
  <h2>The table</h2>
  <p class="small">Every row is from the Rent Board's rate sheet [[S2]]. The 1992 rows carry the Board's own
  caution that only one of the two may be imposed for that period, depending on the tenant's anniversary date.</p>
"""

    rows = [[period, rate + "%", "[[S2]]"] for period, rate in ALLOWANCES]
    rows.append(["<strong>3/1/2027 &ndash; 2/29/2028</strong>", "&mdash;", badge("unverified") + " not yet published"])
    b += tbl("Official allowable annual rent increases, 4/1/1982 to 2/28/2027",
             [("Effective period", False), ("Amount of increase", True), ("Source", False)], rows)
    b += """
  <p class="small">The next period is deliberately blank: the Rent Board had not published a 3/1/2027 rate as at
  7 November 2026. It is listed rather than guessed so that any later notice can be re-checked against it.</p>
</section>

<section class="panel">
  <h2>Banking, in one paragraph</h2>
  <p>A landlord who refrains from imposing an annual increase, or any part of it, may accumulate the amount and
  impose it on or after a later anniversary date; banked amounts are given only at the time of an annual increase,
  only once every 12 months, are not compounded and are not rounded up, and a full 12 months must have elapsed from
  the date the increase could first have been imposed [[S9]] [[S10]]. Banking has been permitted only for increases
  available on or after 1 April 1982, there is no cap on the total banked amount under the current rules, banked
  amounts do not carry over to a new tenant, and a new owner inherits the bank [[S11]].</p>
  <div class="callout"><strong>Two official pages disagree about the waiting period.</strong> The Rent Board's
  &ldquo;Banked rent increases&rdquo; page says a skipped increase is banked only if &ldquo;at least 24 full months
  pass without any rent increase&rdquo; [[S11]], while Rule 4.12 and the &ldquo;Learn about rent increases&rdquo;
  page both say a full <strong>12</strong> months must elapse [[S9]] [[S1]]. We did not choose between them. The
  conservative assumption &mdash; 24 months &mdash; is the one flagged on
  <a href="units.html">Units &amp; numbers</a>, and the discrepancy is item F1 on
  <a href="flagged.html">Flagged for review</a>.</div>
</section>
"""
    return layout("Allowed increases", resolve(b), active="pages/allowed-increases.html", rel="../")


# ---------------------------------------------------------------------------
def laws():
    b = page_head(
        "Local, state and federal rules",
        "Which cap actually governs, why the statewide cap does not apply here, and what federal law does "
        "&mdash; and does not &mdash; say about rent increases.",
        crumb="Dashboard / Local / State / Federal")

    b += """
<section class="panel">
  <h2>In one line</h2>
  <div class="answer"><p><strong>These units are governed by the San Francisco Rent Ordinance alone.</strong> The
  statewide cap (AB 1482) expressly does not apply to housing already limited by a local ordinance below the state
  figure [[S14]] [[S15]], and there is no federal rent cap at all. Federal law enters through fair housing, which
  is about <em>why</em> an increase is imposed, not <em>how much</em> it is [[S25]] [[S26]].</p></div>
"""

    b += tbl(
        "Which rule caps the rent, and at what",
        [("Layer", False), ("Rule", False), ("Cap that applies to Units A and B", False), ("Applies here?", False), ("Source", False)],
        [
            ["San Francisco", "Rent Ordinance Ch. 37 annual allowance", "1.6% (3/1/2026&ndash;2/28/2027) once every 12 months, plus banked years", "<strong>Yes &mdash; governs</strong>", "[[S5]] [[S1]]"],
            ["San Francisco", "Banked allowances", "Added, not compounded; no current cap on the total", "Yes", "[[S9]] [[S11]]"],
            ["San Francisco", "Above-allowance petition route", "Only by Rent Board petition (six types)", "Available, not automatic", "[[S5]] [[S19]]"],
            ["San Francisco", "Housing Inventory licence", "Increase unenforceable without a current licence", "Yes", "[[S4]] [[S3]]"],
            ["California", "Costa-Hawkins (Civ. Code 1954.50 et seq.)", "Sets the initial rate for a vacant unit; exempts single-family homes and condos, not two-unit buildings", "Yes &mdash; confirms coverage", "[[S17]] [[S13]]"],
            ["California", "AB 1482 / Civ. Code 1947.12", "5% + CPI or 10% (8.8% locally for 8/1/2026&ndash;7/31/2027)", "<strong>No &mdash; displaced by the local ordinance</strong>", "[[S15]] [[S14]]"],
            ["California", "Civ. Code 827", "30/90-day notice mechanics for a change in terms", "Yes &mdash; notice mechanics", "[[S16]]"],
            ["Federal", "Rent stabilisation statute", "None exists", "No", badge("none")],
            ["Federal / state", "Fair Housing Act and FEHA", "Prohibits discrimination on protected characteristics, including through rent terms", "Yes &mdash; a conduct rule", "[[S25]] [[S26]]"],
        ])
    b += """
</section>

<section class="panel">
  <h2>Local detail that actually bites</h2>
"""

    b += tbl(
        None,
        [("Provision", False), ("What it requires or forbids", False), ("Source", False)],
        [
            ["&sect;37.3(a)(1)", "Annual increase = 60% of the CPI increase, never more than 7%; available only to an owner who has reported the unit.", "[[S5]]"],
            ["&sect;37.3(a)(2)", "Banking of unused annual increases, subject to &sect;37.15.", "[[S5]]"],
            ["&sect;37.3(a)(8)", "Any increase above the allowance requires an arbitration petition.", "[[S5]]"],
            ["&sect;37.3(a)(11)", "No increase merely because an additional occupant moved in, even if the lease allows it.", "[[S5]]"],
            ["&sect;37.3(b)(1)&ndash;(4)", "Notice must break out the annual/banked portion, certified capital or O&amp;M costs, utility passthroughs and RAP amortisation.", "[[S5]]"],
            ["&sect;37.3(b)(5)", "A non-conforming increase is <strong>null and void</strong>.", "[[S5]]"],
            ["&sect;37.3(f)", "After an owner no-fault notice (for example &sect;37.9(a)(8), (9), (10), (11), (14) or (17)), the initial rent for the next tenancy is limited for five years.", "[[S18]] [[S5]]"],
            ["&sect;37.10B(a)(5)", "Influencing a tenant to vacate by fraud, intimidation or coercion is harassment; a rent increase used that way is evidence of bad faith.", "[[S21]]"],
            ["&sect;37.10B(a)(9)", "Violating anti-discrimination law is harassment under the ordinance.", "[[S21]]"],
            ["&sect;37.10C", "Landlords may not use revenue-management software that sets or recommends rents from non-public competitor data.", "[[S22]]"],
            ["&sect;37.15(e)", "The licence issues on substantial compliance with inventory reporting and is suspended during non-compliance.", "[[S4]]"],
            ["Chapter 37A", "Annual Rent Board fee of $59.00 per dwelling unit for 2026-27, due 1 March.", "[[S7]] [[S8]]"],
        ])
    b += """
</section>

<section class="panel">
  <h2>State detail</h2>
  <p><strong>AB 1482</strong> limits increases to 5% + CPI or 10%, whichever is lower, and to no more than two
  increments in 12 months [[S15]]. For San Francisco the Rent Board publishes 8.8% for 1 August 2026 to 31 July
  2027 &mdash; and states on the same page that it does <strong>not</strong> apply to units under the Rent
  Ordinance increase limits [[S14]]. The statutory basis is &sect;1947.12(d)(3), which excludes housing subject to
  a local ordinance restricting annual increases below the state figure [[S15]]. At 1.6% these units are below
  8.8%, so the local cap controls.</p>
  <p><strong>AB 1482 also contains a detail worth knowing:</strong> the exemption for single-family homes and
  condominiums is unavailable to an owner that is a real estate investment trust, a corporation, or an LLC with a
  corporate member [[S15]] [[S14]]. It is irrelevant to a two-unit building, but it explains why corporate
  ownership is not a privileged position in California rent law.</p>
  <p><strong>Costa-Hawkins</strong> lets an owner set the initial rate for a vacant unit [[S17]], which is why a new
  tenancy can begin at a market rent; the Rent Board says the same in plain terms [[S1]] [[S24]]. It is also why a
  two-unit building stays covered: only units alienable separately from the title to another dwelling &mdash;
  single-family homes and condominiums &mdash; fall outside local rent limits, and a house with an in-law unit
  counts as two units [[S13]].</p>
  <p><strong>Notice mechanics.</strong> 30 days for an increase of 10% or less, 90 days for more than 10%, either
  in itself or combined with other increases in the preceding 12 months; personal delivery, or mail under Code of
  Civil Procedure &sect;1013 [[S16]]. The Rent Board restates this and adds five days where the notice is mailed
  [[S1]].</p>
</section>

<section class="panel">
  <h2>Federal detail</h2>
  <p>There is no federal statute capping residential rent. The federal role is fair housing enforcement:
  discrimination in the terms and conditions of a rental &mdash; which includes how rent is set &mdash; can be
  challenged through HUD's Fair Housing and Equal Opportunity office [[S26]] and, at state level, through the
  California Civil Rights Department under FEHA [[S25]]. FEHA's protected list includes race, colour, ancestry,
  national origin, citizenship, immigration status, primary language, religion, disability, sex, gender, sexual
  orientation, gender identity, marital status, familial status, source of income (including a Section 8 voucher),
  military status and age [[S25]]. Retaliation for asserting rights is separately prohibited [[S25]].</p>
  <div class="callout">A HUD Fair Market Rent benchmark for a two-bedroom unit in this area would be useful
  context, but no official FY2026/27 figure could be confirmed this session: the HUD summary page rendered without
  values, and secondary sources disagree ($2,850 / $3,174 / $3,604 / $3,697). It is therefore left blank and logged
  as F5 rather than estimated.</div>
</section>
"""
    return layout("Local / State / Federal", resolve(b), active="pages/laws.html", rel="../")


# ---------------------------------------------------------------------------
def notices():
    b = page_head(
        "Notices",
        "The notice is where most increases fail. What it must contain, how far ahead it must be served, and "
        "the defects that void it.",
        crumb="Dashboard / Notices")

    b += """
<section class="panel">
  <h2>Requirements</h2>
"""

    b += tbl(
        None,
        [("Requirement", False), ("Rule", False), ("Source", False)],
        [
            ["Lead time &mdash; 10% or less", "At least 30 days before the effective date (35 if mailed).", "[[S16]] [[S1]]"],
            ["Lead time &mdash; more than 10%", "At least 90 days before the effective date (95 if mailed). Applies to a single increase or to the total of increases in the preceding 12 months.", "[[S16]] [[S1]]"],
            ["Delivery", "Personal delivery to the tenant, or mail under Code of Civil Procedure &sect;1013.", "[[S16]]"],
            ["Dollar amount", "State the dollar amount of the increase.", "[[S1]]"],
            ["Percentage", "State the percentage, using the rate in effect on the <em>effective date</em>, not the service date.", "[[S1]]"],
            ["Effective date", "State the date the increase takes effect.", "[[S1]]"],
            ["Composition &mdash; annual vs banked", "Say which portion is the annual increase and which is banked, and identify the years the banked amount comes from.", "[[S5]] [[S9]] [[S11]]"],
            ["Composition &mdash; other components", "Identify any certified capital improvement, O&amp;M, utility, water-bond or RAP component separately.", "[[S5]]"],
            ["Licence", "The rent increase licence must be current on the effective date; it does not need to be attached to the notice.", "[[S3]] [[S4]]"],
            ["Timing", "No increase within 12 months of the last one; a late increase resets the anniversary date.", "[[S1]]"],
        ])
    b += """
</section>

<section class="panel">
  <h2>The eight defects that void an increase</h2>
"""

    b += tbl(
        "Each of these is a reason a tenant petition succeeds",
        [("Defect", False), ("Why it fails", False), ("Source", False)],
        [
            ["Percentage above the allowance without a petition", "Null and void &mdash; the Rules void the <em>entire</em> increase, not only the excess; only a certified petition authorises more.", "[[S5]] [[S19]] [[S9]]"],
            ["No licence on the effective date", "The increase is unenforceable; the tenant is not obligated to pay during a suspension.", "[[S4]] [[S3]]"],
            ["Rounding up", "The increase is calculated on base rent and may not be rounded up; banked amounts may not be rounded up either.", "[[S1]] [[S9]]"],
            ["Compounding banked years", "Banked percentages are added, not compounded.", "[[S9]] [[S11]]"],
            ["Wrong rate period", "Using the rate in effect when the notice was written instead of when it takes effect.", "[[S1]]"],
            ["Short notice", "Fewer than 30 or 90 days, or no five-day mailing allowance.", "[[S16]] [[S1]]"],
            ["Missing annual/banked breakdown", "Rule 4.10 requires the disclosure; a conforming amount may still be corrected by a judge, but the defect is the first thing a petition tests.", "[[S9]]"],
            ["Second increase inside 12 months", "Only one increase every 12 months per tenancy.", "[[S1]]"],
        ])
    b += """
  <p class="small">The ordinance's own words are blunt: &ldquo;Any rent increase which does not conform with the
  provisions of this section shall be null and void&rdquo; [[S5]], and Rule 4.10(b) says a non-conforming increase
  &ldquo;shall render the entire rent increase null and void&rdquo; [[S9]]. The Rules then carve out a narrow
  good-faith adjustment: where an increase given in a good-faith effort to comply with the ordinance and rules
  does not exceed the limitations by more than one-half of one percent of the prior base rent, an Administrative
  Law Judge readjusts the base rent to the proper percentage instead of voiding it; Rule 4.12 contains a parallel
  provision for banked amounts [[S9]]. That is a drafting-error margin, not a safe harbour &mdash; do not plan
  around it.</p>
</section>

<section class="panel">
  <h2>Notice-preparation checklist</h2>
  <p class="small">A checklist, not a legal template. Have counsel review the final wording, and read it back to
  the Rent Board counsellor before service.</p>
  <ol>
    <li>Unit and tenant names exactly as they appear on the lease (placeholders in this record).</li>
    <li>Current base rent and the new base rent, in dollars.</li>
    <li>The dollar increase and the percentage, to one decimal place.</li>
    <li>The composition &mdash; for example &ldquo;1.4% banked (available 1 February 2026) + 1.6% annual = 3.0%&rdquo;
    for Unit A, or &ldquo;11.5% banked (2020&ndash;2025) + 1.6% annual = 13.1%&rdquo; for Unit B.</li>
    <li>The effective date, chosen so the lead time is at least 30 or 90 days, plus five if mailed.</li>
    <li>The date of the last increase, or the tenancy start date if there has been none.</li>
    <li>A statement that the increase is calculated under the Rent Ordinance's annual allowance and banked
    allowances, with the yearly percentages itemised.</li>
    <li>A dated internal record that the Housing Inventory report is filed and the rent increase licence is live.</li>
    <li>Proof of service: method, date and recipient.</li>
    <li>A copy filed with the rent ledger, and the new figure reported in the next March 1 Housing Inventory update.</li>
  </ol>
</section>

<section class="panel">
  <h2>Worked example of the composition sentence</h2>
  <div class="answer"><p><strong>Unit B, effective 1 June 2027:</strong> &ldquo;Your monthly rent will increase by
  $412.65, from $3,150.00 to $3,562.65 (13.1%). This increase is composed of banked annual allowances of 11.5%
  (1.8% available 1 June 2020; 0.7% 2021; 2.3% 2022; 3.6% 2023; 1.7% 2024; 1.4% 2025) and the annual allowance of
  1.6% in effect on 1 June 2027. Banked allowances are added and not compounded.&rdquo;</p></div>
  <p class="small">Every element of that sentence answers a specific requirement: dollar amount, percentage,
  effective date, annual versus banked split, and the years in the bank [[S1]] [[S5]] [[S9]] [[S11]]. Leave a blank
  for the 2027-28 annual rate if the notice is finalised after the Rent Board publishes it.</p>
</section>
"""
    return layout("Notices", resolve(b), active="pages/notices.html", rel="../")


# ---------------------------------------------------------------------------
def owner_practices():
    b = page_head(
        "Owner playbook",
        "How institutions and individual owners handle increases, whether to raise one unit or both, what counts "
        "as a lawful reason, and the policy that makes the answer defensible.",
        crumb="Dashboard / Owner playbook")

    b += """
<section class="panel">
  <h2>&ldquo;How do big real estate corporations handle increases?&rdquo;</h2>
  <p>The honest answer is that <strong>they are subject to exactly the same cap, and the differences are
  procedural rather than legal.</strong> Nothing in the Rent Ordinance scales the allowance to the size of the
  owner, and nothing exempts an individual owner from the reporting duties. What differs is administration &mdash;
  and in one respect the law treats corporate owners <em>worse</em>.</p>
"""

    b += tbl(
        "Corporate owner vs individual owner, item by item",
        [("Item", False), ("Corporate owner", False), ("Individual owner (these units)", False), ("Source", False)],
        [
            ["Annual allowance", "1.6%, once every 12 months", "1.6%, once every 12 months", "[[S5]] [[S1]]"],
            ["Banked allowances", "Same rules, added not compounded", "Same rules", "[[S9]]"],
            ["Housing Inventory report and licence", "Required", "Required &mdash; no natural-person exception", "[[S4]] [[S3]]"],
            ["Rent Board fee", "$59 per unit", "$59 per unit", "[[S7]]"],
            ["Revenue-management software", "Prohibited if it uses non-public competitor data", "Prohibited on the same terms", "[[S22]]"],
            ["AB 1482 single-family/condo exemption", "Unavailable to a REIT, a corporation or an LLC with a corporate member", "Available in principle, and irrelevant here: a two-unit building is covered either way", "[[S15]] [[S14]]"],
            ["Designated habitability contact", "Must be reported to the Rent Board", "May be the owner, and must be reported", "[[S4]]"],
            ["Practitioner norm: review rents annually on each anniversary date with a documented notice and rent ledger", "Reported industry practice", "Reported industry practice", badge("unverified") + " no official source states a required practice"],
        ])
    b += """
  <p class="small">The last row describes behaviour, not law: it is included because the question was asked, and it
  is deliberately not presented as a requirement. Every enforceable row points at the ordinance.</p>
  <div class="callout ok"><strong>Practical takeaway:</strong> borrow the institutional <em>process</em> &mdash; an
  annual review on each anniversary date, a notice built from the checklist, a rent ledger and a dated licence
  record &mdash; while using the latitude an individual owner has: the law does not require you to take the maximum,
  and a documented decision not to take it is itself evidence of reasonableness.</div>
</section>

<section class="panel">
  <h2>&ldquo;Should I raise one unit or both?&rdquo;</h2>
  <p><strong>The law does not require equal treatment, and the arithmetic will never produce it.</strong> Each
  tenancy has its own anniversary date, base rent and bank, so the maximum lawful increase differs by construction:
  3.0% for Unit A and 13.1% for Unit B. Chapter 37 and the Rules were reviewed for a same-increase-across-units
  requirement and none was found; that absence is recorded as a finding, not as permission to be arbitrary.</p>
"""

    b += tbl(
        "The discrimination question, separated from the arithmetic question",
        [("Question", False), ("Answer", False), ("Source", False)],
        [
            ["Does the Rent Ordinance require the same percentage for every unit?", "No provision found in Chapter 37 or the Rules.", badge("none") + " [[S18]] [[S5]]"],
            ["Can a rent increase itself be unlawful discrimination?", "Yes, if it is imposed because of a protected characteristic, or if the terms differ on that basis.", "[[S25]] [[S26]]"],
            ["Does a difference in percentage prove discrimination?", "No. Different base rents, tenancy lengths and banks produce lawful differences in percentage. What matters is the reason and the pattern.", "[[S25]]"],
            ["Is the ordinance's harassment section relevant?", "Yes: a rent increase used to influence a tenant to vacate, or one that violates anti-discrimination law, is harassment under &sect;37.10B.", "[[S21]]"],
            ["What makes the pattern defensible?", "One written method applied to both units, documented reasons tied to the tenancy, and no correlation between the size of the increase and any protected characteristic.", "[[S25]] [[S21]]"],
        ])
    b += """
  <div class="callout"><strong>Recommendation.</strong> Raise both units, using the same documented method &mdash;
  but expect the percentages to diverge, because the ledgers diverge, and say so in each notice. Raising only one
  unit is lawful where the reason is objective and documented, for example that the other tenancy's anniversary
  date has not arrived; but with two units under one roof a selective increase invites the question, and Unit B's
  13.1% is already the largest single fact in this file. The cleanest sequence is Unit A's 3.0% on 2027-02-01, then
  Unit B's 13.1% on its own anniversary, each with its own notice and ledger. Whether to run both in the same cycle
  is a decision for the owner with counsel; the legal record supports either, provided the method is uniform and
  documented.</div>
</section>

<section class="panel">
  <h2>&ldquo;What are reasonable reasons for an increase?&rdquo;</h2>
"""

    b += tbl(
        "Reasons that are lawful, reasons that need a petition, reasons that are not lawful",
        [("Reason given to the tenant", False), ("Status", False), ("What it requires", False), ("Source", False)],
        [
            ["The annual allowance set by the Rent Board", "Lawful &mdash; the normal case", "A compliant notice and a current licence", "[[S5]] [[S2]]"],
            ["Banked allowances from years not increased", "Lawful", "Correct arithmetic and the annual/banked breakdown with years", "[[S9]] [[S11]]"],
            ["Capital improvements to the building", "Lawful only via petition", "Rent Board petition and certification filed before notice", "[[S19]] [[S5]]"],
            ["Increased operating and maintenance costs", "Lawful only via petition", "Rent Board petition for a certified amount", "[[S19]]"],
            ["Rents for comparable units", "Lawful only via petition", "Rent Board petition", "[[S19]]"],
            ["Adding an occupant or roommate", "Not lawful", "No increase is permitted, even if the lease says otherwise", "[[S5]]"],
            ["&ldquo;Market rate&rdquo; while the tenancy continues", "Not lawful", "The allowance is the ceiling; market rate is available only at a new tenancy", "[[S1]] [[S17]]"],
            ["A general inflation or insurance-cost figure above the allowance", "Not lawful without a petition", "Null and void &mdash; the Rules void the entire increase, not only the excess", "[[S5]] [[S9]]"],
            ["To encourage a tenant to leave", "Unlawful", "Harassment under &sect;37.10B(a)(5)", "[[S21]]"],
        ])
    b += """
  <p class="small">Note what is <em>not</em> on the list: there is no requirement to justify an annual-allowance
  increase at all, and no requirement to disclose a business reason to the tenant. The disclosure duty concerns the
  <em>composition</em> of the number, not the motive [[S5]] [[S9]].</p>
</section>

<section class="panel">
  <h2>A one-page rent-increase policy you can point to</h2>
  <ol>
    <li><strong>Scope.</strong> Applies to every residential tenancy in the building, without exception.</li>
    <li><strong>Timing.</strong> Reviewed once a year on each tenancy's anniversary date; never more than once in
    12 months [[S1]].</li>
    <li><strong>Amount.</strong> The published annual allowance plus any properly banked allowance; never above the
    allowance without a Rent Board petition [[S5]].</li>
    <li><strong>Calculation.</strong> Percentages added, not compounded, not rounded up; the arithmetic is attached
    to the notice [[S9]].</li>
    <li><strong>Licence gate.</strong> No notice is served unless the Housing Inventory report is filed and the
    licence is current [[S3]] [[S4]].</li>
    <li><strong>Notice.</strong> 30 or 90 days (plus five if mailed), with the dollar amount, percentage, effective
    date and annual/banked composition [[S16]] [[S5]].</li>
    <li><strong>Records.</strong> Notice, proof of service, rent ledger, licence record and calculation sheet kept
    for the life of the tenancy [[S20]].</li>
    <li><strong>Fairness.</strong> No increase is timed to a repair request, a complaint, a protected-characteristic
    event, or anything that resembles pressure to vacate [[S21]] [[S25]].</li>
    <li><strong>Review.</strong> Any deviation is approved in writing before service, with the reason recorded.</li>
  </ol>
</section>
"""
    return layout("Owner playbook", resolve(b), active="pages/owner-practices.html", rel="../")


# ---------------------------------------------------------------------------
def tenant_review():
    b = page_head(
        "Would this pass a tenant-side review?",
        "A tenant can petition at any time, for free, with no deadline. These are the fifteen questions that "
        "review will actually ask, and the document that answers each one.",
        crumb="Dashboard / Tenant-lawyer test")

    b += """
<section class="panel">
  <h2>How the review works</h2>
  <p>A tenant files the Tenant Petition and Form C, checks box C for an unlawful rent increase, pays nothing, and
  there is no time limit [[S20]]. A completed petition is served on the owner and usually heard within a few months
  by a Rent Board Administrative Law Judge; the decision can be appealed to the Rent Board Commission [[S20]]
  [[S18]]. The frame is not &ldquo;was this a nice thing to do&rdquo; but &ldquo;does the arithmetic and the
  paperwork conform to the ordinance&rdquo; &mdash; and a non-conforming increase is void [[S5]].</p>
  <p>Tenants in San Francisco also have access to free legal help: the Rent Board's own termination notice tells
  tenants they are eligible for the Tenant Right to Counsel Program through the Eviction Defense Collaborative
  [[S27]]. Assume the file will be read by someone who does this every week.</p>
</section>

<section class="panel">
  <h2>The fifteen questions</h2>
"""

    b += tbl(
        None,
        [("#", False), ("What the reviewer asks", False), ("Unit A", False), ("Unit B", False), ("Source", False)],
        [
            ["1", "Is the unit rent-controlled at all?", "Yes &mdash; 1940, two units", "Yes", "[[S12]] [[S13]]"],
            ["2", "Did the owner report into the Housing Inventory?", "Must be confirmed in the portal", "Must be confirmed", "[[S3]] [[S4]]"],
            ["3", "Was the licence live on the effective date?", "Must be confirmed", "Must be confirmed", "[[S4]]"],
            ["4", "Is the base rent documented?", "Yes, $3,995.00 from 2025-02-01 &mdash; but the reset itself is in question", "Yes, $3,150.00 from 2019-06-01", "[[S6]] [[S1]]"],
            ["5", "Is the anniversary date right?", "1 February", "1 June", "[[S1]]"],
            ["6", "Is it more than 12 months since the last increase?", "Yes &mdash; none ever imposed", "Yes &mdash; none since 2019", "[[S1]]"],
            ["7", "Is the percentage within the published table?", "1.4% + 1.6% = 3.0%", "Seven years = 13.1%", "[[S2]]"],
            ["8", "Is the arithmetic added, not compounded, and not rounded up?", "Yes", "Yes", "[[S9]] [[S1]]"],
            ["9", "Was each banked year actually available?", "2025-26 only", "2020-21 through 2026-27", "[[S2]]"],
            ["10", "Does the notice state the dollar amount, percentage and effective date?", "Required", "Required", "[[S1]]"],
            ["11", "Does it separate the annual and banked portions, with years?", "Required &mdash; 1.4% of 3.0%", "Required &mdash; 11.5% of 13.1%", "[[S5]] [[S9]] [[S11]]"],
            ["12", "Was the lead time correct (30 or 90 days, plus five if mailed)?", "30 days", "90 days", "[[S16]] [[S1]]"],
            ["13", "Is the increase timed or sized in a way that looks like pressure to vacate?", "No indication", "13.1% is large: document the reason and the policy", "[[S21]]"],
            ["14", "Is the same method applied to every tenancy?", "Yes, if the written policy exists", "Yes, same policy", "[[S25]]"],
            ["15", "Is there any correlation with a protected characteristic?", "None identified", "None identified", "[[S25]] [[S26]]"],
        ])
    b += """
  <p class="small">Answers 2, 3 and 4 are the three that cannot be closed from public sources: they depend on the
  portal record and on the owner's own file.</p>
</section>

<section class="panel">
  <h2>Where the file is strongest and weakest</h2>
  <div class="grid">
    <div class="callout ok"><strong>Strongest: Unit B's arithmetic.</strong> Seven years of published percentages,
    added, on a base rent that has not moved since 2019. That is the textbook banked increase, and every element is
    checkable against the Rent Board's own table.</div>
    <div class="callout"><strong>Weakest: Unit B's size.</strong> 13.1% in one notice will be petitioned even when
    it is correct, and it is the target of the pending 10% cap. The defence is documentation, not persuasion.</div>
    <div class="callout bad"><strong>Weakest: Unit A's base rent.</strong> A base rent set at a new tenancy is
    assumed lawful, but if the prior vacancy followed an owner notice the ordinance limits the new initial rent for
    five years [[S5]], and if Tenant A2 was never served a &sect;6.14 notice the reset may not be available at all
    [[S24]]. Both are open items (F3 and F4).</div>
  </div>
</section>

<section class="panel">
  <h2>What to hold in the file, per unit</h2>
  <ul>
    <li>The lease showing the start date and the initial rent.</li>
    <li>Every rent increase notice ever served, with proof of service.</li>
    <li>A year-by-year calculation sheet naming the official percentage for each year [[S2]].</li>
    <li>The Housing Inventory submission confirmation and the licence status, dated [[S3]].</li>
    <li>Proof the Rent Board fee was paid, or the exemption [[S7]].</li>
    <li>Any &sect;6.14 notice served on a subsequent occupant, with the date [[S24]].</li>
    <li>The written rent-increase policy and the record that it was applied to both units [[S25]].</li>
  </ul>
</section>
"""
    return layout("Tenant-lawyer test", resolve(b), active="pages/tenant-review.html", rel="../")


# ---------------------------------------------------------------------------
def sources():
    b = page_head(
        "Source register",
        "Every source used on this site, what it was used for, and whether it was opened and read in this "
        "session.",
        crumb="Dashboard / Sources")
    b += """
<section class="panel">
  <h2>How verification was done</h2>
  <p>Each source below was fetched and read in full during the session on 7 November 2026, and each table row
  elsewhere on the site links to the specific page its value came from. Nothing was taken from a secondary summary
  without a matching official page. Where an official page could not be read, the value is blank and the gap is
  listed on <a href="flagged.html">Flagged for review</a>.</p>
"""
    b += legend()
    b += """
</section>

<section class="panel">
  <h2>The register</h2>
"""
    rows = [["<strong>%s</strong>" % sid,
             '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, title),
             pub, used, badge("verified")]
            for sid, title, pub, url, used, status in SOURCES]
    b += tbl("Sources, what each was used for, and verification status",
             [("ID", False), ("Source", False), ("Publisher", False), ("Used for", False), ("Status", False)],
             rows)
    b += """
  <p class="small">Publisher note: the Rent Board publishes its copies of the ordinance and rules &ldquo;for
  administrative and public convenience only&rdquo;; the official publisher of San Francisco's Administrative Code
  is American Legal Publishing, linked from the Rent Board's ordinance page [[S18]]. For a court filing, cite the
  official code publication.</p>
</section>

<section class="panel">
  <h2>Sources deliberately not used</h2>
  <ul>
    <li><strong>Secondary blogs, law-firm marketing pages and property-management guides</strong> that appeared in
    search results. Several gave contradictory banked-increase rules, and two stated a different 2026 allowance
    (1.7%). None is relied on here.</li>
    <li><strong>The HUD FMR summary page</strong> &mdash; reachable, but the FY2026 table rendered without values,
    so no figure is reported.</li>
    <li><strong>Legistar</strong> &mdash; the pending File 261020 file was opened later: its official status is
    <em>Pending Committee Action</em>, and it is reported that way here rather than summarised from press
    coverage.</li>
  </ul>
</section>
"""
    return layout("Sources", resolve(b), active="pages/sources.html", rel="../")


# ---------------------------------------------------------------------------
FLAS_DIRECT = [
    ("F1", "Two official Rent Board pages give different banking waiting periods",
     "The &ldquo;Banked rent increases&rdquo; page says a skipped increase is banked only if &ldquo;at least 24 "
     "full months pass without any rent increase&rdquo; [[S11]]; Rule 4.12 and the &ldquo;Learn about rent "
     "increases&rdquo; page say a full 12 months must elapse [[S9]] [[S1]].",
     "Unit A's 2026-02-01 allowance and any future skipped year.",
     "Ask the Rent Board counsellor which is current, and whether the 1/13/26 rule amendments changed Rule 4.12. Until then, treat the earlier year as at risk if the anniversary date is moved.",
     "conflict", ["S11", "S9", "S1", "S10"]),
    ("F2", "File 261020 (10% cap on banked and capital-improvement increases) &mdash; pending, not enacted",
     "Board of Supervisors File 261020, introduced 15 September 2026, would cap banked plus capital-improvement "
     "increases at 10% per year for three years. The official Legistar status page reads Pending Committee Action. "
     "The Rent Board posted an official notice about it on 9 November 2026.",
     "Directly changes Unit B's 13.1% to 10% this cycle if enacted as described.",
     "Check the Board of Supervisors legislative record and the Rent Board's news page before drafting any Unit B notice; if enacted, recompute and carry the balance forward.",
     "pending", ["S18", "S28"]),
    ("F3", "Unit A base rent of $3,995.00 set on 2025-02-01 &mdash; lawfulness unverified",
     "A new-tenancy initial rent may be set without limit for an empty unit [[S1]], but the ordinance withdraws that "
     "for five years where the prior tenancy ended by an owner notice under Civil Code &sect;1946.1 or a &sect;827 "
     "change of terms [[S5]]. How the prior tenancy ended was not supplied.",
     "If the reset was unavailable, every figure computed from $3,995.00 is wrong.",
     "Obtain the document that ended the prior tenancy (notice, surrender, buyout or vacate letter) and the prior rent history; if it was an owner no-fault notice, recompute from the prior lawful rent.",
     "unverified", ["S1", "S5", "S17"]),
    ("F4", "Tenant A2 is a continuing occupant, not an original lessee",
     "Whether a Rules &amp; Regs &sect;6.14 notice or a Costa-Hawkins reset was ever served on Tenant A2 is unknown. "
     "That determines whether a new tenancy was created for rent purposes when the last original occupant left "
     "[[S24]].",
     "Changes both the base rent and the anniversary date for Unit A.",
     "Search the file for a &sect;6.14 notice. If none was served within a reasonable time of learning of the occupancy, obtain advice before treating the base rent as settled.",
     "unverified", ["S24", "S17", "S5"]),
    ("F5", "HUD Fair Market Rent for this ZIP area &mdash; no official value confirmed",
     "The FY2026/27 HUD FMR summary page rendered without values and the API requires a token. Secondary sites give "
     "$2,850, $3,174, $3,604 and $3,697 for a two-bedroom unit.",
     "Market context only; it does not change the lawful maximum.",
     "Look the figure up directly on huduser.gov, or treat market comparison as out of scope. The value is intentionally blank on this site.",
     "unverified", ["S26"]),
    ("F6", "Rent Board fee payment is not tied to increase validity in Chapter 37",
     "&sect;37.15(e) ties the licence to Housing Inventory reporting [[S4]]. No provision was found in Chapter 37 "
     "making an increase void for non-payment of the Chapter 37A fee, although the fee is mandatory and penalties "
     "accrue [[S8]].",
     "Procedural and tenant-relations risk, not an identified legal bar.",
     "Pay the fee by 1 March and keep the receipt. Recorded as an absence-of-authority finding rather than assumed to be a requirement.",
     "none", ["S4", "S7", "S8"]),
    ("F8", "Unit A: the 2026-04-01 entry is an assumption, not a fact",
     "The owner's record shows a lease start of 2025-02-01 at $3,995.00, then a &ldquo;continuing tenancy&rdquo; "
     "dated 2026-04-01 at the same rent for two occupants, one of whom was an original lessee. This site reads that "
     "as a partial change of occupants within one continuing tenancy, because a new tenancy for rent purposes "
     "requires the <em>last</em> original occupant to vacate or cease permanently residing in the unit [[S24]] "
     "[[S5]].",
     "If it was in fact a wholly new lease with no original occupant remaining, Unit A's anniversary date is 1 April, not 1 February, and the available allowance and effective date change.",
     "Confirm from the signed documents whether Tenant A1 has been in continuous occupancy since 2025-02-01 and whether a new lease was signed in April 2026. If a new tenancy began, recompute: the first increase would be available 2027-04-01.",
     "unverified", ["S24", "S5", "S1"]),
    ("F7", "No provision requires the same increase across units",
     "Chapter 37 and the Rules were reviewed for an equal-treatment requirement across tenancies [[S18]] [[S5]]. None "
     "was found. Discrimination law operates on reason and effect, not on identical percentages [[S25]].",
     "Bears on the one-unit-or-both decision.",
     "Adopt the written policy on the Owner playbook page and apply it uniformly; have counsel review the decision if only one unit is increased.",
     "none", ["S18", "S5", "S25"]),
]

FLAGS = FLAS_DIRECT  # name used by build_site.py


def flagged():
    b = page_head(
        "Flagged for review",
        "Eight items where the record is incomplete or two official sources disagree. Nothing here blocks "
        "publication; all of it needs a human decision or a phone call.",
        crumb="Dashboard / Flagged for review")

    b += """
<section class="panel">
  <h2>Summary</h2>
  <div class="grid">
    <div class="tile"><div class="k">Conflicting official sources</div><div class="v">1</div><div class="n">F1 &mdash; banking waiting period</div></div>
    <div class="tile"><div class="k">Pending legislation</div><div class="v">1</div><div class="n">F2 &mdash; File 261020, 10% cap</div></div>
    <div class="tile"><div class="k">Unverified facts</div><div class="v">3</div><div class="n">F3, F4, F5</div></div>
    <div class="tile"><div class="k">Absence-of-authority findings</div><div class="v">2</div><div class="n">F6, F7</div></div>
    <div class="tile"><div class="k">Documented assumption</div><div class="v">1</div><div class="n">F8 &mdash; Unit A anniversary date</div></div>
  </div>
</section>
"""

    for fid, title, detail, impact, action, kind, srcs in sorted(FLAS_DIRECT, key=lambda f: f[0]):
        b += "<section class=\"panel\">\n<h2>%s &nbsp;%s</h2>\n" % (fid, badge(kind))
        b += "<p><strong>%s</strong></p>\n<p>%s</p>\n" % (title, detail)
        b += "<p class=\"small\"><strong>What it affects:</strong> %s</p>\n" % impact
        b += "<p class=\"small\"><strong>Recommended action:</strong> %s</p>\n" % action
        b += "<p class=\"small\"><strong>Sources:</strong> %s</p>\n</section>\n" % " ".join("[[%s]]" % s for s in srcs)

    b += """
<section class="panel">
  <h2>Values left blank on purpose</h2>
  <ul>
    <li>Allowable annual increase for 3/1/2027&ndash;2/29/2028 &mdash; not yet published by the Rent Board. <span class="badge bad">unverified</span></li>
    <li>HUD Fair Market Rent, two-bedroom, this area, FY2026/27 &mdash; could not be confirmed. <span class="badge bad">unverified</span></li>
    <li>Outcome and effective date of File 261020 &mdash; pending committee action, not enacted. <span class="badge warn">pending legislation</span></li>
  </ul>
  <p class="small">Each of these is a cell a reader might expect to be filled. They are blank because filling them
  would have meant guessing.</p>
</section>

<section class="panel">
  <h2>What is <em>not</em> flagged</h2>
  <ul>
    <li>The current 1.6% allowance, the 1.4% prior-year figure and the full historical table.</li>
    <li>Coverage of a pre-1979 two-unit building.</li>
    <li>The existence and mechanics of the rent increase licence, and the March 1 Housing Inventory deadline.</li>
    <li>The 30/90-day notice rule and the null-and-void consequence of a non-conforming increase.</li>
    <li>The $59.00 fee for 2026-27.</li>
    <li>That AB 1482's cap does not apply to these units.</li>
  </ul>
  <p class="small">These were confirmed directly against the official pages linked throughout the site.</p>
</section>
"""
    return layout("Flagged for review", resolve(b), active="pages/flagged.html", rel="../")
