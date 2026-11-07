#!/usr/bin/env python3
"""Renders the static dashboard site into docs/ from data/*.json.

Everything rendered here is either (a) a value read out of data/allowable_increases.json
or data/computed.json, or (b) prose that is quoted from or directly supported by a
registered official source. Anything else is rendered blank and routed to flagged.html.
"""

import json
import os
from datetime import date

from site_shell import page, write, CSS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
DATA = os.path.join(ROOT, "data")

with open(os.path.join(DATA, "sources.json")) as f:
    SOURCES = json.load(f)["sources"]
with open(os.path.join(DATA, "allowable_increases.json")) as f:
    ALLOW = json.load(f)
with open(os.path.join(DATA, "units.json")) as f:
    UNITS = json.load(f)
with open(os.path.join(DATA, "computed.json")) as f:
    COMPUTED = json.load(f)

UNITS_BY_ID = {u["unit_id"]: u for u in UNITS["units"]}
COMP_BY_ID = {u["unit_id"]: u for u in COMPUTED["units"]}


# --------------------------------------------------------------------------- #
def src(key, label=None):
    """Render a source citation cell."""
    s = SOURCES[key]
    text = label or s["publisher"].split(" (")[0]
    return ('<span class="src"><a href="{}" target="_blank" rel="noopener" '
            'title="{}">{} &#8599;</a></span>').format(
        s["url"], s["title"].replace('"', "'"), text)


def money(v):
    return "&mdash;" if v is None else "${:,.2f}".format(v)


def pct(v):
    return "&mdash;" if v is None else "{:g}%".format(v)


def fdate(iso):
    if not iso:
        return "&mdash;"
    y, m, d = (int(x) for x in iso.split("-"))
    return date(y, m, d).strftime("%b %-d, %Y") if os.name != "nt" else date(y, m, d).strftime("%b %d, %Y")


def blank_note(text="Not yet published &mdash; no official source exists for this figure."):
    return '<span class="pill warn">blank</span> <span class="small muted">{}</span>'.format(text)


def topnav():
    return ('<div class="topnav"><a href="index.html">Overview</a> '
            '<a href="license.html">License</a> '
            '<a href="steps.html">Checklist</a> '
            '<a href="allowable.html">Rates</a> '
            '<a href="units.html">Units</a> '
            '<a href="notice.html">Notice</a> '
            '<a href="flagged.html">Flagged</a> '
            '<a href="sources.html">Sources</a></div>')


# --------------------------------------------------------------------------- #
# INDEX / EXECUTIVE SUMMARY
# --------------------------------------------------------------------------- #
def build_index():
    ua = COMP_BY_ID["A"]
    ub = COMP_BY_ID["B"]
    ua_max = [s for s in ua["scenarios"] if s["key"] == "maximum_rule_4_12"][0]
    ub_max = [s for s in ub["scenarios"] if s["key"] == "maximum_rule_4_12"][0]
    ub_cons = [s for s in ub["scenarios"] if s["key"] == "conservative"][0]

    body = topnav() + """
<div class="grid g4">
  <div class="kpi"><div class="k">Allowed increase now</div><div class="v">1.6%</div>
    <div class="s">Mar 1, 2026 &ndash; Feb 28, 2027<br>{}</div></div>
  <div class="kpi"><div class="k">Rent Board fee 2026&ndash;27</div><div class="v">$59.00</div>
    <div class="s">per dwelling unit, due Mar 1<br>{}</div></div>
  <div class="kpi"><div class="k">License to raise rent</div><div class="v" style="color:#0f7b4f">Required</div>
    <div class="s">for individual owners too<br>{}</div></div>
  <div class="kpi"><div class="k">Annual reporting deadline</div><div class="v">Mar 1</div>
    <div class="s">every year, next: Mar 1, 2027<br>{}</div></div>
</div>

<div class="note bad">
  <b>Read this first &mdash; you cannot skip the Rent Board</b>
  Being an individual owner does <b>not</b> exempt you. San Francisco Administrative
  Code &sect;37.15 requires <b>every</b> owner of a residential dwelling unit to report
  into the Rent Board Housing Inventory. Only a landlord who has &ldquo;substantially
  complied&rdquo; receives a <b>license to impose rent increases</b> under &sect;&sect;37.3(a)(1)&ndash;(2).
  Without a current license on the effective date, the tenant is not obligated to pay
  the increase, and the Rent Board's own notice warns that
  &ldquo;some rent increases given without a license will be null and void.&rdquo;
  {} {} {}
</div>

<h2>Executive summary</h2>

<div class="card">
<h3>1. The license question &mdash; answered</h3>
<p><b>Do you need to apply for a license and inform the Rent Board before notifying
tenants? Yes to the first part, no to the second &mdash; and being an individual rather
than a corporation makes no difference.</b></p>
<ul class="tight">
  <li><b>You do <em>not</em></b> need to file a petition, get advance approval, or send
      the Rent Board a copy of your notice for an ordinary annual or banked increase.
      {}</li>
  <li><b>You <em>do</em></b> need a current <b>rent increase license</b>, which the Rent
      Board generates automatically once you complete the annual Housing Inventory
      report for a non-owner-occupied unit. {}</li>
  <li>You must <b>also</b> pay the annual Rent Board fee. It is a separate obligation
      from the license, with its own March 1 deadline and 5%-per-month late penalty.
      {}</li>
  <li>The statute says &ldquo;owners of residential dwelling units subject to this
      Chapter 37.&rdquo; There is no corporation / individual distinction anywhere in
      &sect;37.15, and the fee page states the fee applies to &ldquo;all residential
      property owners&hellip; This includes single-family homes and condominiums.&rdquo;
      {}</li>
</ul>
<p><b>Consequence of getting it wrong:</b> under &sect;37.15(e) the license is
<i>temporarily suspended</i> during noncompliance, it is restored only
<i>prospectively</i>, and &ldquo;a tenant shall not be obligated to pay the increased
rent for months during the period of suspension.&rdquo; You cannot retroactively
collect those months. {}</p>
</div>

<div class="card">
<h3>2. What a &ldquo;reasonable and normal&rdquo; increase looks like</h3>
<p>Both units are in a building built in 1940, so they sit on the covered side of San
Francisco's June 13, 1979 cutoff. The starting point for any increase is the single
percentage the Rent Board publishes each year: <b>1.6% for March 1, 2026 &ndash;
February 28, 2027</b>. {} A landlord may impose it <b>once every 12 months</b>, on the
tenant's anniversary date, and it requires <b>no justification at all</b> &mdash; no
cost increase, no improvement, no reason needs to be stated. {}</p>
<p>Anything above that has to come from a specific, documented mechanism: banked
increases from years you skipped, or a Rent Board&ndash;approved petition. {}</p>
</div>

<div class="card">
<h3>3. Recommended plan (both units, same method)</h3>
<div class="tw">
<table>
<thead><tr><th>Unit</th><th>Effective date</th><th>Recommended increase</th>
<th class="num">Increase</th><th class="num">New base rent</th>
<th>Notice</th><th>Serve by</th><th class="src">Source</th></tr></thead>
<tbody>
<tr>
  <td><b>Unit A</b><br><span class="small muted">base {abase}</span></td>
  <td class="nowrap">{ua_eff}<br><span class="small muted">on the anniversary</span></td>
  <td>{ua_pct} &mdash; current annual {ua_ann} + banked {ua_bk}</td>
  <td class="num">+{ua_amt}</td><td class="num"><b>{ua_new}</b></td>
  <td class="nowrap">{ua_days} days</td>
  <td class="nowrap">{ua_serve}<br><span class="small muted">{ua_mail} if mailed</span></td>
  <td class="src">{src571}</td>
</tr>
<tr>
  <td><b>Unit B</b><br><span class="small muted">base {bbase}</span></td>
  <td class="nowrap">{ub_eff}<br><span class="small muted">on the anniversary</span></td>
  <td>Current-year annual increase only<br>
      <span class="small muted">Leaves {ub_bk} of verified banked increases
      available for later years.</span></td>
  <td class="num">blank</td><td class="num">blank</td>
  <td class="nowrap">{ubc_days} days</td>
  <td class="nowrap">{ubc_serve}<br><span class="small muted">{ubc_mail} if mailed</span></td>
  <td class="src">{src827}</td>
</tr>
</tbody></table>
</div>
<p class="small muted">Unit B's annual percentage is left <b>blank on purpose</b>. The
Rent Board has not yet published the rate for the period containing June 1, 2027; it
publishes on or about January 1, effective March 1. There is no official source for that
number today, so we will not print one. {} The 90-day/30-day notice question is still
answerable, because the annual component is capped at 7% by &sect;37.3(a)(1). {}</p>
</div>

<div class="card">
<h3>4. The maximum lawful ceiling &mdash; and why we do not recommend it</h3>
<div class="tw">
<table>
<thead><tr><th>Unit</th><th>Banked available (verified)</th><th>Plus current annual</th>
<th class="num">Max total</th><th>Realistic outcome</th></tr></thead>
<tbody>
<tr><td><b>Unit A</b></td><td>1.4% (1 year skipped)</td><td>1.6%</td>
  <td class="num">3.0%</td>
  <td>+{ua_amt} &rarr; {ua_new}. Modest, unremarkable, hard to challenge.</td></tr>
<tr><td><b>Unit B</b></td><td>13.1% (7 years skipped)</td>
  <td>{ub_ann_blank}</td><td class="num">blank</td>
  <td>A one-year jump of roughly 13&ndash;15% is lawful <i>if</i> the banking is valid,
  but it is the single most likely thing on this page to trigger a tenant petition,
  a hardship application, or a discrimination complaint.</td></tr>
</tbody></table>
</div>
<p class="small muted">Unit B's banked figure of 13.1% is arithmetic straight from
Form 571 (1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 + 1.6) under Rent Board Rule 4.12's
12-month test. {} It assumes no increase has ever been served on that tenancy &mdash;
<b>unconfirmed</b>. {}</p>
</div>

<h2>The other questions, in one line each</h2>
<div class="grid g2">
  <div class="card tight"><h3>Local, state and federal limits</h3>
    <p class="small">San Francisco's 1.6% is the binding number. The state AB 1482 cap
    (5% + CPI, max 10%) does <b>not</b> stack on top of it &mdash; Civil Code
    &sect;1947.12(d)(3) exempts housing already under a lower local cap. Federal law
    adds no rent ceiling but bans discriminatory increases.</p>
    <p class="small"><a href="laws.html">Full three-tier breakdown &rarr;</a></p></div>

  <div class="card tight"><h3>Corporations vs. individuals</h3>
    <p class="small">The rent-increase rules are <b>identical</b>. The one place the
    statute actually distinguishes them: a <b>corporation</b> can never use the AB 1482
    single-family-home / condo exemption (&sect;1947.12(d)(5)(A)(ii)). San Francisco
    also bans algorithmic rent-setting software for everyone.</p>
    <p class="small"><a href="owners.html">Owner comparison &rarr;</a></p></div>

  <div class="card tight"><h3>How to tell tenants</h3>
    <p class="small">Written notice with the dollar amount, the percentage, the
    effective date, and &mdash; if any of it is banked &mdash; which portion is banked
    and the dates it is based on. 30 days if the increase is 10% or less, 90 days if
    more. Add 5 days if you mail it.</p>
    <p class="small"><a href="notice.html">Notice requirements &rarr;</a></p></div>

  <div class="card tight"><h3>Raise one unit or both?</h3>
    <p class="small">No law requires uniformity, but applying <b>the same method</b> to
    both units on each unit's own anniversary date is the most defensible posture.
    What creates exposure is a <i>difference in treatment that lines up with a
    protected characteristic</i> or follows a tenant complaint.</p>
    <p class="small"><a href="fair-housing.html">Discrimination analysis &rarr;</a></p></div>
</div>

<div class="note warn">
  <b>Before you serve anything</b>
  Two items on this dashboard are unresolved and could change the answer:
  (1) the property type has not been verified &mdash; if either unit is a single-family
  home or condominium, Costa-Hawkins removes the rent ceiling entirely because both
  tenancies began after January 1, 1996; and (2) no rent-increase history has been
  supplied, so every banked figure rests on an assumption.
  See <a href="flagged.html">Flagged for review</a>.
</div>
""".format(
        # 1-4: KPI cards
        src("SFRB-CURRENT-RATES"), src("SFRB-FEE"), src("SF-ORD-3715"),
        src("SFRB-2027-NOTICE"),
        # 5-7: headline warning note
        src("SFRB-PETITIONS"), src("SFRB-HOUSING-INVENTORY"), src("SFRB-FEE"),
        # 8-11: section 1 bullets
        src("SF-ORD-3715"), src("SFRB-HOUSING-INVENTORY"), src("SFRB-FEE"),
        src("SF-ORD-3715"),
        # 12-14: section 2
        src("SFRB-CURRENT-RATES"), src("SFRB-LEARN-RENT-INCREASES"),
        src("SFRB-PETITIONS"),
        # 15-19: section 3 and 4
        src("SFRB-571"), src("SF-ORD-373"),
        src("SFRB-571"), src("SFRB-RR-PART4"), src("SFRB-BANKED"),
        abase=money(ua["current_base_rent"]), ua_eff=fdate(ua["next_effective_date"]),
        ua_pct=pct(ua_max["total_percent"]), ua_ann=pct(ua_max["annual"]["percent"]),
        ua_bk=pct(ua_max["banked_percent"]), ua_amt=money(ua_max["increase_amount"]),
        ua_new=money(ua_max["new_base_rent"]),
        ua_days=ua_max["notice_days_required"], ua_serve=fdate(ua_max["serve_by_delivered"]),
        ua_mail=fdate(ua_max["serve_by_mailed"]),
        src571=src("SFRB-571"), src827=src("CA-CIV-827"),
        bbase=money(ub["current_base_rent"]), ub_eff=fdate(ub["next_effective_date"]),
        ub_bk=pct(ub_max["banked_percent"]),
        ubc_days=ub_cons["notice_days_required"], ubc_serve=fdate(ub_cons["serve_by_delivered"]),
        ubc_mail=fdate(ub_cons["serve_by_mailed"]),
        ub_ann_blank='<span class="pill warn">blank</span>',
    )
    return page("Executive summary", "index.html", body,
                "San Francisco rent increase research &mdash; Outer Sunset, ZIP 94122. "
                "Compiled 2026-11-07 from official government sources.")


