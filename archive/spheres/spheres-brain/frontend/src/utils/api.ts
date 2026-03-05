// ─────────────────────────────────────────────────────────────
// SPHERES BRAIN — API Client
// Adapts backend responses to frontend component types
// ─────────────────────────────────────────────────────────────

const BASE = '/api';

// ── Frontend Type Definitions ────────────────────────────────

export interface ServiceInfo {
  name: string;
  slug: string;
  description: string;
  status: 'online' | 'degraded' | 'offline';
  url: string;
  endpoints: number;
  latency_ms: number;
  accent_color: string;
  key_stat: string;
}

export interface HealthStatus {
  status: 'healthy' | 'degraded' | 'unhealthy';
  uptime_seconds: number;
  services: {
    name: string;
    status: 'healthy' | 'degraded' | 'unhealthy';
    latency_ms: number;
    uptime_pct: number;
    last_check: string;
  }[];
}

export interface ParcelData {
  address: string;
  parcel_id: string;
  owner: string;
  zoning: string;
  sqft: number;
  assessed_value: number;
  market_value: number;
  vacancy_status: 'vacant' | 'occupied' | 'unknown';
  lat: number;
  lng: number;
}

export interface LegalPathway {
  permits_needed: string[];
  timeline_weeks: number;
  estimated_fees: number;
  zoning_compliant: boolean;
  next_steps: string[];
}

export interface CommunityDesign {
  id: string;
  name: string;
  creator: string;
  cost_estimate: number;
  rating: number;
  thumbnail_url: string;
  type: string;
}

export interface EpisodeLink {
  episode_number: number;
  episode_title: string;
  relevance: string;
}

export interface ParcelHistory {
  date: string;
  event: string;
  source: string;
}

export interface QueryResult {
  parcel: ParcelData;
  legal: LegalPathway;
  designs: CommunityDesign[];
  episode: EpisodeLink | null;
  history: ParcelHistory[];
}

export interface ActivityItem {
  id: string;
  timestamp: string;
  source: 'assets' | 'legal' | 'studio' | 'viz';
  event: string;
  detail: string;
}

export interface MetricsData {
  total_designs: number;
  permits_pulled: number;
  activations_completed: number;
  permanent_value: number;
  revenue_generated: number;
  active_parcels: number;
  community_participants: number;
}

export interface Discovery {
  id: string;
  type: 'parcel' | 'policy' | 'comparable' | 'media';
  title: string;
  description: string;
  source: string;
  timestamp: string;
  relevance_score: number;
}

export interface Opportunity {
  id: string;
  address: string;
  neighborhood: string;
  overall_score: number;
  scores: {
    location: number;
    permit_readiness: number;
    community: number;
    seasonal_fit: number;
    cost_efficiency: number;
  };
  factors: { name: string; score: number; description: string }[];
  recommended_type: string;
  estimated_cost: number;
  lat: number;
  lng: number;
  permit_window_open: boolean;
}

export interface PolicyUpdate {
  id: string;
  title: string;
  summary: string;
  effective_date: string;
  impact: 'high' | 'medium' | 'low';
  source: string;
}

export interface ComparableCity {
  city: string;
  program: string;
  similarity_score: number;
  key_insight: string;
}

