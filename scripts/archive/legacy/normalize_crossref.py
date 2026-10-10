#!/usr/bin/env python3
"""
normalize_crossref.py (نسخه اصلاح‌شده)
- یکنواخت‌سازی command در قالب کانونیک +CMGS (UPPER با +)
- یکنواخت‌سازی state_name در قالب UPPER_SNAKE
- حل ارجاعات ID فقط در صورتی که به مقدار معتبر در همان نوع اشاره کنند
- **رفع باگ**: اگر ID به دیتاست دیگری اشاره کند (dat_09_XXXX)، دست‌نخورده باقی می‌ماند
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[ERROR] pip install pyyaml"); sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ID_RE = re.compile(r"^dat_\d{2}_\d{4}$")

def canonical_cmd(s):
    """+CMGS (UPPER با +)"""
    if s is None: return None
    s = str(s).strip()
    if not s: return s
    # اگر ID است، دست نزن
    if ID_RE.match(s): return s
    if len(s) > 2 and s[:3].upper() == "AT+":
        s = s[2:]
    s = re.split(r"[=\s]", s, 1)[0].strip()
    if s and not s.startswith("+") and not s.startswith("AT"):
        s = "+" + s
    return s.upper()

def canonical_state(s):
    """POWER_ON"""
    if s is None: return None
    s = str(s).strip()
    if ID_RE.match(s): return s
    return s.upper().replace("-", "_").replace(" ", "_")

def is_id(s):
    return isinstance(s, str) and bool(ID_RE.match(s))

def load_yaml(p):
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_yaml(p, data):
    with open(p, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False,
                  default_flow_style=False, width=1000)

def build_maps():
    """id → command از dat_01، id → state_name از dat_05 (پشتیبانی از state_id هم)"""
    id_to_cmd = {}
    id_to_state = {}
    for yml in DATA.rglob("*.yaml"):
        try:
            data = load_yaml(yml)
        except Exception:
            continue
        def walk(o):
            if isinstance(o, list):
                for x in o: walk(x)
            elif isinstance(o, dict):
                rid = o.get("id")
                if isinstance(rid, str) and ID_RE.match(rid):
                    if rid.startswith("dat_01_") and o.get("command"):
                        id_to_cmd[rid] = canonical_cmd(o["command"])
                    if rid.startswith("dat_05_"):
                        # پشتیبانی از هر دو فیلد state_name و state_id
                        sn = o.get("state_name") or o.get("state_id")
                        if sn:
                            id_to_state[rid] = canonical_state(sn)
                for v in o.values(): walk(v)
        walk(data)
    return id_to_cmd, id_to_state

def resolve_ref(x, id_map, canonical_fn):
    """اگر x یک ID معتبر در map باشد، مقدار real را برگردان. وگرنه canonical کن."""
    if not isinstance(x, str) or not x.strip():
        return x
    x = x.strip()
    if is_id(x):
        if x in id_map:
            return id_map[x]
        # اگر ID متعلق به دیتاست دیگری است که در map نیست، دست نزن
        ds = x.split("_")[1]
        # ID برای command (dat_01) یا state (dat_05)
        if ds in ("01", "05"):
            # نمی‌توانیم resolve کنیم، دست نزن
            return x
        # اگر ID برای دیتاست دیگری (مثل dat_09) است، دست نزن
        return x
    return canonical_fn(x)

def process_record(r, id_to_cmd, id_to_state):
    changes = 0
    # command (فقط یکنواخت‌سازی، نه ID)
    if isinstance(r.get("command"), str) and r["command"] and not is_id(r["command"]):
        old = r["command"]; new = canonical_cmd(old)
        if new != old: r["command"] = new; changes += 1
    # related_command (single)
    if isinstance(r.get("related_command"), str) and r["related_command"]:
        old = r["related_command"]
        new = resolve_ref(old, id_to_cmd, canonical_cmd)
        if new != old: r["related_command"] = new; changes += 1
    # related_commands (list)
    if isinstance(r.get("related_commands"), list):
        new = [resolve_ref(x, id_to_cmd, canonical_cmd) for x in r["related_commands"]]
        if new != r["related_commands"]: r["related_commands"] = new; changes += 1
    # supported_commands (list)
    if isinstance(r.get("supported_commands"), list):
        new = [resolve_ref(x, id_to_cmd, canonical_cmd) for x in r["supported_commands"]]
        if new != r["supported_commands"]: r["supported_commands"] = new; changes += 1
    # unsupported_commands (list)
    if isinstance(r.get("unsupported_commands"), list):
        new = [resolve_ref(x, id_to_cmd, canonical_cmd) for x in r["unsupported_commands"]]
        if new != r["unsupported_commands"]: r["unsupported_commands"] = new; changes += 1
    # related_state (single)
    if isinstance(r.get("related_state"), str) and r["related_state"]:
        old = r["related_state"]
        new = resolve_ref(old, id_to_state, canonical_state)
        if new != old: r["related_state"] = new; changes += 1
    # related_states (list)
    if isinstance(r.get("related_states"), list):
        new = [resolve_ref(x, id_to_state, canonical_state) for x in r["related_states"]]
        if new != r["related_states"]: r["related_states"] = new; changes += 1
    return changes

def process_file(p, id_to_cmd, id_to_state):
    try:
        data = load_yaml(p)
    except Exception as e:
        return 0
    if not isinstance(data, dict): return 0
    records = data.get("records")
    if not isinstance(records, list): return 0
    total = 0
    for r in records:
        if isinstance(r, dict):
            total += process_record(r, id_to_cmd, id_to_state)
    if total > 0:
        save_yaml(p, data)
    return total

def main():
    print("=== NORMALIZE CROSS-REF (v2) ===")
    id_to_cmd, id_to_state = build_maps()
    print(f"id_to_cmd: {len(id_to_cmd)} entries")
    print(f"id_to_state: {len(id_to_state)} entries")

    total_changes = 0
    total_files = 0
    for yml in DATA.rglob("*.yaml"):
        n = process_file(yml, id_to_cmd, id_to_state)
        if n > 0:
            print(f"  [{n:4d} changes] {yml.relative_to(ROOT)}")
            total_changes += n
            total_files += 1
    print(f"\nمجموع: {total_changes} تغییر در {total_files} فایل")
    print("=== DONE ===")

if __name__ == "__main__":
    main()
