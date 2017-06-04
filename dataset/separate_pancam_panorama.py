#!/usr/bin/env python

"""separate_pancam_panorama.py: Script that separates the PanCam images into left, center and right folders depending on the position of the pan-tilt unit"""

__author__      = "Karl Kangur"
__copyright__   = "Kangur Pagnamenta Robotics SNC"

import os
import shutil

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

if __name__ == "__main__":
    separatePanCamImages("dataset_test/PanCam_panorama", IMAGE_RIGHT)

