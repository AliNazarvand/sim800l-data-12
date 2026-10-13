import sys, subprocess, shutil
from pathlib import Path

def extract_with_pdfplumber(pdf, out_txt):
    try:
        import pdfplumber
    except ImportError:
        return False
    try:
        with pdfplumber.open(pdf) as doc:
            with open(out_txt, "w", encoding="utf-8") as f:
                for i, page in enumerate(doc.pages, 1):
                    f.write(f"\n===== PAGE {i} =====\n")
                    f.write(page.extract_text() or "")
                    f.write("\n")
        return True
    except Exception:
        return False

def extract_with_pdftotext(pdf, out_txt):
    exe = shutil.which("pdftotext")
    if not exe:
        return False
    try:
        subprocess.run([exe, "-layout", str(pdf), str(out_txt)], check=True)
        return True
    except Exception:
        return False

def main():
    root = Path(sys.argv[1])
    src  = root / "sources" / "originals"
    dst  = root / "sources" / "extracted"
    dst.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        print("no sources/originals dir"); return
    # FIX: deduplicate case-insensitive on Windows
    seen, pdfs = set(), []
    for p in list(src.glob("*.pdf")) + list(src.glob("*.PDF")):
        key = p.name.lower()
        if key in seen: continue
        seen.add(key); pdfs.append(p)
    pdfs.sort(key=lambda p: p.name.lower())
    if not pdfs:
        print("no PDFs found"); return
    for pdf in pdfs:
        out_txt = dst / (pdf.stem + ".txt")
        ok = extract_with_pdfplumber(pdf, out_txt) or extract_with_pdftotext(pdf, out_txt)
        if ok:
            print(f"OK  {pdf.name}  -> {out_txt.name}  ({out_txt.stat().st_size} bytes)")
        else:
            print(f"FAIL {pdf.name}: no extractor available")

if __name__ == "__main__":
    main()