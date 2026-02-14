// ─────────────────────────────────────────────────────────────
// SPHERES Innovation Laboratory — API Client & Data Layer
// ─────────────────────────────────────────────────────────────

// ── TypeScript Interfaces ────────────────────────────────────

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
  time_horizon: string;
  status: string;
  details: Record<string, unknown>;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface Collaboration {
  id: number;
  title: string;
  description: string;
  domains: string[];
  teammate_ids: number[];
  status: string;
  created_at: string;
}

export interface LabSession {
  id: number;
  session_type: string;
  status: string;
  started_at: string;
  ended_at: string | null;
  results: Record<string, unknown>;
}

export interface StatsResponse {
  totals: Record<string, number>;
  averages: Record<string, number>;
  domain_breakdown: Record<string, number>;
  status_breakdown: Record<string, number>;
  horizon_breakdown: Record<string, number>;
  recent_innovations: Innovation[];
}

export interface DomainConfig {
  slug: string;
  label: string;
  description: string;
  icon: string;
  color: string;
  backendDomain: string;
}

// ── Domain Configuration (11 domains, excluding "architect") ─

export const DOMAINS: DomainConfig[] = [
  {
    slug: 'sphere-economist',
    label: 'Business Models',
    description: 'Sphere Exchange, subscriptions, cooperatives, reverse-payment models',
    icon: '$',
    color: '#C9A726',
    backendDomain: 'space-economics',
  },
  {
    slug: 'revenue-architect',
    label: 'City Revenue',
    description: 'Green bonds, impact funds, tax incentives, public-private partnerships',
    icon: '▲',
    color: '#2E8B57',
    backendDomain: 'revenue-architecture',
  },
  {
    slug: 'space-inventor',
    label: 'New Space Types',
    description: 'Water Spheres, Temporal Spheres, Weather Spheres, Invisible Spheres',
    icon: '◆',
    color: '#4169E1',
    backendDomain: 'spatial-invention',
  },
  {
    slug: 'culture-engineer',
    label: 'Culture',
    description: 'Public art, performance series, maker spaces, heritage celebrations',
    icon: '✦',
    color: '#DB2777',
    backendDomain: 'cultural-engineering',
  },
  {
    slug: 'platform-inventor',
    label: 'Platform/Tech',
    description: 'IoT networks, community apps, digital twins, sensor dashboards',
    icon: '★',
    color: '#9333EA',
    backendDomain: 'platform-invention',
  },
  {
    slug: 'world-builder',
    label: 'Spatial Computing',
    description: 'AR overlays, VR workshops, projection mapping, 3D parcel exploration',
    icon: '⌂',
    color: '#0891B2',
    backendDomain: 'immersive-worlds',
  },
  {
    slug: 'policy-inventor',
    label: 'Policy',
    description: 'Zoning reforms, fast-track permits, anti-displacement, Right to Activate',
    icon: '§',
    color: '#DC2626',
    backendDomain: 'policy-invention',
  },
  {
    slug: 'city-replicator',
    label: 'City Scaling',
    description: 'City readiness scores, replication playbooks, Rust Belt alliance',
    icon: '⚒',
    color: '#EA580C',
    backendDomain: 'city-replication',
  },
  {
    slug: 'ecosystem-architect',
    label: 'Ecosystem',
    description: 'Governance councils, resource networks, university alliances',
    icon: '❀',
    color: '#6D28D9',
    backendDomain: 'ecosystem-architecture',
  },
  {
    slug: 'impact-scientist',
    label: 'Impact',
    description: 'SROI calculators, health outcomes, property uplift, violence reduction',
    icon: 'Δ',
    color: '#059669',
    backendDomain: 'impact-science',
  },
  {
    slug: 'narrative-designer',
    label: 'Narrative',
    description: 'Documentary series, oral histories, data stories, social campaigns',
    icon: '✎',
    color: '#CA8A04',
    backendDomain: 'narrative-design',
  },
];

// ── Connection Graph (18 edges between domains) ──────────────

export interface Connection {
  from: string;
  to: string;
  strength: number;
  reason: string;
}

