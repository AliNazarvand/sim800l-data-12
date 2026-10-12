# Changelog

_Last updated: 2026-10-12_

## [Unreleased]

### Fixed (v8)
- `Get-RecordStats` now reads `source.name` from within the `source:` block (fixes 59-record regression in dat_01)
- `cross_ref.py` normalizes AT commands (AT+X / +X / X treated as same)
- `_validation_summary.json` now includes `cross_ref_issues` field

### Earlier
- v7: 18 dat_XX_REPORT.md regenerated; SOURCE_INVENTORY lists mcc-mnc.com for dat_14
- v6: Jalali dates converted to Gregorian ISO 8601; reports derived from single status source
- v5: dat_01 (334 records) and dat_07 (56 records) restored from oldest backup
- v4: schema restructure; PHASE_*_REPORT preserved; `example-only` in enum