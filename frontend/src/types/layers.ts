// Generated from domes-legal/backend/app/studio/ OS layer modules

// ── Treasury (CliffGuard) ────────────────────────────────────────

export interface TreasuryAccount {
  account_id: string;
  person_id: string;
  balance: number;
  restricted_uses: string[];
  created_at: string;
}

export interface Disbursement {
  disbursement_id: string;
  account_id: string;
  amount: number;
  category: string;
  method: "fednow" | "rtp" | "ach" | "check";
  status: "pending" | "completed" | "failed" | "clawed_back";
  initiated_at: string;
  completed_at: string | null;
}

export interface CliffGuard {
  person_id: string;
  current_benefits: Record<string, number>;
  earned_income: number;
  effective_marginal_tax_rate: number;
  cliff_zones: number[];
  max_safe_income: number;
}

// ── Bio Experiment (N-of-1 Trials) ──────────────────────────────

export interface TrialPhase {
  phase_type: "baseline" | "intervention" | "washout" | "control";
  start_day: number;
  end_day: number;
  measurements: number[];
}

export interface PersonalTrial {
  trial_id: string;
  person_id: string;
  hypothesis: string;
  intervention: string;
  control: string;
  metric_name: string;
  phases: TrialPhase[];
  status: "designed" | "active" | "washout" | "completed" | "stopped";
  created_at: string;
}

export interface TrialResult {
  trial_id: string;
  intervention_mean: number;
  control_mean: number;
  effect_size: number;
  p_value: number;
  bayesian_probability: number;
  recommendation: string;
}

// ── Evidence Registry ───────────────────────────────────────────

export interface EvidenceEntry {
  entry_id: string;
  source: string;
  population_descriptor: Record<string, unknown>;
  endpoint_clinical: string;
  endpoint_fiscal: string;
  effect_size: number;
  confidence_interval: [number, number];
  external_validity_score: number;
  unit_cost_function: string;
}

export interface OutcomeMapping {
  clinical_endpoint: string;
  utilization_endpoint: string;
  payer_cost_function: string;
}

// ── Provider Marketplace ────────────────────────────────────────

export interface Provider {
  provider_id: string;
  name: string;
  service_types: string[];
  accepts_medicaid: boolean;
  accepts_medicare: boolean;
  sliding_scale: boolean;
  languages: string[];
  location: Record<string, unknown>;
  availability_score: number;
  quality_score: number;
  wait_days: number;
}

export interface Referral {
  referral_id: string;
  person_id: string;
  provider_id: string;
  service_type: string;
  status:
    | "created"
    | "sent"
    | "accepted"
    | "completed"
    | "no_show"
    | "cancelled";
  created_at: string;
  outcome_score: number | null;
}

// ── Labor Market ────────────────────────────────────────────────

export interface JobOpening {
  job_id: string;
  title: string;
  employer: string;
  wage_hourly: number;
  wage_annual: number;
  credentials_required: string[];
  location: Record<string, unknown>;
  commute_minutes: number;
  benefits: Record<string, unknown>;
  industry: string;
  posted_at: string;
}

export interface CredentialPathway {
  pathway_id: string;
  current_credentials: string[];
  target_credential: string;
  steps: string[];
  estimated_weeks: number;
  estimated_cost: number;
  funding_sources: string[];
}

export interface LaborMarketAnalysis {
  person_id: string;
  current_wage: number;
  target_wage: number;
  matched_jobs: Record<string, unknown>[];
  credential_gaps: string[];
  pathways: CredentialPathway[];
  commute_feasibility: Record<string, unknown>;
}

// ── Capital Markets (Prevention-Backed Securities) ──────────────

export interface SettlementContract {
  contract_id: string;
  person_id: string;
  intervention_type: string;
  expected_savings: Record<string, number>;
  probability_of_success: number;
  verification_method: string;
  term_years: number;
  status: "active" | "verified" | "defaulted" | "matured";
}

export interface PreventionBond {
  bond_id: string;
  name: string;
  contracts: string[];
  total_notional: number;
  coupon_rate: number;
  expected_yield: number;
  tranche: "senior" | "mezzanine" | "equity";
  vintage_year: number;
  status: "structuring" | "offered" | "active" | "matured";
}

export interface BondPricing {
  bond_id: string;
  expected_return: number;
  var_95: number;
  default_probability: number;
  stress_test_results: Record<string, unknown>;
  discount_rate: number;
}

