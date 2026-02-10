import type {
  ParcelListResponse,
  ParcelFull,
  GeoJSONCollection,
  Stats,
  StaticValue,
  ActivationValue,
  LeveragedValue,
  ParcelSummary,
} from "../types";

async function request<T>(path: string): Promise<T> {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json() as Promise<T>;
}

export async function fetchParcels(params: Record<string, string | number | boolean | undefined> = {}): Promise<ParcelListResponse> {
  const qs = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== "") qs.set(k, String(v));
  }
  const q = qs.toString();
  return request<ParcelListResponse>(`/api/parcels${q ? `?${q}` : ""}`);
}

export async function fetchParcelsGeoJSON(params: Record<string, string | number | boolean | undefined> = {}): Promise<GeoJSONCollection> {
  const qs = new URLSearchParams();
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== "") qs.set(k, String(v));
  }
  const q = qs.toString();
  return request<GeoJSONCollection>(`/api/parcels/geojson${q ? `?${q}` : ""}`);
}

export async function fetchParcel(id: string): Promise<ParcelFull> {
  return request<ParcelFull>(`/api/parcels/${id}`);
}

export async function fetchNearby(lat: number, lng: number, radiusFt = 1000): Promise<(ParcelSummary & { distance_ft: number })[]> {
  return request(`/api/parcels/nearby?lat=${lat}&lng=${lng}&radius_ft=${radiusFt}`);
}

export async function fetchStats(): Promise<Stats> {
  return request<Stats>("/api/stats");
}

export async function fetchStaticValue(): Promise<StaticValue> {
  return request<StaticValue>("/api/value/static");
}

export async function fetchActivationValue(): Promise<ActivationValue> {
  return request<ActivationValue>("/api/value/activation");
}

export async function fetchLeveragedValue(): Promise<LeveragedValue> {
  return request<LeveragedValue>("/api/value/leveraged");
}
