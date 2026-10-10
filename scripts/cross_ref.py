#!/usr/bin/env python3
"""cross_ref.py — گزارش ارجاعات متقابل (YAML only)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

try:
    import yaml as _yaml
except ImportError:
    _yaml = None


def load_yaml(p: Path):
    return _yaml.safe_load(p.read_text(encoding="utf-8"))


def iter_records():
    for f in sorted(DATA.rglob("*.yaml")):
        if f.name.startswith("_dataset_meta"):
            continue
        try:
            obj = load_yaml(f)
        except Exception:
            continue
        if obj is None:
            continue
        if isinstance(obj, list):
            for rec in obj:
                yield f, rec
        elif isinstance(obj, dict) and "id" in obj:
            yield f, obj
        elif isinstance(obj, dict):
            for _k, v in obj.items():
                if isinstance(v, list):
                    for rec in v:
                        yield f, rec


def main() -> int:
    REPORTS.mkdir(parents=True, exist_ok=True)
    index = {}
    records_with_id = 0
    records_without_id = 0
    for _f, rec in iter_records():
        if not isinstance(rec, dict):
            continue
        rid = rec.get("id")
        if rid:
            records_with_id += 1
            index[rid] = _f.name
        else:
            records_without_id += 1

    rows = []
    for f, rec in iter_records():
        if not isinstance(rec, dict):
            continue
        rid = rec.get("id")
        for key in ("related_commands", "related_urcs", "related_timings"):
            for ref in (rec.get(key) or []):
                status = "resolved" if ref in index else "unresolved"
                rows.append((rid, key, ref, status, f.name))

    out = REPORTS / "CROSS_REF_REPORT.md"
    lines = [
        "# CROSS REF REPORT", "",
        f"تعداد رکورد با id: {records_with_id}",
        f"تعداد رکورد بدون id: {records_without_id}",
        f"تعداد ارجاعات: {len(rows)}",
        "",
    ]
    lines.append("| از | نوع | مقصد | وضعیت | فایل |")
    lines.append("|---|---|---|---|---|")
    for rid, key, ref, st, fn in rows:
        lines.append(f"| {rid} | {key} | {ref} | {st} | {fn} |")
    if not rows:
        lines.append("")
        lines.append("> هیچ ارجاع متقابلی در داده‌های فعلی یافت نشد.")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK]   {out.relative_to(ROOT)}  ({len(rows)} refs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())