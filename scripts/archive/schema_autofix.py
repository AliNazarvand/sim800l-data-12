#!/usr/bin/env python3
"""
schema_autofix.py — هر schema را با فیلدهای واقعی داده هم‌راستا می‌کند
و additionalProperties: false اضافه می‌کند.

گزارش: reports/SCHEMA_AUTOFIX_REPORT.md
"""
import json
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

try:
    import yaml as _yaml
except ImportError:
    print("[FATAL] PyYAML not installed"); sys.exit(2)


def load_yaml(p):
    return _yaml.safe_load(p.read_text(encoding="utf-8"))


def dump_yaml(p, obj):
    p.write_text(_yaml.safe_dump(obj, allow_unicode=True, sort_keys=False),
                 encoding="utf-8")


def records_of(path):
    try:
        obj = load_yaml(path)
    except Exception:
        return []
    if isinstance(obj, list): return obj
    if isinstance(obj, dict):
        for _k, v in obj.items():
            if isinstance(v, list): return v
    return []


def py_type(v):
    if v is None: return "null"
    if isinstance(v, bool): return "boolean"
    if isinstance(v, int): return "integer"
    if isinstance(v, float): return "number"
    if isinstance(v, str): return "string"
    if isinstance(v, list): return "array"
    if isinstance(v, dict): return "object"
    return "string"


def infer_schema(types_set, sample_value):
    types = set(types_set)
    if "array" in types:
        item_types = set()
        if isinstance(sample_value, list):
            for it in sample_value:
                item_types.add(py_type(it))
        item_types.discard("null")
        if not item_types: item_types = {"string"}
        return {"type": "array", "items": {"type": sorted(item_types)}}
    if "object" in types:
        return {"type": "object"}
    if len(types) == 1:
        return {"type": types.pop()}
    return {"type": sorted(types)}


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    lines = ["# SCHEMA AUTOFIX REPORT", "",
             "| دیتاست | فیلدهای افزوده‌شده | additionalProperties |",
             "|---|---|---|"]
    total_added = 0
    for folder, dat_id in sorted(DATASET_FOLDERS.items(), key=lambda x: x[1]):
        sp = SCHEMAS / f"{dat_id}.schema.yaml"
        if not sp.exists(): continue
        schema = load_yaml(sp)
        if not isinstance(schema, dict): continue
        props = schema.setdefault("properties", {})

        # جمع‌آوری فیلدها + نمونه‌ها
        seen = {}  # field -> (types_set, sample)
        folder_path = DATA / folder
        if folder_path.exists():
            for f in sorted(folder_path.rglob("*.yaml")):
                if f.name.startswith("_dataset_meta"): continue
                for rec in records_of(f):
                    if not isinstance(rec, dict): continue
                    for k, v in rec.items():
                        if k not in seen:
                            seen[k] = (set(), v)
                        seen[k][0].add(py_type(v))

        added = []
        for k, (tset, sample) in seen.items():
            if k not in props:
                props[k] = infer_schema(tset, sample)
                added.append(k)

        schema["additionalProperties"] = False
        dump_yaml(sp, schema)
        total_added += len(added)
        lines.append(f"| {dat_id} | {', '.join(added) if added else '—'} | false |")

    lines += ["", f"کل فیلدهای افزوده‌شده: {total_added}"]
    out = REPORTS / "SCHEMA_AUTOFIX_REPORT.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK]   {out.relative_to(ROOT)}  ({total_added} fields added)")
    return 0


if __name__ == "__main__":
    sys.exit(main())