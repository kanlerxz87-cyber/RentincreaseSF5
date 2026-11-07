# Rental Increase Research — San Francisco (Outer Sunset, ZIP 94122)

A source-linked research record and published dashboard about lawful rent increases for **two rent-controlled
units in a 1940 two-unit building** in San Francisco's Outer Sunset.

**Live site:** https://kanlerxz87-cyber.github.io/RentincreaseSF5/

---

## What the research answers

1. **Does an individual owner need to inform the Rent Board and obtain a licence before raising rent?**
   Yes to the licence, no to an application: every owner must report into the Rent Board **Housing Inventory**,
   which generates a **rent increase licence** that must be current on the effective date of the notice.
   No petition or approval is required for an ordinary annual or banked increase.
2. **What is a reasonable and normal increase?** The Rent Board's published annual allowance — **1.6%** for
   3/1/2026–2/28/2027, once every 12 months per tenancy, plus properly banked skipped years (added, never
   compounded, never rounded up).
3. **What is available to each unit?** Unit A: **3.0%** ($119.85 → $4,114.85) on its 2027-02-01 anniversary.
   Unit B: **13.1%** ($412.65 → $3,562.65) from seven skipped years.
4. **How should tenants be told, and can it survive a tenant-side review?** 30 days' notice (90 days above
   10%), with the dollar amount, percentage, effective date and the annual/banked split; see the fifteen-question
   stress test on the site.
5. **One unit or both?** The law does not require equal percentages; a documented, uniform method does the work
   that equal percentages are imagined to do.

## Repository layout

| Path | Purpose |
| --- | --- |
| `index.html` | Dashboard (published) |
| `pages/*.html` | Topic pages (published) |
| `assets/style.css` | Stylesheet (published) |
| `data/*.csv` | Machine-readable tables: sources, allowances, unit figures, flags |
| `tools/site_lib.py` | Layout, source register, citation helper |
| `tools/pages_1.py`, `tools/pages_2.py` | Page content |
| `tools/build_site.py` | Builds the site and runs the link + source checks |
| `COORDINATION.md` | Shared task board for agent sessions |
| `internal/notes.md` | Internal working notes (contains no personal data) |

## Rebuild

```bash
python3 tools/build_site.py
```

The build writes `index.html`, `pages/*.html`, `assets/style.css`, `data/*.csv`, and fails (non-zero exit) if any
internal link is broken or any table row lacks a source link or verification badge. GitHub Pages is configured to
publish from the repository root of `main`; `.nojekyll` makes it serve the HTML verbatim.

## Verification rules used

- Every table row links to the official page its value came from (SF.gov / Rent Board, California Legislative
  Information, California Civil Rights Department, U.S. HUD).
- Values are never inferred. If an official source could not confirm a value, the cell is **blank** and the gap
  appears on the *Flagged for review* page.
- Arithmetic is labelled **calculated** and shows the official percentages it derives from. It is not a Rent
  Board determination.

## Privacy

Tenant names, initials and addresses are **not** stored in this repository, in git history, or on the site.
The record uses `Tenant A1`, `Tenant A2`, `Tenant B1`, `Tenant B2`, `Unit A` and `Unit B`. Dates and dollar
amounts are preserved because the arithmetic depends on them.

## Not legal advice

This is a research record compiled for one owner from public official sources. The Rent Ordinance and Rent Board
rules change. The controlling text is on the official pages linked throughout the site. The Rent Board counsellor
line is 415-252-4600.
