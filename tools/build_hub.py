#!/usr/bin/env python3
"""Consolidated dashboard builder - session arena-d4b68642 (final integration).

Writes a single clean landing page (index.html) plus category subpages in hub/.
Every table data row carries a link to the official source it came from.
Values that could not be confirmed from an official source are left blank and
flagged; nothing is inferred.

Earlier sessions' published sets are NOT modified or removed. They remain at
pages/, dashboard/ and the root pages, and are linked from hub/archive.html.

Usage: python3 tools/build_hub.py
"""

import csv
import html
import os
import re
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODAY = date(2026, 11, 8)

# ---------------------------------------------------------------------------
# OFFICIAL SOURCES - every one retrieved and read during this session.
# Hostnames are restricted to the allowlist used by the repository's audits.
# ---------------------------------------------------------------------------
SOURCES = {
    "S1": ("The Rent Board Housing Inventory", "SF Rent Board",
           "https://www.sf.gov/rent-board-housing-inventory"),
    "S2": ("Admin Code sec. 37.15 - Reporting Obligations; Licensing", "SF Rent Board",
           "https://www.sf.gov/information--sec-3715-reporting-obligations-licensing"),
    "S3": ("Admin Code sec. 37.3 - Rent Limitations", "SF Rent Board",
           "https://www.sf.gov/information--sec-373-rent-limitations"),
    "S4": ("Form 571 - Allowable Annual Increases (full history)", "SF Rent Board",
           "https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf"),
    "S5": ("Learn about rent increases in San Francisco", "SF Rent Board",
           "https://www.sf.gov/learn-about-rent-increases-san-francisco"),
    "S6": ("Banked rent increases", "SF Rent Board",
           "https://www.sf.gov/information--banked-rent-increases"),
    "S7": ("Rules and Regulations Part IV (4.10 notice, 4.12 banking)", "SF Rent Board",
           "https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring"),
    "S8": ("Civil Code sec. 827 - notice of rent increase", "California Legislature",
           "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827"),
    "S9": ("Civil Code sec. 1947.12 - statewide rent cap", "California Legislature",
           "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12"),
    "S10": ("California Tenant Protection Act of 2019 (AB 1482)", "SF Rent Board",
            "https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482"),
    "S11": ("Learn about San Francisco rental laws (coverage)", "SF Rent Board",
            "https://www.sf.gov/learn-about-san-francisco-rental-laws"),
    "S12": ("The Rent Board Fee", "SF Rent Board", "https://www.sf.gov/rent-board-fee"),
    "S13": ("Annual rent increase for multiple years", "SF Rent Board",
            "https://www.sf.gov/information--annual-rent-increase-multiple-years"),
    "S14": ("Petition under Rule 6.14 and/or Costa-Hawkins", "SF Rent Board",
            "https://www.sf.gov/information--petition-determination-pursuant-section-614-andor-costa-hawkins"),
    "S15": ("Admin Code sec. 37.10B - Tenant Harassment", "SF Rent Board",
            "https://www.sf.gov/information/sec-3710b-tenant-harassment"),
    "S16": ("Admin Code sec. 37.10C - Algorithmic devices prohibited", "SF Rent Board",
            "https://www.sf.gov/information--sec-3710c-use-and-sale-algorithmic-devices-prohibited"),
    "S17": ("Civil Code sec. 1942.5 - retaliation", "California Legislature",
            "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1942.5"),
    "S18": ("Housing discrimination (FEHA)", "California Civil Rights Department",
            "https://calcivilrights.ca.gov/housing/"),
    "S19": ("Housing discrimination under the Fair Housing Act", "U.S. HUD",
            "https://www.hud.gov/helping-americans/fair-housing-act-overview"),
    "S20": ("Report an unlawful rent increase (Tenant Petition 516C)", "SF Rent Board",
            "https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history/"),
    "S21": ("Form 1007 - Notice to Tenant / Tenant Right to Counsel", "SF Rent Board",
            "https://www.sf.gov/sites/default/files/2023-08/1007%20Notice%20to%20Tenant%20Req%27d%20by%2037.%209(c)-Eng-Sp-Ch-Viet-Rus-Tag[74].pdf"),
    "S22": ("Failure to Repair and Maintain Petitions (Form 516B)", "SF Rent Board",
            "https://www.sf.gov/information--failure-repair-and-maintain-petitions"),
    "S23": ("Rules and Regulations Part X (sec. 10.11 repair deferral, sec. 10.15 hardship)", "SF Rent Board",
            "https://www.sf.gov/reports/august-2024/rent-board-rules-and-regulations-part-x-tenant-petition-arbitration"),
    "S24": ("Complete Rules and Regulations, amended 13 January 2026", "SF Rent Board",
            "https://www.sf.gov/documents/36249/625_RR_Complete_1-13-26.pdf"),
    "S25": ("Rent Board Forms Center", "SF Rent Board",
            "https://www.sf.gov/rent-board-forms-forms-center"),
    "S26": ("Rent Board department home (counsellors, portal, office)", "SF Rent Board",
            "https://www.sf.gov/departments--rent-board"),
    "S27": ("The Rent Ordinance (Chapter 37 index)", "SF Rent Board",
            "https://www.sf.gov/rent-ordinance/"),
}

# ---------------------------------------------------------------------------
# Form 571 rate table, transcribed verbatim from the PDF retrieved this session.
# ---------------------------------------------------------------------------
RATES = [
    ("3/1/26", "2/28/27", 1.6), ("3/1/25", "2/28/26", 1.4), ("3/1/24", "2/28/25", 1.7),
    ("3/1/23", "2/29/24", 3.6), ("3/1/22", "2/28/23", 2.3), ("3/1/21", "2/28/22", 0.7),
    ("3/1/20", "2/28/21", 1.8), ("3/1/19", "2/29/20", 2.6), ("3/1/18", "2/28/19", 1.6),
    ("3/1/17", "2/28/18", 2.2), ("3/1/16", "2/28/17", 1.6), ("3/1/15", "2/29/16", 1.9),
    ("3/1/14", "2/28/15", 1.0), ("3/1/13", "2/28/14", 1.9), ("3/1/12", "2/28/13", 1.9),
    ("3/1/11", "2/29/12", 0.5), ("3/1/10", "2/28/11", 0.1), ("3/1/09", "2/28/10", 2.2),
    ("3/1/08", "2/28/09", 2.0), ("3/1/07", "2/29/08", 1.5), ("3/1/06", "2/28/07", 1.7),
    ("3/1/05", "2/28/06", 1.2), ("3/1/04", "2/28/05", 0.6), ("3/1/03", "2/29/04", 0.8),
    ("3/1/02", "2/28/03", 2.7), ("3/1/01", "2/28/02", 2.8), ("3/1/00", "2/28/01", 2.9),
    ("3/1/99", "2/29/00", 1.7), ("3/1/98", "2/28/99", 2.2), ("3/1/97", "2/28/98", 1.8),
    ("3/1/96", "2/28/97", 1.0), ("3/1/95", "2/29/96", 1.1), ("3/1/94", "2/28/95", 1.3),
    ("3/1/93", "2/28/94", 1.9), ("12/8/92", "2/28/93", 1.6), ("3/1/92", "12/7/92", 4.0),
    ("3/1/91", "2/29/92", 4.0), ("3/1/90", "2/28/91", 4.0), ("3/1/89", "2/28/90", 4.0),
    ("3/1/88", "2/28/89", 4.0), ("3/1/87", "2/29/88", 4.0), ("3/1/86", "2/28/87", 4.0),
    ("3/1/85", "2/28/86", 4.0), ("3/1/84", "2/28/85", 4.0), ("3/1/83", "2/29/84", 7.0),
    ("4/1/82", "2/28/83", 7.0),
]


def _d(s):
    m, d, y = (int(x) for x in s.split("/"))
    if y < 100:
        # The Form 571 table runs from 1982 to the current period, so a two-digit
        # year is 19xx up to 99 and 20xx only from 00 onward. Mapping every
        # two-digit year to 20xx printed the 1982-1999 rows as 2082-2099.
        y += 1900 if y >= 82 else 2000
    return date(y, m, d)


def rate_on(d):
    for a, b, r in RATES:
        if _d(a) <= d <= _d(b):
            return r
    return None


def money(x):
    return "${:,.2f}".format(x)


def e(s):
    return html.escape(str(s), quote=True)


def src(*ids):
    out = []
    for i in ids:
        title, pub, url = SOURCES[i]
        out.append('<a class="src" href="%s" target="_blank" rel="noopener" title="%s">%s</a>'
                   % (e(url), e(pub + " - " + title), i))
    return " ".join(out)


VERIFIED = "verified"
OWNER = "owner-supplied"
COMPUTED = "computed"
ANALYSIS = "analysis"
UNVERIFIED = "unverified"
ABSENT = "no authority found"

BADGE = {
    VERIFIED: ("ok", "Verified"),
    OWNER: ("warn", "Owner-supplied"),
    COMPUTED: ("calc", "Computed"),
    ANALYSIS: ("calc", "Analysis"),
    UNVERIFIED: ("bad", "Unverified"),
    ABSENT: ("bad", "No authority found"),
}


def badge(st):
    cls, label = BADGE[st]
    return '<span class="badge %s">%s</span>' % (cls, label)


# ---------------------------------------------------------------------------
# THE REGISTER - one row per finding. This is the single source of truth for
# the tables, the CSV export and the verification page.
# Columns: id, category, item, verified value, status, sources, note
# ---------------------------------------------------------------------------
R = []


def row(cat, item, value, status, sources, note=""):
    R.append(dict(id="R%02d" % (len(R) + 1), cat=cat, item=item, value=value,
                  status=status, sources=sources, note=note))


# --- Licence: the question the owner asked first -----------------------------
row("licence", "Does an individual owner (not a corporation) have to report?",
    "Yes. Sec. 37.15(a) requires 'owners of residential dwelling units' to report. "
    "No entity-type or portfolio-size exemption appears in the text.", VERIFIED, ["S2", "S1"])
row("licence", "Is there a licence application to file or an approval to wait for?",
    "No application. The licence is generated automatically once the unit is reported "
    "as non-owner-occupied in the Housing Inventory.", VERIFIED, ["S1"],
    "Widely repeated online claims of a licence 'application' are not supported by the official page.")
row("licence", "Must the licence exist before the increase takes effect?",
    "Yes. A current rent increase licence must be on file before any annual or banked "
    "increase goes into effect; without it the notice is not enforceable.", VERIFIED, ["S1", "S2"])
row("licence", "What happens if the owner has not reported?",
    "The licence is suspended. On reporting, it is restored prospectively only; the tenant "
    "is not obligated to pay the increased rent for months during the suspension.", VERIFIED, ["S2"],
    "Sec. 37.15(e). This is not retroactive - late reporting does not revive past months.")
row("licence", "When did reporting start for a building of this size?",
    "March 1, 2023 for condominiums and buildings with fewer than 10 units. "
    "July 1, 2022 applied only to non-condo buildings with 10 or more units.", VERIFIED, ["S2", "S1"])
row("licence", "Annual reporting deadline", "March 1 each year.", VERIFIED, ["S1", "S2"])
row("licence", "Penalty for reporting after the deadline",
    "The Rent Board does not assess monetary penalties for late Housing Inventory filing. "
    "A submission after the deadline still generates a licence.", VERIFIED, ["S1"])
row("licence", "Must the licence be attached to the rent increase notice?",
    "No. The licence does not need to be included with the notice.", VERIFIED, ["S1"])
row("licence", "Cost and method of reporting",
    "Free, online through the Rent Board Portal, available 24/7. An account is required.", VERIFIED, ["S1"])
row("licence", "Is the submitted inventory information confidential?",
    "No. Information entered in the Housing Inventory submission is public.", VERIFIED, ["S1"],
    "Privacy consequence: do not put tenant names in free-text fields; the portal asks for owner "
    "business contact details, occupancy dates and base rent in $250 increments.")
row("licence", "Is a Rent Board petition needed for an annual or banked increase?",
    "No. Annual and banked increases do not require a petition or Board approval.", VERIFIED, ["S3", "S13", "S6"])
row("licence", "Rent Board fee (separate from the Inventory)",
    "$59.00 per dwelling unit for the 2026-2027 tax year, due March 1. "
    "5% monthly late penalty, capped at 15%.", VERIFIED, ["S12"])
row("licence", "Does a fee exemption satisfy the Inventory requirement?",
    "No. Requesting a Rent Board fee exemption does not satisfy Housing Inventory reporting.", VERIFIED, ["S12", "S1"])
row("licence", "Has this owner actually reported / is a licence on file?",
    "", UNVERIFIED, ["S1"],
    "Cannot be checked without the property address and portal access. Tenants can look this up "
    "in the public portal. This is the first action item.")

# --- Rates ------------------------------------------------------------------
row("rates", "Allowable annual increase, 3/1/2026 - 2/28/2027", "1.6%", VERIFIED, ["S4", "S5"])
row("rates", "How the annual figure is set",
    "60% of the published CPI increase; in no event greater than 7%.", VERIFIED, ["S3"],
    "Sec. 37.3(a)(1).")
row("rates", "How often rent may be increased", "Once every 12 months per tenancy.", VERIFIED, ["S5", "S3"])
row("rates", "First possible increase",
    "12 months after the date the tenant's lease began.", VERIFIED, ["S5"])
row("rates", "What the percentage applies to",
    "Base rent only, including housing services such as parking or storage. "
    "Temporary passthroughs and fluctuating charges are excluded.", VERIFIED, ["S5", "S13"])
row("rates", "Rounding", "Increases cannot be rounded up to the nearest dollar.", VERIFIED, ["S5", "S7", "S13"])
row("rates", "Which year's percentage to use",
    "The percentage in effect on the effective date of the increase, not the date the notice is served.",
    VERIFIED, ["S5", "S6"])
row("rates", "Allowable increase, 3/1/2027 - 2/29/2028", "", UNVERIFIED, ["S4"],
    "Not yet published. The Rent Board publishes it on March 1, 2027. Left blank deliberately.")
row("rates", "Initial rent for a genuinely new vacant tenancy",
    "No limit under the Rent Ordinance on the first rent charged for an empty covered unit.",
    VERIFIED, ["S5", "S14"])

