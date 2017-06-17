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
    "timestamp",
    "t1",
    "t2",
    "t3",
    "t4",
    "t5",
    "t6"
    ]

readings = []

# Parse the file
with open(filename) as f:
    for line in f:
        # Regular expression for the parser
        regex = re.match('^(\d+)\s([-\d\.]+)\s([-\d\.]+)\s([-\d\.]+)\s([-\d\.]+)\s([-\d\.]+)\s([-\d\.]+)\s', line, re.IGNORECASE)
        if regex:
            values = []
            for m in regex.groups():
                values.append(m)
            # Append to the end of the list
            readings.append(dict(zip(fields, values)))

x = []
y = []

plot_outputs = [plot_channel+"1", plot_channel+"2", plot_channel+"3", plot_channel+"4" , plot_channel+"5" , plot_channel+"6"]

for reading in readings:
    x.append(datetime.datetime.fromtimestamp(int(reading["timestamp"]) / 1000000))
    outputs = []
    for output in plot_outputs:
        outputs.append(reading[output])
    y.append(outputs)

plt.title(filename)
plt.ylabel("Temperature")
plt.xlabel("Time")
plt.plot(x, y)
plt.legend(plot_outputs)
plt.show()

