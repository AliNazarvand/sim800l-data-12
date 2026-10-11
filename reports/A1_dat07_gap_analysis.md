# A1_dat07_gap_analysis

dat_07 canonical module pins: 50
V2.02 canonical pins:         56
V1.00 canonical pins:         0

## Coverage of V2.02 pins by dat_07

- Covered: 48 / 56  (85%)

## Missing pins (in V2.02 but not in dat_07)

| Pin | In V2.02 | In V1.00 | Recommend |
|-----|----------|----------|-----------|
| BT_ANT | yes | no | Add from V2.02 (only) |
| FM_ANTN | yes | no | Add from V2.02 (only) |
| FM_ANTP | yes | no | Add from V2.02 (only) |
| GSM_ANT | yes | no | Add from V2.02 (only) |
| RESET | yes | no | Add from V2.02 (only) |
| RF_SYNC | yes | no | Add from V2.02 (only) |
| VDD_EXT | yes | no | Add from V2.02 (only) |
| VRTC | yes | no | Add from V2.02 (only) |

## Missing pins (in V1.00 but not in dat_07, not in V2.02)

(none)

## Extra pins (in dat_07 but not in either PDF pin table)

- PWM
- VSIM

## Notes

- Pins C1..C8 in dat_07 are from the Molex / Amphenol
  SIM card holder tables (V2.02 §Table 18/19 and V1.00 §Table 18/19).
  They are not module pads and were excluded from coverage math.
- V2.02 uses `KBCx`/`KBRx` for keypad columns/rows;
  V1.00 uses `COLx`/`ROWx`. Both were normalised to `KBCx`/`KBRx`.
- V2.02 uses `PCM_CLK`/`PCM_OUT`/`PCM_SYNC`/`PCM_IN`;
  V1.00 uses `PCMCLK`/`PCMOUT`/`PCMSYNC`/`PCMIN`.
- V2.02 uses `USB_DN`; V1.00 uses `USB_DM`.
- V2.02 uses `SIM_DET`; V1.00 uses `SIMPRE`/`SIM_PRE`.
- V2.02 uses `DTR`/`RI`/`DCD`; V1.00 uses `UART_DTR`/`UART_RI`/`UART_DCD`.
- V2.02 uses `VDD_EXT`; V1.00 uses `VEXT`.
- V2.02 uses `GSM_ANT`/`FM_ANTP`/`FM_ANTN`;
  V1.00 uses `ANT`/`FM_ANT_P`/`FM_ANT_N`.
- V2.02 uses `RF_SYNC`; V1.00 uses `BPI_BUS1`.
- `BT_ANT` is SIM800H-only — should not be added to dat_07 for SIM800L.

## Recommended next actions

1. Add missing V2.02 pins to dat_07 with source = V2.02 (priority).
2. For each new record, capture page/section from V2.02 table.
3. Where a V2.02 pin has a V1.00 alias (see A1_dat07_pdf_pins.md),
   record the alias in `alternate_function` or `notes`.
4. Do not add `BT_ANT` (SIM800H-only).
5. After populating, update `status` to `partial` or `complete`
   depending on confidence in each record's source.
