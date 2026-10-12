import re, sys, yaml
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
PAGED = ROOT / "sources" / "extracted" / "at_manual_v1_01_paged.txt"
DAT01 = ROOT / "data" / "dat_01_at_command.yaml"

def load_pages(p):
    txt = p.read_text(encoding="utf-8")
    pages, cur, buf = {}, None, []
    for ln in txt.splitlines():
        m = re.match(r"^<<<PAGE (\d+)>>>\s*$", ln)
        if m:
            if cur is not None:
                pages[cur] = "\n".join(buf)
            cur = int(m.group(1)); buf = []
        else:
            buf.append(ln)
    if cur is not None:
        pages[cur] = "\n".join(buf)
    return pages

def find_block(pages, cmd):
    pat = re.compile(r"^\s*\d+\.\d+[\d.]*\s+" + re.escape(cmd) + r"\b", re.M)
    for pg in sorted(pages):
        m = pat.search(pages[pg])
        if m:
            return pg, pages[pg][m.start():]
    return None, None

def parse_params(block):
    out = []
    for ln in block.splitlines():
        m = re.match(r"^\s*<([a-zA-Z_]\w*)>\s*(.*)$", ln)
        if m:
            n = m.group(1); d = m.group(2).strip()[:160]
            if not any(p["name"] == n for p in out):
                out.append({"name": n, "type": "unknown", "description": d})
    return out

def parse_resp(block):
    m = re.search(r"(?i)\n\s*response[s]?\s*\n((?:[^\n]+\n){1,12})", block)
    if not m:
        m = re.search(r"(?i)response[^\n]*\n((?:[^\n]+\n){1,12})", block)
    if m:
        for ln in m.group(1).splitlines():
            s = ln.strip()
            if s and (s.startswith("+") or s == "OK" or s == "ERROR"):
                return s[:220]
    return None

def parse_ex(block):
    out = []
    m = re.search(r"(?i)\n\s*example[s]?\s*\n((?:[^\n]+\n){1,15})", block)
    if not m:
        m = re.search(r"(?i)example[s]?[^\n]*\n((?:[^\n]+\n){1,15})", block)
    if m:
        for ln in m.group(1).splitlines():
            s = ln.strip()
            if s.startswith("AT+"):
                out.append(s)
                if len(out) >= 2:
                    break
    return out

def main():
    if not PAGED.exists():
        print("FAILED: paged text not found: " + str(PAGED))
        return 1
    pages = load_pages(PAGED)
    print("Loaded " + str(len(pages)) + " pages")
    data = yaml.safe_load(DAT01.read_text(encoding="utf-8"))
    updated = 0; considered = 0
    for rec in data:
        if rec.get("status") == "complete":
            continue
        cmd = (rec.get("command") or "").strip()
        if not cmd.startswith("+"):
            continue
        considered += 1
        pg, blk = find_block(pages, "AT" + cmd)
        if blk is None:
            continue
        prm = parse_params(blk); rsp = parse_resp(blk); exs = parse_ex(blk)
        if prm and (rsp or exs):
            rec["parameters"] = prm
            if rsp: rec["response_success"] = rsp
            if exs: rec["examples"] = exs
            rec["status"] = "complete"
            rec["confidence"] = 0.85
            rec["source"] = rec.get("source") or {}
            rec["source"]["page"] = rec["source"].get("page") or str(pg)
            updated += 1
    DAT01.write_text(yaml.safe_dump(data, allow_unicode=True,
        sort_keys=False, default_flow_style=False, width=4096), encoding="utf-8")
    print("Considered " + str(considered) + " partial records")
    print("Updated " + str(updated) + " records to complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())
