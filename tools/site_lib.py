"""Shared site library: layout, styles, helpers, source register.

All factual values live in this module or in pages_1.py / pages_2.py and each one is
tied to a source id from SOURCES. Nothing here is inferred: if a value could not be
confirmed from an official source it is either omitted, or emitted as a blank cell
with an "unverified" badge.
"""

SITE_TITLE = "SF Rental Increase Compliance Dashboard"
SITE_SUB = "Two rent-controlled units &middot; 1940 building &middot; Outer Sunset, ZIP 94122 &middot; research date 7 November 2026"

# ---------------------------------------------------------------------------
# Source register. Every row of every table cites one of these ids.
# ---------------------------------------------------------------------------
SOURCES = [
    ("S1", "Learn about rent increases in San Francisco", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/learn-about-rent-increases-san-francisco",
     "1.6% allowable increase 3/1/26-2/28/27; 30/90-day notice; no limit on initial rent for an empty unit; anniversary date; notice content; no rounding up.", "verified"),
    ("S2", "571 Allowable Annual Increases (through 2/28/27)", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf",
     "Official year-by-year table of allowable annual increases, 4/1/1982 through 2/28/2027; states an increase may be imposed 'without filing a petition at the Rent Board'.", "verified"),
    ("S3", "The Rent Board Housing Inventory", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/rent-board-housing-inventory",
     "All owners must report; rent increase license generated automatically for tenant-occupied units; licence must be current on the effective date of the notice; March 1 deadline; no monetary penalty for late filing.", "verified"),
    ("S4", "S.F. Administrative Code Sec. 37.15 - Reporting Obligations; Licensing", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/information/sec-3715-reporting-obligations-licensing",
     "Ordinance text: licence to impose increases under Sec. 37.3(a)(1)-(2); suspension during noncompliance; tenant not obligated to pay increased rent during suspension; annual March 1 reporting.", "verified"),
    ("S5", "S.F. Administrative Code Sec. 37.3 - Rent Limitations", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/information/sec-373-rent-limitations",
     "60% of CPI capped at 7%; banking; petition route above the cap (a)(8); notice content (b)(1)-(4); nonconforming increase null and void (b)(5); no charge for additional occupants (a)(11); vacancy-control exceptions (f).", "verified"),
    ("S6", "S.F. Administrative Code Sec. 37.2 - Definitions", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/information/sec-372-definitions",
     "Definition of base rent: initial rent plus allowable increases imposed under the chapter.", "verified"),
    ("S7", "The Rent Board Fee", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/rent-board-fee",
     "$59.00 per dwelling unit for tax year 2026-27; due March 1; up to 50% ($29.50) recoverable from a tenant in occupancy on November 1; late penalties.", "verified"),
    ("S8", "S.F. Administrative Code Chapter 37A (Rent Stabilization and Arbitration Fee)", "SF.gov",
     "https://api.sf.gov/documents/7835/901_Rent_Board_Fee_Ch._37ARe.pdf",
     "Fee ordinance: applies to every residential unit; fee paid by March 1; 5% penalties; exemptions.", "verified"),
    ("S9", "Rules & Regulations Part IV - Rent Increases Not Requiring Approval by the Rent Board (Sec. 4.10 Notice, Sec. 4.12 Banking)", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/reports/february-2024/rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring",
     "Rule 4.10(a) notice content and 4.10(b) null-and-void rule with 0.5% good-faith tolerance; Rule 4.12 banking: only once every 12 months, 12 months must elapse, not compounded, not rounded up.", "verified"),
    ("S10", "625 - Complete San Francisco Rent Board Rules and Regulations (amended 1/13/26)", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/documents/36249/625_RR_Complete_1-13-26.pdf",
     "Current consolidated text of the Rules and Regulations (referenced for currency of Part IV).", "verified"),
    ("S11", "Banked rent increases", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/information/banked-rent-increases",
     "Banking mechanics; no cap on banked amount under current rules; bank does not carry to a new tenant; notice must state the banked portion; states a skipped increase is banked only if 'at least 24 full months pass' (see Flagged item F1).", "verified"),
    ("S12", "Learn about San Francisco rental laws", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/learn-about-san-francisco-rental-laws/",
     "June 13, 1979 coverage cutoff; units built before 6/14/1979 that are not single-family dwellings may have rent control and eviction protection.", "verified"),
    ("S13", "Partial exemption for certain single-family homes and condominiums under Costa-Hawkins", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/information/partial-exemption-certain-single-family-homes-and-condominiums-under-costa-hawkins",
     "A single-family dwelling with a legal or illegal in-law unit is a two-unit building and is NOT exempt.", "verified"),
    ("S14", "The California Tenant Protection Act of 2019 (AB 1482)", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482/",
     "AB 1482 cap 5%+CPI or 10%; 8.8% for SF from 8/1/2026-7/31/2027; does NOT apply to units under the SF Rent Ordinance increase limits; no limit on initial rent for a vacant unit.", "verified"),
    ("S15", "Cal. Civil Code Sec. 1947.12 (AB 1482 rent cap)", "California Legislative Information",
     "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1947.12",
     "Statutory text: 5%+CPI or 10%; only two increments in 12 months; new-tenancy initial rate (b); exemption for housing under a local ordinance that restricts increases below the state cap (d)(3).", "verified"),
    ("S16", "Cal. Civil Code Sec. 827 (notice of change in terms / rent increase)", "California Legislative Information",
     "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827",
     "30 days for an increase of 10% or less; 90 days for more than 10%; personal delivery or mail per Code Civ. Proc. Sec. 1013.", "verified"),
    ("S17", "Cal. Civil Code Sec. 1954.53 (Costa-Hawkins: initial rental rate)", "California Legislative Information",
     "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=1954.53",
     "An owner may establish the initial rental rate for a dwelling, except in the enumerated situations.", "verified"),
    ("S18", "The Rent Ordinance (Chapter 37 index and full text, amended 11/2/26)", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/reports--rent-ordinance/",
     "Section index for Chapter 37; links to the complete ordinance PDF (600_Ordinance_11-02-26).", "verified"),
    ("S19", "Landlord Petitions and Passthroughs", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/landlord-petitions-and-passthroughs/",
     "The six increase types that require a landlord petition before serving notice; no charge for filing; tenants need not pay until approved.", "verified"),
    ("S20", "Report an unlawful rent increase or request a review of your rent history", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/report-unlawful-rent-increase-or-request-review-your-rent-history/",
     "Tenant Petition Form C; no filing fee; no time limit for filing; arbitration hearing before a Rent Board Administrative Law Judge; decision appealable to the Rent Board Commission.", "verified"),
    ("S21", "S.F. Administrative Code Sec. 37.10B - Tenant Harassment", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/information/sec-3710b-tenant-harassment",
     "Harassment text, including (a)(5) influencing a tenant to vacate by fraud, intimidation or coercion; (a)(9) discrimination; civil and criminal remedies.", "verified"),
    ("S22", "S.F. Administrative Code Sec. 37.10C - Use and Sale of Algorithmic Devices Prohibited", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/information--sec-3710c-use-and-sale-algorithmic-devices-prohibited",
     "Revenue-management software that recommends rents using non-public competitor data may not be used by landlords in San Francisco; remedies.", "verified"),
    ("S23", "Rent Board news: Housing Inventory and rent increase licence (Ord. 265-20)", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/news--new-legislation-creates-housing-inventory-and-requires-owners-obtain-license-imposing",
     "Legislative history of the licence requirement; the licence issues only on substantial compliance with inventory reporting.", "verified"),
    ("S24", "Petition for a Determination Pursuant to Section 6.14 and/or Costa-Hawkins", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/information--petition-determination-pursuant-section-614-andor-costa-hawkins",
     "The ordinance does not regulate the initial rent for a new tenancy; 6.14 / Costa-Hawkins resets for remaining occupants; no petition is required but one may be filed.", "verified"),
    ("S25", "Housing Discrimination (FEHA)", "California Civil Rights Department",
     "https://calcivilrights.ca.gov/housing/",
     "Protected characteristics and prohibited practices for housing providers, including landlords and property managers; retaliation prohibited.", "verified"),
    ("S26", "Report housing discrimination / contact FHEO", "U.S. Department of Housing and Urban Development",
     "https://www.hud.gov/contactus/fairhousing",
     "Federal fair-housing enforcement contact, including the San Francisco Regional FHEO office.", "verified"),
    ("S27", "Notice to Tenant required by Sec. 37.9(c) (Tenant Right to Counsel Program)", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/sites/default/files/2023-08/1007%20Notice%20to%20Tenant%20Req%27d%20by%2037.%209(c)-Eng-Sp-Ch-Viet-Rus-Tag[74].pdf",
     "Official notice stating tenants are eligible for free assistance through the Tenant Right to Counsel Program (Eviction Defense Collaborative, 415-659-9184).", "verified"),
    ("S28", "San Francisco Rent Board (home; counsellor line 415-252-4600; portal; forms)", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/departments--rent-board",
     "Counselling hours, forms centre and Housing Inventory / fee portal.", "verified"),
    ("S29", "The Rent Board Rules and Regulations (landing page)", "SF.gov / San Francisco Rent Board",
     "https://www.sf.gov/reports--rent-board-rules-and-regulations",
     "Current consolidated Rules and Regulations, last amended 1/13/26; Part IV linked from here.", "verified"),
    ("S30", "626A - Complete list of amendments to the Rules and Regulations (through 1/13/26)", "SF.gov / San Francisco Rent Board",
     "https://media.api.sf.gov/documents/626A_Complete_List_of_Amendments_to_the_RRs_1-13-26_.pdf",
     "Amendment history, including the 3/11/86 entry that the landlord bears the burden of proving an above-allowable increase is justified, and the 5/6/86 banking clarifications.", "verified"),
]

