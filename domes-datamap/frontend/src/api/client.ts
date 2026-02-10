import type {
  System,
  Connection,
  Gap,
  Bridge,
  PersonMapResult,
  MatrixData,
  Stats,
} from "../types";

const BASE = "/api";

async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init);
  if (!res.ok) {
    const text = await res.text().catch(() => "Unknown error");
    throw new Error(`API ${res.status}: ${text}`);
  }
  return res.json();
}

// Systems
export function getSystems(params?: {
  domain?: string;
  data_standard?: string;
  search?: string;
}): Promise<System[]> {
  const qs = new URLSearchParams();
  if (params?.domain) qs.set("domain", params.domain);
  if (params?.data_standard) qs.set("data_standard", params.data_standard);
  if (params?.search) qs.set("search", params.search);
  const q = qs.toString();
  return fetchJson(`${BASE}/systems${q ? `?${q}` : ""}`);
}

export function getSystem(
  systemId: string
): Promise<System & { connections: Connection[]; gaps: Gap[] }> {
  return fetchJson(`${BASE}/systems/${systemId}`);
}

// Connections
export function getConnections(): Promise<Connection[]> {
  return fetchJson(`${BASE}/connections`);
}

export function getConnectionMatrix(): Promise<MatrixData> {
  return fetchJson(`${BASE}/connections/matrix`);
}

// Gaps
export function getGaps(params?: {
  barrier_type?: string;
  severity?: string;
  consent_closable?: string;
  domain?: string;
}): Promise<Gap[]> {
  const qs = new URLSearchParams();
  if (params?.barrier_type) qs.set("barrier_type", params.barrier_type);
  if (params?.severity) qs.set("severity", params.severity);
  if (params?.consent_closable)
    qs.set("consent_closable", params.consent_closable);
  if (params?.domain) qs.set("domain", params.domain);
  const q = qs.toString();
  return fetchJson(`${BASE}/gaps${q ? `?${q}` : ""}`);
}

export function getGap(gapId: number): Promise<Gap> {
  return fetchJson(`${BASE}/gaps/${gapId}`);
}

// Person Map
export function postPersonMap(
  circumstances: string[]
): Promise<PersonMapResult> {
  return fetchJson(`${BASE}/person-map`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ circumstances }),
  });
}

// Bridges
export function getBridges(params?: {
  bridge_type?: string;
  status?: string;
  min_priority?: number;
}): Promise<Bridge[]> {
  const qs = new URLSearchParams();
  if (params?.bridge_type) qs.set("bridge_type", params.bridge_type);
  if (params?.status) qs.set("status", params.status);
  if (params?.min_priority)
    qs.set("min_priority", String(params.min_priority));
  const q = qs.toString();
  return fetchJson(`${BASE}/bridges${q ? `?${q}` : ""}`);
}

export function getBridgesForGap(gapId: number): Promise<Bridge[]> {
  return fetchJson(`${BASE}/bridges/${gapId}`);
}

export function getBridgesPriority(params?: {
  limit?: number;
  offset?: number;
}): Promise<Bridge[]> {
  const qs = new URLSearchParams();
  if (params?.limit) qs.set("limit", String(params.limit));
  if (params?.offset) qs.set("offset", String(params.offset));
  const q = qs.toString();
  return fetchJson(`${BASE}/bridges/priority${q ? `?${q}` : ""}`);
}

export function postConsentPathway(
  circumstances: string[]
): Promise<{ consent_closable_gaps: Gap[]; consent_bridges: Bridge[] }> {
  return fetchJson(`${BASE}/bridges/consent-pathway`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ circumstances }),
  });
}

// Stats
export function getStats(): Promise<Stats> {
  return fetchJson(`${BASE}/stats`);
}
