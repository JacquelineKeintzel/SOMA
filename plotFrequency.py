"""
Script to plot frequency analysis output.
"""

from __future__ import print_function
from optparse import OptionParser
import numpy as np 
import matplotlib.pyplot as plt
import os
from func import read_bpms
from matplotlib.backends.backend_pdf import PdfPages


def read_spectrum(file, j):
    """
    Reads amps or freqs file and returns all entries.
    """
    vals = []
    with open(file) as fo:
        lines = fo.readlines()[3:]
    fo.close()

    #for j in range(len(lines[0].split())):
    vals = vals + [float(lines[i].split()[j]) for i in range(len(lines))]

    #print(len(vals))
    #quit()
    return np.array(vals)


def get_model_tunes(twiss):
    with open(twiss) as fo:
        lines = fo.readlines()
    Qx = float(lines[9].split()[3]) - np.trunc(float(lines[9].split()[3]))
    Qy = float(lines[10].split()[3]) - np.trunc(float(lines[10].split()[3]))

    return Qx, Qy


def get_harmonic_tunes(linx):
    with open(linx) as fo:
        lines = fo.readlines()
    Q = float(lines[0].split()[3])
    Qnat = float(lines[2].split()[3])
    return Q, Qnat


if __name__ == "__main__":

    fix = 12
    fiy = 4.5
    size = 20
    size2 = 16
    
    parser = OptionParser()
    parser.add_option("-s", "--sdds",  dest="sdds", help="Folder of sdds files, leads to other folders.", action="store")
    parser.add_option("-m", "--model",  dest="model", help="Model folder to get the twiss model for the tunes.", action="store")
    parser.add_option("-a", "--axis",  dest="axis", help="Transverse plane, either x or y.", action="store")
    parser.add_option("-p", "--pngpdf",  dest="pngpdf", help="Format of plot.", action="store")
    (options, args) = parser.parse_args()

    all_sdds = [sd for sd in os.listdir(options.sdds) if 'sdds' in sd]
    harmonic_output = os.path.join(options.sdds[:-15], 'unsynched_harmonic_output')
    model = os.path.join(options.model, 'twiss.dat')
    Qx, Qy = get_model_tunes(model)
    
    all_bpms=read_bpms(os.path.join(options.sdds, all_sdds[0]))
    # print(all_sdds)
    # quit()
    for sdds in all_sdds:
        Q_x, Q_x_nat = get_harmonic_tunes(os.path.join(harmonic_output, sdds+'.linx'))
        Q_y, Q_y_nat = get_harmonic_tunes(os.path.join(harmonic_output, sdds+'.liny'))
        print(sdds)
        #print(os.path.join(harmonic_output, str(sdds)+'_FreqPlot.pdf'))
        #quit()
        with PdfPages(os.path.join(harmonic_output, str(sdds[:-5])+'_FreqPlot.pdf')) as pdf:
            with open(os.path.join(harmonic_output, sdds+'.ampsx')) as fo:
                lines = fo.readlines()
            fo.close() 
            with open(os.path.join(harmonic_output, sdds+'.ampsy')) as fy:
                linesy = fy.readlines()
            fy.close()  

            bpmsx = lines[1].split()[1:]    
            bpmsy = linesy[1].split()[1:]        
            lines = lines[3:]

            for bpm in all_bpms:
                print(bpm)
                if (bpm in bpmsx) and (bpm in bpmsy):
                    indx = bpmsx.index(bpm) 
                    indy = bpmsy.index(bpm)

                    ampx = read_spectrum(os.path.join(harmonic_output, sdds+'.ampsx'), indx)
                    freqx = read_spectrum(os.path.join(harmonic_output, sdds+'.freqsx'), indx)
                    ampy = read_spectrum(os.path.join(harmonic_output, sdds+'.ampsy'), indy)
                    freqy = read_spectrum(os.path.join(harmonic_output, sdds+'.freqsy'), indy)

                    plt.figure(figsize=(fix, fiy))
                    plt.yscale('log')

                    # if (Q_x - Q_x_nat) > 1e-5:
                    #     plt.plot([Q_x, Q_x], [1e-10,1e10], ls='--', lw=1.2, c='grey')
                    #     plt.text(Q_x, 1e0, r'(1,0)_{D}', fontsize=size2)
                    # plt.plot([Q_x_nat, Q_x_nat], [1e-10,1e10], ls='--', lw=1.2, c='grey')
                    # plt.text(Q_x_nat, 0.1e0, r'(1,0)', fontsize=size2)
                    
                    # if (Q_y - Q_y_nat) > 1e-5:
                    #     plt.plot([Q_y, Q_y], [1e-10,1e10], ls='--', lw=1.2, c='grey')
                    #     plt.text(Q_y, 1e0, r'(0,1)_{D}', fontsize=size2)
                    # plt.plot([Q_y_nat, Q_y_nat], [1e-10,1e10], ls='--', lw=1.2, c='grey')
                    # plt.text(Q_y_nat, 0.1e0, r'(0,1)', fontsize=size2)
                    

                    plt.plot(1-freqx, ampx*1e3, lw=1, label='X')
                    plt.plot(1-freqy, ampy*1e3, lw=1, label='Y')

                    plt.xlabel(str(bpm)+ ': Fractional Tune [-]', fontsize=size)
                    plt.ylabel('Amplitude [mm]', fontsize=size)
                    plt.tick_params('both', labelsize=size)
                    plt.legend(fontsize=size, ncol=3, fancybox=True,  numpoints=1, scatterpoints = 1)
                    plt.ylim(1e-5, 5e0)
                    plt.xlim(0.5, max(1-freqx))
                    plt.tight_layout()
                    plt.show()
                    pdf.savefig()
                    plt.close()


                elif bpm in bpmsx:
                    indx = bpmsx.index(bpm)

                    ampx = read_spectrum(os.path.join(harmonic_output, sdds+'.ampsx'), indx)
                    freqx = read_spectrum(os.path.join(harmonic_output, sdds+'.freqsx'), indx)
                    
                    plt.figure(figsize=(fix, fiy))
                    plt.yscale('log')
                    plt.plot(1-freqx, ampx*1e3, lw=1, label='X')
                    #plt.plot(1-freqy, ampy*1e3, lw=1, label='liny')
                    plt.xlabel(str(bpm)+ ': Fractional Tune [-]', fontsize=size)
                    plt.ylabel('Amplitude [mm]', fontsize=size)
                    plt.tick_params('both', labelsize=size)
                    plt.legend(fontsize=size, ncol=3, fancybox=True,  numpoints=1, scatterpoints = 1)
                    #plt.ylim(5e2*min(amp*1e3), 1.3*max(amp*1e3))
                    plt.xlim(0.5, max(1-freqx))
                    plt.tight_layout()
                    pdf.savefig()
                    plt.close()
                    
                elif bpm in bpmsy:
                    indy = bpmsy.index(bpm)

                    ampy = read_spectrum(os.path.join(harmonic_output, sdds+'.ampsy'), indy)
                    freqy = read_spectrum(os.path.join(harmonic_output, sdds+'.freqsy'), indy)

                    plt.figure(figsize=(fix, fiy))
                    plt.yscale('log')
                    #plt.plot(1-freqx, ampx*1e3, lw=1, label=str(bpms[j])+' linx')
                    plt.plot(1-freqy, ampy*1e3, lw=1, label='Y')
                    plt.xlabel(str(bpm)+ ': Fractional Tune [-]', fontsize=size)
                    plt.ylabel('Amplitude [mm]', fontsize=size)
                    plt.tick_params('both', labelsize=size)
                    plt.legend(fontsize=size, ncol=3, fancybox=True,  numpoints=1, scatterpoints = 1)
                    #plt.ylim(5e2*min(amp*1e3), 1.3*max(amp*1e3))
                    plt.xlim(0.5, max(1-freqy))
                    plt.tight_layout()
                    pdf.savefig()
                    plt.close()

                else:
                    plt.figure(figsize=(fix, fiy))
                    plt.yscale('log')
                    #plt.plot(1-freqx, ampx*1e3, lw=1, label=str(bpms[j])+' linx')
                    #plt.plot(1-freqy, ampy*1e3, lw=1, label=str(bpm)+' liny')
                    plt.plot([0.6,0.6], [1,1], c='white')
                    plt.xlabel(str(bpm)+ ': Fractional Tune [-]', fontsize=size)
                    plt.ylabel('Amplitude [mm]', fontsize=size)
                    plt.tick_params('both', labelsize=size)
                    plt.legend(fontsize=size, ncol=3, fancybox=True,  numpoints=1, scatterpoints = 1)
                    #plt.ylim(5e2*min(amp*1e3), 1.3*max(amp*1e3))
                    plt.xlim(0.5, 1.0)
                    plt.tight_layout()
                    pdf.savefig()
                    plt.close()
                    

    quit()

    

    num=1
    plt.figure(num, figsize=(fix, fiy))
    plt.scatter(1-freq, amp*1e3, s=5, marker='o')
    plt.plot(np.array([Qx, Qx]), np.array([1e-10, 1e10]), ls='--', color = 'orange', lw = 2)
    plt.plot(np.array([Qy, Qy]), np.array([1e-10, 1e10]), ls='--', color = 'orange', lw = 2)
    plt.xlabel('Fractional Tune [-]', fontsize=size)
    plt.ylabel('Amplitude [mm]', fontsize=size)
    plt.tick_params('both', labelsize=size)
    plt.yscale('log')
    plt.ylim(5e2*min(amp*1e3), 1.3*max(amp*1e3))
    plt.xlim(0.5, max(1-freq))
    plt.tight_layout()
    plt.savefig(options.sdds+'../FrequencySpectrum_'+options.axis+'.'+options.pngpdf)
    plt.close(num)
    num=num+1

    plt.figure(num, figsize=(fix, fiy))
    plt.scatter(1-freq, amp*1e3, s=5, marker='o')
    plt.plot(np.array([Qx, Qx]), np.array([1e-10, 1e10]), ls='--', color = 'orange', lw = 2)
    plt.plot(np.array([Qy, Qy]), np.array([1e-10, 1e10]), ls='--', color = 'orange', lw = 2)
    plt.xlabel('Fractional Tune [-]', fontsize=size)
    plt.ylabel('Amplitude [mm]', fontsize=size)
    plt.tick_params('both', labelsize=size)
    plt.yscale('log')
    plt.ylim(5e2*min(amp*1e3), 1.3*max(amp*1e3))
    # plt.ylim(5e2*min(amp/(max(amp))), 1.3)
    plt.tight_layout()
    plt.xlim(Qx-0.01, Qx+0.01)
    plt.savefig(options.sdds+'../FrequencySpectrum_QxZoom_'+options.axis+'.'+options.pngpdf)
    plt.close(num)
    num=num+1

    plt.figure(num, figsize=(fix, fiy))
    plt.scatter(1-freq, amp*1e3, s=5, marker='o')
    plt.plot(np.array([Qx, Qx]), np.array([1e-10, 1e10]), ls='--', color = 'orange', lw = 2)
    plt.plot(np.array([Qy, Qy]), np.array([1e-10, 1e10]), ls='--', color = 'orange', lw = 2)
    plt.xlabel('Fractional Tune [-]', fontsize=size)
    plt.ylabel('Amplitude [mm]', fontsize=size)
    plt.tick_params('both', labelsize=size)
    plt.yscale('log')
    plt.ylim(5e2*min(amp*1e3), 1.3*max(amp*1e3))
    # plt.ylim(5e2*min(amp/(max(amp))), 1.3)
    plt.tight_layout()
    plt.xlim(Qy-0.01, Qy+0.01)
    plt.savefig(options.sdds+'../FrequencySpectrum_QyZoom_'+options.axis+'.'+options.pngpdf)
    plt.close(num)
    num=num+1

    
