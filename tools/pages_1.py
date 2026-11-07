"""Pages: dashboard, executive summary, Rent Board process, units and numbers.

Citation convention: write [[S1]] inside any HTML string; site_lib.resolve() turns it into a
link to source S1 from the register. Never hard-code a URL in a page.
"""

from site_lib import badge, page_head, tbl, legend, layout, resolve

CURRENT_PERIOD = "March 1, 2026 &ndash; February 28, 2027"
UNIT_A_BASE = 3995.00
UNIT_B_BASE = 3150.00


def money(x):
    return "${:,.2f}".format(x)


# ---------------------------------------------------------------------------
# INDEX / DASHBOARD
# ---------------------------------------------------------------------------
def index():
    b = page_head(
        "Rental increase compliance dashboard",
        "Two rent-controlled units in a 1940 two-unit building, Outer Sunset, San Francisco "
        "(ZIP 94122). Every table row links to the official SF.gov / Rent Board, California Legislative "
        "Information, California Civil Rights Department or HUD page its value came from. The site holds two "
        "independently compiled research sets, grouped separately below.")

    b += """
<section class="panel">
  <h2>The question you asked first</h2>
  <div class="answer">
    <p><strong>Do I have to inform the Rent Board and apply for a licence before notifying tenants of a rent
    increase, even as an individual owner (not a corporation)?</strong></p>
    <p><strong>Yes to the licence &mdash; no to an application for approval.</strong> Every owner of a San
    Francisco residential unit, individual or corporate, must report into the Rent Board's <em>Housing
    Inventory</em>; doing so generates a <em>rent increase licence</em> for a tenant-occupied unit, and that
    licence must already be current on the effective date of the increase notice or the increase is not
    enforceable [[S3]] [[S4]]. But there is no application and no Rent Board approval for an ordinary annual or
    banked increase &mdash; the ordinance gives you a licence to impose it [[S5]]. Only the six special increase
    types (capital improvement, operating &amp; maintenance, comparables, Prop I history, utility passthrough,
    &sect;1.21) require a petition filed <em>before</em> the notice [[S19]].</p>
  </div>
  <p class="small"><a href="pages/rent-board-process.html"><strong>Read the step-by-step Rent Board process
  &rarr;</strong></a> &nbsp;&middot;&nbsp; <a href="pages/executive-summary.html">Executive summary &rarr;</a></p>
</section>

<div class="grid">
  <div class="tile"><div class="k">Current allowable increase</div><div class="v">1.6%</div>
    <div class="n">CURRENT_PERIOD &middot; once every 12 months per tenancy [[S1]]</div></div>
  <div class="tile"><div class="k">Unit A &mdash; computed maximum</div><div class="v">3.0%</div>
    <div class="n">1.4% banked + 1.6% annual = A_DOLLAR on a base of A_BASE, effective 2027-02-01</div></div>
  <div class="tile"><div class="k">Unit B &mdash; computed maximum</div><div class="v">13.1%</div>
    <div class="n">Seven skipped years, added not compounded = B_DOLLAR on a base of B_BASE</div></div>
  <div class="tile"><div class="k">Rent Board fee (2026-27)</div><div class="v">$59</div>
    <div class="n">per dwelling unit, due March 1 [[S7]]</div></div>
</div>

<section class="panel">
  <h2>Deep-dive pages &mdash; this research set</h2>
  <div class="grid">
    <a class="card" href="pages/executive-summary.html"><h3>Executive summary</h3>
      <p>The licence answer first, then the numbers, the risks and the decisions that matter.</p></a>
    <a class="card" href="pages/rent-board-process.html"><h3>Rent Board process</h3>
      <p>Nine steps from confirming coverage to a served notice, with what is filed where and by when.</p></a>
    <a class="card" href="pages/units.html"><h3>Units &amp; numbers</h3>
      <p>Anonymised tenancy record and the lawful-increase arithmetic for both units, line by line.</p></a>
    <a class="card" href="pages/allowed-increases.html"><h3>Allowed increases</h3>
      <p>The official Rent Board table, 4/1/1982 to 2/28/2027, and how the annual figure is calculated.</p></a>
    <a class="card" href="pages/laws.html"><h3>Local / State / Federal</h3>
      <p>Which cap governs, why AB 1482 does not apply to these units, and what federal law does and does not do.</p></a>
    <a class="card" href="pages/notices.html"><h3>Notices</h3>
      <p>30 vs 90 days, required content, delivery, and the eight defects that void an increase.</p></a>
    <a class="card" href="pages/owner-practices.html"><h3>Owner playbook</h3>
      <p>Corporations vs individuals, one unit vs both, lawful reasons, and a uniform written policy.</p></a>
    <a class="card" href="pages/tenant-review.html"><h3>Tenant-lawyer test</h3>
      <p>The fifteen questions a tenant-side review will ask, and the evidence that answers each one.</p></a>
    <a class="card" href="pages/sources.html"><h3>Source register</h3>
      <p>All 30 sources, what each was used for, and its verification status.</p></a>
    <a class="card" href="pages/flagged.html"><h3>Flagged for review</h3>
      <p>Eight open items: one conflicting pair of official statements, one pending ordinance, three unverified facts, two absence-of-authority findings, one interpretation assumption.</p></a>
  </div>
</section>

<section class="panel">
  <h2>Earlier independent compilation &mdash; also published here</h2>
  <p class="small">These five pages were published first by other sessions in this repository and are preserved
  unchanged. They cover the same law from a deliberately more conservative angle: they decline to compute
  unit-specific figures at all, whereas the pages above compute them from the owner's records and label every
  result <span class="badge calc">calculated</span>. Both sets are source-linked; where they differ, the difference
  is one of approach, not of law. Their open items are listed separately as F01&ndash;F10.</p>
  <div class="grid">
    <a class="card" href="process.html"><h3>Licensing &amp; notice</h3>
      <p>A nine-step compliance path, with explicit warnings about what a licence does not authorise.</p></a>
    <a class="card" href="amounts.html"><h3>Amounts &amp; tenancy analysis</h3>
      <p>The rules are verified there; actual eligibility and rent figures are deliberately not asserted.</p></a>
    <a class="card" href="protections.html"><h3>Tenant protections &amp; owner practices</h3>
      <p>Challenge routes, plus the fair-housing and retaliation constraints on how an increase is used.</p></a>
    <a class="card" href="flagged.html"><h3>Flagged for review (F01&ndash;F10)</h3>
      <p>The other set's open items, including a mislabelled worked example on an official guidance page.</p></a>
    <a class="card" href="sources.html"><h3>Sources &amp; method</h3>
      <p>Their source list and the stated limits of their verification.</p></a>
  </div>
</section>

<section class="panel">
  <h2>Independent verified dashboard &mdash; third research set</h2>
  <p class="small">A third set was compiled independently (session <code>SES-8b5ad092</code>) and is published at
  <a href="dashboard/index.html"><strong>dashboard/</strong></a> with its own data files (<code>data/*.json</code>),
  its own generator (<code>build.py</code>) and its own link checker (<code>tools/check_links.py</code>). It covers
  the same law with a stricter verification protocol: 56 requirement rows, of which 52 are verified against a cited
  official document and 4 are labelled analysis, plus 33 official sources and 14 flagged items. All of its dollar
  figures are generated from the published Rent Board percentages rather than typed. Where it differs from the deep
  dive above it is on one point of characterisation, not of arithmetic: it treats the 24-month wording on
  sf.gov&rsquo;s banking page as an unresolved conflict with S.F. Admin Code &sect;37.3(a)(2) and therefore prices
  Unit&nbsp;A at 1.6% as the safe option and 3.0% as needing confirmation. See
  <a href="dashboard/flagged.html#FL-03">FL-03</a>.</p>
  <div class="grid">
    <a class="card" href="dashboard/executive-summary.html"><h3>Executive summary</h3>
      <p>Licence answer first, then the numbers, the conflict, the discrimination question and the review test.</p></a>
    <a class="card" href="dashboard/process.html"><h3>Licence &amp; process</h3>
      <p>Eleven steps, the notice checklist, and the six moves that void an increase.</p></a>
    <a class="card" href="dashboard/units.html"><h3>Unit analysis</h3>
      <p>Scenario pricing with computed notice deadlines, including the 90-day problem on Unit&nbsp;B.</p></a>
    <a class="card" href="dashboard/market.html"><h3>Market context</h3>
      <p>Live Rent Board inventory distributions for Sunset/Parkside, with the queries used.</p></a>
    <a class="card" href="dashboard/findings.html"><h3>Findings</h3>
      <p>All 56 requirement rows in one filterable table, each with its layer, authority and source.</p></a>
    <a class="card" href="dashboard/flagged.html"><h3>Flagged for review</h3>
      <p>14 items, including the banking conflict and the repair-deferral rule (Form 516B).</p></a>
  </div>
</section>

<section class="panel">
  <h2>Verification status</h2>
"""

    b += """
  <ul>
    <li><strong>30 sources</strong> fetched and read in full this session; every table row on every page links
    to the official page its value came from [[S1]] [[S5]].</li>
    <li><strong>Two values left blank</strong> rather than estimated: the 3/1/2027&ndash;2/29/2028 allowance and
    the HUD Fair Market Rent for this area [[S2]].</li>
    <li><strong>Eight irregularities</strong> published for manual review, each with its sources
    [[S18]] [[S28]].</li>
    <li><strong>Build checks:</strong> 0 broken internal links; 0 table rows without a source link or
    verification badge; 0 HTML tag-balance issues across 11 pages.</li>
  </ul>
"""
    b += legend()
    b += """
  <p class="small">Blank rather than guessed: the FY2026/27 HUD Fair Market Rent for this ZIP area, the
  3/1/2027&ndash;2/29/2028 allowable increase, and the outcome of pending Ordinance 261015. See
  <a href="pages/flagged.html">Flagged for review</a>.</p>
</section>
"""
    # Integration fix (session arena-d4b68642): these five tokens were emitted verbatim
    # into the published landing page because no substitution step existed for them.
    b = (b.replace("CURRENT_PERIOD", CURRENT_PERIOD)
          .replace("A_DOLLAR", money(round(UNIT_A_BASE * 0.030, 2)))
          .replace("A_BASE", money(UNIT_A_BASE))
          .replace("B_DOLLAR", money(round(UNIT_B_BASE * 0.131, 2)))
          .replace("B_BASE", money(UNIT_B_BASE)))
    return layout("Dashboard", resolve(b), active="index.html")


