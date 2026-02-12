// DOMES Innovation Laboratory -- API Client
// Wraps all backend calls with envelope unwrapping and demo fallbacks

// ─── Types ───────────────────────────────────────────────────────────────────

export interface Teammate {
  id: number;
  slug: string;
  name: string;
  title: string;
  domain: string;
  description: string;
  color: string;
  innovation_count: number;
  avg_impact: number;
  avg_feasibility: number;
  avg_novelty: number;
  status: 'active' | 'standby' | 'offline';
}

export interface Innovation {
  id: number;
  title: string;
  summary: string;
  detail: string;
  domain: string;
  teammate_slug: string;
  teammate_name: string;
  impact_score: number;
  feasibility_score: number;
  novelty_score: number;
  time_horizon: 'near' | 'medium' | 'far';
  status: 'draft' | 'review' | 'approved' | 'archived';
  created_at: string;
  tags: string[];
}

export interface Collaboration {
  id: number;
  title: string;
  description: string;
  status: 'proposed' | 'active' | 'completed';
  participants: { slug: string; name: string; color: string }[];
  innovation_ids: number[];
  created_at: string;
}

export interface LabSession {
  id: number;
  title: string;
  focus_domain: string;
  status: 'scheduled' | 'active' | 'completed' | 'cancelled';
  participants: string[];
  findings: string;
  started_at: string;
  ended_at: string | null;
}

export interface StatsResponse {
  total_innovations: number;
  total_teammates: number;
  total_collaborations: number;
  total_sessions: number;
  avg_impact: number;
  avg_feasibility: number;
  avg_novelty: number;
  domain_counts: Record<string, number>;
  domain_avg_impact: Record<string, number>;
  domain_avg_feasibility: Record<string, number>;
  domain_avg_novelty: Record<string, number>;
  status_counts: Record<string, number>;
  horizon_counts: Record<string, number>;
}

// ─── API Envelope Unwrapper ──────────────────────────────────────────────────

