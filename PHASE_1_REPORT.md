# PHASE 1 REPORT -- sim800l-data

_Last updated: 

## Objective

Complete the data-driven `sim800l-data` project for **SIM800L only**, with
documented, traceable, schema-valid, cross-referenced, and reproducible
datasets.

## Available Sources (confirmed)

- `SIM800L_Hardware_Design_V1.00.pdf` (2013-08-20)
- `SIM800H&SIM800L_Hardware_Design_V2.02.PDF` (2015-07-27) -- priority
- `SIM800 Series_AT Command Manual_V1.01.pdf` (date not verified)

## Status Snapshot (2026-10-12)

- **dat_01** (AT Command): partial -- 0 records
- **dat_02** (URC): partial -- 206 records
- **dat_03** (Error Code): partial -- 255 records
- **dat_04** (Timing & Timeout): partial -- 40 records
- **dat_05** (State Machine): partial -- 31 records
- **dat_06** (Init Sequence): partial -- 32 records
- **dat_07** (Hardware Reference): partial -- 0 records
- **dat_08** (Firmware Compatibility): blocked -- 1 records
- **dat_09** (SMS): partial -- 14 records
- **dat_10** (GPRS/Data): partial -- 24 records
- **dat_11** (HTTP/FTP/SSL): partial -- 38 records
- **dat_12** (Audio): partial -- 13 records
- **dat_13** (SIM Management): partial -- 10 records
- **dat_14** (Operator/APN): deferred -- 52 records
- **dat_15** (Power Management): partial -- 14 records
- **dat_16** (Board/EVB): deferred -- 1 records
- **dat_17** (Certificate/Key Store): partial -- 9 records
- **dat_18** (Certification): blocked -- 1 records

## Notes

- Bootstrap extraction (prior session) extracted 0 records from both AT JSON
  and HW text. It also overwrote dat_01/dat_07 with empty files.
- This session restored dat_01/dat_07 from the oldest available backup.
- Future extraction should reuse existing scripts (see scripts/_rebuild_*.py).

See `reports/COVERAGE_MATRIX.md` for details.