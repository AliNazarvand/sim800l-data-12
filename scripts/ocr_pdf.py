#!/usr/bin/env python3
"""
ocr_pdf.py — OCR برای PDFهای اسکن‌شده با tesseract (eng).
خروجی: sources/extracted/<stem>.ocr.txt
"""
import sys
from pathlib import Path

try:
    import pytesseract
    from pdf2image import convert_from_path
except Exception:
    pytesseract = None
    convert_from_path = None


def ocr_one(pdf: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / (pdf.stem + ".ocr.txt")
    if pytesseract is None or convert_from_path is None:
        print(f"[WARN] pytesseract/pdf2image missing; skipping {pdf.name}")
        return
    pages = convert_from_path(str(pdf), dpi=300)
    parts = []
    for i, img in enumerate(pages, 1):
        parts.append(f"===== page {i} =====\n{pytesseract.image_to_string(img, lang='eng')}\n")
    out_file.write_text("\n".join(parts), encoding="utf-8")
    print(f"[OK]   {pdf.name} -> {out_file.name}")


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    src = root / "sources" / "originals"
    dst = root / "sources" / "extracted"
    if not src.exists():
        print(f"[FAIL] sources/originals not found: {src}")
        return 1
    for p in list(src.glob("*.pdf")) + list(src.glob("*.PDF")):
        ocr_one(p, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())