/** Profile sent to the backend POST /api/match endpoint. */
export interface PersonProfile {
  insurance: string[];
  disabilities: string[];
  age_group: string;
  pregnant: boolean;
  housing: string[];
  income: string[];
  system_involvement: string[];
  veteran: boolean;
  dv_survivor: boolean;
  immigrant: boolean;
  lgbtq: boolean;
  rural: boolean;
  state: string;
}

/** A provision as returned by GET /api/provisions. */
export interface Provision {
  id: number;
  citation: string;
  title: string;
  full_text: string;
  domain: Domain;
  provision_type: ProvisionType;
  applies_when: Record<string, string[]>;
  enforcement_mechanisms: string[];
  source_url: string;
  cross_references: string[];
}

export type Domain =
  | 'health'
  | 'housing'
  | 'income'
  | 'justice'
  | 'education'
  | 'civil_rights';

export type ProvisionType = 'right' | 'obligation' | 'protection' | 'enforcement';

/** A single matched provision returned by the backend matching engine. */
export interface MatchedProvision {
  provision_id: number;
  citation: string;
  title: string;
  domain: Domain;
  provision_type: ProvisionType;
  relevance_score: number;
  match_reasons: string[];
  enforcement_steps: string[];
  is_gap: boolean;
  full_text?: string;
  source_url?: string;
  cross_references?: string[];
}

/** Cross-reference between two provisions. */
export interface CrossReference {
  target_id: number;
  target_citation: string;
  relationship: string;
  description: string;
}

/** Raw response from POST /api/match. */
export interface MatchApiResponse {
  matches: MatchedProvision[];
  gaps: MatchedProvision[];
  cross_references: Record<number, CrossReference[]>;
}

/** Frontend-friendly match result passed through router state. */
export interface MatchResult {
  profile: PersonProfile;
  matches: MatchedProvision[];
  gaps: MatchedProvision[];
  cross_references: Record<number, CrossReference[]>;
  total_matched: number;
}

export interface DomainCount {
  domain: Domain;
  count: number;
}

export const DOMAIN_COLORS: Record<Domain, string> = {
  health: '#1a1a2e',
  housing: '#16213e',
  income: '#0f3460',
  justice: '#533483',
  education: '#e94560',
  civil_rights: '#0a0a0a',
};

export const DOMAIN_LABELS: Record<Domain, string> = {
  health: 'Health',
  housing: 'Housing',
  income: 'Income',
  justice: 'Justice',
  education: 'Education',
  civil_rights: 'Civil Rights',
};

/** A provision annotated with matching metadata for the dome visualization. */
export interface DomeProvision {
  provision: Provision;
  relevance_score: number;
  match_reasons: string[];
  is_gap: boolean;
}

/** Result from the Claude API explanation endpoint. */
export interface ExplanationResult {
  plain_english: string;
  what_it_means_for_you: string;
  your_rights: string[];
  enforcement_steps: string[];
  key_deadlines: string[];
  who_to_contact: string[];
}
