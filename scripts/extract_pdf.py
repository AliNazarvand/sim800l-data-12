#!/usr/bin/env python3
"""Extract text and tables from PDF files (with basic column detection)."""
import argparse
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("[FATAL] PyMuPDF not installed. Run: pip install pymupdf", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
EXTRACTED_DIR = ROOT / "sources" / "extracted"


def extract_text(pdf_path: Path, out_dir: Path) -> None:
    doc = fitz.open(pdf_path)
    out_file = out_dir / f"{pdf_path.stem}.txt"
    with out_file.open("w", encoding="utf-8") as fh:
        for page in doc:
            # Try to detect multi-column layout using blocks
            blocks = page.get_text("blocks")
            if blocks:
                # Sort blocks top-to-bottom, then left-to-right
                blocks_sorted = sorted(blocks, key=lambda b: (round(b[1]), b[0]))
                for b in blocks_sorted:
                    fh.write(b[4])
                    fh.write("\n")
            else:
                fh.write(page.get_text())
    doc.close()
    print(f"[OK] Text extracted: {out_file}")


def detect_scanned(pdf_path: Path) -> bool:
    """Return True if PDF appears scanned (very little extractable text)."""
    doc = fitz.open(pdf_path)
    total = 0
    pages = len(doc)
    for page in doc:
        total += len(page.get_text())
    doc.close()
    return pages > 0 and (total / pages) < 100


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract text from PDF(s).")
    parser.add_argument("pdf", nargs="+", help="Path(s) to PDF file(s).")
    parser.add_argument("--outdir", default=str(EXTRACTED_DIR), help="Output directory.")
    args = parser.parse_args()

    out_dir = Path(args.outdir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for pdf in args.pdf:
        p = Path(pdf)
        if not p.exists():
            print(f"[WARN] Not found: {p}", file=sys.stderr)
            continue
        try:
            if detect_scanned(p):
                print(f"[INFO] {p.name} appears scanned; run ocr_pdf.py", file=sys.stderr)
            extract_text(p, out_dir)
        except Exception as exc:
            print(f"[ERROR] {p}: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())