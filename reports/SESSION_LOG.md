# SESSION_LOG

## گام A3 (اصلاح‌شده) — تصحیح وضعیت dat_05 و dat_06

- تاریخ: 1405-07-19T16:28:39Z
- برنچ: feature/complete-datasets

### ۱) خلاصه A3
- اسکن ساختاریافته PDF انجام شد (12۹ جدول، 120 شکل، 19 بخش در V2.02).
- هیچ رکورد auto-detected اضافه نشد (طبق D-019).
- وضعیت اولیه A3 برای dat_05 و dat_06 اشتباهاً blocked ثبت شد.

### ۲) تصحیح این نشست
- تشخیص: dat_05 دارای 11 رکورد inferred و dat_06 دارای 10 رکورد inferred است. منبع (V2.02/V1.00) در دسترس است.
- COVERAGE_MATRIX: dat_05 و dat_06 از blocked به partial تغییر یافت.
- DECISIONS_LOG: D-021 اضافه شد (تصحیح وضعیت + قاعده D-022).
- TODO: بازبینی دستی جداول V2.02 صفحات 6، 15-25 ثبت شد.

### ۳) قاعده جدید (D-022)
- یک دیتاست blocked نباید هیچ رکوردی در فایل داده داشته باشد.
- اگر رکورد هست -> حداقل partial.
- اگر منبع در دسترس است -> حداکثر partial (نه blocked).

### ۴) وضعیت نهایی خوشه A3
- dat_04: partial
- dat_05: partial
- dat_06: partial

### ۵) کار گام بعد
- خوشه A4: dat_16 Board/EVB (احتمالاً deferred)
- یا بازگشت به dat_04/dat_05/dat_06/dat_15 برای استخراج دستی (نشست جداگانه)

### ۶) منابع موردنیاز
- SIM800 Series Sleep Mode Application Manual — dat_15
- بازبینی دستی PDF برای dat_04/dat_05/dat_06