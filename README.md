# SF Rental Review

Privacy-first, official-source research dashboard for San Francisco rent-controlled housing.

Live site: https://kanlerxz87-cyber.github.io/RentincreaseSF5/

## Build and validate

Requires Python 3 only; no third-party packages or remote UI assets.

```sh
python scripts/build.py
python scripts/check.py
python -m http.server 8000 --bind 0.0.0.0 --directory site
```

Content lives in `scripts/build.py`; generated static pages and stylesheet live in `site/`. GitHub Actions verifies PRs. Existing GitHub Pages legacy publishing serves main from the repository root; the root landing file redirects to `site/`. Source register and Flagged for Review pages document evidence, unresolved facts and official-source irregularities. Verification is dated November 7, 2026; no automatic legal updates are implied.

No actual tenant names, supplied initials, street address, portal credentials or private lease documents are stored. User-reported dates/rents are explicitly unverified scenario context, not official facts. Verified unit-specific values are intentionally blank. Public dates and rents can still be identifying; this is pseudonymization, not an anonymity guarantee. Do not add private files to this public repository.

Research is not legal advice; no tenant notice or government filing has been made.
