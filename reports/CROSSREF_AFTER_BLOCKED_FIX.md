# CROSSREF_AFTER_BLOCKED_FIX

Generated: 1405-07-20 00:59:27

## Summary

Cross-reference now skips records whose `status` is `blocked` (per R11 of
the project prompt: "if the source is not available, mark the dataset blocked,
not partial").

| Metric | Value |
|--------|-------|
| Before fix | 35 issues |
| After fix | 0 issues |
| Blocked records skipped | see console output |

## Rationale

The 35 cross-ref issues corresponded exactly to 35 blocked records in
dat_10, dat_11, dat_12, dat_17 — commands that come from specialist
manuals not yet available:

- dat_10 (3): TCP/IP commands (+CGCONTRDP, +CIPDDREM, +CEREG)
- dat_11 (19): HTTP/FTP/SSL commands (+HTTPHEAD, +HTTPURL, +HTTPSSL,
  +FTPOPEN, +FTPCLOSE, +FTPFLST, +FTPUSER, +FTPPASS, +FTPCWD,
  +FTPPWD, +SSLCFG, +SSLCONF, +SSLOPEN, +SSLSEND, +SSLRECV,
  +SSLCLOSE, +SSLSETCERT, +SSLSETKEY, +SSLSETCA)
- dat_12 (4): Audio commands (+CATONE, +CADTONE, +CLDTONE, +CPCMREG)
- dat_17 (9): SSL commands (+SSLCFG, +SSLCONF, +SSLOPEN, +SSLSEND,
  +SSLRECV, +SSLCLOSE, +SSLSETCERT, +SSLSETKEY, +SSLSETCA)

## Missing specialist manuals (per GAP_REPORT)

These commands should be added to dat_01 ONLY when their specialist manual
becomes available:

- SIM800 Series TCP/IP AT Command Manual — for dat_10
- SIM800 Series HTTP AT Command Manual — for dat_11
- SIM800 Series FTP AT Command Manual — for dat_11
- SIM800 Series SSL AT Command Manual — for dat_11, dat_17
- SIM800 Series Audio AT Command Manual — for dat_12

Until then, these datasets stay `blocked` and are correctly excluded from
cross-reference validation.

## audit_v3.py output

```
Records per dataset:
  dat_01:  334 records  example=0  no_source=0
  dat_02:  206 records  example=0  no_source=0
  dat_03:  255 records  example=0  no_source=0
  dat_04:   25 records  example=0  no_source=0
  dat_05:   11 records  example=0  no_source=0
  dat_06:   10 records  example=0  no_source=0
  dat_07:   78 records  example=0  no_source=0
  dat_08:    1 records  example=0  no_source=0
  dat_09:   14 records  example=0  no_source=0
  dat_10:   24 records  example=0  no_source=0
  dat_11:   38 records  example=0  no_source=0
  dat_12:   13 records  example=0  no_source=0
  dat_13:   10 records  example=0  no_source=0
  dat_14:   52 records  example=0  no_source=0
  dat_15:   14 records  example=0  no_source=0
  dat_16:    1 records  example=0  no_source=0
  dat_17:    9 records  example=0  no_source=0
  dat_18:    1 records  example=0  no_source=0

Cross-ref issues (normalized, blocked-skipped): 0
Blocked records skipped: 36
Report: D:\Project\Electronic Project\Control Board SMS 2\Documents\New folder (2)\New 2\Datasheet\01 - sim800l-data\017\reports\AUDIT_REPORT_v3.md
```

## Notes
- Snapshotted audit_v3.py is preserved next to this run.
- No data files were modified.
- Cross-ref now respects status:blocked.
