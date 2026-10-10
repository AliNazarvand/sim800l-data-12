#!/usr/bin/env python3
"""OCR helper using tesseract if available."""
import os
import sys
import subprocess
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "sources", "originals")
OUT = os.path.join(ROOT, "sources", "extracted", "ocr")

def main():
    os.makedirs(OUT, exist_ok=True)
    from shutil import which
    if which("tesseract") is None:
        print("tesseract not installed.")
        return
    pdfs = glob.glob(os.path.join(SRC, "*.pdf")) + glob.glob(os.path.join(SRC, "*.PDF"))
    for pdf in pdfs:
        base = os.path.splitext(os.path.basename(pdf))[0]
        txt = os.path.join(OUT, base + ".ocr.txt")
        try:
            subprocess.run(["tesseract", pdf, txt[:-4], "-l", "eng"], check=True)
            print("OCR done:", txt)
        except Exception as e:
            print("OCR failed:", pdf, e)

if __name__ == "__main__":
    main()