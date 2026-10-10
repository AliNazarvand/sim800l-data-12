# dat_01_REFINE — طبقه‌بندی ۵۹ رکورد only_dat01

تاریخ: 2026-10-10T20:30:54Z
منبع: `sources/extracted/SIM800 Series_AT Command Manual_V1.01.txt`

## خلاصه

- کل رکوردهای only_dat01: **59**
- دسته A (parameter — کاندیدای حذف): **2**
- دسته B (context-mismatch — کاندیدای حذف): **39**
- دسته C (valid-but-not-in-TOC — کاندیدای نگه‌داشتن): **18**

## معیارها

| دسته | معیار | اقدام پیشنهادی |
|---|---|---|
| A | `AT+CMD` در بدنه manual ≤ 2 بار **و** `<CMD>` به‌عنوان پارامتر | حذف |
| B | `AT+CMD` = 0 **و** هیچ placeholder پارامتری هم نبود → context غلط | حذف |
| C | `AT+CMD` در بدنه ≥ 3 بار → احتمالاً command واقعی که از TOC جا افتاده | نگه‌داشتن |

## دسته A — پارامتر (کاندیدای حذف) — 2

| command | id | at_count | param_count |
|---|---|---|---|
| +DTMF | dat_01_0335 | 0 | 14 |
| +RECV | dat_01_0308 | 0 | 4 |

## دسته B — context-mismatch (کاندیدای حذف) — 39

| command | id | at_count | param_count |
|---|---|---|---|
| +CALV | dat_01_0293 | 0 | 0 |
| +CBM | dat_01_0289 | 0 | 0 |
| +CBPF | dat_01_0282 | 0 | 0 |
| +CBUZZER | dat_01_0298 | 2 | 0 |
| +CCWV | dat_01_0283 | 0 | 0 |
| +CDS | dat_01_0290 | 0 | 0 |
| +CEXTERN | dat_01_0299 | 2 | 0 |
| +CEXTERNT | dat_01_0300 | 1 | 0 |
| +CGSM | dat_01_0280 | 0 | 0 |
| +CIPSTATU | dat_01_0304 | 1 | 0 |
| +CME | dat_01_0277 | 0 | 0 |
| +CMMSDELFI | dat_01_0326 | 2 | 0 |
| +CMMSRDPUS | dat_01_0329 | 2 | 0 |
| +CMMSSENDCF | dat_01_0334 | 1 | 0 |
| +CMMSSTATU | dat_01_0332 | 2 | 0 |
| +CMS | dat_01_0286 | 0 | 0 |
| +CMT | dat_01_0288 | 0 | 0 |
| +CMTI | dat_01_0287 | 0 | 0 |
| +CNETLIGH | dat_01_0301 | 1 | 0 |
| +CRING | dat_01_0281 | 0 | 0 |
| +CSQN | dat_01_0296 | 0 | 0 |
| +CSSI | dat_01_0284 | 0 | 0 |
| +CSSU | dat_01_0285 | 0 | 0 |
| +CTZV | dat_01_0294 | 0 | 0 |
| +FTPMOD | dat_01_0316 | 2 | 0 |
| +FTPTIMEOUT | dat_01_0322 | 0 | 0 |
| +FTSIZE | dat_01_0323 | 1 | 0 |
| +GID | dat_01_0295 | 0 | 0 |
| +HTTPACTI | dat_01_0312 | 2 | 0 |
| +HTTPACTIO | dat_01_0333 | 1 | 0 |
| +HTTPSCON | dat_01_0314 | 2 | 0 |
| +HTTPSTAT | dat_01_0315 | 2 | 0 |
| +HTTPTER | dat_01_0311 | 2 | 0 |
| +IPD | dat_01_0305 | 0 | 0 |
| +PDP | dat_01_0303 | 0 | 0 |
| +POP3REST | dat_01_0324 | 0 | 0 |
| +RECEIVE | dat_01_0306 | 0 | 0 |
| +STKENV | dat_01_0292 | 1 | 0 |
| +STKTR | dat_01_0291 | 1 | 0 |

## دسته C — معتبر اما گم‌شده از TOC (نگه‌داشتن) — 18

