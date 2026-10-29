-- Illustrative relational target schema only. Training—not a production clinical system.
PRAGMA foreign_keys = ON;
CREATE TABLE participants (
  participant_id TEXT PRIMARY KEY,
  site_id TEXT NOT NULL,
  age_years INTEGER NOT NULL CHECK (age_years BETWEEN 18 AND 100),
  consent_date TEXT NOT NULL,
  enrolment_date TEXT NOT NULL CHECK (enrolment_date >= consent_date)
);
CREATE TABLE treatment_assignments (
  assignment_id TEXT PRIMARY KEY,
  participant_id TEXT NOT NULL REFERENCES participants(participant_id),
  arm_code TEXT NOT NULL,
  assignment_date TEXT NOT NULL,
  protocol_version INTEGER NOT NULL
);
CREATE TABLE visits (
  visit_id TEXT PRIMARY KEY,
  participant_id TEXT NOT NULL REFERENCES participants(participant_id),
  visit_type TEXT NOT NULL,
  planned_date TEXT NOT NULL,
  actual_date TEXT,
  visit_status TEXT NOT NULL CHECK (visit_status IN ('completed','missed','scheduled')),
  protocol_version INTEGER NOT NULL
);
CREATE TABLE assessments (
  assessment_id TEXT PRIMARY KEY,
  visit_id TEXT NOT NULL REFERENCES visits(visit_id),
  fatigue_score INTEGER NOT NULL CHECK (fatigue_score BETWEEN 0 AND 10)
);
-- In a real adaptive study, protocol configurations, audit history and release controls
-- would need a validated platform-specific implementation.
