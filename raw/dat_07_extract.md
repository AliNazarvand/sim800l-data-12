# Raw Extraction — dat_07 (Hardware Reference DB)

**Source documents:**
- `SIM800H&SIM800L_Hardware_Design_V2.02` (primary, authoritative)
- `SIM800L_Hardware_Design_V1.00` (secondary, for V1.00-unique data)

## Section 3.1 — Pinout diagram (V2.02, PDF page 15)

> Figure 2: Pin assignment (Top view) — 88 pads, LGA package.

## Section 3.2 — Pin description (V2.02, PDF pages 16–17)

> Table 5: Pin description. Full enumeration of pin numbers, I/O direction, and function.

Direct excerpts:

> "VBAT 1, 42 I Power supply"
> "VRTC 56 I/O Power supply for RTC. It is recommended to connect with a battery or a capacitor (e.g. 4.7uF)."
> "VDD_EXT 18 O 2.8V power output"
> "PWRKEY 48 I PWRKEY should be pulled down at least 1 second and then released to power on/down the module. Internally pulled up to VBAT."
> "RESET 49 I Reset input (Active low)"
> "RF_SYNC 5 I/O Synchronizing signal of RF"
> "BT_ANT 36 I/O Connect Bluetooth antenna — Only SIM800H"

## Section 2.2 — Module information (V2.02, PDF page 11)

> Table 1: SIM800H FLASH 32Mbit, RAM 32Mbit; SIM800L FLASH 16Mbit, RAM 32Mbit.

## Section 6.1 — Absolute maximum ratings (V2.02, PDF page 58)

> Table 42: `VBAT max 4.5V`; `Current 0–2.0A`; `VBUS max 12V`.

## Section 6.2 — Recommended operating conditions (V2.02, PDF page 58)

> Table 43: `VBAT: min 3.4V, typ 4.0V, max 4.4V`; `TOPER: -40 / +25 / +85 °C`; `TSTG: -45 / +90 °C`.

## Section 6.3 — Digital interface characteristics (V2.02, PDF page 58)

> Table 44: `VIH 2.1–3.1V`, `VIL -0.3–0.7V`, `VOH 2.4–2.8V`, `VOL 0–0.4V`.

## Section 6.5–6.7 — SIM_VDD, VDD_EXT, VRTC (V2.02, PDF page 59)

> Table 46 (SIM_VDD): 1.8V or 3.0V, IO max 10mA.
> Table 47 (VDD_EXT): 2.7 / 2.8 / 2.9 V, IO max 50mA.
> Table 48 (VRTC): input 1.2 / 2.8 / 3.0 V, IO 2mA.

## Section 4.13 / 4.14 — ADC and PWM (V2.02, PDF pages 47–48)

> Table 29 (ADC): voltage range 0–2.8V; resolution 10 bits; sampling ≤1.0833 MHz.
> Table 30 (PWM): pin 26 PWM output.