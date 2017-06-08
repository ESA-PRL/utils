#!/usr/bin/env python

"""create_dataset.py: Script that delogs ROCK .log files and creates a dataset."""

__author__      = "Karl Kangur"
__copyright__   = "Kangur Pagnamenta Robotics SNC"

import subprocess
import os
import sys
from datetime import datetime
import time
import threading

# Class that accepts parameters for functions to be run in threads
class DelogThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)

def formatTime(timestampUnix):
    # Provide integer as input 
    timestamp = datetime.fromtimestamp(timestampUnix)
    return timestamp.strftime('%Y_%m_%d_%H_%M_%S_%f')

def getTimestampedDictionary(input_array, timestamp_field_index = 0):
    # Make a dictionary with the input array, use timestamp as key value
    output_array = {}
    for item in input_array:
        # Required because of the log file headers
        try:
            timestamp = item.split(" ").pop(timestamp_field_index)
            output_array.update({timestamp: item})
        except Exception as e:
            # Skip the header
            continue
    return output_array

def showTime(item, start_time):
    elapsed_time = time.time() - start_time
    print "%s delog finished in %s seconds" % (item, elapsed_time)

def runRubyScript(script_name, log_folder):
    subprocess.call(["ruby", script_name, log_folder])

def delogPanCamPTU(file_input, file_output, stream_pan, stream_tilt):
    print "Delogging PTU angles from %s to %s" % (file_input, file_output)
    start_time = time.time()

    # Delog the pan angle
    file_pan = open("temp_pan.txt", "w")
    subprocess.call(["pocolog", file_input, "-s", stream_pan, "-t"], stdout = file_pan)
    file_pan.close()

    # Delog the tilt angle
    file_tilt = open("temp_tilt.txt", "w")
    subprocess.call(["pocolog", file_input, "-s", stream_tilt, "-t"], stdout = file_tilt)
    file_tilt.close()

    # Read all pan angles to array
    with open("temp_pan.txt", "r") as lines:
        content_pan = lines.readlines()
    content_pan = [x.strip() for x in content_pan]

    # Read all tilt angles to array
    with open("temp_tilt.txt", "r") as lines:
        content_tilt = lines.readlines()
    content_tilt = [x.strip() for x in content_tilt]

    # Make a dictionary with the temperatures for look-up
    angles_tilt = getTimestampedDictionary(content_tilt, 0)

    # Combine pan and tilt together based on the timestamp
    file_combined = open(file_output, "w")
    # Add custom headers
    file_combined.write("Timestamp panAngleDegrees tiltAngleDegrees\n")
    for pan in content_pan:
        # Required because of the log file headers
        try:
            timestamp_pan, angle_pan = pan.split(" ")
            if not timestamp_pan in angles_tilt:
                raise LookupError("Could not find pan and tilt angle combination!")
            timestamp_tilt, angle_tilt = angles_tilt[timestamp_pan].split(" ")
            # Timestamp extracted from the log needs further processing 
            timeFormated = formatTime(float(timestamp_pan.replace(".","")) / 1000000.0)
            file_combined.write("%s %f %f\n" % (timeFormated, float(angle_pan), float(angle_tilt)))
        except ValueError:
            # Skip the header
            continue            
        except Exception as e:
            # Detect unmatched samples
            print type(e).__name__, e
            continue

    file_combined.close()

    # Remove the temporary separated pan and tilt files
    os.remove("temp_pan.txt")
    os.remove("temp_tilt.txt")
    showTime("PTU", start_time)


