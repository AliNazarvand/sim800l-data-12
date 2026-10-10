#!/usr/bin/env python3
"""
extract_figures.py - استخراج شکل‌های معنادار PDF به PNG (فیلتر شده)

فیلترها:
  - حداقل ابعاد: 100x100 پیکسل
  - حداقل حجم: 5 KB
  - حذف تصاویر تکراری (SHA-256 hash)
  - حذف تصاویر کوچک‌تر (آیکون/خط تزئینی)
"""
from __future__ import annotations
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "originals"
DST = ROOT / "sources" / "extracted" / "figures"

MIN_WIDTH = 100
MIN_HEIGHT = 100
MIN_BYTES = 5 * 1024

def save_if_valid(doc, xref, out_path: Path, seen_hashes: set) -> bool:
    try:
        import fitz
    except ImportError:
        return False
    try:
        pix = fitz.Pixmap(doc, xref)
        # تبدیل به RGB اگر CMYK/alpha دارد
        if pix.n - pix.alpha >= 4:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        if pix.width < MIN_WIDTH or pix.height < MIN_HEIGHT:
            return False
        png_bytes = pix.tobytes("png")
        if len(png_bytes) < MIN_BYTES:
            return False
        h = hashlib.sha256(png_bytes).hexdigest()
        if h in seen_hashes:
            return False
        seen_hashes.add(h)
        out_path.write_bytes(png_bytes)
        return True
    except Exception:
        return False

def extract(pdf, outdir, seen_hashes):
    try:
        import fitz
    except ImportError:
        return -1
    n = 0
    try:
        doc = fitz.open(str(pdf))
        for pno in range(len(doc)):
            page = doc[pno]
            for ino, img in enumerate(page.get_images(full=True)):
                out = outdir / f"{pdf.stem}_p{pno+1:03d}_img{ino+1}.png"
                if save_if_valid(doc, img[0], out, seen_hashes):
                    n += 1
        doc.close()
    except Exception as e:
        print(f"  [ERR] {e}")
    return n

def main():
    if not SRC.exists():
        print(f"[ERROR] {SRC}"); sys.exit(1)
    DST.mkdir(parents=True, exist_ok=True)
    pdfs = list(SRC.glob("*.pdf")) + list(SRC.glob("*.PDF"))
    seen = set()
    total = 0
    for pdf in pdfs:
        print(f"[FIGURE] {pdf.name}")
        n = extract(pdf, DST, seen)
        if n < 0:
            print("  [SKIP] PyMuPDF نصب نیست (pip install pymupdf)")
        else:
            print(f"  {n} شکل معنادار")
            total += n
    print(f"\nمجموع شکل‌های استخراج‌شده: {total}")
    print(f"معیارها: ابعاد >= {MIN_WIDTH}x{MIN_HEIGHT}px, حجم >= {MIN_BYTES//1024}KB, hash-based dedup")

if __name__ == "__main__":
    main()
