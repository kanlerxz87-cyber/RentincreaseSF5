#!/usr/bin/env python3
"""Rent increase calculator for San Francisco rent-controlled units.

Implements, and only implements, rules that were read off official sources:

  * Rent Ordinance Sec. 37.3(a)(1)-(2)  - annual increase = 60% of CPI change, capped at 7%
  * Rent Ordinance Sec. 37.15(e)        - license required; no license => tenant need not pay
  * Rent Board Rule 4.12                - banking: a full 12 months must have elapsed
                                          banked increases are NOT compounded, NOT rounded up
  * Rent Board Rule 4.10(a)             - required contents of the rent increase notice
  * Civil Code 827(b)(2)-(3)            - 30 days if <=10%, 90 days if >10%; +5 days if mailed
  * Civil Code 1947.12(d)(3)            - AB 1482 cap does not apply where a lower local cap applies

Every percentage comes from data/allowable_increases.json, transcribed from Rent Board
Form 571. Nothing in this file invents a number.

Run:  python3 tools/calc.py        -> writes data/computed.json and runs self-tests
      python3 tools/calc.py --test -> self-tests only
"""

import json
import os
import sys
from datetime import date, timedelta
from decimal import Decimal, ROUND_DOWN

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "docs", "data")


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def d(s):
    """'YYYY-MM-DD' -> date"""
    y, m, day = (int(x) for x in s.split("-"))
    return date(y, m, day)


def add_months(start, months):
    """Anniversary arithmetic: same day-of-month, N months later."""
    m_index = start.month - 1 + months
    year = start.year + m_index // 12
    month = m_index % 12 + 1
    # clamp to last valid day (e.g. Feb 29 -> Feb 28)
    last_day = [31, 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28,
                31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]
    return date(year, month, min(start.day, last_day))


def money(x):
    """Truncate to the cent. Rule 4.12(a): banked increases 'shall not be rounded up'."""
    return float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_DOWN))


def fmt_money(x):
    return "${:,.2f}".format(x)


def fmt_pct(x):
    return "{:g}%".format(round(x, 4))


# --------------------------------------------------------------------------- #
# rate table
# --------------------------------------------------------------------------- #
class RateTable:
    def __init__(self, periods):
        self.periods = []
        for p in periods:
            if p.get("percent") is None:
                continue  # split 1992-93 period, not used for current tenancies
            self.periods.append((d(p["start"]), d(p["end"]), float(p["percent"])))
        self.periods.sort(key=lambda t: t[0])

    @property
    def horizon(self):
        """Last date covered by a published rate. The Rent Board publishes the next
        period's rate on or about January 1, effective March 1."""
        return max(end for _, end, _ in self.periods)

    def rate_on(self, when):
        """Published rate in effect on `when`, or None if not yet published.

        Returns None rather than guessing: an unpublished rate cannot be cited to an
        official source, so the site must show it blank and flag it.
        """
        for start, end, pct in self.periods:
            if start <= when <= end:
                return pct
        return None

    def period_label(self, when):
        for start, end, pct in self.periods:
            if start <= when <= end:
                return "{} - {}".format(start.isoformat(), end.isoformat())
        return "UNKNOWN"


# --------------------------------------------------------------------------- #
# core model
# --------------------------------------------------------------------------- #
def anniversary_schedule(tenancy_start, until):
    out = []
    i = 1
    while True:
        a = add_months(tenancy_start, 12 * i)
        if a > until:
            break
        out.append(a)
        i += 1
    return out


def banked_candidates(tenancy_start, effective, horizon=60):
    """Anniversary dates whose increase is eligible to be treated as 'banked'.

    Mirrors the Rent Board's own worked examples:
      * if the effective date IS an anniversary A(k), the current-year increase is A(k)
        and A(1)..A(k-1) are banked candidates;
      * if the effective date falls between A(k) and A(k+1) it becomes the new
        anniversary date, and A(1)..A(k) are banked candidates.
    """
    sched = anniversary_schedule(tenancy_start, effective)
    if not sched or effective < sched[0]:
        return [], None
    k = max(i for i, a in enumerate(sched) if a <= effective)
    on_anniversary = sched[k] == effective
    idx = k if on_anniversary else k + 1
    return sched[:idx], sched[k]


