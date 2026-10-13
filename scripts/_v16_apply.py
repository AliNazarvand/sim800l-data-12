#!/usr/bin/env python3
"""v16 data corrections for sim800l-data.

Fixes:
  1. dat_02: move AT-commands-mislabeled-as-URCs to dat_01.
  2. dat_07: add missing pins from V2.02 Table 5.
  3. audit_data_integrity.py: fix expected pin count.

Usage:
  python scripts/_v16_apply.py           # apply fixes
  python scripts/_v16_apply.py --dry-run # show what would be done
"""
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[FATAL] PyYAML required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SCRIPTS = ROOT / "scripts"

DAT_01 = DATA / "dat_01_at_command.yaml"
DAT_02 = DATA / "dat_02_urc.yaml"
DAT_07 = DATA / "dat_07_hardware_reference.yaml"


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_yaml(path):
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    return data if isinstance(data, list) else []


def save_yaml(path, records):
    with path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(records, fh, sort_keys=False,
                       allow_unicode=True, default_flow_style=False)


# ----------------------------------------------------------------------------
# Detection: is this dat_02 record actually an AT command?
# ----------------------------------------------------------------------------
def is_at_command_record(rec):
    """True if the record represents an AT command, not a URC.

    Strong signal: `related_command` field is "AT+" + urc_string
    (case-insensitive, ignoring leading '+'). This is the pattern
    produced when a record was auto-generated from an AT command
    section of the manual, not from the URC section.

    Real URCs have either empty related_command or reference their
    *enabling* command (e.g., +CMTI references +CNMI).
    """
    urc = str(rec.get("urc_string", "")).strip().lstrip("+").upper()
    related = str(rec.get("related_command", "")).strip().upper()

    if not urc or not related:
        return False

    # Case: related_command == "AT+" + urc (e.g., urc="CAAS", related="AT+CAAS")
    if related.startswith("AT+"):
        tail = related[3:].strip()
        if tail == urc:
            return True

    return False


# ----------------------------------------------------------------------------
# Fix #1: dat_02 cleanup
# ----------------------------------------------------------------------------
def fix_dat_02(dry_run=False):
    print("\n=== Fix #1: dat_02 cleanup (move AT commands to dat_01) ===")
    dat_02 = load_yaml(DAT_02)
    dat_01 = load_yaml(DAT_01)
    if not dat_02:
        print("  [SKIP] dat_02 is empty")
        return

    print(f"  dat_02 records before: {len(dat_02)}")
    print(f"  dat_01 records before: {len(dat_01)}")

    # Find max existing dat_01 id to avoid collisions
    max_id_01 = 0
    for r in dat_01:
        if isinstance(r, dict):
            m = re.match(r"dat_01_(\d+)$", str(r.get("id", "")))
            if m:
                max_id_01 = max(max_id_01, int(m.group(1)))

    new_dat_02 = []
    moved = 0
    kept = 0

    for rec in dat_02:
        if not isinstance(rec, dict):
            continue

        if is_at_command_record(rec):
            # Move to dat_01 as an AT command
            moved += 1
            cmd = str(rec.get("urc_string", "")).strip()
            if not cmd.startswith("+"):
                cmd = "+" + cmd

            max_id_01 += 1
            new_rec = {
                "id": f"dat_01_{max_id_01:04d}",
                "category": rec.get("category", "General"),
                "command": cmd,
                "mode": "write",
                "syntax": "",
                "parameters": rec.get("parameters", []),
                "response_success": "",
                "response_error": "",
                "examples": rec.get("examples", []),
                "related_urcs": [],
                "related_states": [],
                "related_commands": [],
                "firmware_min": "unknown",
                "firmware_max": "unknown",
                "source": rec.get("source", {}),
                "source_type": rec.get("source_type", "primary"),
                "confidence": rec.get("confidence", 0.6),
                "status": "partial",
                "conflicts": [],
                "notes": f"Moved from dat_02 ({rec.get('id')}) during v16 cleanup.",
                "tags": ["moved-from-dat02"],
                "applicable_models": ["SIM800L"],
                "created_at": rec.get("created_at", now_iso()),
                "updated_at": now_iso(),
            }
            dat_01.append(new_rec)
        else:
            # Keep as URC; clean up the "suspected" note
            kept += 1
            notes = str(rec.get("notes", ""))
            cleaned = re.sub(r"(?i)suspected[^.]*\.\s*", "", notes).strip()
            rec["notes"] = cleaned
            rec["updated_at"] = now_iso()
            new_dat_02.append(rec)

    print(f"  Moved to dat_01: {moved}")
    print(f"  Kept as URCs:    {kept}")
    print(f"  dat_02 records after: {len(new_dat_02)}")
    print(f"  dat_01 records after: {len(dat_01)}")

    if not dry_run:
        save_yaml(DAT_01, dat_01)
        save_yaml(DAT_02, new_dat_02)
        print("  [SAVED] dat_01 and dat_02 updated")
    else:
        print("  [DRY-RUN] no files written")


