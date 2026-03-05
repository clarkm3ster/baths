"""
SPHERES Innovation Laboratory — Revenue Architect domain seeds.

Revenue streams, financing mechanisms, green bonds, impact funds,
tax incentives, and public-private partnerships for Philadelphia's
40,000+ vacant lots and public space activation.
"""

# ---------------------------------------------------------------------------
# Seed Innovations (6)
# ---------------------------------------------------------------------------

INNOVATIONS: list[dict] = [
    # ── 1. Green Space Bond ───────────────────────────────────────────────
    {
        "title": "Green Space Bond",
        "summary": (
            "A municipal bond instrument backed by the measurable property-value "
            "uplift generated when vacant lots are activated as community green "
            "spaces. Revenue is captured through the incremental tax base and "
            "recycled into bond service."
        ),
        "category": "green-bonds",
        "impact_level": 5,
        "feasibility": 3,
        "novelty": 4,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "funding_mechanism": (
                "General obligation green bond issued by the City of Philadelphia, "
                "certified under the Climate Bonds Standard. Proceeds fund lot "
                "remediation, planting, and basic amenity installation across "
                "targeted corridors."
            ),
            "total_capital": "$75M initial issuance; scalable to $200M with "
                             "demonstrated performance across the first 500 lots",
            "investor_returns": (
                "Tax-exempt coupon of 3.2-3.8 % with 20-year maturity. Green "
                "certification unlocks ESG-mandated institutional demand, "
                "compressing spreads ~25 bps below comparable GO debt."
            ),
            "repayment_source": (
                "Incremental property-tax revenue within a 400-meter radius of "
                "each activated lot. Philadelphia's 1.3998 % real-estate tax rate "
                "on rising assessments provides a self-reinforcing repayment "
                "stream as neighborhoods improve."
            ),
            "risk_profile": (
                "Moderate. Principal risk is slower-than-projected value uplift "
                "in distressed corridors. Mitigated by a 1.35x debt-service "
                "coverage ratio covenant, a reserve fund equal to 12 months of "
                "debt service, and geographic diversification across 15+ zip codes."
            ),
            "projected_leverage_ratio": "4.2x — every $1 of bond proceeds is "
                                        "projected to unlock $4.20 in private "
                                        "reinvestment within the activation zone",
            "legal_structure": (
                "City Council authorizing ordinance under Pennsylvania's "
                "Municipality Authorities Act. Bond counsel opinion from a "
                "nationally recognized firm; trustee holds proceeds in a "
                "restricted project fund with quarterly draw-down certification."
            ),
        },
        "tags": [
            "green-bonds",
            "municipal-finance",
            "property-value-uplift",
            "ESG",
            "philadelphia-land-bank",
        ],
    },
    # ── 2. Pay-for-Success Vacant Lot Remediation ─────────────────────────
    {
        "title": "Pay-for-Success Vacant Lot Remediation",
        "summary": (
            "An outcomes-based contract where private investors fund lot cleanup "
            "and greening up front, and the City repays only when pre-agreed "
            "health, safety, and property-value metrics are independently verified."
        ),
        "category": "impact-investing",
        "impact_level": 4,
        "feasibility": 3,
        "novelty": 4,
        "time_horizon": "medium",
        "status": "approved",
        "details": {
            "funding_mechanism": (
                "Social Impact Bond structure. An SPV raises working capital from "
                "impact investors and philanthropic first-loss providers (William "
                "Penn Foundation as anchor). Funds flow to vetted service providers "
                "who remediate and green lots. An independent evaluator triggers "
                "City success payments upon metric achievement."
            ),
            "total_capital": "$12M across three cohorts of 600 lots each, with "
                             "per-lot intervention cost averaging $6,500",
            "investor_returns": (
                "Base return of 5.0 % IRR if minimum outcomes met; up to 8.5 % "
                "IRR at stretch targets. First-loss tranche absorbs initial 15 % "
                "of losses, shielding senior investors."
            ),
            "repayment_source": (
                "City of Philadelphia general fund, justified by actuarial savings "
                "in Medicaid-funded mental-health visits (estimated $780/lot/year) "
                "and reduced blight-remediation enforcement costs."
            ),
            "risk_profile": (
                "Moderate-High. Outcome measurement methodology must survive "
                "independent audit. Key risk is attribution — isolating lot "
                "greening effects from broader neighborhood trends. Mitigated by "
                "randomized control evaluation design and precedent from the "
                "University of Pennsylvania vacant-lot RCT."
            ),
            "projected_leverage_ratio": "2.8x — each $1 of public success "
                                        "payment mobilizes $2.80 in private "
                                        "capital and avoided public cost",
            "legal_structure": (
                "Pay-for-Success contract between the City and an SPV organized "
                "as a Delaware LLC. Governed by Pennsylvania's Act 55 (2014) "
                "enabling social impact bonds for state and municipal use."
            ),
        },
        "tags": [
            "pay-for-success",
            "social-impact-bond",
            "health-outcomes",
            "vacant-lot-greening",
            "evidence-based",
        ],
    },
    # ── 3. Micro-Impact Fund ──────────────────────────────────────────────
    {
        "title": "Micro-Impact Fund",
        "summary": (
            "A crowdfunded neighborhood activation pool that lets residents "
            "invest $25-$500 in hyper-local lot transformations, earning modest "
            "returns from event revenue, vendor fees, and micro-lease income."
        ),
        "category": "community-finance",
        "impact_level": 4,
        "feasibility": 4,
        "novelty": 5,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "funding_mechanism": (
                "Regulation CF (Regulation Crowdfunding) offering through an "
                "SEC-registered portal. Each neighborhood fund targets $5K-$50K, "
                "pooling micro-investments into a community-governed LLC that "
                "leases and activates a specific lot cluster."
            ),
            "total_capital": "$2.5M aggregate across 80 neighborhood funds in "
                             "the pilot phase, with average fund size of $31K",
            "investor_returns": (
                "Revenue-share notes returning 3-6 % annually from pop-up market "
                "vendor fees, event ticket splits, seasonal produce sales, and "
                "small-scale advertising. Returns subordinate to a community "
                "benefit reserve that funds ongoing maintenance."
            ),
            "repayment_source": (
                "Direct operating revenue from activated lots: vendor stall "
                "rental ($50-$150/day), event hosting fees, mobile food permits, "
                "and community garden plot subscriptions ($75/season)."
            ),
            "risk_profile": (
                "Low-Moderate. Small ticket sizes distribute risk widely. "
                "Principal risk is insufficient activation revenue in "
                "lower-traffic neighborhoods. Mitigated by a philanthropic "
                "backstop from Knight Foundation covering first two years of "
                "operating shortfalls."
            ),
            "projected_leverage_ratio": "1.8x — modest but meaningful, "
                                        "reflecting the grassroots scale and "
                                        "low overhead of the model",
            "legal_structure": (
                "Series LLC under Pennsylvania law, with each neighborhood fund "
                "as a protected series. Reg CF offering statement filed with the "
                "SEC; maximum raise of $5M aggregate in any 12-month period."
            ),
        },
        "tags": [
            "crowdfunding",
            "community-investment",
            "micro-finance",
            "neighborhood-activation",
            "regulation-cf",
        ],
    },
    # ── 4. Tax Increment Greening District ────────────────────────────────
    {
        "title": "Tax Increment Greening District",
        "summary": (
            "A TIF variant that captures incremental property tax revenue within "
            "designated green-infrastructure corridors and reinvests it "
            "exclusively into public space activation, stormwater management, "
            "and tree canopy expansion."
        ),
        "category": "tax-incentives",
        "impact_level": 5,
        "feasibility": 2,
        "novelty": 4,
        "time_horizon": "far",
        "status": "review",
        "details": {
            "funding_mechanism": (
                "Tax Increment Financing district established by City Council "
                "ordinance. The frozen base-year assessed value continues to "
                "service existing obligations; all incremental tax revenue above "
                "the base flows into a Greening District Fund administered by a "
                "new quasi-public authority."
            ),
            "total_capital": "$120M over a 25-year district life, assuming 4.5 % "
                             "annual assessed-value growth in pilot corridors "
                             "along Germantown Avenue and Kensington Avenue",
            "investor_returns": (
                "TIF bonds sold to institutional investors at 4.0-4.5 % "
                "tax-exempt yield. Returns are competitive with standard "
                "municipal TIF paper but carry a green certification premium "
                "that attracts ESG-dedicated capital."
            ),
            "repayment_source": (
                "Incremental real-estate tax revenue above the frozen base "
                "within the designated district boundaries. Secondary source: "
                "stormwater fee credits from Philadelphia Water Department for "
                "permeable green infrastructure installed by the district."
            ),
            "risk_profile": (
                "Moderate-High. TIF districts carry concentration risk — if the "
                "corridor does not appreciate, increment revenue underperforms. "
                "Mitigated by conservative growth assumptions (4.5 % vs. "
                "citywide 6.2 % recent trend), moral-obligation backstop from "
                "the City, and diversification across two non-contiguous corridors."
            ),
            "projected_leverage_ratio": "5.5x — strongest leverage in the "
                                        "portfolio due to the compounding "
                                        "nature of assessed-value growth over "
                                        "a 25-year horizon",
            "legal_structure": (
                "TIF district created under Pennsylvania's Tax Increment "
                "Financing Act (Act 113 of 1990, as amended). Requires City "
                "Council approval, School District of Philadelphia consent for "
                "the education share, and a formal blight finding for the "
                "designated area."
            ),
        },
        "tags": [
            "tax-increment-financing",
            "green-infrastructure",
            "stormwater",
            "corridor-revitalization",
            "long-term-capital",
        ],
    },
    # ── 5. Space Activation Revenue Share ─────────────────────────────────
    {
        "title": "Space Activation Revenue Share",
        "summary": (
            "A structured revenue-sharing agreement between the City and "
            "community operators where net income from activated vacant lots is "
            "split on a sliding scale that rewards sustained community stewardship."
        ),
        "category": "public-private-partnership",
        "impact_level": 4,
        "feasibility": 4,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "funding_mechanism": (
                "License agreements between the Philadelphia Land Bank and "
                "qualified Community Development Corporations (CDCs). The Land "
                "Bank contributes the lot at zero cost; the CDC raises activation "
                "capital through a blended stack of Rebuild initiative grants, "
                "LISC Philadelphia loans, and retained revenue."
            ),
            "total_capital": "$8M in aggregate activation investment across "
                             "200 lots in years 1-3, with average per-lot "
                             "capital expenditure of $40K",
            "investor_returns": (
                "Not a traditional investment — returns accrue as community "
                "wealth. The sliding-scale split starts at 80/20 (community/City) "
                "in year 1 and shifts to 60/40 by year 5, incentivizing early "
                "community ownership. City share funds a Lot Activation "
                "Revolving Fund for future sites."
            ),
            "repayment_source": (
                "Gross revenue from lot operations: farmers-market stall fees, "
                "event rentals, seasonal programming sponsorships, parking "
                "revenue during stadium events (for lots near sports complexes), "
                "and solar micro-grid energy credits."
            ),
            "risk_profile": (
                "Low. City exposure is limited to foregone land-sale revenue "
                "(minimal for lots that have sat vacant for 5+ years). Community "
                "operator risk is capped by the license structure — no debt "
                "obligation, voluntary exit with 90-day notice."
            ),
            "projected_leverage_ratio": "3.1x — reflects the value of the "
                                        "contributed land asset and the "
                                        "multiplier effect of community "
                                        "programming on surrounding commerce",
            "legal_structure": (
                "Revocable license agreement (not a lease, preserving City "
                "ownership) under the Philadelphia Land Bank's enabling statute "
                "(Act 153 of 2012). Revenue-share terms codified in a standard "
                "Community Activation Agreement template approved by the City "
                "Solicitor."
            ),
        },
        "tags": [
            "revenue-share",
            "land-bank",
            "community-development",
            "public-private-partnership",
            "rebuild-initiative",
        ],
    },
    # ── 6. Philanthropic Match Accelerator ────────────────────────────────
    {
        "title": "Philanthropic Match Accelerator",
        "summary": (
            "A 3:1 matching fund that amplifies community-raised dollars for "
            "space activation projects, blending philanthropic capital from "
            "anchor foundations with grassroots fundraising to accelerate lot "
            "transformation at neighborhood scale."
        ),
        "category": "philanthropic-finance",
        "impact_level": 4,
        "feasibility": 5,
        "novelty": 3,
        "time_horizon": "near",
        "status": "approved",
        "details": {
            "funding_mechanism": (
                "Pooled philanthropic fund anchored by the William Penn "
                "Foundation ($5M), Knight Foundation ($3M), and the Lenfest "
                "Foundation ($2M). For every $1 raised by a neighborhood "
                "association or CDC through local fundraising, the Accelerator "
                "matches $3, up to $150K per project."
            ),
            "total_capital": "$10M philanthropic pool seeding $13.3M total "
                             "when combined with community match contributions, "
                             "funding approximately 90 activation projects",
            "investor_returns": (
                "No financial return — purely catalytic capital. Foundations "
                "receive impact reporting aligned with their program areas: "
                "creative placemaking (Knight), environment and watershed "
                "health (William Penn), and civic infrastructure (Lenfest). "
                "Community co-investment requirement ensures skin-in-the-game "
                "accountability."
            ),
            "repayment_source": (
                "Non-repayable grant capital. Sustainability ensured through "
                "a mandatory operating endowment contribution: 10 % of each "
                "project's matched funds are set aside in a neighborhood "
                "stewardship endowment invested in a balanced portfolio, "
                "generating income to cover annual maintenance."
            ),
            "risk_profile": (
                "Low. Grant capital carries no repayment risk. Principal "
                "concern is absorptive capacity — ensuring enough community "
                "organizations have the project-management capability to deploy "
                "funds effectively. Mitigated by a technical-assistance program "
                "funded from the pool's 5 % admin allocation."
            ),
            "projected_leverage_ratio": "3.0x match ratio by design, with "
                                        "an effective 4.5x when accounting "
                                        "for volunteer labor and in-kind "
                                        "donations typically accompanying "
                                        "community-led projects",
            "legal_structure": (
                "Fiscal sponsorship through a 501(c)(3) intermediary (e.g., "
                "the Philadelphia Foundation). Donor-advised fund structure "
                "for each anchor funder, with a shared investment committee "
                "governing match approvals. Community applicants submit through "
                "a streamlined RFP process twice annually."
            ),
        },
        "tags": [
            "philanthropic-match",
            "catalytic-capital",
            "community-fundraising",
            "william-penn-foundation",
            "knight-foundation",
        ],
    },
]

