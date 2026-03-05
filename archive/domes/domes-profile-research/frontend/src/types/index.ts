export interface SystemProfile {
  id: string;
  name: string;
  acronym: string;
  domain: Domain;
  data_held: string[];
  annual_cost_per_person: number | null;
  typical_utilization?: number;
  cost_source: string | null;
  applies_when: string[];
}

export interface DocumentedCase {
  id: string;
  source: string;
  source_url: string | null;
  source_title: string;
  source_date: string | null;
  source_type: string;
  domain: string;
  system_ids: string[];
  circumstance_tags: string[];
  age_range: string | null;
  summary: string;
  finding: string;
  cost_data: Record<string, number> | null;
  location: string | null;
  year: number | null;
  relevance_score?: number;
}

export interface CostBenchmark {
  id: string;
  category: string;
  label: string;
  cost_per_unit: number;
  unit: string;
  source: string;
  source_url: string | null;
  year: number | null;
  notes: string | null;
}

export interface TimelineEvent {
  age: number;
  event: string;
  system: string | null;
  domain: string | null;
  type: "entry" | "placement" | "disruption" | "gap" | "waiting" | "release" | "crisis" | "current";
  citation_id?: string | null;
}

export interface CostItem {
  system_id: string;
  system_name: string;
  acronym: string;
  domain: string;
  full_annual_cost?: number;
  typical_utilization?: number;
  utilized_cost?: number;
  annual_cost: number;
  source: string;
}

export interface CoordinatedItem {
  domain: string;
  fragmented_cost: number;
  coordinated_cost: number;
  savings: number;
  savings_factor: number;
  source: string;
  source_url: string;
  notes: string;
}

export interface CostResult {
  fragmented: {
    items: CostItem[];
    total: number;
    admin_overhead: number;
    admin_source: string;
    grand_total: number;
  };
  coordinated: {
    items: CoordinatedItem[];
    total: number;
    admin_overhead: number;
    grand_total: number;
  };
  savings: {
    service_savings: number;
    admin_savings: number;
    total_savings: number;
    savings_pct: number;
  };
  benchmarks: Record<string, CostBenchmark>;
}

export interface SystemDetailItem {
  id: string;
  name: string;
  acronym: string;
  domain: string;
  data_held: string[];
  annual_cost_per_person: number | null;
  cost_source: string | null;
}

export interface CompositeProfile {
  id: string;
  name: string;
  age: number;
  circumstances: Record<string, unknown>;
  systems_involved: string[];
  timeline: TimelineEvent[];
  total_annual_cost: number;
  cost_breakdown: CostItem[];
  citations: string[];
  coordinated_cost: number;
  narrative: string;
  matched_cases: DocumentedCase[];
  matched_systems: SystemProfile[];
  systems_detail: SystemDetailItem[];
  cost_benchmarks: CostBenchmark[];
}

export interface Circumstances {
  age: string;
  gender: string;
  has_mental_health: boolean;
  has_substance_use: boolean;
  has_disability: boolean;
  is_homeless: boolean;
  has_criminal_justice: boolean;
  has_children: boolean;
  is_on_medicaid: boolean;
  is_on_snap: boolean;
  is_on_tanf: boolean;
  is_on_ssi: boolean;
  has_housing_assistance: boolean;
  is_unemployed: boolean;
  has_foster_care: boolean;
  has_juvenile_justice: boolean;
  has_chronic_health: boolean;
  is_on_probation: boolean;
}

export type Domain = "health" | "justice" | "housing" | "income" | "education" | "child_welfare";

export const DOMAIN_COLORS: Record<string, string> = {
  health: "#1A6B3C",
  justice: "#8B1A1A",
  housing: "#1A3D8B",
  income: "#6B5A1A",
  education: "#5A1A6B",
  child_welfare: "#1A6B6B",
};

export const DOMAIN_LABELS: Record<string, string> = {
  health: "Health",
  justice: "Justice",
  housing: "Housing",
  income: "Income",
  education: "Education",
  child_welfare: "Child Welfare",
};

export type Section = "timeline" | "cost" | "citations" | "compare";
