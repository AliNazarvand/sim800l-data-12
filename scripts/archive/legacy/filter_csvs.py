#!/usr/bin/env python3
"""
filter_csvs.py — حذف جدول‌های CSV بی‌ارزش (idempotent).
اگر فایل‌های ALL.tsv موجود باشند، این اسکریپت هیچ‌کاری نمی‌کند
چون همه CSVها باید حذف شده باشند.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TABLES = ROOT / "sources" / "extracted" / "tables"

ALL_FILES = ["at_v1_01_ALL.tsv", "v2_02_ALL.tsv", "v1_00_ALL.tsv"]

def main():
    if not TABLES.exists():
        print("tables dir not found")
        return 0

    all_present = all((TABLES / f).exists() for f in ALL_FILES)
    remaining_csv = list(TABLES.glob("*.csv"))
    if all_present and not remaining_csv:
        print("already done — 3 ALL.tsv exist, no CSV remains")
        return 0

    # if not all present, delete all CSVs (they will be merged by merge_csvs.py)
    deleted = 0
    for p in remaining_csv:
        try:
            p.unlink()
            deleted += 1
        except Exception as e:
            print(f"  err deleting {p.name}: {e}", file=sys.stderr)
    print(f"deleted {deleted} CSV files")
    return 0

if __name__ == "__main__":
    sys.exit(main())