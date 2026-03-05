// ---------------------------------------------------------------------------
// Domain types
// ---------------------------------------------------------------------------

export type Domain =
  | "Health"
  | "Justice"
  | "Housing"
  | "Income"
  | "Education"
  | "Child Welfare";

export const DOMAIN_COLORS: Record<string, string> = {
  Health: "var(--color-health)",
  Justice: "var(--color-justice)",
  Housing: "var(--color-housing)",
  Income: "var(--color-income)",
  Education: "var(--color-education)",
  "Child Welfare": "var(--color-child-welfare)",
};

export const DOMAIN_LABELS: Record<string, string> = {
  Health: "Health",
  Justice: "Justice",
  Housing: "Housing",
  Income: "Income",
  Education: "Education",
  "Child Welfare": "Child Welfare",
};

// ---------------------------------------------------------------------------
// Agreement types
// ---------------------------------------------------------------------------

export const AGREEMENT_TYPE_LABELS: Record<string, string> = {
  BAA: "Business Associate Agreement",
  DUA: "Data Use Agreement",
  MOU: "Memorandum of Understanding",
  IDSA: "Inter-Agency Data Sharing Agreement",
  QSOA: "Qualified Service Organization Agreement",
  HIPAA_consent: "HIPAA Consent",
  FERPA_consent: "FERPA Consent",
  compact: "Interstate Compact",
  joint_funding: "Joint Funding Agreement",
};

// ---------------------------------------------------------------------------
// System reference (from domes-datamap)
// ---------------------------------------------------------------------------

export interface SystemRef {
  id: string;
  name: string;
  acronym: string;
  domain: string;
}

// ---------------------------------------------------------------------------
// Gap (from domes-datamap)
// ---------------------------------------------------------------------------

export interface Gap {
  id: number;
  system_a_id: string;
  system_b_id: string;
  barrier_type: string;
  barrier_law: string;
  barrier_description: string;
  impact: string;
  what_it_would_take: string;
  consent_closable: boolean;
  consent_mechanism: string;
  severity: string;
  applies_when: string[];
  system_a?: SystemRef;
  system_b?: SystemRef;
}

// ---------------------------------------------------------------------------
// Compliance flag (embedded in Agreement)
// ---------------------------------------------------------------------------

export interface ComplianceFlag {
  rule_id: string;
  law: string;
  requirement: string;
  severity: string;
  status: "pass" | "fail" | "warning";
  detail: string;
}

// ---------------------------------------------------------------------------
// Agreement
// ---------------------------------------------------------------------------

export interface Agreement {
  id: string;
  template_id: string;
  agreement_type: string;
  title: string;
  status: "draft" | "in_review" | "executed";
  gap_id: number | null;
  system_a_id: string;
  system_b_id: string;
  party_a_name: string;
  party_b_name: string;
  governing_laws: string[];
  required_signatories: string[];
  data_elements: string[];
  privacy_provisions: string[];
  key_terms: string[];
  body_text: string;
  compliance_status: string;
  compliance_flags: ComplianceFlag[];
  created_at: string;
  updated_at: string;
}

// ---------------------------------------------------------------------------
// Template
// ---------------------------------------------------------------------------

export interface Template {
  id: string;
  agreement_type: string;
  name: string;
  description: string;
  governing_laws: string[];
  required_provisions: string[];
  variable_fields: string[];
  body_template: string;
}

// ---------------------------------------------------------------------------
// Compliance rule
// ---------------------------------------------------------------------------

export interface ComplianceRule {
  id: string;
  law: string;
  requirement: string;
  description: string;
  applies_to: string[];
  severity: string;
  provision_text: string;
}

// ---------------------------------------------------------------------------
// Consent form
// ---------------------------------------------------------------------------

export interface ConsentForm {
  id: string;
  gap_id: number | null;
  consent_type: string;
  title: string;
  governing_law: string;
  description: string;
  body_text: string;
  required_fields: string[];
  status: string;
  created_at: string;
}

// ---------------------------------------------------------------------------
// Stats
// ---------------------------------------------------------------------------

export interface AgreementStats {
  total: number;
  by_status: Record<string, number>;
  by_type: Record<string, number>;
}

export interface ConsentStats {
  total: number;
  by_type: Record<string, number>;
  by_status: Record<string, number>;
}

// ---------------------------------------------------------------------------
// Compliance validation result
// ---------------------------------------------------------------------------

export interface ComplianceCheck {
  rule_id: string;
  law: string;
  requirement: string;
  severity: string;
  status: "pass" | "fail" | "warning";
  detail: string;
}

export interface ValidationResult {
  agreement_id: string;
  status: string;
  checks: ComplianceCheck[];
  summary: { passed: number; failed: number; warnings: number };
}

// ---------------------------------------------------------------------------
// Generation responses
// ---------------------------------------------------------------------------

export interface GenerateFromGapResponse {
  gap_id: number;
  agreement_types_needed: string[];
  agreements_generated: number;
  agreements: Agreement[];
}

export interface ChecklistItem {
  id: string;
  law: string;
  requirement: string;
  description: string;
  severity: string;
  provision_text: string;
}
