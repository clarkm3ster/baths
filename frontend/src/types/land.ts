// Generated from sphere-os/src/land/models.py

export interface ParcelRecord {
  id: string;
  source: string;
  external_id: string;
  geometry: GeoJSON.Polygon | null;
  centroid: { lat: number; lng: number } | null;
  ownership_type: string | null;
  owner_name: string | null;
  area_sqft: number | null;
  street_frontage_ft: number | null;
  zoning: string | null;
  vacancy_score: number | null;
  vacant_building_count: number;
  vacant_land_indicator: boolean;
  last_activity_date: string | null;
  census_block_group: string | null;
  transit_proximity_ft: number | null;
  environmental_flags: string[];
  sphere_viability_score: number | null;
  sphere_viability_updated_at: string | null;
  status: string;
  activated_at: string | null;
  cluster_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface ParcelCluster {
  id: string;
  geometry: GeoJSON.MultiPolygon | null;
  total_area_sqft: number;
  parcel_count: number;
  avg_viability_score: number;
  created_at: string;
  updated_at: string;
  parcels: ParcelRecord[];
}

export interface GeoJSONPolygon {
  type: "Polygon";
  coordinates: number[][][];
}

export interface GeoJSONMultiPolygon {
  type: "MultiPolygon";
  coordinates: number[][][][];
}

// eslint-disable-next-line @typescript-eslint/no-namespace
declare namespace GeoJSON {
  type Polygon = GeoJSONPolygon;
  type MultiPolygon = GeoJSONMultiPolygon;
}
