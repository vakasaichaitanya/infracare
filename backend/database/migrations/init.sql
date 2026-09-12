-- Migration script for InfraCare backend schema
-- Location: backend/database/migrations/init.sql

-- Table: users (already created by SQLAlchemy) - no changes needed here.

-- Table: reports
ALTER TABLE reports ADD COLUMN IF NOT EXISTS priority_reason TEXT;

-- Indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_reports_lat_lng ON reports (latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_reports_category ON reports (category);
CREATE INDEX IF NOT EXISTS idx_reports_status ON reports (status);
CREATE INDEX IF NOT EXISTS idx_reports_priority ON reports (priority);

-- Optional: GIST index for geographic distance (PostgreSQL specific, placeholder for future DB)
-- CREATE EXTENSION IF NOT EXISTS postgis;
-- CREATE INDEX IF NOT EXISTS idx_reports_location_gist ON reports USING GIST (ST_MakePoint(latitude, longitude));
