#!/usr/bin/env python3
"""Read-only repository/public-artifact audit with deterministic, redacted outputs.

This is an independent release check, not a legal opinion or a live URL monitor.
It scans every tracked text file, all HTML tables (including archived sets), local
links/anchors/assets, source-row coverage, privacy patterns and git merge markers.

Exact identifier checks never embed identifiers in source code. Supply them on
stdin with --identifiers-stdin, or use a git-ignored --identifier-file. Without
either, the report explicitly says the exact check was NOT run; generic initial
patterns still run. Matching values are never printed or written to reports.

Archived citation gaps and historical exposure are review warnings, not silent
passes. Current-file privacy hits, broken local targets and malformed pages fail.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import audit_page

ROOT = Path(__file__).resolve().parent.parent
TEXT_EXTENSIONS = {
    ".md", ".py", ".html", ".css", ".js", ".json", ".csv", ".yml", ".yaml",
    ".txt", ".gitignore", ".nojekyll", ".svg",
}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}
# Government publishers used by the research, plus GitHub's own documentation.
OFFICIAL_SUFFIXES = (".sf.gov", ".ca.gov", ".hud.gov", ".huduser.gov", ".sfgov.org")
OFFICIAL_EXACT = {
    "sf.gov", "ca.gov", "hud.gov", "huduser.gov", "sfgov.org",
    "sfplanning.org", "sfplanninggis.org", "sfassessor.org", "sfrb.org",
    "docs.github.com", "github.com",
}
INITIAL_PAIR = re.compile(r"(?<![A-Za-z])[A-Z]\s[A-Z](?![A-Za-z])|(?<![A-Za-z])[A-Z]\.[A-Z]\.(?![A-Za-z])")
CIVIC_ABBREVIATIONS = {"S.F.", "U.S.", "D.C.", "N.Y.", "N.J.", "N.M.", "N.C.", "S.C."}
MERGE_MARKER = re.compile(r"^(<{7}|={7}|>{7})(?:\s|$)")
MALFORMED_ANCHOR = re.compile(r"<a\s+https?://")
TRACKERS = ("google-analytics", "googletagmanager", "gtag(", "fbevents", "hotjar")
STREET = re.compile(
    r"\b\d{2,6}\s+[A-Z][A-Za-z.'-]*(?:\s+[A-Z][A-Za-z.'-]*){0,3}\s+"
    r"(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Court|Ct)\b"
)


def official(url: str) -> bool:
    try:
        u = urlsplit(url)
        host = (u.hostname or "").lower()
        return u.scheme == "https" and (host in OFFICIAL_EXACT or host.endswith(OFFICIAL_SUFFIXES))
    except ValueError:
        return False


def tracked_files() -> list[Path]:
    out = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return [ROOT / name.decode() for name in out.split(b"\0") if name]


def text_of(path: Path) -> str | None:
    if path.suffix.lower() not in TEXT_EXTENSIONS and path.name not in {".gitignore", ".nojekyll"}:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[tuple[str, str]] = []
        self.assets: list[tuple[str, str]] = []
        self.rows: list[dict] = []
        self.stack: list[tuple[str, str | None]] = []
        self.id_sources: dict[str, set[str]] = defaultdict(set)
        self.row: dict | None = None
        self.thead = 0
        self.h1 = 0
        self.title = False
        self.has_title = False
        self.lang = False
        self.main = False
        self.viewport = False
        self.balance: list[str] = []
        self.remote_active: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: v or "" for k, v in attrs}
        ident = a.get("id") or None
        if ident:
            self.ids.append(ident)
            if self.row is not None:
                self.row["ids"].append(ident)
        if tag not in VOID:
            self.stack.append((tag, ident))
        if tag == "html" and a.get("lang"):
            self.lang = True
        if tag == "main":
            self.main = True
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self.title = True
        if tag == "meta" and a.get("name", "").lower() == "viewport":
            self.viewport = True
        if tag == "thead":
            self.thead += 1
        if tag == "tr" and not self.thead:
            self.row = {"line": self.getpos()[0], "direct": set(), "indirect": [], "cells": 0, "ids": []}
        if tag in {"td", "th"} and self.row is not None:
            self.row["cells"] += 1
        href = a.get("href")
        if href and tag in {"a", "link"}:
            self.links.append((tag, href))
            if tag == "a" and official(href):
                for _, active_id in self.stack:
                    if active_id:
                        self.id_sources[active_id].add(href)
                if self.row is not None:
                    self.row["direct"].add(href)
            elif tag == "a" and self.row is not None:
                self.row["indirect"].append(href)
        src = a.get("src")
        if src:
            self.assets.append((tag, src))
        if tag == "link" and href:
            self.assets.append(("link", href))
        remote_value = src or a.get("data", "")
        if tag in {"script", "iframe", "img", "embed", "object"} and remote_value.startswith(("http://", "https://", "//")):
            self.remote_active.append(tag + ": " + remote_value)
        if tag == "form" and a.get("action"):
            self.assets.append(("form", a["action"]))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self.title = False
        if tag == "thead":
            self.thead = max(0, self.thead - 1)
        if tag == "tr" and self.row is not None:
            if self.row["cells"]:
                for row_id in self.row["ids"]:
                    self.id_sources[row_id].update(self.row["direct"])
                self.rows.append(self.row)
            self.row = None
        if tag in VOID:
            return
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        elif tag in [t for t, _ in self.stack]:
            while self.stack and self.stack[-1][0] != tag:
                self.balance.append("unclosed <%s>" % self.stack.pop()[0])
            if self.stack:
                self.stack.pop()
        else:
            self.balance.append("stray </%s>" % tag)

    def handle_data(self, data: str) -> None:
        if self.title and data.strip():
            self.has_title = True


def load_identifier_tokens(args: argparse.Namespace) -> tuple[list[str], str]:
    if args.identifiers_stdin:
        return [line.strip() for line in sys.stdin.read().splitlines() if line.strip()], "stdin"
    if args.identifier_file:
        path = Path(args.identifier_file).expanduser().resolve()
        if path.is_relative_to(ROOT) and not is_ignored(path):
            raise SystemExit("Refusing an identifier file tracked inside the repository.")
        if not path.exists():
            raise SystemExit("Identifier file not found; no values were read.")
        return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()], "private-file"
    return [], "not-run"


def is_ignored(path: Path) -> bool:
    rel = str(path.relative_to(ROOT))
    return subprocess.run(["git", "check-ignore", "-q", rel], cwd=ROOT).returncode == 0


def resolve_local(page: Path, href: str) -> tuple[Path | None, str]:
    try:
        u = urlsplit(href)
    except ValueError:
        return None, ""
    if u.scheme or href.startswith(("mailto:", "tel:", "data:", "javascript:")):
        return None, ""
    target = (page.parent / unquote(u.path)).resolve() if u.path else page.resolve()
    if not target.is_relative_to(ROOT):
        return None, unquote(u.fragment)
    return target, unquote(u.fragment)


def scan_history(ref: str, tokens: list[str]) -> dict:
    """Exact-token history scan; output contains counts and paths only."""
    commits = subprocess.check_output(["git", "rev-list", ref], cwd=ROOT).decode().splitlines()
    affected_commits: set[str] = set()
    affected_paths: set[str] = set()
    versions = 0
    patterns = [re.compile(r"(?<![A-Za-z])" + re.escape(t) + r"(?![A-Za-z])") for t in tokens]
    for commit in commits:
        names = subprocess.check_output(["git", "ls-tree", "-rz", "--name-only", commit], cwd=ROOT).decode().split("\0")
        for name in filter(None, names):
            path = Path(name)
            if path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            try:
                raw = subprocess.check_output(["git", "show", f"{commit}:{name}"], cwd=ROOT, stderr=subprocess.DEVNULL)
                text = raw.decode("utf-8")
            except (subprocess.CalledProcessError, UnicodeDecodeError):
                continue
            versions += 1
            if any(p.search(text) for p in patterns):
                affected_commits.add(commit)
                affected_paths.add(name)
    return {
        "ref": ref, "commits_scanned": len(commits), "text_versions_scanned": versions,
        "commits_with_matches": len(affected_commits), "affected_paths": sorted(affected_paths),
        "values_redacted": True,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--identifier-file", help="Git-ignored/private exact-token list; values never emitted")
    ap.add_argument("--identifiers-stdin", action="store_true", help="Read exact tokens from stdin; values never emitted")
    ap.add_argument("--history-ref", help="Optional exact-token history scan, e.g. origin/main; requires exact tokens")
    ap.add_argument("--output", default="audit/results.json")
    ap.add_argument("--manifest", default="audit/artifact-manifest.csv")
    ap.add_argument("--no-page", action="store_true", help="Do not rewrite the tracked public audit page (CI gate mode)")
    args = ap.parse_args()
    tokens, token_mode = load_identifier_tokens(args)
    if args.history_ref and not tokens:
        ap.error("--history-ref requires exact identifiers; a generic history pass is not an exact clearance")

    files = tracked_files()
    failures: list[dict] = []
    warnings: list[dict] = []
    texts: dict[Path, str] = {}
    pages: dict[Path, Page] = {}
    manifest = []
    current_privacy_files: set[str] = set()
    generic_initial_files: set[str] = set()
    street_candidates: set[str] = set()

    def fail(kind: str, path: str, detail: str, line: int | None = None) -> None:
        failures.append({"kind": kind, "path": path, "line": line, "detail": detail})

    def warn(kind: str, path: str, detail: str, line: int | None = None) -> None:
        warnings.append({"kind": kind, "path": path, "line": line, "detail": detail})

    for path in files:
        rel = str(path.relative_to(ROOT))
        raw = path.read_bytes()
        text = text_of(path)
        if text is not None:
            texts[path] = text
        for token in tokens:
            if text is not None and re.search(r"(?<![A-Za-z])" + re.escape(token) + r"(?![A-Za-z])", text):
                current_privacy_files.add(rel)
                fail("exact-identifier", rel, "Supplied identifier match; value withheld")
        if text is not None:
            for number, line in enumerate(text.splitlines(), 1):
                if MERGE_MARKER.match(line):
                    fail("merge-marker", rel, "Unresolved merge marker", number)
                if path.suffix in {".html", ".js", ".css"} and MALFORMED_ANCHOR.search(line):
                    fail("malformed-anchor", rel, "Anchor URL is missing href=; source link is not usable", number)
                if any(m.group() not in CIVIC_ABBREVIATIONS for m in INITIAL_PAIR.finditer(line)):
                    generic_initial_files.add(rel)
                    fail("initial-pattern", rel, "Initial-shaped pair; value withheld pending review", number)
                if STREET.search(line):
                    street_candidates.add(rel)
                    warn("address-candidate", rel, "Street-shaped text; verify public agency address, not property address", number)
            for tracker in (TRACKERS if path.suffix in {".html", ".js", ".css"} else ()):
                if tracker in text:
                    fail("tracker", rel, "Tracker token: " + tracker)
        if path.suffix == ".html":
            page = Page()
            page.feed(text or "")
            page.close()
            pages[path] = page
            if page.h1 != 1:
                fail("html-structure", rel, f"Expected one h1, found {page.h1}")
            for flag, present in [("lang", page.lang), ("main", page.main), ("title", page.has_title), ("viewport", page.viewport)]:
                if not present:
                    fail("html-structure", rel, "Missing " + flag)
            for ident, count in Counter(page.ids).items():
                if count > 1:
                    fail("duplicate-id", rel, "Repeated id: " + ident)
            for problem in page.balance + ["unclosed <%s> at EOF" % t for t, _ in page.stack]:
                fail("tag-balance", rel, problem)
        manifest.append({
            "path": rel, "bytes": len(raw), "lines": len(text.splitlines()) if text is not None else "",
            "sha256": hashlib.sha256(raw).hexdigest(),
            "text_scanned": text is not None,
            "exact_identifier_check": token_mode,
        })

    # Resolve source-register anchors before judging indirect table citations.
    source_maps = {p.resolve(): {k: sorted(v) for k, v in pg.id_sources.items() if v} for p, pg in pages.items()}
    row_counts = Counter()
    unsourced_rows = []
    indirect_rows = []
    link_count = 0
    external_urls: set[str] = set()
    for path, page in pages.items():
        rel = str(path.relative_to(ROOT))
        is_archive = not (path == ROOT / "index.html" or path.is_relative_to(ROOT / "hub") or path.is_relative_to(ROOT / "audit"))
        for row in page.rows:
            row_counts["total"] += 1
            resolved_sources = set(row["direct"])
            for href in row["indirect"]:
                target, fragment = resolve_local(path, href)
                if target and fragment:
                    resolved_sources.update(source_maps.get(target, {}).get(fragment, []))
            if resolved_sources:
                row_counts["direct" if row["direct"] else "indirect"] += 1
                if not row["direct"]:
                    indirect_rows.append({"path": rel, "line": row["line"]})
            else:
                row_counts["untraceable"] += 1
                item = {"path": rel, "line": row["line"]}
                unsourced_rows.append(item)
                (warn if is_archive else fail)("row-source", rel, "No direct or resolvable official source for data row", row["line"])
        for tag, href in page.links + page.assets:
            link_count += 1
            try:
                u = urlsplit(href)
            except ValueError:
                fail("malformed-url", rel, "Malformed URL in " + tag)
                continue
            if u.scheme:
                if u.scheme not in {"https", "mailto", "tel"}:
                    fail("url-scheme", rel, "Unexpected scheme in " + tag)
                elif u.scheme == "https":
                    external_urls.add(href)
                    if not official(href):
                        warn("external-publisher", rel, "Outside official-source allowlist: " + href)
                continue
            if href.startswith(("mailto:", "tel:", "data:", "javascript:")):
                continue
            target, fragment = resolve_local(path, href)
            if target is None or not target.exists():
                fail("local-target", rel, "Missing local target: " + href)
            elif fragment and target in pages and fragment not in pages[target].ids:
                fail("local-anchor", rel, "Missing anchor: " + href)
        for tag in page.remote_active:
            warn("remote-active-element", rel, "Review remote/active element: " + tag)

    # Every mirrored HTML/CSS/JS/data artifact must match its root counterpart.
    mirror_count = 0
    for path in files:
        rel = path.relative_to(ROOT)
        if rel.parts[0] == "site" and len(rel.parts) > 1:
            original = ROOT.joinpath(*rel.parts[1:])
            mirror_count += 1
            if not original.exists() or original.read_bytes() != path.read_bytes():
                fail("mirror-parity", str(rel), "Missing or differing root counterpart")

    history = scan_history(args.history_ref, tokens) if args.history_ref else None
    prior_history = None
    prior_exact = None
    output = ROOT / args.output
    if output.exists():
        try:
            prior = json.loads(output.read_text(encoding="utf-8"))
            prior_history = prior.get("history") or prior.get("last_history_scan")
            if prior.get("exact_identifier_check") in {"stdin", "private-file"}:
                prior_exact = {k: prior.get(k) for k in (
                    "exact_identifier_check", "exact_identifier_count",
                    "current_exact_match_files", "tracked_files", "text_files_scanned")}
            else:
                prior_exact = prior.get("last_exact_scan")
        except (json.JSONDecodeError, OSError):
            pass
    if history and history["commits_with_matches"]:
        warnings.append({
            "kind": "historical-privacy", "path": args.history_ref, "line": None,
            "detail": "Exact identifiers remain in public history; current-file cleanup is not history removal. Values withheld.",
        })

    result = {
        "schema": 1,
        "scope": "All tracked artifacts; all root HTML including archived sets; local targets and citation traceability. Not a live external URL monitor or legal certification.",
        "tracked_files": len(files), "text_files_scanned": len(texts), "html_files": len(pages),
        "table_rows": dict(row_counts), "links_and_assets_checked": link_count,
        "unique_external_urls": len(external_urls), "mirror_files_checked": mirror_count,
        "exact_identifier_check": token_mode, "exact_identifier_count": len(tokens),
        "current_exact_match_files": sorted(current_privacy_files),
        "generic_initial_match_files": sorted(generic_initial_files),
        "street_shaped_candidate_files": sorted(street_candidates),
        "untraceable_rows": unsourced_rows, "indirect_only_rows": indirect_rows,
        "history": history, "last_exact_scan": prior_exact, "last_history_scan": prior_history,
        "failures": failures, "warnings": warnings,
        "limitations": [
            "A source link does not prove that every sentence in a row is supported; semantic review is separate.",
            "Owner-supplied rents, dates, coverage and license status are not authenticated by a government URL.",
            "Without exact stdin/private-file input, only generic initial/address patterns run.",
            "Historical matches, forks, caches and clones are not removed by this audit.",
            "External URL retrieval evidence is recorded separately in audit/source-review.json.",
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest_path = ROOT / args.manifest
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "bytes", "lines", "sha256", "text_scanned", "exact_identifier_check"])
        writer.writeheader()
        writer.writerows(manifest)
    if not args.no_page:
        audit_page.write(ROOT, result)
    print(f"Repository audit: {len(files)} tracked files, {len(pages)} HTML files, {row_counts['total']} data rows")
    print(f"Exact identifier check: {token_mode}; current matching files: {len(current_privacy_files)}")
    print(f"Rows: {row_counts['direct']} direct, {row_counts['indirect']} indirect, {row_counts['untraceable']} untraceable")
    print(f"Failures: {len(failures)}; review warnings: {len(warnings)}")
    for item in failures[:30]:
        print(" FAIL", item["kind"], item["path"], item.get("line") or "", item["detail"])
    if history:
        print("History:", history["commits_with_matches"], "affected commits;", len(history["affected_paths"]), "paths; values withheld")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
