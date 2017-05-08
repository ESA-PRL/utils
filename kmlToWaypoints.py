# Script to convert KML paths to waypoints for HDPR.
#
# Create a path in Google Earth and export it as a KML file.
# Specify the origin (in this script) and finally run this script.
# The resulting waypoints are relative to the origin (in meters).

# KML PARSER
# https://pythonhosted.org/pykml/installation.html
# check that lxml is installed (>>> import lxml )
# install pip (sudo apt-get install python-pip)
# install pykml (sudo pip install pykml)
from pykml import parser

# OPEN FILE DIALOG
# sudo apt-get install python-tk
import Tkinter as tk
import tkFileDialog

# CONVERTER FROM lat/lon TO utm
# https://pypi.python.org/pypi/utm
# sudo pip install utm
import utm


# ORIGIN [utm easting/northing]
originX = 597481.68
originY = 5785983.94


# get path to kml file
root = tk.Tk()
root.withdraw()
file_path = tkFileDialog.askopenfilename()

# parse kml contents
f = open(file_path, 'r')
root = parser.parse(f).getroot()
f.close()

# get coordinates and split into "tuples" of lon,lat,alt
coords = str(root.Document.Placemark.LineString.coordinates).replace("\t","").replace("\n","").split(' ')

xpos = []
ypos = []
for coord in coords[:-1]: # the last entry in coords is ''
    lon,lat,_ = coord.split(',')
    easting,northing,_,_ = utm.from_latlon(float(lat),float(lon))
    xpos.append( easting  - originX )
    ypos.append( northing - originY )


# PRINT RESULTS

# select all points.
# index starts at 1 -> indices[1:];
# and range yields numbers until but excluding its parameter
print("selectedWaypoints: " + str( range(len(xpos)+1)[1:] ) )
print("xpos: "+ str(xpos))
print("ypos: "+ str(ypos))
