#!/usr/bin/env python3
"""گزارش Cross-Reference واقعی."""
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pyyaml"])
    import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def load(name):
    p = DATA / name
    if not p.exists(): return []
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or []

def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    files = {p.name: load(p.name) for p in sorted(DATA.glob("dat_*.yaml"))}

    out = [f"# CROSS_REF_REPORT", f"> auto-generated at {NOW}", ""]
    out.append("## شمارش رکوردها")
    for name, arr in files.items():
        out.append(f"- {name}: {len(arr)}")

    out.append("")
    out.append("## ارجاعات بین‌دیتاستی")
    cmd_set = {r.get("command") for r in files.get("dat_01_at_command.yaml", []) if r.get("command")}
    for fname, arr in files.items():
        if not arr: continue
        hits = 0
        misses = 0
        for r in arr:
            c = r.get("command")
            if not c: continue
            if c in cmd_set: hits += 1
            else: misses += 1
        if hits or misses:
            out.append(f"- {fname}: {hits} ارجاع موفق، {misses} ناموفق")

    (REPORTS / "CROSS_REF_REPORT.md").write_text("\n".join(out), encoding="utf-8")
    print("CROSS_REF_REPORT.md نوشته شد")
    return 0

if __name__ == "__main__":
    sys.exit(main())