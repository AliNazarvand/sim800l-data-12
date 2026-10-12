# Contributing

## Rules

1. Only SIM800L data. No other module data unless explicitly stated.
2. Every record must have a source (name, version, date, page, section).
3. No synthetic data. Use `status: unknown` with `null` values if data is missing.
4. V2.02 takes precedence over V1.00.
5. YAML must be valid UTF-8 without tabs.
6. IDs must be unique: `dat_XX_NNNN`.
7. All datasets must be schema-valid before commit.

## Workflow

1. Update schema first, then data.
2. Run `python scripts/validate.py`.
3. Commit with message: `Complete dat_XX: <description>`.