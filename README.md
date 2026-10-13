# sim800l-data — SIM800L structured dataset

 Module-specific, source-documented, schema-validated dataset for the SIM800L module.

 ## Status Summary

 | Dataset | Name | Status | Records (real/total) |
 |---------|------|--------|----------------------|
 | dat_01 | AT Command | blocked | 0/1 |
 | dat_02 | URC | blocked | 0/1 |
 | dat_03 | Error Code | blocked | 0/1 |
 | dat_04 | Timing & Timeout | blocked | 0/1 |
 | dat_05 | State Machine | blocked | 0/1 |
 | dat_06 | Init Sequence | blocked | 0/1 |
 | dat_07 | Hardware Reference | blocked | 0/1 |
 | dat_08 | Firmware Compatibility | partial | 1/1 |
 | dat_09 | SMS | blocked | 0/1 |
 | dat_10 | GPRS/Data | blocked | 0/1 |
 | dat_11 | HTTP/FTP/SSL | blocked | 0/1 |
 | dat_12 | Audio | blocked | 0/1 |
 | dat_13 | SIM Management | blocked | 0/1 |
 | dat_14 | Operator/APN | complete | 52/52 |
 | dat_15 | Power Management | complete | 28/28 |
 | dat_16 | Board/EVB | partial | 1/1 |
 | dat_17 | Certificate/Key Store | partial | 9/9 |
 | dat_18 | Certification | partial | 1/1 |
 
## Sources Present

 - sources/originals/SIM800 Series_AT Command Manual_V1.01.pdf
 - sources/originals/SIM800H&SIM800L_Hardware_Design_V2.02.PDF
 - sources/originals/SIM800L_Hardware_Design_V1.00.pdf

 ## Validation

 - scripts/validate.py — exit=1
 - scripts/cross_ref.py — exit=1
