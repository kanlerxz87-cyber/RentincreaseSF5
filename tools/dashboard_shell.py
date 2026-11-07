"""Shared layout, navigation and styles for the static site."""

import html
import os

CSS = """
:root{
  --bg:#f5f7fa; --panel:#ffffff; --ink:#1a2233; --muted:#5b6779;
  --line:#e2e8f0; --accent:#0b5394; --accent-soft:#eaf2fb;
  --ok:#0f7b4f; --ok-soft:#e7f6ee;
  --warn:#8a5a00; --warn-soft:#fdf3dd;
  --bad:#a3231d; --bad-soft:#fdecea;
  --radius:10px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font:15px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
a{color:var(--accent)}
a:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.wrap{display:flex;min-height:100vh;align-items:flex-start}
nav.side{
  width:262px;flex:0 0 262px;background:#0f1b2d;color:#c9d6e5;
  position:sticky;top:0;height:100vh;overflow-y:auto;padding:18px 0 40px;
}
nav.side .brand{padding:6px 20px 16px;border-bottom:1px solid #22344d;margin-bottom:10px}
nav.side .brand b{display:block;color:#fff;font-size:15px;letter-spacing:.2px}
nav.side .brand span{display:block;font-size:11.5px;color:#7f93aa;margin-top:3px}
nav.side .sec{padding:12px 20px 4px;font-size:10.5px;letter-spacing:.9px;
  text-transform:uppercase;color:#6d819a}
nav.side a{display:block;padding:7px 20px;color:#c9d6e5;text-decoration:none;
  font-size:13.5px;border-left:3px solid transparent}
nav.side a:hover{background:#16253a;color:#fff}
nav.side a.active{background:#16253a;color:#fff;border-left-color:#4ea1f7;font-weight:600}
main{flex:1 1 auto;min-width:0;padding:26px 34px 70px;max-width:1180px}
h1{font-size:25px;margin:0 0 6px;letter-spacing:-.2px}
h2{font-size:18px;margin:30px 0 10px;padding-bottom:7px;border-bottom:2px solid var(--line)}
h3{font-size:15px;margin:20px 0 8px}
p{margin:9px 0}
.lede{color:var(--muted);font-size:14.5px;margin:0 0 18px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);
  padding:18px 20px;margin:14px 0;box-shadow:0 1px 2px rgba(16,32,56,.04)}
.card.tight{padding:14px 16px}
.grid{display:grid;gap:14px}
.g2{grid-template-columns:repeat(2,1fr)}
.g3{grid-template-columns:repeat(3,1fr)}
.g4{grid-template-columns:repeat(4,1fr)}
@media(max-width:980px){.g3,.g4{grid-template-columns:repeat(2,1fr)}}
@media(max-width:760px){
  .wrap{flex-direction:column}
  nav.side{width:100%;flex:none;height:auto;position:static}
  main{padding:18px}
  .g2,.g3,.g4{grid-template-columns:1fr}
}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);padding:14px 16px}
.kpi .k{font-size:11px;text-transform:uppercase;letter-spacing:.7px;color:var(--muted)}
.kpi .v{font-size:23px;font-weight:700;margin:5px 0 2px;letter-spacing:-.4px}
.kpi .s{font-size:12px;color:var(--muted)}
table{width:100%;border-collapse:collapse;margin:10px 0;background:var(--panel);
  font-size:13.5px;border:1px solid var(--line)}
caption{text-align:left;font-size:12.5px;color:var(--muted);padding:6px 0}
th,td{padding:9px 11px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
thead th{background:#f0f4f9;font-size:12px;text-transform:uppercase;letter-spacing:.5px;
  color:#3c4a5e;border-bottom:2px solid var(--line);position:sticky;top:0}
tbody tr:hover{background:#fafcfe}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.tw{overflow-x:auto;max-width:100%}
.pill{display:inline-block;padding:2px 8px;border-radius:999px;font-size:11.5px;
  font-weight:600;white-space:nowrap}
.pill.ok{background:var(--ok-soft);color:var(--ok)}
.pill.warn{background:var(--warn-soft);color:var(--warn)}
.pill.bad{background:var(--bad-soft);color:var(--bad)}
.pill.info{background:var(--accent-soft);color:var(--accent)}
.note{border-left:4px solid var(--accent);background:var(--accent-soft);padding:11px 14px;
  border-radius:0 8px 8px 0;margin:14px 0;font-size:14px}
.note.warn{border-color:#d99b00;background:var(--warn-soft)}
.note.bad{border-color:var(--bad);background:var(--bad-soft)}
.note.ok{border-color:var(--ok);background:var(--ok-soft)}
.note b{display:block;margin-bottom:3px}
.steps{counter-reset:s;list-style:none;padding:0;margin:10px 0}
.steps li{counter-increment:s;position:relative;padding:0 0 16px 44px;
  border-left:2px solid var(--line);margin-left:13px}
.steps li:last-child{border-left-color:transparent;padding-bottom:0}
.steps li::before{content:counter(s);position:absolute;left:-14px;top:0;width:27px;height:27px;
  background:var(--accent);color:#fff;border-radius:50%;display:flex;align-items:center;
  justify-content:center;font-size:13px;font-weight:700}
.steps li b{display:block;margin-bottom:2px}
.steps li .meta{font-size:12.5px;color:var(--muted)}
ul.tight{margin:8px 0;padding-left:20px}
ul.tight li{margin:4px 0}
code{background:#eef2f7;padding:1.5px 5px;border-radius:4px;font-size:12.5px;
  font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.src{font-size:11.5px;white-space:nowrap}
.src a{text-decoration:none;border-bottom:1px dotted var(--accent)}
.src a:hover{border-bottom-style:solid}
footer{margin-top:40px;padding-top:16px;border-top:1px solid var(--line);
  color:var(--muted);font-size:12.5px}
.topnav{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.topnav a{font-size:12px;background:var(--panel);border:1px solid var(--line);
  padding:5px 10px;border-radius:999px;text-decoration:none;color:var(--muted)}
.topnav a:hover{border-color:var(--accent);color:var(--accent)}
.muted{color:var(--muted)}
.small{font-size:12.5px}
.big{font-size:16px}
.nowrap{white-space:nowrap}
"""

