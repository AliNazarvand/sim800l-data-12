#!/usr/bin/env python3
import sys, json, re
from pathlib import Path
from datetime import datetime, timezone
try:
    import yaml
except ImportError: sys.exit(2)
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"; SRC_EX = ROOT / "sources" / "extracted"; REPORTS = ROOT / "reports"
def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml")); return c[0] if c else None
def load_paged(path):
    if not path.exists(): return []
    text = path.read_text(encoding="utf-8", errors="replace")
    pages = []; parts = re.split(r"<<<PAGE\s+(\d+)>>>", text)
    for i in range(1, len(parts) - 1, 2):
        try: num = int(parts[i])
        except Exception: continue
        pages.append((num, parts[i+1]))
    return pages
pages = load_paged(SRC_EX / "v2_02_paged.txt") + load_paged(SRC_EX / "v1_00_paged.txt")
def fuzzy(term):
    if not term: return None
    pat = re.compile(re.escape(str(term)[:30]), re.IGNORECASE)
    for pn, body in pages:
        for line in body.splitlines():
            s = line.strip()
            if len(s) < 4 or len(s) > 220: continue
            if pat.search(s): return (pn, s)
    return None
p = find("dat_15")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0; blocked = 0
for r in records:
    if not isinstance(r, dict): continue
    src = r.get("source") or {}
    if isinstance(src, dict) and src.get("page"): continue
    hit = None
    for k in ("parameter","mode","command","category"):
        v = r.get(k)
        if v: hit = fuzzy(v)
        if hit: break
    if hit:
        pn, line = hit
        src = src if isinstance(src, dict) else {}
        src["page"] = str(pn); src.setdefault("section","Power Management"); src.setdefault("quote", line[:260])
        src.setdefault("name","SIM800H&SIM800L_Hardware_Design"); src.setdefault("version","V2.02"); src.setdefault("date","2015-07-27")
        r["source"] = src
        if r.get("status") == "unknown": r["status"] = "partial"
        if r.get("confidence") in (0.0,0): r["confidence"] = 0.5
        r["updated_at"] = ts; filled += 1
    else:
        r["status"] = "blocked"; r["confidence"] = 0.0
        notes = r.get("notes") or ""
        if "No additional power source" not in notes: r["notes"] = (notes + " | No additional power source in V2.02/V1.00.").strip(" |")
        r["updated_at"] = ts; blocked += 1
with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
wp = sum(1 for r in records if isinstance(r, dict) and (r.get("source") or {}).get("page"))
(REPORTS / "_step_D11_dat15.json").write_text(json.dumps({"total":len(records),"with_page":wp,"filled":filled,"blocked":blocked}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_15: total={len(records)} with_page={wp} filled={filled} blocked={blocked}")