#!/usr/bin/env python3
"""A1 — dat_07 Hardware Reference audit + gap analysis. Read-only."""

import re
import yaml
from pathlib import Path
from collections import Counter, OrderedDict

ROOT     = Path(__file__).resolve().parent.parent
DATA     = ROOT / "data"
SOURCES  = ROOT / "sources" / "extracted"
REPORTS  = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

PIN_ROW_RE = re.compile(r'^([A-Z][A-Z0-9_]{1,20})\s+\d')

# Aliases: V1.00 name -> V2.02 canonical name
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
}
for i in range(5):
    ALIASES[f"COL{i}"] = f"KBC{i}"
    ALIASES[f"ROW{i}"] = f"KBR{i}"

def canonical(name: str) -> str:
    return ALIASES.get(name, name)

def extract_pins_from_txt(txt_path: Path):
    """Locate the pin description table and extract pin names."""
    if not txt_path.exists():
        return []
    text = txt_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    start = None
    for i, line in enumerate(lines):
        if "Pin description" in line and "Table" in line:
            start = i + 1
            break
    if start is None:
        return []

    pins, seen = [], set()
    for line in lines[start:start + 400]:
        stripped = line.strip()
        if re.match(r'^Table \d+:', stripped):
            break
        if re.match(r'^3\.3\.', stripped):
            break
        if re.match(r'^4\.', stripped) and "Pin" not in stripped:
            break
        m = PIN_ROW_RE.match(stripped)
        if m:
            pin = m.group(1)
            # Filter obvious non-pins
            if pin in {"Power", "Audio", "Interface", "PCM", "GPIO",
                       "UART", "Debug", "I2C", "SIM", "ADC", "PWM",
                       "Table", "Keypads", "Serial", "Status"}:
                continue
            if pin not in seen:
                seen.add(pin)
                pins.append(pin)
    return pins

# ---------------------------------------------------------------------------
# Phase 1 — current dat_07 state
# ---------------------------------------------------------------------------
def phase1():
    p = DATA / "dat_07_hardware_reference.yaml"
    if not p.exists():
        return None
    dat07 = yaml.safe_load(p.read_text(encoding="utf-8")) or []

    categories = Counter()
    src_names  = Counter()
    src_full   = Counter()
    statuses   = Counter()
    conf_bins  = Counter()
    duplicates = []
    names, pin_numbers = [], []

    for r in dat07:
        if not isinstance(r, dict):
            continue
        categories[r.get("category", "?")] += 1
        statuses[r.get("status", "?")] += 1
        s = r.get("source", {})
        if isinstance(s, dict):
            src_names[s.get("name", "?")] += 1
            src_full[f"{s.get('name','?')} {s.get('version','?')}"] += 1
        c = r.get("confidence", 0)
        if isinstance(c, (int, float)):
            if c == 0:      conf_bins["0.0"] += 1
            elif c < 0.5:   conf_bins["<0.5"] += 1
            elif c < 0.7:   conf_bins["0.5-0.7"] += 1
            else:           conf_bins[">=0.7"] += 1
        n = r.get("name")
        if n:
            names.append(n)
        pn = r.get("pin_number")
        if pn:
            pin_numbers.append(pn)
        if "possible-duplicate" in (r.get("tags") or []):
            duplicates.append(n)

    L = []
    L.append("# A1_dat07_current_state")
    L.append("")
    L.append(f"Total records: {len(dat07)}")
    L.append("")
    L.append("## Category distribution")
    L.append("")
    L.append("| Category | Count |")
    L.append("|----------|-------|")
    for k, v in categories.most_common():
        L.append(f"| {k} | {v} |")
    L.append("")
    L.append("## Status distribution")
    L.append("")
    L.append("| Status | Count |")
    L.append("|--------|-------|")
    for k, v in statuses.most_common():
        L.append(f"| {k} | {v} |")
    L.append("")
    L.append("## Source distribution")
    L.append("")
    L.append("| Source | Count |")
    L.append("|--------|-------|")
    for k, v in src_names.most_common():
        L.append(f"| {k} | {v} |")
    L.append("")
    L.append("### Source+version")
    L.append("")
    L.append("| Source + Version | Count |")
    L.append("|------------------|-------|")
    for k, v in src_full.most_common():
        L.append(f"| {k} | {v} |")
    L.append("")
    L.append("## Confidence distribution")
    L.append("")
    L.append("| Bucket | Count |")
    L.append("|--------|-------|")
    for k, v in conf_bins.most_common():
        L.append(f"| {k} | {v} |")
    L.append("")
    L.append("## All pin names in dat_07 (alphabetical)")
    L.append("")
    for n in sorted(set(names)):
        L.append(f"- {n}")
    L.append("")
    L.append("## All pin_number values in dat_07 (raw)")
    L.append("")
    for n in sorted(set(pin_numbers)):
        L.append(f"- {n}")
    L.append("")
    L.append("## Records tagged possible-duplicate")
    L.append("")
    if duplicates:
        for n in sorted(set(duplicates)):
            L.append(f"- {n}")
    else:
        L.append("- (none)")
    L.append("")

    out = REPORTS / "A1_dat07_current_state.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"  Wrote {out}")
    return {
        "count": len(dat07),
        "names": names,
        "categories": categories,
        "statuses": statuses,
    }

