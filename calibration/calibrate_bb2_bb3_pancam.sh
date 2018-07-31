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

cd bb2_bb3_pancam

mkdir cam0
cd cam0
echo "Extracting BB2 left"
rock-export ../bb2.log --stream /camera_bb2.left_frame --filename "#TIME.png" > /dev/null 2>&1
cd ..
renameFiles cam0

mkdir cam1
cd cam1
echo "Extracting BB2 right"
rock-export ../bb2.log --stream /camera_bb2.right_frame --filename "#TIME.png" > /dev/null 2>&1
cd ..
renameFiles cam1

mkdir cam2
cd cam2
echo "Extracting BB3 left"
rock-export ../bb3.log --stream /camera_bb3.left_frame --filename "#TIME.png" > /dev/null 2>&1
cd ..
renameFiles cam2

mkdir cam3
cd cam3
echo "Extracting BB3 center"
rock-export ../bb3.log --stream /camera_bb3.center_frame --filename "#TIME.png" > /dev/null 2>&1
cd ..
renameFiles cam3

mkdir cam4
cd cam4
echo "Extracting BB3 right"
rock-export ../bb3.log --stream /camera_bb3.right_frame --filename "#TIME.png" > /dev/null 2>&1
cd ..
renameFiles cam4

mkdir cam5
cd cam5
echo "Extracting pancam left"
rock-export ../pancam.log --stream /pancam_left.frame --filename "#TIME.png" > /dev/null 2>&1
cd ..
renameFiles cam5

mkdir cam6
cd cam6
echo "Extracting pancam right"
rock-export ../pancam.log --stream /pancam_right.frame --filename "#TIME.png" > /dev/null 2>&1
cd ..
renameFiles cam6

echo "Image extraction done"

echo "Generating bag file"

kalibr_bagcreater --folder . --output-bag bb2_bb3_pancam.bag

echo "Calibrating cameras using the bag file"

kalibr_calibrate_cameras --bag bb2_bb3_pancam.bag --topics /cam0/image_raw /cam1/image_raw /cam2/image_raw /cam3/image_raw /cam4/image_raw /cam5/image_raw /cam6/image_raw --models pinhole-radtan pinhole-radtan pinhole-radtan pinhole-radtan pinhole-radtan pinhole-radtan pinhole-radtan --target ./aprilgrid_target_6x6.yaml



