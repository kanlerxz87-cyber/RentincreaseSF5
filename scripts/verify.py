#!/usr/bin/env python3
"""Dependency-free release checks for a static, source-cited rental research site.

This is a structural/arithmetic checker, not a legal opinion. See
 docs/VERIFICATION-CONTRACT.md and record proposition-level reading separately.
Sensitive audit terms are read at runtime and never included in output.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import csv
import datetime as dt
import html.parser
import io
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation, ROUND_CEILING
from pathlib import Path
from typing import Iterable

ALIASES = {
    "id": ("id", "row_id"),
    "category": ("category",),
    "finding": ("finding", "claim", "requirement", "issue", "question"),
    "value": ("value", "verified_value", "increase_pct", "rate_pct", "total_pct", "verdict"),
    "status": ("status", "verification_status"),
    "source_url": ("source_url", "official_source_url", "official_source", "sources", "url"),
    "verified_at": ("verified_at", "retrieved_at", "source_checked_at"),
    "notes": ("notes", "verification_notes", "detail", "used_for", "verifies"),
    "owner_reported_value": ("owner_reported_value", "owner_input"),
    "flag_id": ("flag_id", "review_id"),
}
STATUSES = {"verified", "unverified", "owner-reported", "calculated", "analysis", "conflict", "pending", "banked", "owner record; calculated"}
OFFICIAL_EXACT = {
    "sfrb.org", "www.sfrb.org", "portal.sfrb.org",
    "sftreasurer.org", "www.sftreasurer.org", "sfassessor.org", "www.sfassessor.org", "data.sfgov.org",
    "sfwater.org", "www.sfwater.org", "sfbos.org", "www.sfbos.org",
    "codelibrary.amlegal.com", "docs.github.com", "github.com", "api.github.com",
}
# Primary organizational sources may support statements about their own services,
# never replace a statute or agency rule. The manual review must check that scope.
INSTITUTIONAL_EXACT = {
    "sftu.org", "www.sftu.org", "sfbar.org", "www.sfbar.org",
    "evictiondefense.org", "www.evictiondefense.org",
}
TEXT_SUFFIXES = {".html", ".htm", ".css", ".js", ".json", ".csv", ".md", ".txt", ".xml", ".svg", ".yml", ".yaml"}
EXCLUDED_DIRS = {".git", ".arena", "node_modules", ".venv", "__pycache__", "build", "dist", "out"}


@dataclass
class Issue:
    level: str
    code: str
    path: str
    message: str


def official_source(url: str) -> bool:
    try:
        p = urllib.parse.urlsplit(url)
        host = (p.hostname or "").lower().rstrip(".")
        if p.scheme != "https" or p.username or p.password or p.port not in (None, 443):
            return False
        if host == "codelibrary.amlegal.com":
            return p.path.startswith("/codes/san_francisco/")
        return (host in OFFICIAL_EXACT or host in INSTITUTIONAL_EXACT
                or host.endswith(".gov") or host.endswith(".ca.gov")
                or host.endswith(".sfrb.org") or host.endswith(".sf.gov"))
    except ValueError:
        return False


def source_urls(value: str) -> list[str]:
    return [u.rstrip(".,;") for u in re.split(r"[\s|]+", value.strip()) if u]


def norm_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def normalize_row(raw: dict) -> dict:
    lookup = {norm_key(str(k)): v for k, v in raw.items() if k is not None}
    return {key: str(next((lookup[norm_key(a)] for a in names if norm_key(a) in lookup), "") or "").strip()
            for key, names in ALIASES.items()}


class LegacyAdapter:
    """Read the published multi-set schema without rewriting its owned files.

    JSON facts/questions cite source-register IDs. Resolve those IDs to the
    official URLs in data/sources.json. CSV reference tables have their own
    value columns. This adapter does not invent verification dates or evidence.
    """
    def __init__(self, root: Path):
        self.root = root
        self.registry: dict[str, str] = {}
        self.registry_source: dict[str, dict] = {}
        path = root / "data" / "sources.json"
        if path.is_file():
            obj = json.loads(path.read_text(encoding="utf-8"))
            for row in obj.get("sources", []):
                self.registry[row["id"]] = row["url"]
                self.registry_source[row["id"]] = row
        self.retrieved = ""
        if path.is_file():
            self.retrieved = str(json.loads(path.read_text(encoding="utf-8")).get("retrieved", ""))

    def normalize(self, raw: dict, path: str) -> dict:
        row = normalize_row(raw)
        if not row["id"]:
            # Stable content-addressed ID for legacy reference rows without IDs.
            import hashlib
            payload = json.dumps(raw, sort_keys=True, ensure_ascii=False)
            row["id"] = Path(path).stem + "-" + hashlib.sha256(payload.encode()).hexdigest()[:12]
        if not row["source_url"]:
            refs = raw.get("source", raw.get("sources", ""))
            if isinstance(refs, str):
                refs = re.findall(r"S\d+", refs)
            if isinstance(refs, list):
                row["source_url"] = " ".join(self.registry.get(str(r), "") for r in refs).strip()
        if not row["value"]:
            for key in ("requirement", "issue", "question", "title", "used_for", "source"):
                if raw.get(key):
                    row["value"] = str(raw[key])
                    break
        if not row["notes"]:
            for key in ("used_for", "verifies", "detail", "recommended_action"):
                if raw.get(key):
                    row["notes"] = str(raw[key])
                    break
        if not row["notes"] and path.endswith("data/facts.json"):
            ref = str(raw.get("source", ""))
            reg = self.registry_source.get(ref)
            if reg:
                row["notes"] = str(reg.get("verifies", ""))
        if not row["notes"] and path.endswith("data/allowable-increases.csv"):
            row["notes"] = f"Official Form 571 rate-table row: {raw.get('effective_period', '')}; {raw.get('increase_pct', '')}%."
        if not row["value"] and raw.get("source"):
            row["value"] = str(raw.get("used_for") or raw.get("title") or raw.get("requirement") or raw.get("source"))
        if not row["verified_at"] and row["status"] == "verified":
            row["verified_at"] = self.retrieved
        if row["status"] in {"owner record; calculated", "banked"}:
            row["status"] = "calculated"
            if not row["notes"]:
                row["notes"] = "Legacy calculated row; formula/provenance must be checked against the rendered scenario and owner-reported inputs."
        if row["status"].startswith("unverified"):
            row["status"] = "unverified"
            if path.endswith("data/flagged.csv"):
                row["value"] = ""
                row["flag_id"] = row["id"]
        if row["status"] in {"not imposed; banked if 12 months elapse", "annual increase in effect on that date"}:
            row["status"] = "calculated"
            row["notes"] = row["notes"] or str(raw.get("status", ""))
        if row["status"] == "verified-dataset":
            row["status"] = "verified"
            market = self.root / "data" / "market.json"
            if market.is_file():
                row["verified_at"] = str(json.loads(market.read_text(encoding="utf-8")).get("extracted", ""))[:10]
            row["notes"] = row["notes"] or str(raw.get("requirement", ""))
        if row["status"] in {"conflict", "pending", "none"}:
            row["status"] = "unverified"
            row["value"] = ""
            row["flag_id"] = row["id"]
        if row["status"] == "analysis":
            row["status"] = "calculated"
            row["notes"] = row["notes"] or str(raw.get("requirement", ""))
        return row

class PageParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, int]] = []
        self.ids: set[str] = set()
        self.duplicate_ids: list[str] = []
        self.rows: list[dict] = []
        self.text: list[str] = []
        self.lang = ""
        self.title = ""
        self.viewport = False
        self.description = False
        self.h1 = 0
        self.nav = False
        self.main = False
        self.table_count = 0
        self.tables_without_headers = 0
        self._table_depth = 0
        self._table_has_header = False
        self._row: dict | None = None
        self._title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: v or "" for k, v in attrs}
        line = self.getpos()[0]
        if "id" in a:
            if a["id"] in self.ids:
                self.duplicate_ids.append(a["id"])
            self.ids.add(a["id"])
        if tag == "a" and "name" in a:
            self.ids.add(a["name"])
        if tag == "html":
            self.lang = a.get("lang", "")
        if tag == "title":
            self._title = True
        if tag == "meta":
            self.viewport |= a.get("name", "").lower() == "viewport" and "width=device-width" in a.get("content", "")
            self.description |= a.get("name", "").lower() == "description" and bool(a.get("content"))
        self.h1 += tag == "h1"
        self.nav |= tag == "nav"
        self.main |= tag == "main"
        if tag in {"a", "link"} and "href" in a:
            self.links.append((a["href"], line))
        if tag in {"script", "img", "iframe", "source", "embed"} and "src" in a:
            self.links.append((a["src"], line))
        if "srcset" in a:
            for candidate in a["srcset"].split(","):
                if candidate.strip():
                    self.links.append((candidate.strip().split()[0], line))
        if tag == "object" and a.get("data"):
            self.links.append((a["data"], line))
        for style in ([a["style"]] if "style" in a else []):
            self.links.extend((u, line) for u in re.findall(r"url\(\s*['\"]?([^)'\"]+)", style))
        if tag == "table":
            self._table_depth += 1
            if self._table_depth == 1:
                self.table_count += 1
                self._table_has_header = False
        if tag == "th" and self._table_depth:
            self._table_has_header = True
        if tag == "tr" and self._table_depth:
            self._row = {"line": line, "id": a.get("data-row-id", ""), "status": a.get("data-status", ""),
                         "text": [], "sources": [], "links": [], "cells": 0, "header": False}
        if tag == "td" and self._row is not None:
            self._row["cells"] += 1
        if tag == "a" and self._row is not None and "href" in a:
            self._row["links"].append(a["href"])
            if official_source(a["href"]):
                self._row["sources"].append(a["href"])
            elif re.search(r"sources\.html#S\d+$", a["href"]):
                self._row["sources"].append(a["href"])

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._title = False
        if tag == "tr" and self._row is not None:
            self._row["header"] = self._row["cells"] == 0
            self.rows.append(self._row)
            self._row = None
        if tag == "table" and self._table_depth:
            self._table_depth -= 1
            if self._table_depth == 0 and not self._table_has_header:
                self.tables_without_headers += 1

    def handle_data(self, data: str) -> None:
        self.text.append(data)
        if self._title:
            self.title += data
        if self._row is not None:
            self._row["text"].append(data)


class Audit:
    def __init__(self, root: Path, base_path: str = "/RentincreaseSF5", external: bool = False,
                 strict: bool = False, require_sensitive: bool = False, timeout: float = 15,
                 sensitive: Iterable[str] = (), workers: int = 8) -> None:
        self.root = root.resolve()
        self.base_path = "/" + base_path.strip("/") if base_path.strip("/") else ""
        self.external, self.strict, self.require_sensitive = external, strict, require_sensitive
        self.timeout, self.workers = timeout, workers
        self.sensitive = [s for s in sensitive if s.strip()]
        self.issues: list[Issue] = []
        self.counts: Counter = Counter()
        self.pages: dict[Path, PageParser] = {}
        self.records: dict[str, tuple[str, dict]] = {}
        self.external_results: dict[str, dict] = {}
        self.site_root = self.root if (self.root / "index.html").is_file() else self.root / "docs"
        self.legacy = LegacyAdapter(self.root)

    def issue(self, level: str, code: str, path: str, message: str) -> None:
        self.issues.append(Issue(level, code, path, message))

    def files(self) -> list[Path]:
        return sorted(p for p in self.root.rglob("*") if p.is_file()
                      and not any(part in EXCLUDED_DIRS for part in p.relative_to(self.root).parts))

    def rel(self, path: Path) -> str:
        return path.relative_to(self.root).as_posix()

    def local_target(self, source: Path, url: str) -> tuple[Path | None, str]:
        p = urllib.parse.urlsplit(url)
        path = urllib.parse.unquote(p.path)
        if not path:
            return source, p.fragment
        if path.startswith("/"):
            if self.base_path:
                if path != self.base_path and not path.startswith(self.base_path + "/"):
                    raise ValueError(f"Absolute link is outside project base {self.base_path}: {url}")
                path = path[len(self.base_path):]
            target = self.site_root / path.lstrip("/")
        else:
            target = source.parent / path
        target = target.resolve()
        try:
            target.relative_to(self.site_root.resolve())
        except ValueError as exc:
            raise ValueError(f"Local link escapes published tree: {url}") from exc
        if target.is_dir():
            target = target / "index.html"
        return target, p.fragment

    def check_pages(self) -> None:
        if not (self.site_root / "index.html").is_file():
            self.issue("ERROR", "SITE_MISSING", "index.html", "No static entry point; integration is not ready.")
            return
        html_files = sorted(p for p in self.site_root.rglob("*.html")
                            if not any(part in EXCLUDED_DIRS for part in p.relative_to(self.root).parts))
        # Include HTM files as pages too.
        html_files += sorted(p for p in self.site_root.rglob("*.htm") if p not in html_files
                             and not any(part in EXCLUDED_DIRS for part in p.relative_to(self.root).parts))
        external_urls: set[str] = set()
        rendered_ids: Counter = Counter()
        for path in html_files:
            rel = self.rel(path)
            parser = PageParser()
            try:
                parser.feed(path.read_text(encoding="utf-8"))
                parser.close()
            except (UnicodeError, OSError) as exc:
                self.issue("ERROR", "HTML_READ", rel, str(exc))
                continue
            self.pages[path] = parser
            self.counts["html_pages"] += 1
            for attr, present, code in [("lang", parser.lang, "HTML_LANG"), ("title", parser.title.strip(), "HTML_TITLE"),
                                        ("viewport", parser.viewport, "HTML_VIEWPORT"), ("description", parser.description, "HTML_DESCRIPTION"),
                                        ("navigation", parser.nav, "HTML_NAV"), ("main landmark", parser.main, "HTML_MAIN")]:
                if not present:
                    self.issue("WARN", code, rel, f"Missing {attr}.")
            if parser.h1 != 1:
                self.issue("WARN", "HTML_H1", rel, f"Expected one h1, found {parser.h1}.")
            for ident in parser.duplicate_ids:
                self.issue("ERROR", "DUPLICATE_ID", rel, f"Duplicate fragment ID: {ident}.")
            if not parser.tables_without_headers:
                pass
            else:
                self.issue("WARN", "TABLE_HEADERS", rel, "A table has no th header cells.")
            for url, line in parser.links:
                scheme = urllib.parse.urlsplit(url).scheme.lower()
                if url.startswith("//"):
                    external_urls.add("https:" + urllib.parse.urldefrag(url)[0])
                    continue
                if url.strip() in {"#", "javascript:void(0)", "javascript:;"}:
                    self.issue("ERROR", "EMPTY_LINK", f"{rel}:{line}", "Link has no destination.")
                    continue
                if scheme in {"http", "https"}:
                    external_urls.add(urllib.parse.urldefrag(url)[0])
                    continue
                if scheme in {"mailto", "tel", "data", "javascript"}:
                    continue
                try:
                    target, fragment = self.local_target(path, url)
                    if target is None or not target.is_file():
                        self.issue("ERROR", "LOCAL_LINK", f"{rel}:{line}", f"Missing local target: {url}")
                    elif fragment:
                        target_parser = self.pages.get(target)
                        if target.suffix.lower() in {".html", ".htm"}:
                            if target_parser is None:
                                tp = PageParser()
                                tp.feed(target.read_text(encoding="utf-8"))
                                target_parser = tp
                            if urllib.parse.unquote(fragment) not in target_parser.ids:
                                self.issue("ERROR", "LOCAL_FRAGMENT", f"{rel}:{line}", f"Missing fragment: {url}")
                except (ValueError, OSError) as exc:
                    self.issue("ERROR", "LOCAL_LINK", f"{rel}:{line}", str(exc))
            for row in parser.rows:
                if row["header"]:
                    continue
                self.counts["html_data_rows"] += 1
                loc = f"{rel}:{row['line']}"
                if row["id"]:
                    rendered_ids[row["id"]] += 1
                if not row["sources"]:
                    self.issue("ERROR", "ROW_SOURCE", loc, "Every data row needs its own official-source hyperlink.")
                text = " ".join(row["text"]).lower()
                status = row["status"].lower() or ("unverified" if "unverified" in text else "owner-reported" if "owner-reported" in text else "")
                has_flag_ref = bool(re.search(r"\b(?:FL-\d+|F\d+)\b", text)) and any("flagged" in u.lower() for u, _ in parser.links)
                if status in {"unverified", "owner-reported"} and not any("flagged" in u.lower() or "review" in u.lower() for u in row["links"]) and not has_flag_ref:
                    self.issue("ERROR", "ROW_REVIEW_LINK", loc, "Unverified/owner-reported row must link to Flagged for Review.")
        for stylesheet in sorted(self.site_root.rglob("*.css")):
            if any(part in EXCLUDED_DIRS for part in stylesheet.relative_to(self.root).parts):
                continue
            try:
                css = stylesheet.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                self.issue("ERROR", "CSS_READ", self.rel(stylesheet), str(exc))
                continue
            urls = re.findall(r"url\(\s*['\"]?([^)'\"]+)", css)
            urls += re.findall(r"@import\s+['\"]([^'\"]+)['\"]", css)
            for url in set(urls):
                if url.startswith("data:"):
                    continue
                if url.startswith("//"):
                    external_urls.add("https:" + urllib.parse.urldefrag(url)[0])
                    continue
                if urllib.parse.urlsplit(url).scheme in {"http", "https"}:
                    external_urls.add(urllib.parse.urldefrag(url)[0])
                    continue
                if urllib.parse.urlsplit(url).scheme:
                    continue
                try:
                    target, _ = self.local_target(stylesheet, url)
                    if target is None or not target.is_file():
                        self.issue("ERROR", "CSS_LINK", self.rel(stylesheet), f"Missing CSS asset: {url}")
                except ValueError as exc:
                    self.issue("ERROR", "CSS_LINK", self.rel(stylesheet), str(exc))
        for ident, count in rendered_ids.items():
            if count > 1:
                self.issue("ERROR", "DUPLICATE_RENDERED_ROW", "site", f"Data row {ident} rendered {count} times; expected exactly once.")
        if self.records:
            missing = set(self.records) - set(rendered_ids)
            unknown = set(rendered_ids) - set(self.records)
            if rendered_ids:
                for ident in sorted(missing):
                    self.issue("ERROR", "DATA_NOT_RENDERED", "data", f"Record {ident} has no matching HTML data-row-id.")
                for ident in sorted(unknown):
                    self.issue("ERROR", "HTML_NOT_IN_DATA", "site", f"HTML data-row-id {ident} has no data record.")
            else:
                self.issue("WARN", "ROW_ID_MAPPING", "site", "Legacy HTML has no data-row-id attributes; automated record-to-row identity comparison unavailable. Manual row review required.")
        flagged = [p for p in self.pages if "flag" in p.stem.lower() or "review" in p.stem.lower()]
        if not flagged:
            self.issue("ERROR", "FLAG_PAGE", "site", "No clearly named Flagged for Review page found.")
        self.check_markdown_tables()
        for _, row in self.records.values():
            for url in source_urls(row["source_url"]):
                if urllib.parse.urlsplit(url).scheme in {"http", "https"}:
                    external_urls.add(urllib.parse.urldefrag(url)[0])
        self.counts["external_unique_urls"] = len(external_urls)
        if self.external:
            self.check_external(sorted(external_urls))
        else:
            self.issue("WARN", "EXTERNAL_UNCHECKED", "site", f"{len(external_urls)} unique external URLs not requested; this is not a release pass.")

    def check_markdown_tables(self) -> None:
        research = self.root / "research"
        if not research.is_dir():
            return
        for path in sorted(research.rglob("*.md")):
            lines = path.read_text(encoding="utf-8").splitlines()
            separator = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")
            for index in range(1, len(lines)):
                if not separator.match(lines[index]) or "|" not in lines[index - 1]:
                    continue
                j = index + 1
                while j < len(lines) and "|" in lines[j] and lines[j].strip():
                    row = lines[j]
                    self.counts["markdown_data_rows"] += 1
                    urls = re.findall(r"https?://[^\s)<>]+", row)
                    if not any(official_source(u.rstrip(".,;")) for u in urls):
                        self.issue("ERROR", "ROW_SOURCE", f"{self.rel(path)}:{j + 1}", "Research table row lacks an official-source link.")
                    if re.search(r"unverified|owner-reported", row, re.I) and not re.search(r"\[[^]]*(?:flag|review)[^]]*\]\([^)]*(?:flag|review)[^)]*\)", row, re.I):
                        self.issue("ERROR", "ROW_REVIEW_LINK", f"{self.rel(path)}:{j + 1}", "Unverified/owner-reported research row needs a Flagged for Review link.")
                    j += 1

    def check_data(self) -> None:
        data_dir = self.root / "data"
        files = sorted(data_dir.rglob("*.csv")) if data_dir.is_dir() else []
        json_files = sorted(data_dir.rglob("*.json")) if data_dir.is_dir() else []
        if not files and not json_files:
            self.issue("ERROR", "DATA_MISSING", "data", "No CSV/JSON research records available to audit.")
        for path in files:
            try:
                with path.open(encoding="utf-8-sig", newline="") as handle:
                    reader = csv.DictReader(handle)
                    if not reader.fieldnames:
                        self.issue("ERROR", "DATA_HEADER", self.rel(path), "CSV has no header.")
                        continue
                    for raw in reader:
                        self.check_record(raw, f"{self.rel(path)}:{reader.line_num}")
            except (OSError, UnicodeError, csv.Error) as exc:
                self.issue("ERROR", "DATA_READ", self.rel(path), str(exc))
        for path in json_files:
            try:
                obj = json.loads(path.read_text(encoding="utf-8"))
                rows = obj.get("rows") if isinstance(obj, dict) else obj
                if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
                    continue  # A configuration/metadata JSON, not a record collection.
                for index, raw in enumerate(rows, 1):
                    self.check_record(raw, f"{self.rel(path)}:row-{index}")
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                self.issue("ERROR", "DATA_READ", self.rel(path), str(exc))

    def check_record(self, raw: dict, loc: str) -> None:
        if None in raw:
            self.issue("ERROR", "CSV_COLUMNS", loc, "Row has more fields than its header.")
        row = self.legacy.normalize(raw, loc.split(":")[0])
        self.counts["data_rows"] += 1
        ident = row["id"]
        if not ident:
            self.issue("ERROR", "ROW_ID", loc, "Missing stable row ID.")
        elif ident in self.records:
            self.issue("ERROR", "DUPLICATE_ROW_ID", loc, f"ID {ident} already defined in {self.records[ident][0]}.")
        else:
            self.records[ident] = (loc, row)
        status = row["status"].lower().replace("_", "-").replace("owner reported", "owner-reported")
        if status not in STATUSES:
            self.issue("ERROR", "ROW_STATUS", loc, f"Unknown/missing status {row['status']!r}; use the documented vocabulary.")
        urls = source_urls(row["source_url"])
        if not urls:
            self.issue("ERROR", "ROW_SOURCE", loc, "Missing row-level official source URL.")
        for url in urls:
            if not official_source(url):
                self.issue("ERROR", "SOURCE_OFFICIAL", loc, f"Source is not an accepted official HTTPS URL: {url}")
        if status in {"unverified", "owner-reported"}:
            if row["value"]:
                self.issue("ERROR", "UNVERIFIED_VALUE", loc, "Authoritative value must be blank; owner input belongs in owner_reported_value.")
            if not row["notes"] or not (row["flag_id"] or re.search(r"flag|review|unverified|not.*verified", row["notes"], re.I)):
                self.issue("ERROR", "UNVERIFIED_FLAG", loc, "Explain missing evidence and reference a review flag.")
            if status == "owner-reported" and not row["owner_reported_value"]:
                self.issue("ERROR", "OWNER_PROVENANCE", loc, "Owner-reported status requires a separately labeled owner_reported_value.")
        if status == "verified":
            if not row["value"]:
                self.issue("ERROR", "VERIFIED_EMPTY", loc, "Verified record has no value.")
            if not row["notes"]:
                self.issue("ERROR", "VERIFIED_EVIDENCE", loc, "Record the exact supporting rule/passage in notes.")
            try:
                checked = dt.date.fromisoformat(row["verified_at"])
                if checked > dt.datetime.now(dt.timezone.utc).date():
                    raise ValueError("Retrieval date is in the future.")
            except ValueError as exc:
                self.issue("ERROR", "VERIFIED_DATE", loc, f"Actual ISO retrieval date required: {exc}")
        if status == "calculated" and not row["notes"]:
            self.issue("ERROR", "CALCULATION_BASIS", loc, "Disclose formula and input provenance for calculated values.")
        lookup = {norm_key(str(k)): v for k, v in raw.items() if k is not None}
        keys = [norm_key(k) for k in ("base_rent", "rate_percent", "increase_amount", "new_rent")]
        if all(k in lookup and str(lookup[k]).strip() for k in keys):
            try:
                values = [Decimal(re.sub(r"[$,%\s,]", "", str(lookup[k]))) for k in keys]
                base, rate, increase, new_rent = values
                exact = base * rate / Decimal(100)
                if increase != exact or new_rent != base + increase:
                    self.issue("ERROR", "ARITHMETIC", loc, f"Expected increase {exact}, new rent {base + exact}; no inferred rounding.")
                if increase != exact.quantize(Decimal("0.01"), rounding=ROUND_CEILING):
                    self.issue("WARN", "ARITHMETIC_PRECISION", loc, "Increase is not expressed to cents; review legal rounding before service.")
            except InvalidOperation:
                self.issue("ERROR", "ARITHMETIC_INPUT", loc, "Calculation columns must contain numeric amounts/rates.")

    def check_external(self, urls: list[str]) -> None:
        def fetch(url: str) -> tuple[str, dict]:
            request = urllib.request.Request(url, headers={"User-Agent": "RentincreaseSF5-source-verifier/1.0", "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.8"})
            for attempt in range(2):
                try:
                    with urllib.request.urlopen(request, timeout=self.timeout) as response:
                        sample = response.read(262144).decode("utf-8", errors="replace")
                        title_match = re.search(r"<title[^>]*>(.*?)</title>", sample, re.I | re.S)
                        title = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else ""
                        soft = bool(re.search(r"^(not found|page not found|404)\b", title, re.I))
                        return url, {"status": response.status, "final_url": response.url, "soft_404": soft, "title": title[:160]}
                except urllib.error.HTTPError as exc:
                    if exc.code in {403, 429} or 500 <= exc.code < 600:
                        if attempt == 0:
                            continue
                        return url, {"status": exc.code, "blocked": exc.code in {403, 429}, "error": str(exc)}
                    return url, {"status": exc.code, "error": str(exc)}
                except (urllib.error.URLError, TimeoutError, OSError) as exc:
                    if attempt == 0:
                        continue
                    return url, {"status": None, "blocked": True, "error": str(exc)}
            return url, {"status": None, "blocked": True}
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as pool:
            self.external_results = dict(pool.map(fetch, urls))
        for url, result in self.external_results.items():
            self.counts["external_requested"] += 1
            if result.get("soft_404"):
                self.issue("ERROR", "EXTERNAL_SOFT_404", url, "Source returned a Not Found document.")
            elif result.get("blocked"):
                self.issue("WARN", "EXTERNAL_BLOCKED", url, f"Could not verify source response: {result.get('error', result.get('status'))}.")
            elif not result.get("status") or result["status"] >= 400:
                self.issue("ERROR", "EXTERNAL_HTTP", url, f"Source returned {result.get('status')}: {result.get('error', '')}.")

    def sensitive_pattern(self, term: str) -> re.Pattern:
        tokens = re.findall(r"[a-z0-9]+", term.lower())
        if len(tokens) > 1 and all(len(t) == 1 for t in tokens):
            pattern = r"[\s.\-]+".join(re.escape(t) for t in tokens)
        else:
            pattern = r"\s+".join(re.escape(t) for t in tokens)
        return re.compile(r"(?<![a-z0-9])" + pattern + r"(?![a-z0-9])", re.I)

    def check_privacy(self) -> None:
        self.counts["sensitive_terms_supplied"] = len(self.sensitive)
        if not self.sensitive:
            self.issue("ERROR" if self.require_sensitive else "WARN", "SENSITIVE_AUDIT_NOT_RUN", "privacy", "No private audit terms supplied; exact-term privacy audit not performed.")
        patterns = [self.sensitive_pattern(s) for s in self.sensitive]
        for path in self.files():
            if path.suffix.lower() not in TEXT_SUFFIXES or path.stat().st_size > 5_000_000:
                continue
            rel = self.rel(path)
            if rel.startswith("scripts/tests/"):
                continue  # Synthetic fixtures are not publication or actual personal data.
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeError, OSError):
                continue
            self.counts["privacy_files_scanned"] += 1
            if path.suffix.lower() == ".html" and path.is_relative_to(self.site_root):
                for match in re.finditer(r"\b(?:[A-Z][A-Z0-9]*_(?:DOLLAR|BASE|PERIOD|NAME|ADDRESS|EMAIL|PHONE))\b", text):
                    line = text.count("\n", 0, match.start()) + 1
                    self.issue("ERROR", "UNRESOLVED_TEMPLATE", f"{rel}:{line}", f"Unresolved publication placeholder {match.group(0)}.")
            for index, pattern in enumerate(patterns, 1):
                match = pattern.search(text)
                if match:
                    line = text.count("\n", 0, match.start()) + 1
                    self.issue("ERROR", "SENSITIVE_TERM", f"{rel}:{line}", f"Private audit term #{index} found; value intentionally redacted.")
            for match in re.finditer(r"\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b", text, re.I):
                if not official_source("https://" + match.group(1)):
                    self.issue("WARN", "EMAIL_REVIEW", rel, "Non-government email address requires privacy review; value not emitted.")

    def run(self) -> dict:
        self.check_data()
        self.check_pages()
        self.check_privacy()
        errors = sum(i.level == "ERROR" for i in self.issues)
        warnings = sum(i.level == "WARN" for i in self.issues)
        passed = errors == 0 and (not self.strict or warnings == 0)
        return {"tool": "rent-increase-static-verifier/1", "passed": passed,
                "scope": "Structural, source-domain, optional HTTP, arithmetic and runtime-term checks; not legal approval.",
                "external_requested": self.external, "strict": self.strict,
                "counts": dict(self.counts), "issues": [asdict(i) for i in self.issues],
                "external_results": self.external_results}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--base-path", default="/RentincreaseSF5")
    parser.add_argument("--external", action="store_true", help="Request every external HTTP(S) link.")
    parser.add_argument("--strict-warnings", action="store_true")
    parser.add_argument("--require-sensitive-audit", action="store_true")
    parser.add_argument("--timeout", type=float, default=15)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--json", type=Path, help="Optional report path; never contains private input terms.")
    args = parser.parse_args(argv)
    if args.workers < 1 or args.workers > 16 or args.timeout <= 0:
        parser.error("workers must be 1..16 and timeout must be positive")
    terms = []
    if not sys.stdin.isatty():
        stdin = sys.stdin.read().strip()
        if stdin:
            try:
                terms = json.loads(stdin)
                if not isinstance(terms, list) or not all(isinstance(s, str) for s in terms):
                    raise ValueError("Expected a JSON array of strings.")
            except (ValueError, json.JSONDecodeError):
                print("Invalid private audit input; expected a JSON array of strings. Input not echoed.", file=sys.stderr)
                return 2
    audit = Audit(args.root, args.base_path, args.external, args.strict_warnings, args.require_sensitive_audit,
                  args.timeout, terms, args.workers)
    report = audit.run()
    if args.json:
        args.json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for issue in report["issues"]:
        print(f"{issue['level']} {issue['code']} {issue['path']}: {issue['message']}")
    print(json.dumps({k: report[k] for k in ("passed", "counts")}, indent=2))
    if not report["passed"]:
        print("NOT A RELEASE PASS. Resolve errors/warnings as applicable; manual legal review is separate.")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
