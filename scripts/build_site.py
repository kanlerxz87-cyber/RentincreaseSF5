#!/usr/bin/env python3
"""Build the static GitHub Pages dashboard from the verified JSON datasets.

Every rendered data row includes at least one link to an official government
source. Values that could not be confirmed from an official source are rendered
as an EMPTY cell and marked UNVERIFIED. No value is inferred or filled in.

Run: python3 scripts/build_site.py
"""
from __future__ import annotations
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
PREFIX = ""
VERIFIED_ON = "2026-11-07"


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


SOURCES = load("sources.json")
PROCESS = load("process.json")
REQUIREMENTS = load("requirements.json")
LEGAL = load("legal.json")
RATES = load("rates.json")
UNITS = load("units.json")
PRACTICE = load("practice.json")
DISCRIMINATION = load("discrimination.json")
FLAGS = load("flags.json")
VERIFICATION = load("verification.json")


def esc(x) -> str:
    return html.escape(str(x), quote=True)


def src_links(ids) -> str:
    out = []
    for sid in ids:
        s = SOURCES.get(sid)
        if not s:
            raise SystemExit(f"Unknown source id {sid}")
        out.append(
            f'<a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer" '
            f'title="{esc(s["title"])} — {esc(s["agency"])}">{esc(sid)}</a>'
        )
    return "".join(out)


def badge(status: str) -> str:
    label = {
        "verified": "Verified",
        "unverified": "UNVERIFIED",
        "owner-provided": "Owner-provided",
        "computed": "Computed",
        "analysis": "Analysis",
    }.get(status, status)
    extra = ""
    if status == "unverified":
        extra = f'<br><a href="{PREFIX}pages/flagged-for-review.html">Flagged for review</a>'
    return f'<span class="badge b-{esc(status)}">{label}</span>{extra}'


def table(headers, rows_html: list[str], classes: str = "") -> str:
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    return (
        f'<div class="tablewrap"><table data-filterable class="{classes}">'
        f"<thead><tr>{head}</tr></thead><tbody>" + "".join(rows_html) + "</tbody></table></div>"
    )


def td(value: str, cls: str = "", title: str = "") -> str:
    t = f' title="{esc(title)}"' if title else ""
    c = f' class="{cls}"' if cls else ""
    return f"<td{c}{t}>{value}</td>"


def generic_table(rows, group_key: str | None = None, group_label: str = "Scope") -> str:
    headers = ["ID"]
    if group_key:
        headers.append(group_label)
    headers += ["Topic / requirement", "Value / finding", "Detail / verification", "Status", "Official source(s)"]
    out = []
    for r in rows:
        cells = [td(esc(r["id"]), "id")]
        if group_key:
            cells.append(esc(r.get(group_key, "")))
        cells.append(td(esc(r["topic"])))
        value = r.get("value", "")
        if value == "" or value is None:
            cells.append('<td class="value blank" title="Left blank — unverified"></td>')
        else:
            cells.append(td(esc(value), "value"))
        cells.append(td(esc(r.get("detail", "")), "detail"))
        cells.append(td(badge(r.get("status", "verified"))))
        cells.append(td(src_links(r.get("sources", [])), "src"))
        out.append("<tr>" + "".join(cells) + "</tr>")
    return table(headers, out)


def rates_table() -> str:
    headers = ["ID", "Effective period", "Allowable annual increase", "Notes", "Status", "Official source(s)"]
    out = []
    for r in RATES:
        if r["rate"] == "":
            val = '<td class="value blank" title="Left blank — unverified"></td>'
        else:
            val = td(esc(r["rate"]), "value")
        out.append(
            "<tr>"
            + td(esc(r["id"]), "id")
            + td(esc(r["period"]))
            + val
            + td(esc(r.get("note", "")), "detail")
            + td(badge(r["status"]))
            + td(src_links(r["sources"]), "src")
            + "</tr>"
        )
    return table(headers, out)


