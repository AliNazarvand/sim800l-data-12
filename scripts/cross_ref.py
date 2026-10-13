import sys, json, re, yaml
from pathlib import Path

CMD_RE = re.compile(r'^\+[A-Z0-9]{2,}[A-Z0-9]*$', re.IGNORECASE)

def load(p):
    try:
        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f) or []
    except Exception:
        return []

def norm_cmd(s):
    if not isinstance(s, str): return None
    s = s.strip()
    if not s: return None
    m = CMD_RE.match(s)
    return m.group(0).upper() if m else None

def collect_dat01(records):
    cmds = set()
    for r in records:
        if not isinstance(r, dict): continue
        for key in ("command","cmd"):
            c = norm_cmd(r.get(key))
            if c: cmds.add(c)
    return cmds

def collect_refs(records):
    refs = set()
    for r in records:
        if not isinstance(r, dict): continue
        for key in ("command","related_commands","related_command"):
            v = r.get(key)
            items = v if isinstance(v, list) else [v]
            for it in items:
                c = norm_cmd(it)
                if c: refs.add(c)
    return refs

def main():
    root = Path(sys.argv[1])
    data_dir = root / "data"
    files = sorted(data_dir.glob("dat_*.yaml")) if data_dir.exists() else []
    by_ds = {"_".join(p.stem.split("_")[:2]): load(p) for p in files}

    known = collect_dat01(by_ds.get("dat_01", []))
    report = {"dat_01_commands": sorted(known), "refs": [], "unresolved": [], "note": ""}
    if not known:
        report["note"] = "dat_01 empty: cross-ref degraded to inventory only."

    for ds, recs in by_ds.items():
        if ds == "dat_01": continue
        local = collect_refs(recs)
        resolved = sorted([c for c in local if c in known])
        unresolved = sorted([c for c in local if c not in known])
        report["refs"].append({"dataset": ds, "total_refs": len(local),
                               "resolved": len(resolved), "unresolved": len(unresolved)})
        for u in unresolved:
            report["unresolved"].append({"dataset": ds, "command": u})

    out = root / "reports" / "_cross_ref_result.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()