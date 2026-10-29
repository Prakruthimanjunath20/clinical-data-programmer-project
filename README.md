# Mini Adaptive Clinical Trial Data Management Project

## Beginner-friendly, two-day interview-preparation project

**Training only:** all study/data are fictional. This is not Imperial's internal environment, a validated clinical system, or for real patient data.

## What you will build
A small end-to-end data-management workflow for fictional study `SYN-ADAPT-01`: protocol and data dictionary → simulated EDC export → Python validation/QC → issue/query listing → participant listing and site metrics → SQLite staging database → unit tests → mock REST API import → controlled amendment notes. It mirrors the work categories in the Imperial Clinical Data Programmer advert: trial lifecycle, EDC, Python/SQL, validation, QC, reports/listings/metrics, API integration, collaboration/timelines, GCP and data protection.

## Tools
Python 3.10+, pandas, pytest, SQLite (included with Python), terminal/PowerShell, and preferably VS Code.

### Setup (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
If activation is blocked, use Command Prompt and run `.venv\Scripts\activate.bat`.

### Day 1 — understand the workflow
1. Read `docs/01_fictional_protocol.md`, `docs/02_data_management_plan.md`, `docs/03_amendment_change_control.md`, `docs/04_closeout_and_lock_checklist.md`, `docs/data_dictionary.csv`, and `docs/validation_specification.csv`.
2. Inspect the CSVs in `data/`. Some rows deliberately contain errors. Don't guess the correct value and don't auto-fix data.
3. Run `python -m src.pipeline`.
4. Open outputs: `validation_issues.csv`, `participant_listing.csv`, `quality_metrics.csv`, `site_metrics.csv`, and `raw_study_data.sqlite`.
5. For each finding, identify the rule, why it matters, what evidence you need, who to ask, and how to document the resolution.
6. Run `python -m pytest -q` and read `tests/test_pipeline.py`.

### Day 2 — practise amendment control and integration
1. Explain how `data/study_config.csv` changes between protocol versions: arm C and WEEK12 are only available from the fictional v2 effective date.
2. Add one rule (for example, a missed visit should not have an assessment) to `src/pipeline.py` and `docs/validation_specification.csv`; add a matching test.
3. Terminal 1: `python -m src.mock_edc_api_server`
4. Terminal 2: `python -m src.fetch_edc_api`
   This is a local mock API, not a real EDC endpoint. It demonstrates HTTP, JSON payload validation, and conversion to a CSV import.
5. Explain `sql/target_schema.sql`: primary keys, foreign keys, ranges, and why raw imports should be preserved separately from validated outputs.
6. Review `docs/04_closeout_and_lock_checklist.md` and explain what should be checked before data lock and archive.
7. Practise a 90-second walkthrough: study requirement → model/data → checks → query listing → metrics → amendment tests → limitations.

## What the validation script checks
- Participant identifier uniqueness, age range, consent date, and date sequence
- Assignment participant reference, configured arm and effective date
- Visit participant reference, permitted visit/version, completed visit date, possible duplicate visit, and chronology
- Assessment visit reference and fatigue score range
- Completed visit with no assessment (query candidate)

`validation_issues.csv` contains **findings to investigate**, not an instruction to change data. A rule may flag a genuine error or an item needing clarification. Never silently overwrite clinical data.

## Read official system/guidance pages
- Imperial Clinical Data Systems: https://www.imperial.ac.uk/clinical-trials-unit/clinical-data-systems/
- Imperial OpenClinica 4.0: https://www.imperial.ac.uk/clinical-trials-unit/clinical-data-systems/cds-openclinica/
- Imperial REDCap: https://www.imperial.ac.uk/clinical-trials-unit/clinical-data-systems/redcap/
- OpenClinica study-build guide (older v3.1 reference; concepts only): https://docs.openclinica.com/3-1/study-setup/study-setup-build-study/
- ICH GCP: https://www.ema.europa.eu/en/scientific-guidelines/ich-e6-good-clinical-practice

Imperial publicly states it has OpenClinica 4.0 and REDCap available. This project simulates EDC exports because access to Imperial's internal systems is not public. OpenClinica training/account availability may depend on the provider. Don't let access setup block your two-day learning project.

## Interview honesty
Say: “I built a synthetic end-to-end workflow to practise EDC-export validation, QC listings, metrics, amendment control and API patterns.” Do **not** present it as real clinical trial experience or claim that you used Imperial's instance. Production work needs the organisation's validated EDC, SOPs, approved specifications, permissions and formal release procedures.
