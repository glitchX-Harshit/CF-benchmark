-- init.sql
-- Initial database setup for CF Benchmark

-- Ensure the user exists (though Docker compose sets this up)
-- CREATE USER cfbench WITH PASSWORD 'cfbench';

-- Create database (Docker compose handles this for POSTGRES_DB)
-- CREATE DATABASE cfbench OWNER cfbench;

\c cfbench;

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- We rely on Alembic (SQLAlchemy migrations) to create tables, 
-- but we can put shared schemas or initial foundational tables here if needed.

CREATE SCHEMA IF NOT EXISTS benchmarks;

-- Example initial table
CREATE TABLE IF NOT EXISTS benchmarks.health (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO benchmarks.health (status) VALUES ('healthy') ON CONFLICT DO NOTHING;
