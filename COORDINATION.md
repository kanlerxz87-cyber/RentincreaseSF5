# Coordination

Session: arena-05e5d5ab. Started 2026-11-07 UTC. Assigned branch: arena/05e5d5ab-rentincreasesf5 (platform-required; no alternate branches).

| Task | Status | Owner | File scope |
|---|---|---|---|
| Official-source research, privacy review, site implementation and final integration | in progress | arena-05e5d5ab | COORDINATION.md, README.md, site/**, scripts/**, .github/workflows/** |

Repository initially contained only README.md. No other claims existed. Do not publish supplied personal identifiers. Supplied tenancy facts are not officially verified and will not populate verified-value tables.

## Integration log · 2026-11-07
- Claim pull from assigned branch initially failed because the remote branch did not exist; pulled/rebased main, then created only the assigned remote branch by pushing the claim. No conflict or other session found.
- Integration additionally owns root `index.html` and `.nojekyll`, required by existing Pages root/main configuration.
- Research: directly read official SF Housing Inventory, rate schedule, general rent guide, §37.3, Part IV rules, and California Civil Code §§827, 1947.12 and 1942.5. Official extracted text reviewed for banking, roommate, CRD, HUD and counsel references. Source register: site/sources.html. Per-row evidence links provided; private facts not officially authenticated.
- Needs review: site/flagged.html publishes missing tenancy/license records, no historical bank calculation, official example date errors, missing market/industry evidence, privacy re-identification risk and no lawyer review. These are not publication blockers.
- Verification: Python build completed; 7 pages / 60 body rows have official source links; local navigation/style paths, HTML language/landmark and supplied-initial exclusion pass. External government links were retrieved using research tools, not a blanket HTTP crawl (sandbox outbound restrictions).
- Deployment adaptation: Pages read API confirmed existing main/root legacy publishing. Changing Pages to workflow mode returned HTTP 403 (integration permission). Preserved legacy deployment instead; no credential changes needed. Workflow is validation-only; root redirect and .nojekyll support existing publisher.