# --------------------------------------------------------------------------- #
# LICENSE PAGE
# --------------------------------------------------------------------------- #
def build_license():
    body = topnav() + """
<div class="note ok">
  <b>Short answer</b>
  You do not apply for permission to raise the rent, but you must <b>hold a current
  rent increase license</b>, which you get automatically by completing the annual
  Housing Inventory report. This applies to individual owners exactly as it does to
  corporations.
</div>

<h2>What the law actually says</h2>
<div class="card">
<p>San Francisco Administrative Code &sect;37.15(e):</p>
<blockquote class="small" style="border-left:4px solid var(--line);padding-left:14px;margin:10px 0">
  &ldquo;If a landlord has substantially complied with the obligation to report
  information about a rental unit as required under this Section 37.15, the landlord
  shall receive a license to impose rent increases on tenants in that unit under
  Sections 37.3(a)(1)-(2). If the landlord has not substantially complied with the
  reporting obligation, then the license to impose rent increases shall be temporarily
  suspended during the period of the landlord's noncompliance. Upon receipt of the
  required information from the landlord, the suspension shall be terminated, and the
  license to impose rent increases shall be restored <b>prospectively</b>, but a tenant
  shall not be obligated to pay the increased rent for months during the period of
  suspension.&rdquo;
</blockquote>
<p class="src">{}</p>
<p>And &sect;37.3(a)(1) makes the license a precondition of the increase itself: the
clause reads &ldquo;A landlord <b>who has reported the required information about their
rental unit to the Rent Board as set forth in Section 37.15 shall have a license to</b>
impose annually a rent increase&hellip;&rdquo; {}</p>
</div>

<h2>The two separate obligations people confuse</h2>
<div class="tw">
<table>
<caption>Reporting and the fee are different things. Doing one does not do the other.</caption>
<thead><tr><th>Obligation</th><th>Who owes it</th><th>Deadline</th><th>What it produces</th>
<th class="src">Source</th></tr></thead>
<tbody>
<tr><td><b>Housing Inventory report</b><br><span class="small muted">Ordinance 265-20,
  added 2021</span></td>
    <td>Owners of residential dwelling units subject to Chapter 37</td>
    <td class="nowrap">March 1 annually<br><span class="small muted">next: Mar 1, 2027</span></td>
    <td><b>The rent increase license</b> &mdash; auto-generated for non-owner-occupied
        units once the submission is complete</td>
    <td class="src">{}</td></tr>
<tr><td><b>Rent Board fee</b><br><span class="small muted">Admin. Code Ch. 37A</span></td>
    <td>All residential property owners unless exempt &mdash; expressly including
        single-family homes, condos and post-1979 units</td>
    <td class="nowrap">March 1 annually<br><span class="small muted">5%/month penalty,
        capped at 15%</span></td>
    <td>Nothing by itself; $59.00 per dwelling unit for 2026&ndash;27, of which
        <b>$29.50</b> may be recovered from the tenant</td>
    <td class="src">{}</td></tr>
</tbody></table>
</div>
<p class="small">The Rent Board states this explicitly in more than one place:
&ldquo;Requesting a Rent Board Fee exemption does not satisfy Rent Board Housing
Inventory reporting requirements.&rdquo; {} {}</p>
<p class="small">The Rules and Regulations devote a whole part to implementing
&sect;37.15 &mdash; Part XIII, &ldquo;Reporting Obligations Under Rent Ordinance Section
37.15&rdquo; &mdash; including <b>Section 13.14, &ldquo;Licensing &ndash; Notice of Rent
Increase.&rdquo;</b> {}</p>

<div class="note warn">
  <b>Irregularity &mdash; logged for review</b>
  The Rent Board's pages tie the <i>license</i> to Housing Inventory reporting only.
  None of the official pages reviewed state whether being <i>delinquent on the fee</i>
  also suspends the license. Do not assume it is harmless. Confirm with a counselor
  before relying on it. <a href="flagged.html">See flagged item 4 &rarr;</a>
</div>

<h2>&ldquo;Inform the Rent Board&rdquo; &mdash; when you must, and when you must not</h2>
<div class="tw">
<table>
<thead><tr><th>Type of increase</th><th>File with the Rent Board first?</th>
<th>Timing</th><th class="src">Source</th></tr></thead>
<tbody>
<tr><td>Annual allowable increase</td><td><span class="pill ok">No</span></td>
  <td>No petition, no filing. Just hold a current license.</td>
  <td class="src">{}</td></tr>
<tr><td>Banked increase</td><td><span class="pill ok">No</span></td>
  <td>Not Rent Board&ndash;approved, but must be calculated correctly and itemised in
      the notice.</td><td class="src">{}</td></tr>
<tr><td>Capital improvement passthrough</td><td><span class="pill bad">Yes &mdash; petition</span></td>
  <td>Tenants need not pay until the Rent Board approves; approved increases are
      retroactive to a valid notice.</td><td class="src">{}</td></tr>
<tr><td>Operating &amp; maintenance increase</td><td><span class="pill bad">Yes &mdash; petition</span></td>
  <td>Same</td><td class="src">{}</td></tr>
<tr><td>Special circumstances / comparable rents</td><td><span class="pill bad">Yes &mdash; petition</span></td>
  <td>Same</td><td class="src">{}</td></tr>
<tr><td>Proposition I past rent history</td><td><span class="pill bad">Yes &mdash; petition</span></td>
  <td>Same</td><td class="src">{}</td></tr>
<tr><td>Utility passthrough</td><td><span class="pill warn">Petition or worksheet</span></td>
  <td>Worksheets must be filed with the Rent Board <b>before</b> serving the notice.</td>
  <td class="src">{}</td></tr>
<tr><td>Rules &amp; Regs &sect;1.21 (no tenant in occupancy)</td><td><span class="pill bad">Yes &mdash; petition</span></td>
  <td>Same</td><td class="src">{}</td></tr>
<tr><td>General obligation bond / water revenue bond passthrough</td>
  <td><span class="pill warn">Worksheet, not a petition</span></td>
  <td>Use the Rent Board worksheet; no petition needed.</td><td class="src">{}</td></tr>
<tr><td>Section 6.14 or Costa-Hawkins market-rate reset</td>
  <td><span class="pill ok">No &mdash; but a petition is available if unsure</span></td>
  <td>Not required; the Rent Board recommends legal advice first.</td>
  <td class="src">{}</td></tr>
</tbody></table>
</div>

<h2>What happens if you serve a notice without a license</h2>
<div class="grid g3">
  <div class="card tight"><b>The increase is unenforceable for the suspended months.</b>
    <p class="small">&sect;37.15(e): the license is restored only prospectively, and
    the tenant &ldquo;shall not be obligated to pay the increased rent for months during
    the period of suspension.&rdquo;</p></div>
  <div class="card tight"><b>The Rent Board may tell your tenants.</b>
    <p class="small">If you miss the deadline, the Rent Board may notify occupants that
    you are not in compliance.</p></div>
  <div class="card tight"><b>No penalty for filing late &mdash; but no increase either.</b>
    <p class="small">The Rent Board &ldquo;does not assess monetary penalties for filing
    after the deadline.&rdquo; The loss is the increase itself.</p></div>
</div>
<p class="src">{} {} {}</p>
""".format(
        src("SF-ORD-3715"), src("SF-ORD-373"),
        src("SFRB-HOUSING-INVENTORY"), src("SFRB-FEE"), src("SFRB-RR-1314"),
        src("SFRB-2027-NOTICE"), src("SFRB-FEE"),
        src("SFRB-LEARN-RENT-INCREASES"), src("SFRB-BANKED"),
        src("SFRB-PETITIONS"), src("SFRB-PETITIONS"), src("SFRB-PETITIONS"),
        src("SFRB-PETITIONS"), src("SFRB-PETITIONS"), src("SFRB-PETITIONS"),
        src("SFRB-PETITIONS"), src("SFRB-TOPIC-329"),
        src("SF-ORD-3715"), src("SFRB-HOUSING-INVENTORY"), src("SFRB-2027-NOTICE"),
    )
    return page("Do I need the Rent Board license?", "license.html", body,
                "The short version: you don't apply for permission, but you must hold a "
                "current license &mdash; and being an individual owner is not an exemption.")


