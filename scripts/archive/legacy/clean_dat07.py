#!/usr/bin/env python3
"""clean_dat07.py — فقط از V2.02 بازسازی می‌کند."""
import csv, re, sys
from pathlib import Path
from datetime import datetime, timezone

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TABLES = ROOT / "sources" / "extracted" / "tables"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

PIN_NAME_RE = re.compile(r'^[A-Z][A-Z0-9_]{1,15}$')
PIN_NUM_RE  = re.compile(r'^\d{1,3}(?:,\d{1,3})*$')

def read_tsv(path):
    rows = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        r = csv.reader(f, delimiter="\t")
        next(r, None)
        for row in r:
            if len(row) >= 3:
                rows.append((row[0].strip(), row[1].strip(), row[2]))
    return rows

def parse_pins(tsv_path):
    pins = {}
    for page, _, text in read_tsv(tsv_path):
        cells = [c.strip() for c in text.split(" | ")]
        if len(cells) < 2: continue
        name, num = cells[0], cells[1]
        if not PIN_NAME_RE.match(name): continue
        if not PIN_NUM_RE.match(num): continue
        # reject suspicious: skip if function mentions frequency/band/temperature
        func = " ".join(cells[3:]).lower() if len(cells) > 3 else ""
        if any(x in func for x in ("frequency", "band", "temperature", "kbps", "mhz")):
            continue
        if name in pins: continue
        pins[name] = {
            "name": name,
            "pin_number": num,
            "direction": cells[2] if len(cells) > 2 and cells[2] in ("I","O","I/O","P","-") else "",
            "function": (cells[3] if len(cells) > 3 else "")[:200],
            "page": page,
        }
    return pins

def categorize(n):
    u = n.upper()
    if any(x in u for x in ("VBAT","VDD","GND","VRTC")): return "Power"
    if "SIM" in u: return "SIM"
    if u in ("TXD","RXD","RTS","CTS","DTR","DCD","RI"): return "UART"
    if "MIC" in u or "SPK" in u: return "Audio"
    if "ANT" in u or "RF" in u: return "RF"
    if "RESET" in u: return "Reset"
    if "PWRKEY" in u: return "PWRKEY"
    if "PCM" in u: return "PCM"
    if u.startswith("KBC"): return "Keypad"
    if "USB" in u or "VBUS" in u: return "USB"
    if "ADC" in u: return "ADC"
    if "PWM" in u: return "PWM"
    if u in ("SCL","SDA"): return "I2C"
    if "GPIO" in u: return "GPIO"
    if "ISINK" in u: return "GPIO"
    return "Other"

def main():
    pins = parse_pins(TABLES / "v2_02_ALL.tsv")
    print(f"  pins from V2.02: {len(pins)}")

    records = []
    for i, (name, p) in enumerate(sorted(pins.items()), 1):
        records.append({
            "id": f"dat_07_{i:04d}",
            "category": categorize(name),
            "source": {
                "name": "SIM800H&SIM800L_Hardware_Design",
                "version": "V2.02",
                "date": "2015-07-27",
                "page": p["page"],
                "section": "Pin Description",
            },
            "source_type": "primary",
            "confidence": 0.95,
            "status": "complete",
            "conflicts": [],
            "notes": "Extracted from V2.02 pin table only",
            "tags": [categorize(name).lower()],
            "applicable_models": ["SIM800L"],
            "created_at": NOW,
            "updated_at": NOW,
            "name": p["name"],
            "pin_number": p["pin_number"],
            "direction": p["direction"],
            "voltage_min": None, "voltage_typ": None, "voltage_max": None,
            "current_typ": None, "current_max": None,
            "function": p["function"],
            "alternate_function": None, "pull_up_down": None,
            "esd_rating": None, "impedance": None, "decoupling": None,
        })

    out = DATA / "dat_07_hardware_reference.yaml"
    header = f"# dat_07 — regenerated from V2.02 only at {NOW}\n"
    body = yaml.safe_dump(records, allow_unicode=True, sort_keys=False, default_flow_style=False)
    out.write_text(header + body, encoding="utf-8")

    with_num  = sum(1 for r in records if r["pin_number"])
    with_func = sum(1 for r in records if r["function"])
    with_dir  = sum(1 for r in records if r["direction"])
    print(f"  written: {len(records)} records")
    print(f"  with pin_number: {with_num}")
    print(f"  with function:   {with_func}")
    print(f"  with direction:  {with_dir}")
    return 0

if __name__ == "__main__":
    sys.exit(main())