| command | id | at_count | param_count |
|---|---|---|---|
| +CEXTBUT | dat_01_0279 | 3 | 0 |
| +CEXTHS | dat_01_0278 | 4 | 0 |
| +CGMSCLA | dat_01_0297 | 3 | 0 |
| +CIPRDTIM | dat_01_0310 | 3 | 0 |
| +CIPSERVE | dat_01_0307 | 3 | 0 |
| +CIPUDPMOD | dat_01_0309 | 5 | 0 |
| +CMMSDELBC | dat_01_0328 | 3 | 0 |
| +CMMSDELRE | dat_01_0327 | 3 | 0 |
| +CMMSPROFI | dat_01_0330 | 3 | 0 |
| +CMMSSENDC | dat_01_0325 | 3 | 0 |
| +CMMSTIMEO | dat_01_0331 | 3 | 0 |
| +CWHITELI | dat_01_0302 | 3 | 0 |
| +FTPGETNA | dat_01_0318 | 3 | 0 |
| +FTPGETPA | dat_01_0319 | 3 | 0 |
| +FTPPUTNA | dat_01_0320 | 3 | 0 |
| +FTPPUTOP | dat_01_0317 | 3 | 0 |
| +FTPPUTPA | dat_01_0321 | 3 | 0 |
| +HTTPREA | dat_01_0313 | 4 | 0 |

## نمونه context (۱۰ مورد اول هر دسته)

### دسته A — نمونه

- **+DTMF** (`dat_01_0335`):
  > T+DDET=1 OK Set up a call connection ATD***********; OK If module detected DTMF, URC will be reported via serial port SIM800 Series_AT Command Manual_V1.01 308 2013-07-23 Smart Machine Smart Decision +DTMF:1 //report DTMF value +DTMF:2 +DTMF:3 +DTMF:4 +DTMF:5 +DTMF:6 +DTMF:7 +DTMF:8 +DTMF:9 +DTMF:0 +DTMF:# +DTMF:* Receive an incoming call ATA OK If module detected DTMF, URC will be reported via se

- **+RECV** (`dat_01_0308`):
  > d port. 0 Do not show the prompt 1 Show the prompt, the format is as follows: 1) For single IP connection (+CIPMUX=0) SIM800 Series_AT Command Manual_V1.01 197 2013-07-23 Smart Machine Smart Decision +RECV FROM:<IP ADDRESS>:<PORT> 1) For multi IP connection (+CIPMUX=1) +RECEIVE,<n>,<data length>,<IP ADDRESS>:<PORT> Reference 8.2.21 AT+CIPDPDP Set Whether to Check State of GPRS Network Timing AT+CI

### دسته B — نمونه

- **+CALV** (`dat_01_0293`):
  > s See Write Command Write Command Response AT+CALA= OK <time>[,<n> If error is related to ME functionality: [,<recurr>]] +CME ERROR: <err> Unsolicited Result Code Indicate the index of expired alarm. +CALV: <n> Parameters <time> A string parameter(string should be included in quotation marks) which indicates the time when alarm arrives. The format is "yy/MM/dd,hh:mm:ss" where characters indicate t

- **+CBM** (`dat_01_0289`):
  > ): 0 No CBM indications are routed to the TE. SIM800 Series_AT Command Manual_V1.01 113 2013-07-23 Smart Machine Smart Decision 2 New CBMs are routed directly to the TE using unsolicited result code: +CBM: <length><CR><LF><pdu> (PDU mode enabled) or +CBM: <sn>,<mid>,<dcs>,<page>,<pages><CR><LF><data> (text mode enabled). <ds> 0 No SMS-STATUS-REPORTs are routed to the TE. 1 SMS-STATUS-REPORTs are r

- **+CBPF** (`dat_01_0282`):
  > A returns phone book entries (from the current phone book memory text>] storage selected with +CPBS) which contains alphanumeric string <findtext>. [+CPBF:<index1>,<number>,<type>,<text>] [[…]<CR><LF>+CBPF:<index2>,<number>,<type>,<text>] OK Parameters <findtext> String type(string should be included in quotation marks) field of maximum length <tlength> in current TE character set specified by +CS

- **+CBUZZER** (`dat_01_0298`):
  > er_on>,<timer_off> 1,64,800 2,64,3000 3,64,300 6.2.49 AT+CBUZZERRING Use the Buzzer Sound as the Incoming Call Ring AT+CBUZZERRING Use the Buzzer Sound as the Incoming Call Ring Read Command Response AT+CBUZZER +CBUZZERRING: <mode> RING? OK Parameter See Write Command Write Command Response AT+CBUZZER OK RING=<mode> ERROR Parameter <mode> 0 disable the function of using buzzer sound as the incomin

- **+CCWV** (`dat_01_0283`):
  > AT+CCWE=<m OK ode> If error is related to ME functionality: +CME ERROR: <err> Parameter <mode> 0 Disable call meter warning event 1 Enable call meter warning event Unsolicited result codes supported: +CCWV Shortly before the ACM (Accumulated Call Meter) maximum value is reached, an unsolicited result code +CCWV will be sent, if enabled by this command. The warning is issued approximately when 5 se