# --------------------------------------------------------------------------- #
# STEPS PAGE
# --------------------------------------------------------------------------- #
def build_steps():
    ua = COMP_BY_ID["A"]
    ub = COMP_BY_ID["B"]
    ua_max = [s for s in ua["scenarios"] if s["key"] == "maximum_rule_4_12"][0]
    ub_cons = [s for s in ub["scenarios"] if s["key"] == "conservative"][0]

    body = topnav() + """
<h2>Do this, in this order</h2>
<ol class="steps">
  <li><b>Confirm the property is actually rent-controlled.</b>
    <span class="meta">Built 1940 clears the June 13, 1979 test, but it is not
    sufficient on its own. If either unit is a single-family home or a condominium,
    Costa-Hawkins removes the rent-increase ceiling because both tenancies began after
    January 1, 1996. A single-family dwelling with a legal or illegal in-law unit is a
    two-unit building and is <i>not</i> exempt. Check the
    <a href="https://sfplanninggis.org/PIM/" target="_blank" rel="noopener">SF Property
    Information Map</a>.</span>
    <span class="src">{} {}</span></li>

  <li><b>Pull the full rent history for each unit.</b>
    <span class="meta">Every banked-increase figure depends on it. If any increase was
    served and you cannot prove it, assume it did not happen.</span>
    <span class="src">{}</span></li>

  <li><b>Report into the Rent Board Housing Inventory at portal.sfrb.org.</b>
    <span class="meta">Required annually by <b>March 1</b> (next: March 1, 2027).
    Submitted under penalty of perjury. You will report square footage, bedrooms,
    bathrooms, occupancy date, and base rent in $250 increments.</span>
    <span class="src">{}</span></li>

  <li><b>Pay the Rent Board fee.</b>
    <span class="meta">$59.00 per dwelling unit for tax year 2026&ndash;27, due March 1.
    Separate from the license. If the property may be exempt, the 2027 exemption
    request deadline is <b>Monday, December 14, 2026</b> &mdash; and you must re-request
    every year.</span>
    <span class="src">{} {}</span></li>

  <li><b>Confirm the license issued.</b>
    <span class="meta">It is generated automatically for non-owner-occupied units after
    reporting. It does <b>not</b> get attached to the tenant's notice, but it must be
    current on the notice's effective date. Tenants can look it up in the portal too.</span>
    <span class="src">{}</span></li>

  <li><b>Pick the effective date &mdash; use the anniversary date.</b>
    <span class="meta">Unit A: <b>February 1</b>. Unit B: <b>June 1</b>. Moving the date
    earlier creates a <i>new</i> anniversary and can permanently forfeit an increase
    that had not yet been bankable for a full 12 months.</span>
    <span class="src">{} {}</span></li>

  <li><b>Calculate on base rent only, and do not round up.</b>
    <span class="meta">Base rent includes housing services such as parking or storage.
    It excludes temporary passthroughs and fluctuating charges. Banked increases are
    <b>added, not compounded</b>.</span>
    <span class="src">{} {}</span></li>

  <li><b>Serve written notice with the required content.</b>
    <span class="meta">Dollar amount, percentage, effective date, and &mdash; if any
    part is banked &mdash; which portion is banked and the dates it is based on.</span>
    <span class="src">{} {}</span></li>

  <li><b>Count the days correctly.</b>
    <span class="meta">30 days if the increase is 10% or less; 90 days if greater than
    10%, alone or combined with other increases in the prior 12 months. Add <b>5 days</b>
    if you mail it.</span>
    <span class="src">{}</span></li>

  <li><b>Keep proof of service.</b>
    <span class="meta">The Rent Board cannot adjudicate whether notice was received; if
    it is later disputed, the burden is on you.</span></li>
</ol>

<h2>Your two dates, computed</h2>
<div class="tw">
<table>
<thead><tr><th>Unit</th><th>Anniversary</th><th>Next lawful effective date</th>
<th>Increase to serve</th><th>Notice period</th><th>Serve by (hand-delivered)</th>
<th>Serve by (mailed)</th><th class="src">Source</th></tr></thead>
<tbody>
<tr><td><b>Unit A</b></td><td>Feb 1</td><td class="nowrap">{ua_eff}</td>
  <td>{ua_pct} &mdash; {ua_ann} annual + {ua_bk} banked<br>
      <span class="small muted">+{ua_amt}, new base {ua_new}</span></td>
  <td class="nowrap">{ua_days} days</td><td class="nowrap"><b>{ua_serve}</b></td>
  <td class="nowrap">{ua_mail}</td><td class="src">{s827}</td></tr>
<tr><td><b>Unit B</b></td><td>Jun 1</td><td class="nowrap">{ub_eff}</td>
  <td>Current-year annual only<br>
      <span class="small muted">percentage not yet published &mdash; see below</span></td>
  <td class="nowrap">{ub_days} days</td><td class="nowrap"><b>{ub_serve}</b></td>
  <td class="nowrap">{ub_mail}</td><td class="src">{s827}</td></tr>
</tbody></table>
</div>

<div class="note">
  <b>Unit B timing works out fine</b>
  The Rent Board publishes the next period's rate on or about January 1, effective
  March 1. Unit B's rate therefore appears around <b>January 1, 2027</b>, well before
  the {ub_serve} notice deadline. There is no reason to guess the number today.
  {} {}
</div>
""".format(
        src("SFRB-RENTAL-LAWS"), src("SFRB-COSTA-HAWKINS-SFR"),
        src("SFRB-BANKED"),
        src("SFRB-HOUSING-INVENTORY"),
        src("SFRB-FEE"), src("SFRB-2027-NOTICE"),
        src("SFRB-HOUSING-INVENTORY"),
        src("SFRB-LEARN-RENT-INCREASES"), src("SFRB-RR-PART4"),
        src("SFRB-LEARN-RENT-INCREASES"), src("SFRB-RR-PART4"),
        src("SFRB-LEARN-RENT-INCREASES"), src("SFRB-RR-PART4"),
        src("CA-CIV-827"),
        src("SFRB-571"), src("SF-ORD-373"),
        ua_eff=fdate(ua["next_effective_date"]), ua_pct=pct(ua_max["total_percent"]),
        ua_ann=pct(ua_max["annual"]["percent"]), ua_bk=pct(ua_max["banked_percent"]),
        ua_amt=money(ua_max["increase_amount"]), ua_new=money(ua_max["new_base_rent"]),
        ua_days=ua_max["notice_days_required"], ua_serve=fdate(ua_max["serve_by_delivered"]),
        ua_mail=fdate(ua_max["serve_by_mailed"]),
        ub_eff=fdate(ub["next_effective_date"]), ub_days=ub_cons["notice_days_required"],
        ub_serve=fdate(ub_cons["serve_by_delivered"]), ub_mail=fdate(ub_cons["serve_by_mailed"]),
        s827=src("CA-CIV-827"),
    )
    return page("Step-by-step checklist", "steps.html", body,
                "The exact order of operations, with the two notice deadlines already "
                "computed for your units.")


# --------------------------------------------------------------------------- #
# ALLOWABLE INCREASES PAGE
# --------------------------------------------------------------------------- #
def build_allowable():
    # Which published periods each unit's banked-increase maths actually draws on.
    banked_starts = {}
    for uid in ("A", "B"):
        comp = COMP_BY_ID[uid]
        mx = [s for s in comp["scenarios"] if s["key"] == "maximum_rule_4_12"][0]
        for b in mx["banked"]:
            # map the anniversary date back to the period that contained it
            for p in ALLOW["periods"]:
                if p.get("percent") is None:
                    continue
                if p["start"] <= b["anniversary"] <= p["end"]:
                    banked_starts.setdefault(p["start"], set()).add(uid)
                    break

    rows = []
    s571 = src("SFRB-571")
    for p in ALLOW["periods"]:
        y, m, d0 = (int(x) for x in p["start"].split("-"))
        y2, m2, d2 = (int(x) for x in p["end"].split("-"))
        span = "{} &ndash; {}".format(date(y, m, d0).strftime("%b %Y"),
                                    date(y2, m2, d2).strftime("%b %Y"))
        if p.get("percent") is None:
            rows.append("<tr><td class='nowrap'>{}</td><td class='num'>&mdash;</td>"
                        "<td colspan='2' class='small muted'>{}</td></tr>".format(
                            span, p.get("note", "")))
            continue
        cur = " <span class='pill info'>current</span>" if p["start"] == "2026-03-01" else ""
        who = banked_starts.get(p["start"], set())
        used = ", ".join("banked for Unit {}".format(u) for u in sorted(who)) if who else ""
        rows.append("<tr><td class='nowrap'>{}{}</td><td class='num'><b>{:g}%</b></td>"
                    "<td class='small muted'>{}</td><td class='src'>{}</td></tr>".format(
                        span, cur, p["percent"], used, s571))

    other = "".join(
        "<tr><td>{}</td><td><b>{}</b></td><td class='src'><a href='{}' target='_blank' "
        "rel='noopener'>source &#8599;</a></td></tr>".format(o["item"], o["value"], o["source_url"])
        for o in ALLOW["other_current_rates"])

    body = topnav() + """
<div class="grid g3">
  <div class="kpi"><div class="k">Current allowable increase</div><div class="v">1.6%</div>
    <div class="s">Mar 1, 2026 &ndash; Feb 28, 2027<br>{}</div></div>
  <div class="kpi"><div class="k">Statutory ceiling</div><div class="v">7%</div>
    <div class="s">&sect;37.3(a)(1): no annual increase may exceed 7%<br>{}</div></div>
  <div class="kpi"><div class="k">AB 1482 state cap</div><div class="v">Not applicable</div>
    <div class="s">Civ. Code &sect;1947.12(d)(3) excludes housing already under a lower
    local cap<br>{}</div></div>
</div>

<h2>How the number is set</h2>
<div class="card">
<p>The Rent Board publishes one percentage a year, effective March 1. It is
<b>60% of the increase in the Consumer Price Index for All Urban Consumers in the Bay
Area</b>, rounded to the nearest tenth, and it can never exceed 7%. {} {}</p>
<p>To turn it into dollars: <code>base rent &times; 0.016</code>. The Rent Board's own
example: a $2,000 base rent rises by $32.00 to $2,032.00. {}</p>
<ul class="tight">
  <li><b>Base rent only.</b> Includes housing services such as parking or storage;
      excludes temporary passthroughs and fluctuating charges. {}</li>
  <li><b>Do not round up.</b> {}</li>
  <li><b>Once every 12 months.</b> The first increase may be imposed 12 months after the
      lease began; after that, the effective date becomes the anniversary date. {}</li>
  <li><b>Use the rate in effect on the <i>effective date</i></b>, not the date you serve
      the notice. {}</li>
</ul>
</div>

<h2>Full published history (Rent Board Form 571)</h2>
<div class="tw">
<table>
<caption>Transcribed line by line from the official Form 571 (2026&ndash;27 edition).
Rows your units actually use are flagged.</caption>
<thead><tr><th>Effective period</th><th class="num">Allowable increase</th>
<th>Used by</th><th class="src">Source</th></tr></thead>
<tbody>
{}
</tbody></table>
</div>
<p class="small muted">Banking is only available for increases that could have been
imposed on or after <b>April 1, 1982</b>. {}</p>

<h2>Other current rates</h2>
<div class="tw"><table>
<thead><tr><th>Item</th><th>Rate / amount</th><th class="src">Source</th></tr></thead>
<tbody>{}</tbody></table></div>

<div class="note warn">
  <b>Why the 2019&ndash;2020 rate of 2.6% never appears in Unit B's maths</b>
  Unit B's tenancy began June 1, 2019, so its <i>first</i> increase eligibility date was
  June 1, 2020 &mdash; which falls in the 3/1/2020&ndash;2/28/2021 period (1.8%). The
  2.6% rate expired two months before that tenancy became eligible for any increase at
  all. This was caught by an automated self-test, not by hand.
</div>
""".format(
        src("SFRB-CURRENT-RATES"), src("SF-ORD-373"), src("CA-CIV-1947-12"),
        src("SF-ORD-373"), src("SFRB-571"), src("SFRB-LEARN-RENT-INCREASES"),
        src("SFRB-LEARN-RENT-INCREASES"), src("SFRB-LEARN-RENT-INCREASES"),
        src("SFRB-LEARN-RENT-INCREASES"), src("SFRB-LEARN-RENT-INCREASES"),
        src("SFRB-RR-PART4"),
        "\n".join(rows), other,
    )
    return page("Allowable increase rates", "allowable.html", body,
                "The single percentage that governs almost everything, plus the full "
                "published history it is drawn from.")


