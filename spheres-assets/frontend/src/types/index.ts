export interface ParcelSummary {
  parcel_number: string;
  address: string;
  lat: number | null;
  lng: number | null;
  owner_agency: string;
  total_area_sqft: number;
  market_value: number;
  activation_score: number;
  activation_categories: string[];
  vacancy_likely: boolean;
  zoning: string;
}

export interface ParcelFull extends ParcelSummary {
  owner: string;
  category_code: string;
  category_description: string;
  frontage: number;
  depth: number;
  exterior_condition: string;
  year_built: string;
  geographic_ward: string;
  zip_code: string;
  taxable_land: number;
  taxable_building: number;
  exempt_land: number;
  exempt_building: number;
}

export interface ParcelListResponse {
  total: number;
  offset: number;
  limit: number;
  parcels: ParcelSummary[];
}

export interface GeoJSONFeature {
  type: "Feature";
  geometry: { type: "Point"; coordinates: [number, number] };
  properties: {
    id: string;
    address: string;
    owner_agency: string;
    score: number;
    area: number;
    value: number;
    vacancy: boolean;
    zoning: string;
    categories: string[];
  };
}

export interface GeoJSONCollection {
  type: "FeatureCollection";
  features: GeoJSONFeature[];
}

export interface Stats {
  total_parcels: number;
  total_area_sqft: number;
  total_acres: number;
  total_value: number;
  avg_activation_score: number;
  vacant_count: number;
  by_agency: { agency: string; count: number; total_value: number }[];
  by_zoning: { zoning: string; count: number }[];
  by_ward: { ward: string; count: number }[];
}

export interface StaticValue {
  total_value: number;
  total_parcels: number;
  total_area_sqft: number;
  total_acres: number;
  by_agency: Record<string, { count: number; total_value: number; total_area_sqft: number }>;
}

export interface ActivationValue {
  annual_revenue: number;
  by_agency: Record<string, number>;
  by_category: Record<string, number>;
}

export interface LeveragedValue {
  bond_capacity: number;
  tif_potential: number;
  grant_match: number;
  private_investment: number;
  total_leveraged: number;
  annual_activation_revenue: number;
  static_assessed_value: number;
  maintenance_cost_estimate: number;
  net_activation_benefit: number;
}

export interface Filters {
  owner?: string;
  score_min: number;
  score_max: number;
  size_min: number;
  size_max?: number;
  category?: string;
  vacancy?: boolean;
  ward?: string;
  search?: string;
}

export const AGENCY_LABELS: Record<string, string> = {
  city: "City of Philadelphia",
  housing_authority: "Housing Authority",
  land_bank: "Land Bank",
  redevelopment_authority: "Redevelopment Authority",
  school_district: "School District",
  septa: "SEPTA",
  state: "Commonwealth of PA",
  federal: "Federal (GSA)",
  parks: "Fairmount Park",
  pidc: "PIDC",
  penndot: "PennDOT",
  other: "Other",
};

export const CATEGORY_LABELS: Record<string, string> = {
  film: "Film",
  events: "Events",
  pop_up_commercial: "Pop-up Commercial",
  green_garden: "Green / Garden",
  art_installation: "Art Installation",
  recreation: "Recreation",
  general: "General",
};
