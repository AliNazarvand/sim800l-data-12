# PHASE2-v3 HW datasets
import sys, pathlib
from datetime import datetime, timezone
try:
    import yaml
except ImportError:
    print("PyYAML required"); sys.exit(2)

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
SRC = "SIM800L_Hardware_Design_V1.00"

def rec(p, i, payload):
    b = {"id":f"{p}_{i:04d}","source_type":"primary",
         "applicable_models":["SIM800L"],"created_at":NOW,"updated_at":NOW}
    b.update(payload); return b

def write(p, recs, fname):
    (DATA / fname).write_text(
        yaml.safe_dump({"records":recs}, allow_unicode=True, sort_keys=False, width=200),
        encoding="utf-8")
    print(f"  {p}: wrote {len(recs)} records -> {fname}")

def dat_04():
    rows = [
        ("PWRKEY low time (power on)", 1000, None, None, "ms", "PWRKEY pulled low then release", "4.2.1"),
        ("PWRKEY low time (power down)", 1000, None, None, "ms", "PWRKEY pulled low then release", "4.2.2.1"),
        ("RESET low pulse time", 105, None, None, "ms", "RESET pin held low", "4.2.3 Table 6"),
        ("RESET VIH", 2.7, 2.8, 2.9, "V", "High level input", "4.2.3 Table 6"),
        ("RESET VIL", None, None, 0.6, "V", "Low level input", "4.2.3 Table 6"),
        ("Wake from sleep via DTR low", 50, None, None, "ms", "DTR to low then serial active", "4.3.3"),
        ("Serial VIL", 0, None, 0.3, "V", "Digital interface", "4.5 Table 9"),
        ("Serial VIH", 2.5, None, 2.8, "V", "Digital interface", "4.5 Table 9"),
        ("Serial VOL", 0, None, 0.1, "V", "Digital interface", "4.5 Table 9"),
        ("Serial VOH", 2.7, None, 2.8, "V", "Digital interface", "4.5 Table 9"),
        ("VBAT recommended operating", 3.4, 4.0, 4.4, "V", "Supply voltage", "6.2 Table 42"),
        ("VBAT absolute maximum", None, None, 4.5, "V", "Stress rating", "6.1 Table 41"),
        ("VBAT under-voltage warning", None, 3.5, None, "V", "URC emitted below", "4.2.2.3"),
        ("VBAT over-voltage warning", 4.3, None, None, "V", "URC emitted above", "4.2.2.3"),
        ("VBAT under-voltage shutdown", None, None, 3.4, "V", "Shutdown threshold", "4.2.2.3"),
        ("VBAT over-voltage shutdown", 4.4, None, None, "V", "Shutdown threshold", "4.2.2.3"),
        ("VBUS operating voltage", 4.3, 5.0, 7.0, "V", "USB power", "4.5.3 Table 10"),
        ("ADC voltage range", 0, None, 2.8, "V", "Analog input", "4.13 Table 29"),
        ("ADC resolution", None, 10, None, "bits", "ADC spec", "4.13 Table 29"),
        ("PWM output frequency", 0, None, 2000, "Hz", "PWM spec", "4.14"),
        ("Microphone bias voltage", 1.9, 2.2, None, "V", "Mic input", "4.7.3 Table 15"),
        ("VDD_EXT output voltage", 2.70, 2.80, 2.90, "V", "2.8V output", "6.6 Table 46"),
        ("SIM_VDD output voltage", None, 1.80, None, "V", "SIM 1.8V mode", "6.5 Table 45"),
        ("VRTC input voltage", None, 2.8, None, "V", "RTC backup", "6.7 Table 47"),
    ]
    return [rec("dat_04", i, {"category":"Timing","parameter":p,"min":mn,"typ":ty,"max":mx,
            "unit":u,"condition":c,
            "source":{"name":SRC,"version":"V1.00","date":"2013-08-20","section":s},
            "confidence":0.9,"status":"complete","notes":"","tags":["timing"]})
            for i,(p,mn,ty,mx,u,c,s) in enumerate(rows,1)]