def delogGPS(file_input, file_output):
    print "Delogging GPS from %s to %s" % (file_input, file_output)
    start_time = time.time()

    file_gps_raw = open("temp_gps.txt", "w")
    subprocess.call(["pocolog", file_input, "-s", "/gps.raw_data"], stdout = file_gps_raw)
    file_gps_raw.close()

    # Read all GPS data to an array
    with open("temp_gps.txt", "r") as lines:
        content_gps = lines.readlines()
    content_gps = [x.strip() for x in content_gps]

    file_gps = open(file_output, "w")
    # Add custom headers
    file_gps.write("Timestamp signalQuality latitudeDegrees longitudeDegrees altitudeMeters latitudeStandardDeviationMeters longitudeStandardDeviationMeters altitudeStandardDeviationMeters\n")
    for gps in content_gps:
        try:
            timestamp, latitude, longitude, signal, satellites, altitude, geoidalSeparation, ageOfDifferentialCorrections, deviationLatitude, deviationLongitude, deviationAltitude = gps.split(" ")

            timeFormated = formatTime(float(timestamp) / 1000000.0)
            file_gps.write("%s %s %s %s %.3f %.3f %.3f %.3f\n" % (timeFormated, signal, latitude, longitude, float(altitude), float(deviationLatitude), float(deviationLongitude), float(deviationAltitude)))
        except Exception as e:
            # Skip the header
            continue

    file_gps.close()

    # Remove the temporary GPS file
    os.remove("temp_gps.txt")
    showTime("GPS", start_time)


def delogIMU(file_input, file_output):
    print "Delogging IMU from %s to %s" % (file_input, file_output)
    start_time = time.time()

    file_imu = open("temp_imu.txt", "w")
    subprocess.call(["pocolog", file_input, "-s", "/imu_stim300.inertial_sensors_out"], stdout = file_imu)
    file_imu.close()

    # Read all IMU data to an array
    with open("temp_imu.txt", "r") as lines:
        content_imu = lines.readlines()
    content_imu = [x.strip() for x in content_imu]

    file_imu = open(file_output, "w")
    # Add custom headers
    file_imu.write("Timestamp accelerationXm/s^2 accelerationYm/s^2 accelerationZm/s^2 angularVelocityXrad/s angularVelocityYrad/s angularVelocityZrad/s inclinometerAccXm/s^2 inclinometerAccYm/s^2 inclinometerAccZm/s^2\n")
    for imu in content_imu:
        try:
            timestamp, accX, accY, accZ, gyroX, gyroY, gyroZ, incX, incY, incZ = imu.split(" ")
            timeFormated = formatTime(float(timestamp) / 1000000.0)
            file_imu.write("%s %s %s %s %s %s %s %s %s %s\n" % (timeFormated, accX, accY, accZ, gyroX, gyroY, gyroZ, incX, incY, incZ))
        except ValueError:
            # Skip the header
            continue
        except Exception as e:
            # Detect unmatched samples
            print type(e).__name__, e
            continue

    file_imu.close()

    # Remove the temporary file
    os.remove("temp_imu.txt")
    showTime("IMU", start_time)


def delogIMUTemperatures(file_input, file_output):
    print "Delogging IMU temperatures from %s to %s" % (file_input, file_output)
    start_time = time.time()

    # Delog the tilt angle
    file_imu_temperature = open("temp_imu_temperature.txt", "w")
    subprocess.call(["pocolog", file_input, "-s", "/imu_stim300.temp_sensors_out"], stdout = file_imu_temperature)
    file_imu_temperature.close()

    # Read all pan angles to array
    with open("temp_imu_temperature.txt", "r") as lines:
        content_imu_temperature = lines.readlines()
    content_imu_temperature = [x.strip() for x in content_imu_temperature]

    file_imu_temperature = open(file_output, "w")
    # Add custom headers
    file_imu_temperature.write("timestamp temperatureAccXKelvin temperatureAccYKelvin temperatureAccZKelvin temperatureGyroXKelvin temperatureGyroYKelvin temperatureGyroZKelvin temperatureIncXKelvin temperatureIncYKelvin temperatureIncZKelvin\n")
    for imu_temperature in content_imu_temperature:
        try:
            timestamp, tempAccX, tempAccY, tempAccZ, tempGyroX, tempGyroY, tempGyroZ, tempIncX, tempIncY, tempIncZ = imu_temperature.split(" ")
            timeFormated = formatTime(float(timestamp) / 1000000.0)
            file_imu_temperature.write("%s %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.3f\n" % (timeFormated, float(tempAccX), float(tempAccY), float(tempAccZ), float(tempGyroX), float(tempGyroY), float(tempGyroZ), float(tempIncX), float(tempIncY), float(tempIncZ)))
        except ValueError:
            # Skip the header
            continue            
        except Exception as e:
            # Detect unmatched samples
            print type(e).__name__, e
            continue

    file_imu_temperature.close()

    # Remove the temporary file
    os.remove("temp_imu_temperature.txt")
    showTime("IMU temperature", start_time)


