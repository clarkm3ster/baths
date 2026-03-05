// Generated from sphere-os/src/safety/models.py

export interface SafetyViolation {
  system_type: string;
  parameter: string;
  value: number;
  threshold: number;
  severity: string;
  description: string;
}

export interface SafetyReport {
  sphere_id: string;
  timestamp: string;
  all_clear: boolean;
  violations: SafetyViolation[];
  system_states: Record<string, unknown>;
}

export interface SafetyEvent {
  id: string;
  sphere_id: string;
  timestamp: string;
  system_type: string;
  severity: string;
  parameter: string;
  value: number;
  threshold: number;
  resolved: boolean;
  acknowledged: boolean;
  resolved_at?: string | null;
  /** Compat: alias for timestamp */
  created_at?: string;
  /** Compat: derived description */
  message?: string;
}