# ----------------------------------------------------------------------------
# Fix #2: dat_07 completion from Table 5 of V2.02
# ----------------------------------------------------------------------------
# Complete list of unique pin names for SIM800L from hw_v2_02_full.txt
# (58 pins; BT_ANT is excluded because it is SIM800H-only)
FULL_PINS_V202 = [
    # Power supply
    ("VBAT",     "1, 42",       "power",  "Main power supply (3.4V to 4.4V)", "Power"),
    ("VRTC",     "56",          "I/O",    "Power supply for RTC backup", "Power"),
    ("VDD_EXT",  "18",          "output", "2.8V power output", "Power"),
    ("GND",      "2, 6, 8, 35, 37-39, 41, 43-45, 58, 67, 71-73, 76-88", "ground", "Ground (multiple pins)", "Ground"),
    # Power on/off
    ("PWRKEY",   "48",          "input",  "Power on/off control (pull low >= 1s)", "PWRKEY"),
    # Audio
    ("MIC1P",    "52",          "input",  "Main audio input positive", "Audio"),
    ("MIC1N",    "12",          "input",  "Main audio input negative", "Audio"),
    ("SPK1P",    "53",          "output", "Main audio output positive", "Audio"),
    ("SPK1N",    "13",          "output", "Main audio output negative", "Audio"),
    ("MIC2P",    "9",           "input",  "Secondary audio input positive", "Audio"),
    ("MIC2N",    "10",          "input",  "Secondary audio input negative", "Audio"),
    ("SPK2P",    "51",          "output", "Secondary audio output positive", "Audio"),
    ("SPK2N",    "11",          "output", "Secondary audio output negative", "Audio"),
    # PCM
    ("PCM_CLK",  "29",          "output", "PCM clock", "Audio"),
    ("PCM_OUT",  "30",          "output", "PCM data output", "Audio"),
    ("PCM_SYNC", "65",          "output", "PCM sync", "Audio"),
    ("PCM_IN",   "66",          "input",  "PCM data input", "Audio"),
    # Keypad
    ("KBC4",     "24",          "input",  "Keypad matrix column 4", "GPIO"),
    ("KBC3",     "21",          "input",  "Keypad matrix column 3", "GPIO"),
    ("KBC2",     "22",          "input",  "Keypad matrix column 2", "GPIO"),
    ("KBC1",     "25",          "input",  "Keypad matrix column 1", "GPIO"),
    ("KBC0",     "20",          "input",  "Keypad matrix column 0 (must be HIGH at power-on)", "GPIO"),
    ("KBR4",     "63",          "output", "Keypad matrix row 4", "GPIO"),
    ("KBR3",     "23",          "output", "Keypad matrix row 3", "GPIO"),
    ("KBR2",     "61",          "output", "Keypad matrix row 2", "GPIO"),
    ("KBR1",     "60",          "output", "Keypad matrix row 1", "GPIO"),
    ("KBR0",     "62",          "output", "Keypad matrix row 0", "GPIO"),
    # GPIO / indicators
    ("GPIO1",    "3",           "I/O",    "Programmable GPIO", "GPIO"),
    ("GPIO2",    "27",          "I/O",    "Programmable GPIO", "GPIO"),
    ("GPIO3",    "28",          "I/O",    "Programmable GPIO", "GPIO"),
    ("NETLIGHT", "64",          "output", "Network status indication LED", "NETLIGHT"),
    ("STATUS",   "4",           "output", "Power on status indication", "STATUS"),
    # Serial port
    ("DTR",      "69",          "input",  "Data terminal ready", "UART"),
    ("RI",       "68",          "output", "Ring indicator", "UART"),
    ("DCD",      "70",          "output", "Data carrier detect", "UART"),
    ("CTS",      "34",          "output", "Clear to send (flow control)", "UART"),
    ("RTS",      "33",          "input",  "Request to send (flow control)", "UART"),
    ("TXD",      "32",          "output", "Transmit data", "UART"),
    ("RXD",      "31",          "input",  "Receive data", "UART"),
    # USB
    ("VBUS",     "7",           "input",  "USB power supply (4.3-7.0V)", "USB"),
    ("USB_DP",   "59",          "I/O",    "USB data positive (D+)", "USB"),
    ("USB_DN",   "19",          "I/O",    "USB data negative (D-)", "USB"),
    # ADC
    ("ADC",      "50",          "input",  "10-bit general ADC input", "ADC"),
    # PWM
    ("PWM",      "26",          "output", "Pulse width modulation output", "PWM"),
    # I2C
    ("SDA",      "75",          "I/O",    "I2C serial data (open drain)", "GPIO"),
    ("SCL",      "74",          "output", "I2C serial clock (open drain)", "GPIO"),
    # SIM card interface
    ("SIM_VDD",  "16",          "output", "SIM card power supply (1.8V or 3V)", "SIM"),
    ("SIM_DATA", "14",          "I/O",    "SIM card data I/O", "SIM"),
    ("SIM_CLK",  "55",          "output", "SIM card clock", "SIM"),
    ("SIM_RST",  "15",          "output", "SIM card reset", "SIM"),
    ("SIM_DET",  "54",          "input",  "SIM card detection", "SIM"),
    # Antenna
    ("GSM_ANT",  "40",          "I/O",    "GSM antenna (50 ohm)", "Antenna"),
    ("FM_ANTP",  "17",          "input",  "FM antenna positive", "Antenna"),
    ("FM_ANTN",  "57",          "input",  "FM antenna negative", "Antenna"),
    # RF
    ("RF_SYNC",  "5",           "output", "RF transmit synchronization signal", "RF"),
    # Other
    ("RESET",    "49",          "input",  "Module reset (active low)", "Reset"),
    ("ISINK1",   "46",          "input",  "Keypad backlight sink current", "GPIO"),
    ("ISINK0",   "47",          "input",  "LCD backlight sink current", "GPIO"),
]


