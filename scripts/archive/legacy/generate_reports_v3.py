#!/usr/bin/env python3
"""تولید dat_XX_REPORT کامل + گزارش‌های مدیریتی."""
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

META = {
"01":("AT Command DB","AT Command Manual V1.01","dat_01_at_command.yaml"),
"02":("URC DB","AT Command Manual V1.01","dat_02_urc.yaml"),
"03":("Error Code DB (CME/CMS)","AT Command Manual V1.01","dat_03_error_code.yaml"),
"04":("Timing & Timeout DB","Hardware V1.00 + V2.02","dat_04_timing_timeout.yaml"),
"05":("State Machine DB","AT Manual + Hardware (inferred)","dat_05_state_machine.yaml"),
"06":("Init Sequence DB","AT Manual (inferred)","dat_06_init_sequence.yaml"),
"07":("Hardware Reference DB","Hardware V1.00 + V2.02","dat_07_hardware_reference.yaml"),
"08":("Firmware Compatibility Matrix","—","dat_08_firmware_compatibility.yaml"),
"09":("SMS DB","AT Manual V1.01","dat_09_sms.yaml"),
"10":("GPRS/Data DB","AT Manual V1.01","dat_10_gprs_data.yaml"),
"11":("HTTP/FTP/SSL DB","AT Manual V1.01","dat_11_http_ftp_ssl.yaml"),
"12":("Audio DB","AT Manual V1.01","dat_12_audio.yaml"),
"13":("SIM Management DB","AT Manual V1.01","dat_13_sim_management.yaml"),
"14":("Operator/APN DB","mcc-mnc.com (external)","dat_14_operator_apn.yaml"),
"15":("Power Management DB","AT Manual + Hardware","dat_15_power_management.yaml"),
"16":("Board/EVB Definitions","—","dat_16_board_evb.yaml"),
"17":("Certificate/Key Store","AT Manual V1.01","dat_17_certificate_key_store.yaml"),
"18":("Certification Data","—","dat_18_certification.yaml"),
}

def count_file(name):
    p = DATA / name
    if not p.exists(): return 0
    try:
        with open(p, encoding="utf-8") as f:
            return len(yaml.safe_load(f) or [])
    except Exception:
        return 0

def determine_status(num, n):
    if n == 0:
        if num in ("08","18"): return "blocked"
        if num == "16": return "deferred"
        return "blocked"
    if num in ("04","05","06","07","15"):
        # اگر پوشش خوب بود complete، وگرنه partial
        if n >= 20: return "complete"
        return "partial"
    if num == "14": return "external"
    if num == "17" and n >= 5: return "partial"
    return "partial"

def coverage_estimate(num, n):
    if n == 0: return "low"
    if num in ("01",) and n >= 200: return "high"
    if num in ("02",) and n >= 40: return "medium"
    if num in ("03",) and n >= 100: return "medium"
    if num in ("04",) and n >= 20: return "high"
    if num in ("07",) and n >= 50: return "high"
    if num in ("10",) and n >= 25: return "high"
    if num in ("11",) and n >= 30: return "high"
    if num in ("14",) and n >= 50: return "medium"
    return "medium"

def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    counts = {num: count_file(META[num][2]) for num in META}

    # dat_XX_REPORT
    for num in sorted(META.keys()):
        name, src, fname = META[num]
        n = counts[num]
        st = determine_status(num, n)
        cov = coverage_estimate(num, n)
        if n == 0 and st in ("blocked","deferred"):
            reason = "منبع رسمی در دیسک موجود نیست"
            plan = "تهیه منبع رسمی و سپس استخراج"
        elif n > 0:
            reason = "استخراج‌شده از منابع موجود"
            plan = "تکمیل با منابع جدیدتر یا جدول‌کشی دقیق‌تر"
        else:
            reason = "—"
            plan = "—"

        content = f"""# dat_{num}_REPORT — {name}

- **وضعیت**: `{st}`
- **تعداد رکورد**: {n}
- **منبع اصلی**: {src}
- **coverage_estimate**: `{cov}`
- **تاریخ تولید گزارش**: {NOW}

## دلیل وضعیت
{reason}

## برنامه تکمیل
{plan}

## منابع مرتبط
- به `SOURCE_INVENTORY.md` مراجعه شود
- به `GAP_REPORT.md` مراجعه شود

## یادداشت
این گزارش به صورت خودکار از `data/{fname}` تولید شده است.
"""
        (REPORTS / f"dat_{num}_REPORT.md").write_text(content, encoding="utf-8")

    # COVERAGE_MATRIX
    lines = [f"# COVERAGE_MATRIX", f"> auto-generated at {NOW}", "",
             "| دیتاست | نام | status | تعداد رکورد | coverage_estimate | منبع |",
             "|---|---|---|---|---|---|"]
    for num in sorted(META.keys()):
        name, src, _ = META[num]
        st = determine_status(num, counts[num])
        cov = coverage_estimate(num, counts[num])
        lines.append(f"| dat_{num} | {name} | {st} | {counts[num]} | {cov} | {src} |")
    (ROOT / "COVERAGE_MATRIX.md").write_text("\n".join(lines), encoding="utf-8")

    print("گزارش‌ها نوشته شدند")
    return 0

if __name__ == "__main__":
    sys.exit(main())