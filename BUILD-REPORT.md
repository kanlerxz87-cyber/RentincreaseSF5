# Build report — verified dashboard set

Generated: 2026-11-07 20:20 UTC

The repository builds in one command. `scripts/build.py` builds the earlier set, then the dashboard set (`build.py`), then the hub (`tools/build_site.py`), and mirrors everything into `site/`.

## `python3 scripts/build.py` (full pipeline)

```
Built 10 pages into dashboard/ and mirrored to site/dashboard/
Verified rows: 52 | analysis rows: 4 | sources: 33 | flagged: 14
  Unit 1 U1-A   1.6% -> $63.92 (new rent $4,058.92), notice 30 days, serve by 2027-01-02
  Unit 1 U1-B     3% -> $119.85 (new rent $4,114.85), notice 30 days, serve by 2027-01-02
  Unit 2 U2-A   1.6% -> $50.40 (new rent $3,200.40), notice 30 days, serve by 2027-01-29
  Unit 2 U2-B  13.1% -> $412.65 (new rent $3,562.65), notice 90 days, serve by 2026-11-30
  Unit 2 U2-C    10% -> $315.00 (new rent $3,465.00), notice 30 days, serve by 2027-01-29
Wrote 13 files.
Broken internal links: 0
Table rows without a source link or status badge: 0
Built 6 pages / 50 finding rows
```

## `python3 tools/check_links.py` (dashboard set)

```
pages checked: 10
mirror parity: site/dashboard/ compared against dashboard/
internal links: 342 | external links: 36
data rows: 56 facts, 6 questions, 14 flagged, 50 source tags

All internal links, anchors and source tags resolve. No problems found.
```

## Repository checks (earlier + deep-dive sets)

```
PASS: local links, official source allowlist, every data row source, page headings, no analytics
PASS: 6 pages, 55 official-sourced data rows, root/site parity, internal links, stylesheet, landmarks, identifier exclusion
```

## `python3 tools/build_site.py`

```
Wrote 13 files.
Broken internal links: 0
Table rows without a source link or status badge: 0
```

## Output trees

```
assets
executive-summary.html
findings.html
flagged.html
index.html
market.html
method.html
process.html
questions.html
sources.html
units.html

app.js
style.css
```
