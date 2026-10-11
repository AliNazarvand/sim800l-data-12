#!/usr/bin/env python3
"""
validate.py — Step 1: schema + business logic + cross-ref + consistency
"""
import sys
import re
from pathlib import Path
from datetime import datetime

try:
    import yaml
except ImportError:
    print("PyYAML is required. pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SCHEMAS = ROOT / "schemas"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

VALID_STATUS = {"complete","partial","unknown","inferred","blocked","deferred","example-only"}
VALID_SOURCE_TYPE = {"primary","secondary","external"}
REQ_FIELDS = ["id","category","source","source_type","confidence","status","applicable_models","created_at","updated_at"]

def load_yaml(path):
    try:
        text = path.read_text(encoding="utf-8")
        return yaml.safe_load(text)
    except Exception as e:
        return e

def check_schema(dat_id, records):
    errors = []
    if not isinstance(records, list):
        records = [records]
    ids = set()
    for idx, r in enumerate(records):
        if not isinstance(r, dict):
            errors.append(f"[{dat_id}] record {idx} is not a dict")
            continue
        rid = r.get("id", "?")
        for f in REQ_FIELDS:
            if f not in r:
                errors.append(f"[{dat_id}] {rid}: missing field {f}")
        if rid in ids:
            errors.append(f"[{dat_id}] duplicate id {rid}")
        ids.add(rid)
    return errors

def check_business(dat_id, records):
    errors = []
    warnings = []
    if not isinstance(records, list):
        records = [records]
    for r in records:
        if not isinstance(r, dict):
            continue
        rid = r.get("id", "?")
        status = r.get("status")
        if status == "synthetic":
            errors.append(f"[{dat_id}] {rid}: status synthetic not allowed")
        if status == "example-only":
            errors.append(f"[{dat_id}] {rid}: example-only in data/ (R21)")
        if status not in VALID_STATUS:
            errors.append(f"[{dat_id}] {rid}: invalid status {status}")
        st = r.get("source_type")
        if st not in VALID_SOURCE_TYPE:
            errors.append(f"[{dat_id}] {rid}: invalid source_type {st}")
        models = r.get("applicable_models") or []
        if "SIM800L" not in models:
            errors.append(f"[{dat_id}] {rid}: applicable_models missing SIM800L")
        src = r.get("source") or {}
        if not src.get("name"):
            errors.append(f"[{dat_id}] {rid}: source.name missing")
        if src.get("version") in (None, "", "auto"):
            errors.append(f"[{dat_id}] {rid}: source.version invalid")
        if src.get("date") in (None, "", "auto"):
            errors.append(f"[{dat_id}] {rid}: source.date invalid")
        if src.get("page") == "auto":
            errors.append(f"[{dat_id}] {rid}: source.page is auto (R2)")
        if "SIM800H-only" in str(r.get("notes", "")):
            errors.append(f"[{dat_id}] {rid}: SIM800H-only record")
        conf = r.get("confidence")
        if not isinstance(conf, (int, float)) or conf < 0.0 or conf > 1.0:
            errors.append(f"[{dat_id}] {rid}: confidence out of range")
        for tf in ("created_at", "updated_at"):
            v = r.get(tf)
            if v:
                try:
                    datetime.fromisoformat(str(v).replace("Z", "+00:00"))
                except Exception:
                    errors.append(f"[{dat_id}] {rid}: {tf} not ISO 8601")
    return errors, warnings

def check_cross_ref(all_data):
    errors = []
    dat01 = all_data.get("dat_01")
    commands = set()
    if isinstance(dat01, list):
        for r in dat01:
            if isinstance(r, dict) and r.get("command"):
                commands.add(str(r["command"]).lstrip("+"))
    for ds in ["dat_09","dat_10","dat_11","dat_12","dat_13","dat_15","dat_17"]:
        recs = all_data.get(ds)
        if not isinstance(recs, list):
            continue
        for r in recs:
            if not isinstance(r, dict):
                continue
            cmd = r.get("command")
            if cmd:
                c = str(cmd).lstrip("+")
                if c not in commands:
                    errors.append(f"[{ds}] {r.get('id')}: command +{c} not found in dat_01")
    return errors

def check_consistency(all_data):
    errors = []
    for ds, recs in all_data.items():
        if not isinstance(recs, list):
            continue
        for r in recs:
            if isinstance(r, dict) and r.get("status") == "in-progress":
                errors.append(f"[{ds}] {r.get('id')}: status in-progress is not allowed")
    return errors

def main():
    all_errors = []
    all_warnings = []
    all_data = {}
    for i in range(1, 19):
        dat_id = f"dat_{i:02d}"
        path = DATA / f"{dat_id}.yaml"
        if not path.exists():
            all_errors.append(f"[{dat_id}] data file missing")
            continue
        data = load_yaml(path)
        if isinstance(data, Exception):
            all_errors.append(f"[{dat_id}] YAML parse error: {data}")
            continue
        all_data[dat_id] = data
        all_errors.extend(check_schema(dat_id, data))
        e2, w2 = check_business(dat_id, data)
        all_errors.extend(e2)
        all_warnings.extend(w2)
    all_errors.extend(check_cross_ref(all_data))
    all_errors.extend(check_consistency(all_data))

    report = REPORTS / "VALIDATION_REPORT.md"
    lines = [
        "# VALIDATION_REPORT",
        "",
        f"Generated: {datetime.utcnow().isoformat()}Z",
        "",
        "## خلاصه",
        f"- خطاهای سطح ۱ (Schema): {len([e for e in all_errors if 'missing field' in e or 'duplicate id' in e])}",
        f"- خطاهای سطح ۲ (Business): {len([e for e in all_errors if 'synthetic' in e or 'example-only' in e or 'source.' in e or 'confidence' in e or 'applicable_models' in e])}",
        f"- خطاهای سطح ۳ (Cross-ref): {len([e for e in all_errors if 'not found in dat_01' in e])}",
        f"- خطاهای سطح ۴ (Consistency): {len([e for e in all_errors if 'in-progress' in e])}",
        "",
        "## خطاها",
        "",
    ]
    lines += [f"- {e}" for e in all_errors] or ["- (none)"]
    lines += ["", "## هشدارها", ""]
    lines += [f"- {w}" for w in all_warnings] or ["- (none)"]
    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"Validation: {len(all_errors)} errors, {len(all_warnings)} warnings")
    sys.exit(1 if all_errors else 0)

if __name__ == "__main__":
    main()