# Research: allowable increases and banked-increase arithmetic

## The single number

**1.6% for March 1, 2026 – February 28, 2027.**

- https://www.sf.gov/reports--current-rates-including-rent-increase-relocation-sec-deposit
- https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf

Formula: 60% of the increase in the Bay Area CPI-U, rounded to the nearest tenth, capped
at 7% (§37.3(a)(1), https://www.sf.gov/information/sec-373-rent-limitations).

**Note on how 1.6% was derived.** The Rules were amended effective 1/13/26:
"Provides a methodology for approximating the missing October 2025 CPI caused by the
federal government shutdown and deletes city names other than San Francisco from the
Consumer Price Index region."
— https://www.sf.gov/documents/36249/625_RR_Complete_1-13-26.pdf

## Mechanics that matter

| Rule | Source |
|---|---|
| Once every 12 months; first increase 12 months after the lease began | https://www.sf.gov/learn-about-rent-increases-san-francisco/ |
| Calculated on **base rent only**, which includes housing services (parking, storage) but excludes temporary passthroughs | same |
| Rent increases **cannot be rounded up** | same |
| Use the percentage in effect on the **effective date**, not the date of service | same |
| Banked increases are **added, not compounded**, and are **not rounded up** | Rule 4.12(a) |
| Banking only for increases first available on/after **April 1, 1982** | Rule 4.12(a) |
| "There is no limit on how much can be banked" | https://sf.gov/information/banked-rent-increases |
| Banked increases do not expire during a tenancy; they do **not** carry over to a new tenant | same |
| Taking only part of an increase banks the remainder | same |

## The banking conflict (flagged)

| Source | Test |
|---|---|
| Rule 4.12(a) (the regulation) | "A full **12** months must have elapsed…" |
| sf.gov "Banked rent increases" page | "at least **24** full months pass without any rent increase" |
| Rent Board's own worked examples | consistent with the **12**-month test |

The engine uses Rule 4.12. For Unit A the two readings agree (24 months have elapsed).
For Unit B they do not: 13.1% vs 11.5%.

## Worked example used as a regression test

Rent Board example: tenant moved in 2023-06-01 at $1,000; first increase 2026-06-01.

    3.6% (2024)  ... no — 2024-06-01 is 1.7%
    banked = 1.7% (2024-06-01) + 1.4% (2025-06-01) = 3.1%
    annual = 1.6% (2026-06-01)
    total  = 4.7%  ->  $1,000 x .047 = $47.00  ->  new base $1,047.00

Reproduced exactly by `tools/calc.py`; test output is on the Sources page.

## Error caught by the self-tests

My first hand calculation gave Unit B a banked total of 14.1% by including the 2.6%
rate for 3/1/2019–2/29/2020. That is wrong: Unit B's tenancy began 2019-06-01, so its
first increase eligibility date was **2020-06-01**, which falls in the 3/1/2020–2/28/2021
period (1.8%). The 2.6% period expired before the tenancy was ever eligible for an
increase. Correct banked chain:

    1.8 + 0.7 + 2.3 + 3.6 + 1.7 + 1.4 + 1.6 = 13.1%

## Unpublished figure

The Rent Board has not published the rate for the period containing **June 1, 2027**
(Unit B's next anniversary). It publishes on or about January 1, effective March 1. The
field is rendered blank everywhere and routed to the Flagged page. No estimate is
printed, including in the notice-period logic — but the notice period is still
determinable because §37.3(a)(1) caps the annual component at 7%.