# --------------------------------------------------------------------------- #
# UNITS PAGE
# --------------------------------------------------------------------------- #
def build_units():
    blocks = []
    for uid in ("A", "B"):
        raw = UNITS_BY_ID[uid]
        comp = COMP_BY_ID[uid]
        mx = [s for s in comp["scenarios"] if s["key"] == "maximum_rule_4_12"][0]

        occ_rows = "".join(
            "<tr><td>{}</td><td>{}</td><td>{}</td><td class='nowrap'>{}</td></tr>".format(
                o["label"], o["role"], o["status"], fdate(o["since"]))
            for o in raw["occupants_current"])

        ann_rows = "".join(
            "<tr><td class='nowrap'>{}</td><td class='num'>{:g}%</td><td>{}</td>"
            "<td class='src'>{}</td></tr>".format(
                fdate(b["anniversary"]), b["percent"], b["rate_period"], src("SFRB-571"))
            for b in mx["banked"]) or (
            "<tr><td colspan='4' class='muted'>No banked increases yet.</td></tr>")

        scen_rows = []
        for s in comp["scenarios"]:
            if s["key"] == "maximum_24_month_reading":
                continue  # shown separately on the Flagged page
            notice = ("{} days<br><span class='small muted'>by {}</span>".format(
                s["notice_days_required"], fdate(s["serve_by_delivered"]))
                if s["notice_days_required"] else "&mdash;")
            scen_rows.append(
                "<tr><td><b>{}</b></td><td class='num'>{}</td><td class='num'>{}</td>"
                "<td class='num'>{}</td><td class='num'>{}</td><td class='num'>{}</td>"
                "<td class='nowrap'>{}</td></tr>".format(
                    s["label"], pct(s["banked_percent"]), pct(s["annual"]["percent"]),
                    pct(s["total_percent"]), money(s["increase_amount"]),
                    money(s["new_base_rent"]), notice))

        blocks.append("""
<h2>{label}</h2>
<div class="grid g4">
  <div class="kpi"><div class="k">Tenancy start</div>
    <div class="v" style="font-size:17px">{start}</div>
    <div class="s">Lease commencement</div></div>
  <div class="kpi"><div class="k">Base rent</div><div class="v">{base}</div>
    <div class="s">Unchanged since move-in</div></div>
  <div class="kpi"><div class="k">Anniversary</div>
    <div class="v" style="font-size:19px">{ann_date}</div>
    <div class="s">Once every 12 months</div></div>
  <div class="kpi"><div class="k">Next lawful date</div>
    <div class="v" style="font-size:17px">{next_d}</div>
    <div class="s">Keeps the anniversary intact</div></div>
</div>

<h3>Current occupants <span class="small muted">(anonymized)</span></h3>
<div class="tw"><table>
<thead><tr><th>Occupant</th><th>Role</th><th>Status</th><th>Since</th></tr></thead>
<tbody>{occ}</tbody></table></div>

<h3>Banked increases available &mdash; verified line by line</h3>
<div class="tw"><table>
<thead><tr><th>Anniversary skipped</th><th class="num">Rate that year</th>
<th>Rate period</th><th class="src">Source</th></tr></thead>
<tbody>{ann_rows}</tbody></table></div>
<p class="small muted">Assumes no increase has ever been served on this tenancy.
<b>Unconfirmed &mdash; see <a href="flagged.html">flagged item 3</a>.</b></p>

<h3>Scenarios at {next_d}</h3>
<div class="tw"><table>
<thead><tr><th>Scenario</th><th class="num">Banked</th><th class="num">Annual</th>
<th class="num">Total</th><th class="num">Increase</th><th class="num">New base rent</th>
<th>Notice</th></tr></thead>
<tbody>{scen}</tbody></table></div>
<p class="src">Banking rule: {rr} &middot; Notice rule: {civ} &middot; Rates: {f571}
&middot; Base rent &amp; no rounding-up: {learn}</p>
""".format(label=raw["public_label"], start=fdate(raw["tenancy_start"]),
           base=money(raw["current_base_rent"]),
           ann_date="{:02d}/{:02d}".format(raw["anniversary_month"], raw["anniversary_day"]),
           next_d=fdate(comp["next_effective_date"]), occ=occ_rows, ann_rows=ann_rows,
           scen="\n".join(scen_rows), rr=src("SFRB-RR-PART4"), civ=src("CA-CIV-827"),
           f571=src("SFRB-571"), learn=src("SFRB-LEARN-RENT-INCREASES")))

    ub = COMP_BY_ID["B"]
    ub_max = [s for s in ub["scenarios"] if s["key"] == "maximum_rule_4_12"][0]

    body = topnav() + """
<div class="note">
  <b>Anonymization</b>
  Tenant names and initials are replaced with occupant codes throughout. Dates and
  dollar amounts are unchanged, as requested. The mapping from codes to real people
  exists only in a local file that is not committed to this repository.
</div>

{blocks}

<div class="note warn">
  <b>Unit B &mdash; two numbers are deliberately blank</b>
  The Rent Board has not published the allowable increase for the period containing
  June 1, 2027, so the annual component and every total that depends on it are shown
  blank. What <i>is</i> verified is the banked component: <b>{b12}</b> under Rent Board
  Rule 4.12. Because that already exceeds 10% on its own, a 90-day notice is required if
  you take it. {rr}
</div>

<h2>Banking: the one rule that changes everything for Unit B</h2>
<div class="tw"><table>
<thead><tr><th>Question</th><th>Official answer</th><th class="src">Source</th></tr></thead>
<tbody>
<tr><td>How long before a skipped increase can be banked?</td>
  <td><b>A full 12 months</b> &mdash; Rule 4.12(a): &ldquo;A full 12 months must have
  elapsed from the date that an annual rent increase, or a portion thereof, could have
  been imposed before this banking section becomes applicable.&rdquo;</td>
  <td class="src">{rr}</td></tr>
<tr><td>Is there a limit on how much can be banked?</td>
  <td><b>No.</b> &ldquo;There is no limit on how much can be banked&rdquo; (back to
  April 1, 1982).</td><td class="src">{banked}</td></tr>
<tr><td>Do banked increases expire?</td>
  <td><b>No</b> &mdash; not during a tenancy. But they <b>do not carry over to a new
  tenant</b>.</td><td class="src">{banked}</td></tr>
<tr><td>Can I compound them?</td>
  <td><b>No.</b> &ldquo;Banked increases shall not be compounded and shall not be
  rounded up.&rdquo; Add the percentages, then apply the total to the current base
  rent.</td><td class="src">{rr}</td></tr>
<tr><td>Can I take only part of the banked amount?</td>
  <td>Yes. &ldquo;If only part of the allowable increase is used, the rest is banked.
  The remaining portion may be imposed at a later time, after at least 12 months have
  passed.&rdquo;</td><td class="src">{banked}</td></tr>
<tr><td>Does a new owner inherit them?</td>
  <td>Yes &mdash; &ldquo;New owners may use banked increases from prior owners.&rdquo;</td>
  <td class="src">{banked}</td></tr>
</tbody></table>
</div>

<h2>Unit A &mdash; the replacement occupant matters</h2>
<div class="card">
<p>Unit A's original lease had three occupants; today it has one of the originals plus a
replacement occupant. Three rules govern that, and they point in different directions:</p>
<ul class="tight">
  <li><b>You cannot charge more because someone new moved in.</b> &ldquo;A landlord
  cannot charge additional rent simply because a new (or additional) roommate has moved
  into a unit with the existing tenant. This is an unlawful rent increase, even if the
  lease or rental agreement provides for the additional charge.&rdquo; {learn}</li>
  <li><b>Costa-Hawkins does not help you here.</b> The market-rate reset under Civil
  Code &sect;1954.53(d) applies to <i>subtenants and assignees</i> who moved in after
  January 1, 1996. Per the Rent Board, &ldquo;any co-tenant who moved in after the
  original occupant is not subject to such a rent increase, regardless of when the
  co-tenant moved in.&rdquo; {t329}</li>
  <li><b>But Rules &amp; Regulations &sect;6.14 might, later.</b> &sect;6.14 allows an
  unlimited increase on remaining occupants when the <b>last original occupant
  vacates</b> &mdash; <i>but only if</i> you served each subsequent occupant a written
  &ldquo;6.14 notice&rdquo; within a reasonable time (generally 60 days) of learning
  about the occupancy. {t329}</li>
</ul>
<div class="note ok">
  <b>Action item &mdash; free, and time-sensitive</b>
  An original occupant is still in Unit A, so no &sect;6.14 or Costa-Hawkins reset is
  available today. But if you have <b>not</b> already served a written 6.14 notice on the
  replacement occupant, serve one now. If you wait until the last original occupant
  leaves, it is too late &mdash; the option is lost permanently. The Rent Board
  recommends getting legal advice before relying on &sect;6.14.
  {t329} <a href="https://www.sf.gov/documents/7737/537_6.14_Costa-Hawkins_Petition_3.25.pdf"
  target="_blank" rel="noopener">Form 537 (6.14 / Costa-Hawkins petition) &#8599;</a>
</div>
</div>
""".format(blocks="".join(blocks), b12=pct(ub_max["banked_percent"]),
           rr=src("SFRB-RR-PART4"), banked=src("SFRB-BANKED"),
           learn=src("SFRB-LEARN-RENT-INCREASES"), t329=src("SFRB-TOPIC-329"))
    return page("Unit ledgers &amp; scenarios", "units.html", body,
                "Anonymized unit-by-unit calculations. Every percentage traces back to "
                "Rent Board Form 571.")


