export type Domain = "health" | "justice" | "housing" | "income" | "education" | "child_welfare" | "civil_rights";

export const DOMAIN_COLORS: Record<string, string> = {
  health: "#1A6B3C",
  justice: "#8B1A1A",
  housing: "#1A3D8B",
  income: "#6B5A1A",
  education: "#5A1A6B",
  child_welfare: "#1A6B6B",
  civil_rights: "#6B1A4B",
};

export const DOMAIN_LABELS: Record<string, string> = {
  health: "Health",
  justice: "Justice",
  housing: "Housing",
  income: "Income",
  education: "Education",
  child_welfare: "Child Welfare",
  civil_rights: "Civil Rights",
};

export interface Provision {
  id: number;
  citation: string;
  title: string;
  full_text: string;
  source_type: string;
  title_number: string | null;
  chapter: string | null;
  part: string | null;
  section: string | null;
  subsection: string | null;
  domain: string;
  provision_type: string;
  applies_when: Record<string, unknown>;
  enforcement_mechanisms: string[];
  cross_references: string[];
  source_url: string | null;
  effective_date: string | null;
  last_amended: string | null;
  version: number;
  is_current: boolean;
  tags: string[];
  populations: string[];
  confidence_score: number;
  relevance_score?: number;
  match_score?: number;
  match_reasons?: string[];
}

export interface ProvisionHistory {
  id: number;
  provision_id: number;
  citation: string;
  field_changed: string;
  old_value: string | null;
  new_value: string | null;
  changed_at: string | null;
  change_source: string | null;
}

export interface ProvisionRelationship {
  id: number;
  source_id: number;
  target_id: number;
  source_citation: string | null;
  target_citation: string | null;
  relationship_type: string;
  description: string | null;
  confidence: number;
}

export interface TaxonomyTag {
  id: number;
  name: string;
  category: string;
  description: string | null;
  parent_tag: string | null;
}

export interface GraphNode {
  id: number;
  citation: string;
  title: string;
  domain: string;
  type: string;
  color: string;
  x: number;
  y: number;
}

export interface GraphEdge {
  source: number;
  target: number;
  type: string;
  label: string;
  confidence: number;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
}

export interface TaxonomyStats {
  total_provisions: number;
  domains: Record<string, number>;
  provision_types: Record<string, number>;
  source_types: Record<string, number>;
  total_tags: number;
}

export interface GraphStats {
  nodes: number;
  edges: number;
  relationship_types: Record<string, number>;
}

export interface SearchRequest {
  query?: string;
  domains?: string[];
  provision_types?: string[];
  tags?: string[];
  populations?: string[];
}

export interface DomainCount {
  domain: string;
  count: number;
}

export type Section = "search" | "browse" | "graph" | "monitor";
