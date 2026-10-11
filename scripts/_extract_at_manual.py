#!/usr/bin/env python3
"""Extract SIM800 Series AT Command Manual V1.01 to paged text."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "originals"
OUT = ROOT / "sources" / "extracted"
OUT.mkdir(parents=True, exist_ok=True)

PDF_NAME = "SIM800 Series_AT Command Manual_V1.01.pdf"
OUT_NAME = "at_manual_v1_01_paged.txt"

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
        print(f"  [pypdf] open failed: {e}", file=sys.stderr)
        return None
    parts = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            txt = page.extract_text() or ""
        except Exception as e:
            txt = f"[ERROR page {i}: {e}]"
        parts.append(f"<<<PAGE {i}>>>\n{txt}\n")
    return "\n".join(parts)

def main():
    pdf_path = SRC / PDF_NAME
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}", file=sys.stderr); sys.exit(1)
    text = extract_with_pypdf(pdf_path)
    if text is None:
        print("pypdf not installed. Try: pip install pypdf", file=sys.stderr); sys.exit(2)
    out_path = OUT / OUT_NAME
    out_path.write_text(text, encoding="utf-8")
    pages = text.count("<<<PAGE ")
    print(f"OK: {pages} pages, {len(text)} chars -> {out_path.name}")

if __name__ == "__main__":
    main()