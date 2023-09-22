"""
Main script which allows the user to utilise desired
functions of this analysis package.
"""
from __future__ import print_function
import argparse
import os
import sys

from func import read_parameters, sdds_conv, harmonic_analysis, optics_analysis, asynch_analysis
from func import asynch_cmap, bpm_calibration, calib_hist, freq_spec, chromatic_analysis
from func import plot_optics, coupling_analysis, sdds_turns, cut_large_sdds

parser = argparse.ArgumentParser()
required = parser.add_argument_group('required arguments')
required.add_argument('--parameters',
                    action='store',
                    dest='parameters',
                    help='Path to parameters.txt file, which contains all other paths necessary for this script.')


parser.add_argument('--all_files', '-all',
                    action='store_true',
                    help='To be used when all files should run at once, e.g. for dispersion measurement with off-momentum files.')
parser.add_argument('--harmonic1', '-h1',
                    action='store_true',
                    help='Harmonic analysis without knowledge of BPM synch. This is enough to obtain tunes.')
parser.add_argument('--plotsdds1', '-ps1',
                    action='store_true',
                    help='Plotting of raw sdds files.')        
parser.add_argument('--plotfreq1', '-pf1',
                    action='store_true',
                    help='Plotting of frequency spectrum.')
parser.add_argument('--optics1', '-o1',
                    action='store_true',
                    help='Optics analysis of harmonic1 output without BPM synch knowledge.')
parser.add_argument('--plotasynch1', '-pa1',
                    action='store_true',
                    help='Plotting of BPM synchronisation from optics1 output, before synch fix is applied.')
parser.add_argument('--asynch', '-aa',
                    action='store_true',
                    help='Analysis of BPM synchronisation from optics1 output.')
parser.add_argument('--harmonic2', '-h2',
                    action='store_true',
                    help='sdds conversion and harmonic analysis with knowledge of BPM synch.')
parser.add_argument('--plotsdds2', '-ps2',
                    action='store_true',
                    help='Plotting of synchronized sdds files.')     
parser.add_argument('--plotfreq2', '-pf2',
                    action='store_true',
                    help='Plotting of frequency spectrum after synchronization.')   
parser.add_argument('--optics2', '-o2',
                    action='store_true',
                    help='Optics analysis of harmonic2 output with knowledge of BPM synch.')
parser.add_argument('--plotoptics2', '-po2',
                    action='store_true',
                    help='Plots the optics repository after BPM synchronisation.')
parser.add_argument('--plotasynch2', '-pa2',
                    action='store_true',
                    help='Plotting of BPM synchronisation from optics2 output, after synch fix is applied.')
parser.add_argument('--calib', '-c',
                    action='store_true',
                    help='Estimates the BPM calibration (beta from phase vs amplitude) for this measurement.')
parser.add_argument('--optics3', '-o3',
                    action='store_true',
                    help='Optics analysis of harmonic3 output with estimate of BPM calibration.')
parser.add_argument('--plotoptics3', '-po3',
                    action='store_true',
                    help='Plots the optics repository after BPM calibration.')
parser.add_argument('--plotcalib1', '-pc1',
                    action='store_true',
                    help='Plotting of BPM calibration from optics2 output, before calibration is applied.')
parser.add_argument('--plotcalib2', '-pc2',
                    action='store_true',
                    help='Plotting of BPM calibration from optics3 output, after calibration is applied.')
parser.add_argument('--omc3', '-omc3',
                    action='store_true',
                    help='Use OMC3/python3 instead of BetaBeat.src/python2.')
args = parser.parse_args()

# Read in destinations
parameters = read_parameters(args.parameters)

# Inputs from study
nturns = parameters["nturns"]
ringID = parameters["ringID"].lower()
lattice = parameters["lattice"]
input_data = parameters["input_data_path"]
kickax = parameters["kickax"]

# For BetaBeat.src
model_path = parameters["model_path"]

# For present code
main_output = parameters["main_output_path"]
if not os.path.exists(main_output):
    os.system('mkdir ' + main_output)
else:
    pass
unsynched_sdds = os.path.join(main_output, 'unsynched_sdds/')
synched_sdds = os.path.join(main_output, 'synched_sdds/')
file_dict = parameters["file_dict"]

# Executables
gsad = parameters["gsad"]

# Output directories
unsynched_harmonic_output = os.path.join(main_output, 'unsynched_harmonic/')
unsynched_optics_output = os.path.join(main_output, 'unsynched_optics/')
synched_harmonic_output = os.path.join(main_output, 'synched_harmonic/')
synched_optics_output = os.path.join(main_output, 'synched_optics/')
calibrated_harmonic_output = os.path.join(main_output, 'calibrated_harmonic/')
calibrated_optics_output = os.path.join(main_output, 'calibrated_optics/')


