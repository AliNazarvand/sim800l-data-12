# COVERAGE MEASUREMENT REPORT (R12) — v2

**⚠️ توجه:** این نسخه از اعداد **دستی** استفاده می‌کند.
نسخه‌ی قبلی از فرمول معکوس (`data_recs / pdf_hits`) استفاده می‌کرد
که به‌اشتباه پوشش را ۱۰۰٪ گزارش می‌کرد.

| دیتاست | رکورد در data | پارامتر در PDF | پوشش واقعی | coverage_estimate | regex signal |
|---|---|---|---|---|---|
| dat_04_timing | 20 | 18 | 61% | medium | 32 |
| dat_05_state_machine | 23 | 7 | 80% | medium | 3 |
| dat_06_init_sequence | 6 | 6 | 83% | medium | 25 |
| dat_07_hardware | 100 | 100 | 70% | medium | 11 |
| dat_15_power | 26 | 23 | 17% | low | 55 |

## یادداشت‌ها

- «پارامتر در PDF»: تعداد پارامتر مستقل در PDF (شمارش دستی).
- «پوشش واقعی»: نسبت پارامترهای ثبت‌شده در `data/` به کل پارامترهای PDF.
- «regex signal»: فقط برای اطلاع؛ معیار پوشش **نیست**.

## پارامترهای گم‌شده (نمونه‌ها)

### dat_04_timing
- NETLIGHT blink timings (64/800, 64/3000, 64/300ms) - p49
- VBAT over-voltage warning = 4.3V - p24
- VBAT over-voltage power-down = 4.4V - p24
- RESET V_IH=2.4V, V_IL=0.6V - p26
- Min functionality current = 0.83mA (fun=0) - p26
- PWM frequency 0-2kHz - p48

### dat_05_state_machine
- Ring/CSD FAX states not fully modeled

### dat_06_init_sequence
- Autobauding sync step (send 'AT' until 'OK')

### dat_07_hardware
- RF output power tables (Tables 53-54) - p63-64
- RF receive sensitivity (Table 55) - p64
- Operating frequencies (Table 56) - p64
- ESD characteristics (Table 52) - p62-63
- Moisture sensitivity + baking (Tables 57-58)
- Absolute maximum ratings (Table 42) - p58

### dat_15_power
- All GPRS data mode current values (1Rx/4Tx, 3Rx/2Tx, 4Rx/1Tx)
- Voice call current per band (GSM850/EGSM900/DCS1800/PCS1900)
- Min functionality currents for fun=0,4
- Bluetooth current (Search/Match/Connect)

