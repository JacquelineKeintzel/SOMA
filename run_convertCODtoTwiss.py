'''
Script to convert closed orbit distortion (COD) measurements of
given timestamp to file in TFS format including beta-functions
and phase advances.


--betafile
should be the timestamp e.g.:
/nfs/sadnas1a/ldata/SuperKEKB/KCG/HER/MeasOpt/2019/11/BETA_RAW_2019_11_21_17:58:18

--dispfile
should be the timestamp e.g.:
/nfs/sadnas1a/ldata/SuperKEKB/KCG/HER/MeasOpt/2019/11/DISP_2019_11_12_12:40:54

--coupfile
should be the timestamp e.g.:
/nfs/sadnas1a/ldata/SuperKEKB/KCG/HER/MeasOpt/2019/11/XYC_2019_11_29_15:41:16

--outputfile
path to the new TFS file

--ring
ringID, HER or LER

--model
path to model directory

The SAD scripts are written by H. Sugimoto.
It is called and generated a file in sad format with the following
structure:

beta is a llist of {BPM,BX,BY,PHIX,PHIY,Flag}.
Flag is validity of data
tune is a ist of measured tune {NUX,NUY}.

This file is then read by python (3) and converted to tfs format.

The files extract_dispersionCOD.mask and extract_couplingCOD.mask
are base on scripts obtained from Koiso-san.

The converison to a twiss format is then done by python 3.


Author: Jacqueline Keintzel
Date: 09/12/2019

'''

import os
import numpy as np 
from optparse import OptionParser
import pandas as pd 
import tfs
import matplotlib.pyplot as plt

parser = OptionParser()
parser.add_option("-b", "--beta",  dest="betafile", help="SAD timestamp of COD measurements for beta.", action="store")
parser.add_option("-d", "--disp",  dest="dispfile", help="SAD timestamp of COD measurements for dispersion.", action="store")
parser.add_option("-c", "--coup",  dest="coupfile", help="SAD timestamp of COD measurements for coupling.", action="store")
parser.add_option("-r", "--ring",  dest="ring", help="RingID, either HER or LER.", action="store")
parser.add_option("-o", "--output",  dest="outputdir", help="Directory containing beta-functions and phase advances obtained from COD.", action="store")
parser.add_option("-m", "--model",  dest="model", help="Path to twiss elements model.", action="store")
(options, args) = parser.parse_args()


if options.betafile is not None:
    with open('extract_betaphaseCOD.mask') as mask: reader = mask.read()
    mask.close()
    script = reader % {'RING' : options.ring }
    with open('COD_extract_betaphse.sad', 'w') as ff:  ff.write(script)
    ff.close

    os.system('/SAD/bin/gs -env skekb'+
                ' COD_extract_betaphse.sad ' +
                str(options.betafile) )

    with open('COD_Beta_Phase.txt') as fo:
        beta_sad = fo.readlines()
    fo.close()

    bpms = []
    betx = []
    bety = []
    mux = []
    muy = []
    nextone = False



    for i in range(len(beta_sad)):
        split_left = beta_sad[i].split('{')
        for j in range(len(split_left)):
            split_right = split_left[j].split('}')
            for k in range(len(split_right)):
                split_colon = split_right[k].split(',')
                if 'MQ' in split_colon[0] and len(split_colon)>5:
                    bpms.append(str(split_colon[0])[1:-1])
                    betx.append(float(split_colon[1]))
                    bety.append(float(split_colon[2]))
                    mux.append(float(split_colon[3])/(2*np.pi))
                    muy.append(float(split_colon[4])/(2*np.pi))
                if nextone == True:
                    tunex = float(split_colon[0])
                    tuney = float(split_colon[1])
                    nextone=False
                if 'Tune' in split_colon[0]: nextone = True
                
    with open(os.path.join(options.model, 'twiss_elements.dat')) as fo:
        tw = fo.readlines()
    fo.close

    tw_bpms = [tw[13+i].split()[0] for i in range(len(tw[13:]))]
    tw_s = [tw[13+i].split()[2] for i in range(len(tw[13:]))]
    tw_betx = [tw[13+i].split()[4] for i in range(len(tw[13:]))]
    tw_bety = [tw[13+i].split()[5] for i in range(len(tw[13:]))]

    positions = []
    for pos, bpm in enumerate(tw_bpms):
        if bpm in bpms: 
            positions.append(pos)


    bpms_s = []
    mdl_betx = []
    mdl_bety = []
    for pos in positions: 
        bpms_s.append(float(tw_s[pos]))
        mdl_betx.append(float(tw_betx[pos]))
        mdl_bety.append(float(tw_bety[pos]))


    # plt.scatter(bpms_s, (np.array(betx)-np.array(mdl_betx))/np.array(mdl_betx))
    # plt.scatter(bpms_s, (np.array(bety)-np.array(mdl_bety))/np.array(mdl_bety))
 

    df = pd.DataFrame(zip(bpms_s, betx, (np.array(betx)-np.array(mdl_betx))/np.array(mdl_betx), bety, (np.array(bety)-np.array(mdl_bety))/np.array(mdl_bety), mux, muy), columns = ['S', 'BETX', 'DELTABETX', 'BETY', 'DELTABETY', 'MUX', 'MUY'], index=bpms)
    tfs.write(os.path.join(str(options.outputdir),'COD_betxy_muxy.tfs'), df, save_index=True )

    
