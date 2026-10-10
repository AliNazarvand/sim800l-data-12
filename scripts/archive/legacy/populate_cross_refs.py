#!/usr/bin/env python3
"""
populate_cross_refs.py v2 — پرکردن related_* (دوطرفه) برای dat_01/02/04/05/06.

تغییرات v2:
  * mapping صریح POWER_ON → POWER_ON_PWRKEY_PRESSED
  * step_number → state برای init
  * URC → commands/states
  * دوطرفه: at_commands هم related_states/related_urcs می‌گیرد
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

try:
    import yaml as _yaml
except ImportError:
    print("[FATAL] PyYAML not installed")
    sys.exit(2)


def load(p):
    return _yaml.safe_load(p.read_text(encoding="utf-8"))


def dump(p, obj):
    p.write_text(_yaml.safe_dump(obj, allow_unicode=True, sort_keys=False),
                 encoding="utf-8")


def records_of(path):
    obj = load(path)
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        for _k, v in obj.items():
            if isinstance(v, list):
                return v
    return []


def build_index():
    idx = {"cmd_by_name": {}, "cmd_by_id": {}, "state_by_name": {},
           "state_by_id": {}, "urc_by_code": {}}
    at = DATA / "at_commands" / "at_commands.yaml"
    if at.exists():
        for rec in records_of(at):
            n = rec.get("command"); rid = rec.get("id")
            if n: idx["cmd_by_name"].setdefault(n, rid)
            if rid: idx["cmd_by_id"][rid] = n
    sm = DATA / "state_machine" / "states.yaml"
    if sm.exists():
        for rec in records_of(sm):
            s = rec.get("state_id"); rid = rec.get("id")
            if s: idx["state_by_name"].setdefault(s, rid)
            if rid: idx["state_by_id"][rid] = s
    for uf in ("urc_hw.yaml", "urc_at.yaml"):
        p = DATA / "urc" / uf
        if p.exists():
            for rec in records_of(p):
                c = rec.get("urc_code"); rid = rec.get("id")
                if c: idx["urc_by_code"].setdefault(c, rid)
    return idx


def add_unique(rec, key, values):
    values = [v for v in values if v]
    if not values:
        return False
    cur = rec.get(key)
    if not isinstance(cur, list):
        cur = []
    changed = False
    for v in values:
        if v not in cur:
            cur.append(v)
            changed = True
    if changed:
        rec[key] = cur
    return changed


PIN_TO_CMD = {
    "PWRKEY": ["AT+CPOWD", "AT+CFUN"],
    "RESET": [],
    "DTR": ["AT+CSCLK"],
    "RXD": ["AT+CSCLK"],
    "RI": [],
    "SIM_DET": ["AT+CSDT"],
    "RF_SYNC": ["AT+SJDR"],
    "VBAT": ["AT+CBC"],
}
PIN_TO_STATE = {
    "PWRKEY": ["POWER_OFF", "POWER_ON_PWRKEY_PRESSED",
               "POWER_DOWN_PWRKEY_PRESSED"],
    "RESET": ["RESET_ACTIVE"],
    "DTR": ["SLEEP_MODE_1"],
    "RXD": ["SLEEP_MODE_2"],
    "STATUS": ["POWER_ON_RDY_RECEIVED", "POWER_OFF"],
}
STEP_TO_STATE = {
    1: "POWER_OFF",
    2: "POWER_ON_PWRKEY_PRESSED",
    3: "POWER_ON_PWRKEY_PRESSED",
    4: "POWER_ON_RDY_RECEIVED",
    5: "POWER_ON_RDY_RECEIVED",
}
URC_TO_CMD = {
    "RDY": ["AT+IPR"],
    "NORMAL POWER DOWN": ["AT+CPOWD"],
    "UNDER-VOLTAGE WARNNING": ["AT+CBC"],
    "OVER-VOLTAGE WARNNING": ["AT+CBC"],
    "UNDER-VOLTAGE POWER DOWN": ["AT+CBC"],
    "OVER-VOLTAGE POWER DOWN": ["AT+CBC"],
    "+CMTE: 1": ["AT+CMTE"],
    "+CMTE: -1": ["AT+CMTE"],
    "+CMTE: 2": ["AT+CMTE"],
    "+CMTE: -2": ["AT+CMTE"],
    "+CFUN: 1": ["AT+CFUN", "AT+IPR"],
    "+CPIN: READY": [],
}
URC_TO_STATE = {
    "RDY": ["POWER_ON_RDY_RECEIVED"],
    "NORMAL POWER DOWN": ["POWER_OFF"],
    "UNDER-VOLTAGE POWER DOWN": ["POWER_OFF"],
    "OVER-VOLTAGE POWER DOWN": ["POWER_OFF"],
    "+CPIN: READY": ["POWER_ON_RDY_RECEIVED"],
}


def process_timing(idx):
    f = DATA / "timing" / "timing.yaml"
    if not f.exists(): return 0
    obj = load(f); recs = obj.get("records", obj) if isinstance(obj, dict) else obj
    n = 0
    for rec in recs:
        pin = rec.get("related_pin") or ""
        pins = [p.strip() for p in pin.split(",")]
        cmds, states = [], []
        for p in pins:
            cmds += PIN_TO_CMD.get(p, [])
            states += PIN_TO_STATE.get(p, [])
        ids_c = [idx["cmd_by_name"].get(c) for c in cmds]
        ids_s = [idx["state_by_name"].get(s) for s in states]
        if add_unique(rec, "related_commands", ids_c): n += 1
        if add_unique(rec, "related_states", ids_s): n += 1
    if n:
        dump(f, {"records": recs} if isinstance(obj, dict) else recs)
        print(f"[OK]   {f.relative_to(ROOT)}: {n} fields updated")
    return n


def process_states(idx):
    f = DATA / "state_machine" / "states.yaml"
    if not f.exists(): return 0
    obj = load(f); recs = obj.get("records", obj) if isinstance(obj, dict) else obj
    n = 0
    for rec in recs:
        pins = rec.get("related_pins") or []
        cmds = []
        for p in pins:
            cmds += PIN_TO_CMD.get(p, [])
        ids_c = [idx["cmd_by_name"].get(c) for c in cmds]
        if add_unique(rec, "related_commands", ids_c): n += 1
    if n:
        dump(f, {"records": recs} if isinstance(obj, dict) else recs)
        print(f"[OK]   {f.relative_to(ROOT)}: {n} fields updated")
    return n


def process_init(idx):
    f = DATA / "init_sequence" / "hardware_init.yaml"
    if not f.exists(): return 0
    obj = load(f); recs = obj.get("records", obj) if isinstance(obj, dict) else obj
    n = 0
    for rec in recs:
        sn = rec.get("step_number")
        st_name = STEP_TO_STATE.get(sn)
        if not st_name: continue
        sid = idx["state_by_name"].get(st_name)
        if sid and add_unique(rec, "related_states", [sid]): n += 1
    if n:
        dump(f, {"records": recs} if isinstance(obj, dict) else recs)
        print(f"[OK]   {f.relative_to(ROOT)}: {n} fields updated")
    return n


def process_urcs(idx):
    total = 0
    for uf in ("urc_hw.yaml", "urc_at.yaml"):
        f = DATA / "urc" / uf
        if not f.exists(): continue
        obj = load(f); recs = obj.get("records", obj) if isinstance(obj, dict) else obj
        n = 0
        for rec in recs:
            code = rec.get("urc_code") or ""
            cmds = URC_TO_CMD.get(code, [])
            states = URC_TO_STATE.get(code, [])
            ids_c = [idx["cmd_by_name"].get(c) for c in cmds]
            ids_s = [idx["state_by_name"].get(s) for s in states]
            if add_unique(rec, "related_commands", ids_c): n += 1
            if add_unique(rec, "related_states", ids_s): n += 1
        if n:
            dump(f, {"records": recs} if isinstance(obj, dict) else recs)
            print(f"[OK]   {f.relative_to(ROOT)}: {n} fields updated")
            total += n
    return total


def process_commands_reverse(idx):
    """دوطرفه: at_commands → related_states/related_urcs بر اساس reverse-index."""
    f = DATA / "at_commands" / "at_commands.yaml"
    if not f.exists(): return 0
    obj = load(f); recs = obj.get("records", obj) if isinstance(obj, dict) else obj

    # reverse از timing/states/urcs
    cmd_to_states = {}
    cmd_to_urcs = {}

    for tf in ("timing.yaml",):
        p = DATA / "timing" / tf
        if p.exists():
            for rec in records_of(p):
                for cid in (rec.get("related_commands") or []):
                    for sid in (rec.get("related_states") or []):
                        cmd_to_states.setdefault(cid, set()).add(sid)
    for sf in ("states.yaml",):
        p = DATA / "state_machine" / sf
        if p.exists():
            for rec in records_of(p):
                sid = rec.get("id")
                for cid in (rec.get("related_commands") or []):
                    if sid:
                        cmd_to_states.setdefault(cid, set()).add(sid)
    for uf in ("urc_hw.yaml", "urc_at.yaml"):
        p = DATA / "urc" / uf
        if p.exists():
            for rec in records_of(p):
                uid = rec.get("id")
                for cid in (rec.get("related_commands") or []):
                    if uid:
                        cmd_to_urcs.setdefault(cid, set()).add(uid)

    n = 0
    for rec in recs:
        rid = rec.get("id")
        if not rid: continue
        st_ids = sorted(cmd_to_states.get(rid, []))
        urc_ids = sorted(cmd_to_urcs.get(rid, []))
        if add_unique(rec, "related_states", st_ids): n += 1
        if add_unique(rec, "related_urcs", urc_ids): n += 1
    if n:
        dump(f, {"records": recs} if isinstance(obj, dict) else recs)
        print(f"[OK]   {f.relative_to(ROOT)}: {n} fields updated")
    return n


def main() -> int:
    idx = build_index()
    total = 0
    total += process_timing(idx)
    total += process_states(idx)
    total += process_init(idx)
    total += process_urcs(idx)
    total += process_commands_reverse(idx)
    print(f"[OK]   populate_cross_refs.py v2 done ({total} field updates)")
    return 0


if __name__ == "__main__":
    sys.exit(main())