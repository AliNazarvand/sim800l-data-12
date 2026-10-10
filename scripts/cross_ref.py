#!/usr/bin/env python3
"""cross_ref.py — بررسی ارجاعات متقابل (سبک) بین دیتاست‌ها"""
import yaml, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

def load(name):
    p = DATA / name
    if not p.exists(): return []
    try:
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or []
        return d if isinstance(d, list) else [d]
    except Exception:
        return []

def main():
    d01 = load("dat_01_at_command.yaml")
    commands = {r.get("command","") for r in d01 if isinstance(r, dict) and r.get("command")}
    d02 = load("dat_02_urc.yaml")
    d03 = load("dat_03_error_code.yaml")
    d09 = load("dat_09_sms.yaml")
    d13 = load("dat_13_sim_management.yaml")
    issues = []
    for u in d02:
        if not isinstance(u, dict): continue
        rc = u.get("related_command","")
        if rc and rc not in commands:
            issues.append(f"URC {u.get('id','?')} -> {rc} در dat_01 یافت نشد")
    for e in d03:
        if not isinstance(e, dict): continue
        for rc in e.get("related_commands", []) or []:
            if rc and rc not in commands:
                issues.append(f"Error {e.get('id','?')} -> {rc} در dat_01 یافت نشد")
    for s in d09:
        if not isinstance(s, dict): continue
        c = s.get("command","")
        if c and c not in commands:
            issues.append(f"SMS {s.get('id','?')} -> {c} در dat_01 یافت نشد")
    for s in d13:
        if not isinstance(s, dict): continue
        c = s.get("command","")
        if c and c not in commands:
            issues.append(f"SIM {s.get('id','?')} -> {c} در dat_01 یافت نشد")
    rp = ROOT / "reports" / "CROSS_REF_REPORT.md"
    lines = ["# CROSS_REF_REPORT", "", f"## مشکلات ({len(issues)})", ""]
    lines += [f"- {x}" for x in issues]
    lines += ["", "## آمار", f"- commandهای dat_01: {len(commands)}",
              f"- URCها: {len(d02)}", f"- Error codes: {len(d03)}",
              f"- SMS: {len(d09)}", f"- SIM: {len(d13)}"]
    rp.write_text("\n".join(lines), encoding="utf-8")
    print(f"Cross-ref: {len(issues)} issues, {len(commands)} commands in dat_01")
    sys.exit(0)

if __name__ == "__main__":
    main()