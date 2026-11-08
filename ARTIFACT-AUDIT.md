# Repository and source artifact audit — 8 November 2026

**Session:** `arena-e126bdbe`  
**Scope:** every tracked text artifact, all HTML tables/links/assets, all mirrored copies, current exact-token privacy, and reachable `origin/main` history. No tenant identifiers are reproduced here.

## Release status

**Mechanical release checks pass; review warnings remain.** The existing consolidated release gate, follow-up checks and the new whole-repository mechanical audit pass after the missing docs mirror was added. Untraceable archived rows, mobile header overflow in the active hub, and historical identifier exposure remain disclosed review items; this is not legal certification or a privacy-history clean bill.

## What was checked

- 196 tracked files; 115 HTML files; 2,129 table data rows; links/assets recorded in `audit/results.json`.
- Exact-token privacy check supplied only through stdin: **0 current matching files**. A generic initial-shaped-pair heuristic remains advisory and is not equivalent to exact review.
- History: 78 commits / 8,252 text versions scanned on `origin/main` at the last exact scan. **22 commits** still contain exact identifier tokens in four prior checker paths. Values and raw lines are withheld. Current-file cleanup did not erase history.
- Tables: 1,595 rows have a direct official citation in the row; 166 have an indirect caption/section citation; 368 archived/mirror rows are not traceable to a source in their own row. Indirect citations are disclosed, not silently treated as row-level proof.
- Five released archive pages had 92 malformed source anchors (`<a https://...>`). Repaired to usable `href` links and mirrored byte-for-byte; no legal text or figures changed. A regression check now rejects malformed URL anchors.
- Browser render: desktop 1440px clean; mobile 390px had 8px document overflow from the nowrap header brand. Requested fix from the active CSS owner (PR #18); tables already scroll inside their wrappers. No JavaScript page errors observed.
- Repaired: the released archive target `site/docs/index.html` now exists by mirroring the existing tracked `docs/` set through `scripts/build.py`; no active hub file was edited.

## Legal/source review

`audit/source-review.json` records direct retrieval evidence and scope. `audit/register-line-review.csv` reviews all 62 consolidated findings against the retrieved official text/guidance.

The core answer remains: individual and corporate owners have the same Inventory obligation; tenant-occupied reporting generates the rent-increase licence automatically; the licence must be current on the increase effective date; ordinary annual/banked increases do not require a petition. Checking before service is prudent workflow, not a quoted legal prerequisite.

Blank/unverified items remain blank: actual licence status, actual lawful base rents, complete Unit 2 rent history, 2027–28 annual rate, official ZIP-level market rent, empirical corporate-practice norm, and any universal federal rent ceiling or uniform-increase rule. Banked arithmetic is conditional, not an approved entitlement. No increase is certified to survive a tenant-side lawyer's review.

## Privacy limitation

The repository is public and Pages publishes `main:/`, so tracked non-HTML files are also served. `/internal/notes.md` was directly retrieved from the live site and now warns readers that it is public. The new audit script is not yet on live `main` (404 at check time). GitHub API confirms public reachability of repository contents. Earlier commits still expose identifiers; force-pushing a rewrite alone cannot remove clones, forks, cached views or open PR refs. No destructive history rewrite was attempted while other sessions were active. See GitHub's official [sensitive-data removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) and [Pages publishing-source guidance](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Reproduce

```bash
python3 scripts/build.py
python3 scripts/check.py
python3 scripts/independent_audit.py
python3 tools/check_links.py
python3 tools/dashboard_check_links.py
python3 tools/verify_site.py
python3 tools/release_gate.py
python3 tools/repository_audit.py
python3 tools/followup_audit.py
```

For the exact-token scan, keep the six literal tokens outside Git and pipe them through stdin; never paste them into a public file, command transcript or report. `tools/repository_audit.py --identifiers-stdin --history-ref origin/main` records only counts/paths, not values. A later CI run without tokens preserves the last exact/history result as explicitly labeled prior evidence, not a fresh CI scan.

## Live release verification

PR #24 merged as `7eb39fb`; validation and Pages deployment succeeded. Cache-busted live fetches confirmed the audit page, repaired docs mirror target and audit script are served from `main:/`. Live review caught and this follow-up corrects a generated-page count-rendering defect (raw list representations instead of integer counts); the corrected page is compact and responsive. Historical privacy exposure remains unresolved and disclosed.
