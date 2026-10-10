#!/usr/bin/env python3
"""
populate_cross_refs_v3.py — گسترش cross-ref به dat_07، 12، 13، 15.

dat_07 (Hardware) → related به dat_13 (SIM pins) و dat_16 (Board)
dat_12 (Audio)    → related به dat_07 (audio pins)
dat_13 (SIM Mgmt) → related به dat_07 (SIM pins)
dat_15 (Power)    → related به dat_05 (States) و dat_01 (CFUN/CSCLK)

فقط فیلدهای related_* را پر می‌کند، نه re-write کل رکورد.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

try:
    import yaml as _yaml
except ImportError:
    print("[FATAL] PyYAML not installed"); sys.exit(2)


def load(p): return _yaml.safe_load(p.read_text(encoding="utf-8"))
def dump(p, obj): p.write_text(_yaml.safe_dump(obj, allow_unicode=True, sort_keys=False), encoding="utf-8")


def records_of(path):
    obj = load(path)
    if isinstance(obj, list): return obj
    if isinstance(obj, dict):
        for _k, v in obj.items():
            if isinstance(v, list): return v
    return []


def add_unique(rec, key, values):
    values = [v for v in values if v]
    if not values: return False
    cur = rec.get(key)
    if not isinstance(cur, list): cur = []
    changed = False
    for v in values:
        if v not in cur:
            cur.append(v); changed = True
    if changed: rec[key] = cur
    return changed


def build_index():
    idx = {"cmd_by_name": {}, "state_by_name": {}}
    at = DATA / "at_commands" / "at_commands.yaml"
    if at.exists():
        for rec in records_of(at):
            n = rec.get("command"); rid = rec.get("id")
            if n and rid: idx["cmd_by_name"].setdefault(n, rid)
    sm = DATA / "state_machine" / "states.yaml"
    if sm.exists():
        for rec in records_of(sm):
            s = rec.get("state_id"); rid = rec.get("id")
            if s and rid: idx["state_by_name"].setdefault(s, rid)
    return idx


def main() -> int:
    idx = build_index()
    total = 0

    # ---- dat_07: هر پین در hardware → related_states و related_commands بر اساس نام پین
    pin_to_cmd = {
        "PWRKEY": ["AT+CPOWD"], "RESET": [],
        "DTR": ["AT+CSCLK"], "RXD": ["AT+CSCLK"],
        "VBAT": ["AT+CBC"], "SIM_VDD": ["AT+CSDT"], "SIM_DET": ["AT+CSDT"],
        "RF_SYNC": ["AT+SJDR"],
    }
    pin_to_state = {
        "PWRKEY": ["POWER_OFF", "POWER_ON_PWRKEY_PRESSED"],
        "RESET": ["RESET_ACTIVE"],
        "DTR": ["SLEEP_MODE_1"], "RXD": ["SLEEP_MODE_2"],
        "STATUS": ["POWER_ON_RDY_RECEIVED"],
    }
    hw = DATA / "hardware" / "pinout.yaml"
    if hw.exists():
        recs = records_of(hw); n = 0
        for rec in recs:
            pn = rec.get("pin_name") or ""
            cmds = pin_to_cmd.get(pn, []); states = pin_to_state.get(pn, [])
            ids_c = [idx["cmd_by_name"].get(c) for c in cmds]
            ids_s = [idx["state_by_name"].get(s) for s in states]
            if add_unique(rec, "related_commands", ids_c): n += 1
            if add_unique(rec, "related_states", ids_s): n += 1
        if n:
            dump(hw, {"records": recs}); total += n
            print(f"[OK]   {hw.relative_to(ROOT)}: {n} updates")

    # ---- dat_12: audio pins → commands (Audio group)
    audio = DATA / "audio" / "audio_hw.yaml"
    if audio.exists():
        recs = records_of(audio); n = 0
        for rec in recs:
            # audio pins → AT+CMIC, AT+CLVL, AT+SIDET
            ids = [idx["cmd_by_name"].get(c) for c in ["AT+CMIC", "AT+CLVL", "AT+SIDET"]]
            if add_unique(rec, "related_commands", ids): n += 1
        if n:
            dump(audio, {"records": recs}); total += n
            print(f"[OK]   {audio.relative_to(ROOT)}: {n} updates")

    # ---- dat_15: power modes → related به states + commands
    pm = DATA / "power_management" / "power_modes.yaml"
    if pm.exists():
        recs = records_of(pm); n = 0
        mode_map = {
            "NORMAL_OPERATION": (["AT+CFUN"], []),
            "SLEEP_MODE_CFUN1": (["AT+CSCLK", "AT+CFUN"], ["SLEEP_MODE_1"]),
            "POWER_DOWN_MODE": (["AT+CPOWD"], ["POWER_OFF"]),
            "MINIMUM_FUNCTIONALITY": (["AT+CFUN"], []),
        }
        for rec in recs:
            mid = rec.get("mode_id")
            cmds, states = mode_map.get(mid, ([], []))
            ids_c = [idx["cmd_by_name"].get(c) for c in cmds]
            ids_s = [idx["state_by_name"].get(s) for s in states]
            if add_unique(rec, "related_commands", ids_c): n += 1
            if add_unique(rec, "related_states", ids_s): n += 1
        if n:
            dump(pm, {"records": recs}); total += n
            print(f"[OK]   {pm.relative_to(ROOT)}: {n} updates")

    # ---- dat_13: SIM pins → related به AT+CSDT
    sm = DATA / "sim_management" / "sim_management_hw.yaml"
    if sm.exists():
        recs = records_of(sm); n = 0
        for rec in recs:
            if rec.get("category") == "pin":
                ids = [idx["cmd_by_name"].get("AT+CSDT")]
                if add_unique(rec, "related_commands", ids): n += 1
        if n:
            dump(sm, {"records": recs}); total += n
            print(f"[OK]   {sm.relative_to(ROOT)}: {n} updates")

    print(f"[OK]   populate_cross_refs_v3.py done ({total} updates)")
    return 0


if __name__ == "__main__":
    sys.exit(main())