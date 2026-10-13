import sys, json, yaml
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print("ERROR: jsonschema missing. Run: pip install jsonschema")
    sys.exit(3)

REQUIRED = ["id","category","source","source_type","confidence","status","applicable_models"]
STATUS_ENUM = {"complete","partial","unknown","inferred","blocked","deferred"}
SRC_TYPE_ENUM = {"primary","secondary","external"}

def load_yaml(p):
    try:
        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        return {"__error__": str(e)}

def main():
    root = Path(sys.argv[1])
    data_dir = root / "data"
    schemas_dir = root / "schemas"
    report = {"datasets": [], "errors": [], "warnings": [], "schema_used": {}}

    schema_cache = {}
    if schemas_dir.exists():
        for sp in schemas_dir.glob("dat_*.schema.yaml"):
            try:
                schema_cache[sp.stem.replace(".schema","")] = load_yaml(sp)
            except Exception:
                pass

    data_files = sorted(data_dir.glob("dat_*.yaml")) if data_dir.exists() else []
    for f in data_files:
        ds = "_".join(f.stem.split("_")[:2])  # dat_01
        doc = load_yaml(f)
        errors = []
        if isinstance(doc, dict) and "__error__" in doc:
            errors.append(f"YAML parse error: {doc['__error__']}")
            report["datasets"].append({"dataset": ds, "file": f.name, "records": 0, "errors": len(errors), "schema_ok": False})
            report["errors"].extend([f"{f.name}: {e}" for e in errors])
            continue

        records = doc if isinstance(doc, list) else ([doc] if isinstance(doc, dict) else [])
        seen_ids = set()
        for i, rec in enumerate(records):
            if not isinstance(rec, dict):
                errors.append(f"[{i}] not a mapping"); continue
            for field in REQUIRED:
                if field not in rec:
                    errors.append(f"[{i}] missing required field: {field}")
            rid = rec.get("id")
            if rid:
                if rid in seen_ids: errors.append(f"[{i}] duplicate id: {rid}")
                seen_ids.add(rid)
            st = rec.get("status")
            if st is not None and st not in STATUS_ENUM:
                errors.append(f"[{i}] invalid status: {st}")
            if st == "example-only":
                errors.append(f"[{i}] example-only present (R21)")
            if st == "synthetic":
                errors.append(f"[{i}] synthetic forbidden (R6)")
            stype = rec.get("source_type")
            if stype is not None and stype not in SRC_TYPE_ENUM:
                errors.append(f"[{i}] invalid source_type: {stype}")
            conf = rec.get("confidence")
            if conf is not None:
                try:
                    cf = float(conf)
                    if cf < 0 or cf > 1: errors.append(f"[{i}] confidence out of range")
                    if st == "inferred" and cf > 0.5: errors.append(f"[{i}] inferred > 0.5 (R4)")
                except (TypeError, ValueError):
                    errors.append(f"[{i}] non-numeric confidence")
            am = rec.get("applicable_models")
            if not isinstance(am, list) or "SIM800L" not in am:
                errors.append(f"[{i}] applicable_models must contain SIM800L (R1)")

        schema_ok = True
        schema_key = ds
        if schema_key in schema_cache:
            schema = schema_cache[schema_key]
            if isinstance(schema, dict):
                report["schema_used"][f.name] = schema_key
                try:
                    for i, rec in enumerate(records):
                        if not isinstance(rec, dict): continue
                        try:
                            jsonschema.validate(instance=rec, schema=schema)
                        except jsonschema.ValidationError as ve:
                            msg = str(ve.message).split("\n")[0][:160]
                            errors.append(f"[{i}] schema: {msg}")
                            schema_ok = False
                except Exception as e:
                    errors.append(f"schema validator error: {e}")
                    schema_ok = False

        report["datasets"].append({
            "dataset": ds, "file": f.name, "records": len(records),
            "errors": len(errors), "schema_ok": schema_ok
        })
        if errors:
            report["errors"].extend([f"{f.name}: {e}" for e in errors[:120]])

    out = root / "reports" / "_validation_result.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()