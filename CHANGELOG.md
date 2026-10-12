# Changelog

_Last updated: 2026-10-12_

## [Unreleased]

### Added

- Dataset-specific schemas for all 18 datasets (v3)
- 4-level validation in `validate.py` (v3)
- Real cross-reference checks in `cross_ref.py` (v3)
- Column detection in `extract_pdf.py` (v3)
- Scanned-PDF detection in `ocr_pdf.py` (v3)
- Diagnostic tool `diagnose_sources.py` (v5)
- Real vs placeholder record counting (v6)

### Fixed

- AT Command Manual V1.01 correctly reported as available (v4)
- COVERAGE_MATRIX no longer contains `pending` status (v4, R22)
- Schema enums include `example-only` (v4, R21)
- PHASE_*_REPORT and _v*_FINAL_REPORT preserved (v4)
- dat_01 (334 records) restored from oldest backup (v5)
- dat_07 (56 records) restored from oldest backup (v5)
- All Jalali (1405-*) dates converted to Gregorian ISO 8601 (v6)
- GAP_REPORT, TODO, COVERAGE_MATRIX now derived from single status source (v6)
- Cross-reference report regenerated and logged (v7)
- SOURCE_INVENTORY reflects external mcc-mnc.com for dat_14 (v7)
- All 18 reports/dat_XX_REPORT.md generated with real counts (v7)
- ROLE_MAP.md regenerated with current statuses (v7)
- Placeholder detection improved (unknown version/date excluded) (v7)