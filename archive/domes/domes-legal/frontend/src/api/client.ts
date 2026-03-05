import type { Provision, TaxonomyTag, TaxonomyStats, GraphData, GraphStats, DomainCount, SearchRequest } from "../types";

const BASE = "/api";

async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

// Provisions
export function getProvisions(params?: { domain?: string; provision_type?: string; q?: string }): Promise<{ total: number; items: Provision[] }> {
  const qs = new URLSearchParams();
  if (params?.domain) qs.set("domain", params.domain);
  if (params?.provision_type) qs.set("provision_type", params.provision_type);
  if (params?.q) qs.set("q", params.q);
  return fetchJSON(`${BASE}/provisions?${qs}`);
}

export function getProvision(id: number): Promise<Provision> {
  return fetchJSON(`${BASE}/provisions/${id}`);
}

export function getDomains(): Promise<DomainCount[]> {
  return fetchJSON(`${BASE}/provisions/domains`);
}

export function getHierarchy(): Promise<Record<string, unknown>> {
  return fetchJSON(`${BASE}/provisions/hierarchy`);
}

// Search & Match
export function searchProvisions(req: SearchRequest): Promise<{ total: number; items: Provision[] }> {
  return fetchJSON(`${BASE}/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
}

export function matchCircumstances(circumstances: Record<string, string[]>): Promise<{ total: number; items: Provision[] }> {
  return fetchJSON(`${BASE}/match`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ circumstances }),
  });
}

// Taxonomy
export function getTags(category?: string): Promise<TaxonomyTag[]> {
  const qs = category ? `?category=${category}` : "";
  return fetchJSON(`${BASE}/taxonomy/tags${qs}`);
}

export function getTaxonomyStats(): Promise<TaxonomyStats> {
  return fetchJSON(`${BASE}/taxonomy/stats`);
}

// Graph
export function getProvisionGraph(id: number, depth = 2): Promise<GraphData> {
  return fetchJSON(`${BASE}/graph/provision/${id}?depth=${depth}`);
}

export function getFullGraph(domain?: string): Promise<GraphData> {
  const qs = domain ? `?domain=${domain}` : "";
  return fetchJSON(`${BASE}/graph/full${qs}`);
}

export function getGraphStats(): Promise<GraphStats> {
  return fetchJSON(`${BASE}/graph/stats`);
}

export function buildRelationships(): Promise<{ added: number }> {
  return fetchJSON(`${BASE}/graph/build`, { method: "POST" });
}

// Ingest / Monitor
export interface RecentChange {
  date: string;
  source: string;
  citation: string;
  title: string;
  change_type: string;
  summary: string;
  affected_domains: string[];
  affected_provisions: number;
}

export interface SourceStatus {
  last_checked: string;
  status: string;
}

export interface RecentChangesResponse {
  week_summary: string;
  changes: RecentChange[];
  source_status: Record<string, SourceStatus>;
}

export function getRecentChanges(): Promise<RecentChangesResponse> {
  return fetchJSON(`${BASE}/ingest/recent-changes`);
}
