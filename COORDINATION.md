# COORDINATION — Shared Task Board

This file is the shared task board for all agent sessions working in this repository.
Protocol: claim a task by adding your session ID and file scope below, **commit and push the
claim immediately**, never start a task another session has claimed, keep scopes non-overlapping,
run `git pull --rebase` before every push, make small frequent commits, and log every handoff,
conflict, and completion here. Marking anything "verified" requires checking it against an official
source with a linked URL.

## Sessions

| Session ID | Branch | Notes |
|---|---|---|
| `6f06d5b3-rentincreasesf5` | `arena/6f06d5b3-rentincreasesf5` | Owner-directed session. Sole session active so far; **also designated final integration session** (merges data, re-verifies line by line, publishes site, opens & merges PR to `main`). |

## Task Board

| ID | Task | Status | Owner (session ID) | File scope |
|---|---|---|---|---|
| T1 | Research & verify SF rent-increase rules (local/state/federal) from official sources; build per-row sourced findings table | claimed → in progress | `6f06d5b3-rentincreasesf5` | `data/findings.csv`, `data/sources.md` |
| T2 | Unit & tenancy data (anonymized; dates/amounts unchanged) + allowed-increase analysis per unit | claimed → in progress | `6f06d5b3-rentincreasesf5` | `data/units.csv`, `data/analysis.md` |
| T3 | Executive summary (license/notice question front and center, step-by-step, official links) | claimed → in progress | `6f06d5b3-rentincreasesf5` | `pages/executive-summary.html`, `pages/process.html` |
| T4 | Site build: landing dashboard + subpages (rules, units, practice, legal, flagged) | claimed → in progress | `6f06d5b3-rentincreasesf5` | `index.html`, `css/style.css`, `pages/*.html`, `data/flagged.csv` |
| T5 | Final integration: re-verify combined data line by line, broken-link check, PR to main, merge, confirm Pages deploy | claimed → in progress | `6f06d5b3-rentincreasesf5` | repo-wide read-only review + this file |

Shared outputs (table data, site index & navigation) are touched **only** by the final integration
session (T5) — here, the same sole session, which is noted in the log.

## Log

- 2026-11-07 — Session `6f06d5b3-rentincreasesf5` started. Repo surveyed: initial commit only
  (`README.md`). GitHub Pages already enabled: public, source = `main` branch, path `/`,
  URL `https://kanlerxz87-cyber.github.io/RentincreaseSF5/`. Claimed T1–T5 (pushing this claim now).
  Anonymization policy: real tenant initials are **never written in this repo or site**; placeholder
  IDs (e.g., `U1-TA`) are used; dates and dollar amounts are kept unchanged. The placeholder→identity
  mapping is held by the property owner only and is intentionally not stored in the repo.

## Open Requests to Other Sessions

None (sole session).
