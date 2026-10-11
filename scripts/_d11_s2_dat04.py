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
v202 = load_paged(SRC_EX / "v2_02_paged.txt"); v100 = load_paged(SRC_EX / "v1_00_paged.txt")
NUM_RE = re.compile(r"\b\d+(?:\.\d+)?\b")
UNIT_RE = re.compile(r"\b(ms|us|µs|s|mV|V|mA|uA|µA|kbps)\b", re.IGNORECASE)
def fuzzy(term, pages):
    if not term: return None
    pat = re.compile(re.escape(str(term)[:40]), re.IGNORECASE)
    for pn, body in pages:
        for line in body.splitlines():
            s = line.strip()
            if len(s) < 8 or len(s) > 220: continue
            if pat.search(s):
                nums = NUM_RE.findall(s)
                if len(nums) >= 2 and UNIT_RE.search(s): return (pn, s, nums)
    return None
p = find("dat_04")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("value_typ") not in (None, 0, ""): continue
    hit = None
    for k in ("parameter","name","condition","category"):
        v = r.get(k)
        if not v: continue
        hit = fuzzy(v, v202) or fuzzy(v, v100)
        if hit: break
    if not hit: continue
    pn, line, nums = hit
    try:
        if len(nums) >= 3:
            r["value_min"] = float(nums[0]); r["value_typ"] = float(nums[1]); r["value_max"] = float(nums[2])
        elif len(nums) == 2:
            r["value_min"] = float(nums[0]); r["value_max"] = float(nums[1]); r["value_typ"] = (float(nums[0])+float(nums[1]))/2.0
        else:
            r["value_typ"] = float(nums[0])
        m = UNIT_RE.search(line)
        if m and not r.get("unit"): r["unit"] = m.group(0)
        src = r.get("source") or {}
        if not isinstance(src, dict): src = {}
        if not src.get("page"): src["page"] = str(pn)
        if not src.get("quote"): src["quote"] = line[:260]
        r["source"] = src; r["updated_at"] = ts; filled += 1
    except Exception: pass
with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
wv = sum(1 for r in records if isinstance(r, dict) and r.get("value_typ") not in (None, 0, ""))
(REPORTS / "_step_D11_dat04.json").write_text(json.dumps({"total":len(records),"with_values":wv,"filled":filled}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_04: total={len(records)} with_values={wv} filled={filled}")