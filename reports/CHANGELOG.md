# CHANGELOG

## [0.2.0] — 14050718-235606
### Added
- scripts/extract_at_commands.py — استخراج خودکار AT Command از متن manual
- data/dat_01_at_command.yaml — پر شد با رکوردهای واقعی
- sources/extracted/_at_commands_index.json — ایندکس commandها

### Changed
- reports/COVERAGE_MATRIX.md — dat_01 از blocked به partial
- reports/TODO.md — به‌روزرسانی دقیق
- reports/SESSION_LOG.md — ثبت نشست ۱
- reports/DECISIONS_LOG.md — تصمیم‌های D-101..D-106
- reports/ROLE_MAP.md — هم‌راستا با وضعیت جدید
- scripts/validate.py — نسخه سبک‌شده و دقیق‌تر
- scripts/cross_ref.py — نسخه سبک‌شده

### Restored (from git history, if available)
- scripts/validate_v2.py
- scripts/clean_and_reextract.py
- scripts/populate_datasets.py

### Notes
- طبق R22 (WIP=1) و R23 (Vertical Slice)، فقط dat_01 در این نشست کار شد.
- برنچ: feature/complete-datasets