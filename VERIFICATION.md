# Independent verification report — T6

**Session:** `session-a00d318d` / platform branch `arena/a00d318d-rentincreasesf5`  
**Initial report date:** 2026-11-07 UTC  
**Release status:** NOT YET VERIFIED — the other session's research/data/site integration is not present on this branch.

## Ownership and repo review

The initial repository contained only `README.md`, line 1: `# RentincreaseSF5`. A concurrent session subsequently published `COORDINATION.md` at commit `528c731` and claimed T1–T5 and integration T7. This session preserved that commit, claimed only T6, and pushed the claim before implementation. No research, data, index, navigation, or site page owned by the other session has been edited here.

## Implemented checks

- `scripts/verify.py`: standard-library-only CSV/JSON, HTML, source-domain, local-link/fragment, row-to-render mapping, privacy-term, optional external-HTTP and arithmetic checks.
- `scripts/tests/test_verify.py`: 21 synthetic tests, all passing at this checkpoint. No actual tenant identifiers are used in fixtures.
- `.github/workflows/verify.yml`: PR/dispatch verification job. Action revisions were checked against the official GitHub repositories and pinned by commit SHA.
- `docs/VERIFICATION-CONTRACT.md`: integration schema and release criteria, published for the owner of the shared outputs.

The incomplete-tree audit correctly fails with `SITE_MISSING`, `DATA_MISSING`, and `FLAG_PAGE`; this is an integration blocker, not a passed site. CI's exact-private-term audit is deliberately not claimed: that check requires private runtime input and must be run locally before release. CI also does not constitute a lawyer's review.

## Official-source reading performed for the audit contract

These checks support the verification requirements; they are not a substitute for the pending line-by-line review of the integrated research.

| Check | Official evidence read | Result |
|---|---|---|
| Individual owners and license | [SF Rent Board Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) requires residential owners to report; tenant-occupied reporting generates a license; a current license is needed before an annual/banked increase takes effect. | Confirmed agency guidance. No individual-owner exemption found in this guidance. Do not infer this property's actual license status. |
| Public-file privacy | [SF Rent Board Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) says submitted information is public and lists owner/business contact information among required filings. | Confirmed. Anonymous website labels do not make mandatory government filings anonymous. |
| Current increase rate | [SF Rent Board current rates](https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit) states 1.6% for March 1, 2026–February 28, 2027. | Confirmed rate and effective period, not an entitlement to increase either unit without the other prerequisites. |
| Notice and roommate rule | [SF Rent Board rent-increase guidance](https://www.sf.gov/learn-about-rent-increases-san-francisco) states 30 days, 90 days above 10%, five more days if mailed; it also says no additional rent merely for an additional roommate with an existing tenant. | Confirmed guidance. Actual prior increases, lease terms and service dates remain unverified. |
| Banking examples | [SF Rent Board rent-increase guidance](https://www.sf.gov/learn-about-rent-increases-san-francisco) explains anniversary changes and loss of an unbanked increase. | Confirmed guidance. Do not infer a banking balance from a lease date and rent alone. |
| Code-source irregularity | A guessed SF.gov ordinance URL returned a visible Not Found page; search then located [SF Administrative Code §37.15 on the official code publisher](https://codelibrary.amlegal.com/codes/san_francisco/latest/sf_admin/0-0-0-16540). | Guessed URL rejected, not used as evidence. Official code location identified for proposition-level integration review. |
| CI action provenance | [checkout v7.0.1](https://github.com/actions/checkout/releases/tag/v7.0.1), [setup-python v7.1.0](https://github.com/actions/setup-python/releases/tag/v7.1.0), and GitHub tag APIs for the pinned revisions. | Confirmed official action repositories/revisions. |

## Outstanding release gates

1. Obtain the other session's integrated research/data/site without overwriting its work or taking its active claims.
2. Read every substantive row against its official source; record mismatches and missing evidence, not just working URLs.
3. Run the strict external/local-link audit and exact sensitive-term audit with private input that is never committed or echoed.
4. Inspect the site at desktop/mobile sizes and verify the GitHub Pages base path and live deployment.
5. Hand findings to the owning integration session through `COORDINATION.md`; T7 remains its claimed task unless a documented stale-claim handoff occurs.

No tenant attorney has reviewed or approved this project. No such approval is claimed.
