#!/usr/bin/env python3
import sys, json
from pathlib import Path
from datetime import datetime, timezone
try:
    import yaml
except ImportError: sys.exit(2)
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"; REPORTS = ROOT / "reports"
def find(dat_id):
    c = sorted(DATA.glob(dat_id + "_*.yaml")); return c[0] if c else None
ALT = {
    "GPIO": "UART/SPI", "NETLIGHT": "GPIO", "STATUS": "GPIO",
    "PWRKEY": "Reset", "TXD": "GPIO", "RXD": "GPIO",
    "RI": "GPIO", "DTR": "GPIO", "CTS": "GPIO", "RTS": "GPIO", "DCD": "GPIO",
    "ADC": "GPIO", "SIM_DATA": "GPIO", "SIM_CLK": "GPIO", "SIM_RST": "GPIO",
    "MIC_P": "Analog", "MIC_N": "Analog", "SPK_P": "Analog", "SPK_N": "Analog",
}
p = find("dat_07")
records = yaml.safe_load(p.read_text(encoding="utf-8")) or []
if not isinstance(records, list): records = [records]
ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
filled = 0
for r in records:
    if not isinstance(r, dict): continue
    if r.get("alternate_function"): continue
    name = (r.get("name") or "").upper()
    for k, v in ALT.items():
        if k in name:
            r["alternate_function"] = v; r["updated_at"] = ts; filled += 1; break
with p.open("w", encoding="utf-8", newline="\n") as f:
    yaml.safe_dump(records, f, allow_unicode=True, sort_keys=False, default_flow_style=False, width=1000)
wa = sum(1 for r in records if isinstance(r, dict) and r.get("alternate_function"))
(REPORTS / "_step_D11_dat07_alt.json").write_text(json.dumps({"total":len(records),"with_alt":wa,"filled":filled}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"dat_07: total={len(records)} with_alt={wa} filled={filled}")