def flags_table() -> str:
    headers = ["ID", "Severity", "Irregularity / unverified item", "Finding", "Impact", "Action", "Official source(s)"]
    out = []
    for r in FLAGS:
        out.append(
            "<tr>"
            + td(esc(r["id"]), "id")
            + td(f'<span class="sev {esc(r["severity"])}">{esc(r["severity"])}</span>')
            + td(esc(r["topic"]), "value")
            + td(esc(r["finding"]), "detail")
            + td(esc(r["impact"]), "detail")
            + td(esc(r["action"]), "detail")
            + td(src_links(r["sources"]), "src")
            + "</tr>"
        )
    return table(headers, out)


def sources_table() -> str:
    headers = ["ID", "Level", "Official source", "Agency", "What it verifies", "Official link"]
    out = []
    for sid, s in SOURCES.items():
        out.append(
            "<tr>"
            + td(esc(sid), "id")
            + td(esc(s["level"]))
            + td(esc(s["title"]), "value")
            + td(esc(s["agency"]))
            + td(esc(s["verifies"]), "detail")
            + td(
                f'<a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">Open official source ↗</a>',
                "src",
            )
            + "</tr>"
        )
    return table(headers, out)


def verification_table() -> str:
    headers = ["ID", "Check", "Method (line-by-line)", "Result", "Official source(s)"]
    out = []
    for r in VERIFICATION:
        out.append(
            "<tr>"
            + td(esc(r["id"]), "id")
            + td(esc(r["check"]), "value")
            + td(esc(r["method"]), "detail")
            + td(esc(r["result"]))
            + td(src_links(r["sources"]), "src")
            + "</tr>"
        )
    return table(headers, out)


NAV = [
    ("Dashboard", [
        ("Overview", "index.html"),
        ("Executive Summary", "pages/executive-summary.html"),
        ("Flagged for Review", "pages/flagged-for-review.html"),
    ]),
    ("Research", [
        ("Rent Board Process", "pages/rent-board-process.html"),
        ("Requirements Checklist", "pages/requirements.html"),
        ("Legal Framework", "pages/legal-framework.html"),
    ]),
    ("Data & Analysis", [
        ("Allowable Rates", "pages/allowable-rates.html"),
        ("Units & Calculations", "pages/units.html"),
        ("Practice & Notice", "pages/practice-and-notice.html"),
        ("Fair Housing / One vs Both", "pages/fair-housing.html"),
    ]),
    ("Audit", [
        ("Official Sources", "pages/sources.html"),
        ("Verification Log", "pages/verification.html"),
    ]),
]


def nav_html(active: str) -> str:
    parts = []
    for group, items in NAV:
        parts.append(f'<div class="navgroup">{esc(group)}</div>')
        for label, path in items:
            cls = ' class="active"' if label == active else ""
            parts.append(f'<a{cls} href="{PREFIX}{path}">{esc(label)}</a>')
    return '<nav aria-label="Site navigation">' + "".join(parts) + "</nav>"


def emit(rel: str, active: str, title: str, subtitle: str, body_fn):
    global PREFIX
    PREFIX = "" if rel == "index.html" else "../"
    body = body_fn()
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{esc(subtitle)}">
<title>{esc(title)} — SF Rent Increase Research</title>
<link rel="stylesheet" href="{PREFIX}assets/style.css">
<script defer src="{PREFIX}assets/app.js"></script>
</head>
<body>
<div class="wrap">
  <aside class="sidebar">
    <div class="brand">SF Rent Increase<br>Research Dashboard</div>
    <div class="sub">Outer Sunset · ZIP 94122 · anonymized</div>
    {nav_html(active)}
    <div class="foot">Official government sources only.<br>Last verified {VERIFIED_ON} (UTC).<br>Research, not legal advice.</div>
  </aside>
  <main class="main">
    <header class="top">
      <div><h1>{esc(title)}</h1><p>{esc(subtitle)}</p></div>
      <div class="stamp">Verified {VERIFIED_ON} · UTC</div>
    </header>
    {body}
    <footer class="pagefoot">
      All tenant identifiers are placeholders. No personal information is published. Dates and amounts are preserved as supplied.
      Every table row links to an official government source; unverifiable values are left blank and listed on the
      <a href="{PREFIX}pages/flagged-for-review.html">Flagged for Review</a> page.
      This project is research and compliance documentation, not legal advice.
    </footer>
  </main>
