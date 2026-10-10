#!/usr/bin/env python3
"""
extract_pdf_v2.py — استخراج متن از PDFهای SIM800 در sources/.

استراتژی:
1. اگر sources/extracted/<stem>.txt از قبل وجود دارد → skip
2. pdftotext (poppler) اگر در PATH باشد
3. pdfplumber به‌عنوان fallback
4. تشخیص کیفیت: high (>2000 کاراکتر)، medium (>100)، low (نیازمند OCR)

نسخه ۲ (رفع باگ Unicode روی Windows cp1252).
"""
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources"
DST = SRC / "extracted"
REPORTS = ROOT / "reports"

try:
    import pdfplumber
except Exception:
    pdfplumber = None


def safe_print(s: str):
    """چاپ امن روی هر ترمینال (رفع UnicodeEncodeError در Windows cp1252)."""
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("ascii", errors="replace").decode("ascii"))


def quality(text: str) -> str:
    n = len(text)
    if n > 2000: return "high"
    if n > 100:  return "medium"
    return "low"


def try_pdftotext(pdf: Path, out: Path) -> bool:
    exe = shutil.which("pdftotext")
    if not exe: return False
    try:
        subprocess.run([exe, "-layout", str(pdf), str(out)],
                       check=True, capture_output=True)
        return True
    except Exception as e:
        safe_print(f"[WARN] pdftotext failed: {e}")
        return False


def try_pdfplumber(pdf: Path, out: Path) -> bool:
    if pdfplumber is None:
        return False
    try:
        with pdfplumber.open(str(pdf)) as pl:
            parts = []
            for i, page in enumerate(pl.pages, 1):
                parts.append(f"===== page {i} =====\n{page.extract_text() or ''}\n")
        out.write_text("\n".join(parts), encoding="utf-8")
        return True
    except Exception as e:
        safe_print(f"[WARN] pdfplumber failed: {e}")
        return False


def main() -> int:
    DST.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)

    pdfs = [p for p in SRC.iterdir()
            if p.is_file() and p.suffix.lower() == ".pdf"]
    if not pdfs:
        safe_print(f"[FATAL] no PDF found in {SRC}")
        return 1

    lines = ["# PDF EXTRACTION REPORT", "",
             "| file | output | size | quality |",
             "|---|---|---|---|"]
    for pdf in sorted(pdfs):
        out = DST / (pdf.stem + ".txt")
        if out.exists() and out.stat().st_size > 100:
            txt = out.read_text(encoding="utf-8", errors="ignore")
            q = quality(txt)
            lines.append(f"| {pdf.name} | {out.name} | {len(txt)} | {q} (cached) |")
            safe_print(f"[SKIP] {pdf.name}: cached ({len(txt)} chars, q={q})")
            continue

        ok = try_pdftotext(pdf, out) or try_pdfplumber(pdf, out)
        if not ok:
            safe_print(f"[FAIL] {pdf.name}: extraction failed")
            lines.append(f"| {pdf.name} | - | 0 | FAILED |")
            continue
        txt = out.read_text(encoding="utf-8", errors="ignore")
        q = quality(txt)
        lines.append(f"| {pdf.name} | {out.name} | {len(txt)} | {q} |")
        safe_print(f"[OK]   {pdf.name} -> {out.name} ({len(txt)} chars, q={q})")

    rep = REPORTS / "PDF_EXTRACTION_REPORT.md"
    rep.write_text("\n".join(lines) + "\n", encoding="utf-8")
    safe_print(f"[OK]   {rep.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())