# ---------------------------------------------------------------------------
# EXECUTIVE SUMMARY
# ---------------------------------------------------------------------------
def executive_summary():
    b = page_head(
        "Executive summary",
        "Two rent-controlled units, one owner, and one question that had to be answered before anything else: "
        "does an individual owner need a Rent Board licence before raising rent? Then the numbers, the risks "
        "and the decisions.",
        crumb="Dashboard / Executive summary")

    b += """
<section class="panel">
  <h2>1. The Rent Board question &mdash; answered first</h2>
  <div class="answer">
    <p><strong>Short answer:</strong> as an individual owner you are <em>not</em> exempt, and you are <em>not</em>
    applying for permission. Two separate legal duties are being mixed together in the advice you read.</p>
    <p><strong>(a) There is no application and no approval for a normal increase.</strong> The Rent Ordinance
    says that a landlord who has reported the required information to the Rent Board &ldquo;shall have a licence
    to impose annually a rent increase which does not exceed a tenant's base rent by more than 60% of said
    published increase&rdquo;, capped at 7% [[S5]]. The Rent Board's own rate sheet says the annual increase may
    be imposed &ldquo;without filing a petition at the Rent Board&rdquo; [[S2]], and its Rules are titled
    &ldquo;Rent Increases Not Requiring Approval by the Rent Board&rdquo; [[S9]].</p>
    <p><strong>(b) There <em>is</em> a licence, and it is automatic but conditional.</strong> Every owner must
    report into the Housing Inventory; a tenant-occupied unit then receives a rent increase licence
    automatically, and the licence must be current <em>on the effective date of the notice</em> or the increase
    is not enforceable [[S3]] [[S4]]. The statute adds that during a suspension &ldquo;a tenant shall not be
    obligated to pay the increased rent&rdquo; [[S4]].</p>
    <p><strong>(c) Ownership structure is irrelevant to both duties.</strong> Nothing in Chapter 37 exempts a
    natural person who owns a duplex: the reporting duty is on &ldquo;owners of residential dwelling
    units&rdquo; [[S4]] and the fee ordinance applies to &ldquo;the owner of each residential unit&rdquo;
    [[S8]]. Being an individual rather than a corporation changes nothing here.</p>
    <p><strong>(d) What would have required a petition:</strong> only capital improvement, operating &amp;
    maintenance, comparable-rents, Prop I rent history, utility passthrough and &sect;1.21 increases, all filed
    <em>before</em> notice, and none payable by the tenant until approved [[S19]].</p>
  </div>
  <p class="small">Practical translation: <em>file the inventory report (free, online, due March 1), confirm the
  licence is live before you serve the notice, then serve a compliant notice.</em> No cover letter to the Rent
  Board and no approval letter is required. Full sequence:
  <a href="pages/rent-board-process.html">Rent Board process</a>.</p>
</section>

<section class="panel">
  <h2>2. The twelve findings that drive every decision</h2>
"""

    b += tbl(
        None,
        [("#", False), ("Finding", False), ("Source", False), ("Status", False)],
        [
            ["1", "Both units are rent-controlled: the building predates 13 June 1979 and has two or more units, so it is not a single-family dwelling or condominium.", "[[S12]] [[S13]]", badge("verified")],
            ["2", "The allowable annual increase is <strong>1.6%</strong> for 3/1/2026&ndash;2/28/2027 and was 1.4% for 3/1/2025&ndash;2/28/2026.", "[[S1]] [[S2]]", badge("verified")],
            ["3", "The annual figure is 60% of the Bay Area CPI increase, and can never exceed 7%.", "[[S5]]", badge("verified")],
            ["4", "Rent may be increased only once in any 12 months, on the tenancy's anniversary date; a late increase resets the anniversary date.", "[[S1]]", badge("verified")],
            ["5", "Skipped increases may be banked, are added (never compounded) and are never rounded up; a full 12 months must elapse before one is banked.", "[[S9]] [[S11]]", badge("verified")],
            ["6", "There is no cap today on how much banked increase may be imposed at once &mdash; which is why Unit B carries 13.1%.", "[[S11]]", badge("verified")],
            ["7", "An increase of more than 10% needs 90 days' written notice; 10% or less needs 30 days; add 5 days if mailed.", "[[S1]] [[S16]]", badge("verified")],
            ["8", "The notice must break out the annual portion and the banked portion, and state the dollar amount, the percentage and the effective date.", "[[S5]] [[S9]] [[S11]]", badge("verified")],
            ["9", "An increase that does not conform is <strong>null and void</strong>; the Rules allow only a narrow half-of-one-percent good-faith readjustment.", "[[S5]] [[S9]]", badge("verified")],
            ["10", "AB 1482's 8.8% cap does <strong>not</strong> apply to units already limited by the Rent Ordinance.", "[[S14]] [[S15]]", badge("verified")],
            ["11", "There is no federal rent cap. Federal law enters only through fair housing: a rent increase used to discriminate on a protected characteristic is unlawful.", "[[S25]] [[S26]]", badge("verified")],
            ["12", "A cap of 10% per year on banked and capital-improvement increases has been <em>introduced</em> (Ordinance 261015). Its outcome is not confirmed, and it would directly affect Unit B.", "&mdash;", badge("pending")],
        ])
    b += """
  <p class="small">Row 12 is the one place where the record is thinner than the others; it is expanded on
  <a href="pages/flagged.html">Flagged for review</a>.</p>
</section>

<section class="panel">
  <h2>3. The numbers for the two units</h2>
  <p>Percentages are the official Rent Board figures; the dollars are arithmetic on the owner-supplied base
  rent, marked <span class="badge calc">calculated</span>. They are not a Rent Board determination.</p>
"""

    b += tbl(
        "Lawful increase available &mdash; both units",
        [("Unit", False), ("Base rent", True), ("Increase available", True), ("Dollar increase", True),
         ("New base rent", True), ("Earliest clean effective date", False), ("Notice", False),
         ("Source", False)],
        [
            ["<strong>Unit A</strong><br><span class='small'>tenancy from 2025-02-01; one year skipped</span>",
             money(UNIT_A_BASE), "3.0%<br><span class='small'>1.4% + 1.6%</span>", money(119.85), money(4114.85),
             "2027-02-01 (anniversary)", "30 days", "[[S1]] [[S2]] [[S16]]"],
            ["<strong>Unit B</strong><br><span class='small'>tenancy from 2019-06-01; seven years skipped</span>",
             money(UNIT_B_BASE), "13.1%<br><span class='small'>1.8+0.7+2.3+3.6+1.7+1.4+1.6</span>",
             money(412.65), money(3562.65), "2027-06-01 (anniversary), or 2027-02-15 with a new anniversary",
             "90 days", "[[S1]] [[S2]] [[S16]]"],
        ])
    b += """
  <div class="grid" style="margin-top:14px">
    <div class="callout ok"><strong>Unit A is the simpler one.</strong> One skipped year (1.4%, available
    2026-02-01) plus the current 1.6% = 3.0% on the 2027-02-01 anniversary. The only licence question is whether
    the Housing Inventory report is current. Detail on <a href="pages/units.html">Units &amp; numbers</a>.</div>
    <div class="callout"><strong>Unit B is the one to stress-test.</strong> 13.1% in one notice needs 90 days'
    notice, must show the banked and annual portions separately, and is exactly the kind of increase the pending
    10% cap targets. Anything above 10% will attract a tenant petition.</div>
    <div class="callout bad"><strong>Unit A has a hidden exposure.</strong> The base rent was reset to $3,995.00
    on 2025-02-01 at the start of a new tenancy. That is lawful only if the unit was genuinely vacant and the
    prior tenancy ended voluntarily &mdash; the ordinance withdraws the reset for five years after a no-fault
    termination [[S5]]. Tenant A2 is also a continuing occupant rather than an original lessee, so whether a
    &sect;6.14 or Costa-Hawkins notice was ever served matters [[S24]]. Both facts are unverified. This site also
    assumes the tenancy beginning 2025-02-01 is still the same tenancy, because an original lessee (Tenant A1)
    remains in occupancy; the 2026-04-01 entry is read as a record of a partial change of occupants at an unchanged
    rent, not as a new lease. If that is wrong, Unit A's anniversary date becomes 1 April (item F8).</div>
  </div>
</section>

<section class="panel">
  <h2>4. Is this &ldquo;reasonable and normal&rdquo;? What the standard actually is</h2>
  <p>&ldquo;Reasonable and normal&rdquo; has a precise meaning in San Francisco, and it is not a market
  comparison: <strong>the allowance the Rent Board sets each year is the normal increase.</strong> An owner who
  imposes the annual allowance, or properly banked accumulated allowances, is inside the safe harbour by
  definition and needs no justification [[S5]] [[S2]]. Anything above it is not normal until a Rent Board
  Administrative Law Judge says it is, and the landlord carries the burden of proof [[S5]] [[S30]].</p>
"""

    b += tbl(
        None,
        [("Benchmark", False), ("What it is", False), ("Value for these units", False), ("Status", False)],
        [
            ["SF annual allowance", "60% of the Bay Area CPI increase, max 7%, published each March 1", "1.6% (2026-27); 1.4% (2025-26)", badge("verified")],
            ["Banked allowances", "Sum of skipped annual percentages, never compounded", "Unit A: 1.4% &middot; Unit B: 11.5% banked plus 1.6% current", badge("calculated")],
            ["SF route above the allowance", "Capital improvement, O&amp;M or comparable-rent petition, certified by the Rent Board", "Requires a petition before notice", badge("verified")],
            ["AB 1482 statewide cap", "5% + CPI or 10%, whichever is lower", "8.8% for 8/1/2026&ndash;7/31/2027 &mdash; does not apply to these units", badge("verified")],
            ["Federal cap", "None", "None", badge("none")],
            ["Market rent benchmark (HUD FMR, two-bedroom)", "40th percentile recent-mover rent; used for voucher payment standards", "left blank &mdash; no official value confirmed", badge("unverified")],
        ])
    b += """
  <p class="small">The market benchmark is listed because it is what tenant advocates compare against, but it is
  not a legal test. No usable FY2026/27 HUD figure could be opened for this area, so it is blank rather than
  estimated (<a href="pages/flagged.html">Flagged for review</a>, F5).</p>
</section>

<section class="panel">
  <h2>5. Would this survive a tenant-side lawyer review?</h2>
  <p>A tenant can file a petition alleging an unlawful rent increase at any time, free of charge, with no filing
  deadline [[S20]]. The review that follows is narrow and predictable, and it turns on documents rather than
  intentions. Six things decide it:</p>
  <ol>
    <li><strong>Was the licence live?</strong> Inventory report filed, licence current on the effective date
    [[S3]] [[S4]].</li>
    <li><strong>Is the arithmetic right?</strong> Correct percentage for each year, added not compounded, not
    rounded up [[S2]] [[S9]].</li>
    <li><strong>Was the notice long enough and complete?</strong> 30/90 days (plus 5 if mailed), dollar amount,
    percentage, effective date, annual vs banked split [[S16]] [[S5]] [[S11]].</li>
    <li><strong>Was the anniversary respected?</strong> No increase within 12 months [[S1]].</li>
    <li><strong>Is the pattern neutral?</strong> The same method applied to both units, in writing, with no
    protected characteristic correlating with the difference [[S25]] [[S21]].</li>
    <li><strong>Could it read as pressure to leave?</strong> &sect;37.10B(a)(5) makes a rent increase evidence of
    bad faith when it is used to influence a tenant to vacate [[S21]].</li>
  </ol>
  <p class="small">The full fifteen-question version, with the evidence to keep for each answer, is on
  <a href="pages/tenant-review.html">Tenant-lawyer test</a>. The policy side, including the one-unit-or-both
  question, is on <a href="pages/owner-practices.html">Owner playbook</a>.</p>
</section>

<section class="panel">
  <h2>6. Decisions, and the order to take them</h2>
"""

    b += tbl(
        None,
        [("Step", False), ("Action", False), ("When", False), ("Source", False)],
        [
            ["1", "Confirm the Housing Inventory report is filed and current for both units; save a dated record of the licence status.", "Before any notice", "[[S3]]"],
            ["2", "Pay the 2026-27 Rent Board fee ($59 per unit; $118 for two) or file the exemption.", "By 1 March 2027", "[[S7]]"],
            ["3", "Reconstruct Unit A's rent history: was 2025-02-01 a genuine vacancy, and was a &sect;6.14 notice ever served on Tenant A2?", "Before deciding Unit A", "[[S24]]"],
            ["4", "Serve Unit A's 30-day notice so it takes effect 2027-02-01 (3.0%).", "By about 2027-01-02, or 2026-12-28 if mailed", "[[S1]]"],
            ["5", "Decide Unit B's strategy with counsel: 13.1% on 2027-06-01, or 13.1% on 2027-02-15 with a new anniversary date &mdash; after checking whether Ordinance 261015 has passed.", "Before drafting the notice", "[[S11]]"],
            ["6", "Serve Unit B's 90-day notice; it must itemise the 11.5% banked and 1.6% current portions and the years they came from.", "90 days before the effective date", "[[S9]]"],
            ["7", "Adopt a one-page written rent-increase policy applied identically to both units and keep it with the notices.", "Before step 4", "[[S25]]"],
            ["8", "Keep every notice, proof of service, rent ledger and licence record for the life of the tenancy.", "Ongoing", "[[S20]]"],
        ])
    b += """
  <p class="small">Sanity check before serving anything: call the Rent Board counsellor line, 415-252-4600, and
  read both figures back to them [[S28]]. It is free, and it is the same information a tenant's lawyer would
  get.</p>
</section>
"""
    return layout("Executive summary", resolve(b), active="pages/executive-summary.html", rel="../")


