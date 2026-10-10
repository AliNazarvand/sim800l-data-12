#!/usr/bin/env python3
"""
extract_tables.py - استخراج جدول‌های معنادار PDF به CSV (فیلتر شده)

فیلترها:
  - حداقل 2 ردیف داده
  - حداقل 2 ستون داده
  - حداقل 2 سلول غیرخالی
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "originals"
DST = ROOT / "sources" / "extracted" / "tables"

MIN_ROWS = 2
MIN_COLS = 2
MIN_NON_EMPTY = 4

def is_meaningful(tbl) -> bool:
    if not tbl or len(tbl) < MIN_ROWS:
        return False
    cols = max((len(r) for r in tbl), default=0)
    if cols < MIN_COLS:
        return False
    non_empty = sum(1 for r in tbl for c in r if c and str(c).strip())
    return non_empty >= MIN_NON_EMPTY

def extract(pdf, outdir):
    try:
        import pdfplumber
    except ImportError:
        return -1
    n = 0
    try:
        with pdfplumber.open(str(pdf)) as p:
            for i, page in enumerate(p.pages):
                for j, tbl in enumerate(page.extract_tables() or []):
                    if not is_meaningful(tbl):
                        continue
                    out = outdir / f"{pdf.stem}_p{i+1:03d}_t{j+1}.csv"
                    with out.open("w", encoding="utf-8", newline="") as f:
                        w = csv.writer(f)
                        for row in tbl:
                            w.writerow([c if c else "" for c in row])
                    n += 1
    except Exception as e:
        print(f"  [ERR] {e}")
    return n

def main():
    if not SRC.exists():
        print(f"[ERROR] {SRC}"); sys.exit(1)
    DST.mkdir(parents=True, exist_ok=True)
    pdfs = list(SRC.glob("*.pdf")) + list(SRC.glob("*.PDF"))
    total = 0
    for pdf in pdfs:
        print(f"[TABLE] {pdf.name}")
        n = extract(pdf, DST)
        if n < 0:
            print("  [SKIP] pdfplumber نصب نیست (pip install pdfplumber)")
        else:
            print(f"  {n} جدول معنادار")
            total += n
    print(f"\nمجموع جدول‌های استخراج‌شده: {total}")
    print(f"معیارها: ردیف >= {MIN_ROWS}, ستون >= {MIN_COLS}, سلول غیرخالی >= {MIN_NON_EMPTY}")

if __name__ == "__main__":
    main()
