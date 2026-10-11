#!/usr/bin/env python3
"""Retry: broader regex for URC and Error, filter using known-name list."""
import sys, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_EX = ROOT / "sources" / "extracted"
REPORTS = ROOT / "reports"

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

# لیست URC های شناخته‌شده برای SIM800L (بر اساس دانش عمومی از AT Manual)
KNOWN_URCS = [
    "RDY", "RING", "NO CARRIER",
    "+CMTI", "+CMT", "+CDS", "+CBM",
    "+CUSD", "+CREG", "+CGREG",
    "+CLIP", "+CRING", "+CPIN",
    "+PDP: DEACT", "+PDP DEACT",
    "+CIPRXGET", "+CIPCLOSE", "+CIPSTATUS",
    "+HTTPACTION", "+HTTPREAD",
    "+FTPPUT", "+FTPGET",
    "+SSLRECV",
    "+POWER DOWN",
    "+SIM DETECT",
    "OVER-VOLTAGE WARNNING",
    "UNDER-VOLTAGE WARNNING",
]

def find_urc_context(urc_name, pages):
    """Return (page, line) of the first strong hit."""
    pat = re.compile(re.escape(urc_name))
    for page_no, body in pages:
        for line in body.splitlines():
            s = line.strip()
            if len(s) < 4 or len(s) > 260:
                continue
            # حذف فهرست مطالب
            if re.match(r"^[+]?[A-Z0-9]+\s*\.{3,}", s):
                continue
            if pat.search(s):
                # باید در بافت URC باشد: شامل ':' یا '<' یا 'OK' یا 'command'
                if any(k in s for k in [":", "<", ">", "URC", "Unsolicited", "Result", "indication"]):
                    return (page_no, s)
    return None

urc_entries = {}
for u in KNOWN_URCS:
    hit = find_urc_context(u, pages)
    if hit:
        page_no, line = hit
        urc_entries[u] = {
            "urc_string": u,
            "page": page_no,
            "line": line[:260],
            "description": line[:160],
        }

# ---------- Error Code ----------
# صفحات حاوی 'Error' در سرصفحه + دنبال خطوطی با کد عددی
ERR_HEADER = re.compile(
    r"^\s*[0-9]+(?:\.[0-9]+){1,4}\s+.*(?:Error Code|Error Codes|CME|CMS)\s*$",
    re.IGNORECASE
)
err_zones = {}
for page_no, body in pages:
    for line in body.splitlines():
        s = line.strip()
        if ERR_HEADER.match(s):
            t = "CME" if "CME" in s.upper() else ("CMS" if "CMS" in s.upper() else "UNKNOWN")
            for d in range(0, 10):
                err_zones[page_no + d] = t

ERR_ROW = re.compile(r"^\s*([0-9]{1,4})\s+([A-Z][A-Za-z0-9 \(\)\-/,\.]{3,140})\s*$")

err_entries = {}
for page_no, body in pages:
    if page_no not in err_zones:
        continue
    etype = err_zones[page_no]
    for line in body.splitlines():
        s = line.strip()
        if len(s) < 5 or len(s) > 200:
            continue
        m = ERR_ROW.match(s)
        if m:
            code = int(m.group(1))
            desc = m.group(2).strip()
            key = f"{etype}_{code}"
            if key not in err_entries:
                err_entries[key] = {
                    "error_type": etype,
                    "code": code,
                    "meaning": desc[:160],
                    "page": page_no,
                    "line": s[:240],
                }

report = {
    "urc_entries": urc_entries,
    "err_entries": err_entries,
    "total_urc": len(urc_entries),
    "total_err": len(err_entries),
}
(REPORTS / "_step_B2B3_parsed_retry.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"URC entries detected: {len(urc_entries)}")
for k, v in urc_entries.items():
    print(f"  {k}  p{v['page']}  {v['description'][:80]}")
print(f"Error entries detected: {len(err_entries)}")
for k, v in list(err_entries.items())[:15]:
    print(f"  {k}  p{v['page']}  {v['meaning'][:80]}")