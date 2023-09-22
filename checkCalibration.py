"""
Calculated BPM calibration by using beta_phase and 
beta_amplitude. Calibration factors are applied to lin files
and written in a new folder.
"""

from __future__ import print_function
from optparse import OptionParser
import numpy as np 
import os
import pandas
from func import get_dict_colormap, read_bpms, read_bet_phase, read_bet_amp, reject_outliers
import sys
# sys.path.append('/afs/cern.ch/work/j/jkeintze/public/Beta-Beat.src/')
# from tfs_files import tfs_pandas
import tfs




if __name__ == "__main__":
    
    parser = OptionParser()
    parser.add_option("-s", "--sdds",  dest="sdds", help="Folder of sdds files, leades to other folders.", action="store")
    parser.add_option("-p", "--plane",  dest="plane", help="Transverse plane, either x or y.", action="store")
    parser.add_option("-r", "--ring",  dest="ring", help="Ring ID, HER or LER", action="store")
    (options, args) = parser.parse_args()

    all_sdds = [sd for sd in os.listdir(options.sdds) if '.sdds' in sd[-5:]]
    all_bpms = read_bpms(os.path.join(options.sdds, all_sdds[0]))

    synched_harmonic_output = os.path.join(options.sdds[:-13], 'synched_harmonic')
    synched_phase_output = os.path.join(options.sdds[:-13], 'synched_optics')
    calibrated_harmonic_output = os.path.join(options.sdds[:-13], 'calibrated_harmonic')


    df = {}
    df2 = {}
  

    for sdds in all_sdds:
        df[sdds] = []
        df2[sdds] = []

        folder = os.path.join(synched_phase_output, sdds)
        beta_phase, beta_phase_err, bpms = read_bet_phase(folder, options.plane)
        beta_amp, beta_amp_err = read_bet_amp(folder, options.plane)
            

        cal = [(beta_phase[i]/beta_amp[i]) for i in range(len(beta_phase))]
        cal_err = [(beta_phase_err[i]**2 / (4*beta_amp[i]*beta_phase[i]) + beta_amp_err[i]**2 * beta_phase[i] / (4*beta_amp[i]**3)) for i in range(len(beta_phase))]
        
        for bpm in all_bpms:
            try:
                df[sdds].append(get_dict_colormap(bpms, cal)[bpm])
                df2[sdds].append(get_dict_colormap(bpms, cal_err)[bpm])
            except KeyError:
                df[sdds].append(np.nan)
                df2[sdds].append(np.nan)


    df = pandas.DataFrame(df, index=all_bpms)
    df=df.T
    df2 = pandas.DataFrame(df2, index=all_bpms)
    df2=df2.T

    tfs.write(options.sdds + '../CalibrationSquareBPM_'+options.plane+'.tfs', df, save_index=True)
    tfs.write(options.sdds + '../CalibrationErrorSquareBPM_'+options.plane+'.tfs', df, save_index=True)

    av_cal_bpms = []
    av_cal_err_bpms = []

    for bpm in all_bpms:
        av_cal = [np.sqrt(df[bpm][i]) for i in range(len(all_sdds)) if not np.isnan(df[bpm][i]) and df[bpm][i] >= 0  ]
        av_cal_err = [np.sqrt(df2[bpm][i]) for i in range(len(all_sdds)) if not np.isnan(df2[bpm][i]) and df2[bpm][i] >= 0 ]

        av_cal = reject_outliers(av_cal)
        av_cal_err = reject_outliers(av_cal_err)

        av_cal_bpms.append(1) if np.isnan(np.mean(av_cal)) else av_cal_bpms.append(np.mean(av_cal)) 
        av_cal_err_bpms.append(1) if np.isnan(np.mean(av_cal_err)) else av_cal_err_bpms.append(np.mean(av_cal_err)) 

    
    df_calibration = pandas.DataFrame(zip(all_bpms, av_cal_bpms, av_cal_err_bpms), columns=['NAME', 'CALIBRATION', 'ERROR_CALIBRATION'])
    
    tfs.write(options.sdds + '../calibration_'+options.plane+'.tfs', df_calibration, save_index=False)

    if not os.path.exists(calibrated_harmonic_output):
        os.system('mkdir ' + calibrated_harmonic_output)
    else: pass

    if os.path.exists(synched_harmonic_output) == False:
        print(" ********************************************\n",
                "There is no synched_harmonic for calibration..\n",
                " I stop now.\n",
                "********************************************")
        sys.exit()
    else: pass


    lins = [lin for lin in os.listdir(synched_harmonic_output) if 'lin'+options.plane in lin]
    for lin in lins:
        df_lin = tfs.read(os.path.join(synched_harmonic_output, lin))
        df_lin['AMP'+options.plane.upper()] = df_lin['AMP'+options.plane.upper()]*df_calibration['CALIBRATION']
        df_lin['ERRAMP'+options.plane.upper()] = df_lin['AMP'+options.plane.upper()]*df_calibration['ERROR_CALIBRATION']
        tfs.write(os.path.join(calibrated_harmonic_output, lin), df_lin, save_index=False)

    print(" ********************************************\n",
            "BPM calibration finished.\n",
            "Lin files are stored in " +calibrated_harmonic_output+ "\n",
            "********************************************")
