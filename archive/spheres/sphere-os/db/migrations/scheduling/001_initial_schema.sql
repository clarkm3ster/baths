-- SPHERE/OS Scheduling — Initial Schema
-- Sphere, TimeSlice, Booking

BEGIN;

CREATE SCHEMA IF NOT EXISTS scheduling;

-- Enums
CREATE TYPE scheduling.sphere_status AS ENUM (
    'planning', 'construction', 'active_production',
    'legacy_soundstage', 'public_access', 'dormant'
);
CREATE TYPE scheduling.sphere_mode AS ENUM (
    'production', 'public', 'community', 'maintenance'
);
CREATE TYPE scheduling.time_slice_mode AS ENUM (
    'production', 'public', 'community', 'maintenance', 'transition'
);
CREATE TYPE scheduling.booking_status AS ENUM (
    'pending', 'confirmed', 'active', 'completed', 'cancelled'
);

-- Spheres
CREATE TABLE scheduling.spheres (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parcel_id           UUID,
    name                VARCHAR(255) NOT NULL,
    status              scheduling.sphere_status NOT NULL DEFAULT 'planning',
    material_inventory  TEXT[] NOT NULL DEFAULT '{}',
    current_mode        scheduling.sphere_mode NOT NULL DEFAULT 'maintenance',
    base_state          JSONB NOT NULL DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Bookings (created before time_slices so FK works)
CREATE TABLE scheduling.bookings (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id             UUID NOT NULL,
    sphere_id           UUID NOT NULL REFERENCES scheduling.spheres(id) ON DELETE CASCADE,
    material_request    JSONB NOT NULL DEFAULT '{}',
    material_actual     JSONB,
    pricing_usd         DOUBLE PRECISION NOT NULL DEFAULT 0.0,
    status              scheduling.booking_status NOT NULL DEFAULT 'pending',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_bookings_sphere ON scheduling.bookings(sphere_id);
CREATE INDEX idx_bookings_user ON scheduling.bookings(user_id);

-- Time Slices
CREATE TABLE scheduling.time_slices (
    id                          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sphere_id                   UUID NOT NULL REFERENCES scheduling.spheres(id) ON DELETE CASCADE,
    start_time                  TIMESTAMPTZ NOT NULL,
    end_time                    TIMESTAMPTZ NOT NULL,
    mode                        scheduling.time_slice_mode NOT NULL DEFAULT 'public',
    material_config             JSONB NOT NULL DEFAULT '{}',
    transition_buffer_minutes   INTEGER NOT NULL DEFAULT 0,
    booking_id                  UUID REFERENCES scheduling.bookings(id) ON DELETE SET NULL,
    created_at                  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_time_slices_sphere ON scheduling.time_slices(sphere_id);
CREATE INDEX idx_time_slices_start ON scheduling.time_slices(start_time);
CREATE INDEX idx_time_slices_end ON scheduling.time_slices(end_time);
CREATE INDEX idx_time_slices_booking ON scheduling.time_slices(booking_id);

COMMIT;
