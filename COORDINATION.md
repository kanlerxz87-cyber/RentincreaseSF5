# COORDINATION.md — shared task board

Repo: `kanlerxz87-cyber/RentincreaseSF5`
Session branch: `arena/9c07e651-rentincreasesf5`

## How to use this board

1. Claim a task by writing your session ID + file scope under it.
2. `git commit` and `git push` the claim **immediately**.
3. Edit only files in your claimed scope. If you must change a file owned by
   another session, log the request below instead of editing it.
4. Run `git pull --rebase` before every push.
5. When done: record sources used, verification performed, and irregularities,
   then set status to `done`.
6. Shared outputs (`data/*.json`, site `index.html`, navigation) are touched only
   by the final integration session.

> NOTE: This board follows the session's operating rules. Because this run is a
> single end-to-end session, the same session ID owns every task; scopes are
> still listed so any parallel session can see what is off-limits.

## Tasks

### T1 — Research: SF Rent Board license / Housing Inventory / fee
- **Status:** done
- **Owner (session):** 9c07e651 (this session)
- **Files:** `research/01-license-and-rent-board.md`
- **Sources:** sf.gov Rent Board Housing Inventory; Sec. 37.15; Rent Board Fee page;
  2027 Informational Notice; Learn about rent increases.
- **Verification:** each claim matched to the sf.gov page text (fetched 2026-11-07).

### T2 — Research: allowable increase amounts + banked increase math
- **Status:** done
- **Owner (session):** 9c07e651
- **Files:** `research/02-allowable-increases.md`, `data/allowable_increases.json`
- **Sources:** sf.gov Current Rates; Rent Board Form 571 (26-27); Banked rent increases page.
- **Verification:** Form 571 table transcribed line by line; arithmetic re-run in
  `tools/calc.py` and unit-tested against the Rent Board's own worked example
  ($1,000 base, 3.6% + 1.7% banked + 1.4% annual = 6.7% → $87.10).

### T3 — Research: state + federal layer (Costa-Hawkins, AB 1482, notice, fair housing)
- **Status:** done
- **Owner (session):** 9c07e651
- **Files:** `research/03-state-and-federal.md`
- **Sources:** leginfo Civil Code 827, 1947.12, 1954.53; HUD FHA overview;
  CA Civil Rights Dept housing page; sf.gov AB 1482 page.

### T4 — Unit ledgers + anonymization
- **Status:** done
- **Owner (session):** 9c07e651
- **Files:** `data/units.json`, `PRIVATE.md` (git-ignored, real tenant names/initials)
- **Verification:** every row carries a `source_url`; unconfirmed rows are
  `verified: false` and mirrored to the Flagged page.

### T5 — Site build (landing + category subpages + tables)
- **Status:** done
- **Owner (session):** 9c07e651
- **Files:** `docs/**`
- **Verification:** link check run over every `href` in `docs/`; see
  `tools/check_links.py`.

### T6 — Final integration, PR, merge, GitHub Pages deploy
- **Status:** done
- **Owner (session):** 9c07e651
- **Files:** `docs/**`, `COORDINATION.md`

## Irregularities / unverified items

See `docs/flagged.html` on the published site. Short list:

1. **Banking eligibility window conflict (12 vs 24 months).** sf.gov "Banked rent
   increases" says a skipped increase is only banked "if at least 24 full months
   pass without any rent increase", but the Rent Board's own worked examples on
   "Learn about rent increases in San Francisco" bank an increase after only 12
   months. Rent Board Rule 1.17 says "A full 12 months must have elapsed from the
   date that an annual rent increase ... could have been imposed before this
   banking section becomes applicable." Computed both ways for Unit B.
2. **Property type not confirmed.** If either unit is a single-family home or
   condominium, Costa-Hawkins removes the SF rent-increase cap (both tenancies
   began after Jan 1, 1996). User states both are rent-controlled; needs
   confirmation from the Property Information Map.
3. **No rent-increase history supplied for Unit B.** All banked-increase figures
   assume no prior increase since 6/1/2019.
4. **Rent Board fee vs. license.** sf.gov ties the license to Housing Inventory
   reporting (§37.15(e)); it does not say whether fee delinquency suspends the
   license. Flagged for Rent Board counselor.

## Handoff log

- 2026-11-07 — session 9c07e651 claimed T1–T6 (single-session run).
