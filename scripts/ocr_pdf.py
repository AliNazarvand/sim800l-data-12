#!/usr/bin/env python3
"""OCR scanned PDF files using Tesseract (with scanned-PDF detection)."""
import argparse
import subprocess
import sys
from pathlib import Path

try:
    import fitz
except ImportError:
    fitz = None

ROOT = Path(__file__).resolve().parent.parent
EXTRACTED_DIR = ROOT / "sources" / "extracted"


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


def ocr_pdf(pdf_path: Path, out_dir: Path, lang: str = "eng") -> None:
    out_base = out_dir / pdf_path.stem
    subprocess.run(
        ["tesseract", str(pdf_path), str(out_base), "-l", lang],
        check=True,
    )
    print(f"[OK] OCR complete: {out_base}.txt")


def main() -> int:
    parser = argparse.ArgumentParser(description="OCR PDF file(s).")
    parser.add_argument("pdf", nargs="+")
    parser.add_argument("--outdir", default=str(EXTRACTED_DIR))
    parser.add_argument("--lang", default="eng")
    parser.add_argument("--force", action="store_true", help="OCR even if PDF has text")
    args = parser.parse_args()

    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for pdf in args.pdf:
        p = Path(pdf)
        if not p.exists():
            print(f"[WARN] Not found: {p}", file=sys.stderr)
            continue
        if not args.force and not is_scanned(p):
            print(f"[SKIP] {p.name} has extractable text; use --force to OCR anyway", file=sys.stderr)
            continue
        try:
            ocr_pdf(p, out_dir, args.lang)
        except Exception as exc:
            print(f"[ERROR] {p}: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())