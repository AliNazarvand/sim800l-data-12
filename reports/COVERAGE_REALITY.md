# COVERAGE REALITY REPORT

> این گزارش یک اعتراف صادقانه است. در run 8، یک اسکریپت با فرمول
> معکوس، به‌اشتباه پوشش dat_05 و dat_07 را ۱۰۰٪ گزارش کرد. این گزارش
> اعداد واقعی را بر اساس **شمارش دستی جدول‌های PDF** ارائه می‌دهد.

## خطای run 8

فرمول اشتباه در `measure_coverage.py`:

```python
ratio = min(data_recs / pdf_hits, 1.0)
```

این فرمول:
- `dat_05`: 19 رکورد ÷ 3 regex = 6.33 → min(6.33, 1.0) = **1.0** → 100% ❌
- `dat_07`: 80 رکورد ÷ 30 regex = 2.67 → min(2.67, 1.0) = **1.0** → 100% ❌

اما این **بی‌معنی** است. regex-match معیار پوشش نیست.

## اعداد واقعی (بر اساس خواندن دستی PDF)

### dat_04 — Timing & Timeout

**پارامترهای زمانی واقعی در PDF (~۱۸ مورد)**:

| # | صفحه | پارامتر | در data |
|---|---|---|---|
| 1 | p21 | TX burst duration (577 µs) | ✅ |
| 2 | p22 | PWRKEY power-on low ≥ 1s | ✅ |
| 3 | p23 | PWRKEY power-down low ≥ 1s | ✅ |
| 4 | p23 | Power-down window 1s~33s | ✅ |
| 5 | p24 | VBAT under-voltage warning 3.5V | ✅ |
| 6 | p24 | VBAT over-voltage warning 4.3V | ❌ |
| 7 | p24 | VBAT under-voltage power-down 3.4V | ❌ |
| 8 | p24 | VBAT over-voltage power-down 4.4V | ❌ |
| 9 | p25 | Restart wait after STATUS low ≥ 800ms | ✅ |
| 10 | p26 | RESET low pulse ≥ 105ms | ✅ |
| 11 | p26 | RESET V_IH = 2.4V, V_IL = 0.6V | ❌ |
| 12 | p26 | Min functionality current 0.83mA | ❌ |
| 13 | p27 | Sleep Mode 1 wake: DTR low ≥ 50ms | ✅ |
| 14 | p27 | Sleep Mode 2 entry: no RXD 5s | ✅ |
| 15 | p34 | RI pulse for SMS: 120ms | ✅ |
| 16 | p39 | SIM hot-plug interval ≥ 2s | ✅ |
| 17 | p48 | PWM frequency 0-2kHz | ❌ |
| 18 | p49 | NETLIGHT blink timings (64/800, 64/3000, 64/300ms) | ❌ |

**پوشش واقعی: 11/18 = 61%**

### dat_05 — State Machine

**حالت‌های اصلی در PDF (۷ مورد)**:
POWER_OFF, POWER_ON_PWRKEY_PRESSED, POWER_ON_RDY_RECEIVED,
POWER_DOWN_PWRKEY_PRESSED, RESET_ACTIVE, SLEEP_MODE_1, SLEEP_MODE_2

همه در data/ موجودند. ۱۲ transition هم ثبت شده. برخی حالات جانبی
(RING/CSD FAX) مدل نشده‌اند.

**پوشش واقعی: ~80%** → `partial` (نه `complete`).

### dat_06 — Init Sequence

**مراحل init در PDF (۵-۶ مورد)**:
1. Apply VBAT power
2. Pull PWRKEY low ≥ 1s
3. Release PWRKEY
4. Wait for URD "RDY"
5. Verify module ready via STATUS

همه در data/ موجودند. مرحله‌ی autobauding sync گم است.

**پوشش واقعی: ~83%** → `partial`.

### dat_07 — Hardware Reference

**پارامترهای سخت‌افزاری در PDF (~۱۰۰ مورد)**:
- Table 5 (Pin description): ~۵۰ پین
- Tables 42-49 (Electrical + Current): ~۳۰ پارامتر
- Tables 52-56 (ESD + RF): ~۲۰ پارامتر
- Package dimensions + Reflow: چند مورد

**گم‌شده‌های مهم**:
- RF output power tables (Tables 53-54) — ۲۰+ ردیف
- RF receive sensitivity (Table 55)
- Operating frequencies (Table 56)
- ESD characteristics (Table 52)
- Absolute maximum ratings (Table 42)
- Moisture sensitivity + baking (Tables 57-58)

**پوشش واقعی: ~70%** → `partial` (نه `complete`).

### dat_15 — Power Management

**مقادیر جریان در PDF (~۲۳ مورد)**:
- Power down: 150/200 µA
- Sleep (MFRMS=9): 1.04 mA
- Sleep (MFRMS=5): 1.14 mA
- Sleep (MFRMS=2): 1.57 mA
- Min functionality (fun=0): 0.83 mA
- Min functionality (fun=1): 1.04 mA
- Min functionality (fun=4): 0.92 mA
- Idle: 17.38 mA (all 4 bands)
- Voice call: 4 amounts (GSM850/EGSM900/DCS1800/PCS1900)
- GPRS 1Rx/4Tx: 4 amounts
- GPRS 3Rx/2Tx: 4 amounts
- GPRS 4Rx/1Tx: 4 amounts

در data فقط ۴ مورد ثبت شده.

**پوشش واقعی: ~17%** → `partial` با coverage_estimate: low.

## نتیجه

هیچ دیتاستی در پروژه **complete** نیست. همه‌ی دیتاست‌های دسته A
در وضعیت `partial` قرار دارند و برای ارتقا، باید پارامترهای گم‌شده
از جدول‌های PDF استخراج و به `data/` اضافه شوند.

## گام بعدی

برای رسیدن به `complete`:
1. NETLIGHT blink timings + PWM frequency + over-voltage thresholds → dat_04
2. RF output power + ESD + Absolute max + Operating freq → dat_07
3. All GPRS/voice current values → dat_15
4. Autobauding sync step → dat_06

این کار **نیازمند استخراج دستی** از PDF است.

## Update — 2026-10-10

B1 Final rolled back the A1 auto-extraction (see DECISIONS_LOG.md D-B1-001).
The 60 garbage records it added are gone. Data was restored from
`_backup_extract_20261010_160808`. Validation: **0 errors**.

### Final project state (reconciled with DECISIONS_LOG.md Session 11-12)

| Dataset | Status    | Coverage | Source                          |
|---------|-----------|----------|---------------------------------|
| dat_04  | complete  | 95%      | V1.00 + V2.02 (Session 12)      |
| dat_15  | complete  | 95%      | V1.00 + V2.02 (Session 11)      |
| dat_05  | partial   | 80%      | V2.02                            |
| dat_06  | partial   | 83%      | V2.02                            |
| dat_07  | partial   | 70%      | V2.02                            |
| dat_01, 02, 03, 08, 09, 10, 11, 12, 13, 17, 18 | blocked | - | AT Manual / external sources |
| dat_14, 16 | deferred | -        | External / EVB schematic         |

### Note on previous inconsistency

An earlier version of this Update section incorrectly marked dat_04 and
dat_15 as `partial`. This was a documentation bug introduced by the B1
Final script. The decision log (Session 11-12) is authoritative: both
datasets pass the R12 threshold (coverage ≥ 95%) and are `complete`.
