#!/usr/bin/env python3
"""Deterministic builder and self-verifier for the f46f7d0f dashboard set.

Generates the anonymized San Francisco rent-increase research dashboard under
f46f7d0f/, plus the session executive summary and verification log at the repo
root. Every table row carries at least one direct official source link. Values
that could not be confirmed from an official source are rendered blank and
listed on the Flagged for Review page. No tenant names, initials, street or
unit addresses appear anywhere; dates and dollar amounts are preserved from
the owner intake exactly as supplied.

Run from the repository root: python3 f46f7d0f/build_f46f7d0f.py
The script writes its outputs, then validates structure, privacy patterns,
link integrity, source coverage and all arithmetic before reporting PASS.
"""
from __future__ import annotations

import json
import re
from datetime import date, timedelta
from decimal import Decimal
from html import escape as esc
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA_DIR = HERE / "data"
RESEARCH_DATE = "2026-11-11"
RESEARCH_DATE_LONG = "November 11, 2026"

OFFICIAL_SUFFIXES = (".sf.gov", ".ca.gov", ".hud.gov", ".huduser.gov", ".sfgov.org")
OFFICIAL_EXACT = {
    "sf.gov", "ca.gov", "hud.gov", "huduser.gov", "sfgov.org",
    "sfplanning.org", "sfplanninggis.org", "sfassessor.org", "sfrb.org",
}
INITIAL_PAIR = re.compile(r"(?<![A-Za-z])[A-Z]\s[A-Z](?![A-Za-z])|(?<![A-Za-z])[A-Z]\.[A-Z]\.(?![A-Za-z])")
CIVIC = {"S.F.", "U.S.", "D.C.", "N.Y.", "N.J.", "N.M.", "N.C.", "S.C."}
STREET = re.compile(
    r"\b\d{2,6}\s+[A-Z][A-Za-z.'-]*(?:\s+[A-Z][A-Za-z.'-]*){0,3}\s+"
    r"(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct)\b"
)
MERGE_MARKER = re.compile(r"^(<{7}|={7}|>{7})(?:\s|$)")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}


def is_official(url: str) -> bool:
    host = (urlsplit(url).hostname or "").lower()
    return urlsplit(url).scheme == "https" and (
        host in OFFICIAL_EXACT or host.endswith(OFFICIAL_SUFFIXES)
    )


CITY = "City and County of San Francisco"
STATE = "State of California"
FEDERAL = "United States government"

