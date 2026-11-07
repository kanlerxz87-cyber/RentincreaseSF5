# Coordination

Session: arena-f5ead75b. All work stays on the Arena-assigned branch `arena/f5ead75b-rentincreasesf5` (platform requirement; no session branch created).

| Task | Status | Owner | File scope |
|---|---|---|---|
| Official-source research, privacy-safe dashboard, tests and publication integration | in progress | arena-f5ead75b | COORDINATION.md, site/**, scripts/**, .github/workflows/**, README.md |

## Log
- 2026-11-07: Empty repository inspected; no other claims. Claimed sole integration scope. Private tenant identifiers will not be copied into files. Owner-supplied dates and amounts are unverified, not official records.
- Claim bootstrap: remote Arena branch did not exist; initial pull failed without modifying work. Rebased against origin/main and pushed claim to assigned branch.
- 2026-11-07: Research read against SF Housing Inventory, annual-increase guidance, rental coverage, Rule 4.10, AB1482 guidance, California Civil Code §§827 and 1942.5, CRD housing guidance, and HUD guide. Full manual-review links are in Sources page. Source-date inconsistency in SF annual example published as F07.
- Privacy: no tenant names/initials or exact address copied. Owner-reported dates/amounts retained separately and marked unverified. Illustrations are derived, not verified rents. No license/notice/legal action performed.
- Validation: Python build succeeds; local href targets, every table data-row official link, source hostname allowlist, headings and no analytics checks pass. External references retrieved by research tools; no claim of exhaustive automated external-link health. No browser rendering automation available/used.
- Research irregularities task: needs review (published site/flagged.html F01–F10; property evidence, legal eligibility and empirical norms remain unknown). Integration implementation complete; publication in progress.
- Deployment adaptation: Pages configuration update returned HTTP 403 (integration lacks Pages-admin permission). Existing Pages configuration already publishes main:/; scope extended to generated root *.html, style.css and .nojekyll (no other session claims exist). Preserve existing deployment settings and use root static files instead of requiring admin changes. Workflow will validate only; GitHub's existing Pages build publishes after merge.
