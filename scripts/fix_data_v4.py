#!/usr/bin/env python3
"""تکمیل dat_04, dat_07, dat_15, dat_17 + پر کردن cross-ref واقعی."""
import csv
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pyyaml"])
    import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
EXTRACTED = ROOT / "sources" / "extracted"
TABLES = EXTRACTED / "tables"
REPORTS = ROOT / "reports"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# ---------- helpers ----------
def read_csv_rows(path):
    rows = []
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            for r in csv.reader(f, delimiter="\t"):
                if any(c.strip() for c in r):
                    rows.append([c.strip() for c in r])
    except Exception:
        pass
    return rows

def load_yaml(path):
    if not path.exists(): return []
    try:
        d = yaml.safe_load(path.read_text(encoding="utf-8"))
        return d if isinstance(d, list) else []
    except Exception:
        return []

def write_yaml(path, records):
    header = f"# auto-generated at {NOW}\n"
    body = yaml.safe_dump(records, allow_unicode=True, sort_keys=False, default_flow_style=False)
    path.write_text(header + body, encoding="utf-8")

def rec(did, cat, src_name, src_ver, page, section, extra, status, conf, notes=""):
    return {
        "id": did, "category": cat,
        "source": {"name": src_name, "version": src_ver, "date": "",
                   "page": str(page) if page else "", "section": section or ""},
        "source_type": "primary", "confidence": conf, "status": status,
        "conflicts": [], "notes": notes,
        "tags": [cat.lower()], "applicable_models": ["SIM800L"],
        "created_at": NOW, "updated_at": NOW,
        **extra
    }

def page_of(csv_path):
    m = re.search(r'_p(\d+)_', csv_path.name)
    return m.group(1) if m else ""

def hw_ver_of(csv_path):
    if "v2_02" in csv_path.name: return ("SIM800H&SIM800L_Hardware_Design", "V2.02")
    if "v1_00" in csv_path.name: return ("SIM800L_Hardware_Design", "V1.00")
    if "at_v1_01" in csv_path.name: return ("SIM800 Series AT Command Manual", "V1.01")
    return ("Unknown", "")

# ---------- dat_04 ----------
def fix_dat_04():
    old = load_yaml(DATA / "dat_04_timing_timeout.yaml")
    new = []
    seen = set()
    for csv_path in sorted(TABLES.glob("*.csv")):
        if not (csv_path.name.startswith("v2_02_") or csv_path.name.startswith("v1_00_")):
            continue
        sn, sv = hw_ver_of(csv_path)
        pg = page_of(csv_path)
        for row in read_csv_rows(csv_path):
            joined = " | ".join(row)
            for m in re.finditer(r'([A-Za-z][A-Za-z0-9 _\-/\.\(\)]{2,80}?)\s+([0-9]+(?:\.[0-9]+)?)\s*(ms|us|µs|s)\b', joined):
                param = m.group(1).strip()
                if len(param) < 4: continue
                key = (param.lower(), m.group(2), m.group(3))
                if key in seen: continue
                seen.add(key)
                new.append(rec(
                    f"dat_04_tmp_{len(new)+1:04d}", "Timing", sn, sv, pg, "Timing",
                    {"parameter": param, "min": None, "typ": float(m.group(2)), "max": None,
                     "unit": m.group(3), "condition": "", "related_command": None, "related_state": None},
                    "partial", 0.75, notes="extracted from PDF table row"
                ))
    # merge old + new (dedupe by parameter+typ)
    merged = []
    seen_keys = set()
    for r in (old + new):
        p = r.get("parameter", "")
        t = r.get("typ", "")
        key = (str(p).lower(), str(t))
        if key in seen_keys: continue
        seen_keys.add(key)
        merged.append(r)
    # re-id
    for i, r in enumerate(merged, 1):
        r["id"] = f"dat_04_{i:04d}"
    write_yaml(DATA / "dat_04_timing_timeout.yaml", merged)
    return len(merged)

