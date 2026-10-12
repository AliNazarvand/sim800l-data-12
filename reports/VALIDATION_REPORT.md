# VALIDATION_REPORT.md

Generated: 2026-10-12T06:14:52Z

## Levels

- L1: JSON-Schema conformance
- L2: Business logic
- L3: Cross-reference
- L4: Consistency

## Result of scripts/validate.py

``````text
Validation: 1 errors (L1=0 L2=0 L3=1 L4=0)
dat_01 status=b  cross-ref ran=True  specialist_whitelist=46
``````

## Error count: 1

- dat_04 L3 dat_04_0032 -- related_state RESET not in dat_05

## Notes

- _validation_summary.json is patched in v9 BLOCK 7 (post-validate).
- This report is English-only per D-062.
