# SESSION_LOG

## Batch D6 — 12 substeps

- تاریخ: 1405-07-19T17:29:55Z
- موفق: 9 / 12

| زیرگام | نام | نتیجه | وضعیت |
|---|---|---|---|
| 1_validate | rewrite validate.py | L3=8 | OK |
| 2_dat03 | complete dat_03 | wp=255 blk=0 total=255 | OK |
| 3_dat06 | complete dat_06 | with_page=6 (<10) | PARTIAL |
| 4_dat10 | complete dat_10 | wp=24/24 | OK |
| 5_dat11 | dat_11 unknown->blocked | unknown=0 | OK |
| 6_dat12 | complete dat_12 | wp=13 blk=4 total=13 | OK |
| 7_dat15 | complete dat_15 | wp=13/14 | PARTIAL |
| 8_dat01_params | dat_01 parameters | with_parameters=16 (<50) | PARTIAL |
| 9_dat14 | dat_14 external | total=52 url=52 ext=52 | OK |
| 10_coverage | rebuild COVERAGE | c=11 p=3 b=3 d=1 | OK |
| 11_docs | finalize docs | README + PHASE_1 | OK |
| 12_phase1_report | phase1 final table | table written | OK |


### validate.py
- L1: 0
- L2: 0
- L3: 8
- L4: 0

### Coverage
- complete: 11
- partial: 3
- blocked: 3
- deferred: 1

### Phase 1
- جدول نهایی: reports/PHASE_1_FINAL_TABLE.md