// ── Spatial Mobility ────────────────────────────────────────────

export interface MobilityProfile {
  person_id: string;
  home_location: { lat: number; lng: number };
  has_vehicle: boolean;
  transit_pass: boolean;
  mobility_constraints: string[];
  typical_travel_budget_monthly: number;
}

export interface AccessScore {
  destination_type: string;
  destination_name: string;
  straight_line_miles: number;
  transit_minutes: number;
  drive_minutes: number;
  cost_per_trip: number;
  accessibility_score: number;
  barriers: string[];
}

export interface SpatialAnalysis {
  person_id: string;
  access_scores: AccessScore[];
  overall_mobility_score: number;
  critical_gaps: string[];
  recommendations: string[];
}

// ── Info Security ───────────────────────────────────────────────

export interface ExposureEvent {
  event_id: string;
  person_id: string;
  exposure_type:
    | "predatory_ad"
    | "algorithmic_radicalization"
    | "doomscrolling"
    | "phishing"
    | "misinformation"
    | "scam_contact";
  source_platform: string;
  severity: number;
  detected_at: string;
  context: Record<string, unknown>;
  intervention_triggered: boolean;
}

export interface CognitiveHealthScore {
  person_id: string;
  score: number;
  exposure_count_30d: number;
  high_severity_count: number;
  trend: "improving" | "stable" | "declining";
  risk_factors: string[];
}

export interface DigitalEnvironmentReport {
  person_id: string;
  period_days: number;
  total_exposures: number;
  by_type: Record<string, number>;
  cognitive_health: CognitiveHealthScore;
  recommended_interventions: string[];
}

// ── Governance ──────────────────────────────────────────────────

export interface AppealRequest {
  appeal_id: string;
  person_id: string;
  prediction_type: "trajectory" | "alert" | "classification";
  prediction_id: string;
  grounds: string;
  evidence: string[];
  status:
    | "submitted"
    | "under_review"
    | "upheld"
    | "overturned"
    | "withdrawn";
  filed_at: string;
  resolved_at: string | null;
  resolution_notes: string | null;
}

export interface DataRights {
  right_id: string;
  person_id: string;
  right_type:
    | "export"
    | "deletion"
    | "benefit_sharing"
    | "access_log"
    | "correction";
  requested_at: string;
  fulfilled_at: string | null;
  status: "requested" | "in_progress" | "fulfilled" | "denied";
  details: string | null;
}

// ── Narrative Synthesis ─────────────────────────────────────────

export type ArcType =
  | "rising_tension"
  | "turning_point"
  | "fall_and_recovery"
  | "slow_burn"
  | "cascade"
  | "breakthrough";

export interface NarrativeThread {
  thread_id: string;
  person_id: string;
  title: string;
  arc_type: ArcType;
  summary: string;
  tension_score: number;
  stakes: Record<string, unknown>;
  events: Record<string, unknown>[];
  turning_points: string[];
  resolution_hooks: string[];
  discovered_at: string;
}

export interface NarrativePackage {
  package_id: string;
  person_id: string;
  threads: NarrativeThread[];
  dramatic_potential: number;
  recommended_medium: string;
  generated_at: string;
}

// ── Full Packet (all layers combined for one person) ────────────

export interface FullPacket {
  person: {
    person_id: string;
    name: string;
    age: number;
    sex: string;
    earned_income: number;
    benefits: Record<string, number>;
    conditions: string[];
    location: Record<string, unknown>;
  };
  treasury: {
    cliff_guard: CliffGuard;
  };
  bio_experiment: {
    trial: PersonalTrial;
    result: TrialResult;
  };
  providers: {
    matched: Provider[];
    referrals: Referral[];
  };
  labor_market: LaborMarketAnalysis;
  spatial: {
    mobility_profile: MobilityProfile;
    spatial_analysis: SpatialAnalysis;
  };
  governance: {
    appeal: AppealRequest;
    data_rights: DataRights[];
  };
  evidence: {
    entries: EvidenceEntry[];
  };
  info_security: {
    cascade_risk: {
      risk_level: string;
      exposure_count: number;
    };
  };
  capital_markets: {
    contract: SettlementContract;
    pricing: BondPricing;
  };
  narrative: {
    package: NarrativePackage;
    production_score: {
      total_score: number;
      recommendation: string;
    };
  };
}