def compute_scenario(unit, rates, effective, banked_months_rule, only_most_recent=False,
                     annual_only=False):
    """Return a full scenario dict for one unit at one effective date."""
    start = d(unit["tenancy_start"])
    base = float(unit["current_base_rent"])
    if effective < add_months(start, 12):
        return None

    candidates, _ = banked_candidates(start, effective)
    if annual_only:
        banked_items = []
    else:
        eligible = [a for a in candidates
                    if add_months(a, banked_months_rule) <= effective]
        if only_most_recent and eligible:
            eligible = [eligible[-1]]
        banked_items = []
        for a in eligible:
            pct = rates.rate_on(a)
            banked_items.append({
                "anniversary": a.isoformat(),
                "percent": pct,
                "rate_period": rates.period_label(a),
                "source_url": "https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf",
            })

    annual_pct = rates.rate_on(effective)
    annual_published = annual_pct is not None
    annual_item = {
        "effective": effective.isoformat(),
        "percent": annual_pct,
        "published": annual_published,
        "rate_period": rates.period_label(effective) if annual_published else None,
        "note": None if annual_published else (
            "The Rent Board has not yet published the allowable increase for the period "
            "containing {}. The Board publishes it on or about January 1, effective March 1. "
            "Left blank deliberately - no official source exists for this figure yet."
        ).format(effective.isoformat()),
        "source_url": "https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf",
    }

    banked_pct = round(sum(b["percent"] for b in banked_items), 4)

    # Rule 4.12(a): banked increases are NOT compounded. Percentages are added and the
    # total is applied to the current base rent (Rent Board worked example: 3.6% + 1.7%
    # banked + 1.4% annual = 6.7% applied to the base rent).
    if annual_published:
        total_pct = round(annual_pct + banked_pct, 4)
        increase_amt = money(base * total_pct / 100.0)
        new_base = money(base + increase_amt)
    else:
        total_pct = None
        increase_amt = None
        new_base = None

    # Civil Code 827(b)(2)-(3).
    # When the total is not yet knowable (rate not published), reason from bounds:
    #   * if the banked component alone already exceeds 10%, 90 days is certain;
    #   * otherwise the annual component is capped at 7% by Sec. 37.3(a)(1), so if
    #     banked + 7% is still <= 10%, 30 days is certain.
    # Only if neither bound resolves it do we leave it blank.
    ANNUAL_STATUTORY_CAP = 7.0  # Sec. 37.3(a)(1)
    if total_pct is not None:
        days = 30 if total_pct <= 10.0 else 90
        reason = ("Civil Code 827(b)(2): increase is 10% or less -> 30 days" if days == 30
                  else "Civil Code 827(b)(3)(A): increase is greater than 10% -> 90 days")
    elif banked_pct > 10.0:
        days = 90
        reason = ("Civil Code 827(b)(3)(A): the banked component alone ({:g}%) is greater "
                  "than 10%, so 90 days is required whatever the annual component turns "
                  "out to be").format(banked_pct)
    elif banked_pct + ANNUAL_STATUTORY_CAP <= 10.0:
        days = 30
        reason = ("Civil Code 827(b)(2): banked component is {:g}% and the annual component "
                  "is capped at 7% by Sec. 37.3(a)(1), so the total cannot exceed 10% -> "
                  "30 days").format(banked_pct)
    else:
        days = None
        reason = ("Cannot be determined yet: the allowable increase for this period has not "
                  "been published, and the banked component sits in the range where either "
                  "30 or 90 days could apply.")
    return {
        "effective_date": effective.isoformat(),
        "base_rent": base,
        "banked_months_rule": banked_months_rule,
        "annual": annual_item,
        "banked": banked_items,
        "banked_percent": banked_pct,
        "total_percent": total_pct,
        "total_percent_published": total_pct is not None,
        "increase_amount": increase_amt,
        "new_base_rent": new_base,
        "notice_days_required": days,
        "notice_reason": reason,
        "serve_by_delivered": (effective - timedelta(days=days)).isoformat() if days else None,
        "serve_by_mailed": (effective - timedelta(days=days + 5)).isoformat() if days else None,
        "notice_source_url": "https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827.",
    }


def next_anniversary_on_or_after(start_md, analysis_date):
    """Next (month, day) anniversary strictly after the analysis date.

    Using the anniversary date keeps the existing anniversary intact; moving the date
    earlier can permanently forfeit a recently available annual increase.
    """
    m, day = start_md
    for year in range(analysis_date.year - 1, analysis_date.year + 3):
        last_day = [31, 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28,
                    31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1]
        cand = date(year, m, min(day, last_day))
        if cand > analysis_date:
            return cand
    raise RuntimeError("no future anniversary found")


