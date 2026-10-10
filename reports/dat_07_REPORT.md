# dat_07_REPORT — Hardware Reference

تاریخ: 2026-10-10T20:37:12Z

## خلاصه
- رکوردهای استخراج‌شده: **78**
- منبع V2.02: 57
- منبع V1.00: 21

## توزیع category
- Unclassified: 36
- SIM: 12
- UART: 10
- Audio: 8
- GPIO: 3
- USB: 3
- Power: 2
- NETLIGHT: 1
- PWM: 1
- PWRKEY: 1
- STATUS: 1

## یادداشت
- وضعیت دیتاست: `partial` (فیلدهای voltage/current/esd خودکار استخراج نشده‌اند).
- تمام رکوردها از جدول‌های pin استخراج شده‌اند و `source` دارند.
- برای رسیدن به `complete` نیاز به بازبینی دستی و تکمیل voltage/current از متن manual است.

## کار باقی‌مانده
1. بازبینی رکوردهای Unclassified و انتقال به دسته مناسب.
2. تکمیل voltage_min/typ/max، current_typ/max از متن manual.
3. تنظیم direction (input/output/power/ground) برای هر pin.