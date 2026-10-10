#!/usr/bin/env python3
"""validate.py — اعتبارسنجی سبک schema + business logic + یکتایی id"""
import sys, yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REQ = ["id","category","source","source_type","confidence","status","applicable_models","created_at","updated_at"]
VALID_STATUS = {"complete","partial","unknown","inferred","blocked","deferred","example-only"}
VALID_ST = {"primary","secondary","external"}

def check(dat_id):
    p = DATA / f"{dat_id}.yaml"
    if not p.exists():
        return [f"[{dat_id}] missing data file"], []
    try:
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    except Exception as e:
        return [f"[{dat_id}] YAML parse error: {e}"], []
    if not isinstance(d, list): d = [d]
    errs, warns = [], []
    ids = set()
    for r in d:
        if not isinstance(r, dict):
            errs.append(f"[{dat_id}] non-dict record"); continue
        for f in REQ:
            if f not in r: errs.append(f"[{dat_id}] missing field {f} in {r.get('id','?')}")
        rid = r.get("id","")
        if rid in ids: errs.append(f"[{dat_id}] duplicate id {rid}")
        ids.add(rid)
        if r.get("status") == "example-only":
            errs.append(f"[{dat_id}] example-only in data/ ({rid})")
        if r.get("status") not in VALID_STATUS:
            errs.append(f"[{dat_id}] invalid status {r.get('status')} ({rid})")
        if r.get("source_type") not in VALID_ST:
            errs.append(f"[{dat_id}] invalid source_type ({rid})")
        if "SIM800L" not in (r.get("applicable_models") or []):
            errs.append(f"[{dat_id}] applicable_models missing SIM800L ({rid})")
    return errs, warns

def main():
    all_errs, all_warns = [], []
    for i in range(1, 19):
        dat = f"dat_{i:02d}"
        e, w = check(dat)
        all_errs += e; all_warns += w
    rp = ROOT / "reports" / "VALIDATION_REPORT.md"
    rp.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# VALIDATION_REPORT", "", f"## خطاها ({len(all_errs)})", ""]
    lines += [f"- {x}" for x in all_errs]
    lines += ["", f"## هشدارها ({len(all_warns)})", ""]
    lines += [f"- {x}" for x in all_warns]
    rp.write_text("\n".join(lines), encoding="utf-8")
    print(f"Validation: {len(all_errs)} errors, {len(all_warns)} warnings")
    sys.exit(1 if all_errs else 0)

if __name__ == "__main__":
    main()