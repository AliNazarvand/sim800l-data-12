#!/usr/bin/env python3
"""
Cross-reference validator for sim800l-data.

Checks that every AT command referenced from dat_02 (URC), dat_09 (SMS),
and dat_13 (SIM Management) actually exists in dat_01 (AT Command DB).

Normalization: strips leading "AT+" or "AT" and then any leading "+",
finally uppercases. This makes "AT+CNMI", "+CNMI", and "cnmi" all equal.
"""
import sys
from pathlib import Path
import yaml

DATA = Path(__file__).resolve().parent.parent / "data"


def normalize(cmd):
    if cmd is None:
        return ""
    s = str(cmd).strip().upper()
    if s.startswith("AT+"):
        s = s[3:]
    elif s.startswith("AT"):
        s = s[2:]
    if s.startswith("+"):
        s = s[1:]
    return s


def load(path):
    if not path.exists():
        return []
    try:
        with path.open(encoding="utf-8") as f:
            data = yaml.safe_load(f)
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"[cross_ref] WARN: cannot read {path}: {e}", file=sys.stderr)
        return []


def main():
    dat01 = load(DATA / "dat_01_at_command.yaml")
    dat02 = load(DATA / "dat_02_urc.yaml")
    dat09 = load(DATA / "dat_09_sms.yaml")
    dat13 = load(DATA / "dat_13_sim_management.yaml")

    cmds = set()
    for r in dat01:
        if isinstance(r, dict):
            n = normalize(r.get("command"))
            if n:
                cmds.add(n)

    issues = []

    for r in dat02:
        if not isinstance(r, dict):
            continue
        rc = r.get("related_command")
        if rc:
            n = normalize(rc)
            if n and n not in cmds:
                issues.append(f"URC {r.get('id')} -> {rc} not in dat_01")

    for r in dat09:
        if not isinstance(r, dict):
            continue
        c = r.get("command")
        if c:
            n = normalize(c)
            if n and n not in cmds:
                issues.append(f"SMS {r.get('id')} -> {c} not in dat_01")

    for r in dat13:
        if not isinstance(r, dict):
            continue
        c = r.get("command")
        if c:
            n = normalize(c)
            if n and n not in cmds:
                issues.append(f"SIM {r.get('id')} -> {c} not in dat_01")

    print(f"Cross-ref: {len(issues)} issues, {len(dat01)} commands in dat_01")
    if issues:
        print()
        print(f"## Issues ({len(issues)})")
        for i in issues:
            print(f"- {i}")
    print()
    print("## Stats")
    print(f"- dat_01 commands: {len(dat01)}")
    print(f"- dat_02 URCs: {len(dat02)}")
    print(f"- dat_09 SMS: {len(dat09)}")
    print(f"- dat_13 SIM: {len(dat13)}")

    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())