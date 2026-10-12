# Validation Report -- sim800l-data

_Last updated: 2026-10-12_

## Status

- **Result:** PASSED
- **Command:** `python scripts/validate.py`

## Output

```
Validation PASSED: all datasets are schema-valid.
```

## Notes

- Level 1: schema validation (jsonschema)
- Level 2: business logic (id uniqueness, source presence, applicable_models)
- Level 3: cross-reference (see reports/CROSS_REF_REPORT.md)
- Level 4: consistency (ISO 8601 timestamps; no example-only/synthetic in data/)