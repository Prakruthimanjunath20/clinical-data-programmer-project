# Change request CR-002 — fictional protocol amendment

## Request
Protocol version 2 becomes effective on 1 March 2026, adding treatment arm C and visit WEEK12.

## Impact assessment
Review impact on eCRFs and visit/event definitions, treatment-arm configuration, validation/skip logic, exports, scripts, reports, permissions/blinding, user guidance, test evidence, approval records and release notes.

## Build/test/release checklist
1. Confirm the approved amendment and effective date.
2. Update configuration in a controlled test environment.
3. Confirm arms A and B still behave as expected.
4. Confirm arm C is not available before the effective date.
5. Confirm WEEK12 is permitted only under v2.
6. Check historic data and existing reports remain interpretable.
7. Test exports, metrics and permissions.
8. Document defects, retests and approval.
9. Release using authorised procedures and communicate the change.

## Deliberate demo findings
The dataset has an arm C assignment before the effective date and a WEEK12 visit under v1. Investigate them; do not make up the correct values.

This simulates change control only. It is not a validated or approved production change.
