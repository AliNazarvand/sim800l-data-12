#!/usr/bin/env python3
"""Dump raw text of pages containing URC or CME/CMS Error markers."""
import sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_EX = ROOT / "sources" / "extracted"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

def load_paged(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    pages = []
    parts = re.split(r"<<<PAGE\s+(\d+)>>>", text)
    for i in range(1, len(parts) - 1, 2):
        try:
            num = int(parts[i])
        except Exception:
            continue
        pages.append((num, parts[i + 1]))
    return pages

pages = load_paged(SRC_EX / "at_manual_v1_01_paged.txt")

# کلیدواژه‌ها برای انتخاب صفحات
URC_KEYWORDS = ["+CMTI", "+CMT", "+CDS", "+CBM", "+CUSD", "+CREG", "+CGREG",
                "+CLIP", "+CRING", "+CPIN", "+PDP", "+CIP", "+HTTPACTION",
                "+FTPPUT", "+SSLRECV", "RING", "NO CARRIER", "RDY"]
ERR_KEYWORDS = ["CME Error", "CMS Error", "CME ERROR", "CMS ERROR",
                "Error Code", "ERROR CODE"]

urc_pages = set()
err_pages = set()
for page_no, body in pages:
    for kw in URC_KEYWORDS:
        if kw in body:
            urc_pages.add(page_no)
            break
    for kw in ERR_KEYWORDS:
        if kw in body:
            err_pages.add(page_no)
            break

# صفحه‌هایی که احتمالاً appendix جدول error هستند
candidate_err_pages = sorted(err_pages | set(range(130, 200)))

out_lines = []
out_lines.append("=" * 70)
out_lines.append(f"INSPECT DUMP — AT Manual V1.01")
out_lines.append(f"URC candidate pages: {sorted(urc_pages)[:30]}")
out_lines.append(f"Error candidate pages: {sorted(candidate_err_pages)[:30]}")
out_lines.append("=" * 70)

def dump_page(page_no, body, max_lines=50):
    out_lines.append(f"\n--- PAGE {page_no} (first {max_lines} lines) ---")
    lines = body.splitlines()
    for ln in lines[:max_lines]:
        out_lines.append(ln)

# نمونه URC pages
urc_sample = sorted(urc_pages)[:6]
for p in urc_sample:
    for page_no, body in pages:
        if page_no == p:
            dump_page(page_no, body, 40)
            break

# نمونه Error pages (appendix-like)
err_sample = sorted(err_pages)[:3] + [p for p in candidate_err_pages if p in err_pages][:3]
err_sample = sorted(set(err_sample))[:6]
for p in err_sample:
    for page_no, body in pages:
        if page_no == p:
            dump_page(page_no, body, 60)
            break

(REPORTS / "_step_B2B3_inspect.txt").write_text("\n".join(out_lines), encoding="utf-8")
print(f"URC candidate pages: {len(urc_pages)}")
print(f"Error candidate pages: {len(err_pages)}")
print(f"Diagnostic written to reports/_step_B2B3_inspect.txt")