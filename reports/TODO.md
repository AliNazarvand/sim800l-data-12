# TODO

## منابع گمشده
- [ ] SIM800 Series TCP/IP AT Command Manual — موردنیاز برای dat_10
- [ ] SIM800 Series HTTP AT Command Manual — موردنیاز برای dat_11
- [ ] SIM800 Series FTP AT Command Manual — موردنیاز برای dat_11
- [ ] SIM800 Series SSL AT Command Manual — موردنیاز برای dat_11, dat_17
- [ ] SIM800 Series Audio AT Command Manual — موردنیاز برای dat_12
- [ ] SIM800 Series SIM AT Command Manual — موردنیاز برای dat_13
- [ ] SIM800L Datasheet — موردنیاز برای dat_07
- [ ] SIM800 Series Sleep Mode Application Note — موردنیاز برای dat_15
- [ ] SIM800 Series URC Application Note — موردنیاز برای dat_02
- [ ] SIM800 Series Firmware Release Notes — موردنیاز برای dat_08
- [ ] SIM800 Series Certification Documents — موردنیاز برای dat_18
- [ ] GSMA / ITU / mcc-mnc.com — موردنیاز برای dat_14 (اختیاری، در دسترس نبود؛ فقط 52 رکورد نمونه)

## دیتاست‌های بلاک‌شده (منبع اصلی در دسترس نیست)
- [ ] dat_08 — نیازمند Release Notes
- [ ] dat_17 — نیازمند SSL Manual
- [ ] dat_18 — نیازمند اسناد رسمی CE/FCC/...

## دیتاست‌های partial (منبع موجود، استخراج ناقص)
- [ ] dat_01 — needs re-verification of source.page/section against AT Manual V1.01
- [ ] dat_07 — needs re-verification of source.page/section against V2.02/V1.00
- [ ] dat_14 — 52 رکورد نمونه؛ source_type=external، confidence<=0.7 (اختیاری؛ تکمیل کامل نیازمند GSMA/ITU)

## دیتاست‌های deferred
- [ ] dat_16 — EVB document not available

## رکوردهای دارای source.date پاک‌شده (R3: unknown / 0.0)
- dat_14: 52 رکورد (مقادیر date پاک شد، status=unknown، confidence=0.0 در آن مرحله؛ سپس در این گام confidence<=0.7 بازنشانی شد)

## خطاهای cross-ref پذیرفته‌شده (L3)
- 303 خطای L3 از دیتاست‌های partial — رفع در خوشه B پس از کامل شدن dat_01
- جزئیات در reports/CROSS_REF_REPORT.md

## خوشه‌های در انتظار
- [ ] خوشه A — شروع با A1: dat_07 (partial — نیازمند استخراج دقیق از PDF)
- [ ] خوشه B — pending_blocked (وابسته به dat_01 که partial است)