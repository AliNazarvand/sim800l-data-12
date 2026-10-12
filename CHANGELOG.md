# Changelog

_Last updated: 2026-10-12_

## [Unreleased]

### Fixed (v10)
- Classification now uses **dataset source availability** (not record-level status):
  - dat_14 (mcc-mnc.com) and dat_17 (AT Manual) records are **REAL** again
  - dat_04, dat_11 etc. restored to full real counts
- Fixed PowerShell `if/elseif/else` expression bug in `_validation_summary.json`

### Earlier
- v9: record-level status detection (reverted in v10 for over-aggressiveness)
- v8: source.name regex fix; AT command normalization
- v7: 18 dat_XX_REPORT.md regenerated
- v6: Jalali dates converted to Gregorian ISO 8601
- v5: dat_01 (334) and dat_07 (56) restored from oldest backup
- v4: schema restructure; PHASE_*_REPORT preserved