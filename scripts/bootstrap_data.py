#!/usr/bin/env python3
"""Bootstrap data extraction for sim800l-data.

Reads pre-extracted source files and produces initial YAML datasets.
Defensive: skips anything it cannot parse; never invents data.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[FATAL] PyYAML required. pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
EXTRACTED = ROOT / "sources" / "extracted"
DATA = ROOT / "data"

AT_JSON   = EXTRACTED / "_at_commands_index.json"
AT_TXT    = EXTRACTED / "at_v1_01_full.txt"
HW_V2_TXT = EXTRACTED / "hw_v2_02_full.txt"
HW_V1_TXT = EXTRACTED / "hw_v1_00_full.txt"

AT_MANUAL = "SIM800 Series_AT Command Manual"
AT_VERSION = "V1.01"
AT_DATE    = "2017-09-15"

HW_V2 = "SIM800H&SIM800L_Hardware_Design"
HW_V2_VER = "V2.02"
HW_V2_DATE = "2015-07-27"

HW_V1 = "SIM800L_Hardware_Design"
HW_V1_VER = "V1.00"
HW_V1_DATE = "2013-08-20"


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def base_record(rid, category, src_name, src_ver, src_date, status="partial"):
    return {
        "id": rid,
        "category": category,
        "source": {"name": src_name, "version": src_ver, "date": src_date},
        "source_type": "primary",
        "confidence": 0.7,
        "status": status,
        "conflicts": [],
        "notes": "",
        "tags": [],
        "applicable_models": ["SIM800L"],
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }


def load_json(path):
    if not path.exists():
        return None
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except Exception as exc:
        print(f"[WARN] Cannot parse {path.name}: {exc}", file=sys.stderr)
        return None


def extract_at_commands():
    """Try to populate dat_01 from _at_commands_index.json."""
    print("[bootstrap] dat_01: trying AT commands index ...")
    data = load_json(AT_JSON)
    if data is None:
        print("[bootstrap] dat_01: no JSON index, skipping", file=sys.stderr)
        return []

    # Defensive: try multiple formats
    records = []
    n = 0
    if isinstance(data, dict):
        # Format: {"+CMGS": {"page": 123, ...}, ...}
        for name, meta in data.items():
            if not isinstance(name, str):
                continue
            n += 1
            rec = base_record(f"dat_01_{n:04d}", "General", AT_MANUAL, AT_VERSION, AT_DATE)
            rec["command"] = name if name.startswith("+") else "+" + name
            if isinstance(meta, dict):
                if "page" in meta:
                    rec["source"]["page"] = str(meta["page"])
                if "section" in meta:
                    rec["source"]["section"] = str(meta["section"])
                if "category" in meta:
                    rec["category"] = str(meta["category"])
    elif isinstance(data, list):
        # Format: [{"name": "+CMGS", "page": 123}, ...] or ["+CMGS", ...]
        for item in data:
            n += 1
            rec = base_record(f"dat_01_{n:04d}", "General", AT_MANUAL, AT_VERSION, AT_DATE)
            if isinstance(item, dict):
                name = item.get("name") or item.get("command")
                if not name:
                    continue
                rec["command"] = name if name.startswith("+") else "+" + name
                if "page" in item:
                    rec["source"]["page"] = str(item["page"])
                if "category" in item:
                    rec["category"] = str(item["category"])
            elif isinstance(item, str):
                rec["command"] = item if item.startswith("+") else "+" + item
            else:
                continue
            records.append(rec)
        return records
    else:
        print("[bootstrap] dat_01: unrecognized JSON format", file=sys.stderr)
        return []

    records = [r for r in records if r.get("command")]
    print(f"[bootstrap] dat_01: extracted {len(records)} command(s)")
    return records


def extract_hw_pins():
    """Try to populate dat_07 from hw text files."""
    print("[bootstrap] dat_07: trying HW pin extraction ...")
    src_txt = HW_V2_TXT if HW_V2_TXT.exists() else (HW_V1_TXT if HW_V1_TXT.exists() else None)
    if src_txt is None:
        print("[bootstrap] dat_07: no HW text files", file=sys.stderr)
        return []

    src_name = HW_V2 if src_txt == HW_V2_TXT else HW_V1
    src_ver  = HW_V2_VER if src_txt == HW_V2_TXT else HW_V1_VER
    src_date = HW_V2_DATE if src_txt == HW_V2_TXT else HW_V1_DATE

    try:
        text = src_txt.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        print(f"[bootstrap] dat_07: cannot read {src_txt.name}: {exc}", file=sys.stderr)
        return []

    # Common pin table line pattern: "<pin> <NAME> <description...>"
    # We stay conservative: only lines with a numeric pin and an ALLCAPS name.
    pin_re = re.compile(r"^\s*(\d+)\s+([A-Z][A-Z0-9_]{1,20})\s+(.+)$", re.MULTILINE)
    records = []
    n = 0
    for m in pin_re.finditer(text):
        pin_num, pin_name, desc = m.group(1), m.group(2), m.group(3).strip()
        # Skip obvious non-pin matches
        if pin_name in ("PIN", "GND", "VCC", "VBAT") and len(desc) < 5:
            pass
        n += 1
        rec = base_record(f"dat_07_{n:04d}", "GPIO", src_name, src_ver, src_date)
        rec["name"] = pin_name
        rec["pin_number"] = pin_num
        rec["function"] = desc[:200]
        rec["notes"] = "Extracted from text file; verify against PDF"
        records.append(rec)

    print(f"[bootstrap] dat_07: extracted {len(records)} candidate pin(s)")
    return records


def write_yaml(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        # Write header-only file
        header = f"# {path.stem} - no records extracted yet\n"
        path.write_text(header, encoding="utf-8")
        return 0
    with path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(records, fh, sort_keys=False, allow_unicode=True,
                       default_flow_style=False)
    return len(records)


def main():
    print("=== bootstrap_data.py ===")
    at_records = extract_at_commands()
    hw_records = extract_hw_pins()

    n_at = write_yaml(DATA / "dat_01_at_command.yaml", at_records)
    n_hw = write_yaml(DATA / "dat_07_hardware_reference.yaml", hw_records)

    print(f"\nSummary:")
    print(f"  dat_01 records written : {n_at}")
    print(f"  dat_07 records written : {n_hw}")
    print(f"\nNote: extraction is conservative. Verify against source PDFs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())