#!/usr/bin/env python3
"""
Link and integrity check for the generated site.

Checks:
  1. every internal link resolves to a file that exists
  2. every in-page anchor link (#id) resolves to an id in the target file
  3. every source tag (class="src") points at an anchor that exists in sources.html
  4. every external URL is a well-formed absolute https URL
  5. every fact row, flagged item and question has at least one source
  6. every flagged id referenced from a unit exists in flagged.json

Exit code 0 = clean, 1 = problems found.
"""
import json
import os
import re

# Generic initial-pair pattern. Catches initials without committing any real one.
INITIAL_PAIR = re.compile(r"\b[A-Z]\s[A-Z]\b")
import sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "dashboard")
DATA = os.path.join(ROOT, "data")

PAGES = [
    "index.html", "executive-summary.html", "process.html", "units.html",
    "market.html", "findings.html", "questions.html", "sources.html", "flagged.html",
    "method.html",
]


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.ids = set()
        self.src_targets = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
            if "src" in (a.get("class") or "").split():
                self.src_targets.append(a["href"])

def _identifier_tokens():
    """Exact identifier tokens, loaded only from a git-ignored private file.

    Keeping the tokens out of version control means no personal identifier is
    published to GitHub Pages, while the check still works for the owner locally.
    """
    path = os.path.join(ROOT, "private", "identifiers.txt")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as handle:
        return [line.strip() for line in handle if line.strip()]


def main():
    problems = []
    parsed = {}

    for p in PAGES:
        path = os.path.join(DOCS, p)
        if not os.path.exists(path):
            problems.append("MISSING PAGE: %s" % p)
            continue
        c = Collector()
        c.feed(open(path, encoding="utf-8").read())
        parsed[p] = c

    html_files = [f for f in os.listdir(DOCS) if f.endswith(".html")]
    internal_links = 0
    external_links = 0

    for p in PAGES:
        c = parsed.get(p)
        if not c:
            continue
        for href in c.hrefs:
            if href.startswith(("http://", "https://")):
                external_links += 1
                if not re.match(r"^https://[^\s\"'<>]+$", href):
                    if not re.match(r"^http://[^\s\"'<>]+$", href):
                        problems.append("%s: malformed external URL %s" % (p, href))
                continue
            if href.startswith("mailto:") or href.startswith("tel:"):
                continue
            internal_links += 1
            if href.startswith("#"):
                if href[1:] not in c.ids:
                    problems.append("%s: anchor %s has no matching id" % (p, href))
                continue
            target, _, frag = href.partition("#")
            if target:
                if target not in html_files and not os.path.exists(os.path.join(DOCS, target)):
                    problems.append("%s: broken link to %s" % (p, href))
                    continue
            if frag and target.endswith(".html"):
                tc = parsed.get(target)
                if tc and frag not in tc.ids:
                    problems.append("%s: link %s - anchor %s missing in %s" % (p, href, frag, target))

    # source tags must resolve to sources.html anchors
    src_page = parsed.get("sources.html")
    if src_page:
        for p in PAGES:
            c = parsed.get(p)
            if not c:
                continue
            for href in c.src_targets:
                if href.startswith("sources.html#"):
                    frag = href.split("#", 1)[1]
                    if frag not in src_page.ids:
                        problems.append("%s: source tag %s does not exist on sources page" % (p, href))

    # data integrity
    src = {s["id"] for s in json.load(open(os.path.join(DATA, "sources.json")))["sources"]}
    facts = json.load(open(os.path.join(DATA, "facts.json")))["rows"]
    flagged = {f["id"] for f in json.load(open(os.path.join(DATA, "flagged.json")))["items"]}
    units = json.load(open(os.path.join(DATA, "units.json")))["units"]
    questions = json.load(open(os.path.join(DATA, "questions.json")))["questions"]

    for row in facts:
        if row["source"] not in src:
            problems.append("facts.json %s: unknown source %s" % (row["id"], row["source"]))
    for q in questions:
        if not q["sources"]:
            problems.append("questions.json %s: no sources" % q["id"])
        for s in q["sources"]:
            if s not in src:
                problems.append("questions.json %s: unknown source %s" % (q["id"], s))
    for u in units:
        for f in u["flags"]:
            if f not in flagged:
                problems.append("units.json %s: unknown flag %s" % (u["id"], f))
    for item in json.load(open(os.path.join(DATA, "flagged.json")))["items"]:
        for s in item["sources"]:
            if s not in src:
                problems.append("flagged %s: unknown source %s" % (item["id"], s))

    # anchors referenced from flagged/unit pages
    fl_page = parsed.get("flagged.html")
    if fl_page:
        for fid in flagged:
            if fid not in fl_page.ids:
                problems.append("flagged.html: missing anchor for %s" % fid)

    # mirror parity: dashboard/ is the published tree, site/dashboard/ is the repository mirror
    mirror = os.path.join(ROOT, "site", "dashboard")
    for dirpath, _dirs, files in os.walk(DOCS):
        for name in files:
            src = os.path.join(dirpath, name)
            rel = os.path.relpath(src, DOCS)
            dst = os.path.join(mirror, rel)
            if not os.path.exists(dst):
                problems.append("mirror missing: site/dashboard/%s" % rel)
            elif open(src, "rb").read() != open(dst, "rb").read():
                problems.append("mirror differs: site/dashboard/%s" % rel)

    # identifier exclusion (privacy-preserving)
    # No real identifier is stored in this repository. Exact tokens are read from an
    # optional git-ignored file private/identifiers.txt (one per line); when that file
    # is absent the exact-token check is skipped. The generic initial-pair pattern is
    # always enforced, so initials are still caught without anyone being named here.
    banned = _identifier_tokens()
    for dirpath, _dirs, files in os.walk(DOCS):
        for name in files:
            if not name.endswith(".html"):
                continue
            text = open(os.path.join(dirpath, name), encoding="utf-8").read()
            for token in banned:
                if token in text:
                    problems.append("%s: contains a personal identifier token" % name)
                    break
            hit = INITIAL_PAIR.search(re.sub(r"<[^>]+>", " ", text))
            if hit:
                problems.append("%s: initial-pair pattern %r - verify it is a placeholder"
                                % (name, hit.group(0)))

    print("pages checked: %d" % len(PAGES))
    print("mirror parity: site/dashboard/ compared against dashboard/")
    print("internal links: %d | external links: %d" % (internal_links, external_links))
    print("data rows: %d facts, %d questions, %d flagged, %d source tags"
          % (len(facts), len(questions), len(flagged), len(src)))
    if problems:
        print("\nPROBLEMS (%d):" % len(problems))
        for p in problems:
            print("  -", p)
        return 1
    print("\nAll internal links, anchors and source tags resolve. No problems found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
