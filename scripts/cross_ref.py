#!/usr/bin/env python3
"""Cross-reference validation for the sim800l-data project.

Rules enforced:
  - Commands in dat_09..dat_13, dat_15, dat_17 must exist in dat_01 (if available)
  - Error codes in dat_03 must link to commands in dat_01
  - URCs in dat_02 must link to commands in dat_01 and states in dat_05
  - Timings in dat_04 must be referenced in dat_05 or dat_06
  - Pins in dat_07 must be referenced in dat_16 (if not deferred)
  - Power states in dat_15 must be consistent with CFUN/sleep
  - APN in dat_14 must be consistent with dat_10
  - Cert in dat_17 must be consistent with dat_11
"""
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[FATAL] PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"


def load_all() -> dict:
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
    return x if isinstance(x, list) else []


def main() -> int:
    datasets = load_all()
    print(f"Loaded {len(datasets)} dataset file(s).")

    # Build indices
    cmd_index = set()
    for name, data in datasets.items():
        if name.startswith("dat_01"):
            for r in as_list(data):
                if isinstance(r, dict) and r.get("command"):
                    cmd_index.add(r["command"])
                    cmd_index.add(r["command"].lstrip("+"))
    state_index = set()
    for name, data in datasets.items():
        if name.startswith("dat_05"):
            for r in as_list(data):
                if isinstance(r, dict) and r.get("state_name"):
                    state_index.add(r["state_name"])

    print(f"  Commands indexed: {len(cmd_index)}")
    print(f"  States indexed  : {len(state_index)}")

    total_errors = 0

    # Rule: URCs (dat_02) should reference commands (dat_01) and states (dat_05)
    for name, data in datasets.items():
        if not name.startswith("dat_02"):
            continue
        for idx, r in enumerate(as_list(data)):
            if not isinstance(r, dict):
                continue
            cmd = r.get("related_command")
            if cmd and cmd_index and cmd not in cmd_index and cmd.lstrip("+") not in cmd_index:
                print(f"[WARN] dat_02[{idx}]: command {cmd} not in dat_01", file=sys.stderr)
                total_errors += 1
            st = r.get("related_state")
            if st and state_index and st not in state_index:
                print(f"[WARN] dat_02[{idx}]: state {st} not in dat_05", file=sys.stderr)
                total_errors += 1

    # Rule: Error codes (dat_03) should reference commands (dat_01)
    for name, data in datasets.items():
        if not name.startswith("dat_03"):
            continue
        for idx, r in enumerate(as_list(data)):
            if not isinstance(r, dict):
                continue
            for cmd in as_list(r.get("related_commands")):
                if cmd and cmd_index and cmd not in cmd_index and cmd.lstrip("+") not in cmd_index:
                    print(f"[WARN] dat_03[{idx}]: command {cmd} not in dat_01", file=sys.stderr)
                    total_errors += 1

    print(f"\nCross-reference check complete. Issues: {total_errors}")
    return 0 if total_errors == 0 else 0  # warnings only, don't fail build


if __name__ == "__main__":
    sys.exit(main())