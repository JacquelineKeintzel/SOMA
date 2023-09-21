
"""
Script to plot histograms of beta-beating before and after
BPM calibration.
"""

from __future__ import print_function
from optparse import OptionParser
import matplotlib.pyplot as plt
import os
import numpy as np
from func import read_bet_phase, read_bet_amp


if __name__ == "__main__":

    fix = 10
    fiy = 4.5
    size = 20

    parser = OptionParser()
    parser.add_option("-s", "--sdds",  dest="sdds", help="Folder of sdds files.", action="store")
    parser.add_option("-o", "--phase",  dest="phase", help="Folder of phase output files.", action="store")
    parser.add_option("-a", "--axis",  dest="axis", help="Transverse plane, either x or y.", action="store")
    parser.add_option("-w", "--when",  dest="when", help="Before or after calibration.", action="store")
    parser.add_option("-p", "--pngpdf",  dest="pngpdf", help="Format of plot.", action="store")
    (options, args) = parser.parse_args()


    all_sdds = [sd for sd in os.listdir(options.sdds) if 'sdds' in sd]

    beat = []
    for sdds in all_sdds:
        folder = os.path.join(options.phase, sdds)

        beta_phase, beta_phase_err, bpms = read_bet_phase(folder, options.axis)
        beta_amp, beta_amp_err = read_bet_amp(folder, options.axis)

        beat = beat + [100*(beta_amp[i] - beta_phase[i])/beta_phase[i] for i in range(len(beta_phase)) if abs(100*(beta_amp[i] - beta_phase[i])/beta_phase[i]) <= 250 ] 

    av = np.mean(beat)

    plt.figure(figsize=(fix, fiy))
    n, bins, patches  = plt.hist(beat, bins=200)
    plt.plot(np.array([av,av]), np.array([0,max(n)]), ls='--', color = 'grey', lw = 2)
    plt.ylim(0, max(n))
    plt.tick_params('both', labelsize=size)
    if options.axis == 'x': plt.xlabel(r'$(\beta_{x, amp}-\beta_{x, ph}) / \beta_{x, ph}$ [%]', fontsize=size)
    else: plt.xlabel(r'$(\beta_{y, amp}-\beta_{y, ph}) / \beta_{y, ph}$ [%]', fontsize=size)
    plt.ylabel('Counts', fontsize=size)
    plt.tight_layout()
    plt.savefig(options.sdds+'../BPMcalib_'+options.when+'_'+options.axis+'.'+options.pngpdf)
    plt.close()
