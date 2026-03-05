/** SPHERE/OS API client. */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8100";

async function fetchApi<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new Error(`API ${res.status}: ${body}`);
  }
  return res.json();
}

// ── Land ──────────────────────────────────────────────────────────

import type {
  ParcelCollection,
  ViabilityBreakdown,
  Sphere,
  MaterialState,
  DriverInfo,
  Booking,
  TimeSlot,
  ProductionProposal,
  SafetyEvent,
} from "./types";

export async function getParcels(params?: {
  min_viability?: number;
  status?: string;
  limit?: number;
}): Promise<ParcelCollection> {
  const qs = new URLSearchParams();
  if (params?.min_viability) qs.set("min_viability", String(params.min_viability));
  if (params?.status) qs.set("status", String(params.status));
  if (params?.limit) qs.set("limit", String(params.limit));
  const q = qs.toString();
  return fetchApi(`/api/land/parcels${q ? `?${q}` : ""}`);
}

export async function getParcelViability(id: string): Promise<ViabilityBreakdown> {
  return fetchApi(`/api/land/parcels/${id}/viability`);
}

// ── Spheres ───────────────────────────────────────────────────────

export async function getSpheres(): Promise<Sphere[]> {
  return fetchApi("/api/spheres");
}

export async function getSphere(id: string): Promise<Sphere> {
  return fetchApi(`/api/spheres/${id}`);
}

// ── Materials ─────────────────────────────────────────────────────

export async function getMaterialState(sphereId: string): Promise<MaterialState> {
  return fetchApi(`/api/spheres/${sphereId}/material-state`);
}

export async function getDrivers(): Promise<DriverInfo[]> {
  return fetchApi("/api/materials/drivers");
}

export async function sendMaterialCommand(
  sphereId: string,
  config: Record<string, unknown>,
): Promise<unknown> {
  return fetchApi(`/api/spheres/${sphereId}/material-command`, {
    method: "POST",
    body: JSON.stringify({ target: config }),
  });
}

export async function emergencyReset(sphereId: string): Promise<void> {
  await fetchApi(`/api/spheres/${sphereId}/emergency-reset`, { method: "POST" });
}

/** Create a WebSocket connection for real-time material state streaming. */
export function createMaterialStream(sphereId: string): WebSocket {
  const wsBase = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:8100")
    .replace("http", "ws");
  return new WebSocket(`${wsBase}/api/spheres/${sphereId}/material-stream`);
}

// ── Bookings ──────────────────────────────────────────────────────

export async function getSchedule(sphereId: string): Promise<Booking[]> {
  return fetchApi(`/api/spheres/${sphereId}/schedule`);
}

export async function getAvailability(
  sphereId: string,
  date: string,
): Promise<TimeSlot[]> {
  return fetchApi(`/api/spheres/${sphereId}/availability?date=${date}`);
}

export async function createBooking(
  sphereId: string,
  data: { start_time: string; end_time: string; production_id?: string },
): Promise<Booking> {
  return fetchApi(`/api/spheres/${sphereId}/bookings`, {
    method: "POST",
    body: JSON.stringify(data),
  });
}

// ── Productions ───────────────────────────────────────────────────

export async function generateProposal(data: {
  parcel_id?: string;
  area_sqft: number;
  zoning?: string;
}): Promise<ProductionProposal> {
  return fetchApi("/api/productions/generate", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getProposal(id: string): Promise<ProductionProposal> {
  return fetchApi(`/api/productions/${id}`);
}

// ── Safety ────────────────────────────────────────────────────────

export async function getSafetyEvents(sphereId?: string): Promise<SafetyEvent[]> {
  const path = sphereId
    ? `/api/safety/events?sphere_id=${sphereId}`
    : "/api/safety/events";
  return fetchApi(path);
}

export async function acknowledgeSafetyEvent(eventId: string): Promise<void> {
  await fetchApi(`/api/safety/acknowledge/${eventId}`, { method: "POST" });
}
