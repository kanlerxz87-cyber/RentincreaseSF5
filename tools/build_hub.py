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
TODAY = date(2026, 11, 11)

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
    "S22": ("Annual rent increase for multiple years", "SF Rent Board",
            "https://www.sf.gov/information--annual-rent-increase-multiple-years"),
    "S23": ("The Rent Ordinance (Chapter 37 index)", "SF Rent Board",
            "https://www.sf.gov/reports--rent-ordinance/"),
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

# ---------------------------------------------------------------------------
# Unit arithmetic - computed from owner-supplied inputs and official rates.
# ---------------------------------------------------------------------------
UNITS = [
    dict(label="Unit 1", base=3995.00, start=date(2025, 2, 1), anniversary="February 1",
         tenants="Three original occupants; one original occupant remains, one later co-tenant added.",
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

NAV = [
    ("index.html", "Overview"),
    ("executive-summary.html", "Executive summary"),
    ("process.html", "Rent Board process"),
    ("units.html", "Units and numbers"),
    ("rates.html", "Allowable increases"),
    ("notices.html", "Notices"),
    ("laws.html", "Law and protections"),
    ("practices.html", "Owner practices"),
    ("review.html", "Tenant-lawyer test"),
    ("register.html", "Full register"),
    ("flagged.html", "Flagged for review"),
    ("sources.html", "Sources"),
    ("verification.html", "Verification"),
    ("archive.html", "Earlier research sets"),
]


def nav_html(active, root=False):
    out = []
    for href, label in NAV:
        target = ("hub/" + href) if root else href
        if href == "index.html":
            target = "index.html" if root else "../index.html"
        cls = ' class="active"' if href == active else ""
        out.append('<a href="%s"%s>%s</a>' % (target, cls, e(label)))
    return "".join(out)


def layout(title, body, active, root=False, desc=None):
    flag_link = "hub/flagged.html" if root else "flagged.html"
    body = ('<section class="panel"><p><strong>Conditional research, not an approved increase.</strong> '
            'Coverage, lawful base rents, complete rent history and current licences are unverified. '
            'Banked examples assume no intervening increases; that history was not established for Unit 2. '
            'No amount is cleared for service or guaranteed to pass legal review. '
            '<a href="' + flag_link + '">Review the limitations (including F17–F19)</a>.</p></section>') + body
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
<small>Outer Sunset 94122 &middot; anonymised &middot; sources rechecked 11 Nov 2026</small></div>
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
             "Every figure below is either quoted from an official source or computed from the published "
             "rate, and each table row links to the page it came from.")
    b += """
<section class="panel">
<h2>Your first question: the Rent Board and the licence</h2>
<div class="answer">
<p><strong>Yes, you need the licence. No, you do not apply for it, and being an individual owner
changes nothing.</strong></p>
<p>Section 37.15(a) obliges every owner of a residential unit covered by the Rent Ordinance to report
into the Rent Board's Housing Inventory. There is no corporation threshold and no small-owner
exemption. Once a unit is reported as tenant-occupied, a rent increase licence is
<strong>generated automatically</strong> - there is no application form and no approval to wait for. %s</p>
<p>The licence must already be on file <strong>on the effective date</strong> of the increase. If it is
not, the licence is suspended, the notice is not enforceable, and the tenant owes no increased rent for
the months of suspension. Reporting later restores the licence <strong>prospectively only</strong>. %s</p>
<p>You do <strong>not</strong> need a petition or Board approval for an ordinary annual or banked
increase. Petitions are only for the special increase types such as certified capital improvements. %s</p>
</div>
<p class="note">So the order is: report into the Inventory first, confirm the licence is on file, then
serve the notice. <a href="hub/process.html">Read the nine-step process &rarr;</a></p>
</section>
""" % (src("S1", "S2"), src("S2"), src("S3", "S13"))

    b += '<div class="grid">'
    for k, v, n in [
        ("Allowable annual increase", "1.6%", "1 Mar 2026 - 28 Feb 2027 " + src("S4", "S5")),
        ("Unit 1 conditional scenario, 1 Feb 2027", "%.1f%%" % U1_TOTAL,
         "%s on %s " % (money(round(3995 * U1_TOTAL / 100, 2)), money(3995)) + src("S4")),
        ("Unit 2 conditional full-bank scenario", "%.1f%%" % U2_TOTAL,
         "%s on %s " % (money(round(3150 * U2_TOTAL / 100, 2)), money(3150)) + src("S4")),
        ("Notice above 10%", "90 days", "30 days at or below 10% " + src("S8")),
    ]:
        b += '<div class="tile"><div class="k">%s</div><div class="v">%s</div><div class="n">%s</div></div>' % (e(k), e(v), n)
    b += '</div>'

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
          '<a href="hub/units.html">See the line-by-line arithmetic &rarr;</a></p></section>')

    b += '<section class="panel"><h2>Browse by category</h2><div class="cards">'
    for href, label, desc in [
        ("executive-summary.html", "Executive summary", "The licence answer first, then the numbers, the risks and the decisions."),
        ("process.html", "Rent Board process", "Nine steps from confirming coverage to a served notice, with official links."),
        ("units.html", "Units and numbers", "Anonymised tenancy records and every calculation shown line by line."),
        ("rates.html", "Allowable increases", "The full official rate table back to 1982 and how the figure is set."),
        ("notices.html", "Notices", "30 versus 90 days, required content, service methods and what voids a notice."),
        ("laws.html", "Law and protections", "Which cap governs, why the state cap does not, and fair-housing limits."),
        ("practices.html", "Owner practices", "Corporations versus individuals, one unit versus both, and lawful reasons."),
        ("review.html", "Tenant-lawyer test", "The questions a tenant-side review will ask and the evidence that answers them."),
        ("register.html", "Full register", "Every finding in one filterable table with its status and source."),
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
          'Nothing is inferred. <a href="hub/register.html">Open the full register &rarr;</a> &middot; <a href="hub/verification.html">What was checked and how &rarr;</a></p>'
          '<p class="note">Privacy: no tenant name, initial or street address appears anywhere on this site. '
          'Occupants are described by role only. Dates and dollar amounts are preserved exactly as supplied.</p>'
          '</section>' % (len(R), nver,
                          sum(1 for r in R if r["status"] in (OWNER, COMPUTED, ANALYSIS)),
                          sum(1 for r in R if r["status"] in (UNVERIFIED, ABSENT))))
    return layout("Overview", b, "index.html", root=True)