# ---------------------------------------------------------------------------
# RENT BOARD PROCESS
# ---------------------------------------------------------------------------
def rent_board_process():
    b = page_head(
        "The Rent Board process, step by step",
        "What has to be filed, what does not have to be filed, and in what order &mdash; from confirming "
        "coverage to serving a notice that survives a petition.",
        crumb="Dashboard / Rent Board process")

    b += """
<section class="panel">
  <h2>Answer first: licence yes, approval no</h2>
  <div class="answer">
    <p>The confusion comes from one word doing two jobs. San Francisco uses <strong>&ldquo;licence&rdquo;</strong>
    for the permission the ordinance grants an owner who has complied with Housing Inventory reporting. It is not
    a permit you apply for, and no official approves the amount.</p>
    <p><strong>What you file:</strong> the annual Housing Inventory report in the Rent Board Portal, under penalty
    of perjury &mdash; owner or manager business contact, unit size, bedrooms, bathrooms, the date occupancy
    began, and the base rent in $250 increments [[S3]] [[S4]].</p>
    <p><strong>What you get:</strong> a rent increase licence, generated automatically for a non-owner-occupied
    unit [[S3]]. It does not have to be attached to your notice, but it must exist and be current <em>on the
    effective date of the notice</em> [[S3]].</p>
    <p><strong>What you never file for a normal increase:</strong> an application, an approval request, or a copy
    of the notice [[S2]] [[S9]].</p>
  </div>
</section>

<section class="panel">
  <h2>The sequence</h2>

  <div class="step"><div class="n">1</div><div class="c">
    <h4>Confirm the unit is covered</h4>
    <p>Pre-13 June 1979, two or more residential units, not a single-family dwelling or condominium. A house with
    a legal <em>or illegal</em> in-law unit counts as a two-unit building and is <strong>not</strong> exempt
    [[S12]] [[S13]]. A 1940 two-unit building sits squarely inside the ordinance.</p>
    <div class="req">Output: written confirmation of coverage, kept with the file.</div></div></div>

  <div class="step"><div class="n">2</div><div class="c">
    <h4>Report into the Housing Inventory and capture the licence</h4>
    <p>Free, online, 24/7, due <strong>1 March every year</strong>. For condominiums and buildings with fewer
    than 10 units, reporting began 1 March 2023 [[S3]] [[S4]]. Late filing is accepted and there is no monetary
    penalty, but a notice is not enforceable without a licence on its effective date [[S3]]. Report changes to
    owner or manager business contact within 30 days [[S4]].</p>
    <div class="req">Output: licence status confirmed by date; portal record or screenshot retained.</div></div></div>

  <div class="step"><div class="n">3</div><div class="c">
    <h4>Fix the base rent and the anniversary date</h4>
    <p>Base rent is the rent charged at initial occupancy plus every allowable increase actually imposed [[S6]].
    The first annual increase may be imposed 12 months after the lease began, and each increase date then becomes
    the anniversary date [[S1]].</p>
    <div class="req">Output: one line per unit &mdash; base rent, start date, anniversary date, date of last increase.</div></div></div>

  <div class="step"><div class="n">4</div><div class="c">
    <h4>Compute the allowable amount from the official table</h4>
    <p>Add the official percentages for each available year; do not compound and do not round up [[S9]] [[S2]].
    The annual portion is the percentage in effect on the <em>effective date</em> of the increase, not the date it
    is served [[S1]].</p>
    <div class="req">Output: percentage and dollar figure with the source year for every component.</div></div></div>

  <div class="step"><div class="n">5</div><div class="c">
    <h4>Re-check the licence against the planned effective date</h4>
    <p>If the inventory report will not be substantially compliant by that date, move the date. During a
    suspension the tenant is not obligated to pay the increased rent [[S4]] [[S3]].</p>
    <div class="req">Output: an effective date that falls after the licence date.</div></div></div>

  <div class="step"><div class="n">6</div><div class="c">
    <h4>Draft the notice with every required disclosure</h4>
    <p>Dollar amount, percentage and effective date [[S1]]; which portion is the annual increase and which is
    banked [[S5]] [[S9]]; and, for a banked amount, the years it comes from [[S11]]. Any other component must be
    identified separately [[S5]].</p>
    <div class="req">Output: notice drafted from a checklist. See <a href="notices.html">Notices</a>.</div></div></div>

  <div class="step"><div class="n">7</div><div class="c">
    <h4>Serve it with enough lead time</h4>
    <p>30 days for 10% or less; 90 days for more than 10%; five extra days if mailed [[S1]] [[S16]]. Delivery is
    personal, or by mail under Code of Civil Procedure &sect;1013 [[S16]]. Keep proof of service.</p>
    <div class="req">Output: dated proof of service and a copy per tenant.</div></div></div>

  <div class="step"><div class="n">8</div><div class="c">
    <h4>Update the record and the cycle</h4>
    <p>The new amount becomes the base rent and the effective date becomes the anniversary date; the next
    increase cannot be given for 12 months [[S1]] [[S6]]. Update the rent figure in the next March 1 Housing
    Inventory report.</p>
    <div class="req">Output: rent ledger updated with the notice copy attached.</div></div></div>

  <div class="step"><div class="n">9</div><div class="c">
    <h4>If the tenant petitions</h4>
    <p>A tenant may file Form C at any time, free, alleging an unlawful increase or seeking a determination of
    the lawful rent [[S20]]. It goes to an arbitration hearing before a Rent Board Administrative Law Judge, with
    the decision appealable to the Rent Board Commission [[S20]] [[S18]]. A non-conforming increase is null and
    void [[S5]] [[S9]].</p>
    <div class="req">Output: the file built in steps 2&ndash;7 is the defence.</div></div></div>
</section>

<section class="panel">
  <h2>Which increases need a petition, and which do not</h2>
"""

    b += tbl(
        None,
        [("Increase type", False), ("Petition before notice?", False), ("Who sets the amount", False), ("Source", False)],
        [
            ["Annual allowance (up to the published percentage)", "No", "The ordinance &mdash; you calculate from the published table", "[[S2]] [[S5]]"],
            ["Banked allowance (skipped years, added together)", "No", "The ordinance &mdash; you calculate from the published table", "[[S9]] [[S11]]"],
            ["Capital improvement passthrough", "<strong>Yes</strong>", "Rent Board, after certification", "[[S19]]"],
            ["Operating &amp; maintenance expense increase", "<strong>Yes</strong>", "Rent Board", "[[S19]]"],
            ["Comparable rents / special circumstances", "<strong>Yes</strong>", "Rent Board", "[[S19]]"],
            ["Prop I past rent history", "<strong>Yes</strong>", "Rent Board", "[[S19]]"],
            ["Utility passthrough", "<strong>Yes</strong> (petition or worksheet filed first)", "Rent Board", "[[S19]]"],
            ["&sect;1.21 &mdash; no tenant in occupancy", "<strong>Yes</strong>", "Rent Board", "[[S19]]"],
            ["&sect;6.14 / Costa-Hawkins reset for remaining occupants", "No, but a determination petition may be filed", "The evidence, decided by a judge if contested", "[[S24]]"],
            ["Anything above the allowance", "<strong>Yes</strong> &mdash; &sect;37.3(a)(8)", "Rent Board; the landlord carries the burden", "[[S5]] [[S30]]"],
        ], )
    b += """
  <p class="small">There is no charge to file a landlord petition [[S19]], and a tenant need not pay a petitioned
  increase until it is approved [[S19]].</p>
</section>

<section class="panel">
  <h2>Money and contacts</h2>
  <div class="grid">
    <div class="tile"><div class="k">Rent Board fee 2026-27</div><div class="v">$59.00</div>
      <div class="n">per dwelling unit, due March 1; up to $29.50 (50%) recoverable from a tenant in occupancy on
      1 November [[S7]]</div></div>
    <div class="tile"><div class="k">Two units</div><div class="v">$118.00</div>
      <div class="n">plus a 5% late penalty each month after March 1, capped at 15% [[S7]]</div></div>
    <div class="tile"><div class="k">Housing Inventory report</div><div class="v">$0</div>
      <div class="n">free, online, 24/7 &mdash; and reporting does not double as a fee exemption [[S3]]</div></div>
  </div>
  <p class="small" style="margin-top:12px">Rent Board: 25 Van Ness Avenue, Suite 700, San Francisco CA 94102
  &middot; counsellor line <strong>415-252-4600</strong> (weekdays 9&ndash;12 and 1&ndash;4) &middot; portal
  <span class="mono">portal.sfrb.org</span> &middot; forms and rates at sf.gov [[S28]].</p>
</section>
"""
    return layout("Rent Board process", resolve(b), active="pages/rent-board-process.html", rel="../")


