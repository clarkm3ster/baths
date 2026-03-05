// DOMES Innovation Laboratory — API Client
// Types match backend response format. Includes domain config, readiness
// mapping, connection graph, and brief generator.

// ─── Types ──────────────────────────────────────────────────────────────────────

export interface Teammate {
  id: number;
  slug: string;
  name: string;
  title: string;
  domain: string;
  description: string;
  color: string;
  icon_symbol: string;
  status: string;
  created_at: string;
  innovation_count: number;
  innovations?: Innovation[];
}

export interface Innovation {
  id: number;
  teammate_id: number;
  title: string;
  summary: string;
  domain: string;
  category: string;
  impact_level: number;
  feasibility: number;
  novelty: number;
  time_horizon: 'near' | 'medium' | 'far';
  status: string;
  details: Record<string, unknown>;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export type Readiness = 'immediate' | '1-year' | '5-year' | 'moonshot';

// ─── Domain Configuration (11 research domains, excluding Architect) ────────

export interface DomainConfig {
  slug: string;
  label: string;
  description: string;
  icon: string;
  color: string;
  backendDomain: string; // maps to Innovation.domain field from backend
}

export const DOMAINS: DomainConfig[] = [
  { slug: 'fiscal-alchemist', label: 'Financing', description: 'Creative funding mechanisms, Dome Bonds, person-centered budgets', icon: '$', color: '#C9A726', backendDomain: 'creative-financing' },
  { slug: 'impact-investor', label: 'Investment', description: 'Impact investment products, Outcomes Marketplace, social finance', icon: '%', color: '#2E8B57', backendDomain: 'impact-investment' },
  { slug: 'data-inventor', label: 'Data / Privacy', description: 'Data wallets, federated queries, consent platforms, AI matching', icon: '#', color: '#4169E1', backendDomain: 'data-innovation' },
  { slug: 'tech-futurist', label: 'Technology', description: 'AR overlays, voice interfaces, wearable Dome ID, real-time monitoring', icon: '>', color: '#9333EA', backendDomain: 'emerging-technology' },
  { slug: 'legislative-inventor', label: 'Legislation', description: 'THE DOME ACT, RIGHT TO YOUR DOME, model laws with full text', icon: '§', color: '#DC2626', backendDomain: 'model-legislation' },
  { slug: 'regulatory-hacker', label: 'Regulatory', description: 'Medicaid waivers, CMMI models, existing authority pathways', icon: '!', color: '#EA580C', backendDomain: 'regulatory-reform' },
  { slug: 'service-designer', label: 'Service Design', description: 'Dome Navigator profession, Dome Centers, peer support, transitions', icon: '*', color: '#0891B2', backendDomain: 'service-design' },
  { slug: 'space-architect', label: 'Physical Space', description: 'Dome Center designs at 3 scales, anti-pattern library', icon: '□', color: '#6D28D9', backendDomain: 'space-design' },
  { slug: 'measurement-scientist', label: 'Measurement', description: 'Dome Index (0-100), outcomes framework, evaluation dashboards', icon: '=', color: '#059669', backendDomain: 'impact-measurement' },
  { slug: 'narrative-researcher', label: 'Narrative', description: 'Documentary series, testimony generator, journalism toolkit', icon: '~', color: '#DB2777', backendDomain: 'narrative-research' },
  { slug: 'market-maker', label: 'Market', description: 'Dome Certification, workforce sizing, international adaptation', icon: '&', color: '#CA8A04', backendDomain: 'social-markets' },
];

export function getDomain(slug: string): DomainConfig | undefined {
  return DOMAINS.find(d => d.slug === slug);
}

export function getDomainByBackend(backendDomain: string): DomainConfig | undefined {
  return DOMAINS.find(d => d.backendDomain === backendDomain);
}

// ─── Readiness Mapping ──────────────────────────────────────────────────────

export function getReadiness(inn: Innovation): Readiness {
  if (inn.time_horizon === 'near') return 'immediate';
  if (inn.time_horizon === 'medium') return '1-year';
  // far horizon
  if (inn.feasibility <= 2 || inn.novelty >= 5) return 'moonshot';
  return '5-year';
}

export const READINESS_ORDER: Readiness[] = ['immediate', '1-year', '5-year', 'moonshot'];

export const READINESS_CONFIG: Record<Readiness, { label: string; short: string; description: string; color: string }> = {
  immediate: { label: 'IMMEDIATE', short: 'NOW', description: 'Deploy tomorrow with existing authority', color: '#059669' },
  '1-year':  { label: '1-YEAR',    short: '1YR', description: 'Needs some legislation or funding',    color: '#D97706' },
  '5-year':  { label: '5-YEAR',    short: '5YR', description: 'Requires systemic change',             color: '#DC2626' },
  moonshot:  { label: 'MOONSHOT',   short: '!!',  description: 'Paradigm shift innovations',           color: '#9333EA' },
};

export function getReadinessBreakdown(innovations: Innovation[]): Record<Readiness, number> {
  const result: Record<Readiness, number> = { immediate: 0, '1-year': 0, '5-year': 0, moonshot: 0 };
  for (const inn of innovations) {
    result[getReadiness(inn)]++;
  }
  return result;
}

// ─── Connection Graph ───────────────────────────────────────────────────────

export interface Connection {
  from: string; // teammate slug
  to: string;
  reason: string;
  strength: number; // 1-10
}

export const CONNECTIONS: Connection[] = [
  { from: 'fiscal-alchemist', to: 'impact-investor', reason: 'Dome Bonds create investable instruments for the Outcomes Marketplace', strength: 9 },
  { from: 'impact-investor', to: 'measurement-scientist', reason: 'Investment returns depend on verified outcome measurement via Dome Index', strength: 9 },
  { from: 'measurement-scientist', to: 'data-inventor', reason: 'Outcomes measurement requires cross-system data infrastructure', strength: 9 },
  { from: 'data-inventor', to: 'tech-futurist', reason: 'Data wallets and federated queries need emerging privacy technology', strength: 8 },
  { from: 'tech-futurist', to: 'service-designer', reason: 'AR overlays and voice interfaces enable new service delivery models', strength: 7 },
  { from: 'service-designer', to: 'space-architect', reason: 'Dome Navigator profession defines Dome Center physical requirements', strength: 8 },
  { from: 'legislative-inventor', to: 'regulatory-hacker', reason: 'DOME ACT creates mandate; Regulatory Hacker finds existing authority shortcuts', strength: 9 },
  { from: 'regulatory-hacker', to: 'fiscal-alchemist', reason: 'Medicaid waivers and CMMI models unlock new coordination financing', strength: 8 },
  { from: 'narrative-researcher', to: 'legislative-inventor', reason: 'Documentary evidence and testimony drive legislative action on DOME ACT', strength: 7 },
  { from: 'market-maker', to: 'impact-investor', reason: 'Dome Certification creates market demand; investors fund certified agencies', strength: 8 },
  { from: 'market-maker', to: 'service-designer', reason: 'Workforce sizing determines how many Dome Navigators America needs', strength: 7 },
  { from: 'measurement-scientist', to: 'narrative-researcher', reason: 'Dome Index quantitative scores need qualitative storytelling context', strength: 7 },
  { from: 'fiscal-alchemist', to: 'measurement-scientist', reason: 'Coordination savings calculations require rigorous Dome Index measurement', strength: 8 },
  { from: 'data-inventor', to: 'regulatory-hacker', reason: 'Cross-system data sharing requires navigating HIPAA, FERPA, and state privacy laws', strength: 8 },
  { from: 'space-architect', to: 'narrative-researcher', reason: 'Anti-pattern library tells the story of what dignity looks like in physical space', strength: 6 },
  { from: 'legislative-inventor', to: 'service-designer', reason: 'COORDINATION MANDATE defines service integration requirements for Dome Navigators', strength: 7 },
  { from: 'fiscal-alchemist', to: 'space-architect', reason: 'Dome Bonds finance Dome Center construction at all three scales', strength: 7 },
  { from: 'market-maker', to: 'measurement-scientist', reason: 'Dome Certification assessment criteria built on Dome Index methodology', strength: 8 },
];

// ─── Brief Generation ───────────────────────────────────────────────────────

type AudienceKey = 'governor' | 'cms' | 'investor' | 'legislature';

export const AUDIENCES: { key: AudienceKey; label: string; description: string }[] = [
  { key: 'governor', label: "Governor's Office", description: 'Executive summary, policy implications, fiscal impact' },
  { key: 'cms', label: 'CMS / Federal Agency', description: 'Federal compliance, waiver opportunities, demonstration models' },
  { key: 'investor', label: 'Impact Investor', description: 'ROI projections, risk analysis, market opportunity' },
  { key: 'legislature', label: 'State Legislature', description: 'Legislative framework, constituent impact, cost analysis' },
];

export function generateBrief(
  domainSlug: string,
  readiness: Readiness | 'all',
  audience: AudienceKey,
  innovations: Innovation[],
): string {
  const domain = getDomain(domainSlug);
  if (!domain) return 'Domain not found.';

  const domainInnovations = innovations.filter(i => i.domain === domain.backendDomain);
  const filtered = readiness === 'all'
    ? domainInnovations
    : domainInnovations.filter(i => getReadiness(i) === readiness);

  if (filtered.length === 0) return 'No innovations match the selected criteria.';

  const audienceLabel = AUDIENCES.find(a => a.key === audience)?.label ?? audience;
  const readinessLabel = readiness === 'all' ? 'All Readiness Levels' : READINESS_CONFIG[readiness].label;
  const date = new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });

  const line = '═'.repeat(72);
  const dash = '─'.repeat(72);

  let b = '';
  b += `${line}\n`;
  b += `DOMES INNOVATION LABORATORY\n`;
  b += `${domain.label.toUpperCase()} DOMAIN BRIEF\n`;
  b += `${line}\n\n`;
  b += `Prepared for:  ${audienceLabel}\n`;
  b += `Domain:        ${domain.label} — ${domain.description}\n`;
  b += `Readiness:     ${readinessLabel}\n`;
  b += `Innovations:   ${filtered.length}\n`;
  b += `Date:          ${date}\n\n`;

  // Executive summary
  b += `${dash}\nEXECUTIVE SUMMARY\n${dash}\n\n`;
  b += audienceOpener(audience, domain, filtered);
  b += '\n\n';

  // Each innovation
  for (const inn of filtered) {
    const r = getReadiness(inn);
    b += `${dash}\n`;
    b += `${inn.title.toUpperCase()}\n`;
    b += `Readiness: ${READINESS_CONFIG[r].label} | Impact: ${inn.impact_level}/5 | Feasibility: ${inn.feasibility}/5 | Novelty: ${inn.novelty}/5\n`;
    b += `${dash}\n\n`;
    b += `${inn.summary}\n\n`;

    // Render details
    if (inn.details && typeof inn.details === 'object') {
      for (const [key, value] of Object.entries(inn.details)) {
        const label = key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
        if (Array.isArray(value)) {
          b += `${label}:\n`;
          for (const item of value) {
            b += typeof item === 'object' ? `  - ${JSON.stringify(item)}\n` : `  - ${item}\n`;
          }
        } else if (typeof value === 'object' && value !== null) {
          b += `${label}:\n`;
          for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
            const subLabel = k.replace(/_/g, ' ');
            if (typeof v === 'object' && v !== null) {
              b += `  ${subLabel}: ${JSON.stringify(v)}\n`;
            } else {
              b += `  ${subLabel}: ${v}\n`;
            }
          }
        } else {
          b += `${label}: ${value}\n`;
        }
        b += '\n';
      }
    }
  }

  // Next steps
  b += `${line}\nNEXT STEPS\n${line}\n\n`;
  b += audienceClosing(audience, filtered);
  b += '\n\n';
  b += `${dash}\n`;
  b += `Generated by DOMES Innovation Laboratory\n`;
  b += `For questions: DOMES Lab Research Team\n`;

  return b;
}

