# ROLE_MAP.md

Generated: 2026-10-12T11:29:52Z

| Dataset | Role | Depends on | Depended on by | Status |
|---|---|---|---|---|
| dat_01 | AT command / protocol | - | dat_02, dat_03, dat_09, dat_10, dat_11, dat_12, dat_13, dat_17 | partial |
| dat_02 | AT command / protocol | dat_01 | - | partial |
| dat_03 | AT command / protocol | dat_01 | - | complete |
| dat_04 | Hardware reference | - | dat_05, dat_06 | partial |
| dat_05 | Hardware reference | - | dat_06 | partial |
| dat_06 | Hardware reference | - | - | partial |
| dat_07 | Hardware reference | - | dat_13, dat_16 | complete |
| dat_08 | External / certification | - | - | blocked |
| dat_09 | AT command / protocol | dat_01 | - | complete |
| dat_10 | AT command / protocol | dat_01 | - | partial |
| dat_11 | AT command / protocol | dat_01 | dat_17 | blocked |
| dat_12 | AT command / protocol | dat_01 | - | partial |
| dat_13 | AT command / protocol | dat_01, dat_07 | - | complete |
| dat_14 | External / certification | - | - | deferred |
| dat_15 | Hardware reference | - | - | blocked |
| dat_16 | Hardware reference | - | - | deferred |
| dat_17 | AT command / protocol | dat_01, dat_11 | - | blocked |
| dat_18 | External / certification | - | - | blocked |
