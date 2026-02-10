export interface System {
  id: string;
  name: string;
  acronym: string;
  agency: string;
  domain: Domain;
  description: string;
  data_standard: string;
  data_held: string[];
  who_can_access: string[];
  privacy_law: string;
  privacy_laws: string[];
  applies_when: string[];
  is_federal: boolean;
  state_operated: boolean;
}

export interface Connection {
  id: number;
  source_id: string;
  target_id: string;
  direction: "unidirectional" | "bidirectional";
  frequency: string;
  format: string;
  data_shared: string[];
  description: string;
  reliability: "high" | "moderate" | "low";
}

export interface Gap {
  id: number;
  system_a_id: string;
  system_b_id: string;
  barrier_type: "legal" | "technical" | "political" | "funding" | "consent";
  barrier_law: string;
  barrier_description: string;
  impact: string;
  what_it_would_take: string;
  consent_closable: boolean;
  consent_mechanism: string;
  severity: "critical" | "high" | "moderate" | "low";
  applies_when: string[];
}

export interface ConstellationResponse {
  systems: System[];
  connections: Connection[];
  gaps: Gap[];
  summary: {
    total_systems: number;
    connected: number;
    siloed: number;
    gaps: number;
    consent_closable: number;
  };
}

export type Domain =
  | "health"
  | "justice"
  | "housing"
  | "income"
  | "education"
  | "child_welfare";

export interface Profile {
  age_group?: string;
  insurance: string[];
  disabilities: string[];
  housing: string[];
  income: string[];
  system_involvement: string[];
  pregnant?: boolean;
  veteran?: boolean;
  dv_survivor?: boolean;
  immigrant?: boolean;
  lgbtq?: boolean;
  rural?: boolean;
}

export const DOMAIN_LABELS: Record<Domain, string> = {
  health: "Health",
  justice: "Justice",
  housing: "Housing",
  income: "Income & Benefits",
  education: "Education",
  child_welfare: "Child Welfare",
};

export const DOMAIN_COLORS: Record<Domain, string> = {
  health: "#1A6B3C",
  justice: "#8B1A1A",
  housing: "#1A3D8B",
  income: "#6B5A1A",
  education: "#5A1A6B",
  child_welfare: "#1A6B6B",
};

export const SEVERITY_LABELS: Record<string, string> = {
  critical: "Critical",
  high: "High",
  moderate: "Moderate",
  low: "Low",
};