function audienceOpener(audience: AudienceKey, domain: DomainConfig, innovations: Innovation[]): string {
  const count = innovations.length;
  const immediate = innovations.filter(i => getReadiness(i) === 'immediate').length;
  switch (audience) {
    case 'governor':
      return `The DOMES Lab has developed ${count} innovations in ${domain.label} that can transform coordination across your state's human services agencies. ${immediate > 0 ? `${immediate} can be deployed immediately using existing authority.` : 'These represent strategic investments in cross-system coordination.'} Below is a detailed briefing on each innovation with implementation paths and fiscal projections.`;
    case 'cms':
      return `The DOMES Lab presents ${count} innovations in ${domain.label} aligned with CMS goals of reducing fragmentation and improving beneficiary outcomes. Each innovation has been analyzed for compatibility with existing federal authorities including Section 1115, CMMI, and Medicaid administrative claiming.`;
    case 'investor':
      return `The DOMES Lab has identified ${count} investment-ready innovations in ${domain.label} with documented social returns and defined risk profiles. Government coordination represents a $740B+ market with significant inefficiency — these innovations capture value from reducing fragmentation.`;
    case 'legislature':
      return `The DOMES Lab presents ${count} legislative innovations in ${domain.label} designed for bipartisan support. Each addresses documented coordination failures that cost taxpayers billions and harm families. Fiscal notes, constituent impact analyses, and model text are provided.`;
  }
}

