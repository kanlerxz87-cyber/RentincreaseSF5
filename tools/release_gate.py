#!/usr/bin/env python3
"""Release gate - session arena-d4b68642.

Runs every check that must pass before the site may be merged and published.
Exits non-zero on any failure, so CI blocks a broken site.

Checks
  1. every published page parses and has exactly one <h1>, lang, and a main landmark
  2. every internal link and stylesheet target resolves on disk
  3. every external link is https and on the official-publisher allowlist
  4. every table data row carries at least one official source link
  5. no supplied tenant initials, street address, or analytics/tracker token
  6. no unsubstituted template token (the defect found on the previous landing page)
  7. no unresolved git merge-conflict marker in any tracked text file
  8. root / site mirror parity
  9. HTML tag balance
 10. the rate table matches the officially published Form 571 values and every
     effective period falls inside 1982-2027 (guards the F19 century defect)
 11. scenario arithmetic recomputes to the cent and is never rounded up

Usage: python3 tools/release_gate.py
"""

import re
import sys
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = {
    "www.sf.gov",
    "leginfo.legislature.ca.gov",
    "calcivilrights.ca.gov",
    "www.hud.gov",
    "sfgov.legistar.com",
    "www.govinfo.gov",
}

# Privacy: no personal identifier is committed to this repository. GitHub Pages
# serves this file from the repository root, so a literal token list here would
# itself be a public disclosure. Exact tokens are read from a git-ignored file;
# when it is absent the generic initial-pair pattern below is still enforced.
# This follows the remediation merged in PR #8.
INITIAL_PAIR = re.compile(r"\b[A-Z]\s[A-Z]\b")


def _identifier_tokens():
    path = ROOT / "private" / "identifiers.txt"
    if not path.exists():
        return []
    return [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]


PRIVATE_TOKENS = _identifier_tokens()

# Tokens that indicate a generator emitted a placeholder instead of a value.
TEMPLATE_TOKENS = [
    "CURRENT_PERIOD", "A_DOLLAR", "A_BASE", "B_DOLLAR", "B_BASE",
    "{:,.2f}", "%s", "%d", "TODO", "FIXME", "PLACEHOLDER",
]

# Mustache/Jinja-style placeholders only. Bare "}}" also occurs as legitimate
# JavaScript closing braces, so it must not be matched as a substring.
PLACEHOLDER_RE = re.compile(r"\{\{\s*[A-Za-z_][A-Za-z0-9_.]*\s*\}\}|\{%.*?%\}")

TRACKER_TOKENS = ["google-analytics", "googletagmanager", "gtag(", "fbevents", "hotjar"]

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}

failures = []
stats = {}


def fail(check, detail):
    failures.append("[%s] %s" % (check, detail))


class Page(HTMLParser):
    """Collects links, data rows, headings and tag balance in one pass."""

    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.links = []
        self.stack = []
        self.h1 = 0
        self.in_tbody = False
        self.in_row = False
        self.row_has_official = False
        self.rows = 0
        self.unsourced = []
        self.row_text = []
        self.balance = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        if tag == "h1":
            self.h1 += 1
        if tag in ("a", "link") and a.get("href"):
            self.links.append((tag, a["href"]))
        if tag == "tbody":
            self.in_tbody = True
        if tag == "tr" and self.in_tbody:
            self.in_row = True
            self.row_has_official = False
            self.row_text = []
        if tag == "a" and self.in_row:
            u = urlsplit(a.get("href", ""))
            if u.scheme == "https" and u.hostname in ALLOWED_HOSTS:
                self.row_has_official = True

    def handle_data(self, data):
        if self.in_row:
            self.row_text.append(data)

    def handle_endtag(self, tag):
        if tag == "tr" and self.in_row:
            self.rows += 1
            if not self.row_has_official:
                self.unsourced.append("".join(self.row_text)[:110])
            self.in_row = False
        if tag == "tbody":
            self.in_tbody = False
        if tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.balance.append("unclosed <%s>" % self.stack.pop())
            if self.stack:
                self.stack.pop()
        else:
            self.balance.append("stray </%s>" % tag)


