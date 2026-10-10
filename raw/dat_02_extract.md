# Raw Extraction — dat_02 (URC DB)

**Source document:** `SIM800H&SIM800L_Hardware_Design_V2.02` (authoritative).

## Section 4.2.1 — Power-on (V2.02, PDF page 23)

> "When power on procedure is completed, SIM800H&SIM800L will send following URC: RDY"

## Section 4.2.2.1 — Normal power down (V2.02, PDF page 24)

> "Before the completion of the power down procedure, the module will send URC: NORMAL POWER DOWN"

## Section 4.2.2.3 — Over/under-voltage (V2.02, PDF page 24)

> "If the voltage <= 3.5V ... UNDER-VOLTAGE WARNNING"
> "If the voltage >= 4.3V ... OVER-VOLTAGE WARNNING"
> "If the voltage < 3.4V ... UNDER-VOLTAGE POWER DOWN"
> "If the voltage > 4.4V ... OVER-VOLTAGE POWER DOWN"

## Section 4.2.2.4 — Over/under-temperature (V2.02, PDF page 24)

> "+CMTE: 1" (T >= +80C); "+CMTE: -1" (T <= -30C);
> "+CMTE: 2" (T > +85C); "+CMTE: -2" (T < -40C).

## AT-command URCs

Deferred to Phase 2a (AT Command Manual not available).
