import sys, json, yaml
from pathlib import Path
import jsonschema

REQUIRED = ["id","category","source","source_type","confidence","status","applicable_models"]
STATUS_ENUM = {"complete","partial","unknown","inferred","blocked","deferred"}
SRC_TYPE_ENUM = {"primary","secondary","external"}

def load(p):
    try:
        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        return {"__error__": str(e)}

def main():
    root = Path(sys.argv[1])
    data_dir = root / "data"
    schemas_dir = root / "schemas"
    report = {"datasets": [], "errors": [], "schema_used": {}}

    schema_cache = {}
    for sp in schemas_dir.glob("dat_*.schema.yaml"):
        try:
            schema_cache[sp.stem.replace(".schema","")] = load(sp)
        except Exception:
            pass

    for f in sorted(data_dir.glob("dat_*.yaml")):
        ds = "_".join(f.stem.split("_")[:2])
        doc = load(f)
        errors = []
        if isinstance(doc, dict) and "__error__" in doc:
            errors.append(f"YAML error: {doc['__error__']}")
            report["datasets"].append({"dataset": ds, "file": f.name, "records": 0,
                                       "errors": len(errors), "schema_ok": False})
            report["errors"].extend([f"{f.name}: {e}" for e in errors])
            continue
        records = doc if isinstance(doc, list) else ([doc] if isinstance(doc, dict) else [])
        seen_ids = set()
        for i, rec in enumerate(records):
            if not isinstance(rec, dict):
                errors.append(f"[{i}] not a mapping"); continue
            for field in REQUIRED:
                if field not in rec:
                    errors.append(f"[{i}] missing: {field}")
            rid = rec.get("id")
            if rid in seen_ids: errors.append(f"[{i}] duplicate id: {rid}")
            seen_ids.add(rid)
            st = rec.get("status")
            if st is not None and st not in STATUS_ENUM:
                errors.append(f"[{i}] invalid status: {st}")
            if st == "example-only":
                errors.append(f"[{i}] example-only forbidden (R21)")
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
                errors.append(f"[{i}] applicable_models missing SIM800L (R1)")

        schema_ok = True
        if ds in schema_cache and isinstance(schema_cache[ds], dict):
            report["schema_used"][f.name] = ds
            for i, rec in enumerate(records):
                if not isinstance(rec, dict): continue
                try:
                    jsonschema.validate(instance=rec, schema=schema_cache[ds])
                except jsonschema.ValidationError as ve:
                    errors.append(f"[{i}] schema: {str(ve.message).splitlines()[0][:160]}")
                    schema_ok = False
                except Exception as e:
                    errors.append(f"[{i}] validator error: {e}")
                    schema_ok = False

        report["datasets"].append({"dataset": ds, "file": f.name, "records": len(records),
                                   "errors": len(errors), "schema_ok": schema_ok})
        if errors:
            report["errors"].extend([f"{f.name}: {e}" for e in errors[:120]])

    out = root / "reports" / "_validation_result.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()