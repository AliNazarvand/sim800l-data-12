# CROSSREF_35_REAL

dat_01 normalized commands: 334
Total remaining issues: 35
Distinct missing normalized commands: 26

## Issues grouped by dataset

### dat_10 (3 issues)

- `dat_10_0004` : raw=`AT+CGCONTRDP`  norm=`CGCONTRDP`
- `dat_10_0017` : raw=`AT+CIPDDREM`  norm=`CIPDDREM`
- `dat_10_0023` : raw=`AT+CEREG`  norm=`CEREG`

### dat_11 (19 issues)

- `dat_11_0007` : raw=`AT+HTTPHEAD`  norm=`HTTPHEAD`
- `dat_11_0009` : raw=`AT+HTTPURL`  norm=`HTTPURL`
- `dat_11_0010` : raw=`AT+HTTPSSL`  norm=`HTTPSSL`
- `dat_11_0011` : raw=`AT+FTPOPEN`  norm=`FTPOPEN`
- `dat_11_0012` : raw=`AT+FTPCLOSE`  norm=`FTPCLOSE`
- `dat_11_0019` : raw=`AT+FTPFLST`  norm=`FTPFLST`
- `dat_11_0020` : raw=`AT+FTPUSER`  norm=`FTPUSER`
- `dat_11_0021` : raw=`AT+FTPPASS`  norm=`FTPPASS`
- `dat_11_0022` : raw=`AT+FTPCWD`  norm=`FTPCWD`
- `dat_11_0023` : raw=`AT+FTPPWD`  norm=`FTPPWD`
- `dat_11_0030` : raw=`AT+SSLCFG`  norm=`SSLCFG`
- `dat_11_0031` : raw=`AT+SSLCONF`  norm=`SSLCONF`
- `dat_11_0032` : raw=`AT+SSLOPEN`  norm=`SSLOPEN`
- `dat_11_0033` : raw=`AT+SSLSEND`  norm=`SSLSEND`
- `dat_11_0034` : raw=`AT+SSLRECV`  norm=`SSLRECV`
- `dat_11_0035` : raw=`AT+SSLCLOSE`  norm=`SSLCLOSE`
- `dat_11_0036` : raw=`AT+SSLSETCERT`  norm=`SSLSETCERT`
- `dat_11_0037` : raw=`AT+SSLSETKEY`  norm=`SSLSETKEY`
- `dat_11_0038` : raw=`AT+SSLSETCA`  norm=`SSLSETCA`

### dat_12 (4 issues)

- `dat_12_0006` : raw=`AT+CATONE`  norm=`CATONE`
- `dat_12_0007` : raw=`AT+CADTONE`  norm=`CADTONE`
- `dat_12_0008` : raw=`AT+CLDTONE`  norm=`CLDTONE`
- `dat_12_0012` : raw=`AT+CPCMREG`  norm=`CPCMREG`

### dat_17 (9 issues)

- `dat_17_0001` : raw=`AT+SSLCFG`  norm=`SSLCFG`
- `dat_17_0002` : raw=`AT+SSLCONF`  norm=`SSLCONF`
- `dat_17_0003` : raw=`AT+SSLOPEN`  norm=`SSLOPEN`
- `dat_17_0004` : raw=`AT+SSLSEND`  norm=`SSLSEND`
- `dat_17_0005` : raw=`AT+SSLRECV`  norm=`SSLRECV`
- `dat_17_0006` : raw=`AT+SSLCLOSE`  norm=`SSLCLOSE`
- `dat_17_0007` : raw=`AT+SSLSETCERT`  norm=`SSLSETCERT`
- `dat_17_0008` : raw=`AT+SSLSETKEY`  norm=`SSLSETKEY`
- `dat_17_0009` : raw=`AT+SSLSETCA`  norm=`SSLSETCA`

## Distinct missing commands (normalized)

| # | Normalized | Count | In dat_01 with other raw? |
|---|-----------|-------|---------------------------|
| 1 | CADTONE | 1 | — |
| 2 | CATONE | 1 | — |
| 3 | CEREG | 1 | — |
| 4 | CGCONTRDP | 1 | — |
| 5 | CIPDDREM | 1 | — |
| 6 | CLDTONE | 1 | — |
| 7 | CPCMREG | 1 | — |
| 8 | FTPCLOSE | 1 | — |
| 9 | FTPCWD | 1 | — |
| 10 | FTPFLST | 1 | — |
| 11 | FTPOPEN | 1 | — |
| 12 | FTPPASS | 1 | — |
| 13 | FTPPWD | 1 | — |
| 14 | FTPUSER | 1 | — |
| 15 | HTTPHEAD | 1 | — |
| 16 | HTTPSSL | 1 | — |
| 17 | HTTPURL | 1 | — |
| 18 | SSLCFG | 2 | — |
| 19 | SSLCLOSE | 2 | — |
| 20 | SSLCONF | 2 | — |
| 21 | SSLOPEN | 2 | — |
| 22 | SSLRECV | 2 | — |
| 23 | SSLSEND | 2 | — |
| 24 | SSLSETCA | 2 | — |
| 25 | SSLSETCERT | 2 | — |
| 26 | SSLSETKEY | 2 | — |

## Interpretation

- 'In dat_01 with other raw?' = whether dat_01 stores the same
  command under a different raw form (e.g. '+X' vs 'AT+X').
  If this column is '—', the command is truly absent from dat_01.
  If it is non-'—', the command exists but the comparison form differs.
- After normalization, all issues above are truly missing from dat_01,
  by definition. This column only shows if a *raw* match exists.