#!/usr/bin/env python3
import sys, json, re
from pathlib import Path
from datetime import datetime, timezone
try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SRC_EX = ROOT / "sources" / "extracted"
REPORTS = ROOT / "reports"

def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    return c[0] if c else None

def load_paged(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    pages = []
    parts = re.split(r"<<<PAGE\s+(\d+)>>>", text)
    for i in range(1, len(parts) - 1, 2):
        try: num = int(parts[i])
        except Exception: continue
        pages.append((num, parts[i + 1]))
    return pages

pages = load_paged(SRC_EX / "v2_02_paged.txt")
def fuzzy(term):
    if not term: return None
    pat = re.compile(re.escape(str(term)[:40]), re.IGNORECASE)
    for pn, body in pages:
        for line in body.splitlines():
            s = line.strip()
            if len(s) < 4 or len(s) > 240: continue
            if pat.search(s):
                return (pn, s)
    return None

p = find("dat_06")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
blocked = 0
for r in records:
    if not isinstance(r, dict): continue
    src = r.get("source") or {}
    if isinstance(src, dict) and src.get("page"):
        if r.get("status") == "partial":
            # already partial with page; keep
            continue
        continue
    # try to fill from v2_02
    hit = None
    for key in ("command","category","step_order","related_state"):
        v = r.get(key)
        if v: hit = fuzzy(v); 
        if hit: break
    if hit:
        pn, line = hit
        src = src if isinstance(src, dict) else {}
        src["page"] = str(pn)
        if not src.get("section"): src["section"] = "Hardware Design V2.02"
        if not src.get("quote"): src["quote"] = line[:260]
        if not src.get("name"): src["name"] = "SIM800H&SIM800L_Hardware_Design"
        if not src.get("version"): src["version"] = "V2.02"
        if not src.get("date"): src["date"] = "2015-07-27"
        r["source"] = src
        r["status"] = "partial"
        if r.get("confidence") in (0.0, 0): r["confidence"] = 0.5
        r["updated_at"] = ts
        filled += 1
    else:
        r["status"] = "blocked"
        r["confidence"] = 0.0
        notes = r.get("notes") or ""
        marker = "No additional init source in V2.02"
        if marker not in notes:
            r["notes"] = (notes + " | " + marker + ".").strip(" |")
        r["updated_at"] = ts
        blocked += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)

partial = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "partial")
unknown = sum(1 for r in records if isinstance(r, dict) and r.get("status") == "unknown")
summary = {"total": len(records), "filled": filled, "blocked": blocked, "partial": partial, "unknown": unknown}
(REPORTS / "_step_D8_dat06.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_06: total={len(records)} partial={partial} unknown={unknown} filled={filled} blocked={blocked}")