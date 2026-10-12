# PHASE 1 REPORT -- sim800l-data

_Last updated: 2026-10-12_

## Objective

Complete the data-driven `sim800l-data` project for **SIM800L only**, with documented, traceable, schema-valid, cross-referenced, and reproducible datasets.

## Available Sources

- `SIM800L_Hardware_Design_V1.00.pdf` (2013-08-20)
- `SIM800H&SIM800L_Hardware_Design_V2.02.PDF` (2015-07-27) -- priority
- `SIM800 Series_AT Command Manual_V1.01.pdf` (date not verified)
- Extracted text: `at_v1_01_full.txt`, `hw_v2_02_full.txt`, `hw_v1_00_full.txt`
- Extracted index: `_at_commands_index.json`

## Status Snapshot (2026-10-12)

| Dataset | Status | Real | Placeholders |
|---------|--------|------|--------------|
| dat_01 (AT Command) | partial | 334 | 0 |
| dat_02 (URC) | partial | 206 | 0 |
| dat_03 (Error Code) | partial | 255 | 0 |
| dat_04 (Timing & Timeout) | partial | 40 | 0 |
| dat_05 (State Machine) | partial | 31 | 0 |
| dat_06 (Init Sequence) | partial | 32 | 0 |
| dat_07 (Hardware Reference) | partial | 56 | 0 |
| dat_08 (Firmware Compatibility) | blocked | 1 | 0 |
| dat_09 (SMS) | partial | 14 | 0 |
| dat_10 (GPRS/Data) | partial | 24 | 0 |
| dat_11 (HTTP/FTP/SSL) | partial | 38 | 0 |
| dat_12 (Audio) | partial | 13 | 0 |
| dat_13 (SIM Management) | partial | 10 | 0 |
| dat_14 (Operator/APN) | partial | 52 | 0 |
| dat_15 (Power Management) | partial | 14 | 0 |
| dat_16 (Board/EVB) | deferred | 1 | 0 |
| dat_17 (Certificate/Key Store) | partial | 9 | 0 |
| dat_18 (Certification) | blocked | 1 | 0 |

## Notes

- Bootstrap extraction (v3) extracted 0 records and overwrote dat_01/dat_07.
- dat_01 (334) and dat_07 (56) were restored from the oldest backup.
- Future extraction should reuse existing scripts: `scripts/_rebuild_B1_dat01.py`, `scripts/_rebuild_dat07.py`.
- All statuses now derived from real record counts (see DECISIONS_LOG D-008).