def build_notice():
    body = topnav() + """
<h2>The statutory notice period</h2>
<div class="tw"><table>
<caption>California Civil Code &sect;827(b). The 10% test is applied to the increase
alone <i>or</i> combined with any other increase in the 12 months before it takes effect.</caption>
<thead><tr><th>Size of increase</th><th>Notice required</th><th>If mailed</th>
<th class="src">Source</th></tr></thead>
<tbody>
<tr><td>10% or less</td><td><b>30 days</b> before the effective date</td>
  <td>35 days</td><td class="src">{}</td></tr>
<tr><td>Greater than 10%</td><td><b>90 days</b> before the effective date</td>
  <td>95 days</td><td class="src">{}</td></tr>
</tbody></table></div>
<p class="small muted">Service must follow Code of Civil Procedure &sect;1162: personal
delivery, or substituted service plus mailing, or posting and mailing. The San Francisco
Rent Board's summary is the same: 30 days, 90 days if over 10%, and &ldquo;if the notice
is mailed, the landlord must give the tenant 5 more days.&rdquo; {}</p>

<h2>What the notice must contain</h2>
<div class="tw"><table>
<thead><tr><th>Required item</th><th>Why</th><th>Authority</th>
<th class="src">Source</th></tr></thead>
<tbody>
<tr><td>Dollar amount of the increase</td><td>Rent Board guidance</td>
  <td>Rent Board</td><td class="src">{}</td></tr>
<tr><td>Percentage amount of the increase</td><td>Rent Board guidance</td>
  <td>Rent Board</td><td class="src">{}</td></tr>
<tr><td>Date the increase takes effect</td><td>Rent Board guidance</td>
  <td>Rent Board</td><td class="src">{}</td></tr>
<tr><td>Which portion is the annual increase and/or the <b>banked amount</b>, if any</td>
  <td><b>Mandatory.</b> Rule 4.10(b): a notice that does not conform renders
  <i>the entire increase null and void</i>, unless the amount requested equals no more
  than the allowable annual and banked increase.</td>
  <td>Rule 4.10(a)(1)</td><td class="src">{}</td></tr>
<tr><td>The <b>dates on which the banked amount is based</b></td>
  <td>Rule 4.12(b). Failure to include it does not void the increase, but it is still
  required.</td><td>Rule 4.12(b)</td><td class="src">{}</td></tr>
<tr><td>Which portion reflects certified capital improvement / rehabilitation /
  energy conservation costs</td><td>Rule 4.10(a)(2)</td><td>Rule 4.10(a)(2)</td>
  <td class="src">{}</td></tr>
<tr><td>Which portion reflects a gas/electricity passthrough, with the charges
  <b>explained</b></td><td>Rule 4.10(a)(3)</td><td>Rule 4.10(a)(3)</td>
  <td class="src">{}</td></tr>
<tr><td>Which portion reflects RAP loan amortisation</td><td>Rule 4.10(a)(4)</td>
  <td>Rule 4.10(a)(4)</td><td class="src">{}</td></tr>
</tbody></table></div>

<h2>Do you need a reason?</h2>
<div class="card">
<p><b>For the annual allowable increase: no.</b> Nothing in the Rent Ordinance requires
a landlord to justify, explain or document a reason for taking the annual increase. It
is simply available once every 12 months. That is the whole point of the percentage.</p>
<p>What <i>does</i> require a stated, provable justification is anything above it:</p>
<div class="tw"><table>
<thead><tr><th>Mechanism</th><th>What you must show</th><th class="src">Source</th></tr></thead>
<tbody>
<tr><td>Banked increase</td><td>Which anniversaries were skipped and the published rate
  for each. No Rent Board approval needed, but the maths must be right.</td>
  <td class="src">{}</td></tr>
<tr><td>Capital improvement passthrough</td><td>Proof of cost and that the work
  prolongs the life of the building or adds substantially to its value. Requires a
  petition.</td><td class="src">{}</td></tr>
<tr><td>Operating &amp; maintenance increase</td><td>That your operating expenses rose
  faster than the annual allowable increase.</td><td class="src">{}</td></tr>
<tr><td>Utility passthrough</td><td>A completed Rent Board worksheet filed
  <b>before</b> the notice is served.</td><td class="src">{}</td></tr>
<tr><td>Bond passthrough</td><td>Completed worksheet; no petition.</td>
  <td class="src">{}</td></tr>
</tbody></table></div>
<p class="small muted">Put plainly: claiming &ldquo;my costs went up&rdquo; is not a
basis for exceeding 1.6%. The ordinance has a specific petition for that, and it has to
be approved first.</p>
</div>

<h2>Notice checklist</h2>
<div class="card">
<ul class="tight">
  <li>&#9744; Housing Inventory report submitted and license current (check the portal)</li>
  <li>&#9744; Rent Board fee paid, or a current exemption on file</li>
  <li>&#9744; At least 12 months since the last increase or since the lease began</li>
  <li>&#9744; Effective date is the anniversary date (or you accept the new anniversary)</li>
  <li>&#9744; Rate used is the one in effect on the <b>effective date</b></li>
  <li>&#9744; Calculated on base rent only; not rounded up</li>
  <li>&#9744; Banked amounts added, not compounded; each one dated</li>
  <li>&#9744; Dollar amount, percentage and effective date stated</li>
  <li>&#9744; 30 or 90 days counted correctly; +5 days if mailed</li>
  <li>&#9744; Same method applied to every unit</li>
  <li>&#9744; Proof of service retained</li>
</ul>
<p class="src">{} {} {}</p>
</div>

<div class="note warn">
  <b>Timing trap for Unit B</b>
  If you serve Unit B a 90-day notice you must already know the percentage that will be
  in effect on the effective date. The Rent Board publishes around January 1, so a
  June 1, 2027 effective date is fine &mdash; but do not serve a 90-day notice in
  December 2026 for a March 2027 date and assume last year's rate still applies.
</div>
""".format(
        src("CA-CIV-827"), src("CA-CIV-827"), src("SFRB-LEARN-RENT-INCREASES"),
        src("SFRB-LEARN-RENT-INCREASES"), src("SFRB-LEARN-RENT-INCREASES"),
        src("SFRB-LEARN-RENT-INCREASES"), src("SFRB-RR-PART4"), src("SFRB-RR-PART4"),
        src("SFRB-RR-PART4"), src("SFRB-RR-PART4"), src("SFRB-RR-PART4"),
        src("SFRB-BANKED"), src("SFRB-PETITIONS"), src("SFRB-PETITIONS"),
        src("SFRB-PETITIONS"), src("SFRB-PETITIONS"),
        src("SFRB-LEARN-RENT-INCREASES"), src("SFRB-RR-PART4"), src("CA-CIV-827"),
    )
    return page("How to notify tenants", "notice.html", body,
                "Statutory notice periods, the mandatory contents of the notice, and "
                "whether a reason is required.")


# --------------------------------------------------------------------------- #
# PASSTHROUGHS PAGE
# --------------------------------------------------------------------------- #
def build_passthroughs():
    body = topnav() + """
<div class="note">
  <b>Filing a rent increase petition costs nothing.</b>
  &ldquo;There is no charge for filing a Rent Board petition.&rdquo; In some capital
  improvement or substantial rehabilitation cases an estimator's fee may be collected.
  {}
</div>

<h2>The six increases that require a petition before you serve notice</h2>
<div class="tw"><table>
<thead><tr><th>Petition type</th><th>Topic</th><th>What it is for</th>
<th class="src">Source</th></tr></thead>
<tbody>
<tr><td>Capital Improvement Passthrough</td><td>302</td>
  <td>Roof, exterior painting, seismic retrofitting, new windows &mdash; work that
  prolongs the life of the building or adds substantially to its value. Must be
  certified before it can be passed through.</td><td class="src">{}</td></tr>
<tr><td>Operating &amp; Maintenance Expense Increase</td><td>322</td>
  <td>Increased cost of operating the property, where the increase exceeds the annual
  allowable increase. Capped at <b>7%</b>.</td><td class="src">{}</td></tr>
<tr><td>Special Circumstances &mdash; Comparable Rents</td><td>323</td>
  <td>Based on rents for comparable units.</td><td class="src">{}</td></tr>
<tr><td>Proposition I Past Rent History</td><td>324</td>
  <td>For units affected by Proposition I.</td><td class="src">{}</td></tr>
<tr><td>Utility Passthrough</td><td>325</td>
  <td>Petition <i>or</i> worksheet. Worksheets must be filed with the Rent Board before
  the notice is served.</td><td class="src">{}</td></tr>
<tr><td>Rules &amp; Regs &sect;1.21 &mdash; No Tenant in Occupancy</td><td>328</td>
  <td>Where there is no tenant in occupancy.</td><td class="src">{}</td></tr>
</tbody></table></div>

<h2>And the ones that do not</h2>
<div class="tw"><table>
<thead><tr><th>Mechanism</th><th>Rent Board filing?</th><th>Detail</th>
<th class="src">Source</th></tr></thead>
<tbody>
<tr><td>Annual allowable increase</td><td><span class="pill ok">None</span></td>
  <td>Just the license.</td><td class="src">{}</td></tr>
<tr><td>Banked increase</td><td><span class="pill ok">None</span></td>
  <td>Must be calculated correctly and itemised.</td><td class="src">{}</td></tr>
<tr><td>General obligation bond passthrough</td><td><span class="pill warn">Worksheet</span></td>
  <td>50% of recently adopted bond measures.</td><td class="src">{}</td></tr>
<tr><td>Water revenue bond passthrough</td><td><span class="pill warn">Worksheet</span></td>
  <td>Use the Rent Board worksheet.</td><td class="src">{}</td></tr>
<tr><td>Rent Board fee recovery</td><td><span class="pill ok">None</span></td>
  <td>Once the fee is paid in full you may recover <b>50% ($29.50 per dwelling unit for
  2026&ndash;27)</b> from tenants in occupancy as of November 1 of the tax year. Cannot
  be evicted for non-payment.</td><td class="src">{}</td></tr>
<tr><td>Excess water use charges</td><td><span class="pill warn">Worksheet</span></td>
  <td>Up to 50% of SF Water Department excess-use penalties, with retrofit
  certifications. Not part of base rent.</td><td class="src">{}</td></tr>
</tbody></table></div>

<div class="note warn">
  <b>Passthroughs do not become part of base rent</b>
  Capital improvement amounts, utility passthroughs and water penalties are charged
  <i>on top of</i> base rent and are excluded from it when calculating future
  percentage increases. That is set out in Rule 4.11(h) and Rule 4.13(f), and in the
  definition of base rent. Getting this wrong compounds an overcharge every year.
  {}
</div>

<h2>Capital improvement reference rates, 3/1/2026 &ndash; 2/28/2027</h2>
<div class="tw"><table>
<thead><tr><th>Amortisation period</th><th class="num">Imputed interest rate</th>
<th class="num">Factor</th><th class="src">Source</th></tr></thead>
<tbody>
<tr><td>7 year</td><td class="num">4.1%</td><td class="num">.01372</td>
  <td class="src">{}</td></tr>
<tr><td>10 year</td><td class="num">4.3%</td><td class="num">.01027</td>
  <td class="src">{}</td></tr>
<tr><td>15 year</td><td class="num">4.6%</td><td class="num">.00770</td>
  <td class="src">{}</td></tr>
<tr><td>20 year</td><td class="num">4.8%</td><td class="num">.00649</td>
  <td class="src">{}</td></tr>
</tbody></table></div>
<p class="small muted">Uncompensated labour rate for work commenced from 6/29/26:
$40.40 per hour. {}</p>
""".format(
        src("SFRB-PETITIONS"),
        src("SFRB-PETITIONS"), src("SFRB-PETITIONS"), src("SFRB-PETITIONS"),
        src("SFRB-PETITIONS"), src("SFRB-PETITIONS"), src("SFRB-PETITIONS"),
        src("SFRB-LEARN-RENT-INCREASES"), src("SFRB-BANKED"), src("SFRB-PETITIONS"),
        src("SFRB-PETITIONS"), src("SFRB-FEE"), src("SFRB-RR-PART4"),
        src("SFRB-RR-PART4"),
        src("SFRB-CURRENT-RATES"), src("SFRB-CURRENT-RATES"),
        src("SFRB-CURRENT-RATES"), src("SFRB-CURRENT-RATES"),
        src("SFRB-CURRENT-RATES"),
    )
    return page("Petitions &amp; passthroughs", "passthroughs.html", body,
                "Every lawful way to go above 1.6%, and which ones require Rent Board "
                "approval first.")


