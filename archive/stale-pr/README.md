# Stale pull-request artifacts — preserved, not active

These files come from open pull requests that were closed as superseded during the
10 November 2026 final integration. They are stored as `.txt` snapshots so that
they are not part of the live site navigation, release gate or active CI. The
original PR heads remain available through GitHub's pull-request refs.

- PR #5 contributed the historical deployment record now preserved at `../../PR-LOG.md`.
- PR #7 contributed an independent verifier, synthetic tests, a verification
  contract and a workflow. Its verifier expects a different CSV contract from the
  current `tools/release_gate.py`; running it against this tree reports schema
  errors, so it is archived rather than activated.
- PR #18 contributed an independent audit page, a notice-kit page and a Markdown
  audit. Later merged integration work superseded those pages; text snapshots are
  kept here with their original 8 November 2026 wording.
- PR #17 and PR #20 contained no files unique relative to the merged `main`
  tree; their changes were superseded by later merged integration PRs.

Current site sources are listed in `../../hub/sources.html`,
`../../data/sources.csv` and `../../audit/source-review.json`. Current official
starting points include the [Rent Board Housing Inventory](https://www.sf.gov/rent-board-housing-inventory),
[Administrative Code sec. 37.15](https://www.sf.gov/information--sec-3715-reporting-obligations-licensing),
[Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf)
and [Board of Supervisors File No. 261020](https://sfgov.legistar.com/LegislationDetail.aspx?ID=8217304&GUID=7EDA4662-EBFB-4AF5-962F-C669B64AA770).
