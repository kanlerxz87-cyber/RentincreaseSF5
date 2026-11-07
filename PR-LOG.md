# PR log and deployment record

## Pull requests

| PR | Title | Base ← Head | Result |
| --- | --- | --- | --- |
| [#4](https://github.com/kanlerxz87-cyber/RentincreaseSF5/pull/4) | SF rent-increase compliance research + public dashboard (Outer Sunset, 94122) | `main` ← `arena/8b5ad092-rentincreasesf5` | **MERGED** 2026-11-07T20:20:33Z, merge commit `a6672cc` |
| #5 | Record PR, merge result and Pages deployment in COORDINATION.md / PR-LOG.md | `main` ← `arena/8b5ad092-rentincreasesf5` | this record |

PR #4 was merged without waiting for review, per the project instruction. It contained the third
research set (`dashboard/`), the data files, the generator and checker, and the additive integration
with the two sets already published by earlier sessions.

### What happened to the first merge attempt

`gh pr merge 4` initially failed: *"Pull request #4 is not mergeable: the merge commit cannot be
cleanly created."* Cause: three other sessions had published to `main` while this session was
researching, and the branch had been cut from the original empty commit. Resolution: fetched
`main`, read the other sessions' work, merged `main` into the branch, and resolved the three
conflicting files by **combining, never replacing** (`README.md`, `COORDINATION.md`, `.gitignore`).
All of the other sessions' published pages were preserved byte-for-byte and all of their checks
still pass. Full detail in `COORDINATION.md`.

## Checks at merge time

| Check | Command | Result |
| --- | --- | --- |
| Full pipeline | `python3 scripts/build.py` | 6 pages / 50 rows (earlier set) → dashboard set → hub; **0 broken internal links** |
| Repository checks | `python3 scripts/check.py` | PASS — local links, official-source allowlist, every data row sourced, headings, no analytics |
| Independent audit | `python3 scripts/independent_audit.py` | PASS — 6 pages, 55 sourced rows, root/site parity, landmarks, identifier exclusion |
| Dashboard set | `python3 tools/check_links.py` | PASS — 10 pages, 342 internal links, 36 external links, all anchors and source tags resolve, `dashboard/` ≡ `site/dashboard/`, no personal-identifier token |
| Hub link check | `python3 tools/build_site.py` | 13 files written, 0 broken links, 0 rows without a source link or status badge |

## GitHub Pages deployment

| Item | Value |
| --- | --- |
| Configuration | source `main`, path `/`, legacy builder (pre-existing; not changed by this session) |
| Build after PR #4 merge | status **built** (polled via `gh api repos/…/pages/builds/latest`) |
| Site root | https://kanlerxz87-cyber.github.io/RentincreaseSF5/ — status 200, serves the consolidated hub |
| Third set | https://kanlerxz87-cyber.github.io/RentincreaseSF5/dashboard/ — status 200 |
| Unit analysis page | `…/dashboard/units.html` — 200, both units priced with computed notice deadlines |
| Flagged page | `…/dashboard/flagged.html` — 200, 14 items with source links |
| Hub integration | the hub now lists the third set; its intro reads "three independently compiled research sets" |
| Earlier sets | `…/pages/units.html`, `…/process.html`, `…/amounts.html` — 200, unchanged |

Pages serves through a CDN; the first request after deploy returned the previous cached hub and a
cache-busted request returned the new one. Recorded here because it briefly looked like a failed
deploy.

## Open items for the owner (none blocks the merge)

Published on `dashboard/flagged.html`, with sources:

1. **FL-03** — the banking conflict (sf.gov's 24-month wording vs S.F. Admin Code §37.3(a)(2)). Decides
   whether Unit 1 takes $63.92 (safe) or $119.85 (needs confirmation).
2. **FL-01 / FL-02** — base rents and the 1940 build year are owner-supplied; coverage is assumed.
3. **FL-05** — whether a §6.14 notice was served on Unit 1's new co-tenant.
4. **FL-14** — the repair-deferral rule (Form 516B): a tenant can defer an increase for unrepaired
   defects within 60 days of the notice, so the repair file matters as much as the arithmetic.
