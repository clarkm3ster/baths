import type {
  Agreement,
  AgreementStats,
  ChecklistItem,
  ComplianceRule,
  ConsentForm,
  ConsentStats,
  Gap,
  GenerateFromGapResponse,
  Template,
  ValidationResult,
} from "../types";

// ---------------------------------------------------------------------------
// Generic fetch helper
// ---------------------------------------------------------------------------

async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    ...init,
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`${res.status} ${res.statusText}: ${text}`);
  }
  return res.json() as Promise<T>;
}

// ---------------------------------------------------------------------------
// Gaps (from domes-datamap via proxy)
// ---------------------------------------------------------------------------

export async function getGaps(): Promise<Gap[]> {
  return fetchJSON<Gap[]>("/datamap-api/gaps");
}

export async function getGap(id: number): Promise<Gap> {
  return fetchJSON<Gap>(`/datamap-api/gaps/${id}`);
}

// ---------------------------------------------------------------------------
// Agreements
// ---------------------------------------------------------------------------

export async function getAgreements(filters?: {
  status?: string;
  agreement_type?: string;
  gap_id?: number;
}): Promise<{ count: number; agreements: Agreement[] }> {
  const params = new URLSearchParams();
  if (filters?.status) params.set("status", filters.status);
  if (filters?.agreement_type) params.set("agreement_type", filters.agreement_type);
  if (filters?.gap_id !== undefined) params.set("gap_id", String(filters.gap_id));
  const qs = params.toString();
  return fetchJSON(`/api/agreements${qs ? `?${qs}` : ""}`);
}

export async function getAgreement(id: string): Promise<Agreement> {
  return fetchJSON<Agreement>(`/api/agreements/${id}`);
}

export async function generateFromGap(gapId: number): Promise<GenerateFromGapResponse> {
  return fetchJSON<GenerateFromGapResponse>(`/api/agreements/from-gap/${gapId}`, {
    method: "POST",
  });
}

export async function generateAgreement(body: {
  template_id: string;
  party_a_name: string;
  party_b_name: string;
  state?: string;
  gap_id?: number | null;
  system_a_id?: string;
  system_b_id?: string;
  barrier_description?: string;
  barrier_law?: string;
  barrier_type?: string;
  impact?: string;
  what_it_would_take?: string;
  consent_closable?: boolean;
}): Promise<Agreement> {
  return fetchJSON<Agreement>("/api/agreements/generate", {
    method: "POST",
    body: JSON.stringify(body),
  });
}

export async function updateAgreementStatus(
  id: string,
  status: string
): Promise<Agreement> {
  return fetchJSON<Agreement>(`/api/agreements/${id}/status`, {
    method: "PATCH",
    body: JSON.stringify({ status }),
  });
}

export async function getAgreementStats(): Promise<AgreementStats> {
  return fetchJSON<AgreementStats>("/api/agreements/stats");
}

export async function getAgreementsForGap(
  gapId: number
): Promise<{ gap_id: number; count: number; agreements: Agreement[] }> {
  return fetchJSON(`/api/agreements/for-gap/${gapId}`);
}

// ---------------------------------------------------------------------------
// Templates
// ---------------------------------------------------------------------------

export async function getTemplates(): Promise<{
  count: number;
  templates: Template[];
}> {
  return fetchJSON("/api/agreements/templates");
}

export async function getTemplate(id: string): Promise<Template> {
  return fetchJSON<Template>(`/api/agreements/templates/${id}`);
}

// ---------------------------------------------------------------------------
// Compliance
// ---------------------------------------------------------------------------

export async function validateAgreement(
  agreementId: string
): Promise<ValidationResult> {
  return fetchJSON<ValidationResult>(
    `/api/compliance/validate/${agreementId}`,
    { method: "POST" }
  );
}

export async function validateAllUnchecked(): Promise<{
  agreements_checked: number;
  valid: number;
  issues_found: number;
  total_checks: { passed: number; failed: number; warnings: number };
  results: ValidationResult[];
}> {
  return fetchJSON("/api/compliance/validate-all", { method: "POST" });
}

export async function getComplianceRules(filters?: {
  law?: string;
  agreement_type?: string;
}): Promise<{ count: number; rules: ComplianceRule[] }> {
  const params = new URLSearchParams();
  if (filters?.law) params.set("law", filters.law);
  if (filters?.agreement_type) params.set("agreement_type", filters.agreement_type);
  const qs = params.toString();
  return fetchJSON(`/api/compliance/rules${qs ? `?${qs}` : ""}`);
}

export async function getChecklist(
  type: string
): Promise<{ agreement_type: string; count: number; checklist: ChecklistItem[] }> {
  return fetchJSON(`/api/compliance/checklist/${type}`);
}

// ---------------------------------------------------------------------------
// Consent
// ---------------------------------------------------------------------------

export async function getConsentForms(filters?: {
  gap_id?: number;
  consent_type?: string;
  status?: string;
}): Promise<{ count: number; forms: ConsentForm[] }> {
  const params = new URLSearchParams();
  if (filters?.gap_id !== undefined) params.set("gap_id", String(filters.gap_id));
  if (filters?.consent_type) params.set("consent_type", filters.consent_type);
  if (filters?.status) params.set("status", filters.status);
  const qs = params.toString();
  return fetchJSON(`/api/consent/forms${qs ? `?${qs}` : ""}`);
}

export async function getConsentForm(id: string): Promise<ConsentForm> {
  return fetchJSON<ConsentForm>(`/api/consent/forms/${id}`);
}

export async function getConsentForGap(
  gapId: number
): Promise<{ gap_id: number; count: number; forms: ConsentForm[] }> {
  return fetchJSON(`/api/consent/for-gap/${gapId}`);
}

export async function getConsentStats(): Promise<ConsentStats> {
  return fetchJSON<ConsentStats>("/api/consent/stats");
}

// ---------------------------------------------------------------------------
// Gap coverage + batch + export
// ---------------------------------------------------------------------------

export async function getGapCoverage(): Promise<Record<number, string>> {
  return fetchJSON<Record<number, string>>("/api/agreements/gap-coverage");
}

export async function batchGenerate(
  circumstances: string[]
): Promise<{
  gaps_matched: number;
  gaps_skipped_existing: number;
  agreements_generated: number;
  agreements: Agreement[];
}> {
  return fetchJSON("/api/agreements/batch-generate", {
    method: "POST",
    body: JSON.stringify({ circumstances }),
  });
}

export function getExportUrl(agreementId: string): string {
  return `/api/agreements/${agreementId}/export`;
}
