# Independent evidence register

Session `a872cd08` · scope `evidence/**` · checked **2026-11-07 (UTC)** · research, not legal advice.

This folder is an independent fact-check of the rent-increase research for a rent-controlled two-unit property in San Francisco (94122). It has three jobs:

1. **Register** every finding with a verbatim excerpt and a link to an official source.
2. **Recompute** the unit arithmetic and notice deadlines by script, and test the banking model against the Rent Board's own worked examples.
3. **Audit** the pages other sessions published, and log requested corrections (it never edits their files).

Open `index.html` first (overview, step-by-step Rent Board process, corrections, flagged items), then `register.html` and `calculations.html`.

## Files

| File | What it is |
| --- | --- |
| `index.html` | Overview: bottom line, Rent Board process step by step, corrections requested, **Flagged for review**, method |
| `register.html` / `register.csv` | Every finding: id, category, finding, value, status, official `source_url`, `verified_at`, notes, verbatim `excerpt`, source title/publisher/type, `owner_reported_value` |
| `calculations.html` / `calculations.csv` | Scenario arithmetic (`calculated`), banking schedules, model test, the full rate table |
| `allowable_increases_official.csv` | Rent Board Form 571: all 46 published periods (1982 to 2027) |
| `audit-findings.csv` | Published claim vs official evidence vs requested fix, with severity and file owner |
| `tools/data.py` | The source rows (plain text tables) |
| `tools/build_evidence.py` | Builds everything above and runs the checks |

## Status legend

| Status | Meaning |
| --- | --- |
| `verified` | The linked official page states it. `excerpt` is copied word for word (an ellipsis marks omitted words). |
| `unverified` | **Not confirmed.** `value` is blank on purpose. `source_url` is the official place that was checked. Listed under *Flagged for review*. |
| `owner-reported` | Supplied by the owner, cannot be checked against public official data. `value` is blank; the supplied figure sits in `owner_reported_value`. |
| `calculated` | Arithmetic computed by script from verified rates and owner-reported inputs. Not a Rent Board determination. |

Nothing is inferred or filled in. A claim about an absence (for example "no federal rent cap") is `unverified` unless an official page says it.

## Official-source allowlist

Only these hosts are cited as verification: `www.sf.gov` / `sf.gov` (Rent Board and City pages), `sfgov.legistar.com` (Board of Supervisors records), `leginfo.legislature.ca.gov` (California statutes), `calcivilrights.ca.gov`, `www.hud.gov`, `sftreasurer.org`, `portal.sfrb.org` (Rent Board portal), `www.justice.gov` and `www.sec.gov` (checked for corporate-practice claims; nothing was confirmed there). News sites, law-firm summaries, aggregators and commercial rent sites are never cited as verification. The builder fails if a register link is not `https` on this list.

## Checks run by the builder

```
python3 evidence/tools/build_evidence.py      # Python 3.9+, standard library only
```

* schema, unique ids, status vocabulary; verified rows need a value and an excerpt; unverified and owner-reported rows must have a blank value
* every register link is `https` on the allowlist; every table row in the HTML has `data-row-id` and an https link
* the rate table is contiguous from 4/1/1982 and has 46 rows
* the banking model (Rent Board Rule 4.12(a)) reproduces **all four** of the Rent Board's published worked examples; a looser reading of the "24 months" sentence fails one of them
* if `data/allowable-increases.csv` and `data/allowance-ledger.csv` are present, they are compared with Form 571

## What this register could not confirm (all flagged)

Housing Inventory and license status for the two units; actual rent history; the building facts behind coverage; whether the notice itself is ever filed; the 2027-28 annual percentage; HUD fair-market rent; DOJ and SEC material on corporate landlords; the Mayor's September 2026 "rent emergency" and whether Penal Code 396 applies; the reported annual-reminder ordinance. See the *Flagged for review* table.

## Privacy

No tenant names, initials, exact address or parcel number appear here. Units are "Unit 1" and "Unit 2" (the `pages/` set calls them Unit A and Unit B). Dates and amounts are exactly as supplied by the owner. Leak checks with real identifiers are typed into a shell by hand and never written to a file.

## Corrections to other sessions' pages

Requests, with exact replacement text, are logged in `COORDINATION.md` (Session a872cd08 section) and tabulated in `audit-findings.csv`. Highest priority: the pending banked-rent cap is **File #261020**, not "261015"; the "12 vs 24 months" banking conflict is not a conflict; `internal/notes.md` is publicly served.