# --------------------------------------------------------------------------- #
# self-tests against the Rent Board's own published examples
# --------------------------------------------------------------------------- #
def self_test(rates):
    checks = []

    def check(name, got, want):
        ok = abs(got - want) < 0.005
        checks.append({"check": name, "expected": want, "got": round(got, 4), "pass": ok})

    def check_eq(name, got, want):
        checks.append({"check": name, "expected": str(want), "got": str(got),
                       "pass": got == want})

    # Example: moved in 2023-06-01 @ $1,000; first increase 2026-06-01.
    u = {"tenancy_start": "2023-06-01", "current_base_rent": 1000.00}
    s = compute_scenario(u, rates, d("2026-06-01"), 12)
    check("Rent Board example: 2023-06-01 start, increase 2026-06-01, total %",
          s["total_percent"], 4.7)
    check("Rent Board example: same, increase amount", s["increase_amount"], 47.00)
    check("Rent Board example: same, new base rent", s["new_base_rent"], 1047.00)

    # Example: moved in 2022-08-01 @ $1,300; first increase 2025-08-01 (3.6% + 1.7% + 1.4%).
    u = {"tenancy_start": "2022-08-01", "current_base_rent": 1300.00}
    s = compute_scenario(u, rates, d("2025-08-01"), 12)
    check("Banked page example: 2022-08-01 start, increase 2025-08-01, total %",
          s["total_percent"], 6.7)
    check("Banked page example: same, increase amount", s["increase_amount"], 87.10)

    # Example: moved in 2025-06-01 @ $1,000; increase 2026-07-01 -> 1.6%, new anniversary.
    u = {"tenancy_start": "2025-06-01", "current_base_rent": 1000.00}
    s = compute_scenario(u, rates, d("2026-07-01"), 12)
    check("Rent Board example: 2025-06-01 start, increase 2026-07-01, total %",
          s["total_percent"], 1.6)
    check("Rent Board example: same, new base rent", s["new_base_rent"], 1016.00)

    # Notice thresholds (Civil Code 827)
    check("Notice: 3.0% increase -> 30 days",
          compute_scenario({"tenancy_start": "2025-02-01", "current_base_rent": 3995.00},
                           rates, d("2027-02-01"), 12)["notice_days_required"], 30)
    check("Notice: banked component alone >10% at 2027-06-01 -> 90 days",
          compute_scenario({"tenancy_start": "2019-06-01", "current_base_rent": 3150.00},
                           rates, d("2027-06-01"), 12)["notice_days_required"], 90)

    # Rate table spot checks against Form 571 / Current Rates
    check("Rate on 2027-02-01 (Unit A next anniversary)", rates.rate_on(d("2027-02-01")), 1.6)
    check("Rate on 2026-02-01 (Unit A skipped anniversary)", rates.rate_on(d("2026-02-01")), 1.4)
    # Unit B's first anniversary is 2020-06-01, which falls in the 3/1/2020-2/28/2021
    # period (1.8%). The 2.6% rate for 3/1/2019-2/29/2020 expired before the tenancy's
    # first increase eligibility date, so it is never available to this tenancy.
    check("Rate on 2020-06-01 (Unit B first anniversary)", rates.rate_on(d("2020-06-01")), 1.8)
    check("Rate on 2026-11-07 (analysis date)", rates.rate_on(d("2026-11-07")), 1.6)

    # A rate that does not exist yet must come back as None, never as a guess.
    check_eq("Rate on 2027-06-01 is NOT published yet -> None",
             rates.rate_on(d("2027-06-01")), None)
    check_eq("Publication horizon is 2027-02-28", rates.horizon.isoformat(), "2027-02-28")

    # Banked percentages for Unit B under Rule 4.12 (verified against Form 571 line by line)
    b12 = compute_scenario({"tenancy_start": "2019-06-01", "current_base_rent": 3150.00},
                           rates, d("2027-06-01"), 12)
    check("Unit B banked total under Rule 4.12 (12-month test)", b12["banked_percent"], 13.1)
    b24 = compute_scenario({"tenancy_start": "2019-06-01", "current_base_rent": 3150.00},
                           rates, d("2027-06-01"), 24)
    check("Unit B banked total under the 24-month reading", b24["banked_percent"], 11.5)
    # Unit B banked years, verified line by line against Form 571:
    #   2020 1.8 + 2021 0.7 + 2022 2.3 + 2023 3.6 + 2024 1.7 + 2025 1.4 + 2026 1.6
    check_eq("Unit B banked year-by-year rates",
             [b["percent"] for b in b12["banked"]],
             [1.8, 0.7, 2.3, 3.6, 1.7, 1.4, 1.6])
    a12 = compute_scenario({"tenancy_start": "2025-02-01", "current_base_rent": 3995.00},
                           rates, d("2027-02-01"), 12)
    check("Unit A total under Rule 4.12 (1.4% banked + 1.6% annual)", a12["total_percent"], 3.0)
    check("Unit A increase amount", a12["increase_amount"], 119.85)
    check("Unit A new base rent", a12["new_base_rent"], 4114.85)

    return checks


