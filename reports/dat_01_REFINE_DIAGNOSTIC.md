# dat_01_REFINE_DIAGNOSTIC

تاریخ: 2026-10-10T20:33:06Z
منبع: `reports/dat_01_REFINE.json`

## خلاصه

- مجموع A+B بررسی‌شده: **41**
- **weak_at_signal**: 18
- **likely_valid_colon**: 13
- **likely_valid_table**: 9
- **confirmed_noise**: 1

## معنا verdictها و اقدام پیشنهادی

| verdict | معنا | اقدام |
|---|---|---|
| `confirmed_noise` | هیچ اثری در manual یا table نیست | **حذف مطمئن** |
| `confirmed_parameter` | فقط به‌عنوان پارامتر `<CMD>` آمده | **حذف مطمئن** |
| `likely_valid_table` | فقط در جدول‌های استخراج‌شده هست | **نگه‌داشتن** (نقص classifier قبلی) |
| `likely_valid_colon` | به‌شکل `+CMD:` در متن هست | **نگه‌داشتن** |
| `likely_valid_text` | به‌شکل `+CMD` ≥۳ بار آمده | **نگه‌داشتن** |
| `weak_at_signal` | ۱-۲ بار `+CMD` آمده | **بازبینی دستی** |

## جدول کامل (sorted by verdict)

| command | id | orig_cat | verdict | manual_at | manual_colon | manual_param | tsv | raw |
|---|---|---|---|---|---|---|---|---|
| +CGSM | dat_01_0280 | B | confirmed_noise | 0 | 0 | 0 | - | - |
| +CBUZZER | dat_01_0298 | B | weak_at_signal | 2 | 0 | 0 | - | - |
| +CEXTERN | dat_01_0299 | B | weak_at_signal | 2 | 0 | 0 | - | - |
| +CEXTERNT | dat_01_0300 | B | weak_at_signal | 1 | 0 | 0 | - | - |
| +CIPSTATU | dat_01_0304 | B | weak_at_signal | 1 | 0 | 0 | - | - |
| +CMMSDELFI | dat_01_0326 | B | weak_at_signal | 2 | 0 | 0 | - | - |
| +CMMSRDPUS | dat_01_0329 | B | weak_at_signal | 2 | 0 | 0 | - | - |
| +CMMSSENDCF | dat_01_0334 | B | weak_at_signal | 1 | 0 | 0 | - | - |
| +CMMSSTATU | dat_01_0332 | B | weak_at_signal | 2 | 0 | 0 | - | - |
| +CNETLIGH | dat_01_0301 | B | weak_at_signal | 1 | 0 | 0 | - | - |
| +FTPMOD | dat_01_0316 | B | weak_at_signal | 2 | 0 | 0 | - | - |
| +FTSIZE | dat_01_0323 | B | weak_at_signal | 1 | 0 | 0 | - | - |
| +HTTPACTI | dat_01_0312 | B | weak_at_signal | 2 | 0 | 0 | - | - |
| +HTTPACTIO | dat_01_0333 | B | weak_at_signal | 1 | 0 | 0 | - | - |
| +HTTPSCON | dat_01_0314 | B | weak_at_signal | 2 | 0 | 0 | - | - |
| +HTTPSTAT | dat_01_0315 | B | weak_at_signal | 2 | 0 | 0 | - | - |
| +HTTPTER | dat_01_0311 | B | weak_at_signal | 2 | 0 | 0 | - | - |
| +STKENV | dat_01_0292 | B | weak_at_signal | 1 | 0 | 0 | - | - |
| +STKTR | dat_01_0291 | B | weak_at_signal | 1 | 0 | 0 | - | - |
| +CALV | dat_01_0293 | B | likely_valid_colon | 0 | 1 | 0 | - | - |
| +CBPF | dat_01_0282 | B | likely_valid_colon | 0 | 1 | 0 | - | - |
| +CDS | dat_01_0290 | B | likely_valid_colon | 0 | 6 | 0 | - | - |
| +CMT | dat_01_0288 | B | likely_valid_colon | 0 | 6 | 0 | - | - |
| +CMTI | dat_01_0287 | B | likely_valid_colon | 0 | 9 | 0 | - | - |
| +CRING | dat_01_0281 | B | likely_valid_colon | 0 | 3 | 0 | - | - |
| +CSQN | dat_01_0296 | B | likely_valid_colon | 0 | 2 | 0 | - | - |
| +CSSI | dat_01_0284 | B | likely_valid_colon | 0 | 2 | 0 | - | - |
| +CSSU | dat_01_0285 | B | likely_valid_colon | 0 | 2 | 0 | - | - |
| +CTZV | dat_01_0294 | B | likely_valid_colon | 0 | 2 | 0 | - | - |
| +FTPTIMEOUT | dat_01_0322 | B | likely_valid_colon | 0 | 1 | 0 | - | - |
| +GID | dat_01_0295 | B | likely_valid_colon | 0 | 1 | 0 | - | - |
| +POP3REST | dat_01_0324 | B | likely_valid_colon | 0 | 1 | 0 | - | - |
| +CBM | dat_01_0289 | B | likely_valid_table | 0 | 6 | 0 | - | ✓ |
| +CCWV | dat_01_0283 | B | likely_valid_table | 0 | 0 | 0 | ✓ | ✓ |
| +CME | dat_01_0277 | B | likely_valid_table | 1 | 0 | 0 | - | ✓ |
| +CMS | dat_01_0286 | B | likely_valid_table | 0 | 0 | 0 | - | ✓ |
| +DTMF | dat_01_0335 | A | likely_valid_table | 0 | 24 | 9 | ✓ | ✓ |
| +IPD | dat_01_0305 | B | likely_valid_table | 0 | 0 | 0 | ✓ | ✓ |
| +PDP | dat_01_0303 | B | likely_valid_table | 0 | 3 | 0 | ✓ | ✓ |
| +RECEIVE | dat_01_0306 | B | likely_valid_table | 0 | 0 | 0 | ✓ | ✓ |
| +RECV | dat_01_0308 | A | likely_valid_table | 0 | 0 | 4 | ✓ | ✓ |

