#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import math
import re
from sys import argv
import datetime

if len(argv) == 3:
    script, filename, plot_channels = argv
else:
    script, filename = argv
    plot_outputs = ["latitude", "longitude"]

fields = [
    "timestamp",
    "latitude",
    "longitude",
    "position_type",
    "satellites",
    "altitude",
    "geoidal_separation",
    "age_of_differential_corrections",
    "deviation_latitude",
    "deviation_longitude",
    "deviation_altitude"
    ]

readings = []

# Parse the file
with open(filename) as f:
    for line in f:
        # Regular expression for the parser
        regex = re.match('^(\d+)\s([-\d\.]+)\s([-\d\.]+)\s([\w]+)\s(\d+)\s([\d\.]+)\s([\d\.]+)\s([\d\.]+)\s([\d\.]+)\s([\d\.]+)\s([\d\.]+)', line, re.IGNORECASE)
        if regex:
            values = []
            for m in regex.groups():
                values.append(m)
            # Append to the end of the list
            readings.append(dict(zip(fields, values)))

x = []
y = []

#plot_outputs = ["latitude", "longitude"]
#plot_outputs = ["satellites"]
#plot_outputs = [plot_channels]

"""for reading in readings:
    x.append(datetime.datetime.fromtimestamp(int(reading["timestamp"]) / 1000000.0))
    outputs = []
    for output in plot_outputs:
        outputs.append(reading[output])
    y.append(outputs)

plt.title(filename)
plt.ylabel("Value")
plt.xlabel("Time")
plt.plot(x, y)
plt.legend(plot_outputs)"""

x = []
y = []

for reading in readings:
    #print reading["latitude"], reading["longitude"]
    x.append(reading["latitude"])
    y.append(reading["longitude"])

plt.figure()
plt.title(filename)
plt.ylabel("y")
plt.xlabel("x")
plt.plot(x, y)
plt.axis('equal')
plt.show()

