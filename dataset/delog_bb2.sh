#!/bin/bash
set -e
source ./helper.sh

if [[ $# -eq 0 ]] ; then
    echo "Please provide path to the bb2_deinterlaced.log file as argument"
    exit 1
fi

echo "Delogging the deinterlaced BB2 left and right camera pictures to bb2_left and bb2_right folders"

# Make directory if it does not exist yet
mkdir -p bb2_left
cd bb2_left
echo "Extracting BB2 left"
rock-export "$1" --stream /camera_bb2.left_frame --filename "#TIME.png" > /dev/null 2>&1
renameFilesUnix
cd ..

mkdir -p bb2_right
cd bb2_right
echo "Extracting BB2 right"
rock-export "$1" --stream /camera_bb2.right_frame --filename "#TIME.png" > /dev/null 2>&1
renameFilesUnix
cd ..

