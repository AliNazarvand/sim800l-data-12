

## 2026-10-13T18:07:56Z — v5-corrective decisions
- **dat_01 dedup by command name**: extract_at_commands.py (335 records) and _rebuild_B1_dat01.py (275 records) both wrote to the same file causing 610 records. Dedup merges by command key; keeps the record with proper source.name and merges list fields.
- **dat_15 dedup by (category, mode, parameter)**: _rebuild_dat15.py added 350 records on top of 13 existing, causing 363 records. Dedup groups by semantic key.
- **dat_16 -> deferred (was blocked)**: Per prompt spec, dat_16 is deferred when no official EVB source exists (R11 interpretation).
- **dat_17 -> blocked (was complete)**: SSL Manual is required for dat_17 per prompt spec; it is missing, so dat_17 must be blocked.
- **Status thresholds per prompt NOMINAL**: dat_05=20, dat_09=10, dat_10=20, dat_11=30, dat_12=10, dat_13=8.
- **Coverage**: computed for dat_01 only (from _at_commands_index.json); for others use coverage_estimate = null (source cardinality unknown).
