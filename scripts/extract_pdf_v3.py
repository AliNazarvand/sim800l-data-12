#!/usr/bin/env python3
"""استخراج متن + جداول + OCR از PDFها."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIGINALS = ROOT / "sources" / "originals"
EXTRACTED = ROOT / "sources" / "extracted"
TABLES = EXTRACTED / "tables"
OCR = EXTRACTED / "ocr"

def has_pdfplumber():
    try:
        import pdfplumber  # noqa
        return True
    except ImportError:
        return False

def has_pytesseract():
    try:
        import pytesseract  # noqa
        return True
    except ImportError:
        return False

def extract_text_and_tables(pdf_path, out_txt, tables_prefix):
    import pdfplumber
    parts = []
    table_count = 0
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            txt = page.extract_text() or ""
            parts.append(f"\n=== PAGE {i} ===\n{txt}")
            try:
                tables = page.extract_tables() or []
                for ti, table in enumerate(tables, 1):
                    table_count += 1
                    csv_name = f"{tables_prefix}_p{i}_t{ti}.csv"
                    with open(TABLES / csv_name, "w", encoding="utf-8") as f:
                        for row in table:
                            if row:
                                f.write("\t".join((cell or "").replace("\n"," ") for cell in row) + "\n")
            except Exception:
                pass
    content = "\n".join(parts)
    EXTRACTED.mkdir(parents=True, exist_ok=True)
    out_txt.write_text(content, encoding="utf-8", errors="ignore")
    return len(content), table_count

def try_ocr_pages(pdf_path, out_prefix, min_chars=100):
    """اگر متن هر صفحه < min_chars بود، آن را OCR می‌کند."""
    if not has_pytesseract():
        print(f"  skip OCR (pytesseract نصب نیست): {pdf_path.name}")
        return 0
    import pdfplumber
    import pytesseract
    from PIL import Image
    OCR.mkdir(parents=True, exist_ok=True)
    ocr_count = 0
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            txt = (page.extract_text() or "").strip()
            if len(txt) >= min_chars:
                continue
            try:
                img = page.to_image(resolution=200).original
                ocr_text = pytesseract.image_to_string(img, lang="eng")
                if ocr_text.strip():
                    out = OCR / f"{out_prefix}_p{i}.txt"
                    out.write_text(ocr_text, encoding="utf-8", errors="ignore")
                    ocr_count += 1
            except Exception:
                pass
    return ocr_count

def main():
    if not has_pdfplumber():
        print("pdfplumber نصب نیست")
        return 1
    EXTRACTED.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    targets = [
        ("SIM800L_Hardware_Design_V1.00.pdf", "v1.00.txt", "v1_00"),
        ("SIM800H&SIM800L_Hardware_Design_V2.02.PDF", "v2.02.txt", "v2_02"),
        ("SIM800 Series_AT Command Manual_V1.01.pdf", "at_v1_01.txt", "at_v1_01"),
    ]
    for pdf_name, out_name, prefix in targets:
        p = ORIGINALS / pdf_name
        if not p.exists():
            print(f"  skip: {pdf_name} یافت نشد")
            continue
        try:
            n, tc = extract_text_and_tables(p, EXTRACTED / out_name, prefix)
            print(f"  ok: {pdf_name} -> {out_name} ({n} chars, {tc} tables)")
            oc = try_ocr_pages(p, prefix)
            if oc: print(f"     OCR: {oc} صفحه")
        except Exception as e:
            print(f"  err: {pdf_name}: {e}")
    return 0

if __name__ == "__main__":
    sys.exit(main())