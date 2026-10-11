#!/usr/bin/env python3
"""A1 supplementary — fix extraction bug, find duplicates, final gaps. Read-only."""

import re
import yaml
from pathlib import Path
from collections import defaultdict

ROOT     = Path(__file__).resolve().parent.parent
DATA     = ROOT / "data"
SOURCES  = ROOT / "sources" / "extracted"
REPORTS  = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

# --- Alias map: V1.00 name -> V2.02 canonical name ------------------------
ALIASES = {
    "VEXT":     "VDD_EXT",
    "ANT":      "GSM_ANT",
    "FM_ANT_P": "FM_ANTP",
    "FM_ANT_N": "FM_ANTN",
    "BPI_BUS1": "RF_SYNC",
    "USB_DM":   "USB_DN",
    "SIMPRE":   "SIM_DET",
    "SIM_PRE":  "SIM_DET",
    "UART_DTR": "DTR",
    "UART_RI":  "RI",
    "UART_DCD": "DCD",
    "PCMCLK":   "PCM_CLK",
    "PCMOUT":   "PCM_OUT",
    "PCMSYNC":  "PCM_SYNC",
    "PCMIN":    "PCM_IN",
    "VSIM":     "SIM_VDD",
}
for i in range(5):
    ALIASES[f"COL{i}"] = f"KBC{i}"
    ALIASES[f"ROW{i}"] = f"KBR{i}"

def canonical(name):
    return ALIASES.get(name, name)

# --- Fixed extraction ------------------------------------------------------
# Only match the actual section header, not Table Index entries (which have
# trailing dots). Examples:
#   OK   : "Table 5: Pin description"       (V2.02 uses uppercase; still ok)
#   SKIP : "Table 4: Pin description ....... 16"   (Table Index)
PIN_NAME_RE = re.compile(r'^([A-Z][A-Z0-9_]{1,20})\s+\d')

def extract_pins_from_txt(txt_path: Path):
    """Return list of raw pin names from the Pin Description section."""
    if not txt_path.exists():
        return []
    lines = txt_path.read_text(encoding="utf-8", errors="replace").splitlines()

    # Find the actual header line — start of line, "Table N: Pin description",
    # optional whitespace, and NOTHING else after (no dots, no page number).
    start = None
    header_re = re.compile(
        r'^\s*Table\s+\d+:\s+Pin\s+description\s*$',
        re.IGNORECASE,
    )
    for i, line in enumerate(lines):
        if header_re.match(line):
            start = i + 1
            break
    if start is None:
        return []

    # Collect rows until next section boundary
    pins, seen = [], set()
    for line in lines[start:start + 500]:
        stripped = line.strip()
        if not stripped:
            continue
        # Stop on next numbered section like 3.3. or 4. or a new table header
        if re.match(r'^\d+(\.\d+)?\.\d', stripped):
            break
        if re.match(r'^Table\s+\d+:', stripped, re.IGNORECASE):
            break
        m = PIN_NAME_RE.match(stripped)
        if not m:
            continue
        pin = m.group(1)
        # Filter group headings that appear inside the table
        if pin in {
            "Power", "Audio", "Interface", "PCM", "GPIO", "UART", "Debug",
            "I2C", "SIM", "ADC", "PWM", "Table", "Keypads", "Serial",
            "Status", "Ground", "Antenna", "Other", "Synchronizing",
            "Keypad", "Network", "Operating",
        }:
            continue
        if pin not in seen:
            seen.add(pin)
            pins.append(pin)
    return pins

# --- Phase A: re-extract pins (fixed) --------------------------------------
def phase_a():
    v2 = extract_pins_from_txt(SOURCES / "hw_v2_02_full.txt")
    v1 = extract_pins_from_txt(SOURCES / "hw_v1_00_full.txt")

    v2_c = list(dict.fromkeys(canonical(p) for p in v2))
    v1_c = list(dict.fromkeys(canonical(p) for p in v1))

    print(f"V2.02 raw pins: {len(v2)}  (canonical: {len(v2_c)})")
    print(f"V1.00 raw pins: {len(v1)}  (canonical: {len(v1_c)})")
    print()
    print("V1.00 raw pin names:")
    for p in v1:
        print(f"  - {p}")
    print()
    return {"v2": v2, "v1": v1, "v2_c": v2_c, "v1_c": v1_c}

