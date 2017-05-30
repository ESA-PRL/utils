#!/bin/bash
set -e
source ./helper.sh

if [[ $# -eq 0 ]] ; then
    echo "Please provide path to the tof.log file as argument"
    exit 1
fi

echo "Delogging the pancam TOF pictures, index building might take some time..."

# Make directory if it does not exist yet
mkdir -p tof_ir_frame
cd tof_ir_frame
echo "Extracting TOF IR frames to tof_ir_frame"
rock-export "$1" --stream /tofcamera_mesasr.ir_frame --filename "#TIME.png" > /dev/null 2>&1
renameFilesUnix
cd ..

