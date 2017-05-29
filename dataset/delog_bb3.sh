#!/bin/bash
set -e
source ./helper.sh

if [[ $# -eq 0 ]] ; then
    echo "Please provide path to the bb3_deinterlaced.log file as argument"
    exit 1
fi

echo "Delogging the deinterlaced BB3 left and right camera pictures to bb3_left and bb3_right folders"

# Make directory if it does not exist yet
mkdir -p bb3_left
cd bb3_left
echo "Extracting BB3 left"
rock-export "$1" --stream /camera_bb3.left_frame --filename "#TIME.png" > /dev/null 2>&1
renameFilesUnix
cd ..

mkdir -p bb3_center
cd bb3_center
echo "Extracting BB3 center"
rock-export "$1" --stream /camera_bb3.center_frame --filename "#TIME.png" > /dev/null 2>&1
renameFilesUnix
cd ..

mkdir -p bb3_right
cd bb3_right
echo "Extracting BB3 right"
rock-export "$1" --stream /camera_bb3.right_frame --filename "#TIME.png" > /dev/null 2>&1
renameFilesUnix
cd ..