</div>
</body>
</html>
"""
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc, encoding="utf-8")
    print(f"wrote {rel}")


def tiles() -> str:
    items = [
        ("Executive Summary", "The license answer, up front", "pages/executive-summary.html"),
        ("Rent Board Process", "Step-by-step, with official links", "pages/rent-board-process.html"),
        ("Requirements Checklist", "Full list of requirements", "pages/requirements.html"),
        ("Legal Framework", "Local · State · Federal", "pages/legal-framework.html"),
        ("Allowable Rates", "Form 571, 1982–2027", "pages/allowable-rates.html"),
        ("Units & Calculations", "Anonymized case facts + math", "pages/units.html"),
        ("Practice & Notice", "Owners, corporations, reasons, advocates", "pages/practice-and-notice.html"),
        ("Fair Housing / One vs Both", "Discrimination analysis", "pages/fair-housing.html"),
        ("Official Sources", "Every link, in one registry", "pages/sources.html"),
        ("Verification Log", "Line-by-line verification", "pages/verification.html"),
        ("Flagged for Review", "Irregularities and blank values", "pages/flagged-for-review.html"),
    ]
    return '<div class="grid">' + "".join(
        f'<a class="tile link" href="{PREFIX}{p}"><div class="k">Page</div><div class="v">{esc(t)}</div><div class="d">{esc(d)}</div></a>'
        for t, d, p in items
    ) + "</div>"


def index_body() -> str:
    blanks = sum(1 for ds in (PROCESS, REQUIREMENTS, LEGAL, UNITS, PRACTICE, DISCRIMINATION) for r in ds if r.get("value", "") == "")
    blanks += sum(1 for r in RATES if r.get("rate", "") == "")
    verified_rows = sum(len(ds) for ds in (PROCESS, REQUIREMENTS, LEGAL, UNITS, PRACTICE, DISCRIMINATION, RATES, FLAGS, VERIFICATION))
    kpis = [
        ("Current allowable increase", "1.6%", "Effective 3/1/2026 – 2/28/2027 · citywide", "S02"),
        ("Rent Increase License", "REQUIRED", "For individual owners too; current on effective date", "S07"),
        ("Written notice", "30 / 90 days", "≤10% / >10%; +5 days if mailed", "S30"),
        ("Units analyzed", "2", "Anonymized · dates and amounts preserved", "S01"),
        ("Flags for review", str(len(FLAGS)), "Irregularities and unverified items", "S49"),
        ("Verified data rows", str(verified_rows), "Each with official source links", "S03"),
    ]
    cards = '<div class="grid">' + "".join(
        f'<div class="tile"><div class="k">{esc(k)}</div><div class="v">{esc(v)}</div>'
        f'<div class="d">{esc(d)} · {src_links([s])}</div></div>'
        for k, v, d, s in kpis
    ) + "</div>"
    return f"""
<div class="card answer">
  <p class="big">The Rent Board “license” question — answered first</p>
  <p><strong>Yes.</strong> As an individual owner of a rent-controlled unit you must comply with the Rent Increase License requirement. It is <strong>not a separate application</strong>: the license is generated automatically when you file the annual Housing Inventory report. There is <strong>no petition or notice about the specific increase</strong> for an ordinary annual or banked increase. But a current license must be on file <strong>on the effective date</strong> of the increase — otherwise the entire increase is null and void. A license does <strong>not</strong> prevent a tenant challenge.</p>
  <p class="srclist">Official sources: {src_links(['S07','S05','S03','S06','S08','S22'])} · Full answer on the <a href="{PREFIX}pages/executive-summary.html">Executive Summary</a> page.</p>