function audienceClosing(audience: AudienceKey, innovations: Innovation[]): string {
  const immediate = innovations.filter(i => getReadiness(i) === 'immediate');
  switch (audience) {
    case 'governor':
      return immediate.length > 0
        ? `Recommended immediate action:\n${immediate.map(i => `  1. ${i.title} — can be launched by executive order or existing agency authority`).join('\n')}\n\nRequest a 30-minute briefing with the DOMES Lab team to discuss implementation timelines and pilot site selection.`
        : 'Request a 30-minute briefing with the DOMES Lab team to discuss implementation timelines, legislative requirements, and pilot site selection.';
    case 'cms':
      return 'We request a meeting with CMMI leadership to discuss alignment with current Innovation Center priorities. These innovations are designed to complement existing demonstration models and can be integrated into forthcoming NOFOs.';
    case 'investor':
      return 'We invite interested investors to a detailed diligence session where we will present financial models, risk analyses, and projected returns for each innovation. Minimum investment threshold and fund structure available upon request.';
    case 'legislature':
      return 'Model legislative text, fiscal notes, and constituent impact analyses are available for each innovation. We recommend scheduling committee testimony and constituent roundtables to build support for a comprehensive coordination reform package.';
  }
}

// ─── API Layer ──────────────────────────────────────────────────────────────

const API_BASE = '/api';

async function fetchJSON<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...options?.headers },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
  const envelope = await res.json();
  if (envelope.status === 'ok' && envelope.data !== undefined) return envelope.data as T;
  return envelope as T;
}

// ─── Demo Fallback Data ─────────────────────────────────────────────────────
// Used when backend is not running. Subset of real seed data.

const DEMO_TEAMMATES: Teammate[] = [
  { id: 1, slug: 'fiscal-alchemist', name: 'Fiscal Alchemist', title: 'Creative Financing Specialist', domain: 'creative-financing', description: 'Transforms conventional funding into innovative financing mechanisms — tax increment financing, social impact bonds, blended capital stacks, and CDFIs.', color: '#C9A726', icon_symbol: '♦', status: 'active', created_at: '2025-12-01T00:00:00Z', innovation_count: 6 },
  { id: 2, slug: 'impact-investor', name: 'Impact Investor', title: 'Social Impact Investment Strategist', domain: 'impact-investment', description: 'Designs social impact investment models aligning financial returns with measurable social outcomes.', color: '#2E8B57', icon_symbol: '▲', status: 'active', created_at: '2025-12-01T00:00:00Z', innovation_count: 4 },
  { id: 3, slug: 'data-inventor', name: 'Data Inventor', title: 'Novel Data Methods Pioneer', domain: 'data-innovation', description: 'Invents new approaches to data collection, linkage, and analysis for human services.', color: '#4169E1', icon_symbol: '◆', status: 'active', created_at: '2025-12-01T00:00:00Z', innovation_count: 5 },
  { id: 4, slug: 'tech-futurist', name: 'Tech Futurist', title: 'Emerging Technology Researcher', domain: 'emerging-technology', description: 'Explores cutting-edge technology for government services — blockchain, AI, IoT, digital identity.', color: '#9333EA', icon_symbol: '★', status: 'active', created_at: '2025-12-01T00:00:00Z', innovation_count: 5 },
  { id: 5, slug: 'legislative-inventor', name: 'Legislative Inventor', title: 'Model Legislation Architect', domain: 'model-legislation', description: 'Drafts innovative model legislation enabling systemic reform — enabling statutes, regulatory sandboxes, interstate compacts.', color: '#DC2626', icon_symbol: '§', status: 'active', created_at: '2025-12-01T00:00:00Z', innovation_count: 5 },
  { id: 6, slug: 'regulatory-hacker', name: 'Regulatory Hacker', title: 'Regulatory Reform Strategist', domain: 'regulatory-reform', description: 'Finds creative pathways through regulatory frameworks — waivers, demonstration projects, MOUs.', color: '#EA580C', icon_symbol: '⚒', status: 'active', created_at: '2025-12-01T00:00:00Z', innovation_count: 4 },
  { id: 7, slug: 'service-designer', name: 'Service Designer', title: 'Human-Centered Service Expert', domain: 'service-design', description: 'Reimagines government service delivery through human-centered design — journey mapping, no-wrong-door, trauma-informed design.', color: '#0891B2', icon_symbol: '❀', status: 'active', created_at: '2025-12-01T00:00:00Z', innovation_count: 5 },
  { id: 8, slug: 'space-architect', name: 'Space Architect', title: 'Physical Space Designer', domain: 'space-design', description: 'Designs physical environments that enhance service delivery and client dignity — Dome Centers, mobile units, virtual hubs.', color: '#6D28D9', icon_symbol: '⌂', status: 'active', created_at: '2025-12-01T00:00:00Z', innovation_count: 5 },
  { id: 9, slug: 'measurement-scientist', name: 'Measurement Scientist', title: 'Impact Measurement Researcher', domain: 'impact-measurement', description: 'Develops rigorous measurement frameworks — RCTs, quasi-experimental designs, SROI, cost-benefit analysis.', color: '#059669', icon_symbol: 'Δ', status: 'active', created_at: '2025-12-01T00:00:00Z', innovation_count: 5 },
  { id: 10, slug: 'narrative-researcher', name: 'Narrative Researcher', title: 'Story-Based Research Specialist', domain: 'narrative-research', description: 'Elevates lived experience into rigorous research — photovoice, digital storytelling, participatory action research.', color: '#DB2777', icon_symbol: '✎', status: 'active', created_at: '2025-12-01T00:00:00Z', innovation_count: 4 },
  { id: 11, slug: 'market-maker', name: 'Market Maker', title: 'Social Markets Specialist', domain: 'social-markets', description: 'Creates markets for social goods — social enterprise incubation, cooperative models, community land trusts, time banking.', color: '#CA8A04', icon_symbol: '⚖', status: 'active', created_at: '2025-12-01T00:00:00Z', innovation_count: 5 },
];

