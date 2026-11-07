#!/usr/bin/env python3
"""Build the independent evidence register (evidence/) from tools/data.py.

Offline and deterministic.  Run from anywhere:  python3 evidence/tools/build_evidence.py

Writes (inside evidence/):
  register.csv, allowable_increases_official.csv, calculations.csv, audit-findings.csv,
  index.html, register.html, calculations.html
Checks (exit status 1 if any fails):
  * register schema, status vocabulary, unique ids
  * verified rows carry a value and a verbatim excerpt; unverified / owner-reported rows have a blank value
  * every source_url is https on the official-host allowlist
  * the rate table is contiguous 1982-2027 and has 46 rows (Form 571 lists 46 periods)
  * the banking model (Rent Board Rule 4.12(a)) reproduces the Rent Board's own four worked examples
  * when the repository's data/allowable-increases.csv and data/allowance-ledger.csv exist, they match Form 571 (blank placeholder rows are accepted)
  * no tenant identifiers: only placeholder unit labels are used (leak-greps with real names are run
    by hand and are never written to a file)
"""
import calendar
import csv
import html
import re
import sys
from datetime import date, timedelta
from decimal import Decimal, ROUND_DOWN
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import data  # noqa: E402

OUT = HERE.parent                      # evidence/
REPO = OUT.parent                      # repository root
VERIFIED_AT = data.VERIFIED_AT
ERRORS = []


def fail(msg):
    ERRORS.append(msg)
    print("FAIL:", msg)


# ----------------------------------------------------------------------------- parsing
REG_FIELDS = ["id", "category", "finding", "value", "status", "source_url", "source_title",
              "publisher", "source_type", "excerpt", "notes", "owner_reported_value"]
AUD_FIELDS = ["id", "severity", "title", "where_published", "published_statement",
              "official_finding", "register_refs", "requested_action", "file_owner", "status"]


def parse_table(text, fields):
    rows = []
    for ln in text.strip().splitlines():
        parts = re.split(r"\s*\|\|\|\s*", ln.strip())
        if len(parts) > len(fields):
            fail(f"too many fields in row {parts[0]}")
            continue
        parts += [""] * (len(fields) - len(parts))
        rows.append(dict(zip(fields, parts)))
    return rows


REGISTER = parse_table(data.REGISTER_TEXT, REG_FIELDS)
AUDIT = parse_table(data.AUDIT_TEXT, AUD_FIELDS)
for r in REGISTER:
    if r["source_url"].startswith("@"):
        r["source_url"] = data.URLS[r["source_url"][1:]]
    r["verified_at"] = VERIFIED_AT
BY_ID = {r["id"]: r for r in REGISTER}


def yy(y):
    y = int(y)
    return 1900 + y if y >= 82 else 2000 + y


RATE_RE = re.compile(r"^(\*?)(\d{1,2})/(\d{1,2})/(\d{2}) – (\d{1,2})/(\d{1,2})/(\d{2})$")


def parse_rates():
    out = []
    for ln in data.RATES_TEXT.strip().splitlines():
        period, pct = [x.strip() for x in ln.split("|")]
        m = RATE_RE.match(period)
        if not m:
            fail(f"bad period {period}")
            continue
        star, m1, d1, y1, m2, d2, y2 = m.groups()
        out.append({"period": period.lstrip("*"), "special": bool(star),
                    "start": date(yy(y1), int(m1), int(d1)), "end": date(yy(y2), int(m2), int(d2)),
                    "percent": Decimal(pct)})
    return out


RATES = parse_rates()


def rate_for(d):
    for r in RATES:
        if r["start"] <= d <= r["end"]:
            return r["percent"]
    return None


# ----------------------------------------------------------------------------- model
def add_months(d, n):
    y = d.year + (d.month - 1 + n) // 12
    m = (d.month - 1 + n) % 12 + 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def months_between(a, b):
    return (b.year - a.year) * 12 + (b.month - a.month) - (1 if b.day < a.day else 0)


def banking(start, eff):
    """Rule 4.12(a) model: an anniversary increase becomes bankable once a full 12 months have elapsed from
    the date it could first be imposed; the annual increase in effect on the effective date is separate.
    Assumes no increase has been imposed since `start`."""
    res = {"eligible": eff >= add_months(start, 12), "items": [], "banked": Decimal("0"), "annual": None}
    if not res["eligible"]:
        return res
    k = 1
    while True:
        a = add_months(start, 12 * k)
        due = add_months(a, 12)
        if due > eff:
            break
        pct = rate_for(a)
        res["items"].append({"available": a, "bankable_from": due, "percent": pct})
        res["banked"] += pct if pct is not None else Decimal("0")
        k += 1
    res["annual"] = rate_for(eff)
    return res


def loose_banked(start, eff):
    """Alternative reading used only as a test: bank every skipped anniversary before eff once 24 months
    have passed since the last increase."""
    if months_between(start, eff) < 24:
        return Decimal("0")
    total, k = Decimal("0"), 1
    while True:
        a = add_months(start, 12 * k)
        if a >= eff:
            break
        total += rate_for(a) or Decimal("0")
        k += 1
    return total


def cents(x):
    return x.quantize(Decimal("0.01"), rounding=ROUND_DOWN)


def money(x):
    return f"${x:,.2f}"


def pct_txt(x):
    return f"{x.normalize():f}%" if x == x.to_integral() else f"{x}%"


def notice_days(total_pct):
    return 90 if total_pct > Decimal("10") else 30


def iso(d):
    return d.isoformat()


