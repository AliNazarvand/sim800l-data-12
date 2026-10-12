#!/usr/bin/env python3
"""Extract text from PDF(s) with basic column detection."""
import argparse
import sys
from pathlib import Path

try:
    import fitz
except ImportError:
    print("[FATAL] PyMuPDF not installed. pip install pymupdf", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
EXTRACTED = ROOT / "sources" / "extracted"


def detect_scanned(pdf_path: Path) -> bool:
    doc = fitz.open(pdf_path)
    total = 0
    pages = len(doc)
    for page in doc:
        total += len(page.get_text())
    doc.close()
    return pages > 0 and (total / pages) < 100


def extract_text(pdf_path: Path, out_dir: Path) -> None:
    doc = fitz.open(pdf_path)
    out_file = out_dir / f"{pdf_path.stem}.txt"
    with out_file.open("w", encoding="utf-8") as fh:
        for page in doc:
            blocks = page.get_text("blocks")
            if blocks:
                blocks_sorted = sorted(blocks, key=lambda b: (round(b[1]), b[0]))
                for b in blocks_sorted:
                    fh.write(b[4])
                    fh.write("\n")
            else:
                fh.write(page.get_text())
    doc.close()
    print(f"[OK] {out_file}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", nargs="+")
    parser.add_argument("--outdir", default=str(EXTRACTED))
    args = parser.parse_args()
    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for pdf in args.pdf:
        p = Path(pdf)
        if not p.exists():
            print(f"[WARN] Not found: {p}", file=sys.stderr)
            continue
        if detect_scanned(p):
            print(f"[INFO] {p.name} appears scanned; run ocr_pdf.py", file=sys.stderr)
        try:
            extract_text(p, out_dir)
        except Exception as exc:
            print(f"[ERROR] {p}: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())