SRC = {sid: dict(id=sid, title=t, pub=p, url=u, used=w, status=s) for sid, t, p, u, w, s in SOURCES}


def link(sid, text=None):
    """Inline citation link."""
    s = SRC[sid]
    label = text if text else s["id"]
    return '<a class="src" href="%s" target="_blank" rel="noopener">%s</a>' % (s["url"], label)


BADGE = {
    "verified": '<span class="badge ok">verified</span>',
    "unverified": '<span class="badge bad">unverified</span>',
    "pending": '<span class="badge warn">pending legislation</span>',
    "calculated": '<span class="badge calc">calculated</span>',
    "owner": '<span class="badge neutral">owner record</span>',
    "none": '<span class="badge neutral">no provision found</span>',
}


def badge(kind, text=None):
    if text:
        return '<span class="badge %s">%s</span>' % (
            {"verified": "ok", "unverified": "bad", "pending": "warn", "calculated": "calc",
             "owner": "neutral", "none": "neutral"}[kind], text)
    return BADGE[kind]


NAV = [
    ("index.html", "Dashboard"),
    ("pages/executive-summary.html", "Executive summary"),
    ("pages/rent-board-process.html", "Rent Board process"),
    ("pages/units.html", "Units &amp; numbers"),
    ("pages/allowed-increases.html", "Allowed increases"),
    ("pages/laws.html", "Local / State / Federal"),
    ("pages/notices.html", "Notices"),
    ("pages/owner-practices.html", "Owner playbook"),
    ("pages/tenant-review.html", "Tenant-lawyer test"),
    ("pages/sources.html", "Sources"),
    ("pages/flagged.html", "Flagged for review"),
]