def page_exec():
    b = head("Executive summary",
             "Compiled 7 November 2026; every figure re-verified against the same official sources on 8 &amp; 11 November 2026. The licence question comes first because nothing else "
             "can be done safely until it is settled.")
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

    b += '<section class="panel"><h2>3. The banking conflict, resolved for these units</h2>'
    b += ("<p class=\"small\">The Rent Board's banking page says a skipped increase banks only after "
          "<strong>24 full months</strong>; Rule 4.12 says <strong>12 months</strong> from the date the "
          "increase could have been imposed. %s The Board's own worked example shows the clock runs "
          "from the date each increase became available. %s Because the first increase becomes available "
          "12 months after the tenancy starts, the two wordings describe the same point in time measured "
          "from different starting points.</p>" % (src("S6", "S7"), src("S5")))
    b += ("<p class=\"small\"><strong>Conditional illustration only.</strong> Assuming no intervening increases, Unit 1 reaches 24 months "
          "without an increase on 1 February 2027. Unit 2 banking assumes no increases since 2019, which was not established. Both "
          "readings give the same answer for both units, so the 3.0% figure for Unit 1 does not depend "
          "on resolving the wording. This reconciliation is analysis, not a quoted rule, and is "
          "published on the flagged page for confirmation. A proposed temporary 10% cap on combined "
          "banked and capital-improvement increases (File No. 261020) is under consideration and has "
          "not been enacted; see F09. " + src("S5") + "</p>")
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
    b += ('<p class="note">The occupant change reported on 2026-04-01 did not create a new tenancy because '
          'an original occupant remained, so the anniversary is unchanged and no rent reset arises. '
          'Charging more because a roommate moved in is unlawful. ' + src("S5", "S14") + '</p></section>')

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
    b += table("Serve-by dates assume personal service and are computed backwards from the effective date; the earlier of the two applies.",
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
    b += table("Transcribed from Rent Board Form 571, retrieved 7 November 2026 and re-read on 8 &amp; 11 November 2026. "
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
    ("F04", "Banking wording: 12 versus 24 months", "The banking page says 24 full months; Rule 4.12 says 12 months from when the increase could have been imposed. The worked example on the rent increase page runs the clock from availability, which reconciles them.",
     "Conflicting official wording, reconciled by analysis", ["S6", "S7", "S5"],
     "The reconciliation is interpretation, not a quoted rule. Conditional on no intervening increases: Unit 1 hits 24 months on 2027-02-01. Unit 2's no-increase history is unconfirmed (F18). Obtain written counselling and authenticate the ledger before relying on banking."),
    ("F05", "Rule 6.14 notice on the later co-tenant", "Whether a 6.14 notice was served on the occupant added to Unit 1 around 2026-04-01 is unknown. Generally 60 days is considered reasonable.",
     "Missing fact with future consequences", ["S14"],
     "If it was not served, an unlimited increase when the last original occupant leaves may not be available under Rule 6.14. This does not affect the current annual or banked increase."),
    ("F06", "Effective date after 28 February 2027", "The annual rate for 1 March 2027 onward has not been published.",
     "Left blank", ["S4"], "Any effective date on or after 2027-03-01 needs the rate published on that date. The figure is deliberately blank."),
    ("F07", "No federal rent ceiling identified", "No federal statute capping increases for private unsubsidised housing was found in the sources reviewed.",
     "Absence of authority, not a quoted rule", ["S19"], "Recorded as a search result, not as a legal conclusion."),
    ("F08", "No uniform-increase requirement found", "No provision requiring both units to be raised together, or by the same amount, was found.",
     "Absence of authority, not a quoted rule", ["S3", "S18"], "The anti-discrimination and retaliation rules still apply to the reason for any difference."),
    ("F09", "Pending local legislation on banked increases", "SF Rent Board notice posted 9 November 2026: Board of Supervisors File No. 261020 would temporarily limit combined banked and capital-improvement increases to 10% per year. If enacted as proposed it would apply to banked increases noticed on or after 15 September 2026. It has not been enacted and is subject to change.",
     "Proposed, not enacted - recheck before serving", ["S5"], "No value is asserted. If enacted as proposed, it would affect the Unit 2 full-bank option (13.1%). Recheck the Rent Board page before serving any banked increase."),
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
    ("F17", "Follow-up audit: practices and customary increases",
     "No official empirical comparison of corporate versus individual-owner conduct, or customary ZIP 94122 increase, was established. The legal allowance is not evidence of observed market practice.",
     "Unverified; recommendations distinguished", ["S5", "S20"],
     "Follow-up 8 November 2026: removed unsupported corporate-practice assertions from the consolidated page. Use the compliance workflow as a recommendation only."),
    ("F18", "Banked scenarios assume an unprovided complete rent history",
     "The user supplied a 2019 starting rent for Unit 2, not a complete intervening ledger. Full-bank examples assume no intervening increases and unchanged lawful base rent; they are not verified entitlements. Earlier archived sets may describe that assumption as owner-supplied.",
     "Unverified input; conditional arithmetic only", ["S5", "S6", "S20"],
     "Authenticate leases, receipts, every prior increase and concessions before using any illustrated total. No increase is cleared for notice or certified to pass a lawyer's review."),
    ("F19", "Published rate table showed the wrong century for 1982-1999",
     "The date helper that sorts and prints the Form 571 table mapped every two-digit year to 20xx, so the 1982-1999 rows were published as 2082-2099 (for example '2082-04-01 - 2083-02-28' for the 7.0% period that began 1 April 1982). No percentage was wrong; the years were.",
     "Repository defect, fixed and re-verified 2026-11-08", ["S4"],
     "Repaired in tools/build_hub.py and guarded by the release gate, which fails if any effective period falls outside 1982-2027. The full table was re-read against Form 571 after the fix: all 46 rows match. No legal conclusion or unit figure changed."),
    ("F20", "The licence must be current on the effective date, not necessarily at service",
     "Section 37.15(e) and the Inventory page tie the licence to the increase taking effect. Neither source states that the licence must already exist when the notice is served. Obtaining it before service is the recommended safer workflow, not a rule quoted from the ordinance.",
     "Wording precision, no figure affected", ["S1", "S2", "S5"],
     "Treat 'licence current before service' as prudent practice; treat 'licence current on the effective date' as the documented requirement."),
    ("F21", "Publication surface: GitHub Pages serves the whole repository root",
     "GitHub Pages publishes the entire repository root, so files such as the internal working notes and this coordination file are publicly readable, not just the HTML pages. The earlier internal note's claim that it was not published was incorrect and has been corrected. No tenant name, initial, address or parcel appears in any current file.",
     "Publication-surface limitation", ["S1", "S2"],
     "If the repository is made private, confirm Pages access settings before serving notices. Never store personal data anywhere in this repository."),

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
        ["Rate table years", e("Every effective period re-read from Form 571 on 11 November 2026 and the two-digit years re-checked."),
         e("Defect found: 1982-1999 printed as 2082-2099 (F19). Fixed, table re-checked row by row; gate now rejects any year outside 1982-2027."),
         badge(VERIFIED) + " " + src("S4")],
        ["Independent re-verification", e("Section 37.15, section 37.3, Form 571, the rent increase and banking pages, Rules 4.10 and 4.12, Civil Code sections 827, 1942.5 and 1947.12, the AB 1482 page, the Rent Board fee page, Form 516C and Form 1007 re-fetched and re-read on 11 November 2026. See VERIFICATION-47ECD4E4.md for today’s line-by-line check."),
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

    # Current standalone summary supersedes the archived generator summary.
    from followup_audit import write_summary
    write_summary(ROOT)

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
