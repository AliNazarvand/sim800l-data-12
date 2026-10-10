#!/usr/bin/env python3
"""Real cross-reference validator v2."""
import os, glob, yaml
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT,"data")
REP  = os.path.join(ROOT,"reports")

def load(fn):
    p = os.path.join(DATA,fn)
    if not os.path.exists(p): return []
    try:
        with open(p,"r",encoding="utf-8") as f:
            doc = yaml.safe_load(f) or {}
    except Exception:
        return []
    return doc.get("records",[]) if isinstance(doc,dict) else (doc or [])

def main():
    cmds = set()
    for r in load("dat_01_at_command.yaml"):
        c = r.get("command") or r.get("syntax") or ""
        if c: cmds.add(str(c).strip())
    urcs = set()
    for r in load("dat_02_urc.yaml"):
        u = r.get("urc_string") or ""
        if u: urcs.add(str(u).strip())
    states = set()
    for r in load("dat_05_state_machine.yaml"):
        s = r.get("state_name")
        if s: states.add(str(s).strip())
    pins = set()
    for r in load("dat_07_hardware_reference.yaml"):
        n = r.get("name")
        if n: pins.add(str(n).strip())

    lines = ["# Cross-Reference Report (v2)","",
             "- dat_01 commands: %d"%len(cmds),
             "- dat_02 URCs: %d"%len(urcs),
             "- dat_05 states: %d"%len(states),
             "- dat_07 pins: %d"%len(pins),""]

    for fn in sorted(glob.glob(os.path.join(DATA,"*.yaml"))):
        base = os.path.basename(fn)
        if base in ("dat_01_at_command.yaml","dat_02_urc.yaml",
                    "dat_05_state_machine.yaml","dat_07_hardware_reference.yaml"):
            continue
        recs = load(base)
        mc, ms, mu, mp = [], [], [], []
        for r in recs:
            for k in ("command","related_command","related_commands"):
                v = r.get(k)
                if isinstance(v,str) and v.startswith("+") and v not in cmds:
                    mc.append((r.get("id"),v))
                elif isinstance(v,list):
                    for x in v:
                        if isinstance(x,str) and x.startswith("+") and x not in cmds:
                            mc.append((r.get("id"),x))
            rs = r.get("related_state") or ""
            if rs and rs not in states and rs not in ("","unknown"):
                ms.append((r.get("id"),rs))
            ru = r.get("related_urc") or ""
            if ru and ru not in urcs and ru not in ("","unknown"):
                mu.append((r.get("id"),ru))
            for pk in ("hardware_pins","related_pins"):
                v = r.get(pk)
                if isinstance(v,list):
                    for p in v:
                        if isinstance(p,str) and p and p not in pins:
                            mp.append((r.get("id"),p))
        if mc or ms or mu or mp:
            lines.append("## %s"%base)
            if mc: lines.append("- %d unresolved command refs"%len(mc))
            if ms: lines.append("- %d unresolved state refs"%len(ms))
            if mu: lines.append("- %d unresolved URC refs"%len(mu))
            if mp: lines.append("- %d unresolved pin refs"%len(mp))
            lines.append("")
    with open(os.path.join(REP,"CROSS_REF_REPORT.md"),"w",encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Cross-ref report written.")

if __name__ == "__main__":
    main()