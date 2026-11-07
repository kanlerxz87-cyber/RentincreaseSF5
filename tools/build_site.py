#!/usr/bin/env python3
"""Build the static dashboard site at the repository root (GitHub Pages source).

Usage:  python3 tools/build_site.py
Writes: index.html, pages/*.html, assets/style.css, data/*.csv
Checks: internal links resolve; exits non-zero if any are broken.
"""

import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import site_lib as L          # noqa: E402
import pages_1 as P1          # noqa: E402
import pages_2 as P2          # noqa: E402

PAGES = [
    ("executive-summary.html", "Executive summary", P1.executive_summary),
    ("rent-board-process.html", "Rent Board process", P1.rent_board_process),
    ("units.html", "Units &amp; numbers", P1.units),
    ("allowed-increases.html", "Allowed increases", P2.allowed_increases),
    ("laws.html", "Local / State / Federal", P2.laws),
    ("notices.html", "Notices", P2.notices),
    ("owner-practices.html", "Owner playbook", P2.owner_practices),
    ("tenant-review.html", "Tenant-lawyer test", P2.tenant_review),
    ("sources.html", "Sources", P2.sources),
    ("flagged.html", "Flagged for review", P2.flagged),
]


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(text)
    return full


def build_html():
    written = []
    written.append(write("index.html", P1.index()))
    for slug, _title, fn in PAGES:
        written.append(write(os.path.join("pages", slug), fn()))
    written.append(write(os.path.join("assets", "style.css"), L.CSS))
    written.append(write(".nojekyll", ""))
    return written


def build_csv():
    # source register
    rows = [[sid, title, pub, url, used, status] for sid, title, pub, url, used, status in L.SOURCES]
    write_csv("data/sources.csv", ["id", "source", "publisher", "url", "used_for", "verification_status"], rows)

    # allowable increases
    rows = [[p, r, "verified", L.SRC["S2"]["url"]] for p, r in P2.ALLOWANCES]
    rows.append(["3/1/2027 - 2/29/2028", "", "unverified - not yet published", L.SRC["S2"]["url"]])
    write_csv("data/allowable-increases.csv",
              ["effective_period", "increase_pct", "verification_status", "source_url"], rows)

    # units
    rows = [
        ["Unit A", "Tenant A1 (original lessee), Tenant A2 (continuing occupant)", "2025-02-01", "3995.00",
         "2026-02-01", "1.4", "1.6", "3.0", "119.85", "4114.85", "30 days", "owner record; calculated"],
        ["Unit B", "Tenant B1, Tenant B2", "2019-06-01", "3150.00",
         "2020-06-01", "11.5 (six years)", "1.6", "13.1", "412.65", "3562.65", "90 days", "owner record; calculated"],
    ]
    write_csv("data/units.csv",
              ["unit", "occupants_placeholder", "base_rent_effective", "base_rent", "first_allowance_date",
               "banked_pct", "current_annual_pct", "total_pct", "dollar_increase", "new_base_rent",
               "notice_period", "status"], rows)

    # allowance ledger per unit
    rows = []
    for year, rate, period in [(2020, "1.8", "3/1/2020-2/28/2021"), (2021, "0.7", "3/1/2021-2/28/2022"),
                               (2022, "2.3", "3/1/2022-2/28/2023"), (2023, "3.6", "3/1/2023-2/29/2024"),
                               (2024, "1.7", "3/1/2024-2/28/2025"), (2025, "1.4", "3/1/2025-2/28/2026"),
                               (2026, "1.6", "3/1/2026-2/28/2027")]:
        rows.append(["Unit B", "6/1/%d" % year, rate, period, "banked", L.SRC["S2"]["url"]])
    rows.append(["Unit A", "2/1/2026", "1.4", "3/1/2025-2/28/2026", "not imposed; banked if 12 months elapse",
                 L.SRC["S2"]["url"]])
    rows.append(["Unit A", "2/1/2027", "1.6", "3/1/2026-2/28/2027", "annual increase in effect on that date",
                 L.SRC["S2"]["url"]])
    write_csv("data/allowance-ledger.csv",
              ["unit", "date_available", "rate_pct", "rate_period", "status", "source_url"], rows)

    # flagged
    rows = [[f[0], re.sub("<[^>]+>", "", f[1]), re.sub("<[^>]+>", "", f[2]), re.sub("<[^>]+>", "", f[3]),
             re.sub("<[^>]+>", "", f[4]), f[5], " ".join(L.SRC[s]["url"] for s in f[6])]
            for f in sorted(P2.FLAGS, key=lambda x: x[0])]
    write_csv("data/flagged.csv",
              ["id", "issue", "detail", "what_it_affects", "recommended_action", "status", "sources"], rows)


def write_csv(path, header, rows):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def check_links(files):
    href_re = re.compile(r'href="([^"]+)"')
    broken = []
    for f in files:
        if not f.endswith(".html"):
            continue
        base = os.path.dirname(f)
        with open(f, encoding="utf-8") as fh:
            html = fh.read()
        for href in href_re.findall(html):
            if href.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = os.path.normpath(os.path.join(base, href.split("#")[0]))
            if not os.path.exists(os.path.join(ROOT, target)):
                broken.append((os.path.relpath(f, ROOT), href))
    return broken


def check_rows_have_sources():
    """Every <tbody><tr> should contain at least one citation link or an explicit status badge."""
    problems = []
    for f in [os.path.join(ROOT, "index.html")] + [os.path.join(ROOT, "pages", s) for s, _, _ in PAGES]:
        with open(f, encoding="utf-8") as fh:
            html = fh.read()
        for m in re.finditer(r"<tr>(.*?)</tr>", html, re.S):
            row = m.group(1)
            if "<th" in row:
                continue
            if 'class="src"' in row or "badge" in row:
                continue
            problems.append((os.path.relpath(f, ROOT), row[:90]))
    return problems


def main():
    files = build_html()
    build_csv()
    broken = check_links(files)
    print("Wrote %d files." % len(files))
    print("Broken internal links: %d" % len(broken))
    for f, h in broken:
        print("  BROKEN  %s -> %s" % (f, h))
    unlinked = check_rows_have_sources()
    print("Table rows without a source link or status badge: %d" % len(unlinked))
    for f, row in unlinked:
        print("  ROW %s :: %s" % (f, row))
    if broken or unlinked:
        sys.exit(1)


if __name__ == "__main__":
    main()
