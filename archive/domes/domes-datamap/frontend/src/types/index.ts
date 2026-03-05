export interface System {
  id: string;
  name: string;
  acronym: string;
  agency: string;
  domain: string;
  description: string;
  data_standard: string;
  fields_held: string[];
  api_availability: string;
  update_frequency: string;
  privacy_law: string;
  privacy_laws: string[];
  is_federal: boolean;
  state_operated: boolean;
  applies_when: string[];
}

export interface Connection {
  id: number;
  source_id: string;
  target_id: string;
  source_name?: string;
  target_name?: string;
  direction: string;
  format: string;
  frequency: string;
  data_shared: string[];
  governing_agreement: string;
  privacy_law: string;
  reliability: string;
  description: string;
}

export interface Gap {
  id: number;
  system_a_id: string;
  system_b_id: string;
  system_a_name?: string;
  system_b_name?: string;
  barrier_type: string;
  barrier_law: string | null;
  barrier_description: string;
  impact: string;
  severity: string;
  cost_to_bridge: string;
  timeline_to_bridge: string;
  consent_closable: boolean;
  consent_mechanism: string | null;
  what_it_would_take: string;
  applies_when: string[];
  bridges?: Bridge[];
}

export interface Bridge {
  id: number;
  gap_id: number;
  bridge_type: string;
  title: string;
  description: string;
  technical_requirements: string | null;
  legal_requirements: string | null;
  estimated_cost: string;
  timeline: string;
  who_pays: string;
  priority_score: number;
  impact_score: number;
  effort_score: number;
  status: string;
}

export interface PersonMapResult {
  systems: System[];
  connections: Connection[];
  gaps: Gap[];
  bridges: Bridge[];
  summary: {
    total_systems: number;
    connected_pairs: number;
    disconnected_pairs: number;
    gaps_count: number;
    consent_closable_count: number;
    total_bridge_cost: string;
  };
}

export interface MatrixData {
  systems: System[];
  matrix: (Connection | null)[][];
}

export interface Stats {
  total_systems: number;
  total_connections: number;
  total_gaps: number;
  by_severity: Record<string, number>;
  by_barrier_type: Record<string, number>;
  consent_closable_count: number;
  total_bridges: number;
  avg_priority: number;
}

export type Domain =
  | "Health"
  | "Justice"
  | "Housing"
  | "Income"
  | "Education"
  | "Child Welfare";

export const DOMAIN_COLORS: Record<string, string> = {
  Health: "#1A6B3C",
  Justice: "#8B1A1A",
  Housing: "#1A3D8B",
  Income: "#6B5A1A",
  Education: "#5A1A6B",
  "Child Welfare": "#1A6B6B",
};

export const DOMAINS: Domain[] = [
  "Health",
  "Justice",
  "Housing",
  "Income",
  "Education",
  "Child Welfare",
];

export const SEVERITY_ORDER = ["critical", "high", "moderate", "low"] as const;

export const CIRCUMSTANCES = [
  "medicaid",
  "incarcerated",
  "recently_released",
  "substance_use",
  "mental_health",
  "homeless",
  "foster_care",
  "veteran",
  "disabled",
  "low_income",
  "school_age",
  "special_education",
  "pregnant",
  "unemployed",
  "snap_recipient",
  "tanf_recipient",
  "child_support",
  "probation",
  "parole",
  "immigration",
] as const;

export type Circumstance = (typeof CIRCUMSTANCES)[number];
