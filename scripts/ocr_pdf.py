#!/usr/bin/env python3
"""OCR scanned PDF(s) with Tesseract."""
import argparse
import subprocess
import sys
from pathlib import Path

try:
    import fitz
except ImportError:
    fitz = None

ROOT = Path(__file__).resolve().parent.parent
EXTRACTED = ROOT / "sources" / "extracted"


def is_scanned(pdf_path: Path) -> bool:
    if fitz is None:
        return True
    doc = fitz.open(pdf_path)
    total = 0
    pages = len(doc)
    for page in doc:
        total += len(page.get_text())
    doc.close()
    return pages > 0 and (total / pages) < 100


def ocr(pdf_path: Path, out_dir: Path, lang: str = "eng"):
    subprocess.run(["tesseract", str(pdf_path), str(out_dir / pdf_path.stem), "-l", lang], check=True)
    print(f"[OK] OCR done: {pdf_path.stem}.txt")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", nargs="+")
    parser.add_argument("--outdir", default=str(EXTRACTED))
    parser.add_argument("--lang", default="eng")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for pdf in args.pdf:
        p = Path(pdf)
        if not p.exists():
            print(f"[WARN] Not found: {p}", file=sys.stderr)
            continue
        if not args.force and not is_scanned(p):
            print(f"[SKIP] {p.name} has text; use --force", file=sys.stderr)
            continue
        try:
            ocr(p, out_dir, args.lang)
        except Exception as exc:
            print(f"[ERROR] {p}: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())