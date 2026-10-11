# TODO

## Blocked datasets
- [ ] dat_08 Firmware: Release Notes not available
- [ ] dat_17 Certificate/Key Store: SSL Manual not available
- [ ] dat_18 Certification: certification documents not available

## Deferred datasets
- [ ] dat_16 Board/EVB: EVB document not available

## Partial datasets (sourced but params_pct < 50%)
- [ ] dat_03 Error Code (params via recovery_steps)
- [ ] dat_04 Timing (values)
- [ ] dat_11 HTTP/FTP/SSL (specialist)
- [ ] dat_14 Operator/APN (external)
- [ ] dat_15 Power Management

## Missing sources (priority)
1. [ ] SIM800 Series HTTP AT Command Manual (highest — dat_11)
2. [ ] SIM800 Series FTP AT Command Manual (dat_11)
3. [ ] SIM800 Series SSL AT Command Manual (dat_11, dat_17)
4. [ ] SIM800 Series Audio AT Command Manual (dat_12)
5. [ ] SIM800 Series SIM AT Command Manual (dat_13)
6. [ ] SIM800 Series TCP/IP AT Command Manual (dat_10)
7. [ ] SIM800 Series Sleep Mode Application Note (dat_15)
8. [ ] SIM800 Series Firmware Release Notes (dat_08)
9. [ ] SIM800 Series Certification Documents (dat_18)
10. [ ] GSMA / ITU / mcc-mnc.com for APN (dat_14)
11. [ ] SIM800L Datasheet (dat_07)
12. [ ] EVB Schematic (dat_16)

## Notes
- D11 criteria: complete = with_page==count AND params_pct >= 50%
- L3 whitelist extended in D11.