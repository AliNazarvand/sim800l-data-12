#!/usr/bin/env python3
"""پیدا کردن AT Manual در صورت نبود فایل txt استخراج‌شده."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTRACTED = ROOT / "sources" / "extracted"
ORIGINALS = ROOT / "sources" / "originals"

def main():
    targets = list(EXTRACTED.glob("*AT*Command*Manual*.txt"))
    if targets:
        print(f"AT Manual text موجود است: {targets[0].name}")
        return 0
    print("WARN: AT Manual text یافت نشد. extract_pdf.py اجرا شود.")
    return 0

if __name__ == "__main__":
    sys.exit(main())