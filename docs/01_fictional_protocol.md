# Protocol summary — SYN-ADAPT-01 (fictional)

## Purpose
A training-only example for learning data management; not real research and not intended to support a medical claim.

## Study
- Study ID: SYN-ADAPT-01; sites SITE-01 and SITE-02
- Participant identifiers such as P001; no names, addresses, date of birth or contact details
- Outcome: fictional participant-reported fatigue score, integer 0–10
- All records are synthetic.

## Protocol version 1
- Treatment arms: A and B
- Planned visits: BASELINE, WEEK4, WEEK8

## Approved fictional amendment — version 2
Effective 1 March 2026:
- Add arm C for assignments from the effective date
- Add a WEEK12 visit
- Do not retrospectively change the version of old visits or silently modify old records

## Simplified data flow
Site enters data in an EDC → EDC applies edit checks and tracks changes → an export is supplied to data management → Python QC checks the export → issue/query listing is reviewed → authorised correction is made through approved EDC procedures → validated extract/listings/metrics go to authorised users.

This project simulates the export/QC stage. It does not replace eCRF entry, source-data verification or a validated EDC.
