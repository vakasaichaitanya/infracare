-- init.sql for InfraCare PostgreSQL
-- Create tables for users, workers, reports, assignments

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE workers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    capacity INTEGER DEFAULT 5,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TYPE severity_enum AS ENUM ('low','medium','high','critical');
CREATE TYPE status_enum AS ENUM ('pending','in_progress','resolved');

CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    image_url TEXT,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    severity severity_enum NOT NULL,
    status status_enum DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    reporter_id INTEGER REFERENCES users(id)
);

CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    report_id INTEGER REFERENCES reports(id) ON DELETE CASCADE,
    worker_id INTEGER REFERENCES workers(id),
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
