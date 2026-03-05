// Generated from sphere-os/src/materials/drivers/

export type MaterialSystemType =
  | "acoustic_metamaterial"
  | "haptic_surface"
  | "olfactory_synthesis"
  | "electrochromic_surface"
  | "projection_mapping"
  | "phase_change_panel"
  | "shape_memory_element"
  | "4d_printed_deployable"
  | "bioluminescent_coating";

export type DriverStatus =
  | "idle"
  | "applying"
  | "transitioning"
  | "active"
  | "error"
  | "emergency_reset";

export type ValidationSeverity = "info" | "warning" | "error";

export interface ValidationIssue {
  field: string;
  message: string;
  severity: ValidationSeverity;
}

export interface ValidationResult {
  valid: boolean;
  issues: ValidationIssue[];
}

export interface DriverResponse {
  success: boolean;
  system_type: MaterialSystemType;
  transition_time_s: number;
  state_snapshot: Record<string, unknown>;
  error: string | null;
  request_id: string;
  timestamp: number;
}

export interface DriverInfo {
  system_type: MaterialSystemType;
  trl: number;
  status: DriverStatus;
  simulation_mode: boolean;
  simulation_speed: number;
  capabilities: Record<string, unknown>;
}

// ── Per-driver state shapes ─────────────────────────────────────

export interface AcousticState {
  reverb_time_s: number;
  absorption_bands: number[];
  diffusion: number;
  beam_steering_deg: number;
  switching_time_ms: number;
}

export interface HapticState {
  floor_haptic_pattern: string;
  floor_haptic_intensity: number;
}

export interface ElectrochromicState {
  wall_color_rgb: [number, number, number];
  wall_opacity: number;
}

export interface OlfactoryState {
  components: Record<string, number>;
  intensity: number;
  blend_name: string;
  clearing: boolean;
  clearing_remaining_s: number;
  voc_level: number;
}

export interface PhaseChangeState {
  thermal_target_celsius: number;
  current_celsius: number;
}

export interface ProjectionState {
  light_color_temp_kelvin: number;
  light_intensity_lux: number;
}

export interface ShapeMemoryElement {
  element_id: string;
  target_curvature: number;
}

export interface ShapeMemoryState {
  elements: ShapeMemoryElement[];
}

export interface Deployable4DState {
  deployed: boolean;
  configuration: Record<string, unknown>;
}

export interface BioluminescentState {
  health: number;
  luminosity: number;
  culture_age_days: number;
}

export type DriverState =
  | AcousticState
  | HapticState
  | ElectrochromicState
  | OlfactoryState
  | PhaseChangeState
  | ProjectionState
  | ShapeMemoryState
  | Deployable4DState
  | BioluminescentState;

// ── Material Configuration (composite) ──────────────────────────

export interface ScentProfile {
  primary: string | null;
  secondary: string | null;
  intensity: number;
}

export interface MaterialConfiguration {
  acoustic_reverb_time_seconds: number;
  acoustic_absorption_profile: number[];
  wall_color_rgb: [number, number, number];
  wall_opacity: number;
  light_color_temp_kelvin: number;
  light_intensity_lux: number;
  floor_haptic_pattern: string;
  floor_haptic_intensity: number;
  scent_profile: ScentProfile;
  thermal_target_celsius: number;
  shape_memory_elements: ShapeMemoryElement[];
}

// ── Transition times ────────────────────────────────────────────

export const MATERIAL_TRANSITION_TIMES: Record<
  MaterialSystemType,
  { min_s: number; max_s: number }
> = {
  acoustic_metamaterial: { min_s: 0.025, max_s: 60 },
  haptic_surface: { min_s: 0.025, max_s: 5 },
  olfactory_synthesis: { min_s: 600, max_s: 1200 },
  electrochromic_surface: { min_s: 1, max_s: 5 },
  projection_mapping: { min_s: 0.1, max_s: 10 },
  phase_change_panel: { min_s: 300, max_s: 1800 },
  shape_memory_element: { min_s: 300, max_s: 3600 },
  "4d_printed_deployable": { min_s: 1800, max_s: 3600 },
  bioluminescent_coating: { min_s: 0, max_s: 0 },
};
