#!/usr/bin/env python3
"""READ-ONLY data integrity audit for sim800l-data.

This script does NOT modify any data file. It only reports.

Based on findings from `diagnose_sources.py`:
  - _at_commands_index.json appears to be DERIVED from dat_01 (not a source)
  - dat_01 command format may be missing '+' prefix
  - dat_02 contains records with `notes: Suspected command syntax, not URC`
  - dat_07 has fewer pins than the hardware design expects

Exit code:
  0 - audit completed (issues may exist)
  1 - fatal error
"""
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[FATAL] PyYAML required. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


def load_records(filename):
    """Read a YAML dataset (list of records)."""
    path = DATA_DIR / filename
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
    except Exception as exc:
        print(f"  [WARN] {filename}: {exc}", file=sys.stderr)
        return []
    if data is None:
        return []
    if not isinstance(data, list):
        return [data]
    return data


def audit_dat_01():
    print("\n=== dat_01 AT Command Audit ===")
    records = load_records("dat_01_at_command.yaml")
    total = len(records)
    print(f"  Total records: {total}")
    if total == 0:
        return {"total": 0, "with_plus": 0, "without_plus": 0,
                "with_at_plus": 0, "bad_samples": []}

    with_plus = 0
    with_at_plus = 0
    without_plus = 0
    bad_samples = []
    for r in records:
        if not isinstance(r, dict):
            continue
        cmd = str(r.get("command", "")).strip()
        if not cmd:
            continue
        if cmd.startswith("AT+"):
            with_at_plus += 1
        elif cmd.startswith("+"):
            with_plus += 1
        else:
            without_plus += 1
            if len(bad_samples) < 10:
                bad_samples.append(cmd)

    print(f"  Commands with 'AT+' prefix : {with_at_plus}")
    print(f"  Commands with '+' prefix   : {with_plus}")
    print(f"  Commands WITHOUT any prefix: {without_plus}")
    if bad_samples:
        print(f"  Samples without prefix     : {bad_samples}")

    return {"total": total, "with_plus": with_plus,
            "with_at_plus": with_at_plus,
            "without_plus": without_plus,
            "bad_samples": bad_samples}


def audit_dat_02():
    print("\n=== dat_02 URC Audit ===")
    records = load_records("dat_02_urc.yaml")
    total = len(records)
    print(f"  Total records: {total}")
    if total == 0:
        return {"total": 0, "suspected": 0, "incomplete_trigger": 0}

    suspected = 0
    incomplete_trigger = 0
    samples = []
    for r in records:
        if not isinstance(r, dict):
            continue
        notes = str(r.get("notes", "")).lower()
        if "suspected" in notes or "not urc" in notes or "needs manual" in notes:
            suspected += 1
            if len(samples) < 5:
                samples.append(str(r.get("id", "?")))
        trigger = str(r.get("trigger_event", "")).strip()
        if trigger and len(trigger) > 5 and not trigger.endswith("."):
            words = trigger.split()
            if words and len(words[-1]) < 8 and words[-1].islower():
                incomplete_trigger += 1

    print(f"  Self-marked as 'Suspected' : {suspected}")
    print(f"  Possibly truncated triggers: {incomplete_trigger}")
    if samples:
        print(f"  Sample suspected IDs       : {samples}")

    return {"total": total, "suspected": suspected,
            "incomplete_trigger": incomplete_trigger,
            "sample_suspected": samples}


def audit_dat_03():
    print("\n=== dat_03 Error Code Audit ===")
    records = load_records("dat_03_error_code.yaml")
    total = len(records)
    print(f"  Total records: {total}")
    if total == 0:
        return {"total": 0, "unique_pairs": 0, "duplicates": 0}

    pairs = []
    for r in records:
        if not isinstance(r, dict):
            continue
        et = str(r.get("error_type", "")).upper()
        code = str(r.get("code", "")).strip()
        if et and code:
            pairs.append((et, code))

    cnt = Counter(pairs)
    duplicates = [(k, v) for k, v in cnt.items() if v > 1]
    print(f"  Unique (error_type, code): {len(cnt)}")
    print(f"  Duplicates (>1 occurrence): {len(duplicates)}")
    for k, v in duplicates[:5]:
        print(f"    {k[0]} {k[1]}: {v} times")

    return {"total": total, "unique_pairs": len(cnt),
            "duplicates": len(duplicates)}


def audit_dat_07():
    print("\n=== dat_07 Hardware Pin Audit ===")
    records = load_records("dat_07_hardware_reference.yaml")
    total = len(records)
    expected_approx = 88
    coverage = round(100.0 * total / expected_approx, 1) if total else 0.0
    print(f"  Total records: {total}")
    print(f"  Expected (approx): {expected_approx}")
    print(f"  Coverage (approx): {coverage}%")

    pin_names = []
    for r in records:
        if not isinstance(r, dict):
            continue
        n = r.get("name")
        if n:
            pin_names.append(str(n))
    unique_names = len(set(pin_names))
    print(f"  Unique pin names: {unique_names}")

    return {"total": total, "expected": expected_approx,
            "coverage_pct": coverage, "unique_names": unique_names}


def main():
    print("=== DATA INTEGRITY AUDIT (read-only) ===")
    print(f"ROOT: {ROOT}")

    r01 = audit_dat_01()
    r02 = audit_dat_02()
    r03 = audit_dat_03()
    r07 = audit_dat_07()

    print("\n=== SUMMARY ===")
    if r01["total"] > 0:
        pct_bad = round(100.0 * r01["without_plus"] / r01["total"], 1)
        print(f"  dat_01: {r01['without_plus']} of {r01['total']} ({pct_bad}%) lack '+' prefix")
    print(f"  dat_02: {r02['suspected']} records self-marked as suspected")
    print(f"  dat_03: {r03['duplicates']} duplicate (error_type, code) pairs")
    print(f"  dat_07: {r07['total']} pins ({r07['coverage_pct']}% of ~{r07['expected']})")

    print("\n  NO data files were modified.")
    print("  See reports/DATA_INTEGRITY_REPORT.md for details.")
    return 0


if __name__ == "__main__":
    sys.exit(main())