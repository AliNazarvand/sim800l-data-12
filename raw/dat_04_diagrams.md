# Diagram Descriptions — dat_04

Source: `SIM800H&SIM800L_Hardware_Design_V2.02`.

| Figure | Page | Description | Mapped to |
|--------|------|-------------|-----------|
| Figure 8 | 21 | VBAT drop during transmit burst: 577µs burst, 4.615ms period, 2A peak, max drop 350mV. | dat_04_timing_005 |
| Figure 12 | 23 | Power-on timing: PWRKEY low ≥1s, VDD_EXT rise, STATUS high, RDY URC. | dat_04_timing_001 |
| Figure 13 | 23 | Power-down by PWRKEY: 1s<t<33s PWRKEY low window, V_IL<0.7V, t>1.6s to VDD_EXT/STATUS drop. | dat_04_timing_002 |
| Figure 14 | 25 | Restart: 1s<T1<2s PWRKEY low, T2≥2s STATUS low, T3>800ms before next power-on. | dat_04_timing_004 |
| Figure 16 | 26 | Reset timing sequence: t>105ms RESET low, t<400us VDD_EXT reaction, 800ms, 2.7s STATUS. | dat_04_timing_003 |
| Figure 48 | 51 | RF_SYNC timing: 220µs high, 577µs low during TX burst. | dat_04_timing_007 |