export const CONNECTIONS: Connection[] = [
  { from: 'sphere-economist', to: 'revenue-architect', strength: 9, reason: 'Revenue models directly feed financial architecture and pricing frameworks' },
  { from: 'sphere-economist', to: 'impact-scientist', strength: 7, reason: 'Economic viability depends on measurable impact outcomes for funding' },
  { from: 'revenue-architect', to: 'platform-inventor', strength: 8, reason: 'Digital platforms enable scalable revenue collection and subscription models' },
  { from: 'revenue-architect', to: 'city-replicator', strength: 7, reason: 'Financial models must adapt to each city deployment context' },
  { from: 'space-inventor', to: 'world-builder', strength: 10, reason: 'Physical spaces are the canvas for immersive world experiences' },
  { from: 'space-inventor', to: 'culture-engineer', strength: 8, reason: 'Space design shapes and enables cultural programming and rituals' },
  { from: 'culture-engineer', to: 'narrative-designer', strength: 9, reason: 'Cultural programs generate the stories and brand narratives' },
  { from: 'culture-engineer', to: 'ecosystem-architect', strength: 6, reason: 'Community rituals require partner networks for programming' },
  { from: 'platform-inventor', to: 'ecosystem-architect', strength: 8, reason: 'Digital platforms connect and orchestrate the partner ecosystem' },
  { from: 'platform-inventor', to: 'impact-scientist', strength: 7, reason: 'Platforms collect the data needed for impact measurement' },
  { from: 'world-builder', to: 'narrative-designer', strength: 8, reason: 'Immersive worlds need compelling narratives to drive engagement' },
  { from: 'world-builder', to: 'city-replicator', strength: 6, reason: 'World themes must be adapted for different city contexts' },
  { from: 'policy-inventor', to: 'impact-scientist', strength: 9, reason: 'Policy frameworks require evidence-based impact data for approval' },
  { from: 'policy-inventor', to: 'city-replicator', strength: 8, reason: 'Each city deployment requires local policy compliance and adaptation' },
  { from: 'city-replicator', to: 'ecosystem-architect', strength: 7, reason: 'City rollout depends on local partner networks and supply chains' },
  { from: 'ecosystem-architect', to: 'narrative-designer', strength: 5, reason: 'Partner stories enrich the overall brand narrative' },
  { from: 'impact-scientist', to: 'narrative-designer', strength: 7, reason: 'Impact data provides compelling evidence for storytelling' },
  { from: 'sphere-economist', to: 'policy-inventor', strength: 6, reason: 'Economic models must align with regulatory and policy constraints' },
];

// ── Readiness Mapping ────────────────────────────────────────

export type ReadinessLevel = 'immediate' | '1-year' | '5-year' | 'moonshot';

export interface ReadinessConfig {
  key: ReadinessLevel;
  label: string;
  color: string;
  description: string;
}

export const READINESS_LEVELS: ReadinessConfig[] = [
  { key: 'immediate', label: 'Immediate', color: '#00CC66', description: 'Ready to deploy now' },
  { key: '1-year', label: '1-Year', color: '#FFCC00', description: 'Achievable within 12 months' },
  { key: '5-year', label: '5-Year', color: '#0066FF', description: 'Strategic 5-year horizon' },
  { key: 'moonshot', label: 'Moonshot', color: '#9333EA', description: 'Visionary long-term bets' },
];

export function getReadiness(innovation: Innovation): ReadinessLevel {
  const { time_horizon, feasibility } = innovation;
  if (time_horizon === 'near') return 'immediate';
  if (time_horizon === 'medium') return '1-year';
  if (time_horizon === 'far' && feasibility <= 4) return 'moonshot';
  if (time_horizon === 'far') return '5-year';
  // fallback
  return '1-year';
}

export function getReadinessConfig(level: ReadinessLevel): ReadinessConfig {
  return READINESS_LEVELS.find((r) => r.key === level) ?? READINESS_LEVELS[1];
}

// ── Status Colors ────────────────────────────────────────────

export const STATUS_COLORS: Record<string, string> = {
  draft: '#6B7280',
  review: '#D97706',
  approved: '#059669',
  archived: '#4B5563',
};

export function getStatusColor(status: string): string {
  return STATUS_COLORS[status] ?? '#6B7280';
}

// ── Domain Helpers ───────────────────────────────────────────

export function getDomainConfig(slugOrDomain: string): DomainConfig | undefined {
  return DOMAINS.find(
    (d) => d.slug === slugOrDomain || d.backendDomain === slugOrDomain
  );
}

// ── Brief Generator ──────────────────────────────────────────

export type Audience = 'Mayor' | 'Developer' | 'Investor' | 'Community Group';

