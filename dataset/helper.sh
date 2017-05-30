#!/bin/bash

# Renames files from their human readable timestamp to unix timestamp
function renameFilesUnix {
    for f in *; do
        year=${f:0:4}
        month=${f:5:2}
        day=${f:8:2}
        hour=${f:11:2}
        minute=${f:14:2}
        second=${f:17:2}
        millisecond=${f:20:3}
        
        adate=$(date +%s%N -d "${month}/${day}/${year} ${hour}:${minute}:${second}.${millisecond}")
        mv $f "$adate.png"
    done
}

