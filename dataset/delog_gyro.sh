#!/bin/bash
set -e
source ./helper.sh

if [[ $# -eq 0 ]] ; then
    echo "Please provide path to the gyro.log file as argument"
    exit 1
fi

gyro_sensors="gyro_sensors.txt"
gyro_raw="gyro_raw.txt"
gyro_orientation="gyro_orientation.txt"
gyro_temperature="gyro_temperature.txt"

echo "Delogging the gyro streams"

# Make directory if it does not exist yet
mkdir -p gyro
cd gyro

echo "Extracting gyro sensors"
pocolog "$1" -s /dsp1760.rotation > "temp.txt"
echo "Reformating gyro sensors"
regex_sensors='^([0-9]+)\s0\s0\s0\s0\s0\s([\.0-9e-]+)'
echo "Timestamp rotationZrad" > $gyro_sensors
while read line; do
    if [[ $line =~ $regex_sensors ]]; then
        echo "${BASH_REMATCH[1]} ${BASH_REMATCH[2]}" >> $gyro_sensors
    fi
done < "temp.txt"
rm "temp.txt"

echo "Extracting gyro raw data"
pocolog "$1" -s /dsp1760.rotation_raw > "temp.txt"
echo "Reformating gyro raw data"
regex_raw='^([0-9]+)\s0\s0\s0\s0\s0\s([\.0-9e-]+)'
echo "Timestamp rotationZrad" > $gyro_raw
while read line; do
    if [[ $line =~ $regex_raw ]]; then
        echo "${BASH_REMATCH[1]} ${BASH_REMATCH[2]}" >> $gyro_raw
    fi
done < "temp.txt"
rm "temp.txt"

echo "Extracting gyro orientation"
pocolog "$1" -s /dsp1760.orientation_samples > "temp.txt"
echo "Reformating gyro raw data"
regex_orientation='^([0-9]+)\snan\snan\snan\snan\snan\snan\snan\snan\snan\snan\snan\snan\s([\.0-9e-]+)\s([\.0-9e-]+)\s([\.0-9e-]+)\s([\.0-9e-]+)\snan\snan\snan\snan\snan\snan\snan\snan\snan\snan\snan\snan\snan\snan\snan\snan\snan\snan\snan\snan\snan\s([\.0-9e-]+)\s([\.0-9e-]+)\s([\.0-9e-]+)'
echo "Timestamp quaternionX quaternionY quaternionZ quaternionW angVelRadPerSecondX angVelRadPerSecondY angVelRadPerSecondZ" > $gyro_orientation
while read line; do
    if [[ $line =~ $regex_orientation ]]; then
        echo "${BASH_REMATCH[1]} ${BASH_REMATCH[2]} ${BASH_REMATCH[3]} ${BASH_REMATCH[4]} ${BASH_REMATCH[5]} ${BASH_REMATCH[6]} ${BASH_REMATCH[7]} ${BASH_REMATCH[8]}" >> $gyro_orientation
    fi
done < "temp.txt"
rm "temp.txt"

echo "Extracting gyro temperature"
pocolog "$1" -s /dsp1760.temperature -t > $gyro_temperature
tail -n +3 $gyro_temperature > "temp.txt"
echo "Timestamp gyroTempCelsius" | cat - "temp.txt" > temp2.txt && mv temp2.txt "temp.txt"
mv "temp.txt" $gyro_temperature

cd ..

