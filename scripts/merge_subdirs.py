#!/usr/bin/env python3
"""ادغام داده پوشه‌های فرعی data/*/ به فایل‌های اصلی dat_XX در ریشه data/."""
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pyyaml"])
    import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

MAPPING = {
    "hardware/pinout.yaml": "dat_07_hardware_reference.yaml",
    "hardware/electrical.yaml": "dat_07_hardware_reference.yaml",
    "hardware/power_consumption.yaml": "dat_07_hardware_reference.yaml",
    "hardware/rf_characteristics.yaml": "dat_07_hardware_reference.yaml",
    "hardware/physical.yaml": "dat_07_hardware_reference.yaml",
    "hardware/interfaces.yaml": "dat_07_hardware_reference.yaml",
    "timing/timing.yaml": "dat_04_timing_timeout.yaml",
    "urc/urc_at.yaml": "dat_02_urc.yaml",
    "urc/urc_hw.yaml": "dat_02_urc.yaml",
    "state_machine/states.yaml": "dat_05_state_machine.yaml",
    "state_machine/transitions.yaml": "dat_05_state_machine.yaml",
    "init_sequence/hardware_init.yaml": "dat_06_init_sequence.yaml",
    "power_management/power_modes.yaml": "dat_15_power_management.yaml",
    "sim_management/sim_management_at.yaml": "dat_13_sim_management.yaml",
    "sim_management/sim_management_hw.yaml": "dat_13_sim_management.yaml",
    "audio/audio_at.yaml": "dat_12_audio.yaml",
    "audio/audio_hw.yaml": "dat_12_audio.yaml",
    "http_ftp_ssl/http_ftp_ssl.yaml": "dat_11_http_ftp_ssl.yaml",
    "gprs_data/gprs_data.yaml": "dat_10_gprs_data.yaml",
    "sms/sms.yaml": "dat_09_sms.yaml",
    "error_codes/error_codes.yaml": "dat_03_error_code.yaml",
    "firmware_compat/firmware_compat.yaml": "dat_08_firmware_compatibility.yaml",
    "certification/certification.yaml": "dat_18_certification.yaml",
    "certificate_keystore/certificate_keystore.yaml": "dat_17_certificate_key_store.yaml",
    "board_evb/boards.yaml": "dat_16_board_evb.yaml",
    "operator_apn/operator_apn.yaml": "dat_14_operator_apn.yaml",
    "at_commands/at_commands.yaml": "dat_01_at_command.yaml",
}

def load_list(p):
    if not p.exists():
        return []
    try:
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        return d if isinstance(d, list) else []
    except Exception:
        return []

def main():
    total_added = 0
    for src_rel, dst_name in MAPPING.items():
        src = DATA / src_rel
        dst = DATA / dst_name
        if not src.exists():
            continue
        src_data = load_list(src)
        if not src_data:
            continue
        dst_data = load_list(dst)
        existing_ids = {r.get("id") for r in dst_data if isinstance(r, dict)}
        existing_cmds = {r.get("command") for r in dst_data if isinstance(r, dict) and r.get("command")}
        added = 0
        for r in src_data:
            if not isinstance(r, dict):
                continue
            rid = r.get("id")
            cmd = r.get("command")
            if rid and rid in existing_ids:
                continue
            if cmd and cmd in existing_cmds:
                continue
            dst_data.append(r)
            if rid: existing_ids.add(rid)
            if cmd: existing_cmds.add(cmd)
            added += 1
        if added:
            header = "# auto-merged from subfolder\n"
            body = yaml.safe_dump(dst_data, allow_unicode=True, sort_keys=False, default_flow_style=False)
            dst.write_text(header + body, encoding="utf-8")
            print(f"  merged {src_rel} -> {dst_name}: +{added}")
            total_added += added
    print(f"Total records merged: {total_added}")
    return 0

if __name__ == "__main__":
    sys.exit(main())