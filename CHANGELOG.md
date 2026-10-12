# Changelog

## [Unreleased]

### Added
- Comprehensive schema definitions for all 18 datasets.
- Validation scripts: validate.py, extract_pdf.py, cross_ref.py, ocr_pdf.py.
- Preflight tool: tools/preflight.py.
- Complete reporting suite.

## [2.0.0] - 2026-10-12

### Added
- `PHASE_2_REPORT.md` summarizing phase 2.
- Cluster A cross-reference section in `CROSS_REF_REPORT.md`.
- Cluster B verification section in `CROSS_REF_REPORT.md`.
- Decisions D-042..D-053 in `DECISIONS_LOG.md`.

### Changed
- `data/dat_04_timing_timeout.yaml` — rewritten with 6 active records and
  23 legacy records; YAML anchor removed; schema-compliant.
- `data/dat_05_state_machine.yaml` — rewritten with 12 active records and
  11 legacy records; schema-compliant; `state_name: OFF` quoted.
- `data/dat_06_init_sequence.yaml` — rewritten with 15 active records and
  10 legacy records; schema-compliant.
- `reports/COVERAGE_MATRIX.md` — regenerated with real record counts.
- `reports/CROSS_REF_REPORT.md` — reconciled L3 count; header note added.
- `reports/VALIDATION_REPORT.md` — regenerated with 0 errors.

### Removed
- YAML anchors (`&id001`) from `data/dat_04_timing_timeout.yaml`.
- Fields not defined in schemas (`coverage_estimate`, `wake_source`, etc.).
- Legacy mixed-source sections from `dat_04`, `dat_05`, `dat_06`.

### Blocked
- `dat_08`, `dat_11`, `dat_15`, `dat_17`, `dat_18`.

### Deferred
- `dat_14`, `dat_16`.


<!-- refresh-20261012054641 -->
## [2026-10-12T05:46:40Z] - Final reconciliation

### Added
- D-057 status rule (>=90% threshold + explicit overrides).
- D-058 Cluster A closure.
- D-059 Cluster B closure.
- D-060 language policy.
- reports/EXTRACTION_TEST.md.

### Changed
- COVERAGE_MATRIX.md, ROLE_MAP.md, README.md, 18 dat_XX_REPORT.md rebuilt.
- Source names normalized (Series_AT -> Series AT).
