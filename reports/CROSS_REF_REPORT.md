# CROSS_REF_REPORT

## مشکلات (40)

- URC dat_02_0013 -> AT+CNMI در dat_01 یافت نشد
- URC dat_02_0027 -> AT+CNMI در dat_01 یافت نشد
- URC dat_02_0043 -> AT+CGREG در dat_01 یافت نشد
- URC dat_02_0062 -> AT+CIPRXGET در dat_01 یافت نشد
- URC dat_02_0071 -> AT+CIPSTATUS در dat_01 یافت نشد
- URC dat_02_0077 -> AT+CLIP در dat_01 یافت نشد
- URC dat_02_0119 -> AT+CNMI در dat_01 یافت نشد
- URC dat_02_0121 -> AT+CNMI در dat_01 یافت نشد
- URC dat_02_0134 -> AT+CPIN در dat_01 یافت نشد
- URC dat_02_0142 -> AT+CREG در dat_01 یافت نشد
- URC dat_02_0144 -> AT+CLIP در dat_01 یافت نشد
- URC dat_02_0172 -> AT+CUSD در dat_01 یافت نشد
- URC dat_02_0177 -> AT+FTPGET در dat_01 یافت نشد
- URC dat_02_0184 -> AT+FTPPUT در dat_01 یافت نشد
- URC dat_02_0198 -> AT+HTTPACTION در dat_01 یافت نشد
- URC dat_02_0201 -> AT+HTTPREAD در dat_01 یافت نشد
- SMS dat_09_0001 -> AT+CMGF در dat_01 یافت نشد
- SMS dat_09_0002 -> AT+CMGS در dat_01 یافت نشد
- SMS dat_09_0003 -> AT+CMGR در dat_01 یافت نشد
- SMS dat_09_0004 -> AT+CMGL در dat_01 یافت نشد
- SMS dat_09_0005 -> AT+CMGD در dat_01 یافت نشد
- SMS dat_09_0006 -> AT+CMGW در dat_01 یافت نشد
- SMS dat_09_0007 -> AT+CSCA در dat_01 یافت نشد
- SMS dat_09_0008 -> AT+CSMS در dat_01 یافت نشد
- SMS dat_09_0009 -> AT+CPMS در dat_01 یافت نشد
- SMS dat_09_0010 -> AT+CNMI در dat_01 یافت نشد
- SMS dat_09_0011 -> AT+CSMP در dat_01 یافت نشد
- SMS dat_09_0012 -> AT+CSDH در dat_01 یافت نشد
- SMS dat_09_0013 -> AT+CMEE در dat_01 یافت نشد
- SMS dat_09_0014 -> AT+CSCS در dat_01 یافت نشد
- SIM dat_13_0001 -> AT+CPIN در dat_01 یافت نشد
- SIM dat_13_0002 -> AT+CLCK در dat_01 یافت نشد
- SIM dat_13_0003 -> AT+CPWD در dat_01 یافت نشد
- SIM dat_13_0004 -> AT+CSIM در dat_01 یافت نشد
- SIM dat_13_0005 -> AT+CRSM در dat_01 یافت نشد
- SIM dat_13_0006 -> AT+CIMI در dat_01 یافت نشد
- SIM dat_13_0007 -> AT+CCID در dat_01 یافت نشد
- SIM dat_13_0008 -> AT+CSMINS در dat_01 یافت نشد
- SIM dat_13_0009 -> AT+CSPN در dat_01 یافت نشد
- SIM dat_13_0010 -> AT+CUSD در dat_01 یافت نشد

## آمار
- commandهای dat_01: 334
- URCها: 18
- Error codes: 255
- SMS: 14
- SIM: 10
---
<!-- v6-fix RunId=c6f60ee0 -->

## v6 honest cross-ref recount (1405-07-21T07:56:20Z)

- cross_ref issues: 40
- These are LEGITIMATE: they reference URC/SMS/SIM records whose related
  commands are absent from dat_01 because dat_01 is only partial.
- To bring this to zero, dat_01 must be completed from
  `sources/originals/SIM800 Series_AT Command Manual_V1.01.pdf`.