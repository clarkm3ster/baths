-- SPHERE/OS Productions — Initial Schema

BEGIN;

CREATE SCHEMA IF NOT EXISTS productions;

CREATE TABLE productions.production_proposals (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parcel_id                   UUID NOT NULL,
    title                       TEXT NOT NULL,
    logline                     TEXT NOT NULL,
    genre                       VARCHAR(32) NOT NULL,
    format                      VARCHAR(32) NOT NULL,
    narrative_concept           TEXT NOT NULL,
    material_script             JSONB NOT NULL DEFAULT '[]',
    min_area_sqft               DOUBLE PRECISION NOT NULL,
    required_utilities          TEXT[] NOT NULL DEFAULT '{}',
    crew_size_estimate          INTEGER NOT NULL,
    estimated_budget_low_usd    INTEGER NOT NULL,
    estimated_budget_high_usd   INTEGER NOT NULL,
    production_timeline_weeks   INTEGER NOT NULL,
    legacy_modes                TEXT[] NOT NULL DEFAULT '{}',
    generated_by_model          VARCHAR(64) NOT NULL,
    creative_brief              TEXT,
    generated_at                TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    parent_proposal_id          UUID,
    iteration_feedback          TEXT
);

CREATE INDEX idx_proposals_parcel ON productions.production_proposals(parcel_id);
CREATE INDEX idx_proposals_genre ON productions.production_proposals(genre);
CREATE INDEX idx_proposals_format ON productions.production_proposals(format);

COMMIT;
