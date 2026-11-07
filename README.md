# Rent Increase SF (94122)

Research and verification dashboard for rent increases on two rent-controlled units in San Francisco's Outer Sunset (ZIP 94122). Built by an individual (non-corporate) property owner. All personal information is anonymized; dates and dollar amounts are preserved.

## What this repo contains

- **Live site (GitHub Pages):** https://kanlerxz87-cyber.github.io/RentincreaseSF5/
  - `index.html` — Executive summary (the rent increase license answer is forefront)
  - `pages/process.html` — Step-by-step Rent Board process
  - `pages/rates.html` — Allowable annual increase rates (Form 571 history)
  - `pages/units.html` — Anonymized unit profiles + normal increase scenarios
  - `pages/notices.html` — Tenant notification rules (30/90-day notice)
  - `pages/questions.html` — Answers to the owner's questions
  - `pages/review.html` — Flagged for Review (irregularities & unverified items)
  - `pages/sources.html` — Every official source link
- `COORDINATION.md` — shared task board, verification notes, flagged items

## Key verified findings

1. **Rent increase license required (individual owners too)** — SF Admin Code Sec. 37.15 (Ord. 265-20, eff. 1/18/2021): all owners must report into the Housing Inventory and hold a rent increase license before imposing annual/banked increases.
2. **Current allowable annual increase: 1.6%** (3/1/2026–2/28/2027), 60% of Bay Area CPI-U, capped at 7% (Sec. 37.3(a)(1)).
3. **Notice:** 30 days for increases ≤10%, 90 days for >10% (+5 days if mailed) — CA Civ. Code Sec. 827(b).
4. **AB 1482 (5%+CPI/10% cap) does not apply** to SF rent-controlled units; SF rules govern.
5. **Petition-based increases** (capital improvements, operating expenses, etc.) require a Rent Board petition filed before notice.
6. **Federal:** no rent cap/license; Fair Housing Act (42 U.S.C. Sec. 3604) applies.

Every data row on the site links to an official source (sf.gov, leginfo.legislature.ca.gov, govinfo.gov). Unconfirmed values are left blank and flagged on the Flagged for Review page.

## Verification protocol

- No hallucinations: every claim traces to an official source link.
- Unverified values are never inferred — left blank and flagged.
- The owner's specific facts (lease dates, rents) are labeled "Per owner" and flagged where independently unverifiable.
