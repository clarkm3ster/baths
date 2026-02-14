"""
SPHERES Innovation Laboratory -- Policy Inventor
=================================================
Domain: policy-invention
Zoning reforms, land bank legislation, community benefit agreements,
green infrastructure mandates, and anti-displacement protections
for Philadelphia's public space activation platform.
"""

# ---------------------------------------------------------------------------
# Seed Innovations — 6 concrete policy proposals grounded in Philadelphia law
# ---------------------------------------------------------------------------

INNOVATIONS: list[dict] = [
    # ---- 1. Community First Zoning Overlay ----
    {
        "title": "Community First Zoning Overlay",
        "summary": (
            "A new zoning overlay district that designates vacant and "
            "underutilized parcels as Community Activation Zones, granting "
            "by-right permission for temporary public-space uses without a "
            "full variance hearing."
        ),
        "category": "zoning-reform",
        "impact_level": 5,
        "feasibility": 3,
        "novelty": 5,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "legislative_text_summary": (
                "Amends Title 14 (Zoning and Planning) of the Philadelphia "
                "Code to create a new '/CA' Community Activation overlay. "
                "Parcels within the overlay receive by-right approval for "
                "temporary community uses including public gardens, outdoor "
                "gathering spaces, pop-up markets, and civic programming "
                "lasting up to 24 months with a single renewal option. "
                "Permanent structures are excluded; all installations must "
                "be removable within 30 days of permit expiration."
            ),
            "sponsoring_body": (
                "Philadelphia City Council (introduced via district council "
                "members representing Point Breeze, Kensington, and "
                "Strawberry Mansion) with co-sponsorship from the "
                "Philadelphia City Planning Commission."
            ),
            "implementation_timeline": (
                "Phase 1 (months 1-6): Draft overlay language and hold "
                "community input sessions in each target neighborhood. "
                "Phase 2 (months 7-12): City Planning Commission review "
                "and recommendation. Phase 3 (months 13-18): Council "
                "committee hearings, full council vote, and mayoral "
                "signature. Phase 4 (months 19-24): L&I develops "
                "streamlined permit application and begins accepting filings."
            ),
            "enforcement_mechanism": (
                "Department of Licenses and Inspections (L&I) issues a "
                "Community Activation Permit with annual inspections. "
                "Violations trigger a 30-day cure period; failure to cure "
                "results in permit revocation and a $500/day fine. The "
                "Zoning Board of Adjustment retains appellate jurisdiction."
            ),
            "affected_parcels_estimate": (
                "Approximately 4,200 vacant parcels across 14 council "
                "districts qualify for initial overlay designation, with "
                "the highest concentrations in North Philadelphia (1,600), "
                "West Philadelphia (900), and Kensington (700)."
            ),
            "precedent_cities": [
                "Detroit Land Use Permit for temporary activations",
                "Los Angeles Arts District overlay zoning",
                "Minneapolis Green Zone overlay for environmental justice",
                "Cleveland Vacant Property Reuse District",
            ],
            "equity_provisions": (
                "At least 60% of parcels in the initial overlay must be "
                "located in census tracts where median household income is "
                "below 80% of the city median. Community organizations "
                "headquartered in the overlay neighborhood receive priority "
                "permitting, and application fees are waived for groups "
                "with annual budgets under $250,000."
            ),
        },
        "tags": [
            "zoning-reform",
            "community-activation",
            "by-right-permitting",
            "vacant-land",
            "title-14",
        ],
    },
    # ---- 2. Vacant Lot Fast-Track Ordinance ----
    {
        "title": "Vacant Lot Fast-Track Ordinance",
        "summary": (
            "Creates a 30-day administrative approval pathway for temporary "
            "activations on vacant lots, bypassing the standard zoning "
            "variance process that currently takes 6-12 months."
        ),
        "category": "zoning-reform",
        "impact_level": 4,
        "feasibility": 4,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "legislative_text_summary": (
                "Adds Chapter 14-900 to the Philadelphia Code establishing "
                "a Temporary Activation Permit (TAP). Any parcel vacant for "
                "12+ months and not subject to active redevelopment plans "
                "qualifies. TAP applications are reviewed administratively "
                "by L&I within 30 calendar days. Approved uses include "
                "community gardens, open-air performance spaces, "
                "recreational areas, and artisan markets. Permits are valid "
                "for 12 months with two 6-month renewals."
            ),
            "sponsoring_body": (
                "Philadelphia City Council, co-sponsored by the Managing "
                "Director's Office of Community Empowerment and Opportunity "
                "(CEO) and the Philadelphia Redevelopment Authority."
            ),
            "implementation_timeline": (
                "Months 1-3: Draft ordinance language and interagency MOU. "
                "Months 4-6: Council introduction, committee hearings, and "
                "vote. Months 7-9: L&I develops TAP application form, "
                "online portal, and staff training. Month 10: First "
                "applications accepted. Target: 50 TAPs issued in year one."
            ),
            "enforcement_mechanism": (
                "L&I conducts site visits at permit issuance and at the "
                "6-month mark. Neighborhood advisory committees may file "
                "complaints through the 311 system. Non-compliant sites "
                "receive a 14-day cure notice; uncured violations result "
                "in permit revocation and site clearance at the "
                "applicant's expense."
            ),
            "affected_parcels_estimate": (
                "Roughly 7,800 parcels meet the 12-month vacancy threshold "
                "citywide. The ordinance projects 200-400 activations in "
                "the first three years, prioritizing the 3,100 parcels "
                "already in the Philadelphia Land Bank inventory."
            ),
            "precedent_cities": [
                "New York City CLIP (Clean Lots Initiative Program)",
                "Baltimore Adopt-A-Lot 30-day approval",
                "Pittsburgh Vacant Lot Toolkit expedited permits",
            ],
            "equity_provisions": (
                "Fast-track applications from community land trusts and "
                "BIPOC-led organizations are processed within 15 days "
                "instead of 30. A technical assistance fund of $200,000 "
                "annually is established to help under-resourced groups "
                "complete applications."
            ),
        },
        "tags": [
            "fast-track",
            "temporary-activation",
            "vacant-lots",
            "administrative-approval",
            "land-bank",
        ],
    },
    # ---- 3. Anti-Displacement Green Shield ----
    {
        "title": "Anti-Displacement Green Shield",
        "summary": (
            "Freezes property tax assessments for owner-occupied homes "
            "within 500 feet of newly activated public spaces, preventing "
            "green gentrification from displacing long-term residents."
        ),
        "category": "anti-displacement",
        "impact_level": 5,
        "feasibility": 2,
        "novelty": 5,
        "time_horizon": "medium",
        "status": "review",
        "details": {
            "legislative_text_summary": (
                "Amends Title 19 (Finance, Taxes, and Collections) of the "
                "Philadelphia Code to create the Green Shield Assessment "
                "Freeze. Owner-occupied residential properties within a "
                "500-foot radius of a parcel activated through a SPHERES "
                "Community Activation Permit are eligible for a 10-year "
                "assessment freeze at the pre-activation assessed value. "
                "The freeze applies only to the land value component and "
                "does not affect improvement assessments from renovations "
                "initiated by the owner."
            ),
            "sponsoring_body": (
                "Philadelphia City Council with advisory support from the "
                "Office of Property Assessment (OPA) and endorsement from "
                "the Philadelphia Coalition for Affordable Communities."
            ),
            "implementation_timeline": (
                "Year 1: Commission a gentrification impact study by the "
                "Pew Charitable Trusts Philadelphia Research Initiative. "
                "Year 2: Draft legislation informed by study findings; hold "
                "12 community hearings across affected neighborhoods. "
                "Year 3: Council vote, OPA system modifications, and "
                "enrollment of first cohort of protected homeowners."
            ),
            "enforcement_mechanism": (
                "OPA automatically identifies eligible parcels using GIS "
                "proximity analysis when a Community Activation Permit is "
                "issued. Homeowners opt in via a one-page application. "
                "Annual audits confirm continued owner-occupancy; loss of "
                "homestead exemption status terminates the freeze. Revenue "
                "impact is offset by a 1% surcharge on speculative property "
                "transfers (non-owner-occupied sales above $300,000) within "
                "the same radius."
            ),
            "affected_parcels_estimate": (
                "Based on current activation projections, approximately "
                "12,000 owner-occupied homes would be eligible in the "
                "first 5 years. Highest concentrations expected in Point "
                "Breeze (2,100), Strawberry Mansion (1,800), Kensington "
                "(1,500), and Mantua (1,200)."
            ),
            "precedent_cities": [
                "Portland Anti-Displacement Tax Exemption (N/NE Portland)",
                "Austin Homestead Preservation Act assessment limits",
                "Washington DC limited equity cooperative protections",
                "San Francisco Proposition M anti-speculation transfer tax",
            ],
            "equity_provisions": (
                "Eligibility is restricted to households earning below "
                "120% of Area Median Income. Long-term residents (10+ "
                "years of continuous owner-occupancy) receive an enhanced "
                "freeze covering both land and improvement assessments. "
                "Renters in eligible areas receive parallel protections "
                "through a companion rent stabilization ordinance."
            ),
        },
        "tags": [
            "anti-displacement",
            "property-tax",
            "green-gentrification",
            "assessment-freeze",
            "equity",
        ],
    },
    # ---- 4. Land Bank Community Transfer Act ----
    {
        "title": "Land Bank Community Transfer Act",
        "summary": (
            "Streamlines the Philadelphia Land Bank's disposition process "
            "to transfer city-owned vacant lots to community land trusts "
            "and neighborhood organizations within 90 days."
        ),
        "category": "land-bank-legislation",
        "impact_level": 5,
        "feasibility": 3,
        "novelty": 4,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "legislative_text_summary": (
                "Amends the Philadelphia Land Bank's enabling legislation "
                "(Ordinance 130986, 2013) to create a Community Transfer "
                "Track. Eligible community organizations — defined as "
                "501(c)(3) nonprofits with at least 3 years of operation "
                "in the target neighborhood — may apply for direct transfer "
                "of Land Bank parcels at nominal cost ($1). The Land Bank "
                "board must act on applications within 90 days. Transferred "
                "parcels carry a deed restriction requiring community use "
                "for a minimum of 15 years."
            ),
            "sponsoring_body": (
                "Philadelphia City Council in partnership with the "
                "Philadelphia Land Bank Board of Directors and the "
                "Philadelphia Association of Community Development "
                "Corporations (PACDC)."
            ),
            "implementation_timeline": (
                "Months 1-4: Stakeholder convening with Land Bank staff, "
                "community land trusts, and council members. Months 5-8: "
                "Draft amendment and public comment period. Months 9-12: "
                "Council vote and implementation. Months 13-18: First "
                "cohort of 50 community transfers completed."
            ),
            "enforcement_mechanism": (
                "Deed restrictions are recorded with the Department of "
                "Records and enforceable by the Land Bank, the City "
                "Solicitor's Office, and any resident of the census tract. "
                "If the receiving organization dissolves or abandons the "
                "parcel, title reverts to the Land Bank with all "
                "improvements becoming city property. Annual compliance "
                "reports are filed with the Land Bank."
            ),
            "affected_parcels_estimate": (
                "The Philadelphia Land Bank holds approximately 3,100 "
                "parcels as of 2024. An estimated 1,800 are suitable for "
                "community transfer (excluding parcels reserved for "
                "affordable housing development or with environmental "
                "remediation requirements). Target: 300 transfers in the "
                "first three years."
            ),
            "precedent_cities": [
                "Cleveland Land Bank $1 side-lot program",
                "Baltimore Community Land Trust disposition track",
                "Detroit Land Bank community partner transfers",
                "St. Louis Land Reutilization Authority neighborhood sales",
            ],
            "equity_provisions": (
                "Priority scoring awards additional points to organizations "
                "led by residents of the target neighborhood, BIPOC-led "
                "organizations, and groups with demonstrated track records "
                "of anti-displacement work. Community land trusts receive "
                "automatic priority over private developers for all parcels "
                "in gentrifying census tracts as identified by the "
                "Reinvestment Fund's Market Value Analysis."
            ),
        },
        "tags": [
            "land-bank",
            "community-transfer",
            "land-trust",
            "disposition",
            "community-ownership",
        ],
    },
    # ---- 5. Green Infrastructure Mandate ----
    {
        "title": "Green Infrastructure Mandate for Activated Parcels",
        "summary": (
            "Requires all parcels activated through the SPHERES platform "
            "to incorporate stormwater management best practices, turning "
            "every community space into green infrastructure."
        ),
        "category": "green-infrastructure",
        "impact_level": 4,
        "feasibility": 4,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "legislative_text_summary": (
                "Adds Section 14-704(7) to the Philadelphia Code requiring "
                "that all Community Activation Permits include a stormwater "
                "management plan meeting the Philadelphia Water Department's "
                "Green Stormwater Infrastructure (GSI) standards. Activated "
                "parcels must manage the first 1.5 inches of rainfall on "
                "site through permeable surfaces, rain gardens, bioswales, "
                "or cisterns. Compliance qualifies the parcel and adjacent "
                "properties for stormwater fee credits under the "
                "Parcel-Based Billing program."
            ),
            "sponsoring_body": (
                "Philadelphia Water Department (PWD) in coordination with "
                "City Council and the Office of Sustainability. Technical "
                "standards developed jointly by PWD and the Philadelphia "
                "City Planning Commission."
            ),
            "implementation_timeline": (
                "Months 1-3: PWD publishes simplified GSI design templates "
                "for community-scale installations. Months 4-6: Council "
                "enacts the mandate as an amendment to the activation "
                "permit ordinance. Months 7-12: First activated parcels "
                "install GSI features. Ongoing: PWD provides free design "
                "assistance and materials for qualifying sites."
            ),
            "enforcement_mechanism": (
                "PWD inspectors review stormwater plans as part of the "
                "Community Activation Permit process. Post-installation "
                "inspections occur within 60 days and annually thereafter. "
                "Sites that fail inspection enter a 90-day remediation "
                "period with free technical assistance from PWD. Stormwater "
                "fee credits are suspended for non-compliant parcels."
            ),
            "affected_parcels_estimate": (
                "All SPHERES-activated parcels (projected 200-400 in the "
                "first 3 years) must comply. Collectively these parcels "
                "could manage an estimated 8-15 million gallons of "
                "stormwater annually, equivalent to 120-220 acres of "
                "impervious surface offset."
            ),
            "precedent_cities": [
                "Philadelphia Green City Clean Waters program (existing PWD framework)",
                "Portland Green Streets stormwater management requirements",
                "Washington DC Green Area Ratio requirements",
                "Seattle Green Factor for new development",
            ],
            "equity_provisions": (
                "PWD allocates $1.5 million annually from the Green City "
                "Clean Waters budget to fund GSI installations on community "
                "activation sites in environmental justice communities. "
                "Neighborhoods in the combined sewer overflow area — "
                "disproportionately low-income and communities of color — "
                "receive priority funding and enhanced stormwater credits "
                "worth 150% of the standard rate."
            ),
        },
        "tags": [
            "green-infrastructure",
            "stormwater",
            "water-department",
            "sustainability",
            "resilience",
        ],
    },
    # ---- 6. Right to Activate ----
    {
        "title": "Right to Activate",
        "summary": (
            "Establishes a legal framework giving neighbors within 150 "
            "feet of a vacant lot the first right to propose and operate "
            "a temporary community activation on the site."
        ),
        "category": "community-benefit-agreement",
        "impact_level": 4,
        "feasibility": 3,
        "novelty": 5,
        "time_horizon": "medium",
        "status": "review",
        "details": {
            "legislative_text_summary": (
                "Creates Chapter 9-4200 of the Philadelphia Code, the "
                "'Right to Activate Act.' When a parcel has been vacant "
                "and unmaintained for 24 or more consecutive months, "
                "adjacent property owners and registered community "
                "organizations within 150 feet may file a Right to "
                "Activate petition with the Department of Licenses and "
                "Inspections. The property owner receives 60 days' notice "
                "and may present a redevelopment plan; absent a credible "
                "plan, L&I issues a Community Activation License to the "
                "petitioning neighbors for a period of up to 36 months."
            ),
            "sponsoring_body": (
                "Philadelphia City Council, with legal framework developed "
                "by the Community Justice Project at the Public Interest "
                "Law Center and endorsed by the Philadelphia Vacant "
                "Property Coalition."
            ),
            "implementation_timeline": (
                "Year 1: Legal analysis and constitutional review by the "
                "City Solicitor's Office; stakeholder input sessions. "
                "Year 2: Council introduction, Judiciary Committee "
                "hearings, and vote. Year 3: L&I develops petition process "
                "and online filing system. First Right to Activate "
                "petitions accepted 30 months after legislative process "
                "begins."
            ),
            "enforcement_mechanism": (
                "L&I mediates disputes between property owners and "
                "petitioners. A Community Activation License grants the "
                "petitioner a revocable license — not a property interest — "
                "to use the lot for approved community purposes. The "
                "license terminates immediately if the property owner "
                "commences bona fide construction. Liability insurance "
                "requirements and indemnification provisions protect both "
                "the property owner and the city."
            ),
            "affected_parcels_estimate": (
                "Philadelphia has approximately 40,000 vacant lots, of "
                "which an estimated 15,000-18,000 have been vacant for "
                "24+ months with no active development plans. The Right "
                "to Activate could unlock 2,000-3,000 of these parcels "
                "for community use in the first five years."
            ),
            "precedent_cities": [
                "Scotland's Community Right to Buy (Land Reform Act 2003)",
                "England's Community Right to Bid (Localism Act 2011)",
                "New York City community garden protection legislation",
                "Detroit community stabilization agreements for vacant land",
            ],
            "equity_provisions": (
                "Petitions from residents of historically disinvested "
                "neighborhoods — as defined by the City Planning "
                "Commission's equity atlas — receive expedited 30-day "
                "processing. Legal aid organizations receive city funding "
                "to assist low-income petitioners. The Act includes a "
                "non-retaliation clause prohibiting property owners from "
                "raising rents or initiating eviction proceedings against "
                "tenants who participate in Right to Activate petitions."
            ),
        },
        "tags": [
            "right-to-activate",
            "neighbor-rights",
            "vacant-land",
            "community-power",
            "legal-framework",
        ],
    },
]


