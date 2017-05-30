#!/bin/bash
set -e
source ./helper.sh

if [[ $# -eq 0 ]] ; then
    echo "Please provide path to the pancam.log file as argument"
    exit 1
fi

pancam_panorama_pan="pancam_panorama_pan.txt"
pancam_panorama_tilt="pancam_panorama_tilt.txt"

echo "Delogging the pancam panorama pictures to pancam_panorama_left and pancam_panorama_right folders and pan/tilt angles to pancam_panorama_angles"

mkdir -p pancam_panorama_angles
cd pancam_panorama_angles
echo "Extracting pancam pan angles"
pocolog "$1" -s /pancam_panorama.pan_angle_out_degrees -t > $pancam_panorama_pan
tail -n +3 $pancam_panorama_pan > "temp.txt"
echo "Timestamp panAngleDegrees" | cat - "temp.txt" > temp2.txt && mv temp2.txt "temp.txt"
mv "temp.txt" $pancam_panorama_pan

echo "Extracting pancam tilt angles, beware that the tilt angle has a multiplication factor or 4, so the real angle is 1/4th the value"
pocolog "$1" -s /pancam_panorama.tilt_angle_out_degrees -t > $pancam_panorama_tilt
tail -n +3 $pancam_panorama_tilt > "temp.txt"
echo "Timestamp tiltAngleDegrees" | cat - "temp.txt" > temp2.txt && mv temp2.txt "temp.txt"
mv "temp.txt" $pancam_panorama_tilt
cd ..

mkdir -p pancam_panorama_left
cd pancam_panorama_left
echo "Extracting pancam panorama left"
rock-export "$1" --stream /pancam_panorama.left_frame_out --filename "#TIME.png" > /dev/null 2>&1
renameFilesUnix
cd ..

mkdir -p pancam_panorama_right
cd pancam_panorama_right
echo "Extracting pancam panorama right"
rock-export "$1" --stream /pancam_panorama.right_frame_out --filename "#TIME.png" > /dev/null 2>&1
renameFilesUnix
cd ..