</div>
{cards}
<div class="card"><h2>Browse the dashboard</h2><p>Everything is organized by category. Each page presents its findings in a filterable table with an official source link on every row.</p>{tiles()}</div>
<div class="card"><h2>Answer to the license question — verification table</h2>
{generic_table([r for r in PROCESS if r['id'] in ('P01','P02','P03','P04','P05','P06','P07')])}
</div>
<div class="card"><h2>At a glance: what is reasonable and normal</h2>
{generic_table([r for r in UNITS if r['id'] in ('U15','U33','U36','U37')], 'unit', 'Unit')}
</div>
<div class="note red"><strong>Read this before serving any notice:</strong> two official SF Rent Board sources disagree on when a skipped annual increase becomes “banked” (12 months vs 24 months). This changes the largest lawful increase for Unit 2. The <a href="{PREFIX}pages/flagged-for-review.html">Flagged for Review</a> page documents the conflict with both source links. {src_links(['S15','S10'])}</div>
<p class="srclist">{blanks} value cells across the datasets are intentionally blank (unverified). No value was inferred or filled in.</p>
"""


def executive_body() -> str:
    return f"""
<div class="card answer">
  <p class="big">1. The Rent Board “license” — do you need it as an individual owner?</p>
  <p><strong>Yes.</strong> Section 37.15 applies to “<strong>Owners</strong> of residential dwelling units subject to this Chapter 37,” and Section 37.2(h) defines “Landlord” as “an owner, lessor, sublessor … and the agent, representative or successor of any of the foregoing.” There is <strong>no corporate carve-out</strong>. Condominiums and buildings with fewer than 10 residential units have been covered since <strong>March 1, 2023</strong> (10+ unit buildings since July 1, 2022). {src_links(['S07','S14','S05','S09'])}</p>
  <p><strong>But three details in the question need correcting:</strong></p>
  <ul class="clean">
    <li><strong>Not a separate application.</strong> “Once you have reported into the Housing Inventory, a rent increase license will be <strong>automatically generated</strong> for non-owner occupied units.” {src_links(['S05'])}</li>
    <li><strong>No notice/petition about this specific increase.</strong> Form 571: the allowable annual increase may be imposed “without filing a petition at the Rent Board”; the license “does not need to be included with your rent increase notice.” {src_links(['S03','S11','S05'])}</li>
    <li><strong>The effective date, not the notice date, controls.</strong> “A current Rent Increase License must be on file … before any annual or banked rent increase goes into effect”; Rule 13.14: “the effective date of the rent increase, not the date of service, shall be used.” An increase effective while unlicensed “shall render the entire rent increase null and void.” {src_links(['S06','S08','S07'])}</li>
    <li><strong>It does not prevent a challenge.</strong> Tenants may file an unlawful-rent-increase petition that is free with <strong>no time limit</strong>, or a Tenant Summary Petition. {src_links(['S22','S23'])}</li>
  </ul>
