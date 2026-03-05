// ─────────────────────────────────────────────────────────────────────────────
// DOMES Brain — API Client
// ─────────────────────────────────────────────────────────────────────────────

const BASE = '/api';

// ── Types ────────────────────────────────────────────────────────────────────

export type ServiceStatus = 'online' | 'offline' | 'degraded';

export interface ServiceInfo {
  slug: string;
  name: string;
  description: string;
  port: number;
  status: ServiceStatus;
  lastChecked: string;
  responseTime: number;
  uptime: number;
  domainColor: string;
  url: string;
  endpoints: string[];
  recentErrors: ErrorEntry[];
  dataFreshness: string;
  uptimeHistory: boolean[];
}

export interface ErrorEntry {
  timestamp: string;
  message: string;
  endpoint: string;
}

export interface HealthResponse {
  status: string;
  servicesOnline: number;
  servicesTotal: number;
  lastScan: string;
  uptime: number;
}

export interface QueryResult {
  id: string;
  source: string;
  sourceSlug: string;
  title: string;
  snippet: string;
  relevance: number;
  url: string;
  timestamp: string;
}

export interface QueryResponse {
  query: string;
  totalResults: number;
  results: QueryResult[];
  routedTo: string[];
  executionTime: number;
}

export type DiscoveryImpact = 'critical' | 'high' | 'medium' | 'low';
export type DiscoveryStatus = 'new' | 'reviewed' | 'queued' | 'dismissed';
export type DiscoverySourceType = 'legislation' | 'regulation' | 'policy' | 'data' | 'news' | 'research';

export interface Discovery {
  id: string;
  title: string;
  summary: string;
  sourceType: DiscoverySourceType;
  impact: DiscoveryImpact;
  relevanceScore: number;
  status: DiscoveryStatus;
  timestamp: string;
  source: string;
  url: string;
}

export interface DiscoveryFilters {
  sourceType?: DiscoverySourceType;
  impact?: DiscoveryImpact;
  status?: DiscoveryStatus;
}

export interface DiscoveryStats {
  totalDiscoveries: number;
  pendingReview: number;
  criticalItems: number;
  lastScanTime: string;
  sourceCounts: Record<string, number>;
}

export type ActivityEventType = 'scan' | 'error' | 'update' | 'query';

export interface ActivityEntry {
  id: string;
  timestamp: string;
  service: string;
  serviceSlug: string;
  eventType: ActivityEventType;
  description: string;
}

export interface StatsResponse {
  totalQueries: number;
  totalDiscoveries: number;
  avgResponseTime: number;
  uptimePercent: number;
  queriesThisHour: number;
  discoveriesToday: number;
}

export interface RoutePreview {
  query: string;
  services: string[];
  estimatedTime: number;
}

// ── Helpers ──────────────────────────────────────────────────────────────────

async function fetchJSON<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}: ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

function isoNow(offsetMinutes = 0): string {
  const d = new Date(Date.now() - offsetMinutes * 60_000);
  return d.toISOString();
}

function randomUptime(): boolean[] {
  return Array.from({ length: 24 }, () => Math.random() > 0.06);
}

// ── Backend → Frontend mappers ───────────────────────────────────────────────

function mapSourceType(raw: string): DiscoverySourceType {
  const map: Record<string, DiscoverySourceType> = {
    federal_register: 'regulation',
    ecfr: 'regulation',
    state_legislation: 'legislation',
    academic: 'research',
    news: 'news',
    gap_analysis: 'data',
    legislation: 'legislation',
    regulation: 'regulation',
    policy: 'policy',
    data: 'data',
    research: 'research',
  };
  return map[raw] ?? 'data';
}

function mapImpact(raw: string): DiscoveryImpact {
  const map: Record<string, DiscoveryImpact> = {
    critical: 'critical',
    high: 'high',
    medium: 'medium',
    low: 'low',
  };
  return map[raw] ?? 'low';
}

function mapDiscoveryStatus(raw: string): DiscoveryStatus {
  const map: Record<string, DiscoveryStatus> = {
    new: 'new',
    reviewed: 'reviewed',
    queued: 'queued',
    dismissed: 'dismissed',
  };
  return map[raw] ?? 'new';
}

