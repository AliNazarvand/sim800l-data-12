# TODO

## منابع گمشده
- [ ] SIM800 Series TCP/IP AT Command Manual — dat_10
- [ ] SIM800 Series HTTP AT Command Manual — dat_11
- [ ] SIM800 Series FTP AT Command Manual — dat_11
- [ ] SIM800 Series SSL AT Command Manual — dat_11, dat_17
- [ ] SIM800 Series Audio AT Command Manual — dat_12
- [ ] SIM800 Series SIM AT Command Manual — dat_13
- [ ] SIM800L Datasheet — dat_07
- [ ] SIM800 Series Sleep Mode Application Note — dat_15
- [ ] SIM800 Series URC Application Note — dat_02
- [ ] SIM800 Series Firmware Release Notes — dat_08
- [ ] SIM800 Series Certification Documents — dat_18
- [ ] GSMA / ITU / mcc-mnc.com — dat_14 (فقط ۵۲ رکورد نمونه)

## دیتاست‌های بلاک‌شده
- [ ] dat_08 — Release Notes
- [ ] dat_15 — پارامترهای ساختاریافته Power از PDF قابل استخراج خودکار نیست
- [ ] dat_17 — SSL Manual
- [ ] dat_18 — اسناد رسمی CE/FCC/...

## دیتاست‌های deferred
- [ ] dat_16 — EVB document

## دیتاست‌های partial
- [ ] dat_01, dat_02, dat_03, dat_04, dat_05, dat_06
- [ ] dat_07 — 75/78 رکورد annotate شده؛ نیازمند بازبینی جدول پین‌های PDF
- [ ] dat_09, dat_10, dat_11, dat_12, dat_13
- [ ] dat_14 — 52 رکورد external

## مشکل dat_15 — نیازمند کار دستی
- [ ] استخراج خودکار خطوط power از V2.02 منجر به ۳۵۱ رکورد بی‌ارزش شد (فقط خطوط متنی PDF کپی شده بودند، بدون value/unit). این رکوردها حذف شدند.
- [ ] dat_15 نیازمند استخراج دستی جدول‌های Power Consumption از V2.02 (صفحات مشخص).
- [ ] جدول‌های موردنیاز: Power Consumption table، Sleep Mode current، CFUN levels.
- [ ] منبع تکمیلی: SIM800 Series Sleep Mode Application Note.
- [ ] توصیه: این کار باید در یک نشست جداگانه و با بازبینی دستی PDF انجام شود، نه با اسکریپت auto-detection.

## محدودیت استخراج dat_07
- [ ] اسکریپت _rebuild_dat07.py صرفاً ۷۵ رکورد موجود را annotate کرده.
- [ ] استخراج واقعی جدول پین‌ها (تشخیص پین‌های غایب PDF) انجام نشده.
- [ ] بازبینی دستی جدول پین‌های V2.02 و V1.00 لازم است.
- [ ] ۳ رکورد حل‌نشده در dat_07 نیازمند بازبینی دستی.

## خطاهای L3 پذیرفته‌شده
- ۳۰۳ خطای cross-ref — رفع در خوشه B پس از کامل شدن dat_01.

## خوشه‌های در انتظار
- [ ] خوشه A3: dat_04 + dat_05 + dat_06
- [ ] خوشه A4: dat_16 Board/EVB (احتمالاً deferred)
- [ ] خوشه B: pending_blocked (وابسته به dat_01)
- [ ] بازگشت به dat_15 برای استخراج دستی (نشست جداگانه)

## قاعده جدید (از D-019)
- [ ] ممنوعیت auto-detection بر اساس کلیدواژه برای تولید رکورد داده. استخراج فقط با ساختار (جدول / بخش مشخص) و مقادیر عددی معتبر.