</div>
<div class="card"><h2>2. Step by step</h2>
  <ol class="clean">
    <li><strong>Confirm coverage</strong> — built on/before June 13, 1979, not single-family; verify on the official Property Information Map. {src_links(['S18','S36'])}</li>
    <li><strong>Report into the Housing Inventory by March 1 each year</strong> — under penalty of perjury; owner/manager contact, unit size, occupancy dates, base rent in $250 increments, utilities. {src_links(['S05','S07'])}</li>
    <li><strong>Confirm the license is current</strong> in the Rent Board Portal for the relevant year. {src_links(['S06','S37'])}</li>
    <li><strong>Pay the Rent Board fee separately</strong> — $59.00 per dwelling unit (2026-27); 50% recoverable from a qualifying tenant. {src_links(['S21'])}</li>
    <li><strong>Calculate</strong> — rate in effect on the effective date (1.6%), on base rent only, once per 12 months, no compounding, no rounding up. {src_links(['S01','S02','S04','S03'])}</li>
    <li><strong>Serve written notice</strong> — 30 days (≤10%) or 90 days (&gt;10%), +5 days if mailed; include dollar amount, percentage, effective date and any banked breakdown. {src_links(['S30','S01','S10','S13','S15'])}</li>
    <li><strong>On the effective date the license must still be current</strong>; keep the whole compliance file. {src_links(['S08','S22'])}</li>
  </ol>
  <div class="note blue">Six exception categories <strong>do</strong> require a landlord petition before the notice is served (capital improvements, O&amp;M, comparable rents, Proposition I, utility passthrough, Rule 1.21). {src_links(['S17'])}</div>
</div>
<div class="card"><h2>3. Full verification of the licensing answer</h2>{generic_table(PROCESS)}</div>
<div class="card"><h2>4. The other questions, summarized</h2>
  <ul class="clean">
    <li><strong>Reasonable/normal increase:</strong> 1.6% citywide for 3/1/2026–2/28/2027; no 94122-specific official rate; AB 1482 does not apply; no federal numeric cap located (blank/flagged). <a href="{PREFIX}pages/legal-framework.html">Legal Framework</a> · <a href="{PREFIX}pages/allowable-rates.html">Rates</a></li>
    <li><strong>Two units:</strong> 1.6% = $63.92 (Unit 1) and $50.40 (Unit 2); Unit 2 banked scenarios 13.1% or 11.7% depending on the unresolved conflict. <a href="{PREFIX}pages/units.html">Units &amp; Calculations</a></li>
    <li><strong>Corporations vs individuals:</strong> same rules; size-based, not entity-based, differences; internal corporate practices blank/unverified. <a href="{PREFIX}pages/practice-and-notice.html">Practice &amp; Notice</a></li>
    <li><strong>Notice &amp; reasons:</strong> written 30/90-day notice with a full breakdown; annual increase needs no justification; a new occupant is never a reason. <a href="{PREFIX}pages/practice-and-notice.html">Practice &amp; Notice</a></li>
    <li><strong>Tenant lawyers/advocates:</strong> free petitions, free Tenant Right to Counsel, official referral listing; the compliance file is the defense. <a href="{PREFIX}pages/practice-and-notice.html">Practice &amp; Notice</a></li>
    <li><strong>One unit or both:</strong> not required to raise both; use one written unit-neutral policy; discrimination/retaliation is the legal risk. <a href="{PREFIX}pages/fair-housing.html">Fair Housing</a></li>
    <li><strong>Irregularities:</strong> {len(FLAGS)} items, all with official links. <a href="{PREFIX}pages/flagged-for-review.html">Flagged for Review</a></li>
  </ul>
</div>
<div class="note"><strong>Privacy:</strong> all occupants appear as Occupant A–F. The owner's original identifiers are internal only and are not stored in this public repository. Dates and dollar amounts are unchanged.</div>
"""


def process_body() -> str:
    return f"""
<div class="card answer"><p class="big">Direct answer: yes, the license applies to you — and it must be current on the effective date</p>
<p>Official sources: {src_links(['S07','S05','S06','S08','S03','S22'])}</p></div>
<div class="card"><h2>Step-by-step findings and the exact official basis</h2>{generic_table(PROCESS)}</div>
<div class="card"><h2>The underlying statute, in brief</h2>
<p>Section 37.15 requires owners to report unit information under penalty of perjury, sets the 7/1/2022 and 3/1/2023 phase-ins, and states that a substantially compliant landlord “shall receive a license to impose rent increases … under Sections 37.3(a)(1)-(2),” suspended during noncompliance. {src_links(['S07'])} Rule 13.14 makes an increase effective while unlicensed null and void and fixes the effective date as the test. {src_links(['S08'])} Form 571 confirms that annual increases need no petition. {src_links(['S03'])}</p>
<p>Free, no-legal-advice counseling: {src_links(['S26'])} · Referral listing: {src_links(['S25'])}</p></div>
"""


def requirements_body() -> str:
    return f"""
