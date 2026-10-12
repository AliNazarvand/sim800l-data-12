#!/usr/bin/env python3
"""Preflight checks for sim800l-data."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIRS = ["schemas", "data", "reports", "scripts", "sources", "docs", "tools"]
SCHEMAS = [f"dat_{i:02d}.schema.yaml" for i in range(1, 19)]
DATAS = [
    "dat_01_at_command.yaml", "dat_02_urc.yaml", "dat_03_error_code.yaml",
    "dat_04_timing_timeout.yaml", "dat_05_state_machine.yaml",
    "dat_06_init_sequence.yaml", "dat_07_hardware_reference.yaml",
    "dat_08_firmware_compatibility.yaml", "dat_09_sms.yaml",
    "dat_10_gprs_data.yaml", "dat_11_http_ftp_ssl.yaml",
    "dat_12_audio.yaml", "dat_13_sim_management.yaml",
    "dat_14_operator_apn.yaml", "dat_15_power_management.yaml",
    "dat_16_board_evb.yaml", "dat_17_certificate_key_store.yaml",
    "dat_18_certification.yaml",
]


def check():
    missing = []
    for d in DIRS:
        if not (ROOT / d).is_dir():
            missing.append(f"dir: {d}")
    for s in SCHEMAS:
        if not (ROOT / "schemas" / s).exists():
            missing.append(f"schema: {s}")
    for d in DATAS:
        if not (ROOT / "data" / d).exists():
            missing.append(f"data: {d}")
    if missing:
        print("[FAIL] Missing:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1
    print("[PASS] All required artifacts present.")
    return 0


if __name__ == "__main__":
    sys.exit(check())