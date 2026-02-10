import type { ConstellationResponse, Profile, System, Gap } from "../types";

const BASE = "/api";

async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export function getConstellation(
  profile: Profile
): Promise<ConstellationResponse> {
  return fetchJSON(`${BASE}/constellation`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });
}

export function getSystems(): Promise<System[]> {
  return fetchJSON(`${BASE}/systems`);
}

export function getSystem(id: string): Promise<System> {
  return fetchJSON(`${BASE}/systems/${id}`);
}

export function getGaps(): Promise<Gap[]> {
  return fetchJSON(`${BASE}/gaps`);
}

export function getGap(id: number): Promise<Gap & { system_a: System; system_b: System }> {
  return fetchJSON(`${BASE}/gaps/${id}`);
}

export function getConsentPathways(): Promise<Gap[]> {
  return fetchJSON(`${BASE}/consent-pathways`);
}
