#!/usr/bin/env python3
"""Diagnose dat_01: record count, status, whether source.page/section are filled."""
import json, sys
from pathlib import Path
try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

p = find("dat_01")
if p is None:
    print("dat_01 not found"); sys.exit(1)
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list):
    records = [records]

from collections import Counter
status_counts = Counter()
has_page = 0
has_section = 0
has_quote = 0
has_command = 0
for r in records:
    if not isinstance(r, dict):
        continue
    status_counts[r.get("status")] += 1
    src = r.get("source") or {}
    if isinstance(src, dict):
        if src.get("page"): has_page += 1
        if src.get("section"): has_section += 1
        if src.get("quote"): has_quote += 1
    if r.get("command"): has_command += 1

report = {
    "file": p.name,
    "total": len(records),
    "status_counts": dict(status_counts),
    "with_command": has_command,
    "with_page": has_page,
    "with_section": has_section,
    "with_quote": has_quote,
    "sample": records[0] if records else None,
}
out = REPORTS / "_step_B1_dat01_diagnosis.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
print(f"total={len(records)} status={dict(status_counts)}")
print(f"with_command={has_command} with_page={has_page} with_section={has_section} with_quote={has_quote}")