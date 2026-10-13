

## 2026-10-13T18:11:10Z — v6-final decisions
- **PowerShell .Count bug**: ( | Where-Object).Count on a single-item result returns the number of keys in the hashtable (9), not 1. Wrapped with @() to force array semantics.
- **dat_01 dedup normalization**: extract_at_commands.py writes commands like +CMGS; _rebuild_B1_dat01.py writes AT+CMGS. Dedup now strips the AT prefix and =... parameter suffix so both collapse to +CMGS.
- **dat_15 dedup key**: 4-field key (category, mode, parameter, command) was too strict. Now uses 2-field key (category, parameter); mode and command serve as fallbacks.
- **Coverage > 100% rule**: coverage of 182% means 610 records against 335 source entries — data quality issue, not completion. Status rule now requires 95 <= coverage <= 100.
- **dat_15 oversize**: If real > 50, mark partial with reason 'oversize'.
