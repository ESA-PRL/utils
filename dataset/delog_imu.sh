#!/bin/bash
set -e
source ./helper.sh

if [[ $# -eq 0 ]] ; then
    echo "Please provide path to the imu.log file as argument"
    exit 1
fi

imu_sensors_input="imu_sensors.txt"
imu_sensors_output="imu_sensors_formated.txt"
imu_orientation_input="imu_orientation.txt"
imu_orientation_output="imu_orientation_formated.txt"
imu_temperature_input="imu_temperature.txt"
imu_temperature_output="imu_temperature_formated.txt"

echo "Delogging the IMU streams"

# Make directory if it does not exist yet
mkdir -p imu
cd imu

echo "Extracting IMU sensors"
pocolog "$1" -s /imu_stim300.inertial_sensors_out >> $imu_sensors_input
echo "Reformating IMU sensors"
tail -n +3 $imu_sensors_input > "temp.txt"
echo "Timestamp accX accY accZ gyroX gyroY gyroZ magX magY magZ" | cat - "temp.txt" > temp2.txt && mv temp2.txt $imu_sensors_output
rm "temp.txt"
mv $imu_sensors_output $imu_sensors_input

echo "Extracting IMU temperature"
pocolog "$1" -s /imu_stim300.temp_sensors_out >> $imu_temperature_input
echo "Reformating IMU temperature"
tail -n +3 $imu_temperature_input > "temp.txt"
echo "Timestamp accXKelvin accYKelvin accZKelvin gyroXKelvin gyroYKelvin gyroZKelvin magXKelvin magYKelvin magZKelvin" | cat - "temp.txt" > temp2.txt && mv temp2.txt $imu_temperature_output
rm "temp.txt"
mv $imu_temperature_output $imu_temperature_input

echo "Extracting IMU orientation"
pocolog "$1" -s /imu_stim300.orientation_samples_out >> $imu_orientation_input
echo "Reformating IMU orientation"
regex_orientation='^([0-9]+)\s([0-9]{2,3}\s)+(nan\s)+([\.0-9e-]+)\s([\.0-9e-]+)\s([\.0-9e-]+)\s([\.0-9e-]+)'
echo "Timestamp quaternionX quaternionY quaternionZ quaternionW" > $imu_orientation_output
while read line; do
    if [[ $line =~ $regex_orientation ]]; then
        echo "${BASH_REMATCH[1]} ${BASH_REMATCH[4]} ${BASH_REMATCH[5]} ${BASH_REMATCH[6]} ${BASH_REMATCH[7]}" >> $imu_orientation_output
    fi
done < $imu_orientation_input
mv $imu_orientation_output $imu_orientation_input

cd ..