EXAMPLE_RESULTS = []
for ex_id, label, st, ef, base, e_banked, e_annual, e_new, src in data.OFFICIAL_EXAMPLES:
    s, e = date.fromisoformat(st), date.fromisoformat(ef)
    b = banking(s, e)
    base_d = Decimal(base)
    total = b["banked"] + (b["annual"] or Decimal("0"))
    new_rent = base_d + cents(base_d * total / 100)
    loose_total = loose_banked(s, e) + (b["annual"] or Decimal("0"))
    loose_new = base_d + cents(base_d * loose_total / 100)
    ok = (b["banked"] == Decimal(e_banked) and b["annual"] == Decimal(e_annual) and new_rent == Decimal(e_new))
    loose_ok = loose_new == Decimal(e_new)
    EXAMPLE_RESULTS.append({"id": ex_id, "label": label, "start": st, "effective": ef, "base": base_d,
                            "official_banked": e_banked, "official_annual": e_annual, "official_new": Decimal(e_new),
                            "model_banked": b["banked"], "model_annual": b["annual"], "model_new": new_rent,
                            "model_ok": ok, "loose_new": loose_new, "loose_ok": loose_ok, "source": src})
    if not ok:
        fail(f"banking model disagrees with official example {ex_id}")

# ----------------------------------------------------------------------------- scenarios
U1_BASE, U1_START = Decimal("3995.00"), date(2025, 2, 1)
U2_BASE, U2_START = Decimal("3150.00"), date(2019, 6, 1)
CAP = Decimal("10")


def scenario(cid, unit, label, base, start, eff, *, use_banked=True, partial_annual_only=False,
             cap_mode=None, notes="", refs=""):
    b = banking(start, eff)
    annual = b["annual"]
    banked_pct = b["banked"] if use_banked else Decimal("0")
    unpublished = annual is None
    deferred = Decimal("0")
    cap_amount = None
    banked_amt = cents(base * banked_pct / 100)
    annual_amt = cents(base * (annual or Decimal("0")) / 100)
    if cap_mode:
        cap_amount = cents(base * CAP / 100)
        if banked_amt > cap_amount:
            deferred = banked_amt - cap_amount
            banked_amt = cap_amount
        if cap_mode == "annual-inside":
            annual_amt = min(annual_amt, cap_amount - banked_amt)
    inc = banked_amt + annual_amt
    total_pct = (inc / base * 100) if base else Decimal("0")
    days = notice_days(total_pct)
    row = {
        "id": cid, "unit": unit, "scenario": label, "base_rent": money(base), "tenancy_start": iso(start),
        "effective_date": iso(eff),
        "banked_pct": pct_txt(banked_pct) if not cap_mode else f"{pct_txt(b['banked'])} (capped)",
        "annual_pct": "unpublished" if unpublished else pct_txt(annual),
        "increase_amount": ("at least " if unpublished else "") + money(inc),
        "new_rent": ("at least " if unpublished else "") + money(base + inc),
        "total_pct": ("at least " if unpublished else "") + f"{total_pct.quantize(Decimal('0.01'))}%",
        "notice_days": days, "serve_by_personal": iso(eff - timedelta(days=days)),
        "serve_by_mail": iso(eff - timedelta(days=days + 5)),
        "status": "calculated", "refs": refs, "notes": notes,
        "_schedule": b["items"], "_deferred": deferred,
    }
    return row


TODAY = date(2026, 11, 7)
CALCS = [
    scenario("CALC-01", "Unit 1", "Annual increase only, effective before 2027-02-01 (example date); the 1.4% available 2026-02-01 is forfeited and the anniversary moves",
             U1_BASE, U1_START, date(2026, 12, 15), use_banked=True,
             notes="Earlier than 12 months after 2026-02-01, so nothing banks. Earliest possible effective date with 30 days' personal notice served 2026-11-07 is 2026-12-07.",
             refs="INC-01, INC-05, INC-06, INC-07, INC-09"),
    scenario("CALC-02", "Unit 1", "Banked 1.4% plus annual 1.6%, effective on the second anniversary of the lease start",
             U1_BASE, U1_START, date(2027, 2, 1),
             notes="1.4% became available 2026-02-01 and banks once 12 full months have passed (2027-02-01). The same date satisfies the banked page's 24-month wording. Notice must itemize annual vs banked.",
             refs="INC-01, INC-07, INC-08, INC-12, NTC-06, NTC-09"),
    scenario("CALC-03", "Unit 1", "Annual 1.6% only on 2027-02-01, leaving the 1.4% banked for a later increase",
             U1_BASE, U1_START, date(2027, 2, 1), use_banked=False,
             notes="Partial increases are allowed and the rest is banked (INC-11). The banked 1.4% would later be exposed to any enacted cap (PND-02).",
             refs="INC-11, INC-10, PND-02"),
    scenario("CALC-04", "Unit 2", "Six years of banked increases (11.5%) plus annual 1.6%, effective in the 2026-27 rate window",
             U2_BASE, U2_START, date(2027, 2, 15),
             notes="Assumes no increase since 2019-06-01 (OWN-03). Over 10% in total, so 90 days' notice (95 if mailed). The 1.6% is the rate in effect on the effective date. Subject to the pending cap if File 261020 is enacted as introduced (CALC-06, CALC-07).",
             refs="INC-01, INC-07, INC-10, NTC-01, NTC-03, NTC-06, OWN-03"),
    scenario("CALC-05", "Unit 2", "All seven anniversary increases banked (13.1%) plus the unpublished 2027-28 annual rate, effective on the lease anniversary",
             U2_BASE, U2_START, date(2027, 6, 1),
             notes="The annual rate for 3/1/2027 onward is not yet published (INC-13), so only the banked minimum can be shown. Keeps the 1 June anniversary date.",
             refs="INC-07, INC-13, NTC-05"),
    scenario("CALC-06", "Unit 2", "If File 261020 is enacted as introduced: banked part capped at 10% of base rent, annual 1.6% outside the cap (literal reading)",
             U2_BASE, U2_START, date(2027, 2, 15), cap_mode="annual-outside",
             notes="Scenario only; not law. Cap = 10% x lowest base rent in prior 12 months ($3,150.00). The 1.5% excess ($47.25) could be imposed on or after 2030-01-01 'as otherwise permitted by law'. Whether the annual increase sits outside the cap is unverified (PND-05).",
             refs="PND-01, PND-02, PND-03, PND-05, PND-06"),
    scenario("CALC-07", "Unit 2", "If File 261020 is enacted as introduced: annual 1.6% counted inside the 10% cap (alternative reading)",
             U2_BASE, U2_START, date(2027, 2, 15), cap_mode="annual-inside",
             notes="Scenario only; not law. Same cap, with the annual increase counted inside it, giving exactly 10% and a 30-day notice. See PND-05.",
             refs="PND-02, PND-05"),
    scenario("CALC-08", "Unit 2", "Annual 1.6% only, effective 2027-02-15 (all banked amounts left unused)",
             U2_BASE, U2_START, date(2027, 2, 15), use_banked=False,
             notes="Unused banked amounts stay banked (INC-11) but would later be exposed to any enacted cap (PND-02). The anniversary becomes the effective date.",
             refs="INC-11, INC-06, PND-02"),
]
# fix CALC-01: 'banked' must be zero by construction; verify the model agrees
if CALCS[0]["banked_pct"] != "0%":
    fail("CALC-01 expected no banked amount")
