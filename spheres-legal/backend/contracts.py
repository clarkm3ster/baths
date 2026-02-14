"""
contracts.py - Agreement Generation Engine for Public Space Activation in Philadelphia

Provides comprehensive legal agreement templates for temporary and permanent use of
public spaces, revenue sharing, community benefits, insurance, and permanence clauses.
All templates reference real City of Philadelphia requirements, including Department of
Parks & Recreation, Streets Department, and Office of Arts, Culture and the Creative
Economy regulations.

Author: DOMES Project
"""

from __future__ import annotations

import copy
import re
from datetime import date, datetime
from typing import Any


# ---------------------------------------------------------------------------
# Permanence Framework
# ---------------------------------------------------------------------------

PERMANENCE_REQUIREMENTS: dict[str, Any] = {
    "minimum_permanent_value_pct": 25,
    "description": (
        "Every public-space activation agreement executed under this framework "
        "must allocate no less than twenty-five percent (25%) of total project value "
        "toward permanent community benefit. Permanent value is measured across five "
        "categories and must be documented, audited, and reported to the City of "
        "Philadelphia Office of Arts, Culture and the Creative Economy within ninety "
        "(90) days of project completion."
    ),
    "categories": [
        {
            "id": "physical_improvement",
            "name": "Physical Improvement",
            "description": (
                "Tangible, lasting improvements to the physical site or surrounding "
                "public infrastructure that remain after the activation period ends."
            ),
            "examples": [
                "Permanent murals, mosaics, or sculptural installations",
                "ADA-compliant ramp or pathway construction",
                "Stormwater management infrastructure (rain gardens, bioswales)",
                "Permanent seating, shade structures, or lighting fixtures",
                "Playground equipment or fitness stations",
                "Restored or new tree canopy plantings with 5-year maintenance bond",
            ],
        },
        {
            "id": "community_asset",
            "name": "Community Asset Creation",
            "description": (
                "Organizational, programmatic, or institutional assets that strengthen "
                "the surrounding community s capacity for self-governance and continued "
                "activation of public space."
            ),
            "examples": [
                "Establishment of a community land trust or cooperative",
                "Creation of a registered neighborhood advisory board",
                "Endowed fund for ongoing public programming (minimum 0,000)",
                "Shared tool library or community workshop space",
                "Permanent community bulletin board or information kiosk",
                "Digital infrastructure (free public Wi-Fi access point)",
            ],
        },
        {
            "id": "knowledge_transfer",
            "name": "Knowledge Transfer",
            "description": (
                "Structured programs that build skills, share expertise, and create "
                "documented knowledge resources accessible to the public in perpetuity."
            ),
            "examples": [
                "Apprenticeship programs with at least 3 completions",
                "Published open-source toolkit or curriculum",
                "Oral history archive deposited with Free Library of Philadelphia",
                "Training certification program for at least 10 residents",
                "Documented best-practices guide for future activations",
                "Youth mentorship program with minimum 6-month duration",
            ],
        },
        {
            "id": "economic_legacy",
            "name": "Economic Legacy",
            "description": (
                "Lasting economic structures, revenue streams, or employment pathways "
                "that continue to benefit the community beyond the activation period."
            ),
            "examples": [
                "Permanent vendor stalls or market infrastructure",
                "Revenue-generating community asset (e.g., solar array)",
                "Established supply chain relationships with local vendors",
                "Job training pipeline with documented employer partnerships",
                "Micro-enterprise incubator with at least 5 graduates",
                "Community benefit fund with board-governed disbursement",
            ],
        },
        {
            "id": "environmental_improvement",
            "name": "Environmental Improvement",
            "description": (
                "Measurable improvements to environmental quality - air, water, soil, "
                "biodiversity, or climate resilience - that persist beyond the project."
            ),
            "examples": [
                "Remediation of contaminated soil (certified by PA DEP)",
                "Native species habitat restoration (minimum 500 sq ft)",
                "Permanent composting infrastructure",
                "Urban agriculture plots with irrigation and soil amendments",
                "Green roof or living wall installation",
                "Stormwater capture system reducing runoff by at least 25%",
            ],
        },
    ],
}


# ---------------------------------------------------------------------------
# Agreement Templates
# ---------------------------------------------------------------------------

