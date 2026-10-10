#!/usr/bin/env python3
"""Final dat_07 cleanup:
- dedup by pin_number (NOT by name) — V2.02 > V1.00 > curated
- remove SIM800H-only pins (e.g. BT_ANT)
- clean junk continuation text in function field
- rewrite file with clean IDs
"""
import pathlib, re
from datetime import datetime, timezone
try:
    import yaml
except ImportError:
    print("pip install pyyaml"); raise SystemExit(2)

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

p = DATA / "dat_07_hardware_reference.yaml"
if not p.exists():
    print("dat_07 file missing"); raise SystemExit(1)
d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
recs = d.get("records") or []
print(f"  loaded {len(recs)} raw pins")

# -- 1) Filter SIM800H-only --
JUNK_NOTE = ["SIM800H", "SIM800H/L", "only SIM800H", "Bluetooth antenna Only"]
before = len(recs)
recs = [r for r in recs if not any(tok in (str(r.get("function","")) + str(r.get("notes",""))) for tok in JUNK_NOTE)]
print(f"  removed {before-len(recs)} SIM800H-only pins (kept {len(recs)})")

# -- 2) Clean function text (strip continuation fragments) --
JUNK_SUFFIXES = [
    "If these pins are unused, keep open.",
    "If these pins are unused,",
    "keep open.（Please make", "keep open.", "keep open",
    "least 1 second and then released to",
    "Connect to GND",  # not junk, but not useful either — actually keep
]
def clean_fn(fn):
    if not fn: return fn
    fn = re.sub(r'\s+', ' ', fn).strip()
    # remove any prefix that is actually the previous pin's text
    for tok in JUNK_SUFFIXES:
        if fn.endswith(tok):
            fn = fn[:-len(tok)].strip()
        if fn.startswith(tok):
            fn = fn[len(tok):].strip()
    return fn

MANUAL_FALLBACK = {
    "VBAT":      "Power supply (3.4-4.4V, 2A peak)",
    "VRTC":      "Power supply for RTC backup",
    "VDD_EXT":   "2.8V power output (max 50mA)",
    "VEXT":      "2.8V power output (max 50mA)",
    "PWRKEY":    "Power on/off, pulled low >=1s to switch",
    "PCM_OUT":   "PCM data output",
    "PCMOUT":    "PCM data output",
    "PCM_SYNC":  "PCM synchrony",
    "PCMSYNC":   "PCM synchrony",
    "PCMCLK":    "PCM clock",
    "PCMIN":     "PCM data input",
    "KBC4":      "Keypad column 4",
    "KBC3":      "Keypad column 3",
    "COL0":      "Keypad column 0 (pull up)",
    "COL1":      "Keypad column 1",
    "COL2":      "Keypad column 2",
    "COL3":      "Keypad column 3",
    "COL4":      "Keypad column 4",
    "ROW0":      "Keypad row 0",
    "ROW1":      "Keypad row 1",
    "ROW2":      "Keypad row 2",
    "ROW3":      "Keypad row 3",
    "ROW4":      "Keypad row 4",
    "NETLIGHT":  "Network status indication",
    "STATUS":    "Power on status indication",
    "DTR":       "Data terminal ready (UART)",
    "UART_DTR":  "Data terminal ready (UART)",
    "RI":        "Ring indicator (UART)",
    "UART_RI":   "Ring indicator (UART)",
    "DCD":       "Data carrier detect (UART)",
    "UART_DCD":  "Data carrier detect (UART)",
    "CTS":       "Clear to send (UART hardware flow control)",
    "RTS":       "Request to send (UART hardware flow control)",
    "TXD":       "Transmit data (UART)",
    "RXD":       "Receive data (UART)",
    "USB_DP":    "USB data plus (debug/download)",
    "USB_DM":    "USB data minus (debug/download)",
    "PWM":       "Pulse-width modulation output",
    "SDA":       "I2C serial bus data",
    "SCL":       "I2C serial bus clock",
    "SIM_VDD":   "SIM card voltage supply (1.8V or 3V)",
    "VSIM":      "SIM card voltage supply (1.8V or 3V)",
    "SIM_DATA":  "SIM card data I/O",
    "SIM_CLK":   "SIM card clock",
    "SIM_RST":   "SIM card reset",
    "SIM_DET":   "SIM card detection",
    "SIMPRE":    "SIM card detection",
    "GSM_ANT":   "GSM antenna (50 ohm)",
    "ANT":       "GSM antenna (50 ohm)",
    "FM_ANTP":   "FM differential antenna positive",
    "FM_ANT_P":  "FM differential antenna positive",
    "FM_ANT_N":  "FM differential antenna negative",
    "RF_SYNC":   "RF synchronization signal",
    "BPI_BUS1":  "RF synchronization signal",
    "RESET":     "Reset input (active low)",
    "ISINK0":    "LCD backlight current sink",
    "ISINK1":    "Keypad backlight current sink",
    "MIC1P": "Main Audio input positive",
    "MIC1N": "Main Audio input negative",
    "MIC2P": "Secondary Audio input positive",
    "MIC2N": "Secondary Audio input negative",
    "SPK1P": "Main Audio output positive",
    "SPK1N": "Main Audio output negative",
    "SPK2P": "Secondary Audio output positive",
    "SPK2N": "Secondary Audio output negative",
    "GPIO1": "Programmable GPIO 1",
    "GPIO2": "Programmable GPIO 2",
    "GPIO3": "Programmable GPIO 3",
    "VBUS":  "USB power supply (4.3-7V)",
    "ADC":   "10-bit ADC input (0-2.8V)",
}
for r in recs:
    nm = r.get("name","")
    if nm in MANUAL_FALLBACK:
        r["function"] = MANUAL_FALLBACK[nm]
    else:
        r["function"] = clean_fn(r.get("function",""))

# -- 3) Dedup by pin_number (V2.02 wins over V1.00 wins over curated) --
# Sort: V2.02 first, then V1.00, then curated (curated has notes containing 'curated')
def sort_key(r):
    ver = r.get("source",{}).get("version","")
    notes = r.get("notes","")
    prio = 3
    if ver == "V2.02": prio = 1
    elif ver == "V1.00" and "curated" not in notes: prio = 2
    elif "curated" in notes: prio = 4
    return prio
recs.sort(key=sort_key)

seen_pins = set()
merged = []
for r in recs:
    key = str(r.get("pin_number","")).strip()
    if not key or key == "":
        continue
    if key in seen_pins:
        continue
    seen_pins.add(key)
    merged.append(r)

print(f"  after dedup by pin_number: {len(merged)} pins")

# -- 4) Reassign IDs in stable order --
# Order by primary pin number
def first_pin_num(r):
    pn = str(r.get("pin_number",""))
    m = re.match(r'^(\d+)', pn)
    return int(m.group(1)) if m else 9999
merged.sort(key=first_pin_num)
for i, r in enumerate(merged, 1):
    r["id"] = f"dat_07_{i:04d}"
    r["updated_at"] = NOW

p.write_text(yaml.safe_dump({"records": merged}, allow_unicode=True, sort_keys=False, width=200),
             encoding="utf-8")
print(f"  [OK] wrote {len(merged)} unique pins -> {p.name}")

# Quick check for duplicates
from collections import Counter
cnt = Counter(str(r.get("pin_number","")) for r in merged)
dups = {k:v for k,v in cnt.items() if v > 1}
if dups:
    print(f"  [WARN] residual duplicate pin_numbers: {dups}")
else:
    print(f"  [OK] no duplicate pin_numbers")