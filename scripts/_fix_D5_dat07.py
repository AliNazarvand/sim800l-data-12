#!/usr/bin/env python3
"""Fill source for remaining dat_07 unsourced records via fuzzy search in both PDFs."""
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
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

def load_paged(path):
    if not path.exists(): return []
    text = path.read_text(encoding="utf-8", errors="replace")
    pages = []
    parts = re.split(r"<<<PAGE\s+(\d+)>>>", text)
    for i in range(1, len(parts) - 1, 2):
        try: num = int(parts[i])
        except Exception: continue
        pages.append((num, parts[i + 1]))
    return pages

v202 = load_paged(SRC_EX / "v2_02_paged.txt")
v100 = load_paged(SRC_EX / "v1_00_paged.txt")

def fuzzy(term, pages):
    if not term: return None
    pat = re.compile(r"\b" + re.escape(str(term).strip()) + r"\b", re.IGNORECASE)
    for pn, body in pages:
        for line in body.splitlines():
            s = line.strip()
            if len(s) < 3 or len(s) > 260: continue
            if pat.search(s):
                if any(k in s.lower() for k in ["gnd","vbat","vdd","txd","rxd","pwr","reset","sim","mic",
                                                 "spk","gpio","adc","rf","ant","pin","v","ma","mm"]):
                    return (pn, s)
    return None

p = find("dat_07")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
blocked = 0
for r in records:
    if not isinstance(r, dict): continue
    src = r.get("source") or {}
    if isinstance(src, dict) and src.get("page"): continue
    # try each of: name, pin_number, category
    hit = None; ver = "V2.02"
    for key in ("name", "pin_number"):
        v = r.get(key)
        if v:
            hit = fuzzy(v, v202)
            if hit: break
    if not hit:
        for key in ("name", "pin_number"):
            v = r.get(key)
            if v:
                hit = fuzzy(v, v100)
                if hit: ver = "V1.00"; break
    if hit:
        pn, line = hit
        src = src if isinstance(src, dict) else {}
        src["page"] = str(pn)
        if not src.get("section"): src["section"] = "Hardware Reference"
        if not src.get("quote"): src["quote"] = line[:280]
        if not src.get("name"): src["name"] = "SIM800H&SIM800L_Hardware_Design" if ver=="V2.02" else "SIM800L_Hardware_Design"
        if not src.get("version"): src["version"] = ver
        if not src.get("date"): src["date"] = "2015-07-27" if ver=="V2.02" else "2013-08-20"
        r["source"] = src
        if r.get("status") == "unknown": r["status"] = "partial"
        if r.get("confidence") in (0.0, 0): r["confidence"] = 0.5
        r["updated_at"] = ts
        filled += 1
    else:
        r["status"] = "blocked"
        r["confidence"] = 0.0
        r["updated_at"] = ts
        blocked += 1

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)

with_page = sum(1 for r in records if isinstance(r, dict) and (r.get("source") or {}).get("page"))
summary = {"total": len(records), "with_page": with_page, "filled": filled, "blocked": blocked}
(REPORTS / "_step_D5_dat07.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_07: total={len(records)} with_page={with_page} filled={filled} blocked={blocked}")