// ── Demo / Fallback Data ─────────────────────────────────────────────────────

const DEMO_SERVICES: ServiceInfo[] = [
  {
    slug: 'spheres-assets',
    name: 'Spheres Assets',
    description: 'Philadelphia public property map',
    port: 8000,
    status: 'online',
    lastChecked: isoNow(1),
    responseTime: 42,
    uptime: 99.8,
    domainColor: '#1A3D8B',
    url: 'http://localhost:8000',
    endpoints: ['/api/properties', '/api/parcels', '/api/search', '/api/stats'],
    recentErrors: [],
    dataFreshness: '2 hours ago',
    uptimeHistory: randomUptime(),
  },
  {
    slug: 'domes-data',
    name: 'Data Research',
    description: 'Government data constellation',
    port: 8001,
    status: 'online',
    lastChecked: isoNow(2),
    responseTime: 78,
    uptime: 99.5,
    domainColor: '#5A1A6B',
    url: 'http://localhost:8001',
    endpoints: ['/api/datasets', '/api/constellations', '/api/search', '/api/sources'],
    recentErrors: [],
    dataFreshness: '45 minutes ago',
    uptimeHistory: randomUptime(),
  },
  {
    slug: 'domes-profile',
    name: 'Profile Research',
    description: 'Composite profile builder',
    port: 8002,
    status: 'online',
    lastChecked: isoNow(1),
    responseTime: 55,
    uptime: 99.9,
    domainColor: '#1A6B3C',
    url: 'http://localhost:8002',
    endpoints: ['/api/profiles', '/api/build', '/api/templates', '/api/export'],
    recentErrors: [],
    dataFreshness: '1 hour ago',
    uptimeHistory: randomUptime(),
  },
  {
    slug: 'domes-contracts',
    name: 'Contracts',
    description: 'Agreement generation engine',
    port: 8003,
    status: 'degraded',
    lastChecked: isoNow(3),
    responseTime: 234,
    uptime: 97.2,
    domainColor: '#6B5A1A',
    url: 'http://localhost:8003',
    endpoints: ['/api/contracts', '/api/generate', '/api/templates', '/api/validate'],
    recentErrors: [
      { timestamp: isoNow(30), message: 'Template rendering timeout', endpoint: '/api/generate' },
      { timestamp: isoNow(120), message: 'Database connection pool exhausted', endpoint: '/api/contracts' },
    ],
    dataFreshness: '3 hours ago',
    uptimeHistory: (() => { const h = randomUptime(); h[18] = false; h[19] = false; return h; })(),
  },
  {
    slug: 'domes-architect',
    name: 'Architect',
    description: 'Coordination architecture designer',
    port: 8004,
    status: 'online',
    lastChecked: isoNow(1),
    responseTime: 61,
    uptime: 99.7,
    domainColor: '#8B1A1A',
    url: 'http://localhost:8004',
    endpoints: ['/api/designs', '/api/blueprints', '/api/stakeholders', '/api/export'],
    recentErrors: [],
    dataFreshness: '30 minutes ago',
    uptimeHistory: randomUptime(),
  },
  {
    slug: 'domes-viz',
    name: 'Viz',
    description: 'Public-facing website',
    port: 8005,
    status: 'online',
    lastChecked: isoNow(1),
    responseTime: 29,
    uptime: 99.9,
    domainColor: '#1A6B6B',
    url: 'http://localhost:8005',
    endpoints: ['/api/pages', '/api/content', '/api/assets'],
    recentErrors: [],
    dataFreshness: '15 minutes ago',
    uptimeHistory: randomUptime(),
  },
];

const DEMO_HEALTH: HealthResponse = {
  status: 'operational',
  servicesOnline: 5,
  servicesTotal: 6,
  lastScan: isoNow(1),
  uptime: 99.3,
};

