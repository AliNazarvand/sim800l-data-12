#!/usr/bin/env python3
"""
ocr_pdf.py - OCR برای PDFهای اسکن‌شده (fallback)
پیش‌نیاز: tesseract + pdf2image  یا  tesseract + pytesseract
"""
from __future__ import annotations
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC = PROJECT_ROOT / "sources" / "originals"
DST = PROJECT_ROOT / "sources" / "extracted" / "ocr"

def which(name: str) -> str | None:
    return shutil.which(name)

def ocr_pdf(pdf: Path, out: Path) -> bool:
    # ابتدا تلاش pdftoppm برای تبدیل به تصویر
    pdftoppm = which("pdftoppm")
    tesseract = which("tesseract")
    if not (pdftoppm and tesseract):
        print("[SKIP] tesseract یا pdftoppm نصب نیست.")
        return False
    tmp = DST / (pdf.stem + "_pages")
    tmp.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run([pdftoppm, "-r", "300", "-png",
                        str(pdf), str(tmp / "page")],
                       check=True, capture_output=True)
        texts = []
        for png in sorted(tmp.glob("page-*.png")):
            r = subprocess.run(
                [tesseract, str(png), "stdout", "-l", "eng"],
                check=True, capture_output=True, text=True
            )
            texts.append(r.stdout)
        out.write_text("\n".join(texts), encoding="utf-8")
        return True
    except Exception as e:
        print(f"[FAIL] OCR {pdf.name}: {e}")
        return False

def main():
    if not SRC.exists():
        print(f"[ERROR] {SRC} یافت نشد.")
        sys.exit(1)
    DST.mkdir(parents=True, exist_ok=True)
    pdfs = list(SRC.glob("*.pdf")) + list(SRC.glob("*.PDF"))
    ok = 0
    for pdf in pdfs:
        out = DST / (pdf.stem + ".ocr.txt")
        if out.exists() and out.stat().st_size > 100:
            print(f"[SKIP] {out.name}")
            ok += 1
            continue
        if ocr_pdf(pdf, out):
            ok += 1
    print(f"OCR: {ok}/{len(pdfs)}")

if __name__ == "__main__":
    main()
