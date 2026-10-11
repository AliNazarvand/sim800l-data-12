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
REPORTS = ROOT / "reports"

def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    return c[0] if c else None

NUM_RE = re.compile(r"\b\d+(?:\.\d+)?\b")
UNIT_RE = re.compile(r"\b(mA|uA|µA|V|mV)\b", re.IGNORECASE)

p = find("dat_15")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("value_typ") not in (None, 0, ""): continue
    src = r.get("source") or {}
    quote = src.get("quote") if isinstance(src, dict) else None
    text = " ".join([str(r.get("parameter") or ""), str(quote or "")])
    nums = NUM_RE.findall(text)
    if len(nums) >= 1:
        try:
            if len(nums) >= 3:
                r["value_min"] = float(nums[0])
                r["value_typ"] = float(nums[1])
                r["value_max"] = float(nums[2])
            elif len(nums) == 2:
                r["value_min"] = float(nums[0])
                r["value_max"] = float(nums[1])
                r["value_typ"] = (float(nums[0])+float(nums[1]))/2.0
            else:
                r["value_typ"] = float(nums[0])
            m = UNIT_RE.search(text)
            if m and not r.get("unit"): r["unit"] = m.group(0)
            r["updated_at"] = ts
            filled += 1
        except Exception:
            pass

with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)

wv = sum(1 for r in records if isinstance(r, dict) and r.get("value_typ") not in (None, 0, ""))
summary = {"total": len(records), "with_values": wv, "filled": filled}
(REPORTS / "_step_D8_dat15_values.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_15: total={len(records)} with_values={wv} filled={filled}")