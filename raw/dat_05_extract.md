# Raw Extraction — dat_05 (State Machine DB — hardware)

**Source document:** `SIM800H&SIM800L_Hardware_Design_V2.02` (authoritative)

## Section 4.2.1 — Power on (V2.02, PDF page 22)

> "Power on SIM800H&SIM800L by pulling down the PWRKEY pin for at least 1 second and release."
> "When power on procedure is completed, SIM800H&SIM800L will send following URC: RDY"

## Section 4.2.2 — Power down (V2.02, PDF page 23)

> Two normal methods: PWRKEY low ≥ 1s, or AT+CPOWD=1.
> Two abnormal methods: over/under voltage; over/under temperature.

## Section 4.2.2.1 — Power down by PWRKEY (V2.02, PDF page 23)

> "Before the completion of the power down procedure, the module will send URC: NORMALPOWERDOWN."

## Section 4.2.2.3 / 4.2.2.4 — Abnormal power-down (V2.02, PDF page 24)

> URCs: UNDER-VOLTAGE WARNING, OVER-VOLTAGE WARNING, UNDER-VOLTAGE POWER DOWN, OVER-VOLTAGE POWER DOWN, +CMTE:1, +CMTE:-1, +CMTE:2, +CMTE:-2.

## Section 4.2.3 — Reset (V2.02, PDF page 25)

> "SIM800H&SIM800L also has a RESET pin (pin 49) used to reset the module. This function is used as an emergency reset only when AT command 'AT+CPOWD=1' and the PWRKEY pin has no effect."

## Section 4.3 — Sleep mode (V2.02, PDF pages 26–27)

> AT+CSCLK=1 → DTR controls entry/exit. DTR high + no interrupt → sleep. DTR low ≥ 50ms → wake.
> AT+CSCLK=2 → enters after 5s no RXD data; wakes on RXD data (first char lost).

## Section 4.16 — STATUS pin (V2.02, PDF page 50)

> "The pin output is high when module is powered on, and output is low when module is powered down."