def delogOdometry(file_input, file_output):
    print "Delogging odometry from %s to %s" % (file_input, file_output)
    start_time = time.time()

    file_odometry = open("temp_odometry.txt", "w")
    subprocess.call(["pocolog", file_input, "-s", "/platform_driver.joints_readings"], stdout = file_odometry)
    file_odometry.close()

    # Read all odometry data to an array
    with open("temp_odometry.txt", "r") as lines:
        content_odometry = lines.readlines()
    content_odometry = [x.strip() for x in content_odometry]

    file_odometry = open(file_output, "w")
    # Add custom headers
    file_odometry.write("timestamp driveAngleFrontLeftRad driveAngleFrontRightRad driveAngleCenterLeftRad driveAngleCenterRightRad driveAngleBackLeftRad driveAngleBackLeftRad steerAngleFrontLeftRad steerAngleFrontRightRad steerAngleBackLeftRad steerAngleBackLeftRad rockerLeftRad rockerRightRad bogieLeftRad bogieRightRad\n")
    for odometry in content_odometry:
        try:
            # Remove the ASCII names of the elements
            data = odometry.split(" ")
            data = data[184:]
            data = " ".join(data)

            fl_angle, fl_speed, fl_effort, fl_current, fl_acc,\
            fr_angle, fr_speed, fr_effort, fr_current, fr_acc,\
            cl_angle, cl_speed, cl_effort, cl_current, cl_acc,\
            cr_angle, cr_speed, cr_effort, cr_current, cr_acc,\
            bl_angle, bl_speed, bl_effort, bl_current, bl_acc,\
            br_angle, br_speed, br_effort, br_current, br_acc,\
            sfl_angle, sfl_speed, sfl_effort, sfl_current, sfl_acc,\
            sfr_angle, sfr_speed, sfr_effort, sfr_current, sfr_acc,\
            sbl_angle, sbl_speed, sbl_effort, sbl_current, sbl_acc,\
            sbr_angle, sbr_speed, sbr_effort, sbr_current, sbr_acc,\
            rockl_angle, rockl_speed, rockl_effort, rockl_current, rockl_acc,\
            rockr_angle, rockr_speed, rockr_effort, rockr_current, rockr_acc,\
            bogl_angle, bogl_speed, bogl_effort, bogl_current, bogl_acc,\
            bogr_angle, bogr_speed, bogr_effort, bogr_current, bogr_acc,\
            timestamp = data.split(" ")

            timeFormated = formatTime(float(timestamp) / 1000000.0)
            file_odometry.write("%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n" % (timeFormated, fl_angle, fr_angle, cl_angle, cr_angle, bl_angle, br_angle, sfl_angle, sfr_angle, sbl_angle, sbr_angle, rockl_angle, rockr_angle, bogl_angle, bogr_angle))
        except Exception as e:
            # Skip the header
            continue

    file_odometry.close()

    # Remove the temporary GPS file
    os.remove("temp_odometry.txt")
    showTime("Odometry", start_time)