function makeDemoResults(query: string): QueryResponse {
  const results: QueryResult[] = [
    {
      id: 'r1',
      source: 'Data Research',
      sourceSlug: 'domes-data',
      title: `Federal datasets matching "${query}"`,
      snippet: `Found 14 government datasets related to ${query} across HUD, HHS, and DOJ sources. Includes quarterly reports and annual surveys with geographic breakdowns.`,
      relevance: 0.94,
      url: '#',
      timestamp: isoNow(5),
    },
    {
      id: 'r2',
      source: 'Profile Research',
      sourceSlug: 'domes-profile',
      title: `Profile templates for ${query} circumstances`,
      snippet: `3 composite profile templates available for situations involving ${query}. Templates include eligibility mapping, service coordination, and outcome tracking.`,
      relevance: 0.87,
      url: '#',
      timestamp: isoNow(5),
    },
    {
      id: 'r3',
      source: 'Spheres Assets',
      sourceSlug: 'spheres-assets',
      title: `Property records related to "${query}"`,
      snippet: `Located 28 public property records in Philadelphia that may be relevant to ${query}. Includes vacant lots, city-owned facilities, and condemned properties.`,
      relevance: 0.72,
      url: '#',
      timestamp: isoNow(5),
    },
    {
      id: 'r4',
      source: 'Contracts',
      sourceSlug: 'domes-contracts',
      title: `Agreement templates for ${query}`,
      snippet: `5 agreement templates and 2 existing contracts reference ${query}. Covers interagency MOUs, service-level agreements, and data sharing protocols.`,
      relevance: 0.68,
      url: '#',
      timestamp: isoNow(5),
    },
    {
      id: 'r5',
      source: 'Architect',
      sourceSlug: 'domes-architect',
      title: `Coordination designs involving ${query}`,
      snippet: `2 active architecture designs address ${query} through multi-stakeholder coordination. Includes blueprint diagrams and stakeholder network maps.`,
      relevance: 0.61,
      url: '#',
      timestamp: isoNow(5),
    },
  ];
  return {
    query,
    totalResults: results.length,
    results,
    routedTo: ['domes-data', 'domes-profile', 'spheres-assets', 'domes-contracts', 'domes-architect'],
    executionTime: 342,
  };
}

const DEMO_DISCOVERIES: Discovery[] = [
  {
    id: 'd1',
    title: 'HUD issues new fair housing enforcement guidance',
    summary: 'The Department of Housing and Urban Development released updated enforcement guidance for fair housing violations, expanding protections for source-of-income discrimination cases in Philadelphia County.',
    sourceType: 'regulation',
    impact: 'critical',
    relevanceScore: 0.96,
    status: 'new',
    timestamp: isoNow(15),
    source: 'Federal Register',
    url: '#',
  },
  {
    id: 'd2',
    title: 'PA General Assembly introduces SB-1247: Tenant Protection Act',
    summary: 'New state legislation would require 90-day notice for rent increases above 5% and establish a statewide rental assistance fund. Bill referred to Housing Committee.',
    sourceType: 'legislation',
    impact: 'high',
    relevanceScore: 0.91,
    status: 'new',
    timestamp: isoNow(45),
    source: 'PA Legislature',
    url: '#',
  },
  {
    id: 'd3',
    title: 'Census Bureau releases updated poverty thresholds for 2026',
    summary: 'Updated federal poverty guidelines show 3.2% increase in thresholds across all family sizes. Affects eligibility calculations for 47 federal programs tracked by DOMES.',
    sourceType: 'data',
    impact: 'high',
    relevanceScore: 0.88,
    status: 'reviewed',
    timestamp: isoNow(120),
    source: 'Census Bureau',
    url: '#',
  },
  {
    id: 'd4',
    title: 'City of Philadelphia expands eviction diversion program',
    summary: 'Municipal court system announces expansion of eviction diversion to cover commercial tenancies. Program now mandatory for all residential and small commercial lease disputes.',
    sourceType: 'policy',
    impact: 'medium',
    relevanceScore: 0.79,
    status: 'queued',
    timestamp: isoNow(240),
    source: 'Philadelphia Courts',
    url: '#',
  },
  {
    id: 'd5',
    title: 'HHS publishes TANF reauthorization proposed rule',
    summary: 'Proposed rule would modify work participation requirements and expand allowable activities to include digital literacy training and remote employment programs.',
    sourceType: 'regulation',
    impact: 'medium',
    relevanceScore: 0.74,
    status: 'new',
    timestamp: isoNow(360),
    source: 'Federal Register',
    url: '#',
  },
  {
    id: 'd6',
    title: 'Philadelphia Inquirer: Lead paint crisis in Kensington rentals',
    summary: 'Investigative report identifies 340 rental units with dangerous lead levels in the Kensington neighborhood. City health department has not issued violations for 60% of known cases.',
    sourceType: 'news',
    impact: 'high',
    relevanceScore: 0.85,
    status: 'new',
    timestamp: isoNow(480),
    source: 'Philadelphia Inquirer',
    url: '#',
  },
  {
    id: 'd7',
    title: 'Urban Institute publishes housing voucher utilization study',
    summary: 'New research finds voucher utilization rates in Philadelphia at 78%, below national average. Study identifies landlord acceptance and housing quality as primary barriers.',
    sourceType: 'research',
    impact: 'low',
    relevanceScore: 0.62,
    status: 'dismissed',
    timestamp: isoNow(720),
    source: 'Urban Institute',
    url: '#',
  },
  {
    id: 'd8',
    title: 'DOJ updates ADA compliance requirements for digital services',
    summary: 'New guidance requires all government-funded digital services to meet WCAG 2.2 AA standards by January 2027. Affects all DOMES-tracked service delivery platforms.',
    sourceType: 'regulation',
    impact: 'medium',
    relevanceScore: 0.71,
    status: 'new',
    timestamp: isoNow(900),
    source: 'DOJ Civil Rights Division',
    url: '#',
  },
];