# ---------------------------------------------------------------------------
# Phase 2 — extract pins from both PDFs
# ---------------------------------------------------------------------------
def phase2():
    v2 = extract_pins_from_txt(SOURCES / "hw_v2_02_full.txt")
    v1 = extract_pins_from_txt(SOURCES / "hw_v1_00_full.txt")

    v2_canon = list(OrderedDict.fromkeys(canonical(p) for p in v2))
    v1_canon = list(OrderedDict.fromkeys(canonical(p) for p in v1))

    set2 = set(v2_canon)
    set1 = set(v1_canon)

    both    = sorted(set2 & set1)
    only_v2 = sorted(set2 - set1)
    only_v1 = sorted(set1 - set2)

    L = []
    L.append("# A1_dat07_pdf_pins")
    L.append("")
    L.append(f"V2.02 raw pin count: {len(v2)}  (canonical: {len(v2_canon)})")
    L.append(f"V1.00 raw pin count: {len(v1)}  (canonical: {len(v1_canon)})")
    L.append("")
    L.append("## Raw pin names extracted — V2.02")
    L.append("")
    for n in v2:
        L.append(f"- {n}")
    L.append("")
    L.append("## Raw pin names extracted — V1.00")
    L.append("")
    for n in v1:
        L.append(f"- {n}")
    L.append("")
    L.append("## Canonical comparison")
    L.append("")
    L.append(f"- In both: {len(both)}")
    L.append(f"- Only in V2.02: {len(only_v2)}")
    L.append(f"- Only in V1.00: {len(only_v1)}")
    L.append("")
    L.append("### Pins in both")
    L.append("")
    for n in both:
        L.append(f"- {n}")
    L.append("")
    L.append("### Pins only in V2.02 (candidates for priority source)")
    L.append("")
    for n in only_v2:
        L.append(f"- {n}")
    L.append("")
    L.append("### Pins only in V1.00 (may be aliases or V1-only)")
    L.append("")
    for n in only_v1:
        L.append(f"- {n}")
    L.append("")
    L.append("## Alias map used (V1 -> canonical)")
    L.append("")
    L.append("| V1 name | Canonical |")
    L.append("|---------|-----------|")
    for k in sorted(ALIASES.keys()):
        L.append(f"| {k} | {ALIASES[k]} |")
    L.append("")

    out = REPORTS / "A1_dat07_pdf_pins.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"  Wrote {out}")
    return {
        "v2": v2, "v1": v1,
        "v2_canon": v2_canon, "v1_canon": v1_canon,
        "both": both, "only_v2": only_v2, "only_v1": only_v1,
    }