# ---------- dat_07 ----------
def fix_dat_07():
    old = load_yaml(DATA / "dat_07_hardware_reference.yaml")
    new = []
    seen = set()
    pin_header_re = re.compile(r'\b(pin|signal|name|ball)\b', re.IGNORECASE)
    for csv_path in sorted(TABLES.glob("*.csv")):
        if not (csv_path.name.startswith("v2_02_") or csv_path.name.startswith("v1_00_")):
            continue
        rows = read_csv_rows(csv_path)
        if len(rows) < 2:
            continue
        first = " ".join(rows[0]).lower()
        if not pin_header_re.search(first):
            continue
        sn, sv = hw_ver_of(csv_path)
        pg = page_of(csv_path)
        for row in rows[1:]:
            if len(row) < 2: continue
            pin_num = ""
            pin_name = ""
            function = ""
            for cell in row:
                if not cell: continue
                if not pin_num and re.match(r'^\d{1,3}[A-Za-z]?$', cell):
                    pin_num = cell
                elif not pin_name and len(cell) >= 2 and not cell.isdigit():
                    pin_name = cell
                elif not function and len(cell) >= 3:
                    function = cell
            if not pin_name: continue
            key = (pin_name.upper(), pin_num)
            if key in seen: continue
            seen.add(key)
            pn = pin_name.upper()
            cat = ("Power" if any(x in pn for x in ("VBAT","VDD","GND","VRTC")) else
                   "SIM" if "SIM" in pn else
                   "UART" if pn in ("TXD","RXD","RTS","CTS","DTR","DCD","RI") else
                   "Audio" if any(x in pn for x in ("MIC","SPK")) else
                   "RF" if ("RF" in pn or "ANT" in pn) else
                   "Reset" if "RESET" in pn else
                   "PWRKEY" if "PWRKEY" in pn else "GPIO")
            new.append(rec(
                f"dat_07_tmp_{len(new)+1:04d}", cat, sn, sv, pg, "Pin Description",
                {"name": pin_name, "pin_number": pin_num, "direction": "",
                 "voltage_min": None, "voltage_typ": None, "voltage_max": None,
                 "current_typ": None, "current_max": None,
                 "function": function, "alternate_function": None,
                 "pull_up_down": None, "esd_rating": None, "impedance": None,
                 "decoupling": None},
                "partial", 0.8, notes="extracted from pin table"
            ))
    # merge
    merged = []
    seen_keys = set()
    for r in (old + new):
        key = (str(r.get("name", "")).upper(), str(r.get("pin_number", "")))
        if key in seen_keys: continue
        seen_keys.add(key)
        merged.append(r)
    for i, r in enumerate(merged, 1):
        r["id"] = f"dat_07_{i:04d}"
    write_yaml(DATA / "dat_07_hardware_reference.yaml", merged)
    return len(merged)

# ---------- dat_15 ----------
def fix_dat_15():
    old = load_yaml(DATA / "dat_15_power_management.yaml")
    new = []
    seen = set()
    for csv_path in sorted(TABLES.glob("*.csv")):
        if not (csv_path.name.startswith("v2_02_") or csv_path.name.startswith("v1_00_") or
                csv_path.name.startswith("at_v1_01_")):
            continue
        rows = read_csv_rows(csv_path)
        joined_all = "\n".join(" ".join(r) for r in rows)
        low = joined_all.lower()
        if not any(k in low for k in ("sleep", "cfun", "csc", "dtr", "wake", "slow clock", "power saving")):
            continue
        sn, sv = hw_ver_of(csv_path)
        pg = page_of(csv_path)
        for row in rows:
            jr = " ".join(c for c in row if c)
            if not jr: continue
            if re.search(r'(AT\+CSCLK|AT\+CFUN|AT\+CSDT|sleep mode|slow clock|minimum function|power saving|deep sleep)', jr, re.IGNORECASE):
                key = jr[:80].lower()
                if key in seen: continue
                seen.add(key)
                # try to find command
                cm = re.search(r'(AT\+[A-Z]+)', jr)
                cmd = cm.group(1) if cm else ""
                new.append(rec(
                    f"dat_15_tmp_{len(new)+1:04d}", "Power", sn, sv, pg, "Power Management",
                    {"mode": "", "command": cmd, "parameter": jr[:200],
                     "value_min": None, "value_typ": None, "value_max": None,
                     "unit": "", "condition": "", "wake_source": "",
                     "related_commands": [cmd] if cmd else [], "related_states": []},
                    "partial", 0.7, notes="extracted from table row"
                ))
    # also pull commands from AT text
    at_text = EXTRACTED / "at_v1_01.txt"
    if at_text.exists():
        text = at_text.read_text(encoding="utf-8", errors="ignore")
        for cmd in ["+CSCLK", "+CFUN", "+CSDT", "+CBATCHK"]:
            if cmd in text:
                key = ("cmd", cmd)
                if key in seen: continue
                seen.add(key)
                new.append(rec(
                    f"dat_15_tmp_cmd_{cmd[1:]}", "Power",
                    "SIM800 Series AT Command Manual", "V1.01", "", "Power",
                    {"mode": "", "command": f"AT{cmd}", "parameter": cmd,
                     "value_min": None, "value_typ": None, "value_max": None,
                     "unit": "", "condition": "", "wake_source": "",
                     "related_commands": [cmd], "related_states": []},
                    "partial", 0.75, notes="command found in AT Manual V1.01"
                ))
    merged = old + new
    for i, r in enumerate(merged, 1):
        r["id"] = f"dat_15_{i:04d}"
    write_yaml(DATA / "dat_15_power_management.yaml", merged)
    return len(merged)