def dat_05():
    rows = [
        ("OFF","Module fully powered off","Power down AT+CPOWD or PWRKEY","PWRKEY low >=1s",
         ["PWRKEY pull-down"],["Assert PWRKEY low"],"4.2.2"),
        ("POWER_ON","Boot sequence running","PWRKEY pull-down done","RDY URC received",
         ["RDY emitted"],["Wait for RDY","Send AT"],"4.2.1"),
        ("SIM_READY","SIM detected and initialized","AT+CPIN? READY","AT+CFUN=0 or SIM removed",
         ["AT+CPIN?","+CPIN: READY"],["Read IMSI","Read ICCID"],"3.2.28"),
        ("NETWORK_SEARCH","Searching network","SIM ready + CFUN=1","Registered home/roaming",
         ["+CREG: 1","+CREG: 5"],["Poll AT+CREG?"],"3.2.32"),
        ("REGISTERED","Registered to network","+CREG: 1 or 5","GPRS attach or CFUN=0",
         ["+CREG: 1","+CREG: 5"],["Enable GPRS"],"3.2.32"),
        ("GPRS_STANDBY","GPRS attached, no data session","AT+CGATT=1","PDP activation",
         ["+CGATT: 1"],["Configure APN"],"7.2.1"),
        ("PDP_ACTIVE","PDP active, local IP assigned","AT+CIICR/CIFSR","CIPSHUT or PDP DEACT",
         ["+PDP: DEACT"],["Open TCP/UDP"],"8.2.10"),
        ("DATA_MODE","Active TCP/UDP transfer","CIPSTART returns CONNECT OK","CIPCLOSE or remote disconnect",
         ["CONNECT OK","SEND OK","CLOSED"],["Send via CIPSEND"],"8.2.2"),
        ("SMS_MODE","SMS send/receive","CMGF set or CMGS","Session complete",
         ["+CMTI","+CMGS"],["Read/send SMS"],"4.2.5"),
        ("CALL_MODE","Voice/data/fax call","ATD or ATA","ATH or NO CARRIER",
         ["RING","CONNECT"],["Manage via CHLD"],"2.2.2"),
        ("SLEEP","Low power, UART not accessible","CSCLK=1 + DTR high + no IRQ",
         "DTR low, call, SMS, IRQ",["DTR low"],["Wait for wake"],"4.3.2"),
        ("MINIMUM_FUNCTIONALITY","RF and/or SIM disabled","CFUN=0 or CFUN=4","CFUN=1",
         ["+CFUN: 0","+CFUN: 4"],["Minimize current"],"4.3.1"),
        ("CHARGE","Charger connected (HW support)","VBUS + charge circuit","Charger removed",
         ["+CBC charging"],["Monitor via CBC"],"3.2.56"),
        ("ERROR","Fatal voltage/temperature condition","Voltage or temp out of range","Power cycle",
         ["OVER-VOLTAGE POWER DOWN","UNDER-VOLTAGE POWER DOWN"],["Power cycle"],"4.2.2.3"),
    ]
    return [rec("dat_05", i, {"category":"State","state_name":n,"description":d,
            "entry_conditions":[e] if isinstance(e,str) else e,
            "exit_conditions":[x] if isinstance(x,str) else x,
            "events":ev,"actions":ac,
            "source":{"name":SRC,"version":"V1.00","date":"2013-08-20","section":s},
            "confidence":0.85,"status":"complete","notes":"","tags":["state"]})
            for i,(n,d,e,x,ev,ac,s) in enumerate(rows,1)]

def dat_06():
    rows = [
        (1,"Assert PWRKEY low","PWRKEY",None,1000,1,"Retry",None,"OFF","4.2.1"),
        (2,"Wait for RDY","RDY","RDY",5000,0,"Check baud",1,"POWER_ON","4.2.1"),
        (3,"Sync baud","AT","OK",1000,5,"Check baud",2,"POWER_ON","4.5.2"),
        (4,"Disable echo","ATE0","OK",500,2,"None",3,"POWER_ON","2.2.7"),
        (5,"Set error reporting","AT+CMEE=2","OK",500,2,"None",4,"POWER_ON","3.2.20"),
        (6,"Check SIM","AT+CPIN?","+CPIN: READY",5000,5,"Wait SIM",5,"SIM_READY","3.2.28"),
        (7,"Wait network","AT+CREG?","+CREG: 0,1",30000,10,"Check antenna",6,"REGISTERED","3.2.32"),
        (8,"Attach GPRS","AT+CGATT=1","OK",60000,3,"Check APN",7,"GPRS_STANDBY","7.2.1"),
        (9,"Define PDP","AT+CGDCONT=1,\"IP\",\"<APN>\"","OK",5000,2,"Check APN",8,"GPRS_STANDBY","7.2.2"),
        (10,"Start TCP task","AT+CSTT=\"<APN>\",\"<user>\",\"<pwd>\"","OK",5000,2,"Check creds",9,"GPRS_STANDBY","8.2.9"),
        (11,"Bring up wireless","AT+CIICR","OK",60000,3,"Check CSQ",10,"PDP_ACTIVE","8.2.10"),
        (12,"Get local IP","AT+CIFSR","<ip>",5000,3,"Retry CIICR",11,"PDP_ACTIVE","8.2.11"),
        (13,"Open TCP","AT+CIPSTART=\"TCP\",\"<host>\",<port>","CONNECT OK",75000,3,"Check host/DNS",12,"DATA_MODE","8.2.2"),
        (14,"Send data","AT+CIPSEND",">",5000,3,"Check state",13,"DATA_MODE","8.2.3"),
        (15,"Close connection","AT+CIPCLOSE","CLOSE OK",10000,2,"None",14,"PDP_ACTIVE","8.2.6"),
        (16,"Shut down GPRS","AT+CIPSHUT","SHUT OK",20000,2,"None",15,"GPRS_STANDBY","8.2.7"),
        (17,"Set SMS text mode","AT+CMGF=1","OK",1000,2,"None",6,"SMS_MODE","4.2.2"),
        (18,"Configure new-SMS URC","AT+CNMI=2,1","OK",1000,2,"None",17,"SMS_MODE","4.2.8"),
        (19,"Enter sleep","AT+CSCLK=1","OK",1000,2,"Check DTR",3,"SLEEP","4.3.2"),
        (20,"Normal power down","AT+CPOWD=1","NORMAL POWER DOWN",5000,1,"Force PWRKEY",2,"OFF","6.2.2"),
    ]
    return [rec("dat_06", o, {"category":"Sequence","step_order":o,"description":d,
            "command":c,"expected_response":er,"timeout_ms":t,"retry_count":r,
            "failure_action":fa,"dependency_step":dep,"related_state":st,
            "source":{"name":SRC,"version":"V1.00","date":"2013-08-20","section":s},
            "confidence":0.85,"status":"complete","notes":"","tags":["init"]})
            for o,d,c,er,t,r,fa,dep,st,s in rows]

print("== HW ==")
write("dat_04", dat_04(), "dat_04_timing_timeout.yaml")
write("dat_05", dat_05(), "dat_05_state_machine.yaml")
write("dat_06", dat_06(), "dat_06_init_sequence.yaml")