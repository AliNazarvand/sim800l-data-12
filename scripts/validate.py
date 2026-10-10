#!/usr/bin/env python3
"""
validate.py — اعتبارسنجی چهار سطحی داده‌های پروژه sim800l-data (YAML only).

نسخه ۳:
  * فقط data/**/*.yaml را اعتبارسنجی می‌کند (JSON خروجی auto-generated است).
  * jsonschema.validate واقعی روی هر رکورد.
  * نگاشت پوشه به دیتاست.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = ROOT / "schemas"
DATA = ROOT / "data"

VALID_STATUSES = {"complete", "partial", "unknown", "inferred", "blocked", "deferred", "example-only"}
VALID_SOURCE_TYPES = {"primary", "secondary", "external"}

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
    print("[FATAL] PyYAML not installed")
    sys.exit(2)

try:
    import jsonschema
except ImportError:
    jsonschema = None


def load_yaml(p: Path):
    return _yaml.safe_load(p.read_text(encoding="utf-8"))


def load_schema(dat_id: str):
    y = SCHEMAS / f"{dat_id}.schema.yaml"
    j = SCHEMAS / f"{dat_id}.schema.json"
    if y.exists():
        return load_yaml(y)
    if j.exists():
        return json.loads(j.read_text(encoding="utf-8"))
    return None


def dataset_of(file_path: Path):
    try:
        rel = file_path.relative_to(DATA)
    except ValueError:
        return None
    if not rel.parts:
        return None
    return DATASET_FOLDERS.get(rel.parts[0])


def data_files():
    for f in sorted(DATA.rglob("*.yaml")):
        if f.name.startswith("_dataset_meta"):
            continue
        yield f


def iter_records():
    for f in data_files():
        dat = dataset_of(f)
        try:
            obj = load_yaml(f)
        except Exception as e:
            print(f"[FAIL] parse {f.relative_to(ROOT)}: {e}")
            continue
        if obj is None:
            continue
        if isinstance(obj, list):
            for rec in obj:
                yield f, dat, rec
        elif isinstance(obj, dict) and "id" in obj:
            yield f, dat, obj
        elif isinstance(obj, dict):
            for _k, v in obj.items():
                if isinstance(v, list):
                    for rec in v:
                        yield f, dat, rec


def level1_schema() -> int:
    errors = 0
    if jsonschema is None:
        print("[WARN] jsonschema not installed; L1 data validation skipped")
        return errors
    for f, dat, rec in iter_records():
        if not isinstance(rec, dict):
            continue
        if dat is None:
            continue
        sch = load_schema(dat)
        if sch is None:
            continue
        try:
            jsonschema.Draft7Validator(sch).validate(rec)
        except jsonschema.ValidationError as e:
            print(f"[FAIL] L1 {f.relative_to(ROOT)}: {e.message} (path={list(e.absolute_path)})")
            errors += 1
        except jsonschema.SchemaError as e:
            print(f"[FAIL] L1 schema {dat}: {e.message}")
            errors += 1
    return errors


def level2_business() -> int:
    errors = 0
    for f, _dat, rec in iter_records():
        if not isinstance(rec, dict):
            continue
        rid = rec.get("id")
        if not rid:
            print(f"[WARN] L2 {f.relative_to(ROOT)}: record missing id")
            continue
        st = rec.get("status")
        if st is not None and st not in VALID_STATUSES:
            print(f"[FAIL] L2 {f.name}:{rid}: invalid status {st!r}")
            errors += 1
        src = rec.get("source_type")
        if src is not None and src not in VALID_SOURCE_TYPES:
            print(f"[FAIL] L2 {f.name}:{rid}: invalid source_type {src!r}")
            errors += 1
        conf = rec.get("confidence")
        if conf is not None:
            try:
                c = float(conf)
                if not (0.0 <= c <= 1.0):
                    print(f"[FAIL] L2 {f.name}:{rid}: confidence out of range {conf}")
                    errors += 1
            except Exception:
                print(f"[FAIL] L2 {f.name}:{rid}: confidence not numeric")
                errors += 1
        models = rec.get("applicable_models")
        if models is not None and "SIM800L" not in models:
            print(f"[FAIL] L2 {f.name}:{rid}: applicable_models missing SIM800L")
            errors += 1
        if st == "complete" and conf is not None:
            try:
                if float(conf) < 0.95:
                    print(f"[FAIL] L2 {f.name}:{rid}: status=complete but confidence<0.95")
                    errors += 1
            except Exception:
                pass
    return errors


def level3_cross_ref() -> int:
    warnings = 0
    index = {}
    for _f, _d, rec in iter_records():
        if isinstance(rec, dict) and rec.get("id"):
            index.setdefault(rec["id"], _f.name)
    for f, _d, rec in iter_records():
        if not isinstance(rec, dict):
            continue
        for key in ("related_commands", "related_urcs", "related_timings"):
            vals = rec.get(key) or []
            if not isinstance(vals, list):
                continue
            for ref in vals:
                if ref and ref not in index:
                    print(f"[WARN] L3 {f.name}:{rec.get('id')}: {key} -> unknown {ref!r}")
                    warnings += 1
    return warnings


def level4_consistency() -> int:
    errors = 0
    seen_ids = {}
    for f, _d, rec in iter_records():
        if not isinstance(rec, dict):
            continue
        if rec.get("status") == "example-only":
            print(f"[FAIL] L4 {f.relative_to(ROOT)}: example-only in data/")
            errors += 1
        rid = rec.get("id")
        if rid:
            if rid in seen_ids:
                print(f"[FAIL] L4 duplicate id {rid!r} in {seen_ids[rid]} and {f.name}")
                errors += 1
            else:
                seen_ids[rid] = f.name
    return errors


def main() -> int:
    print("== validate.py (YAML only) ==")
    total = 0
    print("-- Level 1: schema (actual) --")
    total += level1_schema()
    print("-- Level 2: business logic --")
    total += level2_business()
    print("-- Level 3: cross-reference --")
    total += level3_cross_ref()
    print("-- Level 4: consistency --")
    total += level4_consistency()
    print(f"== total errors: {total} ==")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())