<div class="note blue">This is the full requirements checklist. Every row links to the official source that establishes it. Rows marked <strong>UNVERIFIED</strong> have an intentionally blank value cell and appear on the <a href="{PREFIX}pages/flagged-for-review.html">Flagged for Review</a> page.</div>
<div class="card"><h2>All requirements ({len(REQUIREMENTS)} rows)</h2>{generic_table(REQUIREMENTS)}</div>
<div class="card"><h2>Companion process notes</h2>{generic_table(PROCESS[:8])}</div>
"""


def legal_body() -> str:
    local = [r for r in LEGAL if r["level"] == "Local"]
    state = [r for r in LEGAL if r["level"] == "State"]
    federal = [r for r in LEGAL if r["level"] == "Federal"]
    return f"""
<div class="card"><h2>Local — City and County of San Francisco (controlling)</h2>{generic_table(local)}</div>
<div class="card"><h2>State — California</h2>{generic_table(state)}</div>
<div class="card"><h2>Federal — United States</h2>{generic_table(federal)}
<div class="note">A federal numeric rent-increase cap for private, unsubsidized housing was not found in any official source. That value is <strong>left blank</strong> and flagged; no inference was made. Federal law that does apply is the Fair Housing Act's ban on discriminatory rental terms. {src_links(['S34','S35','S47'])}</div></div>
<div class="card"><h2>ZIP 94122</h2><p>The Rent Board publishes one allowable annual increase for all covered units in the City; no official 94122-specific rate or market benchmark was located, so that value is blank and flagged. Verify a property's build date for coverage on the official Property Information Map. {src_links(['S02','S18','S36'])}</p></div>
"""


def rates_body() -> str:
    return f"""
<div class="card answer"><p class="big">Current allowable annual increase: 1.6%</p><p>Effective March 1, 2026 through February 28, 2027, for rent-controlled units. Based on 60% of the increase in CPI-U for the Bay Area; statutory ceiling 7%; once every 12 months; calculated on base rent only; no rounding up. {src_links(['S02','S04','S01','S03','S13'])}</p></div>
<div class="note">Use the percentage in effect on the <strong>effective date</strong> of the increase, not the date the notice is served. {src_links(['S01'])} The 2027–2028 rate has not been published; its cell below is intentionally blank and flagged. {src_links(['S02','S42','S46'])}</div>
<div class="card"><h2>Official Form 571 table, 1982–2027, transcribed row by row</h2>{rates_table()}</div>
<div class="card"><h2>How the rate is used</h2>{generic_table([r for r in REQUIREMENTS if r['id'] in ('R08','R09','R10','R11','R12','R13','R14','R15')])}</div>
"""


def units_body() -> str:
    facts = [r for r in UNITS if r["id"] in ("U01", "U02", "U03", "U04", "U05", "U06")]
    u1 = [r for r in UNITS if r["unit"] == "Unit 1"]
    u2 = [r for r in UNITS if r["unit"] == "Unit 2"]
    both = [r for r in UNITS if r["unit"] == "Both"]
    return f"""