CSS = """
:root{
  --bg:#f6f7f9; --panel:#ffffff; --ink:#15202b; --muted:#5d6b7a; --line:#e2e7ee;
  --brand:#0f4c81; --brand-soft:#eaf2f9; --ok:#1b7f4b; --ok-soft:#e8f6ee;
  --bad:#a8231f; --bad-soft:#fdecea; --warn:#8a5a00; --warn-soft:#fdf3e0;
  --calc:#3d4d8f; --calc-soft:#eceffa; --radius:10px;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
  font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--brand);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1120px;margin:0 auto;padding:0 20px}
header.top{background:var(--panel);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:20}
.top-inner{display:flex;gap:18px;align-items:center;justify-content:space-between;padding:12px 0;flex-wrap:wrap}
.brand{display:flex;gap:10px;align-items:center;font-weight:700;letter-spacing:.2px}
.brand .dot{width:10px;height:10px;border-radius:50%;background:var(--brand);display:inline-block}
.brand small{display:block;font-weight:500;color:var(--muted);font-size:12px;letter-spacing:0}
nav.main{display:flex;gap:4px;flex-wrap:wrap}
nav.main a{padding:6px 10px;border-radius:8px;font-size:13.5px;color:#2b3a49;font-weight:600}
nav.main a:hover{background:var(--brand-soft);text-decoration:none}
nav.main a.active{background:var(--brand);color:#fff}
.hero{padding:26px 0 6px}
.hero h1{margin:0 0 6px;font-size:27px;line-height:1.2;letter-spacing:-.3px}
.hero p.lede{margin:0;color:var(--muted);max-width:78ch}
.crumb{font-size:13px;color:var(--muted);margin:18px 0 4px}
main{padding:8px 0 60px}
section.panel{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:20px 22px;margin:16px 0}
section.panel h2{margin:0 0 10px;font-size:19px;letter-spacing:-.2px}
section.panel h3{margin:20px 0 8px;font-size:15.5px}
section.panel p{margin:0 0 10px}
section.panel ul,section.panel ol{margin:0 0 10px;padding-left:22px}
section.panel li{margin:0 0 6px}
.answer{border-left:4px solid var(--brand);background:var(--brand-soft);border-radius:0 8px 8px 0;padding:14px 16px;margin:0 0 12px}
.answer strong{color:#0d3f6b}
.callout{border-left:4px solid var(--warn);background:var(--warn-soft);border-radius:0 8px 8px 0;padding:12px 14px;margin:12px 0;font-size:15px}
.callout.bad{border-color:var(--bad);background:var(--bad-soft)}
.callout.ok{border-color:var(--ok);background:var(--ok-soft)}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}
.tile{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:16px}
.tile .k{font-size:12px;text-transform:uppercase;letter-spacing:.6px;color:var(--muted);font-weight:700}
.tile .v{font-size:26px;font-weight:750;letter-spacing:-.5px;margin:4px 0 2px}
.tile .n{font-size:13px;color:var(--muted)}
.tile a.more{font-size:13px;font-weight:600}
.card{display:block;background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);
  padding:16px 18px;color:inherit}
.card:hover{border-color:#c3d3e2;text-decoration:none;box-shadow:0 2px 10px rgba(15,76,129,.06)}
.card h3{margin:0 0 6px;font-size:16px;color:var(--brand)}
.card p{margin:0;color:var(--muted);font-size:14px}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:var(--radius);background:var(--panel)}
table{border-collapse:collapse;width:100%;font-size:14px;min-width:520px}
caption{caption-side:top;text-align:left;padding:12px 14px 0;font-weight:700;font-size:14px;color:var(--ink)}
th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:#f2f5f9;font-size:12px;text-transform:uppercase;letter-spacing:.4px;color:#42536b;font-weight:700;white-space:nowrap}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover{background:#fbfcfe}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
td code,td .mono{font-family:var(--mono);font-size:13px}
.badge{display:inline-block;font-size:11px;font-weight:700;padding:2px 7px;border-radius:999px;letter-spacing:.2px;white-space:nowrap}
.badge.ok{background:var(--ok-soft);color:var(--ok)}
.badge.bad{background:var(--bad-soft);color:var(--bad)}
.badge.warn{background:var(--warn-soft);color:var(--warn)}
.badge.calc{background:var(--calc-soft);color:var(--calc)}
.badge.neutral{background:#eef1f5;color:#4a5866}
a.src{font-family:var(--mono);font-size:12px;background:#eef4fa;border:1px solid #d7e5f2;border-radius:5px;
  padding:1px 5px;font-weight:700;color:#0d4a7a}
a.src:hover{background:#dcebf8;text-decoration:none}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:13px;color:var(--muted);margin:8px 0 0}
.step{display:flex;gap:14px;padding:14px 0;border-bottom:1px solid var(--line)}
.step:last-child{border-bottom:none}
.step .n{flex:0 0 34px;height:34px;border-radius:50%;background:var(--brand);color:#fff;display:flex;
  align-items:center;justify-content:center;font-weight:700;font-size:14px}
.step .c{flex:1}
.step h4{margin:2px 0 4px;font-size:15.5px}
.step p{margin:0 0 6px;font-size:14.5px}
.step .req{font-size:13px;color:var(--muted)}
footer{border-top:1px solid var(--line);background:var(--panel);padding:18px 0;color:var(--muted);font-size:13px}
.disclaimer{font-size:13px;color:var(--muted);border-top:1px dashed var(--line);margin-top:14px;padding-top:12px}
.pill{display:inline-block;font-size:12px;background:#eef1f5;border-radius:999px;padding:2px 9px;color:#42536b;font-weight:600;margin:0 6px 6px 0}
.right{text-align:right}
.small{font-size:13px}
.hr{height:1px;background:var(--line);margin:16px 0}
@media (max-width:640px){
  .hero h1{font-size:22px}
  section.panel{padding:16px}
  table{font-size:13px}
}
@media print{
  header.top,nav.main{display:none}
  body{background:#fff}
  section.panel{border:none;padding:0;margin:10px 0;break-inside:avoid}
  a.src{color:#000}
}
"""


