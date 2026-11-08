from pathlib import Path
from html import escape as e
import json
S={
'inventory':('Housing Inventory & licensing','https://www.sf.gov/rent-board-housing-inventory'),
'increase':('SF annual increases & notice','https://www.sf.gov/learn-about-rent-increases-san-francisco'),
'coverage':('SF rental-law coverage','https://www.sf.gov/learn-about-san-francisco-rental-laws/'),
'notice':('Civil Code §827','https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=827.&lawCode=CIV'),
'rules':('Rent Board Rule 4.10','https://www.sf.gov/reports--december-2022--rent-board-rules-and-regulations-part-iv-rent-increases-not-requiring'),
'state':('SF guidance on AB 1482','https://www.sf.gov/reports--california-tenant-protection-act-2019-ab-1482'),
'crd':('California Civil Rights Department','https://calcivilrights.ca.gov/housing/'),
'retaliation':('Civil Code §1942.5','https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?sectionNum=1942.5.&lawCode=CIV'),
'hud':('HUD fair housing guide, §2.3','https://www.hud.gov/sites/dfiles/PIH/documents/HCV_Guidebook-Chapter_Fair-Housing_April-2025.pdf'),
'challenge':('Tenant summary petition','https://www.sf.gov/file/518-tenant-summary-petition-fillable-224pdf'),
'counsel':('SF tenant right-to-counsel notice',"https://www.sf.gov/sites/default/files/2023-08/1007%20Notice%20to%20Tenant%20Req%27d%20by%2037.%209(c)-Eng-Sp-Ch-Viet-Rus-Tag[74].pdf"),
'court':('SF unlawful detainer guidance','https://www.sf.gov/information--unlawful-detainer-actions-court')}
def row(topic,finding,status,src): return (topic,finding,status,src)
P={
'index':('Executive summary','Start with licensing. Then verify each tenancy.',[
row('Individual owner: yes','Being an individual rather than a corporation does not excuse Housing Inventory reporting or the license requirement for covered annual/banked increases.','Verified rule','inventory'),
row('Report, then license','Report residential unit information through the Rent Board Portal. A rent-increase license is automatically generated for non-owner-occupied units after reporting; reporting is free.','Verified rule','inventory'),
row('Before notice or before effective date?','A current license must be on file before the annual/banked increase goes into effect. The official guidance does not require attaching the license to the tenant notice. Recommendation: obtain and check it before serving notice to avoid timing failures.','Rule + recommendation','inventory'),
row('Not immunity from challenge','A license is not approval of the amount, service, timing, tenancy classification, or motive. Tenants can challenge unlawful increases, including absence of a license. No lawyer outcome can be guaranteed.','Verified rule + limitation','challenge'),
row('Conservative approach','Consider only the current annual allowance, no banked increases or passthroughs until documented. 1.6% applies March 1, 2026–February 28, 2027; the cap is not an obligation to increase.','Recommendation','increase'),
row('Outer Sunset / 94122','The cited SF annual allowance applies to covered units citywide; it is not a neighborhood market-rent benchmark. A neighborhood “normal” increase is not verified here.','Rule; market norm unverified','increase'),
row('Do not issue notices from this site','No unit-specific license, lawful base rent, last increase, lease restriction or coverage has been independently established. This is research, not a legal opinion or a notice.','Needs review','coverage')]),
'process':('Licensing & notice','A step-by-step compliance path, not an automatic filing service.',[
row('01 · Confirm coverage','Check building and unit records, exemptions and lease terms. Many pre-June 14, 1979 units are covered, but a reported 1940 construction year alone does not prove coverage.','Verified rule','coverage'),
row('02 · Report annually','Use the Rent Board Portal at https://portal.sfrb.org/. Reporting deadline is March 1 each year; late reporting remains possible. Keep business-contact details updated within 30 days of changes.','Verified rule','inventory'),
row('03 · Check each license','Confirm the current unit license is on file and remains effective on the increase date. Retain evidence privately. Housing Inventory reporting is separate from the Rent Board fee exemption process.','Verified rule + recordkeeping recommendation','inventory'),
row('04 · Audit rent history','Establish lawful base rent and the last effective increase. First annual increase follows 12 months from lease start; subsequent annual increases require at least 12 months. A delayed increase changes the anniversary.','Verified rule','increase'),
row('05 · Select effective-date rate','Use the allowance effective on the increase date, not service date. Apply to base rent including housing services, excluding temporary passthroughs/fluctuating charges; do not round up to whole dollars.','Verified rule','increase'),
row('06 · Prepare written notice','State dollar increase, percentage and effective date; recommendation: also show old and new base rent. Identify annual and any banked portions separately; Rule 4.10 requires disclosure of applicable certified work, utilities and RAP portions.','Rule + recommendation','rules'),
row('07 · Serve properly','For periodic residential tenancies, §827 allows personal delivery or mail. At least 30 days for an increase totaling 10% or less over the prior 12 months; over 10% generally requires 90 days. These are notice thresholds, not permission to exceed a cap.','Verified rule','notice'),
row('08 · Allow mailing time','SF guidance says add five days if mailed. Check applicable service rules and actual destination; do not assume email or a text message satisfies statutory service. Fixed-term lease terms need separate review.','Verified guidance + recommendation','increase'),
row('09 · Retain a private audit file','Recommendation: preserve license evidence, lease/addenda, ledger, calculations, dated notice, proof of service and neutral decision memo. No personal documents should go in this public repository.','Recommendation','notice'),
row('Annual increase vs petition','Ordinary annual/banked increases within limits are addressed under rules titled “Rent Increases Not Requiring Approval.” Do not confuse inventory licensing with approval of a landlord petition for additional increases.','Verified distinction','rules'),
row('Privacy warning for official filing','The City says Housing Inventory submissions are public and made under penalty of perjury. Use truthful required information in the official portal, not the public site’s placeholder identities.','Verified warning','inventory')]),
'amounts':('Amounts & tenancy analysis','Rules are verified. Actual eligibility and rent figures are not.',[
row('Current annual allowance','1.6%, effective March 1, 2026 through February 28, 2027. This is the ordinary annual allowance, not the maximum including every possible banked/petitioned adjustment.','Verified rule','increase'),
row('Historical allowance','1.4%, March 1, 2025 through February 28, 2026 (shown in the City’s multiple-year examples). No accumulated banked entitlement has been calculated for either unit.','Verified rate; entitlement unverified','increase'),
row('Unit A lawful base rent','','Unverified — official record not supplied','increase'),
row('Unit B lawful base rent','','Unverified — official record not supplied','increase'),
row('Unit A illustrative arithmetic','$3,995.00 × 0.016 = $63.92; hypothetical new base rent $4,058.92. This is derived arithmetic using an owner-reported input, NOT a verified lawful rent or approved increase.','Illustration only','increase'),
row('Unit B illustrative arithmetic','$3,150.00 × 0.016 = $50.40; hypothetical new base rent $3,200.40. This is derived arithmetic using an owner-reported input, NOT a verified lawful rent or approved increase.','Illustration only','increase'),
row('Unit A occupant change','A new roommate moving in with an existing tenant does not itself permit extra rent. Do not treat the reported April 2026 change as a vacancy reset or automatically establish a new annual anniversary. Lease/addendum and actual history need review.','Rule + case limitation','increase'),
row('Unit B long tenancy','A reported 2019 lease start does not prove no intervening increases, concessions or other adjustments. No banked amount or lawful effective date is verified.','Needs review','increase'),
row('Reasonable and normal','Recommendation: a documented current annual increase (or less), lawful timing and neutral treatment is a conservative option. No official source here establishes a market “normal,” and a lawful ceiling is not a fairness guarantee.','Recommendation; norm unverified','increase'),
row('Cost explanations','Routine inflation/maintenance can be a truthful business explanation, but is not authority to exceed the allowance. Extra increases/passthroughs have separate procedures; no cost claim is substantiated for these units.','Analysis','increase'),
row('Future effective dates','','Unverified — recheck the published allowance for dates after February 28, 2027','increase')]),
'protections':('Tenant protections & owner practices','Review the policy, not just the percentage.',[
row('Local and state interaction','SF local rent protections remain applicable. The state 5% + CPI / 10% formula is not an alternative allowance for units subject to SF’s lower local rent cap.','Verified rule','state'),
row('Federal layer','The Fair Housing Act prohibits discrimination in rental terms based on protected characteristics, including race, color, religion, sex, national origin, disability and familial status. HUD guide §2.3 is fair-housing guidance, not a rent-percentage schedule. Subsidized housing can carry additional program rules.','Verified federal guidance','hud'),
row('Raise one unit or both?','Different decisions are not automatically discrimination: the prohibited link is discriminatory or retaliatory treatment. Recommendation: use a neutral written policy, document tenancy-specific timing/eligibility and review exceptions. Increasing both does not cure a discriminatory motive.','Analysis / recommendation, not safe harbor','crd'),
row('Consistency over identical dollars','Recommendation: if both qualify, consider the same annual-only percentage on each unit’s lawful base rent at its lawful time. Different rents produce different dollar amounts. Do not force identical dates if one unit is not eligible.','Recommendation','increase'),
row('Retaliation screen','Do not use an increase to punish repair complaints, tenant organizing or exercise of legal rights. §1942.5 includes specific 180-day protections under stated conditions and broader prohibitions; review the facts before service.','Verified rule','retaliation'),
row('Disability and source of income','California protections include disability accommodation duties and source-of-income protections, including rental assistance. Do not target a tenant because of a voucher, family status or other protected characteristic.','Verified rule','crd'),
row('Large corporate owners: actual practices','','Unverified — no official empirical evidence reviewed establishes how large corporations normally choose increases','increase'),
row('Individual owners: actual practices','','Unverified — no official empirical evidence reviewed establishes a typical owner practice','increase'),
row('Operational comparison','Recommendation for either owner type: use a compliance calendar, unit-specific eligibility checks, written neutral policy and preserved calculations/service evidence. Scale or software is not a substitute for legal compliance.','Recommendation, not observed industry fact','inventory'),
row('Tenant-lawyer stress test','Recommendation: ask whether coverage, license on effective date, lawful base, annual interval, current rate, notice content/service, lease restrictions and motive all have supporting evidence. This site is not a lawyer’s approval.','Recommendation','challenge'),
row('Free lawyer claim: limit','SF official eviction notices refer tenants to the Tenant Right to Counsel Program for free assistance. This does not establish that every rent-increase dispute receives automatic free representation.','Verified distinction','counsel')]),
'flagged':('Flagged for Review','Published limitations do not disappear when the site is deployed.',[
row('F01 · Coverage / construction','','Unverified — 1940 year and rent-control status were owner-reported, not checked against a parcel or determination','coverage'),
row('F02 · License / inventory status','','Unverified — no access to unit records; do not presume a current license','inventory'),
row('F03 · Actual lawful rents / history','','Unverified — owner-reported rent is not an authenticated lawful base; prior increases, concessions and banked rights unknown','increase'),
row('F04 · Unit A continuity','','Unverified — continuing original occupant was reported, not independently authenticated; no vacancy reset recommended','increase'),
row('F05 · Lease and service','','Unverified — no lease end dates, rent clauses, subsidy rules, notice or proof of service reviewed','notice'),
row('F06 · Motive and complaints','','Unverified — no discrimination/retaliation factual assessment or attorney review performed','retaliation'),
row('F07 · Source irregularity','The City annual-increase page’s first example says the June 1, 2025 rate is 1.6%, although the 2025–26 allowance is 1.4%. Do not rely on that example’s mislabeled date; the current-rate heading states the 2026–27 effective period.','Source inconsistency flagged','increase'),
row('F08 · Market and business norms','','Unverified — neither neighborhood norms nor corporate/individual-owner empirical practices established from official sources','increase'),
row('F09 · No guaranteed lawyer result','','Unverified — legal outcome, challenge risk and tenant counsel eligibility cannot be guaranteed','challenge'),
row('F10 · Filing not performed','No Housing Inventory submission, license application, tenant notice or legal engagement has been made. Those require authentic records and authority; public placeholders must not be filed as facts.','Scope limitation','inventory')])}
reported='''<section class="note"><h2>Owner-reported context · not independently verified</h2><p>These are intake statements, not official findings. Dates and amounts are preserved; tenant names and initials are intentionally omitted. Unit labels are placeholders. The combination of dates and amounts may still permit re-identification, so no address, parcel, owner contact or identifying document is published.</p><p><strong>Unit A:</strong> lease start February 1, 2025 at $3,995/month; continuing-tenancy change reported April 1, 2026 at $3,995/month, with one original occupant continuing and a replacement occupant.</p><p><strong>Unit B:</strong> lease start June 1, 2019 at $3,150/month. Reported building year: 1940; reported location: Outer Sunset, San Francisco, 94122; both units described as rent controlled. No official records authenticate these statements. Verified property fields above remain blank.</p></section>'''
nav=[(k,v[0]) for k,v in P.items()]+[('sources','Sources & method')]
for key in [*P,'sources']:
 title,desc,rows=P.get(key,('Sources & method','Evidence checked on November 7, 2026. Rules are not property verification.',[]))
 links=''.join(f'<a href="{k}.html" '+('aria-current="page"' if k==key else '')+f'>{e(t)}</a>' for k,t in nav)
 body=''
 if rows:
  body='<div class="table-wrap"><table><caption>Findings, evidence status and official reference</caption><thead><tr><th scope="col">Topic</th><th scope="col">Finding / verified value</th><th scope="col">Status</th><th scope="col">Official reference</th></tr></thead><tbody>'
  for t,f,st,s in rows:
   name,url=S[s];body+=f'<tr><th scope="row">{e(t)}</th><td>{e(f)}</td><td><span class="status">{e(st)}</span></td><td><a href="{e(url)}">{e(name)} ↗</a></td></tr>'
  body+='</tbody></table></div>'
 if key=='amounts':body+=reported
 if key=='sources':
  body+='<section class="note"><h2>Verification method</h2><p>Official SF, California Legislature, California Civil Rights Department and HUD pages were retrieved or searched during this session. Each finding links its rule source. A link beside an unverified row is a review reference, not evidence that its missing property value is confirmed. Blank cells are intentional.</p><p>Derived examples are explicitly hypothetical and do not turn owner-reported numbers into verified facts. Recommendations and analysis are labeled separately from rules. No private leases, portal account, parcel record, rent ledger, notice or attorney opinion was available. No claim of complete legal certification is made.</p><p>External references were retrieved with research tools; automated build checks validate local links and source coverage, not future availability of government sites. Recheck law and rates before acting. HUD guide §2.3 concerns the Fair Housing Act; other guide sections address voucher-program obligations and are not assumed to apply to these units.</p></section><div class="table-wrap"><table><caption>Official-source register · checked 2026-11-07</caption><thead><tr><th>Source</th><th>Scope</th><th>Official link</th></tr></thead><tbody>'
  for s,(name,url) in S.items():body+=f'<tr><th scope="row">{e(name)}</th><td>Rule reference; no individual tenancy verification</td><td><a href="{e(url)}">{e(url)}</a></td></tr>'
  body+='</tbody></table></div>'
 html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Privacy-safe San Francisco rent increase research with official sources and explicit verification limits."><title>{e(title)} · SF Rent Review</title><link rel="stylesheet" href="style.css"></head><body><a class="skip" href="#main">Skip to findings</a><aside><a class="brand" href="index.html">SF / RENT REVIEW</a><p class="muted">Owner research dashboard</p><nav aria-label="Main navigation">{links}</nav><p class="sidefoot">PUBLIC • ANONYMIZED<br>Research date: 07 Nov 2026</p></aside><main id="main"><header><span class="eyebrow">SAN FRANCISCO · RESIDENTIAL RENT</span><h1>{e(title)}</h1><p class="subtitle">{e(desc)}</p></header><div class="metrics"><div><span>Annual allowance</span><strong>1.6%</strong><small>01 Mar 2026 – 28 Feb 2027 · <a href="{S['increase'][1]}">SF Rent Board</a></small></div><div><span>License first</span><strong>Individual owners too</strong><small>Valid on effective date · <a href="{S['inventory'][1]}">Official requirements</a></small></div><div><span>Property findings</span><strong>Not verified</strong><small>No notices or filings made</small></div></div><p class="banner">Research, not legal advice. No increase is cleared for service. Blank verified-value cells mean evidence is missing; see <a href="flagged.html">Flagged for Review</a>.</p>{body}<footer>Privacy first: no tenant names, initials, exact address, analytics or external assets. Public intake details retain dates and amounts by request. <a href="sources.html">Evidence & limitations</a> · Print this page using your browser.</footer></main></body></html>'''
 Path('site',key+'.html').write_text(html)