AGREEMENT_TEMPLATES: list[dict[str, Any]] = [
    # -----------------------------------------------------------------------
    # 1. TEMPORARY USE LICENSE
    # -----------------------------------------------------------------------
    {
        "id": "temporary_use_license",
        "name": "Temporary Use License Agreement",
        "description": (
            "Grants a licensee revocable, non-exclusive permission to occupy and "
            "activate a designated public space within the City of Philadelphia for a "
            "defined period. This is NOT a lease and conveys no possessory interest."
        ),
        "category": "use",
        "parties_required": [
            "Licensor (City of Philadelphia or Authorized Agency)",
            "Licensee (Activating Organization or Individual)",
        ],
        "variable_fields": [
            {"field_name": "licensee_name", "field_type": "string", "description": "Full legal name of the licensee organization or individual", "required": True},
            {"field_name": "licensee_address", "field_type": "string", "description": "Mailing address of the licensee", "required": True},
            {"field_name": "site_address", "field_type": "string", "description": "Street address of the public space to be activated", "required": True},
            {"field_name": "site_parcel_id", "field_type": "string", "description": "Philadelphia OPA parcel number", "required": True},
            {"field_name": "site_square_footage", "field_type": "number", "description": "Approximate usable square footage of the licensed area", "required": True},
            {"field_name": "license_start_date", "field_type": "date", "description": "First date of authorized use (YYYY-MM-DD)", "required": True},
            {"field_name": "license_end_date", "field_type": "date", "description": "Last date of authorized use (YYYY-MM-DD)", "required": True},
            {"field_name": "permitted_use_description", "field_type": "text", "description": "Detailed description of the permitted use and activities", "required": True},
            {"field_name": "maximum_occupancy", "field_type": "number", "description": "Maximum number of persons on site at any one time", "required": True},
            {"field_name": "license_fee", "field_type": "currency", "description": "Total fee for the license period, in USD", "required": True},
            {"field_name": "security_deposit", "field_type": "currency", "description": "Refundable security deposit amount, in USD", "required": False},
            {"field_name": "hours_of_operation", "field_type": "string", "description": "Permitted hours (e.g., '8:00 AM - 10:00 PM daily')", "required": True},
            {"field_name": "council_district", "field_type": "string", "description": "Philadelphia City Council district number", "required": True},
        ],
        "standard_terms": [
            "License is revocable at will by the Licensor upon thirty (30) days written notice, or immediately in the event of a threat to public safety.",
            "Licensee shall maintain the premises in a clean, safe, and sanitary condition at all times and shall comply with all applicable City of Philadelphia codes and ordinances.",
            "No permanent structures or alterations shall be made without prior written consent of the Licensor and all required permits from the Philadelphia Department of Licenses & Inspections.",
            "Licensee shall obtain and maintain throughout the license period a commercial general liability insurance policy with minimum coverage of One Million Dollars ($1,000,000) per occurrence and Two Million Dollars ($2,000,000) aggregate, naming the City of Philadelphia as additional insured.",
            "Licensee shall not assign or sublicense any rights under this agreement without the prior written consent of the Licensor.",
            "Upon expiration or termination, Licensee shall restore the site to its original condition within fourteen (14) days at Licensee's sole expense.",
            "Licensee shall comply with all noise ordinances as set forth in Philadelphia Code Title 10, Chapter 10-400.",
            "Licensee shall provide ADA-compliant access to the site at all times during public-facing operations.",
        ],
        "negotiation_points": [
            "Duration and renewal options",
            "Fee schedule and payment terms",
            "Scope of permitted activities",
            "Insurance coverage levels above minimums",
            "Hours of operation",
            "Noise and amplified sound allowances",
            "Signage and branding rights",
            "Exclusivity provisions",
        ],
        "philadelphia_specific_requirements": [
            "Obtain a Temporary Use Permit from the Philadelphia Department of Licenses & Inspections (L&I) for any structure, tent, or stage exceeding 120 square feet.",
            "File a Special Events Application with the Managing Director's Office for events exceeding 200 attendees.",
            "Notify the relevant City Council member's office at least fourteen (14) days before the first day of use.",
            "Comply with Philadelphia Parks & Recreation regulations if the site is within Fairmount Park or any PPR-managed property.",
            "Obtain a Philadelphia Commercial Activity License (CAL) if any commercial sales will occur on site.",
            "Submit a Stormwater Management Plan to the Philadelphia Water Department if the activation covers more than 5,000 square feet of impervious surface.",
            "Coordinate with the Philadelphia Police Department for traffic management if the activation will affect vehicular traffic on any public right-of-way.",
        ],
        "estimated_legal_review_hours": 4,
        "template_text": """TEMPORARY USE LICENSE AGREEMENT

THIS TEMPORARY USE LICENSE AGREEMENT ("Agreement") is entered into as of the date last signed below (the "Effective Date"), by and between:

LICENSOR: The City of Philadelphia, acting through its Department of Parks & Recreation and/or the Philadelphia Land Bank, with offices at 1515 Arch Street, Philadelphia, PA 19102 (the "City" or "Licensor");

and

LICENSEE: {{licensee_name}}, with a mailing address at {{licensee_address}} (the "Licensee").

COLLECTIVELY, the Licensor and Licensee are referred to as the "Parties" and individually as a "Party."

RECITALS

WHEREAS, the City of Philadelphia owns or controls certain real property located at {{site_address}}, identified by the Philadelphia Office of Property Assessment as Parcel No. {{site_parcel_id}}, comprising approximately {{site_square_footage}} square feet (the "Premises"); and

WHEREAS, the Licensee desires to use the Premises on a temporary, non-exclusive, revocable basis for the purpose of {{permitted_use_description}}; and

WHEREAS, the City desires to encourage productive activation of underutilized public spaces in accordance with the Philadelphia2035 Comprehensive Plan and the goals of the City's Office of Arts, Culture and the Creative Economy; and

WHEREAS, the City has determined that such temporary use is consistent with the public interest and does not interfere with any planned municipal use of the Premises;

NOW, THEREFORE, in consideration of the mutual covenants and conditions set forth herein, and for other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the Parties agree as follows:

ARTICLE 1 - GRANT OF LICENSE

1.1. License. The City hereby grants to Licensee a revocable, non-exclusive, non-transferable license (the "License") to enter upon and use the Premises solely for the purposes described in this Agreement. This License is personal to Licensee and does not create any leasehold estate, tenancy, or possessory interest in the Premises.

1.2. Term. The License shall commence on {{license_start_date}} and shall expire on {{license_end_date}} (the "License Period"), unless sooner terminated in accordance with this Agreement.

1.3. Hours of Operation. Licensee's use of the Premises shall be limited to the following hours: {{hours_of_operation}}. Operations outside these hours require prior written approval from the Licensor.

1.4. Occupancy. The maximum number of persons on the Premises at any one time shall not exceed {{maximum_occupancy}} persons, inclusive of Licensee's staff, vendors, performers, and members of the public.

ARTICLE 2 - FEES AND DEPOSITS

2.1. License Fee. Licensee shall pay to the City a license fee of {{license_fee}} USD (the "License Fee"), payable in full within ten (10) business days of the Effective Date unless an alternative payment schedule is set forth in Exhibit A.

2.2. Security Deposit. Licensee shall deposit with the City the sum of {{security_deposit}} USD (the "Security Deposit") prior to the commencement of the License Period. The Security Deposit shall be returned to Licensee, without interest, within thirty (30) days following the expiration or termination of this Agreement, less any amounts deducted for damage, unpaid fees, or restoration costs.

2.3. No Abatement. The License Fee shall not be subject to abatement or reduction for any reason, including inclement weather, except by mutual written agreement of the Parties.

ARTICLE 3 - USE AND CONDUCT

3.1. Permitted Use. Licensee shall use the Premises solely for the following purpose: {{permitted_use_description}}. Any use not expressly authorized herein is prohibited.

3.2. Compliance with Law. Licensee shall, at its sole expense, comply with all applicable federal, state, and local laws, ordinances, regulations, and codes, including but not limited to the Philadelphia Code, the Pennsylvania Liquor Code, Title III of the Americans with Disabilities Act, and all applicable fire and safety codes.

3.3. Philadelphia City Council Notification. Licensee acknowledges that the Premises are located within Philadelphia City Council District {{council_district}}. Licensee shall notify the office of the Council member representing said district at least fourteen (14) days prior to the commencement of activities.

3.4. Noise. Licensee shall comply with the noise regulations set forth in Philadelphia Code Title 10, Chapter 10-400. Amplified sound shall not exceed seventy (70) decibels as measured from the nearest residential property line between the hours of 9:00 PM and 8:00 AM.

3.5. Sanitation. Licensee shall provide adequate waste receptacles and shall remove all trash and debris from the Premises and surrounding sidewalks at the close of each operating day. Licensee shall arrange for supplemental waste hauling if the volume exceeds normal municipal collection capacity.

3.6. No Alterations. Licensee shall not make any permanent alterations, additions, or improvements to the Premises without the prior written consent of the Licensor and the issuance of all required permits by the Philadelphia Department of Licenses & Inspections.

ARTICLE 4 - INSURANCE

4.1. General Liability. Licensee shall obtain and maintain, at its sole expense, commercial general liability insurance with a minimum coverage of One Million Dollars ($1,000,000) per occurrence and Two Million Dollars ($2,000,000) in the aggregate. The policy shall name the City of Philadelphia, its officers, employees, and agents as additional insureds.

4.2. Workers' Compensation. If Licensee has employees, Licensee shall maintain workers' compensation insurance as required by the laws of the Commonwealth of Pennsylvania.

4.3. Evidence of Insurance. Licensee shall deliver certificates of insurance to the City's Risk Management Division at least ten (10) days prior to the commencement of the License Period.

ARTICLE 5 - INDEMNIFICATION

5.1. Licensee shall defend, indemnify, and hold harmless the City of Philadelphia, its elected officials, officers, employees, agents, and volunteers from and against any and all claims, demands, suits, losses, damages, judgments, costs, and expenses (including reasonable attorneys' fees) arising out of or resulting from Licensee's use of the Premises, including but not limited to claims for bodily injury, death, or property damage.

ARTICLE 6 - TERMINATION

6.1. Termination by City. The City may terminate this License at any time upon thirty (30) days' written notice to Licensee, or immediately upon written notice if Licensee's use poses an imminent threat to public safety, violates any law or regulation, or materially breaches any provision of this Agreement.

6.2. Termination by Licensee. Licensee may terminate this License upon thirty (30) days' written notice to the City. No refund of the License Fee shall be due unless otherwise agreed in writing.

6.3. Restoration. Upon expiration or termination, Licensee shall, at its sole expense, restore the Premises to its condition as of the Effective Date within fourteen (14) calendar days, reasonable wear and tear excepted.

ARTICLE 7 - GENERAL PROVISIONS

7.1. Governing Law. This Agreement shall be governed by and construed in accordance with the laws of the Commonwealth of Pennsylvania, without regard to conflicts-of-law principles.

7.2. Venue. Any action arising under this Agreement shall be brought exclusively in the Court of Common Pleas of Philadelphia County or the United States District Court for the Eastern District of Pennsylvania.

7.3. Entire Agreement. This Agreement constitutes the entire agreement between the Parties with respect to the subject matter hereof and supersedes all prior and contemporaneous agreements and understandings.

7.4. Amendments. This Agreement may not be amended except by a written instrument signed by both Parties.

7.5. Waiver. No waiver of any provision of this Agreement shall be deemed a waiver of any other provision, nor shall any waiver constitute a continuing waiver.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the date last signed below.

LICENSOR:
City of Philadelphia
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________

LICENSEE:
{{licensee_name}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________""",
    },

    # -----------------------------------------------------------------------
    # 2. SPACE ACTIVATION AGREEMENT
    # -----------------------------------------------------------------------
    {
        "id": "space_activation_agreement",
        "name": "Public Space Activation Agreement",
        "description": (
            "A comprehensive agreement governing the activation of a public space "
            "with programming, installations, and community engagement. More detailed "
            "than a simple license, this agreement addresses programming commitments, "
            "community advisory requirements, and reporting obligations."
        ),
        "category": "use",
        "parties_required": [
            "Property Owner (City of Philadelphia or Authorized Agency)",
            "Activation Partner (Organization Leading the Activation)",
            "Community Advisory Body (Registered Community Organization)",
        ],
        "variable_fields": [
            {"field_name": "activation_partner_name", "field_type": "string", "description": "Legal name of the activating organization", "required": True},
            {"field_name": "activation_partner_ein", "field_type": "string", "description": "Federal Employer Identification Number of the activating organization", "required": True},
            {"field_name": "community_org_name", "field_type": "string", "description": "Name of the registered community organization serving as advisory body", "required": True},
            {"field_name": "site_address", "field_type": "string", "description": "Full street address of the activation site", "required": True},
            {"field_name": "site_parcel_id", "field_type": "string", "description": "Philadelphia OPA parcel number", "required": True},
            {"field_name": "activation_start_date", "field_type": "date", "description": "Start date of the activation period", "required": True},
            {"field_name": "activation_end_date", "field_type": "date", "description": "End date of the activation period", "required": True},
            {"field_name": "programming_description", "field_type": "text", "description": "Detailed description of all planned programming and activities", "required": True},
            {"field_name": "total_project_budget", "field_type": "currency", "description": "Total project budget in USD", "required": True},
            {"field_name": "city_contribution", "field_type": "currency", "description": "City financial contribution, if any, in USD", "required": False},
            {"field_name": "minimum_free_programming_hours", "field_type": "number", "description": "Minimum number of hours of free public programming per week", "required": True},
            {"field_name": "reporting_frequency", "field_type": "string", "description": "How often reports are due (e.g., monthly, quarterly)", "required": True},
        ],
        "standard_terms": [
            "Activation Partner shall provide a minimum of the specified free public programming hours per week during the activation period.",
            "All programming shall be accessible to persons with disabilities in compliance with Title III of the Americans with Disabilities Act and the Philadelphia Fair Practices Ordinance.",
            "Activation Partner shall convene a Community Advisory Committee comprising at least five (5) residents of the surrounding neighborhood, meeting no less than quarterly.",
            "Activation Partner shall submit activity reports at the agreed frequency to the City's Office of Arts, Culture and the Creative Economy, including attendance data, programming descriptions, and financial summaries.",
            "Activation Partner shall maintain commercial general liability insurance of no less than $1,000,000 per occurrence / $2,000,000 aggregate, naming the City as additional insured.",
            "Activation Partner shall allocate no less than twenty-five percent (25%) of the total project value toward permanent community benefit as defined in the Permanence Framework.",
            "The City reserves the right to conduct unannounced site inspections during operating hours.",
            "Activation Partner shall hire from the local community for at least 50% of all paid positions created by the activation.",
        ],
        "negotiation_points": [
            "Scope and frequency of programming",
            "Community advisory committee composition and authority",
            "Permanence commitment percentage (minimum 25%)",
            "Revenue sharing terms",
            "City financial contribution and disbursement schedule",
            "Reporting and audit requirements",
            "Renewal and extension options",
            "Branding and naming rights",
            "Sublicensing to vendors and performers",
        ],
        "philadelphia_specific_requirements": [
            "Register activation with the Philadelphia Office of Arts, Culture and the Creative Economy.",
            "Comply with the Philadelphia Percent for Art Program if total project budget exceeds $250,000.",
            "Obtain a Public Entertainment Permit from the Philadelphia Department of Licenses & Inspections for any event with paid admission.",
            "File a community impact statement with the relevant Registered Community Organization (RCO) at least 30 days before activation begins.",
            "Comply with Philadelphia's Fair Workweek Ordinance (Chapter 9-4400) for any employees scheduled for retail or food service roles.",
            "If food is served, obtain all required Philadelphia Department of Public Health permits and comply with the Philadelphia Food Code.",
        ],
        "estimated_legal_review_hours": 8,
        "template_text": """PUBLIC SPACE ACTIVATION AGREEMENT

THIS PUBLIC SPACE ACTIVATION AGREEMENT ("Agreement") is made and entered into as of the date last signed below (the "Effective Date"), by and among:

THE CITY OF PHILADELPHIA, a municipal corporation of the Commonwealth of Pennsylvania, acting through its Department of Parks & Recreation and the Office of Arts, Culture and the Creative Economy, with principal offices at 1515 Arch Street, Philadelphia, PA 19102 (the "City");

{{activation_partner_name}}, an organization with EIN {{activation_partner_ein}} (the "Activation Partner");

and

{{community_org_name}}, a registered community organization recognized under the Philadelphia Zoning Code, Section 14-303(12)(e) (the "Community Advisory Body").

RECITALS

WHEREAS, the City of Philadelphia owns certain real property located at {{site_address}}, designated as Parcel No. {{site_parcel_id}} in the records of the Philadelphia Office of Property Assessment (the "Site"); and

WHEREAS, the City seeks to activate underutilized public spaces in accordance with the Philadelphia2035 Comprehensive Plan, the Rebuild Initiative, and the goals of vibrant, equitable, and inclusive public life; and

WHEREAS, the Activation Partner has proposed a program of activities, installations, and community engagement as described herein; and

WHEREAS, the Community Advisory Body has reviewed the proposed activation and has endorsed its alignment with community priorities;

NOW, THEREFORE, in consideration of the mutual covenants set forth herein, the Parties agree as follows:

ARTICLE 1 - PURPOSE AND SCOPE

1.1. Purpose. The purpose of this Agreement is to establish the terms under which the Activation Partner will program, manage, and maintain the Site for the benefit of the public, with particular emphasis on serving the residents of the surrounding neighborhood.

1.2. Activation Period. The activation shall commence on {{activation_start_date}} and conclude on {{activation_end_date}} (the "Activation Period"), subject to renewal upon mutual written agreement.

1.3. Programming. The Activation Partner shall implement the following programming: {{programming_description}}. Programming shall include a minimum of {{minimum_free_programming_hours}} hours per week of free, open-to-the-public activities.

ARTICLE 2 - FINANCIAL TERMS

2.1. Total Project Budget. The total budget for the activation is {{total_project_budget}} USD. The Activation Partner shall provide a detailed budget breakdown as Exhibit B.

2.2. City Contribution. The City shall contribute {{city_contribution}} USD toward the activation, disbursed according to the schedule in Exhibit C. All City funds shall be subject to audit by the City Controller's Office.

2.3. Permanence Allocation. The Activation Partner shall allocate no less than twenty-five percent (25%) of the total project value toward permanent community benefit, as defined in the Permanence Framework annexed as Exhibit D. Documentation of permanence investments shall be submitted with each periodic report.

ARTICLE 3 - COMMUNITY ENGAGEMENT

3.1. Community Advisory Committee. The Activation Partner shall establish and maintain a Community Advisory Committee ("CAC") comprising no fewer than five (5) residents of the zip codes immediately surrounding the Site. The CAC shall meet no less than quarterly, and its recommendations shall be documented and shared with the City.

3.2. Local Hiring. The Activation Partner shall use best efforts to fill at least fifty percent (50%) of all paid positions created by the activation with residents of the City of Philadelphia, with preference given to residents of the surrounding neighborhood.

3.3. Cultural Competence. All programming shall reflect and respect the cultural diversity of the surrounding community. The Activation Partner shall conduct community input sessions prior to finalizing seasonal programming calendars.

ARTICLE 4 - REPORTING AND ACCOUNTABILITY

4.1. Periodic Reports. The Activation Partner shall submit reports on a {{reporting_frequency}} basis to the City's Office of Arts, Culture and the Creative Economy, including: (a) attendance figures; (b) programming summaries; (c) financial statements; (d) permanence investment documentation; (e) community feedback summaries.

4.2. Annual Audit. If the total project budget exceeds One Hundred Thousand Dollars ($100,000), the Activation Partner shall provide an annual financial audit conducted by an independent certified public accountant.

4.3. Site Inspections. The City reserves the right to conduct announced or unannounced site inspections during operating hours to verify compliance with this Agreement and all applicable laws.

ARTICLE 5 - INSURANCE AND INDEMNIFICATION

5.1. Insurance. The Activation Partner shall maintain, at its sole expense, the following insurance coverage throughout the Activation Period:
    (a) Commercial General Liability: $1,000,000 per occurrence / $2,000,000 aggregate;
    (b) Workers' Compensation: As required by Pennsylvania law;
    (c) Automobile Liability (if applicable): $1,000,000 combined single limit;
    (d) Professional Liability (if applicable): $1,000,000 per claim.
All policies shall name the City of Philadelphia, its officers, employees, and agents as additional insureds.

5.2. Indemnification. The Activation Partner shall defend, indemnify, and hold harmless the City from all claims, damages, losses, and expenses arising out of the Activation Partner's use of the Site or performance under this Agreement.

ARTICLE 6 - TERMINATION

6.1. Termination for Cause. Either Party may terminate this Agreement upon sixty (60) days' written notice if the other Party materially breaches any provision and fails to cure such breach within thirty (30) days of receiving notice thereof.

6.2. Termination for Convenience. The City may terminate this Agreement for convenience upon ninety (90) days' written notice.

6.3. Effect of Termination. Upon termination, the Activation Partner shall complete all permanence commitments then in progress, restore non-permanent areas of the Site, and submit a final report within sixty (60) days.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the date last signed below.

CITY OF PHILADELPHIA
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________

ACTIVATION PARTNER: {{activation_partner_name}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________

COMMUNITY ADVISORY BODY: {{community_org_name}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________""",
    },

    # -----------------------------------------------------------------------
    # 3. REVENUE SHARING AGREEMENT
    # -----------------------------------------------------------------------
    {
        "id": "revenue_sharing_agreement",
        "name": "Revenue Sharing Agreement",
        "description": (
            "Governs the distribution of revenue generated from commercial activities "
            "conducted on public space, including vendor fees, ticket sales, sponsorships, "
            "and concessions. Ensures equitable distribution among the City, the operating "
            "partner, and the surrounding community."
        ),
        "category": "financial",
        "parties_required": [
            "Revenue Generator (Operating Partner or Vendor)",
            "Property Owner (City of Philadelphia)",
            "Community Benefit Recipient (Designated Community Organization or Fund)",
        ],
        "variable_fields": [
            {"field_name": "operator_name", "field_type": "string", "description": "Legal name of the operating partner generating revenue", "required": True},
            {"field_name": "site_address", "field_type": "string", "description": "Address of the revenue-generating site", "required": True},
            {"field_name": "community_fund_name", "field_type": "string", "description": "Name of the community benefit fund or organization", "required": True},
            {"field_name": "agreement_start_date", "field_type": "date", "description": "Start date of the revenue sharing period", "required": True},
            {"field_name": "agreement_end_date", "field_type": "date", "description": "End date of the revenue sharing period", "required": True},
            {"field_name": "city_share_pct", "field_type": "number", "description": "Percentage of net revenue allocated to the City", "required": True},
            {"field_name": "operator_share_pct", "field_type": "number", "description": "Percentage of net revenue retained by the operator", "required": True},
            {"field_name": "community_share_pct", "field_type": "number", "description": "Percentage of net revenue allocated to the community fund", "required": True},
            {"field_name": "minimum_annual_guarantee", "field_type": "currency", "description": "Minimum annual payment to the City regardless of revenue", "required": True},
            {"field_name": "revenue_reporting_period", "field_type": "string", "description": "How often revenue is reported and distributed (e.g., monthly, quarterly)", "required": True},
            {"field_name": "gross_revenue_threshold", "field_type": "currency", "description": "Gross revenue threshold above which sharing percentages apply", "required": False},
        ],
        "standard_terms": [
            "All revenue figures shall be calculated on a net basis, deducting only sales tax, credit card processing fees, and documented cost of goods sold.",
            "Operator shall maintain complete and accurate books and records of all revenue generated at the site, available for inspection by the City upon 48 hours notice.",
            "Revenue sharing payments shall be accompanied by a certified revenue report signed by the Operator's chief financial officer or authorized representative.",
            "The City reserves the right to audit the Operator's books and records at any time, at the City's expense, with a surcharge to the Operator if the audit reveals underreporting of more than 5%.",
            "The community share shall be deposited into the designated community fund within fifteen (15) days of the close of each reporting period.",
            "Philadelphia Business Income and Receipts Tax (BIRT) and Net Profits Tax obligations remain the sole responsibility of the Operator.",
        ],
        "negotiation_points": [
            "Revenue sharing percentages among City, Operator, and Community",
            "Definition of net revenue and allowable deductions",
            "Minimum annual guarantee amount",
            "Revenue threshold before sharing commences",
            "Audit rights and frequency",
            "Treatment of in-kind sponsorships",
            "Capital improvement credits against revenue share",
            "Performance benchmarks triggering adjusted percentages",
        ],
        "philadelphia_specific_requirements": [
            "Operator must hold a valid Philadelphia Commercial Activity License.",
            "All revenue must be reported for Philadelphia Business Income and Receipts Tax (BIRT) purposes.",
            "Community fund disbursements must comply with Pennsylvania nonprofit law if the recipient is a 501(c)(3).",
            "Revenue generated on Philadelphia Land Bank property is subject to Land Bank disposition policies.",
            "Food and beverage revenue must comply with Philadelphia Department of Public Health regulations.",
        ],
        "estimated_legal_review_hours": 6,
        "template_text": """REVENUE SHARING AGREEMENT

THIS REVENUE SHARING AGREEMENT ("Agreement") is entered into as of the date last signed below (the "Effective Date"), by and among:

THE CITY OF PHILADELPHIA, a municipal corporation of the Commonwealth of Pennsylvania, acting through its Department of Revenue and the managing department with jurisdiction over the Site (the "City");

{{operator_name}} (the "Operator"); and

{{community_fund_name}} (the "Community Fund").

RECITALS

WHEREAS, the City has authorized the Operator to conduct revenue-generating activities at the public space located at {{site_address}} (the "Site") pursuant to a separate activation or license agreement; and

WHEREAS, the Parties desire to establish a fair, transparent, and accountable mechanism for sharing revenue generated at the Site;

NOW, THEREFORE, the Parties agree as follows:

ARTICLE 1 - TERM

1.1. This Agreement shall be effective from {{agreement_start_date}} through {{agreement_end_date}}, coterminous with the underlying activation or license agreement.

ARTICLE 2 - REVENUE DEFINITIONS

2.1. "Gross Revenue" means all income received by the Operator from activities conducted at the Site, including but not limited to vendor fees, ticket sales, concession sales, sponsorship payments, advertising revenue, rental fees, and parking fees.

2.2. "Net Revenue" means Gross Revenue less the following allowable deductions: (a) sales tax collected and remitted; (b) credit card and payment processing fees not to exceed three percent (3%) of transaction value; (c) documented cost of goods sold for items sold directly by the Operator (not applicable to vendor sublicenses).

2.3. "Allowable Operating Expenses" shall NOT be deducted from Net Revenue for purposes of calculating revenue shares. The Parties acknowledge that the sharing percentages herein account for the Operator's operating costs.

ARTICLE 3 - REVENUE SHARING

3.1. Distribution. Net Revenue shall be distributed as follows:
    (a) City of Philadelphia: {{city_share_pct}}%
    (b) Operator: {{operator_share_pct}}%
    (c) Community Fund: {{community_share_pct}}%

3.2. Minimum Annual Guarantee. Regardless of actual revenue, the Operator shall pay to the City a minimum annual guarantee of {{minimum_annual_guarantee}} USD, payable in equal installments on a {{revenue_reporting_period}} basis. In the event that the City's share under Section 3.1(a) exceeds the minimum annual guarantee, the City shall receive the greater amount.

3.3. Revenue Threshold. Revenue sharing under Section 3.1 shall apply to all Net Revenue in excess of {{gross_revenue_threshold}} USD per annum. Net Revenue below this threshold shall be retained entirely by the Operator, except that the minimum annual guarantee remains payable.

ARTICLE 4 - REPORTING AND PAYMENT

4.1. Reporting Period. The Operator shall report revenue on a {{revenue_reporting_period}} basis. Reports shall be due within fifteen (15) days of the close of each reporting period.

4.2. Certified Reports. Each revenue report shall include: (a) itemized Gross Revenue by source; (b) itemized deductions; (c) calculated Net Revenue; (d) amounts due to each Party. Reports shall be certified by the Operator's chief financial officer or an authorized officer.

4.3. Payment. Revenue sharing payments to the City and the Community Fund shall accompany each certified report. Payments more than fifteen (15) days late shall bear interest at the rate of one and one-half percent (1.5%) per month.

ARTICLE 5 - AUDIT RIGHTS

5.1. The City shall have the right to audit the Operator's books and records related to Site revenue at any time upon forty-eight (48) hours' written notice. If an audit reveals that the Operator has underreported Net Revenue by more than five percent (5%) in any reporting period, the Operator shall bear the full cost of the audit and shall immediately remit all underpaid amounts plus interest.

ARTICLE 6 - COMMUNITY FUND GOVERNANCE

6.1. The Community Fund shall be governed by a board of no fewer than five (5) members, a majority of whom shall be residents of the zip codes immediately surrounding the Site.

6.2. The Community Fund shall disburse funds solely for purposes that benefit the community surrounding the Site, including but not limited to public programming, infrastructure improvements, scholarships, small business grants, and workforce development.

6.3. The Community Fund shall provide the City with annual audited financial statements within ninety (90) days of the close of each fiscal year.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the date last signed below.

CITY OF PHILADELPHIA
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________

OPERATOR: {{operator_name}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________

COMMUNITY FUND: {{community_fund_name}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________""",
    },

    # -----------------------------------------------------------------------
    # 4. COMMUNITY BENEFIT AGREEMENT
    # -----------------------------------------------------------------------
    {
        "id": "community_benefit_agreement",
        "name": "Community Benefit Agreement",
        "description": (
            "A binding agreement between a developer or activator and community "
            "stakeholders that guarantees specific benefits to the surrounding "
            "neighborhood in exchange for community support of the project."
        ),
        "category": "community",
        "parties_required": [
            "Developer / Activator",
            "Community Coalition (representing neighborhood organizations)",
            "City of Philadelphia (as witness and enforcement body)",
        ],
        "variable_fields": [
            {"field_name": "developer_name", "field_type": "string", "description": "Legal name of the developer or activating entity", "required": True},
            {"field_name": "coalition_name", "field_type": "string", "description": "Name of the community coalition or alliance", "required": True},
            {"field_name": "project_name", "field_type": "string", "description": "Name of the development or activation project", "required": True},
            {"field_name": "site_address", "field_type": "string", "description": "Address of the project site", "required": True},
            {"field_name": "local_hiring_pct", "field_type": "number", "description": "Minimum percentage of jobs to be filled by local residents", "required": True},
            {"field_name": "living_wage_rate", "field_type": "currency", "description": "Minimum hourly wage for all project employees", "required": True},
            {"field_name": "community_fund_amount", "field_type": "currency", "description": "Total contribution to the community benefit fund", "required": True},
            {"field_name": "affordable_space_pct", "field_type": "number", "description": "Percentage of commercial space reserved at below-market rates", "required": False},
            {"field_name": "environmental_commitments", "field_type": "text", "description": "Specific environmental remediation or improvement commitments", "required": True},
            {"field_name": "monitoring_period_years", "field_type": "number", "description": "Number of years the CBA will be monitored for compliance", "required": True},
        ],
        "standard_terms": [
            "Developer shall pay all workers, including subcontractor employees, no less than the agreed living wage rate.",
            "Developer shall provide quarterly compliance reports to the Community Coalition and the City for the entire monitoring period.",
            "Failure to meet local hiring targets shall trigger liquidated damages of $500 per unfilled local position per month.",
            "Community Coalition shall have standing to enforce this Agreement in the Court of Common Pleas of Philadelphia County.",
            "Developer shall fund an independent compliance monitor, selected jointly by the Developer and the Coalition, for the duration of the monitoring period.",
            "All community benefit commitments shall be binding on successors and assigns of the Developer.",
        ],
        "negotiation_points": [
            "Local hiring percentage and geographic definition of 'local'",
            "Wage floor and benefits package",
            "Community fund contribution amount and disbursement schedule",
            "Environmental remediation scope",
            "Affordable commercial space allocation",
            "Anti-displacement provisions",
            "Enforcement mechanisms and liquidated damages",
            "Duration of obligations",
        ],
        "philadelphia_specific_requirements": [
            "CBA must be filed with the Philadelphia Department of Commerce.",
            "Local hiring provisions must be consistent with Philadelphia's Economic Opportunity Plan requirements for city-assisted projects.",
            "Wage commitments must meet or exceed the City of Philadelphia's prevailing wage requirements where applicable.",
            "Environmental commitments must be coordinated with the Philadelphia Department of Public Health's Air Management Services.",
            "If the project receives any City subsidy exceeding $100,000, the CBA must be consistent with the Philadelphia 21st Century Minimum Wage and Benefits Standard.",
        ],
        "estimated_legal_review_hours": 12,
        "template_text": """COMMUNITY BENEFIT AGREEMENT

THIS COMMUNITY BENEFIT AGREEMENT ("CBA" or "Agreement") is entered into as of the date last signed below (the "Effective Date"), by and among:

{{developer_name}} (the "Developer");

{{coalition_name}}, a coalition of community organizations representing the residents and stakeholders of the neighborhood surrounding the project site (the "Coalition"); and

THE CITY OF PHILADELPHIA, acting as witness and enforcement body (the "City").

RECITALS

WHEREAS, the Developer proposes to undertake a project known as "{{project_name}}" at the site located at {{site_address}}, Philadelphia, PA (the "Project"); and

WHEREAS, the Coalition represents the interests of community members who will be directly affected by the Project; and

WHEREAS, the Parties recognize that equitable development requires binding commitments to ensure that the benefits of the Project are shared with the surrounding community; and

WHEREAS, the Developer seeks community support and the Coalition seeks enforceable guarantees of community benefit;

NOW, THEREFORE, in consideration of the mutual promises and covenants herein, the Parties agree as follows:

ARTICLE 1 - LOCAL HIRING AND WORKFORCE

1.1. Local Hiring. The Developer shall ensure that no fewer than {{local_hiring_pct}}% of all jobs created by the Project - including construction, operations, and management positions - are filled by residents of the City of Philadelphia, with priority given to residents of the zip codes within one mile of the Site.

1.2. Living Wage. The Developer shall pay, and shall require all contractors and subcontractors to pay, a minimum hourly wage of {{living_wage_rate}} USD to all workers engaged in the Project. This wage floor shall be adjusted annually by the Consumer Price Index for the Philadelphia-Camden-Wilmington metropolitan area.

1.3. Workforce Development. The Developer shall establish or fund a pre-apprenticeship training program in partnership with a Philadelphia-based workforce development organization, enrolling no fewer than ten (10) participants per year for the duration of the monitoring period.

ARTICLE 2 - COMMUNITY FUND

2.1. Contribution. The Developer shall contribute a total of {{community_fund_amount}} USD to the Community Benefit Fund (the "Fund"), disbursed according to the schedule in Exhibit A.

2.2. Governance. The Fund shall be governed by a board comprising representatives of the Coalition (majority), the Developer (one seat), and the City (one seat). Disbursement decisions shall be made by majority vote.

2.3. Permitted Uses. Fund disbursements shall be limited to: (a) public space improvements; (b) youth programming and education; (c) small business grants; (d) anti-displacement assistance; (e) cultural programming; and (f) environmental remediation.

ARTICLE 3 - AFFORDABLE AND ACCESSIBLE SPACE

3.1. Below-Market Space. The Developer shall reserve {{affordable_space_pct}}% of all commercial or programmable space within the Project for community-serving tenants at rents not exceeding fifty percent (50%) of the fair market rate, for a period of no less than fifteen (15) years.

3.2. Community Priority. Priority for below-market space shall be given to: (a) businesses owned by residents of the surrounding neighborhood; (b) certified Minority, Women, or Disabled-Owned Business Enterprises; (c) nonprofit organizations serving the local community.

ARTICLE 4 - ENVIRONMENTAL COMMITMENTS

4.1. The Developer shall undertake the following environmental improvements: {{environmental_commitments}}.

4.2. All environmental work shall comply with Pennsylvania Department of Environmental Protection standards and shall be documented with third-party environmental assessments.

ARTICLE 5 - MONITORING AND ENFORCEMENT

5.1. Monitoring Period. The commitments in this Agreement shall be monitored for {{monitoring_period_years}} years from the Effective Date.

5.2. Independent Monitor. The Parties shall jointly select and the Developer shall fund an independent compliance monitor who shall produce semi-annual compliance reports.

5.3. Quarterly Reports. The Developer shall provide the Coalition and the City with quarterly reports documenting compliance with all commitments.

5.4. Liquidated Damages. In the event the Developer fails to meet the local hiring commitment in any quarter, the Developer shall pay liquidated damages of Five Hundred Dollars ($500) per unfilled local position per month of non-compliance, payable to the Community Benefit Fund.

5.5. Legal Enforcement. The Coalition shall have standing to enforce this Agreement in the Court of Common Pleas of Philadelphia County. The prevailing party in any enforcement action shall be entitled to recover reasonable attorneys' fees.

ARTICLE 6 - SUCCESSORS AND ASSIGNS

6.1. This Agreement shall be binding on the Developer's successors, assigns, and transferees. Any transfer of the Developer's interest in the Project shall require the transferee to assume all obligations under this Agreement.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the date last signed below.

DEVELOPER: {{developer_name}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________

COALITION: {{coalition_name}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________

CITY OF PHILADELPHIA (Witness)
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________""",
    },

    # -----------------------------------------------------------------------
    # 5. ARTIST / PERFORMER CONTRACT
    # -----------------------------------------------------------------------
    {
        "id": "artist_performer_contract",
        "name": "Artist and Performer Engagement Contract",
        "description": (
            "Governs the engagement of artists, musicians, performers, and cultural "
            "practitioners for public space activations. Addresses compensation, "
            "intellectual property, performance requirements, and artist rights."
        ),
        "category": "use",
        "parties_required": [
            "Commissioning Organization (Activation Partner)",
            "Artist / Performer",
        ],
        "variable_fields": [
            {"field_name": "artist_name", "field_type": "string", "description": "Legal name of the artist or performer", "required": True},
            {"field_name": "artist_address", "field_type": "string", "description": "Mailing address of the artist", "required": True},
            {"field_name": "commissioning_org_name", "field_type": "string", "description": "Name of the organization commissioning the work", "required": True},
            {"field_name": "engagement_type", "field_type": "string", "description": "Type of engagement (e.g., performance, installation, workshop, mural)", "required": True},
            {"field_name": "work_description", "field_type": "text", "description": "Detailed description of the work to be created or performed", "required": True},
            {"field_name": "venue_address", "field_type": "string", "description": "Address where the work will be presented", "required": True},
            {"field_name": "performance_dates", "field_type": "string", "description": "Dates and times of performance or installation period", "required": True},
            {"field_name": "compensation_amount", "field_type": "currency", "description": "Total compensation for the engagement in USD", "required": True},
            {"field_name": "materials_budget", "field_type": "currency", "description": "Budget for materials, separate from artist compensation", "required": False},
            {"field_name": "payment_schedule", "field_type": "text", "description": "Payment schedule (e.g., 50% upon signing, 50% upon completion)", "required": True},
            {"field_name": "cancellation_fee_pct", "field_type": "number", "description": "Percentage of compensation due if engagement is cancelled by commissioner", "required": True},
            {"field_name": "ip_retention", "field_type": "string", "description": "Who retains intellectual property rights (artist, commissioner, shared)", "required": True},
        ],
        "standard_terms": [
            "Artist shall retain all intellectual property rights to the work unless explicitly assigned in this Agreement.",
            "Commissioning Organization shall provide artist credit in all promotional materials, press releases, and public communications.",
            "Artist shall have the right to document the work for portfolio and promotional purposes.",
            "Commissioning Organization shall provide adequate technical support, including sound, lighting, and installation assistance as specified in the technical rider (Exhibit A).",
            "If the engagement is cancelled by the Commissioning Organization, the Artist shall receive the agreed cancellation fee regardless of the reason for cancellation.",
            "Artist shall comply with all site-specific safety requirements and applicable City of Philadelphia regulations.",
            "For installations, the Visual Artists Rights Act (VARA), 17 U.S.C. 106A, shall apply to the extent the work qualifies as a work of visual art.",
            "Commissioning Organization shall provide or reimburse reasonable travel and lodging expenses for artists residing outside the Philadelphia metropolitan area.",
        ],
        "negotiation_points": [
            "Compensation amount and payment schedule",
            "Intellectual property ownership and licensing",
            "Cancellation and force majeure terms",
            "Technical requirements and support",
            "Materials budget and procurement responsibility",
            "Duration of installation (if applicable)",
            "Moral rights and VARA protections",
            "Documentation and reproduction rights",
            "Exclusivity period",
        ],
        "philadelphia_specific_requirements": [
            "If the work is a mural, comply with the Philadelphia Mural Arts Program coordination requirements.",
            "If the artist is an independent contractor, Commissioning Organization must file a 1099-MISC for compensation exceeding $600.",
            "Public performances require a Public Entertainment Permit from Philadelphia L&I if admission is charged.",
            "Street performances on public rights-of-way must comply with Philadelphia Code Title 10, Chapter 10-600.",
            "Works installed in public space for more than 30 days may require approval from the Philadelphia Art Commission.",
        ],
        "estimated_legal_review_hours": 3,
        "template_text": """ARTIST AND PERFORMER ENGAGEMENT CONTRACT

THIS ENGAGEMENT CONTRACT ("Contract") is entered into as of the date last signed below (the "Effective Date"), by and between:

{{commissioning_org_name}} (the "Commissioner"); and

{{artist_name}}, an individual residing at {{artist_address}} (the "Artist").

RECITALS

WHEREAS, the Commissioner is organizing a public space activation at {{venue_address}}, Philadelphia, PA, and desires to engage the Artist to provide the services described herein; and

WHEREAS, the Artist possesses the skills, experience, and artistic vision necessary to create or perform the commissioned work;

NOW, THEREFORE, the Parties agree as follows:

ARTICLE 1 - SCOPE OF ENGAGEMENT

1.1. Engagement Type. The Commissioner hereby engages the Artist to provide the following: {{engagement_type}}.

1.2. Work Description. The Artist shall create or perform the following: {{work_description}}.

1.3. Schedule. The engagement shall take place on the following dates: {{performance_dates}}. Any changes to the schedule shall be mutually agreed upon in writing no fewer than fourteen (14) days in advance.

1.4. Technical Requirements. The Commissioner shall provide technical support as described in the Technical Rider attached as Exhibit A. The Commissioner shall ensure that the venue meets all safety and accessibility requirements under applicable law.

ARTICLE 2 - COMPENSATION

2.1. Fee. The Commissioner shall pay the Artist a total fee of {{compensation_amount}} USD for the engagement described herein.

2.2. Materials. In addition to the Artist's fee, the Commissioner shall provide a materials budget of {{materials_budget}} USD. The Artist shall provide receipts for all materials purchased. Unused materials budget shall be returned to the Commissioner.

2.3. Payment Schedule. Payment shall be made according to the following schedule: {{payment_schedule}}. All payments shall be made by check or electronic funds transfer within ten (10) business days of each milestone.

2.4. Taxes. The Artist acknowledges that they are engaged as an independent contractor and are solely responsible for all applicable taxes. The Commissioner shall issue a Form 1099-MISC for payments exceeding Six Hundred Dollars ($600) in a calendar year.

ARTICLE 3 - CANCELLATION

3.1. Cancellation by Commissioner. If the Commissioner cancels the engagement for any reason other than the Artist's material breach, the Artist shall be entitled to a cancellation fee equal to {{cancellation_fee_pct}}% of the total compensation.

3.2. Cancellation by Artist. If the Artist cancels the engagement without cause, the Artist shall refund all compensation received and shall reimburse the Commissioner for documented out-of-pocket expenses incurred in reliance on the engagement, up to a maximum of the total compensation amount.

3.3. Force Majeure. Neither Party shall be liable for cancellation caused by events beyond their reasonable control, including but not limited to acts of God, government orders, pandemic, or severe weather. In such cases, the Parties shall negotiate in good faith to reschedule or equitably adjust compensation.

ARTICLE 4 - INTELLECTUAL PROPERTY

4.1. Ownership. Intellectual property rights to the work created under this Contract shall be held as follows: {{ip_retention}}.

4.2. Artist Retained Rights. Regardless of the IP ownership arrangement, the Artist shall retain the right to: (a) be credited as the creator of the work in all contexts; (b) use images and documentation of the work in the Artist's portfolio and promotional materials; (c) exercise moral rights to the extent provided by applicable law, including the Visual Artists Rights Act (17 U.S.C. 106A).

4.3. Commissioner License. If the Artist retains IP ownership, the Commissioner shall receive a non-exclusive, perpetual, royalty-free license to use images of the work for promotional, educational, and archival purposes, with proper artist credit.

4.4. VARA Protections. If the work constitutes a "work of visual art" as defined by the Visual Artists Rights Act, the Commissioner shall not intentionally destroy, distort, mutilate, or modify the work without the Artist's written consent. If the work must be removed, the Commissioner shall provide the Artist ninety (90) days' notice and the opportunity to remove the work at the Artist's expense.

ARTICLE 5 - ARTIST CREDIT AND PROMOTION

5.1. Credit. The Commissioner shall credit the Artist by name in all promotional materials, press releases, social media posts, signage, and public communications related to the engagement.

5.2. Approval. The Artist shall have the right to approve any reproduction of the work used in promotional materials. Approval shall not be unreasonably withheld.

ARTICLE 6 - INSURANCE AND LIABILITY

6.1. The Commissioner shall maintain commercial general liability insurance of at least One Million Dollars ($1,000,000) per occurrence covering the engagement.

6.2. The Artist shall not be required to carry separate liability insurance unless the engagement involves activities that the Commissioner's policy does not cover, in which case the Commissioner shall reimburse the Artist for the cost of such coverage.

IN WITNESS WHEREOF, the Parties have executed this Contract as of the date last signed below.

COMMISSIONER: {{commissioning_org_name}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________

ARTIST: {{artist_name}}
Signature: _____________________
Date: _________________________""",
    },

    # -----------------------------------------------------------------------
    # 6. VENDOR AGREEMENT
    # -----------------------------------------------------------------------
    {
        "id": "vendor_agreement",
        "name": "Vendor Participation Agreement",
        "description": (
            "Governs the terms under which vendors, food trucks, artisans, and "
            "merchants may participate in a public space activation, market, or event. "
            "Covers fees, space allocation, operational requirements, and health and "
            "safety compliance."
        ),
        "category": "use",
        "parties_required": [
            "Market Operator / Event Organizer",
            "Vendor",
        ],
        "variable_fields": [
            {"field_name": "organizer_name", "field_type": "string", "description": "Legal name of the event organizer or market operator", "required": True},
            {"field_name": "vendor_name", "field_type": "string", "description": "Legal name of the vendor", "required": True},
            {"field_name": "vendor_business_type", "field_type": "string", "description": "Type of vendor business (e.g., food truck, artisan, retail)", "required": True},
            {"field_name": "vendor_products", "field_type": "text", "description": "Description of products or services the vendor will offer", "required": True},
            {"field_name": "event_name", "field_type": "string", "description": "Name of the market, festival, or activation", "required": True},
            {"field_name": "event_location", "field_type": "string", "description": "Address of the event", "required": True},
            {"field_name": "event_dates", "field_type": "string", "description": "Dates and hours of the event", "required": True},
            {"field_name": "booth_space_size", "field_type": "string", "description": "Dimensions of the assigned vendor space (e.g., 10x10 feet)", "required": True},
            {"field_name": "booth_fee", "field_type": "currency", "description": "Fee for the vendor space in USD", "required": True},
            {"field_name": "revenue_share_pct", "field_type": "number", "description": "Percentage of vendor gross sales paid to organizer, if any", "required": False},
            {"field_name": "setup_time", "field_type": "string", "description": "Permitted setup time before event opens", "required": True},
            {"field_name": "breakdown_time", "field_type": "string", "description": "Required breakdown completion time after event closes", "required": True},
        ],
        "standard_terms": [
            "Vendor shall operate only within the assigned booth space and shall not obstruct pedestrian pathways, fire lanes, or ADA-accessible routes.",
            "Vendor shall obtain and display all required City of Philadelphia licenses, including a Commercial Activity License and, for food vendors, a valid Philadelphia Department of Public Health food establishment permit.",
            "Vendor shall maintain the booth area in a clean and sanitary condition throughout the event and shall remove all products, equipment, and waste upon breakdown.",
            "Vendor shall carry commercial general liability insurance of at least $1,000,000 per occurrence, naming the Organizer and the City of Philadelphia as additional insureds.",
            "Vendor shall comply with all applicable Philadelphia Fire Code requirements, including restrictions on open flames, propane tanks, and cooking equipment.",
            "Vendor shall not sell or distribute any illegal substances, weapons, or items prohibited by Philadelphia Code.",
            "The Organizer reserves the right to remove any vendor who violates these terms or applicable law, without refund.",
            "Vendor shall not play amplified music or use loudspeakers without the Organizer's prior written consent.",
        ],
        "negotiation_points": [
            "Booth fee and payment terms",
            "Revenue sharing percentage",
            "Booth size and location preference",
            "Exclusivity for product category",
            "Power, water, and waste disposal access",
            "Weather cancellation and refund policy",
            "Multi-event discount",
            "Marketing and promotion inclusion",
        ],
        "philadelphia_specific_requirements": [
            "Food vendors must hold a valid Philadelphia Food Establishment Permit and display it prominently.",
            "All vendors must hold a valid Philadelphia Commercial Activity License (CAL).",
            "Food trucks must comply with Philadelphia Code Title 9, Chapter 9-600 (Mobile Food Vending).",
            "Vendors selling tobacco products must hold a Philadelphia Tobacco Retailer License.",
            "Sales tax must be collected and remitted to the Pennsylvania Department of Revenue.",
            "Vendors using propane or open flame must comply with Philadelphia Fire Prevention Code Section F-3801.",
        ],
        "estimated_legal_review_hours": 2,
        "template_text": """VENDOR PARTICIPATION AGREEMENT

THIS VENDOR PARTICIPATION AGREEMENT ("Agreement") is entered into as of the date last signed below, by and between:

{{organizer_name}} (the "Organizer"); and

{{vendor_name}}, operating as a {{vendor_business_type}} (the "Vendor").

RECITALS

WHEREAS, the Organizer is producing an event known as "{{event_name}}" at {{event_location}}, Philadelphia, PA (the "Event"); and

WHEREAS, the Vendor desires to participate in the Event by offering the following products or services: {{vendor_products}};

NOW, THEREFORE, the Parties agree as follows:

ARTICLE 1 - EVENT DETAILS AND VENDOR SPACE

1.1. Event Dates. The Event will take place on: {{event_dates}}.

1.2. Vendor Space. The Organizer assigns the Vendor a booth space of {{booth_space_size}} (the "Booth"). The specific location of the Booth within the Event grounds shall be determined by the Organizer and communicated to the Vendor no later than seven (7) days before the Event.

1.3. Setup and Breakdown. The Vendor may begin setup at {{setup_time}} and must complete breakdown by {{breakdown_time}}. Vendors remaining past the breakdown time may be assessed a fee of $100 per hour.

1.4. Utilities. The Organizer shall provide access to electrical power as specified in Exhibit A. Any additional utility needs are the Vendor's responsibility and must be approved in advance by the Organizer.

ARTICLE 2 - FEES AND REVENUE SHARING

2.1. Booth Fee. The Vendor shall pay a booth fee of {{booth_fee}} USD, due in full no later than fourteen (14) days before the first day of the Event. Fees are non-refundable except as provided in Section 5.

2.2. Revenue Share. In addition to the booth fee, the Vendor shall pay to the Organizer {{revenue_share_pct}}% of gross sales generated during the Event. The Vendor shall submit a certified sales report within five (5) business days following the Event, and payment of the revenue share shall accompany the report.

ARTICLE 3 - VENDOR OBLIGATIONS

3.1. Licensing. The Vendor shall obtain and maintain all licenses and permits required by the City of Philadelphia, the Commonwealth of Pennsylvania, and applicable federal agencies, including but not limited to a Commercial Activity License, sales tax license, and (for food vendors) a Philadelphia Department of Public Health Food Establishment Permit.

3.2. Insurance. The Vendor shall maintain commercial general liability insurance with limits of at least One Million Dollars ($1,000,000) per occurrence. The policy shall name the Organizer and the City of Philadelphia as additional insureds. Evidence of insurance shall be provided no later than seven (7) days before the Event.

3.3. Products. The Vendor shall sell only the products or services described in this Agreement. The Vendor shall not sell or distribute products that are illegal, unsafe, or in competition with an exclusive arrangement granted by the Organizer to another vendor.

3.4. Food Safety. Food vendors shall comply with all Philadelphia Department of Public Health regulations, including proper food handling, temperature control, handwashing, and allergen labeling requirements. The Vendor shall have at least one person on site who holds a valid ServSafe or equivalent food safety certification.

3.5. Appearance and Conduct. The Vendor shall maintain the Booth in a clean, safe, and visually appealing condition throughout the Event. The Vendor shall conduct business in a professional and courteous manner.

3.6. Waste Management. The Vendor shall remove all waste generated by its operations and shall use the designated waste and recycling stations provided by the Organizer.

ARTICLE 4 - ORGANIZER OBLIGATIONS

4.1. The Organizer shall provide the Booth space as described, adequate pedestrian traffic management, event marketing and promotion, and access to common facilities (restrooms, waste stations).

4.2. The Organizer shall maintain commercial general liability insurance of at least Two Million Dollars ($2,000,000) covering the Event.

ARTICLE 5 - CANCELLATION AND WEATHER

5.1. Cancellation by Organizer. If the Organizer cancels the Event for reasons other than force majeure, the Vendor shall receive a full refund of the booth fee.

5.2. Weather. If the Event is cancelled or shortened due to severe weather as determined by the National Weather Service, the Organizer shall offer the Vendor a pro-rated credit toward a future event. No cash refunds shall be issued for weather-related cancellations.

5.3. Cancellation by Vendor. If the Vendor cancels fewer than seven (7) days before the Event, the booth fee is forfeited in full.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the date last signed below.

ORGANIZER: {{organizer_name}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________

VENDOR: {{vendor_name}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________""",
    },

    # -----------------------------------------------------------------------
    # 7. SPONSORSHIP AGREEMENT
    # -----------------------------------------------------------------------
    {
        "id": "sponsorship_agreement",
        "name": "Sponsorship Agreement",
        "description": (
            "Governs corporate or organizational sponsorship of a public space "
            "activation, including sponsorship tiers, branding rights, activation "
            "rights, and community benefit obligations of sponsors."
        ),
        "category": "financial",
        "parties_required": [
            "Sponsee (Activation Organization)",
            "Sponsor (Corporate or Organizational Sponsor)",
        ],
        "variable_fields": [
            {"field_name": "sponsee_name", "field_type": "string", "description": "Name of the organization receiving sponsorship", "required": True},
            {"field_name": "sponsor_name", "field_type": "string", "description": "Name of the sponsoring entity", "required": True},
            {"field_name": "event_or_program_name", "field_type": "string", "description": "Name of the event, program, or activation being sponsored", "required": True},
            {"field_name": "sponsorship_level", "field_type": "string", "description": "Tier of sponsorship (e.g., Title, Presenting, Supporting, Community)", "required": True},
            {"field_name": "sponsorship_amount", "field_type": "currency", "description": "Total sponsorship contribution in USD", "required": True},
            {"field_name": "in_kind_value", "field_type": "currency", "description": "Estimated value of in-kind contributions, if any", "required": False},
            {"field_name": "in_kind_description", "field_type": "text", "description": "Description of in-kind goods or services provided", "required": False},
            {"field_name": "sponsorship_term_start", "field_type": "date", "description": "Start of the sponsorship term", "required": True},
            {"field_name": "sponsorship_term_end", "field_type": "date", "description": "End of the sponsorship term", "required": True},
            {"field_name": "branding_rights_description", "field_type": "text", "description": "Detailed description of branding and recognition benefits", "required": True},
            {"field_name": "exclusivity_category", "field_type": "string", "description": "Product or service category in which the sponsor has exclusivity, if any", "required": False},
        ],
        "standard_terms": [
            "Sponsee shall provide all branding benefits described in the sponsorship package within the agreed-upon timeline.",
            "Sponsor's logo, name, and branding shall not imply governmental endorsement by the City of Philadelphia.",
            "Sponsee reserves the right to decline sponsorship from entities whose products or business practices conflict with the public interest mission of the activation.",
            "Sponsor shall not engage in direct sales or marketing to event attendees beyond the scope agreed in this Agreement without prior written consent.",
            "Sponsee shall provide a post-event impact report including attendance data, media impressions, and community engagement metrics within 60 days of the event's conclusion.",
            "Neither Party may assign this Agreement without the other Party's prior written consent.",
        ],
        "negotiation_points": [
            "Sponsorship amount and payment schedule",
            "Branding placement, size, and prominence",
            "Category exclusivity",
            "On-site activation rights (sampling, displays, engagement)",
            "Digital and social media mentions",
            "VIP hospitality and ticket allocations",
            "Right of first refusal for future sponsorship",
            "Naming rights",
            "Community benefit tie-in requirements",
        ],
        "philadelphia_specific_requirements": [
            "Sponsorship signage on public property must comply with Philadelphia Zoning Code sign regulations (Title 14, Chapter 14-900).",
            "Alcohol brand sponsorship must comply with Pennsylvania Liquor Control Board advertising regulations.",
            "Sponsorship of events in Fairmount Park requires approval from Philadelphia Parks & Recreation.",
            "Naming rights for public spaces require approval by Philadelphia City Council ordinance.",
            "Tobacco and e-cigarette brand sponsorship is prohibited for events receiving City of Philadelphia funding or support.",
        ],
        "estimated_legal_review_hours": 4,
        "template_text": """SPONSORSHIP AGREEMENT

THIS SPONSORSHIP AGREEMENT ("Agreement") is entered into as of the date last signed below, by and between:

{{sponsee_name}} (the "Sponsee"); and

{{sponsor_name}} (the "Sponsor").

RECITALS

WHEREAS, the Sponsee is organizing and producing "{{event_or_program_name}}" (the "Program"), a public space activation in the City of Philadelphia; and

WHEREAS, the Sponsor desires to support the Program and to receive certain recognition and branding benefits in connection therewith;

NOW, THEREFORE, the Parties agree as follows:

ARTICLE 1 - SPONSORSHIP TERMS

1.1. Level. The Sponsor is engaged at the "{{sponsorship_level}}" sponsorship level.

1.2. Term. This sponsorship shall be effective from {{sponsorship_term_start}} through {{sponsorship_term_end}}.

1.3. Financial Contribution. The Sponsor shall contribute {{sponsorship_amount}} USD, payable as follows: fifty percent (50%) within fifteen (15) days of execution of this Agreement and the remaining fifty percent (50%) no later than thirty (30) days before the first event date.

1.4. In-Kind Contributions. In addition to the financial contribution, the Sponsor shall provide the following in-kind goods or services, with an estimated value of {{in_kind_value}} USD: {{in_kind_description}}.

ARTICLE 2 - SPONSOR BENEFITS

2.1. Branding and Recognition. The Sponsee shall provide the following branding and recognition benefits: {{branding_rights_description}}.

2.2. Exclusivity. The Sponsor shall have category exclusivity in the following product or service category: {{exclusivity_category}}. The Sponsee shall not accept sponsorship from a direct competitor of the Sponsor in this category during the term of this Agreement.

2.3. On-Site Activation. The Sponsor shall have the right to conduct on-site activation activities as mutually agreed upon and described in Exhibit A. All on-site activities must comply with applicable City of Philadelphia regulations and the Sponsee's community standards.

2.4. No Governmental Endorsement. The Sponsor acknowledges that its association with the Program does not constitute an endorsement by the City of Philadelphia, and the Sponsor shall not represent or imply otherwise in any marketing or communications.

ARTICLE 3 - SPONSOR OBLIGATIONS

3.1. Brand Standards. The Sponsor shall provide the Sponsee with approved logos, brand guidelines, and any required legal disclaimers within ten (10) days of executing this Agreement.

3.2. Community Alignment. The Sponsor acknowledges that the Program is rooted in community service and public benefit. The Sponsor shall not engage in activities during the Program that are inconsistent with the Program's community-serving mission.

3.3. Compliance. All Sponsor activities at the Program shall comply with applicable federal, state, and City of Philadelphia laws and regulations, including signage regulations under Philadelphia Zoning Code Title 14, Chapter 14-900.

ARTICLE 4 - SPONSEE OBLIGATIONS

4.1. Delivery. The Sponsee shall deliver all sponsorship benefits as described herein and in the attached Exhibit A.

4.2. Impact Report. Within sixty (60) days of the Program's conclusion, the Sponsee shall provide the Sponsor with a post-event impact report including: (a) total attendance; (b) media coverage summary; (c) social media metrics; (d) photographs of sponsor branding in situ; and (e) community impact narrative.

4.3. Insurance. The Sponsee shall maintain commercial general liability insurance of at least One Million Dollars ($1,000,000) per occurrence and shall name the Sponsor as additional insured upon request.

ARTICLE 5 - TERMINATION

5.1. Either Party may terminate this Agreement upon thirty (30) days' written notice if the other Party materially breaches any provision and fails to cure within fifteen (15) days of notice.

5.2. The Sponsee may terminate this Agreement immediately if the Sponsor engages in conduct that materially damages the reputation or community relationships of the Program.

5.3. Upon termination by the Sponsee without cause, the Sponsee shall refund any portion of the sponsorship contribution attributable to undelivered benefits.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the date last signed below.

SPONSEE: {{sponsee_name}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________

SPONSOR: {{sponsor_name}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________""",
    },

    # -----------------------------------------------------------------------
    # 8. INSURANCE RIDER
    # -----------------------------------------------------------------------
    {
        "id": "insurance_rider",
        "name": "Insurance Rider for Public Space Activation",
        "description": (
            "A supplemental insurance document that extends an existing commercial "
            "general liability policy to cover specific public space activation "
            "activities, names the City of Philadelphia as additional insured, and "
            "confirms compliance with City insurance requirements."
        ),
        "category": "insurance",
        "parties_required": [
            "Named Insured (Activation Partner / Licensee)",
            "Insurance Carrier",
            "Additional Insured (City of Philadelphia)",
        ],
        "variable_fields": [
            {"field_name": "named_insured", "field_type": "string", "description": "Legal name of the policyholder", "required": True},
            {"field_name": "policy_number", "field_type": "string", "description": "Existing CGL policy number", "required": True},
            {"field_name": "insurance_carrier", "field_type": "string", "description": "Name of the insurance carrier", "required": True},
            {"field_name": "carrier_naic_number", "field_type": "string", "description": "NAIC number of the insurance carrier", "required": True},
            {"field_name": "site_address", "field_type": "string", "description": "Address of the activation site to be covered", "required": True},
            {"field_name": "coverage_start_date", "field_type": "date", "description": "Start date of additional coverage", "required": True},
            {"field_name": "coverage_end_date", "field_type": "date", "description": "End date of additional coverage", "required": True},
            {"field_name": "per_occurrence_limit", "field_type": "currency", "description": "Per-occurrence coverage limit (minimum $1,000,000)", "required": True},
            {"field_name": "aggregate_limit", "field_type": "currency", "description": "Aggregate coverage limit (minimum $2,000,000)", "required": True},
            {"field_name": "additional_coverage_types", "field_type": "text", "description": "Any additional coverage types (e.g., liquor liability, auto, umbrella)", "required": False},
            {"field_name": "activities_covered", "field_type": "text", "description": "Description of specific activities covered under this rider", "required": True},
            {"field_name": "additional_premium", "field_type": "currency", "description": "Additional premium for this rider, if any", "required": False},
        ],
        "standard_terms": [
            "This rider supplements and does not replace the Named Insured's existing commercial general liability policy.",
            "The City of Philadelphia, its elected officials, officers, employees, agents, and volunteers are named as additional insureds with respect to liability arising out of the Named Insured's activities at the specified site.",
            "Coverage shall be primary and non-contributory with respect to the additional insured's own insurance.",
            "A waiver of subrogation is granted in favor of the City of Philadelphia.",
            "The insurance carrier shall provide the City of Philadelphia's Risk Management Division with at least thirty (30) days' written notice prior to cancellation, non-renewal, or material change in coverage.",
            "This rider shall not be construed to expand coverage beyond the terms, conditions, and exclusions of the underlying policy, except as expressly stated herein.",
        ],
        "negotiation_points": [
            "Coverage limits above City minimums",
            "Additional coverage types (liquor liability, professional liability, cyber)",
            "Premium allocation",
            "Deductible and self-insured retention amounts",
            "Scope of activities covered",
            "Duration of coverage",
        ],
        "philadelphia_specific_requirements": [
            "Minimum coverage of $1,000,000 per occurrence and $2,000,000 aggregate as required by the City of Philadelphia Risk Management Division.",
            "Insurance carrier must be licensed to do business in the Commonwealth of Pennsylvania.",
            "Insurance carrier must hold an A.M. Best rating of A- VII or better.",
            "Certificate of insurance must be filed with the City's Risk Management Division at 1515 Arch Street, 14th Floor, Philadelphia, PA 19102.",
            "For events serving alcohol, a separate liquor liability policy or endorsement with minimum coverage of $1,000,000 is required.",
            "For events involving vehicles, automobile liability coverage of $1,000,000 combined single limit is required.",
        ],
        "estimated_legal_review_hours": 2,
        "template_text": """INSURANCE RIDER FOR PUBLIC SPACE ACTIVATION

RIDER NUMBER: [To be assigned]
EFFECTIVE DATE: {{coverage_start_date}}
EXPIRATION DATE: {{coverage_end_date}}

THIS RIDER is attached to and forms part of Policy No. {{policy_number}} issued by {{insurance_carrier}} (NAIC No. {{carrier_naic_number}}) to:

NAMED INSURED: {{named_insured}}

This Rider amends the above-referenced policy to provide coverage for public space activation activities as described herein.

SECTION 1 - COVERED LOCATION

The following location is added as a covered premises under this policy:

{{site_address}}, Philadelphia, PA

SECTION 2 - COVERED ACTIVITIES

This Rider extends coverage to the following activities conducted at the Covered Location during the period of this Rider:

{{activities_covered}}

SECTION 3 - ADDITIONAL INSURED

The following are added as Additional Insureds under this policy, but only with respect to liability arising out of the Named Insured's activities at the Covered Location:

    The City of Philadelphia
    Its elected and appointed officials
    Its officers, employees, agents, and volunteers
    Acting in their official capacities

    Address for notices:
    City of Philadelphia, Risk Management Division
    1515 Arch Street, 14th Floor
    Philadelphia, PA 19102

SECTION 4 - LIMITS OF LIABILITY

The following limits apply to this Rider:

    Each Occurrence Limit:           {{per_occurrence_limit}} USD
    General Aggregate Limit:         {{aggregate_limit}} USD
    Products/Completed Operations:   {{per_occurrence_limit}} USD
    Personal & Advertising Injury:   {{per_occurrence_limit}} USD
    Damage to Rented Premises:       $100,000
    Medical Payments:                $5,000 per person

Additional Coverage (if applicable): {{additional_coverage_types}}

These limits are part of, and not in addition to, the limits of the underlying policy, unless otherwise endorsed.

SECTION 5 - CONDITIONS

5.1. Primary and Non-Contributory. The coverage afforded to the Additional Insured under this Rider shall be primary coverage. Any insurance or self-insurance maintained by the City of Philadelphia shall be excess and non-contributing.

5.2. Waiver of Subrogation. The Named Insured and the Insurance Carrier waive any right of subrogation against the City of Philadelphia, its elected officials, officers, employees, agents, and volunteers, but only with respect to claims arising out of the Named Insured's activities at the Covered Location.

5.3. Notice of Cancellation. The Insurance Carrier shall provide the City of Philadelphia's Risk Management Division with no fewer than thirty (30) days' advance written notice of cancellation, non-renewal, or material reduction in coverage. In the event of cancellation for non-payment of premium, ten (10) days' notice shall be provided.

5.4. Severability of Interests. The insurance afforded under this Rider applies separately to each insured against whom a claim is made or suit is brought, except with respect to the limits of liability.

5.5. Carrier Rating. The Insurance Carrier represents that it holds a current A.M. Best rating of no less than A- VII and is licensed to conduct insurance business in the Commonwealth of Pennsylvania.

SECTION 6 - PREMIUM

Additional Premium for this Rider: {{additional_premium}} USD

All other terms, conditions, and exclusions of the underlying policy remain unchanged.

AUTHORIZED REPRESENTATIVE:
Insurance Carrier: {{insurance_carrier}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________

NAMED INSURED: {{named_insured}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________""",
    },

    # -----------------------------------------------------------------------
    # 9. INDEMNIFICATION AGREEMENT
    # -----------------------------------------------------------------------
    {
        "id": "indemnification_agreement",
        "name": "Indemnification and Hold Harmless Agreement",
        "description": (
            "A standalone indemnification agreement in which one party agrees to "
            "defend, indemnify, and hold harmless another party from claims arising "
            "out of the indemnitor's use of public space. Used when a full activation "
            "agreement is not warranted or as a supplement to existing agreements."
        ),
        "category": "insurance",
        "parties_required": [
            "Indemnitor (Party Using the Space)",
            "Indemnitee (City of Philadelphia or Property Owner)",
        ],
        "variable_fields": [
            {"field_name": "indemnitor_name", "field_type": "string", "description": "Legal name of the party providing indemnification", "required": True},
            {"field_name": "indemnitor_address", "field_type": "string", "description": "Address of the indemnitor", "required": True},
            {"field_name": "indemnitee_name", "field_type": "string", "description": "Legal name of the party being indemnified", "required": True},
            {"field_name": "site_address", "field_type": "string", "description": "Address of the property being used", "required": True},
            {"field_name": "activity_description", "field_type": "text", "description": "Description of the activities giving rise to the indemnification obligation", "required": True},
            {"field_name": "indemnification_start_date", "field_type": "date", "description": "Start date of the indemnification period", "required": True},
            {"field_name": "indemnification_end_date", "field_type": "date", "description": "End date of the indemnification period", "required": True},
            {"field_name": "indemnification_cap", "field_type": "currency", "description": "Maximum aggregate liability under this indemnification, if any", "required": False},
            {"field_name": "insurance_required", "field_type": "string", "description": "Whether insurance backing is required (yes or no)", "required": True},
            {"field_name": "insurance_minimum", "field_type": "currency", "description": "Minimum insurance coverage required to back indemnification", "required": False},
        ],
        "standard_terms": [
            "Indemnitor shall defend, indemnify, and hold harmless the Indemnitee from and against any and all claims, demands, actions, suits, damages, liabilities, losses, settlements, judgments, costs, and expenses, including reasonable attorneys' fees and costs, arising out of or in connection with the Indemnitor's use of the premises.",
            "The indemnification obligation shall extend to claims arising from the negligence or willful misconduct of the Indemnitor, its employees, agents, contractors, invitees, and licensees.",
            "The indemnification obligation shall NOT extend to claims arising from the sole negligence or willful misconduct of the Indemnitee.",
            "Indemnitor's obligation to defend shall arise upon tender of defense by the Indemnitee and shall include the selection of counsel reasonably acceptable to the Indemnitee.",
            "The indemnification obligation shall survive the expiration or termination of any underlying use agreement for a period of three (3) years.",
            "This Agreement shall be governed by and construed in accordance with the laws of the Commonwealth of Pennsylvania.",
        ],
        "negotiation_points": [
            "Scope of indemnification (broad form vs. intermediate form)",
            "Cap on indemnification liability",
            "Survival period after agreement termination",
            "Insurance backing requirements",
            "Whether indemnification covers Indemnitee's own negligence (comparative fault)",
            "Defense obligation and counsel selection",
            "Waiver of governmental immunity provisions",
        ],
        "philadelphia_specific_requirements": [
            "The City of Philadelphia does not waive governmental immunity except as provided by the Pennsylvania Political Subdivision Tort Claims Act (42 Pa.C.S. 8541 et seq.).",
            "Indemnification of the City must be consistent with the Philadelphia Home Rule Charter.",
            "If the Indemnitor is a nonprofit, the indemnification must be within the scope of the organization's insured activities.",
            "Indemnification agreements involving City property must be reviewed and approved by the City's Law Department.",
        ],
        "estimated_legal_review_hours": 3,
        "template_text": """INDEMNIFICATION AND HOLD HARMLESS AGREEMENT

THIS INDEMNIFICATION AND HOLD HARMLESS AGREEMENT ("Agreement") is entered into as of the date last signed below (the "Effective Date"), by and between:

INDEMNITOR: {{indemnitor_name}}, with an address at {{indemnitor_address}} (the "Indemnitor");

and

INDEMNITEE: {{indemnitee_name}} (the "Indemnitee").

RECITALS

WHEREAS, the Indemnitor intends to use, occupy, or conduct activities upon certain real property located at {{site_address}}, Philadelphia, PA (the "Premises"); and

WHEREAS, the Indemnitee is the owner, manager, or authorized custodian of the Premises; and

WHEREAS, the Indemnitee requires indemnification as a condition of permitting the Indemnitor's use of the Premises;

NOW, THEREFORE, in consideration of the Indemnitee's permission to use the Premises, the Indemnitor agrees as follows:

ARTICLE 1 - SCOPE OF ACTIVITIES

1.1. This Agreement covers the following activities conducted by the Indemnitor at the Premises: {{activity_description}}.

1.2. The indemnification period shall commence on {{indemnification_start_date}} and shall expire on {{indemnification_end_date}}, subject to the survival provisions of Article 4.

ARTICLE 2 - INDEMNIFICATION

2.1. General Indemnification. The Indemnitor shall defend, indemnify, and hold harmless the Indemnitee, its elected and appointed officials, officers, employees, agents, and volunteers (collectively, the "Indemnified Parties") from and against any and all claims, demands, actions, suits, proceedings, damages, liabilities, losses, settlements, judgments, penalties, fines, costs, and expenses, including but not limited to reasonable attorneys' fees, expert witness fees, and court costs (collectively, "Losses"), arising out of, resulting from, or in connection with:

    (a) The Indemnitor's use, occupancy, or presence on the Premises;
    (b) Any act or omission of the Indemnitor, its employees, agents, contractors, subcontractors, invitees, guests, or licensees;
    (c) Any breach of this Agreement by the Indemnitor;
    (d) Any violation of applicable law by the Indemnitor;
    (e) Any injury to or death of any person, or damage to or destruction of any property, occurring on or about the Premises during the indemnification period and arising from the Indemnitor's activities.

2.2. Comparative Fault. The Indemnitor's obligation under this Article extends to Losses caused in whole or in part by the negligence of the Indemnitor, but shall NOT extend to Losses caused by the sole negligence or willful misconduct of the Indemnitee.

2.3. Cap on Liability. The Indemnitor's aggregate liability under this Agreement shall not exceed {{indemnification_cap}} USD. If no cap is specified, the Indemnitor's liability shall be unlimited to the extent permitted by law.

ARTICLE 3 - DEFENSE OBLIGATION

3.1. Duty to Defend. Upon receipt of written notice from any Indemnified Party of a claim or threatened claim covered by this Agreement, the Indemnitor shall, at its sole expense, assume the defense of such claim using legal counsel reasonably acceptable to the Indemnitee.

3.2. Cooperation. The Indemnitee shall cooperate with the Indemnitor in the defense of any claim, including making available relevant documents and personnel. The Indemnitee shall have the right to participate in the defense at its own expense.

3.3. Settlement. The Indemnitor shall not settle any claim without the prior written consent of the Indemnitee if the settlement involves any admission of liability by the Indemnitee, any injunctive or non-monetary relief affecting the Indemnitee, or any payment by the Indemnitee.

ARTICLE 4 - SURVIVAL

4.1. The indemnification obligations of the Indemnitor under this Agreement shall survive the expiration or earlier termination of this Agreement and any underlying use agreement for a period of three (3) years following the last day of the indemnification period.

ARTICLE 5 - INSURANCE

5.1. Insurance Requirement. Insurance backing is {{insurance_required}} for this indemnification.

5.2. If insurance is required, the Indemnitor shall obtain and maintain commercial general liability insurance with minimum limits of {{insurance_minimum}} USD per occurrence, naming the Indemnified Parties as additional insureds. The policy shall provide coverage for the indemnification obligations assumed under this Agreement.

5.3. Evidence of insurance shall be delivered to the Indemnitee prior to the commencement of any activities on the Premises.

ARTICLE 6 - GENERAL PROVISIONS

6.1. Governing Law. This Agreement shall be governed by the laws of the Commonwealth of Pennsylvania.

6.2. Venue. Any action arising under this Agreement shall be brought in the Court of Common Pleas of Philadelphia County or the United States District Court for the Eastern District of Pennsylvania.

6.3. Severability. If any provision of this Agreement is held invalid or unenforceable, the remaining provisions shall remain in full force and effect.

6.4. Entire Agreement. This Agreement constitutes the entire agreement between the Parties regarding indemnification for the activities described herein.

6.5. Governmental Immunity. Nothing in this Agreement shall be construed as a waiver of any immunity or defense available to the City of Philadelphia under the Pennsylvania Political Subdivision Tort Claims Act (42 Pa.C.S. 8541 et seq.) or any other applicable law.

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the date last signed below.

INDEMNITOR: {{indemnitor_name}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________

INDEMNITEE: {{indemnitee_name}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________""",
    },

    # -----------------------------------------------------------------------
    # 10. PERMANENCE CLAUSE ADDENDUM
    # -----------------------------------------------------------------------
    {
        "id": "permanence_clause_addendum",
        "name": "Permanence Clause Addendum",
        "description": (
            "An addendum to any public space activation agreement that details "
            "the specific permanence commitments, milestones, verification procedures, "
            "and enforcement mechanisms ensuring that a minimum of 25% of project "
            "value creates lasting community benefit."
        ),
        "category": "permanence",
        "parties_required": [
            "Activation Partner (Organization Making Permanence Commitments)",
            "City of Philadelphia (Permanence Verification Authority)",
            "Community Advisory Body (Verification Participant)",
        ],
        "variable_fields": [
            {"field_name": "activation_partner_name", "field_type": "string", "description": "Legal name of the organization making permanence commitments", "required": True},
            {"field_name": "underlying_agreement_date", "field_type": "date", "description": "Date of the underlying activation agreement this addendum modifies", "required": True},
            {"field_name": "underlying_agreement_title", "field_type": "string", "description": "Title of the underlying agreement", "required": True},
            {"field_name": "site_address", "field_type": "string", "description": "Address of the activation site", "required": True},
            {"field_name": "total_project_value", "field_type": "currency", "description": "Total project value (basis for permanence percentage calculation)", "required": True},
            {"field_name": "permanence_commitment_pct", "field_type": "number", "description": "Percentage of project value committed to permanence (minimum 25%)", "required": True},
            {"field_name": "permanence_dollar_value", "field_type": "currency", "description": "Dollar value of permanence commitment", "required": True},
            {"field_name": "physical_improvement_description", "field_type": "text", "description": "Description of physical improvement commitments, if any", "required": False},
            {"field_name": "community_asset_description", "field_type": "text", "description": "Description of community asset creation commitments, if any", "required": False},
            {"field_name": "knowledge_transfer_description", "field_type": "text", "description": "Description of knowledge transfer commitments, if any", "required": False},
            {"field_name": "economic_legacy_description", "field_type": "text", "description": "Description of economic legacy commitments, if any", "required": False},
            {"field_name": "environmental_improvement_description", "field_type": "text", "description": "Description of environmental improvement commitments, if any", "required": False},
            {"field_name": "verification_date", "field_type": "date", "description": "Date by which permanence commitments must be verified as complete", "required": True},
            {"field_name": "community_advisory_body_name", "field_type": "string", "description": "Name of the community advisory body participating in verification", "required": True},
        ],
        "standard_terms": [
            "The Activation Partner commits to allocating no less than the stated percentage of total project value toward permanent community benefit as defined in the Permanence Framework.",
            "Permanence investments must span at least two (2) of the five permanence categories: Physical Improvement, Community Asset Creation, Knowledge Transfer, Economic Legacy, and Environmental Improvement.",
            "The Activation Partner shall submit a detailed Permanence Plan within thirty (30) days of executing this Addendum, itemizing each permanence investment with projected cost, timeline, and measurable outcomes.",
            "Permanence investments shall be verified by a joint inspection conducted by the City, the Community Advisory Body, and an independent evaluator selected by the City.",
            "If the Activation Partner fails to meet its permanence commitments by the verification date, liquidated damages equal to the shortfall amount shall be payable to the City's Public Space Permanence Fund.",
            "All physical improvements shall be warranted by the Activation Partner for a minimum of five (5) years following installation.",
            "Knowledge transfer assets (curricula, toolkits, archives) shall be licensed under a Creative Commons Attribution-ShareAlike 4.0 International License or equivalent open license.",
            "The Activation Partner shall provide annual permanence status reports for five (5) years following completion.",
        ],
        "negotiation_points": [
            "Permanence percentage above the 25% minimum",
            "Distribution across permanence categories",
            "Timeline for permanence investments",
            "Verification procedures and evaluator selection",
            "Liquidated damages formula",
            "Warranty period for physical improvements",
            "Intellectual property licensing for knowledge transfer assets",
            "Long-term maintenance obligations",
        ],
        "philadelphia_specific_requirements": [
            "Physical improvements on City property must be approved by the relevant managing department (Parks & Recreation, Streets, etc.).",
            "Permanent installations in public view are subject to review by the Philadelphia Art Commission.",
            "Environmental improvements must comply with Philadelphia Green City, Clean Waters regulations.",
            "Community asset funds must be deposited with a Philadelphia-chartered financial institution.",
            "Knowledge transfer archives intended for public access should be coordinated with the Free Library of Philadelphia or the Philadelphia City Archives.",
            "All permanence investments must be documented in a format compatible with the City's capital asset tracking system.",
        ],
        "estimated_legal_review_hours": 6,
        "template_text": """PERMANENCE CLAUSE ADDENDUM

THIS PERMANENCE CLAUSE ADDENDUM ("Addendum") is attached to and incorporated into that certain agreement entitled "{{underlying_agreement_title}}" dated {{underlying_agreement_date}} (the "Underlying Agreement"), by and among:

{{activation_partner_name}} (the "Activation Partner");

THE CITY OF PHILADELPHIA, acting through its Office of Arts, Culture and the Creative Economy and relevant managing departments (the "City"); and

{{community_advisory_body_name}} (the "Community Advisory Body").

RECITALS

WHEREAS, the Underlying Agreement governs the activation of public space at {{site_address}}, Philadelphia, PA (the "Site"); and

WHEREAS, the Parties are committed to ensuring that public space activations create lasting, permanent value for the communities they serve; and

WHEREAS, the Permanence Framework established by the City requires that no less than twenty-five percent (25%) of total project value be allocated toward permanent community benefit;

NOW, THEREFORE, the Parties agree to the following permanence commitments:

ARTICLE 1 - PERMANENCE COMMITMENT

1.1. Commitment Amount. The total value of the project governed by the Underlying Agreement is {{total_project_value}} USD. The Activation Partner commits to allocating {{permanence_commitment_pct}}% of this value - equal to {{permanence_dollar_value}} USD - toward permanent community benefit as defined in this Addendum.

1.2. Minimum Threshold. In no event shall the permanence commitment be less than twenty-five percent (25%) of total project value. If the stated percentage is less than 25%, it shall be deemed to be 25%.

1.3. Multi-Category Requirement. Permanence investments must span at least two (2) of the five categories defined in Article 2.

ARTICLE 2 - PERMANENCE CATEGORIES AND COMMITMENTS

The Activation Partner shall invest in the following permanence categories:

2.1. Physical Improvement.
Physical improvements are tangible, lasting improvements to the Site or surrounding public infrastructure that remain after the activation period ends.
Commitment: {{physical_improvement_description}}

2.2. Community Asset Creation.
Community assets are organizational, programmatic, or institutional resources that strengthen the community's capacity for self-governance and continued public space activation.
Commitment: {{community_asset_description}}

2.3. Knowledge Transfer.
Knowledge transfer includes structured programs that build skills, share expertise, and create documented knowledge resources accessible to the public in perpetuity.
Commitment: {{knowledge_transfer_description}}

2.4. Economic Legacy.
Economic legacy includes lasting economic structures, revenue streams, or employment pathways that continue to benefit the community beyond the activation period.
Commitment: {{economic_legacy_description}}

2.5. Environmental Improvement.
Environmental improvements are measurable improvements to air, water, soil, biodiversity, or climate resilience that persist beyond the project.
Commitment: {{environmental_improvement_description}}

ARTICLE 3 - PERMANENCE PLAN

3.1. Submission. Within thirty (30) days of executing this Addendum, the Activation Partner shall submit a detailed Permanence Plan to the City and the Community Advisory Body. The Permanence Plan shall include:
    (a) Itemized list of each permanence investment;
    (b) The permanence category for each investment;
    (c) Projected cost for each investment;
    (d) Timeline and milestones for each investment;
    (e) Measurable outcomes and success criteria for each investment;
    (f) Maintenance plan for physical improvements;
    (g) Licensing terms for knowledge transfer assets.

3.2. Approval. The City shall review and approve the Permanence Plan within thirty (30) days of submission. The City may request modifications to ensure the plan meets the requirements of this Addendum.

ARTICLE 4 - VERIFICATION

4.1. Verification Date. All permanence commitments must be substantially complete by {{verification_date}}.

4.2. Verification Process. Verification shall be conducted by a joint inspection team comprising:
    (a) A representative of the City's Office of Arts, Culture and the Creative Economy;
    (b) A representative of the relevant City managing department;
    (c) Two representatives of the Community Advisory Body;
    (d) An independent evaluator selected and funded by the City.

4.3. Verification Report. The inspection team shall produce a Verification Report within thirty (30) days of the inspection, documenting: (a) each permanence investment; (b) its completion status; (c) its estimated value; (d) its conformity with the approved Permanence Plan; and (e) any deficiencies.

4.4. Cure Period. If the Verification Report identifies deficiencies, the Activation Partner shall have sixty (60) days to cure such deficiencies and request a follow-up inspection.

ARTICLE 5 - ENFORCEMENT

5.1. Liquidated Damages. If the Activation Partner fails to meet its permanence commitments by the end of the cure period, the Activation Partner shall pay liquidated damages equal to the dollar value of the shortfall (the difference between the committed permanence value and the verified permanence value). Liquidated damages shall be payable to the City of Philadelphia's Public Space Permanence Fund within thirty (30) days of the final Verification Report.

5.2. The Parties agree that the liquidated damages amount is a reasonable estimate of the damages the City and community would suffer from the failure to realize permanent value, and is not a penalty.

ARTICLE 6 - WARRANTIES AND MAINTENANCE

6.1. Physical Improvement Warranty. The Activation Partner warrants all physical improvements against defects in materials and workmanship for a period of five (5) years from the date of installation. During the warranty period, the Activation Partner shall repair or replace defective improvements at its sole expense.

6.2. Maintenance Plan. The Activation Partner shall submit a five-year maintenance plan for all physical improvements. The maintenance plan shall identify responsible parties, estimated annual costs, and funding sources.

6.3. Transfer of Maintenance. Upon expiration of the warranty period, maintenance responsibility for physical improvements shall transfer to the City, unless the Parties agree otherwise in writing. The Activation Partner shall ensure that maintenance endowment or reserve funds, if any, are fully funded at the time of transfer.

ARTICLE 7 - INTELLECTUAL PROPERTY AND OPEN ACCESS

7.1. Knowledge transfer assets created under this Addendum - including but not limited to curricula, toolkits, research reports, oral histories, and training materials - shall be licensed under a Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0) or an equivalent open license approved by the City.

7.2. Digital copies of all knowledge transfer assets shall be deposited with the Free Library of Philadelphia and/or the Philadelphia City Archives within ninety (90) days of completion.

ARTICLE 8 - ANNUAL REPORTING

8.1. The Activation Partner shall provide annual permanence status reports to the City and the Community Advisory Body for five (5) years following the Verification Date. Reports shall include: (a) condition of physical improvements; (b) utilization of community assets; (c) access and usage metrics for knowledge transfer assets; (d) economic impact data; (e) environmental monitoring data.

ARTICLE 9 - GENERAL

9.1. Conflict. In the event of any conflict between this Addendum and the Underlying Agreement, the terms of this Addendum shall control with respect to permanence commitments.

9.2. Binding Effect. This Addendum is binding on the Parties and their successors and assigns.

9.3. Governing Law. This Addendum shall be governed by the laws of the Commonwealth of Pennsylvania.

IN WITNESS WHEREOF, the Parties have executed this Addendum as of the date last signed below.

ACTIVATION PARTNER: {{activation_partner_name}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________

CITY OF PHILADELPHIA
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________

COMMUNITY ADVISORY BODY: {{community_advisory_body_name}}
By: ___________________________
Name: _________________________
Title: _________________________
Date: _________________________""",
    },
]


