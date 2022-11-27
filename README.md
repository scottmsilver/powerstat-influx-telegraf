# powerstat-influx-telegraf
Outputs stats in influx line protocol format about a CyberPower UPC by querying powerstatd.

# Install
```
pip install influx_line_protocol
git clone https://github.com/scottmsilver/powerstat-influx-telegraf
```

# Test

```
python3 powerstat-influx-telegraf/power-stat-telegraf.py
```

# Install in telegraf

# telegraf.conf
Add the following to telegraf.conf. NB: you will need to change your paths below.

```
[[inputs.exec]]
        commands = ["/home/ssilver/powerpanel/env/bin/python3 /home/ssilver/powerpanel/powerstat-influx-telegraf/power-stat-telegraf.py"]
        timeout = "2m"
        data_format = "influx"
        interval = "10m"
```

# Test telegraf

Look for a line about cyberpower, below

```
telegraf --test
```

```
> cyberpower,avr_supported=yes,battery_volt=24000,host=measure-slc,input_rating_volt=120000,online_type=no,output_rating_watt=900000 ac_present="yes",battery_capacity=100,battery_charging="no",battery_discharging="no",battery_remainingtime=7226,boost="no",diagnostic_date="2022/11/22 05:41:08",diagnostic_result=1,firmware_num="",load=14000,model_name="",output_volt=123000,power_event_date="2022/11/07 12:02:43",power_event_during="3 sec.",power_event_result=2,state=0,utility_volt=123000 1669575389000000000
```

# Use in influx
Example FluxQL query to query capacity, assuming your bucket is telegraf
```
from(bucket: "telegraf")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "cyberpower")
  |> filter(fn: (r) => r["_field"] == "battery_capacity")
  |> aggregateWindow(every: v.windowPeriod, fn: mean, createEmpty: false)
  |> yield(name: "mean")
```
