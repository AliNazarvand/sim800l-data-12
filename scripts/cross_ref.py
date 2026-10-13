"""
v6 cross-ref: classify unresolved references by the manual that would
contain them. This converts "unresolved errors" into honest
"blocked-source: needs <manual>" records.
"""
import sys, json, re, yaml
from pathlib import Path

CMD_RE = re.compile(r'\+([A-Z][A-Z0-9]{1,})', re.IGNORECASE)

# Commands NOT in AT Manual V1.01; they live in separate SIMCom manuals.
NEEDS_SSL    = {"+SSLCFG","+SSLOPEN","+SSLCLOSE","+SSLSEND","+SSLRECV",
                "+SSLSETCERT","+SSLSETKEY","+SSLSETCA","+SSLCONF"}
NEEDS_HTTP   = {"+HTTPHEAD","+HTTPURL","+HTTPSSL"}
NEEDS_FTP    = {"+FTPOPEN","+FTPCLOSE","+FTPUSER","+FTPPASS",
                "+FTPCWD","+FTPPWD","+FTPFLST"}
NEEDS_AUDIO  = {"+CADTONE","+CATONE","+CLDTONE","+CPCMREG"}
NEEDS_FW     = {"+CEREG","+CGCONTRDP","+CIPDDREM"}  # newer firmware

def classify_missing(cmd):
    if cmd in NEEDS_SSL:   return "SIM800 SSL AT Command Manual"
    if cmd in NEEDS_HTTP:  return "SIM800 HTTP AT Command Manual"
    if cmd in NEEDS_FTP:   return "SIM800 FTP AT Command Manual"
    if cmd in NEEDS_AUDIO: return "SIM800 Audio AT Command Manual"
    if cmd in NEEDS_FW:    return "SIM800 Firmware Release Notes"
    return "unknown manual"

def load(p):
    try:
        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f) or []
    except Exception:
        return []

def norm_cmd(s):
    if not isinstance(s, str): return None
    m = CMD_RE.search(s.strip().upper())
    return "+" + m.group(1).upper() if m else None

FIELD_KNOWN = ("command","cmd","at_command","name")
FIELD_REFS  = ("command","cmd","at_command",
               "related_commands","related_command",
               "related","related_at","commands")

def collect(records, names):
    s = set()
    for r in records:
        if not isinstance(r, dict): continue
        for k in names:
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
    known = collect(by_ds.get("dat_01", []), FIELD_KNOWN)
    report = {
        "dat_01_commands": sorted(known),
        "refs": [],
        "unresolved": [],
        "blocked_source": {},   # manual -> [commands]
        "note": ""
    }
    if not known:
        report["note"] = "dat_01 is empty: cross-ref degraded."

    for ds, recs in by_ds.items():
        if ds == "dat_01": continue
        local = collect(recs, FIELD_REFS)
        resolved = sorted(c for c in local if c in known)
        unresolved = sorted(c for c in local if c not in known)
        report["refs"].append({
            "dataset": ds,
            "total_refs": len(local),
            "resolved": len(resolved),
            "unresolved": len(unresolved),
        })
        for u in unresolved:
            manual = classify_missing(u)
            report["unresolved"].append({"dataset": ds, "command": u, "needs": manual})
            report["blocked_source"].setdefault(manual, [])
            report["blocked_source"][manual].append(f"{ds}:{u}")

    out = root / "reports" / "_cross_ref_result.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()