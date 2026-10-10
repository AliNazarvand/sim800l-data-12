import re, sys, pathlib
from datetime import datetime, timezone
try:
    import yaml
except ImportError:
    print("ERROR: pip install pyyaml"); sys.exit(2)

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC  = ROOT / "sources" / "extracted"
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def read(p):
    try: return pathlib.Path(p).read_text(encoding="utf-8", errors="ignore")
    except Exception: return ""

def classify():
    at = hw1 = hw2 = ""
    for f in sorted(SRC.glob("*.txt")):
        t = read(f)
        if len(t) < 500: continue
        name = f.name
        if "AT Commands According" in t or ("+CMGS" in t and "19.1 Summary of CME" in t):
            at = t; print(f"  [AT] {name} ({len(t)})")
        elif "Hardware" in name or "Hardware_Design" in name:
            if "1.00" in name: hw1 = t; print(f"  [HW1] {name} ({len(t)})")
            elif "2.02" in name: hw2 = t; print(f"  [HW2] {name} ({len(t)})")
    return at, hw1, hw2

# ---- AT commands
CMD_RX = re.compile(
    r'(?m)^\s*(\d+(?:\.\d+){1,4})\s+'
    r'(AT\+[A-Z0-9_]+|AT[A-Z&]|A/|ATA|ATD|ATE|ATH|ATI|ATL|ATM|ATO|ATP|ATQ|ATS\d+|ATT|ATV|ATX|ATZ|\+\+\+|ATD><[a-z]+>)\s{1,6}'
    r'([A-Z][^\n]{2,90})')
CHAPTER = {"2":("V25TER","dat_01"),"3":("3GPP","dat_01"),"4":("SMS","dat_09"),
           "5":("STK","dat_01"),"6":("SIMCom","dat_01"),"7":("GPRS","dat_10"),
           "8":("TCPIP","dat_10"),"9":("IP","dat_10"),"10":("PING","dat_10"),
           "11":("HTTP","dat_11"),"12":("FTP","dat_11"),"13":("Location","dat_10"),
           "14":("Email","dat_10"),"15":("MMS","dat_11"),"16":("DDET","dat_12"),
           "17":("RECORD","dat_12"),"18":("TTS","dat_12")}
AUDIO = {"SIDET","CMIC","CRSL","CLVL","CMUT","CHF","CHFA","CEXTERNTONE","CMICBIAS",
         "CAAS","SVR","ECHO","SIMTONE","STTONE","CLDTMF","CALS","CALM"}
SIMSET = {"CPIN","CLCK","CPWD","CSIM","CRSM","CIMI","CCID","CSMINS","CSPN","CUSD","CSDT","SPIC"}
SSLSET = {"SSLCFG","SSLCONF","SSLOPEN","SSLSEND","SSLRECV","SSLCLOSE","SSLSETCERT","SSLSETKEY","SSLSETCA"}

def extract_at(text):
    out, seen = [], set()
    for m in CMD_RX.finditer(text):
        sec, cmd, desc = m.group(1), m.group(2).strip(), m.group(3).strip()
        if cmd in seen: continue
        seen.add(cmd)
        ch = sec.split(".")[0]
        cat, ds = CHAPTER.get(ch, ("General","dat_01"))
        name = cmd.replace("AT+","").replace("AT","").strip()
        if name in AUDIO:  cat, ds = "Audio","dat_12"
        elif name in SIMSET: cat, ds = "SIM","dat_13"
        elif name in SSLSET: cat, ds = "SSL","dat_11"
        out.append({"id":None,"category":cat,"command":cmd,"description":desc,
            "section":sec,
            "source":{"name":"SIM800 Series AT Command Manual","version":"V1.01",
                      "date":"2013-07-23","section":sec},
            "source_type":"primary","confidence":0.9,"status":"complete",
            "applicable_models":["SIM800L"],"notes":"","tags":["at_command"],
            "created_at":NOW,"updated_at":NOW,"_ds":ds})
    return out

# ---- FIXED: use LAST start with valid end (skip TOC)
def find_body(text, start_rx, end_rx, kind):
    all_starts = [m.start() for m in re.finditer(start_rx, text)]
    all_ends = [m.start() for m in re.finditer(end_rx, text)]
    print(f"  [DBG] {kind}: starts {all_starts}, ends {all_ends}")
    # Iterate from LAST start going backward, pick first with valid end > start + 500
    best = None
    for sp in sorted(all_starts, reverse=True):
        later = [ep for ep in all_ends if ep > sp + 500]
        if later:
            best = (sp, later[0])
            break
    if not best:
        print(f"  [DBG] {kind}: no valid (start,end) pair")
        return None
    print(f"  [DBG] {kind}: using start={best[0]} end={best[1]}  span={best[1]-best[0]} chars")
    return text[best[0]:best[1]]

