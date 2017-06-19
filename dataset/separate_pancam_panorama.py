#!/usr/bin/env python

"""separate_pancam_panorama.py: Script that separates the PanCam images into left, center and right folders depending on the position of the pan-tilt unit"""

__author__      = "Karl Kangur"
__copyright__   = "Kangur Pagnamenta Robotics SNC"

import os
import shutil
import sys
import re
import datetime

# Define constants
IMAGE_LEFT = 0
IMAGE_CENTER = 1
IMAGE_RIGHT = 2

def separatePanCamImages(input_path, start_position = IMAGE_LEFT):
    # Make the left, center and right directories
    output_path = [input_path + "/left", input_path + "/center", input_path + "/right", input_path + "/center"]

    for path in output_path:
        if not os.path.exists(path):
            os.mkdir(path)

    # Process the files
    position = start_position
    # Files need to be sorted as os.listdir order is arbitrary
    for f in sorted(os.listdir(input_path)):
        # Only move files, not directories
        if not os.path.isdir(f):
            root = os.path.abspath(input_path)
            folder = os.path.basename(os.path.normpath(output_path[position]))
            file_source = os.path.join(root, f)
            file_destination = os.path.join(root, folder, f)
            shutil.move(file_source, file_destination)
            print "Moving %s to %s" % (file_source, file_destination)
            #file_destination = os.path.join(root, "other", f)
            #print "Moving %s" % file_source
            #shutil.move(file_source, file_destination)
            position = (position + 1) % len(output_path)
            
def separatePanCamImages2(input_path, ptu_position_file):

    # Read the PTU position to an array
    with open(ptu_position_file, "r") as f:
        ptu_positions = f.readlines()
        # you may also want to remove whitespace characters like `\n` at the end of each line
    ptu_positions = [x.strip() for x in ptu_positions]
    
    ptu_positions_timestamped = []
    # Parse the timestamps of the image positions
    for pos in ptu_positions:
        image_regexp = re.match(r'(?P<year>\d{4})_(?P<month>\d{2})_(?P<day>\d{2})_(?P<hour>\d{2})_(?P<minute>\d{2})_(?P<second>\d{2})_(?P<millisecond>\d{6})\s(?P<angle>[-\d\.]+)', pos)
        if image_regexp:
            stamp = datetime.datetime(
                int(image_regexp.group('year')),
                int(image_regexp.group('month')),
                int(image_regexp.group('day')),
                int(image_regexp.group('hour')),
                int(image_regexp.group('minute')),
                int(image_regexp.group('second')),
                int(image_regexp.group('millisecond')))
            pos = {"time": stamp, "angle": float(image_regexp.group('angle'))}
            ptu_positions_timestamped.append(pos)
    
    # Make the left, center and right folders
    output_path = [input_path + "/left", input_path + "/center", input_path + "/right", input_path + "/center"]
    for path in output_path:
        if not os.path.exists(path):
            os.mkdir(path)
    
    for f in sorted(os.listdir(input_path)):
        # Only move files, not directories
        if not os.path.isdir(f):
            # Get the timestamp of the image
            image_regexp = re.match(r'.+_(?P<year>\d{4})_(?P<month>\d{2})_(?P<day>\d{2})_(?P<hour>\d{2})_(?P<minute>\d{2})_(?P<second>\d{2})_(?P<millisecond>\d{3})_L', f)
            if image_regexp:
                stamp = datetime.datetime(
                    int(image_regexp.group('year')),
                    int(image_regexp.group('month')),
                    int(image_regexp.group('day')),
                    int(image_regexp.group('hour')),
                    int(image_regexp.group('minute')),
                    int(image_regexp.group('second')),
                    int(image_regexp.group('millisecond')))
                
                for pos in ptu_positions_timestamped:
                    # Angle is always registered after the picture
                    if (stamp - pos["time"]).total_seconds() < 0.0:
                        
                        if pos["angle"] == 0.0:                        
                            root = os.path.abspath(input_path)
                            folder = os.path.basename(os.path.normpath(input_path + "/center"))
                            file_source = os.path.join(root, f)
                            file_destination = os.path.join(root, folder, f)
                            shutil.move(file_source, file_destination)
                            print "Moving %s to %s" % (file_source, file_destination)
                            #print "Photo: %s, angle time: %s, difference: %f" % (stamp, pos["time"], abs((stamp - pos["time"]).total_seconds()))
                        
                        break
                else:
                    exit("Could not find angle for %s" % f)
 
    
if __name__ == "__main__":
    #separatePanCamImages("dataset_test/PanCam_panorama", IMAGE_RIGHT)
    separatePanCamImages2(sys.argv[1], sys.argv[2])


