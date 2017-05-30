#!/bin/bash
set -e
source ./helper.sh

if [[ $# -eq 0 ]] ; then
    echo "Please provide path to the pancam.log file as argument"
    exit 1
fi

pancam_360_pan="pancam_360_pan.txt"
pancam_360_tilt="pancam_360_tilt.txt"
pancam_360_set="pancam_360_set.txt"

echo "Delogging the pancam 360 pictures to pancam_360_left and pancam_360_right folders and pan/tilt angles and number of the set to pancam_360_angles"

mkdir -p pancam_360_angles
cd pancam_360_angles
echo "Extracting pancam pan angles"
pocolog "$1" -s /pancam_360.pan_angle_out_degrees -t > $pancam_360_pan
echo "Extracting pancam tilt angles"
pocolog "$1" -s /pancam_360.tilt_angle_out_degrees -t > $pancam_360_tilt
echo "Extracting pancam set identification numbers"
pocolog "$1" -s /pancam_360.set_id -t > $pancam_360_set
cd ..

# Make directory if it does not exist yet
mkdir -p pancam_360_left
cd pancam_360_left
echo "Extracting pancam 360 left"
rock-export "$1" --stream /pancam_360.left_frame_out --filename "#TIME.png" > /dev/null 2>&1
renameFilesUnix
cd ..

mkdir -p pancam_360_right
cd pancam_360_right
echo "Extracting pancam 360 right"
rock-export "$1" --stream /pancam_360.right_frame_out --filename "#TIME.png" > /dev/null 2>&1
renameFilesUnix
cd ..

