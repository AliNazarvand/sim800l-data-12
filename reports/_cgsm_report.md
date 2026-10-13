# +CGSM Migration Report

- CGSM in index: True
- Target ID: dat_01_0280
- CGSM already in dat_01: False
- AT+CGSM occurrences in extracted text: 7

Outcome: SKIP (no syntax 'AT+CGSM=' found in context)

## Context samples (first 2)

### Occurrence 1

```
..................172 
7.2.4 AT+CGQREQ  Quality of Service Profile (Requested) .............................................173 
7.2.5 AT+CGACT  PDP Context Activate or Deactivate ....................................................175 
7.2.6 AT+CGDATA  Enter Data State .................................................................................176 
7.2.7 AT+CGPADDR  Show PDP Address .........................................................................176 
7.2.8 AT+CGCLASS  GPRS Mobile Station Class .............................................................177 
7.2.9 AT+CGEREP  Control Unsolicited GPRS Event Reporting ......................................177 
7.2.10 AT+CGREG  Network Registration Status ..............................................................178 
7.2.11 AT+CGSMS  Select Service for MO SMS Messages ..............................................179 
8 AT Commands for TCPIP Application Toolkit ..................................181 
8.1 Overview ..........................................................................................................181 
8.2 Detailed Descriptions of Commands................................................................182 
8.2.1 AT+CIPMUX  Start Up Multi-IP Connection ............................................................182 
8.2.2 AT+CIPSTART  Start Up TCP or UDP Connection...................................................182 
8.2.3 AT+CIPSEND  Send Data Through TCP or UDP Connection .................
```

### Occurrence 2

```
<mode> 
Parameter 
<mode> 
0 re-open the micbias 
1 close the micbias  
Reference  
 
 Note 
 
 
                                                           S m a r t  M a c h i n e  S m a r t  D e c i s i o n  
SIM800 Series_AT Command Manual_V1.01 170 2013-07-23                    
7 AT Commands for GPRS Support 
7.1 Overview of AT Commands for GPRS Support 
Command Description 
AT+CGATT ATTACH OR DETACH FROM GPRS SERVICE 
AT+CGDCONT DEFINE PDP CONTEXT 
AT+CGQMIN QUALITY OF SERVICE PROFILE (MINIMUM ACCEPTABLE) 
AT+CGQREQ QUALITY OF SERVICE PROFILE (REQUESTED) 
AT+CGACT PDP CONTEXT ACTIV ATE OR DEACTIV ATE 
AT+CGDATA ENTER DATA STATE 
AT+CGPADDR SHOW PDP ADDRESS 
AT+CGCLASS GPRS MOBILE STATION CLASS 
AT+CGEREP CONTROL UNSOLICITED GPRS EVENT REPORTING 
AT+CGREG NETWORK REGISTRATION STATUS 
AT+CGSMS SELECT SERVICE FOR MO SMS MESSAGES 
 
7.2 Detailed Descriptions of AT Commands for GPRS Support 
7.2.1 AT+CGATT  Attach or Detach from GPRS Service 
AT+CGATT  Attach or Detach from GPRS Service 
Response 
+CGATT: (list of supported <state>s) 
 
OK 
Test Command 
AT+CGATT=? 
Parameter 
See Write Command 
Response 
+CGATT: <state> 
 
OK 
Read Command 
AT+CGATT? 
Parameter 
See Write Command 
Response 
OK 
If error is related to ME functionality: 
+CME ERROR: <err> 
Write Command 
AT+CGATT=<st
ate> 
Parameter 
                                                           S m a r t  M a c h i n e  S m a r t  D e c i s i o n  
SIM800 Series_AT Command Manual_V1.01 171 2013-07-23            
```