export function generateBrief(
  domain: DomainConfig,
  readiness: ReadinessLevel,
  audience: Audience,
  innovations: Innovation[]
): string {
  const now = new Date();
  const dateStr = now.toISOString().split('T')[0];
  const readinessLabel =
    READINESS_LEVELS.find((r) => r.key === readiness)?.label ?? readiness;

  const filtered = innovations.filter(
    (inn) =>
      inn.domain === domain.backendDomain && getReadiness(inn) === readiness
  );

  const divider = '═'.repeat(64);
  const thinDivider = '─'.repeat(64);

  let brief = '';
  brief += `${divider}\n`;
  brief += `  SPHERES INNOVATION LABORATORY — POLICY BRIEF\n`;
  brief += `${divider}\n\n`;
  brief += `  DATE:       ${dateStr}\n`;
  brief += `  DOMAIN:     ${domain.label} (${domain.icon})\n`;
  brief += `  READINESS:  ${readinessLabel}\n`;
  brief += `  AUDIENCE:   ${audience}\n`;
  brief += `  ITEMS:      ${filtered.length} innovation(s)\n\n`;
  brief += `${thinDivider}\n`;
  brief += `  EXECUTIVE SUMMARY\n`;
  brief += `${thinDivider}\n\n`;

  if (filtered.length === 0) {
    brief += `  No innovations currently match the selected criteria.\n`;
    brief += `  Consider broadening the readiness filter or selecting\n`;
    brief += `  a different domain to generate a comprehensive brief.\n\n`;
  } else {
    brief += `  The ${domain.label} domain has ${filtered.length} innovation(s)\n`;
    brief += `  at the ${readinessLabel} readiness level. These innovations\n`;
    brief += `  represent strategic opportunities for ${audience} consideration.\n\n`;

    const avgImpact =
      filtered.reduce((s, i) => s + i.impact_level, 0) / filtered.length;
    const avgFeasibility =
      filtered.reduce((s, i) => s + i.feasibility, 0) / filtered.length;
    const avgNovelty =
      filtered.reduce((s, i) => s + i.novelty, 0) / filtered.length;

    brief += `  AGGREGATE SCORES:\n`;
    brief += `    Impact:      ${avgImpact.toFixed(1)} / 10  ${'█'.repeat(Math.round(avgImpact))}${'░'.repeat(10 - Math.round(avgImpact))}\n`;
    brief += `    Feasibility: ${avgFeasibility.toFixed(1)} / 10  ${'█'.repeat(Math.round(avgFeasibility))}${'░'.repeat(10 - Math.round(avgFeasibility))}\n`;
    brief += `    Novelty:     ${avgNovelty.toFixed(1)} / 10  ${'█'.repeat(Math.round(avgNovelty))}${'░'.repeat(10 - Math.round(avgNovelty))}\n\n`;
  }

  brief += `${thinDivider}\n`;
  brief += `  INNOVATIONS\n`;
  brief += `${thinDivider}\n\n`;

  filtered.forEach((inn, idx) => {
    brief += `  [${idx + 1}] ${inn.title.toUpperCase()}\n`;
    brief += `      Status: ${inn.status}  |  Category: ${inn.category}\n`;
    brief += `      Impact: ${inn.impact_level}/10  Feasibility: ${inn.feasibility}/10  Novelty: ${inn.novelty}/10\n\n`;
    brief += `      ${inn.summary}\n\n`;
    if (inn.tags.length > 0) {
      brief += `      Tags: ${inn.tags.join(', ')}\n\n`;
    }
  });

  brief += `${thinDivider}\n`;
  brief += `  RECOMMENDATIONS FOR ${audience.toUpperCase()}\n`;
  brief += `${thinDivider}\n\n`;

  switch (audience) {
    case 'Mayor':
      brief += `  1. Prioritize innovations with immediate readiness for quick wins\n`;
      brief += `  2. Frame public space activation as economic development and safety\n`;
      brief += `  3. Identify 5 pilot parcels in high-visibility council districts\n`;
      break;
    case 'Developer':
      brief += `  1. Model revenue projections for space activation at portfolio scale\n`;
      brief += `  2. Structure public-private partnerships with city land bank\n`;
      brief += `  3. Design mixed-use integration with surrounding development\n`;
      break;
    case 'Investor':
      brief += `  1. Focus on innovations with feasibility >= 4 for near-term ROI\n`;
      brief += `  2. Build portfolio across readiness levels for risk diversification\n`;
      brief += `  3. Quantify social return using SROI methodology from Impact domain\n`;
      break;
    case 'Community Group':
      brief += `  1. Engage neighbors through design charrettes and block meetings\n`;
      brief += `  2. Secure community land trust or stewardship agreement for long-term control\n`;
      brief += `  3. Apply for Land Bank community transfer for target parcels\n`;
      break;
  }

  brief += `\n${divider}\n`;
  brief += `  Generated by SPHERES Innovation Laboratory\n`;
  brief += `  ${now.toISOString()}\n`;
  brief += `${divider}\n`;

  return brief;
}

// ── Hardcoded Demo Data (fallback) ───────────────────────────

