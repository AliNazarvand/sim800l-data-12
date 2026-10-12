# Changelog -- sim800l-data (reports)

_Last updated: 2026-10-12_

## [Unreleased]

### Added
- Initial infrastructure: 18 schemas, 18 data placeholders (v1)
- Base reports: COVERAGE_MATRIX, SOURCE_INVENTORY, GAP_REPORT, TODO, ROLE_MAP (v1)
- DECISIONS_LOG, SESSION_LOG, VALIDATION_REPORT, CROSS_REF_REPORT (v1)
- Diagnostic tool `diagnose_sources.py` (v5)
- 18 `dat_XX_REPORT.md` regenerated (v7)

### Changed
- All reports now derived from single status source (v6, D-009)
- Real vs placeholder counting (v6, D-008)
- All Jalali dates converted to Gregorian ISO 8601 (v6, D-010)
- SOURCE_INVENTORY reflects external mcc-mnc.com for dat_14 (v7)