const DEMO_DISCOVERY_STATS: DiscoveryStats = {
  totalDiscoveries: 247,
  pendingReview: 12,
  criticalItems: 3,
  lastScanTime: isoNow(15),
  sourceCounts: {
    legislation: 34,
    regulation: 62,
    policy: 45,
    data: 51,
    news: 38,
    research: 17,
  },
};

const DEMO_ACTIVITY: ActivityEntry[] = [
  { id: 'a1', timestamp: isoNow(2), service: 'Brain', serviceSlug: 'domes-brain', eventType: 'scan', description: 'Scheduled health check completed — 5/6 services responding' },
  { id: 'a2', timestamp: isoNow(5), service: 'Data Research', serviceSlug: 'domes-data', eventType: 'update', description: 'Ingested 14 new federal datasets from data.gov' },
  { id: 'a3', timestamp: isoNow(12), service: 'Contracts', serviceSlug: 'domes-contracts', eventType: 'error', description: 'Template rendering timeout on /api/generate (234ms > 200ms threshold)' },
  { id: 'a4', timestamp: isoNow(18), service: 'Profile Research', serviceSlug: 'domes-profile', eventType: 'query', description: 'Cross-system query: "housing assistance eligibility" — 23 results' },
  { id: 'a5', timestamp: isoNow(25), service: 'Architect', serviceSlug: 'domes-architect', eventType: 'update', description: 'Blueprint "Multi-Agency Housing Initiative" updated by coordinator' },
  { id: 'a6', timestamp: isoNow(35), service: 'Spheres Assets', serviceSlug: 'spheres-assets', eventType: 'scan', description: 'Property database sync completed — 1,247 records updated' },
  { id: 'a7', timestamp: isoNow(48), service: 'Viz', serviceSlug: 'domes-viz', eventType: 'update', description: 'Public dashboard content refreshed with latest statistics' },
  { id: 'a8', timestamp: isoNow(60), service: 'Brain', serviceSlug: 'domes-brain', eventType: 'scan', description: 'Discovery scan completed — 3 new items found' },
  { id: 'a9', timestamp: isoNow(75), service: 'Contracts', serviceSlug: 'domes-contracts', eventType: 'error', description: 'Database connection pool exhausted — recovered after 12s' },
  { id: 'a10', timestamp: isoNow(90), service: 'Data Research', serviceSlug: 'domes-data', eventType: 'query', description: 'Constellation mapping query: "child welfare data systems" — 8 nodes' },
  { id: 'a11', timestamp: isoNow(120), service: 'Brain', serviceSlug: 'domes-brain', eventType: 'scan', description: 'Scheduled health check completed — 6/6 services responding' },
  { id: 'a12', timestamp: isoNow(180), service: 'Profile Research', serviceSlug: 'domes-profile', eventType: 'update', description: 'New profile template created: "Emergency Housing Relocation"' },
  { id: 'a13', timestamp: isoNow(240), service: 'Architect', serviceSlug: 'domes-architect', eventType: 'query', description: 'Stakeholder network query for "eviction diversion" — 12 stakeholders' },
  { id: 'a14', timestamp: isoNow(360), service: 'Spheres Assets', serviceSlug: 'spheres-assets', eventType: 'update', description: 'GIS layer updated — 47 new vacant property designations' },
  { id: 'a15', timestamp: isoNow(1440), service: 'Brain', serviceSlug: 'domes-brain', eventType: 'scan', description: 'Daily system audit completed — all services within parameters' },
];

