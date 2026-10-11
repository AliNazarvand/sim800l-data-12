#!/usr/bin/env python3
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
s = json.loads((REPORTS / "_validation_summary.json").read_text(encoding="utf-8"))
l3 = s["counts"].get("3", 0)
wl = s.get("specialist_commands_count", 0)
out = {"L3": l3, "whitelist": wl, "verified": l3 <= 2}
(REPORTS / "_d12_l3_confirm.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"L3={l3} whitelist={wl} verified={l3<=2}")