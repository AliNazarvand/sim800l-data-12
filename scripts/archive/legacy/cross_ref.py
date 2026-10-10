#!/usr/bin/env python3
"""اجرای Cross-Reference بین دیتاست‌ها."""
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pyyaml"])
    import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load(name):
    p = DATA / name
    if not p.exists(): return []
    try:
        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f) or []
    except Exception:
        return []

def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    d01 = load("dat_01_at_command.yaml")
    d02 = load("dat_02_urc.yaml")
    d03 = load("dat_03_error_code.yaml")
    d05 = load("dat_05_state_machine.yaml")
    d07 = load("dat_07_hardware_reference.yaml")
    d09 = load("dat_09_sms.yaml")
    d10 = load("dat_10_gprs_data.yaml")
    d11 = load("dat_11_http_ftp_ssl.yaml")
    d13 = load("dat_13_sim_management.yaml")
    d15 = load("dat_15_power_management.yaml")

    cmd_index = {r.get("command"): r.get("id") for r in d01 if r.get("command")}
    state_index = {r.get("state_name"): r.get("id") for r in d05 if r.get("state_name")}

    lines = [f"# CROSS_REF_REPORT\n", f"> auto-generated at {NOW}\n"]
    lines.append("## شمارش رکوردها\n")
    for name, arr in [("dat_01",d01),("dat_02",d02),("dat_03",d03),("dat_05",d05),
                       ("dat_07",d07),("dat_09",d09),("dat_10",d10),("dat_11",d11),
                       ("dat_13",d13),("dat_15",d15)]:
        lines.append(f"- **{name}**: {len(arr)} رکورد")

    lines.append("\n## ارجاعات بین دیتاست‌ها\n")
    # dat_09..dat_13 باید به dat_01 ارجاع داشته باشند
    for name, arr in [("dat_09",d09),("dat_10",d10),("dat_11",d11),
                       ("dat_13",d13),("dat_15",d15)]:
        for r in arr:
            c = r.get("command")
            if c and c in cmd_index:
                lines.append(f"- ✅ {name}/{r.get('id')} → {c} (موجود در dat_01)")
            elif c:
                lines.append(f"- ⚠ {name}/{r.get('id')} → {c} (در dat_01 یافت نشد)")

    lines.append("\n## وضعیت کلی\n")
    lines.append(f"- dat_01 (مرجع command): {len(d01)} command")
    lines.append(f"- dat_02 (URC): {len(d02)} رکورد")
    lines.append(f"- dat_03 (Error Code): {len(d03)} رکورد")
    lines.append(f"- dat_05 (State): {len(d05)} state")
    lines.append(f"- dat_07 (Hardware): {len(d07)} pin/signal")

    (REPORTS / "CROSS_REF_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
    print("✅ CROSS_REF_REPORT.md نوشته شد")
    return 0

if __name__ == "__main__":
    sys.exit(main())