# --- Phase B: duplicate detection in dat_07 --------------------------------
def phase_b():
    p = DATA / "dat_07_hardware_reference.yaml"
    dat07 = yaml.safe_load(p.read_text(encoding="utf-8")) or []

    # Group records by canonical name
    groups = defaultdict(list)
    for r in dat07:
        if not isinstance(r, dict):
            continue
        n = r.get("name", "?")
        groups[canonical(n)].append({
            "id": r.get("id", "?"),
            "raw_name": n,
            "version": (r.get("source") or {}).get("version", "?"),
            "source_name": (r.get("source") or {}).get("name", "?"),
            "page": (r.get("source") or {}).get("page", "?"),
            "category": r.get("category", "?"),
        })

    # Only report groups with >1 record
    dup_groups = {k: v for k, v in groups.items() if len(v) > 1}

    L = []
    L.append("# A1_dat07_duplicates")
    L.append("")
    L.append(f"Total records: {len(dat07)}")
    L.append(f"Distinct canonical names: {len(groups)}")
    L.append(f"Groups with duplicates: {len(dup_groups)}")
    L.append("")
    L.append("## Duplicate groups")
    L.append("")
    L.append("| Canonical | Records | Versions | Recommendation |")
    L.append("|-----------|---------|----------|----------------|")
    for canon in sorted(dup_groups.keys()):
        recs = dup_groups[canon]
        versions = ", ".join(sorted({r["version"] for r in recs}))
        rec = "Keep V2.02 record, move V1.00 alias to alternate_function"
        if all(r["version"] == "V1.00" for r in recs):
            rec = "All V1.00 — review manually (no V2.02 equivalent)"
        L.append(f"| {canon} | {len(recs)} | {versions} | {rec} |")
    L.append("")
    L.append("## Detail per group")
    L.append("")
    for canon in sorted(dup_groups.keys()):
        recs = dup_groups[canon]
        L.append(f"### {canon}")
        L.append("")
        L.append("| ID | Raw name | Version | Source | Page | Category |")
        L.append("|----|----------|---------|--------|------|----------|")
        for r in recs:
            L.append(f"| {r['id']} | {r['raw_name']} | {r['version']} | "
                     f"{r['source_name']} | {r['page']} | {r['category']} |")
        L.append("")

    out = REPORTS / "A1_dat07_duplicates.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"  Wrote {out}")
    print(f"  Duplicate groups: {len(dup_groups)}")
    return {"groups": groups, "dups": dup_groups}

# --- Phase C: final gaps ---------------------------------------------------
# Pins that exist in V2.02 Table 5 but were missed by the regex (because
# they appear as their own subheading such as "PWM" or under "Other").
KNOWN_V2_EXTRA = {"PWM"}   # known to be in V2.02 §Table 30

# Pins that should NOT be added (module-family-specific)
EXCLUDE = {"BT_ANT"}       # SIM800H-only; dat_07 is SIM800L-only

# SIM-card-holder pins (not module pads)
HOLDER_PINS = {f"C{i}" for i in range(1, 9)}

