# A1_dat07_final_gaps

dat_07 module pins (excl. holder): 49
dat_07 SIM-card-holder pins:       8
V2.02 canonical pins (extracted):  56
V1.00 canonical pins (extracted):  56
V2.02 extra (subheading pins):     ['PWM']

## Final missing pins to add to dat_07

| Pin | In V2.02 | In V1.00 | Source page | Notes |
|-----|----------|----------|-------------|-------|
| FM_ANTN | yes | yes | V2.02 Table 5 | Add from V2.02 (primary) |
| FM_ANTP | yes | yes | V2.02 Table 5 | Add from V2.02 (primary) |
| GSM_ANT | yes | yes | V2.02 Table 5 | Add from V2.02 (primary) |
| RESET | yes | yes | V2.02 Table 5 | Add from V2.02 (primary) |
| RF_SYNC | yes | yes | V2.02 Table 5 | Add from V2.02 (primary) |
| VDD_EXT | yes | yes | V2.02 Table 5 | Add from V2.02 (primary) |
| VRTC | yes | yes | V2.02 Table 5 | Add from V2.02 (primary) |

## Excluded pins (must NOT be added)

- BT_ANT — SIM800H-only, R1 forbids including it in SIM800L dataset

## V1.00-only pins (not in dat_07 and not in V2.02)

- NC

## SIM-card-holder pins currently in dat_07

These are pins of the Molex 91228 / Amphenol C707 SIM card holder,
not module pads. They do not belong in dat_07.

- C1
- C2
- C3
- C4
- C5
- C6
- C7
- C8

Recommendation: move these records to `dat_16_board_evb.yaml`
(or delete if dat_16 is deferred). Do NOT keep them in dat_07.

## PWM — was reported as 'extra' by the previous run

PWM **is present** in V2.02 §Table 30 (Pin definition of the PWM).
The previous extraction missed it because PWM appears as a subheading
(group label) inside the Pin Description table, not as a data row
with a pin number. It has been restored to the missing list.
