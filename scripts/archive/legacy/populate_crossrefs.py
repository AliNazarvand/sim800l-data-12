import pathlib, sys
from datetime import datetime, timezone
try:
    import yaml
except ImportError:
    print("PyYAML required"); sys.exit(2)

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

def load(p):
    if not p.exists(): return []
    try: d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except Exception: return []
    if isinstance(d, dict) and "records" in d: return d["records"] or []
    if isinstance(d, list): return d
    return []

def save(recs, path):
    path.write_text(yaml.safe_dump({"records":recs}, allow_unicode=True, sort_keys=False, width=200),
                    encoding="utf-8")

def find(prefix):
    fs = list(DATA.glob(f"{prefix}_*.yaml")) + list(DATA.glob(f"{prefix}.yaml"))
    return fs[0] if fs else None

# Build cmd_idx from ALL datasets (not just dat_01)
cmd_idx = {}
for prefix in ["dat_01","dat_09","dat_10","dat_11","dat_12","dat_13"]:
    p = find(prefix)
    if not p: continue
    for r in load(p):
        c = r.get("command")
        if c and c not in cmd_idx:
            cmd_idx[c] = r["id"]
print(f"cmd_idx: {len(cmd_idx)} commands (from all datasets)")

# Domain groups
GROUPS = {
    "SMS":["AT+CMGD","AT+CMGF","AT+CMGL","AT+CMGR","AT+CMGS","AT+CMGW","AT+CMSS","AT+CNMI",
           "AT+CPMS","AT+CRES","AT+CSAS","AT+CSCA","AT+CSCB","AT+CSDH","AT+CSMP","AT+CSMS",
           "AT+CMGDA","AT+CMGHEX","AT+CCODE","AT+SCLASS0"],
    "GPRS":["AT+CGATT","AT+CGDCONT","AT+CGQMIN","AT+CGQREQ","AT+CGACT","AT+CGDATA","AT+CGPADDR",
            "AT+CGCLASS","AT+CGEREP","AT+CGREG","AT+CGSMS","AT+CSTT","AT+CIICR","AT+CIFSR",
            "AT+CIPSHUT","AT+CIPSTATUS","AT+CIPMUX","AT+CIPSTART","AT+CIPSEND","AT+CIPQSEND",
            "AT+CIPACK","AT+CIPCLOSE","AT+CLPORT","AT+CDNSCFG","AT+CDNSGIP","AT+CIPHEAD",
            "AT+CIPATS","AT+CIPSPRT","AT+CIPSERVER","AT+CIPCSGP","AT+CIPSRIP","AT+CIPDPDP",
            "AT+CIPMODE","AT+CIPCCFG","AT+CIPSHOWTP","AT+CIPUDPMODE","AT+CIPRXGET","AT+CIPSCONT",
            "AT+CIPRDTIMER","AT+CIPSGTXT","AT+SAPBR"],
    "HTTP_FTP_SSL":["AT+HTTPINIT","AT+HTTPTERM","AT+HTTPPARA","AT+HTTPDATA","AT+HTTPACTION",
                    "AT+HTTPREAD","AT+HTTPSCONT","AT+HTTPSTATUS","AT+FTPPORT","AT+FTPMODE",
                    "AT+FTPTYPE","AT+FTPPUTOPT","AT+FTPCID","AT+FTPREST","AT+FTPSERV","AT+FTPUN",
                    "AT+FTPPW","AT+FTPGETNAME","AT+FTPGETPATH","AT+FTPPUTNAME","AT+FTPPUTPATH",
                    "AT+FTPGET","AT+FTPPUT","AT+FTPSCONT","AT+FTPDELE","AT+FTPSIZE","AT+FTPSTATE",
                    "AT+FTPEXTPUT","AT+FTPMKD","AT+FTPRMD","AT+FTPLIST"],
    "AUDIO":["AT+SIDET","AT+CMIC","AT+CRSL","AT+CLVL","AT+CMUT","AT+CHF","AT+CHFA",
             "AT+CEXTERNTONE","AT+CMICBIAS","AT+CAAS","AT+SVR","AT+ECHO","AT+SIMTONE",
             "AT+STTONE","AT+CLDTMF","AT+CALS","AT+CALM","AT+VTS","AT+VTD"],
    "SIM":["AT+CPIN","AT+CLCK","AT+CPWD","AT+CSIM","AT+CRSM","AT+CIMI","AT+CCID","AT+CSMINS",
           "AT+CSPN","AT+CUSD","AT+CSDT","AT+SPIC","AT+CGID"],
    "POWER":["AT+CFUN","AT+CSCLK","AT+CPOWD","AT+CBC","AT+CMTE"],
    "NET":["AT+CREG","AT+CGREG","AT+COPS","AT+CSQ","AT+CPOL","AT+COPN","AT+CENG","AT+CBAND"],
    "CALL":["ATA","ATH","ATD","ATDL","AT+CHLD","AT+CCWA","AT+CLIP","AT+CLIR","AT+COLP",
            "AT+CCFC","AT+CLCC","AT+CRC"],
}

