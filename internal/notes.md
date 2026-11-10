# Internal working notes — read this before relying on the word "internal"

**Corrected 8 November 2026.** An earlier version of this file said it was not published. That was wrong.

GitHub Pages for this repository is configured with **source = `main`, path = `/`**, so the *whole*
repository root is served publicly. This file is therefore reachable at
`/internal/notes.md` on the live site, and so is every other tracked file that is not excluded by a
`_config.yml`/`.nojekyll` rule. Verified by retrieving both this path and `/COORDINATION.md` from the
deployed URL; both returned 200.

Consequence: **assume every tracked file is public.** It contains **no tenant names, initials,
addresses, parcel numbers or owner identifiers** — those must stay outside this repository.

Additional 8 November 2026 finding: the *current* copies of `scripts/independent_audit.py`,
`tools/check_links.py` and `tools/release_gate.py` no longer contain any identifier (they read a
git-ignored `private/identifiers.txt`). Literal initials **do remain in earlier commits**; see
`PRIVACY-REVIEW.md` and flagged item F15. Do not assume the history is clean.

Placeholders used across the repo: `Tenant A1`, `Tenant A2`, `Tenant B1`, `Tenant B2`, `Unit A`, `Unit B`.

---

## The three phone calls before any notice is served

1. **Rent Board counsellor — 415-252-4600** (weekdays 9–12 and 1–4).
   Ask: (a) for both units, is the Housing Inventory report current and is the rent increase licence live?
   (b) does a skipped increase bank after 12 months or 24 months — the website says 24, Rule 4.12 says 12?
   (c) confirm the arithmetic: Unit A 1.4% + 1.6% = 3.0%; Unit B 1.8+0.7+2.3+3.6+1.7+1.4+1.6 = 13.1%.
2. **A landlord-side attorney** (one hour, paid). Ask: whether the 2025-02-01 base-rent reset on Unit A is safe;
   whether a §6.14 notice was required for Tenant A2; and whether to increase one unit or both in the same cycle.
3. **Rent Board portal check** — take a dated screenshot of the licence status for both units and file it with
   each notice. This is the single most common missing document in a petition defence.

## Documents to pull from the owner's file

- [ ] Unit A: lease starting 2025-02-01 showing $3,995.00.
- [ ] Unit A: the document that ended the *previous* tenancy (notice, surrender, buyout, vacate letter).
- [ ] Unit A: any §6.14 notice served on Tenant A2, with date and proof of service.
- [ ] Unit B: lease starting 2019-06-01 showing $3,150.00, and every notice since (expected: none).
- [ ] Both: Housing Inventory submission confirmations, year by year.
- [ ] Both: Rent Board fee receipts ($59 per unit, 2026-27) or exemption approvals.
- [ ] Both: rent ledger (date, amount, method) for the whole tenancy.

## Calendar once the strategy is chosen

Dates assume the notice is drafted in November 2026. Recompute from the actual service date.

| Service / effective date | Action |
| --- | --- |
| 2026-11-12 | **Deadline pressure:** last day to *mail* Unit B's 90-day notice for a 2027-02-15 effective date. |
| 2026-11-17 | Last day to *personally serve* Unit B's 90-day notice for a 2027-02-15 effective date. |
| 2026-12-28 | Last day to *mail* Unit A's 30-day notice for a 2027-02-01 effective date. |
| 2027-01-02 | Last day to *personally serve* Unit A's 30-day notice for a 2027-02-01 effective date. |
| 2027-02-01 | Unit A effective date (3.0% → $4,114.85). If served later than this, the anniversary date moves. |
| 2027-02-15 | Unit B alternative effective date (13.1% → $3,562.65); anniversary moves to 15 February. |
| 2027-02-26 | Last day to *mail* Unit B's 90-day notice for a 2027-06-01 effective date (anniversary kept). |
| 2027-03-01 | Rent Board fee due ($118 for two units) **and** Housing Inventory update due. |
| 2027-03-03 | Last day to *personally serve* Unit B's 90-day notice for a 2027-06-01 effective date. |
| 2027-06-01 | Unit B anniversary-date effective date (13.1% plus the 2027-28 rate, once published). |

The 2027-02-15 route for Unit B needs a notice served in the next ten days. If that is not realistic, keep the
1 June anniversary date and serve by 3 March 2027 — the computed total is the same 13.1% either way, and the
1 June route also picks up the 2027-28 allowance.

## Decision still open

Do both units in one cycle, or Unit A now and Unit B on its own anniversary? The legal record supports either,
provided the same written method is applied to both. See `pages/owner-practices.html`.

## Known gaps (published on the Flagged for review page)

- F1 banking waiting period: 12 vs 24 months (official pages disagree).
- F2 Ordinance 261015 (10% cap on banked increases): superseded. The real file is Board of Supervisors File 261020; official Legistar status "Pending Committee Action" (introduced 15 September 2026). See hub/flagged.html F09/F22.
- F3 Unit A base-rent reset lawfulness.
- F4 Tenant A2 status and §6.14 notice.
- F5 HUD Fair Market Rent: no official value confirmed.
- F6 No provision ties fee payment to increase validity.
- F7 No provision requires equal increases across units.
