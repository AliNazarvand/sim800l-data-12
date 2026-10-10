#!/usr/bin/env python3
"""
clean_schemas.py — حذف فیلدهای تکراری مفرد از schemaها.

فقط فیلدهایی که:
  * در schema وجود دارند
  * در داده‌ی واقعی استفاده نمی‌شوند
  * نسخه‌ی جمع معادلشان در داده هست
حذف می‌شوند.

گزارش: reports/SCHEMA_CLEAN_REPORT.md
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

DATASET_FOLDERS = {
    "at_commands": "dat_01", "urc": "dat_02", "error_codes": "dat_03",
    "timing": "dat_04", "state_machine": "dat_05", "init_sequence": "dat_06",
    "hardware": "dat_07", "firmware_compat": "dat_08", "sms": "dat_09",
    "gprs_data": "dat_10", "http_ftp_ssl": "dat_11", "audio": "dat_12",
    "sim_management": "dat_13", "operator_apn": "dat_14",
    "power_management": "dat_15", "board_evb": "dat_16",
    "certificate_keystore": "dat_17", "certification": "dat_18",
}

# فیلدهای مفرد که باید حذف شوند (نسخه‌ی جمع معنادارتر است)
SINGULAR_TO_REMOVE = {
    "dat_04": ["related_command", "related_state", "related_urc"],
    "dat_05": [],
    "dat_02": ["related_command", "related_state"],
}
# فیلدهای زائد که هرگز پر نمی‌شوند
EXTRA_TO_REMOVE = {
    "dat_04": ["parameter"],   # parameter_id + parameter_name کافی است
    "dat_06": ["step_order"],  # step_number کافی است
}

try:
    import yaml as _yaml
except ImportError:
    print("[FATAL] PyYAML not installed"); sys.exit(2)


def load_yaml(p): return _yaml.safe_load(p.read_text(encoding="utf-8"))
def dump_yaml(p, obj): p.write_text(_yaml.safe_dump(obj, allow_unicode=True, sort_keys=False), encoding="utf-8")


def records_of(path):
    try: obj = load_yaml(path)
    except Exception: return []
    if isinstance(obj, list): return obj
    if isinstance(obj, dict):
        for _k, v in obj.items():
            if isinstance(v, list): return v
    return []


def fields_in_data(folder):
    """فیلدهای واقعاً استفاده‌شده در داده‌ی یک دیتاست."""
    used = set()
    fp = DATA / folder
    if not fp.exists(): return used
    for f in fp.rglob("*.yaml"):
        if f.name.startswith("_dataset_meta"): continue
        for rec in records_of(f):
            if isinstance(rec, dict):
                used.update(rec.keys())
    return used


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = ["# SCHEMA CLEAN REPORT", "",
             "| دیتاست | فیلدهای حذف‌شده | فیلدهای افزوده (از داده) |",
             "|---|---|---|"]
    total_removed = 0
    total_added = 0
    for folder, dat_id in sorted(DATASET_FOLDERS.items(), key=lambda x: x[1]):
        sp = SCHEMAS / f"{dat_id}.schema.yaml"
        if not sp.exists(): continue
        schema = load_yaml(sp)
        if not isinstance(schema, dict): continue
        props = schema.get("properties", {})
        if not isinstance(props, dict): continue

        used = fields_in_data(folder)

        removed = []
        # حذف فیلدهای مفرد/زائد
        to_remove = SINGULAR_TO_REMOVE.get(dat_id, []) + EXTRA_TO_REMOVE.get(dat_id, [])
        for k in to_remove:
            if k in props and k not in used:
                del props[k]
                removed.append(k)

        added = []
        # فیلدهای داده که در schema نیستند — هشدار: این باید دستی انجام شود
        # ولی برای سازگاری، اینجا فقط گزارش می‌کنیم
        for k in used:
            if k not in props:
                added.append(k)

        schema["properties"] = props
        dump_yaml(sp, schema)
        total_removed += len(removed)
        total_added += len(added)
        lines.append(f"| {dat_id} | {', '.join(removed) if removed else '—'} | "
                     f"{', '.join(added) if added else '—'} |")

    lines += ["", f"کل فیلدهای حذف‌شده: {total_removed}",
              f"کل فیلدهای داده که در schema نیستند: {total_added}"]
    out = REPORTS / "SCHEMA_CLEAN_REPORT.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK]   {out.relative_to(ROOT)}  (removed: {total_removed}, missing: {total_added})")
    return 0


if __name__ == "__main__":
    sys.exit(main())