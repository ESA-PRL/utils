#!/usr/bin/env python

"""check_timestamps.py: Script that checks all the timestamps for the sensors."""

__author__      = "Karl Kangur"
__copyright__   = "Kangur Pagnamenta Robotics SNC"

import subprocess
import os
from sys import argv
import threading
import time

if len(argv) == 2:
    script, log_path = argv
else:
    print("Enter log path as argument")
    exit()
    
# Class that accepts parameters for functions to be run in threads
class DelogThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)

def checkTimesamp(file_input, stream_name):
    path, filename = os.path.split(file_input)
    temp_filename = "%s.txt" % filename
    file_output = open(temp_filename, "w")
    subprocess.call(["pocolog", file_input, "-s", stream_name, "--fields", "time"], stdout = file_output)
    file_output.close()
    
    subprocess.call(["python", "../delogging/timestamp_delta.py", temp_filename])
    
    os.remove(temp_filename)

if __name__ == "__main__":
    log_list = [
        {"name": "bb2.log", "stream": "/camera_firewire_bb2.frame"},
        {"name": "bb3.log", "stream": "/camera_firewire_bb3.frame"},
        {"name": "pancam.log", "stream": "/pancam_panorama.left_frame_out"},
        {"name": "control.log", "stream": "/platform_driver.joints_readings"},
        {"name": "gyro.log", "stream": "/dsp1760.rotation_raw"},
        {"name": "imu.log", "stream": "/imu_stim300.inertial_sensors_out"},
        {"name": "lidar.log", "stream": "/velodyne_lidar.ir_frame"},
        {"name": "temperature.log", "stream": "/temperature.temperature_samples"},
        {"name": "tof.log", "stream": "/tofcamera_mesasr.tofscan"},
        {"name": "waypoint_navigation.log", "stream": "/gps.pose_samples"}
    ]

    for log in log_list:
        full_path = os.path.join(log_path, log["name"])
        log["thread"] = DelogThread(checkTimesamp, full_path, log["stream"])
        log["thread"].start()

    checking = False
    while checking:
        checking = False
        for log in log_list:
            if log["thread"].isAlive():
                checking = True
                break
        time.sleep(1)

