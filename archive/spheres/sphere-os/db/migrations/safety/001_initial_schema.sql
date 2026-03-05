-- SPHERE/OS Safety Monitoring — Initial Schema

BEGIN;

CREATE SCHEMA IF NOT EXISTS safety;

CREATE TABLE safety.safety_events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sphere_id       UUID NOT NULL,
    timestamp       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    system_type     VARCHAR(64) NOT NULL,
    severity        VARCHAR(16) NOT NULL,
    parameter       VARCHAR(64) NOT NULL,
    value           DOUBLE PRECISION NOT NULL,
    threshold       DOUBLE PRECISION NOT NULL,
    resolved        BOOLEAN NOT NULL DEFAULT FALSE,
    resolved_at     TIMESTAMPTZ,
    acknowledged    BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_safety_events_sphere ON safety.safety_events(sphere_id);
CREATE INDEX idx_safety_events_severity ON safety.safety_events(severity);
CREATE INDEX idx_safety_events_timestamp ON safety.safety_events(timestamp DESC);

COMMIT;