def extract_errors(text, kind):
    if kind == "CME":
        body = find_body(text,
            r"19\.1 Summary of CME ERROR Codes",
            r"19\.2 Summary of CMS ERROR Codes", "CME")
        section = "19.1"
    else:
        body = find_body(text,
            r"19\.2 Summary of CMS ERROR Codes",
            r"19\.3 Summary of Unsolicited", "CMS")
        section = "19.2"
    if not body:
        print(f"  [DBG] {kind}: body NOT found")
        return []
    print(f"  [DBG] {kind}: body length={len(body)}")
    out = []
    for line in body.split("\n"):
        s = line.strip()
        if not s: continue
        if "SIM800 Series" in s or "Smart Machine" in s or "Code of <err>" in s: continue
        m = re.match(r'^(\d{1,5})\s+([A-Za-z][A-Za-z0-9 \-/&(),.\'`]{2,120})$', s)
        if not m: continue
        code = int(m.group(1)); meaning = m.group(2).strip()
        if len(meaning) < 4: continue
        if re.match(r'^[\d\s]+$', meaning): continue
        out.append({"id":None,"category":kind,"error_type":kind,
            "code":code,"meaning":meaning,"description":meaning,
            "source":{"name":"SIM800 Series AT Command Manual","version":"V1.01",
                      "date":"2013-07-23","section":section},
            "source_type":"primary","confidence":0.9,"status":"complete",
            "applicable_models":["SIM800L"],"notes":"","tags":[kind.lower()],
            "created_at":NOW,"updated_at":NOW})
    print(f"  [DBG] {kind}: parsed {len(out)} records")
    return out

# ---- URC
def extract_urcs(text):
    out, seen = [], set()
    all_starts = [m.start() for m in re.finditer(r"19\.3 Summary of Unsolicited Result Codes", text)]
    if not all_starts: return out
    sp = all_starts[-1]
    rest = text[sp:]
    em = re.search(r"(?m)^\s*20\s+AT Commands Examples\s*$", rest)
    body = rest[:em.start()] if em else rest[:60000]
    print(f"  [DBG] URC: body length={len(body)}")
    URC_KW = {"RING","RDY","NORMAL POWER DOWN","Call Ready","MO RING","MO CONNECTED",
              "UNDER-VOLTAGE POWER DOWN","UNDER-VOLTAGE WARNNING",
              "OVER-VOLTAGE POWER DOWN","OVER-VOLTAGE WARNNING","CHARGE-ONLY MODE"}
    for line in body.split("\n"):
        s = line.strip()
        if not s: continue
        if "Smart Machine" in s or "SIM800 Series" in s: continue
        m = re.match(r'^([+*][A-Z][A-Z0-9_]{1,20})\s*[:,\s]', s)
        token = None
        if m: token = m.group(1)
        else:
            for kw in URC_KW:
                if s == kw or s.startswith(kw + " ") or s.startswith(kw + "\t"):
                    token = kw; break
        if not token or len(token) < 3: continue
        if token in seen: continue
        seen.add(token)
        tail = s[len(token):].strip().lstrip(":,").strip()
        if len(tail) > 200: tail = tail[:200]
        out.append({"id":None,"category":"URC","urc_string":token,
            "trigger_event":tail,"format":token,
            "source":{"name":"SIM800 Series AT Command Manual","version":"V1.01",
                      "date":"2013-07-23","section":"19.3"},
            "source_type":"primary","confidence":0.85,"status":"complete",
            "applicable_models":["SIM800L"],"notes":"","tags":["urc"],
            "created_at":NOW,"updated_at":NOW})
    print(f"  [DBG] URC: parsed {len(out)} records")
    return out

# ---- Pins (per-version)
PIN_RX = re.compile(r'^([A-Z][A-Z0-9_]{1,20}(?:/[A-Z0-9_]+)?)\s+([\d][\d,\s]{0,140}?)\s+(I/O|IO|I|O|PWR|GND)\s+(.{2,160})$')

