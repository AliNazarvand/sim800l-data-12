#!/usr/bin/env python3
"""
Validate every YAML file under data/** against its dataset schema.

Behavior:
  * data/<dataset>/*.yaml are validated against schemas/<dataset>.schema.json
    when that schema file exists. If it does not exist, the file is only
    checked for a well-formed top-level structure.
  * _dataset_meta.yaml files are validated against a built-in meta schema.
  * Records must carry a _meta block with all required keys, a constant
    license_note, and a _meta.missing_reason drawn from the allowed set.
  * _meta.id values must be unique within a dataset.
  * When status is "complete" or "partial", record_count must match the
    actual number of records and be >= numeric min_records_required.

Exit code 0 on success, 1 on any failure.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
    from jsonschema import Draft202012Validator
except Exception as exc:  # pragma: no cover
    print(f"ERROR: missing dependency: {exc}", file=sys.stderr)
    print("Install with: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SCHEMAS = ROOT / "schemas"

DATASET_MAP = {
    "at_commands":          "dat_01",
    "urc":                  "dat_02",
    "error_codes":          "dat_03",
    "timing":               "dat_04",
    "state_machine":        "dat_05",
    "init_sequence":        "dat_06",
    "hardware":             "dat_07",
    "firmware_compat":      "dat_08",
    "sms":                  "dat_09",
    "gprs_data":            "dat_10",
    "http_ftp_ssl":         "dat_11",
    "audio":                "dat_12",
    "sim_management":       "dat_13",
    "operator_apn":         "dat_14",
    "power_management":     "dat_15",
    "board_evb":            "dat_16",
    "certificate_keystore": "dat_17",
    "certification":        "dat_18",
}

LICENSE_NOTE = "See NOTICE file for licensing and copyright information."
ALLOWED_MISSING = {
    "NOT_FOUND_IN_SOURCES",
    "DEFERRED_TO_PHASE_2A",
    "DEFERRED_TO_PHASE_2B",
    "CONFLICTING_SOURCES",
    "MIXED",
}
ID_RE = re.compile(r"^dat_[0-9]{2}_[a-z0-9_]+_[0-9]{3}$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

REQUIRED_META_KEYS = {
    "id", "source", "source_version", "source_page", "source_section",
    "source_figure_number", "extracted_at", "pending_fields",
    "compatible_models", "missing_reason", "completion_source",
    "license_note",
}

def load_yaml(p: Path):
    with p.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)

def records_of(doc):
    if doc is None:
        return []
    if isinstance(doc, dict):
        return doc.get("records") or []
    if isinstance(doc, list):
        return doc
    return []

def check_meta(rec, path, idx, errs):
    meta = rec.get("_meta") if isinstance(rec, dict) else None
    if not isinstance(meta, dict):
        errs.append(f"{path} record[{idx}]: missing _meta object")
        return
    for k in REQUIRED_META_KEYS:
        if k not in meta:
            errs.append(f"{path} record[{idx}] _meta: missing '{k}'")
    if meta.get("license_note") not in (None, LICENSE_NOTE):
        errs.append(f"{path} record[{idx}] _meta.license_note: must equal {LICENSE_NOTE!r}")
    if meta.get("missing_reason") is not None and meta.get("missing_reason") not in ALLOWED_MISSING:
        errs.append(f"{path} record[{idx}] _meta.missing_reason: invalid value {meta.get('missing_reason')!r}")
    if meta.get("missing_reason") == "MIXED" and not meta.get("pending_fields"):
        errs.append(f"{path} record[{idx}] _meta: missing_reason=MIXED requires non-empty pending_fields")
    rid = meta.get("id")
    if isinstance(rid, str) and not ID_RE.match(rid):
        errs.append(f"{path} record[{idx}] _meta.id: does not match pattern")
    ea = meta.get("extracted_at")
    if isinstance(ea, str) and not ISO_DATE_RE.match(ea):
        errs.append(f"{path} record[{idx}] _meta.extracted_at: not ISO 8601 date")
    if meta.get("deprecated_in") and meta.get("source_version") != "V1.00":
        errs.append(f"{path} record[{idx}] _meta.deprecated_in: only allowed when source_version=V1.00")
    cm = meta.get("compatible_models")
    if not (isinstance(cm, list) and cm and all(x in ("SIM800L","SIM800H") for x in cm)):
        errs.append(f"{path} record[{idx}] _meta.compatible_models: must be non-empty subset of ['SIM800L','SIM800H']")

def validate_dataset_file(p: Path, schema: dict | None, cache: dict, errs) -> int:
    """
    Validate one dataset YAML file.

    Returns the number of records found in the file (0 on parse error).
    Errors are appended to `errs` in place.
    """
    try:
        doc = load_yaml(p)
    except Exception as exc:
        errs.append(f"{p}: YAML parse error: {exc}")
        return 0
    records = records_of(doc)
    ids = {}
    validator = None
    if schema is not None:
        key = json.dumps(schema, sort_keys=True)
        if key not in cache:
            Draft202012Validator.check_schema(schema)
            cache[key] = Draft202012Validator(schema)
        validator = cache[key]
    for i, rec in enumerate(records):
        check_meta(rec, p, i, errs)
        if validator is not None:
            for e in validator.iter_errors(rec):
                loc = "/".join(str(x) for x in e.absolute_path)
                errs.append(f"{p} record[{i}] {loc or '<root>'}: {e.message}")
        if isinstance(rec, dict):
            rid = (rec.get("_meta") or {}).get("id")
            if rid in ids:
                errs.append(f"{p}: duplicate id '{rid}' at records {ids[rid]} and {i}")
            elif rid:
                ids[rid] = i
    return len(records)

def validate_dataset_meta(folder: Path, actual_count: int, errs):
    meta = folder / "_dataset_meta.yaml"
    if not meta.exists():
        errs.append(f"{folder}: missing _dataset_meta.yaml")
        return
    try:
        doc = load_yaml(meta) or {}
    except Exception as exc:
        errs.append(f"{meta}: YAML parse error: {exc}")
        return
    for k in ("dataset_id", "dataset_name", "phase_completed", "record_count",
              "min_records_required", "status", "pending_fields",
              "completion_source", "last_updated", "retry_count"):
        if k not in doc:
            errs.append(f"{meta}: missing key '{k}'")
    status = doc.get("status")
    if status not in ("complete", "partial", "deferred"):
        errs.append(f"{meta}: invalid status {status!r}")
    if doc.get("record_count") != actual_count:
        errs.append(f"{meta}: record_count={doc.get('record_count')} does not match actual {actual_count}")
    if status in ("complete", "partial"):
        mr = doc.get("min_records_required")
        if isinstance(mr, int) and actual_count < mr:
            errs.append(f"{meta}: record_count {actual_count} < min_records_required {mr}")
    if status == "deferred" and not doc.get("reason"):
        errs.append(f"{meta}: status=deferred requires reason")
    lu = doc.get("last_updated")
    if isinstance(lu, str) and not ISO_DATE_RE.match(lu):
        errs.append(f"{meta}: last_updated not ISO 8601 date")

def main() -> int:
    if not DATA.exists():
        print(f"ERROR: data/ not found under {ROOT}", file=sys.stderr)
        return 1

    errs: list[str] = []
    cache: dict = {}

    for ds, schema_name in DATASET_MAP.items():
        folder = DATA / ds
        if not folder.exists():
            continue
        schema_path = SCHEMAS / f"{schema_name}.schema.json"
        schema = None
        if schema_path.exists():
            try:
                with schema_path.open("r", encoding="utf-8") as fh:
                    schema = json.load(fh)
            except Exception as exc:
                errs.append(f"{schema_path}: cannot load schema: {exc}")

        count = 0
        for p in sorted(folder.rglob("*.yaml")):
            if p.name == "_dataset_meta.yaml":
                continue
            count += validate_dataset_file(p, schema, cache, errs)

        validate_dataset_meta(folder, count, errs)

    if errs:
        for e in errs:
            print(e, file=sys.stderr)
        print(f"\nFAILED: {len(errs)} error(s).", file=sys.stderr)
        return 1
    print("OK: validation passed.")
    return 0

if __name__ == "__main__":
    sys.exit(main())