- **+CDS** (`dat_01_0290`):
  > or +CBM: <sn>,<mid>,<dcs>,<page>,<pages><CR><LF><data> (text mode enabled). <ds> 0 No SMS-STATUS-REPORTs are routed to the TE. 1 SMS-STATUS-REPORTs are routed to the TE using unsolicited result code: +CDS: <length><CR><LF><pdu> (PDU mode enabled) or +CDS: <fo>,<mr>[,<ra>][,<tora>],<scts>,<dt>,<st> (text mode enabled) <bfr> 0 TA buffer of unsolicited result codes defined within this Command is flus

- **+CEXTERN** (`dat_01_0299`):
  > SIM800 Series_AT Command Manual_V1.01 164 2013-07-23 Smart Machine Smart Decision 6.2.50 AT+CEXTERNTONE Close or Open the Microphone AT+CEXTERNTONE Close or Open the Microphone Test Command Response AT+CEXTERN +CEXTERNTONE: (0,1) TONE=? OK Parameter See Write Command Read Command Response AT+CEXTERN +CEXTERNTONE: <mode> TONE? OK Parameter See Write Command Write Command Response AT+CEXTERNT OK ONE

- **+CEXTERNT** (`dat_01_0300`):
  > Command Response AT+CEXTERN +CEXTERNTONE: (0,1) TONE=? OK Parameter See Write Command Read Command Response AT+CEXTERN +CEXTERNTONE: <mode> TONE? OK Parameter See Write Command Write Command Response AT+CEXTERNT OK ONE=<mode> ERROR Parameter <mode> 0 re-open the microphone 1 close the microphone Reference Note 6.2.51 AT+CNETLIGHT Close the Net Light or Open It to Shining AT+CNETLIGHT Close the Net

- **+CGSM** (`dat_01_0280`):
  > nse Command TA reports a list of additional capabilities. AT+GCAP +GCAP: list of supported <name>s SIM800 Series_AT Command Manual_V1.01 40 2013-07-23 Smart Machine Smart Decision OK Parameter <name> +CGSM GSM function is supported +FCLASS FAX function is supported Reference Note V.25ter 2.2.34 AT+GMI Request Manufacturer Identification AT+GMI Request Manufacturer Identification Test Command Respo

- **+CIPSTATU** (`dat_01_0304`):
  > ent Connection Status Test Command Response AT+CIPSTATUS OK =? Write Command Response If multi IP +CIPSTATUS: <n>,<bearer>, <TCP/UDP>, <IP address>, <port>, connection mode <client state> (+CIPMUX=1) AT+CIPSTATU OK S=<n> Parameters See Execution Command Execution Response Command 1）If in single connection mode (+CIPMUX=0) AT+CIPSTATUS OK STATE: <state> 2) If in multi-connection mode (+CIPMUX=1) OK

### دسته C — نمونه

- **+CEXTBUT** (`dat_01_0279`):
  > <n> Y AT+CIURC <mode> Y AT+CFGRI <mode> Y AT+CMTE <mode> Y AT+STKPCIS <switch> Y AT+CMGF <mode> Y AT+CNMI <mode>,<mt>,<bm>,<ds>,<bfr> Y AT+CSCS <chest> Y AT+VTD <n> Y AT+CALS <n> Y AT+CEXTHS <mode> Y AT+CEXTBUT <mode> Y AT+CHF <ind> Y AT+CAAS <mode> Y AT+CBUZZERRING <mode> Y AT+DDET <n> Y AT+MORING <mode> Y AT+SVR <voice_rate_coding> Y AT+CCPD <mode> Y AT+CSGS <mode> Y AT+CNETLIGHT <mode> Y AT+SLE

- **+CEXTHS** (`dat_01_0278`):
  > MEE <n> Y AT+CSCLK <n> Y AT+CIURC <mode> Y AT+CFGRI <mode> Y AT+CMTE <mode> Y AT+STKPCIS <switch> Y AT+CMGF <mode> Y AT+CNMI <mode>,<mt>,<bm>,<ds>,<bfr> Y AT+CSCS <chest> Y AT+VTD <n> Y AT+CALS <n> Y AT+CEXTHS <mode> Y AT+CEXTBUT <mode> Y AT+CHF <ind> Y AT+CAAS <mode> Y AT+CBUZZERRING <mode> Y AT+DDET <n> Y AT+MORING <mode> Y AT+SVR <voice_rate_coding> Y AT+CCPD <mode> Y AT+CSGS <mode> Y AT+CNETLI

- **+CGMSCLA** (`dat_01_0297`):
  > +CSQN: <rssi>,<ber>when values change. <mode> 0 Disable 1 Enable 2 Query Reference Note 6.2.36 AT+CGMSCLASS Change GPRS Multislot Class AT+CGMSCLASS Change GPRS Multislot Class Test Command Response AT+CGMSCLA MULTISLOT CLASS: (2,4,8,9,10,12) SS=? OK Parameter See Write Command Read Command Response AT+CGMSCLA MULTISLOT CLASS: <class> SS? OK Parameter See Write Command Write Command Response AT+CG

