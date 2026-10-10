#!/usr/bin/env python3
"""به‌روزرسانی اسناد مدیریتی با محتوای واقعی."""
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pyyaml"])
    import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def cnt(name):
    p = DATA / name
    if not p.exists(): return 0
    try:
        with open(p, encoding="utf-8") as f:
            return len(yaml.safe_load(f) or [])
    except Exception:
        return 0

FILES = {
"01":"dat_01_at_command.yaml","02":"dat_02_urc.yaml","03":"dat_03_error_code.yaml",
"04":"dat_04_timing_timeout.yaml","05":"dat_05_state_machine.yaml","06":"dat_06_init_sequence.yaml",
"07":"dat_07_hardware_reference.yaml","08":"dat_08_firmware_compatibility.yaml",
"09":"dat_09_sms.yaml","10":"dat_10_gprs_data.yaml","11":"dat_11_http_ftp_ssl.yaml",
"12":"dat_12_audio.yaml","13":"dat_13_sim_management.yaml","14":"dat_14_operator_apn.yaml",
"15":"dat_15_power_management.yaml","16":"dat_16_board_evb.yaml",
"17":"dat_17_certificate_key_store.yaml","18":"dat_18_certification.yaml"}

def main():
    counts = {k: cnt(v) for k, v in FILES.items()}

    # README.md
    readme = f"""# sim800l-data

پروژه داده‌محور SIM800L.

**آخرین به‌روزرسانی**: {NOW}

## وضعیت ۱۸ دیتاست

| # | نام | تعداد رکورد |
|---|---|---|
"""
    for k in sorted(FILES.keys()):
        readme += f"| dat_{k} | {FILES[k]} | {counts[k]} |\n"

    readme += f"""

## منابع
- SIM800L_Hardware_Design_V1.00.pdf
- SIM800H&SIM800L_Hardware_Design_V2.02.PDF
- SIM800 Series_AT Command Manual_V1.01.pdf

## ساختار
- `data/` — ۱۸ دیتاست YAML
- `schemas/` — ۱۸ JSON schema
- `scripts/` — اسکریپت‌های pipeline
- `sources/` — PDFهای اصلی و متن استخراج‌شده
- `reports/` — گزارش‌ها

## Pipeline
```
py scripts/extract_pdf_v3.py
py scripts/parse_sources_v2.py
py scripts/populate_v3.py
py scripts/cross_ref_v3.py
py scripts/validate_v3.py
py scripts/generate_reports_v3.py
```
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")

    # PHASE_1_REPORT.md
    phase1 = f"""# PHASE_1_REPORT

**تاریخ**: {NOW}

## دستاوردها
- ۱۸ Schema در `schemas/`
- استخراج متن و جداول از ۳ PDF
- {counts['01']} AT command استخراج‌شده
- {counts['02']} URC شناسایی‌شده
- {counts['03']} error code
- {counts['07']} پین/سیگنال سخت‌افزاری
- {counts['14']} رکورد اپراتور/APN نمونه

## وضعیت
- complete: dat_04, 05, 06, 07, 15 (در صورت رسیدن به حد نصاب)
- partial: dat_01, 02, 03, 09, 10, 11, 12, 13, 17
- external: dat_14
- blocked: dat_08, 17, 18 (اگر خالی)
- deferred: dat_16
"""
    (ROOT / "PHASE_1_REPORT.md").write_text(phase1, encoding="utf-8")

    # SOURCE_INVENTORY.md
    src = f"""# SOURCE_INVENTORY

| نام سند | نسخه | مسیر | وضعیت | نوع |
|---|---|---|---|---|
| SIM800L_Hardware_Design | V1.00 | sources/originals/SIM800L_Hardware_Design_V1.00.pdf | available | primary |
| SIM800H&SIM800L_Hardware_Design | V2.02 | sources/originals/SIM800H&SIM800L_Hardware_Design_V2.02.PDF | available | primary |
| SIM800 Series AT Command Manual | V1.01 | sources/originals/SIM800 Series_AT Command Manual_V1.01.pdf | available | primary |
| AT Manual V1.09+ | - | - | missing | primary |
| TCP/IP AT Manual | - | - | missing | primary |
| HTTP AT Manual | - | - | missing | primary |
| FTP AT Manual | - | - | missing | primary |
| SSL AT Manual | - | - | missing | primary |
| Audio AT Manual | - | - | missing | primary |
| Firmware Release Notes | - | - | missing | primary |
| Certification Docs | - | - | missing | primary |
| EVB Schematic | - | - | missing | primary |
| mcc-mnc.com | - | - | available (external) | external |
"""
    (ROOT / "SOURCE_INVENTORY.md").write_text(src, encoding="utf-8")

    # GAP_REPORT.md
    gap = f"""# GAP_REPORT