def extract_pins(text, version="V1.00"):
    out, seen = [], set()
    sm = re.search(r"Table 4:\s*Pin description", text)
    if not sm:
        print(f"  [DBG] Pin({version}): Table 4 marker NOT found")
        return out
    rest = text[sm.end():]
    em = re.search(r"3\.3\.", rest)
    body = rest[:em.start()] if em else rest[:30000]
    print(f"  [DBG] Pin({version}): body length={len(body)}")
    lines = body.split("\n")
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s: i += 1; continue
        m = PIN_RX.match(s)
        consumed = 1
        if not m and i+1 < len(lines):
            s2 = s + " " + lines[i+1].strip()
            m = PIN_RX.match(s2)
            if m: consumed = 2
        if not m: i += 1; continue
        name = m.group(1).strip()
        pins = re.sub(r'\s+','', m.group(2).strip())
        direction = m.group(3).strip()
        desc = m.group(4).strip()
        if name in seen: i += consumed; continue
        seen.add(name)
        out.append({"id":None,"category":"Pin","name":name,
            "pin_number":pins,"direction":direction,"function":desc,
            "source":{"name":"SIM800L_Hardware_Design","version":version,
                      "date":"2013-08-20" if version=="V1.00" else "2015-07-27",
                      "section":"Table 4"},
            "source_type":"primary","confidence":0.8,"status":"partial",
            "applicable_models":["SIM800L"],
            "notes":f"auto-extracted from {version}","tags":["pin"],
            "created_at":NOW,"updated_at":NOW})
        i += consumed
    print(f"  [DBG] Pin({version}): parsed {len(out)} records")
    return out

# ---- Power
def extract_power(text):
    out = []
    for fun, val in [("AT+CFUN=0",0.796),("AT+CFUN=1",1.02),("AT+CFUN=4",0.892)]:
        out.append({"id":None,"category":"MinimumFunctionality","mode":fun,"command":fun,
            "parameter":"current","value_typ":val,"unit":"mA",
            "condition":"sleep, BS-PA-MFRMS=9",
            "source":{"name":"SIM800L_Hardware_Design","version":"V1.00",
                      "date":"2013-08-20","section":"4.3.1 Table 7"},
            "source_type":"primary","confidence":0.9,"status":"complete",
            "applicable_models":["SIM800L"],"notes":"","tags":["power","cfun"],
            "created_at":NOW,"updated_at":NOW})
    facts = [
        ("Power down mode",60,"uA","typical"),("Sleep BS-PA-MFRMS=9",1.02,"mA","typical"),
        ("Sleep BS-PA-MFRMS=5",1.11,"mA","typical"),("Sleep BS-PA-MFRMS=2",1.88,"mA","typical"),
        ("Idle all bands",18.7,"mA","typical"),
        ("Voice GSM850 PCL=5",199.48,"mA","typical"),("Voice EGSM900 PCL=5",216.12,"mA","typical"),
        ("Voice DCS1800 PCL=5",146.48,"mA","typical"),("Voice PCS1900 PCL=5",131.77,"mA","typical"),
        ("GPRS 1Rx4Tx GSM850",453.57,"mA","typical"),("GPRS 1Rx4Tx EGSM900",344.74,"mA","typical"),
        ("GPRS 1Rx4Tx DCS1800",216.20,"mA","typical"),("GPRS 1Rx4Tx PCS1900",274.04,"mA","typical"),
        ("GPRS 3Rx2Tx GSM850",386.09,"mA","typical"),("GPRS 3Rx2Tx EGSM900",345.02,"mA","typical"),
        ("GPRS 3Rx2Tx DCS1800",216.79,"mA","typical"),("GPRS 3Rx2Tx PCS1900",239.12,"mA","typical"),
        ("GPRS 4Rx1Tx GSM850",212.69,"mA","typical"),("GPRS 4Rx1Tx EGSM900",227.95,"mA","typical"),
        ("GPRS 4Rx1Tx DCS1800",158.19,"mA","typical"),("GPRS 4Rx1Tx PCS1900",148.49,"mA","typical"),
        ("Peak Tx burst",2.0,"A","max"),
    ]
    for label,val,unit,kind in facts:
        out.append({"id":None,"category":"CurrentConsumption","mode":label,"command":None,
            "parameter":"current","value_typ":val,"unit":unit,"condition":"VBAT=3.8V",
            "source":{"name":"SIM800L_Hardware_Design","version":"V1.00",
                      "date":"2013-08-20","section":"6.8 Table 48"},
            "source_type":"primary","confidence":0.9,"status":"complete",
            "applicable_models":["SIM800L"],"notes":f"{kind} value","tags":["power"],
            "created_at":NOW,"updated_at":NOW})
    return out