# ---------------------------------------------------------------------------
# Template Index (for fast lookup)
# ---------------------------------------------------------------------------

_TEMPLATE_INDEX: dict[str, dict[str, Any]] = {t["id"]: t for t in AGREEMENT_TEMPLATES}


# ---------------------------------------------------------------------------
# Public API Functions
# ---------------------------------------------------------------------------


def get_all_templates() -> list[dict[str, Any]]:
    """Return metadata for all agreement templates (without full template text)."""
    results = []
    for t in AGREEMENT_TEMPLATES:
        summary = {k: v for k, v in t.items() if k != "template_text"}
        summary["template_text_length"] = len(t["template_text"])
        results.append(summary)
    return results


def get_template(template_id: str) -> dict[str, Any] | None:
    """Return a single template by ID, or None if not found."""
    return copy.deepcopy(_TEMPLATE_INDEX.get(template_id))


def get_templates_by_category(category: str) -> list[dict[str, Any]]:
    """Return all templates in a given category."""
    return [copy.deepcopy(t) for t in AGREEMENT_TEMPLATES if t["category"] == category]


def get_permanence_requirements() -> dict[str, Any]:
    """Return the permanence framework requirements."""
    return copy.deepcopy(PERMANENCE_REQUIREMENTS)


def generate_agreement(template_id: str, variables: dict[str, Any]) -> dict[str, Any]:
    """
    Generate a filled-in agreement from a template and a dictionary of variables.

    Parameters
    ----------
    template_id : str
        The ID of the agreement template to use (e.g., "temporary_use_license").
    variables : dict
        A dictionary mapping variable field names to their values. Values will be
        substituted into the template text wherever ``{{field_name}}`` appears.

    Returns
    -------
    dict with keys:
        - title: str -- the agreement title
        - parties: list[str] -- the parties required for this agreement
        - effective_date: str -- today's date in ISO format
        - body: str -- the full agreement text with variables filled in
        - permanence_clause: str -- the permanence clause text (if applicable)
        - signatures_required: list[str] -- list of signature blocks required

    Raises
    ------
    ValueError
        If template_id is not found or if required variables are missing.
    """
    template = _TEMPLATE_INDEX.get(template_id)
    if template is None:
        available = ", ".join(sorted(_TEMPLATE_INDEX.keys()))
        raise ValueError(
            f"Unknown template_id: '{template_id}'. Available templates: {available}"
        )

    # -- Validate required fields ------------------------------------------
    required_fields = [
        f["field_name"]
        for f in template["variable_fields"]
        if f.get("required", False)
    ]
    missing = [f for f in required_fields if f not in variables or variables[f] is None]
    if missing:
        raise ValueError(
            f"Missing required variable(s) for template '{template_id}': {missing}"
        )

    # -- Fill template text ------------------------------------------------
    body = template["template_text"]
    for field_name, value in variables.items():
        placeholder = "{{" + field_name + "}}"
        body = body.replace(placeholder, str(value))

    # -- Generate permanence clause ----------------------------------------
    permanence_clause = _generate_permanence_clause(template, variables)

    # -- Build signature list from template --------------------------------
    signatures_required = list(template["parties_required"])

    # -- Build result ------------------------------------------------------
    return {
        "title": template["name"],
        "parties": list(template["parties_required"]),
        "effective_date": date.today().isoformat(),
        "body": body,
        "permanence_clause": permanence_clause,
        "signatures_required": signatures_required,
    }