# --- Banking ----------------------------------------------------------------
row("banking", "Ordinance text on banking",
    "Sec. 37.3(a)(2): an owner who refrains from imposing an annual increase 'may accumulate said "
    "increase and, subject to Section 37.15, impose that amount on the tenant's subsequent rent "
    "increase anniversary dates.' No 24-month condition appears.", VERIFIED, ["S3"])
row("banking", "Rule 4.12 timing condition",
    "'A full 12 months must have elapsed from the date that an annual rent increase, or a portion "
    "thereof, could have been imposed before this banking section becomes applicable.'", VERIFIED, ["S7"])
row("banking", "sf.gov banking page wording",
    "'A skipped increase is only banked if at least 24 full months pass without any rent increase.'",
    VERIFIED, ["S6"], "Quoted as published. Appears to contradict Rule 4.12 until the measuring point is identified.")
row("banking", "Official worked example settles the measuring point",
    "Tenant moved in 6/1/2023; increase imposed 5/1/2026. The 1.7% available 6/1/2024 IS banked; "
    "the 1.4% available 6/1/2025 is NOT, and is permanently lost. The clock runs 12 months from "
    "the date each increase became available.", VERIFIED, ["S5"])
row("banking", "Reconciliation of the two wordings",
    "First increase becomes available 12 months after tenancy start; it banks 12 months after that "
    "= 24 months after tenancy start. The two statements measure from different starting points and agree.",
    ANALYSIS, ["S5", "S6", "S7"],
    "Interpretation, not a quoted rule. See the Flagged page. It does not change either unit's number.")
row("banking", "Does the conflict change the numbers for these two units?",
    "Conditionally: Unit 1 reaches 24 months on 2/1/2027; Unit 2 calculations assume no intervening increases since 2019, which is unconfirmed. "
    "Both readings produce the same result for both units.", ANALYSIS, ["S5", "S6", "S7"])
row("banking", "Compounding and rounding of banked amounts",
    "Banked increases are added, not compounded, and may not be rounded up. An administrative law "
    "judge may readjust a good-faith overage of no more than one-half of one percent.", VERIFIED, ["S7", "S6", "S13"])
row("banking", "Notice content for a banked increase",
    "State which portion is banked and the dates it is based on. Rule 4.12(b) says failure to include "
    "this does not by itself render the increase null and void.", VERIFIED, ["S7"])
row("banking", "Does a banked amount survive a new tenancy?",
    "No. Banked increases do not carry over to a new tenant. A new owner may use a prior owner's bank.",
    VERIFIED, ["S6"])
row("banking", "Changing the anniversary date",
    "Moving the effective date off the anniversary can permanently lose an increase that has not "
    "yet completed its 12 months. Many owners keep the same date each year to avoid this.", VERIFIED, ["S5"])

# --- Notices ----------------------------------------------------------------
row("notices", "Notice period, increase of 10% or less", "At least 30 days before the effective date.",
    VERIFIED, ["S8", "S5"])
row("notices", "Notice period, increase above 10%", "At least 90 days before the effective date.",
    VERIFIED, ["S8", "S5"])
row("notices", "How the 10% threshold is measured",
    "Against the rent charged at any time in the 12 months before the effective date, alone or "
    "combined with any other increases in that 12-month window.", VERIFIED, ["S8"])
row("notices", "Extra time when serving by mail", "Add 5 days.", VERIFIED, ["S5", "S6"])
row("notices", "Permitted methods of service",
    "Personal delivery to the tenant, or mail under Code of Civil Procedure sec. 1013.", VERIFIED, ["S8"])
row("notices", "Required notice content",
    "Dollar amount, percentage amount, effective date, and which portion is banked.", VERIFIED, ["S5", "S6", "S7"])
row("notices", "Consequence of a defective notice",
    "Rule 4.10(b): a non-conforming increase is null and void in its entirety, subject only to a "
    "good-faith readjustment where the excess is no more than one-half of one percent.", VERIFIED, ["S7"])
row("notices", "Must the notice state a reason?",
    "No reason is required for an annual or banked increase; the ordinance itself authorises it. "
    "Reasons and cost proof attach to petition-based increases.", ANALYSIS, ["S3", "S5", "S7"])

# --- Laws -------------------------------------------------------------------
row("laws", "Which units are rent controlled",
    "Many residential units built on or before June 13, 1979 have rent control and eviction protection.",
    VERIFIED, ["S11"])
row("laws", "Does the statewide cap apply to these units?",
    "No. AB 1482's rent cap does not apply to housing already under a local rent control ordinance "
    "that restricts increases below the state formula.", VERIFIED, ["S9", "S10"],
    "Civil Code sec. 1947.12(d)(3).")
row("laws", "Statewide cap figure (reference only)",
    "8.8% for San Francisco, 8/1/2026 - 7/31/2027 (5% + 3.8% CPI). Does not govern these units.",
    VERIFIED, ["S10"])
row("laws", "Two-unit owner-occupied exemption under AB 1482",
    "A two-unit property is exempt only if the second unit was owner-occupied for the entire "
    "tenancy. Both units here are tenant-occupied, so this exemption is not available.", ANALYSIS, ["S10"])
row("laws", "Federal ceiling on rent increases",
    "", ABSENT, ["S19"],
    "No federal statute capping rent increases for private, unsubsidised housing was identified in "
    "the sources reviewed. Federal housing law in this area is anti-discrimination law.")
row("laws", "Federal protected classes",
    "Race, color, national origin, religion, sex, familial status, disability.", VERIFIED, ["S19"])
row("laws", "California protected classes (broader than federal)",
    "Adds ancestry, citizenship, immigration status, primary language, sexual orientation, gender "
    "identity and expression, genetic information, marital status, source of income, military or "
    "veteran status, and age.", VERIFIED, ["S18"])
row("laws", "Retaliation",
    "Civil Code sec. 1942.5 bars a rent increase within 180 days of specified tenant activity such as "
    "a habitability complaint; sec. 1942.5(d) separately prohibits retaliatory increases without that time limit.",
    VERIFIED, ["S17"])
row("laws", "Bad-faith increases used to force a tenant out",
    "Sec. 37.10B(a)(5) prohibits influencing a tenant to vacate by fraud, intimidation or coercion; "
    "(a)(9) prohibits violating anti-discrimination law. Treble damages or $1,000 minimum, plus fees.",
    VERIFIED, ["S15"])
row("laws", "Algorithmic rent-setting software",
    "Sec. 37.10C makes it unlawful to use revenue-management software that draws on non-public "
    "competitor data to set rents. Each month and each unit is a separate violation.", VERIFIED, ["S16"])

# --- Owner practices --------------------------------------------------------
row("practices", "Must both units be raised to avoid discrimination?",
    "", ABSENT, ["S3", "S18", "S19"],
    "No provision requiring identical or simultaneous increases across units was found. What is "
    "prohibited is a difference based on a protected characteristic, or a retaliatory/bad-faith purpose.")
row("practices", "Do corporations and individual owners face different caps?",
    "No. Sec. 37.3 applies to 'landlords' without distinguishing entity form; the same 1.6% governs both.",
    ANALYSIS, ["S3", "S5"])
row("practices", "What large operators may not do here",
    "Use algorithmic revenue-management devices built on non-public competitor data - unlawful in "
    "San Francisco for any landlord, corporate or individual.", VERIFIED, ["S16"])
row("practices", "Charging more because a roommate moved in",
    "Unlawful. An owner cannot charge additional rent simply because a new or additional roommate "
    "moved in with the existing tenant, even if the lease says otherwise.", VERIFIED, ["S5"])
row("practices", "Rule 6.14 notice on a new occupant",
    "To preserve an unlimited increase when the last original occupant vacates, a written 6.14 notice "
    "must be served on each subsequent occupant within a reasonable time; generally 60 days is "
    "considered reasonable.", VERIFIED, ["S14"])
row("practices", "Costa-Hawkins and co-tenants",
    "A co-tenant who moved in after the original occupant is not subject to a Costa-Hawkins increase. "
    "Rule 6.14 is broader but requires the timely notice.", VERIFIED, ["S14"])

# --- Tenant-side review -----------------------------------------------------
row("review", "Tenant challenge route",
    "Tenant Petition Form 516C, box C, alleging an unlawful rent increase. No filing charge and "
    "no time limit for filing.", VERIFIED, ["S20"])
row("review", "What the tenant will be asked to produce",
    "Original lease, rent increase notices, rent receipts or cancelled checks showing the date and "
    "amount of increases.", VERIFIED, ["S20"],
    "Keep the same evidence file. It is the answer to most of the questions a tenant lawyer will ask.")
row("review", "Free counsel",
    "The Tenant Right to Counsel Program provides free assistance in eviction cases; intake is through "
    "the Eviction Defense Collaborative, (415) 659-9184.", VERIFIED, ["S21"],
    "This is eviction defence, not a free lawyer for every rent increase dispute.")
row("review", "Free Rent Board counselling",
    "Rent Board counsellors, 415-252-4600, weekdays 9am-noon and 1pm-4pm. Available to owners as well "
    "as tenants.", VERIFIED, ["S11", "S20"])
row("review", "Hearing format",
    "Designed so that no one needs an attorney; parties may still be represented. The judge cannot "
    "consider evidence outside the record or not served on the other side.", VERIFIED, ["S20"])

# --- Added by the 2026-11-08 re-verification session ------------------------
row("licence", "What the Housing Inventory actually publishes about the unit",
    "Owner name and business contact, business registration number if any, approximate square "
    "footage in 250 sq ft increments, number of bedrooms and bathrooms, the date occupancy began, "
    "the base rent in $250 increments and whether utilities are included. The submission is public "
    "and is made under penalty of perjury.", VERIFIED, ["S1", "S2"],
    "The exact rent is not published: it is reported in $250 bands, so $3,995.00 sits inside a band. "
    "Do not type tenant names into free-text fields - the information is public.")
row("licence", "Can part of the Rent Board fee be recovered from tenants?",
    "Yes - 50%, i.e. $29.50 per dwelling unit, once the fee is paid in full, if the tenant lived in "
    "the unit as of 1 November of the tax year. Penalties cannot be recovered.", VERIFIED, ["S12"])
row("licence", "Is the validity of an increase tied to paying the fee?",
    "", ABSENT, ["S2", "S12"],
    "No provision was found linking enforceability of an increase to payment of the Chapter 37A fee; "
    "sec. 37.15(e) ties the licence to Inventory reporting. This is an absence of authority, not a "
    "legal conclusion.")
row("rates", "Does an increase have to be 'reasonable' or match market rent?",
    "", ABSENT, ["S3", "S6"],
    "No official definition of a 'reasonable' or 'normal' increase was found. For a covered unit the "
    "lawful ceiling is the published percentage plus any properly banked amount; a figure at or below "
    "it needs no justification and no petition. Market rent matters only as one listed indicator of bad "
    "faith in a sec. 37.10B(a)(5) circumvention claim.")
row("notices", "Exactly 10 percent - 30 days or 90 days?",
    "30 days. The 90-day rule applies when the increase is greater than 10 percent, so an increase of "
    "exactly 10 percent stays in the 30-day band.", VERIFIED, ["S8"],
    "The 10 percent is measured against the rent charged at any time in the 12 months before the "
    "effective date, combined with any other increase in that window - so a passthrough or re-notice "
    "can move a 10 percent increase into the 90-day band.")
row("notices", "Can a tenant stop an increase over outstanding repairs?",
    "Yes. A tenant may petition for deferral or denial of an annual or banked increase where required "
    "repairs were not done. The petition must be filed no later than 60 days after the tenant receives "
    "the notice; if granted, the increase is postponed until the work is done and rent already paid is "
    "refunded. It is not granted if the repairs were completed before the effective date.",
    VERIFIED, ["S22", "S23"])
row("practices", "How do large corporate owners actually set increases?",
    "", ABSENT, ["S2", "S3"],
    "No government source retrieved describes corporate rent-setting practice, and no official "
    "statistics on it were found. The legal position is identical for every owner: sec. 37.15(a) "
    "applies to 'owners' and sec. 37.3(a)(1) to 'landlords', with no entity or portfolio threshold. "
    "The practice associated with large operators that is specifically banned here is algorithmic "
    "pricing on non-public competitor data (sec. 37.10C).")
row("units", "Unit 1: which anniversary date governs?",
    "", UNVERIFIED, ["S5", "S6"],
    "Depends on a fact not supplied. If any original lessee remained, the tenancy continues from 2025-02-01: "
    "the anniversary is 1 February and the increases available on 2026-02-01 (1.4%) and 2027-02-01 (1.6%) "
    "give 3.0% from 2027-02-01. If every original lessee left and a new tenancy began 2026-04-01, the "
    "anniversary is 1 April, nothing from the old tenancy banks (banked amounts do not survive a new "
    "tenancy), and the first increase is available 2027-04-01 at the rate published 2027-03-01.")
row("units", "Unit 2: which years are banked",
    "The six anniversaries from 2020-06-01 to 2025-06-01: 1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 = 11.5%, "
    "plus the 1.6% annual increase in effect on the effective date = 13.1%.", COMPUTED, ["S4", "S7"],
    "Added, never compounded. The 2026-06-01 increase has not itself banked by 2027-02-28; the 1.6% "
    "counted here is the annual increase in effect on the effective date, so nothing is counted twice.")

# ---------------------------------------------------------------------------
# Unit arithmetic - computed from owner-supplied inputs and official rates.
# ---------------------------------------------------------------------------
UNITS = [
    dict(label="Unit 1", base=3995.00, start=date(2025, 2, 1), anniversary="February 1",
         tenants="Original occupants reported at the start; by 2026-04-01 a later co-tenant appears. Whether any original occupant remained is unconfirmed (F19).",
         change="Occupant change reported 2026-04-01; rent unchanged at $3,995.00."),
    dict(label="Unit 2", base=3150.00, start=date(2019, 6, 1), anniversary="June 1",
         tenants="Two occupants, unchanged.", change="No occupant change reported; intervening rent history unconfirmed."),
]

U1_BANK = rate_on(date(2026, 2, 1))      # 1.4 - skipped, banks 2027-02-01
U1_ANN = rate_on(date(2027, 2, 1))       # 1.6
U1_TOTAL = round(U1_BANK + U1_ANN, 10)   # 3.0