- **+CIPRDTIM** (`dat_01_0310`):
  > Reference Note 8.2.28 AT+CIPRDTIMER Set Remote Delay Timer AT+CIPRDTIMER Set Remote Delay Timer SIM800 Series_AT Command Manual_V1.01 204 2013-07-23 Smart Machine Smart Decision Test Command Response AT+CIPRDTIM +CIPRDTIMER: (100-4000),(100-7000) ER=? OK Parameter See Write Command Read Command Response AT+CIPRDTIM +CIPRDTIMER: <rdsigtimer>,<rdmuxtimer> ER? OK Parameter See Write Command Write Com

- **+CIPSERVE** (`dat_01_0307`):
  > It neither prompts echo ‘>’ nor shows "send ok" when sending is successful. Reference Note 8.2.18 AT+CIPSERVER Configure Module as Server AT+CIPSERVER Configure Module as Server Test Command Response AT+CIPSERVE +CIPSERVER: (0-CLOSE SERVER, 1-OPEN SERVER),(1-65535) R=? OK Parameters See Write Command SIM800 Series_AT Command Manual_V1.01 195 2013-07-23 Smart Machine Smart Decision Read Command Res

- **+CIPUDPMOD** (`dat_01_0309`):
  > 07-23 Smart Machine Smart Decision Only when +CIPHEAD is set to 1, the setting of this command will work.. 8.2.25 AT+CIPUDPMODE UDP Extended Mode AT+CIPUDPMODE UDP Extended Mode Test Command Response AT+CIPUDPMOD 1) For single IP connection (+CIPMUX=0) E=? +CIPUDPMODE: (0-2),("(0-255).(0-255).(0-255).(0-255)"),(1-65535) OK 2) For multi IP connection (+CIPMUX=1) +CIPUDPMODE: (0-5),(0-2),("(0-255).(

- **+CMMSDELBC** (`dat_01_0328`):
  > T+CMMSDELCC Response OK Reference Note This command is valid when it is allowed to edit MMS 15.2.14 AT+CMMSDELBCC Delete secret recipients AT+CMMSDELBCC Delete secret recipients Test Command Response AT+CMMSDELBC +CMMSDELBCC: "ADDRESS" C=? OK Write Command Response AT+CMMSDELBC OK C=<addr> or ERROR or +CME ERROR: <err> Parameter <addr> a string parameter which indicates phone number or email addre

- **+CMMSDELRE** (`dat_01_0327`):
  > te The maximum of secret recipients is 20 and this command is valid only when it is allowed to edit MMS 15.2.12 AT+CMMSDELRECP Delete recipients AT+CMMSDELRECP Delete recipients Test Command Response AT+CMMSDELRE +CMMSDELRECP: "ADDRESS" CP=? OK Write Command Response AT+CMMSDELRE OK CP=<addr> or ERROR or +CME ERROR: <err> Parameter <addr> a string parameter which indicates phone number or email ad

- **+CMMSPROFI** (`dat_01_0330`):
  > erence Note 15.2.20 AT+CMMSPROFILE Set User Agent Profile AT+CMMSPROFILE Set User Agent Profile SIM800 Series_AT Command Manual_V1.01 273 2013-07-23 Smart Machine Smart Decision Test Command Response AT+CMMSPROFI +CMMSPROFILE: "UserAgentProfile" LE=? OK Parameter See Write Command Read Command Response AT+CMMSPROFI +CMMSPROFILE: <UAProfile> LE? OK Parameter See Write Command Write Command Response

- **+CMMSSENDC** (`dat_01_0325`):
  > s, refer to AT+SAPBR Parameter Saving AT+CMMSSCONT Mode Reference Note 15.2.4 AT+CMMSSENDCFG Set the parameters for sending MMS AT+CMMSSENDCFG Set the parameters for sending MMS Test Command Response AT+CMMSSENDC +CMMSSENDCFG: (0-6), (0-3),(0,1), (0,1),(0-2),(0-4),(1-2),(0,1) FG=? OK Parameter See Write Command Read Command Response AT+CMMSSENDC +CMMSSENDCFG: FG? <valid>,<pri>,<sendrep>,<readrep>,

## یادداشت

- این گزارش هیچ داده‌ای را از `data/dat_01_at_command.yaml` حذف نکرده است.
- برای اعمال حذف، باید یک اسکریپت جداگانه با تأیید صریح مالک پروژه اجرا شود.
- توصیه: قبل از حذف، دسته A و B دستی sample review شوند.