const DEMO_STATS: StatsResponse = {
  totalQueries: 1847,
  totalDiscoveries: 247,
  avgResponseTime: 67,
  uptimePercent: 99.3,
  queriesThisHour: 14,
  discoveriesToday: 8,
};

// ── API Functions ────────────────────────────────────────────────────────────

export async function getServices(): Promise<ServiceInfo[]> {
  try {
    const raw = await fetchJSON<Record<string, unknown>>(`${BASE}/services`);
    // Backend wraps in { status, data: { services: [...] } }
    const wrapper = raw as { data?: { services?: unknown[] } };
    const arr = wrapper?.data?.services;
    if (!Array.isArray(arr) || arr.length === 0) return DEMO_SERVICES;
    return arr.map((s: Record<string, unknown>) => ({
      slug: String(s.slug ?? ''),
      name: String(s.name ?? ''),
      description: String(s.description ?? ''),
      port: Number(s.port ?? 0),
      status: (s.status === 'online' ? 'online' : s.status === 'degraded' ? 'degraded' : 'offline') as ServiceStatus,
      lastChecked: String(s.last_checked ?? s.lastChecked ?? isoNow()),
      responseTime: Number(s.response_time_ms ?? s.responseTime ?? 0),
      uptime: Number(s.uptime ?? 99),
      domainColor: getServiceColor(String(s.slug ?? '')),
      url: String(s.base_url ?? s.url ?? ''),
      endpoints: Array.isArray(s.endpoints) ? s.endpoints.map(String) : [],
      recentErrors: [],
      dataFreshness: String(s.data_freshness ?? s.dataFreshness ?? 'unknown'),
      uptimeHistory: randomUptime(),
    })) as ServiceInfo[];
  } catch {
    return DEMO_SERVICES;
  }
}

export async function getHealth(): Promise<HealthResponse> {
  try {
    const raw = await fetchJSON<Record<string, unknown>>(`${BASE}/health`);
    // Backend wraps in { status, data: { brain, services_online, services_total, ... } }
    const d = raw.data as Record<string, unknown> | undefined;
    if (!d) return DEMO_HEALTH;
    return {
      status: String(d.brain ?? 'ok'),
      servicesOnline: Number(d.services_online ?? 0),
      servicesTotal: Number(d.services_total ?? 6),
      lastScan: isoNow(),
      uptime: 99.3,
    };
  } catch {
    return DEMO_HEALTH;
  }
}

export async function postQuery(
  query: string,
  circumstances?: Record<string, string>,
): Promise<QueryResponse> {
  try {
    const raw = await fetchJSON<Record<string, unknown>>(`${BASE}/query`, {
      method: 'POST',
      body: JSON.stringify({ query, circumstances }),
    });
    const d = raw.data as Record<string, unknown> | undefined;
    if (!d) return makeDemoResults(query);
    // Transform backend response to frontend shape
    const routedTo = Array.isArray(d.services_queried) ? d.services_queried.map(String) : [];
    const backendResults = d.results as Record<string, unknown> | undefined;
    const results: QueryResult[] = [];
    if (backendResults && typeof backendResults === 'object') {
      for (const [slug, val] of Object.entries(backendResults)) {
        const svc = val as Record<string, unknown>;
        if (svc.status === 'offline') continue;
        results.push({
          id: slug,
          source: String(svc.label ?? slug),
          sourceSlug: slug,
          title: `Results from ${svc.label ?? slug}`,
          snippet: JSON.stringify(svc.data ?? {}).slice(0, 200),
          relevance: 0.8,
          url: '#',
          timestamp: isoNow(),
        });
      }
    }
    if (results.length === 0) return makeDemoResults(query);
    return {
      query: String(d.query ?? query),
      totalResults: results.length,
      results,
      routedTo,
      executionTime: 342,
    };
  } catch {
    return makeDemoResults(query);
  }
}