# --------------------------------------------------------------------------- #
# OWNERS PAGE
# --------------------------------------------------------------------------- #
def build_owners():
    body = topnav() + """
<div class="note ok">
  <b>The headline</b>
  San Francisco's rent-increase rules do not distinguish between a large corporate
  landlord and one person owning a two-unit building. The ordinance says
  &ldquo;landlord&rdquo; and &sect;37.15 says &ldquo;owners of residential dwelling
  units subject to this Chapter 37.&rdquo; There is no size threshold and no
  incorporation test anywhere in it.
</div>

<h2>Where the rules are genuinely identical</h2>
<div class="tw"><table>
<thead><tr><th>Requirement</th><th>Large corporate owner</th><th>Individual owner</th>
<th class="src">Source</th></tr></thead>
<tbody>
<tr><td>Annual increase ceiling</td><td>1.6% (60% of Bay Area CPI, capped at 7%)</td>
  <td>1.6% &mdash; identical</td><td class="src">{}</td></tr>
<tr><td>Housing Inventory report &amp; rent increase license</td>
  <td>Required annually by March 1</td><td>Required annually by March 1</td>
  <td class="src">{}</td></tr>
<tr><td>Rent Board fee</td><td>$59.00 per dwelling unit, 2026&ndash;27</td>
  <td>$59.00 per dwelling unit &mdash; the fee page expressly includes single-family
  homes and condos</td><td class="src">{}</td></tr>
<tr><td>30 / 90-day notice</td><td>Civil Code &sect;827</td><td>Civil Code &sect;827</td>
  <td class="src">{}</td></tr>
<tr><td>Petition-based passthroughs</td><td>Available, no filing fee</td>
  <td>Available, no filing fee</td><td class="src">{}</td></tr>
<tr><td>Fair housing / anti-discrimination</td><td>Applies</td><td>Applies &mdash;
  including the &ldquo;Mrs. Murphy&rdquo; limits, which never excuse race, colour or
  national origin discrimination</td><td class="src">{}</td></tr>
<tr><td>Algorithmic rent-setting software</td><td><b>Banned</b></td><td><b>Banned</b> &mdash;
  this is the one area where San Francisco singled out large-portfolio practice</td>
  <td class="src">{}</td></tr>
</tbody></table></div>

<h2>Where the law actually draws a line</h2>
<div class="tw"><table>
<thead><tr><th>Provision</th><th>Effect</th><th class="src">Source</th></tr></thead>
<tbody>
<tr><td>Civil Code &sect;1947.12(d)(5)(A)(ii)</td>
  <td>The AB 1482 exemption for a single-family home or condo held separately from any
  other dwelling unit is <b>not available to a corporation</b> (nor to a REIT, nor to an
  LLC in which a corporation holds membership). A natural-person owner can qualify;
  a corporate owner cannot.</td><td class="src">{}</td></tr>
<tr><td>Rent Ordinance &sect;37.10C</td>
  <td>No landlord in San Francisco may use &ldquo;revenue management software&rdquo;
  that calculates non-public competitor data to set or recommend rents. Up to $1,000 per
  violation, per month, per unit, with a tenant right of action and attorney's fees.</td>
  <td class="src">{}</td></tr>
<tr><td>Rent Ordinance &sect;37.10B</td>
  <td>Tenant harassment &mdash; bad-faith conduct to influence a tenant to vacate.
  Unlawful rent increases are a recurring fact pattern in these claims.</td>
  <td class="src">{}</td></tr>
</tbody></table></div>

<h2>Practice differences &mdash; not from an official source</h2>
<div class="note warn">
  <b>Everything in this section is observation, not verified fact.</b>
  No official source was found that documents how differently-sized owners behave. It is
  recorded here because you asked, and flagged because it cannot be cited.
</div>
<div class="tw"><table>
<thead><tr><th>Observation</th><th>Status</th></tr></thead>
<tbody>
<tr><td>Institutional owners tend to impose the annual increase every single year on the
  anniversary date, so little or nothing ever accumulates as banked increases.</td>
  <td><span class="pill warn">Unverified</span></td></tr>
<tr><td>Institutional owners are more likely to file capital improvement and O&amp;M
  petitions, because the filing is free and they have the records to document costs.</td>
  <td><span class="pill warn">Unverified</span></td></tr>
<tr><td>Smaller individual owners more often skip years, then face a large banked
  increase later &mdash; which is exactly the situation Unit B is in.</td>
  <td><span class="pill warn">Unverified</span></td></tr>
</tbody></table></div>
<p class="small muted">What <i>is</i> verifiable is the mechanism each group uses, and
it is the same mechanism: the annual allowable increase, banked increases, and approved
petitions. There is no separate &ldquo;corporate&rdquo; rent increase in San Francisco
law. {}</p>
""".format(
        src("SF-ORD-373"), src("SF-ORD-3715"), src("SFRB-FEE"), src("CA-CIV-827"),
        src("SFRB-PETITIONS"), src("HUD-FHA"), src("SF-ORD-3710C"),
        src("CA-CIV-1947-12"), src("SF-ORD-3710C"), src("SF-ORD-3710B"),
        src("SFRB-PETITIONS"),
    )
    return page("Corporate vs. individual owners", "owners.html", body,
                "The rules are the same. Here is the one place the statute actually "
                "treats them differently.")


