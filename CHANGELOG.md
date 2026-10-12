# Changelog

## [Unreleased]

### Added

- Initial project structure: 18 schemas, 18 data files, 4 scripts
- Base reports and documentation
- CI workflow for schema validation
- Dataset-specific schemas for all 18 datasets
- 4-level validation in `validate.py`
- Real cross-reference checks in `cross_ref.py`
- Column detection in `extract_pdf.py`
- Scanned-PDF detection in `ocr_pdf.py`

### Fixed

- AT Command Manual V1.01 now correctly reported as AVAILABLE
- COVERAGE_MATRIX no longer contains `pending` status (R22)
- Schema enums include `example-only` (R21)
- Preserved PHASE_*_REPORT.md and _v*_FINAL_REPORT.md (previously deleted by mistake)