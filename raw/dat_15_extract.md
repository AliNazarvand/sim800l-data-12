# Raw Extraction — dat_15 (Power Management DB)

**Source document:** `SIM800H&SIM800L_Hardware_Design_V2.02` (authoritative)

## Section 2.3 — Operating modes (V2.02, PDF page 13, Table 4)

> Normal operation / GSM/GPRS SLEEP / GSM IDLE / GSM TALK / GPRS STANDBY / Power down / Minimum functionality.

## Section 4.3 — Power Saving Mode (V2.02, PDF pages 26–27)

> "SIM800H&SIM800L has two power saving modes: Minimum functionality mode and sleep mode."
> AT+CSCLK=1 → Sleep Mode 1 (DTR-controlled)
> AT+CSCLK=2 → Sleep Mode 2 (auto after 5s no RXD data)
> AT+CFUN=0 → Minimum functionality
> AT+CFUN=1 → Full functionality (default)
> AT+CFUN=4 → Flight mode

## Section 6.8 / Table 49 — Current consumption (V2.02, PDF page 60)

Measured at VBAT=3.8V, PCL=5:
> Power down mode: 150 / 200 µA
> Sleep mode (BS-PA-MFRMS=9): 1.04 mA; (MFRMS=5): 1.14 mA; (MFRMS=2): 1.57 mA
> Idle mode: 17.38 mA (all four bands)
> Voice call: GSM850 221.11 mA; EGSM900 238.44 mA; DCS1800 157.48 mA; PCS1900 159.22 mA
> GPRS Data 1Rx/4Tx: 491.79 / 529.84 / 333.16 / 336.28 mA
> GPRS Data 3Rx/2Tx: 359.75 / 385.73 / 250.54 / 251.30 mA
> GPRS Data 4Rx/1Tx: 233.87 / 249.85 / 174.13 / 174.94 mA
> Peak current (TX burst): 2.0 A

## Note on MINIMUM_FUNCTIONALITY current

Table 8 in V2.02 is partially corrupted in the extracted text. The exact
numeric value for current consumption in minimum functionality mode
could not be extracted reliably and has been marked as
`DEFERRED_TO_PHASE_2A` at the record level.