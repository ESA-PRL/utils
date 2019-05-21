#! /usr/bin/env python
#
# Authors:
# Moritz Schilling
# Max Ehrhardt
# Levin Gerdes

import sys

infile, outfile = sys.argv[1], sys.argv[2]
inf,outf = open(infile), open(outfile,"w")

outf.write("digraph \"" + infile + "\" {\n")
outf.write("graph [nodesep=1.5 ranksep=1.0];\n")
outf.write("node [margin=0.2 shape=box];\n")

for line in inf.readlines():
    if "#" not in line:
        if ".connect_to" in line:
            splitted = line.lstrip().replace("\n","").split(".connect_to ")
            sourceSplit = splitted[0].lstrip().split(".")
            targetSplit = splitted[1].lstrip().split(".")
            sourceNode,sourcePort = "\""+sourceSplit[0]+"\"","\""+sourceSplit[1]+""
            targetNode,targetPort = "\""+targetSplit[0]+"\"",""+targetSplit[1]+"\""
            outf.write(sourceNode + " -> " + targetNode + "[ label="+ sourcePort + "\\n" + targetPort + " ];\n")
        if ".log(" in line:
            splitted = line.lstrip().replace("\n","").split(".log(")
            targetNode = splitted[0].lstrip()
            sourceSplit = splitted[1].lstrip().replace(")","").split(".")
            sourceNode,sourcePort = "\""+sourceSplit[0]+"\"","\""+sourceSplit[1]+"\""
            outf.write(sourceNode + " -> " + targetNode + "[ taillabel=" + sourcePort + "\" ];\n")

outf.write("}\n")

inf.close()
outf.close()
