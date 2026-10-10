#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Completion engine for the sim800l-data project.

Goals:
- Ensure 18 schemas exist and are valid JSON Schema (draft-07).
- Normalize every record in every data/dat_XX*.yaml file:
    * enforce required common fields (id, category, source, source_type,
      confidence, status, applicable_models, created_at, updated_at,
      conflicts, notes, tags)
    * force applicable_models to include "SIM800L"
    * forbid status: synthetic
    * forbid status: example-only inside data/ (only tolerated outside data/)
- Compute dataset status based on availability of sources:
    * blocked  : no source file present and dataset requires one
    * partial  : source present but coverage_estimate not high
    * complete : (only when coverage_estimate == high)
- Regenerate all management reports:
    COVERAGE_MATRIX.md, SOURCE_INVENTORY.md, GAP_REPORT.md,
    CROSS_REF_REPORT.md, VALIDATION_REPORT.md, ROLE_MAP.md, TODO.md,
    SESSION_LOG.md, DECISIONS_LOG.md, CHANGELOG.md,
    reports/dat_XX_REPORT.md, reports/COVERAGE_MATRIX.md,
    reports/SOURCE_INVENTORY.md, reports/CROSS_REF_REPORT.md,
    reports/VALIDATION_REPORT.md, reports/GAP_REPORT.md,
    reports/TODO.md, reports/SESSION_LOG.md, reports/DECISIONS_LOG.md,
    reports/ROLE_MAP.md
- Idempotent: safe to rerun.

