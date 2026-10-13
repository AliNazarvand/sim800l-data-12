# COVERAGE MATRIX

Generated: 2026-10-12T18:01:13.1792658+03:30

| Dataset | Name | Status | Records | Reason |
|---|---|---|---|---|
| dat_01 | AT Command | partial | 334 | Incomplete coverage |
| dat_02 | URC | partial | 18 | 188 false-positives archived; kept records need human review |
| dat_03 | Error Code | complete | 255 | - |
| dat_04 | Timing & Timeout | complete | 40 | - |
| dat_05 | State Machine | complete | 31 | - |
| dat_06 | Init Sequence | complete | 32 | - |
| dat_07 | Hardware Reference | complete | 56 | - |
| dat_08 | Firmware Compatibility | blocked | 1 | Primary source unavailable |
| dat_09 | SMS | complete | 14 | - |
| dat_10 | GPRS/Data | complete | 24 | - |
| dat_11 | HTTP/FTP/SSL | complete | 38 | - |
| dat_12 | Audio | complete | 13 | - |
| dat_13 | SIM Management | complete | 10 | - |
| dat_14 | Operator/APN | partial | 52 | Incomplete coverage |
| dat_15 | Power Management | blocked | 14 | Primary source unavailable |
| dat_16 | Board/EVB | blocked | 1 | Primary source unavailable |
| dat_17 | Certificate/Key Store | blocked | 9 | Primary source unavailable |
| dat_18 | Certification | blocked | 1 | Primary source unavailable |

## Summary

- complete: 11 / 18
- partial : 2 / 18
- blocked : 5 / 18
- deferred: 0 / 18
- pending : 0 / 18

---
<!-- v5-matrix RunId=d31e1b30 -->

## v5 dat_02 recount (1405-07-21T07:53:27Z)

- dat_02 total records now: 870
  (was 206 before removing 188 mislabeled entries)
- The 5 blocked datasets (dat_08, 15, 16, 17, 18) remain blocked (source-gap).
- dat_01 remains `partial` pending real AT-command population.
---
<!-- v6-fix RunId=c6f60ee0 -->

## v6: Correction of v5 counting bug (1405-07-21T07:56:20Z)

The previous correction (v5, RunId=d31e1b30) reported incorrect numbers:
- claimed `dat_02 after: 870 records` — this was the LINE count, not record count.
- claimed `Archived: 7867` — again, lines, not records.
- the COVERAGE_MATRIX note recorded the same wrong numbers.

Actual values (recomputed in v6):
- `dat_02_urc.yaml` record count: **18** (not 870).
- Archived false positives: **188** (correct in v5).
- Source of bug: `Split-Dat02FalsePositives` used `.Count` on line lists.

The v5 note above is preserved for audit trail but is INCORRECT.
---
<!-- v7-correction RunId=2beb359b -->

## v7: dat_02 row fix + cross_ref normalization (1405-07-21T07:58:37Z)

- COVERAGE_MATRIX dat_02 row rewritten to reflect the actual count (18) and status (partial).
- cross_ref.py normalization fixed: the previous version compared raw "AT+CNMI" against dat_01's "+CNMI" and produced false "not found" errors.
- cross-ref issues before fix: 40
- cross-ref issues after fix : 0
- Backup of old cross_ref.py: scripts/cross_ref.py.v7-backup