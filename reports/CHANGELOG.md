# CHANGELOG

## 1405-07-19T17:21:50Z — Batch B6+C+D2
- dat_10 (GPRS/Data): 21 records annotated from AT Manual V1.01
- dat_11 (HTTP/FTP/SSL): 10 records annotated
- dat_12 (Audio): 7 records annotated
- dat_17 (Certificate/Key Store): BLOCKED (SSL Manual required)
- dat_04, dat_06: re-annotate attempts with per-dataset gates
- dat_02: suspicious records attempt fix
- dat_01: unknown records attempt completion
- L3 analysis: see reports/_step_D2_L3_analysis.json

## Earlier batches
- B1: dat_01 rebuild from AT Manual V1.01 (275 commands)
- B1 fix: dedup dat_01, cmd_norm fix
- B2+B3 retry: dat_02 + dat_03 extraction (with suspicious flags)
- A1: dat_07 hardware reference (75/78 annotated)
- A2: dat_15 (revert — auto-detection failed)
- A3: structured scan for dat_04/dat_05/dat_06
- Step 1: infrastructure cleanup + validate.py rewrite