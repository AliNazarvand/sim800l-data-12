#!/usr/bin/env python3
"""
extract_pdf.py — استخراج متن از PDFهای سخت‌افزاری SIM800L.

استراتژی:
1. تلاش با pdftotext (poppler) — سریع‌ترین.
2. اگر خروجی < 100 کاراکتر در کل: PDF اسکن‌شده است → ocr_pdf.py.
3. اگر pdftotext نبود: pdfplumber.
خروجی: sources/extracted/<stem>.txt
"""
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import pdfplumber
except Exception:
    pdfplumber = None


def extract_with_pdftotext(pdf: Path, out: Path) -> bool:
    exe = shutil.which("pdftotext")
    if exe is None:
        return False
    try:
        subprocess.run([exe, "-layout", str(pdf), str(out)],
                       check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"[WARN] pdftotext failed on {pdf.name}: {e}")
        return False


def extract_with_pdfplumber(pdf: Path, out: Path) -> bool:
    if pdfplumber is None:
        return False
    try:
        with pdfplumber.open(str(pdf)) as pl:
            parts = []
            for i, page in enumerate(pl.pages, 1):
                parts.append(f"===== page {i} =====\n{page.extract_text() or ''}\n")
        out.write_text("\n".join(parts), encoding="utf-8")
        return True
    except Exception as e:
        print(f"[WARN] pdfplumber failed on {pdf.name}: {e}")
        return False


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    src = root / "sources" / "originals"
    dst = root / "sources" / "extracted"
    if not src.exists():
        print(f"[FAIL] sources/originals not found: {src}")
        return 1
    dst.mkdir(parents=True, exist_ok=True)
    pdfs = list(src.glob("*.pdf")) + list(src.glob("*.PDF"))
    if not pdfs:
        print(f"[WARN] no PDFs in {src}")
        return 0
    for pdf in pdfs:
        out = dst / (pdf.stem + ".txt")
        ok = extract_with_pdftotext(pdf, out) or extract_with_pdfplumber(pdf, out)
        if not ok:
            print(f"[WARN] extraction failed: {pdf.name} (needs OCR)")
            continue
        text = out.read_text(encoding="utf-8", errors="ignore")
        quality = "high" if len(text) > 2000 else ("medium" if len(text) > 100 else "low")
        print(f"[OK]   {pdf.name} -> {out.name}  quality={quality}")
        if quality == "low":
            print(f"[INFO] {pdf.name}: appears to be scanned; run ocr_pdf.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())