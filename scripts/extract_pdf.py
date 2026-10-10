#!/usr/bin/env python3
"""استخراج متن و جداول از PDFهای سخت‌افزاری."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIGINALS = ROOT / "sources" / "originals"
EXTRACTED = ROOT / "sources" / "extracted"

def try_import():
    try:
        import pdfplumber  # noqa
        return True
    except ImportError:
        print("pdfplumber نصب نیست. نصب خودکار...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pdfplumber"])
        return True

def extract_pdf(pdf_path, out_txt):
    import pdfplumber
    parts = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            txt = page.extract_text() or ""
            parts.append(f"\n=== PAGE {i} ===\n{txt}")
    content = "\n".join(parts)
    EXTRACTED.mkdir(parents=True, exist_ok=True)
    out_txt.write_text(content, encoding="utf-8", errors="ignore")
    return len(content)

def main():
    try_import()
    EXTRACTED.mkdir(parents=True, exist_ok=True)
    targets = [
        ("SIM800L_Hardware_Design_V1.00.pdf", "SIM800L_Hardware_Design_V1.00.txt"),
        ("SIM800H&SIM800L_Hardware_Design_V2.02.PDF", "SIM800H&SIM800L_Hardware_Design_V2.02.txt"),
        ("SIM800H&SIM800L_Hardware_Design_V2.02.pdf", "SIM800H&SIM800L_Hardware_Design_V2.02.txt"),
        ("SIM800 Series_AT Command Manual_V1.01.pdf", "SIM800 Series_AT Command Manual_V1.01.txt"),
    ]
    for pdf_name, out_name in targets:
        p = ORIGINALS / pdf_name
        if not p.exists():
            print(f"skip (not found): {p.name}")
            continue
        out = EXTRACTED / out_name
        try:
            n = extract_pdf(p, out)
            print(f"ok: {p.name} -> {out.name} ({n} chars)")
        except Exception as e:
            print(f"err: {p.name}: {e}")
    return 0

if __name__ == "__main__":
    sys.exit(main())