/**
 * TypeScript types for the DOMES Dome visualization.
 *
 * The Dome is an architectural metaphor: a rotunda viewed from above,
 * divided into domain panels that can be fragmented (cracked, costly)
 * or coordinated (whole, efficient).
 */

// ---------------------------------------------------------------------------
// Core domain / system types
// ---------------------------------------------------------------------------

export interface DomeSystem {
  id: string;
  name: string;
  acronym: string;
  domain: string;
  annual_cost: number;
  coordinated_cost: number;
}

export interface DomeGapInfo {
  id: number;
  system_a: string;
  system_b: string;
  barrier_type: string;
  severity: string;
  consent_closable: boolean;
}

export interface DomeBridgeInfo {
  id: number;
  title: string;
  bridge_type: string;
  priority_score: number;
  estimated_cost: string;
}

export interface DomeDomain {
  domain: string;
  label: string;
  color: string;
  systems: DomeSystem[];
  provisions_count: number;
  gaps_count: number;
  annual_cost: number;
  coordinated_cost: number;
  savings: number;
  top_provisions: Array<{
    citation: string;
    title: string;
    type: string;
  }>;
  gaps: DomeGapInfo[];
  bridges: DomeBridgeInfo[];
}

// ---------------------------------------------------------------------------
// Connection / gap types
// ---------------------------------------------------------------------------

export interface DomeConnection {
  source_id: string;
  target_id: string;
  source_name: string;
  target_name: string;
  direction: string;
  format: string;
  reliability: string;
}

export interface DomeGap {
  id: number;
  system_a_id: string;
  system_b_id: string;
  system_a_name: string;
  system_b_name: string;
  barrier_type: string;
  severity: string;
  consent_closable: boolean;
  cost_to_bridge: string;
}

// ---------------------------------------------------------------------------
// Totals
// ---------------------------------------------------------------------------

export interface DomeTotals {
  annual_cost: number;
  coordinated_cost: number;
  savings: number;
  five_year: number;
  lifetime: number;
  systems_count: number;
  gaps_count: number;
  consent_closable: number;
}

// ---------------------------------------------------------------------------
// Mode
// ---------------------------------------------------------------------------

export type DomeMode = 'fragmented' | 'coordinated';

// ---------------------------------------------------------------------------
// Computed layout helpers (internal)
// ---------------------------------------------------------------------------

/** Computed position of a system element within the dome SVG. */
export interface SystemPosition {
  system: DomeSystem;
  x: number;
  y: number;
  angle: number;
  domain: string;
}

/** A sector's angular extent. */
export interface SectorGeometry {
  domain: string;
  startAngle: number;
  endAngle: number;
  midAngle: number;
  color: string;
  label: string;
}
