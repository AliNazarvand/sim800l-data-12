# TODO — Missing Sources & Blockers

**Last updated:** 2026-10-10

## Missing primary sources

- [ ] **SIM800 Series AT Command Manual** — blocks dat_01, 02, 03, 09, 10, 11, 12, 13, 17
- [ ] SIM800 Series TCP/IP AT Command Manual — blocks dat_10
- [ ] SIM800 Series HTTP AT Command Manual — blocks dat_11
- [ ] SIM800 Series FTP AT Command Manual — blocks dat_11
- [ ] SIM800 Series SSL AT Command Manual — blocks dat_11, 17
- [ ] SIM800 Series Audio AT Command Manual — blocks dat_12
- [ ] SIM800 Series Firmware Release Notes — blocks dat_08
- [ ] SIM800L EVB Schematic — blocks dat_16
- [ ] CE / FCC / GCF / PTCRB Certificates — blocks dat_18

## Partial datasets — remaining work

### dat_05 (State Machine) — currently 80%
- Missing: Ring/CSD FAX states
- Requires: AT Command Manual (state machine section) or PDF update

### dat_07 (Hardware Reference) — currently 70%
- Missing: Moisture sensitivity + baking (Tables 57-58 of v2.02)
- All other items extracted: RF power, ESD, AbsMax, frequencies

## Blocked datasets (11)

- dat_01, dat_02, dat_03, dat_08, dat_09, dat_10, dat_11, dat_12, dat_13,
  dat_17, dat_18

## Deferred datasets (2)

- dat_14 (Operator/APN) — optional, needs external source
- dat_16 (Board/EVB) — needs official EVB schematic

## How to unblock

1. Obtain the SIM800 Series AT Command Manual (V1.09+).
2. Obtain protocol manuals (TCP/IP, HTTP, FTP, SSL, Audio).
3. Obtain Release Notes and EVB schematic.
4. Re-run extraction, cross-ref, and validation pipelines.

## Note on dat_06

dat_06 (Init Sequence) is **complete** as of Session 12 — autobaud sync
was added, all 6 init steps covered.
