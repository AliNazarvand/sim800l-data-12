#!/usr/bin/env python3
"""
extract_text_only.py — فقط متن PDFها را استخراج می‌کند.
- به پوشه tables/ دست نمی‌زند.
- Idempotent: اگر فایل خروجی جدیدتر از PDF باشد، دوباره استخراج نمی‌کند.
- خروجی: sources/extracted/{v1.00.txt, v2.02.txt, at_v1_01.txt}
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIGINALS = ROOT / "sources" / "originals"
EXTRACTED = ROOT / "sources" / "extracted"

TARGETS = [
    ("SIM800L_Hardware_Design_V1.00.pdf",        "v1.00.txt"),
    ("SIM800H&SIM800L_Hardware_Design_V2.02.PDF","v2.02.txt"),
    ("SIM800 Series_AT Command Manual_V1.01.pdf","at_v1_01.txt"),
]

def extract_one(pdf_path, out_path, force=False):
    if not pdf_path.exists():
        print(f"  skip (not found): {pdf_path.name}")
        return ("missing", 0)
    if out_path.exists() and not force:
        if out_path.stat().st_mtime >= pdf_path.stat().st_mtime:
            print(f"  skip (up-to-date): {out_path.name}")
            return ("skipped", out_path.stat().st_size)
    try:
        import pdfplumber
    except ImportError:
        print("  ERROR: pdfplumber نصب نیست.")
        return ("error", 0)
    parts = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        total = len(pdf.pages)
        for i, page in enumerate(pdf.pages, 1):
            txt = page.extract_text() or ""
            parts.append(f"\n=== PAGE {i} ===\n{txt}")
    content = "\n".join(parts)
    out_path.write_text(content, encoding="utf-8", errors="ignore")
    print(f"  ok: {pdf_path.name} -> {out_path.name} ({len(content)} chars, {total} pages)")
    return ("ok", len(content))

def main():
    force = "--force" in sys.argv
    EXTRACTED.mkdir(parents=True, exist_ok=True)
    results = {}
    for pdf_name, out_name in TARGETS:
        pdf = ORIGINALS / pdf_name
        out = EXTRACTED / out_name
        status, size = extract_one(pdf, out, force=force)
        results[out_name] = {"status": status, "size": size}
    import json
    (ROOT / "scripts" / "_step_b_result.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return 0

if __name__ == "__main__":
    sys.exit(main())