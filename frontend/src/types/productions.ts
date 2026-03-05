// Generated from sphere-os/src/productions/models.py

export type Genre = "sci-fi" | "drama" | "thriller" | "experimental";
export type Format =
  | "feature_film"
  | "series"
  | "short"
  | "installation"
  | "hybrid";
export type NarrativeFunction =
  | "builds_tension"
  | "reveals_character"
  | "marks_time_passage"
  | "establishes_mood"
  | "signals_resolution"
  | "creates_contrast";
export type LegacyMode =
  | "living_soundstage"
  | "public_installation"
  | "community_space"
  | "research_lab";

export interface MaterialCue {
  beat_id: string;
  timestamp_range: [number, number] | string;
  material_system: string;
  target_property: string;
  value_curve: number[];
  narrative_function: NarrativeFunction;
}

export interface MaterialPalette {
  tier_1_deployable_now: string[];
  tier_2_near_term: string[];
  tier_3_long_term: string[];
}

export interface ProductionProposal {
  id: string;
  parcel_id: string;
  title: string;
  logline: string;
  genre: Genre;
  format: Format;
  narrative_concept: string;
  material_script: MaterialCue[];
  min_area_sqft: number;
  required_utilities: string[];
  crew_size_estimate: number;
  estimated_budget_low_usd: number;
  estimated_budget_high_usd: number;
  production_timeline_weeks: number;
  legacy_modes: LegacyMode[];
  generated_by_model: string;
  creative_brief: string | null;
  generated_at: string;
  parent_proposal_id: string | null;
  iteration_feedback: string | null;
}

export interface GenerateRequest {
  parcel_id: string;
  creative_brief?: string;
  tier_filter?: number[];
  format?: string;
}

export interface IterateRequest {
  feedback: string;
}

export interface MaterialScriptResponse {
  proposal_id: string;
  title: string;
  material_script: MaterialCue[];
}
