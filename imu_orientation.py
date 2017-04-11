#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import math
import re
from sys import argv, exit
import datetime

if len(argv) == 3:
    script, filename, plot_channel = argv
else:
    script, filename = argv
    plot_channel = "pos"

fields = [
    "timestamp",
    "pos_x",
    "pos_y",
    "pos_z",
    "quaternion_x",
    "quaternion_y",
    "quaternion_z",
    "quaternion_w",
    "velocity_x",
    "velocity_y",
    "velocity_z",
    "angular_velocity_x",
    "angular_velocity_y",
    "angular_velocity_z"
    ]

readings = []

# Parse the file
with open(filename) as f:
    for line in f:
        # Regular expression for the parser
        regex = re.match('^(\d+)\s(?:[nan\d\s]+)([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)', line, re.IGNORECASE)
        if regex:
            values = []
            for m in regex.groups():
                values.append(m)
            # Append to the end of the list
            readings.append(dict(zip(fields, values)))

x = []
y = []

#plot_outputs = ["pos_x", "pos_y", "pos_z"]
#plot_outputs = ["quaternion_x", "quaternion_y", "quaternion_z", "quaternion_w"]
#plot_outputs = ["velocity_x", "velocity_y", "velocity_z"]
#plot_outputs = ["angular_velocity_x", "angular_velocity_y", "angular_velocity_z"]
plot_outputs = [plot_channel+"_x", plot_channel+"_y", plot_channel+"_z"]

for reading in readings:
    x.append(datetime.datetime.fromtimestamp(int(reading["timestamp"]) / 1000000))
    outputs = []
    for output in plot_outputs:
        outputs.append(reading[output])
    y.append(outputs)

plt.title(filename)
plt.ylabel("Value")
plt.xlabel("Time")
plt.plot(x, y)
plt.legend(plot_outputs)
plt.show()

