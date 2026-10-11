#!/usr/bin/env python3
"""Scan AT Manual V1.01 for URC and Error Code sections.
   Report only; does not modify any data file."""
import sys, json, re
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

# الگوهای سکشن
URC_TITLE_RE = re.compile(
    r"^\s*([0-9]+(?:\.[0-9]+){1,4})?\s*(URC|Unsolicited|Unsolicited Result)",
    re.IGNORECASE
)
ERR_TITLE_RE = re.compile(
    r"^\s*([0-9]+(?:\.[0-9]+){1,4})?\s*(CME Error|CMS Error|Error Code|Error Codes|Appendix.*[Ee]rror)",
    re.IGNORECASE
)

urc_sections = []
err_sections = []
for page_no, body in pages:
    for line in body.splitlines():
        s = line.strip()
        if len(s) < 6 or len(s) > 200:
            continue
        if URC_TITLE_RE.match(s):
            urc_sections.append({"page": page_no, "title": s[:200]})
        if ERR_TITLE_RE.match(s):
            err_sections.append({"page": page_no, "title": s[:200]})

report = {
    "urc_sections": urc_sections,
    "err_sections": err_sections,
    "total_urc": len(urc_sections),
    "total_err": len(err_sections),
}
(REPORTS / "_step_B2B3_section_scan.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

print(f"URC sections detected: {len(urc_sections)}")
for s in urc_sections[:10]:
    print(f"  p{s['page']}: {s['title']}")
print(f"Error sections detected: {len(err_sections)}")
for s in err_sections[:10]:
    print(f"  p{s['page']}: {s['title']}")