const DEMO_INNOVATIONS: Innovation[] = [
  // ── Financing ──
  { id: 1, teammate_id: 1, title: 'Braided Benefit Bridge Fund', summary: 'Braids TANF, SNAP E&T, and WIOA funds into a single flexible pool, reducing administrative overhead by 40% while expanding eligibility windows for transitional employment programs.', domain: 'creative-financing', category: 'blended-finance', impact_level: 5, feasibility: 3, novelty: 4, time_horizon: 'medium', status: 'review', details: { mechanism: 'Braided funding pool with unified reporting', funding_sources: ['TANF', 'SNAP E&T', 'WIOA Title I', 'CDBG'], projected_savings: '$2.3M annually per county', legal_basis: 'Section 1115 waiver + WIOA flexibility provisions', implementation_steps: ['Secure MOUs across 4 funding agencies', 'Design unified cost allocation methodology', 'Build integrated reporting dashboard', 'Pilot in 3 counties for 18 months'] }, tags: ['blended-finance', 'TANF', 'workforce', 'cost-reduction'], created_at: '2025-11-15T10:00:00Z', updated_at: '2025-11-15T11:00:00Z' },
  { id: 2, teammate_id: 1, title: 'Pay-for-Success Recidivism Reduction Bond', summary: 'Social impact bond targeting 30% recidivism reduction. Private investors fund upfront; government repays only upon verified outcomes. Shifts financial risk from taxpayers to investors.', domain: 'creative-financing', category: 'social-impact-bonds', impact_level: 5, feasibility: 3, novelty: 3, time_horizon: 'medium', status: 'approved', details: { mechanism: 'Pay-for-success contract with independent validation', target_population: 'Individuals released from state correctional facilities', outcome_metric: '12-month recidivism rate reduction', projected_roi: '287% social return on investment', bond_structure: { total_raise: '$12M', investor_return_cap: '6.5% IRR', measurement_period: '36 months' } }, tags: ['pay-for-success', 'recidivism', 'impact-bonds'], created_at: '2025-11-10T09:00:00Z', updated_at: '2025-11-10T10:00:00Z' },
  { id: 50, teammate_id: 1, title: 'Dome Bonds: Municipal Coordination Savings Bonds', summary: 'New class of municipal bonds backed by documented coordination savings. When DOMES coordination reduces duplicative spending, verified savings back bond issuance — self-funding infrastructure for person-centered government.', domain: 'creative-financing', category: 'dome-financing', impact_level: 5, feasibility: 2, novelty: 5, time_horizon: 'far', status: 'draft', details: { financial_model: { bond_type: 'Revenue bond backed by coordination savings', target_issuance: '$50M initial offering', coupon_rate: '3.5-4.2% tax-exempt', term: '20-year maturity' }, revenue_sources: ['Reduced duplicative assessments ($2.1M/yr per county)', 'Eliminated redundant case management ($1.8M/yr)', 'Prevented crisis interventions ($3.4M/yr)', 'Reduced admin overhead from shared intake ($900K/yr)'], legal_requirements: ['State enabling legislation', 'Independent savings verification', 'Bond counsel opinion on tax-exempt status', 'Credit rating agency engagement (target: A-)'], estimated_cost: '$2M for pilot verification infrastructure', evidence_base: 'Hennepin County coordination savings of $8.2M/yr documented 2019-2023' }, tags: ['dome-bonds', 'municipal-finance', 'coordination-savings'], created_at: '2025-12-01T10:00:00Z', updated_at: '2025-12-01T11:00:00Z' },
  { id: 51, teammate_id: 1, title: 'Person-Centered Budgets: Unified Flexible Spending', summary: 'Replace fragmented categorical spending with a single flexible budget per person. Instead of $4,200 SNAP + $8,400 Medicaid + $6,000 housing as separate allocations, combine into $18,600 the individual helps direct.', domain: 'creative-financing', category: 'dome-financing', impact_level: 5, feasibility: 2, novelty: 5, time_horizon: 'far', status: 'draft', details: { mechanism: 'Pooled categorical funding with person-directed allocation', current_fragmentation: { average_programs_per_person: 4.3, administrative_overhead_rate: '23% of total spending', duplication_rate: '17% of assessments redundant' }, implementation_path: ['Phase 1: Shadow budgets (calculate unified amount)', 'Phase 2: Flex margins (10% movement between categories)', 'Phase 3: Full person-centered budgets for pilot cohort'], estimated_cost: '$1.5M for pilot infrastructure', evidence_base: 'UK Personal Budgets: 40% higher satisfaction, similar costs' }, tags: ['person-centered-budgets', 'flexible-spending'], created_at: '2025-12-02T10:00:00Z', updated_at: '2025-12-02T11:00:00Z' },
  // ── Investment ──
  { id: 3, teammate_id: 2, title: 'Maternal Health Outcomes Bond', summary: 'Development impact bond reducing maternal mortality disparities. Investors fund community health workers and doula services; returns tied to measured reductions in adverse birth outcomes among Black and Indigenous mothers.', domain: 'impact-investment', category: 'development-impact-bonds', impact_level: 5, feasibility: 3, novelty: 4, time_horizon: 'medium', status: 'review', details: { target_outcome: '35% reduction in severe maternal morbidity', investment_size: '$8.5M', equity_focus: 'Black and Indigenous birthing persons in rural areas', measurement: 'Claims data + patient-reported outcomes' }, tags: ['maternal-health', 'equity', 'impact-bond'], created_at: '2025-11-12T09:00:00Z', updated_at: '2025-11-12T10:00:00Z' },
  { id: 52, teammate_id: 2, title: 'Outcomes Marketplace: Coordination Credits Exchange', summary: 'Like carbon credits but for coordination savings. Agencies earning verified savings trade Outcome Credits. Creates market incentives for system integration. 1 Credit = $1,000 in verified coordination savings.', domain: 'impact-investment', category: 'outcomes-markets', impact_level: 5, feasibility: 2, novelty: 5, time_horizon: 'far', status: 'draft', details: { market_design: { unit: '1 Outcome Credit = $1,000 verified savings', verification: 'Independent actuarial audit', trading_platform: 'Government-regulated exchange' }, estimated_cost: '$5M for exchange infrastructure', evidence_base: 'Carbon credit markets: $851B in 2022' }, tags: ['outcomes-marketplace', 'coordination-credits'], created_at: '2025-12-03T10:00:00Z', updated_at: '2025-12-03T11:00:00Z' },
  // ── Data / Privacy ──
  { id: 4, teammate_id: 3, title: 'Cross-System Administrative Data Spine', summary: 'Privacy-preserving data linkage connecting child welfare, Medicaid, SNAP, housing, and education using hashed identifiers — whole-person analytics without sharing raw PII between agencies.', domain: 'data-innovation', category: 'data-linkage', impact_level: 5, feasibility: 3, novelty: 4, time_horizon: 'medium', status: 'review', details: { architecture: 'Federated data spine with tokenized linkage keys', systems_connected: ['CPS/CWS', 'Medicaid/MMIS', 'SNAP/TANF', 'PHA/HCV', 'SIS/education'], privacy_model: 'Differential privacy + k-anonymity thresholds' }, tags: ['data-linkage', 'privacy', 'cross-system'], created_at: '2025-11-08T14:00:00Z', updated_at: '2025-11-08T15:00:00Z' },
  { id: 53, teammate_id: 3, title: 'Person-Held Data Wallets', summary: 'Sovereign data wallet putting individuals in control. Instead of 7 agencies each maintaining separate records, the person holds a verified digital wallet with eligibility data, service history, and outcome records.', domain: 'data-innovation', category: 'data-sovereignty', impact_level: 5, feasibility: 2, novelty: 5, time_horizon: 'far', status: 'draft', details: { architecture: { storage: 'Encrypted local-first', credentials: 'W3C Verifiable Credentials', sharing: 'Selective disclosure' }, data_categories: ['Identity verification', 'Income and employment', 'Benefit enrollment status', 'Service history', 'Consent preferences'], estimated_cost: '$3M for wallet infrastructure', evidence_base: "Estonia's X-Road: 1.3M citizens with sovereign data" }, tags: ['data-wallet', 'sovereignty', 'privacy'], created_at: '2025-12-04T10:00:00Z', updated_at: '2025-12-04T11:00:00Z' },
  // ── Technology ──
  { id: 5, teammate_id: 4, title: 'Blockchain Benefits Portability Ledger', summary: 'Distributed ledger making benefit eligibility portable across state lines. When a SNAP recipient moves states, verified eligibility travels with them — eliminating redundant applications and 60-day coverage gaps.', domain: 'emerging-technology', category: 'blockchain', impact_level: 5, feasibility: 2, novelty: 5, time_horizon: 'far', status: 'draft', details: { technology: 'Permissioned blockchain with state-node architecture', privacy: 'Zero-knowledge proofs for eligibility verification', governance: 'Interstate compact with federated node management' }, tags: ['blockchain', 'portability', 'interstate'], created_at: '2025-11-05T11:00:00Z', updated_at: '2025-11-05T12:00:00Z' },
  { id: 6, teammate_id: 4, title: 'AI-Powered Caseworker Decision Support', summary: 'AI tool surfacing relevant precedents, policy options, and risk factors during caseworker interactions — augmenting judgment with pattern recognition across thousands of similar cases.', domain: 'emerging-technology', category: 'artificial-intelligence', impact_level: 4, feasibility: 3, novelty: 4, time_horizon: 'medium', status: 'review', details: { model_approach: 'Retrieval-augmented generation over case history corpus', safeguards: ['No autonomous decisions', 'Confidence scoring', 'Quarterly bias auditing', 'Caseworker opt-out'] }, tags: ['AI', 'decision-support', 'casework'], created_at: '2025-11-06T09:00:00Z', updated_at: '2025-11-06T10:00:00Z' },
  { id: 54, teammate_id: 4, title: 'AR Caseworker Overlay: Real-Time Dome Visualization', summary: 'Augmented reality showing a person\'s complete Dome profile during home visits. Caseworker sees all active programs, deadlines, benefit cliffs, and coordination opportunities overlaid in real time.', domain: 'emerging-technology', category: 'augmented-reality', impact_level: 4, feasibility: 2, novelty: 5, time_horizon: 'far', status: 'draft', details: { technology_stack: { display: 'Tablet-first (iPad), smart glasses option', data_source: 'Real-time API to cross-system data spine', privacy: 'Requires person consent via Dome Wallet' }, use_cases: ['Home visit: see all agency touchpoints', 'Hospital discharge: housing + benefits status', 'School meeting: family support ecosystem'], dependencies: ['Cross-system data spine', 'Person-held data wallets'], estimated_cost: '$2.5M development + $500K/yr maintenance' }, tags: ['augmented-reality', 'caseworker', 'real-time'], created_at: '2025-12-05T10:00:00Z', updated_at: '2025-12-05T11:00:00Z' },
  // ── Legislation ──
  { id: 7, teammate_id: 5, title: 'THE DOME ACT: Federal Coordination Cost Transparency', summary: 'Federal legislation mandating every agency in means-tested programs publish annual coordination cost reports — documenting fragmentation cost, coordination savings, and the gap. Makes invisible waste visible.', domain: 'model-legislation', category: 'federal-legislation', impact_level: 5, feasibility: 3, novelty: 5, time_horizon: 'medium', status: 'review', details: { full_title: 'Documenting Outcomes and Measuring Efficiency Act (DOME Act)', key_provisions: ['SEC. 101: Annual Coordination Cost Report from HHS, USDA, HUD, DOL, ED', 'SEC. 102: Standardized methodology for measuring duplication', 'SEC. 103: Public dashboard showing coordination costs by state and county', 'SEC. 104: GAO audit of coordination savings potential every 3 years', 'SEC. 105: Innovation grants for states demonstrating 10%+ savings', 'SEC. 201: Person-centered coordination pilot authority for 10 states', 'SEC. 202: Data sharing safe harbor for coordination purposes', 'SEC. 301: Coordination Savings Reinvestment Fund'], strategy_memo: { bipartisan_framing: 'Efficiency (R) + better outcomes for families (D)', coalition: 'NGA, APHSA, NASCIO, CLASP, CBPP, Heritage Foundation', CBO_score: 'Net savings $2.1B over 10 years' }, talking_points: ['$740B in means-tested programs but no one can tell you the cost of NOT coordinating', 'Families in 4+ programs repeat their trauma story 7 times', 'Hennepin County: $8.2M in annual coordination savings', 'This bill makes existing spending transparent, not new programs'], estimated_cost: '$50M implementation over 5 years (offset by savings)' }, tags: ['dome-act', 'federal', 'transparency', 'coordination-costs'], created_at: '2025-12-06T10:00:00Z', updated_at: '2025-12-06T11:00:00Z' },
  { id: 8, teammate_id: 5, title: 'RIGHT TO YOUR DOME: Cross-System Data Access Rights', summary: 'Model state legislation: every person receiving government services can see their complete cross-system profile — every enrollment, assessment, caseworker, and outcome recorded about them.', domain: 'model-legislation', category: 'rights-legislation', impact_level: 5, feasibility: 3, novelty: 5, time_horizon: 'medium', status: 'review', details: { full_title: 'Right to Integrated Government Records Act', key_provisions: ['SEC. 1: Right to complete cross-system profile within 30 days', 'SEC. 2: Must include all enrollments, assessments, assigned workers, outcomes', 'SEC. 3: Right to correct inaccurate information across all systems', 'SEC. 4: Data portability — export in machine-readable format', 'SEC. 5: No adverse actions from cross-system data without notice and appeal', 'SEC. 6: Annual notification of data rights to all enrolled individuals'], talking_points: ['You can see your credit score but not your government profile', 'A mother in 4 programs has 4 case files — never a unified picture', 'Government data rights lag 20 years behind private sector'], estimated_cost: '$800K per state for portal and training' }, tags: ['data-rights', 'transparency', 'person-centered'], created_at: '2025-12-07T10:00:00Z', updated_at: '2025-12-07T11:00:00Z' },
  { id: 9, teammate_id: 5, title: 'Regulatory Sandbox Authorization Act', summary: 'Creates formal regulatory sandbox allowing agencies to test innovative service delivery for 36 months with relaxed requirements, built-in evaluation, and automatic sunset.', domain: 'model-legislation', category: 'regulatory-sandboxes', impact_level: 4, feasibility: 4, novelty: 4, time_horizon: 'near', status: 'approved', details: { sandbox_parameters: { duration: 'Up to 36 months + 12-month extension', scope: 'Up to 5 counties or 50,000 participants', oversight: 'Quarterly reporting to legislative committee' }, sunset_trigger: 'Automatic expiration unless affirmatively renewed' }, tags: ['regulatory-sandbox', 'innovation', 'pilot-authority'], created_at: '2025-11-04T08:00:00Z', updated_at: '2025-11-04T09:00:00Z' },
  // ── Regulatory ──
  { id: 10, teammate_id: 6, title: 'Section 1115 Super-Waiver for Whole-Family Services', summary: 'Comprehensive Medicaid waiver extending coverage to social determinants — housing supports, nutritional counseling, employment services — treating the whole family as the unit of care.', domain: 'regulatory-reform', category: 'waiver-authorities', impact_level: 5, feasibility: 3, novelty: 4, time_horizon: 'medium', status: 'review', details: { waiver_type: 'Section 1115 Research & Demonstration', expanded_services: ['Housing transition and sustaining services', 'Nutrition counseling and food prescription', 'Community health worker home visits', 'Employment readiness assessments'], budget_neutrality: 'Reduced ER utilization and hospital readmissions' }, tags: ['1115-waiver', 'Medicaid', 'social-determinants'], created_at: '2025-11-03T09:00:00Z', updated_at: '2025-11-03T10:00:00Z' },
  { id: 11, teammate_id: 6, title: 'Cross-Agency MOU Template', summary: 'Standardized MOU enabling any two agencies to share eligibility data, conduct joint interviews, and make cross-program referrals — reducing legal negotiation from 18 months to 6 weeks.', domain: 'regulatory-reform', category: 'cross-agency-agreements', impact_level: 3, feasibility: 5, novelty: 2, time_horizon: 'near', status: 'approved', details: { template_sections: ['Purpose and legal authority', 'Data elements to share', 'Security and privacy', 'Roles and responsibilities', 'Dispute resolution', 'Amendment and termination'], implementation_time: '6 weeks from initiation to execution' }, tags: ['MOU', 'data-sharing', 'eligibility'], created_at: '2025-11-02T15:00:00Z', updated_at: '2025-11-02T16:00:00Z' },
  { id: 55, teammate_id: 6, title: 'CMMI Dome Innovation Model', summary: 'CMMI demonstration testing whole-person coordination across Medicaid, housing, nutrition, and employment. Uses existing Section 1115A authority — CMS already has the power to test this. No new legislation needed.', domain: 'regulatory-reform', category: 'federal-authority', impact_level: 5, feasibility: 4, novelty: 4, time_horizon: 'near', status: 'approved', details: { legal_authority: 'Section 1115A of the Social Security Act (ACA Section 3021)', model_design: { population: 'Medicaid beneficiaries in 3+ programs', intervention: 'Dome Navigator + shared care plan + braided funding', duration: '5 years with 3-year extension option' }, existing_precedents: ['Accountable Health Communities', 'Integrated Care for Kids', 'State Innovation Models'], estimated_cost: '$0 in new legislation; $50M CMMI allocation', evidence_base: 'CMMI Accountable Health Communities: 9% utilization reduction' }, tags: ['CMMI', 'medicaid', 'existing-authority', 'immediate'], created_at: '2025-12-08T10:00:00Z', updated_at: '2025-12-08T11:00:00Z' },
  // ── Service Design ──
  { id: 12, teammate_id: 7, title: 'No-Wrong-Door Triage Protocol', summary: 'Any government office can initiate service connections across all programs using a 10-minute structured conversation — identifying needs and generating warm referrals with scheduled appointments.', domain: 'service-design', category: 'no-wrong-door', impact_level: 5, feasibility: 4, novelty: 3, time_horizon: 'near', status: 'approved', details: { triage_tool: '10-minute structured needs assessment', domains_screened: ['Food security', 'Housing stability', 'Health coverage', 'Income/employment', 'Child care', 'Legal needs'], referral_method: 'Warm handoff with scheduled appointment within 48 hours', training_requirement: '8-hour cross-training for all front-line staff' }, tags: ['no-wrong-door', 'triage', 'warm-handoff'], created_at: '2025-11-01T12:00:00Z', updated_at: '2025-11-01T13:00:00Z' },
  { id: 56, teammate_id: 7, title: 'The Dome Navigator: A New Professional Role', summary: 'New profession whose sole job is cross-system coordination for 25-30 people. Not a caseworker in any single system — a coordinator across ALL systems. Licensed, trained in all benefit programs, with authority to convene agencies.', domain: 'service-design', category: 'workforce-innovation', impact_level: 5, feasibility: 3, novelty: 5, time_horizon: 'medium', status: 'review', details: { role_definition: { caseload: '25-30 individuals/families', function: 'Cross-system coordination, not direct service', authority: 'Can convene case conferences across agencies' }, training_requirements: ['120-hour curriculum covering all benefit programs', '40-hour trauma-informed practice certification', '20-hour data systems navigation', 'Supervised practicum'], salary_model: { entry_level: '$48,000-$55,000', experienced: '$62,000-$75,000', senior: '$78,000-$95,000' }, workforce_sizing: { us_need: '~85,000 Dome Navigators nationally', per_county: '27 Navigators per county average' }, estimated_cost: '$650K/yr for 10-Navigator pilot', evidence_base: 'Community health workers show 3:1 ROI; Navigator extends to cross-system' }, tags: ['dome-navigator', 'workforce', 'profession'], created_at: '2025-12-09T10:00:00Z', updated_at: '2025-12-09T11:00:00Z' },
  // ── Physical Space ──
  { id: 13, teammate_id: 8, title: 'Neighborhood Dome Center (2,000 sq ft Storefront)', summary: 'Smallest viable coordination space — a welcoming community living room, not a government office. Two private rooms, open area, children\'s corner, tech station. Anti-pattern library: NO fluorescent lights, NO plastic chairs, NO bulletproof glass.', domain: 'space-design', category: 'dome-center-design', impact_level: 4, feasibility: 4, novelty: 4, time_horizon: 'near', status: 'approved', details: { floor_plan: { total_sqft: 2000, private_rooms: '2 consultation rooms (100 sqft each)', open_area: '800 sqft with flexible furniture', tech_station: '4 workstations + scanner', children_corner: '200 sqft supervised play', kitchenette: 'Coffee, water, healthy snacks' }, material_palette: { flooring: 'Warm wood-look LVT', walls: 'Soft white + terracotta accent', furniture: 'Residential-quality upholstered (not plastic)', lighting: 'Warm LED 2700-3000K, NO fluorescent' }, anti_patterns: ['NO fluorescent lighting', 'NO plastic chairs', 'NO bulletproof glass', 'NO numbered ticket queuing', 'NO mounted TVs playing news', 'NO visible security cameras in consultation areas'], cost_estimate: { buildout: '$180,000-$240,000', furniture: '$45,000-$65,000', technology: '$25,000-$35,000', annual_operating: '$180,000-$220,000 including 3 staff' } }, tags: ['dome-center', 'neighborhood', 'storefront', 'anti-pattern'], created_at: '2025-10-20T10:00:00Z', updated_at: '2025-10-20T11:00:00Z' },
  { id: 57, teammate_id: 8, title: 'Regional Dome Hub (50,000 sq ft Campus)', summary: 'Flagship campus: Navigator training academy, data operations center, community halls, health clinic, legal aid, demonstration spaces. Biophilic design, universal accessibility, trauma-informed architecture.', domain: 'space-design', category: 'dome-center-design', impact_level: 5, feasibility: 2, novelty: 5, time_horizon: 'far', status: 'draft', details: { floor_plan: { total_sqft: 50000, coordination_wing: '10,000 sqft — 20 rooms + Navigator floor', training_academy: '8,000 sqft — classrooms + simulation lab', community_wing: '12,000 sqft — 500-seat assembly + gallery', health_clinic: '5,000 sqft — FQHC partner', legal_aid: '3,000 sqft — civil legal + record expungement', data_center: '4,000 sqft — secure ops + visualization wall' }, cost_estimate: { new_construction: '$18M-$24M', adaptive_reuse: '$12M-$16M', annual_operating: '$4.5M-$6M including 50+ staff' }, dependencies: ['Dome Navigator workforce pipeline', 'Dome Bonds financing'], evidence_base: 'UK Integrated Care Hubs: 22% better outcomes from similar scale' }, tags: ['dome-hub', 'regional', 'campus', 'flagship'], created_at: '2025-12-10T10:00:00Z', updated_at: '2025-12-10T11:00:00Z' },
  { id: 14, teammate_id: 8, title: 'Mobile Service Unit Fleet Design', summary: 'Fleet of 30-foot converted vehicles with private interview rooms, computer stations, and telepresence — bringing full-service government to underserved communities on rotating schedules.', domain: 'space-design', category: 'mobile-service-units', impact_level: 4, feasibility: 4, novelty: 3, time_horizon: 'near', status: 'approved', details: { vehicle_specs: { type: '30-foot converted transit vehicle', stations: 3, private_rooms: 1, accessibility: 'ADA-compliant ramp' }, technology: ['Satellite internet', 'Telepresence screen', 'Document scanner/printer'], deployment: 'Rotating schedule covering 12 underserved zones/month' }, tags: ['mobile-units', 'access', 'outreach'], created_at: '2025-10-25T10:00:00Z', updated_at: '2025-10-25T11:00:00Z' },
  // ── Measurement ──
  { id: 15, teammate_id: 9, title: 'Rapid-Cycle RCT Framework', summary: 'Streamlined RCT producing actionable results in 6-12 months instead of 3-5 years — using administrative data, adaptive designs, and Bayesian stopping rules. Cost: $150K-$400K vs $2M+ traditional.', domain: 'impact-measurement', category: 'randomized-controlled-trials', impact_level: 5, feasibility: 3, novelty: 4, time_horizon: 'medium', status: 'review', details: { design_features: ['Administrative data outcomes', 'Adaptive randomization', 'Bayesian stopping rules', 'Pre-registered on OSF'], timeline: '6-12 months', cost_estimate: '$150K-$400K vs. $2M+ for traditional RCT' }, tags: ['RCT', 'rapid-cycle', 'evidence'], created_at: '2025-11-20T09:00:00Z', updated_at: '2025-11-20T10:00:00Z' },
  { id: 58, teammate_id: 9, title: 'Dome Index: 0-100 Coordination Quality Score', summary: 'Single composite score measuring coordination quality for any jurisdiction. Six sub-indices: data sharing, service integration, financing alignment, workforce capacity, client experience, outcome equity. Like a credit score for government coordination.', domain: 'impact-measurement', category: 'measurement-frameworks', impact_level: 5, feasibility: 3, novelty: 5, time_horizon: 'medium', status: 'review', details: { scoring_methodology: { total_range: '0-100', sub_indices: { data_sharing: '0-20 points', service_integration: '0-20 points', financing_alignment: '0-15 points', workforce_capacity: '0-15 points', client_experience: '0-15 points', outcome_equity: '0-15 points' } }, benchmarks: { '0-25': 'Siloed — agencies operate independently', '26-50': 'Connecting — some data sharing in place', '51-75': 'Coordinating — shared intake, braided funding', '76-100': 'Integrated — person-centered budgets, full interop' }, estimated_cost: '$400K development; $150K/yr for 50 jurisdictions', evidence_base: 'Pilot-tested in 5 counties, Cronbach alpha = 0.87' }, tags: ['dome-index', 'coordination-score', 'benchmarking'], created_at: '2025-12-11T10:00:00Z', updated_at: '2025-12-11T11:00:00Z' },
  { id: 16, teammate_id: 9, title: 'Social Return on Investment Calculator', summary: 'Open-source calculator enabling any program to estimate SROI using standardized value maps and conservative estimates. 15 pre-built program type templates. Democratizes impact measurement.', domain: 'impact-measurement', category: 'social-return-on-investment', impact_level: 4, feasibility: 4, novelty: 3, time_horizon: 'near', status: 'approved', details: { methodology: 'SROI Network International Standard (2012 update)', value_maps: 'Pre-built for 15 common program types', outputs: ['SROI ratio (dollars per dollar invested)', 'Sensitivity analysis', 'Stakeholder value breakdown', 'Narrative impact report generator'] }, tags: ['SROI', 'calculator', 'open-source'], created_at: '2025-11-18T09:00:00Z', updated_at: '2025-11-18T10:00:00Z' },
  // ── Narrative ──
  { id: 17, teammate_id: 10, title: 'Photovoice Project: Navigating the Safety Net', summary: '30 families document daily experiences navigating government systems through photography — producing exhibition and policy report centering client voice. SHOWeD analysis framework.', domain: 'narrative-research', category: 'photovoice', impact_level: 4, feasibility: 4, novelty: 3, time_horizon: 'near', status: 'review', details: { participants: 30, duration: '12 weeks photo documentation + 4 weeks analysis', outputs: ['Public exhibition at county government center', 'Policy brief with 10 recommendations', 'Digital story collection', 'Peer-reviewed publication'] }, tags: ['photovoice', 'participatory', 'client-voice'], created_at: '2025-11-22T14:00:00Z', updated_at: '2025-11-22T15:00:00Z' },
  { id: 59, teammate_id: 10, title: 'DOMES Documentary Series: The Invisible Architecture', summary: "3-part series: 'The Maze' (families navigating fragmentation), 'The Workers' (caseworker moral injury), 'The Builders' (communities constructing DOMES). Target: Sundance → PBS → Congressional screening.", domain: 'narrative-research', category: 'documentary', impact_level: 4, feasibility: 3, novelty: 4, time_horizon: 'medium', status: 'draft', details: { series_structure: { part_1_the_maze: { duration: '55 min', subjects: '3 families in 4+ programs' }, part_2_the_workers: { duration: '55 min', subjects: '12 caseworkers across systems' }, part_3_the_builders: { duration: '55 min', subjects: '3 communities building DOMES' } }, distribution: ['Sundance social impact track', 'PBS national broadcast', 'Congressional screening', 'University curriculum integration'], estimated_cost: '$1.8M total production budget', evidence_base: "'13th' influenced criminal justice reform; 'Waiting for Superman' drove education policy" }, tags: ['documentary', 'storytelling', 'advocacy'], created_at: '2025-12-12T10:00:00Z', updated_at: '2025-12-12T11:00:00Z' },
  // ── Market ──
  { id: 18, teammate_id: 11, title: 'Social Enterprise Incubator for Reentry', summary: '12-month incubator helping formerly incarcerated individuals launch social enterprises. Business training, $5K-$15K seed capital, mentorship, legal support for record barriers. 15 entrepreneurs per cohort.', domain: 'social-markets', category: 'social-enterprise', impact_level: 5, feasibility: 3, novelty: 4, time_horizon: 'medium', status: 'review', details: { program_structure: { phase_1: '8-week business fundamentals', phase_2: '16-week venture development + mentoring', phase_3: '6-month post-launch support' }, seed_capital: '$5,000-$15,000 per venture (grant)', legal_support: 'Record expungement clinic + licensing assistance' }, tags: ['social-enterprise', 'reentry', 'entrepreneurship'], created_at: '2025-11-25T11:00:00Z', updated_at: '2025-11-25T12:00:00Z' },
  { id: 19, teammate_id: 11, title: 'Time Banking Network for Mutual Aid', summary: 'Digital platform for hour-for-hour service exchange — childcare for tax prep, transportation for home repairs. 8 service categories, 500-member target, community steering committee governance.', domain: 'social-markets', category: 'time-banking', impact_level: 3, feasibility: 4, novelty: 3, time_horizon: 'near', status: 'approved', details: { service_categories: ['Transportation', 'Childcare', 'Home repair', 'Tax preparation', 'Translation', 'Technology help', 'Cooking/meal prep', 'Companionship'], scale_target: '500 active members within 18 months' }, tags: ['time-banking', 'mutual-aid', 'community'], created_at: '2025-11-23T09:00:00Z', updated_at: '2025-11-23T10:00:00Z' },
  { id: 60, teammate_id: 11, title: 'Dome Certification: Agency Coordination Quality Standard', summary: 'Like LEED for buildings but for government coordination. Bronze/Silver/Gold/Platinum certification based on coordination practices, data sharing, client experience, and outcomes. Market incentive for integration.', domain: 'social-markets', category: 'certification', impact_level: 4, feasibility: 4, novelty: 4, time_horizon: 'near', status: 'review', details: { certification_levels: { bronze: 'Basic data sharing + referral protocols with 2+ agencies', silver: 'Shared intake + braided funding + coordination staff', gold: 'Integrated case management + shared outcomes + co-design', platinum: 'Person-centered budgets + full interop + Dome Index 75+' }, market_incentives: ['Preferred status in federal grants', 'Insurance premium reductions', 'Public Dome Certified branding', 'Access to Dome Network exchanges'], estimated_cost: '$2M program development; $500K/yr operations', evidence_base: 'LEED drove $83B in green construction via verified quality markets' }, tags: ['certification', 'quality-standard', 'coordination'], created_at: '2025-12-13T10:00:00Z', updated_at: '2025-12-13T11:00:00Z' },
];

