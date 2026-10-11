#!/usr/bin/env python3
"""Verify dat_01 records actually got annotated after dedup."""
import yaml, sys
from pathlib import Path
try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

p = find("dat_01")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list):
    records = [records]

total = len(records)
with_page = 0
with_section = 0
with_quote = 0
partial = 0
unknown = 0
for r in records:
    if not isinstance(r, dict):
        continue
    src = r.get("source") or {}
    if isinstance(src, dict):
        if src.get("page"): with_page += 1
        if src.get("section"): with_section += 1
        if src.get("quote"): with_quote += 1
    st = r.get("status")
    if st == "partial": partial += 1
    elif st == "unknown": unknown += 1

print(f"total={total} with_page={with_page} with_section={with_section} with_quote={with_quote} partial={partial} unknown={unknown}")
print("--- samples ---")
for r in records[:3]:
    if not isinstance(r, dict): continue
    src = r.get("source") or {}
    print(f"  {r.get('id')} cmd={r.get('command')} status={r.get('status')} page={src.get('page')} section={(src.get('section') or '')[:50]}")