# ---------------------------------------------------------------------------
# Generator Templates — 8 parameterized templates for producing new policies
# ---------------------------------------------------------------------------

TEMPLATES: list[dict] = [
    # ---- T1. Zoning Overlay Generator ----
    {
        "title": "Zoning Overlay District Generator",
        "summary": (
            "Generates new overlay zoning districts that grant by-right "
            "permissions for specified community uses in targeted areas."
        ),
        "category": "zoning-reform",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [3, 5],
        "details": {
            "legislative_text_summary": (
                "Template for amending Title 14 of the Philadelphia Code "
                "to create new overlay districts. Variables include: "
                "permitted uses, geographic boundaries, lot size thresholds, "
                "permit duration, and community review requirements."
            ),
            "sponsoring_body": (
                "Configurable: City Council district member, Planning "
                "Commission, or joint introduction."
            ),
            "implementation_timeline": (
                "Standard 18-24 month track: drafting (4 months), community "
                "input (3 months), commission review (4 months), council "
                "hearings and vote (4 months), administrative buildout "
                "(3-6 months)."
            ),
            "enforcement_mechanism": (
                "L&I permit-based enforcement with configurable inspection "
                "schedules, violation cure periods, and fine structures."
            ),
            "equity_provisions": (
                "Template includes mandatory equity thresholds: minimum "
                "percentage of overlay parcels in low-income census tracts, "
                "priority processing for community-based applicants, and "
                "fee waiver schedules."
            ),
        },
        "tags": ["zoning", "overlay", "generator", "title-14"],
    },
    # ---- T2. Expedited Permit Pathway Generator ----
    {
        "title": "Expedited Permit Pathway Generator",
        "summary": (
            "Creates fast-track administrative approval processes for "
            "temporary community uses, with configurable timelines, "
            "eligibility criteria, and review standards."
        ),
        "category": "zoning-reform",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [3, 5],
        "novelty_range": [2, 4],
        "details": {
            "legislative_text_summary": (
                "Template for new sections of the Philadelphia Code "
                "establishing abbreviated permit processes. Parameters: "
                "review timeline (14-90 days), qualifying vacancy duration, "
                "permitted use categories, permit term and renewal options, "
                "and interagency coordination requirements."
            ),
            "sponsoring_body": (
                "Configurable: Council ordinance, Managing Director's "
                "executive order, or L&I administrative regulation."
            ),
            "implementation_timeline": (
                "Accelerated 6-12 month track suitable for administrative "
                "regulations; 12-18 months for council ordinances."
            ),
            "enforcement_mechanism": (
                "Administrative review with configurable complaint-driven "
                "and proactive inspection models."
            ),
            "equity_provisions": (
                "Built-in equity accelerators: reduced timelines for "
                "organizations serving disadvantaged communities, technical "
                "assistance budgets, and multilingual application support."
            ),
        },
        "tags": ["fast-track", "permits", "generator", "administrative"],
    },
    # ---- T3. Anti-Displacement Protection Generator ----
    {
        "title": "Anti-Displacement Protection Generator",
        "summary": (
            "Produces tailored anti-displacement policies including "
            "assessment freezes, transfer tax surcharges, and right-of-first-"
            "refusal mechanisms tied to public space activations."
        ),
        "category": "anti-displacement",
        "time_horizon": "medium",
        "impact_range": [4, 5],
        "feasibility_range": [2, 3],
        "novelty_range": [4, 5],
        "details": {
            "legislative_text_summary": (
                "Template for Title 19 amendments and standalone ordinances "
                "addressing displacement triggered by neighborhood "
                "improvements. Configurable parameters: protection radius, "
                "income eligibility thresholds, freeze duration, funding "
                "offset mechanisms, and interaction with existing programs "
                "like the Homestead Exemption and LOOP."
            ),
            "sponsoring_body": (
                "Configurable: Council with OPA advisory support, or "
                "mayoral executive action for assessment policy changes."
            ),
            "implementation_timeline": (
                "24-36 month track reflecting the complexity of tax policy "
                "changes: impact study (6-12 months), legislative drafting "
                "and hearings (8-12 months), system implementation "
                "(6-12 months)."
            ),
            "enforcement_mechanism": (
                "GIS-based automatic eligibility identification with "
                "opt-in enrollment. Annual occupancy verification and "
                "income recertification."
            ),
            "equity_provisions": (
                "All generated policies must include income-tiered "
                "protections, enhanced benefits for long-term residents, "
                "renter parallel protections, and anti-retaliation clauses."
            ),
        },
        "tags": [
            "anti-displacement",
            "tax-protection",
            "generator",
            "equity",
        ],
    },
    # ---- T4. Land Bank Disposition Policy Generator ----
    {
        "title": "Land Bank Disposition Policy Generator",
        "summary": (
            "Generates streamlined disposition tracks for the Philadelphia "
            "Land Bank, enabling faster transfers to community organizations "
            "with appropriate deed restrictions and accountability."
        ),
        "category": "land-bank-legislation",
        "time_horizon": "near",
        "impact_range": [3, 5],
        "feasibility_range": [3, 4],
        "novelty_range": [3, 4],
        "details": {
            "legislative_text_summary": (
                "Template for amendments to Ordinance 130986 (Philadelphia "
                "Land Bank enabling legislation). Variables: eligible "
                "recipient types, transfer price, deed restriction terms, "
                "reversion triggers, application review timeline, and "
                "board approval thresholds."
            ),
            "sponsoring_body": (
                "Configurable: Council amendment to enabling legislation, "
                "or Land Bank Board policy resolution for changes within "
                "existing statutory authority."
            ),
            "implementation_timeline": (
                "8-14 months for board policy changes; 14-20 months for "
                "legislative amendments requiring council action."
            ),
            "enforcement_mechanism": (
                "Deed-restriction-based enforcement with annual compliance "
                "reporting, reversion clauses, and multi-party standing "
                "to enforce (Land Bank, City Solicitor, neighborhood "
                "residents)."
            ),
            "equity_provisions": (
                "Priority scoring matrices weighted toward neighborhood-"
                "based organizations, BIPOC leadership, anti-displacement "
                "mission, and low-income community benefit."
            ),
        },
        "tags": ["land-bank", "disposition", "generator", "community-transfer"],
    },
    # ---- T5. Green Infrastructure Requirement Generator ----
    {
        "title": "Green Infrastructure Requirement Generator",
        "summary": (
            "Produces stormwater management requirements for activated "
            "parcels, calibrated to site size, soil conditions, and "
            "combined sewer overflow priority areas."
        ),
        "category": "green-infrastructure",
        "time_horizon": "near",
        "impact_range": [3, 4],
        "feasibility_range": [3, 5],
        "novelty_range": [2, 4],
        "details": {
            "legislative_text_summary": (
                "Template for stormwater management provisions attached to "
                "Community Activation Permits. Parameters: rainfall depth "
                "capture threshold (0.5-2.0 inches), approved BMP types, "
                "maintenance obligations, credit calculations under "
                "Parcel-Based Billing, and interaction with PWD's Green "
                "City Clean Waters targets."
            ),
            "sponsoring_body": (
                "Configurable: PWD administrative regulation, council "
                "ordinance, or joint Planning Commission/PWD standard."
            ),
            "implementation_timeline": (
                "6-10 months: template design guide publication (2 months), "
                "staff training (2 months), pilot site installations "
                "(3-4 months), full program launch (2 months)."
            ),
            "enforcement_mechanism": (
                "PWD plan review, post-installation inspection, and annual "
                "maintenance verification. Stormwater credit incentives "
                "tied to compliance."
            ),
            "equity_provisions": (
                "Enhanced funding for sites in environmental justice "
                "communities and combined sewer overflow areas. Free "
                "design and materials for community groups with budgets "
                "under $100,000."
            ),
        },
        "tags": [
            "green-infrastructure",
            "stormwater",
            "generator",
            "resilience",
        ],
    },
    # ---- T6. Community Benefit Agreement Generator ----
    {
        "title": "Community Benefit Agreement Generator",
        "summary": (
            "Creates enforceable community benefit agreements between "
            "developers, community organizations, and the city, ensuring "
            "that development near activated spaces delivers measurable "
            "neighborhood benefits."
        ),
        "category": "community-benefit-agreement",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [3, 5],
        "details": {
            "legislative_text_summary": (
                "Template for standardized CBA frameworks triggered by "
                "development projects within 1,000 feet of activated "
                "community spaces. Configurable terms: local hiring "
                "percentages, affordable housing set-asides, community "
                "space preservation commitments, financial contributions "
                "to a neighborhood trust fund, and developer obligations "
                "for public realm improvements."
            ),
            "sponsoring_body": (
                "Configurable: Council ordinance mandating CBAs for "
                "projects receiving public subsidy, or voluntary framework "
                "facilitated by the Commerce Department."
            ),
            "implementation_timeline": (
                "12-18 months for mandatory CBA ordinance; 6-9 months "
                "for voluntary framework and model agreement publication."
            ),
            "enforcement_mechanism": (
                "CBAs recorded as covenants running with the land. "
                "Independent community monitor funded by developer "
                "escrow. Annual public reporting on compliance metrics. "
                "City retains right to withhold permits for non-compliant "
                "developers."
            ),
            "equity_provisions": (
                "All CBAs must include anti-displacement provisions, "
                "living wage requirements for created jobs, and community "
                "ownership opportunities. Negotiating power is equalized "
                "through city-funded technical assistance for community "
                "groups."
            ),
        },
        "tags": ["CBA", "development", "generator", "community-benefit"],
    },
    # ---- T7. Neighbor Rights Framework Generator ----
    {
        "title": "Neighbor Rights Framework Generator",
        "summary": (
            "Generates legal frameworks establishing neighbor and "
            "community rights to intervene in vacant land management, "
            "from notification rights to full activation authority."
        ),
        "category": "community-benefit-agreement",
        "time_horizon": "far",
        "impact_range": [4, 5],
        "feasibility_range": [1, 3],
        "novelty_range": [4, 5],
        "details": {
            "legislative_text_summary": (
                "Template for new chapters of the Philadelphia Code "
                "establishing tiered neighbor rights. Configurable tiers: "
                "notification rights (right to know about ownership and "
                "plans), consultation rights (right to comment on proposed "
                "uses), preference rights (right of first refusal for "
                "purchase or lease), and activation rights (right to use "
                "neglected parcels). Parameters include vacancy duration "
                "triggers, proximity thresholds, and due process "
                "protections for property owners."
            ),
            "sponsoring_body": (
                "Configurable: Council legislation with City Solicitor "
                "constitutional review, or pilot program via executive "
                "order limited to city-owned parcels."
            ),
            "implementation_timeline": (
                "30-48 months for full legislative framework including "
                "constitutional analysis (6 months), community design "
                "process (6 months), drafting and hearings (12 months), "
                "and phased implementation (6-24 months)."
            ),
            "enforcement_mechanism": (
                "L&I petition process with administrative law judge review "
                "for contested cases. Property owner due process protections "
                "include notice, hearing, and appeal rights. Graduated "
                "intervention tiers minimize constitutional concerns."
            ),
            "equity_provisions": (
                "Framework must prioritize neighborhoods with the highest "
                "vacancy rates and lowest incomes. Free legal assistance "
                "for petitioners below 200% of the federal poverty line. "
                "Language access requirements for all notices and processes."
            ),
        },
        "tags": [
            "neighbor-rights",
            "vacant-land",
            "generator",
            "community-power",
        ],
    },
    # ---- T8. Interagency Coordination Protocol Generator ----
    {
        "title": "Interagency Coordination Protocol Generator",
        "summary": (
            "Produces memoranda of understanding and joint operating "
            "procedures connecting city agencies — L&I, PWD, Planning, "
            "Land Bank, Parks and Recreation — around community space "
            "activation permitting and support."
        ),
        "category": "zoning-reform",
        "time_horizon": "near",
        "impact_range": [3, 4],
        "feasibility_range": [3, 5],
        "novelty_range": [2, 3],
        "details": {
            "legislative_text_summary": (
                "Template for interagency MOUs and executive orders "
                "establishing coordinated review processes for community "
                "activation projects. Parameters: participating agencies, "
                "lead agency designation, joint review timelines, "
                "data-sharing protocols, single-point-of-contact "
                "requirements, and escalation procedures for interagency "
                "disagreements."
            ),
            "sponsoring_body": (
                "Configurable: Managing Director's executive directive, "
                "mayoral executive order, or council resolution directing "
                "interagency coordination."
            ),
            "implementation_timeline": (
                "4-8 months: interagency working group formation (1 month), "
                "MOU drafting (2-3 months), staff training and system "
                "integration (1-2 months), pilot launch (1-2 months)."
            ),
            "enforcement_mechanism": (
                "Managing Director's Office conducts quarterly performance "
                "reviews. Metrics include average permit review time, "
                "interagency referral completion rates, and applicant "
                "satisfaction scores. Agencies failing to meet benchmarks "
                "are subject to corrective action plans."
            ),
            "equity_provisions": (
                "All coordination protocols must include community "
                "navigator positions — city-funded staff embedded in "
                "neighborhood organizations to guide applicants through "
                "multi-agency processes. Navigators are required in "
                "every council district with vacancy rates above 10%."
            ),
        },
        "tags": [
            "interagency",
            "coordination",
            "generator",
            "MOU",
            "operations",
        ],
    },
]
