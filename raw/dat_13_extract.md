# Raw Extraction — dat_13 (SIM Management DB)

**Source document:** `SIM800H&SIM800L_Hardware_Design_V2.02` (authoritative).

## Section 4.8.1 / Table 17 — SIM pin definition (V2.02, PDF page 38)

> "SIM_VDD 16 — Voltage supply for SIM card. Support 1.8V or 3V SIM card."
> "SIM_DATA 14 — SIM data input/output."
> "SIM_CLK 55 — SIM clock."
> "SIM_RST 15 — SIM reset."
> "SIM_DET 54 — SIM card detection."

## Section 4.8.2 — SIM card design guide (V2.02, PDF page 39)

> "Recommended to place a 100nF capacitor on SIM_VDD line and keep close to the
> SIM card holder."
> "Add some TVS which parasitic capacitance should not exceed 50pF."
> "Add 51 ohm resistor to (SIM_RST/SIM_CLK/SIM_DATA) signal could enhance ESD
> protection."

## Section 4.8.3 / Note (V2.02, PDF page 41)

> "Every time plug SIM card interval advice is greater than 2s. Otherwise may
> not be able to correct detection."

## Section 6.4 / Table 45 — SIM card interface characteristics (V2.02, PDF page 59)

> IIH/IIL -1.0 .. 1.0 uA; VIH min 1.4 V (1.8V SIM) / 2.4 V (3V SIM);
> VIL max 0.27/0.4 V; VOH min 1.62 V (1.8V SIM) / 2.7 V (3V SIM);
> VOL max 0.36/0.4 V.

## Section 6.5 / Table 46 — SIM_VDD characteristics (V2.02, PDF page 59)

> Output voltage: 1.8 V or 3.0 V; output current max: 10 mA.

## AT-command SIM records

Deferred to Phase 2a (AT Command Manual not available).
