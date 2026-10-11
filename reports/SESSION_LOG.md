# SESSION_LOG

## Batch D11 — 25 substeps

- تاریخ: 1405-07-19T17:47:20Z
- موفق: 16 / 25

| زیرگام | نام | نتیجه | وضعیت |
|---|---|---|---|
| s1_dat15 | dat_15 last record | with_page=13 | PARTIAL |
| s2_dat04 | dat_04 values ext | with_values=12 | PARTIAL |
| s3_dat10 | dat_10 params ext | with_params=17 | PARTIAL |
| s4_dat12 | dat_12 params ext | with_params=9 | PARTIAL |
| s5_dat03 | dat_03 recovery ext | with_recovery=96 | PARTIAL |
| s6_dat11 | dat_11 params ext | with_params=25 | PARTIAL |
| s7_dat14 | dat_14 external depth | with_params=52 | OK |
| s8_dat01_err | dat_01 response_error | with_err=334 | OK |
| s9_dat01_fw | dat_01 firmware_min | with_fw=334 | OK |
| s10_dat02_urcs | dat_02 related_urcs | with_urcs=188 | OK |
| s11_dat05_tim | dat_05 related_timings | with_tim=0 | PARTIAL |
| s12_dat07_alt | dat_07 alt_function | with_alt=19 | PARTIAL |
| s13_dat09_ex | dat_09 examples | with_examples=14 | OK |
| s14_l3_analysis | L3 analysis | see _step_D11_L3_analysis.json | OK |
| s15_whitelist | extend whitelist | added=8 | OK |
| s16_validate | validate rerun | L3=8 | PARTIAL |
| s17_dat08 | dat_08 confirmed blocked | rn_found=0 | OK |
| s18_dat17 | dat_17 confirmed blocked | ssl_found=0 | OK |
| s19_dat18 | dat_18 confirmed blocked | cert_found=1 | OK |
| s20_dat16 | dat_16 confirmed deferred | evb_found=1 | OK |
| s21_todo | TODO | updated | OK |
| s22_coverage | COVERAGE final | c=9 p=5 b=3 d=1 | OK |
| s23_table | table v5 | written | OK |
| s24_changelog | CHANGELOG | written | OK |
| s25_validate | final validation | L1=0 L2=0 L3=8 L4=0 | OK |


### validate.py
- L1: 0
- L2: 0
- L3: 8
- L4: 0

### Coverage
- complete: 9
- partial: 5
- blocked: 3
- deferred: 1

### Notes
- } else { در یک خط (رفع باگ D8).
- L3 whitelist extended.
- Production criteria: complete = with_page==count AND params_pct >= 50%.