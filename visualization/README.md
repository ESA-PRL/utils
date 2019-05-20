# rock2dot

Script to create a dot graph of the connections defined in a rock ruby file.

This script is taken and adapted from https://github.com/m0rsch1/rock2dot.

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