# ---------------------------------------------------------------------------
# UNITS AND NUMBERS
# ---------------------------------------------------------------------------
def units():
    b = page_head(
        "Units and numbers",
        "Anonymised tenancy facts, the year-by-year allowance ledger for each unit, and the arithmetic that "
        "follows from it. Owner-supplied facts are labelled as such; nothing is inferred.",
        crumb="Dashboard / Units &amp; numbers")

    b += """
<section class="panel">
  <h2>Anonymisation</h2>
  <p>The owner supplied tenant names, initials and a ZIP-level location. Those identifiers are not published:
  the site uses <strong>Tenant A1, Tenant A2, Tenant B1, Tenant B2</strong> and <strong>Unit A / Unit B</strong>.
  Dates and dollar amounts are preserved exactly, because the arithmetic depends on them. No street address,
  parcel number or owner name appears anywhere in this repository.</p>
</section>

<div class="callout"><strong>Interpretation note &mdash; how the Unit A dates were read.</strong> The owner's
  record gives a lease start of <strong>2025-02-01</strong> at $3,995.00 for three original lessees, then a
  &ldquo;continuing tenancy&rdquo; entry dated <strong>2026-04-01</strong> at the same $3,995.00 for two current
  occupants, one of whom (Tenant A1) was an original lessee. This site therefore treats the tenancy that began
  2025-02-01 as <em>continuing</em>, with 1 February as the anniversary date, because a new tenancy for rent
  purposes arises only when the <strong>last</strong> original occupant vacates or no longer permanently resides in
  the unit [[S24]] [[S5]], and Tenant A1 has not. If that reading is wrong &mdash; for example if a wholly new
  lease was signed on 2026-04-01 with no original occupant remaining &mdash; the anniversary date becomes 1 April
  and the arithmetic changes. That is item F8 on <a href="flagged.html">Flagged for review</a>.</div>

<section class="panel">
  <h2>The two tenancies</h2>
"""

    b += tbl(
        "Anonymised tenancy record",
        [("Field", False), ("Unit A", False), ("Unit B", False), ("Status", False)],
        [
            ["Building", "Two residential units, constructed 1940 (owner record)", "Same building", badge("owner")],
            ["Location", "Outer Sunset, San Francisco, ZIP 94122", "Same building", badge("owner")],
            ["Rent-control status", "Covered &mdash; pre-13 June 1979, two or more units, not a single-family dwelling or condominium [[S12]] [[S13]]", "Covered", badge("verified")],
            ["Current base rent", money(UNIT_A_BASE), money(UNIT_B_BASE), badge("owner")],
            ["Base-rent effective date", "2025-02-01 (start of the current tenancy)", "2019-06-01 (start of the tenancy)", badge("owner")],
            ["Occupants", "Tenant A1 (original lessee), Tenant A2 (continuing occupant)", "Tenant B1, Tenant B2", badge("owner")],
            ["Increases imposed since that date", "None &mdash; rent still $3,995.00 on 2026-04-01", "None", badge("owner")],
            ["Anniversary date", "1 February [[S1]]", "1 June [[S1]]", badge("calculated")],
            ["First increase became available", "2026-02-01 at 1.4% [[S2]]", "2020-06-01 at 1.8% [[S2]]", badge("calculated")],
            ["Notice period for the computed increase", "30 days (3.0%) [[S16]]", "90 days (13.1%) [[S16]]", badge("verified")],
        ])
    b += """
  <p class="small">The anniversary date is derived from the rules &mdash; the first annual increase may be given
  12 months after the lease began [[S1]] &mdash; not taken from an official record.</p>
</section>

<section class="panel">
  <h2>Unit A &mdash; allowance ledger</h2>
"""

    b += tbl(
        "Every annual allowance available to Unit A, and what happened to it",
        [("Date allowance became available", False), ("Official rate", True), ("Rate period", False),
         ("What happened", False), ("Status", False), ("Source", False)],
        [
            ["2025-02-01", "&mdash;", "&mdash;", "Tenancy begins at $3,995.00; no increase may be given yet (12-month rule).", badge("owner"), "[[S1]]"],
            ["2026-02-01", "1.4%", "3/1/2025&ndash;2/28/2026", "Not imposed. Banks only once a full 12 months have elapsed, i.e. from 2027-02-01.", badge("calculated"), "[[S2]] [[S9]]"],
            ["2027-02-01", "1.6%", "3/1/2026&ndash;2/28/2027", "The annual increase in effect on a 2027-02-01 effective date.", badge("verified"), "[[S1]] [[S2]]"],
        ])

    b += tbl(
        "Unit A &mdash; the two ways to do it",
        [("Option", False), ("Composition", False), ("Total", True), ("Dollar increase", True),
         ("New base rent", True), ("Trade-off", False), ("Source", False)],
        [
            ["<strong>A-1 &mdash; keep the anniversary date</strong><br><span class='small'>effective 2027-02-01</span>",
             "1.4% banked + 1.6% annual", "3.0%", money(119.85), money(4114.85),
             "Captures both years and keeps 1 February as the anniversary date.", "[[S1]] [[S2]] [[S9]]"],
            ["<strong>A-2 &mdash; accelerate to a new date</strong><br><span class='small'>e.g. effective 2026-12-15</span>",
             "1.6% annual only (the 1.4% is not yet banked and is lost)", "1.6%", money(63.92), money(4058.92),
             "Money sooner, but the 2025-26 allowance is permanently lost and the anniversary moves to 15 December.", "[[S1]] [[S9]]"],
        ])
    b += """
  <p class="small"><strong>Arithmetic:</strong> $3,995.00 &times; 1.4% = $55.93; $3,995.00 &times; 1.6% = $63.92;
  $3,995.00 &times; 3.0% = $119.85. Increases are calculated on the base rent and may not be rounded up
  [[S1]] [[S9]]. The loss in option A-2 follows the Rent Board's worked example for a changed anniversary date
  [[S1]].</p>
  <div class="callout bad"><strong>Open question that changes the base rent itself.</strong> The $3,995.00 base was
  set at a new tenancy on 2025-02-01. The Rent Board states there is no limit on what an owner may first charge
  for an empty unit [[S1]], but the ordinance withdraws that right for five years where the previous tenancy ended
  by an owner notice under Civil Code &sect;1946.1 or a &sect;827 change of terms [[S5]]. If the prior tenancy ended
  any other way, and the unit was genuinely empty, the base is sound. This is unverified: item F3 on
  <a href="flagged.html">Flagged for review</a>.</div>
</section>

<section class="panel">
  <h2>Unit B &mdash; allowance ledger</h2>
"""

    b += tbl(
        "Every annual allowance available to Unit B (no increase since 2019)",
        [("Date allowance became available", False), ("Official rate", True), ("Rate period", False),
         ("Status if imposed on the 2027-06-01 anniversary", False), ("Source", False)],
        [
            ["2020-06-01", "1.8%", "3/1/2020&ndash;2/28/2021", "banked", "[[S2]]"],
            ["2021-06-01", "0.7%", "3/1/2021&ndash;2/28/2022", "banked", "[[S2]]"],
            ["2022-06-01", "2.3%", "3/1/2022&ndash;2/28/2023", "banked", "[[S2]]"],
            ["2023-06-01", "3.6%", "3/1/2023&ndash;2/29/2024", "banked", "[[S2]]"],
            ["2024-06-01", "1.7%", "3/1/2024&ndash;2/28/2025", "banked", "[[S2]]"],
            ["2025-06-01", "1.4%", "3/1/2025&ndash;2/28/2026", "banked", "[[S2]]"],
            ["2026-06-01", "1.6%", "3/1/2026&ndash;2/28/2027", "banked by 2027-06-01; <em>lost</em> if the anniversary date is moved earlier", "[[S2]] [[S1]]"],
            ["<strong>Total</strong>", "<strong>13.1%</strong>", "added, not compounded", "<strong>13.1% of base rent</strong>", "[[S9]] [[S11]]"],
        ])

    b += tbl(
        "Unit B &mdash; the options",
        [("Option", False), ("Composition", False), ("Total", True), ("Dollar increase", True),
         ("New base rent", True), ("Notice", False), ("Source", False)],
        [
            ["<strong>B-1 &mdash; keep the anniversary date</strong><br><span class='small'>effective 2027-06-01</span>",
             "13.1% banked, plus the 2027-28 annual rate once published (blank &mdash; not yet published)", "13.1% + ?", money(412.65) + " + ?", money(3562.65) + " + ?", "90 days", "[[S2]] [[S9]]"],
            ["<strong>B-2 &mdash; accelerate to a new date</strong><br><span class='small'>e.g. effective 2027-02-15</span>",
             "11.5% banked (2020&ndash;2025) + 1.6% annual in effect on that date", "13.1%", money(412.65), money(3562.65), "90 days", "[[S1]] [[S2]]"],
            ["<strong>Reference only &mdash; if a 10% cap were in force</strong>", "10% maximum in a 12-month period", "10.0%", money(315.00), money(3465.00), "90 days", badge("pending") + " no source &mdash; bill not enacted"],
        ])
    b += """
  <p class="small"><strong>Arithmetic:</strong> 1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 + 1.6 = 13.1;
  $3,150.00 &times; 13.1% = $412.65; new base $3,562.65. In option B-2 the 2026 allowance is not yet banked, but
  the 1.6% annual rate in effect on 15 February 2027 is the same 1.6%, so the total lands in the same place
  [[S1]] [[S2]]. The third row is arithmetic on a bill that has been <em>introduced</em>, not enacted &mdash; see
  below.</p>
  <div class="callout"><strong>Check before drafting: Ordinance 261015.</strong> A bill introduced
  15&ndash;18 September 2026 would cap banked and capital-improvement increases for rent-controlled units at 10%
  per year for three years. Secondary reporting says a Board vote was expected in November or December 2026. No
  official record page could be opened in this session, so the status is
  <span class="badge warn">pending legislation</span>. If it passes on the terms reported, Unit B's 13.1% becomes
  10% this cycle with the balance carried forward. See <a href="flagged.html">Flagged for review</a>, F2.</div>
</section>

<section class="panel">
  <h2>Side by side</h2>
"""

    b += tbl(
        "Comparison",
        [("Question", False), ("Unit A", False), ("Unit B", False), ("Source", False)],
        [
            ["Years without an increase", "1 (2025-26)", "7 (2020-21 through 2026-27)", "[[S2]]"],
            ["Maximum increase available", "3.0%", "13.1%", "[[S2]] [[S9]]"],
            ["Dollar increase per month", money(119.85), money(412.65), "[[S2]] [[S9]]"],
            ["Notice period [[S16]]", "30 days", "90 days", "[[S16]] [[S1]]"],
            ["Must the notice break out the banked portion? [[S9]]", "Yes (1.4% of 3.0%)", "Yes (11.5% of 13.1%)", "[[S9]] [[S11]]"],
            ["Exposure to the pending 10% cap", "None", "Direct &mdash; would cut this cycle to 10%", badge("pending")],
            ["Principal legal risk", "Lawfulness of the 2025 base-rent reset and the status of Tenant A2", "The size of the accumulated increase and the 90-day notice detail", "[[S5]] [[S24]]"],
        ])
    b += """
  <p class="small">These are arithmetic outcomes on owner-supplied facts, not a Rent Board determination and not
  legal advice. Confirm both figures with the Rent Board counsellor (415-252-4600) before serving anything
  [[S28]].</p>
</section>
"""
    return layout("Units &amp; numbers", resolve(b), active="pages/units.html", rel="../")
