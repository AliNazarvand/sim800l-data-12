# Changelog

All notable changes to this repository are documented here.
Format: [SemVer](https://semver.org/).

## [v0.1.0] — Initial skeleton
- Repository skeleton, tools, docs, LICENSE, NOTICE.

## [v0.2.0] — Source PDFs downloaded
- Added `sources/SIM800L_Hardware_Design_V1.00.pdf` and
  `sources/SIM800H&SIM800L_Hardware_Design_V2.02.PDF`.
- Added `tools/preflight.py`.

## [v0.3.0] — Text extraction
- Added `sources/extracted/v1.00.txt`, `sources/extracted/v2.02.txt` and
  per-page files.

## [v0.4.0] — Add dat_07 (Hardware Reference DB, 80 records)
- 50 records in `pinout.yaml`.
- 10 records in `electrical.yaml`.
- 10 records in `power_consumption.yaml`.
- 9 records in `interfaces.yaml`.
- 1 record in `physical.yaml`.
- Added `schemas/dat_07.schema.json`.
- Added `_dataset_meta.yaml` (status: partial).

## [v0.5.0] — Add dat_04 (Timing & Timeout DB, 11 records)
- 11 records in `timing.yaml`.
- Added `schemas/dat_04.schema.json`.
- Added `_dataset_meta.yaml` (status: complete).

## [v0.6.0] — Add dat_15 (Power Management DB, 4 records)
- 4 records in `power_modes.yaml`.
- Added `schemas/dat_15.schema.json`.
- Added `_dataset_meta.yaml` (status: partial).

## [v0.7.0] — Add dat_05 (State Machine DB, 19 records)
- 7 states + 12 transitions.
- Added `schemas/dat_05.schema.json`.
- Added `_dataset_meta.yaml` (status: complete).

## [v0.8.0] — Add dat_06 (Init Sequence DB, 5 records)
- 5 records in `hardware_init.yaml`.
- Added `schemas/dat_06.schema.json`.
- Added `_dataset_meta.yaml` (status: complete).

## [v0.9.0] — dat_16 deferred
- `data/board_evb/boards.yaml` empty.
- `_dataset_meta.yaml` (status: deferred, reason: INSUFFICIENT_RECORDS).

## [v1.0.0] — Phase 1 stable
- Filled `docs/source_mapping.md`, `docs/conflict_log.md`,
  `docs/diagram_mapping.md`.
- Added `raw/*_extract.md` and `raw/*_diagrams.md`.
- Final `PHASE_1_REPORT.md`.
- Final `README.md`.