"""Extract text from a PDF, page by page, into a page-marked file.

Uses pypdf (pure Python). Also writes one file per page and a manifest.
Flags pages that come back empty so the caller can detect scanned PDFs.

Usage:
    python _extract.py <input.pdf> <output.txt> <pages_dir> <label>

Page markers: "===== PAGE N =====" (used for _meta.source_page references).
UTF-8 output, no BOM.
"""
import json
import sys
from pathlib import Path

from pypdf import PdfReader

def main() -> int:
    if len(sys.argv) != 5:
        print("usage: _extract.py <pdf> <out.txt> <pages_dir> <label>", file=sys.stderr)
        return 2
    pdf_path  = Path(sys.argv[1])
    out_path  = Path(sys.argv[2])
    pages_dir = Path(sys.argv[3])
    label     = sys.argv[4]

    if not pdf_path.is_file():
        print(f"ERROR: PDF not found: {pdf_path}", file=sys.stderr)
        return 1

    pages_dir.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(str(pdf_path))
    page_count = len(reader.pages)
    combined = []
    total_chars = 0
    empty_pages = []

    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            text = f"<<extraction error on page {i}: {exc}>>"
        if not text.strip():
            empty_pages.append(i)
        total_chars += len(text)
        combined.append(f"===== PAGE {i} =====")
        combined.append(text)
        combined.append("")
        (pages_dir / f"p{i:04d}.txt").write_text(text, encoding="utf-8")

    out_path.write_text("\n".join(combined), encoding="utf-8")

    manifest = {
        "label": label,
        "source_pdf": str(pdf_path),
        "output_txt": str(out_path),
        "pages_dir": str(pages_dir),
        "page_count": page_count,
        "total_characters": total_chars,
        "empty_pages": empty_pages,
        "empty_page_count": len(empty_pages),
        "extractor": "pypdf",
    }
    out_path.with_suffix(out_path.suffix + ".manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"{label}: {page_count} pages, {total_chars} chars, "
          f"{len(empty_pages)} empty -> {out_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())