/**
 * Typed API client for the SPHERE/OS FastAPI backend.
 *
 * All requests go through the Next.js rewrite proxy:
 *   /api/* → http://localhost:8100/api/*
 */
import type {
  ParcelRecord,
  ParcelCluster,
  DriverInfo,
  DriverResponse,
  SafetyEvent,
  SafetyReport,
  ProductionProposal,
  MaterialScriptResponse,
  Booking,
  TimeSlice,
} from "@/types";

const BASE = "/api";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`API ${res.status}: ${detail}`);
  }
  return res.json();
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`API ${res.status}: ${detail}`);
  }
  return res.json();
}

async function put<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`API ${res.status}: ${detail}`);
  }
  return res.json();
}

// ── Land Intelligence ───────────────────────────────────────────

export function listParcels(params?: {
  ownership_type?: string;
  min_area?: number;
  min_viability?: number;
  status?: string;
  limit?: number;
}) {
  const qs = new URLSearchParams();
  if (params?.ownership_type) qs.set("ownership_type", params.ownership_type);
  if (params?.min_area) qs.set("min_area", String(params.min_area));
  if (params?.min_viability)
    qs.set("min_viability", String(params.min_viability));
  if (params?.status) qs.set("status", params.status);
  if (params?.limit) qs.set("limit", String(params.limit));
  const q = qs.toString();
  return get<ParcelRecord[]>(`/land/parcels${q ? `?${q}` : ""}`);
}

export function getParcel(parcelId: string) {
  return get<ParcelRecord>(`/land/parcels/${parcelId}`);
}

export function getParcelViability(parcelId: string) {
  return get<{
    parcel_id: string;
    viability_score: number;
    factors: Record<string, number>;
  }>(`/land/parcels/${parcelId}/viability`);
}

export function listClusters() {
  return get<ParcelCluster[]>("/land/clusters");
}

export function activateParcel(parcelId: string) {
  return post<{ sphere_id: string; status: string }>(
    `/land/parcels/${parcelId}/activate`,
    {}
  );
}

export function ingestPhillyVacant() {
  return post<{ ingested: number }>("/land/ingest/philly-vacant", {});
}

// ── Material Drivers ────────────────────────────────────────────

export function listDrivers() {
  return get<DriverInfo[]>("/materials/drivers");
}

export function getMaterialState(sphereId: string) {
  return get<Record<string, unknown>>(`/spheres/${sphereId}/material-state`);
}

export function sendMaterialCommand(
  sphereId: string,
  systemType: string,
  config: Record<string, unknown>
) {
  return post<DriverResponse>(`/spheres/${sphereId}/material-command`, {
    system_type: systemType,
    config,
  });
}

export function setMaterialConfig(
  sphereId: string,
  config: Record<string, unknown>
) {
  return post<Record<string, DriverResponse>>(
    `/spheres/${sphereId}/material-config`,
    config
  );
}

export function emergencyReset(sphereId: string) {
  return post<{ status: string }>(`/spheres/${sphereId}/emergency-reset`, {});
}

/** WebSocket for real-time material state streaming. */
export function createMaterialStream(sphereId: string): WebSocket {
  const wsBase = (
    typeof window !== "undefined" ? window.location.origin : "http://localhost:8100"
  ).replace("http", "ws");
  return new WebSocket(`${wsBase}/api/spheres/${sphereId}/material-stream`);
}

// ── Scheduling ──────────────────────────────────────────────────

export function getSphereSchedule(
  sphereId: string,
  params?: { start?: string; end?: string }
) {
  const qs = new URLSearchParams();
  if (params?.start) qs.set("start", params.start);
  if (params?.end) qs.set("end", params.end);
  const q = qs.toString();
  return get<TimeSlice[]>(`/spheres/${sphereId}/schedule${q ? `?${q}` : ""}`);
}

export function createBooking(
  sphereId: string,
  booking: {
    user_id: string;
    start_time: string;
    end_time: string;
    mode: string;
    material_request: Record<string, unknown>;
  }
) {
  return post<Booking>(`/spheres/${sphereId}/bookings`, booking);
}

