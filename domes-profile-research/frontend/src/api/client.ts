import type { CompositeProfile, Circumstances, CostResult, DocumentedCase, SystemProfile, CostBenchmark } from "../types";

const BASE = "/api";

async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export function generateProfile(circumstances: Circumstances): Promise<CompositeProfile> {
  return fetchJSON(`${BASE}/profiles/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ circumstances }),
  });
}

export function calculateCosts(systemIds: string[]): Promise<CostResult> {
  return fetchJSON(`${BASE}/cost/calculate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ system_ids: systemIds }),
  });
}

export function getCases(): Promise<DocumentedCase[]> {
  return fetchJSON(`${BASE}/cases`);
}

export function getCase(id: string): Promise<DocumentedCase> {
  return fetchJSON(`${BASE}/cases/${id}`);
}

export function searchCases(tags: string[], systemIds: string[]): Promise<DocumentedCase[]> {
  return fetchJSON(`${BASE}/cases/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tags, system_ids: systemIds }),
  });
}

export function getSystems(): Promise<SystemProfile[]> {
  return fetchJSON(`${BASE}/systems`);
}

export function getBenchmarks(): Promise<CostBenchmark[]> {
  return fetchJSON(`${BASE}/cost/benchmarks`);
}
