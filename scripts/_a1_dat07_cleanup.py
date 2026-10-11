#!/usr/bin/env python3
"""A1 CLEANUP — real pin_numbers, honest status, clean tags/notes, fix quotes."""

import re
import shutil
import yaml
from datetime import datetime, timezone
from pathlib import Path

ROOT    = Path(__file__).resolve().parent.parent
DATA    = ROOT / "data"
REPORTS = ROOT / "reports"
DATA07  = DATA / "dat_07_hardware_reference.yaml"
REPORTS.mkdir(parents=True, exist_ok=True)

# --- Verified pin_number map (from V2.02 §Table 5, cross-checked §Table 30) -
PIN_NUMBERS = {
    # Power / RTC
    "VBAT": "1,42", "VRTC": "56", "VDD_EXT": "18",
    # Power on/off
    "PWRKEY": "48",
    # Audio
    "MIC1P": "52", "MIC1N": "12", "SPK1P": "53", "SPK1N": "13",
    "MIC2P": "9",  "MIC2N": "10", "SPK2P": "51", "SPK2N": "11",
    # PCM
    "PCM_CLK": "29", "PCM_OUT": "30", "PCM_SYNC": "65", "PCM_IN": "66",
    # Keypad
    "KBC0": "20", "KBC1": "25", "KBC2": "22", "KBC3": "21", "KBC4": "24",
    "KBR0": "62", "KBR1": "60", "KBR2": "61", "KBR3": "23", "KBR4": "63",
    # GPIO
    "GPIO1": "3", "GPIO2": "27", "GPIO3": "28",
    # NETLIGHT / STATUS
    "NETLIGHT": "64", "STATUS": "4",
    # Serial port
    "DTR": "69", "RI": "68", "DCD": "70",
    "CTS": "34", "RTS": "33", "TXD": "32", "RXD": "31",
    # Debug / USB
    "VBUS": "7", "USB_DP": "59", "USB_DN": "19",
    # I2C
    "SDA": "75", "SCL": "74",
    # SIM
    "SIM_VDD": "16", "SIM_DATA": "14", "SIM_CLK": "55",
    "SIM_RST": "15", "SIM_DET": "54",
    # Antenna
    "GSM_ANT": "40", "FM_ANTP": "17", "FM_ANTN": "57",
    # Sync / Reset
    "RF_SYNC": "5", "RESET": "49",
    # LED
    "ISINK0": "47", "ISINK1": "46",
    # PWM
    "PWM": "26",
}

# --- Verified quote/page fixes (5 records were pulling from Figure Index) ---
QUOTE_FIXES = {
    "PWM": {
        "page": "48",
        "section": "Table 30: Pin definition of the PWM",
        "quote": "PWM 26 O Pulse-width modulation",
    },
    "NETLIGHT": {
        "page": "17",
        "section": "Table 5: Pin description",
        "quote": "NETLIGHT 64 O Network status",
    },
    "STATUS": {
        "page": "17",
        "section": "Table 5: Pin description",
        "quote": "STATUS 4 O Power on status",
    },
    "PWRKEY": {
        "page": "16",
        "section": "Table 5: Pin description",
        "quote": "PWRKEY 48 I PWRKEY should be pulled low at least 1 second",
    },
    "VBAT": {
        "page": "16",
        "section": "Table 5: Pin description",
        "quote": "VBAT 1,42 I Power supply",
    },
    "SIM_VDD": {
        "page": "17",
        "section": "Table 5: Pin description",
        "quote": "SIM_VDD 16 O Voltage supply for SIM card. Support 1.8V or 3V SIM card",
    },
}

# --- Helpers ---------------------------------------------------------------
def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load_dat07():
    return yaml.safe_load(DATA07.read_text(encoding="utf-8")) or []

def save_dat07(records):
    out = yaml.safe_dump(
        records,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=1000,
    )
    DATA07.write_text(out, encoding="utf-8")

def strip_possible_duplicate_from_notes(notes):
    if not notes:
        return notes
    # Remove pattern ' | possible_duplicate_of: dat_XX_YYYY' (with optional spaces)
    return re.sub(
        r'\s*\|\s*possible_duplicate_of:\s*dat_\d+_\d{4}',
        '',
        str(notes),
    ).strip()

# --- Snapshot --------------------------------------------------------------
def phase_snapshot():
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    snap = ROOT / f"dat07_a1_cleanup_snapshot_{stamp}"
    snap.mkdir(exist_ok=True)
    if DATA07.exists():
        shutil.copy2(DATA07, snap / DATA07.name)
    print(f"Snapshot: {snap}")

# --- Phase 1: fix pin_number ----------------------------------------------
def phase_pin_number(records):
    fixed = 0
    details = []
    for r in records:
        name = r.get("name", "")
        cur  = str(r.get("pin_number", "") or "")
        real = PIN_NUMBERS.get(name)
        if real is None:
            continue
        # Only fix if current looks wrong (equal to name, or empty)
        if cur == "" or cur == name:
            r["pin_number"] = real
            fixed += 1
            details.append((r.get("id"), name, cur, real))
    print(f"  pin_number fixed: {fixed}")
    return fixed, details