def siblings(cmd):
    for dom, cmds in GROUPS.items():
        if cmd in cmds:
            return [c for c in cmds if c != cmd]
    return []

# Annotate dat_09..dat_13
total_refs = 0
for prefix in ["dat_09","dat_10","dat_11","dat_12","dat_13"]:
    p = find(prefix)
    if not p: continue
    recs = load(p)
    if not recs: continue
    n = 0
    for r in recs:
        cmd = r.get("command")
        if not cmd: continue
        refs = [cmd_idx[s] for s in siblings(cmd) if s in cmd_idx]
        refs = list(dict.fromkeys(refs))[:8]
        if refs:
            r["related_commands"] = refs
            n += 1; total_refs += len(refs)
    save(recs, p)
    print(f"  {prefix}: {n}/{len(recs)} annotated, total_refs={total_refs}")

# Annotate dat_02
p2 = find("dat_02")
if p2:
    recs = load(p2)
    URC2CMD = {
        "+CMTI":"AT+CNMI","+CMT":"AT+CNMI","+CDS":"AT+CNMI","+CBM":"AT+CNMI",
        "+CLIP":"AT+CLIP","+CRING":"AT+CRC","+CREG":"AT+CREG","+CGREG":"AT+CGREG",
        "+CSQ":"AT+CSQ","+CPIN":"AT+CPIN","+CSMINS":"AT+CSMINS","+CUSD":"AT+CUSD",
        "+CCWA":"AT+CCWA","+CSSU":"AT+CSSN","+CSSI":"AT+CSSN","+COLP":"AT+COLP",
        "+CLCC":"AT+CLCC","+CBC":"AT+CBC","+CENG":"AT+CENG","+CHF":"AT+CHF","+CMTE":"AT+CMTE",
        "+HTTPACTION":"AT+HTTPACTION","+FTPGET":"AT+FTPGET","+FTPPUT":"AT+FTPPUT",
        "+FTPDELE":"AT+FTPDELE","+FTPSIZE":"AT+FTPSIZE","+CDNSGIP":"AT+CDNSGIP",
        "RDY":"AT+IPR","NORMAL POWER DOWN":"AT+CPOWD","RING":"ATA",
        "MO RING":"AT+MORING","MO CONNECTED":"AT+MORING","+CTZV":"AT+CLTS",
        "+CLTS":"AT+CLTS","+IPD":"AT+CIPHEAD","+RECEIVE":"AT+CIPHEAD",
        "+RECV":"AT+CIPSRIP","+PDP":"AT+CIPSHUT","+SAPBR":"AT+SAPBR",
        "+STKPCI":"AT+STKPCIS","+SIMTONE":"AT+SIMTONE","+STTONE":"AT+STTONE",
        "+CREC":"AT+CREC","+CTTS":"AT+CTTS","+DTMF":"AT+DDET","+CALV":"AT+CALA",
        "+CCWV":"AT+CCWE","+CSQN":"AT+EXUNSOL","+FTPSCONT":"AT+FTPSCONT",
        "+HTTPSCONT":"AT+HTTPSCONT","+CIPSCONT":"AT+CIPSCONT",
    }
    n = 0
    for r in recs:
        u = r.get("urc_string","")
        c = URC2CMD.get(u)
        if c and c in cmd_idx:
            r["related_command"] = cmd_idx[c]
            n += 1
    save(recs, p2)
    print(f"  dat_02: {n}/{len(recs)} URCs linked")

print(f"total_refs: {total_refs}")