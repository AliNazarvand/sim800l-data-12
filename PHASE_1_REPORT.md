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