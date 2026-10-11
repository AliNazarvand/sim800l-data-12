# SCHEMA_NULLABLE_FIX_v2

Generated: 2026-10-12T00:48:38
Snapshot:  D:\Project\Electronic Project\Control Board SMS 2\Documents\New folder (2)\New 2\Datasheet\01 - sim800l-data\017\schemas_nullable_snapshot_v2_20261012-004837

## Summary

- Files processed: 18
- Fields nullable: 158

## Per-file counts

| Schema | Nullable fields added |
|--------|-----------------------|
| dat_01.schema.yaml | 12 |
| dat_02.schema.yaml | 9 |
| dat_03.schema.yaml | 6 |
| dat_04.schema.yaml | 9 |
| dat_05.schema.yaml | 9 |
| dat_06.schema.yaml | 8 |
| dat_07.schema.yaml | 14 |
| dat_08.schema.yaml | 8 |
| dat_09.schema.yaml | 11 |
| dat_10.schema.yaml | 8 |
| dat_11.schema.yaml | 7 |
| dat_12.schema.yaml | 6 |
| dat_13.schema.yaml | 7 |
| dat_14.schema.yaml | 9 |
| dat_15.schema.yaml | 11 |
| dat_16.schema.yaml | 5 |
| dat_17.schema.yaml | 12 |
| dat_18.schema.yaml | 7 |

## Method
- Recursive PyYAML walk over `properties`.
- Skips `id` (pattern-only field).
- Skips any property listed in its parent's `required`.
- Removed `date` from `source.required`.