export const DEMO_TEAMMATES: Teammate[] = [
  {
    id: 1,
    slug: 'sphere-economist',
    name: 'Sphere Economist',
    title: 'Economic Strategist',
    domain: 'space-economics',
    description: 'Business models for sustainable public space activation — Sphere Exchange, subscriptions, cooperatives.',
    color: '#C9A726',
    icon_symbol: '$',
    status: 'idle',
    created_at: '2025-01-15T00:00:00Z',
    innovation_count: 4,
  },
  {
    id: 2,
    slug: 'space-inventor',
    name: 'Space Inventor',
    title: 'Spatial Innovation Designer',
    domain: 'spatial-invention',
    description: 'Novel spatial typologies — Water Spheres, Temporal Spheres, Weather Spheres, Invisible Spheres.',
    color: '#4169E1',
    icon_symbol: '◆',
    status: 'idle',
    created_at: '2025-01-15T00:00:00Z',
    innovation_count: 4,
  },
  {
    id: 3,
    slug: 'city-replicator',
    name: 'City Replicator',
    title: 'Scaling Strategist',
    domain: 'city-replication',
    description: 'City readiness scorecards, replication playbooks, Rust Belt alliance.',
    color: '#EA580C',
    icon_symbol: '⚒',
    status: 'idle',
    created_at: '2025-01-15T00:00:00Z',
    innovation_count: 4,
  },
  {
    id: 4,
    slug: 'impact-scientist',
    name: 'Impact Scientist',
    title: 'Measurement & Evaluation Lead',
    domain: 'impact-science',
    description: 'SROI calculators, health outcomes, property value uplift, violence reduction mapping.',
    color: '#059669',
    icon_symbol: 'Δ',
    status: 'idle',
    created_at: '2025-01-15T00:00:00Z',
    innovation_count: 3,
  },
];