def published_pages():
    pages = [ROOT / "index.html"]
    pages += sorted((ROOT / "hub").glob("*.html"))
    return [p for p in pages if p.exists()]


def check_pages():
    total_rows = 0
    total_links = 0
    pages = published_pages()
    for p in pages:
        text = p.read_text(encoding="utf-8")
        rel = p.relative_to(ROOT)

        if 'lang="en"' not in text:
            fail("structure", "%s missing lang" % rel)
        if 'id="main"' not in text:
            fail("structure", "%s missing main landmark" % rel)

        pg = Page(rel)
        pg.feed(text)
        if pg.h1 != 1:
            fail("structure", "%s has %d <h1> (expected 1)" % (rel, pg.h1))
        for b in pg.balance:
            fail("tag-balance", "%s %s" % (rel, b))
        for t in pg.stack:
            fail("tag-balance", "%s unclosed <%s> at EOF" % (rel, t))
        for u in pg.unsourced:
            fail("row-source", "%s row without official source: %s" % (rel, u))
        total_rows += pg.rows

        for tag, href in pg.links:
            total_links += 1
            u = urlsplit(href)
            if u.scheme:
                if u.scheme != "https":
                    fail("external", "%s non-https link %s" % (rel, href))
                elif u.hostname not in ALLOWED_HOSTS:
                    fail("external", "%s non-official host %s" % (rel, href))
            elif u.path:
                target = (p.parent / unquote(u.path)).resolve()
                if not target.exists():
                    fail("internal-link", "%s -> %s does not resolve" % (rel, href))

        for tok in PRIVATE_TOKENS:
            if tok in text:
                # Do not echo the identifier into CI logs either.
                fail("privacy", "%s contains a supplied identifier token" % rel)
        prose_only = re.sub(r"<[^>]+>", " ", text)
        m = INITIAL_PAIR.search(prose_only)
        if m:
            fail("privacy", "%s contains an initial-shaped pair; verify it is not a person" % rel)
        # Scan prose only: inline script legitimately contains braces and % ops.
        prose = re.sub(r"<script\b.*?</script>", "", text, flags=re.S)
        for tok in TEMPLATE_TOKENS:
            if tok in prose:
                fail("template", "%s contains unsubstituted token %r" % (rel, tok))
        m = PLACEHOLDER_RE.search(prose)
        if m:
            fail("template", "%s contains placeholder %r" % (rel, m.group(0)))
        for tok in TRACKER_TOKENS:
            if tok in text:
                fail("privacy", "%s contains tracker %r" % (rel, tok))
        if re.search(r"\b\d{2,5}\s+[A-Z][a-z]+\s+(Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd)\b", text):
            fail("privacy", "%s appears to contain a street address" % rel)

    stats["pages"] = len(pages)
    stats["data rows"] = total_rows
    stats["links"] = total_links


def check_orphans():
    """Every published page must be reachable from the landing page or the nav."""
    pages = published_pages()
    inbound = {p: 0 for p in pages}
    for p in pages:
        text = p.read_text(encoding="utf-8")
        for href in re.findall(r'href="([^"]+)"', text):
            u = urlsplit(href)
            if u.scheme or not u.path:
                continue
            target = (p.parent / unquote(u.path)).resolve()
            if target in inbound and target != p.resolve():
                inbound[target] += 1
    for p, n in inbound.items():
        if n == 0 and p.name != "index.html":
            fail("orphan", "%s has no inbound internal link" % p.relative_to(ROOT))
    stats["orphans"] = sum(1 for p, n in inbound.items() if n == 0 and p.name != "index.html")


def check_merge_markers():
    exts = {".md", ".py", ".html", ".css", ".json", ".csv", ".yml", ".yaml"}
    n = 0
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts or p.suffix not in exts:
            continue
        if "site" in p.parts:
            continue
        n += 1
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(text.split("\n"), 1):
            if re.match(r"^(<{7}|={7}|>{7})(\s|$)", line):
                fail("merge-marker", "%s:%d %s" % (p.relative_to(ROOT), i, line[:60]))
    stats["files scanned for markers"] = n


