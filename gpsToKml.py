# Script to convert recorded GPS coordinates to KML path.
#
# Get the gps coordinates of your logged run via
# pocolog waypoint_navigation.log -s /gps.raw_data --fields latitude,longitude,altitude > gps_data
# and find that data file, when this script's dialog asks for it
__author__ = "Levin Gerdes"

# For Open File dialog
# sudo apt-get install python-tk
import Tkinter as tk
import tkFileDialog

skeletonUpper = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Paths</name>
    <description>GPS coordinates from rover traverse</description>
    <Style id="yellowLineGreenPoly">
      <LineStyle>
        <color>7f00ffff</color>
        <width>4</width>
      </LineStyle>
      <PolyStyle>
        <color>7f00ff00</color>
      </PolyStyle>
    </Style>
    <Placemark>
      <name>Absolute Extruded</name>
      <description>Transparent green wall with yellow outlines</description>
      <styleUrl>#yellowLineGreenPoly</styleUrl>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>absolute</altitudeMode>
        <coordinates>
"""
skeletonLower = """        </coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>
"""

# get path to gps data file
root = tk.Tk()
root.withdraw()
file_path = tkFileDialog.askopenfilename()

# read contents
f = open(file_path, 'r')
lines = f.readlines()[2:] # ignore the two header lines
f.close()

# split into longitude, latitude, altitude
coordinates = [l.split() for l in lines]
# swap longitude with latitude and indent
coordinates = ["          "+crds[1]+","+crds[0]+","+crds[2]+"\n" for crds in coordinates]
coordinates = ''.join(coordinates)

# save results
kmlContent = skeletonUpper + coordinates + skeletonLower

f = open('gps_path.kml', 'w')
f.write(kmlContent)
f.close()
