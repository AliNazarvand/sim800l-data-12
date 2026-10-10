#!/usr/bin/env python3
"""
preflight.py - بررسی پیش از اجرا: وجود منابع، ساختار پوشه‌ها، اسکیم‌ها
"""
from __future__ import annotations
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_DIRS = ["data", "schemas", "sources", "sources/originals",
                 "sources/extracted", "reports", "scripts", "docs"]
REQUIRED_ORIGINALS = [
    "SIM800 Series_AT Command Manual_V1.01.pdf",
    "SIM800L_Hardware_Design_V1.00.pdf",
    "SIM800H&SIM800L_Hardware_Design_V2.02.PDF",
]

def main():
    print("=== PREFLIGHT ===")
    ok = True
    for d in REQUIRED_DIRS:
        p = PROJECT_ROOT / d
        status = "OK" if p.exists() else "MISSING"
        if status == "MISSING":
            ok = False
        print(f"  [{status}] {d}")
    print("-- منابع اصلی --")
    for f in REQUIRED_ORIGINALS:
        p = PROJECT_ROOT / "sources" / "originals" / f
        status = "OK" if p.exists() else "MISSING"
        if status == "MISSING":
            ok = False
        print(f"  [{status}] {f}")
    print(f"\nنتیجه: {'آماده' if ok else 'ناقص'}")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
