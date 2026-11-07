#!/usr/bin/env python3
"""Line-by-line verification of the generated site.

Checks:
  1. Every data-table row has at least one link to an official source.
  2. Every UNVERIFIED row has an EMPTY (blank) value cell.
  3. All internal links and asset paths resolve (no broken links).
  4. No owner-supplied tenant identifiers appear in published files.
  5. Every source ID used in the datasets exists in the registry and points at
     an official domain.
  6. Every page has a title, navigation and the privacy footer.

Writes VERIFICATION.md. Exits non-zero on any failure.
Run: python3 scripts/verify.py
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
HTML_FILES = [ROOT / "index.html"] + sorted((ROOT / "pages").glob("*.html"))
TEXT_FILES = [ROOT / "README.md", ROOT / "COORDINATION.md"] + sorted((ROOT / "research").glob("*.md"))

OFFICIAL_DOMAINS = {
    "sf.gov", "www.sf.gov", "media.api.sf.gov", "www.sf.gov", "sfbos.archive.sf.gov",
    "sfgov.legistar.com", "portal.sfrb.org", "sfrb.org", "sfplanninggis.org",
    "leginfo.legislature.ca.gov", "hud.gov", "www.hud.gov", "archives.hud.gov",
    "govinfo.gov", "www.govinfo.gov", "justice.gov", "www.justice.gov",
    "github.com", "docs.github.com", "www.sfassessor.org", "bls.gov", "www.bls.gov",
}

# Owner-supplied personal identifiers (initials) that must never be published.
PII_PATTERNS = [r"\bL\s+O\b", r"\bV\s+N\b", r"\bJP\b", r"\bM\s+T\b", r"\bE\s+R\b", r"\bI\s+S\b"]

TR_RE = re.compile(r"<tr\b[^>]*>(.*?)</tr>", re.S | re.I)
HREF_RE = re.compile(r'href="([^"]+)"', re.I)
TABLE_RE = re.compile(r"<table\b[^>]*>(.*?)</table>", re.S | re.I)

errors: list[str] = []
stats = {"pages": 0, "rows": 0, "rows_with_official_link": 0, "blank_unverified": 0, "internal_links": 0, "source_ids": 0}


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def is_official(url: str) -> bool:
    try:
        host = (urlparse(url).hostname or "").lower()
    except ValueError:
        return False
    return host in OFFICIAL_DOMAINS or host.endswith(".sf.gov") or host.endswith(".hud.gov") or host.endswith(".gov")


def check_sources():
    sources = load("sources.json")
    for sid, s in sources.items():
        stats["source_ids"] += 1
        if not is_official(s["url"]):
            errors.append(f"source {sid} URL is not an official domain: {s['url']}")
        if not s.get("title") or not s.get("agency"):
            errors.append(f"source {sid} is missing title/agency")
    datasets = ["process.json", "requirements.json", "legal.json", "units.json", "practice.json",
                "discrimination.json", "flags.json", "verification.json", "rates.json"]
    for name in datasets:
        rows = load(name)
        for r in rows:
            for sid in r.get("sources", []):
                if sid not in sources:
                    errors.append(f"{name} row {r.get('id')} references unknown source {sid}")
            if r.get("status") == "unverified" and r.get("value", "") != "" and name != "flags.json":
                errors.append(f"{name} row {r.get('id')} is UNVERIFIED but has a non-empty value")
            if name == "rates.json" and r.get("status") == "unverified" and r.get("rate", "") != "":
                errors.append(f"rates.json row {r.get('id')} is UNVERIFIED but has a non-empty rate")


def check_rows(path: Path, doc: str):
    for table_html in TABLE_RE.findall(doc):
        for row in TR_RE.findall(table_html):
            if "<th" in row.lower():
                continue
            stats["rows"] += 1
            links = HREF_RE.findall(row)
            official = [u for u in links if is_official(u)]
            if official:
                stats["rows_with_official_link"] += 1
            else:
                errors.append(f"{path.relative_to(ROOT)}: table row without an official source link: {row[:140]}")
            if "b-unverified" in row:
                stats["blank_unverified"] += 1
                if 'class="value blank"' not in row:
                    errors.append(f"{path.relative_to(ROOT)}: UNVERIFIED row without a blank value cell: {row[:140]}")


def check_links(path: Path, doc: str):
    for attr in re.findall(r'(?:href|src)="([^"]+)"', doc, re.I):
        u = attr.strip()
        if not u or u.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
            continue
        stats["internal_links"] += 1
        clean = u.split("#")[0].split("?")[0]
        target = (path.parent / clean).resolve()
        if not target.exists():
            errors.append(f"{path.relative_to(ROOT)}: broken internal link {u}")


def check_page(path: Path):
    doc = path.read_text(encoding="utf-8")
    stats["pages"] += 1
    if "<title>" not in doc or "Site navigation" not in doc or "All tenant identifiers are placeholders" not in doc:
        errors.append(f"{path.relative_to(ROOT)}: missing title, navigation, or privacy footer")
    check_rows(path, doc)
    check_links(path, doc)


def check_pii():
    published = HTML_FILES + [p for p in TEXT_FILES if p.exists()] + sorted((DATA).glob("*.json"))
    for p in published:
        text = p.read_text(encoding="utf-8")
        for pat in PII_PATTERNS:
            if re.search(pat, text):
                errors.append(f"possible personal identifier {pat!r} found in {p.relative_to(ROOT)}")


def main():
    check_sources()
    for p in HTML_FILES:
        if not p.exists():
            errors.append(f"missing page {p.relative_to(ROOT)}")
            continue
        check_page(p)
    check_pii()

    lines = [
        "# VERIFICATION.md",
        "",
        "Generated by `scripts/verify.py` on 2026-11-07 (UTC). Re-run after any data or site change.",
        "",
        "## Automated results",
        "",
        "| Check | Result |",
        "|---|---|",
        f"| Pages checked | {stats['pages']} |",
        f"| Data table rows checked | {stats['rows']} |",
        f"| Rows with at least one official-source link | {stats['rows_with_official_link']} |",
        f"| UNVERIFIED rows with an intentionally blank value cell | {stats['blank_unverified']} |",
        f"| Internal links / asset paths checked | {stats['internal_links']} |",
        f"| Source registry entries checked | {stats['source_ids']} |",
        f"| Personal-identifier scan | {'PASS' if not any('personal identifier' in e for e in errors) else 'FAIL'} |",
        f"| Overall | {'PASS — no errors' if not errors else 'FAIL — ' + str(len(errors)) + ' error(s)'} |",
        "",
        "## Method",
        "",
        "1. Each factual value was read from an official government page (sf.gov, media.api.sf.gov, portal.sfrb.org, leginfo.legislature.ca.gov, hud.gov, govinfo.gov, sfplanninggis.org) or from the repository's own GitHub record. No commercial guides, press reports or forums were used as verification.",
        "2. Every data-table row on the site carries a link to at least one official source. The verifier parses each generated `<tr>` and checks the href against the official-domain allowlist.",
        "3. Where an official value could not be confirmed, the value cell is empty and the row is marked UNVERIFIED and listed on the Flagged for Review page. The verifier rejects any UNVERIFIED row with a non-empty value.",
        "4. Computed figures are pure arithmetic on owner-provided rents and official published rates; they are labelled 'Computed', not 'Verified'. Analysis rows are labelled 'Analysis'.",
        "5. All internal page links, stylesheet paths and script paths are resolved against the filesystem; any missing target fails the build.",
        "6. Published files are scanned for the owner-supplied tenant identifiers. Only Occupant A–F placeholders are used; no personal information is stored in this public repository. Dates and amounts are unchanged.",
        "7. Conflicting official sources are not silently resolved. Both readings are published with their links and both appear on the Flagged for Review page.",
        "",
        "## Known conflicts (not resolved by this project)",
        "",
        "- Rule 4.12(a) (full 12 months) vs sf.gov 'Banked rent increases' (at least 24 full months).",
        "- Sec. 37.15(c) / Rule 13.14 (7/1/2022, 3/1/2023) vs official Form 538 (7/1/2020, 3/1/2021) for the license start dates.",
        "- Sec. 37.15(e) (tenant not obligated during suspension) vs Rule 13.14 (entire increase null and void).",
        "- The Rent Board states its online Ordinance text is not the official record of the City's laws.",
        "",
        "See `research/01-executive-summary.md` and the site's Flagged for Review page for the full list.",
        "",
    ]
    if errors:
        lines += ["## Errors", ""] + [f"- {e}" for e in errors] + [""]
    (ROOT / "VERIFICATION.md").write_text("\n".join(lines), encoding="utf-8")

    if errors:
        print("VERIFICATION FAILED")
        for e in errors[:40]:
            print(" -", e)
        print(f"({len(errors)} errors total)")
        sys.exit(1)
    print("VERIFICATION PASSED")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