def delogGyro(file_input, file_output):
    print "Delogging gyro from %s to %s" % (file_input, file_output)
    start_time = time.time()

    file_gyro = open("temp_gyro.txt", "w")
    subprocess.call(["pocolog", file_input, "-s", "/dsp1760.rotation_raw"], stdout = file_gyro)
    file_gyro.close()

    # Read all odometry data to an array
    with open("temp_gyro.txt", "r") as lines:
        content_gyro = lines.readlines()
    content_gyro = [x.strip() for x in content_gyro]

    file_gyro = open(file_output, "w")
    # Add custom headers
    file_gyro.write("timestamp angularVelocityZrad/s\n")
    for gyro in content_gyro:
        try:
            # Remove the ASCII names of the elements
            timestamp, accX, accY, accZ, gyroX, gyroY, gyroZ, incX, incY, incZ = gyro.split(" ")
            timeFormated = formatTime(float(timestamp) / 1000000.0)
            file_gyro.write("%s %s\n" % (timeFormated, gyroZ))
        except Exception as e:
            # Skip the header
            continue

    file_gyro.close()

    # Remove the temporary GPS file
    os.remove("temp_gyro.txt")
    showTime("Gyro", start_time)


def delogGyroTemperatures(file_input, file_output):
    print "Delogging gyro temperatures from %s to %s" % (file_input, file_output)
    start_time = time.time()

    file_gyro_temperature = open("temp_gyro_temperature.txt", "w")
    subprocess.call(["pocolog", file_input, "-s", "/dsp1760.temperature", "-t"], stdout = file_gyro_temperature)
    file_gyro_temperature.close()

    # Read all odometry data to an array
    with open("temp_gyro_temperature.txt", "r") as lines:
        content_gyro_temperature = lines.readlines()
    content_gyro_temperature = [x.strip() for x in content_gyro_temperature]

    file_gyro_temperature = open(file_output, "w")
    # Add custom headers
    file_gyro_temperature.write("timestamp temperatureCelsius\n")
    for gyro_temperature in content_gyro_temperature:
        try:
            # Remove the ASCII names of the elements
            timestamp, temperature = gyro_temperature.split(" ")
            timeFormated = formatTime(float(timestamp.replace(".","")) / 1000000.0)
            file_gyro_temperature.write("%s %.3f\n" % (timeFormated, float(temperature)))
        except Exception as e:
            # Skip the header
            continue

    file_gyro_temperature.close()

    # Remove the temporary GPS file
    os.remove("temp_gyro_temperature.txt")
    showTime("Gyro temperature", start_time)

def delogCamera(file_input, folder_output, stream_name, name_structure):
    print "Delogging camera from %s to %s" % (file_input, folder_output)
    start_time = time.time()

    # Get the absolute path as "rock-export" script requires it
    file_input = os.path.abspath(file_input)

    try:
        os.mkdir(folder_output)
    except:
        # Ignore error if the folder already exists (thread safe this way)
        pass

    # Redirect output to /dev/null, change the working directory to folder_output so images will be exported there
    FNULL = open(os.devnull, 'w')
    process = subprocess.Popen(["rock-export", file_input, "--stream", stream_name, "--filename", name_structure + ".png"], stdout = FNULL, cwd = folder_output)
    # Wait process to finish before showing the elapsed time
    process.communicate()

    showTime(file_input, start_time)

