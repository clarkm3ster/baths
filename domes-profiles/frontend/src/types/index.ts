/**
 * DOMES Profiles — TypeScript type definitions.
 *
 * Core data types for profiles, domains, costs, and circumstances.
 * Dome visualization types are in components/dome/types.ts (owned by DOME-RENDERER).
 */

// Re-export dome types for convenience
export type {
  DomeDomain,
  DomeSystem,
  DomeConnection,
  DomeGap,
  DomeTotals,
  DomeMode,
  DomeGapInfo,
  DomeBridgeInfo,
} from '../components/dome/types';

// ---------------------------------------------------------------------------
// Profile
// ---------------------------------------------------------------------------

export interface Profile {
  id: string;
  name: string;
  version: number;
  created_at: string;
  updated_at: string;
  circumstances: Record<string, boolean | string>;
  systems_involved: string[];
  total_annual_cost: number;
  coordinated_annual_cost: number;
  savings_annual: number;
  five_year_projection: number;
  lifetime_estimate: number;
  narrative: string;
  is_sample: boolean;
  domains: ProfileDomain[];
}

export interface ProfileDomain {
  id: number;
  profile_id: string;
  domain: string;
  domain_label: string;
  systems: any[];
  provisions_count: number;
  annual_cost: number;
  coordinated_cost: number;
  savings: number;
  top_provisions: any[];
  gaps: any[];
  bridges: any[];
}

// ---------------------------------------------------------------------------
// Dome data (response from /api/profiles/{id}/dome)
// ---------------------------------------------------------------------------

export interface DomeData {
  profile: Profile;
  domains: import('../components/dome/types').DomeDomain[];
  totals: import('../components/dome/types').DomeTotals;
  connections: import('../components/dome/types').DomeConnection[];
  consent_pathways: any[];
}

// ---------------------------------------------------------------------------
// Cost
// ---------------------------------------------------------------------------

export interface CostBenchmark {
  label: string;
  domain: string;
  base_cost: number;
  categories?: Record<string, number>;
  source: string;
}

export interface CostCalculation {
  systems: SystemCost[];
  total_fragmented: number;
  total_coordinated: number;
  total_savings: number;
  five_year_projection: number;
}

export interface SystemCost {
  system_id: string;
  system_name: string;
  domain: string;
  fragmented_cost: number;
  coordinated_cost: number;
  savings: number;
  categories?: Record<string, number>;
  source?: string;
}

export interface ROIResult {
  coordination_cost: number;
  annual_savings: number;
  break_even_months: number;
  five_year_roi: number;
  five_year_net: number;
  ten_year_net: number;
}

export interface ScaleResult {
  per_person: number;
  formatted: Record<string, string>;
  populations: Record<string, number>;
}

export interface AvoidableEvent {
  id: string;
  label: string;
  domain: string;
  cost_per_event: number;
  annual_frequency: number;
  annual_cost: number;
  avoidable_pct: number;
  avoidable_savings: number;
  source: string;
}

// ---------------------------------------------------------------------------
// Circumstances
// ---------------------------------------------------------------------------

export interface Circumstance {
  key: string;
  label: string;
  category: string;
}

export interface CircumstanceGroup {
  category: string;
  color: string;
  items: Circumstance[];
}

// ---------------------------------------------------------------------------
// Compare
// ---------------------------------------------------------------------------

export interface CompareResult {
  profiles: Profile[];
  deltas: {
    cost_delta: number;
    savings_delta: number;
    systems_delta: number;
    gaps_delta: number;
    circumstances_diff: string[];
  };
}

// ---------------------------------------------------------------------------
// Timeline
// ---------------------------------------------------------------------------

export interface TimelineEvent {
  date: string;
  label: string;
  type: 'entry' | 'crisis' | 'gap' | 'coordination' | 'exit';
  systems: string[];
  domain: string;
  cost_impact: number;
  description: string;
}
