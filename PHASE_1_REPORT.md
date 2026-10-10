# گزارش فاز ۱ — sim800l-data

**وضعیت:** تکمیل‌شده با یک دیتاست partial و یک دیتاست deferred.

**منابع:** V1.00 و V2.02 در `sources/` استخراج و متن هر دو PDF در
`sources/extracted/` ذخیره شده است. V2.02 به‌عنوان مرجع قطعی اعمال شد.

---

## ۱. دیتاست‌های فاز ۱ و وضعیت نهایی

| ID | دیتاست | تعداد رکورد | وضعیت |
|----|--------|--------------|--------|
| dat_07 | Hardware Reference DB | 80 | partial |
| dat_04 | Timing & Timeout DB | 11 | complete |
| dat_15 | Power Management DB | 4 | partial |
| dat_05 | State Machine DB | 19 (7 states + 12 transitions) | complete |
| dat_06 | Init Sequence DB | 5 | complete |
| dat_16 | Board/EVB Definitions | 0 | deferred (INSUFFICIENT_RECORDS → Phase 2b) |

## ۲. دیتاست‌های partial

- **dat_07** — 50 رکورد pinout + 10 رکورد electrical + 10 رکورد power_consumption
  + 9 رکورد interfaces + 1 رکورد physical = 80 رکورد. وضعیت `partial` است
  چون برخی پین‌های GND به‌صورت گروهی ثبت شده‌اند و ممکن است در فاز ۲.الف
  به رکوردهای مستقل تفکیک شوند.
- **dat_15** — ۴ رکورد؛ رکورد MINIMUM_FUNCTIONALITY فیلدهای جریان را
  ندارد و `missing_reason: "DEFERRED_TO_PHASE_2A"` گرفته است.

## ۳. دیتاست‌های deferred

- **dat_16** — پس از ۳ تلاش، هیچ EVB با ≥۵ فیلد پر در هیچ‌کدام از PDFها
  یافت نشد. به Phase 2b منتقل شد.

## ۴. فیلدهای `DEFERRED_TO_PHASE_2A`

- `dat_15.MINIMUM_FUNCTIONALITY.current_consumption_typical`
- `dat_15.MINIMUM_FUNCTIONALITY.current_consumption_max`

## ۵. فیلدهای `CONFLICTING_SOURCES`

سه تعارض در `docs/conflict_log.md` ثبت شد:
1. `dat_04_timing_002.min_value`: V1.00 = 1.5s vs V2.02 = 1s
2. `dat_15_mode_003.current_consumption_typical`: V1.00 = 50µA vs V2.02 = 150µA
3. `dat_15_mode_003.current_consumption_max`: V1.00 = 60µA vs V2.02 = 200µA

همه با قاعده `V2.02_wins` حل شدند.

## ۶. یادداشت حقوقی

داده‌ها مشتق از اسناد SIMCom هستند؛ بازنشر عمومی محدودیت دارد.
`NOTICE` و `LICENSE` را ببینید.

> **یادآوری:** Phase 2a تنها با دستور صریح جدید و ارائه منابع ثانویه
> آغاز می‌شود.
---

## ۷. محدودیت استخراج متن از تصاویر شکل

برخی از مقادیر فنی مهم در **تصاویر شکل‌ها** قرار دارند، نه در متن
قابل انتخاب PDF. ابزار `pypdf` این مقادیر را نمی‌تواند از متن استخراج
کند. این مقادیر در `raw/*.md` ثبت شده‌اند، اما قابل تأیید خودکار از
`sources/extracted/v2.02.txt` نیستند:

| مقدار | منبع | رکورد مرتبط |
|-------|------|--------------|
| `577 us` (پهنای burst) | Figure 8 (ص ۲۱) | `dat_04_timing_005` |
| `4.615 ms` (دوره burst) | Figure 8 (ص ۲۱) | `dat_04_timing_005` |
| `220 us` (RF_SYNC high) | Figure 48 (ص ۵۱) | `dat_04_timing_007` |
| `33 s` (بالای پنجره PWRKEY low) | Figure 13 (ص ۲۳) | `dat_04_timing_002` |
| `1.5 s` (power-down، V1.00) | Figure 13 (ص ۲۵) | `dat_04_timing_002` |

**توضیح:** این مقادیر در حین استخراج **از متن شکل** یا با ابزار جایگزین
(`pymupdf` یا بازبینی بصری) خوانده شده‌اند. اعتبارسنجی خودکار
`validate.py` فقط ساختار داده را تأیید می‌کند، نه درستی این مقادیر عددی.

**مقادیر متنی تأیید‌شده:** مقادیر متنی دیگر (شامل `VBAT 1,42`,
`VRTC 56`, `VDD_EXT 18`, `Normal power down`, `emergency reset`,
`105ms`, `4.5 V`, `6.8`, `1.04`) در `sources/extracted/v2.02.txt`
تأیید شدند.

**بازبینی انسانی لازم:** برای تأیید قطعی مقادیر جدول بالا، در فاز ۲.الف
از `pymupdf` با `page.get_text("words")` یا از بازبینی دستی PDF استفاده
خواهد شد. این مقادیر در فاز ۲.الف با علامت `DEFERRED_TO_PHASE_2A`
بازبینی می‌شوند.