export function getSphereAvailability(
  sphereId: string,
  params?: { date?: string; duration_hours?: number }
) {
  const qs = new URLSearchParams();
  if (params?.date) qs.set("date", params.date);
  if (params?.duration_hours)
    qs.set("duration_hours", String(params.duration_hours));
  const q = qs.toString();
  return get<{ available_slots: unknown[] }>(
    `/spheres/${sphereId}/availability${q ? `?${q}` : ""}`
  );
}

export function updateBookingMaterialConfig(
  bookingId: string,
  config: Record<string, unknown>
) {
  return put<Booking>(`/bookings/${bookingId}/material-config`, config);
}

export function getTransitionTime(sphereId: string) {
  return get<{ transition_time_s: number; details: Record<string, number> }>(
    `/spheres/${sphereId}/transition-time`
  );
}

// ── Safety Monitoring ───────────────────────────────────────────

export function listSafetyEvents(params?: {
  sphere_id?: string;
  severity?: string;
  resolved?: boolean;
}) {
  const qs = new URLSearchParams();
  if (params?.sphere_id) qs.set("sphere_id", params.sphere_id);
  if (params?.severity) qs.set("severity", params.severity);
  if (params?.resolved !== undefined)
    qs.set("resolved", String(params.resolved));
  const q = qs.toString();
  return get<SafetyEvent[]>(`/safety/events${q ? `?${q}` : ""}`);
}

export function getSafetyReport(sphereId: string) {
  return get<SafetyReport>(`/safety/report/${sphereId}`);
}

export function acknowledgeSafetyEvent(eventId: string) {
  return post<SafetyEvent>(`/safety/acknowledge/${eventId}`, {});
}

export function getSafetyThresholds() {
  return get<Record<string, Record<string, number>>>("/safety/thresholds");
}

export function updateSafetyThresholds(
  thresholds: Record<string, Record<string, number>>
) {
  return put<Record<string, Record<string, number>>>(
    "/safety/thresholds",
    thresholds
  );
}

// ── Productions ─────────────────────────────────────────────────

export function generateProduction(params: {
  parcel_id: string;
  creative_brief?: string;
  tier_filter?: number[];
  format?: string;
}) {
  return post<ProductionProposal>("/productions/generate", params);
}

export function getProduction(proposalId: string) {
  return get<ProductionProposal>(`/productions/${proposalId}`);
}

export function getProductionMaterialScript(proposalId: string) {
  return get<MaterialScriptResponse>(
    `/productions/${proposalId}/material-script`
  );
}

export function iterateProduction(proposalId: string, feedback: string) {
  return post<ProductionProposal>(`/productions/${proposalId}/iterate`, {
    feedback,
  });
}

// ── Health ──────────────────────────────────────────────────────

export function healthCheck() {
  return get<{ status: string }>("/health");
}

// ── Compat aliases (old function names) ─────────────────────────

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Any = any;

/** @deprecated Use listParcels */
export function getParcels(params?: Parameters<typeof listParcels>[0]): Promise<Any> {
  return listParcels(params);
}
/** @deprecated Use listSafetyEvents */
export function getSafetyEvents(sphereId?: string): Promise<Any> {
  return listSafetyEvents(sphereId ? { sphere_id: sphereId } : undefined);
}
/** @deprecated Use listDrivers */
export const getDrivers = listDrivers;
/** @deprecated Use getSphereSchedule */
export function getSchedule(sphereId: string): Promise<Any> {
  return getSphereSchedule(sphereId);
}
/** @deprecated Use getSphereAvailability */
export function getAvailability(sphereId: string, date: string): Promise<Any> {
  return getSphereAvailability(sphereId, { date });
}
/** @deprecated Use generateProduction */
export const generateProposal = generateProduction;
/** @deprecated Use getProduction */
export const getProposal = getProduction;

export function getSpheres(): Promise<Any> {
  return get("/spheres");
}

export function getSphere(id: string): Promise<Any> {
  return get(`/spheres/${id}`);
}

/** @deprecated Compat createBooking with fewer required fields */
export function createBookingCompat(
  sphereId: string,
  data: { start_time: string; end_time: string; production_id?: string }
): Promise<Any> {
  return post(`/spheres/${sphereId}/bookings`, {
    user_id: "demo-user",
    mode: "production",
    material_request: {},
    ...data,
  });
}
