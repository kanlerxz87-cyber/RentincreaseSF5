# RentincreaseSF5 — San Francisco rent increase research

Research dashboard for a two-unit rent-controlled property in the Outer Sunset
(ZIP 94122), compiled from official government sources.

**Live site:** https://kanlerxz87-cyber.github.io/RentincreaseSF5/

## The headline finding

San Francisco Administrative Code **§37.15** requires every owner of a residential
dwelling unit to report into the Rent Board Housing Inventory annually. A landlord who
has substantially complied receives a **license to impose rent increases**; without one,
the increase is unenforceable and the Rent Board states that "some rent increases given
without a license will be null and void."

**Being an individual owner rather than a corporation makes no difference.** §37.15 says
"owners of residential dwelling units subject to this Chapter 37" — there is no size
threshold and no incorporation test.

You do **not** file a petition or seek approval for an ordinary annual or banked
increase. You do need the license, and you do need to pay the annual Rent Board fee
(separate obligation).

## Layout

```
data/
  sources.json            registry of official sources, keyed and cited site-wide
  allowable_increases.json  Form 571 history, transcribed line by line
  units.json              anonymized unit facts
  computed.json           generated: scenarios, notice deadlines
  link_status.json        fetch evidence for every cited URL
tools/
  calc.py                 calculator + 21 self-tests against Rent Board examples
  site_shell.py           layout, navigation, CSS
  build_site.py           renders docs/ from data/
  check_links.py          link + citation integrity check
research/                 line-by-line research notes with citations
docs/                     the published static site (GitHub Pages source)
COORDINATION.md           shared task board
PRIVATE.md                git-ignored — real tenant identities, never published
```

## Rebuilding

```bash
python3 tools/calc.py          # recompute + run self-tests
python3 tools/build_site.py    # regenerate docs/
python3 tools/check_links.py   # verify links and citations
```

`check_links.py` exits non-zero on any broken internal link, any external URL missing
from the source registry, or any registry entry missing a recorded fetch.

## Rules this project follows

- Every table row cites an official government source.
- Nothing is inferred. Where the Rent Board has not published a figure (Unit B's rate
  for the period containing June 1, 2027), the field is rendered **blank** and routed to
  the Flagged for Review page.
- Conflicts between official sources are published, not resolved silently — see the
  banking 12-month vs 24-month conflict.
- Tenant names and initials are anonymized. Dates and dollar amounts are unchanged.

## Not legal advice

Compiled from public government sources. San Francisco Rent Board counseling:
415-252-4600, weekdays 9am–12pm and 1–4pm.