# --------------------------------------------------------------------------- #
def main():
    with open(os.path.join(DATA, "allowable_increases.json")) as f:
        ai = json.load(f)
    with open(os.path.join(DATA, "units.json")) as f:
        units = json.load(f)

    rates = RateTable(ai["periods"])
    checks = self_test(rates)

    failed = [c for c in checks if not c["pass"]]
    if failed:
        print("SELF-TEST FAILURES:")
        for c in failed:
            print("  ", c)
        if "--test" in sys.argv:
            sys.exit(1)

    analysis = d(units["meta"]["analysis_date"])
    for c in checks:
        print("{:6}  {:62}  expected {:>8}  got {:>8}".format(
            "PASS" if c["pass"] else "FAIL", c["check"][:62], c["expected"], c["got"]))

    out = {
        "generated": analysis.isoformat(),
        "self_tests": checks,
        "self_tests_passed": len(checks) - len(failed),
        "self_tests_total": len(checks),
        "units": [],
    }

    for u in units["units"]:
        start = d(u["tenancy_start"])
        eff = next_anniversary_on_or_after((u["anniversary_month"], u["anniversary_day"]), analysis)
        scenarios = []
        labels = [
            ("conservative", "Current-year annual increase only", dict(annual_only=True)),
            ("moderate", "Current-year annual increase + the most recent banked year",
             dict(only_most_recent=True)),
            ("maximum_rule_4_12", "Maximum lawful under Rule 4.12 (12-month banking test)", dict()),
        ]
        for key, label, kw in labels:
            s = compute_scenario(u, rates, eff, 12, **kw)
            s["key"] = key
            s["label"] = label
            scenarios.append(s)

        # Alternative reading published on the sf.gov "Banked rent increases" page.
        alt = compute_scenario(u, rates, eff, 24)
        alt["key"] = "maximum_24_month_reading"
        alt["label"] = ("Conservative lower bound - the most restrictive reading possible "
                        "(24 months measured from each skipped anniversary). Not stated in "
                        "any official source; shown only as a floor.")
        scenarios.append(alt)

        sched = anniversary_schedule(start, eff)
        out["units"].append({
            "unit_id": u["unit_id"],
            "public_label": u["public_label"],
            "tenancy_start": u["tenancy_start"],
            "current_base_rent": u["current_base_rent"],
            "anniversary_date": "{:02d}/{:02d}".format(u["anniversary_month"], u["anniversary_day"]),
            "next_effective_date": eff.isoformat(),
            "anniversary_schedule": [a.isoformat() for a in sched],
            "scenarios": scenarios,
        })

    with open(os.path.join(DATA, "computed.json"), "w") as f:
        json.dump(out, f, indent=2)
    print("\nWrote data/computed.json  ({}/{} self-tests passed)".format(
        out["self_tests_passed"], out["self_tests_total"]))
    def show(v, fn):
        return "-" if v is None else fn(v)

    for u in out["units"]:
        print("\n{}  base {}  next anniversary {}".format(
            u["public_label"], fmt_money(u["current_base_rent"]), u["next_effective_date"]))
        for s in u["scenarios"]:
            print("   {:26} total {:>7}  +{:>9}  -> {:>9}   notice {} days, serve by {}".format(
                s["key"], show(s["total_percent"], fmt_pct),
                show(s["increase_amount"], fmt_money),
                show(s["new_base_rent"], fmt_money),
                s["notice_days_required"], s["serve_by_delivered"]))

    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
