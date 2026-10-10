#!/usr/bin/env python3
"""پر کردن ۱۸ دیتاست از _index.json + استخراج cross-ref واقعی."""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pyyaml"])
    import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
EXTRACTED = ROOT / "sources" / "extracted"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

INDEX = json.loads((EXTRACTED / "_index.json").read_text(encoding="utf-8"))
AT_CMDS = INDEX.get("at_commands", {})
AT_DETAILS = INDEX.get("at_details", {})
SSL_KW = INDEX.get("ssl_keywords", {})
HW_PINS = INDEX.get("hw_pins", [])
TIMINGS = INDEX.get("timings", [])
POWER = INDEX.get("power_mgmt", [])

def rec(did, category, source_name, source_version, source_date, page, section,
        extra, status, confidence, notes=""):
    base = {
        "id": did,
        "category": category,
        "source": {
            "name": source_name,
            "version": source_version,
            "date": source_date,
            "page": str(page) if page else "",
            "section": section or "",
        },
        "source_type": "primary",
        "confidence": confidence,
        "status": status,
        "conflicts": [],
        "notes": notes,
        "tags": [category.lower()] if category else [],
        "applicable_models": ["SIM800L"],
        "created_at": NOW,
        "updated_at": NOW,
    }
    base.update(extra)
    return base

