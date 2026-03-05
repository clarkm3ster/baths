/**
 * DOMES API client — fetch wrapper for all backend endpoints.
 *
 * All functions return typed promises. Errors are thrown with
 * a descriptive message so callers can catch and display.
 */

import type {
  Profile,
  DomeData,
  CostBenchmark,
  CostCalculation,
  ROIResult,
  ScaleResult,
  AvoidableEvent,
  Circumstance,
  CompareResult,
} from '../types';

// ---------------------------------------------------------------------------
// Base fetch helper
// ---------------------------------------------------------------------------

const BASE = '/api';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const body = await res.text().catch(() => '');
    throw new Error(`API ${res.status}: ${body || res.statusText}`);
  }
  return res.json();
}

function get<T>(path: string): Promise<T> {
  return request<T>(path);
}

function post<T>(path: string, body: unknown): Promise<T> {
  return request<T>(path, {
    method: 'POST',
    body: JSON.stringify(body),
  });
}

function put<T>(path: string, body: unknown): Promise<T> {
  return request<T>(path, {
    method: 'PUT',
    body: JSON.stringify(body),
  });
}

// ---------------------------------------------------------------------------
// Profile routes
// ---------------------------------------------------------------------------

export function generateProfile(
  circumstances: Record<string, boolean | string>,
  name?: string
): Promise<Profile> {
  return post('/profiles/generate', { circumstances, name });
}

export function listProfiles(params?: {
  is_sample?: boolean;
  limit?: number;
  offset?: number;
}): Promise<Profile[]> {
  const qs = new URLSearchParams();
  if (params?.is_sample !== undefined) qs.set('is_sample', String(params.is_sample));
  if (params?.limit !== undefined) qs.set('limit', String(params.limit));
  if (params?.offset !== undefined) qs.set('offset', String(params.offset));
  const q = qs.toString();
  return get<{ items: Profile[] }>(`/profiles${q ? `?${q}` : ''}`).then(r => r.items);
}

export function getProfile(id: string): Promise<Profile> {
  return get(`/profiles/${id}`);
}

export function getDomeData(id: string): Promise<DomeData> {
  return get<Record<string, unknown>>(`/profiles/${id}/dome`).then(raw => {
    const rawDomains = raw.domains as Array<Record<string, unknown>>;
    const domains = rawDomains.map(d => {
      const rawSystems = (d.systems ?? []) as Array<Record<string, unknown>>;
      const domainKey = d.domain as string;
      const systems = rawSystems.map(s => ({
        id: s.id as string,
        name: (s.label ?? s.name ?? s.id) as string,
        acronym: ((s.id as string) ?? '').toUpperCase(),
        domain: domainKey,
        annual_cost: s.annual_cost as number,
        coordinated_cost: Math.round((s.annual_cost as number) * (1 - ((s.coord_savings_pct as number) ?? 0.3))),
      }));
      const rawProvisions = (d.provisions ?? d.top_provisions ?? []) as Array<Record<string, unknown>>;
      const rawGaps = (d.gaps ?? []) as Array<Record<string, unknown>>;
      const rawBridges = (d.bridges ?? []) as Array<Record<string, unknown>>;
      return {
        domain: domainKey,
        label: d.label as string,
        color: d.color as string,
        systems,
        provisions_count: rawProvisions.length,
        gaps_count: rawGaps.length,
        annual_cost: d.annual_cost as number,
        coordinated_cost: d.coordinated_cost as number,
        savings: d.savings as number,
        top_provisions: rawProvisions.slice(0, 6).map(p => ({
          citation: (p.id ?? p.citation ?? '') as string,
          title: (p.title ?? '') as string,
          type: (p.type ?? '') as string,
        })),
        gaps: rawGaps.map((g, i) => ({
          id: i,
          system_a: (g.label ?? g.system_a ?? '') as string,
          system_b: '',
          barrier_type: (g.severity ?? g.barrier_type ?? '') as string,
          severity: (g.severity ?? 'medium') as string,
          consent_closable: false,
        })),
        bridges: rawBridges.map((b, i) => ({
          id: i,
          title: (b.label ?? b.title ?? '') as string,
          bridge_type: (b.type ?? b.bridge_type ?? '') as string,
          priority_score: b.impact === 'high' ? 9 : b.impact === 'medium' ? 6 : 3,
          estimated_cost: (b.estimated_cost ?? '') as string,
        })),
      };
    });
    return {
      profile: raw.profile as DomeData['profile'],
      domains,
      totals: raw.totals as DomeData['totals'],
      connections: (raw.connections ?? []) as DomeData['connections'],
      consent_pathways: raw.consent_pathways as DomeData['consent_pathways'],
    } as DomeData;
  });
}

export function compareProfiles(profileIds: string[]): Promise<CompareResult> {
  return post<Record<string, unknown>>('/profiles/compare', { profile_ids: profileIds }).then(r => {
    const p1 = r.profile_1 as Profile;
    const p2 = r.profile_2 as Profile;
    const diff = r.differences as Record<string, unknown>;
    return {
      profiles: [p1, p2],
      deltas: {
        cost_delta: (diff.cost_difference as number) ?? 0,
        savings_delta: (diff.savings_difference as number) ?? 0,
        systems_delta: ((diff.systems_only_in_1 as string[])?.length ?? 0) - ((diff.systems_only_in_2 as string[])?.length ?? 0),
        gaps_delta: 0,
        circumstances_diff: Object.keys({
          ...((p1.circumstances ?? {}) as Record<string, unknown>),
          ...((p2.circumstances ?? {}) as Record<string, unknown>),
        }).filter(k => {
          const c1 = (p1.circumstances as Record<string, unknown>)?.[k];
          const c2 = (p2.circumstances as Record<string, unknown>)?.[k];
          return c1 !== c2;
        }),
      },
    };
  });
}

export function updateProfile(
  id: string,
  circumstances: Record<string, boolean | string>
): Promise<Profile> {
  return put(`/profiles/${id}`, { circumstances });
}

export function getProfileVersions(id: string): Promise<Profile[]> {
  return get(`/profiles/${id}/versions`);
}

export function getCircumstances(): Promise<Circumstance[]> {
  return get('/profiles/circumstances');
}

// ---------------------------------------------------------------------------
// Cost routes
// ---------------------------------------------------------------------------

export function calculateCost(
  circumstances: Record<string, boolean | string>,
  systems: string[]
): Promise<CostCalculation> {
  return post('/cost/calculate', { circumstances, systems });
}

export function getCostBenchmarks(): Promise<CostBenchmark[]> {
  return get('/cost/benchmarks');
}

export function getSystemBenchmark(systemId: string): Promise<CostBenchmark> {
  return get(`/cost/benchmarks/${systemId}`);
}

export function calculateROI(params: {
  coordination_cost: number;
  annual_savings: number;
  years: number;
}): Promise<ROIResult> {
  return post('/cost/roi', params);
}

export function calculateScale(params: {
  per_person_savings: number;
  populations: Record<string, number>;
}): Promise<ScaleResult> {
  return post('/cost/scale', params);
}

export function getAvoidableEvents(): Promise<AvoidableEvent[]> {
  return get<{ events: AvoidableEvent[] }>('/cost/avoidable-events').then(r => r.events);
}