def _generate_permanence_clause(
    template: dict[str, Any], variables: dict[str, Any]
) -> str:
    """
    Generate a permanence clause appropriate for the given template.

    For the permanence_clause_addendum template, the clause is embedded in the
    body itself. For all other templates, a standard permanence reminder clause
    is generated.
    """
    if template["id"] == "permanence_clause_addendum":
        return (
            "Permanence commitments are detailed in the body of this Addendum. "
            "The Activation Partner has committed to allocating "
            f"{variables.get('permanence_commitment_pct', 25)}% of total project "
            "value toward permanent community benefit across the categories defined "
            "in the Permanence Framework."
        )

    # For all other templates, generate a standard permanence reminder
    min_pct = PERMANENCE_REQUIREMENTS["minimum_permanent_value_pct"]
    categories_text = ", ".join(
        c["name"] for c in PERMANENCE_REQUIREMENTS["categories"]
    )

    return (
        f"PERMANENCE REQUIREMENT: Pursuant to the City of Philadelphia's Public "
        f"Space Permanence Framework, the parties acknowledge that no less than "
        f"{min_pct}% of the total value of any public space activation project "
        f"must be allocated toward permanent community benefit. Permanent value "
        f"is measured across the following categories: {categories_text}. "
        f"The parties shall execute a separate Permanence Clause Addendum "
        f"detailing specific commitments, timelines, and verification procedures. "
        f"Failure to execute and comply with a Permanence Clause Addendum may "
        f"constitute a material breach of this Agreement."
    )


