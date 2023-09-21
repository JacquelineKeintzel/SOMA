"""
Script for analysing synchronisation of BPMs from phase data (output from measure_optics.py).
This script outputs a text file discribing the number of turns each BPM is out of synch by.

"""
from __future__ import print_function
import sys
import os
import numpy as np
import argparse
from func import read_phase, read_phasetot, read_bpms

# Argument parser.
parser = argparse.ArgumentParser()
parser.add_argument('--phase_output_dir', '-pod', dest="pod", action="store")
parser.add_argument('--async_output_dir', '-aod', dest="aod", action="store")
parser.add_argument('--axis', '-ax', dest="axis", choices = ('x', 'y') ,action="store")
parser.add_argument('--ring', '-r', dest="ring", choices = ('her', 'ler'), action="store")
parser.add_argument('--sdds', '-s', dest="sdds", action="store")
args = parser.parse_args()


# Check if phase output directory exists, if not, exit.
if not os.path.exists(args.pod):
    print("Directory", args.pod, "not found.")
    sys.exit()
# Check if output dir for the present script exists, if not, create one.
if not os.path.exists(args.aod):
    os.system("mkdir " + args.aod)

# Check for asynchronous BPMs in each measurement reun using phase output.
for count, run in enumerate(os.listdir(args.pod)):
    datapath = os.path.join(args.pod, run)
    # try:
        # S, names, deltaph, phx, phxmdl, Qx, Qy = phase(datapath, args.axis)
    # except IOError:
    #     continue

    namesmdl = read_bpms(args.sdds)
    names, Qx, Qy = read_phase(datapath, args.axis)
    deltaphtot = read_phasetot(datapath, args.axis)
    
    level = []
    deltaQ = 0.90
    deltaQ2 = 0.10 

    tune = (1.-Qx) if args.axis == 'x' else (1.-Qy)
    #tune = (Qx) if args.axis == 'x' else (Qy)
    j=0
    i=0
    while j < len(namesmdl):
        try:
            if namesmdl[j] == names[i]:
                if deltaphtot[i] / tune >= deltaQ:
                    level.append('-1') if args.ring == 'her' else level.append('+1') 
                elif deltaphtot[i] / tune <= -deltaQ:
                    level.append('+1') if args.ring == 'her' else level.append('-1')
                elif deltaphtot[i] / tune >= (deltaQ-deltaQ2):
                    level.append('-1') if args.ring == 'her' else level.append('+1') 
                elif deltaphtot[i] / tune <= -(deltaQ-deltaQ2):
                    level.append('+1') if args.ring == 'her' else level.append('-1')
                elif deltaphtot[i] / tune >= deltaQ2: 
                    level.append('+2') if args.ring == 'her' else  level.append('-2')
                elif deltaphtot[i] / tune <= -deltaQ2: 
                    level.append('-2') if args.ring == 'her' else level.append('+2')
                else:
                    level.append('0')
            else:
                level.append('u')
                i=i-1
            i=i+1
            j=j+1
        except IndexError:
            break
    #print('\n')                
    while len(level) < len(namesmdl): level.append('0')

    for i in range(len(level)):
        if 1 < i < len(level)-1:
            if (level[i-1] == level[i+1]) != 'u' : 
                if level[i] == 'u': level[i] = level[i-1]
            else: level[i] = '0'
    
    for i in range(len(level)):
        if level[i] == 'u': level[i]='0'
    #print(level)
    file = open(args.aod + run + '.txt', 'w')
    file.write('{\n')

    # try:
    for i in range(len(level)):
        file.write('"' + namesmdl[i] + '"->' + level[i] + ',\n')
    file.write('}')
    # except IndexError:
        # print(run)
    file.close()
    # quit()

sys.exit()
