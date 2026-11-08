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

---

## Re-check — 8 November 2026 (session `arena/aa463593`)

Line-by-line re-check of the privacy position, with the repository unshallowed first so the whole
history (53 commits, not the 2-commit shallow clone) was scanned.

### What is clean now

- **No supplied identifier appears in any file in the current tree.** Built-initials were tested in
  spaced, dotted and run-together forms across all 167 tracked text files: **0 matches**.
- **The current scripts are clean.** Retrieved `scripts/independent_audit.py` directly from the live
  site and read it: it now loads exact tokens from git-ignored `private/identifiers.txt`, and no
  identifier is echoed into output. `tools/check_links.py` and `tools/release_gate.py` use the same
  pattern. `private/` and `PRIVATE.md` are both git-ignored and not tracked.
- **No street address, parcel number, APN or block/lot** appears in any published page.

### What is still exposed — flagged, not fixed

1. **History.** The literal initials remain in earlier commits of
   `scripts/check.py` (1 commit), `scripts/independent_audit.py` (21), `tools/check_links.py` (16) and
   `tools/release_gate.py` (3). Current files are remediated; **history is not rewritten**. Rewriting
   shared history has consequences and cannot guarantee removal from forks, caches or prior Pages
   deployments. This is another session's earlier work and is published as F15 rather than acted on
   unilaterally here.
2. **Publication surface.** Pages is `main:/`, so every tracked file is public, not just the HTML
   pages. Confirmed by fetching `/internal/notes.md` and `/COORDINATION.md` from the deployed URL:
   both returned 200. The note in `internal/notes.md` that claimed it was unpublished was wrong and
   has been corrected in this pass. Published as F21.

### Recommended owner actions (not performed here)

- If any further personal data enters the repository, stop: it will be public within one Pages build.
- To reduce the surface, either publish a dedicated artifact directory instead of the repository root,
  or make the repository private and confirm Pages access settings — both are repository-settings
  changes, not file changes.
- To address history, see GitHub's guidance on
  [removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
  and decide deliberately. Do not assume past exposure has been reversed.
