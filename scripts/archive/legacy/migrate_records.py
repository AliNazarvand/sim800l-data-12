#!/usr/bin/env python3
"""
migrate_records.py — نرمال‌سازی رکوردهای YAML در data/**.

نسخه ۴:
  * فقط YAML.
  * id یکتا در سطح دیتاست.
  * source از _meta ساخته می‌شود و _meta حذف می‌شود (رفع R20).
  * status/confidence بر اساس _meta.pending_fields و _meta.missing_reason تعیین می‌شود.
  * اطلاعات مهم _meta (extracted_at, license_note) در notes حفظ می‌شوند.
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

DATASET_FOLDERS = {
    "at_commands": "01", "urc": "02", "error_codes": "03", "timing": "04",
    "state_machine": "05", "init_sequence": "06", "hardware": "07",
    "firmware_compat": "08", "sms": "09", "gprs_data": "10",
    "http_ftp_ssl": "11", "audio": "12", "sim_management": "13",
    "operator_apn": "14", "power_management": "15", "board_evb": "16",
    "certificate_keystore": "17", "certification": "18",
}

DATE_FROM_VERSION = {
    "V1.00": "2013-08-20",
    "V2.02": "2015-07-27",
}

try:
    import yaml as _yaml
except ImportError:
    print("[FATAL] PyYAML not installed")
    sys.exit(2)


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_yaml(p: Path):
    return _yaml.safe_load(p.read_text(encoding="utf-8"))


def dump_yaml(p: Path, obj):
    p.write_text(_yaml.safe_dump(obj, allow_unicode=True, sort_keys=False),
                 encoding="utf-8")


def folder_dat(file_path: Path):
    try:
        rel = file_path.relative_to(DATA)
    except ValueError:
        return None
    if not rel.parts:
        return None
    return DATASET_FOLDERS.get(rel.parts[0])


def build_source(meta):
    if not isinstance(meta, dict):
        return None
    name = meta.get("source")
    version = meta.get("source_version")
    if not name or not version:
        return None
    src = {"name": name, "version": version,
           "date": DATE_FROM_VERSION.get(version, "1970-01-01")}
    if meta.get("source_page") is not None:
        src["page"] = str(meta["source_page"])
    if meta.get("source_section") is not None:
        src["section"] = str(meta["source_section"])
    return src


def derive_status_confidence(meta):
    """status و confidence را از _meta استخراج می‌کند."""
    if not isinstance(meta, dict):
        return "unknown", 0.0
    missing_reason = meta.get("missing_reason")
    pending = meta.get("pending_fields") or []
    if missing_reason:
        return "unknown", 0.0
    if not pending:
        return "complete", 0.95
    return "partial", 0.7


class DatasetCounter:
    def __init__(self):
        self._c = {}

    def next_id(self, dat_id: str) -> str:
        n = self._c.get(dat_id, 0) + 1
        self._c[dat_id] = n
        return f"dat_{dat_id}_{n:04d}"


def migrate_list(lst, dat_id, counter):
    n_changed = 0
    for rec in lst:
        if not isinstance(rec, dict):
            continue
        changed = False

        # id یکتا در سطح دیتاست
        new_id = counter.next_id(dat_id)
        if rec.get("id") != new_id:
            rec["id"] = new_id
            changed = True

        if "category" not in rec:
            rec["category"] = "unspecified"
            changed = True

        meta = rec.pop("_meta", None) if isinstance(rec.get("_meta"), dict) else None
        if meta is not None:
            changed = True  # _meta حذف شد

        if meta:
            real_source = build_source(meta)
            if real_source is not None:
                rec["source"] = real_source
                rec["source_type"] = "primary"
            st, cf = derive_status_confidence(meta)
            rec["status"] = st
            rec["confidence"] = cf

            # حفظ notes مهم
            notes_parts = []
            if meta.get("license_note"):
                notes_parts.append(f"License: {meta['license_note']}")
            if meta.get("extracted_at"):
                notes_parts.append(f"Extracted at: {meta['extracted_at']}")
            if meta.get("source_figure_number"):
                notes_parts.append(f"Figure: {meta['source_figure_number']}")
            if notes_parts:
                existing = rec.get("notes") or ""
                extra = " | ".join(notes_parts)
                rec["notes"] = (existing + " | " + extra).strip(" |") if existing else extra
        else:
            if "source" not in rec:
                rec["source"] = {"name": "UNMIGRATED",
                                 "version": "0.0.0", "date": "1970-01-01"}
                changed = True
            if "source_type" not in rec:
                rec["source_type"] = "primary"
                changed = True
            if "confidence" not in rec:
                rec["confidence"] = 0.0
                changed = True
            if "status" not in rec:
                rec["status"] = "unknown"
                changed = True

        if "applicable_models" not in rec:
            rec["applicable_models"] = ["SIM800L"]
            changed = True
        if "created_at" not in rec:
            rec["created_at"] = now_iso()
            changed = True
        if "updated_at" not in rec:
            rec["updated_at"] = now_iso()
            changed = True

        if changed:
            n_changed += 1
    return n_changed


def migrate_file(f: Path, counter):
    dat_id = folder_dat(f)
    if dat_id is None:
        return 0
    try:
        obj = load_yaml(f)
    except Exception as e:
        print(f"[FAIL] parse {f.relative_to(ROOT)}: {e}")
        return 0
    if obj is None:
        return 0

    total = 0
    if isinstance(obj, list):
        total += migrate_list(obj, dat_id, counter)
    elif isinstance(obj, dict):
        if "id" in obj or any(k in obj for k in ("name", "pin_number", "command")):
            total += migrate_list([obj], dat_id, counter)
        else:
            for _k, v in obj.items():
                if isinstance(v, list):
                    total += migrate_list(v, dat_id, counter)

    if total:
        dump_yaml(f, obj)
    return total


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    counter = DatasetCounter()
    total_files = 0
    total_records = 0
    details = []
    for f in sorted(DATA.rglob("*.yaml")):
        if f.name.startswith("_dataset_meta"):
            continue
        n = migrate_file(f, counter)
        if n:
            total_files += 1
            total_records += n
            details.append((str(f.relative_to(ROOT)), n))
            print(f"[OK]   {f.relative_to(ROOT)}: {n} records")

    out = REPORTS / "MIGRATION_REPORT.md"
    lines = ["# MIGRATION REPORT", "",
             f"تاریخ: {now_iso()}",
             f"نسخه اسکریپت: ۴ (pending_fields + حذف _meta)",
             f"تعداد فایل‌های تغییر‌یافته: {total_files}",
             f"تعداد رکوردهای پردازش‌شده: {total_records}",
             "",
             "| فایل | رکوردها |",
             "|---|---|"]
    for fn, n in details:
        lines.append(f"| {fn} | {n} |")
    if not details:
        lines.append("")
        lines.append("> هیچ رکوردی نیازمند تغییر نبود.")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK]   {out.relative_to(ROOT)}  ({total_records} records)")
    return 0


if __name__ == "__main__":
    sys.exit(main())