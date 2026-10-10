#!/usr/bin/env python3
"""
Comprehensive fix v3.1 — based on critic's v3 with one correction:
  - `code` field kept as required integer (NOT nullable)
  - All other fixes identical to v3
"""
import os, re, sys, json, glob
from datetime import datetime, timezone
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
EXT  = os.path.join(ROOT, "sources", "extracted")
SCH  = os.path.join(ROOT, "schemas")
REP  = os.path.join(ROOT, "reports")
NOW  = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

AT_SRC = {"name":"SIM800 Series AT Command Manual","version":"V1.01",
          "date":"2013-07-23","page":"","section":""}
HW202  = {"name":"SIM800H&SIM800L Hardware Design","version":"V2.02",
          "date":"2015-07-27","page":"","section":""}

def base(rid, cat, source, conf=0.9, status="partial"):
    return {"id":rid,"category":cat,"source":source,"source_type":"primary",
            "confidence":conf,"status":status,"conflicts":[],"notes":"",
            "tags":[],"applicable_models":["SIM800L"],
            "created_at":NOW,"updated_at":NOW}

SUMMARY = {"dat_03":{}, "yaml_fixed":[], "schemas_fixed":[],
           "dat_07_cleaned":0, "blocked_marked":[], "errors":[]}

# =====================================================================
# 1. dat_03 — strict section header (skip TOC)
# =====================================================================
def fix_dat_03():
    at_path = None
    for p in glob.glob(os.path.join(EXT,"*.txt")):
        n = os.path.basename(p).lower()
        if "at command" in n or "at_v1" in n or "series_at" in n:
            at_path = p; break
    if not at_path:
        SUMMARY["errors"].append("dat_03: AT manual text not found")
        return
    with open(at_path,"r",encoding="utf-8",errors="ignore") as f:
        text = f.read()

    cme_header = re.compile(r'(?m)^19\.1\s+Summary of CME ERROR Codes\s*$')
    cms_header = re.compile(r'(?m)^19\.2\s+Summary of CMS ERROR Codes\s*$')
    urs_header = re.compile(r'(?m)^19\.3\s+Summary of Unsolicited Result Codes\s*$')

    cme_matches = list(cme_header.finditer(text))
    cms_matches = list(cms_header.finditer(text))
    urs_matches = list(urs_header.finditer(text))

    cme_codes, cms_codes = {}, {}

    if cme_matches and cms_matches:
        cme_block = text[cme_matches[-1].end():cms_matches[-1].start()]
        for line in cme_block.splitlines():
            m = re.match(r'^\s*(\d{1,3})\s+([a-zA-Z][^\n]{2,120}?)\s*$', line)
            if m:
                code = int(m.group(1))
                meaning = m.group(2).strip()
                if meaning.lower() in ("code of <err> meaning","code meaning","meaning","description"):
                    continue
                if code not in cme_codes:
                    cme_codes[code] = meaning
    if cms_matches and urs_matches:
        cms_block = text[cms_matches[-1].end():urs_matches[-1].start()]
        for line in cms_block.splitlines():
            m = re.match(r'^\s*(\d{1,3})\s+([a-zA-Z][^\n]{2,120}?)\s*$', line)
            if m:
                code = int(m.group(1))
                meaning = m.group(2).strip()
                if meaning.lower() in ("code of <err> meaning","code meaning","meaning","description"):
                    continue
                if code not in cms_codes:
                    cms_codes[code] = meaning

    recs = []
    i = 0
    for code in sorted(cme_codes):
        i += 1
        r = base("dat_03_%04d"%i, "CME", AT_SRC)
        r.update({"error_type":"CME","code":int(code),
                  "meaning":cme_codes[code][:200],
                  "description":cme_codes[code][:400],
                  "related_commands":[],"recovery_steps":[]})
        recs.append(r)
    for code in sorted(cms_codes):
        i += 1
        r = base("dat_03_%04d"%i, "CMS", AT_SRC)
        r.update({"error_type":"CMS","code":int(code),
                  "meaning":cms_codes[code][:200],
                  "description":cms_codes[code][:400],
                  "related_commands":[],"recovery_steps":[]})
        recs.append(r)

    if not recs:
        SUMMARY["errors"].append("dat_03: still 0 codes after strict extraction")
        return
    path = os.path.join(DATA,"dat_03_error_code.yaml")
    out = ["# CME/CMS error codes — strict extraction (v3.1)",
           "# CME=%d, CMS=%d, total=%d"%(len(cme_codes),len(cms_codes),len(recs)),
           "records:"]
    for r in recs:
        out.append(yaml.safe_dump([r], allow_unicode=True, sort_keys=False,
                                  default_flow_style=False).rstrip())
    with open(path,"w",encoding="utf-8") as f:
        f.write("\n".join(out)+"\n")
    SUMMARY["dat_03"] = {"cme":len(cme_codes),"cms":len(cms_codes),"total":len(recs)}