if (CALCS[1]["total_pct"], CALCS[1]["increase_amount"], CALCS[1]["new_rent"]) != ("3.00%", "$119.85", "$4,114.85"):
    fail(f"CALC-02 unexpected: {CALCS[1]['total_pct']} {CALCS[1]['increase_amount']} {CALCS[1]['new_rent']}")
if (CALCS[0]["increase_amount"], CALCS[0]["new_rent"]) != ("$63.92", "$4,058.92"):
    fail("CALC-01 unexpected result")
if (CALCS[3]["total_pct"], CALCS[3]["increase_amount"], CALCS[3]["new_rent"]) != ("13.10%", "$412.65", "$3,562.65"):
    fail("CALC-04 unexpected result")

# ----------------------------------------------------------------------------- register checks
HOSTS = data.OFFICIAL_HOSTS
ids = [r["id"] for r in REGISTER]
if len(ids) != len(set(ids)):
    fail("duplicate register ids")
for r in REGISTER:
    u = urlsplit(r["source_url"])
    if u.scheme != "https" or u.hostname not in HOSTS:
        fail(f"{r['id']}: source_url not https on allowlist: {r['source_url']}")
    if r["status"] not in data.STATUSES:
        fail(f"{r['id']}: bad status {r['status']}")
    if r["status"] == "verified" and not (r["value"] and r["excerpt"]):
        fail(f"{r['id']}: verified row needs value and excerpt")
    if r["status"] in ("unverified", "owner-reported") and r["value"]:
        fail(f"{r['id']}: {r['status']} row must have a blank value")
    if r["status"] == "owner-reported" and not r["owner_reported_value"]:
        fail(f"{r['id']}: owner-reported row needs owner_reported_value")
for a in AUDIT:
    for ref in re.findall(r"\b[A-Z]{3,4}-\d\d\b", a["register_refs"]):
        if ref not in BY_ID:
            fail(f"{a['id']}: unknown register ref {ref}")
for c in CALCS:
    for ref in re.findall(r"\b[A-Z]{3,4}-\d\d\b", c["refs"]):
        if ref not in BY_ID:
            fail(f"{c['id']}: unknown register ref {ref}")

# rate table integrity
if len(RATES) != 46:
    fail(f"expected 46 rate rows (Form 571 lists 46 periods), found {len(RATES)}")
ordered = sorted(RATES, key=lambda r: r["start"])
for prev, nxt in zip(ordered, ordered[1:]):
    if nxt["start"] != prev["end"] + timedelta(days=1):
        fail(f"rate periods not contiguous between {prev['period']} and {nxt['period']}")

# cross-check with the repository's own CSVs (present once main is merged)
CROSSCHECK = []
rep_csv = REPO / "data" / "allowable-increases.csv"
led_csv = REPO / "data" / "allowance-ledger.csv"


def norm_period(s):
    s = html.unescape(s).replace("\u2013", "-").replace(" ", "")
    return s


def to_date(s):
    m, d, y = [int(x) for x in s.split("/")]
    return date(y if y > 99 else yy(y), m, d)


