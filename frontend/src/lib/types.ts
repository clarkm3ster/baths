/**
 * Compatibility re-exports — maps old type names to new canonical types.
 * New code should import from "@/types" directly.
 */
export type {
  ParcelRecord,
  ParcelCluster,
} from "@/types/land";

export type {
  MaterialSystemType,
  DriverStatus,
  DriverInfo,
  DriverResponse,
  MaterialConfiguration,
} from "@/types/materials";

export type {
  ProductionProposal,
  MaterialCue,
} from "@/types/productions";

export type {
  SafetyEvent,
  SafetyReport,
  SafetyViolation,
} from "@/types/safety";

export type {
  Sphere,
  SphereStatus,
  SphereMode,
  Booking,
  BookingStatus,
  TimeSlice,
} from "@/types/scheduling";

// ── Compat aliases for old type names ───────────────────────────

/** @deprecated Use ParcelRecord instead */
export interface ParcelFeature {
  type: "Feature";
  id: string;
  geometry: unknown;
  properties: {
    address: string;
    area_sqft: number;
    zoning: string | null;
    viability_score: number | null;
    cluster_id: string | null;
    status: string;
  };
}

/** @deprecated Use ParcelRecord[] instead */
export interface ParcelCollection {
  type: "FeatureCollection";
  features: ParcelFeature[];
}

/** @deprecated Use Record<string, unknown> instead */
export type MaterialState = Record<string, Record<string, unknown>>;

/** @deprecated Use TimeSlice instead */
export interface TimeSlot {
  start: string;
  end: string;
  available: boolean;
}

export type { EnvironmentReading } from "@/types/scheduling";
