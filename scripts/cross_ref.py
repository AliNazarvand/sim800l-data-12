#!/usr/bin/env python3
"""Cross-reference validation for the sim800l-data project."""
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[FATAL] PyYAML not installed", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


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
    return x if isinstance(x, list) else ([] if x is None else [x])


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

    cmd_set = set()
    for r in as_list(dat01):
        if isinstance(r, dict) and r.get("command"):
            cmd_set.add(r["command"])
            cmd_set.add(r["command"].lstrip("+"))
    state_set = set()
    for r in as_list(dat05):
        if isinstance(r, dict) and r.get("state_name"):
            state_set.add(r["state_name"])
    pin_set = set()
    for r in as_list(dat07):
        if isinstance(r, dict) and r.get("name"):
            pin_set.add(r["name"])

    print(f"  Commands indexed : {len(cmd_set)}")
    print(f"  States indexed   : {len(state_set)}")
    print(f"  Pins indexed     : {len(pin_set)}")

    issues = 0

    # URC -> command + state
    for idx, r in enumerate(as_list(dat02)):
        if not isinstance(r, dict):
            continue
        c = r.get("related_command")
        if c and cmd_set and c not in cmd_set and c.lstrip("+") not in cmd_set:
            print(f"[WARN] dat_02[{idx}]: command {c} not in dat_01", file=sys.stderr)
            issues += 1
        s = r.get("related_state")
        if s and state_set and s not in state_set:
            print(f"[WARN] dat_02[{idx}]: state {s} not in dat_05", file=sys.stderr)
            issues += 1

    # Errors -> command
    for idx, r in enumerate(as_list(dat03)):
        if not isinstance(r, dict):
            continue
        for c in as_list(r.get("related_commands")):
            if c and cmd_set and c not in cmd_set and c.lstrip("+") not in cmd_set:
                print(f"[WARN] dat_03[{idx}]: command {c} not in dat_01", file=sys.stderr)
                issues += 1

    print(f"\nCross-reference check complete. Issues: {issues}")
    return 0


if __name__ == "__main__":
    sys.exit(main())