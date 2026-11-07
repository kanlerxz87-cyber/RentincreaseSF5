# Per-Unit Analysis — Allowable Rent Increases

Prepared: 2026-11-07 · Session `6f06d5b3-rentincreasesf5`
Method: every percentage below comes from the official Rent Board announcements registered in
[data/sources.md](sources.md) (S1–S8). Amounts are computed as `base rent × total %`, **rounded to the
cent, never rounded up** (official rule, S1). All figures are **base rent** only (parking/services included
in base rent; passthroughs excluded).

The allowable total for an increase = **annual rate in effect on the effective date** + **banked rates**
from each prior year in which the increase was not imposed and a full 12 months has elapsed (official
worked example in S1: 1.7% + 1.4% banked + 1.6% annual = 4.7% total).

Official annual rates used:

| Period (effective) | Rate | Source |
|---|---|---|
| 2019-03-01 – 2020-02-29 | 2.6% | S8 |
| 2020-03-01 – 2021-02-28 | 1.8% | S7 |
| 2021-03-01 – 2022-02-28 | 0.7% | S6 |
| 2022-03-01 – 2023-02-28 | 2.3% | S5 |
| 2023-03-01 – 2024-02-29 | 3.6% | S5 |
| 2024-03-01 – 2025-02-28 | 1.7% | S4 |
| 2025-03-01 – 2026-02-28 | 1.4% | S3 |
| 2026-03-01 – 2027-02-28 | 1.6% | S2 / S1 |

---

## Unit 2 (Tenants U2-A, U2-B) — anniversary date June 1

Facts (owner-provided): lease start **2019-06-01** at **$3,150/month**; **no increases documented since**
(flag F-02 — verify against payment records). Anniversary date: **June 1** (S1: first increase 12 months
after lease start; every increase resets it to the effective date).

Banked rates available for an increase effective **2026-06-01** (each skipped a full year; all 12-month
availability windows elapsed by 2026-06-01):

| Anniversary skipped | Rate | Status |
|---|---|---|
| 2020-06-01 | 2.6% | banked |
| 2021-06-01 | 1.8% | banked |
| 2022-06-01 | 0.7% | banked |
| 2023-06-01 | 2.3% | banked |
| 2024-06-01 | 1.7% | banked |
| 2025-06-01 | 1.4% | banked (12 months elapsed exactly on 2026-06-01) |
| 2026-06-01 | 1.6% | current annual |

**Option A — full banked + annual (effective 2026-06-01):** total 2.6+1.8+0.7+2.3+1.7+1.4+1.6 = **12.1%**
- Increase: $3,150 × 0.121 = **$381.15**
- New base rent: **$3,531.15**
- Notice: **90 days** (>10% cumulative in 12 months, S1/S15) → serve by **2026-03-03** (by 2026-02-27 if mailed)
- Notice must identify which portion is banked and from which years (flag F-12; see S1 banking guidance)

**Option B — annual only (effective 2026-06-01):** total **1.6%**
- Increase: $3,150 × 0.016 = **$50.40**
- New base rent: **$3,200.40**
- Notice: **30 days** → serve by **2026-05-02** (by 2026-04-26 if mailed)
- The remaining 10.5% stays banked for later

No increase may be imposed before **2026-06-01** (12-month rule, S1). The next cycle (2027-06-01) adds the
2026-27 rate (1.6%) to the bank if not used.

---

## Unit 1 (Tenants U1-A, U1-D) — anniversary date depends on rent history

Facts (owner-provided): **last lease start 2025-02-01 at $3,995**; initial-lease tenants were U1-A, U1-B,
U1-C; U1-B/U1-C vacated and U1-D moved in (dates undocumented — flag F-03); **continuing tenancy from
2026-04-01 at the same $3,995**. Because U1-A (an initial tenant) remained, this is a **continuing
tenancy** — no unrestricted "initial rent" reset was permitted at the 2025-02-01 lease (S1, S16; flag F-03).

**The pre-2025-02-01 rent is not documented (flag F-01), so two scenarios are shown.**

### Scenario 1 — the 2025-02-01 lease set/increased rent to $3,995 (anniversary date = 2025-02-01)
- Next increase no earlier than **2026-02-01**.
- Effective 2026-02-01 – 2026-02-28: rate in effect = **1.4%** (2025-26 period, S3)
  - Increase $3,995 × 0.014 = **$55.93** → new base rent **$4,050.93**; 30-day notice (serve by 2026-01-01).
- Effective **2026-03-01** (or any date after): rate in effect = **1.6%** (S2/S1) + **1.4% banked** (2026-02-01 skipped; 12 months elapsed) = **3.0%**
  - Increase $3,995 × 0.030 = **$119.85** → new base rent **$4,114.85**; 30-day notice (≤10%).
- The 2025-02-01 increase itself must have been lawful (license in force, proper notice, ≤ cap then in effect: 1.7% for 2024-25 + any banked) — flag F-11.

### Scenario 2 — rent was already $3,995 before 2025-02-01 (no increase on 2025-02-01)
- Anniversary date = the date of the **last actual increase — unknown**.
- Upper-bound bank (if no increase since before 2019-03-01): 2.6+1.8+0.7+2.3+3.6+1.7+1.4 = **14.1% banked** + 1.6% current = **15.7%**
  - Increase $3,995 × 0.157 = **$627.22** → new base rent **$4,622.22**; **90-day notice** (>10%).
- The true figure is **1.6% + (sum of rates for each skipped year since the last actual increase)** —
  cannot be computed without the rent ledger (flag F-01).

### What both scenarios share
- Increase must be on base rent only; no rounding up (S1).
- No charge for Tenant U1-D's presence as an "additional occupant" (S1).
- License must be current on the effective date (S1, S9); 30/90-day written notice (S1, S15).

---

## "Reasonable and normal" — summary answer

- For both units, the **lawful maximum** is the only defensible benchmark: **1.6%** (2026-27) plus
  documented banked increases. Anything at or below that, properly noticed and licensed, is within the
  range that a tenant-side review would treat as normal business practice (findings F-A01, F-D02, F-C01/02).
- Market-rate comparisons (non-official) are NOT used in any table on this site, per the verification rule.
