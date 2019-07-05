# Visualization
Folder containing scripts for visualization purposes, i.e. for graphically representing
data collected during experiments, software diagrams, etc.

## comptime_visualizer
This script plots computational time samples collected during experimental tests.

Authors:
 - [J. Ricardo Sánchez Ibáñez](https://github.com/Ryk-San) (University of Málaga - ricardosan@uma.es)

## rock2dot

Script to create a dot graph of the connections defined in a rock ruby file.

Usage:
```
python rock2dot.py <ruby-script> <output-file.dot>
```


To convert the dot file to an svg image use:
```
dot -Tsvg <dot-file.dot> -o <image.svg>
```
Other image formats like png are possible as well. For this check the documentation of graphviz:
https://www.graphviz.org/doc/info/output.html

Authors:

 - [Moritz Schilling](https://github.com/m0rsch1), DFKI

 - [Max Ehrhardt](https://github.com/maxehrhardt), ESA

 - [Levin Gerdes](https://github.com/levingerdes), ESA
