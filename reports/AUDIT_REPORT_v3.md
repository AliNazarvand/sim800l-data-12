# AUDIT_REPORT_v3

Generated: 2026-10-12T00:59:23

## Method

- validate.py: 0 errors (L1=L2=L3=L4=0)
- cross_ref uses normalize_cmd (strips 'AT+' and '+').
- cross_ref skips records with status == 'blocked' (per R11).
- This audit is read-only.

## Dataset Summary

| Dataset | Records | Status | example-only | no-source | conf<0.5 | conf>=0.7 | Sources |
|---------|---------|--------|--------------|-----------|----------|-----------|---------|
| dat_01 | 334 | partial:334 | 0 | 0 | 0 | 0 | SIM800 Series AT Command Manual, SIM800 Series_AT  |
| dat_02 | 206 | complete:16, partial:189, unknown:1 | 0 | 0 | 1 | 16 | SIM800 Series AT Command Manual, SIM800 Series_AT  |
| dat_03 | 255 | complete:237, partial:12, unknown:6 | 0 | 0 | 6 | 237 | SIM800 Series AT Command Manual, SIM800 Series_AT  |
| dat_04 | 25 | complete:13, partial:12 | 0 | 0 | 12 | 13 | SIM800H&SIM800L_Hardware_Design |
| dat_05 | 11 | inferred:11 | 0 | 0 | 11 | 0 | SIM800 Series AT Command Manual |
| dat_06 | 10 | inferred:6, partial:4 | 0 | 0 | 10 | 0 | SIM800 Series AT Command Manual |
| dat_07 | 78 | partial:78 | 0 | 0 | 0 | 0 | SIM800H&SIM800L_Hardware_Design, SIM800L_Hardware_ |
| dat_08 | 1 | blocked:1 | 0 | 0 | 1 | 0 | SIM800 Firmware Release Notes |
| dat_09 | 14 | complete:13, partial:1 | 0 | 0 | 0 | 13 | SIM800 Series AT Command Manual, SIM800 Series_AT  |
| dat_10 | 24 | blocked:3, complete:21 | 0 | 0 | 0 | 21 | SIM800 Series AT Command Manual |
| dat_11 | 38 | blocked:19, complete:19 | 0 | 0 | 19 | 19 | SIM800 Series AT Command Manual |
| dat_12 | 13 | blocked:4, complete:8, partial:1 | 0 | 0 | 0 | 8 | SIM800 Series AT Command Manual, SIM800 Series_AT  |
| dat_13 | 10 | complete:10 | 0 | 0 | 0 | 10 | SIM800 Series AT Command Manual |
| dat_14 | 52 | unknown:52 | 0 | 0 | 52 | 0 | mcc-mnc.com |
| dat_15 | 14 | blocked:1, partial:13 | 0 | 0 | 14 | 0 | SIM800 Sleep Mode Application Note, SIM800H&SIM800 |
| dat_16 | 1 | blocked:1 | 0 | 0 | 1 | 0 | SIM800L EVB Schematic |
| dat_17 | 9 | blocked:9 | 0 | 0 | 9 | 0 | SIM800 Series AT Command Manual |
| dat_18 | 1 | blocked:1 | 0 | 0 | 1 | 0 | SIM800L Certification Documents |

## Cluster Status

### Cluster A: dat_04, dat_05, dat_06, dat_07, dat_15, dat_16

- Total records: 139
- Blocked datasets: dat_15, dat_16
- Complete datasets: none

### Cluster B: dat_01, dat_02, dat_03, dat_09, dat_10, dat_11, dat_12, dat_13, dat_17

- Total records: 903
- Blocked datasets: dat_10, dat_11, dat_12, dat_17
- Complete datasets: dat_13

### Cluster C: dat_08, dat_14, dat_18

- Total records: 54
- Blocked datasets: dat_08, dat_18
- Complete datasets: none

## Cross-Reference Issues

- Records skipped (blocked): 36
- No issues found.

## Readiness for Cluster A

- Ready: **YES**

## Source Inventory

- dat_01: SIM800 Series AT Command Manual, SIM800 Series_AT Command Manual
- dat_02: SIM800 Series AT Command Manual, SIM800 Series_AT Command Manual
- dat_03: SIM800 Series AT Command Manual, SIM800 Series_AT Command Manual
- dat_04: SIM800H&SIM800L_Hardware_Design
- dat_05: SIM800 Series AT Command Manual
- dat_06: SIM800 Series AT Command Manual
- dat_07: SIM800H&SIM800L_Hardware_Design, SIM800L_Hardware_Design
- dat_08: SIM800 Firmware Release Notes
- dat_09: SIM800 Series AT Command Manual, SIM800 Series_AT Command Manual
- dat_10: SIM800 Series AT Command Manual
- dat_11: SIM800 Series AT Command Manual
- dat_12: SIM800 Series AT Command Manual, SIM800 Series_AT Command Manual
- dat_13: SIM800 Series AT Command Manual
- dat_14: mcc-mnc.com
- dat_15: SIM800 Sleep Mode Application Note, SIM800H&SIM800L_Hardware_Design
- dat_16: SIM800L EVB Schematic
- dat_17: SIM800 Series AT Command Manual
- dat_18: SIM800L Certification Documents

## Notes

- No files were modified during this audit.
- Cross-ref skips records with status == 'blocked' (R11).
- 'no-source' counts records missing source.name or source.version.