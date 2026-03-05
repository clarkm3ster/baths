export interface CoordinationModel {
  id: number;
  name: string;
  abbreviation: string;
  category: string;
  description: string;
  target_population: string[];
  domains_covered: string[];
  authority_type: string;
  funding_sources: string[];
  typical_budget_range: { min: number; max: number; unit: string };
  staffing_model: Record<string, string>;
  governance_structure: string;
  key_features: string[];
  limitations: string[];
  evidence_rating: string;
  example_sites: string[];
  regulatory_requirements: string[];
  timeline_to_launch: string;
  political_feasibility: string;
}

export interface Architecture {
  id: number;
  name: string;
  description: string;
  status: string;
  population_size: number;
  population_description: string;
  annual_budget: number;
  geography: string;
  political_context: string;
  time_horizon: string;
  primary_model_id: number;
  hybrid_model_ids: number[];
  model_rationale: string;
  domains_targeted: string[];
  constraints: Record<string, unknown>;
  scores: ModelScore;
  implementation_phases: Phase[];
  stakeholders: Stakeholder[];
  budget_breakdown: BudgetBreakdown;
  risks: Risk[];
  workforce_plan: WorkforcePlan;
  authority_map: AuthorityMap;
  created_at: string;
  updated_at: string;
}

export interface ModelScore {
  model_id: number;
  model_name: string;
  composite: number;
  coverage: number;
  budget_feasibility: number;
  political_feasibility: number;
  speed: number;
  sustainability: number;
  population_fit: number;
  cost_efficiency: number;
}

export interface Phase {
  name: string;
  duration: string;
  description: string;
  milestones: string[];
  status: string;
}

export interface Stakeholder {
  name: string;
  role: string;
  influence: string;
  interest: string;
  description: string;
  engagement_strategy: string;
}

export interface BudgetBreakdown {
  total_annual: number;
  categories: BudgetCategory[];
  funding_sources: string[];
}

export interface BudgetCategory {
  name: string;
  percentage: number;
  amount: number;
  description: string;
}

export interface Risk {
  category: string;
  description: string;
  likelihood: string;
  impact: string;
  mitigation: string;
}

export interface WorkforcePlan {
  total_estimated_fte: number;
  roles: WorkforceRole[];
  training_approach: string;
  retention_strategy: string;
}

export interface WorkforceRole {
  title: string;
  ratio: string;
  estimated_fte: number;
  recruitment_timeline: string;
  training_required: string;
}

export interface AuthorityMap {
  primary_authority_type: string;
  entries: AuthorityEntry[];
}

export interface AuthorityEntry {
  authority: string;
  grantor: string;
  type: string;
  timeline: string;
  requirements: string[];
  status: string;
}

export interface ComparisonSet {
  id: number;
  name: string;
  architecture_ids: number[];
  architectures?: Architecture[];
  winner_id: number | null;
  comparison_notes: Record<string, string>;
  created_at: string;
}

export const DOMAIN_COLORS: Record<string, string> = {
  health: "#1A6B3C",
  behavioral_health: "#1A6B3C",
  justice: "#8B1A1A",
  housing: "#1A3D8B",
  income: "#6B5A1A",
  education: "#5A1A6B",
  child_welfare: "#1A6B6B",
  social_support: "#1A6B6B",
  immigration: "#555555",
};

export const CATEGORY_COLORS: Record<string, string> = {
  managed_care: "#1A3D8B",
  community_based: "#1A6B3C",
  hybrid: "#6B5A1A",
  specialized: "#5A1A6B",
};

export const DOMAIN_LABELS: Record<string, string> = {
  health: "Health",
  behavioral_health: "Behavioral Health",
  justice: "Justice",
  housing: "Housing",
  income: "Income",
  education: "Education",
  child_welfare: "Child Welfare",
  social_support: "Social Support",
  immigration: "Immigration",
};

export const CATEGORY_LABELS: Record<string, string> = {
  managed_care: "Managed Care",
  community_based: "Community-Based",
  hybrid: "Hybrid",
  specialized: "Specialized",
};