async function fetchJSON<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${res.statusText}`);
  const envelope = await res.json();
  if (envelope.status === 'ok' && envelope.data !== undefined) {
    return envelope.data as T;
  }
  return envelope as T;
}

// ─── Demo / Fallback Data ────────────────────────────────────────────────────

const TEAMMATE_COLORS: Record<string, string> = {
  'fiscal-alchemist': '#C9A726',
  'impact-investor': '#2E8B57',
  'data-inventor': '#4169E1',
  'tech-futurist': '#9333EA',
  'legislative-inventor': '#DC2626',
  'regulatory-hacker': '#EA580C',
  'service-designer': '#0891B2',
  'space-architect': '#6D28D9',
  'measurement-scientist': '#059669',
  'narrative-researcher': '#DB2777',
  'market-maker': '#CA8A04',
  'architect': '#475569',
};

export const DEMO_TEAMMATES: Teammate[] = [
  {
    id: 1, slug: 'fiscal-alchemist', name: 'The Fiscal Alchemist', title: 'Revenue Transformation Specialist',
    domain: 'Revenue & Fiscal Innovation', description: 'Transforms municipal revenue structures through creative fiscal engineering, alternative funding mechanisms, and public-private value capture strategies.',
    color: '#C9A726', innovation_count: 14, avg_impact: 4.2, avg_feasibility: 3.8, avg_novelty: 4.5, status: 'active',
  },
  {
    id: 2, slug: 'impact-investor', name: 'The Impact Investor', title: 'Social Returns Architect',
    domain: 'Impact Investment & Social Finance', description: 'Designs investment vehicles that generate measurable social returns alongside financial sustainability for public programs.',
    color: '#2E8B57', innovation_count: 11, avg_impact: 4.5, avg_feasibility: 3.6, avg_novelty: 4.1, status: 'active',
  },
  {
    id: 3, slug: 'data-inventor', name: 'The Data Inventor', title: 'Information Systems Architect',
    domain: 'Data Infrastructure & Analytics', description: 'Engineers novel data architectures and analytical frameworks that reveal hidden patterns in government operations and community needs.',
    color: '#4169E1', innovation_count: 18, avg_impact: 4.0, avg_feasibility: 4.2, avg_novelty: 4.7, status: 'active',
  },
  {
    id: 4, slug: 'tech-futurist', name: 'The Tech Futurist', title: 'Emerging Technology Strategist',
    domain: 'Technology & Digital Innovation', description: 'Scouts and adapts emerging technologies for government application, from AI-driven service delivery to blockchain-based transparency systems.',
    color: '#9333EA', innovation_count: 16, avg_impact: 4.3, avg_feasibility: 3.4, avg_novelty: 4.8, status: 'active',
  },
  {
    id: 5, slug: 'legislative-inventor', name: 'The Legislative Inventor', title: 'Policy Innovation Engineer',
    domain: 'Legislative Design & Policy', description: 'Crafts novel legislative frameworks and policy instruments that enable rather than constrain innovation in public service.',
    color: '#DC2626', innovation_count: 12, avg_impact: 4.6, avg_feasibility: 3.2, avg_novelty: 4.3, status: 'active',
  },
  {
    id: 6, slug: 'regulatory-hacker', name: 'The Regulatory Hacker', title: 'Compliance Innovation Specialist',
    domain: 'Regulatory Innovation', description: 'Finds creative pathways through regulatory frameworks, identifying opportunities for innovation within existing compliance structures.',
    color: '#EA580C', innovation_count: 10, avg_impact: 3.9, avg_feasibility: 4.4, avg_novelty: 4.0, status: 'active',
  },
  {
    id: 7, slug: 'service-designer', name: 'The Service Designer', title: 'Human-Centered Systems Architect',
    domain: 'Service Design & Delivery', description: 'Reimagines government service delivery through human-centered design, reducing friction and increasing accessibility for all residents.',
    color: '#0891B2', innovation_count: 15, avg_impact: 4.4, avg_feasibility: 4.0, avg_novelty: 3.9, status: 'active',
  },
  {
    id: 8, slug: 'space-architect', name: 'The Space Architect', title: 'Urban Infrastructure Innovator',
    domain: 'Physical Space & Infrastructure', description: 'Reimagines physical infrastructure and urban spaces as platforms for innovation, community building, and adaptive reuse.',
    color: '#6D28D9', innovation_count: 13, avg_impact: 4.1, avg_feasibility: 3.5, avg_novelty: 4.4, status: 'active',
  },
  {
    id: 9, slug: 'measurement-scientist', name: 'The Measurement Scientist', title: 'Outcomes & Evaluation Engineer',
    domain: 'Impact Measurement & Evaluation', description: 'Develops rigorous measurement frameworks that capture true program impact, enabling evidence-based iteration of government innovations.',
    color: '#059669', innovation_count: 9, avg_impact: 3.8, avg_feasibility: 4.3, avg_novelty: 4.2, status: 'active',
  },
  {
    id: 10, slug: 'narrative-researcher', name: 'The Narrative Researcher', title: 'Public Engagement Strategist',
    domain: 'Communication & Public Narrative', description: 'Crafts compelling narratives that build public support for innovation, translating complex policy into stories that resonate.',
    color: '#DB2777', innovation_count: 8, avg_impact: 3.7, avg_feasibility: 4.5, avg_novelty: 3.8, status: 'active',
  },
  {
    id: 11, slug: 'market-maker', name: 'The Market Maker', title: 'Economic Ecosystem Designer',
    domain: 'Market Design & Economic Systems', description: 'Designs market mechanisms and economic incentive structures that align private action with public benefit.',
    color: '#CA8A04', innovation_count: 11, avg_impact: 4.3, avg_feasibility: 3.7, avg_novelty: 4.6, status: 'active',
  },
  {
    id: 12, slug: 'architect', name: 'The Architect', title: 'Systems Integration Coordinator',
    domain: 'Coordination & Architecture', description: 'Orchestrates cross-domain collaboration, ensuring innovations work together as a coherent system rather than isolated experiments.',
    color: '#475569', innovation_count: 7, avg_impact: 4.0, avg_feasibility: 4.1, avg_novelty: 3.6, status: 'active',
  },
];

export const DEMO_INNOVATIONS: Innovation[] = [
  {
    id: 1, title: 'Land Value Recapture Mechanism', summary: 'Automated system to capture incremental land value increases from public infrastructure investments, redirecting gains into community development funds.',
    detail: '', domain: 'Revenue & Fiscal Innovation', teammate_slug: 'fiscal-alchemist', teammate_name: 'The Fiscal Alchemist',
    impact_score: 5, feasibility_score: 3, novelty_score: 4, time_horizon: 'medium', status: 'approved', created_at: '2025-12-15T10:00:00Z', tags: ['revenue', 'land-value', 'automation'],
  },
  {
    id: 2, title: 'Social Impact Bond Dashboard', summary: 'Real-time performance tracking platform for social impact bonds, enabling dynamic pricing adjustments based on outcome achievement rates.',
    detail: '', domain: 'Impact Investment & Social Finance', teammate_slug: 'impact-investor', teammate_name: 'The Impact Investor',
    impact_score: 4, feasibility_score: 4, novelty_score: 5, time_horizon: 'near', status: 'approved', created_at: '2025-12-14T09:00:00Z', tags: ['sib', 'dashboard', 'outcomes'],
  },
  {
    id: 3, title: 'Cross-Agency Data Lake Architecture', summary: 'Federated data architecture enabling real-time cross-agency data sharing while maintaining department-level governance and privacy controls.',
    detail: '', domain: 'Data Infrastructure & Analytics', teammate_slug: 'data-inventor', teammate_name: 'The Data Inventor',
    impact_score: 5, feasibility_score: 4, novelty_score: 5, time_horizon: 'medium', status: 'review', created_at: '2025-12-13T14:00:00Z', tags: ['data-lake', 'cross-agency', 'federated'],
  },
  {
    id: 4, title: 'AI-Powered Permit Routing', summary: 'Machine learning system that automatically routes permit applications to the optimal review pathway, reducing processing time by 60%.',
    detail: '', domain: 'Technology & Digital Innovation', teammate_slug: 'tech-futurist', teammate_name: 'The Tech Futurist',
    impact_score: 4, feasibility_score: 5, novelty_score: 4, time_horizon: 'near', status: 'approved', created_at: '2025-12-12T11:00:00Z', tags: ['ai', 'permits', 'automation'],
  },
  {
    id: 5, title: 'Innovation Sandbox Legislation', summary: 'Model legislation creating protected regulatory sandboxes for testing government innovations with reduced compliance burden and built-in sunset clauses.',
    detail: '', domain: 'Legislative Design & Policy', teammate_slug: 'legislative-inventor', teammate_name: 'The Legislative Inventor',
    impact_score: 5, feasibility_score: 3, novelty_score: 5, time_horizon: 'medium', status: 'review', created_at: '2025-12-11T08:00:00Z', tags: ['sandbox', 'legislation', 'innovation'],
  },
  {
    id: 6, title: 'Compliance-as-Code Framework', summary: 'Executable compliance specifications that automatically validate government innovations against regulatory requirements during development.',
    detail: '', domain: 'Regulatory Innovation', teammate_slug: 'regulatory-hacker', teammate_name: 'The Regulatory Hacker',
    impact_score: 4, feasibility_score: 4, novelty_score: 5, time_horizon: 'near', status: 'approved', created_at: '2025-12-10T15:00:00Z', tags: ['compliance', 'code', 'automation'],
  },
  {
    id: 7, title: 'One-Stop Digital Service Portal', summary: 'Unified digital gateway aggregating all city services with intelligent routing, pre-filled forms, and proactive eligibility notifications.',
    detail: '', domain: 'Service Design & Delivery', teammate_slug: 'service-designer', teammate_name: 'The Service Designer',
    impact_score: 5, feasibility_score: 4, novelty_score: 3, time_horizon: 'near', status: 'approved', created_at: '2025-12-09T12:00:00Z', tags: ['portal', 'digital', 'services'],
  },
  {
    id: 8, title: 'Adaptive Reuse Accelerator', summary: 'Framework for rapid conversion of underutilized city properties into innovation hubs, combining zoning flexibility with modular construction.',
    detail: '', domain: 'Physical Space & Infrastructure', teammate_slug: 'space-architect', teammate_name: 'The Space Architect',
    impact_score: 4, feasibility_score: 3, novelty_score: 4, time_horizon: 'medium', status: 'review', created_at: '2025-12-08T10:00:00Z', tags: ['reuse', 'property', 'construction'],
  },
  {
    id: 9, title: 'Composite Outcome Index', summary: 'Multi-dimensional measurement framework combining quantitative metrics with qualitative community feedback for holistic program evaluation.',
    detail: '', domain: 'Impact Measurement & Evaluation', teammate_slug: 'measurement-scientist', teammate_name: 'The Measurement Scientist',
    impact_score: 4, feasibility_score: 5, novelty_score: 4, time_horizon: 'near', status: 'approved', created_at: '2025-12-07T09:00:00Z', tags: ['measurement', 'outcomes', 'index'],
  },
  {
    id: 10, title: 'Civic Innovation Storytelling Platform', summary: 'Digital platform for collecting and amplifying resident stories about government innovation impact, building narrative evidence alongside data.',
    detail: '', domain: 'Communication & Public Narrative', teammate_slug: 'narrative-researcher', teammate_name: 'The Narrative Researcher',
    impact_score: 3, feasibility_score: 5, novelty_score: 4, time_horizon: 'near', status: 'draft', created_at: '2025-12-06T14:00:00Z', tags: ['storytelling', 'civic', 'platform'],
  },
  {
    id: 11, title: 'Micro-Enterprise Incentive Engine', summary: 'Dynamic incentive system matching small business development needs with city resources, using market-making algorithms to optimize allocation.',
    detail: '', domain: 'Market Design & Economic Systems', teammate_slug: 'market-maker', teammate_name: 'The Market Maker',
    impact_score: 4, feasibility_score: 3, novelty_score: 5, time_horizon: 'medium', status: 'review', created_at: '2025-12-05T11:00:00Z', tags: ['micro-enterprise', 'incentives', 'matching'],
  },
  {
    id: 12, title: 'Innovation Pipeline Orchestrator', summary: 'System for tracking innovations from ideation through implementation, managing cross-team dependencies and resource allocation.',
    detail: '', domain: 'Coordination & Architecture', teammate_slug: 'architect', teammate_name: 'The Architect',
    impact_score: 4, feasibility_score: 4, novelty_score: 3, time_horizon: 'near', status: 'approved', created_at: '2025-12-04T08:00:00Z', tags: ['pipeline', 'orchestration', 'tracking'],
  },
  {
    id: 13, title: 'Blockchain Tax Transparency Ledger', summary: 'Distributed ledger system providing real-time transparency into municipal tax collection and allocation, building public trust through verifiable data.',
    detail: '', domain: 'Revenue & Fiscal Innovation', teammate_slug: 'fiscal-alchemist', teammate_name: 'The Fiscal Alchemist',
    impact_score: 4, feasibility_score: 2, novelty_score: 5, time_horizon: 'far', status: 'draft', created_at: '2025-12-03T16:00:00Z', tags: ['blockchain', 'tax', 'transparency'],
  },
  {
    id: 14, title: 'Predictive Service Demand Model', summary: 'ML model forecasting community service demand by neighborhood, enabling proactive resource deployment before crises emerge.',
    detail: '', domain: 'Data Infrastructure & Analytics', teammate_slug: 'data-inventor', teammate_name: 'The Data Inventor',
    impact_score: 5, feasibility_score: 3, novelty_score: 5, time_horizon: 'medium', status: 'review', created_at: '2025-12-02T13:00:00Z', tags: ['predictive', 'ml', 'demand'],
  },
  {
    id: 15, title: 'Digital Twin City Simulator', summary: 'Virtual replica of city infrastructure enabling policy simulation and impact testing before real-world implementation.',
    detail: '', domain: 'Technology & Digital Innovation', teammate_slug: 'tech-futurist', teammate_name: 'The Tech Futurist',
    impact_score: 5, feasibility_score: 2, novelty_score: 5, time_horizon: 'far', status: 'draft', created_at: '2025-12-01T10:00:00Z', tags: ['digital-twin', 'simulation', 'city'],
  },
  {
    id: 16, title: 'Community Wealth Building Zones', summary: 'Designated zones with special economic rules favoring cooperative ownership, local hiring, and community land trusts.',
    detail: '', domain: 'Market Design & Economic Systems', teammate_slug: 'market-maker', teammate_name: 'The Market Maker',
    impact_score: 5, feasibility_score: 3, novelty_score: 4, time_horizon: 'medium', status: 'review', created_at: '2025-11-30T09:00:00Z', tags: ['community-wealth', 'zones', 'cooperative'],
  },
  {
    id: 17, title: 'Resident Experience Score', summary: 'Continuous measurement system tracking resident experience across all government touchpoints, similar to NPS but for civic services.',
    detail: '', domain: 'Impact Measurement & Evaluation', teammate_slug: 'measurement-scientist', teammate_name: 'The Measurement Scientist',
    impact_score: 4, feasibility_score: 4, novelty_score: 3, time_horizon: 'near', status: 'approved', created_at: '2025-11-29T14:00:00Z', tags: ['resident', 'experience', 'nps'],
  },
  {
    id: 18, title: 'Regulatory API Gateway', summary: 'Programmable interface exposing regulatory requirements as queryable APIs, enabling automated compliance checking for developers and businesses.',
    detail: '', domain: 'Regulatory Innovation', teammate_slug: 'regulatory-hacker', teammate_name: 'The Regulatory Hacker',
    impact_score: 4, feasibility_score: 4, novelty_score: 5, time_horizon: 'medium', status: 'approved', created_at: '2025-11-28T11:00:00Z', tags: ['api', 'regulatory', 'gateway'],
  },
];

export const DEMO_COLLABORATIONS: Collaboration[] = [
  {
    id: 1, title: 'Data-Driven Fiscal Innovation Pipeline', description: 'Combining data analytics with fiscal engineering to identify and capture new revenue opportunities through predictive modeling.',
    status: 'active', participants: [
      { slug: 'fiscal-alchemist', name: 'The Fiscal Alchemist', color: '#C9A726' },
      { slug: 'data-inventor', name: 'The Data Inventor', color: '#4169E1' },
      { slug: 'measurement-scientist', name: 'The Measurement Scientist', color: '#059669' },
    ], innovation_ids: [1, 3, 14], created_at: '2025-12-10T10:00:00Z',
  },
  {
    id: 2, title: 'Smart Service Delivery Ecosystem', description: 'Integrating AI-powered routing with human-centered design to create a next-generation service delivery platform.',
    status: 'active', participants: [
      { slug: 'tech-futurist', name: 'The Tech Futurist', color: '#9333EA' },
      { slug: 'service-designer', name: 'The Service Designer', color: '#0891B2' },
      { slug: 'regulatory-hacker', name: 'The Regulatory Hacker', color: '#EA580C' },
    ], innovation_ids: [4, 6, 7], created_at: '2025-12-08T09:00:00Z',
  },
  {
    id: 3, title: 'Innovation Accountability Framework', description: 'Building measurement systems into the innovation pipeline from day one, with public narrative components for transparency.',
    status: 'proposed', participants: [
      { slug: 'measurement-scientist', name: 'The Measurement Scientist', color: '#059669' },
      { slug: 'narrative-researcher', name: 'The Narrative Researcher', color: '#DB2777' },
      { slug: 'architect', name: 'The Architect', color: '#475569' },
    ], innovation_ids: [9, 10, 12], created_at: '2025-12-05T14:00:00Z',
  },
  {
    id: 4, title: 'Community Economic Resilience', description: 'Designing market mechanisms and investment structures that build lasting community economic resilience.',
    status: 'active', participants: [
      { slug: 'impact-investor', name: 'The Impact Investor', color: '#2E8B57' },
      { slug: 'market-maker', name: 'The Market Maker', color: '#CA8A04' },
      { slug: 'space-architect', name: 'The Space Architect', color: '#6D28D9' },
    ], innovation_ids: [2, 8, 11, 16], created_at: '2025-12-01T11:00:00Z',
  },
  {
    id: 5, title: 'Legislative Innovation Sandbox', description: 'Creating the legal and regulatory framework for government innovation experimentation.',
    status: 'completed', participants: [
      { slug: 'legislative-inventor', name: 'The Legislative Inventor', color: '#DC2626' },
      { slug: 'regulatory-hacker', name: 'The Regulatory Hacker', color: '#EA580C' },
    ], innovation_ids: [5, 6], created_at: '2025-11-15T10:00:00Z',
  },
];

export const DEMO_SESSIONS: LabSession[] = [
  {
    id: 1, title: 'Cross-Domain Revenue Innovation Sprint', focus_domain: 'Revenue & Fiscal Innovation',
    status: 'completed', participants: ['fiscal-alchemist', 'data-inventor', 'impact-investor'],
    findings: 'Identified 3 new revenue capture mechanisms leveraging real-time property data. Estimated annual yield: $12M. Next step: feasibility analysis with regulatory-hacker.',
    started_at: '2025-12-14T09:00:00Z', ended_at: '2025-12-14T17:00:00Z',
  },
  {
    id: 2, title: 'Service Delivery Redesign Workshop', focus_domain: 'Service Design & Delivery',
    status: 'completed', participants: ['service-designer', 'tech-futurist', 'narrative-researcher'],
    findings: 'Mapped 47 resident journey friction points across 8 service categories. Prioritized top 10 for rapid prototyping. Digital portal MVP spec completed.',
    started_at: '2025-12-12T10:00:00Z', ended_at: '2025-12-12T16:00:00Z',
  },
  {
    id: 3, title: 'Data Architecture Deep Dive', focus_domain: 'Data Infrastructure & Analytics',
    status: 'active', participants: ['data-inventor', 'measurement-scientist', 'architect'],
    findings: 'Working session on federated data lake design. Privacy-preserving linkage protocol under development.',
    started_at: '2025-12-15T09:00:00Z', ended_at: null,
  },
  {
    id: 4, title: 'Impact Investment Strategy Session', focus_domain: 'Impact Investment & Social Finance',
    status: 'scheduled', participants: ['impact-investor', 'fiscal-alchemist', 'market-maker', 'measurement-scientist'],
    findings: '', started_at: '2025-12-18T10:00:00Z', ended_at: null,
  },
  {
    id: 5, title: 'Regulatory Sandbox Design Sprint', focus_domain: 'Regulatory Innovation',
    status: 'completed', participants: ['regulatory-hacker', 'legislative-inventor', 'tech-futurist'],
    findings: 'Drafted sandbox framework v2.0 with automated compliance monitoring hooks. Compliance-as-Code integration points identified for 3 pilot programs.',
    started_at: '2025-12-08T09:00:00Z', ended_at: '2025-12-08T17:00:00Z',
  },
  {
    id: 6, title: 'Urban Space Innovation Lab', focus_domain: 'Physical Space & Infrastructure',
    status: 'scheduled', participants: ['space-architect', 'service-designer', 'narrative-researcher'],
    findings: '', started_at: '2025-12-20T10:00:00Z', ended_at: null,
  },
];

export const DEMO_STATS: StatsResponse = {
  total_innovations: 18,
  total_teammates: 12,
  total_collaborations: 5,
  total_sessions: 6,
  avg_impact: 4.3,
  avg_feasibility: 3.6,
  avg_novelty: 4.4,
  domain_counts: {
    'Revenue & Fiscal Innovation': 2,
    'Impact Investment & Social Finance': 1,
    'Data Infrastructure & Analytics': 2,
    'Technology & Digital Innovation': 2,
    'Legislative Design & Policy': 1,
    'Regulatory Innovation': 2,
    'Service Design & Delivery': 1,
    'Physical Space & Infrastructure': 1,
    'Impact Measurement & Evaluation': 2,
    'Communication & Public Narrative': 1,
    'Market Design & Economic Systems': 2,
    'Coordination & Architecture': 1,
  },
  domain_avg_impact: {
    'Revenue & Fiscal Innovation': 4.5,
    'Impact Investment & Social Finance': 4.5,
    'Data Infrastructure & Analytics': 5.0,
    'Technology & Digital Innovation': 4.5,
    'Legislative Design & Policy': 5.0,
    'Regulatory Innovation': 4.0,
    'Service Design & Delivery': 5.0,
    'Physical Space & Infrastructure': 4.0,
    'Impact Measurement & Evaluation': 4.0,
    'Communication & Public Narrative': 3.0,
    'Market Design & Economic Systems': 4.5,
    'Coordination & Architecture': 4.0,
  },
  domain_avg_feasibility: {
    'Revenue & Fiscal Innovation': 2.5,
    'Impact Investment & Social Finance': 4.0,
    'Data Infrastructure & Analytics': 3.5,
    'Technology & Digital Innovation': 3.5,
    'Legislative Design & Policy': 3.0,
    'Regulatory Innovation': 4.0,
    'Service Design & Delivery': 4.0,
    'Physical Space & Infrastructure': 3.0,
    'Impact Measurement & Evaluation': 4.5,
    'Communication & Public Narrative': 5.0,
    'Market Design & Economic Systems': 3.0,
    'Coordination & Architecture': 4.0,
  },
  domain_avg_novelty: {
    'Revenue & Fiscal Innovation': 4.5,
    'Impact Investment & Social Finance': 5.0,
    'Data Infrastructure & Analytics': 5.0,
    'Technology & Digital Innovation': 4.5,
    'Legislative Design & Policy': 5.0,
    'Regulatory Innovation': 5.0,
    'Service Design & Delivery': 3.0,
    'Physical Space & Infrastructure': 4.0,
    'Impact Measurement & Evaluation': 3.5,
    'Communication & Public Narrative': 4.0,
    'Market Design & Economic Systems': 4.5,
    'Coordination & Architecture': 3.0,
  },
  status_counts: { draft: 3, review: 5, approved: 8, archived: 2 },
  horizon_counts: { near: 8, medium: 7, far: 3 },
};

// ─── Color Helpers ───────────────────────────────────────────────────────────

export function getTeammateColor(slug: string): string {
  return TEAMMATE_COLORS[slug] || '#475569';
}

export function getStatusColor(status: string): string {
  const colors: Record<string, string> = {
    draft: '#6B7280', review: '#D97706', approved: '#059669', archived: '#4B5563',
    proposed: '#8B5CF6', active: '#2563EB', completed: '#10B981',
    scheduled: '#D97706', cancelled: '#DC2626',
    standby: '#D97706', offline: '#6B7280',
  };
  return colors[status] || '#6B7280';
}

export function getHorizonLabel(horizon: string): string {
  const labels: Record<string, string> = {
    near: '0-2 YRS', medium: '2-5 YRS', far: '5+ YRS',
  };
  return labels[horizon] || horizon.toUpperCase();
}

// ─── API Functions ───────────────────────────────────────────────────────────

export async function getTeammates(): Promise<Teammate[]> {
  try {
    return await fetchJSON<Teammate[]>('/api/teammates');
  } catch {
    return DEMO_TEAMMATES;
  }
}

export async function getTeammate(slug: string): Promise<Teammate | undefined> {
  try {
    return await fetchJSON<Teammate>(`/api/teammates/${slug}`);
  } catch {
    return DEMO_TEAMMATES.find(t => t.slug === slug);
  }
}

export async function getInnovations(filters?: {
  domain?: string;
  status?: string;
  time_horizon?: string;
  min_impact?: number;
  sort?: string;
}): Promise<Innovation[]> {
  try {
    const params = new URLSearchParams();
    if (filters?.domain) params.set('domain', filters.domain);
    if (filters?.status) params.set('status', filters.status);
    if (filters?.time_horizon) params.set('time_horizon', filters.time_horizon);
    if (filters?.min_impact) params.set('min_impact', String(filters.min_impact));
    if (filters?.sort) params.set('sort', filters.sort);
    const qs = params.toString();
    return await fetchJSON<Innovation[]>(`/api/innovations${qs ? '?' + qs : ''}`);
  } catch {
    let result = [...DEMO_INNOVATIONS];
    if (filters?.domain) result = result.filter(i => i.domain === filters.domain);
    if (filters?.status) result = result.filter(i => i.status === filters.status);
    if (filters?.time_horizon) result = result.filter(i => i.time_horizon === filters.time_horizon);
    if (filters?.min_impact) result = result.filter(i => i.impact_score >= filters.min_impact!);
    if (filters?.sort) {
      const sortMap: Record<string, (a: Innovation, b: Innovation) => number> = {
        newest: (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
        impact: (a, b) => b.impact_score - a.impact_score,
        feasibility: (a, b) => b.feasibility_score - a.feasibility_score,
        novelty: (a, b) => b.novelty_score - a.novelty_score,
      };
      if (sortMap[filters.sort]) result.sort(sortMap[filters.sort]);
    }
    return result;
  }
}

export async function getInnovation(id: number): Promise<Innovation | undefined> {
  try {
    return await fetchJSON<Innovation>(`/api/innovations/${id}`);
  } catch {
    return DEMO_INNOVATIONS.find(i => i.id === id);
  }
}

export async function createInnovation(data: Partial<Innovation>): Promise<Innovation> {
  try {
    return await fetchJSON<Innovation>('/api/innovations', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  } catch {
    const newInnovation: Innovation = {
      id: DEMO_INNOVATIONS.length + 1,
      title: data.title || 'New Innovation',
      summary: data.summary || 'Generated innovation concept.',
      detail: data.detail || '',
      domain: data.domain || 'Coordination & Architecture',
      teammate_slug: data.teammate_slug || 'architect',
      teammate_name: data.teammate_name || 'The Architect',
      impact_score: data.impact_score || 3,
      feasibility_score: data.feasibility_score || 3,
      novelty_score: data.novelty_score || 3,
      time_horizon: data.time_horizon || 'medium',
      status: 'draft',
      created_at: new Date().toISOString(),
      tags: data.tags || [],
    };
    return newInnovation;
  }
}

export async function getCollaborations(): Promise<Collaboration[]> {
  try {
    return await fetchJSON<Collaboration[]>('/api/collaborations');
  } catch {
    return DEMO_COLLABORATIONS;
  }
}

export async function getStats(): Promise<StatsResponse> {
  try {
    return await fetchJSON<StatsResponse>('/api/stats');
  } catch {
    return DEMO_STATS;
  }
}

export async function generateInnovation(slug: string): Promise<Innovation> {
  try {
    return await fetchJSON<Innovation>(`/api/generate/${slug}`, { method: 'POST' });
  } catch {
    const teammate = DEMO_TEAMMATES.find(t => t.slug === slug);
    const titles: Record<string, string> = {
      'fiscal-alchemist': 'Dynamic Revenue Optimization Engine',
      'impact-investor': 'Green Bond Accelerator Platform',
      'data-inventor': 'Neural Graph Analytics Framework',
      'tech-futurist': 'Quantum-Ready Government Cloud',
      'legislative-inventor': 'Adaptive Policy Compiler',
      'regulatory-hacker': 'Zero-Friction Compliance Gateway',
      'service-designer': 'Empathy-Mapped Service Blueprint',
      'space-architect': 'Modular Urban Commons Network',
      'measurement-scientist': 'Causal Impact Attribution System',
      'narrative-researcher': 'Participatory Evidence Narrative Engine',
      'market-maker': 'Decentralized Public Goods Exchange',
      'architect': 'Cross-Domain Synergy Orchestrator',
    };
    const summaries: Record<string, string> = {
      'fiscal-alchemist': 'AI-driven system that continuously optimizes revenue collection strategies across multiple channels, adapting to economic conditions in real-time.',
      'impact-investor': 'Platform connecting green infrastructure projects with impact-focused capital, using automated outcome verification for payment triggers.',
      'data-inventor': 'Graph-based analytics engine that discovers non-obvious relationships between city datasets, revealing intervention opportunities invisible to traditional analysis.',
      'tech-futurist': 'Quantum-computing-ready cloud architecture that future-proofs government digital infrastructure while providing immediate classical computing benefits.',
      'legislative-inventor': 'System that translates policy objectives into testable legislative specifications, enabling simulation of policy outcomes before enactment.',
      'regulatory-hacker': 'Unified API gateway that handles all regulatory compliance checks automatically, reducing business-government friction to near-zero.',
      'service-designer': 'Service design methodology mapping emotional journeys alongside functional requirements, ensuring government services respect human dignity at every touchpoint.',
      'space-architect': 'Network of adaptable community spaces that reconfigure based on neighborhood needs, from co-working to emergency shelter to event venues.',
      'measurement-scientist': 'Statistical framework that isolates the causal impact of specific interventions from background trends, providing actionable evidence for policy decisions.',
      'narrative-researcher': 'Platform where residents co-create evidence narratives about innovation impacts, building bridges between data-driven and story-driven understanding.',
      'market-maker': 'Blockchain-based marketplace for public goods where community members can fund, trade, and govern local development projects collectively.',
      'architect': 'System identifying synergy opportunities across all innovation domains, automatically suggesting collaborations with highest combined impact potential.',
    };
    return {
      id: Math.floor(Math.random() * 1000) + 100,
      title: titles[slug] || 'Generated Innovation Concept',
      summary: summaries[slug] || 'A novel approach generated by the innovation laboratory.',
      detail: '',
      domain: teammate?.domain || 'General',
      teammate_slug: slug,
      teammate_name: teammate?.name || 'Unknown',
      impact_score: Math.floor(Math.random() * 3) + 3,
      feasibility_score: Math.floor(Math.random() * 3) + 2,
      novelty_score: Math.floor(Math.random() * 3) + 3,
      time_horizon: (['near', 'medium', 'far'] as const)[Math.floor(Math.random() * 3)],
      status: 'draft',
      created_at: new Date().toISOString(),
      tags: ['generated', slug],
    };
  }
}

export async function getSessions(): Promise<LabSession[]> {
  try {
    return await fetchJSON<LabSession[]>('/api/sessions');
  } catch {
    return DEMO_SESSIONS;
  }
}