Path('site/.nojekyll').touch()
print(f'Built {len(nav)} pages / {sum(len(x[2]) for x in P.values())} finding rows')

# Mirror public artifacts to existing GitHub Pages main:/ configuration.
for artifact in Path("site").iterdir():
 if artifact.is_file(): Path(artifact.name).write_bytes(artifact.read_bytes())

# --- Integrated build · added by session-c6d53281 · 2026-11-07 -------------------
# A second, deeper research set lives in tools/ and publishes pages/, assets/ and a consolidated
# landing page that links both sets. Run it last so the published home page is the merged hub, then
# mirror its artifacts into site/ so the two trees stay identical (the independent audit checks parity).
import subprocess as _sp, shutil as _sh, sys as _sys
# --- Dashboard set · added by session SES-8b5ad092 · 2026-11-07 -------------------
# A third research set (dashboard/) is generated from data/*.json by build.py and mirrored into
# site/dashboard/. It runs before the hub build so the hub's link check can see the files.
# Additive only: nothing above is regenerated or replaced by it.
_sp.run([_sys.executable, 'build.py'], check=True)
_sp.run([_sys.executable, 'tools/build_site.py'], check=True)
_sh.copyfile('index.html', Path('site') / 'index.html')
for _src in list(Path('pages').glob('*.html')) + [p for p in Path('assets').glob('*') if p.is_file()]:
    _dst = Path('site') / _src
    _dst.parent.mkdir(parents=True, exist_ok=True)
    _sh.copyfile(_src, _dst)

# --- Consolidated hub - session arena-d4b68642 (final integration) ------------
# Runs LAST so index.html is the single consolidated landing page. The hub that
# tools/build_site.py just produced is preserved as previous-dashboard.html and
# linked from hub/archive.html, so no earlier session's work is discarded.
_sh.copyfile('index.html', 'previous-dashboard.html')
_sh.copyfile('index.html', Path('site') / 'previous-dashboard.html')
_sp.run([_sys.executable, 'tools/build_hub.py'], check=True)
# The released hub archive links to ../docs/index.html from site/hub/. Mirror the
# existing independent docs set so that target exists under the main:/ publication
# surface. Additive only: no docs content or active hub file is rewritten.
_sh.copytree('docs', Path('site') / 'docs', dirs_exist_ok=True)
print('Consolidated hub built; earlier sets preserved and linked from hub/archive.html.')

