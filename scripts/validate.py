#!/usr/bin/env python3
"""validate.py - Full validation with glob-aware data file lookup."""
import sys
import json
from pathlib import Path
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

try:
    from jsonschema import Draft7Validator
    HAS_JS = True
except ImportError:
    HAS_JS = False

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SCHEMAS = ROOT / "schemas"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

VALID_STATUS = {"complete","partial","unknown","inferred","blocked","deferred","example-only"}
VALID_SOURCE_TYPE = {"primary","secondary","external"}
REQ_FIELDS = ["id","category","source","source_type","confidence","status","applicable_models","created_at","updated_at"]

errors = []

def add(dataset, level, record, error, suggestion=""):
    errors.append({
        "dataset": dataset, "level": level, "record": str(record),
        "error": str(error), "suggestion": str(suggestion)
    })

def load_yaml(path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        return e

def norm_records(data):
    if data is None:
        return []
    if isinstance(data, list):
        return data
    return [data]

def find_data_file(dat_id):
    """Find data file matching dat_XX.yaml OR dat_XX_*.yaml."""
    candidates = sorted(DATA.glob(f"{dat_id}_*.yaml"))
    if candidates:
        return candidates[0]
    exact = DATA / f"{dat_id}.yaml"
    if exact.exists():
        return exact
    return None

all_data = {}
data_paths = {}

# ---------- Level 1: schema + required fields ----------
for i in range(1, 19):
    dat_id = f"dat_{i:02d}"
    data_path = find_data_file(dat_id)
    schema_path = SCHEMAS / f"{dat_id}.schema.yaml"
    if data_path is None:
        add(dat_id, 1, "-", f"data file missing (no dat_{i:02d}*.yaml)", "create file")
        continue
    data_paths[dat_id] = str(data_path.name)
    if not schema_path.exists():
        add(dat_id, 1, "-", f"schema file missing: {schema_path.name}", "create schema")
        continue
    data = load_yaml(data_path)
    if isinstance(data, Exception):
        add(dat_id, 1, "-", f"YAML parse error in {data_path.name}: {data}", "fix YAML")
        continue
    records = norm_records(data)
    all_data[dat_id] = records

    ids = set()
    for rec in records:
        if not isinstance(rec, dict):
            add(dat_id, 1, "-", "record is not a mapping", "")
            continue
        rid = rec.get("id", "?")
        for f in REQ_FIELDS:
            if f not in rec:
                add(dat_id, 1, rid, f"missing required field: {f}", f"add {f}")
        if rid in ids:
            add(dat_id, 1, rid, "duplicate id", "make unique")
        ids.add(rid)

    if HAS_JS:
        schema = load_yaml(schema_path)
        if isinstance(schema, Exception):
            add(dat_id, 1, "-", f"schema parse error: {schema}", "fix schema")
        else:
            try:
                validator = Draft7Validator(schema)
                if isinstance(schema, dict) and schema.get("type") == "array":
                    for err in validator.iter_errors(data):
                        p = "/".join(str(x) for x in err.absolute_path) or "(root)"
                        add(dat_id, 1, p, err.message, "")
                else:
                    for rec in records:
                        if not isinstance(rec, dict):
                            continue
                        for err in validator.iter_errors(rec):
                            p = "/".join(str(x) for x in err.absolute_path) or "(root)"
                            add(dat_id, 1, f"{rec.get('id','?')}:{p}", err.message, "")
            except Exception as e:
                add(dat_id, 1, "-", f"schema validation failed: {e}", "check schema")

# ---------- Level 2: business logic ----------
for dat_id, records in all_data.items():
    for rec in records:
        if not isinstance(rec, dict):
            continue
        rid = rec.get("id", "?")
        status = rec.get("status")
        if status == "synthetic":
            add(dat_id, 2, rid, "status: synthetic not allowed (R6)", "change status")
        if status == "example-only":
            add(dat_id, 2, rid, "status: example-only in data/ (R21)", "remove or replace")
        if status not in VALID_STATUS:
            add(dat_id, 2, rid, f"invalid status: {status}", "use valid enum")
        st = rec.get("source_type")
        if st not in VALID_SOURCE_TYPE:
            add(dat_id, 2, rid, f"invalid source_type: {st}", "use primary/secondary/external")
        models = rec.get("applicable_models") or []
        if "SIM800L" not in models:
            add(dat_id, 2, rid, "applicable_models missing SIM800L (R1)", "add SIM800L")
        src = rec.get("source") or {}
        if not src.get("name"):
            add(dat_id, 2, rid, "source.name missing (R2)", "provide name")
        v = src.get("version")
        if v in (None, "", "auto"):
            add(dat_id, 2, rid, "source.version invalid", "provide version")
        d = src.get("date")
        if d in (None, "", "auto"):
            add(dat_id, 2, rid, "source.date invalid", "provide date")
        if src.get("page") in ("auto", "unknown"):
            add(dat_id, 2, rid, "source.page invalid (auto/unknown)", "fix or remove")
        if src.get("section") in ("auto-extracted", "unknown"):
            add(dat_id, 2, rid, "source.section invalid", "fix or remove")
        notes = str(rec.get("notes", ""))
        if "SIM800H-only" in notes or "SIM800H only" in notes:
            add(dat_id, 2, rid, "SIM800H-only record (R1)", "remove")
        conf = rec.get("confidence")
        if not isinstance(conf, (int, float)) or conf < 0.0 or conf > 1.0:
            add(dat_id, 2, rid, f"confidence out of range: {conf}", "0.0..1.0")
        for tf in ("created_at", "updated_at"):
            val = rec.get(tf)
            if val:
                try:
                    datetime.fromisoformat(str(val).replace("Z", "+00:00"))
                except Exception:
                    add(dat_id, 2, rid, f"{tf} not ISO 8601", "fix timestamp")

# ---------- Level 3: cross-reference ----------
def commands_in_dat01():
    s = set()
    for rec in all_data.get("dat_01", []):
        if isinstance(rec, dict) and rec.get("command"):
            s.add(str(rec["command"]).lstrip("+").upper())
    return s

def cmd_norm(c):
    return str(c).lstrip("+").upper()

dat01_cmds = commands_in_dat01()
dat01_nonblocked = bool(dat01_cmds)

if dat01_nonblocked:
    for rec in all_data.get("dat_02", []):
        if not isinstance(rec, dict):
            continue
        rc = rec.get("related_command")
        if rc and cmd_norm(rc) not in dat01_cmds:
            add("dat_02", 3, rec.get("id"), f"related_command {rc} not in dat_01", "add or fix")
    for rec in all_data.get("dat_03", []):
        if not isinstance(rec, dict):
            continue
        for rc in (rec.get("related_commands") or []):
            if cmd_norm(rc) not in dat01_cmds:
                add("dat_03", 3, rec.get("id"), f"related_command {rc} not in dat_01", "add or fix")
    for ds in ["dat_09","dat_10","dat_11","dat_12","dat_13","dat_15","dat_17"]:
        for rec in all_data.get(ds, []):
            if not isinstance(rec, dict):
                continue
            cmd = rec.get("command")
            if cmd and cmd_norm(cmd) not in dat01_cmds:
                add(ds, 3, rec.get("id"), f"command {cmd} not in dat_01", "add to dat_01 or fix")

dat05_states = set()
for rec in all_data.get("dat_05", []):
    if isinstance(rec, dict) and rec.get("state_name"):
        dat05_states.add(str(rec["state_name"]).upper())
for rec in all_data.get("dat_04", []):
    if not isinstance(rec, dict):
        continue
    rs = rec.get("related_state")
    if rs and str(rs).upper() not in dat05_states:
        add("dat_04", 3, rec.get("id"), f"related_state {rs} not in dat_05", "add or fix")

# ---------- Level 4: consistency ----------
for dat_id, records in all_data.items():
    for rec in records:
        if isinstance(rec, dict) and rec.get("status") == "in-progress":
            add(dat_id, 4, rec.get("id"), "status: in-progress not allowed (R22)", "close dataset")

# ---------- Report ----------
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
by_level = {1:0, 2:0, 3:0, 4:0}
for e in errors:
    by_level[e["level"]] = by_level.get(e["level"], 0) + 1

lines = ["# VALIDATION_REPORT", "", f"Generated: {ts}", "", "## خلاصه"]
lines.append(f"- خطاهای سطح ۱ (Schema): {by_level[1]}")
lines.append(f"- خطاهای سطح ۲ (Business): {by_level[2]}")
lines.append(f"- خطاهای سطح ۳ (Cross-ref): {by_level[3]}")
lines.append(f"- خطاهای سطح ۴ (Consistency): {by_level[4]}")
lines.append("")
lines.append("## فایل‌های کشف‌شده")
lines.append("")
lines.append("| دیتاست | فایل |")
lines.append("|---|---|")
for i in range(1, 19):
    dat_id = f"dat_{i:02d}"
    lines.append(f"| {dat_id} | {data_paths.get(dat_id, '-')} |")
lines.append("")
lines.append("## جزئیات خطاها")
lines.append("")
lines.append("| دیتاست | سطح | رکورد | خطا | پیشنهاد اصلاح |")
lines.append("|---|---|---|---|---|")
if errors:
    for e in errors:
        err = e["error"].replace("|", "\\|")
        sug = e["suggestion"].replace("|", "\\|")
        lines.append(f"| {e['dataset']} | {e['level']} | {e['record']} | {err} | {sug} |")
else:
    lines.append("| - | - | - | (none) | - |")
lines.append("")

(REPORTS / "VALIDATION_REPORT.md").write_text("\n".join(lines), encoding="utf-8")
(REPORTS / "_validation_summary.json").write_text(
    json.dumps({"generated": ts, "errors": errors, "counts": by_level, "total": len(errors),
                "data_paths": data_paths}, ensure_ascii=False, indent=2),
    encoding="utf-8"
)

print(f"Validation: {len(errors)} errors (L1={by_level[1]} L2={by_level[2]} L3={by_level[3]} L4={by_level[4]})")
if not HAS_JS:
    print("WARNING: jsonschema not installed; schema-level validation was skipped.")
    print("         Install with: pip install jsonschema")
sys.exit(1 if errors else 0)