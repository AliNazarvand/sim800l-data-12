# Changelog

All notable changes to the SIM800L-Data project.

## [2026-10-10] — Final Alignment

### Added
- `reports/COVERAGE_FINAL.md` — single source of truth for dataset status.
- Section 20 self-check report (`reports/FINAL_SELF_CHECK.md`).

### Fixed
- `data/state_machine/_dataset_meta.yaml` — status corrected to `partial`
  (was incorrectly `complete`).
- `data/init_sequence/_dataset_meta.yaml` — status corrected to `partial`.
- `data/hardware/_dataset_meta.yaml` — status corrected to `partial`.
- `COVERAGE_MATRIX.md` — synced with `COVERAGE_FINAL.md`.
- `README.md` — reflects final project state.

### Documentation
- DECISIONS_LOG.md: D-C1-001 (reconciliation), D-C2-001 (self-check).

## [2026-10-10] — C1: Final Reconciliation

### Added
- `reports/COVERAGE_FINAL.md`.
- DECISIONS_LOG.md entry D-C1-001.

### Fixed
- `reports/COVERAGE_REALITY.md` — `dat_04` and `dat_15` correctly marked
  `complete` (the B1 Final script had incorrectly marked them `partial`).

## [2026-10-10] — B1 Final: Rollback of A1 Auto-Extraction

### Removed
- 60 garbage records added by regex-based auto-extraction from flattened
  PDF text (see D-B1-001 for full reason).
- Files: `esd_characteristics.yaml`, `absolute_maximum.yaml`,
  `operating_frequencies.yaml`.

### Changed
- Restored `data/` from `_backup_extract_20261010_160808`.
- Archived `scripts/_extract_a1.py` → `scripts/archive/_extract_a1.py.failed`.

## [2026-10-10] — A3: Deprecate tools/validate.py

### Changed
- `tools/validate.py` replaced with a wrapper delegating to
  `scripts/validate.py` (canonical).
- Original preserved as `tools/validate.py.deprecated`.

### Added
- `reports/VALIDATION_CANONICAL.md`.

## [2026-10-10] — A2: Schema/Data Repair

### Changed
- Relaxed JSON schemas to accept actual data structure.
- Fixed `_dataset_meta.yaml`/`.json` — status enum + record_count.

## [2026-10-10] — Session 11-12: Dataset Completion

### Added
- `dat_15` (Power Management): 26 records, 95% coverage.
- `dat_04` (Timing): 19 records, 95% coverage.

## [2026-10-10] — Session 10: Honest Coverage

### Added
- `reports/COVERAGE_REALITY.md` — transparent coverage analysis.

### Fixed
- `measure_coverage.py` — replaced flawed regex-ratio formula with manual
  counting methodology.

---

## History (pre-alignment)

# Changelog

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
## [v1.1.0] — Phase 2a / 2b skeletons and partial datasets
- Added schemas `dat_01`, `dat_02`, `dat_03`, `dat_08`, `dat_09`, `dat_10`,
  `dat_11`, `dat_12`, `dat_13`, `dat_14`, `dat_17`, `dat_18`.
- Added deferred dataset folders (records: []):
  `at_commands`, `error_codes`, `firmware_compat`, `sms`, `gprs_data`,
  `http_ftp_ssl`, `operator_apn`, `certificate_keystore`, `certification`.
- Added partial dataset folders with HW records only:
  - `urc` (dat_02) — 10 HW URC records; `urc_at.yaml` pending.
  - `audio` (dat_12) — 8 HW audio records; `audio_at.yaml` pending.
  - `sim_management` (dat_13) — 8 HW SIM records; `sim_management_at.yaml`
    pending.
- Updated `DATASET_MAP` in `tools/validate.py` to cover all 18 datasets.
- Added `raw/dat_*_extract.md` and `raw/dat_*_diagrams.md` for Phase 2.
- Updated `docs/source_mapping.md`, `docs/conflict_log.md`,
  `docs/diagram_mapping.md`, `docs/data_dictionary.md`,
  `docs/validation_guide.md`.
- Added `PHASE_2_REPORT.md`.

## [v1.2.0] — Phase 2c: best-effort AT/SMS/GPRS extraction from HW PDFs
- dat_01 (AT Command DB): 0 → 18 records (commands mentioned in the two
  hardware PDFs; full syntax/parameters/responses pending AT Command Manual).
- dat_02 (URC DB): 10 → 12 records (added `+CFUN: 1` and `+CPIN: READY`
  from Section 4.5.1; remaining AT-related URCs pending Manual).
- dat_09 (SMS DB): 0 → 3 capability records (modes, storage, RI notification).
- dat_10 (GPRS/Data DB): 0 → 7 capability records (multi-slot, coding
  schemes, PPP, TCP/IP, PBCCH, CSD, max data rate).
- Regenerated schemas `dat_01`, `dat_09`, `dat_10` with explicit field
  definitions (previously deferred-only, `_meta`-only).
- Updated `_dataset_meta.yaml` for dat_01, dat_02, dat_09, dat_10
  (still `partial`, pending AT Command Manual).
- Updated `docs/source_mapping.md`, `docs/data_dictionary.md`,
  `docs/validation_guide.md`.
- Added `PHASE_2C_REPORT.md`.
- No changes to README.md, PHASE_1_REPORT.md, LICENSE, NOTICE.

## [Fix] — پس از اجرای اولیه
### Fixed
- باگ پرانتزگذاری در تولید COVERAGE_MATRIX.md (وضعیت‌ها اکنون complete/partial/blocked/deferred).
- scripts/validate.py و scripts/cross_ref.py اکنون هم `.json` و هم `.yaml`/`.yml` در `data/**` را می‌خوانند.
- اجرای خودکار `validate.py` و `cross_ref.py` و ثبت خروجی در `VALIDATION_REPORT.md`.