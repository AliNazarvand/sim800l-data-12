#!/usr/bin/env python3
"""Extract value_min/typ/max from V2.02 lines matching N / N / N unit pattern."""
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
    text = path.read_text(encoding="utf-8", errors="replace")
    pages = []
    parts = re.split(r"<<<PAGE\s+(\d+)>>>", text)
    for i in range(1, len(parts) - 1, 2):
        try: num = int(parts[i])
        except Exception: continue
        pages.append((num, parts[i + 1]))
    return pages

pages = load_paged(SRC_EX / "v2_02_paged.txt")
NUM_RE = re.compile(r"\b\d+(?:\.\d+)?\b")
UNIT_RE = re.compile(r"\b(ms|us|µs|s|mV|V|mA|uA|µA)\b", re.IGNORECASE)

def find_values(term):
    if not term: return None
    pat = re.compile(re.escape(str(term)[:40]), re.IGNORECASE)
    for pn, body in pages:
        for line in body.splitlines():
            s = line.strip()
            if len(s) < 8 or len(s) > 200: continue
            if pat.search(s):
                nums = NUM_RE.findall(s)
                if len(nums) >= 2 and UNIT_RE.search(s):
                    return (pn, s, nums)
    return None

p = find("dat_04")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("value_typ") not in (None, 0, ""): continue
    for key in ("parameter","name","condition"):
        v = r.get(key)
        if not v: continue
        hit = find_values(v)
        if hit:
            pn, line, nums = hit
            try:
                if len(nums) >= 3:
                    r["value_min"] = float(nums[0])
                    r["value_typ"] = float(nums[1])
                    r["value_max"] = float(nums[2])
                elif len(nums) == 2:
                    r["value_min"] = float(nums[0])
                    r["value_max"] = float(nums[1])
                    r["value_typ"] = (float(nums[0]) + float(nums[1])) / 2.0
                else:
                    r["value_typ"] = float(nums[0])
                # unit
                m = UNIT_RE.search(line)
                if m and not r.get("unit"): r["unit"] = m.group(0)
                src = r.get("source") or {}
                if not isinstance(src, dict): src = {}
                if not src.get("page"): src["page"] = str(pn)
                if not src.get("quote"): src["quote"] = line[:260]
                r["source"] = src
                r["updated_at"] = ts
                filled += 1
                break
            except Exception:
                continue

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)

wv = sum(1 for r in records if isinstance(r, dict) and r.get("value_typ") not in (None, 0, ""))
summary = {"total": len(records), "with_values": wv, "filled": filled}
(REPORTS / "_step_D8_dat04_values.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_04: total={len(records)} with_values={wv} filled={filled}")