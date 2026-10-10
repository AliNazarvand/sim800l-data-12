#!/usr/bin/env python3
"""اعتبارسنجی با jsonschema واقعی."""
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
    import jsonschema
    from jsonschema import validate as js_validate, Draft7Validator
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pyyaml", "jsonschema"])
    import yaml, jsonschema
    from jsonschema import validate as js_validate, Draft7Validator

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SCHEMAS = ROOT / "schemas"
REPORTS = ROOT / "reports"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

FORBIDDEN = {"synthetic", "example-only"}
VALID_STATUS = {"complete","partial","unknown","inferred","blocked","deferred"}
VALID_SRC_TYPE = {"primary","secondary","external"}
REQUIRED = ["id","category","source","source_type","confidence","status","applicable_models","created_at","updated_at"]

def schema_path_for(yaml_name):
    stem = yaml_name.replace(".yaml", "")
    parts = stem.split("_")
    if len(parts) >= 2:
        return SCHEMAS / f"{parts[0]}_{parts[1]}.schema.yaml"
    return None

def main():
    errors = []
    warnings = []
    per_file = {}
    files = sorted(DATA.glob("dat_*.yaml"))
    print(f"بررسی {len(files)} فایل...")

    for p in files:
        try:
            with open(p, encoding="utf-8") as f:
                data = yaml.safe_load(f) or []
        except Exception as e:
            errors.append(f"[YAML] {p.name}: {e}")
            continue
        if not isinstance(data, list):
            errors.append(f"[SHAPE] {p.name}: باید لیست باشد")
            continue
        per_file[p.name] = len(data)

        # schema validation
        sp = schema_path_for(p.name)
        if sp and sp.exists():
            try:
                schema = yaml.safe_load(sp.read_text(encoding="utf-8"))
                validator = Draft7Validator(schema)
                for idx, rec in enumerate(data):
                    # jsonschema expects required+properties — ما schema پایه را داریم
                    for err in validator.iter_errors(rec):
                        errors.append(f"[SCHEMA] {p.name}[{idx}] {err.message[:150]}")
            except Exception as e:
                warnings.append(f"[SCHEMA-LOAD] {sp.name}: {e}")

        seen_ids = set()
        for idx, rec in enumerate(data):
            if not isinstance(rec, dict):
                errors.append(f"[REC] {p.name}[{idx}]")
                continue
            for f in REQUIRED:
                if f not in rec:
                    errors.append(f"[REQ] {p.name}[{idx}]: فیلد '{f}' ندارد")
            rid = rec.get("id")
            if rid in seen_ids:
                errors.append(f"[DUP] {p.name}: id تکراری {rid}")
            seen_ids.add(rid)
            st = rec.get("status")
            if st in FORBIDDEN:
                errors.append(f"[STATUS] {p.name}/{rid}: status ممنوع '{st}'")
            if st and st not in VALID_STATUS:
                errors.append(f"[STATUS] {p.name}/{rid}: status نامعتبر '{st}'")
            stp = rec.get("source_type")
            if stp and stp not in VALID_SRC_TYPE:
                errors.append(f"[SRC] {p.name}/{rid}: source_type نامعتبر")
            am = rec.get("applicable_models") or []
            if "SIM800L" not in am:
                errors.append(f"[MODEL] {p.name}/{rid}: SIM800L ندارد")

    REPORTS.mkdir(parents=True, exist_ok=True)
    out = [f"# VALIDATION_REPORT", f"> auto-generated at {NOW}", ""]
    out.append(f"## خلاصه")
    out.append(f"- فایل‌ها: {len(files)}")
    out.append(f"- خطاها: {len(errors)}")
    out.append(f"- هشدارها: {len(warnings)}")
    out.append("")
    out.append("## تعداد رکورد در هر فایل")
    for k in sorted(per_file.keys()):
        out.append(f"- {k}: {per_file[k]}")
    if errors:
        out.append("")
        out.append("## خطاها")
        for e in errors[:300]:
            out.append(f"- {e}")
    if warnings:
        out.append("")
        out.append("## هشدارها")
        for w in warnings[:100]:
            out.append(f"- {w}")
    (REPORTS / "VALIDATION_REPORT.md").write_text("\n".join(out), encoding="utf-8")

    if errors:
        print(f"{len(errors)} خطا")
        return 1
    print("بدون خطا")
    return 0

if __name__ == "__main__":
    sys.exit(main())