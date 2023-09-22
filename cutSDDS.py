"""
Script to cut too long sdds file into smaller one by reducing turn number.

Author: Jacqueline Keintzel
Date: 27/11/2019
"""

from __future__ import print_function
from optparse import OptionParser
import numpy as np 
import sys
import os


parser = OptionParser()
parser.add_option("-f", "--file",  dest="file", help="Path to ASCII SKEKB SDDS file.", action="store")
parser.add_option("-o", "--output",  dest="output", help="Path folder where the cut file will be stored.", action="store")
parser.add_option("-s", "--start",  dest="start", help="Start turn number of smaller SDDS file.", action="store", type=int)
parser.add_option("-e", "--end",  dest="end", help="End turn number of smaller SDDS file.", action="store", type=int)
(options, args) = parser.parse_args()


with open(options.file) as fo:
    lines = fo.readlines()
fo.close()
header = [lin for lin in lines if '#' in lin]
header.insert(4, '# cut set from turns: \t '+str(options.start)+' \t '+str(options.end)+' \n' )
header.insert(11, '# - SDDS cutter written by Jacqueline Keintzel (27/11/2019) \n')
orbits = [lin for lin in lines if not '#' in lin]
end = (len(orbits[0].split()))-5 if options.end > len(orbits[0].split()) else options.end 
cut = [(orbits[i].split()[:3] + orbits[i].split()[options.start+3 : end+3] + ['0', '0', '\n'] ) for i in range(len(orbits))]

cut_file_name = options.file[-28:-5]+'_cut_'+str(options.start)+'_'+str(options.end)+'.sdds'
fc = open(os.path.join(options.output, cut_file_name), 'w')
for i in header: fc.write(str(i))
for i in cut: 
    for j, n in enumerate(i): 
        if j == 0: fc.write(str(n)+' ')
        elif j != len(i)-1: fc.write(str(n)+'\t\t')
        else: fc.write(str(n))

fc.close()