NAV = [
    ("Overview", [
        ("index.html", "Executive summary"),
    ]),
    ("The license question", [
        ("license.html", "Do I need the Rent Board license?"),
        ("steps.html", "Step-by-step checklist"),
    ]),
    ("The numbers", [
        ("allowable.html", "Allowable increase rates"),
        ("units.html", "Unit ledgers &amp; scenarios"),
        ("notice.html", "How to notify tenants"),
    ]),
    ("Going further", [
        ("passthroughs.html", "Petitions &amp; passthroughs"),
        ("owners.html", "Corporate vs. individual owners"),
        ("fair-housing.html", "Discrimination risk: one or both?"),
    ]),
    ("Reference", [
        ("laws.html", "Federal / state / local law"),
        ("flagged.html", "Flagged for review"),
        ("sources.html", "Source registry"),
    ]),
]


def nav_html(current):
    out = ['<div class="brand"><b>Rent Increase &mdash; SF</b>'
           '<span>Outer Sunset &middot; ZIP 94122 &middot; research dashboard</span></div>']
    for section, items in NAV:
        out.append('<div class="sec">{}</div>'.format(section))
        for path, label in items:
            cls = ' class="active"' if path == current else ""
            out.append('<a href="{}"{}>{}</a>'.format(path, cls, label))
    return "\n".join(out)


def esc(s):
    return html.escape(str(s), quote=False)


def page(title, current, body, subtitle=None):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} &middot; SF Rent Increase Research</title>
<meta name="description" content="San Francisco rent increase research dashboard: Rent Board license, allowable increases, notice rules and unit-by-unit calculations, each row sourced to an official government page.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<div class="wrap">
<nav class="side">
{nav}
</nav>
<main>
<h1>{title}</h1>
{sub}
{body}
<footer>
  <p><b>Every figure on this site is tied to an official government source.</b>
  Anything that could not be confirmed from an official source is left blank and
  listed on the <a href="flagged.html">Flagged for review</a> page.</p>
  <p class="small">Tenant names and all personal details are anonymized. Dates and
  dollar amounts are unchanged. This is research, not legal advice &mdash; confirm
  with a San Francisco Rent Board counselor (415-252-4600, weekdays 9am&ndash;12pm
  and 1&ndash;4pm) before serving any notice.</p>
</footer>
</main>
</div>
</body>
</html>
""".format(title=title, nav=nav_html(current), body=body,
           sub='<p class="lede">{}</p>'.format(subtitle) if subtitle else "")


def write(docs_dir, filename, content):
    path = os.path.join(docs_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