# --------------------------------------------------------------------------- #
# FAIR HOUSING PAGE
# --------------------------------------------------------------------------- #
def build_fair_housing():
    body = topnav() + """
<div class="note ok">
  <b>Short answer to &ldquo;one unit or both?&rdquo;</b>
  Raise both, using the <b>same method</b>, on each unit's own anniversary date. Not
  because uniformity is legally required &mdash; it isn't &mdash; but because a
  documented, uniformly-applied formula is the single best answer to any later claim
  that the difference in treatment was discriminatory.
</div>

<h2>What the law actually prohibits</h2>
<div class="card">
<p><b>Federal &mdash; Fair Housing Act.</b> Seven protected classes: race, colour,
national origin, religion, sex, familial status, disability. {}</p>
<p><b>California &mdash; FEHA.</b> Broader. The state list includes race, colour,
ancestry, national origin, <b>citizenship, immigration status, primary language</b>,
religion, disability, sex and gender, sexual orientation, gender identity and expression,
genetic information, marital status, familial status, <b>source of income</b> (including
a Section 8 voucher), military or veteran status, and <b>age</b>. It also protects
against retaliation, and protects people associated with someone in a protected class.
{}</p>
<p class="small muted">Note what is <i>not</i> on either list: being a long-standing
tenant, being on good or bad terms with the owner, or having a low rent. Raising one
tenant's rent more because they have lived there longer is not, by itself,
discrimination &mdash; but it is precisely the pattern a tenant lawyer will look at
first.</p>
</div>

<h2>One unit vs. both &mdash; the analysis</h2>
<div class="tw"><table>
<thead><tr><th>Option</th><th>Lawful?</th><th>Risk profile</th><th>Assessment</th></tr></thead>
<tbody>
<tr><td><b>Raise both, same method, each on its own anniversary</b></td>
  <td><span class="pill ok">Yes</span></td>
  <td>Lowest</td>
  <td><b>Recommended.</b> The difference between Unit A (3.0%) and Unit B is fully
  explained by objective facts: different anniversary dates, different base rents,
  different banking history. That is a defence, not a liability.</td></tr>
<tr><td><b>Raise one unit only</b></td>
  <td><span class="pill ok">Yes</span></td>
  <td>Low to moderate</td>
  <td>Lawful if the reason is objective and documented &mdash; e.g. the other unit's
  anniversary has not arrived yet, or you are choosing to leave its increases banked.
  The risk is not the act; it is an unexplained pattern.</td></tr>
<tr><td><b>Raise one unit to the maximum and leave the other untouched</b></td>
  <td><span class="pill warn">Lawful, but</span></td>
  <td>Highest</td>
  <td>This is the pattern most likely to draw scrutiny. A 13&ndash;15% jump on one
  household while the other gets nothing invites both a discrimination complaint and a
  Rent Board petition.</td></tr>
<tr><td><b>Raise a unit shortly after the tenant complained, requested repairs, or
  exercised a right</b></td>
  <td><span class="pill bad">High risk</span></td>
  <td>Highest</td>
  <td>Retaliation is itself unlawful under California law, independent of whether the
  increase amount is correct.</td></tr>
</tbody></table></div>
<p class="src">{} {}</p>

<h2>Why &ldquo;identical&rdquo; is not the right target</h2>
<div class="card">
<p>Unit A and Unit B <b>cannot</b> receive identical increases, and trying to force that
would itself be arbitrary. They have different anniversary dates (February 1 and
June 1), different base rents, and different banking histories. A 3.0% increase for Unit
A and a different percentage for Unit B is not unequal treatment &mdash; it is the same
rule applied to different facts.</p>
<p>What matters for defensibility is that the <b>rule</b> is identical:</p>
<ul class="tight">
  <li>same source for the percentage (the Rent Board's published rate);</li>
  <li>same timing rule (the anniversary date, never earlier);</li>
  <li>same treatment of banked increases (the same policy applied to both);</li>
  <li>same notice period and same notice content;</li>
  <li>a written record of the calculation for each unit, kept on file.</li>
</ul>
<p class="small muted">If you depart from your own rule for one household, write down
the objective reason at the time. Contemporaneous notes are worth far more than a
reconstruction two years later.</p>
</div>

<h2>The scrutiny test you asked for</h2>
<div class="card">
<p>You asked that any increase be able to survive review by a San Francisco tenant
lawyer and be recognisable as normal business practice. Applying that test to the
recommended plan:</p>
<div class="tw"><table>
<thead><tr><th>Test</th><th>Unit A &mdash; 3.0% on Feb 1, 2027</th>
<th>Unit B &mdash; current annual only on Jun 1, 2027</th></tr></thead>
<tbody>
<tr><td>Is it within the published cap?</td>
  <td><span class="pill ok">Yes</span> 1.6% annual + 1.4% banked</td>
  <td><span class="pill ok">Yes</span> the published rate, nothing more</td></tr>
<tr><td>Is the banking valid?</td>
  <td><span class="pill ok">Yes</span> 24 months elapsed &mdash; clears even the
  stricter reading</td>
  <td><span class="pill ok">Yes</span> nothing banked is being taken</td></tr>
<tr><td>Is the notice period right?</td>
  <td><span class="pill ok">Yes</span> 30 days, well under 10%</td>
  <td><span class="pill ok">Yes</span> 30 days</td></tr>
<tr><td>Is the notice content complete?</td>
  <td><span class="pill ok">Yes</span> if the banked portion and its dates are stated</td>
  <td><span class="pill ok">Yes</span> no banked component to disclose</td></tr>
<tr><td>Would it look like normal practice?</td>
  <td><span class="pill ok">Yes</span> a routine, modest annual adjustment</td>
  <td><span class="pill ok">Yes</span> the most conservative option available</td></tr>
<tr><td>Does it correlate with a protected characteristic?</td>
  <td><span class="pill ok">No</span> derived solely from dates and published rates</td>
  <td><span class="pill ok">No</span> same</td></tr>
<tr><td>Any harassment or retaliation exposure?</td>
  <td><span class="pill ok">No</span></td><td><span class="pill ok">No</span></td></tr>
</tbody></table></div>
<p class="small muted">The recommended plan leaves Unit B's verified banked increases
untouched and available for a future year. Taking them all at once is lawful but
maximises both the tenant-relations cost and the legal surface area. {} {}</p>
</div>

<div class="note bad">
  <b>The statutory test a tenant lawyer would actually reach for</b>
  Rent Ordinance &sect;37.10B(a)(5) makes it harassment to &ldquo;influence or attempt to
  influence a tenant to vacate a rental housing unit through fraud, intimidation or
  coercion&rdquo; &mdash; including &ldquo;by means of a rent increase that is imposed
  with an intent to defraud, intimidate, or coerce the tenant into vacating.&rdquo; The
  ordinance then spells out what counts as evidence of bad faith:
  &ldquo;(1) the rent increase was substantially in excess of market rates for comparable
  units; (2) the rent increase was within six months after an attempt to recover
  possession of the unit; and (3) such other factors as a court or the Rent Board may
  deem relevant.&rdquo; {}
  <br><br>Remedies are not symbolic: treble actual damages or $1,000 in statutory
  damages &mdash; <b>whichever is greater</b> &mdash; plus reasonable attorney's fees
  and costs to a prevailing plaintiff. {}
  <br><br>Measured against that test, a 3.0% anniversary increase on Unit A is nowhere
  near &ldquo;substantially in excess of market rates,&rdquo; and neither unit's
  increase follows an attempt to recover possession. That is the difference between an
  increase that survives scrutiny and one that does not.
</div>

<div class="note bad">
  <b>One exposure worth naming</b>
  Unit A's tenancy changed composition during the term. If any increase, deposit change
  or fee coincided with, or followed, a request from an occupant relating to a
  disability, a reasonable accommodation, or a protected characteristic, the timing
  alone can carry a retaliation claim regardless of the amount. California law protects
  against retaliation for exercising fair housing rights. {}
</div>
""".format(
        src("HUD-FHA"), src("CRD-HOUSING"), src("CRD-HOUSING"), src("HUD-FHA"),
        src("SFRB-BANKED"), src("SF-ORD-3710B"),
        src("SF-ORD-3710B"), src("SF-ORD-3710B"),
        src("CRD-HOUSING"),
    )
    return page("Discrimination risk: one unit or both?", "fair-housing.html", body,
                "Whether to raise one unit or both, and what a tenant lawyer would "
                "actually look at.")


# --------------------------------------------------------------------------- #
# LAWS PAGE
# --------------------------------------------------------------------------- #
def build_laws():
    body = topnav() + """
<h2>Three tiers, one binding number</h2>
<div class="tw"><table>
<thead><tr><th>Tier</th><th>Instrument</th><th>What it does to your rent increase</th>
<th>Applies here?</th><th class="src">Source</th></tr></thead>
<tbody>
<tr><td rowspan="5"><b>Local</b><br><span class="small muted">San Francisco</span></td>
  <td>Rent Ordinance &sect;37.3(a)(1)</td>
  <td>Annual increase capped at 60% of Bay Area CPI change, never more than 7%.
  Currently <b>1.6%</b>.</td>
  <td><span class="pill ok">Yes &mdash; binding</span></td>
  <td class="src">{}</td></tr>
<tr><td>Rent Ordinance &sect;37.3(a)(2)</td>
  <td>Banking of skipped annual increases.</td>
  <td><span class="pill ok">Yes</span></td><td class="src">{}</td></tr>
<tr><td>Rent Ordinance &sect;37.15</td>
  <td>Housing Inventory reporting and the license to impose rent increases.</td>
  <td><span class="pill ok">Yes</span></td><td class="src">{}</td></tr>
<tr><td>Rent Board Rules &amp; Regs &sect;&sect;4.10, 4.12</td>
  <td>Notice content; the 12-month banking test; no compounding.</td>
  <td><span class="pill ok">Yes</span></td><td class="src">{}</td></tr>
<tr><td>Rent Ordinance &sect;37.10B</td>
  <td>Tenant harassment &mdash; bad-faith conduct.</td>
  <td><span class="pill ok">Yes</span></td><td class="src">{}</td></tr>

<tr><td rowspan="4"><b>State</b><br><span class="small muted">California</span></td>
  <td>Civil Code &sect;827(b)</td>
  <td>30 days' notice if the increase is 10% or less; 90 days if greater.</td>
  <td><span class="pill ok">Yes &mdash; binding</span></td>
  <td class="src">{}</td></tr>
<tr><td>Civil Code &sect;1947.12 (AB 1482)</td>
  <td>Statewide cap of 5% + CPI, max 10%. For San Francisco the current figure is
  <b>8.8%</b> (5% + 3.8% CPI, Aug 1, 2026 &ndash; Jul 31, 2027).
  <b>&sect;1947.12(d)(3) exempts housing already under a lower local cap</b>, so it does
  not apply to these units. Also: no more than two increments in any 12-month period.</td>
  <td><span class="pill info">Exempt</span></td><td class="src">{} {}</td></tr>
<tr><td>Civil Code &sect;1954.53 (Costa-Hawkins)</td>
  <td>Vacancy decontrol; the &sect;(d) market-rate reset for subtenants and assignees.
  The single-family / condo exemption can remove rent control entirely.</td>
  <td><span class="pill warn">Only if the property is an SFR or condo</span></td>
  <td class="src">{}</td></tr>
<tr><td>FEHA (Gov. Code &sect;12900 et seq.)</td>
  <td>Bans discriminatory and retaliatory housing practices; broader protected
  characteristics than federal law.</td>
  <td><span class="pill ok">Yes</span></td><td class="src">{}</td></tr>

<tr><td rowspan="2"><b>Federal</b><br><span class="small muted">United States</span></td>
  <td>Fair Housing Act (42 U.S.C. &sect;&sect;3601&ndash;3619)</td>
  <td>No rent ceiling. Bans increases motivated by race, colour, national origin,
  religion, sex, familial status or disability.</td>
  <td><span class="pill ok">Yes</span></td><td class="src">{}</td></tr>
<tr><td>General</td>
  <td>There is no federal rent control for private residential property and no federal
  cap on rent increases.</td><td><span class="pill info">No cap</span></td>
  <td class="src">{}</td></tr>
</tbody></table></div>

<div class="note">
  <b>Why 1.6% and not 8.8%</b>
  AB 1482's cap is 5% plus regional inflation, capped at 10%. For San Francisco,
  Aug 1, 2026 &ndash; Jul 31, 2027, that works out to <b>8.8%</b> (5% + 3.8% CPI).
  None of it applies here: Civil Code &sect;1947.12(d)(3) exempts &ldquo;housing subject
  to rent or price control through a public entity's valid exercise of its police power
  &hellip; that restricts annual increases in the rental rate to an amount less than that
  provided in subdivision (a).&rdquo; The Rent Board says the same thing in plain
  language: &ldquo;This does NOT apply for units under the rent increase limitations of
  the San Francisco Rent Ordinance.&rdquo; 1.6% is less than 8.8%, so 1.6% is the only
  number that matters. {} {}
</div>
""".format(
        src("SF-ORD-373"), src("SF-ORD-373"), src("SF-ORD-3715"),
        src("SFRB-RR-PART4"), src("SF-ORD-3710B"),
        src("CA-CIV-827"), src("CA-CIV-1947-12"), src("SFRB-AB1482"),
        src("CA-CIV-1954-53"),
        src("CRD-HOUSING"), src("HUD-FHA"), src("HUD-FHA"),
        src("CA-CIV-1947-12"), src("SFRB-AB1482"),
    )
    return page("Federal / state / local law", "laws.html", body,
                "Which layer governs, and the one state provision that does not apply "
                "here and why.")