export const DEMO_INNOVATIONS: Innovation[] = [
  {
    id: 1,
    teammate_id: 1,
    title: 'Sphere Exchange',
    summary: 'Real-time marketplace for activated public spaces with dynamic pricing, revenue projections, and pilot design for 50 parcels across Philadelphia.',
    domain: 'space-economics',
    category: 'marketplace',
    impact_level: 5,
    feasibility: 4,
    novelty: 5,
    time_horizon: 'near',
    status: 'approved',
    details: { revenue_model: 'dynamic marketplace', pilot_parcels: 50 },
    tags: ['marketplace', 'dynamic-pricing', 'pilot'],
    created_at: '2025-02-01T00:00:00Z',
    updated_at: '2025-02-10T00:00:00Z',
  },
  {
    id: 2,
    teammate_id: 1,
    title: 'Subscription Spheres',
    summary: '$29/mo gets access to any activated space citywide — ClassPass for public space with projected 10K subscriber base.',
    domain: 'space-economics',
    category: 'subscription',
    impact_level: 4,
    feasibility: 4,
    novelty: 4,
    time_horizon: 'medium',
    status: 'approved',
    details: { monthly_price: '$29', projected_subscribers: 10000 },
    tags: ['subscription', 'access', 'citywide'],
    created_at: '2025-02-05T00:00:00Z',
    updated_at: '2025-02-12T00:00:00Z',
  },
  {
    id: 3,
    teammate_id: 2,
    title: 'Water Spheres',
    summary: 'Floating platform concepts for the Delaware and Schuylkill rivers — modular decks with gardens, performance space, and community gathering areas on the water.',
    domain: 'spatial-invention',
    category: 'floating-platform',
    impact_level: 5,
    feasibility: 2,
    novelty: 5,
    time_horizon: 'far',
    status: 'review',
    details: { rivers: ['Delaware', 'Schuylkill'], platform_sqft: 2400 },
    tags: ['floating', 'river', 'modular', 'waterfront'],
    created_at: '2025-01-20T00:00:00Z',
    updated_at: '2025-02-08T00:00:00Z',
  },
  {
    id: 4,
    teammate_id: 2,
    title: 'Temporal Spheres',
    summary: 'Time-locked activations — dawn-only sound baths, midnight-only film screenings, solstice-only fire installations that create urgency and ritual.',
    domain: 'spatial-invention',
    category: 'temporal-activation',
    impact_level: 4,
    feasibility: 4,
    novelty: 5,
    time_horizon: 'near',
    status: 'approved',
    details: { activation_windows: ['dawn', 'midnight', 'solstice', 'equinox'] },
    tags: ['temporal', 'ritual', 'urgency', 'time-locked'],
    created_at: '2025-02-03T00:00:00Z',
    updated_at: '2025-02-11T00:00:00Z',
  },
  {
    id: 5,
    teammate_id: 3,
    title: 'Philadelphia Readiness Scorecard',
    summary: 'Philadelphia scores 82/100: massive parcel inventory, moderate permits, strong cultural assets. Detailed breakdown across 5 dimensions.',
    domain: 'city-replication',
    category: 'readiness-scorecard',
    impact_level: 4,
    feasibility: 5,
    novelty: 3,
    time_horizon: 'near',
    status: 'approved',
    details: { overall_score: 82, city: 'Philadelphia' },
    tags: ['readiness', 'scorecard', 'philadelphia', 'assessment'],
    created_at: '2025-01-25T00:00:00Z',
    updated_at: '2025-02-09T00:00:00Z',
  },
  {
    id: 6,
    teammate_id: 3,
    title: 'Detroit Readiness Scorecard',
    summary: 'Detroit scores 91/100: enormous inventory (150K+ lots), friendly policy, desperate need. Highest readiness of any US city.',
    domain: 'city-replication',
    category: 'readiness-scorecard',
    impact_level: 5,
    feasibility: 4,
    novelty: 3,
    time_horizon: 'near',
    status: 'approved',
    details: { overall_score: 91, city: 'Detroit' },
    tags: ['readiness', 'scorecard', 'detroit', 'rust-belt'],
    created_at: '2025-02-07T00:00:00Z',
    updated_at: '2025-02-13T00:00:00Z',
  },
  {
    id: 7,
    teammate_id: 4,
    title: 'Violence Reduction Mapper',
    summary: 'Correlating lot greening with gun violence reduction by census tract, building on Penn studies showing 29% reduction near activated spaces.',
    domain: 'impact-science',
    category: 'safety-analysis',
    impact_level: 5,
    feasibility: 4,
    novelty: 3,
    time_horizon: 'near',
    status: 'approved',
    details: { methodology: 'difference-in-differences', baseline_reduction: '29%' },
    tags: ['violence-reduction', 'safety', 'greening', 'evidence'],
    created_at: '2025-01-28T00:00:00Z',
    updated_at: '2025-02-10T00:00:00Z',
  },
  {
    id: 8,
    teammate_id: 4,
    title: 'Property Value Uplift Tracker',
    summary: 'Real-time monitoring of home values within 500ft of activated spaces, using hedonic pricing models calibrated to Philadelphia OPA data.',
    domain: 'impact-science',
    category: 'property-analysis',
    impact_level: 4,
    feasibility: 4,
    novelty: 3,
    time_horizon: 'near',
    status: 'approved',
    details: { radius_ft: 500, data_source: 'Philadelphia OPA' },
    tags: ['property-value', 'uplift', 'hedonic-pricing', 'real-time'],
    created_at: '2025-02-06T00:00:00Z',
    updated_at: '2025-02-12T00:00:00Z',
  },
];

// ── API Fetch Functions ──────────────────────────────────────

const API_BASE = '/api';

async function apiFetch<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  const json = await res.json();
  return json.data as T;
}

export async function getTeammates(): Promise<Teammate[]> {
  try {
    return await apiFetch<Teammate[]>('/teammates');
  } catch {
    return DEMO_TEAMMATES;
  }
}

export async function getTeammate(slug: string): Promise<Teammate | null> {
  try {
    return await apiFetch<Teammate>(`/teammates/${slug}`);
  } catch {
    const demo = DEMO_TEAMMATES.find((t) => t.slug === slug);
    if (demo) {
      return {
        ...demo,
        innovations: DEMO_INNOVATIONS.filter(
          (i) => i.domain === demo.domain
        ),
      };
    }
    return null;
  }
}

export async function getAllInnovations(): Promise<Innovation[]> {
  try {
    return await apiFetch<Innovation[]>('/innovations');
  } catch {
    return DEMO_INNOVATIONS;
  }
}

export async function getInnovationsByDomain(
  domain: string
): Promise<Innovation[]> {
  try {
    return await apiFetch<Innovation[]>(`/innovations?domain=${domain}`);
  } catch {
    return DEMO_INNOVATIONS.filter((i) => i.domain === domain);
  }
}

export async function getStats(): Promise<StatsResponse | null> {
  try {
    return await apiFetch<StatsResponse>('/stats');
  } catch {
    return null;
  }
}

export async function generateInnovation(
  slug: string
): Promise<Innovation | null> {
  try {
    const res = await fetch(`${API_BASE}/generate/${slug}`, { method: 'POST' });
    if (!res.ok) throw new Error(`Generate error: ${res.status}`);
    const json = await res.json();
    return json.data as Innovation;
  } catch {
    return null;
  }
}
