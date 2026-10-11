#!/usr/bin/env python3
import sys, json
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

out = {}
for i in range(1, 19):
    dat_id = f"dat_{i:02d}"
    p = find(dat_id)
    if not p:
        out[dat_id] = {"file": None, "count": 0}
        continue
    records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    out[dat_id] = {
        "file": p.name,
        "count": len(records),
    }
print(json.dumps(out, ensure_ascii=False, indent=2))