# گزارش فاز ۲ — sim800l-data

## گام صفر: وضعیت AT Command Manual

**پاسخ:** `SIM800 Series_AT Command Manual.pdf` **در مخزن موجود نیست.**
هیچ مسیری (ریشه، `sources/`، `pdfs/`، پوشه والد) شامل این فایل نیست.
بنابراین تمام دیتاست‌های وابسته به Manual به‌صورت deferred یا partial
ساخته شدند. هیچ داده‌ای از دانش پیشین تولید نشد.

## دیتاست‌های افزوده‌شده

| ID | دیتاست | وضعیت | رکورد | منبع |
|----|--------|-------|-------|------|
| dat_01 | AT Command DB | deferred | 0 | AT Command Manual (موجود نیست) |
| dat_02 | URC DB | partial | 10 HW | V2.02 PDF (بخش HW) |
| dat_03 | Error Code DB | deferred | 0 | AT Command Manual |
| dat_08 | Firmware Compatibility Matrix | deferred | 0 | Manual + منابع ثانویه |
| dat_09 | SMS DB | deferred | 0 | AT Command Manual |
| dat_10 | GPRS/Data DB | deferred | 0 | AT Command Manual |
| dat_11 | HTTP/FTP/SSL DB | deferred | 0 | AT Command Manual |
| dat_12 | Audio DB | partial | 8 HW | V2.02 PDF (بخش HW) |
| dat_13 | SIM Management DB | partial | 8 HW | V2.02 PDF (بخش HW) |
| dat_14 | Operator/APN DB | deferred | 0 | MCC/MNC + APN databases |
| dat_17 | Certificate/Key Store | deferred | 0 | منابع ثانویه |
| dat_18 | Certification Data | deferred | 0 | منابع ثانویه |

## فیلدهای pending

- **dat_02**: `urc_at_*` — URCهای مربوط به AT commands تا زمان در دسترس
  بودن Manual به تعویق افتاده‌اند. فایل `data/urc/urc_at.yaml` با
  `records: []` ساخته شد.
- **dat_12**: `audio_at_*` — رکوردهای AT مربوط به صدا (AT+CMIC، AT+SIDET،
  AT+CLVL). فایل `data/audio/audio_at.yaml` خالی ساخته شد.
- **dat_13**: `sim_management_at_*` — رکوردهای AT مربوط به SIM (AT+CSDT
  و…). فایل `data/sim_management/sim_management_at.yaml` خالی ساخته شد.

## منابع گمشده

- `SIM800 Series_AT Command Manual.pdf` — مسئول deferred شدن ۹ دیتاست
  کامل و بخش AT سه دیتاست ترکیبی.
- منابع ثانویه (MCC/MNC databases، certificate/key store، certification
  bodies) — مسئول deferred شدن dat_14، dat_17، dat_18 و همچنین بخش
  ثانویهٔ dat_08 و dat_16.

## تنظیمات `_dataset_meta.yaml`

- دیتاست‌های deferred: `phase_completed: 2` + `status: deferred` +
  `reason: "INSUFFICIENT_RECORDS"` + `retry_count: 0`.
- دیتاست‌های partial (dat_02، dat_12، dat_13): طبق قانون ۱۲ پروژه،
  چون فقط بخش HW ساخته شده، `phase_completed: 1` + `status: partial` +
  `pending_fields` غیرخالی.
- dat_08 طبق قاعدهٔ اختصاصی: `phase_completed: 2` (در Phase 2 تلاش شد).

## به‌روزرسانی DATASET_MAP

`tools/validate.py` به‌روزرسانی شد و اکنون هر ۱۸ دیتاست را می‌شناسد.
پس از جایگزینی، کلیدهای مورد انتظار در متن خروجی اعتبارسنجی شدند تا
جایگزینی ناقص رخ ندهد.

## اسناد به‌روزرسانی‌شده

- `docs/source_mapping.md`
- `docs/conflict_log.md` (ردیف اطلاعاتی برای `dat_07_pinout_045` طبق قانون ۸)
- `docs/diagram_mapping.md`
- `docs/data_dictionary.md`
- `docs/validation_guide.md`
- `CHANGELOG.md`

## فایل‌های دست‌نخورده (به‌صورت عمدی)

طبق قوانین صریح پروژه، این فایل‌ها **به‌صورت عمدی دست‌نخورده** باقی
ماندند و تغییر نکردند:

- `README.md` در ریشهٔ مخزن و `sources/README.md`.
- `PHASE_1_REPORT.md`.
- `LICENSE` و `NOTICE`.
- تمام فایل‌های `tools/*.py` به‌جز `tools/validate.py` (که فقط
  `DATASET_MAP` در آن به‌روزرسانی شد).
