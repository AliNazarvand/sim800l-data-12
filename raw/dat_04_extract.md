# Raw Extraction — dat_04 (Timing & Timeout DB)

**Source document:** `SIM800H&SIM800L_Hardware_Design_V2.02` (authoritative)

## Section 4.2.1 — PWRKEY power-on (V2.02, PDF page 22)

> "Customer can power on SIM800H&SIM800L by pulling down the PWRKEY pin for at least 1 second and release."

## Section 4.2.2.1 — PWRKEY power-down (V2.02, PDF page 23)

> Figure 13: Timing of power down — `1s < t < 33s` PWRKEY low window, `V_IL < 0.7V`, `t > 1.6s` until VDD_EXT/STATUS drop.

## Section 4.2.2.3 — Over/under-voltage thresholds (V2.02, PDF page 24)

> VBAT ≤ 3.5V → `UNDER-VOLTAGE WARNING`
> VBAT ≥ 4.3V → `OVER-VOLTAGE WARNING`
> VBAT ≤ 3.4V → `UNDER-VOLTAGE POWER DOWN`
> VBAT ≥ 4.4V → `OVER-VOLTAGE POWER DOWN`

## Section 4.2.2.5 — Restart by PWRKEY (V2.02, PDF page 25)

> Figure 14: `1s < T1 < 2s` PWRKEY low, then wait `T3 > 800ms` after STATUS low, then power on again.

## Section 4.2.3 / Table 7 / Figure 16 — RESET (V2.02, PDF pages 25–26)

> Table 7: `V_IH min 2.4V`, `V_IL max 0.6V`, `Low power time min 105ms`.
> Figure 16: `t > 105ms` RESET low pulse; `800ms` until VDD_EXT high; `2.7s` STATUS low period.

## Section 4.3.3 — Sleep Mode 1 wake (V2.02, PDF page 27)

> "The serial port will be active after DTR pin is pulled to low level for about 50ms."

## Section 4.3.4 — Sleep Mode 2 entry (V2.02, PDF page 27)

> "When there is no data transfer over 5 seconds on the RXD signal ... will enter sleep mode 2 automatically."

## Section 4.6 — RI behavior (V2.02, PDF page 34)

> "SMS: pin low for 120ms when a SMS is received."
> "URC: pin low for 120ms when some URCs are reported."

## Section 4.1 / Figure 8 — Transmit burst (V2.02, PDF pages 20–21)

> Figure 8: Burst duration `577 µs`, period `4.615 ms`, `Burst = 2A`, `Max VBAT drop = 350 mV`.

## Section 4.18.1 / Figure 48 — RF_SYNC timing (V2.02, PDF page 51)

> Figure 48: `220 µs` high (before burst), `577 µs` low.

## Section 4.8.3 — SIM hot-plug interval (V2.02, PDF page 41)

> "Every time plug SIM card interval advice is greater than 2s. Otherwise may not be able to correct detection."