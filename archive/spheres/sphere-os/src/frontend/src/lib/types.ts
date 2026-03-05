/** SPHERE/OS frontend type definitions. */

// ── Land ──────────────────────────────────────────────────────────

export interface ParcelFeature {
  type: "Feature";
  id: string;
  geometry: GeoJSON.Geometry;
  properties: {
    address: string;
    area_sqft: number;
    zoning: string | null;
    viability_score: number | null;
    cluster_id: string | null;
    status: "vacant" | "activated" | "decommissioned";
  };
}

export interface ParcelCollection {
  type: "FeatureCollection";
  features: ParcelFeature[];
}

export interface ViabilityBreakdown {
  overall: number;
  lot_size: number;
  street_visibility: number;
  pedestrian_traffic: number;
  environmental_risk: number;
  zoning_compatibility: number;
  population_density: number;
  cluster_potential: number;
}

// ── Sphere ────────────────────────────────────────────────────────

export type SphereStatus = "provisioning" | "idle" | "active" | "transitioning" | "maintenance" | "decommissioned";
export type SphereMode = "production" | "rehearsal" | "open_play" | "maintenance" | "dark";

export interface Sphere {
  id: string;
  parcel_id: string;
  name: string;
  status: SphereStatus;
  mode: SphereMode;
  material_inventory: string[];
  created_at: string;
}

// ── Material State ────────────────────────────────────────────────

export interface MaterialState {
  [system: string]: Record<string, unknown>;
}

export interface DriverInfo {
  system_type: string;
  trl: number;
  status: string;
  capabilities: Record<string, unknown>;
}

// ── Booking ───────────────────────────────────────────────────────

export type BookingStatus = "requested" | "confirmed" | "active" | "completed" | "cancelled";

export interface Booking {
  id: string;
  sphere_id: string;
  production_id: string | null;
  start_time: string;
  end_time: string;
  status: BookingStatus;
  material_config: Record<string, unknown>;
}

export interface TimeSlot {
  start: string;
  end: string;
  available: boolean;
}

// ── Production ────────────────────────────────────────────────────

export interface MaterialCue {
  beat_id: string;
  timestamp_range: [number, number] | "persistent";
  material_system: string;
  target_property: string;
  value_curve: number[];
  narrative_function: string;
}

export interface ProductionProposal {
  id: string;
  title: string;
  logline: string;
  genre: string;
  format: string;
  narrative_concept: string;
  material_script: MaterialCue[];
  min_area_sqft: number;
  estimated_budget_low_usd: number;
  estimated_budget_high_usd: number;
  production_timeline_weeks: number;
  legacy_modes: string[];
}

// ── Safety ────────────────────────────────────────────────────────

export type Severity = "warning" | "critical" | "emergency";

export interface SafetyEvent {
  id: string;
  sphere_id: string;
  severity: Severity;
  system_type: string;
  parameter: string;
  value: number;
  threshold: number;
  message: string;
  created_at: string;
  acknowledged: boolean;
}
