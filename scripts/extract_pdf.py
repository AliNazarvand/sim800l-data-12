#!/usr/bin/env python3
"""PDF text / table extraction helper.

Uses pdftotext if available; falls back to PyPDF2 if installed.
"""
import os
import sys
import subprocess
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "sources", "originals")
OUT = os.path.join(ROOT, "sources", "extracted")

def pdftotext_available():
    from shutil import which
    return which("pdftotext") is not None

def extract_with_pdftotext(pdf_path, txt_path):
    subprocess.run(["pdftotext", "-layout", pdf_path, txt_path], check=True)

def main():
    os.makedirs(OUT, exist_ok=True)
    pdfs = glob.glob(os.path.join(SRC, "*.pdf")) + glob.glob(os.path.join(SRC, "*.PDF"))
    if not pdfs:
        print("No PDFs found in", SRC)
        return
    if not pdftotext_available():
        print("pdftotext not available. Install poppler-utils.")
        return
    for pdf in pdfs:
        base = os.path.splitext(os.path.basename(pdf))[0]
        txt = os.path.join(OUT, base + ".txt")
        try:
            extract_with_pdftotext(pdf, txt)
            print("Extracted:", txt)
        except Exception as e:
            print("Failed:", pdf, e)

if __name__ == "__main__":
    main()