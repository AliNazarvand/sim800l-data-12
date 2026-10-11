#!/usr/bin/env python3
"""A1 FINAL — merge dups, remove holder/NC, add 7 missing, upgrade status."""

import re
import shutil
import yaml
from datetime import datetime, timezone
from pathlib import Path

ROOT     = Path(__file__).resolve().parent.parent
DATA     = ROOT / "data"
REPORTS  = ROOT / "reports"
DATA07   = DATA / "dat_07_hardware_reference.yaml"
REPORTS.mkdir(parents=True, exist_ok=True)

# --- Alias map (V1.00 name -> V2.02 canonical) -----------------------------
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

# --- Records to remove entirely --------------------------------------------
REMOVE_NAMES = {f"C{i}" for i in range(1, 9)} | {"NC"}

# --- Missing pins (source: V2.02 Table 5, verified in hw_v2_02_full.txt) ---
MISSING_PINS = [
    {"name": "FM_ANTP", "pin_number": "17", "category": "Antenna",
     "direction": "input",  "function": "Differential antenna for FM",
     "quote": "FM_ANTP 17 I Differential antenna for FM"},
    {"name": "FM_ANTN", "pin_number": "57", "category": "Antenna",
     "direction": "input",  "function": "Differential antenna for FM",
     "quote": "FM_ANTN 57 I (differential pair with FM_ANTP)"},
    {"name": "GSM_ANT", "pin_number": "40", "category": "Antenna",
     "direction": "io",     "function": "Connect GSM antenna",
     "quote": "GSM_ANT 40 I/O Connect GSM antenna"},
    {"name": "RESET",   "pin_number": "49", "category": "Reset",
     "direction": "input",  "function": "Reset input (Active low)",
     "quote": "RESET 49 I Reset input(Active low)"},
    {"name": "RF_SYNC", "pin_number": "5",  "category": "RF",
     "direction": "output", "function": "Synchronizing signal of RF",
     "quote": "RF_SYNC 5 O Synchronizing signal of RF"},
    {"name": "VDD_EXT", "pin_number": "18", "category": "Power",
     "direction": "output", "function": "2.8V power output",
     "quote": "VDD_EXT 18 O 2.8V power output"},
    {"name": "VRTC",    "pin_number": "56", "category": "Power",
     "direction": "io",     "function": "Power supply for RTC",
     "quote": "VRTC 56 I/O Power supply for RTC"},
]

# --- Helpers ---------------------------------------------------------------
def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def max_id_suffix(records):
    m = 0
    for r in records:
        i = str(r.get("id", ""))
        mm = re.match(r'^dat_07_(\d{4})$', i)
        if mm:
            m = max(m, int(mm.group(1)))
    return m

def load_dat07():
    if not DATA07.exists():
        return []
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

# --- Phase 1: snapshot ------------------------------------------------------
def phase_snapshot():
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    snap = ROOT / f"dat07_a1_snapshot_{stamp}"
    snap.mkdir(exist_ok=True)
    if DATA07.exists():
        shutil.copy2(DATA07, snap / DATA07.name)
    print(f"Snapshot: {snap}")
    return snap

# --- Phase 2: merge duplicates ---------------------------------------------
def phase_merge(records):
    """Return (new_records, merge_log)."""
    # Group by canonical name
    groups = {}
    for r in records:
        n = r.get("name", "")
        groups.setdefault(canonical(n), []).append(r)

    remove_ids = set()
    merge_log = []
    conflicts_added = 0

    for canon, recs in groups.items():
        if len(recs) < 2:
            continue
        # Prefer V2.02
        v2_rec = None
        v1_recs = []
        for r in recs:
            ver = (r.get("source") or {}).get("version", "")
            if ver == "V2.02" and v2_rec is None:
                v2_rec = r
            else:
                v1_recs.append(r)
        if v2_rec is None:
            # no V2.02, keep first V1.00 and drop the rest
            v2_rec = v1_recs[0]
            v1_recs = v1_recs[1:]

        # Merge aliases into alternate_function
        v1_names = [r.get("name", "") for r in v1_recs]
        if v1_names:
            existing = v2_rec.get("alternate_function")
            existing = "" if existing in (None, "") else str(existing)
            additions = [f"V1.00: {n}" for n in v1_names]
            merged = existing
            for a in additions:
                merged = f"{merged}; {a}" if merged else a
            v2_rec["alternate_function"] = merged

            # Add conflicts entries
            conflicts = v2_rec.get("conflicts")
            if not isinstance(conflicts, list):
                conflicts = []
            for r in v1_recs:
                conflicts.append({
                    "type": "alias",
                    "detail": f"V1.00 named it {r.get('name')}",
                })
            v2_rec["conflicts"] = conflicts
            conflicts_added += len(v1_recs)

            for r in v1_recs:
                remove_ids.add(r.get("id"))

            merge_log.append({
                "canonical": canon,
                "kept_id": v2_rec.get("id"),
                "kept_name": v2_rec.get("name"),
                "removed": [(r.get("id"), r.get("name"),
                             (r.get("source") or {}).get("version", "?"))
                            for r in v1_recs],
            })

    new_records = [r for r in records if r.get("id") not in remove_ids]
    return new_records, merge_log

# --- Phase 3: remove holder/NC ---------------------------------------------
def phase_remove(records):
    removed = []
    kept = []
    for r in records:
        n = r.get("name", "")
        if n in REMOVE_NAMES:
            removed.append((r.get("id"), n))
        else:
            kept.append(r)
    return kept, removed

