#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import math
import re
from sys import argv
import datetime

if len(argv) == 3:
    script, gps_heading_filename, gyro_heading_filename = argv
else:
    print "Enter the gps_heading and gyro_heading paths as arguments"
    exit(0)

gyro_offset = 0
plot_channel = "quaternion"

gps_fields = [
    "timestamp",
    "pos_x",
    "pos_y",
    "pos_z",
    "quaternion_x",
    "quaternion_y",
    "quaternion_z",
    "quaternion_w"
    ]

gps_readings = []

# Parse the gps_heading file
with open(gps_heading_filename) as f:
    for line in f:
        # Regular expression for the parser
        regex = re.match('^(\d+)\s(?:\d{2,3}\s){12}([-\d\.]+)\s([-\d\.]+)\s([-\d\.]+)\s(?:nan\s){9}([-\d\.]+)\s([-\d\.]+)\s([-\d\.]+)\s([-\d\.]+)', line, re.IGNORECASE)
        if regex:
            values = []
            for m in regex.groups():
                values.append(m)
            # Append to the end of the list
            gps_readings.append(dict(zip(gps_fields, values)))

gps_x = []
gps_y = []

plot_outputs = [plot_channel+"_x", plot_channel+"_y", plot_channel+"_z", plot_channel+"_w"]

for reading in gps_readings:
    gps_x.append(datetime.datetime.fromtimestamp(int(reading["timestamp"]) / 1000000.0))
    outputs = []
    for output in plot_outputs:
        outputs.append(float(reading[output]))
    angle_rad = math.atan2(2.0*(outputs[0]*outputs[1] + outputs[3]*outputs[2]), outputs[3]*outputs[3] + outputs[0]*outputs[0] - outputs[1]*outputs[1] - outputs[2]*outputs[2]);
    gps_y.append(((angle_rad + math.pi) % math.pi) * 180.0 / math.pi)
    #if reading["timestamp"] > 1494336343835561:
    #    print datetime.datetime.fromtimestamp(int(reading["timestamp"]) / 1000000.0)
    #    break
    if gyro_offset == 0 and int(reading["timestamp"]) > 1494336357929815:
        gyro_offset = -angle_rad

gyro_fields = [
    "timestamp",
    "quaternion_x",
    "quaternion_y",
    "quaternion_z",
    "quaternion_w"
    ]

gyro_readings = []

# Parse the gps_heading file
with open(gyro_heading_filename) as f:
    for line in f:
        # Regular expression for the parser
        regex = re.match('^(\d+)\s(?:nan\s){12}([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)\s([-e\d\.]+)', line, re.IGNORECASE)
        if regex:
            values = []
            for m in regex.groups():
                values.append(m)
            # Append to the end of the list
            gyro_readings.append(dict(zip(gyro_fields, values)))

gyro_x = []
gyro_y = []

for reading in gyro_readings:
    gyro_x.append(datetime.datetime.fromtimestamp(int(reading["timestamp"]) / 1000000.0))
    outputs = []
    for output in plot_outputs:
        outputs.append(float(reading[output]))
    angle_rad = math.atan2(2.0*(outputs[0]*outputs[1] + outputs[3]*outputs[2]), outputs[3]*outputs[3] + outputs[0]*outputs[0] - outputs[1]*outputs[1] - outputs[2]*outputs[2]) - gyro_offset;
    gyro_y.append(((angle_rad + math.pi) % math.pi) * 180.0 / math.pi)

plt.title("GPS heading vs gyro heading")
plt.ylabel("Value")
plt.xlabel("Time")
plt.plot(gps_x, gps_y)
plt.plot(gyro_x, gyro_y)
#plt.plot(gyro_x, gyro_y, marker='o')
plt.legend(["GPS heading", "gyro heading"])
plt.show()


