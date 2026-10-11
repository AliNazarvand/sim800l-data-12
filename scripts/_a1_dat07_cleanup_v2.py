#!/usr/bin/env python3
"""A1 CLEANUP v2 — fill direction/function from Table 5, fix quotes, restatus."""

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

# --- Authoritative pin data from V2.02 Table 5 -----------------------------
# (name -> direction, function, page)
# direction is one of: input, output, io
PIN_DATA = {
    "VBAT":     {"direction": "input",  "function": "Power supply",                  "page": "16"},
    "VRTC":     {"direction": "io",     "function": "Power supply for RTC",          "page": "16"},
    "VDD_EXT":  {"direction": "output", "function": "2.8V power output",             "page": "16"},
    "PWRKEY":   {"direction": "input",  "function": "Power on/down",                 "page": "16"},

    "MIC1P":    {"direction": "input",  "function": "Differential audio input",      "page": "16"},
    "MIC1N":    {"direction": "input",  "function": "Differential audio input",      "page": "16"},
    "SPK1P":    {"direction": "output", "function": "Differential audio output",     "page": "16"},
    "SPK1N":    {"direction": "output", "function": "Differential audio output",     "page": "16"},
    "MIC2P":    {"direction": "input",  "function": "Differential audio input",      "page": "16"},
    "MIC2N":    {"direction": "input",  "function": "Differential audio input",      "page": "16"},
    "SPK2P":    {"direction": "output", "function": "Differential audio output",     "page": "16"},
    "SPK2N":    {"direction": "output", "function": "Differential audio output",     "page": "16"},

    "PCM_CLK":  {"direction": "output", "function": "PCM interface for digital audio", "page": "16"},
    "PCM_OUT":  {"direction": "output", "function": "PCM interface for digital audio", "page": "16"},
    "PCM_SYNC": {"direction": "output", "function": "PCM interface for digital audio", "page": "16"},
    "PCM_IN":   {"direction": "input",  "function": "PCM interface for digital audio", "page": "16"},

    "KBC0":     {"direction": "input",  "function": "Keypad matrix column",          "page": "16"},
    "KBC1":     {"direction": "input",  "function": "Keypad matrix column",          "page": "16"},
    "KBC2":     {"direction": "input",  "function": "Keypad matrix column",          "page": "16"},
    "KBC3":     {"direction": "input",  "function": "Keypad matrix column",          "page": "16"},
    "KBC4":     {"direction": "input",  "function": "Keypad matrix column",          "page": "16"},
    "KBR0":     {"direction": "output", "function": "Keypad matrix row",             "page": "16"},
    "KBR1":     {"direction": "output", "function": "Keypad matrix row",             "page": "16"},
    "KBR2":     {"direction": "output", "function": "Keypad matrix row",             "page": "16"},
    "KBR3":     {"direction": "output", "function": "Keypad matrix row",             "page": "16"},
    "KBR4":     {"direction": "output", "function": "Keypad matrix row",             "page": "16"},

    "GPIO1":    {"direction": "io",     "function": "Programmable general purpose input and output", "page": "16"},
    "GPIO2":    {"direction": "io",     "function": "Programmable general purpose input and output", "page": "16"},
    "GPIO3":    {"direction": "io",     "function": "Programmable general purpose input and output", "page": "16"},

    "NETLIGHT": {"direction": "output", "function": "Network status",                "page": "17"},
    "STATUS":   {"direction": "output", "function": "Power on status",               "page": "17"},

    "DTR":      {"direction": "input",  "function": "Data terminal ready",           "page": "17"},
    "RI":       {"direction": "output", "function": "Ring indicator",                "page": "17"},
    "DCD":      {"direction": "output", "function": "Data carrier detect",           "page": "17"},
    "CTS":      {"direction": "output", "function": "Request to send",               "page": "17"},
    "RTS":      {"direction": "input",  "function": "Clear to send",                 "page": "17"},
    "TXD":      {"direction": "output", "function": "Transmit data",                 "page": "17"},
    "RXD":      {"direction": "input",  "function": "Receive data",                  "page": "17"},

    "VBUS":     {"direction": "input",  "function": "USB power supply",              "page": "17"},
    "USB_DP":   {"direction": "io",     "function": "Debug and download",            "page": "17"},
    "USB_DN":   {"direction": "io",     "function": "Debug and download",            "page": "17"},

    "SDA":      {"direction": "io",     "function": "Open drain output",             "page": "17"},
    "SCL":      {"direction": "output", "function": "Open drain output",             "page": "17"},

    "SIM_VDD":  {"direction": "output", "function": "Voltage supply for SIM card. Support 1.8V or 3V SIM card", "page": "17"},
    "SIM_DATA": {"direction": "io",     "function": "SIM data input/output",         "page": "17"},
    "SIM_CLK":  {"direction": "output", "function": "SIM clock",                     "page": "17"},
    "SIM_RST":  {"direction": "output", "function": "SIM reset",                     "page": "17"},
    "SIM_DET":  {"direction": "input",  "function": "SIM card detection",            "page": "17"},

    "GSM_ANT":  {"direction": "io",     "function": "Connect GSM antenna",           "page": "17"},
    "FM_ANTP":  {"direction": "input",  "function": "Differential antenna for FM",   "page": "17"},
    "FM_ANTN":  {"direction": "input",  "function": "Differential antenna for FM",   "page": "17"},

    "RF_SYNC":  {"direction": "output", "function": "Synchronizing signal of RF",    "page": "17"},
    "RESET":    {"direction": "input",  "function": "Reset input (Active low)",      "page": "17"},

    "ISINK0":   {"direction": "input",  "function": "Drive LCD backlight",           "page": "18"},
    "ISINK1":   {"direction": "input",  "function": "Drive keypad backlight",        "page": "18"},

    # PWM is from Table 30 (page 48)
    "PWM":      {"direction": "output", "function": "Pulse-width modulation",
                 "page": "48",
                 "section": "Table 30: Pin definition of the PWM",
                 "quote": "PWM 26 O Pulse-width modulation"},
}

