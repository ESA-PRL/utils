#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import math
import re
from sys import argv
import datetime

if len(argv) == 3:
    script, filename, plot_channel = argv
else:
    script, filename = argv
    plot_channel = "t"

fields = [ "timestamp" ]
readings_fixed = []
readings_auto = []
readings_diff = []
readings_other = []

# Parse the file
with open(filename) as f:
    for line in f:
        regex = re.match('^(\d+)', line, re.IGNORECASE)
        if regex:
            values = []
            for m in regex.groups():
                values.append(m)
            if "RTK_FIXED" in line:
                readings_fixed.append(dict(zip(fields, values)))
            elif "DIFFERENTIAL" in line:
                readings_diff.append(dict(zip(fields, values)))
            elif "AUTONOMOUS" in line:
                readings_auto.append(dict(zip(fields, values)))
            else:
                readings_other.append(dict(zip(fields, values)))

x_fixed = []
y_fixed = []

x_auto = []
y_auto = []

x_diff = []
y_diff = []

x_other = []
y_other = []

plot_outputs = ["timestamp_delta_fixed", "timestamp_delta_diff", "timestamp_delta_auto", "timestamp_delta_other"]

for i in range(1,len(readings_fixed)):
    x_fixed.append(datetime.datetime.fromtimestamp(float(int(readings_fixed[i]["timestamp"]) / 1000000.0)))
    y_fixed.append(int(readings_fixed[i]["timestamp"]) - int(readings_fixed[i-1]["timestamp"]) )

for i in range(1,len(readings_auto)):
    x_auto.append(datetime.datetime.fromtimestamp(float(int(readings_auto[i]["timestamp"]) / 1000000.0)))
    y_auto.append(int(readings_auto[i]["timestamp"]) - int(readings_auto[i-1]["timestamp"]) )

for i in range(1,len(readings_diff)):
    x_diff.append(datetime.datetime.fromtimestamp(float(int(readings_diff[i]["timestamp"]) / 1000000.0)))
    y_diff.append(int(readings_diff[i]["timestamp"]) - int(readings_diff[i-1]["timestamp"]) )

for i in range(1,len(readings_other)):
    x_other.append(datetime.datetime.fromtimestamp(float(int(readings_other[i]["timestamp"]) / 1000000.0)))
    y_other.append(int(readings_other[i]["timestamp"]) - int(readings_other[i-1]["timestamp"]) )

#print(np.mean(y))

plt.title(filename)
plt.ylabel("Timestamp Delta [usecs]")
plt.xlabel("Time [date]")
plt.plot(x_fixed, y_fixed, marker='o')
plt.plot(x_diff, y_diff, marker='o')
plt.plot(x_auto, y_auto, marker='o')
plt.plot(x_other, y_other, marker='o')
plt.legend(plot_outputs)
plt.show()
