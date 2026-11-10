#!/usr/bin/env python3
"""Check external links published by the static site.

The sandbox has restricted outbound access, so this check is designed to run on
a GitHub Actions runner. It collects HTTPS links from tracked HTML, Markdown,
CSV and JSON artifacts, requests each unique URL with curl, and classifies the
status. A 403/405/429 from a government host is treated as bot blocking for
manual review, not as a broken link; persistent 404/410/5xx responses fail.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
SCAN_SUFFIXES = {".html", ".md", ".csv", ".json"}
URL_RE = re.compile(r"https://[^\s\"'<>\\`]+")
ATTR_URL_RE = re.compile(r"(?:href|src|poster)\s*=\s*[\"']([^\"']+)[\"']", re.I)
TRAILING = ".,;:)]}>'\"`"
USER_AGENT = "RentincreaseSF5-official-link-check/1.0 (+GitHub Actions)"
BROKEN = {400, 404, 410, 500, 501, 502, 503, 504}
BLOCKED = {401, 403, 405, 406, 429}


def clean(url: str) -> str:
    # HTML attribute URLs are read from the raw source so that an unescaped
    # "&sectionNum" is not misdecoded as the &sect; entity. Only &amp; is
    # normalized; other query ampersands stay literal.
    url = url.replace("&amp;", "&")
    while url and url[-1] in TRAILING:
        url = url[:-1]
    return url


def published_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, text=True,
        stdout=subprocess.PIPE, check=True,
    )
    files = []
    for line in result.stdout.splitlines():
        p = ROOT / line
        if ".git" in p.parts or p.suffix.lower() not in SCAN_SUFFIXES:
            continue
        files.append(p)
    return files


def collect_urls() -> dict[str, list[str]]:
    found: dict[str, set[str]] = {}
    for path in published_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        urls: set[str] = set()
        if path.suffix.lower() == ".html":
            for value in ATTR_URL_RE.findall(text):
                if value.startswith("https://"):
                    urls.add(clean(value))
        # Also catches source links in Markdown, CSV and JSON. HTML duplicates
        # are harmless because the URL set is deduplicated below.
        urls |= {clean(m.group(0)) for m in URL_RE.finditer(text)}
        for url in urls:
            if not url.startswith("https://"):
                continue
            parsed = urlsplit(url)
            if not parsed.hostname:
                continue
            found.setdefault(url, []).append(str(path.relative_to(ROOT)))
    return {url: sorted(set(paths)) for url, paths in found.items()}


def probe(url: str) -> tuple[str, str]:
    command = [
        "curl", "-L", "-sS", "-o", os.devnull,
        "-w", "%{http_code}", "--max-time", "20",
        "--connect-timeout", "10", "--max-filesize", "2000000",
        "-A", USER_AGENT, url,
    ]
    last = "000"
    for attempt in range(2):
        proc = subprocess.run(command, text=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        candidate = (proc.stdout or "").strip().splitlines()[-1:] or ["000"]
        last = candidate[0] if re.fullmatch(r"\d{3}", candidate[0]) else "000"
        if last not in {"000", "429", "500", "502", "503", "504"}:
            return last, (proc.stderr or "").strip()[:240]
        if attempt == 0:
            time.sleep(2)
    return last, "retried once"


def classify(status: str) -> str:
    if not status.isdigit():
        return "unknown"
    code = int(status)
    if 200 <= code < 400:
        return "ok"
    if code in BLOCKED:
        return "bot-blocked-review"
    if code in BROKEN:
        return "broken"
    return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default="external-link-status.csv")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    urls = collect_urls()
    rows: list[dict[str, str]] = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(probe, url): url for url in urls}
        for future in as_completed(futures):
            url = futures[future]
            status, note = future.result()
            rows.append({
                "url": url,
                "status": status,
                "classification": classify(status),
                "source_files": "; ".join(urls[url][:3]),
                "note": note,
            })
    rows.sort(key=lambda r: (r["classification"], r["url"]))

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=[
            "url", "status", "classification", "source_files", "note"])
        writer.writeheader()
        writer.writerows(rows)

    counts: dict[str, int] = {}
    for row in rows:
        counts[row["classification"]] = counts.get(row["classification"], 0) + 1
    print("External links checked: %d" % len(rows))
    for key in sorted(counts):
        print("  %-18s %d" % (key, counts[key]))
    for row in rows:
        if row["classification"] == "broken":
            print("BROKEN %s -> %s" % (row["status"], row["url"]))
    print("CSV: %s" % output.relative_to(ROOT))
    broken = counts.get("broken", 0)
    unknown = counts.get("unknown", 0)
    if broken:
        print("FAIL: %d broken external links" % broken)
        return 1
    if unknown:
        print("REVIEW: %d links returned an unclassified status" % unknown)
    print("PASS: no confirmed broken external links")
    return 0


if __name__ == "__main__":
    sys.exit(main())