# --- Phase 4: add missing pins ---------------------------------------------
def phase_add(records):
    existing = {canonical(r.get("name", "")) for r in records}
    next_n = max_id_suffix(records)
    added = []
    ts = now_iso()
    for spec in MISSING_PINS:
        if canonical(spec["name"]) in existing:
            continue
        next_n += 1
        new_id = f"dat_07_{next_n:04d}"
        rec = {
            "id": new_id,
            "category": spec["category"],
            "name": spec["name"],
            "pin_number": spec["pin_number"],
            "direction": spec["direction"],
            "voltage_min": None,
            "voltage_typ": None,
            "voltage_max": None,
            "current_typ": None,
            "current_max": None,
            "function": spec["function"],
            "alternate_function": None,
            "pull_up_down": None,
            "esd_rating": None,
            "impedance": None,
            "decoupling": None,
            "source": {
                "name": "SIM800H&SIM800L_Hardware_Design",
                "version": "V2.02",
                "date": "2015-07-27",
                "page": "16",
                "section": "Table 5: Pin description",
                "quote": spec["quote"],
            },
            "source_type": "primary",
            "confidence": 0.9,
            "status": "complete",
            "conflicts": [],
            "notes": "Added in A1 final pass from V2.02 Table 5.",
            "applicable_models": ["SIM800L"],
            "tags": ["hardware", "pin", "added-a1"],
            "created_at": ts,
            "updated_at": ts,
        }
        records.append(rec)
        added.append(new_id + " " + spec["name"])
    return records, added

# --- Phase 5: upgrade status -----------------------------------------------
def phase_status(records):
    ts = now_iso()
    changed = {"to_complete": 0, "kept_partial": 0}
    for r in records:
        ver = (r.get("source") or {}).get("version", "")
        old = r.get("status", "")
        if ver == "V2.02":
            r["status"] = "complete"
            r["confidence"] = 0.9
            if old != "complete":
                changed["to_complete"] += 1
        elif ver == "V1.00":
            r["status"] = "partial"
            r["confidence"] = 0.6
            changed["kept_partial"] += 1
        r["updated_at"] = ts
    return records, changed

# --- Report ----------------------------------------------------------------
def write_report(before_count, after_count, merge_log, removed, added,
                 status_changes, v2_total):
    L = []
    L.append("# A1_dat07_final_report")
    L.append("")
    L.append(f"Generated: {now_iso()}")
    L.append("")
    L.append("## Summary")
    L.append("")
    L.append(f"- Records before: {before_count}")
    L.append(f"- Records after:  {after_count}")
    L.append(f"- V2.02 canonical pins (excl. BT_ANT): {v2_total}")
    L.append(f"- Coverage: {after_count} / {v2_total} = "
             f"{100 * after_count // max(1, v2_total)}%")
    L.append("")
    L.append("## Duplicate merges")
    L.append("")
    L.append("| Canonical | Kept (V2.02) | Removed (V1.00) |")
    L.append("|-----------|--------------|-----------------|")
    for m in merge_log:
        removed_str = ", ".join(f"{i}({n})" for i, n, _ in m["removed"])
        L.append(f"| {m['canonical']} | {m['kept_id']} ({m['kept_name']}) "
                 f"| {removed_str} |")
    L.append("")
    L.append("## Removed (SIM-card-holder + NC)")
    L.append("")
    for i, n in removed:
        L.append(f"- {i} ({n})")
    L.append("")
    L.append("## Added (missing V2.02 pins)")
    L.append("")
    for a in added:
        L.append(f"- {a}")
    L.append("")
    L.append("## Status changes")
    L.append("")
    L.append(f"- Upgraded to `complete` (V2.02): {status_changes['to_complete']}")
    L.append(f"- Kept `partial` (V1.00):          {status_changes['kept_partial']}")
    L.append("")
    out = REPORTS / "A1_dat07_final_report.md"
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"  Wrote {out}")

# --- Main ------------------------------------------------------------------
def main():
    print("=" * 60)
    print("A1 FINAL — dat_07 Hardware Reference")
    print("=" * 60)

    print()
    print("Phase 1: snapshot")
    phase_snapshot()

    print()
    print("Phase 2: load and merge duplicates")
    records = load_dat07()
    before = len(records)
    records, merge_log = phase_merge(records)
    print(f"  Before: {before}")
    print(f"  After merge: {len(records)}  (removed {before - len(records)})")

    print()
    print("Phase 3: remove holder (C1..C8) and NC")
    records, removed = phase_remove(records)
    print(f"  Removed: {len(removed)}")
    for i, n in removed:
        print(f"    - {i} ({n})")

    print()
    print("Phase 4: add missing V2.02 pins")
    records, added = phase_add(records)
    print(f"  Added: {len(added)}")
    for a in added:
        print(f"    - {a}")

    print()
    print("Phase 5: upgrade status")
    records, changes = phase_status(records)
    print(f"  to_complete: {changes['to_complete']}")
    print(f"  kept_partial: {changes['kept_partial']}")

    print()
    print("Phase 6: save and report")
    save_dat07(records)
    after = len(records)
    # V2.02 canonical total = 56, minus BT_ANT = 55
    v2_total = 55
    write_report(before, after, merge_log, removed, added, changes, v2_total)

    print()
    print("=" * 60)
    print(f"Records before: {before}")
    print(f"Records after:  {after}")
    print(f"Coverage:       {after}/{v2_total} = {100*after//max(1,v2_total)}%")
    print("=" * 60)

if __name__ == "__main__":
    main()