# ---------------------------------------------------------------------------
# Phase 3 — gap analysis
# ---------------------------------------------------------------------------
def phase3(state, pdfs):
    names_dat07 = state["names"]
    dat07_canon = {canonical(n) for n in names_dat07}

    # Exclude "C1".."C8" (SIM card holder pins from Molex/Amphenol table)
    dat07_module_pins = {n for n in dat07_canon if not re.match(r'^C\d$', n)}

    v2_set = set(pdfs["v2_canon"])
    v1_set = set(pdfs["v1_canon"])

    missing_in_dat07_from_v2 = sorted(v2_set - dat07_module_pins)
    missing_in_dat07_from_v1 = sorted(v1_set - dat07_module_pins)
    extra_in_dat07 = sorted(dat07_module_pins - (v2_set | v1_set))

    L = []
    L.append("# A1_dat07_gap_analysis")
    L.append("")
    L.append(f"dat_07 canonical module pins: {len(dat07_module_pins)}")
    L.append(f"V2.02 canonical pins:         {len(v2_set)}")
    L.append(f"V1.00 canonical pins:         {len(v1_set)}")
    L.append("")
    L.append("## Coverage of V2.02 pins by dat_07")
    L.append("")
    covered_v2 = sorted(v2_set & dat07_module_pins)
    L.append(f"- Covered: {len(covered_v2)} / {len(v2_set)}  "
             f"({100*len(covered_v2)//max(1,len(v2_set))}%)")
    L.append("")
    L.append("## Missing pins (in V2.02 but not in dat_07)")
    L.append("")
    if missing_in_dat07_from_v2:
        L.append("| Pin | In V2.02 | In V1.00 | Recommend |")
        L.append("|-----|----------|----------|-----------|")
        for p in missing_in_dat07_from_v2:
            in_v1 = "yes" if p in v1_set else "no"
            rec = "Add from V2.02"
            if in_v1 == "no":
                rec = "Add from V2.02 (only)"
            L.append(f"| {p} | yes | {in_v1} | {rec} |")
    else:
        L.append("(none)")
    L.append("")
    L.append("## Missing pins (in V1.00 but not in dat_07, not in V2.02)")
    L.append("")
    if missing_in_dat07_from_v1:
        for p in missing_in_dat07_from_v1:
            in_v2 = "yes" if p in v2_set else "no"
            L.append(f"- {p}  (in V2.02: {in_v2})")
    else:
        L.append("(none)")
    L.append("")
    L.append("## Extra pins (in dat_07 but not in either PDF pin table)")
    L.append("")
    if extra_in_dat07:
        for p in extra_in_dat07:
            L.append(f"- {p}")
    else:
        L.append("(none)")
    L.append("")
    L.append("## Notes")
    L.append("")
    L.append("- Pins C1..C8 in dat_07 are from the Molex / Amphenol")
    L.append("  SIM card holder tables (V2.02 §Table 18/19 and V1.00 §Table 18/19).")
    L.append("  They are not module pads and were excluded from coverage math.")
    L.append("- V2.02 uses `KBCx`/`KBRx` for keypad columns/rows;")
    L.append("  V1.00 uses `COLx`/`ROWx`. Both were normalised to `KBCx`/`KBRx`.")
    L.append("- V2.02 uses `PCM_CLK`/`PCM_OUT`/`PCM_SYNC`/`PCM_IN`;")
    L.append("  V1.00 uses `PCMCLK`/`PCMOUT`/`PCMSYNC`/`PCMIN`.")
    L.append("- V2.02 uses `USB_DN`; V1.00 uses `USB_DM`.")
    L.append("- V2.02 uses `SIM_DET`; V1.00 uses `SIMPRE`/`SIM_PRE`.")
    L.append("- V2.02 uses `DTR`/`RI`/`DCD`; V1.00 uses `UART_DTR`/`UART_RI`/`UART_DCD`.")
    L.append("- V2.02 uses `VDD_EXT`; V1.00 uses `VEXT`.")
    L.append("- V2.02 uses `GSM_ANT`/`FM_ANTP`/`FM_ANTN`;")
    L.append("  V1.00 uses `ANT`/`FM_ANT_P`/`FM_ANT_N`.")
    L.append("- V2.02 uses `RF_SYNC`; V1.00 uses `BPI_BUS1`.")
    L.append("- `BT_ANT` is SIM800H-only — should not be added to dat_07 for SIM800L.")
    L.append("")
    L.append("## Recommended next actions")
    L.append("")
    L.append("1. Add missing V2.02 pins to dat_07 with source = V2.02 (priority).")
    L.append("2. For each new record, capture page/section from V2.02 table.")
    L.append("3. Where a V2.02 pin has a V1.00 alias (see A1_dat07_pdf_pins.md),")
    L.append("   record the alias in `alternate_function` or `notes`.")
    L.append("4. Do not add `BT_ANT` (SIM800H-only).")
    L.append("5. After populating, update `status` to `partial` or `complete`")
    L.append("   depending on confidence in each record's source.")
    L.append("")

    out = REPORTS / "A1_dat07_gap_analysis.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"  Wrote {out}")

# ---------------------------------------------------------------------------
def main():
    print("Phase 1: dat_07 current state")
    state = phase1()
    if state is None:
        print("ERROR: dat_07 not found")
        return

    print()
    print("Phase 2: extract pins from PDFs")
    pdfs = phase2()

    print()
    print("Phase 3: gap analysis")
    phase3(state, pdfs)

    print()
    print("=" * 60)
    print(f"dat_07 records: {state['count']}")
    print(f"V2.02 pins extracted: {len(pdfs['v2'])}")
    print(f"V1.00 pins extracted: {len(pdfs['v1'])}")
    print(f"Pins in both: {len(pdfs['both'])}")
    print(f"Only V2.02:   {len(pdfs['only_v2'])}")
    print(f"Only V1.00:   {len(pdfs['only_v1'])}")
    print("=" * 60)

if __name__ == "__main__":
    main()