def validate_permanence_allocation(
    total_project_value: float,
    allocations: dict[str, float],
) -> dict[str, Any]:
    """
    Validate that a set of permanence allocations meets the minimum requirements.

    Parameters
    ----------
    total_project_value : float
        Total value of the project in USD.
    allocations : dict[str, float]
        Dictionary mapping permanence category IDs to dollar amounts allocated.

    Returns
    -------
    dict with keys:
        - valid: bool
        - total_allocated: float
        - percentage_allocated: float
        - minimum_required_pct: int
        - minimum_required_amount: float
        - categories_used: int
        - minimum_categories_required: int
        - shortfall: float (0.0 if valid)
        - errors: list[str]
    """
    valid_category_ids = {c["id"] for c in PERMANENCE_REQUIREMENTS["categories"]}
    errors: list[str] = []

    # Validate category IDs
    for cat_id in allocations:
        if cat_id not in valid_category_ids:
            errors.append(f"Unknown permanence category: '{cat_id}'")

    total_allocated = sum(allocations.values())
    min_pct = PERMANENCE_REQUIREMENTS["minimum_permanent_value_pct"]
    min_amount = total_project_value * (min_pct / 100.0)
    percentage_allocated = (
        (total_allocated / total_project_value * 100.0) if total_project_value > 0 else 0.0
    )
    categories_used = sum(1 for v in allocations.values() if v > 0)
    min_categories = 2

    shortfall = max(0.0, min_amount - total_allocated)

    if total_allocated < min_amount:
        errors.append(
            f"Total permanence allocation (${total_allocated:,.2f} / "
            f"{percentage_allocated:.1f}%) is below the minimum requirement "
            f"of {min_pct}% (${min_amount:,.2f})."
        )

    if categories_used < min_categories:
        errors.append(
            f"Permanence investments span {categories_used} category(ies), "
            f"but a minimum of {min_categories} categories is required."
        )

    return {
        "valid": len(errors) == 0,
        "total_allocated": total_allocated,
        "percentage_allocated": round(percentage_allocated, 2),
        "minimum_required_pct": min_pct,
        "minimum_required_amount": min_amount,
        "categories_used": categories_used,
        "minimum_categories_required": min_categories,
        "shortfall": shortfall,
        "errors": errors,
    }


