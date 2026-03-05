// Generated from sphere-os/src/scheduling/models.py

export type SphereStatus =
  | "planning"
  | "construction"
  | "active_production"
  | "legacy_soundstage"
  | "public_access"
  | "dormant";

export type SphereMode = "production" | "public" | "community" | "maintenance";

export type TimeSliceMode =
  | "production"
  | "public"
  | "community"
  | "maintenance"
  | "transition";

export type BookingStatus =
  | "pending"
  | "confirmed"
  | "active"
  | "completed"
  | "cancelled";

export interface Sphere {
  id: string;
  parcel_id: string | null;
  name: string;
  status: SphereStatus;
  material_inventory: string[];
  current_mode: SphereMode;
  base_state: Record<string, unknown>;
  created_at: string;
  updated_at: string;
  time_slices?: TimeSlice[];
}

export interface TimeSlice {
  id: string;
  sphere_id: string;
  start_time: string;
  end_time: string;
  mode: TimeSliceMode;
  material_config: Record<string, unknown>;
  transition_buffer_minutes: number;
  booking_id: string | null;
  created_at: string;
}

export interface Booking {
  id: string;
  user_id: string;
  sphere_id: string;
  material_request: Record<string, unknown>;
  material_actual: Record<string, unknown> | null;
  pricing_usd: number;
  status: BookingStatus;
  created_at: string;
  updated_at: string;
  time_slices?: TimeSlice[];
}

// ── Environment Reading (telemetry) ─────────────────────────────

export interface EnvironmentReading {
  timestamp: string;
  temperature_f: number;
  humidity_pct: number;
  reverb_s: number;
  vibration_mm_s: number;
}

// ── Activation (parcel → sphere) ────────────────────────────────

export interface Activation {
  parcel_id: string;
  sphere_id: string;
  activated_at: string;
  material_systems_installed: string[];
  status: SphereStatus;
}