// ─── API Functions ──────────────────────────────────────────────────────────

export async function getTeammates(): Promise<Teammate[]> {
  try {
    const all = await fetchJSON<Teammate[]>(`${API_BASE}/teammates`);
    // Exclude the architect (system-integration) — it's the dashboard, not a domain
    return all.filter(t => t.slug !== 'architect');
  } catch {
    return DEMO_TEAMMATES;
  }
}

export async function getTeammate(slug: string): Promise<(Teammate & { innovations: Innovation[] }) | null> {
  try {
    const data = await fetchJSON<Teammate & { innovations: Innovation[] }>(`${API_BASE}/teammates/${slug}`);
    return data;
  } catch {
    const t = DEMO_TEAMMATES.find(t => t.slug === slug);
    if (!t) return null;
    const innovations = DEMO_INNOVATIONS.filter(i => i.domain === t.domain);
    return { ...t, innovations };
  }
}

export async function getAllInnovations(): Promise<Innovation[]> {
  try {
    const all = await fetchJSON<Innovation[]>(`${API_BASE}/innovations`);
    // Exclude architect/system-integration innovations
    return all.filter(i => i.domain !== 'system-integration');
  } catch {
    return DEMO_INNOVATIONS;
  }
}

export async function getInnovationsByDomain(backendDomain: string): Promise<Innovation[]> {
  try {
    return await fetchJSON<Innovation[]>(`${API_BASE}/innovations?domain=${backendDomain}`);
  } catch {
    return DEMO_INNOVATIONS.filter(i => i.domain === backendDomain);
  }
}

export function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    draft: '#6B7280', review: '#D97706', approved: '#059669', archived: '#4B5563',
  };
  return colors[status] || '#6B7280';
}