if args.omc3 == True:
    py_version = 3
    python_exe = parameters["python3_exe"]
    BetaBeatsrc_path = parameters["omc3_path"]
else: 
    py_version = 2
    python_exe = parameters["python_exe"]
    BetaBeatsrc_path = parameters["BetaBeatsrc_path"]



# First conversion and harmonic analysis 1
if args.harmonic1 == True:
    sdds_conv(input_data, file_dict, main_output, unsynched_sdds,
              lattice, gsad, ringID, kickax, asynch_info=False)

    cut_large_sdds(python_exe, unsynched_sdds)

    harmonic_analysis(py_version, python_exe, BetaBeatsrc_path, model_path,
                      unsynched_harmonic_output, unsynched_sdds,
                      nturns, str(0.04), lattice, gsad)
else: pass


if args.plotsdds1 == True:
    sdds_turns(python_exe, unsynched_sdds)
else: pass

if args.plotfreq1 == True:
    freq_spec(python_exe, unsynched_sdds, model_path)
else: pass


# Optics analysis 1, before synchronization
if args.optics1 == True:
    optics_analysis(py_version, python_exe, BetaBeatsrc_path, model_path,
                   unsynched_harmonic_output, unsynched_optics_output, unsynched_sdds, 
                   ringID, args.all_files)
    try: chromatic_analysis(model_path, unsynched_optics_output)         
    except: pass
else: pass


# Asynch analysis
if args.asynch == True:
    asynch_analysis(python_exe, unsynched_optics_output, main_output, model_path, ringID)
else: pass


# Plotting BPM synchronisation pre-fix
if args.plotasynch1 == True:
    asynch_cmap(python_exe, unsynched_sdds, unsynched_optics_output, when='before')
else: pass


# Second sdds conversion (with knowledge of BPM synch) and harmonic analysis 2
if args.harmonic2 == True:
    # sdds_conv(input_data, file_dict, main_output, synched_sdds,
    #           lattice, gsad, ringID, kickax, asynch_info=True)

    cut_large_sdds(python_exe, synched_sdds)

    harmonic_analysis(py_version, python_exe, BetaBeatsrc_path, model_path,
                      synched_harmonic_output, synched_sdds,
                      nturns, str(0.04), lattice, gsad)
else: pass

if args.plotsdds2 == True:
    sdds_turns(python_exe, synched_sdds)
else: pass

if args.plotfreq2 == True:
    freq_spec(python_exe, synched_sdds, model_path)
else: pass

# Phase analysis 2
if args.optics2 == True:
    optics_analysis(py_version, python_exe, BetaBeatsrc_path, model_path,
                   synched_harmonic_output, synched_optics_output, synched_sdds, 
                   ringID, args.all_files)
    try: chromatic_analysis(model_path, synched_optics_output)    
    except: pass
    try: coupling_analysis(model_path, synched_sdds, synched_harmonic_output, synched_optics_output, args.all_files)
    except: pass
else: pass

if args.plotoptics2 == True:
    plot_optics(python_exe, synched_optics_output, model_path, ringID)
else: pass


# Plotting BPM synchronisation post-fix
if args.plotasynch2 == True:
    asynch_cmap(python_exe, synched_sdds, synched_optics_output, when='after')
else: pass


# Plotting BPM calibration pre-calib
if args.plotcalib1 == True:
    calib_hist(python_exe, synched_sdds, synched_optics_output, when='before')
else: pass


# Calculation of BPM calibration and writing lin files and calib harmonic folder
if args.calib == True:
    bpm_calibration(python_exe, synched_sdds, ringID)
else: pass


# Phase analysis 3, with calibrated BPMs
if args.optics3 == True:
    optics_analysis(py_version, python_exe, BetaBeatsrc_path, model_path,
                   calibrated_harmonic_output, calibrated_optics_output, synched_sdds, 
                   ringID, args.all_files)
    try: chromatic_analysis(model_path, calibrated_optics_output)
    except: pass
else: pass

if args.plotoptics3 == True:
    plot_optics(python_exe, calibrated_optics_output, model_path, ringID)
else: pass

# Plotting BPM calibration post-calib
if args.plotcalib2 == True:
    calib_hist(python_exe, synched_sdds, calibrated_optics_output, when='after')
else: pass


print(" ********************************************\n",
        "Everything comes to an end at some point...\n",
        "SuperKEKB Optics Measurements Analysis ends.\n",
        "********************************************")


