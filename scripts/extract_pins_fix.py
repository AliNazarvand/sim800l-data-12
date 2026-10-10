#!/usr/bin/env python3
"""dat_07 dedicated extractor with multi-column support.

Fixes the pin extraction problem:
- Multi-match regex per line (catches 2 pins per line)
- Multiple V2.02 marker patterns
- Manual curated fill for pins hidden by two-column layout
- Dedup keeps first (V2.02 priority over V1.00)
"""
import re, sys, pathlib
from datetime import datetime, timezone
try:
    import yaml
except ImportError:
    print("ERROR: pip install pyyaml"); sys.exit(2)

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC  = ROOT / "sources" / "extracted"
DATA = ROOT / "data"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def read(p):
    try: return pathlib.Path(p).read_text(encoding="utf-8", errors="ignore")
    except Exception: return ""

def find_hw():
    hw1 = hw2 = ""
    for f in sorted(SRC.glob("*.txt")):
        t = read(f)
        if len(t) < 500: continue
        name = f.name
        if "Hardware" in name or "Hardware_Design" in name:
            if "1.00" in name: hw1 = t; print(f"  [HW1] {name} ({len(t)})")
            elif "2.02" in name: hw2 = t; print(f"  [HW2] {name} ({len(t)})")
    return hw1, hw2

# Multi-match: find all pins in a line, using lookahead to detect start of next pin
PIN_GLOBAL = re.compile(
    r'\b([A-Z][A-Z0-9_]{1,20})\s+'          # name
    r'(\d[\d,\s]{0,40}?)\s+'                 # pin numbers
    r'(I/O|IO|I|O)\s+'                       # direction
    r'([^\n]{0,180}?)'                       # description (lazy)
    r'(?=\s+[A-Z][A-Z0-9_]{1,20}\s+\d|\s*$)'  # next pin or end
)
PIN_SIMPLE = re.compile(
    r'^([A-Z][A-Z0-9_]{1,20})\s+(\d[\d,\s]{0,40}?)\s+(I/O|IO|I|O)\s+(.{2,180})$'
)

V202_MARKERS = [
    r"Table 4:\s*Pin description",
    r"Table 2:\s*Pin description",
    r"Table\s+\d+:\s*Pin\s+description",
    r"3\.2\.\s*Pin Description",
    r"Pin Description",
    r"Pin name\s+Pin number",
    r"Pin\s+name\s+Pin\s+number",
    r"Table\s+\d+\s*:.*Pin\s+description",
]

def find_pin_body(text, version):
    for i, marker in enumerate(V202_MARKERS):
        try:
            m = re.search(marker, text, re.IGNORECASE)
        except Exception:
            continue
        if m:
            print(f"  [DBG] Pin({version}): marker[{i}] FOUND at {m.start()} -> {marker[:40]}")
            rest = text[m.end():]
            for end_pat in [r"3\.3\.", r"\nPackage Dimensions", r"\n4\.\s+Application", r"\n\d+\.\d+\.\s+[A-Z]"]:
                em = re.search(end_pat, rest)
                if em and em.start() > 200:
                    return rest[:em.start()]
            return rest[:40000]
    print(f"  [DBG] Pin({version}): NO marker found")
    return None

def extract_from_body(body, version):
    out, seen = [], set()
    if not body: return out
    for line in body.split("\n"):
        s = line.strip()
        if not s: continue
        if "Smart Machine" in s: continue
        if s.startswith("Pin name") or s.startswith("Pin Name"): continue
        matches = list(PIN_GLOBAL.finditer(s))
        if not matches:
            matches = list(PIN_SIMPLE.finditer(s))
        for m in matches:
            try:
                name = m.group(1).strip()
                pins = re.sub(r'\s+','', m.group(2).strip()).rstrip(',')
                direction = m.group(3).strip()
                desc = (m.group(4) if m.lastindex >= 4 else "").strip()
            except Exception:
                continue
            if len(name) < 2 or len(name) > 22: continue
            if name in {"PIN","PINNAME","TABLE","THIS","THESE","POWER","ON","IO"}: continue
            if not re.match(r'^[A-Z][A-Z0-9_/]+$', name): continue
            key = name.upper()
            if key in seen: continue
            seen.add(key)
            out.append({
                "id": None, "category": "Pin", "name": name,
                "pin_number": pins, "direction": direction,
                "function": desc[:180],
                "source": {
                    "name": "SIM800L_Hardware_Design",
                    "version": version,
                    "date": "2013-08-20" if version=="V1.00" else "2015-07-27",
                    "section": "Table 4 Pin Description"
                },
                "source_type": "primary", "confidence": 0.85,
                "status": "complete",
                "applicable_models": ["SIM800L"],
                "notes": f"auto-extracted from {version} (multi-column)",
                "tags": ["pin"], "created_at": NOW, "updated_at": NOW
            })
    return out

