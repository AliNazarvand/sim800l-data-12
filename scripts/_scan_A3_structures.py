#!/usr/bin/env python3
"""Scan V2.02 and V1.00 for STRUCTURED sections relevant to timing / state / init.
   Report only; does NOT modify any data file."""
import sys, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_EX = ROOT / "sources" / "extracted"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

def load_paged(path):
    if not path.exists():
        return []
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

v202 = load_paged(SRC_EX / "v2_02_paged.txt")
v100 = load_paged(SRC_EX / "v1_00_paged.txt")

# الگوهای ساختاری
TABLE_RE = re.compile(r"\bTable\s+([0-9]+[\-\.][0-9]+|[0-9]+)\s*[:\.]?\s*(.{3,80})", re.IGNORECASE)
FIGURE_RE = re.compile(r"\bFigure\s+([0-9]+[\-\.][0-9]+|[0-9]+)\s*[:\.]?\s*(.{3,80})", re.IGNORECASE)
SECTION_RE = re.compile(r"^\s*([0-9]+\.[0-9]+(?:\.[0-9]+)?)\s+([A-Z][A-Za-z0-9 \-/&]{3,60})\s*$")

def scan_structure(pages):
    """Return dict: {tables: [...], figures: [...], sections: [...], headings_by_keyword: {...}}"""
    tables = []
    figures = []
    sections = []
    keyword_hits = {
        "timing": [],
        "state": [],
        "init": [],
        "startup": [],
        "boot": [],
        "power-on": [],
        "power_on": [],
        "power sequence": [],
    }
    for page_no, body in pages:
        for line in body.splitlines():
            s = line.strip()
            if len(s) < 4:
                continue
            m = TABLE_RE.search(s)
            if m:
                tables.append({"page": page_no, "id": m.group(1), "title": m.group(2).strip()[:120]})
            m = FIGURE_RE.search(s)
            if m:
                figures.append({"page": page_no, "id": m.group(1), "title": m.group(2).strip()[:120]})
            m = SECTION_RE.match(s)
            if m:
                sections.append({"page": page_no, "id": m.group(1), "title": m.group(2).strip()[:120]})
            low = s.lower()
            for key in keyword_hits:
                if key in low and len(s) < 200:
                    keyword_hits[key].append({"page": page_no, "line": s[:160]})
    return {"tables": tables, "figures": figures, "sections": sections, "keywords": keyword_hits}

report = {
    "V2.02": scan_structure(v202),
    "V1.00": scan_structure(v100),
    "summary": {
        "V2.02": {"tables": 0, "figures": 0, "sections": 0},
        "V1.00": {"tables": 0, "figures": 0, "sections": 0},
    }
}
for ver in ["V2.02", "V1.00"]:
    report["summary"][ver]["tables"] = len(report[ver]["tables"])
    report["summary"][ver]["figures"] = len(report[ver]["figures"])
    report["summary"][ver]["sections"] = len(report[ver]["sections"])

out = REPORTS / "_step_A3_structured_scan.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

# چاپ خلاصه
for ver in ["V2.02", "V1.00"]:
    s = report["summary"][ver]
    print(f"{ver}: tables={s['tables']} figures={s['figures']} sections={s['sections']}")

print()
print("--- Samples (V2.02) ---")
for t in report["V2.02"]["tables"][:8]:
    print(f"TABLE p{t['page']} [{t['id']}] {t['title']}")
for f in report["V2.02"]["figures"][:8]:
    print(f"FIGURE p{f['page']} [{f['id']}] {f['title']}")
for sec in report["V2.02"]["sections"][:15]:
    print(f"SECTION p{sec['page']} {sec['id']} {sec['title']}")

# تشخیص اینکه برای هر دیتاست، ساختار موجود هست یا نه
found = {
    "dat_04_timing": False,
    "dat_05_state": False,
    "dat_06_init": False,
}
# dat_04: table/figure/section حاوی timing/reset/power-on sequence
for source in ["V2.02", "V1.00"]:
    for t in report[source]["tables"]:
        title = t["title"].lower()
        if any(k in title for k in ["timing", "reset", "power-on", "power on", "sequence", "startup"]):
            found["dat_04_timing"] = True
    for s in report[source]["sections"]:
        title = s["title"].lower()
        if any(k in title for k in ["timing", "reset", "power-on", "power sequence", "startup"]):
            found["dat_04_timing"] = True

# dat_05: figure/section حاوی state/state diagram/operating modes
for source in ["V2.02", "V1.00"]:
    for f in report[source]["figures"]:
        title = f["title"].lower()
        if any(k in title for k in ["state", "operation", "mode"]):
            found["dat_05_state"] = True
    for s in report[source]["sections"]:
        title = s["title"].lower()
        if any(k in title for k in ["state", "operating mode", "power state", "operation mode"]):
            found["dat_05_state"] = True

# dat_06: section حاوی initialization/startup/power-on sequence
for source in ["V2.02", "V1.00"]:
    for s in report[source]["sections"]:
        title = s["title"].lower()
        if any(k in title for k in ["initial", "startup", "power on", "power-on", "boot"]):
            found["dat_06_init"] = True

print()
print("--- Structure found ---")
for k, v in found.items():
    print(f"{k}: {v}")

report["structure_found"] = found
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")