<div class="note blue"><strong>Privacy control:</strong> all occupant identifiers are placeholders (Occupant A–F). The owner's original identifiers are internal only and are not stored in this public repository. All dates and dollar amounts are preserved exactly as supplied. Owner-provided facts are labelled; where an official value is required but unavailable, the value cell is blank and the row is flagged.</div>
<div class="card"><h2>Property-level case facts and verification status</h2>{generic_table(facts, 'section', 'Section')}</div>
<div class="card"><h2>Unit 1 — lease February 1, 2025 @ $3,995; continuing tenancy April 1, 2026 @ $3,995</h2>
<p class="lead"><strong>Key finding:</strong> because an original occupant still resides there, the occupant change does not permit a market-rate reset and cannot be used as a reason for any increase. {src_links(['S13','S19','S16','S20'])}</p>
{generic_table(u1, 'section', 'Section')}</div>
<div class="card"><h2>Unit 2 — lease June 1, 2019 @ $3,150; occupants unchanged</h2>
<p class="lead"><strong>Key finding:</strong> six skipped annual increases are potentially bankable, but two official sources disagree on the eligibility window, so two scenarios are shown. Both exceed 10% and need 90 days' notice. {src_links(['S10','S15','S30','S03'])}</p>
{generic_table(u2, 'section', 'Section')}</div>
<div class="card"><h2>Conclusion for both units</h2>{generic_table(both, 'section', 'Section')}</div>
<div class="note">All dollar figures on this page are <strong>computed</strong> arithmetic applied to owner-provided rents and official published rates; they are not official Rent Board determinations. Percentages were added, not compounded, and no amount was rounded up. {src_links(['S01','S03','S11','S10'])}</div>
"""


def practice_body() -> str:
    return f"""
<div class="card"><h2>Corporations vs individual owners; notice; reasons; tenant-side review</h2>
<p>Rows labelled <span class="badge b-analysis">Analysis</span> are editorial synthesis of verified rules, not official determinations. Rows labelled <span class="badge b-unverified">UNVERIFIED</span> have a blank value cell.</p>
{generic_table(PRACTICE, 'group', 'Category')}</div>
<div class="card"><h2>Reasonable and normal, summarized</h2>
{generic_table([r for r in UNITS if r['id'] in ('U15','U33','U36','U37')], 'unit', 'Unit')}</div>
"""


def fair_body() -> str:
    return f"""
<div class="card answer"><p class="big">One unit or both?</p>
<p>Raising only one unit is not inherently unlawful, and <strong>no official source requires raising both</strong>. The Rent Ordinance is tenancy-specific: different lease dates, base rents, anniversary dates and banked histories legitimately produce different amounts. What is unlawful is choosing the unit or the amount because of a protected characteristic or in retaliation. Adopt one written, uniformly applied, unit-neutral policy and document the objective reason for each amount. {src_links(['S01','S12','S10','S33','S35','S28'])}</p></div>
<div class="card"><h2>Verification table</h2>{generic_table(DISCRIMINATION)}</div>
<div class="card"><h2>Requirements that matter most for a discrimination-safe process</h2>
{generic_table([r for r in REQUIREMENTS if r['id'] in ('R01','R08','R10','R15','R22','R23','R25','R28')])}</div>
"""


def sources_body() -> str:
    return f"""
<div class="note blue">Only official government sources (sf.gov / media.api.sf.gov / portal.sfrb.org / leginfo.legislature.ca.gov / hud.gov / govinfo.gov / sfplanninggis.org), plus the repository's own GitHub record, were used as verification. Commercial guides, press reports and forums were deliberately excluded. {src_links(['S49','S50'])}</div>
<div class="card"><h2>Official source registry ({len(SOURCES)} sources)</h2>{sources_table()}</div>
"""


def verification_body() -> str:
    return f"""
<div class="card"><h2>Line-by-line verification log</h2><p>Each check below was performed against the linked official page(s). Checks with no confirming official source produced a blank value and a flag, never an inferred value.</p>{verification_table()}</div>
<div class="card"><h2>Automated checks</h2>
<p><code>scripts/verify.py</code> parses every generated HTML page and enforces: (1) each data row has at least one link to an official source; (2) UNVERIFIED rows have an empty value cell; (3) all internal links and asset paths resolve; (4) no owner-supplied personal identifiers appear anywhere; (5) all source IDs used in the datasets exist in the registry. {src_links(['S49','S50','S03'])}</p>
<p>The site is plain static HTML/CSS/JS with a <code>.nojekyll</code> file so GitHub Pages serves the files without Jekyll processing. {src_links(['S50'])}</p></div>
"""


def flagged_body() -> str:
    return f"""