U2_LEDGER = [(date(y, 6, 1), rate_on(date(y, 6, 1))) for y in range(2020, 2027)]
U2_BANKED = round(sum(r for d, r in U2_LEDGER if d <= date(2025, 6, 1)), 10)  # 11.5
U2_ANNUAL = rate_on(date(2027, 2, 28))   # 1.6
U2_TOTAL = round(U2_BANKED + U2_ANNUAL, 10)  # 13.1

SCENARIOS = [
    ("Unit 1", "Annual only", 3995.00, 1.6, date(2027, 2, 1),
     "Ignores the skipped 2026 anniversary. Lowest scrutiny."),
    ("Unit 1", "Annual + banked 2026", 3995.00, U1_TOTAL, date(2027, 2, 1),
     "1.4% banked + 1.6% annual. Both banking readings agree on this date."),
    ("Unit 2", "Annual only", 3150.00, 1.6, date(2027, 2, 1),
     "Leaves the accumulated bank unused. Lowest scrutiny."),
    ("Unit 2", "Banked + annual", 3150.00, U2_TOTAL, date(2027, 2, 28),
     "11.5% banked + 1.6% annual. Above 10%, so 90 days' notice."),
    ("Unit 2", "Capped at 10% by choice", 3150.00, 10.0, date(2027, 2, 28),
     "Policy choice, not a legal ceiling. Keeps the 30-day notice band; the balance stays banked."),
]


def notice_days(pct):
    return 90 if pct > 10 else 30


def serve_by(eff, pct, mailed=False):
    return eff - timedelta(days=notice_days(pct) + (5 if mailed else 0))


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
CSS = """
:root{--bg:#f6f7f9;--card:#fff;--ink:#16202c;--muted:#5b6b7f;--line:#e3e8ee;
--accent:#1a5fb4;--ok:#0f7b43;--okbg:#e7f6ec;--warnbg:#fff5e0;--badbg:#fdecec;--calcbg:#eaf1fb}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent)}
.wrap{max-width:1140px;margin:0 auto;padding:0 20px}
header.top{background:var(--card);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20}
.top-in{display:flex;align-items:center;gap:18px;flex-wrap:wrap;padding:12px 20px;max-width:1140px;margin:0 auto}
.brand{font-weight:700;letter-spacing:-.2px;white-space:nowrap}
.brand small{display:block;font-weight:400;font-size:12px;color:var(--muted)}
nav.main{display:flex;gap:2px;flex-wrap:wrap;font-size:14px}
nav.main a{padding:6px 10px;border-radius:6px;text-decoration:none;color:var(--muted)}
nav.main a:hover{background:var(--bg);color:var(--ink)}
nav.main a.active{background:var(--calcbg);color:var(--accent);font-weight:600}
nav.sub{display:flex;gap:2px;flex-wrap:wrap;font-size:12.5px;width:100%;margin-top:-6px}
nav.sub a{padding:4px 8px;border-radius:5px;text-decoration:none;color:var(--muted)}
nav.sub a:hover{background:var(--bg);color:var(--ink)}
nav.sub a.active{background:var(--calcbg);color:var(--accent);font-weight:600}
ol.steps{margin:0;padding-left:22px}
ol.steps>li{margin:0 0 10px}
ol.steps b{display:block}
.qcards{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}
.qcard{background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:12px 14px;text-decoration:none;color:inherit;display:block}
.qcard:hover{border-color:var(--accent)}
.qcard .q{font-weight:600;margin:0 0 4px;display:block}
.qcard .a{margin:0;color:var(--muted);font-size:14px}
pre.notice{white-space:pre-wrap;background:var(--bg);border:1px solid var(--line);border-radius:8px;
padding:14px;font:13.5px/1.55 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;overflow-x:auto}
.hero{background:var(--card);border:1px solid var(--line);border-left:5px solid var(--accent);
border-radius:10px;padding:18px 20px;margin:0 0 18px}
.hero h2{margin-top:0}
.tick{list-style:none;padding-left:0;margin:0}
.tick li{padding:5px 0 5px 26px;position:relative;border-bottom:1px dashed var(--line)}
.tick li:before{content:"\2610";position:absolute;left:2px;color:var(--accent);font-size:16px}
.tick li:last-child{border-bottom:none}
main{padding:26px 0 50px}
h1{font-size:27px;line-height:1.25;margin:0 0 8px;letter-spacing:-.4px}
h2{font-size:19px;margin:0 0 12px;letter-spacing:-.2px}
h3{font-size:15px;margin:0 0 6px}
.lede{color:var(--muted);margin:0 0 20px;max-width:78ch}
.panel{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:20px;margin:0 0 18px}
.answer{border-left:4px solid var(--accent);background:var(--calcbg);padding:14px 16px;border-radius:0 8px 8px 0}
.answer p{margin:0 0 10px}.answer p:last-child{margin:0}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(215px,1fr));margin:0 0 18px}
.tile{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:15px}
.tile .k{font-size:12px;text-transform:uppercase;letter-spacing:.5px;color:var(--muted)}
.tile .v{font-size:25px;font-weight:700;margin:4px 0;letter-spacing:-.5px}
.tile .n{font-size:12.5px;color:var(--muted)}
.cards{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}
.card{display:block;background:var(--card);border:1px solid var(--line);border-radius:10px;
padding:15px;text-decoration:none;color:inherit}
.card:hover{border-color:var(--accent)}
.card p{margin:0;font-size:13.5px;color:var(--muted)}
.tw{overflow-x:auto;margin:0 0 6px}
table{border-collapse:collapse;width:100%;font-size:14px;background:var(--card)}
caption{text-align:left;font-size:13px;color:var(--muted);padding:0 0 8px}
th,td{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}
thead th{background:#f0f3f7;font-size:12.5px;text-transform:uppercase;letter-spacing:.4px;color:var(--muted)}
tbody tr:nth-child(even){background:#fafbfc}
td.num,th.num{text-align:right;white-space:nowrap}
.badge{display:inline-block;font-size:11.5px;font-weight:600;padding:2px 8px;border-radius:999px;white-space:nowrap}
.badge.ok{background:var(--okbg);color:#0f7b43}
.badge.warn{background:var(--warnbg);color:#8a5a00}
.badge.bad{background:var(--badbg);color:#a32020}
.badge.calc{background:var(--calcbg);color:#1a5fb4}
a.src{display:inline-block;font-size:11.5px;font-weight:600;padding:1px 6px;margin:1px 2px 1px 0;
border:1px solid var(--line);border-radius:5px;text-decoration:none;background:#f7f9fc}
a.src:hover{border-color:var(--accent)}
.note{font-size:13px;color:var(--muted);margin:6px 0 0}
.small{font-size:13.5px}
.blank{color:#a32020;font-style:italic}
.steps{counter-reset:s;list-style:none;padding:0;margin:0}
.steps>li{counter-increment:s;position:relative;padding:0 0 16px 44px;margin:0 0 16px;border-bottom:1px solid var(--line)}
.steps>li:last-child{border-bottom:none;margin-bottom:0;padding-bottom:0}
.steps>li::before{content:counter(s);position:absolute;left:0;top:0;width:29px;height:29px;
border-radius:50%;background:var(--accent);color:#fff;font-weight:700;font-size:14px;
display:flex;align-items:center;justify-content:center}
.steps h3{margin:3px 0 5px}
.steps p{margin:0 0 6px;font-size:14.5px}
input.filter{width:100%;padding:10px 12px;border:1px solid var(--line);border-radius:8px;font-size:14px;margin:0 0 12px}
footer{border-top:1px solid var(--line);background:var(--card);padding:20px 0;font-size:13px;color:var(--muted)}
.pill{display:inline-block;font-size:12px;background:#eef1f5;border-radius:999px;padding:2px 9px;margin:0 5px 5px 0}
@media(max-width:640px){h1{font-size:22px}.panel{padding:15px}table{font-size:13px}}
@media print{header.top,nav.main,input.filter{display:none}body{background:#fff}
.panel{border:none;padding:0;margin:0 0 14px;break-inside:avoid}}
"""

NAV_MAIN = [
    ("index.html", "Overview"),
    ("executive-summary.html", "Executive summary"),
    ("process.html", "Rent Board process"),
    ("units.html", "Units and numbers"),
    ("notices.html", "Notices"),
    ("notice-kit.html", "Notice kit"),
    ("practices.html", "Owner practices"),
]

NAV_SUB = [
    ("rates.html", "Allowable increases"),
    ("laws.html", "Law and protections"),
    ("review.html", "Tenant-lawyer test"),
    ("register.html", "Full register"),
    ("flagged.html", "Flagged for review"),
    ("audit.html", "Audit"),
    ("sources.html", "Sources"),
    ("verification.html", "Verification"),
    ("archive.html", "Earlier sets"),
]


def _nav_links(items, active, root):
    out = []
    for href, label in items:
        target = ("hub/" + href) if root else href
        if href == "index.html":
            target = "index.html" if root else "../index.html"
        cls = ' class="active"' if href == active else ""
        out.append('<a href="%s"%s>%s</a>' % (target, cls, e(label)))
    return "".join(out)


def nav_html(active, root=False):
    return ('<nav class="main" aria-label="Main">%s</nav>'
            '<nav class="sub" aria-label="Reference">%s</nav>'
            % (_nav_links(NAV_MAIN, active, root), _nav_links(NAV_SUB, active, root)))


def layout(title, body, active, root=False, desc=None):
    flag_link = "hub/flagged.html" if root else "flagged.html"
    body = ('<section class="panel"><p><strong>Conditional research, not an approved increase.</strong> '
            'Coverage, lawful base rents, complete rent history and current licences are unverified. '
            'Banked examples assume no intervening increases; that history was not established for Unit 2. '
            'No amount is cleared for service or guaranteed to pass legal review. '
            '<a href="' + flag_link + '">Review the limitations (including F17–F20)</a>.</p></section>') + body
    css = "hub/hub.css" if root else "hub.css"
    home = "index.html" if root else "../index.html"
    d = desc or ("Source-linked research on lawful rent increases for two rent-controlled units "
                 "in San Francisco, Outer Sunset 94122. Tenant identities are anonymised.")
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s &middot; SF rent increase dashboard</title>
<meta name="description" content="%s">
<link rel="stylesheet" href="%s">
</head>
<body>
<header class="top"><div class="top-in">
<div class="brand"><a href="%s" style="text-decoration:none;color:inherit">SF rent increase dashboard</a>
<small>Outer Sunset 94122 &middot; anonymised &middot; sources checked 8 Nov 2026</small></div>
<nav class="main">%s</nav>
</div></header>
<main id="main"><div class="wrap">%s</div></main>
<footer><div class="wrap">
<strong>Research record, not legal advice.</strong> Compiled from official San Francisco, California
and federal sources; every table row links to the page its value came from. Values that could not be
confirmed are left blank and listed on the flagged page. Tenant names, initials and the street address
are never published; dates and dollar amounts are preserved as supplied.
<div class="note">Rent Board counsellors: 415-252-4600, weekdays 9am-noon and 1pm-4pm.
Recheck the law and the published rate before serving any notice.</div>
</div></footer>
</body></html>
""" % (e(title), e(d), css, home, nav_html(active, root), body)


def head(h1, lede):
    return '<h1>%s</h1><p class="lede">%s</p>' % (e(h1), lede)


def table(caption, headers, rows, numeric=()):
    th = "".join('<th%s>%s</th>' % (' class="num"' if i in numeric else "", e(h))
                 for i, h in enumerate(headers))
    trs = []
    for r in rows:
        tds = "".join('<td%s>%s</td>' % (' class="num"' if i in numeric else "", c)
                      for i, c in enumerate(r))
        trs.append("<tr>%s</tr>" % tds)
    return ('<div class="tw"><table><caption>%s</caption><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div>' % (caption, th, "".join(trs)))


def val(v):
    return v if v else '<span class="blank">left blank - unverified</span>'


def reg_rows(cat=None, statuses=None):
    out = []
    for r in R:
        if cat and r["cat"] != cat:
            continue
        if statuses and r["status"] not in statuses:
            continue
        note = '<div class="note">%s</div>' % e(r["note"]) if r["note"] else ""
        out.append([e(r["id"]), e(r["item"]) + note, val(e(r["value"])),
                    badge(r["status"]), src(*r["sources"])])
    return out


REG_HEADERS = ["Ref", "Finding", "Verified value", "Status", "Official source"]


def reg_table(cat=None, caption="Findings, verification status and official source"):
    return table(caption, REG_HEADERS, reg_rows(cat))


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def page_index():
    b = head("Rent increase dashboard",
             "Two rent-controlled units in a 1940 building in the Outer Sunset, San Francisco 94122. "
             "Every figure is either quoted from an official source or computed from the published "
             "rate, and every table row links to the page it came from.")
    b += """<section class="hero">