# ---------------------------------------------------------------------------
# Generator Templates (8)
# ---------------------------------------------------------------------------

TEMPLATES: list[dict] = [
    # ── T1. Community Land Trust Revenue Model ────────────────────────────
    {
        "title": "Community Land Trust Revenue Model",
        "summary": (
            "Template for structuring a Community Land Trust that generates "
            "sustainable revenue from ground leases, community land fees, and "
            "shared-equity appreciation on activated parcels."
        ),
        "category": "community-finance",
        "time_horizon": "far",
        "impact_range": [4, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [3, 4],
        "details": {
            "funding_mechanism": (
                "Acquisition capital from city land disposition programs and "
                "CDBG funds. Ongoing revenue from 99-year ground leases to "
                "community operators, shared-equity formulas on any future "
                "development, and annual stewardship fees."
            ),
            "total_capital": "$15M-$40M depending on parcel portfolio size",
            "legal_structure": (
                "501(c)(3) community land trust organized under Pennsylvania "
                "nonprofit corporation law, with tripartite board governance "
                "(residents, community members, public representatives)."
            ),
            "risk_profile": (
                "Low-Moderate. Land trust model has 50+ year track record "
                "nationally. Key risk is political interference with land "
                "disposition pipeline."
            ),
        },
        "tags": [
            "community-land-trust",
            "shared-equity",
            "ground-lease",
            "long-term-stewardship",
        ],
    },
    # ── T2. Opportunity Zone Activation Fund ──────────────────────────────
    {
        "title": "Opportunity Zone Activation Fund",
        "summary": (
            "Template for a Qualified Opportunity Fund targeting vacant-lot "
            "activation in Philadelphia's 42 designated Opportunity Zones, "
            "unlocking capital gains deferrals and step-up basis for investors."
        ),
        "category": "impact-investing",
        "time_horizon": "medium",
        "impact_range": [3, 5],
        "feasibility_range": [3, 4],
        "novelty_range": [3, 4],
        "details": {
            "funding_mechanism": (
                "Qualified Opportunity Fund (QOF) organized as a partnership. "
                "Investors contribute realized capital gains and receive federal "
                "tax benefits: deferral until 2026, 10 % basis step-up at 5 "
                "years, and full exclusion of QOF appreciation at 10 years."
            ),
            "total_capital": "$20M-$80M target, with minimum LP commitment "
                             "of $250K",
            "legal_structure": (
                "Delaware LP with a Philadelphia-based GP entity. Must maintain "
                "90 % of assets in Qualified Opportunity Zone Property as "
                "certified by annual compliance testing."
            ),
            "investor_returns": (
                "Target 10-14 % net IRR over 10-year hold, inclusive of tax "
                "benefits. Cash-on-cash distributions begin in year 3 from "
                "operating income."
            ),
        },
        "tags": [
            "opportunity-zones",
            "capital-gains",
            "tax-incentives",
            "place-based-investing",
        ],
    },
    # ── T3. Stormwater Credit Trading Platform ────────────────────────────
    {
        "title": "Stormwater Credit Trading Platform",
        "summary": (
            "Template for monetizing green infrastructure on activated lots "
            "through Philadelphia Water Department stormwater credit trading, "
            "creating a recurring revenue stream from impervious-surface offsets."
        ),
        "category": "environmental-finance",
        "time_horizon": "medium",
        "impact_range": [3, 4],
        "feasibility_range": [3, 5],
        "novelty_range": [4, 5],
        "details": {
            "funding_mechanism": (
                "Green infrastructure installations on activated lots generate "
                "stormwater credits tradable under Philadelphia's parcel-based "
                "billing system. Property owners with impervious surfaces "
                "purchase credits to reduce their stormwater fees."
            ),
            "total_capital": "$3M-$8M in green infrastructure installation "
                             "across 300+ lots",
            "risk_profile": (
                "Moderate. Revenue depends on continued regulatory support for "
                "credit trading. Philadelphia Water Department has signaled "
                "strong commitment to green infrastructure incentives through "
                "its Green City Clean Waters program."
            ),
            "legal_structure": (
                "Credit-generating entity structured as a social enterprise LLC "
                "or B-Corp. Bilateral credit purchase agreements with commercial "
                "property owners; registry maintained by a third-party verifier."
            ),
        },
        "tags": [
            "stormwater-credits",
            "green-infrastructure",
            "water-department",
            "environmental-markets",
        ],
    },
    # ── T4. Vacant Lot Insurance Pool ─────────────────────────────────────
    {
        "title": "Vacant Lot Insurance Pool",
        "summary": (
            "Template for a shared insurance mechanism that reduces liability "
            "costs for community lot activators by pooling risk across hundreds "
            "of sites and negotiating group coverage with underwriters."
        ),
        "category": "risk-management",
        "time_horizon": "near",
        "impact_range": [3, 4],
        "feasibility_range": [4, 5],
        "novelty_range": [3, 4],
        "details": {
            "funding_mechanism": (
                "Annual premium pool funded by participating community "
                "organizations ($200-$800/lot/year based on activity level). "
                "City contributes a risk-mitigation subsidy covering 40 % of "
                "premiums for the first three years."
            ),
            "total_capital": "$1.5M-$3M annual premium pool covering "
                             "500-1,000 activated lots",
            "risk_profile": (
                "Low. Actuarial data from similar programs (Cleveland, Detroit) "
                "shows claim rates below 2 % for managed community green spaces. "
                "Catastrophic coverage via a reinsurance treaty."
            ),
            "legal_structure": (
                "Group captive insurance arrangement or risk-retention group "
                "organized under Pennsylvania's Insurance Company Law. "
                "Administered by a licensed TPA with community-organization "
                "governance board."
            ),
        },
        "tags": [
            "insurance",
            "risk-pooling",
            "liability",
            "community-activation",
        ],
    },
    # ── T5. Carbon Sequestration Micro-Credits ────────────────────────────
    {
        "title": "Carbon Sequestration Micro-Credits",
        "summary": (
            "Template for generating and selling verified carbon offset credits "
            "from urban tree planting, soil restoration, and biomass cultivation "
            "on activated vacant lots."
        ),
        "category": "environmental-finance",
        "time_horizon": "far",
        "impact_range": [3, 5],
        "feasibility_range": [2, 3],
        "novelty_range": [4, 5],
        "details": {
            "funding_mechanism": (
                "Aggregated urban carbon credits verified under Verra's VCS or "
                "Gold Standard, bundled across hundreds of lots to reach "
                "minimum viable issuance thresholds. Sold to corporate buyers "
                "seeking urban-impact offsets with strong co-benefit narratives."
            ),
            "total_capital": "$500K-$2M in monitoring and verification "
                             "infrastructure; revenue of $8-$25/ton CO2e",
            "legal_structure": (
                "Carbon credit aggregator organized as a cooperative or "
                "nonprofit. Each lot operator assigns sequestration rights via "
                "a standardized contribution agreement. Credits registered on "
                "a public blockchain ledger for transparency."
            ),
            "risk_profile": (
                "High. Urban micro-scale carbon projects face permanence "
                "challenges and high per-unit verification costs. Viable only "
                "at scale (1,000+ lots) and with methodological innovation "
                "in urban carbon measurement."
            ),
        },
        "tags": [
            "carbon-credits",
            "urban-forestry",
            "sequestration",
            "voluntary-carbon-market",
        ],
    },
    # ── T6. Blended Capital Stack Blueprint ───────────────────────────────
    {
        "title": "Blended Capital Stack Blueprint",
        "summary": (
            "Template for assembling layered financing that combines "
            "philanthropic first-loss capital, CDFI debt, New Markets Tax "
            "Credits, and market-rate equity into a single activation fund."
        ),
        "category": "blended-finance",
        "time_horizon": "medium",
        "impact_range": [4, 5],
        "feasibility_range": [2, 4],
        "novelty_range": [3, 5],
        "details": {
            "funding_mechanism": (
                "Four-layer capital stack: (1) philanthropic first-loss equity "
                "at 0 % return, (2) CDFI mezzanine debt at 3-5 %, (3) New "
                "Markets Tax Credit allocation providing 39 % federal credit "
                "over 7 years, (4) market-rate senior debt from regional banks "
                "seeking CRA credit."
            ),
            "total_capital": "$25M-$60M depending on NMTC allocation size",
            "investor_returns": (
                "Blended cost of capital of 2.8-4.2 %, significantly below "
                "market rate. Senior lenders receive 5-6 % with NMTC subsidy "
                "effectively reducing their risk-adjusted return requirement."
            ),
            "legal_structure": (
                "Master fund with subsidiary CDEs (Community Development "
                "Entities) for NMTC compliance. Leveraged structure with "
                "investor entity making Qualified Equity Investment and "
                "lending proceeds to the QALICB project entity."
            ),
        },
        "tags": [
            "blended-finance",
            "new-markets-tax-credits",
            "cdfi",
            "capital-stack",
            "cra-credit",
        ],
    },
    # ── T7. Municipal Land Lease-Back Instrument ──────────────────────────
    {
        "title": "Municipal Land Lease-Back Instrument",
        "summary": (
            "Template for a sale-leaseback arrangement where the City sells "
            "vacant parcels to a trust and leases them back for community use, "
            "unlocking one-time capital while preserving long-term public access."
        ),
        "category": "public-private-partnership",
        "time_horizon": "medium",
        "impact_range": [3, 4],
        "feasibility_range": [3, 4],
        "novelty_range": [3, 4],
        "details": {
            "funding_mechanism": (
                "City sells a portfolio of vacant lots to a mission-aligned "
                "real-estate trust at appraised value. Simultaneously executes "
                "a 30-year ground lease at nominal rent ($1/year) with community "
                "activation covenants. City deploys sale proceeds into a "
                "Space Activation Endowment."
            ),
            "total_capital": "$10M-$30M from portfolio sale; endowment "
                             "generates $400K-$1.2M annually for activation",
            "risk_profile": (
                "Moderate. Political risk around perceived privatization of "
                "public land. Mitigated by iron-clad lease-back covenants, "
                "community oversight board, and reverter clauses that return "
                "land to the City if activation covenants are violated."
            ),
            "legal_structure": (
                "Real estate investment trust (REIT) or mission-driven LLC "
                "as purchaser. Master ground lease with community benefit "
                "agreement attached as a restrictive covenant running with "
                "the land. Requires City Council approval for disposition."
            ),
        },
        "tags": [
            "sale-leaseback",
            "land-disposition",
            "endowment",
            "public-access",
            "covenant",
        ],
    },
    # ── T8. Digital Space Token Economy ────────────────────────────────────
    {
        "title": "Digital Space Token Economy",
        "summary": (
            "Template for a blockchain-based community token that represents "
            "governance rights, usage credits, and revenue participation in "
            "activated public spaces — enabling frictionless micro-transactions "
            "and transparent fund allocation."
        ),
        "category": "fintech-innovation",
        "time_horizon": "far",
        "impact_range": [3, 5],
        "feasibility_range": [2, 3],
        "novelty_range": [5, 5],
        "details": {
            "funding_mechanism": (
                "Utility token issued on a public blockchain (Ethereum L2 or "
                "Solana for low gas fees). Tokens are earned through community "
                "participation (volunteering, attending events) and spent on "
                "space reservations, vendor access, and governance votes. "
                "Initial liquidity seeded by a philanthropic token purchase."
            ),
            "total_capital": "$1M-$5M seed liquidity; ongoing value accrual "
                             "through transaction fees and token burns",
            "legal_structure": (
                "Utility token structured to avoid securities classification "
                "under the Howey test — no expectation of profit from the "
                "efforts of others. Legal opinion from fintech counsel. "
                "DAO governance framework with multi-sig treasury management. "
                "Compliance with Pennsylvania's Money Transmitter Act via "
                "exemption for closed-loop tokens."
            ),
            "risk_profile": (
                "High. Regulatory uncertainty around token classification, "
                "user adoption barriers, and technology risk. Suitable only "
                "as a long-horizon experimental pilot with capped exposure. "
                "Mitigated by phased rollout starting with a single "
                "neighborhood and paper-token fallback."
            ),
        },
        "tags": [
            "blockchain",
            "community-token",
            "dao-governance",
            "fintech",
            "experimental",
        ],
    },
]
