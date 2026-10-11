# SESSION_LOG

## Batch D10 — 20 substeps (production criteria)

- تاریخ: 1405-07-19T17:44:20Z
- موفق: 15 / 18

| زیرگام | نام | نتیجه | وضعیت |
|---|---|---|---|
| s0_sections | build section index | see _section_index.json | OK |
| s1_dat09 | dat_09 SMS params | with_params=14 | OK |
| s2_dat10 | dat_10 GPRS params | with_params=17 | PARTIAL |
| s3_dat12 | dat_12 Audio params | with_params=9 | PARTIAL |
| s4_dat13 | dat_13 SIM params | with_params=9 | OK |
| s5_dat11 | dat_11 HTTP/FTP params | with_params=19 | OK |
| s6_dat02 | dat_02 URC examples verify | with_examples=206 | OK |
| s7_dat05 | dat_05 related_urcs | with_urcs=9 | OK |
| s8_dat03 | dat_03 recovery | with_recovery=86 | OK |
| s9_dat04 | dat_04 values ext | with_values=11 | PARTIAL |
| s10_dat15 | dat_15 verify | with_values=13 | OK |
| s11_dat06 | dat_06 finalize | unknown=0 | OK |
| s12_dat07 | dat_07 function | with_function=78 | OK |
| s13_coverage | COVERAGE params | c=9 p=5 b=3 d=1 | OK |
| s14_docs | finalize docs | L1=0 L2=0 L3=8 | OK |
| s15_changelog | CHANGELOG | written | OK |
| s16_sources | source inventory | files=4 | OK |
| s17_todo | TODO | updated | OK |


### validate.py
- L1: 0
- L2: 0
- L3: 8
- L4: 0

### Coverage (production)
- complete: 9
- partial: 5
- blocked: 3
- deferred: 1

### Notes
- } else { در یک خط نوشته شد (رفع باگ D8).
- params_pct معیار واقعی تولید است.
- Section body AT Manual برای پر کردن params استفاده شد.