def phase_c(pdfs, dup_data):
    v2_set = set(pdfs["v2_c"])
    v1_set = set(pdfs["v1_c"])

    groups = dup_data["groups"]
    dat07_canon = set(groups.keys())

    # Separate module pins from SIM-card-holder pins
    dat07_module_pins = {n for n in dat07_canon if n not in HOLDER_PINS}
    dat07_holder_pins = {n for n in dat07_canon if n in HOLDER_PINS}

    # Truly missing = in V2.02 (or known V2.02 extra) but not in dat_07 module pins
    v2_all = v2_set | KNOWN_V2_EXTRA
    missing_v2 = sorted(v2_all - dat07_module_pins - EXCLUDE)
    excluded_bt_ant = sorted(v2_all & EXCLUDE)

    # In V1.00 but not in dat_07 and not in V2.02
    only_v1 = sorted(v1_set - dat07_module_pins - v2_all)

    L = []
    L.append("# A1_dat07_final_gaps")
    L.append("")
    L.append(f"dat_07 module pins (excl. holder): {len(dat07_module_pins)}")
    L.append(f"dat_07 SIM-card-holder pins:       {len(dat07_holder_pins)}")
    L.append(f"V2.02 canonical pins (extracted):  {len(v2_set)}")
    L.append(f"V1.00 canonical pins (extracted):  {len(v1_set)}")
    L.append(f"V2.02 extra (subheading pins):     {sorted(KNOWN_V2_EXTRA)}")
    L.append("")
    L.append("## Final missing pins to add to dat_07")
    L.append("")
    if missing_v2:
        L.append("| Pin | In V2.02 | In V1.00 | Source page | Notes |")
        L.append("|-----|----------|----------|-------------|-------|")
        for p in missing_v2:
            in_v2 = "yes"
            in_v1 = "yes" if p in v1_set else "no"
            L.append(f"| {p} | {in_v2} | {in_v1} | V2.02 Table 5 | "
                     f"Add from V2.02 (primary) |")
    else:
        L.append("(none)")
    L.append("")
    L.append("## Excluded pins (must NOT be added)")
    L.append("")
    for p in excluded_bt_ant:
        L.append(f"- {p} — SIM800H-only, R1 forbids including it in SIM800L dataset")
    L.append("")
    L.append("## V1.00-only pins (not in dat_07 and not in V2.02)")
    L.append("")
    if only_v1:
        for p in only_v1:
            L.append(f"- {p}")
    else:
        L.append("(none)")
    L.append("")
    L.append("## SIM-card-holder pins currently in dat_07")
    L.append("")
    L.append("These are pins of the Molex 91228 / Amphenol C707 SIM card holder,")
    L.append("not module pads. They do not belong in dat_07.")
    L.append("")
    for p in sorted(dat07_holder_pins):
        L.append(f"- {p}")
    L.append("")
    L.append("Recommendation: move these records to `dat_16_board_evb.yaml`")
    L.append("(or delete if dat_16 is deferred). Do NOT keep them in dat_07.")
    L.append("")
    L.append("## PWM — was reported as 'extra' by the previous run")
    L.append("")
    L.append("PWM **is present** in V2.02 §Table 30 (Pin definition of the PWM).")
    L.append("The previous extraction missed it because PWM appears as a subheading")
    L.append("(group label) inside the Pin Description table, not as a data row")
    L.append("with a pin number. It has been restored to the missing list.")
    L.append("")

    out = REPORTS / "A1_dat07_final_gaps.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"  Wrote {out}")
    print()
    print(f"  Missing pins to add: {missing_v2}")
    print(f"  Excluded (SIM800H-only): {excluded_bt_ant}")
    print(f"  V1-only extras: {only_v1}")
    print(f"  Holder pins in dat_07: {sorted(dat07_holder_pins)}")

# --- Main ------------------------------------------------------------------
def main():
    print("=" * 60)
    print("Phase A — re-extract pins (fixed extraction function)")
    print("=" * 60)
    pdfs = phase_a()

    print("=" * 60)
    print("Phase B — duplicate analysis in dat_07")
    print("=" * 60)
    dup_data = phase_b()

    print()
    print("=" * 60)
    print("Phase C — final gaps")
    print("=" * 60)
    phase_c(pdfs, dup_data)

    print()
    print("=" * 60)
    print("Reports:")
    print("  - reports/A1_dat07_duplicates.md")
    print("  - reports/A1_dat07_final_gaps.md")
    print("=" * 60)

if __name__ == "__main__":
    main()
