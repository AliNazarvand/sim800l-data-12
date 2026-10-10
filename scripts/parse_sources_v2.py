#!/usr/bin/env python3
"""پارسر عمیق: AT command با syntax/parameters/examples + جداول سخت‌افزاری."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTRACTED = ROOT / "sources" / "extracted"
TABLES = EXTRACTED / "tables"

def read(name):
    p = EXTRACTED / name
    if not p.exists(): return ""
    try: return p.read_text(encoding="utf-8", errors="ignore")
    except Exception: return ""

def read_any(*names):
    for n in names:
        t = read(n)
        if t: return t
    return ""

# ---------- AT Command Detail Parser ----------

def extract_at_details(text, cmd):
    """برای یک command خاص، syntax/params/examples/response استخراج می‌کند."""
    details = {"syntax": "", "parameters": [], "examples": [], "response_success": "OK", "response_error": "", "mode": ""}
    # بخش‌یابی: جستجوی AT+CMD به عنوان شروع بخش
    pattern = r'AT' + re.escape(cmd) + r'\s*\n'
    m = re.search(pattern, text)
    if not m:
        # تلاش دوم: AT+CMD به عنوان heading
        pattern2 = r'AT' + re.escape(cmd) + r'\s'
        m = re.search(pattern2, text)
        if not m:
            return details
    start = m.start()
    section = text[start:start+4000]

    # Syntax
    syntax_m = re.search(r'(AT' + re.escape(cmd) + r'[^\n\r]{0,300})', section)
    if syntax_m:
        details["syntax"] = syntax_m.group(1).strip()[:300]

    # Mode (test/read/write/exec)
    low = section.lower()
    if "execution command" in low or "exec command" in low:
        details["mode"] = "exec"
    elif "read command" in low:
        details["mode"] = "read"
    elif "write command" in low:
        details["mode"] = "write"
    elif "test command" in low:
        details["mode"] = "test"

    # Parameters: <name>
    params = []
    seen = set()
    for pm in re.finditer(r'<([a-zA-Z_][a-zA-Z0-9_]*)>\s*[-:]?\s*([^\n<]{0,200})', section):
        name = pm.group(1)
        if name in seen: continue
        seen.add(name)
        desc = pm.group(2).strip()[:150]
        params.append({"name": name, "type": "string", "description": desc})
        if len(params) >= 20: break
    details["parameters"] = params

    # Examples
    examples = []
    ex_block = re.search(r'(?:Example|e\.g\.|for example)[^\n]*\n((?:[^\n]*\n){1,15})', section, re.IGNORECASE)
    if ex_block:
        for line in ex_block.group(1).split("\n"):
            line = line.strip()
            if line.startswith("AT"):
                examples.append(line[:300])
    if not examples:
        for em in re.finditer(r'^(AT' + re.escape(cmd) + r'[^\n\r]{0,200})$', section, re.MULTILINE):
            examples.append(em.group(1).strip()[:300])
            if len(examples) >= 5: break
    details["examples"] = examples[:5]

    # Response
    resp_m = re.search(r'(?:Response|Response\s+Success)[^\n]*\n\s*([^\n]+)', section, re.IGNORECASE)
    if resp_m:
        details["response_success"] = resp_m.group(1).strip()[:200]

    err_m = re.search(r'(?:ERROR|CMS ERROR|CME ERROR)[^\n]{0,150}', section)
    if err_m:
        details["response_error"] = err_m.group(0).strip()[:200]

    return details

def find_all_at_commands(text):
    cmds = {}
    pages = re.split(r'=== PAGE (\d+) ===', text)
    current_page = "?"
    i = 0
    while i < len(pages):
        chunk = pages[i]
        if re.fullmatch(r'\d+', chunk.strip() or ""):
            current_page = chunk.strip()
            i += 1
            continue
        page = chunk
        for m in re.finditer(r'AT\+([A-Z][A-Z0-9_]*)', page):
            cmd = "+" + m.group(1)
            if cmd not in cmds:
                cmds[cmd] = {"page": current_page}
        i += 1
    return cmds

def search_ssl_keywords(text):
    """جستجوی کلمات کلیدی SSL/TLS/Certificate در متن."""
    found = {}
    for kw in ["SSL", "TLS", "SSLCFG", "SSLCONF", "SSLSETCERT", "SSLSETKEY",
               "SSLSETCA", "SSLOPEN", "SSLSEND", "SSLRECV", "SSLCLOSE",
               "Certificate", "Keystore", "Key Store", "HTTPS"]:
        cnt = len(re.findall(re.escape(kw), text, re.IGNORECASE))
        if cnt:
            found[kw] = cnt
    return found

# ---------- Hardware Parsers ----------

def parse_tables_from_csv():
    """خواندن تمام csvهای جداول استخراج‌شده."""
    rows = []
    if not TABLES.exists():
        return rows
    for csv in sorted(TABLES.glob("*.csv")):
        try:
            with open(csv, encoding="utf-8") as f:
                content = f.read()
            rows.append({"file": csv.name, "content": content})
        except Exception:
            pass
    return rows

def parse_hw_pins(text):
    """پین‌ها از جدول Pin Description."""
    pins = []
    # نام‌های استاندارد
    known = ["VBAT","GND","VDD_EXT","PWRKEY","RESET","STATUS","NETLIGHT",
             "TXD","RXD","RTS","CTS","DTR","DCD","RI",
             "SIM_VDD","SIM_DATA","SIM_CLK","SIM_RST","SIM_DET",
             "MIC_P","MIC_N","SPK_P","SPK_N","RF_ANT","ADC",
             "PWM1","PWM2","USB_DP","USB_DM","VRTC","CHARGE","KPLUS"]
    for name in known:
        if re.search(r'\b' + re.escape(name) + r'\b', text):
            pins.append(name)
    return pins

def parse_timing(text):
    """زمان‌بندی از متن."""
    timings = []
    for m in re.finditer(r'([A-Za-z][A-Za-z0-9 _\-/]{3,80})\s+([0-9]+(?:\.[0-9]+)?)\s*(ms|us|s|µs)\b', text):
        timings.append({
            "parameter": m.group(1).strip(),
            "value": float(m.group(2)),
            "unit": m.group(3),
        })
    return timings

def parse_power_mgmt(text):
    """Power management keywords."""
    keys = ["Sleep", "Sleep Mode", "CFUN", "Slow Clock", "DTR", "RTC",
            "Deep Sleep", "Minimum Functionality", "Power Saving",
            "AT+CSCLK", "AT+CFUN", "AT+CSDT", "AT+CBATCHK"]
    results = []
    for k in keys:
        cnt = len(re.findall(re.escape(k), text, re.IGNORECASE))
        if cnt:
            results.append({"keyword": k, "count": cnt})
    return results

def main():
    at_text = read_any("at_v1_01.txt", "SIM800 Series_AT Command Manual_V1.01.txt")
    hw100 = read_any("v1.00.txt", "SIM800L_Hardware_Design_V1.00.txt")
    hw202 = read_any("v2.02.txt", "SIM800H&SIM800L_Hardware_Design_V2.02.txt")

    at_cmds = find_all_at_commands(at_text) if at_text else {}
    print(f"AT commands found: {len(at_cmds)}")

    # استخراج جزئیات برای هر command (این ممکن است طولانی باشد)
    details = {}
    for cmd in list(at_cmds.keys()):
        details[cmd] = extract_at_details(at_text, cmd)

    ssl_kw = search_ssl_keywords(at_text)
    print(f"SSL keywords: {ssl_kw}")

    hw_pins = parse_hw_pins(hw202 or hw100)
    timings = parse_timing((hw202 or "") + "\n" + (hw100 or ""))
    power = parse_power_mgmt((hw202 or "") + "\n" + (hw100 or "") + "\n" + at_text)

    idx_path = EXTRACTED / "_index.json"
    idx_path.write_text(json.dumps({
        "at_commands": at_cmds,
        "at_details": details,
        "ssl_keywords": ssl_kw,
        "hw_pins": hw_pins,
        "timings": timings,
        "power_mgmt": power,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"saved: {idx_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())