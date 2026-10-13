"""
v4: more robust AT command extraction.
v3 required the literal form '+XXX' with only alnum after. Many records
store commands as 'AT+CMGS=...' or 'AT+CMGS' or '+CMGS' or 'CMGS'.
v4 strips the AT prefix, extracts the '+XXX' token, and normalizes.
Also supports additional field names: related, related_at, commands.
"""
import sys, json, re, yaml
from pathlib import Path

CMD_RE = re.compile(r'\+([A-Z][A-Z0-9]{1,})', re.IGNORECASE)

def load(p):
    try:
        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f) or []
    except Exception:
        return []

def norm_cmd(s):
    """Return '+XXX' uppercase, or None."""
    if not isinstance(s, str): return None
    t = s.strip().upper()
    if not t: return None
    m = CMD_RE.search(t)
    if not m: return None
    return "+" + m.group(1).upper()

FIELD_NAMES_FOR_KNOWN = ("command", "cmd", "at_command", "name")
FIELD_NAMES_FOR_REFS  = ("command", "cmd", "at_command",
                         "related_commands", "related_command",
                         "related", "related_at", "commands")

def collect(records, field_names):
    s = set()
    for r in records:
        if not isinstance(r, dict): continue
        for k in field_names:
            v = r.get(k)
            items = v if isinstance(v, list) else [v]
            for it in items:
                c = norm_cmd(it)
                if c: s.add(c)
    return s

def main():
    root = Path(sys.argv[1])
    data_dir = root / "data"
    by_ds = {"_".join(p.stem.split("_")[:2]): load(p)
             for p in sorted(data_dir.glob("dat_*.yaml"))}
    known = collect(by_ds.get("dat_01", []), FIELD_NAMES_FOR_KNOWN)
    report = {"dat_01_commands": sorted(known), "refs": [],
              "unresolved": [], "note": ""}
    if not known:
        report["note"] = "dat_01 is empty: cross-ref degraded to inventory only."
    for ds, recs in by_ds.items():
        if ds == "dat_01": continue
        local = collect(recs, FIELD_NAMES_FOR_REFS)
        resolved = [c for c in local if c in known]
        unresolved = [c for c in local if c not in known]
        report["refs"].append({"dataset": ds, "total_refs": len(local),
                               "resolved": len(resolved),
                               "unresolved": len(unresolved)})
        for u in sorted(unresolved):
            report["unresolved"].append({"dataset": ds, "command": u})
    out = root / "reports" / "_cross_ref_result.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()