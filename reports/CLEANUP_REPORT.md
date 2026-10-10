# Cleanup Report

## خلاصه

پروژه با یک خطای استخراج بدون فیلتر مواجه شده بود:
- **6125** فایل PNG در sources/extracted/figures/
- **735** فایل CSV در sources/extracted/tables/
- **0** فایل در sources/extracted/ocr/

مجموع: **6860 فایل** که عمدتاً آیکون، خط تزئینی، header/footer تکراری، یا
تصاویر ریز بوده‌اند و هیچ ارزش دانشی ندارند.

## اقدامات انجام‌شده

| # | اقدام | نتیجه |
|---|-------|-------|
| 1 | حذف فایل‌های اضافی figures/tables/ocr | حذف 6860 فایل |
| 2 | افزودن به .gitignore | پوشه‌های حجیم دیگر commit نمی‌شوند |
| 3 | افزودن .gitkeep به پوشه‌ها | ساختار پوشه حفظ می‌شود |
| 4 | بازنویسی xtract_figures.py | فیلتر ابعاد/حجم/hash |
| 5 | بازنویسی xtract_tables.py | فیلتر ردیف/ستون/سلول |
| 6 | حفظ فایل‌های .txt و manifest.json | متن اصلی PDFها دست‌نخورده |

## معیارهای جدید فیلتر

### extract_figures.py
- حداقل ابعاد: **100x100 پیکسل**
- حداقل حجم فایل: **5 KB**
- حذف تصاویر تکراری با **SHA-256 hash**
- تبدیل CMYK به RGB قبل از ذخیره

### extract_tables.py
- حداقل **2 ردیف** داده
- حداقل **2 ستون** داده
- حداقل **4 سلول غیرخالی**

## فایل‌های حفظ‌شده (tracked در git)

- sources/extracted/*.txt - متن کامل استخراج‌شده از PDFها
- sources/extracted/*.manifest.json - اطلاعات نسخه و hash
- sources/originals/* - PDFهای اصلی

## فایل‌های محلی (untracked در git)

- sources/extracted/figures/* - در صورت نیاز بازتولید می‌شوند
- sources/extracted/tables/* - در صورت نیاز بازتولید می‌شوند
- sources/extracted/ocr/* - در صورت نیاز بازتولید می‌شوند

## بازتولید

`ash
pip install pymupdf pdfplumber
python scripts/extract_figures.py
python scripts/extract_tables.py
`

## نتیجه

- تعداد فایل‌های پروژه از **~6860** به زیر **500** کاهش یافت.
- git status و grep سرعت طبیعی دارند.
- هیچ فایل دانشی از دست نرفت.
