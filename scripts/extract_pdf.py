#!/usr/bin/env python3
"""Simple text extraction from PDF (no OCR). Outputs text with <<<PAGE n>>> markers.
Falls back to reading existing .txt if PDF library not available."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC  = ROOT / "sources" / "originals"
OUT  = ROOT / "sources" / "extracted"
OUT.mkdir(parents=True, exist_ok=True)

def extract_with_pypdf(pdf_path):
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            return None
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as e:
        print(f"  [pypdf] failed to open: {e}", file=sys.stderr)
        return None
    parts = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            txt = page.extract_text() or ""
        except Exception as e:
            txt = f"[ERROR extracting page {i}: {e}]"
        parts.append(f"<<<PAGE {i}>>>\n{txt}\n")
    return "\n".join(parts)

def extract_with_pdfplumber(pdf_path):
    try:
        import pdfplumber
    except ImportError:
        return None
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            parts = []
            for i, page in enumerate(pdf.pages, start=1):
                try:
                    txt = page.extract_text() or ""
                except Exception as e:
                    txt = f"[ERROR extracting page {i}: {e}]"
                parts.append(f"<<<PAGE {i}>>>\n{txt}\n")
            return "\n".join(parts)
    except Exception as e:
        print(f"  [pdfplumber] failed: {e}", file=sys.stderr)
        return None

def main():
    targets = [
        ("v2_02_paged.txt", "SIM800H&SIM800L_Hardware_Design_V2.02.PDF"),
        ("v1_00_paged.txt", "SIM800L_Hardware_Design_V1.00.pdf"),
    ]
    for out_name, pdf_name in targets:
        pdf_path = SRC / pdf_name
        out_path = OUT / out_name
        print(f"Extracting {pdf_name} -> {out_name}")
        if not pdf_path.exists():
            print(f"  PDF not found: {pdf_path}", file=sys.stderr)
            continue
        text = extract_with_pdfplumber(pdf_path)
        if text is None:
            text = extract_with_pypdf(pdf_path)
        if text is None:
            print(f"  No PDF library available. Install: pip install pypdf", file=sys.stderr)
            continue
        out_path.write_text(text, encoding="utf-8")
        pages = text.count("<<<PAGE ")
        print(f"  OK: {pages} pages, {len(text)} chars")

if __name__ == "__main__":
    main()