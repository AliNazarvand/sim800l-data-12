#!/usr/bin/env python3
"""
Master extractor and dataset population for sim800l-data.
Extracts text from the source PDFs, parses AT commands, URCs, error codes,
and hardware pin definitions, then writes YAML data files and reports.
Idempotent: safe to run multiple times.
"""
import os, re, sys, json, glob, subprocess, io
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "sources", "originals")
EXT  = os.path.join(ROOT, "sources", "extracted")
DATA = os.path.join(ROOT, "data")
REP  = os.path.join(ROOT, "reports")
NOW  = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

for d in (EXT, DATA, REP):
    os.makedirs(d, exist_ok=True)

SUMMARY = {
    "pdfs_found": [],
    "pdfs_extracted": [],
    "extraction_backend": {},
    "datasets_populated": {},
    "datasets_blocked": [],
    "datasets_empty": [],
    "errors": []
}

# ---------------------------------------------------------------------
# PDF text extraction with multiple fallbacks
# ---------------------------------------------------------------------
def try_import(name):
    try:
        __import__(name)
        return True
    except Exception:
        return False

def extract_pdf_text(pdf_path):
    # pdfplumber
    if try_import("pdfplumber"):
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                parts = []
                for page in pdf.pages:
                    try:
                        parts.append(page.extract_text() or "")
                    except Exception:
                        parts.append("")
                text = "\n".join(parts)
                if len(text.strip()) > 500:
                    return text, "pdfplumber"
        except Exception as e:
            SUMMARY["errors"].append("pdfplumber failed on %s: %s" % (pdf_path, e))
    # pypdf
    if try_import("pypdf"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(pdf_path)
            parts = []
            for p in reader.pages:
                try:
                    parts.append(p.extract_text() or "")
                except Exception:
                    parts.append("")
            text = "\n".join(parts)
            if len(text.strip()) > 500:
                return text, "pypdf"
        except Exception as e:
            SUMMARY["errors"].append("pypdf failed on %s: %s" % (pdf_path, e))
    # PyPDF2
    if try_import("PyPDF2"):
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(pdf_path)
            parts = []
            for p in reader.pages:
                try:
                    parts.append(p.extract_text() or "")
                except Exception:
                    parts.append("")
            text = "\n".join(parts)
            if len(text.strip()) > 500:
                return text, "PyPDF2"
        except Exception as e:
            SUMMARY["errors"].append("PyPDF2 failed on %s: %s" % (pdf_path, e))
    # pdftotext (poppler)
    try:
        out = os.path.join(EXT, "_tmp.txt")
        r = subprocess.run(["pdftotext", "-layout", pdf_path, out],
                           capture_output=True)
        if r.returncode == 0 and os.path.exists(out):
            with open(out, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            try: os.remove(out)
            except Exception: pass
            if len(text.strip()) > 500:
                return text, "pdftotext"
    except Exception as e:
        SUMMARY["errors"].append("pdftotext failed on %s: %s" % (pdf_path, e))
    return None, None

# ---------------------------------------------------------------------
# AT command / URC / error parsing
# ---------------------------------------------------------------------
AT_CMD_RE  = re.compile(r'\bAT\+([A-Z][A-Z0-9]{0,15})\b')
URC_RE     = re.compile(r'(?m)^\s*(\+[A-Z][A-Z0-9]{1,15}:|RING\b|NO CARRIER\b|BUSY\b|ERROR\b|OK\b|CONNECT\b)')
CME_RE     = re.compile(r'\+CME ERROR:\s*<?(\d{1,3})>?\s*[:\-]?\s*([^\n]{0,120})')
CMS_RE     = re.compile(r'\+CMS ERROR:\s*<?(\d{1,3})>?\s*[:\-]?\s*([^\n]{0,120})')
VOLT_RE    = re.compile(r'(\d+\.\d+)\s*V\b')
CURR_RE    = re.compile(r'(\d+\.?\d*)\s*mA\b')

CATEGORY_RULES = [
    (("CMG","CMGR","CMGL","CMGD","CMGW","CMGF","CNMI","CSCA","CSMP","CSDH","CPMS"), "SMS"),
    (("HTTP",), "HTTP"),
    (("FTP",),  "FTP"),
    (("SSL",),  "SSL"),
    (("CIP","CGDCONT","CGATT","CGACT","CSTT","CIICR","CIFSR","CGPADDR","CDNS","CIPMUX"), "GPRS"),
    (("CPIN","CLCK","CPWD","CSIM","CRSM","CIMI","CCID","CSMINS","CSPN","CUSD"), "SIM"),
    (("CREG","CGREG","CEREG","COPS","CSQ"), "Network"),
    (("CLVL","CMUT","CRSL","CHFA","CAC","CMIC"), "Audio"),
    (("CFUN","CSCLK","SLP","PWR"), "Power"),
    (("GPIO","SGPIO"), "GPIO"),
    (("CCLK","CTZU","CTZR"), "Time"),
    (("CMEE",), "Debug"),
]

def guess_category(cmd):
    c = cmd.upper().lstrip("+")
    for keys, cat in CATEGORY_RULES:
        for k in keys:
            if c.startswith(k):
                return cat
    return "General"

def parse_at_commands(text):
    found = {}
    for m in AT_CMD_RE.finditer(text):
        name = "+" + m.group(1)
        if name in found:
            continue
        start = max(0, m.start() - 60)
        end   = min(len(text), m.end() + 500)
        ctx = text[start:end].replace("\r", "").strip()
        found[name] = ctx
    return found

def parse_urcs(text):
    found = {}
    for m in URC_RE.finditer(text):
        token = m.group(1).strip()
        if token in ("OK", "ERROR"):  # skip generic
            continue
        if token in found:
            continue
        start = m.start()
        end   = min(len(text), m.end() + 200)
        found[token] = text[start:end].replace("\r", "").strip()
    return found

def parse_error_codes(text):
    cme, cms = {}, {}
    for m in CME_RE.finditer(text):
        code = int(m.group(1))
        if code not in cme:
            cme[code] = m.group(2).strip()
    for m in CMS_RE.finditer(text):
        code = int(m.group(1))
        if code not in cms:
            cms[code] = m.group(2).strip()
    return cme, cms

# ---------------------------------------------------------------------
# Hardware pin parsing
# ---------------------------------------------------------------------
PIN_HINTS = [
    "VBAT","GND","VDD_EXT","VDD","VRTC","UART_TXD","UART_RXD","UART_CTS","UART_RTS",
    "UART_DTR","UART_DCD","UART_RI","SIM_VDD","SIM_DATA","SIM_CLK","SIM_RST","SIM_DET",
    "MIC_P","MIC_N","SPK_P","SPK_N","PWRKEY","RESET","STATUS","NETLIGHT",
    "ADC1","ADC2","GPIO","PWM1","PWM2","ANT","RF_ANT","VCHG","VBUS","USB_DP","USB_DM",
    "TXD","RXD","CTS","RTS","DTR","DCD","RI","GND_1","GND_2","GND_3",
]

def parse_hw_pins(text):
    pins = {}
    for hint in PIN_HINTS:
        pat = re.compile(r'\b' + re.escape(hint) + r'\b([^\n]{0,180})', re.IGNORECASE)
        m = pat.search(text)
        if m:
            line = (hint + m.group(1)).strip()
            volts = VOLT_RE.findall(line)
            currs = CURR_RE.findall(line)
            pins[hint] = {
                "raw": line[:300],
                "volts": volts[:4],
                "currents": currs[:4],
            }
    return pins

# ---------------------------------------------------------------------
# Simple YAML serializer for list-of-dict records
# ---------------------------------------------------------------------
def yaml_scalar(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    s = str(v)
    if s == "" or any(ch in s for ch in (":", "#", "\n", "\"", "'", ",", "[", "]", "{", "}")) \
       or s.strip() != s:
        esc = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return '"' + esc + '"'
    return s

def dump_record(rec):
    lines = []
    first = True
    for k, v in rec.items():
        prefix = "- " if first else "  "
        first = False
        if isinstance(v, list):
            if not v:
                lines.append("%s%s: []" % (prefix, k))
            else:
                lines.append("%s%s:" % (prefix, k))
                for item in v:
                    if isinstance(item, dict):
                        lines.append("    - " + json.dumps(item, ensure_ascii=False))
                    else:
                        lines.append("    - " + yaml_scalar(item))
        elif isinstance(v, dict):
            lines.append("%s%s:" % (prefix, k))
            for kk, vv in v.items():
                if isinstance(vv, (dict, list)):
                    lines.append("    %s: %s" % (kk, json.dumps(vv, ensure_ascii=False)))
                else:
                    lines.append("    %s: %s" % (kk, yaml_scalar(vv)))
        else:
            lines.append("%s%s: %s" % (prefix, k, yaml_scalar(v)))
    return "\n".join(lines)

def write_yaml(path, records, header=""):
    out = io.StringIO()
    if header:
        for line in header.splitlines():
            out.write("# " + line + "\n")
    if not records:
        out.write("records: []\n")
    else:
        out.write("records:\n")
        for rec in records:
            out.write(dump_record(rec) + "\n")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out.getvalue())

# ---------------------------------------------------------------------
# Source descriptors
# ---------------------------------------------------------------------
AT_SRC = {
    "name": "SIM800 Series AT Command Manual",
    "version": "V1.01",
    "date": "unknown",
    "page": "",
    "section": "",
}
HW_SRC_202 = {
    "name": "SIM800H&SIM800L Hardware Design",
    "version": "V2.02",
    "date": "2015-07-27",
    "page": "",
    "section": "",
}
HW_SRC_100 = {
    "name": "SIM800L Hardware Design",
    "version": "V1.00",
    "date": "2013-08-20",
    "page": "",
    "section": "",
}

def base_record(prefix, rid, category, source, src_type="primary", conf=0.85):
    return {
        "id": rid,
        "category": category,
        "source": source,
        "source_type": src_type,
        "confidence": conf,
        "status": "partial",
        "conflicts": [],
        "notes": "",
        "tags": [],
        "applicable_models": ["SIM800L"],
        "created_at": NOW,
        "updated_at": NOW,
    }

# ---------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------
def main():
    # 1. Discover PDFs
    pdfs = []
    for pat in ("*.pdf", "*.PDF"):
        pdfs.extend(glob.glob(os.path.join(SRC, pat)))
    pdfs = sorted(set(pdfs))
    SUMMARY["pdfs_found"] = [os.path.basename(p) for p in pdfs]

    # 2. Extract text
    texts = {}
    for p in pdfs:
        name = os.path.basename(p)
        text, backend = extract_pdf_text(p)
        if text:
            base = os.path.splitext(name)[0]
            txt_path = os.path.join(EXT, base + ".txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)
            texts[name] = text
            SUMMARY["pdfs_extracted"].append(name)
            SUMMARY["extraction_backend"][name] = backend

    # 3. Identify AT Manual text
    at_manual_text = ""
    hw_202_text = ""
    hw_100_text = ""
    for name, t in texts.items():
        low = name.lower()
        if "at command" in low:
            at_manual_text = t
        elif "v2.02" in low or "2.02" in low:
            hw_202_text = t
        elif "v1.00" in low or "1.00" in low:
            hw_100_text = t
    # Fallback if naming is off
    if not at_manual_text:
        for name, t in texts.items():
            if "at" in name.lower() and "command" in name.lower():
                at_manual_text = t
                break
    hw_text = (hw_202_text or "") + "\n" + (hw_100_text or "")

    # 4. Parse from AT Manual
    if at_manual_text:
        cmds = parse_at_commands(at_manual_text)
        urcs = parse_urcs(at_manual_text)
        cme, cms = parse_error_codes(at_manual_text)

        # dat_01 — AT Command DB
        at_records = []
        for i, (cmd, ctx) in enumerate(sorted(cmds.items()), start=1):
            rid = "dat_01_%04d" % i
            rec = base_record("dat_01", rid, guess_category(cmd), AT_SRC, conf=0.9)
            rec.update({
                "command": cmd,
                "mode": "exec",
                "syntax": cmd,
                "parameters": [],
                "response_success": "OK",
                "response_error": "+CME ERROR: <err>",
                "examples": [],
                "related_urcs": [],
                "related_states": [],
                "related_commands": [],
                "firmware_min": "",
                "firmware_max": "",
                "notes": "Auto-extracted from AT Command Manual. Context: " + ctx[:200],
            })
            at_records.append(rec)
        write_yaml(
            os.path.join(DATA, "dat_01_at_command.yaml"),
            at_records,
            "Auto-extracted from SIM800 Series AT Command Manual V1.01\n"
            "Records: %d\n" % len(at_records)
        )
        SUMMARY["datasets_populated"]["dat_01"] = len(at_records)

        # dat_02 — URC DB
        urc_records = []
        for i, (u, ctx) in enumerate(sorted(urcs.items()), start=1):
            rid = "dat_02_%04d" % i
            rec = base_record("dat_02", rid, "URC", AT_SRC, conf=0.85)
            rec.update({
                "urc_string": u,
                "trigger_event": "",
                "related_command": "",
                "related_state": "",
                "format": u,
                "parameters": [],
                "examples": [u],
                "timing": "",
                "suppression_method": "",
                "notes": "Auto-extracted. Context: " + ctx[:160],
            })
            urc_records.append(rec)
        write_yaml(
            os.path.join(DATA, "dat_02_urc.yaml"),
            urc_records,
            "Auto-extracted URC candidates from AT Command Manual V1.01\n"
            "Records: %d\n" % len(urc_records)
        )
        SUMMARY["datasets_populated"]["dat_02"] = len(urc_records)

        # dat_03 — Error codes
        err_records = []
        i = 0
        for code in sorted(cme.keys()):
            i += 1
            rid = "dat_03_%04d" % i
            rec = base_record("dat_03", rid, "CME", AT_SRC, conf=0.85)
            rec.update({
                "error_type": "CME",
                "code": code,
                "meaning": cme[code][:120] or "Unknown",
                "description": cme[code][:200],
                "related_commands": [],
                "recovery_steps": [],
            })
            err_records.append(rec)
        for code in sorted(cms.keys()):
            i += 1
            rid = "dat_03_%04d" % i
            rec = base_record("dat_03", rid, "CMS", AT_SRC, conf=0.85)
            rec.update({
                "error_type": "CMS",
                "code": code,
                "meaning": cms[code][:120] or "Unknown",
                "description": cms[code][:200],
                "related_commands": [],
                "recovery_steps": [],
            })
            err_records.append(rec)
        write_yaml(
            os.path.join(DATA, "dat_03_error_code.yaml"),
            err_records,
            "Auto-extracted CME/CMS error codes from AT Command Manual V1.01\n"
            "Records: %d\n" % len(err_records)
        )
        SUMMARY["datasets_populated"]["dat_03"] = len(err_records)

        # dat_09 — SMS
        sms_cmds = {k: v for k, v in cmds.items()
                    if k.upper().lstrip("+").startswith(("CMG","CNMI","CPMS","CSCA","CSMP","CSDH","CSMS","CSCS"))}
        sms_records = []
        for i, (c, ctx) in enumerate(sorted(sms_cmds.items()), start=1):
            rid = "dat_09_%04d" % i
            rec = base_record("dat_09", rid, "SMS", AT_SRC, conf=0.9)
            rec.update({
                "mode": "text",
                "command": c,
                "syntax": c,
                "parameters": [],
                "response": "OK",
                "examples": [],
                "related_urcs": [],
                "encoding": "GSM7",
                "storage": "SM",
                "concat_sms": False,
                "delivery_report": False,
            })
            sms_records.append(rec)
        write_yaml(os.path.join(DATA, "dat_09_sms.yaml"), sms_records,
                   "Auto-extracted SMS commands. Records: %d" % len(sms_records))
        SUMMARY["datasets_populated"]["dat_09"] = len(sms_records)

        # dat_10 — GPRS / Data
        gprs_cmds = {k: v for k, v in cmds.items()
                     if k.upper().lstrip("+").startswith(("CGDCONT","CGATT","CGACT","CSTT","CIICR","CIFSR",
                                                          "CGPADDR","CDNSGIP","CIP","CREG","CGREG","CEREG","CSQ","COPS"))}
        gprs_records = []
        for i, (c, ctx) in enumerate(sorted(gprs_cmds.items()), start=1):
            rid = "dat_10_%04d" % i
            rec = base_record("dat_10", rid, "GPRS", AT_SRC, conf=0.9)
            rec.update({
                "command": c,
                "syntax": c,
                "parameters": [],
                "response": "OK",
                "examples": [],
                "related_urcs": [],
                "related_states": [],
                "related_commands": [],
            })
            gprs_records.append(rec)
        write_yaml(os.path.join(DATA, "dat_10_gprs_data.yaml"), gprs_records,
                   "Auto-extracted GPRS/Data commands. Records: %d" % len(gprs_records))
        SUMMARY["datasets_populated"]["dat_10"] = len(gprs_records)

        # dat_11 — HTTP/FTP/SSL
        hfs_cmds = {k: v for k, v in cmds.items()
                    if k.upper().lstrip("+").startswith(("HTTP","FTP","SSL"))}
        hfs_records = []
        for i, (c, ctx) in enumerate(sorted(hfs_cmds.items()), start=1):
            rid = "dat_11_%04d" % i
            rec = base_record("dat_11", rid, "HTTP/FTP/SSL", AT_SRC, conf=0.9)
            rec.update({
                "command": c,
                "syntax": c,
                "parameters": [],
                "response": "OK",
                "examples": [],
                "related_urcs": [],
                "related_commands": [],
            })
            hfs_records.append(rec)
        write_yaml(os.path.join(DATA, "dat_11_http_ftp_ssl.yaml"), hfs_records,
                   "Auto-extracted HTTP/FTP/SSL commands. Records: %d" % len(hfs_records))
        SUMMARY["datasets_populated"]["dat_11"] = len(hfs_records)

        # dat_12 — Audio
        audio_cmds = {k: v for k, v in cmds.items()
                      if k.upper().lstrip("+").startswith(("CLVL","CMUT","CRSL","CHFA","CAC","CMIC","CSDTMF","CRSL"))}
        audio_records = []
        for i, (c, ctx) in enumerate(sorted(audio_cmds.items()), start=1):
            rid = "dat_12_%04d" % i
            rec = base_record("dat_12", rid, "Audio", AT_SRC, conf=0.9)
            rec.update({
                "command": c,
                "syntax": c,
                "parameters": [],
                "response": "OK",
                "examples": [],
                "related_commands": [],
            })
            audio_records.append(rec)
        write_yaml(os.path.join(DATA, "dat_12_audio.yaml"), audio_records,
                   "Auto-extracted audio commands. Records: %d" % len(audio_records))
        SUMMARY["datasets_populated"]["dat_12"] = len(audio_records)

        # dat_13 — SIM management
        sim_cmds = {k: v for k, v in cmds.items()
                    if k.upper().lstrip("+").startswith(("CPIN","CLCK","CPWD","CSIM","CRSM","CIMI","CCID","CSMINS","CSPN","CUSD"))}
        sim_records = []
        for i, (c, ctx) in enumerate(sorted(sim_cmds.items()), start=1):
            rid = "dat_13_%04d" % i
            rec = base_record("dat_13", rid, "SIM", AT_SRC, conf=0.9)
            rec.update({
                "command": c,
                "syntax": c,
                "parameters": [],
                "response": "OK",
                "examples": [],
                "related_urcs": [],
                "hardware_pins": [],
            })
            sim_records.append(rec)
        write_yaml(os.path.join(DATA, "dat_13_sim_management.yaml"), sim_records,
                   "Auto-extracted SIM management commands. Records: %d" % len(sim_records))
        SUMMARY["datasets_populated"]["dat_13"] = len(sim_records)

    # 5. Hardware pins
    if hw_text:
        pins = parse_hw_pins(hw_text)
        pin_records = []
        cat_map = {
            "VBAT":"Power","GND":"Ground","GND_1":"Ground","GND_2":"Ground","GND_3":"Ground",
            "VDD_EXT":"Power","VDD":"Power","VRTC":"RTC","VCHG":"Charge","VBUS":"USB",
            "UART_TXD":"UART","UART_RXD":"UART","UART_CTS":"UART","UART_RTS":"UART",
            "UART_DTR":"UART","UART_DCD":"UART","UART_RI":"UART",
            "TXD":"UART","RXD":"UART","CTS":"UART","RTS":"UART","DTR":"UART","DCD":"UART","RI":"UART",
            "SIM_VDD":"SIM","SIM_DATA":"SIM","SIM_CLK":"SIM","SIM_RST":"SIM","SIM_DET":"SIM",
            "MIC_P":"Audio","MIC_N":"Audio","SPK_P":"Audio","SPK_N":"Audio",
            "PWRKEY":"Power","RESET":"Reset","STATUS":"Status","NETLIGHT":"Status",
            "ADC1":"ADC","ADC2":"ADC","GPIO":"GPIO","PWM1":"PWM","PWM2":"PWM",
            "ANT":"Antenna","RF_ANT":"Antenna","USB_DP":"USB","USB_DM":"USB",
        }
        i = 0
        for pin_name, info in sorted(pins.items()):
            i += 1
            rid = "dat_07_%04d" % i
            cat = cat_map.get(pin_name, "Mechanical")
            rec = base_record("dat_07", rid, cat,
                              HW_SRC_202 if hw_202_text else HW_SRC_100, conf=0.85)
            volts = info.get("volts") or []
            currs = info.get("currents") or []
            def fnum(v):
                try: return float(v)
                except Exception: return None
            rec.update({
                "name": pin_name,
                "pin_number": "",
                "direction": "",
                "voltage_min": fnum(volts[0]) if len(volts) > 0 else None,
                "voltage_typ": fnum(volts[1]) if len(volts) > 1 else (fnum(volts[0]) if len(volts) > 0 else None),
                "voltage_max": fnum(volts[2]) if len(volts) > 2 else (fnum(volts[0]) if len(volts) > 0 else None),
                "current_typ": fnum(currs[0]) if currs else None,
                "current_max": fnum(currs[1]) if len(currs) > 1 else (fnum(currs[0]) if currs else None),
                "function": info["raw"][:200],
                "alternate_function": "",
                "pull_up_down": "",
                "esd_rating": "",
                "impedance": "",
                "decoupling": "",
                "notes": "Auto-extracted from hardware design PDF",
            })
            pin_records.append(rec)
        if pin_records:
            write_yaml(os.path.join(DATA, "dat_07_hardware_reference.yaml"), pin_records,
                       "Auto-extracted hardware pins. Records: %d" % len(pin_records))
            SUMMARY["datasets_populated"]["dat_07"] = len(pin_records)

    # 6. Explicitly blocked datasets (no source)
    blocked = []
    for nn in ("08","14","16","17","18"):
        blocked.append("dat_%s" % nn)
    SUMMARY["datasets_blocked"] = blocked

    # 7. Output summary JSON for PowerShell
    print(json.dumps(SUMMARY, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()