# Curated pins from SIM800L_Hardware_Design_V1.00 Table 4 (pages 16-18)
# These are hidden by the two-column layout and would be lost by regex
MANUAL_V100 = [
    ("MIC1P",   "52", "I",   "Main Audio input positive",         "4.7 Table 13"),
    ("MIC1N",   "12", "I",   "Main Audio input negative",         "4.7 Table 13"),
    ("MIC2P",   "9",  "I",   "Secondary Audio input positive",    "4.7 Table 13"),
    ("MIC2N",   "10", "I",   "Secondary Audio input negative",    "4.7 Table 13"),
    ("SPK1P",   "53", "O",   "Main Audio output positive",        "4.7 Table 13"),
    ("SPK1N",   "13", "O",   "Main Audio output negative",        "4.7 Table 13"),
    ("SPK2P",   "51", "O",   "Secondary Audio output positive",   "4.7 Table 13"),
    ("SPK2N",   "11", "O",   "Secondary Audio output negative",   "4.7 Table 13"),
    ("PCMCLK",  "29", "O",   "PCM clock",                         "4.9 Table 20"),
    ("PCMOUT",  "30", "O",   "PCM data output",                   "4.9 Table 20"),
    ("PCMSYNC", "65", "O",   "PCM synchrony",                     "4.9 Table 20"),
    ("PCMIN",   "66", "I",   "PCM data input",                    "4.9 Table 20"),
    ("COL0",    "20", "I",   "Keypad column 0 (pull up)",         "4.10 Table 23"),
    ("COL1",    "25", "I",   "Keypad column 1 (pull down)",       "4.10 Table 23"),
    ("COL2",    "22", "I",   "Keypad column 2 (pull down)",       "4.10 Table 23"),
    ("COL3",    "21", "I",   "Keypad column 3 (pull down)",       "4.10 Table 23"),
    ("COL4",    "24", "I",   "Keypad column 4 (pull down)",       "4.10 Table 23"),
    ("ROW0",    "62", "O",   "Keypad row 0 (pull down)",          "4.10 Table 23"),
    ("ROW1",    "60", "O",   "Keypad row 1 (pull down)",          "4.10 Table 23"),
    ("ROW2",    "61", "O",   "Keypad row 2 (pull down)",          "4.10 Table 23"),
    ("ROW3",    "23", "O",   "Keypad row 3 (pull down)",          "4.10 Table 23"),
    ("ROW4",    "63", "O",   "Keypad row 4 (pull down)",          "4.10 Table 23"),
    ("GPIO1",   "3",  "I/O", "Programmable general purpose IO 1", "4.12 Table 27"),
    ("GPIO2",   "27", "I/O", "Programmable general purpose IO 2", "4.12 Table 27"),
    ("GPIO3",   "28", "I/O", "Programmable general purpose IO 3", "4.12 Table 27"),
    ("USB_DP",  "59", "I/O", "USB data plus (debug/download)",    "4.5 Table 8"),
    ("USB_DM",  "19", "I/O", "USB data minus (debug/download)",   "4.5 Table 8"),
    ("VBUS",    "7",  "I",   "USB power supply (4.3-7V)",         "4.5.3 Table 10"),
    ("FM_ANT_P","17", "I",   "FM differential antenna positive",  "4.19.2"),
    ("FM_ANT_N","57", "I",   "FM differential antenna negative",  "4.19.2"),
]

def manual_pins(version="V1.00"):
    out = []
    for name, pin, direction, desc, section in MANUAL_V100:
        out.append({
            "id": None, "category": "Pin", "name": name,
            "pin_number": pin, "direction": direction,
            "function": desc,
            "source": {
                "name": "SIM800L_Hardware_Design",
                "version": version,
                "date": "2013-08-20" if version=="V1.00" else "2015-07-27",
                "section": section
            },
            "source_type": "primary", "confidence": 0.95,
            "status": "complete",
            "applicable_models": ["SIM800L"],
            "notes": "curated from datasheet table (layout hides from regex)",
            "tags": ["pin"], "created_at": NOW, "updated_at": NOW
        })
    return out

def dedup_by_name(records):
    seen, out = set(), []
    for r in records:
        key = r["name"].upper()
        if key in seen: continue
        seen.add(key)
        out.append(r)
    return out

def main():
    print("== dat_07 dedicated pin extractor ==")
    hw1, hw2 = find_hw()
    all_pins = []

    if hw2:
        body = find_pin_body(hw2, "V2.02")
        if body:
            v202 = extract_from_body(body, "V2.02")
            print(f"  [DBG] V2.02 regex hits: {len(v202)}")
            all_pins.extend(v202)

    if hw1:
        body = find_pin_body(hw1, "V1.00")
        if body:
            v100 = extract_from_body(body, "V1.00")
            print(f"  [DBG] V1.00 regex hits: {len(v100)}")
            all_pins.extend(v100)

    # Curated fill (guaranteed coverage for two-column-lost pins)
    all_pins.extend(manual_pins("V1.00"))

    # Dedup keeps first (so V2.02 wins over V1.00, V1.00 wins over curated)
    all_pins = dedup_by_name(all_pins)
    print(f"  [DBG] Total unique pins: {len(all_pins)}")

    p = DATA / "dat_07_hardware_reference.yaml"
    for i, r in enumerate(all_pins, 1):
        r["id"] = f"dat_07_{i:04d}"
    p.write_text(yaml.safe_dump({"records": all_pins}, allow_unicode=True, sort_keys=False, width=200),
                 encoding="utf-8")
    print(f"  [OK] Wrote {len(all_pins)} pins -> {p.name}")

if __name__ == "__main__":
    main()