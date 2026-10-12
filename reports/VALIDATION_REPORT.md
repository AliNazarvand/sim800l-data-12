# Validation Report -- sim800l-data

_Last updated: 2026-10-12_

## validate.py output

```
Validation PASSED: all datasets are schema-valid.
```

## Notes

- If errors reference `additionalProperties`, some real records have fields not yet declared in the schema.
- If errors reference `example-only`, remove those records (R21 violation).