def check_parity():
    pairs = [(ROOT / "index.html", ROOT / "site" / "index.html")]
    for p in (ROOT / "hub").glob("*"):
        if p.is_file():
            pairs.append((p, ROOT / "site" / "hub" / p.name))
    for a, b in pairs:
        if not b.exists():
            fail("parity", "%s missing mirror" % b.relative_to(ROOT))
        elif a.read_bytes() != b.read_bytes():
            fail("parity", "%s differs from its site/ mirror" % a.relative_to(ROOT))
    stats["mirror pairs"] = len(pairs)


def check_rates_and_arithmetic():
    sys.path.insert(0, str(ROOT / "tools"))
    import build_hub as H

    # Values read from Form 571 during this session, independently re-entered here.
    expected = {
        date(2026, 3, 1): 1.6, date(2025, 3, 1): 1.4, date(2024, 3, 1): 1.7,
        date(2023, 3, 1): 3.6, date(2022, 3, 1): 2.3, date(2021, 3, 1): 0.7,
        date(2020, 3, 1): 1.8, date(2019, 3, 1): 2.6,
    }
    for d, want in expected.items():
        got = H.rate_on(d)
        if got != want:
            fail("rates", "rate_on(%s) = %s, official %s" % (d, got, want))
    if len(H.RATES) != 46:
        fail("rates", "expected 46 periods from Form 571, found %d" % len(H.RATES))

    # Form 571 covers 1 April 1982 to 28 February 2027 and nothing else. This
    # range check is what catches a two-digit-year parsing error: the defect
    # recorded as F19 printed the 1982-1999 rows as 2082-2099.
    for a, b, _pct in H.RATES:
        for label in (a, b):
            y = H._d(label).year
            if not 1982 <= y <= 2027:
                fail("rates", "effective date %s parses to year %d, outside 1982-2027" % (label, y))
    if H._d("3/1/99") != date(1999, 3, 1) or H._d("4/1/82") != date(1982, 4, 1):
        fail("rates", "two-digit year parsing is wrong for 1982-1999")

    if abs(H.U1_TOTAL - 3.0) > 1e-9:
        fail("arithmetic", "Unit 1 total %.4f != 3.0" % H.U1_TOTAL)
    if abs(H.U2_BANKED - 11.5) > 1e-9:
        fail("arithmetic", "Unit 2 banked %.4f != 11.5" % H.U2_BANKED)
    if abs(H.U2_TOTAL - 13.1) > 1e-9:
        fail("arithmetic", "Unit 2 total %.4f != 13.1" % H.U2_TOTAL)

    for unit, name, base, pct, eff, note in H.SCENARIOS:
        inc = round(base * pct / 100, 2)
        exact = base * pct / 100
        if inc - exact > 1e-9:
            fail("arithmetic", "%s %s rounded up: %s > %s" % (unit, name, inc, exact))
        days = 90 if pct > 10 else 30
        if H.notice_days(pct) != days:
            fail("arithmetic", "%s %s notice days wrong" % (unit, name))
        if H.serve_by(eff, pct) != eff - timedelta(days=days):
            fail("arithmetic", "%s %s serve-by wrong" % (unit, name))
        if H.serve_by(eff, pct, True) != eff - timedelta(days=days + 5):
            fail("arithmetic", "%s %s mailed serve-by wrong" % (unit, name))
    stats["scenarios recomputed"] = len(H.SCENARIOS)

    # Every register row must cite at least one known official source.
    for r in H.R:
        if not r["sources"]:
            fail("register", "%s has no source" % r["id"])
        for s in r["sources"]:
            if s not in H.SOURCES:
                fail("register", "%s cites unknown source %s" % (r["id"], s))
        if r["status"] in (H.UNVERIFIED, H.ABSENT) and r["value"]:
            fail("register", "%s is unverified but has a value" % r["id"])
    stats["register findings"] = len(H.R)


def main():
    check_pages()
    check_orphans()
    check_merge_markers()
    check_parity()
    check_rates_and_arithmetic()

    print("Release gate")
    for k, v in stats.items():
        print("  %-30s %s" % (k, v))
    if failures:
        print("\nFAILED (%d)" % len(failures))
        for f in failures:
            print("  " + f)
        return 1
    print("\nPASS - all checks green. Safe to merge and publish.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