# Extra quote fixes for records whose current quote is from Figure Index/TOC
EXTRA_QUOTE_FIX = {
    "NETLIGHT": "NETLIGHT 64 O Network status",
    "STATUS":   "STATUS 4 O Power on status",
    "PWRKEY":   "PWRKEY 48 I PWRKEY should be pulled low at least 1 second and then released to power on/down the module.",
    "VBAT":     "VBAT 1,42 I Power supply",
    "SIM_VDD":  "SIM_VDD 16 O Voltage supply for SIM card. Support 1.8V or 3V SIM card",
}

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

def snapshot():
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    snap = ROOT / f"dat07_a1_cleanup_v2_snapshot_{stamp}"
    snap.mkdir(exist_ok=True)
    if DATA07.exists():
        shutil.copy2(DATA07, snap / DATA07.name)
    print(f"Snapshot: {snap}")
    return snap

def phase_fill(records):
    """Fill direction/function for all records with a matching name in PIN_DATA."""
    dir_filled = 0
    fn_filled = 0
    section_fixed = 0
    page_fixed = 0

    for r in records:
        name = r.get("name", "")
        spec = PIN_DATA.get(name)
        if not spec:
            continue

        # direction
        cur_dir = str(r.get("direction", "") or "").lower()
        if cur_dir in ("", "unknown") and spec["direction"] != "unknown":
            r["direction"] = spec["direction"]
            dir_filled += 1

        # function
        cur_fn = str(r.get("function", "") or "").strip().lower()
        if cur_fn in ("", "unknown", "n/a"):
            r["function"] = spec["function"]
            fn_filled += 1

        # source.section
        src = r.get("source")
        if not isinstance(src, dict):
            src = {}
            r["source"] = src
        want_section = spec.get("section", "Table 5: Pin description")
        if str(src.get("section", "")).strip() != want_section:
            src["section"] = want_section
            section_fixed += 1

        # source.page
        if str(src.get("page", "")).strip() != spec["page"]:
            src["page"] = spec["page"]
            page_fixed += 1

    print(f"  direction filled: {dir_filled}")
    print(f"  function filled:  {fn_filled}")
    print(f"  section fixed:    {section_fixed}")
    print(f"  page fixed:       {page_fixed}")
    return dir_filled, fn_filled, section_fixed, page_fixed

