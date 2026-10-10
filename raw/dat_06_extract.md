# Raw Extraction — dat_06 (Init Sequence DB — hardware)

**Source document:** `SIM800H&SIM800L_Hardware_Design_V2.02` (authoritative)

## Section 4.1 — Power supply (V2.02, PDF page 20)

> "The power supply range is from 3.4V to 4.4V. Recommended voltage is 4.0V."
> "The transmitting burst will cause voltage drop and the power supply must be able to provide sufficient current up to 2A."
> "Ensure that the input voltage never drops below 3.0V even when current consumption rises to 2A."

## Section 4.2.1 — Power on sequence (V2.02, PDF pages 22–23)

Step 1: Apply VBAT (3.4–4.4V, capable of ≥2A peak).
Step 2: Pull PWRKEY low for at least 1 second.
Step 3: Release PWRKEY.
Step 4: Wait for URC `RDY` from serial port (only reported if a fixed baud rate is set with AT+IPR=x).
Step 5: Verify module ready: STATUS pin high, VDD_EXT = 2.8V.

## Section 4.5.4 — Software upgrade vs UART (V2.02, PDF page 33)

> "It is strongly recommended to lead the UART1_TXD, UART1_RXD, GND and PWRKEY pin to IO connector for the upgrading."

## Section 4.5.1 — Autobauding synchronization (V2.02, PDF page 30)

> "When DCE powers on with autobauding enabled, it is recommended to send 'AT' ... until DTE receives the 'OK' response."
> "The URC such as 'RDY', '+CFUN: 1' and '+CPIN: READY' will not be reported" with autobauding.