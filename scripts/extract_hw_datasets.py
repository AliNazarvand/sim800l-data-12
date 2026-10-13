"""
Reads CSV tables previously extracted from the hardware design PDFs and
produces real records for:
  - dat_07 hardware_reference
  - dat_04 timing_timeout
  - dat_15 power_management

The CSVs live under sources/extracted/tables/<hw_v2_02|hw_v1_00>/_raw/.
Filenames encode the PDF page and table index, e.g. ..._p017_t01.csv.
We classify each CSV by inspecting its header row and emit records
accordingly. Records follow schemas/dat_XX.schema.yaml (subset of fields).
"""
import sys, csv, re, json, datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML missing"); sys.exit(3)

NOW = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

PIN_HEADER_KEYS = {"pin", "pin no", "pin number", "no.", "no", "pin#", "number"}
PIN_NAME_KEYS   = {"name", "signal", "pin name", "signal name", "symbol"}
PIN_DESC_KEYS   = {"description", "function", "comment", "remarks", "note", "notes"}
PIN_IO_KEYS     = {"i/o", "io", "direction", "type", "in/out"}

TIMING_KEYS     = {"parameter", "item", "symbol"}
TIMING_MIN_KEYS = {"min", "minimum", "min."}
TIMING_TYP_KEYS = {"typ", "typical", "type", "typ."}
TIMING_MAX_KEYS = {"max", "maximum", "max."}
TIMING_UNIT_KEYS= {"unit", "units"}

POWER_KEYS      = {"mode", "state", "parameter", "item"}
POWER_CURR_KEYS = {"current", "current (ma)", "current(ma)", "icc", "consumption"}

def norm(s):
    if s is None: return ""
    return re.sub(r"\s+", " ", str(s).strip().lower())

def pick(d, *keys):
    for k, v in d.items():
        nk = norm(k)
        for want in keys:
            if nk == want or nk.startswith(want + " ") or nk.endswith(" " + want):
                return v
    return ""

def is_pin_table(headers):
    hs = {norm(h) for h in headers}
    return bool(hs & PIN_HEADER_KEYS) and bool(hs & PIN_NAME_KEYS)

def is_timing_table(headers):
    hs = {norm(h) for h in headers}
    has_param = bool(hs & TIMING_KEYS)
    has_range = bool(hs & TIMING_MIN_KEYS) or bool(hs & TIMING_TYP_KEYS) or bool(hs & TIMING_MAX_KEYS)
    return has_param and has_range

def is_power_table(headers):
    hs = {norm(h) for h in headers}
    return bool(hs & POWER_CURR_KEYS) and bool(hs & POWER_KEYS)

