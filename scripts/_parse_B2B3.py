#!/usr/bin/env python3
"""Parse structured URC entries and Error Code entries from AT Manual V1.01.
   Only uses lines inside detected sections."""
import sys, json, re
from pathlib import Path
from datetime import datetime, timezone
try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
SRC_EX = ROOT / "sources" / "extracted"
DATA = ROOT / "data"
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

def find_data_file(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    if c: return c[0]
    p = DATA / (dat_id + ".yaml")
    return p if p.exists() else None

pages = load_paged(SRC_EX / "at_manual_v1_01_paged.txt")

# ---- URC extraction ----
# URC markers: usually "+XXXX:" pattern at start of line in URC section
URC_LINE_RE = re.compile(r"^\s*(\+[A-Z0-9]{2,})\s*[:]?\s*(.{0,200})$")
# Section headers, to know when to stop URC capture
SECTION_RE = re.compile(r"^\s*[0-9]+(?:\.[0-9]+){1,4}\s+[A-Z][A-Za-z0-9 \-/&]{3,80}\s*$")

# Identify URC section page ranges: any page whose section header contains URC/Unsolicited
urc_pages = set()
for page_no, body in pages:
    for line in body.splitlines():
        s = line.strip()
        if re.match(r"^[0-9]+(?:\.[0-9]+){1,4}\s+(URC|Unsolicited)", s, re.IGNORECASE):
            urc_pages.add(page_no)

# Expand to a few pages around (URC section usually spans multiple pages)
urc_zone = set()
for p in urc_pages:
    for d in range(-1, 6):
        urc_zone.add(p + d)

urc_entries = {}
for page_no, body in pages:
    if page_no not in urc_zone:
        continue
    for line in body.splitlines():
        s = line.strip()
        if len(s) < 4 or len(s) > 240:
            continue
        # Skip TOC entries: "AT+XXX ...."
        if re.match(r"^[+]?[A-Z0-9]+\s*\.{3,}", s):
            continue
        m = URC_LINE_RE.match(s)
        if m:
            urc_str = m.group(1).strip()
            desc = m.group(2).strip()
            if urc_str not in urc_entries:
                urc_entries[urc_str] = {
                    "urc_string": urc_str,
                    "page": page_no,
                    "line": s[:240],
                    "description": desc[:160],
                }

# ---- Error Code extraction ----
# Error entries: "<number> <description>" inside CME/CMS sections
ERR_LINE_RE = re.compile(r"^\s*([0-9]{1,4})\s+([A-Z][A-Za-z0-9 \(\)\-/,\.]{3,120})\s*$")
err_section_pages = set()
err_section_type = {}
for page_no, body in pages:
    for line in body.splitlines():
        s = line.strip()
        m = re.match(r"^[0-9]+(?:\.[0-9]+){1,4}\s+(CME Error|CMS Error|Error Codes?|Appendix.*[Ee]rror)",
                     s, re.IGNORECASE)
        if m:
            err_section_pages.add(page_no)
            t = "CME" if "CME" in s.upper() else ("CMS" if "CMS" in s.upper() else "UNKNOWN")
            err_section_type[page_no] = t

err_zone = {}
for p in err_section_pages:
    for d in range(0, 8):
        err_zone[p + d] = err_section_type.get(p, "UNKNOWN")

err_entries = {}  # (type, code) -> dict
for page_no, body in pages:
    if page_no not in err_zone:
        continue
    etype = err_zone[page_no]
    for line in body.splitlines():
        s = line.strip()
        if len(s) < 5 or len(s) > 200:
            continue
        m = ERR_LINE_RE.match(s)
        if m:
            code = int(m.group(1))
            desc = m.group(2).strip()
            key = (etype, code)
            if key not in err_entries:
                err_entries[key] = {
                    "error_type": etype,
                    "code": code,
                    "meaning": desc[:160],
                    "page": page_no,
                    "line": s[:240],
                }

print(f"URC entries detected: {len(urc_entries)}")
for k, v in list(urc_entries.items())[:10]:
    print(f"  {k}  p{v['page']}  {v['description'][:60]}")
print(f"Error entries detected: {len(err_entries)}")
for (t, c), v in list(err_entries.items())[:10]:
    print(f"  {t} {c}  p{v['page']}  {v['meaning'][:60]}")

report = {
    "urc_entries": urc_entries,
    "err_entries": {f"{t}_{c}": v for (t, c), v in err_entries.items()},
    "total_urc": len(urc_entries),
    "total_err": len(err_entries),
}
(REPORTS / "_step_B2B3_parsed.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")