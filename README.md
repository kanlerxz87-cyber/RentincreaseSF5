# SF Rent Review — rental increase research dashboard

Privacy-safe, official-source research on lawful rent increases for **two rent-controlled units in a 1940
two-unit building** in San Francisco's Outer Sunset (ZIP 94122).

**Public site:** https://kanlerxz87-cyber.github.io/RentincreaseSF5/

Two independently compiled research sets are published here and linked from the home page:

| Set | Pages | Character |
| --- | --- | --- |
| Deep dive (`pages/`) | executive summary, Rent Board process, units & numbers, allowed increases, local/state/federal law, notices, owner playbook, tenant-lawyer test, source register, flagged for review | Computes unit-specific figures from the owner's records and labels every result `calculated` |
| Earlier compilation (root) | `process.html`, `amounts.html`, `protections.html`, `flagged.html`, `sources.html` | Deliberately declines to assert unit-specific figures; assertions limited to verified rules |

Both sets are source-linked to official pages. Where they differ, the difference is one of approach, not of law.

## The question the research answers first

*Does an individual owner need to tell the Rent Board and apply for a licence before notifying tenants of a rent
increase?* **Licence yes, application no.** Every owner — individual or corporate — must report into the Rent
Board Housing Inventory; that generates a rent increase licence for a tenant-occupied unit, which must be current
on the effective date of the notice or the increase is not enforceable (S.F. Admin Code §37.15(e)). No petition or
approval is needed for an ordinary annual or banked increase (§37.3(a)(1)–(2); the Rent Board's 571 rate sheet
states it may be imposed "without filing a petition"). Only six special increase types require a petition filed
before notice.

## Numbers (arithmetic on owner-supplied base rents; not a Rent Board determination)

| Unit | Tenancy from | Base rent | Available | Increase | New base | Notice |
| --- | --- | --- | --- | --- | --- | --- |
| A | 2025-02-01 | $3,995.00 | 1.4% + 1.6% = **3.0%** | $119.85 | $4,114.85 | 30 days |
| B | 2019-06-01 | $3,150.00 | 1.8+0.7+2.3+3.6+1.7+1.4+1.6 = **13.1%** | $412.65 | $3,562.65 | 90 days |

## Build and validate

Requires Python 3, no packages or external assets:

```
python3 scripts/build.py             # earlier 6 pages, then the 11-page set and the consolidated hub
python3 scripts/check.py             # local links, official-source allowlist, every data row sourced, headings
python3 scripts/independent_audit.py # root/site parity, landmarks, identifier exclusion
python3 tools/build_site.py          # link + source-coverage check for the pages/ set
python3 -m http.server 8000 --bind 0.0.0.0   # preview from the repository root
```

Generated HTML is written to the repository root (GitHub Pages publishes `main:/`) and mirrored into `site/`.
`.nojekyll` keeps Pages from processing the files.

## Repository layout

| Path | Purpose |
| --- | --- |
| `index.html` | Consolidated hub (generated) |
| `pages/*.html`, `assets/style.css`, `data/*.csv` | Deep-dive set, its stylesheet and machine-readable tables |
| `process.html`, `amounts.html`, `protections.html`, `flagged.html`, `sources.html`, `style.css` | Earlier published set (unchanged) |
| `site/` | Mirror of the published root, used by the validation scripts |
| `tools/` | Generator for the deep-dive set (`site_lib.py`, `pages_1.py`, `pages_2.py`, `build_site.py`) |
| `scripts/` | Earlier set's generator, checks and independent audit |
| `COORDINATION.md` | Shared task board, source list and reconciliation log |

## Verification rules

- Every table row links the official page its value came from (SF.gov / Rent Board, California Legislative
  Information, California Civil Rights Department, U.S. HUD).
- Values are never inferred. If an official source could not confirm a value, the cell is blank and the gap is
  listed on the *Flagged for review* page.
- Arithmetic is labelled `calculated` and shows the official percentages it derives from.
- Research date: **7 November 2026**. Statutes, rules and rates change; re-check before acting.

## Privacy

No tenant names, initials, addresses, parcel numbers or personal documents are stored in this repository, its
history or the site. The record uses `Tenant A1`, `Tenant A2`, `Tenant B1`, `Tenant B2`, `Unit A` and `Unit B`.
Dates and dollar amounts are preserved because the arithmetic depends on them. Housing Inventory submissions are
public and made under penalty of perjury — use truthful data in the official Rent Board portal, never placeholders.

## Not legal advice

Research only. No licence was obtained, no inventory report filed, and no notice served or approved by this
repository. Recommendations and hypothetical arithmetic are not official determinations. The controlling text is
on the official pages linked throughout; the Rent Board counsellor line is 415-252-4600.