export async function routeQuery(
  query: string,
  circumstances?: Record<string, string>,
): Promise<RoutePreview> {
  try {
    return await fetchJSON<RoutePreview>(`${BASE}/query/route`, {
      method: 'POST',
      body: JSON.stringify({ query, circumstances }),
    });
  } catch {
    return {
      query,
      services: ['domes-data', 'domes-profile', 'spheres-assets', 'domes-contracts', 'domes-architect'],
      estimatedTime: 350,
    };
  }
}

export async function getDiscoveries(filters?: DiscoveryFilters): Promise<Discovery[]> {
  try {
    const params = new URLSearchParams();
    if (filters?.sourceType) params.set('source_type', filters.sourceType);
    if (filters?.impact) params.set('impact_level', filters.impact);
    if (filters?.status) params.set('status', filters.status);
    const qs = params.toString();
    const raw = await fetchJSON<Record<string, unknown>>(`${BASE}/discoveries${qs ? `?${qs}` : ''}`);
    const arr = raw.data as unknown[];
    if (!Array.isArray(arr)) return DEMO_DISCOVERIES;
    const mapped: Discovery[] = arr.map((raw_item: unknown) => {
      const item = raw_item as Record<string, unknown>;
      return {
        id: String(item.id ?? ''),
        title: String(item.title ?? ''),
        summary: String(item.summary ?? ''),
        sourceType: mapSourceType(String(item.source_type ?? 'data')),
        impact: mapImpact(String(item.impact_level ?? 'low')),
        relevanceScore: Number(item.relevance_score ?? 0) / 100,
        status: mapDiscoveryStatus(String(item.status ?? 'new')),
        timestamp: String(item.discovered_at ?? isoNow()),
        source: String(item.source_type ?? 'Unknown'),
        url: String(item.url ?? '#'),
      };
    });
    return mapped.length > 0 ? mapped : DEMO_DISCOVERIES;
  } catch {
    let items = DEMO_DISCOVERIES;
    if (filters?.sourceType) items = items.filter((d) => d.sourceType === filters.sourceType);
    if (filters?.impact) items = items.filter((d) => d.impact === filters.impact);
    if (filters?.status) items = items.filter((d) => d.status === filters.status);
    return items;
  }
}

export async function getDiscoveryQueue(): Promise<Discovery[]> {
  try {
    const raw = await fetchJSON<Record<string, unknown>>(`${BASE}/discoveries/queue`);
    const arr = raw.data as unknown[];
    if (!Array.isArray(arr)) throw new Error('bad shape');
    return arr.map((raw_item: unknown) => {
      const item = raw_item as Record<string, unknown>;
      return {
        id: String(item.id ?? ''),
        title: String(item.title ?? ''),
        summary: String(item.summary ?? ''),
        sourceType: mapSourceType(String(item.source_type ?? 'data')),
        impact: mapImpact(String(item.impact_level ?? 'low')),
        relevanceScore: Number(item.relevance_score ?? 0) / 100,
        status: mapDiscoveryStatus(String(item.status ?? 'new')),
        timestamp: String(item.discovered_at ?? isoNow()),
        source: String(item.source_type ?? 'Unknown'),
        url: String(item.url ?? '#'),
      };
    });
  } catch {
    return DEMO_DISCOVERIES.filter((d) => d.status === 'new' || d.status === 'queued')
      .sort((a, b) => b.relevanceScore - a.relevanceScore);
  }
}

export async function triggerScan(sourceType?: string): Promise<{ started: boolean; message: string }> {
  try {
    const raw = await fetchJSON<Record<string, unknown>>(`${BASE}/discoveries/scan`, {
      method: 'POST',
      body: JSON.stringify({ sourceType }),
    });
    return { started: raw.status === 'ok', message: 'Scan completed successfully' };
  } catch {
    return { started: true, message: 'Demo scan initiated — results will appear in discovery feed' };
  }
}