def layout(title, body, active="", rel=""):
    if rel == "../":
        # pages live one directory down: "pages/x.html" must become "x.html"
        body = body.replace('href="pages/', 'href="')
    nav = []
    for href, label in NAV:
        cls = ' class="active"' if href == active else ""
        nav.append('<a href="%s%s"%s>%s</a>' % (rel, href, cls, label))
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s &middot; SF Rental Increase Dashboard</title>
<meta name="description" content="Source-linked research dashboard on lawful rent increases for a two-unit, rent-controlled building in San Francisco (Outer Sunset, ZIP 94122).">
<link rel="stylesheet" href="%(rel)sassets/style.css">
</head>
<body>
<header class="top">
  <div class="wrap top-inner">
    <div class="brand"><span class="dot"></span><span>SF Rental Increase Dashboard
      <small>Anonymised research &middot; sources verified 7 Nov 2026</small></span></div>
    <nav class="main">%(nav)s</nav>
  </div>
</header>
<div class="wrap">%(body)s</div>
<footer>
  <div class="wrap">
    <strong>Not legal advice.</strong> This is a source-linked research record compiled for one owner.
    Statutes and Rent Board rules change; the Rent Board counsellor line is 415-252-4600 and the
    official pages linked on every table are controlling. All tenant names, initials and addresses are
    replaced with placeholders; dates and dollar amounts are preserved.
    <div class="disclaimer">Built from official sources only (SF.gov / Rent Board, California Legislative
    Information, California Civil Rights Department, U.S. HUD). Values that could not be confirmed from an
    official source are left blank and listed on the <a href="%(rel)spages/flagged.html">Flagged for review</a> page.</div>
  </div>