def delogAll(input_path, output_path):
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    start_time = time.time()

    # Start a thread for every item

    t1 = DelogThread(delogPanCamPTU, input_path + "/pancam.log", output_path + "/ptu-panorama.txt", "/pancam_panorama.pan_angle_out_degrees", "/pancam_panorama.tilt_angle_out_degrees")
    t1.start()

    # See below for t2

    t3 = DelogThread(delogGPS, input_path + "/waypoint_navigation.log", output_path + "/gps.txt")
    t3.start()

    t4 = DelogThread(delogIMU, input_path + "/imu.log", output_path + "/imu.txt")
    t4.start()

    t5 = DelogThread(delogIMUTemperatures, input_path + "/imu.log", output_path + "/imu_temperature.txt")
    t5.start()

    t6 = DelogThread(delogOdometry, input_path + "/control.log", output_path + "/odometry.txt")
    t6.start()

    t7 = DelogThread(delogGyro, input_path + "/gyro.log", output_path + "/gyro.txt")
    t7.start()

    t8 = DelogThread(delogGyroTemperatures, input_path + "/gyro.log", output_path + "/gyro_temperature.txt")
    t8.start()

    t9 = DelogThread(delogCamera, input_path + "/pancam.log", output_path + "/PanCam_360", "/pancam_360.left_frame_out", "PanCam_360_#TIME_L")
    t9.start()

    t10 = DelogThread(delogCamera, input_path + "/pancam.log", output_path + "/PanCam_360", "/pancam_360.right_frame_out", "PanCam_360_#TIME_R")
    t10.start()

    t11 = DelogThread(delogCamera, input_path + "/pancam.log", output_path + "/PanCam_panorama", "/pancam_panorama.left_frame_out", "PanCam_panorama_#TIME_L")
    t11.start()

    t12 = DelogThread(delogCamera, input_path + "/pancam.log", output_path + "/PanCam_panorama", "/pancam_panorama.right_frame_out", "PanCam_panorama_#TIME_R")
    t12.start()

    t13 = DelogThread(delogCamera, input_path + "/tof.log", output_path + "/ToF", "/tofcamera_mesasr.ir_frame", "ToF_#TIME_intensity")
    t13.start()

    t14 = DelogThread(delogCamera, input_path + "/tof.log", output_path + "/ToF", "/tofcamera_mesasr.distance_frame", "ToF_#TIME_range")
    t14.start()

    t15 = DelogThread(delogCamera, input_path + "/lidar.log", output_path + "/Velodyne", "/velodyne_lidar.azimuth_frame", "Velodyne_#TIME_azimuth")
    t15.start()

    t16 = DelogThread(delogCamera, input_path + "/lidar.log", output_path + "/Velodyne", "/velodyne_lidar.ir_frame", "Velodyne_#TIME_intensity")
    t16.start()

    t17 = DelogThread(delogCamera, input_path + "/lidar.log", output_path + "/Velodyne", "/velodyne_lidar.range_frame", "Velodyne_#TIME_range")
    t17.start()

    # Deinterlace the BB2 and BB3 cameras before exporting the images
    tbb2 = DelogThread(runRubyScript, "deinterlace_bb2.rb", input_path)
    tbb2.start()

    tbb3 = DelogThread(runRubyScript, "deinterlace_bb3.rb", input_path)
    tbb3.start()

    t1.join()

    # t1 must finish before t2 starts as it uses the same temporary file (but it is fast)
    t2 = DelogThread(delogPanCamPTU, input_path + "/pancam.log", output_path + "/ptu-360.txt", "/pancam_360.pan_angle_out_degrees", "/pancam_360.tilt_angle_out_degrees")
    t2.start()

    # Wait for the threads to finish
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    t8.join()
    t9.join()
    t10.join()
    t11.join()
    t12.join()
    t13.join()
    t14.join()
    t15.join()
    t16.join()
    t17.join()

    tbb2.join()

    # BB2 delogging

    t18 = DelogThread(delogCamera, input_path + "/bb2_deinterlaced.log", output_path + "/HazCam", "/camera_bb2.left_frame", "HazCam_#TIME_L")
    t18.start()

    t19 = DelogThread(delogCamera, input_path + "/bb2_deinterlaced.log", output_path + "/HazCam", "/camera_bb2.right_frame", "HazCam_#TIME_R")
    t19.start()

    tbb3.join()

    # BB3 delogging

    t20 = DelogThread(delogCamera, input_path + "/bb3_deinterlaced.log", output_path + "/LocCam", "/camera_bb3.left_frame", "LocCam_#TIME_L")
    t20.start()

    t21 = DelogThread(delogCamera, input_path + "/bb3_deinterlaced.log", output_path + "/LocCam", "/camera_bb3.center_frame", "LocCam_#TIME_C")
    t21.start()

    t22 = DelogThread(delogCamera, input_path + "/bb3_deinterlaced.log", output_path + "/LocCam", "/camera_bb3.right_frame", "LocCam_#TIME_R")
    t22.start()

    t18.join()
    t19.join()
    t20.join()
    t21.join()
    t22.join()

    showTime("All", start_time)

if __name__ == "__main__":
    # Delog all dataset, must provide absolute paths
    delogAll("/home/marta/20170509-1524", "/media/marta/HDPR/20170509-1524")

