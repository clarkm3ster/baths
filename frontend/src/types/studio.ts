// Generated from domes-legal/backend/app/studio/schemas.py

export type CharacterType = "real" | "fictional" | "composite" | "scenario";
export type ConsentTier =
  | "tier1_public"
  | "tier2_personal"
  | "tier3_sensitive"
  | "tier4_highest";
export type ProductionMedium =
  | "film"
  | "short"
  | "doc"
  | "series"
  | "installation"
  | "live_event"
  | "product"
  | "game"
  | "interactive";
export type ProductionStageStatus =
  | "greenlit"
  | "in_progress"
  | "paused"
  | "shipped";
export type GapArea =
  | "metrics"
  | "connectors"
  | "ledger"
  | "forecast"
  | "scenario"
  | "settlement"
  | "validation"
  | "consent"
  | "ux";
export type GapSeverity = "low" | "medium" | "high" | "blocking";
export type GapStatus =
  | "new"
  | "triaged"
  | "planned"
  | "in_progress"
  | "shipped"
  | "wont_fix";
export type AssetType =
  | "script"
  | "footage"
  | "cut"
  | "poster"
  | "soundtrack"
  | "prototype"
  | "dataset_synthetic"
  | "curriculum"
  | "installation_plan";

export interface CharacterProfile {
  character_id: string;
  character_type: CharacterType;
  name_or_alias: string;
  consent_tier: ConsentTier;
  fictionalization_rules: Record<string, unknown>;
  circumstances_summary: string;
  initial_conditions: Record<string, unknown>;
  created_at?: string;
}

export interface TalentRole {
  person_or_entity: string;
  role: string;
  rate_type: "day" | "week" | "flat" | "salary" | "vendor";
  rate: number;
  production_id?: string;
}

export interface ProductionStage {
  stage: string;
  start_date: string;
  end_date: string;
  cost_cap: number;
  deliverables: string[];
  risk_register: string[];
  production_id?: string;
}

export interface Production {
  production_id: string;
  title: string;
  medium: ProductionMedium;
  character_id: string;
  stage: ProductionStageStatus;
  stages: ProductionStage[];
  team: TalentRole[];
  budget_total: number;
  financing_sources: string[] | Record<string, unknown>;
  generated_at: string;
  stats?: { gaps: number; assets: number };
}

export interface GapItem {
  gap_id: string;
  production_id: string;
  character_id: string;
  discovered_at: string;
  area: GapArea;
  severity: GapSeverity;
  description: string;
  reproduction_steps: string[];
  proposed_fix: string | null;
  owner_module: string | null;
  status: GapStatus;
}

export interface IPAsset {
  asset_id: string;
  production_id: string;
  asset_type: AssetType;
  title: string;
  storage_uri: string | null;
  contributors: string[];
  rights: Record<string, unknown>;
  created_at: string;
}

export interface LearningPackage {
  learning_id: string;
  production_id: string;
  summary: string;
  gap_ids: string[];
  proposed_os_changes: string[];
  validation_needed: string[];
  generated_at: string;
}

export interface BacklogView {
  production_id: string;
  total: number;
  by_severity: Record<string, { count: number; items: GapItem[] }>;
  by_area: Record<string, { count: number; items: GapItem[] }>;
  by_owner_module: Record<string, { count: number; items: GapItem[] }>;
}

export interface StudioDashboard {
  total_characters: number;
  total_productions: number;
  productions_by_stage: Record<string, number>;
  total_gaps: number;
  gaps_by_severity: Record<string, number>;
  total_assets: number;
  total_learning_packages: number;
}
