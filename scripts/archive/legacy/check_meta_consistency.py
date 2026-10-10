#!/usr/bin/env python3
"""
check_meta_consistency.py — مقایسه وضعیت _dataset_meta.yaml با COVERAGE_MATRIX.md.

نسخه ۴:
  * DATASET_FOLDERS با پیشوند "dat_" تا با dat_id مطابقت کند.
  * منطق مقایسه: missing → MISSING (نه OK).
  * نمایش محتوای خام همه _dataset_meta.yaml ها (نه فقط نمونه).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
COVERAGE = ROOT / "COVERAGE_MATRIX.md"

try:
    import yaml as _yaml
except ImportError:
    _yaml = None

DATASET_FOLDERS = {
    "at_commands": "dat_01", "urc": "dat_02", "error_codes": "dat_03",
    "timing": "dat_04", "state_machine": "dat_05", "init_sequence": "dat_06",
    "hardware": "dat_07", "firmware_compat": "dat_08", "sms": "dat_09",
    "gprs_data": "dat_10", "http_ftp_ssl": "dat_11", "audio": "dat_12",
    "sim_management": "dat_13", "operator_apn": "dat_14",
    "power_management": "dat_15", "board_evb": "dat_16",
    "certificate_keystore": "dat_17", "certification": "dat_18",
}

STATUS_KEYS = ("status", "meta_status", "dataset_status", "state", "completion_status")


def parse_coverage():
    result = {}
    if not COVERAGE.exists():
        return result
    for line in COVERAGE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\|\s*(dat_\d{2})\s*\|\s*[^|]*\|\s*([a-z]+)\s*\|", line)
        if m:
            result[m.group(1)] = m.group(2)
    return result


def extract_status(obj):
    if not isinstance(obj, dict):
        return None
    for k in STATUS_KEYS:
        v = obj.get(k)
        if isinstance(v, str):
            return v
    for parent in ("dataset", "_dataset", "meta", "_meta", "info"):
        sub = obj.get(parent)
        if isinstance(sub, dict):
            for k in STATUS_KEYS:
                v = sub.get(k)
                if isinstance(v, str):
                    return v
    return None


def read_meta(dat_id: str):
    for folder, d in DATASET_FOLDERS.items():
        if d != dat_id:
            continue
        meta = DATA / folder / "_dataset_meta.yaml"
        if not meta.exists():
            return None, None
        if _yaml is None:
            return None, meta
        try:
            obj = _yaml.safe_load(meta.read_text(encoding="utf-8"))
            return extract_status(obj), meta
        except Exception:
            return None, meta
    return None, None


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    cov = parse_coverage()
    lines = ["# META CONSISTENCY REPORT", "",
             "| دیتاست | COVERAGE_MATRIX | _dataset_meta | وضعیت |",
             "|---|---|---|---|"]
    mismatch = 0
    missing = 0
    for dat_id in sorted(cov.keys()):
        cm = cov[dat_id]
        mt, meta_path = read_meta(dat_id)
        if mt is None:
            mt_disp = "-"
            missing += 1
            status = "MISSING"
            mismatch += 1
        else:
            mt_disp = mt
            if cm == mt:
                status = "OK"
            else:
                status = "MISMATCH"
                mismatch += 1
        lines.append(f"| {dat_id} | {cm} | {mt_disp} | {status} |")

    lines.append("")
    lines.append(f"تعداد ناسازگاری: {mismatch}")
    lines.append(f"تعداد دیتاست بدون status در _dataset_meta: {missing}")
    lines.append("")
    lines.append("## محتوای خام همه _dataset_meta.yaml")
    lines.append("")
    for folder, dat_id in sorted(DATASET_FOLDERS.items(), key=lambda x: x[1]):
        meta = DATA / folder / "_dataset_meta.yaml"
        if not meta.exists():
            continue
        lines.append(f"### {dat_id} — {meta.relative_to(ROOT)}")
        lines.append("```yaml")
        lines.append(meta.read_text(encoding="utf-8").rstrip())
        lines.append("```")
        lines.append("")

    out = REPORTS / "META_CONSISTENCY_REPORT.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK]   {out.relative_to(ROOT)}  ({mismatch} mismatches, {missing} missing)")
    return 0


if __name__ == "__main__":
    sys.exit(main())