def key_of(r, prefix):
    if prefix in ("dat_01","dat_09","dat_10","dat_11","dat_12","dat_13"): return r.get("command")
    if prefix == "dat_02": return r.get("urc_string")
    if prefix == "dat_03": return (r.get("error_type"), r.get("code"))
    if prefix == "dat_07": return r.get("name")
    if prefix == "dat_15": return (r.get("mode"), r.get("parameter"))
    return None

def load(path):
    if not path.exists(): return []
    try: d = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception: return []
    if isinstance(d, dict) and "records" in d: return d["records"] or []
    if isinstance(d, list): return d
    return []

def write_ds(prefix, recs, force_replace=False):
    files = list(DATA.glob(f"{prefix}_*.yaml")) + list(DATA.glob(f"{prefix}.yaml"))
    path = files[0] if files else DATA / f"{prefix}.yaml"
    existing = [] if force_replace else load(path)
    was_empty = len(existing) == 0
    idx = {}
    for r in existing:
        k = key_of(r, prefix)
        if k is not None: idx[k] = r
    added = updated = 0
    for r in recs:
        k = key_of(r, prefix)
        if k is None: added += 1; idx[("_k", len(idx))] = r; continue
        if k in idx:
            merged = dict(idx[k])
            for kk, vv in r.items():
                if vv not in (None,"",[],{}): merged[kk] = vv
            idx[k] = merged; updated += 1
        else:
            idx[k] = r; added += 1
    final = list(idx.values())
    for i, r in enumerate(final, 1):
        r["id"] = f"{prefix}_{i:04d}"
        r.pop("_ds", None)
    path.write_text(yaml.safe_dump({"records": final}, allow_unicode=True, sort_keys=False, width=200),
                    encoding="utf-8")
    return was_empty, len(final), added, updated, path.name

def main():
    print("== Extract ==")
    at, hw1, hw2 = classify()
    if not at: print("WARNING: AT Manual not found"); return
    at_cmds = extract_at(at)
    print(f"  AT: {len(at_cmds)}")
    cme = extract_errors(at, "CME")
    cms = extract_errors(at, "CMS")
    urcs = extract_urcs(at)

    # Pins: combine V2.02 (primary) + V1.00 (fill gaps)
    pins = []
    seen_names = set()
    if hw2:
        for r in extract_pins(hw2, "V2.02"):
            if r["name"] not in seen_names:
                pins.append(r); seen_names.add(r["name"])
    if hw1:
        for r in extract_pins(hw1, "V1.00"):
            if r["name"] not in seen_names:
                pins.append(r); seen_names.add(r["name"])
    print(f"  [DBG] Pin(total): {len(pins)} records from V1.00+V2.02")

    power = extract_power(hw1) if hw1 else []
    print(f"  Totals: AT={len(at_cmds)} CME={len(cme)} CMS={len(cms)} URC={len(urcs)} PIN={len(pins)} PWR={len(power)}")

    # SSL check
    if "AT+SSLCFG" in at or "AT+SSLOPEN" in at:
        print("  [INFO] SSL commands FOUND in AT Manual V1.01")
    else:
        print("  [INFO] SSL commands NOT in AT Manual V1.01 -> dat_17 stays blocked")

    by = {"dat_01":[],"dat_09":[],"dat_10":[],"dat_11":[],"dat_12":[],"dat_13":[]}
    for r in at_cmds:
        ds = r.pop("_ds","dat_01")
        if ds in by: by[ds].append(r)

    tasks = [("dat_01",by["dat_01"],False),("dat_02",urcs,True),
             ("dat_03",cme+cms,True),("dat_07",pins,True),
             ("dat_09",by["dat_09"],False),("dat_10",by["dat_10"],False),
             ("dat_11",by["dat_11"],False),("dat_12",by["dat_12"],False),
             ("dat_13",by["dat_13"],False),("dat_15",power,False)]
    print("== Write ==")
    for prefix, recs, force in tasks:
        if not recs:
            print(f"  {prefix}: SKIP"); continue
        was_empty, total, added, updated, fname = write_ds(prefix, recs, force_replace=force)
        state = "NEW" if was_empty else ("REPLACED" if force else "MERGE")
        print(f"  {prefix}: {state} total={total} added={added} updated={updated} ({fname})")

if __name__ == "__main__":
    main()