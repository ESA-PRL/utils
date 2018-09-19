#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import math
import re
from sys import argv

script, filename = argv

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
        regex = re.match('^(\d+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)', line, re.IGNORECASE)
        if regex:
            values = []
            for m in regex.groups():
                values.append(m)
            # Append to the end of the list
            readings.append(dict(zip(fields, values)))

x = []
y = []
time_start = 0

for reading in readings:
    if time_start == 0:
        time_start = int(reading["timestamp"])
    x.append(int(reading["timestamp"]) - time_start)
    y.append([reading["gyro_x"], reading["gyro_y"], reading["gyro_z"]])
    #y.append([reading["acc_x"], reading["acc_y"], reading["acc_z"]])

plt.title(filename)
plt.ylabel("Accelerometer")
plt.xlabel("Timestamp")
plt.plot(x, y)
plt.legend(["gyro_x", "gyro_y", "gyro_z"])
#plt.legend(["acc_x", "acc_y", "acc_z"])
plt.show()

