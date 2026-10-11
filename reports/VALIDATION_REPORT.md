# VALIDATION_REPORT

Generated: 2026-10-11T17:28:23Z

## خلاصه
- خطاهای سطح ۱ (Schema): 0
- خطاهای سطح ۲ (Business): 0
- خطاهای سطح ۳ (Cross-ref): 35
- خطاهای سطح ۴ (Consistency): 0

## وضعیت cross-ref

- dat_01 status: `complete`
- cross-ref اجرا شد: `True`

## فایل‌های کشف‌شده

| دیتاست | فایل |
|---|---|
| dat_01 | dat_01_at_command.yaml |
| dat_02 | dat_02_urc.yaml |
| dat_03 | dat_03_error_code.yaml |
| dat_04 | dat_04_timing_timeout.yaml |
| dat_05 | dat_05_state_machine.yaml |
| dat_06 | dat_06_init_sequence.yaml |
| dat_07 | dat_07_hardware_reference.yaml |
| dat_08 | dat_08_firmware_compatibility.yaml |
| dat_09 | dat_09_sms.yaml |
| dat_10 | dat_10_gprs_data.yaml |
| dat_11 | dat_11_http_ftp_ssl.yaml |
| dat_12 | dat_12_audio.yaml |
| dat_13 | dat_13_sim_management.yaml |
| dat_14 | dat_14_operator_apn.yaml |
| dat_15 | dat_15_power_management.yaml |
| dat_16 | dat_16_board_evb.yaml |
| dat_17 | dat_17_certificate_key_store.yaml |
| dat_18 | dat_18_certification.yaml |

## جزئیات خطاها

| دیتاست | سطح | رکورد | خطا | پیشنهاد اصلاح |
|---|---|---|---|---|
| dat_10 | 3 | dat_10_0004 | command AT+CGCONTRDP not in dat_01 | add to dat_01 or fix |
| dat_10 | 3 | dat_10_0017 | command AT+CIPDDREM not in dat_01 | add to dat_01 or fix |
| dat_10 | 3 | dat_10_0023 | command AT+CEREG not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0007 | command AT+HTTPHEAD not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0009 | command AT+HTTPURL not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0010 | command AT+HTTPSSL not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0011 | command AT+FTPOPEN not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0012 | command AT+FTPCLOSE not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0019 | command AT+FTPFLST not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0020 | command AT+FTPUSER not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0021 | command AT+FTPPASS not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0022 | command AT+FTPCWD not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0023 | command AT+FTPPWD not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0030 | command AT+SSLCFG not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0031 | command AT+SSLCONF not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0032 | command AT+SSLOPEN not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0033 | command AT+SSLSEND not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0034 | command AT+SSLRECV not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0035 | command AT+SSLCLOSE not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0036 | command AT+SSLSETCERT not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0037 | command AT+SSLSETKEY not in dat_01 | add to dat_01 or fix |
| dat_11 | 3 | dat_11_0038 | command AT+SSLSETCA not in dat_01 | add to dat_01 or fix |
| dat_12 | 3 | dat_12_0006 | command AT+CATONE not in dat_01 | add to dat_01 or fix |
| dat_12 | 3 | dat_12_0007 | command AT+CADTONE not in dat_01 | add to dat_01 or fix |
| dat_12 | 3 | dat_12_0008 | command AT+CLDTONE not in dat_01 | add to dat_01 or fix |
| dat_12 | 3 | dat_12_0012 | command AT+CPCMREG not in dat_01 | add to dat_01 or fix |
| dat_17 | 3 | dat_17_0001 | command AT+SSLCFG not in dat_01 | add to dat_01 or fix |
| dat_17 | 3 | dat_17_0002 | command AT+SSLCONF not in dat_01 | add to dat_01 or fix |
| dat_17 | 3 | dat_17_0003 | command AT+SSLOPEN not in dat_01 | add to dat_01 or fix |
| dat_17 | 3 | dat_17_0004 | command AT+SSLSEND not in dat_01 | add to dat_01 or fix |
| dat_17 | 3 | dat_17_0005 | command AT+SSLRECV not in dat_01 | add to dat_01 or fix |
| dat_17 | 3 | dat_17_0006 | command AT+SSLCLOSE not in dat_01 | add to dat_01 or fix |
| dat_17 | 3 | dat_17_0007 | command AT+SSLSETCERT not in dat_01 | add to dat_01 or fix |
| dat_17 | 3 | dat_17_0008 | command AT+SSLSETKEY not in dat_01 | add to dat_01 or fix |
| dat_17 | 3 | dat_17_0009 | command AT+SSLSETCA not in dat_01 | add to dat_01 or fix |