def write_yaml(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    header = f"# auto-generated at {NOW}\n"
    body = yaml.safe_dump(records, allow_unicode=True, sort_keys=False, default_flow_style=False)
    path.write_text(header + body, encoding="utf-8", errors="ignore")

# ============================================================
# 1) dat_01 — AT commands با syntax/params/examples
# ============================================================
def build_dat01():
    recs = []
    for i, (cmd, info) in enumerate(sorted(AT_CMDS.items()), 1):
        d = AT_DETAILS.get(cmd, {})
        recs.append(rec(
            f"dat_01_{i:04d}", "AT Command",
            "SIM800 Series AT Command Manual", "V1.01", "", info.get("page",""), "AT Commands",
            {
                "command": cmd,
                "mode": d.get("mode","unknown"),
                "syntax": d.get("syntax",""),
                "parameters": d.get("parameters",[]),
                "response_success": d.get("response_success","OK"),
                "response_error": d.get("response_error",""),
                "examples": d.get("examples",[]),
                "related_urcs": [],
                "related_states": [],
                "related_commands": [],
            },
            "partial", 0.85,
            notes="extracted from AT Manual V1.01 with syntax/params/examples" if d.get("syntax") else "command name only"
        ))
    return recs

# ============================================================
# 2) dat_02 — URCs
# ============================================================
def build_dat02():
    at_text = (EXTRACTED / "at_v1_01.txt").read_text(encoding="utf-8", errors="ignore") if (EXTRACTED / "at_v1_01.txt").exists() else ""
    urcs = {}
    for m in re.finditer(r'^\s*(\+[A-Z][A-Z0-9_]*)\s*:', at_text, re.MULTILINE):
        u = m.group(1)
        if u not in urcs:
            urcs[u] = {"page": "", "context": at_text[max(0,m.start()-50):m.end()+200].strip()}
    recs = []
    for i, (u, info) in enumerate(sorted(urcs.items()), 1):
        recs.append(rec(
            f"dat_02_{i:04d}", "URC",
            "SIM800 Series AT Command Manual", "V1.01", "", info.get("page",""), "URCs",
            {
                "urc_string": u,
                "trigger_event": info["context"][:150],
                "related_command": "",
                "related_state": "",
                "format": info["context"][:200],
                "examples": [],
                "timing": "",
                "suppression_method": "",
            },
            "partial", 0.7, notes="extracted via regex from AT Manual"
        ))
    return recs

# ============================================================
# 3) dat_03 — Error Codes
# ============================================================
def build_dat03():
    at_text = (EXTRACTED / "at_v1_01.txt").read_text(encoding="utf-8", errors="ignore") if (EXTRACTED / "at_v1_01.txt").exists() else ""
    codes = []
    seen = set()
    for m in re.finditer(r'\b(CME|CMS)\s+ERROR[:\s]+([0-9]+)', at_text):
        key = (m.group(1), m.group(2))
        if key in seen: continue
        seen.add(key)
        codes.append({"type": m.group(1), "code": m.group(2), "desc": m.group(0)})
    for m in re.finditer(r'^\s*(\d{1,4})\s+([A-Z][A-Za-z0-9 ,\-\.\(\)]{4,80})$', at_text, re.MULTILINE):
        key = ("CME", m.group(1))
        if key in seen: continue
        seen.add(key)
        codes.append({"type": "CME", "code": m.group(1), "desc": m.group(2).strip()})
    recs = []
    for i, c in enumerate(codes, 1):
        recs.append(rec(
            f"dat_03_{i:04d}", "Error Code",
            "SIM800 Series AT Command Manual", "V1.01", "", "", "Error Codes",
            {"error_type": c["type"], "code": c["code"], "meaning": c["desc"],
             "description": c["desc"], "related_commands": [], "recovery_steps": []},
            "partial", 0.7, notes="extracted via regex"
        ))
    return recs

# ============================================================
# 4) dat_04 — Timing
# ============================================================
def build_dat04():
    recs = []
    for i, t in enumerate(TIMINGS[:200], 1):
        recs.append(rec(
            f"dat_04_{i:04d}", "Timing",
            "SIM800H&SIM800L_Hardware_Design", "V2.02", "2015-07-27", "", "Timing",
            {"parameter": t["parameter"], "min": None, "typ": t["value"], "max": None,
             "unit": t["unit"], "condition": "", "related_command": None, "related_state": None},
            "partial", 0.75, notes="extracted via regex from hardware PDFs"
        ))
    return recs

# ============================================================
# 5) dat_05 — State Machine (استنتاجی از AT Manual)
# ============================================================
def build_dat05():
    states = ["OFF","POWER_ON","SIM_READY","NETWORK_SEARCH","REGISTERED",
              "PDP_ACTIVE","DATA_MODE","SMS_MODE","CALL_MODE","SLEEP","ERROR"]
    # جستجو در متن AT Manual برای شواهد هر state
    at_text = (EXTRACTED / "at_v1_01.txt").read_text(encoding="utf-8", errors="ignore") if (EXTRACTED / "at_v1_01.txt").exists() else ""
    recs = []
    for i, s in enumerate(states, 1):
        # keywords مرتبط
        keywords = s.lower().replace("_", " ").split()
        found_evidence = any(re.search(kw, at_text, re.IGNORECASE) for kw in keywords if len(kw) > 3)
        recs.append(rec(
            f"dat_05_{i:04d}", "State",
            "SIM800 Series AT Command Manual + Hardware Design", "V1.01/V2.02", "", "", "State Machine",
            {"state_name": s, "description": f"State {s}",
             "entry_conditions": [], "exit_conditions": [], "events": [], "actions": [],
             "related_commands": [], "related_urcs": [], "related_timings": []},
            "inferred", 0.4 if found_evidence else 0.3,
            notes=f"استنتاج‌شده؛ شواهد در متن AT Manual: {'موجود' if found_evidence else 'ضعیف'}"
        ))
    return recs

# ============================================================
# 6) dat_06 — Init Sequence (استنتاجی)
# ============================================================
def build_dat06():
    steps = [
        ("AT", "OK"),
        ("AT+CPIN?", "+CPIN: READY"),
        ("AT+CSQ", "+CSQ: <rssi>,<ber>"),
        ("AT+CREG?", "+CREG: <n>,<stat>"),
        ("AT+CGREG?", "+CGREG: <n>,<stat>"),
        ("AT+CGATT=1", "OK"),
        ("AT+CSTT", "OK"),
        ("AT+CIICR", "OK"),
        ("AT+CIFSR", "<IP>"),
        ("AT+CIPSTART", "CONNECT OK"),
        ("AT+CIPSEND", ">"),
        ("AT+CIPCLOSE", "CLOSE OK"),
    ]
    recs = []
    for i, (cmd, resp) in enumerate(steps, 1):
        recs.append(rec(
            f"dat_06_{i:04d}", "Init Sequence",
            "SIM800 Series AT Command Manual", "V1.01", "", "", "Init",
            {"step_order": i, "command": cmd, "expected_response": resp,
             "timeout_ms": 5000, "retry_count": 3, "failure_action": "retry",
             "dependency_step": i-1 if i > 1 else None},
            "inferred", 0.45, notes="توالی استنتاج‌شده از تجربه استاندارد SIM800L، نه استخراج مستقیم"
        ))
    return recs

# ============================================================
# 7) dat_07 — Hardware Reference
# ============================================================
def build_dat07():
    recs = []
    for i, p in enumerate(HW_PINS, 1):
        cat = "Power" if any(x in p for x in ("VBAT","VDD","GND")) else \
              "SIM" if "SIM" in p else \
              "UART" if p in ("TXD","RXD","RTS","CTS","DTR","DCD","RI") else \
              "Audio" if any(x in p for x in ("MIC","SPK")) else \
              "RF" if "RF" in p or "ANT" in p else \
              "Reset" if "RESET" in p else \
              "PWRKEY" if "PWRKEY" in p else "GPIO"
        recs.append(rec(
            f"dat_07_{i:04d}", cat,
            "SIM800H&SIM800L_Hardware_Design", "V2.02", "2015-07-27", "", "Pinout",
            {"name": p, "pin_number": "", "direction": "",
             "voltage_min": None, "voltage_typ": None, "voltage_max": None,
             "current_typ": None, "current_max": None,
             "function": p, "alternate_function": None, "pull_up_down": None,
             "esd_rating": None, "impedance": None, "decoupling": None},
            "partial", 0.75,
            notes="نام پین‌ها استخراج شده؛ جزئیات (voltage/pin_number) نیازمند جدول‌کشی دقیق‌تر"
        ))
    return recs

# ============================================================
# 8) dat_09..dat_13 — دسته‌بندی AT commands
# ============================================================
def filter_cmds(cmds_set):
    return [c for c in AT_CMDS if c in cmds_set]

def build_dat09():
    sms = filter_cmds({"+CMGF","+CSMS","+CPMS","+CMGS","+CMGR","+CMGL","+CMGD","+CMGW",
                       "+CSCA","+CSCS","+CSMP","+CNMI","+CSDH","+CMEE"})
    return [rec(
        f"dat_09_{i:04d}", "SMS",
        "SIM800 Series AT Command Manual", "V1.01", "", AT_CMDS[c].get("page",""), "SMS",
        {"mode": "text", "command": c, "syntax": AT_DETAILS.get(c,{}).get("syntax",""),
         "parameters": AT_DETAILS.get(c,{}).get("parameters",[]),
         "response": "OK", "examples": AT_DETAILS.get(c,{}).get("examples",[]),
         "related_urcs": [], "encoding": "GSM7", "storage": "SM",
         "concat_sms": False, "delivery_report": False},
        "partial", 0.85
    ) for i, c in enumerate(sorted(sms), 1)]

def build_dat10():
    gprs = filter_cmds({"+CGDCONT","+CGATT","+CGACT","+CGCONTRDP","+CGPADDR","+CSTT",
                        "+CIICR","+CIFSR","+CIPSTART","+CIPOPEN","+CIPSEND","+CIPCLOSE",
                        "+CIPSHUT","+CIPSTATUS","+CIPRXGET","+CIPMUX","+CIPQSEND",
                        "+CIPDDREM","+CIPMODE","+CIPCCFG","+CSQ","+CREG","+CGREG",
                        "+CEREG","+CDNSGIP"})
    return [rec(
        f"dat_10_{i:04d}", "GPRS/Data",
        "SIM800 Series AT Command Manual", "V1.01", "", AT_CMDS[c].get("page",""), "GPRS",
        {"command": c, "syntax": AT_DETAILS.get(c,{}).get("syntax",""),
         "parameters": AT_DETAILS.get(c,{}).get("parameters",[]),
         "response": "OK", "examples": AT_DETAILS.get(c,{}).get("examples",[]),
         "related_urcs": [], "related_states": [], "related_commands": []},
        "partial", 0.85
    ) for i, c in enumerate(sorted(gprs), 1)]

def build_dat11():
    net = [c for c in AT_CMDS if c.startswith(("+HTTP","+FTP","+SSL"))]
    recs = []
    for i, c in enumerate(sorted(net), 1):
        cat = "HTTP" if c.startswith("+HTTP") else "FTP" if c.startswith("+FTP") else "SSL"
        recs.append(rec(
            f"dat_11_{i:04d}", cat,
            "SIM800 Series AT Command Manual", "V1.01", "", AT_CMDS[c].get("page",""), cat,
            {"command": c, "syntax": AT_DETAILS.get(c,{}).get("syntax",""),
             "parameters": AT_DETAILS.get(c,{}).get("parameters",[]),
             "response": "OK", "examples": AT_DETAILS.get(c,{}).get("examples",[]),
             "related_commands": []},
            "partial", 0.75
        ))
    return recs

def build_dat12():
    audio = filter_cmds({"+CLVL","+CMUT","+CRSL","+CHFA","+CCMX","+CMIC"})
    return [rec(
        f"dat_12_{i:04d}", "Audio",
        "SIM800 Series AT Command Manual", "V1.01", "", AT_CMDS[c].get("page",""), "Audio",
        {"command": c, "syntax": AT_DETAILS.get(c,{}).get("syntax",""),
         "parameters": AT_DETAILS.get(c,{}).get("parameters",[]),
         "response": "OK", "examples": AT_DETAILS.get(c,{}).get("examples",[]),
         "related_commands": []},
        "partial", 0.7
    ) for i, c in enumerate(sorted(audio), 1)]

def build_dat13():
    sim = filter_cmds({"+CPIN","+CLCK","+CPWD","+CSIM","+CRSM","+CIMI","+CCID",
                       "+CSMINS","+CSPN","+CUSD"})
    return [rec(
        f"dat_13_{i:04d}", "SIM",
        "SIM800 Series AT Command Manual", "V1.01", "", AT_CMDS[c].get("page",""), "SIM",
        {"command": c, "syntax": AT_DETAILS.get(c,{}).get("syntax",""),
         "parameters": AT_DETAILS.get(c,{}).get("parameters",[]),
         "response": "OK", "examples": AT_DETAILS.get(c,{}).get("examples",[]),
         "related_urcs": [], "hardware_pins": []},
        "partial", 0.85
    ) for i, c in enumerate(sorted(sim), 1)]

# ============================================================
# 9) dat_14 — Operator/APN (نمونه‌های external)
# ============================================================
def build_dat14():
    # ۵۰ رکورد نمونه از اپراتورهای GSM/GPRS معتبر
    # منبع: mcc-mnc.com (public)
    ops = [
        ("310","260","United States","US","T-Mobile","T-Mobile","GSM","fast.t-mobile.com"),
        ("310","410","United States","US","AT&T","AT&T","GSM","phone"),
        ("310","150","United States","US","AT&T","AT&T","GSM","phone"),
        ("310","030","United States","US","AT&T","AT&T","GSM","phone"),
        ("311","480","United States","US","Verizon","Verizon","GSM","vzwinternet"),
        ("234","15","United Kingdom","GB","Vodafone","Vodafone","GSM","internet"),
        ("234","10","United Kingdom","GB","O2","O2","GSM","mobile.o2.co.uk"),
        ("234","20","United Kingdom","GB","3","Three","GSM","three.co.uk"),
        ("234","30","United Kingdom","GB","EE","EE","GSM","everytime"),
        ("234","33","United Kingdom","GB","EE","Orange","GSM","orangeinternet"),
        ("262","01","Germany","DE","Telekom","T-Mobile","GSM","internet.t-mobile"),
        ("262","02","Germany","DE","Vodafone","Vodafone","GSM","web.vodafone.de"),
        ("262","03","Germany","DE","O2","O2","GSM","internet"),
        ("262","07","Germany","DE","O2","O2","GSM","internet"),
        ("208","01","France","FR","Orange","Orange","GSM","orange.fr"),
        ("208","10","France","FR","SFR","SFR","GSM","websfr"),
        ("208","20","France","FR","Bouygues","Bouygues","GSM","mmsbouygtel.com"),
        ("222","01","Italy","IT","TIM","TIM","GSM","ibox.tim.it"),
        ("222","10","Italy","IT","Vodafone","Vodafone","GSM","web.omnitel.it"),
        ("222","88","Italy","IT","Wind","Wind","GSM","internet.wind"),
        ("214","01","Spain","ES","Vodafone","Vodafone","GSM","airtelnet.es"),
        ("214","03","Spain","ES","Orange","Orange","GSM","orangeworld"),
        ("214","07","Spain","ES","Movistar","Movistar","GSM","movistar.es"),
        ("204","04","Netherlands","NL","Vodafone","Vodafone","GSM","web.vodafone.de"),
        ("204","08","Netherlands","NL","KPN","KPN","GSM","internet"),
        ("204","16","Netherlands","NL","T-Mobile","T-Mobile","GSM","internet"),
        ("286","01","Turkey","TR","Turkcell","Turkcell","GSM","internet"),
        ("286","02","Turkey","TR","Vodafone","Vodafone","GSM","internet"),
        ("286","03","Turkey","TR","Turk Telekom","Avea","GSM","internet"),
        ("432","11","Iran","IR","MCI","Hamrah-e Aval","GSM","mci-gprs"),
        ("432","35","Iran","IR","MTN Irancell","Irancell","GSM","mtnirancell"),
        ("432","14","Iran","IR","Rightel","Rightel","GSM","rightel"),
        ("440","10","Japan","JP","NTT docomo","docomo","GSM","mopera.net"),
        ("440","20","Japan","JP","SoftBank","SoftBank","GSM","softbank"),
        ("440","50","Japan","JP","KDDI","au","GSM","au.au-net.ne.jp"),
        ("450","05","South Korea","KR","SK Telecom","SKT","GSM","internet"),
        ("450","08","South Korea","KR","KT","KT","GSM","internet"),
        ("450","06","South Korea","KR","LG U+","LGU+","GSM","internet"),
        ("460","00","China","CN","China Mobile","China Mobile","GSM","cmnet"),
        ("460","01","China","CN","China Unicom","China Unicom","GSM","3gnet"),
        ("460","03","China","CN","China Telecom","China Telecom","GSM","ctnet"),
        ("404","10","India","IN","Airtel","Airtel","GSM","airtelgprs.com"),
        ("404","45","India","IN","Airtel","Airtel","GSM","airtelgprs.com"),
        ("404","20","India","IN","Vodafone","Vodafone","GSM","www"),
        ("404","11","India","IN","Vodafone","Vodafone","GSM","www"),
        ("405","840","India","IN","Jio","Jio","GSM","jionet"),
        ("505","01","Australia","AU","Telstra","Telstra","GSM","telstra.internet"),
        ("505","02","Australia","AU","Optus","Optus","GSM","yesinternet"),
        ("505","03","Australia","AU","Vodafone","Vodafone","GSM","vfinternet.au"),
        ("724","05","Brazil","BR","Claro","Claro","GSM","claro.com.br"),
        ("724","06","Brazil","BR","Vivo","Vivo","GSM","zap.vivo.com.br"),
        ("724","10","Brazil","BR","TIM","TIM","GSM","tim.br"),
    ]
    recs = []
    for i, (mcc, mnc, country, cc, op, brand, net, apn) in enumerate(ops, 1):
        r = rec(
            f"dat_14_{i:04d}", "MCC/MNC",
            "mcc-mnc.com", "public", "", "", "Operator/APN",
            {"mcc": mcc, "mnc": mnc, "country": country, "country_code": cc,
             "operator": op, "brand": brand, "network_type": net,
             "apn_list": [apn], "source_url": "https://www.mcc-mnc.com/"},
            "partial", 0.7, notes="external reference; برای کامل شدن نیاز به تطبیق دقیق با mcc-mnc.com"
        )
        r["source_type"] = "external"
        recs.append(r)
    return recs

# ============================================================
# 10) dat_15 — Power Management
# ============================================================
def build_dat15():
    recs = []
    hw_text = ""
    for name in ("v2.02.txt","v1.00.txt"):
        p = EXTRACTED / name
        if p.exists():
            hw_text += p.read_text(encoding="utf-8", errors="ignore") + "\n"
    at_text = ""
    p = EXTRACTED / "at_v1_01.txt"
    if p.exists():
        at_text = p.read_text(encoding="utf-8", errors="ignore")

    if "Sleep" in hw_text or "AT+CSCLK" in at_text:
        recs.append(rec(
            "dat_15_0001", "Sleep",
            "SIM800H&SIM800L_Hardware_Design", "V2.02", "2015-07-27", "", "Sleep Mode",
            {"mode": "Sleep Mode 1", "command": "AT+CSCLK=1", "parameter": "DTR",
             "value_min": 0, "value_typ": 0, "value_max": 1, "unit": "logic",
             "condition": "DTR high", "wake_source": "DTR low",
             "related_commands": ["+CSCLK"], "related_states": ["SLEEP"]},
            "inferred", 0.5, notes="شواهد در PDF موجود است؛ استنتاج از الگو"
        ))
    if "+CSCLK" in AT_CMDS:
        recs.append(rec(
            "dat_15_0002", "CSCLK",
            "SIM800 Series AT Command Manual", "V1.01", "", "", "CSCLK",
            {"mode": "Slow Clock", "command": "AT+CSCLK", "parameter": "mode",
             "value_min": 0, "value_typ": 0, "value_max": 2, "unit": "int",
             "condition": "", "wake_source": "DTR",
             "related_commands": ["+CSCLK"], "related_states": ["SLEEP"]},
            "partial", 0.75, notes="AT+CSCLK در AT Manual موجود است"
        ))
    if "+CFUN" in AT_CMDS:
        recs.append(rec(
            "dat_15_0003", "CFUN",
            "SIM800 Series AT Command Manual", "V1.01", "", "", "CFUN",
            {"mode": "Minimum Functionality", "command": "AT+CFUN=0", "parameter": "fun",
             "value_min": 0, "value_typ": 0, "value_max": 4, "unit": "int",
             "condition": "", "wake_source": "",
             "related_commands": ["+CFUN"], "related_states": ["OFF"]},
            "partial", 0.75
        ))
    if "+CSDT" in AT_CMDS:
        recs.append(rec(
            "dat_15_0004", "CSDT",
            "SIM800 Series AT Command Manual", "V1.01", "", "", "CSDT",
            {"mode": "Sleep", "command": "AT+CSDT", "parameter": "mode",
             "value_min": 0, "value_typ": 0, "value_max": 1, "unit": "int",
             "condition": "", "wake_source": "",
             "related_commands": ["+CSDT"], "related_states": ["SLEEP"]},
            "partial", 0.75
        ))
    return recs

# ============================================================
# 11) dat_17 — SSL (استخراج واقعی)
# ============================================================
def build_dat17():
    ssl_cmds = [c for c in AT_CMDS if c.startswith("+SSL")]
    recs = []
    for i, c in enumerate(sorted(ssl_cmds), 1):
        d = AT_DETAILS.get(c, {})
        recs.append(rec(
            f"dat_17_{i:04d}", "SSL",
            "SIM800 Series AT Command Manual", "V1.01", "", AT_CMDS[c].get("page",""), "SSL",
            {"command": c, "syntax": d.get("syntax",""), "parameters": d.get("parameters",[]),
             "response": "OK", "examples": d.get("examples",[]),
             "tls_version": "", "cipher_suite": "", "cert_format": "PEM",
             "key_format": "PEM", "storage": "Module internal", "limits": "",
             "related_commands": []},
            "partial", 0.7
        ))
    return recs

# ============================================================
# Cross-ref: پر کردن فیلدهای related_*
# ============================================================
def populate_crossrefs(all_data):
    cmd_ids = {r.get("command"): r.get("id") for r in all_data.get("dat_01", []) if r.get("command")}
    state_ids = {r.get("state_name"): r.get("id") for r in all_data.get("dat_05", []) if r.get("state_name")}
    urc_ids = {r.get("urc_string"): r.get("id") for r in all_data.get("dat_02", []) if r.get("urc_string")}

    # dat_09..dat_13, dat_15, dat_17: related_commands
    for key in ("dat_09","dat_10","dat_11","dat_12","dat_13","dat_15","dat_17"):
        for r in all_data.get(key, []):
            c = r.get("command")
            if c and c in cmd_ids:
                r["related_commands"] = list(set(r.get("related_commands", []) + [cmd_ids[c]]))
    return all_data

# ============================================================
# main
# ============================================================
def main():
    DATA.mkdir(parents=True, exist_ok=True)
    builders = {
        "dat_01": (build_dat01, "dat_01_at_command.yaml"),
        "dat_02": (build_dat02, "dat_02_urc.yaml"),
        "dat_03": (build_dat03, "dat_03_error_code.yaml"),
        "dat_04": (build_dat04, "dat_04_timing_timeout.yaml"),
        "dat_05": (build_dat05, "dat_05_state_machine.yaml"),
        "dat_06": (build_dat06, "dat_06_init_sequence.yaml"),
        "dat_07": (build_dat07, "dat_07_hardware_reference.yaml"),
        "dat_09": (build_dat09, "dat_09_sms.yaml"),
        "dat_10": (build_dat10, "dat_10_gprs_data.yaml"),
        "dat_11": (build_dat11, "dat_11_http_ftp_ssl.yaml"),
        "dat_12": (build_dat12, "dat_12_audio.yaml"),
        "dat_13": (build_dat13, "dat_13_sim_management.yaml"),
        "dat_14": (build_dat14, "dat_14_operator_apn.yaml"),
        "dat_15": (build_dat15, "dat_15_power_management.yaml"),
        "dat_17": (build_dat17, "dat_17_certificate_key_store.yaml"),
    }
    all_data = {}
    for key, (fn, fname) in builders.items():
        try:
            recs = fn()
            all_data[key] = recs
            print(f"  {key}: {len(recs)} رکورد")
        except Exception as e:
            print(f"  {key}: ERROR - {e}")
            all_data[key] = []

    # دیتاست‌های blocked/deferred
    for key, fname in [("dat_08","dat_08_firmware_compatibility.yaml"),
                       ("dat_16","dat_16_board_evb.yaml"),
                       ("dat_18","dat_18_certification.yaml")]:
        all_data[key] = []

    # Cross-ref
    all_data = populate_crossrefs(all_data)

    # نوشتن
    for key, (fn, fname) in builders.items():
        write_yaml(DATA / fname, all_data.get(key, []))
    for key, fname in [("dat_08","dat_08_firmware_compatibility.yaml"),
                       ("dat_16","dat_16_board_evb.yaml"),
                       ("dat_18","dat_18_certification.yaml")]:
        write_yaml(DATA / fname, [])
    return 0

if __name__ == "__main__":
    sys.exit(main())