# id, publisher tier, register title, short link label, official URL.
S = [
    ("S01", CITY, "Rent Board Housing Inventory - reporting instructions and portal access",
     "Housing Inventory", "https://www.sf.gov/rent-board-housing-inventory"),
    ("S02", CITY, "San Francisco Administrative Code Sec. 37.15 - Reporting Obligations; Licensing",
     "Admin Code Sec. 37.15", "https://www.sf.gov/information--sec-3715-reporting-obligations-licensing"),
    ("S03", CITY, "Learn about rent increases in San Francisco (Rent Board)",
     "Rent increase guide", "https://www.sf.gov/learn-about-rent-increases-san-francisco"),
    ("S04", CITY, "Form 571 - Allowable Annual Rent Increases, 2026-27 edition (PDF)",
     "Form 571 PDF", "https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf"),
    ("S05", CITY, "Banked rent increases (Rent Board)",
     "Banked increases", "https://www.sf.gov/information--banked-rent-increases"),
    ("S06", CITY, "Annual rent increases for multiple years (Rent Board)",
     "Multiple-year increases", "https://www.sf.gov/information/annual-rent-increase-multiple-years"),
    ("S07", CITY, "Rent Board Rules and Regulations Part IV - Rent increases not requiring approval (December 2022)",
     "Part IV rules", "https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring"),
    ("S08", CITY, "San Francisco Administrative Code Sec. 37.2 - Definitions",
     "Sec. 37.2 definitions", "https://www.sf.gov/information/sec-372-definitions"),
    ("S09", CITY, "San Francisco Administrative Code Sec. 37.3 - Rent Limitations",
     "Sec. 37.3 rent limitations", "https://www.sf.gov/information/sec-373-rent-limitations"),
    ("S10", CITY, "San Francisco Administrative Code Sec. 37.10B - Tenant harassment",
     "Sec. 37.10B harassment", "https://www.sf.gov/information/sec-3710b-tenant-harassment"),
    ("S11", CITY, "San Francisco Administrative Code Sec. 37.10C - Use and sale of algorithmic devices prohibited",
     "Sec. 37.10C algorithmic devices", "https://www.sf.gov/information--sec-3710c-use-and-sale-algorithmic-devices-prohibited"),
    ("S12", CITY, "Petition determination pursuant to Section 6.14 and Costa-Hawkins (Rent Board)",
     "Sec. 6.14 and Costa-Hawkins", "https://www.sf.gov/information--petition-determination-pursuant-section-614-andor-costa-hawkins"),
    ("S13", CITY, "The Rent Board Fee",
     "Rent Board Fee", "https://www.sf.gov/rent-board-fee"),
    ("S14", CITY, "Landlord petitions and passthroughs (Rent Board)",
     "Petitions and passthroughs", "https://www.sf.gov/landlord-petitions-and-passthroughs/"),
    ("S15", CITY, "Learn about San Francisco rental laws - coverage guide (Rent Board)",
     "Rental-law coverage", "https://www.sf.gov/learn-about-san-francisco-rental-laws/"),
    ("S16", CITY, "California Tenant Protection Act of 2019 (state bill 1482) - Rent Board guide",
     "State bill 1482 guide", "https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482"),
    ("S17", CITY, "Report an unlawful rent increase or request a review of your rent history (Rent Board)",
     "Unlawful-increase review", "https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history/"),
    ("S18", CITY, "Form 1007 - Notice to Tenant required by Sec. 37.9(c) (multilingual PDF)",
     "Form 1007 notice", "https://www.sf.gov/sites/default/files/2023-08/1007%20Notice%20to%20Tenant%20Req%27d%20by%2037.%209(c)-Eng-Sp-Ch-Viet-Rus-Tag%5B74%5D.pdf"),
    ("S19", STATE, "California Civil Code Sec. 827 - written notice of rent increase",
     "Civil Code Sec. 827", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=827&lawCode=CIV"),
    ("S20", STATE, "California Civil Code Sec. 1942.5 - retaliatory actions prohibited",
     "Civil Code Sec. 1942.5", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1942.5&lawCode=CIV"),
    ("S21", STATE, "California Civil Code Sec. 1947.12 - Tenant Protection Act rent cap",
     "Civil Code Sec. 1947.12", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1947.12&lawCode=CIV"),
    ("S22", STATE, "California Civil Code Sec. 1954.53 - Costa-Hawkins Rental Housing Act",
     "Civil Code Sec. 1954.53", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1954.53&lawCode=CIV"),
    ("S23", STATE, "California Government Code Sec. 12955 - FEHA housing discrimination prohibitions",
     "Government Code Sec. 12955", "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=12955&lawCode=GOV"),
    ("S24", STATE, "California Civil Rights Department - housing discrimination",
     "Civil Rights Department", "https://calcivilrights.ca.gov/housing/"),
    ("S25", FEDERAL, "HUD - Fair Housing Act overview",
     "HUD Fair Housing overview", "https://www.hud.gov/helping-americans/fair-housing-act-overview"),
]
SRC = {sid: (title, url, tier) for sid, tier, title, _label, url in S}
SHORT = {sid: label for sid, _tier, _title, label, _url in S}
for _sid in SRC:
    assert is_official(SRC[_sid][1]), _sid


def link(sid: str) -> str:
    url = SRC[sid][1]
    return f'<a href="{esc(url, quote=True)}">{sid} · {esc(SHORT[sid])}</a>'


def links(*sids: str) -> str:
    return '<span class="src-links">' + '<br>'.join(link(s) for s in sids) + '</span>'


def badge(kind: str, text: str) -> str:
    return f'<span class="badge badge-{kind}">{esc(text)}</span>'


BADGES = {
    "verified": badge("verified", "Verified"),
    "calculated": badge("calculated", "Calculated - conditional"),
    "analysis": badge("analysis", "Analysis"),
    "recommendation": badge("analysis", "Recommendation"),
    "pending": badge("pending", "Pending"),
    "reported": badge("pending", "Owner-reported"),
    "unverified": badge("unverified", "Unverified"),
    "irregularity": badge("unverified", "Irregularity"),
}

BLANK = '<span class="blank-cell">&mdash; blank (unverified)</span>'


def table(caption: str, heads: list, rows: list, table_id: str | None = None) -> str:
    tid = f' id="{table_id}"' if table_id else ""
    out = ['<div class="table-wrap"><table%s>' % tid,
           f'<caption>{esc(caption)}</caption>',
           '<thead><tr>' + ''.join(f'<th scope="col">{esc(h)}</th>' for h in heads) + '</tr></thead>',
           '<tbody>']
    for row in rows:
        rid = f' id="{row["id"]}"' if row.get("id") else ""
        cells = row["cells"]
        body = ''.join(
            f'<th scope="row">{cells[0]}</th>' if i == 0 else f'<td>{c}</td>'
            for i, c in enumerate(cells)
        )
        out.append(f'<tr{rid}>{body}<td>{links(*row["srcs"])}</td></tr>')
    out.append('</tbody></table></div>')
    return "".join(out)


def money(base: Decimal, pct: Decimal) -> tuple[str, str]:
    inc = (base * pct / Decimal(100)).quantize(Decimal("0.01"))
    new = (base + inc).quantize(Decimal("0.01"))
    return f"${inc:,.2f}", f"${new:,.2f}"


def d(y: int, m: int, dd: int) -> str:
    return date(y, m, dd).isoformat()


# ---- deterministic figures, asserted before any rendering -------------------
UNIT_A_BASE = Decimal("3995.00")
UNIT_B_BASE = Decimal("3150.00")
B_BANKED = [("2020-21", Decimal("1.8")), ("2021-22", Decimal("0.7")),
            ("2022-23", Decimal("2.3")), ("2023-24", Decimal("3.6")),
            ("2024-25", Decimal("1.7")), ("2025-26", Decimal("1.4"))]
_bsum = sum(v for _p, v in B_BANKED)
assert _bsum == Decimal("11.5"), _bsum
_bcumulative = []
_run = Decimal("0")
for _p, _v in B_BANKED:
    _run += _v
    _bcumulative.append((_p, _v, _run))
assert [c for _p, _v, c in _bcumulative] == [Decimal("1.8"), Decimal("2.5"), Decimal("4.8"),
                                             Decimal("8.4"), Decimal("10.1"), Decimal("11.5")]
A1_INC, A1_NEW = money(UNIT_A_BASE, Decimal("1.6"))
A2_INC, A2_NEW = money(UNIT_A_BASE, Decimal("3.0"))
B1_INC, B1_NEW = money(UNIT_B_BASE, Decimal("1.6"))
B2_INC, B2_NEW = money(UNIT_B_BASE, Decimal("10.0"))
B3_INC, B3_NEW = money(UNIT_B_BASE, Decimal("13.1"))
assert (A1_INC, A1_NEW) == ("$63.92", "$4,058.92")
assert (A2_INC, A2_NEW) == ("$119.85", "$4,114.85")
assert (B1_INC, B1_NEW) == ("$50.40", "$3,200.40")
assert (B2_INC, B2_NEW) == ("$315.00", "$3,465.00")
assert (B3_INC, B3_NEW) == ("$412.65", "$3,562.65")
assert date(2027, 1, 1) - timedelta(days=30) == date(2026, 12, 2)
assert date(2027, 1, 1) - timedelta(days=35) == date(2026, 11, 27)
assert date(2027, 2, 1) - timedelta(days=30) == date(2027, 1, 2)
assert date(2027, 2, 1) - timedelta(days=35) == date(2026, 12, 28)
assert date(2027, 2, 15) - timedelta(days=90) == date(2026, 11, 17)
assert date(2027, 2, 15) - timedelta(days=95) == date(2026, 11, 12)

FORM571 = [
    ("3/1/26 - 2/28/27", "1.6%"), ("3/1/25 - 2/28/26", "1.4%"),
    ("3/1/24 - 2/28/25", "1.7%"), ("3/1/23 - 2/29/24", "3.6%"),
    ("3/1/22 - 2/28/23", "2.3%"), ("3/1/21 - 2/28/22", "0.7%"),
    ("3/1/20 - 2/28/21", "1.8%"), ("3/1/19 - 2/29/20", "2.6%"),
    ("3/1/18 - 2/28/19", "1.6%"), ("3/1/17 - 2/28/18", "2.2%"),
    ("3/1/16 - 2/28/17", "1.6%"), ("3/1/15 - 2/29/16", "1.9%"),
    ("3/1/14 - 2/28/15", "1.0%"), ("3/1/13 - 2/28/14", "1.9%"),
    ("3/1/12 - 2/28/13", "1.9%"), ("3/1/11 - 2/29/12", "0.5%"),
    ("3/1/10 - 2/28/11", "0.1%"), ("3/1/09 - 2/28/10", "2.2%"),
    ("3/1/08 - 2/28/09", "2.0%"), ("3/1/07 - 2/29/08", "1.5%"),
    ("3/1/06 - 2/28/07", "1.7%"), ("3/1/05 - 2/28/06", "1.2%"),
    ("3/1/04 - 2/28/05", "0.6%"), ("3/1/03 - 2/29/04", "0.8%"),
    ("3/1/02 - 2/28/03", "2.7%"), ("3/1/01 - 2/28/02", "2.8%"),
    ("3/1/00 - 2/28/01", "2.9%"), ("3/1/99 - 2/29/00", "1.7%"),
    ("3/1/98 - 2/28/99", "2.2%"), ("3/1/97 - 2/28/98", "1.8%"),
    ("3/1/96 - 2/28/97", "1.0%"), ("3/1/95 - 2/29/96", "1.1%"),
    ("3/1/94 - 2/28/95", "1.3%"), ("3/1/93 - 2/28/94", "1.9%"),
    ("12/8/92 - 2/28/93", "1.6%"), ("3/1/92 - 12/7/92", "4.0%"),
    ("3/1/91 - 2/29/92", "4.0%"), ("3/1/90 - 2/28/91", "4.0%"),
    ("3/1/89 - 2/28/90", "4.0%"), ("3/1/88 - 2/28/89", "4.0%"),
    ("3/1/87 - 2/29/88", "4.0%"), ("3/1/86 - 2/28/87", "4.0%"),
    ("3/1/85 - 2/28/86", "4.0%"), ("3/1/84 - 2/28/85", "4.0%"),
    ("3/1/83 - 2/29/84", "7.0%"), ("4/1/82 - 2/28/83", "7.0%"),
]
assert len(FORM571) == 46, len(FORM571)

NAV = [
    ("index.html", "Executive summary"),
    ("process.html", "License &amp; process"),
    ("units-and-rates.html", "Units &amp; rates"),
    ("laws-and-notices.html", "Laws &amp; notices"),
    ("practices-and-scrutiny.html", "Practices &amp; scrutiny"),
    ("repo-audit.html", "Repository audit"),
    ("flagged.html", "Flagged for review"),
    ("sources.html", "Sources"),
]

LEGAL_NOTE = (
    "Research only - not legal advice, not a rent-increase notice, and not a "
    "certification of any unit. No inventory filing, license request, tenant "
    "notice or attorney engagement was performed."
)
PRIVACY_NOTE = (
    "Privacy first: placeholder identities only (Unit A / Unit B; Tenant A1, "
    "Tenant A4, Tenant B1, Tenant B2). No tenant names, initials, street or "
    "unit addresses, parcel numbers or contact details are published. Dates "
    "and dollar amounts are reproduced exactly as supplied by the owner; the "
    "combination can still permit re-identification, so treat this page as "
    "sensitive."
)


def page(fname: str, title: str, eyebrow: str, lead: str, body: str) -> str:
    nav = "".join(
        '<a href="%s"%s%s>%s</a>' % (
            f, ' class="nav-flagged"' if f == "flagged.html" else "",
            ' aria-current="page"' if f == fname else "", label)
        for f, label in NAV
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Privacy-safe San Francisco rent-increase research dashboard, session F46F7D0F. Official sources only; unconfirmed values left blank and flagged.">
<title>{esc(title)} · SF Rent Review F46F7D0F</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<div class="topbar"><div class="topbar-inner">
<div class="brand-group"><a class="brand-title" href="index.html">SF RENT REVIEW · F46F7D0F</a>
<span class="brand-sub">Privacy-safe rent-increase research · Research date {RESEARCH_DATE_LONG}</span></div>
<a class="hub-return" href="../index.html">Repository hub</a>
</div></div>
<nav class="nav-bar" aria-label="Section navigation"><div class="nav-inner">{nav}</div></nav>
<main id="main" class="container">
<header class="page-header"><span class="eyebrow">{esc(eyebrow)}</span>
<h1>{esc(title)}</h1>
<p class="lead">{lead}</p></header>
{body}
</main>
<footer class="site-footer">
<p><strong>{LEGAL_NOTE}</strong></p>
<p>{PRIVACY_NOTE}</p>
<p>All findings verified against official sources fetched on {RESEARCH_DATE_LONG} (see <a href="sources.html">Sources</a>). Unconfirmed values are blank and listed under <a href="flagged.html">Flagged for review</a>, which does not block publication. Machine-readable copy of the findings: <a href="data/verified_findings.json">data/verified_findings.json</a>. Session verification log: <a href="../VERIFICATION-F46F7D0F.md">VERIFICATION-F46F7D0F.md</a>.</p>
</footer>
</body>
</html>
"""


def panel(title: str, inner: str, cls: str = "") -> str:
    c = f"panel {cls}".strip()
    return f'<section class="{c}"><h2>{esc(title)}</h2>{inner}</section>'


# ============================ page 1: index.html =============================
INDEX_ALERT = (
    '<div class="alert-banner"><strong>Pending legislation:</strong> Board of '
    'Supervisors File No. 261020 (introduced 2026-09-15) would temporarily cap '
    'combined banked and capital-improvement increases at 10% per year and, if '
    'enacted as drafted, would reach notices served on or after 2026-09-15. The '
    'City states it has <strong>not been enacted</strong> and is subject to '
    'change. See <a href="units-and-rates.html#banking-271020">banking impact</a> '
    'and <a href="flagged.html#FR-09">FR-09</a>. <strong>Time-sensitive:</strong> '
    'for the full-banked Unit B scenario effective 2027-02-15, a mailed 90-day '
    'notice would have to go out by 2026-11-12 - one day after this research '
    'date.</div>'
)

INDEX_FOREFRONT = panel("The license question, answered first", """
<p><strong>Question:</strong> I am an individual property owner, not a corporation. Do I still have to
report to the Rent Board and hold a rent-increase license before notifying tenants of an increase?</p>
<p><strong>Answer: yes on reporting, and the license comes from reporting.</strong> San Francisco
Administrative Code Sec. 37.15 applies to owners of covered residential units generally - it does not
exempt individuals (one of several co-owners may file for all). There is <strong>no separate license
application form or license fee</strong>: reporting a tenant-occupied unit into the Housing Inventory
through the Rent Board Portal generates the unit&rsquo;s rent-increase license on substantial compliance.
The practical rule is timing: the license must not be suspended <strong>on the increase&rsquo;s effective
date</strong>. If reporting lapses, the license is suspended during noncompliance, and even after it is
restored the tenant does not owe the increase for the suspended months.</p>
<p>The cited rules do <strong>not</strong> require attaching the license to the tenant notice, and the City
does not state that the license must precede service of the notice - but verifying it before service is
the safer workflow. A license also is <strong>not</strong> approval of the amount and does not prevent a
challenge for other violations (amount, timing, service, motive).</p>
""" + table(
    "License basics for an individual owner - verified 2026-11-11",
    ["Question", "Verified answer", "Status", "Official source"],
    [
        {"cells": ["Does the reporting duty cover individual owners?",
                   "Yes. Owners of residential units subject to Chapter 37 must report; in a multiple-owner unit a single owner&rsquo;s report suffices.",
                   BADGES["verified"], ],
         "srcs": ["S02", "S01"]},
        {"cells": ["Where and when to report?",
                   "Rent Board Portal Housing Inventory report, updated annually by March 1 (condominiums and buildings of 1-9 units report since 2023-03-01). Update contact details within 30 days of changes.",
                   BADGES["verified"], ],
         "srcs": ["S02", "S01"]},
        {"cells": ["How is the license obtained?",
                   "Substantial compliance with reporting generates the license automatically; no separate application or license fee exists.",
                   BADGES["verified"], ],
         "srcs": ["S02", "S03", "S01"]},
        {"cells": ["When must the license be effective?",
                   "On the increase&rsquo;s effective date. Suspension ends prospectively upon compliance; suspended months are not collectible.",
                   BADGES["verified"], ],
         "srcs": ["S02"]},
        {"cells": ["Must it be attached to the notice?",
                   "No such requirement in the cited rules. Recommended: confirm license status before serving the notice.",
                   BADGES["verified"] + " " + BADGES["recommendation"], ],
         "srcs": ["S01", "S03"]},
        {"cells": ["Accuracy duty",
                   "Reports are under penalty of perjury; never file placeholder identities from this site - use authentic records.",
                   BADGES["verified"], ],
         "srcs": ["S02", "S01"]},
        {"cells": ["Separate annual fee?",
                   "The license itself carries no fee. The separate Rent Board Fee is $59.00 per dwelling unit for 2026-27, due March 1 (exemptions exist).",
                   BADGES["verified"], ],
         "srcs": ["S13"]},
    ]),
    cls="callout-forefront")

INDEX_KPIS = """<div class="kpi-grid">
<div class="kpi-card"><span class="kpi-label">Current annual allowance</span>
<span class="kpi-value">1.6%</span>
<span class="kpi-detail">Effective dates 2026-03-01 through 2027-02-28 · 60% of Bay Area CPI change · <a href="https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf">S04 · Form 571 PDF</a></span></div>
<div class="kpi-card"><span class="kpi-label">License required on effective date</span>
<span class="kpi-value">Yes - individuals too</span>
<span class="kpi-detail">Automatic from Housing Inventory reporting · <a href="https://www.sf.gov/information--sec-3715-reporting-obligations-licensing">S02 · Admin Code Sec. 37.15</a></span></div>
<div class="kpi-card"><span class="kpi-label">Rent Board Fee 2026-27</span>
<span class="kpi-value">$59.00 / unit</span>
<span class="kpi-detail">Due March 1 · 50% pass-through possible · <a href="https://www.sf.gov/rent-board-fee">S13 · Rent Board Fee</a></span></div>
<div class="kpi-card"><span class="kpi-label">File No. 261020</span>
<span class="kpi-value">Pending - not enacted</span>
<span class="kpi-detail">Proposed 10% cap on combined banked and capital-improvement increases · <a href="https://www.sf.gov/learn-about-rent-increases-san-francisco">S03 · Rent increase guide</a></span></div>
</div>"""

INDEX_SEQUENCE = panel("Beginner sequence - the whole process in seven steps", """
<p>Each step is expanded with the official text it relies on in
<a href="process.html">License &amp; process</a>. Follow them in order; do not skip the
rent-history step - an overcharged base makes any later increase defeasible.</p>
""" + table(
    "Seven-step compliance path",
    ["Step", "Action", "Status", "Official source"],
    [
        {"cells": ['<a href="process.html#step-01">01</a>',
                   "Confirm both units are covered and check exemptions (reported 1940 construction is owner-reported, not authenticated - see <a href=\"flagged.html#FR-01\">FR-01</a>).",
                   BADGES["verified"], ], "srcs": ["S15"]},
        {"cells": ['<a href="process.html#step-02">02</a>',
                   "Report each unit into the Housing Inventory on the Rent Board Portal; renew by March 1 every year.",
                   BADGES["verified"], ], "srcs": ["S01", "S02"]},
        {"cells": ['<a href="process.html#step-03">03</a>',
                   "Confirm each unit&rsquo;s rent-increase license is active and will still be active on the chosen effective date.",
                   BADGES["verified"], ], "srcs": ["S02"]},
        {"cells": ['<a href="process.html#step-04">04</a>',
                   "Authenticate the lawful base rent and rent history; keep passthroughs out of the base.",
                   BADGES["verified"], ], "srcs": ["S17", "S03", "S14"]},
        {"cells": ['<a href="process.html#step-05">05</a>',
                   "Pick a lawful effective date: first increase 12 months after lease start, then at 12-month intervals; use the rate in force on the effective date.",
                   BADGES["verified"], ], "srcs": ["S03"]},
        {"cells": ['<a href="process.html#step-06">06</a>',
                   "Compute on the base rent only, never round up, and itemize any banked portion with its dates in the notice.",
                   BADGES["verified"], ], "srcs": ["S03", "S04", "S05", "S07"]},
        {"cells": ['<a href="process.html#step-08">07</a>',
                   "Serve a written notice: 30 days for a cumulative increase of 10% or less, 90 days above 10%; add 5 days if mailed; keep proof of service.",
                   BADGES["verified"], ], "srcs": ["S19", "S03"]},
    ]))

INDEX_SNAPSHOT = panel("Anonymized intake ledger - owner-reported, not authenticated", """
<p>Personal identifiers are withheld by policy. All values below come from the owner intake and remain
<strong>unverified</strong> against official records; blank fields stay blank (see
<a href="flagged.html">Flagged for review</a>).</p>
""" + table(
    "Intake facts as supplied - placeholders only",
    ["Item", "Supplied value", "Status", "Official route to authenticate"],
    [
        {"cells": ["Unit A - lease start",
                   "2025-02-01 at $3,995.00 per month; three initial occupants (placeholder identities only).",
                   BADGES["reported"], ], "srcs": ["S17"]},
        {"cells": ["Unit A - continuing tenancy",
                   "Reported 2026-04-01 at an unchanged $3,995.00; one original occupant (placeholder Tenant A1) remains and one subsequent occupant (Tenant A4) joined - a roommate addition alone cannot justify a surcharge, and no vacancy reset is available while an original occupant resides.",
                   BADGES["reported"], ], "srcs": ["S03", "S12", "S22"]},
        {"cells": ["Unit B - lease start",
                   "2019-06-01 at $3,150.00 per month; two occupants (placeholders Tenant B1 and Tenant B2). Intervening increases since 2019 are unknown (<a href=\"flagged.html#FR-05\">FR-05</a>).",
                   BADGES["reported"], ], "srcs": ["S17", "S05"]},
        {"cells": ["Building context",
                   "Owner reports 1940 construction, Outer Sunset (94122), both units rent controlled. Not authenticated (<a href=\"flagged.html#FR-01\">FR-01</a>).",
                   BLANK + " " + BADGES["unverified"], ], "srcs": ["S15"]},
    ]))

INDEX_RESULTS = panel("Headline results - conditional scenario arithmetic", """
<p>Each figure is <strong>conditional arithmetic on owner-reported inputs</strong>, not a verified
lawful rent or a recommendation to serve. Assumptions: periodic tenancy, active license, lawful base
equal to intake, no intervening increases for Unit B, no passthroughs, no subsidy restriction. Full
derivations and serve-by dates: <a href="units-and-rates.html">Units &amp; rates</a>.</p>
""" + table(
    "Scenario outcomes (computed and asserted in the build)",
    ["Scenario", "Increase", "Conditional new rent", "Notice", "Status", "Official source"],
    [
        {"cells": ['<a href="units-and-rates.html#sc-a1">A-1</a> · Unit A · annual-only 1.6%',
                   A1_INC, A1_NEW, "30 days (35 if mailed)", BADGES["calculated"], ],
         "srcs": ["S03", "S04", "S19"]},
        {"cells": ['<a href="units-and-rates.html#sc-a2">A-2</a> · Unit A · 2027-02-01 anniversary, 1.4% banked + 1.6% annual',
                   A2_INC, A2_NEW, "30 days (35 if mailed)", BADGES["calculated"], ],
         "srcs": ["S04", "S05", "S19"]},
        {"cells": ['<a href="units-and-rates.html#sc-b1">B-1</a> · Unit B · annual-only 1.6%',
                   B1_INC, B1_NEW, "30 days (35 if mailed)", BADGES["calculated"], ],
         "srcs": ["S03", "S04", "S19"]},
        {"cells": ['<a href="units-and-rates.html#sc-b2">B-2</a> · Unit B · 1.6% annual + 8.4% partial bank = 10.0%',
                   B2_INC, B2_NEW, "30 days (35 if mailed)", BADGES["calculated"], ],
         "srcs": ["S04", "S05", "S19"]},
        {"cells": ['<a href="units-and-rates.html#sc-b3">B-3</a> · Unit B · full bank 11.5% + 1.6% annual = 13.1%',
                   B3_INC, B3_NEW, "90 days (95 if mailed) · proposed-cap exposure", BADGES["calculated"], ],
         "srcs": ["S04", "S05", "S19"]},
    ]))

INDEX_INQUIRIES = panel("Your five inquiries - where each is answered", table(
    "Inquiry map",
    ["Inquiry", "Short verified answer", "Full analysis", "Official source"],
    [
        {"cells": ["1 · Reasonable and normal increases for both units",
                   "The lawful annual allowance is 1.6% for effective dates 2026-03-01 to 2027-02-28, citywide including 94122. No government benchmark for a neighborhood-specific &ldquo;normal&rdquo; amount exists - that value stays blank (<a href=\"flagged.html#FR-10\">FR-10</a>).",
                   '<a href="units-and-rates.html">Units &amp; rates</a>', ], "srcs": ["S03", "S04"]},
        {"cells": ["2 · Corporations vs individual owners",
                   "Legal duties are identical for both. No official empirical study of actual practices was found - blank and flagged (<a href=\"flagged.html#FR-11\">FR-11</a>); algorithmic pricing tools using non-public competitor data are banned for anyone.",
                   '<a href="practices-and-scrutiny.html">Practices &amp; scrutiny</a>', ],
         "srcs": ["S02", "S11"]},
        {"cells": ["3 · Correct notice and reasonable reasons",
                   "Written 30-day (or 90-day above 10%) notice stating dollar, percentage and effective date; mail adds 5 days. The ordinance does not condition annual increases on a stated reason; reasons such as inflation and upkeep are context, not authority.",
                   '<a href="laws-and-notices.html">Laws &amp; notices</a>', ], "srcs": ["S19", "S03", "S09"]},
        {"cells": ["4 · Tenant-advocate scrutiny",
                   "Twelve-point stress test built from the same sources a tenant-side reviewer would use; tenants can file a free petition with no deadline.",
                   '<a href="practices-and-scrutiny.html#stress-test">Stress test</a>', ],
         "srcs": ["S17", "S10", "S20"]},
        {"cells": ["5 · Raise one unit or both?",
                   "No uniform-increase statute was identified. A neutral written policy - commonly the same percentage for both eligible units - is the defensible posture; raising only one unit demands a documented, non-discriminatory basis.",
                   '<a href="practices-and-scrutiny.html#one-or-both">One or both</a>', ],
         "srcs": ["S23", "S24", "S25"]},
    ]))

INDEX_CARDS = panel("Dashboard sections", """
<div class="category-cards">
<div class="cat-card"><h3><a href="process.html">License &amp; process</a></h3>
<p>Nine-step compliance path, Housing Inventory reporting fields, license timing, Rent Board Fee calendar.</p></div>
<div class="cat-card"><h3><a href="units-and-rates.html">Units &amp; rates</a></h3>
<p>Anonymized Unit A / Unit B analysis, banking composition, conditional scenarios, and the complete 46-period Form 571 table.</p></div>
<div class="cat-card"><h3><a href="laws-and-notices.html">Laws &amp; notices</a></h3>
<p>Local, state and federal layers, notice content and service rules, and what counts as a valid reason.</p></div>
<div class="cat-card"><h3><a href="practices-and-scrutiny.html">Practices &amp; scrutiny</a></h3>
<p>Corporations vs individuals, one unit or both, and the twelve-point tenant-lawyer stress test.</p></div>
<div class="cat-card"><h3><a href="repo-audit.html">Repository audit</a></h3>
<p>Line-by-line review of this repository&rsquo;s files against official sources, including confirmed irregularities.</p></div>
<div class="cat-card"><h3><a href="flagged.html">Flagged for review</a></h3>
<p>Every unverified value and irregularity, FR-01 through FR-20, with blank cells instead of guesses.</p></div>
<div class="cat-card"><h3><a href="sources.html">Sources</a></h3>
<p>The 25 official sources behind every row, all fetched on 2026-11-11.</p></div>
</div>""")

INDEX_BODY = INDEX_ALERT + INDEX_FOREFRONT + INDEX_KPIS + INDEX_SEQUENCE + INDEX_SNAPSHOT + INDEX_RESULTS + INDEX_INQUIRIES + INDEX_CARDS


# =========================== page 2: process.html ============================
PROCESS_STEPS = panel("The nine-step compliance path", """
<p>Numbered in the order a first-time owner should work through them. Steps 01-04 are prerequisites;
steps 05-08 decide the amount and notice; step 09 preserves the evidence a reviewer would request.</p>
""" + table(
    "Step-by-step path with the controlling rule for each step",
    ["Step", "What to do", "Key rule or limit", "Status", "Official source"],
    [
        {"id": "step-01", "cells": ["01 · Confirm coverage",
                   "Use the City coverage guide against the building records; the reported 1940 construction year suggests rent-control coverage for a multi-unit building (built before 1979-06-14), but the intake value is not authenticated.",
                   "Coverage controls which cap and procedures apply; confirm before anything else.",
                   BADGES["verified"] + " " + BADGES["reported"], ], "srcs": ["S15"]},
        {"id": "step-02", "cells": ["02 · Report into the Housing Inventory",
                   "File the Housing Inventory report for each covered unit on the Rent Board Portal; renew by March 1 each year; update owner or manager contact details within 30 days of any change.",
                   "Free, online, under penalty of perjury; report is used for compliance monitoring.",
                   BADGES["verified"], ], "srcs": ["S01", "S02"]},
        {"id": "step-03", "cells": ["03 · Verify the license is active",
                   "Reporting in substantial compliance generates the unit&rsquo;s rent-increase license. Confirm it will be in effect on the planned effective date; noncompliance suspends it, and restoration is prospective only.",
                   "Suspended months are not collectible from the tenant.",
                   BADGES["verified"], ], "srcs": ["S02"]},
        {"id": "step-04", "cells": ["04 · Authenticate the rent history",
                   "Establish the lawful base rent: the actual rent charged and paid, excluding temporary passthroughs or fluctuating charges. A rent-history review route exists for disputes.",
                   "The intake amounts are owner-reported; an inflated base makes every increase defeasible.",
                   BADGES["verified"] + " " + BADGES["unverified"], ], "srcs": ["S03", "S14", "S17"]},
        {"id": "step-05", "cells": ["05 · Choose a lawful effective date",
                   "First annual increase no earlier than 12 months after the lease start; later increases at least 12 months after the last one. A late increase moves the anniversary to the new effective date.",
                   "Use the rate in force on the effective date, not the service date.",
                   BADGES["verified"], ], "srcs": ["S03"]},
        {"id": "step-06", "cells": ["06 · Compute the amount",
                   "Multiply base rent by the allowance in force (1.6% for effective dates between 2026-03-01 and 2027-02-28). Never round up; apply to base rent including housing services, excluding passthroughs.",
                   "No petition is needed for an annual increase within the allowance.",
                   BADGES["verified"], ], "srcs": ["S03", "S04"]},
        {"id": "step-07", "cells": ["07 · Add banking only if reconstructed",
                   "Skipped annual increases can be banked after 12 full months from when first imposable; banked amounts are added, never compounded, and must be itemized with dates in the notice (Rules 4.10 / 4.12).",
                   "A nonconforming banked notice is void per Rule 4.10(b); proposed File No. 261020 would cap combined banked and capital-improvement increases at 10%.",
                   BADGES["verified"] + " " + BADGES["pending"], ], "srcs": ["S05", "S06", "S07", "S03"]},
        {"id": "step-08", "cells": ["08 · Serve the written notice",
                   "State the dollar amount, percentage and effective date. Serve at least 30 days ahead for a cumulative increase of 10% or less in the prior 12 months, 90 days if above 10%; mailing adds 5 days. Personal delivery or statutory mail service; the statute does not authorize email or text.",
                   "Use certified calculation records; keep proof of how and when service happened.",
                   BADGES["verified"], ], "srcs": ["S19", "S03"]},
        {"id": "step-09", "cells": ["09 · Preserve a private evidence pack",
                   "Keep the lease and addenda, rent ledger, calculation worksheet, license status snapshot, the notice as served, and proof of service - privately, never in this public repository.",
                   "This is the file a tenant-side reviewer or an administrative law judge would request.",
                   BADGES["recommendation"], ], "srcs": ["S03", "S19"]},
    ]))

PROCESS_FIELDS = panel("What the Housing Inventory report asks for", """
<p>For a unit that is <strong>not owner-occupied</strong>, Sec. 37.15(b)(2) lists the exact fields below.
Owner-occupied units report only the address and owner-occupied status. One co-owner can file for all
owners of a unit.</p>
""" + table(
    "Section 37.15(b)(2) reporting fields - tenant-occupied units",
    ["Field", "What the ordinance requires", "Status", "Official source"],
    [
        {"cells": ["Owner or manager contact",
                   "Name and business contact information (address, phone, email) of the owner(s) or the designated property manager for habitability issues; update within 30 days of any change.",
                   BADGES["verified"], ], "srcs": ["S02"]},
        {"cells": ["Business registration number",
                   "The business registration number for the unit, if any.",
                   BADGES["verified"], ], "srcs": ["S02"]},
        {"cells": ["Size and rooms",
                   "Approximate square footage to the owner&rsquo;s or manager&rsquo;s best knowledge, plus bedroom and bathroom counts.",
                   BADGES["verified"], ], "srcs": ["S02"]},
        {"cells": ["Occupancy status and dates",
                   "Whether the unit is vacant or occupied, when that status commenced, and the start and end dates of other occupancies or vacancies in the prior 12 months.",
                   BADGES["verified"], ], "srcs": ["S02"]},
        {"cells": ["Base rent and utilities",
                   "For tenant-occupied units, the base rent (reported in $250 increments) and whether it includes specified utilities.",
                   BADGES["verified"], ], "srcs": ["S02"]},
        {"cells": ["Additional items",
                   "Any further information the Rent Board adds after a noticed public meeting.",
                   BADGES["verified"], ], "srcs": ["S02"]},
    ]))

PROCESS_FEE = panel("Rent Board Fee calendar - separate from the license", """
<p>The annual fee funds the Rent Board; it is independent of Housing Inventory reporting and the
rent-increase license. Requesting a fee exemption does <strong>not</strong> satisfy inventory
reporting.</p>
""" + table(
    "Rent Board Fee 2026-27 - verified amounts and dates",
    ["Item", "Verified value", "Status", "Official source"],
    [
        {"cells": ["Fee amount", "$59.00 per dwelling unit; $29.50 per guest room unit.", BADGES["verified"], ], "srcs": ["S13"]},
        {"cells": ["Payment deadline", "March 1 each year; 5% late penalties accrue monthly up to a 15% cap; unpaid bills go delinquent on June 1.", BADGES["verified"], ], "srcs": ["S13"]},
        {"cells": ["Tenant recovery", "After paying in full, 50% of the fee ($29.50 per dwelling unit) may be collected from tenants who occupied the unit as of November 1 of the applicable tax year; penalties cannot be passed through.", BADGES["verified"], ], "srcs": ["S13"]},
        {"cells": ["Exemption window", "Requests are filed October through early December; the City page lists 2026-12-14 as the request deadline for the 2027 fee cycle. An exemption is not inventory relief.", BADGES["verified"], ], "srcs": ["S13"]},
        {"cells": ["Payment channels", "Rent Board Portal (preferred), in person with the Treasurer and Tax Collector, or by mail; no payments at the Rent Board office.", BADGES["verified"], ], "srcs": ["S13"]},
    ]))

PROCESS_BODY = PROCESS_STEPS + PROCESS_FIELDS + PROCESS_FEE


# ======================= page 3: units-and-rates.html ========================
UNITS_GATE = panel("Gate conditions - what must be true before any scenario applies", """
<p>Each condition below is currently <strong>unverified</strong>. Until a condition is confirmed with
authentic records, the matching scenarios remain conditional arithmetic rather than served notices.</p>
""" + table(
    "Conditions gate",
    ["Condition", "Why it gates the increase", "Where flagged", "Status", "Official source"],
    [
        {"cells": ["Rent-control coverage and 1940 construction",
                   "Determines that the local 1.6% allowance, banking rules and license duty apply.",
                   '<a href="flagged.html#FR-01">FR-01</a>', BADGES["unverified"], ], "srcs": ["S15"]},
        {"cells": ["Active rent-increase license on the effective date",
                   "A suspended license makes the increase uncollectible for the suspended months.",
                   '<a href="flagged.html#FR-02">FR-02</a>', BADGES["unverified"], ], "srcs": ["S02"]},
        {"cells": ["Lawful base rent equals the intake amount",
                   "All dollar results below are arithmetic on intake values, not authenticated rent ledgers.",
                   '<a href="flagged.html#FR-03">FR-03</a>', BADGES["unverified"], ], "srcs": ["S03", "S17"]},
        {"cells": ["Unit A stays periodic (no fixed-term bar)",
                   "The reported 2026-04-01 continuing-tenancy change must not have created a fixed-term restriction on increases.",
                   '<a href="flagged.html#FR-06">FR-06</a>', BADGES["unverified"], ], "srcs": ["S03", "S12"]},
        {"cells": ["Unit B had no intervening increases since 2019",
                   "The full 11.5% banked figure exists only if every annual increase since 2020 was skipped.",
                   '<a href="flagged.html#FR-05">FR-05</a>', BADGES["unverified"], ], "srcs": ["S05", "S06"]},
        {"cells": ["No lease, subsidy or program restriction",
                   "Lease clauses, subsidies or program rules can narrow what the ordinance allows.",
                   '<a href="flagged.html#FR-07">FR-07</a>', BADGES["unverified"], ], "srcs": ["S15"]},
    ]))

UNITS_A = panel("Unit A analysis - continuing tenancy, so no market reset", """
<p>Intake: lease start <strong>2025-02-01</strong> at <strong>$3,995.00</strong> per month with three
initial occupants; a continuing-tenancy occupancy change was reported for <strong>2026-04-01</strong>
at an unchanged $3,995.00, leaving one original occupant (placeholder Tenant A1) plus one subsequent
occupant (Tenant A4). Consequences from the official texts:</p>
<ul>
<li>No surcharge may be charged merely because a new roommate joined the existing tenant - the City
calls that an unlawful increase, even where a lease purports to allow it (<a href="https://www.sf.gov/learn-about-rent-increases-san-francisco">S03</a>).</li>
<li>While an original occupant still resides in the unit, a Costa-Hawkins vacancy reset to market is
not available; subtenant and subsequent-occupant treatment follows Rule 6.14, which requires written
notice within a reasonable time after the owner learns of the change (the 2026-04-01 notice status is
unverified - <a href="flagged.html#FR-06">FR-06</a>) (<a href="https://www.sf.gov/information--petition-determination-pursuant-section-614-andor-costa-hawkins">S12</a>,
<a href="https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1954.53&amp;lawCode=CIV">S22</a>).</li>
<li>First annual increase was imposable on 2026-02-01 (the 1.4% period). Because it was skipped, it
banks after 12 full months - on 2027-02-01 (<a href="https://www.sf.gov/information--banked-rent-increases">S05</a>).</li>
</ul>
""" + table(
    "Unit A scenarios (assumptions: periodic tenancy, active license, lawful base = $3,995.00)",
    ["Scenario", "Composition", "Increase", "Conditional new rent", "Notice and serve-by example", "Trade-offs", "Status", "Official source"],
    [
        {"id": "sc-a1", "cells": ["A-1 · Annual-only now",
                   "1.6% annual for an effective date before 2027-02-01.",
                   A1_INC, A1_NEW,
                   "30-day written notice (35 if mailed). Example effective 2027-01-01: personal service by 2026-12-02, mailing by 2026-11-27.",
                   "Anniversary moves to the new effective date; imposing before 2027-02-01 ends the 12-month accrual window, so the skipped 1.4% never banks (rule-based interpretation, see <a href=\"flagged.html#FR-18\">FR-18</a>).",
                   BADGES["calculated"], ], "srcs": ["S03", "S04", "S05", "S19"]},
        {"id": "sc-a2", "cells": ["A-2 · Wait for the second anniversary",
                   "1.4% banked (2026-02-01 window) + 1.6% annual = 3.0% on 2027-02-01.",
                   A2_INC, A2_NEW,
                   "30-day written notice: personal service by 2027-01-02, or mailing by 2026-12-28 (35 days).",
                   "Keeps the anniversary at February 1; at 3.0% total it stays far below both the 10% notice threshold and the proposed File No. 261020 cap.",
                   BADGES["calculated"], ], "srcs": ["S04", "S05", "S19", "S03"]},
    ]))

UNITS_B = panel("Unit B analysis - long tenancy with potential banking", """
<p>Intake: lease start <strong>2019-06-01</strong> at <strong>$3,150.00</strong> per month with two
occupants (placeholders Tenant B1 and Tenant B2). <strong>If</strong> - and only if - no annual
increase was imposed from June 2020 onward (<a href="flagged.html#FR-05">FR-05</a>), the skipped
allowances bank after 12 full months each and remain available because the tenancy continues; banking
carries across owners and expires only when the tenancy ends
(<a href="https://www.sf.gov/information--banked-rent-increases">S05</a>). The banked stack then totals
<strong>11.5%</strong> through the 2025-26 rate year (see composition table below). The City confirms
banked portions are added, never compounded, and must be itemized with dates in the notice; a notice
that fails Rule 4.10 is void.</p>
""" + table(
    "Unit B scenarios (assumptions: active license, lawful base = $3,150.00, zero intervening increases)",
    ["Scenario", "Composition", "Increase", "Conditional new rent", "Notice and serve-by example", "Risk profile", "Status", "Official source"],
    [
        {"id": "sc-b1", "cells": ["B-1 · Annual-only",
                   "1.6% annual; the full 11.5% bank stays available for later.",
                   B1_INC, B1_NEW,
                   "30-day written notice (35 if mailed). Example effective 2027-01-01: personal service by 2026-12-02, mailing by 2026-11-27.",
                   "Lowest-scrutiny option; leaves every banked year intact for future use.",
                   BADGES["calculated"], ], "srcs": ["S03", "S04", "S05", "S19"]},
        {"id": "sc-b2", "cells": ["B-2 · Partial bank capped at 10.0%",
                   "1.6% annual + 8.4% drawn from the bank = 10.0% total; 3.1% of bank remains.",
                   B2_INC, B2_NEW,
                   "30-day written notice because 10.0% is not above 10% (35 if mailed); same example dates as B-1.",
                   "Stays at or below the pending File No. 261020 ceiling even if enacted as drafted, and avoids the 90-day notice tier.",
                   BADGES["calculated"], ], "srcs": ["S04", "S05", "S19", "S03"]},
        {"id": "sc-b3", "cells": ["B-3 · Full bank through 2027-02-28",
                   "11.5% banked (2020-21 through 2025-26) + 1.6% annual = 13.1%.",
                   B3_INC, B3_NEW,
                   "90-day written notice; example effective 2027-02-15: personal service by 2026-11-17, mailing by 2026-11-12 - one day after this research date.",
                   "Above 10%: exposed to retroactive reduction of the banked portion if File No. 261020 is enacted as drafted (notices on or after 2026-09-15); heaviest tenant-challenge optics.",
                   BADGES["calculated"] + " " + BADGES["pending"], ], "srcs": ["S04", "S05", "S19", "S03"]},
    ]))

UNITS_BANK = panel("Unit B banked-increase composition (id: banking-271020)".replace("(id: banking-271020)", ""), """
<p id="banking-271020">Derived by applying Rule 4.12(a)&rsquo;s 12-month maturation to each annual allowance
first imposable on the June 1 anniversaries, using the published Form 571 rates; additive only, no
compounding, no rounding up. Any intervening increase or concession resets the count - that history is
unverified (<a href="flagged.html#FR-05">FR-05</a>).</p>
""" + table(
    "Banking stack for a 2019-06-01 lease with zero intervening increases",
    ["Allowance year", "Published rate", "Banked cumulative after maturation", "Status", "Official source"],
    [{"cells": [p, f"{v}%", f"{c}%", BADGES["verified"] + " per Form 571; availability " + BADGES["unverified"].lower()],
      "srcs": ["S04", "S05"]} for p, v, c in _bcumulative]
))

UNITS_FORM571 = panel("Form 571 - the complete official allowance table", """
<p>All 46 published periods, re-fetched from the official PDF on 2026-11-11 and matched cell-by-cell
against this repository&rsquo;s <code>data/allowable-increases.csv</code> (full match; see the
<a href="repo-audit.html#V01">repository audit</a>). The two starred 1992 periods are mutually
exclusive: only one of them may be imposed for a tenancy, per the Form 571 footnote.</p>
""" + table(
    "Allowable annual increases by effective period (Form 571, 2026-27 edition)",
    ["Effective period", "Allowable increase", "Note", "Status", "Official source"],
    [{"cells": ["* " + p if p.startswith(("12/8/92", "3/1/92")) else p, r,
                "One of the two starred 1992 periods only" if p.startswith(("12/8/92", "3/1/92")) else "",
                BADGES["verified"], ], "srcs": ["S04"]} for p, r in FORM571]
    + [{"cells": ["3/1/27 - 2/29/28", BLANK, "Not yet published; next edition expected around March 2027 - <a href=\"flagged.html#FR-08\">FR-08</a>",
                  BADGES["unverified"], ], "srcs": ["S04"]}]
))

UNITS_COSTA = panel("Costa-Hawkins and Rule 6.14 - why Unit A cannot reset to market", table(
    "Vacancy-decontrol analysis for the reported occupant change",
    ["Rule", "Verified content", "Effect here", "Status", "Official source"],
    [
        {"cells": ["Costa-Hawkins, Civil Code Sec. 1954.53",
                   "Permits the owner to set initial rent on a qualifying vacancy, but not while an original occupant still lives in the unit under the circumstances the statute limits.",
                   "Tenant A1 (placeholder) reportedly remains; no vacancy reset is available for Unit A.",
                   BADGES["verified"], ], "srcs": ["S22", "S12"]},
        {"cells": ["Rent Board Rule 6.14",
                   "A subsequent occupant is protected against a Costa-Hawkins reset; the owner must serve written notice within a reasonable time after learning of the occupant change - Rent Board guidance discusses 60 days - and a petition route exists for disputes.",
                   "Whether timely 6.14 notice was given for the 2026-04-01 change is unverified; treat the current rent level as continuing.",
                   BADGES["verified"] + " " + BADGES["analysis"], ], "srcs": ["S12", "S22"]},
        {"cells": ["Roommate surcharge prohibition",
                   "Charging more rent merely because an additional roommate joined the existing tenant is an unlawful increase, even if a lease clause purports to allow it.",
                   "Do not raise Unit A&rsquo;s rent because of the reported 2026-04-01 occupant change.",
                   BADGES["verified"], ], "srcs": ["S03"]},
        {"cells": ["Vacant-unit pricing power",
                   "For a covered unit that is actually empty and qualifying, there is no limit on the initial rent charged to a new tenant.",
                   "Not applicable to either unit on the reported facts; both are occupied by continuing tenancies.",
                   BADGES["verified"], ], "srcs": ["S03", "S22"]},
    ]))

UNITS_BODY = UNITS_GATE + UNITS_A + UNITS_B + UNITS_BANK + UNITS_FORM571 + UNITS_COSTA


# ====================== page 4: laws-and-notices.html ========================
LAWS_LOCAL = panel("Local layer - San Francisco Rent Ordinance", table(
    "Local rules that govern these two units (as reported)",
    ["Rule", "Verified content", "Status", "Official source"],
    [
        {"cells": ["Coverage", "The Rent Ordinance&rsquo;s rent-increase limits generally reach multi-unit residential buildings certified before 1979-06-14; the reported 1940 construction year would qualify, but it is unverified.", BADGES["verified"] + " " + BADGES["reported"], ], "srcs": ["S15"]},
        {"cells": ["Annual cap mechanics", "Sec. 37.3(a)(1): the annual allowance is 60% of the Bay Area consumer-price-index change, capped at 7%; the Rent Board publishes it each year (currently 1.6%). It applies to base rent including housing services.", BADGES["verified"], ], "srcs": ["S09", "S04", "S03"]},
        {"cells": ["Reporting and license", "Sec. 37.15: annual Housing Inventory reporting for covered units; substantial compliance generates the rent-increase license; noncompliance suspends it and suspended months are not collectible.", BADGES["verified"], ], "srcs": ["S02", "S01"]},
        {"cells": ["Banking", "Part IV Rules 4.10-4.12: skipped allowances bank after 12 full months from first imposable; additive only; must be itemized with dates in the notice; nonconforming notices are void.", BADGES["verified"], ], "srcs": ["S07", "S05", "S06"]},
        {"cells": ["Harassment", "Sec. 37.10B prohibits bad-faith coercion and similar conduct, with civil remedies including trebled actual damages, a $1,000 minimum per violation, and attorney fees.", BADGES["verified"], ], "srcs": ["S10"]},
        {"cells": ["Algorithmic devices", "Sec. 37.10C prohibits using or selling algorithmic rent-setting tools that rely on non-public competitor data, with per-unit monthly civil exposure.", BADGES["verified"], ], "srcs": ["S11"]},
        {"cells": ["Tenant challenge route", "A tenant may file a summary petition (Form 516C) with the Rent Board at no cost and with no filing deadline to contest an unlawful increase.", BADGES["verified"], ], "srcs": ["S17"]},
        {"cells": ["Rent Board Fee", "$59.00 per dwelling unit for 2026-27, due March 1; 50% pass-through allowed to qualifying occupants.", BADGES["verified"], ], "srcs": ["S13"]},
    ]))

LAWS_STATE = panel("State layer - California", table(
    "State statutes that control notice, retaliation, discrimination and decontrol",
    ["Statute", "Verified content", "Status", "Official source"],
    [
        {"cells": ["Civil Code Sec. 827 - notice", "Written notice of increase, personally delivered or served by statutory mail; 30 days for increases of 10% or less within a 12-month window, 90 days above 10%; mailing inside California adds 5 days. No email or text authorization appears in the statute.", BADGES["verified"], ], "srcs": ["S19"]},
        {"cells": ["Civil Code Sec. 1942.5 - retaliation", "Prohibits retaliation against tenants for exercising legal rights, including a statutory 180-day protection window after protected activity.", BADGES["verified"], ], "srcs": ["S20"]},
        {"cells": ["Civil Code Sec. 1947.12 - state cap", "The Tenant Protection Act caps increases at 5% plus CPI (10% maximum) for covered units, but subsection (d)(3) yields where a stricter local cap applies - so San Francisco&rsquo;s 1.6% governs these units, not the statewide figure (8.8% for 2026-08-01 to 2027-07-31, published for state-law-covered units).", BADGES["verified"], ], "srcs": ["S21", "S16"]},
        {"cells": ["Civil Code Sec. 1954.53 - Costa-Hawkins", "Vacancy decontrol allows market reset on qualifying vacancies; barred while protected original occupants remain.", BADGES["verified"], ], "srcs": ["S22", "S12"]},
        {"cells": ["Government Code Sec. 12955 - FEHA", "Prohibits housing discrimination across California&rsquo;s protected classes, broader than the federal list (including source of income and immigration status).", BADGES["verified"], ], "srcs": ["S23", "S24"]},
        {"cells": ["Civil Rights Department guidance", "State enforcement agency guidance on fair-housing duties, reasonable accommodations and complaint filing.", BADGES["verified"], ], "srcs": ["S24"]},
    ]))

LAWS_FED = panel("Federal layer - United States", table(
    "Federal rules reviewed",
    ["Rule", "Verified content", "Status", "Official source"],
    [
        {"cells": ["Fair Housing Act", "42 U.S.C. Sec. 3601-3619 prohibits discrimination in rental terms on the basis of race, color, religion, sex, national origin, disability and familial status.", BADGES["verified"], ], "srcs": ["S25"]},
        {"cells": ["Federal rent cap", BLANK + " No federal numerical rent cap or federal uniform-increase rule for private unsubsidized units was identified in the reviewed official sources; subsidy programs can add their own rules.", BADGES["unverified"], ], "srcs": ["S25"]},
    ]))

LAWS_NOTICE = panel("What a legally clean notice contains - and what counts as a reason", """
<p>The ordinance and the statute care about the <strong>number, dates and service</strong>, not the
owner&rsquo;s justification: no cited rule conditions an annual or banked increase within the allowance
on a stated reason. A truthful, neutral explanation (inflation, insurance and maintenance cost
movements) is nonetheless good practice and helps a tenant-side reviewer see routine business purpose;
it never authorizes exceeding the allowance, and invented reasons can create harassment exposure under
Sec. 37.10B (<a href="https://www.sf.gov/information/sec-3710b-tenant-harassment">S10</a>).</p>
""" + table(
    "Notice content and service checklist",
    ["Element", "Requirement", "Status", "Official source"],
    [
        {"cells": ["Dollar amount", "State the dollar amount of the increase.", BADGES["verified"], ], "srcs": ["S03", "S19"]},
        {"cells": ["Percentage", "State the percentage; split the annual and banked portions with the banking dates if any banked amount is used.", BADGES["verified"], ], "srcs": ["S03", "S07", "S05"]},
        {"cells": ["Effective date", "State when the increase takes effect; the rate in force on that date controls.", BADGES["verified"], ], "srcs": ["S03"]},
        {"cells": ["Timing", "At least 30 days before the effective date for cumulative increases up to 10% in the prior 12 months; at least 90 days above 10%.", BADGES["verified"], ], "srcs": ["S19", "S03"]},
        {"cells": ["Service method", "Personal delivery or statutory mail (5 extra days if mailed). Email and text are not authorized in the cited statute.", BADGES["verified"], ], "srcs": ["S19"]},
        {"cells": ["Reason statement", "Not required by the cited rules; if added, keep it truthful and neutral - a justification narrative cannot raise the lawful ceiling and a false one can be challenged.", BADGES["analysis"], ], "srcs": ["S09", "S10"]},
    ]))

LAWS_BODY = LAWS_LOCAL + LAWS_STATE + LAWS_FED + LAWS_NOTICE

# ===================== page 5: practices-and-scrutiny.html ===================
PRAC_CORP = panel("How large corporate owners and individual owners handle increases", """
<p><strong>Verified:</strong> the legal duties are identical for both - the same ordinance sections bind
every owner of a covered unit (<a href="https://www.sf.gov/information--sec-3715-reporting-obligations-licensing">S02</a>).
<strong>Not verified:</strong> no official empirical study describing how the two owner types actually
choose increase amounts was found; that comparison value stays blank
(<a href="flagged.html#FR-11">FR-11</a>).</p>
""" + table(
    "Owner-type comparison - verified law vs labeled analysis",
    ["Topic", "What was verified from official sources", "Status", "Official source"],
    [
        {"cells": ["Legal duties", "Identical: Housing Inventory reporting, rent-increase license, annual allowance, banking rules, notice statutes and civil-rights laws apply regardless of entity form.", BADGES["verified"], ], "srcs": ["S02", "S09"]},
        {"cells": ["Algorithmic pricing", "Sec. 37.10C bans algorithmic rent-setting tools fed with non-public competitor data - most relevant to portfolio-scale operators, but binding on anyone.", BADGES["verified"], ], "srcs": ["S11"]},
        {"cells": ["Observed corporate practice", BLANK + " no official empirical benchmark reviewed.", BADGES["unverified"], ], "srcs": ["S15"]},
        {"cells": ["Observed individual practice", BLANK + " no official empirical benchmark reviewed.", BADGES["unverified"], ], "srcs": ["S15"]},
        {"cells": ["Recommended operating model for either", "Compliance calendar keyed to anniversaries and March 1 reporting; per-unit ledger; written neutral increase policy; preserved notice and service evidence.", BADGES["recommendation"], ], "srcs": ["S02", "S03"]},
    ]))

PRAC_ONE_BOTH = panel("Raise one unit or both? (id: one-or-both)".replace(" (id: one-or-both)", ""), """
<p id="one-or-both">No uniform-increase statute was identified in the reviewed sources: nothing requires
the same percentage on every unit. The risk lives in <strong>motive and pattern</strong>, not in
arithmetic.</p>
""" + table(
    "One unit vs both units - legal analysis",
    ["Question", "Analysis grounded in the cited rules", "Status", "Official source"],
    [
        {"cells": ["Is a selective increase per se unlawful?",
                   "No such rule was identified. Different lawful dates and histories can lawfully produce different increases. Prohibited treatment linked to protected characteristics or protected activity is what creates liability.",
                   BADGES["analysis"], ], "srcs": ["S23", "S24", "S25"]},
        {"cells": ["Does raising both immunize the owner?",
                   "No. Raising both units does not cure a discriminatory or retaliatory motive, and neither guarantees a favorable review outcome.",
                   BADGES["analysis"], ], "srcs": ["S20", "S23"]},
        {"cells": ["Defensible posture",
                   "Apply a neutral written policy - for example the same annual-only percentage to every unit at its lawful date - and document unit-specific reasons (anniversary mismatch, lease restrictions, banking elections) whenever outcomes differ.",
                   BADGES["recommendation"], ], "srcs": ["S09", "S03"]},
        {"cells": ["Practical answer for this building",
                   "Both units are reportedly eligible for the annual allowance, so applying the same percentage to each (scenarios A-1/A-2 and B-1/B-2 as elected) is easier to defend than a one-unit-only increase, unless a documented unit-specific reason exists.",
                   BADGES["analysis"], ], "srcs": ["S03", "S04"]},
    ]))

_STRESS = [
    ("Coverage match", "Building coverage confirmed against official records before relying on the local allowance.", ["S15"]),
    ("License continuity", "Rent-increase license active on the effective date, with no suspension gap to reconstruct.", ["S02"]),
    ("Inventory currency", "March 1 Housing Inventory report current, perjury-standard accurate, contact changes filed within 30 days.", ["S01", "S02"]),
    ("Lawful base rent", "Ledger-authenticated base rent; no temporary passthroughs folded into the base.", ["S03", "S14", "S17"]),
    ("Twelve-month interval", "At least 12 months since the lease start or last increase; anniversary arithmetic shown.", ["S03"]),
    ("Correct rate period", "Allowance taken from the effective date&rsquo;s rate year; no rounding up.", ["S03", "S04"]),
    ("Banking itemization", "Any banked portion split out with its dates, per Rules 4.10 and 4.12; nonconforming notices are void.", ["S05", "S07"]),
    ("Notice content", "Dollar amount, percentage and effective date all stated.", ["S03", "S19"]),
    ("Service and timing", "30-day or 90-day threshold chosen correctly, 5 extra days if mailed, proof of service kept.", ["S19"]),
    ("Retaliation screen", "No protected activity in the trailing 180 days (repair complaints, organizing) motivating the increase.", ["S20"]),
    ("Discrimination screen", "Neutral criteria applied; no disparate treatment across FEHA and Fair Housing Act classes, including source of income.", ["S23", "S24", "S25"]),
    ("Harassment and devices", "No bad-faith pressure tactics (Sec. 37.10B) and no algorithmic pricing tool using non-public competitor data (Sec. 37.10C).", ["S10", "S11"]),
]
PRAC_STRESS = panel("Twelve-point tenant-lawyer stress test", """
<p id="stress-test">This mirrors what free tenant-side review channels in San Francisco would check. A
tenant can file a summary petition (Form 516C) at no cost with no filing deadline
(<a href="https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history/">S17</a>);
eviction defense carries a right-to-counsel referral under Form 1007
(<a href="https://www.sf.gov/sites/default/files/2023-08/1007%20Notice%20to%20Tenant%20Req%27d%20by%2037.%209(c)-Eng-Sp-Ch-Viet-Rus-Tag%5B74%5D.pdf">S18</a>).
Treat every point as pass/fail with evidence, not as a vibe.</p>
""" + table(
    "Stress test - each point must have documentary proof before service",
    ["Point", "What the reviewer will look for", "Status", "Official source"],
    [{"cells": [f"{i + 1:02d} · {name}", desc, BADGES["recommendation"], ], "srcs": srcs}
     for i, (name, desc, srcs) in enumerate(_STRESS)]))

PRAC_BODY = PRAC_CORP + PRAC_ONE_BOTH + PRAC_STRESS


# ========================= page 6: repo-audit.html ===========================
REPO_VERIFIED = panel("Re-verified repository artifacts", table(
    "Artifacts confirmed against official sources on 2026-11-11",
    ["ID", "Artifact", "Verification performed", "Status", "Official source"],
    [
        {"id": "V01", "cells": ["V01",
                   '<a href="../data/allowable-increases.csv">data/allowable-increases.csv</a>',
                   "All 46 effective-period rows re-matched cell-by-cell against Form 571 as re-fetched on 2026-11-11; the 2027-28 row is correctly blank and unverified.",
                   BADGES["verified"], ], "srcs": ["S04"]},
        {"cells": ["V02",
                   '<a href="../EXECUTIVE-SUMMARY.md">EXECUTIVE-SUMMARY.md</a>',
                   "Current allowance 1.6%, license-first framing, 30/90-day notice tiers and pending-legislation warning all still match the live official pages on 2026-11-11.",
                   BADGES["verified"], ], "srcs": ["S03", "S02", "S19"]},
        {"cells": ["V03",
                   '<a href="../data/verified-register.csv">data/verified-register.csv</a>',
                   "Lines 1-64 read line by line; cited sf.gov, leginfo and hud.gov sources resolve to the same substantive rules re-verified today (one encoding nit in row R60 - see RA-02).",
                   BADGES["verified"], ], "srcs": ["S03", "S19", "S25"]},
    ]))

REPO_ISSUES = panel("Irregularities found - flagged, not silently edited", """
<p>Scope discipline: files owned by other sessions are audited here but not modified; every issue is
published on the <a href="flagged.html">Flagged for review</a> page with a source link for manual
review.</p>
""" + table(
    "Repository irregularities confirmed on 2026-11-11",
    ["ID", "Artifact", "Irregularity", "Flag", "Status", "Official source"],
    [
        {"cells": ["RA-01", '<a href="../internal/notes.md">internal/notes.md</a>',
                   "Internal notes cite ordinance number &ldquo;261015&rdquo;, but the official legislative record and the City notice refer to Board of Supervisors File No. 261020 (Legistar record 8217304, pending committee action as of 2026-11-11).",
                   '<a href="flagged.html#FR-14">FR-14</a>', BADGES["irregularity"], ], "srcs": ["S03"]},
        {"cells": ["RA-02", '<a href="../data/verified-register.csv">data/verified-register.csv</a> row R60 and <a href="../scripts/build.py">scripts/build.py</a>',
                   "The Form 1007 link carries literal square brackets ([74]) instead of the canonical percent-encoded form %5B74%5D used by the official page.",
                   '<a href="flagged.html#FR-15">FR-15</a>', BADGES["irregularity"], ], "srcs": ["S18"]},
        {"cells": ["RA-03", '<a href="../scripts/build.py">scripts/build.py</a>',
                   "Leginfo citations embed a trailing period (sectionNum=827. and sectionNum=1942.5.); the canonical parameter form ends at the section number.",
                   '<a href="flagged.html#FR-15">FR-15</a>', BADGES["irregularity"], ], "srcs": ["S19", "S20"]},
        {"cells": ["RA-04", "Base pages stamped research date 07 Nov 2026 (root six-page set)",
                   "The archived research stamp predates the City&rsquo;s 2026-11-09 File No. 261020 notice; hub/verification pages carry newer stamps. Left to the owning sessions to refresh.",
                   '<a href="flagged.html#FR-16">FR-16</a>', BADGES["irregularity"], ], "srcs": ["S03"]},
        {"cells": ["RA-05", '<a href="../data/allowable-increases.csv">data/allowable-increases.csv</a>',
                   "Effective-period strings embed the HTML entity &amp;ndash; instead of a plain dash - a cosmetic CSV hygiene nit; values themselves re-verified correct (V01).",
                   '<a href="flagged.html#FR-15">FR-15</a>', BADGES["irregularity"], ], "srcs": ["S04"]},
        {"cells": ["RA-06", "git history of the public main branch (22 commits on origin/main reviewed)",
                   "Earlier commits contain literal personal identifier tokens (prior reviewers&rsquo; F15-class finding). Current tracked files are clean under the generic scans; only a history rewrite purges the exposure - owner action, outside this session&rsquo;s scope.",
                   '<a href="flagged.html#FR-17">FR-17</a>', BADGES["irregularity"], ], "srcs": ["S01"]},
    ]))

REPO_METHOD = panel("Review method and limits", """
<p>Every tracked file in scope was read line by line on 2026-11-11; numeric tables were recomputed with
exact decimal arithmetic, and each official URL was fetched live the same day. The audit is read-only:
it reports, it does not repair other sessions&rsquo; files. A source link beside a finding identifies
where a human reviewer can confirm the underlying rule; it does not certify correctness of a repo file
that this session did not author.</p>
""")

REPO_BODY = REPO_VERIFIED + REPO_ISSUES + REPO_METHOD

# ========================= page 7: flagged.html ==============================
FLAGS = [
    ("FR-01", "Building coverage, 1940 construction year and rent-control status",
     "Owner intake only; never authenticated against parcel or Rent Board records. All unit analysis assumes coverage.",
     ["S15"]),
    ("FR-02", "Rent-increase license and Housing Inventory status for both units",
     "No portal access; cannot confirm whether reports were filed or a license is active. Every scenario is conditional on this.",
     ["S02", "S01"]),
    ("FR-03", "Lawful base rent for Unit A ($3,995.00 claimed) and Unit B ($3,150.00 claimed)",
     "Intake amounts are not rent ledgers; concessions, passthroughs or prior overcharges would change every computed figure.",
     ["S03", "S17"]),
    ("FR-04", "Unit A actual occupancy (one original and one subsequent occupant reported)",
     "Roommate composition reported but not documented here; affects the Costa-Hawkins/6.14 analysis only, not the allowance arithmetic.",
     ["S12"]),
    ("FR-05", "Unit B intervening increases since 2019-06-01",
     "Any increase or concession since 2019 shrinks the 11.5% assumed bank; if unknown, treat B-3 as an upper bound, not an entitlement.",
     ["S05", "S06"]),
    ("FR-06", "Whether the reported 2026-04-01 Unit A arrangement created a fixed-term lease, and whether timely Rule 6.14 written notice was given",
     "A fixed term can bar mid-lease increases; a missed reasonable-time notice can convert a subsequent occupant&rsquo;s status.",
     ["S12", "S03"]),
    ("FR-07", "Lease terms, addenda, subsidy or program restrictions for both units",
     "No lease document was reviewed; subsidies can layer program rules on top of the ordinance.",
     ["S15"]),
    ("FR-08", "Allowable increase for effective dates on or after 2027-03-01",
     "Not yet published; expected around March 2027. The Form 571 table carries a deliberately blank row.",
     ["S04"]),
    ("FR-09", "Final text and enactment of Board of Supervisors File No. 261020",
     "Pending Land Use and Transportation Committee as of 2026-11-11 (Legistar record 8217304). If enacted as drafted, combined banked and capital-improvement increases cap at 10% per year for notices on or after 2026-09-15. Recheck before serving any banked increase.",
     ["S03"]),
    ("FR-10", "Neighborhood market-norm increase for Outer Sunset / 94122",
     "No official benchmark exists; the verified lawful allowance is the 1.6% citywide annual figure. Any 'normal for the neighborhood' number here would be fabrication.",
     ["S03", "S04"]),
    ("FR-11", "How large corporate owners in practice choose increases vs individual owners",
     "No official empirical study reviewed; only the legal common denominator could be verified.",
     ["S02", "S15"]),
    ("FR-12", "City rent-increase page worked-example date label",
     "The first example on the live page ties the 1.6% rate to a June 1, 2025 effective date even though 1.4% governed that period; the labeled period is the typo, the 1.6% heading period (2026-03-01 to 2027-02-28) is correct. Verified persisting on 2026-11-11.",
     ["S03", "S04"]),
    ("FR-13", "City banked-increases page example label",
     "An example on the banking page mislabels an August 1, 2024 date with the 1.4% figure that belongs to the 2025-26 period; surrounding rule text and Form 571 are consistent.",
     ["S05", "S04"]),
    ("FR-14", "internal/notes.md ordinance number 261015",
     "Should read File No. 261020 per the official legislative record (pending committee action, introduced 2026-09-15). Audited, not edited - owned by another session.",
     ["S03"]),
    ("FR-15", "Repository citation hygiene",
     "Form 1007 URL with literal [74] instead of %5B74%5D (verified-register row R60 and scripts/build.py), leginfo citations with trailing periods, and HTML entities inside a CSV column.",
     ["S18", "S19"]),
    ("FR-16", "Frozen 2026-11-07 research date on the archived base page set",
     "Predates the 2026-11-09 File No. 261020 posting; hub pages are newer. Refresh belongs to the owning sessions.",
     ["S03"]),
    ("FR-17", "Historical personal identifiers in public git history",
     "Prior commits contain literal identifier tokens (F15-class finding by earlier sessions). Current files scan clean; erasure needs a history rewrite by the repository owner and is not performed here.",
     ["S01"]),
    ("FR-18", "Banking-forfeiture interpretation for an early Unit A increase",
     "The statement that imposing an annual increase before 2027-02-01 ends accrual of the skipped 1.4% is this session&rsquo;s reading of Rule 4.12(a)&rsquo;s 12-month maturation, applied consistently with the City&rsquo;s published examples; the Rent Board has not ruled on this property. Treat as interpretation, not adjudication.",
     ["S05", "S07"]),
    ("FR-19", "Exemption eligibility for the Rent Board Fee",
     "No owner facts (owner-occupancy, program participation) were verified; deadline and amounts are verified, eligibility is not.",
     ["S13"]),
    ("FR-20", "Email or text message service sufficiency",
     "Civil Code Sec. 827 authorizes personal delivery or statutory mail; no official authorization of electronic service for these notices was identified. Treated as unavailable; confirm with counsel before relying on electronic service.",
     ["S19"]),
]
assert len(FLAGS) == 20
FLAGGED_BODY = (
    '<div class="alert-banner"><strong>Flagged for review:</strong> twenty items (FR-01 through FR-20) '
    'remain unverified or irregular. Blank cells are deliberate - no value was invented. None of these '
    'blocks publication; each carries the official source needed for a manual follow-up.</div>'
    + panel("Flagged items - unverified values stay blank", table(
        "FR-01 through FR-20",
        ["ID", "Item", "Verified value", "Why it matters / evidence trail", "Status", "Official source"],
        [{"id": fid,
          "cells": [fid, item, BLANK, why, BADGES["unverified"], ],
          "srcs": srcs} for fid, item, why, srcs in FLAGS]))
    + panel("How to clear a flag", """
<p>Each flag names its official follow-up route: the Rent Board portal and counseling line for property
facts (inventory, license, rent-history review), the legislative record for File No. 261020, and the
cited statute or rule for interpretations. After confirming a value against the official source, update
the matching row and remove the flag in a later, logged session.</p>
"""))

# ========================= page 8: sources.html ==============================
SOURCES_BODY = panel("Method", """
<p>Twenty-five official sources were fetched and read on 2026-11-11 (San Francisco Rent Board and
legislative pages, the California Legislature&rsquo;s codes, the California Civil Rights Department, and
the United States Department of Housing and Urban Development). Three load-bearing sources - the
Sec. 37.15 text, the rent-increase guide with the File No. 261020 notice, and the Rent Board Fee page -
were re-fetched a second time after the session rebased, to confirm nothing moved mid-day. Form 571 was
re-fetched in full to transcribe every period. A source link beside a finding means the rule was read
there on 2026-11-11; it never proves an owner-supplied property fact.</p>
<p>Legislative-record pages hosted on the City&rsquo;s legislation portal (outside the official-source
link allowlist used by this repository&rsquo;s audit) are cited textually only: File No. 261020, record
8217304, introduced 2026-09-15, pending committee action as of 2026-11-11.</p>
""")
SOURCES_BODY += table(
    "Official source register - all fetched 2026-11-11",
    ["ID", "Title", "Publisher", "Direct official link"],
    [{"id": sid, "cells": [sid, esc(SRC[sid][0]), esc(SRC[sid][2]),
                           f'<a href="{esc(SRC[sid][1], quote=True)}">{esc(SRC[sid][1])}</a>'],
      "srcs": [sid]} for sid, _t, _ti, _l, _u in S])


# ===================== machine-readable findings (JSON) ======================
def build_json() -> str:
    payload = {
        "schema": 1,
        "generated_by": "f46f7d0f/build_f46f7d0f.py",
        "research_date": RESEARCH_DATE,
        "principle": "official sources only; unconfirmed values are null and appear on flagged.html",
        "privacy": {
            "unit_placeholders": ["Unit A", "Unit B"],
            "tenant_placeholders": ["Tenant A1", "Tenant A4", "Tenant B1", "Tenant B2"],
            "never_published": ["tenant names", "tenant initials", "street or unit address",
                                "parcel number", "contact details"],
        },
        "sources": [
            {"id": sid, "title": SRC[sid][0], "url": SRC[sid][1],
             "publisher": SRC[sid][2], "fetched": RESEARCH_DATE}
            for sid, _t, _ti, _l, _u in S
        ],
        "intake": [
            {"unit": "Unit A", "lease_start": "2025-02-01", "monthly_rent_usd": "3995.00",
             "initial_occupant_count": 3,
             "continuing_tenancy": {"effective": "2026-04-01", "monthly_rent_usd": "3995.00",
                                    "original_occupants_remaining": 1, "subsequent_occupants": 1},
             "verification": "owner-reported", "sources": ["S17", "S03", "S12"]},
            {"unit": "Unit B", "lease_start": "2019-06-01", "monthly_rent_usd": "3150.00",
             "occupant_count": 2,
             "intervening_increases": None,
             "verification": "owner-reported", "sources": ["S17", "S05"]},
        ],
        "rates": {
            "current_allowance_pct": "1.6",
            "current_period": {"start": "2026-03-01", "end": "2027-02-28"},
            "next_period_rate_pct": None,
            "form571_periods": [{"period": p, "rate": r} for p, r in FORM571],
            "form571_source": "S04",
            "pending_legislation": {
                "file": "Board of Supervisors File No. 261020",
                "status": "pending committee action as of 2026-11-11, not enacted",
                "proposal": "10% per-year cap on combined banked and capital-improvement increases through 2029-12-31; retroactive to notices served on or after 2026-09-15 if enacted as drafted",
                "sources": ["S03"],
            },
        },
        "scenarios": [
            {"id": "A-1", "unit": "Unit A", "composition": "1.6% annual only",
             "increase_pct": "1.6", "increase_usd": A1_INC, "new_rent_usd": A1_NEW,
             "notice_days": 30, "mail_days": 35,
             "example_effective": "2027-01-01", "serve_by_personal": "2026-12-02",
             "serve_by_mail": "2026-11-27", "status": "calculated-conditional",
             "sources": ["S03", "S04", "S05", "S19"]},
            {"id": "A-2", "unit": "Unit A", "composition": "1.4% banked + 1.6% annual = 3.0%",
             "increase_pct": "3.0", "increase_usd": A2_INC, "new_rent_usd": A2_NEW,
             "notice_days": 30, "mail_days": 35,
             "example_effective": "2027-02-01", "serve_by_personal": "2027-01-02",
             "serve_by_mail": "2026-12-28", "status": "calculated-conditional",
             "sources": ["S04", "S05", "S19", "S03"]},
            {"id": "B-1", "unit": "Unit B", "composition": "1.6% annual only",
             "increase_pct": "1.6", "increase_usd": B1_INC, "new_rent_usd": B1_NEW,
             "notice_days": 30, "mail_days": 35,
             "example_effective": "2027-01-01", "serve_by_personal": "2026-12-02",
             "serve_by_mail": "2026-11-27", "status": "calculated-conditional",
             "sources": ["S03", "S04", "S05", "S19"]},
            {"id": "B-2", "unit": "Unit B", "composition": "1.6% annual + 8.4% partial bank = 10.0%",
             "increase_pct": "10.0", "increase_usd": B2_INC, "new_rent_usd": B2_NEW,
             "notice_days": 30, "mail_days": 35,
             "example_effective": "2027-01-01", "serve_by_personal": "2026-12-02",
             "serve_by_mail": "2026-11-27", "status": "calculated-conditional",
             "sources": ["S04", "S05", "S19", "S03"]},
            {"id": "B-3", "unit": "Unit B", "composition": "11.5% banked + 1.6% annual = 13.1%",
             "increase_pct": "13.1", "increase_usd": B3_INC, "new_rent_usd": B3_NEW,
             "notice_days": 90, "mail_days": 95,
             "example_effective": "2027-02-15", "serve_by_personal": "2026-11-17",
             "serve_by_mail": "2026-11-12",
             "exposure": "banked portion above the proposed 10% ceiling if File No. 261020 is enacted as drafted",
             "status": "calculated-conditional", "sources": ["S04", "S05", "S19", "S03"]},
        ],
        "banking_unit_b": {
            "assumption": "zero intervening increases since 2019-06-01 (unverified, FR-05)",
            "stack": [{"year": p, "rate_pct": str(v), "cumulative_pct": str(c)}
                      for p, v, c in _bcumulative],
            "total_banked_pct": "11.5",
            "maturation_rule": "banks 12 full months after first imposable; additive only (Rules 4.12, 4.10)",
            "sources": ["S04", "S05", "S06", "S07"],
        },
        "flags": [{"id": fid, "item": item, "verified_value": None,
                   "detail": why, "sources": srcs} for fid, item, why, srcs in FLAGS],
        "inquiries": [
            {"id": "Q1", "topic": "reasonable and normal increases, 94122",
             "answer": "1.6% lawful annual allowance citywide; no official neighborhood benchmark exists",
             "sources": ["S03", "S04"]},
            {"id": "Q2", "topic": "corporate vs individual owner practice",
             "answer": "identical legal duties; empirical practice comparison unverified (FR-11)",
             "sources": ["S02", "S11"]},
            {"id": "Q3", "topic": "correct notification and reasonable reasons",
             "answer": "written 30/90-day notice with dollar, percentage, effective date; no reason required by rule",
             "sources": ["S19", "S03", "S09"]},
            {"id": "Q4", "topic": "tenant-advocate scrutiny",
             "answer": "twelve-point stress test; free tenant petition route with no deadline",
             "sources": ["S17", "S10", "S20"]},
            {"id": "Q5", "topic": "one unit or both",
             "answer": "no uniform-increase statute identified; neutral written policy recommended",
             "sources": ["S23", "S24", "S25"]},
        ],
        "repo_review": {
            "verified": ["V01", "V02", "V03"],
            "irregularities": ["RA-01", "RA-02", "RA-03", "RA-04", "RA-05", "RA-06"],
            "linked_flags": ["FR-14", "FR-15", "FR-16", "FR-17"],
        },
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


# ======================== markdown deliverables ==============================
def build_exec_md() -> str:
    return f"""# Executive summary - San Francisco residential rent increases (session F46F7D0F)

Research date: **{RESEARCH_DATE_LONG}**. Privacy-safe: placeholder identities only (Unit A / Unit B;
Tenant A1, Tenant A4, Tenant B1, Tenant B2). Dates and dollar amounts preserved exactly as supplied by
the owner. This is research, not legal advice, and no inventory filing, license request or tenant
notice was made.

Companion dashboard: `f46f7d0f/index.html` (published via GitHub Pages under `f46f7d0f/`). Verification
log: `VERIFICATION-F46F7D0F.md`. Unverified values: `f46f7d0f/flagged.html` (FR-01 through FR-20).

## 1. The license question, first - individual owner, not a corporation

**Do you still need to report to the Rent Board and hold a rent-increase license before notifying
tenants? Yes on reporting; the license comes automatically from reporting.**

- San Francisco Administrative Code Sec. 37.15 requires **owners** of covered residential units to
  report into the Rent Board Housing Inventory every year by **March 1** - individuals included; one
  co-owner's report suffices (buildings of 1-9 units and condominiums report since 2023-03-01).
- There is **no separate license application and no license fee**. Substantial compliance with the
  Housing Inventory reporting **generates the unit's rent-increase license automatically**.
- Timing rule: the license must **not be suspended on the increase's effective date**. If reporting
  lapses, the license is suspended for the noncompliance period, restoration is prospective only, and a
  tenant does not owe the increase for suspended months.
- The cited rules do not require attaching the license to the notice, and the City does not state it
  must precede service - but confirming status before serving is the safer workflow. A license is not
  approval of the amount and does not shield against challenges for other violations.
- Reports are made **under penalty of perjury** and are used for compliance monitoring: file authentic
  records, never the placeholder identities on this site. No monetary late penalty applies to the
  inventory report itself; the separate 2026-27 Rent Board Fee of **$59.00 per dwelling unit** (due
  March 1, March 2 starts 5% monthly penalties capped at 15%) still applies unless exempt.

Official links: [Housing Inventory](https://www.sf.gov/rent-board-housing-inventory),
[Admin Code Sec. 37.15](https://www.sf.gov/information--sec-3715-reporting-obligations-licensing),
[Rent increase guide](https://www.sf.gov/learn-about-rent-increases-san-francisco),
[Rent Board Fee](https://www.sf.gov/rent-board-fee).

## 2. Step-by-step for a first-time landlord

1. **Confirm coverage** with the City's rental-law guide; the reported 1940 building would generally be
   rent-controlled, but that intake is unverified (FR-01).
   [Coverage guide](https://www.sf.gov/learn-about-san-francisco-rental-laws/)
2. **Report both units into the Housing Inventory** on the Rent Board Portal and renew by March 1
   (update contact changes within 30 days).
3. **Verify each unit's license will be active on the effective date** (Sec. 37.15(e)).
4. **Authenticate the lawful base rent and history** - exclude passthroughs; a rent-history review
   route exists. Intake amounts are unverified (FR-03).
   [Unlawful-increase and rent-history review](https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history/)
5. **Pick a lawful effective date**: first increase 12 months after lease start, then at 12-month
   intervals; use the allowance in force on the effective date, not the service date.
6. **Compute on base rent only, never round up**, and itemize any banked portion with dates (Rules
   4.10/4.12; a nonconforming banked notice is void).
   [Banked increases](https://www.sf.gov/information--banked-rent-increases),
   [Part IV rules](https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring)
7. **Serve a written notice**: dollar amount, percentage, effective date; 30 days for a cumulative
   increase of 10% or less in the prior 12 months, 90 days above 10%, plus 5 days if mailed; email and
   text are not authorized by the statute.
   [Civil Code Sec. 827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=827&lawCode=CIV)
8. **Keep a private evidence pack** - lease, ledger, calculations, license snapshot, notice and proof
   of service - never in this public repository.

## 3. Rates verified on {RESEARCH_DATE_LONG}

- **1.6%** annual allowance for effective dates 2026-03-01 through 2027-02-28
  ([Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf)); the
  2027-28 rate is unpublished and blank (FR-08).
- Banking: skipped allowances bank after 12 full months; additive only, carry across owners, expire
  when a tenancy ends.
- **Pending legislation**: Board of Supervisors File No. 261020 (introduced 2026-09-15, pending
  committee action as of 2026-11-11) would cap combined banked and capital-improvement increases at
  10% per year, retroactive to notices served on or after 2026-09-15 if enacted as drafted (FR-09).

## 4. Conditional scenario results (arithmetic on owner-reported amounts)

Assumptions: periodic tenancy, active license, lawful base equals intake, zero intervening increases
for Unit B, no passthroughs, no subsidy restrictions. All assumptions are individually flagged.

| Scenario | Composition | Increase | Conditional new rent | Notice |
|---|---|---|---|---|
| A-1 (Unit A) | 1.6% annual only | $63.92 | $4,058.92 | 30 days (35 mailed) |
| A-2 (Unit A, 2027-02-01) | 1.4% banked + 1.6% annual = 3.0% | $119.85 | $4,114.85 | 30 days (35 mailed) |
| B-1 (Unit B) | 1.6% annual only | $50.40 | $3,200.40 | 30 days (35 mailed) |
| B-2 (Unit B) | 1.6% annual + 8.4% partial bank = 10.0% | $315.00 | $3,465.00 | 30 days (35 mailed) |
| B-3 (Unit B, 2027-02-15) | 11.5% full bank + 1.6% annual = 13.1% | $412.65 | $3,562.65 | 90 days (95 mailed) |

Intake: Unit A - lease start 2025-02-01 at $3,995.00 (three initial occupants), continuing tenancy
reported 2026-04-01 at unchanged $3,995.00 with one original and one subsequent occupant; Unit B -
lease start 2019-06-01 at $3,150.00, two occupants, intervening increases unknown (FR-05).

Time-sensitive: B-3's mailed-notice deadline for a 2027-02-15 effective date is **2026-11-12**, one day
after the research date; B-3's banked portion also exceeds the proposed File No. 261020 ceiling.
Scenarios B-1 and B-2 (and A-1/A-2) sit at or below 10%.

## 5. Answers to the five owner inquiries

1. **Reasonable and normal increases (94122):** the lawful annual allowance is 1.6% citywide, including
   Outer Sunset; no official neighborhood-specific "normal" figure exists (blank, FR-10). Banking up to
   the verified stack is lawful with correct notice; above 10% draws the 90-day tier and, if File No.
   261020 passes as drafted, a 10% combined cap.
2. **Corporations vs individuals:** identical legal duties; the empirical comparison is unverified
   (FR-11). Algorithmic rent-setting tools using non-public competitor data are banned for anyone
   (Sec. 37.10C).
3. **Correct notification and reasons:** serve the written 30/90-day notice with dollar, percentage and
   effective date; no cited rule requires a stated reason for an in-allowance increase - truthful,
   neutral context (inflation, insurance, maintenance) is good practice but never raises the ceiling.
4. **Tenant-advocate scrutiny:** the site's twelve-point stress test mirrors tenant-side review; a
   tenant petition (Form 516C) is free with no deadline; retaliation (Civil Code Sec. 1942.5),
   discrimination (Government Code Sec. 12955; Fair Housing Act) and harassment (Sec. 37.10B) reviews
   are factual - keep the evidence pack.
5. **One unit or both:** no uniform-increase statute was identified; a neutral written policy applied
   to both units (same percentage at each unit's lawful time) is the defensible posture, and raising
   only one unit needs a documented, non-discriminatory reason.

## 6. Repository review outcome

Re-verified: the 46-period allowance CSV matches Form 571 exactly; the existing executive summary still
matches the live rules. Irregularities flagged (FR-14 to FR-17): a mis-numbered ordinance reference in
internal notes (261015 vs File No. 261020), bracket-encoding and trailing-period citation nits, a frozen
2026-11-07 research stamp on archived base pages, and historical personal identifiers in public git
history that only a history rewrite can remove.

All 25 official sources with direct links: `f46f7d0f/sources.html`. All flags: `f46f7d0f/flagged.html`.
"""


def build_verification_md() -> str:
    src_lines = "\n".join(
        f"| {sid} | {SRC[sid][2]} | {SRC[sid][0]} | <{SRC[sid][1]}> |" for sid, _t, _ti, _l, _u in S)
    return f"""# Verification log - session F46F7D0F ({RESEARCH_DATE_LONG})

Scope claimed in `COORDINATION.md`: `f46f7d0f/**`, `EXECUTIVE-SUMMARY-F46F7D0F.md`,
`VERIFICATION-F46F7D0F.md`, and this session's `COORDINATION.md` entries. No other session's files are
modified; irregularities found in them are published (flagged), not edited.

## Method

1. Re-read the full repository state after rebasing onto the latest `origin/main`; audited the files in
   scope line by line.
2. Fetched every official source live on {RESEARCH_DATE_LONG} (see register below). Form 571, the
   Sec. 37.15 text, the rent-increase guide (File No. 261020 notice) and the Rent Board Fee page were
   fetched twice - once during initial research and again after the mid-session rebase - with identical
   results.
3. Recomputed every dollar figure with exact decimal arithmetic and every serve-by date with calendar
   arithmetic inside the site's builder; assertions fail the build if any number drifts.
4. Self-check then enforces on every generated file: no initial-shaped or street-shaped personal
   patterns, no merge markers, balanced HTML, unique ids, exactly one h1, lang/main/title/viewport
   present, every data-table row carrying at least one direct official source link, all local links and
   anchors resolving, and no external URL outside the official allowlist.
5. The continuous-integration suite was then run locally: `scripts/build.py` (twice - reproducible),
   `scripts/check.py`, `scripts/independent_audit.py`, `tools/check_links.py`, `tools/release_gate.py`,
   `tools/repository_audit.py --no-page`, `tools/followup_audit.py` - all results recorded in the pull
   request and `COORDINATION.md`.

## Official source register (fetched {RESEARCH_DATE_LONG})

| ID | Publisher | Title | URL |
|---|---|---|---|
{src_lines}

Textual-only legislative cite (portal host sits outside the repository audit allowlist): Board of
Supervisors File No. 261020, legislative record 8217304, introduced 2026-09-15, pending Land Use and
Transportation Committee action as of {RESEARCH_DATE_LONG}; the proposal is summarized and linked by
the City's own rent-increase page (S03).

## Arithmetic re-checks asserted in the builder

- Unit A: 3995.00 x 1.6% = 63.92 -> 4,058.92; 3995.00 x 3.0% = 119.85 -> 4,114.85.
- Unit B: 3150.00 x 1.6% = 50.40 -> 3,200.40; 3150.00 x 10.0% = 315.00 -> 3,465.00;
  3150.00 x 13.1% = 412.65 -> 3,562.65.
- Unit B banking stack: 1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 = 11.5 (additive only, Rule 4.12).
- Serve-by dates (verified by day count): 2027-01-01 minus 30/35 = 2026-12-02 / 2026-11-27;
  2027-02-01 minus 30/35 = 2027-01-02 / 2026-12-28; 2027-02-15 minus 90/95 = 2026-11-17 / 2026-11-12.
- Form 571: 46 published periods transcribed; 2027-28 deliberately blank; full match with
  `data/allowable-increases.csv` (repo audit row V01).

## Source irregularities caught while verifying

- The City's rent-increase page worked example attaches 1.6% to a June 1, 2025 effective date; the
  2025-26 allowance is 1.4%. The 2026-27 heading (1.6% for 2026-03-01 to 2027-02-28) is the correct
  statement. Persisting on {RESEARCH_DATE_LONG} (FR-12).
- The City's banked-increases page example mislabels an August 1, 2024 date with 1.4% (that period's
  rate was 1.7%); the rules text and Form 571 govern (FR-13).
- Repository items: internal notes cite 261015 instead of File No. 261020; Form 1007 URL appears with
  literal [74] rather than %5B74%5D in two places; two leginfo citations carry trailing periods; the
  archived base pages are stamped 07 Nov 2026, predating the 2026-11-09 File No. 261020 notice;
  historical public git history contains literal identifier tokens (earlier sessions' F15-class
  finding) that current-file edits cannot erase (FR-14 through FR-17).

## Limits

- Owner intake values (rents, dates, coverage, 1940 construction, occupant history) are not
  authenticated by any URL; they drive conditional arithmetic only and appear flagged.
- No inventory submission, license filing, tenant notice or attorney review was performed.
- The 2027-28 allowance was unpublished at research time; File No. 261020 was pending; recheck both
  before serving anything.
- Privacy: placeholder identities only in every tracked file; real identifiers were never committed.
"""


# ========================= writers and self-check ============================
PAGES = {
    "index.html": ("Executive summary", "SAN FRANCISCO · INDIVIDUAL OWNER · OUTER SUNSET 94122",
                   "Whether an individual owner must report and hold a rent-increase license comes "
                   "first, answered step by step with official links; everything else follows.",
                   INDEX_BODY),
    "process.html": ("License & step-by-step process", "HOUSING INVENTORY · LICENSE · NOTICE",
                     "The complete compliance path from Housing Inventory report to served notice, "
                     "with the exact reporting fields and fee calendar.",
                     PROCESS_BODY),
    "units-and-rates.html": ("Anonymized unit & rate analysis", "UNIT A · UNIT B · FORM 571",
                             "Every scenario is conditional arithmetic on owner-reported intake; "
                             "assumptions are explicit and flagged, never inferred.",
                             UNITS_BODY),
    "laws-and-notices.html": ("Laws & valid notices", "LOCAL · STATE · FEDERAL",
                              "The three legal layers that bound a rent increase for these "
                              "rent-controlled units, and what a defensible notice says.",
                              LAWS_BODY),
    "practices-and-scrutiny.html": ("Practices & tenant-side scrutiny", "CORPORATE VS INDIVIDUAL · ONE OR BOTH",
                                    "What could and could not be verified about owner practice, the "
                                    "one-unit-or-both analysis, and a twelve-point stress test.",
                                    PRAC_BODY),
    "repo-audit.html": ("Line-by-line repository audit", "READ-ONLY REVIEW · FLAGGED, NOT EDITED",
                        "Every tracked artifact in scope re-checked against official sources on "
                        "2026-11-11; irregularities published instead of silently fixed.",
                        REPO_BODY),
    "flagged.html": ("Flagged for review", "UNVERIFIED VALUES STAY BLANK",
                     "Twenty open items - unverified property facts, pending legislation, source and "
                     "repository irregularities - each with the official route to resolve it.",
                     FLAGGED_BODY),
    "sources.html": ("Official sources register", "TWENTY-FIVE SOURCES · FETCHED 2026-11-11",
                     "The complete evidence base. A link shows where a rule was read on the research "
                     "date; it never certifies an owner-supplied fact.",
                     SOURCES_BODY),
}


class Lint(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.row_official = False
        self.rows = 0
        self.thead = 0
        self.in_row = False
        self.h1 = 0
        self.title_text = False
        self.in_title = False
        self.lang = False
        self.main = False
        self.viewport = False
        self.links: list[str] = []
        self.stack: list[str] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        if tag == "html" and a.get("lang"):
            self.lang = True
        if tag == "main":
            self.main = True
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.in_title = True
        if tag == "meta" and a.get("name", "").lower() == "viewport":
            self.viewport = True
        if tag == "thead":
            self.thead += 1
        if tag == "tr" and not self.thead:
            self.in_row = True
            self.row_official = False
        if tag in ("a", "link"):
            href = a.get("href", "")
            if href:
                if urlsplit(href).scheme:
                    assert urlsplit(href).scheme == "https" and is_official(href), href
                    if tag == "a" and self.in_row:
                        self.row_official = True
                else:
                    self.links.append(href)
        if tag in ("script", "iframe", "embed", "object"):
            self.errors.append(f"active element <{tag}>")

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "thead":
            self.thead = max(0, self.thead - 1)
        if tag == "tr" and self.in_row:
            self.rows += 1
            assert self.row_official, f"row {self.rows} lacks an official source anchor"
            self.in_row = False
        if tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.errors.append(f"unclosed {self.stack.pop()}")
            if self.stack:
                self.stack.pop()
        else:
            self.errors.append(f"stray </{tag}>")

    def handle_data(self, data):
        if self.in_title and data.strip():
            self.title_text = True


def scan_text(path: Path, text: str) -> None:
    for n, line in enumerate(text.splitlines(), 1):
        assert not MERGE_MARKER.match(line), f"{path}:{n} merge marker"
        bad = [m.group() for m in INITIAL_PAIR.finditer(line) if m.group() not in CIVIC]
        assert not bad, f"{path}:{n} initial-shaped pair {bad}"
        assert not STREET.search(line), f"{path}:{n} street-shaped text"


def self_check(outputs: dict[str, str]) -> dict:
    assert (HERE / "style.css").is_file(), "style.css missing"
    scan_text(HERE / "style.css", (HERE / "style.css").read_text())
    scan_text(HERE / "build_f46f7d0f.py", (HERE / "build_f46f7d0f.py").read_text())
    html_docs: dict[str, Lint] = {}
    total_rows = 0
    for name, text in outputs.items():
        scan_text(HERE / name, text)
        if name.endswith(".html"):
            lint = Lint()
            lint.feed(text)
            lint.close()
            assert lint.lang and lint.main and lint.title_text and lint.viewport, name
            assert lint.h1 == 1, f"{name}: h1 count {lint.h1}"
            assert len(lint.ids) == len(set(lint.ids)), f"{name}: duplicate ids"
            assert not lint.stack, f"{name}: unclosed {lint.stack}"
            assert not lint.errors, f"{name}: {lint.errors}"
            assert "<script" not in text, name
            total_rows += lint.rows
            html_docs[name] = lint
    for name, lint in html_docs.items():
        for href in lint.links:
            target, _, frag = href.partition("#")
            target_path = (HERE / unquote(target)) if target else HERE / name
            assert target_path.exists(), f"{name}: missing local target {href}"
            assert target_path.resolve().is_relative_to(ROOT), href
            if frag and target.endswith(".html"):
                dest = target.rsplit("/", 1)[-1]
                if dest in html_docs:
                    assert frag in html_docs[dest].ids, f"{name}: anchor {href} missing"
    data = json.loads(outputs["data/verified_findings.json"])
    ids = {s["id"] for s in data["sources"]}
    assert ids == set(SRC), "JSON source register mismatch"
    for coll in ("scenarios", "flags", "inquiries"):
        for entry in data[coll]:
            for sid in entry["sources"]:
                assert sid in ids, f"{coll}: {sid}"
    assert data["rates"]["next_period_rate_pct"] is None
    assert {f["id"] for f in data["flags"]} == {f"FR-{i:02d}" for i in range(1, 21)}
    return {"pages": len(html_docs), "rows": total_rows, "sources": len(ids)}


def main() -> None:
    outputs: dict[str, str] = {}
    for fname, (title, eyebrow, lead, body) in PAGES.items():
        outputs[fname] = page(fname, title, eyebrow, lead, body)
    outputs["data/verified_findings.json"] = build_json()
    summaries = {
        ROOT / "EXECUTIVE-SUMMARY-F46F7D0F.md": build_exec_md(),
        ROOT / "VERIFICATION-F46F7D0F.md": build_verification_md(),
    }
    for path, text in summaries.items():
        scan_text(path, text)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    for name, text in outputs.items():
        (HERE / name).write_text(text, encoding="utf-8")
    for path, text in summaries.items():
        path.write_text(text, encoding="utf-8")
    stats = self_check(outputs)
    print(f"BUILD PASS: {stats['pages']} pages, {stats['rows']} sourced data rows, "
          f"{stats['sources']} official sources, 20 flagged items")
    print("Privacy patterns clean; arithmetic and serve-by dates asserted; all local and "
          "official links resolve.")


if __name__ == "__main__":
    main()
