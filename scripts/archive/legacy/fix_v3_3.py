#!/usr/bin/env python3
"""Final fix v3.3 — resolve v3.2.1 regression + close cross-ref gaps."""
import os, re, sys, json, glob
from datetime import datetime, timezone
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REP  = os.path.join(ROOT, "reports")
NOW  = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
os.makedirs(REP, exist_ok=True)

BOOLEAN_FIELDS = {"concat_sms","delivery_report"}
YAML11_BOOL_LIKE = {"y","n","yes","no","true","false","on","off"}

SUMMARY = {"yaml_fixed":[], "dat_09_reverted":0, "dat_05_added":[], "errors":[]}

def revert_boolean_all():
    for path in sorted(glob.glob(os.path.join(DATA,"*.yaml"))):
        try:
            with open(path,"r",encoding="utf-8") as f:
                text = f.read()
            original = text
            for field in BOOLEAN_FIELDS:
                text = re.sub(
                    r'^(\s*'+field+r':\s*)"(true|false)"\s*$',
                    r'\1\2', text, flags=re.M
                )
            if text != original:
                with open(path,"w",encoding="utf-8") as f:
                    f.write(text)
                SUMMARY["yaml_fixed"].append(os.path.basename(path))
        except Exception as e:
            SUMMARY["errors"].append("revert %s: %s"%(os.path.basename(path),e))

NEW_STATES = [
    {
        "state_name":"POWER_DOWN",
        "description":"Power-down sequence running; network detach in progress",
        "entry_conditions":["PWRKEY held low >=1s","AT+CPOWD=1 issued"],
        "exit_conditions":["NORMAL POWER DOWN URC","STATUS pin low"],
        "events":["Power key hold","AT+CPOWD command"],
        "actions":["Log off from network","Save data to NVM"],
        "related_commands":["+CPOWD"],
        "related_urcs":["NORMAL POWER DOWN"],
    },
    {
        "state_name":"RESET",
        "description":"Hardware reset in progress (RESET pin low)",
        "entry_conditions":["RESET pin pulled to ground"],
        "exit_conditions":["RESET released","RDY URC"],
        "events":["Emergency reset"],
        "actions":["Module restarts"],
        "related_commands":[],
        "related_urcs":["RDY"],
    },
]

def add_missing_states():
    path = os.path.join(DATA,"dat_05_state_machine.yaml")
    if not os.path.exists(path): return
    with open(path,"r",encoding="utf-8") as f:
        text = f.read()
    existing = set(re.findall(r'state_name:\s*"?([A-Z_]+)"?', text))
    ids = re.findall(r'dat_05_(\d+)', text)
    next_idx = max((int(i) for i in ids), default=0) + 1
    additions = []
    for st in NEW_STATES:
        if st["state_name"] in existing: continue
        lines = []
        lines.append("- id: dat_05_%04d" % next_idx)
        lines.append("  category: State")
        lines.append("  source:")
        lines.append("    name: SIM800H&SIM800L Hardware Design")
        lines.append("    version: V2.02")
        lines.append('    date: "2015-07-27"')
        lines.append('    page: ""')
        lines.append('    section: ""')
        lines.append("  source_type: primary")
        lines.append("  confidence: 0.55")
        lines.append("  status: inferred")
        lines.append("  conflicts: []")
        lines.append('  notes: "State derived from hardware design PDF."')
        lines.append("  tags: []")
        lines.append("  applicable_models:")
        lines.append("    - SIM800L")
        lines.append('  created_at: "%s"' % NOW)
        lines.append('  updated_at: "%s"' % NOW)
        lines.append('  state_name: "%s"' % st["state_name"])
        lines.append('  description: "%s"' % st["description"])
        lines.append("  entry_conditions:")
        for c in st["entry_conditions"]:
            lines.append('    - "%s"' % c)
        lines.append("  exit_conditions:")
        for c in st["exit_conditions"]:
            lines.append('    - "%s"' % c)
        lines.append("  events:")
        for c in st["events"]:
            lines.append('    - "%s"' % c)
        lines.append("  actions:")
        for c in st["actions"]:
            lines.append('    - "%s"' % c)
        if st["related_commands"]:
            lines.append("  related_commands:")
            for c in st["related_commands"]:
                lines.append('    - "%s"' % c)
        else:
            lines.append("  related_commands: []")
        if st["related_urcs"]:
            lines.append("  related_urcs:")
            for c in st["related_urcs"]:
                lines.append('    - "%s"' % c)
        else:
            lines.append("  related_urcs: []")
        lines.append("  related_timings: []")
        additions.append("\n".join(lines))
        next_idx += 1
    if additions:
        with open(path,"a",encoding="utf-8") as f:
            f.write("\n" + "\n".join(additions) + "\n")
        SUMMARY["dat_05_added"] = [s["state_name"] for s in NEW_STATES
                                    if s["state_name"] not in existing]

