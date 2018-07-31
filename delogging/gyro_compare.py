#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import math
import re
from sys import argv
import datetime

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

plot_outputs = ["gyro_z"]

readings_gyro = []
x_gyro = []
y_gyro = []

# Parse the file
with open("imu_inertial.txt") as f:
    for line in f:
        # Regular expression for the parser
        regex = re.match('^(\d+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)', line, re.IGNORECASE)
        if regex:
            values = []
            for m in regex.groups():
                values.append(m)
            # Append to the end of the list
            readings_gyro.append(dict(zip(fields, values)))

for reading in readings_gyro:
    x_gyro.append(datetime.datetime.fromtimestamp(int(reading["timestamp"]) / 1000000.0))
    outputs = []
    for output in plot_outputs:
        outputs.append(reading[output])
    y_gyro.append(outputs)

readings_raw = []
x_raw = []
y_raw = []

# Parse the file
with open("gyro_inertial.txt") as f:
    for line in f:
        # Regular expression for the parser
        regex = re.match('^(\d+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)\s([-\d\.e]+)', line, re.IGNORECASE)
        if regex:
            values = []
            for m in regex.groups():
                values.append(m)
            # Append to the end of the list
            readings_raw.append(dict(zip(fields, values)))

for reading in readings_raw:
    x_raw.append(datetime.datetime.fromtimestamp(int(reading["timestamp"]) / 1000000.0))
    outputs = []
    for output in plot_outputs:
        outputs.append(reading[output])
    y_raw.append(outputs)

print "Earth rotation:", 7.2921159e-5 * math.sin(52.0 * math.pi / 180.0)
raw_mean = np.mean(np.array(y_raw).astype(np.float))
print "Raw mean:", raw_mean
earth_removed = np.mean(np.array(y_gyro).astype(np.float))
print "Earth rotation removed mean:", earth_removed
print "ROCK evaluated mean:", 5.5359030385e-06
print "Difference:", abs(earth_removed - 5.5359030385e-06)

plt.title("Gyro test")
plt.ylabel("Value")
plt.xlabel("Time")
plt.plot(x_gyro, y_gyro)
plt.plot(x_raw, y_raw)
plt.legend(["imu", "gyro"])
plt.show()

