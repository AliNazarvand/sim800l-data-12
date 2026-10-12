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


## [3.0.0] - 
2026-10-12T06:04:32Z

### Added
- D-065..D-068 in DECISIONS_LOG.md
- 21 new records: 8 timing (dat_04) + 7 states (dat_05) + 6 init steps (dat_06)

### Fixed
- DECISIONS_LOG control characters (U+0008) removed
- _validation_summary.json dat01_status (b -> partial)

### Changed
- README status updated (Phase 3 complete)
- All reports regenerated in English (D-062)

## [3.1.0] - 2026-10-12T06:14:52Z

### Fixed
- REPAIR: unquoted source.date in 21 records (D-069)
- Ratio-Str overload error -> string.Format (D-070)
- Duplicate CHANGELOG/SESSION_LOG entries -> idempotent append (D-071)
- JSON patch timing: post-validate (D-072)

### Added
- D-069..D-072 in DECISIONS_LOG.md
- 5 new records: 3 timing + 1 state + 1 init step

### Changed
- README reflects current status
- All reports regenerated (English, D-062)

## [3.2.0] - 2026-10-12T11:29:52Z

### Fixed
- dat_04_0032 related_state RESET -> POWER_ON (D-073)
- Duplicate [3.0.0] block removed from CHANGELOG
- Duplicate Session v8 block removed from SESSION_LOG

### Added
- scripts/_v10_parse_at_manual.py - best-effort parser
- D-073 in DECISIONS_LOG.md

### Changed
- All reports regenerated (v10)
## [v4.0.0] — 2026-10-12T14:39:53Z

- Reconciliation against reports/DECISIONS_LOG.md (D-042, D-046, D-047, D-049, D-054, D-057, D-058, D-059).
- Real enrichment pass on dat_01 using AT Command Manual V1.01 (parameters/responses/errors/examples).
- Ran scripts/extract_pdf.py, scripts/validate.py, scripts/cross_ref.py.
- Regenerated COVERAGE_MATRIX, ROLE_MAP, TODO, VALIDATION_REPORT, CROSS_REF_REPORT, SOURCE_INVENTORY, GAP_REPORT, README, and all 18 dat_XX_REPORT.md.
- Committed per cluster (A, B, C) and merged to main.