def fix_dat_07(dry_run=False):
    print("\n=== Fix #2: dat_07 completion from V2.02 Table 5 ===")
    dat_07 = load_yaml(DAT_07)
    if not dat_07:
        print("  [SKIP] dat_07 is empty")
        return

    print(f"  dat_07 records before: {len(dat_07)}")
    existing_names = {
        str(r.get("name", "")).strip().upper()
        for r in dat_07 if isinstance(r, dict)
    }
    print(f"  Existing unique pin names: {len(existing_names)}")

    # Find max existing id to avoid collisions
    max_id = 0
    for r in dat_07:
        if isinstance(r, dict):
            m = re.match(r"dat_07_(\d+)$", str(r.get("id", "")))
            if m:
                max_id = max(max_id, int(m.group(1)))

    added = 0
    for (name, pin_num, direction, function, category) in FULL_PINS_V202:
        if name.upper() in existing_names:
            continue
        max_id += 1
        new_rec = {
            "id": f"dat_07_{max_id:04d}",
            "category": category,
            "name": name,
            "pin_number": pin_num,
            "direction": direction,
            "function": function,
            "source": {
                "name": "SIM800H&SIM800L_Hardware_Design",
                "version": "V2.02",
                "date": "2015-07-27",
                "page": "16",
                "section": "Table 5: Pin Description",
                "quote": "",
            },
            "source_type": "primary",
            "confidence": 0.95,
            "status": "partial",
            "conflicts": [],
            "notes": "Added by v16 from V2.02 Table 5.",
            "tags": ["pin", "hardware"],
            "applicable_models": ["SIM800L"],
            "created_at": now_iso(),
            "updated_at": now_iso(),
        }
        dat_07.append(new_rec)
        added += 1

    print(f"  Added: {added} pins")
    print(f"  dat_07 records after: {len(dat_07)}")

    if not dry_run:
        save_yaml(DAT_07, dat_07)
        print("  [SAVED] dat_07 updated")
    else:
        print("  [DRY-RUN] no files written")


# ----------------------------------------------------------------------------
# Fix #3: audit_data_integrity.py expected count
# ----------------------------------------------------------------------------
def fix_audit_script():
    print("\n=== Fix #3: audit_data_integrity.py expected count ===")
    audit = SCRIPTS / "audit_data_integrity.py"
    if not audit.exists():
        print("  [SKIP] audit_data_integrity.py not found")
        return

    content = audit.read_text(encoding="utf-8")
    # The bug: expected_approx = 88 (physical pads, not unique pin names)
    # The fix: expected 58 (unique names for SIM800L)
    if 'expected_approx = 88' in content:
        content = content.replace(
            'expected_approx = 88',
            'expected_approx = 58  # unique pin names for SIM800L (excludes BT_ANT)'
        )
        audit.write_text(content, encoding="utf-8")
        print("  [FIXED] changed expected_approx from 88 to 58")
    elif 'expected_approx = 58' in content:
        print("  [SKIP] already fixed")
    else:
        print("  [WARN] marker string not found; manual review recommended")


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    dry_run = "--dry-run" in sys.argv
    print(f"=== v16 apply (dry_run={dry_run}) ===")
    print(f"ROOT: {ROOT}")

    fix_dat_02(dry_run=dry_run)
    fix_dat_07(dry_run=dry_run)
    fix_audit_script()

    print("\n=== v16 done ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())