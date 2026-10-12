#!/usr/bin/env python3
"""Cross-reference validation for the sim800l-data project (v9).

Strict mode: commands referenced elsewhere must be DEFINED as their own
record in dat_01 (via the `command:` field).

Soft mode: if a command is only mentioned in dat_01's `related_commands`
of some other record (but not defined standalone), it is reported as
INFO, not as an error.

AT commands are normalized:
    "AT+CMGS"  ->  "CMGS"
    "+CMGS"    ->  "CMGS"
    "at+cmgs"  ->  "CMGS"
    "CMGS=1"   ->  "CMGS"
"""
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[FATAL] PyYAML not installed", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


def normalize_cmd(c) -> str:
    if c is None:
        return ""
    s = str(c).strip().upper()
    if not s:
        return ""
    if s.startswith("AT+"):
        s = s[3:]
    elif s.startswith("AT"):
        rest = s[2:]
        if rest and (rest[0] == "+" or rest[0].isalnum()):
            s = rest
    if s.startswith("+"):
        s = s[1:]
    m = re.match(r"[A-Z0-9_]+", s)
    return m.group(0) if m else s


def load_all():
    datasets = {}
    for path in sorted(DATA_DIR.glob("dat_*.yaml")):
        try:
            with path.open("r", encoding="utf-8") as fh:
                datasets[path.stem] = yaml.safe_load(fh) or []
        except Exception as exc:
            print(f"[WARN] Cannot load {path.name}: {exc}", file=sys.stderr)
            datasets[path.stem] = []
    return datasets


def as_list(x):
    if x is None:
        return []
    if isinstance(x, list):
        return x
    return [x]


def find(datasets, prefix):
    for name, data in datasets.items():
        if name.startswith(prefix):
            return name, data
    return None, []


def main():
    datasets = load_all()
    print(f"Loaded {len(datasets)} dataset file(s).")

    _, dat01 = find(datasets, "dat_01")
    _, dat02 = find(datasets, "dat_02")
    _, dat03 = find(datasets, "dat_03")
    _, dat05 = find(datasets, "dat_05")
    _, dat07 = find(datasets, "dat_07")

    # STRICT: commands defined standalone in dat_01
    strict_set = set()
    # SOFT: commands mentioned in related_commands of dat_01
    soft_set = set()

    for r in as_list(dat01):
        if not isinstance(r, dict):
            continue
        if r.get("command"):
            k = normalize_cmd(r["command"])
            if k:
                strict_set.add(k)
        for rc in as_list(r.get("related_commands")):
            k = normalize_cmd(rc)
            if k:
                soft_set.add(k)

    state_set = set()
    for r in as_list(dat05):
        if isinstance(r, dict) and r.get("state_name"):
            state_set.add(str(r["state_name"]).upper())

    pin_set = set()
    for r in as_list(dat07):
        if isinstance(r, dict) and r.get("name"):
            pin_set.add(str(r["name"]).upper())

    print(f"  Strict commands (defined)        : {len(strict_set)}")
    print(f"  Soft commands (related_commands) : {len(soft_set)}")
    print(f"  States indexed                   : {len(state_set)}")
    print(f"  Pins indexed                     : {len(pin_set)}")

    strict_issues = 0
    soft_issues = 0

    def check_cmd(c, label):
        nonlocal strict_issues, soft_issues
        k = normalize_cmd(c)
        if not k:
            return
        if k in strict_set:
            return
        if k in soft_set:
            print(f"[INFO] {label}: command {c} defined via related_commands (soft match)", file=sys.stderr)
            soft_issues += 1
        else:
            print(f"[WARN] {label}: command {c} not in dat_01 (strict)", file=sys.stderr)
            strict_issues += 1

    for idx, r in enumerate(as_list(dat02)):
        if not isinstance(r, dict):
            continue
        c = r.get("related_command")
        if c:
            check_cmd(c, f"dat_02[{idx}]")
        s = r.get("related_state")
        if s and state_set and str(s).upper() not in state_set:
            print(f"[WARN] dat_02[{idx}]: state {s} not in dat_05", file=sys.stderr)
            strict_issues += 1

    for idx, r in enumerate(as_list(dat03)):
        if not isinstance(r, dict):
            continue
        for c in as_list(r.get("related_commands")):
            if c:
                check_cmd(c, f"dat_03[{idx}]")

    print()
    print(f"Strict issues : {strict_issues}")
    print(f"Soft issues   : {soft_issues}")
    print(f"Total issues  : {strict_issues + soft_issues}")
    print(f"\nCross-reference check complete. Strict={strict_issues}  Soft={soft_issues}")
    return 0


if __name__ == "__main__":
    sys.exit(main())