#!/usr/bin/env python3
"""تولید گزارش‌های نهایی v4 با آمار واقعی."""
import json
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
TABLES = ROOT / "sources" / "extracted" / "tables"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def count_records(fname):
    p = DATA / fname
    if not p.exists(): return 0
    try:
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        return len(d) if isinstance(d, list) else 0
    except Exception:
        return 0

FILES = {
    "01":"dat_01_at_command.yaml", "02":"dat_02_urc.yaml", "03":"dat_03_error_code.yaml",
    "04":"dat_04_timing_timeout.yaml","05":"dat_05_state_machine.yaml","06":"dat_06_init_sequence.yaml",
    "07":"dat_07_hardware_reference.yaml","08":"dat_08_firmware_compatibility.yaml",
    "09":"dat_09_sms.yaml","10":"dat_10_gprs_data.yaml","11":"dat_11_http_ftp_ssl.yaml",
    "12":"dat_12_audio.yaml","13":"dat_13_sim_management.yaml","14":"dat_14_operator_apn.yaml",
    "15":"dat_15_power_management.yaml","16":"dat_16_board_evb.yaml",
    "17":"dat_17_certificate_key_store.yaml","18":"dat_18_certification.yaml",
}

META = {
    "01":("AT Command DB","AT Command Manual V1.01"),
    "02":("URC DB","AT Command Manual V1.01"),
    "03":("Error Code DB (CME/CMS)","AT Command Manual V1.01"),
    "04":("Timing & Timeout DB","Hardware V1.00 + V2.02"),
    "05":("State Machine DB","AT Manual + Hardware"),
    "06":("Init Sequence DB","AT Manual + Hardware"),
    "07":("Hardware Reference DB","Hardware V1.00 + V2.02"),
    "08":("Firmware Compatibility Matrix","—"),
    "09":("SMS DB","AT Manual V1.01"),
    "10":("GPRS/Data DB","AT Manual V1.01"),
    "11":("HTTP/FTP/SSL DB","AT Manual V1.01"),
    "12":("Audio DB","AT Manual V1.01"),
    "13":("SIM Management DB","AT Manual V1.01"),
    "14":("Operator/APN DB","mcc-mnc.com (external)"),
    "15":("Power Management DB","AT Manual + Hardware"),
    "16":("Board/EVB Definitions","—"),
    "17":("Certificate/Key Store","AT Manual V1.01 / missing SSL"),
    "18":("Certification Data","—"),
}

def status_for(num, n):
    if n == 0:
        if num in ("08","18"): return "blocked"
        if num == "16": return "deferred"
        if num == "17": return "blocked"
        return "blocked"
    if num in ("04","07","15") and n >= (20 if num != "15" else 15): return "complete"
    if num in ("04","07","15"): return "partial"
    if num == "14": return "external"
    return "partial"

def cov_for(num, n):
    if n == 0: return "low"
    if num == "01" and n >= 200: return "high"
    if num == "02" and n >= 40: return "medium"
    if num == "03" and n >= 100: return "medium"
    if num == "04" and n >= 20: return "high"
    if num == "07" and n >= 50: return "high"
    if num == "10" and n >= 25: return "high"
    if num == "11" and n >= 30: return "high"
    if num == "14" and n >= 50: return "medium"
    if num == "15" and n >= 15: return "high"
    return "medium"

def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    counts = {num: count_records(FILES[num]) for num in FILES}
    table_count = len(list(TABLES.glob("*.csv"))) if TABLES.exists() else 0

    # dat_XX_REPORT
    for num in sorted(FILES.keys()):
        name, src = META[num]
        n = counts[num]
        st = status_for(num, n)
        cov = cov_for(num, n)
        content = f"""# dat_{num}_REPORT — {name}

- **وضعیت**: `{st}`
- **تعداد رکورد**: {n}
- **منبع اصلی**: {src}
- **coverage_estimate**: `{cov}`
- **تاریخ**: {NOW}

## یادداشت
این گزارش به‌صورت خودکار از داده واقعی موجود در `data/{FILES[num]}` تولید شده است.
"""
        (REPORTS / f"dat_{num}_REPORT.md").write_text(content, encoding="utf-8")

    # COVERAGE_MATRIX
    lines = [f"# COVERAGE_MATRIX", f"> auto-generated at {NOW}", "",
             "| دیتاست | نام | status | تعداد | coverage | منبع |",
             "|---|---|---|---|---|---|"]
    for num in sorted(FILES.keys()):
        name, src = META[num]
        lines.append(f"| dat_{num} | {name} | {status_for(num,counts[num])} | {counts[num]} | {cov_for(num,counts[num])} | {src} |")
    (ROOT / "COVERAGE_MATRIX.md").write_text("\n".join(lines), encoding="utf-8")

    # summary for PowerShell
    summary = {"counts": counts, "tables": table_count}
    (ROOT / "scripts" / "_v4_report_state.json").write_text(json.dumps(summary), encoding="utf-8")

    print(f"Reports regenerated. Tables remaining: {table_count}")
    for k in sorted(counts):
        print(f"  dat_{k}: {counts[k]}")
    return 0

if __name__ == "__main__":
    sys.exit(main())