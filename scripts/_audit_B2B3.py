#!/usr/bin/env python3
"""Audit dat_02 and dat_03 records after B2+B3 retry."""
import sys, json, re
from pathlib import Path
try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml"))
    return c[0] if c else (DATA / (dat_id + ".yaml") if (DATA / (dat_id + ".yaml")).exists() else None)

def is_urc_quote_ok(quote):
    """URC quote must contain URC markers: :, <, >, URC, unsolicited."""
    if not quote:
        return False
    q = str(quote)
    if "AT+" in q and not any(m in q for m in [":", "<", ">", "URC", "unsolicited", "indication"]):
        return False
    return any(m in q for m in [":", "<", ">", "URC", "unsolicited", "indication"])

SUSPICIOUS_ERR_WORDS = ["supported", "list", "section", "table", "overview", "appendix"]

def is_err_meaning_ok(meaning):
    if not meaning:
        return False
    m = str(meaning).lower()
    for w in SUSPICIOUS_ERR_WORDS:
        if w in m:
            return False
    return True

report = {"dat_02": {"total": 0, "suspicious": [], "ok": 0},
          "dat_03": {"total": 0, "suspicious": [], "ok": 0}}

p02 = find("dat_02")
if p02:
    records = yaml.safe_load(p02.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    for r in records:
        if not isinstance(r, dict): continue
        report["dat_02"]["total"] += 1
        src = r.get("source") or {}
        quote = src.get("quote") if isinstance(src, dict) else None
        if is_urc_quote_ok(quote):
            report["dat_02"]["ok"] += 1
        else:
            report["dat_02"]["suspicious"].append(r.get("id", "?"))

p03 = find("dat_03")
if p03:
    records = yaml.safe_load(p03.read_text(encoding="utf-8")) or []
    if not isinstance(records, list): records = [records]
    for r in records:
        if not isinstance(r, dict): continue
        report["dat_03"]["total"] += 1
        meaning = r.get("meaning") or ""
        if is_err_meaning_ok(meaning):
            report["dat_03"]["ok"] += 1
        else:
            report["dat_03"]["suspicious"].append(r.get("id", "?"))

out = REPORTS / "_step_B4_audit_B2B3.json"
out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

s2t = report["dat_02"]["total"]
s2s = len(report["dat_02"]["suspicious"])
s3t = report["dat_03"]["total"]
s3s = len(report["dat_03"]["suspicious"])
print(f"dat_02: total={s2t} suspicious={s2s} ok={report['dat_02']['ok']}")
print(f"dat_03: total={s3t} suspicious={s3s} ok={report['dat_03']['ok']}")
p2 = (s2s / s2t * 100) if s2t else 0
p3 = (s3s / s3t * 100) if s3t else 0
print(f"dat_02 suspicious% = {p2:.1f}")
print(f"dat_03 suspicious% = {p3:.1f}")