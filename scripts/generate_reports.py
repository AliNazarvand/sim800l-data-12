#!/usr/bin/env python3
"""تولید گزارش‌های مدیریتی و dat_XX_REPORT از داده واقعی."""
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

DATASETS = {
"01":("AT Command DB","AT Command Manual V1.01"),
"02":("URC DB","AT Command Manual V1.01"),
"03":("Error Code DB (CME/CMS)","AT Command Manual V1.01"),
"04":("Timing & Timeout DB","Hardware V1.00 + V2.02"),
"05":("State Machine DB","Hardware V1.00 + V2.02"),
"06":("Init Sequence DB","AT Manual + Hardware"),
"07":("Hardware Reference DB","Hardware V1.00 + V2.02"),
"08":("Firmware Compatibility Matrix","—"),
"09":("SMS DB","AT Command Manual V1.01"),
"10":("GPRS/Data DB","AT Command Manual V1.01"),
"11":("HTTP/FTP/SSL DB","AT Command Manual V1.01"),
"12":("Audio DB","AT Command Manual V1.01"),
"13":("SIM Management DB","AT Command Manual V1.01"),
"14":("Operator/APN DB (MCC/MNC)","—"),
"15":("Power Management DB","Hardware V1.00 + V2.02"),
"16":("Board/EVB Definitions","—"),
"17":("Certificate/Key Store","AT Command Manual V1.01"),
"18":("Certification Data","—"),
}

FILES = {
"01":"dat_01_at_command.yaml","02":"dat_02_urc.yaml","03":"dat_03_error_code.yaml",
"04":"dat_04_timing_timeout.yaml","05":"dat_05_state_machine.yaml","06":"dat_06_init_sequence.yaml",
"07":"dat_07_hardware_reference.yaml","08":"dat_08_firmware_compatibility.yaml",
"09":"dat_09_sms.yaml","10":"dat_10_gprs_data.yaml","11":"dat_11_http_ftp_ssl.yaml",
"12":"dat_12_audio.yaml","13":"dat_13_sim_management.yaml","14":"dat_14_operator_apn.yaml",
"15":"dat_15_power_management.yaml","16":"dat_16_board_evb.yaml",
"17":"dat_17_certificate_key_store.yaml","18":"dat_18_certification.yaml",
}

def count(name):
    p = DATA / name
    if not p.exists(): return 0
    try:
        with open(p, encoding="utf-8") as f:
            return len(yaml.safe_load(f) or [])
    except Exception:
        return 0

def status_for(num, n):
    if n == 0:
        if num in ("08","16","18"): return "blocked"
        return "blocked"
    if num in ("04","05","06","07","15"): return "complete"
    return "partial"

def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    counts = {num: count(FILES[num]) for num in DATASETS}

    for num in sorted(DATASETS.keys()):
        name, src = DATASETS[num]
        n = counts[num]
        st = status_for(num, n)
        content = f"""# dat_{num}_REPORT — {name}

- **وضعیت**: `{st}`
- **تعداد رکورد**: {n}
- **منبع اصلی**: {src}
- **تاریخ تولید**: {NOW}

## یادداشت
این گزارش به صورت خودکار از داده واقعی موجود در `data/{FILES[num]}` تولید شده است.

## وابستگی‌ها
برای جزئیات بیشتر: `COVERAGE_MATRIX.md`, `TODO.md`, `DECISIONS_LOG.md`, `CROSS_REF_REPORT.md`
"""
        (REPORTS / f"dat_{num}_REPORT.md").write_text(content, encoding="utf-8")

    # COVERAGE_MATRIX
    lines = ["# COVERAGE_MATRIX — وضعیت واقعی دیتاست‌ها\n",
             f"> auto-generated at {NOW}\n",
             "| دیتاست | نام | status | تعداد رکورد | منبع |",
             "|---|---|---|---|---|"]
    for num in sorted(DATASETS.keys()):
        name, src = DATASETS[num]
        st = status_for(num, counts[num])
        lines.append(f"| dat_{num} | {name} | {st} | {counts[num]} | {src} |")
    (ROOT / "COVERAGE_MATRIX.md").write_text("\n".join(lines), encoding="utf-8")

    print("✅ گزارش‌ها تولید شدند")
    return 0

if __name__ == "__main__":
    sys.exit(main())