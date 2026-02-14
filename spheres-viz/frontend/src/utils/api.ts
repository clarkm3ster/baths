// ---------------------------------------------------------------------------
// SPHERES Viz — API Client
// ---------------------------------------------------------------------------

const API_BASE = '/api';

// ---------------------------------------------------------------------------
// Types — mirrors the FastAPI / Pydantic models on the backend
// ---------------------------------------------------------------------------

/** Spatial coordinates for a Philadelphia location. */
export interface Coordinates {
  lat: number;
  lng: number;
}

/** A single design principle or concept for the episode. */
export interface DesignPrinciple {
  title: string;
  description: string;
}

/** Program element describing a functional component of the space. */
export interface ProgramElement {
  name: string;
  description: string;
  area_sqft?: number;
}

/** Configuration for the 3D world tied to an episode. */
export interface WorldConfig {
  scene_type: string;
  primary_color: string;
  secondary_color: string;
  accent_color: string;
  ambient_sound?: string;
  fog_density?: number;
  camera_height?: number;
}

/** Compact episode data returned by the list endpoint. */
export interface EpisodeSummary {
  slug: string;
  episode_number: number;
  title: string;
  subtitle: string;
  genre: string;
  location_name: string;
  neighborhood: string;
  color: string;
  tagline: string;
  status: 'dormant' | 'activated';
}

/** Full episode payload returned by the detail endpoint. */
export interface Episode {
  slug: string;
  episode_number: number;
  title: string;
  subtitle: string;
  genre: string;
  location_name: string;
  address: string;
  neighborhood: string;
  coordinates: Coordinates;
  color: string;
  tagline: string;
  description: string;
  current_state: string;
  vision: string;
  design_principles: DesignPrinciple[];
  program_elements: ProgramElement[];
  world_config: WorldConfig;
  status: 'dormant' | 'activated';
  square_footage?: number;
  year_dormant?: number;
}

/** Aggregate statistics across all episodes. */
export interface Stats {
  total_episodes: number;
  total_square_footage: number;
  neighborhoods: string[];
  genres: string[];
  dormant_count: number;
  activated_count: number;
}

// ---------------------------------------------------------------------------
// Fetchers
// ---------------------------------------------------------------------------

/** Fetch the summary list of all episodes. */
export async function fetchEpisodes(): Promise<EpisodeSummary[]> {
  const res = await fetch(`${API_BASE}/episodes`);
  if (!res.ok) throw new Error('Failed to fetch episodes');
  return res.json();
}

/** Fetch the full detail for a single episode by slug. */
export async function fetchEpisode(slug: string): Promise<Episode> {
  const res = await fetch(`${API_BASE}/episodes/${slug}`);
  if (!res.ok) throw new Error('Failed to fetch episode');
  return res.json();
}

/** Fetch aggregate stats for all episodes. */
export async function fetchStats(): Promise<Stats> {
  const res = await fetch(`${API_BASE}/episodes/stats`);
  if (!res.ok) throw new Error('Failed to fetch stats');
  return res.json();
}
