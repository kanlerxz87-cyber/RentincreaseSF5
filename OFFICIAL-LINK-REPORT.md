# Official-source link health — spot check

Checked 7 November 2026 by `arena/9c25de43-rentincreasesf5`. This is a **partial** link/content availability review, not a claim that every citation supports every claim or that the whole site is verified. The sandbox cannot directly connect to government websites; pages were retrieved using the research retrieval tool. The URL inventory contains 65 distinct external URLs in the root, `pages/`, and `dashboard/` HTML; mirrored `site/` copies are excluded. Not all 65 have been checked in this session. A successful retrieval does not guarantee future availability or legal accuracy.

## Retrieved official sources

| Source and manual review link | Result of spot check |
| --- | --- |
| [SF Housing Inventory](https://www.sf.gov/rent-board-housing-inventory) | Retrieved; confirms annual reporting and current license before an annual or banked increase goes into effect. |
| [SF rent increases](https://www.sf.gov/learn-about-rent-increases-san-francisco) | Retrieved; states 1.6% for March 1, 2026–February 28, 2027. |
| [SF Form 571](https://www.sf.gov/documents/34344/571_Allowable_Annual_Increases_26-27_1.pdf) | PDF retrieved; current and prior rates shown. |
| [SF §37.15](https://www.sf.gov/information/sec-3715-reporting-obligations-licensing) | Retrieved; reporting and licensing text. |
| [SF §37.3](https://www.sf.gov/information/sec-373-rent-limitations) | Retrieved; annual and banking provisions. |
| [SF banked increases](https://www.sf.gov/information/banked-rent-increases) | Retrieved after redirect; the 24-month statement and example warrant careful review alongside the ordinance. |
| [SF Part IV rules](https://www.sf.gov/reports/february-2024/rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring) | Retrieved after redirect; contains Rule 4.10. |
| [CA Civil Code §827](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=CIV&sectionNum=827) | Retrieved; notice rules. |
| [SF AB 1482](https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482/) | Retrieved; explains exclusion for units covered by local rent increase limits. |
| [SF Rent Board fee](https://www.sf.gov/rent-board-fee) | Retrieved; fee distinct from Housing Inventory reporting. |
| [SF Chapter 37A fee PDF](https://api.sf.gov/documents/7835/901_Rent_Board_Fee_Ch._37ARe.pdf) | Retrieved on retry after initial tool failure; redirects to media.api.sf.gov. Initial failure is not evidence the link is broken. |
| [SF Rent Board counselor](https://www.sf.gov/speak-rent-board-counselor/) | Retrieved; counseling is free but is not legal advice. |
| [SF tenant summary petition](https://www.sf.gov/file/518-tenant-summary-petition-fillable-224pdf) | PDF retrieved; tenant summary-petition form. |
| [HUD fair housing](https://www.hud.gov/helping-americans/fair-housing-act-overview) | Retrieved; federal protected classes. |

Additional Rent Board pages retrieved: coverage, multi-year increases, tenant summary petitions, algorithmic-device rules, additional occupants, index, coverage exemptions, failure-to-repair petitions, Rule 6.14/Costa-Hawkins determination, tenant harassment, landlord petitions, the forms center, and tenant unlawful-increase petitions. Their retrieval is not a full validation of the statements citing them.

## Findings and handoff

1. **Outdated source edition — review requested.** Dashboard source S09 references the [June 2023 Rent Ordinance compilation](https://www.sf.gov/sites/default/files/2023-07/600%20Ordinance%206-2-23.pdf). That PDF is reachable but historical. The [Rent Board ordinance page](https://www.sf.gov/reports--rent-ordinance/) points to its [November 2, 2026 compilation](https://www.sf.gov/documents/65403/600_Ordinance_11-02-26_2.pdf). The Rent Board says its compilation is for convenience, not the official record, and links the official publisher. Re-check any claims relying on the older PDF against current law. This does not by itself establish that the specific cited rules changed.
2. **Landing page unresolved publication tokens.** The current root `index.html` contains literal `CURRENT_PERIOD`, `A_DOLLAR`, `A_BASE`, `B_DOLLAR`, and `B_BASE`. This is a publication defect, not a source-link error. It was independently identified in active PR #7; a change request was posted there and on PR #5. Do not represent the landing page as fully verified while unresolved.
3. **Some checks remain incomplete.** Government hosts cannot be reached directly from this sandbox. Fetch-tool checks were sampled, and another active session is investigating row-level, privacy, and publication defects. Do not treat local-link tests or HTTP status alone as proof of source accuracy.

## Reproducible inventory

`python3 tools/official_link_health.py` lists external links and the published files in which they occur. `python3 tools/official_link_health.py --self-test` checks two query-string parsing cases. `--check` makes live GET requests from a network-enabled machine; it reports failures as requiring review and cannot detect a soft-404 page, verify claims, or prove future availability. It must not be interpreted as an exhaustive legal audit.