# --------------------------------------------------------------------------- #
# FLAGGED PAGE
# --------------------------------------------------------------------------- #
def build_flagged():
    ub = COMP_BY_ID["B"]
    ub_max = [s for s in ub["scenarios"] if s["key"] == "maximum_rule_4_12"][0]
    ub_24 = [s for s in ub["scenarios"] if s["key"] == "maximum_24_month_reading"][0]
    ua = COMP_BY_ID["A"]
    ua_max = [s for s in ua["scenarios"] if s["key"] == "maximum_rule_4_12"][0]
    ua_24 = [s for s in ua["scenarios"] if s["key"] == "maximum_24_month_reading"][0]

    body = topnav() + """
<div class="note warn">
  <b>What this page is</b>
  Anything that could not be confirmed against an official source, or where two official
  sources disagree. These items are published rather than hidden. None of them blocks
  using the rest of the dashboard &mdash; but items 1 and 2 should be resolved before
  any notice is served.
</div>

<h2>1. Banking window &mdash; two official sources disagree</h2>
<div class="card">
<div class="tw"><table>
<thead><tr><th>Source</th><th>Says</th><th>Effect on Unit B</th></tr></thead>
<tbody>
<tr><td>Rent Board <b>Rule 4.12(a)</b> (the regulation itself)</td>
  <td>&ldquo;A full 12 months must have elapsed from the date that an annual rent
  increase, or a portion thereof, could have been imposed before this banking section
  becomes applicable.&rdquo;</td>
  <td>Banked = <b>{b12}</b></td></tr>
<tr><td>sf.gov <b>&ldquo;Banked rent increases&rdquo;</b> information page</td>
  <td>&ldquo;A skipped increase is only banked if at least 24 full months pass without
  any rent increase.&rdquo;</td>
  <td>Banked = <b>{b24}</b></td></tr>
<tr><td>Rent Board's own <b>worked examples</b> on &ldquo;Learn about rent
  increases&rdquo;</td>
  <td>Two separate examples bank an increase after only 12 months have elapsed.</td>
  <td>Consistent with Rule 4.12</td></tr>
</tbody></table></div>
<p><b>How this dashboard handles it.</b> The calculation engine uses Rule 4.12 (the
regulation, and the reading consistent with the Rent Board's own worked examples). But
the difference is real money: {b12} vs {b24} on a ${base:,.0f} base rent. Before
serving any large banked increase on Unit B, confirm the treatment with a Rent Board
counselor, or file a petition for a determination.</p>
<p class="src">{} {} {}</p>
<p class="small muted">Note that Unit A is unaffected in practice: its one skipped
increase is 24 months old by February 1, 2027, so it qualifies under <b>both</b>
readings. {}</p>
</div>

<h2>2. Property type not verified</h2>
<div class="card">
<p>The building dates from 1940, which clears the June 13, 1979 cutoff. But that test is
necessary, not sufficient. If either unit is a <b>single-family home or a
condominium</b>, Costa-Hawkins removes the rent-increase limits entirely for tenancies
that commenced on or after January 1, 1996 &mdash; which both of these did (2025 and
2019). The units would keep just-cause eviction protection and would still owe the Rent
Board fee, but the 1.6% cap would not apply.</p>
<p>Two exceptions that would keep you covered: a single-family dwelling with a legal
<i>or illegal</i> in-law unit is a two-unit building and is not exempt; and a
single-family dwelling is not exempt if there is another residential structure on the
same lot.</p>
<p><b>Action:</b> confirm on the
<a href="https://sfplanninggis.org/PIM/" target="_blank" rel="noopener">SF Property
Information Map</a>, or ask a Rent Board counselor.</p>
<p class="src">{} {}</p>
</div>

<h2>3. No rent-increase history supplied</h2>
<div class="card">
<p>Every banked figure on this site assumes <b>no increase has ever been served</b> on
either tenancy. That was not confirmed. If any notice was served and cannot be proved,
treat it as not served.</p>
<div class="tw"><table>
<thead><tr><th>Unit</th><th>Banked assumed</th><th>If even one year was increased</th></tr></thead>
<tbody>
<tr><td>Unit A</td><td>1.4% (one skipped year)</td>
  <td>Reduce by that year's rate; Unit A has only one skipped year so the exposure is
  small.</td></tr>
<tr><td>Unit B</td><td>{b12} (seven skipped years)</td>
  <td>Reduce by the rate for each year an increase was actually imposed. The oldest
  years carry the largest rates (3.6% in 2023, 2.3% in 2022).</td></tr>
</tbody></table></div>
<p class="src">{}</p>
</div>

<h2>4. Does fee delinquency suspend the license?</h2>
<div class="card">
<p>The Rent Board's pages tie the rent increase <b>license</b> to Housing Inventory
reporting (&sect;37.15(e)). None of the official pages reviewed state whether being
delinquent on the <b>Rent Board fee</b> also suspends the license. They are described as
separate obligations with separate deadlines, and the Rent Board warns that
&ldquo;requesting a Rent Board Fee exemption does not satisfy Rent Board Housing
Inventory reporting requirements&rdquo; &mdash; which is the reverse direction.</p>
<p><b>Action:</b> pay the fee on time. Do not test the question.</p>
<p class="src">{} {} {}</p>
</div>

<h2>5. Rent Board worked example applies an inconsistent rate</h2>
<div class="card">
<p>On sf.gov's &ldquo;Learn about rent increases&rdquo; page, the worked example titled
<i>&ldquo;Rent increase for multiple years with new anniversary date&rdquo;</i> applies
<b>1.6%</b> to an increase effective <b>May 1, 2026</b>. The same page instructs
landlords to &ldquo;use the percentage that will be in effect on the date of the
increase,&rdquo; and 1.6% only took effect on March 1, 2026 &mdash; a May 1, 2026
effective date sits in the 1.4% period. The page's other examples follow the stated rule
correctly.</p>
<p><b>Impact on you: none.</b> Both of your units' effective dates are exactly on their
anniversary dates, where the two readings agree. Noted for completeness and because it is
the kind of thing to raise with a counselor if you ever move an anniversary date.</p>
<p class="src">{} {}</p>
</div>

<h2>6. Unverified observations</h2>
<div class="tw"><table>
<thead><tr><th>Claim</th><th>Why it is not verified</th></tr></thead>
<tbody>
<tr><td>Practice differences between institutional and small individual owners (skipping
  years, filing petitions more often)</td>
  <td>No official source found that documents owner behaviour by portfolio size. Listed
  on the <a href="owners.html">owners page</a> and marked unverified there.</td></tr>
<tr><td>Unit B's annual increase for the period containing June 1, 2027</td>
  <td>Not yet published. Expected on or about January 1, 2027. Shown blank everywhere
  rather than estimated.</td></tr>
</tbody></table></div>
""".format(
        # item 1
        src("SFRB-RR-PART4"), src("SFRB-BANKED"), src("SFRB-LEARN-RENT-INCREASES"),
        src("SFRB-571"),
        # item 2
        src("SFRB-COSTA-HAWKINS-SFR"), src("SFRB-RENTAL-LAWS"),
        # item 3
        src("SFRB-BANKED"),
        # item 4
        src("SFRB-HOUSING-INVENTORY"), src("SFRB-FEE"), src("SFRB-2027-NOTICE"),
        # item 5
        src("SFRB-LEARN-RENT-INCREASES"), src("SFRB-571"),
        b12=pct(ub_max["banked_percent"]), b24=pct(ub_24["banked_percent"]),
        base=ub["current_base_rent"])
    return page("Flagged for review", "flagged.html", body,
                "Unverified values and conflicts between official sources. Published "
                "rather than hidden.")


# --------------------------------------------------------------------------- #
# SOURCES PAGE
# --------------------------------------------------------------------------- #
def build_sources():
    rows = []
    for key, s in SOURCES.items():
        rows.append(
            "<tr><td><code>{}</code></td><td><a href='{}' target='_blank' "
            "rel='noopener'>{}</a><br><span class='small muted'>{}</span></td>"
            "<td class='small'>{}</td></tr>".format(
                key, s["url"], s["title"], s["publisher"], s["supports"]))
    body = topnav() + """
<p>Every table row on this site links back to one of the sources below. All are
government pages: San Francisco Rent Board / sf.gov, California Legislative Information,
HUD, or the California Civil Rights Department. No secondary commentary, law-firm blogs
or AI summaries were used to produce any figure.</p>

<div class="tw"><table>
<thead><tr><th>ID</th><th>Source</th><th>What it supports</th></tr></thead>
<tbody>{}</tbody></table></div>

<h2>Verification method</h2>
<div class="card">
<ul class="tight">
  <li>Every percentage was transcribed from the official Form 571 PDF and then
  cross-checked against the Rent Board's &ldquo;Current Rates&rdquo; page.</li>
  <li>The calculator (<code>tools/calc.py</code>) runs {} automated self-tests on every
  build, reproducing the Rent Board's own published worked examples. All {} pass.
  <a href="https://github.com/kanlerxz87-cyber/RentincreaseSF5/blob/main/tools/calc.py"
  target="_blank" rel="noopener">View the tests &#8599;</a></li>
  <li>Dates are computed with real calendar arithmetic, not estimates.</li>
  <li>Where the Rent Board has not published a figure, the field is rendered blank and
  routed to the <a href="flagged.html">Flagged for review</a> page.</li>
</ul>
</div>

<h2>Not legal advice</h2>
<p>This is research compiled from public government sources. The San Francisco Rent Board
offers free counseling at <b>415-252-4600</b>, weekdays 9am&ndash;12pm and
1&ndash;4pm, and the Rent Board's own guidance recommends speaking with a counselor when
a unit is hard to classify. {}</p>
""".format("\n".join(rows), COMPUTED["self_tests_total"], COMPUTED["self_tests_passed"],
           src("SFRB-RENTAL-LAWS"))
    return page("Source registry", "sources.html", body,
                "Every official source used, and what each one supports.")


# --------------------------------------------------------------------------- #
def main():
    os.makedirs(DOCS, exist_ok=True)
    os.makedirs(os.path.join(DOCS, "assets"), exist_ok=True)
    with open(os.path.join(DOCS, "assets", "style.css"), "w") as f:
        f.write(CSS)

    pages = [
        ("index.html", build_index()),
        ("license.html", build_license()),
        ("steps.html", build_steps()),
        ("allowable.html", build_allowable()),
        ("units.html", build_units()),
        ("notice.html", build_notice()),
        ("passthroughs.html", build_passthroughs()),
        ("owners.html", build_owners()),
        ("fair-housing.html", build_fair_housing()),
        ("laws.html", build_laws()),
        ("flagged.html", build_flagged()),
        ("sources.html", build_sources()),
    ]
    for name, content in pages:
        p = write(DOCS, name, content)
        print("wrote {} ({} bytes)".format(os.path.relpath(p, ROOT), len(content)))


if __name__ == "__main__":
    main()