## نمونه‌های هر verdict (تا ۵ مورد)

### `confirmed_noise` — 1 رکورد

- **+CGSM** (`dat_01_0280`, orig=B)
  > nse Command TA reports a list of additional capabilities. AT+GCAP +GCAP: list of supported <name>s SIM800 Series_AT Command Manual_V1.01 40 2013-07-23 Smart Machine Smart Decision 

### `weak_at_signal` — 18 رکورد

- **+CBUZZER** (`dat_01_0298`, orig=B)
  > er_on>,<timer_off> 1,64,800 2,64,3000 3,64,300 6.2.49 AT+CBUZZERRING Use the Buzzer Sound as the Incoming Call Ring AT+CBUZZERRING Use the Buzzer Sound as the Incoming Call Ring Re
- **+CEXTERN** (`dat_01_0299`, orig=B)
  > SIM800 Series_AT Command Manual_V1.01 164 2013-07-23 Smart Machine Smart Decision 6.2.50 AT+CEXTERNTONE Close or Open the Microphone AT+CEXTERNTONE Close or Open the Microphone Tes
- **+CEXTERNT** (`dat_01_0300`, orig=B)
  > Command Response AT+CEXTERN +CEXTERNTONE: (0,1) TONE=? OK Parameter See Write Command Read Command Response AT+CEXTERN +CEXTERNTONE: <mode> TONE? OK Parameter See Write Command Wri
- **+CIPSTATU** (`dat_01_0304`, orig=B)
  > ent Connection Status Test Command Response AT+CIPSTATUS OK =? Write Command Response If multi IP +CIPSTATUS: <n>,<bearer>, <TCP/UDP>, <IP address>, <port>, connection mode <client
- **+CMMSDELFI** (`dat_01_0326`, orig=B)
  > nd only ASCII code is recognized for <name>. 15.2.7 AT+CMMSDELFILE Delete the file of the edited MMS by file index AT+CMMSDELFILE Delete the file of the edited MMS by file index Te

### `likely_valid_colon` — 13 رکورد

- **+CALV** (`dat_01_0293`, orig=B)
  > s See Write Command Write Command Response AT+CALA= OK <time>[,<n> If error is related to ME functionality: [,<recurr>]] +CME ERROR: <err> Unsolicited Result Code Indicate the inde
- **+CBPF** (`dat_01_0282`, orig=B)
  > A returns phone book entries (from the current phone book memory text>] storage selected with +CPBS) which contains alphanumeric string <findtext>. [+CPBF:<index1>,<number>,<type>,
- **+CDS** (`dat_01_0290`, orig=B)
  > or +CBM: <sn>,<mid>,<dcs>,<page>,<pages><CR><LF><data> (text mode enabled). <ds> 0 No SMS-STATUS-REPORTs are routed to the TE. 1 SMS-STATUS-REPORTs are routed to the TE using unsol
- **+CMT** (`dat_01_0288`, orig=B)
  > indication of the memory location is routed to the TE using unsolicited result code: +CMTI: <mem>,<index> 2 SMS-DELIVERs (except class 2) are routed directly to the TE using unsoli
- **+CMTI** (`dat_01_0287`, orig=B)
  > setting and this value): 0 No SMS-DELIVER indications are routed to the TE. 1 If SMS-DELIVER is stored into ME/TA, indication of the memory location is routed to the TE using unsol

### `likely_valid_table` — 9 رکورد

- **+CBM** (`dat_01_0289`, orig=B)
  > ): 0 No CBM indications are routed to the TE. SIM800 Series_AT Command Manual_V1.01 113 2013-07-23 Smart Machine Smart Decision 2 New CBMs are routed directly to the TE using unsol
- **+CCWV** (`dat_01_0283`, orig=B)
  > AT+CCWE=<m OK ode> If error is related to ME functionality: +CME ERROR: <err> Parameter <mode> 0 Disable call meter warning event 1 Enable call meter warning event Unsolicited resu
- **+CME** (`dat_01_0277`, orig=B)
  > y by receiving an ATH Command or a character during execution. The aborting is not possible during some states of connection establishment such as handshaking. If error is related 
- **+CMS** (`dat_01_0286`, orig=B)
  > preferred message storage <mem1> location dex>[,<delflag>] <index>. OK SIM800 Series_AT Command Manual_V1.01 101 2013-07-23 Smart Machine Smart Decision ERROR If error is related t
- **+DTMF** (`dat_01_0335`, orig=A)
  > T+DDET=1 OK Set up a call connection ATD***********; OK If module detected DTMF, URC will be reported via serial port SIM800 Series_AT Command Manual_V1.01 308 2013-07-23 Smart Mac

## یادداشت

- این گزارش هیچ داده‌ای را از `data/dat_01_at_command.yaml` تغییر نداده است.
- برای اعمال حذف، از verdictهای `confirmed_noise` و `confirmed_parameter` استفاده شود.
- `weak_at_signal` را دستی بازبینی کنید.