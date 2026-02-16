/** Types for the World Labs Marble integration. */

export interface MarbleWorld {
  key: string;
  title: string;
  prompt: string;
  worldId: string;
  operationId: string;
  details: Record<string, unknown>;
  splatUrl: string;
  fallback?: boolean;
}

export interface MarbleWorldsResponse {
  worlds: MarbleWorld[];
}
