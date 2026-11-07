#!/usr/bin/env python3
"""
Static site build for the SF rental-increase compliance dashboard.

Every table on the generated site is rendered from data/*.json. Dollar amounts are
computed here, from the officially published percentages in data/units.json
(Rent Board Form 571), so the arithmetic can never drift away from the rate table.

Run:  python3 build.py
Out:  docs/
"""

import json
import os
import shutil
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs")

TODAY = date(2026, 11, 7)          # research date for this session
PCT_WINDOW_END = date(2027, 2, 28)  # last day of the published 1.6% rate window


def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


SRC = {s["id"]: s for s in load("sources.json")["sources"]}
FACTS = load("facts.json")["rows"]
PROCESS = load("process.json")
UNITS_DATA = load("units.json")
MARKET = load("market.json")
QUESTIONS = load("questions.json")["questions"]
FLAGGED = load("flagged.json")

RATES = {r["key"]: r for r in UNITS_DATA["rates"]}

# ---------------------------------------------------------------- helpers

def money(v):
    return "${:,.2f}".format(v)


def pct(v):
    s = ("%f" % v).rstrip("0").rstrip(".")
    return s + "%"


def d(s):
    return date.fromisoformat(s)


def human(s):
    dt = d(s) if isinstance(s, str) else s
    return dt.strftime("%b %-d, %Y")


def src_links(ids, sources=SRC):
    out = []
    for i in ids:
        s = sources.get(i)
        if not s:
            out.append('<span class="badge badge-warn">%s (missing)</span>' % i)
            continue
        out.append(
            '<a class="src" href="sources.html#%s" title="%s">%s</a>'
            % (i, escape(s["title"]), i)
        )
    return " ".join(out)