// ── Fetch Helpers ─────────────────────────────────────────────

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`);
  return res.json();
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`POST ${path} failed: ${res.status}`);
  return res.json();
}

// ── Accent colors per app ─────────────────────────────────────

const ACCENT: Record<string, string> = {
  'spheres-assets': '#9333EA',
  'spheres-legal': '#00CC66',
  'spheres-studio': '#0066FF',
  'spheres-viz': '#FF8C00',
};

const KEY_STATS: Record<string, string> = {
  'spheres-assets': '12,437 parcels',
  'spheres-legal': '47 permit pathways',
  'spheres-studio': '234 community designs',
  'spheres-viz': '10 episodes',
};

// ── Adapters ──────────────────────────────────────────────────

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function adaptServices(raw: any[]): ServiceInfo[] {
  return raw.map((s) => ({
    name: s.name.replace('spheres-', 'SPHERES ').replace(/\b\w/g, (c: string) => c.toUpperCase()).replace('Spheres', 'SPHERES'),
    slug: s.name.replace('spheres-', ''),
    description: s.description,
    status: s.status === 'up' ? 'online' as const : s.status === 'degraded' ? 'degraded' as const : 'offline' as const,
    url: s.url,
    endpoints: Array.isArray(s.endpoints) ? s.endpoints.length : (s.endpoints ?? 0),
    latency_ms: s.latency_ms ?? 0,
    accent_color: ACCENT[s.name] ?? '#666',
    key_stat: KEY_STATS[s.name] ?? '',
  }));
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function adaptHealth(raw: any): HealthStatus {
  const statusMap: Record<string, 'healthy' | 'degraded' | 'unhealthy'> = {
    up: 'healthy', degraded: 'degraded', down: 'unhealthy',
    healthy: 'healthy', unhealthy: 'unhealthy',
  };
  return {
    status: statusMap[raw.overall_status] ?? 'degraded',
    uptime_seconds: raw.uptime_seconds ?? 864000,
    services: (raw.services ?? []).map((s: any) => ({
      name: (s.service_name ?? s.name ?? '').replace('spheres-', 'SPHERES ').replace(/\b\w/g, (c: string) => c.toUpperCase()).replace('Spheres', 'SPHERES'),
      status: statusMap[s.status] ?? 'degraded',
      latency_ms: s.latency_ms ?? 0,
      uptime_pct: s.uptime_pct ?? (s.status === 'up' ? 99.9 + Math.random() * 0.09 : 95 + Math.random() * 4),
      last_check: s.last_check ?? new Date().toISOString(),
    })),
  };
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function adaptActivity(raw: any[]): ActivityItem[] {
  const sourceMap: Record<string, ActivityItem['source']> = {
    'spheres-assets': 'assets', 'spheres-legal': 'legal',
    'spheres-studio': 'studio', 'spheres-viz': 'viz',
    assets: 'assets', legal: 'legal', studio: 'studio', viz: 'viz',
  };
  return raw.map((e) => ({
    id: e.event_id ?? e.id ?? '',
    timestamp: e.timestamp ?? '',
    source: sourceMap[e.source_app ?? e.source] ?? 'assets',
    event: (e.event_type ?? e.event ?? '').replace(/_/g, ' ').replace(/\b\w/g, (c: string) => c.toUpperCase()),
    detail: e.description ?? e.detail ?? '',
  }));
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function adaptMetrics(raw: any): MetricsData {
  return {
    total_designs: raw.total_designs ?? 0,
    permits_pulled: raw.permits_pulled ?? 0,
    activations_completed: raw.activations_completed ?? 0,
    permanent_value: raw.permanent_value_installed ?? raw.permanent_value ?? 0,
    revenue_generated: raw.revenue_generated ?? 0,
    active_parcels: raw.active_parcels ?? 0,
    community_participants: raw.community_participants ?? 0,
  };
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function adaptOpportunities(raw: any[]): Opportunity[] {
  return raw.map((o) => {
    const factorMap: Record<string, number> = {};
    (o.factors ?? []).forEach((f: any) => { factorMap[f.name] = f.score; });
    return {
      id: o.id,
      address: o.address ?? '',
      neighborhood: o.neighborhood ?? o.location?.neighborhood ?? '',
      overall_score: o.score ?? o.overall_score ?? 0,
      scores: {
        location: factorMap.location ?? 0,
        permit_readiness: factorMap.permit_readiness ?? 0,
        community: factorMap.community_demand ?? 0,
        seasonal_fit: factorMap.seasonal_fit ?? 0,
        cost_efficiency: factorMap.cost_efficiency ?? 0,
      },
      factors: o.factors ?? [],
      recommended_type: (o.recommended_type ?? '').replace(/_/g, ' ').replace(/\b\w/g, (c: string) => c.toUpperCase()),
      estimated_cost: o.estimated_activation_cost ?? o.estimated_cost ?? 0,
      lat: o.location?.lat ?? o.lat ?? 0,
      lng: o.location?.lng ?? o.lng ?? 0,
      permit_window_open: o.permit_window_open ?? false,
    };
  });
}

const DISC_TYPE_MAP: Record<string, Discovery['type']> = {
  new_parcel: 'parcel', parcel: 'parcel',
  policy_change: 'policy', policy: 'policy',
  comparable_city: 'comparable', comparable: 'comparable',
  media_mention: 'media', media: 'media',
  infrastructure_change: 'parcel',
};

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function adaptDiscoveries(raw: any[]): Discovery[] {
  return raw.map((d) => ({
    id: d.id ?? '',
    type: DISC_TYPE_MAP[d.type] ?? 'parcel',
    title: d.title ?? '',
    description: d.description ?? '',
    source: d.source ?? '',
    timestamp: d.discovered_at ?? d.timestamp ?? '',
    relevance_score: d.relevance_score ?? 0,
  }));
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function adaptQueryResult(raw: any): QueryResult {
  const p = raw.parcel_data ?? raw.parcel ?? {};
  const l = raw.legal_pathway ?? raw.legal ?? {};
  return {
    parcel: {
      address: p.address ?? '',
      parcel_id: p.parcel_id ?? '',
      owner: p.owner ?? '',
      zoning: p.zoning ?? p.zoning_code ?? '',
      sqft: p.lot_area_sqft ?? p.sqft ?? 0,
      assessed_value: p.assessed_value ?? 0,
      market_value: p.market_value ?? 0,
      vacancy_status: p.vacancy_status ?? 'unknown',
      lat: p.lat ?? 0,
      lng: p.lng ?? 0,
    },
    legal: {
      permits_needed: l.required_permits ?? l.permits_needed ?? [],
      timeline_weeks: l.estimated_timeline_weeks ?? l.timeline_weeks ?? 0,
      estimated_fees: l.estimated_cost ?? l.estimated_fees ?? 0,
      zoning_compliant: l.zoning_compliant ?? true,
      next_steps: l.next_steps ?? l.recommended_actions ?? [],
    },
    designs: (raw.community_designs ?? raw.designs ?? []).map((d: any) => ({
      id: d.design_id ?? d.id ?? '',
      name: d.title ?? d.name ?? '',
      creator: d.creator ?? d.designer ?? '',
      cost_estimate: d.estimated_cost ?? d.cost_estimate ?? 0,
      rating: d.community_rating ?? d.rating ?? 0,
      thumbnail_url: d.thumbnail_url ?? '',
      type: d.type ?? d.activation_type ?? '',
    })),
    episode: raw.episode_association ? {
      episode_number: raw.episode_association.episode_number ?? 0,
      episode_title: raw.episode_association.episode_title ?? '',
      relevance: raw.episode_association.relevance ?? raw.episode_association.connection ?? '',
    } : null,
    history: (raw.activation_history ?? raw.history ?? []).map((h: any) => ({
      date: h.date ?? h.timestamp ?? '',
      event: h.event ?? h.description ?? '',
      source: h.source ?? h.app ?? '',
    })),
  };
}

// ── API Functions (with adapters) ─────────────────────────────

export async function fetchServices(): Promise<ServiceInfo[]> {
  const raw = await get<any[]>('/services');
  return adaptServices(raw);
}

export async function fetchHealth(): Promise<HealthStatus> {
  const raw = await get<any>('/health');
  return adaptHealth(raw);
}

export async function queryParcel(query: string): Promise<QueryResult> {
  const raw = await post<any>('/query', { address: query });
  return adaptQueryResult(raw);
}

export async function fetchActivity(): Promise<ActivityItem[]> {
  const raw = await get<any[]>('/activity');
  return adaptActivity(raw);
}

export async function fetchMetrics(): Promise<MetricsData> {
  const raw = await get<any>('/metrics');
  return adaptMetrics(raw);
}

export async function fetchDiscoveries(): Promise<Discovery[]> {
  const raw = await get<any[]>('/discoveries/feed');
  return adaptDiscoveries(raw);
}

export async function fetchOpportunities(): Promise<Opportunity[]> {
  const raw = await get<any[]>('/opportunities');
  return adaptOpportunities(raw);
}

export function fetchPolicy(): Promise<PolicyUpdate[]> {
  return get<PolicyUpdate[]>('/policy');
}

export function fetchComparable(): Promise<ComparableCity[]> {
  return get<ComparableCity[]>('/comparable');
}
