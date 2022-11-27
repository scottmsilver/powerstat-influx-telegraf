"""
Prints an influx line protocol compatible version of metrics from pwrstatd (CyberPower daemon).

e.g. will print the following:

cyberpower,battery_volt=24000,input_rating_volt=120000,output_rating_watt=900000,avr_supported=yes,online_type=no state=0,model_name="",firmware_num="",diagnostic_result=1,diagnostic_date="2022/11/22 05:41:08",power_event_result=2,power_event_date="2022/11/07 12:02:43",power_event_during="3 sec.",battery_remainingtime=6867,battery_charging="no",battery_discharging="no",ac_present="yes",boost="no",utility_volt=123000,output_volt=123000,load=16000,battery_capacity=100

"""
import os
import socket
import time

from influx_line_protocol import Metric

# Return True if element can be parsed into a float.
def isFloat(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False

# Returns all data available from powerstatd as a dictionary.
def getPowerStatData():
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("/var/pwrstatd.ipc")
    s.sendall(b"STATUS\n\n")
    data = s.recv(512)
    
    result = {}
    
    for line in data.decode("ascii").splitlines():
        col = line.split("=")
        if len(col) != 2:
            continue
        result[col[0]] = col[1]
        
    return result

# Build the cyberpower metric and print it out.
metric = Metric("cyberpower")
tags = ("input_rating_volt", "output_rating_watt", "battery_volt", "output_rating_watt", "avr_supported", "online_type")
data = getPowerStatData()
for key in data:
   if key in tags:
       metric.add_tag(key, data[key])
   else:
       if isFloat(data[key]):
           metric.add_value(key, float(data[key]))
       else:
           metric.add_value(key, data[key])

print(metric)