if rep_csv.exists():
    with open(rep_csv, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    mine = {(r["start"], r["end"]): r["percent"] for r in RATES}
    seen = set()
    bad = []
    placeholders = []
    for row in rows:
        if not row["increase_pct"].strip():          # a blank value is the correct way to show an unpublished rate
            placeholders.append(row["effective_period"])
            continue
        per = norm_period(row["effective_period"])
        try:
            s, e = per.lstrip("*").split("-", 1) if per.count("-") == 1 else (None, None)
            key = (to_date(s), to_date(e))
        except Exception:
            bad.append(f"unparseable period {row['effective_period']!r}")
            continue
        seen.add(key)
        if key not in mine:
            bad.append(f"period not in Form 571: {row['effective_period']}")
        elif Decimal(row["increase_pct"]) != mine[key]:
            bad.append(f"{row['effective_period']}: repo {row['increase_pct']} vs Form 571 {mine[key]}")
    missing = set(mine) - seen
    if missing:
        bad.append(f"{len(missing)} Form 571 periods absent from repo CSV")
    CROSSCHECK.append(("data/allowable-increases.csv", len(rows) - len(placeholders), bad, placeholders))
    for b_ in bad:
        fail("allowable-increases.csv: " + b_)
if led_csv.exists():
    with open(led_csv, newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    bad = []
    for row in rows:
        d = to_date(row["date_available"])
        want = rate_for(d)
        if want is None or Decimal(row["rate_pct"]) != want:
            bad.append(f"{row['unit']} {row['date_available']}: repo {row['rate_pct']} vs Form 571 {want}")
    CROSSCHECK.append(("data/allowance-ledger.csv", len(rows), bad, []))
    for b_ in bad:
        fail("allowance-ledger.csv: " + b_)

# ----------------------------------------------------------------------------- CSV output
def write_csv(path, fieldnames, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow(r)


write_csv(OUT / "register.csv",
          ["id", "category", "finding", "value", "status", "source_url", "verified_at", "notes", "excerpt",
           "source_title", "publisher", "source_type", "owner_reported_value"], REGISTER)
write_csv(OUT / "allowable_increases_official.csv",
          ["effective_period", "increase_pct", "start", "end", "special_1992_93_row", "status", "source_url", "verified_at"],
          [{"effective_period": r["period"], "increase_pct": str(r["percent"]), "start": iso(r["start"]),
            "end": iso(r["end"]), "special_1992_93_row": "yes" if r["special"] else "",
            "status": "verified", "source_url": data.URLS["PDF571"], "verified_at": VERIFIED_AT} for r in RATES])
write_csv(OUT / "calculations.csv",
          ["id", "unit", "scenario", "base_rent", "tenancy_start", "effective_date", "banked_pct", "annual_pct",
           "total_pct", "increase_amount", "new_rent", "notice_days", "serve_by_personal", "serve_by_mail",
           "status", "refs", "notes"], CALCS)
write_csv(OUT / "audit-findings.csv",
          ["id", "severity", "title", "where_published", "published_statement", "official_finding",
           "register_refs", "requested_action", "file_owner", "status"], AUDIT)

# ----------------------------------------------------------------------------- HTML
CSS = """
:root{--ink:#1b2430;--muted:#55606e;--line:#d5dbe3;--bg:#f6f8fa;--card:#fff;--link:#0b4f9c;
--ok:#0f6b3a;--okbg:#e4f5ea;--warn:#8a5300;--warnbg:#fff1d6;--own:#1f4e8c;--ownbg:#e3eefc;--calc:#5b3a8c;--calcbg:#efe7fa;--bad:#9b1c1c;--badbg:#fde8e8}
*{box-sizing:border-box}body{margin:0;font:16px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:var(--bg)}
a{color:var(--link)}a:focus,button:focus,summary:focus{outline:3px solid #ffbf47;outline-offset:2px}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:#fff;padding:6px 10px;z-index:9}
header.top{background:#12263f;color:#fff;padding:18px 20px}header.top h1{margin:0 0 4px;font-size:1.5rem}header.top p{margin:0;color:#cfd9e6}
nav.main{background:#fff;border-bottom:1px solid var(--line);padding:8px 20px;display:flex;flex-wrap:wrap;gap:6px 18px}
main{max-width:1240px;margin:0 auto;padding:18px 20px 40px}section{margin:0 0 30px}h2{font-size:1.25rem;margin:0 0 8px;border-bottom:2px solid var(--line);padding-bottom:4px}
h3{font-size:1.05rem;margin:18px 0 6px}.note{background:var(--warnbg);border:1px solid #f0cf8f;padding:10px 14px;border-radius:6px}
.box{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 16px}.muted{color:var(--muted)}
.wrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:8px}
table{border-collapse:collapse;width:100%;font-size:.9rem}caption{text-align:left;padding:8px 10px;font-weight:600}
th,td{border-top:1px solid var(--line);padding:7px 9px;vertical-align:top;text-align:left}thead th{background:#eef2f6;position:sticky;top:0}
td.num{text-align:right;white-space:nowrap}td.mono,.mono{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.82rem}
tr:target{outline:3px solid #ffbf47;background:#fff9e6}
.badge{display:inline-block;padding:1px 8px;border-radius:999px;font-size:.78rem;font-weight:600;white-space:nowrap}
.b-verified{background:var(--okbg);color:var(--ok)}.b-unverified{background:var(--warnbg);color:var(--warn)}
.b-owner-reported{background:var(--ownbg);color:var(--own)}.b-calculated{background:var(--calcbg);color:var(--calc)}
.sev-High{background:var(--badbg);color:var(--bad)}.sev-Medium{background:var(--warnbg);color:var(--warn)}.sev-Low,.sev-Info{background:#e9eef4;color:#33475b}
blockquote.x{margin:0;padding:0 0 0 8px;border-left:3px solid var(--line);color:#2d3947;font-size:.84rem}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}.cards .box strong{display:block;font-size:1.15rem}
ol.steps li{margin:6px 0}footer{border-top:1px solid var(--line);padding:14px 20px;color:var(--muted);font-size:.85rem;max-width:1240px;margin:0 auto}
details summary{cursor:pointer;font-weight:600;margin:8px 0}
@media print{nav.main,.skip{display:none}thead th{position:static}body{background:#fff}}
"""

SEV_ORDER = {"High": 0, "Medium": 1, "Low": 2, "Info": 3}


def e(s):
    return html.escape(str(s), quote=True)


def badge(status):
    return f'<span class="badge b-{e(status)}">{e(status)}</span>'


def link(url, text=None, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<a{c} href="{e(url)}" rel="noopener">{e(text or url)}</a>'


def nav(active):
    items = [("index.html", "Overview"), ("register.html", "Register"), ("calculations.html", "Calculations"),
             ("README.md", "Method"), ("register.csv", "register.csv"), ("../index.html", "Project home")]
    out = []
    for href, label in items:
        cur = ' aria-current="page"' if href == active else ""
        out.append(f'<a href="{e(href)}"{cur}>{e(label)}</a>')
    return '<nav class="main" aria-label="Evidence navigation">' + " ".join(out) + "</nav>"


def page(title, subtitle, body, active):
    n_ver = sum(1 for r in REGISTER if r["status"] == "verified")
    n_unv = sum(1 for r in REGISTER if r["status"] == "unverified")
    n_own = sum(1 for r in REGISTER if r["status"] == "owner-reported")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | Independent evidence register</title>
<meta name="description" content="Independent, official-source evidence register for a San Francisco rent increase review. Not legal advice.">
<style>{CSS}</style></head>
<body><a class="skip" href="#main">Skip to content</a>
<header class="top"><h1>{e(title)}</h1><p>{e(subtitle)}</p></header>
{nav(active)}
<main id="main">
<p class="note"><strong>Research, not legal advice.</strong> Every register row links to an official government source and was checked on {VERIFIED_AT} (UTC); audit rows link to the official evidence (or, for a finding about this repository, to the published page itself). Rows marked <em>unverified</em> have a blank value on purpose and are listed under <a href="index.html#flagged">Flagged for review</a>. This register does not certify that any increase is lawful; no lawyer or Rent Board staff reviewed it.</p>
{body}
</main>
<footer>Independent evidence register, session a872cd08, scope <span class="mono">evidence/**</span>. {len(REGISTER)} register rows: {n_ver} verified, {n_unv} unverified, {n_own} owner-reported; {len(CALCS)} calculated scenarios. No tenant names, initials or addresses appear here. Checked {VERIFIED_AT} UTC. Law and rates change: re-check before acting.</footer>
</body></html>
"""


def ref_links(refs):
    out = []
    for ref in re.findall(r"\b[A-Z]{3,4}-\d\d\b", refs):
        r = BY_ID[ref]
        out.append(f'<a href="register.html#{e(ref)}">{e(ref)}</a>&nbsp;(<a href="{e(r["source_url"])}" rel="noopener">official</a>)')
    return "; ".join(out)


def register_row(r):
    flagged = r["status"] in ("unverified", "owner-reported")
    status = badge(r["status"])
    if flagged:
        status = f'<a href="index.html#flagged" title="listed under Flagged for review">{status}</a>'
    value = e(r["value"]) if r["value"] else ('<span class="muted">(blank: not confirmed)</span>' if r["status"] == "unverified" else
                                                   '<span class="muted">(blank: owner-supplied)</span>')
    if r["owner_reported_value"]:
        value += f'<br><span class="muted">owner supplied: {e(r["owner_reported_value"])}</span>'
    ex = f'<blockquote class="x">{e(r["excerpt"])}</blockquote>' if r["excerpt"] else '<span class="muted">none: nothing confirmed to quote</span>'
    return (f'<tr id="{e(r["id"])}" data-row-id="{e(r["id"])}" data-status="{e(r["status"])}">'
            f'<th scope="row" class="mono">{e(r["id"])}</th><td>{e(r["category"])}</td><td>{e(r["finding"])}</td>'
            f'<td>{value}</td><td>{status}</td>'
            f'<td>{link(r["source_url"], r["source_title"])}<br><span class="muted">{e(r["publisher"])} &middot; {e(r["source_type"])}</span></td>'
            f'<td>{ex}</td><td>{e(r["notes"])}</td></tr>')


def build_register():
    heads = ["ID", "Category", "Finding", "Value", "Status", "Official source", "Verbatim excerpt", "Notes"]
    thead = "".join(f'<th scope="col">{h}</th>' for h in heads)
    tbody = "".join(register_row(r) for r in REGISTER)
    legend = ('<div class="box"><p><strong>Status legend.</strong> ' + badge("verified") + ' the value is stated by the linked official page; the excerpt is copied verbatim (ellipses mark omitted words). '
              + badge("unverified") + ' not confirmed: the value is blank and the link is the official place that was checked. '
              + badge("owner-reported") + ' supplied by the owner; it cannot be checked against public official data. '
              + badge("calculated") + ' arithmetic computed by script from verified inputs (see Calculations).</p></div>')
    body = (f'<section><h2>Register ({len(REGISTER)} rows)</h2>{legend}'
            f'<p><a href="register.csv">Download register.csv</a> &middot; columns: id, category, finding, value, status, source_url, verified_at, notes, excerpt, source_title, publisher, source_type, owner_reported_value.</p>'
            f'<div class="wrap"><table><caption>Every row links to an official source; unverified rows link to the official place that was checked</caption><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table></div></section>')
    return page("Evidence register", "All findings with verbatim excerpts and official links", body, "register.html")


def build_calcs():
    own = [BY_ID[i] for i in ("OWN-01", "OWN-02", "OWN-03", "OWN-04")]
    own_rows = "".join(
        f'<tr data-row-id="{e(r["id"])}"><th scope="row" class="mono"><a href="register.html#{e(r["id"])}">{e(r["id"])}</a></th><td>{e(r["finding"])}</td>'
        f'<td>{e(r["owner_reported_value"])}</td><td>{badge(r["status"])}</td><td>{link(r["source_url"], r["source_title"])}</td></tr>' for r in own)
    inputs = (f'<section><h2>Inputs</h2><p>These are the only facts about the property used here. They were supplied by the owner and could not be checked against public official data.</p>'
              f'<div class="wrap"><table><caption>Owner-reported inputs (unverified)</caption><thead><tr><th scope="col">ID</th><th scope="col">Input</th><th scope="col">Owner supplied</th><th scope="col">Status</th><th scope="col">Where it would be checked</th></tr></thead><tbody>{own_rows}</tbody></table></div></section>')

    heads = ["ID", "Unit", "Scenario", "Effective", "Banked (imposed)", "Annual", "Total", "Increase", "New base rent", "Notice", "Serve by (personal)", "Serve by (mail)", "Official basis"]
    rows = []
    for c in CALCS:
        rows.append(
            f'<tr id="{c["id"]}" data-row-id="{c["id"]}"><th scope="row" class="mono">{c["id"]}</th><td>{e(c["unit"])}</td><td>{e(c["scenario"])}<br><span class="muted">{e(c["notes"])}</span></td>'
            f'<td class="num">{c["effective_date"]}</td><td class="num">{e(c["banked_pct"])}</td><td class="num">{e(c["annual_pct"])}</td><td class="num">{e(c["total_pct"])}</td>'
            f'<td class="num">{e(c["increase_amount"])}</td><td class="num">{e(c["new_rent"])}</td><td class="num">{c["notice_days"]} days</td>'
            f'<td class="num">{c["serve_by_personal"]}</td><td class="num">{c["serve_by_mail"]}</td>'
            f'<td>{ref_links(c["refs"])}<br>{link(data.URLS["PDF571"], "Form 571 (rates)")}</td></tr>')
    scen = (f'<section><h2>Scenarios (calculated, not Rent Board determinations)</h2>'
            f'<p>Computed by <span class="mono">evidence/tools/build_evidence.py</span> from the official Form 571 rates and the Rule 4.12(a) banking test, using the owner-reported inputs above. Amounts are exact to the cent and never rounded up (INC-04). "Serve by" is the last day for delivery that leaves the full notice period before the effective date; add a day of margin. Today for deadline purposes: {iso(TODAY)}.</p>'
            f'<div class="wrap"><table><caption>Scenario results</caption><thead><tr>{"".join(f"<th scope=col>{h}</th>" for h in heads)}</tr></thead><tbody>{"".join(rows)}</tbody></table></div></section>')

    sched = ['<section><h2>Banking schedule behind each scenario</h2><p>An anniversary increase is bankable once a full 12 months have elapsed from the date it could first be imposed (Rule 4.12(a), INC-07). The rate used is the Form 571 rate in effect on that date.</p>']
    for c in CALCS:
        if c["id"] not in ("CALC-01", "CALC-02", "CALC-04", "CALC-05"):
            continue
        trs = "".join(
            f'<tr data-row-id="{c["id"]}-{i+1}"><td class="num">{iso(it["available"])}</td><td class="num">{iso(it["bankable_from"])}</td><td class="num">{it["percent"]}%</td><td>{link(data.URLS["PDF571"], "Form 571")}</td></tr>'
            for i, it in enumerate(c["_schedule"]))
        if not trs:
            trs = f'<tr data-row-id="{c["id"]}-0"><td colspan="3">No anniversary increase has been available for 12 full months by {c["effective_date"]}: nothing banks.</td><td>{link(data.URLS["PDF571"], "Form 571")}</td></tr>'
        sched.append(f'<details><summary>{c["id"]}: {e(c["unit"])}, effective {c["effective_date"]}</summary><div class="wrap"><table><caption>Anniversary increases that bank for {c["id"]}</caption><thead><tr><th scope="col">Became available</th><th scope="col">Bankable from</th><th scope="col">Rate</th><th scope="col">Official source</th></tr></thead><tbody>{trs}</tbody></table></div></details>')
    sched.append("</section>")

    ex_rows = []
    for x in EXAMPLE_RESULTS:
        ex_rows.append(
            f'<tr data-row-id="{x["id"]}"><th scope="row" class="mono">{x["id"]}</th><td>{e(x["label"])}</td><td class="num">{x["start"]}</td><td class="num">{x["effective"]}</td>'
            f'<td class="num">{money(x["base"])}</td><td class="num">{x["official_banked"]}% + {x["official_annual"]}%</td><td class="num">{money(x["official_new"])}</td>'
            f'<td class="num">{x["model_banked"]}% + {x["model_annual"]}%</td><td class="num">{money(x["model_new"])}</td><td>{"matches" if x["model_ok"] else "DIFFERS"}</td>'
            f'<td class="num">{money(x["loose_new"])}</td><td>{"matches" if x["loose_ok"] else "<strong>differs</strong>"}</td>'
            f'<td>{link(data.URLS[x["source"]], "Rent Board example")}</td></tr>')
    tests = (f'<section id="model-test"><h2>Model test against the Rent Board\'s own worked examples</h2>'
             f'<p>If the banking model is right it must reproduce the Rent Board\'s published examples. The per-increase 12-month test (Rule 4.12(a)) matches all four. A loose reading of the banked page\'s 24-month sentence (bank every skipped anniversary once 24 months have passed) fails on EX-3, where the Rent Board says the 1.4% is lost after 35 months without an increase. That is why the "12 vs 24 months" item is resolved rather than open (audit finding A-03).</p>'
             f'<div class="wrap"><table><caption>Official examples vs model</caption><thead><tr><th scope="col">ID</th><th scope="col">Example</th><th scope="col">Lease start</th><th scope="col">Effective</th><th scope="col">Base rent</th><th scope="col">Official banked + annual</th><th scope="col">Official new rent</th><th scope="col">Model banked + annual</th><th scope="col">Model new rent</th><th scope="col">Model vs official</th><th scope="col">Loose-reading new rent</th><th scope="col">Loose vs official</th><th scope="col">Source</th></tr></thead><tbody>{"".join(ex_rows)}</tbody></table></div></section>')

    rate_rows = "".join(
        f'<tr data-row-id="RATE-{i+1:02d}"><td>{e(r["period"])}{" *" if r["special"] else ""}</td><td class="num">{r["percent"]}%</td><td>{link(data.URLS["PDF571"], "Form 571")}</td></tr>'
        for i, r in enumerate(RATES))
    cc = ""
    if CROSSCHECK:
        items = "".join(f'<li><span class="mono">{e(n)}</span>: {cnt} rows checked; ' + ("all match Form 571." if not bad else f'{len(bad)} problem(s): {e("; ".join(bad))}') + (f' Blank placeholder row(s) left blank, as they should be: {e("; ".join(ph))}.' if ph else "") + "</li>" for n, cnt, bad, ph in CROSSCHECK)
        cc = f'<p><strong>Cross-check with the repository\'s own tables:</strong></p><ul>{items}</ul>'
    else:
        cc = '<p class="muted">The repository\'s data/allowable-increases.csv was not present in this checkout, so no cross-check ran. Re-run the builder after merging main.</p>'
    rates = (f'<section id="rates"><h2>Official allowable annual increases (Form 571, {len(RATES)} rows)</h2>{cc}'
             f'<p><a href="allowable_increases_official.csv">Download allowable_increases_official.csv</a>. Rows marked * are the Rent Board\'s 1992-93 pair, of which only one may be imposed.</p>'
             f'<details><summary>Show all {len(RATES)} rows</summary><div class="wrap"><table><caption>Allowable annual increases</caption><thead><tr><th scope="col">Effective period</th><th scope="col">Increase</th><th scope="col">Official source</th></tr></thead><tbody>{rate_rows}</tbody></table></div></details></section>')
    return page("Calculations", "Scenario arithmetic, banking schedule and model test", inputs + scen + "".join(sched) + tests + rates, "calculations.html")


def build_index():
    steps = [
        ("Confirm the units are covered.", "Many units built on or before 1979-06-13 are rent controlled; a single-family home with a legal in-law unit counts as a two-unit building and is not exempt. The building facts here are owner-reported, so coverage is assumed, not confirmed.", "OCC-01, OCC-02, OWN-04"),
        ("Report each tenant-occupied unit into the Rent Board Housing Inventory.", "Owners of every kind must report (free, online, yearly by March 1). The report is public and made under penalty of perjury. There is no separate license application: the license is generated from the report.", "LIC-02, LIC-03, LIC-08, LIC-13, LIC-14, LIC-16"),
        ("Check that a current license shows for each unit and keep a dated screenshot.", "Status is searchable by address or APN in the portal. Whether these two units have one is not confirmed.", "LIC-15, LIC-18"),
        ("Compute the increase from base rent only.", "Annual 1.6% for 3/1/2026 to 2/28/2027 needs no petition. Banked amounts count only after a full 12 months from the date each became available; no compounding, no rounding up.", "INC-01, INC-02, INC-04, INC-07, INC-10"),
        ("Write the notice.", "State the dollar amount, the percentage, the effective date, and itemize annual vs banked. A nonconforming notice is null and void. Use the rate in effect on the effective date.", "NTC-04, NTC-05, NTC-06, NTC-09, INC-12"),
        ("Serve it on time.", "At least 30 days before the effective date, or 90 if the increase (with any others in the prior 12 months) exceeds 10%; add 5 days if mailed. Personal delivery or CCP 1013 mail.", "NTC-01, NTC-02, NTC-03"),
        ("Screen for retaliation and discrimination before serving.", "No increase within 180 days of a tenant's good-faith habitability complaint; no differences tied to a protected characteristic; no increase solely because an occupant was added.", "LAW-01, LAW-02, LAW-04, LAW-07, LAW-08, NTC-07, NTC-08"),
        ("On the effective date the license must be current.", "It does not have to be attached to the notice. An increase that takes effect without one may be null and void and the tenant may be entitled to a refund. The Rent Board fee ($59 per unit; 50% recoverable) and City business registration are separate.", "LIC-05, LIC-06, LIC-10, FEE-01, FEE-03, REG-01"),
        ("Before serving, re-check the pending cap and the emergency question.", "File 261020 is pending; an emergency price-gouging rule may or may not apply. Both are flagged below.", "PND-01, PND-02, PND-03, LAW-11, LAW-12"),
    ]
    step_html = "".join(f'<li data-row-id="STEP-{i+1}"><strong>{e(t)}</strong> {e(d)} <span class="muted">Evidence: {ref_links(refs)}</span></li>' for i, (t, d, refs) in enumerate(steps))
    c = {x["id"]: x for x in CALCS}
    cards = f"""<div class="cards">
<div class="box"><span class="muted">License for an individual owner</span><strong>Required; automatic from the Housing Inventory report</strong>Must be current on the effective date. No individual-owner exemption appears in the official text. <a href="register.html#LIC-03">LIC-03</a></div>
<div class="box"><span class="muted">Unit 1 (lease start 2025-02-01, $3,995.00)</span><strong>1.6% now, or 3.0% from 2027-02-01</strong>{e(c["CALC-01"]["new_rent"])} early (annual only); {e(c["CALC-02"]["new_rent"])} on 2027-02-01. <a href="calculations.html#CALC-02">CALC-02</a></div>
<div class="box"><span class="muted">Unit 2 (lease start 2019-06-01, $3,150.00)</span><strong>13.1% under current text, if no increase since 2019-06-01</strong>{e(c["CALC-04"]["new_rent"])}; 90 days' notice (mail by {c["CALC-04"]["serve_by_mail"]}, personal by {c["CALC-04"]["serve_by_personal"]} for 2027-02-15). <a href="calculations.html#CALC-04">CALC-04</a></div>
<div class="box"><span class="muted">Pending File 261020 (not law)</span><strong>Would cap the banked part at 10%, if enacted as introduced</strong>For Unit 2 that is {e(money(Decimal("315.00")))} of the {e(money(Decimal("362.25")))} banked; $47.25 would wait until 2030. <a href="register.html#PND-02">PND-02</a></div>
</div>"""

    # corrections table
    arows = []
    for a in sorted(AUDIT, key=lambda x: (SEV_ORDER[x["severity"]], x["id"])):
        refs = a["register_refs"]
        official = ref_links(refs) if re.search(r"\b[A-Z]{3,4}-\d\d\b", refs) else ""
        if a["id"] == "A-04":
            official += (" " if official else "") + link("https://kanlerxz87-cyber.github.io/RentincreaseSF5/internal/notes.md", "live-site retrieval, 2026-11-07", "evidence-link")
        if not official:
            official = link("https://kanlerxz87-cyber.github.io/RentincreaseSF5/", "published site (repository finding)", "evidence-link")
        arows.append(
            f'<tr id="{e(a["id"])}" data-row-id="{e(a["id"])}"><th scope="row" class="mono">{e(a["id"])}</th><td><span class="badge sev-{e(a["severity"])}">{e(a["severity"])}</span></td>'
            f'<td><strong>{e(a["title"])}</strong><br><span class="muted">{e(a["where_published"])}</span></td>'
            f'<td><blockquote class="x">{e(a["published_statement"])}</blockquote></td><td>{e(a["official_finding"])}</td>'
            f'<td>{e(a["requested_action"])}<br><span class="muted">Owner of the file: {e(a["file_owner"])}</span></td><td>{e(a["status"])}</td><td>{official}</td></tr>')
    corr = (f'<section id="corrections"><h2>Corrections requested to the published pages</h2>'
            f'<p>These are requests logged in COORDINATION.md, not edits: each page belongs to another session. <a href="audit-findings.csv">audit-findings.csv</a> has the same table.</p>'
            f'<div class="wrap"><table><caption>Audit findings (published claim vs official evidence)</caption><thead><tr><th scope="col">ID</th><th scope="col">Severity</th><th scope="col">Finding</th><th scope="col">Published claim</th><th scope="col">Official evidence</th><th scope="col">Requested fix</th><th scope="col">Status</th><th scope="col">Official links</th></tr></thead><tbody>{"".join(arows)}</tbody></table></div></section>')

    # flagged
    frows = []
    for r in REGISTER:
        if r["status"] not in ("unverified", "owner-reported"):
            continue
        why = r["notes"]
        val = f'owner supplied: {r["owner_reported_value"]}' if r["owner_reported_value"] else "blank on purpose"
        frows.append(
            f'<tr id="flag-{e(r["id"])}" data-row-id="F-{e(r["id"])}"><th scope="row" class="mono"><a href="register.html#{e(r["id"])}">{e(r["id"])}</a></th><td>{e(r["finding"])}</td>'
            f'<td>{badge(r["status"])}</td><td>{e(val)}</td><td>{e(why)}</td><td>{link(r["source_url"], r["source_title"])}</td></tr>')
    flagged = (f'<section id="flagged"><h2>Flagged for review ({len(frows)} items, non-blocking)</h2>'
               f'<p>Nothing here is asserted. Each link is the official place that was checked or where the answer should be found.</p>'
               f'<div class="wrap"><table><caption>Unverified and owner-reported items</caption><thead><tr><th scope="col">ID</th><th scope="col">Item</th><th scope="col">Status</th><th scope="col">Value</th><th scope="col">Why it is open</th><th scope="col">Official place checked</th></tr></thead><tbody>{"".join(frows)}</tbody></table></div></section>')

    analysis = ('<section id="analysis"><h2>Analysis (labelled as analysis, not as verified fact)</h2><div class="box">'
                '<p><strong>One unit or both.</strong> Different amounts for the two units follow from different lease dates and banking histories: neutral, documented criteria. '
                'What the official texts prohibit is differing treatment because of a protected characteristic (<a href="register.html#LAW-01">LAW-01</a>, <a href="register.html#LAW-02">LAW-02</a>, <a href="register.html#LAW-04">LAW-04</a>) '
                'and retaliation (<a href="register.html#LAW-07">LAW-07</a>, <a href="register.html#LAW-08">LAW-08</a>). No official source reviewed requires equal increases. The record worth keeping is one written method, applied the same way to each unit.</p>'
                '<p><strong>Where a challenge would most likely land.</strong> A tenant advocate would check, in order: coverage; a license on the effective date; the arithmetic and the annual/banked itemization; the notice period and service; retaliation timing; and the pending cap. '
                'Those are the items the register above lets you evidence.</p></div></section>')

    method = ('<section id="method"><h2>Method, sources and limits</h2><div class="box">'
              f'<p>Official pages were fetched on {VERIFIED_AT} (UTC) from: ' + ", ".join(sorted(HOSTS)) + '. Anything else (news, law-firm summaries, aggregators, commercial rent sites) is never cited as verification. '
              'See <a href="README.md">README.md</a> for the status rules and how to rebuild. Not covered: the owner\'s Housing Inventory and license status, actual rent history, building coverage facts, HUD fair-market rent, corporate-landlord practice, and the emergency declaration (all flagged above).</p></div></section>')

    body = (f'<section><h2>Bottom line</h2>{cards}</section>'
            f'<section id="process"><h2>The Rent Board process, step by step (official text)</h2><ol class="steps">{step_html}</ol></section>'
            + corr + flagged + analysis + method)
    return page("Independent evidence register", "Official-source verification and audit of the published rent-increase pages", body, "index.html")


(OUT / "register.html").write_text(build_register(), encoding="utf-8")
(OUT / "calculations.html").write_text(build_calcs(), encoding="utf-8")
(OUT / "index.html").write_text(build_index(), encoding="utf-8")

# ----------------------------------------------------------------------------- final page checks
for name in ("index.html", "register.html", "calculations.html"):
    t = (OUT / name).read_text(encoding="utf-8")
    if "<h1>" not in t:
        fail(f"{name}: missing h1")
    # every tbody row must have data-row-id and at least one https link
    for body in t.split("<tbody>")[1:]:
        for tr in body.split("</tbody>")[0].split("</tr>"):
            if "<tr" in tr:
                if "data-row-id=" not in tr:
                    fail(f"{name}: row without data-row-id: {tr[:80]}")
                if 'href="https://' not in tr:
                    fail(f"{name}: row without an https link: {tr[:120]}")
    for m in re.finditer(r'href="(https://[^"]+)"', t):
        host = urlsplit(html.unescape(m.group(1))).hostname
        if host not in HOSTS and host != "kanlerxz87-cyber.github.io":
            fail(f"{name}: link host not on allowlist: {host}")

if ERRORS:
    print(f"\n{len(ERRORS)} check(s) failed")
    sys.exit(1)
print(f"OK: {len(REGISTER)} register rows, {len(AUDIT)} audit findings, {len(CALCS)} scenarios, {len(RATES)} rates; "
      f"model matches {sum(x['model_ok'] for x in EXAMPLE_RESULTS)}/{len(EXAMPLE_RESULTS)} official examples; "
      f"loose 24-month reading matches {sum(x['loose_ok'] for x in EXAMPLE_RESULTS)}/{len(EXAMPLE_RESULTS)}; "
      f"cross-checks: {[(n, c, len(b)) for n, c, b, _ in CROSSCHECK] or 'none (repo CSVs absent)'}")
