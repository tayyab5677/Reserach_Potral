-- ============================================================
-- University Research Opportunity Portal — Database Schema
-- ============================================================
-- Run this file to create the database and table:
--   mysql -u root -p < schema.sql
-- ============================================================

-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS research_portal
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Switch to the database
USE research_portal;

-- Drop table if it exists (useful for re-running during development)
DROP TABLE IF EXISTS opportunities;

-- Create the opportunities table
CREATE TABLE opportunities (
    id                    INT AUTO_INCREMENT PRIMARY KEY,
    title                 VARCHAR(200)              NOT NULL,
    description           TEXT                      NOT NULL,
    research_area         VARCHAR(100)              NOT NULL,
    faculty_name          VARCHAR(100)              NOT NULL,
    department            VARCHAR(100)              NOT NULL,
    required_skills       VARCHAR(500)              NOT NULL,
    positions_available   INT                       NOT NULL CHECK (positions_available >= 0),
    application_deadline  DATE                      NOT NULL,
    status                ENUM('Open', 'Closed')    NOT NULL DEFAULT 'Open',
    created_at            TIMESTAMP                 DEFAULT CURRENT_TIMESTAMP,
    updated_at            TIMESTAMP                 DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
