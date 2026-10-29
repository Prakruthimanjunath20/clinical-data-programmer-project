# Mini data-management plan (training example)

## Purpose
Define a small workflow for synthetic study data from import through QC and reporting.

## Simplified roles
- Site staff: enter/clarify source data according to study procedures
- Clinical Data Programmer/Data Manager: define checks, run QC, investigate findings, produce listings and metrics, document changes
- Investigator/trial manager: clarify study requirements and approved procedures
- Statistician: advise on variables, outputs and analysis implications
- System administrator: manage access and supported system configuration

## Data handling
- Use only this project's synthetic files.
- Preserve source exports; write findings to `outputs/`.
- Do not guess, impute or silently overwrite participant values.
- Separate raw imports, issue listings and reporting outputs.
- Do not place direct identifiers or free-text health details in outputs.

## Core checks
Uniqueness, referential integrity, ranges, required fields, chronology, protocol-version configuration, completeness, and expected relationships between participants, visits and assessments.

## Query handling
A finding is a query candidate, not automatically a confirmed error. A real process records the source record, rule, date raised, responsible person, response, resolution and closure. Correction happens through the authorised source-system procedure.

## GCP/validation caveat
This project is not validated for clinical use. Real studies require appropriate SOPs, approved specifications, access controls, validation, privacy protection, retention and applicable GCP controls.
