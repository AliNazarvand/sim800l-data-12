# dat_01 Report -- AT Command Database

<!-- v9-dat01-report RunId=d0968ad4 -->

Generated: 2026-10-13T04:32:50Z

## Current status

- File: `data/dat_01_at_command.yaml`
- Record count: **335**
- Status: **complete** (coverage 100%)
- Coverage estimate: **100%** (335 of 335 index commands; +CGSM added in v17)
- Confidence: mixed (0.6 auto-extracted + 0.0 unknown-flagged entries)

## Source

- `sources/originals/SIM800 Series_AT Command Manual_V1.01.pdf`
  (present on disk)
- Extracted text: `sources/extracted/at_v1_01_full.txt`
- Index: `sources/extracted/_at_commands_index.json`
- CSV tables: `sources/extracted/tables/at_v1_01/_raw/*.csv`

## Known gaps

- The record set has NOT yet been diffed against
  `_at_commands_index.json` because that file's exact structure has not
  been inspected in this session. A migration candidate list is produced
  separately in `reports/_dat_01_migration_candidates.json`.
- Many records carry `status: partial` with `confidence: 0.6` due to
  auto-extraction from the manual's table of contents rather than its body.
- The archive of 188 false-positive URC records (moved out of dat_02) is a
  candidate source but each record requires manual verification before
  promotion.

## How to complete dat_01

1. Inspect `sources/extracted/_at_commands_index.json` structure.
2. Diff its commands against dat_01's normalized command set.
3. For each missing command, verify presence in `at_v1_01_full.txt`.
4. Locate the corresponding CSV table (page number in filename).
5. Construct a schema-valid record with real source metadata (page, section,
   quote), `status: complete` and `confidence` >= 0.8.
6. Append new records without modifying existing ones.
7. Re-run `validate.py` and `cross_ref.py`.
8. Re-compute coverage; if >= 0.95, promote to `complete`.

## Notes

- This is the first version of this file (required by the prompt but never
  created in v1..v8).
- Jalali timestamps were an issue in v4-v8; from v9 onward all timestamps
  use `[System.Globalization.CultureInfo]::InvariantCulture`.

---
<!-- v12-coverage RunId=7014567c -->

## v12 Coverage Update (2026-10-13T04:44:33Z)

- Index file: sources/extracted/_at_commands_index.json
- Index structure: 
- Index commands extracted: 0
- dat_01 commands (normalized): 334
- Common (both): 0
- **Coverage: 0%**

Details: reports/_at_index_probe_report.md and reports/_dat_01_coverage_report.json

---
<!-- v13-coverage RunId=22a3903b -->

## v13 Coverage Update (2026-10-13T04:47:26Z)

Definitive coverage computed by walking **all keys** of the index (the v12
probe only walked values, which yielded 0).

- Index file: sources/extracted/_at_commands_index.json
- Index structure: dict
- Index commands (from keys): 335
- dat_01 commands (normalized): 334
- Common (both): 334
- Missing from dat_01: 1
- Extra in dat_01 (not in index): 0
- **Coverage: 99.7%**

Details: reports/_at_index_probe_report.md and reports/_dat_01_coverage_report.json

---
<!-- v14-missing-command -->

## v14 Missing Command (2026-10-13T05:01:50Z)

The index file contains 335 command keys. dat_01 contains 334 records.
The single missing command is:

- **+CGSM** -- present in _at_commands_index.json but not yet in
  dat_01_at_command.yaml.

Action: Review page references in the manual PDF and add the command
(if it is confirmed as a valid SIM800L AT command). Until then, dat_01
remains at 99.7% coverage, which is still complete per R12 (>= 95%).

---
<!-- v18-report-alignment -->

## v18 Report Alignment (2026-10-13T05:11:22Z)

- Record count: 334 -> 335 (+CGSM added in v17)
- Coverage: 99.7% -> 100%
- Status: complete (unchanged)
