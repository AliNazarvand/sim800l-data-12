# dat_01 Report -- AT Command Database

<!-- v9-dat01-report RunId=d0968ad4 -->

Generated: 2026-10-13T04:32:50Z

## Current status

- File: `data/dat_01_at_command.yaml`
- Record count: **334**
- Status: **partial**
- Coverage estimate: unknown (source index not compared yet)
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