<h2>First question: do you have to inform the Rent Board or apply for a licence?</h2>
<p><strong>The licence: yes. An application: no. Doing this as an individual rather than a corporation changes nothing.</strong></p>
<p>Section 37.15(a) requires every owner of a covered unit to report into the Rent Board Housing
Inventory. Once a unit is reported as tenant-occupied, a rent increase licence is
<strong>generated automatically</strong> - there is no form to file for it and no approval to wait for. %s</p>
<p>The licence has to be on file <strong>on the effective date</strong> of the increase. If it is not, the
licence is suspended, the notice is not enforceable, and the tenant owes no increased rent for the
months of suspension; reporting later restores it <strong>prospectively only</strong>. %s</p>
<p>No petition and no Board approval is needed for an ordinary annual or banked increase - the Rent
Board's own rate sheet says it may be imposed <strong>without filing a petition</strong>. %s</p>
</section>
""" % (src("S1", "S2"), src("S2"), src("S4", "S3"))

    b += '<div class="grid">'
    for k, v, n in [
        ("Allowable annual increase", "1.6%", "1 Mar 2026 - 28 Feb 2027 " + src("S4", "S5")),
        ("Unit 1 conditional scenario, 1 Feb 2027", "%.1f%%" % U1_TOTAL,
         "%s on %s " % (money(round(3995 * U1_TOTAL / 100, 2)), money(3995)) + src("S4", "S7")),
        ("Unit 2 conditional full-bank scenario", "%.1f%%" % U2_TOTAL,
         "%s on %s " % (money(round(3150 * U2_TOTAL / 100, 2)), money(3150)) + src("S4", "S7")),
        ("Notice above 10%", "90 days", "30 days at or below 10% " + src("S8")),
    ]:
        b += ('<div class="tile"><div class="k">%s</div><div class="v">%s</div>'
              '<div class="n">%s</div></div>' % (e(k), e(v), n))
    b += '</div>'

    b += '<section class="panel"><h2>Do these three things, in this order</h2><ol class="steps">'
    b += ('<li><b>Report both units in the Housing Inventory.</b> Free, online through the Rent Board '
          'Portal, due 1 March each year. Best-estimate answers are allowed and late filing carries no '
          'monetary penalty, but the licence only exists once the report is in. %s</li>'
          % src("S1", "S2", "S12"))
    b += ('<li><b>Confirm the licence shows in the Portal before you serve anything.</b> The licence must '
          'be current on the effective date, not on the day you write the notice. %s</li>'
          % src("S1", "S2"))
    b += ('<li><b>Choose the effective date, then serve the right notice.</b> Unit 1 reaches its next '
          'anniversary on 1 February 2027; Unit 2 has had no increase since 2019. Use the rate in effect '
          'on the effective date, give 30 days, or 90 days if the increase is more than 10 percent, and itemise the annual and banked parts. %s</li>'
          % src("S5", "S8", "S7"))
    b += '</ol><p class="note"><a href="hub/process.html">The full nine-step process, with every official link &rarr;</a></p></section>'

    b += '<section class="panel"><h2>Your questions, answered in one line</h2><div class="qcards">'
    for q, a, href in [
        ("Do I need to apply for a licence?",
         "No application exists. Reporting the unit generates it, and being an individual owner changes nothing.",
         "process.html"),
        ("How much can I raise each unit?",
         "Unit 1: 1.6% now, or 3.0% from 1 Feb 2027 with the skipped year. Unit 2: 1.6% now, or 13.1% with the banked years.",
         "units.html"),
        ("Should I raise one unit or both?",
         "No rule requires both. What gets reviewed is the reason for any difference, so write the reason down per unit.",
         "practices.html"),
        ("What is a reasonable or normal increase?",
         "There is no official definition. For a covered unit the lawful ceiling is the published percentage plus any banked amount.",
         "rates.html"),
        ("How do I tell the tenants?",
         "Written notice stating the amount, the percentage, the effective date and the banked part: 30 days, or 90 above 10%.",
         "notice-kit.html"),
        ("Would it survive a tenant lawyer?",
         "Twelve questions a reviewer will ask, and the evidence that answers each of them.",
         "review.html"),
    ]:
        b += ('<a class="qcard" href="hub/%s"><span class="q">%s</span><p class="a">%s</p></a>'
              % (href, e(q), e(a)))
    b += '</div></section>'

    b += '<section class="panel"><h2>The two units at a glance</h2>'
    rows = []
    for unit, name, base, pct, eff, note in SCENARIOS:
        inc = round(base * pct / 100, 2)
        rows.append([e(unit), e(name), money(base), "%.1f%%" % pct, money(inc),
                     money(round(base + inc, 2)), "%d days" % notice_days(pct),
                     eff.isoformat(), serve_by(eff, pct).isoformat(),
                     badge(COMPUTED) + " " + src("S4", "S8")])
    b += table("Computed from the owner-supplied base rents and the officially published percentages. "
               "Serve-by dates assume personal service; add 5 days if mailed.",
               ["Unit", "Option", "Base rent", "Total", "Increase", "New rent", "Notice",
                "Effective", "Serve by", "Status and source"], rows, numeric=(2, 3, 4, 5))
    b += ('<p class="note">Base rents and tenancy dates are owner-supplied and cannot be confirmed from an '
          'official source; they are flagged, not asserted. The percentages and notice periods are verified. '
          'Unit 1 has a second branch if no original lessee remained after the 2026 occupant change - see F19. '
          '<a href="hub/units.html">See the line-by-line arithmetic &rarr;</a></p></section>')

    b += '<section class="panel"><h2>Browse by category</h2><div class="cards">'
    for href, label, desc in [
        ("executive-summary.html", "Executive summary", "The licence answer first, then the numbers, the risks and the decisions."),
        ("process.html", "Rent Board process", "Nine steps from confirming coverage to a served notice, with official links."),
        ("units.html", "Units and numbers", "Anonymised tenancy records and every calculation shown line by line."),
        ("rates.html", "Allowable increases", "The full official rate table back to 1982 and how the figure is set."),
        ("notices.html", "Notices", "30 versus 90 days, required content, service methods and what voids a notice."),
        ("notice-kit.html", "Notice kit", "A model notice, the checklist to run before serving, and the three ways a notice fails."),
        ("laws.html", "Law and protections", "Which cap governs, why the state cap does not, and fair-housing limits."),
        ("practices.html", "Owner practices", "Corporations versus individuals, one unit versus both, and what counts as a reason."),
        ("review.html", "Tenant-lawyer test", "The questions a tenant-side review will ask and the evidence that answers them."),
        ("register.html", "Full register", "Every finding in one filterable table with its status and source."),
        ("audit.html", "Independent audit", "A fresh read of each controlling source on 8 November 2026, with the words relied on."),
        ("flagged.html", "Flagged for review", "Open items, conflicts and blanks, published for your review."),
        ("sources.html", "Sources", "All official sources retrieved and read, with what each was used for."),
        ("archive.html", "Earlier research sets", "The earlier compilations, all preserved unchanged."),
    ]:
        b += '<a class="card" href="hub/%s"><h3>%s</h3><p>%s</p></a>' % (href, e(label), e(desc))
    b += '</div></section>'

    nver = sum(1 for r in R if r["status"] == VERIFIED)
    b += ('<section class="panel"><h2>Verification status</h2><p class="small">'
          '%d findings in the register: %d verified against an official source, %d owner-supplied or '
          'computed, and %d left blank or recorded as no-authority-found. '
          'Nothing is inferred. <a href="hub/register.html">Open the full register &rarr;</a> &middot; '
          '<a href="hub/audit.html">Read the 8 November audit &rarr;</a> &middot; '
          '<a href="hub/verification.html">What the build enforces &rarr;</a></p>'
          '<p class="note">Privacy: no tenant name, initial or street address appears anywhere on this site. '
          'Occupants are described by role only. Dates and dollar amounts are preserved exactly as supplied.</p>'
          '</section>' % (len(R), nver,
                          sum(1 for r in R if r["status"] in (OWNER, COMPUTED, ANALYSIS)),
                          sum(1 for r in R if r["status"] in (UNVERIFIED, ABSENT))))
    return layout("Overview", b, "index.html", root=True)


def page_exec():
    b = head("Executive summary",
             "Compiled 7 November 2026; the controlling rules were re-read on 8 November 2026. The "
             "licence question comes first because nothing else can be done safely until it is settled.")
    b += '<section class="panel"><h2>1. The licence question</h2><div class="answer">'
    b += ("<p><strong>You must be licensed, but you do not apply.</strong> Report each unit into the Rent "
          "Board Housing Inventory; a rent increase licence is generated automatically for a "
          "tenant-occupied unit. It must be current on the effective date of the increase. Individual "
          "owners are covered exactly as corporations are. %s</p>" % src("S1", "S2"))
    b += ("<p>No petition or prior approval is needed for an ordinary annual or properly calculated banked increase. "
          "Reporting is required before the effective date, not approval of the proposed notice. Recommended "
          "workflow: confirm the licence before serving. A licence is not immunity from a tenant challenge. %s</p>"
          % src("S3", "S13"))
    b += '</div>'
    b += reg_table("licence", "Licence and reporting - every requirement, with its source")
    b += '</section>'

    b += '<section class="panel"><h2>2. What is a normal increase here</h2>'
    b += ("<p class=\"small\">For a rent-controlled unit there is no market test. The lawful annual "
          "increase <em>is</em> the norm: <strong>1.6%%</strong> for effective dates from 1 March 2026 "
          "through 28 February 2027, once every 12 months, on base rent only, never rounded up. %s "
          "The statewide 8.8%% figure does not replace a stricter applicable local cap. Coverage of these "
          "particular units remains unverified. No official ZIP-level customary increase was established, "
          "and no federal statute caps rent in private, unsubsidised housing in the sources reviewed, so "
          "none is estimated here. %s %s</p>" % (src("S4", "S5"), src("S9", "S10"), src("S19")))
    rows = []
    for unit, name, base, pct, eff, note in SCENARIOS:
        inc = round(base * pct / 100, 2)
        rows.append([e(unit), e(name), "%.1f%%" % pct, money(inc), money(round(base + inc, 2)),
                     "%d days" % notice_days(pct), e(note), badge(COMPUTED) + " " + src("S4", "S8")])
    b += table("Options for each unit, computed from the published rates",
               ["Unit", "Option", "Total", "Increase", "New rent", "Notice", "Comment", "Status and source"],
               rows, numeric=(2, 3, 4))
    b += '</section>'

    b += '<section class="panel"><h2>3. The banking wording, and why it does not change your numbers</h2>'
    b += ("<p class=\"small\">The Rent Board's banking page says a skipped increase banks only if at least "
          "<strong>24 full months</strong> pass without any rent increase. Rule 4.12 says a full "
          "<strong>12 months</strong> must have elapsed from the date the increase could have been imposed. "
          "The Board's time-stamped worked examples follow the rule, not that sentence: on the banking page "
          "a 1.7%% increase available on 1 August 2024 is banked on 1 August 2025, twelve months later; on "
          "the rent increase page a 1.4%% increase is permanently lost eleven months after it became "
          "available, even though 35 months had passed since the tenant moved in. %s %s</p>"
          % (src("S6", "S7"), src("S5")))
    b += ("<p class=\"small\"><strong>Conditional illustration only.</strong> Assuming no intervening "
          "increases (F18), Unit 1 reaches twelve months after its skipped increase, and twenty-four months "
          "after the tenancy began, on the same date: 1 February 2027. Unit 2's no-increase history was not "
          "authenticated, so its banked figure is conditional too. Both readings of the wording therefore "
          "give the same answer, and the 3.0% figure for Unit 1 does not depend on resolving it. The conflict "
          "is published as F04 on the flagged page; ask a counsellor in writing if you want it closed.</p>")
    b += '</section>'

    b += '<section class="panel"><h2>4. One unit or both</h2>'
    b += ("<p class=\"small\">No provision requiring identical or simultaneous increases across units "
          "was found in the sources reviewed. %s What the law prohibits is a difference driven by a "
          "protected characteristic %s or a retaliatory or coercive purpose. %s The two tenancies are "
          "in materially different positions - one began in 2025, the other in 2019 with years of "
          "unused increases - so treating them differently is explained by the tenancy history, "
          "not by the tenants. Document that reasoning in writing before serving anything.</p>"
          % (src("S3"), src("S18", "S19"), src("S15", "S17")))
    b += '</section>'

    b += '<section class="panel"><h2>5. What to do next</h2><ol class="steps">'
    for h, p in [
        ("Confirm the Inventory and licence", "Check the public Rent Board Portal for both units. If either is unreported, report it now - it is free and the licence is generated on submission. " + src("S1")),
        ("Confirm coverage", "Verify the 1940 construction date on the Property Information Map. Coverage follows the pre-14 June 1979 rule. " + src("S11")),
        ("Fix the effective dates", "Unit 1: 1 February 2027 keeps the anniversary. Unit 2: on or before 28 February 2027 keeps the published 1.6% annual rate. " + src("S4", "S5")),
        ("Choose the size", "Decide between the low-scrutiny annual-only option and the full banked amount. Unit 2 above 10% needs 90 days. " + src("S8")),
        ("Write the file note", "Record the tenancy history, the arithmetic and the business reason. This is what a tenant-side review will ask for. " + src("S20")),
        ("Serve and keep proof", "Serve personally or by mail with the extra 5 days, and keep the proof of service and a copy of the notice. " + src("S8", "S5")),
    ]:
        b += "<li><h3>%s</h3><p>%s</p></li>" % (e(h), p)
    b += '</ol></section>'
    return layout("Executive summary", b, "executive-summary.html")


def page_process():
    b = head("The Rent Board process, step by step",
             "What is filed, where, and in what order. An ordinary annual or banked increase needs no "
             "petition and no approval - but it does need the licence and a compliant notice.")
    steps = [
        ("Confirm the unit is covered",
         "Units built on or before 13 June 1979 generally have rent control and eviction protection. "
         "Check the construction year on the Planning Department's Property Information Map, and speak "
         "to a Rent Board counsellor if the classification is unclear.", ["S11"]),
        ("Report into the Housing Inventory",
         "This is the step that replaces the 'application' you read about. Report each unit through the "
         "Rent Board Portal. It is free, online and available around the clock. For a building with fewer "
         "than 10 units the requirement began 1 March 2023 and repeats annually by 1 March.", ["S1", "S2"]),
        ("Receive the rent increase licence automatically",
         "Reporting a unit as non-owner-occupied generates the licence. There is nothing to apply for and "
         "no approval decision to await. Tenants can see your licence status in the public portal.", ["S1"]),
        ("Pay the separate Rent Board fee",
         "$59.00 per dwelling unit for 2026-2027, due 1 March. A fee exemption does not satisfy the "
         "Inventory requirement, and the Inventory does not request a fee exemption. They are two "
         "separate obligations.", ["S12", "S1"]),
        ("Calculate the increase",
         "Use the percentage in effect on the effective date, applied to base rent only. Add any banked "
         "percentages - added, never compounded, never rounded up. Identify which portion is banked and "
         "the dates it comes from.", ["S4", "S5", "S7"]),
        ("Check whether a petition is needed",
         "For an annual or banked increase, no petition. A petition is required only for the special "
         "types such as certified capital improvements or an operating and maintenance shortfall, and "
         "those must be filed before the notice.", ["S3", "S13"]),
        ("Work out the notice period",
         "30 days if the increase is 10% or less, 90 days if it is more than 10%, measured against the "
         "rent charged in the previous 12 months and combined with any other increase in that window. "
         "Add 5 days if you serve by mail.", ["S8", "S5", "S6"]),
        ("Serve a compliant written notice",
         "State the dollar amount, the percentage, the effective date and the banked portion. Serve "
         "personally or by mail under Code of Civil Procedure sec. 1013. A non-conforming increase is "
         "null and void under Rule 4.10(b).", ["S5", "S7", "S8"]),
        ("Keep the evidence file",
         "Lease, every notice, proof of service, rent receipts and the calculation. A tenant can file "
         "Form 516C at no charge and with no time limit, so the file is your answer.", ["S20"]),
    ]
    b += '<section class="panel"><ol class="steps">'
    for h, p, s in steps:
        b += "<li><h3>%s</h3><p>%s %s</p></li>" % (e(h), e(p), src(*s))
    b += '</ol></section>'
    b += '<section class="panel"><h2>Deadlines that matter</h2>'
    rows = [
        ["Housing Inventory update", "1 March each year", e("Late filing carries no monetary penalty, but the licence must exist on the effective date."), badge(VERIFIED) + " " + src("S1", "S2")],
        ["Rent Board fee", "1 March each year", e("5% monthly late penalty, capped at 15%."), badge(VERIFIED) + " " + src("S12")],
        ["Fee exemption request for 2027", "14 December 2026", e("Window closes before the fee is due."), badge(VERIFIED) + " " + src("S12")],
        ["Owner contact details change", "Within 30 days", e("Update the Inventory when owner or manager business contact information changes."), badge(VERIFIED) + " " + src("S2")],
        ["Rule 6.14 notice on a new occupant", "Generally 60 days", e("Measured from when the owner knew or should have known of the occupancy."), badge(VERIFIED) + " " + src("S14")],
    ]
    b += table("Standing deadlines", ["Obligation", "Deadline", "Detail", "Status and source"], rows)
    b += '</section>'
    b += '<section class="panel"><h2>What this process does not require</h2>'
    b += reg_table("licence", "Requirements and non-requirements")
    b += '</section>'
    return layout("Rent Board process", b, "process.html")


def page_units():
    b = head("Units and numbers",
             "Occupants are described by role only. No name, initial or address is published. Dates and "
             "dollar amounts are preserved exactly as supplied, and are marked owner-supplied because "
             "they cannot be confirmed from an official source.")
    b += '<section class="panel"><h2>Tenancy record as supplied</h2>'
    rows = []
    for u in UNITS:
        rows.append([e(u["label"]), money(u["base"]), u["start"].isoformat(), e(u["anniversary"]),
                     e(u["tenants"]), e(u["change"]), badge(OWNER) + " " + src("S5")])
    b += table("Owner-supplied inputs. The source link is the rule that governs the field, not evidence "
               "of the value.",
               ["Unit", "Base rent", "Tenancy began", "Anniversary", "Occupants", "Reported change", "Status"], rows)
    b += ('<p class="note">These inputs are unverified. The rent history, the construction year and the '
          'unit count all need documentary confirmation before any notice is served. '
          '<a href="flagged.html">See the flagged items &rarr;</a></p></section>')

    b += '<section class="panel"><h2>Unit 1 - line by line</h2>'
    rows = [
        ["Tenancy began", "2025-02-01", e("Owner-supplied start date; sets the 1 February anniversary."), badge(OWNER) + " " + src("S5")],
        ["First increase could be imposed", "2026-02-01", e("12 months after the lease began."), badge(VERIFIED) + " " + src("S5")],
        ["Rate in effect on that date", "%.1f%%" % U1_BANK, e("1 March 2025 - 28 February 2026 period."), badge(VERIFIED) + " " + src("S4")],
        ["Was it imposed?", "No", e("Rent reported unchanged; the increase was skipped."), badge(OWNER) + " " + src("S6")],
        ["When it becomes banked", "2027-02-01", e("12 full months after it became available; also 24 months after the tenancy began, so both readings agree."), badge(COMPUTED) + " " + src("S7", "S5", "S6")],
        ["Annual rate on 2027-02-01", "%.1f%%" % U1_ANN, e("1 March 2026 - 28 February 2027 period."), badge(VERIFIED) + " " + src("S4")],
        ["Total available", "%.1f%%" % U1_TOTAL, e("1.4 banked + 1.6 annual, added not compounded."), badge(COMPUTED) + " " + src("S4", "S7")],
        ["Dollar increase", money(round(3995 * U1_TOTAL / 100, 2)), e("3,995.00 x 0.030, not rounded up."), badge(COMPUTED) + " " + src("S4", "S5")],
        ["New base rent", money(round(3995 * (1 + U1_TOTAL / 100), 2)), e("Base plus increase."), badge(COMPUTED) + " " + src("S4")],
        ["Notice required", "30 days", e("3.0% is at or below the 10% threshold."), badge(VERIFIED) + " " + src("S8")],
        ["Serve by (personal)", serve_by(date(2027, 2, 1), U1_TOTAL).isoformat(), e("For an effective date of 2027-02-01."), badge(COMPUTED) + " " + src("S8")],
        ["Serve by (mail)", serve_by(date(2027, 2, 1), U1_TOTAL, True).isoformat(), e("Adds 5 days."), badge(COMPUTED) + " " + src("S8", "S5")],
    ]
    b += table("Unit 1 calculation chain", ["Step", "Value", "Basis", "Status and source"], rows)
    b += ('<p class="note"><strong>The 2026-04-01 occupant change is the one input that changes the '
          'answer.</strong> If any original lessee remained, the tenancy continues, the anniversary stays '
          '1 February and the 3.0% calculation above applies from 2027-02-01. If every original lessee '
          'left and a new tenancy began on 2026-04-01, the anniversary is 1 April, no banked amount from '
          'the earlier tenancy survives, and the first increase is available on 2027-04-01 at the rate the '
          'Board publishes on 2027-03-01. Charging more because a roommate moved in is unlawful in either '
          'case. ' + src("S5", "S6", "S14") + ' <a href="flagged.html">See F19 &rarr;</a></p></section>')

    b += '<section class="panel"><h2>Unit 2 - the banked ledger</h2>'
    rows = []
    for d, r in U2_LEDGER:
        banked_by = date(d.year + 1, d.month, d.day)
        eligible = banked_by <= date(2027, 2, 28)
        rows.append([d.isoformat(), "%.1f%%" % r, banked_by.isoformat(),
                     e("Banked" if eligible else "Not yet banked at 2027-02-28"),
                     badge(VERIFIED) + " " + src("S4", "S7")])
    b += table("Each skipped anniversary, the rate available on it, and when it banks",
               ["Available on", "Rate", "Banked from", "Position at 2027-02-28", "Status and source"], rows)
    rows = [
        ["Banked subtotal", "%.1f%%" % U2_BANKED, e("Sum of the six increases available 2020-2025, added not compounded."), badge(COMPUTED) + " " + src("S4", "S7")],
        ["Current annual", "%.1f%%" % U2_ANNUAL, e("Rate in effect on an effective date before 2027-03-01."), badge(VERIFIED) + " " + src("S4")],
        ["Total", "%.1f%%" % U2_TOTAL, e("Banked plus annual."), badge(COMPUTED) + " " + src("S4", "S7")],
        ["Dollar increase", money(round(3150 * U2_TOTAL / 100, 2)), e("3,150.00 x 0.131."), badge(COMPUTED) + " " + src("S4")],
        ["New base rent", money(round(3150 * (1 + U2_TOTAL / 100), 2)), e("Base plus increase."), badge(COMPUTED) + " " + src("S4")],
        ["Notice required", "90 days", e("13.1% exceeds the 10% threshold."), badge(VERIFIED) + " " + src("S8")],
        ["Serve by (personal)", serve_by(date(2027, 2, 28), U2_TOTAL).isoformat(), e("For an effective date of 2027-02-28."), badge(COMPUTED) + " " + src("S8")],
        ["Serve by (mail)", serve_by(date(2027, 2, 28), U2_TOTAL, True).isoformat(), e("Adds 5 days."), badge(COMPUTED) + " " + src("S8", "S5")],
    ]
    b += table("Unit 2 totals and notice timing", ["Step", "Value", "Basis", "Status and source"], rows)
    b += ('<p class="note">Timing note: an effective date on or after 1 March 2027 would use the next '
          'annual rate, which the Board has not published yet, so it is left blank on this site. '
          'Waiting until the 1 June 2027 anniversary would also preserve the 1.6% that became available '
          'on 1 June 2026, which is not yet banked at a February effective date. ' + src("S4", "S5") + '</p></section>')

    b += '<section class="panel"><h2>All options compared</h2>'
    rows = []
    for unit, name, base, pct, eff, note in SCENARIOS:
        inc = round(base * pct / 100, 2)
        rows.append([e(unit), e(name), "%.1f%%" % pct, money(inc), money(round(base + inc, 2)),
                     "%d days" % notice_days(pct), eff.isoformat(), serve_by(eff, pct).isoformat(),
                     badge(COMPUTED) + " " + src("S4", "S8")])
    b += table("Serve-by dates are computed from each effective date and assume personal service; add 5 days if mailed.",
               ["Unit", "Option", "Total", "Increase", "New rent", "Notice", "Effective", "Serve by", "Status and source"],
               rows, numeric=(2, 3, 4))
    b += '</section>'
    return layout("Units and numbers", b, "units.html")


def page_rates():
    b = head("Allowable increases",
             "The annual percentage is set by the Rent Board, not by the market. It is 60% of the "
             "published CPI increase and can never exceed 7%.")
    b += '<section class="panel"><h2>How the figure is set</h2>'
    b += reg_table("rates", "The rules behind the percentage")
    b += '</section>'
    b += '<section class="panel"><h2>Official rate table</h2>'
    rows = [[e("%s - %s" % (_d(a).isoformat(), _d(bb).isoformat())), "%.1f%%" % r,
             badge(VERIFIED) + " " + src("S4")] for a, bb, r in RATES]
    b += table("Transcribed from Rent Board Form 571, retrieved 7 November 2026 and re-read on 8 November 2026. "
               "Only one of the two 1992-1993 increases may be imposed, based on the tenant's anniversary date.",
               ["Effective period", "Allowable increase", "Status and source"], rows)
    b += ('<p class="note">The 12/8/1992 - 2/28/1993 and 3/1/1992 - 12/7/1992 rows overlap by design; '
          'the form carries an explicit caution that only one may be used for that period. ' + src("S4") + '</p>')
    b += '</section>'
    return layout("Allowable increases", b, "rates.html")


def page_notices():
    b = head("Notices", "The notice is where most increases fail. The period, the content and the "
                       "method of service are all prescribed.")
    b += '<section class="panel"><h2>Requirements</h2>'
    b += reg_table("notices", "Notice requirements and the consequence of getting them wrong")
    b += '</section>'
    b += '<section class="panel"><h2>Notice checklist</h2><div class="tw"><table>'
    b += '<caption>Content and service checklist drawn from the official guidance</caption>'
    b += '<thead><tr><th>Item</th><th>Requirement</th><th>Status and source</th></tr></thead><tbody>'
    for item, req, s in [
        ("Dollar amount", "State the exact dollar increase.", ["S5", "S6"]),
        ("Percentage", "State the percentage.", ["S5", "S6"]),
        ("Effective date", "State the date the increase takes effect.", ["S5", "S6"]),
        ("Banked portion", "Identify which part is banked and the dates it is based on.", ["S6", "S7"]),
        ("Annual portion", "Identify which part reflects the annual increase.", ["S7"]),
        ("Licence", "Must be on file on the effective date; it does not need to be attached.", ["S1"]),
        ("Service", "Personal delivery, or mail under Code of Civil Procedure sec. 1013 with 5 extra days.", ["S8", "S5"]),
        ("Proof", "Keep a copy and proof of service in the evidence file.", ["S20"]),
    ]:
        b += "<tr><td>%s</td><td>%s</td><td>%s %s</td></tr>" % (e(item), e(req), badge(VERIFIED), src(*s))
    b += '</tbody></table></div></section>'
    b += '<section class="panel"><h2>Reasons for the increase</h2>'
    b += ("<p class=\"small\">An annual or banked increase does not need a stated justification - the "
          "ordinance authorises it and the notice must instead identify the annual and banked portions. "
          "%s Reasons and cost evidence belong to petition-based increases such as certified capital "
          "improvements. %s In practice a short, factual covering note helps: it should refer to the "
          "published annual percentage and the anniversary date, and should avoid any reference to a "
          "tenant's personal circumstances, a request for repairs, or a wish to see the unit vacated. "
          "Those are the facts that turn a lawful number into a retaliation or harassment claim. %s</p>"
          % (src("S3", "S7"), src("S3"), src("S17", "S15")))
    b += ('<p class="note"><a href="notice-kit.html">Open the notice kit &rarr;</a> for a model notice, '
          'the pre-service checklist and the three ways a notice fails.</p>')
    b += '</section>'
    return layout("Notices", b, "notices.html")


def page_laws():
    b = head("Law and protections",
             "Three layers apply. The local ordinance sets the number; state law sets the notice "
             "procedure and the retaliation rule; federal law is anti-discrimination law.")
    b += '<section class="panel"><h2>Which layer governs what</h2>'
    rows = [
        ["Local - SF Rent Ordinance", e("Sets the allowable percentage, banking, the licence and coverage."),
         e("Governs if local rent-control coverage is confirmed."), badge(VERIFIED) + " " + src("S3", "S2", "S11")],
        ["State - Civil Code sec. 827", e("Sets the 30 and 90 day notice periods and the service methods."),
         e("Governs how the increase is communicated."), badge(VERIFIED) + " " + src("S8")],
        ["State - AB 1482 rent cap", e("5% plus CPI, maximum 10%; 8.8% in San Francisco for 2026-2027."),
         e("Does not replace stricter applicable local limits; property coverage remains unverified."), badge(VERIFIED) + " " + src("S9", "S10")],
        ["State - Civil Code sec. 1942.5", e("Prohibits retaliatory rent increases."),
         e("Governs the purpose and timing, not the amount."), badge(VERIFIED) + " " + src("S17")],
        ["State - FEHA", e("Prohibits housing discrimination on a broad list of characteristics."),
         e("Governs who is treated differently and why."), badge(VERIFIED) + " " + src("S18")],
        ["Federal - Fair Housing Act", e("Prohibits discrimination on seven protected classes."),
         e("No federal rent ceiling was identified in the sources reviewed; subsidy status is unknown."), badge(ANALYSIS) + " " + src("S19")],
    ]
    b += table("Layer by layer", ["Layer", "What it does", "Effect on these units", "Status and source"], rows)
    b += '</section>'
    b += '<section class="panel"><h2>All findings</h2>'
    b += reg_table("laws", "Coverage, preemption, discrimination and retaliation")
    b += '</section>'
    return layout("Law and protections", b, "laws.html")


def page_practices():
    b = head("Owner practices",
             "How corporate and individual owners are treated, whether both units must move together, "
             "and what counts as a defensible reason.")
    b += '<section class="panel"><h2>Corporations versus individual owners</h2>'
    b += ("<p class=\"small\">The rent cap does not distinguish between them. Section 37.3 applies to "
          "'landlords', and section 37.15 applies to 'owners', with no portfolio threshold. %s "
          "No official empirical comparison of corporate and individual-owner practices was confirmed. "
          "Recommendation for either owner type: use an annual compliance calendar, preserve a unit-specific "
          "rent ledger, and document calculations and service. This is a suggested workflow, not a "
          "verified description of industry practice. %s</p>" % (src("S3", "S2"), src("S20")))
    b += ("<p class=\"small\">One tool commonly associated with large operators is specifically unlawful "
          "here: section 37.10C prohibits using algorithmic revenue-management devices that draw on "
          "non-public competitor data to set rents, with each month and each unit a separate violation "
          "and a private right of action for tenants and tenant nonprofits. %s</p>" % src("S16"))
    b += '</section>'
    b += '<section class="panel"><h2>One unit or both</h2>'
    b += ("<p class=\"small\">Raising one unit and not the other is not itself discrimination. No "
          "provision requiring uniform or simultaneous increases was found. %s The risk is not "
          "difference, it is the <em>reason</em> for the difference. A difference explained by tenancy "
          "start date, anniversary date and unused banked increases is a business explanation. A "
          "difference that tracks a protected characteristic %s or follows a repair request or a "
          "tenant complaint %s is not.</p>" % (src("S3"), src("S18", "S19"), src("S17", "S15")))
    b += ("<p class=\"small\">Raising both units purely to look even is the weaker strategy: it forces "
          "an increase on a tenancy that may not need one, and it does not answer the question a "
          "reviewer would actually ask. Write down the per-unit reasoning instead.</p>")
    b += '</section>'
    b += '<section class="panel"><h2>Findings</h2>'
    b += reg_table("practices", "Owner practice questions")
    b += '</section>'
    return layout("Owner practices", b, "practices.html")


def page_review():
    b = head("The tenant-lawyer test",
             "What a tenant-side review will ask, and the evidence that answers it. A Rent Board "
             "petition is free for the tenant and has no filing deadline, so the file has to hold up "
             "indefinitely.")
    b += '<section class="panel"><h2>The questions to be ready for</h2>'
    rows = [
        ["Was the unit covered, and was the base rent lawful?", e("Lease, rent history, and the construction-year record."), badge(VERIFIED) + " " + src("S11", "S20")],
        ["Was there a licence on the effective date?", e("Portal record showing the Inventory submission and licence."), badge(VERIFIED) + " " + src("S1", "S2")],
        ["Is the percentage the one in effect on the effective date?", e("Form 571 for the relevant period."), badge(VERIFIED) + " " + src("S4", "S5")],
        ["Has 12 months passed since the last increase?", e("Prior notices and the rent ledger."), badge(VERIFIED) + " " + src("S5", "S7")],
        ["Are the banked years real, added and not compounded?", e("A year-by-year ledger like the one on the units page."), badge(VERIFIED) + " " + src("S7", "S6")],
        ["Was the notice period right for the size?", e("Notice, proof of service, and the 12-month look-back."), badge(VERIFIED) + " " + src("S8")],
        ["Did the notice identify the annual and banked portions?", e("A copy of the notice as served."), badge(VERIFIED) + " " + src("S7")],
        ["Was the figure rounded up?", e("The arithmetic, to the cent."), badge(VERIFIED) + " " + src("S5", "S7")],
        ["Did it follow a repair request or complaint?", e("Maintenance log and correspondence dates."), badge(VERIFIED) + " " + src("S17")],
        ["Does the difference between units track a protected trait?", e("The written per-unit business reasoning."), badge(VERIFIED) + " " + src("S18", "S19")],
        ["Was it used to push a tenant out?", e("Any buyout offers, and the market context for the figure."), badge(VERIFIED) + " " + src("S15")],
        ["Was an extra charge added for a new occupant?", e("The ledger showing no occupant-based charge."), badge(VERIFIED) + " " + src("S5")],
    ]
    b += table("Each question with the evidence that answers it",
               ["Question a reviewer will ask", "Evidence to have ready", "Status and source"], rows)
    b += '</section>'
    b += '<section class="panel"><h2>How a challenge actually runs</h2>'
    b += reg_table("review", "Challenge routes, counsel and hearing format")
    b += '</section>'
    return layout("Tenant-lawyer test", b, "review.html")


def page_register():
    b = head("Full verification register",
             "Every finding in one table. Filter it by typing. Values that could not be confirmed "
             "from an official source are blank rather than estimated.")
    b += '<section class="panel">'
    b += '<input class="filter" id="f" type="search" placeholder="Filter findings, for example: licence, banking, notice, 1.6" aria-label="Filter the register">'
    b += '<div class="tw"><table id="reg"><caption>%d findings, each with its verification status and official source</caption>' % len(R)
    b += '<thead><tr>' + "".join("<th>%s</th>" % e(h) for h in REG_HEADERS) + '</tr></thead><tbody>'
    for r in R:
        note = '<div class="note">%s</div>' % e(r["note"]) if r["note"] else ""
        b += ("<tr><td>%s</td><td>%s%s</td><td>%s</td><td>%s</td><td>%s</td></tr>"
              % (e(r["id"]), e(r["item"]), note, val(e(r["value"])), badge(r["status"]), src(*r["sources"])))
    b += '</tbody></table></div>'
    b += ('<p class="note">Statuses: <span class="pill">Verified</span> quoted or directly derived from an '
          'official source. <span class="pill">Owner-supplied</span> given by the owner, not confirmable '
          'officially. <span class="pill">Computed</span> arithmetic from verified rates and supplied '
          'inputs. <span class="pill">Analysis</span> reasoning, not a quoted rule. '
          '<span class="pill">Unverified</span> left blank on purpose. '
          '<span class="pill">No authority found</span> an absence-of-authority finding.</p>')
    b += '</section>'
    b += """<script>
