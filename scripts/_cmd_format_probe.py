#!/usr/bin/env python3
import yaml
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

def load(f):
    try:
        d = yaml.safe_load(f.read_text(encoding="utf-8")) or []
        return d if isinstance(d, list) else [d]
    except Exception:
        return []

def sample(dat_id, n=5):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    if not c: return []
    data = load(c[0])
    out = []
    for r in data:
        if isinstance(r, dict):
            v = r.get("command") or r.get("related_command")
            if v: out.append(str(v))
        if len(out) >= n: break
    return out

print("Command format samples (read-only):")
for d in ["dat_01","dat_02","dat_09","dat_10","dat_11","dat_12","dat_13","dat_17"]:
    s = sample(d)
    print(f"  {d}: {s}")
