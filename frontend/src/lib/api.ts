/**
 * Typed API client for the DOMES FastAPI backend.
 *
 * All requests go through the Next.js rewrite proxy:
 *   /api/* → http://localhost:8003/api/*
 */
import type {
  FullPacket,
  StudioDashboard,
  CharacterProfile,
  Production,
  GapItem,
  BacklogView,
  IPAsset,
  LearningPackage,
  CliffGuard,
  BondPricing,
  SettlementContract,
} from "@/types";

const BASE = "/api";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`API ${res.status}: ${detail}`);
  }
  return res.json();
}

async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`API ${res.status}: ${detail}`);
  }
  return res.json();
}

// ── Full Packet (primary person view) ───────────────────────────

export function getFullPacket(personId: string) {
  return get<FullPacket>(`/layers/full_packet/${personId}`);
}

export function listPersons() {
  return get<{ persons: { id: string; name: string; key: string }[] }>(
    "/layers/full_packet"
  );
}

// ── Studio ──────────────────────────────────────────────────────

export function getStudioDashboard() {
  return get<StudioDashboard>("/studio/dashboard");
}

export function listCharacters() {
  return get<CharacterProfile[]>("/studio/characters");
}

export function getCharacter(characterId: string) {
  return get<CharacterProfile>(`/studio/characters/${characterId}`);
}

export function listProductions() {
  return get<Production[]>("/studio/productions");
}

export function getProduction(productionId: string) {
  return get<Production>(`/studio/productions/${productionId}`);
}

export function getProductionGaps(productionId: string) {
  return get<GapItem[]>(`/studio/productions/${productionId}/gaps`);
}

export function getBacklog(productionId: string) {
  return get<BacklogView>(`/studio/productions/${productionId}/backlog`);
}

export function getProductionAssets(productionId: string) {
  return get<IPAsset[]>(`/studio/productions/${productionId}/assets`);
}

export function getProductionLearnings(productionId: string) {
  return get<LearningPackage[]>(
    `/studio/productions/${productionId}/learning-packages`
  );
}

export function getProductionFinancials(productionId: string) {
  return get<Record<string, unknown>>(
    `/studio/productions/${productionId}/financials`
  );
}

export function seedScenarios() {
  return post<{ status: string; characters: number }>(
    "/studio/seed-scenarios",
    {}
  );
}

// ── Layer-specific endpoints ────────────────────────────────────

export function postCliffGuard(
  personId: string,
  benefits: Record<string, number>,
  earnedIncome: number
) {
  return post<CliffGuard>("/layers/treasury/cliff-guard", {
    person_id: personId,
    benefits,
    earned_income: earnedIncome,
  });
}

export function postTrialDesign(params: {
  person_id: string;
  hypothesis: string;
  intervention: string;
  control: string;
  metric_name: string;
}) {
  return post<{ trial_id: string }>("/layers/bio/trials", params);
}

// ── Demo / Scenarios ────────────────────────────────────────────

export function getDemoAll() {
  return get<{
    scenarios: Record<string, FullPacket>;
    bond_pool: {
      bond: Record<string, unknown>;
      pricing: BondPricing;
      contracts: SettlementContract[];
    };
  }>("/layers/demo");
}

// ── Health check ────────────────────────────────────────────────

export function healthCheck() {
  return get<{ status: string; app: string; port: number }>("/health");
}
