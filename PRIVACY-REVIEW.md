# Privacy review — 2026-11-07

## Needs review: tenant initials in publicly accessible source files

The site's readable dashboard pages use placeholders, but two verification scripts contain literal tenant initials in lists intended to detect identifiers. GitHub Pages is configured to publish the repository root with `.nojekyll`; both files were independently retrieved from the deployed site:

- `scripts/independent_audit.py`, identifier-exclusion loop.
- `tools/check_links.py`, identifier-exclusion list.

No initials are repeated in this report. Their presence is not proof that every reader can identify a tenant, but it conflicts with the requested privacy policy and should be treated as an exposure. Because the repository is public, a file under `internal/` is not private merely because of its directory name. The user-supplied dates and rents remain deliberately published as requested; those combinations can still be identifying in context.

**Requested remediation by file owners:** remove the real identifiers from current files and replace the tests with a privacy-preserving method that does not commit or publish those identifiers. Ensure errors do not echo sensitive values. Add this issue to the site's Flagged for Review page without reproducing the identifiers. Check the full published tree, not only HTML pages. Consider deploying a dedicated public artifact rather than the repository root; this alone will not make a public GitHub repository private.

Removing strings from the current branch and redeploying does not remove them from public git history, forks, caches, or prior deployments. Review GitHub's official guidance on [removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) before deciding on any history rewrite or removal request; rewriting shared history has consequences and cannot guarantee removal from all copies. Do not assume past exposure has been reversed.

## Scope and checks

Reviewed tracked working-tree text for the supplied initials; matches were found in the two scripts above. Fetched both directly from the live Pages site. Existing HTML-focused checks passed but did not check the scripts containing the test inputs. This was a targeted search, not a guarantee that no other identifying information exists. No source files owned by other sessions were changed.