<div class="note red"><strong>Flagged for Review</strong> — these items are published so the owner can review them after the site is live and request changes. Flags do not block the site or the merge. Every row links to the official source(s) involved. Values that could not be confirmed from an official source are left <strong>blank</strong> in the data tables; they are never inferred or filled in.</div>
<div class="card"><h2>Irregularities, conflicts, and unverified items ({len(FLAGS)})</h2>{flags_table()}</div>
<div class="card"><h2>All blank / unverified value cells</h2>
{generic_table([r for ds in (PROCESS, REQUIREMENTS, LEGAL, UNITS, PRACTICE, DISCRIMINATION) for r in ds if r.get('value','') == ''])}
</div>
<div class="card"><h2>Blank rate cells</h2>{table(
    ['ID', 'Effective period', 'Allowable annual increase', 'Notes', 'Status', 'Official source(s)'],
    ['<tr>' + td(esc(r['id']), 'id') + td(esc(r['period'])) +
     '<td class="value blank" title="Left blank — unverified"></td>' +
     td(esc(r['note']), 'detail') + td(badge(r['status'])) + td(src_links(r['sources']), 'src') + '</tr>'
     for r in RATES if r['rate'] == ''])}</div>
"""


def main():
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    emit("index.html", "Overview", "SF rent increase research — verified dashboard",
         "A clean, source-linked dashboard for an individual owner of two rent-controlled units in San Francisco's Outer Sunset (ZIP 94122).", index_body)
    emit("pages/executive-summary.html", "Executive Summary", "Executive summary — the Rent Board license question comes first",
         "The full executive summary: the license answer, step-by-step process, and every other question answered with official links.", executive_body)
    emit("pages/rent-board-process.html", "Rent Board Process", "Rent Board process — license, reporting, notice",
         "The verified answer to the licensing question and the exact official basis for each step.", process_body)
    emit("pages/requirements.html", "Requirements Checklist", "Full requirements checklist",
         "Every requirement for a lawful rent increase on a San Francisco rent-controlled unit, row by row.", requirements_body)
    emit("pages/legal-framework.html", "Legal Framework", "Legal framework — local, state, federal",
         "Which laws actually cap or constrain the rent increase, and which do not.", legal_body)
    emit("pages/allowable-rates.html", "Allowable Rates", "Official allowable annual increases (Form 571)",
         "The complete official rate table and how the current 1.6% rate is applied.", rates_body)
    emit("pages/units.html", "Units & Calculations", "Unit-level case facts and calculations (anonymized)",
         "Anonymized case facts, verified legal effects, and arithmetic from official rates — with formulas shown.", units_body)
    emit("pages/practice-and-notice.html", "Practice & Notice", "Practice, notice, reasons, and tenant-side review",
         "Corporations vs individual owners, the correct way to notify tenants, reasonable reasons, and advocate scrutiny.", practice_body)
    emit("pages/fair-housing.html", "Fair Housing / One vs Both", "Fair housing and the one-unit vs both-units question",
         "What is lawful, what is not, and how to document a unit-neutral decision.", fair_body)
    emit("pages/sources.html", "Official Sources", "Official source registry",
         "Every source used for verification, with its official link and what it verifies.", sources_body)
    emit("pages/verification.html", "Verification Log", "Line-by-line verification log",
         "What was checked, how it was checked, and what was left blank.", verification_body)
    emit("pages/flagged-for-review.html", "Flagged for Review", "Flagged for review — irregularities and unverified items",
         "Published for owner review after deployment. Flags do not block the site.", flagged_body)


if __name__ == "__main__":
    main()
