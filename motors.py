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
    plot_channel = "effort"

fields = [
    "DFL",
    "DFR",
    "DCL",
    "DCR",
    "DBL",
    "DBR",
    "SFL",
    "SFR",
    "SBL",
    "SBR",
    "ROL",
    "ROR",
    "BOL",
    "BOR",
    "timestamp"
    ]

parameters = [
    "position",
    "speed",
    "effort",
    "raw",
    "acceleration"
    ]

readings = []

# Parse the file
with open(filename) as f:
    for line in f:
        # Regular expression for the parser
        regex = re.match('^(?:\d{2}\s)+((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})(\d+)', line, re.IGNORECASE)
        if regex:
            values = []
            for m in regex.groups():
                m = m.split(" ")
                if len(m) == 6:
                    values.append(dict(zip(parameters, m)))
                else:
                    values.append(m[0])
            # Append to the end of the list
            readings.append(dict(zip(fields, values)))
x = []
y = []

plot_outputs = ["DFL", "DFR", "DCL", "DCR", "DBL", "DBR"]
#plot_outputs = ["SFL", "SFR", "SBL", "SBR"]
#plot_outputs = ["ROL", "ROR"]

for reading in readings:
    x.append(datetime.datetime.fromtimestamp(float(reading["timestamp"]) / 1000000.0))
    outputs = []
    for output in plot_outputs:
        outputs.append(reading[output][plot_channel])
    y.append(outputs)

plt.title(filename)
plt.ylabel(plot_channel)
plt.xlabel("Time")
plt.plot(x, y)
plt.legend(plot_outputs)
plt.show()

