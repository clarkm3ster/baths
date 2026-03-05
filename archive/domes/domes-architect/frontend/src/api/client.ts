import type { CoordinationModel, Architecture, ModelScore, ComparisonSet } from "../types";

async function fetchJSON<T>(url: string, options?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export const getModels = () => fetchJSON<CoordinationModel[]>("/api/models");
export const getModel = (id: number) => fetchJSON<CoordinationModel>(`/api/models/${id}`);
export const getModelsByCategory = (cat: string) => fetchJSON<CoordinationModel[]>(`/api/models/category/${cat}`);
export const compareModels = (ids: number[]) =>
  fetchJSON<{ models: CoordinationModel[]; comparison_dimensions: string[] }>(`/api/models/compare/${ids.join(",")}`);

export const getArchitectures = () => fetchJSON<Architecture[]>("/api/architectures");
export const getArchitecture = (id: number) => fetchJSON<Architecture>(`/api/architectures/${id}`);
export const generateArchitecture = (constraints: Record<string, unknown>) =>
  fetchJSON<Architecture>("/api/architectures/generate", { method: "POST", body: JSON.stringify(constraints) });
export const recommendModels = (constraints: Record<string, unknown>) =>
  fetchJSON<{ recommendations: ModelScore[] }>("/api/architectures/recommend", { method: "POST", body: JSON.stringify(constraints) });
export const updateArchitectureStatus = (id: number, status: string) =>
  fetchJSON<Architecture>(`/api/architectures/${id}/status`, { method: "PUT", body: JSON.stringify({ status }) });
export const deleteArchitecture = (id: number) =>
  fetchJSON<{ deleted: number }>(`/api/architectures/${id}`, { method: "DELETE" });
export const createComparison = (name: string, ids: number[]) =>
  fetchJSON<ComparisonSet & { architectures: Architecture[] }>("/api/architectures/compare", {
    method: "POST",
    body: JSON.stringify({ name, architecture_ids: ids }),
  });
export const exportArchitecture = (id: number) => fetchJSON<Architecture>(`/api/architectures/export/${id}`);
