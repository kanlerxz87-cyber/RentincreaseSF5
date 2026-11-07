# SF Rent Review

Privacy-safe, official-source research dashboard. Public site: https://kanlerxz87-cyber.github.io/RentincreaseSF5/

## Build and validate

Requires Python 3, no packages or external assets:

```
python scripts/build.py
python scripts/check.py
python -m http.server 8000 --bind 0.0.0.0 --directory site
```

Research checked November 7, 2026. All table rows link official rule references; unverified actual property values are blank. Owner-reported dates/amounts are separately labeled, not authenticated. Names/initials, address and personal documents are not stored. Recommendations and hypothetical arithmetic are not official legal determinations. No notices served or inventory reports filed. See the site's Flagged for Review and Sources pages.

The source-of-truth content is in scripts/build.py; generated HTML is in site/. GitHub Actions validates all pages. Generated files are mirrored to the repository root for the existing main:/ GitHub Pages deployment (Pages-admin API changes are not permitted to this integration). Local link and source-coverage checks do not establish permanent external availability or legal correctness.