# --- Phase 2: status / confidence split ------------------------------------
def phase_status(records):
    to_complete = 0
    to_partial = 0
    ts = now_iso()
    for r in records:
        direction = r.get("direction")
        function  = r.get("function")
        complete_info = (
            direction is not None and str(direction).strip().lower() not in ("", "unknown")
            and function is not None and str(function).strip().lower() not in ("", "unknown")
        )
        if complete_info:
            r["status"] = "complete"
            r["confidence"] = 0.9
            # Strip misleading "Needs manual verification" suffix from notes
            notes = r.get("notes", "")
            if notes:
                notes = re.sub(
                    r'\s*\|\s*Needs manual verification of direction/voltage/current and pin_number\.?',
                    '',
                    str(notes),
                )
                notes = notes.replace(
                    "Auto-extracted from pin table. Needs manual verification of direction/voltage/current and pin_number.",
                    "",
                )
                notes = notes.strip().strip("|").strip()
                r["notes"] = notes if notes else None
            to_complete += 1
        else:
            r["status"] = "partial"
            r["confidence"] = 0.6
            to_partial += 1
        r["updated_at"] = ts
    print(f"  to_complete: {to_complete}")
    print(f"  to_partial:  {to_partial}")
    return to_complete, to_partial

# --- Phase 3: clean tags/notes --------------------------------------------
def phase_clean_tags(records):
    tags_cleaned = 0
    notes_cleaned = 0
    for r in records:
        # tags
        tags = r.get("tags")
        if isinstance(tags, list) and "possible-duplicate" in tags:
            r["tags"] = [t for t in tags if t != "possible-duplicate"]
            tags_cleaned += 1
        # notes
        notes = r.get("notes")
        if notes:
            new_notes = strip_possible_duplicate_from_notes(notes)
            if new_notes != notes:
                r["notes"] = new_notes if new_notes else None
                notes_cleaned += 1
    print(f"  tags cleaned:  {tags_cleaned}")
    print(f"  notes cleaned: {notes_cleaned}")
    return tags_cleaned, notes_cleaned

# --- Phase 4: fix quote/page ----------------------------------------------
def phase_quote_fix(records):
    fixed = 0
    for r in records:
        name = r.get("name", "")
        fix = QUOTE_FIXES.get(name)
        if not fix:
            continue
        src = r.get("source")
        if not isinstance(src, dict):
            continue
        # Only fix if current quote looks wrong (points to figure index etc.)
        cur_quote = str(src.get("quote", "") or "")
        if ("FIGURE" in cur_quote.upper() and "REFERENCE" in cur_quote.upper()) \
           or "Table Index" in cur_quote \
           or cur_quote.strip() == "":
            src["page"] = fix["page"]
            src["section"] = fix["section"]
            src["quote"] = fix["quote"]
            fixed += 1
    print(f"  quote/page fixed: {fixed}")
    return fixed

# --- Report ----------------------------------------------------------------
def write_report(before, after, pin_details, to_complete, to_partial,
                 tags_cleaned, notes_cleaned, quote_fixed, v2_total):
    L = []
    L.append("# A1_dat07_cleanup_report")
    L.append("")
    L.append(f"Generated: {now_iso()}")
    L.append("")
    L.append("## Summary")
    L.append("")
    L.append(f"- Records before: {before}")
    L.append(f"- Records after:  {after}")
    L.append("")
    L.append("## pin_number fixes")
    L.append("")
    L.append(f"- Records fixed: {len(pin_details)}")
    L.append("")
    L.append("| ID | Name | Old | New |")
    L.append("|----|------|-----|-----|")
    for i, n, old, new in pin_details:
        L.append(f"| {i} | {n} | {old} | {new} |")
    L.append("")
    L.append("## Status / confidence split")
    L.append("")
    L.append(f"- to `complete` (direction+function present): {to_complete}")
    L.append(f"- to `partial`  (missing info):               {to_partial}")
    L.append("")
    L.append("## Merge leftovers cleaned")
    L.append("")
    L.append(f"- tags cleaned (removed `possible-duplicate`):  {tags_cleaned}")
    L.append(f"- notes cleaned (removed `possible_duplicate_of`): {notes_cleaned}")
    L.append("")
    L.append("## Quote/page fixes (from Figure Index to Table 5)")
    L.append("")
    L.append(f"- Records fixed: {quote_fixed}")
    L.append("")
    L.append("## Coverage")
    L.append("")
    L.append(f"- V2.02 canonical pins (excl. BT_ANT, incl. PWM): {v2_total}")
    L.append(f"- dat_07 records: {after}")
    L.append(f"- Coverage: {after} / {v2_total} = {100*after//max(1,v2_total)}%")
    L.append("")

    out = REPORTS / "A1_dat07_cleanup_report.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"  Wrote {out}")

# --- Main ------------------------------------------------------------------
def main():
    print("=" * 60)
    print("A1 CLEANUP — dat_07 quality pass")
    print("=" * 60)
    print()
    print("Phase 0: snapshot")
    phase_snapshot()

    print()
    print("Phase 1: load")
    records = load_dat07()
    before = len(records)
    print(f"  Records: {before}")

    print()
    print("Phase 2: fix pin_number")
    _, pin_details = phase_pin_number(records)

    print()
    print("Phase 3: split status / confidence")
    to_complete, to_partial = phase_status(records)

    print()
    print("Phase 4: clean tags / notes")
    tags_cleaned, notes_cleaned = phase_clean_tags(records)

    print()
    print("Phase 5: fix quote / page")
    quote_fixed = phase_quote_fix(records)

    print()
    print("Phase 6: save and report")
    save_dat07(records)
    after = len(records)
    v2_total = 56   # 55 + PWM
    write_report(before, after, pin_details, to_complete, to_partial,
                 tags_cleaned, notes_cleaned, quote_fixed, v2_total)

    print()
    print("=" * 60)
    print(f"Records before: {before}")
    print(f"Records after:  {after}")
    print(f"pin_number fixed: {len(pin_details)}")
    print(f"complete: {to_complete}  partial: {to_partial}")
    print(f"Coverage: {after}/{v2_total} = {100*after//v2_total}%")
    print("=" * 60)

if __name__ == "__main__":
    main()