# =====================================================================
# 2. YAML quoting
# =====================================================================
def quote_yaml_text(text):
    text = re.sub(r'^(\s*date:\s*)(\d{4}-\d{2}-\d{2})\s*$',
                  r'\1"\2"', text, flags=re.M)
    text = re.sub(r'^(\s*wake_source:\s*)-\s*$', r'\1"-"', text, flags=re.M)
    for field in ("failure_action","condition","parameter","value","name"):
        text = re.sub(r'^(\s*'+field+r':\s*)-\s*$', r'\1"-"', text, flags=re.M)
    text = re.sub(r'^(\s*pin_number:\s*)(\d{1,3})\s*$', r'\1"\2"', text, flags=re.M)
    text = re.sub(r'^(\s*dependency_step:\s*)(\d+)\s*$', r'\1"\2"', text, flags=re.M)
    return text

def fix_yaml_quoting():
    for path in sorted(glob.glob(os.path.join(DATA,"*.yaml"))):
        try:
            with open(path,"r",encoding="utf-8") as f:
                text = f.read()
            fixed = quote_yaml_text(text)
            if fixed != text:
                with open(path,"w",encoding="utf-8") as f:
                    f.write(fixed)
                SUMMARY["yaml_fixed"].append(os.path.basename(path))
            with open(path,"r",encoding="utf-8") as f:
                yaml.safe_load(f)
        except Exception as e:
            SUMMARY["errors"].append("YAML fix %s: %s"%(os.path.basename(path), str(e)[:120]))

# =====================================================================
# 3. Schemas: allow null in OPTIONAL numerics ONLY (not `code`)
# =====================================================================
def fix_schemas():
    # `code` intentionally EXCLUDED — it must always be an integer
    numeric_fields = ["voltage_min","voltage_typ","voltage_max",
                      "current_typ","current_max","min","typ","max",
                      "value_min","value_typ","value_max"]
    for path in sorted(glob.glob(os.path.join(SCH,"*.yaml"))):
        try:
            with open(path,"r",encoding="utf-8") as f:
                text = f.read()
            original = text
            for fn in numeric_fields:
                text = re.sub(
                    r'(\b'+fn+r':\s*)\{type:\s*(number|integer)\}',
                    r'\1{type: ["\2", "null"]}', text)
                text = re.sub(
                    r'(\b'+fn+r':\s*\n\s+type:\s*)(number|integer)\s*$',
                    r'\1["\2", "null"]', text, flags=re.M)
            if text != original:
                with open(path,"w",encoding="utf-8") as f:
                    f.write(text)
                SUMMARY["schemas_fixed"].append(os.path.basename(path))
        except Exception as e:
            SUMMARY["errors"].append("Schema fix %s: %s"%(os.path.basename(path), str(e)[:120]))

# =====================================================================
# 4. dat_07 cleanup
# =====================================================================
def clean_dat_07():
    path = os.path.join(DATA,"dat_07_hardware_reference.yaml")
    if not os.path.exists(path): return
    with open(path,"r",encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    recs = doc.get("records") or []
    cleaned = 0
    valid_dirs = {"I","O","I/O","IO"}
    for r in recs:
        if not isinstance(r, dict): continue
        fn = r.get("function") or ""
        dr = r.get("direction") or ""
        if dr in valid_dirs and re.match(r'^[IO](\s+|$)', fn):
            r["function"] = re.sub(r'^[IO]\s+', '', fn).strip()[:200]
            cleaned += 1
        if dr and dr not in valid_dirs and dr not in ("","unknown"):
            r["direction"] = ""
            cleaned += 1
        pn = r.get("pin_number") or ""
        if pn and not re.match(r'^[\d,\s]+$', str(pn)):
            r["pin_number"] = ""
            cleaned += 1
    with open(path,"w",encoding="utf-8") as f:
        f.write(yaml.safe_dump({"records":recs}, allow_unicode=True,
                               sort_keys=False, default_flow_style=False))
    SUMMARY["dat_07_cleaned"] = cleaned

# =====================================================================
# 5. Blocked markers
# =====================================================================
BLOCKED = {
    "dat_08_firmware_compatibility.yaml":
        ("dat_08","Firmware Compatibility","SIM800 Series Firmware Release Notes"),
    "dat_16_board_evb.yaml":
        ("dat_16","Board/EVB","SIM800L EVB Schematic / BOM"),
    "dat_17_certificate_key_store.yaml":
        ("dat_17","Certificate/Key Store","SIM800 Series SSL AT Command Manual"),
    "dat_18_certification.yaml":
        ("dat_18","Certification","CE/FCC/GCF/PTCRB official certificates"),
}

def mark_blocked():
    for fname, (prefix, name, needed_source) in BLOCKED.items():
        path = os.path.join(DATA, fname)
        with open(path,"r",encoding="utf-8") as f:
            existing = yaml.safe_load(f) or {}
        if existing.get("records"): continue
        header = ("# %s\n"
                  "# STATUS: BLOCKED — primary source unavailable\n"
                  "# Missing source: %s\n"
                  "# See reports/TODO.md and reports/COVERAGE_MATRIX.md\n"%(fname, needed_source))
        with open(path,"w",encoding="utf-8") as f:
            f.write(header + "records: []\n")
        SUMMARY["blocked_marked"].append(prefix)

def main():
    fix_dat_03()
    fix_schemas()
    fix_yaml_quoting()
    clean_dat_07()
    mark_blocked()
    print(json.dumps(SUMMARY, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()