if options.dispfile is not None:
    with open('extract_dispersionCOD.mask') as mask: reader = mask.read()
    mask.close()
    script = reader % {'RING' : options.ring,
                        'DISP_FILE' : options.dispfile }
    with open('COD_extract_dispersion.sad', 'w') as ff: ff.write(script)
    ff.close()

    os.system('/SAD/bin/gs -env skekb ' + 
                ' COD_extract_dispersion.sad')

    with open('COD_Dispersion.txt') as fo:
        disp_sad = fo.readlines()
    fo.close()

    bpms = []
    dx = []
    dy = []
    
    for i in range(len(disp_sad)):
        split_left = disp_sad[i].split('{')
        for j in range(len(split_left)):
            split_right = split_left[j].split('}')
            for k in range(len(split_right)):
                split_colon = split_right[k].split(',')
                if 'MQ' in split_colon[0] and len(split_colon)>3:
                    bpms.append(str(split_colon[0])[1:-1])
                    dx.append(float(split_colon[1])*1e-3)
                    dy.append(float(split_colon[2])*1e-3)


    with open(os.path.join(options.model, 'twiss_elements.dat')) as fo:
        tw = fo.readlines()
    fo.close

    tw_bpms = [tw[13+i].split()[0] for i in range(len(tw[13:]))]
    tw_s = [tw[13+i].split()[2] for i in range(len(tw[13:]))]
    tw_dx = [tw[13+i].split()[10] for i in range(len(tw[13:]))]
    tw_dy = [tw[13+i].split()[11] for i in range(len(tw[13:]))]

    positions = []
    for pos, bpm in enumerate(tw_bpms):
        if bpm in bpms: 
            positions.append(pos)


    bpms_s = []
    mdl_dx = []
    mdl_dy = []
    for pos in positions: 
        bpms_s.append(float(tw_s[pos]))
        mdl_dx.append(float(tw_dx[pos]))
        mdl_dy.append(float(tw_dy[pos]))

    # plt.plot(bpms_s, np.array(dx))
    # plt.plot(bpms_s, np.array(dy))
    # plt.show()

    df = pd.DataFrame(zip(bpms_s, dx, (np.array(dx)-np.array(mdl_dx))/np.array(mdl_dx), dy, (np.array(dy)-np.array(mdl_dy))/np.array(mdl_dy)), columns = ['S', 'DX', 'DELTADX', 'DY', 'DELTADY'], index=bpms)
    tfs.write(os.path.join(str(options.outputdir),'COD_dxy.tfs'), df, save_index=True )


if options.coupfile is not None:
    pass
