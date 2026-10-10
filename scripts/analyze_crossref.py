#!/usr/bin/env python3
"""analyze_crossref.py - تحلیل ناسازگاری فرمت داده‌ها بین دیتاست‌ها"""
from __future__ import annotations
import re
from pathlib import Path
from collections import Counter

try:
    import yaml
except ImportError:
    print("[ERROR] pip install pyyaml"); raise SystemExit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORT = ROOT / "reports" / "CROSSREF_GAP_ANALYSIS.md"

ID_RE = re.compile(r"^dat_\d{2}_\d{4}$")

def load_all():
    by_ds = {i: [] for i in range(1, 19)}
    for yml in DATA.rglob("*.yaml"):
        try:
            data = yaml.safe_load(yml.read_text(encoding="utf-8"))
        except Exception:
            continue
        def walk(o):
            if isinstance(o, list):
                for x in o: walk(x)
            elif isinstance(o, dict):
                if isinstance(o.get("id"), str) and ID_RE.match(o["id"]):
                    try:
                        ds = int(o["id"].split("_")[1])
                        by_ds[ds].append(o)
                    except Exception: pass
                for v in o.values(): walk(v)
        walk(data)
    return by_ds

def main():
    by_ds = load_all()
    L = ["# Cross-Reference Gap Analysis\n\n",
         "تحلیل ناسازگاری فرمت‌ها در فیلدهای کلیدی.\n\n"]

    # تحلیل command در dat_01
    L.append("## نمونه command در dat_01\n\n```\n")
    cmds = [r.get("command") for r in by_ds[1][:20] if r.get("command")]
    for c in cmds: L.append(f"  {c!r}\n")
    L.append("```\n\n")

    L.append("## نمونه command در dat_09..17\n\n")
    for ds in [9, 10, 11, 12, 13, 15, 17]:
        recs = [r.get("command") for r in by_ds[ds][:5] if r.get("command")]
        if recs:
            L.append(f"### dat_{ds:02d}\n```\n")
            for c in recs: L.append(f"  {c!r}\n")
            L.append("```\n\n")

    # تحلیل related_command در dat_02
    L.append("## نمونه related_command در dat_02\n\n```\n")
    for r in by_ds[2][:10]:
        L.append(f"  {r.get('id')}: {r.get('related_command')!r}\n")
    L.append("```\n\n")

    # تحلیل related_commands در dat_03
    L.append("## نمونه related_commands در dat_03\n\n```\n")
    for r in by_ds[3][:10]:
        L.append(f"  {r.get('id')}: {r.get('related_commands')!r}\n")
    L.append("```\n\n")

    # تحلیل supported_commands در dat_08
    L.append("## نمونه supported_commands در dat_08\n\n```\n")
    for r in by_ds[8][:5]:
        L.append(f"  {r.get('id')}: {r.get('supported_commands')}\n")
    L.append("```\n\n")

    # تحلیل related_states در dat_15
    L.append("## نمونه related_states در dat_15\n\n```\n")
    for r in by_ds[15][:10]:
        L.append(f"  {r.get('id')}: {r.get('related_states')!r}\n")
    L.append("```\n\n")

    # تحلیل state_name در dat_05
    L.append("## نمونه state_name در dat_05\n\n```\n")
    for r in by_ds[5][:15]:
        L.append(f"  {r.get('id')}: {r.get('state_name')!r}\n")
    L.append("```\n")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("".join(L), encoding="utf-8")
    print(f"[REPORT] {REPORT}")
    print(f"dat_01: {len(by_ds[1])}, dat_02: {len(by_ds[2])}, dat_03: {len(by_ds[3])}, dat_05: {len(by_ds[5])}, dat_08: {len(by_ds[8])}, dat_09: {len(by_ds[9])}")

if __name__ == "__main__":
    main()
