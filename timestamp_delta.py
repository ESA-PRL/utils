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

fields = [
        "timestamp"
        ]

readings = []

# Parse the file
with open(filename) as f:
    for line in f:
        regex = re.match('^(\d+)', line, re.IGNORECASE)
        if regex:
            values = []
            for m in regex.groups():
                values.append(m)
            readings.append(dict(zip(fields, values)))

x = []
y = []

plot_outputs = ["timestamp_delta"]

for i in range(1,len(readings)):
    x.append(datetime.datetime.fromtimestamp(float(int(readings[i]["timestamp"]) / 1000000.0)))
    y.append(int(readings[i]["timestamp"]) - int(readings[i-1]["timestamp"]) )
    #x.append(int(readings[i]["timestamp"]))

print(np.mean(y))

plt.title(filename)
plt.ylabel("Timestamp Delta")
plt.xlabel("Time")
plt.plot(x, y, marker='o')
#plt.plot(x, marker='o')
plt.legend(plot_outputs)
plt.show()
