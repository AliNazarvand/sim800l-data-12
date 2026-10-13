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
    m = CMD_RE.match(s.strip())
    return m.group(0).upper() if m else None

def collect_keys(records, keys):
    s = set()
    for r in records:
        if not isinstance(r, dict): continue
        for k in keys:
            v = r.get(k)
            items = v if isinstance(v, list) else [v]
            for it in items:
                c = norm_cmd(it)
                if c: s.add(c)
    return s

def main():
    root = Path(sys.argv[1])
    data_dir = root / "data"
    by_ds = {"_".join(p.stem.split("_")[:2]): load(p) for p in sorted(data_dir.glob("dat_*.yaml"))}
    known = collect_keys(by_ds.get("dat_01", []), ("command","cmd"))
    report = {"dat_01_commands": sorted(known), "refs": [], "unresolved": [], "note": ""}
    if not known:
        report["note"] = "dat_01 is empty: cross-ref degraded to inventory only."
    for ds, recs in by_ds.items():
        if ds == "dat_01": continue
        local = collect_keys(recs, ("command","cmd","related_commands","related_command"))
        resolved = [c for c in local if c in known]
        unresolved = [c for c in local if c not in known]
        report["refs"].append({"dataset": ds, "total_refs": len(local),
                               "resolved": len(resolved), "unresolved": len(unresolved)})
        for u in sorted(unresolved):
            report["unresolved"].append({"dataset": ds, "command": u})
    out = root / "reports" / "_cross_ref_result.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()