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
    plot_channel = "acc"

fields = [
    "timestamp",
    "acc_x",
    "acc_y",
    "acc_z",
    "gyro_x",
    "gyro_y",
    "gyro_z",
    "mag_x",
    "mag_y",
    "mag_z"
    ]

readings = []

# Parse the file
with open(filename) as f:
    for line in f:
        # Regular expression for the parser
        regex = re.match('^(\d+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)', line, re.IGNORECASE)
        if regex:
            values = []
            for m in regex.groups():
                values.append(m)
            # Append to the end of the list
            readings.append(dict(zip(fields, values)))

x = []
y = []

#plot_outputs = ["acc_x", "acc_y", "acc_z"]
#plot_outputs = ["gyro_x", "gyro_y", "gyro_z"]
#plot_outputs = ["mag_x", "mag_y", "mag_z"]
plot_outputs = [plot_channel+"_x", plot_channel+"_y", plot_channel+"_z"]

for reading in readings:
    x.append(datetime.datetime.fromtimestamp(int(reading["timestamp"]) / 1000000.0))
    outputs = []
    for output in plot_outputs:
        outputs.append(reading[output])
    y.append(outputs)

plt.title(filename)
plt.ylabel("Value")
plt.xlabel("Time")
plt.plot(x, y, marker='o')
plt.legend(plot_outputs)
plt.show()