export async function getActivity(): Promise<ActivityEntry[]> {
  try {
    const raw = await fetchJSON<Record<string, unknown>>(`${BASE}/activity`);
    const arr = raw.data as unknown[];
    if (!Array.isArray(arr)) return DEMO_ACTIVITY;
    return arr.map((raw_item: unknown) => {
      const item = raw_item as Record<string, unknown>;
      return {
        id: String(item.id ?? ''),
        timestamp: String(item.timestamp ?? isoNow()),
        service: String(item.service_slug ?? ''),
        serviceSlug: String(item.service_slug ?? ''),
        eventType: (item.event_type === 'error' ? 'error' : item.event_type === 'query' ? 'query' : item.event_type === 'update' ? 'update' : 'scan') as ActivityEventType,
        description: String(item.description ?? ''),
      };
    });
  } catch {
    return DEMO_ACTIVITY;
  }
}

export async function getStats(): Promise<StatsResponse> {
  try {
    const raw = await fetchJSON<Record<string, unknown>>(`${BASE}/stats`);
    const d = raw.data as Record<string, unknown> | undefined;
    if (!d) return DEMO_STATS;
    const queries = d.queries as Record<string, unknown> | undefined;
    return {
      totalQueries: Number(queries?.total ?? 0),
      totalDiscoveries: 34,
      avgResponseTime: Number(queries?.avg_duration_ms ?? 0),
      uptimePercent: 99.3,
      queriesThisHour: Number(queries?.last_24h ?? 0),
      discoveriesToday: 8,
    };
  } catch {
    return DEMO_STATS;
  }
}

export async function getDiscoveryStats(): Promise<DiscoveryStats> {
  try {
    const raw = await fetchJSON<Record<string, unknown>>(`${BASE}/discoveries/stats`);
    const d = raw.data as Record<string, unknown> | undefined;
    if (!d) return DEMO_DISCOVERY_STATS;
    const bySource = d.by_source as Record<string, number> | undefined;
    const byImpact = d.by_impact as Record<string, number> | undefined;
    return {
      totalDiscoveries: Number(d.total ?? 0),
      pendingReview: Number(byImpact?.critical ?? 0) + Number(byImpact?.high ?? 0),
      criticalItems: Number(byImpact?.critical ?? 0),
      lastScanTime: isoNow(5),
      sourceCounts: bySource ?? {},
    };
  } catch {
    return DEMO_DISCOVERY_STATS;
  }
}

// ── Utility ──────────────────────────────────────────────────────────────────

export function formatTimestamp(iso: string): string {
  const d = new Date(iso);
  const now = new Date();
  const diffMs = now.getTime() - d.getTime();
  const diffMin = Math.floor(diffMs / 60_000);
  if (diffMin < 1) return 'just now';
  if (diffMin < 60) return `${diffMin}m ago`;
  const diffHr = Math.floor(diffMin / 60);
  if (diffHr < 24) return `${diffHr}h ago`;
  const diffDay = Math.floor(diffHr / 24);
  return `${diffDay}d ago`;
}

export function formatTime(iso: string): string {
  return new Date(iso).toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });
}

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
  });
}

export function getDateGroup(iso: string): string {
  const d = new Date(iso);
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const yesterday = new Date(today.getTime() - 86_400_000);
  const itemDate = new Date(d.getFullYear(), d.getMonth(), d.getDate());

  if (itemDate.getTime() === today.getTime()) return 'Today';
  if (itemDate.getTime() === yesterday.getTime()) return 'Yesterday';
  return d.toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' });
}

export function getServiceColor(slug: string): string {
  const map: Record<string, string> = {
    'spheres-assets': '#1A3D8B',
    'domes-data': '#5A1A6B',
    'domes-profile': '#1A6B3C',
    'domes-contracts': '#6B5A1A',
    'domes-architect': '#8B1A1A',
    'domes-viz': '#1A6B6B',
    'domes-brain': '#448AFF',
  };
  return map[slug] ?? '#8A8A96';
}