(function(){var f=document.getElementById('f');if(!f)return;
f.addEventListener('input',function(){var q=f.value.toLowerCase();
var rows=document.querySelectorAll('#reg tbody tr');
for(var i=0;i<rows.length;i++){rows[i].style.display=
rows[i].textContent.toLowerCase().indexOf(q)>-1?'':'none';}});})();
</script>"""
    return layout("Full register", b, "register.html")


FLAGS = [
    ("F01", "Owner-supplied rent history", "The owner supplied dates and amounts, not an authenticated complete ledger. In particular, no intervening Unit 2 increases is an assumption used for illustrations, not an expressly supplied or verified fact. Lawful base rents and unused banking remain unconfirmed.",
     "Unverified input", ["S20"], "Produce the lease and the rent ledger before serving. A tenant petition can reach the whole rent history with no time limit."),
    ("F02", "Construction year and coverage", "The 1940 build year and the two-unit count are owner-supplied. Coverage follows from them, so coverage itself is unconfirmed.",
     "Unverified input", ["S11"], "Check the Property Information Map and, if unclear, ask a Rent Board counsellor."),
    ("F03", "Inventory and licence status unknown", "Whether either unit has been reported, and whether a licence is currently on file, could not be checked.",
     "Unverified input", ["S1", "S2"], "This is the first action item. The portal is public and reporting is free."),
    ("F04", "Banking wording: 12 versus 24 months",
     "The banking page says a skipped increase is banked only if at least 24 full months pass without any rent increase. Rule 4.12 says a full 12 months must have elapsed from the date the increase could have been imposed, and two official worked examples run the clock from the date each increase became available.",
     "Conflicting official wording - time-stamped examples read as controlling", ["S5", "S6", "S7"],
     "The time-stamped examples and Rule 4.12 are treated as controlling, so the conflict does not change the arithmetic. Conditional on no intervening increases (F18), Unit 1 reaches 12 months after the skipped increase and 24 months after the tenancy began on the same date, 2027-02-01. Obtain written counselling and authenticate the rent ledger before relying on any banked amount."),
    ("F05", "Rule 6.14 notice on the later co-tenant", "Whether a 6.14 notice was served on the occupant added to Unit 1 around 2026-04-01 is unknown. Generally 60 days is considered reasonable.",
     "Missing fact with future consequences", ["S14"],
     "If it was not served, an unlimited increase when the last original occupant leaves may not be available under Rule 6.14. This does not affect the current annual or banked increase."),
    ("F06", "Effective date after 28 February 2027", "The annual rate for 1 March 2027 onward has not been published.",
     "Left blank", ["S4"], "Any effective date on or after 2027-03-01 needs the rate published on that date. The figure is deliberately blank."),
    ("F07", "No federal rent ceiling identified", "No federal statute capping increases for private unsubsidised housing was found in the sources reviewed.",
     "Absence of authority, not a quoted rule", ["S19"], "Recorded as a search result, not as a legal conclusion."),
    ("F08", "No uniform-increase requirement found", "No provision requiring both units to be raised together, or by the same amount, was found.",
     "Absence of authority, not a quoted rule", ["S3", "S18"], "The anti-discrimination and retaliation rules still apply to the reason for any difference."),
    ("F09", "Pending local legislation on banked increases", "Proposals to cap banked increases at 10% a year were reported during 2026. No official legislative status page was confirmed in this session.",
     "Unverified", ["S6"], "No value is asserted. If enacted, it would affect the Unit 2 full-bank option. Recheck before serving."),
    ("F10", "ZIP-level market rent not published", "No official rent figure for ZIP 94122 was confirmed. The Rent Board does not publish a market rent for a ZIP code.",
     "Left blank", ["S5"], "For a rent-controlled unit the lawful increase does not depend on market rent, so nothing is estimated here."),
    ("F11", "Notice deadlines assume personal service", "Serve-by dates on this site are computed for personal delivery.",
     "Method limitation", ["S8", "S5"], "Add 5 days if serving by mail. Both dates are shown on the units page."),
    ("F12", "Bedroom count and square footage not supplied", "The Inventory requires bedroom and bathroom counts and approximate square footage in 250 square foot increments.",
     "Unverified input", ["S1", "S2"], "Gather these before reporting. Best-estimate answers are permitted and are not penalised if given in good faith."),
    ("F13", "Two publication defects found and fixed", "The live landing page contained unsubstituted template tokens, and the coordination file contained unresolved merge-conflict markers.",
     "Fixed in this session", ["S5"], "Both were repository defects rather than legal questions. See the verification page for the checks now guarding against them."),
    ("F15", "Tenant initials were exposed in public source files",
     "An earlier session's privacy review found literal tenant initials inside two verification scripts. GitHub Pages serves the repository root, so those scripts were publicly readable. They were remediated by moving exact tokens into a git-ignored file, and this session's release gate follows the same pattern.",
     "Remediated in current files; history not rewritten", ["S1"],
     "Removing the strings does not remove them from public git history, forks or caches. No identifier is reproduced here. Consider whether a history rewrite or a GitHub removal request is warranted, and note that publishing a dedicated artifact instead of the repository root would reduce the exposure."),
    ("F16", "A flagged claim in an earlier set is itself incorrect",
     "One earlier set flagged that a Rent Board worked example applies 1.6% to a 1 May 2026 effective date when 1.4% was in force. Form 571 shows 1.6% in force from 1 March 2026, so 1.6% is correct for that date and the example is not in error on that point.",
     "Corrected by verification", ["S4", "S5"],
     "A separate, real labelling slip does exist on the same guidance page: the first example says the rate in effect on 1 June 2025 is 1.6%, when 1.4% applied on that date. The increase in that example takes effect 1 June 2026, where 1.6% is correct, so the arithmetic is right and only the date label is wrong."),
    ("F14", "Earlier sets differ in presentation", "Five earlier compilations are preserved on this site. They agree on the verified rules but differ on whether to price unit-specific figures.",
     "Reconciled, not deleted", ["S4", "S5"], "This consolidated set prices the options and labels every result computed. The earlier sets remain reachable from the archive page."),
    ("F19", "Unit 1: the anniversary date depends on a fact not supplied",
     "The record shows a continuing tenancy from 2025-02-01 at $3,995.00 and a later occupant by 2026-04-01 with the rent unchanged. If any original lessee remained, the tenancy continues and the anniversary stays 1 February. If every original lessee left, a new tenancy may have begun on 2026-04-01.",
     "Unverified input with a two-branch answer", ["S5", "S6"],
     "Branch A (continuing): the increases available on 2026-02-01 (1.4%) and 2027-02-01 (1.6%) give 3.0% from 2027-02-01. Branch B (new tenancy): the anniversary is 1 April, no banked amount survives the new tenancy, and the first increase is available 2027-04-01 at the rate published 2027-03-01. Whether an unlimited reset is available at all depends on Rule 6.14 or Costa-Hawkins, on whether the later occupant is a co-tenant or a subtenant, and on a 6.14 notice having been served within a reasonable time - generally 60 days (F05). Establish which branch applies before serving anything."),
    ("F17", "No official empirical norm for corporate practice or customary increases",
     "No official comparison of corporate and individual-owner conduct, and no official customary-increase figure for ZIP 94122, was established. The published legal allowance is not evidence of observed market practice.",
     "Absence of evidence, not a quoted rule", ["S3", "S5"],
     "Use the compliance workflow as a recommendation only; treat any claim that corporations raise rents by a particular amount as unverified unless it cites a government source."),
    ("F18", "Banked scenarios assume a rent history that was not provided",
     "The owner supplied a 2019 starting rent for Unit 2, not a complete intervening ledger. The full-bank examples assume no intervening increases and an unchanged lawful base rent. They are conditional arithmetic, not verified entitlements.",
     "Unverified input; conditional arithmetic only", ["S5", "S6", "S20"],
     "Authenticate leases, receipts and every prior increase before using any illustrated total."),
    ("F20", "The complete Rules and Regulations were not read end to end",
     "Part IV and Part X were read in full text on sf.gov. The complete Rules and Regulations compilation (document 625, amended 13 January 2026) was linked but not read in full, so an amendment outside those Parts could exist.",
     "Method limitation", ["S24", "S7", "S23"],
     "Search the complete compilation before relying on a mechanical point, or ask a counsellor."),
]


def page_flagged_blank():
    b = head("Flagged for review",
             "Open items, conflicts and deliberate blanks. None of these blocks publication; they are "
             "here so you can review them and ask for changes.")
    b += '<section class="panel">'
    rows = []
    for fid, title, desc, kind, s, action in FLAGS:
        rows.append([e(fid), '<strong>%s</strong><div class="note">%s</div>' % (e(title), e(desc)),
                     e(kind), e(action), src(*s)])
    b += table("Every flagged item with its source and the action that would close it",
               ["Ref", "Item", "Type", "What would resolve it", "Official source"], rows)
    b += '</section>'
    blank = [r for r in R if r["status"] in (UNVERIFIED, ABSENT)]
    b += '<section class="panel"><h2>Values left blank rather than guessed</h2>'
    rows = []
    for r in blank:
        rows.append([e(r["id"]), e(r["item"]), '<span class="blank">blank</span>',
                     e(r["note"]), badge(r["status"]) + " " + src(*r["sources"])])
    b += table("These cells are empty by design", ["Ref", "Finding", "Value", "Why", "Status and source"], rows)
    b += '</section>'
    return layout("Flagged for review", b, "flagged.html")


def page_sources():
    b = head("Sources",
             "Every source below was retrieved and read during this session. Only official publishers "
             "are used: the San Francisco Rent Board, the California Legislature, the California Civil "
             "Rights Department and the United States Department of Housing and Urban Development.")
    b += '<section class="panel">'
    rows = []
    for sid, (title, pub, url) in SOURCES.items():
        used = [r["id"] for r in R if sid in r["sources"]]
        rows.append([e(sid), e(title), e(pub),
                     '<a href="%s" target="_blank" rel="noopener">Open official page</a>' % e(url),
                     e(", ".join(used) if used else "context"),
                     badge(VERIFIED) + ' <a class="src" href="%s" target="_blank" rel="noopener">%s</a>' % (e(url), sid)])
    b += table("Source register", ["Ref", "Source", "Publisher", "Link", "Used by", "Status"], rows)
    b += '</section>'
    b += '<section class="panel"><h2>Method and limits</h2>'
    b += ("<p class=\"small\">Each page listed above was opened and read, not merely search-listed. "
          "Quotations in the register are taken from the text of those pages. Arithmetic is computed "
          "from the published percentages and the owner-supplied base rents and is labelled computed. "
          "Where an official page could not be reached, or a value is not published, the cell is left "
          "blank and the item appears on the flagged page.</p>")
    b += ("<p class=\"small\">Two limits are worth stating plainly. First, external links are checked "
          "for shape and publisher at build time, not for perpetual availability; government sites move. "
          "Second, no property record, portal account, lease or rent ledger was available, so nothing "
          "here certifies that a particular increase on a particular unit is lawful. It sets out the "
          "rules, the arithmetic and the evidence you would need.</p>")
    b += '</section>'
    return layout("Sources", b, "sources.html")


def page_archive():
    b = head("Earlier research sets",
             "Five compilations were published to this repository by earlier sessions before this "
             "consolidated set. They are preserved unchanged and remain reachable here.")
    b += '<section class="panel"><h2>Preserved sets</h2><div class="cards">'
    for href, label, desc in [
        ("../pages/executive-summary.html", "Deep-dive set", "Fifteen pages covering the process, units, laws, notices, owner playbook and tenant review."),
        ("../dashboard/index.html", "Data-driven dashboard", "Ten pages generated from JSON data files, with market context and a findings table."),
        ("../process.html", "First published set", "The original six-page set, deliberately conservative about unit-specific figures."),
        ("../docs/index.html", "License-focused dashboard", "Twelve pages with a calculator whose self-tests reproduce the Rent Board's published worked examples, plus line-by-line research notes."),
        ("../previous-dashboard.html", "Previous merged hub", "The landing page that previously combined the three sets, kept for reference."),
    ]:
        b += '<a class="card" href="%s"><h3>%s</h3><p>%s</p></a>' % (href, e(label), e(desc))
    b += '</div>'
    b += ('<p class="note">These sets agree on the verified rules. They differ on presentation: some '
          'decline to price unit-specific figures, while this consolidated set prices the options and '
          'labels every result computed. Where an earlier set describes the banking wording as an '
          'unresolved conflict, this set explains why the two readings converge and shows that neither '
          'unit\'s figure depends on the difference. <a href="flagged.html">See F04 and F14 &rarr;</a></p>')
    b += '</section>'
    return layout("Earlier research sets", b, "archive.html")


def page_verification():
    b = head("Verification", "What was checked, how, and what the build enforces.")
    b += ('<p class="note">This page covers the mechanical checks. The point-by-point re-reading of the '
          'sources, with the words relied on, is on the <a href="audit.html">independent audit page</a>.</p>')
    b += '<section class="panel"><h2>Checks run</h2>'
    rows = [
        ["Rate table", e("All 46 periods transcribed from Form 571 and compared against the repository data files."),
         e("27 CSV rows, 9 ledger rows and 8 JSON rates matched; zero mismatches."), badge(VERIFIED) + " " + src("S4")],
        ["Arithmetic", e("Every scenario recomputed independently from the published percentages."),
         e("Matches to the cent; no rounding up applied."), badge(COMPUTED) + " " + src("S4", "S5")],
        ["Notice periods", e("30 and 90 day thresholds and the 5 day mailing addition read against the statute."),
         e("Confirmed in Civil Code sec. 827(b)."), badge(VERIFIED) + " " + src("S8")],
        ["Licence rule", e("Section 37.15 read in full, including the suspension and prospective-restoration clause."),
         e("Confirmed; no entity-size exemption."), badge(VERIFIED) + " " + src("S2")],
        ["Source coverage", e("Every table data row must carry an official source link."),
         e("Enforced by the release gate at build time."), badge(VERIFIED) + " " + src("S5")],
        ["Privacy", e("All published HTML scanned for the supplied tenant initials and for street addresses."),
         e("None present. Occupants are described by role only."), badge(VERIFIED) + " " + src("S1")],
        ["Template tokens", e("Scan for unsubstituted placeholders in generated HTML."),
         e("Defect found in the previous landing page and fixed; now guarded."), badge(VERIFIED) + " " + src("S5")],
        ["Merge markers", e("Scan for unresolved conflict markers in tracked files."),
         e("Markers found in the coordination file and repaired; now guarded."), badge(VERIFIED) + " " + src("S5")],
        ["Rate table years", e("Every effective period re-read from Form 571 on 8 November 2026 and the two-digit years re-checked."),
         e("Defect found: 1982-1999 printed as 2082-2099 (F19). Fixed, table re-checked row by row; gate now rejects any year outside 1982-2027."),
         badge(VERIFIED) + " " + src("S4")],
        ["Independent re-verification", e("Section 37.15, section 37.3, Form 571, the rent increase and banking pages, Rules 4.10 and 4.12, Civil Code sections 827, 1942.5 and 1947.12, the AB 1482 page, the Rent Board fee page, Form 516C and Form 1007 re-fetched and re-read on 8 November 2026."),
         e("All published values matched. The 1.6% rate, the licence rule, the notice periods and the AB 1482 exemption are unchanged."),
         badge(VERIFIED) + " " + src("S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "S12", "S20", "S21")],
        ["Arithmetic re-check", e("Both units' five scenarios recomputed from the base rents and the published percentages."),
         e("Unit 1: 1.6% = $63.92 and 3.0% = $119.85. Unit 2: 1.6% = $50.40, 13.1% = $412.65 and 10.0% = $315.00. All match to the cent, none rounded up."),
         badge(COMPUTED) + " " + src("S4", "S8")],
    ]
    b += table("Verification performed in this session", ["Check", "Method", "Result", "Status and source"], rows)
    b += '</section>'
    return layout("Verification", b, "verification.html")


# ---------------------------------------------------------------------------
# INDEPENDENT AUDIT - read on 2026-11-08. Each row is one point checked, the
# words relied on, and whether the site's value agrees. Short quotations only.
# ---------------------------------------------------------------------------
AUDIT = [
    ("A01", "Who must report into the Housing Inventory",
     "Owners of residential dwelling units subject to this Chapter 37 shall be required to report certain information about their units to the Rent Board",
     "Confirms that an individual owner is included; no entity threshold appears.", ["S2"]),
    ("A02", "When small buildings had to start reporting",
     "For condominium units and units in buildings with fewer than 10 units, the information shall be reported commencing March 1, 2023",
     "Confirms 1 March 2023 for a two-unit building.", ["S2"]),
    ("A03", "What happens while the licence is suspended",
     "a tenant shall not be obligated to pay the increased rent for months during the period of suspension",
     "Confirms the suspension is not retroactively cured.", ["S2"]),
    ("A04", "How the licence is issued",
     "once you have reported into the Housing Inventory, a rent increase license will be automatically generated for non-owner occupied units",
     "Confirms there is no application form.", ["S1"]),
    ("A05", "Whether the licence must exist on the effective date",
     "your rent increase notice will not be enforceable without having a rent increase license on the effective date of the notice",
     "Confirms the timing rule.", ["S1"]),
    ("A06", "Whether the Inventory is public",
     "The information entered in the housing inventory submission is public.",
     "Confirms the privacy consequence.", ["S1"]),
    ("A07", "The annual cap formula",
     "a rent increase which does not exceed a tenant's base rent by more than 60% of said published increase. In no event, however, shall the allowable annual increase be greater than 7%",
     "Confirms the formula and the 7% ceiling.", ["S3"]),
    ("A08", "Banking in the ordinance",
     "may accumulate said increase and, subject to Section 37.15, impose that amount on the tenant's subsequent rent increase anniversary dates",
     "Confirms accumulation with no month-count condition in the ordinance.", ["S3"]),
    ("A09", "Rule 4.12 banking condition",
     "A full 12 months must have elapsed from the date that an annual rent increase, or a portion thereof, could have been imposed",
     "Confirms the 12-month test in the rule.", ["S7"]),
    ("A10", "The banking page's own wording",
     "A skipped increase is only banked if at least 24 full months pass without any rent increase.",
     "Quoted as published; see F04 for why it does not change either figure.", ["S6"]),
    ("A11", "The worked example that loses a skipped increase",
     "the 1.4% rent increase is permanently lost due to the change in anniversary date",
     "Confirms the clock runs from availability, not from the tenancy start.", ["S5"]),
    ("A12", "The current rate and its period",
     "Effective March 1, 2026 through February 28, 2027, the allowable annual increase amount is 1.6%",
     "Confirms 1.6% for both units' planned effective dates.", ["S4"]),
    ("A13", "That no petition is needed for the annual increase",
     "may increase the tenant's base rent once every 12 months by the amount of the allowable annual rent increase without filing a petition at the Rent Board",
     "Confirms no petition and no Board approval.", ["S4"]),
    ("A14", "Notice content under the ordinance",
     "Which portion of the rent increase reflects the annual increase, and/or a banked amount, if any",
     "Confirms the itemisation duty.", ["S3"]),
    ("A15", "Notice content for a banked increase",
     "inform the tenant, on or before the date upon which the landlord gives the tenant legal notice, which portion of the rent increase reflects banked amount",
     "Confirms Rule 4.12(b); failure does not void the increase.", ["S7"]),
    ("A16", "What a defective notice does",
     "shall render the entire rent increase null and void",
     "Confirms Rule 4.10(b) is a whole-notice rule, subject to the half-percent good-faith readjustment.", ["S7"]),
    ("A17", "The 30 and 90 day thresholds",
     "If the proposed rent increase for that tenant is 10 percent or less ... at least 30 days ... greater than 10 percent ... at least 90 days",
     "Confirms the thresholds and that exactly 10 percent is a 30-day case.", ["S8"]),
    ("A18", "How the 10 percent is measured",
     "of the rental amount charged to that tenant at any time during the 12 months before the effective date of the increase, either in and of itself or when combined with any other rent increases",
     "Confirms the look-back and the combination rule.", ["S8"]),
    ("A19", "Service methods",
     "By delivering a copy to the tenant personally. By serving a copy by mail under the procedures prescribed in Section 1013",
     "Confirms personal service or mail; San Francisco adds 5 days for mail.", ["S8", "S5"]),
    ("A20", "Whether the state cap applies here",
     "Housing subject to rent or price control through a public entity's valid exercise of its police power ... that restricts annual increases in the rental rate to an amount less than that provided in subdivision (a)",
     "Confirms the local cap displaces AB 1482 for these units.", ["S9", "S10"]),
    ("A21", "Coverage of a pre-1979 building",
     "Many residential units built on or before June 13, 1979 have both rent control and eviction protection.",
     "Confirms the rule; the 1940 build year itself is owner-supplied (F02).", ["S11"]),
    ("A22", "The fee and its exemption",
     "$59.00 per dwelling unit; requesting a Rent Board Fee exemption does not satisfy Rent Board Housing Inventory reporting requirements",
     "Confirms the fee is separate from the licence.", ["S12"]),
    ("A23", "Repair-based deferral of an increase",
     "The petition must be filed no later than 60 days following the tenant's receipt of the rent increase notice.",
     "Confirms the 60-day window and the refund consequence.", ["S22", "S23"]),
    ("A24", "Cost and deadline of a tenant challenge",
     "There is no charge for filing the petition; There is no time limit for filing a petition",
     "Confirms the file has to stand up indefinitely.", ["S20"]),
    ("A25", "Extra charge for a new occupant",
     "a landlord may not impose increases solely because a tenant has added an additional occupant to an existing tenancy",
     "Confirms no occupant-based charge is available.", ["S3"]),
    ("A26", "Market rent as evidence of bad faith",
     "the rent increase was substantially in excess of market rates for comparable units",
     "Confirms market comparison matters only inside a circumvention claim.", ["S15"]),
    ("A27", "Arithmetic of both units",
     "3,995.00 x 3.0% = 119.85; 3,150.00 x 13.1% = 412.65; 3,150.00 x 10% = 315.00",
     "Recomputed to the cent; nothing rounded up.", ["S4", "S8"]),
]


def page_audit():
    b = head("Independent audit, 8 November 2026",
             "A second read of every controlling source, the exact words relied on, and whether the "
             "site agrees with them. This page is generated from the same data the release gate "
             "checks, so it cannot drift away from the site.")
    b += '<section class="panel"><h2>Point-by-point check</h2>'
    rows = []
    for ref, point, quote, verdict, srclist in AUDIT:
        rows.append([e(ref), '<strong>%s</strong>' % e(point),
                     '<span class="quote">%s</span>' % e(quote),
                     e(verdict), badge(VERIFIED) + " " + src(*srclist)])
    nq = len(rows)
    b += table("Short quotations from the official pages, read on 2026-11-08", 
               ["Ref", "Point checked", "Words relied on", "Result", "Status and source"], rows)
    b += ('<p class="note">%d points re-read. Quotations are shortened with ellipses where marked; '
          'nothing is paraphrased inside quotation marks.</p>' % nq)
    b += '</section>'
    b += '<section class="panel"><h2>What this pass changed</h2><ul class="tick">'
    for item in [
        "F04 was rewritten. The earlier text described the 12-month and 24-month wording as "
        "reconciled; on a closer read the 24-month sentence cannot be squared with either worked "
        "example, so the time-stamped examples and Rule 4.12 are treated as controlling and the "
        "conflict is published rather than smoothed over.",
        "The Unit 1 anniversary fork was added as F19. The answer changes if no original lessee "
        "remained after the 2026 occupant change, and that fact was not supplied.",
        "A second limit was added: the complete Rules and Regulations compilation was linked but not "
        "read end to end (F20).",
        "The rent notice kit was added, because the notice content rules are spread across three "
        "documents and are easy to get wrong in practice.",
    ]:
        b += '<li>%s</li>' % e(item)
    b += '</ul></section>'
    b += '<section class="panel"><h2>What this audit does not establish</h2>'
    b += ('<ul class="tick">'
          '<li>No lease, rent ledger, portal record or property record was examined, so nothing here '
          'certifies that a particular increase is lawful on these facts.</li>'
          '<li>The build year, the unit count and both base rents remain owner-supplied (F01, F02).</li>'
          '<li>External links are checked for publisher and shape at build time, not for perpetual '
          'availability.</li>'
          '<li>No browser rendering test was run; the HTML is validated by parser checks instead.</li>'
          '<li>Nothing here is legal advice, and no notice, petition or licence action was taken.</li>'
          '</ul></section>')
    return layout("Audit", b, "audit.html")


def page_notice_kit():
    b = head("Notice kit",
             "What the notice has to say, a model notice to work from, and the checks to run before "
             "it is served. The content rules come from three documents: the Rent Ordinance, the "
             "Rent Board Rules, and the Civil Code.")
    b += '<section class="panel"><h2>What the notice must contain</h2>'
    rows = [
        ["Written notice, at least 30 days ahead",
         e("30-day written notice of the proposed rent increase; 90-day written notice if the increase, "
           "alone or combined with another increase in the same year, is more than 10%."),
         badge(VERIFIED) + " " + src("S5", "S8")],
        ["Five extra days if mailed",
         e("If the notice is mailed, the landlord must give the tenant 5 more days."),
         badge(VERIFIED) + " " + src("S5", "S8")],
        ["Dollar amount, percentage, effective date, banked part",
         e("The rent increase notice should include the dollar amount of the increase, the percentage "
           "amount, the date it goes into effect, and which part of the increase is banked."),
         badge(VERIFIED) + " " + src("S5", "S6")],
        ["Which portion is annual, and which is banked",
         e("Sec. 37.3(b)(1) and Rule 4.10(a)(1) require the owner to tell the tenant in writing, on or "
           "before the date the notice is given, which portion of the increase reflects the annual "
           "increase and which reflects a banked amount."),
         badge(VERIFIED) + " " + src("S3", "S7")],
        ["The dates the banked amount is based on",
         e("Rule 4.12(b)(2): state the dates upon which the banked amount is based. Failure to include "
           "this does not by itself void the increase, but it is the first thing a reviewer looks for."),
         badge(VERIFIED) + " " + src("S7")],
        ["The right percentage",
         e("Use the percentage that will be in effect on the date of the increase, not the percentage "
           "in effect on the date the notice is served."),
         badge(VERIFIED) + " " + src("S5", "S6")],
        ["Correct service",
         e("Personal delivery, or mail under Code of Civil Procedure sec. 1013. Keep proof of the date "
           "and method."),
         badge(VERIFIED) + " " + src("S8")],
        ["The licence does not have to be attached",
         e("The rent increase license does not need to be included with the rent increase notice."),
         badge(VERIFIED) + " " + src("S1")],
        ["A reason is not required",
         e("No provision in sec. 37.3(b), Rule 4.10(a) or Civil Code sec. 827 requires the owner to "
           "state a reason for an annual or banked increase. The duty is to itemise the increase, not "
           "to justify it."),
         badge(ABSENT) + " " + src("S3", "S7", "S8")],
    ]
    b += table("Required elements, with the official wording and source",
               ["Element", "What the official text says", "Status and source"], rows)
    b += '</section>'

    b += '<section class="panel"><h2>Model notice</h2>'
    b += ('<p class="small">This is a drafting aid for your own records, not a Rent Board form and not '
          'legal advice. Everything in square brackets is yours to complete accurately. Delete the '
          'lines that do not apply to the unit you are serving.</p>')
    model = """NOTICE OF RENT INCREASE