def requote_string_booleans():
    for path in sorted(glob.glob(os.path.join(DATA,"*.yaml"))):
        try:
            with open(path,"r",encoding="utf-8") as f:
                lines = f.read().splitlines()
            out = []
            for line in lines:
                s = line.strip()
                if not s or s.startswith("#"):
                    out.append(line); continue
                m = re.match(r'^(\s*)([A-Za-z_][A-Za-z0-9_]*):\s+([A-Za-z]+)\s*$', line)
                if m:
                    indent, key, val = m.groups()
                    if key in BOOLEAN_FIELDS:
                        out.append(line); continue
                    if val.lower() in YAML11_BOOL_LIKE:
                        out.append('%s%s: "%s"' % (indent, key, val)); continue
                m = re.match(r'^(\s*-\s+)([A-Za-z]+)\s*$', line)
                if m:
                    prefix, val = m.groups()
                    if val.lower() in YAML11_BOOL_LIKE:
                        out.append('%s"%s"' % (prefix, val)); continue
                out.append(line)
            new_text = "\n".join(out) + "\n"
            with open(path,"w",encoding="utf-8") as f:
                f.write(new_text)
        except Exception as e:
            SUMMARY["errors"].append("requote %s: %s"%(os.path.basename(path),e))

DATASET_NAMES = {
    "01":"AT Command DB","02":"URC DB","03":"Error Code DB (CME/CMS)",
    "04":"Timing & Timeout","05":"State Machine","06":"Init Sequence",
    "07":"Hardware Reference","08":"Firmware Compatibility","09":"SMS DB",
    "10":"GPRS/Data DB","11":"HTTP/FTP/SSL DB","12":"Audio DB",
    "13":"SIM Management","14":"Operator/APN DB","15":"Power Management",
    "16":"Board/EVB Definitions","17":"Certificate/Key Store","18":"Certification",
}
BLOCKED_REASONS = {
    "08":"Awaiting Firmware Release Notes","16":"Awaiting EVB schematic/BOM",
    "17":"Awaiting SSL AT Command Manual","18":"Awaiting CE/FCC/GCF certificates",
}
INFERRED = {"04","05","06","15"}

def count_records():
    counts = {}
    for nn in DATASET_NAMES:
        matches = glob.glob(os.path.join(DATA,"dat_%s_*.yaml"%nn))
        if not matches: counts[nn] = 0; continue
        try:
            with open(matches[0],"r",encoding="utf-8") as f:
                doc = yaml.safe_load(f) or {}
            recs = doc.get("records",[]) if isinstance(doc,dict) else (doc or [])
            counts[nn] = len(recs) if isinstance(recs,list) else 0
        except Exception as e:
            SUMMARY["errors"].append("count %s: %s"%(matches[0],e))
            counts[nn] = 0
    return counts

def status_for(nn, cnt):
    if nn in BLOCKED_REASONS and cnt == 0: return "blocked"
    if cnt == 0: return "deferred"
    if nn in INFERRED: return "partial (inferred)"
    return "populated"

def update_reports(counts):
    lines = ["# Coverage Matrix (v3.3 final)","",
             "| Dataset | Name | Records | Status | Notes |","|---|---|---|---|---|"]
    for nn in sorted(DATASET_NAMES.keys()):
        cnt = counts.get(nn,0)
        st = status_for(nn, cnt)
        note = BLOCKED_REASONS.get(nn,"") if st=="blocked" else ""
        if nn in INFERRED and cnt>0:
            note = "Records inferred (conf 0.55) — pending primary extraction"
        lines.append("| dat_%s | %s | %d | %s | %s |" % (nn, DATASET_NAMES[nn], cnt, st, note))
    lines += ["","Generated: %s"%NOW]
    with open(os.path.join(REP,"COVERAGE_MATRIX.md"),"w",encoding="utf-8") as f:
        f.write("\n".join(lines))

def main():
    revert_boolean_all()
    add_missing_states()
    requote_string_booleans()
    counts = count_records()
    update_reports(counts)
    SUMMARY["datasets"] = counts
    print(json.dumps(SUMMARY, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()