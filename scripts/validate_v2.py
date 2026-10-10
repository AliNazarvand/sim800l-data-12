#!/usr/bin/env python3
"""Schema-based validator with jsonschema (falls back to structure-only)."""
import os, sys, glob, yaml
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT,"data")
SCH  = os.path.join(ROOT,"schemas")
REP  = os.path.join(ROOT,"reports")

try:
    import jsonschema
    HAVE_JS = True
except Exception:
    HAVE_JS = False

REQUIRED = ["id","category","source","source_type","confidence",
            "status","applicable_models"]
VALID_STATUS = {"complete","partial","unknown","inferred",
                "blocked","deferred","example-only"}
VALID_SRC_TYPE = {"primary","secondary","external"}

def load_schema(nn):
    p = os.path.join(SCH,"dat_%s.schema.yaml"%nn)
    if not os.path.exists(p): return None
    try:
        with open(p,"r",encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        return None

def validate_file(path):
    errs = []
    try:
        with open(path,"r",encoding="utf-8") as f:
            doc = yaml.safe_load(f) or {}
    except Exception as e:
        return ["%s: YAML parse error: %s"%(os.path.basename(path),e)]
    recs = doc.get("records",[]) if isinstance(doc,dict) else (doc or [])
    if not isinstance(recs,list):
        return ["%s: records not a list"%os.path.basename(path)]
    bn = os.path.basename(path)
    m = bn.split("_")
    nn = m[1] if len(m)>1 else "00"
    schema = load_schema(nn)
    seen = set()
    for i,r in enumerate(recs):
        tag = "%s[%d]"%(bn,i)
        if not isinstance(r,dict):
            errs.append("%s not a mapping"%tag); continue
        for k in REQUIRED:
            if k not in r: errs.append("%s missing %s"%(tag,k))
        rid = r.get("id")
        if rid:
            if rid in seen: errs.append("%s duplicate id %s"%(tag,rid))
            seen.add(rid)
        if "SIM800L" not in (r.get("applicable_models") or []):
            errs.append("%s missing SIM800L"%tag)
        st = r.get("status")
        if st == "synthetic":
            errs.append("%s status=synthetic forbidden"%tag)
        if st == "example-only" and "data/" in path.replace("\\","/"):
            errs.append("%s example-only forbidden inside data/"%tag)
        if st and st not in VALID_STATUS:
            errs.append("%s invalid status=%s"%(tag,st))
        stp = r.get("source_type")
        if stp and stp not in VALID_SRC_TYPE:
            errs.append("%s invalid source_type=%s"%(tag,stp))
        if HAVE_JS and schema:
            try:
                jsonschema.validate(r, schema)
            except jsonschema.ValidationError as e:
                errs.append("%s schema: %s"%(tag,str(e.message)[:140]))
    return errs

def main():
    all_errs = []
    files = sorted(glob.glob(os.path.join(DATA,"*.yaml")))
    for p in files:
        all_errs += validate_file(p)
    rep = os.path.join(REP,"VALIDATION_REPORT.md")
    with open(rep,"w",encoding="utf-8") as f:
        f.write("# Validation Report (v2)\n\n")
        f.write("- jsonschema available: **%s**\n"%HAVE_JS)
        f.write("- Files checked: %d\n"%len(files))
        f.write("- Errors: %d\n\n"%len(all_errs))
        if all_errs:
            f.write("## Errors\n\n")
            for e in all_errs[:500]:
                f.write("- %s\n"%e)
        else:
            f.write("## No errors ✅\n")
    if all_errs:
        for e in all_errs[:40]: print("ERR:", e)
        print("...")
        print("TOTAL ERRORS: %d (see reports/VALIDATION_REPORT.md)"%len(all_errs))
        sys.exit(1)
    print("Validation OK (jsonschema=%s, files=%d)"%(HAVE_JS,len(files)))

if __name__ == "__main__":
    main()