</footer>
</body>
</html>
""" % dict(title=title, nav="".join(nav), body=body, rel=rel)


def page_head(h1, lede, crumb=""):
    c = '<div class="crumb">%s</div>' % crumb if crumb else ""
    return '<div class="hero">%s<h1>%s</h1><p class="lede">%s</p></div>' % (c, h1, lede)


def tbl(caption, head, rows, cls=""):
    """head: list of (label, is_num). rows: list of list of cell html strings."""
    th = "".join('<th%s>%s</th>' % (' class="num"' if num else "", label) for label, num in head)
    trs = []
    for r in rows:
        tds = []
        for i, cell in enumerate(r):
            num = head[i][1] if i < len(head) else False
            tds.append("<td%s>%s</td>" % (' class="num"' if num else "", cell))
        trs.append("<tr>%s</tr>" % "".join(tds))
    cap = "<caption>%s</caption>" % caption if caption else ""
    return '<div class="tablewrap"><table%s>%s<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (
        (' class="%s"' % cls) if cls else "", cap, th, "".join(trs))


def legend():
    return ('<div class="legend"><span>' + badge("verified") + " confirmed in the official source linked on the row</span>"
            "<span>" + badge("calculated") + " arithmetic from official percentages, not a Rent Board determination</span>"
            "<span>" + badge("owner") + " supplied by the owner, not independently verifiable</span>"
            "<span>" + badge("pending") + " bill introduced, outcome not confirmed</span>"
            "<span>" + badge("unverified") + " could not be confirmed &mdash; left blank</span></div>")


import re as _re


def resolve(html):
    """Replace [[S1]] markers with an inline citation link to source S1."""
    def _sub(m):
        sid = m.group(1)
        if sid not in SRC:
            raise KeyError("Unknown source id: %s" % sid)
        return link(sid)
    return _re.sub(r"\[\[(S\d+)\]\]", _sub, html)
