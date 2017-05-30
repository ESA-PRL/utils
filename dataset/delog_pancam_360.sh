#!/bin/bash
set -e
source ./helper.sh

if [[ $# -eq 0 ]] ; then
    echo "Please provide path to the pancam.log file as argument"
    exit 1
fi

echo "Delogging the deinterlaced BB3 left and right camera pictures to bb3_left and bb3_right folders"

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

