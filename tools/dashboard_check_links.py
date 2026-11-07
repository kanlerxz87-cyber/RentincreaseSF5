#!/usr/bin/env python3
"""Link and citation integrity check for the published site.

Checks performed
----------------
1. INTERNAL LINKS   every relative href in docs/*.html resolves to a real file.
2. ANCHORS          every #fragment used internally exists as an id in the target.
3. REGISTRY         every external URL used on the site is present in
                    data/sources.json (or in the small allowlist of non-source
                    utility links below).
4. FETCH STATUS     every external URL has a recorded fetch result in
                    data/link_status.json. The sandbox has no general outbound
                    network access, so these statuses were recorded by actually
                    retrieving each page during the research phase.
5. ORPHANS          every source in the registry appears on at least one page.

Exit code 0 = clean, 1 = problems found.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
DATA = os.path.join(ROOT, "docs", "data")

HREF_RE = re.compile(r'href="([^"]+)"')

# Non-source utility links: official tools/portals referenced for action, not citation.
ALLOWLIST = {
    "https://portal.sfrb.org/": "Rent Board Portal (official)",
    "https://sfplanninggis.org/PIM/": "SF Property Information Map (official)",
    "https://www.sf.gov/documents/7737/537_6.14_Costa-Hawkins_Petition_3.25.pdf": "Rent Board Form 537 (official form, fetched and confirmed)",
    "https://github.com/kanlerxz87-cyber/RentincreaseSF5/blob/main/tools/calc.py": "this repository's own source code",
}


def main():
    sources = json.load(open(os.path.join(DATA, "sources.json")))["sources"]
    status = json.load(open(os.path.join(DATA, "link_status.json")))
    fetches = status["urls"]
    GOOD = {"ok", "official_reference", "self"}
    src_urls = {s["url"] for s in sources.values()}

    problems = []
    used_internal = 0
    used_external = set()
    pages = sorted(f for f in os.listdir(DOCS) if f.endswith(".html"))

    for page in pages:
        html_text = open(os.path.join(DOCS, page), encoding="utf-8").read()
        ids = set(re.findall(r'id="([^"]+)"', html_text))
        for href in HREF_RE.findall(html_text):
            if href.startswith(("mailto:", "tel:")):
                continue
            if href.startswith("#"):
                if href[1:] and href[1:] not in ids:
                    problems.append("{}: dangling anchor {}".format(page, href))
                continue
            if href.startswith(("http://", "https://")):
                used_external.add(href)
                if href not in src_urls and href not in ALLOWLIST:
                    problems.append("{}: external URL not in registry: {}".format(page, href))
                elif href in src_urls and fetches.get(href, {}).get("result") not in GOOD:
                    problems.append("{}: URL has no successful fetch record: {}".format(page, href))
                continue
            # internal
            target = href.split("#")[0]
            frag = href.split("#")[1] if "#" in href else None
            if not target:
                continue
            path = os.path.join(DOCS, target)
            used_internal += 1
            if not os.path.exists(path):
                problems.append("{}: broken internal link -> {}".format(page, href))
                continue
            if frag:
                tgt_ids = set(re.findall(r'id="([^"]+)"',
                                         open(path, encoding="utf-8").read()))
                if frag not in tgt_ids:
                    problems.append("{}: broken internal anchor -> {}".format(page, href))

    # every external URL should have a fetch record
    for url in sorted(used_external):
        if url not in fetches:
            problems.append("no fetch record for {}".format(url))

    # orphans: registry entries never used on any page
    all_html = "".join(open(os.path.join(DOCS, p), encoding="utf-8").read() for p in pages)
    for key, s in sources.items():
        if s["url"] not in all_html:
            problems.append("registry source {} is never linked on any page".format(key))

    print("pages checked        : {}".format(len(pages)))
    print("internal links       : {}".format(used_internal))
    print("external citations   : {}".format(len(used_external)))
    print("registry sources     : {}".format(len(sources)))
    print("sources verified live: {}".format(
        sum(1 for s in sources.values() if fetches.get(s["url"], {}).get("result") in GOOD)))
    print("-" * 60)
    problems = sorted(set(problems))
    if problems:
        for p in problems:
            print("FAIL  " + p)
        print("\n{} problem(s)".format(len(problems)))
        return 1
    print("OK - no broken links, no unregistered citations, no orphan sources")
    return 0


if __name__ == "__main__":
    sys.exit(main())
