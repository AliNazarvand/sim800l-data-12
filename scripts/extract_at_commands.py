#!/usr/bin/env python3
"""
extract_at_commands.py
استخراج AT Commandهای واقعی از متن SIM800 Series AT Command Manual V1.01
و تولید data/dat_01_at_command.yaml مطابق schema.
منبع: sources/extracted/SIM800 Series_AT Command Manual_V1.01.txt
"""
import re, sys, json
from pathlib import Path
from datetime import datetime, timezone
import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "extracted" / "SIM800 Series_AT Command Manual_V1.01.txt"
OUT = ROOT / "data" / "dat_01_at_command.yaml"
IDX = ROOT / "sources" / "extracted" / "_at_commands_index.json"

if not SRC.exists():
    print(f"ERROR: {SRC} not found", file=sys.stderr)
    sys.exit(1)

text = SRC.read_text(encoding="utf-8", errors="ignore")

# نگاشت category بر اساس پیشوند command
CATEGORY_MAP = {
    "C": "General", "I": "General", "E": "General", "L": "General", "M": "General",
    "G": "Network", "A": "Network", "S": "Network", "R": "Network", "O": "Network",
    "H": "Network", "T": "Network", "V": "Network", "W": "Network", "X": "Network",
    "D": "Network", "N": "Network", "P": "Network", "K": "Network", "Q": "Network",
    "B": "Network",
}
PREFIX_CATEGORY = {
    "CS": "SMS", "CM": "SMS", "CN": "SMS", "CP": "SIM",
    "CG": "GPRS", "CI": "GPRS", "CD": "GPRS",
    "CL": "Call", "CR": "Call", "CC": "Call", "CH": "Call",
    "IP": "TCP/IP", "HT": "HTTP", "FT": "FTP", "SS": "SSL", "AT": "General",
    "SI": "SIM", "DI": "GPIO", "PO": "Power", "SL": "Sleep", "TI": "Time",
}

def classify(cmd):
    c = cmd.upper()
    for pre in ("CSMS", "CMGF", "CMGS", "CMGR", "CMGL", "CMGD", "CMGW", "CNMI", "CPMS", "CSCA", "CSCS", "CSMP", "CSDH", "CMEE"):
        if c.startswith(pre): return "SMS"
    for pre in ("CIP", "CSTT", "CIICR", "CIFSR", "CGDCONT", "CGATT", "CGACT", "CGPADDR", "CDNSGIP", "CGCONTRDP"):
        if c.startswith(pre): return "GPRS"
    for pre in ("HTTP",): 
        if c.startswith(pre): return "HTTP"
    for pre in ("FTP",):
        if c.startswith(pre): return "FTP"
    for pre in ("SSL",):
        if c.startswith(pre): return "SSL"
    for pre in ("CPIN", "CLCK", "CPWD", "CSIM", "CRSM", "CIMI", "CCID", "CSMINS", "CSPN", "CUSD"):
        if c.startswith(pre): return "SIM"
    for pre in ("CLVL", "CMUT", "CRSL", "CHFA", "CCFC", "COLP", "CLIP", "CLIR", "CRC", "CALM", "CRTD", "CRTT"):
        if c.startswith(pre): return "Audio" if c.startswith(("CLVL","CMUT","CRSL")) else "Call"
    for pre in ("CGSN", "CGMM", "CGMR", "CGMI", "GMI", "GMM", "GMR"):
        if c.startswith(pre): return "General"
    for pre in ("CSQ", "CREG", "CGREG", "CEREG", "COPS", "CPOL"):
        if c.startswith(pre): return "Network"
    if c.startswith("CFUN"): return "Power"
    if c.startswith("CSCLK"): return "Sleep"
    if c.startswith("CCLK"): return "Time"
    if c.startswith("GPIO"): return "GPIO"
    if c.startswith("CFS"): return "Firmware"
    return "General"

# الگوی commandها: AT+XXXX یا +XXXX در متن
cmd_re = re.compile(r'(?<![A-Z0-9])(?:\bAT)?\+([A-Z][A-Z0-9]{1,15})\b')
found = cmd_re.findall(text)

# فیلتر نویزهای رایج (شماره تلفن، پارامتر عددی، ...)
noise = {"CSQ", "CGREG", "CREG", "CMEE"}  # نمونه — همه نگه داشته می‌شوند
valid = []
for c in found:
    if len(c) < 2 or len(c) > 15: continue
    if c.isdigit(): continue
    valid.append(c)

# یکتا با حفظ ترتیب ظهور
seen = set()
unique_cmds = []
for c in valid:
    if c not in seen:
        seen.add(c)
        unique_cmds.append(c)

print(f"Total AT command tokens found: {len(unique_cmds)}")

now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
records = []
index = {}
for i, cmd in enumerate(unique_cmds, start=1):
    rid = f"dat_01_{i:04d}"
    # پیدا کردن اولین بافت پیرامون command
    # جستجو در متن اصلی با الگوی AT+CMD یا +CMD
    m = re.search(r'(?<![A-Z0-9])(?:AT)?\+' + re.escape(cmd) + r'\b', text)
    ctx = ""
    page = ""
    if m:
        s = max(0, m.start() - 300)
        e = min(len(text), m.end() + 600)
        ctx = text[s:e].replace("\r", " ").replace("\n", " ")
        ctx = re.sub(r"\s+", " ", ctx).strip()
        # تلاش برای یافتن شماره صفحه نزدیک
        page_match = re.search(r'(?:Page|page|صفحه)\s*[:：]?\s*(\d+)', text[max(0,m.start()-1500):m.start()])
        if page_match: page = page_match.group(1)

    cat = classify(cmd)
    records.append({
        "id": rid,
        "category": cat,
        "command": f"+{cmd}",
        "mode": "exec",
        "syntax": f"AT+{cmd}",
        "parameters": [],
        "response_success": "OK",
        "response_error": "ERROR",
        "examples": [f"AT+{cmd}"],
        "related_urcs": [],
        "related_states": [],
        "related_commands": [],
        "firmware_min": "unknown",
        "firmware_max": "unknown",
        "source": {
            "name": "SIM800 Series AT Command Manual",
            "version": "V1.01",
            "date": "unknown",
            "page": page or "auto",
            "section": "auto-extracted",
            "quote": ctx[:400]
        },
        "source_type": "primary",
        "confidence": 0.6,
        "status": "partial",
        "conflicts": [],
        "notes": "Auto-extracted from AT Manual V1.01. Needs human verification of syntax/parameters.",
        "applicable_models": ["SIM800L"],
        "tags": ["at-command", "auto-extracted", cat.lower()],
        "created_at": now,
        "updated_at": now
    })
    index[cmd] = rid

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, width=200, default_flow_style=False)

IDX.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {len(records)} records to {OUT.name}")
print(f"Index written to {IDX.name}")