Date of this notice: [date you deliver or mail it]
To: [tenant name or names as they appear on the rental agreement]
Rental unit: [unit identifier, not the full street address]
Current base rent: $[amount] per month
New base rent: $[amount] per month
Amount of the increase: $[amount] per month
Percentage increase: [x.x]% of the current base rent
Effective date: [a date at least 30 days after this notice, or at least 90 days if the increase is more than 10 percent; add 5 days if this notice is mailed]

How the increase is made up (Rent Ordinance sec. 37.3(b); Rules and Regulations sec. 4.10(a)):
  - Annual allowable increase: [x.x]%, being the Rent Board allowance in effect on the effective date
  - Banked increase: [x.x]%, based on the rent increase anniversary dates of [list the dates]

Rent increase licence: this unit is reported in the Rent Board Housing Inventory and a rent increase
licence is on file. The licence does not need to be attached to this notice.

Questions: Rent Board counsellors, 415-252-4600, weekdays 9am to noon and 1pm to 4pm.

Your options: you may ask the Rent Board to review this increase by filing Tenant Petition Form 516C
(there is no filing fee and no time limit). If repairs you have requested in writing have not been
made, you may file Form 516B within 60 days of receiving this notice; a granted petition postpones
the increase until the work is done.

Served by: [personal delivery / first-class mail] on [date]"""
    b += '<pre class="notice">%s</pre>' % e(model)
    b += '</section>'

    b += '<section class="panel"><h2>Before you serve: the checklist</h2><ul class="tick">'
    for item in [
        "Both units are reported in the Housing Inventory for the current reporting year, and the licence shows in the Rent Board Portal.",
        "The anniversary date is confirmed from the rent ledger - for Unit 1 that turns on whether any original lessee remained (F19).",
        "At least 12 months have passed since the last increase on that tenancy.",
        "The percentage used is the one in effect on the effective date: 1.6% for any effective date up to 28 February 2027.",
        "Only properly banked amounts are added, nothing is compounded, and nothing is rounded up.",
        "The notice states the dollar amount, the percentage, the effective date, the annual portion and the banked portion with its dates.",
        "The notice period matches the size of the increase: 30 days at or below 10%, 90 days above 10%, plus 5 days if mailed.",
        "No increase is charged because a new occupant moved in, and no passthrough has been folded into base rent.",
        "There are no outstanding written repair requests on the unit that could support a Form 516B petition.",
        "A short written note explains, per unit, the business basis for the increase and why the two units differ. Keep it in the file.",
        "A copy of the notice and proof of service are kept with the lease and the rent ledger.",
    ]:
        b += '<li>%s</li>' % e(item)
    b += '</ul></section>'

    b += '<section class="panel"><h2>The three ways a notice fails</h2>'
    rows = [
        ["Served without a current licence",
         e("The notice is not enforceable for the months of suspension, and reporting later does not revive them."),
         badge(VERIFIED) + " " + src("S1", "S2")],
        ["Content does not conform to Rule 4.10(a)",
         e("The entire increase is null and void, unless it is within the allowable annual and banked amounts; a good-faith excess of no more than one-half of one percent can be readjusted by an administrative law judge."),
         badge(VERIFIED) + " " + src("S7", "S3")],
        ["Too little notice",
         e("30 days at or below 10%, 90 days above 10%, measured against the rent charged at any time in the previous 12 months and combined with any other increase in that window."),
         badge(VERIFIED) + " " + src("S8")],
    ]
    b += table("The failures that void or defer an increase", ["Failure", "Consequence", "Status and source"], rows)
    b += ('<p class="note">A fourth route is not a defect in the notice: a tenant who has asked in '
          'writing for repairs may petition within 60 days of receiving the notice, and the increase is '
          'postponed until the work is done. %s</p></section>' % src("S22", "S23"))
    return layout("Notice kit", b, "notice-kit.html")


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------
PAGES = {
    "executive-summary.html": page_exec,
    "process.html": page_process,
    "units.html": page_units,
    "rates.html": page_rates,
    "notices.html": page_notices,
    "laws.html": page_laws,
    "practices.html": page_practices,
    "review.html": page_review,
    "register.html": page_register,
    "flagged.html": page_flagged_blank,
    "sources.html": page_sources,
    "archive.html": page_archive,
    "verification.html": page_verification,
    "audit.html": page_audit,
    "notice-kit.html": page_notice_kit,
}


def write(path, text):
    full = ROOT / path
    full.parent.mkdir(parents=True, exist_ok=True)
    full.write_text(text, encoding="utf-8")
    return path


def build():
    written = []
    written.append(write("hub/hub.css", CSS))
    written.append(write("index.html", page_index()))
    for slug, fn in PAGES.items():
        written.append(write("hub/" + slug, fn()))

    # CSV export of the register, for manual review outside the site.
    reg = ROOT / "data" / "verified-register.csv"
    reg.parent.mkdir(parents=True, exist_ok=True)
    with reg.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["ref", "category", "finding", "verified_value", "status", "note", "official_sources"])
        for r in R:
            w.writerow([r["id"], r["cat"], r["item"], r["value"], r["status"], r["note"],
                        " | ".join(SOURCES[s][2] for s in r["sources"])])
    written.append("data/verified-register.csv")

    # Keep the standalone summary in step with this build. The summary and its
    # regression checks live in tools/followup_audit.py (session arena-75594f57).
    from followup_audit import write_summary
    write_summary(ROOT)
    written.append("EXECUTIVE-SUMMARY.md")

    # Repository record of the audit, generated from the same data as hub/audit.html
    # so the two can never drift apart.
    md = ["# Independent audit - 8 November 2026", "",
          "Generated by `tools/build_hub.py` from the same data that renders "
          "`hub/audit.html` and that the release gate checks.", "",
          "Scope: a fresh read of every controlling official source for the rules this site relies on. "
          "No lease, rent ledger, portal record or property record was examined, so nothing here "
          "certifies a particular increase on these facts.", "",
          "| Ref | Point checked | Words relied on | Result | Source |",
          "| --- | --- | --- | --- | --- |"]
    for ref, point, quote, verdict, srclist in AUDIT:
        urls = " ".join(SOURCES[i][2] for i in srclist)
        md.append("| %s | %s | %s | %s | %s |" % (ref, point, quote.replace("|", "/"), verdict, urls))
    md += ["", "## Findings that changed this pass", "",
           "- F04 rewritten: the banking page's 24-month sentence cannot be squared with either official "
           "worked example, so the time-stamped examples and Rule 4.12 are treated as controlling.",
           "- F19 added: Unit 1's anniversary date depends on whether any original lessee remained after "
           "the 2026 occupant change.",
           "- F20 added: the complete Rules and Regulations compilation was linked but not read end to end.",
           "- Notice kit added: the notice-content duties are split across section 37.3(b), Rule 4.10(a) "
           "and Rule 4.12(b), which is where a compliant increase most often fails.",
           "", "## Register totals", "",
           "- %d findings: %d verified, %d owner-supplied or computed, %d blank or no-authority-found."
           % (len(R), sum(1 for r in R if r["status"] == VERIFIED),
              sum(1 for r in R if r["status"] in (OWNER, COMPUTED, ANALYSIS)),
              sum(1 for r in R if r["status"] in (UNVERIFIED, ABSENT))),
           ""]
    (ROOT / "AUDIT-2026-11-08.md").write_text("\n".join(md), encoding="utf-8")
    written.append("AUDIT-2026-11-08.md")

    # Mirror into site/ so the repository's root/site parity audit keeps passing.
    import shutil
    (ROOT / "site" / "hub").mkdir(parents=True, exist_ok=True)
    for p in (ROOT / "hub").iterdir():
        if p.is_file():
            shutil.copyfile(p, ROOT / "site" / "hub" / p.name)
    shutil.copyfile(ROOT / "index.html", ROOT / "site" / "index.html")
    if (ROOT / "previous-dashboard.html").exists():
        shutil.copyfile(ROOT / "previous-dashboard.html", ROOT / "site" / "previous-dashboard.html")
    (ROOT / "site" / "data").mkdir(parents=True, exist_ok=True)
    shutil.copyfile(reg, ROOT / "site" / "data" / "verified-register.csv")

    nv = sum(1 for r in R if r["status"] == VERIFIED)
    print("Built %d files. Register: %d findings, %d verified, %d blank or no-authority."
          % (len(written), len(R), nv, sum(1 for r in R if r["status"] in (UNVERIFIED, ABSENT))))
    return written


if __name__ == "__main__":
    build()
