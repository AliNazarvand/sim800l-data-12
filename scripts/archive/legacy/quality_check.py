#!/usr/bin/env python3
"""Visual quality check of all datasets."""
import pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

def load(prefix):
    fs = sorted(DATA.glob(f"{prefix}_*.yaml")) or sorted(DATA.glob(f"{prefix}.yaml"))
    if not fs: return []
    try: d = yaml.safe_load(fs[0].read_text(encoding="utf-8")) or {}
    except Exception: return []
    recs = d.get("records") if isinstance(d, dict) else d
    return recs if isinstance(recs, list) else []

print("===== QUALITY CHECK =====")
print()
print(f"-- dat_01 AT commands: {len(load('dat_01'))} --")
print(f"-- dat_02 URCs:        {len(load('dat_02'))} --")
print(f"-- dat_03 errors:      {len(load('dat_03'))} --")
print(f"-- dat_04 timings:     {len(load('dat_04'))} --")
print(f"-- dat_05 states:      {len(load('dat_05'))} --")
print(f"-- dat_06 init steps:  {len(load('dat_06'))} --")
print(f"-- dat_07 pins:        {len(load('dat_07'))} --")
print(f"-- dat_09 SMS:         {len(load('dat_09'))} --")
print(f"-- dat_10 GPRS:        {len(load('dat_10'))} --")
print(f"-- dat_11 HTTP/FTP:    {len(load('dat_11'))} --")
print(f"-- dat_12 Audio:       {len(load('dat_12'))} --")
print(f"-- dat_13 SIM:         {len(load('dat_13'))} --")
print(f"-- dat_15 Power:       {len(load('dat_15'))} --")
print()
print("-- dat_07 Pins (full list) --")
pins = load("dat_07")
for r in pins:
    fn = r.get('function','')
    if len(fn) > 45: fn = fn[:42] + "..."
    print(f"  {r['name']:<12} pin={str(r.get('pin_number','?')):<12} {str(r.get('direction','?')):<5} {fn}")
print(f"  TOTAL: {len(pins)} pins")