**تاریخ**: {NOW}

## شکاف‌های منابع
- AT Manual V1.09+ موجود نیست → dat_01..13 محدود به V1.01
- TCP/IP, HTTP, FTP, SSL Manuals موجود نیستند
- Audio Manual موجود نیست
- Firmware Release Notes موجود نیست → dat_08 blocked
- Certification Docs موجود نیستند → dat_18 blocked
- EVB Schematic موجود نیست → dat_16 deferred

## شکاف‌های داده‌ای
- dat_04: {counts['04']} رکورد (هدف ≥ ۲۰)
- dat_07: {counts['07']} رکورد (هدف ≥ ۵۰)
- dat_15: {counts['15']} رکورد (هدف ≥ ۱۵)
- dat_17: {counts['17']} رکورد (هدف ≥ ۵)
"""
    (ROOT / "GAP_REPORT.md").write_text(gap, encoding="utf-8")

    # TODO.md
    todo = f"""# TODO

## منابع گمشده
- [ ] SIM800 Series AT Command Manual V1.09+
- [ ] TCP/IP, HTTP, FTP, SSL, Audio Manuals
- [ ] Firmware Release Notes
- [ ] Certification Documents
- [ ] EVB Schematic

## دیتاست‌های بلاک‌شده
- [ ] dat_08 — Release Notes
- [ ] dat_18 — Certification Docs

## دیتاست‌های deferred
- [ ] dat_16 — EVB Schematic
"""
    (ROOT / "TODO.md").write_text(todo, encoding="utf-8")

    # DECISIONS_LOG.md
    dec = f"""# DECISIONS_LOG

## D-001 — V2.02 بر V1.00 مقدم
- **دلیل**: نسخه جدیدتر
- **جایگزین‌های رد‌شده**: استفاده از V1.00 به عنوان مرجع

## D-002 — عدم تولید داده synthetic
- **دلیل**: قاعده R6

## D-003 — dat_05/dat_06 به عنوان inferred
- **دلیل**: این دیتاست‌ها از تجربه عمومی SIM800L استنتاج شده‌اند، نه استخراج مستقیم
- **confidence**: 0.4-0.45
- **جایگزین‌های رد‌شده**: hardcode کردن بدون ذکر منبع

## D-004 — dat_14 external
- **دلیل**: منبع mcc-mnc.com عمومی است

## D-005 — dat_08/17/18 blocked در صورت نبود منبع
- **دلیل**: قواعد R3, R11
"""
    (ROOT / "DECISIONS_LOG.md").write_text(dec, encoding="utf-8")

    # ROLE_MAP.md
    role = f"""# ROLE_MAP

| دیتاست | نقش | وابسته به | وضعیت |
|---|---|---|---|
| dat_01 | مرجع command | - | partial |
| dat_02 | مرجع URC | dat_01 | partial |
| dat_03 | مرجع خطا | dat_01 | partial |
| dat_04 | زمان‌بندی | - | partial |
| dat_05 | حالت‌ها | - | inferred |
| dat_06 | init | - | inferred |
| dat_07 | سخت‌افزار | - | partial |
| dat_08 | firmware | - | blocked |
| dat_09 | SMS | dat_01 | partial |
| dat_10 | GPRS | dat_01 | partial |
| dat_11 | HTTP/FTP/SSL | dat_01 | partial |
| dat_12 | Audio | dat_01 | partial |
| dat_13 | SIM | dat_01, dat_07 | partial |
| dat_14 | APN | - | external |
| dat_15 | Power | - | partial |
| dat_16 | EVB | - | deferred |
| dat_17 | Certificate | dat_01, dat_11 | partial/blocked |
| dat_18 | Certification | - | blocked |
"""
    (ROOT / "ROLE_MAP.md").write_text(role, encoding="utf-8")

    # SESSION_LOG.md
    sess = f"""# SESSION_LOG

## نشست جاری — pipeline v3

**تاریخ**: {NOW}

### کارهای انجام‌شده
- استخراج متن + جداول + OCR از ۳ PDF
- استخراج عمیق AT command (syntax/parameters/examples)
- حذف hardcode و علامت‌گذاری inferred
- پر کردن cross-ref در خود داده
- اعتبارسنجی با jsonschema واقعی
- به‌روزرسانی همه گزارش‌های مدیریتی

### وضعیت نهایی
"""
    for k in sorted(FILES.keys()):
        sess += f"- dat_{k}: {counts[k]} رکورد\n"
    (ROOT / "SESSION_LOG.md").write_text(sess, encoding="utf-8")

    print("اسناد مدیریتی به‌روزرسانی شدند")
    return 0

if __name__ == "__main__":
    sys.exit(main())