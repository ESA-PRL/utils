#!/bin/bash

function renameFiles {
    for f in "$1/"*; do
        year=${f:5:4}
        month=${f:10:2}
        day=${f:13:2}
        hour=${f:16:2}
        minute=${f:19:2}
        second=${f:22:2}
        millisecond=${f:25:3}
        
        adate=$(date +%s%N -d "${month}/${day}/${year} ${hour}:${minute}:${second}.${millisecond}")
        mv $f "$1/$adate.png"
    done
}

cd rover_frame

mkdir cam0
cd cam0
echo "Extracting pancam right"
rock-export ../pancam.log --stream /pancam_right.frame --filename "#TIME.png" > /dev/null 2>&1
cd ..
renameFiles cam0

echo "Image extraction done"

echo "Generating bag file"

kalibr_bagcreater --folder . --output-bag rover_frame.bag

echo "Calibrating cameras using the bag file"

kalibr_calibrate_cameras --bag rover_frame.bag --topics /cam0/image_raw --models pinhole-radtan --target ../aprilgrid_target_3x3.yaml



