# گزارش فاز ۲c — sim800l-data

## گام صفر: وضعیت منبع AT Command Manual

**پاسخ:** `SIM800 Series_AT Command Manual.pdf` **در مخزن موجود نیست.**
بنابراین این فاز به‌صورت **best-effort** و فقط با استخراج AT commandهای
ذکرشده در همان دو PDF سخت‌افزاری انجام شد. هیچ داده‌ای از دانش پیشین
تولید نشد.

## دیتاست‌های تغییر‌یافته

| ID | دیتاست | قبل | بعد | وضعیت |
|----|--------|-----|-----|--------|
| dat_01 | AT Command DB | 0 (deferred) | 18 | partial |
| dat_02 | URC DB | 10 (partial) | 12 | partial |
| dat_09 | SMS DB | 0 (deferred) | 3 | partial |
| dat_10 | GPRS/Data DB | 0 (deferred) | 7 | partial |

## جزئیات

### dat_01 — 18 AT command از دو PDF سخت‌افزاری
AT+CBAND, AT+CPOWD, AT+CFUN, AT+CSCLK (×2), AT+IPR, AT+CBC, AT+CMTE,
AT+CADC, AT+SPWM, AT+SGPIO, AT+CSDT, AT+CMIC, AT+SIDET, AT+CLVL,
AT+IFC, AT+CMNRP, AT+SJDR.

فیلدهای `parameters` و `responses` به‌صورت موقت خالی یا عمومی ثبت شدند
تا در فاز بعدی (با Manual) کامل شوند.

### dat_02 — 2 URC اضافه شد
`+CFUN: 1` و `+CPIN: READY` (هر دو در بخش 4.5.1 ذکر شده‌اند).

### dat_09 — 3 رکورد capability
حالت‌های SMS، محل ذخیره، اطلاع‌رسانی از طریق RI.

### dat_10 — 7 رکورد capability
multi-slot class، coding schemes، PPP، TCP/IP، PBCCH، CSD، نرخ داده.

## Schemaها

سه اسکیمای `dat_01`, `dat_09`, `dat_10` بازتولید شدند تا فیلدهای جدید
را مجاز کنند. بقیه اسکیماها دست‌نخورده ماندند.

## منابع گمشده (باقی‌مانده برای فاز بعدی)

- `SIM800 Series_AT Command Manual.pdf` — برای تکمیل:
  - syntax/parameters/responses در dat_01
  - URCهای AT اضافه در dat_02
  - AT commandهای SMS در dat_09
  - AT commandهای GPRS/Data در dat_10
  - کل dat_03 (CME/CMS)، dat_08 (firmware)، dat_11 (HTTP/FTP/SSL)
  - بخش AT دیتاست‌های dat_12 و dat_13

## به‌روزرسانی‌شده

- `CHANGELOG.md` → v1.2.0
- `docs/source_mapping.md` → بلوک «Phase 2c additions»
- `docs/data_dictionary.md` → بلوک «Phase 2c updates»
- `docs/validation_guide.md` → بلوک «Phase 2c additions»

## فایل‌های دست‌نخورده (به‌صورت عمدی)

- `README.md` (ریشه و `sources/README.md`)
- `PHASE_1_REPORT.md`
- `LICENSE` و `NOTICE`
- `tools/*.py` (به‌جز validate.py که در فاز ۲ به‌روز شد و در این فاز دست نخورد)

## نتیجهٔ validate و generate_json

پس از اجرا و اجرای دستورات زیر تأیید می‌شود:

```
python tools/validate.py           # باید OK: validation passed بدهد
python tools/generate_json.py      # باید JSONهای جدید را بسازد
python tools/generate_json.py --check  # باید OK: in sync بدهد
```
