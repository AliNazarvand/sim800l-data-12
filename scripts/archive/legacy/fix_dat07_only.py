#!/usr/bin/env python3
"""fix_dat07_only.py — فقط dat_07 را از TSV بازسازی می‌کند."""
import csv, re, sys
from pathlib import Path
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pyyaml"])
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
        reader = csv.reader(f, delimiter="\t")
        next(reader, None)  # header
        for r in reader:
            if len(r) >= 3:
                rows.append((r[0].strip(), r[1].strip(), r[2]))
    return rows

def parse_pins_from_tsv(tsv_path, source_name, source_ver):
    pins = {}
    rows = read_tsv(tsv_path)
    for page, tidx, row_text in rows:
        cells = [c.strip() for c in row_text.split(" | ")]
        if len(cells) < 2:
            continue
        name = cells[0]
        num  = cells[1]
        if not PIN_NAME_RE.match(name):
            continue
        if not PIN_NUM_RE.match(num):
            continue
        direction = cells[2] if len(cells) > 2 and cells[2] in ("I","O","I/O","P","-") else ""
        function  = cells[3] if len(cells) > 3 else ""
        # skip if already have this pin from a better (later) source
        if name in pins:
            continue
        pins[name] = {
            "name": name,
            "pin_number": num,
            "direction": direction,
            "function": function[:200],
            "page": page,
            "source_name": source_name,
            "source_ver": source_ver,
        }
    return pins

def categorize(name):
    n = name.upper()
    if any(x in n for x in ("VBAT","VDD","GND","VRTC")): return "Power"
    if "SIM" in n: return "SIM"
    if n in ("TXD","RXD","RTS","CTS","DTR","DCD","RI"): return "UART"
    if "MIC" in n or "SPK" in n: return "Audio"
    if "ANT" in n or "RF" in n: return "RF"
    if "RESET" in n: return "Reset"
    if "PWRKEY" in n: return "PWRKEY"
    if "PCM" in n: return "PCM"
    if n.startswith("KBC"): return "Keypad"
    if "USB" in n or "VBUS" in n: return "USB"
    if "ADC" in n: return "ADC"
    if "PWM" in n: return "PWM"
    if n in ("SCL","SDA"): return "I2C"
    if "GPIO" in n: return "GPIO"
    if "ISINK" in n: return "GPIO"
    return "Other"

def main():
    v202 = TABLES / "v2_02_ALL.tsv"
    v100 = TABLES / "v1_00_ALL.tsv"
    if not v202.exists():
        print("ERROR: v2_02_ALL.tsv missing")
        return 1

    # first from V2.02 (higher priority), then V1.00 for anything missed
    pins = parse_pins_from_tsv(v202,
        "SIM800H&SIM800L_Hardware_Design", "V2.02")
    print(f"  pins from V2.02: {len(pins)}")
    if v100.exists():
        pins_v100 = parse_pins_from_tsv(v100, "SIM800L_Hardware_Design", "V1.00")
        added = 0
        for k, v in pins_v100.items():
            if k not in pins:
                pins[k] = v
                added += 1
        print(f"  extra from V1.00: {added}")

    # build records
    records = []
    for i, (name, p) in enumerate(sorted(pins.items()), 1):
        records.append({
            "id": f"dat_07_{i:04d}",
            "category": categorize(name),
            "source": {
                "name": p["source_name"],
                "version": p["source_ver"],
                "date": "2015-07-27" if p["source_ver"] == "V2.02" else "2013-08-20",
                "page": p["page"],
                "section": "Pin Description",
            },
            "source_type": "primary",
            "confidence": 0.9,
            "status": "complete",
            "conflicts": [],
            "notes": "Extracted from PDF table via TSV",
            "tags": [categorize(name).lower()],
            "applicable_models": ["SIM800L"],
            "created_at": NOW,
            "updated_at": NOW,
            "name": p["name"],
            "pin_number": p["pin_number"],
            "direction": p["direction"],
            "voltage_min": None,
            "voltage_typ": None,
            "voltage_max": None,
            "current_typ": None,
            "current_max": None,
            "function": p["function"],
            "alternate_function": None,
            "pull_up_down": None,
            "esd_rating": None,
            "impedance": None,
            "decoupling": None,
        })

    out = DATA / "dat_07_hardware_reference.yaml"
    header = f"# dat_07 — regenerated from TSV at {NOW}\n"
    body = yaml.safe_dump(records, allow_unicode=True, sort_keys=False, default_flow_style=False)
    out.write_text(header + body, encoding="utf-8")
    print(f"  written: {out.name} ({len(records)} records)")

    # stats
    with_num = sum(1 for r in records if r["pin_number"])
    with_func = sum(1 for r in records if r["function"])
    print(f"  with pin_number: {with_num}")
    print(f"  with function:   {with_func}")
    return 0

if __name__ == "__main__":
    sys.exit(main())