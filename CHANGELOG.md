# Changelog

_Last updated: 2026-10-12_

## [Unreleased]

### Fixed (v9)
- `Get-RecordStats` now reads record-level `status:` — records with `blocked|deferred|unknown|example-only` are documented placeholders, not real
- `cross_ref.py` separates STRICT (defined in dat_01) from SOFT (only mentioned in related_commands)
- Session log numbering fixed

### Earlier
- v8: regex fix for source.name; AT command normalization; 202→0 cross-ref warnings
- v7: 18 dat_XX_REPORT.md regenerated; SOURCE_INVENTORY reflects mcc-mnc.com for dat_14
- v6: Jalali dates converted to Gregorian ISO 8601
- v5: dat_01 (334 records) and dat_07 (56 records) restored from oldest backup
- v4: schema restructure; PHASE_*_REPORT preserved; `example-only` in enum