def phase_quote_fix(records):
    """Fix quotes for records whose quote is from Figure Index/TOC."""
    fixed = 0
    for r in records:
        name = r.get("name", "")
        want_quote = EXTRA_QUOTE_FIX.get(name)
        if not want_quote:
            continue
        src = r.get("source")
        if not isinstance(src, dict):
            continue
        cur = str(src.get("quote", "") or "")
        bad = (
            "FIGURE" in cur.upper()
            or "Multiplexing Function" in cur
            or "Current Consumption" in cur
            or "Characteristics" in cur
            or "RI Behaviors" in cur
            or cur.strip() == ""
        )
        if bad:
            src["quote"] = want_quote
            fixed += 1
    print(f"  quote fixed:      {fixed}")
    return fixed

def phase_status(records):
    to_complete = 0
    to_partial = 0
    ts = now_iso()
    for r in records:
        d = str(r.get("direction", "") or "").lower()
        f = str(r.get("function", "") or "").lower()
        ok = d not in ("", "unknown") and f not in ("", "unknown", "n/a")
        if ok:
            if r.get("status") != "complete":
                to_complete += 1
            r["status"] = "complete"
            r["confidence"] = 0.9
            # Remove misleading suffix from notes
            n = r.get("notes")
            if n:
                n = re.sub(r'\s*\|\s*Needs manual verification[^|]*',
                           '', str(n)).strip().strip("|").strip()
                if n.startswith("Auto-extracted from pin table."):
                    n = n.replace("Auto-extracted from pin table.", "").strip()
                if n.startswith("Added in A1 final pass from V2.02 Table 5."):
                    n = "Added in A1 final pass from V2.02 Table 5."
                r["notes"] = n if n else None
        else:
            r["status"] = "partial"
            r["confidence"] = 0.6
            to_partial += 1
        r["updated_at"] = ts
    print(f"  to complete:      {to_complete}")
    print(f"  to partial:       {to_partial}")
    return to_complete, to_partial

def phase_report(before, after, dir_f, fn_f, sect_f, page_f, quote_f, to_c, to_p, v2_total=56):
    L = []
    L.append("# A1_dat07_cleanup_v2_report")
    L.append("")
    L.append(f"Generated: {now_iso()}")
    L.append("")
    L.append("## Summary")
    L.append("")
    L.append(f"- Records before: {before}")
    L.append(f"- Records after:  {after}")
    L.append("")
    L.append("## Fields filled from V2.02 Table 5")
    L.append("")
    L.append(f"- direction filled:  {dir_f}")
    L.append(f"- function filled:   {fn_f}")
    L.append(f"- section fixed:     {sect_f}")
    L.append(f"- page fixed:        {page_f}")
    L.append(f"- quote fixed:       {quote_f}")
    L.append("")
    L.append("## Status distribution")
    L.append("")
    L.append(f"- Upgraded to `complete`: {to_c}")
    L.append(f"- Kept `partial`:         {to_p}")
    L.append("")
    L.append(f"## Coverage")
    L.append("")
    L.append(f"- V2.02 canonical pins (excl. BT_ANT, incl. PWM): {v2_total}")
    L.append(f"- dat_07 records: {after}")
    L.append(f"- Coverage: {after}/{v2_total} = {100*after//v2_total}%")
    L.append("")
    out = REPORTS / "A1_dat07_cleanup_v2_report.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"  Wrote {out}")

def main():
    print("=" * 60)
    print("A1 CLEANUP v2 — full direction/function fill")
    print("=" * 60)
    print()
    print("Phase 0: snapshot")
    snapshot()

    print()
    print("Phase 1: load")
    records = load_dat07()
    before = len(records)
    print(f"  Records: {before}")

    print()
    print("Phase 2: fill direction/function/section/page")
    dir_f, fn_f, sect_f, page_f = phase_fill(records)

    print()
    print("Phase 3: fix remaining quotes")
    quote_f = phase_quote_fix(records)

    print()
    print("Phase 4: re-evaluate status")
    to_c, to_p = phase_status(records)

    print()
    print("Phase 5: save and report")
    save_dat07(records)
    after = len(records)
    phase_report(before, after, dir_f, fn_f, sect_f, page_f, quote_f, to_c, to_p)

    print()
    print("=" * 60)
    print(f"Records:      {after}")
    print(f"Complete:     {sum(1 for r in records if r.get('status')=='complete')}")
    print(f"Partial:      {sum(1 for r in records if r.get('status')=='partial')}")
    print("=" * 60)

if __name__ == "__main__":
    main()
