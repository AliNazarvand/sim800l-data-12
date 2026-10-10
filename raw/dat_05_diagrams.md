# Diagram Descriptions — dat_05

Source: `SIM800H&SIM800L_Hardware_Design_V2.02`.

| Figure | Page | Description | Mapped to |
|--------|------|-------------|-----------|
| Figure 12 | 23 | Power-on: PWRKEY low → RDY URC → operating. | dat_05_transition_001/002 |
| Figure 13 | 23 | Power-down by PWRKEY → VDD_EXT low → STATUS low → NORMALPOWERDOWN. | dat_05_transition_003/004 |
| Figure 14 | 25 | Restart sequence. | dat_05_transition_005 |
| Figure 16 | 26 | Reset: RESET low → STATUS low → VDD_EXT high after 800ms → STATUS high after 2.7s. | dat_05_transition_006/007 |
| Figure 27–30 | 34–35 | RI behavior for voice / data / SMS / URC / caller. | dat_05_state_006/007 |