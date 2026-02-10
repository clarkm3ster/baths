import type { PersonProfile, Provision, MatchApiResponse, MatchResult, DomainCount, ExplanationResult } from '../types';

const API_BASE = '';

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`);
  }

  return response.json() as Promise<T>;
}

export async function matchProvisions(profile: PersonProfile): Promise<MatchResult> {
  const apiResponse = await request<MatchApiResponse>('/api/match', {
    method: 'POST',
    body: JSON.stringify(profile),
  });

  return {
    profile,
    matches: apiResponse.matches,
    gaps: apiResponse.gaps,
    cross_references: apiResponse.cross_references,
    total_matched: apiResponse.matches.length,
  };
}

export async function getProvisions(filters?: {
  domain?: string;
  provision_type?: string;
  search?: string;
}): Promise<Provision[]> {
  const params = new URLSearchParams();
  if (filters?.domain) params.set('domain', filters.domain);
  if (filters?.provision_type) params.set('provision_type', filters.provision_type);
  if (filters?.search) params.set('search', filters.search);

  const query = params.toString();
  return request<Provision[]>(`/api/provisions${query ? `?${query}` : ''}`);
}

export async function getDomains(): Promise<DomainCount[]> {
  return request<DomainCount[]>('/api/domains');
}

export async function explainProvision(
  provisionId: number,
  personProfile: Record<string, unknown>,
): Promise<ExplanationResult> {
  return request<ExplanationResult>('/api/explain', {
    method: 'POST',
    body: JSON.stringify({
      provision_id: provisionId,
      person_profile: personProfile,
    }),
  });
}