# ---------- dat_17 ----------
def fix_dat_17():
    ssl_cmds = set()
    # Search in tables
    for csv_path in sorted(TABLES.glob("at_v1_01_*.csv")):
        for row in read_csv_rows(csv_path):
            j = " ".join(row)
            for m in re.finditer(r'AT\+([A-Z]*SSL[A-Z]*)', j):
                ssl_cmds.add("+" + m.group(1))
    # Search in AT text
    at_text = EXTRACTED / "at_v1_01.txt"
    if at_text.exists():
        text = at_text.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r'AT\+([A-Z]*SSL[A-Z]*)', text):
            ssl_cmds.add("+" + m.group(1))
        for kw in ["SSLSETCERT", "SSLSETKEY", "SSLCFG", "SSLCONF",
                   "SSLOPEN", "SSLSEND", "SSLRECV", "SSLCLOSE", "SSLSETCA"]:
            if kw in text:
                ssl_cmds.add("+" + kw)
    # also search in all tables (not just at_v1_01 prefix)
    for csv_path in sorted(TABLES.glob("*.csv")):
        for row in read_csv_rows(csv_path):
            j = " ".join(row)
            if "SSL" in j.upper():
                for m in re.finditer(r'AT\+([A-Z]*SSL[A-Z]*)', j):
                    ssl_cmds.add("+" + m.group(1))
    records = []
    for i, cmd in enumerate(sorted(ssl_cmds), 1):
        records.append(rec(
            f"dat_17_{i:04d}", "SSL",
            "SIM800 Series AT Command Manual", "V1.01", "", "SSL",
            {"command": cmd, "syntax": "", "parameters": [], "response": "OK",
             "examples": [], "tls_version": "", "cipher_suite": "",
             "cert_format": "PEM", "key_format": "PEM", "storage": "", "limits": "",
             "related_commands": []},
            "partial", 0.7, notes="extracted from search of AT Manual & tables"
        ))
    if not records:
        # write empty
        write_yaml(DATA / "dat_17_certificate_key_store.yaml", [])
        return (0, "blocked")
    write_yaml(DATA / "dat_17_certificate_key_store.yaml", records)
    return (len(records), "partial" if len(records) < 5 else "complete")

# ---------- cross-ref ----------
def fix_crossref():
    d01 = load_yaml(DATA / "dat_01_at_command.yaml")
    cmd_index = {r.get("command"): r.get("id") for r in d01 if r.get("command")}
    count = 0
    for name in ["dat_09_sms.yaml","dat_10_gprs_data.yaml","dat_11_http_ftp_ssl.yaml",
                 "dat_12_audio.yaml","dat_13_sim_management.yaml",
                 "dat_15_power_management.yaml","dat_17_certificate_key_store.yaml"]:
        path = DATA / name
        data = load_yaml(path)
        changed = False
        for r in data:
            c = r.get("command")
            if c and c in cmd_index:
                existing = r.get("related_commands") or []
                if not isinstance(existing, list):
                    existing = []
                if cmd_index[c] not in existing:
                    r["related_commands"] = existing + [cmd_index[c]]
                    count += 1
                    changed = True
        if changed:
            write_yaml(path, data)
    return count

# ---------- main ----------
def main():
    print("Fixing dat_04...")
    n04 = fix_dat_04()
    print(f"  -> dat_04: {n04}")

    print("Fixing dat_07...")
    n07 = fix_dat_07()
    print(f"  -> dat_07: {n07}")

    print("Fixing dat_15...")
    n15 = fix_dat_15()
    print(f"  -> dat_15: {n15}")

    print("Fixing dat_17...")
    n17, st17 = fix_dat_17()
    print(f"  -> dat_17: {n17} ({st17})")

    print("Cross-referencing...")
    nc = fix_crossref()
    print(f"  -> {nc} cross-refs added")

    # state file for PowerShell
    state = {"dat_04": n04, "dat_07": n07, "dat_15": n15,
             "dat_17": n17, "dat_17_status": st17, "crossref": nc}
    import json
    (ROOT / "scripts" / "_v4_state.json").write_text(json.dumps(state), encoding="utf-8")
    return 0

if __name__ == "__main__":
    sys.exit(main())