# Verification contract — T6

**Scope:** independent checks of the research/data/site deliverables. This document does not claim that those deliverables have passed yet. It gives the integration session a stable target without taking ownership of its files.

## Publication and privacy

- The static entry point is `index.html` at the repository root (or `docs/index.html` if explicitly documented). Category pages and assets must be included in the published tree, not just generated locally.
- Use relative links or links beginning with `/RentincreaseSF5/`. Every local page, stylesheet, script, image, download, and fragment must resolve on GitHub Pages.
- Public occupant labels must be placeholders such as `Tenant A`, not supplied initials, real names, contact details, signatures, or a re-identification key. Preserve the owner-supplied dates and dollar amounts, but label them **owner-reported / not independently verified**.
- The public Housing Inventory is not an anonymous publication channel. The Rent Board says submitted information is public and requires owner/business contact information. Website anonymization does not remove or change official filing obligations. Official source: [SF Rent Board Housing Inventory](https://www.sf.gov/rent-board-housing-inventory).
- Do not put identifying values in this repository, including in tests, examples, commit messages, or error reports. The final local audit accepts a JSON array of sensitive strings on standard input and reports counts only. That input must come from the private conversation, not a committed file.

## Data rows

The preferred CSV schema is:

```text
id,category,finding,value,status,source_url,verified_at,notes
```

Aliases accepted by the checker are listed in `scripts/verify.py`. Additional columns are welcome. Suggested optional columns are `owner_reported_value`, `flag_id`, `base_rent`, `rate_percent`, `increase_amount`, and `new_rent`.

- Every row needs a stable ID, a verification status, and a clickable-equivalent HTTPS URL to an official source. A source on a separate bibliography page alone is not a row-level source.
- `verified`: the value is supported by the linked official source; `verified_at` is an actual retrieval date in ISO format; notes identify the supporting passage/rule. A link to a general portal is not proof of an individual license, property age, rent history, or tenancy.
- `unverified`: the authoritative `value` must be empty, not zero, `N/A`, a guess, or an inferred answer. Notes must explain the missing evidence and identify a Flagged for Review entry. The source URL remains mandatory as the official context or the place checked, and must not be presented as confirming the blank value.
- `owner-reported`: `value` must also be empty. Preserve supplied facts only in `owner_reported_value` and clearly label their provenance. Link official context without implying that the government confirmed the owner's facts.
- `calculated`: use only verified/owner-reported inputs, disclose the formula and input provenance, and link the official rule. An arithmetic result is not a government-verified fact or an authorized rent increase.
- Do not convert an unavailable license status, actual current rent, anniversary date, banking balance, exemption, or coverage determination into a presumed fact.

## HTML tables

- Every data-table row must contain its own official-source hyperlink. Header-only rows are excluded. Plain-text URLs and JavaScript-only citations are insufficient.
- Put `data-row-id` on each rendered data row so the automated checker can compare it with the CSV/JSON record. Every data ID must appear exactly once in the rendered data tables; every rendered data-row-id must have a data record.
- Rows marked unverified or owner-reported must link to the Flagged for Review page. Blank official values may be displayed as an em dash only when explicitly labeled unverified; do not substitute a fabricated value.
- Include the legal-information/not-legal-advice boundary, the verification date, and a visible distinction between verified rules, owner reports, calculations, and unresolved questions.

## Official-source policy

Government agencies, California Legislative Information, the official San Francisco code publisher, and primary official institutional sources are accepted according to the allowlist in the checker. A commercial blog, search snippet, Reddit post, or copied statute on an unofficial site is not an official legal source. Official organizations may document their own services, but are not substitutes for statutes or agency guidance.

The checker validates source hostname and URL syntax. With `--external`, it also requests the URLs and detects HTTP errors and known soft-404 pages. Network blocks are reported separately, not silently treated as successful verification. Source existence does **not** establish that a particular proposition follows from the source: the independent reviewer must read the source and record the proposition-level result in `VERIFICATION.md`.

## Checks and limits

Run:

```sh
python -m unittest discover -s scripts/tests -v
python scripts/verify.py --root . --base-path /RentincreaseSF5
```

For a release audit, after the integration files exist:

```sh
python scripts/verify.py --root . --base-path /RentincreaseSF5 --external --strict-warnings --require-sensitive-audit --json verification-report.json < /path/outside/repository/private-sensitive-terms.json
```

The last command is intentionally not suitable for a public CI secret containing tenant initials. Run it locally with private input; CI runs structural tests and checks without claiming that the private-term audit occurred. Keep `verification-report.json` out of Git unless it contains no private input (the checker never emits the input strings).

A release requires zero errors and no unchecked external links. Automated checks cover structure, row-source presence, blank-value discipline, source domains, arithmetic where inputs are supplied, local links/fragments, privacy terms supplied at runtime, and common metadata. They do not replace reading each legal proposition, inspecting the rendered site, confirming a live deployment, or obtaining a lawyer's actual review. No tenant-lawyer approval may be claimed unless a real review occurred.