def parse_csv(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace", newline="") as f:
            reader = csv.reader(f)
            rows = [r for r in reader if any(c.strip() for c in r)]
    except Exception:
        return [], []
    if not rows:
        return [], []
    headers = rows[0]
    data = []
    for r in rows[1:]:
        if len(r) < len(headers):
            r = r + [""] * (len(headers) - len(r))
        data.append(dict(zip(headers, r)))
    return headers, data

def page_from_name(name):
    m = re.search(r"_p(\d+)", name)
    return int(m.group(1)) if m else None

def pdf_version_from_path(path):
    s = str(path).lower()
    if "hw_v2_02" in s: return "V2.02", "2015-07-27", "SIM800H&SIM800L_Hardware_Design"
    if "hw_v1_00" in s: return "V1.00", "2013-08-20", "SIM800L_Hardware_Design"
    return "unknown", "unknown", "unknown"

def make_common(ds_prefix, idx, src_name, src_version, src_date, page):
    return {
        "id": f"{ds_prefix}_{idx:04d}",
        "source": {
            "name": src_name,
            "version": src_version,
            "date": src_date,
            "page": str(page) if page else "",
            "section": "",
            "quote": ""
        },
        "source_type": "primary",
        "confidence": 0.9,
        "status": "complete",
        "conflicts": [],
        "notes": "",
        "tags": ["auto-extracted"],
        "applicable_models": ["SIM800L"],
        "created_at": NOW,
        "updated_at": NOW
    }

def emit_dat07(headers, rows, csvpath, counter, out):
    version, date, name = pdf_version_from_path(csvpath)
    page = page_from_name(csvpath.name)
    for r in rows:
        pin = pick(r, *PIN_HEADER_KEYS)
        sig = pick(r, *PIN_NAME_KEYS)
        if not str(pin).strip() and not str(sig).strip():
            continue
        counter[0] += 1
        rec = make_common("dat_07", counter[0], name, version, date, page)
        rec.update({
            "category": "Hardware",
            "name": str(sig).strip() or f"PIN_{pin}",
            "pin_number": str(pin).strip(),
            "direction": str(pick(r, *PIN_IO_KEYS)).strip(),
            "voltage_min": None, "voltage_typ": None, "voltage_max": None,
            "current_typ": None, "current_max": None,
            "function": str(pick(r, *PIN_DESC_KEYS)).strip(),
            "alternate_function": None,
            "pull_up_down": None, "esd_rating": None,
            "impedance": None, "decoupling": None
        })
        out.append(rec)

def emit_dat04(headers, rows, csvpath, counter, out):
    version, date, name = pdf_version_from_path(csvpath)
    page = page_from_name(csvpath.name)
    for r in rows:
        param = pick(r, *TIMING_KEYS)
        if not str(param).strip():
            continue
        counter[0] += 1
        def tofloat(x):
            try: return float(str(x).strip())
            except (TypeError, ValueError): return None
        rec = make_common("dat_04", counter[0], name, version, date, page)
        rec.update({
            "category": "Timing",
            "parameter": str(param).strip(),
            "min": tofloat(pick(r, *TIMING_MIN_KEYS)),
            "typ": tofloat(pick(r, *TIMING_TYP_KEYS)),
            "max": tofloat(pick(r, *TIMING_MAX_KEYS)),
            "unit": str(pick(r, *TIMING_UNIT_KEYS)).strip(),
            "condition": "",
            "related_command": None,
            "related_state": None,
            "related_urc": None
        })
        out.append(rec)

def emit_dat15(headers, rows, csvpath, counter, out):
    version, date, name = pdf_version_from_path(csvpath)
    page = page_from_name(csvpath.name)
    for r in rows:
        mode = pick(r, *POWER_KEYS)
        if not str(mode).strip():
            continue
        counter[0] += 1
        rec = make_common("dat_15", counter[0], name, version, date, page)
        rec.update({
            "category": "Power",
            "mode": str(mode).strip(),
            "command": None,
            "parameter": "current",
            "value_min": None, "value_typ": None, "value_max": None,
            "unit": "mA",
            "condition": "",
            "wake_source": None,
            "related_commands": [], "related_states": []
        })
        out.append(rec)

def main():
    root = Path(sys.argv[1])
    tables_root = root / "sources" / "extracted" / "tables"
    if not tables_root.exists():
        print("no tables dir; nothing to extract"); return
    csvs = []
    for sub in ("hw_v2_02", "hw_v1_00"):
        d = tables_root / sub / "_raw"
        if d.exists():
            csvs.extend(sorted(d.glob("*.csv")))
    if not csvs:
        print("no CSV tables found"); return

    dat07, dat04, dat15 = [], [], []
    c07 = [0]; c04 = [0]; c15 = [0]
    stats = {"pin_tables": 0, "timing_tables": 0, "power_tables": 0, "skipped": 0}

    for c in csvs:
        headers, rows = parse_csv(c)
        if not headers:
            stats["skipped"] += 1; continue
        if is_pin_table(headers):
            stats["pin_tables"] += 1
            emit_dat07(headers, rows, c, c07, dat07)
        elif is_timing_table(headers):
            stats["timing_tables"] += 1
            emit_dat04(headers, rows, c, c04, dat04)
        elif is_power_table(headers):
            stats["power_tables"] += 1
            emit_dat15(headers, rows, c, c15, dat15)
        else:
            stats["skipped"] += 1

    data_dir = root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    def dump(path, records):
        if not records:
            path.write_text("[]\n", encoding="utf-8")
            return
        with open(path, "w", encoding="utf-8") as f:
            yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False)

    # MERGE (do not overwrite existing non-empty files if new extraction is empty)
    def merge(path, new):
        existing = []
        if path.exists():
            try:
                existing = yaml.safe_load(path.read_text(encoding="utf-8")) or []
                if not isinstance(existing, list): existing = []
            except Exception:
                existing = []
        if not new:
            return existing
        # keep records whose id is not in new (preserve manual edits)
        new_ids = {r.get("id") for r in new if isinstance(r, dict)}
        preserved = [r for r in existing if isinstance(r, dict) and r.get("id") not in new_ids]
        return preserved + new

    p07 = data_dir / "dat_07_hardware_reference.yaml"
    p04 = data_dir / "dat_04_timing_timeout.yaml"
    p15 = data_dir / "dat_15_power_management.yaml"

    merged07 = merge(p07, dat07)
    merged04 = merge(p04, dat04)
    merged15 = merge(p15, dat15)

    dump(p07, merged07)
    dump(p04, merged04)
    dump(p15, merged15)

    summary = {
        "csv_files_scanned": len(csvs),
        "pin_tables": stats["pin_tables"],
        "timing_tables": stats["timing_tables"],
        "power_tables": stats["power_tables"],
        "skipped_csv": stats["skipped"],
        "dat_07_records": len(merged07),
        "dat_04_records": len(merged04),
        "dat_15_records": len(merged15),
    }
    (root / "reports" / "_hw_extraction_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()