# ---------------------------------------------------------------------------
# Module self-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 72)
    print("AGREEMENT GENERATION ENGINE - MODULE SELF-TEST")
    print("=" * 72)

    # List all templates
    print(f"\nLoaded {len(AGREEMENT_TEMPLATES)} agreement templates:\n")
    for t in AGREEMENT_TEMPLATES:
        req_fields = sum(1 for f in t["variable_fields"] if f.get("required"))
        opt_fields = len(t["variable_fields"]) - req_fields
        print(
            f"  [{t['category']:>11s}]  {t['id']:<35s}  "
            f"({req_fields} required, {opt_fields} optional fields, "
            f"~{t['estimated_legal_review_hours']}h legal review)"
        )

    # Test: generate a temporary use license
    print("\n" + "-" * 72)
    print("TEST: Generate a Temporary Use License")
    print("-" * 72)

    test_vars = {
        "licensee_name": "Philadelphia Community Arts Collective",
        "licensee_address": "1234 North Broad Street, Philadelphia, PA 19121",
        "site_address": "800 Vine Street, Philadelphia, PA 19107",
        "site_parcel_id": "888-000-1234",
        "site_square_footage": 5000,
        "license_start_date": "2026-04-01",
        "license_end_date": "2026-10-31",
        "permitted_use_description": (
            "community art market, live music performances, "
            "and interactive public art installations"
        ),
        "maximum_occupancy": 300,
        "license_fee": "2,500.00",
        "security_deposit": "1,000.00",
        "hours_of_operation": "10:00 AM - 9:00 PM, Thursday through Sunday",
        "council_district": "5",
    }

    result = generate_agreement("temporary_use_license", test_vars)
    print(f"\n  Title: {result['title']}")
    print(f"  Effective Date: {result['effective_date']}")
    print(f"  Parties: {result['parties']}")
    print(f"  Body length: {len(result['body'])} characters")
    print(f"  Signatures required: {result['signatures_required']}")
    print(f"\n  Permanence Clause (excerpt):\n    {result['permanence_clause'][:200]}...")

    # Test: validate permanence allocation
    print("\n" + "-" * 72)
    print("TEST: Validate Permanence Allocation")
    print("-" * 72)

    validation = validate_permanence_allocation(
        total_project_value=100000.00,
        allocations={
            "physical_improvement": 15000.00,
            "knowledge_transfer": 12000.00,
        },
    )
    print(f"\n  Valid: {validation['valid']}")
    print(f"  Allocated: ${validation['total_allocated']:,.2f} ({validation['percentage_allocated']}%)")
    print(f"  Categories used: {validation['categories_used']}")
    print(f"  Errors: {validation['errors']}")

    print("\n" + "=" * 72)
    print("SELF-TEST COMPLETE")
    print("=" * 72)