def escape(t):
    return (
        str(t)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


STATUS_CLASS = {
    "verified": "badge-ok",
    "verified-dataset": "badge-ok",
    "analysis": "badge-note",
    "unverified": "badge-warn",
}
STATUS_LABEL = {
    "verified": "Verified",
    "verified-dataset": "Verified (dataset)",
    "analysis": "Analysis",
    "unverified": "Unverified",
}


def status_badge(s):
    return '<span class="badge %s">%s</span>' % (
        STATUS_CLASS.get(s, "badge-note"),
        STATUS_LABEL.get(s, s),
    )


# ---------------------------------------------------------------- calculations

def scenario_calc(unit, sc):
    total = sc.get("manual_total_pct")
    if total is None:
        total = sum(RATES[k]["pct"] for k in sc["rates"])
    base = unit["base_rent"]
    dollar = round(base * total / 100.0, 2)
    new_rent = round(base + dollar, 2)
    notice = 90 if total > 10.0 else 30
    eff = d(unit["target_effective_date"])
    latest = eff - timedelta(days=notice)
    latest_mail = latest - timedelta(days=5)
    return {
        "pct": total,
        "dollar": dollar,
        "new_rent": new_rent,
        "notice": notice,
        "latest": latest,
        "latest_mail": latest_mail,
        "passed": latest < TODAY,
    }


def market_stats(dist, rent):
    bands = [b for b in dist["bands"] if not b.get("exclude")]
    bands_sorted = sorted(bands, key=lambda b: b["lo"])
    n = sum(b["count"] for b in bands_sorted)
    # median band
    cum = 0
    median = None
    for b in bands_sorted:
        cum += b["count"]
        if cum >= n / 2.0:
            median = b
            break
    top = max(bands_sorted, key=lambda b: b["count"])
    at_or_above = sum(b["count"] for b in bands_sorted if b["lo"] >= rent)
    fully_below = sum(b["count"] for b in bands_sorted if b["lo"] + 250 <= rent)
    containing = [b for b in bands_sorted if b["lo"] <= rent < b["lo"] + 250]
    return {
        "n": n,
        "median": median,
        "top": top,
        "share_at_or_above": 100.0 * at_or_above / n if n else 0.0,
        "share_below": 100.0 * fully_below / n if n else 0.0,
        "containing": containing[0] if containing else None,
        "at_or_above_count": at_or_above,
        "below_count": fully_below,
    }


FLAGGED_BY_ID = {f["id"]: f for f in FLAGGED["items"]}

# ---------------------------------------------------------------- layout

NAV = [
    ("index.html", "Dashboard"),
    ("executive-summary.html", "Executive Summary"),
    ("process.html", "Licence &amp; Process"),
    ("units.html", "Unit Analysis"),
    ("market.html", "Market Context"),
    ("findings.html", "Findings"),
    ("questions.html", "Questions"),
    ("sources.html", "Sources"),
    ("flagged.html", "Flagged for Review"),
    ("method.html", "Method"),
]

SITE_NAME = "SF Rent Increase Compliance Dashboard"

CSS = """
:root{
  --ink:#12233b; --ink-soft:#43566f; --line:#dfe6ee; --bg:#f5f7fa;
  --card:#ffffff; --navy:#12385c; --teal:#0f766e; --amber:#b45309; --red:#b91c1c;
  --green:#15803d; --shadow:0 1px 2px rgba(18,35,59,.06),0 8px 24px rgba(18,35,59,.06);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  color:var(--ink);background:var(--bg)}
a{color:#0b5fa5;text-decoration:none}
a:hover{text-decoration:underline}
header.top{background:var(--navy);color:#fff;padding:0}
header.top .wrap{display:flex;align-items:center;gap:16px;flex-wrap:wrap;padding:14px 20px;max-width:1180px;margin:0 auto}
header.top .brand{font-weight:700;letter-spacing:.01em;font-size:15px;color:#fff}
header.top .brand span{display:block;font-weight:400;font-size:12px;opacity:.72}
nav.main{background:#0d2a46;border-top:1px solid rgba(255,255,255,.08)}
nav.main .wrap{max-width:1180px;margin:0 auto;padding:0 8px;display:flex;overflow-x:auto;gap:2px}
nav.main a{color:#cfe0f0;padding:11px 13px;font-size:14px;white-space:nowrap;border-bottom:3px solid transparent}
nav.main a:hover{background:rgba(255,255,255,.06);text-decoration:none;color:#fff}
nav.main a.on{color:#fff;border-bottom-color:#38bdf8;font-weight:600}
main{max-width:1180px;margin:0 auto;padding:28px 20px 64px}
h1{font-size:29px;line-height:1.25;margin:.2em 0 .35em;letter-spacing:-.01em}
h2{font-size:20px;margin:2em 0 .5em;padding-bottom:.3em;border-bottom:1px solid var(--line)}
h3{font-size:16px;margin:1.6em 0 .4em}
p,li{color:var(--ink-soft)}
p{margin:.6em 0}
.lede{font-size:17px;color:var(--ink)}
.kicker{text-transform:uppercase;letter-spacing:.08em;font-size:11px;font-weight:700;color:#0b5fa5}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:20px 22px;box-shadow:var(--shadow);margin:18px 0}
.grid{display:grid;gap:16px}
.g4{grid-template-columns:repeat(4,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g2{grid-template-columns:repeat(2,1fr)}
@media(max-width:900px){.g4{grid-template-columns:repeat(2,1fr)}.g3,.g2{grid-template-columns:1fr}}
@media(max-width:520px){.g4{grid-template-columns:1fr}}
.stat{background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px 18px;box-shadow:var(--shadow)}
.stat .n{font-size:26px;font-weight:700;letter-spacing:-.02em;color:var(--navy);line-height:1.15}
.stat .l{font-size:12.5px;color:#5b6b80;margin-top:4px}
.stat .s{font-size:11.5px;margin-top:8px}
table{width:100%;border-collapse:collapse;font-size:14px;background:#fff}
.wrap-table{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:#fff;box-shadow:var(--shadow);margin:14px 0}
th,td{padding:10px 12px;text-align:left;vertical-align:top;border-bottom:1px solid var(--line)}
th{background:#eef4fa;font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:#334760;position:sticky;top:0}
tbody tr:nth-child(even){background:#fafcfe}
tbody tr:last-child td{border-bottom:none}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.badge{display:inline-block;font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;letter-spacing:.02em;white-space:nowrap}
.badge-ok{background:#dcfce7;color:#14532d}
.badge-note{background:#fef3c7;color:#78350f}
.badge-warn{background:#fee2e2;color:#7f1d1d}
.badge-info{background:#e0f2fe;color:#075985}
a.src{display:inline-block;font-size:11.5px;font-weight:700;background:#eef4fa;border:1px solid #cfe0f0;
  color:#12385c;border-radius:6px;padding:1px 6px;margin:1px 2px 1px 0}
a.src:hover{background:#dbeafe;text-decoration:none}
.answer{border-left:4px solid var(--teal);background:#f0fdfa;padding:14px 18px;border-radius:0 8px 8px 0;margin:14px 0}
.answer .v{font-weight:700;color:#0f3f3a;font-size:16px}
.warnbox{border-left:4px solid var(--amber);background:#fffbeb;padding:14px 18px;border-radius:0 8px 8px 0;margin:14px 0}
.stopbox{border-left:4px solid var(--red);background:#fef2f2;padding:14px 18px;border-radius:0 8px 8px 0;margin:14px 0}
.navcards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:18px 0}
@media(max-width:900px){.navcards{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.navcards{grid-template-columns:1fr}}
a.navcard{display:block;background:#fff;border:1px solid var(--line);border-radius:10px;padding:16px 18px;
  box-shadow:var(--shadow);color:var(--ink)}
a.navcard:hover{border-color:#9cc3e6;text-decoration:none;transform:translateY(-1px);transition:.15s}
a.navcard b{display:block;font-size:15px;color:var(--navy);margin-bottom:3px}
a.navcard span{font-size:13px;color:#5b6b80}
.filter{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin:10px 0}
.filter input,.filter select{padding:8px 10px;border:1px solid #c6d3e0;border-radius:8px;font-size:14px;background:#fff;color:var(--ink)}
.filter input{min-width:240px}
.muted{color:#6b7c92;font-size:13px}
.tag{display:inline-block;font-size:11px;background:#eef4fa;color:#334760;border-radius:5px;padding:1px 6px;margin-right:4px}
ol.steps{list-style:none;counter-reset:s;padding:0;margin:8px 0}
ol.steps>li{counter-increment:s;position:relative;padding:0 0 0 52px;margin:0 0 22px}
ol.steps>li:before{content:counter(s);position:absolute;left:0;top:0;width:34px;height:34px;border-radius:50%;
  background:var(--navy);color:#fff;font-weight:700;font-size:15px;display:flex;align-items:center;justify-content:center}
ol.steps>li h3{margin:.1em 0 .2em;font-size:16.5px;color:var(--ink)}
ol.steps>li .meta{font-size:12.5px;color:#6b7c92;margin-top:6px}
footer{background:#0d2a46;color:#a9c2d8;padding:26px 20px;font-size:13px;margin-top:40px}
footer .wrap{max-width:1180px;margin:0 auto}
footer a{color:#cfe0f0}
ul.check{list-style:none;padding-left:0}
ul.check li{padding-left:26px;position:relative;margin:5px 0}
ul.check li:before{content:"\\2713";position:absolute;left:0;color:var(--green);font-weight:700}
ul.xlist{list-style:none;padding-left:0}
ul.xlist li{padding-left:26px;position:relative;margin:5px 0}
ul.xlist li:before{content:"\\2715";position:absolute;left:0;color:var(--red);font-weight:700}
.flagitem{border:1px solid var(--line);border-left:5px solid var(--red);background:#fff;border-radius:8px;
  padding:16px 18px;margin:14px 0;box-shadow:var(--shadow)}
.flagitem.amber{border-left-color:var(--amber)}
.flagitem h3{margin:.1em 0 .3em}
.flagitem .id{font-size:12px;font-weight:700;color:var(--red);letter-spacing:.04em}
.flagitem.amber .id{color:var(--amber)}
.anchor{scroll-margin-top:80px}
.kv{display:grid;grid-template-columns:200px 1fr;gap:6px 16px;font-size:14px}
@media(max-width:560px){.kv{grid-template-columns:1fr}}
.kv dt{color:#6b7c92;font-weight:600;font-size:13px}
.kv dd{margin:0}
.bar{height:9px;background:#e8eef5;border-radius:4px;overflow:hidden;min-width:70px}
.bar i{display:block;height:100%;background:#3d84c6}
.unit-a{border-left:5px solid var(--navy)}
.unit-b{border-left:5px solid var(--teal)}
.printonly{display:none}
@media print{nav.main,footer{display:none}.card{box-shadow:none}}
"""

JS = """
document.addEventListener('DOMContentLoaded', function () {
  // table filter: <div class="filter" data-table="#id">
  document.querySelectorAll('.filter').forEach(function (f) {
    var sel = f.getAttribute('data-table');
    var table = document.querySelector(sel);
    if (!table) return;
    var input = f.querySelector('input');
    var select = f.querySelector('select');
    function apply() {
      var q = (input && input.value || '').toLowerCase();
      var s = (select && select.value || '');
      var shown = 0;
      table.querySelectorAll('tbody tr').forEach(function (tr) {
        var txt = tr.textContent.toLowerCase();
        var ok = (!q || txt.indexOf(q) > -1) && (!s || tr.getAttribute('data-group') === s);
        tr.style.display = ok ? '' : 'none';
        if (ok) shown++;
      });
      var out = f.querySelector('.count');
      if (out) out.textContent = shown + ' row' + (shown === 1 ? '' : 's');
    }
    if (input) input.addEventListener('input', apply);
    if (select) select.addEventListener('change', apply);
    apply();
  });
});
"""

# ---------------------------------------------------------------- page shell

def page(slug, title, body, subtitle=""):
    nav = []
    for href, label in NAV:
        on = ' class="on"' if href == slug else ""
        nav.append('<a href="%s"%s>%s</a>' % (href, on, label))
    sub = '<span>%s</span>' % subtitle if subtitle else ""
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &middot; {site}</title>
<meta name="description" content="Verified San Francisco rent-increase requirements for two rent-controlled Outer Sunset units, with official source links.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="top"><div class="wrap"><div class="brand">SF Rent Increase Compliance Dashboard{sub}</div></div></header>
<nav class="main"><div class="wrap">{nav}</div></nav>
<main>
{body}
</main>
<footer><div class="wrap">
<p><strong>Research work product, not legal advice.</strong> Prepared {today} from primary government sources only. Dollar figures are our arithmetic on officially published percentages. Personal identifiers are withheld by design; tenant names are replaced with letters and dates and amounts are unchanged.</p>
<p>Every factual row links to its official source on the <a href="sources.html">Sources</a> page. Anything that could not be confirmed is on the <a href="flagged.html">Flagged for Review</a> page rather than in the tables.</p>
</div></footer>
<script src="assets/app.js"></script>
</body>
</html>
""".format(title=escape(title), site=SITE_NAME, sub=sub, nav="".join(nav), body=body, today=TODAY.strftime("%B %-d, %Y"))
    return html


def table(headers, rows, table_id=None, numeric_cols=(), classes=""):
    idattr = ' id="%s"' % table_id if table_id else ""
    th = "".join(
        '<th%s>%s</th>' % (' class="num"' if i in numeric_cols else "", h)
        for i, h in enumerate(headers)
    )
    body = []
    for r in rows:
        cells = []
        for i, c in enumerate(r):
            cls = ' class="num"' if i in numeric_cols else ""
            cells.append("<td%s>%s</td>" % (cls, c))
        body.append("<tr>%s</tr>" % "".join(cells))
    return '<div class="wrap-table"><table%s class="%s"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (
        idattr, classes, th, "".join(body)
    )


# ---------------------------------------------------------------- compute everything

UNITS = []
for u in UNITS_DATA["units"]:
    calc = []
    for sc in u["scenarios"]:
        c = scenario_calc(u, sc)
        c["sc"] = sc
        calc.append(c)
    UNITS.append({"unit": u, "calc": calc})

MARKET_STATS = {}
for dist in MARKET["distributions"]:
    MARKET_STATS[dist["bedrooms"]] = {
        "dist": dist,
        "by_rent": {b["unit"]: market_stats(dist, b["rent"]) for b in MARKET["benchmarks"]},
    }

N_VERIFIED = sum(1 for f in FACTS if f["status"].startswith("verified"))
N_ANALYSIS = sum(1 for f in FACTS if f["status"] == "analysis")
N_SOURCES = len(SRC)
N_FLAGS = len(FLAGGED["items"])

U1_SAFE = [c for c in UNITS[0]["calc"] if c["sc"]["id"] == "U1-A"][0]
U1_BANK = [c for c in UNITS[0]["calc"] if c["sc"]["id"] == "U1-B"][0]
U2_SAFE = [c for c in UNITS[1]["calc"] if c["sc"]["id"] == "U2-A"][0]
U2_ALL = [c for c in UNITS[1]["calc"] if c["sc"]["id"] == "U2-B"][0]
U2_TEN = [c for c in UNITS[1]["calc"] if c["sc"]["id"] == "U2-C"][0]

# ---------------------------------------------------------------- index page

def index_body():
    stats = [
        (pct(1.6), "Maximum annual increase<br>Mar 1 2026 - Feb 28 2027", "Rent Board Form 571", "ok"),
        (money(U1_SAFE["dollar"]), "Unit 1 increase at 1.6%<br>on " + money(3995), "computed", "ok"),
        (money(U2_TEN["dollar"]), "Unit 2 increase if held to 10%<br>on " + money(3150), "computed", "ok"),
        ("Yes", "Rent increase licence required<br>before the increase takes effect", "SF Admin Code §37.15", "ok"),
        ("30 / 90", "Days of written notice<br>(90 if the increase is over 10%)", "Civil Code §827", "ok"),
        (money(59), "Rent Board fee per unit<br>2026-2027 tax year, due March 1", "Rent Board Fee page", "ok"),
        (str(N_FLAGS), "Items flagged for review<br>unverified or conflicting", "Flagged page", "warn"),
        (str(N_VERIFIED), "Fact rows verified against<br>official sources", str(N_SOURCES) + " sources", "ok"),
    ]
    cards = []
    for n, l, s, kind in stats:
        badge = '<span class="badge badge-warn">needs review</span>' if kind == "warn" else '<span class="badge badge-ok">verified</span>'
        cards.append(
            '<div class="stat"><div class="n">%s</div><div class="l">%s</div><div class="s">%s</div></div>'
            % (n, l, badge)
        )
    navcards = [
        ("executive-summary.html", "Executive Summary", "Licence question answered first, then the findings that matter."),
        ("process.html", "Licence &amp; Process", "Eleven-step sequence, notice checklist and the things that void an increase."),
        ("units.html", "Unit Analysis", "Base rent, anniversary dates, scenarios and notice deadlines for Unit 1 and Unit 2."),
        ("market.html", "Market Context", "Published rate history and Sunset/Parkside rent distributions from the Rent Board inventory."),
        ("findings.html", "Findings", "All %d requirements in one filterable table, each with its official source." % len(FACTS)),
        ("questions.html", "Questions", "Direct answers to each question you asked, with the sources behind each."),
        ("sources.html", "Sources", "All %d official sources, each linked, with what it verifies." % N_SOURCES),
        ("flagged.html", "Flagged for Review", "What could not be verified, what conflicts, and what needs a human decision."),
        ("method.html", "Method", "How rows were verified, what was excluded, and the limits of this work."),
    ]
    nv = "".join(
        '<a class="navcard" href="%s"><b>%s</b><span>%s</span></a>' % (h, t, s)
        for h, t, s in navcards
    )
    body = """
<p class="kicker">San Francisco &middot; Outer Sunset, ZIP 94122 &middot; two rent-controlled units</p>
<h1>Raising rent on two rent-controlled units, verified line by line</h1>
<p class="lede">Everything below is built from primary government sources: the San Francisco Rent Ordinance and Rent Board, the California codes, HUD and the City's open-data portal. Each table row carries a link to the official source that supports it. Nothing was inferred.</p>

<div class="answer">
<div class="v">Short answer to your first question: yes, an individual owner needs the licence - but there is no application and nothing to send the Rent Board in advance.</div>
<p>Reporting each unit in the Rent Board <strong>Housing Inventory</strong> automatically generates the <strong>rent increase licence</strong>. The licence has to exist on the <em>date the increase takes effect</em>. Skip it and the increase is unenforceable and the tenant is not obligated to pay it (SF Admin Code §37.15(e); Rent Board Housing Inventory page). Being an individual rather than a corporation changes nothing in the ordinance. Full detail in step 2 and 3 of the process, and in the executive summary.</p>
</div>

<h2>At a glance</h2>
<div class="grid g4">{stats}</div>
<p class="muted">Percentages are the officially published Rent Board rates. Dollar amounts are this project's arithmetic on those rates, using the base rents you supplied; the base rents themselves are flagged as owner-supplied (FL-01).</p>

<h2>Sections</h2>
<div class="navcards">{nav}</div>

<h2>What this file says, in four sentences</h2>
<ol>
<li>The two increases are capped at <strong>1.6%</strong> of base rent for an effective date between March 1, 2026 and February 28, 2027, and the cap is the same for an individual owner and a corporation.</li>
<li>Unit 1 can lawfully take a <strong>1.6%</strong> increase on February 1, 2027 ({u1}); whether it can also add the skipped 2026 increase ({u1b}) depends on a genuine conflict between the ordinance text and the Rent Board's website, which is flagged rather than decided.</li>
<li>Unit 2 has six unused years of increases behind it, worth <strong>{u2all}</strong> including the current year - lawful, but the one item in this file most likely to attract a tenant petition, which is why a held-back 10% option is also priced ({u2ten}).</li>
<li>Nothing in the reviewed federal, state or local sources requires raising both units, or raising them equally. What is prohibited is discrimination on a protected ground and bad-faith pressure to vacate.</li>
</ol>
""".format(
        stats="".join(cards),
        nav=nv,
        u1=money(U1_SAFE["dollar"]),
        u1b=money(U1_BANK["dollar"]),
        u2all=money(U2_ALL["dollar"]),
        u2ten=money(U2_TEN["dollar"]),
    )
    return body


# ---------------------------------------------------------------- executive summary

def exec_body():
    scen_rows = []
    for item in UNITS:
        u = item["unit"]
        for c in item["calc"]:
            scen_rows.append(
                [
                    u["label"],
                    escape(c["sc"]["name"]),
                    pct(c["pct"]),
                    money(c["dollar"]),
                    money(c["new_rent"]),
                    "%d days" % c["notice"],
                    human(c["latest"]),
                    status_badge("verified")
                    if c["sc"]["id"].startswith("U1-A") or c["sc"]["id"] == "U2-A"
                    else status_badge("analysis"),
                ]
            )
    body = """
<p class="kicker">Executive summary</p>
<h1>The Rent Board question first, then what it means for these two units</h1>

<div class="answer">
<div class="v">You read that you must inform the Rent Board and apply for a licence to stop a rent increase from being challenged. The requirement is real. The mechanism is not what you read.</div>
<p><strong>There is no application, no approval step and no letter to the Rent Board before you notify tenants.</strong> What the law requires is that each unit be reported in the Rent Board's <em>Housing Inventory</em>, which is an annual online submission due March 1 and is free. Once a tenant-occupied unit is reported, a <strong>rent increase licence is generated automatically</strong>. That licence must be in effect on the date the increase takes effect - not merely by the time you write the notice. If it is not, the licence is treated as suspended for the period of noncompliance and the tenant is not obligated to pay the increased rent for those months; the Rent Board's own page adds that a notice is not enforceable without a licence on its effective date.</p>
<p><strong>And being an individual owner rather than a corporation changes nothing.</strong> The ordinance applies to "owners of residential dwelling units subject to this Chapter 37" without any size, entity or corporate threshold, and the licence provision is written the same way.</p>
<p><strong>Sequence therefore:</strong> report the unit &rarr; confirm the licence shows in the Rent Board Portal &rarr; calculate at the published rate &rarr; serve a conforming notice in time. An increase with perfect arithmetic served out of that order is still void, because a nonconforming increase is null and void under §37.3(b)(5) and a suspended licence defeats payment under §37.15(e).</p>
</div>

<h2>1. What the law actually allows, in numbers</h2>
<p>For an effective date between <strong>March 1, 2026 and February 28, 2027 the allowable annual increase is 1.6%</strong> of base rent (Rent Board Form 571; Rent Board rent-increase guidance). Three limits sit around that number:</p>
<ul>
<li><strong>One increase per 12 months</strong>, on the tenancy's anniversary date, with the first available 12 months after the lease began.</li>
<li><strong>No compounding and no rounding up.</strong> Multiple skipped years are added as percentages, then applied once to base rent.</li>
<li><strong>The 7% ceiling</strong> in the ordinance means the annual figure can never exceed 7% even if CPI spikes; this year it is 1.6% because the formula is 60% of the Bay Area CPI change.</li>
</ul>
<p>Anything above the cap requires a Rent Board petition filed <em>before</em> the notice: capital improvement, operating and maintenance, comparable rents, Prop I rent history, utility passthroughs, or a §1.21 increase. Filing is free and tenants do not pay until approval.</p>

<h2>2. What that means for your two units</h2>
<div class="wrap-table"><table><thead><tr>
<th>Unit</th><th>Base rent</th><th>Anniversary</th><th>Increases skipped</th><th>Safe option</th><th>Full entitlement</th></tr></thead><tbody>
<tr><td><strong>Unit 1</strong></td><td class="num">{u1base}</td><td>February 1</td><td>2026 only</td>
<td class="num">{u1safe}<br><span class="muted">1.6% &rarr; {u1new}</span></td>
<td class="num">{u1bank}<br><span class="muted">1.6% + 1.4% &rarr; {u1bnew}<br><em>needs confirmation (FL-03)</em></span></td></tr>
<tr><td><strong>Unit 2</strong></td><td class="num">{u2base}</td><td>June 1</td><td>2020 through 2025 (six years)</td>
<td class="num">{u2safe}<br><span class="muted">1.6% &rarr; {u2new}</span></td>
<td class="num">{u2all}<br><span class="muted">13.1% &rarr; {u2allnew}<br><em>requires 90-day notice</em></span></td></tr>
</tbody></table></div>
<p class="muted">Amounts are monthly, computed by this project from the published percentages against the base rents you supplied. Unit 2 also has a middle option - banked years held to a 10% total ({u2ten}) - which is a business choice, not a legal requirement, and keeps the increase inside the 30-day notice band.</p>

<h2>3. The reason there is a favourite and a risky option</h2>
<p>Unit 2 has not had an increase since 2019, so six years of published percentages have accumulated: 1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 = <strong>11.5%</strong>, plus the current 1.6% = <strong>13.1%</strong>. That is lawful and needs no petition. It is also the single number in this file most likely to produce a tenant petition, because a 13.1% single-step increase is the kind of fact pattern the ordinance's harassment section points at: §37.10B(a)(5) lists a rent increase "substantially in excess of market rates for comparable units" as evidence of bad faith where the tenant believes the increase is aimed at getting them to leave. There is no suggestion here that it is - but the notice has to survive a stranger reading it that way.</p>

<h2>4. A conflict you should know about before you rely on any number</h2>
<div class="warnbox">
<p><strong>FL-03.</strong> The Rent Board's "Banked rent increases" page says a skipped increase is banked only if <strong>24 full months</strong> pass without any rent increase. The ordinance itself, §37.3(a)(2), contains no 24-month condition - it allows a skipped increase to be imposed on "the tenant's subsequent rent increase anniversary dates" - and the Rent Board's own worked examples bank increases after 12 months. This is the difference between Unit 1 taking {u1safe} or {u1bank} on February 1, 2027. We did not resolve it in your favour or against you: both options are priced, the safe one is labelled safe, and a written answer from a Rent Board counsellor is the next step.</p>
</div>

<h2>5. Discrimination: one unit or both?</h2>
<p>No reviewed source - federal, state or local - requires you to increase both units or to increase them equally. Every rule constrains the amount, the timing, the notice and the licensing. What <em>is</em> prohibited is different treatment because of a protected characteristic: race, colour, religion, sex, gender identity or expression, sexual orientation, marital status, national origin, ancestry, familial status, source of income, disability, veteran status or genetic information under FEHA §12955, and race, colour, national origin, religion, sex, familial status or disability under the federal Fair Housing Act. Violating those laws is separately bad-faith harassment under §37.10B(a)(9), which carries treble damages and attorney fees.</p>
<p><strong>Raising both to look even is the weaker strategy here</strong>, because the two tenancies are not in the same position: Unit 1 is 21 months old with a skipped 2026 anniversary, Unit 2 has six banked years. Forcing one timetable would either impose a catch-up on Unit 1 it is not entitled to, or forfeit Unit 2's accumulated entitlement. The defensible position is the opposite of uniformity: treat each tenancy on its own anniversary, and keep a one-page file note per unit recording the anniversary date, the published rate, the licence check and the service date.</p>

<h2>6. Would a San Francisco tenant lawyer be able to overturn these increases?</h2>
<p>Not on the law, if four objective things are true: the units are covered; the licence was in effect on the effective date; the percentage is at or under the published rate; and the notice conforms to §37.3(b) and was served at least 30 days ahead (90 days above 10%). A tenant's remedy is a Rent Board petition - free, no time limit, heard by an Administrative Law Judge - and the Board can void only increases that break those rules. Free legal representation under the Tenant Right to Counsel programme attaches to eviction notices and unlawful detainer lawsuits, not to a rent-increase notice on its own; the petition process is expressly built for unrepresented parties.</p>
<p>There is also one challenge that has nothing to do with the percentage: a tenant who has asked for repairs required by law and not received them can petition on Form 516B to <strong>defer</strong> the annual increase, filing within 60 days of receiving the notice. If granted, the increase is postponed until the work is done and any increase already collected is refunded. A textbook-conforming 1.6% notice is still deferrable that way, which is why the repair file matters as much as the arithmetic.</p>
<p>What genuinely draws fire is not arithmetic but a catch-up that looks like pressure, an increase served on a tenant who has just complained about repairs, or a difference between two apparently identical tenancies that nobody wrote down. Those are the risks this file manages - not the 1.6%.</p>

<h2>7. All scenarios priced</h2>
{scen}
<p class="muted">Status marks: <span class="badge badge-ok">Verified</span> = rate and arithmetic are directly supported by Form 571 and the statute. <span class="badge badge-note">Analysis</span> = the percentage is supported but the choice of scenario (banking, or holding to 10%) depends on a judgement or an unresolved conflict.</p>

<h2>8. What to do next, in order</h2>
<ol>
<li>Confirm coverage from the City's Property Information Map - build year and unit count (FL-02).</li>
<li>Report both units in the Housing Inventory and confirm the licence shows in the Portal.</li>
<li>Call the Rent Board counsellor (415-252-4600) about the Unit 1 banking question and ask for it in writing (FL-03).</li>
<li>Reconcile each base rent against the original lease and bank records (FL-01).</li>
<li>Check whether a §6.14 notice was served on Unit 1's new co-tenant; if not, get advice before doing anything else (FL-05).</li>
<li>Pick the scenario, then serve a conforming notice on time - remembering the five extra days if mailed.</li>
</ol>

<div class="stopbox"><p><strong>Caveat.</strong> This is a research work product built from primary sources, not legal advice. Three of the inputs that drive the dollars - base-rent history, build year, bedroom count - come from you and cannot be checked against an official source without the property address. They are flagged, not asserted.</p></div>
""".format(
        u1base=money(3995),
        u2base=money(3150),
        u1safe=money(U1_SAFE["dollar"]),
        u1new=money(U1_SAFE["new_rent"]),
        u1bank=money(U1_BANK["dollar"]),
        u1bnew=money(U1_BANK["new_rent"]),
        u2safe=money(U2_SAFE["dollar"]),
        u2new=money(U2_SAFE["new_rent"]),
        u2all=money(U2_ALL["dollar"]),
        u2allnew=money(U2_ALL["new_rent"]),
        u2ten=money(U2_TEN["dollar"]),
        scen=table(
            ["Unit", "Scenario", "Total %", "Monthly increase", "New rent", "Notice", "Serve by (personal)", "Status"],
            scen_rows,
            numeric_cols=(2, 3, 4),
        ),
    )
    return body


# ---------------------------------------------------------------- process page

def process_body():
    steps = []
    for s in PROCESS["steps"]:
        n = s["n"]
        nlabel = str(int(n)) if float(n).is_integer() else "%s (optional branch)" % n
        steps.append(
            """<li><h3>%s</h3><p>%s</p><div class="meta"><strong>Timing:</strong> %s &nbsp;&middot;&nbsp; <strong>Source:</strong> %s</div></li>"""
            % (
                escape(s["title"]),
                escape(s["detail"]),
                escape(s["timing"]),
                src_links(s["sources"]),
            )
        )
    checks = "".join("<li>%s</li>" % escape(c) for c in PROCESS["notice_checklist"])
    nevers = "".join("<li>%s</li>" % escape(c) for c in PROCESS["never_do"])

    # licence timeline table
    tl = [
        ["Non-condominium units in buildings with 10 or more units", "July 1, 2022", "March 1 each year", src_links(["S05"])],
        ["Condominium units", "March 1, 2023", "March 1 each year", src_links(["S05"])],
        ["Units in buildings with fewer than 10 units", "March 1, 2023", "March 1 each year", src_links(["S05"])],
        ["Owner-occupied and vacant units", "Same schedule as the building type", "March 1 each year", src_links(["S05"])],
        ["Change of owner or manager business contact", "-", "Within 30 days", src_links(["S05"])],
    ]
    # notice requirements
    notice_rows = [
        ["Dollar amount of the increase", "Rent Board guidance", src_links(["S02"])],
        ["Percentage amount of the increase", "Rent Board guidance", src_links(["S02"])],
        ["Effective date", "Rent Board guidance", src_links(["S02"])],
        ["Which portion is the annual increase and/or a banked amount", "SF Admin Code §37.3(b)(1)", src_links(["S09"])],
        ["Which portion is O&amp;M, comparable rents, or certified capital improvements", "SF Admin Code §37.3(b)(2)", src_links(["S09"])],
        ["Which portion is a utility, water-bond or GO-bond passthrough", "SF Admin Code §37.3(b)(3)", src_links(["S09"])],
        ["Which portion is RAP loan amortisation", "SF Admin Code §37.3(b)(4)", src_links(["S09"])],
        ["30 days' written notice (10% or less) / 90 days (more than 10%)", "Civil Code §827(b); Rent Board", src_links(["S10", "S02"])],
        ["Service personally, or by mail under CCP §1013 (+5 days)", "Civil Code §827(b)(1)", src_links(["S10"])],
    ]
    body = """
<p class="kicker">Licence and process</p>
<h1>The sequence, step by step</h1>
<p class="lede">{headline}</p>

<div class="warnbox"><p><strong>No-application correction.</strong> You do not apply for the licence and you do not notify the Rent Board before notifying tenants. The Housing Inventory submission <em>is</em> the licence mechanism, it is generated automatically for tenant-occupied units, and it must be current on the effective date of the increase. Nothing has to be attached to the notice.</p></div>

<h2>The eleven steps</h2>
<ol class="steps">{steps}</ol>

<h2>When the reporting obligation started</h2>
{tl}

<h2>Notice content: what must be in the document</h2>
{notice}
<p class="muted">There is no official requirement to state a <em>reason</em> for the increase. The required content is the money, the percentage, the date and the breakdown. A nonconforming increase is null and void (§37.3(b)(5)).</p>

<h2>Checklist before it goes out</h2>
<ul class="check">{checks}</ul>

<h2>Things that will void an increase or create liability</h2>
<ul class="xlist">{nevers}</ul>

<h2>If you need more than the cap</h2>
<p>Six categories of increase require a landlord petition filed before the notice: capital improvement, operating and maintenance expenses, comparable rents, Prop I past rent history, utility passthroughs, and a §1.21 increase where there is no tenant in occupancy. There is no filing fee, tenants are not required to pay until the Rent Board approves, and an approved increase is retroactive to the effective date stated in a valid notice. {s22}</p>
""".format(
        headline=escape(PROCESS["headline"]),
        steps="".join(steps),
        tl=table(["Who reports", "Reporting began", "Ongoing requirement", "Source"], tl),
        notice=table(["Required content", "Authority", "Source"], notice_rows),
        checks=checks,
        nevers=nevers,
        s22=src_links(["S22"]),
    )
    return body


# ---------------------------------------------------------------- units page

def units_body():
    out = []
    for idx, item in enumerate(UNITS):
        u = item["unit"]
        cls = "unit-a" if idx == 0 else "unit-b"
        sc_rows = []
        for c in item["calc"]:
            sc = c["sc"]
            srcs = src_links(sorted({RATES[k]["source"] for k in sc["rates"]}) or ["S01"])
            passed = '<span class="badge badge-warn">date passed</span>' if c["passed"] else '<span class="badge badge-ok">available</span>'
            sc_rows.append(
                [
                    "<strong>%s</strong><br>%s" % (escape(sc["id"]), escape(sc["name"])),
                    pct(c["pct"]),
                    money(c["dollar"]),
                    money(c["new_rent"]),
                    "%d days" % c["notice"],
                    human(c["latest"]) + "<br>" + passed,
                    human(c["latest_mail"]),
                    srcs,
                ]
            )
        explain = []
        for c in item["calc"]:
            sc = c["sc"]
            if sc.get("rates"):
                parts = " + ".join(
                    "%s (%s)" % (pct(RATES[k]["pct"]), RATES[k]["period"]) for k in sc["rates"]
                )
            else:
                parts = "held to %s by choice" % pct(c["pct"])
            explain.append(
                "<li><strong>%s</strong>: %s = <strong>%s</strong>. %s &times; %s = <strong>%s</strong>, so the new rent is <strong>%s</strong>. Notice period: %d days.<br><span class=\"muted\">%s</span></li>"
                % (
                    escape(sc["id"]),
                    parts,
                    pct(c["pct"]),
                    money(u["base_rent"]),
                    pct(c["pct"]),
                    money(c["dollar"]),
                    money(c["new_rent"]),
                    c["notice"],
                    escape(sc["note"]),
                )
            )
        flags = "".join(
            '<a class="src" href="flagged.html#%s">%s</a>' % (f, f) for f in u["flags"]
        )
        out.append(
            """<div class="card {cls}">
<h2 style="margin-top:0">{label}</h2>
<dl class="kv">
<dt>Base rent</dt><dd><strong>{base}</strong> per month (as of {asof})</dd>
<dt>Lease started</dt><dd>{lease}</dd>
<dt>Original tenants</dt><dd>{ti}</dd>
<dt>Current tenants</dt><dd>{tc}</dd>
<dt>Occupancy change</dt><dd>{occ}</dd>
<dt>Anniversary date</dt><dd>{ann}</dd>
<dt>First eligible increase</dt><dd>{first}</dd>
<dt>Last increase</dt><dd>{last}</dd>
<dt>Target effective date</dt><dd>{target} &mdash; {why}</dd>
<dt>Open flags</dt><dd>{flags}</dd>
</dl>
<h3>Calculation</h3>
<ul>{explain}</ul>
<h3>Notice planner</h3>
{sc}
<p class="muted">"Serve by (personal)" is the last day a notice can be delivered in person to keep the target effective date. "Serve by (mail)" subtracts the five extra days required for mailed service under CCP §1013. Dates are computed; the notice periods come from Civil Code §827 and the Rent Board's guidance.</p>
</div>""".format(
                cls=cls,
                label=escape(u["label"]),
                base=money(u["base_rent"]),
                asof=human(u["base_rent_as_of"]),
                lease=human(u["lease_start"]),
                ti=escape(u["tenants_initial"]),
                tc=escape(u["tenants_current"]),
                occ=escape(u["occupancy_change"]),
                ann=escape(u["anniversary"]),
                first=human(u["first_eligible_increase"]),
                last=escape(u["last_increase_note"]),
                target=human(u["target_effective_date"]),
                why=escape(u["target_rationale"]),
                flags=flags,
                explain="".join(explain),
                sc=table(
                    ["Scenario", "Total %", "Monthly increase", "New rent", "Notice", "Serve by (personal)", "Serve by (mail)", "Rate source"],
                    sc_rows,
                    numeric_cols=(1, 2, 3),
                ),
            )
        )
    body = """
<p class="kicker">Unit analysis</p>
<h1>Both units, priced and dated</h1>
<p class="lede">The percentages are verified; the dollars are arithmetic; the base rents and the build year are your inputs and are flagged. Tenant names are replaced with letters.</p>
{units}
<h2>Cross-cutting notes</h2>
<div class="warnbox">
<p><strong>Unit 1 changed occupants.</strong> Two rules bite, and neither allows a market-rate reset now. Costa-Hawkins §1954.53(d)(3) says the market-rate right does not apply to a partial change of occupancy where one of the original occupants remains - and one does. Rules &amp; Regs §6.14 permits an unlimited increase when the last original occupant vacates, but only if the new occupant was served a written 6.14 notice within a reasonable time of moving in, generally 60 days. Whether that happened is unknown (FL-05) and it is worth checking, because it is the difference between a controlled rent and a market rent later.</p>
</div>
<div class="warnbox">
<p><strong>Unit 2's target date matters.</strong> The 1.6% rate is published only through February 28, 2027. An increase effective after that date needs the rate that will not be published until March 1, 2027, which nobody can verify today. Because Unit 2's full entitlement exceeds 10%, a 90-day notice is required - which for a February 28, 2027 effective date means service by {u2last} ({u2mail} if mailed). Those dates are close.</p>
</div>
""".format(
        units="".join(out),
        u2last=human(U2_ALL["latest"]),
        u2mail=human(U2_ALL["latest_mail"]),
    )
    return body


# ---------------------------------------------------------------- market page

def market_body():
    rate_rows = []
    for r in UNITS_DATA["rates"]:
        rate_rows.append([r["period"], pct(r["pct"]), src_links([r["source"]])])
    counts_rows = [
        [c["bedrooms"], "{:,}".format(c["count"])] for c in MARKET["counts_by_bedrooms_2026"]
    ]
    dist_tables = []
    for bedrooms, info in MARKET_STATS.items():
        dist = info["dist"]
        bands = sorted([b for b in dist["bands"] if not b.get("exclude")], key=lambda b: b["lo"])
        n = info["by_rent"]
        rows = []
        maxc = max(b["count"] for b in bands)
        for b in dist["bands"]:
            if b.get("exclude"):
                continue
            share = 100.0 * b["count"] / (sum(x["count"] for x in bands) or 1)
            rows.append(
                [
                    escape(b["label"]),
                    "{:,}".format(b["count"]),
                    "{:.1f}%".format(share),
                    '<div class="bar"><i style="width:%.0f%%"></i></div>' % (100.0 * b["count"] / maxc if maxc else 0),
                ]
            )
        total = sum(b["count"] for b in bands)
        summary = []
        for bmk in MARKET["benchmarks"]:
            st = info["by_rent"][bmk["unit"]]
            summary.append(
                [
                    bmk["unit"],
                    money(bmk["rent"]),
                    escape(st["median"]["label"]) if st["median"] else "-",
                    escape(st["top"]["label"]) if st["top"] else "-",
                    "{:,} of {:,} ({:.0f}%)".format(st["at_or_above_count"], st["n"], st["share_at_or_above"]),
                    "{:,} of {:,} ({:.0f}%)".format(st["below_count"], st["n"], st["share_below"]),
                ]
            )
        dist_tables.append(
            """<h2>{bed} &mdash; {total:,} reported units (2026 submissions)</h2>
{summary}
<details><summary class="muted">Show the full band distribution and the exact query used</summary>
{bands}
<p class="muted">Query: <a href="{q}">re-run this query on data.sfgov.org</a></p>
</details>""".format(
                bed=bedrooms,
                total=total,
                summary=table(
                    ["Unit", "Rent", "Median band", "Most common band", "In bands at/above this rent", "In bands entirely below"],
                    summary,
                ),
                bands=table(["Rent band ($/month)", "Units", "Share", ""], rows, numeric_cols=(1, 2)),
                q=dist["query_url"],
            )
        )
    body = """
<p class="kicker">Market context</p>
<h1>What "normal" looks like in the Outer Sunset, and what the rate history is</h1>
<p class="lede">Two different questions hide inside "what is a normal increase": what the law allows (a hard number), and what comparable units actually rent for (a distribution). The first is exact; the second is only as good as the City's self-reported inventory.</p>

<h2>1. The published maximum: every rate back to 2020</h2>
{rates}
<p class="muted">Complete table back to 1982 is in Form 571 ({s01}). The rate is set as 60% of the change in the Bay Area CPI, and the ordinance caps any annual increase at 7%.</p>

<h2>2. Why the state cap does not raise the ceiling</h2>
<p>AB 1482 caps rent increases at 5% plus CPI or 10%, whichever is lower, for covered units - but §1947.12(d)(3) excludes housing subject to a local ordinance that restricts annual increases below that level. San Francisco's 1.6% is far below it, so the local cap governs and the AB 1482 cap never binds for a covered unit here. {s11}</p>
<p>Federal law adds no ceiling: the Fair Housing Act governs <em>who</em> you may discriminate against, not <em>how much</em> you may charge. {s14}</p>

<h2>3. What comparable units are reported to be paying</h2>
<p>The Rent Board's public housing inventory reports base rent in $250 bands by City analysis neighbourhood. The figures below are the 2026 submission year, non-owner-occupied units, for <strong>Sunset/Parkside</strong> - the City's published geography that covers the Outer Sunset. {geo}</p>
{counts}
{dists}

<h2>4. Reading this honestly</h2>
<ul>
<li>These are <strong>contract rents already in force</strong>, not asking rents. They lag the market by construction.</li>
<li>Bands are $250 wide and self-reported, so a "median band" is the band containing the median, not a median dollar figure.</li>
<li>Neither unit's bedroom count was supplied, so all three distributions are shown (FL-06). At {u1}, Unit 1 sits near the top of the one-bedroom range, mid-range for two-bedrooms and below the middle of three-bedrooms. At {u2}, Unit 2 is mid-to-upper for one-bedrooms, near the middle for two-bedrooms and below the middle for three-bedrooms.</li>
<li>The inventory is not a rent-cap dataset and has no notion of "normal increase". The only official definition of a normal increase is the published percentage.</li>
</ul>
<div class="warnbox"><p><strong>Why this data matters legally.</strong> §37.10B(a)(5) treats a rent increase "substantially in excess of market rates for comparable units" as evidence of bad faith where a tenant believes an increase is aimed at getting them out. Because this inventory is public, a tenant advocate can run the same comparison in minutes. Knowing where your rent sits in the distribution is therefore not market research - it is risk assessment.</p></div>
""".format(
        rates=table(["Effective period", "Allowable increase", "Source"], rate_rows, numeric_cols=(1,)),
        s01=src_links(["S01"]),
        s11=src_links(["S11"]),
        s14=src_links(["S14"]),
        geo=src_links(["S24"]),
        counts=table(["Bedrooms (2026 submissions, Sunset/Parkside)", "Reported units"], counts_rows, numeric_cols=(1,)),
        dists="".join(dist_tables),
        u1=money(3995),
        u2=money(3150),
    )
    return body


# ---------------------------------------------------------------- findings page

def findings_body():
    rows = []
    for f in FACTS:
        rows.append(
            [
                "<strong>%s</strong>" % f["id"],
                escape(f["level"]),
                escape(f["topic"]),
                escape(f["requirement"]),
                escape(f["authority"]),
                src_links([f["source"]]),
                status_badge(f["status"]),
            ]
        )
    levels = sorted({f["level"] for f in FACTS})
    opts = '<option value="">All layers</option>' + "".join(
        '<option value="%s">%s</option>' % (l.lower(), l) for l in levels
    )
    body = """
<p class="kicker">Findings</p>
<h1>Every requirement checked, in one table</h1>
<p class="lede">{n} rows. Each one states the requirement, the authority it comes from, a link to the official source, and whether it is verified or analysis. Rows that could not be confirmed are not here - they are on the <a href="flagged.html">Flagged for Review</a> page.</p>
<div class="filter" data-table="#findings"><input type="search" placeholder="Filter by keyword (licence, notice, banking, deposit...)"><select>{opts}</select><span class="muted count"></span></div>
<div class="wrap-table"><table id="findings"><thead><tr>
<th>ID</th><th>Layer</th><th>Topic</th><th>Requirement</th><th>Authority</th><th>Source</th><th>Status</th>
</tr></thead><tbody>
{rows}
</tbody></table></div>
<p class="muted"><strong>Status key:</strong> <span class="badge badge-ok">Verified</span> read directly in the cited official source &middot; <span class="badge badge-ok">Verified (dataset)</span> counted from an official dataset &middot; <span class="badge badge-note">Analysis</span> this project's reasoning, labelled as such and excluded from the verified count.</p>

<h2>How the layers interact</h2>
<ul>
<li><strong>Local binds hardest.</strong> San Francisco's 1.6% is lower than the state cap, so the local number is the operative ceiling, and the local licence condition has no state equivalent.</li>
<li><strong>State fills the gaps the ordinance leaves.</strong> Service method, the 10%/90-day notice split and the emergency price-gouging ceiling come from the Civil Code and Penal Code, not from Chapter 37.</li>
<li><strong>Federal sets conduct, not price.</strong> The Fair Housing Act governs who you may discriminate against; it does not cap rent.</li>
</ul>
""".format(
        n=len(FACTS),
        opts=opts,
        rows="".join(
            "<tr data-group=\"%s\">%s</tr>" % (FACTS[i]["level"].lower(), "".join(
                '<td%s>%s</td>' % (' class="num"' if j == 0 else "", c) for j, c in enumerate(r)
            ))
            for i, r in enumerate(rows)
        ),
    )
    return body


# ---------------------------------------------------------------- questions page

def questions_body():
    out = []
    for q in QUESTIONS:
        pts = "".join("<li>%s</li>" % escape(p) for p in q["points"])
        note = (
            '<p class="muted"><strong>Note:</strong> %s</p>' % escape(q["analysis_note"])
            if q.get("analysis_note")
            else ""
        )
        out.append(
            """<div class="card anchor" id="{qid}">
<p class="kicker">{qid}</p>
<h2 style="margin-top:0;border:none;padding:0">{q}</h2>
<div class="answer"><div class="v">{v}</div></div>
{status}
<ul>{pts}</ul>
{note}
<p class="muted"><strong>Sources:</strong> {srcs}</p>
</div>""".format(
                qid=q["id"],
                q=escape(q["question"]),
                v=escape(q["verdict"]),
                status=status_badge(q["status"]),
                pts=pts,
                note=note,
                srcs=src_links(q["sources"]),
            )
        )
    body = """
<p class="kicker">Questions</p>
<h1>Your questions, answered against the sources</h1>
<p class="lede">{intro}</p>
{dash}
{qs}
""".format(
        intro=escape(load("questions.json")["intro"]),
        dash='<p class="muted">' + " &middot; ".join('<a href="#%s">%s</a>' % (q["id"], q["id"]) for q in QUESTIONS) + "</p>",
        qs="".join(out),
    )
    return body


# ---------------------------------------------------------------- sources page

def sources_body():
    rows = []
    for s in load("sources.json")["sources"]:
        rows.append(
            [
                '<span class="anchor" id="%s"></span><strong>%s</strong>' % (s["id"], s["id"]),
                escape(s["publisher"]),
                escape(s["title"]) + '<br><span class="tag">%s</span>' % escape(s["type"]),
                '<a href="%s" rel="noopener">%s</a>' % (s["url"], escape(s["url"][:78] + ("..." if len(s["url"]) > 78 else ""))),
                escape(s["verifies"]),
            ]
        )
    body = """
<p class="kicker">Sources</p>
<h1>Source register</h1>
<p class="lede">Every source is a government publication: the City and County of San Francisco (including Rent Board forms and the Chapter 37 ordinance PDF), the California Legislative Information service, HUD, HUD USER and SF Open Data. All were retrieved and read on {today}.</p>
<div class="stopbox"><p><strong>Excluded on purpose.</strong> Law-firm blogs, property-management marketing pages, rent-calculator sites and forum posts appeared in search results and were <em>not</em> used to support any row. Where they made a claim this project could not confirm - such as a licence "application" - the correction is recorded on the <a href="flagged.html">Flagged for Review</a> page instead.</p></div>
{rows}
<h2>How a row gets a source link</h2>
<p>Fact rows, process steps, scenarios and question answers all carry short source tags such as {ex}. Each tag jumps to the matching entry above, which states exactly what that document verifies. A row with no confirmable source was not written into a table at all - it was moved to the flagged register.</p>
""".format(
        today=TODAY.strftime("%B %-d, %Y"),
        rows=table(["ID", "Publisher", "Document", "Link", "What it verifies"], rows),
        ex=src_links(["S01"]),
    )
    return body


# ---------------------------------------------------------------- flagged page

def flagged_body():
    items = []
    for f in FLAGGED["items"]:
        hard = f["category"] in ("Conflicting official sources", "Unverified input", "Open question")
        items.append(
            """<div class="flagitem anchor {cls}" id="{id}">
<div class="id">{id} &middot; {cat}</div>
<h3>{title}</h3>
<p><strong>What we found.</strong> {detail}</p>
<p><strong>Why it matters.</strong> {why}</p>
<p><strong>Suggested action.</strong> {action}</p>
<p class="muted"><strong>Sources:</strong> {srcs}</p>
</div>""".format(
                cls="" if hard else "amber",
                id=f["id"],
                cat=escape(f["category"]),
                title=escape(f["title"]),
                detail=escape(f["detail"]),
                why=escape(f["why_it_matters"]),
                action=escape(f["action"]),
                srcs=src_links(f["sources"]),
            )
        )
    body = """
<p class="kicker">Flagged for review</p>
<h1>{n} items for you to review</h1>
<p class="lede">{intro}</p>
<div class="warnbox">
<p><strong>Nothing on this page blocks publication.</strong> The site is published with these items clearly marked so you can decide what to do with each one. Red-edged items are conflicting or unconfirmable facts; amber-edged items are method limits, retrieval failures and reasoning limits.</p>
</div>
<div class="card"><h3 style="margin-top:0">The three that change a dollar figure</h3>
<ul>
<li><a href="#FL-01"><strong>FL-01</strong></a> - the base rents are your inputs. Nothing can be checked without the lease file.</li>
<li><a href="#FL-03"><strong>FL-03</strong></a> - the 24-month banking conflict decides whether Unit 1 is {u1safe} or {u1bank}.</li>
<li><a href="#FL-05"><strong>FL-05</strong></a> - whether a §6.14 notice was served on Unit 1's new co-tenant decides a future market reset.</li>
</ul></div>
{items}
""".format(
        n=len(FLAGGED["items"]),
        intro=escape(FLAGGED["intro"]),
        items="".join(items),
        u1safe=money(U1_SAFE["dollar"]),
        u1bank=money(U1_BANK["dollar"]),
    )
    return body


# ---------------------------------------------------------------- method page

def method_body():
    by_level = {"Local": 0, "State": 0, "Federal": 0}
    for f in FACTS:
        by_level[f["level"]] = by_level.get(f["level"], 0) + 1
    body = """
<p class="kicker">Method</p>
<h1>How this was built, and what it cannot do</h1>

<h2>Verification protocol</h2>
<ol>
<li><strong>Primary sources only.</strong> City ordinance text and Rent Board publications, California statutes on leginfo, HUD pages, and the City's open-data API. Secondary commentary was used only to generate questions, never to answer them.</li>
<li><strong>Read the text, not the summary.</strong> Where a page summarised a rule, the underlying section was pulled. Example: the 1.6% figure comes from Form 571 and is corroborated by §37.3(a)(1); the banking rule came from §37.3(a)(2) in the ordinance PDF, which is where the conflict with the website text showed up.</li>
<li><strong>Row-level citation.</strong> Every row carries a tag that resolves to the exact document on the Sources page, with a note stating what that document verifies.</li>
<li><strong>No fill-ins.</strong> If a value could not be confirmed it was left out of the tables. It is on the Flagged for Review page instead. That includes the federal rent ceiling question, the ACS median, and the HUD FMR figures.</li>
<li><strong>Arithmetic is generated, not typed.</strong> Percentages live in data/units.json with their Form 571 source; build.py multiplies them against the base rents. There is no hand-entered dollar figure in the data files.</li>
</ol>

<h2>Verification counts</h2>
{counts}
<p class="muted">"Analysis" rows are reasoning steps - for example that no reviewed source requires uniform increases. They are labelled, never mixed into the verified count.</p>

<h2>Privacy handling</h2>
<ul>
<li>This repository is public, so personal information is not stored in it. Tenant names are replaced with letters (Tenant A-F). No address, no initials, no dates of birth, no contact details.</li>
<li>Dates and amounts are kept exactly as supplied, because they carry the legal meaning.</li>
<li>Nothing in this project was published to any third-party service; the site is static files served by GitHub Pages.</li>
</ul>

<h2>Known limits</h2>
<ul>
<li><strong>Coverage is assumed, not proven.</strong> The 1940 build year and the unit count are your inputs (FL-02). If either unit is a single-family home or condominium, the local cap does not apply at all.</li>
<li><strong>Base rents are your inputs</strong> (FL-01). Every dollar figure inherits any error in them.</li>
<li><strong>Banking has an unresolved conflict</strong> inside official guidance (FL-03).</li>
<li><strong>Market context is neighbourhood-level and self-reported</strong>, not ZIP-level and not asking rents (FL-04).</li>
<li><strong>This is not legal advice</strong> and no attorney-client relationship exists. The Rent Board counsellor line (415-252-4600) answers these questions for free; a landlord-tenant attorney should review anything before a notice is served.</li>
</ul>

<h2>Reproducing the build</h2>
<p>Static site, no dependencies: <code>python3 build.py</code> writes <code>docs/</code> from <code>data/*.json</code>. <code>python3 tools/check_links.py</code> verifies every internal link and every external row URL.</p>
""".format(
        counts=table(
            ["Layer", "Rows verified", "Notes"],
            [
                ["Local (San Francisco)", by_level["Local"], "Rent Ordinance Chapter 37, Rent Board forms and pages, SF Open Data"],
                ["State (California)", by_level["State"], "Civil Code, Government Code, Penal Code, chaptered bills on leginfo"],
                ["Federal", by_level["Federal"], "HUD Fair Housing Act overview; HUD FMR page reviewed but values unretrievable"],
                ["Analysis rows", sum(1 for f in FACTS if f["status"] == "analysis"), "Labelled reasoning, excluded from the verified count"],
            ],
            numeric_cols=(1,),
        )
    )
    return body


# ---------------------------------------------------------------- write

def write(path, content):
    full = os.path.join(DOCS, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)


def main():
    if os.path.isdir(DOCS):
        shutil.rmtree(DOCS)
    os.makedirs(os.path.join(DOCS, "assets"), exist_ok=True)
    write("assets/style.css", CSS)
    write("assets/app.js", JS)
    write(".nojekyll", "")

    pages = [
        ("index.html", "Dashboard", index_body(), "Two rent-controlled units, Outer Sunset, ZIP 94122"),
        ("executive-summary.html", "Executive Summary", exec_body(), "Licence question first"),
        ("process.html", "Licence and Process", process_body(), "Report, licence, calculate, notice, serve"),
        ("units.html", "Unit Analysis", units_body(), "Unit 1 and Unit 2"),
        ("market.html", "Market Context", market_body(), "Rate history and reported rents"),
        ("questions.html", "Questions", questions_body(), "Direct answers with sources"),
        ("sources.html", "Sources", sources_body(), "%d official documents" % N_SOURCES),
        ("findings.html", "Findings", findings_body(), "%d verified requirements" % N_VERIFIED),
        ("flagged.html", "Flagged for Review", flagged_body(), "Unverified and conflicting items"),
        ("method.html", "Method", method_body(), "Verification protocol and limits"),
    ]
    for slug, title, body, sub in pages:
        write(slug, page(slug, title, body, sub))

    # companion markdown for offline reading / diffing
    md = ["# Executive summary - SF rent increase (Outer Sunset, ZIP 94122)", "",
          "Prepared %s. Research work product, not legal advice." % TODAY.strftime("%B %-d, %Y"), ""]
    write_md = os.path.join(ROOT, "EXECUTIVE-SUMMARY.md")
    rows = []
    for item in UNITS:
        for c in item["calc"]:
            rows.append("| %s | %s | %s | %s | %s | %s | %s |" % (
                item["unit"]["label"], c["sc"]["name"], pct(c["pct"]), money(c["dollar"]),
                money(c["new_rent"]), "%d days" % c["notice"], human(c["latest"])))
    md += [
        "## 1. The Rent Board licence question", "",
        "You do need a rent increase licence, but there is **no application** and nothing is sent to the Rent Board in advance.",
        "Reporting each unit in the **Housing Inventory** (annual, free, due March 1) generates the licence automatically for a tenant-occupied unit.",
        "The licence must be **in effect on the effective date** of the increase; without it the licence is suspended and the tenant is not obligated to pay the increase (SF Admin Code 37.15(e)).",
        "Being an individual owner rather than a corporation changes nothing: Chapter 37 applies to 'owners' with no size or entity threshold.", "",
        "## 2. Allowable increase", "",
        "- 1.6% for effective dates 2026-03-01 to 2027-02-28 (Rent Board Form 571).",
        "- One increase per 12 months, on the anniversary date; first available 12 months after the lease began.",
        "- Percentages for skipped years are added, never compounded; no rounding up; calculate on base rent only.",
        "- Anything above the cap needs a Rent Board petition filed before the notice.", "",
        "## 3. Scenarios", "",
        "| Unit | Scenario | Total % | Monthly increase | New rent | Notice | Serve by (personal) |",
        "|---|---|---|---|---|---|---|",
    ] + rows + [
        "",
        "## 4. The conflict to resolve before relying on Unit 1's higher figure", "",
        "sf.gov's banking page says a skipped increase banks only after **24 full months** without any increase; SF Admin Code 37.3(a)(2) has no such condition and the Rent Board's own examples bank after **12 months**. Flagged as FL-03; ask a Rent Board counsellor in writing.", "",
        "## 5. One unit or both", "",
        "No reviewed source requires raising both units or raising them equally. What is prohibited is discrimination on a protected ground (FEHA 12955; federal Fair Housing Act) and bad-faith pressure to vacate (SF Admin Code 37.10B(a)(5), (a)(9)). The two tenancies are in materially different positions, so uniform treatment is the weaker strategy.", "",
        "## 6. Flagged for review", "",
    ]
    for f in FLAGGED["items"]:
        md.append("- **%s** %s (%s)" % (f["id"], f["title"], f["category"]))
    md += ["", "Full detail, with sources, on the published site's Flagged for Review page.", ""]
    with open(write_md, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))

    print("Built %d pages into docs/" % len(pages))
    print("Verified rows: %d | analysis rows: %d | sources: %d | flagged: %d"
          % (N_VERIFIED, N_ANALYSIS, N_SOURCES, N_FLAGS))
    for item in UNITS:
        for c in item["calc"]:
            print("  %s %-3s %6s -> %s (new rent %s), notice %d days, serve by %s"
                  % (item["unit"]["label"], c["sc"]["id"], pct(c["pct"]), money(c["dollar"]),
                     money(c["new_rent"]), c["notice"], c["latest"]))


if __name__ == "__main__":
    main()
