#!/usr/bin/env python

"Test script to validate the GPS heading component."

import numpy as np
import matplotlib.pyplot as plt
import math
import re
from sys import argv

script, filename = argv

names = ["DFL", "DFR", "DCL", "DCR", "DBL", "DBR", "SFL", "SFR", "SBL", "SBR", "ROL", "ROR", "BOL", "BOR", "timestamp"]
fields = ["position", "speed", "effort", "raw", "acceleration"]

joint_readings = []
# Parse the file
with open(filename) as f:
    for line in f:
        # Regular expression for the parser
        regex = re.match('^(?:\d{2}\s)+((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})((?:[^\s]+\s){5})(\d+)', line, re.IGNORECASE)
        if regex:
            joints = []
            for m in regex.groups():
                values = m.split(" ")
                # Append to the end of the list, 6 because it splits the last space as well
                if len(values) == 6:
                    joints.append(dict(zip(fields, values)))
                else:
                    joints.append(values[0])
            # Append to the end of the list
            joint_readings.append(dict(zip(names, joints)))

x = []
y = []
time_start = 0

for reading in joint_readings:
    if time_start == 0:
        time_start = int(reading["timestamp"])
    x.append(int(reading["timestamp"]) - time_start)
    #y.append([reading["DFL"]["effort"], reading["DFR"]["effort"], reading["DCL"]["effort"], reading["DCR"]["effort"], reading["DBL"]["effort"], reading["DBR"]["effort"]])
    #y.append([reading["SFL"]["effort"], reading["SFR"]["effort"], reading["SBL"]["effort"], reading["SBR"]["effort"]])
    y.append([reading["SFL"]["position"], reading["SFR"]["position"], reading["SBL"]["position"], reading["SBR"]["position"]])
    
# Filter data
#filtered_data = lowess([row[0] for row in y], x, is_sorted=True, frac=0.025, it=0)

plt.title("HDPR motor current during DECOS test (2017-02-21)")
plt.ylabel("Current")
plt.xlabel("Time")
plt.plot(x, y)
#plt.legend(["DFL", "DFR", "DCL", "DCR", "DBL", "DBR"])
plt.legend(["SFL", "SFR", "SBL", "SBR"])
plt.show()