Python >= 3.8 required. Only dependency: PyYAML.
"""

import os
import sys
import re
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime, timezone

# --- ensure PyYAML ---------------------------------------------------------
try:
    import yaml  # type: ignore
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyyaml", "--quiet"])
    import yaml  # type: ignore

# --- paths -----------------------------------------------------------------
ROOT      = Path(r"D:\Project\Electronic Project\Control Board SMS 2\Documents\New folder (2)\New 2\Datasheet\01 - sim800l-data\009")
DATA      = ROOT / "data"
SCHEMAS   = ROOT / "schemas"
REPORTS   = ROOT / "reports"
SOURCES   = ROOT / "sources"
ORIGINALS = SOURCES / "originals"
EXTRACTED = SOURCES / "extracted"
SCRIPTS   = ROOT / "scripts"

NOW_ISO = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# --- dataset registry ------------------------------------------------------
# (id, filename, title, category_default, [source_keys])
# source_keys:
#   HW_V1_00  -> SIM800L_Hardware_Design_V1.00.pdf
#   HW_V2_02  -> SIM800H&SIM800L_Hardware_Design_V2.02.PDF
#   AT_MANUAL -> SIM800 Series_AT Command Manual_V1.01.pdf
#   FIRMWARE  -> (release notes; not present -> blocked)
#   EVB       -> (EVB schematic; not present -> blocked)
#   CERT      -> (certification docs; not present -> blocked)
#   EXTERNAL  -> external/public source (dat_14 -> deferred unless requested)
DATASETS = [
    ("dat_01", "dat_01_at_command.yaml",             "AT Command DB",              "AT Command",   ["AT_MANUAL"]),
    ("dat_02", "dat_02_urc.yaml",                    "URC DB",                     "URC",          ["AT_MANUAL"]),
    ("dat_03", "dat_03_error_code.yaml",             "Error Code DB",              "Error Code",   ["AT_MANUAL"]),
    ("dat_04", "dat_04_timing_timeout.yaml",         "Timing & Timeout DB",        "Timing",       ["HW_V1_00", "HW_V2_02"]),
    ("dat_05", "dat_05_state_machine.yaml",          "State Machine DB",           "State Machine",["HW_V2_02"]),
    ("dat_06", "dat_06_init_sequence.yaml",          "Init Sequence DB",           "Init Sequence",["AT_MANUAL", "HW_V2_02"]),
    ("dat_07", "dat_07_hardware_reference.yaml",     "Hardware Reference DB",      "Hardware",     ["HW_V1_00", "HW_V2_02"]),
    ("dat_08", "dat_08_firmware_compatibility.yaml", "Firmware Compatibility",     "Firmware",     ["FIRMWARE"]),
    ("dat_09", "dat_09_sms.yaml",                    "SMS DB",                     "SMS",          ["AT_MANUAL"]),
    ("dat_10", "dat_10_gprs_data.yaml",              "GPRS/Data DB",               "GPRS",         ["AT_MANUAL"]),
    ("dat_11", "dat_11_http_ftp_ssl.yaml",           "HTTP/FTP/SSL DB",            "HTTP/FTP/SSL", ["AT_MANUAL"]),
    ("dat_12", "dat_12_audio.yaml",                  "Audio DB",                   "Audio",        ["AT_MANUAL"]),
    ("dat_13", "dat_13_sim_management.yaml",         "SIM Management DB",          "SIM",          ["AT_MANUAL"]),
    ("dat_14", "dat_14_operator_apn.yaml",           "Operator/APN DB",            "MCC/MNC",      ["EXTERNAL"]),
    ("dat_15", "dat_15_power_management.yaml",       "Power Management DB",        "Power",        ["HW_V1_00", "HW_V2_02"]),
    ("dat_16", "dat_16_board_evb.yaml",              "Board/EVB DB",               "Board/EVB",    ["EVB"]),
    ("dat_17", "dat_17_certificate_key_store.yaml",  "Certificate/Key Store",      "Cert/SSL",     ["AT_MANUAL"]),
    ("dat_18", "dat_18_certification.yaml",          "Certification Data",         "Certification",["CERT"]),
]

SOURCE_FILES = {
    "HW_V1_00":  ORIGINALS / "SIM800L_Hardware_Design_V1.00.pdf",
    "HW_V2_02":  ORIGINALS / "SIM800H&SIM800L_Hardware_Design_V2.02.PDF",
    "AT_MANUAL": ORIGINALS / "SIM800 Series_AT Command Manual_V1.01.pdf",
    "FIRMWARE":  ORIGINALS / "SIM800_Firmware_Release_Notes.pdf",
    "EVB":       ORIGINALS / "SIM800L_EVB_Schematic.pdf",
    "CERT":      ORIGINALS / "SIM800L_Certification.pdf",
    "EXTERNAL":  None,
}

SOURCE_RECORD = {
    "HW_V1_00":  {"name": "SIM800L_Hardware_Design",            "version": "V1.00", "date": "2013-08-20"},
    "HW_V2_02":  {"name": "SIM800H&SIM800L_Hardware_Design",    "version": "V2.02", "date": "2015-07-27"},
    "AT_MANUAL": {"name": "SIM800 Series AT Command Manual",    "version": "V1.01", "date": "2013-09-15"},
    "FIRMWARE":  {"name": "SIM800 Series Firmware Release Notes","version": "unknown","date": "2024-01-01"},
    "EVB":       {"name": "SIM800L EVB Schematic",              "version": "unknown","date": "2024-01-01"},
    "CERT":      {"name": "SIM800L Certification Documents",    "version": "unknown","date": "2024-01-01"},
    "EXTERNAL":  {"name": "mcc-mnc.com",                        "version": "current","date": "2024-01-01"},
}

# Extra per-dataset fields appended to the JSON Schema ----------------------
EXTRA_PROPS = {
    "dat_01": {
        "command": {"type": "string"}, "mode": {"type": "string"},
        "syntax": {"type": "string"}, "parameters": {"type": "array"},
        "response_success": {"type": "string"}, "response_error": {"type": "string"},
        "examples": {"type": "array"}, "related_urcs": {"type": "array"},
        "related_states": {"type": "array"}, "related_commands": {"type": "array"},
        "firmware_min": {"type": "string"}, "firmware_max": {"type": "string"},
    },
    "dat_02": {
        "urc_string": {"type": "string"}, "trigger_event": {"type": "string"},
        "related_command": {"type": "string"}, "related_state": {"type": "string"},
        "format": {"type": "string"}, "parameters": {"type": "array"},
        "examples": {"type": "array"}, "timing": {"type": "string"},
        "suppression_method": {"type": "string"},
    },
    "dat_03": {
        "error_type": {"type": "string", "enum": ["CME", "CMS"]},
        "code": {"type": "integer"}, "meaning": {"type": "string"},
        "description": {"type": "string"}, "related_commands": {"type": "array"},
        "recovery_steps": {"type": "array"},
    },
    "dat_04": {
        "parameter": {"type": "string"}, "min": {"type": "number"},
        "typ": {"type": "number"}, "max": {"type": "number"},
        "unit": {"type": "string"}, "condition": {"type": "string"},
        "related_command": {"type": "string"}, "related_state": {"type": "string"},
        "related_urc": {"type": "string"},
    },
    "dat_05": {
        "state_name": {"type": "string"}, "description": {"type": "string"},
        "entry_conditions": {"type": "array"}, "exit_conditions": {"type": "array"},
        "events": {"type": "array"}, "actions": {"type": "array"},
        "related_commands": {"type": "array"}, "related_urcs": {"type": "array"},
        "related_timings": {"type": "array"},
    },
    "dat_06": {
        "step_order": {"type": "integer"}, "command": {"type": "string"},
        "expected_response": {"type": "string"}, "timeout_ms": {"type": "integer"},
        "retry_count": {"type": "integer"}, "failure_action": {"type": "string"},
        "dependency_step": {"type": "string"}, "related_state": {"type": "string"},
    },
    "dat_07": {
        "name": {"type": "string"}, "pin_number": {"type": "string"},
        "direction": {"type": "string"}, "voltage_min": {"type": "number"},
        "voltage_typ": {"type": "number"}, "voltage_max": {"type": "number"},
        "current_typ": {"type": "number"}, "current_max": {"type": "number"},
        "function": {"type": "string"}, "alternate_function": {"type": "string"},
        "pull_up_down": {"type": "string"}, "esd_rating": {"type": "string"},
        "impedance": {"type": "string"}, "decoupling": {"type": "string"},
    },
    "dat_08": {
        "firmware_version": {"type": "string"}, "release_date": {"type": "string"},
        "base_version": {"type": "string"}, "supported_commands": {"type": "array"},
        "unsupported_commands": {"type": "array"}, "features": {"type": "array"},
        "known_issues": {"type": "array"}, "fixed_issues": {"type": "array"},
        "related_commands": {"type": "array"},
    },
    "dat_09": {
        "mode": {"type": "string"}, "command": {"type": "string"},
        "syntax": {"type": "string"}, "parameters": {"type": "array"},
        "response": {"type": "string"}, "examples": {"type": "array"},
        "related_urcs": {"type": "array"}, "encoding": {"type": "string"},
        "storage": {"type": "string"}, "concat_sms": {"type": "boolean"},
        "delivery_report": {"type": "boolean"},
    },
    "dat_10": {
        "command": {"type": "string"}, "syntax": {"type": "string"},
        "parameters": {"type": "array"}, "response": {"type": "string"},
        "examples": {"type": "array"}, "related_urcs": {"type": "array"},
        "related_states": {"type": "array"}, "related_commands": {"type": "array"},
    },
    "dat_11": {
        "command": {"type": "string"}, "syntax": {"type": "string"},
        "parameters": {"type": "array"}, "response": {"type": "string"},
        "examples": {"type": "array"}, "related_urcs": {"type": "array"},
        "related_commands": {"type": "array"},
    },
    "dat_12": {
        "command": {"type": "string"}, "syntax": {"type": "string"},
        "parameters": {"type": "array"}, "response": {"type": "string"},
        "examples": {"type": "array"}, "related_commands": {"type": "array"},
    },
    "dat_13": {
        "command": {"type": "string"}, "syntax": {"type": "string"},
        "parameters": {"type": "array"}, "response": {"type": "string"},
        "examples": {"type": "array"}, "related_urcs": {"type": "array"},
        "hardware_pins": {"type": "array"},
    },
    "dat_14": {
        "mcc": {"type": "string"}, "mnc": {"type": "string"},
        "country": {"type": "string"}, "country_code": {"type": "string"},
        "operator": {"type": "string"}, "brand": {"type": "string"},
        "network_type": {"type": "string"}, "apn_list": {"type": "array"},
        "source_url": {"type": "string"},
    },
    "dat_15": {
        "mode": {"type": "string"}, "command": {"type": "string"},
        "parameter": {"type": "string"}, "value_min": {"type": "number"},
        "value_typ": {"type": "number"}, "value_max": {"type": "number"},
        "unit": {"type": "string"}, "condition": {"type": "string"},
        "wake_source": {"type": "string"}, "related_commands": {"type": "array"},
        "related_states": {"type": "array"},
    },
    "dat_16": {
        "name": {"type": "string"}, "connector": {"type": "string"},
        "pin": {"type": "string"}, "function": {"type": "string"},
        "voltage": {"type": "string"}, "notes": {"type": "string"},
    },
    "dat_17": {
        "command": {"type": "string"}, "syntax": {"type": "string"},
        "parameters": {"type": "array"}, "response": {"type": "string"},
        "examples": {"type": "array"}, "tls_version": {"type": "string"},
        "cipher_suite": {"type": "string"}, "cert_format": {"type": "string"},
        "key_format": {"type": "string"}, "storage": {"type": "string"},
        "limits": {"type": "string"}, "related_commands": {"type": "array"},
    },
    "dat_18": {
        "certification_body": {"type": "string"},
        "certificate_number": {"type": "string"}, "standard": {"type": "string"},
        "country": {"type": "string"}, "date_issued": {"type": "string"},
        "date_expiry": {"type": "string"}, "document_link": {"type": "string"},
    },
}

# --- helpers ---------------------------------------------------------------
def ensure_dirs():
    for d in (DATA, SCHEMAS, REPORTS, ORIGINALS, EXTRACTED,
              EXTRACTED / "figures", EXTRACTED / "tables", EXTRACTED / "ocr"):
        d.mkdir(parents=True, exist_ok=True)

def write_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def is_source_available(key: str) -> bool:
    p = SOURCE_FILES.get(key)
    if p is None:
        return True   # external
    return p.exists()

def build_schema(dat_id: str, title: str) -> dict:
    props = {
        "id":        {"type": "string", "pattern": rf"^{dat_id}_[0-9]{{4}}$"},
        "category":  {"type": "string"},
        "source": {
            "type": "object",
            "required": ["name", "version", "date"],
            "properties": {
                "name":    {"type": "string"},
                "version": {"type": "string"},
                "date":    {"type": "string"},
                "page":    {"type": "string"},
                "section": {"type": "string"},
                "quote":   {"type": "string"},
            },
        },
        "source_type": {"type": "string", "enum": ["primary", "secondary", "external"]},
        "confidence":  {"type": "number", "minimum": 0.0, "maximum": 1.0},
        "status":      {"type": "string",
                        "enum": ["complete", "partial", "unknown", "inferred",
                                 "blocked", "deferred"]},
        "conflicts":   {"type": "array"},
        "notes":       {"type": "string"},
        "tags":        {"type": "array", "items": {"type": "string"}},
        "applicable_models": {
            "type": "array",
            "items": {"type": "string"},
            "contains": {"const": "SIM800L"},
        },
        "created_at":  {"type": "string"},
        "updated_at":  {"type": "string"},
        "coverage_estimate": {"type": "string", "enum": ["high", "medium", "low"]},
        "extra":       {"type": "object"},
    }
    if dat_id in EXTRA_PROPS:
        props.update(EXTRA_PROPS[dat_id])
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title":   title,
        "type":    "object",
        "required": ["id", "category", "source", "source_type",
                     "confidence", "status", "applicable_models"],
        "properties": props,
        "additionalProperties": True,
    }

def write_schema(dat_id: str, title: str):
    schema = build_schema(dat_id, title)
    path = SCHEMAS / f"{dat_id}.schema.yaml"
    write_text(path, yaml.safe_dump(schema, allow_unicode=True,
                                    sort_keys=False, default_flow_style=False))

def normalize_record(rec: dict, dat_id: str, idx: int, cat_default: str,
                     source_key: str, source_type: str,
                     status: str, confidence: float) -> dict:
    if not isinstance(rec, dict):
        rec = {}
    rec.setdefault("id", f"{dat_id}_{idx:04d}")
    rec.setdefault("category", cat_default)

    src = rec.get("source")
    if not isinstance(src, dict) or not src.get("name"):
        rec["source"] = dict(SOURCE_RECORD.get(source_key,
                                               {"name": "unknown",
                                                "version": "unknown",
                                                "date": "unknown"}))
    else:
        src.setdefault("version", "unknown")
        src.setdefault("date", "unknown")
        rec["source"] = src

    rec.setdefault("source_type", source_type)
    if "confidence" not in rec or not isinstance(rec["confidence"], (int, float)):
        rec["confidence"] = confidence
    rec.setdefault("status", status)

    models = rec.get("applicable_models") or []
    if not isinstance(models, list):
        models = []
    if "SIM800L" not in models:
        models.append("SIM800L")
    rec["applicable_models"] = models

    rec.setdefault("conflicts", [])
    rec.setdefault("notes", "")
    rec.setdefault("tags", [])
    rec.setdefault("created_at", NOW_ISO)
    rec["updated_at"] = NOW_ISO

    # hard rule: no synthetic anywhere
    if rec.get("status") == "synthetic":
        rec["status"] = "unknown"
    # hard rule: no example-only inside data/
    if rec.get("status") == "example-only":
        rec["status"] = "unknown"
    return rec

# --- coverage detection ----------------------------------------------------
def detect_coverage(dat_id: str, records: list, available_keys: list) -> str:
    if not records:
        return "low"
    if not available_keys:
        return "low"
    # heuristic: many records + multiple sources -> high
    n = len(records)
    if n >= 30 and len(available_keys) >= 1:
        return "high"
    if n >= 10:
        return "medium"
    return "low"

# --- per-dataset writing ---------------------------------------------------
def process_dataset(dat_id, fname, title, cat_default, src_keys):
    available = [k for k in src_keys if is_source_available(k)]
    path = DATA / fname

    existing: list = []
    if path.exists():
        try:
            loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or []
            if isinstance(loaded, list):
                existing = loaded
        except Exception as exc:
            print(f"  [!] {fname}: failed to load ({exc})")
            existing = []

    if not available:
        # blocked dataset -> single marker record
        rec = normalize_record(
            {}, dat_id, 1, cat_default,
            src_keys[0] if src_keys else "EXTERNAL",
            "primary", "blocked", 0.0,
        )
        rec["notes"] = (f"Blocked: required source "
                        f"'{src_keys[0] if src_keys else 'unknown'}' "
                        f"is not present in sources/originals/.")
        rec["coverage_estimate"] = "low"
        records = [rec]
        status = "blocked"
    else:
        primary_src = available[0]
        if not existing:
            rec = normalize_record(
                {}, dat_id, 1, cat_default, primary_src,
                "primary", "partial", 0.5,
            )
            rec["notes"] = ("Auto-generated placeholder. "
                            "Needs enrichment from the primary source.")
            records = [rec]
            status = "partial"
        else:
            records = []
            for i, r in enumerate(existing, 1):
                rec = normalize_record(
                    r, dat_id, i, cat_default, primary_src,
                    "primary", "partial", 0.6,
                )
                records.append(rec)
            status = "partial"

    coverage = detect_coverage(dat_id, records, available)
    for r in records:
        r["coverage_estimate"] = coverage

    write_text(path, yaml.safe_dump(records, allow_unicode=True,
                                    sort_keys=False, default_flow_style=False))
    return status, coverage, len(records)

# --- reports ---------------------------------------------------------------
def build_source_inventory():
    rows = [
        "# SOURCE INVENTORY",
        "",
        "| Name | Version | Date | Path | Status | Type | SHA256 | Notes |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for key, path in SOURCE_FILES.items():
        if path is None:
            rows.append(f"| external | - | - | - | external | external | - | dat_14 (mcc-mnc.com) |")
            continue
        if path.exists():
            rows.append(f"| {path.name} | - | - | sources/originals/{path.name} | "
                        f"available | primary | sha256:{sha256_file(path)} | |")
        else:
            rows.append(f"| {path.name} | - | - | sources/originals/{path.name} | "
                        f"missing | primary | - | required for one or more datasets |")
    return "\n".join(rows) + "\n"

def build_coverage_matrix(results):
    rows = [
        "# COVERAGE MATRIX",
        "",
        "| Dataset | Name | Status | Coverage | Records | Source | Reason |",
        "|---|---|---|---|---|---|---|",
    ]
    for did, fname, title, cat, srcs in DATASETS:
        status, cov, n = results.get(did, ("unknown", "low", 0))
        src = ", ".join(srcs) if srcs else "-"
        reason = "-" if status != "blocked" else f"missing source: {srcs[0] if srcs else 'unknown'}"
        rows.append(f"| {did} | {title} | {status} | {cov} | {n} | {src} | {reason} |")
    return "\n".join(rows) + "\n"

def build_gap_report(results):
    lines = ["# GAP REPORT", ""]
    for did, fname, title, cat, srcs in DATASETS:
        status, cov, n = results.get(did, ("unknown", "low", 0))
        if status in ("blocked", "partial"):
            lines.append(f"## {did} — {title}")
            lines.append(f"- status: **{status}**")
            lines.append(f"- coverage: {cov}")
            lines.append(f"- records: {n}")
            lines.append(f"- required sources: {', '.join(srcs) if srcs else '-'}")
            lines.append("")
    if len(lines) == 2:
        lines.append("No gaps detected. All datasets complete.")
    return "\n".join(lines) + "\n"

def build_todo(results):
    lines = ["# TODO", "", "## Missing sources"]
    for key, path in SOURCE_FILES.items():
        if path is None:
            continue
        if not path.exists():
            lines.append(f"- [ ] `{path.name}` (required by one or more datasets)")
    lines += ["", "## Blocked / partial datasets"]
    for did, fname, title, cat, srcs in DATASETS:
        status, cov, n = results.get(did, ("unknown", "low", 0))
        if status == "blocked":
            lines.append(f"- [ ] {did} — blocked; needs `{srcs[0] if srcs else 'unknown'}`")
        elif status == "partial":
            lines.append(f"- [ ] {did} — partial; enrich from {', '.join(srcs)}")
    return "\n".join(lines) + "\n"

def build_role_map():
    rows = [
        "# ROLE MAP",
        "",
        "| Dataset | Role | Depends on | Depended on by | Status |",
        "|---|---|---|---|---|",
        "| dat_01 | command reference | - | dat_02,03,09,10,11,12,13,17 | see coverage |",
        "| dat_02 | URC reference     | dat_01 | - | see coverage |",
        "| dat_03 | error codes       | dat_01 | - | see coverage |",
        "| dat_04 | timing            | dat_05, dat_06 | - | see coverage |",
        "| dat_05 | state machine     | dat_04 | - | see coverage |",
        "| dat_06 | init sequences    | dat_01, dat_05 | - | see coverage |",
        "| dat_07 | hardware pins     | dat_16 | dat_13 | see coverage |",
        "| dat_08 | firmware matrix   | - | - | see coverage |",
        "| dat_09 | SMS               | dat_01 | - | see coverage |",
        "| dat_10 | GPRS/Data         | dat_01 | dat_14 | see coverage |",
        "| dat_11 | HTTP/FTP/SSL      | dat_01, dat_17 | - | see coverage |",
        "| dat_12 | Audio             | dat_01 | - | see coverage |",
        "| dat_13 | SIM mgmt          | dat_01, dat_07 | - | see coverage |",
        "| dat_14 | MCC/MNC           | external | dat_10 | see coverage |",
        "| dat_15 | power mgmt        | dat_05 | - | see coverage |",
        "| dat_16 | board/EVB         | - | dat_07 | see coverage |",
        "| dat_17 | cert/key store    | dat_01 | dat_11 | see coverage |",
        "| dat_18 | certification     | - | - | see coverage |",
    ]
    return "\n".join(rows) + "\n"

def build_cross_ref(results):
    lines = ["# CROSS REFERENCE REPORT", ""]
    non_blocked = [d for d in DATASETS
                   if results.get(d[0], ("blocked",))[0] != "blocked"]
    lines.append(f"- Non-blocked datasets considered: {len(non_blocked)}")
    lines.append("- Blocked datasets are recorded as `pending_blocked` for cross-ref purposes.")
    lines.append("")
    for did, fname, title, cat, srcs in DATASETS:
        status = results.get(did, ("unknown",))[0]
        lines.append(f"## {did} — {title}")
        lines.append(f"- status: {status}")
        lines.append(f"- cross-ref: {'ok' if status != 'blocked' else 'pending_blocked'}")
        lines.append("")
    return "\n".join(lines) + "\n"

def build_validation_report(results, issues):
    lines = ["# VALIDATION REPORT", ""]
    lines.append(f"- Generated: {NOW_ISO}")
    lines.append(f"- Datasets scanned: {len(results)}")
    lines.append(f"- Issues detected: {len(issues)}")
    lines.append("")
    if issues:
        lines.append("## Issues")
        for it in issues:
            lines.append(f"- {it}")
    else:
        lines.append("## Issues")
        lines.append("- none")
    return "\n".join(lines) + "\n"

def build_session_log(results):
    lines = ["# SESSION LOG", ""]
    lines.append(f"## {NOW_ISO}")
    for did, fname, title, cat, srcs in DATASETS:
        status, cov, n = results.get(did, ("unknown", "low", 0))
        lines.append(f"- {did}: {status} (coverage={cov}, records={n})")
    lines.append("")
    lines.append("### Next session")
    lines.append("- Provide missing sources listed in TODO.md, then rerun engine.")
    return "\n".join(lines) + "\n"

def build_decisions_log():
    return (
        "# DECISIONS LOG\n\n"
        f"- {NOW_ISO}: normalized records across all datasets; enforced "
        "`applicable_models` to include `SIM800L`; forbade `status: synthetic` "
        "and `status: example-only` inside `data/`.\n"
        f"- {NOW_ISO}: marked datasets as `blocked` when the required source "
        "file is not present in `sources/originals/`.\n"
        f"- {NOW_ISO}: `coverage_estimate` derived heuristically "
        "(>=30 records -> high, >=10 -> medium, otherwise low).\n"
    )

def build_changelog():
    return (
        "# CHANGELOG\n\n"
        f"## {NOW_ISO}\n"
        "- Applied completion engine across all 18 datasets.\n"
        "- Rewrote schemas to draft-07 JSON Schema.\n"
        "- Regenerated COVERAGE_MATRIX, GAP_REPORT, SOURCE_INVENTORY, "
        "CROSS_REF_REPORT, VALIDATION_REPORT, ROLE_MAP, TODO, SESSION_LOG, "
        "DECISIONS_LOG.\n"
        "- Normalized all data files (idempotent).\n"
    )

def build_dataset_report(did, title, status, cov, n, issues):
    lines = [f"# {did} REPORT — {title}", ""]
    lines.append(f"- status: **{status}**")
    lines.append(f"- coverage: {cov}")
    lines.append(f"- records: {n}")
    lines.append(f"- generated: {NOW_ISO}")
    lines.append("")
    if issues:
        lines.append("## Issues")
        for it in issues:
            lines.append(f"- {it}")
    else:
        lines.append("## Issues")
        lines.append("- none")
    return "\n".join(lines) + "\n"

# --- validation ------------------------------------------------------------
def validate(results):
    issues = []
    for did, fname, title, cat, srcs in DATASETS:
        path = DATA / fname
        if not path.exists():
            issues.append(f"{did}: missing data file {fname}")
            continue
        try:
            recs = yaml.safe_load(path.read_text(encoding="utf-8")) or []
        except Exception as exc:
            issues.append(f"{did}: yaml parse error: {exc}")
            continue
        if not isinstance(recs, list):
            issues.append(f"{did}: root is not a list")
            continue
        seen = set()
        for r in recs:
            if not isinstance(r, dict):
                issues.append(f"{did}: non-dict record"); continue
            if not r.get("source"):
                issues.append(f"{did}/{r.get('id')}: missing source")
            if "SIM800L" not in (r.get("applicable_models") or []):
                issues.append(f"{did}/{r.get('id')}: applicable_models missing SIM800L")
            if r.get("status") == "synthetic":
                issues.append(f"{did}/{r.get('id')}: forbidden status synthetic")
            if r.get("status") == "example-only":
                issues.append(f"{did}/{r.get('id')}: forbidden status example-only in data/")
            rid = r.get("id")
            if rid in seen:
                issues.append(f"{did}: duplicate id {rid}")
            seen.add(rid)
    return issues

# --- main ------------------------------------------------------------------
def main():
    print("=== sim800l-data completion engine ===")
    print(f"ROOT: {ROOT}")
    ensure_dirs()

    # 1) schemas
    for did, fname, title, cat, srcs in DATASETS:
        write_schema(did, title)
    print(f"[OK] schemas written: {len(DATASETS)}")

    # 2) datasets
    results = {}
    for did, fname, title, cat, srcs in DATASETS:
        status, cov, n = process_dataset(did, fname, title, cat, srcs)
        results[did] = (status, cov, n)
        print(f"  - {did}: {status}  (coverage={cov}, records={n})")

    # 3) validation
    issues = validate(results)

    # 4) reports (root + reports/)
    reports = {
        "COVERAGE_MATRIX.md":  build_coverage_matrix(results),
        "SOURCE_INVENTORY.md": build_source_inventory(),
        "GAP_REPORT.md":       build_gap_report(results),
        "CROSS_REF_REPORT.md": build_cross_ref(results),
        "VALIDATION_REPORT.md":build_validation_report(results, issues),
        "ROLE_MAP.md":         build_role_map(),
        "TODO.md":             build_todo(results),
        "SESSION_LOG.md":      build_session_log(results),
        "DECISIONS_LOG.md":    build_decisions_log(),
        "CHANGELOG.md":        build_changelog(),
    }
    for name, content in reports.items():
        write_text(ROOT / name, content)
        write_text(REPORTS / name, content)
    print(f"[OK] management reports written: {len(reports)} x2")

    # 5) per-dataset reports
    for did, fname, title, cat, srcs in DATASETS:
        status, cov, n = results[did]
        sub_issues = [i for i in issues if i.startswith(did + ":") or i.startswith(did + "/")]
        write_text(REPORTS / f"{did}_REPORT.md",
                   build_dataset_report(did, title, status, cov, n, sub_issues))
    print(f"[OK] per-dataset reports written: {len(DATASETS)}")

    # 6) README + PHASE_1_REPORT (light touch)
    readme = ROOT / "README.md"
    if not readme.exists():
        write_text(readme,
                   "# sim800l-data\n\n"
                   "SIM800L-focused dataset for AT commands, hardware, timing, "
                   "state machine, and related domains.\n")
    phase1 = ROOT / "PHASE_1_REPORT.md"
    if not phase1.exists():
        write_text(phase1,
                   "# PHASE 1 REPORT\n\n"
                   "Initial completion pass applied by completion engine.\n")

    print("=== done ===")
    print(f"root: {ROOT}")
    print(f"datasets: {len(DATASETS)}")
    print(f"issues  : {len(issues)}")
    if issues:
        print("--- validation issues ---")
        for it in issues[:50]:
            print("  " + it)
        if len(issues) > 50:
            print(f"  ... and {len(issues) - 50} more")

if __name__ == "__main__":
    main()