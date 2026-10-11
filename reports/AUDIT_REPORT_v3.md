# AUDIT_REPORT_v3

Generated: 2026-10-12T00:52:23

## Method

- validate.py: 0 errors (L1=L2=L3=L4=0)
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

- dat_09_0001 in dat_09: command '+AT+CMGF' not in dat_01
- dat_09_0002 in dat_09: command '+AT+CMGS' not in dat_01
- dat_09_0003 in dat_09: command '+AT+CMGR' not in dat_01
- dat_09_0004 in dat_09: command '+AT+CMGL' not in dat_01
- dat_09_0005 in dat_09: command '+AT+CMGD' not in dat_01
- dat_09_0006 in dat_09: command '+AT+CMGW' not in dat_01
- dat_09_0007 in dat_09: command '+AT+CSCA' not in dat_01
- dat_09_0008 in dat_09: command '+AT+CSMS' not in dat_01
- dat_09_0009 in dat_09: command '+AT+CPMS' not in dat_01
- dat_09_0010 in dat_09: command '+AT+CNMI' not in dat_01
- dat_09_0011 in dat_09: command '+AT+CSMP' not in dat_01
- dat_09_0012 in dat_09: command '+AT+CSDH' not in dat_01
- dat_09_0013 in dat_09: command '+AT+CMEE' not in dat_01
- dat_09_0014 in dat_09: command '+AT+CSCS' not in dat_01
- dat_10_0001 in dat_10: command '+AT+CGDCONT' not in dat_01
- dat_10_0002 in dat_10: command '+AT+CGATT' not in dat_01
- dat_10_0003 in dat_10: command '+AT+CGACT' not in dat_01
- dat_10_0004 in dat_10: command '+AT+CGCONTRDP' not in dat_01
- dat_10_0005 in dat_10: command '+AT+CGPADDR' not in dat_01
- dat_10_0006 in dat_10: command '+AT+CSTT' not in dat_01
- dat_10_0007 in dat_10: command '+AT+CIICR' not in dat_01
- dat_10_0008 in dat_10: command '+AT+CIFSR' not in dat_01
- dat_10_0009 in dat_10: command '+AT+CIPSTART' not in dat_01
- dat_10_0010 in dat_10: command '+AT+CIPSEND' not in dat_01
- dat_10_0011 in dat_10: command '+AT+CIPCLOSE' not in dat_01
- dat_10_0012 in dat_10: command '+AT+CIPSHUT' not in dat_01
- dat_10_0013 in dat_10: command '+AT+CIPSTATUS' not in dat_01
- dat_10_0014 in dat_10: command '+AT+CIPRXGET' not in dat_01
- dat_10_0015 in dat_10: command '+AT+CIPMUX' not in dat_01
- dat_10_0016 in dat_10: command '+AT+CIPQSEND' not in dat_01
- dat_10_0017 in dat_10: command '+AT+CIPDDREM' not in dat_01
- dat_10_0018 in dat_10: command '+AT+CIPMODE' not in dat_01
- dat_10_0019 in dat_10: command '+AT+CIPCCFG' not in dat_01
- dat_10_0020 in dat_10: command '+AT+CSQ' not in dat_01
- dat_10_0021 in dat_10: command '+AT+CREG' not in dat_01
- dat_10_0022 in dat_10: command '+AT+CGREG' not in dat_01
- dat_10_0023 in dat_10: command '+AT+CEREG' not in dat_01
- dat_10_0024 in dat_10: command '+AT+CDNSGIP' not in dat_01
- dat_11_0001 in dat_11: command '+AT+HTTPINIT' not in dat_01
- dat_11_0002 in dat_11: command '+AT+HTTPTERM' not in dat_01
- dat_11_0003 in dat_11: command '+AT+HTTPPARA' not in dat_01
- dat_11_0004 in dat_11: command '+AT+HTTPDATA' not in dat_01
- dat_11_0005 in dat_11: command '+AT+HTTPACTION' not in dat_01
- dat_11_0006 in dat_11: command '+AT+HTTPREAD' not in dat_01
- dat_11_0007 in dat_11: command '+AT+HTTPHEAD' not in dat_01
- dat_11_0008 in dat_11: command '+AT+HTTPSTATUS' not in dat_01
- dat_11_0009 in dat_11: command '+AT+HTTPURL' not in dat_01
- dat_11_0010 in dat_11: command '+AT+HTTPSSL' not in dat_01
- dat_11_0011 in dat_11: command '+AT+FTPOPEN' not in dat_01
- dat_11_0012 in dat_11: command '+AT+FTPCLOSE' not in dat_01
- dat_11_0013 in dat_11: command '+AT+FTPPUT' not in dat_01
- dat_11_0014 in dat_11: command '+AT+FTPGET' not in dat_01
- dat_11_0015 in dat_11: command '+AT+FTPDELE' not in dat_01
- dat_11_0016 in dat_11: command '+AT+FTPMKD' not in dat_01
- dat_11_0017 in dat_11: command '+AT+FTPRMD' not in dat_01
- dat_11_0018 in dat_11: command '+AT+FTPLIST' not in dat_01
- dat_11_0019 in dat_11: command '+AT+FTPFLST' not in dat_01
- dat_11_0020 in dat_11: command '+AT+FTPUSER' not in dat_01
- dat_11_0021 in dat_11: command '+AT+FTPPASS' not in dat_01
- dat_11_0022 in dat_11: command '+AT+FTPCWD' not in dat_01
- dat_11_0023 in dat_11: command '+AT+FTPPWD' not in dat_01
- dat_11_0024 in dat_11: command '+AT+FTPTYPE' not in dat_01
- dat_11_0025 in dat_11: command '+AT+FTPMODE' not in dat_01
- dat_11_0026 in dat_11: command '+AT+FTPPUTOPT' not in dat_01
- dat_11_0027 in dat_11: command '+AT+FTPGETPATH' not in dat_01
- dat_11_0028 in dat_11: command '+AT+FTPPUTPATH' not in dat_01
- dat_11_0029 in dat_11: command '+AT+FTPPORT' not in dat_01
- dat_11_0030 in dat_11: command '+AT+SSLCFG' not in dat_01
- dat_11_0031 in dat_11: command '+AT+SSLCONF' not in dat_01
- dat_11_0032 in dat_11: command '+AT+SSLOPEN' not in dat_01
- dat_11_0033 in dat_11: command '+AT+SSLSEND' not in dat_01
- dat_11_0034 in dat_11: command '+AT+SSLRECV' not in dat_01
- dat_11_0035 in dat_11: command '+AT+SSLCLOSE' not in dat_01
- dat_11_0036 in dat_11: command '+AT+SSLSETCERT' not in dat_01
- dat_11_0037 in dat_11: command '+AT+SSLSETKEY' not in dat_01
- dat_11_0038 in dat_11: command '+AT+SSLSETCA' not in dat_01
- dat_12_0001 in dat_12: command '+AT+CLVL' not in dat_01
- dat_12_0002 in dat_12: command '+AT+CRSL' not in dat_01
- dat_12_0003 in dat_12: command '+AT+CMUT' not in dat_01
- dat_12_0004 in dat_12: command '+AT+CRSM' not in dat_01
- dat_12_0005 in dat_12: command '+AT+VTS' not in dat_01
- dat_12_0006 in dat_12: command '+AT+CATONE' not in dat_01
- dat_12_0007 in dat_12: command '+AT+CADTONE' not in dat_01
- dat_12_0008 in dat_12: command '+AT+CLDTONE' not in dat_01
- dat_12_0009 in dat_12: command '+AT+CMIC' not in dat_01
- dat_12_0010 in dat_12: command '+AT+CSDT' not in dat_01
- dat_12_0011 in dat_12: command '+AT+CHFA' not in dat_01
- dat_12_0012 in dat_12: command '+AT+CPCMREG' not in dat_01
- dat_12_0013 in dat_12: command '+AT+CADC' not in dat_01
- dat_13_0001 in dat_13: command '+AT+CPIN' not in dat_01
- dat_13_0002 in dat_13: command '+AT+CLCK' not in dat_01
- dat_13_0003 in dat_13: command '+AT+CPWD' not in dat_01
- dat_13_0004 in dat_13: command '+AT+CSIM' not in dat_01
- dat_13_0005 in dat_13: command '+AT+CRSM' not in dat_01
- dat_13_0006 in dat_13: command '+AT+CIMI' not in dat_01
- dat_13_0007 in dat_13: command '+AT+CCID' not in dat_01
- dat_13_0008 in dat_13: command '+AT+CSMINS' not in dat_01
- dat_13_0009 in dat_13: command '+AT+CSPN' not in dat_01
- dat_13_0010 in dat_13: command '+AT+CUSD' not in dat_01
- dat_17_0001 in dat_17: command '+AT+SSLCFG' not in dat_01
- ... (210 more)

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
- Review cross-reference issues above before declaring datasets complete.
- 'no-source' counts records missing source.name or source.version.