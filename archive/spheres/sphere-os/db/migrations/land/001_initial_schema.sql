-- SPHERE/OS Land Intelligence Engine — Initial Schema
-- Requires: PostGIS extension enabled on the database
-- Schema: land

BEGIN;

-- Ensure PostGIS is available
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create land schema
CREATE SCHEMA IF NOT EXISTS land;

-- =============================================================================
-- ParcelCluster: groups of spatially adjacent vacant parcels
-- =============================================================================
CREATE TABLE land.parcel_clusters (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    geometry        GEOMETRY(MULTIPOLYGON, 4326) NOT NULL,
    total_area_sqft DOUBLE PRECISION NOT NULL DEFAULT 0,
    parcel_count    INTEGER NOT NULL DEFAULT 0,
    avg_viability_score DOUBLE PRECISION NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_parcel_clusters_geometry ON land.parcel_clusters USING GIST (geometry);

-- =============================================================================
-- ParcelRecord: individual land parcels discovered from public data sources
-- =============================================================================
CREATE TABLE land.parcels (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source                  VARCHAR(64) NOT NULL,
    external_id             VARCHAR(128) NOT NULL,
    geometry                GEOMETRY(POLYGON, 4326),
    centroid                GEOMETRY(POINT, 4326),

    -- Ownership
    ownership_type          VARCHAR(64),
    owner_name              VARCHAR(256),

    -- Physical
    area_sqft               DOUBLE PRECISION,
    street_frontage_ft      DOUBLE PRECISION,

    -- Zoning & Vacancy
    zoning                  VARCHAR(32),
    vacancy_score           DOUBLE PRECISION CHECK (vacancy_score >= 0 AND vacancy_score <= 1),
    vacant_building_count   INTEGER DEFAULT 0,
    vacant_land_indicator   BOOLEAN DEFAULT FALSE,
    last_activity_date      DATE,

    -- Context
    census_block_group      VARCHAR(32),
    transit_proximity_ft    DOUBLE PRECISION,
    environmental_flags     TEXT[] DEFAULT '{}',

    -- Sphere viability (computed)
    sphere_viability_score      DOUBLE PRECISION CHECK (sphere_viability_score >= 0 AND sphere_viability_score <= 1),
    sphere_viability_updated_at TIMESTAMPTZ,

    -- Status
    status                  VARCHAR(32) NOT NULL DEFAULT 'discovered',
    activated_at            TIMESTAMPTZ,

    -- Cluster relationship
    cluster_id              UUID REFERENCES land.parcel_clusters(id) ON DELETE SET NULL,

    -- Timestamps
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Uniqueness: one record per source + external_id pair
    CONSTRAINT uq_parcels_source_external UNIQUE (source, external_id)
);

-- Spatial indexes
CREATE INDEX idx_parcels_geometry ON land.parcels USING GIST (geometry);
CREATE INDEX idx_parcels_centroid ON land.parcels USING GIST (centroid);

-- Query indexes
CREATE INDEX idx_parcels_source ON land.parcels (source);
CREATE INDEX idx_parcels_viability ON land.parcels (sphere_viability_score DESC NULLS LAST);
CREATE INDEX idx_parcels_area ON land.parcels (area_sqft);
CREATE INDEX idx_parcels_status ON land.parcels (status);
CREATE INDEX idx_parcels_cluster ON land.parcels (cluster_id);
CREATE INDEX idx_parcels_zoning ON land.parcels (zoning);

COMMIT;
